# FAR variants 08

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**What this adds:** 33 variants, three for each of 11 numeric items from FAR batch 01. The script is `scripts/batches/far-variants-08.py`, with the same method as variants 03. Parameter set 0 rebuilt all 11 reviewed items word for word.

| Item | Area | Key letters by version | New distractor errors |
| --- | --- | --- | --- |
| `far-cash-flows-0003` | I | B C A B | carrying amount subtracted instead of the gain; receivables increase added |
| `far-cash-flows-0004` | I | C D C D | interest paid counted as financing |
| `far-consolidated-statements-0001` | I | C B C B | dividends to the noncontrolling interest left in |
| `far-eps-diluted-0001` | I | B A B A | cumulative preferred dividends not deducted |
| `far-comprehensive-income-0002` | I | B C B C | exchange gain left in OCI as well; equity-security gain removed |
| `far-equity-paid-in-capital-0002` | I | A B A B | full proceeds credited to APIC with no par split |
| `far-equity-retirement-0002` | II | A B A B | whole excess to retained earnings; APIC-only method (ASU 2025-12) |
| `far-debt-extinguishment-0001` | II | C D C C | straight-line discount amortization; loss measured against face |
| `far-equity-method-0001` | II | B A C B | profit on the resold inventory eliminated; dividends not deducted |
| `far-contingencies-0002` | III | A B A B | Claim 1 disclosed only |
| `far-accounting-errors-0001` | III | A B A B | inventory error added; Year 3 depreciation also removed |

**Where the variants add variety:**
- **Bond prices:** each is computed from its stated yield.
- **Diluted EPS:** the convertible bonds are antidilutive in every version, but by different margins.

## Blind verification

One verifier agent solved all 33 blind:

- It matched the key on all 33.
- All three bond prices matched a recomputation from their yields.
- Goodwill stayed positive in every NCI version, and there was enough APIC for every retirement charge.

| Finding | Fix |
| --- | --- |
| Required: one extinguishment version's "measured against face" distractor came out as "$-1,000", a negative number under a loss question. | Replaced it in that version with straight-line discount amortization ($39,438). |
| Optional: one equity-method distractor (profit on the resold 75% eliminated) is a thin error. | Kept. It is a nameable error, and the family uses it only once. |
| Optional: in one paid-in-capital version, the land's appraisal is above the value of the shares issued. | Kept. The shares are actively traded, so their price governs either way, which is the point of the item. |

A blind recheck of the changed version matched the key and named the error behind every distractor.
