/**
 * Choosing which questions go into a practice session.
 *
 * A session mixes the section's blueprint areas roughly by their blueprint weight.
 * Within an area it prefers, in order: items the scheduler says are due, then
 * items the student has never seen (weakest topics first), then items seen
 * recently. Picks rotate across topics so one topic doesn't fill the session.
 */

export interface PoolItem {
  id: string;
  area: string;
  topic: string;
}

export type Rng = () => number;

/** Midpoints of the 2026 blueprint area ranges. Sections not listed weight areas equally. */
export const AREA_WEIGHTS: Record<string, Record<string, number>> = {
  FAR: {
    'Area I — Financial Reporting': 35,
    'Area II — Select Balance Sheet Accounts': 35,
    'Area III — Select Transactions': 30,
  },
  BAR: {
    'Area I — Business Analysis': 45,
    'Area II — Technical Accounting and Reporting': 40,
    'Area III — State and Local Governments': 15,
  },
};

export const DIAGNOSTIC_SIZE = 20;

export interface PracticeInput {
  pool: PoolItem[];
  size: number;
  /** Due time (epoch ms) of each item the student has a review card for. */
  due: Map<string, number>;
  /** Recency-weighted accuracy (0–1) per topic; topics with no attempts are absent. */
  topicScore: Map<string, number>;
  /** Blueprint weight per area; defaults to equal weights. */
  weights?: Record<string, number>;
  now?: number;
  rng?: Rng;
}

/** Pick `size` items for a practice session and return their ids in serving order. */
export function selectPracticeItems(input: PracticeInput): string[] {
  const { pool, due, topicScore, weights = {}, now = Date.now(), rng = Math.random } = input;
  const quotas = allocateByArea(pool, input.size, weights);
  const picked: string[] = [];

  for (const [area, quota] of quotas) {
    // Rank each item: due reviews first (most overdue first), then unseen items
    // (random order), then seen-but-not-due items (soonest due first).
    const ranked = shuffle(
      pool.filter((i) => i.area === area),
      rng,
    )
      .map((item) => {
        const d = due.get(item.id);
        const tier = d === undefined ? 1 : d <= now ? 2 : 0;
        return { item, tier, dueAt: d ?? 0 };
      })
      .sort((a, b) => b.tier - a.tier || (a.tier === 1 ? 0 : a.dueAt - b.dueAt));

    const byTopic = groupBy(ranked, (r) => r.item.topic);
    const picksPerTopic = new Map<string, number>();
    for (let n = 0; n < quota; n++) {
      let best: { topic: string; score: number } | null = null;
      for (const [topic, queue] of byTopic) {
        const head = queue[0];
        if (!head) continue;
        const weakness = 1 - (topicScore.get(topic) ?? 0.5);
        const score =
          head.tier * 10 + weakness / (1 + (picksPerTopic.get(topic) ?? 0)) + rng() * 0.25;
        if (!best || score > best.score) best = { topic, score };
      }
      if (!best) break;
      picked.push(byTopic.get(best.topic)!.shift()!.item.id);
      picksPerTopic.set(best.topic, (picksPerTopic.get(best.topic) ?? 0) + 1);
    }
  }

  return shuffle(picked, rng);
}

/**
 * A first session in a section: spread across as many topics as possible, one
 * random item per topic before any topic gets a second, with areas by blueprint weight.
 */
export function selectDiagnosticItems(
  pool: PoolItem[],
  size = DIAGNOSTIC_SIZE,
  weights: Record<string, number> = {},
  rng: Rng = Math.random,
): string[] {
  const picked: string[] = [];
  for (const [area, quota] of allocateByArea(pool, size, weights)) {
    const byTopic = [
      ...groupBy(
        shuffle(
          pool.filter((i) => i.area === area),
          rng,
        ),
        (i) => i.topic,
      ).values(),
    ];
    const topics = shuffle(byTopic, rng);
    for (let n = 0; n < quota;) {
      let took = false;
      for (const queue of topics) {
        if (n >= quota || queue.length === 0) continue;
        picked.push(queue.shift()!.id);
        n++;
        took = true;
      }
      if (!took) break;
    }
  }
  return shuffle(picked, rng);
}

/**
 * Split `size` across the pool's areas in proportion to `weights` (largest
 * remainder), never giving an area more items than it has. Unlisted areas get the
 * average weight of the listed ones, or 1 when nothing is listed.
 */
export function allocateByArea(
  pool: PoolItem[],
  size: number,
  weights: Record<string, number> = {},
): Map<string, number> {
  const available = new Map<string, number>();
  for (const i of pool) available.set(i.area, (available.get(i.area) ?? 0) + 1);
  const listed = Object.values(weights);
  const fallback = listed.length ? listed.reduce((s, w) => s + w, 0) / listed.length : 1;
  const weightOf = (area: string) => weights[area] ?? fallback;

  const quotas = new Map([...available.keys()].map((a) => [a, 0]));
  let remaining = Math.min(Math.max(0, Math.floor(size)), pool.length);
  // Repeat because capping a small area frees items for the others.
  while (remaining > 0) {
    const open = [...available.keys()].filter((a) => quotas.get(a)! < available.get(a)!);
    const total = open.reduce((s, a) => s + weightOf(a), 0);
    const shares = open.map((a) => {
      const exact = (remaining * weightOf(a)) / total;
      return { a, whole: Math.floor(exact), frac: exact - Math.floor(exact) };
    });
    let left = remaining - shares.reduce((s, x) => s + x.whole, 0);
    shares.sort((x, y) => y.frac - x.frac || x.a.localeCompare(y.a));
    for (const s of shares) if (left > 0 && s.frac > 0) (s.whole++, left--);
    let given = 0;
    for (const s of shares) {
      const room = available.get(s.a)! - quotas.get(s.a)!;
      const add = Math.min(s.whole, room);
      quotas.set(s.a, quotas.get(s.a)! + add);
      given += add;
    }
    remaining -= given;
    if (given === 0) break;
  }
  for (const [a, q] of quotas) if (q === 0) quotas.delete(a);
  return quotas;
}

function groupBy<T>(list: T[], key: (t: T) => string): Map<string, T[]> {
  const m = new Map<string, T[]>();
  for (const t of list) {
    const k = key(t);
    const g = m.get(k);
    if (g) g.push(t);
    else m.set(k, [t]);
  }
  return m;
}

function shuffle<T>(list: T[], rng: Rng): T[] {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j]!, a[i]!];
  }
  return a;
}
