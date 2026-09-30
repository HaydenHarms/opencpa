import { describe, expect, it } from 'vitest';
import type { TbsItem, TbsTask } from '@opencpa/schema';
import {
  gradeJournalEntry,
  gradeSimulation,
  gradeTask,
  masteryByArea,
  newCard,
  ratingFor,
  ratingForScore,
  review,
  Rating,
} from './index';

describe('gradeJournalEntry', () => {
  const expected = [
    { account: 'Cash', debit: 580000, credit: 0 },
    { account: 'Contract liability', debit: 0, credit: 580000 },
  ];

  it('gives full credit for an exact match, ignoring order and case', () => {
    const r = gradeJournalEntry(
      expected,
      [
        { account: 'contract liability', credit: 580000 },
        { account: 'Cash', debit: 580000 },
      ],
      2,
    );
    expect(r).toEqual({ earned: 2, possible: 2, correct: true });
  });

  it('cancels a right line with a wrong extra line', () => {
    const r = gradeJournalEntry(
      expected,
      [
        { account: 'Cash', debit: 580000 },
        { account: 'Revenue', credit: 580000 },
      ],
      2,
    );
    expect(r.earned).toBe(0);
    expect(r.correct).toBe(false);
  });

  it('nets split and gross lines by account before matching', () => {
    const key = [
      { account: 'Income tax expense', debit: 16380000, credit: 0 },
      { account: 'Deferred tax asset', debit: 840000, credit: 0 },
      { account: 'Income taxes payable', debit: 0, credit: 15960000 },
      { account: 'Deferred tax liability', debit: 0, credit: 1260000 },
    ];
    const gross = [
      { account: 'Income tax expense', debit: 15960000 },
      { account: 'Income taxes payable', credit: 15960000 },
      { account: 'Income tax expense', debit: 1260000 },
      { account: 'Deferred tax liability', credit: 1260000 },
      { account: 'Deferred tax asset', debit: 840000 },
      { account: 'Income tax expense', credit: 840000 },
    ];
    expect(gradeJournalEntry(key, gross, 3)).toEqual({ earned: 3, possible: 3, correct: true });
  });

  it('scores a wrong amount as a miss and an extra', () => {
    const r = gradeJournalEntry(
      expected,
      [
        { account: 'Cash', debit: 580000 },
        { account: 'Contract liability', credit: 58000 },
      ],
      2,
    );
    expect(r.earned).toBe(0);
  });

  it('gives half credit when one line is missing', () => {
    const r = gradeJournalEntry(expected, [{ account: 'Cash', debit: 580000 }], 2);
    expect(r.earned).toBe(1);
  });
});

describe('gradeTask', () => {
  it('accepts research citations regardless of spacing and § sign', () => {
    const task = {
      id: 't',
      type: 'research',
      prompt: '',
      points: 1,
      answer: ['IRC §162(a)'] as string[],
      explanation: '',
    } satisfies TbsTask;
    expect(gradeTask(task, { type: 'research', citation: 'irc 162(a)' }).correct).toBe(true);
  });

  it('respects numeric tolerance', () => {
    const task = {
      id: 't',
      type: 'numeric',
      prompt: '',
      points: 1,
      answer: 221000,
      tolerance: 100,
      unit: 'cents',
      explanation: '',
    } satisfies TbsTask;
    expect(gradeTask(task, { type: 'numeric', value: 220950 }).correct).toBe(true);
    expect(gradeTask(task, { type: 'numeric', value: 203200 }).correct).toBe(false);
  });
});

describe('scheduling', () => {
  it('schedules a wrong answer sooner than a right one', () => {
    const now = new Date('2026-01-01T00:00:00Z');
    const again = review(newCard(now), ratingFor(false), now);
    const good = review(newCard(now), ratingFor(true), now);
    expect(again.due.getTime()).toBeLessThanOrEqual(good.due.getTime());
    expect(ratingFor(true, true)).toBe(Rating.Hard);
  });
});

describe('masteryByArea', () => {
  it('weights recent attempts more heavily', () => {
    const now = Date.UTC(2026, 0, 31);
    const day = 86_400_000;
    const m = masteryByArea(
      [
        { section: 'FAR', area: 'Leases', correct: false, at: now - 60 * day },
        { section: 'FAR', area: 'Leases', correct: true, at: now },
      ],
      now,
    );
    expect(m[0]!.attempts).toBe(2);
    expect(m[0]!.score).toBeGreaterThan(0.9);
  });
});

describe('gradeSimulation', () => {
  const sim = {
    id: 'far-test-0005',
    type: 'tbs',
    blueprint: { section: 'FAR', area: 'A', topic: 'T', skill: 'Application' },
    review: { status: 'draft', references: [] },
    title: 'T',
    scenario: 'S',
    exhibits: [],
    tasks: [
      { id: 'n', type: 'numeric', prompt: '', points: 1, answer: 5000, tolerance: 0, unit: 'cents', explanation: '' },
      {
        id: 'j',
        type: 'journal_entry',
        prompt: '',
        points: 2,
        accounts: ['Cash', 'Revenue'],
        answer: [
          { account: 'Cash', debit: 5000, credit: 0 },
          { account: 'Revenue', debit: 0, credit: 5000 },
        ],
        explanation: '',
      },
    ],
  } satisfies TbsItem;

  it('sums task scores and scores a missing response as zero', () => {
    const r = gradeSimulation(sim, { n: { type: 'numeric', value: 5000 } });
    expect(r).toMatchObject({ earned: 1, possible: 3, correct: false });
    expect(r.tasks.j).toEqual({ earned: 0, possible: 2, correct: false });
  });

  it('is correct only when every task is', () => {
    const r = gradeSimulation(sim, {
      n: { type: 'numeric', value: 5000 },
      j: {
        type: 'journal_entry',
        lines: [
          { account: 'Cash', debit: 5000 },
          { account: 'Revenue', credit: 5000 },
        ],
      },
    });
    expect(r).toMatchObject({ earned: 3, possible: 3, correct: true });
  });

  it('gives no credit for a response of the wrong type', () => {
    const r = gradeSimulation(sim, { n: { type: 'research', citation: '5000' } });
    expect(r.tasks.n!.earned).toBe(0);
  });

  it('maps partial scores to review ratings', () => {
    expect(ratingForScore(0.8)).toBe(Rating.Good);
    expect(ratingForScore(0.5)).toBe(Rating.Hard);
    expect(ratingForScore(0.49)).toBe(Rating.Again);
  });
});
