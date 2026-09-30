/**
 * Library search. Runs in the browser over the public search index, with no model calls.
 *
 * It matches beyond exact wording in three ways:
 * - stemming, so "leases", "leasing" and "leased" all match "lease";
 * - an accounting synonym map, so "fixed assets" finds Property, plant and equipment,
 *   "DTL" finds Accounting for income taxes, and "842" finds lessee accounting;
 * - typo tolerance (trigram similarity), so "recievables" still finds receivables.
 *
 * Topic names weigh most, then references and simulation titles, then question text.
 */
import type { SearchDoc } from './api';

/** Each group is one idea; a query that hits any phrase in a group also matches the others. */
const SYNONYMS: string[][] = [
  [
    'lease',
    'lessee',
    'lessor',
    'right of use',
    'rou asset',
    'finance lease',
    'operating lease',
    'asc 842',
  ],
  [
    'ppe',
    'property plant and equipment',
    'fixed asset',
    'depreciation',
    'capitalized interest',
    'asset retirement obligation',
    'asc 360',
  ],
  [
    'receivable',
    'accounts receivable',
    'bad debt',
    'allowance for credit losses',
    'credit loss',
    'cecl',
    'uncollectible',
    'asc 326',
  ],
  ['payable', 'accounts payable', 'accrued liability', 'accrual', 'accrued expense'],
  [
    'debt',
    'bond',
    'note payable',
    'bond premium',
    'bond discount',
    'effective interest',
    'covenant',
    'extinguishment',
    'asc 470',
  ],
  [
    'income tax',
    'deferred tax',
    'dta',
    'dtl',
    'tax provision',
    'valuation allowance',
    'temporary difference',
    'asc 740',
  ],
  [
    'cash flow',
    'statement of cash flows',
    'operating activities',
    'investing activities',
    'financing activities',
    'indirect method',
    'direct method',
    'asc 230',
  ],
  [
    'consolidation',
    'consolidated',
    'subsidiary',
    'parent company',
    'noncontrolling interest',
    'nci',
    'intercompany',
    'elimination',
    'asc 810',
  ],
  [
    'business combination',
    'acquisition method',
    'acquiree',
    'bargain purchase',
    'purchase price allocation',
    'asc 805',
  ],
  ['goodwill', 'indefinite lived', 'impairment', 'asc 350'],
  ['intangible', 'patent', 'trademark', 'copyright', 'amortization', 'cloud computing', 'software'],
  [
    'revenue',
    'revenue recognition',
    'performance obligation',
    'five step',
    'transaction price',
    'contract with customer',
    'asc 606',
  ],
  [
    'inventory',
    'fifo',
    'lifo',
    'weighted average',
    'lower of cost',
    'net realizable value',
    'nrv',
    'cost of goods sold',
    'cogs',
    'asc 330',
  ],
  [
    'equity',
    'stockholders equity',
    'shareholders equity',
    'treasury stock',
    'dividend',
    'stock split',
    'apic',
    'retained earnings',
    'asc 505',
  ],
  ['earnings per share', 'eps', 'diluted', 'asc 260'],
  [
    'government',
    'governmental',
    'gasb',
    'fund',
    'modified accrual',
    'measurement focus',
    'fiduciary',
    'proprietary',
    'enterprise fund',
    'budgetary',
  ],
  [
    'not for profit',
    'nfp',
    'nonprofit',
    'net assets',
    'donor restriction',
    'contribution',
    'asc 958',
  ],
  [
    'fair value',
    'level 1',
    'level 2',
    'level 3',
    'valuation technique',
    'market approach',
    'income approach',
    'asc 820',
  ],
  [
    'investment',
    'security',
    'equity method',
    'held to maturity',
    'available for sale',
    'trading security',
    'amortized cost',
    'asc 320',
    'asc 321',
    'asc 323',
  ],
  [
    'contingency',
    'contingent',
    'loss contingency',
    'litigation',
    'lawsuit',
    'warranty',
    'guarantee',
    'commitment',
    'asc 450',
  ],
  ['subsequent event', 'recognized subsequent event', 'nonrecognized', 'after year end', 'asc 855'],
  [
    'accounting change',
    'error correction',
    'restatement',
    'change in estimate',
    'change in principle',
    'retrospective',
    'prospective',
    'asc 250',
  ],
  [
    'ratio',
    'current ratio',
    'quick ratio',
    'turnover',
    'return on assets',
    'return on equity',
    'roa',
    'roe',
    'ebitda',
    'margin',
    'liquidity',
    'solvency',
    'financial statement analysis',
  ],
  ['derivative', 'hedge', 'hedging', 'interest rate swap', 'swap', 'forward contract', 'asc 815'],
  [
    'stock compensation',
    'share based payment',
    'stock option',
    'rsu',
    'restricted stock',
    'asc 718',
  ],
  [
    'managerial',
    'cost accounting',
    'variance',
    'cvp',
    'break even',
    'contribution margin',
    'absorption costing',
    'variable costing',
    'make or buy',
    'budget',
    'forecast',
  ],
  [
    'capital budgeting',
    'npv',
    'net present value',
    'irr',
    'internal rate of return',
    'cost of capital',
    'wacc',
    'valuation',
  ],
  [
    'foreign currency',
    'translation',
    'remeasurement',
    'functional currency',
    'exchange rate',
    'asc 830',
  ],
  ['cash', 'bank reconciliation', 'overdraft', 'cash equivalent', 'restricted cash'],
  [
    'public company',
    'sec',
    'segment',
    'regulation s x',
    'regulation s k',
    'form 10 k',
    'interim reporting',
    'non gaap',
  ],
  ['research and development', 'r d', 'asc 730'],
  ['comprehensive income', 'oci', 'other comprehensive income', 'unrealized gain'],
  ['notes to financial statements', 'disclosure', 'footnote', 'related party'],
  ['special purpose framework', 'cash basis', 'tax basis', 'other comprehensive basis', 'ocboa'],
  ['risk management', 'coso', 'enterprise risk', 'erm', 'internal control'],
];

const STOP = new Set(
  'a an and are as at be by do does for from how i in is it of on or the to what when which with vs versus'.split(
    ' ',
  ),
);

/** Lowercase, expand symbols, and split into words. */
function words(s: string): string[] {
  return s
    .toLowerCase()
    .replace(/pp&e/g, 'ppe')
    .replace(/r&d/g, 'r d')
    .replace(/[’']/g, '')
    .split(/[^a-z0-9]+/)
    .filter((w) => w && !STOP.has(w));
}

/** A light suffix stripper: enough to fold plurals and common verb endings together. */
export function stem(w: string): string {
  if (w.length <= 3 || /^\d/.test(w)) return w;
  if (w.endsWith('ies') && w.length > 4) return w.slice(0, -3) + 'y';
  if (w.endsWith('sses')) return w.slice(0, -2);
  if (w.endsWith('ing') && w.length > 5) return w.slice(0, -3);
  if (w.endsWith('ed') && w.length > 4) return w.slice(0, -2);
  if (w.endsWith('es') && /(ch|sh|x|z)es$/.test(w)) return w.slice(0, -2);
  if (w.endsWith('s') && !/(ss|us|is)$/.test(w)) return w.slice(0, -1);
  return w;
}

const terms = (s: string) => words(s).map(stem);

function trigrams(w: string): Set<string> {
  const p = `  ${w} `;
  const out = new Set<string>();
  for (let i = 0; i < p.length - 2; i++) out.add(p.slice(i, i + 3));
  return out;
}

/** Dice similarity of trigram sets, 0–1. */
function similarity(a: string, b: string): number {
  const ta = trigrams(a);
  const tb = trigrams(b);
  let common = 0;
  for (const t of ta) if (tb.has(t)) common++;
  return (2 * common) / (ta.size + tb.size);
}

/** Optimal-string-alignment distance (edits, with swapped neighbors counting as one). */
function editDistance(a: string, b: string): number {
  if (Math.abs(a.length - b.length) > 2) return 3;
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array<number>(b.length).fill(0)]);
  for (let j = 1; j <= b.length; j++) d[0]![j] = j;
  for (let i = 1; i <= a.length; i++)
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      let v = Math.min(d[i - 1]![j]! + 1, d[i]![j - 1]! + 1, d[i - 1]![j - 1]! + cost);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1])
        v = Math.min(v, d[i - 2]![j - 2]! + 1);
      d[i]![j] = v;
    }
  return d[a.length]![b.length]!;
}

/** Spelling closeness, 0–1: trigram overlap, or a small edit distance for short typos. */
function closeness(a: string, b: string): number {
  if (a.length < 4 || b.length < 4) return 0;
  const tri = similarity(a, b);
  const allowed = a.length >= 8 ? 2 : 1;
  const ed = editDistance(a, b);
  return Math.max(tri, ed <= allowed ? 1 - ed / (a.length + 1) : 0);
}

interface Field {
  weight: number;
  terms: Set<string>;
  /** The field's terms joined with spaces, padded, for phrase matching. */
  joined: string;
}

function field(text: string, weight: number): Field {
  const t = terms(text);
  return { weight, terms: new Set(t), joined: ` ${t.join(' ')} ` };
}

const SYNONYM_TERMS = SYNONYMS.map((g) => g.map((p) => terms(p).join(' ')).filter(Boolean));

interface Query {
  /** Each query word, stemmed. */
  words: string[];
  /** Per word: rarer words count more (1 for rare, down to 0.3 for words in most items). */
  weights: number[];
  /** Synonym groups the query named outright as a phrase (these count fully). */
  named: Set<string[]>;
  /** Synonym groups the query touches, as stemmed phrases, minus what the query said itself. */
  related: string[][];
}

function parse(input: string, df: (w: string) => number): Query {
  const qWords = terms(input);
  const joined = ` ${qWords.join(' ')} `;
  const named = new Set<string[]>();
  const related = SYNONYM_TERMS.filter((g) => {
    const exact = g.some((p) => joined.includes(` ${p} `));
    if (exact && g.some((p) => p.includes(' ') && joined.includes(` ${p} `))) named.add(g);
    return exact || g.some((p) => !p.includes(' ') && fuzzyIn(p, qWords));
  });
  return { words: qWords, weights: qWords.map((w) => Math.max(0.3, 1 - df(w))), related, named };
}

function fuzzyIn(term: string, list: string[]): boolean {
  return list.some((w) => closeness(term, w) >= 0.6);
}

/** How well one query word matches a field: 1 exact, less for a prefix or near-spelling. */
function wordScore(w: string, f: Field): number {
  if (f.terms.has(w)) return 1;
  let best = 0;
  for (const t of f.terms) {
    if (w.length >= 3 && t.startsWith(w)) best = Math.max(best, 0.85);
    else {
      const c = closeness(w, t);
      if (c >= 0.55) best = Math.max(best, c * 0.75);
    }
  }
  return best;
}

/** Score a record made of weighted fields. 0 means no match. */
function score(q: Query, fields: Field[]): number {
  let total = 0;
  let hit = 0;
  q.words.forEach((w, i) => {
    let best = 0;
    for (const f of fields) best = Math.max(best, wordScore(w, f) * f.weight);
    if (best > 0) hit++;
    total += best * q.weights[i]!;
  });
  // Related ideas from the synonym map count, but less than the words actually typed.
  for (const group of q.related) {
    let best = 0;
    for (const f of fields)
      for (const p of group) if (f.joined.includes(` ${p} `)) best = Math.max(best, f.weight);
    total += best * (q.named.has(group) ? 1 : 0.6);
    if (best > 0 && hit < q.words.length) hit += 0.5;
  }
  if (!q.words.length) return 0;
  // Favor records that cover more of the query.
  return total * Math.min(1, hit / q.words.length);
}

export interface TopicHit {
  section: string;
  area: string;
  topic: string;
  score: number;
  /** Items in the topic that matched the query themselves. */
  matches: number;
  items: number;
}

export interface ItemHit {
  doc: SearchDoc;
  score: number;
}

export interface Results {
  topics: TopicHit[];
  items: ItemHit[];
}

/** Build once per index; returns a function that runs a query. */
export function makeSearch(docs: SearchDoc[]) {
  const itemFields = docs.map((d) => ({
    doc: d,
    fields: [
      field(d.topic, 2),
      field(d.area, 0.5),
      field(d.title ?? '', 1.5),
      field(d.refs.join(' '), 1.5),
      field(d.text, 1),
    ],
  }));
  const topicKeys = new Map<
    string,
    { section: string; area: string; topic: string; docs: number }
  >();
  for (const d of docs) {
    const k = `${d.section}::${d.topic}`;
    const t = topicKeys.get(k) ?? { section: d.section, area: d.area, topic: d.topic, docs: 0 };
    t.docs++;
    topicKeys.set(k, t);
  }
  const topicFields = new Map(
    [...topicKeys].map(([k, t]) => [k, [field(t.topic, 3), field(t.area, 1), field(t.section, 1)]]),
  );

  // Share of items each term appears in, for down-weighting common words like "asset".
  const counts = new Map<string, number>();
  for (const { fields } of itemFields) {
    const seen = new Set<string>();
    for (const f of fields) for (const t of f.terms) seen.add(t);
    for (const t of seen) counts.set(t, (counts.get(t) ?? 0) + 1);
  }
  const df = (w: string) => (counts.get(w) ?? 0) / Math.max(1, itemFields.length);

  return function search(input: string, section?: string): Results {
    const q = parse(input, df);
    if (!q.words.length) return { topics: [], items: [] };

    const items: ItemHit[] = [];
    const perTopic = new Map<string, { best: number; count: number }>();
    for (const { doc, fields } of itemFields) {
      if (section && doc.section !== section) continue;
      const s = score(q, fields);
      if (s < 0.5) continue;
      items.push({ doc, score: s });
      const k = `${doc.section}::${doc.topic}`;
      const t = perTopic.get(k) ?? { best: 0, count: 0 };
      t.best = Math.max(t.best, s);
      t.count++;
      perTopic.set(k, t);
    }

    const topics: TopicHit[] = [];
    for (const [k, t] of topicKeys) {
      if (section && t.section !== section) continue;
      const own = score(q, topicFields.get(k)!);
      const hits = perTopic.get(k);
      // A topic ranks on its own name first, then on how much of its content matched.
      const s = own + (hits ? hits.best * 0.5 + Math.log2(1 + hits.count) * 0.3 : 0);
      if (s < 0.6) continue;
      topics.push({ ...t, score: s, matches: hits?.count ?? 0, items: t.docs });
    }

    topics.sort((a, b) => b.score - a.score);
    items.sort((a, b) => b.score - a.score);
    return { topics: topics.slice(0, 12), items: items.slice(0, 15) };
  };
}
