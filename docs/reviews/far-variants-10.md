# FAR variants 10

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

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
  recovery back in as an *additional* liability instead of a receivable, and misreading the gain
  contingency (the patent suit) as a loss and adding its expected award to the accrual. Both land above
  the key.
- `far-debt-covenant-0001`: the three original distractors (no adjustment, both adjustments added to
  liabilities only, and the warranty accrual recorded without the dividend) all understate the ratio.
  Added: recording the dividend but not the warranty accrual (also understates it, for more choice below
  the key), and two duplicate-posting errors — double-counting both adjustments, or just the dividend, in
  liabilities while equity reflects them only once — which overstate the ratio above the key.
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

| Item | Area | Key letters by version | New distractor errors |
| --- | --- | --- | --- |
| `far-accounting-errors-0002` | III | B D C C | believes the error fully resolved; treats it as a direct retained-earnings adjustment |
| `far-contingencies-0005` | III | D C B B | confirmed insurance recovery added as a liability; gain contingency misread as a loss |
| `far-debt-covenant-0001` | II | D C B C | dividend recorded without the warranty accrual; both adjustments, or just the dividend, double-posted |
| `far-revenue-allocation-0003` | III | B A B B | discount split equally among the three obligations; residual approach (ASC 606-10-32-34(c) bars it here) |

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

No version-0 distractor set changed, but the distractor pools are new designs, so a gate covers all four families' variants (results below once run).
