import { describe, expect, it } from 'vitest';
import { McqItem, TbsItem } from './index';

const blueprint = {
  section: 'FAR',
  area: 'Area II — Select Balance Sheet Accounts',
  topic: 'Leases',
  skill: 'Application',
} as const;
const review = { status: 'draft', references: [] } as const;

describe('McqItem', () => {
  const valid = {
    id: 'far-test-0001',
    type: 'mcq',
    blueprint,
    review,
    stem: 'Test stem',
    choices: ['A', 'B', 'C', 'D'].map((id) => ({ id, text: `Choice ${id}`, rationale: 'why' })),
    answer: 'B',
    explanation: 'Because.',
  };

  it('accepts a valid item', () => {
    expect(McqItem.safeParse(valid).success).toBe(true);
  });

  it('rejects an answer that is not a choice', () => {
    expect(McqItem.safeParse({ ...valid, answer: 'E' }).success).toBe(false);
  });

  it('rejects anything other than four choices', () => {
    const e = { id: 'E', text: 'Choice E', rationale: 'why' };
    expect(McqItem.safeParse({ ...valid, choices: [...valid.choices, e] }).success).toBe(false);
    expect(McqItem.safeParse({ ...valid, choices: valid.choices.slice(0, 3) }).success).toBe(false);
  });

  it('rejects a malformed id', () => {
    expect(McqItem.safeParse({ ...valid, id: 'FAR_1' }).success).toBe(false);
  });
});

describe('TbsItem', () => {
  const tbs = (answer: { account: string; debit?: number; credit?: number }[]) => ({
    id: 'far-test-0002',
    type: 'tbs',
    blueprint,
    review,
    title: 'T',
    scenario: 'S',
    tasks: [
      {
        id: 't1',
        type: 'journal_entry',
        prompt: 'Record it.',
        points: 2,
        accounts: ['Cash', 'Revenue', 'Unearned revenue'],
        answer,
        explanation: 'E',
      },
    ],
  });

  it('accepts a balanced entry', () => {
    const r = TbsItem.safeParse(
      tbs([
        { account: 'Cash', debit: 100 },
        { account: 'Revenue', credit: 100 },
      ]),
    );
    expect(r.success).toBe(true);
  });

  it('rejects an unbalanced entry', () => {
    const r = TbsItem.safeParse(
      tbs([
        { account: 'Cash', debit: 100 },
        { account: 'Revenue', credit: 90 },
      ]),
    );
    expect(r.success).toBe(false);
  });

  it('rejects an account missing from the list', () => {
    const r = TbsItem.safeParse(
      tbs([
        { account: 'Cash', debit: 100 },
        { account: 'Sales', credit: 100 },
      ]),
    );
    expect(r.success).toBe(false);
  });
});
