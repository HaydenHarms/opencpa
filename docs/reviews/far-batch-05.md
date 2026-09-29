# Review report: FAR batch 05

**25 items**, all written from scratch (`scripts/batches/far-batch-05.py`), aimed at the gaps the batch 04 review named.

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

## Plan

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-foreign-currency-transactions-0001` | I.A.2 Calculate transaction gains or losses on foreign-currency monetary items | Application |
| `far-performance-metrics-0002` | I.F Calculate performance metrics (EBITDA, asset turnover) | Application |
| `far-comprehensive-income-0003` | I.A.3 Identify items classified as other comprehensive income | Remembering and Understanding |
| `far-nfp-statement-of-activities-0001` | I.B.2 Prepare an NFP statement of activities | Application |
| `far-balance-sheet-0004` | I.A.1 Detect and correct discrepancies (noncurrent liabilities) | Analysis |
| `far-cash-flows-0007` | I.A.5 Detect and correct discrepancies (operating section) | Analysis |
| `far-changes-in-equity-0002` | I.A.4 Detect and correct discrepancies (retained earnings) | Analysis |
| `far-consolidated-statements-0005` | I.A.6 Detect and correct discrepancies (intercompany loan) | Analysis |
| `far-notes-0003` | I.A.7 Compare the notes with the statements | Analysis |
| `far-troubled-debt-restructuring-0001` | II.H.1 Understand when a change in debt terms is a troubled debt restructuring | Remembering and Understanding |
| `far-software-purchased-0001` | II.F Calculate the carrying amount of purchased software | Application |
| `far-investments-equity-securities-0001` | II.E.1 Impairment of investments reported at fair value (measurement alternative) | Application |
| `far-equity-method-0002` | II.E.3 Calculate the carrying amount of an equity method investment | Application |
| `far-payables-cutoff-0001` | II.G Reconcile and investigate accounts payable (search for unrecorded liabilities) | Analysis |
| `far-bonds-between-interest-dates-0001` | II.H.1 Calculate the carrying amount of bonds and prepare journal entries | Application |
| `far-inventory-gross-profit-method-0001` | II.C Calculate the carrying amount of inventory | Application |
| `far-property-dividend-0001` | II.I Equity transactions (property dividend) | Application |
| `far-subsequent-events-0004` | III.G Derive the impact of subsequent events | Analysis |
| `far-accounting-errors-0004` | III.A Derive the impact of an error correction | Analysis |
| `far-contingencies-0005` | III.B Review documentation for recognition versus disclosure | Analysis |
| `far-revenue-contract-modification-0001` | III.C Determine the amount of revenue (contract modification) | Application |
| `far-revenue-material-right-0001` | III.C Determine the amount of revenue (customer option) | Application |
| `far-lessee-variable-payments-0001` | III.F Recall the treatment of variable lease payments | Remembering and Understanding |
| `far-income-taxes-rate-change-0001` | III.D Calculate deferred taxes (enacted rate change) | Application |
| `far-nfp-gifts-in-kind-0001` | III.C Calculate contributions of nonfinancial assets | Application |

## Process

Same pipeline, with the rules added after batch 04: elections the Codification makes optional are named in the stem; tasks the blueprint marks Remembering and Understanding are tagged that way; company names and amounts checked against the bank (seven clashing names were renamed before verification); every amount computed with `Decimal`, rounded half up.

## Tallies

| Measure | Batch 05 | Bank (125 FAR items) | Blueprint target |
| --- | --- | --- | --- |
| Area I / II / III | 9 / 8 / 8 (36% / 32% / 32%) | 44 / 42 / 39 (35% / 34% / 31%) | 30–40% / 30–40% / 25–35% |
| Remembering and Understanding | 3 (12%) | 15 (12%) | 5–15% |
| Application | 13 (52%) | 63 (50%) | 45–55% |
| Analysis | 9 (36%) | 47 (38%) | 35–45% |

## Blind verification

A separate agent solved all 25 items from the stems and choices only. It **matched the key on 25 of 25** (with low confidence on one, fixed below), confirmed every topic is FAR, and found no superseded rules. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-notes-0003` (required) | Nothing showed the draft's 200,000 shares and $3.00 EPS were pre-split, so the statements might already reflect the split | Stem says 200,000 is the number outstanding throughout Year 1 before any split |
| `far-payables-cutoff-0001` (required) | $626,000 was defensible if the utility bill were classified as an accrued liability | Stem says Kirk records all vendor bills, including utilities, in accounts payable |
| `far-equity-method-0002` | The price of the new 20% implied a higher fair value for the old 10%, inviting a remeasurement argument | Stem gives the fair value immediately before the purchase and says the price includes a premium for significant influence |
| `far-nfp-statement-of-activities-0001`, `far-property-dividend-0001`, `far-nfp-gifts-in-kind-0001` | One weak distractor each | Replaced with single-error figures (releases omitted; carrying amount with a gain; painting recognized but warehouse omitted) |

## Review gate

A fresh review agent graded the batch without reading this report first. **All 25 keys correct; average estimated pass likelihood 82.4%; 16 exam-ready, 9 minor, 0 major.** Batch and bank mixes are inside every blueprint range. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-notes-0003` → `far-notes-0004` | Nearly duplicated `far-subsequent-events-0003` (same income, shares, split and EPS), and "before any split" pointed at the answer | Retired and replaced: the inconsistent note is now an income tax policy that still splits deferred taxes into current and noncurrent (superseded by ASU 2015-17), matched by a current deferred tax asset on the draft balance sheet |
| `far-consolidated-statements-0005` → `far-consolidated-statements-0006` | The stem listed the intercompany balances in the draft, so it was Application, not Analysis | Retired and replaced: the draft gives only its total assets and how it was prepared; the student must find the intercompany loan |
| `far-lessee-variable-payments-0001` | Key was the longest choice and paired with a second CPI choice | Choices rewritten to similar length, one index-based and three performance- or usage-based |
| `far-troubled-debt-restructuring-0001` | Three choices were combinations of the same two conditions | Choices are now four scenarios; only one has both financial difficulty and a concession |
| `far-revenue-contract-modification-0001` | "Distinct performance obligation" is a giveaway label | Stem describes the units instead |
| `far-investments-equity-securities-0001` | "Qualitative assessment indicates impairment" stated the conclusion | Stem gives the event (loss of a customer providing 40% of revenue) |
| `far-payables-cutoff-0001` | "Accepts the draft" was weak; the $18,000 December 28 fact echoed another item | Replaced with $663,000 (FOB destination goods included); the goods-in-transit amount and dates changed |

The reviewer's other points (template reuse in `far-accounting-errors-0004`, a collection-criteria description in `far-nfp-gifts-in-kind-0001`) are left as they are; the quality bar now covers template reuse for future batches.

Gaps for batch 06 named by the reviewer: fund determination, the NFP statement of financial position, NFP cash flows and NFP notes, amortized-cost investments and debt covenants. Revenue recognition is heavily covered (about 10% of the bank). Keep Remembering and Understanding to about three items.

A blind check of the seven changed items matched the key on all seven with no required fixes. It read `far-consolidated-statements-0006` as Application; the tag stays Analysis because the student must find the intercompany loan in the supporting schedules and correct a draft total (the FAR "detect, investigate and correct discrepancies" task for consolidated statements), and the next review should confirm.
