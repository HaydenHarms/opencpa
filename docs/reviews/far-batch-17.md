# Review report: FAR batch 17

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**16 items**, all written from scratch in `scripts/batches/far-batch-17.py`, all numeric with three variants each (48 variants), so the batch adds 64 problems. Every variant family moves the key's letter. Built in parallel with batch 16 (Area III tasks III.C-III.F only); no shared tasks, topics or ids.

**Status: draft, rebuilt after a failed gate.** The first gate scored 62.0% with five major items and three wrong keys (details below). Every finding was applied or answered, nine of the 16 items were substantially rebuilt under the same ids (none was ever served), and the items are written with `review.status: draft` so they stay unserved until the blind verifier and the gate pass again.

## Plan

Slice: Area III -- Select Transactions, eight Application items and eight Analysis items, split across three task groups: accounting changes and error corrections (III.A), contingencies (III.B), and subsequent events (III.G). Each item was checked against every existing item on its task (read from `content/far/` before drafting). The rebuilt items change at least two of the scenario's component events and the stem format against those items, as the table's last column records.

| Item | Blueprint task | Skill | Scenario (after the rebuild) |
| --- | --- | --- | --- |
| `far-change-in-estimate-0003` | III.A.a Calculate adjustments for accounting changes and error corrections | Application | Life and salvage re-estimate; carrying amount after the year of change (distractors fixed only) |
| `far-change-in-principle-0003` | III.A.a | Application | **Rebuilt.** Change at the start of Year 4/5 with *three* years presented; asks for the restated prior-year **net income** (not opening retained earnings); a profit-sharing bonus as an indirect effect that isn't restated. No change *to* LIFO. |
| `far-error-correction-0001` | III.A.a | Application | **Rebuilt.** Note signed mid-year (partial-year interest computed from the date), found in Year 3 *after* the Year 2 statements were issued; asks for the January 1, Year 3, retained earnings adjustment. |
| `far-accounting-errors-0010` | III.A.b Derive the impact of an accounting change or error correction | Analysis | **Rebuilt.** Draft net income plus three recorded entries: a right-of-return sale (refund liability *and* return asset), freight and installation expensed on a machine placed in service mid-year, and a customer deposit correctly recorded as a liability. Asks for corrected net income (no EPS, no internal-use software). |
| `far-accounting-errors-0011` | III.A.b | Analysis | **Rebuilt.** Draft total liabilities and three questioned items: a purchase order in accounts payable, a declared but unrecorded dividend (treasury shares excluded), and an FOB-destination invoice that is correctly recorded. No item is labeled an error. |
| `far-accounting-errors-0012` | III.A.b | Analysis | **Rebuilt.** Draft total assets traced to support: unaccrued interest on a note receivable accepted mid-year, listed equity shares carried at cost instead of fair value, and goods out on consignment correctly kept in inventory. |
| `far-contingencies-0015` | III.B.b Calculate amounts of contingencies and prepare journal entries | Application | **Rebuilt.** Litigation roll-forward plus unasserted recall claims with a range and no best estimate (minimum accrued). No warranty. |
| `far-contingencies-0016` | III.B.b | Application | **Reframed.** Purchase-commitment loss plus a mail-in cash rebate as a refund liability under ASC 606 (expected claim rate less claims paid). |
| `far-contingencies-0017` | III.B.b | Application | **Rebuilt.** Discounted settlement (the entity's stated policy) plus self-insured injury claims: reported and incurred-but-not-reported accrued, next year's expected injuries not. No warranty. |
| `far-contingencies-0018` | III.B.c Review documentation for recognition versus disclosure | Analysis | **Rebuilt.** A draft contingencies note: an unasserted environmental penalty that agency practice and its published schedule make probable and estimable, and a patent suit with a stated demand that counsel can't assess. No guarantee. |
| `far-contingencies-0019` | III.B.c | Analysis | Indemnity best estimate within a range versus an unassessable whistleblower complaint; facts now establish probability, the complaint's figure is stated neutrally, and the indemnity's inception fair value is addressed. |
| `far-subsequent-events-0014` | III.G.b Calculate adjustments for identified subsequent events | Application | **Rebuilt.** A bonus pool fixed by Year 1 income as finally reported: a final Year 1 property-tax bill (recognized) lowers the base; a February warehouse gain (nonrecognized) doesn't. |
| `far-subsequent-events-0015` | III.G.b | Application | **Rebuilt.** A customer's bankruptcy after year-end from losses during the year (recognized, net of the existing specific allowance and expected recovery) versus a dividend declared in February; ASU 2025-05 election stated. |
| `far-subsequent-events-0016` | III.G.c Derive the impact of identified subsequent events | Analysis | Warranty settlement above accrual and a sales-tax audit assessment for Year 1 (both recognized) versus a customer default caused by a post-year-end regulation (described with facts, not a conclusion). |
| `far-subsequent-events-0017` | III.G.c | Analysis | **Rebuilt.** Insurance receivable reduced by the insurer's January assessment (recognized) versus a court award under appeal (gain contingency) and a February market decline. No count error, no bond cash. |
| `far-subsequent-events-0018` | III.G.c | Analysis | Penalty to a customer (a reduction of revenue) fixed after year-end versus a stock dividend; the company is a private, non-SEC filer, so SAB Topic 4C doesn't apply. |

- **Batch mix:** by skill, 0 / 8 / 8 (0% / 50% / 50%); by area, 0 / 0 / 16 (all Area III). The three `accounting-errors` items are now genuine Analysis by the quality bar's rule: each gives draft figures and supporting facts, includes one item that is correctly recorded, and never says which items are errors. So no tags changed, and no task mapping changed.
- **Variants:** 48. Items plus variants: 64.
- **Key letters:** version 0: A 4, B 5, C 5, D 2 (was A 1, B 11, C 4, D 0). All 64 versions: A 13, B 24, C 23, D 4.

## Process

### First build

Each builder computes the key and every distractor from `Decimal` inputs, rounded half up, with a named-error rationale for each distractor. The first build fixed two near-duplicate openings the lint caught (`accounting-errors-0011` and `-0012`; `contingencies-0015` and `-0017`).

### Script rewrite (after the gate)

`scripts/batches/far-batch-17.py` had drifted from `content/far`. A previous session had started rewriting it into 16 different questions under the same ids, left one builder referencing a missing parameter, and added a guard in `main()` that made it exit. The script was rewritten from scratch as the source of truth again, and the guard is gone:

- It has one builder per family. Parameter set 0 is the item, sets 1-3 are variants via `attach_variants`, each family has 4-5 error-derived distractors with `use` so the key's letter moves, and `family()` asserts that version 0 shows the central-twist distractor. Amounts use `Decimal` with `ROUND_HALF_UP`, and `audit()` runs on every version.
- Every amount that depends on a date is computed from the stem's dates (`months_from`, `months_to`): partial-year interest in `error-correction-0001` and `accounting-errors-0012`, and partial-year depreciation in `accounting-errors-0010`. No stem states a derived amount; for example, `contingencies-0017` no longer states the sum of reported and unreported claims.
- A local `rendering()` check fails the build on the template defects the gate found: a month or day followed by a bare digit ("December 31, 1"), "a 1 incident", "$-", "..", and "2 year". The script also reports amounts repeated in a stem (`REPEAT`) and choices within 0.4% of each other (`CLOSE`), and `distinct()` refuses two choices with the same signed amount.
- `review.status` is written as `draft`; `review.notes` keeps the "Batch 17." prefix.
- Run: `B17_SCRATCH=<dir> python3 scripts/batches/far-batch-17.py` writes `b17-blind.md` and `b17-keys.json` to that directory, in the same format as batch 16.

### Checks on the rebuilt batch

- `audit()`: zero warnings on all 16 items and 48 variants. The only lint output is four `note:key_in_stem` lines on `far-contingencies-0019`; counsel's stated best estimate is the answer, as in `far-contingencies-0012`.
- No `CLOSE` pairs. The remaining `REPEAT` lines are "accept the draft" or "accrue the demand" distractors, which by design equal a stem amount.
- An independent re-solve script (fresh formulas written from the accounting, not from the builders) reproduced the key and every displayed distractor in all 64 versions.
- `python3 scripts/batches/lint.py`: no warnings on batch 17 items; the 14 warnings it reports are all on older items.
- `python3 scripts/far-coverage.py`: all ids mapped, with no task-mapping changes.
- `pnpm content:validate`: passes.

**Blind file (rebuilt batch):** `/tmp/claude-0/-home-user-opencpa/e9bf392c-4031-54cc-bfc7-5753ee948460/scratchpad/gate/b17r/b17-blind.md` (64 versions, stems and lettered choices only) and `b17-keys.json` in the same directory, both outside the repo.

## Blind verification

**First run (on the original build):** 64 versions. The verifier found:

- No correct choice in any version of `accounting-errors-0010` and `accounting-errors-0012`.
- A timing contradiction that gave `error-correction-0001` a second defensible answer.
- Broken year labels ("December 31, 1") in `subsequent-events-0016` to `-0018`.
- A second defensible answer in `subsequent-events-0018` under SAB Topic 4C.
- Distractors in `contingencies-0018` that no stem fact produces.

All other items were clean, with advisories on `contingencies-0015`, `-0016`, `-0019`, `change-in-principle-0003` and `subsequent-events-0014`.

| Finding (verifier) | Fix |
| --- | --- |
| AE-0010: amortization run for a full year although the software went into service mid-year; no returns estimate given; distractors with no nameable error | Rebuilt (see the gate table). Partial-year depreciation is computed from the in-service date; the expected-return rate and cost ratio are given; every distractor is a single named error. |
| AE-0012: "two of the three years" contradicts a September 1 payment; stated unexpired amount; "remains" | Rebuilt with new events; no prepaid, and no derived amount in the stem. |
| EC-0001: "before closing its Year 2 books" makes the Year 1-only amount a second answer | Discovery is now in Year 3, *after* the Year 2 statements were issued; the Year 1-only amount is a distractor with that rationale. |
| SE-0016/17/18: "Year" dropped from the dates | Restored, and the build now fails on that pattern (`rendering()`). |
| SE-0018: SAB Topic 4C makes the stock-dividend deduction defensible | The company is a private, non-SEC filer, and statements are "available to be issued"; the explanation cites SAB 4C as the registrant-only rule. |
| C-0018: phantom $250,000-type distractors; CECL and release-from-risk facts missing | Guarantee dropped; every distractor is derived from a stem fact (statutory maximum, the demand). |
| Advisory: C-0019 add a probability fact | Added (state cleanup order and the buyer's claim). |
| Advisory: C-0016 "counted twice" distractors | Replaced; each distractor recomputed from its rationale. |
| Advisory: C-0015 "remaining estimate of the total cost" | Reworded ("revised its estimate of the suit's total cost upward by"). |
| Advisory: CP-0003 v3 change *to* LIFO | Removed; the four versions are FIFO to weighted-average, weighted-average to FIFO, LIFO to FIFO and LIFO to weighted-average. |
| Advisory: SE-0014 duplicate-sheet noise | Item rebuilt. |

**Second run:** pending, on the blind file above.

## Review gate

**First gate (on the original build):** **62.0%** average estimated pass likelihood, with five major items: AE-0010, AE-0012 and EC-0001, which had wrong keys in every version, plus C-0018 and SE-0014. The other 11 were minor and none was exam-ready. The gate failed. Every finding and how it was handled:

| Item | Gate finding | Fix |
| --- | --- | --- |
| AE-0010 (major) | Wrong key in all versions (full-year amortization); no returns estimate and no return asset; internally developed software is BAR scope and ASU 2025-06 is unaddressed; EPS has no Analysis task and the errors are listed | Rebuilt: right-of-return sale with refund liability and return asset (ASC 606-10-55-22 to 55-29), freight and installation capitalized and depreciated from the in-service month (ASC 360-10-30-1), and a correctly recorded deposit. Asks for corrected net income; draft figures with no "errors" label make it Analysis. |
| AE-0011 (minor) | Names its errors (Application); rebate cite should be ASC 606, not ASC 450 | Rebuilt as three questioned items with one correctly recorded (an FOB-destination invoice); the rebate moved out (C-0016 now carries the ASC 606 rebate), replaced by a declared, unrecorded dividend with treasury shares. |
| AE-0012 (major) | Wrong key (unexpired months); stated derived amount; repeats AE-0004 and AE-0008 events | Rebuilt with three new events (interest receivable from a mid-year note, equity shares at fair value under ASC 321, consigned-out goods correctly included); interest computed from the date. |
| CE-0003 (minor) | Retrospective-distractor rationale named the remaining life as the "total" life; v0 D weak | The rationale now names the revised total life; v0 shows the retrospective distractor; the weak "cost less depreciation" distractor is replaced by "ignores salvage" and "over the total life" distractors. |
| CP-0003 (minor) | Near-duplicate of CP-0001 and CP-0002; v2 "exceeds" false; "$-50,000"; change to LIFO | Two events changed (three years presented with a restated prior-year net-income ask, and an indirect-effect bonus that isn't restated, ASC 250-10-45-8); direction-aware rationales; amounts never print signed; no LIFO target. |
| C-0015 (minor) | Warranty repeats C-0003 and C-0017; v1 amount stands for two facts; weak distractor; ambiguous wording | Warranty replaced by unasserted recall claims at the range minimum; all amounts distinct; wording fixed. |
| C-0016 (minor) | v1-v3 distractor math didn't match the rationale; premiums under legacy ASC 605-50 and 450; v1 contract price echoed v0 | Reframed as a mail-in cash rebate: consideration payable to a customer and a refund liability (ASC 606-10-32-25, 32-10). Each distractor is recomputed from its rationale, and the contract prices differ in every version. |
| C-0017 (minor) | Warranty duplicates C-0015 and C-0003; wrong cite (ASC 450-20-30 for discounting) | Warranty replaced by self-insured IBNR claims; the cite is now SEC SAB Topic 5Y and ASC 835-30, and the stem states the discounting policy. |
| C-0018 (major) | Year-end guarantee measurement indeterminate (ASC 460-10-35-2 method, CECL); phantom distractors; near-duplicate of C-0004 | Guarantee dropped, as the gate preferred. Rebuilt in a new format (a draft contingencies note) with an unasserted, probable and estimable penalty and an unassessable patent suit whose demand is stated, so every distractor comes from a stem figure. |
| C-0019 (minor) | Probability not established; "only as background" is a giveaway; ASC 460 inception fair value not addressed | Added the state's cleanup order and the buyer's claim; the complaint "alleges $X"; stated that the indemnity's fair value when given was immaterial and nothing was recognized. |
| EC-0001 (major) | Stem contradicts the key (Year 2 still open); "2 year" grammar | Discovery after the Year 2 statements were issued; mid-year note with partial-year interest from the date; distractor for interest through the discovery date. The wrong-sign distractor was dropped because it formed a mirror pair with the key. |
| SE-0014 (major) | One subtraction; form-ruled-out D; posting-twice A; count error duplicates SE-0004 and SE-0017 | Rebuilt as a bonus-pool calculation. **Not built as the gate's NRV item:** `far-subsequent-events-0005`, on this same task (III.G.b), is already an NRV recognized-versus-nonrecognized inventory item, so that rebuild would have reused its template. |
| SE-0015 (minor) | Easy; dividend decorative in v0; settlement above accrual repeats SE-0004 and others | Customer bankruptcy from pre-year-end deterioration (net of the specific allowance and expected recovery); v0 shows the dividend distractor; ASU 2025-05 election stated. |
| SE-0016 (minor) | Year bug; "Ltd.."; "current and creditworthy then" states the conclusion; lawsuit repeats SE-0015 | Year restored; the customer's status is described with facts (paid within terms, credit line renewed); the lawsuit is replaced by a sales-tax audit assessment; ASU 2025-05 election stated. |
| SE-0017 (minor) | Year bug; count error duplicates SE-0014 and SE-0004; v0 D combined three errors; bond-cash D ruled out on form | Year restored; the count error is replaced by an insurance-receivable shortfall; the bond issue is replaced by a court award under appeal (gain contingency, ASC 450-30-25-1); every distractor is one error. **Not used: the gate's "final tax assessment for Year 1".** It would change liabilities, not the total assets asked for, and ASC 740-10 measures a tax position on information at the reporting date, which makes such an assessment's recognized-or-not classification contestable. |
| SE-0018 (minor) | Year bug; "includes a $140,000 accrual" loose; penalty is variable consideration | Year restored; "reflects a $X penalty, recorded as a reduction of revenue"; ASC 606-10-32-5 to 32-9 cited; nonpublic, so SAB Topic 4C doesn't apply. |
| Batch | Over-represented components (settlement above accrual, warranty, count error) | Each now appears at most once: warranty once (SE-0016's claim settlement), settlement above accrual once (the same claim), count error nowhere. |
| Batch | Key-letter skew (B 11 of 16) | Rebalanced: version 0 A 4, B 5, C 5, D 2. |
| Batch | Suggested bar additions (date-driven amounts in code, render audit, timing, derivable distractors, premiums under ASC 606, probability facts) | Applied inside this batch. The render check is local to `far-batch-17.py`, because `common.py` and `lint.py` are shared; moving it into `audit()` is a follow-up for the lead. |

**Second gate:** pending. Per the stratified policy, every Analysis item (8) and every rebuilt item gets the full gate. In practice that is the whole batch.

## Open items

1. **The rebuilt items haven't been through the blind verifier or the gate.** They stay `draft` until both pass.
2. **`far-contingencies-0016` and the III.B.b task.** A cash-rebate refund liability is ASC 606 measurement sitting on a contingencies task, as the gate recommended. If the second gate prefers a pure ASC 450 component, the rebate can be swapped without touching the commitment half.
3. **`far-subsequent-events-0014`** tests a bonus whose base depends on a recognized subsequent event. The gate should confirm that the bonus-determination framing reads as III.G.b ("calculate adjustments for identified subsequent events") and not as a payroll-accrual item.

## Second round (2026-10-07)

Reports in `docs/reviews/far-batches-15-17-round2/`.

- **Blind verifier:** all 64 versions agree with the key; no required fixes. Recommended: spread key positions (A 13, B 24, C 23, D 4, so the largest value is almost never the key); add "Ignore income taxes" to subsequent-events-0016 and -0017; state in contingencies-0017 that only the one-year payment is discounted.
- **Gate:** **78.5%** average (first gate 62.0%), all keys correct, **1 major**: `far-subsequent-events-0015` repeats the customer-bankruptcy event of subsequent-events-0002 and -0008 and the post-year-end dividend of four others; rebuild with two events new to III.G.b. Eleven minor findings with fixes are in the gate report, including an ASU 2015-11 currency gap in contingencies-0016 (commitment losses measured at NRV for a FIFO entity).

**Still to do:** apply both reports' fixes in `far-batch-17.py`, re-run the blind verifier and gate on the changed items, then set the builder's status to `reviewed` and rebuild.
