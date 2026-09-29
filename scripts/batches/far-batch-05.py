"""FAR batch 05 — 25 items written from scratch for the gaps named by the batch 04 review (see
docs/reviews/far-batch-05.md). Target skill mix 3 / 13 / 9. Scope and skill tags follow the AICPA CPA Exam
Blueprints effective January 2026.

Run: python3 scripts/batches/far-batch-05.py  (writes content/far/*.yaml; leaves other batches' files alone)
Every numeric answer and distractor below was computed in code (Decimal, rounded half up).
"""
import os
from common import mcq as _mcq, finalize, audit, write_items, RU, AP, AN

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 05. Written from scratch; answers solved and every number and distractor computed in code."


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


ITEMS = [
# ── Area I ──────────────────────────────────────────────────────────────
mcq("far-foreign-currency-transactions-0001", A1, "Income statement", AP,
    ["ASC 830-20 (foreign currency transactions)"],
    """On November 1, Year 1, Abbott Co., whose functional currency is the U.S. dollar, buys inventory from a German supplier for €100,000, payable on February 1, Year 2. Exchange rates for one euro were $1.10 on November 1, $1.14 on December 31, and $1.12 on February 1, when Abbott paid the invoice. What foreign currency transaction gain or loss should Abbott report in Year 1 and in Year 2?""",
    [("$0 in Year 1; $2,000 loss in Year 2", "Waits until settlement and compares the payment with the original rate. The payable is remeasured at each balance sheet date."),
     ("$4,000 gain in Year 1; $2,000 loss in Year 2", "Reverses the signs, as if Abbott held a euro receivable. A stronger euro increases what Abbott owes."),
     ("$4,000 loss in Year 1; $2,000 gain in Year 2", "Correct. Year 1: €100,000 × ($1.14 − $1.10). Year 2: €100,000 × ($1.14 − $1.12)."),
     ("$4,000 loss in Year 1; $2,000 loss in Year 2", "Measures Year 2 against the original $1.10 rate instead of the December 31 rate, counting part of the Year 1 loss again.")],
    "C",
    """A payable denominated in a foreign currency is remeasured at the spot rate at each balance sheet date and at settlement, with changes reported in net income. December 31: the payable rises from $110,000 to $114,000, a $4,000 loss in Year 1. February 1: Abbott pays $112,000, so Year 2 has a $2,000 gain."""),

mcq("far-performance-metrics-0002", A1, "Financial Statement Ratios and Performance Metrics", AP,
    ["Financial statement analysis: EBITDA and asset turnover"],
    """For Year 2, Brand Co. reports revenue of $5,000,000 and net income of $400,000, after interest expense of $100,000, income tax expense of $120,000, and depreciation and amortization of $280,000. Total assets were $3,800,000 at the start of the year and $4,200,000 at the end. Using average total assets, what are Brand's EBITDA and asset turnover?""",
    [("$620,000 EBITDA; 1.25 asset turnover", "Leaves out the $280,000 of depreciation and amortization, which EBITDA adds back."),
     ("$800,000 EBITDA; 1.25 asset turnover", "Leaves out the $100,000 of interest expense, which EBITDA adds back."),
     ("$900,000 EBITDA; 1.19 asset turnover", "Gets EBITDA right but divides revenue by ending total assets instead of the average."),
     ("$900,000 EBITDA; 1.25 asset turnover", "Correct. EBITDA = $400,000 + $100,000 + $120,000 + $280,000; asset turnover = $5,000,000 ÷ $4,000,000.")],
    "D",
    """EBITDA = net income + interest + income taxes + depreciation and amortization = $400,000 + $100,000 + $120,000 + $280,000 = $900,000. Asset turnover = revenue ÷ average total assets = $5,000,000 ÷ [($3,800,000 + $4,200,000) ÷ 2] = 1.25."""),

mcq("far-comprehensive-income-0003", A1, "Statement of comprehensive income", RU,
    ["ASC 220-10 (items of other comprehensive income)", "ASC 321-10 (equity securities, after ASU 2016-01)"],
    """Which of the following is reported in other comprehensive income?""",
    [("An unrealized gain on equity securities that have a readily determinable fair value", "Since ASU 2016-01, changes in the fair value of equity securities are reported in net income."),
     ("An unrealized holding gain on available-for-sale debt securities", "Correct. Unrealized holding gains and losses on AFS debt securities are reported in other comprehensive income."),
     ("A gain from remeasuring a payable denominated in a foreign currency", "A foreign currency transaction gain is reported in net income."),
     ("An unrealized gain on debt securities classified as trading securities", "Changes in the fair value of trading securities are reported in net income.")],
    "B",
    """Other comprehensive income includes unrealized holding gains and losses on available-for-sale debt securities, foreign currency translation adjustments, certain pension and postretirement amounts, and effective portions of cash flow hedges. Fair value changes on equity securities and trading securities, and foreign currency transaction gains and losses, go to net income."""),

mcq("far-nfp-statement-of-activities-0001", A1, "Statement of activities (Not-for-Profit)", AP,
    ["ASC 958-225 (statement of activities)", "ASC 958-205 (net assets released from restrictions)"],
    """For Year 1, Cedar Clinic, a not-for-profit entity, reports: contributions without donor restrictions of $500,000; contributions with donor restrictions of $100,000; program service fees of $200,000; net assets released from donor restrictions of $150,000; investment return on unrestricted investments, net of external investment expenses, of $20,000; and expenses of $780,000 ($600,000 for programs, $120,000 for management and general, and $60,000 for fundraising). What is the change in Cedar's net assets without donor restrictions for Year 1?""",
    [("$90,000 increase", "Correct. $500,000 + $200,000 + $150,000 released + $20,000 − $780,000."),
     ("$190,000 increase", "Also counts the $100,000 of restricted contributions. They increase net assets with donor restrictions until released."),
     ("$60,000 decrease", "Leaves out the $150,000 released from donor restrictions. Releases increase net assets without donor restrictions."),
     ("$270,000 increase", "Subtracts only the $600,000 of program expenses. Management and general and fundraising expenses also reduce net assets without donor restrictions.")],
    "A",
    """Net assets without donor restrictions increase by unrestricted contributions ($500,000), program service fees ($200,000), releases from restrictions ($150,000) and net investment return ($20,000), and decrease by all expenses ($780,000): a $90,000 increase. The $100,000 of restricted contributions increases net assets with donor restrictions."""),

mcq("far-balance-sheet-0004", A1, "Balance sheet", AN,
    ["ASC 210-10 (current liabilities)", "ASC 740-10 (deferred taxes classified as noncurrent, after ASU 2015-17)", "ASC 842-20 (lessee presentation)"],
    """Dale Co.'s draft December 31, Year 1, classified balance sheet reports total noncurrent liabilities of $2,100,000: bonds payable $1,500,000, operating lease liabilities $400,000, deferred tax liability $150,000, and warranty liability $50,000. Supporting schedules show that $300,000 of the bonds mature on June 30, Year 2; that $60,000 of the lease liability will be paid during Year 2; and that the warranty claims are all expected to be paid during Year 2. After correcting the draft, what are Dale's total noncurrent liabilities?""",
    [("$1,540,000", "Also moves the $150,000 deferred tax liability to current. Deferred taxes are always classified as noncurrent."),
     ("$1,690,000", "Correct. $1,200,000 of bonds + $340,000 of lease liability + $150,000 deferred tax liability."),
     ("$1,750,000", "Leaves the $60,000 current portion of the lease liability in noncurrent."),
     ("$1,990,000", "Leaves the $300,000 of bonds maturing in Year 2 in noncurrent.")],
    "B",
    """Liabilities due within a year are current: the $300,000 of bonds maturing in Year 2, the $60,000 of lease payments due in Year 2, and the $50,000 warranty liability. Deferred tax liabilities are classified as noncurrent. Noncurrent liabilities = $1,200,000 + $340,000 + $150,000 = $1,690,000."""),

mcq("far-cash-flows-0007", A1, "Statement of cash flows", AN,
    ["ASC 230-10 (indirect method; classification)"],
    """Eads Co.'s staff accountant prepared this draft operating section of the statement of cash flows under the indirect method: net income $300,000; depreciation $50,000; amortization of discount on bonds payable $4,000; increase in deferred tax liability $12,000; gain on sale of land $(25,000); increase in accounts payable $18,000; increase in inventory $22,000; proceeds from issuing common stock $100,000; net cash provided by operating activities $481,000. After correcting the draft to comply with U.S. GAAP, what is net cash provided by operating activities?""",
    [("$337,000", "Correct. The inventory increase is subtracted ($44,000 swing) and the stock proceeds move to financing."),
     ("$381,000", "Moves the stock proceeds to financing but still adds the increase in inventory. Buying more inventory uses cash."),
     ("$437,000", "Subtracts the inventory increase but leaves the $100,000 of stock proceeds in operating activities."),
     ("$481,000", "Accepts the draft.")],
    "A",
    """Two errors. An increase in inventory is subtracted under the indirect method, not added: that changes the total by $44,000. Proceeds from issuing stock are a financing inflow. The other adjustments are right: depreciation, discount amortization and the deferred tax increase are noncash charges added back, the gain on land is subtracted, and the payables increase is added. Corrected: $481,000 − $44,000 − $100,000 = $337,000."""),

mcq("far-changes-in-equity-0002", A1, "Statement of changes in equity", AN,
    ["ASC 505-20 (stock splits)", "ASC 505-10 (dividends declared)", "ASC 220-10 (accumulated other comprehensive income)"],
    """Faye Inc.'s draft Year 1 statement of changes in equity reports ending retained earnings of $980,000, computed as beginning retained earnings of $800,000, plus net income of $250,000, plus a $30,000 unrealized holding gain on available-for-sale debt securities, less $100,000 for a 2-for-1 stock split. Supporting documents show that the split was effected by halving the par value per share, and that on December 15, Year 1, the board declared a $40,000 cash dividend payable on January 10, Year 2, which the draft omits because it had not been paid. After correcting the draft, what is Faye's ending retained earnings?""",
    [("$910,000", "Removes the unrealized gain and records the dividend but still charges retained earnings for the split. A split effected by halving par value needs no entry to retained earnings."),
     ("$1,010,000", "Correct. $800,000 + $250,000 − $40,000 declared dividend."),
     ("$1,040,000", "Records the dividend and removes the split charge but leaves the $30,000 unrealized gain in retained earnings. It belongs in accumulated other comprehensive income."),
     ("$1,050,000", "Removes the split charge and the unrealized gain but omits the dividend. A dividend reduces retained earnings when declared, not when paid.")],
    "B",
    """Three corrections. (1) The unrealized gain on AFS debt securities is other comprehensive income, accumulated separately from retained earnings. (2) A stock split effected by reducing par value requires no entry. (3) Dividends reduce retained earnings on the declaration date. Ending retained earnings = $800,000 + $250,000 − $40,000 = $1,010,000."""),

mcq("far-consolidated-statements-0006", A1, "Consolidated financial statements", AN,
    ["ASC 810-10 (consolidation procedures: intercompany balances and transactions)"],
    """Pym Corp. owns 100% of Tovey Inc. Pym's draft December 31, Year 1, consolidated balance sheet reports total assets of $4,200,000; to prepare it, the staff eliminated Pym's investment in Tovey against Tovey's equity and added the two companies' other balances. Supporting schedules show that on July 1, Year 1, Pym lent Tovey $500,000 at 6%, with interest due each June 30, and that both companies accrued interest at December 31. After any corrections needed, what total assets should the consolidated balance sheet report?""",
    [("$3,670,000", "Eliminates the accrued interest twice, once for each company's accrual. Only Pym's $15,000 receivable is an asset."),
     ("$3,685,000", "Correct. $4,200,000 − $500,000 note receivable − $15,000 accrued interest receivable."),
     ("$3,700,000", "Eliminates the note but not the $15,000 of accrued interest receivable."),
     ("$4,200,000", "Accepts the draft. Balances between parent and subsidiary are eliminated, not only the investment account.")],
    "B",
    """Consolidated statements present the group as one entity, so the intercompany loan is eliminated along with the investment. Pym's note receivable ($500,000) and accrued interest receivable ($500,000 × 6% × 6/12 = $15,000) come out of assets, and Tovey's matching payables come out of liabilities. Total assets = $4,200,000 − $515,000 = $3,685,000."""),

mcq("far-notes-0004", A1, "Notes to financial statements", AN,
    ["ASC 740-10 (deferred taxes classified as noncurrent, after ASU 2015-17)", "ASC 855-10 (nonrecognized subsequent events)", "ASC 842-20 (lease maturity disclosures)", "ASC 360-10 (property, plant and equipment)"],
    """Galton Co.'s draft December 31, Year 1, balance sheet, for statements to be issued on March 10, Year 2, reports among current assets a deferred tax asset of $12,000, property and equipment, net, of $1,500,000, and operating lease liabilities of $180,000. You compare four draft note excerpts with the statements. Income taxes: deferred tax assets and liabilities are classified as current or noncurrent according to the classification of the related asset or liability; the $12,000 current deferred tax asset arises from accrued warranty costs. Property and equipment: cost of $2,400,000 less accumulated depreciation of $900,000. Leases: undiscounted lease payments of $195,000 less imputed interest of $15,000. Subsequent events: on February 10, Year 2, Galton agreed to acquire a competitor for $3,000,000 in cash; no amounts are recognized in Year 1. Which note reveals that the draft financial statements must be corrected?""",
    [("The income tax note", "Correct. Since ASU 2015-17, all deferred tax assets and liabilities are classified as noncurrent, so the $12,000 must move out of current assets and the policy note must change."),
     ("The property and equipment note", "Consistent. $2,400,000 − $900,000 = $1,500,000."),
     ("The lease note", "Consistent. $195,000 − $15,000 = $180,000, the liability on the balance sheet."),
     ("The subsequent events note", "Consistent. An acquisition agreed after year-end is a nonrecognized event that is disclosed.")],
    "A",
    """ASU 2015-17 requires all deferred tax assets and liabilities to be presented as noncurrent (netted by jurisdiction). The income tax note describes the superseded current/noncurrent split, and the draft balance sheet follows it by showing a $12,000 current deferred tax asset, so the classification and the note must be corrected. The other three notes agree with the statements and with GAAP."""),

# ── Area II ─────────────────────────────────────────────────────────────
mcq("far-troubled-debt-restructuring-0001", A2, "Debt (Notes and bonds payable)", RU,
    ["ASC 470-60 (troubled debt restructurings by debtors)", "ASU 2022-02 (eliminated TDR accounting for creditors only)"],
    """Under ASC 470-60, which of the following changes in debt terms is a troubled debt restructuring for the debtor?""",
    [("A lender lowers the rate to the current market rate to keep a creditworthy borrower from refinancing elsewhere", "No financial difficulty: a market-rate change for a healthy borrower is a modification or extinguishment, not a troubled debt restructuring."),
     ("A borrower that has missed two payments refinances with a new lender at the market rate for its credit risk", "No concession: market terms for the borrower's actual risk are not a concession, even though the borrower is struggling."),
     ("A lender cuts the rate below market and defers principal because the borrower cannot meet its payments", "Correct. The debtor is in financial difficulty, and the creditor grants a concession it would not otherwise give."),
     ("A healthy borrower extends its note, and the new cash flows' present value differs from the old by 12%", "The 10% test decides modification versus extinguishment when the change is not troubled; this borrower is not in difficulty.")],
    "C",
    """A restructuring is troubled for the debtor when the debtor is experiencing financial difficulties and the creditor, for economic or legal reasons related to those difficulties, grants a concession it would not otherwise consider. ASU 2022-02 removed TDR accounting for creditors, but ASC 470-60 still applies to debtors."""),

mcq("far-software-purchased-0001", A2, "Intangible assets", AP,
    ["ASC 350-40 (internal-use software)", "ASU 2025-06 (targeted improvements to internal-use software; same result here)"],
    """On January 1, Year 1, Hart Co. buys a perpetual license for accounting software to use internally for $240,000. It also pays a consultant $60,000 to configure the software for Hart's processes, $15,000 to train employees, and $10,000 to convert data from its old system. The software is ready for its intended use on April 1, Year 1, and Hart amortizes it straight-line over five years. What total expense related to these costs should Hart recognize in Year 1?""",
    [("$48,750", "Capitalizes the training and data conversion costs as well. Both are expensed as incurred."),
     ("$70,000", "Correct. Capitalized cost $300,000 ÷ 5 × 9/12 = $45,000 of amortization, plus $25,000 of training and data conversion."),
     ("$85,000", "Amortizes from January 1. Amortization begins when the software is ready for its intended use on April 1."),
     ("$121,000", "Expenses the $60,000 of configuration. Costs to configure internal-use software for its intended use are capitalized.")],
    "B",
    """The license ($240,000) and the configuration needed to make the software ready for use ($60,000) are capitalized: $300,000. Training ($15,000) and data conversion ($10,000) are expensed. Amortization starts April 1: $300,000 ÷ 5 × 9/12 = $45,000. Year 1 expense = $45,000 + $25,000 = $70,000."""),

mcq("far-investments-equity-securities-0001", A2, "Investments (Financial assets at fair value)", AP,
    ["ASC 321-10 (equity securities without readily determinable fair values: measurement alternative and impairment)"],
    """In January, Iredale Co. pays $400,000 for 5% of the shares of a private company whose shares have no readily determinable fair value, and elects the measurement alternative. In June, the investee sells identical shares to an unrelated investor in an orderly transaction at a price implying that Iredale's shares are worth $460,000. In November, the investee loses its largest customer, which provided 40% of its revenue, and Iredale estimates the shares' fair value at $380,000. At what amount should Iredale report the investment at year-end?""",
    [("$320,000", "Measures the impairment from cost ($400,000 − $80,000). The June observable price change had already raised the carrying amount to $460,000."),
     ("$380,000", "Correct. Adjusted up to $460,000 for the observable price change, then written down to its $380,000 fair value when impaired."),
     ("$400,000", "Keeps cost, ignoring both the observable price change and the impairment."),
     ("$460,000", "Records the June observable price change but not the November impairment.")],
    "B",
    """Under the measurement alternative, the investment is carried at cost less impairment, adjusted for observable price changes in orderly transactions for identical or similar securities. June: adjust to $460,000 (a $60,000 gain in net income). November: impairment indicators require measuring the investment at fair value, $380,000 (an $80,000 loss in net income). Year-end carrying amount = $380,000."""),

mcq("far-equity-method-0002", A2, "Investments (Equity method investments)", AP,
    ["ASC 323-10 (equity method: becoming an equity method investor, applied prospectively after ASU 2016-07)"],
    """Jade Co. owns 10% of Varro Inc., carried at fair value with changes in net income; its fair value on July 1, Year 1, immediately before the purchase below, is $150,000. That day Jade buys another 20% of Varro for $330,000, a price that includes a premium for obtaining significant influence. Varro's net income totals $380,000 for Year 1 ($200,000 from July 1 to December 31), and Varro pays dividends of $50,000 in December. Any excess of cost over Jade's share of Varro's book value is attributable to goodwill, which Jade does not amortize. At what amount should Jade report its investment in Varro at December 31, Year 1?""",
    [("$465,000", "Deducts Jade's share of the December dividend but never adds its share of Varro's income."),
     ("$480,000", "Stops at the combined cost basis of $480,000 without applying the equity method from July 1."),
     ("$510,000", "Applies only the newly purchased 20% to Varro's income and dividends. The equity method applies to Jade's whole 30% interest from July 1."),
     ("$525,000", "Correct. $150,000 + $330,000 + 30% × $200,000 − 30% × $50,000.")],
    "D",
    """Since ASU 2016-07, an investor that becomes eligible for the equity method adds the cost of the new interest to the current basis of its existing interest and applies the equity method prospectively, with no retroactive adjustment. Basis on July 1 = $150,000 + $330,000 = $480,000. Add 30% of Varro's income after July 1 ($60,000) and subtract 30% of the dividends ($15,000): $525,000."""),

mcq("far-payables-cutoff-0001", A2, "Payables and accrued liabilities", AN,
    ["ASC 405-10 (liabilities)", "ASC 330-10 (goods in transit)"],
    """Kirk Co.'s draft December 31, Year 1, balance sheet reports accounts payable of $620,000; Kirk records all vendor bills, including utilities, in accounts payable. Searching for unrecorded liabilities, you examine January, Year 2, payments and invoices and find: (1) a $21,000 invoice for goods shipped FOB shipping point on December 22 and received December 29, not recorded until January; (2) a $9,000 bill for December utilities, received and recorded in January; (3) a $25,000 invoice for goods shipped FOB destination on December 30 and received January 4; and (4) a $12,000 December supplier invoice that was entered twice in December. What amount should Kirk report as accounts payable at December 31, Year 1?""",
    [("$608,000", "Removes the duplicate invoice but adds neither of the unrecorded December liabilities."),
     ("$629,000", "Adds the $21,000 of goods and removes the duplicate but omits the $9,000 of December utilities, a Year 1 liability."),
     ("$638,000", "Correct. $620,000 + $21,000 + $9,000 − $12,000. The FOB destination goods became Kirk's in January."),
     ("$663,000", "Also adds the $25,000 of goods shipped FOB destination. Title passed when they arrived in January, so they are a Year 2 purchase.")],
    "C",
    """Record the Year 1 liabilities found in the search: goods received in December ($21,000; title passed at shipment in any case) and December utilities ($9,000). Remove the duplicated $12,000 invoice. Goods shipped FOB destination belong to the seller until they arrive, so the $25,000 is a Year 2 purchase. Accounts payable = $620,000 + $21,000 + $9,000 − $12,000 = $638,000."""),

mcq("far-bonds-between-interest-dates-0001", A2, "Debt (Notes and bonds payable)", AP,
    ["ASC 835-30 (interest)", "ASC 470-10 (debt)"],
    """On April 1, Year 1, Lamb Co. issues $1,000,000 of 10-year, 6% bonds at 102 plus accrued interest. The bonds are dated January 1, Year 1, and pay interest each January 1 and July 1. How much cash does Lamb receive at issuance?""",
    [("$1,000,000", "Uses the face amount only. The bonds sell at 102 of face, plus accrued interest."),
     ("$1,005,000", "Subtracts the accrued interest instead of adding it. Buyers pay the interest accrued since the last interest date and receive a full six months' interest on July 1."),
     ("$1,020,000", "Includes the 2% premium but not the three months of accrued interest."),
     ("$1,035,000", "Correct. $1,000,000 × 102% + $1,000,000 × 6% × 3/12 accrued interest.")],
    "D",
    """Price = $1,000,000 × 1.02 = $1,020,000. Interest accrued from January 1 to April 1 = $1,000,000 × 6% × 3/12 = $15,000, which the buyers pay now and recover on July 1. Cash received = $1,035,000; Lamb records the $15,000 as interest payable (or a reduction of interest expense)."""),

mcq("far-inventory-gross-profit-method-0001", A2, "Inventory", AP,
    ["ASC 330-10 (inventory: estimating methods)"],
    """A fire on August 31 destroys most of Mosley Co.'s inventory. Records show beginning inventory of $200,000, purchases of $800,000, purchase returns of $20,000, freight-in of $10,000, sales of $1,100,000, and sales returns of $50,000 through that date. Mosley's gross profit rate has been 30% of net sales for several years. Goods costing $15,000 were salvaged undamaged. Using the gross profit method, what is Mosley's estimated inventory loss?""",
    [("$205,000", "Estimates cost of goods sold from gross sales ($1,100,000). Sales returns reduce the sales on which cost of goods sold is based."),
     ("$230,000", "Leaves the $10,000 of freight-in out of goods available for sale. Freight-in is part of inventory cost."),
     ("$240,000", "Correct. Goods available $990,000 − cost of goods sold $735,000 ($1,050,000 × 70%) − $15,000 salvaged."),
     ("$255,000", "Does not subtract the $15,000 of salvaged goods.")],
    "C",
    """Goods available = $200,000 + $800,000 − $20,000 + $10,000 = $990,000. Net sales = $1,100,000 − $50,000 = $1,050,000; estimated cost of goods sold = $1,050,000 × (1 − 30%) = $735,000. Estimated inventory at the date of the fire = $255,000; less $15,000 salvaged, the loss is $240,000."""),

mcq("far-property-dividend-0001", A2, "Equity", AP,
    ["ASC 845-10 (nonreciprocal transfers to owners)", "ASC 505-10 (dividends)"],
    """Noble Corp. declares a property dividend of a parcel of land to its shareholders. The land's carrying amount is $70,000, and its fair value on the declaration date is $100,000; the fair value does not change before distribution. What does Noble record for the dividend?""",
    [("$70,000 decrease in retained earnings; no gain", "Records the dividend at the land's carrying amount. A nonreciprocal transfer of a nonmonetary asset to owners is recorded at fair value."),
     ("$100,000 decrease in retained earnings; no gain (the difference goes to paid-in capital)", "The difference between fair value and carrying amount is a gain on disposal of the land, not paid-in capital."),
     ("$100,000 decrease in retained earnings; $30,000 gain", "Correct. The land is remeasured to its $100,000 fair value, recognizing a $30,000 gain, and the dividend is recorded at fair value."),
     ("$70,000 decrease in retained earnings; $30,000 gain", "Recognizes the gain but charges retained earnings only the land's carrying amount. The dividend is recorded at the fair value distributed.")],
    "C",
    """A property dividend is a nonreciprocal transfer to owners recorded at the fair value of the asset distributed. Noble remeasures the land to $100,000, recognizing a $30,000 gain in net income, and debits retained earnings for $100,000 (credit property dividends payable, later settled by distributing the land)."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("far-subsequent-events-0004", A3, "Subsequent events", AN,
    ["ASC 855-10 (recognized and nonrecognized subsequent events)", "ASC 250-10 (errors discovered before issuance)"],
    """Owen Co.'s December 31, Year 1, statements will be issued on March 10, Year 2. Between those dates: (1) on January 20, a fire destroyed the plant of a major customer, which filed for bankruptcy on January 30, making its $60,000 December 31 receivable uncollectible; the customer had been in good financial condition at year-end; (2) on January 15, Owen settled for $90,000 a lawsuit over a Year 1 accident, for which it had accrued $50,000; (3) on February 20, Owen found that its December 31 inventory count had double-counted goods costing $25,000; and (4) on March 1, Owen's board declared a cash dividend. Ignore income taxes. By how much should Owen reduce its Year 1 pretax income?""",
    [("$65,000", "Correct. $40,000 more for the lawsuit settlement plus the $25,000 inventory count error."),
     ("$115,000", "Charges the full $90,000 settlement instead of the $40,000 not yet accrued."),
     ("$125,000", "Also recognizes the $60,000 receivable loss. The customer's problems arose from a fire after year-end, so the loss is disclosed, not recognized."),
     ("$175,000", "Charges the full settlement and also recognizes the receivable loss.")],
    "A",
    """The settlement gives evidence about a Year 1 condition, so the accrual rises from $50,000 to $90,000: $40,000. The inventory double count is an error in the Year 1 statements found before issuance: $25,000. The customer's bankruptcy resulted from a fire after year-end, so it is a nonrecognized event (disclosed if material), as is the dividend. Reduction = $65,000."""),

mcq("far-accounting-errors-0004", A3, "Accounting changes and error corrections", AN,
    ["ASC 250-10 (correction of an error in previously issued statements)"],
    """On January 1, Year 1, Pollard Co. paid $36,000 for a three-year insurance policy and charged the full amount to Year 1 insurance expense; Year 1 statements were issued that way. Before closing its Year 2 books, Pollard discovers the error. It has recorded no insurance expense in Year 2. Pollard's tax rate is 25% for all effects, and it presents single-year statements. What are the effects of correcting the error?""",
    [("$18,000 increase to January 1, Year 2, retained earnings; $0 change to Year 2 net income", "Gets the prior-period adjustment right but records no Year 2 insurance expense. One year of the policy, $12,000, belongs in Year 2."),
     ("$18,000 increase to January 1, Year 2, retained earnings; $9,000 decrease to Year 2 net income", "Correct. Year 1 expense was overstated by $24,000 ($18,000 after tax); Year 2 needs $12,000 of expense ($9,000 after tax)."),
     ("$24,000 increase to January 1, Year 2, retained earnings; $12,000 decrease to Year 2 net income", "Leaves out the 25% tax effect."),
     ("$27,000 increase to January 1, Year 2, retained earnings; $0 change to Year 2 net income", "Treats all $36,000 as overstated Year 1 expense. One year of coverage, $12,000, was a proper Year 1 expense.")],
    "B",
    """Pollard should have expensed $12,000 a year. Year 1 expense was overstated by $24,000, so Year 1 net income was understated by $18,000 after tax, and January 1, Year 2, retained earnings is increased by $18,000 as a prior-period adjustment (with prepaid insurance of $24,000). Year 2 then records $12,000 of insurance expense, reducing Year 2 net income by $9,000 after tax."""),

mcq("far-contingencies-0005", A3, "Contingencies and commitments", AN,
    ["ASC 450-20 (loss contingencies, including unasserted claims)", "ASC 450-30 (gain contingencies)", "ASC 210-20 (offsetting; insurance recoveries presented gross)"],
    """Quenby Co. is preparing its December 31 statements, which have not been issued. Counsel's letter and other files show: (1) a customer sued Quenby in November over a defective product; counsel expects Quenby to lose and estimates damages of $200,000, and Quenby's insurer has confirmed in writing that it will reimburse $150,000 of any damages; (2) an employee was injured in a December accident at Quenby's plant; no claim has been filed yet, but counsel expects one and expects Quenby to pay about $30,000; and (3) Quenby is suing a competitor for patent infringement and counsel expects an award of about $80,000. What total liabilities should Quenby report for these matters?""",
    [("$50,000", "Nets the insurance recovery against the lawsuit liability and omits the unasserted claim."),
     ("$80,000", "Nets the $150,000 insurance recovery against the $200,000 liability. The liability and the recovery receivable are reported separately."),
     ("$200,000", "Omits the $30,000 unasserted claim. An unasserted claim is accrued when assertion is probable and a loss is probable and estimable."),
     ("$230,000", "Correct. The $200,000 lawsuit liability, reported gross, plus the $30,000 expected claim; the insurance recovery is a separate receivable.")],
    "D",
    """(1) The loss is probable and estimable, so Quenby accrues $200,000; the confirmed insurance reimbursement is recognized as a separate $150,000 receivable, not netted against the liability. (2) An unasserted claim is accrued when it is probable a claim will be asserted and probable that the outcome will be unfavorable: $30,000. (3) The expected award is a gain contingency, not recognized. Liabilities = $230,000."""),

mcq("far-revenue-contract-modification-0001", A3, "Revenue recognition", AP,
    ["ASC 606-10 (contract modifications)"],
    """Reed Co. contracts to deliver 120 identical standard units to a customer over six months for $100 per unit; the customer can use each unit on its own as it is delivered. After 50 units are delivered, the parties modify the contract to add 30 more units at $80 each; Reed's standalone selling price for the units is $95 at that time, and the discount does not reflect any cost savings or other reason tied to the added units. What revenue per unit should Reed recognize for each of the 100 units delivered after the modification?""",
    [("$80", "Uses the price of the added units for all remaining units."),
     ("$94", "Correct. The modification is accounted for prospectively: (70 × $100 + 30 × $80) ÷ 100 units."),
     ("$96", "Applies a cumulative catch-up by blending all 150 units, including the 50 already delivered. When the remaining goods are distinct, the modification is prospective."),
     ("$100", "Keeps $100 for the original units and treats the added units as a separate contract. That applies only when the added units are priced at their standalone selling price.")],
    "B",
    """The added units are distinct but not priced at standalone selling price, so the modification is not a separate contract. Because the remaining units are distinct from those already delivered, Reed treats it as terminating the old contract and creating a new one: the remaining consideration (70 × $100 + 30 × $80 = $9,400) is allocated to the 100 remaining units, $94 each."""),

mcq("far-revenue-material-right-0001", A3, "Revenue recognition", AP,
    ["ASC 606-10 (customer options for additional goods or services: material rights)"],
    """Stark Co. sells a product for $1,000, its standalone selling price, and gives the customer a voucher for 40% off any future purchase of up to $500 within a year. Stark offers no similar discount to other customers. It expects 80% of vouchers to be redeemed, on purchases averaging $500. How much revenue should Stark recognize when it delivers the product?""",
    [("$800", "Subtracts the full $200 voucher value (40% × $500) without allocating the price or adjusting for expected redemptions."),
     ("$840", "Subtracts the voucher's $160 standalone selling price directly. The $1,000 price is allocated between the product and the voucher by relative standalone selling price."),
     ("$862", "Correct. Voucher standalone selling price = $500 × 40% × 80% = $160; product revenue = $1,000 × $1,000 ÷ $1,160."),
     ("$1,000", "Ignores the voucher. A discount not available to other customers is a material right, a separate performance obligation.")],
    "C",
    """The voucher gives a material right because the discount is not offered to other customers, so it is a separate performance obligation. Its standalone selling price reflects the discount and the likelihood of redemption: $500 × 40% × 80% = $160. Allocating the $1,000 price: product $1,000 × 1,000 ÷ 1,160 = $862; voucher $138, recognized when redeemed or when it expires."""),

mcq("far-lessee-variable-payments-0001", A3, "Lessee accounting", RU,
    ["ASC 842-10 (lease payments: variable payments)"],
    """Which of the following variable lease payments is included in a lessee's lease liability at commencement?""",
    [("Rent that is reset each year to the current Consumer Price Index", "Correct. Payments that depend on an index are lease payments, measured using the index at commencement; later changes are expensed as incurred."),
     ("Rent equal to a percentage of the lessee's sales in the leased store", "Performance-based variable payments are excluded from the liability and expensed when incurred."),
     ("A bonus payable to the lessor if the store's annual sales exceed a target", "A payment contingent on the lessee's performance is excluded from the liability until incurred."),
     ("Rent based on how many hours the lessee operates the leased equipment", "Usage-based variable payments are excluded from the liability and expensed when incurred.")],
    "A",
    """Lease payments include variable payments that depend on an index or a rate, initially measured using the index or rate at commencement. Later changes in the index are recognized in profit or loss when incurred. Variable payments based on performance or usage are not lease payments."""),

mcq("far-income-taxes-rate-change-0001", A3, "Accounting for income taxes", AP,
    ["ASC 740-10 (measurement at enacted rates; effect of a change in tax rates)"],
    """At December 31, Year 1, Tyne Co. has a deferred tax liability of $42,000 on $200,000 of taxable temporary differences, measured at the 21% enacted rate. On November 1, Year 2, legislation is enacted raising Tyne's tax rate to 25% for Year 3 and later years. At December 31, Year 2, Tyne's taxable temporary differences total $260,000, all reversing in Year 3 or later. What deferred income tax expense should Tyne recognize for Year 2?""",
    [("$12,600", "Measures the ending liability at the old 21% rate. Deferred taxes are measured at the enacted rate for the years the differences reverse."),
     ("$15,000", "Applies the new rate only to the $60,000 of new differences and does not remeasure the beginning liability for the rate change."),
     ("$23,000", "Correct. Ending liability $260,000 × 25% = $65,000, less the $42,000 beginning balance."),
     ("$65,000", "Reports the ending deferred tax liability as the year's expense, ignoring the $42,000 already recorded.")],
    "C",
    """Deferred tax liabilities are measured at the enacted rate expected to apply when the differences reverse, and the effect of a rate change is recognized in income from continuing operations in the period of enactment. Ending liability = $260,000 × 25% = $65,000. Deferred tax expense = $65,000 − $42,000 = $23,000 (including $8,000 from remeasuring the beginning differences)."""),

mcq("far-nfp-gifts-in-kind-0001", A3, "Revenue recognition", AP,
    ["ASC 958-605 (contributions of nonfinancial assets; collections)", "ASU 2020-07 (presentation and disclosure of contributed nonfinancial assets)"],
    """During Year 1, Upton Food Bank, a not-for-profit entity, receives: donated food with a fair value of $40,000 to distribute; free use of a warehouse for the year, which would otherwise rent for $24,000; publicly traded shares worth $15,000; and a painting worth $50,000 that it adds to a collection held for public exhibition, which it protects and preserves, and whose sale proceeds would go only to new collection items. Upton's policy is not to capitalize collections. What contribution revenue should Upton recognize for Year 1?""",
    [("$55,000", "Omits the donated use of the warehouse. Contributed use of facilities is recognized at fair value as revenue and expense."),
     ("$105,000", "Recognizes the painting but omits the donated use of the warehouse. The collection item is not recognized under Upton's policy, and contributed use of facilities is."),
     ("$79,000", "Correct. $40,000 of food + $24,000 of donated facilities + $15,000 of shares."),
     ("$129,000", "Also recognizes the painting. An entity that does not capitalize a qualifying collection does not recognize contributed collection items as revenue.")],
    "C",
    """Contributions of food, use of facilities and securities are recognized at fair value: $40,000 + $24,000 + $15,000 = $79,000 (contributed nonfinancial assets are presented separately under ASU 2020-07). Works of art added to a collection that meets the collection criteria need not be recognized, and under Upton's policy they are not."""),
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
