# Review report: FAR batch 02

**25 items**, all written from scratch (`scripts/batches/far-batch-02.py`). The legacy bank is thin on these topics, so none was adapted from it.

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026. Each item was matched to a representative task in the FAR blueprint before it was written.

## Plan

Batch 01 left these FAR groups with no items: balance sheet classification, the income statement, the statement of changes in equity, notes, SEC forms, special purpose frameworks, ratios, the NFP statement of cash flows, intercompany eliminations, cash and cash equivalents, receivable transfers, inventory and payables reconciliations, held-to-maturity investments, finite-lived intangibles (beyond cloud computing), debt covenants, treasury stock, changes in principle and estimate, principal versus agent, contract costs, lessee operating leases, uncertain tax positions, and subsequent-event calculations. Batch 02 covers every one of them, and aims Analysis at about 40% to pull the bank toward the middle of the 35–45% range.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-balance-sheet-0001` | I.A.1 Detect, investigate and correct discrepancies (classified balance sheet) | Analysis |
| `far-income-statement-0001` | I.A.2 Detect, investigate and correct discrepancies (discontinued operations, FX transaction loss, no extraordinary items) | Analysis |
| `far-changes-in-equity-0001` | I.A.4 Detect, investigate and correct discrepancies (stock dividend, treasury stock, prior-period adjustment) | Analysis |
| `far-notes-0001` | I.A.7 Compare the notes to the statements to identify inconsistencies | Analysis |
| `far-sec-forms-0001` | I.D Identify the items of Form 10-K (Part II, Items 7, 7A, 8) | Remembering and Understanding |
| `far-special-purpose-frameworks-0001` | I.E Convert cash basis to accrual basis | Application |
| `far-ratios-0001` | I.F Calculate liquidity ratios | Application |
| `far-nfp-cash-flows-0001` | I.B.3 Prepare an NFP statement of cash flows | Application |
| `far-consolidated-statements-0002` | I.A.6 Detect, investigate and correct discrepancies (intercompany profit) | Analysis |
| `far-cash-bank-reconciliation-0001` | II.A Reconcile the bank balance to the general ledger | Analysis |
| `far-cash-equivalents-0001` | II.A Calculate cash and cash equivalents | Application |
| `far-receivables-factoring-0001` | II.B Record a transfer of receivables (factoring) | Application |
| `far-inventory-reconciliation-0001` | II.C Reconcile and investigate subledger and general ledger differences | Analysis |
| `far-investments-htm-0001` | II.E.2 Calculate the carrying amount of investments at amortized cost | Application |
| `far-intangibles-patent-0001` | II.F Calculate the carrying amount of finite-lived intangibles | Application |
| `far-payables-reconciliation-0001` | II.G Reconcile and investigate subledger and general ledger differences | Analysis |
| `far-debt-covenant-0001` | II.H.2 Perform debt covenant calculations | Application |
| `far-treasury-stock-0001` | II.I Journal entries for treasury stock | Application |
| `far-change-in-principle-0001` | III.A Derive the impact of an accounting change | Analysis |
| `far-change-in-estimate-0001` | III.A Calculate the adjustment for a change in estimate | Application |
| `far-revenue-principal-agent-0001` | III.C Determine the amount of revenue (principal versus agent) | Application |
| `far-revenue-contract-costs-0001` | III.C Contract costs | Application |
| `far-lessee-operating-0003` | III.F Classify a lease and calculate lessee lease cost | Application |
| `far-uncertain-tax-positions-0001` | III.D Recall the treatment of uncertain tax positions | Remembering and Understanding |
| `far-subsequent-events-0002` | III.G Derive the impact of subsequent events on the statements and notes | Analysis |

## Process

1. **Plan coverage first** (table above), then write each item to one task.
2. **Compute every number in code**, including each distractor, and name the error that produces it.
3. **Analysis items give the draft and the supporting facts, not the error.** The student has to find what is wrong.
4. **Key positions.** Numeric choices are ascending, so the first draft had 13 of 25 keys in B. Several distractors were swapped for equally real errors on the other side of the key, giving A 6 / B 5 / C 7 / D 7.
5. **Blind verification and the review gate** (below).

## Tallies

| Measure | Batch 02 | Bank (batches 01 + 02, 50 items) | Blueprint target |
| --- | --- | --- | --- |
| Area I / II / III | 9 / 9 / 7 (36% / 36% / 28%) | 17 / 18 / 15 (34% / 36% / 30%) | 30–40% / 30–40% / 25–35% |
| Remembering and Understanding | 2 (8%) | 4 (8%) | 5–15% |
| Application | 13 (52%) | 27 (54%) | 45–55% |
| Analysis | 10 (40%) | 19 (38%) | 35–45% |

## Blind verification

A separate agent solved all 25 items from the stems and choices only. It **matched the key on 25 of 25**, confirmed every topic is FAR under the 2026 blueprint, found no reliance on superseded rules, and traced every numeric distractor to a named error. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-revenue-contract-costs-0001` (required) | The key needs the $6,000 legal fee to be non-incremental, but the stem did not say so | Stem says the fee is owed whether or not the customer signs |
| `far-investments-htm-0001` | An ASC 326 allowance question could arise | Stem says Nolan expects no credit losses |
| `far-income-statement-0001` | "Major geographic area" is ASC 205-20 wording | Stem gives facts instead (only operation on the continent, 30% of revenue) |
| `far-treasury-stock-0001` | ASC 505-30 says losses "may" be charged to same-class paid-in capital, leaving a thin case for $6,000 | Stem names Sutton's election (paid-in capital to the maximum extent permitted) |

It rated `far-debt-covenant-0001` as Application (as tagged) and `far-cash-equivalents-0001` as borderline Remembering and Understanding; tags unchanged.
