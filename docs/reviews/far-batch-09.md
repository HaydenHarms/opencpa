# Review report: FAR batch 09

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**25 items**, all written from scratch in `scripts/batches/far-batch-09.py`. Each of the 21 numeric items ships with three variants (63 in all), so the batch adds 88 problems. Every variant family moves the key's letter.

## Plan

The batch takes the three FAR tasks that had no items (II.E.1a, II.E.3a, II.F.a), the Area I "adjust ... to correct identified errors" tasks, and a further item on each Area I and Area II Analysis task, so the batch leans toward Areas I and II with Analysis at 40%. There are no Area III items, because the bank's Area III share is near its ceiling.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-investments-fair-value-0003` | II.E.1a Identify investments eligible or required to be reported at fair value (fair value option scope: a consolidated subsidiary is excluded) | Remembering and Understanding |
| `far-equity-method-0003` | II.E.3a Identify when the equity method applies (presumptions overcome both ways; control) | Remembering and Understanding |
| `far-intangibles-classification-0001` | II.F.a Identify recognition criteria and classify intangibles as finite- or indefinite-lived (renewable license; internally built brand not recognized) | Remembering and Understanding |
| `far-balance-sheet-0006` | I.A.1b Adjust the balance sheet to correct identified errors (total assets: prepaid insurance, depreciation, credit balances, unrecorded dividend, accrued interest) | Application |
| `far-income-statement-0005` | I.A.2b Adjust the income statement to correct identified errors (expensed equipment, warranty accrual, loss charged to retained earnings, FOB destination sale) | Application |
| `far-changes-in-equity-0004` | I.A.4b Adjust the statement of changes in equity to correct identified errors (APIC: issuance excess, treasury reissue gain and shortfall, large stock dividend) | Application |
| `far-cash-flows-0010` | I.A.5b Adjust a statement of cash flows to correct identified errors (financing section: dividends declared vs paid, interest, conversion, treasury shares) | Application |
| `far-notes-0005` | I.A.7a Adjust the notes to correct identified errors and omissions (debt maturities for next year) | Application |
| `far-nfp-statement-of-activities-0002` | I.B.2c Adjust an NFP statement of activities to correct identified errors (endowment return, missing release, gala gross vs net, unrealized loss) | Application |
| `far-special-purpose-frameworks-0004` | I.E.d Prepare income tax basis statements (net income from GAAP: depreciation, advance rent, warranties, bad debts) | Application |
| `far-ppe-held-for-sale-0002` | II.D.d Determine whether an asset qualifies as held for sale (five assets; total carrying amount classified) | Application |
| `far-foreign-currency-transactions-0002` | I.A.2c Calculate foreign-currency transaction gains or losses (receivable remeasured, payable settled, nonmonetary advance) | Application |
| `far-receivables-factoring-0002` | II.B.b Record transfers of trade receivables (sale with recourse; recourse obligation at fair value; holdback) | Application |
| `far-inventory-lcm-0001` | II.C.b Apply lower of cost or market (LIFO; ceiling, floor and replacement cost cases) | Application |
| `far-debt-noninterest-note-0001` | II.H.1c Calculate interest expense on notes and bonds (noninterest-bearing note, imputed rate, interest across note years) | Application |
| `far-changes-in-equity-0005` | I.A.4c Detect and correct statement of changes in equity discrepancies (total equity: OCI double count, property dividend, treasury retirement, conversion) | Analysis |
| `far-cash-flows-0011` | I.A.5c Detect and correct statement of cash flows discrepancies (operating section: premium amortization, prepaid sign, dividends payable, equity method income) | Analysis |
| `far-notes-0006` | I.A.7b Compare the notes with the statements to identify inconsistencies (property, leases, debt, dividends declared) | Analysis |
| `far-cash-bank-reconciliation-0004` | II.A.b Reconcile the bank balance to the general ledger (certified check, unmailed check, loan payment, dividend received) | Analysis |
| `far-receivables-rollforward-0003` | II.B.c Prepare a rollforward of trade receivables (collections: cash sales, returns, discounts, write-offs, note conversion) | Analysis |
| `far-receivables-reconciliation-0003` | II.B.d Reconcile the receivables subledger to the general ledger (duplicated memo, underfooting, unposted write-off, misposted payment) | Analysis |
| `far-inventory-rollforward-0003` | II.C.c Prepare a rollforward of inventory (cost of goods sold: consigned-in goods, fire loss, freight-out, discounts) | Analysis |
| `far-inventory-reconciliation-0003` | II.C.d Reconcile the inventory subledger to the general ledger (pricing error, write-down, shipment cutoff, consigned-in goods) | Analysis |
| `far-ppe-rollforward-0003` | II.D.f Prepare a rollforward of PP&E (depreciation expense from accumulated depreciation with a sale and a retirement) | Analysis |
| `far-ppe-reconciliation-0003` | II.D.g Reconcile the PP&E subledger to the general ledger (net carrying amount: excess depreciation, land in equipment, capitalized repairs) | Analysis |

- **Batch mix:** by skill, 3 / 12 / 10 (12% / 48% / 40%); by area, 11 / 14 / 0.
- **Variants:** 63 (21 numeric items × 3). Items plus variants: 88.
- **New ids are not yet in `scripts/far-coverage.py`**; the lead adds them (the builder did not edit the map).

### Version-0 key letters

- Numeric: after the verifier round, none of the 21 version-0 keys is on A or D. As the coordinator asked, every version 0 whose distractors all erred in the same direction now has a distractor on the other side of the key, which puts that key on B or C.
- Word items (rotated by `finalize()`): `investments-fair-value-0003` A, `equity-method-0003` B, `intangibles-classification-0001` C, `notes-0006` D.
- Overall: A 1, B 11, C 12, D 1.

| Item | Key letters (version 0, variants 1–3) |
| --- | --- |
| `balance-sheet-0006` | C B C C |
| `income-statement-0005` | B C B C |
| `changes-in-equity-0004` | B B C C |
| `cash-flows-0010` | C B C C |
| `notes-0005` | B C C B |
| `nfp-statement-of-activities-0002` | C C B B |
| `special-purpose-frameworks-0004` | C C C D |
| `foreign-currency-transactions-0002` | B A B A |
| `changes-in-equity-0005` | B C C B |
| `cash-flows-0011` | B C B B |
| `ppe-held-for-sale-0002` | B A B B |
| `receivables-factoring-0002` | C B B C |
| `inventory-lcm-0001` | C B C B |
| `debt-noninterest-note-0001` | C B B C |
| `cash-bank-reconciliation-0004` | C C C D |
| `receivables-rollforward-0003` | B B B A |
| `receivables-reconciliation-0003` | C B B B |
| `inventory-rollforward-0003` | B B C A |
| `inventory-reconciliation-0003` | B C B B |
| `ppe-rollforward-0003` | C C C D |
| `ppe-reconciliation-0003` | C B C B |

## Process

- Existing items on each task were read first, and each new item changes at least two component events against them: for example, the receivables reconciliation uses a duplicated credit memo, an underfooted receipts column, an unposted write-off and a misposted payment (the earlier items used unposted sales, a posting error, a credit memo to the control account and a consignment invoice); the bank reconciliation uses a certified check, an unmailed check, a loan payment and a wired dividend.
- Each numeric item is a builder with four parameter sets and a pool of four or five distractors, each from one named error; each version shows a different three. The script asserts that no distractor coincides with the key or another distractor, and the self-check removed coincidences between stem quantities (for example, expired insurance equal to the credit balances, dividends paid equal to the treasury purchase, a fee equal to the recourse cap).
- Every amount is computed with `Decimal` and rounded half up; the noninterest-bearing note refuses a half-dollar step, and its present value factors are computed from the formula.
- Company names were checked against `content/` and `scripts/batches/`; ten clashing names were replaced before the first run.
- The script ran with no FAIL lines and no audit or lint warnings, and `pnpm content:validate` (run as `tsx scripts/content.ts validate`) passed.

## Blind verification

One verifier solved all 88 versions and matched every key. Fixes applied:
- `ppe-rollforward-0003`: the "proceeds taken as carrying amount" distractor now uses the right figure (key − gain).
- `inventory-rollforward-0003`: the consigned goods are counted but were never recorded as a purchase, so they matter in one place; new distractors are "consigned goods left in the count" and "all freight treated as selling expense". The key changed.
- `notes-0005`: dropped "although it has no refinancing agreement".
- `cash-flows-0011`: cumulative distributions have not exceeded cumulative equity in earnings.
- `notes-0006`: the balance sheet now states trade accounts payable of $214,000.
- `debt-noninterest-note-0001`: the straight-line rationale shows the rounded figure.
- `receivables-rollforward-0003`: dropped "records under the gross method".
- Version 0 of 11 items now has a distractor on each side of the key.

**Kept:** the verifier asked to retag `foreign-currency-transactions-0002` to Area III. It stays Area I / Income statement, because the 2026 FAR blueprint lists foreign-currency transaction gains and losses as task I.A.2c, and `foreign-currency-transactions-0001` is tagged the same way.

**Second blind pass.** A fresh verifier re-solved all 53 versions of the 14 changed items and matched every key, with no required fixes. One optional fix is applied: `special-purpose-frameworks-0004` now says the LLC uses the accrual method for tax, which the bad-debt deduction assumes.

**Key positions (a trade-off, accepted).** Giving every version 0 a distractor on each side of the key left version-0 keys at A 1, B 11, C 12, D 1, because numeric choices sort ascending. A key at A or D with every distractor on one side is the stronger cue, so the middle positions are accepted. The key letter still moves across versions in every family.

## Review gate

**Stratified gate** (tactic 4): 23 of 25 items. Twenty-two were reviewed in full: the 10 Analysis items, the 11 first items on empty tasks, and `inventory-lcm-0001` (ASU 2015-11). One was drawn at random from the other three (seed 20261001): `foreign-currency-transactions-0002`. Not gated: `receivables-factoring-0002`, `debt-noninterest-note-0001`.

**Result: passed.** The gated items average **84.9%** estimated pass likelihood (batches 07–08: 84.0%). 20 are exam-ready, 3 need minor revision and none need major revision, with no wrong keys in 81 versions. The sampled item was exam-ready, so escalation was not triggered. The gate mapped every item to a blueprint task independently and agreed with `far-coverage.py` on all 23, and it judged the mostly-B/C version-0 keys not to be a cue.

| Item | Gate | Fix |
| --- | --- | --- |
| `far-notes-0005` (78%) | Nothing said the note due June 30, Year 2 was long-term, so leaving it out of the maturities note was defensible. | The note was "originally issued with a three-year term". |
| `far-changes-in-equity-0004` (78%) | The "treasury excess left in income" distractor still charged the shortfall to paid-in capital from treasury stock, which that error would leave at zero; and "requires only par value … of that size" hinted at the correction. | The distractor is recomputed with the errors interacting ($2,130,000 / $1,367,000 / $3,320,000 / $869,000), and the stem says neutrally that state law requires par value to be capitalized for stock dividends. |
| `far-investments-fair-value-0003` (80%) | The key's "a company it must consolidate" echoed the ASC 825-10-15-5 exclusion wording. | The key is now "common shares giving it 70% of the voting shares of a regional distributor". |
| Nits | Held-for-sale move-out timing; "site of a future plant"; FX variant 1 ordering. | "Will vacate the building at closing"; "land for the new plant"; FX variant 1 swaps the loss distractor so its choices sort cleanly. |

**Blind re-check after the fixes:** a fresh verifier re-solved all 21 versions of the six changed items. It matched every key and found no second answers. Its one item-level fix is applied: variant 2 of `ppe-reconciliation-0003` swaps the weak "repair deducted twice" distractor ($3,286,600) for "no depreciation fix" ($3,250,000), as in the other versions.

**Open, bank-wide:** the verifier noted that none of those 21 keys is D. Because numeric choices sort ascending and each version 0 now has distractors on both sides of the key, the largest value is rarely correct. Bank-wide D keys are scarce (version 0: A 44, B 63, C 58, D 35 before this batch). The next batch should put some keys at D, using variants or items whose natural errors understate, without making every distractor err the same way.

**Bank after batch 09:** 200 FAR MCQs (501 variants), 12% / 51.5% / 36.5% by skill and 35.5% / 35% / 29.5% by area, all in range. Tasks I.A.3a and I.F.a still have no items.
