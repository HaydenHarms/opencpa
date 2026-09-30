/** Practice-session storage and what an answered item reveals, shared by the API and the MCP connector. */
import {
  mcqVariant,
  toPublicMcq,
  toPublicTbs,
  variantCount,
  type McqItem,
  type TbsItem,
} from '@opencpa/schema';
import { gradeSimulation } from '@opencpa/engine';
import { byId } from './content';

export type SessionRow = {
  id: string;
  user_id: string;
  section: string;
  kind: 'diagnostic' | 'practice';
  /** Set for a Library session scoped to one blueprint topic; null for a whole-section session. */
  topic: string | null;
  status: 'active' | 'completed' | 'abandoned';
  item_ids: string;
  /** JSON array of the version served for each item, parallel to item_ids; null means all 0. */
  variants: string | null;
  created_at: number;
  completed_at: number | null;
};

export function loadSession(db: D1Database, userId: string, id: string) {
  return db
    .prepare('SELECT * FROM practice_sessions WHERE id = ? AND user_id = ?')
    .bind(id, userId)
    .first<SessionRow>();
}

/** The session's items that are still in the bank (retired items drop out). */
export function sessionItemIds(row: SessionRow): string[] {
  return (JSON.parse(row.item_ids) as string[]).filter((id) => byId.has(id));
}

/** Which version of an item the session serves (0 when the session predates variants). */
export function sessionVariant(row: SessionRow, itemId: string): number {
  if (!row.variants) return 0;
  const ids = JSON.parse(row.item_ids) as string[];
  const variants = JSON.parse(row.variants) as number[];
  return variants[ids.indexOf(itemId)] ?? 0;
}

/**
 * Pick the version of each multiple-choice item to serve: rotate through the versions by how
 * many times the student has answered that item, so a repeat shows new numbers.
 */
export async function pickVariants(db: D1Database, userId: string, ids: string[]) {
  const { results } = await db
    .prepare('SELECT item_id, COUNT(*) AS n FROM attempts WHERE user_id = ? GROUP BY item_id')
    .bind(userId)
    .all<{ item_id: string; n: number }>();
  const seen = new Map(results.map((r) => [r.item_id, r.n]));
  return ids.map((id) => {
    const item = byId.get(id);
    return item?.type === 'mcq' ? (seen.get(id) ?? 0) % variantCount(item) : 0;
  });
}

export type SessionCheck =
  { session: SessionRow | null } | { error: string; status: 400 | 404 | 409 };

/** When an attempt names a session: it must be active, contain the item, and not have it answered yet. */
export async function checkSession(
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
export async function completeIfDone(db: D1Database, session: SessionRow | null) {
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
export function reveal(item: McqItem, selected: string, correct: boolean) {
  return {
    selected,
    correct,
    answer: item.answer,
    explanation: item.explanation,
    rationales: Object.fromEntries(item.choices.map((ch) => [ch.id, ch.rationale])),
  };
}

export type Responses = Parameters<typeof gradeSimulation>[1];

/** What a simulation attempt reveals: the score, and each task's answer and explanation. */
export function revealSimulation(item: TbsItem, responses: Responses) {
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
export async function sessionView(db: D1Database, row: SessionRow) {
  const { results } = await db
    .prepare('SELECT item_id, response, correct, variant FROM attempts WHERE session_id = ?')
    .bind(row.id)
    .all<{ item_id: string; response: string; correct: number; variant: number }>();
  const answered: Record<string, ReturnType<typeof reveal> | ReturnType<typeof revealSimulation>> =
    {};
  for (const r of results) {
    const item = byId.get(r.item_id);
    if (item?.type === 'mcq') {
      const { selected } = JSON.parse(r.response) as { selected: string };
      answered[r.item_id] = reveal(mcqVariant(item, r.variant), selected, !!r.correct);
    } else if (item?.type === 'tbs') {
      // Grading is deterministic, so re-grading the stored responses reproduces the result.
      answered[r.item_id] = revealSimulation(item, JSON.parse(r.response) as Responses);
    }
  }
  return {
    id: row.id,
    section: row.section,
    kind: row.kind,
    topic: row.topic ?? null,
    status: row.status,
    createdAt: row.created_at,
    completedAt: row.completed_at,
    items: sessionItemIds(row).map((id) => {
      const item = byId.get(id)!;
      return item.type === 'mcq' ? toPublicMcq(item, sessionVariant(row, id)) : toPublicTbs(item);
    }),
    answered,
  };
}

/** Whether the student has answered any multiple-choice question in this section. */
export async function hasMcqAttempts(db: D1Database, userId: string, section: string) {
  const { results } = await db
    .prepare('SELECT DISTINCT item_id FROM attempts WHERE user_id = ? AND section = ?')
    .bind(userId, section)
    .all<{ item_id: string }>();
  return results.some((r) => byId.get(r.item_id)?.type === 'mcq');
}
