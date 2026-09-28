export interface AttemptSummary {
  section: string;
  area: string;
  correct: boolean;
  /** Epoch ms. */
  at: number;
}

export interface Mastery {
  section: string;
  area: string;
  attempts: number;
  /** 0–1, recency-weighted accuracy. */
  score: number;
}

/**
 * Recency-weighted accuracy per blueprint area. Each attempt's weight halves
 * every `halfLifeDays`, so old mistakes fade as the student improves.
 */
export function masteryByArea(
  attempts: AttemptSummary[],
  now = Date.now(),
  halfLifeDays = 14,
): Mastery[] {
  const groups = new Map<
    string,
    { section: string; area: string; w: number; wc: number; n: number }
  >();
  for (const a of attempts) {
    const key = `${a.section}::${a.area}`;
    const g = groups.get(key) ?? { section: a.section, area: a.area, w: 0, wc: 0, n: 0 };
    const ageDays = Math.max(0, now - a.at) / 86_400_000;
    const weight = Math.pow(0.5, ageDays / halfLifeDays);
    g.w += weight;
    g.wc += a.correct ? weight : 0;
    g.n++;
    groups.set(key, g);
  }
  return [...groups.values()]
    .map((g) => ({ section: g.section, area: g.area, attempts: g.n, score: g.w ? g.wc / g.w : 0 }))
    .sort((a, b) => a.section.localeCompare(b.section) || a.area.localeCompare(b.area));
}
