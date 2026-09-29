"""FAR batch 01 — 25 items, revised three times after independent quality reviews (see docs/reviews/far-batch-01.md).
Scope and skill tags are checked against the AICPA CPA Exam Blueprints effective January 2026.

Run: python3 scripts/batches/far-batch-01.py  (writes content/far/*.yaml)
Every numeric answer and distractor below was recomputed in code during review.
"""
import os
import glob
from common import mcq as _mcq, finalize, audit, write_items, RU, AP, AN

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = ("Batch 01, revision 3 (2026 blueprint scope, four choices, Analysis items in the blueprint's task frames). "
        "Answers re-solved and every number and distractor computed in code.")


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


ITEMS = [
# ── Area I ──────────────────────────────────────────────────────────────
mcq("far-cash-flows-0003", A1, "Statement of cash flows", AN,
    ["ASC 230-10 (statement of cash flows: classification and indirect method)"],
    """Marlow Corp.'s staff accountant prepared the operating section of the draft statement of cash flows under the indirect method as follows: net income $180,000; plus depreciation $24,000; plus proceeds from the sale of equipment $45,000; less increase in accounts receivable $31,000; plus decrease in inventory $12,000; less dividends paid $20,000; net cash provided by operating activities $210,000. The equipment sold had a carrying amount of $36,000, and the sale is reflected in net income. After correcting the draft to comply with U.S. GAAP, what is net cash provided by operating activities?""",
    [("$156,000", "Moves the proceeds to investing and removes the gain, but leaves the $20,000 of dividends paid in operating activities. Under U.S. GAAP, dividends paid are a financing outflow."),
     ("$176,000", "Correct. $180,000 + $24,000 − $9,000 gain − $31,000 + $12,000. The $45,000 of proceeds is investing and the dividends are financing."),
     ("$185,000", "Removes the proceeds and the dividends but not the $9,000 gain ($45,000 − $36,000) inside net income. The gain's cash is part of the investing inflow, so it must come out of operating."),
     ("$210,000", "Accepts the draft. Proceeds from selling equipment are an investing inflow and dividends paid are a financing outflow; neither belongs in operating activities.")],
    "B",
    """The draft has three errors. (1) The $45,000 of sale proceeds is an investing inflow, so it comes out of operating. (2) Net income includes a $9,000 gain ($45,000 − $36,000 carrying amount); under the indirect method the gain is subtracted, because its cash is reported in investing. (3) Dividends paid are a financing outflow under U.S. GAAP. Corrected: $180,000 + $24,000 − $9,000 − $31,000 + $12,000 = $176,000."""),

mcq("far-cash-flows-0004", A1, "Statement of cash flows", AN,
    ["ASC 230-10 (statement of cash flows: classification of cash receipts and payments; noncash investing and financing activities)"],
    """During the year, Fenwick Ltd. (1) retired bonds with a carrying amount of $192,000 by paying bondholders $200,000 in cash, (2) paid $20,000 of cash dividends to its shareholders, (3) issued common stock for $150,000 in cash, (4) issued common stock to holders of its preferred stock, who converted preferred shares with a carrying amount of $100,000, (5) paid $12,000 of interest on its bonds, and (6) paid $30,000 to reacquire its own common shares as treasury stock. Under U.S. GAAP, what is Fenwick's net cash used in financing activities for the year?""",
    [("$0", "Treats the $100,000 preferred-to-common conversion as a financing inflow. No cash changes hands; it is disclosed as a noncash financing activity."),
     ("$92,000", "Uses the bonds' $192,000 carrying amount instead of the $200,000 of cash paid to retire them. The $8,000 loss is not cash; the financing outflow is the cash paid."),
     ("$100,000", "Correct. −$200,000 bond retirement − $20,000 dividends + $150,000 stock issued − $30,000 treasury stock."),
     ("$112,000", "Also includes the $12,000 of interest paid. Under U.S. GAAP, interest paid is an operating outflow.")],
    "C",
    """Financing activities under U.S. GAAP: cash paid to retire debt (the $200,000 paid, not the carrying amount) −$200,000; dividends paid −$20,000; proceeds from issuing stock +$150,000; purchase of treasury stock −$30,000. Net cash used = $100,000. The preferred-to-common conversion involves no cash and is disclosed as a noncash financing activity, and interest paid is an operating cash flow."""),

mcq("far-nfp-net-assets-0001", A1, "Statement of activities (Not-for-Profit)", RU,
    ["ASC 958-205 (net assets with and without donor restrictions)", "ASU 2016-14 (eliminated the option to imply a time restriction on long-lived assets)"],
    """Clearfield Museum receives a $500,000 gift in Year 1 that the donor restricts to constructing a new gallery. The donor does not say how long the museum must use the gallery. In Year 2, the museum spends the $500,000 completing construction and places the gallery in service. How are Clearfield's net assets affected?""",
    [("Year 1: with donor restrictions +$500,000. Year 2: the full $500,000 is released to without donor restrictions.", "Correct. The purpose restriction is met by the Year 2 construction spending and placing the gallery in service, so the full gift is released in Year 2."),
     ("Year 1: without donor restrictions +$500,000. Year 2: no reclassification is needed because the gift was never restricted.", "Ignores the donor's restriction. A gift restricted to a purpose is reported with donor restrictions when received."),
     ("Year 1: with donor restrictions +$500,000. Year 2: released to without donor restrictions over the gallery's useful life as it is depreciated.", "Former practice, when an entity could imply a time restriction over the asset's life. ASU 2016-14 eliminated that option."),
     ("Year 1: with donor restrictions +$500,000. Year 2: no release until the museum sells or otherwise disposes of the gallery.", "Confuses the restriction on the gift with a restriction on the asset's future use. Absent donor stipulations on use, the restriction ends when the asset is placed in service.")],
    "A",
    """A gift restricted to a purpose is reported as an increase in net assets with donor restrictions. When the donor gives no explicit stipulation about how long a long-lived asset must be used, the restriction is met when the asset is placed in service, and the amount is reclassified as net assets released from restrictions. Since ASU 2016-14, an entity may no longer imply a time restriction that spreads the release over the asset's useful life."""),

mcq("far-consolidated-statements-0001", A1, "Consolidated financial statements", AN,
    ["ASC 805-20 (noncontrolling interest measured at acquisition-date fair value)", "ASC 810-10 (noncontrolling interests in consolidated financial statements)"],
    """On January 1, Year 1, Pratt Corp. acquires 80% of the voting stock of Tern Inc. for $800,000 in cash. The acquisition-date fair value of the 20% noncontrolling interest is $200,000. Tern's net assets had a book value of $700,000. Its equipment, with a 5-year remaining life and straight-line depreciation, had a fair value $100,000 above book value, and every other identifiable asset and liability had a fair value equal to book value. For Year 1, Tern reports net income of $150,000 on its own books and pays dividends of $50,000. Pratt's draft December 31, Year 1, consolidated balance sheet reports noncontrolling interest of $160,000. After any correction needed, at what amount should noncontrolling interest be reported?""",
    [("$160,000", "Accepts the draft, which is 20% of the $800,000 of net assets on Tern's own year-end books. Noncontrolling interest starts at its acquisition-date fair value, not at a share of the subsidiary's book value."),
     ("$176,000", "Starts from 20% of the fair value of Tern's identifiable net assets ($160,000), which leaves out the noncontrolling interest's share of goodwill. U.S. GAAP measures noncontrolling interest at its full acquisition-date fair value."),
     ("$216,000", "Correct. $200,000 + 20% × ($150,000 − $20,000 extra depreciation) − 20% × $50,000 dividends."),
     ("$220,000", "Allocates 20% of Tern's reported $150,000 without first deducting the $20,000 of depreciation on the equipment's fair value step-up.")],
    "C",
    """Under ASC 805 and 810, noncontrolling interest is measured at acquisition-date fair value ($200,000), which includes its share of goodwill. It is then increased by its share of the subsidiary's income as adjusted for the acquisition-date fair value differences and reduced by its share of dividends. Consolidated Year 1 income of Tern = $150,000 − $100,000 ÷ 5 = $130,000; the noncontrolling interest's share is $26,000. Dividends to the noncontrolling interest are 20% × $50,000 = $10,000. NCI = $200,000 + $26,000 − $10,000 = $216,000."""),

mcq("far-nfp-contributions-0001", A3, "Revenue recognition", AP,
    ["ASC 958-605 (contributions received, including conditional contributions)", "ASC 958-205 (net assets with and without donor restrictions)", "ASU 2018-08 (clarifying the scope and the accounting guidance for contributions)"],
    """Harbor Arts Foundation, a not-for-profit entity, has these transactions in Year 1. (1) On December 31 it receives a written promise of $80,000 payable on January 1, Year 3; nothing else is required of the foundation to receive it, and the donor states no use for the money. The promise has a present value of $72,000. (2) It receives $60,000 in cash that the donor requires to be used for scholarships, and it spends $25,000 on qualifying scholarships during Year 1. (3) It receives $150,000 in cash under an agreement that lets the donor recover the money if the foundation does not raise $150,000 of matching gifts by the end of Year 2. By December 31, Year 1, the foundation has raised no matching gifts. (4) It receives a $100,000 cash gift with no donor stipulations. The foundation reports every restricted gift as with donor restrictions when received, even if the restriction is met in the same period. Ignoring interest accretion, what is the net change in net assets with donor restrictions for Year 1?""",
    [("$107,000", "Correct. $72,000 for the promise (restricted by time) + $60,000 for the scholarship gift − $25,000 released when the scholarships were funded. The $150,000 is a refundable advance, and the $100,000 gift is without donor restrictions."),
     ("$115,000", "Measures the promise at its $80,000 face amount. A promise due in a future period is recorded at present value."),
     ("$132,000", "Reports the restricted contributions only and leaves out the $25,000 release. Spending on the donor's purpose moves that amount out of net assets with donor restrictions, so the net change is smaller."),
     ("$257,000", "Counts the $150,000 as revenue with donor restrictions. Because the donor can recover it until the matching gifts are raised, it is a refundable advance (a liability), not revenue.")],
    "A",
    """The $80,000 promise carries no condition other than the passage of time, so it is recognized now at present value ($72,000) as an increase in net assets with donor restrictions (time restriction). The $60,000 scholarship gift is restricted to a purpose; spending $25,000 on it releases that amount, leaving a $35,000 net increase. The $150,000 depends on a measurable barrier (matching gifts) and includes a right of return, so it is not revenue until the barrier is overcome; the cash is a refundable advance. The $100,000 gift is without donor restrictions. Net change in net assets with donor restrictions: $72,000 + $60,000 − $25,000 = $107,000 increase."""),

mcq("far-eps-diluted-0001", A1, "Public Company Reporting Topics", AP,
    ["ASC 260-10 (earnings per share)", "ASU 2020-06 (if-converted method for convertible instruments)"],
    """Kestrel Corp. reports net income of $1,200,000 and 500,000 weighted-average common shares outstanding for the year. It has cumulative preferred stock on which $100,000 of dividends accrued this year, none of which was declared. Kestrel also has (1) options to buy 40,000 common shares at $30 per share, outstanding all year, with an average market price of $50 during the year, and (2) $1,000,000 of 6% convertible bonds issued at par and outstanding all year, convertible into 20,000 common shares. Kestrel's tax rate is 25%. What are Kestrel's diluted earnings per share, rounded to the nearest cent?""",
    [("$2.04", "Adds all 40,000 option shares. Under the treasury stock method only the shares not covered by assumed repurchase (16,000) are added."),
     ("$2.13", "Correct. ($1,200,000 − $100,000) ÷ (500,000 + 16,000 option shares)."),
     ("$2.14", "Includes the convertible bonds. Their incremental effect is $45,000 ÷ 20,000 = $2.25 per share, above the $2.13 diluted EPS before the bonds, so they are antidilutive and excluded."),
     ("$2.33", "Does not deduct the $100,000 of cumulative preferred dividends. Cumulative dividends are deducted whether or not declared.")],
    "B",
    """Income available to common = $1,200,000 − $100,000 cumulative preferred dividends = $1,100,000. Options (treasury stock method): 40,000 − (40,000 × $30 ÷ $50) = 16,000 incremental shares, which are dilutive. Convertible bonds (if-converted): add back after-tax interest of $60,000 × (1 − 25%) = $45,000 and add 20,000 shares; the incremental effect is $2.25 per share, higher than the $2.13 EPS so far, so the bonds are antidilutive and excluded. Diluted EPS = $1,100,000 ÷ 516,000 = $2.13."""),

mcq("far-comprehensive-income-0002", A1, "Income statement", AN,
    ["ASC 220-10 (comprehensive income; reclassification adjustments)", "ASC 320-10 (available-for-sale debt securities)", "ASC 321-10 (equity securities)", "ASC 830-20 (foreign currency transactions)"],
    """Delmar Inc.'s draft statement of comprehensive income reports net income of $400,000 and other comprehensive income (OCI) of $97,500, for comprehensive income of $497,500. All amounts below are net of tax. Net income includes a $22,500 gain on the sale of available-for-sale debt securities that Delmar bought three years ago and whose fair value did not change during the current year before the sale, and a $15,000 gain from the increase in fair value of an equity investment that has a readily determinable fair value. The draft's OCI consists of $67,500 of unrealized holding gains that arose this year on Delmar's remaining available-for-sale debt securities and a $30,000 gain from remeasuring a euro-denominated account payable at the year-end exchange rate. What is Delmar's corrected comprehensive income for the year?""",
    [("$445,000", "Takes the $30,000 exchange gain out of OCI but never adds it to net income. A remeasurement gain on a foreign-currency payable is a transaction gain reported in net income, so it stays in comprehensive income."),
     ("$475,000", "Correct. Net income $430,000 ($400,000 + $30,000 transaction gain) + OCI $45,000 ($67,500 − $22,500 reclassification adjustment)."),
     ("$497,500", "Accepts the draft total. Moving the exchange gain to net income does not change the total, but the draft omits the reclassification adjustment: the $22,500 gain sat in OCI in earlier years and is now in net income, so it must come out of OCI."),
     ("$505,000", "Adds the $30,000 exchange gain to net income and makes the reclassification adjustment, but also leaves the gain in OCI, so it is counted twice.")],
    "B",
    """The draft has two errors. (1) The $30,000 gain on remeasuring a euro payable is a foreign-currency transaction gain, which is reported in net income, not OCI; corrected net income is $430,000. (2) The $22,500 gain on the AFS securities was recognized in OCI as an unrealized gain in earlier years (their fair value did not change this year), so moving it into net income on the sale requires a reclassification adjustment out of OCI: $67,500 − $22,500 = $45,000. The $15,000 equity-investment gain is correctly in net income (ASC 321). Comprehensive income = $430,000 + $45,000 = $475,000."""),

mcq("far-governmental-fund-types-0001", A1, "Purpose of funds", AP,
    ["GASB Statement No. 54 (governmental fund type definitions)"],
    """Northgate City accounts for the four activities below. Which activity is reported in a capital projects fund?""",
    [("Bond proceeds restricted for a new fire station, plus the related construction costs", "Correct. Capital projects funds account for resources restricted, committed, or assigned to capital outlay."),
     ("Water service charges that are set to recover the full cost of running the city's water utility", "Reported in an enterprise fund, which accounts for activities financed by fees charged to external users."),
     ("Resources accumulated to pay principal and interest on the city's general obligation bonds", "Reported in a debt service fund, which accounts for resources set aside for debt payments."),
     ("Hotel occupancy tax revenue that the city council has committed to tourism promotion", "Reported in a special revenue fund, which accounts for revenue sources restricted or committed to a specific operating purpose.")],
    "A",
    """A capital projects fund accounts for financial resources that are restricted, committed, or assigned to expenditure for capital outlay, such as bond proceeds and the construction of a fire station. Debt service funds accumulate resources for principal and interest payments, special revenue funds account for revenue sources restricted or committed for specific operating purposes, and enterprise funds account for fee-supported business-type activities."""),

# ── Area II ─────────────────────────────────────────────────────────────
mcq("far-ppe-reconciliation-0001", A2, "Property, plant and equipment", AN,
    ["ASC 360-10 (property, plant and equipment: cost, derecognition)", "ASC 610-20 (gains and losses from the derecognition of nonfinancial assets)"],
    """At year-end, Ashby Co.'s fixed-asset subledger shows total equipment cost of $2,450,000, while the general ledger equipment account shows $2,500,000. Ashby's draft pretax income is $400,000. Investigating the difference, the controller finds two items. First, in October Ashby sold a machine with a cost of $60,000 and accumulated depreciation of $48,000 for $15,000 in cash, after recording depreciation through the date of sale; the subledger removed the machine, and the general ledger entry debited cash and credited gain on sale for $15,000. Second, $10,000 of freight and installation for new equipment placed in service on December 31 is included in the subledger cost but was charged to repairs expense in the general ledger. Ignore depreciation on the new equipment for the year and income taxes. What is Ashby's corrected pretax income?""",
    [("$350,000", "Removes the machine's $60,000 cost without its $48,000 of accumulated depreciation, turning the $15,000 gain into a $45,000 loss."),
     ("$388,000", "Corrects the sale but leaves the $10,000 of freight and installation in expense. Costs to bring equipment to its location and ready it for use are part of its cost."),
     ("$398,000", "Correct. The gain falls from $15,000 to $3,000 ($15,000 − $12,000 carrying amount), and the $10,000 of freight and installation is capitalized: $400,000 − $12,000 + $10,000."),
     ("$413,000", "Adds the correct $3,000 gain on top of the $15,000 already recorded instead of replacing it.")],
    "C",
    """Reconcile first: the general ledger still carries the sold machine ($60,000) and is missing the capitalized freight and installation ($10,000), so $2,500,000 − $60,000 + $10,000 = $2,450,000 agrees with the subledger. Sale: the carrying amount was $60,000 − $48,000 = $12,000, so the gain is $15,000 − $12,000 = $3,000, not $15,000; correcting it reduces income by $12,000 (Dr Accumulated depreciation $48,000, Dr Gain $12,000, Cr Equipment $60,000). Freight and installation are costs of getting the asset ready for use, so capitalizing them increases income by $10,000. Corrected pretax income: $400,000 − $12,000 + $10,000 = $398,000."""),

mcq("far-ppe-exchange-0001", A2, "Property, plant and equipment", AP,
    ["ASC 845-10 (nonmonetary transactions)"],
    """Harwick Corp. exchanges old machinery (book value $180,000; fair value $210,000) plus $40,000 cash for new equipment with a fair value of $250,000. The old machinery stamped metal brackets for a product line Harwick is discontinuing; the new equipment will mold plastic housings for a different customer base, under three-year supply contracts at different volumes and prices. What gain does Harwick recognize, and at what amount is the new equipment recorded?""",
    [("$30,000 gain; new equipment $250,000", "Correct. The new equipment serves a different product, customers, and pricing, so Harwick's future cash flows change significantly and the exchange has commercial substance: the gain is fair value minus book value of the asset given up, and the new asset is recorded at fair value."),
     ("$0 gain; new equipment $220,000", "Carryover-basis treatment, which applies only when an exchange lacks commercial substance. Replacing a discontinued line with a different product sold under new contracts changes Harwick's future cash flows significantly."),
     ("$70,000 gain; new equipment $250,000", "Compares the new asset's fair value to the old book value and ignores the $40,000 of cash paid."),
     ("$30,000 gain; new equipment $220,000", "Mixes the two methods: recognizes the gain but records the asset at carryover basis.")],
    "A",
    """An exchange has commercial substance when the entity's future cash flows are expected to change significantly as a result of it. Here the new equipment makes a different product for different customers at different volumes and prices, so the risk, timing, and amount of its cash flows differ from the old machinery's. With commercial substance, the exchange is measured at fair value. Gain = $210,000 fair value − $180,000 book value = $30,000. The new equipment is recorded at $210,000 + $40,000 cash = $250,000, which equals its fair value."""),

mcq("far-inventory-lcnrv-0001", A2, "Inventory", AP,
    ["ASC 330-10 (inventory; ASU 2015-11 lower of cost and net realizable value)"],
    """Crestview Co. uses FIFO and applies the lower of cost and net realizable value to each product separately. At year-end: Product A has 1,000 units with FIFO cost of $12.00, selling price of $14.50, cost to complete and sell of $3.00, and replacement cost of $11.20 per unit. Product B has 2,000 units with FIFO cost of $8.00, selling price of $10.00, cost to complete and sell of $2.50, and replacement cost of $7.60 per unit. Product C has 500 units with FIFO cost of $20.00, selling price of $25.00, cost to complete and sell of $4.00, and replacement cost of $20.50 per unit. What inventory write-down should Crestview recognize?""",
    [("$0", "Compares selling price with cost and ignores the costs to complete and sell that net realizable value subtracts. Every selling price exceeds its cost, so this test finds no write-down."),
     ("$1,000", "Applies the test to the inventory as a whole: total cost $38,000 against total NRV $37,000. Crestview applies the test product by product, so Product C's surplus cannot offset the shortfalls."),
     ("$1,500", "Correct. NRV is selling price less costs to complete and sell; Products A and B are each $0.50 per unit below cost, and Product C is not written down."),
     ("$1,600", "Measures the shortfall against replacement cost, the old lower-of-cost-or-market approach. FIFO and average-cost inventory use NRV; replacement cost applies only to LIFO and the retail inventory method.")],
    "C",
    """For FIFO or average-cost inventory, measure each product at the lower of cost and NRV. Product A: NRV $14.50 − $3.00 = $11.50, below cost by $0.50 × 1,000 = $500. Product B: NRV $10.00 − $2.50 = $7.50, below cost by $0.50 × 2,000 = $1,000. Product C: NRV $25.00 − $4.00 = $21.00, above the $20.00 cost, so no write-down and no write-up. Total write-down: $1,500."""),

mcq("far-equity-paid-in-capital-0002", A1, "Statement of changes in equity", AN,
    ["ASC 505-10 (equity securities issued for noncash consideration)", "ASC 718 (share-based payments to nonemployees for goods, after ASU 2018-07)", "SEC Staff Accounting Bulletin Topic 5.A (expenses of offering)"],
    """During the year, Redford Corp. issues $2 par value common stock as follows: (1) 5,000 shares sold for cash at $18 per share, and (2) 3,000 shares issued for a parcel of land. On the exchange date, Redford's shares trade actively on a national exchange at $19 per share, and an independent appraisal values the land at $60,000. Redford also pays $9,000 of legal and underwriting costs directly attributable to issuing the shares. Redford's draft year-end statements show land of $60,000, additional paid-in capital of $134,000 from these issuances, and $9,000 of legal and underwriting fees in general and administrative expense. After any corrections needed, what is the total additional paid-in capital from these issuances?""",
    [("$122,000", "Correct. Cash sale $80,000 + land $51,000 (3,000 × $17) − $9,000 of offering costs."),
     ("$125,000", "Nets the offering costs against APIC but keeps the land at its $60,000 appraisal. Shares issued for an asset are measured at the shares' fair value, and the quoted $19 price gives $57,000."),
     ("$131,000", "Measures the land at the share price but leaves the $9,000 of offering costs in expense. Direct costs of issuing shares reduce the proceeds, so they reduce APIC."),
     ("$134,000", "Accepts the draft, which records the land at the appraisal ($54,000 of APIC) and expenses the offering costs.")],
    "A",
    """Since ASU 2018-07, shares issued to a nonemployee for goods used in operations are measured under ASC 718 at the fair value of the shares issued; the quoted price in an active market is also more reliable than an appraisal. The land is recorded at 3,000 × $19 = $57,000: $6,000 of par and $51,000 of APIC. Cash sale: 5,000 × ($18 − $2) = $80,000 of APIC. Direct costs of issuing equity reduce the proceeds, so the $9,000 is reclassified from expense to a reduction of APIC. Total: $80,000 + $51,000 − $9,000 = $122,000."""),

mcq("far-investments-afs-credit-loss-0002", A2, "Investments (Financial assets at fair value)", AP,
    ["ASC 326-30 (credit losses on available-for-sale debt securities)"],
    """Foxworth Inc. holds available-for-sale debt securities whose amortized cost was $100,000 at the end of both Year 1 and Year 2. At the end of Year 1, Foxworth recorded a $2,000 allowance for credit losses on them. At the end of Year 2, their fair value is $88,000, and the present value of the cash flows Foxworth expects to collect, discounted at the securities' effective interest rate, is $93,000. Foxworth does not intend to sell the securities, and it is not more likely than not that it will be required to sell them before recovering their amortized cost. What credit loss expense should Foxworth recognize in net income for Year 2?""",
    [("$5,000", "Correct. The allowance must be $7,000 ($100,000 − $93,000); it already holds $2,000, so Year 2 expense is $5,000."),
     ("$7,000", "Records the full credit loss as this year's expense and ignores the $2,000 already in the allowance."),
     ("$10,000", "Treats the whole $12,000 decline below amortized cost as a credit loss, less the existing allowance. The $5,000 of the decline not explained by expected cash flows goes to OCI."),
     ("$12,000", "Recognizes the whole decline in earnings, as if the securities were trading, and ignores the existing allowance.")],
    "A",
    """For an AFS debt security the holder neither intends nor is likely to be required to sell, the credit loss is amortized cost minus the present value of expected cash flows, limited to the amount by which fair value is below amortized cost: $100,000 − $93,000 = $7,000, within the $12,000 limit. The allowance is adjusted from $2,000 to $7,000, so Year 2 credit loss expense is $5,000. The remaining $5,000 of the decline ($12,000 − $7,000) is reported in other comprehensive income."""),

mcq("far-equity-retirement-0002", A2, "Equity", AP,
    ["ASC 505-30 (treasury stock and retirement of shares)"],
    """Mercer Inc. has 10,000 shares of $2 par common stock outstanding, all originally issued at $14 per share. Its equity also includes $1,500 of additional paid-in capital from earlier sales, at more than cost, of treasury shares from that same issue. Mercer reacquires 1,000 shares at $20 per share and retires them immediately. Mercer's policy is to charge additional paid-in capital on a retirement to the maximum extent ASC 505-30 permits and to charge any remainder to retained earnings. What amount is debited to retained earnings on the retirement?""",
    [("$4,500", "Correct. The $18,000 excess over par is charged first to the pro rata original APIC ($12,000) and the $1,500 of APIC from treasury transactions in the same issue; the remaining $4,500 goes to retained earnings."),
     ("$6,000", "Charges only the pro rata original APIC ($12,000). APIC from earlier treasury stock gains on the same issue can also absorb the excess."),
     ("$16,500", "Charges only the $1,500 of APIC from treasury transactions and none of the $12,000 of original APIC on the retired shares."),
     ("$18,000", "Charges the entire excess over par to retained earnings. ASC 505-30 permits that alternative, but Mercer's policy is to use APIC first.")],
    "A",
    """On retirement, common stock is debited at par (1,000 × $2 = $2,000) and the $18,000 excess of cost over par is charged either entirely to retained earnings or allocated between APIC and retained earnings. When it is allocated, the APIC charge is limited to APIC from earlier retirements and net gains on treasury stock of the same issue ($1,500) plus the pro rata APIC on the same issue (1,000 × $12 = $12,000). Mercer charges APIC to that limit, $13,500, and retained earnings $18,000 − $13,500 = $4,500."""),

mcq("far-receivables-credit-losses-0002", A2, "Trade receivables", AN,
    ["ASC 326-20 (credit losses on financial instruments measured at amortized cost)", "ASC 310-10 (receivables)", "ASU 2025-05 (practical expedient for current receivables; not elected here)"],
    """At year-end, Orchard Supply Co.'s accounts receivable subledger totals $1,007,000, and the general ledger control account shows $1,018,000. Orchard's investigation finds two reconciling items, both involving customers in its main customer pool: the December 18 sales journal batch of $18,000 was posted to the control account twice, and a $7,000 credit memo for goods returned on December 30 was posted to the control account but not to the customer's subledger account. Of the correct receivables balance, $150,000 is owed by one customer that has filed for bankruptcy; Orchard expects to collect 30% of that balance in the proceedings. The remaining balances are owed by customers with similar credit profiles. Orchard's historical loss rate on such balances is 3%, and its reasonable and supportable forecast indicates losses 1 percentage point above that rate. Orchard does not elect the practical expedient for current trade receivables in ASU 2025-05. Before adjustment, the allowance for credit losses has a $25,000 credit balance. After the reconciling items are corrected, what credit loss expense should Orchard record for the year?""",
    [("$114,000", "Correct. The corrected receivables balance is $1,000,000, so the pool is $850,000. Required allowance $105,000 + $850,000 × 4% = $139,000, less the $25,000 already in the allowance."),
     ("$105,500", "Uses the 3% historical rate for the pool. Expected credit losses must reflect reasonable and supportable forecasts, which raise the rate to 4%."),
     ("$114,720", "Uses the unadjusted control account ($1,018,000, a pool of $868,000). The duplicated $18,000 batch is not a real receivable."),
     ("$139,000", "Records the whole required allowance as expense and ignores the $25,000 credit balance already in the allowance.")],
    "A",
    """First reconcile. The control account is overstated by the duplicated $18,000 batch: $1,018,000 − $18,000 = $1,000,000. The subledger is overstated by the unposted $7,000 credit memo: $1,007,000 − $7,000 = $1,000,000. Both records agree at $1,000,000 after correction, so the pool is $1,000,000 − $150,000 = $850,000. Under the current expected credit loss model, the bankrupt customer is evaluated on its own: $150,000 × 70% = $105,000. The pool's historical 3% is adjusted for the forecast to 4%: $850,000 × 4% = $34,000. Required allowance = $139,000; with a $25,000 credit balance already recorded, credit loss expense is $114,000."""),

mcq("far-debt-extinguishment-0001", A2, "Debt (Notes and bonds payable)", AP,
    ["ASC 470-50 (debt modifications and extinguishments)", "ASC 835-30 (interest method and presentation of debt issuance costs)"],
    """On January 1, Year 1, Sable Corp. issues $1,000,000 of five-year, 6% bonds, with interest paid each December 31, for $920,146, a price that yields 8%. Sable pays $20,000 of issuance costs and amortizes them straight-line over the five years, because the result is not materially different from the interest method. Sable amortizes the bond discount using the effective interest method and rounds to the nearest dollar at each step. On December 31, Year 2, immediately after paying interest, Sable repurchases all of the bonds in the open market for $1,020,000. What loss on extinguishment does Sable recognize?""",
    [("$71,541", "Ignores the $12,000 of unamortized issuance costs, which are part of the net carrying amount and are written off in the loss."),
     ("$79,912", "Amortizes the discount straight-line ($15,971 a year). The stem calls for the effective interest method, which amortizes $13,612 and then $14,701."),
     ("$83,541", "Correct. $1,020,000 − ($948,459 carrying amount − $12,000 unamortized issuance costs)."),
     ("$91,541", "Treats all $20,000 of issuance costs as unamortized. Two of five years have passed, so $8,000 has been amortized and $12,000 remains.")],
    "C",
    """Year 1 interest expense = $920,146 × 8% = $73,612; cash interest $60,000; discount amortization $13,612; carrying amount $933,758. Year 2 interest expense = $933,758 × 8% = $74,701; amortization $14,701; carrying amount $948,459. Unamortized issuance costs = $20,000 − 2 × $4,000 = $12,000, so the net carrying amount is $936,459. Loss = $1,020,000 − $936,459 = $83,541."""),

mcq("far-intangibles-cloud-computing-0001", A2, "Intangible assets", AP,
    ["ASC 350-40 (internal-use software; implementation costs of a hosting arrangement that is a service contract)", "ASU 2018-15 (customer's accounting for implementation costs in a cloud computing arrangement)", "ASU 2025-06 (targeted improvements to internal-use software; same result here)"],
    """On January 1, Year 1, Lark Co. signs a noncancellable 3-year contract to access a vendor's cloud-hosted ERP software. Lark has no right to take possession of the software, and it is reasonably certain to exercise its option to renew the contract for 2 more years. Before the software became ready for its intended use on July 1, Year 1, Lark incurred these costs: $25,000 to evaluate vendors before selecting this one; $180,000 for configuration, coding, and testing of interfaces; $30,000 to convert and cleanse legacy data; and $20,000 to train employees. Lark amortizes capitalized costs straight-line. Excluding the hosting fees, what total expense should Lark recognize in Year 1 related to these costs?""",
    [("$66,000", "Capitalizes the $30,000 of data conversion with the configuration costs ($25,000 + $20,000 + $210,000 ÷ 5 × ½). Data conversion costs are expensed as incurred."),
     ("$93,000", "Correct. $25,000 + $30,000 + $20,000 expensed as incurred, plus $180,000 ÷ 5 years × ½ year = $18,000 of amortization."),
     ("$105,000", "Amortizes over the 3-year noncancellable term. The term includes renewal periods Lark is reasonably certain to exercise, so it is 5 years."),
     ("$111,000", "Amortizes for the full year. Amortization begins when the software is ready for its intended use on July 1.")],
    "B",
    """A cloud computing arrangement without a right to take possession of the software is a service contract, and its implementation costs are capitalized or expensed as for internal-use software. Evaluating and selecting a vendor ($25,000) happens before the entity commits to a project, and data conversion ($30,000) and training ($20,000) are not costs of developing the software, so all three are expensed as incurred. (ASU 2025-06, which removes the project-stage model from ASC 350-40, does not change these conclusions.) Application-development costs (configuration, coding, and testing, $180,000) are capitalized and amortized straight-line over the term of the arrangement, including renewals Lark is reasonably certain to exercise (5 years), starting when the software is ready for its intended use: $180,000 ÷ 5 × ½ = $18,000. Total Year 1 expense: $25,000 + $30,000 + $20,000 + $18,000 = $93,000."""),

mcq("far-equity-method-0001", A2, "Investments (Equity method investments)", AP,
    ["ASC 323-10 (equity method investments)"],
    """On January 1, Year 1, Pillar Corp. pays $1,500,000 for 30% of the common stock of Quarry Inc. and can significantly influence Quarry's operating decisions. Quarry's net assets have a book value of $4,000,000. Quarry's equipment, which has a 4-year remaining life and is depreciated straight-line, has a fair value $400,000 above its book value, and no other asset or liability has a fair value that differs from book value. For the year, Quarry reports net income of $600,000 and pays dividends of $200,000. During Year 1, Pillar sold inventory to Quarry at a profit of $100,000. Quarry resold 60% of that inventory to outsiders during the year and holds the rest at year-end. Ignore income taxes, and assume Pillar has not elected the fair value option. What is the carrying amount of Pillar's investment in Quarry at December 31, Year 1?""",
    [("$1,550,000", "Eliminates 100% of the unrealized profit ($40,000). Pillar eliminates only its 30% share ($12,000)."),
     ("$1,578,000", "Correct. $1,500,000 + $180,000 share of income − $60,000 dividends − $30,000 equipment amortization − $12,000 unrealized profit."),
     ("$1,590,000", "Does not eliminate any of the unrealized profit on the inventory Quarry still holds."),
     ("$1,608,000", "Omits the $30,000 amortization of the equipment's basis difference.")],
    "B",
    """Excess of cost over share of book value = $1,500,000 − (30% × $4,000,000) = $300,000. Of that, 30% × $400,000 = $120,000 relates to the equipment (amortized over 4 years, $30,000 a year) and $180,000 is goodwill (not amortized). Carrying amount = $1,500,000 + 30% × $600,000 ($180,000) − 30% × $200,000 ($60,000 dividends) − $30,000 amortization − 30% × (40% × $100,000) = $12,000 unrealized profit = $1,578,000."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("far-contingencies-0002", A3, "Contingencies and commitments", AN,
    ["ASC 450-20 (loss contingencies: recognition, measurement within a range, disclosure)"],
    """Bravo Corp.'s December 31 financial statements have not yet been issued. Its outside counsel's letter describes two lawsuits filed against Bravo during the year. Claim 1: last year the same court ruled against a competitor on nearly identical facts, Bravo has offered to settle, and counsel expects Bravo to pay damages of between $400,000 and $900,000, with no amount in that range a better estimate than any other. Claim 2: counsel believes Bravo's defenses are stronger than the plaintiff's case and that Bravo will more likely than not prevail, but counsel cannot dismiss the chance of an adverse judgment; if Bravo loses, damages would be about $300,000. What total liability should Bravo accrue for the two lawsuits at December 31?""",
    [("$400,000", "Correct. Claim 1 is probable with no best estimate in the range, so Bravo accrues the minimum and discloses the further $500,000 of possible loss. Claim 2 is only disclosed."),
     ("$650,000", "Accrues the midpoint of Claim 1's range. When no amount in a range is a better estimate than any other, U.S. GAAP accrues the minimum."),
     ("$700,000", "Also accrues Claim 2. A loss that is more than remote but less than probable is disclosed, not accrued."),
     ("$900,000", "Accrues the top of Claim 1's range. The minimum is accrued, and the rest of the range is disclosed.")],
    "A",
    """Claim 1: the adverse precedent, the settlement offer, and counsel's expectation of payment make the loss probable, and it can be estimated as a range. With no amount in the range better than any other, ASC 450-20 requires accruing the minimum ($400,000) and disclosing the reasonably possible additional loss of up to $500,000. Claim 2: a loss that counsel thinks is less likely than not but cannot dismiss is reasonably possible, so Bravo discloses its nature and the $300,000 estimate but records nothing. Total accrual: $400,000."""),

mcq("far-revenue-allocation-0003", A3, "Revenue recognition", AP,
    ["ASC 606-10 (identifying performance obligations; allocating a discount to fewer than all performance obligations)"],
    """Harmon Technologies enters into a contract to sell a software license, implementation services, and one year of post-contract support for a total of $370,000. Harmon regularly sells each item separately at these standalone selling prices: license $240,000, implementation $100,000, and support $60,000. It also regularly sells the license and one year of support together, without implementation, for $270,000. The implementation is a standard installation that does not modify the software, and several other firms offer it. How much of the transaction price should Harmon allocate to the license?""",
    [("$210,000", "Assigns the entire $30,000 discount to the license. The discount belongs to the license-and-support bundle and is shared between those two in proportion to their standalone selling prices."),
     ("$216,000", "Correct. The $30,000 discount matches the regular license-and-support bundle, so it is allocated to those two only: $270,000 × $240,000 ÷ $300,000."),
     ("$222,000", "Spreads the discount across all three obligations ($370,000 × $240,000 ÷ $400,000). Observable evidence shows the discount relates only to the license and support."),
     ("$240,000", "Uses the license's standalone selling price and ignores the discount.")],
    "B",
    """The implementation does not modify the software and is available from other firms, so the license, implementation, and support are distinct performance obligations. The contract's discount is $400,000 − $370,000 = $30,000. Harmon regularly sells each item separately, and regularly sells the license and support together at the same $30,000 discount, which is observable evidence that the whole discount relates to those two. Implementation gets its $100,000 standalone selling price, and the remaining $270,000 is split between license and support by their standalone selling prices: $270,000 × $240,000 ÷ $300,000 = $216,000."""),

mcq("far-lessee-finance-0001", A3, "Lessee accounting", AP,
    ["ASC 842-20 (lessee accounting: finance leases)"],
    """On January 1, Year 1, Reeves Corp. commences a 5-year finance lease. The lease liability at commencement is $200,000 (rounded), the annual payment of $50,000 is due each December 31, and the discount rate is 8%. The right-of-use asset is amortized straight-line over the lease term. What total lease-related expense does Reeves recognize in Year 2?""",
    [("$53,280", "Correct. Year 2 interest of $13,280 on a $166,000 opening liability, plus $40,000 of amortization."),
     ("$56,000", "Uses Year 1 interest ($16,000) without reducing the liability for the Year 1 principal payment."),
     ("$40,000", "Includes only amortization. A finance lease also has interest expense."),
     ("$50,000", "Treats the cash payment as the expense.")],
    "A",
    """Year 1: interest $16,000, principal reduction $34,000, ending liability $166,000. Year 2: interest = $166,000 × 8% = $13,280. Amortization = $200,000 ÷ 5 = $40,000. Total Year 2 expense = $53,280."""),

mcq("far-accounting-errors-0001", A3, "Accounting changes and error corrections", AN,
    ["ASC 250-10 (accounting changes and error corrections)"],
    """In Year 3, before its Year 3 financial statements are issued, Tanner Inc. finds two errors in its prior-year statements. (1) On January 1, Year 1, it bought a machine for $90,000 with a 5-year life, no salvage value, and straight-line depreciation, and it recorded the entire $90,000 as Year 1 expense. The machine is still in use. (2) Its December 31, Year 2, ending inventory was overstated by $30,000. Tanner presents single-year financial statements and applies a 25% tax rate to all corrections. What adjustment should Tanner make to its January 1, Year 3, retained earnings?""",
    [("$18,000 increase", "Correct. Machine: $54,000 pre-tax understatement ($90,000 − 2 × $18,000 of depreciation). Inventory: $30,000 overstatement. Net $24,000 × 75%."),
     ("$24,000 increase", "Gets the net pre-tax effect right but omits the 25% tax effect of the corrections."),
     ("$40,500 increase", "Corrects only the machine ($54,000 × 75%). The inventory overstatement also affected retained earnings at December 31, Year 2."),
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
     ("$139,500", "Correct. $107,500 current + $32,000 deferred ($50,000 liability − $30,000 asset + $12,000 allowance).")],
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
