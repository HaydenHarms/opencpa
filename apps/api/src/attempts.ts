/** Recording attempts and review cards, shared by practice and mock exams. */
import { z } from 'zod';
import type { Item } from '@opencpa/schema';
import { newCard, review, type Card, type GradeResult } from '@opencpa/engine';

const cents = z.number().int().nonnegative();
export const taskResponse = z.discriminatedUnion('type', [
  z.object({ type: z.literal('numeric'), value: z.number().finite() }),
  z.object({
    type: z.literal('journal_entry'),
    lines: z
      .array(z.object({ account: z.string(), debit: cents.optional(), credit: cents.optional() }))
      .max(20),
  }),
  z.object({ type: z.literal('research'), citation: z.string().max(100) }),
  z.object({
    type: z.literal('select'),
    choices: z
      .record(z.string().max(300))
      .refine((c) => Object.keys(c).length <= 50, 'at most 50 rows'),
  }),
]);

/** The statements that record one attempt and the item's updated review card. */
export function attemptStatements(
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
  return [
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
  ];
}

/** Record one attempt and the item's updated review card in a single batch. */
export function saveAttempt(...args: Parameters<typeof attemptStatements>) {
  return args[0].batch(attemptStatements(...args));
}

export type CardRow = {
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

export function rowToCard(r: CardRow): Card {
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

/** The student's review card for an item, moved forward by one review with `rating`. */
export async function cardFor(
  db: D1Database,
  userId: string,
  itemId: string,
  rating: Parameters<typeof review>[1],
  now: Date,
) {
  const row = await db
    .prepare('SELECT * FROM review_cards WHERE user_id = ? AND item_id = ?')
    .bind(userId, itemId)
    .first<CardRow>();
  return review(row ? rowToCard(row) : newCard(now), rating, now);
}
