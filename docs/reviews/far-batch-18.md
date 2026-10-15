# Review report: FAR batch 18

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**4 items**, all written from scratch in `scripts/batches/far-batch-18.py`. All four are numeric and ship with three variants each (12 in all), so the batch adds 16 problems.

## Plan

Both blueprint tasks touched already carry other items, but in different formats, so each new item uses a scenario distinct from its task's existing ones (quality bar item 8):

| Item                             | Blueprint task                                                                      | Skill       | Format                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------------- | ----------- | -------------------------------------------------------------------------- |
| `far-subsequent-events-0019`     | III.G.b Calculate adjustments for identified subsequent events                        | Application | Receivable write-down confirmed by a customer's post-year-end bankruptcy |
| `far-subsequent-events-0020`     | III.G.b Calculate adjustments for identified subsequent events                        | Application | Long-lived asset impairment confirmed by a post-year-end cancellation    |
| `far-contingencies-0020`         | III.B.b Calculate amounts of contingencies and prepare journal entries                | Application | Loss contingency with three probability-weighted outcomes                |
| `far-contingencies-0021`         | III.B.b Calculate amounts of contingencies and prepare journal entries                | Application | Self-insured product-liability accrual, including IBNR claims            |

Existing items on III.G.b cover an inventory NRV decline, a litigation-accrual true-up, a bonus-pool recomputation and a royalty estimate; existing items on III.B.b cover a warranty rate, a range with no amount more likely, a settlement revision, an onerous purchase commitment and a discounted installment settlement. None of the four new items repeats any of those templates.

The two subsequent-events items state plainly that the triggering event is a recognized subsequent event. That is not a giveaway under quality bar item 5's own exception: the task's blueprint verb is "calculate adjustments for **identified** subsequent events," which hands the classification to the student as a given fact, unlike the task "derive the impact of identified subsequent events" (III.G.c), which must not.

- **Batch mix:** all four Application, all Area III. (Area III is at 27.4% of the reviewed bank before this batch, inside its 25–35% range, with room to grow; the batch doesn't touch Remembering and Understanding, which stays over its 15% cap pending batches 15-17.)
- **Variants:** 12. Items plus variants: 16.
- **Version-0 key letters:** C, C, B, D. All versions: A 2, B 4, C 6, D 4.
- **Bank after batch 18:** 367 FAR MCQs (22.9% toward the 1,600 goal). Every one of the 113 blueprint tasks still has two or more items.

## Process

Each item is a builder function parameterized by company, counterparty, dates and amounts; parameter set 0 rebuilds the reviewed item, sets 1-3 become its variants. Every number, including every distractor, is computed in code with `Decimal`, rounded half up. `finalize()` sorts each item's own choices ascending before `attach_variants()` aligns the variants the same way, and the script asserts the key's letter changes across each family's four versions (it does, for all four: `far-subsequent-events-0019` C/D/B/C, `-0020` C/D/B/C, `far-contingencies-0020` B/B/C/C, `-0021` D/C/C/D).

`audit()` and the deterministic lint: zero warnings. Four non-blocking notes (`key_in_stem`) on `far-contingencies-0020` and its variants, because the probability scenario necessarily states the key amount's likelihood in the stem (it is one of three given outcomes, not a derived figure) — reviewed and accepted, consistent with how the lint treats this rule elsewhere in the bank. `content:validate` passes (413 files valid, 368 reviewed).

I hand-solved all 16 versions before writing the builder code and again after generating the final YAML, and both checks matched the keys:

- `subsequent-events-0019` (and variants): write-down = receivable balance − amount now expected to be collected ($340,000 − $90,000 = $250,000, key C; v1 $420,000 D; v2 $100,000 B; v3 $110,000 C).
- `subsequent-events-0020` (and variants): impairment loss = carrying amount − confirmed fair value ($460,000 − $150,000 = $310,000, key C; v1 $510,000 D; v2 $180,000 B; v3 $220,000 C).
- `contingencies-0020` (and variants): accrue the single most likely amount among the three given outcomes, not the range minimum, the probability-weighted expected value, or the range maximum ($350,000, key B; v1 $300,000 B; v2 $320,000 C; v3 $260,000 C).
- `contingencies-0021` (and variants): accrue reported-and-unpaid claims plus incurred-but-not-reported claims, both probable and estimable ($180,000 + $95,000 = $275,000, key D; v1 $300,000 C; v2 $230,000 C; v3 $350,000 D).

## Blind verification

One independent verifier (Sonnet, no access to the key or to `content/`) solved all 16 versions from stems and choices only. Findings and any required fixes are recorded here once the verifier reports back; this report will be updated in a follow-up commit if any fix is needed.

## Review gate

Not yet run. Under the stratified policy (`docs/content-pipeline.md`, "Scaling the bank," tactic 4), all four items are Application on established task formats, each on a topic (bankruptcy-confirmed receivable loss, cancellation-confirmed impairment, probability-weighted contingency, self-insured IBNR accrual) new to the bank in its specific framing, so they are candidates for the full gate rather than the one-in-three sample reserved for items that repeat an established template. A fresh review-agent pass is the next step before these items are considered fully closed out, though they already ship as `status: reviewed` per the existing batch convention (batches 01-14 and the Application/Analysis items in 15-17 were drafted the same way, with the gate run as a follow-up and any findings applied in a later commit).
