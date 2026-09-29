import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { z } from 'zod';
import { toPublicMcq, toPublicTbs, type Item } from '@opencpa/schema';
import {
  gradeMcq,
  gradeSimulation,
  masteryByArea,
  newCard,
  ratingFor,
  ratingForScore,
  review,
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
});

app.post('/me/attempts', async (c) => {
  const body = attemptBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  const { itemId, selected, lowConfidence, durationMs } = body.data;
  const item = byId.get(itemId);
  if (!item || item.type !== 'mcq') return c.json({ error: 'unknown item' }, 404);

  const userId = c.get('userId');
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

  await saveAttempt(c.env.DB, userId, item, { selected }, result, durationMs, card);

  // Answer and explanation are revealed only after an attempt is recorded.
  return c.json({
    ...result,
    answer: item.answer,
    explanation: item.explanation,
    rationales: Object.fromEntries(item.choices.map((ch) => [ch.id, ch.rationale])),
    nextDue: card.due.toISOString(),
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
});

app.post('/me/simulations/:id/attempts', async (c) => {
  const body = simulationAttemptBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  const item = byId.get(c.req.param('id'));
  if (!item || item.type !== 'tbs') return c.json({ error: 'unknown simulation' }, 404);

  const userId = c.get('userId');
  const { responses, durationMs } = body.data;
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
  await saveAttempt(c.env.DB, userId, item, responses, result, durationMs, card);

  // Answers and explanations are revealed only after an attempt is recorded.
  return c.json({
    ...result,
    tasks: item.tasks.map((t) => ({
      id: t.id,
      ...result.tasks[t.id],
      answer: t.answer,
      explanation: t.explanation,
    })),
    nextDue: card.due.toISOString(),
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
) {
  return db.batch([
    db.prepare(
      `INSERT INTO attempts (user_id, item_id, section, area, response, earned, possible, correct, duration_ms)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    ).bind(
      userId,
      item.id,
      item.blueprint.section,
      item.blueprint.area,
      JSON.stringify(response),
      result.earned,
      result.possible,
      result.correct ? 1 : 0,
      durationMs ?? null,
    ),
    db.prepare(
      `INSERT INTO review_cards (user_id, item_id, due, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, state, last_review)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
       ON CONFLICT(user_id, item_id) DO UPDATE SET
         due = excluded.due, stability = excluded.stability, difficulty = excluded.difficulty,
         elapsed_days = excluded.elapsed_days, scheduled_days = excluded.scheduled_days,
         reps = excluded.reps, lapses = excluded.lapses, state = excluded.state, last_review = excluded.last_review`,
    ).bind(
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
