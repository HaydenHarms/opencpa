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

As drafted, `far-subsequent-events-0020` stated that the cancellation was a recognized subsequent event. That is allowed under quality bar item 5's exception for III.G.b ("calculate adjustments for **identified** subsequent events"), but the review gate pointed out that it made the $0 "disclosure only" distractor answerable by rereading the stem, unlike `-0019`, which leaves the student to infer recognition from the facts. The sentence is now gone from all four versions (see "Review gate").

- **Batch mix:** all four Application, all Area III. (Area III is at 27.4% of the reviewed bank before this batch, inside its 25–35% range, with room to grow; the batch doesn't touch Remembering and Understanding, which stays over its 15% cap pending batches 15-17.)
- **Variants:** 12. Items plus variants: 16.
- **Version-0 key letters:** C, C, B, C. All versions: A 0, B 5, C 11, D 0. The skew is a side effect of every version now carrying the $0 or general-reserve distractor (the $0 choice always sorts first, the general reserve always sorts above the key); the bank-wide position balance absorbs it, but the next batch should lean toward A and D keys.
- **Bank after batch 18:** 322 reviewed FAR MCQs (20.1% toward the 1,600 goal). Every one of the 113 blueprint tasks still has two or more items.

## Process

Each item is a builder function parameterized by company, counterparty, dates and amounts; parameter set 0 rebuilds the reviewed item, sets 1-3 become its variants. Every number, including every distractor, is computed in code with `Decimal`, rounded half up. `finalize()` sorts each item's own choices ascending before `attach_variants()` aligns the variants the same way, and the script asserts the key's letter changes across each family's four versions (it does, for all four: `far-subsequent-events-0019` C/C/B/C, `-0020` C/C/B/C, `far-contingencies-0020` B/B/C/C, `-0021` C/C/C/B, after the review-gate fixes).

`audit()` and the deterministic lint: zero warnings. Four non-blocking notes (`key_in_stem`) on `far-contingencies-0020` and its variants, because the probability scenario necessarily states the key amount's likelihood in the stem (it is one of three given outcomes, not a derived figure) — reviewed and accepted, consistent with how the lint treats this rule elsewhere in the bank. `content:validate` passes (413 files valid, 368 reviewed).

I hand-solved all 16 versions before writing the builder code and again after generating the final YAML, and both checks matched the keys:

- `subsequent-events-0019` (and variants): write-down = receivable balance − amount now expected to be collected ($340,000 − $90,000 = $250,000, key C; v1 $420,000 C; v2 $100,000 B; v3 $110,000 C).
- `subsequent-events-0020` (and variants): impairment loss = carrying amount − confirmed fair value ($460,000 − $150,000 = $310,000, key C; v1 $510,000 C; v2 $180,000 B; v3 $220,000 C).
- `contingencies-0020` (and variants): accrue the single most likely amount among the three given outcomes, not the range minimum, the probability-weighted expected value, or the range maximum ($350,000, key B; v1 $300,000 B; v2 $320,000 C; v3 $260,000 C).
- `contingencies-0021` (and variants): accrue reported-and-unpaid claims plus incurred-but-not-reported claims, both probable and estimable ($180,000 + $95,000 = $275,000, key C; v1 $300,000 C; v2 $230,000 C; v3 $350,000 B).

## Blind verification

One independent verifier (Sonnet, no access to the key or to `content/`) solved all 16 versions from stems and choices only, with every calculation done in Python.

- **`far-subsequent-events-0019`/`-0020` (and all variants): matched the key in every version, clean.** One soft note on `-0019` v3 (distractor B, half of face value) as a "weak but defensible" derivation; no change made.
- **`far-contingencies-0020` (and all variants): the verifier answered with the probability-weighted expected value, not the key (the single most likely amount).** This is a methodology disagreement, not an arithmetic one. Resolved against the verifier: US GAAP (ASC 450-20-55-23 to 55-24, formerly FAS 5 ¶3) measures a loss contingency within a range at the single amount that is a better estimate than any other, or the range minimum if none is; it has no expected-value method for a single obligation (that is an IFRS, IAS 37, convention, not ASC 450-20). The bank's own existing item on this exact rule, `far-contingencies-0007`, is built the same way (its Year 2 remeasurement uses "$720,000 the most likely amount," not a weighted average). Kept the key. Fixed instead: the "expected value" distractor's rationale originally said "GAAP uses the expected value only when no single amount in a range is more likely than any other," which misstated the actual minimum-amount rule; corrected to say GAAP has no expected-value method and uses the minimum when no amount is a better estimate. The key's own explanation now says explicitly that the accrual is not a probability-weighted average.
- **`far-contingencies-0021`: the verifier flagged a real defect.** The fourth distractor (originally "the key amount plus an unexplained $30,000 margin") had no derivation a real student error would produce. Replaced it with a stated fact: the stem now gives a board-approved general contingency reserve for unspecified future claims, and the distractor adds that reserve to the real accrual, a concrete and GAAP-grounded error (ASC 450-20-25 does not permit accruing a general or unspecified business risk). Regenerated all four versions; `audit()` and the lint are still clean, and the keys and other three choices in each version are unchanged.

The batch itself was already on `main` (`654492c`) when the verifier reported back; both fixes went in as a follow-up commit (`a2eb6cb`).

## Review gate

**Result: passed.** One fresh review agent (Sonnet, no access to this report, the builder or the verifier's findings) graded all 16 versions against the quality bar, solving each in Python first and checking the task wording against the 2026 blueprint PDF. Average estimated pass likelihood **87.5%** (batch 14: 86.3%), no wrong keys (all 16 independently re-derived), no second defensible answer, no currency issues, no major-revision items. Nine versions were exam-ready; seven drew minor findings, all applied in a follow-up commit:

1. **`far-subsequent-events-0019`: the base version lacked the family's $0 "disclosure only" distractor**, which all three variants carried, and the "half the balance" distractor maps to no real student error. Dropped "half" from the family; every version now offers $0 (nonrecognized), the expected collection, and the full balance. Made the same change to `-0020`, whose "half the carrying amount" distractor had the same weakness.
2. **`far-subsequent-events-0020`: "This is a recognized subsequent event" in every stem** gave away the $0 distractor and was inconsistent with `-0019`. Removed from all four stems; the facts (the customer's stated intent to cancel before year end) still decide recognition.
3. **`far-contingencies-0021`: the base and v3 lacked the general-reserve distractor** the stem is built to test. Both now carry it ($340,000 and $415,000), replacing the "$0, no insurance" choice. Because the general-reserve choice always sorts above the key, v3 also gets a new distractor (reported claims plus the board's reserve in place of the IBNR estimate, $375,000) so the key letter still varies across versions.

The builder now asserts that every version of each family offers its central-twist distractor (`build(..., twist=...)`), so the gap can't come back. Keys are unchanged in every version. The 12 changed versions were blind-checked again before committing: all 12 matched the key with one defensible answer each. The re-check caught one stem defect the gate had missed, `-0019` v2 saying the customer stopped paying creditors in January of Year 1, before its finances began deteriorating in November; it now says December, Year 1 (no change to the key). Batch-level notes from the reviewer, carried forward rather than fixed here: all 16 versions are single-judgment Moderate items, so the next Area III batch should add multi-step items; and none of the III.B.b items asks for a journal entry, though the task says "prepare journal entries." The reviewer also suggested two quality-bar additions (state the III.G.b exception explicitly; add a review check that every version of a family carries its central-twist distractor).

Full report: kept outside the repo, per the brief.
