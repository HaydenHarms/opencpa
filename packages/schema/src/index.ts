import { z } from 'zod';

/** CPA Evolution sections: three core + three discipline. */
export const Section = z.enum(['FAR', 'AUD', 'REG', 'BAR', 'ISC', 'TCP']);
export type Section = z.infer<typeof Section>;

/** AICPA blueprint skill levels. */
export const SkillLevel = z.enum([
  'Remembering and Understanding',
  'Application',
  'Analysis',
  'Evaluation',
]);
export type SkillLevel = z.infer<typeof SkillLevel>;

/** Item IDs look like `far-leases-0001`: section, slug, 4-digit number. */
export const ItemId = z
  .string()
  .regex(
    /^(far|aud|reg|bar|isc|tcp)-[a-z0-9]+(?:-[a-z0-9]+)*-\d{4}$/,
    'id must look like far-leases-0001',
  );

/** Where an item sits in the AICPA blueprint. */
export const Blueprint = z.object({
  section: Section,
  /** Blueprint content area, e.g. "Area II — Select Balance Sheet Accounts". */
  area: z.string().min(1),
  /** Blueprint group/topic within the area, e.g. "Leases". */
  topic: z.string().min(1),
  skill: SkillLevel,
});

/** Review provenance. Nothing ships without passing review. */
export const Review = z.object({
  status: z.enum(['draft', 'reviewed', 'retired']),
  /** Authoritative references checked, e.g. "ASC 842-20-30-1", "IRC §179". */
  references: z.array(z.string()).default([]),
  /** Tax year or standards effective date the answer depends on, if any. */
  asOf: z.string().optional(),
  notes: z.string().optional(),
});

const Choice = z.object({
  id: z.string().regex(/^[A-D]$/),
  text: z.string().min(1),
  /** Why this choice is right, or why it is a tempting wrong answer. */
  rationale: z.string().min(1),
});

const base = {
  id: ItemId,
  blueprint: Blueprint,
  review: Review,
};

const mcqBody = {
  stem: z.string().min(1),
  /** Exactly four choices, A–D, as on the CPA exam. */
  choices: z.array(Choice).length(4, 'an MCQ has exactly four choices (A–D)'),
  answer: z.string().regex(/^[A-D]$/),
  explanation: z.string().min(1),
};

/**
 * Another version of a question with different numbers, so a student who sees the item
 * again can't answer from memory. It tests the same thing with the same distractor errors.
 */
export const McqVariant = z.object(mcqBody);
export type McqVariant = z.infer<typeof McqVariant>;

/** Multiple-choice question. The item itself is variant 0; `variants` are 1, 2, … */
export const McqItem = z
  .object({
    ...base,
    type: z.literal('mcq'),
    ...mcqBody,
    variants: z.array(McqVariant).max(9).optional(),
  })
  .superRefine((q, ctx) => {
    [q, ...(q.variants ?? [])].forEach((v, i) => {
      const where = i ? `variant ${i}: ` : '';
      const ids = v.choices.map((c) => c.id);
      if (new Set(ids).size !== ids.length)
        ctx.addIssue({ code: 'custom', message: `${where}duplicate choice ids` });
      if (!ids.includes(v.answer))
        ctx.addIssue({
          code: 'custom',
          message: `${where}answer ${v.answer} is not one of the choices`,
        });
      if (i && v.stem === q.stem)
        ctx.addIssue({ code: 'custom', message: `${where}stem is identical to the item's` });
    });
  });
export type McqItem = z.infer<typeof McqItem>;

/** How many versions an MCQ has: the item itself plus its variants. */
export function variantCount(q: McqItem): number {
  return 1 + (q.variants?.length ?? 0);
}

/** The item as it reads in variant `v` (0 is the item itself). */
export function mcqVariant(q: McqItem, v: number): McqItem {
  const alt = v > 0 ? q.variants?.[v - 1] : undefined;
  return alt ? { ...q, ...alt } : q;
}

/** One line of a journal entry. Amounts are whole cents to avoid float error. */
export const JournalLine = z.object({
  account: z.string().min(1),
  debit: z.number().int().nonnegative().default(0),
  credit: z.number().int().nonnegative().default(0),
});
export type JournalLine = z.infer<typeof JournalLine>;

/** Tasks that make up a task-based simulation. */
export const TbsTask = z.discriminatedUnion('type', [
  z.object({
    id: z.string(),
    type: z.literal('numeric'),
    prompt: z.string(),
    points: z.number().int().positive(),
    /** Correct value in the stated unit (cents for currency). */
    answer: z.number(),
    tolerance: z.number().nonnegative().default(0),
    unit: z.enum(['cents', 'percent', 'units']).default('cents'),
    explanation: z.string(),
  }),
  z.object({
    id: z.string(),
    type: z.literal('journal_entry'),
    prompt: z.string(),
    points: z.number().int().positive(),
    /** Account list shown to the candidate (includes distractors). */
    accounts: z.array(z.string()).min(2),
    answer: z.array(JournalLine).min(2),
    explanation: z.string(),
  }),
  z.object({
    id: z.string(),
    type: z.literal('research'),
    prompt: z.string(),
    points: z.number().int().positive(),
    /** Accepted citations, e.g. "ASC 606-10-25-1" or "IRC §162(a)". */
    answer: z.array(z.string()).min(1),
    explanation: z.string(),
  }),
  z.object({
    id: z.string(),
    type: z.literal('select'),
    prompt: z.string(),
    points: z.number().int().positive(),
    /** Options offered in every row's drop-down, unless a row lists its own. */
    options: z.array(z.string()).min(2).optional(),
    /**
     * One drop-down per row, as in the exam's option-list and document-review tasks
     * (classify each item, or pick the correction for each highlighted phrase).
     * `answer` is the text of the correct option.
     */
    rows: z
      .array(
        z.object({
          id: z.string(),
          label: z.string().min(1),
          options: z.array(z.string()).min(2).optional(),
          answer: z.string(),
        }),
      )
      .min(1),
    explanation: z.string(),
  }),
]);
export type TbsTask = z.infer<typeof TbsTask>;
export type SelectTask = Extract<TbsTask, { type: 'select' }>;

/** The options in one row's drop-down: its own list, or the task's shared one. */
export function rowOptions(task: SelectTask, row: SelectTask['rows'][number]): string[] {
  return row.options ?? task.options ?? [];
}

/** A task's key as revealed after an attempt. A select task's key is the correct option per row id. */
export function taskAnswer(task: TbsTask) {
  return task.type === 'select'
    ? Object.fromEntries(task.rows.map((r) => [r.id, r.answer]))
    : task.answer;
}

export const Exhibit = z.object({
  title: z.string(),
  /** Markdown (tables allowed). */
  body: z.string(),
});

/** Task-based simulation. */
export const TbsItem = z
  .object({
    ...base,
    type: z.literal('tbs'),
    title: z.string().min(1),
    scenario: z.string().min(1),
    exhibits: z.array(Exhibit).default([]),
    tasks: z.array(TbsTask).min(1),
  })
  .superRefine((t, ctx) => {
    for (const task of t.tasks) {
      if (task.type === 'select') {
        const ids = task.rows.map((r) => r.id);
        if (new Set(ids).size !== ids.length)
          ctx.addIssue({ code: 'custom', message: `task ${task.id}: duplicate row ids` });
        for (const r of task.rows) {
          const opts = rowOptions(task, r);
          if (opts.length < 2)
            ctx.addIssue({
              code: 'custom',
              message: `task ${task.id}: row ${r.id} has no options (give the task or the row a list)`,
            });
          else if (!opts.includes(r.answer))
            ctx.addIssue({
              code: 'custom',
              message: `task ${task.id}: row ${r.id} answer "${r.answer}" is not one of its options`,
            });
          if (new Set(opts).size !== opts.length)
            ctx.addIssue({
              code: 'custom',
              message: `task ${task.id}: row ${r.id} repeats an option`,
            });
        }
        continue;
      }
      if (task.type !== 'journal_entry') continue;
      const dr = task.answer.reduce((s, l) => s + l.debit, 0);
      const cr = task.answer.reduce((s, l) => s + l.credit, 0);
      if (dr !== cr)
        ctx.addIssue({
          code: 'custom',
          message: `task ${task.id}: entry does not balance (${dr} vs ${cr})`,
        });
      const accounts = task.answer.map((l) => l.account);
      if (new Set(accounts).size !== accounts.length)
        ctx.addIssue({
          code: 'custom',
          message: `task ${task.id}: the key must have one line per account (the grader nets by account)`,
        });
      for (const l of task.answer)
        if (!task.accounts.includes(l.account))
          ctx.addIssue({
            code: 'custom',
            message: `task ${task.id}: account "${l.account}" not in account list`,
          });
    }
  });
export type TbsItem = z.infer<typeof TbsItem>;

export const Item = z.union([McqItem, TbsItem]);
export type Item = z.infer<typeof Item>;

/** What the API sends to the browser: no answers, rationales, or explanations. */
export type PublicMcq = Pick<McqItem, 'id' | 'type' | 'blueprint' | 'stem'> & {
  choices: { id: string; text: string }[];
  /** Which version of the item this is (0 is the item itself). */
  variant: number;
};

/** A simulation task as the browser sees it: no answer, tolerance, or explanation. */
export type PublicTbsTask =
  | {
      id: string;
      type: 'numeric';
      prompt: string;
      points: number;
      unit: 'cents' | 'percent' | 'units';
    }
  | { id: string; type: 'journal_entry'; prompt: string; points: number; accounts: string[] }
  | { id: string; type: 'research'; prompt: string; points: number }
  | {
      id: string;
      type: 'select';
      prompt: string;
      points: number;
      rows: { id: string; label: string; options: string[] }[];
    };

export type PublicTbs = Pick<
  TbsItem,
  'id' | 'type' | 'blueprint' | 'title' | 'scenario' | 'exhibits'
> & {
  tasks: PublicTbsTask[];
};

export function toPublicTbs(t: TbsItem): PublicTbs {
  return {
    id: t.id,
    type: t.type,
    blueprint: t.blueprint,
    title: t.title,
    scenario: t.scenario,
    exhibits: t.exhibits,
    tasks: t.tasks.map((task): PublicTbsTask => {
      const { id, prompt, points } = task;
      switch (task.type) {
        case 'numeric':
          return { id, type: 'numeric', prompt, points, unit: task.unit };
        case 'journal_entry':
          return { id, type: 'journal_entry', prompt, points, accounts: task.accounts };
        case 'research':
          return { id, type: 'research', prompt, points };
        case 'select':
          return {
            id,
            type: 'select',
            prompt,
            points,
            rows: task.rows.map((r) => ({
              id: r.id,
              label: r.label,
              options: rowOptions(task, r),
            })),
          };
      }
    }),
  };
}

export function toPublicMcq(q: McqItem, variant = 0): PublicMcq {
  const v = mcqVariant(q, variant);
  return {
    id: q.id,
    type: q.type,
    blueprint: q.blueprint,
    stem: v.stem,
    choices: v.choices.map(({ id, text }) => ({ id, text })),
    variant: v === q ? 0 : variant,
  };
}
