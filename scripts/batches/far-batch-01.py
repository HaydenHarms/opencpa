"""FAR batch 01 — 25 items: 12 adapted from the legacy cpa-study.html bank and re-reviewed, 13 written from scratch
to raise difficulty and fill blueprint gaps (see docs/reviews/far-batch-01.md).

Run: python3 scripts/batches/far-batch-01.py  (writes content/far/*.yaml)
Every numeric answer and distractor below was recomputed in code during review.
"""
import os
import glob
from common import mcq as _mcq, finalize, audit, write_items, RU, AP, AN

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = ("Batch 01, revised after independent quality review and a second pass to raise difficulty. "
        "Answers re-solved and every number and distractor computed in code.")


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


ITEMS = [
# ── Area I ──────────────────────────────────────────────────────────────
mcq("far-cash-flows-0001", A1, "Statement of cash flows", AP,
    ["ASC 230-10 (statement of cash flows: operating activities, indirect method)"],
    """Marlow Corp. reports net income of $180,000. During the year, depreciation was $24,000, accounts receivable increased by $31,000, inventory decreased by $12,000, and Marlow recorded a $9,000 gain on the sale of equipment. Under the indirect method, what is net cash provided by operating activities?""",
    [("$152,000", "Subtracts the inventory decrease. A decrease in inventory means less cash was tied up, so it is added back."),
     ("$176,000", "Correct. $180,000 + $24,000 − $9,000 − $31,000 + $12,000."),
     ("$185,000", "Forgets to remove the $9,000 gain. The full sale proceeds belong in investing activities, so the gain must come out of operating."),
     ("$238,000", "Adds the receivables increase. Higher receivables mean revenue was recognized but not yet collected, so the increase is subtracted.")],
    "B",
    """Start with net income, add back noncash depreciation, remove the gain (its cash is in investing), subtract the increase in receivables, and add the decrease in inventory: $180,000 + $24,000 − $9,000 − $31,000 + $12,000 = $176,000."""),

mcq("far-cash-flows-0002", A1, "Statement of cash flows", AP,
    ["ASC 230-10 (statement of cash flows: classification and indirect method)"],
    """Fenwick Ltd. reports net income of $140,000. During the year: depreciation $33,000; loss on early retirement of bonds $8,000; accounts receivable increased $19,000; unearned revenue increased $13,000; dividends paid $20,000. Under the indirect method and U.S. GAAP, what is net cash provided by operating activities?""",
    [("$155,000", "Subtracts the $20,000 of dividends paid. Under U.S. GAAP, dividends paid are a financing outflow, not an operating adjustment."),
     ("$159,000", "Subtracts the $8,000 loss instead of adding it back. A loss reduced net income without using operating cash."),
     ("$162,000", "Omits the unearned revenue increase. Cash collected in advance of earning revenue is an operating inflow."),
     ("$175,000", "Correct. $140,000 + $33,000 + $8,000 − $19,000 + $13,000.")],
    "D",
    """Add back depreciation and the loss on bond retirement (the cash paid to retire bonds is financing), subtract the receivables increase, and add the unearned revenue increase: $140,000 + $33,000 + $8,000 − $19,000 + $13,000 = $175,000. Dividends paid are reported in financing activities."""),

mcq("far-nfp-net-assets-0001", A1, "Statement of activities (Not-for-Profit)", AP,
    ["ASC 958-205 (net assets with and without donor restrictions)", "ASU 2016-14 (eliminated the option to imply a time restriction on long-lived assets)"],
    """Clearfield Museum receives a $500,000 gift in Year 1 that the donor restricts to constructing a new gallery. The donor does not say how long the museum must use the gallery. In Year 2, the museum spends the $500,000 completing construction and places the gallery in service. How are Clearfield's net assets affected?""",
    [("Year 1: with donor restrictions +$500,000. Year 2: the full $500,000 is released to without donor restrictions.", "Correct. The purpose restriction is met by the Year 2 construction spending and placing the gallery in service, so the full gift is released in Year 2."),
     ("Year 1: without donor restrictions +$500,000. Year 2: no reclassification is needed because the gift was never restricted.", "Ignores the donor's restriction. A gift restricted to a purpose is reported with donor restrictions when received."),
     ("Year 1: with donor restrictions +$500,000. Year 2: released to without donor restrictions over the gallery's useful life as it is depreciated.", "Former practice, when an entity could imply a time restriction over the asset's life. ASU 2016-14 eliminated that option."),
     ("Year 1: with donor restrictions +$500,000. Year 2: no release until the museum sells or otherwise disposes of the gallery.", "Confuses the restriction on the gift with a restriction on the asset's future use. Absent donor stipulations on use, the restriction ends when the asset is placed in service.")],
    "A",
    """A gift restricted to a purpose is reported as an increase in net assets with donor restrictions. When the donor gives no explicit stipulation about how long a long-lived asset must be used, the restriction is met when the asset is placed in service, and the amount is reclassified as net assets released from restrictions. Since ASU 2016-14, an entity may no longer imply a time restriction that spreads the release over the asset's useful life."""),

mcq("far-governmental-property-tax-0001", A1, "Measurement focus and basis of accounting", AP,
    ["GASB Statement No. 33 (nonexchange transactions)", "GASB Statement No. 34 (government-wide and fund financial statements)", "GASB Statement No. 65 (deferred inflows of resources)"],
    """Lakeview Township's fiscal year is the calendar year. On January 1, Year 5, it levies $4,000,000 of property taxes to finance Year 5 operations. The levy becomes legally enforceable that day, and no taxes were prepaid. The township expects 2% of the levy to prove uncollectible. It collects $3,650,000 through December 31, Year 5, and $150,000 during the first 45 days of Year 6, and it expects to collect the rest of the collectible amount between 90 and 120 days after year-end. In its governmental funds, the township treats property taxes as available if collected within 60 days after year-end. By how much does property tax revenue in the government-wide statement of activities exceed property tax revenue in the general fund's statement of revenues, expenditures, and changes in fund balance?""",
    [("$0", "Applies one basis to both statements. Government-wide statements use full accrual and the funds use modified accrual, so the amounts differ."),
     ("$120,000", "Correct. Government-wide: $4,000,000 less $80,000 expected uncollectible is $3,920,000. General fund: $3,650,000 + $150,000 = $3,800,000. The remaining $120,000 will arrive too late to be available, so the fund reports it as a deferred inflow of resources."),
     ("$200,000", "Leaves the expected uncollectible amount out of the government-wide figure ($4,000,000 − $3,800,000). Government-wide revenue is net of the $80,000 the township expects not to collect."),
     ("$270,000", "Measures fund revenue at cash collected by year-end only ($3,650,000), ignoring the $150,000 collected within the 60-day availability period.")],
    "B",
    """Government-wide statements use the economic resources focus and full accrual. The levy is for Year 5 and enforceable on January 1, so Year 5 revenue is $4,000,000 − $80,000 = $3,920,000. Governmental funds use the current financial resources focus and modified accrual, so revenue is limited to amounts collected by year-end or within the 60-day availability period: $3,650,000 + $150,000 = $3,800,000. The $120,000 of collectible taxes expected later is a deferred inflow of resources in the fund. Difference: $3,920,000 − $3,800,000 = $120,000."""),

mcq("far-nfp-contributions-0001", A1, "Statement of activities (Not-for-Profit)", AN,
    ["ASC 958-605 (contributions received, including conditional contributions)", "ASC 958-205 (net assets with and without donor restrictions)", "ASU 2018-08 (clarifying the scope and the accounting guidance for contributions)"],
    """Harbor Arts Foundation, a not-for-profit entity, has these transactions in Year 1. (1) On December 31 it receives a written promise of $80,000 payable on January 1, Year 3; nothing else is required of the foundation to receive it, and the donor states no use for the money. The promise has a present value of $72,000. (2) It receives $60,000 in cash that the donor requires to be used for scholarships, and it spends $25,000 on qualifying scholarships during Year 1. (3) It receives $150,000 in cash under an agreement that lets the donor recover the money if the foundation does not raise $150,000 of matching gifts by the end of Year 2. By December 31, Year 1, the foundation has raised no matching gifts. (4) It receives a $100,000 cash gift with no donor stipulations. The foundation reports every restricted gift as with donor restrictions when received, even if the restriction is met in the same period. Ignoring interest accretion, by what amount do net assets with donor restrictions increase in Year 1?""",
    [("$107,000", "Correct. $72,000 for the promise (restricted by time) + $60,000 for the scholarship gift − $25,000 released when the scholarships were funded. The $150,000 is a refundable advance, and the $100,000 gift is without donor restrictions."),
     ("$115,000", "Measures the promise at its $80,000 face amount. A promise due in a future period is recorded at present value."),
     ("$132,000", "Leaves out the $25,000 release. Spending on the donor's purpose moves that amount out of net assets with donor restrictions."),
     ("$257,000", "Counts the $150,000 as revenue with donor restrictions. Because the donor can recover it until the matching gifts are raised, it is a refundable advance (a liability), not revenue.")],
    "A",
    """The $80,000 promise carries no condition other than the passage of time, so it is recognized now at present value ($72,000) as an increase in net assets with donor restrictions (time restriction). The $60,000 scholarship gift is restricted to a purpose; spending $25,000 on it releases that amount, leaving a $35,000 net increase. The $150,000 depends on a measurable barrier (matching gifts) and includes a right of return, so it is not revenue until the barrier is overcome; the cash is a refundable advance. The $100,000 gift is without donor restrictions. Increase with donor restrictions: $72,000 + $60,000 − $25,000 = $107,000."""),

mcq("far-eps-diluted-0001", A1, "Public Company Reporting Topics", AN,
    ["ASC 260-10 (earnings per share)", "ASU 2020-06 (if-converted method for convertible instruments)"],
    """Kestrel Corp. reports net income of $1,200,000 and 500,000 weighted-average common shares outstanding for the year. It has cumulative preferred stock on which $100,000 of dividends accrued this year, none of which was declared. Kestrel also has (1) options to buy 40,000 common shares at $30 per share, outstanding all year, with an average market price of $50 during the year, and (2) $1,000,000 of 6% convertible bonds issued at par and outstanding all year, convertible into 20,000 common shares. Kestrel's tax rate is 25%. What are Kestrel's diluted earnings per share, rounded to the nearest cent?""",
    [("$2.04", "Adds all 40,000 option shares. Under the treasury stock method only the shares not covered by assumed repurchase (16,000) are added."),
     ("$2.13", "Correct. ($1,200,000 − $100,000) ÷ (500,000 + 16,000 option shares)."),
     ("$2.14", "Includes the convertible bonds. Their incremental effect is $45,000 ÷ 20,000 = $2.25 per share, above the $2.13 diluted EPS before the bonds, so they are antidilutive and excluded."),
     ("$2.33", "Does not deduct the $100,000 of cumulative preferred dividends. Cumulative dividends are deducted whether or not declared.")],
    "B",
    """Income available to common = $1,200,000 − $100,000 cumulative preferred dividends = $1,100,000. Options (treasury stock method): 40,000 − (40,000 × $30 ÷ $50) = 16,000 incremental shares, which are dilutive. Convertible bonds (if-converted): add back after-tax interest of $60,000 × (1 − 25%) = $45,000 and add 20,000 shares; the incremental effect is $2.25 per share, higher than the $2.13 EPS so far, so the bonds are antidilutive and excluded. Diluted EPS = $1,100,000 ÷ 516,000 = $2.13."""),

mcq("far-comprehensive-income-0001", A1, "Statement of comprehensive income", AP,
    ["ASC 220-10 (comprehensive income)", "ASC 320-10 (available-for-sale debt securities)", "ASC 321-10 (equity securities)", "ASC 830-30 (translation of financial statements)"],
    """Delmar Inc. reports net income of $420,000 for the year. Net income includes a $30,000 gain realized on the sale of available-for-sale debt securities, which Delmar had reported in other comprehensive income as an unrealized gain in earlier periods, and a $20,000 gain from the increase in fair value of an equity investment that has a readily determinable fair value. During the year, unrealized holding gains on Delmar's remaining available-for-sale debt securities arose totaling $90,000 before tax, and a foreign subsidiary's financial statements produced a $50,000 translation gain. Delmar recognizes no deferred taxes on the translation gain because it plans to reinvest the subsidiary's earnings indefinitely, and it applies a 25% tax rate to all gains and losses on available-for-sale securities, including the gain reclassified into net income, but not to the translation gain. What is Delmar's comprehensive income for the year?""",
    [("$502,500", "Applies the 25% rate to the translation gain as well. Delmar recognizes no deferred taxes on it, so it is $50,000 in full."),
     ("$515,000", "Correct. $420,000 + [($90,000 − $30,000) × 75% = $45,000] + $50,000."),
     ("$530,000", "Ignores the tax effect of the unrealized holding gains ($60,000 + $50,000 of other comprehensive income)."),
     ("$537,500", "Omits the reclassification adjustment. The $30,000 gain is already in net income, so it must come out of other comprehensive income to avoid counting it twice ($67,500 + $50,000).")],
    "B",
    """Comprehensive income = net income + other comprehensive income (OCI). The $20,000 gain on the equity investment is already in net income (changes in fair value of equity securities go through earnings), so it is not OCI. AFS debt: unrealized holding gains of $90,000 arose, and $30,000 previously in OCI moved to net income on sale (a reclassification adjustment), so pre-tax OCI is $60,000 and after tax $60,000 × 75% = $45,000. The translation gain is $50,000 with no tax. OCI = $95,000; comprehensive income = $420,000 + $95,000 = $515,000."""),

mcq("far-governmental-fund-types-0001", A1, "Purpose of funds", RU,
    ["GASB Statement No. 54 (governmental fund type definitions)"],
    """Northgate City accounts for the four activities below. Which activity is reported in a capital projects fund?""",
    [("Bond proceeds restricted for a new fire station, plus the related construction costs", "Correct. Capital projects funds account for resources restricted, committed, or assigned to capital outlay."),
     ("Water service charges that are set to recover the full cost of running the city's water utility", "Reported in an enterprise fund, which accounts for activities financed by fees charged to external users."),
     ("Resources accumulated to pay principal and interest on the city's general obligation bonds", "Reported in a debt service fund, which accounts for resources set aside for debt payments."),
     ("Hotel occupancy tax revenue that the city council has committed to tourism promotion", "Reported in a special revenue fund, which accounts for revenue sources restricted or committed to a specific operating purpose.")],
    "A",
    """A capital projects fund accounts for financial resources that are restricted, committed, or assigned to expenditure for capital outlay, such as bond proceeds and the construction of a fire station. Debt service funds accumulate resources for principal and interest payments, special revenue funds account for revenue sources restricted or committed for specific operating purposes, and enterprise funds account for fee-supported business-type activities."""),

# ── Area II ─────────────────────────────────────────────────────────────
mcq("far-ppe-impairment-0001", A2, "Property, plant and equipment", AP,
    ["ASC 360-10 (impairment of long-lived assets held and used)"],
    """Parkside Manufacturing's machinery (held and used) has a carrying amount of $850,000. Undiscounted future cash flows from its use and disposition are $820,000, and its fair value is $700,000. What impairment loss should Parkside recognize?""",
    [("$150,000", "Correct. The asset fails the recoverability test ($850,000 > $820,000), so the loss is carrying amount minus fair value."),
     ("$30,000", "Uses the undiscounted cash flows to measure the loss. They are used only to test recoverability."),
     ("$0", "Would be right only if undiscounted cash flows equaled or exceeded the carrying amount."),
     ("$120,000", "Measures the loss as undiscounted cash flows minus fair value; the loss is carrying amount minus fair value.")],
    "A",
    """Step 1 (recoverability): carrying amount $850,000 exceeds undiscounted cash flows of $820,000, so the asset is not recoverable. Step 2 (measurement): loss = carrying amount − fair value = $850,000 − $700,000 = $150,000."""),

mcq("far-ppe-exchange-0001", A2, "Property, plant and equipment", AP,
    ["ASC 845-10 (nonmonetary transactions)"],
    """Harwick Corp. exchanges old machinery (book value $180,000; fair value $210,000) plus $40,000 cash for new equipment with a fair value of $250,000. The exchange has commercial substance. What gain does Harwick recognize, and at what amount is the new equipment recorded?""",
    [("Gain of $30,000; new equipment $250,000", "Correct. With commercial substance, the gain is fair value minus book value of the asset given up, and the new asset is recorded at fair value."),
     ("No gain; new equipment $220,000", "Carryover-basis treatment, which applies only when the exchange lacks commercial substance."),
     ("Gain of $70,000; new equipment $250,000", "Compares the new asset's fair value to the old book value and ignores the $40,000 of cash paid."),
     ("Gain of $30,000; new equipment $220,000", "Mixes the two methods: recognizes the gain but records the asset at carryover basis.")],
    "A",
    """With commercial substance, the exchange is measured at fair value. Gain = $210,000 fair value − $180,000 book value = $30,000. The new equipment is recorded at $210,000 + $40,000 cash = $250,000, which equals its fair value."""),

mcq("far-inventory-lcnrv-0001", A2, "Inventory", AP,
    ["ASC 330-10 (inventory; ASU 2015-11 lower of cost and net realizable value)"],
    """Crestview Co. uses FIFO and applies the lower of cost and net realizable value to each product separately. At year-end: Product A has 1,000 units with FIFO cost of $12.00, selling price of $14.50, cost to complete and sell of $3.00, and replacement cost of $11.20 per unit. Product B has 2,000 units with FIFO cost of $8.00, selling price of $10.00, cost to complete and sell of $2.50, and replacement cost of $7.60 per unit. Product C has 500 units with FIFO cost of $20.00, selling price of $25.00, cost to complete and sell of $4.00, and replacement cost of $20.50 per unit. What inventory write-down should Crestview recognize?""",
    [("$0", "Compares selling price with cost and ignores the costs to complete and sell that net realizable value subtracts. Every selling price exceeds its cost, so this test finds no write-down."),
     ("$1,000", "Applies the test to the inventory as a whole: total cost $38,000 against total NRV $37,000. Crestview applies the test product by product, so Product C's surplus cannot offset the shortfalls."),
     ("$1,500", "Correct. NRV is selling price less costs to complete and sell; Products A and B are each $0.50 per unit below cost, and Product C is not written down."),
     ("$1,600", "Measures the shortfall against replacement cost, the old lower-of-cost-or-market approach. FIFO and average-cost inventory use NRV; replacement cost applies only to LIFO and the retail inventory method.")],
    "C",
    """For FIFO or average-cost inventory, measure each product at the lower of cost and NRV. Product A: NRV $14.50 − $3.00 = $11.50, below cost by $0.50 × 1,000 = $500. Product B: NRV $10.00 − $2.50 = $7.50, below cost by $0.50 × 2,000 = $1,000. Product C: NRV $25.00 − $4.00 = $21.00, above the $20.00 cost, so no write-down and no write-up. Total write-down: $1,500."""),

mcq("far-equity-paid-in-capital-0001", A2, "Equity", AP,
    ["ASC 505-10 (equity securities issued for noncash consideration)", "SEC Staff Accounting Bulletin Topic 5.A (expenses of offering)"],
    """Redford Corp. issues $2 par value common stock during the year. It (1) sells 5,000 shares for cash at $18 per share, (2) issues 3,000 shares in exchange for land whose fair value is $60,000 (the shares are thinly traded, so the land's value is more clearly evident), and (3) pays $9,000 of legal and underwriting costs directly attributable to the offering. What amount of additional paid-in capital results from these transactions?""",
    [("$119,000", "Records the land at the shares' $18 price ($54,000) instead of the land's more clearly evident $60,000 fair value. That leaves $48,000 of APIC on the land shares: $80,000 + $48,000 − $9,000."),
     ("$125,000", "Correct. APIC on the cash sale is $80,000 and on the land exchange is $54,000, less $9,000 of offering costs."),
     ("$134,000", "Ignores the offering costs, which are netted against the proceeds of the offering."),
     ("$143,000", "Adds the offering costs to APIC instead of deducting them.")],
    "B",
    """Cash sale: 5,000 × ($18 − $2 par) = $80,000 of APIC. Land exchange: the land is recorded at its more clearly evident fair value of $60,000, so 3,000 shares carry $6,000 of par and $54,000 of APIC. Offering costs of $9,000 reduce APIC. Total: $80,000 + $54,000 − $9,000 = $125,000."""),

mcq("far-investments-afs-credit-loss-0001", A2, "Investments (Financial assets at fair value)", AP,
    ["ASC 326-30 (available-for-sale debt securities)"],
    """Foxworth Inc. holds available-for-sale bonds with an amortized cost of $100,000 and a year-end fair value of $88,000. Of the $12,000 decline, $7,000 is attributable to expected credit losses and $5,000 to rising market interest rates. Foxworth does not intend to sell and is not likely to be required to sell. How is the decline reported?""",
    [("$12,000 loss in net income, because the security is impaired below amortized cost", "Recognizes the whole decline in earnings, as if the securities were trading."),
     ("$7,000 credit loss in net income (allowance); $5,000 in other comprehensive income", "Correct. For AFS debt, the credit portion goes to net income (via an allowance) and the noncredit portion goes to OCI."),
     ("$12,000 unrealized loss in other comprehensive income, with no credit loss in earnings", "Ignores the credit loss, which must be recognized in earnings."),
     ("$5,000 market loss in net income; $7,000 credit loss in other comprehensive income", "Swaps the two components.")],
    "B",
    """Under ASC 326-30, an impaired AFS debt security the holder does not intend to sell is split: the credit loss ($7,000) is recorded through an allowance and net income (limited to the amount by which fair value is below amortized cost), and the remaining decline ($5,000) goes to OCI."""),

mcq("far-equity-retirement-0001", A2, "Equity", AP,
    ["ASC 505-30 (treasury stock and retirement of shares)"],
    """Mercer Inc. originally issued 1,000 shares of $2 par common stock at $14 per share. It later reacquires and retires all 1,000 shares at $20 per share. Mercer's policy is to charge additional paid-in capital for the original paid-in capital in excess of par on the retired shares, and to charge any remaining excess of the purchase price to retained earnings. What amount is debited to retained earnings on retirement?""",
    [("$6,000", "Correct. Common stock ($2,000) and APIC ($12,000) are removed at their original amounts; the remaining $6,000 of the price is charged to retained earnings."),
     ("$0", "Would let APIC absorb more than the $12,000 originally received, which Mercer's policy does not do."),
     ("$18,000", "Charges the entire excess over par ($20,000 − $2,000) to retained earnings. GAAP permits that alternative, but it is not Mercer's stated policy."),
     ("$20,000", "Charges the entire price to retained earnings without removing par or APIC.")],
    "A",
    """Under Mercer's policy the retirement entry is: Dr Common stock $2,000; Dr APIC $12,000; Dr Retained earnings $6,000; Cr Cash $20,000. ASC 505-30 also allows an entity to charge the entire excess over par to retained earnings, so the policy matters: it determines how much of the excess APIC absorbs."""),

mcq("far-receivables-credit-losses-0001", A2, "Trade receivables", AN,
    ["ASC 326-20 (credit losses on financial instruments measured at amortized cost)"],
    """Orchard Supply Co. reports trade receivables of $1,000,000 at year-end. Of that amount, $150,000 is owed by one customer that has filed for bankruptcy, and Orchard expects to collect 30% of that balance in the proceedings. The remaining $850,000 is owed by customers with similar credit profiles. Orchard's historical credit loss rate on such balances is 3%, and its reasonable and supportable forecast of economic conditions indicates expected losses on them will be 1 percentage point higher than the historical rate. Orchard has no other information bearing on expected credit losses. What should the ending balance in Orchard's allowance for credit losses be?""",
    [("$40,000", "Applies a single 4% rate to all $1,000,000. The bankrupt customer's balance has different expected losses and is evaluated on its own."),
     ("$79,000", "Reserves the 30% Orchard expects to collect ($45,000) instead of the 70% it expects to lose ($105,000), then adds $34,000 for the pool."),
     ("$130,500", "Uses the 3% historical rate for the pool. Expected credit losses must reflect current conditions and reasonable and supportable forecasts, which raise the rate to 4%."),
     ("$139,000", "Correct. $150,000 × 70% = $105,000 for the bankrupt customer, plus $850,000 × 4% = $34,000 for the pool."),
     ("$184,000", "Reserves the entire $150,000 from the bankrupt customer. Orchard expects to collect 30% of it, so the allowance covers only the expected 70% loss.")],
    "D",
    """Under the current expected credit loss model, balances that do not share risk characteristics with the pool are evaluated separately. The bankrupt customer: expected loss = $150,000 × (1 − 30%) = $105,000. The pool: the historical 3% is adjusted for forecast conditions to 4%, so $850,000 × 4% = $34,000. Ending allowance = $105,000 + $34,000 = $139,000."""),

mcq("far-debt-extinguishment-0001", A2, "Debt (Notes and bonds payable)", AP,
    ["ASC 470-50 (debt modifications and extinguishments)", "ASC 835-30 (interest method and presentation of debt issuance costs)"],
    """On January 1, Year 1, Sable Corp. issues $1,000,000 of five-year, 6% bonds, with interest paid each December 31, for $920,146, a price that yields 8%. Sable pays $20,000 of issuance costs, which it presents as a deduction from the bonds' carrying amount and amortizes straight-line over the five years. Sable amortizes the bond discount using the effective interest method and rounds to the nearest dollar at each step. On December 31, Year 2, immediately after paying interest, Sable repurchases all of the bonds in the open market for $1,020,000. What loss on extinguishment does Sable recognize?""",
    [("$20,000", "Compares the price with the $1,000,000 face amount. The loss is measured against the net carrying amount, which reflects the unamortized discount and issuance costs."),
     ("$71,541", "Ignores the $12,000 of unamortized issuance costs, which are part of the net carrying amount and are written off in the loss."),
     ("$79,912", "Amortizes the discount straight-line ($15,971 a year). The stem calls for the effective interest method, which amortizes $13,612 and then $14,701."),
     ("$83,541", "Correct. $1,020,000 − ($948,459 carrying amount − $12,000 unamortized issuance costs)."),
     ("$91,541", "Treats all $20,000 of issuance costs as unamortized. Two of five years have passed, so $8,000 has been amortized and $12,000 remains.")],
    "D",
    """Year 1 interest expense = $920,146 × 8% = $73,612; cash interest $60,000; discount amortization $13,612; carrying amount $933,758. Year 2 interest expense = $933,758 × 8% = $74,701; amortization $14,701; carrying amount $948,459. Unamortized issuance costs = $20,000 − 2 × $4,000 = $12,000, so the net carrying amount is $936,459. Loss = $1,020,000 − $936,459 = $83,541."""),

mcq("far-intangibles-goodwill-0001", A2, "Intangible assets", AN,
    ["ASC 350-20 (goodwill)", "ASC 350-30 (indefinite-lived intangible assets)", "ASU 2017-04 (simplifying the test for goodwill impairment)"],
    """Whitfield Corp., a public business entity, tests one reporting unit for impairment at year-end. The unit's carrying amount is $12,000,000, which includes goodwill of $3,000,000 and an indefinite-lived trade name carried at $2,000,000. Whitfield estimates the fair value of the reporting unit at $9,500,000 and the fair value of the trade name at $1,700,000. Ignore income tax effects. What goodwill impairment loss should Whitfield recognize?""",
    [("$0", "Compares the unit's $9,500,000 fair value with its carrying amount excluding goodwill ($9,000,000). The unit's carrying amount includes goodwill."),
     ("$2,200,000", "Correct. The trade name is impaired first by $300,000, leaving a carrying amount of $11,700,000; the goodwill loss is $11,700,000 − $9,500,000."),
     ("$2,500,000", "Measures goodwill against the full $12,000,000 carrying amount without first recognizing the $300,000 trade-name impairment, so that shortfall is counted twice."),
     ("$3,000,000", "Writes off all the goodwill. The loss is the amount by which carrying amount exceeds fair value, limited to the goodwill balance.")],
    "B",
    """When goodwill and other assets of a reporting unit are tested together, the other assets are tested first. The indefinite-lived trade name is impaired by $2,000,000 − $1,700,000 = $300,000, which reduces the reporting unit's carrying amount to $11,700,000. Goodwill impairment is the excess of the unit's carrying amount over its fair value, limited to goodwill: $11,700,000 − $9,500,000 = $2,200,000, which is less than the $3,000,000 of goodwill."""),

mcq("far-equity-method-0001", A2, "Investments (Equity method investments)", AP,
    ["ASC 323-10 (equity method investments)"],
    """On January 1, Year 1, Pillar Corp. pays $1,500,000 for 30% of the common stock of Quarry Inc. and can significantly influence Quarry's operating decisions. Quarry's net assets have a book value of $4,000,000. Quarry's equipment, which has a 4-year remaining life and is depreciated straight-line, has a fair value $400,000 above its book value, and no other asset or liability has a fair value that differs from book value. For the year, Quarry reports net income of $600,000 and pays dividends of $200,000. During Year 1, Pillar sold inventory to Quarry at a profit of $100,000. Quarry resold 60% of that inventory to outsiders during the year and holds the rest at year-end. Ignore income taxes, and assume Pillar has not elected the fair value option. What is the carrying amount of Pillar's investment in Quarry at December 31, Year 1?""",
    [("$1,533,000", "Amortizes the entire $300,000 excess over the equipment's life ($75,000). Only the $120,000 attributed to the equipment is amortized; the $180,000 remainder is goodwill and is not amortized."),
     ("$1,550,000", "Eliminates 100% of the unrealized profit ($40,000). Pillar eliminates only its 30% share ($12,000)."),
     ("$1,578,000", "Correct. $1,500,000 + $180,000 share of income − $60,000 dividends − $30,000 equipment amortization − $12,000 unrealized profit."),
     ("$1,590,000", "Does not eliminate any of the unrealized profit on the inventory Quarry still holds."),
     ("$1,608,000", "Omits the $30,000 amortization of the equipment's basis difference.")],
    "C",
    """Excess of cost over share of book value = $1,500,000 − (30% × $4,000,000) = $300,000. Of that, 30% × $400,000 = $120,000 relates to the equipment (amortized over 4 years, $30,000 a year) and $180,000 is goodwill (not amortized). Carrying amount = $1,500,000 + 30% × $600,000 ($180,000) − 30% × $200,000 ($60,000 dividends) − $30,000 amortization − 30% × (40% × $100,000) = $12,000 unrealized profit = $1,578,000."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("far-contingencies-0001", A3, "Contingencies and commitments", AP,
    ["ASC 450-20 (loss contingencies)"],
    """Bravo Corp. is a defendant in a product liability lawsuit. Its attorneys believe an unfavorable outcome is more than remote but less than likely, and they estimate a loss of $2,000,000 if the plaintiff prevails. How should Bravo report the lawsuit?""",
    [("Accrue a $2,000,000 liability, because the loss can be reasonably estimated", "Accrual requires both a probable loss and a reasonable estimate. An outcome that is less than likely is not probable."),
     ("Disclose the nature of the loss and its estimate in the notes; record no liability", "Correct. A loss that is more than remote but less than probable is reasonably possible: disclose it, but do not accrue."),
     ("Neither record nor disclose the lawsuit until an unfavorable outcome is probable", "Describes the treatment of a remote contingency. A reasonably possible loss must be disclosed."),
     ("Accrue a probability-weighted liability and disclose the range of possible loss", "U.S. GAAP does not accrue expected values for contingencies that are not probable.")],
    "B",
    """Under ASC 450, a loss is accrued only when it is probable (likely to occur) and reasonably estimable. Attorneys' view that an outcome is more than remote but less than likely means the loss is reasonably possible, which requires disclosure of the nature of the contingency and an estimate of the possible loss or range, but no accrual."""),

mcq("far-revenue-allocation-0001", A3, "Revenue recognition", AP,
    ["ASC 606-10 (allocating the transaction price to performance obligations)"],
    """Harmon Technologies sells software licenses, implementation services, and one year of post-contract support for a total of $450,000. The standalone selling prices are licenses $300,000, implementation $150,000, and support $50,000. Harmon concludes that each of the three is a distinct performance obligation, and no observable evidence shows that the discount relates to fewer than all three. How much of the transaction price is allocated to the licenses?""",
    [("$270,000", "Correct. $300,000 ÷ $500,000 = 60%; 60% × $450,000."),
     ("$300,000", "Uses the standalone selling price and ignores the $50,000 discount, which is allocated proportionally."),
     ("$150,000", "Splits the price equally across the three obligations instead of using relative standalone selling prices."),
     ("$250,000", "Uses a residual approach ($450,000 − $150,000 − $50,000), which is not permitted when all standalone selling prices are observable.")],
    "A",
    """Allocate on a relative standalone selling price basis. Total SSP = $500,000, so the licenses get $300,000 ÷ $500,000 × $450,000 = $270,000. The $50,000 discount is spread across all three obligations."""),

mcq("far-lessee-finance-0001", A3, "Lessee accounting", AP,
    ["ASC 842-20 (lessee accounting: finance leases)"],
    """On January 1, Year 1, Reeves Corp. commences a 5-year finance lease. The lease liability at commencement is $200,000 (rounded), the annual payment of $50,000 is due each December 31, and the discount rate is 8%. The right-of-use asset is amortized straight-line over the lease term. What total lease-related expense does Reeves recognize in Year 2?""",
    [("$53,280", "Correct. Year 2 interest of $13,280 on a $166,000 opening liability, plus $40,000 of amortization."),
     ("$56,000", "Uses Year 1 interest ($16,000) without reducing the liability for the Year 1 principal payment."),
     ("$40,000", "Includes only amortization. A finance lease also has interest expense."),
     ("$50,000", "Treats the cash payment as the expense.")],
    "A",
    """Year 1: interest $16,000, principal reduction $34,000, ending liability $166,000. Year 2: interest = $166,000 × 8% = $13,280. Amortization = $200,000 ÷ 5 = $40,000. Total Year 2 expense = $53,280."""),

mcq("far-accounting-errors-0001", A3, "Accounting changes and error corrections", AP,
    ["ASC 250-10 (accounting changes and error corrections)"],
    """In Year 3, before its Year 3 financial statements are issued, Tanner Inc. finds two errors in its prior-year statements. (1) On January 1, Year 1, it bought a machine for $90,000 with a 5-year life, no salvage value, and straight-line depreciation, and it recorded the entire $90,000 as Year 1 expense. The machine is still in use. (2) Its December 31, Year 2, ending inventory was overstated by $30,000. Tanner presents single-year financial statements and applies a 25% tax rate to all corrections. What adjustment should Tanner make to its January 1, Year 3, retained earnings?""",
    [("$18,000 increase", "Correct. Machine: $54,000 pre-tax understatement ($90,000 − 2 × $18,000 of depreciation). Inventory: $30,000 overstatement. Net $24,000 × 75%."),
     ("$24,000 increase", "Gets the net pre-tax effect right but omits the 25% tax effect of the corrections."),
     ("$40,500 increase", "Corrects only the machine ($54,000 × 75%). The inventory overstatement also affected retained earnings at December 31, Year 2."),
     ("$45,000 increase", "Reverses the whole $90,000 expense and ignores the $36,000 of depreciation Years 1 and 2 should have carried ($90,000 − $30,000 = $60,000 × 75%)."),
     ("$63,000 increase", "Adds the inventory overstatement instead of subtracting it. Overstated ending inventory overstated income, so it reduces the correction ($54,000 + $30,000) × 75%.")],
    "A",
    """A correction of a prior-period error adjusts the opening balance of retained earnings, net of tax. Machine: expensing $90,000 in Year 1 understated retained earnings at January 1, Year 3, by the asset's carrying amount then, $90,000 − 2 × $18,000 = $54,000. Inventory: the $30,000 overstatement at December 31, Year 2, overstated retained earnings. Net pre-tax effect: $54,000 − $30,000 = $24,000 increase; after 25% tax, $18,000 increase."""),

mcq("far-fair-value-highest-best-use-0001", A3, "Fair value measurements", AP,
    ["ASC 820-10 (fair value measurement: highest and best use)"],
    """Clover Corp. owns land that it uses as a parking lot and intends to keep using that way. The present value of the parking cash flows is $1,900,000. Local zoning allows condominiums on the site. A market-participant developer could complete a condominium project there, which would be worth $2,900,000 to market participants, and completing it would take $450,000 of construction costs plus $150,000 for the profit a market-participant developer would require. Clover must determine the land's fair value under ASC 820. What is the fair value?""",
    [("$1,900,000", "Measures the land at value in Clover's intended use. Fair value assumes the use a market participant would make, not the entity's own plans."),
     ("$2,300,000", "Correct. $2,900,000 − $450,000 construction − $150,000 developer profit."),
     ("$2,450,000", "Deducts the construction costs but not the profit a market-participant developer would require."),
     ("$2,900,000", "Uses the completed project's value and ignores the cost and required profit of developing it.")],
    "B",
    """Fair value reflects the use of the asset by market participants that would maximize its value, provided that use is physically possible, legally permissible, and financially feasible. Zoning permits the development and it is feasible, so the land is valued as development land. A market participant would pay the completed value less the costs and required profit: $2,900,000 − $450,000 − $150,000 = $2,300,000, which exceeds the $1,900,000 value in Clover's current use."""),

mcq("far-income-taxes-deferred-0001", A3, "Accounting for income taxes", AP,
    ["ASC 740-10 (income taxes)"],
    """In its first year of operations, Ridgeway Corp. reports pretax book income of $500,000. Book income includes $30,000 of tax-exempt municipal bond interest and is after deducting $40,000 of nondeductible fines. It is also after warranty expense of $120,000 that is not deductible until claims are paid, and no claims were paid this year. Tax depreciation exceeded book depreciation by $200,000. The enacted tax rate is 25% for all years, and Ridgeway has no other differences. Based on its forecast of taxable income, management concludes that it is more likely than not that $12,000 of the deferred tax asset will not be realized. What is Ridgeway's total income tax expense?""",
    [("$115,500", "Subtracts the valuation allowance from deferred tax expense. An allowance increases deferred tax expense."),
     ("$127,500", "Omits the valuation allowance ($107,500 current + $50,000 − $30,000 deferred)."),
     ("$137,000", "Ignores the permanent differences and computes current tax on $420,000 of taxable income ($105,000 current + $32,000 deferred)."),
     ("$139,500", "Correct. $107,500 current + $32,000 deferred ($50,000 liability − $30,000 asset + $12,000 allowance)."),
     ("$187,500", "Treats the warranty difference as taxable (a liability) instead of deductible, and omits the allowance ($107,500 current + $80,000 deferred).")],
    "D",
    """Taxable income = $500,000 − $30,000 (tax-exempt interest, permanent) + $40,000 (nondeductible fines, permanent) + $120,000 (warranty, deductible later) − $200,000 (excess tax depreciation) = $430,000; current tax = $107,500. Deferred: warranty gives a deferred tax asset of $120,000 × 25% = $30,000, depreciation gives a deferred tax liability of $200,000 × 25% = $50,000, and the valuation allowance adds $12,000 of expense: $50,000 − $30,000 + $12,000 = $32,000. Total income tax expense = $107,500 + $32,000 = $139,500."""),

mcq("far-subsequent-events-0001", A3, "Subsequent events", RU,
    ["ASC 855-10 (subsequent events)"],
    """Alder Corp.'s financial statements for the year ended December 31, Year 5, are issued on March 10, Year 6. Which of the following events, occurring between year-end and the issuance date, requires Alder to adjust its Year 5 financial statements?""",
    [("On February 10, a fire destroys one of Alder's warehouses and all of the inventory stored inside it, with no insurance.", "A condition that arose after year-end. It is disclosed but not recognized in the Year 5 statements."),
     ("On March 1, a court rules against Alder in a suit over an accident in October, Year 5.", "Correct. The accident occurred before year-end, so the ruling gives added evidence about a condition that existed at the balance sheet date."),
     ("On January 20, Alder issues $5,000,000 of bonds to finance the expansion of one of its manufacturing plants.", "A new financing that arose after year-end. It is disclosed but not recognized."),
     ("In February, a broad market downturn sharply reduces the fair value of Alder's investments in trading securities.", "Fair value declines after year-end reflect conditions that arose after the balance sheet date, so they are not recognized.")],
    "B",
    """Subsequent events that give additional evidence about conditions that existed at the balance sheet date are recognized by adjusting the statements. Events reflecting conditions that arose after the balance sheet date are not recognized, though some are disclosed. The court ruling settles an obligation arising from an October, Year 5 accident, so it is recognized. The fire, the bond issue, and the post-year-end decline in fair value all arose after December 31."""),
]

if __name__ == "__main__":
    finalize(ITEMS)
    warnings = audit(ITEMS)
    out = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
    keep = {it["id"] + ".yaml" for it in ITEMS}
    for f in glob.glob(os.path.join(out, "*.yaml")):
        if os.path.basename(f) not in keep:
            os.remove(f)  # retired item: git history keeps it
            print("retired", os.path.basename(f))
    write_items(ITEMS, out)
    from collections import Counter
    c = lambda k: dict(Counter(k(it) for it in ITEMS))
    print("skills", c(lambda i: i["blueprint"]["skill"]))
    print("areas", c(lambda i: i["blueprint"]["area"]))
    print("warnings", warnings)
