"""FAR batch 03 — 25 items written from scratch to deepen the groups batches 01 and 02 touched only once
(see docs/reviews/far-batch-03.md). Target skill mix 3 / 12 / 10 to bring the bank back inside the blueprint ranges.
Scope and skill tags follow the AICPA CPA Exam Blueprints effective January 2026.

Run: python3 scripts/batches/far-batch-03.py  (writes content/far/*.yaml; leaves other batches' files alone)
Every numeric answer and distractor below was computed in code.
"""
import os
from common import mcq as _mcq, finalize, audit, write_items, RU, AP, AN

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 03. Written from scratch; answers solved and every number and distractor computed in code."


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


ITEMS = [
# ── Area I ──────────────────────────────────────────────────────────────
mcq("far-cash-flows-0005", A1, "Statement of cash flows", AN,
    ["ASC 230-10 (classification of cash receipts and payments; noncash investing and financing activities)"],
    """Brenner Co.'s staff accountant prepared the investing section of the draft statement of cash flows: purchases of equipment $(250,000); proceeds from sales of available-for-sale debt securities $90,000; interest and dividends received $12,000; loan made to a supplier $(40,000); principal collected on that loan $10,000; purchases of debt securities bought and held principally to sell in the near term $(30,000); net cash used in investing activities $(208,000). Supporting documents show that $100,000 of the equipment was acquired by signing a note payable to the seller. After correcting the draft to comply with U.S. GAAP, what is net cash used in investing activities?""",
    [("$90,000", "Correct. −$150,000 cash paid for equipment + $90,000 AFS proceeds − $40,000 loan + $10,000 collected."),
     ("$120,000", "Keeps the $30,000 of trading-security purchases in investing. Securities bought principally to sell in the near term are classified by their nature, as operating cash flows."),
     ("$190,000", "Keeps the $100,000 of equipment financed by the seller. Buying an asset with a note is a noncash investing and financing activity, disclosed but not in the cash flow totals."),
     ("$208,000", "Accepts the draft, which also counts interest and dividends received (operating under U.S. GAAP), the note-financed equipment, and the trading securities.")],
    "A",
    """Three corrections. (1) Only $150,000 of the equipment was paid in cash; the $100,000 financed by a note is a noncash activity disclosed separately. (2) Interest and dividends received are operating cash flows under U.S. GAAP. (3) Cash flows from securities acquired specifically for resale (trading) are operating. Investing: −$150,000 + $90,000 − $40,000 + $10,000 = −$90,000."""),

mcq("far-eps-basic-0001", A1, "Public Company Reporting Topics", AP,
    ["ASC 260-10 (basic earnings per share; stock dividends applied retroactively)"],
    """Crane Corp. had 100,000 common shares outstanding on January 1. It issued 20,000 shares for cash on April 1, distributed a 10% stock dividend on July 1, and bought 6,000 shares as treasury stock on October 1. Net income for the year is $500,000. Crane also has 5% cumulative preferred stock with a par value of $1,000,000; no preferred dividends were declared this year. What is Crane's basic earnings per share, rounded to the nearest cent?""",
    [("$3.52", "Adds the treasury shares' 1,500 weighted shares instead of subtracting them. Reacquired shares are removed from the weighted average from the date bought."),
     ("$3.57", "Uses the 126,000 shares outstanding at year-end instead of the weighted average."),
     ("$3.60", "Correct. ($500,000 − $50,000) ÷ 125,000 weighted-average shares."),
     ("$4.00", "Ignores the cumulative preferred dividends. For cumulative preferred stock, the current year's dividend is deducted whether or not declared.")],
    "C",
    """Income available to common = $500,000 − 5% × $1,000,000 = $450,000 (cumulative dividends are deducted even if not declared). A stock dividend is applied retroactively to all shares outstanding before it: 100,000 × 1.10 × 12/12 = 110,000; 20,000 × 1.10 × 9/12 = 16,500; treasury shares −6,000 × 3/12 = −1,500. Weighted average = 125,000. Basic EPS = $450,000 ÷ 125,000 = $3.60."""),

mcq("far-consolidated-statements-0003", A1, "Consolidated financial statements", AN,
    ["ASC 810-10 (consolidation procedures: intercompany transfers of long-lived assets)"],
    """Pike Corp. owns 100% of Sully Inc. On January 1, Year 2, Sully sold equipment to Pike for $90,000. Sully's carrying amount for the equipment was $60,000, and Pike depreciates it straight-line over its 5-year remaining life with no salvage value. For Year 2, Pike reports net income of $400,000 from its own operations, excluding any income from its investment in Sully, and Sully reports net income of $150,000. Pike's draft Year 2 consolidated income statement reports consolidated net income of $550,000. After any corrections needed, what is consolidated net income?""",
    [("$514,000", "Eliminates the gain but also deducts the $6,000 of excess depreciation. Pike's depreciation on the $90,000 price is $6,000 higher than on Sully's $60,000 carrying amount, so eliminating it increases consolidated income."),
     ("$520,000", "Eliminates the $30,000 intercompany gain but not the $6,000 of excess depreciation on the stepped-up cost."),
     ("$526,000", "Correct. $550,000 − $30,000 intercompany gain + $6,000 excess depreciation."),
     ("$550,000", "Accepts the draft. A gain on a sale between consolidated entities is not realized until the equipment is used up or sold outside the group.")],
    "C",
    """The draft simply adds the two companies' income. In consolidation, Sully's $30,000 gain ($90,000 − $60,000) on the sale to Pike is eliminated, and the equipment is carried at Sully's original basis. Pike's depreciation of $90,000 ÷ 5 = $18,000 exceeds depreciation on the $60,000 basis ($12,000) by $6,000, which is eliminated each year as the gain is realized through use. Consolidated net income = $550,000 − $30,000 + $6,000 = $526,000."""),

mcq("far-nfp-functional-expenses-0001", A1, "Statement of activities (Not-for-Profit)", AP,
    ["ASC 958-720 (reporting expenses by nature and function)", "ASC 958-225 (investment return reported net of external and direct internal investment expenses)", "ASU 2016-14"],
    """Linden Center, a not-for-profit entity, incurred these costs in Year 1: salaries of $600,000, of which staff time records show 70% was spent on programs, 20% on management and general activities, and 10% on fundraising; rent of $120,000, allocated by floor space 75% to programs and 25% to management and general; program supplies of $80,000; and $10,000 of fees paid to an outside investment adviser who manages Linden's endowment. What amount should Linden report as management and general expenses in its analysis of expenses by function?""",
    [("$150,000", "Correct. 20% of salaries ($120,000) + 25% of rent ($30,000). External investment fees are netted against investment return."),
     ("$160,000", "Adds the $10,000 of external investment fees. Since ASU 2016-14, they are netted against investment return rather than reported as an expense."),
     ("$210,000", "Adds the $60,000 of fundraising salaries. Fundraising is a separate supporting function."),
     ("$240,000", "Charges all of the rent to management and general. Rent is allocated by floor space, and 75% supports programs.")],
    "A",
    """Expenses are reported by function using a reasonable allocation basis. Management and general: salaries $600,000 × 20% = $120,000, plus rent $120,000 × 25% = $30,000, for $150,000. Program supplies are program expenses. External investment expenses are netted against investment return, so the $10,000 adviser fee is not a functional expense."""),

mcq("far-balance-sheet-0002", A1, "Balance sheet", AN,
    ["ASC 210-10 (current assets)", "ASC 325-30 (investments in insurance contracts)"],
    """Keel Co.'s draft December 31, Year 1, classified balance sheet reports total current assets of $1,000,000: cash $150,000, trading debt securities $80,000, receivables $300,000, inventory $400,000, prepaid insurance $20,000, and cash surrender value of officers' life insurance $50,000. Supporting documents show that the cash includes $60,000 the board set aside in a fund to retire bonds maturing in Year 5; receivables include a $50,000 loan to an officer due in Year 4; and the prepaid insurance is a two-year policy ($10,000 per year) that began January 1, Year 2, paid in December. After correcting the draft, what are Keel's total current assets?""",
    [("$750,000", "Also removes the $80,000 of trading securities. Securities held for sale in the near term are current assets."),
     ("$820,000", "Removes all of the prepaid insurance. The portion covering the next twelve months is a current asset."),
     ("$830,000", "Correct. $1,000,000 − $60,000 bond fund − $50,000 officer loan − $10,000 second-year insurance − $50,000 cash surrender value."),
     ("$890,000", "Leaves the $60,000 bond retirement fund in cash. Cash set aside to retire long-term debt is not available for current operations.")],
    "C",
    """Current assets are those expected to be realized or consumed within a year (or the operating cycle). Reclassify to noncurrent: the $60,000 fund for bonds due in Year 5, the $50,000 officer loan due in Year 4, the $10,000 of insurance covering Year 3, and the $50,000 cash surrender value, which is a long-term investment. Current assets = $90,000 + $80,000 + $250,000 + $400,000 + $10,000 = $830,000."""),

mcq("far-income-statement-0002", A1, "Income statement", AN,
    ["ASC 225-10 (income statement)", "ASC 360-10 (gains and losses on sales of long-lived assets are included in income from operations)", "ASC 330-10 (inventory write-downs)"],
    """Lund Co.'s draft multi-step income statement reports operating income of $500,000. Reviewing the supporting schedules, you find: (1) sales revenue includes $25,000 of interest earned on notes receivable; (2) a $40,000 loss on the sale of warehouse equipment is reported in other expenses, below operating income; (3) a $30,000 write-down of obsolete inventory is also reported in other expenses; and (4) general and administrative expenses include $15,000 of interest expense on a bank loan. Lund is a manufacturer. After correcting the draft, what is Lund's operating income?""",
    [("$420,000", "Correct. $500,000 − $25,000 interest income − $40,000 loss on sale − $30,000 inventory write-down + $15,000 interest expense."),
     ("$445,000", "Leaves the $25,000 of interest income in sales revenue. For a manufacturer, interest income is nonoperating."),
     ("$450,000", "Leaves the $30,000 inventory write-down below operating income. Write-downs of inventory are part of cost of goods sold."),
     ("$460,000", "Leaves the $40,000 loss below operating income. Gains and losses on sales of long-lived assets are reported within income from operations.")],
    "A",
    """Corrections: interest income (−$25,000) and interest expense (+$15,000) are nonoperating items for a manufacturer, so they move out of operating income. The loss on the sale of equipment (−$40,000) and the inventory write-down (−$30,000) are operating items that the draft placed below operating income. Operating income = $500,000 − $25,000 − $40,000 − $30,000 + $15,000 = $420,000."""),

mcq("far-ratios-0002", A1, "Financial Statement Ratios and Performance Metrics", AP,
    ["Financial statement analysis: inventory turnover and days in inventory"],
    """For Year 2, Mott Co. reports sales of $2,190,000 and cost of goods sold of $1,460,000. Inventory was $180,000 at the beginning of the year and $220,000 at the end. Using a 365-day year and average inventory, what is Mott's number of days' sales in inventory, rounded to one decimal place?""",
    [("33.3", "Computes turnover with sales ($2,190,000 ÷ $200,000). Inventory turnover uses cost of goods sold, because inventory is carried at cost."),
     ("36.7", "Uses sales and ending inventory ($2,190,000 ÷ $220,000). Use cost of goods sold and average inventory."),
     ("45.0", "Uses beginning inventory ($1,460,000 ÷ $180,000). The question calls for average inventory."),
     ("50.0", "Correct. Turnover = $1,460,000 ÷ $200,000 average inventory = 7.3; 365 ÷ 7.3 = 50.0 days.")],
    "D",
    """Inventory turnover = cost of goods sold ÷ average inventory = $1,460,000 ÷ [($180,000 + $220,000) ÷ 2] = 7.3 times. Days in inventory = 365 ÷ 7.3 = 50.0 days."""),

mcq("far-governmental-measurement-focus-0001", A1, "Measurement focus and basis of accounting", RU,
    ["GASB Statement No. 34 (measurement focus and basis of accounting)", "GASB Codification 1600"],
    """A city reports the activities below. Which is reported using the current financial resources measurement focus and the modified accrual basis of accounting?""",
    [("The general fund, in the governmental funds statements", "Correct. Governmental funds use the current financial resources focus and the modified accrual basis."),
     ("The water utility, in the proprietary funds statements", "Enterprise funds use the economic resources focus and the accrual basis."),
     ("The police pension plan, in the fiduciary funds statements", "Fiduciary funds use the economic resources focus and the accrual basis."),
     ("Governmental activities, in the government-wide statements", "Government-wide statements use the economic resources focus and the accrual basis for all activities.")],
    "A",
    """Governmental funds (general, special revenue, capital projects, debt service, permanent) use the current financial resources measurement focus and the modified accrual basis. Proprietary and fiduciary funds, and all government-wide statements, use the economic resources measurement focus and the accrual basis."""),

mcq("far-special-purpose-frameworks-0002", A1, "Special Purpose Frameworks", RU,
    ["AU-C 800 (financial statements prepared in accordance with special purpose frameworks: titles)"],
    """A small business prepares its financial statements on the cash basis of accounting. Which title is appropriate for the statement that reports its revenues and expenses?""",
    [("Statement of income and changes in retained earnings", "Uses titles associated with GAAP statements, which could suggest the statements follow GAAP."),
     ("Statement of revenues collected and expenses paid", "Correct. A title that reflects the cash basis distinguishes the statement from a GAAP income statement."),
     ("Statement of comprehensive income for the year", "A GAAP title; comprehensive income is an accrual-basis concept."),
     ("Income statement", "A GAAP title. Special purpose framework statements use titles that do not imply GAAP presentation.")],
    "B",
    """Financial statements prepared under a special purpose framework should have titles that distinguish them from GAAP statements. For the cash basis, "statement of assets and liabilities arising from cash transactions" replaces the balance sheet and "statement of revenues collected and expenses paid" replaces the income statement."""),

# ── Area II ─────────────────────────────────────────────────────────────
mcq("far-cash-bank-reconciliation-0002", A2, "Cash and cash equivalents", AN,
    ["ASC 305-10 (cash)", "Bank reconciliation practice"],
    """Dunmore Co.'s general ledger cash balance at March 31 is $34,625, and its bank statement shows $35,200. The controller finds: deposits in transit of $4,100; outstanding checks of $6,300; a $45 bank service charge not yet recorded; a customer's $1,200 electronic payment received by the bank and not yet recorded; a $500 check drawn by another company that the bank charged to Dunmore's account in error; and a $2,280 customer deposit that Dunmore recorded twice in its cash receipts journal. After the reconciliation, what adjustment should Dunmore make to its general ledger cash balance?""",
    [("$1,125 decrease", "Correct. −$45 + $1,200 − $2,280 = −$1,125, bringing the ledger to $33,500, which agrees with the adjusted bank balance."),
     ("$1,155 increase", "Records the service charge and the electronic payment but not the duplicate $2,280 deposit, which overstates the ledger."),
     ("$1,625 decrease", "Also deducts the $500 bank error in the ledger. The bank's error is corrected by the bank; Dunmore's books are right for that item."),
     ("$3,525 decrease", "Deducts the $1,200 electronic payment instead of adding it. Cash the bank received for Dunmore increases Dunmore's cash.")],
    "A",
    """Bank side: $35,200 + $4,100 deposits in transit − $6,300 outstanding checks + $500 bank error = $33,500. Book side: $34,625 − $45 service charge + $1,200 electronic payment − $2,280 duplicate deposit = $33,500. Only the book-side items need journal entries: a net decrease of $1,125."""),

mcq("far-inventory-dollar-value-lifo-0001", A2, "Inventory", AP,
    ["ASC 330-10 (inventory: LIFO and dollar-value LIFO)"],
    """Dorset Co. adopted dollar-value LIFO at the end of Year 1, when its inventory was $200,000 and the price index was 1.00. Inventory at current year-end cost was $264,000 at the end of Year 2 (index 1.10) and $286,000 at the end of Year 3 (index 1.30). What is Dorset's dollar-value LIFO inventory at the end of Year 3?""",
    [("$222,000", "Correct. Base-year cost $220,000: the $200,000 base layer plus $20,000 left of the Year 2 layer, priced at 1.10 ($22,000)."),
     ("$226,000", "Prices the remaining Year 2 layer at the Year 3 index (1.30). A layer keeps the index of the year it was added."),
     ("$244,000", "Keeps the whole Year 2 layer. Year 3 base-year cost fell to $220,000, so $20,000 of the $40,000 Year 2 layer was liquidated."),
     ("$286,000", "Reports current cost. Dollar-value LIFO restates inventory to base-year cost and prices each layer at its own index.")],
    "A",
    """Convert to base-year cost: Year 2 $264,000 ÷ 1.10 = $240,000 (a $40,000 layer at 1.10 = $44,000; LIFO inventory $244,000). Year 3 $286,000 ÷ 1.30 = $220,000, a $20,000 decrease that liquidates half of the Year 2 layer. Year 3 LIFO inventory = $200,000 × 1.00 + $20,000 × 1.10 = $222,000."""),

mcq("far-ppe-interest-capitalization-0001", A2, "Property, plant and equipment", AP,
    ["ASC 835-20 (capitalization of interest)"],
    """Garvey Co. constructs a building for its own use during Year 1. It spends $400,000 on January 1, $600,000 on July 1, and $200,000 on December 31, and the building is completed on December 31. Garvey borrowed $500,000 at 8% on January 1 specifically for the project and also has $1,000,000 of other debt outstanding all year at 10%. What amount of interest should Garvey capitalize for Year 1?""",
    [("$40,000", "Capitalizes only the interest on the specific construction loan. Expenditures above the specific borrowing use the rate on other debt."),
     ("$56,000", "Applies the 8% construction-loan rate to all $700,000 of weighted-average expenditures."),
     ("$60,000", "Correct. Weighted-average accumulated expenditures $700,000: $500,000 × 8% + $200,000 × 10%."),
     ("$70,000", "Applies the 10% rate on other debt to all $700,000 of weighted-average expenditures.")],
    "C",
    """Weighted-average accumulated expenditures = $400,000 × 12/12 + $600,000 × 6/12 + $200,000 × 0/12 = $700,000. Avoidable interest: the first $500,000 at the specific borrowing's 8% ($40,000) and the remaining $200,000 at the 10% rate on other borrowings ($20,000), for $60,000. That is less than the $140,000 of actual interest incurred, so $60,000 is capitalized."""),

mcq("far-ppe-held-for-sale-0001", A2, "Property, plant and equipment", AP,
    ["ASC 360-10 (long-lived assets to be disposed of by sale)"],
    """On October 1, Year 1, Harlow Co.'s board approves selling a piece of equipment it no longer needs. Harlow takes it out of service that day and lists it with a dealer at $255,000, in line with recent sales of similar equipment; it expects a buyer within six months and does not expect to change the plan. The equipment cost $500,000; accumulated depreciation was $200,000 at January 1, Year 1, and annual depreciation is $40,000. On October 1, the equipment's fair value is $250,000 and the estimated cost to sell is $15,000. On December 31, Year 1, it is still unsold, its fair value is $260,000, and the estimated cost to sell is still $15,000. At what amount should the equipment be reported at December 31, Year 1?""",
    [("$235,000", "Keeps the October 1 measurement. A later increase in fair value less cost to sell is recognized as a gain, up to the loss previously recognized."),
     ("$245,000", "Correct. Carrying amount at October 1 is $270,000; it is written down to $235,000 and then increased to $245,000 at year-end."),
     ("$260,000", "Uses fair value without deducting the cost to sell."),
     ("$270,000", "Reclassifies the equipment at its carrying amount without comparing it with fair value less cost to sell.")],
    "B",
    """The board's approval, the listing at a price in line with the market, the asset's immediate availability, and the expected sale within six months meet the held-for-sale criteria on October 1. Depreciation runs until then: $200,000 + 9/12 × $40,000 = $230,000 of accumulated depreciation, so the carrying amount on October 1 is $270,000. A held-for-sale asset is measured at the lower of carrying amount and fair value less cost to sell ($235,000), a $35,000 loss, and is no longer depreciated. At year-end, fair value less cost to sell is $245,000; the $10,000 increase is recognized as a gain because it does not exceed the $35,000 loss recognized earlier."""),

mcq("far-receivables-reconciliation-0001", A2, "Trade receivables", AN,
    ["ASC 310-10 (receivables)", "ASC 210-10 (presentation: credit balances in customer accounts)"],
    """At December 31, Arden Co.'s accounts receivable subledger shows customer accounts with debit balances totaling $512,000 and customer accounts with credit balances totaling $14,000 (overpayments and advance deposits), for a net of $498,000. The general ledger accounts receivable control account shows $505,000. Investigating the difference, the controller finds that a $7,000 credit memo for goods returned on December 30 was posted to the customer's subledger account but not to the general ledger. Before any allowance for credit losses, what amount should Arden report as accounts receivable?""",
    [("$491,000", "Posts the $7,000 credit memo twice, subtracting it from the subledger net that already reflects it."),
     ("$498,000", "Reports the subledger net. Customer credit balances are liabilities and are not netted against receivables from other customers."),
     ("$505,000", "Reports the unadjusted general ledger, which does not yet reflect the $7,000 credit memo."),
     ("$512,000", "Correct. After the credit memo is posted, the ledger agrees with the subledger net ($498,000); receivables are the $512,000 of debit balances, and the $14,000 of credit balances is a current liability.")],
    "D",
    """Reconcile first: the general ledger is $7,000 too high because the credit memo was never posted; $505,000 − $7,000 = $498,000 agrees with the subledger net. For presentation, customer accounts with credit balances are reclassified as liabilities rather than netted against other customers' debit balances. Accounts receivable = $512,000; customer credit balances of $14,000 are reported as current liabilities."""),

mcq("far-accrued-liabilities-0001", A2, "Payables and accrued liabilities", AN,
    ["ASC 710-10 (compensated absences)", "ASC 450-20 (self-insurance and incurred but not reported claims)", "ASC 405-10 (liabilities)"],
    """Morrow Co.'s general ledger shows accrued liabilities of $210,000 at December 31: accrued wages $30,000, accrued vacation $40,000, accrued bonus $100,000, and accrued self-insurance claims $40,000. Supporting schedules show: wages earned but unpaid for the last three days of the year were $30,000; employees had earned $48,000 of vested, unused vacation pay; the bonus plan pays 10% of income after deducting the bonus, and income before the bonus was $1,100,000; and for its self-insured health plan, Morrow owes $10,000 on claims reported but unpaid, and its actuary estimates $55,000 of claims incurred but not yet reported. What amount should Morrow report as accrued liabilities?""",
    [("$188,000", "Accrues only the claims already reported. Claims incurred but not yet reported are part of a self-insurer's liability."),
     ("$218,000", "Updates vacation pay but leaves self-insurance at the general ledger's $40,000. The liability is $10,000 reported plus $55,000 incurred but not reported."),
     ("$235,000", "Updates self-insurance but leaves vacation at $40,000. Vested vacation pay earned and unused at year-end is accrued in full ($48,000)."),
     ("$243,000", "Correct. $30,000 wages + $48,000 vacation + $100,000 bonus + $65,000 self-insurance.")],
    "D",
    """Wages: $30,000 (agrees). Vacation: vested, earned rights are accrued at $48,000, $8,000 more than recorded. Bonus: B = 10% × ($1,100,000 − B), so B = $100,000 (agrees). Self-insurance: $10,000 reported and unpaid plus $55,000 incurred but not reported = $65,000, $25,000 more than recorded. Accrued liabilities = $30,000 + $48,000 + $100,000 + $65,000 = $243,000."""),

mcq("far-bonds-premium-0001", A2, "Debt (Notes and bonds payable)", AP,
    ["ASC 835-30 (interest method)", "ASC 470-10 (debt)"],
    """On January 1, Year 1, Wynn Corp. issues $1,000,000 of ten-year, 8% bonds that pay interest each June 30 and December 31, for $1,148,775, a price that yields 6% compounded semiannually. Wynn uses the effective interest method and rounds to the nearest dollar at each step. What is Wynn's interest expense on the bonds for Year 1?""",
    [("$65,123", "Amortizes the premium straight-line ($14,878 a year). The effective interest method is required unless the difference is immaterial."),
     ("$68,760", "Correct. June 30: $1,148,775 × 3% = $34,463; the carrying amount falls to $1,143,238. December 31: $1,143,238 × 3% = $34,297."),
     ("$68,926", "Applies the 6% annual rate to the issue price once. Interest is compounded semiannually, and the carrying amount falls after the first payment."),
     ("$80,000", "Uses the cash interest paid. A premium reduces interest expense below the stated rate.")],
    "B",
    """Effective interest is computed each semiannual period at 3% of the carrying amount. June 30: $1,148,775 × 3% = $34,463 expense; cash $40,000; premium amortized $5,537; carrying amount $1,143,238. December 31: $1,143,238 × 3% = $34,297 expense; premium amortized $5,703. Year 1 interest expense = $34,463 + $34,297 = $68,760."""),

mcq("far-stock-dividends-splits-0001", A2, "Equity", AP,
    ["ASC 505-20 (stock dividends and stock splits)"],
    """At January 1, Tolland Corp. has 200,000 shares of $1 par common stock outstanding. On March 1 it distributes a 5% stock dividend when the market price is $20 per share. On July 1 it effects a 2-for-1 stock split, reducing par value to $0.50 per share. On November 1 it distributes a 50% stock dividend when the market price is $12 per share. By how much do these three transactions reduce retained earnings?""",
    [("$115,000", "Records both stock dividends at par. The 5% dividend is small, so it is recorded at market value."),
     ("$200,000", "Records the 5% dividend at market value but nothing for the 50% dividend, treating it like a split. A large stock dividend is still capitalized, at par."),
     ("$305,000", "Correct. 10,000 shares × $20 = $200,000 for the small dividend, plus 210,000 shares × $0.50 par = $105,000 for the large dividend."),
     ("$2,720,000", "Records the 50% dividend at market value. A distribution of more than 20–25% is accounted for like a split and capitalized at par.")],
    "C",
    """March 1: a 5% dividend is small, so 10,000 shares are capitalized at the $20 market price: $200,000. July 1: a stock split changes the number of shares and the par value but requires no entry to retained earnings; shares become 420,000 at $0.50 par. November 1: a 50% dividend is large, so 210,000 shares are capitalized at par: $105,000. Total reduction = $305,000."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("far-accounting-errors-0002", A3, "Accounting changes and error corrections", AN,
    ["ASC 250-10 (correction of an error: counterbalancing errors)"],
    """In Year 3, before its Year 3 statements are issued, Rook Co. discovers that its inventory at December 31, Year 1, was overstated by $40,000. Inventory at December 31, Year 2, was correct. Ignore income taxes. As originally reported, by how much were Rook's Year 2 net income and its December 31, Year 2, retained earnings misstated?""",
    [("$0 net income; $40,000 overstated retained earnings", "Treats the error as affecting only Year 1 and carrying into retained earnings. The overstated beginning inventory also overstated Year 2 cost of goods sold."),
     ("$40,000 understated net income; $0 retained earnings", "Correct. Year 2 cost of goods sold was overstated, understating Year 2 income by $40,000 and offsetting Year 1's overstatement, so retained earnings at the end of Year 2 was correct."),
     ("$40,000 overstated net income; $40,000 overstated retained earnings", "Reverses the direction for Year 2. An overstated beginning inventory raises cost of goods sold and lowers income."),
     ("$40,000 understated net income; $40,000 understated retained earnings", "Counts the Year 2 understatement in retained earnings without the Year 1 overstatement it offsets.")],
    "B",
    """Overstated ending inventory in Year 1 understated Year 1 cost of goods sold and overstated Year 1 net income by $40,000. That inventory became Year 2's beginning inventory, overstating Year 2 cost of goods sold and understating Year 2 net income by $40,000. The two errors counterbalance, so retained earnings at December 31, Year 2, was correct, and no adjustment to Year 3 opening retained earnings is needed; the Year 2 comparative figures are restated if presented."""),

mcq("far-contingencies-0003", A3, "Contingencies and commitments", AN,
    ["ASC 450-20 (loss contingencies)", "ASC 450-30 (gain contingencies)", "ASC 460-10 (product warranties)", "ASC 410-30 (environmental obligations)"],
    """Knox Co. is preparing its Year 1 statements, which have not been issued. Its files show: (1) Knox is suing a competitor for patent infringement, and counsel expects Knox to be awarded about $500,000; (2) Knox's Year 1 sales of $2,000,000 carry a one-year warranty, past experience shows warranty costs of 3% of sales, and Knox paid $25,000 of claims on these sales in Year 1; (3) the Environmental Protection Agency named Knox a potentially responsible party for a contaminated site, and engineers estimate Knox's share of the cleanup at $300,000 to $700,000, with $450,000 the most likely amount; and (4) no one has asserted a claim over a minor chemical spill at one of Knox's plants, and counsel believes a claim is unlikely to be asserted. By how much do these matters reduce Knox's Year 1 pretax income?""",
    [("$10,000", "Offsets the expected $500,000 award against the losses. A gain contingency is not recognized until it is realized."),
     ("$360,000", "Accrues the $300,000 low end of the environmental range. When one amount in a range is the best estimate, that amount is accrued."),
     ("$485,000", "Uses the $35,000 warranty liability remaining at year-end instead of the $60,000 warranty expense."),
     ("$510,000", "Correct. Warranty expense of $60,000 (3% × $2,000,000) plus the $450,000 best estimate of the environmental obligation.")],
    "D",
    """Review each item. (1) The expected award is a gain contingency: disclosed, not recognized. (2) Warranty expense is recognized in the period of sale: 3% × $2,000,000 = $60,000 (the liability is $35,000 after claims paid). (3) The environmental loss is probable and estimable, and $450,000 is the best estimate within the range, so it is accrued. (4) An unasserted claim that is unlikely to be asserted requires neither accrual nor disclosure. Pretax income falls by $60,000 + $450,000 = $510,000."""),

mcq("far-subsequent-events-0003", A3, "Subsequent events", AN,
    ["ASC 855-10 (subsequent events)", "ASC 260-10 (retroactive adjustment of EPS for stock splits after the balance sheet date)", "ASC 330-10 (net realizable value)"],
    """Pell Co.'s December 31, Year 1, statements will be issued on March 1, Year 2. Before any subsequent-event adjustments, Year 1 net income is $600,000 and weighted-average common shares outstanding are 200,000; Pell has no preferred stock. On January 20, Pell sold inventory carried at $90,000 for $70,000 because the goods had become obsolete during Year 1. On February 1, it effected a 2-for-1 stock split. On February 10, it agreed to acquire a competitor. Ignore income taxes. What basic earnings per share should Pell report for Year 1?""",
    [("$1.45", "Correct. ($600,000 − $20,000 write-down) ÷ 400,000 shares, restated for the split."),
     ("$1.50", "Restates shares for the split but does not recognize the $20,000 write-down, which gives evidence of the inventory's value at year-end."),
     ("$2.90", "Recognizes the write-down but does not restate shares for the split. A split before the statements are issued is reflected retroactively in EPS."),
     ("$3.00", "Makes neither adjustment.")],
    "A",
    """The January sale shows that obsolescence existing at year-end had reduced the inventory's net realizable value to $70,000, so a $20,000 write-down is recognized in Year 1. A stock split after year-end but before issuance is applied retroactively to EPS: 400,000 shares. The February 10 acquisition agreement is disclosed only. Basic EPS = ($600,000 − $20,000) ÷ 400,000 = $1.45."""),

mcq("far-revenue-variable-consideration-0002", A3, "Revenue recognition", AP,
    ["ASC 606-10 (variable consideration: volume discounts; constraint)"],
    """On January 1, Harlan Co. agrees to sell a customer parts at $100 per unit. If the customer buys more than 10,000 units during the calendar year, the price for all units bought that year falls retroactively to $90. From many years of dealing with this customer, Harlan expects it to buy about 12,000 units, and a shortfall below 10,000 has never occurred. In the first quarter, the customer buys 3,000 units. How much revenue should Harlan recognize for the first quarter?""",
    [("$180,000", "Deducts the whole year's expected discount (12,000 × $10 = $120,000) from first-quarter sales at $100. The discount is recognized as the units it applies to are sold."),
     ("$270,000", "Correct. The expected volume discount is included in the transaction price: 3,000 × $90."),
     ("$285,000", "Averages the two prices. With strong experience that the threshold will be met, the $90 price is the best estimate."),
     ("$300,000", "Uses the $100 list price until the threshold is reached. The expected retroactive discount is variable consideration estimated from the start.")],
    "B",
    """The retroactive volume discount makes the consideration variable. Harlan estimates it from its experience with the customer: purchases of about 12,000 units, so the price will be $90. Because it has long experience and a shortfall has never occurred, including the discounted price is not expected to cause a significant revenue reversal. Q1 revenue = 3,000 × $90 = $270,000, with $30,000 recognized as a refund liability."""),

mcq("far-revenue-over-time-0001", A3, "Revenue recognition", AP,
    ["ASC 606-10 (performance obligations satisfied over time; measuring progress with an input method)"],
    """Barlow Builders has a $5,000,000 fixed-price contract to construct a building for a customer on the customer's land, recognizing revenue over time using costs incurred relative to total estimated costs. In Year 1 it incurred $1,200,000 of costs and estimated $2,800,000 more to complete. By the end of Year 2 it had incurred $2,700,000 in total and estimated $900,000 more to complete. What gross profit should Barlow recognize in Year 2?""",
    [("$375,000", "Measures Year 2 progress against the original $4,000,000 cost estimate. Progress uses the updated $3,600,000 total estimate."),
     ("$450,000", "Applies the 45-point increase in percent complete to the original $1,000,000 profit estimate, ignoring the change in estimated profit."),
     ("$750,000", "Correct. Cumulative profit 75% × $1,400,000 = $1,050,000, less the $300,000 recognized in Year 1."),
     ("$1,050,000", "Reports cumulative gross profit to date without subtracting the $300,000 recognized in Year 1.")],
    "C",
    """Year 1: 1,200,000 ÷ 4,000,000 = 30% complete; gross profit 30% × ($5,000,000 − $4,000,000) = $300,000. Year 2: the revised total cost is $3,600,000, so progress is 2,700,000 ÷ 3,600,000 = 75% and estimated profit is $1,400,000. Cumulative gross profit = 75% × $1,400,000 = $1,050,000; Year 2 gross profit = $1,050,000 − $300,000 = $750,000. The change in estimate is handled prospectively through the cumulative catch-up."""),

mcq("far-nfp-contributed-services-0001", A3, "Revenue recognition", AP,
    ["ASC 958-605 (contributed services)"],
    """During Year 1, volunteers gave Aster Museum, a not-for-profit entity, these services: a CPA prepared its financial statements, which Aster would otherwise have paid $12,000 for; carpenters built a permanent exhibit hall addition worth $18,000; volunteer greeters worked at the entrance, time that would cost $25,000 at local wage rates; and board members spent time at meetings valued at $5,000. What amount should Aster recognize as contributed services revenue?""",
    [("$12,000", "Recognizes only the specialized service. Services that create or enhance a nonfinancial asset are also recognized."),
     ("$17,000", "Recognizes the CPA's work and the board members' time. Governance by board members is not a specialized skill Aster would otherwise purchase."),
     ("$18,000", "Recognizes only the exhibit hall work. Specialized services, such as the CPA's, that Aster would otherwise purchase are also recognized."),
     ("$30,000", "Correct. The CPA's specialized service ($12,000) and the carpentry that created a nonfinancial asset ($18,000).")],
    "D",
    """Contributed services are recognized only if they create or enhance nonfinancial assets, or require specialized skills, are provided by people with those skills, and would typically need to be purchased if not donated. The CPA's work ($12,000) and the carpentry on the addition ($18,000) qualify. Greeters and board members do not. Contributed services revenue = $30,000."""),

mcq("far-lessee-finance-0002", A3, "Lessee accounting", AP,
    ["ASC 842-10 (lease payments: residual value guarantees)", "ASC 842-20 (lessee initial measurement)"],
    """On January 1, Year 1, Casey Co. leases a machine for five years. It pays $50,000 at the end of each year and guarantees the lessor that the machine will be worth $40,000 at the end of the lease; Casey expects its value then to be $30,000. The discount rate is 6%, and present value factors at 6% for five periods are 4.2124 for an ordinary annuity and 0.7473 for a single sum. At what amount should Casey initially measure its lease liability?""",
    [("$210,620", "Omits the residual value guarantee. The amount Casey expects to owe under the guarantee is a lease payment."),
     ("$218,093", "Correct. $50,000 × 4.2124 = $210,620, plus the $10,000 expected to be owed under the guarantee × 0.7473 = $7,473."),
     ("$240,512", "Includes the full $40,000 guarantee. Only the amount probable of being owed ($40,000 − $30,000) is a lease payment."),
     ("$260,000", "Adds the undiscounted payments and expected guarantee payment. The liability is the present value of the lease payments.")],
    "B",
    """Lease payments include the amount the lessee expects to owe under a residual value guarantee: $40,000 guaranteed − $30,000 expected value = $10,000. Liability = $50,000 × 4.2124 + $10,000 × 0.7473 = $210,620 + $7,473 = $218,093."""),

mcq("far-fair-value-hierarchy-0001", A3, "Fair value measurements", RU,
    ["ASC 820-10 (fair value hierarchy: Levels 1, 2 and 3)"],
    """Under ASC 820, which of these inputs is a Level 2 input?""",
    [("A quoted price in an active market for an asset identical to the one measured", "A quoted price for an identical asset in an active market is a Level 1 input."),
     ("A broker quote that the entity adjusts using significant assumptions of its own", "Significant unobservable adjustments make the measurement Level 3."),
     ("A quoted price in an active market for an asset similar to the one measured", "Correct. Quoted prices for similar assets in active markets are observable inputs other than Level 1 prices."),
     ("The entity's own projections of cash flows from using the asset", "The entity's own data, not observable in the market, is a Level 3 input.")],
    "C",
    """Level 1 inputs are unadjusted quoted prices in active markets for identical assets. Level 2 inputs are other observable inputs, such as quoted prices for similar assets in active markets, quoted prices in inactive markets, and observable interest rates and yield curves. Level 3 inputs are unobservable, including the entity's own assumptions and significantly adjusted quotes."""),
]

if __name__ == "__main__":
    finalize(ITEMS)
    warnings = audit(ITEMS)
    out = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
    write_items(ITEMS, out)
    from collections import Counter
    c = lambda k: dict(Counter(k(it) for it in ITEMS))
    print("skills", c(lambda i: i["blueprint"]["skill"]))
    print("areas", c(lambda i: i["blueprint"]["area"]))
    print("warnings", warnings)
