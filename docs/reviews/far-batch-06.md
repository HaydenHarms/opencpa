# Review report: FAR batch 06

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**25 items**, all written from scratch in `scripts/batches/far-batch-06.py`. Each of the 21 numeric items ships with three variants, 63 in all. Every variant family moves the key's letter.

## Plan: the coverage map

Roadmap step 4 defines FAR as done when every representative task in the blueprint has at least two reviewed MCQs. `scripts/far-coverage.py` is the new map for that:

- It lists all 113 representative tasks in the 2026 FAR blueprint, each with its skill.
- It maps every FAR MCQ to one task.
- It prints the tasks that still have fewer than two items.

Before this batch, 45 tasks had fewer than two items. Batch 06 took 25 of those gaps, including every gap the batch 05 review named: fund determination, the NFP statement of financial position, NFP cash flows and notes, amortized-cost investments, and debt covenants. It also filled most of the Area II subledger reconciliation and rollforward tasks, which are Analysis and keep the skill mix in range.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-balance-sheet-0005` | I.A.1 Prepare a classified balance sheet (working capital) | Application |
| `far-changes-in-equity-0003` | I.A.4 Prepare a statement of changes in equity | Application |
| `far-consolidated-statements-0007` | I.A.6 Prepare consolidated statements (upstream and downstream inventory profit) | Application |
| `far-nfp-financial-position-0002` | I.B.1 Recall the purpose of the NFP statement of financial position | Remembering and Understanding |
| `far-nfp-financial-position-0003` | I.B.1 Adjust an NFP statement of financial position | Application |
| `far-nfp-cash-flows-0002` | I.B.3 Recall the NFP statement of cash flows (restricted gifts as financing) | Remembering and Understanding |
| `far-nfp-cash-flows-0003` | I.B.3 Adjust an NFP statement of cash flows | Application |
| `far-nfp-notes-0001` | I.B.4 Adjust NFP notes (liquidity and availability) | Application |
| `far-governmental-fund-types-0002` | I.C.2 Determine the appropriate fund (permanent fund) | Application |
| `far-special-purpose-frameworks-0003` | I.E Prepare modified cash basis statements | Application |
| `far-ratios-0003` | I.F Calculate profitability ratios (return on common equity) | Application |
| `far-ratios-0004` | I.F Calculate solvency ratios (total debt ratio) | Application |
| `far-cash-bank-reconciliation-0003` | II.A Reconcile the bank balance (proof of cash) | Analysis |
| `far-cash-unreconciled-0001` | II.A Investigate an unreconciled cash difference | Analysis |
| `far-receivables-rollforward-0002` | II.B Rollforward of receivables and the allowance | Analysis |
| `far-receivables-reconciliation-0002` | II.B Reconcile the receivables subledger | Analysis |
| `far-inventory-rollforward-0002` | II.C Inventory rollforward with cutoff | Analysis |
| `far-inventory-reconciliation-0002` | II.C Reconcile the inventory subledger (LIFO reserve) | Analysis |
| `far-ppe-rollforward-0002` | II.D PP&E rollforward (cash paid for equipment) | Analysis |
| `far-ppe-reconciliation-0002` | II.D Reconcile the PP&E subledger | Analysis |
| `far-investments-amortized-cost-0001` | II.E.2 Identify investments eligible for amortized cost | Remembering and Understanding |
| `far-investments-htm-credit-loss-0001` | II.E.2 Impairment of held-to-maturity securities (CECL, discounted cash flows) | Application |
| `far-debt-covenant-0002` | II.H.2 Debt covenant calculation (funded debt to EBITDA) | Application |
| `far-contingencies-0006` | III.B Calculate contingency amounts (product warranty) | Application |
| `far-income-taxes-provision-0001` | III.D Tax provision entry | Application |

- **Batch mix:** by skill, 3 / 14 / 8 (12% / 56% / 32%); by area, 12 / 11 / 2.
- **Bank after batch 06:** 150 FAR MCQs. By skill, 12% / 51% / 37%. By area, 37% / 35% / 27%. Every figure is inside the blueprint ranges.
- **Variants:** there are now 372 variants across the bank.
- **Coverage:** 37 of 113 tasks now have two or more items. The map says about 98 more items are needed.

## Blind verification

One verifier solved all 92 versions blind. It matched the key on every version except three families, where it found a second defensible answer. There were no arithmetic errors. The fixes:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-contingencies-0006` (required) | "Repair in the year of sale" suggested the first-year window closed on December 31, which made the second-year-only amount defensible. | The stem now says "within 12 months after sale" and "in the second 12 months after sale", and that the estimates have not changed. |
| `far-income-taxes-provision-0001` (required) | "Credited to income taxes payable in the provision entry" allowed crediting the full current tax, with the prepaid relieved in a separate entry. | The item now asks for income taxes payable on the balance sheet after the estimated payments are applied, plus total expense. |
| `far-nfp-notes-0001` (required) | A board can undo its own designation, so counting the quasi-endowment as available was partly defensible. The receivables were not stated to be unrestricted. | The stem now says the board does not intend to spend from the quasi-endowment beyond the policy appropriation, and that the receivables are without donor restrictions. |
| `far-investments-htm-credit-loss-0001` | One version's present value ended in exactly $0.50, so the distractor's rounding was ambiguous. | New numbers in that version. The script now refuses a half-dollar present value. |
| `far-consolidated-statements-0007` | "Inc.." typo. | Fixed. |

The verifier also flagged four "duplicate" questions. The duplication was only in the blind file, where the four word items were listed twice; the content itself was not affected.

Kept, with the reasons:

- **Two of the Analysis tags** were read as Application, because the stems name the reconciling items: `far-cash-unreconciled-0001` and `far-inventory-rollforward-0002`. The tag stays Analysis. Both map to the blueprint's Analysis-marked tasks (investigate unreconciled cash; inventory rollforward), and the student must work out each item's effect and which side it belongs on. The review gate should confirm.
- **Key clustering in some families:** the key is C in three of four versions in four families. The letter does move, so this was left alone.
