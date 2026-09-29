import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { z } from 'zod';
import { toPublicMcq, toPublicTbs, type Item, type McqItem, type TbsItem } from '@opencpa/schema';
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
  const result = gradeMcq(item, selected);
  const now = new Date();

  const row = await c.env.DB.prepare('SELECT * FROM review_cards WHERE user_id = ? AND item_id = ?')
    .bind(userId, itemId)
    .first<CardRow>();
  const card = review(
    row ? rowToCard(row) : newCard(now),
    ratingFor(result.correct, lowConfidence),
    now,
  );

  await saveAttempt(c.env.DB, userId, item, { selected }, result, durationMs, card, sessionId);
  const sessionComplete = await completeIfDone(c.env.DB, check.session);

  // Answer and explanation are revealed only after an attempt is recorded.
  return c.json({
    ...result,
    ...reveal(item, selected, result.correct),
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
  const row = await c.env.DB.prepare(
    `SELECT * FROM practice_sessions WHERE user_id = ? AND section = ? AND status = 'active'
     ORDER BY created_at DESC LIMIT 1`,
  )
    .bind(userId, section.data)
    .first<SessionRow>();
  const poolSize = mcqs.filter((q) => q.blueprint.section === section.data).length;
  const simPool = simulations.filter((t) => t.blueprint.section === section.data).length;
  const diagnostic = !(await hasMcqAttempts(c.env.DB, userId, section.data));
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
});

app.post('/me/sessions', async (c) => {
  const body = newSessionBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  const { section, size } = body.data;
  const userId = c.get('userId');
  const db = c.env.DB;

  const toPool = (i: Item) => ({ id: i.id, area: i.blueprint.area, topic: i.blueprint.topic });
  const pool = mcqs.filter((q) => q.blueprint.section === section).map(toPool);
  const simPool = simulations.filter((t) => t.blueprint.section === section).map(toPool);
  if (pool.length === 0) return c.json({ error: `no ${section} questions yet` }, 404);

  const weights = AREA_WEIGHTS[section];
  let kind: 'diagnostic' | 'practice';
  let ids: string[];
  let simIds: string[];
  if (!(await hasMcqAttempts(db, userId, section))) {
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
      size: simulationCount(ids.length, simPool.length),
    });
  }
  // Simulations are spread through the questions (exam-day mode will use the exam's order).
  ids = spreadThrough(ids, simIds);

  // Starting a new session abandons any unfinished one in the same section.
  // Its answers still count toward mastery and review scheduling.
  const id = crypto.randomUUID();
  await db.batch([
    db
      .prepare(
        `UPDATE practice_sessions SET status = 'abandoned'
         WHERE user_id = ? AND section = ? AND status = 'active'`,
      )
      .bind(userId, section),
    db
      .prepare(
        'INSERT INTO practice_sessions (id, user_id, section, kind, item_ids) VALUES (?, ?, ?, ?, ?)',
      )
      .bind(id, userId, section, kind, JSON.stringify(ids)),
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
) {
  return db.batch([
    db
      .prepare(
        `INSERT INTO attempts (user_id, item_id, section, area, response, earned, possible, correct, duration_ms, session_id)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
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

type SessionRow = {
  id: string;
  user_id: string;
  section: string;
  kind: 'diagnostic' | 'practice';
  status: 'active' | 'completed' | 'abandoned';
  item_ids: string;
  created_at: number;
  completed_at: number | null;
};

function loadSession(db: D1Database, userId: string, id: string) {
  return db
    .prepare('SELECT * FROM practice_sessions WHERE id = ? AND user_id = ?')
    .bind(id, userId)
    .first<SessionRow>();
}

/** The session's items that are still in the bank (retired items drop out). */
function sessionItemIds(row: SessionRow): string[] {
  return (JSON.parse(row.item_ids) as string[]).filter((id) => byId.has(id));
}

type SessionCheck = { session: SessionRow | null } | { error: string; status: 400 | 404 | 409 };

/** When an attempt names a session: it must be active, contain the item, and not have it answered yet. */
async function checkSession(
  db: D1Database,
  userId: string,
  sessionId: string | undefined,
  itemId: string,
): Promise<SessionCheck> {
  if (!sessionId) return { session: null };
  const session = await loadSession(db, userId, sessionId);
  if (!session || session.status !== 'active')
    return { error: 'no active session with that id', status: 404 };
  if (!sessionItemIds(session).includes(itemId))
    return { error: 'that item is not in this session', status: 400 };
  const answered = await db
    .prepare('SELECT 1 FROM attempts WHERE session_id = ? AND item_id = ? LIMIT 1')
    .bind(sessionId, itemId)
    .first();
  if (answered) return { error: 'already answered in this session', status: 409 };
  return { session };
}

/** Mark the session completed once every item has an attempt. Returns whether it is complete. */
async function completeIfDone(db: D1Database, session: SessionRow | null) {
  if (!session) return false;
  const done = await db
    .prepare('SELECT COUNT(DISTINCT item_id) AS n FROM attempts WHERE session_id = ?')
    .bind(session.id)
    .first<{ n: number }>();
  if ((done?.n ?? 0) < sessionItemIds(session).length) return false;
  await db
    .prepare("UPDATE practice_sessions SET status = 'completed', completed_at = ? WHERE id = ?")
    .bind(Date.now(), session.id)
    .run();
  return true;
}

/** What an attempt reveals: the key, the explanation and every choice's rationale. */
function reveal(item: McqItem, selected: string, correct: boolean) {
  return {
    selected,
    correct,
    answer: item.answer,
    explanation: item.explanation,
    rationales: Object.fromEntries(item.choices.map((ch) => [ch.id, ch.rationale])),
  };
}

type Responses = Parameters<typeof gradeSimulation>[1];

/** What a simulation attempt reveals: the score, and each task's answer and explanation. */
function revealSimulation(item: TbsItem, responses: Responses) {
  const result = gradeSimulation(item, responses);
  return {
    ...result,
    responses,
    tasks: item.tasks.map((t) => ({
      id: t.id,
      ...result.tasks[t.id],
      answer: t.answer,
      explanation: t.explanation,
    })),
  };
}

/** A session's public items, plus the revealed result of each item already answered. */
async function sessionView(db: D1Database, row: SessionRow) {
  const { results } = await db
    .prepare('SELECT item_id, response, correct FROM attempts WHERE session_id = ?')
    .bind(row.id)
    .all<{ item_id: string; response: string; correct: number }>();
  const answered: Record<string, ReturnType<typeof reveal> | ReturnType<typeof revealSimulation>> =
    {};
  for (const r of results) {
    const item = byId.get(r.item_id);
    if (item?.type === 'mcq') {
      const { selected } = JSON.parse(r.response) as { selected: string };
      answered[r.item_id] = reveal(item, selected, !!r.correct);
    } else if (item?.type === 'tbs') {
      // Grading is deterministic, so re-grading the stored responses reproduces the result.
      answered[r.item_id] = revealSimulation(item, JSON.parse(r.response) as Responses);
    }
  }
  return {
    id: row.id,
    section: row.section,
    kind: row.kind,
    status: row.status,
    createdAt: row.created_at,
    completedAt: row.completed_at,
    items: sessionItemIds(row).map((id) => {
      const item = byId.get(id)!;
      return item.type === 'mcq' ? toPublicMcq(item) : toPublicTbs(item);
    }),
    answered,
  };
}

/** Whether the student has answered any multiple-choice question in this section. */
async function hasMcqAttempts(db: D1Database, userId: string, section: string) {
  const { results } = await db
    .prepare('SELECT DISTINCT item_id FROM attempts WHERE user_id = ? AND section = ?')
    .bind(userId, section)
    .all<{ item_id: string }>();
  return results.some((r) => byId.get(r.item_id)?.type === 'mcq');
}

export default app;
