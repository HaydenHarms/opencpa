# Review report: FAR batch 03

**25 items**, all written from scratch (`scripts/batches/far-batch-03.py`).

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

## Plan

Batches 01 and 02 touch every FAR content group, most of them once. Batch 03 deepens the groups with a single item and the heavily tested ones, and targets a 3 / 12 / 10 skill mix so the bank comes back inside the blueprint ranges after batch 02 ended one Application item over.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-cash-flows-0005` | I.A.5 Detect, investigate and correct discrepancies (investing section) | Analysis |
| `far-eps-basic-0001` | I.D Calculate basic EPS | Application |
| `far-consolidated-statements-0003` | I.A.6 Detect, investigate and correct discrepancies (intercompany equipment sale) | Analysis |
| `far-nfp-functional-expenses-0001` | I.B.2 Report expenses by nature and function | Application |
| `far-balance-sheet-0002` | I.A.1 Detect, investigate and correct discrepancies (current assets) | Analysis |
| `far-income-statement-0002` | I.A.2 Detect, investigate and correct discrepancies (operating versus nonoperating) | Analysis |
| `far-ratios-0002` | I.F Calculate liquidity ratios (days in inventory) | Application |
| `far-governmental-measurement-focus-0001` | I.C.1 Recall measurement focus and basis of accounting | Remembering and Understanding |
| `far-special-purpose-frameworks-0002` | I.E Recall appropriate statement titles | Remembering and Understanding |
| `far-cash-bank-reconciliation-0002` | II.A Reconcile the bank balance and investigate unreconciled items | Analysis |
| `far-inventory-dollar-value-lifo-0001` | II.C Calculate inventory using costing methods | Application |
| `far-ppe-interest-capitalization-0001` | II.D Calculate gross PP&E | Application |
| `far-ppe-held-for-sale-0001` | II.D Adjust the carrying amount of assets held for sale | Application |
| `far-receivables-reconciliation-0001` | II.B Reconcile and investigate subledger and general ledger differences | Analysis |
| `far-accrued-liabilities-0001` | II.G Reconcile and investigate subledger and general ledger differences | Analysis |
| `far-bonds-premium-0001` | II.H.1 Calculate interest expense on bonds | Application |
| `far-stock-dividends-splits-0001` | II.I Equity transactions (stock dividends and splits) | Application |
| `far-accounting-errors-0002` | III.A Derive the impact of an error correction | Analysis |
| `far-contingencies-0003` | III.B Review documentation for recognition versus disclosure | Analysis |
| `far-subsequent-events-0003` | III.G Derive the impact of subsequent events | Analysis |
| `far-revenue-variable-consideration-0002` | III.C Determine the amount of revenue (variable consideration) | Application |
| `far-revenue-over-time-0001` | III.C Determine the amount and timing of revenue (over time) | Application |
| `far-nfp-contributed-services-0001` | III.C Contributed services | Application |
| `far-lessee-finance-0002` | III.F Calculate lessee liabilities (residual value guarantee) | Application |
| `far-fair-value-hierarchy-0001` | III.E Fair value hierarchy | Remembering and Understanding |

## Process

Same as batch 02: plan to the blueprint tasks, compute every number and distractor in code, give Analysis items the draft and supporting facts rather than the error, name elections by method, and spread key positions by choosing real errors on both sides of the key (A 7 / B 6 / C 7 / D 5).

## Tallies

| Measure | Batch 03 | Bank (75 FAR items) | Blueprint target |
| --- | --- | --- | --- |
| Area I / II / III | 9 / 8 / 8 (36% / 32% / 32%) | 26 / 26 / 23 (35% / 35% / 31%) | 30–40% / 30–40% / 25–35% |
| Remembering and Understanding | 3 (12%) | 7 (9%) | 5–15% |
| Application | 12 (48%) | 40 (53%) | 45–55% |
| Analysis | 10 (40%) | 28 (37%) | 35–45% |

## Blind verification

A separate agent solved all 25 items from the stems and choices only. It **matched the key on 25 of 25**, confirmed every topic is FAR, and found no reliance on superseded rules. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-stock-dividends-splits-0001` (required) | A 25% dividend sits on the "20 to 25 percent" boundary, so recording it at market value was defensible | The November dividend is now 50%; key and choices recomputed |
| `far-nfp-contributed-services-0001` (required) | The greeters' $30,000 equalled the correct total, so a wrong reason reached the key | Greeters' time is now valued at $25,000 |
| `far-ppe-held-for-sale-0001` (required) | The stem restated the held-for-sale criteria nearly word for word | Stem gives facts (board approval, dealer listing at a market price, buyer expected within six months) |
| `far-revenue-variable-consideration-0002` (required) | The $240,000 distractor had no real error behind it | Replaced with $180,000: the whole year's expected discount deducted from first-quarter sales |
| `far-balance-sheet-0002` | Splitting the two-year prepaid was a judgment call | Stem gives $10,000 per year |
| `far-cash-bank-reconciliation-0002` | Company name duplicated another item | Renamed to Dunmore Co. |

It read `far-contingencies-0003` as Application; the tag stays Analysis because the item maps to the blueprint's "review supporting documentation to determine whether a contingency requires recognition and/or disclosure" task, as `far-contingencies-0002` did in batch 01.

## Review gate

A fresh review agent graded the batch without reading this report first. **All 25 keys correct; average estimated pass likelihood 84.3%; 23 exam-ready, 2 minor revision, 0 major.** Skill and area mix confirmed inside the blueprint ranges for the batch and the 75-item bank. Its tool checks were interrupted partway (a service outage), so it could not read the skill marks for lessee accounting and subsequent events or check standards online; those points rest on its own knowledge. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-receivables-reconciliation-0001` | The reconciling item did not change the key, so the reconciliation was decorative; it also reused batch 02's "$7,000 credit memo on December 30" | The reconciling item is now a $9,000 sale missing from the subledger, which changes the debit-balance total; the hint "(overpayments and advance deposits)" is gone |
| `far-bonds-premium-0001` | Choice C showed $68,926 for $68,926.50, a round-half-to-even artifact | Now $68,927 |
| `far-ratios-0002` | One distractor needed two errors at once | Replaced with the common single error (ending inventory, 55.0 days) |
| `far-eps-basic-0001` | One distractor was a sign slip | Replaced with not applying the stock dividend retroactively ($3.77) |

Quality-bar additions from this review are in `CLAUDE.md`: a reconciliation item's reconciling entries must change the key, amounts round half up, and new items are checked against the bank for reused amounts and phrasing.
