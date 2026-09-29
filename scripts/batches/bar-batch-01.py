"""BAR batch 01 — 25 items: the two moved out of FAR batch 01 because the AICPA CPA Exam Blueprints effective
January 2026 place their topics in BAR (see docs/reviews/far-batch-01.md, Revision 3), plus 23 written from
scratch (see docs/reviews/bar-batch-01.md). BAR targets: Area I 40–50%, Area II 35–45%, Area III 10–20%;
Remembering and Understanding 10–20%, Application 45–55%, Analysis 30–40%.

Run: python3 scripts/batches/bar-batch-01.py  (writes content/bar/*.yaml)
Every numeric answer and distractor below was recomputed in code during review.
"""
import os
import glob
from common import mcq as _mcq, finalize, audit, write_items, RU, AP, AN

A1 = "Area I — Business Analysis"
A2 = "Area II — Technical Accounting and Reporting"
A3 = "Area III — State and Local Governments"
NOTE = ("BAR batch 01. Answers solved and every number and distractor computed in code "
        "(the goodwill and nonexchange revenue items moved from FAR batch 01).")


def mcq(*a, **k):
    return _mcq(*a, section="BAR", batch=NOTE, **k)


ITEMS = [
# ── Area I ──────────────────────────────────────────────────────────────
mcq("bar-variance-analysis-0001", A1, "Managerial and cost accounting", AP,
    ["Standard costing: direct materials price and quantity variances"],
    """Brook Co.'s standard cost for each unit of its product includes 4 pounds of material at $3.00 per pound. During the month Brook produced 5,000 units, buying and using 21,000 pounds of material at $3.20 per pound. What are the direct materials price and quantity variances?""",
    [("$3,000 unfavorable price; $4,200 unfavorable quantity", "Swaps the two variances. The price variance is the price difference times the actual quantity ($0.20 × 21,000); the quantity variance is the excess pounds at standard price."),
     ("$4,000 unfavorable price; $3,200 unfavorable quantity", "Uses the standard quantity for the price variance and the actual price for the quantity variance. Price variance uses actual quantity; quantity variance uses standard price."),
     ("$4,200 unfavorable price; $3,000 unfavorable quantity", "Correct. Price: ($3.20 − $3.00) × 21,000 = $4,200 U. Quantity: (21,000 − 20,000) × $3.00 = $3,000 U."),
     ("$4,200 unfavorable price; $3,200 unfavorable quantity", "Prices the 1,000 excess pounds at the actual $3.20. The quantity variance uses the standard price, so price effects are not counted twice.")],
    "C",
    """Standard quantity allowed = 5,000 units × 4 pounds = 20,000 pounds. Price variance = (actual price − standard price) × actual quantity = $0.20 × 21,000 = $4,200 unfavorable. Quantity variance = (actual quantity − standard quantity) × standard price = 1,000 × $3.00 = $3,000 unfavorable. Together they explain the $7,200 total variance."""),

mcq("bar-cvp-what-if-0001", A1, "Budgeting, forecasting and projection", AN,
    ["Cost-volume-profit analysis: sensitivity and what-if analysis"],
    """Carver Co. sells 30,000 units a year of one product at $50 per unit. Variable costs are $30 per unit and fixed costs are $400,000 a year. Management is considering raising the price to $54, and its market study indicates unit sales would fall by 10%. Costs per unit and fixed costs would not change. What operating income should Carver expect under the proposal?""",
    [("$140,000", "Applies the 10% volume decline but keeps the $50 price. The proposal raises the contribution margin to $24 a unit."),
     ("$158,000", "Uses the new revenue ($1,458,000) but variable costs for the old 30,000 units. Variable costs fall with volume: 27,000 × $30."),
     ("$248,000", "Correct. 27,000 units × ($54 − $30) − $400,000."),
     ("$320,000", "Raises the price but ignores the expected 10% fall in unit sales.")],
    "C",
    """Under the proposal, unit sales = 30,000 × 90% = 27,000 and the contribution margin = $54 − $30 = $24 a unit. Operating income = 27,000 × $24 − $400,000 = $248,000, compared with 30,000 × $20 − $400,000 = $200,000 now, so the price increase adds $48,000."""),

mcq("bar-npv-0001", A1, "Investment alternatives using financial valuation decision models", AP,
    ["Capital budgeting: net present value"],
    """Delta Co. is evaluating Project Y, which costs $100,000 today and is expected to produce after-tax cash inflows of $55,000 at the end of each of Years 3, 4 and 5, with nothing in Years 1 and 2. Delta's discount rate is 10%. Present value factors at 10% are: single sum — Year 3 0.7513, Year 4 0.6830, Year 5 0.6209; ordinary annuity for 3 years 2.4869 and for 5 years 3.7908. What is Project Y's net present value?""",
    [("$13,036", "Correct. $55,000 × (0.7513 + 0.6830 + 0.6209) = $113,036, less the $100,000 cost."),
     ("$36,780", "Discounts the three inflows as if received in Years 1–3 ($55,000 × 2.4869). They arrive in Years 3–5."),
     ("$108,494", "Applies the five-year annuity factor to the $55,000 ($208,494) as if the inflows came every year for five years, then subtracts the cost. Years 1 and 2 have no inflow."),
     ("$65,000", "Ignores the time value of money: $165,000 of inflows less $100,000.")],
    "A",
    """NPV = present value of inflows − initial cost. Each inflow is discounted with its own single-sum factor because there are no inflows in Years 1 and 2: $55,000 × (0.7513 + 0.6830 + 0.6209) = $55,000 × 2.0552 = $113,036. NPV = $113,036 − $100,000 = $13,036."""),

mcq("bar-cost-of-capital-0001", A1, "Capital structure", AP,
    ["Weighted average cost of capital"],
    """Easton Corp.'s capital structure at market values is: debt $4,000,000 with a pretax yield of 8%; preferred stock $1,000,000 with a dividend yield of 7%; and common equity $5,000,000 with a required return of 12%. Easton's income tax rate is 25%. What is Easton's weighted average cost of capital?""",
    [("9.9%", "Uses the 8% pretax cost of debt. Interest is deductible, so debt's cost is 8% × (1 − 25%) = 6%."),
     ("8.3%", "Takes a simple average of the three component costs (6%, 7% and 12%) instead of weighting by market value."),
     ("8.9%", "Tax-adjusts the preferred dividend yield as well. Preferred dividends are not deductible, so preferred's cost is its full 7%."),
     ("9.1%", "Correct. 40% × 6% after-tax debt + 10% × 7% + 50% × 12%.")],
    "D",
    """Weights at market value: debt 40%, preferred 10%, common 50%. After-tax cost of debt = 8% × (1 − 25%) = 6%. Preferred dividends and common returns are not deductible. WACC = 0.40 × 6% + 0.10 × 7% + 0.50 × 12% = 2.4% + 0.7% + 6.0% = 9.1%."""),

mcq("bar-variable-absorption-costing-0001", A1, "Managerial and cost accounting", AP,
    ["Absorption and variable costing: income reconciliation"],
    """In its first year, Fenn Co. produced 10,000 units and sold 8,000. Fixed manufacturing overhead was $150,000, and there was no beginning inventory. Operating income under absorption costing was $210,000. What was Fenn's operating income under variable costing?""",
    [("$90,000", "Subtracts the $120,000 of fixed overhead in the units sold. Both methods expense that amount; only the overhead in ending inventory differs."),
     ("$180,000", "Correct. Absorption costing defers 2,000 × $15 = $30,000 of fixed overhead in ending inventory; variable costing expenses it."),
     ("$210,000", "Assumes the two methods give the same income. They differ whenever production and sales differ."),
     ("$240,000", "Adds the deferred fixed overhead instead of subtracting it. With inventory rising, absorption income is the higher figure.")],
    "B",
    """Fixed overhead per unit under absorption costing = $150,000 ÷ 10,000 = $15. Ending inventory of 2,000 units carries $30,000 of fixed overhead that absorption costing defers and variable costing expenses in full. Variable costing income = $210,000 − $30,000 = $180,000."""),

mcq("bar-financial-statement-analysis-0001", A1, "Financial statement analysis", AN,
    ["Financial statement analysis: interpreting profitability and activity ratios"],
    """Gale Co.'s sales rose 10% from Year 1 to Year 2. Over the same period its gross margin fell from 40% to 35%, its accounts receivable turnover fell from 8.0 to 6.0 times, and its inventory turnover fell from 6.0 to 4.0 times. Which explanation is most consistent with all of these changes?""",
    [("Gale cut prices and eased credit terms to win sales, while slow-moving goods built up in its warehouses.", "Correct. Lower prices reduce gross margin, easier credit slows collections, and unsold goods slow inventory turnover."),
     ("Gale tightened credit and trimmed inventory to free up cash, and it raised prices on its best sellers.", "Tighter credit and leaner inventory would raise both turnovers, and higher prices would lift gross margin."),
     ("Gale raised selling prices on steady unit volume, which lifted both its revenue and its gross margin.", "Gross margin fell, which is inconsistent with price increases on steady costs."),
     ("Gale shifted toward cash sales and just-in-time purchasing, which let it grow sales with less capital.", "More cash sales and just-in-time purchasing would raise receivable and inventory turnover, not lower them.")],
    "A",
    """Each ratio points the same way. A lower gross margin on higher sales suggests price cuts or rising costs. A lower receivables turnover means collections slowed relative to sales, consistent with easier credit terms. A lower inventory turnover means inventory grew faster than cost of sales, consistent with slow-moving goods. Only the first explanation fits all three."""),

mcq("bar-non-gaap-measures-0001", A1, "Non-financial and non-GAAP measures of performance", AN,
    ["SEC Regulation G and Item 10(e) of Regulation S-K (non-GAAP measures)", "Non-GAAP measures: EBITDA and adjusted EBITDA"],
    """Hale Inc. defines adjusted EBITDA as net income before interest, income taxes, depreciation and amortization, excluding restructuring charges and gains or losses on divestitures. For Year 1, Hale reports net income of $500,000, which reflects income tax expense of $150,000, interest expense of $80,000, depreciation of $120,000, amortization of $30,000, a restructuring charge of $70,000, and a $40,000 gain on the sale of a division. Hale's draft earnings release reports adjusted EBITDA of $990,000. Applying Hale's definition, what should adjusted EBITDA be?""",
    [("$760,000", "Leaves out the add-back for income tax expense. EBITDA starts from income before taxes."),
     ("$880,000", "Stops at EBITDA and does not make the adjustments in Hale's definition."),
     ("$910,000", "Correct. $500,000 + $150,000 + $80,000 + $120,000 + $30,000 + $70,000 restructuring − $40,000 gain."),
     ("$990,000", "Accepts the draft, which adds back the $40,000 gain. Excluding a gain means subtracting it, since it is included in net income.")],
    "C",
    """EBITDA = $500,000 + $150,000 taxes + $80,000 interest + $120,000 depreciation + $30,000 amortization = $880,000. Hale's adjustments exclude the restructuring charge (add back $70,000) and the divestiture gain (subtract $40,000, because it increased net income). Adjusted EBITDA = $910,000. The draft's $990,000 adds the gain back instead of removing it."""),

mcq("bar-make-or-buy-0001", A1, "Investment alternatives using financial valuation decision models", AN,
    ["Relevant costs: make-or-buy decisions and opportunity cost"],
    """Irwin Co. makes 10,000 units a year of a component at these costs per unit: direct materials $12, direct labor $8, variable overhead $5, and fixed overhead $10 (allocated from $100,000 of total fixed overhead). An outside supplier offers to sell the component for $30 per unit. If Irwin buys it, it can eliminate a $60,000 supervisor salary included in fixed overhead and rent the freed space to another company for $25,000 a year; the rest of the fixed overhead would continue. How would buying the component affect Irwin's annual operating income?""",
    [("$10,000 increase", "Leaves out the $25,000 of rent Irwin could earn on the freed space, an opportunity cost of continuing to make the part."),
     ("$35,000 increase", "Correct. Relevant cost to make: $250,000 variable + $60,000 avoidable salary + $25,000 forgone rent = $335,000, versus $300,000 to buy."),
     ("$50,000 decrease", "Compares only variable costs ($250,000) with the purchase price, ignoring the avoidable salary and the rent."),
     ("$75,000 increase", "Treats all $100,000 of fixed overhead as avoidable. Only the $60,000 salary goes away if Irwin buys.")],
    "B",
    """Relevant costs are those that differ between the alternatives. Making: variable costs 10,000 × $25 = $250,000, avoidable fixed overhead $60,000, and the $25,000 rent forgone = $335,000. Buying: 10,000 × $30 = $300,000. Buying raises operating income by $35,000. The other $40,000 of fixed overhead continues either way."""),

mcq("bar-sales-mix-variance-0001", A1, "Managerial and cost accounting", AN,
    ["Sales variances: sales mix and sales quantity variances"],
    """Jory Co. budgeted sales of 6,000 units of Product A with a contribution margin of $10 per unit and 4,000 units of Product B with a contribution margin of $20 per unit. It actually sold 8,400 units of A and 3,600 units of B, and actual contribution margins per unit equaled the budget. What is Jory's sales mix variance?""",
    [("$12,000 favorable", "Gets the amount right but the direction wrong. The mix shifted toward A, the lower-margin product, which reduces contribution margin."),
     ("$12,000 unfavorable", "Correct. At actual total volume of 12,000 units, A's share rose from 60% to 70% and B's fell from 40% to 30%: 1,200 × $10 − 1,200 × $20."),
     ("$16,000 favorable", "Computes the total sales volume variance (quantity $28,000 favorable less mix $12,000 unfavorable), not the mix variance alone."),
     ("$28,000 favorable", "Computes the sales quantity variance: 2,000 more units at the budgeted average margin of $14.")],
    "B",
    """Budgeted mix: A 60%, B 40%; budgeted average contribution margin = $140,000 ÷ 10,000 = $14. Mix variance = actual total units × (actual mix − budgeted mix) × budgeted margin: A 12,000 × 10% × $10 = $12,000 F; B 12,000 × (−10%) × $20 = $24,000 U; net $12,000 unfavorable. The quantity variance is (12,000 − 10,000) × $14 = $28,000 favorable."""),

mcq("bar-coso-erm-0001", A1, "Risk management", RU,
    ["COSO Enterprise Risk Management — Integrating with Strategy and Performance (2017)"],
    """Which of the following is one of the five components of COSO's 2017 Enterprise Risk Management — Integrating with Strategy and Performance framework?""",
    [("Control activities", "A component of COSO's Internal Control — Integrated Framework, not the ERM framework."),
     ("Review and revision", "Correct. The five ERM components are governance and culture; strategy and objective-setting; performance; review and revision; and information, communication, and reporting."),
     ("Monitoring activities", "A component of COSO's Internal Control — Integrated Framework."),
     ("Control environment", "A component of COSO's Internal Control — Integrated Framework; the ERM framework's comparable component is governance and culture.")],
    "B",
    """The 2017 COSO ERM framework has five components: governance and culture; strategy and objective-setting; performance; review and revision; and information, communication, and reporting. Control environment, control activities and monitoring activities belong to the Internal Control — Integrated Framework (2013)."""),

mcq("bar-performance-measures-impact-0001", A1, "Risk management", AN,
    ["Liquidity ratios: effect of transactions on the current and quick ratios"],
    """Kerr Co. has current assets of $600,000, of which $300,000 are quick assets (cash, marketable securities and receivables), and current liabilities of $400,000. Management proposes using $100,000 of cash to pay suppliers before year-end. If it does, what will Kerr's current ratio and quick ratio be?""",
    [("1.25 current ratio; 0.50 quick ratio", "Reduces the assets but not the liabilities. Paying suppliers lowers both cash and accounts payable."),
     ("1.50 current ratio; 0.75 quick ratio", "Assumes paying a liability with cash leaves both ratios unchanged. That holds only when a ratio equals 1.0."),
     ("1.67 current ratio; 0.67 quick ratio", "Correct. Current: $500,000 ÷ $300,000. Quick: $200,000 ÷ $300,000."),
     ("1.67 current ratio; 0.50 quick ratio", "Gets the current ratio right but, for the quick ratio, reduces quick assets without reducing current liabilities ($200,000 ÷ $400,000).")],
    "C",
    """Paying $100,000 of payables with cash reduces current assets, quick assets and current liabilities by the same amount. Current ratio: $500,000 ÷ $300,000 = 1.67 (up from 1.50, because it was above 1.0). Quick ratio: $200,000 ÷ $300,000 = 0.67 (down from 0.75, because it was below 1.0)."""),

# ── Area II ─────────────────────────────────────────────────────────────
mcq("bar-goodwill-impairment-0001", A2, "Indefinite-lived intangible assets, including goodwill", AP,
    ["ASC 350-20 (goodwill)", "ASC 350-30 (indefinite-lived intangible assets)", "ASU 2017-04 (simplifying the test for goodwill impairment)"],
    """Whitfield Corp., a public business entity, tests one reporting unit for impairment at year-end. The unit's carrying amount is $12,000,000, which includes goodwill of $3,000,000 and an indefinite-lived trade name carried at $2,000,000. Whitfield estimates the fair value of the reporting unit at $9,500,000 and the fair value of the trade name at $1,700,000. Ignore income tax effects. What goodwill impairment loss should Whitfield recognize?""",
    [("$0", "Compares the unit's $9,500,000 fair value with its carrying amount excluding goodwill ($9,000,000). The unit's carrying amount includes goodwill."),
     ("$2,200,000", "Correct. The trade name is impaired first by $300,000, leaving a carrying amount of $11,700,000; the goodwill loss is $11,700,000 − $9,500,000."),
     ("$2,500,000", "Measures goodwill against the full $12,000,000 carrying amount without first recognizing the $300,000 trade-name impairment, so that shortfall is counted twice."),
     ("$3,000,000", "Writes off all the goodwill. The loss is the amount by which carrying amount exceeds fair value, limited to the goodwill balance.")],
    "B",
    """When goodwill and other assets of a reporting unit are tested together, the other assets are tested first. The indefinite-lived trade name is impaired by $2,000,000 − $1,700,000 = $300,000, which reduces the reporting unit's carrying amount to $11,700,000. Goodwill impairment is the excess of the unit's carrying amount over its fair value, limited to goodwill: $11,700,000 − $9,500,000 = $2,200,000, which is less than the $3,000,000 of goodwill."""),

mcq("bar-software-for-sale-0001", A2, "Internally developed software", AP,
    ["ASC 985-20 (costs of software to be sold, leased or otherwise marketed)"],
    """Lyle Software develops a product to sell to customers. Before establishing technological feasibility it spent $300,000 on planning, design and testing. After technological feasibility and before the product was released for general sale on January 1, Year 1, it spent $200,000 on coding and testing. After release it spent $20,000 producing copies for customers and $30,000 on customer support. Year 1 revenue from the product is $400,000, and Lyle expects total revenue of $1,600,000 over the product's five-year economic life. What amortization of capitalized software costs should Lyle recognize in Year 1?""",
    [("$40,000", "Uses straight-line amortization only. Amortization is the greater of the revenue-ratio amount and the straight-line amount."),
     ("$50,000", "Correct. Capitalized costs of $200,000; revenue ratio 25% gives $50,000, which exceeds straight-line ($40,000)."),
     ("$100,000", "Capitalizes all $500,000 of development costs and amortizes it straight-line. Costs before technological feasibility are research and development expense."),
     ("$125,000", "Capitalizes all $500,000 of development costs before applying the 25% revenue ratio.")],
    "B",
    """Costs incurred before technological feasibility ($300,000) are R&D expense. Costs from technological feasibility until general release ($200,000) are capitalized. Duplication costs are inventory and support is expensed. Annual amortization is the greater of (a) current revenue ÷ total expected revenue × capitalized costs = $400,000 ÷ $1,600,000 × $200,000 = $50,000 and (b) straight-line over the remaining life = $200,000 ÷ 5 = $40,000. Year 1 amortization = $50,000."""),

mcq("bar-stock-compensation-0001", A2, "Stock compensation (share-based payments)", AP,
    ["ASC 718-10 (equity-classified awards; forfeitures)", "ASU 2016-09 (election to estimate forfeitures or account for them as they occur)"],
    """On January 1, Year 1, Hunt Corp. grants 10,000 stock options with a grant-date fair value of $12 each. The options cliff-vest after four years of service. Hunt's policy is to estimate forfeitures. At grant it expected 10% of the options to be forfeited; at the end of Year 2 it revises that estimate to 20%. What compensation cost should Hunt recognize in Year 2?""",
    [("$21,000", "Correct. Cumulative cost through Year 2 is $120,000 × 80% × 2/4 = $48,000, less the $27,000 recognized in Year 1."),
     ("$24,000", "Uses the revised estimate for Year 2's quarter share only ($120,000 × 80% ÷ 4), without the catch-up for Year 1."),
     ("$27,000", "Keeps the original 10% forfeiture estimate. A change in the estimate is recognized in the period of change through a cumulative catch-up."),
     ("$30,000", "Ignores forfeitures, although Hunt's policy is to estimate them.")],
    "A",
    """Total expected compensation cost = 10,000 × $12 × (1 − forfeiture rate), recognized over the four-year service period. Year 1: $120,000 × 90% × 1/4 = $27,000. At the end of Year 2, cumulative cost = $120,000 × 80% × 2/4 = $48,000. Year 2 cost = $48,000 − $27,000 = $21,000."""),

mcq("bar-research-development-0001", A2, "Research and development costs", RU,
    ["ASC 730-10 (research and development: activities included and excluded)"],
    """Which of the following costs is research and development expense under ASC 730?""",
    [("Routine quality-control testing of products during commercial production", "Excluded from R&D: quality control during commercial production is a production cost."),
     ("Market research to test customer reaction to a new product line", "Excluded from R&D: market research is a selling or marketing cost."),
     ("Engineering follow-through in an early phase of commercial production", "Excluded from R&D: follow-through after production begins is a production cost."),
     ("Salaries of engineers who design, build and test a preproduction prototype", "Correct. Designing, constructing and testing preproduction prototypes is a development activity.")],
    "D",
    """ASC 730 includes conceptual formulation, design and testing of product alternatives, and the design, construction and testing of preproduction prototypes and models. It excludes routine quality control, engineering follow-through in an early phase of commercial production, and market research."""),

mcq("bar-business-combination-0001", A2, "Business combinations", AP,
    ["ASC 805-30 (goodwill; consideration transferred including contingent consideration)", "ASC 805-10 (acquisition-related costs expensed)"],
    """Kent Corp. acquires 100% of Lark Inc. by paying $800,000 in cash and agreeing to pay more if Lark meets earnings targets; the acquisition-date fair value of that contingent payment is $50,000. The acquisition-date fair values of Lark's identifiable assets and liabilities are $1,100,000 and $400,000. Kent also pays $30,000 of legal and advisory fees to complete the acquisition. What amount of goodwill should Kent recognize?""",
    [("$50,000", "Subtracts the contingent consideration from the cash paid. Its acquisition-date fair value is part of the consideration transferred."),
     ("$100,000", "Leaves out the $50,000 of contingent consideration."),
     ("$150,000", "Correct. Consideration $850,000 less identifiable net assets $700,000."),
     ("$180,000", "Adds the $30,000 of acquisition costs to the consideration. Acquisition-related costs are expensed as incurred.")],
    "C",
    """Consideration transferred = $800,000 cash + $50,000 fair value of contingent consideration = $850,000. Identifiable net assets at fair value = $1,100,000 − $400,000 = $700,000. Goodwill = $850,000 − $700,000 = $150,000. The $30,000 of legal and advisory fees is expensed."""),

mcq("bar-foreign-currency-translation-0001", A2, "Consolidated financial statements", AP,
    ["ASC 830-30 (translation of financial statements; cumulative translation adjustment)"],
    """Moss Corp.'s foreign subsidiary uses the euro as its functional currency. At the beginning of the year its net assets were €1,000,000, when the exchange rate was $1.10 per euro. During the year it earned net income of €200,000 (average rate $1.15) and paid dividends of €50,000 when the rate was $1.12. The year-end rate is $1.20. What translation adjustment arises for the year in Moss's consolidated statements?""",
    [("$6,000 gain", "Captures only the effect on the year's income and dividends and ignores the change in rate on the beginning net assets."),
     ("$96,000 gain", "Translates net income at the year-end rate. Income is translated at the average rate."),
     ("$100,000 gain", "Captures only the rate change on the beginning net assets and ignores the year's income and dividends."),
     ("$106,000 gain", "Correct. Ending net assets €1,150,000 × $1.20 = $1,380,000, less $1,100,000 + $230,000 − $56,000 = $1,274,000.")],
    "D",
    """Translate each change in net assets at its historical rate: beginning €1,000,000 × $1.10 = $1,100,000; income €200,000 × $1.15 = $230,000; dividends €50,000 × $1.12 = $56,000. Total $1,274,000. Ending net assets at the current rate: €1,150,000 × $1.20 = $1,380,000. Translation adjustment = $106,000 gain, reported in other comprehensive income."""),

mcq("bar-interest-rate-swap-0001", A2, "Derivatives and hedge accounting", AP,
    ["ASC 815-20 and 815-30 (cash flow hedges)", "ASU 2017-12 (targeted improvements to hedge accounting)"],
    """On January 1, Year 1, Nash Co. borrows $1,000,000 at a variable rate of SOFR plus 1%, reset annually. To fix its interest cost, it enters into an interest rate swap to pay 5% fixed and receive SOFR on a $1,000,000 notional amount, and designates the swap as a cash flow hedge that qualifies for hedge accounting and is fully effective. SOFR for Year 1 is 4.5%, and settlements occur each December 31. At December 31, Year 1, the swap's fair value rises to an asset of $12,000. What interest expense does Nash report for Year 1, and what amount does it report in other comprehensive income?""",
    [("$48,000 interest expense; $0 in other comprehensive income", "Reports the $12,000 gain in earnings as a reduction of interest. For a qualifying cash flow hedge, the change in the swap's fair value goes to OCI."),
     ("$55,000 interest expense; $12,000 in other comprehensive income", "Omits the $5,000 net swap payment, which is part of Nash's interest cost."),
     ("$60,000 interest expense; $0 in other comprehensive income", "Recognizes interest correctly but puts the swap's fair value change in earnings."),
     ("$60,000 interest expense; $12,000 in other comprehensive income", "Correct. Debt interest $55,000 (5.5%) plus the $5,000 net swap payment; the $12,000 fair value change goes to OCI.")],
    "D",
    """Interest on the debt = $1,000,000 × (4.5% + 1%) = $55,000. The swap's net settlement: Nash pays 5% and receives 4.5%, a net payment of $5,000, recorded as interest expense, so total interest expense is $60,000 (a fixed 6%). For a qualifying cash flow hedge, the change in the swap's fair value ($12,000) is recorded in other comprehensive income and reclassified to earnings when the hedged interest payments affect earnings."""),

mcq("bar-revenue-contract-analysis-0001", A2, "Revenue recognition", AN,
    ["ASC 606-10 (control transfer; bill-and-hold arrangements; consignment arrangements)"],
    """Oakes Co. reviews three December arrangements before closing its year on December 31. (1) Oakes finished building $120,000 of equipment to one customer's specifications. The customer, whose new plant will not open until February, asked in writing that Oakes keep the equipment until then; it inspected and accepted the equipment in December and was billed on normal terms, and Oakes has set it aside in its warehouse under the customer's name. (2) Oakes shipped $80,000 of goods to a dealer, which pays Oakes only when it sells them to its own customers and may return any unsold goods. (3) On December 30 Oakes shipped $50,000 of goods FOB destination; they arrived January 3. What revenue should Oakes recognize in December from these arrangements?""",
    [("$120,000", "Correct. Control of the held equipment has passed to the customer; the consigned goods and the goods in transit under FOB destination have not transferred."),
     ("$170,000", "Also recognizes the goods shipped FOB destination. Control passes when the goods reach the customer on January 3."),
     ("$200,000", "Also recognizes the goods shipped to the dealer. The dealer does not control them: it pays only when it resells and can return unsold goods, so the arrangement is a consignment."),
     ("$250,000", "Recognizes all three arrangements.")],
    "A",
    """Revenue is recognized when control transfers. (1) This is a bill-and-hold arrangement that transfers control: the customer asked for the hold for a substantive reason (its plant is not ready), the equipment is set aside under its name, it is finished and accepted so it is ready for delivery, and because it is built to the customer's specifications Oakes cannot use it for anyone else: $120,000. (2) The dealer arrangement is a consignment: Oakes keeps control until the dealer sells. (3) Under FOB destination, control passes on delivery in January. December revenue = $120,000."""),

mcq("bar-lessor-sales-type-0001", A2, "Leases", AP,
    ["ASC 842-30 (lessor accounting: sales-type leases)"],
    """On January 1, Year 1, Pratt Equipment leases a machine to a customer for five years, with $85,000 due at the beginning of each year. Title transfers to the customer at the end of the lease. The machine's carrying amount on Pratt's books is $300,000 and its fair value is $366,529. The rate implicit in the lease is 8%; present value factors at 8% for five periods are 4.3121 for an annuity due and 3.9927 for an ordinary annuity. What selling profit should Pratt recognize at lease commencement?""",
    [("$0", "Defers the profit over the lease term. A lease that transfers ownership is a sales-type lease, and selling profit is recognized at commencement."),
     ("$39,380", "Discounts the payments as an ordinary annuity ($339,380). Payments are due at the beginning of each year, so the annuity-due factor applies."),
     ("$66,529", "Correct. Present value of payments $85,000 × 4.3121 = $366,529, less the $300,000 carrying amount."),
     ("$125,000", "Uses the undiscounted payments ($425,000). The lessor measures the sale at the present value of the lease payments.")],
    "C",
    """Transfer of ownership makes this a sales-type lease. Revenue equals the lower of fair value and the present value of lease payments: $85,000 × 4.3121 = $366,529, which equals fair value. Selling profit = $366,529 − $300,000 carrying amount = $66,529, recognized at commencement, with a net investment in the lease of $366,529."""),

mcq("bar-segment-reporting-0001", A2, "Public company reporting topics", RU,
    ["ASC 280-10 (segment reporting: quantitative thresholds)", "ASU 2023-07 (improvements to reportable segment disclosures; thresholds unchanged)"],
    """Under ASC 280, one test that makes an operating segment reportable is based on its revenue. What is that threshold?""",
    [("Revenue of at least 10% of the combined revenue of all operating segments, including intersegment sales", "Correct. The revenue test includes both external and intersegment revenue."),
     ("Revenue of at least 10% of combined revenue of all operating segments from external customers only", "The revenue test counts intersegment revenue too."),
     ("Revenue of at least 5% of the combined revenue of all operating segments, including intersegment sales", "The threshold is 10%, not 5%."),
     ("Revenue that brings reported segments to 75% of consolidated revenue from external customers", "That is the separate test of whether enough segments have been reported, not the threshold for an individual segment.")],
    "A",
    """An operating segment is reportable if it meets any one of three 10% tests: its revenue (external and intersegment) is at least 10% of combined segment revenue; its profit or loss is at least 10% of the greater of combined profits or combined losses; or its assets are at least 10% of combined segment assets. Separately, reportable segments must together account for at least 75% of consolidated external revenue. ASU 2023-07 added disclosures but left these thresholds unchanged."""),

mcq("bar-revenue-analytics-discrepancy-0001", A2, "Revenue recognition", AN,
    ["ASC 606-10 (transfer of control; variable consideration; licenses providing a right to access)"],
    """A data analytics report of Quill Co.'s fourth-quarter revenue, which totals $2,000,000, flags three outliers for review. (1) A $300,000 sale to a new customer invoiced December 30; the goods were shipped FOB destination and delivered January 5. (2) A $400,000 December sale to a distributor that, based on Quill's recent practice, will receive a $50,000 price concession; Quill granted it on January 10, and it had been expected at year-end. (3) An $80,000 invoice dated December 31 for a one-year license, starting January 1, that gives the customer access to Quill's continually updated online content. After resolving these items, what should Quill's fourth-quarter revenue be?""",
    [("$1,570,000", "Correct. $2,000,000 − $300,000 undelivered sale − $50,000 expected concession − $80,000 license for next year."),
     ("$1,620,000", "Keeps the full $400,000 for the distributor sale. An expected price concession is variable consideration that reduces revenue when the sale is recognized."),
     ("$1,650,000", "Keeps the $80,000 license. A license that gives access to continually updated content is recognized over the license period, which begins January 1."),
     ("$1,870,000", "Keeps the $300,000 sale. Under FOB destination, control passed on delivery in January.")],
    "A",
    """(1) Control of the goods passed on delivery on January 5, so the $300,000 is next year's revenue. (2) Quill's practice made a price concession expected when the sale was made, so the transaction price was $350,000; reduce revenue by $50,000. (3) A right-to-access license is recognized over time as access is provided, starting January 1; none belongs in the fourth quarter. Revenue = $2,000,000 − $300,000 − $50,000 − $80,000 = $1,570,000."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("bar-nonexchange-revenue-0001", A3, "Nonexchange revenue transactions", AP,
    ["GASB Statement No. 33 (nonexchange transactions)", "GASB Statement No. 34 (government-wide and fund financial statements)", "GASB Statement No. 65 (deferred inflows of resources)"],
    """Lakeview Township's fiscal year is the calendar year. On January 1, Year 5, it levies $4,000,000 of property taxes to finance Year 5 operations. The levy becomes legally enforceable that day, and no taxes were prepaid. The township expects 2% of the levy to prove uncollectible. It collects $3,650,000 through December 31, Year 5, and $150,000 during the first 45 days of Year 6, and it expects to collect the rest of the collectible amount between 90 and 120 days after year-end. In its governmental funds, the township treats property taxes as available if collected within 60 days after year-end. By how much does property tax revenue in the government-wide statement of activities exceed property tax revenue in the general fund's statement of revenues, expenditures, and changes in fund balance?""",
    [("$0", "Applies one basis to both statements. Government-wide statements use full accrual and the funds use modified accrual, so the amounts differ."),
     ("$120,000", "Correct. Government-wide: $4,000,000 less $80,000 expected uncollectible is $3,920,000. General fund: $3,650,000 + $150,000 = $3,800,000. The remaining $120,000 will arrive too late to be available, so the fund reports it as a deferred inflow of resources."),
     ("$200,000", "Leaves the expected uncollectible amount out of the government-wide figure ($4,000,000 − $3,800,000). Government-wide revenue is net of the $80,000 the township expects not to collect."),
     ("$270,000", "Measures fund revenue at cash collected by year-end only ($3,650,000), ignoring the $150,000 collected within the 60-day availability period.")],
    "B",
    """Government-wide statements use the economic resources focus and full accrual. The levy is for Year 5 and enforceable on January 1, so Year 5 revenue is $4,000,000 − $80,000 = $3,920,000. Governmental funds use the current financial resources focus and modified accrual, so revenue is limited to amounts collected by year-end or within the 60-day availability period: $3,650,000 + $150,000 = $3,800,000. The $120,000 of collectible taxes expected later is a deferred inflow of resources in the fund. Difference: $3,920,000 − $3,800,000 = $120,000."""),

mcq("bar-government-wide-reconciliation-0001", A3, "Deriving government-wide financial statements and reconciliation requirements", AN,
    ["GASB Statement No. 34 (reconciliation of governmental fund balances to net position of governmental activities)", "GASB Statement No. 65 (deferred inflows of resources)"],
    """Rowan County's governmental funds report total fund balances of $2,000,000. Other information: capital assets used in governmental activities, net of accumulated depreciation, $5,000,000; general obligation bonds payable, $3,000,000; interest accrued on those bonds but not due until next year, $50,000; property taxes that will be collected after the availability period and are reported as deferred inflows of resources in the funds, $120,000; and an internal service fund, whose net position of $200,000 serves mainly governmental departments. What net position should Rowan report for governmental activities in its government-wide statement of net position?""",
    [("$4,030,000", "Subtracts the $120,000 of unavailable property taxes instead of adding it. Under full accrual they are revenue, so the deferred inflow is removed and net position rises."),
     ("$4,070,000", "Leaves out the internal service fund. When it serves mainly governmental departments, its net position is included in governmental activities."),
     ("$4,150,000", "Leaves the $120,000 of unavailable property taxes as a deferred inflow. Availability is a modified accrual concept; full accrual recognizes the revenue."),
     ("$4,270,000", "Correct. $2,000,000 + $5,000,000 − $3,000,000 − $50,000 + $120,000 + $200,000.")],
    "D",
    """Start from governmental fund balances and adjust to the economic resources focus: add capital assets ($5,000,000), subtract long-term debt ($3,000,000) and accrued interest not yet due ($50,000), add back property taxes deferred only because they are unavailable ($120,000), and add the internal service fund's net position ($200,000) because it mainly serves governmental activities. Net position = $4,270,000."""),

mcq("bar-budgetary-accounting-0001", A3, "Budgetary accounting", RU,
    ["GASB Codification 1700 (budgetary accounting; encumbrances)", "GASB Statement No. 54 (encumbrances within fund balance)"],
    """A city's general fund, which records encumbrances, issues a purchase order for $40,000 of supplies. Which entry does it record when the order is issued?""",
    [("Debit encumbrances; credit budgetary fund balance — reserved for encumbrances, $40,000", "Correct. An encumbrance entry commits the appropriation when the order is issued."),
     ("Debit expenditures; credit vouchers payable, $40,000, and close the related appropriation", "The expenditure and liability are recorded when the supplies are received, not when the order is placed."),
     ("Debit appropriations; credit encumbrances, $40,000, to reduce the spending authority available", "Not a standard entry; appropriations are recorded when the budget is adopted and closed at year-end."),
     ("Debit supplies inventory; credit accounts payable, $40,000, at the purchase order price", "A full-accrual entry on receipt of goods; the order alone creates no asset or liability.")],
    "A",
    """When a purchase order is issued, a government using encumbrance accounting records Dr Encumbrances, Cr Budgetary fund balance — reserved for encumbrances, to track the commitment against the appropriation. When the goods arrive, it reverses the encumbrance and records the expenditure and liability at the actual amount."""),
]

if __name__ == "__main__":
    finalize(ITEMS)
    warnings = audit(ITEMS)
    out = os.path.join(os.path.dirname(__file__), "..", "..", "content", "bar")
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
