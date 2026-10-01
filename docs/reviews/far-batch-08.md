# Review report: FAR batch 08

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**14 items**, all written from scratch in `scripts/batches/far-batch-08.py`. Every item is numeric and ships with three variants, 42 in all, so the batch adds 56 problems. Every variant family moves the key's letter.

## Plan

This slice takes blueprint tasks that `scripts/far-coverage.py` lists with fewer than two items: deferred taxes and the tax provision entry, lessee initial measurement, subsequent events, the income statement, the statement of cash flows, correcting consolidated statements, and investments at fair value. Another slice covers III.A, III.B, III.C and II.G.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-income-statement-0004` | I.A.2a Prepare a single-step or multi-step income statement (income from continuing operations before taxes, from a trial balance with discontinued operations, OCI items and dividends) | Application |
| `far-cash-flows-0008` | I.A.5a Prepare a statement of cash flows and required disclosures (interest paid, net of amounts capitalized) | Application |
| `far-cash-flows-0009` | I.A.5d Derive the impact of transactions on the statement of cash flows (net cash used in investing activities) | Analysis |
| `far-consolidated-statements-0008` | I.A.6b Adjust consolidated statements to correct identified errors (80% subsidiary, NCI at fair value) | Application |
| `far-investments-fair-value-0001` | II.E.1b Calculate the carrying amount of investments at fair value (trading, available-for-sale, held-to-maturity and equity securities) | Application |
| `far-investments-fair-value-0002` | II.E.1c Calculate investment income on investments at fair value (sale of AFS securities with reclassification; equity fair value changes) | Application |
| `far-income-taxes-deferred-0002` | III.D.d Calculate deferred tax assets and liabilities (scheduled enacted rates; a proposed rate) | Application |
| `far-income-taxes-provision-0002` | III.D.e Prepare the journal entry for the tax provision (debit to income tax expense; DTL and DTA changes netting) | Application |
| `far-income-taxes-provision-0003` | III.D.e Prepare the journal entry for the tax provision (credit to the DTL account, including the tax effect of AFS gains in OCI) | Application |
| `far-lessee-operating-0004` | III.F.c Calculate lessee assets and liabilities (ROU asset with payment at commencement, initial direct costs and an incentive) | Application |
| `far-subsequent-events-0005` | III.G.b Calculate adjustments for subsequent events (year-end inventory) | Application |
| `far-subsequent-events-0006` | III.G.b Calculate adjustments for subsequent events (claims and litigation liability; an event after issuance) | Application |
| `far-subsequent-events-0007` | III.G.c Derive the impact of subsequent events (current ratio for a covenant) | Analysis |
| `far-subsequent-events-0008` | III.G.c Derive the impact of subsequent events (allowance for credit losses; private company, available-to-be-issued date) | Analysis |

- **Batch mix:** by skill, 0 / 11 / 3 (Remembering and Understanding / Application / Analysis); by area, 4 / 2 / 8.
- **Variants:** 42 (three per item).
- **Version-0 key letters:** A 5, B 2, C 1, D 6. Eleven of 14 version-0 keys are A or D, to offset the bank's lean toward B.

| Item | Key letters (version 0, variants 1-3) |
| --- | --- |
| `far-income-statement-0004` | D B B C |
| `far-cash-flows-0008` | A B B D |
| `far-cash-flows-0009` | A B B B |
| `far-consolidated-statements-0008` | A C B B |
| `far-investments-fair-value-0001` | D C B D |
| `far-investments-fair-value-0002` | D C C C |
| `far-income-taxes-deferred-0002` | A B C A |
| `far-income-taxes-provision-0002` | B C A D |
| `far-income-taxes-provision-0003` | B B A C |
| `far-lessee-operating-0004` | C B D C |
| `far-subsequent-events-0005` | D B C B |
| `far-subsequent-events-0006` | D B B C |
| `far-subsequent-events-0007` | D B C B |
| `far-subsequent-events-0008` | A B B B |

## Process

Each item is a builder with four parameter sets and a pool of four or five distractors, each from one named error. Each version shows a different three. The script refuses a family whose key letter never moves. Every amount is computed with `Decimal` and rounded half up. The present value factors in `far-lessee-operating-0004` were recomputed from the formula. Company names were checked against `content/` and `scripts/batches/` before use. The key phrasing of each stem was searched in `content/far` for echoes of existing items.

The script ran with no FAIL lines and no audit warnings, and `pnpm content:validate` passed.

## Blind verification

One verifier solved all 56 versions blind and matched the key on every one. It named an error behind every numeric distractor, and it found no key that relies on a superseded rule. Fixes:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-subsequent-events-0007` (required) | In versions 0 and 1, the corrected current ratio breached the stated covenant, which brings in ASC 470-10-45-11 debt classification, and the stem lacks the facts for it. | The covenants in those versions are now 1.75 and 1.40, so the corrected ratio meets the covenant in every version. |
| `far-subsequent-events-0006` variant 2 (required) | "a Elland store". | "one of Elland's stores" in every version. |
| `far-consolidated-statements-0008` | "Measured the NCI at fair value on the acquisition date" read as an election; under US GAAP it is required, and acquisition-date accounting is BAR. | The stem now says only when the parent acquired its interest. |
| `far-subsequent-events-0008` | Ruskin's year-end default facts could be read as calling for a larger year-end allowance. | The stem says the draft amount for Ruskin was management's year-end expected loss on all information then available. |
| `far-income-taxes-deferred-0002` | Version 0 had no distractor for the proposed-rate trap. | Version 0 now shows it in place of the DTA-added distractor. |

Kept, with reasons:
- **`far-cash-flows-0009` stays Analysis.** The verifier read it as classify-and-sum (Application). It maps to I.A.5d, "derive the impact of transactions on the statement of cash flows", which the blueprint marks Analysis, and the student must work out each transaction's cash effect and section (insurance proceeds, a noncash land purchase, T-bills as cash equivalents). The review gate should confirm.
- **`far-investments-fair-value-0001`** includes a held-to-maturity security at amortized cost as a distractor source; the question asks for investments at fair value, so it stays on II.E.1b.
- **`far-investments-fair-value-0002`:** the double-counted recycled gain is the weakest distractor in versions 1–3, but it is a real error. The only replacement suggested was a two-error distractor, which the quality bar discourages.

**Second blind pass.** A fresh verifier re-solved all 32 changed versions across batches 07 and 08, and matched every key. Applied:
- `far-subsequent-events-0007`, versions 0 and 2: a new flood amount, because recognizing only the flood (a wrong path) rounded to the key.
- Version 0 of `far-subsequent-events-0006`, `far-consolidated-statements-0008` and `far-subsequent-events-0008`: each swaps one distractor from its pool. In each, every distractor had erred in the same direction, which made the key the most extreme choice.
- Variant 3 of `far-subsequent-events-0008`: a different set of distractors, so the key letter moves across versions.

Every swapped-in distractor comes from a pool the first pass had already verified.

## Review gate

See `far-batch-07.md` for the sample and method; the gate ran once on both batches (**84.0%**, no major items).

| Item | Gate | Fix |
| --- | --- | --- |
| `far-subsequent-events-0007` (72%, minor) | Every explanation said the corrected ratio was "below" the covenant after the covenant values were raised; in every version it meets it. | The builder now computes "meets" / "falls below" from the numbers. Quality bar item 8 now requires this for every comparative in an explanation. |
| `far-subsequent-events-0008` (82%, minor) | A private company's allowance on current receivables, without saying whether it elects ASU 2025-05. | The stem says Langdale has not elected the practical expedient or the related policy election. The key does not change. |
| `far-investments-fair-value-0001` (78%, minor) | The stem recited the held-to-maturity and trading tests word for word. | The stem now gives facts (a treasury desk turning the securities over within weeks; a board resolution to hold bonds to maturity, backed by cash forecasts). It adds a distractor for "only trading securities are at fair value". |
| `far-investments-fair-value-0002` (nit) | "No interest was due" didn't rule out accrued interest. | "Ignore interest on these securities." |
| `far-lessee-operating-0004` (nit) | Entity type not stated (private companies may elect a risk-free rate). | The lessee is a public business entity. |

Exam-ready: `cash-flows-0009` (84%; the gate confirmed the Analysis tag, at the low end), `lessee-operating-0004` (86%), `investments-fair-value-0002` (83%), and from the sample `income-taxes-deferred-0002` (87%), `income-taxes-provision-0003` (86%) and `consolidated-statements-0008` (86%).

**Final blind check (done 2026-09-30):** a fresh verifier re-solved all 16 versions of the four changed items and matched every key. It found no second answer and no superseded rule. One required fix is applied: `subsequent-events-0008` no longer says the company "is finalizing" statements that were available to be issued on April 2, which could have moved the cutoff past the April 10 event. Also applied: `investments-fair-value-0001` now says the entity expects no credit losses and records no allowance, since "expects to collect all contractual cash flows" doesn't by itself mean a zero allowance under CECL.

**Bank after batches 07 and 08:** 175 FAR MCQs, 12% / 52% / 36% by skill and 34.3% / 32.0% / 33.7% by area, all in range. Analysis is 1 point above its floor and Area III is 1.3 points below its ceiling, so the next batches lean toward Areas I and II with Analysis at 40% or more.
