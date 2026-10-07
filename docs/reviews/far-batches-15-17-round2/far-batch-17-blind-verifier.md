# FAR batch 17 blind verification

All arithmetic was done in Python (calc.py, calc2.py, calc3.py, calc4.py in this folder). Blueprint tags are not in the blind file, so I could not check them. I checked only that each id's topic matches its content, and all 16 do.

| id version | answer | conf | problems (or "clean") |
|---|---|---|---|
| far-change-in-estimate-0003 v0 | C 351,000 | high | clean. 292,500 = new life and salvage applied retroactively from cost; 342,000 = new salvage ignored (BV/4); 386,000 = new salvage over the original remaining 6 years |
| far-change-in-estimate-0003 v1 | A 510,000 | high | clean. 513,600 = old salvage, new life; 529,000 = original remaining life (6); 552,750 = BV less (BV-sal)/8 (total life used as remaining) |
| far-change-in-estimate-0003 v2 | B 318,750 | high | clean. 282,000 = retroactive; 324,750 = old salvage; 351,500 = total life used as remaining |
| far-change-in-estimate-0003 v3 | C 546,000 | high | clean. 468,000 = retroactive; 534,000 = salvage ignored; 606,750 = total life used as remaining |
| far-change-in-principle-0003 v0 | A 586,250 | high | clean. 589,625 = bonus recomputed (indirect effect); 601,250 = Year 2 change used, sign reversed; 653,750 = Year 3 effect with sign reversed |
| far-change-in-principle-0003 v1 | C 571,600 | high | clean. 568,440 = bonus recomputed; 563,700 = Year 3 change used; 658,500 = cumulative difference |
| far-change-in-principle-0003 v2 | D 797,500 | high | clean. 793,000 = bonus recomputed; 782,500 = Year 2 change used; 722,500 = sign reversed |
| far-change-in-principle-0003 v3 | B 473,700 | high | clean. 470,856 = bonus recomputed; 480,000 = pretax; 525,050 = cumulative difference |
| far-error-correction-0001 v0 | B 37,800 | high | clean. 16,200 = Year 1 only, after tax; 43,200 = 24 months after tax (start date ignored); 45,000 = accrued through the discovery date (May 1, Y3) |
| far-error-correction-0001 v1 | A 56,880 | high | clean. 63,200 = through discovery; 72,000 = pretax; 75,840 = 24 months after tax |
| far-error-correction-0001 v2 | A 27,000 | high | clean. 32,400 = through discovery; 36,000 = pretax; 43,200 = 24 months after tax |
| far-error-correction-0001 v3 | B 39,500 | high | clean. 15,800 = Year 1 only; 47,400 = 24 months after tax; 50,000 = pretax |
| far-accounting-errors-0010 v0 | C 688,800 | high | clean. 678,000 = revenue reversed but the return-asset cost not; 680,800 = a full year of depreciation on the 60,000 capitalized; 713,800 = deposit also taken as revenue |
| far-accounting-errors-0010 v1 | A 551,200 | high | clean. 557,200 = no extra depreciation; 562,000 = returns not adjusted; 570,200 = deposit taken as revenue |
| far-accounting-errors-0010 v2 | B 840,780 | high | clean. 828,300 = revenue only; 845,280 = no extra depreciation; 874,780 = deposit taken as revenue |
| far-accounting-errors-0010 v3 | B 476,100 | high | clean. 468,000 = revenue only; 481,100 = no extra depreciation; 486,000 = returns not adjusted |
| far-accounting-errors-0011 v0 | D 1,934,000 | high | clean. 1,808,000 = dividend omitted; 1,860,000 = no change; 1,896,000 = FOB-destination invoice also removed |
| far-accounting-errors-0011 v1 | B 1,205,000 | high | clean. 1,178,000 = invoice also removed; 1,211,000 = dividend on issued shares; 1,266,000 = PO kept |
| far-accounting-errors-0011 v2 | B 2,993,000 | high | clean. 2,920,000 = no change; 3,013,000 = dividend on issued shares; 3,060,000 = PO kept |
| far-accounting-errors-0011 v3 | C 1,007,000 | high | clean. 951,000 = dividend omitted; 986,000 = invoice also removed; 1,036,000 = PO kept |
| far-accounting-errors-0012 v0 | B 2,338,000 | high | clean. 2,275,000 = consigned goods removed; 2,360,500 = interest for the full 9-month term; 2,378,000 = no fair-value adjustment |
| far-accounting-errors-0012 v1 | C 2,027,000 | high | clean. 1,980,000 = no change; 1,992,000 = treated as lower of cost or market (no write-up); 2,063,000 = a full year of interest |
| far-accounting-errors-0012 v2 | B 3,096,000 | high | clean. 3,018,000 = consigned goods removed; 3,129,600 = a full year of interest; 3,144,000 = no fair-value adjustment |
| far-accounting-errors-0012 v3 | B 1,585,000 | high | clean. 1,551,000 = consigned goods removed; 1,594,000 = full-term interest; 1,603,000 = a full year of interest |
| far-contingencies-0015 v0 | A 225,000 | high | clean. 265,000 = midpoint of range; 295,000 = payment not deducted; 305,000 = top of range |
| far-contingencies-0015 v1 | C 300,000 | high | clean. 215,000 = recall omitted; 235,000 = revision omitted; 360,000 = midpoint |
| far-contingencies-0015 v2 | B 165,000 | high | clean. 120,000 = recall omitted; 200,000 = midpoint; 235,000 = top of range |
| far-contingencies-0015 v3 | C 380,000 | high | clean. 270,000 = recall omitted; 300,000 = revision omitted; 500,000 = payment not deducted |
| far-contingencies-0016 v0 | A 41,400 | high | clean. 51,000 = claims paid not deducted; 80,400 = 100% redemption; 203,400 = commitment booked at the contract price |
| far-contingencies-0016 v1 | C 49,000 | high | clean. 22,000 = rebate only; 27,000 = commitment loss only; 133,000 = 100% redemption |
| far-contingencies-0016 v2 | B 40,200 | high | clean. 22,400 = commitment loss only; 51,200 = claims paid not deducted; 197,000 = contract price |
| far-contingencies-0016 v3 | C 41,900 | high | clean. 18,500 = rebate only; 23,400 = commitment loss only; 50,400 = claims paid not deducted |
| far-contingencies-0017 v0 | A 268,906 | high | Minor (rec.): the stem never says the 30-day payment is left undiscounted. Discounting it for one month gives 268,324, which is closest to A, so no second answer. 274,000 = undiscounted; 279,400 = 90,000 compounded (x1.06) instead of discounted; 338,906 = next year's injuries added |
| far-contingencies-0017 v1 | C 363,370 | high | Same minor note. 203,370 = the 30-day payment omitted; 332,370 = IBNR omitted; 373,000 = undiscounted |
| far-contingencies-0017 v2 | B 206,667 | high | Same minor note. 188,667 = IBNR omitted; 213,500 = compounded instead of discounted; 256,667 = next year's injuries added |
| far-contingencies-0017 v3 | C 485,224 | high | Same minor note. 275,224 = the 30-day payment omitted; 442,224 = IBNR omitted; 509,600 = compounded |
| far-contingencies-0018 v0 | B 133,000 | high | clean. 0 = nothing accrued; 350,000 = statutory maximum; 1,333,000 = suit demand also accrued |
| far-contingencies-0018 v1 | A 108,000 | high | clean. 270,000 = statutory maximum; 850,000 = suit demand; 958,000 = both |
| far-contingencies-0018 v2 | A 126,000 | high | clean. Same pattern as v1 |
| far-contingencies-0018 v3 | B 132,000 | high | clean. Same pattern as v0 |
| far-contingencies-0019 v0 | C 310,000 | high | clean. 180,000 = low end of range; 300,000 = midpoint; 405,000 = whistleblower amount added |
| far-contingencies-0019 v1 | A 380,000 | high | clean. 400,000 = midpoint; 510,000 = whistleblower amount added; 560,000 = cap |
| far-contingencies-0019 v2 | B 230,000 | high | clean. 150,000 = low end; 300,000 = whistleblower amount added; 350,000 = cap |
| far-contingencies-0019 v3 | B 470,000 | high | clean. 300,000 = low end; 490,000 = midpoint; 680,000 = cap |
| far-subsequent-events-0014 v0 | B 272,640 | high | clean. 252,444 = bonus computed on income after the bonus; 276,000 = draft income used; 303,040 = gain included |
| far-subsequent-events-0014 v1 | C 169,500 | high | clean. 159,906 = income after bonus; 165,000 = amount accrued; 171,600 = draft income |
| far-subsequent-events-0014 v2 | A 195,400 | high | clean. 198,000 = draft income; 205,000 = amount accrued; 219,400 = gain included |
| far-subsequent-events-0014 v3 | C 203,100 | high | clean. 193,429 = income after bonus; 196,000 = amount accrued; 206,000 = draft income |
| far-subsequent-events-0015 v0 | D 1,714,000 | high | clean. 1,624,000 = dividend also deducted; 1,670,000 = balance less existing allowance (expected collection ignored); 1,684,000 = full shortfall expensed without crediting the existing allowance. ASU 2025-05 reference is accurate and harmless. |
| far-subsequent-events-0015 v1 | C 2,168,000 | high | clean. 2,048,000 = dividend deducted; 2,123,000 = existing allowance not credited; 2,340,000 = no change |
| far-subsequent-events-0015 v2 | C 1,312,000 | high | clean. 1,276,000 = balance less allowance; 1,296,000 = existing allowance not credited; 1,420,000 = no change |
| far-subsequent-events-0015 v3 | C 2,754,000 | high | clean. 2,604,000 = dividend deducted; 2,640,000 = balance less allowance; 2,960,000 = no change |
| far-subsequent-events-0016 v0 | B 1,205,000 | high | Rec.: the stem has no "Ignore income taxes," although its sister items do. The options contain no tax-adjusted value, so there is no second answer. 1,065,000 = the customer's default also recognized; 1,234,000 = warranty ignored; 1,251,000 = sales tax ignored |
| far-subsequent-events-0016 v1 | A 1,553,000 | high | Same rec. 1,582,000 = warranty ignored; 1,611,000 = sales tax ignored; 1,640,000 = draft |
| far-subsequent-events-0016 v2 | B 921,000 | high | Same rec. 811,000 = customer default recognized; 958,000 = sales tax ignored; 980,000 = draft |
| far-subsequent-events-0016 v3 | B 1,279,000 | high | Same rec. 1,124,000 = customer default recognized; 1,308,000 = warranty ignored; 1,360,000 = draft |
| far-subsequent-events-0017 v0 | C 8,422,000 | high | Rec.: add "Ignore income taxes" (a deferred tax asset on the loss could otherwise be argued; no option matches it). 8,302,000 = market decline also recognized; 8,364,000 = whole receivable removed; 8,460,000 = no change |
| far-subsequent-events-0017 v1 | B 6,215,000 | high | Same rec. 6,127,000 = market decline recognized; 6,240,000 = no change; 6,335,000 = court award recognized |
| far-subsequent-events-0017 v2 | B 10,135,000 | high | Same rec. 10,048,000 = whole receivable removed; 10,180,000 = no change; 10,345,000 = court award recognized |
| far-subsequent-events-0017 v3 | C 4,897,000 | high | Same rec. 4,830,000 = market decline recognized; 4,859,000 = whole receivable removed; 4,920,000 = no change |
| far-subsequent-events-0018 v0 | C 1,273,750 | med-high | Treating the January penalty settlement as a recognized subsequent event (evidence of a year-end condition, ASC 855-10-55-1(a); ASC 606-10-32-14) is defensible and is the standard answer. Private, non-SEC status correctly excludes SAB Topic 4C. 1,013,750 = stock dividend also deducted; 1,206,250 = sign reversed; 1,285,000 = pretax |
| far-subsequent-events-0018 v1 | D 1,210,020 | med-high | Same. 1,020,020 = stock dividend deducted; 1,149,980 = sign reversed; 1,180,000 = no change |
| far-subsequent-events-0018 v2 | C 2,401,250 | med-high | Same. 2,061,250 = stock dividend deducted; 2,360,000 = no change; 2,415,000 = pretax |
| far-subsequent-events-0018 v3 | C 1,165,280 | med-high | Same. 1,114,720 = sign reversed; 1,140,000 = no change; 1,172,000 = pretax |

Every numeric distractor maps to a nameable student error. None uses an amount that isn't in the stem. I found no rendering defects, superseded rules or second defensible answers. Every given balance is consistent with its inputs, and the dates drive every date-based amount.

## REQUIRED fixes

None. No version has a wrong key, a second defensible answer, a superseded rule, a missing fact or a distractor no error produces.

## Recommended (not blocking)

1. **Answer-position balance**: the 64 keys split A 13 / B 24 / C 23 / D 4. Because the options are in ascending order, D (the largest value) is almost never correct, so a test-wise student can learn "never D." Re-seed some versions so the largest value is the key (e.g., far-subsequent-events-0015 v1-v3 are all C), or rebalance the distractors above and below the key.
2. **far-subsequent-events-0016 (all versions)** and **far-subsequent-events-0017 (all versions)**: add "Ignore income taxes."
3. **far-contingencies-0017 (all versions)**: say that the payment due within 30 days isn't discounted (e.g., "discount the payment due in one year").
4. **Blueprint tags**: not in the blind file, so not checked here.
