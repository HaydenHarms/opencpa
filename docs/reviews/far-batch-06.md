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

## Review gate

The first run passed: **82.4% average estimated pass likelihood** (batch 05 scored 82%), with 17 exam-ready, 8 minor and 0 major. All 25 version-0 keys are correct, and the reviewer re-solved all 63 variants in code with no breaks. It confirmed from the PDF that both disputed Analysis tags are honest (II.A.c and II.C.c are marked Analysis).

**Minor fixes** (applied 2026-09-30; see "Follow-up" below):

1. `far-nfp-financial-position-0002`:
   - The key is the longest choice; shorten it.
   - Replace the budget-comparison choice with "each net asset class as a self-balancing set of accounts".
2. `far-nfp-notes-0001`:
   - Recast it as correcting a draft note of $715,000, to fit I.B.4a.
   - Swap the quasi-endowment point, which repeats `nfp-financial-position-0003`, for another limit on availability.
3. `far-special-purpose-frameworks-0003`:
   - Say only "its one modification is capitalizing and depreciating equipment" instead of spelling out the cash basis.
   - Optionally add fees collected in advance.
4. `far-ratios-0004`:
   - State the fixed redemption amount, or that the entity is a public business entity (ASC 480-10-65-1).
   - Replace the two-error 0.36 distractor.
5. `far-cash-unreconciled-0001`:
   - Delete "an error the bank has agreed to correct" and state the deposit slip total instead.
   - Optionally add a finding that needs no entry.
6. `far-receivables-reconciliation-0002`:
   - Replace the "as recorded" distractor D with one that uses the control-account items ($597,900 or $589,800).
   - Cite ASC 310-10 or Reg. S-X 5-02 instead of ASC 310-10-45.
7. `far-investments-amortized-cost-0001`: the key is the longest choice and uses the textbook wording. Reword it, and lengthen A.
8. `far-contingencies-0006`: replace the $48,000 "second-year only" distractor with $3,000 (the first-year estimate only).

**Also flagged:**

- `far-receivables-rollforward-0002`, variant 2: write-offs and the required ending allowance are both $26,000. Change ending receivables to $296,000.
- The coverage map has three errors:
  - II.D.d is Application in the PDF.
  - III.C.c is Remembering and Understanding.
  - `income-taxes-provision-0001` fits III.D.c better.
- The mix needs attention:
  - This batch is 48% / 44% / 8% by area, so batch 07 must be mostly Area III. The bank as a whole stays in range.
  - Version-0 keys are 56% B, because numeric choices are ascending. Rebalance distractor pools toward A and D.

## Follow-up (2026-09-30): gate findings applied

All eight minor fixes, the variant fix and the three coverage-map corrections are applied in `far-batch-06.py` and `far-coverage.py`:

| Item | Change |
| --- | --- |
| `far-nfp-financial-position-0002` | The key is shortened so it is no longer the longest choice. The budget-comparison choice is replaced by "each net asset class, kept as a self-balancing set of accounts". |
| `far-nfp-notes-0001` | Recast for I.B.4a: the student corrects a draft note ($715,000 in version 0) built as total cash + all receivables + other investments. The quasi-endowment point, which repeated `nfp-financial-position-0003`, is replaced by a bond-indenture debt service reserve (a contractual limit). The receivables are "unconditional" and donors placed no purpose restriction on them. |
| `far-special-purpose-frameworks-0003` | The stem says only that the one modification is capitalizing and depreciating equipment. Fees collected in advance were added, with a distractor that defers them. |
| `far-ratios-0004` | The entity is a public business entity, and the shares redeem at a fixed amount on a fixed date (ASC 480). The two-error 0.36 distractor is replaced by "current liabilities left out". |
| `far-cash-unreconciled-0001` | "An error the bank has agreed to correct" is gone. The stem now gives the bank-validated deposit slip total, and adds a May check that cleared in June, which needs no entry (with a distractor). |
| `far-receivables-reconciliation-0002` | Distractor D ("control account as recorded") is replaced by a control-account error: the posting difference added instead of subtracted. The citation is now ASC 310-10 and Reg. S-X 5-02. |
| `far-investments-amortized-cost-0001` | The key no longer uses the textbook wording and isn't the longest choice; choice A is longer. |
| `far-contingencies-0006` | The $48,000 "second-year only" distractor is replaced by the first-year estimate less repairs paid ($3,000). Versions 1 and 2 swap the weak $0 distractor for a real error. |
| `far-receivables-rollforward-0002` variant 2 | Ending receivables are now $296,000, so write-offs ($25,000) no longer equal the required allowance. |
| `scripts/far-coverage.py` | II.D.d is Application and III.C.c is Remembering and Understanding. `income-taxes-provision-0001` moves to III.D.c, which leaves III.D.e with no items. |

A blind verifier re-solved all 27 changed versions and agreed with every key. It found one problem, which is fixed: `far-ratios-0004` variant 3 lacked the item's core distractor (the mandatorily redeemable shares left in equity, 0.50). It also suggested three optional changes, all applied: the receivables wording, the $0 warranty distractor, and a more natural distractor in variant 3 of the receivables reconciliation.

**Not changed:** the version-0 key skew (bank keys 34% B). Batches 07 and 08 choose their version-0 distractors so the key lands on A or D in at least half of their numeric items.
