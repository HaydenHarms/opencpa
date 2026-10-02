# Review report: FAR batch 13

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**25 items**, all written from scratch in `scripts/batches/far-batch-13.py`. 21 numeric items ship with three variants each (63 in all), so the batch adds 88 problems. Every variant family moves the key's letter. Built in parallel with batch 12 on tasks and topics batch 12 doesn't use.

## Plan

The batch closes the last five one-item Application tasks, takes a second item on four Remembering and Understanding tasks (the skill stays under its 15% cap), adds six Application items in Area III, and adds ten Analysis items on the Area II rollforwards and reconciliations, each changing at least two scenario events against every existing item on its task.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-nfp-cash-flows-0005` | I.B.3c Adjust an NFP statement of cash flows to correct identified errors | Application |
| `far-nfp-notes-0002` | I.B.4a Adjust NFP notes to correct identified errors and omissions (endowment note) | Application |
| `far-income-tax-basis-0001` | I.E.d Prepare income tax basis statements | Application |
| `far-ratios-0007` | I.F.b Calculate profitability ratios (return on assets) | Application |
| `far-budget-variance-0002` | I.F.f Calculate budget-to-actual variances (volume variance) | Application |
| `far-revenue-contract-costs-0003` | III.C.e Determine recognition and measurement of contract costs | Application |
| `far-nfp-contributions-0002` | III.C.g Calculate NFP contributions of financial and nonfinancial assets | Application |
| `far-income-taxes-deferred-0003` | III.D.d Calculate deferred tax assets and liabilities | Application |
| `far-fair-value-techniques-0002` | III.E.b Use assumptions and approaches to measure fair value (principal market) | Application |
| `far-lessee-finance-0003` | III.F.c Calculate lessee assets and liabilities and prepare journal entries | Application |
| `far-lessee-operating-0005` | III.F.d Calculate lessee lease costs | Application |
| `far-fair-value-approaches-0001` | III.E.a Identify valuation techniques used to measure fair value (cost approach) | Remembering and Understanding |
| `far-nfp-agent-transfers-0002` | III.C.c Identify NFP agent or intermediary transfers that are not contributions | Remembering and Understanding |
| `far-troubled-debt-restructuring-0002` | II.H.1b Understand when a change in terms is a troubled debt restructuring (debtor, ASC 470-60 after ASU 2022-02) | Remembering and Understanding |
| `far-intangibles-classification-0002` | II.F.a Identify recognition criteria and classify intangibles as finite- or indefinite-lived | Remembering and Understanding |
| `far-receivables-rollforward-0005` | II.B.c Prepare a rollforward of trade receivables (sales tax, factoring without recourse) | Analysis |
| `far-receivables-reconciliation-0005` | II.B.d Reconcile the receivables subledger to the general ledger (employee advance, finance charges, lockbox timing) | Analysis |
| `far-receivables-reconciliation-0006` | II.B.d (net adjustment to the control account) | Analysis |
| `far-inventory-rollforward-0005` | II.C.c Prepare a rollforward of inventory (import duties, double freight, NRV write-down; superseded LCM as a distractor) | Analysis |
| `far-inventory-reconciliation-0005` | II.C.d Reconcile the inventory subledger to the general ledger (internal transfer, goods on approval, freight-out) | Analysis |
| `far-inventory-reconciliation-0006` | II.C.d (consigned-out goods, return at selling price, bill-and-hold) | Analysis |
| `far-ppe-rollforward-0005` | II.D.f Prepare a rollforward of PP&E (accumulated depreciation: partial year, land and building allocation, leasehold term) | Analysis |
| `far-ppe-reconciliation-0005` | II.D.g Reconcile the PP&E subledger to the general ledger (depreciation expense: construction in progress, capitalized interest, idle asset) | Analysis |
| `far-payables-reconciliation-0004` | II.G.d Reconcile the payables subledger to the general ledger (purchase order, voided check, trade discount) | Analysis |
| `far-payables-reconciliation-0005` | II.G.d (foreign-currency remeasurement, unreversed accrual) | Analysis |

- **Batch mix:** by skill, 4 / 11 / 10 (16% / 44% / 40%); by area, 5 / 10 / 10.
- **Variants:** 63. Items plus variants: 88.
- **Version-0 key letters:** A 6, B 7, C 6, D 6. All versions: A 15, B 35, C 25, D 13.
- **Bank after batches 12 and 13:** 300 FAR MCQs with 744 variants (1,044 problems). Skill 13.7% / 49.3% / 37.0%; area 35.7% / 35.3% / 29.0%, all inside the blueprint ranges. 100 of 113 tasks have two or more items; the 13 left are all Remembering and Understanding.

## Process

The first builder was stopped by a usage limit after writing the script; a second builder (Sonnet) finished it. Before running it, that builder reworded `far-income-taxes-deferred-0003`'s closing clause, which shared a 14-word run with `far-income-taxes-deferred-0002`, and widened four choice pairs the spacing check flagged (`ppe-rollforward-0005` v2 and v3, `ppe-reconciliation-0005` v0 and v3) by changing inputs, not formulas. It then re-solved all 21 numeric version-0 items in a standalone script (none of the builder's functions): every key matched. `audit()` and the lint (including the tag-versus-task check once the ids were mapped): zero warnings. `content:validate` passes.

## Blind verification

One verifier (Sonnet) solved all 88 versions from stems and choices only: **88 of 88 matched the key**, every distractor in every version traced to a single named error, and no required fixes. Notes: `inventory-rollforward-0005` uses the superseded lower-of-cost-or-market floor only as a distractor (the key is lower of cost and NRV under ASU 2015-11); `troubled-debt-restructuring-0002` choice C (assets whose fair value equals the carrying amount, in full settlement) is not a troubled debt restructuring under ASC 470-60-15-9, which the gate should confirm.

## Review gate

Pending; it runs on batches 12 and 13 together.
