"""FAR batch 02 — 25 items written from scratch to fill the blueprint gaps left by batch 01 (see
docs/reviews/far-batch-02.md). Scope and skill tags follow the AICPA CPA Exam Blueprints effective January 2026:
Analysis items use the blueprint's own Analysis tasks (detect and correct discrepancies in a draft, reconcile a
subledger or bank statement, compare notes with the statements, derive the impact of a change or subsequent event).

Run: python3 scripts/batches/far-batch-02.py  (writes content/far/*.yaml; leaves batch 01 files alone)
Every numeric answer and distractor below was computed in code.
"""
import os
from common import mcq as _mcq, finalize, audit, write_items, RU, AP, AN

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 02. Written from scratch; answers solved and every number and distractor computed in code."


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


ITEMS = [
# ── Area I ──────────────────────────────────────────────────────────────
mcq("far-balance-sheet-0001", A1, "Balance sheet", AN,
    ["ASC 210-10 (balance sheet classification)", "ASC 470-10 (classification of short-term obligations expected to be refinanced; current maturities)", "ASC 505-20 (dividends: declaration creates the liability)"],
    """Corbin Co.'s December 31, Year 1, financial statements will be issued on March 1, Year 2. Its draft classified balance sheet reports total current liabilities of $445,000: accounts payable $180,000, accrued wages $40,000, a note payable due June 30, Year 2, of $200,000, and dividends payable of $25,000. Supporting documents show: (1) on February 10, Year 2, Corbin signed an agreement with a bank to refinance the $200,000 note with a five-year loan; the agreement cannot be cancelled by the bank before Year 5, the bank is financially able to honor it, and Corbin is in compliance with its terms; (2) the board declared the $25,000 cash dividend on January 20, Year 2; (3) Corbin's $500,000 of serial bonds, all shown as noncurrent, are repaid in ten annual installments of $50,000 beginning January 15, Year 2; and (4) Corbin netted a $35,000 overdraft at Bank B, where it has no other accounts, against its cash at Bank A. After correcting the draft, what are Corbin's total current liabilities?""",
    [("$255,000", "Reclassifies the note and removes the dividend but leaves the $50,000 bond installment due January 15, Year 2, in noncurrent liabilities."),
     ("$305,000", "Correct. $180,000 + $40,000 + $50,000 current bond installment + $35,000 overdraft. The refinanced note is noncurrent and the dividend is not yet a liability."),
     ("$330,000", "Keeps the $25,000 dividend. A dividend declared after the balance sheet date is not a liability at year-end."),
     ("$270,000", "Leaves the $35,000 overdraft netted against cash. An overdraft at a bank where Corbin has no other accounts cannot be offset; it is a current liability.")],
    "B",
    """Four corrections. (1) A short-term obligation is excluded from current liabilities if, before the statements are issued, the entity enters into a financing agreement that permits long-term refinancing, is noncancelable for more than a year, is with a capable lender, and is not in violation. The $200,000 note meets these conditions, so it moves to noncurrent. (2) A dividend becomes a liability when declared; the January 20 declaration is not a Year 1 liability. (3) The $50,000 bond installment due within a year is current. (4) An overdraft at a bank where the entity has no other accounts cannot be offset against cash elsewhere; it is a current liability. Current liabilities = $180,000 + $40,000 + $50,000 + $35,000 = $305,000."""),

mcq("far-income-statement-0001", A1, "Income statement", AN,
    ["ASC 205-20 (discontinued operations)", "ASC 225-20 (unusual or infrequently occurring items; ASU 2015-01 eliminated extraordinary items)", "ASC 830-20 (foreign currency transactions)"],
    """Oberon Corp.'s draft Year 1 multi-step income statement reports income from continuing operations before income taxes of $900,000. Reviewing the supporting schedules, you find: (1) continuing operations include a $150,000 pretax operating loss of Oberon's South American division, which is Oberon's only operation on that continent and produced 30% of consolidated revenue; in November the board approved a plan to sell the division, began actively marketing it at a reasonable price, and expects a sale within a year; (2) a $40,000 loss from remeasuring a yen-denominated account payable at the year-end exchange rate is reported in other comprehensive income; and (3) a $70,000 hurricane loss, which Oberon considers both unusual and infrequent, is reported below income from continuing operations as an extraordinary item. What is Oberon's corrected income from continuing operations before income taxes?""",
    [("$790,000", "Corrects the exchange loss and the hurricane loss but leaves the division's loss in continuing operations. Selling the company's only operation on a continent, which produced 30% of revenue, is a strategic shift with a major effect, so it is reported in discontinued operations."),
     ("$940,000", "Correct. $900,000 + $150,000 division loss moved to discontinued operations − $40,000 exchange loss − $70,000 hurricane loss."),
     ("$980,000", "Leaves the $40,000 exchange loss in OCI. A remeasurement loss on a foreign-currency payable is a transaction loss reported in income."),
     ("$640,000", "Subtracts the division's $150,000 loss again instead of removing it from continuing operations. Moving a loss to discontinued operations raises income from continuing operations.")],
    "B",
    """(1) The division is a component that meets the held-for-sale criteria (approved plan, actively marketed at a reasonable price, sale expected within a year) and its disposal is a strategic shift with a major effect (exiting a major geographic area that produced 30% of revenue), so its results move to discontinued operations: add back $150,000. (2) Remeasuring a foreign-currency payable produces a transaction loss that belongs in income: subtract $40,000. (3) Since ASU 2015-01 there is no extraordinary-item classification; the hurricane loss is reported within continuing operations: subtract $70,000. Corrected: $900,000 + $150,000 − $40,000 − $70,000 = $940,000."""),

mcq("far-changes-in-equity-0001", A1, "Statement of changes in equity", AN,
    ["ASC 505-20 (stock dividends)", "ASC 505-30 (treasury stock)", "ASC 250-10 (correction of an error in previously issued statements)"],
    """Pruitt Inc.'s draft Year 2 statement of changes in equity reports ending retained earnings of $1,280,000, computed as beginning retained earnings of $1,000,000 (as previously reported), plus net income of $420,000, less cash dividends of $60,000, less a $10,000 stock dividend, less $70,000 for treasury stock. Supporting documents show: (1) the stock dividend was 10,000 shares of $1 par common stock (10% of the shares outstanding), distributed when the market price was $15 per share; (2) Pruitt paid $70,000 to reacquire its own shares and holds them in treasury under the cost method; and (3) in Year 2 Pruitt discovered that it had omitted $40,000 of depreciation in Year 1, an error with an after-tax effect of $30,000. Year 2 net income is correct. What is Pruitt's corrected ending retained earnings for Year 2?""",
    [("$1,110,000", "Fixes the stock dividend and the prior-period error but still charges the treasury stock purchase to retained earnings. Under the cost method, treasury stock is a separate deduction from total equity."),
     ("$1,180,000", "Correct. $1,000,000 − $30,000 prior-period adjustment + $420,000 − $60,000 − $150,000 stock dividend at market value."),
     ("$1,210,000", "Omits the prior-period adjustment. The Year 1 error is corrected by restating beginning retained earnings, net of tax."),
     ("$1,320,000", "Records the stock dividend at par. A distribution of less than 20–25% of the shares outstanding is recorded at the shares' market value.")],
    "B",
    """(1) A stock dividend of 10% is small, so retained earnings is charged at market value: 10,000 × $15 = $150,000, not the $10,000 par. (2) Treasury stock under the cost method is shown as a deduction from total equity; buying it does not reduce retained earnings. (3) The omitted Year 1 depreciation is a prior-period error, corrected by reducing beginning retained earnings by its after-tax effect of $30,000. Corrected ending retained earnings = $1,000,000 − $30,000 + $420,000 − $60,000 − $150,000 = $1,180,000."""),

mcq("far-notes-0001", A1, "Notes to financial statements", AN,
    ["ASC 470-10 (classification of debt callable because of a covenant violation)", "ASC 855-10 (nonrecognized subsequent events)", "ASC 330-10 (inventory)", "ASC 842-20 (lessee presentation)"],
    """Marlin Corp.'s draft December 31, Year 1, balance sheet reports inventory of $840,000 and classifies all of its long-term debt, including a $300,000 term loan due in Year 6, as noncurrent. The statements will be issued on March 5, Year 2. You compare four draft note excerpts with the statements and supporting documents. Inventory note: inventories of $840,000 are stated at the lower of FIFO cost and net realizable value, after a $12,000 write-down charged to cost of sales. Debt note: at December 31, Marlin did not meet the current-ratio covenant in its term loan agreement, which makes the loan payable on demand; on January 20 the lender waived that right until September 30, Year 2. Subsequent events note: on February 5 a fire destroyed uninsured inventory costing $90,000; the loss will be recognized in Year 2. Lease note: operating lease cost of $48,000 is included in selling expenses, and the right-of-use asset and lease liability are presented separately in the balance sheet. Which note reveals that the draft financial statements must be corrected?""",
    [("The debt note", "Correct. A covenant violation that makes the loan callable at year-end requires current classification unless the lender waives the right for more than one year from the balance sheet date. The waiver runs only to September 30, Year 2, so the $300,000 is current."),
     ("The inventory note", "Consistent. The write-down to net realizable value is charged to cost of sales and the carrying amount matches the balance sheet."),
     ("The subsequent events note", "Consistent. The fire is a condition that arose after year-end: it is disclosed, not recognized in Year 1."),
     ("The lease note", "Consistent. A lessee presents operating lease right-of-use assets and liabilities separately, and reports a single lease cost in income from operations.")],
    "A",
    """Long-term debt that is callable by the creditor at the balance sheet date because of a covenant violation is classified as current unless the creditor waives or loses the right to demand repayment for more than one year from the balance sheet date (or the violation will probably be cured within a grace period). Marlin's waiver lasts only nine months, so the $300,000 term loan must be reclassified to current liabilities, and the note is inconsistent with the draft balance sheet. The other three notes agree with the statements and with GAAP."""),

mcq("far-sec-forms-0001", A1, "Public Company Reporting Topics", RU,
    ["SEC Form 10-K (Part II, Items 7, 7A and 8)", "SEC Regulation S-K Item 305 (quantitative and qualitative disclosures about market risk)"],
    """A U.S. registrant is drafting its annual report on Form 10-K. Where in the Form 10-K does it present its quantitative and qualitative disclosures about market risk, such as its exposure to changes in interest rates and foreign-currency exchange rates?""",
    [("Part II, Item 7A", "Correct. Item 7A is Quantitative and Qualitative Disclosures About Market Risk."),
     ("Part II, Item 7", "Item 7 is Management's Discussion and Analysis of Financial Condition and Results of Operations."),
     ("Part II, Item 8", "Item 8 is Financial Statements and Supplementary Data."),
     ("Part I, Item 1A", "Item 1A is Risk Factors, a narrative of material risks, not the market-risk disclosures.")],
    "A",
    """Form 10-K Part II contains Item 7 (MD&A), Item 7A (Quantitative and Qualitative Disclosures About Market Risk), and Item 8 (Financial Statements and Supplementary Data). Market-risk sensitivity to interest rates, exchange rates and commodity prices belongs in Item 7A."""),

mcq("far-special-purpose-frameworks-0001", A1, "Special Purpose Frameworks", AP,
    ["AU-C 800 (special purpose frameworks)", "ASC 606-10 (revenue recognized as performance obligations are satisfied)"],
    """Dalton Consulting keeps its records on the cash basis. In Year 2 it received $480,000 in cash from clients. Client accounts receivable were $60,000 on January 1 and $85,000 on December 31, and during the year Dalton wrote off $5,000 of client receivables as uncollectible. Client advances for work not yet performed were $20,000 on January 1 and $12,000 on December 31. What is Dalton's Year 2 consulting revenue on the accrual basis?""",
    [("$468,000", "Subtracts the $25,000 increase in receivables. Revenue earned but not yet collected raises accrual revenue above cash received."),
     ("$502,000", "Subtracts the $8,000 decrease in client advances. Advances earned during the year exceed new advances received, so accrual revenue is higher than cash."),
     ("$513,000", "Omits the $5,000 written off. Those receivables were billed as revenue even though they were never collected."),
     ("$518,000", "Correct. $480,000 + $25,000 increase in receivables + $5,000 written off + $8,000 decrease in client advances.")],
    "D",
    """Revenue = cash received + ending receivables − beginning receivables + receivables written off + beginning advances − ending advances. $480,000 + ($85,000 − $60,000) + $5,000 + ($20,000 − $12,000) = $518,000. The written-off receivables were revenue that never reached cash, and the net decrease in advances is revenue earned from cash collected in an earlier year."""),

mcq("far-ratios-0001", A1, "Financial Statement Ratios and Performance Metrics", AP,
    ["Financial statement analysis: liquidity ratios (quick or acid-test ratio)"],
    """At year-end, Garner Co. reports the following current assets: cash $60,000; Treasury bills purchased with a two-month maturity $40,000; trading debt securities $50,000; accounts receivable, net $150,000; inventory $200,000; and prepaid insurance $20,000. Current liabilities total $250,000. What is Garner's quick ratio?""",
    [("2.00", "Includes inventory. The quick ratio excludes inventory and prepaid expenses."),
     ("1.20", "Correct. ($60,000 + $40,000 + $50,000 + $150,000) ÷ $250,000."),
     ("1.28", "Includes prepaid insurance. Prepaid expenses will not convert to cash, so they are excluded along with inventory."),
     ("2.08", "Computes the current ratio. The quick ratio excludes inventory and prepaid expenses.")],
    "B",
    """Quick assets are cash and cash equivalents, marketable securities, and net receivables: $60,000 + $40,000 + $50,000 + $150,000 = $300,000. Quick ratio = $300,000 ÷ $250,000 = 1.20. Inventory and prepaid expenses are excluded."""),

mcq("far-nfp-cash-flows-0001", A1, "Statement of cash flows (Not-for-Profit)", AP,
    ["ASC 230-10 (contributions restricted for long-term purposes are financing inflows)", "ASC 958-230 (not-for-profit statement of cash flows)"],
    """During Year 1, Hillcrest Museum, a not-for-profit entity, received these amounts in cash: $400,000 from a donor who restricted the gift to constructing a new wing, $250,000 from a donor who required it to be invested in perpetuity with the income used for operations, and $180,000 of contributions without donor restrictions. Hillcrest also paid $300,000 of construction costs for the new wing and repaid $50,000 of principal on its mortgage. What is Hillcrest's net cash provided by financing activities for Year 1?""",
    [("$200,000", "Reports the $400,000 building gift as an operating inflow. Contributions restricted to acquiring long-lived assets are financing inflows."),
     ("$350,000", "Leaves the $250,000 endowment gift out of financing. Contributions restricted for permanent endowment are financing inflows."),
     ("$600,000", "Correct. $400,000 building gift + $250,000 endowment gift − $50,000 mortgage principal."),
     ("$780,000", "Also counts the $180,000 of unrestricted contributions. Contributions without donor restrictions are operating inflows.")],
    "C",
    """For a not-for-profit entity, cash contributions that donors restrict to long-term purposes (acquiring, constructing or improving long-lived assets, or establishing or increasing an endowment) are financing inflows. Financing: $400,000 + $250,000 − $50,000 mortgage principal = $600,000. The unrestricted contributions are operating, and the construction payments are investing."""),

mcq("far-consolidated-statements-0002", A1, "Consolidated financial statements", AN,
    ["ASC 810-10 (consolidation procedures: intercompany profit elimination)"],
    """Holt Corp. owns 100% of Vale Inc. During Year 1, Holt sold inventory that cost it $150,000 to Vale for $200,000. By December 31, Vale had resold 70% of that inventory to outside customers and still held the rest. Holt reported sales of $1,000,000 and cost of goods sold of $600,000; Vale reported sales of $500,000 and cost of goods sold of $300,000. Holt's draft consolidated income statement for Year 1 reports sales of $1,500,000 and cost of goods sold of $900,000. After any corrections needed, what is consolidated gross profit?""",
    [("$400,000", "Eliminates the $200,000 of intercompany sales without eliminating the matching intercompany purchases from cost of goods sold."),
     ("$550,000", "Eliminates Holt's entire $50,000 profit on the intercompany sale. Only the profit in inventory Vale still holds (30%) is unrealized."),
     ("$585,000", "Correct. The draft's $600,000 less $15,000 of unrealized profit in Vale's ending inventory (30% × $50,000)."),
     ("$600,000", "Accepts the draft. Eliminating intercompany sales and purchases leaves gross profit unchanged, but the profit in Vale's ending inventory must still be removed.")],
    "C",
    """The draft simply adds the two companies' amounts. Eliminate the $200,000 intercompany sale from both sales and cost of goods sold (no effect on gross profit), then remove the unrealized profit in Vale's ending inventory: Holt's markup is $50,000 on $200,000 of goods, and 30% remains unsold, so $15,000 is deferred by increasing cost of goods sold. Consolidated sales $1,300,000 − cost of goods sold $715,000 = $585,000."""),

# ── Area II ─────────────────────────────────────────────────────────────
mcq("far-cash-bank-reconciliation-0001", A2, "Cash and cash equivalents", AN,
    ["ASC 305-10 (cash)", "Bank reconciliation practice"],
    """Ridley Co.'s December 31 bank statement shows a balance of $48,200, and its general ledger cash account shows $45,900. The controller finds: deposits in transit of $6,400; outstanding checks of $9,300; a $60 bank service charge not yet recorded; a customer's $1,200 check returned with the statement marked NSF; check #412, written to a supplier for $540 and cleared by the bank at $540, recorded in the ledger as $450; and a note receivable of $750, including interest, that the bank collected for Ridley and credited to its account. What is Ridley's correct cash balance at December 31?""",
    [("$44,550", "Omits the $750 note the bank collected, which Ridley has not yet recorded."),
     ("$45,300", "Correct. Bank: $48,200 + $6,400 − $9,300. Books: $45,900 − $60 − $1,200 − $90 + $750. Both equal $45,300."),
     ("$45,480", "Corrects check #412 in the wrong direction. The check was $540 but recorded as $450, so the ledger must be reduced by $90."),
     ("$47,700", "Adds back the NSF check. A returned customer check reduces cash and reinstates the receivable.")],
    "B",
    """Reconcile both sides to the correct balance. Bank side: $48,200 + $6,400 deposits in transit − $9,300 outstanding checks = $45,300. Book side: $45,900 − $60 service charge − $1,200 NSF check − $90 understatement of check #412 + $750 note collected = $45,300. The book-side items all require general ledger adjustments; the bank-side items do not."""),

mcq("far-cash-equivalents-0001", A2, "Cash and cash equivalents", AP,
    ["ASC 305-10 (cash equivalents: original maturity of three months or less)", "ASC 210-10 (restricted cash; offsetting)"],
    """At December 31, Year 1, Fulton Corp. has: checking account $120,000; savings account $80,000; petty cash $1,000; a Treasury bill bought December 1, Year 1, that matures February 28, Year 2, $50,000; a Treasury bill bought June 1, Year 1, that matures February 28, Year 2, $30,000; a six-month certificate of deposit maturing March 31, Year 2, $40,000; $25,000 held by a trustee in a bond sinking fund; and an $8,000 overdraft in an account at a different bank. What amount should Fulton report as cash and cash equivalents?""",
    [("$291,000", "Includes the six-month certificate of deposit. Its original maturity is more than three months, so it is a short-term investment, not a cash equivalent."),
     ("$251,000", "Correct. $120,000 + $80,000 + $1,000 + the $50,000 Treasury bill bought with a three-month maturity. The overdraft at another bank is a liability and is not netted."),
     ("$276,000", "Includes the $25,000 sinking fund. Cash restricted for debt retirement is not available for current operations and is reported separately."),
     ("$281,000", "Includes the Treasury bill bought June 1. Cash equivalents must have an original maturity to the holder of three months or less; this bill had about nine.")],
    "B",
    """Cash equivalents are short-term, highly liquid investments with original maturities to the holder of three months or less. The December 1 Treasury bill qualifies; the June 1 bill (about nine months when bought) and the six-month CD do not, even though little time remains. The sinking fund is restricted and reported separately, and the overdraft at another bank is a current liability. Cash and cash equivalents = $120,000 + $80,000 + $1,000 + $50,000 = $251,000."""),

mcq("far-receivables-factoring-0001", A2, "Trade receivables", AP,
    ["ASC 860-10 (transfers of financial assets: sale accounting)", "ASC 860-20 (sales of financial assets)"],
    """Kemp Co. transfers $500,000 of trade receivables to a factor without recourse. The receivables are legally isolated from Kemp, the factor may sell or pledge them, and Kemp has no agreement or right to repurchase them. The factor charges a fee of 4% of the receivables transferred and holds back 10% of the receivables to cover sales returns and allowances, to be paid to Kemp after the accounts are collected. Kemp expects no returns or allowances. How much cash does Kemp receive at the transfer, and what loss does it recognize?""",
    [("$430,000 cash; $20,000 loss", "Correct. $500,000 − $20,000 fee − $50,000 holdback; the fee is the loss, and the holdback is a receivable from the factor."),
     ("$430,000 cash; $70,000 loss", "Treats the $50,000 holdback as part of the loss. Kemp expects to collect it, so it is a receivable from the factor."),
     ("$432,000 cash; $18,000 loss", "Computes the fee on the $450,000 advanced. The fee is 4% of the $500,000 of receivables transferred."),
     ("$480,000 cash; $20,000 loss", "Treats the holdback as paid at the transfer. The factor keeps it until the accounts are collected.")],
    "A",
    """The transfer meets the conditions for sale accounting: the receivables are isolated from Kemp, the factor can pledge or sell them, and Kemp keeps no effective control. Kemp derecognizes the receivables. Cash = $500,000 − 4% fee ($20,000) − 10% holdback ($50,000) = $430,000. The holdback is recorded as a receivable from the factor, and the $20,000 fee is the loss on sale."""),

mcq("far-inventory-reconciliation-0001", A2, "Inventory", AN,
    ["ASC 330-10 (inventory)", "ASC 330-10 (goods in transit and goods held on consignment)"],
    """At December 31, Lassen Co.'s perpetual inventory subledger totals $612,000, but its general ledger inventory account shows $562,000. Investigating, the controller finds: (1) goods costing $18,000 that a supplier shipped FOB shipping point on December 28 arrived January 3 and are recorded in neither record; (2) the subledger includes $22,000 of goods Lassen holds on consignment for Mayer Co.; (3) a $28,000 purchase received December 20 is in the subledger, but the supplier's invoice was never posted to the general ledger; and (4) goods costing $12,000 shipped to a customer FOB destination on December 31, which arrived January 4, were removed from both records when shipped and the sale was recorded. By how much must Lassen increase its general ledger inventory balance?""",
    [("$8,000", "Computes the adjustment the subledger needs ($612,000 to $620,000), not the general ledger."),
     ("$30,000", "Omits the $28,000 purchase that is in the subledger but was never posted to the general ledger."),
     ("$58,000", "Correct. Correct inventory is $620,000; $620,000 − $562,000 = $58,000."),
     ("$80,000", "Treats the $22,000 of consigned goods as Lassen's. Goods held on consignment belong to the consignor.")],
    "C",
    """Correct inventory = subledger $612,000 + $18,000 in transit (title passed at shipment) − $22,000 consigned goods (owned by Mayer) + $12,000 shipped FOB destination (title had not passed) = $620,000. The general ledger is missing the in-transit goods, the unposted $28,000 purchase, and the FOB-destination goods: $562,000 + $18,000 + $28,000 + $12,000 = $620,000. The general ledger must be increased by $58,000 (and the premature sale reversed)."""),

mcq("far-investments-htm-0001", A2, "Investments (Financial assets at amortized cost)", AP,
    ["ASC 320-10 (held-to-maturity debt securities)", "ASC 310-20 (interest method)"],
    """On January 1, Year 1, Nolan Corp. pays $479,499 for $500,000 face amount of five-year, 6% bonds that pay interest each December 31, a price that yields 7%. Nolan has the positive intent and ability to hold the bonds to maturity and expects no credit losses on them. It uses the effective interest method and rounds to the nearest dollar at each step. At December 31, Year 2, the bonds' fair value is $490,000. At what amount should Nolan report the investment at December 31, Year 2?""",
    [("$489,499", "Computes interest income at 7% of face ($35,000), amortizing $5,000 a year. Effective interest applies the yield to the carrying amount."),
     ("$486,878", "Correct. Year 1: $479,499 + ($33,565 − $30,000) = $483,064. Year 2: $483,064 + ($33,814 − $30,000) = $486,878."),
     ("$487,699", "Amortizes the discount straight-line ($4,100 a year). The effective interest method is required unless the difference is immaterial."),
     ("$490,000", "Reports fair value. Held-to-maturity securities are carried at amortized cost.")],
    "B",
    """Held-to-maturity debt securities are carried at amortized cost. Year 1 interest income = $479,499 × 7% = $33,565; cash interest $30,000; discount amortized $3,565; carrying amount $483,064. Year 2 interest income = $483,064 × 7% = $33,814; amortization $3,814; carrying amount $486,878. Fair value is disclosed, not recognized."""),

mcq("far-intangibles-patent-0001", A2, "Intangible assets", AP,
    ["ASC 350-30 (finite-lived intangible assets: amortization over useful life)", "ASC 250-10 (change in accounting estimate)"],
    """On January 1, Year 1, Ivers Co. buys a patent for $360,000. The patent has 15 years of legal life remaining, and Ivers expects it to provide benefits for 12 years. Ivers amortizes it straight-line with no residual value. On January 1, Year 4, a competitor's new technology leads Ivers to conclude that the patent will provide benefits for only 5 more years; its future cash flows still exceed its carrying amount. What patent amortization expense should Ivers recognize in Year 4?""",
    [("$30,000", "Keeps the original 12-year life. A revised estimate of useful life is applied from Year 4 onward."),
     ("$45,000", "Spreads the original cost over the revised total life of 8 years. A change in estimate is prospective: the remaining carrying amount is spread over the remaining life."),
     ("$54,000", "Correct. Carrying amount $360,000 − 3 × $30,000 = $270,000, spread over the remaining 5 years."),
     ("$22,500", "Spreads the $270,000 carrying amount over the 12 years of legal life remaining. Amortization uses the shorter of legal and useful life.")],
    "C",
    """A finite-lived intangible is amortized over the shorter of its legal and useful lives: 12 years, $30,000 a year. After three years its carrying amount is $270,000. The revised life is a change in accounting estimate, applied prospectively: $270,000 ÷ 5 = $54,000 a year from Year 4. The asset is recoverable, so there is no impairment."""),

mcq("far-payables-reconciliation-0001", A2, "Payables and accrued liabilities", AN,
    ["ASC 405-10 (liabilities)", "ASC 330-10 (inventory: goods in transit)"],
    """At December 31, Loring Co.'s accounts payable subledger totals $412,000, and its general ledger accounts payable control account shows $392,000. Investigating, the controller finds: (1) a $14,000 supplier invoice was posted correctly to the supplier's subledger account, but the general ledger entry credited accrued liabilities instead of accounts payable; (2) goods costing $9,000 shipped by a supplier FOB shipping point on December 29 and received January 3 have not been invoiced or recorded in either record; and (3) a $6,000 payment to a supplier on December 30 was recorded in the general ledger but not in the supplier's subledger account. What amount should Loring report as accounts payable at December 31?""",
    [("$406,000", "Omits the $9,000 of goods shipped FOB shipping point. Title passed at shipment, so Loring owes the supplier at year-end."),
     ("$412,000", "Accepts the subledger. The subledger still includes the $6,000 already paid and omits the $9,000 of goods in transit."),
     ("$415,000", "Correct. General ledger $392,000 + $14,000 misposted invoice + $9,000 goods in transit; subledger $412,000 − $6,000 payment + $9,000 agrees."),
     ("$392,000", "Accepts the general ledger. It omits the $14,000 invoice credited to accrued liabilities and the $9,000 of goods in transit.")],
    "C",
    """Reconcile both records to the correct balance. General ledger: $392,000 + $14,000 invoice credited to the wrong account + $9,000 goods in transit (title passed at shipment) = $415,000. Subledger: $412,000 − $6,000 payment not yet posted + $9,000 goods in transit = $415,000. Adjustments: reclassify $14,000 from accrued liabilities to accounts payable, record the $9,000 purchase, and post the payment to the subledger."""),

mcq("far-debt-covenant-0001", A2, "Debt (Debt covenant compliance)", AP,
    ["Debt agreement covenant calculations", "ASC 460-10 (warranty obligations)", "ASC 505-20 (dividends payable on declaration)"],
    """Kade Inc.'s loan agreement requires its ratio of total liabilities to total stockholders' equity to be no more than 1.60 at each year-end. Before year-end adjustments, Kade's December 31 balance sheet shows total liabilities of $1,800,000 and total stockholders' equity of $1,250,000. Two adjustments have not yet been recorded: an accrual for $60,000 of warranty costs on Year 1 sales, and a $50,000 cash dividend the board declared on December 20, payable January 15. Ignore income taxes. What is Kade's debt-to-equity ratio for the covenant test?""",
    [("1.44", "Uses the balances before the year-end adjustments."),
     ("1.53", "Adds the $110,000 to liabilities but does not reduce stockholders' equity for the warranty expense and the dividend."),
     ("1.56", "Records the warranty accrual but not the dividend declared December 20, which is a liability at year-end."),
     ("1.68", "Correct. ($1,800,000 + $110,000) ÷ ($1,250,000 − $110,000) = 1.68, which violates the 1.60 limit.")],
    "D",
    """Both adjustments increase liabilities and decrease equity. The warranty accrual is an expense (reducing retained earnings) and a liability; the declared dividend reduces retained earnings and creates dividends payable. Liabilities = $1,800,000 + $60,000 + $50,000 = $1,910,000. Equity = $1,250,000 − $110,000 = $1,140,000. Ratio = $1,910,000 ÷ $1,140,000 = 1.68, above the 1.60 covenant."""),

mcq("far-treasury-stock-0001", A2, "Equity", AP,
    ["ASC 505-30 (treasury stock: cost method)"],
    """At the start of the year, Sutton Corp.'s equity includes $3,000 of additional paid-in capital from earlier treasury stock transactions in its preferred stock and none from transactions in its common stock. During the year, under the cost method, Sutton reacquires 2,000 shares of its common stock at $30 per share, later resells 800 of them at $36 per share, and later resells another 1,000 at $24 per share. Sutton charges losses on treasury stock to paid-in capital to the maximum extent ASC 505-30 permits. What amount does Sutton debit to retained earnings as a result of these transactions?""",
    [("$0", "Absorbs the rest of the loss with the $3,000 of APIC from preferred treasury transactions. Only APIC from treasury transactions in the same class of stock (common) may absorb the loss."),
     ("$1,200", "Correct. The $6,000 loss on the second resale is charged first to the $4,800 of APIC from the first resale, and the remaining $1,200 to retained earnings."),
     ("$3,000", "Uses the preferred-stock APIC ($3,000) instead of the $4,800 created by the first resale of common treasury shares."),
     ("$6,000", "Charges the entire loss on the second resale to retained earnings, ignoring the $4,800 of APIC from the first resale.")],
    "B",
    """Cost method: treasury stock is debited at cost, 2,000 × $30 = $60,000. First resale: 800 × ($36 − $30) = $4,800 credited to APIC–treasury stock (common). Second resale: 1,000 × ($30 − $24) = $6,000 below cost, charged first to APIC from earlier treasury transactions in the same class ($4,800) and the remaining $1,200 to retained earnings. APIC from preferred-stock treasury transactions cannot absorb a loss on common shares."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("far-change-in-principle-0001", A3, "Accounting changes and error corrections", AN,
    ["ASC 250-10 (change in accounting principle: retrospective application)"],
    """At the start of Year 3, Tate Co. changes its inventory method from weighted-average cost to FIFO because FIFO better reflects its flow of goods. It can determine the effects for all prior periods. Inventory under each method was: December 31, Year 1 — weighted-average $400,000, FIFO $450,000; December 31, Year 2 — weighted-average $460,000, FIFO $540,000. The tax rate is 25%, and the change also applies for tax purposes. Tate issues comparative statements for Years 2 and 3. How does the change affect the Year 2 amounts in those statements?""",
    [("$0 to January 1, Year 2, retained earnings; $60,000 in Year 3 net income", "Reports a cumulative effect in current-year income, the approach used before retrospective application was required."),
     ("$37,500 to January 1, Year 2, retained earnings; $22,500 to Year 2 net income", "Correct. Opening adjustment $50,000 × 75%; Year 2 income rises by the $30,000 increase in the difference, × 75%."),
     ("$50,000 to January 1, Year 2, retained earnings; $30,000 to Year 2 net income", "Ignores the 25% tax effect of the change."),
     ("$60,000 to January 1, Year 2, retained earnings; $22,500 to Year 2 net income", "Uses the December 31, Year 2, difference ($80,000 × 75%) for the opening balance. The opening balance of the earliest period presented reflects the difference at December 31, Year 1.")],
    "B",
    """A change in accounting principle is applied retrospectively. The cumulative effect on periods before the earliest period presented adjusts the opening retained earnings of Year 2: ($450,000 − $400,000) × 75% = $37,500 increase. Year 2 is restated: FIFO raises ending inventory by $80,000 versus $50,000 at the start, so cost of goods sold falls by $30,000 and net income rises by $30,000 × 75% = $22,500. December 31, Year 2, retained earnings rises by $60,000 in total."""),

mcq("far-change-in-estimate-0001", A3, "Accounting changes and error corrections", AP,
    ["ASC 250-10 (change in accounting estimate effected by a change in accounting principle)", "ASC 360-10 (depreciation)"],
    """On January 1, Year 1, Weller Co. bought a machine for $800,000, estimated a 10-year life and $50,000 salvage value, and depreciated it straight-line. On January 1, Year 4, after studying how the machine's benefits are consumed, Weller switches to the double-declining-balance method, which it concludes better reflects that pattern, and revises the remaining life to 5 years and the salvage value to $30,000. What depreciation expense should Weller recognize in Year 4?""",
    [("$75,000", "Keeps the original straight-line depreciation. The new method and estimates apply from Year 4."),
     ("$109,000", "Applies the revised life and salvage value but keeps straight-line: ($575,000 − $30,000) ÷ 5."),
     ("$230,000", "Correct. Carrying amount $800,000 − 3 × $75,000 = $575,000; double-declining rate 2 ÷ 5 = 40%."),
     ("$218,000", "Deducts the $30,000 salvage value before applying the 40% rate. Double-declining balance ignores salvage value except as a floor.")],
    "C",
    """A change in depreciation method is a change in accounting estimate effected by a change in accounting principle, so it is applied prospectively to the carrying amount at the date of change. Carrying amount at January 1, Year 4 = $800,000 − 3 × ($750,000 ÷ 10) = $575,000. Double-declining-balance rate = 2 ÷ 5 = 40%; Year 4 depreciation = $575,000 × 40% = $230,000. Salvage value limits depreciation only in later years."""),

mcq("far-revenue-principal-agent-0001", A3, "Revenue recognition", AP,
    ["ASC 606-10 (principal versus agent considerations)"],
    """Voya Travel operates a website with two lines of business. Hotel bookings: customers book and pay Voya $300 per room night; the hotel sets the room rate, is responsible for providing the room, and bears the risk if rooms go unsold, and Voya keeps $45 of each booking and remits $255 to the hotel. During the year Voya arranged 10,000 room nights. Tour packages: Voya buys blocks of hotel rooms months in advance under nonrefundable contracts, sets the package price, and is responsible to customers for fixing any problem with the stay. It sold 2,000 packages at $900 each, whose rooms cost it $600 each. What total revenue should Voya recognize for the year?""",
    [("$1,050,000", "Reports both lines net. Voya controls the package rooms before transfer (it bears inventory risk, sets the price and is responsible for fulfillment), so it is the principal for packages and reports them gross."),
     ("$2,250,000", "Correct. Hotel bookings net as agent (10,000 × $45 = $450,000) plus tour packages gross as principal (2,000 × $900 = $1,800,000)."),
     ("$3,600,000", "Reports hotel bookings gross and packages net, the reverse of who controls the rooms in each line."),
     ("$1,800,000", "Reports the packages gross but recognizes nothing for hotel bookings. As an agent, Voya still earns revenue: its $45 fee per room night.")],
    "B",
    """An entity is a principal if it controls the good or service before transfer to the customer; indicators include primary responsibility for fulfillment, inventory risk, and pricing discretion. Hotel bookings: the hotel fulfills, bears inventory risk and sets the price, so Voya is an agent and recognizes its net fee of $450,000. Tour packages: Voya commits to the rooms in advance (inventory risk), sets the price and answers for the stay, so it is the principal and recognizes $1,800,000 gross, with the $1,200,000 room cost in cost of sales. Total revenue = $2,250,000."""),

mcq("far-revenue-contract-costs-0001", A3, "Revenue recognition", AP,
    ["ASC 340-40 (other assets and deferred costs: contracts with customers)"],
    """On July 1, Year 1, Cobalt Services signs a three-year contract to provide IT support. Cobalt expects the customer to renew it once for two more years, and it pays no commission on renewals. In obtaining the contract, Cobalt paid its salesperson a $24,000 commission that is owed only because the contract was signed, paid outside counsel $6,000 to draft the contract, a fee owed whether or not the customer signed, and incurred $3,000 of travel costs to present its proposal, which it would also have incurred had it lost the bid. Cobalt amortizes capitalized contract costs straight-line. What total expense related to these costs should Cobalt recognize in Year 1?""",
    [("$13,800", "Amortizes a full year of the commission. Amortization begins when the contract starts on July 1, so Year 1 has half a year ($2,400)."),
     ("$11,400", "Correct. $6,000 legal + $3,000 travel expensed, plus $24,000 ÷ 5 years × ½ year = $2,400 of amortization."),
     ("$13,000", "Amortizes the commission over the three-year initial term. It is amortized over the period of expected benefit, including the anticipated renewal, since no commission is paid on renewal."),
     ("$33,000", "Expenses the commission. The practical expedient to expense commissions applies only when the amortization period is one year or less.")],
    "B",
    """Only incremental costs of obtaining a contract, those that would not have been incurred had the contract not been obtained, are capitalized: the $24,000 commission. Legal fees for drafting and proposal travel are incurred regardless and are expensed ($9,000). The commission is amortized over the period of expected benefit, the three-year term plus the expected two-year renewal (no commensurate renewal commission): $24,000 ÷ 5 × ½ = $2,400 in Year 1. Total expense = $11,400."""),

mcq("far-lessee-operating-0003", A3, "Lessee accounting", AP,
    ["ASC 842-10 (lease classification)", "ASC 842-20 (lessee operating leases: single lease cost)"],
    """On January 1, Year 1, Yardley Co. leases office equipment for 5 years. The equipment's economic life is 20 years, ownership stays with the lessor, there is no purchase option, the present value of the payments is 40% of the equipment's fair value, and the equipment is not specialized. Annual payments, due each December 31, are $40,000 in Year 1 and increase by $2,000 each year. Yardley pays $5,000 of initial direct costs at commencement, and its incremental borrowing rate is 6%. What total lease cost should Yardley recognize in Year 1?""",
    [("$40,000", "Recognizes the Year 1 cash payment. Operating lease cost is recognized straight-line over the term."),
     ("$41,000", "Adds the initial direct costs' amortization to the Year 1 cash payment instead of the straight-line payment amount."),
     ("$44,000", "Uses straight-line payments but omits the $1,000 of amortization of initial direct costs, which is part of the single lease cost."),
     ("$45,000", "Correct. Total payments $220,000 ÷ 5 = $44,000 straight-line, plus $5,000 ÷ 5 = $1,000 of initial direct costs.")],
    "D",
    """None of the finance-lease criteria is met (no transfer of ownership or purchase option, a term that is 25% of economic life, present value well below substantially all of fair value, and nonspecialized equipment), so the lease is an operating lease. Its single lease cost is the total lease payments plus initial direct costs, recognized straight-line: ($40,000 + $42,000 + $44,000 + $46,000 + $48,000 + $5,000) ÷ 5 = $45,000. The discount rate affects the measurement of the liability and right-of-use asset, not the straight-line cost."""),

mcq("far-uncertain-tax-positions-0001", A3, "Accounting for income taxes", RU,
    ["ASC 740-10 (accounting for uncertainty in income taxes)"],
    """Under ASC 740, which statement correctly describes how an entity accounts for an uncertain tax position?""",
    [("It recognizes a benefit only if the position is probable of being sustained on examination.", "Uses the contingency threshold. The recognition threshold for tax positions is more likely than not."),
     ("It measures a recognized benefit at the single most likely amount to be sustained on settlement.", "The benefit is the largest amount with a greater than 50% cumulative likelihood of being realized, not the single most likely outcome."),
     ("It recognizes a benefit only if the position is more likely than not to be sustained on its technical merits.", "Correct. Recognition requires a more-likely-than-not threshold, assuming examination by a taxing authority with full knowledge of all relevant information."),
     ("It considers the chance that the taxing authority will not examine the position when deciding recognition.", "The entity must assume the position will be examined by an authority with full knowledge; detection risk is ignored.")],
    "C",
    """ASC 740-10 uses a two-step approach. Recognition: a benefit is recognized only if it is more likely than not (greater than 50%) that the position will be sustained on examination based on its technical merits, presuming the taxing authority examines it with full knowledge. Measurement: the benefit recognized is the largest amount that is more than 50% likely to be realized on ultimate settlement, based on cumulative probabilities."""),

mcq("far-subsequent-events-0002", A3, "Subsequent events", AN,
    ["ASC 855-10 (recognized and nonrecognized subsequent events)", "ASC 326-20 (credit losses)", "ASC 450-20 (loss contingencies)"],
    """Tamsin Co.'s December 31, Year 1, statements will be issued on March 15, Year 2. Between those dates: (1) on January 25, a customer that owed $80,000 at year-end filed for bankruptcy because of financial difficulties that had built up over Year 1; Tamsin now expects to collect $20,000, and its allowance included $10,000 for this customer; (2) on February 10, Tamsin settled for $150,000 a lawsuit over a Year 1 injury for which it had accrued $100,000; (3) on February 20, a fire destroyed an uninsured warehouse with a carrying amount of $300,000; and (4) on March 1, Tamsin issued $1,000,000 of bonds. What is the effect on Tamsin's Year 1 pretax income, and which events require disclosure without adjustment?""",
    [("$0 decrease; disclose all four events", "Treats every event as nonrecognized. The bankruptcy and the settlement give evidence about conditions that existed at year-end, so they are recognized."),
     ("$50,000 decrease; disclose the fire and the bond issue", "Adjusts for only one of the two events that give evidence about conditions existing at year-end."),
     ("$100,000 decrease; disclose the fire only", "Omits the bond issue. A significant financing after year-end is a nonrecognized event that is disclosed."),
     ("$100,000 decrease; disclose the fire and the bond issue", "Correct. The customer's loss ($50,000 more allowance) and the settlement ($50,000 more accrual) are recognized; the fire and the bond issue are disclosed.")],
    "D",
    """Events that give evidence about conditions existing at the balance sheet date are recognized. The customer's bankruptcy resulted from deterioration during Year 1, so the allowance for that customer rises from $10,000 to $60,000 ($80,000 − $20,000): a $50,000 charge. The settlement confirms a Year 1 obligation at $150,000: $50,000 more than accrued. Year 1 pretax income falls by $100,000. The fire and the bond issue reflect conditions arising after year-end; they are disclosed, not recognized."""),
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
