# Review report: FAR simulations batch 03

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**6 simulations (46 points)**, all Area II, written from scratch in `scripts/batches/far-tbs-03.py` as the second batch of `docs/plans/far-simulations.md`. They use numeric, select and journal-entry tasks. Every amount is computed in the script with `Decimal` and rounded half up. Before writing anything, the script asserts that:

- the receivables aging foots and the subledger and control account reconcile to the same corrected balance;
- the inventory units tie to the count;
- the staff's draft rollforward reconstructs from its stated errors;
- the bond retirement entry balances;
- the payables subledger and control account reconcile.

| Simulation                                | Blueprint task                                                                                     | Skill       | Tasks                                 |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------- | ------------------------------------- |
| `far-tbs-receivables-reconciliation-0001` | II.B.d Reconcile the receivables subledger to the general ledger (with II.B.a allowances)          | Analysis    | 1 select, 4 numeric (8 points)        |
| `far-tbs-inventory-measurement-0001`      | II.C.a Calculate inventory using various costing methods; II.C.b Apply lower of cost and NRV       | Application | 5 numeric (7 points)                  |
| `far-tbs-ppe-rollforward-0002`            | II.D.f Prepare a rollforward of PP&E (with II.D.b disposals)                                       | Analysis    | 1 select, 5 numeric (9 points)        |
| `far-tbs-bonds-payable-0001`              | II.H.1c Calculate interest expense on notes and bonds; II.H.1d carrying amount and journal entries | Application | 4 numeric, 1 journal entry (8 points) |
| `far-tbs-equity-method-0001`              | II.E.3b Calculate the carrying amount of equity method investments                                 | Application | 5 numeric (7 points)                  |
| `far-tbs-payables-reconciliation-0001`    | II.G.d Reconcile the payables subledger to the general ledger                                      | Analysis    | 1 select, 4 numeric (7 points)        |

FAR now has **15 simulations**: Area I 6, Area II 7, Area III 2, with 7 tagged Analysis.

## What each simulation tests

- **Receivables (Tamsin).** A customer aging that doesn't agree with the control account. The candidate works from source documents, not a list of named errors:
  - A remittance for one customer's over-60 invoices was applied to another customer's current invoices. This changes the aging, and so the allowance, but not the total.
  - A December 30 invoice for goods shipped FOB destination and delivered in January must come out of both records.
  - Forklift sale proceeds were keyed into the accounts receivable column of the cash receipts journal (general ledger only).
  - A write-off was posted to the general ledger but left in the aging.
  - A customer's credit balance goes to liabilities.
  - The allowance has a debit balance before adjustment, after write-offs and a recovery.
  - Data to reject: a January wire.
- **Inventory (Pellworth).** Three product lines:
  - Tents use FIFO, with a purchase return taken out of the last layer.
  - Stoves use FIFO, with a water-damaged lot whose net realizable value (NRV) is lower.
  - Fuel canisters use periodic weighted average, with freight-in that was wrongly expensed and must be capitalized, and consigned-in goods in the count.
  - The lower of cost and NRV test applies at the product-line level, which is Pellworth's stated policy. It writes down two lines; the total-inventory comparison would show no write-down.
  - Data to reject: replacement cost and the normal profit margin (the superseded lower-of-cost-or-market inputs).
- **PP&E rollforward (Garroway), revision 2.** A staff draft checked against source documents:
  - The tractor is capitalized at list price plus a separately priced service contract; it belongs at its cash price net of a discount taken, and gets three months of depreciation, not a full year.
  - A truck's life-extending engine overhaul is expensed; it should be capitalized, with depreciation revised from July 1.
  - A trade-in is recorded at book value plus cash; it has commercial substance (backhaul revenue from new customers), so it belongs at fair value plus cash, with a gain.
  - The sale and the disposal lines are handled correctly.
  - Data to reject: an insurance appraisal.
- **Bonds (Halvard).** A discount bond:
  - The issue price comes from present value factors; the stated-rate factors are a distractor.
  - Interest expense for Year 1.
  - A 40% open-market buyback on October 1, which needs a partial-period amortization on the retired bonds, gives a loss, and is recorded as a single journal entry.
  - Year 2 interest split across the retired and remaining bonds.
  - Data to reject: the call price.
- **Equity method (Hartwell and Bexley).** Two years, starting April 1:
  - Basis differences in inventory, a warehouse and a patent, plus goodwill.
  - Income from the acquisition date only, and the investee's OCI.
  - Upstream intra-entity profit deferred in Year 1 and realized in Year 2.
  - Data to reject: dividends treated as income, the broker's fair values (no fair value option), and a lender's replacement-cost land appraisal.
- **Payables (Brackwell).** A January disbursements search plus a vendor statement reconciliation:
  - Unrecorded: a received but unrecorded invoice, December legal services billed in January, and goods in transit under FOB shipping point.
  - An unrecorded vendor credit memo.
  - Not adjustments: an FOB destination receipt in January, a January service contract and a check in the mail.
  - A cash-on-delivery equipment purchase debited to the accounts payable control account explains the subledger-to-control difference.

## Blind verification

One verifier solved every task from the scenarios, exhibits and prompts alone, doing the arithmetic in Python. **Every answer matched the key** on the facts as written, and every exhibit foots and ties. Required fixes, all applied (no key changed):

| Simulation       | Finding                                                                                                                                                                                    | Fix                                                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Receivables      | The aging bucket the misapplied payment came out of in Ashdown's account wasn't stated. Restoring it to 1–30 days instead of Current gives an allowance of $18,059 and expense of $22,859. | The remittance document says the clerk applied the check against Ashdown's current (not yet due) invoices, and that Pryor's invoices were due October 28. |
| Equity method    | A land row giving a $310,000 appraisal excess made a $60,000 goodwill answer defensible, because basis differences use fair value.                                                         | Hartwell's valuation puts the land at book value; the $310,000 is a lender's replacement-cost appraisal, which isn't fair value.                          |
| PP&E             | "Fleet decals" could defensibly be expensed as branding, which would change the cost and depreciation answers.                                                                             | The capitalized costs are dealer preparation, a federally required electronic logging device and USDOT identification markings.                           |
| Inventory, bonds | Confirm the canister cost is $21,725 (exact $21,725.17) and the retirement entry's discount line is the netted $51,044.                                                                    | Both keys already were.                                                                                                                                   |

Suggestions applied:

- The lumber price index sentence is gone, since it could invite an extra overlay on rates already adjusted for forecasts.
- The flatbed exchange's trade-in value now comes from an independent appraiser Garroway engaged, not the counterparty.
- The equity-method topic string matches the bank: "Investments (Equity method investments)".

Not applied:

- The verifier thought the bonds topic might read "Debt (financial liabilities)". `docs/content-pipeline.md` and the bank use "Debt (Notes and bonds payable)", so that stays.
- The payables select names Corran's invoice and credit memo. This was left as is, because the select also has a Corran row that needs no adjustment (the check in the mail).

## Review gate

Every simulation was gated in full, on Sonnet, with the standard brief adapted for simulations.

| Run        | Average pass likelihood                                                                   | Verdicts              | Outcome                                                                                                                                                            |
| ---------- | ----------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Revision 1 | **83.2%**: receivables 86, inventory 86, PP&E 78, bonds 84, equity method 83, payables 82 | 5 exam-ready, 1 minor | **Passed.** Every key matched the reviewer's own solutions (worked in Python before it read the keys), with no second defensible answers, and every exhibit foots. |

The gate confirmed the ASU 2025-05 point from FASB's ASU and two firm summaries: a private company may consider collections after year end only if it also elects the practical expedient.

**Required fixes, both on the PP&E simulation, applied by rebuilding it under a new id, `far-tbs-ppe-rollforward-0002`.** `far-tbs-ppe-rollforward-0001` is retired and must not be reused.

- **Template reuse.** The draft-review framing, the expensed get-ready costs, the scrapped fully depreciated asset, the full-year depreciation error and the commercial-substance evidence together echoed `far-ppe-rollforward-0004`, `-0005` and `far-ppe-exchange-0001`. The rebuild replaces several events:
  - The tractor invoice now has a 2/10 cash discount taken and a separately priced extended service contract. The staff capitalized list price plus the contract.
  - A truck's life-extending engine overhaul was expensed. Capitalizing it means revising depreciation from July 1.
  - The scrapped dolly is gone.
  - The exchange's commercial substance now comes from backhaul revenue from new customers.
  - The staff's disposal lines are now correct, so the select needs a real check of every line.
  - A new task asks how much the draft overstates depreciation, which can't be answered without the draft.
- **Explanation arithmetic.** The depreciation explanation chained "= $8,142 + …"; each piece is now computed separately, with rounded steps marked.

**Blind re-checks of the rebuild.** The first found a second defensible answer in the first rebuild. It had made the trade-in lack commercial substance (carryover basis, no gain), but the cash paid was 41% of the exchange's fair value. Under ASC 845-10-25-6, that makes it a monetary exchange measured at fair value, so the staff's draft was defensible. The exchange now plainly has commercial substance and is also over the 25% threshold, so fair value and a $2,000 gain are the answer under every reading, including ASC 610-20 for a trade with a noncustomer. The staff's error is carrying over book value. The final version is: equipment $4,927,200, depreciation $560,858, accumulated depreciation $2,313,308, draft depreciation overstated by $27,109, net loss on disposals $2,950.

A final blind check of the rebuilt simulation matched every key with no required fixes and confirmed every exhibit foots.

**Optional findings applied:**

- **Bonds:** the factor table shows 2.5% and 3% side by side, rather than titling the exhibit "3% per period". The journal-entry prompt now just says "to record the retirement", so it doesn't flag the interest to the retirement date that the loss task depends on. The scenario says interest is recorded only on payment dates and at retirement.
- **Receivables:** task 2 no longer defines the control balance as "debit balances less credit balances" next to task 3. The rates apply "by its age at December 31". The scenario states that, without the expedient, Tamsin can't consider collections after year end.
- **Payables:** the policy sentence now only fixes the account (no accrued-liabilities account) without restating the recognition test. The non-citation reference is gone, and the task 3 explanation is worded as an adjustment.
- **Inventory:** the canister explanation shows $21,725.17, rounded to $21,725.

**Optional findings not applied:**

- Changing the equity method's 30% stake (it echoes `far-equity-method-0001`). The gate judged that enough else differs.
- Swapping the payables legal-services row, which overlaps `far-payables-cutoff-0001`.

**Quality bar:** the gate's lessons are now in the Simulations section of `docs/content-pipeline.md`:

- Check events against all the MCQs on a task together.
- Mark rounded steps in explanations.
- Exhibit titles don't name the rate or method.
- An Analysis simulation built on a draft needs a task that requires the draft, and the draft has some correct lines.
- A policy sentence doesn't restate the recognition test.
- One task's prompt doesn't define another's answer by contrast.
- State both ASU 2025-05 elections when a collection after year end appears.

## Status

FAR now has **15 simulations**: Area I 6, Area II 7, Area III 2, with 7 tagged Analysis. The gate notes that Area II (46.7%) is now above its band and Area III (13.3%) well below it, so far-tbs-04 (Area III) is next. Area II topics with no simulation yet: cash, intangibles, investments at fair value and equity transactions (far-tbs-06 in the plan).
