# FAR variants 01

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**What this adds:** 39 variants, three for each of 13 numeric items from FAR batch 05. Each variant has new company names and numbers, but the same test and the same distractor errors. With the item itself, each question now has four versions. The legacy tool also had four.

## Process

1. **Builders.** `scripts/batches/far-variants-01.py` gives each item a builder that writes the whole question (stem, choices, rationales and explanation) from parameters. It computes every amount with `Decimal` and rounds half up.
2. **Faithfulness check.** Parameter set 0 must rebuild the reviewed item word for word, and the script refuses to write anything if it doesn't. All 13 rebuilt exactly on the first run, which shows the templates match the reviewed text.
3. **Audit.** `common.attach_variants()` sorts numeric choices in ascending order. `audit()` then runs the usual checks on every version and flags any two versions with the same correct answer.
4. **Blind verification.** One verifier agent solved all 39 variants from the stems and choices only. It matched the key on all 39, found no second defensible answer and could name the error behind every distractor.

| Item | Area | Blueprint topic |
| --- | --- | --- |
| `far-foreign-currency-transactions-0001` | I | Income statement |
| `far-performance-metrics-0002` | I | Financial Statement Ratios and Performance Metrics |
| `far-balance-sheet-0004` | I | Balance sheet |
| `far-cash-flows-0007` | I | Statement of cash flows |
| `far-consolidated-statements-0006` | I | Consolidated financial statements |
| `far-software-purchased-0001` | II | Intangible assets |
| `far-equity-method-0002` | II | Investments (Equity method investments) |
| `far-payables-cutoff-0001` | II | Payables and accrued liabilities |
| `far-bonds-between-interest-dates-0001` | II | Debt (Notes and bonds payable) |
| `far-inventory-gross-profit-method-0001` | II | Inventory |
| `far-subsequent-events-0004` | III | Subsequent events |
| `far-income-taxes-rate-change-0001` | III | Accounting for income taxes |
| `far-revenue-contract-modification-0001` | III | Revenue recognition |

## Fixes

| Item | Finding | Fix |
| --- | --- | --- |
| `far-equity-method-0002` (item) | Found while writing the template: the stem said Varro's income "is earned evenly," but it gave $200,000 of $380,000 for the second half. | Removed "is earned evenly and". |
| `far-equity-method-0002` variant 2 (verifier) | The 5% stake's fair value ($200,000) implied a higher value per share than the 20% purchase price, which contradicts "a premium for obtaining significant influence". | The stake's fair value is now $90,000. Recomputed: key $530,000. |
| `far-equity-method-0002`, all versions (verifier, optional) | "There are no basis differences" sat awkwardly next to a stated premium, since a premium normally creates equity-method goodwill. | Replaced with "Any excess of cost over Jade's share of Varro's book value is attributable to goodwill, which Jade does not amortize." The last clause pins the private-company election. |

The changed family was re-verified blind (see below).

## Revision 2: the key's letter now moves

In the first version of this batch, choices were sorted in ascending order (the AICPA convention) and every version used the same three errors. The key therefore sat on the same letter in all four versions for 12 of 13 families, and a student who remembered "it was D" could answer a repeat without solving it.

Revision 2 gives each family a pool of four or five distractors, each tied to a named error, the same approach as FAR variants 02. Each variant shows a different three. The reviewed item keeps its reviewed three, and parameter set 0 still rebuilds it word for word. The script now refuses to write a family whose key has the same letter in every version.

| Item | Key letters by version | New distractor errors |
| --- | --- | --- |
| `far-foreign-currency-transactions-0001` | C D D D | no Year 2 remeasurement at settlement |
| `far-performance-metrics-0002` | D C C D | income tax not added back; beginning total assets |
| `far-balance-sheet-0004` | B C A C | warranty left noncurrent; whole lease liability moved to current |
| `far-cash-flows-0007` | A B C B | deferred tax increase subtracted; discount amortization subtracted |
| `far-consolidated-statements-0006` | B A C B | interest eliminated but not the note; a full year's interest eliminated |
| `far-software-purchased-0001` | B C B B | training and conversion left out |
| `far-equity-method-0002` | D C C D | equity method applied retroactively to the old stake |
| `far-payables-cutoff-0001` | C B D B | duplicate left in; December goods left out |
| `far-bonds-between-interest-dates-0001` | D C C D | a full six months of interest added |
| `far-inventory-gross-profit-method-0001` | C B C B | gross profit rate used as the cost ratio |
| `far-subsequent-events-0004` | A B B A | settlement treated as a Year 2 event |
| `far-income-taxes-rate-change-0001` | C D C C | only the rate change on the beginning differences |
| `far-revenue-contract-modification-0001` | B A B B | standalone selling price used for all remaining units |

A fresh verifier agent solved all 39 revision 2 variants blind. It matched the key on all 39 and found no second defensible answer or inconsistency. Its fixes:

| Finding | Fix |
| --- | --- |
| Required: in bonds variant 3, the "accrued interest subtracted" choice ($3,010,000) sat just above face and read like two stacked errors. | Added a "face plus accrued interest, premium left out" distractor to the pool, used in variants 2 and 3. |
| Optional: consolidation variant 3's double elimination of interest was contrived. | Replaced with the full-year-interest distractor. |
| Optional: in balance sheet variant 2, two distractors were $5,000 apart. | The warranty liability is now $80,000, which puts them $35,000 apart. |
| Optional: FX variant 1 has a weak "loss in both years" distractor. | Kept. It is the reviewed item's own distractor. |

A blind recheck of the four changed variants matched every key and could name every distractor's error.

## Re-verification (revision 1)

After the fixes, the verifier blind-rechecked all four versions of `far-equity-method-0002`:

- It matched the key on all four ($525,000, $414,000, $530,000 and $460,000).
- Each distractor comes from one nameable error.
- The implied premiums are all positive (10%, 73%, 14% and 67%).
- No fixes were needed.

## Serving

- A session builds each item's version from how many times the student has answered it: 0, 1, 2 or 3 prior answers, taken modulo 4. It stores the choice in `practice_sessions.variants`.
- Each attempt records the version it answered (`attempts.variant`).
- Grading, the reveal, the resume view and the Claude connector all use the version the student actually saw.
