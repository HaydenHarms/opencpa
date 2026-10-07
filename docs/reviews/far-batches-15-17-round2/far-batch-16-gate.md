# FAR batch 16: review gate (second gate, after revisions)

Standard: AICPA Uniform CPA Examination Blueprints, effective January 2026. Read only the 16 batch files, docs/content-pipeline.md (Quality bar) and existing content/far items on the same tasks; did not read docs/reviews/, scripts/batches/ or git history. Every key and every distractor in version 0 and all three variants was recomputed (PV factors and amortization tables in Python with Decimal ROUND_HALF_UP). **All 64 keys (16 items x 4 versions) are correct as computed, and all PV factors given in the stems are correct to four places.** Arithmetic is not the problem in this batch. The defects are in scenario logic, giveaways, variant distractor coverage and template reuse.

Currency checks: ASU 2021-09 (private-company risk-free rate election by class of underlying asset; implicit rate still governs when readily determinable): FASB ASU 2021-09 PDF (storage.fasb.org/ASU_2021-09.pdf), Eide Bailly and Journal of Accountancy summaries. ASU 2013-06 (affiliate personnel services recognized at the affiliate's cost, with an option for fair value when cost significantly misstates value): Plante Moran alert. ASU 2018-08 conditional contributions (barrier plus right of return), ASC 842 lease payments (842-10-30-5), ASC 606 royalties exception (606-10-55-65) and constraint (606-10-32-11/12) were checked against my knowledge of the Codification and were not fetched.

## 1. Summary table

| id | my answer | agrees? | difficulty | skill ok? | pass likelihood | p-value | verdict |
|---|---|---|---|---|---|---|---|
| far-fair-value-in-use-0001 | B $180,000 | yes | Moderate | yes (App) | 80% | .70 | minor revision |
| far-fair-value-liability-0001 | A $356,500 | yes | Moderate | yes | 80% | .65 | minor revision |
| far-income-taxes-deferred-0004 | C $57,000 / $45,000 | yes | Easy–Moderate | yes | 83% | .75 | exam-ready |
| far-income-taxes-provision-0004 | C $132,000 | yes | Moderate | yes | 84% | .70 | exam-ready |
| far-income-taxes-provision-0005 | D $24,500 | yes | Moderate | yes | 80% | .60 | minor revision |
| far-lessee-finance-0004 | B $255,012 | yes | Moderate | yes | 81% | .70 | minor revision |
| far-lessee-finance-0005 | C $18,118 / $37,346 | yes | Moderate–Hard | yes | 86% | .55 | exam-ready |
| far-lessee-operating-0006 | A $237,060 | yes | Easy–Moderate | yes | 78% | .72 | minor revision |
| far-lessee-operating-0007 | B $59,000 | yes | Moderate | yes | 76% | .65 | minor revision |
| far-nfp-contributed-services-0003 | B $23,000 / $14,000 | yes | Moderate | yes | 82% | .65 | exam-ready (note) |
| far-nfp-contributed-services-0004 | D $454,000 / $44,000 | yes | Moderate–Hard | yes | 84% | .55 | exam-ready |
| far-nfp-contributions-0003 | C $88,000 | yes | Moderate | yes | 85% | .70 | exam-ready |
| far-revenue-contract-costs-0004 | B $35,000 | yes | Moderate | yes | 82% | .62 | minor revision |
| far-revenue-licenses-0002 | B $26,600 | yes | Moderate | yes | 82% | .62 | minor revision |
| far-revenue-principal-agent-0002 | C $230,000 | yes | Moderate | yes | 78% | .55 | minor revision |
| far-revenue-variable-consideration-0003 | A $320,000 (only if the board hasn't ruled by year end; see findings) | conditionally | Moderate | yes | 60% | .70 | **major revision** |

**Average estimated pass likelihood: 80.3%** (previous gate: 78.2% with 2 major items). There is 1 major item now.

## 2. Findings (items not exam-ready)

### far-revenue-variable-consideration-0003: MAJOR
- **Logic defect that undermines the key.** The bonus depends on the board approving "by December 31, Year 1", and the question asks for Year 1 revenue. The transaction price is updated at each reporting date (ASC 606-10-32-14), and at December 31, Year 1 the deadline has passed, so the outcome is known. The board either approved, which makes revenue $368,000 (choice C), or didn't, which makes it $320,000. The stem never says which, and the president's "coin flip" describes July 1, not the reporting date. A strong candidate sees this, so the key holds only under an unstated assumption. All four versions have the same problem.
- **Fix:** move the decision after the reporting period and say so. For example: "the board will rule at its meeting in April, Year 2, after Larkspur issues its Year 1 financial statements". Make the bonus apply to "every unit shipped in Year 1". Alternatively, keep the December 31 deadline and ask for revenue for the quarter ended September 30, Year 1, with shipments for that quarter.
- **Weak distractor:** D, $960,000 (lifetime units × price), is an error a prepared candidate won't make. Replace it in version 0 with the $0 "defer everything until the board rules" distractor that the variants already use, and keep the 50% expected-value and full-bonus distractors.

### far-fair-value-in-use-0001: minor
- In variants 2 (Rosudgeon) and 3 (Stithian), the standalone dealer price ($100,000 / $70,000) isn't among the choices. The highest-and-best-use facts, which are the item's central twist, then become decoration, and the item reduces to a subtraction. **Fix:** in each variant, replace the "no deduction" choice (D) with the standalone dealer price.
- C and D ("deducts only one of the two deductions") come from the same error family and are weak. "Of comparable utility" is the cost-approach definition wording, so it is a mild giveaway. **Fix:** describe the substitute as "a new machine with the same capacity and features" and keep one partial-deduction distractor.

### far-fair-value-liability-0001: minor
- "A prospective buyer *of Trewince*" reads as an acquirer of the company, not a transferee of the obligation, which makes the distractor's premise confusing. "Assuming the obligation is transferred to a market participant of comparable credit standing" is close to the rule wording that eliminates the stronger-buyer option. **Fix:** "a higher-rated insurer that might assume the obligation said it would price it at a 1.5% premium". Shorten the transfer clause to "measured on a transfer basis under ASC 820".
- Variant 2 (Wendron) drops the stronger-buyer distractor and substitutes a 7-year discounting error, so the buyer fact is decoration there. Its correct value at 6.5% would be $260,414. Variant 3 drops the risk-free-only distractor. **Fix:** every version should carry the stronger-buyer and stale-premium distractors.

### far-income-taxes-provision-0005: minor
- **Template reuse.** This is the third item on the "January 1 and December 31 temporary-difference balances → deferred-tax entry amount" template (provision-0002, provision-0003). The quality bar requires the next item on a task to use a different format. **Fix:** recast it, for example as a draft tax provision entry to correct, or give the deferred tax account balances and ask for taxable income or the valuation-allowance change.
- Variant 1 (Bramhope) sets the valuation allowance at $9,000 against a $9,450 deferred tax asset, which is effectively a full allowance and an odd fact pattern. Its distractor C (treating ending balances as changes, then netting signs) is contrived. **Fix:** keep the allowance under about 50% of the asset, and use the "adds current tax" distractor, which the variants already use, in version 0 as well.

### far-lessee-finance-0004: minor
- **Distractor rationale doesn't match its number, in all four versions.** The annuity-due choice ($272,232; $241,558; $298,168; $238,142) is annuity-due PV **plus** initial direct costs: $263,232 + $9,000 = $272,232. Each rationale states only "$60,000 × 4.3872", which equals $263,232. **Fix:** "Discounts the payments as an annuity due ($60,000 × 4.3872 = $263,232) and adds the $9,000 commission."
- "Due only because the lease was signed" is the initial-direct-cost definition wording (a giveaway), and it repeats the operating-0004 phrasing. **Fix:** give the facts without the test, for example "a $9,000 commission to the broker who found the press, payable on signing", alongside a non-incremental cost such as legal fees for negotiating terms that the candidate must exclude.

### far-lessee-operating-0006: minor
- **The risk-free election is decoration.** Only one rate is given, so the election changes nothing and the policy sentence just supplies the answer's rate. **Fix:** also give the incremental borrowing rate (for example 7%, with its annuity factors), so the election must be applied. A distractor at the IBR then maps to "ignores the election".
- C ($278,527) combines two errors: ordinary annuity and no deduction of the paid rent. **Fix:** use the single-error number, 5 payments × the ordinary-annuity factor taken as the remaining payments. Note that this coincides with the key, so instead use the "deducts the deposit" distractor, which variants 1 and 3 already carry.
- The scenario is close to operating-0004 (annuity due with first payment at commencement and an incentive or initial direct cost). That is acceptable once the election matters.

### far-lessee-operating-0007: minor
- **Giveaway:** "a variable payment that isn't fixed or tied to an index" states the classification the candidate must make, namely that it is excluded from lease payments. **Fix:** "reimburses the landlord for its pro-rata share of the property taxes actually assessed each year", with no label.
- **Template reuse:** this is the third "What total lease cost should X recognize for Year 1?" item on operating leases (operating-0003, operating-0005). **Fix:** change the ask. For example, ask for the right-of-use asset carrying amount at December 31, Year 1 (liability plus straight-line plug, with the incentive), or for the Year 1 increase in straight-line accrued rent.
- The explanation asserts "Inkberrow uses the space evenly", which isn't in the stem. Add it to the stem or remove it from the explanation.

### far-revenue-contract-costs-0004: minor
- **An amount stands for two facts.** In variant 2 (Zennor), choice D is $43,200 and the pallet jacks cost $43,200. In variant 3 (Marazion), choice B is $18,000 and the packaging supplies cost $18,000. **Fix:** change the equipment or supplies amounts, for example pallet jacks $46,800 and packaging supplies $16,200.
- "The contract's fee schedule includes a setup charge" may lead some candidates to treat the setup as a separate performance obligation, which would expense the labor as the obligation is satisfied. **Fix:** "the setup gives the customer nothing it can use on its own; the monthly fees are priced to recover it". This is facts, not the test.
- The policy "amortizes ... over the period of the services it relates to" nearly answers the start-date distractor (C). That is acceptable but weak.

### far-revenue-licenses-0002: minor
- In variant 2 (Ivymoor), one quarter of projected sales ($880,000 ÷ 4 = $220,000) equals the franchisee's actual Q1 sales of $220,000. The distractor B rationale "8% × $220,000" then reads as if it used the franchisee's figure. **Fix:** change the projection, for example to $920,000 (giving $230,000).
- Version 0 lacks the "quarter of the projection" distractor that all variants carry. That isn't required, but it would replace the weaker D ($83,600, the full-year projection booked up front).
- The template is close to licenses-0001 (a functional-IP license paired with a brand franchise license, revenue for the period). The royalty mechanics differ, so it is acceptable, but the next licenses item must use a different format.

### far-revenue-principal-agent-0002: minor
- **Variant 3 (ZipFleet) has no gross-reporting distractor** ($430,000 + $45,000 = $475,000), even though gross versus net is the item's central twist. Variant 1 (SwiftHail) keeps it but drops the "omits commission" choice. **Fix:** every version carries the gross distractor. Drop the "keeps the driver's 75%/78%" choice, which no prepared candidate makes.
- **Template reuse with principal-agent-0001:** one agent stream plus one principal stream, asking for total revenue. **Fix (preferred):** change the format for this item, for example by asking how much revenue BrightRide reports from rides. Add a fact that genuinely tests control, such as a promotion BrightRide funds, a rider refund it pays, or driver incentives, so the price-setting indicator is weighed against more than one fact.
- The agent conclusion is defensible (it is consistent with how ride-hailing platforms report), but price-setting together with collection pulls some candidates to gross. That is acceptable as the twist.

### Exam-ready items: notes only
- **far-income-taxes-deferred-0004:** variant 2 (Ulverscroft) drops the "current portion only" distractor, the item's twist, for "adds the allowance" ($90,000), which is implausible. Restore it. "Net of the allowance" in the ask makes D (no deduction) weak.
- **far-income-taxes-provision-0004:** the COLI death benefit is excluded only if the IRC §101(j) notice-and-consent rules are met. Add "a policy that meets the tax law's requirements for excluding the proceeds". The installment-sale event and the 25% rate echo deferred-0004 in the same batch.
- **far-lessee-finance-0005:** reuses the 6%/5-period factor pair 4.2124/0.7473 from finance-0002. Say "a new machine with a 10-year useful life from commencement".
- **far-nfp-contributed-services-0003:** the stem template (a list of donated services) is the same as contributed-services-0001 and -0002. The paired revenue-and-expense ask with capitalization is a real change of ask, so I pass it, but the next item on this task must change format, for example to a journal entry or a statement-of-activities line.
- **far-nfp-contributed-services-0004:** cite the affiliate-services paragraphs as Subtopic 958-605 only, which the file already does. Good item.
- **far-nfp-contributions-0003:** this is the second "total contribution revenue from a list" item with contributions-0002, so the next item on this task needs a different format.

## 3. Batch-level assessment

- **Skill mix:** 16 of 16 are Application. That is honest: every topic here (fair value, income taxes, lessee accounting, revenue, NFP contributions) has no Analysis task in the 2026 blueprint. It pushes the bank's Application share up and the Remembering and Understanding share down, which serves the stated goal of getting R&U under 15%. Analysis must come from Area I and II batches.
- **Area mix:** 16 of 16 are in Area III, as the batch was designed. Bank-level balance has to come from other slices.
- **Topic tally:** revenue recognition 7 (4 under ASC 606, 3 NFP), lessee accounting 4, income taxes 3, fair value 2. Lessee and income-tax tasks are now thick, and template reuse is starting to appear there (operating-0007, provision-0005). Thin or missing Area III tasks worth filling next include foreign-currency transactions, the NOL and rate-change items (one each), and subsequent events.
- **Difficulty:** about 11 of 16 are multi-step (2–4 judgments or adjustments), which meets the at-least-half requirement. Easiest: deferred-0004 and operating-0006.
- **Average pass likelihood:** 80.3%, against 78.2% at the first gate. One major item remains (variable-consideration-0003), so **the batch does not yet pass the gate** under the "no major-revision items" rule. The average sits just above the ~80% bar.

### Ten changes that would most improve the batch (ranked)
1. variable-consideration-0003: move the board's decision after the reporting date, or change the period asked, and replace the lifetime-units distractor with $0.
2. principal-agent-0002: put the gross-reporting distractor in every variant and change the ask or format away from the principal-agent-0001 template.
3. operating-0007: remove the "isn't fixed or tied to an index" label and change the ask away from "total lease cost for Year 1".
4. operating-0006: give an IBR as well, so the risk-free election matters.
5. fair-value-in-use-0001: put the standalone-price distractor in variants 2 and 3.
6. fair-value-liability-0001: reword "buyer of Trewince" as a potential transferee, and keep both credit-standing distractors in every variant.
7. provision-0005: change format (third use of the beginning/ending-balance template) and fix variant 1's near-full allowance.
8. finance-0004: make the annuity-due rationales state the +IDC step, and drop the IDC definition wording.
9. contract-costs-0004 and licenses-0002: remove the amount collisions in variants (Zennor $43,200, Marazion $18,000, Ivymoor $220,000).
10. deferred-0004 variant 2 and provision-0004: restore the twist distractor, and add the §101(j) qualifier.

## 4. Suggested additions to the quality bar
- **Timing of resolution versus the reporting date:** for any contingency or variable-consideration item, the uncertainty must still be unresolved at the reporting date asked about, or the stem must say how it resolved.
- **Twist coverage in variants, not only version 0:** every variant carries the central-twist distractor. Several variants here swap it for a weaker error (in-use v2/v3, liability v2, principal-agent v3, deferred v2).
- **Amount collisions across choices and stem:** extend "no amount stands for two facts" to choices. A choice must not equal an unrelated stem amount, and the audit could check this mechanically.
- **Elections must bite:** a stated election (risk-free rate, practical expedient) should change the key against at least one choice. Otherwise it is decoration, or the policy sentence is the solution.
- **Rationale arithmetic:** audit that each distractor rationale's stated computation evaluates to the choice's number. The finance-0004 annuity-due rationales would fail that check.

Sources: [FASB ASU 2021-09](https://storage.fasb.org/ASU_2021-09.pdf); [Eide Bailly on the ASC 842 risk-free rate election](https://www.eidebailly.com/insights/articles/2021/12/accounting-policy-election-to-use-the-risk-free-rate-in-asc-842-lessees); [Journal of Accountancy, Nov 2021](https://www.journalofaccountancy.com/news/2021/nov/fasb-risk-free-rate-rule-cut-costs-nonpublic-lessees/); [Plante Moran on ASU 2013-06](https://www.plantemoran.com/explore-our-thinking/insight/2013/04/alert--fasb-issues-asu-201306--impacts-accounting-for-services-received-fro).
