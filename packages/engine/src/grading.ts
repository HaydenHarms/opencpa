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

/**
 * Journal entries earn partial credit: one point-share per expected line matched
 * exactly (same account, same side, same amount). Extra lines cost a share each.
 * A task is "correct" only when every line matches and nothing extra was entered.
 */
export function gradeJournalEntry(
  expected: JournalLine[],
  response: JournalResponse,
  points: number,
): GradeResult {
  const remaining = response.map((l) => ({
    account: norm(l.account),
    debit: l.debit ?? 0,
    credit: l.credit ?? 0,
  }));
  let matched = 0;
  for (const e of expected) {
    const i = remaining.findIndex(
      (r) => r.account === norm(e.account) && r.debit === e.debit && r.credit === e.credit,
    );
    if (i >= 0) {
      matched++;
      remaining.splice(i, 1);
    }
  }
  const extras = remaining.filter((r) => r.account && (r.debit || r.credit)).length;
  const score = Math.max(0, matched - extras) / expected.length;
  const correct = matched === expected.length && extras === 0;
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
