import { describe, expect, it } from 'vitest';
import {
  AREA_WEIGHTS,
  allocateByArea,
  masteryByTopic,
  selectDiagnosticItems,
  selectPracticeItems,
  type PoolItem,
} from './index';

/** Small seeded generator so the tests are repeatable. */
function seeded(seed: number) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const [A1, A2, A3] = Object.keys(AREA_WEIGHTS.FAR!);

/** 3 areas x 4 topics x 5 items = 60 items. */
const pool: PoolItem[] = [A1!, A2!, A3!].flatMap((area, a) =>
  [0, 1, 2, 3].flatMap((t) =>
    [0, 1, 2, 3, 4].map((n) => ({ id: `i-${a}-${t}-${n}`, area, topic: `t-${a}-${t}` })),
  ),
);
const areaOf = (id: string) => pool.find((i) => i.id === id)!.area;
const topicOf = (id: string) => pool.find((i) => i.id === id)!.topic;
const count = (ids: string[], f: (id: string) => string) =>
  ids.reduce((m, id) => m.set(f(id), (m.get(f(id)) ?? 0) + 1), new Map<string, number>());

describe('allocateByArea', () => {
  it('splits by blueprint weight', () => {
    const q = allocateByArea(pool, 20, AREA_WEIGHTS.FAR);
    expect([q.get(A1!), q.get(A2!), q.get(A3!)]).toEqual([7, 7, 6]);
  });

  it('gives the spare to other areas when one runs out', () => {
    const small = pool.filter((i) => i.area !== A3 || i.topic === 't-2-0'); // area III has 5 items
    const q = allocateByArea(small, 30, AREA_WEIGHTS.FAR);
    expect(q.get(A3!)).toBe(5);
    expect(q.get(A1!)! + q.get(A2!)!).toBe(25);
  });

  it('never asks for more than the pool holds', () => {
    const q = allocateByArea(pool.slice(0, 7), 50, AREA_WEIGHTS.FAR);
    expect([...q.values()].reduce((s, n) => s + n, 0)).toBe(7);
  });
});

describe('selectPracticeItems', () => {
  const base = { pool, size: 12, due: new Map(), topicScore: new Map(), now: 1_000_000 };

  it('returns distinct items, the requested number, mixed across areas and topics', () => {
    const ids = selectPracticeItems({ ...base, weights: AREA_WEIGHTS.FAR, rng: seeded(1) });
    expect(ids).toHaveLength(12);
    expect(new Set(ids).size).toBe(12);
    expect(count(ids, areaOf).size).toBe(3);
    // 4 per area over 4 topics: every topic gets one before any gets two.
    expect(Math.max(...count(ids, topicOf).values())).toBe(1);
  });

  it('does not serve the same order every time', () => {
    const a = selectPracticeItems({ ...base, rng: seeded(1) });
    const b = selectPracticeItems({ ...base, rng: seeded(2) });
    expect(a).not.toEqual(b);
  });

  it('serves due reviews first, then unseen items, then recently seen ones', () => {
    const due = new Map<string, number>();
    for (const i of pool) due.set(i.id, base.now + 86_400_000); // seen, not due
    due.set('i-0-0-0', base.now - 1); // due
    due.set('i-1-2-3', base.now - 5); // due
    due.delete('i-2-1-4'); // unseen
    const ids = selectPracticeItems({ ...base, size: 6, due, rng: seeded(3) });
    expect(ids).toEqual(expect.arrayContaining(['i-0-0-0', 'i-1-2-3', 'i-2-1-4']));
  });

  it('leans toward weak topics', () => {
    const topicScore = new Map([
      ['t-0-0', 0.2],
      ['t-0-1', 0.95],
      ['t-0-2', 0.95],
      ['t-0-3', 0.95],
    ]);
    const areaI = pool.filter((i) => i.area === A1);
    let weak = 0;
    for (let s = 0; s < 50; s++) {
      const ids = selectPracticeItems({
        ...base,
        pool: areaI,
        size: 6,
        topicScore,
        rng: seeded(s),
      });
      weak += ids.filter((id) => topicOf(id) === 't-0-0').length;
    }
    // Even spread would give 1.5 per session; the weak topic should get clearly more.
    expect(weak / 50).toBeGreaterThan(2);
  });
});

describe('selectDiagnosticItems', () => {
  it('covers as many topics as it can before repeating one', () => {
    const ids = selectDiagnosticItems(pool, 12, AREA_WEIGHTS.FAR, seeded(4));
    expect(ids).toHaveLength(12);
    expect(count(ids, topicOf).size).toBe(12);
  });

  it('stops at the pool size', () => {
    expect(selectDiagnosticItems(pool.slice(0, 3), 20, {}, seeded(5))).toHaveLength(3);
  });
});

describe('masteryByTopic', () => {
  it('weights recent attempts more', () => {
    const day = 86_400_000;
    const now = 100 * day;
    const m = masteryByTopic(
      [
        { topic: 'x', correct: false, at: now - 28 * day },
        { topic: 'x', correct: true, at: now },
      ],
      now,
    );
    expect(m.get('x')).toBeCloseTo(0.8, 5); // weights 0.25 and 1
  });
});
