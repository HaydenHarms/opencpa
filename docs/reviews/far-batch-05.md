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
