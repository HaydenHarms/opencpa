# FAR variants 04

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**What this adds:** 36 variants, three for each of 12 numeric items: 7 from FAR batch 05 and 5 from FAR batch 03. The script is `scripts/batches/far-variants-04.py`, with the same method as variants 03. Parameter set 0 rebuilt all 12 reviewed items word for word.

**Left without variants:** `far-contingencies-0005`. Every wrong answer is a subset of the key's liabilities, so the key is always the largest amount and its letter can't move without an implausible distractor.

| Item                                     | Area | Key letters by version | New distractor errors                                                                     |
| ---------------------------------------- | ---- | ---------------------- | ----------------------------------------------------------------------------------------- |
| `far-changes-in-equity-0002`             | I    | B C B B                | draft accepted                                                                            |
| `far-nfp-statement-of-activities-0001`   | I    | B C A B                | investment return left out                                                                |
| `far-cash-flows-0005`                    | I    | A B A B                | interest and dividends kept in investing; loan collection left out                        |
| `far-eps-basic-0001`                     | I    | B A B A                | stock dividend ignored                                                                    |
| `far-consolidated-statements-0003`       | I    | C B C B                | depreciation added back without eliminating the gain                                      |
| `far-balance-sheet-0002`                 | I    | C B A B                | cash surrender value kept current; officer loan kept current                              |
| `far-income-statement-0002`              | I    | A B A B                | interest expense left in operating expenses                                               |
| `far-investments-equity-securities-0001` | II   | B C B C                | none: the key's letter moves because fair value lands above cost in two versions          |
| `far-property-dividend-0001`             | II   | D B D B                | none: two versions have fair value below carrying amount, so the dividend produces a loss |
| `far-accounting-errors-0004`             | III  | B A B B                | Year 2 expense with the wrong sign                                                        |
| `far-nfp-gifts-in-kind-0001`             | III  | B C B C                | donated food left out                                                                     |
| `far-revenue-material-right-0001`        | III  | C D C D                | expected redemption rate left out                                                         |

## Blind verification

One verifier agent solved all 36 blind:

- It matched the key on all 36.
- It found no second defensible answer, no identical choices and no grammar errors.
- It confirmed that the loss versions of the property dividend are worded consistently, and that the impairment applies in every measurement-alternative version.

Its optional notes, and what I did with them:

| Note                                                                                                    | Action                                                              |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| The "loan collection left out" distractor in two cash-flow versions is weaker than the other errors.    | Replaced with "note-financed equipment kept", the item's own error. |
| "Trading securities classified as noncurrent" in one current-assets version is implausible.             | Replaced with "cash surrender value kept current".                  |
| One EPS distractor ($2.71) comes from two different errors: year-end shares, or treasury stock ignored. | Kept. Its rationale names the year-end-shares error.                |
