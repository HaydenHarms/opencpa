# FAR variants 07

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**What this adds:** 39 variants, three for each of 13 numeric items from FAR batch 02. The script is `scripts/batches/far-variants-07.py`, with the same method as variants 03. Parameter set 0 rebuilt all 13 reviewed items word for word.

| Item                                  | Area | Key letters by version | New distractor errors                                                    |
| ------------------------------------- | ---- | ---------------------- | ------------------------------------------------------------------------ |
| `far-special-purpose-frameworks-0001` | I    | D C D C                | cash received only; year-end advances counted as revenue                 |
| `far-ratios-0001`                     | I    | A C B B                | cash ratio; trading securities left out                                  |
| `far-nfp-cash-flows-0001`             | I    | C D B C                | construction payments subtracted; mortgage repayment left out            |
| `far-change-in-principle-0001`        | III  | C B C B                | whole year-end difference treated as a Year 2 effect                     |
| `far-receivables-factoring-0001`      | II   | A B A B                | no loss recorded on the sale                                             |
| `far-investments-htm-0001`            | II   | A C A C                | one year of amortization only; fair value above and below amortized cost |
| `far-payables-reconciliation-0001`    | II   | D C D C                | misposted invoice left in accrued liabilities                            |
| `far-treasury-stock-0001`             | II   | B C B B                | none (the pool's extra error was replaced; see below)                    |
| `far-revenue-principal-agent-0001`    | III  | C B C B                | both lines reported gross                                                |
| `far-revenue-contract-costs-0001`     | III  | A B A B                | legal fee capitalized with the commission                                |
| `far-lessee-operating-0003`           | III  | D C D C                | initial direct costs expensed at once                                    |
| `far-subsequent-events-0002`          | III  | D C B D                | each recognized event on its own; allowance ignored; fire recognized     |
| `far-change-in-estimate-0001`         | III  | D C D C                | double-declining rate applied to original cost                           |

**Where the variants add variety:**

- **Payables reconciliation:** in two versions the unposted payment exceeds the goods in transit, so the subledger total sits above the key.
- **Held-to-maturity bond prices:** each is computed from its stated yield.

## Blind verification

One verifier agent solved all 39 blind:

- It matched the key on all 39.
- All nine bond prices matched a recomputation from their yields.
- All three payables reconciliations tied from both sides.
- Every lease stayed clearly operating.

| Finding                                                                                                               | Fix                                                                                              |
| --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Required: one treasury-stock version's "loss measured from the first resale price" distractor ($17,500) is contrived. | Replaced with "preferred APIC also absorbs the loss" ($3,000), the error the other versions use. |
| Two versions of a family came out with the same key; the audit caught it before writing.                              | Changed one change-in-estimate version's cost.                                                   |
| Optional: one change-in-principle distractor matched two different errors because both years' differences were equal. | Changed that version's Year 1 FIFO figure so the differences differ.                             |

A blind recheck of the two changed versions matched both keys and could name the error behind every distractor.
