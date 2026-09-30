import type { JournalLine, McqItem, TbsItem, TbsTask } from '@opencpa/schema';

export interface GradeResult {
  /** Points earned. */
  earned: number;
  /** Points possible. */
  possible: number;
  correct: boolean;
}

export function gradeMcq(item: McqItem, selected: string): GradeResult {
  const correct = item.answer === selected;
  return { earned: correct ? 1 : 0, possible: 1, correct };
}

const norm = (s: string) => s.trim().toLowerCase().replace(/\s+/g, ' ');
const normCite = (s: string) =>
  s
    .toUpperCase()
    .replace(/[§\s]/g, '')
    .replace(/SECTION/g, '');

type JournalResponse = { account: string; debit?: number; credit?: number }[];

/** Net each account to one signed amount (debits positive), dropping accounts that net to zero. */
function netByAccount(lines: { account: string; debit?: number; credit?: number }[]) {
  const net = new Map<string, number>();
  for (const l of lines) {
    const account = norm(l.account);
    if (!account) continue;
    net.set(account, (net.get(account) ?? 0) + (l.debit ?? 0) - (l.credit ?? 0));
  }
  for (const [account, amount] of net) if (amount === 0) net.delete(account);
  return net;
}

/**
 * Journal entries earn partial credit: one point-share per expected account whose
 * net amount matches. Both the key and the response are netted to one line per
 * account first, so a split entry (two Cash lines) or a gross one (debit and credit
 * the same account) scores the same as the combined entry. A response account that
 * doesn't match (wrong amount, wrong side, or not in the key) costs a share.
 * A task is "correct" only when every account matches and nothing extra was entered.
 */
export function gradeJournalEntry(
  expected: JournalLine[],
  response: JournalResponse,
  points: number,
): GradeResult {
  const want = netByAccount(expected);
  const got = netByAccount(response);
  let matched = 0;
  let extras = 0;
  for (const [account, amount] of got) {
    if (want.get(account) === amount) matched++;
    else extras++;
  }
  const score = Math.max(0, matched - extras) / want.size;
  const correct = matched === want.size && extras === 0;
  return { earned: Math.round(score * points * 100) / 100, possible: points, correct };
}

export type TaskResponse =
  | { type: 'numeric'; value: number }
  | { type: 'journal_entry'; lines: JournalResponse }
  | { type: 'research'; citation: string };

export function gradeTask(task: TbsTask, response: TaskResponse): GradeResult {
  if (task.type !== response.type) return { earned: 0, possible: task.points, correct: false };
  switch (task.type) {
    case 'numeric': {
      const r = response as Extract<TaskResponse, { type: 'numeric' }>;
      const correct = Math.abs(r.value - task.answer) <= task.tolerance;
      return { earned: correct ? task.points : 0, possible: task.points, correct };
    }
    case 'journal_entry':
      return gradeJournalEntry(
        task.answer,
        (response as Extract<TaskResponse, { type: 'journal_entry' }>).lines,
        task.points,
      );
    case 'research': {
      const c = normCite((response as Extract<TaskResponse, { type: 'research' }>).citation);
      const correct = task.answer.some((a) => normCite(a) === c);
      return { earned: correct ? task.points : 0, possible: task.points, correct };
    }
  }
}

export interface SimulationResult extends GradeResult {
  tasks: Record<string, GradeResult>;
}

/**
 * Grade a whole simulation. A task with no response, or a response of the wrong
 * type, earns zero. The simulation is "correct" only when every task is.
 */
export function gradeSimulation(
  item: TbsItem,
  responses: Record<string, TaskResponse | undefined>,
): SimulationResult {
  const tasks: Record<string, GradeResult> = {};
  let earned = 0;
  let possible = 0;
  for (const task of item.tasks) {
    const response = responses[task.id];
    const r = response
      ? gradeTask(task, response)
      : { earned: 0, possible: task.points, correct: false };
    tasks[task.id] = r;
    earned += r.earned;
    possible += r.possible;
  }
  earned = Math.round(earned * 100) / 100;
  return { earned, possible, correct: Object.values(tasks).every((t) => t.correct), tasks };
}
