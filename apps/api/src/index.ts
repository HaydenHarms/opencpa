import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { z } from 'zod';
import { mcqVariant, toPublicMcq, toPublicTbs, variantCount, type Item } from '@opencpa/schema';
import {
  AREA_WEIGHTS,
  DIAGNOSTIC_SIZE,
  gradeMcq,
  gradeSimulation,
  masteryByArea,
  masteryByTopic,
  newCard,
  ratingFor,
  ratingForScore,
  review,
  selectDiagnosticItems,
  selectPracticeItems,
  simulationCount,
  spreadThrough,
  type Card,
  type GradeResult,
} from '@opencpa/engine';
import { byId, items, mcqs, simulations } from './content';
import { handleMcp, hashToken, newToken } from './mcp';
import {
  checkSession,
  completeIfDone,
  hasMcqAttempts,
  loadSession,
  pickVariants,
  reveal,
  revealSimulation,
  sessionVariant,
  sessionView,
  type SessionRow,
} from './sessions';

type Env = { DB: D1Database; ALLOWED_ORIGINS: string };
type Vars = { userId: string };

const app = new Hono<{ Bindings: Env; Variables: Vars }>();

/** ALLOWED_ORIGINS entries are exact origins or wildcards like https://*.opencpa.pages.dev. */
function originAllowed(origin: string, allowed: string): boolean {
  return allowed.split(',').some((raw) => {
    const rule = raw.trim();
    if (!rule.includes('*')) return rule === origin;
    const re = new RegExp(
      '^' + rule.replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace('*', '[a-z0-9-]+') + '$',
    );
    return re.test(origin);
  });
}

app.use('*', (c, next) =>
  cors({
    origin: (origin) => (originAllowed(origin, c.env.ALLOWED_ORIGINS) ? origin : null),
    allowHeaders: ['Content-Type', 'X-OpenCPA-User'],
  })(c, next),
);

app.get('/health', (c) => c.json({ ok: true, items: items.length }));

/** Question list. Answers and rationales never leave the server. */
app.get('/questions', (c) => {
  const section = c.req.query('section')?.toUpperCase();
  const topic = c.req.query('topic');
  const list = mcqs
    .filter(
      (q) =>
        (!section || q.blueprint.section === section) && (!topic || q.blueprint.topic === topic),
    )
    .map(toPublicMcq);
  return c.json(list);
});

app.get('/questions/:id', (c) => {
  const q = byId.get(c.req.param('id'));
  if (!q || q.type !== 'mcq') return c.json({ error: 'not found' }, 404);
  return c.json(toPublicMcq(q));
});

/** Simulation list and detail. Answers, tolerances and explanations never leave the server. */
app.get('/simulations', (c) => {
  const section = c.req.query('section')?.toUpperCase();
  return c.json(
    simulations.filter((t) => !section || t.blueprint.section === section).map(toPublicTbs),
  );
});

app.get('/simulations/:id', (c) => {
  const t = byId.get(c.req.param('id'));
  if (!t || t.type !== 'tbs') return c.json({ error: 'not found' }, 404);
  return c.json(toPublicTbs(t));
});

// Everything below needs a student id. Until auth lands, the browser sends an anonymous device id.
const userIdSchema = z.string().uuid();
app.use('/me/*', async (c, next) => {
  const parsed = userIdSchema.safeParse(c.req.header('X-OpenCPA-User'));
  if (!parsed.success) return c.json({ error: 'missing or invalid X-OpenCPA-User header' }, 401);
  await c.env.DB.prepare('INSERT OR IGNORE INTO users (id) VALUES (?)').bind(parsed.data).run();
  c.set('userId', parsed.data);
  await next();
});

const attemptBody = z.object({
  itemId: z.string(),
  selected: z.string().regex(/^[A-F]$/),
  lowConfidence: z.boolean().optional(),
  durationMs: z.number().int().nonnegative().optional(),
  sessionId: z.string().uuid().optional(),
  /** The version answered, outside a session. In a session the session decides. */
  variant: z.number().int().min(0).max(9).optional(),
});

app.post('/me/attempts', async (c) => {
  const body = attemptBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  const { itemId, selected, lowConfidence, durationMs, sessionId } = body.data;
  const item = byId.get(itemId);
  if (!item || item.type !== 'mcq') return c.json({ error: 'unknown item' }, 404);

  const userId = c.get('userId');
  const check = await checkSession(c.env.DB, userId, sessionId, itemId);
  if ('error' in check) return c.json({ error: check.error }, check.status);
  const variant = check.session ? sessionVariant(check.session, itemId) : (body.data.variant ?? 0);
  if (variant >= variantCount(item)) return c.json({ error: 'unknown variant' }, 400);
  const version = mcqVariant(item, variant);
  const result = gradeMcq(version, selected);
  const now = new Date();

  const row = await c.env.DB.prepare('SELECT * FROM review_cards WHERE user_id = ? AND item_id = ?')
    .bind(userId, itemId)
    .first<CardRow>();
  const card = review(
    row ? rowToCard(row) : newCard(now),
    ratingFor(result.correct, lowConfidence),
    now,
  );

  await saveAttempt(
    c.env.DB,
    userId,
    item,
    { selected },
    result,
    durationMs,
    card,
    sessionId,
    variant,
  );
  const sessionComplete = await completeIfDone(c.env.DB, check.session);

  // Answer and explanation are revealed only after an attempt is recorded.
  return c.json({
    ...result,
    ...reveal(version, selected, result.correct),
    nextDue: card.due.toISOString(),
    sessionComplete,
  });
});

const cents = z.number().int().nonnegative();
const taskResponse = z.discriminatedUnion('type', [
  z.object({ type: z.literal('numeric'), value: z.number().finite() }),
  z.object({
    type: z.literal('journal_entry'),
    lines: z
      .array(z.object({ account: z.string(), debit: cents.optional(), credit: cents.optional() }))
      .max(20),
  }),
  z.object({ type: z.literal('research'), citation: z.string().max(100) }),
]);
const simulationAttemptBody = z.object({
  responses: z.record(taskResponse),
  durationMs: z.number().int().nonnegative().optional(),
  sessionId: z.string().uuid().optional(),
});

app.post('/me/simulations/:id/attempts', async (c) => {
  const body = simulationAttemptBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  const item = byId.get(c.req.param('id'));
  if (!item || item.type !== 'tbs') return c.json({ error: 'unknown simulation' }, 404);

  const userId = c.get('userId');
  const { responses, durationMs, sessionId } = body.data;
  const check = await checkSession(c.env.DB, userId, sessionId, item.id);
  if ('error' in check) return c.json({ error: check.error }, check.status);
  const result = gradeSimulation(item, responses);
  const now = new Date();
  const row = await c.env.DB.prepare('SELECT * FROM review_cards WHERE user_id = ? AND item_id = ?')
    .bind(userId, item.id)
    .first<CardRow>();
  const card = review(
    row ? rowToCard(row) : newCard(now),
    ratingForScore(result.possible ? result.earned / result.possible : 0),
    now,
  );
  await saveAttempt(c.env.DB, userId, item, responses, result, durationMs, card, sessionId);
  const sessionComplete = await completeIfDone(c.env.DB, check.session);

  // Answers and explanations are revealed only after an attempt is recorded.
  return c.json({
    ...revealSimulation(item, responses),
    nextDue: card.due.toISOString(),
    sessionComplete,
  });
});

app.get('/me/review/due', async (c) => {
  const { results } = await c.env.DB.prepare(
    'SELECT item_id FROM review_cards WHERE user_id = ? AND due <= ? ORDER BY due LIMIT 50',
  )
    .bind(c.get('userId'), Date.now())
    .all<{ item_id: string }>();
  const due = results.map((r) => byId.get(r.item_id)).filter((i) => i?.type === 'mcq');
  return c.json(due.map((q) => toPublicMcq(q as never)));
});

app.get('/me/mastery', async (c) => {
  const { results } = await c.env.DB.prepare(
    'SELECT section, area, correct, created_at FROM attempts WHERE user_id = ?',
  )
    .bind(c.get('userId'))
    .all<{ section: string; area: string; correct: number; created_at: number }>();
  return c.json(
    masteryByArea(
      results.map((r) => ({
        section: r.section,
        area: r.area,
        correct: !!r.correct,
        at: r.created_at,
      })),
    ),
  );
});

/**
 * Practice sessions. The server picks the questions (`packages/engine/src/selection.ts`),
 * and progress is the set of attempts tagged with the session id, so a student can
 * leave and come back.
 */
const sectionSchema = z.enum(['FAR', 'AUD', 'REG', 'BAR', 'ISC', 'TCP']);

app.get('/me/sessions/current', async (c) => {
  const section = sectionSchema.safeParse(c.req.query('section')?.toUpperCase());
  if (!section.success) return c.json({ error: 'unknown section' }, 400);
  const userId = c.get('userId');
  const topic = c.req.query('topic') || null;
  const inScope = (i: Item) =>
    i.blueprint.section === section.data && (!topic || i.blueprint.topic === topic);
  const row = await c.env.DB.prepare(
    `SELECT * FROM practice_sessions WHERE user_id = ? AND section = ? AND status = 'active'
     AND topic IS ? ORDER BY created_at DESC LIMIT 1`,
  )
    .bind(userId, section.data, topic)
    .first<SessionRow>();
  const poolSize = mcqs.filter(inScope).length;
  const simPool = simulations.filter(inScope).length;
  // A topic session from the Library never starts with the section diagnostic.
  const diagnostic = !topic && !(await hasMcqAttempts(c.env.DB, userId, section.data));
  // The session lengths on offer, each with the simulations that come with it.
  const option = (n: number) => ({ questions: n, simulations: simulationCount(n, simPool) });
  const lengths = SESSION_LENGTHS.filter((n) => n < poolSize);
  if (poolSize) lengths.push(Math.min(poolSize, SESSION_LENGTHS[SESSION_LENGTHS.length - 1]!));
  return c.json({
    session: row ? await sessionView(c.env.DB, row) : null,
    nextKind: diagnostic ? 'diagnostic' : 'practice',
    diagnostic: option(Math.min(DIAGNOSTIC_SIZE, poolSize)),
    options: [...new Set(lengths)].map(option),
    poolSize,
  });
});

const SESSION_LENGTHS = [10, 25, 50];

const newSessionBody = z.object({
  section: sectionSchema,
  size: z.number().int().min(1).max(100),
  /** Library: limit the session to one blueprint topic. */
  topic: z.string().min(1).max(200).optional(),
});

app.post('/me/sessions', async (c) => {
  const body = newSessionBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  const { section, size } = body.data;
  const topic = body.data.topic ?? null;
  const userId = c.get('userId');
  const db = c.env.DB;

  const toPool = (i: Item) => ({ id: i.id, area: i.blueprint.area, topic: i.blueprint.topic });
  const inScope = (i: Item) =>
    i.blueprint.section === section && (!topic || i.blueprint.topic === topic);
  const pool = mcqs.filter(inScope).map(toPool);
  const simPool = simulations.filter(inScope).map(toPool);
  if (pool.length === 0 && (!topic || simPool.length === 0))
    return c.json({ error: `no ${topic ?? section} questions yet` }, 404);

  const weights = AREA_WEIGHTS[section];
  let kind: 'diagnostic' | 'practice';
  let ids: string[];
  let simIds: string[];
  if (!topic && !(await hasMcqAttempts(db, userId, section))) {
    kind = 'diagnostic';
    ids = selectDiagnosticItems(pool, DIAGNOSTIC_SIZE, weights);
    simIds = selectDiagnosticItems(simPool, simulationCount(ids.length, simPool.length), weights);
  } else {
    kind = 'practice';
    const [cards, attempts] = await Promise.all([
      db
        .prepare('SELECT item_id, due FROM review_cards WHERE user_id = ?')
        .bind(userId)
        .all<{ item_id: string; due: number }>(),
      db
        .prepare(
          'SELECT item_id, correct, created_at FROM attempts WHERE user_id = ? AND section = ?',
        )
        .bind(userId, section)
        .all<{ item_id: string; correct: number; created_at: number }>(),
    ]);
    const history = {
      weights,
      due: new Map(cards.results.map((r) => [r.item_id, r.due])),
      topicScore: masteryByTopic(
        attempts.results.flatMap((r) => {
          const item = byId.get(r.item_id);
          return item
            ? [{ topic: item.blueprint.topic, correct: !!r.correct, at: r.created_at }]
            : [];
        }),
      ),
    };
    ids = selectPracticeItems({ ...history, pool, size });
    simIds = selectPracticeItems({
      ...history,
      pool: simPool,
      // A topic with simulations but no questions yet still gets one simulation.
      size: ids.length ? simulationCount(ids.length, simPool.length) : Math.min(1, simPool.length),
    });
  }
  // Simulations are spread through the questions (exam-day mode will use the exam's order).
  ids = spreadThrough(ids, simIds);
  const variants = await pickVariants(db, userId, ids);

  // Starting a new session abandons any unfinished one in the same section (or the same
  // Library topic). Its answers still count toward mastery and review scheduling.
  const id = crypto.randomUUID();
  await db.batch([
    db
      .prepare(
        `UPDATE practice_sessions SET status = 'abandoned'
         WHERE user_id = ? AND section = ? AND status = 'active' AND topic IS ?`,
      )
      .bind(userId, section, topic),
    db
      .prepare(
        'INSERT INTO practice_sessions (id, user_id, section, kind, item_ids, variants, topic) VALUES (?, ?, ?, ?, ?, ?, ?)',
      )
      .bind(id, userId, section, kind, JSON.stringify(ids), JSON.stringify(variants), topic),
  ]);
  const row = await loadSession(db, userId, id);
  return c.json(await sessionView(db, row!), 201);
});

app.get('/me/sessions/:id', async (c) => {
  const id = z.string().uuid().safeParse(c.req.param('id'));
  const row = id.success ? await loadSession(c.env.DB, c.get('userId'), id.data) : null;
  if (!row) return c.json({ error: 'not found' }, 404);
  return c.json(await sessionView(c.env.DB, row));
});

/**
 * Library: every exam, its blueprint topics, and the full archive of reviewed items, with
 * the student's own progress on each. Only public fields leave the server; an item's key
 * is revealed only through the student's own past attempts.
 */
type AttemptLite = {
  item_id: string;
  correct: number;
  earned: number;
  possible: number;
  created_at: number;
};

async function userAttempts(db: D1Database, userId: string) {
  const { results } = await db
    .prepare(
      'SELECT item_id, correct, earned, possible, created_at FROM attempts WHERE user_id = ? ORDER BY created_at',
    )
    .bind(userId)
    .all<AttemptLite>();
  return results;
}

app.get('/me/library', async (c) => {
  const attempts = await userAttempts(c.env.DB, c.get('userId'));
  const byItem = new Map<string, AttemptLite[]>();
  for (const a of attempts) byItem.set(a.item_id, [...(byItem.get(a.item_id) ?? []), a]);
  const topicMastery = masteryByTopic(
    attempts.flatMap((a) => {
      const item = byId.get(a.item_id);
      return item
        ? [
            {
              topic: `${item.blueprint.section}::${item.blueprint.topic}`,
              correct: !!a.correct,
              at: a.created_at,
            },
          ]
        : [];
    }),
  );

  const sections = SECTION_LIST.map((section) => {
    const inSection = items.filter((i) => i.blueprint.section === section);
    const topics = new Map<
      string,
      {
        area: string;
        topic: string;
        questions: number;
        simulations: number;
        seen: number;
        attempts: number;
      }
    >();
    for (const i of inSection) {
      const t = topics.get(i.blueprint.topic) ?? {
        area: i.blueprint.area,
        topic: i.blueprint.topic,
        questions: 0,
        simulations: 0,
        seen: 0,
        attempts: 0,
        correct: 0,
      };
      if (i.type === 'mcq') t.questions++;
      else t.simulations++;
      const n = byItem.get(i.id)?.length ?? 0;
      if (n) t.seen++;
      t.attempts += n;
      t.correct += byItem.get(i.id)?.filter((a) => a.correct).length ?? 0;
      topics.set(i.blueprint.topic, t);
    }
    const list = [...topics.values()]
      .map((t) => ({
        ...t,
        mastery: t.attempts ? (topicMastery.get(`${section}::${t.topic}`) ?? 0) : null,
      }))
      .sort((a, b) => a.area.localeCompare(b.area) || a.topic.localeCompare(b.topic));
    const seen = inSection.filter((i) => byItem.has(i.id)).length;
    const sectionAttempts = inSection.flatMap((i) => byItem.get(i.id) ?? []);
    return {
      section,
      questions: inSection.filter((i) => i.type === 'mcq').length,
      simulations: inSection.filter((i) => i.type === 'tbs').length,
      seen,
      attempts: sectionAttempts.length,
      accuracy: sectionAttempts.length
        ? sectionAttempts.filter((a) => a.correct).length / sectionAttempts.length
        : null,
      topics: list,
    };
  });
  return c.json(sections);
});

app.get('/me/library/items', async (c) => {
  const section = sectionSchema.safeParse(c.req.query('section')?.toUpperCase());
  if (!section.success) return c.json({ error: 'unknown section' }, 400);
  const topic = c.req.query('topic');
  const attempts = await userAttempts(c.env.DB, c.get('userId'));
  const list = items
    .filter((i) => i.blueprint.section === section.data && (!topic || i.blueprint.topic === topic))
    .map((i) => {
      const mine = attempts.filter((a) => a.item_id === i.id);
      const last = mine[mine.length - 1];
      return {
        id: i.id,
        type: i.type,
        blueprint: i.blueprint,
        /** A short preview: the simulation title, or the start of the question stem. */
        title:
          i.type === 'tbs'
            ? i.title
            : i.stem.length > 180
              ? i.stem.slice(0, 177).trimEnd() + '…'
              : i.stem,
        attempts: mine.length,
        lastCorrect: last ? !!last.correct : null,
        lastScore: last && last.possible ? last.earned / last.possible : null,
        lastAt: last?.created_at ?? null,
      };
    });
  return c.json(list);
});

/**
 * One archive question. `item` is the version to answer next (rotating through the
 * variants like a session does); `last` reveals the student's most recent attempt,
 * with the version they actually saw.
 */
app.get('/me/library/items/:id', async (c) => {
  const item = byId.get(c.req.param('id'));
  if (!item || item.type !== 'mcq') return c.json({ error: 'not found' }, 404);
  const { results } = await c.env.DB.prepare(
    'SELECT response, correct, variant, created_at FROM attempts WHERE user_id = ? AND item_id = ? ORDER BY created_at',
  )
    .bind(c.get('userId'), item.id)
    .all<{ response: string; correct: number; variant: number; created_at: number }>();
  const nextVariant = results.length % variantCount(item);
  const lastRow = results[results.length - 1];
  let last = null;
  if (lastRow) {
    const { selected } = JSON.parse(lastRow.response) as { selected: string };
    last = {
      item: toPublicMcq(item, lastRow.variant),
      at: lastRow.created_at,
      ...reveal(mcqVariant(item, lastRow.variant), selected, !!lastRow.correct),
    };
  }
  return c.json({
    item: toPublicMcq(item, nextVariant),
    attempts: results.length,
    correct: results.filter((r) => r.correct).length,
    last,
  });
});

const SECTION_LIST = sectionSchema.options;

/**
 * Claude connector link. The student adds `<api>/mcp/<token>` as a custom connector in
 * Claude; the token maps to their id. Treat it like a password: making a new link
 * replaces the old one, and deleting it disconnects Claude.
 */
app.get('/me/connector', async (c) => {
  const row = await c.env.DB.prepare(
    'SELECT created_at, last_used_at FROM connector_tokens WHERE user_id = ?',
  )
    .bind(c.get('userId'))
    .first<{ created_at: number; last_used_at: number | null }>();
  return c.json({
    connected: !!row,
    createdAt: row?.created_at ?? null,
    lastUsedAt: row?.last_used_at ?? null,
  });
});

app.post('/me/connector', async (c) => {
  const userId = c.get('userId');
  const token = newToken();
  await c.env.DB.batch([
    c.env.DB.prepare('DELETE FROM connector_tokens WHERE user_id = ?').bind(userId),
    c.env.DB.prepare('INSERT INTO connector_tokens (token_hash, user_id) VALUES (?, ?)').bind(
      await hashToken(token),
      userId,
    ),
  ]);
  return c.json({ url: `${new URL(c.req.url).origin}/mcp/${token}` }, 201);
});

app.delete('/me/connector', async (c) => {
  await c.env.DB.prepare('DELETE FROM connector_tokens WHERE user_id = ?')
    .bind(c.get('userId'))
    .run();
  return c.json({ connected: false });
});

/** The MCP endpoint Claude calls. See `src/mcp.ts`. */
app.all('/mcp/:token', async (c) => {
  const hash = await hashToken(c.req.param('token'));
  const row = await c.env.DB.prepare('SELECT user_id FROM connector_tokens WHERE token_hash = ?')
    .bind(hash)
    .first<{ user_id: string }>();
  if (!row)
    return c.json(
      { error: 'This OpenCPA connector link is not valid. Make a new one on the Claude page.' },
      401,
    );
  c.executionCtx.waitUntil(
    c.env.DB.prepare('UPDATE connector_tokens SET last_used_at = ? WHERE token_hash = ?')
      .bind(Date.now(), hash)
      .run(),
  );
  return handleMcp(c.req.raw, c.env.DB, row.user_id);
});

/** Tutor: wired up in a later milestone (Claude API, bring-your-own-key). */
app.post('/me/tutor', (c) => c.json({ error: 'The tutor is not available yet.' }, 501));

/** Record one attempt and the item's updated review card in a single batch. */
function saveAttempt(
  db: D1Database,
  userId: string,
  item: Item,
  response: unknown,
  result: GradeResult,
  durationMs: number | undefined,
  card: Card,
  sessionId?: string,
  variant = 0,
) {
  return db.batch([
    db
      .prepare(
        `INSERT INTO attempts (user_id, item_id, section, area, response, earned, possible, correct, duration_ms, session_id, variant)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      )
      .bind(
        userId,
        item.id,
        item.blueprint.section,
        item.blueprint.area,
        JSON.stringify(response),
        result.earned,
        result.possible,
        result.correct ? 1 : 0,
        durationMs ?? null,
        sessionId ?? null,
        variant,
      ),
    db
      .prepare(
        `INSERT INTO review_cards (user_id, item_id, due, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, state, last_review)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
       ON CONFLICT(user_id, item_id) DO UPDATE SET
         due = excluded.due, stability = excluded.stability, difficulty = excluded.difficulty,
         elapsed_days = excluded.elapsed_days, scheduled_days = excluded.scheduled_days,
         reps = excluded.reps, lapses = excluded.lapses, state = excluded.state, last_review = excluded.last_review`,
      )
      .bind(
        userId,
        item.id,
        card.due.getTime(),
        card.stability,
        card.difficulty,
        card.elapsed_days,
        card.scheduled_days,
        card.reps,
        card.lapses,
        card.state,
        card.last_review?.getTime() ?? null,
      ),
  ]);
}

type CardRow = {
  due: number;
  stability: number;
  difficulty: number;
  elapsed_days: number;
  scheduled_days: number;
  reps: number;
  lapses: number;
  state: number;
  last_review: number | null;
};

function rowToCard(r: CardRow): Card {
  return {
    due: new Date(r.due),
    stability: r.stability,
    difficulty: r.difficulty,
    elapsed_days: r.elapsed_days,
    scheduled_days: r.scheduled_days,
    reps: r.reps,
    lapses: r.lapses,
    state: r.state,
    last_review: r.last_review ? new Date(r.last_review) : undefined,
  } as Card;
}

export default app;
