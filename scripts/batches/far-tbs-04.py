"""FAR simulations batch 04 — six Area III simulations (docs/plans/far-simulations.md). See docs/reviews/far-tbs-04.md.

Every simulation has at least two source-style exhibits with data to reject, 6-10 points, a stated rounding rule and
one key line per account. Every number is computed here (Decimal, rounded half up) and stored in cents; the script
asserts that each schedule ties before writing anything.

Run: python3 scripts/batches/far-tbs-04.py  (writes content/far/far-tbs-*.yaml for this batch)
"""
import os
from decimal import Decimal, ROUND_HALF_UP

import yaml

A3 = "Area III — Select Transactions"
NOTE = "FAR simulations batch 04. Written from scratch; every number computed in code."


def c(dollars):
    """Dollars (int or Decimal) to whole cents."""
    return int((Decimal(dollars) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def r0(x):
    """Round to the nearest dollar, half up."""
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def d(x):
    """$1,234 or ($1,234) for negatives."""
    return f"(${-x:,})" if x < 0 else f"${x:,}"


def amt(x):
    """Statement-style amount: 1,234 or (1,234)."""
    return f"({-x:,})" if x < 0 else f"{x:,}"


def num(id, prompt, dollars, explanation, points=1, tolerance=100):
    """A currency task: the key in cents, accepting answers within $1 unless told otherwise."""
    return dict(id=id, type="numeric", points=points, unit="cents", tolerance=tolerance, prompt=prompt,
                answer=c(dollars), explanation=explanation)


def select(id, prompt, options, rows, explanation, points):
    """rows: (row id, label, answer)."""
    for _, _, a in rows:
        assert a in options, a
    return dict(id=id, type="select", points=points, prompt=prompt, options=options,
                rows=[dict(id=i, label=l, answer=a) for i, l, a in rows], explanation=explanation)


def table(header, rows):
    out = "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n"
    return out + "\n".join("| " + " | ".join(str(x) for x in r) + " |" for r in rows)


def tbs(id, topic, skill, refs, title, scenario, exhibits, tasks):
    return dict(
        id=id, type="tbs",
        blueprint=dict(section="FAR", area=A3, topic=topic, skill=skill),
        review=dict(status="reviewed", references=refs, notes=NOTE),
        title=title, scenario=scenario.strip(),
        exhibits=[dict(title=t, body=b.strip()) for t, b in exhibits],
        tasks=tasks,
    )


# ── Simulation 1: contingencies from counsel's letter and board minutes (III.B.c, Analysis) ──────────────────────
SUIT_LO, SUIT_HI, SUIT_MID = 340000, 760000, 550000        # product suit: range, no amount better; draft used the midpoint
TAX_LO, TAX_HI, TAX_LIKELY, TAX_PROPOSED = 90000, 186000, 124000, 186000
UNASSERTED_LO, UNASSERTED_HI = 150000, 400000              # indemnification claim by a division buyer, outcome unpredictable
SHAREHOLDER_SOUGHT = 2000000                               # dismissed; appeal pending; remote
GAIN_AWARD = 280000                                        # jury award to Larkhall, appealed: gain contingency
PUMPS, PUMP_PRICE = 600, 1850                              # noncancelable, unhedged purchase commitment
PUMP_SELL, PUMP_SELL_COST, PUMP_REPL = 1900, 210, 1640     # replacement cost is data to reject
assert TAX_PROPOSED == TAX_HI

pump_nrv = PUMP_SELL - PUMP_SELL_COST
commit_loss = PUMPS * (PUMP_PRICE - pump_nrv)
commit_loss_repl = PUMPS * (PUMP_PRICE - PUMP_REPL)
assert commit_loss > 0 and commit_loss != commit_loss_repl
liab_correct = SUIT_LO + TAX_LIKELY + commit_loss
liab_draft = SUIT_MID
assert SUIT_MID == (SUIT_LO + SUIT_HI) // 2
pretax_change = -(liab_correct - liab_draft) - GAIN_AWARD   # draft charged the 550,000 to Year 1 and recorded the gain
rp_excess = (SUIT_HI - SUIT_LO) + (TAX_HI - TAX_LIKELY) + UNASSERTED_HI
rp_excess_no_tax = (SUIT_HI - SUIT_LO) + UNASSERTED_HI

letter1 = table(["Matter", "Counsel's comments"], [
    ("1. Arrandale Paper Mills v. Larkhall (filed March, Year 1)",
     f"A paper mill alleges that a pump Larkhall supplied failed and flooded its plant. Discovery is complete. We expect the jury to find for the plaintiff. We estimate damages at between {d(SUIT_LO)} and {d(SUIT_HI)}; on the evidence so far, no amount in that range is a better estimate than any other. Larkhall's insurer has denied coverage under a policy exclusion, and Larkhall does not dispute the denial."),
    ("2. State sales tax assessment",
     f"In November, Year 1, after auditing Larkhall's returns for the three years ended December 31, Year 0, the state's revenue department proposed an assessment of {d(TAX_PROPOSED)}, including interest, on sales Larkhall treated as exempt. Larkhall has appealed. The appeals board has upheld the department on this issue for other distributors, but has generally reduced the amounts assessed. We expect Larkhall to pay between {d(TAX_LO)} and {d(TAX_HI)}, with {d(TAX_LIKELY)} the most likely result."),
    ("3. Quarrendon Holdings v. Larkhall (shareholder suit)",
     f"The plaintiff sought {d(SHAREHOLDER_SOUGHT)}, alleging that Larkhall's Year 0 annual report misstated its backlog. The trial court dismissed the suit in November, Year 1, and the plaintiff has appealed. The state's appellate court has affirmed the dismissal of every suit raising this claim in the past ten years, and we know of nothing that distinguishes this one. We see no reasonable prospect that the appeal will succeed."),
    ("4. Indemnification claim: Elmford Valve Co.",
     f"When Larkhall sold its valve division to Elmford Valve Co. in Year 0, it agreed to indemnify Elmford for losses from any breach of its representations about the division's customer contracts; the indemnity's fair value when given was immaterial, and no liability was recorded. In December, Year 1, Elmford gave notice of a claim under the indemnity, alleging that two contracts were less profitable than represented. Larkhall's defense that the contracts were disclosed accurately has merit, but we cannot predict the outcome; if the claim succeeds, Larkhall would likely pay between {d(UNASSERTED_LO)} and {d(UNASSERTED_HI)}."),
    ("5. Larkhall v. Haskett Castings",
     f"In December, Year 1, a jury awarded Larkhall {d(GAIN_AWARD)} for defective castings Haskett supplied. Haskett has appealed, and the appeal will not be heard before Year 3."),
])
minutes1 = table(["Date", "Item"], [
    ("October 12, Year 1",
     f"The board approved a noncancelable contract with Halvey Pumps Ltd. to buy {PUMPS} model HX-40 pumps at {d(PUMP_PRICE)} each, for delivery in March, Year 2. Larkhall does not hedge its purchase prices."),
    ("December 18, Year 1",
     f"The sales director reported that a competitor's price cuts in December have lowered the market for the HX-40. Larkhall now expects to sell the pumps on the Halvey contract for {d(PUMP_SELL)} each, with selling and delivery costs of {d(PUMP_SELL_COST)} each, and does not expect prices to recover before they are sold. Halvey's price list for new HX-40 orders fell to {d(PUMP_REPL)} in December."),
])
draft1 = table(["Matter", "Draft treatment", "Amount"], [
    ("Arrandale Paper Mills suit", "Accrued liability for litigation (midpoint of counsel's range); charged to Year 1 litigation expense", amt(SUIT_MID)),
    ("Sales tax assessment", "Not accrued; note describes the assessment and the appeal", "—"),
    ("Quarrendon shareholder suit", "Not accrued or disclosed", "—"),
    ("Elmford indemnification claim", f"Not accrued; note describes the claim and counsel's range of {d(UNASSERTED_LO)} to {d(UNASSERTED_HI)}", "—"),
    ("Haskett jury award", "Other receivable; gain recognized in Year 1 other income", amt(GAIN_AWARD)),
    ("Halvey purchase contract", "Not recorded; note describes the commitment", "—"),
])

SIM1 = tbs(
    "far-tbs-contingencies-review-0001", "Contingencies and commitments", "Analysis",
    ["ASC 450-20 (loss contingencies: accrual, ranges with no best estimate, unasserted claims, disclosure)",
     "ASC 450-30 (gain contingencies)", "ASC 460-10 (indemnifications; contingent losses under ASC 450-20)",
     "ASC 330-10-35-17 and 35-18 (losses on firm purchase commitments)"],
    "Year 1 contingencies and commitments review",
    """Larkhall Industrial Supply Co., a distributor of industrial pumps that costs its inventory by FIFO, is finalizing its December 31, Year 1, financial statements, which have not been issued. The controller's draft treatment of six matters is in Exhibit 3. Exhibit 1 is an excerpt from outside counsel's letter, dated February 20, Year 2, and Exhibit 2 is from the minutes of Larkhall's board of directors. Nothing relevant has happened since counsel's letter. Ignore income taxes, and round every amount to the nearest dollar.""",
    [("Exhibit 1: Outside counsel's letter (excerpt), February 20, Year 2", letter1),
     ("Exhibit 2: Board of directors' minutes (excerpts)", minutes1),
     ("Exhibit 3: Controller's draft treatment of contingencies and commitments", draft1)],
    [
        select("t1", "For each matter, indicate how Larkhall should reflect it in its December 31, Year 1, financial statements.",
               ["Recognize (accrue) in the statements", "Disclose in the notes only", "No recognition or disclosure required"],
               [("r1", "Arrandale Paper Mills suit", "Recognize (accrue) in the statements"),
                ("r2", "State sales tax assessment", "Recognize (accrue) in the statements"),
                ("r3", "Quarrendon shareholder suit", "No recognition or disclosure required"),
                ("r4", "Elmford indemnification claim", "Disclose in the notes only"),
                ("r5", "Haskett jury award", "Disclose in the notes only"),
                ("r6", "Halvey purchase contract", "Recognize (accrue) in the statements")],
               "Arrandale: counsel expects a loss and gives a range, so a loss is probable and estimable; accrue. Sales tax: payment of part of the assessment is probable and counsel gives a most likely amount; accrue it (a non-income tax is a loss contingency under ASC 450-20). Quarrendon: after a dismissal that the appellate court has affirmed in every comparable case, the chance of loss is remote; no accrual or disclosure is required. Elmford: the indemnification claim has been asserted, and counsel can't predict the outcome, so a loss is reasonably possible but not probable; disclose the claim and the range, don't accrue. Haskett: a jury award under appeal is a gain contingency; it is not recognized until realized, but it is disclosed, with care not to mislead about its likelihood (ASC 450-30-50-1). Halvey: a net loss on a firm, noncancelable, unhedged purchase commitment is recognized when the goods' expected net realizable value falls below the contract price (ASC 330-10-35-17).",
               points=3),
        num("t2", "What total liability should Larkhall report at December 31, Year 1, for the six matters?", liab_correct,
            f"Arrandale: no amount in the range is better, so accrue the minimum, {d(SUIT_LO)} (not the {d(SUIT_MID)} midpoint). Sales tax: the most likely amount, {d(TAX_LIKELY)}. Halvey: the expected net realizable value is {d(PUMP_SELL)} − {d(PUMP_SELL_COST)} = {d(pump_nrv)} a pump, so the loss is {PUMPS} × ({d(PUMP_PRICE)} − {d(pump_nrv)}) = {d(commit_loss)}, recognized as a liability for the purchase commitment (the {d(PUMP_REPL)} replacement price is not the measure; it gives {d(commit_loss_repl)}). Total: {d(SUIT_LO)} + {d(TAX_LIKELY)} + {d(commit_loss)} = {d(liab_correct)}. Nothing is accrued for the indemnification claim, the shareholder suit or the jury award.",
            points=2),
        num("t3", "By how much should Larkhall's draft Year 1 income before income taxes change as a result of correcting the draft treatment? Enter a decrease as a negative number.", pretax_change,
            f"The draft charged {d(SUIT_MID)} to Year 1 and recognized a {d(GAIN_AWARD)} gain. The correct Year 1 losses are {d(liab_correct)}, so expenses rise by {d(liab_correct)} − {d(SUIT_MID)} = {d(liab_correct - SUIT_MID)}, and the gain is reversed. Change: −{d(liab_correct - SUIT_MID)} − {d(GAIN_AWARD)} = {d(pretax_change)}.",
            points=2),
        num("t4", "Up to the top of each range counsel gives, what total additional loss, beyond any amount Larkhall accrues, should its notes disclose for the six matters?", rp_excess,
            f"Arrandale: {d(SUIT_HI)} − {d(SUIT_LO)} accrued = {d(SUIT_HI - SUIT_LO)}. Sales tax: {d(TAX_HI)} − {d(TAX_LIKELY)} accrued = {d(TAX_HI - TAX_LIKELY)}. Elmford claim (nothing accrued): {d(UNASSERTED_HI)}. Total {d(rp_excess)}. Omitting the sales tax excess gives {d(rp_excess_no_tax)}; the remote shareholder suit is excluded."),
    ],
)


# ── Simulation 2: subsequent events review (III.G.c, Analysis) ─────────────────────────────────────────────────
NI_DRAFT = 1742000
CA_DRAFT = 6480000                   # draft current assets, including the receivable and the equipment held for sale
CONCESSION = 42000                   # credit to Ostler Foods for nonconforming December goods
SHIPMENT = 168000                    # the December 18 shipment, unpaid at year end
HFS_CARRY, HFS_PRICE, HFS_COMM_RATE = 640000, 575000, Decimal("0.03")
LOAN, INSTALLMENT = 2400000, 300000  # term loan, $300,000 due each December 31 from Year 2
NOTE_ST, BONDS = 1000000, 1500000    # note due June 30, Year 2; bonds issued Feb 10, note repaid Feb 15
OTHER_CL = 1860000
SEVERANCE, ACQ = 260000, 3100000
SUIT_MAR = 125000                    # suit filed March 20, after issuance

hfs_comm = r0(HFS_PRICE * HFS_COMM_RATE)
hfs_fvlcs = HFS_PRICE - hfs_comm
hfs_loss = HFS_CARRY - hfs_fvlcs
assert hfs_loss > 0
ni_correct = NI_DRAFT - CONCESSION - hfs_loss
cl_draft = OTHER_CL + LOAN + NOTE_ST
cl_correct = OTHER_CL + INSTALLMENT
cl_waiver_only = OTHER_CL + INSTALLMENT + NOTE_ST
ca_correct = CA_DRAFT - CONCESSION - hfs_loss
wc = ca_correct - cl_correct
wc_assets_only = CA_DRAFT - cl_correct
assert BONDS >= NOTE_ST

draft2 = table(["Item", "Amount"], [
    ("Net income, Year 1", amt(NI_DRAFT)),
    ("Total current assets (including the Ostler receivable and the equipment held for sale)", amt(CA_DRAFT)),
    ("Current liabilities: accounts payable and accrued liabilities", amt(OTHER_CL)),
    ("Current liabilities: note payable to Brannock Bank, due June 30, Year 2", amt(NOTE_ST)),
    ("Current liabilities: term loan from Calder Trust (see note)", amt(LOAN)),
    ("Total current liabilities", amt(cl_draft)),
    ("Equipment held for sale (classified as held for sale on November 30, Year 1, at its carrying amount)", amt(HFS_CARRY)),
])
draft2 += ("\n\nNote on the term loan: the loan is repayable in installments of "
           f"{d(INSTALLMENT)} each December 31 from Year 2 through Year 9. At December 31, Year 1, Penwortham's debt service coverage ratio was below the minimum in the loan agreement, which allows Calder Trust to demand immediate repayment of the whole loan. The staff therefore classified all {d(LOAN)} as current.")
log2 = table(["Date (Year 2)", "Document", "Summary"], [
    ("January 9", "Purchase agreement", f"Penwortham bought the commercial lighting division of Tellwood Electric for {d(ACQ)} in cash."),
    ("January 18", "Letter from Ostler Foods", f"Ostler reports that the display cases Penwortham shipped on December 18, Year 1 (invoice {d(SHIPMENT)}, unpaid), do not meet the refrigeration specification in Ostler's order. Penwortham's engineers confirmed that the cases left the factory that way."),
    ("January 28", "Board minutes", f"The board approved a plan, announced to employees on February 2, to close the Wrexley plant in June, Year 2. Severance under the plan will total {d(SEVERANCE)}."),
    ("February 3", "Credit memo", f"Penwortham agreed to a {d(CONCESSION)} price reduction on the December 18 invoice, and Ostler is keeping the cases."),
    ("February 10", "Bond indenture", f"Penwortham issued {d(BONDS)} of 10-year bonds to refinance the Brannock Bank note."),
    ("February 12", "Letter from Calder Trust", "Calder Trust waives the December 31, Year 1, covenant violation and gives up any right to demand repayment because of it, or because of any other covenant violation, before March 31, Year 3. The installment schedule is unchanged. Penwortham expects to meet the covenant at every measurement date in Year 2."),
    ("February 14", "Bill of sale and broker's statement", f"The equipment held for sale was sold for {d(HFS_PRICE)}; the broker's commission is {int(HFS_COMM_RATE * 100)}% of the price. The buyer's offer, made January 10, was based on an inspection of the equipment as it stood at year end; prices for similar used equipment did not change between November and February."),
    ("February 15", "Bank statement", f"The Brannock Bank note was repaid in full with the bond proceeds."),
    ("March 20", "Complaint", f"A customer sued Penwortham for {d(SUIT_MAR)}, alleging that a cooler Penwortham installed in October, Year 1, caused a fire in its store in December, Year 1."),
])

SIM2 = tbs(
    "far-tbs-subsequent-events-0001", "Subsequent events", "Analysis",
    ["ASC 855-10 (recognized and nonrecognized subsequent events; evaluation through the date the statements are issued)",
     "ASC 470-10-45-11 (callable obligations: covenant waivers obtained before issuance)",
     "ASC 470-10-45-14 (short-term obligations refinanced after the balance sheet date)",
     "ASC 360-10-35-43 (long-lived assets held for sale: fair value less cost to sell)",
     "ASC 420-10 (exit costs recognized when incurred)"],
    "Year 1 subsequent events review",
    """Penwortham Fixtures Inc., a public company that makes refrigerated display cases, filed its December 31, Year 1, financial statements with the SEC on March 12, Year 2. Exhibit 1 shows amounts from the staff's draft, prepared in early January, Year 2, before any of the events in Exhibit 2 were considered. Exhibit 2 is the controller's log of documents received after year end. Ignore income taxes. Round every amount to the nearest dollar.""",
    [("Exhibit 1: Draft amounts, December 31, Year 1", draft2),
     ("Exhibit 2: Controller's log of documents received, Year 2", log2)],
    [
        select("t1", "For each event, indicate how Penwortham should reflect it in its Year 1 financial statements, as filed on March 12, Year 2.",
               ["Recognize in the Year 1 statements", "Disclose in the notes only", "Not reflected in the Year 1 statements"],
               [("r1", "Acquisition of Tellwood's lighting division (January 9)", "Disclose in the notes only"),
                ("r2", "Ostler Foods price reduction (February 3)", "Recognize in the Year 1 statements"),
                ("r3", "Wrexley plant closing and severance (January 28)", "Disclose in the notes only"),
                ("r4", "Evidence from the sale of the equipment held for sale (February 14)", "Recognize in the Year 1 statements"),
                ("r5", "Customer suit over the December store fire (March 20)", "Not reflected in the Year 1 statements")],
               "The acquisition and the plant closing arise from decisions made after year end; they are nonrecognized subsequent events, disclosed because they are material (the severance is a Year 2 exit cost under ASC 420-10). The price reduction settles a dispute over goods that did not meet the order when they were shipped in December, so it gives evidence about a condition that existed at year end and reduces Year 1 revenue and the receivable. The sale, at a price based on the equipment as it stood at year end in an unchanged market, is evidence of its fair value at December 31, so the held-for-sale equipment is written down. A public company evaluates subsequent events through the date it issues (files) its statements; the March 20 suit came after March 12, so it is not reflected, even though the fire occurred in Year 1.",
               points=2),
        num("t2", "What net income should Penwortham report for Year 1?", ni_correct,
            f"Revenue falls by the {d(CONCESSION)} price reduction. The held-for-sale equipment is written down to fair value less cost to sell: {d(HFS_PRICE)} − {d(hfs_comm)} commission ({int(HFS_COMM_RATE * 100)}% × {d(HFS_PRICE)}) = {d(hfs_fvlcs)}, a loss of {d(HFS_CARRY)} − {d(hfs_fvlcs)} = {d(hfs_loss)}. Net income: {d(NI_DRAFT)} − {d(CONCESSION)} − {d(hfs_loss)} = {d(ni_correct)}. The acquisition, the bond issue and the plant closing don't change Year 1 net income.",
            points=2),
        num("t3", "What total current liabilities should Penwortham report at December 31, Year 1?", cl_correct,
            f"The term loan: Calder Trust's waiver, obtained before the statements were issued, gives up the right to demand repayment for more than one year after the balance sheet date, so only the {d(INSTALLMENT)} installment due December 31, Year 2, is current (ASC 470-10-45-11). The Brannock note: bonds were issued to refinance it after year end and before issuance, so it is excluded from current liabilities (ASC 470-10-45-14); the long-term bonds were issued before the note was repaid. Current liabilities: {d(OTHER_CL)} + {d(INSTALLMENT)} = {d(cl_correct)}. Leaving the note current gives {d(cl_waiver_only)}; the draft's {d(cl_draft)} ignores both events.",
            points=2),
        num("t4", "What working capital should Penwortham report at December 31, Year 1?", wc,
            f"Current assets: {d(CA_DRAFT)} − the {d(CONCESSION)} reduction of the Ostler receivable − the {d(hfs_loss)} write-down of the equipment held for sale = {d(ca_correct)}. Current liabilities (task 3): {d(cl_correct)}. Working capital: {d(ca_correct)} − {d(cl_correct)} = {d(wc)}. Correcting only the liabilities gives {d(wc_assets_only)}."),
    ],
)


# ── Simulation 3: multiple-element revenue contract (III.C.d, Application) ──────────────────────────────────────
SSP_SCAN, LIST_SCAN = 1820000, 2050000            # observable SSP; list price is data to reject
INST_COST, INST_MARGIN, THIRD_PARTY_INST = 62400, Decimal("0.25"), 95000
SSP_TRAIN, SESSIONS, SESSIONS_Y1 = 46000, 10, 6
SSP_MAINT_YR, MAINT_YEARS, MAINT_MONTHS_Y1 = 148000, 3, 9
PKG_PRICE, MAINT_BILL = 1705000, 138000           # package due on acceptance; maintenance billed each April 1

ssp_inst = r0(INST_COST * (1 + INST_MARGIN))
ssp = {"Scanner": SSP_SCAN, "Installation": ssp_inst, "Training": SSP_TRAIN, "Maintenance": SSP_MAINT_YR * MAINT_YEARS}
tp = PKG_PRICE + MAINT_BILL * MAINT_YEARS
ssp_total = sum(ssp.values())
alloc = {k: r0(Decimal(tp) * v / ssp_total) for k, v in ssp.items()}
assert sum(alloc.values()) == tp, (sum(alloc.values()), tp)
alloc_scan_3p = r0(Decimal(tp) * SSP_SCAN / (ssp_total - ssp_inst + THIRD_PARTY_INST))
alloc_scan_list = r0(Decimal(tp) * LIST_SCAN / (ssp_total - SSP_SCAN + LIST_SCAN))
rev_train = r0(Decimal(alloc["Training"]) * SESSIONS_Y1 / SESSIONS)
rev_maint = r0(Decimal(alloc["Maintenance"]) * MAINT_MONTHS_Y1 / (12 * MAINT_YEARS))
rev_y1 = alloc["Scanner"] + alloc["Installation"] + rev_train + rev_maint
cash_y1 = PKG_PRICE + MAINT_BILL
contract_bal = cash_y1 - rev_y1                     # positive = contract liability
assert contract_bal > 0
rev_y1_billed = PKG_PRICE + r0(Decimal(MAINT_BILL) * MAINT_MONTHS_Y1 / 12)   # error: revenue = amounts billed, by item
rev_y1_full_train = alloc["Scanner"] + alloc["Installation"] + alloc["Training"] + rev_maint

contract3 = table(["Term", "Detail"], [
    ("Parties and date", "Stannard Imaging Systems and Pellew Valley Hospital, signed January 20, Year 1"),
    ("Scanner", "One SX-7 MRI scanner, with its operating software installed. The scanner cannot operate without the software, and the software runs only on Stannard scanners; Stannard does not sell or license it separately."),
    ("Site survey", "Before delivery, Stannard's engineers will inspect the hospital's imaging suite to plan the delivery route and installation. The survey report is for Stannard's use and is not given to the hospital."),
    ("Installation", "Stannard will install the scanner and test it. The installation is standard and does not modify the scanner; several independent firms are qualified to install SX-7 scanners."),
    ("Training", f"A {SESSIONS}-session course for the hospital's technicians, scheduled at the hospital's request."),
    ("Maintenance", f"Preventive maintenance and on-call repair for {MAINT_YEARS} years from acceptance of the installation. Stannard stands ready to respond throughout the term. Neither party may cancel the maintenance before the end of the term."),
    ("Warranty", "Stannard's standard warranty that the scanner will operate as specified for one year from acceptance, the same warranty it gives every buyer. It covers repairs of defects only."),
    ("Price and payment", f"{d(PKG_PRICE)} for the scanner, installation and training, due on acceptance of the installation; {d(MAINT_BILL)} for each year of maintenance, billed and due at the start of each maintenance year."),
])
pricing3 = table(["Item", "Stannard's pricing data"], [
    ("SX-7 scanner (with its software)", f"List price {d(LIST_SCAN)}. Stannard regularly sells the scanner, without installation, training or maintenance, at prices clustered around {d(SSP_SCAN)}."),
    ("Installation", f"Not sold separately. Expected cost to Stannard {d(INST_COST)}. Independent installers charge about {d(THIRD_PARTY_INST)}."),
    ("Training course", f"Sold separately for {d(SSP_TRAIN)}."),
    ("Maintenance", f"Sold separately for {d(SSP_MAINT_YR)} a year."),
    ("Policy", f"Where a standalone selling price is not observable, Stannard estimates it using the expected cost plus a margin approach, with its normal margin of {int(INST_MARGIN * 100)}% on cost. Stannard measures progress on training by sessions delivered."),
])
log3 = table(["Date (Year 1)", "Event"], [
    ("February 2", "Site survey completed."),
    ("February 24", "Scanner delivered to the hospital. Title and risk of loss passed to the hospital on delivery."),
    ("March 31", f"Installation completed and accepted by the hospital. The hospital paid {d(PKG_PRICE)}."),
    ("April 1", f"Maintenance term began. The hospital paid {d(MAINT_BILL)} for the first maintenance year."),
    ("April – December", f"{SESSIONS_Y1} of the {SESSIONS} training sessions delivered; the rest are scheduled for Year 2."),
])

SIM3 = tbs(
    "far-tbs-revenue-contract-0001", "Revenue recognition", "Application",
    ["ASC 606-10-25-14 through 25-22 (identifying performance obligations; distinct goods and services; set-up activities)",
     "ASC 606-10-32-28 through 32-41 (allocating the transaction price on relative standalone selling prices; estimation methods)",
     "ASC 606-10-25-23 through 25-37 (satisfaction at a point in time and over time; measuring progress)",
     "ASC 606-10-55-30 through 55-35 (assurance-type warranties)",
     "ASC 606-10-45-1 through 45-4 (contract assets and contract liabilities)"],
    "Imaging equipment contract with installation, training and maintenance",
    """Stannard Imaging Systems, a calendar-year company, manufactures MRI scanners. Exhibit 1 summarizes its contract with Pellew Valley Hospital, Exhibit 2 gives Stannard's pricing data, and Exhibit 3 lists what happened under the contract in Year 1. The contract has no significant financing component, and the price is not subject to any discounts, refunds or other variable amounts. Round every amount to the nearest dollar.""",
    [("Exhibit 1: Contract summary", contract3),
     ("Exhibit 2: Pricing data", pricing3),
     ("Exhibit 3: Year 1 contract log", log3)],
    [
        select("t1", "For each promise or activity in the contract, indicate how Stannard should treat it in identifying performance obligations.",
               ["A separate performance obligation", "Part of the scanner performance obligation", "Not a performance obligation"],
               [("r1", "Operating software", "Part of the scanner performance obligation"),
                ("r2", "Site survey", "Not a performance obligation"),
                ("r3", "Installation", "A separate performance obligation"),
                ("r4", "Training course", "A separate performance obligation"),
                ("r5", "Maintenance", "A separate performance obligation"),
                ("r6", "One-year warranty", "Not a performance obligation")],
               "The software is not distinct: the scanner can't operate without it and it runs only on Stannard scanners, so the two are inputs to one combined item. The site survey transfers nothing to the hospital; it is a set-up activity. Installation is distinct: it is standard, doesn't modify the scanner, and other firms can perform it. Training and maintenance are sold separately and are distinct. The warranty only assures that the scanner works as specified, so it is an assurance-type warranty accounted for under ASC 460, not a performance obligation.",
               points=3),
        num("t2", "How much of the transaction price should Stannard allocate to the scanner?", alloc["Scanner"],
            f"Transaction price: {d(PKG_PRICE)} + {MAINT_YEARS} × {d(MAINT_BILL)} = {d(tp)}. Standalone selling prices: scanner {d(SSP_SCAN)} (observable; not the {d(LIST_SCAN)} list price), installation {d(INST_COST)} × {1 + INST_MARGIN} = {d(ssp_inst)} under Stannard's expected cost plus margin policy, training {d(SSP_TRAIN)}, maintenance {MAINT_YEARS} × {d(SSP_MAINT_YR)} = {d(ssp['Maintenance'])}; total {d(ssp_total)}. Scanner: {d(tp)} × {SSP_SCAN:,} ÷ {ssp_total:,} = {d(alloc['Scanner'])} (rounded). The software is part of the scanner, so it gets no separate share. Using the {d(LIST_SCAN)} list price gives {d(alloc_scan_list)}; using the independent installers' {d(THIRD_PARTY_INST)} for installation gives {d(alloc_scan_3p)}. The discount is allocated to every obligation in proportion, because nothing ties it to particular items."),
        num("t3", "What revenue should Stannard recognize from the contract in Year 1?", rev_y1,
            f"Allocations, computed as in task 2: scanner {d(alloc['Scanner'])}, installation {d(alloc['Installation'])}, training {d(alloc['Training'])}, maintenance {d(alloc['Maintenance'])} (total {d(tp)}). Scanner: control passed on delivery, February 24, so all {d(alloc['Scanner'])}. Installation: completed March 31, so all {d(alloc['Installation'])}. Training: {SESSIONS_Y1} of {SESSIONS} sessions, {d(alloc['Training'])} × {SESSIONS_Y1}/{SESSIONS} = {d(rev_train)}. Maintenance: {MAINT_MONTHS_Y1} of {12 * MAINT_YEARS} months, {d(alloc['Maintenance'])} × {MAINT_MONTHS_Y1}/{12 * MAINT_YEARS} = {d(rev_maint)} (rounded). Total {d(rev_y1)}. Recognizing all of the training gives {d(rev_y1_full_train)}.",
            points=2),
        num("t4", "What contract liability should Stannard report for the contract at December 31, Year 1? Enter a contract asset as a negative number.", contract_bal,
            f"Consideration received in Year 1: {d(PKG_PRICE)} + {d(MAINT_BILL)} = {d(cash_y1)}. Revenue recognized: {d(rev_y1)}. The excess, {d(cash_y1)} − {d(rev_y1)} = {d(contract_bal)}, is a contract liability: Stannard has been paid for more than it has transferred. A contract is presented as a single net contract asset or contract liability.",
            points=2),
    ],
)


# ── Simulation 4: accounting change, error and estimate in comparative statements (III.A.b, Analysis) ────────
TAX = Decimal("0.25")
INV = {"Y1": (812000, 776000), "Y2": (905000, 851000)}     # (FIFO, weighted average) at December 31
INV_Y3_WA, INV_Y3_FIFO = 930000, 968000                      # Y3 FIFO is data to reject
COMM, COMM_MONTHS, COMM_Y2_MONTHS = 108000, 36, 6             # commissions paid July 1, Year 2, expensed in error
FLEET_COST, FLEET_LIFE, FLEET_NEW_TOTAL = 1350000, 10, 6     # bought Jan 1, Year 1; revised total life in Year 3
NI_Y2_ORIG, RE_JAN1_Y2_ORIG, DIV_Y2 = 1180000, 4620000, 300000
NI_Y3_DRAFT, DIV_Y3 = 1306000, 320000

def at(x):
    return r0(Decimal(x) * (1 - TAX))

inv_y1_diff = INV["Y1"][0] - INV["Y1"][1]          # WA lower by
inv_y2_diff = INV["Y2"][0] - INV["Y2"][1]
re_adj = -at(inv_y1_diff)                           # Jan 1, Year 2 retained earnings
ni_y2_inv = -at(inv_y2_diff - inv_y1_diff)          # Y2 COGS higher by the change in the difference
comm_amort_y2 = r0(Decimal(COMM) * COMM_Y2_MONTHS / COMM_MONTHS)
comm_amort_y3 = r0(Decimal(COMM) * 12 / COMM_MONTHS)
ni_y2_comm = at(COMM - comm_amort_y2)
fleet_dep_old = FLEET_COST // FLEET_LIFE
fleet_dep_new_straight = FLEET_COST // FLEET_NEW_TOTAL
staff_fleet_adj = fleet_dep_new_straight - fleet_dep_old    # staff charged this to Year 2
fleet_dep_y3 = (FLEET_COST - 2 * fleet_dep_old) // (FLEET_NEW_TOTAL - 2)
staff_comm_amort = r0(Decimal(COMM) * 12 / COMM_MONTHS)              # staff amortized a full year
staff_comm = at(COMM - staff_comm_amort)
staff_ni_y2 = NI_Y2_ORIG + staff_comm - at(staff_fleet_adj)
ni_y2 = NI_Y2_ORIG + ni_y2_comm + ni_y2_inv
re_jan1_y2 = RE_JAN1_Y2_ORIG + re_adj
ni_y3 = NI_Y3_DRAFT + at(inv_y2_diff)             # draft Y3 COGS used the FIFO beginning inventory
re_dec31_y2 = re_jan1_y2 + ni_y2 - DIV_Y2
re_dec31_y2_staff = RE_JAN1_Y2_ORIG + staff_ni_y2 - DIV_Y2
re_dec31_y3 = re_jan1_y2 + ni_y2 - DIV_Y2 + ni_y3 - DIV_Y3
ni_y2_no_inv = NI_Y2_ORIG + ni_y2_comm
ni_y2_cum = NI_Y2_ORIG + ni_y2_comm - at(inv_y2_diff)     # error: whole Dec 31, Year 2 difference to Year 2
assert (FLEET_COST - 2 * fleet_dep_old) % (FLEET_NEW_TOTAL - 2) == 0

memo4 = table(["Matter", "Facts"], [
    ("Inventory method", "Through Year 2, Corrieside costed inventory by FIFO. On January 1, Year 3, it adopted the weighted-average method for all inventory, because its new purchasing system tracks costs that way and management concluded that weighted-average better matches the way it prices its products. Corrieside's records allow it to compute weighted-average inventory at every prior year end (Exhibit 2)."),
    ("Sales commissions", f"On July 1, Year 2, Corrieside paid its sales staff commissions of {d(COMM)} for signing three-year service contracts that run from July 1, Year 2, to June 30, Year 5. The commissions were paid only because the contracts were signed, and Corrieside expects to recover them from the contract margins. Corrieside charged them to Year 2 expense. Its policy for costs of obtaining contracts that must be capitalized is to amortize them straight-line over the contract term; the contracts are not expected to be renewed."),
    ("Delivery fleet", f"Bought January 1, Year 1, for {d(FLEET_COST)}, depreciated straight-line over {FLEET_LIFE} years with no residual value. In January, Year 3, an engineering study based on two years of route data concluded that the fleet's total useful life will be {FLEET_NEW_TOTAL} years, with no residual value."),
    ("Equipment leasing", "In Year 3, Corrieside began leasing forklifts to customers, a business it had never been in, and adopted lessor accounting policies for those leases."),
])
inv4 = table(["December 31", "FIFO", "Weighted average"], [
    ("Year 1", amt(INV["Y1"][0]), amt(INV["Y1"][1])),
    ("Year 2", amt(INV["Y2"][0]), amt(INV["Y2"][1])),
    ("Year 3", amt(INV_Y3_FIFO), amt(INV_Y3_WA)),
])
draft4 = table(["Item", "Amount"], [
    ("Year 2 net income, as originally reported", amt(NI_Y2_ORIG)),
    (f"Staff adjustment: July 1, Year 2, sales commissions, net of tax (the staff's Year 2 amortization is {d(staff_comm_amort)})", amt(staff_comm)),
    (f"Staff adjustment: depreciation on the fleet under its revised {FLEET_NEW_TOTAL}-year life ({d(fleet_dep_new_straight)} a year, against {d(fleet_dep_old)} reported), net of tax", amt(-at(staff_fleet_adj))),
    ("Year 2 net income, as adjusted by the staff", amt(staff_ni_y2)),
    ("Retained earnings, January 1, Year 2, as originally reported", amt(RE_JAN1_Y2_ORIG)),
    ("Dividends declared: Year 2 / Year 3", f"{amt(DIV_Y2)} / {amt(DIV_Y3)}"),
    ("Year 3 net income, draft", amt(NI_Y3_DRAFT)),
])
draft4 += (f"\n\nThe Year 3 draft uses weighted-average cost for Year 3 purchases and for ending inventory ({d(INV_Y3_WA)}). Its cost of goods sold starts from the December 31, Year 2, inventory as reported in the Year 2 balance sheet. It includes {d(comm_amort_y3)} of commission amortization and fleet depreciation of {d(fleet_dep_y3)}, computed on the fleet's carrying amount at December 31, Year 2, as originally reported. The staff made no other adjustments. All net income and adjustment amounts in this exhibit are after income taxes.")

SIM4 = tbs(
    "far-tbs-accounting-changes-0001", "Accounting changes and error corrections", "Analysis",
    ["ASC 250-10-45-5 through 45-8 (retrospective application of a change in accounting principle)",
     "ASC 250-10-45-17 through 45-20 (changes in accounting estimate, prospective)",
     "ASC 250-10-45-23 and 45-24 (restatement for error corrections)",
     "ASC 250-10-20 (adopting a principle for transactions that previously did not occur is not a change in accounting principle)",
     "ASC 340-40-25-1 through 25-4 and 35-1 (incremental costs of obtaining a contract)"],
    "Year 3 comparative statements: a change, an error and an estimate",
    """Corrieside Supply Co. presents comparative income statements and statements of retained earnings for Years 2 and 3. Its Year 2 statements have been issued; its Year 3 statements have not. The controller's memo on four Year 3 matters is in Exhibit 1, inventory amounts are in Exhibit 2, and the staff's draft figures are in Exhibit 3. Corrieside's income tax rate is 25% for all years and all effects, including deferred taxes. Round every amount to the nearest dollar.""",
    [("Exhibit 1: Controller's memo on Year 3 matters", memo4),
     ("Exhibit 2: Inventory at December 31", inv4),
     ("Exhibit 3: Staff's draft figures", draft4)],
    [
        select("t1", "For each matter in Exhibit 1, indicate how Corrieside should report it.",
               ["Retrospective application to prior periods presented", "Restatement of prior periods presented",
                "Prospective application, from Year 3", "Not an accounting change or error correction"],
               [("r1", "Inventory method", "Retrospective application to prior periods presented"),
                ("r2", "Sales commissions", "Restatement of prior periods presented"),
                ("r3", "Delivery fleet", "Prospective application, from Year 3"),
                ("r4", "Equipment leasing", "Not an accounting change or error correction")],
               "FIFO to weighted average is a change in accounting principle, justified as preferable and with every period's effect determinable, so it is applied retrospectively. Expensing commissions that must be capitalized (incremental, expected to be recovered, amortization period over one year, so the practical expedient is not available) was an error in GAAP: restate Year 2. The fleet's life is an estimate revised for new information, so it is applied prospectively from Year 3; the staff's Year 2 adjustment is wrong. Adopting a policy for transactions that did not occur before is not an accounting change.",
               points=2),
        num("t2", "What net income should Corrieside report for Year 2 in its comparative statements?", ni_y2,
            f"Start from {d(NI_Y2_ORIG)} as reported. Commissions: Year 2 expense should have been amortization of {d(COMM)} × {COMM_Y2_MONTHS}/{COMM_MONTHS} = {d(comm_amort_y2)}, not {d(COMM)}: + ({d(COMM)} − {d(comm_amort_y2)}) × 75% = {d(ni_y2_comm)} (the staff amortized a full year, {d(staff_comm_amort)}, though the contracts began July 1, giving {d(staff_comm)}). Inventory: weighted average lowers December 31, Year 1, inventory by {d(inv_y1_diff)} and December 31, Year 2, inventory by {d(inv_y2_diff)}, so Year 2 cost of goods sold rises by {d(inv_y2_diff)} − {d(inv_y1_diff)} = {d(inv_y2_diff - inv_y1_diff)}: − {d(inv_y2_diff - inv_y1_diff)} × 75% = {d(-ni_y2_inv)}. The fleet change is prospective, so the staff's {d(at(staff_fleet_adj))} reduction is reversed. Year 2: {d(NI_Y2_ORIG)} + {d(ni_y2_comm)} − {d(-ni_y2_inv)} = {d(ni_y2)}. Charging the whole Year 2 inventory difference to Year 2 gives {d(ni_y2_cum)}.",
            points=2),
        num("t3", "What retained earnings should Corrieside report at December 31, Year 2, as adjusted, in its comparative statements?", re_dec31_y2,
            f"Opening balance: only the inventory change reaches periods before Year 2. Weighted average lowers December 31, Year 1, inventory by {d(inv_y1_diff)}, so cumulative income before Year 2 falls by {d(inv_y1_diff)} × 75% = {d(-re_adj)}: {d(RE_JAN1_Y2_ORIG)} − {d(-re_adj)} = {d(re_jan1_y2)}. Then + Year 2 net income as restated {d(ni_y2)} − dividends {d(DIV_Y2)} = {d(re_dec31_y2)}. The staff's figures give {d(re_dec31_y2_staff)}."),
        num("t4", "What net income should Corrieside report for Year 3?", ni_y3,
            f"The draft's Year 3 cost of goods sold starts from FIFO inventory of {d(INV['Y2'][0])}; under retrospective application, beginning inventory is the weighted-average {d(INV['Y2'][1])}. Cost of goods sold falls by {d(inv_y2_diff)}, and net income rises by {d(inv_y2_diff)} × 75% = {d(at(inv_y2_diff))}: {d(NI_Y3_DRAFT)} + {d(at(inv_y2_diff))} = {d(ni_y3)}. The draft's commission amortization ({d(COMM)} × 12/{COMM_MONTHS} = {d(comm_amort_y3)}) and fleet depreciation (({d(FLEET_COST)} − 2 × {d(fleet_dep_old)}) ÷ {FLEET_NEW_TOTAL - 2} remaining years = {d(fleet_dep_y3)}) are already correct.",
            points=2),
        num("t5", "What retained earnings should Corrieside report at December 31, Year 3?", re_dec31_y3,
            f"December 31, Year 2, as adjusted {d(re_dec31_y2)} + Year 3 net income {d(ni_y3)} − dividends {d(DIV_Y3)} = {d(re_dec31_y3)}."),
    ],
)


# ── Simulation 5: NFP contributions (III.C.b/f/g, Application) ─────────────────────────────────────────────────
MATCH_MAX, OTHER_GIFTS = 400000, 265000         # Halsall matches gifts for the nature center, up to the max
GRANT_MAX, GRANT_COSTS, GRANT_PAID = 180000, 117500, 90000
PROMISE_FACE, PROMISE_PV = 120000, 112800
ARCHITECT, TRAIL_VOLUNTEERS = 36000, 21000
SEEDLINGS = 23400
PASS_THROUGH = 50000
TICKETS, TICKET_PRICE, DINNER_FV = 300, 250, 90

match_recog = min(OTHER_GIFTS, MATCH_MAX)
gala_contrib = TICKETS * (TICKET_PRICE - DINNER_FV)
without = GRANT_COSTS + ARCHITECT + SEEDLINGS + gala_contrib
with_r = OTHER_GIFTS + match_recog + PROMISE_PV
receivables = match_recog + PROMISE_PV + (GRANT_COSTS - GRANT_PAID)
without_err_gala = without - gala_contrib + TICKETS * TICKET_PRICE
with_err_full_match = OTHER_GIFTS + MATCH_MAX + PROMISE_PV
recv_err_face = match_recog + PROMISE_FACE + (GRANT_COSTS - GRANT_PAID)

log5 = table(["Date (Year 1)", "Source", "Detail"], [
    ("February 10", "Halsall Foundation", f"Written pledge to match, dollar for dollar, gifts from other donors for Ashgrove's planned nature center received by June 30, Year 2, up to {d(MATCH_MAX)}. Halsall will pay the matched amount on July 15, Year 2; it owes nothing for gifts it has not matched. Construction of the nature center begins in Year 2."),
    ("March – December", "Various donors", f"Cash gifts for the nature center totaling {d(OTHER_GIFTS)}, all of which qualify for Halsall's match."),
    ("March 1", "State Department of Natural Resources", f"Grant to reimburse allowable costs of restoring Tillet Marsh, a preserve Ashgrove owns and opens to the public, up to {d(GRANT_MAX)} of costs incurred in Years 1 and 2. The state receives no goods or services from Ashgrove under the grant, and pays only for costs incurred. Ashgrove incurred {d(GRANT_COSTS)} of allowable costs in Year 1, and the state had paid {d(GRANT_PAID)} of them by December 31."),
    ("June 6", "Kittering Nursery", f"Donated native plant seedlings with a fair value of {d(SEEDLINGS)}, all planted in the marsh restoration in Year 1."),
    ("September 20", "Annual gala", f"{TICKETS} tickets sold at {d(TICKET_PRICE)} each. The dinner served had a fair value of {d(DINNER_FV)} a guest; Ashgrove paid the caterer separately."),
    ("October 4", "Pellow Design", f"An architect designed the nature center without charge. Ashgrove would otherwise have hired an architect; the fee would have been {d(ARCHITECT)}. Pellow placed no conditions or restrictions on the gift."),
    ("Throughout Year 1", "Community volunteers", f"Led weekend trail walks. At local wage rates, their time was worth {d(TRAIL_VOLUNTEERS)}."),
    ("November 12", "Ostrander family", f"{d(PASS_THROUGH)} in cash, which the donors directed Ashgrove to give to Marlbank Food Pantry, an unrelated organization. Ashgrove may not use it for anything else, and it paid Marlbank in January, Year 2."),
    ("December 15", "Rhona Tullis, board member", f"Signed, unconditional promise to give {d(PROMISE_FACE)} on January 31, Year 3, with no use specified. Its present value, measured under Ashgrove's policy, is {d(PROMISE_PV)}."),
])
policy5 = table(["Policy", "Detail"], [
    ("Restrictions met in the same year", "Ashgrove reports donor-restricted contributions whose restrictions are met in the year they are recognized as contributions without donor restrictions. The policy also covers conditional contributions whose conditions and restrictions are met in the same year."),
    ("Marsh restoration", "Restoration costs (planting, earthwork and monitoring) are program expenses as incurred; the restoration creates no asset Ashgrove capitalizes."),
    ("Promises to give", "Unconditional promises due in more than one year are measured at present value; promises due within one year are measured at the amount expected to be collected, without discounting. Ashgrove expects to collect every promise in full."),
    ("Long-lived assets", "Gifts restricted to acquiring or building long-lived assets are released from restriction when the asset is placed in service."),
])

SIM5 = tbs(
    "far-tbs-nfp-contributions-0001", "Revenue recognition", "Application",
    ["ASC 958-605-25-2 and 25-8 through 25-13 (contributions; promises to give; conditional promises and barriers)",
     "ASC 958-605-25-16 (contributed services)",
     "ASC 958-605-25-23 through 25-25 and 958-20 (agency transactions; transfers to a specified beneficiary)",
     "ASC 958-605-30-6 and 958-310-35 (measurement of promises to give)",
     "ASC 958-205-45 and 958-605-45-4 through 45-5 (donor restrictions; restrictions met in the same period; implied time restrictions)",
     "ASC 958-225-45-17 (special events with an exchange element)"],
    "Year 1 contributions at a conservation not-for-profit",
    """Ashgrove River Conservancy, a not-for-profit entity, is preparing its Year 1 statement of activities. Exhibit 1 is its development office's log of Year 1 gifts and grants, and Exhibit 2 gives its accounting policies. No donor has variance power over any gift. Exhibit 1 lists every contribution and grant Ashgrove received in Year 1. Round every amount to the nearest dollar.""",
    [("Exhibit 1: Development office log, Year 1", log5),
     ("Exhibit 2: Accounting policies", policy5)],
    [
        select("t1", "For each item, indicate how Ashgrove should report it in its Year 1 statement of activities.",
               ["Contribution revenue without donor restrictions", "Contribution revenue with donor restrictions", "No contribution revenue in Year 1"],
               [("r1", "Halsall Foundation pledge", "Contribution revenue with donor restrictions"),
                ("r2", "State marsh restoration grant", "Contribution revenue without donor restrictions"),
                ("r3", "Pellow Design architect services", "Contribution revenue without donor restrictions"),
                ("r4", "Trail walk volunteers", "No contribution revenue in Year 1"),
                ("r5", "Ostrander family gift for Marlbank", "No contribution revenue in Year 1"),
                ("r6", "Rhona Tullis promise", "Contribution revenue with donor restrictions")],
               "Halsall's pledge is conditional on a barrier (matching gifts) with a right of release for unmatched amounts; it becomes unconditional as each matching gift arrives, so the matched part is recognized now, restricted to the nature center. The state grant is a contribution (the state receives no commensurate value) conditioned on incurring allowable costs; as costs are incurred the condition and the purpose restriction are met in the same year, which the policy reports as without donor restrictions. The architect's services require specialized skills Ashgrove would otherwise buy and create a nonfinancial asset, so they are recognized. The trail walk volunteers meet neither test. The Ostrander gift passes through to a specified beneficiary, so Ashgrove is an agent and records a liability, not revenue. The Tullis promise is due in a later year, so it carries an implied time restriction.",
               points=3),
        num("t2", "What total contribution revenue without donor restrictions should Ashgrove report for Year 1?", without,
            f"State grant: {d(GRANT_COSTS)} of costs incurred (not the {d(GRANT_MAX)} ceiling or the {d(GRANT_PAID)} paid). Architect: {d(ARCHITECT)}. Seedlings: {d(SEEDLINGS)}. Gala: the contribution is the ticket price less the dinner's fair value, {TICKETS} × ({d(TICKET_PRICE)} − {d(DINNER_FV)}) = {d(gala_contrib)}; the other {d(TICKETS * DINNER_FV)} is exchange revenue. Total {d(GRANT_COSTS)} + {d(ARCHITECT)} + {d(SEEDLINGS)} + {d(gala_contrib)} = {d(without)}. Counting the full ticket price gives {d(without_err_gala)}.",
            points=2),
        num("t3", "What total contribution revenue with donor restrictions should Ashgrove report for Year 1?", with_r,
            f"Gifts from various donors for the nature center, {d(OTHER_GIFTS)}; Halsall's matched amount, {d(match_recog)} (not the {d(MATCH_MAX)} maximum, which is still conditional for the unmatched part); the Tullis promise at present value, {d(PROMISE_PV)}. Total {d(with_r)}. Recognizing Halsall's full pledge gives {d(with_err_full_match)}.",
            points=2),
        num("t4", "What total receivables from contributions and grants should Ashgrove report at December 31, Year 1?", receivables,
            f"Halsall's matched pledge {d(match_recog)} (due within one year, not discounted) + the Tullis promise at present value {d(PROMISE_PV)} + the state's unpaid reimbursement {d(GRANT_COSTS)} − {d(GRANT_PAID)} = {d(GRANT_COSTS - GRANT_PAID)}; total {d(receivables)}. Using the Tullis promise's face amount gives {d(recv_err_face)}."),
    ],
)


# ── Simulation 6: operating lease with an incentive, an index, variable payments and a remeasurement (III.F.d) ─
BASE, TERM, RENEW_YEARS, RENEW_RENT = 120000, 5, 3, 132000
INCENTIVE, IDC, LEGAL_STAFF = 40000, 6000, 3500          # TI reimbursement (incentive); payment to the old tenant; inspection (not IDC)
CPI0, CPI1, CPI2 = Decimal("100.0"), Decimal("103.5"), Decimal("106.0")
CAM = {1: 18600, 2: 21300}
R1, R2 = Decimal("0.06"), Decimal("0.07")
CLEAN_ROOM = 480000


def due(rate, n):
    """Present value of an annuity due of 1, to five places (the exhibit's factors)."""
    return sum(Decimal(1) / (1 + rate) ** k for k in range(n)).quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP)


F = {(r, n): due(r, n) for r in (R1, R2) for n in (3, 5, 6, 8)}
L0 = r0(BASE * F[(R1, TERM)])                 # liability at commencement, before the first payment
rou0 = L0 - INCENTIVE + IDC
single = (BASE * TERM - INCENTIVE + IDC) // TERM
assert (BASE * TERM - INCENTIVE + IDC) % TERM == 0
int1 = r0((L0 - BASE) * R1)
L1 = L0 - BASE + int1
rou1 = rou0 - (single - int1)
cost1 = single + CAM[1]
pay2 = r0(BASE * CPI1 / CPI0)
var2 = pay2 - BASE
int2 = r0((L1 - BASE) * R1)
L2_pre = L1 - BASE + int2
rou2_pre = rou1 - (single - int2)
cost2 = single + var2 + CAM[2]
pay3 = r0(BASE * CPI2 / CPI0)
L2 = r0(pay3 * F[(R2, 3)] + RENEW_RENT * (F[(R2, 6)] - F[(R2, 3)]))
rou2 = rou2_pre + (L2 - L2_pre)
remaining_pay = pay3 * 3 + RENEW_RENT * RENEW_YEARS
cost3_a = Decimal(remaining_pay + rou2 - L2) / (3 + RENEW_YEARS)
cost3_b = Decimal(BASE * 2 + remaining_pay - INCENTIVE + IDC - 2 * single) / (3 + RENEW_YEARS)   # ASC 842-20-25-8
assert cost3_a == cost3_b, (cost3_a, cost3_b)
cost3 = r0(cost3_a)
# Errors, for the explanations
rou0_legal = rou0 + LEGAL_STAFF
L2_old_rate = r0(pay3 * F[(R1, 3)] + RENEW_RENT * (F[(R1, 6)] - F[(R1, 3)]))
L2_no_cpi = r0(BASE * F[(R2, 3)] + RENEW_RENT * (F[(R2, 6)] - F[(R2, 3)]))
cost2_no_var = single + CAM[2]

lease6 = table(["Term", "Detail"], [
    ("Premises", "Production space in a multi-tenant industrial building, leased by Kerrow Precision Parts, a public business entity, from Stellan Properties"),
    ("Term", f"{TERM} years from January 1, Year 1, noncancelable. Kerrow may renew once for {RENEW_YEARS} more years by giving notice before January 1, Year 5."),
    ("Rent", f"Paid each January 1 in advance. The Year 1 rent is {d(BASE)}. Each later year's rent through Year 5 is {d(BASE)} × (the consumer price index at the preceding December 31 ÷ {CPI0}, the index at commencement). Rent during the renewal term is fixed at {d(RENEW_RENT)} a year."),
    ("Common area maintenance", "Kerrow reimburses Stellan for its share of the building's actual maintenance costs each year."),
    ("Fit-out", f"Kerrow fits out the space at its own cost and owns the fit-out. Stellan agrees to reimburse {d(INCENTIVE)} of the fit-out costs; at commencement Kerrow had already spent more than that, and Stellan paid the {d(INCENTIVE)} on February 10, Year 1."),
    ("Other costs", f"To free the space for Kerrow, Kerrow paid the previous tenant {d(IDC)} on January 1, Year 1, to end its lease early, a payment Kerrow would not have made without this lease. Before deciding to lease, Kerrow paid an engineer {d(LEGAL_STAFF)} to inspect the building, a fee owed whether or not Kerrow signed."),
])
events6 = table(["Date or period", "Information"], [
    ("January 1, Year 1", f"Kerrow classified the lease as an operating lease and concluded that it was not reasonably certain to renew: the renewal rent was expected to approximate market, and Kerrow had no significant improvements in the space. Kerrow's incremental borrowing rate was {R1 * 100:.0f}%; Stellan's implicit rate is not known to Kerrow."),
    ("Consumer price index", f"December 31, Year 1: {CPI1}. December 31, Year 2: {CPI2}. Kerrow paid the rent due January 1, Year 2, on time."),
    ("Common area maintenance billed and paid", f"Year 1: {d(CAM[1])}. Year 2: {d(CAM[2])}."),
    ("Year 2", f"Kerrow built a clean room in the space at a cost of {d(CLEAN_ROOM)}, completed December 20, Year 2. The clean room has a 10-year useful life and cannot be removed; building another one elsewhere would cost about {d(CLEAN_ROOM + 40000)}. Kerrow's board approved the clean room on a plan to operate it in this space through at least Year 8. Market rent for comparable space is now about {d(RENEW_RENT + 33000)} a year."),
    ("December 31, Year 2", f"Kerrow's incremental borrowing rate is now {R2 * 100:.0f}%."),
    ("Policy elections", "For leases of real estate, Kerrow accounts for each lease component and its nonlease components together as a single lease component."),
])
factors6 = table(["Periods", f"{R1 * 100:.0f}%", f"{R2 * 100:.0f}%"],
                 [(n, F[(R1, n)], F[(R2, n)]) for n in (3, 5, 6, 8)])
factors6 = "Present value of an annuity due of 1 (payments at the start of each period):\n\n" + factors6

SIM6 = tbs(
    "far-tbs-operating-lease-0001", "Lessee accounting", "Application",
    ["ASC 842-20-30-1 and 30-5 (initial measurement of the lease liability and right-of-use asset; incentives; initial direct costs)",
     "ASC 842-10-30-9 and 30-10 (initial direct costs, including payments to an existing tenant to end its lease)",
     "ASC 842-10-30-5 (lease incentives reduce lease payments) and 842-10-15-37 (combining lease and nonlease components)",
     "ASC 842-10-30-5 and 842-10-35-5 (variable payments that depend on an index: initial measurement and remeasurement)",
     "ASC 842-10-35-1 and 35-4 (reassessing the lease term; updating the discount rate)",
     "ASC 842-20-25-6, 25-8 and 35-3 through 35-5 (operating lease cost; remaining cost after remeasurement)"],
    "Operating lease of production space: two years and a remeasurement",
    """Kerrow Precision Parts closes its books each December 31. Exhibit 1 summarizes its lease of production space, Exhibit 2 gives information from the first two years, and Exhibit 3 gives present value factors. Kerrow makes any reassessment of the lease as of December 31, Year 2; the lease is an operating lease throughout. Measure the fit-out reimbursement at the full amount, ignoring the time until it is paid. Treat December 31 and the following January 1 as the same date for discounting. Round every amount to the nearest dollar, including interest each year.""",
    [("Exhibit 1: Lease summary", lease6),
     ("Exhibit 2: Lease information, Years 1 and 2", events6),
     ("Exhibit 3: Present value factors", factors6)],
    [
        num("t1", "What amount should Kerrow recognize as its right-of-use asset at commencement on January 1, Year 1?", rou0,
            f"Lease liability: {d(BASE)} × {F[(R1, TERM)]} = {d(L0)} (rounded), the present value of five payments due in advance at {R1 * 100:.0f}%, measured with the index at commencement. Right-of-use asset: {d(L0)} − the {d(INCENTIVE)} fit-out reimbursement, a lease incentive receivable at commencement + the {d(IDC)} paid to the previous tenant, an initial direct cost = {d(rou0)}. The inspection fee was owed whether or not the lease was signed, so it is not an initial direct cost (including it gives {d(rou0_legal)})."),
        num("t2", "What total lease cost should Kerrow recognize for Year 1?", cost1,
            f"Straight-line single lease cost: ({TERM} × {d(BASE)} − {d(INCENTIVE)} + {d(IDC)}) ÷ {TERM} = {d(single)}. Because Kerrow combines lease and nonlease components, the common area maintenance payments are variable lease payments, recognized as variable lease cost when incurred: {d(CAM[1])}. Total {d(single)} + {d(CAM[1])} = {d(cost1)}."),
        num("t3", "What is the carrying amount of Kerrow's right-of-use asset at December 31, Year 1?", rou1,
            f"Liability after the January 1 payment: {d(L0)} − {d(BASE)} = {d(L0 - BASE)}; Year 1 accretion at {R1 * 100:.0f}% = {d(int1)} (rounded). The asset's amortization is the single lease cost less the accretion: {d(single)} − {d(int1)} = {d(single - int1)}. {d(rou0)} − {d(single - int1)} = {d(rou1)}."),
        num("t4", "What total lease cost should Kerrow recognize for Year 2?", cost2,
            f"Single lease cost {d(single)}. The January 1, Year 2, rent is {d(BASE)} × {CPI1}/{CPI0} = {d(pay2)}; the {d(var2)} above the {d(BASE)} in the lease liability is variable lease cost, since an index change alone doesn't trigger remeasurement. Common area maintenance {d(CAM[2])}. Total {d(single)} + {d(var2)} + {d(CAM[2])} = {d(cost2)}. Leaving out the index increase gives {d(cost2_no_var)}."),
        num("t5", "What lease liability should Kerrow report at December 31, Year 2?", L2,
            f"Building a costly, immovable clean room is a significant event within Kerrow's control that makes renewal reasonably certain, so Kerrow reassesses the lease term to eight years and remeasures the liability for the six remaining payments, with an updated {R2 * 100:.0f}% rate. The remeasurement updates the index-based payments to the current index: {d(BASE)} × {CPI2}/{CPI0} = {d(pay3)} for Years 3–5, then {d(RENEW_RENT)} for Years 6–8. Liability = {d(pay3)} × {F[(R2, 3)]} + {d(RENEW_RENT)} × ({F[(R2, 6)]} − {F[(R2, 3)]}) = {d(L2)} (rounded). Keeping the {R1 * 100:.0f}% rate gives {d(L2_old_rate)}; keeping the {d(BASE)} payments gives {d(L2_no_cpi)}. Before remeasurement the liability was {d(L2_pre)}.",
            points=2),
        num("t6", "What is the carrying amount of Kerrow's right-of-use asset at December 31, Year 2?", rou2,
            f"Before remeasurement: Year 2 accretion is ({d(L1)} − {d(BASE)}) × {R1 * 100:.0f}% = {d(int2)} (rounded), so the liability is {d(L2_pre)} and the asset is {d(rou1)} − ({d(single)} − {d(int2)}) = {d(rou2_pre)}. The remeasurement adjusts the asset by the change in the liability, {d(L2)} − {d(L2_pre)} = {d(L2 - L2_pre)}: {d(rou2_pre)} + {d(L2 - L2_pre)} = {d(rou2)}."),
        num("t7", "What single (straight-line) lease cost should Kerrow recognize for Year 3? Exclude variable lease cost.", cost3,
            f"After a remeasurement, the remaining cost is spread straight-line over the remaining term. Remaining cost = remaining lease payments + right-of-use asset − lease liability = ({d(pay3 * 3)} + {d(RENEW_RENT * RENEW_YEARS)}) + {d(rou2)} − {d(L2)} = {d(r0(cost3_a * 6))}, over {3 + RENEW_YEARS} years = {d(cost3)} (rounded). Equivalently, total lease payments ({d(BASE)} × 2 + {d(remaining_pay)} − {d(INCENTIVE)} incentive) + {d(IDC)} initial direct costs − {d(2 * single)} cost recognized in Years 1–2, over {3 + RENEW_YEARS} years."),
    ],
)

ITEMS = [SIM1, SIM2, SIM3, SIM4, SIM5, SIM6]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
    for it in ITEMS:
        pts = sum(t["points"] for t in it["tasks"])
        assert 6 <= pts <= 10, (it["id"], pts)
        assert len(it["exhibits"]) >= 2, it["id"]
        with open(os.path.join(out, it["id"] + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(it, f, sort_keys=False, allow_unicode=True, width=100)
        print(it["id"], it["blueprint"]["skill"], len(it["tasks"]), "tasks,", pts, "points")
    print("contingencies", liab_correct, pretax_change, rp_excess, commit_loss)
    print("subsequent", ni_correct, cl_correct, wc, hfs_loss)
    print("revenue", alloc, rev_y1, contract_bal)
    print("changes", ni_y2, re_jan1_y2, ni_y3, re_dec31_y3, staff_ni_y2)
    print("nfp", without, with_r, receivables)
    print("lease", L0, rou0, cost1, rou1, cost2, L2_pre, L2, rou2_pre, rou2, cost3_a, F)
