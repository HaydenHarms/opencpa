# Review report: FAR batch 07 (Area III slice)

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**11 items**, all written from scratch in `scripts/batches/far-batch-07.py`. Each of the 8 numeric items ships with three variants (24 in all), so the slice is 35 versions. Every variant family moves the key's letter. The other Area III and Area I slice of batch 07 is reported separately by its own builder.

## Plan

The items fill gaps that `scripts/far-coverage.py` prints for Area III, plus one Area II payables reconciliation.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-accounting-errors-0005` | III.A.b Derive the impact of an accounting change or error correction (DDB to straight-line applied retrospectively in a draft retained earnings statement, with tax) | Analysis |
| `far-accounting-errors-0006` | III.A.b Derive the impact of an accounting change or error correction (five errors across Years 1–3; find which are still uncorrected at January 1, Year 4) | Analysis |
| `far-contingencies-0010` | III.B.a Recall recognition and disclosure criteria for commitments and contingencies (remote guarantees are still disclosed) | Remembering and Understanding |
| `far-contingencies-0007` | III.B.b Calculate amounts of contingencies and prepare journal entries (environmental remediation: range with no best estimate, then remeasurement, disputed insurance claim) | Application |
| `far-contingencies-0008` | III.B.c Review documentation for recognition versus disclosure (counsel's letters, insurer denial, board minutes: amount accrued and reasonably possible excess disclosed) | Analysis |
| `far-contingencies-0009` | III.B.c Review documentation for recognition versus disclosure (prior-year accrual updated by a judgment on appeal, future compliance cost, settlement range, unpredictable threat: Year 2 loss) | Analysis |
| `far-revenue-five-step-0001` | III.C.a Recall five-step model concepts (indicators that a promise is not separately identifiable) | Remembering and Understanding |
| `far-nfp-promises-to-give-0001` | III.C.b Recall recognition of NFP conditional and unconditional promises to give (barrier plus right of return or release; intention to give) | Remembering and Understanding |
| `far-revenue-contract-costs-0002` | III.C.e Determine recognition and measurement of contract costs (incremental commission, setup fulfillment costs, practical expedient elected, amortization from service start) | Application |
| `far-nfp-contributed-services-0002` | III.C.f Determine NFP revenue for contributed services (specialized skills that would otherwise be bought; services enhancing a nonfinancial asset) | Application |
| `far-payables-reconciliation-0002` | II.G.d Reconcile the payables subledger to the general ledger (net adjustment to the control account) | Analysis |

- **Slice mix:** by skill, 3 / 3 / 5 (Remembering and Understanding / Application / Analysis); by area, 0 / 1 / 10.
- **Variants:** 24 (8 numeric items × 3). Items plus variants: 35.
- **Version-0 key letters:**
  - Numeric: `accounting-errors-0005` D, `accounting-errors-0006` A, `contingencies-0007` C, `contingencies-0008` D, `contingencies-0009` A, `revenue-contract-costs-0002` A, `nfp-contributed-services-0002` B, `payables-reconciliation-0002` D. Six of the eight are on A or D.
  - Word items (rotated by `finalize()`): `contingencies-0010` A, `revenue-five-step-0001` B, `nfp-promises-to-give-0001` C.
  - Overall: A 4, B 2, C 2, D 3.
- **Key letters across versions:** 0005 D A B B; 0006 A D B C; 0007 C D D C; 0008 D B B C; 0009 A B A B; contract costs A C B B; contributed services B C A B; payables D B B C.

## Process

- Existing items read first so no template repeats: `accounting-errors-0001` to `0004`, `change-in-estimate-0001`, `change-in-principle-0001`, `contingencies-0002` to `0006`, all `revenue-*` items, `nfp-contributed-services-0001`, `nfp-financial-position-0003` and `nfp-contributions-0001` (both use matching-gift conditions, so the new promises item avoids them), and `payables-cutoff-0001` and `payables-reconciliation-0001`.
- Company names were checked against `content/` and every batch script; 16 names that clashed were replaced before the final run.
- Every amount is computed with `Decimal`. The script asserts that no distractor coincides with the key or with another distractor in any version. The script ran with no audit warnings, and `pnpm content:validate` passed.

## Blind verification

One verifier solved all 35 versions blind and matched the key on every one. It found no second defensible answer and no superseded rule. Fixes:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-accounting-errors-0005` | Distractor A in versions 0 and 2 matched no nameable error (both corrections made pretax, with the wrong sign). | The pool entry is now one error: the lower Year 4 depreciation added back without its tax effect. |
| `far-contingencies-0007` (all versions) | "A state environmental agency named Ostrander Chemical responsible…" could read as the agency's name. | "…designated Ostrander Chemical as a party responsible…" |
| `far-revenue-contract-costs-0002` (all versions) | "Configuring its own processing systems" could fall under internal-use software (ASC 350-40), which takes precedence over ASC 340-40 and made the commission-only choice defensible. | The set-up is now migrating and testing the client's payroll data and setting up its pay rules in existing systems, "costs not within the scope of any other Topic". |

Kept: the verifier asked whether the NFP items belong under a topic other than "Revenue recognition". The bank's other NFP contribution items use that topic, and the 2026 FAR blueprint places NFP contributions in Area III revenue recognition (III.C).

**Second blind pass.** A fresh verifier re-solved all 32 changed versions across batches 07 and 08, and matched every key. It found no second answer and no superseded rule. For this batch, `far-revenue-contract-costs-0002` now says the 10-month contract won't be renewed and its commission relates only to that contract. Version 0 also swaps a distractor, so the key is no longer the smallest choice with every distractor adding one item.

## Review gate

Pending.
