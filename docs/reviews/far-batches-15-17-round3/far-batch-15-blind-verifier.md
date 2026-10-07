# FAR batch 15 (rev 2) blind verification report

All arithmetic run in Python (solve.py, solve2.py, solve3.py, solve4.py, bonds.py in this folder).

| id version                              | answer                 | conf.    | problems                                                                                                                                  |
| --------------------------------------- | ---------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| far-cash-bank-reconciliation-0006 v0    | B ($890 increase)      | High     | clean (A ignore stop-payment; C ignore card fee; D ignore NSF)                                                                            |
| far-cash-bank-reconciliation-0006 v1    | B ($1,550 decrease)    | High     | clean (A ignore stop; C ignore NSF; D raw bank-minus-book difference)                                                                     |
| far-cash-bank-reconciliation-0006 v2    | B ($1,610 increase)    | High     | clean (A ignore stop; C ignore fee; D raw difference)                                                                                     |
| far-cash-bank-reconciliation-0006 v3    | A ($740 decrease)      | High     | clean (B ignore fee; C ignore NSF; D raw difference)                                                                                      |
| far-cash-bank-reconciliation-0007 v0    | B ($3,670 decrease)    | High     | clean (A postdated check left as cash; C ignore interest; D bank error booked)                                                            |
| far-cash-bank-reconciliation-0007 v1    | C ($4,300 decrease)    | High     | clean (A ignore auto-payment; B postdated left as cash; D bank error booked)                                                              |
| far-cash-bank-reconciliation-0007 v2    | C ($3,170 decrease)    | High     | clean (A ignore auto-payment; B postdated left; D ignore interest)                                                                        |
| far-cash-bank-reconciliation-0007 v3    | B ($4,960 decrease)    | High     | clean (A ignore auto-payment; C ignore interest; D bank error booked)                                                                     |
| far-cash-unreconciled-0004 v0           | B ($1,860)             | High     | clean (A miss DIT double count; C whole difference; D ignore wire / add items wrong way)                                                  |
| far-cash-unreconciled-0004 v1           | B ($2,350)             | High     | clean (A ignore petty-cash duplicate; C whole difference; D ignore wire)                                                                  |
| far-cash-unreconciled-0004 v2           | C ($1,420)             | High     | clean (A miss DIT; B ignore petty; D ignore wire)                                                                                         |
| far-cash-unreconciled-0004 v3           | C ($2,740)             | High     | clean (A miss DIT; B ignore petty; D whole difference)                                                                                    |
| far-cash-unreconciled-0005 v0           | C ($1,250 understated) | High     | clean (A deposit corrected once, not twice; B bank error treated as book error; D ignore premium)                                         |
| far-cash-unreconciled-0005 v1           | C ($960 understated)   | High     | clean (A ignore premium; B ignore counterfeit; D bank error as book error)                                                                |
| far-cash-unreconciled-0005 v2           | B ($1,240 understated) | High     | clean (A single 980 correction; C ignore counterfeit; D ignore premium)                                                                   |
| far-cash-unreconciled-0005 v3           | B ($850 understated)   | High     | clean (A ignore counterfeit; C single correction; D bank error as book error)                                                             |
| far-receivables-rollforward-0006 v0     | C ($516,000)           | High     | clean (A also strip cash sales; B treat transfer as sale; D keep bill-and-hold)                                                           |
| far-receivables-rollforward-0006 v1     | B ($418,000)           | High     | clean (A strip cash sales; C keep bill-and-hold; D add cash sales back)                                                                   |
| far-receivables-rollforward-0006 v2     | C ($639,000)           | High     | clean (A strip cash sales; B treat as sale; D add cash sales)                                                                             |
| far-receivables-rollforward-0006 v3     | B ($359,000)           | High     | clean (A treat as sale; C keep bill-and-hold; D add cash sales)                                                                           |
| far-receivables-rollforward-0007 v0     | C ($526,000)           | Med-High | minor: netting credit balances (B) defensible if immaterial (~2.9%)                                                                       |
| far-receivables-rollforward-0007 v1     | C ($395,000)           | Med-High | same minor netting point (B $384k); D = memo added instead of subtracted                                                                  |
| far-receivables-rollforward-0007 v2     | B ($606,000)           | Med-High | same netting point (A $588k); D = note receivable added back                                                                              |
| far-receivables-rollforward-0007 v3     | B ($332,000)           | Med-High | same netting point (no net option offered here: 323k absent); D = note added back                                                         |
| far-inventory-rollforward-0006 v0       | B ($1,413,000)         | High     | clean (A drop FOB-SP in-transit; C keep discounts lost; D keep consignment)                                                               |
| far-inventory-rollforward-0006 v1       | A ($1,069,000)         | High     | clean (B keep discounts lost; C miss return; D keep consignment)                                                                          |
| far-inventory-rollforward-0006 v2       | B ($1,774,000)         | High     | clean (A drop in-transit; C keep discounts lost; D miss return)                                                                           |
| far-inventory-rollforward-0006 v3       | B ($901,000)           | High     | clean (A drop in-transit; C miss return; D keep consignment)                                                                              |
| far-inventory-rollforward-0007 v0       | B ($1,781,000)         | High     | clean (A whole rebate to COGS; C casualty in COGS; D consignment not reversed)                                                            |
| far-inventory-rollforward-0007 v1       | A ($2,142,000)         | High     | clean (B rebate ignored; C casualty in COGS; D consignment not reversed)                                                                  |
| far-inventory-rollforward-0007 v2       | C ($1,398,500)         | High     | clean (A casualty subtracted from COGS; B whole rebate; D consignment not reversed)                                                       |
| far-inventory-rollforward-0007 v3       | B ($1,623,000)         | High     | clean (A whole rebate; C casualty in; D consignment not reversed)                                                                         |
| far-ppe-rollforward-0006 v0             | C ($630,500)           | High     | clean (A parking lot removed; B transit insurance not added; D fine kept)                                                                 |
| far-ppe-rollforward-0006 v1             | C ($422,900)           | High     | clean (A parking removed; B transit ins. omitted; D property insurance kept)                                                              |
| far-ppe-rollforward-0006 v2             | B ($779,000)           | High     | clean (A transit ins. omitted; C fine kept; D property ins. kept)                                                                         |
| far-ppe-rollforward-0006 v3             | C ($501,700)           | High     | clean (A parking removed; B transit ins. omitted; D property ins. kept)                                                                   |
| far-intangibles-cloud-computing-0002 v0 | B ($288,000)           | Med-High | see note: C ($292,500, 48 months from ready date) is the closest rival; D renewal included; A both modules from first ready date          |
| far-intangibles-cloud-computing-0002 v1 | C ($312,000)           | High     | A amortize from Jan 1; B both modules from first ready date; D redesign capitalized                                                       |
| far-intangibles-cloud-computing-0002 v2 | A ($240,000)           | Med-High | same note (B $248,222 = 36 months from ready date); C renewal; D redesign capitalized                                                     |
| far-intangibles-cloud-computing-0002 v3 | C ($306,000)           | Med-High | same note (D $311,917 = 48 months from ready date); A from Jan 1; B both from first ready date                                            |
| far-exit-costs-0003 v0                  | B ($900,000)           | High     | clean (A severance ratable; C cleaning fee accrued; D full stay bonus)                                                                    |
| far-exit-costs-0003 v1                  | C ($669,000)           | High     | clean (A severance ratable; B severance only; D phone contract accrued)                                                                   |
| far-exit-costs-0003 v2                  | B ($1,092,000)         | High     | clean (A severance only; C phone accrued; D full bonus)                                                                                   |
| far-exit-costs-0003 v3                  | C ($765,000)           | High     | clean (A severance ratable; B severance only; D cleaning fee accrued)                                                                     |
| far-bonds-warrants-0001 v0              | B ($51,937)            | High     | clean (A first period only; C bond FV as carrying amount; D whole proceeds to bonds)                                                      |
| far-bonds-warrants-0001 v1              | B ($32,075)            | High     | clean (A first period only; C bond FV; D whole proceeds)                                                                                  |
| far-bonds-warrants-0001 v2              | C ($56,347)            | High     | clean (A first period only; B cash coupon; D bond FV)                                                                                     |
| far-bonds-warrants-0001 v3              | B ($27,421)            | High     | clean (A cash coupon; C bond FV; D whole proceeds). Allocated $521,952.79 rounds to 521,953 vs PV at 9% of 521,952.38: $1 gap, immaterial |
| far-debt-covenant-0003 v0               | B ($750,000)           | High     | clean (A no restructuring add-back; C gain not excluded; D impairment added back)                                                         |
| far-debt-covenant-0003 v1               | C ($514,750)           | High     | clean (A tax not added back; B no restructuring add-back; D impairment added back)                                                        |
| far-debt-covenant-0003 v2               | B ($824,500)           | High     | clean (A tax not added back; C gain not excluded; D impairment added back)                                                                |
| far-debt-covenant-0003 v3               | C ($509,000)           | High     | clean (A tax not added back; B no restructuring add-back; D gain not excluded)                                                            |

## Working notes

- Bank rec 0006: book adj = -NSF - card fee + stop-payment check reinstated; ties to the corrected bank balance (e.g., v0 49,050 both sides).
- Bank rec 0007: book adj = +interest - auto-payment - postdated check (a receivable, not cash); the bank error and the postdated check come off the bank side. It ties in all four versions.
- Unreconciled 0004: corrected bank = adjusted bank - double-counted DIT; corrected book = GL - wire + petty-cash duplicate; shortage = difference.
- Unreconciled 0005: correct cash = bank + DIT - OC + (charged - written); GL correction = -premium + 2×deposit - counterfeit; both agree.
- AR 0006: the constraint on the transferee's right to pledge or exchange, which gives the transferor more than a trivial benefit, fails ASC 860-10-40-5(b), so the transfer is a secured borrowing (+transfer). The bill-and-hold fails ASC 606-10-55-83 (goods not separately identified, available for other orders) (-invoice). Cash sales posted through AR net to zero.
- AR 0007: gross debit balances - unrecorded return + unrecorded FOB-SP sale; credit balances are reclassified to liabilities.
- Inventory 0006: -consignment-in, -discounts lost (net method, so a financing expense), -Dec 18 return; FOB-SP in transit stays.
- Inventory 0007: casualty loss leaves COGS unchanged (reported separately). Reverse the consignment-out. The rebate is recognized (ASC 705-20-25) and allocated by purchases still on hand vs. sold.
- PP&E 0006: -fine +transit insurance -first-year operating insurance; the parking lot is a reclassification within PP&E, so total additions are unaffected.
- Cloud 0002: ASC 350-40. Process redesign is expensed. Each independent module starts amortizing when it's ready and is amortized straight-line over the remaining term of the hosting arrangement (renewal not reasonably certain: list prices, management undecided), so it is fully amortized at the contract's end. v0: 225,000×9/45 + 117,000×3/39 = 54,000; 342,000-54,000 = 288,000. All keys are whole dollars.
- Exit 0003: ASC 420. Severance with no required future service is recognized in full at the communication date. The stay bonus is recognized ratably over the service period (v0 2/6, v1 3/6, v2 4/7, v3 1/4). The contract-termination fee is recognized when notice is given (Year 2). The non-cancellable phone contract is recognized at the cease-use date (Year 2).
- Bonds 0001: allocation by relative fair values (ASC 470-20-25-2) equals PV at the stated effective rate. Interest is a full semiannual period plus the year-end accrual on the amortized carrying amount.
- Covenant 0003: EBIT = NI + int + tax - gain + restructuring; cushion = EBIT - ratio × interest. The impairment isn't added back.

## REQUIRED fixes

None found that would make a key wrong or create an outright second correct answer. All 52 versions have a single defensible key under the stated facts, and every distractor maps to a nameable error. No .5 ties: the closest is the bond v1 first-period interest of 24,020.535, which is not a tie.

## Optional suggestions

1. far-intangibles-cloud-computing-0002 (v0, v2, v3): ASC 350-40-35-14 says "over the term of the hosting arrangement" without the word "remaining." A student may argue for amortizing the full 48/36-month term from the ready date (options C/B/D). The key is correct, because the term ends on a fixed date and an asset can't outlive the arrangement. To shut the argument down, the explanation should say explicitly that each module is amortized over the months left in the term after it's ready. Alternatively, add "the contract ends on December 31, Year 4" to the stem.
2. far-receivables-rollforward-0007 (all versions): the key relies on reclassifying customer credit balances as liabilities. Credit balances of about 2-3% of AR could be called immaterial, and in v0-v2 the netted figure is an option. Consider adding "Flushing reports material customer credit balances as liabilities" or "the credit balances are material," so that netting is clearly an error rather than a materiality judgment.
3. far-receivables-rollforward-0006: the "add cash sales back" distractor (D in v1-v3) is a weaker error story than the others. It's fine, but "strip cash sales from AR" (A) already covers that misconception.
4. far-bonds-warrants-0001 v3: the allocated bond amount (521,952.79) rounds to 521,953, while PV at 9% is 521,952.38. The $1 gap doesn't change the answer; just make sure the explanation uses 521,953.
5. Key-letter spread across the batch is reasonable (many B and C keys; A in only a few versions). No longest-answer cues: all choices are numeric and in the same format.
