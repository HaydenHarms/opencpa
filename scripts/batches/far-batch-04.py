"""FAR batch 04 — 25 items written from scratch for the gaps named by the batch 03 review (see
docs/reviews/far-batch-04.md). Target skill mix 3 / 12 / 10. Scope and skill tags follow the AICPA CPA Exam
Blueprints effective January 2026.

Run: python3 scripts/batches/far-batch-04.py  (writes content/far/*.yaml; leaves other batches' files alone)
Every numeric answer and distractor below was computed in code (Decimal, rounded half up).
"""
import os
from common import mcq as _mcq, finalize, audit, write_items, RU, AP, AN

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 04. Written from scratch; answers solved and every number and distractor computed in code."


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


ITEMS = [
# ── Area I ──────────────────────────────────────────────────────────────
mcq("far-budget-variance-0001", A1, "Financial Statement Ratios and Performance Metrics", AP,
    ["Budget-versus-actual analysis: flexible budget variances"],
    """Norris Co.'s static budget for Year 1 was based on 10,000 units: revenue $500,000, variable costs $300,000, and fixed costs $120,000, for operating income of $80,000. Norris actually sold 11,000 units, with revenue of $561,000, variable costs of $341,000, and fixed costs of $125,000, for operating income of $95,000. What is the flexible-budget variance for operating income?""",
    [("$5,000 unfavorable", "Correct. The flexible budget for 11,000 units is 11,000 × $20 − $120,000 = $100,000; actual operating income of $95,000 is $5,000 lower."),
     ("$5,000 favorable", "Gets the amount right but the direction wrong. Actual operating income is below the flexible budget."),
     ("$15,000 favorable", "Compares actual results with the static budget. That static-budget variance mixes the effect of selling more units with the flexible-budget variance."),
     ("$20,000 favorable", "Computes the sales-volume variance: 1,000 extra units × the $20 budgeted contribution margin.")],
    "A",
    """The flexible budget restates the budget at the actual 11,000 units: revenue $550,000, variable costs $330,000, fixed costs $120,000, operating income $100,000. Flexible-budget variance = actual $95,000 − flexible $100,000 = $5,000 unfavorable (revenue $11,000 F, variable costs $11,000 U, fixed costs $5,000 U). The $15,000 favorable static-budget variance splits into this $5,000 U and a $20,000 F sales-volume variance."""),

mcq("far-performance-metrics-0001", A1, "Financial Statement Ratios and Performance Metrics", AP,
    ["Financial statement analysis: price-to-earnings ratio and dividend payout ratio"],
    """Oates Corp. reports net income of $2,400,000 for the year. It declared $400,000 of dividends on its preferred stock and $600,000 of dividends on its common stock. Weighted-average common shares outstanding were 1,000,000, and the common stock's market price at year-end is $30. Oates computes the dividend payout ratio on earnings available to common shareholders. What are Oates's price-to-earnings ratio and dividend payout ratio?""",
    [("12.5 P/E; 25% payout", "Uses net income without deducting preferred dividends for both ratios. Both are based on earnings available to common shareholders."),
     ("12.5 P/E; 30% payout", "Computes EPS without deducting the $400,000 of preferred dividends ($2.40), which understates the P/E ratio."),
     ("15.0 P/E; 25% payout", "Gets the P/E ratio right but divides common dividends by total net income for the payout ratio."),
     ("15.0 P/E; 30% payout", "Correct. EPS = ($2,400,000 − $400,000) ÷ 1,000,000 = $2.00; P/E = $30 ÷ $2.00 = 15.0; payout = $600,000 ÷ $2,000,000 = 30%.")],
    "D",
    """Earnings available to common = $2,400,000 − $400,000 preferred dividends = $2,000,000; EPS = $2.00. Price-to-earnings ratio = $30 ÷ $2.00 = 15.0. Dividend payout ratio = common dividends ÷ earnings available to common = $600,000 ÷ $2,000,000 = 30%."""),

mcq("far-nfp-financial-position-0001", A1, "Statement of financial position (Not-for-Profit)", AP,
    ["ASC 958-210 (not-for-profit statement of financial position)", "ASC 958-205 (net assets with and without donor restrictions)", "ASC 958-605 (implied time restrictions on promises to give)"],
    """At year-end, Oak Hollow Society, a not-for-profit entity, has: unconditional promises to give of $80,000, due next year, for which donors specified no purpose; an endowment gift of $500,000 that donors require to be held in perpetuity; $60,000 of accumulated earnings on that endowment that the board has not yet appropriated for spending; $200,000 that the board itself has set aside as a quasi-endowment; $45,000 of unspent gifts that donors restricted to scholarships; and $900,000 of property and equipment bought with unrestricted funds. What total should Oak Hollow report as net assets with donor restrictions?""",
    [("$605,000", "Omits the $80,000 of promises to give. Amounts receivable in a later period carry an implied time restriction until they are due."),
     ("$625,000", "Omits the $60,000 of unappropriated endowment earnings. Earnings on a donor-restricted endowment stay restricted until appropriated for spending."),
     ("$685,000", "Correct. $80,000 + $500,000 + $60,000 + $45,000."),
     ("$885,000", "Includes the $200,000 quasi-endowment. Board designations are net assets without donor restrictions; only donors can impose restrictions.")],
    "C",
    """Net assets with donor restrictions: promises to give due in a future period (implied time restriction) $80,000; the perpetual endowment $500,000; unappropriated earnings on the donor-restricted endowment $60,000; and the unspent scholarship gifts $45,000. Total $685,000. The board-designated quasi-endowment and the property bought with unrestricted funds are without donor restrictions."""),

mcq("far-cash-flows-0006", A1, "Statement of cash flows", AN,
    ["ASC 230-10 (classification of cash receipts and payments)"],
    """Ives Co.'s controller is deriving how six Year 1 transactions affect net cash provided by operating activities: (1) collected $50,000 of accounts receivable from customers; (2) paid $30,000 in December for insurance covering the next year; (3) sold equipment with a carrying amount of $40,000 for $55,000 in cash; (4) paid $20,000 of interest on a bank loan; (5) accrued $12,000 of wages that will be paid in January; and (6) received $15,000 of dividends on an equity investment. Under U.S. GAAP, by how much do these transactions increase net cash provided by operating activities?""",
    [("$15,000", "Correct. +$50,000 − $30,000 − $20,000 + $15,000. The equipment sale is investing, and the accrued wages involve no cash."),
     ("$35,000", "Leaves out the $20,000 of interest paid. Under U.S. GAAP, interest paid is an operating cash outflow."),
     ("$3,000", "Deducts the $12,000 of accrued wages. An accrual records an expense without any cash payment."),
     ("$70,000", "Adds the $55,000 of equipment sale proceeds. Proceeds from selling equipment are an investing inflow.")],
    "A",
    """Operating cash flows: collections from customers +$50,000; insurance paid in advance −$30,000; interest paid −$20,000 (operating under U.S. GAAP); dividends received +$15,000 (operating under U.S. GAAP). Net +$15,000. The $55,000 of equipment proceeds is an investing inflow (the $15,000 gain is removed under the indirect method), and the wage accrual has no cash effect."""),

mcq("far-notes-0002", A1, "Notes to financial statements", AN,
    ["ASC 606-10 (performance obligations satisfied over time; contract liabilities)", "ASC 330-10 (inventory: LIFO)", "ASC 470-10 (debt maturities)", "ASC 360-10 (property, plant and equipment)"],
    """Linwood Co.'s fiscal year ends June 30. Its draft June 30, Year 2, balance sheet reports property and equipment, net, of $1,800,000; inventories of $640,000; long-term debt of $1,500,000, of which $100,000 is current; and no contract liabilities. You compare four draft note excerpts with the statements. Property note: cost $3,000,000, less accumulated depreciation of $1,200,000. Inventory note: inventories are stated at LIFO cost; they would be $90,000 higher under FIFO. Debt note: maturities are $100,000 in fiscal Year 3, $200,000 in each of fiscal Years 4 and 5, and $1,000,000 thereafter. Revenue note: revenue from one-year customer support contracts, which Linwood bills and collects every January 1, is recognized when billed; contracts billed on January 1, Year 2, totaled $240,000. Which note reveals that the draft financial statements must be corrected?""",
    [("The property note", "Consistent. Cost less accumulated depreciation equals the $1,800,000 on the balance sheet."),
     ("The inventory note", "Consistent. Disclosing the FIFO difference (the LIFO reserve) is expected; it does not change the LIFO carrying amount."),
     ("The debt note", "Consistent. The maturities total $1,500,000, and the $100,000 due in fiscal Year 3 matches the current portion."),
     ("The revenue note", "Correct. Support is a service provided over the year, so half of the $240,000 billed on January 1 is unearned at June 30: a $120,000 contract liability is missing.")],
    "D",
    """Support contracts are performance obligations satisfied over time, so revenue is recognized as the year of support passes, not when billed. On June 30, Year 2, six months of the contracts billed January 1 remain: $240,000 × 6/12 = $120,000 should be a contract liability, and revenue is overstated by the same amount. The revenue note describes a policy that does not comply with ASC 606 and reveals the misstatement. The other three notes agree with the statements."""),

mcq("far-consolidated-statements-0004", A1, "Consolidated financial statements", AN,
    ["ASC 810-10 (noncontrolling interests; intercompany profit elimination)"],
    """Pace Corp. owns 80% of Sorel Inc. and measured the noncontrolling interest at fair value at acquisition. For Year 2, Sorel reports net income of $200,000. Consolidation adjustments for Year 2 include $15,000 of amortization of the excess of fair value over book value of Sorel's equipment at the acquisition date. During Year 2 Sorel also sold goods to Pace for $100,000 that had cost Sorel $60,000, and Pace still holds 25% of them at year-end. Pace's draft consolidated income statement reports net income attributable to the noncontrolling interest of $40,000. After any corrections needed, what should that amount be?""",
    [("$35,000", "Correct. 20% × ($200,000 − $15,000 amortization − $10,000 unrealized profit on Sorel's sale)."),
     ("$37,000", "Adjusts Sorel's income for the amortization but not for the unrealized profit. Profit on an upstream sale is earned by the subsidiary, so its elimination is shared with the noncontrolling interest."),
     ("$38,000", "Adjusts for the unrealized profit but not the $15,000 amortization of Sorel's fair value step-up."),
     ("$40,000", "Accepts the draft, which applies 20% to Sorel's reported income without either consolidation adjustment.")],
    "A",
    """The noncontrolling interest shares in the subsidiary's income as adjusted in consolidation. Sorel's reported income of $200,000 is reduced by the $15,000 amortization of its acquisition-date fair value adjustments and by the unrealized profit on its upstream sale still in Pace's inventory: 25% × ($100,000 − $60,000) = $10,000. Adjusted income = $175,000; noncontrolling interest = 20% × $175,000 = $35,000."""),

mcq("far-sec-forms-0002", A1, "Public Company Reporting Topics", RU,
    ["SEC Form 8-K (Item 5.02: departure of principal officers)", "Securities Exchange Act of 1934"],
    """The chief executive officer of a U.S. registrant resigns unexpectedly in the middle of a quarter. Which filing must the registrant make, and within what period?""",
    [("Form 8-K, generally within four business days", "Correct. The departure of a principal officer is a Form 8-K event, reported within four business days."),
     ("Form 10-Q, within 40 or 45 days after quarter-end", "The 10-Q is the quarterly report; a principal officer's departure requires a current report."),
     ("Form 8-K, within 15 calendar days", "The 15-day window applied before the SEC's 2004 amendments; most 8-K items are now due in four business days."),
     ("Form 10-K, within 60 to 90 days after year-end", "The 10-K is the annual report; current events are reported on Form 8-K.")],
    "A",
    """Form 8-K is the current report for significant events between periodic reports. The departure of a principal executive officer (Item 5.02) must generally be reported within four business days. Forms 10-Q and 10-K are the quarterly and annual periodic reports."""),

mcq("far-income-statement-0003", A1, "Income statement", AN,
    ["ASC 205-20 (discontinued operations: presentation)", "ASC 360-10 (long-lived assets held for sale)"],
    """Quinn Co.'s draft Year 1 income statement reports a loss from discontinued operations, net of tax, of $112,500. The discontinued component is a division that met the held-for-sale criteria in November. Supporting schedules show that the division had a pretax operating loss of $150,000 for Year 1, and that when it was classified as held for sale its carrying amount of $800,000 exceeded its fair value less cost to sell of $740,000, a loss that is not in the draft. Quinn's tax rate is 25%. After any corrections needed, what is Quinn's loss from discontinued operations, net of tax?""",
    [("$112,500", "Accepts the draft, which omits the $60,000 write-down to fair value less cost to sell."),
     ("$210,000", "Reports the whole loss before tax. Discontinued operations are presented net of tax."),
     ("$157,500", "Correct. ($150,000 operating loss + $60,000 write-down) × (1 − 25%)."),
     ("$172,500", "Adds the $60,000 write-down without its tax effect. The write-down is part of the discontinued component's pretax loss.")],
    "C",
    """The loss from discontinued operations includes the component's operating results for the period and any loss on measuring it at fair value less cost to sell: $150,000 + ($800,000 − $740,000) = $210,000 before tax. Net of the 25% tax benefit, the loss is $157,500."""),

mcq("far-balance-sheet-0003", A1, "Balance sheet", AN,
    ["ASC 505-30 (treasury stock)", "ASC 810-10 (noncontrolling interest presented in equity)"],
    """Reyes Corp.'s draft consolidated balance sheet reports total stockholders' equity of $1,100,000: common stock $100,000, additional paid-in capital $400,000, and retained earnings $600,000. Supporting documents show that $50,000 of Reyes's own shares, reacquired and held in treasury, are reported among noncurrent assets as "investment in treasury stock," and that the $80,000 noncontrolling interest in a subsidiary is reported as a noncurrent liability. After correcting the draft, what is Reyes's total equity?""",
    [("$1,050,000", "Corrects the treasury stock but leaves the noncontrolling interest in liabilities. Noncontrolling interest is part of equity in consolidated statements."),
     ("$1,100,000", "Accepts the draft. Treasury stock is a deduction from equity, not an asset, and noncontrolling interest is equity, not a liability."),
     ("$1,130,000", "Correct. $1,100,000 − $50,000 treasury stock + $80,000 noncontrolling interest."),
     ("$1,180,000", "Moves the noncontrolling interest into equity but leaves the treasury stock as an asset.")],
    "C",
    """Treasury stock is a contra-equity account, so the $50,000 comes out of assets and reduces equity. Noncontrolling interest is reported within equity, separately from the parent's equity, so the $80,000 moves from liabilities to equity. Total equity = $1,100,000 − $50,000 + $80,000 = $1,130,000 (the parent's share is $1,050,000)."""),

# ── Area II ─────────────────────────────────────────────────────────────
mcq("far-receivables-rollforward-0001", A2, "Trade receivables", AN,
    ["ASC 310-10 (receivables)", "ASC 326-20 (write-offs and recoveries)"],
    """Selby Co. is preparing a rollforward of its trade receivables to test reported credit sales. Receivables were $200,000 at the start of the year and $260,000 at the end, per the aged subledger. Cash receipts from customers, per the cash receipts journal, were $1,180,000, which includes $5,000 collected on an account written off in an earlier year. Write-offs during the year were $18,000. All sales are on credit. What should credit sales for the year be?""",
    [("$1,217,000", "Adds the write-offs instead of subtracting them. Write-offs reduce receivables, so more sales are needed to reach the ending balance."),
     ("$1,235,000", "Leaves out the $18,000 of write-offs."),
     ("$1,253,000", "Correct. $260,000 + $1,180,000 + $18,000 − $200,000 − $5,000 reinstated recovery."),
     ("$1,258,000", "Treats the $5,000 recovery as a collection of current sales. A recovery is first reinstated in receivables and then collected, so it is not a sale.")],
    "C",
    """Rollforward: beginning $200,000 + credit sales + $5,000 recovery reinstated − $1,180,000 collections − $18,000 write-offs = ending $260,000. Credit sales = $260,000 + $1,180,000 + $18,000 − $200,000 − $5,000 = $1,253,000."""),

mcq("far-inventory-rollforward-0001", A2, "Inventory", AN,
    ["ASC 330-10 (inventory)"],
    """Tobin Co. uses a perpetual inventory system. Its inventory rollforward for Year 1 shows beginning inventory of $120,000, purchases of $900,000 per the accounts payable subledger, purchase returns of $20,000, freight-in of $15,000, and cost of goods sold of $870,000 per the general ledger. A year-end physical count, priced at cost, totals $125,000. What inventory shrinkage should Tobin record?""",
    [("$5,000", "Leaves the $15,000 of freight-in out of the rollforward. Freight-in is part of inventory cost."),
     ("$20,000", "Correct. Book inventory $120,000 + $900,000 − $20,000 + $15,000 − $870,000 = $145,000, less the $125,000 count."),
     ("$40,000", "Leaves the $20,000 of purchase returns out of the rollforward. Returned goods leave inventory."),
     ("$60,000", "Adds the purchase returns instead of subtracting them.")],
    "B",
    """Book (perpetual) inventory = beginning $120,000 + purchases $900,000 − returns $20,000 + freight-in $15,000 − cost of goods sold $870,000 = $145,000. The count shows $125,000, so $20,000 of inventory is missing and is recorded as shrinkage (usually in cost of goods sold)."""),

mcq("far-ppe-rollforward-0001", A2, "Property, plant and equipment", AN,
    ["ASC 360-10 (property, plant and equipment; gains and losses on disposal)"],
    """Ulm Co.'s equipment rollforward shows gross equipment of $1,200,000 at the start of the year and $1,350,000 at the end, with $300,000 of purchases per the capital expenditures report. Accumulated depreciation was $400,000 at the start and $430,000 at the end, and depreciation expense was $110,000. The only disposal was one item sold for $50,000 in cash. What gain or loss should Ulm report on the sale?""",
    [("$70,000 loss", "Uses the $30,000 net change in accumulated depreciation as the amount removed. The amount removed is what the rollforward leaves unexplained: $400,000 + $110,000 − $430,000 = $80,000."),
     ("$20,000 loss", "Correct. Cost removed $150,000 less accumulated depreciation removed $80,000 = carrying amount $70,000; proceeds $50,000."),
     ("$50,000 gain", "Treats the whole $50,000 of proceeds as gain, ignoring the equipment's carrying amount."),
     ("$100,000 loss", "Compares the proceeds with the equipment's cost without removing its accumulated depreciation.")],
    "B",
    """Derive the disposal from the rollforward. Cost removed = $1,200,000 + $300,000 − $1,350,000 = $150,000. Accumulated depreciation removed = $400,000 + $110,000 − $430,000 = $80,000. Carrying amount = $70,000; proceeds $50,000; loss = $20,000."""),

mcq("far-exit-costs-0001", A2, "Payables and accrued liabilities", AP,
    ["ASC 420-10 (exit or disposal cost obligations: one-time employee termination benefits)"],
    """On December 1, Year 1, Vail Co. commits to closing a plant on March 31, Year 2, and communicates the plan to the plant's 50 employees that day. Each employee who stays until the plant closes will receive a $6,000 termination payment; employees who leave earlier receive nothing. Under Vail's plan and local law, employees must be given at least 60 days' notice before termination. Vail expects all 50 to stay. Vail recognizes such costs ratably by month. What termination benefit expense should Vail recognize in Year 1?""",
    [("$0", "Waits until the plant closes. When employees must work to a future date to earn the benefit, the cost is recognized over that service period, starting when the plan is communicated."),
     ("$75,000", "Correct. The $300,000 benefit is recognized ratably from December 1 to March 31 (4 months); one month falls in Year 1."),
     ("$150,000", "Spreads the benefit over the 60-day minimum notice period. Because employees must stay beyond that period to earn it, it is spread over the full period to March 31."),
     ("$300,000", "Recognizes the whole benefit when the plan is communicated. That applies only when employees are not required to render service beyond the minimum retention period.")],
    "B",
    """One-time termination benefits are recognized when the plan is communicated if employees need not work beyond the minimum retention period. Here they must stay until March 31, beyond the 60-day minimum, so the $300,000 (50 × $6,000) is recognized ratably over the four months from December 1 to March 31: $75,000 in Year 1."""),

mcq("far-asset-retirement-obligations-0001", A2, "Payables and accrued liabilities", RU,
    ["ASC 410-20 (asset retirement obligations)"],
    """Under ASC 410-20, how is an asset retirement obligation initially measured, and how is the later increase in the liability for the passage of time reported?""",
    [("Fair value, discounting at a credit-adjusted risk-free rate; accretion is an operating expense", "Correct. The liability is initially measured at fair value and accreted over time; accretion is classified as an operating expense, not interest."),
     ("Undiscounted estimated retirement costs; no accretion is recorded in later periods", "The obligation is measured at fair value, typically a present value, and accreted each period."),
     ("Present value at the incremental borrowing rate; accretion is reported as interest expense", "The discount rate is a credit-adjusted risk-free rate, and accretion is not interest cost."),
     ("Fair value, discounting at a credit-adjusted risk-free rate; accretion is interest expense", "The measurement is right, but accretion expense is an operating item; ASC 410-20 says it is not interest cost.")],
    "A",
    """An asset retirement obligation is recognized at fair value when incurred, usually measured as the present value of expected cash flows discounted at a credit-adjusted risk-free rate, and the same amount is added to the asset's carrying amount. The liability is then accreted each period; accretion expense is classified as an operating item, not as interest cost."""),

mcq("far-debt-modification-0001", A2, "Debt (Notes and bonds payable)", AP,
    ["ASC 470-50 (modification or exchange of debt: 10% cash flow test)"],
    """Wade Co. owes a bank $1,000,000 on a note with 5 years remaining and 8% interest paid annually; the note's carrying amount is $1,000,000. The bank agrees to cut the rate to 5%, with the principal and maturity unchanged, and Wade pays the bank a $20,000 fee to modify the note. Wade is not experiencing financial difficulty. At 8%, the present value factors for 5 periods are 3.9927 for an ordinary annuity and 0.6806 for a single sum. By what percentage do the present value of the new cash flows and the present value of the old cash flows differ, and how is the change accounted for?""",
    [("3.00% change; modification", "Compares the interest rates (8% − 5%) instead of the present values of the cash flows."),
     ("13.98% change; extinguishment", "Subtracts the $20,000 fee from the new cash flows. A fee the borrower pays the lender adds to the new debt's cash flows."),
     ("9.98% change; modification", "Correct. New cash flows: $50,000 × 3.9927 + $1,000,000 × 0.6806 + $20,000 fee = $900,235, 9.98% below $1,000,000."),
     ("11.98% change; extinguishment", "Leaves out the $20,000 fee paid to the lender, which is part of the new debt's cash flows in the 10% test.")],
    "C",
    """A change in debt terms is an extinguishment if the present value of the new cash flows, including fees paid to the creditor and discounted at the original effective rate, differs by at least 10% from the present value of the remaining original cash flows. New: $50,000 × 3.9927 = $199,635 + $1,000,000 × 0.6806 = $680,600 + $20,000 fee = $900,235. Old: $1,000,000. Difference 9.98% < 10%, so it is a modification: the fee is amortized as an adjustment of interest over the remaining term."""),

mcq("far-ppe-impairment-0002", A2, "Property, plant and equipment", AP,
    ["ASC 360-10 (impairment of an asset group: allocation of the loss)"],
    """Yates Co. tests an asset group for impairment. The group consists of Machine A (carrying amount $300,000), Machine B ($200,000) and a building ($500,000). The group's undiscounted future cash flows are $900,000 and its fair value is $800,000. The building's own fair value is $460,000; the machines' individual fair values cannot be determined without undue cost. How much of the impairment loss should Yates allocate to Machine A?""",
    [("$36,000", "Allocates to Machine A only its share of the $60,000 that could not be charged to the building."),
     ("$60,000", "Allocates the $200,000 loss pro rata to all three assets without limiting the building to its $40,000 excess over fair value."),
     ("$120,000", "Allocates the whole $200,000 loss to the two machines (60% to Machine A). The building takes its share, limited to its $40,000 excess over fair value."),
     ("$96,000", "Correct. Pro rata $60,000, plus 60% of the $60,000 the building cannot absorb (its loss is capped at $40,000).")],
    "D",
    """The group is not recoverable ($900,000 < $1,000,000), so the loss is $1,000,000 − $800,000 = $200,000, allocated pro rata by carrying amount but not reducing any asset below its determinable fair value. Pro rata: A $60,000, B $40,000, building $100,000. The building can absorb only $500,000 − $460,000 = $40,000, so the other $60,000 is reallocated to the machines in a 3:2 ratio: A $36,000, B $24,000. Machine A's total = $96,000."""),

mcq("far-intangibles-impairment-0001", A2, "Intangible assets", AP,
    ["ASC 350-30 (finite-lived intangibles tested under ASC 360-10)", "ASC 360-10 (recoverability test and measurement)"],
    """Zane Co. bought a customer list for $400,000 three years ago and amortizes it straight-line over 8 years with no residual value. After losing a major customer, Zane estimates the list's remaining undiscounted cash flows at $230,000 and its fair value at $180,000. What impairment loss should Zane recognize?""",
    [("$20,000", "Measures the loss as carrying amount minus undiscounted cash flows. Undiscounted cash flows only test recoverability; the loss is measured against fair value."),
     ("$50,000", "Measures the loss as undiscounted cash flows minus fair value. The loss is carrying amount minus fair value."),
     ("$70,000", "Correct. Carrying amount $400,000 − 3 × $50,000 = $250,000, less fair value $180,000."),
     ("$220,000", "Compares fair value with the original $400,000 cost, ignoring three years of amortization.")],
    "C",
    """A finite-lived intangible is tested for recoverability like other long-lived assets. Carrying amount = $400,000 − 3 × ($400,000 ÷ 8) = $250,000. Undiscounted cash flows of $230,000 are less than the carrying amount, so the asset is impaired. Loss = $250,000 − $180,000 fair value = $70,000."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("far-valuation-allowance-0001", A3, "Accounting for income taxes", RU,
    ["ASC 740-10 (valuation allowance: positive and negative evidence)"],
    """In deciding whether a deferred tax asset needs a valuation allowance, which of the following is significant negative evidence that is difficult to overcome?""",
    [("A firm sales backlog that will produce taxable income", "Positive evidence: expected future taxable income supports realizing the asset."),
     ("Cumulative pretax losses in the three most recent years", "Correct. Cumulative losses in recent years are significant negative evidence that is difficult to overcome."),
     ("Appreciated assets whose sale would produce taxable income", "Positive evidence: a tax-planning source of future taxable income."),
     ("Taxable temporary differences reversing in the carryforward period", "Positive evidence: a source of taxable income against which the deductible amounts can be used.")],
    "B",
    """A valuation allowance is needed if it is more likely than not that some or all of a deferred tax asset will not be realized. Cumulative losses in recent years are significant negative evidence that is difficult to overcome. A sales backlog, appreciated assets, and reversing taxable temporary differences are sources of taxable income that support realization."""),

mcq("far-income-taxes-nol-0001", A3, "Accounting for income taxes", AP,
    ["ASC 740-10 (deferred tax assets for net operating loss carryforwards)", "IRC §172 (net operating loss carryforward; 80% limitation)"],
    """In Year 1, Abbot Corp. has a pretax book loss and a taxable loss of $400,000, with no temporary or permanent differences. Under current federal law the loss can be carried forward indefinitely but not back, and in any future year it can offset only 80% of that year's taxable income. Abbot expects enough future taxable income to use the whole loss and needs no valuation allowance. The enacted tax rate is 21%. What income tax benefit should Abbot report in Year 1?""",
    [("$0", "Recognizes no benefit because the loss cannot be carried back. A carryforward creates a deferred tax asset when realization is more likely than not."),
     ("$67,200", "Applies the 80% limitation to the deferred tax asset. The limit affects how fast the loss is used, not how much of it is used, when future income is sufficient."),
     ("$84,000", "Correct. Deferred tax asset $400,000 × 21% = $84,000, with a matching deferred tax benefit."),
     ("$16,800", "Recognizes a benefit only for the 20% of each future year's income the loss cannot offset. The limit slows the loss's use; the whole loss is still used.")],
    "C",
    """The net operating loss carryforward gives rise to a deferred tax asset of $400,000 × 21% = $84,000. Because Abbot expects to use the entire carryforward, no valuation allowance is needed, and the $84,000 is a deferred income tax benefit that offsets the pretax loss. The 80% limitation affects the timing of use, not the total, when future taxable income is sufficient."""),

mcq("far-fair-value-techniques-0001", A3, "Fair value measurements", AP,
    ["ASC 820-10 (income approach; market participant assumptions)"],
    """Barr Co. must measure the fair value of a patent using an income approach. Market participants would expect the patent to generate cash flows of $100,000 at the end of each of the next five years and would discount them at 10%. Barr itself expects $120,000 a year because of synergies with its other products, and its own cost of capital is 12%. Present value factors for a five-year ordinary annuity are 3.7908 at 10% and 3.6048 at 12%; the four-year factor at 10% is 3.1699. What is the patent's fair value?""",
    [("$416,990", "Treats the cash flows as received at the start of each year ($100,000 + $100,000 × 3.1699). They arrive at the end of each year."),
     ("$360,480", "Discounts market participants' cash flows at Barr's own 12% cost of capital. Fair value uses market participants' discount rate."),
     ("$379,080", "Correct. $100,000 × 3.7908, using market participants' cash flows and discount rate."),
     ("$454,896", "Uses Barr's own expected cash flows, including entity-specific synergies. Fair value reflects market participant assumptions.")],
    "C",
    """Fair value is a market-based measurement: it uses the assumptions market participants would use, not entity-specific synergies or the entity's own cost of capital. Fair value = $100,000 × 3.7908 = $379,080."""),

mcq("far-lessee-classification-0001", A3, "Lessee accounting", AP,
    ["ASC 842-10 (lease classification criteria; ASC 842-10-55-2 thresholds)"],
    """Cole Co. is the lessee in three new leases, none of which transfers ownership, includes a purchase option Cole is reasonably certain to exercise, or includes a residual value guarantee. Cole uses 75% of economic life as a "major part" and 90% of fair value as "substantially all." Lease 1: a 7-year lease of equipment with a 9-year economic life. Lease 2: a 3-year lease of a truck with an 8-year economic life whose lease payments have a present value equal to 60% of its fair value. Lease 3: a 2-year lease of a machine built to Cole's specifications that the lessor could not use for anyone else without major modification. Which leases are finance leases?""",
    [("Lease 1 only", "Misses Lease 3. An asset so specialized that it has no alternative use to the lessor makes the lease a finance lease."),
     ("Leases 1 and 3", "Correct. Lease 1 covers 78% of the economic life, and Lease 3's asset has no alternative use to the lessor."),
     ("Lease 3 only", "Misses Lease 1. A term of 7 of 9 years (78%) is a major part of the economic life."),
     ("Leases 1, 2 and 3", "Includes Lease 2, which meets none of the criteria: its term is short and its payments are 60% of fair value.")],
    "B",
    """A lease is a finance lease if it meets any of five criteria: transfer of ownership, a purchase option reasonably certain to be exercised, a term that is a major part of the remaining economic life, payments (plus any residual guarantee) that are substantially all of fair value, or an asset so specialized it has no alternative use to the lessor. Lease 1: 7 ÷ 9 = 78% ≥ 75%, finance. Lease 2: meets none, operating. Lease 3: specialized asset, finance."""),

mcq("far-nfp-agent-transfers-0001", A3, "Revenue recognition", AP,
    ["ASC 958-605 (transfers received as an agent, trustee or intermediary; variance power)"],
    """During the year, Unity Fund, a not-for-profit federated fundraising organization, receives: $50,000 from donors who specify that it go to Riverside Shelter, an unrelated charity, with no power for Unity to redirect it; $30,000 for Unity's general use; $20,000 from a donor who names a beneficiary but explicitly gives Unity the unilateral power to redirect the gift to another beneficiary; and $10,000 transferred by Riverside Shelter itself for Unity to invest and hold for Riverside's future use. What contribution revenue should Unity recognize?""",
    [("$50,000", "Correct. The $30,000 for general use and the $20,000 over which Unity has variance power."),
     ("$60,000", "Also counts Riverside Shelter's $10,000. A transfer the beneficiary makes for its own benefit is not a contribution to Unity."),
     ("$100,000", "Also counts the $50,000 designated for Riverside without variance power. Unity acts as an agent for it and records a liability."),
     ("$110,000", "Counts every receipt as a contribution.")],
    "A",
    """A recipient that receives assets for a specified beneficiary without variance power acts as an agent: it records a liability, not revenue ($50,000). Explicit variance power makes the gift Unity's contribution ($20,000). The $30,000 for general use is a contribution. Riverside's own $10,000 is held for its benefit and is not a contribution to Unity. Contribution revenue = $50,000."""),

mcq("far-accounting-errors-0003", A3, "Accounting changes and error corrections", AN,
    ["ASC 250-10 (correction of an error in previously issued statements)"],
    """In Year 1, Toft Co. capitalized $60,000 of routine repair costs as equipment and recorded $12,000 of depreciation on it (5-year life). Before closing its Year 2 books, Toft discovers the error; it has already recorded another $12,000 of Year 2 depreciation on the capitalized amount. Toft's tax rate is 25% for all effects, and it presents single-year statements. What are the effects of correcting the error?""",
    [("$36,000 decrease to January 1, Year 2, retained earnings; $0 change to Year 2 net income", "Gets the prior-period adjustment right but leaves the $12,000 of Year 2 depreciation on the repairs in Year 2 expense."),
     ("$36,000 decrease to January 1, Year 2, retained earnings; $9,000 increase to Year 2 net income", "Correct. Year 1 was overstated by ($60,000 − $12,000) × 75%; reversing Year 2's $12,000 of depreciation raises Year 2 income by $9,000."),
     ("$45,000 decrease to January 1, Year 2, retained earnings; $0 change to Year 2 net income", "Ignores the Year 1 depreciation already recorded; the prior-period effect is net of it."),
     ("$48,000 decrease to January 1, Year 2, retained earnings; $12,000 increase to Year 2 net income", "Leaves out the 25% tax effect on both amounts.")],
    "B",
    """The repairs should have been expensed in Year 1. Year 1 income was overstated by $60,000 − $12,000 = $48,000 before tax, $36,000 after tax, so January 1, Year 2, retained earnings is reduced by $36,000 as a prior-period adjustment. The $12,000 of Year 2 depreciation on the capitalized repairs is reversed, raising Year 2 pretax income by $12,000 and net income by $9,000."""),

mcq("far-contingencies-0004", A3, "Contingencies and commitments", AN,
    ["ASC 460-10 (guarantees: recognition at inception)", "ASC 330-10 (losses on firm purchase commitments)", "ASC 450-20 (loss contingencies)"],
    """Dunn Co. is preparing its year-end statements, which have not been issued. Its files show: (1) on December 31, for a fee, Dunn guaranteed a $500,000 bank loan of an unrelated supplier; the guarantee's fair value at inception was $15,000, and default is considered remote, so expected credit losses on the guarantee are immaterial; (2) Dunn has a noncancelable, unhedged commitment to buy materials next year for $200,000, and their market price has fallen to $170,000; (3) counsel considers an unfavorable outcome in a $400,000 lawsuit against Dunn reasonably possible but not probable; and (4) Dunn does not insure its warehouses against fire, and none has occurred. What total liabilities should Dunn recognize for these matters?""",
    [("$0", "Treats every matter as a disclosure. A guarantee is recognized at fair value at inception even when default is remote, and a loss on a firm purchase commitment is accrued."),
     ("$15,000", "Recognizes the guarantee but not the $30,000 loss on the purchase commitment."),
     ("$30,000", "Recognizes the purchase commitment loss but not the guarantee. A guarantee creates a noncontingent obligation to stand ready, recognized at fair value."),
     ("$45,000", "Correct. The $15,000 guarantee obligation plus the $30,000 loss on the purchase commitment.")],
    "D",
    """(1) A guarantor recognizes a liability for the fair value of the obligation it undertakes at inception ($15,000), even if payment is remote. (2) A loss on a noncancelable purchase commitment is recognized when the market price falls below the contract price: $30,000. (3) A reasonably possible loss is disclosed, not accrued. (4) The risk of future uninsured losses is not a liability until an event occurs. Total = $45,000."""),

mcq("far-revenue-licenses-0001", A3, "Revenue recognition", AP,
    ["ASC 606-10 (licenses of intellectual property: right to use versus right to access)"],
    """On December 1, Year 1, Egan Co. sells a customer a perpetual license to its existing accounting software for $300,000, together with two years of technical support for $60,000; the prices equal standalone selling prices, and Egan does not expect updates to change the software's functionality. Also on December 1, Egan grants a franchisee a five-year license to use its restaurant brand, which Egan will continue to support with advertising and brand development, for an upfront fee of $500,000. What revenue should Egan recognize for December, Year 1?""",
    [("$310,833", "Correct. $300,000 for the software license at transfer, plus $60,000 ÷ 24 = $2,500 of support and $500,000 ÷ 60 = $8,333 of the brand license."),
     ("$368,333", "Recognizes the two years of support at the start. Support is a service provided over the two years."),
     ("$802,500", "Recognizes the whole franchise fee at the start. A brand license supported by ongoing activities gives a right to access, recognized over the license term."),
     ("$860,000", "Recognizes everything on December 1.")],
    "A",
    """The software is functional intellectual property whose utility does not depend on Egan's ongoing activities, so the license is a right to use recognized when control transfers: $300,000. Support is recognized over 24 months: $2,500 for December. The brand license is symbolic intellectual property, a right to access recognized over the five-year term: $500,000 ÷ 60 = $8,333. December revenue = $310,833."""),
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
