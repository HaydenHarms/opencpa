# FAR batch 17 — review gate, second pass (after the rebuild)

Reviewer: independent review agent, following `docs/prompts/review-agent.md`. Standard: the AICPA _Uniform CPA Examination Blueprints_, effective January 2026. I could not open the PDF from this session (the egress proxy refused assets.ctfassets.net), so I checked task matches and skill marks against the task map in `scripts/far-coverage.py` (III.A.a/b, III.B.b/c, III.G.b/c) and the pipeline quality bar. Treat the skill-mark checks as provisional until someone confirms them against the PDF.

Scope: all 16 items in full, each with its three variants (64 versions). I solved every version and every distractor in code (`scratchpad/solve.py`, Decimal ROUND_HALF_UP) before reading the keys. **No wrong keys in any version.** Every distractor number reproduces from the error its rationale names. Previous score: 62.0% with 5 major items.

Currency checks:

- **ASU 2025-05**: confirmed from FASB ([ASU 2025-05 PDF](https://storage.fasb.org/ASU%202025-05.pdf)) and firm summaries ([Crowe](https://www.crowe.com/insights/take-into-account/fasb-simplifies-credit-loss-accounting-for-accounts-receivable-and-contract-assets), [EisnerAmper](https://www.eisneramper.com/insights/pcs/fasb-asu-2025-05-streamlines-credit-loss-estimation-1025/)).
  - The practical expedient lets an entity assume that balance-sheet-date conditions persist over the remaining life of current AR and contract assets under ASC 606.
  - Only entities other than PBEs that elect the expedient may also elect to consider collections after the balance sheet date.
  - Effective for annual periods beginning after December 15, 2025, with early adoption permitted.
  - Subsequent-events-0015 and -0016 both state that the entity has not elected the expedient, which also rules out the collections election. That is correct and sufficient.
- **ASC 330-10-35-17**: "measured in the same way as are inventory losses" (text confirmed via [PwC Viewpoint](https://viewpoint.pwc.com/content/pwc-madison/ditaroot/us/en/pwc/accounting_guides/utilities_and_power_/utilities_and_power__US/chapter_11_inventory_US/113_firm_purchase_co_US.html)). After ASU 2015-11, an entity on FIFO or average cost measures inventory losses at NRV, so contingencies-0016 has a small currency gap (see below).
- **SEC SAB Topic 4C**: stock dividends and splits after the balance sheet date get retroactive effect for registrants only. Subsequent-events-0018 handles this correctly.

## 1. Summary table

| id                           | my answer (v0)     | agrees?         | difficulty                  | skill tag ok?                  | pass likelihood | p-value | verdict               |
| ---------------------------- | ------------------ | --------------- | --------------------------- | ------------------------------ | --------------- | ------- | --------------------- |
| far-accounting-errors-0010   | C $688,800         | yes (v1–v3 too) | Moderate–Hard (3 judgments) | Analysis ok; area questionable | 84%             | 0.50    | exam-ready (tag note) |
| far-accounting-errors-0011   | D $1,934,000       | yes             | Moderate                    | Analysis ok; area questionable | 78%             | 0.55    | minor                 |
| far-accounting-errors-0012   | B $2,338,000       | yes             | Moderate                    | Analysis ok; area questionable | 76%             | 0.55    | minor                 |
| far-change-in-estimate-0003  | C $351,000         | yes             | Moderate                    | Application ok                 | 84%             | 0.65    | exam-ready            |
| far-change-in-principle-0003 | A $586,250         | yes             | Moderate                    | Application ok                 | 78%             | 0.55    | minor                 |
| far-contingencies-0015       | A $225,000         | yes             | Moderate                    | Application ok                 | 78%             | 0.60    | minor                 |
| far-contingencies-0016       | A $41,400          | yes             | Moderate                    | Application ok                 | 78%             | 0.60    | minor                 |
| far-contingencies-0017       | A $268,906         | yes             | Moderate                    | Application ok                 | 74%             | 0.60    | minor                 |
| far-contingencies-0018       | B $133,000         | yes             | Moderate                    | Analysis ok                    | 80%             | 0.55    | minor                 |
| far-contingencies-0019       | C $310,000         | yes             | Easy                        | Analysis (weak)                | 72%             | 0.80    | minor                 |
| far-error-correction-0001    | B $37,800 decrease | yes             | Easy–Moderate               | Application ok                 | 83%             | 0.65    | minor (typo)          |
| far-subsequent-events-0014   | B $272,640         | yes             | Moderate                    | Application ok                 | 85%             | 0.55    | exam-ready            |
| far-subsequent-events-0015   | D $1,714,000       | yes             | Easy–Moderate               | Application ok                 | 62%             | 0.70    | **major** (duplicate) |
| far-subsequent-events-0016   | B $1,205,000       | yes             | Moderate                    | Analysis ok                    | 79%             | 0.55    | minor                 |
| far-subsequent-events-0017   | C $8,422,000       | yes             | Moderate                    | Analysis ok                    | 83%             | 0.55    | exam-ready            |
| far-subsequent-events-0018   | C $1,273,750       | yes             | Moderate                    | Analysis ok                    | 82%             | 0.50    | exam-ready            |

**Average estimated pass likelihood: 78.5%** (first gate: 62.0%). That is a +16.5-point gain, but still just below the ~80% bar, with **1 major item** (first gate: 5).

Every item has four choices, numeric choices ascend in all versions, the key letter moves across versions, and every item has a key-letter variety check.

## 2. Findings per item not exam-ready

### far-subsequent-events-0015 — MAJOR

- **Defect: duplicate concept and number structure.** The central event is already in the bank twice.
  - The event: a customer whose finances deteriorated through the year files for bankruptcy after year-end, the entity now expects to collect $X, and the allowance already holds $Y for that customer, so the charge is balance − expected collection − existing allowance.
  - It appears as subsequent-events-0002 event (1) (owed $80,000, collect $20,000, allowance $10,000) and as subsequent-events-0008 (Pryce Foods, collect 30%, allowance $12,000).
  - The second event, a cash dividend declared after year-end, is in 0004, 0007, 0010 and 0011.
  - The task has well over three items, so quality bar item 8 requires at least two component events to change. This item changes none.
- The dividend distractor (A, deduct the dividend from pretax income) does not map to a subsequent-events error. The explanation itself says "a dividend isn't an expense in any case."
- **Fix:** rebuild with two events new to the task.
  - One option: a December sale whose customer pays in February, while another customer's credit deteriorated after year-end because of a post-year-end event. Ask for the allowance or the credit loss expense under a stated election of the ASU 2025-05 expedient and, for a private company, the collections election. This tests the new ASU directly.
  - Another option: inventory NRV evidence from a post-year-end sale, or a bonus or royalty measured on Year 1 results.
  - Replace the dividend distractor with an error a candidate actually makes, such as recognizing a post-year-end, nonrecognized loss.

### far-accounting-errors-0011 — minor

- **Blueprint/area:** this is a current-year draft corrected before issuance. Under ASC 250 an "error" is an error in previously issued statements, so this is really Area I "Balance sheet — detect, investigate and correct discrepancies" (Analysis), or Area II payables. The same applies to 0010 and 0012. **Fix:** retag to the Area I balance-sheet Analysis task, or re-frame as an error in the issued prior-year balance sheet found this year and ask for the comparative or restated amount.
- **Distractor B "accepts the draft total"** (v0, v2) combines two errors at once (keeping the PO and omitting the dividend). **Fix:** replace it with "computes the dividend on issued shares", which is $1,943,000 in v0 (v1 and v2 already use this).
- The stem says Thistlewood "records dividends when it pays them." Acceptable as a found error, but it signals the error. **Fix (optional):** drop the sentence and say only that no entry has been made for the declaration.

### far-accounting-errors-0012 — minor

- **Third use of one template on the task.** 0010, 0011 and 0012 share a frame: "draft total; the controller reviews three items; one is correctly recorded and acts as a decoy; give the corrected total." Quality bar item 8 says the third item on a shared template uses a different format. **Fix:** change 0012's format.
  - One option: ask for the effect on Year 2 net income and on total assets as a pair.
  - Another: make one of the three a prior-period error that goes to opening retained earnings.
- **Implausible distractor:** "full year of interest" on a 6-month note (v1 D $2,063,000, v2 C $3,129,600). No candidate accrues 12 months on a 6-month note. **Fix:** use the whole-term accrual (v1 $2,039,000, v2 $3,100,800), or the at-cost distractor where it isn't already used.
- **v3:** C (whole 9-month term) and D (full year) are the same error family, side by side. The 9-month interest ($27,000) also equals the fair-value gain ($27,000), so one amount stands for two facts in the rationales. **Fix:** drop D and use at-cost ($1,558,000). Change the FV gain so it doesn't equal any interest amount (for example, $207,000 → $211,000).
- Same area/tag note as 0011.

### far-accounting-errors-0010 — exam-ready, with a tag note

- A strong item: three entries, one a correctly recorded decoy, and no stated conclusions. The only issue is the same Area I vs III tag question as 0011.

### far-change-in-principle-0003 — minor

- **Partial giveaway:** "bonuses for prior years were based on income as originally reported and will not be recalculated" tells the candidate the bonus doesn't change. That removes most of the pull of distractor B (recompute the bonus), and the indirect-effects rule (ASC 250-10-45-8) is the item's twist. **Fix:** delete that clause. State only that the plan pays 10% of income before the bonus and taxes, and let the candidate apply 45-8 (indirect effects are not included in the restated periods; any actually incurred are recognized in the period of change). The key is unchanged.
- v0's C ("uses the Year 2 change") is fine. Consider swapping in "applies the cumulative difference" ($522,500 in v0), which v1 and v3 already use, so that v0 carries the cumulative-effect error, the classic wrong treatment.

### far-contingencies-0015 — minor

- **Version 0 lacks a distractor for the central twist:** accruing nothing for the unasserted recall claims. That gives $165,000, which v1–v3 carry. v0's B and D are both "wrong point in the range," a clustered error family. **Fix:** replace D ($305,000, top of range) with $165,000.
- The wording "customers are expected to file claims that Oldcastle will have to pay" comes close to stating the probability conclusion. The bank has accepted it before (contingencies-0005). **Fix (optional):** give evidence instead, for example "312 customers have reported damage to the company's hotline; in two earlier recalls, Oldcastle paid nearly every reported claim."

### far-contingencies-0016 — minor

- **Currency (ASU 2015-11):** ASC 330-10-35-17 measures commitment losses "in the same way as inventory losses." For a FIFO or average-cost entity, that means NRV, not the replacement market price. 35-18 also excludes losses protected by firm sales contracts. **Fix:** add "Harmondsgate uses FIFO; the yarn could be sold for no more than the $4.05 market price, and no firm sales contracts cover the goods it will make from it." That makes the decline a measured loss under either reading.
- **Weak distractor:** D, "treats the whole contract price ($192,000) as the liability," is implausible for a prepared candidate. **Fix:** use the "all buyers claim" error (already C), and for D use "measures the commitment loss at the decline times the quantity still to be delivered after deducting the rebate…". Better still, use a real error: record the rebate as a selling expense with no liability for unpaid claims. That gives $30,000 in v0, already a distractor in v1–v3 as "accrues nothing for rebates."
- The rebate leg is ASC 606 content. Acceptable on a contingencies/commitments item, but note it in the topic tally.

### far-contingencies-0017 — minor

- **The policy is the solution:** "because the amounts and dates are fixed, Cranmoor's policy is to discount such payments, and it uses 6%." With that stated, B (face amount) is only "ignored the stem." **Fix:** keep the election, which is needed, but put the difficulty elsewhere. For example, schedule the deferred payment for 18 months, or make it two later installments, so the PV computation carries the weight. Or drop discounting and add a judgment, for example an insurer's confirmed reimbursement that must be shown gross.
- **Weak distractors:** "leaves out the $160,000/$210,000 due within 30 days" (v1, v3 A) and "compounds forward" (v0 C, v2 C, v3 D) are not common errors. **Fix:** use "omits IBNR" (v0 $242,906) in every version, and "discounts the 30-day payment too."
- **Citation:** ASC 835-30 does not govern a litigation settlement, and SAB Topic 5Y (ASC 450-20-S99-1) applies to SEC registrants; the stem doesn't say whether Cranmoor is one. **Fix:** cite ASC 450-20-S99-1, and for non-registrants ASC 410-30-35-12 by analogy. Alternatively, say Cranmoor is an SEC registrant.

### far-contingencies-0018 — minor

- A good item: the agency's consistent history and published schedule are evidence, not a stated conclusion.
- **Template shared with 0019** in the same batch, and with contingencies-0008(2), -0009(4) and -0013: the second matter is "a claim with a dollar demand; counsel can't assess; accrue nothing; the demand is a distractor." **Fix:** in one of 0018 and 0019, replace the second matter with something that requires a different judgment, for example a reasonably possible loss with an estimate, which is disclosed but not accrued, or a remote guarantee.
- **v1 and v2 C** ("accrues the demand and nothing for the discharges") combine two errors, and those versions lose the $0 central-twist distractor that v0 and v3 have. **Fix:** use $0 in every version, and for the fourth slot use "accrues the statutory maximum plus nothing else" (already present).

### far-contingencies-0019 — minor

- **Easy, and close to a giveaway:** counsel "names $310,000 as the best estimate within that range," and the other matter is "too early to gauge either the outcome or the exposure." The candidate only has to recognize that a best estimate beats the minimum, which is weak for an Analysis tag. The concept duplicates contingencies-0008(1) and -0013 (most likely amount within a range).
- **Fix:** make the indemnity the judgment.
  - Give the consultant's cost scenarios with probabilities, or a most-likely amount that exceeds the $420,000 indemnity cap, so the cap limits the accrual.
  - Replace the whistleblower matter with something other than another "too early" claim (see 0018).
  - Add an ASC 460 reference (460-10-35, the contingent liability under ASC 450 once probable). The "fair value immaterial at inception" sentence points there.

### far-error-correction-0001 — minor (typo only)

- v3 explanation: "The 1 months of Year 3 interest through February 1." **Fix:** "The 1 month."
- Optional: v0 lacks the pretax distractor ($50,400) that the variants carry, and v0's A (Year 1 only) is the weakest of its distractors. Consider swapping.

### far-subsequent-events-0016 — minor

- **Template reuse:** "draft balance-sheet figure, three post-year-end events, an add-on liability from a settlement above the accrual, and a customer loss caused after year-end" repeats subsequent-events-0010 (total liabilities) and -0007 (current ratio). The sales-tax assessment and the regulation-driven default are new, so the event-change rule is met. **Fix (optional):** change the ask, for example the amount to disclose versus recognize, to move away from the "corrected total" template.
- **v1–v3 D "accepts the draft balances"** combines two errors. **Fix:** "writes off the receivable" (already A in v0, v2, v3) plus a single-error item.
- **v3:** "Greystoke Imports … cut off its export business" is inconsistent. **Fix:** rename the customer (for example, "Greystoke Exports"). v1's "customs-tariff order … cut off its export business" reads oddly. Use "export-licensing" or "trade-sanctions" wording.

## 3. Batch-level assessment

- **Keys:** 64/64 versions correct; every distractor reproduces from its named error.
- **Skill mix (this batch):** Analysis 8 (50%), Application 8 (50%), Remembering and Understanding 0.
  - The batch is one Area III slice of batches 15–17, so its own mix is not judged against the section ranges. It does help pull Remembering and Understanding back under 15%, as the plan intends.
  - The tags match the repo task map: III.A.a/b, III.B.b/c, III.G.b/c.
  - Contingencies-0019 sits weakest as Analysis, because the evidence states its own conclusions.
- **Area mix:** 16/16 Area III. That is acceptable for a slice, but accounting-errors-0010 to -0012 are current-year draft corrections that fit the Area I balance-sheet and income-statement "detect, investigate and correct" tasks better. Retagging them would move 3 items to Area I, where the bank is meant to carry 30–40%.
- **Topic tally:**

  | Topic                                    | Items                                                            |
  | ---------------------------------------- | ---------------------------------------------------------------- |
  | Accounting changes and error corrections | 6 (errors 3, estimate 1, principle 1, prior-period correction 1) |
  | Contingencies and commitments            | 5                                                                |
  | Subsequent events                        | 5                                                                |
  - Over-represented: the "draft total, several events, corrected total" frame. It runs through 0010–0012 and subsequent-events 0015–0018, and through 0007 and 0010–0013 of the existing bank.
  - Missing in this slice: change in reporting entity, a change in principle that is impracticable to apply retrospectively (prospective, as with a change to LIFO), and the disclosure-only side of subsequent events (which events need disclosure, and of what).

- **Average pass likelihood:** 78.5% versus 62.0% at the first gate. Major items fell from 5 to 1. **The gate is not yet passed** because of subsequent-events-0015. Fixing it, plus the ten changes below, should move the batch to ~82%.

**Ten changes that would most improve the batch, ranked:**

1. Rebuild subsequent-events-0015 with two events new to III.G (it duplicates subsequent-events-0002 and -0008).
2. Change 0012's format (the third use of the accounting-errors "three entries, one decoy" template), and retag 0010–0012 to Area I or re-frame them as errors in issued statements.
3. Contingencies-0019: make the indemnity a real measurement judgment (cap, scenarios), not a named "best estimate."
4. Split the shared "too early to assess; demand amount as distractor" second matter between contingencies-0018 and -0019.
5. Change-in-principle-0003: delete "will not be recalculated" so the indirect-effects rule carries the item.
6. Contingencies-0017: put the difficulty in the PV computation, replace the "leaves out the 30-day payment" and "compounds forward" distractors, and fix the ASC 835-30 citation.
7. Contingencies-0016: state FIFO/NRV and the absence of protecting sales contracts (ASU 2015-11 measurement), and replace the "whole contract price" distractor.
8. Contingencies-0015 v0: add the "nothing for unasserted claims" distractor in place of the second range-point distractor.
9. Accounting-errors-0012 v1/v2/v3: replace "full year of interest" on 6-month notes, and remove the $27,000 coincidence in v3.
10. Replace every "accepts the draft" double-error distractor: accounting-errors-0011 v0/v2, accounting-errors-0012 v1, subsequent-events-0016 v1–v3. Also fix the small text slips ("1 months", "Greystoke Imports … export").

## 4. Suggested changes to the quality bar

- **Count a task's existing event set before drafting.** Add to item 8: "List every event used by the existing items on the task (from `far-coverage.py`'s map) and show in the builder notes which two events are new." Subsequent-events-0015 slipped through with zero new events.
- **"Accepts the draft" is a two-error distractor** whenever the key changes more than one line. Add it to the list of distractors to avoid unless the draft differs from the key by exactly one item.
- **Current-year draft vs ASC 250 error.** Add to item 1: a draft corrected before issuance is an Area I "detect, investigate and correct discrepancies" item, not an Area III "error correction" item, unless at least one error sits in previously issued statements.
- **ASU 2015-11 and purchase commitments.** Add to item 9: commitment-loss items state the cost-flow method (or that NRV equals the market price), since ASC 330-10-35-17 measures the loss like inventory losses.
- **Duration-consistent distractors.** A "full year" accrual distractor is only allowed when the instrument's term is at least a year.
- **Stated "best estimate."** Naming the best estimate is acceptable in Application items. In Analysis items, the evidence should let the candidate pick the best estimate rather than state it.
