# FAR variants 05

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**What this adds:** 36 variants, three for each of 12 numeric items from FAR batch 03. The script is `scripts/batches/far-variants-05.py`, with the same method as variants 03. Parameter set 0 rebuilt all 12 reviewed items word for word.

| Item                                      | Area | Key letters by version | New distractor errors                                          |
| ----------------------------------------- | ---- | ---------------------- | -------------------------------------------------------------- |
| `far-nfp-functional-expenses-0001`        | I    | A B A B                | management and general's share of rent left out                |
| `far-ratios-0002`                         | I    | C D C D                | stops at the turnover                                          |
| `far-cash-bank-reconciliation-0002`       | II   | A C B B                | ledger adjusted for deposits in transit and outstanding checks |
| `far-inventory-dollar-value-lifo-0001`    | II   | A B A B                | stops at base-year cost                                        |
| `far-accrued-liabilities-0001`            | II   | D C D C                | bonus computed before deducting the bonus                      |
| `far-bonds-premium-0001`                  | II   | B A B A                | stated rate applied to the carrying amount                     |
| `far-ppe-held-for-sale-0001`              | II   | B C B C                | depreciation continued after classification as held for sale   |
| `far-receivables-reconciliation-0001`     | II   | D C D C                | customer credit balances added to receivables                  |
| `far-stock-dividends-splits-0001`         | II   | C B C B                | large dividend at the pre-split par                            |
| `far-contingencies-0003`                  | III  | D C D C                | high end of the environmental range                            |
| `far-subsequent-events-0003`              | III  | A B A B                | inventory's whole carrying amount written off                  |
| `far-revenue-variable-consideration-0002` | III  | B C C C                | all revenue deferred until the threshold                       |

**Where the variants add variety:**

- **Bank reconciliations:** one version's adjustment is an increase. The builders compute each bank balance so that both sides reconcile.
- **Bond issue prices:** each is computed from its stated yield.
- **Dollar-value LIFO:** versions liquidate different fractions of the Year 2 layer.

## Blind verification

One verifier agent solved all 36 blind:

- It matched the key on all 36.
- Every bank reconciliation balanced.
- Every bond price matched its stated yield to the dollar.
- No renumbered figure crossed a rule threshold. Small versus large stock dividends, volume above the discount threshold, and recoveries within the prior loss all held.

| Finding                                                                                        | Fix                                                                                                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Required: "a 8% stock dividend"                                                                | Fixed. It led to a pipeline-wide fix: `attach_variants()` now corrects "a"/"an" before every templated number, since 8…, 11 and 18 are spoken with a vowel. A scan found the same slip in 8 variants from earlier batches ("a $80,000", "a $18,000", "a $11,000"). All are corrected, and a rescan of every variant finds none. |
| Optional: the "averages the two prices" distractor is weak.                                    | Replaced in two volume-discount versions with the list-price and defer-all-revenue errors.                                                                                                                                                                                                                                      |
| Two ratio versions came out with the same key (73.0 days); the audit caught it before writing. | Changed one version's cost of goods sold.                                                                                                                                                                                                                                                                                       |
