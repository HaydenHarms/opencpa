# FAR variants 03

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**What this adds:** 27 variants, three for each of the 9 remaining numeric items from FAR batch 04. The method is the same as variants 02. The shared helpers now live in `scripts/batches/variants.py`, and the script is `scripts/batches/far-variants-03.py`.

- Parameter set 0 rebuilt all 9 reviewed items word for word on the first run.
- Each family has a pool of named-error distractors, and each version shows three of them.

| Item | Area | Key letters by version | New distractor errors |
| --- | --- | --- | --- |
| `far-budget-variance-0001` | I | A C B B | revenue variance only |
| `far-nfp-financial-position-0001` | I | C B D C | scholarship gifts left out; property bought with unrestricted funds included |
| `far-consolidated-statements-0004` | I | A B A B | all intercompany profit eliminated, not just the unsold part |
| `far-debt-modification-0001` | II | B C C B | undiscounted cash flows compared |
| `far-intangibles-impairment-0001` | II | C B C B | one year of amortization short |
| `far-fair-value-techniques-0001` | III | B A B A | entity's own cash flows and discount rate |
| `far-accounting-errors-0003` | III | B C C B | Year 2 effect with the wrong sign |
| `far-contingencies-0004` | III | D C D C | reasonably possible lawsuit accrued |
| `far-income-taxes-nol-0001` | III | D C D C | current refund and deferred tax asset both recorded |

## What the variants change

- **Direction:** one flexible-budget version is favorable where the item is unfavorable, and it sells fewer units than budgeted.
- **Classification:** in two versions of the 10% test, the key becomes an extinguishment instead of a modification. The explanation then describes derecognizing the old note and including the fee in the gain or loss.
- **Relative size:** one income-approach version has an entity cost of capital below the market rate. Discounting at it therefore overstates fair value, the opposite of the reviewed item.
- **Recomputed factors:** the builders recompute the present value factors in each stem to four places.

## Blind verification

One verifier agent solved all 27 variants blind:

- It recomputed every present value factor and found all of them correct.
- It matched the key on all 27.
- It found no second defensible answer and no internal inconsistency.

| Finding | Fix |
| --- | --- |
| In the third 10% test version, every choice said "modification", so the treatment half of the question did no work. | The fee is now $30,000. The fee-subtracted distractor crosses 10% and reads "extinguishment". The verifier re-solved it: key 6.42%, modification. |
| The NOL distractors "20% of the benefit" and "twice the benefit" looked unnamed to a verifier that sees only stems and choices. | Kept. Their rationales name the errors: "benefit only for the 20% the limit disallows" (the reviewed item's own distractor) and "current refund and deferred tax asset both recorded". |
| Optional: the "scholarship gifts left out" distractor is a weaker error. | Kept. Its rationale says a purpose restriction lasts until the gifts are spent for that purpose. |
