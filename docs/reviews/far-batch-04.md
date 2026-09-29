# Review report: FAR batch 04

**25 items**, all written from scratch (`scripts/batches/far-batch-04.py`), aimed at the gaps the batch 03 review named.

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

## Plan

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-budget-variance-0001` | I.F Calculate variances between budget and actual results | Application |
| `far-performance-metrics-0001` | I.F Calculate performance metrics (P/E, dividend payout) | Application |
| `far-nfp-financial-position-0001` | I.B.1 Prepare an NFP statement of financial position | Application |
| `far-cash-flows-0006` | I.A.5 Derive the impact of transactions on the statement of cash flows | Analysis |
| `far-notes-0002` | I.A.7 Compare the notes with the statements to identify inconsistencies | Analysis |
| `far-consolidated-statements-0004` | I.A.6 Detect and correct discrepancies (NCI with upstream profit) | Analysis |
| `far-sec-forms-0002` | I.D Recall the purpose of Form 8-K | Remembering and Understanding |
| `far-income-statement-0003` | I.A.2 Detect and correct discrepancies (discontinued operations) | Analysis |
| `far-balance-sheet-0003` | I.A.1 Detect and correct discrepancies (equity section) | Analysis |
| `far-receivables-rollforward-0001` | II.B Prepare a rollforward of trade receivables | Analysis |
| `far-inventory-rollforward-0001` | II.C Prepare a rollforward of inventory | Analysis |
| `far-ppe-rollforward-0001` | II.D Prepare a rollforward of PP&E; gain or loss on disposal | Analysis |
| `far-exit-costs-0001` | II.G Exit or disposal liabilities: timing of recognition | Application |
| `far-asset-retirement-obligations-0001` | II.G Recall ARO recognition and measurement | Remembering and Understanding |
| `far-debt-modification-0001` | II.H.1 Modification versus extinguishment (10% test) | Application |
| `far-ppe-impairment-0002` | II.D Calculate impairment losses (asset group allocation) | Application |
| `far-intangibles-impairment-0001` | II.F Finite-lived intangibles: impairment | Application |
| `far-valuation-allowance-0001` | III.D Recall the criteria for a valuation allowance | Remembering and Understanding |
| `far-income-taxes-nol-0001` | III.D Calculate income tax expense (NOL carryforward) | Application |
| `far-fair-value-techniques-0001` | III.E Use valuation techniques and market participant assumptions | Application |
| `far-lessee-classification-0001` | III.F Identify the lease classification criteria | Application |
| `far-nfp-agent-transfers-0001` | III.C Identify transfers to an agent or intermediary that are not contributions | Application |
| `far-accounting-errors-0003` | III.A Derive the impact of an error correction | Analysis |
| `far-contingencies-0004` | III.B Review documentation for recognition versus disclosure | Analysis |
| `far-revenue-licenses-0001` | III.C Determine the amount and timing of revenue (licenses) | Application |

## Process

Same pipeline as batches 02 and 03, with the rules the batch 03 review added: every amount computed with `Decimal` and rounded half up; reconciliation and rollforward items built so the reconciling data changes the answer; company names and amounts checked against the bank before use.

## Tallies

| Measure | Batch 04 | Bank (100 FAR items) | Blueprint target |
| --- | --- | --- | --- |
| Area I / II / III | 9 / 8 / 8 (36% / 32% / 32%) | 35 / 34 / 31 | 30–40% / 30–40% / 25–35% |
| Remembering and Understanding | 3 (12%) | 10 (10%) | 5–15% |
| Application | 12 (48%) | 52 (52%) | 45–55% |
| Analysis | 10 (40%) | 38 (38%) | 35–45% |

## Blind verification

A separate agent solved all 25 items from the stems and choices only. It **matched the key on 25 of 25** and found no superseded rules. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-asset-retirement-obligations-0001` (required) | The key and one distractor differed only in the last clause, and the key was the longest choice | All four choices rewritten to similar length, differing in measurement and in accretion treatment |
| `far-lessee-classification-0001` (required) | Lease 2's economic life was missing, and residual value guarantees were not ruled out | Stem gives an 8-year economic life and says no lease has a residual value guarantee |
| `far-contingencies-0004` (required) | A guarantee issued "during the year" would be partly released by year-end; ASC 326 credit losses were not addressed | Guarantee issued December 31; expected credit losses stated to be immaterial |
| `far-debt-modification-0001` (required) | 9.3% came from no plausible error; decimals were inconsistent | Replaced with 13.98% (fee subtracted instead of added); all choices show two decimals |
| `far-cash-flows-0006` (required) | $50,000 needed two errors | Replaced with $3,000 (accrued wages deducted) |
| `far-ppe-impairment-0002` (required) | $66,667 came from no single error | Replaced with $120,000 (whole loss allocated to the machines) |
| `far-income-taxes-nol-0001` (required) | $100,000 used a rate that appears nowhere | Replaced with $16,800 (benefit only for the portion the 80% limit defers) |
| `far-ppe-rollforward-0001`, `far-fair-value-techniques-0001`, `far-income-statement-0003` | Weak distractors | Replaced with single-error figures ($70,000 loss; $416,990 annuity due; $210,000 pretax) |
| `far-exit-costs-0001` | A day count gives a slightly different figure | Stem says costs are recognized ratably by month |

**Scope note.** The verifier asked whether splitting a static-budget variance into flexible-budget and volume variances is BAR managerial content. `far-budget-variance-0001` stays in FAR: it maps to the FAR Area I.F task "Calculate variances between budget and actual results", and it asks only for the budget-versus-actual variance. The review gate is asked to confirm.

It read `far-cash-flows-0006` as Application; the tag stays Analysis because it maps to the FAR task "derive the impact of transactions on the statement of cash flows".

## Review gate

A fresh review agent graded the batch without reading this report first and read the skill marks from the PDF. **All 25 keys correct; average estimated pass likelihood 82.9%; 13 exam-ready, 11 minor, 1 major.** It confirmed that `far-budget-variance-0001` is FAR (Area I.F, marked Application) and that the rollforward tasks and "derive the impact of transactions on the statement of cash flows" are marked Analysis. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-consolidated-statements-0004` (major) | ASC 810-10-45-18 says the upstream profit elimination *may* be allocated to the noncontrolling interest, so full attribution to the parent made $37,000 defensible | Stem states that Pace attributes the elimination proportionately |
| `far-contingencies-0004` | "Reasonably possible" and "remote" are forbidden labels | Replaced with facts from counsel and the supplier's credit position |
| `far-income-statement-0003` | "A loss that is not in the draft" named the error | Clause removed |
| `far-balance-sheet-0003` | "Total equity" could be read as the parent's share only | Asks what the consolidated balance sheet should report |
| `far-receivables-rollforward-0001` | "Test reported credit sales" promised a figure that was not given | Now "determine credit sales" |
| `far-exit-costs-0001` | "Recognizes ratably by month" stated the answer as a policy | Replaced with a neutral whole-months convention |
| `far-asset-retirement-obligations-0001` | Key still the longest choice; two choices shared a first clause | Choices rebalanced; a second fair-value choice with a wrong measurement removes the pairing cue |
| `far-debt-modification-0001`, `far-lessee-classification-0001` | Their blueprint tasks are marked Remembering and Understanding | Retagged |
| `far-nfp-agent-transfers-0001` | The key equalled the $50,000 gift designated for Riverside | That gift is now $40,000 |
| `far-income-taxes-nol-0001` | Depends on current federal law but had no `review.asOf` | `asOf` added |

A blind check of the five changed items matched the key on all five with no required fixes.

**Tallies after the gate:** batch 04 is 5 / 10 / 10 (20% / 40% / 40%), so the batch alone is above the Remembering and Understanding range, but the 100-item FAR bank is 12 / 50 / 38, inside every range. Areas are unchanged (9 / 8 / 8; bank 35 / 34 / 31).

Gaps for batch 05 named by the reviewer: troubled debt restructurings, EBITDA and asset turnover, statement of comprehensive income recall, purchased software, impairment of investments at fair value, the equity method, fund determination, preparing the NFP statement of activities, and a stand-alone foreign-currency transaction item.
