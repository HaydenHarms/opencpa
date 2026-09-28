# Contributing to OpenCPA

Thanks for helping. Most contributions are **questions and simulations**, and every one goes through review before students see it.

## Ground rules

- **Original content only.** Never submit AICPA released questions or anything from Becker, UWorld, Gleim, Roger, or other commercial providers. Writing your own question _about_ a topic is fine; copying or closely paraphrasing someone else's is not.
- **One item per file**, named after its id: `content/far/far-leases-0001.yaml`.
- **Amounts in simulations are whole cents** (`$5,800.00` → `580000`) so grading never hits floating-point errors.
- New items start as `review.status: draft`. Only `reviewed` items are served.

## Review checklist

An item moves to `reviewed` only when a reviewer has confirmed all of the following:

1. **Answer key.** Re-solved independently; every calculation checked by running it, not by eye.
2. **Current authority.** Consistent with current GAAP/GASB, PCAOB/AICPA standards, or IRC amounts. Cite them in `review.references`; set `review.asOf` for anything year-dependent (tax thresholds, effective dates).
3. **One defensible answer.** Distractors are plausible but clearly wrong, and the stem doesn't give the answer away.
4. **Blueprint tag.** `section`, `area`, `topic`, and `skill` match the current AICPA blueprint.
5. **Explanations.** The item explains why the answer is right, and every choice has a `rationale` saying why it's right or why it's tempting.

## Multiple-choice example

```yaml
id: far-leases-0001
type: mcq
blueprint:
  section: FAR
  area: Area II — Select Balance Sheet Accounts
  topic: Leases
  skill: Application
review:
  status: draft
  references: [ASC 842-20-30-1]
stem: >
  On January 1, a lessee signs a 5-year lease with annual payments of $20,000
  due each December 31. The lessee's incremental borrowing rate is 6%
  (PV of an ordinary annuity, 5 periods, 6% = 4.2124). What lease liability
  is recorded at commencement?
choices:
  - { id: A, text: '$84,248', rationale: 'Correct: $20,000 × 4.2124.' }
  - {
      id: B,
      text: '$100,000',
      rationale: 'Sum of undiscounted payments; ignores the time value of money.',
    }
  - {
      id: C,
      text: '$89,303',
      rationale: 'Uses an annuity-due factor, but payments are in arrears.',
    }
  - { id: D, text: '$80,000', rationale: 'Drops one payment instead of discounting.' }
answer: A
explanation: >
  The lease liability is the present value of the remaining lease payments,
  discounted at the rate implicit in the lease or, if not readily determinable,
  the lessee's incremental borrowing rate.
```

## Simulation (TBS) task types

| Type            | Student does                         | Graded by                                                           |
| --------------- | ------------------------------------ | ------------------------------------------------------------------- |
| `journal_entry` | Builds an entry from an account list | Line-by-line match; partial credit; extra lines cost credit         |
| `numeric`       | Enters an amount                     | Exact match within `tolerance`                                      |
| `research`      | Cites authoritative literature       | Match against accepted citations (`ASC 606-10-25-1`, `IRC §162(a)`) |

The schema in `packages/schema/src/index.ts` is the source of truth. Journal entries must balance, and every answer account must appear in the task's account list; CI rejects anything that doesn't.

## Checking your work

```bash
pnpm install
pnpm content:validate
```

## Code contributions

Run `pnpm typecheck && pnpm test` before opening a PR. Keep grading deterministic: the tutor explains, it never scores.
