# FAR variants 09

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**What this adds:** 30 variants, three for each of 10 numeric items from FAR batch 01. The script is `scripts/batches/far-variants-09.py`, with the same method as variants 03. Parameter set 0 rebuilt all 10 reviewed items word for word.

**Left without variants:** `far-revenue-allocation-0003`. Its wrong answers fall in a fixed order around the key (whole discount to the license < key < discount spread across all three obligations < standalone price), so the key's letter can't move.

| Item | Area | Key letters by version | New distractor errors |
| --- | --- | --- | --- |
| `far-ppe-reconciliation-0001` | II | C B C B | freight capitalized but the recorded gain left in place |
| `far-ppe-exchange-0001` | II | C D C D | new asset recorded at the old asset's fair value, without the cash paid |
| `far-inventory-lcnrv-0001` | II | C D C D | none (same three errors, new numbers) |
| `far-investments-afs-credit-loss-0002` | II | A B B A | no credit loss because there is no intent to sell; fair-value floor ignored |
| `far-receivables-credit-losses-0002` | II | B C B C | bankrupt customer pooled at the general rate |
| `far-intangibles-cloud-computing-0001` | II | B A C B | vendor evaluation capitalized; all costs expensed |
| `far-nfp-contributions-0001` | III | A B A B | unconditional promise left out; unrestricted gift counted |
| `far-lessee-finance-0001` | III | C D C C | Year 2 interest only; payment plus amortization |
| `far-fair-value-highest-best-use-0001` | III | B B B A | construction costs not deducted |
| `far-income-taxes-deferred-0001` | III | D C C B | deferred tax asset added to expense |

**Where the variants add variety:**
- **AFS credit loss:** in one version, the fair-value floor limits the allowance, so no part of the decline goes to OCI.
- **Cloud computing:** the terms and renewal periods differ, so the amortization period changes.

## Blind verification

One verifier agent solved all 30 blind (plus a recheck of the fixed variants-08 version):

- It matched the key on all 30.
- Every PP&E reconciliation tied from both sides.
- Every lease liability's rounding was checked against the present value of its payments.

| Finding | Fix |
| --- | --- |
| Required: in one lease version, the key ($73,562) was the only non-round choice. | That version's cash-payment distractor was replaced with Year 2 interest only ($14,562). |
| Required: one lease version's liability ($200,000 "rounded") was $1,427 off the present value of its payments. | Changed the payment to $56,400, whose present value is $199,992. |
| Optional: two fair-value versions leave out the current-use value, the main highest-and-best-use error, so their key is always the lowest choice. | Added the current-use value to one of them. The other keeps its choices so the key's letter still moves. |
| Optional: in one lease version, the key was the only choice with hundreds. | Swapped payment plus amortization for Year 2 interest only ($15,900). |

A blind recheck of the four changed versions matched every key.
