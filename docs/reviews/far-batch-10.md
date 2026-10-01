# Review report: FAR batch 10

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**25 items**, all written from scratch in `scripts/batches/far-batch-10.py`. Each of the 18 numeric items ships with three variants (54 in all), so the batch adds 79 problems. Every variant family moves the key's letter.

## Plan

The batch takes the two FAR tasks that had no items (I.A.3a, I.F.a), a second item on four Remembering and Understanding tasks, a second item on nine Application tasks, and a further item on ten Analysis tasks, so it leans toward Areas I and II with Analysis at 40%. Only two items are in Area III, because the bank's Area III share is near its ceiling.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-comprehensive-income-0004` | I.A.3a Recall the purpose, objectives and structure of the statement of comprehensive income (one continuous statement or two consecutive statements; NCI attribution; tax presentation) | Remembering and Understanding |
| `far-ratios-0005` | I.F.a Identify the appropriate ratio or metric for an analysis (coverage of interest: times interest earned) | Remembering and Understanding |
| `far-governmental-measurement-focus-0002` | I.C.1a Recall government measurement focus and basis of accounting (general fund capital purchase is an expenditure) | Remembering and Understanding |
| `far-asset-retirement-obligations-0002` | II.G.a Recall asset retirement obligation recognition and measurement (upward revision discounted at the current credit-adjusted risk-free rate) | Remembering and Understanding |
| `far-valuation-allowance-0002` | III.D.b Recall valuation allowance criteria (more-likely-than-not threshold and measurement) | Remembering and Understanding |
| `far-subsequent-events-0009` | III.G.a Identify a subsequent event and recall its treatment (customer casualty after year-end is nonrecognized) | Remembering and Understanding |
| `far-consolidated-statements-0009` | I.A.6a Prepare consolidated financial statements (NCI in net income: upstream equipment gain and its realization, fair value amortization, downstream inventory profit and fees as decoys) | Application |
| `far-nfp-functional-expenses-0002` | I.B.2d Report NFP expenses by nature and function (fundraising: time-record allocations, grant writer, joint mailing that fails the audience criterion, unrecognized volunteer services) | Application |
| `far-nfp-cash-flows-0004` | I.B.3b Prepare an NFP statement of cash flows (net cash used in investing: restricted gift for equipment, donated shares sold at once, unrestricted investment income, donated land) | Application |
| `far-special-purpose-frameworks-0005` | I.E.b Convert cash basis statements to accrual basis (net income: receivables, accrued expenses, prepaid insurance, equipment and depreciation) | Application |
| `far-ratios-0006` | I.F.d Calculate solvency ratios (times interest earned with capitalized interest and cash interest paid) | Application |
| `far-ppe-involuntary-conversion-0001` | II.D.b Calculate gains or losses on disposals of long-lived assets (involuntary conversion: partial-year depreciation, deductible, reinvestment) | Application |
| `far-ppe-impairment-0003` | II.D.c Calculate impairment losses on long-lived assets (held and used: recoverability test, then fair value; costs to sell and value in use as distractors) | Application |
| `far-investments-htm-credit-loss-0002` | II.E.2c Calculate impairment losses on investments at amortized cost (CECL pool loss rate on HTM bonds, write-off net of settlement, rate-driven fair value decline; accrued interest elections stated) | Application |
| `far-exit-costs-0002` | II.G.c Calculate exit or disposal liabilities and their timing (termination benefits inside and beyond the minimum retention period, contract termination penalty, cease-use costs, relocation) | Application |
| `far-balance-sheet-0007` | I.A.1c Detect and correct balance sheet discrepancies (working capital: postdated checks, restricted construction cash, consigned-out goods, current installment) | Analysis |
| `far-income-statement-0006` | I.A.2d Detect and correct income statement discrepancies (draft built up line by line: customer deposit in sales, goods in transit left out of the count, prepaid insurance, equity securities gain as a decoy) | Analysis |
| `far-cash-flows-0012` | I.A.5d Derive the impact of transactions on the statement of cash flows (investing cash from equipment and accumulated depreciation balances, a seller-financed machine and a sale at a gain) | Analysis |
| `far-consolidated-statements-0010` | I.A.6c Detect and correct consolidated financial statement discrepancies (current liabilities: in-transit intercompany payable, uneliminated fees, NCI share of a subsidiary dividend payable) | Analysis |
| `far-notes-0007` | I.A.7b Compare the notes with the statements to identify inconsistencies (inventory including consigned-in goods; equity method, revenue and other liabilities notes consistent) | Analysis |
| `far-cash-unreconciled-0002` | II.A.c Investigate unreconciled cash balances to determine an adjustment (omitted outstanding check, misrecorded disbursement, prior-month deposit in transit) | Analysis |
| `far-receivables-rollforward-0004` | II.B.c Prepare a rollforward of trade receivables (ending balance: cash sales, recovery of a written-off account, noncash settlement, refund liability) | Analysis |
| `far-inventory-reconciliation-0004` | II.C.d Reconcile the inventory subledger to the general ledger (duplicate receiving posting, goods in a public warehouse, inbound freight split between units on hand and sold, unposted customer return) | Analysis |
| `far-ppe-reconciliation-0004` | II.D.g Reconcile the PP&E subledger to the general ledger (accumulated depreciation: sold machine left in subledger, fully depreciated press, change in useful life applied with a catch-up) | Analysis |
| `far-payables-reconciliation-0003` | II.G.d Reconcile the payables subledger to the general ledger (debit balances, checks held at year-end, net-method invoice posted gross, unposted debit memo) | Analysis |

- **Batch mix:** by skill, 6 / 9 / 10 (24% / 36% / 40%); by area, 13 / 10 / 2.
- **Variants:** 54 (18 numeric items × 3). Items plus variants: 79.
- **Coverage map:** all 25 ids are in `scripts/far-coverage.py`. 61 of 113 tasks now have two or more items (was 48), and 52 more items are needed (was 67). I.A.3a and I.F.a each have their first item.
- **Bank after batch 10:** 225 FAR MCQs (555 variants), 13.3% / 49.8% / 36.9% by skill and 37.3% / 35.6% / 27.1% by area, all in range.

### Version-0 key letters

- Numeric: six version-0 keys are on D (`nfp-functional-expenses-0002`, `nfp-cash-flows-0004`, `ratios-0006`, `income-statement-0006`, `receivables-rollforward-0004`, `payables-reconciliation-0003`), using items whose natural errors understate the key. In each, the variants bring in an overstating distractor, so the key moves off D. Three are on A (`cash-flows-0012`, `ppe-impairment-0003`, `cash-unreconciled-0002`).
- Word items (rotated by `finalize()`): `comprehensive-income-0004` A, `ratios-0005` B, `governmental-measurement-focus-0002` C, `asset-retirement-obligations-0002` D, `valuation-allowance-0002` A, `subsequent-events-0009` B, `notes-0007` C.
- Overall: A 5, B 7, C 6, D 7.
- Across all 79 versions: A 9, B 26, C 36, D 8 (the variants lean to B and C because each mixes overstating and understating distractors).

| Item | Key letters (version 0, variants 1–3) |
| --- | --- |
| `consolidated-statements-0009` | C B C A |
| `nfp-functional-expenses-0002` | D C C C |
| `nfp-cash-flows-0004` | D B C C |
| `special-purpose-frameworks-0005` | B A C C |
| `ratios-0006` | D C C C |
| `ppe-involuntary-conversion-0001` | B C B C |
| `ppe-impairment-0003` | A B C C |
| `investments-htm-credit-loss-0002` | B B A B |
| `exit-costs-0002` | B C A C |
| `balance-sheet-0007` | C B C B |
| `income-statement-0006` | D B C B |
| `cash-flows-0012` | A C B C |
| `consolidated-statements-0010` | C B B C |
| `cash-unreconciled-0002` | A B B B |
| `receivables-rollforward-0004` | D C B C |
| `inventory-reconciliation-0004` | C D C C |
| `ppe-reconciliation-0004` | B C B B |
| `payables-reconciliation-0003` | D C C C |

## Process

- Existing items on each task were read first, and each new item changes at least two component events against them. Examples: the consolidated-statements Application item uses an upstream equipment sale and NCI attribution (the existing one used inventory both ways in a wholly owned group); the NFP functional expense item asks for fundraising with joint costs and volunteers (the existing one asked for management and general with rent and investment fees); the HTM credit loss item uses a pooled loss rate, a write-off net of a settlement and a prior allowance (the existing one used a discounted-cash-flow measurement on a single bond); the exit-cost item adds contract termination, cease-use and relocation costs and an immediate-recognition group (the existing one tested ratable recognition only); the disposal item is an involuntary conversion (the existing one is a nonmonetary exchange).
- Where two items on a task already shared a stem template, the new item uses another format: the income statement item gives a draft built up line by line with supporting documents (the existing `income-statement-0001`/`-0002` list "you find (1)…(4)"); the balance sheet item asks for working capital from a staff computation (the existing items correct one section total); the cash-flow item derives investing cash from comparative balances (the existing items list transactions); the consolidated discrepancies item works from the staff's elimination entries; the notes item uses inventory, equity method, revenue and other-liability notes (the existing items used debt, revenue recognition, deferred taxes and dividends).
- Each numeric item is a builder with four parameter sets and a pool of four to six distractors, each from one named error; each version shows a different three. The script asserts that no distractor coincides with the key or another distractor and that amounts are positive (except the `$0` deferral distractor in the disposal item). A spacing check was run on every version; parameter sets were changed where two choices fell within a few hundred dollars of each other (the inventory return against freight on units sold, the payables discount against the key, two cash variants) and where the income statement corrections netted to zero.
- Every amount is computed with `Decimal` and rounded half up; the times-interest-earned builder refuses a half-cent ratio, and the impairment item's value-in-use figure is computed from the formula and rounded to the nearest $1,000.
- Standards points checked for currency: ASC 326-20 (HTM pooled CECL; the stem states the accrued-interest elections, that the bonds are unsecured, and that the entity is a PBE; the ASU 2025-05 expedient covers only current receivables and contract assets, so it doesn't apply); ASC 420 after ASC 842 (cease-use costs are for non-lease contracts only, so both contracts are stated as not leases); ASC 230-10-45-21A (donated securities sold nearly immediately are operating); ASU 2016-14 (analysis of expenses by nature and function); ASC 410-20 revisions; ASC 220-10-45 presentation after ASU 2011-05.
- Company names were checked against `content/` and `scripts/batches/`; 15 candidate names that already appeared were dropped before drafting.
- The script ran with no FAIL lines and no audit or lint warnings or notes, and `pnpm content:validate` (run as `tsx scripts/content.ts validate`) passed: 253 files valid.

## Blind verification

One verifier solved all 79 versions blind, and its answers matched the key on every one. Fixes applied:
- `subsequent-events-0009`: choice D (a tax examination of a prior year settled after year-end) was a second defensible "don't adjust" answer, because ASC 740-10-25-15 recognizes a change in an uncertain tax position in the period the change happens. It is replaced with a lawsuit over a Year 3 defect that is settled for more than the amount accrued, which is clearly a recognized event.
- `ppe-involuntary-conversion-0001`: in variant 3 the insurer paid in August, before a September 30 fire. In every version the payment is now in November and the replacement purchase in December. No amounts changed.
- `consolidated-statements-0009` (optional fix): the stem now says the noncontrolling interest was measured at fair value at acquisition. That supports the NCI bearing its share of the step-up amortization.

**Not changed:** the verifier noted that keys across all versions lean toward C (A 9, B 26, C 36, D 8). Version-0 keys are balanced (A 5, B 7, C 6, D 7), and each variant family moves its key letter. It also asked whether ratios belong in FAR; they do, because the 2026 FAR blueprint lists them as tasks I.F.a–f. It found no superseded rule in any stem or key, and no length or format cue.

## Review gate

_Placeholder for the lead: stratified sample, result and fixes._
