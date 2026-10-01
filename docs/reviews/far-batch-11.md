# Review report: FAR batch 11

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**25 items**, all written from scratch in `scripts/batches/far-batch-11.py`. Each of the 19 numeric items ships with three variants (57 in all), so the batch adds 82 problems. Every variant family moves the key's letter.

## Plan

The batch takes a second item on six Area III Remembering and Understanding tasks, a second item on nine Application tasks in Areas I and II, and a further item on ten Analysis tasks, each Analysis item in a format its task's existing items don't use. Area III gets eight items, to bring the bank's Area III share back up from 27.1%.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-contingencies-0011` | III.B.a Recall recognition and disclosure criteria for commitments and contingencies (gain contingency: a jury award under appeal is disclosed, not recognized) | Remembering and Understanding |
| `far-revenue-five-step-0002` | III.C.a Recall five-step model concepts (step 1: collectibility; oral contracts, variable consideration and timing as distractors) | Remembering and Understanding |
| `far-nfp-promises-to-give-0002` | III.C.b Recall recognition of NFP conditional and unconditional promises to give (all-or-nothing matching barrier with release; not recognized, disclosed) | Remembering and Understanding |
| `far-uncertain-tax-positions-0002` | III.D.a Recall accounting for uncertain tax positions (new information after the reporting date is recognized in the later period, not as an adjusting subsequent event) | Remembering and Understanding |
| `far-lessee-residual-value-0001` | III.F.a Recall lessee treatment of residual value guarantees, purchase options and variable payments (amount probable of being owed under a guarantee; option not reasonably certain) | Remembering and Understanding |
| `far-lessee-classification-0002` | III.F.b Identify lease classification criteria (four leases described by facts: bargain purchase option, commencement near the end of economic life, thresholds missed) | Remembering and Understanding |
| `far-balance-sheet-0008` | I.A.1a Prepare a classified balance sheet (total current liabilities: customer credit balances, stock dividend distributable, current portions of lease and warranty liabilities, deferred tax liability) | Application |
| `far-income-statement-0007` | I.A.2a Prepare a single-step or multi-step income statement (income from operations: impairment loss and gain on sale included, interest, dividends and discontinued operations excluded) | Application |
| `far-cash-flows-0013` | I.A.5a Prepare a statement of cash flows and required disclosures (income taxes paid: deferred taxes, tax charged to OCI, deferred tax asset) | Application |
| `far-nfp-financial-position-0004` | I.B.1b Prepare an NFP statement of financial position (net assets without donor restrictions: underwater endowment, board designation, refundable advance) | Application |
| `far-nfp-statement-of-activities-0003` | I.B.2b Prepare an NFP statement of activities (net change in net assets with donor restrictions: releases, placed-in-service equipment, endowment return and appropriation, implied time restriction, conditional pledge) | Application |
| `far-receivables-credit-losses-0003` | II.B.a Calculate trade receivables and allowances (CECL aging, write-offs and a recovery; ASU 2025-05 practical expedient elected, so the recession forecast is excluded) | Application |
| `far-ppe-lump-sum-0001` | II.D.a Calculate gross and net PP&E (lump-sum purchase allocated on appraised values, acquisition costs, renovation before use, partial-year depreciation) | Application |
| `far-investments-htm-0002` | II.E.2b Calculate the carrying amount of investments at amortized cost (held-to-maturity bonds bought at a premium, semiannual effective interest) | Application |
| `far-accrued-liabilities-0002` | II.G.b Calculate payables and accrued liabilities (sales tax included in receipts, payroll withholdings and employer taxes, vested vacation, accrued interest) | Application |
| `far-changes-in-equity-0006` | I.A.4c Detect and correct statement of changes in equity discrepancies (AOCI column: equity securities gain, AFS credit loss, missing reclassification adjustment) | Analysis |
| `far-cash-flows-0014` | I.A.5c Detect and correct statement of cash flows discrepancies (full draft statement, financing section: assumed mortgage, prepayment penalty, finance lease interest) | Analysis |
| `far-cash-flows-0015` | I.A.5d Derive the impact of transactions on the statement of cash flows (direct method cash paid to suppliers: write-down inside cost of goods sold, payable settled by a note) | Analysis |
| `far-cash-bank-reconciliation-0005` | II.A.b Reconcile the bank balance to the general ledger (outstanding checks found by matching the check register to cleared checks; prior-month items; bank error; transposed disbursement) | Analysis |
| `far-cash-unreconciled-0003` | II.A.c Investigate unreconciled cash balances to determine an adjustment (difference plugged to expense; check entered as a receipt, misrecorded deposit, omitted outstanding check, automatic loan payment) | Analysis |
| `far-receivables-reconciliation-0004` | II.B.d Reconcile the receivables subledger to the general ledger (net adjustment to the control account: NSF charge-back, discounts, note conversion, subledger posting error) | Analysis |
| `far-inventory-rollforward-0004` | II.C.c Prepare a rollforward of inventory (perpetual shrinkage after cutoff: FOB destination purchase, FOB destination sale that cancels out, consigned-out goods) | Analysis |
| `far-ppe-rollforward-0004` | II.D.f Prepare a rollforward of PP&E (draft rollforward at cost: capitalized repairs, expensed sales tax and installation, disposal at carrying amount, unrecorded scrapping) | Analysis |
| `far-accounting-errors-0007` | III.A.b Derive the impact of an accounting change or error correction (restated prior-year net income in comparative statements: customer deposit, prior-year interest, prepaid rent; warranty estimate revision as a decoy) | Analysis |
| `far-subsequent-events-0010` | III.G.c Derive the impact of identified subsequent events (total liabilities: settlement below the accrual, warranty defect in goods sold before year-end; new injury, dividend and loan as nonrecognized) | Analysis |

- **Batch mix:** by skill, 6 / 9 / 10 (24% / 36% / 40%); by area, 8 / 9 / 8.
- **Variants:** 57 (19 numeric items × 3). Items plus variants: 82.
- **Coverage map:** all 25 ids are in `scripts/far-coverage.py`. 15 more tasks reach two items (III.B.a, III.C.a, III.C.b, III.D.a, III.F.a, III.F.b, I.A.1a, I.A.2a, I.A.5a, I.B.1b, I.B.2b, II.B.a, II.D.a, II.E.2b, II.G.b), so 76 of 113 tasks have two or more and 37 more items are needed.
- **Retagged older items (lead).** A bank-wide check of skill tags against each mapped task's blueprint mark found three mismatches, now fixed in the YAML and in the source scripts: `accrued-liabilities-0001` (II.G.b) and `receivables-credit-losses-0002` (II.B.a) go from Analysis to Application, because their stems name the items to fix; `nfp-agent-transfers-0001` (III.C.c) goes from Application to Remembering and Understanding, because the task is marked R&U even though the item computes an amount.
- **Bank after batch 11:** 250 FAR MCQs (612 variants), 14.8% / 48.8% / 36.4% by skill and 36.8% / 35.6% / 27.6% by area, all in range. Remembering and Understanding is near its 15% ceiling, so the next batches add none.
- **Bank after batch 11:** 250 FAR MCQs (612 variants), 14.4% / 48.4% / 37.2% by skill and 36.8% / 35.6% / 27.6% by area, all in range. Remembering and Understanding is near its 15% ceiling.

### Version-0 key letters

- Numeric: six version-0 keys are on D (`balance-sheet-0008`, `income-statement-0007`, `nfp-statement-of-activities-0003`, `cash-flows-0015`, `accrued-liabilities-0002`, `cash-bank-reconciliation-0005`) and four on A (`receivables-credit-losses-0003`, `investments-htm-0002`, `receivables-reconciliation-0004`, `ppe-rollforward-0004`). In each, the variants bring in a distractor on the other side of the key, so the letter moves.
- Word items (rotated by `finalize()`): `contingencies-0011` A, `revenue-five-step-0002` B, `nfp-promises-to-give-0002` C, `uncertain-tax-positions-0002` D, `lessee-residual-value-0001` A, `lessee-classification-0002` B.
- Overall: A 6, B 7, C 7, D 5 (after the gate fixes; A 6, B 6, C 6, D 7 as built).
- Across all 82 versions: A 20, B 30, C 20, D 12 (after the blind-verifier fixes). Nine families have only one natural error on the low side of the key (for example, a forgotten NSF charge-back is the only error that lowers the receivables adjustment), so their versions alternate between A and B; the D keys come from the families with three or more low-side errors.

| Item | Key letters (version 0, variants 1–3) |
| --- | --- |
| `balance-sheet-0008` | D A C B |
| `income-statement-0007` | D B C C |
| `cash-flows-0013` | C A B C |
| `nfp-financial-position-0004` | C B C B |
| `nfp-statement-of-activities-0003` | D A C B |
| `changes-in-equity-0006` | B A B A |
| `cash-flows-0014` | B A B B |
| `cash-flows-0015` | C C B C |
| `receivables-credit-losses-0003` | A B B B |
| `ppe-lump-sum-0001` | C D C D |
| `investments-htm-0002` | A C B A |
| `accrued-liabilities-0002` | C A D D |
| `cash-bank-reconciliation-0005` | D A C C |
| `cash-unreconciled-0003` | B A C A |
| `receivables-reconciliation-0004` | A B B B |
| `inventory-rollforward-0004` | B A B B |
| `ppe-rollforward-0004` | A B B B |
| `accounting-errors-0007` | C D B C |
| `subsequent-events-0010` | B A B A |

## Process

- Existing items on each task were read first. Each new item changes at least two component events against them, and where two items on a task already shared a template, the new item uses another format:
  - I.A.4c: the existing items correct retained earnings, APIC or total equity; the new item corrects the AOCI column.
  - I.A.5c: three existing items give a draft operating section and one an investing section; the new item gives the whole draft statement and asks for financing, with errors that cross sections (a penalty left in operating, lease interest in financing) and a noncash mortgage.
  - I.A.5d: the existing items list financing, operating or investing transactions or derive investing cash from balances; the new item derives direct-method cash paid to suppliers, where the inventory write-down cancels out.
  - II.A.b: the existing items give deposit-in-transit and outstanding-check totals (or a proof of cash); the new item makes the student find the outstanding checks by matching the check register against the checks paid, including one carried from November.
  - II.A.c: the existing items describe an attempted reconciliation and ask for the adjustment or the balance; the new item starts from a difference plugged to miscellaneous expense.
  - II.B.d: all three existing items ask for receivables to report; the new item asks for the net adjustment to the control account, so the student must decide which record each error is in.
  - II.C.c: the existing items ask for periodic cost of goods sold (two) or perpetual shrinkage without cutoff; the new item is perpetual shrinkage with cutoff errors on both sides of the count.
  - II.D.f: the existing items derive one missing figure (gain, purchases, depreciation) from a rollforward; the new item corrects a draft rollforward of cost.
  - III.A.b: the existing items ask for retained earnings or the effects of one or two errors; the new item asks for restated prior-year net income in comparative statements, with a change in estimate as a decoy.
  - III.G.c: the existing items ask for pretax income, EPS, a current ratio or an allowance; the new item asks for total liabilities, and (per the batch 10 gate) its nonrecognized events are a new injury, a dividend and a loan, not a casualty.
  - The Application and recall items also avoid the existing items' templates: current liabilities rather than working capital (I.A.1a), income from operations rather than income from continuing operations (I.A.2a), income taxes paid rather than interest paid (I.A.5a), net assets without donor restrictions and the change in net assets with donor restrictions rather than the reverse (I.B.1b, I.B.2b), a lump-sum purchase rather than interest capitalization (II.D.a), a premium bond with semiannual interest rather than a discount bond with annual interest (II.E.2b), a gain contingency rather than remote-loss disclosures (III.B.a), step 1 rather than step 2 of the revenue model (III.C.a), and a residual value guarantee rather than variable payments (III.F.a).
- Each numeric item is a builder with four parameter sets and a pool of four to seven distractors, each from one named error; each version shows a different three. The script asserts that no distractor coincides with the key or another distractor and that every amount is positive. It also prints every dollar amount that appears more than once in a stem, and every choice equal to a stem amount; each line was checked. The repeats left are the same fact named twice (the assumed mortgage and the term-loan principal in `cash-flows-0014`, the bookkeeper's adjusted balance in `cash-unreconciled-0003`), and the choices equal to a stem amount are distractors for the error of using that figure (the bonds' fair value or cost in `investments-htm-0002`, the draft AOCI in `changes-in-equity-0006`, the unadjusted plugged balance, and the note amount as the "forgot the NSF check" adjustment). A spacing check was run on every version; parameter sets were changed where two choices fell within a few hundred dollars (the transposed check and deposit amounts in the cash items, the deferred tax asset changes, a lawsuit estimate).
- Every amount is computed with `Decimal` and rounded half up; the held-to-maturity schedule and the lump-sum allocation round at each step.
- Standards points checked for currency: ASU 2025-05 (the practical expedient assumes conditions at the balance sheet date persist and drops the forecast; effective for fiscal years beginning after December 15, 2025, early adoption permitted; the stem says the public business entity has adopted it and elects the expedient, and the receivables are due within 60 days); ASU 2016-13 for available-for-sale debt securities (credit loss through an allowance and net income, the rest of the decline in OCI); ASU 2016-14 (underwater endowments stay in net assets with donor restrictions; no implied time restriction on long-lived assets after they are placed in service); ASU 2018-08 (barrier plus release makes a promise conditional; the stem says the match is uncertain so the old "remote" exception can't apply); ASU 2016-15 (debt prepayment costs are financing outflows); ASC 842 (finance lease interest is operating; lessee residual value guarantees enter the lease liability at the amount probable of being owed; the "at or near the end of economic life" exception); ASC 360-10-45-4 and 45-5 (impairment losses and gains on sales go in income from operations when that subtotal is presented); ASC 740-10 (a change in judgment on a tax position from information after the reporting date is recognized in the later period, the batch 10 verifier's point, used here as the tested rule).
- Lessons from the batch 10 gate applied: one fact per amount within a version (checked by the script, above); each distractor rationale states exactly the computation behind its number; each reconciling item says which record it is in; no casualty in the subsequent-events item; topic numbers in citations rechecked (paragraph cites kept only where certain, otherwise the Subtopic).
- Company names were checked against `content/` and `scripts/batches/`; three names used twice inside the batch were replaced.
- The script ran with no FAIL lines and no audit or lint warnings or notes, and `npx tsx scripts/content.ts validate` passed: 278 files valid.

## Blind verification

One verifier solved all 82 versions blind, and its answers matched the key on every one. Fixes applied:
- `accrued-liabilities-0002` (required): the question asked for the "total liability for these items", and the note principal was one of the items, so the strict answer wasn't a choice. The stem now says the principal is reported separately as a note payable, and asks for the other liabilities. In variant 3, receipts of $354,000 gave a non-round sales tax; they are now $349,800 (tax $19,800, key $78,362). A builder check requires the sales-tax split to be exact.
- `income-statement-0007`: the key puts the gain on the equipment sale and the impairment loss inside income from operations. That is what ASC 360-10-45-4 and 45-5 require when the subtotal is presented, but it differs from the textbook "other gains" layout. The references, the key's rationale and the "gain left out" rationale now cite those paragraphs.
- `ppe-lump-sum-0001`: variant 2 rounded an intermediate allocation, so one distractor was a dollar off. Allocations are now exact by construction, with an assert to enforce it. Depreciation is rounded once, and the stem says so. Variant 2 now has a distractor above the key, so its key moves from D to C.
- `nfp-statement-of-activities-0003`: in versions 0 and 2, choice A came from a contradictory pair of errors. It now carries one coherent error: the endowment return is reported without donor restrictions, so no release is recorded for the appropriation either.
- `ppe-rollforward-0004`: the "removed twice" distractor in variants 1 and 3 is replaced by "disposal recorded at sale price", which lies above the key, so both keys move from C to B.

**Kept:** the verifier asked whether uncertain tax positions belong in FAR. They do: the 2026 FAR blueprint lists them as task III.D.a.

**Blind re-check after the fixes:** a fresh verifier re-solved all 20 versions of the five changed items. It matched every key and traced every distractor to a single error. It read "rounding it to the nearest dollar" in `ppe-lump-sum-0001` as rounding each month's depreciation, which gives a figure that isn't a choice in versions 0 and 3. The stem now says "rounding Year 1 depreciation to the nearest dollar", which is how the key is computed; no amounts changed. **Open for the gate:** in `accrued-liabilities-0002` the key is the largest choice in three of four versions, because "include every item" is the largest total.

## Review gate

**Stratified gate** (tactic 4): 21 of 25 items. Nineteen were reviewed in full: the 10 Analysis items; the two items on new templates (`lessee-residual-value-0001`, `ppe-lump-sum-0001`); the items on recently changed standards (`receivables-credit-losses-0003` for ASU 2016-13 and 2025-05, `nfp-promises-to-give-0002` for ASU 2018-08, `nfp-financial-position-0004` and `nfp-statement-of-activities-0003` for ASU 2016-14, and `lessee-classification-0002` for ASU 2016-02); and the two items changed after blind verification (`accrued-liabilities-0002`, `income-statement-0007`). Two were drawn at random from the other six (seed 20261003): `cash-flows-0013` and `contingencies-0011`. Not gated: `revenue-five-step-0002`, `uncertain-tax-positions-0002`, `balance-sheet-0008`, `investments-htm-0002`.

**Result: passed.** The 21 gated items average **84.2%** estimated pass likelihood (batch 10: 84.6%). 19 are exam-ready, 2 need minor revision and none need major revision. Every key is correct in all the versions the gate solved. Both sampled items were exam-ready, so escalation was not triggered. The gate checked ASU 2025-05 against the FASB text: stating that the entity is a public business entity correctly rules out the additional election that is available only to entities other than PBEs.

| Item | Gate | Fix |
| --- | --- | --- |
| `far-cash-flows-0015` (78%) | Version 0 had no distractor for the item's main twist: payables settled by issuing a note, treated as paid in cash. Only variants 1 and 2 had one. | Version 0 swaps "inventory change ignored" ($2,718,000) for "note settlement treated as cash" ($2,869,000). Choices are $2,652,000 / $2,738,000 / **$2,784,000** / $2,869,000, so the key moves from D to C. |
| `far-subsequent-events-0010` (80%) | Version 0's distractors tested only the recognized events, and A ($3,292,000) was weak. | Version 0 swaps "suit removed altogether" for "February dividend accrued" ($3,627,000). Choices are $3,405,000 / **$3,477,000** / $3,532,000 / $3,627,000, so the key moves from C to B. |
| Optional, applied | `accrued-liabilities-0002` version 0 lacked the classic error of computing sales tax on gross receipts; `receivables-reconciliation-0004` said "a suspense expense account"; `nfp-promises-to-give-0002` cited 958-605-50 for the conditional-promise disclosure. | Version 0 swaps "vacation left out" for "tax at 7% of gross receipts" ($150,798), so the key moves from D to C, between two distractors. The receivables item now reads "debiting miscellaneous expense". The NFP reference is now Subtopic ASC 958-310-50. |

**Not changed:** the gate called `cash-flows-0015`'s Analysis tag borderline but accepted it under I.A.5d ("derive the impact of transactions on the statement of cash flows"), which the blueprint marks Analysis.

**Gate suggestion for the pipeline** (open): version 0 must include a distractor for the item's central twist, not only the variants; a builder can enforce this by requiring that error in parameter set 0's `use`.

**Blind re-check after the gate fixes:** a fresh verifier re-solved version 0 of the three items whose distractors changed and all four versions of `receivables-reconciliation-0004` (7 versions). It matched every key and traced every distractor to a single error, with no required fixes.
