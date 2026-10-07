# FAR batch 15: review gate, second pass (after rebuild)

- Reviewer: fresh review agent following `docs/prompts/review-agent.md`. I did not read `docs/reviews/`, `scripts/batches/` or git history before writing these findings.
- Standard: AICPA *Uniform CPA Examination Blueprints*, effective January 2026. The PDF host (assets.ctfassets.net) is blocked by this session's egress proxy, so task wording and skill marks come from the repo's transcription in `scripts/far-coverage.py` (II.A.b, II.A.c, II.B.c, II.C.c, II.D.f, II.F.c, II.G.c, II.H.1c, II.H.2a).
- Scope: 13 batch items (all `status: draft`), each graded in full with all three variants, plus the live item `far-intangibles-cloud-computing-0001` (key recently corrected), reported separately.
- Method: I solved every version (13 × 4 + 4 = 56 versions) in code (`solve.py` in this folder, Decimal half-up) from stems and choices only, then compared with the keys. I recomputed every distractor and every stated balance: rollforward identities, the stated reconciliation difference, and bond PVs against the allocated carrying amounts.
- Previous score: first gate 47.4% average, with 8 major items.

## 1. Summary table (13 batch items)

| id | my answer | agrees with key? | difficulty | skill tag ok? | pass likelihood | p-value | verdict |
|---|---|---|---|---|---|---|---|
| far-bonds-premium-0002 | C $51,937 (variants B, C, B) | yes, all 4 versions | Moderate–Hard (allocate, 2 interest periods, accrual) | yes (App, II.H.1c) | 76% | 0.55 | minor revision |
| far-cash-bank-reconciliation-0006 | C $49,050 (D, C, C) | yes, all 4 | Moderate (5 items, 2-sided) | yes (Ana, II.A.b) | 78% | 0.60 | minor revision |
| far-cash-bank-reconciliation-0007 | B $53,440 (A, B, B) | yes, all 4 | Moderate (5 items) | yes (Ana, II.A.b) | 78% | 0.55 | minor revision |
| far-cash-unreconciled-0004 | B $1,860 (B, C, C) | yes, all 4 | Moderate–Hard (3 corrections, then a residual) | yes (Ana, II.A.c) | 84% | 0.50 | exam-ready |
| far-cash-unreconciled-0005 | C $1,250 understated (C, B, B) | yes, all 4 | Hard (4 items, double-effect misposting, direction) | yes (Ana, II.A.c) | 82% | 0.45 | exam-ready |
| far-debt-covenant-0003 | B $750,000 (C, B, C) | yes, all 4 | Moderate (3 definition judgments) | yes (App, II.H.2a) | 86% | 0.60 | exam-ready |
| far-exit-costs-0003 | B $900,000 (C, B, C) | yes, all 4 | Moderate–Hard (4 ASC 420 judgments) | yes (App, II.G.c) | 80% | 0.50 | minor revision |
| far-intangibles-cloud-computing-0002 | B $288,000 (C, A, C) | yes, all 4 | Hard (4 judgments, 2 amortization periods) | yes (App, II.F.c) | 80% | 0.40 | minor revision |
| far-inventory-rollforward-0006 | B $1,413,000 (A, B, B) | yes, all 4 | Moderate (4 cutoff/classification judgments) | yes (Ana, II.C.c) | 84% | 0.55 | exam-ready |
| far-inventory-rollforward-0007 | C $11,000 increase (B, C, B) | yes, all 4 | Moderate (3 judgments, 1 allocation) | questionable: no rollforward in the stem | 76% | 0.55 | minor revision |
| far-ppe-rollforward-0006 | C $630,500 (C, B, C) | yes, all 4 | Moderate (4 judgments) | yes (Ana, II.D.f) | 85% | 0.55 | exam-ready |
| far-receivables-rollforward-0006 | C $516,000 (C, D, C) | yes, all 4 (assuming no transferred account was collected) | Hard (ASC 860, bill-and-hold, a netting decoy) | yes (Ana, II.B.c) | 66% | 0.45 | minor revision |
| far-receivables-rollforward-0007 | B $517,000 (C, B, C), reading "accounts receivable" as the reported asset | yes, all 4; the control-account reading gives $502,000 (choice A) | Moderate | yes (Ana, II.B.c) | 70% | 0.45 | minor revision |

**Average estimated pass likelihood (13 batch items): 78.8%**, up from 47.4%. There are no major-revision items and no wrong keys in any of the 52 batch versions. That is just under the ~80% bar: two items (receivables-rollforward-0006 and -0007) pull it down, and each has a one-clause fix.

### Live item reported separately

| id | my answer | agrees with key? | difficulty | skill tag ok? | pass likelihood | p-value | verdict |
|---|---|---|---|---|---|---|---|
| far-intangibles-cloud-computing-0001 (live, key corrected) | C $95,000 (variants A $153,273, C $76,667, B $127,000) | yes, all 4 | Moderate (4 cost classifications, term with renewal, remaining-term amortization) | yes (App, II.F.c) | 85% | 0.50 | exam-ready |

- The corrected key ($180,000 × 6/54, so amortization runs over the 54 months left in the 60-month term once the software is ready on July 1) is right, and it matches the method used in every variant and in cloud-0002.
- Distractor B, $93,000, now correctly describes the "full 60 months from go-live" error.
- Every distractor in all 4 versions recomputes exactly.
- Note: "it is reasonably certain to exercise its option" hands the candidate the term judgment. That is acceptable, since it is a fact input like a lease-term assessment, but cloud-0002's "management hasn't decided … at list prices" is the better pattern.

## 2. Findings per item not rated exam-ready

### far-bonds-premium-0002 (minor)
- **Giveaway of the central twist.** "Measured on the share of the proceeds that belongs to the bonds, the bonds' effective interest rate is 8%" tells the candidate that part of the proceeds belongs elsewhere, so distractor D (full proceeds as the carrying amount) is defused by the stem itself.
  - **Fix:** state the rate as a market fact that does not point at the allocation, for example "Bonds of similar risk without warrants yield 8%, compounded semiannually." The PV at 8% equals the allocated amount in all four versions (verified: $864,097, $686,301, $1,021,470, $521,952 vs. $521,953 for v3, so v3 needs a $1 tweak or an "approximately"). Use "use the 8% rate on the bonds' carrying amount" if a pointer is needed.
- **Id.** The id says "premium" but the bonds are issued at a discount. The item is still draft, so a matching id (for example `far-bonds-warrants-0001`) costs nothing now.
- Arithmetic is clean in all versions. Distractor C in v1–v3 ("carries the bonds at their own fair value") is a good error-derived choice. Consider putting it in v0 instead of A or B, which are the weakest.

### far-cash-bank-reconciliation-0006 (minor)
- **Template reuse.** This is the fourth item on II.A.b with the "bank balance $X, GL $Y, deposits in transit, outstanding checks, findings → correct cash balance" stem and ask (0001, 0004, 0005 share it). The quality bar says that once two items share a template, the next uses a different format. The bank-collected note also repeats an event from 0001, 0002 and 0003.
  - **Fix:** keep the new events (stop-payment, net card deposit) but change the ask, for example "What net adjustment should Falmouth make to its general ledger cash account?" or "Which amount should replace the bookkeeper's $11,000 of outstanding checks?". Replace the note collection with a new event (for example a returned item for a closed account, or a bank fee on the card batch).
- Keys and distractors are correct in all versions. B ($47,200) is described honestly as producing the same number on either side.

### far-cash-bank-reconciliation-0007 (minor)
- **Template reuse.** Same "correct cash balance" ask as 0001, 0004, 0005 and 0006. The bank's error crediting another customer's deposit repeats 0003 and 0005, and the automatic payment repeats 0004 and cash-unreconciled-0003.
  - **Fix:** ask for the adjusted deposits in transit and the book adjustment as a pair, or for the amount of the book-side correcting entry. Swap the misdirected-deposit event for a new one, keeping the postdated check, which is the item's best feature.

### far-exit-costs-0003 (minor)
- **Echo of exit-costs-0002.** Same ask ("total liability … at December 31, Year 1") and three of 0002's four event types: a stay bonus for supervisors/team leaders, a non-lease contract termination fee, and relocation in Year 2. The changes are real (severance with no service condition, notice not yet sent), so the two-event rule is met, but the format rule (third item on the task) is not.
  - **Fix:** change the ask to Year 1 expense by component or to the Year 2 charge. Or replace the relocation event with something new, for example costs that will continue under an operating contract after the cease-use date (ASC 420-10-25-13), or a benefit covered by an ongoing plan (ASC 712).
- Rules were verified against public summaries of ASC 420-10-25-9 (ratable recognition beyond the minimum retention period, which is 60 days absent a legal notice period) and 25-11 (termination costs recognized when the contract is terminated under its terms). The keys apply both correctly in all 4 versions (6-, 6-, 7- and 4-month periods, all over 60 days).

### far-intangibles-cloud-computing-0002 (minor)
- **v0 distractor C ($292,499) is not what a student making the error gets.** $225,000 × 9/48 + $117,000 × 3/48 = $49,500 exactly, so the full-term error gives $292,500. The $292,499 comes only from rounding each half-dollar product up separately, and the stem gives no rounding instruction.
  - **Fix:** change v0's numbers so the full-48-month amounts are whole dollars, or show C as $292,500 (and re-check the ascending order).
- **v0 has no reengineering distractor.** The $36,000 process redesign is tested only in v1 and v2. The central twist (separate go-live dates) is covered in v0, so this is optional.
- **v1 and v2 rationales for D.** "Capitalizes the $42,000…" should also say it is amortized with the inventory module from March 1 ($42,000 × 10/58 = $7,241). Otherwise the number can't be reproduced from the rationale.
- **Currency confirmed.** Amortization runs over the hosting-arrangement term (noncancellable period plus renewals reasonably certain to be exercised), straight-line, beginning when each module that works independently is ready for its intended use. Business process reengineering is expensed (ASC 720-45). Under ASU 2025-06, capitalization starts once management authorizes and commits to funding and completion is probable. The stem's "after the board approved and funded the project" plus vendor-configuration work meets that test, and gives the same answer under the old stage model. Early adoption is permitted from the start of an annual period, and both regimes agree, so no election is needed.

### far-inventory-rollforward-0007 (minor)
- **Blueprint fit.** It is mapped to II.C.c "Prepare a rollforward of inventory" (Analysis), but the stem has no rollforward: it asks for a net adjustment to a single balance. As written it is closer to an Application "calculate inventory" item.
  - **Fix:** give the draft rollforward (beginning, purchases, COGS, ending) and ask for corrected ending inventory or corrected COGS. The rebate then splits between the two lines, which makes the Analysis tag honest and deepens the rebate judgment.
- **Event reuse.** Goods in transit with title passed at shipment (here in a bonded warehouse) also appear in rollforward-0005 and -0006, and the casualty write-off appears in rollforward-0003. The rebate is new and good.
  - **Fix:** replace the in-transit event, for example with goods out on consignment at a dealer, or freight-in charged to expense.
- **Rebate treatment confirmed** (ASC 705-20-25: a volume rebate that is probable and reasonably estimable reduces the cost of purchases, allocated between inventory on hand and cost of sales). The key ($6,000 = 4% × $150,000 off inventory) is right, and so is every distractor in all 4 versions.

### far-receivables-rollforward-0006 (minor; the most important fix in the batch)
- **Missing fact that changes the key.** The receivables were transferred on October 1. Under secured-borrowing treatment they stay on the books only until the customers pay, and by December 31 most 30-day accounts would have been collected (by the bank, reducing both the receivable and the borrowing). The key ($492,000 + $72,000 − $48,000) assumes none were collected, and the stem never says so.
  - **Fix:** add "None of the transferred accounts had been collected by December 31", or move the transfer to December 20 and say so.
- **Explanation wording.** "Not a sale: Portreath keeps the credit risk, and the agreement forbids…" implies recourse helps defeat sale accounting. Recourse alone does not. Only the pledge/exchange constraint, which gives the transferor more than a trivial benefit, fails ASC 860-10-40-5(b).
  - **Fix:** lead with 40-5(b) and add "recourse by itself would not prevent sale accounting."
- **Template reuse.** Same "balance, before any allowance, at December 31" ask as rollforward-0004 and -0005, and the transfer event is 0005's mirror image (a sale booked as a borrowing there, a borrowing booked as a sale here).
  - **Fix:** ask for the corrected sales figure or corrected collections from the rollforward. Or present the bank's view (the liability balance) beside the receivable.
- **Two-error distractors.** In v1–v3, the "accepts the balance as posted" distractor ($396,000, $609,000, $342,000) combines two errors that offset. Prefer a single-error distractor, for example "treats the showroom sales as needing removal from collections only."

### far-receivables-rollforward-0007 (minor)
- **Ambiguous question.** "What should corrected accounts receivable, before any allowance, be" can be read as the corrected control account ($502,000, choice A, the net of debit and credit balances) or as the asset reported (debit balances, $517,000, the key). The preliminary figure the stem has the candidate correct is the control-account net, which pushes toward A.
  - **Fix:** ask "What amount should Flushing report as accounts receivable, before any allowance, in its December 31, Year 2 balance sheet?". Add that the returning customer's account had a debit balance of at least $9,000, so the return can't create a further credit balance.
- **Reused event.** The recovery of a written-off account is the fourth use on this task (0001, 0002, 0004), and here it is a no-effect decoy.
  - **Fix:** replace it with a new event, for example a December sale on account entered in January, or a customer's note receivable reclassified.
- **Template.** Same balance ask as 0004, 0005 and 0006. With 0006 also fixed, at least one of the two should ask for something else.
- In v2, the control-account distractor ($578,000) is missing, so the version doesn't test the item's central twist the same way. Fine for a variant, but keep it in v0.

## 3. Exam-ready items: short notes

- **far-cash-unreconciled-0004.** New ask (shortage to write off) and a new event (misdirected wire). The deposit already credited but still listed in transit is close to cash-unreconciled-0002's February deposit, and the double-entered disbursement is close to cash-unreconciled-0001; acceptable, since the ask and one event are new. Consider including the petty-cash distractor in v0.
- **far-cash-unreconciled-0005.** The "misstated by how much, in which direction" ask is new. Mixed-direction choices are sorted by signed value correctly in v1 and v3. One reviewer risk: a candidate may treat the unrecorded automatic premium as a timing item, not a misstatement ($1,660). "Before any correction" closes that, and the item is fine as written.
- **far-debt-covenant-0003.** Asking for headroom is a good new format. The impairment-versus-sale exclusion trap is the item's best discrimination. The "excluding gains and losses on sales of long-lived assets" clause is lifted from debt-covenant-0002's EBITDA definition; vary the wording if more covenant items are written. The "omits the tax add-back" distractor in v1–v3 is the weakest.
- **far-inventory-rollforward-0006.** New ask (corrected purchases). Discounts lost under the net method and the purchase-return cutoff are new events. "December 29, FOB shipping point, still in transit" echoes rollforward-0005's December 29 shipment; change the date.
- **far-ppe-rollforward-0006.** All four events are new to the task. The parking-lot reclassification is a good decoy (it changes accounts, not total additions).

## 4. Batch-level assessment

- **Skill mix (13 items):** Remembering and Understanding 0 (0%), Application 4 (31%), Analysis 9 (69%).
  - Against FAR targets (5–15 / 45–55 / 35–45%), the batch alone is Analysis-heavy and Application-light.
  - It adds no R&U, which is what the bank needs while R&U is over its cap.
  - Every Analysis tag matches the mapped task's blueprint mark, except inventory-rollforward-0007's weak fit, noted above.
- **Area mix:** 13/13 Area II (100%) against targets of I 30–40%, II 30–40%, III 25–35%. That is fine for one parallel slice, but the merged batches 15–17 need Area I and III items to balance it. Batches 16 and 17 were not reviewed here.
- **Topic tally:**

  | Topic | Items |
  |---|---|
  | Cash | 4 (bank reconciliation 2, unreconciled 2) |
  | Receivables rollforward | 2 |
  | Inventory rollforward | 2 |
  | PP&E rollforward | 1 |
  | Debt | 2 (interest 1, covenant 1) |
  | Exit costs | 1 |
  | Cloud computing | 1 |

  Cash and the Area II rollforward/reconciliation tasks are over-represented (II.A.b now 6 items, II.A.c 6, II.B.c 7, II.C.c 7, II.D.f 6). Thin tasks the batch skipped include II.B.a (credit losses, 2), II.C.a/b (costing methods, LCNRV), II.D.a–e, II.E.x and II.G.a/b.
- **Average pass likelihood:** 78.8% (13 items) vs. 47.4% at the first gate. No majors and no wrong keys. All 52 batch versions re-solved independently and agree with their keys, and all variant scenarios are internally consistent:
  - rollforward identities hold;
  - the stated $3,370/$4,050/$2,620/$4,560 differences equal GL minus adjusted bank;
  - bond PVs at the effective rate equal the allocated amounts (v3 off by $1);
  - every exit-cost service period exceeds 60 days.

### Ten changes that would most improve the batch, ranked
1. receivables-rollforward-0006: state that no transferred account had been collected by December 31 (or move the transfer to late December).
2. receivables-rollforward-0007: ask for the amount reported in the balance sheet, and state the returning customer's debit balance.
3. receivables-rollforward-0006 explanation: recourse alone does not defeat sale accounting; cite 40-5(b) alone.
4. bonds-premium-0002: replace "measured on the share of the proceeds that belongs to the bonds" with a neutral market-yield sentence, and fix the id.
5. inventory-rollforward-0007: add a draft rollforward and ask for corrected ending inventory or COGS (honest Analysis), and replace the in-transit event.
6. cash-bank-reconciliation-0006 and -0007: change the ask away from "correct cash balance" (fourth and fifth uses on II.A.b), and swap the reused note-collection and misdirected-deposit events.
7. cloud-0002 v0: make distractor C the true full-term figure ($292,500) or change the numbers; add amortization detail to the reengineering rationales.
8. exit-costs-0003: change the ask or replace the relocation event so it doesn't mirror exit-costs-0002.
9. receivables-rollforward-0006/0007: replace the two-error "as posted" distractors and the reused recovery event.
10. inventory-rollforward-0006: change the December 29 FOB shipping-point date that echoes rollforward-0005. debt-covenant-0003: vary the borrowed exclusion clause.

## 5. Suggested additions to the quality bar
- **Secured-borrowing items** state what happened to the transferred receivables after the transfer (collected or not) whenever the balance at a later date is asked.
- **"Accounts receivable" questions** say whether they want the control-account balance or the amount reported in the balance sheet whenever customer credit balances are in the facts.
- **Effective-rate sentences** must not say what carrying amount the rate is "measured on" when allocating that amount is the test. Give a market yield instead.
- **Ask-format tally per task.** The lint could flag a new item whose question sentence matches the ask of two or more existing items on the same task, for example "correct cash balance" or "before any allowance, at December 31".
- **Distractors from per-component rounding:** when a distractor's value depends on rounding each component, the stem must state that rounding. Otherwise use the unrounded total.

## Sources checked (public; full-text fetches from fasb.org, kpmg.com and Big 4 sites were blocked by the egress proxy, so these are search-result summaries)
- ASU 2018-15 / ASC 350-40-35-13 to 35-16 (term of the hosting arrangement; amortization from each module's ready-for-use date): Deloitte Heads Up 2018 (dart.deloitte.com), RSM "Customer's accounting for cloud computing implementation costs", BDO and PYA summaries.
- ASU 2025-06 (stages removed; authorization/funding plus probable-to-complete threshold; effective for annual periods beginning after Dec. 15, 2027, early adoption at the start of an annual period): Crowe, Eide Bailly, Baker Tilly summaries.
- ASC 860-10-40-5(b) (transferee's right to pledge or exchange; constraints giving the transferor more than a trivial benefit): PwC Viewpoint 3.6, Deloitte Roadmap 3.1.
- ASC 705-20-25 (vendor rebates reduce cost of purchases, recognized systematically when probable and reasonably estimable, considered in inventory cost): PwC Inventory guide 1.5.
- ASC 420-10-25-9 and 25-11 (minimum retention period at most the legal notice period or 60 days; contract termination costs when terminated under the contract's terms): PwC PEB guide 8.5, PwC PP&E guide 6.4, Deloitte ASC 420 guidance.
