"""FAR batch 15 — Area II (Select Balance Sheet Accounts), 13 items written from scratch, all numeric
with three variants each.

Plan: 9 Analysis items spread over six Area II Analysis tasks (II.A.b bank reconciliation x2, II.A.c
investigate unreconciled cash x2, II.B.c receivables rollforward x2, II.C.c inventory rollforward x2,
II.D.f PP&E rollforward x1), each changing at least two component events from every existing item on its
task and using a stem format none of them uses. 4 Application items on the four of these Area II tasks
with the fewest existing items chosen for topic spread: II.F.c (cloud computing), II.G.c (exit/disposal
liabilities), II.H.1c (bond interest, with detachable warrants) and II.H.2a (debt covenant, interest
coverage). Target mix: 9 Analysis / 4 Application, all Area II. Scope and skill tags follow the AICPA CPA
Exam Blueprints effective January 2026.

Every numeric answer and distractor is computed in code (Decimal, rounded half up). Each item is a
builder: parameter set 0 is the reviewed item and sets 1-3 become its variants; every family moves the
key's letter across versions; parameter set 0 shows the distractor for the item's central twist.

Run: python scripts/batches/far-batch-15.py [--dry-run]
"""
import json
import os
import re
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AN, AP, attach_variants, audit, finalize, fix_articles, variant, write_items  # noqa: E402
from variants import m, pick, rd  # noqa: E402

A2 = "Area II — Select Balance Sheet Accounts"
NOTE = "Batch 15. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
SCRATCH = os.environ.get("B15_SCRATCH")


def family(id, area, topic, skill, refs, build, params, twist, asof=None):
    """An item built from parameter set 0, with sets 1-3 kept for its variants.

    `twist` names the pool distractor for the item's central twist; parameter set 0 must show it."""
    assert twist in params[0]["use"], f"{id}: version 0 doesn't show the central-twist distractor {twist}"
    base = build(params[0])
    review = dict(status="reviewed", references=refs, notes=NOTE)
    if asof:
        review["asOf"] = asof
    it = dict(id=id, type="mcq", blueprint=dict(section="FAR", area=area, topic=topic, skill=skill),
              review=review, **base)
    it["stem"], it["explanation"] = fix_articles(it["stem"]), fix_articles(it["explanation"])
    for c in it["choices"]:
        c["text"], c["rationale"] = fix_articles(c["text"]), fix_articles(c["rationale"])
    it["_variants"] = [build(p) for p in params[1:]]
    for k, v in enumerate([it] + it["_variants"]):
        repeats(f"{id} v{k}", v)
        spacing(f"{id} v{k}", v)
    return it


def repeats(label, v):
    """Report any dollar amount that appears more than once in a stem, or a choice that equals a stem amount."""
    amts = re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", v["stem"])
    dup = sorted({a for a in amts if amts.count(a) > 1})
    if dup:
        print(f"REPEAT {label}: stem repeats {', '.join(dup)}", file=sys.stderr)
    for c in v["choices"]:
        for a in re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", c["text"]):
            if a in amts:
                print(f"REPEAT {label}: choice {a} equals a stem amount", file=sys.stderr)


def spacing(label, v):
    """Report two choices whose leading amounts are within 0.4% of each other."""
    vals = []
    for c in v["choices"]:
        mm = re.match(r"^\$?([\d,]+(?:\.\d+)?)", c["text"])
        if mm:
            vals.append(float(mm.group(1).replace(",", "")))
    vals.sort()
    for a, b in zip(vals, vals[1:]):
        if b - a < 0.004 * b:
            print(f"CLOSE {label}: {a:,.2f} and {b:,.2f}", file=sys.stderr)


def short(name):
    return name.split()[0]


def distinct(pool, key):
    """No pool value may equal the key or another pool value; amounts must be positive."""
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"
    assert all(not v.startswith("$-") and not v.startswith("$0 ") and v != "$0" for v in vals), vals
    nums = [float(re.match(r"^\$?([\d,]+(?:\.\d+)?)", v).group(1).replace(",", "")) for v in vals]
    assert len(set(nums)) == len(nums), f"two choices share an amount: {vals}"


def build(pool, key, use):
    distinct({k: pool[k] for k in use}, key)
    return pick(pool, key, use)


def ratio(x):
    """A ratio to two decimal places, no dollar sign."""
    return str(rd(x, "0.01"))


# ── Area II Analysis: II.A.b reconcile the bank balance to the general ledger ────────────────


def bank_recon_stop(p):
    co, s = p["co"], short(p["co"])
    key_v = p["BB"] + p["DIT"] - p["OC"]
    fee = p["CCg"] - p["CCn"]
    GB = key_v - p["NR"] + fee - p["SP"]
    assert fee > 0 and GB > 0
    pool = {
        "no_nr": (m(key_v - p["NR"]), f"Leaves out the {m(p['NR'])} note receivable the bank collected for {s}, including interest, which the books haven't recorded."),
        "no_fee": (m(key_v + fee), f"Leaves the {m(p['CCg'])} card-sale deposit at its gross amount. The processor deposited only {m(p['CCn'])} after its {m(fee)} discount fee, which {s} hasn't recorded."),
        "no_stop": (m(key_v - p["SP"]), f"Leaves the {m(p['SP'])} stopped check recorded as a disbursement, even though the bank never paid it."),
        "draft": (m(GB + p["NR"]), f"Records only the {m(p['NR'])} note collected, without correcting the card-sale deposit or reversing the stopped check."),
    }
    key = (m(key_v), f"Correct. {m(p['BB'])} + {m(p['DIT'])} − {m(p['OC'])} (bank side) = {m(GB)} + {m(p['NR'])} − {m(fee)} + {m(p['SP'])} (book side).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""While preparing {co}'s December 31 bank reconciliation, the accountant finds that the bank collected a {m(p['NR'])} note receivable on {s}'s behalf, including interest, which hasn't been recorded in the cash account; that a {m(p['CCg'])} batch of credit-card sales was deposited by the processor net of its {m(fee)} discount fee, though {s} recorded the deposit at the full {m(p['CCg'])} sale amount; and that check #{p['chk']}, for {m(p['SP'])}, on which {s} placed a stop-payment order after a vendor dispute, is still recorded as a disbursement even though the bank never paid it. The bank statement also lists deposits in transit of {m(p['DIT'])} and outstanding checks (other than #{p['chk']}) totaling {m(p['OC'])}. If the bank statement shows a balance of {m(p['BB'])} and the general ledger cash account shows {m(GB)}, what is {s}'s correct cash balance at December 31?""",
        choices, ans,
        f"""The bank side is {m(p['BB'])} + {m(p['DIT'])} − {m(p['OC'])} = {m(key_v)}. On the book side: the {m(p['NR'])} note the bank collected is added; the card-sale deposit was recorded at {m(p['CCg'])} but only {m(p['CCn'])} was actually received, so cash is reduced by the {m(fee)} fee; and the stopped check never left the bank, so its {m(p['SP'])} disbursement is reversed (added back): {m(GB)} + {m(p['NR'])} − {m(fee)} + {m(p['SP'])} = {m(key_v)}.""",
    )


def bank_recon_error(p):
    co, s = p["co"], short(p["co"])
    key_v = p["BB"] + p["DIT"] - p["OC"] - p["BE"]
    GB = key_v - p["INT"]
    assert GB > 0
    pool = {
        "no_be": (m(key_v + p["BE"]), f"Leaves the {m(p['BE'])} deposit that the bank credited to {s}'s account in error in the bank balance. It belongs to another of the bank's customers and must be removed."),
        "no_int": (m(GB), f"Leaves out the {m(p['INT'])} of interest the bank credited on the account, which {s} hasn't recorded."),
        "noadj_wrong": (m(key_v + p["STALE"]), f"Removes the {m(p['STALE'])} check {s} wrote and mailed on December 29 from the outstanding list because the payee hadn't cashed it by year-end. A check mailed before year-end stays outstanding until it clears, however long that takes; no adjustment is needed."),
        "draft": (m(key_v + p["BE"] - p["INT"]), f"Corrects neither the bank's {m(p['BE'])} misdirected deposit nor the uncredited {m(p['INT'])} of interest."),
    }
    key = (m(key_v), f"Correct. {m(p['BB'])} + {m(p['DIT'])} − {m(p['OC'])} − {m(p['BE'])} (bank side) = {m(GB)} + {m(p['INT'])} (book side).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31 bank statement shows a balance of {m(p['BB'])}, which includes a {m(p['BE'])} deposit the bank credited to {s}'s account in error; the deposit belongs to another of the bank's customers. The statement also shows {m(p['INT'])} of interest the bank credited on the account, which {s} hasn't recorded. Deposits in transit total {m(p['DIT'])} and outstanding checks total {m(p['OC'])}, including a {m(p['STALE'])} check {s} wrote and mailed to a supplier on December 29 that the supplier had not yet cashed by December 31. {s}'s general ledger cash account shows {m(GB)}. What is {s}'s correct cash balance at December 31?""",
        choices, ans,
        f"""Bank side: {m(p['BB'])} + {m(p['DIT'])} − {m(p['OC'])} − {m(p['BE'])} (removing the bank's misdirected deposit) = {m(key_v)}. Book side: {m(GB)} + {m(p['INT'])} (the uncredited interest) = {m(key_v)}. The {m(p['STALE'])} check mailed before year-end properly stays on the outstanding list until the bank pays it; the delay in cashing it, by itself, calls for no adjustment.""",
    )


# ── Area II Analysis: II.A.c investigate unreconciled cash balances ──────────────────────────


def cash_unrecon_wire(p):
    co, s = p["co"], short(p["co"])
    key_v = p["ABB"]
    ABK = key_v + p["WIRE"] + p["FEE"] - p["DUP"]
    pool = {
        "no_wire": (m(key_v + p["WIRE"]), f"Keeps the {m(p['WIRE'])} wire transfer as a collection. The customer's bank sent it to another company's account, so {s} never received it."),
        "no_fee": (m(key_v + p["FEE"]), f"Leaves out the {m(p['FEE'])} fee the bank charged for honoring {s}'s stop-payment request, which hasn't been recorded."),
        "no_dup": (m(key_v - p["DUP"]), f"Leaves the {m(p['DUP'])} petty-cash replenishment check recorded twice in the cash disbursements journal."),
        "draft": (m(ABK), f"Accepts the book side's {m(ABK)}, which keeps the misdirected wire, omits the stop-payment fee and leaves the duplicate disbursement."),
    }
    key = (m(key_v), f"Correct. {m(ABK)} − {m(p['WIRE'])} − {m(p['FEE'])} + {m(p['DUP'])} = {m(key_v)}, agreeing with the adjusted bank balance.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s bank reconciliation, after deposits in transit and outstanding checks, shows an adjusted bank balance of {m(key_v)} at November 30. Its general ledger cash account, after recording the bank's service charges and collections already identified, shows {m(ABK)}, an unreconciled difference of {m(ABK - key_v)}. Investigating, the controller finds: a {m(p['WIRE'])} wire transfer that a customer's remittance advice said was sent to pay its account was actually misdirected by the customer's bank to another company's account, and was never credited to {s}'s account, though the collections department recorded it as received; a {m(p['FEE'])} fee the bank charged for honoring {s}'s stop-payment request on an earlier check has not been recorded; and a {m(p['DUP'])} petty-cash replenishment check was recorded twice in the cash disbursements journal. What is {s}'s correct cash balance at November 30?""",
        choices, ans,
        f"""The adjusted bank balance, after deposits in transit and outstanding checks, is already correct at {m(key_v)}. On the book side: the {m(p['WIRE'])} wire was never actually received, since the customer's bank sent it to the wrong account, so it comes out; the {m(p['FEE'])} stop-payment fee reduces cash and hasn't been recorded; and the duplicate {m(p['DUP'])} disbursement overstated total disbursements, so it is added back: {m(ABK)} − {m(p['WIRE'])} − {m(p['FEE'])} + {m(p['DUP'])} = {m(key_v)}.""",
    )


def cash_unrecon_je(p):
    co, s = p["co"], short(p["co"])
    key_v = p["ABB"]
    two_dep = 2 * p["DEP"]
    ABK = key_v + p["INSUR"] - two_dep + p["CF"]
    pool = {
        "no_insur": (m(key_v + p["INSUR"]), f"Leaves out the {m(p['INSUR'])} insurance premium the bank auto-debited under a standing authorization, which {s} hasn't recorded."),
        "no_je": (m(key_v - p["DEP"]), f"Adds back only the {m(p['DEP'])} deposit itself. Because the deposit was recorded in the disbursements journal instead of the receipts journal, cash was reduced when it should have been increased, a {m(two_dep)} swing that must be corrected in full."),
        "no_cf": (m(key_v + p["CF"]), f"Leaves the {m(p['CF'])} counterfeit bill in the recorded deposit. The bank didn't credit it, and {s} hasn't yet written it off."),
        "draft": (m(ABK), f"Accepts the book side's {m(ABK)}, which keeps the insurance debit unrecorded, corrects the misposted deposit by only half its effect and leaves the counterfeit bill in cash."),
    }
    key = (m(key_v), f"Correct. {m(ABK)} + {m(p['INSUR'])} − {m(two_dep)} + {m(p['CF'])} = {m(key_v)}, agreeing with the adjusted bank balance.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s bank reconciliation shows an adjusted bank balance of {m(key_v)} at October 31. Its general ledger cash account shows {m(ABK)}, an unreconciled difference of {m(ABK - key_v)}. Investigating, the controller finds: a {m(p['INSUR'])} insurance premium that the bank auto-debited under a standing authorization has not been recorded; a {m(p['DEP'])} cash deposit was recorded in the cash disbursements journal instead of the cash receipts journal; and a {m(p['CF'])} bill included in an earlier deposit turned out to be counterfeit, which the bank did not credit and which {s} has not yet written off. What is {s}'s correct cash balance at October 31?""",
        choices, ans,
        f"""The {m(p['INSUR'])} auto-debited premium reduces book cash and hasn't been recorded. Recording the {m(p['DEP'])} deposit in the disbursements journal instead of the receipts journal reduced cash when it should have increased it, a {m(two_dep)} swing to correct. The {m(p['CF'])} counterfeit bill was never real cash and must be written off. {m(ABK)} + {m(p['INSUR'])} − {m(two_dep)} + {m(p['CF'])} = {m(key_v)}.""",
    )


# ── Area II Analysis: II.B.c prepare a rollforward of trade receivables ──────────────────────


def ar_rollforward_recourse(p):
    co, s = p["co"], short(p["co"])
    E_draft = p["B"] + p["Rv"] - p["Cc"] - p["Wo"]
    key_v = E_draft + p["Rec"] - p["BH"] - p["Reb"]
    pool = {
        "no_rec": (m(key_v - p["Rec"]), f"Leaves the {m(p['Rec'])} of receivables factored with recourse out of the rollforward. Because {s} kept the risk of nonpayment, the transfer doesn't qualify as a sale; the receivables, and an offsetting liability, stay on the books."),
        "no_bh": (m(key_v + p["BH"]), f"Keeps the {m(p['BH'])} bill-and-hold order as a completed sale. Control hadn't passed to the customer, so it isn't a receivable."),
        "no_reb": (m(key_v + p["Reb"]), f"Leaves the {m(p['Reb'])} volume rebate netted against cash collected. Recording it there understated collections applied to customer accounts by {m(p['Reb'])}, so ending receivables is {m(p['Reb'])} too high."),
        "draft": (m(E_draft), f"Accepts the draft's {m(E_draft)}, which removed the recourse-factored receivables as if sold, counted the bill-and-hold order as a sale and left the rebate netted against collections."),
    }
    key = (m(key_v), f"Correct. {m(E_draft)} + {m(p['Rec'])} − {m(p['BH'])} − {m(p['Reb'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{s}'s staff drafted this Year 2 rollforward of the accounts receivable control account: January 1 balance {m(p['B'])}; plus credit sales {m(p['Rv'])}; less cash collected from customers {m(p['Cc'])}; less accounts written off {m(p['Wo'])}; December 31 balance {m(E_draft)}. All of {s}'s sales are on account. Reviewing the draft, the controller finds: {m(p['Rec'])} of receivables that {s} factored to a bank with recourse, for which the draft removed the receivables and recorded the cash as a sale, though {s} remains obligated to repay the bank for any accounts the bank can't collect; a {m(p['BH'])} order that a customer asked {s} to invoice and hold in {s}'s warehouse until the customer's new store opens, which the draft recorded as a completed sale even though the goods haven't been shipped, aren't identified as the customer's and remain available to fill other orders; and a {m(p['Reb'])} volume rebate owed to a customer, which the draft's cash collected figure already reflects as a reduction, rather than as a separate liability. What amount of accounts receivable, before any allowance, should the corrected rollforward report for {s} at December 31, Year 2?""",
        choices, ans,
        f"""Receivables factored with recourse, where {s} keeps the risk of nonpayment, are accounted for as a secured borrowing, not a sale (ASC 860-10-40-5): the {m(p['Rec'])} stays in receivables (+ {m(p['Rec'])}). The bill-and-hold order doesn't meet the criteria for control to have passed (the goods aren't shipped, aren't identified as the customer's, and {s} can still redirect them), so it is removed (− {m(p['BH'])}). Netting the {m(p['Reb'])} rebate against cash collected understated collections applied to customer accounts, leaving ending receivables {m(p['Reb'])} too high (− {m(p['Reb'])}). Corrected balance = {m(E_draft)} + {m(p['Rec'])} − {m(p['BH'])} − {m(p['Reb'])} = {m(key_v)}.""",
    )


def ar_rollforward_creditbal(p):
    co, s = p["co"], short(p["co"])
    E_draft = p["B"] + p["Rv"] - p["Cc"] - p["Wo"]
    key_v = E_draft + p["CB"] - p["RA"]
    pool = {
        "no_cb": (m(key_v - p["CB"]), f"Leaves the {m(p['CB'])} of customer credit balances netted against the receivables total. Credit balances, from overpayments and returns, are a liability and aren't netted against other customers' debit balances."),
        "no_ra": (m(key_v + p["RA"]), f"Leaves out the {m(p['RA'])} credit memo for goods a customer returned in December, which wasn't recorded until January."),
        "wr_wrong": (m(key_v + p["WR"]), f"Adds the {m(p['WR'])} recovery of a previously written-off account back into receivables. Because the recovery was recorded directly as a credit to bad debt expense rather than by reinstating the account and then recording its collection, it never touched accounts receivable and needs no correction here."),
        "draft": (m(E_draft), f"Accepts the draft's {m(E_draft)}, which nets the customer credit balances against receivables and omits the December return."),
    }
    key = (m(key_v), f"Correct. {m(E_draft)} + {m(p['CB'])} − {m(p['RA'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""All of {s}'s sales are on credit. Its accounts receivable control account began Year 2 at {m(p['B'])}; credit sales for the year were {m(p['Rv'])}, cash collected from customers was {m(p['Cc'])}, and {m(p['Wo'])} of accounts were written off, which a staff accountant used to arrive at a preliminary December 31 figure of {m(E_draft)}. Examining that figure, the internal auditor notes three things: customer accounts with credit balances, from overpayments and returns, totaling {m(p['CB'])}, were netted against the debit balances of other customers rather than reported separately; a {m(p['RA'])} credit memo for goods a customer returned on December 29, logged by the shipping department that day, wasn't entered in the accounting records until the memo was processed in January; and a {m(p['WR'])} recovery of an account written off in an earlier year, paid in cash by the customer in December, was recorded as a direct credit to bad debt expense. For {s}, what should corrected accounts receivable, before any allowance, be at December 31, Year 2?""",
        choices, ans,
        f"""Credit balances in customer accounts are a liability, not a reduction of other customers' receivables, so the {m(p['CB'])} is added back (+ {m(p['CB'])}). The December return is a Year 2 event and must be recorded in Year 2, reducing receivables (− {m(p['RA'])}). The recovery, recorded as a direct credit to bad debt expense rather than by reinstating the account and then recording its collection, never ran through accounts receivable, so it needs no correction here. Corrected balance = {m(E_draft)} + {m(p['CB'])} − {m(p['RA'])} = {m(key_v)}.""",
    )


# ── Area II Analysis: II.C.c prepare a rollforward of inventory ──────────────────────────────


def inv_rollforward_consign_in(p):
    co, s = p["co"], short(p["co"])
    E_draft = p["B"] + p["P"] - p["C"]
    key_v = E_draft - p["CI"] + p["COL"] + p["PD"]
    pool = {
        "no_ci": (m(key_v + p["CI"]), f"Keeps the {m(p['CI'])} of goods {s} holds on consignment from a supplier in inventory. Title to consigned-in goods stays with the consignor until {s} sells them; they aren't {s}'s inventory."),
        "no_col": (m(key_v - p["COL"]), f"Leaves out the {m(p['COL'])} of inventory {s} pledged as collateral for a loan. Pledging goods as security doesn't transfer ownership, so they remain {s}'s inventory."),
        "no_pd": (m(key_v - p["PD"]), f"Leaves purchases recorded net of the {m(p['PD'])} of discounts {s} didn't take. Because {s} paid after the discount period, the {m(p['PD'])} is a financing cost, not a permanent reduction of inventory cost."),
        "draft": (m(E_draft), f"Accepts the draft's {m(E_draft)}, which includes the consigned-in goods, excludes the pledged inventory and records purchases net of the unclaimed discount."),
    }
    key = (m(key_v), f"Correct. {m(E_draft)} − {m(p['CI'])} + {m(p['COL'])} + {m(p['PD'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{s}'s perpetual inventory records show a Year 2 rollforward of beginning inventory {m(p['B'])}, purchases {m(p['P'])}, and cost of goods sold {m(p['C'])}, for a draft December 31 balance of {m(E_draft)}. Reviewing the count and the purchase records, the controller finds: the count includes {m(p['CI'])} of goods a supplier shipped to {s} on consignment, which {s} may return unsold; {m(p['COL'])} of {s}'s own inventory, pledged as collateral for a bank loan, was removed from the inventory account when the loan was obtained; and purchases are recorded under the net method, so {m(p['PD'])} of discounts on invoices {s} paid after the discount period, and so never took, reduced the recorded cost of goods still on hand. What inventory should the corrected rollforward report at December 31, Year 2?""",
        choices, ans,
        f"""Goods held on consignment from a supplier aren't {s}'s inventory until {s} sells them (ASC 606-10-55-80), so the {m(p['CI'])} comes out. Pledging inventory as loan collateral doesn't change who owns it, so the {m(p['COL'])} of pledged goods belongs back in inventory. Discounts lost because an invoice was paid late are a financing cost, not a reduction of inventory cost, so the {m(p['PD'])} is restored. Corrected inventory = {m(E_draft)} − {m(p['CI'])} + {m(p['COL'])} + {m(p['PD'])} = {m(key_v)}.""",
    )


def inv_rollforward_bonded(p):
    co, s = p["co"], short(p["co"])
    E_draft = p["B"] + p["P"] - p["C"]
    key_v = E_draft - p["SP"] + p["BW"] - p["RB"]
    pool = {
        "no_sp": (m(key_v + p["SP"]), f"Keeps the {m(p['SP'])} of raw materials ruined in an equipment malfunction at full cost. Abnormal spoilage is expensed as incurred, not carried in inventory."),
        "no_bw": (m(key_v - p["BW"]), f"Leaves out the {m(p['BW'])} of goods sitting in the customs bonded warehouse. Title passed to {s} when the goods were shipped, so they are {s}'s inventory even though they hadn't yet cleared customs and weren't in the physical count."),
        "no_rb": (m(key_v + p["RB"]), f"Ignores the {m(p['RB'])} volume purchase rebate {s} earned by year-end but hadn't yet billed. The rebate reduces the cost of the inventory still on hand."),
        "draft": (m(E_draft), f"Accepts the draft's {m(E_draft)}, which keeps the spoiled materials at cost, omits the bonded-warehouse goods and ignores the rebate."),
    }
    key = (m(key_v), f"Correct. {m(E_draft)} − {m(p['SP'])} + {m(p['BW'])} − {m(p['RB'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{s}'s perpetual inventory records show a Year 2 rollforward of beginning inventory {m(p['B'])}, purchases {m(p['P'])}, and cost of goods sold {m(p['C'])}, for a draft December 31 balance of {m(E_draft)}. Reviewing the count, the controller finds: {m(p['SP'])} of raw materials ruined in an equipment malfunction during the year, included in the count at full cost; {m(p['BW'])} of goods purchased under terms that passed title to {s} at shipment, which were sitting in a customs bonded warehouse awaiting clearance at year-end and so weren't included in the physical count; and a {m(p['RB'])} volume purchase rebate, for which {s} met the purchase threshold before year-end but which the supplier hadn't yet billed or recorded. What inventory should the corrected rollforward report at December 31, Year 2?""",
        choices, ans,
        f"""Abnormal spoilage from an equipment malfunction is expensed as incurred, not capitalized in inventory (ASC 330-10-30), so the {m(p['SP'])} comes out. The bonded-warehouse goods belong to {s} once title passed at shipment, even though they hadn't cleared customs and weren't physically counted, so the {m(p['BW'])} is added. The {m(p['RB'])} rebate, earned before year-end, reduces the cost of the inventory still on hand even though it hasn't been billed. Corrected inventory = {m(E_draft)} − {m(p['SP'])} + {m(p['BW'])} − {m(p['RB'])} = {m(key_v)}.""",
    )


# ── Area II Analysis: II.D.f prepare a rollforward of PP&E ───────────────────────────────────


def ppe_rollforward_cost(p):
    co, s = p["co"], short(p["co"])
    E_draft = p["B"] + p["P"] - p["Disp"]
    key_v = E_draft + p["ST"] - p["REMOVE"]
    pool = {
        "no_st": (m(key_v - p["ST"]), f"Leaves the {m(p['ST'])} of sales tax and delivery charges on the new machine expensed. These costs are necessary to bring the asset to its intended location and condition and are part of its cost."),
        "reclass_wrong": (m(key_v - p["RECLASS"]), f"Removes the {m(p['RECLASS'])} resurfacing cost entirely because it belongs in a separate land improvements account rather than buildings. Moving it between property, plant and equipment accounts doesn't change the {m(p['RECLASS'])} total reported for property, plant and equipment."),
        "no_remove": (m(key_v + p["REMOVE"]), f"Keeps the {m(p['REMOVE'])} insurance premium to cover the new equipment during shipment capitalized. Insuring an asset in transit is a period cost, not part of the asset's cost."),
        "draft": (m(E_draft), f"Accepts the draft's {m(E_draft)}, which expenses the sales tax and delivery charges and capitalizes the shipping insurance."),
    }
    key = (m(key_v), f"Correct. {m(E_draft)} + {m(p['ST'])} − {m(p['REMOVE'])}; the {m(p['RECLASS'])} resurfacing cost changes which account it's in, not the total.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{s}'s staff prepared this Year 2 rollforward of total property, plant and equipment, at cost: January 1 balance {m(p['B'])}; additions {m(p['P'])}; disposals ({m(p['Disp'])}); December 31 balance {m(E_draft)}. Reviewing the capital expenditures report, the controller finds: {m(p['ST'])} of sales tax and delivery charges on a new machine, paid in cash, was charged to a shipping and tax expense account instead of being added to the machine's cost; a {m(p['RECLASS'])} cost to resurface the parking lot was added to the buildings account as an addition, though {s} carries land improvements in a separate account depreciated over a shorter life; and a {m(p['REMOVE'])} premium to insure a new piece of equipment during shipment was added to the equipment's cost. What should the corrected rollforward report as total property, plant and equipment, at cost, at December 31, Year 2?""",
        choices, ans,
        f"""Sales tax and delivery charges are necessary to bring an asset to its intended location and condition and are capitalized (ASC 360-10-30), so the {m(p['ST'])} is added. Moving the {m(p['RECLASS'])} resurfacing cost from buildings to land improvements changes which account it sits in, but not the {m(p['RECLASS'])} total for property, plant and equipment as a whole, so no dollar change is needed. Insurance on an asset in transit is a period cost and is removed from the equipment's cost (− {m(p['REMOVE'])}). Corrected total = {m(E_draft)} + {m(p['ST'])} − {m(p['REMOVE'])} = {m(key_v)}.""",
    )


# ── Area II Application ───────────────────────────────────────────────────────────────────────


def cloud_computing_asset(p):
    co, s = p["co"], short(p["co"])
    N = p["T1"] + p["T2"]
    months = 13 - p["GLM"]
    annual = rd(D(p["INT"]) / N)
    key_v = p["INT"] - rd(annual * months / 12)
    annual_t1 = rd(D(p["INT"]) / p["T1"])
    no_renewal = p["INT"] - rd(annual_t1 * months / 12)
    combo = p["INT"] + p["DM"]
    annual_combo = rd(D(combo) / N)
    capitalize_dm = combo - rd(annual_combo * months / 12)
    full_year = p["INT"] - annual
    no_amort = D(p["INT"])
    assert months < 12
    pool = {
        "no_renewal": (m(no_renewal), f"Amortizes the implementation costs only over the {p['T1']}-year initial term, ignoring the {p['T2']}-year renewal. Because {s} is reasonably certain to renew, the amortization period is the {N}-year combined term, the same period used to decide the arrangement isn't a lease."),
        "capitalize_dm": (m(capitalize_dm), f"Capitalizes the {m(p['DM'])} of data conversion costs along with the implementation costs. Data conversion costs are expensed as incurred, not capitalized, under ASC 350-40."),
        "full_year": (m(full_year), f"Amortizes a full year's amount, {m(annual)}, instead of the {months} months since the software became ready for its intended use on {p['glive']}, Year 1."),
        "no_amort": (m(no_amort), f"Reports the implementation costs at their full {m(p['INT'])}, with no amortization for Year 1."),
    }
    key = (m(key_v), f"Correct. {m(p['INT'])} − ({m(annual)} × {months}/12).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} runs its inventory management entirely through a vendor's cloud platform under a {p['T1']}-year contract that began January 1, Year 1; {s} never takes possession of the underlying software, and management is confident {s} will exercise the contract's renewal option for another {p['T2']} years once the initial term ends, since switching platforms would be disruptive. {s} did not begin using the system until {p['glive']}, Year 1, once setup was finished; getting there cost {m(p['EV'])} to compare and select a vendor, {m(p['INT'])} to configure the system and build and test its interfaces, {m(p['DM'])} to clean up and load historical data, and {m(p['TRAIN'])} to train staff on the new system. {s} amortizes capitalized implementation costs straight-line over the period it benefits from the arrangement. What amount should {s} report as its capitalized cloud computing implementation asset, net of amortization, at December 31, Year 1?""",
        choices, ans,
        f"""Under ASC 350-40, as amended by ASU 2018-15, only the costs of configuring, coding and testing the hosting arrangement's interfaces are capitalized; selecting a vendor ({m(p['EV'])}) is a preliminary-stage cost and training ({m(p['TRAIN'])}) and data conversion ({m(p['DM'])}) are expensed as incurred, whether or not the project is likely to succeed. (ASU 2025-06's revisions to internal-use software capitalization give the same result for a hosting arrangement like this one.) The capitalized {m(p['INT'])} is amortized over the {N}-year period {s} benefits from the arrangement, the initial {p['T1']}-year term plus the {p['T2']}-year renewal {s} is reasonably certain to exercise, straight-line from {p['glive']}: {m(annual)} a year, or {m(rd(annual * months / 12))} for the {months} months remaining in Year 1. Net asset = {m(p['INT'])} − {m(rd(annual * months / 12))} = {m(key_v)}.""",
    )


def exit_cost_timing(p):
    co, s = p["co"], short(p["co"])
    prorate_wrong = rd(D(p["A"]) * p["elapsed"] / p["total"])
    key_v = D(p["A"])
    pool = {
        "prorate_wrong": (m(prorate_wrong), f"Accrues only {p['elapsed']}/{p['total']} of the {m(p['A'])} of termination benefits, as though employees must render future service to earn them. Because the benefit formula pays employees the same amount whether or not they stay until the facility closes, {s} recognizes the whole {m(p['A'])} at the communication date."),
        "incl_k": (m(key_v + p["K"]), f"Also accrues the {m(p['K'])} fee to cancel the equipment maintenance contract early. {s} will keep using the contracted service until the facility closes, so that cost isn't recognized until {s} ceases using the right under the contract."),
        "incl_rel": (m(key_v + p["REL"]), f"Also accrues the {m(p['REL'])} estimated cost of relocating equipment to another facility. Costs associated with an exit activity, other than one-time termination benefits and contract termination costs, are recognized in the period they are incurred, not when the exit plan is communicated."),
        "incl_both": (m(key_v + p["K"] + p["REL"]), f"Also accrues both the {m(p['K'])} contract termination fee and the {m(p['REL'])} relocation cost. Neither is recognized at the communication date."),
    }
    key = (m(key_v), f"Correct. The full {m(p['A'])} of termination benefits, recognized at the communication date because no significant future service is required to earn them.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On {p['comm']}, Year 1, {co}'s board approves a plan to close a distribution center on {p['close']}, Year 2, and communicates the plan to the center's {p['n']} employees that day. Under the plan, each terminated employee will receive a severance payment based on years of service, a total of {m(p['A'])}, whether the employee stays until the center closes or leaves immediately; {s} expects no significant retention problem and plans no further communication. {s} will also pay a {m(p['K'])} fee to cancel an equipment maintenance contract once it stops using the service, which won't happen until the center closes, and expects to spend {m(p['REL'])} relocating equipment to another facility once the move actually takes place. What liability for exit costs should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""A one-time termination benefit is recognized in full at the communication date when, as here, employees aren't required to render significant future service to receive it (ASC 420-10-25-4): the full {m(p['A'])} is a liability once the plan is communicated. A contract termination cost is recognized when the contract is terminated or, if earlier, when the entity ceases using the right under the contract (ASC 420-10-25-11); {s} keeps using the maintenance service until closure, so the {m(p['K'])} fee isn't yet a liability. Other costs associated with an exit activity, such as the {m(p['REL'])} of relocation, are recognized as incurred (ASC 420-10-25-15), not when the plan is announced. Exit-cost liability at December 31, Year 1 = {m(key_v)}.""",
    )


def bonds_warrants_interest(p):
    co, s = p["co"], short(p["co"])
    i = D(p["MR"]) / 100 / 2
    coupon = rd(D(p["F"]) * D(p["SR"]) / 100 / 2)
    denom = p["BFV"] + p["FVW"]
    CV0 = rd(D(p["PR"]) * p["BFV"] / denom)
    int1 = rd(CV0 * i)
    CV1 = CV0 + (int1 - coupon)
    int2 = rd(CV1 * i)
    key_v = int1 + int2
    CV0f = D(p["PR"])
    int1f = rd(CV0f * i)
    CV1f = CV0f + (int1f - coupon)
    int2f = rd(CV1f * i)
    face_alloc = int1f + int2f
    CV0s = rd(D(p["PR"]) * p["FVW"] / denom)
    int1s = rd(CV0s * i)
    CV1s = CV0s + (int1s - coupon)
    int2s = rd(CV1s * i)
    swap_alloc = int1s + int2s
    stated_only = coupon * 2
    no_second_amort = int1 * 2
    pool = {
        "face_alloc": (m(face_alloc), f"Treats the full {m(p['PR'])} of proceeds as the bonds' initial carrying amount. Because the warrants are detachable and trade separately, part of the proceeds, allocated by relative fair value, belongs to additional paid-in capital, not the bonds."),
        "swap_alloc": (m(swap_alloc), f"Allocates to the bonds the {m(p['FVW'])} share of proceeds that belongs to the warrants, and to the warrants the bonds' {m(p['BFV'])} share. The relative-fair-value method allocates proceeds in proportion to each component's own fair value."),
        "stated_only": (m(stated_only), f"Uses the two {m(coupon)} stated interest payments with no discount amortization. Allocating part of the proceeds to the warrants creates a bond discount, which the effective interest method amortizes into interest expense."),
        "no_second_amort": (m(no_second_amort), f"Uses the {m(CV0)} carrying amount for both semiannual periods. The carrying amount rises as the discount amortizes each period, to {m(CV1)} for the second period, raising its interest."),
    }
    key = (m(key_v), f"Correct. {m(CV0)} × {p['MR']}%/2 + {m(CV1)} × {p['MR']}%/2.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} issues {m(p['F'])} face amount of ten-year, {p['SR']}% bonds, paying interest each June 30 and December 31, together with detachable stock warrants, for total cash proceeds of {m(p['PR'])}. Immediately after issuance, the warrants trade separately at a total fair value of {m(p['FVW'])}, and the bonds alone, without the warrants, would have sold to yield {p['MR']}%, compounded semiannually, for {m(p['BFV'])}. {s} allocates the proceeds between the bonds and the warrants by relative fair value, uses the effective interest method for the bonds, and rounds to the nearest dollar at each step. What total interest expense should {s} recognize on the bonds for Year 1?""",
        choices, ans,
        f"""Because the warrants are detachable, proceeds are allocated between the bonds and the warrants by relative fair value (ASC 470-20-25-2): bonds' share = {m(p['PR'])} × {m(p['BFV'])}/({m(p['BFV'])} + {m(p['FVW'])}) = {m(CV0)}, with the remaining {m(D(p['PR']) - CV0)} credited to additional paid-in capital for the warrants. The {m(coupon)} semiannual coupon is {m(D(p['F']) * D(p['SR']) / 100)} a year on the face amount. First-period interest = {m(CV0)} × {p['MR']}%/2 = {m(int1)}, increasing the carrying amount to {m(CV1)}; second-period interest = {m(CV1)} × {p['MR']}%/2 = {m(int2)}. Total Year 1 interest expense = {m(int1)} + {m(int2)} = {m(key_v)}.""",
    )


def debt_covenant_ratio(p):
    co, s = p["co"], short(p["co"])
    EBIT_adj = p["NI"] + p["IE"] + p["TAX"] - p["GAIN"] + p["REST"]
    key_v = D(EBIT_adj) / p["IE"]
    incl_gain = D(p["NI"] + p["IE"] + p["TAX"] + p["REST"]) / p["IE"]
    excl_rest = D(p["NI"] + p["IE"] + p["TAX"] - p["GAIN"]) / p["IE"]
    no_tax_add = D(p["NI"] + p["IE"] - p["GAIN"] + p["REST"]) / p["IE"]
    draft = D(p["NI"] + p["IE"] + p["TAX"]) / p["IE"]
    pool = {
        "incl_gain": (ratio(incl_gain), f"Includes the {m(p['GAIN'])} gain on the sale of equipment in earnings before interest and taxes. The loan agreement's definition excludes gains and losses on asset sales."),
        "excl_rest": (ratio(excl_rest), f"Leaves the {m(p['REST'])} restructuring charge as a reduction of earnings before interest and taxes. The agreement's definition adds restructuring charges back."),
        "no_tax_add": (ratio(no_tax_add), f"Leaves out the {m(p['TAX'])} of income tax expense. The agreement defines earnings before interest and taxes as net income plus interest expense and income taxes, before the gain and restructuring adjustments."),
        "draft": (ratio(draft), f"Uses net income plus interest and taxes, {m(p['NI'] + p['IE'] + p['TAX'])}, without excluding the gain or adding back the restructuring charge."),
    }
    key = (ratio(key_v), f"Correct. ({m(p['NI'])} + {m(p['IE'])} + {m(p['TAX'])} − {m(p['GAIN'])} + {m(p['REST'])}) ÷ {m(p['IE'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s loan agreement requires its ratio of earnings before interest and taxes to interest expense to be at least {p['min']} at each year-end, where earnings before interest and taxes is defined as net income plus interest expense and income taxes, excluding gains and losses on sales of long-lived assets and excluding restructuring charges. For Year 1, {s} reports net income of {m(p['NI'])}, interest expense of {m(p['IE'])}, and income tax expense of {m(p['TAX'])}. Net income includes a {m(p['GAIN'])} gain on the sale of idle equipment and a {m(p['REST'])} restructuring charge for closing an underperforming store. What interest coverage ratio should {s} report for the covenant test, rounded to two decimal places?""",
        choices, ans,
        f"""Starting from net income, add back interest expense and income taxes, then apply the agreement's own adjustments: exclude the {m(p['GAIN'])} gain on the equipment sale, and add back the {m(p['REST'])} restructuring charge. Earnings before interest and taxes, as defined = {m(p['NI'])} + {m(p['IE'])} + {m(p['TAX'])} − {m(p['GAIN'])} + {m(p['REST'])} = {m(EBIT_adj)}. Ratio = {m(EBIT_adj)} ÷ {m(p['IE'])} = {ratio(key_v)}.""",
    )


FAMILIES = [
    ("far-cash-bank-reconciliation-0006", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice"],
     bank_recon_stop, [
        dict(co="Perranporth Marine Co.", BB=52400, DIT=5800, OC=9150, NR=1350, CCg=1620, CCn=1530, SP=420, chk="498", use=["no_nr", "no_fee", "no_stop"]),
        dict(co="Mullion Boatworks Co.", BB=68900, DIT=7200, OC=11450, NR=980, CCg=2040, CCn=1980, SP=560, chk="512", use=["no_nr", "no_stop", "draft"]),
        dict(co="Falmouth Chandlery Co.", BB=81200, DIT=6400, OC=13700, NR=1150, CCg=1890, CCn=1860, SP=480, chk="305", use=["no_fee", "no_stop", "draft"]),
        dict(co="Padstow Marine Supply Co.", BB=45600, DIT=4900, OC=8300, NR=860, CCg=1480, CCn=1420, SP=350, chk="221", use=["no_nr", "no_fee", "draft"]),
     ], "no_stop"),
    ("far-cash-bank-reconciliation-0007", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (errors by the bank and by the depositor)"],
     bank_recon_error, [
        dict(co="Mevagissey Trawler Co.", BB=61200, DIT=4300, OC=8750, BE=610, INT=85, STALE=940, use=["no_be", "no_int", "noadj_wrong"]),
        dict(co="Porthallow Fisheries Co.", BB=74500, DIT=5600, OC=10200, BE=780, INT=110, STALE=1150, use=["no_be", "noadj_wrong", "draft"]),
        dict(co="Looe Harbour Supply Co.", BB=58300, DIT=3900, OC=7650, BE=520, INT=70, STALE=860, use=["no_int", "noadj_wrong", "draft"]),
        dict(co="Newlyn Fish Market Co.", BB=86700, DIT=6100, OC=12400, BE=690, INT=95, STALE=1020, use=["no_be", "no_int", "draft"]),
     ], "noadj_wrong"),
    ("far-cash-unreconciled-0004", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (errors by the bank and by the depositor)"],
     cash_unrecon_wire, [
        dict(co="Tywardreath Supply Co.", ABB=58900, WIRE=2300, FEE=180, DUP=1050, use=["no_wire", "no_fee", "no_dup"]),
        dict(co="Mevagissey Fisheries Co.", ABB=74500, WIRE=3100, FEE=220, DUP=1380, use=["no_fee", "no_dup", "draft"]),
        dict(co="Polruan Chandlery Co.", ABB=49200, WIRE=1850, FEE=140, DUP=920, use=["no_wire", "no_dup", "draft"]),
        dict(co="Fowey Harbour Traders Co.", ABB=83600, WIRE=2950, FEE=260, DUP=1520, use=["no_wire", "no_fee", "draft"]),
     ], "no_wire"),
    ("far-cash-unreconciled-0005", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (errors by the bank and by the depositor)"],
     cash_unrecon_je, [
        dict(co="St Mawes Marine Co.", ABB=67400, INSUR=410, DEP=980, CF=150, use=["no_insur", "no_je", "no_cf"]),
        dict(co="Portloe Seafood Co.", ABB=54900, INSUR=320, DEP=740, CF=110, use=["no_je", "no_cf", "draft"]),
        dict(co="Gorran Haven Fisheries Co.", ABB=72100, INSUR=460, DEP=1050, CF=190, use=["no_insur", "no_cf", "draft"]),
        dict(co="Veryan Bay Traders Co.", ABB=46300, INSUR=270, DEP=610, CF=95, use=["no_insur", "no_je", "draft"]),
     ], "no_je"),
    ("far-receivables-rollforward-0006", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "ASC 860-10-40 (transfers of receivables failing sale accounting: secured borrowing)", "ASC 606-10-25 (transfer of control; bill-and-hold arrangements)"],
     ar_rollforward_recourse, [
        dict(co="Tregony Supply Co.", B=520000, Rv=3150000, Cc=3080000, Wo=26000, Rec=72000, BH=48000, Reb=19000, use=["no_rec", "no_bh", "draft"]),
        dict(co="Portreath Traders Co.", B=410000, Rv=2460000, Cc=2395000, Wo=21000, Rec=58000, BH=36000, Reb=15000, use=["no_bh", "no_reb", "draft"]),
        dict(co="Perranarworthal Co.", B=630000, Rv=3820000, Cc=3725000, Wo=31000, Rec=85000, BH=55000, Reb=23000, use=["no_rec", "no_reb", "draft"]),
        dict(co="St Agnes Wholesale Co.", B=355000, Rv=2080000, Cc=2030000, Wo=17000, Rec=46000, BH=29000, Reb=12000, use=["no_rec", "no_bh", "no_reb"]),
     ], "no_rec"),
    ("far-receivables-rollforward-0007", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "ASC 326-20-35 (write-offs and recoveries)", "ASC 606-10-25 (cutoff for sales returns)"],
     ar_rollforward_creditbal, [
        dict(co="Mylor Yacht Supply Co.", B=480000, Rv=2920000, Cc=2865000, Wo=24000, CB=15000, RA=9000, WR=6000, use=["no_cb", "no_ra", "wr_wrong"]),
        dict(co="Flushing Marine Co.", B=365000, Rv=2210000, Cc=2168000, Wo=19000, CB=11000, RA=7000, WR=5000, use=["no_cb", "wr_wrong", "draft"]),
        dict(co="Gweek Boatyard Co.", B=545000, Rv=3340000, Cc=3268000, Wo=28000, CB=18000, RA=11000, WR=8000, use=["no_ra", "wr_wrong", "draft"]),
        dict(co="Constantine Chandlers Co.", B=298000, Rv=1860000, Cc=1819000, Wo=15000, CB=9000, RA=6000, WR=4000, use=["no_cb", "no_ra", "draft"]),
     ], "wr_wrong"),
    ("far-inventory-rollforward-0006", A2, "Inventory", AN,
     ["ASC 330-10 (inventory)", "ASC 606-10-55 (consignment arrangements)"],
     inv_rollforward_consign_in, [
        dict(co="Pendeen Hardware Co.", B=210000, P=1480000, C=1395000, CI=34000, COL=52000, PD=12000, use=["no_ci", "no_col", "no_pd"]),
        dict(co="Trewellard Supply Co.", B=165000, P=1120000, C=1055000, CI=26000, COL=40000, PD=9000, use=["no_col", "no_pd", "draft"]),
        dict(co="St Just Builders Supply Co.", B=295000, P=1860000, C=1742000, CI=44000, COL=66000, PD=15000, use=["no_ci", "no_pd", "draft"]),
        dict(co="Botallack Timber Co.", B=138000, P=940000, C=882000, CI=19000, COL=31000, PD=7000, use=["no_ci", "no_col", "draft"]),
     ], "no_ci"),
    ("far-inventory-rollforward-0007", A2, "Inventory", AN,
     ["ASC 330-10 (inventory; abnormal costs)", "ASC 330-10-30 (purchase rebates and cost of inventory)"],
     inv_rollforward_bonded, [
        dict(co="Hayle Industrial Co.", B=340000, P=2150000, C=2015000, SP=21000, BW=38000, RB=16000, use=["no_sp", "no_bw", "no_rb"]),
        dict(co="Camborne Metals Co.", B=410000, P=2480000, C=2322000, SP=25000, BW=44000, RB=20000, use=["no_bw", "no_rb", "draft"]),
        dict(co="Redruth Forge Co.", B=255000, P=1640000, C=1538000, SP=16000, BW=29000, RB=12000, use=["no_sp", "no_rb", "draft"]),
        dict(co="Helston Steelworks Co.", B=298000, P=1920000, C=1801000, SP=18000, BW=33000, RB=14000, use=["no_sp", "no_bw", "draft"]),
     ], "no_bw"),
    ("far-ppe-rollforward-0006", A2, "Property, plant and equipment", AN,
     ["ASC 360-10-30 (cost of property, plant and equipment: sales tax and delivery charges capitalized)", "ASC 360-10-25 (insurance and other period costs expensed)"],
     ppe_rollforward_cost, [
        dict(co="Zelah Fabrication Co.", B=2850000, P=640000, Disp=85000, ST=28000, RECLASS=52000, REMOVE=15000, use=["no_st", "reclass_wrong", "no_remove"]),
        dict(co="Goonhavern Castings Co.", B=1960000, P=430000, Disp=58000, ST=19000, RECLASS=36000, REMOVE=10000, use=["reclass_wrong", "no_remove", "draft"]),
        dict(co="Indian Queens Metalworks Co.", B=3340000, P=790000, Disp=102000, ST=34000, RECLASS=61000, REMOVE=18000, use=["no_st", "no_remove", "draft"]),
        dict(co="Bugle Quarry Equipment Co.", B=2240000, P=510000, Disp=66000, ST=22000, RECLASS=41000, REMOVE=12000, use=["no_st", "reclass_wrong", "draft"]),
     ], "reclass_wrong"),
    ("far-intangibles-cloud-computing-0002", A2, "Intangible assets", AP,
     ["ASC 350-40 (internal-use software; implementation costs of a hosting arrangement that is a service contract)", "ASU 2018-15 (customer's accounting for implementation costs in a cloud computing arrangement)", "ASU 2025-06 (targeted improvements to internal-use software; same result here)"],
     cloud_computing_asset, [
        dict(co="Perrancombe Logistics Co.", T1=4, T2=2, INT=216000, EV=22000, DM=30000, TRAIN=16000, GLM=7, glive="July 1", use=["no_renewal", "capitalize_dm", "full_year"]),
        dict(co="Trebarwith Freight Co.", T1=5, T2=3, INT=256000, EV=26000, DM=32000, TRAIN=18000, GLM=4, glive="April 1", use=["capitalize_dm", "full_year", "no_amort"]),
        dict(co="Delabole Transport Co.", T1=3, T2=3, INT=198000, EV=19000, DM=27000, TRAIN=14000, GLM=10, glive="October 1", use=["no_renewal", "full_year", "no_amort"]),
        dict(co="Bodmin Haulage Co.", T1=4, T2=4, INT=264000, EV=24000, DM=36000, TRAIN=17000, GLM=5, glive="May 1", use=["no_renewal", "capitalize_dm", "no_amort"]),
     ], "no_renewal"),
    ("far-exit-costs-0003", A2, "Payables and accrued liabilities", AP,
     ["ASC 420-10-25 (one-time employee termination benefits: recognition when future service isn't required; contract termination costs; other associated costs)"],
     exit_cost_timing, [
        dict(co="Wadebridge Freight Co.", A=840000, K=65000, REL=38000, elapsed=2, total=5, n=70, comm="November 1", close="April 1", use=["prorate_wrong", "incl_k", "incl_rel"]),
        dict(co="Launceston Carriers Co.", A=615000, K=48000, REL=27000, elapsed=3, total=6, n=55, comm="October 1", close="April 1", use=["incl_k", "incl_rel", "incl_both"]),
        dict(co="Bideford Shipping Co.", A=980000, K=72000, REL=44000, elapsed=4, total=7, n=85, comm="September 1", close="April 1", use=["prorate_wrong", "incl_rel", "incl_both"]),
        dict(co="Barnstaple Transit Co.", A=725000, K=55000, REL=31000, elapsed=1, total=4, n=60, comm="December 1", close="April 1", use=["prorate_wrong", "incl_k", "incl_both"]),
     ], "prorate_wrong"),
    ("far-bonds-premium-0002", A2, "Debt (Notes and bonds payable)", AP,
     ["ASC 470-20-25 (debt issued with detachable stock warrants: relative fair value allocation)", "ASC 835-30 (interest method)"],
     bonds_warrants_interest, [
        dict(co="Padstow Energy Corp.", F=1000000, SR=5, PR=955000, FVW=50000, BFV=950000, MR="7.4", use=["face_alloc", "stated_only", "no_second_amort"]),
        dict(co="Bodmin Power Corp.", F=800000, SR=6, PR=776000, FVW=40000, BFV=780000, MR="8.6", use=["swap_alloc", "stated_only", "no_second_amort"]),
        dict(co="Liskeard Utilities Corp.", F=1200000, SR=4, PR=1134000, FVW=60000, BFV=1140000, MR="6.8", use=["face_alloc", "swap_alloc", "stated_only"]),
        dict(co="Saltash Energy Corp.", F=600000, SR=7, PR=584000, FVW=30000, BFV=585000, MR="9.4", use=["face_alloc", "stated_only", "no_second_amort"]),
     ], "stated_only"),
    ("far-debt-covenant-0003", A2, "Debt (Debt covenant compliance)", AP,
     ["Debt covenant compliance: interest coverage ratio as defined in the loan agreement"],
     debt_covenant_ratio, [
        dict(co="Wadebridge Components Inc.", NI=1240000, IE=310000, TAX=360000, GAIN=85000, REST=140000, min="4.00", use=["incl_gain", "excl_rest", "draft"]),
        dict(co="Truro Fabrication Inc.", NI=980000, IE=245000, TAX=285000, GAIN=62000, REST=108000, min="4.25", use=["excl_rest", "no_tax_add", "draft"]),
        dict(co="Penzance Castings Inc.", NI=1460000, IE=365000, TAX=420000, GAIN=96000, REST=172000, min="4.10", use=["incl_gain", "no_tax_add", "draft"]),
        dict(co="Bodmin Machine Works Inc.", NI=870000, IE=218000, TAX=252000, GAIN=54000, REST=95000, min="4.00", use=["incl_gain", "excl_rest", "no_tax_add"]),
     ], "draft"),
]


def blind_files(items, scratch):
    """Stems and lettered choices only, for the blind verifier, plus a separate key file."""
    lines, keys = ["# FAR batch 15: blind verification input", "",
                   "Each block is one version of a question. Solve each independently; choose one letter.", ""], {}
    for it in items:
        for k, v in enumerate([it] + list(it.get("variants") or [])):
            label = f"{it['id']} v{k}"
            lines += [f"## {label}", "", v["stem"], ""]
            lines += [f"{c['id']}. {c['text']}" for c in v["choices"]] + [""]
            keys[label] = v["answer"]
    with open(os.path.join(scratch, "b15-blind.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(scratch, "b15-keys.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys, f, indent=1)
    print(f"blind file: {len(keys)} versions")


def main():
    items = [family(*f) for f in FAMILIES]
    finalize(items)
    failed = False
    for it in items:
        vs = it.pop("_variants", None)
        attach_variants(it, vs)
        letters = [it["answer"]] + [v["answer"] for v in it["variants"]]
        print(f"{it['id']}: key letters {' '.join(letters)}")
        if len(set(letters)) < 2:
            print(f"FAIL {it['id']}: the key has the same letter in every version", file=sys.stderr)
            failed = True
    if failed:
        sys.exit(1)
    assert len(items) == 13 and len({it["id"] for it in items}) == 13
    warnings = audit(items)
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    tally, v0 = {}, {}
    for it in items:
        v0[it["answer"]] = v0.get(it["answer"], 0) + 1
        for v in [it] + list(it.get("variants") or []):
            tally[v["answer"]] = tally.get(v["answer"], 0) + 1
    print("version-0 keys", dict(sorted(v0.items())), "all versions", dict(sorted(tally.items())))
    print("variants", sum(len(it.get("variants") or []) for it in items))
    if "--dry-run" in sys.argv:
        print("dry run: nothing written")
        return
    write_items(items, CONTENT)
    if SCRATCH:
        os.makedirs(SCRATCH, exist_ok=True)
        blind_files(items, SCRATCH)


if __name__ == "__main__":
    main()
