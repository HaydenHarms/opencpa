# FAR batch 16 blind verification

Every figure below was computed in Python (`calc.py` in this folder). No blueprint tags appear in the blind file, so I could not check tags. Topics implied by the ids look plausible for their areas.

| id version | answer | confidence | problems (or "clean") |
|---|---|---|---|
| far-revenue-variable-consideration-0003 v0 | A (320,000) | Medium | **MAJOR: the year-end resolves the uncertainty.** The board must rule "by December 31, Year 1", so by the Year 1 reporting date the outcome is known: approved gives 368,000 (C); rejected gives 320,000 (A). The constraint answer works only if the estimate is made at shipment, before the deadline. The stem has to move the deadline past year-end, or say the ruling is still pending when the statements are issued. Distractors: 344,000 = expected value (50% x $6); 368,000 = full bonus; 960,000 = whole contract (24,000 x 40). |
| ...0003 v1 | B (325,000) | Medium | Same MAJOR flaw. 347,500 = expected value; 975,000 = contract total; $0 = defer everything. |
| ...0003 v2 | B (336,000) | Medium | Same MAJOR flaw. 360,000 = expected value; 384,000 = full bonus; $0 = defer everything. |
| ...0003 v3 | A (338,000) | Medium | Same MAJOR flaw. 360,750 = expected value; 383,500 = full bonus; 1,014,000 = contract total. |
| far-revenue-principal-agent-0002 v0 | C (230,000) | High | Clean, with a minor note: BrightRide sets the price, which is a principal indicator (ASC 606-10-55-39(c)). Agent is still the better answer because the driver is responsible for fulfillment, owns the vehicle and can decline rides (the same conclusion Uber and Lyft reach). 60,000 = subscriptions only; 170,000 = commissions only; 910,000 = gross fares plus subscriptions. |
| ...0002 v1 | B (197,000) | High | Clean. 155,000 = commissions only; 507,000 = driver's 75% share plus subscriptions; 662,000 = gross. |
| ...0002 v2 | C (247,200) | High | Clean. 60,000 = subscriptions; 187,200 = commissions; 1,100,000 = gross. |
| ...0002 v3 | C (139,600) | High | Clean. 45,000 = subscriptions; 94,600 = commissions; 380,400 = driver's 78% share plus subscriptions. |
| far-revenue-licenses-0002 v0 | B (26,600) | High | Clean. Q1 = royalty 15,000 + fixed fee 32,000/4 + royalty 3,600. 18,600 = drops the fixed fee; 50,600 = fixed fee recognized up front; 83,600 = full-year projected royalty (72,000). Minor: "mature tech, no updates" signals functional IP, which is not needed (the sales-based royalty exception applies either way). |
| ...0002 v1 | C (26,200) | High | Clean. 20,200 = drops the fixed fee; 44,200 = fee up front; 23,950 = projected royalty / 4. The projected-royalty error is a quarter here but a full year in v0 and v3; fine. |
| ...0002 v2 | A (29,900) | High | Clean. 33,100 = projected royalty / 4; 59,900 = fee up front; 85,900 = full-year projected royalty. |
| ...0002 v3 | D (36,200) | High | Clean. 19,800 = leaves out the manufacturer royalty (weakest distractor, but nameable); 24,200 = drops the fixed fee; 33,800 = projected royalty / 4. |
| far-revenue-contract-costs-0004 v0 | B (35,000) | High | Clean. (54,000 + 72,000) x 10/36. 15,000 = commission only; 42,000 = amortized for 12 months from signing; 45,000 = includes the forklifts. |
| ...0004 v1 | C (25,200) | High | Clean. 9 months. 10,800 = commission only; 14,400 = setup only; 27,900 = includes supplies. |
| ...0004 v2 | A (33,600) | High | Clean. 8 months. 36,800 = includes supplies; 42,000 = 10 months from signing; 43,200 = includes pallet jacks. |
| ...0004 v3 | C (30,000) | High | Clean. 6 months. 12,000 = commission only; 18,000 = setup only; 45,000 = 9 months from signing. |
| far-nfp-contributed-services-0003 v0 | B (23,000 / 14,000) | High | Clean. Piano work = specialized skill, so revenue and expense; shed labor = creates an asset, so revenue capitalized. 14/14 = drops the shed; 23/23 = shed expensed; 28/19 = includes mailing. |
| ...0003 v1 | C (18,000 / 11,000) | High | Clean. 7/0 = shed only; 11/11 = drops the shed; 21.5/14.5 = includes lawn. |
| ...0003 v2 | A (30,000 / 18,000) | High | Clean. 30/30 = shed expensed; 35/23 = includes lawn; 38/26 = includes mailing. |
| ...0003 v3 | C (15,500 / 9,500) | High | Clean. 6/0 = shed only; 9.5/9.5 = drops the shed; 15.5/15.5 = shed expensed. |
| far-nfp-contributed-services-0004 v0 | D (454,000 / 44,000) | High | Clean. Architect's design is capitalized; affiliate personnel are recognized at the affiliate's cost (ASU 2013-06) and capitalized as construction oversight; groundbreaking volunteers are excluded. A = services expensed; B = affiliate omitted; C = affiliate expensed. |
| ...0004 v1 | C (361,000 / 36,000) | High | Clean. D (363,500 / 38,500) = includes the volunteers. |
| ...0004 v2 | C (598,000 / 58,000) | High | Clean. D = includes the volunteers. |
| ...0004 v3 | D (304,000 / 29,000) | High | Clean. |
| far-nfp-contributions-0003 v0 | C (88,000) | High | Clean. Pledge + supplies + loan forgiveness; the conditional pledge (barrier) is excluded. 63,000 = drops the forgiveness; 70,000 = drops the supplies; 148,000 = includes the conditional pledge. |
| ...0003 v1 | D (117,000) | High | Clean. 57,000 = drops the pledge; 85,000 = drops the forgiveness; 92,000 = drops the supplies. |
| ...0003 v2 | C (70,000) | High | Clean. 34,000 / 50,000 / 120,000, each a nameable omission or inclusion. |
| ...0003 v3 | D (142,000) | High | Clean. 70,000 / 102,000 / 112,000, each a single-item omission. |
| far-fair-value-in-use-0001 v0 | B (180,000) | High | Clean. Minor: the stem hands over the cost-approach inputs, so the only decision is in-use versus 85,000. 202,000 = no functional obsolescence; 218,000 = no physical deterioration. |
| ...0001 v1 | B (150,000) | High | Clean. 60,000 = in-exchange value; 175,000 = no functional obsolescence; 190,000 = new cost. |
| ...0001 v2 | A (220,000) | High | Clean. 250,000 / 270,000 / 300,000 = one or both deductions left out. |
| ...0001 v3 | A (165,000) | High | Clean. 182,000 / 193,000 / 210,000 = deductions left out. |
| far-fair-value-liability-0001 v0 | A (356,500) | High | Clean. 7% gives factor 0.7130. 382,550 = buyer's 5.5%; 391,750 = 5% before the downgrade; 410,950 = risk-free rate. |
| ...0001 v1 | A (514,865) | High | Clean. 6% gives 0.7921. 545,090 = buyer's rate; 555,620 = rate before the downgrade; 566,410 = risk-free rate. |
| ...0001 v2 | B (239,476) | High | 8% gives 0.6302. C = rate before the downgrade; D = risk-free rate. **A (221,730) = 380,000 x 0.5835 = 8% over 7 periods**: off by one period, the only n+1 error in v0-v2. It is weakly nameable and drops the buyer-rate distractor (260,414) used in v0 and v1. |
| ...0001 v3 | B (621,936) | High | 5% gives 0.8638. C = rate before the downgrade; D = buyer's rate. **A (592,344) = 720,000 x 0.8227 = 5% over 4 periods** (n+1, same weak error). The risk-free distractor (658,872) is missing. |
| far-lessee-finance-0004 v0 | B (255,012) | High | Clean. The lessor's third-party residual insurance is not a lessee guarantee. 246,012 = drops IDC; 272,232 = annuity-due factor; 276,402 = adds the PV of the guarantee. |
| ...0004 v1 | A (228,279) | High | 45,000 x 4.9173 = 221,278.5, an exact .5 tie: the key needs half-up rounding (banker's rounding gives 228,278). Minor; change the numbers. 241,558 = annuity due; 243,789 = adds the guarantee PV; 250,279 = adds the guarantee undiscounted. |
| ...0004 v2 | B (276,968) | High | Clean. 298,168 = annuity due; 311,968 = adds the guarantee undiscounted. The PV-of-guarantee distractor (302,693) is not offered, which is fine. |
| ...0004 v3 | A (224,096) | High | Clean. 238,142 = annuity due; 243,073 = adds the guarantee PV; 250,096 = adds the guarantee undiscounted. |
| far-lessee-operating-0006 v0 | A (237,060) | High | Clean. 54,000 x 5.39 - 54,000; the deposit is not a lease payment. 247,060 = adds the deposit; 278,527 = ordinary-annuity factor; 291,060 = balance before the payment. |
| ...0006 v1 | B (261,353) | High | Clean. 246,353 = deducts the deposit; 276,353 = adds it; 320,530 = ordinary-annuity factor. |
| ...0006 v2 | A (203,028) | High | Clean. 211,028 = adds the deposit; 231,456 = ordinary-annuity factor; 243,028 = before payment. |
| ...0006 v3 | B (266,152) | High | Clean. 246,152 = deducts the deposit; 348,945 = ordinary-annuity factor; 361,152 = before payment. |
| far-lessee-finance-0005 v0 | C (18,118 / 37,346) | High | Clean. Liability 358,459 (option included); ROU 373,459 / 10. A = option excluded; B = drops IDC; D = 5-year life. |
| ...0005 v1 | B (9,738 / 31,692) | High | Clean. A = drops IDC; C = 4-year life; D = Year 1 interest. |
| ...0005 v2 | C (30,086 / 42,695) | High | ROU 512,334 / 12 = 42,694.5, another .5 tie (half-up gives 42,695). Minor; adjust. A = option excluded; B = drops IDC; D = Year 1 interest. |
| ...0005 v3 | B (22,122 / 41,820) | High | Clean. A = option excluded; C = 5-year life; D = Year 1 interest. |
| far-lessee-operating-0007 v0 | B (59,000) | High | Clean. (270 - 20)/5 + 9 variable. 50,000 = drops the variable cost; 63,000 = ignores the incentive; 79,000 = cash rent plus variable. |
| ...0007 v1 | C (77,000) | High | Clean. 57,000 = straight-line minus the full incentive in Year 1; 65,000 = drops the variable cost; 87,000 = adds the incentive instead of subtracting it. |
| ...0007 v2 | C (47,000) | High | Clean. 35,000 = incentive deducted in full in Year 1; 40,000 = drops the variable cost; 50,000 = ignores the incentive. |
| ...0007 v3 | A (95,000) | High | Clean. 101,000 = ignores the incentive; 107,000 = incentive sign flipped; 125,000 = cash rent plus variable. |
| far-income-taxes-provision-0004 v0 | C (132,000) | High | Clean. Taxable income 528,000. 22,000 = net of estimated payments; 127,500 = club dues not added back; 152,000 = no installment adjustment. |
| ...0004 v1 | D (83,370) | High | Clean. 13,370 = net of estimated payments; 77,070 = whole gain deducted; 80,850 = club dues not added back. |
| ...0004 v2 | B (146,000) | High | Clean. 133,500 = whole gain deducted; 161,000 = life insurance not removed; 171,000 = no installment adjustment. |
| ...0004 v3 | C (112,320) | High | Clean. 103,920 = whole gain; 108,720 = club dues; 122,400 = life insurance not removed. |
| far-income-taxes-deferred-0004 v0 | C (57,000 / 45,000) | High | A = only the Year 3 reversal; D = gross DTA. **B (57,000 / $0 liability)**: no clear error produces it. Netting would give 12,000 / 0, not 57,000 / 0. At best it reflects "the gain was already recognized, so no difference", which is weak. |
| ...0004 v1 | C (38,100 / 29,400) | High | Same weak B. A = Year 3 only; D = gross. |
| ...0004 v2 | A (70,000 / 55,000) | High | B (80,000 / 45,000) = gross DTA with the VA charged to the DTL; C = gross; D (90,000) = VA added. This version has a different distractor structure from v0, v1 and v3, which is fine. |
| ...0004 v3 | C (49,400 / 38,400) | High | Same weak B (49,400 / 0). A = Year 3 only; D = gross DTA with the VA charged to the DTL. |
| far-income-taxes-provision-0005 v0 | D (24,500) | High | Clean. DTL +12,500, DTA -5,000, VA +7,000. 10,500 = VA sign flipped; 14,500 = DTA sign flipped; 17,500 = drops the VA. |
| ...0005 v1 | B (14,450) | High | Clean. 9,450 = drops the VA; 31,050 = ending net balances instead of changes; 90,050 = total tax expense. |
| ...0005 v2 | C (31,500) | High | Clean. 13,500 = VA sign; 16,500 = DTA sign; 186,500 = total expense. |
| ...0005 v3 | D (20,200) | High | Clean. 6,200 = VA sign; 10,600 = DTA sign; 13,200 = drops the VA. |

## REQUIRED fixes

1. **far-revenue-variable-consideration-0003 (all four versions): MAJOR.** The board's deadline is December 31, Year 1, the same day as the reporting date, so by year-end the ruling is known and the constraint analysis falls away. Either the bonus is earned (C or the full-bonus figure is correct) or it is not (A or B is correct, but not because of the constraint). Fix: move the deadline after year-end (for example "by June 30, Year 2") and state that the board hasn't ruled when the Year 1 statements are issued. Alternatively, ask for the amount recognized as the units ship. The explanation should cite ASC 606-10-32-11 and 32-12 (outcome highly susceptible to factors outside the entity's influence, no experience with similar contracts).
2. **far-income-taxes-deferred-0004 v0, v1, v3: replace distractor B ("X asset; $0 liability").** No nameable error produces it. Use the v2 pattern instead: gross DTA with the VA charged to the DTL, or the 12,000-style net figure.
3. **far-fair-value-liability-0001 v2 A (221,730) and v3 A (592,344):** both use n+1 periods, an error the other versions don't use. Replace them with the buyer-rate figure (v2: 260,414) and the risk-free figure (v3: 658,872) so every version tests the same misconceptions.
4. **Rounding ties (recommended):** far-lessee-finance-0004 v1 (221,278.5) and far-lessee-finance-0005 v2 (42,694.5) land exactly on .5. Change the inputs, or say "round half up", so a student's or a checker's rounding can't produce a near-miss.

Advisory only: principal-agent-0002 (price-setting is a principal indicator; consider adding "BrightRide does not direct how drivers perform rides"); fair-value-in-use-0001 (the stem gives the cost-approach build-up away).
