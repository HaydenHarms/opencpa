import { describe, expect, it } from 'vitest';
import {
  McqItem,
  TbsItem,
  mcqVariant,
  taskAnswer,
  toPublicMcq,
  toPublicTbs,
  variantCount,
} from './index';

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

describe('public projections', () => {
  it('strips the answer, rationales, and explanation from an MCQ', () => {
    const q = McqItem.parse({
      id: 'far-test-0003',
      type: 'mcq',
      blueprint,
      review,
      stem: 'S',
      choices: ['A', 'B', 'C', 'D'].map((id) => ({ id, text: id, rationale: 'secret' })),
      answer: 'C',
      explanation: 'secret',
    });
    const json = JSON.stringify(toPublicMcq(q));
    expect(json).not.toContain('secret');
    expect(json).not.toContain('"answer"');
  });

  it('strips answers, tolerances, and explanations from every simulation task', () => {
    const t = TbsItem.parse({
      id: 'far-test-0004',
      type: 'tbs',
      blueprint,
      review,
      title: 'T',
      scenario: 'S',
      exhibits: [{ title: 'Trial balance', body: '| Account | Amount |' }],
      tasks: [
        {
          id: 'n',
          type: 'numeric',
          prompt: 'P',
          points: 1,
          answer: 123400,
          tolerance: 100,
          explanation: 'secret',
        },
        {
          id: 'j',
          type: 'journal_entry',
          prompt: 'P',
          points: 2,
          accounts: ['Cash', 'Revenue'],
          answer: [
            { account: 'Cash', debit: 100 },
            { account: 'Revenue', credit: 100 },
          ],
          explanation: 'secret',
        },
        {
          id: 'r',
          type: 'research',
          prompt: 'P',
          points: 1,
          answer: ['ASC 842-20-30-1'],
          explanation: 'secret',
        },
      ],
    });
    const pub = toPublicTbs(t);
    const json = JSON.stringify(pub);
    expect(json).not.toContain('secret');
    expect(json).not.toContain('"answer"');
    expect(json).not.toContain('"tolerance"');
    expect(json).not.toContain('842-20-30-1');
    expect(pub.tasks.map((x) => x.type)).toEqual(['numeric', 'journal_entry', 'research']);
    expect(pub.exhibits).toHaveLength(1);
  });
});

describe('select tasks', () => {
  const sim = (rows: object[], options?: string[]) => ({
    id: 'far-test-0005',
    type: 'tbs',
    blueprint,
    review,
    title: 'T',
    scenario: 'S',
    tasks: [
      {
        id: 's',
        type: 'select',
        prompt: 'Classify each cash flow.',
        points: 2,
        ...(options ? { options } : {}),
        rows,
        explanation: 'secret',
      },
    ],
  });
  const shared = ['Operating', 'Investing', 'Financing'];

  it('serves every row its options and no answers', () => {
    const t = TbsItem.parse(
      sim(
        [
          { id: 'a', label: 'Dividends paid', answer: 'Financing' },
          { id: 'b', label: 'Tone', options: ['Accrue', 'Disclose only'], answer: 'Accrue' },
        ],
        shared,
      ),
    );
    const pub = toPublicTbs(t);
    expect(pub.tasks[0]).toEqual({
      id: 's',
      type: 'select',
      prompt: 'Classify each cash flow.',
      points: 2,
      rows: [
        { id: 'a', label: 'Dividends paid', options: shared },
        { id: 'b', label: 'Tone', options: ['Accrue', 'Disclose only'] },
      ],
    });
    expect(JSON.stringify(pub)).not.toMatch(/answer|secret/);
    expect(taskAnswer(t.tasks[0]!)).toEqual({ a: 'Financing', b: 'Accrue' });
  });

  it('rejects a row whose answer is not an option, a row with no options, and repeated row ids', () => {
    const ok = (rows: object[], options?: string[]) =>
      TbsItem.safeParse(sim(rows, options)).success;
    expect(ok([{ id: 'a', label: 'L', answer: 'Operating' }], shared)).toBe(true);
    expect(ok([{ id: 'a', label: 'L', answer: 'Other' }], shared)).toBe(false);
    expect(ok([{ id: 'a', label: 'L', answer: 'Operating' }])).toBe(false);
    expect(
      ok(
        [
          { id: 'a', label: 'L', answer: 'Operating' },
          { id: 'a', label: 'M', answer: 'Investing' },
        ],
        shared,
      ),
    ).toBe(false);
  });
});

describe('MCQ variants', () => {
  const choices = (key: string) =>
    ['A', 'B', 'C', 'D'].map((id) => ({ id, text: `$${id}${key}`, rationale: 'why' }));
  const item = {
    id: 'far-test-0002',
    type: 'mcq',
    blueprint,
    review,
    stem: 'Original stem',
    choices: choices('1'),
    answer: 'B',
    explanation: 'Base.',
    variants: [{ stem: 'Second stem', choices: choices('2'), answer: 'C', explanation: 'Two.' }],
  };

  it('accepts variants and serves each version', () => {
    const q = McqItem.parse(item);
    expect(variantCount(q)).toBe(2);
    expect(mcqVariant(q, 1)).toMatchObject({ stem: 'Second stem', answer: 'C', id: q.id });
    expect(mcqVariant(q, 0).stem).toBe('Original stem');
    expect(mcqVariant(q, 5).stem).toBe('Original stem'); // out of range falls back to the item
    const pub = toPublicMcq(q, 1);
    expect(pub).toMatchObject({ stem: 'Second stem', variant: 1 });
    expect(JSON.stringify(pub)).not.toMatch(/answer|rationale|explanation/);
    expect(toPublicMcq(q, 7).variant).toBe(0);
  });

  it('rejects a variant whose answer is not a choice or whose stem repeats the item', () => {
    const bad = (v: object) =>
      McqItem.safeParse({ ...item, variants: [{ ...item.variants[0], ...v }] }).success;
    expect(bad({ answer: 'E' })).toBe(false);
    expect(bad({ stem: 'Original stem' })).toBe(false);
  });
});
