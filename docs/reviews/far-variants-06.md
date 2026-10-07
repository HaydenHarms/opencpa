# FAR variants 06

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**What this adds:** 33 variants, three for each of 11 numeric items: 3 from FAR batch 03 and 8 from batch 02. The script is `scripts/batches/far-variants-06.py`, with the same method as variants 03. Parameter set 0 rebuilt all 11 reviewed items word for word.

**Left without variants:** two items whose every wrong answer falls on the same side of the key, so its letter can't move without an implausible distractor.

- `far-debt-covenant-0001`: every error lowers the ratio.
- `far-accounting-errors-0002`: one amount with over- and understated labels.

| Item                                | Area | Key letters by version | New distractor errors                                                 |
| ----------------------------------- | ---- | ---------------------- | --------------------------------------------------------------------- |
| `far-balance-sheet-0001`            | I    | C B C B                | refinanced note kept current                                          |
| `far-income-statement-0001`         | I    | C B C B                | hurricane loss left as an extraordinary item                          |
| `far-changes-in-equity-0001`        | I    | B C B C                | prior-period adjustment made pretax                                   |
| `far-consolidated-statements-0002`  | I    | C D C D                | profit on the resold units eliminated                                 |
| `far-cash-bank-reconciliation-0001` | II   | B C B C                | ledger adjusted for bank-side timing items                            |
| `far-cash-equivalents-0001`         | II   | A B A B                | overdraft at another bank netted                                      |
| `far-inventory-reconciliation-0001` | II   | C D C D                | FOB-destination goods left out                                        |
| `far-intangibles-patent-0001`       | II   | D C D C                | original cost spread over the remaining life                          |
| `far-revenue-over-time-0001`        | III  | C D A C                | percent-complete change × revised profit                              |
| `far-nfp-contributed-services-0001` | III  | D C D C                | greeters' time recognized                                             |
| `far-lessee-finance-0002`           | III  | B A C B                | expected residual value discounted instead of the guarantee shortfall |

## What the variants change

- **Revenue over time:** one version has a cost overrun that cuts estimated profit, so Year 2's catch-up is small.
- **Lease liability:** in one version the expected residual value is below the guarantee shortfall, which moves that distractor below the key.

## Blind verification

One verifier agent solved all 33 blind and found no required fixes:

- **Keys:** it matched the key on all 33.
- **Factors:** every present value factor was correct.
- **Ties:** every draft total and reconciliation tied.
- **Classification:** the stock dividends stayed small, so they are recorded at fair value.
- **Grammar:** every "a"/"an" before a number was correct.

It made two optional notes:

- The held-for-sale discontinued-operations stem could say no write-down was needed. That wording belongs to the reviewed item and doesn't change the key.
- One revenue-over-time distractor is the weakest in its pool. It is used consistently across the family.
