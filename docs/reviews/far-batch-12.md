# Review report: FAR batch 12

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**25 items**, all written from scratch in `scripts/batches/far-batch-12.py`. 23 numeric items ship with three variants each (69 in all), so the batch adds 94 problems. Every variant family moves the key's letter. Built alongside batch 13, which takes no task or topic this batch uses.

## Plan

No Remembering and Understanding items (that skill is at its 15% cap). The batch closes 15 one-item Application tasks in Areas I and II and adds 10 Analysis items in Area III, each changing at least two scenario events against every existing item on its task.

| Item                                   | Blueprint task                                                                                                                                                                  | Skill       |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `far-balance-sheet-0009`               | I.A.1b Adjust the balance sheet to correct identified errors (working capital: unrecorded accrued interest, customer deposit, overdraft, treasury stock, current maturity)      | Application |
| `far-income-statement-0008`            | I.A.2b Adjust the income statement to correct identified errors (dividends, equity security fair value change, consignment)                                                     | Application |
| `far-changes-in-equity-0007`           | I.A.4a Prepare a statement of changes in equity (retained earnings: property dividend at fair value, small stock dividend, treasury reissue below cost)                         | Application |
| `far-changes-in-equity-0008`           | I.A.4b Adjust the statement of changes in equity to correct identified errors (issuance costs, treasury stock, AFS loss)                                                        | Application |
| `far-cash-flows-0016`                  | I.A.5b Adjust a statement of cash flows to correct identified errors (operating section: gain, bond premium, receivables)                                                       | Application |
| `far-consolidated-statements-0011`     | I.A.6b Adjust consolidated financial statements to correct identified errors (wholly owned; intercompany inventory profit, intercompany receivable)                             | Application |
| `far-notes-0008`                       | I.A.7a Adjust the notes to correct identified errors and omissions (lease maturity analysis: omitted operating lease, short-term lease, warehouse liability shown discounted)   | Application |
| `far-nfp-financial-position-0005`      | I.B.1c Adjust an NFP statement of financial position to correct identified errors (perpetually restricted land at fair value, agency transfer, time-restricted pledge, release) | Application |
| `far-nfp-statement-of-activities-0004` | I.B.2c Adjust an NFP statement of activities to correct identified errors (contributed van depreciation, netted investment fees, unskilled volunteers)                          | Application |
| `far-special-purpose-frameworks-0006`  | I.E.c Prepare cash basis or modified cash basis statements (modified cash basis: capitalized equipment, no receivables or prepaids)                                             | Application |
| `far-cash-equivalents-0002`            | II.A.a Calculate cash and cash equivalents (original maturity, postdated and NSF checks; policy stated)                                                                         | Application |
| `far-ppe-held-for-sale-0003`           | II.D.d Determine whether an asset qualifies as held for sale (word item; criteria judged from facts)                                                                            | Application |
| `far-ppe-held-for-sale-0004`           | II.D.e Adjust the carrying amount of assets held for sale (write-down, capped recovery, no depreciation while held for sale)                                                    | Application |
| `far-investments-fair-value-0004`      | II.E.1b Calculate the carrying amount of investments at fair value (fair value option on an equity-method stake, AFS debt with credit loss)                                     | Application |
| `far-investments-fair-value-0005`      | II.E.1c Calculate investment income on investments at fair value and prepare journal entries (AFS debt: OCI credit in the fair value entry)                                     | Application |
| `far-change-in-principle-0002`         | III.A.b Derive the impact of an accounting change or error correction (LIFO to FIFO plus a prior-year error: opening retained earnings of the earliest period)                  | Analysis    |
| `far-change-in-estimate-0002`          | III.A.b (change in useful life with two material errors: Year 3 pretax income)                                                                                                  | Analysis    |
| `far-accounting-errors-0008`           | III.A.b (bond discount never amortized, inventory errors: restated equity)                                                                                                      | Analysis    |
| `far-accounting-errors-0009`           | III.A.b (purchase cutoff, consignment, freight: restated cost of goods sold)                                                                                                    | Analysis    |
| `far-contingencies-0012`               | III.B.c Review documentation for recognition versus disclosure (word item; legal letter)                                                                                        | Analysis    |
| `far-contingencies-0013`               | III.B.c (corrected liability for litigation and claims: settled claim, range, self-insurance reserve)                                                                           | Analysis    |
| `far-contingencies-0014`               | III.B.c (receivables: insurance recovery accepted, signed settlement; jury award under appeal and denied claim excluded)                                                        | Analysis    |
| `far-subsequent-events-0011`           | III.G.c Derive the impact of identified subsequent events (SEC filer; equity)                                                                                                   | Analysis    |
| `far-subsequent-events-0012`           | III.G.c (non-SEC filer, available-to-be-issued date; pretax income)                                                                                                             | Analysis    |
| `far-subsequent-events-0013`           | III.G.c (tax rate change enacted after year-end; net deferred tax liability)                                                                                                    | Analysis    |

- **Batch mix:** by skill, 0 / 15 / 10 (0% / 60% / 40%); by area, 10 / 5 / 10.
- **Variants:** 69. Items plus variants: 94.
- **Version-0 key letters:** A 6, B 7, C 7, D 5. All versions: A 17, B 38, C 30, D 9.
- **Bank after this batch:** 275 FAR MCQs with 681 variants (956 problems). Skill 13.5% / 49.8% / 36.7%; area 37.1% / 34.2% / 28.7%, all inside the blueprint ranges. 91 of 113 tasks have two or more items.

## Process

The builder enforces in code: version 0 shows the item's central-twist distractor; a family whose key letter never moves fails; no two choices coincide; and it prints stem amounts that repeat, choices equal to a stem amount, and choices too close together. The modified-cash builder asserts no two facts share an amount (it caught two coincidences, both fixed). `audit()` and the lint: zero warnings or notes on the 25 ids. `content:validate` passes.

Judgment calls: `far-accounting-errors-0008` says "Ignore income taxes" (a 25% rate put after-tax amounts on 50 cents); its amounts follow an effective-interest schedule to the dollar. Choices equal to a stem amount are each a named error (fair value without the cap in `ppe-held-for-sale-0004`; "most likely amount" in `contingencies-0013`; "settlement only" in `contingencies-0014`).

## Blind verification

One verifier solved all 94 versions from stems and choices only: **94 of 94 matched the key.** Required fixes, all applied:

1. `far-cash-equivalents-0002`: the stem didn't fix the entity's cash-equivalents policy, so a narrower policy (ASC 230-10-45-6) made other choices defensible in v1–v3. Added that the company treats every investment meeting the definition as a cash equivalent.
2. `far-notes-0008`: stated the omitted store lease is an operating lease.
3. `far-change-in-estimate-0002`: stated both errors are material; replaced two distractors that matched no student error with a catch-up-depreciation error (v0 $1,316,000, v1 $963,600, v3 $718,000).
4. `far-subsequent-events-0012`: replaced the "billing deducted twice" distractor (v0, v3) with the April settlement charged to Year 1.
5. `far-contingencies-0013`: stated settled-but-unpaid claims are reported in the litigation-and-claims liability.
6. Minor: `far-changes-in-equity-0007` states net income includes the land gain and the cost method for treasury stock; `far-nfp-financial-position-0005` states the land's net-asset class; `far-accounting-errors-0009` v0 replaced a double-error distractor with the central-twist error (key moves D → C, amount unchanged).

**Re-check** of the 27 changed versions by a fresh verifier: 27 of 27 matched the key. Its points: `far-notes-0008` works only on 59 remaining payments, which is the key (60 is a deliberate distractor); answer position following magnitude in `change-in-estimate-0002` falls out of ascending order, not a defect. One fix applied: `far-nfp-financial-position-0005` now says the camp gifts were made in Year 1, so the election to report gifts restricted and spent in the same period as unrestricted (ASC 958-605-45-4) can't apply.

## Review gate

**Stratified gate** (run on Sonnet, to save usage; same brief): 20 of 25 items. Seventeen in full: the 10 Analysis items; the items on recently changed standards (`notes-0008` for ASU 2016-02; `nfp-financial-position-0005` and `nfp-statement-of-activities-0004` for ASU 2016-14 and 2018-08; `investments-fair-value-0004` and `-0005` for ASU 2016-01 and 2016-13); and the items changed after blind verification (`cash-equivalents-0002`, `changes-in-equity-0007`). Three drawn at random from the other eight (seed 20261001): `cash-flows-0016`, `changes-in-equity-0008`, `ppe-held-for-sale-0003`. Not gated: `balance-sheet-0009`, `income-statement-0008`, `consolidated-statements-0011`, `special-purpose-frameworks-0006`, `ppe-held-for-sale-0004`.

**Result: passed.** The 20 gated items average **89.6%** estimated pass likelihood (batch 11: 84.2%). 19 are exam-ready, 1 needs minor revision, none need major revision. Every key is correct in every version the gate solved (80 numeric amounts). All three sampled items were exam-ready, so escalation was not triggered. This is the first gate run on Sonnet and its score is above every earlier FAR gate (82–85%), so it may grade more leniently; watch the next gates for drift.

| Item                                    | Gate                                                                                                                                                       | Fix                                                                                                                                                                   |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `far-investments-fair-value-0005` (83%) | Tagged II.E.1c ("calculate investment income ... and prepare journal entries") but asks for the OCI credit in the fair value entry, not investment income. | Not changed: the task covers preparing the entries, and the OCI credit is an amount in that entry. Retagging to II.E.1b would also reopen II.E.1c as a one-item task. |

**Batch 13 gate finding applied here too:** choices that mix "increase" and "decrease" now sort by signed value bank-wide (see the batch 13 report); no batch 12 item was affected.
