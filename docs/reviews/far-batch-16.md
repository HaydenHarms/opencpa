# Review report: FAR batch 16

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**16 items**, all written from scratch in `scripts/batches/far-batch-16.py`, all Area III (Select
Transactions), all Application and all numeric with three variants each (48 variants), so the batch adds
64 problems. Built as one slice of batches 15-17 (Application and Analysis items that bring Remembering
and Understanding back under its 15% cap); the other slices cover Area II (batch 15) and III.A, III.B and
III.G (batch 17), with no shared ids or tasks. The items are `status: draft` until the gate re-passes on
the reworked versions below; none has been served.

## Plan

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-revenue-variable-consideration-0003` | III.C.d Determine revenue under the five-step model (a bonus fully constrained) | Application |
| `far-revenue-principal-agent-0002` | III.C.d (ride-hailing platform: agent for rides despite setting the price, principal for its own subscription) | Application |
| `far-revenue-licenses-0002` | III.C.d (sales-based royalty exception for a functional and a symbolic license; a symbolic license's fixed fee over time) | Application |
| `far-revenue-contract-costs-0004` | III.C.e Determine recognition and measurement of contract costs (PP&E and supplies outside ASC 340-40; amortization from the service start) | Application |
| `far-nfp-contributed-services-0003` | III.C.f Determine NFP revenue for contributed services (revenue and expense: a specialized service expensed, unskilled labor that creates an asset capitalized) | Application |
| `far-nfp-contributed-services-0004` | III.C.f (services capitalized into construction in progress, including staff lent by an affiliate) | Application |
| `far-nfp-contributions-0003` | III.C.g Calculate NFP contributions of financial and nonfinancial assets (short-term promise, donated supplies, a condition not met, a donor's forgiveness of a loan) | Application |
| `far-income-taxes-provision-0004` | III.D.c Calculate income tax expense and current taxes payable (current component with an installment sale, life insurance proceeds, nondeductible dues and estimated payments) | Application |
| `far-income-taxes-deferred-0004` | III.D.d Calculate deferred tax assets and liabilities (separate ledger balances with a valuation allowance) | Application |
| `far-income-taxes-provision-0005` | III.D.e Prepare journal entries to record the tax provision (deferred tax expense with a change in the valuation allowance) | Application |
| `far-fair-value-in-use-0001` | III.E.b Use assumptions and approaches to measure fair value (highest and best use in combination, judged from market evidence; cost approach) | Application |
| `far-fair-value-liability-0001` | III.E.b (a liability's own nonperformance risk at the measurement date) | Application |
| `far-lessee-finance-0004` | III.F.c Calculate lessee assets and liabilities (residual value insurance the lessor bought; initial direct costs) | Application |
| `far-lessee-operating-0006` | III.F.c (private-company risk-free rate election after ASU 2021-09; refundable security deposit; payments in advance) | Application |
| `far-lessee-finance-0005` | III.F.d Calculate lessee lease costs (a purchase option the candidate judges; Year 2 interest and amortization over the useful life, with initial direct costs) | Application |
| `far-lessee-operating-0007` | III.F.d (declining rent, a cash incentive and a variable property-tax reimbursement) | Application |

- **Batch mix:** by skill, 0 / 16 / 0 (0% / 100% / 0%); by area, all Area III. None of these tasks is
  marked Analysis in the blueprint, so Application is the ceiling and every tag is honest. The slice is
  meant to be merged with batches 15 and 17 before the lead recomputes the bank-wide mix.
- **Variants:** 48. Items plus variants: 64.
- **Key letters:** version 0, A 3, B 6, C 5, D 2. All versions, A 15, B 19, C 22, D 8 (before the
  rework: A 11, B 34, C 17, D 2). Keys stay in ascending numeric order; the letters moved by choosing
  which three distractors each version shows.
- **Coverage:** `python3 scripts/far-coverage.py` reports 113 of 113 tasks at two or more items. The ids
  are unchanged, so the coverage map needed no edit.

## Process

Built from scratch against `docs/content-pipeline.md`, one builder per family (parameter set 0 is the
item, sets 1-3 its variants, a pool of four or five named-error distractors per family, Decimal
ROUND_HALF_UP throughout). Every existing item on each task was read before the rework, so each reworked
item changes its format or ask and at least two component events against them.

Builder changes made in the rework, beyond the per-item fixes below:
- The builder writes `status: draft`; the lead flips it to `reviewed` once the gate passes.
- `pv_annuity_due()` now computes the annuity-due factor exactly and rounds once. The old version rounded
  the ordinary factor and then multiplied by 1 + i, which put lessee-operating-0006 v3 $6 off.
- The duplicate-choice and clustering checks compare every amount in a paired choice, not just the first.
- lessee-finance-0005's builder derives the liability from the payments and the option price, then
  asserts that the liability rolls forward to the option price (within table rounding) in every version.
- licenses-0002's builder asserts that a quarter of the sales projection never equals actual sales.

`audit()` (with the lint) returns zero warnings on the 16 ids and their 48 variants. The only lint
output is a `key_in_stem` note on nfp-contributed-services-0003, whose key's expense half is the
technician's stated value. That is correct, since the expense is exactly that amount. `python3
scripts/batches/lint.py` shows 14 warnings, all on other batches' ids. `pnpm content:validate` passes
(409 files: 364 reviewed, 45 draft or retired).

## Blind verification

**First pass (before the gate), 64 versions.** All 64 answers matched the keys. The verifier flagged six
required fixes: lessee-finance-0005 v0, v1 and v3 had a liability smaller than the PV of the payments
alone; licenses-0002 v0's forecast trap equalled the key; lessee-finance-0004 v1 to v3 and
deferred-0004 v2 had distractors with no nameable error; nfp-contributions-0003 discounted at a rate the
stem never gave; and lessee-operating-0006 v3 was $6 high. All six are fixed below.

**Rework re-check.** The rebuilt 64 versions were re-solved independently in Python. The solver works from
the blind file's stems and choices only, parses the facts and recomputes each answer from first
principles, including exact present values and a roll-forward of the finance-lease liability. It shares
no code with the builder. Result: 64 of 64 match the key, with exactly one matching choice each. A fresh
blind file for a verifier pass is at the scratch path `gate/b16r/b16-blind.md` (keys in
`b16-keys.json`); see open items.

## Review gate

Independent review agent, 2026-10-05, all 16 items gated in full. **Result: 78.2% average, two
major-revision items, all 64 keys correct.** The batch did not pass. Every finding was applied as
follows.

| Item | Gate (and verifier) finding | Fix |
| --- | --- | --- |
| `far-lessee-finance-0005` | **Major.** The liability in v0, v1 and v3 was less than the PV of the fixed payments, yet a purchase option had to be added. The stem stated "reasonably certain". It was a near-copy of lessee-finance-0001 (same ask, one event changed). The citation 842-20-25-4 to 25-6 was wrong. | Rebuilt. The stem gives the option price ($40,000) against the machine's expected value ($150,000) and its useful life, and the candidate judges exercise. The liability is computed from given factors as PV(payments) + PV(option price), and the builder asserts that it rolls to the option price. Initial direct costs were added. The ask is now a paired "Year 2 interest; amortization", unlike finance-0001's single total. The distractors are term amortization, option excluded (so term amortization too, both effects computed), initial direct costs omitted, and Year 1 interest. Cites 842-10-30-5(c), 842-20-30-5 and 842-20-35-8. |
| `far-nfp-contributed-services-0004` | **Major.** A near-duplicate of 0001 (four of five events mapped one to one), and the fourth item on the same stem and choice template. | Rebuilt with a new event set and format. A clinic under construction: cash paid to the contractor, an architect's donated drawings, a project manager lent by an affiliated hospital, and volunteers at the groundbreaking. The ask is paired "construction in progress; contributed services revenue". The board-member and front-desk events are retired. |
| `far-lessee-operating-0006` | ASU 2021-09: the stem implied the risk-free rate replaces the implicit rate. "Which isn't rent" pre-classified the deposit. The payment sentence was copied from operating-0004. The citation 842-10-15 was wrong. The verifier found v3 $6 off. | The stem now says the implicit rate isn't readily determinable and that the election is made for the real-estate class. "Which isn't rent" was dropped and the payment sentence rewritten. PV factors are given, and the annuity-due factor is computed exactly, so v3's key is $266,152 with every distractor shifted to match. Cites 842-20-30-3 (as amended by ASU 2021-09) and 842-10-30-5. |
| `far-income-taxes-provision-0005` | Same template as provision-0002 (a single entry, then "debit to income tax expense"). The v1 to v3 D rationale misdescribed its computation. Temporary differences weren't named. | The ask changed to deferred income tax expense alone. Current tax becomes a named distractor ("total expense"). The temporary differences are named (prepaid expenses; allowance for credit losses), neither of which provision-0002 uses. The ending-balances distractor now uses all three ending balances, and its rationale states exactly that. |
| `far-income-taxes-deferred-0004` | Third item on III.D.d with the "net deferred tax asset" stem and ask. The allowance sentence was copied from deferred-0001. v0 lacked the current-portion twist distractor. v2's $90,000 had no nameable error. Single jurisdiction wasn't stated. | Format changed to paired ledger balances ("asset net of allowance; liability"). The allowance sentence was rewritten. The current-portion error, now ($47,000; $45,000), is in v0, and $90,000 is gone. Single jurisdiction is moot, since nothing is netted. |
| `far-income-taxes-provision-0004` | Same stem and paired-choice template as provision-0001. "(and taxed)" and "a nontaxable amount" labels. | The ask is now the current component of income tax expense, as disclosed, a figure no III.D.c item asks. The estimated payments become a named error (they reduce the payable, not expense). The installment sale is now of land, with the gain taxed as collected. The labels were dropped. Asking for the payable alone, one of the gate's options, would still have been half of provision-0001's ask, so it wasn't used. |
| `far-nfp-contributed-services-0003` | Two classification giveaways ("enhancing ... even though no specialized skill"; "didn't call on her database expertise"). Third item on the same template. The off-specialty professional repeated 0002. | The events are described without conclusions. The format is now paired "revenue; expense", so the candidate must capitalize the shed labor and expense the specialized service. A piano technician replaces the architect, and stuffing fundraising letters replaces the off-specialty consultant. |
| `far-revenue-contract-costs-0004` | Recited the ASC 340-40-25-5 criteria and the "incremental" definition. Third item on the "contract cost assets at December 31" template. v0 lacked a start-date distractor. | The stem describes the work and says only that the fee schedule includes a setup charge. The ask is now Year 1 amortization. Signing dates are the first of a month, so "from signing" is exact, and v0 carries it ($42,000). New distractors expense one cost or the other. |
| `far-nfp-contributions-0003` | Distractor B discounted at an unstated rate, and present value is a permitted alternative. "Measurable barrier" was definition wording. The van repeated contributions-0002. | The PV distractor was dropped, and the stem states Perrin's measurement for promises due within a year. The condition is stated as facts (pays only if a clinic opens by June 30, Year 2; construction hasn't begun). The van was replaced by a supporter's forgiveness of a loan, a contribution under the ASC 958-605-20 definition. Use of facilities, the gate's suggestion, wasn't used because nfp-gifts-in-kind-0001 on the same task already has free warehouse use. The supplies are "for use in its patient-care programs" (verifier). Citations are at Subtopic level. |
| `far-lessee-finance-0004` | Over-signalled the exclusion ("not Tredinnick ... not a related party") and used IDC definition wording. A redundant "no alternative use" clue. The "half the guarantee" distractor had no nameable error. Wrong citation. | Reworded to "the lessor separately bought residual value insurance from Harbor Mutual" and "a broker commission, due only because the lease was signed". The clue was dropped. "Half" was replaced with "full guarantee, undiscounted" (gate's option). PV factors are given. Cites 842-10-30-5(f) and 842-20-30-5. |
| `far-fair-value-in-use-0001` | The stem stated the highest-and-best-use conclusion. Loose citation. | The stem now gives market evidence (the line installed and running against its machines sold one at a time) and the candidate concludes. Cites 820-10-35-10A to 35-10E and 820-10-55-3D. "Stithians's" became "Stithian". |
| `far-revenue-licenses-0002` | Verifier: v0's quarter-of-projection trap equalled the key. Gate: D in v1 to v3 (gross sales) was implausible, and the stem read awkwardly. | v0's projection is now $1,200,000, and the builder asserts the coincidence can't recur. Gross sales was replaced by "royalty from a quarter of the projection" and "whole brand fee at grant". The brand license's fixed fee is now annual and paid at signing, so the right-to-access judgment changes the key. Both licenses are dated. |
| `far-fair-value-liability-0001` | Exam-ready. Nits: factor precision unstated; citation; weak n+1 distractor in v1 (verifier). | Stem says to use four-place factors. Cites 820-10-35-16 and 35-17 to 35-18. v1 shows the pre-downgrade premium in place of n+1. Undiscounted face dropped from the pool. |
| `far-lessee-operating-0007` | Exam-ready. Nit: odd landlord-cost motivation text. The verifier wanted the explanation to address pattern of benefit. | Text cut. The explanation now says straight-line holds unless another basis better reflects the lessee's use (842-20-25-6(a)). An "incentive deducted all in Year 1" distractor was added. |
| `far-revenue-principal-agent-0002` | Exam-ready. Nit: v0 and v2's 80%-for-20% distractor was weak. The verifier wanted the explanation to say why price-setting is outweighed. | The flip distractor was removed from v0 and v2. The explanation now weighs pricing discretion against the drivers' acceptance and fulfilment. |
| `far-revenue-variable-consideration-0003` | Exam-ready. Suggestion: swap v0's $0 for the expected-value error. | v0 shows $344,000 in place of $0. The citation was narrowed to 606-10-32-11 to 32-12. |

Not applied, with reasons:
- **Asking for the taxes payable alone in provision-0004.** That would still be half of provision-0001's
  paired ask, so the current component was used instead.
- **Single-jurisdiction sentence in deferred-0004.** The item no longer nets the two balances.
- **Verifier's "ROU equals the lease liability" sentence for finance-0005.** It was superseded: the
  rebuilt stem gives initial direct costs, so the right-of-use asset is computed.
- **Verifier's question about the NFP topic tag** ("Revenue recognition"). It was kept. III.C.f and
  III.C.g sit under III.C Revenue recognition in the blueprint task list that `scripts/far-coverage.py`
  mirrors, and the existing NFP items use the same tag.
- **The quality-bar and lint changes the gate proposed** (a mechanical per-task template check, an
  implied-value check, refusing distractors that need an unstated parameter, adding ASU 2021-09 to the
  item 9 list, more recitation examples). They touch shared files (`docs/content-pipeline.md`,
  `scripts/batches/lint.py`), which this slice doesn't edit; they are left for the lead.

## Open items

- **Blind verifier on the reworked versions.** Every version changed, so run one fresh pass of
  `docs/prompts/blind-verifier.md` on `gate/b16r/b16-blind.md` in the session scratchpad (64 versions) and
  reconcile it against `b16-keys.json`. The independent Python re-solve above agreed 64 of 64.
- **Re-gate.** Both rebuilt items are new templates, and the rest changed format or events, so the
  re-gate should cover all 16 in full. Flip `STATUS` in the builder to `reviewed` and rebuild once the
  gate passes.
- **Citations at Subtopic level** where the paragraph couldn't be confirmed: the ASU 2013-06 affiliate
  services rule (ASC 958-605-25) and the conditional and unconditional promise paragraphs (ASC
  958-605-25). Confirm the paragraphs against the Codification if it becomes reachable.
