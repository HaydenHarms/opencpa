/**
 * Mock exams: the testlet layout of each section's exam, how its items are picked, and the
 * clock. See `docs/plans/exam-mode.md`.
 */
import { allocateByArea, type PoolItem, type Rng } from './selection';

export interface TestletSpec {
  kind: 'mcq' | 'tbs';
  count: number;
}

export interface ExamLayout {
  testlets: TestletSpec[];
  /** Testing time, not counting the break or pauses. */
  minutes: number;
  /** The optional break comes after this many testlets. */
  breakAfter: number;
  /** Break time that doesn't count against the clock; time past it does. */
  breakMinutes: number;
}

/** The real exam's format per section. Sections not listed have no mock exam yet. */
export const EXAM_LAYOUTS: Record<string, ExamLayout> = {
  FAR: {
    testlets: [
      { kind: 'mcq', count: 25 },
      { kind: 'mcq', count: 25 },
      { kind: 'tbs', count: 2 },
      { kind: 'tbs', count: 3 },
      { kind: 'tbs', count: 2 },
    ],
    minutes: 240,
    breakAfter: 3,
    breakMinutes: 15,
  },
};

/** Late requests are still accepted this long after the clock runs out, to absorb network lag. */
export const EXAM_GRACE_MS = 30_000;

export interface ExamPoolInput {
  layout: ExamLayout;
  questions: PoolItem[];
  simulations: PoolItem[];
  /** Items used in the student's earlier mock exams. */
  usedInExams: Set<string>;
  /** Items the student has answered anywhere. */
  seen: Set<string>;
  weights?: Record<string, number>;
  rng?: Rng;
}

/**
 * Pick a mock exam's items and split them into testlets. Each kind is spread across the
 * blueprint areas by weight and across topics within an area, preferring items never seen at
 * all. Items from earlier mock exams are used only once the fresh ones run out, even if that
 * leaves an area short, so a student gets as many exams as possible without a repeat. No leaning
 * toward weak topics: a mock exam should measure, not drill. Returns one list of ids per testlet.
 */
export function buildExam(input: ExamPoolInput): string[][] {
  const { layout, usedInExams, seen, weights = {}, rng = Math.random } = input;
  const total = (kind: TestletSpec['kind']) =>
    layout.testlets.filter((t) => t.kind === kind).reduce((s, t) => s + t.count, 0);
  const tier = (id: string) => (usedInExams.has(id) ? 0 : seen.has(id) ? 1 : 2);
  const picked = {
    mcq: pickFresh(input.questions, total('mcq'), weights, tier, rng),
    tbs: pickFresh(input.simulations, total('tbs'), weights, tier, rng),
  };
  return layout.testlets.map((t) => picked[t.kind].splice(0, t.count));
}

/** Fill from items not in an earlier mock exam first, then from the rest. */
function pickFresh(
  pool: PoolItem[],
  size: number,
  weights: Record<string, number>,
  tier: (id: string) => number,
  rng: Rng,
): string[] {
  const fresh = pickSpread(
    pool.filter((i) => tier(i.id) > 0),
    size,
    weights,
    tier,
    rng,
  );
  const taken = new Set(fresh);
  const reused = pickSpread(
    pool.filter((i) => !taken.has(i.id)),
    size - fresh.length,
    weights,
    tier,
    rng,
  );
  return shuffle([...fresh, ...reused], rng);
}

function pickSpread(
  pool: PoolItem[],
  size: number,
  weights: Record<string, number>,
  tier: (id: string) => number,
  rng: Rng,
): string[] {
  const picked: string[] = [];
  for (const [area, quota] of allocateByArea(pool, size, weights)) {
    const byTopic = new Map<string, PoolItem[]>();
    const ranked = shuffle(
      pool.filter((i) => i.area === area),
      rng,
    ).sort((a, b) => tier(b.id) - tier(a.id));
    for (const i of ranked) byTopic.set(i.topic, [...(byTopic.get(i.topic) ?? []), i]);
    const perTopic = new Map<string, number>();
    for (let n = 0; n < quota; n++) {
      let best: { topic: string; score: number } | null = null;
      for (const [topic, queue] of byTopic) {
        const head = queue[0];
        if (!head) continue;
        const score = tier(head.id) * 10 + 1 / (1 + (perTopic.get(topic) ?? 0)) + rng() * 0.25;
        if (!best || score > best.score) best = { topic, score };
      }
      if (!best) break;
      picked.push(byTopic.get(best.topic)!.shift()!.id);
      perTopic.set(best.topic, (perTopic.get(best.topic) ?? 0) + 1);
    }
  }
  return shuffle(picked, rng);
}

/** The clock's raw times, all epoch ms. */
export interface ExamTimes {
  startedAt: number;
  breakStartedAt: number | null;
  breakEndedAt: number | null;
  pausedAt: number | null;
  /** Time spent in pauses that have ended. */
  pausedMs: number;
  finishedAt: number | null;
}

export interface ExamClock {
  limitMs: number;
  /** Testing time used: time since starting, less pauses and up to the break allowance. */
  usedMs: number;
  remainingMs: number;
  paused: boolean;
  onBreak: boolean;
  /** Break time left before the clock starts running again (0 when not on a break). */
  breakRemainingMs: number;
  /** Total time paused, including a pause in progress. */
  pausedMs: number;
}

export function examClock(layout: ExamLayout, t: ExamTimes, now: number): ExamClock {
  const limitMs = layout.minutes * 60_000;
  const allowance = layout.breakMinutes * 60_000;
  const end = t.finishedAt ?? now;
  const pausedMs = t.pausedMs + (t.pausedAt !== null ? Math.max(0, end - t.pausedAt) : 0);
  const onBreak = t.breakStartedAt !== null && t.breakEndedAt === null && t.finishedAt === null;
  const breakMs =
    t.breakStartedAt === null ? 0 : Math.max(0, (t.breakEndedAt ?? end) - t.breakStartedAt);
  const usedMs = Math.max(0, end - t.startedAt - pausedMs - Math.min(breakMs, allowance));
  return {
    limitMs,
    usedMs,
    remainingMs: Math.max(0, limitMs - usedMs),
    paused: t.pausedAt !== null && t.finishedAt === null,
    onBreak,
    breakRemainingMs: onBreak ? Math.max(0, allowance - breakMs) : 0,
    pausedMs,
  };
}

/** Whether the clock ran out long enough ago (past the grace) that the exam must end now. */
export function examExpired(clock: ExamClock) {
  return clock.usedMs > clock.limitMs + EXAM_GRACE_MS;
}

function shuffle<T>(list: T[], rng: Rng): T[] {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j]!, a[i]!];
  }
  return a;
}
