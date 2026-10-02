# Review report: FAR simulations batch 02

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**6 simulations (45 points)**, all Area I, written from scratch in `scripts/batches/far-tbs-02.py` as the first batch of `docs/plans/far-simulations.md`. They use numeric, select and no journal-entry tasks. Research tasks still wait until cited paragraphs can be checked against the Codification. Every amount is computed in the script with `Decimal` and rounded half up. The script asserts that the comparative balance sheets, the corrected balance sheet and the draft-to-corrected net income reconciliations tie before it writes anything.

| Simulation | Blueprint task | Skill | Tasks |
| --- | --- | --- | --- |
| `far-tbs-cash-flows-0001` | I.A.5a Prepare a statement of cash flows (indirect method) and required disclosures | Application | 5 numeric, 1 select (8 points) |
| `far-tbs-consolidation-review-0001` | I.A.6c Detect and correct consolidated financial statement discrepancies | Analysis | 1 select, 4 numeric (9 points) |
| `far-tbs-balance-sheet-review-0001` | I.A.1c Detect and correct balance sheet discrepancies | Analysis | 5 numeric (8 points) |
| `far-tbs-income-statement-review-0001` | I.A.2d Detect and correct income statement discrepancies | Analysis | 6 numeric (8 points) |
| `far-tbs-nfp-activities-0001` | I.B.2b Prepare an NFP statement of activities | Application | 1 select, 4 numeric (8 points) |
| `far-tbs-eps-0001` | I.D.c Calculate basic and diluted EPS | Application | 5 numeric (7 points) |

FAR now has 9 simulations: Area I 6, Area II 1, Area III 2, with 4 of the 9 tagged Analysis.

## What each simulation tests

- **Cash flows (Brennick).** Comparative balance sheets, an income statement and dated transaction notes. Data to reject or handle: equipment bought with a note (noncash disclosure, then a financing principal payment), a 10% stock dividend, dividends declared versus paid, bond discount amortization in interest expense, and a gain on sale. Tasks: operating, investing and financing totals, interest and taxes paid, and a five-row classification.
- **Consolidation review (Pomeroy and Strand).** A wholly owned subsidiary held at cost, with an acquisition-date equipment step-up and goodwill, upstream intra-entity inventory sales with profit in both opening and closing inventory, an intra-entity loan and dividends. The staff accountant's draft has five errors and three correct lines; the candidate marks each line and computes corrected cost of goods sold, net income, equipment and retained earnings. An appraisal of the equipment and of Strand is data to reject.
- **Balance sheet review (Quillon).** A draft classified balance sheet with a six-month certificate of deposit in cash equivalents (beside a Treasury bill that does qualify), customer credit balances netted in receivables, consigned-in goods counted and goods in transit left out, a sinking fund and treasury stock in current assets, a declared dividend not recorded (outstanding versus issued shares) and the current installment of a term loan left in noncurrent liabilities.
- **Income statement review (Varga).** A draft multi-step statement where the sale of a whole operating segment sits in continuing operations and the sale of one warehouse is shown as discontinued, plus a cutoff error, interest in general and administrative expenses, a full-year insurance premium expensed in October, and an AFS fair value gain in net income. The warehouse loss belongs inside income from operations (ASC 360-10).
- **NFP statement of activities (Wrenfield).** A conditional promise with a matching barrier, an unconditional promise payable next year (implied time restriction), skilled and unskilled contributed services, a perpetual endowment gift with an appropriated return, releases for a van placed in service and for program spending, and a board designation that is not a donor restriction. The scenario fixes the clinic's two policy elections (placed-in-service release; restricted gifts met in the same year stay with donor restrictions).
- **EPS (Corwin).** A retroactive stock dividend, a mid-year issue and a treasury purchase in the weighted average, undeclared cumulative preferred dividends, one dilutive and one antidilutive option grant (average versus year-end price), and convertible bonds under the if-converted method (ASU 2020-06) with an after-tax add-back.

## Blind verification

(pending)

## Review gate

(pending)
