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

/** Multiple-choice question. */
export const McqItem = z
  .object({
    ...base,
    type: z.literal('mcq'),
    stem: z.string().min(1),
    /** Exactly four choices, A–D, as on the CPA exam. */
    choices: z.array(Choice).length(4, 'an MCQ has exactly four choices (A–D)'),
    answer: z.string().regex(/^[A-D]$/),
    explanation: z.string().min(1),
  })
  .superRefine((q, ctx) => {
    const ids = q.choices.map((c) => c.id);
    if (new Set(ids).size !== ids.length)
      ctx.addIssue({ code: 'custom', message: 'duplicate choice ids' });
    if (!ids.includes(q.answer))
      ctx.addIssue({ code: 'custom', message: `answer ${q.answer} is not one of the choices` });
  });
export type McqItem = z.infer<typeof McqItem>;

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
]);
export type TbsTask = z.infer<typeof TbsTask>;

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
      if (task.type !== 'journal_entry') continue;
      const dr = task.answer.reduce((s, l) => s + l.debit, 0);
      const cr = task.answer.reduce((s, l) => s + l.credit, 0);
      if (dr !== cr)
        ctx.addIssue({
          code: 'custom',
          message: `task ${task.id}: entry does not balance (${dr} vs ${cr})`,
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
};

export function toPublicMcq(q: McqItem): PublicMcq {
  return {
    id: q.id,
    type: q.type,
    blueprint: q.blueprint,
    stem: q.stem,
    choices: q.choices.map(({ id, text }) => ({ id, text })),
  };
}
