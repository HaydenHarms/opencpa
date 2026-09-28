import { describe, expect, it } from 'vitest';
import type { TbsTask } from '@opencpa/schema';
import {
  gradeJournalEntry,
  gradeTask,
  masteryByArea,
  newCard,
  ratingFor,
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
