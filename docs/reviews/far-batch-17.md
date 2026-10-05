# Review report: FAR batch 17

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**16 items**, all written from scratch in `scripts/batches/far-batch-17.py`, all numeric with three variants each (48 variants), so the batch adds 64 problems. Every variant family moves the key's letter. Built in parallel with batch 16 (Area III tasks III.C-III.F only); no shared tasks, topics or ids.

## Plan

Slice: Area III -- Select Transactions, eight Application items and eight Analysis items, split evenly across three task groups that batch 12 had already added Analysis items to: accounting changes and error corrections (III.A), contingencies (III.B), and subsequent events (III.G). Every item was checked against every existing item on its task (read from `content/far/` before drafting) and changes at least two of the scenario's component events, uses a stem format none of them use, and asks for a figure none of them ask for.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-change-in-estimate-0003` | III.A.a Calculate adjustments for accounting changes and error corrections (depreciation life/salvage re-estimate) | Application |
| `far-change-in-principle-0003` | III.A.a (LIFO/weighted-average/FIFO inventory method change, restated comparative COGS) | Application |
| `far-error-correction-0001` | III.A.a (unaccrued note interest, named error, retained-earnings correction) | Application |
| `far-accounting-errors-0010` | III.A.b Derive the impact of an accounting change or error correction (unrecorded sales returns + capitalized software, corrected EPS) | Analysis |
| `far-accounting-errors-0011` | III.A.b (unaccrued customer rebate liability + a purchase order wrongly recorded as a liability, corrected total liabilities) | Analysis |
| `far-accounting-errors-0012` | III.A.b (unexpired service-contract prepayment + goods in transit FOB shipping point, corrected total assets) | Analysis |
| `far-contingencies-0015` | III.B.b Calculate amounts of contingencies and prepare journal entries (litigation accrual rollforward + warranty rollforward) | Application |
| `far-contingencies-0016` | III.B.b (noncancelable purchase commitment loss + premium-offer liability) | Application |
| `far-contingencies-0017` | III.B.b (settlement with an immediate and a discounted deferred payment + warranty rollforward) | Application |
| `far-contingencies-0018` | III.B.c Review documentation for recognition versus disclosure (board minutes: a fee-paid loan guarantee at inception fair value + a patent suit with no estimate counsel will support) | Analysis |
| `far-contingencies-0019` | III.B.c (counsel's letter naming a best estimate within a range for an indemnification clause + compliance-committee minutes on an open whistleblower inquiry) | Analysis |
| `far-subsequent-events-0014` | III.G.b Calculate adjustments for identified subsequent events (inventory count/pricing error found before issuance vs. post-year-end financing) | Application |
| `far-subsequent-events-0015` | III.G.b (lawsuit settled for more than accrued vs. a dividend declared after year-end) | Application |
| `far-subsequent-events-0016` | III.G.c Derive the impact of identified subsequent events (warranty and lawsuit settlements vs. a customer default from a post-year-end regulation, working capital) | Analysis |
| `far-subsequent-events-0017` | III.G.c (inventory count error vs. an equity-market decline and a bond issuance, total assets) | Analysis |
| `far-subsequent-events-0018` | III.G.c (penalty renegotiation vs. a stock dividend, retained earnings) | Analysis |

- **Batch mix:** by skill, 0 / 8 / 8 (0% / 50% / 50%); by area, 0 / 0 / 16 (all Area III).
- **Variants:** 48. Items plus variants: 64.
- **Version-0 key letters:** A 1, B 11, C 4, D 0. All versions (64): A 7, B 35, C 19, D 3.

## Process

Each builder function computes the key and every distractor from `Decimal` inputs (`ROUND_HALF_UP` via `rd()`/`m()` in `variants.py`), with a named-error rationale per distractor. Parameter set 0 rebuilds the reviewed item; sets 1-3 are its variants; every family's `twist` distractor is asserted present in version 0. Two defects surfaced and were fixed before the batch was final:

- `far-accounting-errors-0011` and `far-accounting-errors-0012` opened with the identical sentence "Reviewing the records before the statements are issued, the controller finds two errors. First, ... Second, ...", a shared run the lint's near-duplicate check caught (`near_duplicate`). `far-accounting-errors-0012`'s opening was reworded to a different structure ("Before \[Co\]'s ... financial statements are issued, its controller finds two problems with the draft ..."); facts, amounts, keys and distractors unchanged.
- `far-contingencies-0015` and `far-contingencies-0017` shared a ~14-word run describing the warranty fact pattern ("sold \[amount\] of products during the year that carry a one-year warranty included in the price; ... estimates warranty costs at ..."). `far-contingencies-0017`'s warranty sentence was reworded to a different structure and order of facts; amounts, keys and distractors unchanged.

`audit()` (which calls the deterministic lint) now reports **zero warnings** on all 16 ids and their 48 variants; the only lint output left is four `note:key_in_stem` lines on `far-contingencies-0018` and `far-contingencies-0019`, both legitimate (the guarantee's inception fair value, and counsel's stated best estimate, are each the correct answer by itself, directly stated as a fact in the stem -- the same pattern as the existing `far-contingencies-0012` item on the same task). `python3 scripts/far-coverage.py` reports no unmapped, double-mapped or missing ids. `npx tsx scripts/content.ts validate` passes (350 files, 350 reviewed).

**far-coverage.py mapping additions** (left applied in the file):
- `III.A.a`: added `"change-in-estimate-0003", "change-in-principle-0003", "error-correction-0001"`
- `III.A.b`: added `"accounting-errors-0010", "accounting-errors-0011", "accounting-errors-0012"`
- `III.B.b`: added `"contingencies-0015", "contingencies-0016", "contingencies-0017"`
- `III.B.c`: added `"contingencies-0018", "contingencies-0019"`
- `III.G.b`: added `"subsequent-events-0014", "subsequent-events-0015"`
- `III.G.c`: added `"subsequent-events-0016", "subsequent-events-0017", "subsequent-events-0018"`

**Blind file:** `C:\Users\harms\AppData\Local\Temp\claude\opencpa-gate\b17\b17-blind.md` (64 versions, stems and lettered choices only) and `b17-keys.json` (same dir), both outside the repo.

## Blind verification

TODO -- not yet run.

## Review gate

TODO -- not yet run.

## Open items / uncertain

1. **Version-0 key-letter skew.** Across the 16 items, version 0's key lands on B eleven times, C four times, A once, and never D; across all 64 versions, B is the key 35 times (55%), far above the ~25% a flat distribution would give. Every family still moves its key's letter across its own four versions (the hard requirement `common.py` enforces, and no family failed it), but the skew arises from how these items are shaped: additive "combine two corrections" items (most of this batch) tend to put the correct combined figure below a couple of "double-counts" or "includes an extra item" distractors and above only an "omits one correction" distractor, which structurally lands the key near the middle-low position (B) across many parameter draws. I didn't rebalance this by hand-picking different `use` subsets per version, since doing that well requires checking each family's numeric ordering individually; flagging it here for the lead's call on whether it's worth a follow-up pass before the gate.
2. **`far-contingencies-0018`'s guarantee fact pattern.** I gave the guarantee a fee in this item (so recognition at inception fair value is tested against a "no claim yet filed" distractor rather than a "no fee, so no liability" distractor, which `far-contingencies-0004` already uses on a different task-adjacent item). Worth the gate double-checking that this doesn't read as too similar to `far-contingencies-0004`'s guarantee fact pattern even though they're on different tasks (III.B.c here vs. the same task for -0004 too, actually -- both are III.B.c) -- I checked -0004's events (guarantee with a fee, insurance commitment, purchase commitment, all building to a "nothing accruable" word-style item structure) against mine (guarantee with a fee at a board meeting, paired with a patent suit with no estimate) and judged the combination of events and the board-minutes document format different enough, but it's a closer call than the others.
3. **`far-change-in-principle-0003`'s direction.** Two of the four parameter sets (Marchant, Oswestry) have the new method's inventory *below* the old method's, so the cumulative effect is a decrease rather than an increase; the builder formats every choice with `chg()` (an explicit "increase"/"decrease" suffix) specifically so this doesn't produce a bare negative dollar amount, and `common.py`'s signed-value sort handles the mixed directions correctly. Worth the gate confirming the explanation text reads correctly in both directions, since I verified the arithmetic but didn't read every rendered variant's prose by eye.
