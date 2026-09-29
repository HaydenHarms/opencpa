"""FAR batch 01 — 25 items adapted from the legacy cpa-study.html bank and fully re-reviewed.

Run: python3 scripts/batches/far-batch-01.py  (writes content/far/*.yaml)
Every numeric answer and distractor below was recomputed in code during review.
"""
import os, yaml

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
RU, AP, AN = "Remembering and Understanding", "Application", "Analysis"


def mcq(id, area, topic, skill, refs, stem, choices, answer, explanation):
    return dict(
        id=id, type="mcq",
        blueprint=dict(section="FAR", area=area, topic=topic, skill=skill),
        review=dict(status="reviewed", references=refs,
                    notes="Batch 01. Adapted from legacy bank; answer re-solved, arithmetic checked in code, distractors rebuilt where needed."),
        stem=stem.strip(),
        choices=[dict(id=k, text=t, rationale=r) for k, (t, r) in zip("ABCDEF", choices)],
        answer=answer, explanation=explanation.strip(),
    )


ITEMS = [
# ── Area I ──────────────────────────────────────────────────────────────
mcq("far-conceptual-framework-0001", A1, "General-purpose financial reporting: for-profit business entities", RU,
    ["FASB Concepts Statement No. 8, Chapter 3 (QC12–QC16)"],
    """A reviewer finds that management deliberately set its warranty reserve and its allowance for credit losses at the high end of their reasonable ranges, choosing both estimates because they reduce reported net income. Under the FASB Conceptual Framework, which ingredient of faithful representation is most directly threatened?""",
    [("Verifiability", "Tempting because estimates are hard to replicate, but verifiability is an enhancing characteristic, not an ingredient of faithful representation."),
     ("Timeliness", "An enhancing characteristic about when information is available; nothing in the facts concerns timing."),
     ("Neutrality", "Correct. Selecting assumptions to push results in a chosen direction is bias, and neutrality means information is free from bias."),
     ("Comparability", "An enhancing characteristic comparing entities or periods; the problem here is directional bias, not inconsistency.")],
    "C",
    """Faithful representation has three ingredients: completeness, neutrality, and freedom from error. Systematically choosing assumptions to lower income is bias, which violates neutrality. Verifiability, comparability, and timeliness are enhancing characteristics."""),

mcq("far-cash-flows-0001", A1, "General-purpose financial reporting: for-profit business entities", AP,
    ["ASC 230-10-45-28"],
    """Marlow Corp. reports net income of $180,000. During the year, depreciation was $24,000, accounts receivable increased by $31,000, inventory decreased by $12,000, and Marlow recorded a $9,000 gain on the sale of equipment. Under the indirect method, what is net cash provided by operating activities?""",
    [("$152,000", "Subtracts the inventory decrease. A decrease in inventory means less cash was tied up, so it is added back."),
     ("$176,000", "Correct. $180,000 + $24,000 − $9,000 − $31,000 + $12,000."),
     ("$185,000", "Forgets to remove the $9,000 gain. The full sale proceeds belong in investing activities, so the gain must come out of operating."),
     ("$238,000", "Adds the receivables increase. Higher receivables mean revenue was recognized but not yet collected, so the increase is subtracted.")],
    "B",
    """Start with net income, add back noncash depreciation, remove the gain (its cash is in investing), subtract the increase in receivables, and add the decrease in inventory: $180,000 + $24,000 − $9,000 − $31,000 + $12,000 = $176,000."""),

mcq("far-cash-flows-0002", A1, "General-purpose financial reporting: for-profit business entities", AP,
    ["ASC 230-10-45-15", "ASC 230-10-45-28"],
    """Fenwick Ltd. reports net income of $140,000. During the year: depreciation $33,000; loss on early retirement of bonds $8,000; accounts receivable increased $19,000; unearned revenue increased $13,000; dividends paid $20,000. Under the indirect method and U.S. GAAP, what is net cash provided by operating activities?""",
    [("$155,000", "Subtracts the $20,000 of dividends paid. Under U.S. GAAP, dividends paid are a financing outflow, not an operating adjustment."),
     ("$159,000", "Subtracts the $8,000 loss instead of adding it back. A loss reduced net income without using operating cash."),
     ("$162,000", "Omits the unearned revenue increase. Cash collected in advance of earning revenue is an operating inflow."),
     ("$175,000", "Correct. $140,000 + $33,000 + $8,000 − $19,000 + $13,000.")],
    "D",
    """Add back depreciation and the loss on bond retirement (the cash paid to retire bonds is financing), subtract the receivables increase, and add the unearned revenue increase: $140,000 + $33,000 + $8,000 − $19,000 + $13,000 = $175,000. Dividends paid are reported in financing activities."""),

mcq("far-nfp-net-assets-0001", A1, "General-purpose financial reporting: nongovernmental not-for-profit entities", AP,
    ["ASC 958-205-45-9 through 45-12"],
    """Clearfield Museum receives a $500,000 donation restricted to building a new gallery. The museum does not have a policy of implying a time restriction on long-lived assets. During the year, the museum spends the $500,000 and places the gallery in service. How are net assets affected by these two events?""",
    [("Receipt: with donor restrictions +$500,000. When the gallery is placed in service: $500,000 released from with donor restrictions to without donor restrictions.", "Correct. The purpose restriction is satisfied when the gallery is placed in service, triggering a release (reclassification)."),
     ("Receipt: without donor restrictions +$500,000. No entry when the gallery is placed in service.", "Ignores the donor's restriction at receipt. Donor-restricted gifts are reported as with donor restrictions."),
     ("Receipt: with donor restrictions +$500,000. No release until the gallery is sold or fully depreciated.", "Would apply only if the museum had a policy of implying a time restriction over the asset's life; the facts say it does not."),
     ("Receipt and use are both reported without donor restrictions because the restriction is met in the same year.", "Only allowed if the entity has elected and disclosed a same-period policy for simultaneous release; not given here, and the question asks about the default.")],
    "A",
    """A purpose-restricted gift increases net assets with donor restrictions. Without a policy implying a time restriction, the restriction on a gift for a long-lived asset expires when the asset is placed in service, and the amount is reported as net assets released from restrictions."""),

mcq("far-nfp-joint-costs-0001", A1, "General-purpose financial reporting: nongovernmental not-for-profit entities", AP,
    ["ASC 958-720-45-29", "ASC 958-720-45-52"],
    """Sunrise Health Coalition runs a $200,000 direct-mail campaign combining health education content with a fundraising appeal. The activity meets the purpose, audience, and content criteria for joint-cost allocation. Using a reasonable allocation method, the coalition determines that 40% of the activity relates to program services. How are the costs reported?""",
    [("$80,000 program services; $120,000 fundraising", "Correct. When all three criteria are met, joint costs are allocated between functions on a rational basis: 40% × $200,000 to program."),
     ("$200,000 fundraising", "This is the result when any of the three criteria is not met. Here all three are met."),
     ("$100,000 program services; $100,000 fundraising", "Splits evenly with no basis. The allocation must follow a rational, systematic method, which produced 40/60."),
     ("$200,000 program services", "Ignores the fundraising component. Meeting the criteria permits allocation, not full program classification.")],
    "A",
    """If a joint activity meets the purpose, audience, and content criteria, costs are allocated between program and fundraising using a reasonable method. Program = 40% × $200,000 = $80,000; fundraising = $120,000. If any criterion fails, all costs are fundraising."""),

mcq("far-governmental-funds-0001", A1, "State and local government concepts", AN,
    ["GASB Statement No. 34", "GASB Codification 1800"],
    """Riverside County issues $5,000,000 of general obligation bonds and uses the proceeds to build a courthouse. How is this reported in the governmental fund statements versus the government-wide statements?""",
    [("Governmental funds: bond proceeds as an other financing source and a capital outlay expenditure. Government-wide: a long-term liability and a capital asset that is depreciated.", "Correct. Funds use the current financial resources focus; government-wide statements use the economic resources focus and full accrual."),
     ("Governmental funds: a long-term liability and a capitalized asset. Government-wide: an other financing source and an expenditure.", "Reverses the two measurement focuses."),
     ("Governmental funds: bond proceeds as revenue and the bonds as a fund liability. Government-wide: the same treatment.", "Bond proceeds are never revenue, and general long-term debt is not a governmental fund liability."),
     ("Governmental funds: an other financing source and the bonds as a fund liability. Government-wide: the courthouse is expensed.", "Governmental funds do not report general long-term debt, and government-wide statements capitalize capital assets.")],
    "A",
    """Governmental funds (modified accrual, current financial resources) report the proceeds as an other financing source and construction as capital outlay expenditures; neither the debt nor the asset appears in the fund. Government-wide statements (full accrual, economic resources) report the bonds as a long-term liability and the courthouse as a depreciable capital asset."""),

mcq("far-governmental-encumbrances-0001", A1, "State and local government concepts", AP,
    ["GASB Codification 1700 (budgetary accounting and encumbrances)"],
    """Oakdale School District's general fund issues a purchase order for $90,000 of science equipment and records an encumbrance. The equipment arrives with an invoice for $92,000. What is recorded when the goods are received?""",
    [("Reverse the $90,000 encumbrance; record a $92,000 expenditure and voucher payable.", "Correct. The encumbrance is reversed at the amount originally recorded, and the expenditure is recorded at the actual invoice amount."),
     ("Keep the $90,000 encumbrance open and add a $2,000 encumbrance for the overrun.", "Encumbrances are closed out once goods are received and the liability is recorded."),
     ("Record the equipment as a $90,000 asset and a $2,000 expenditure for the variance.", "Governmental funds record capital outlay expenditures, not assets, and at the actual amount."),
     ("Reverse the encumbrance at $92,000; record a $92,000 expenditure and voucher payable.", "The reversal must equal the amount originally encumbered ($90,000), not the invoice amount.")],
    "A",
    """When goods arrive, the encumbrance is reversed for the amount originally recorded ($90,000), and the expenditure and liability are recorded at the actual cost ($92,000)."""),

# ── Area II ─────────────────────────────────────────────────────────────
mcq("far-ppe-impairment-0001", A2, "Property, plant and equipment", AP,
    ["ASC 360-10-35-17", "ASC 360-10-35-29"],
    """Parkside Manufacturing's machinery (held and used) has a carrying amount of $850,000. Undiscounted future cash flows from its use and disposition are $820,000, and its fair value is $700,000. What impairment loss should Parkside recognize?""",
    [("$150,000", "Correct. The asset fails the recoverability test ($850,000 > $820,000), so the loss is carrying amount minus fair value."),
     ("$30,000", "Uses the undiscounted cash flows to measure the loss. They are used only to test recoverability."),
     ("$0", "Would be right only if undiscounted cash flows equaled or exceeded the carrying amount."),
     ("$120,000", "Measures the loss as undiscounted cash flows minus fair value; the loss is carrying amount minus fair value.")],
    "A",
    """Step 1 (recoverability): carrying amount $850,000 exceeds undiscounted cash flows of $820,000, so the asset is not recoverable. Step 2 (measurement): loss = carrying amount − fair value = $850,000 − $700,000 = $150,000."""),

mcq("far-ppe-exchange-0001", A2, "Property, plant and equipment", AP,
    ["ASC 845-10-30-1"],
    """Harwick Corp. exchanges old machinery (book value $180,000; fair value $210,000) plus $40,000 cash for new equipment with a fair value of $250,000. The exchange has commercial substance. What gain does Harwick recognize, and at what amount is the new equipment recorded?""",
    [("Gain of $30,000; new equipment $250,000", "Correct. With commercial substance, the gain is fair value minus book value of the asset given up, and the new asset is recorded at fair value."),
     ("No gain; new equipment $220,000", "Carryover-basis treatment, which applies only when the exchange lacks commercial substance."),
     ("Gain of $70,000; new equipment $250,000", "Compares the new asset's fair value to the old book value and ignores the $40,000 of cash paid."),
     ("Gain of $30,000; new equipment $220,000", "Mixes the two methods: recognizes the gain but records the asset at carryover basis.")],
    "A",
    """With commercial substance, the exchange is measured at fair value. Gain = $210,000 fair value − $180,000 book value = $30,000. The new equipment is recorded at $210,000 + $40,000 cash = $250,000, which equals its fair value."""),

mcq("far-ppe-replacement-0001", A2, "Property, plant and equipment", AP,
    ["ASC 360-10-30-1", "ASC 360-10-40"],
    """Bellview Corp. replaces its warehouse roof. The old roof, recorded as a separate component, cost $95,000 and has accumulated depreciation of $75,000. The new roof costs $180,000 and extends the building's useful life. How should Bellview account for the replacement?""",
    [("Capitalize $180,000, remove the old roof's $20,000 carrying amount, and recognize a $20,000 loss.", "Correct. The replaced component is derecognized, and the new component is capitalized."),
     ("Expense $180,000 as repairs and maintenance.", "Ordinary repairs maintain an asset; a replacement that extends useful life is capitalized."),
     ("Capitalize $180,000 and leave the old roof on the books.", "Would double-count the roof. The replaced component's cost and accumulated depreciation must be removed."),
     ("Capitalize $180,000 and reduce accumulated depreciation by $20,000.", "Removes neither the old cost nor its full accumulated depreciation, so the asset records stay wrong.")],
    "A",
    """When the replaced part's cost and depreciation are known, remove them ($95,000 cost and $75,000 accumulated depreciation), recognize a $20,000 loss on the carrying amount written off, and capitalize the new roof at $180,000."""),

mcq("far-ppe-composite-0001", A2, "Property, plant and equipment", AP,
    ["ASC 360-10-35-4"],
    """Montrose Industries depreciates its equipment using the composite method. During the year it retires equipment with an original cost of $180,000 and receives no proceeds. Which entry records the retirement?""",
    [("Dr Accumulated depreciation $180,000; Cr Equipment $180,000", "Correct. Under the composite method, no gain or loss is recognized on retirement; the difference goes to accumulated depreciation."),
     ("Dr Loss on disposal $180,000; Cr Equipment $180,000", "Treats the asset as fully undepreciated and recognizes a loss, which the composite method does not do."),
     ("Dr Depreciation expense $180,000; Cr Equipment $180,000", "Expenses the cost directly instead of charging accumulated depreciation."),
     ("Dr Accumulated depreciation $162,000; Dr Loss $18,000; Cr Equipment $180,000", "Tracks depreciation for an individual asset, which the composite method does not do.")],
    "A",
    """Composite depreciation treats a group as one asset. On retirement, credit the asset for its cost and debit accumulated depreciation for cost minus any proceeds. No gain or loss is recognized."""),

mcq("far-investments-trading-0001", A2, "Investments", AP,
    ["ASC 320-10-35-1(a)"],
    """On January 1, Atlas Corp. buys $500,000 of 4% corporate bonds at par. Management intends to profit from short-term price changes. By December 31, the bonds' fair value is $522,000, and Atlas has earned $20,000 of interest. How much related to these bonds is included in Atlas's net income for the year?""",
    [("$20,000", "Excludes the unrealized gain, which is the treatment for available-for-sale or held-to-maturity securities."),
     ("$20,000, with the $22,000 unrealized gain in other comprehensive income", "That split is the available-for-sale treatment."),
     ("$42,000", "Correct. For trading securities, interest income and unrealized holding gains both go to net income."),
     ("$22,000", "Ignores interest income, which is always recognized in net income.")],
    "C",
    """Bonds held for short-term profit are trading securities. Unrealized holding gains and losses on trading securities are included in earnings: $20,000 interest + ($522,000 − $500,000) $22,000 unrealized gain = $42,000."""),

mcq("far-investments-afs-credit-loss-0001", A2, "Investments", AN,
    ["ASC 326-30-35-2", "ASC 326-30-35-3"],
    """Foxworth Inc. holds available-for-sale bonds with an amortized cost of $100,000 and a year-end fair value of $88,000. Of the $12,000 decline, $7,000 is attributable to expected credit losses and $5,000 to rising market interest rates. Foxworth does not intend to sell and is not likely to be required to sell. How is the decline reported?""",
    [("$12,000 loss in net income", "Recognizes the whole decline in earnings, as if the securities were trading."),
     ("$7,000 credit loss in net income through an allowance; $5,000 unrealized loss in other comprehensive income", "Correct. For AFS debt, the credit portion goes to net income (via an allowance) and the noncredit portion goes to OCI."),
     ("$12,000 unrealized loss in other comprehensive income", "Ignores the credit loss, which must be recognized in earnings."),
     ("$5,000 loss in net income; $7,000 in other comprehensive income", "Swaps the two components.")],
    "B",
    """Under ASC 326-30, an impaired AFS debt security the holder does not intend to sell is split: the credit loss ($7,000) is recorded through an allowance and net income (limited to the amount by which fair value is below amortized cost), and the remaining decline ($5,000) goes to OCI."""),

mcq("far-equity-issuance-0001", A2, "Equity", AP,
    ["ASC 505-10"],
    """Redford Corp. issues 8,000 shares of $2 par value common stock for $18 per share. What are the credits in the journal entry?""",
    [("Common stock $144,000", "Credits all proceeds to common stock. Only par value goes to common stock."),
     ("Common stock $16,000; additional paid-in capital $128,000", "Correct. Par of 8,000 × $2 goes to common stock, and the excess over par goes to APIC."),
     ("Common stock $16,000; additional paid-in capital $144,000", "Credits total proceeds to APIC, so the entry would not balance with $144,000 of cash."),
     ("Common stock $128,000; additional paid-in capital $16,000", "Swaps the par and excess-over-par amounts.")],
    "B",
    """Cash of 8,000 × $18 = $144,000. Common stock is credited at par (8,000 × $2 = $16,000), and additional paid-in capital gets the excess (8,000 × $16 = $128,000)."""),

mcq("far-equity-retirement-0001", A2, "Equity", AN,
    ["ASC 505-30-30-8"],
    """Mercer Inc. originally issued 1,000 shares of $2 par common stock at $14 per share. It later reacquires and retires all 1,000 shares at $20 per share. No other paid-in capital from treasury or retirement transactions exists. What amount is debited to retained earnings on retirement?""",
    [("$6,000", "Correct. Common stock ($2,000) and the original APIC ($12,000) are removed; the remaining $6,000 of cost goes to retained earnings."),
     ("$0", "APIC can absorb only the paid-in capital from the original issuance ($12,000), not the extra $6,000 paid."),
     ("$12,000", "Charges the original APIC amount to retained earnings instead of removing it from APIC."),
     ("$20,000", "Charges the entire cost to retained earnings without first removing par and APIC.")],
    "A",
    """Retirement entry: Dr Common stock $2,000; Dr APIC $12,000; Dr Retained earnings $6,000; Cr Cash $20,000. The excess of retirement cost over the original issue price is charged to retained earnings."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("far-contingencies-0001", A3, "Contingencies and commitments", AP,
    ["ASC 450-20-25-2", "ASC 450-20-50-3"],
    """Bravo Corp. is a defendant in a product liability lawsuit. Its attorneys conclude that an unfavorable outcome is reasonably possible but not probable, and estimate a loss of $2,000,000 if the plaintiff prevails. How should Bravo report the lawsuit?""",
    [("Accrue a $2,000,000 liability because the amount can be estimated", "Accrual requires both a probable loss and a reasonable estimate; the loss is not probable."),
     ("Disclose the contingency in the notes, but do not accrue a liability", "Correct. A reasonably possible loss requires disclosure of its nature and an estimate of the possible loss, but no accrual."),
     ("Neither accrue nor disclose the lawsuit", "That treatment applies to remote contingencies, not reasonably possible ones."),
     ("Accrue a probability-weighted liability", "U.S. GAAP does not accrue expected values for loss contingencies that are not probable.")],
    "B",
    """Under ASC 450, a loss contingency is accrued only when it is probable and reasonably estimable. When a loss is reasonably possible, the entity discloses the nature of the contingency and an estimate of the possible loss or range, or states that an estimate cannot be made."""),

mcq("far-revenue-allocation-0001", A3, "Revenue recognition", AP,
    ["ASC 606-10-32-28", "ASC 606-10-32-31"],
    """Harmon Technologies sells software licenses, implementation services, and one year of post-contract support for a total of $450,000. The standalone selling prices are licenses $300,000, implementation $150,000, and support $50,000. How much of the transaction price is allocated to the licenses?""",
    [("$270,000", "Correct. $300,000 ÷ $500,000 = 60%; 60% × $450,000."),
     ("$300,000", "Uses the standalone selling price and ignores the $50,000 discount, which is allocated proportionally."),
     ("$150,000", "Splits the price equally across the three obligations instead of using relative standalone selling prices."),
     ("$250,000", "Uses a residual approach ($450,000 − $150,000 − $50,000), which is not permitted when all standalone selling prices are observable.")],
    "A",
    """Allocate on a relative standalone selling price basis. Total SSP = $500,000, so the licenses get $300,000 ÷ $500,000 × $450,000 = $270,000. The $50,000 discount is spread across all three obligations."""),

mcq("far-revenue-allocation-0002", A3, "Revenue recognition", AP,
    ["ASC 606-10-32-31"],
    """Delray Corp. contracts to deliver specialized equipment and provide three years of maintenance for $600,000. The standalone selling prices are equipment $480,000 and maintenance $160,000 per year. How much of the transaction price is allocated to the equipment?""",
    [("$300,000", "Correct. Total SSP = $480,000 + 3 × $160,000 = $960,000; $480,000 ÷ $960,000 × $600,000."),
     ("$360,000", "Includes only two years of maintenance in total SSP ($800,000)."),
     ("$450,000", "Includes only one year of maintenance in total SSP ($640,000)."),
     ("$480,000", "Uses the equipment's standalone selling price instead of its allocated share.")],
    "A",
    """Total SSP = $480,000 + $480,000 = $960,000. Equipment share = 50%, so $600,000 × 50% = $300,000 is allocated to the equipment."""),

mcq("far-revenue-variable-consideration-0001", A3, "Revenue recognition", AP,
    ["ASC 606-10-32-8", "ASC 606-10-32-11"],
    """Meridian Construction agrees to build a facility for $800,000 plus a $100,000 bonus if it finishes within 18 months. Meridian estimates an 85% chance of earning the bonus. Meridian uses the most likely amount method, and including the bonus is not constrained. What is the transaction price?""",
    [("$900,000", "Correct. The most likely outcome is that the bonus is earned, so the full $100,000 is included."),
     ("$885,000", "Uses the expected value method: 15% × $800,000 + 85% × $900,000."),
     ("$800,000", "Excludes the variable consideration, which is only appropriate if the constraint applies."),
     ("$850,000", "Includes half the bonus with no basis in either estimation method.")],
    "A",
    """The most likely amount method picks the single most likely outcome, which is best for binary outcomes like a bonus that is either earned or not. With an 85% likelihood, the bonus is included: $800,000 + $100,000 = $900,000."""),

mcq("far-lessee-operating-0001", A3, "Lessee accounting", AP,
    ["ASC 842-20-30-1"],
    """On January 1, Calloway Corp. commences a 4-year operating lease with annual payments of $120,000 due at the end of each year. Calloway's incremental borrowing rate is 6%, and the present value factor for an ordinary annuity of 4 periods at 6% is 3.4651. What lease liability does Calloway record at commencement?""",
    [("$415,812", "Correct. $120,000 × 3.4651."),
     ("$480,000", "Uses the undiscounted payments and ignores the time value of money."),
     ("$120,000", "Records only one payment."),
     ("$440,761", "Discounts the payments as an annuity due, but the payments are made at the end of each year.")],
    "A",
    """For both operating and finance leases, the lessee measures the liability at the present value of the remaining lease payments: $120,000 × 3.4651 = $415,812. Because the payments are in arrears, the ordinary annuity factor applies."""),

mcq("far-lessee-finance-0001", A3, "Lessee accounting", AN,
    ["ASC 842-20-25-5", "ASC 842-20-35-8"],
    """On January 1, Year 1, Reeves Corp. commences a 5-year finance lease. The lease liability at commencement is $200,000 (rounded), the annual payment of $50,000 is due each December 31, and the discount rate is 8%. The right-of-use asset is amortized straight-line over the lease term. What total lease-related expense does Reeves recognize in Year 2?""",
    [("$53,280", "Correct. Year 2 interest of $13,280 on a $166,000 opening liability, plus $40,000 of amortization."),
     ("$56,000", "Uses Year 1 interest ($16,000) without reducing the liability for the Year 1 principal payment."),
     ("$40,000", "Includes only amortization. A finance lease also has interest expense."),
     ("$50,000", "Treats the cash payment as the expense.")],
    "A",
    """Year 1: interest $16,000, principal reduction $34,000, ending liability $166,000. Year 2: interest = $166,000 × 8% = $13,280. Amortization = $200,000 ÷ 5 = $40,000. Total Year 2 expense = $53,280."""),

mcq("far-lessee-operating-0002", A3, "Lessee accounting", AP,
    ["ASC 842-20-25-6"],
    """Garland Inc. leases equipment for 5 years with payments of $30,000 at the end of each year. The discount rate is 7% (PV factor 4.1002), and the equipment's useful life is 7 years. The lease meets none of the finance lease criteria. What total lease expense does Garland recognize in Year 1?""",
    [("$30,000", "Correct. An operating lease recognizes a single straight-line lease cost; with level payments that equals the annual payment."),
     ("$33,212", "Finance lease treatment: $24,601 amortization plus $8,610 interest."),
     ("$24,601", "Only straight-line amortization of the right-of-use asset, with no interest component."),
     ("$26,183", "Amortizes the right-of-use asset over the 7-year useful life and adds interest, which is not how either lease type works here.")],
    "A",
    """Operating lease cost is recognized straight-line over the lease term: ($30,000 × 5) ÷ 5 = $30,000 per year. The single lease cost combines interest on the liability and a plug amortization of the right-of-use asset."""),

mcq("far-income-taxes-0001", A3, "Accounting for income taxes", AP,
    ["ASC 740-10-25-20", "ASC 740-10-30-8"],
    """Cypress Corp. has two book–tax differences this year: (1) $60,000 of dividends that qualify for a 100% dividends-received deduction, and (2) $80,000 of tax depreciation in excess of book depreciation. The enacted tax rate is 21%. What deferred tax liability results from these items?""",
    [("$16,800", "Correct. Only the depreciation difference is temporary: $80,000 × 21%."),
     ("$29,400", "Treats the dividends-received deduction as a temporary difference; it is permanent and never reverses."),
     ("$12,600", "Applies the rate to the dividends instead of the depreciation."),
     ("$0", "Treats both differences as permanent; excess tax depreciation reverses in future years.")],
    "A",
    """Deferred taxes arise only from temporary differences. The 100% dividends-received deduction is permanent. Excess tax depreciation is a taxable temporary difference: $80,000 × 21% = $16,800 deferred tax liability."""),

mcq("far-income-taxes-0002", A3, "Accounting for income taxes", AP,
    ["ASC 740-10-35-4", "ASC 740-10-45-15"],
    """Holloway Corp. has a $300,000 taxable temporary difference that it measured at the 20% enacted rate, producing a $60,000 deferred tax liability. Before year-end, a new 25% rate is enacted that will apply when the difference reverses. No other temporary differences exist. What adjustment does Holloway record?""",
    [("Increase the deferred tax liability by $15,000, with a charge to income tax expense from continuing operations", "Correct. Remeasure at the new enacted rate ($75,000) and recognize the change in income from continuing operations."),
     ("No adjustment; keep the rate that applied when the difference arose", "Deferred taxes are remeasured when rates change; there is no lock-in."),
     ("Increase the deferred tax liability by $15,000 through other comprehensive income", "The effect of a rate change is recognized in income from continuing operations."),
     ("Record $75,000 of additional income tax expense", "Records the entire remeasured balance instead of the $15,000 change.")],
    "A",
    """Deferred tax balances are measured at the enacted rate expected to apply when differences reverse. New liability = $300,000 × 25% = $75,000; the $15,000 increase is recorded in income tax expense in the period of enactment."""),

mcq("far-income-taxes-0003", A3, "Accounting for income taxes", AP,
    ["ASC 740-10-25-20"],
    """A company buys equipment for $500,000 and depreciates it straight-line over 5 years for book purposes ($100,000 per year). In Year 1, it deducts $200,000 of tax depreciation. The enacted tax rate for all years is 25%. What deferred tax balance exists at the end of Year 1?""",
    [("$25,000 deferred tax liability", "Correct. Book basis $400,000 exceeds tax basis $300,000 by $100,000; $100,000 × 25%."),
     ("$25,000 deferred tax asset", "Reverses the direction. Book basis above tax basis means higher future taxable income."),
     ("$50,000 deferred tax liability", "Applies the rate to the full tax deduction instead of the basis difference."),
     ("$125,000 deferred tax liability", "Applies the rate to the equipment's cost.")],
    "A",
    """At year-end, the book basis is $400,000 and the tax basis is $300,000. The $100,000 excess is a taxable temporary difference, so the deferred tax liability is $100,000 × 25% = $25,000."""),
]

def place_answers(items):
    """Move each correct choice to a balanced, deterministic position (A, B, C, D cycling)
    so the key's position carries no signal. Order of the other choices is preserved."""
    for n, it in enumerate(items):
        ch = it["choices"]
        right = next(c for c in ch if c["id"] == it["answer"])
        others = [c for c in ch if c is not right]
        pos = n % len(ch)
        new = others[:pos] + [right] + others[pos:]
        for k, c in zip("ABCDEF", new):
            c["id"] = k
        it["choices"] = new
        it["answer"] = "ABCDEF"[pos]
    return items


if __name__ == "__main__":
    place_answers(ITEMS)
    root = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
    os.makedirs(root, exist_ok=True)
    for it in ITEMS:
        with open(os.path.join(root, it["id"] + ".yaml"), "w") as f:
            yaml.safe_dump(it, f, sort_keys=False, allow_unicode=True, width=100)
    print(f"wrote {len(ITEMS)} items")
