# Review report: FAR simulations batch 03

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**6 simulations (45 points)**, all Area II, written from scratch in `scripts/batches/far-tbs-03.py` as the second batch of `docs/plans/far-simulations.md`. They use numeric, select and journal-entry tasks. Every amount is computed in the script with `Decimal` and rounded half up. Before writing anything, the script asserts that:

- the receivables aging foots and the subledger and control account reconcile to the same corrected balance;
- the inventory units tie to the count;
- the staff's draft rollforward reconstructs from its stated errors;
- the bond retirement entry balances;
- the payables subledger and control account reconcile.

| Simulation                                | Blueprint task                                                                                     | Skill       | Tasks                                 |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------- | ------------------------------------- |
| `far-tbs-receivables-reconciliation-0001` | II.B.d Reconcile the receivables subledger to the general ledger (with II.B.a allowances)          | Analysis    | 1 select, 4 numeric (8 points)        |
| `far-tbs-inventory-measurement-0001`      | II.C.a Calculate inventory using various costing methods; II.C.b Apply lower of cost and NRV       | Application | 5 numeric (7 points)                  |
| `far-tbs-ppe-rollforward-0001`            | II.D.f Prepare a rollforward of PP&E (with II.D.b disposals)                                       | Analysis    | 1 select, 4 numeric (8 points)        |
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
- **PP&E rollforward (Garroway).** A staff draft with four kinds of error:
  - The flatbed from a trade-in exchange is recorded at book value plus boot. The exchange has commercial substance, so the flatbed belongs at the trade-in's appraised fair value plus cash, and a gain is recognized.
  - A sale is removed at its proceeds instead of cost, with no loss recorded.
  - A tractor's required logging device and USDOT markings are expensed while its registration is capitalized, and the tractor gets a full year of depreciation instead of three months.
  - A scrapped, fully depreciated dolly is never removed.
  - Data to reject: the dealer's list price (with its usual discount range) and an insurance appraisal.
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

Pending: every simulation is gated in full. Results will follow in a later commit.
