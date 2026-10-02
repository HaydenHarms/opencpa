# Review report: FAR simulations batch 04

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**6 simulations (47 points)**, all Area III, written from scratch in `scripts/batches/far-tbs-04.py` as the third batch of `docs/plans/far-simulations.md`. They use numeric and select tasks. Every amount is computed in the script with `Decimal` and rounded half up. Before writing anything, the script asserts that:

- the revenue allocation sums to the transaction price;
- the lease's Year 3 cost is the same by both routes in ASC 842-20-25-8 (remaining payments plus the asset less the liability, and total payments plus initial direct costs less cost already recognized);
- the draft amounts it shows are the ones its stated errors produce.

| Simulation                          | Blueprint task                                                                                   | Skill       | Tasks                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------------ | ----------- | --------------------------- |
| `far-tbs-contingencies-review-0001` | III.B.c Review documentation for recognition versus disclosure                                   | Analysis    | 1 select, 3 numeric (8 pts) |
| `far-tbs-subsequent-events-0001`    | III.G.c Derive the impact of identified subsequent events                                        | Analysis    | 1 select, 3 numeric (7 pts) |
| `far-tbs-revenue-contract-0001`     | III.C.d Determine revenue under the five-step model                                              | Application | 1 select, 3 numeric (8 pts) |
| `far-tbs-accounting-changes-0001`   | III.A.b Derive the impact of an accounting change or error correction                            | Analysis    | 1 select, 4 numeric (8 pts) |
| `far-tbs-nfp-contributions-0001`    | III.C.b/f/g NFP promises to give, contributed services, financial and nonfinancial contributions | Application | 1 select, 3 numeric (8 pts) |
| `far-tbs-operating-lease-0001`      | III.F.d Calculate lessee lease costs                                                             | Application | 7 numeric (8 pts)           |

FAR now has **21 simulations**: Area I 6, Area II 7, Area III 8, with 10 tagged Analysis.

## What each simulation tests

- **Contingencies (Larkhall).** Counsel's letter, board minutes and the controller's draft treatment of six matters:
  - A product suit with a range and no best estimate (accrue the minimum; the draft used the midpoint).
  - A non-income tax assessment under appeal with a most likely amount (accrue it; the draft only disclosed it).
  - A shareholder suit dismissed and on appeal, where the appellate court has always affirmed (remote; the draft is right).
  - An indemnification claim from the buyer of a division sold earlier, with an unpredictable outcome (disclose; the draft is right).
  - A jury award to Larkhall under appeal (a gain contingency; the draft recognized it).
  - A noncancelable, unhedged purchase commitment whose expected net realizable value fell below the contract price (recognize the loss; the draft only disclosed it).
  - Data to reject: the supplier's new price (replacement cost), the amount the shareholder sought.
- **Subsequent events (Penwortham).** A public company's log of documents received before and after filing:
  - Recognized: a price concession for goods that didn't meet the order at shipment, and a sale of held-for-sale equipment that shows its year-end fair value.
  - Disclosed only: a division acquisition and a plant closing approved after year end.
  - Not reflected: a suit filed after the filing date.
  - Classification: a covenant waiver obtained before issuance (ASC 470-10-45-11) and a short-term note refinanced with bonds before it was repaid (ASC 470-10-45-14).
  - Working capital after both the asset and the liability corrections.
- **Revenue (Stannard).** A scanner sale with embedded software, a site survey, installation, training, maintenance and a standard warranty:
  - Which promises are separate obligations, part of the scanner, or not obligations at all.
  - Allocation on relative standalone selling prices, with one estimated by expected cost plus margin (Stannard's stated policy); the list price and the independent installers' price are data to reject.
  - Point-in-time and over-time recognition, training by sessions delivered, and the contract liability.
- **Accounting changes (Corrieside).** Four Year 3 matters and the staff's draft comparative figures:
  - FIFO to weighted average, applied retrospectively (the staff did nothing, and the Year 3 draft starts from FIFO inventory).
  - Incremental contract commissions expensed in error (the staff's adjustment amortizes a full year, not six months).
  - A revised fleet life (prospective; the staff wrongly adjusted Year 2). The draft's Year 3 commission amortization and fleet depreciation are correct.
  - A new leasing business (not an accounting change).
- **NFP contributions (Ashgrove).** A matching pledge partly met, a cost-reimbursement state grant, a board member's multiyear promise, an architect's donated design, volunteers, donated seedlings, a gala ticket with an exchange element, and a gift passed through to a named charity.
- **Operating lease (Kerrow).** A lessor reimbursement of fit-out costs (an incentive receivable at commencement), a payment to the previous tenant to leave early (an initial direct cost) and a pre-signing inspection (not one), CPI-indexed rent, common area maintenance under the combine election, and a reassessment of the lease term after Kerrow builds an immovable clean room, with an updated discount rate and the index updated at remeasurement.

## Checks against the bank

Each simulation was drafted after reading every MCQ on its blueprint task together (far-tbs-03 gate lesson). Events chosen to differ from the bank:

- Contingencies: the bank's items use insurer denials, limitation clauses, overbilling, guarantees, future-accident reserves and settled claims. This one adds a non-income tax assessment, a purchase-commitment loss, an indemnification claim and a dismissed suit on appeal. (The gate found that the bank also has a purchase commitment, a range with no best estimate and an appealed award; see below.)
- Subsequent events: the bank uses customer bankruptcies, settlements, dividends, fires, thefts, tax-rate changes and market declines. This one uses a price concession, a held-for-sale sale, a covenant waiver, a refinancing and a split.
- Accounting changes: the bank's change-in-principle item is LIFO to FIFO with an unaccrued invoice; the error items use deposits, inventory, insurance, machines and bonds. This one uses FIFO to weighted average, contract-cost commissions and a staff draft.
- NFP: the bank's items and the far-tbs-02 statement of activities (a clinic with a conditional dental-unit promise) use bequests, annuity promises, collections, warehouse use and veterinarians. This one is a land conservancy with a matching pledge, a reimbursement grant, an agency transfer and a gala.
- Lease: `far-lessee-operating-0005` covers a rent holiday, percentage rent and the short-term exemption; `far-tbs-lessee-accounting-0001` is a finance lease. This one covers a fit-out reimbursement, a payment to the old tenant, an index, nonlease components and a remeasurement.
- Promises to give: `far-nfp-promises-to-give-0002` has an all-or-nothing matching promise (nothing recognized). Ashgrove's Halsall pledge matches dollar for dollar, so the matched part is recognized. That contrast is deliberate, but the gate should judge whether it reads as an echo.

## Blind verification

One verifier solved every task from the scenarios, exhibits and prompts alone, doing the arithmetic in Python. Every answer matched the key except one, the lease liability at December 31, Year 2. There the verifier discounted the payments over eight periods instead of the six that remain (three left in the original term and three in the renewal), giving $829,908 against the key's $659,748. Its right-of-use asset and Year 3 cost moved by the same amount, so its Year 3 cost matched the key ($126,200). The key stands. The eight-period factor stays in the exhibit as data to reject.

Required fixes, all applied (no key changed):

| Simulation         | Finding                                                                                                                                                                             | Fix                                                                                                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contingencies      | The inventory cost method wasn't stated. Under LIFO or retail, lower of cost or market with the $1,640 replacement price would apply (liability $590,000, income change −$320,000). | The scenario says Larkhall costs inventory by FIFO.                                                                                                                    |
| NFP contributions  | "Ashgrove has no other contributions in Year 1" could be read to exclude the other donors' $265,000 for the nature center (giving $377,800).                                        | The scenario now says Exhibit 1 lists every contribution and grant received in Year 1.                                                                                 |
| Revenue            | Without a stated enforceable term, maintenance cancellable each year would make the contract one year long (installation $68,716, revenue $1,794,194, liability $48,806).           | Neither party may cancel the maintenance before the end of the term.                                                                                                   |
| Accounting changes | "The error was found in Year 3" answered the select row, and the staff's commission line handed over a correct piece of the Year 2 answer.                                          | The sentence is gone. The staff now amortizes a full year ($32,000) instead of six months, so the line must be checked; Year 2 as adjusted by the staff is $1,160,500. |

Suggestions applied:

- **Accounting changes:** Exhibit 3 says its net income and adjustment amounts are after tax.
- **Subsequent events:** the select row reads "Evidence from the sale of the equipment held for sale", since the sale itself is a Year 2 event.
- **Lease:** the scenario fixes the reassessment date as December 31, Year 2.

Not applied:

- The verifier asked whether the blueprint has Analysis tasks for contingencies and subsequent events. It does: III.B.c and III.G.c (`scripts/far-coverage.py`).
- NFP contributions are tagged "Revenue recognition" in Area III, as in the bank (III.C.b, f and g).
- The lease's board-approval sentence is an indicator, not the conclusion, and stays.

## Review gate

Every simulation was gated in full, on Sonnet, with the standard brief adapted for simulations.

| Run        | Average pass likelihood                                                                                | Verdicts              | Outcome                                                                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Revision 1 | **79.5%**: contingencies 80, subsequent events 80, revenue 79, accounting changes 84, NFP 78, lease 76 | 6 minor               | **Just under the ~80% bar.** Every key matched the reviewer's own solutions and every explanation's arithmetic held; no major items. Revised (revision 2). |
| Revision 2 | **81.8%**: contingencies 82, subsequent events 87, revenue 83, accounting changes 78, NFP 76, lease 85 | 3 exam-ready, 3 minor | **Passed.** The reviewer's own solutions agreed with every key (33 numeric answers, 30 select rows); no major items.                                       |

The gate confirmed from public sources (PwC, Deloitte, RSM, Clark Nuber, Forvis Mazars, EisnerAmper, Crowe and the ASU text): a significant leasehold improvement triggers a lease term reassessment, with an updated discount rate and index payments at the current index; a waiver of more than one year allows noncurrent classification; a matching requirement is a barrier, met to the extent matched.

**Required fixes, all applied:**

- **Revenue, task 2** asked for the amount allocated to "the installation", which told the candidate installation is a separate obligation (task 1 row 3). It now asks for the scanner's allocation ($1,614,983).
- **NFP:** the other donors' $265,000 appeared only inside Halsall's row. It is now its own "Various donors" row.
- **Lease:** the commencement events (public entity, annuity due, a broker's commission owed on signing, non-incremental legal fees, a cash incentive) repeated `far-lessee-operating-0004`. They are now a reimbursement of Kerrow's fit-out (an incentive receivable at commencement), a payment to the previous tenant to leave early (an initial direct cost), and a pre-signing engineering inspection (not one). The keys are unchanged.

**Strong optional findings, applied:**

- **Contingencies:** the gate found an MCQ twin for most matters. The unasserted injury claim is replaced by an asserted indemnification claim from the buyer of a division Larkhall sold. Counsel's letter now adds that the appeal has no reasonable prospect. Task 4 no longer states the test ("reasonably possible") and asks for the additional loss to disclose up to the top of counsel's ranges.
- **Subsequent events:** the EPS-after-a-split task duplicated `far-subsequent-events-0003`. The split is gone, and task 4 asks for working capital ($4,195,750), which needs both the asset and the liability corrections. The draft no longer gives a November fair value estimate that conflicted with the unchanged market. The waiver row says Penwortham expects to meet the covenant through Year 2.
- **Accounting changes:** task 3 (January 1, Year 2, retained earnings as adjusted) duplicated `far-change-in-principle-0002`, so it now asks for December 31, Year 2, retained earnings as adjusted ($5,527,000). The staff line no longer says "capitalize". The commission is $108,000, not $96,000, which repeated `far-revenue-contract-costs-0003`. New keys: Year 2 net income $1,234,000, Year 3 $1,346,500, December 31, Year 3 retained earnings $6,553,500.
- **NFP:** Pellow placed no restriction on its gift, Ashgrove owns the marsh, and the grant row no longer echoes the commensurate-value wording.
- **Lease:** Exhibit 2 says the January 1, Year 2, rent was paid.

**Not applied:** the gate's optional suggestions to merge the lease's first and third tasks and to drop "contract asset" from the revenue liability prompt.

**Blind re-check of revision 2.** A fresh verifier solved all six and matched every key. Its required fixes, applied (no key changed):

- **Accounting changes:** the staff's $36,000 Year 2 amortization (a full year) is the draft's error. The line now reads as the staff's figure, not as a given fact.
- **NFP:** the same-year release policy now also covers conditional contributions (a separate election), and restoration costs are expensed as incurred, so the grant can't be argued restricted or capitalized.

Suggestions applied: the Elmford indemnity's fair value at inception was immaterial and nothing was recorded; the covenant expectation sits in the waiver row; the lease stays an operating lease, and the fit-out reimbursement is measured at its full amount.

**Revision 2 gate, required fixes applied (wording only, no key changed):**

- **Accounting changes:** the memo's "costs of obtaining contracts that must be capitalized" gave away the judgment that expensing them was an error. It now reads "its policy for capitalized contract acquisition costs".
- **NFP:** "No donor has variance power" misused the term (a donor grants variance power to the recipient). It now says no donor has given Ashgrove variance power, and Ashgrove is not financially interrelated with Marlbank.

Optional findings applied: Halsall's obligation is limited to qualifying gifts received by June 30, Year 2; Penwortham's current assets line lists all its components instead of naming the two adjusted ones; the revenue contract no longer says Stannard "stands ready" (which handed over the ratable pattern); the lease explanation says $535,813 is the liability before the January 1 payment, and the fit-out reimbursement is treated as received at commencement.

Optional findings not applied: the remaining echoes of MCQ templates (an inventory method change, a revised useful life, an appealed award, a log-style NFP exhibit). Each simulation now combines them with events no MCQ has, and the gate passed them; the next Area III batch (far-tbs-07) should avoid these event types.

**Quality bar:** the gate's lessons are now in the Simulations section of `docs/content-pipeline.md`:

- A prompt must not name an amount that exists only under the classification another task asks for.
- A simulation task doesn't repeat an MCQ's exact ask (EPS after a split, retained earnings as adjusted, accrue-then-disclose).
- Every amount a task uses gets its own exhibit row, not a mention inside another item's narrative.

## Status

FAR now has **21 simulations**: Area I 6, Area II 7, Area III 8, with 10 tagged Analysis. Next in the plan is far-tbs-05 (Area I).
