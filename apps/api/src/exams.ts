/**
 * Mock exams (`docs/plans/exam-mode.md`, Phase B). The server runs the clock, so a refresh or
 * another device can't reset it. Testlets are graded when submitted, and the attempts count
 * toward mastery and review scheduling, but no key, rationale or explanation leaves the server
 * until the exam is finished: only the report route reveals them.
 */
import { Hono, type Context } from 'hono';
import { z } from 'zod';
import { mcqVariant, toPublicMcq, toPublicTbs, type Item } from '@opencpa/schema';
import {
  AREA_WEIGHTS,
  EXAM_LAYOUTS,
  buildExam,
  examClock,
  examExpired,
  gradeMcq,
  gradeSimulation,
  newCard,
  ratingFor,
  ratingForScore,
  review,
  type ExamLayout,
  type GradeResult,
} from '@opencpa/engine';
import type { Env } from './auth';
import { byId, mcqs, simulations } from './content';
import { attemptStatements, rowToCard, taskResponse, type CardRow } from './attempts';
import { pickVariants, reveal, revealSimulation, type Responses } from './sessions';

type ExamRow = {
  id: string;
  user_id: string;
  section: string;
  status: 'active' | 'finished' | 'abandoned';
  testlets: string;
  variants: string;
  current: number;
  responses: string;
  flags: string;
  testlet_used: string;
  started_at: number;
  break_started_at: number | null;
  break_ended_at: number | null;
  paused_at: number | null;
  paused_ms: number;
  pauses: number;
  finished_at: number | null;
  ended_by: 'submitted' | 'time' | null;
};

/** A multiple-choice response is the choice picked; a simulation's is its task responses. */
type McqResponse = { selected: string };
type SavedResponse = McqResponse | Responses;

function parse(row: ExamRow) {
  return {
    layout: EXAM_LAYOUTS[row.section]!,
    testlets: JSON.parse(row.testlets) as string[][],
    variants: JSON.parse(row.variants) as Record<string, number>,
    responses: JSON.parse(row.responses) as Record<string, SavedResponse>,
    flags: JSON.parse(row.flags) as string[],
    testletUsed: JSON.parse(row.testlet_used) as number[],
  };
}

function clockOf(row: ExamRow, now: number) {
  return examClock(
    EXAM_LAYOUTS[row.section]!,
    {
      startedAt: row.started_at,
      breakStartedAt: row.break_started_at,
      breakEndedAt: row.break_ended_at,
      pausedAt: row.paused_at,
      pausedMs: row.paused_ms,
      finishedAt: row.finished_at,
    },
    now,
  );
}

function loadExam(db: D1Database, userId: string, id: string) {
  return db
    .prepare('SELECT * FROM exams WHERE id = ? AND user_id = ?')
    .bind(id, userId)
    .first<ExamRow>();
}

/** Grade one item's response as it stands; no response scores zero. */
function gradeItem(item: Item, variant: number, response: SavedResponse | undefined): GradeResult {
  if (item.type === 'mcq') {
    const selected = (response as McqResponse | undefined)?.selected;
    return selected
      ? gradeMcq(mcqVariant(item, variant), selected)
      : { earned: 0, possible: 1, correct: false };
  }
  return gradeSimulation(item, (response as Responses | undefined) ?? {});
}

/**
 * Submit the open testlet with `responses` merged in: write an attempt and review card for each
 * answered item, record the clock, and open the next testlet, or finish the exam after the last
 * one or when time is up. Unanswered items write no attempt, so they stay unseen for Practice.
 */
async function submitTestlet(
  db: D1Database,
  row: ExamRow,
  now: number,
  timeUp: boolean,
): Promise<void> {
  const { testlets, variants, responses, testletUsed } = parse(row);
  const clock = clockOf(row, now);
  const ids = testlets[row.current]!.filter((id) => byId.has(id));
  const answered = ids.filter((id) => responses[id] !== undefined);
  const cards = new Map<string, CardRow>();
  if (answered.length) {
    const { results } = await db
      .prepare(
        `SELECT * FROM review_cards WHERE user_id = ? AND item_id IN (${answered.map(() => '?').join(',')})`,
      )
      .bind(row.user_id, ...answered)
      .all<CardRow & { item_id: string }>();
    for (const r of results) cards.set(r.item_id, r);
  }
  const date = new Date(now);
  const statements = answered.flatMap((id) => {
    const item = byId.get(id)!;
    const variant = variants[id] ?? 0;
    const result = gradeItem(item, variant, responses[id]);
    const rating =
      item.type === 'mcq'
        ? ratingFor(result.correct)
        : ratingForScore(result.possible ? result.earned / result.possible : 0);
    const prior = cards.get(id);
    const card = review(prior ? rowToCard(prior) : newCard(date), rating, date);
    return attemptStatements(
      db,
      row.user_id,
      item,
      responses[id],
      result,
      undefined,
      card,
      row.id,
      variant,
    );
  });

  const used = Math.min(clock.usedMs, clock.limitMs);
  const next = row.current + 1;
  const finished = timeUp || next >= testlets.length || clock.usedMs >= clock.limitMs;
  const endedBy = finished && !timeUp && clock.usedMs < clock.limitMs ? 'submitted' : 'time';
  // Time can run out on a break; the break ends with the exam.
  const breakEnded =
    finished && row.break_started_at !== null && row.break_ended_at === null
      ? now
      : row.break_ended_at;
  await db.batch([
    ...statements,
    db
      .prepare(
        `UPDATE exams SET current = ?, responses = ?, testlet_used = ?, status = ?, finished_at = ?,
           ended_by = ?, break_ended_at = ?
         WHERE id = ? AND current = ? AND status = 'active'`,
      )
      .bind(
        finished ? row.current : next,
        JSON.stringify(responses),
        JSON.stringify([...testletUsed, used]),
        finished ? 'finished' : 'active',
        finished ? now : null,
        finished ? endedBy : null,
        breakEnded,
        row.id,
        row.current,
      ),
  ]);
}

/**
 * Every exam route starts here: if the clock ran out (past the grace period), submit the open
 * testlet as saved and end the exam. Returns the row as it now stands.
 */
async function settle(db: D1Database, row: ExamRow, now: number): Promise<ExamRow> {
  if (row.status !== 'active' || !examExpired(clockOf(row, now))) return row;
  await submitTestlet(db, row, now, true);
  return (await loadExam(db, row.user_id, row.id))!;
}

function publicItem(id: string, variant: number) {
  const item = byId.get(id)!;
  return item.type === 'mcq' ? toPublicMcq(item, variant) : toPublicTbs(item);
}

/** What the exam screen needs: the clock, the testlets, and the open testlet's items. */
function examView(row: ExamRow, now: number) {
  const { layout, testlets, variants, responses, flags, testletUsed } = parse(row);
  const clock = clockOf(row, now);
  const open = row.status === 'active' ? testlets[row.current]!.filter((id) => byId.has(id)) : [];
  const hidden = clock.paused || clock.onBreak || row.status !== 'active';
  return {
    id: row.id,
    section: row.section,
    status: row.status,
    endedBy: row.ended_by,
    current: row.current,
    layout,
    testlets: layout.testlets.map((t, i) => ({
      ...t,
      submitted: i < testletUsed.length,
      usedMs: i < testletUsed.length ? testletUsed[i]! - (testletUsed[i - 1] ?? 0) : null,
    })),
    clock: {
      ...clock,
      pauses: row.pauses,
      breakTaken: row.break_started_at !== null,
      breakAvailable: breakAvailable(row, layout, open, responses, clock),
    },
    serverTime: now,
    // While paused or on a break the items stay hidden, so the time off can't be used on them.
    items: hidden ? null : open.map((id) => publicItem(id, variants[id] ?? 0)),
    responses: hidden
      ? {}
      : Object.fromEntries(open.flatMap((id) => (responses[id] ? [[id, responses[id]]] : []))),
    flags: hidden ? [] : flags.filter((id) => open.includes(id)),
  };
}

/** The break is offered once, after the set testlet and before anything in the next is answered. */
function breakAvailable(
  row: ExamRow,
  layout: ExamLayout,
  open: string[],
  responses: Record<string, SavedResponse>,
  clock: ReturnType<typeof clockOf>,
) {
  return (
    row.status === 'active' &&
    row.current === layout.breakAfter &&
    row.break_started_at === null &&
    !clock.paused &&
    open.every((id) => responses[id] === undefined)
  );
}

type Tally = { name: string; right: number; total: number; earned: number; possible: number };

/** Score a finished exam: questions right, simulation points, and the two combined 50/50. */
function scoreExam(row: ExamRow) {
  const { testlets, variants, responses } = parse(row);
  const graded = testlets.flat().flatMap((id) => {
    const item = byId.get(id);
    return item ? [{ item, result: gradeItem(item, variants[id] ?? 0, responses[id]) }] : [];
  });
  const questions = graded.filter((g) => g.item.type === 'mcq');
  const sims = graded.filter((g) => g.item.type === 'tbs');
  const mcq = { right: questions.filter((g) => g.result.correct).length, total: questions.length };
  const sim = {
    earned: Math.round(sims.reduce((s, g) => s + g.result.earned, 0) * 100) / 100,
    possible: sims.reduce((s, g) => s + g.result.possible, 0),
  };
  const mcqPct = mcq.total ? mcq.right / mcq.total : 0;
  const simPct = sim.possible ? sim.earned / sim.possible : 0;
  const combined = mcq.total && sim.possible ? (mcqPct + simPct) / 2 : mcq.total ? mcqPct : simPct;
  return { graded, mcq, sim, mcqPct, simPct, combined };
}

function tallyBy(graded: ReturnType<typeof scoreExam>['graded'], key: (i: Item) => string) {
  const m = new Map<string, Tally>();
  for (const { item, result } of graded) {
    const t = m.get(key(item)) ?? { name: key(item), right: 0, total: 0, earned: 0, possible: 0 };
    if (item.type === 'mcq') {
      t.total++;
      if (result.correct) t.right++;
    } else {
      t.earned = Math.round((t.earned + result.earned) * 100) / 100;
      t.possible += result.possible;
    }
    m.set(t.name, t);
  }
  return [...m.values()];
}

function summary(row: ExamRow, now: number) {
  const { mcq, sim, mcqPct, simPct, combined } = scoreExam(row);
  const clock = clockOf(row, now);
  return {
    id: row.id,
    section: row.section,
    startedAt: row.started_at,
    finishedAt: row.finished_at,
    endedBy: row.ended_by,
    mcq,
    sim,
    mcqPct,
    simPct,
    combined,
    usedMs: Math.min(clock.usedMs, clock.limitMs),
    pausedMs: clock.pausedMs,
    pauses: row.pauses,
  };
}

const sectionSchema = z.enum(['FAR', 'AUD', 'REG', 'BAR', 'ISC', 'TCP']);
const mcqResponse = z.object({ selected: z.string().regex(/^[A-F]$/) });
const simResponse = z
  .record(taskResponse)
  .refine((r) => Object.keys(r).length <= 20, 'at most 20 tasks');
const saveBody = z.object({
  testlet: z.number().int().min(0),
  responses: z.record(z.unknown()),
  flags: z.array(z.string()).max(50),
});

type Vars = { userId: string };
export const exams = new Hono<{ Bindings: Env; Variables: Vars }>();

/** Past mock exams with their scores, newest first; `section` narrows to one section. */
exams.get('/', async (c) => {
  const section = c.req.query('section')?.toUpperCase() ?? null;
  const { results } = await c.env.DB.prepare(
    `SELECT * FROM exams WHERE user_id = ? AND status = 'finished' AND (?2 IS NULL OR section = ?2)
     ORDER BY started_at DESC`,
  )
    .bind(c.get('userId'), section)
    .all<ExamRow>();
  const now = Date.now();
  return c.json(results.map((r) => summary(r, now)));
});

/** The Mock exam intro page: whether the section has one, the exam in progress, the bank size. */
exams.get('/current', async (c) => {
  const section = sectionSchema.safeParse(c.req.query('section')?.toUpperCase());
  if (!section.success) return c.json({ error: 'unknown section' }, 400);
  const layout = EXAM_LAYOUTS[section.data];
  const userId = c.get('userId');
  const db = c.env.DB;
  const { results } = await db
    .prepare('SELECT * FROM exams WHERE user_id = ? AND section = ? ORDER BY started_at DESC')
    .bind(userId, section.data)
    .all<ExamRow>();
  const now = Date.now();
  const rows = await Promise.all(results.map((r) => settle(db, r, now)));
  const active = rows.find((r) => r.status === 'active') ?? null;
  const usedSims = new Set(
    rows.flatMap((r) => parse(r).testlets.flat()).filter((id) => byId.get(id)?.type === 'tbs'),
  );
  const sims = simulations.filter((s) => s.blueprint.section === section.data);
  return c.json({
    layout: layout ?? null,
    questions: mcqs.filter((q) => q.blueprint.section === section.data).length,
    simulations: sims.length,
    freshSimulations: sims.filter((s) => !usedSims.has(s.id)).length,
    active: active && {
      id: active.id,
      startedAt: active.started_at,
      current: active.current,
      clock: clockOf(active, now),
    },
    history: rows.filter((r) => r.status === 'finished').map((r) => summary(r, now)),
  });
});

/** Start a mock exam. An unfinished one in the section is abandoned; its submitted testlets still count. */
exams.post('/', async (c) => {
  const body = z.object({ section: sectionSchema }).safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  const { section } = body.data;
  const layout = EXAM_LAYOUTS[section];
  if (!layout) return c.json({ error: `no ${section} mock exam yet` }, 404);
  const userId = c.get('userId');
  const db = c.env.DB;

  const toPool = (i: Item) => ({ id: i.id, area: i.blueprint.area, topic: i.blueprint.topic });
  const questions = mcqs.filter((q) => q.blueprint.section === section).map(toPool);
  const sims = simulations.filter((s) => s.blueprint.section === section).map(toPool);
  const need = (k: 'mcq' | 'tbs') =>
    layout.testlets.filter((t) => t.kind === k).reduce((s, t) => s + t.count, 0);
  if (questions.length < need('mcq') || sims.length < need('tbs'))
    return c.json({ error: `not enough ${section} items for a mock exam yet` }, 409);

  const [earlier, seen] = await Promise.all([
    db
      .prepare('SELECT testlets FROM exams WHERE user_id = ?')
      .bind(userId)
      .all<{ testlets: string }>(),
    db
      .prepare('SELECT DISTINCT item_id FROM attempts WHERE user_id = ?')
      .bind(userId)
      .all<{ item_id: string }>(),
  ]);
  const testlets = buildExam({
    layout,
    questions,
    simulations: sims,
    usedInExams: new Set(
      earlier.results.flatMap((r) => (JSON.parse(r.testlets) as string[][]).flat()),
    ),
    seen: new Set(seen.results.map((r) => r.item_id)),
    weights: AREA_WEIGHTS[section],
  });
  const ids = testlets.flat();
  const versions = await pickVariants(db, userId, ids);
  const variants = Object.fromEntries(ids.map((id, i) => [id, versions[i]!]));

  const id = crypto.randomUUID();
  const now = Date.now();
  await db.batch([
    db
      .prepare(
        `UPDATE exams SET status = 'abandoned', finished_at = ?,
           paused_ms = paused_ms + CASE WHEN paused_at IS NULL THEN 0 ELSE ? - paused_at END, paused_at = NULL
         WHERE user_id = ? AND section = ? AND status = 'active'`,
      )
      .bind(now, now, userId, section),
    db
      .prepare(
        'INSERT INTO exams (id, user_id, section, testlets, variants, started_at) VALUES (?, ?, ?, ?, ?, ?)',
      )
      .bind(id, userId, section, JSON.stringify(testlets), JSON.stringify(variants), now),
  ]);
  const row = await loadExam(db, userId, id);
  return c.json(examView(row!, now), 201);
});

type Ctx = Context<{ Bindings: Env; Variables: Vars }>;

/** Load the student's exam, settle the clock, and hand it to `fn`; 404 if it isn't theirs. */
async function withExam(c: Ctx, fn: (row: ExamRow, now: number) => Promise<Response> | Response) {
  const id = z.string().uuid().safeParse(c.req.param('id'));
  const found = id.success ? await loadExam(c.env.DB, c.get('userId'), id.data) : null;
  if (!found) return c.json({ error: 'not found' }, 404);
  const now = Date.now();
  return fn(await settle(c.env.DB, found, now), now);
}

exams.get('/:id', (c) => withExam(c, (row, now) => c.json(examView(row, now))));

/** Why the open testlet can't take answers right now, or null when it can. */
function closed(row: ExamRow, now: number, testlet: number) {
  if (row.status !== 'active') return 'This exam has ended.';
  if (testlet !== row.current) return 'That testlet is already submitted.';
  const clock = clockOf(row, now);
  if (clock.paused) return 'The exam is paused.';
  if (clock.onBreak) return 'You are on a break.';
  return null;
}

/** Validate saved responses against the open testlet: only its items, in the right shape. */
function checkResponses(row: ExamRow, input: Record<string, unknown>, flags: string[]) {
  const { testlets } = parse(row);
  const open = testlets[row.current]!;
  const out: Record<string, SavedResponse> = {};
  for (const [id, value] of Object.entries(input)) {
    if (!open.includes(id)) return { error: `${id} is not in the open testlet` };
    if (value === null) continue;
    const item = byId.get(id);
    const parsed =
      item?.type === 'mcq' ? mcqResponse.safeParse(value) : simResponse.safeParse(value);
    if (!parsed.success) return { error: `bad response for ${id}` };
    out[id] = parsed.data as SavedResponse;
  }
  if (flags.some((id) => !open.includes(id))) return { error: 'flags must be in the open testlet' };
  return { responses: out };
}

/** Replace the open testlet's saved responses and flags (the screen saves as the student works). */
function applySave(row: ExamRow, responses: Record<string, SavedResponse>, flags: string[]) {
  const saved = parse(row);
  const open = new Set(saved.testlets[row.current]!);
  const merged = Object.fromEntries(
    Object.entries(saved.responses).filter(([id]) => !open.has(id)),
  );
  Object.assign(merged, responses);
  const keptFlags = saved.flags.filter((id) => !open.has(id));
  return {
    responses: JSON.stringify(merged),
    flags: JSON.stringify([...keptFlags, ...new Set(flags)]),
  };
}

exams.put('/:id/responses', async (c) => {
  const body = saveBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  return withExam(c, async (row, now) => {
    const why = closed(row, now, body.data.testlet);
    if (why) return c.json({ error: why, exam: examView(row, now) }, 409);
    const checked = checkResponses(row, body.data.responses, body.data.flags);
    if ('error' in checked) return c.json({ error: checked.error }, 400);
    const next = applySave(row, checked.responses, body.data.flags);
    await c.env.DB.prepare(
      "UPDATE exams SET responses = ?, flags = ? WHERE id = ? AND current = ? AND status = 'active'",
    )
      .bind(next.responses, next.flags, row.id, row.current)
      .run();
    return c.json({ saved: true, clock: examView({ ...row, ...next }, now).clock });
  });
});

/** Submit the open testlet (with its final responses). It locks; nothing is revealed. */
exams.post('/:id/submit', async (c) => {
  const body = saveBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: body.error.flatten() }, 400);
  return withExam(c, async (row, now) => {
    // A repeat of a submit that already went through (a retry after a dropped response).
    if (row.status !== 'active' || body.data.testlet < row.current)
      return c.json(examView(row, now));
    const why = closed(row, now, body.data.testlet);
    if (why) return c.json({ error: why, exam: examView(row, now) }, 409);
    const checked = checkResponses(row, body.data.responses, body.data.flags);
    if ('error' in checked) return c.json({ error: checked.error }, 400);
    await submitTestlet(
      c.env.DB,
      { ...row, ...applySave(row, checked.responses, body.data.flags) },
      now,
      false,
    );
    const after = (await loadExam(c.env.DB, row.user_id, row.id))!;
    return c.json(examView(after, now));
  });
});

/** Pause, resume, and the optional break. Each returns the updated exam. */
const transitions: Record<
  string,
  {
    allowed: (row: ExamRow, now: number) => string | null;
    sql: string;
    binds: (now: number) => unknown[];
  }
> = {
  pause: {
    allowed: (row, now) => {
      const clock = clockOf(row, now);
      if (row.status !== 'active') return 'This exam has ended.';
      if (clock.paused) return 'Already paused.';
      if (clock.onBreak) return 'You are on a break.';
      return null;
    },
    sql: 'UPDATE exams SET paused_at = ?, pauses = pauses + 1 WHERE id = ? AND paused_at IS NULL',
    binds: (now) => [now],
  },
  resume: {
    allowed: (row) => (row.status === 'active' && row.paused_at !== null ? null : 'Not paused.'),
    sql: 'UPDATE exams SET paused_ms = paused_ms + (? - paused_at), paused_at = NULL WHERE id = ? AND paused_at IS NOT NULL',
    binds: (now) => [now],
  },
  'break/start': {
    allowed: (row, now) => {
      const { layout, testlets, responses } = parse(row);
      const open = row.status === 'active' ? testlets[row.current]! : [];
      return breakAvailable(row, layout, open, responses, clockOf(row, now))
        ? null
        : 'The break isn’t available now.';
    },
    sql: 'UPDATE exams SET break_started_at = ? WHERE id = ? AND break_started_at IS NULL',
    binds: (now) => [now],
  },
  'break/end': {
    allowed: (row, now) =>
      row.status === 'active' && clockOf(row, now).onBreak ? null : 'You are not on a break.',
    sql: 'UPDATE exams SET break_ended_at = ? WHERE id = ? AND break_ended_at IS NULL',
    binds: (now) => [now],
  },
};

for (const [path, t] of Object.entries(transitions)) {
  exams.post(`/:id/${path}`, (c) =>
    withExam(c, async (row, now) => {
      const why = t.allowed(row, now);
      if (why) return c.json({ error: why, exam: examView(row, now) }, 409);
      await c.env.DB.prepare(t.sql)
        .bind(...t.binds(now), row.id)
        .run();
      return c.json(examView((await loadExam(c.env.DB, row.user_id, row.id))!, now));
    }),
  );
}

/** The score report. Only for a finished exam: this is where keys are first revealed. */
exams.get('/:id/report', (c) =>
  withExam(c, (row, now) => {
    if (row.status !== 'finished')
      return c.json({ error: 'The report is ready when the exam is finished.' }, 409);
    const { layout, testlets, variants, responses, flags } = parse(row);
    const { graded } = scoreExam(row);
    const weights = AREA_WEIGHTS[row.section] ?? {};
    return c.json({
      ...summary(row, now),
      layout,
      testlets: examView(row, now).testlets,
      byArea: tallyBy(graded, (i) => i.blueprint.area)
        .map((t) => ({ ...t, weight: weights[t.name] ?? null }))
        .sort((a, b) => a.name.localeCompare(b.name)),
      byTopic: tallyBy(graded, (i) => i.blueprint.topic).sort((a, b) =>
        a.name.localeCompare(b.name),
      ),
      bySkill: tallyBy(graded, (i) => i.blueprint.skill),
      review: testlets.map((ids) =>
        ids.flatMap((id) => {
          const item = byId.get(id);
          if (!item) return [];
          const variant = variants[id] ?? 0;
          const response = responses[id];
          return [
            {
              item: publicItem(id, variant),
              flagged: flags.includes(id),
              answered: response !== undefined,
              result:
                item.type === 'mcq'
                  ? (() => {
                      const version = mcqVariant(item, variant);
                      const selected = (response as McqResponse | undefined)?.selected ?? '';
                      return reveal(version, selected, gradeMcq(version, selected).correct);
                    })()
                  : revealSimulation(item, (response as Responses | undefined) ?? {}),
            },
          ];
        }),
      ),
    });
  }),
);

/**
 * Items in the student's unfinished mock exams. The Claude connector won't reveal anything
 * about them, so Claude can't be asked for a key mid-exam.
 */
export async function activeExamItems(db: D1Database, userId: string) {
  const { results } = await db
    .prepare("SELECT testlets FROM exams WHERE user_id = ? AND status = 'active'")
    .bind(userId)
    .all<{ testlets: string }>();
  return new Set(results.flatMap((r) => (JSON.parse(r.testlets) as string[][]).flat()));
}
