# FAR variants 10

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**What this adds:** 12 variants, three for each of the four numeric FAR MCQs left without variants by
variants 04, 06 and 09 (`far-contingencies-0005`, `far-debt-covenant-0001`, `far-revenue-allocation-0003`)
because every wrong answer sat in a fixed order around the key, so the key's letter could not move. The
script is `scripts/batches/far-variants-10.py`. Parameter set 0 rebuilt all four reviewed items word for
word, with no change to any version-0 distractor: each family's original three distractors are kept
exactly, and a pool of 1-4 new named-error distractors is added for variants to draw on.

**Method:** for each item, I worked out the pool of distractors that produced the original fixed order and
added at least one distractor on the other side of the key (an over-inclusion error) so a choice of three
could put the key above, below or between the others:

- `far-contingencies-0005`: the three original distractors (netting the insurance recovery against the
  liability with and without the unasserted claim, and reporting the lawsuit gross but omitting the
  unasserted claim) are all subsets of the key's liabilities. Added: adding the confirmed insurance
  recovery back in as an _additional_ liability instead of a receivable, and misreading the gain
  contingency (the patent suit) as a loss and adding its expected award to the accrual. Both land above
  the key.
- `far-debt-covenant-0001`: the three original distractors (no adjustment, both adjustments added to
  liabilities only, and the warranty accrual recorded without the dividend) all understate the ratio.
  Added: recording the dividend but not the warranty accrual (also understates it, for more choice below
  the key), and confusing the debt-to-equity ratio with the equity multiplier (adjusted total assets ÷
  adjusted equity), which always equals the correct ratio plus 1 and so sits well above the key. An earlier
  draft used two "double-posts an adjustment twice" distractors instead of the equity multiplier; the gate
  (below) called that an implausible, invented-for-arithmetic error, so both were dropped.
- `far-revenue-allocation-0003`: the three original distractors (all the discount to the license, the
  discount spread across all three obligations, and the license's full standalone price) bracket the key
  with one below and two above. Added: dividing the discount equally among the three obligations instead
  of by standalone selling price (above the key), and the residual approach — transaction price minus the
  implementation and support standalone selling prices — which ASC 606-10-32-34(c) rules out here because
  the license has an observable standalone selling price (below the key, and numerically identical to
  "all the discount to the license" by the item's own arithmetic, so the two are never used in the same
  version). An earlier draft of this item also tried "mistakes the bundled pair as license-and-implementation"
  and "subtracts the discount from the license twice"; both were dropped after blind verification (see
  below) found no believable student error that produces either number, and the first is ruled out anyway
  because the stem names the bundle explicitly.
- `far-accounting-errors-0002`: already had both a below-key and an above-key distractor (isolating the
  error to Year 1's retained earnings, and reversing the Year 2 direction), so the fixed order came from
  always using the same three. Added: believing the error is fully resolved because Year 2 ending inventory
  was correct (ignores that Year 2's beginning inventory was still wrong), and treating the Year 1 error as
  a direct retained-earnings adjustment instead of recognizing Year 2's income already reversed it — both
  below the key. This item's variants also flip the error's direction (overstated/understated) across
  versions, which changes the facts but tests the identical concept, as the brief for this batch allows.

| Item                          | Area | Key letters by version | New distractor errors                                                                                                                 |
| ----------------------------- | ---- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `far-accounting-errors-0002`  | III  | B D A C                | believes the error fully resolved; treats it as a direct retained-earnings adjustment                                                 |
| `far-contingencies-0005`      | III  | D C B B                | confirmed insurance recovery added as a liability; gain contingency misread as a loss                                                 |
| `far-debt-covenant-0001`      | II   | D C D C                | dividend recorded without the warranty accrual; confuses the ratio with the equity multiplier (total assets ÷ equity = the ratio + 1) |
| `far-revenue-allocation-0003` | III  | B A B B                | discount split equally among the three obligations; residual approach (ASC 606-10-32-34(c) bars it here)                              |

Three families' key letters move across at least three of the four letters; `far-revenue-allocation-0003`
moves between two (B and A) once the two undeliverable distractors described above were dropped, since the
remaining pool only supports one below-key and one above-key grouping. No version-0 distractor set changed,
so no item needs the full review gate solely because of this batch; the new distractors appear only in
versions 1-3.

**Blind-verification fix (applied):** the verifier's required fixes were all in `far-revenue-allocation-0003`
(`C:\Users\harms\AppData\Local\Temp\claude\opencpa-gate\v10\verifier.md`): the "mistakes the bundled pair"
distractor (v2 choice A, v3 choice B) and the "subtracts the discount twice" distractor (v3 choice A) had
no identifiable single-step student error reproducing their numbers, and the "mistakes the bundled pair"
error is implausible anyway since the stem names the license-and-support bundle explicitly. Both were
dropped from the pool and replaced with the residual-approach distractor described above; the equal-split
distractor was kept, with its rationale rewritten to show the subtraction explicitly
(`$L − ($disc ÷ 3) = $L − $disc/3`) so its derivation is unambiguous. Version 0 and all of
`far-accounting-errors-0002`, `far-contingencies-0005` and `far-debt-covenant-0001` were already clean per
the verifier and are unchanged.

**Checks run:** `python scripts/batches/far-variants-10.py` (writes the items; 0 audit warnings, only the
pre-existing `key_in_stem` note on `far-accounting-errors-0002`, which the original reviewed item already
carries), `python scripts/batches/lint.py content/far` (0 warnings on these four ids), `npx tsx
scripts/content.ts validate` (334/334 valid). `scripts/far-coverage.py` needs no change: these are existing
ids, not new ones.

## Blind verification

One verifier solved all 16 versions blind and matched every key. Its required fixes were all in `far-revenue-allocation-0003` versions 1-3 and are applied as described above. A fresh verifier then re-solved the three changed versions: 3 of 3 matched the key, every distractor traced to one named error, and no fixes were required.

## Review gate

Passed: average estimated pass likelihood ~85-86% across the 16 versions, no wrong keys, no major-revision
items (`C:\Users\harms\AppData\Local\Temp\claude\opencpa-gate\v10\gate.md`). The gate required three fixes,
applied here (re-run, audited, linted and validated; not committed by this pass):

1. **`far-contingencies-0005`, v0 choice B ($80,000), v1 choice B ($105,000) and v3 choice A ($145,000):**
   the rationale said the computation nets the insurance recovery against the base lawsuit liability alone,
   but the number nets it against the lawsuit-plus-unasserted-claim total. Reworded to show the actual
   computation, e.g. v0: "Nets the $150,000 insurance recovery against the $200,000 lawsuit liability, then
   adds back the $30,000 unasserted claim: $200,000 − $150,000 + $30,000 = $80,000." This is a rationale-only
   change to v0's choice B; the stem, key amount, tested concept and every other choice are unchanged.
2. **`far-debt-covenant-0001`:** every "double-posts an adjustment twice" distractor (v1 choice D, v2
   choices C and D, v3 choice D) was dropped as an implausible, invented-for-arithmetic error. Replaced with
   the family's existing natural errors (pre-adjustment balances; both adjustments added to liabilities
   without reducing equity; only the warranty recorded; only the dividend recorded) plus one new natural
   above-key error: confusing the ratio with the equity multiplier (adjusted total assets ÷ adjusted equity),
   which always equals the ratio plus 1. Key letters are now D (v0, v2, the multiplier absent) and C (v1, v3,
   the multiplier shown) — still moves, per the gate's suggested design.
3. **`far-accounting-errors-0002`:** `common.py`'s sort rule changed so "understated"/"overstated" after a
   dollar amount counts as a sign for the ascending-choice-order check (understated negative, overstated and
   $0 non-negative), and v0 and v2 were out of order under the new rule (this is also what the gate flagged
   independently). `attach_variants` already re-sorts versions 1-3 on every run, but version 0 is loaded
   from disk as-is and was never re-sorted that way, so I added a one-time `presort_v0()` step that re-sorts
   version 0's choices and recomputes its answer letter under the current rule before `run()` loads it.
   Only the choice order and ids changed; every choice's text and rationale, the stem and the explanation
   are untouched. **v0's key letter changed from B to... B** (coincidentally the same letter after
   resorting: new order is A = "both understated" [the old D], B = the key [unchanged content], C = "$0 net
   income, overstated RE" [the old A], D = "both overstated" [the old C]). v2's key letter changed from C to
   A.

Final key letters after all three fixes: `far-accounting-errors-0002` B D A C, `far-contingencies-0005`
D C B B (unchanged — only rationale wording changed), `far-debt-covenant-0001` D C D C. A second blind pass
of just the nine changed versions (debt-covenant v1-v3, contingencies v0/v1/v3, accounting-errors v0-v2) is
queued at `C:\Users\harms\AppData\Local\Temp\claude\opencpa-gate\v10\recheck2-blind.md` and
`recheck2-keys.json`.

**Blind re-check of the gate fixes:** a fresh verifier re-solved the 9 changed versions (`far-debt-covenant-0001` v1-v3, `far-contingencies-0005` v0, v1, v3, `far-accounting-errors-0002` v0-v2): 9 of 9 matched the key, and the choices sort correctly, including signed order for "understated" and "overstated". It could not derive the debt-covenant choices 2.76 (v1) and 2.59 (v3) from linear combinations of the stem amounts. They are the equity-multiplier error: adjusted total assets ÷ adjusted equity, which equals 1 plus the debt-to-equity ratio. That is a known confusion between two leverage ratios, so they were kept.

**Tooling:** `common.py` now treats "understated" and "overstated" after an amount as directions in the signed-value sort, with understated first. A bank-wide scan found only `far-accounting-errors-0002` out of order.
