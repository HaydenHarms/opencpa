import { describe, expect, it } from 'vitest';
import {
  AREA_WEIGHTS,
  EXAM_GRACE_MS,
  EXAM_LAYOUTS,
  buildExam,
  examClock,
  examExpired,
  type ExamTimes,
  type PoolItem,
} from './index';

function seeded(seed: number) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const FAR = EXAM_LAYOUTS.FAR!;
const areas = Object.keys(AREA_WEIGHTS.FAR!);

/** `perTopic` items in each of `topics` topics in each FAR area. */
function makePool(prefix: string, topics: number, perTopic: number): PoolItem[] {
  return areas.flatMap((area, a) =>
    Array.from({ length: topics }, (_, t) =>
      Array.from({ length: perTopic }, (_, n) => ({
        id: `${prefix}-${a}-${t}-${n}`,
        area,
        topic: `${prefix}-t-${a}-${t}`,
      })),
    ).flat(),
  );
}

const questions = makePool('q', 10, 10); // 300
const simulations = makePool('s', 3, 3); // 27

describe('buildExam', () => {
  const build = (usedInExams = new Set<string>(), seen = new Set<string>(), seed = 1) =>
    buildExam({
      layout: FAR,
      questions,
      simulations,
      usedInExams,
      seen,
      weights: AREA_WEIGHTS.FAR,
      rng: seeded(seed),
    });

  it('follows the FAR layout: 25 and 25 questions, then 2, 3 and 2 simulations', () => {
    const t = build();
    expect(t.map((x) => x.length)).toEqual([25, 25, 2, 3, 2]);
    expect(
      t
        .slice(0, 2)
        .flat()
        .every((id) => id.startsWith('q-')),
    ).toBe(true);
    expect(
      t
        .slice(2)
        .flat()
        .every((id) => id.startsWith('s-')),
    ).toBe(true);
    expect(new Set(t.flat()).size).toBe(57);
  });

  it('splits questions by blueprint area weight', () => {
    const qs = build().slice(0, 2).flat();
    const count = (a: number) => qs.filter((id) => id.startsWith(`q-${a}-`)).length;
    expect([count(0), count(1), count(2)]).toEqual([18, 17, 15]);
  });

  it('spreads questions across topics', () => {
    const qs = build().slice(0, 2).flat();
    const topics = new Map<string, number>();
    for (const id of qs) {
      const t = id.split('-').slice(0, 3).join('-');
      topics.set(t, (topics.get(t) ?? 0) + 1);
    }
    expect(topics.size).toBe(30);
    expect(Math.max(...topics.values())).toBeLessThanOrEqual(2);
  });

  it('avoids items from earlier mock exams, then items already seen', () => {
    const first = build(new Set(), new Set(), 1);
    const used = new Set(first.flat());
    const second = build(used, new Set(), 2);
    expect(second.flat().filter((id) => used.has(id))).toEqual([]);

    // Two questions per topic (20 per area) are unseen: every pick comes from those.
    const seen = new Set(questions.filter((q) => !/-[01]$/.test(q.id)).map((q) => q.id));
    const qs = build(new Set(), seen, 3).slice(0, 2).flat();
    expect(qs.filter((id) => seen.has(id))).toEqual([]);
  });

  it('repeats no simulation until every one has been used, even with uneven areas', () => {
    // 6, 7 and 8 simulations by area, as the FAR bank has today: three exams, no repeats.
    const uneven = makePool('s', 1, 8).filter((s) => !/^s-0-0-[67]$|^s-1-0-7$/.test(s.id));
    expect(uneven.length).toBe(21);
    const used = new Set<string>();
    for (let n = 0; n < 3; n++) {
      const sims = buildExam({
        layout: FAR,
        questions,
        simulations: uneven,
        usedInExams: used,
        seen: new Set(),
        weights: AREA_WEIGHTS.FAR,
        rng: seeded(10 + n),
      })
        .slice(2)
        .flat();
      expect(sims.filter((id) => used.has(id))).toEqual([]);
      for (const id of sims) used.add(id);
    }
    expect(used.size).toBe(21);
  });

  it('reuses simulations once every one has been in a mock exam', () => {
    const used = new Set(simulations.map((s) => s.id));
    const t = build(used, new Set(), 4);
    expect(t.slice(2).flat().length).toBe(7);
  });
});

describe('examClock', () => {
  const start = 1_000_000;
  const base: ExamTimes = {
    startedAt: start,
    breakStartedAt: null,
    breakEndedAt: null,
    pausedAt: null,
    pausedMs: 0,
    finishedAt: null,
  };
  const min = 60_000;

  it('counts down four hours from the start', () => {
    const c = examClock(FAR, base, start + 30 * min);
    expect(c.limitMs).toBe(240 * min);
    expect(c.usedMs).toBe(30 * min);
    expect(c.remainingMs).toBe(210 * min);
  });

  it('stops while paused and leaves out finished pauses', () => {
    const paused = examClock(FAR, { ...base, pausedAt: start + 10 * min }, start + 70 * min);
    expect(paused.paused).toBe(true);
    expect(paused.usedMs).toBe(10 * min);
    expect(paused.pausedMs).toBe(60 * min);
    const resumed = examClock(FAR, { ...base, pausedMs: 60 * min }, start + 80 * min);
    expect(resumed.usedMs).toBe(20 * min);
  });

  it('gives a free 15-minute break; time past it counts', () => {
    const b = { ...base, breakStartedAt: start + 60 * min };
    const during = examClock(FAR, b, start + 70 * min);
    expect(during.onBreak).toBe(true);
    expect(during.usedMs).toBe(60 * min);
    expect(during.breakRemainingMs).toBe(5 * min);
    const over = examClock(FAR, b, start + 80 * min);
    expect(over.usedMs).toBe(65 * min);
    expect(over.breakRemainingMs).toBe(0);
    const ended = examClock(FAR, { ...b, breakEndedAt: start + 70 * min }, start + 100 * min);
    expect(ended.onBreak).toBe(false);
    expect(ended.usedMs).toBe(90 * min);
  });

  it('stops at the finish time', () => {
    const c = examClock(FAR, { ...base, finishedAt: start + 90 * min }, start + 500 * min);
    expect(c.usedMs).toBe(90 * min);
  });

  it('expires only past the grace period', () => {
    expect(examExpired(examClock(FAR, base, start + 240 * min))).toBe(false);
    expect(examExpired(examClock(FAR, base, start + 240 * min + EXAM_GRACE_MS + 1))).toBe(true);
  });
});
