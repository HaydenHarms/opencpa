"""FAR batch 15 — Area II (Select Balance Sheet Accounts), 13 items written from scratch, all numeric
with three variants each.

Plan: 9 Analysis items spread over six Area II Analysis tasks (II.A.b bank reconciliation x2, II.A.c
investigate unreconciled cash x2, II.B.c receivables rollforward x2, II.C.c inventory rollforward x2,
II.D.f PP&E rollforward x1), each changing at least two component events from every existing item on its
task and using a stem format none of them uses. 4 Application items on the four of these Area II tasks
with the fewest existing items chosen for topic spread: II.F.c (cloud computing), II.G.c (exit/disposal
liabilities), II.H.1c (bond interest, with detachable warrants) and II.H.2a (debt covenant). Target mix:
9 Analysis / 4 Application, all Area II. Scope and skill tags follow the AICPA CPA Exam Blueprints
effective January 2026.

Revision 2 (2026-10-05) applies the blind verifier's required fixes and every gate finding (gate: 47.4%,
8 major, 4 wrong keys). Eight items were rebuilt with new events and new stem formats; the other five were
revised. See docs/reviews/far-batch-15.md. Items are written as `status: draft` until the gate re-passes.

Revision 3 (2026-10-07) applies the second-round findings (gate 78.8%, no majors): new asks for the two bank
reconciliations (net adjustment to the ledger) with a returned closed-account check and a bank charge for
another depositor's check; receivables-rollforward-0006 states that no transferred account was collected;
-0007 asks for the balance-sheet amount, with a December sale and a note in settlement replacing the
recovery; inventory-rollforward-0007 becomes a cost-of-goods-sold rollforward with goods on consignment;
exit-costs-0003 replaces the relocation event with a contract that runs past the cease-use date; the bond
item is renamed far-bonds-warrants-0001 and its rate sentence no longer points at the allocation.

Every numeric answer and distractor is computed in code (Decimal, rounded half up). Each item is a
builder: parameter set 0 is the item and sets 1-3 become its variants; every family moves the key's letter
across versions; parameter set 0 shows the distractor for the item's central twist.

Run: python scripts/batches/far-batch-15.py [--dry-run]   (B15_SCRATCH=<dir> also writes the blind file)
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
NOTE = ("Batch 15, revision 3 (second-round blind verifier and gate findings applied). Written from scratch; answers "
        "solved and every number and distractor computed in code.")
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
SCRATCH = os.environ.get("B15_SCRATCH")
STATUS = "draft"  # served only after the review gate re-passes


def family(id, area, topic, skill, refs, build, params, twist, asof=None):
    """An item built from parameter set 0, with sets 1-3 kept for its variants.

    `twist` names the pool distractor for the item's central twist; parameter set 0 must show it."""
    assert twist in params[0]["use"], f"{id}: version 0 doesn't show the central-twist distractor {twist}"
    base = build(params[0])
    review = dict(status=STATUS, references=refs, notes=NOTE)
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
    amts = [a.rstrip(",") for a in re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", v["stem"])]
    dup = sorted({a for a in amts if amts.count(a) > 1})
    if dup:
        print(f"REPEAT {label}: stem repeats {', '.join(dup)}", file=sys.stderr)
    for c in v["choices"]:
        for a in [x.rstrip(",") for x in re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", c["text"])]:
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


def short(p):
    """The company's short name: given explicitly (`s`) or the first word of a one-word place name."""
    return p.get("s") or p["co"].split()[0]


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


def signed(v, up, down):
    """'$1,400 understated' / '$620 overstated': a nonzero amount with its direction word."""
    v = D(v)
    assert v != 0
    return f"{m(abs(v))} {up if v > 0 else down}"


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
LAST = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def month_end(mo):
    mo = (mo - 1) % 12 + 1
    return f"{MONTHS[mo - 1]} {LAST[mo]}"


# ── Area II Analysis: II.A.b reconcile the bank balance to the general ledger ────────────────


def bank_recon_stop(p):
    """Net adjustment to the general ledger: a customer's check returned from a closed account, a
    card-processor fee, and a stopped check that sits on both sides (the books still show it as paid and the
    bookkeeper's outstanding list still includes it)."""
    co, s = p["co"], short(p)
    fee = p["CCg"] - p["CCn"]
    OCL = p["OC"] + p["SP"]
    cash = p["BB"] + p["DIT"] - p["OC"]
    key_v = p["SP"] - p["RET"] - fee
    GB = cash - key_v
    assert fee > 0 and GB > 0
    I, Dn = "increase", "decrease"
    pool = {
        "no_ret": (signed(key_v + p["RET"], I, Dn), f"Leaves out the {m(p['RET'])} customer check the bank returned from a closed account. The bank deducted it from {s}'s balance, so the receipt must be reversed in the books (the customer still owes the amount)."),
        "no_fee": (signed(key_v + fee, I, Dn), f"Leaves the card-sale deposit at its gross {m(p['CCg'])}. The processor deposited only {m(p['CCn'])} after its {m(fee)} discount fee, which {s} hasn't recorded."),
        "no_stop": (signed(key_v - p["SP"], I, Dn), f"Treats check #{p['chk']} as a valid payment, leaving its {m(p['SP'])} disbursement in the books. The bank has stopped the check and will never pay it, so the disbursement is reversed (and the check comes off the outstanding list on the bank side)."),
        "whole": (signed(p["BB"] - GB, I, Dn), f"Adjusts the books by the whole difference between the {m(p['BB'])} bank statement balance and the {m(GB)} ledger balance, as though the deposits in transit and outstanding checks were errors in the books. Those are timing items that adjust the bank side only."),
    }
    key = (signed(key_v, I, Dn), f"Correct. + {m(p['SP'])} (stopped check) − {m(p['RET'])} (returned check) − {m(fee)} (processor fee). Check: {m(GB)} adjusted to {m(cash)} = {m(p['BB'])} + {m(p['DIT'])} − ({m(OCL)} − {m(p['SP'])}).")
    choices, ans = build(pool, key, p["use"])
    result = f"an increase of {m(key_v)}" if key_v > 0 else f"a decrease of {m(-key_v)}"
    return variant(
        f"""{co}'s December 31 bank statement shows a balance of {m(p['BB'])}, and its general ledger cash account shows {m(GB)}. The bookkeeper's reconciliation lists deposits in transit of {m(p['DIT'])} and outstanding checks of {m(OCL)}. Reviewing the statement and the reconciliation, the accountant finds that a {m(p['RET'])} check from a customer, deposited on December 20, was returned by the bank on December 30 marked "account closed," and {s} hasn't recorded the return; that a credit-card processor deposited a batch of card sales net of its {m(fee)} discount fee, while {s} recorded the deposit at the {m(p['CCg'])} gross sale amount; and that the outstanding checks include check #{p['chk']}, for {m(p['SP'])}, on which {s} placed a stop-payment order after a vendor dispute. The bank has confirmed the stop-payment order, and {s}'s books still show the check as a disbursement. What net adjustment should {s} make to its general ledger cash balance at December 31?""",
        choices, ans,
        f"""Only items the books haven't recorded adjust the general ledger; deposits in transit and outstanding checks are timing items on the bank side. The returned check came back from a closed account, so the receipt is reversed (− {m(p['RET'])}) and the amount goes back to accounts receivable. Only {m(p['CCn'])} of the {m(p['CCg'])} card deposit reached the account, so the {m(fee)} processor fee is recorded (− {m(fee)}). The stopped check will never clear, so its disbursement is reversed (+ {m(p['SP'])}). Net adjustment = {m(p['SP'])} − {m(p['RET'])} − {m(fee)} = {result}. Check against the bank side: the stopped check also comes off the outstanding list, leaving {m(OCL)} − {m(p['SP'])} = {m(p['OC'])}, so correct cash is {m(p['BB'])} + {m(p['DIT'])} − {m(p['OC'])} = {m(cash)}, and {m(GB)} adjusted by the net amount gives the same {m(cash)}.""",
    )


def bank_recon_error(p):
    """Adjusted balance per bank: a postdated check wrongly listed in transit and a deposit the bank encoded
    for less than its amount adjust the bank side; interest and an automatic payment already in the statement
    adjust only the books."""
    co, s = p["co"], short(p)
    BE = p["DEPa"] - p["DEPb"]
    key_v = p["BB"] + p["DIT"] - p["PD"] - p["OC"] + BE
    GB = key_v - p["INT"] + p["AD"] + p["PD"]
    assert GB > 0 and BE > 0
    pool = {
        "no_pd": (m(key_v + p["PD"]), f"Leaves the customer's {m(p['PD'])} postdated check in deposits in transit. A check dated after year-end can't be deposited until its date, so it isn't in transit; it is still a receivable at December 31."),
        "no_be": (m(key_v - BE), f"Leaves out the bank's {m(BE)} encoding error. The bank credited the December 27 deposit at {m(p['DEPb'])} instead of the {m(p['DEPa'])} deposited, so the bank balance is {m(BE)} too low until the bank corrects it."),
        "int_bank": (m(key_v + p["INT"]), f"Adds the {m(p['INT'])} of interest to the bank side. The bank has already credited it, so it is in the {m(p['BB'])} statement balance; it adjusts only the books."),
        "ad_bank": (m(key_v - p["AD"]), f"Subtracts the {m(p['AD'])} automatic payment on the bank side. The bank has already deducted it, so it is in the statement balance; it adjusts only the books."),
    }
    key = (m(key_v), f"Correct. {m(p['BB'])} + ({m(p['DIT'])} − {m(p['PD'])}) − {m(p['OC'])} + {m(BE)} encoding error.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31 bank statement shows a balance of {m(p['BB'])}. The statement includes {m(p['INT'])} of interest the bank credited for the quarter and a {m(p['AD'])} automatic payment to the utility company that the bank deducted under {s}'s standing authorization. It also shows {s}'s December 27 deposit credited at {m(p['DEPb'])}; the deposit slip and {s}'s records show {m(p['DEPa'])}, and the bank has agreed to correct the amount in January. {s}'s list of deposits in transit totals {m(p['DIT'])}. It includes a {m(p['PD'])} check that a customer handed over on December 30, dated January 8 of the following year, which {s} recorded as a December 30 cash receipt and will deposit on its date. Outstanding checks total {m(p['OC'])}, and {s}'s general ledger cash account shows {m(GB)}. What adjusted (correct) balance per bank should {s}'s December 31 bank reconciliation show?""",
        choices, ans,
        f"""The bank side starts from the statement and adjusts for items the bank hasn't yet recorded correctly. The postdated check can't be deposited until January, so it comes out of deposits in transit: {m(p['DIT'])} − {m(p['PD'])} = {m(p['DIT'] - p['PD'])}. The bank credited the December 27 deposit at {m(p['DEPb'])} instead of {m(p['DEPa'])}, a bank error of {m(BE)} that is added back. The interest and the automatic payment are already in the statement balance; they adjust only the books. Adjusted balance per bank = {m(p['BB'])} + {m(p['DIT'] - p['PD'])} − {m(p['OC'])} + {m(BE)} = {m(key_v)}. Check against the books: {m(GB)} + {m(p['INT'])} − {m(p['AD'])} − {m(p['PD'])} = {m(key_v)}.""",
    )


# ── Area II Analysis: II.A.c investigate unreconciled cash balances ──────────────────────────


def cash_unrecon_shortage(p):
    """Both sides of the reconciliation are wrong; the untraced remainder is the cash shortage asked for."""
    co, s = p["co"], short(p)
    bank_ok = p["ABB"] - p["DD"]
    ABK = bank_ok + p["SH"] + p["WIRE"] - p["DUP"]
    diff = ABK - p["ABB"]
    book_ok = ABK - p["WIRE"] + p["DUP"]
    key_v = book_ok - bank_ok
    assert key_v == p["SH"] and diff > 0 and p["SH"] > p["DD"] and p["SH"] > p["DUP"]
    pool = {
        "no_dd": (m(key_v - p["DD"]), f"Accepts the reconciliation's {m(p['ABB'])} adjusted bank balance. The {m(p['DD'])} deposit of November 27 already appears on the November statement, so counting it again as a deposit in transit overstates the bank side by {m(p['DD'])}."),
        "no_wire": (m(key_v + p["WIRE"]), f"Leaves the {m(p['WIRE'])} wire in book cash. The customer's bank sent it to another company's account, so {s} never received it and the receipt must be reversed (the customer still owes the amount)."),
        "no_dup": (m(key_v - p["DUP"]), f"Leaves the {m(p['DUP'])} petty-cash check recorded twice. The duplicate entry understates book cash, so reversing it raises the book side by {m(p['DUP'])}."),
        "whole": (m(diff), f"Writes off the whole {m(diff)} difference without first correcting the double-counted deposit, the misdirected wire and the duplicate disbursement."),
    }
    key = (m(key_v), f"Correct. Corrected book balance {m(ABK)} − {m(p['WIRE'])} + {m(p['DUP'])} = {m(book_ok)}; corrected bank balance {m(p['ABB'])} − {m(p['DD'])} = {m(bank_ok)}; shortage = {m(book_ok)} − {m(bank_ok)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s accountant could not reconcile the November 30 bank statement. Her reconciliation shows an adjusted bank balance of {m(p['ABB'])}, after adding deposits in transit and subtracting outstanding checks, while the general ledger cash account, after recording the bank's charges and credits, shows {m(ABK)}. The controller traces the {m(diff)} difference and finds: the deposits in transit include a {m(p['DD'])} deposit made on November 27, which the bank credited on November 28 and which appears on the November statement; a {m(p['WIRE'])} wire transfer, recorded as received because a customer's remittance advice said it had been sent, was misdirected by the customer's bank to another company's account and never reached {s}; and a {m(p['DUP'])} check to replenish petty cash was entered twice in the cash disbursements journal. No other errors can be found, and {s} will write off whatever difference remains as a cash shortage. What cash shortage should {s} record?""",
        choices, ans,
        f"""Correct each side first. Bank side: the {m(p['DD'])} deposit is already in the statement balance, so it isn't in transit: {m(p['ABB'])} − {m(p['DD'])} = {m(bank_ok)}, the true cash balance. Book side: reverse the {m(p['WIRE'])} wire that never arrived and reverse the duplicate {m(p['DUP'])} disbursement: {m(ABK)} − {m(p['WIRE'])} + {m(p['DUP'])} = {m(book_ok)}. The books still show {m(book_ok)} − {m(bank_ok)} = {m(key_v)} more cash than the bank holds, and with no other error to be found, that is the cash shortage to write off.""",
    )


def cash_unrecon_misstated(p):
    """A bank encoding error on one side, three book errors on the other; the ask is the direction and size
    of the general ledger's misstatement."""
    co, s = p["co"], short(p)
    E = p["CKe"] - p["CK"]
    T = p["BB"] + p["DIT"] - p["OC"] + E
    GB = T + p["INSUR"] - 2 * p["DEP"] + p["CF"]
    key_v = T - GB  # positive: the ledger is understated
    draft = (p["BB"] + p["DIT"] - p["OC"]) - GB
    assert E > 0 and key_v > 0 and GB > 0
    U, O = "understated", "overstated"
    pool = {
        "no_je": (signed(p["DEP"] - p["INSUR"] - p["CF"], U, O), f"Corrects the misposted {m(p['DEP'])} deposit by only {m(p['DEP'])}. Recording a receipt in the disbursements journal reduced cash by {m(p['DEP'])} when it should have increased it by {m(p['DEP'])}, so the books are {m(2 * p['DEP'])} too low on that item."),
        "no_insur": (signed(2 * p["DEP"] - p["CF"], U, O), f"Leaves out the {m(p['INSUR'])} insurance premium the bank deducted under a standing authorization, which {s} hasn't recorded."),
        "no_cf": (signed(2 * p["DEP"] - p["INSUR"], U, O), f"Leaves the {m(p['CF'])} counterfeit bill in book cash. The bank didn't credit it, so it was never cash in the account."),
        "no_be": (signed(draft, U, O), f"Compares the ledger with the bank balance plus deposits in transit less outstanding checks, {m(p['BB'] + p['DIT'] - p['OC'])}, without correcting the bank's error: the bank charged check #{p['chk']} at {m(p['CKe'])} instead of the {m(p['CK'])} written on it, so the bank side is {m(E)} too low."),
    }
    key = (signed(key_v, U, O), f"Correct. Correct cash is {m(p['BB'])} + {m(p['DIT'])} − {m(p['OC'])} + {m(E)} = {m(T)}; the ledger's {m(GB)} is {m(key_v)} lower. Book-side check: {m(GB)} − {m(p['INSUR'])} + {m(2 * p['DEP'])} − {m(p['CF'])} = {m(T)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Internal audit is testing {co}'s October 31 cash. The bank statement shows {m(p['BB'])}, deposits in transit total {m(p['DIT'])}, outstanding checks total {m(p['OC'])}, and the general ledger cash account shows {m(GB)}; the bookkeeper's reconciliation does not balance. The auditors find that the bank charged check #{p['chk']}, written and recorded for {m(p['CK'])}, against the account at {m(p['CKe'])} and has agreed to correct the error; that a {m(p['INSUR'])} insurance premium the bank deducted under {s}'s standing authorization hasn't been recorded; that a {m(p['DEP'])} deposit of customer receipts was entered in the cash disbursements journal instead of the cash receipts journal; and that a {m(p['CF'])} bill in an earlier deposit was counterfeit, so the bank didn't credit it, and {s} hasn't written it off. Before any correction, by what amount, and in which direction, is {s}'s general ledger cash balance misstated at October 31?""",
        choices, ans,
        f"""Correct cash comes from the bank side once the bank's error is fixed: the bank charged {m(p['CKe'])} for a {m(p['CK'])} check, so {m(E)} goes back: {m(p['BB'])} + {m(p['DIT'])} − {m(p['OC'])} + {m(E)} = {m(T)}. The book side confirms it: subtract the {m(p['INSUR'])} premium; add {m(2 * p['DEP'])} for the deposit entered as a disbursement (removing the wrong {m(p['DEP'])} reduction and recording the {m(p['DEP'])} receipt); and subtract the {m(p['CF'])} counterfeit bill: {m(GB)} − {m(p['INSUR'])} + {m(2 * p['DEP'])} − {m(p['CF'])} = {m(T)}. The ledger shows {m(GB)}, which is {m(key_v)} below the correct {m(T)}, so it is understated by {m(key_v)}.""",
    )


# ── Area II Analysis: II.B.c prepare a rollforward of trade receivables ──────────────────────


def ar_ledger_postings(p):
    """Control-account postings: a transfer of receivables that can't be a sale, a bill-and-hold invoice that
    isn't a receivable yet, and cash sales posted through AR (no net effect)."""
    co, s = p["co"], short(p)
    E = p["B"] + p["Rv"] - p["Cc"] - p["Wo"] - p["Rec"]
    key_v = E + p["Rec"] - p["BH"]
    L = p["Rec"]

    def pair(ar, liab):
        return f"{m(ar)} receivables; {m(liab)} liability to the bank" if liab else f"{m(ar)} receivables; no liability to the bank"

    pool = {
        "no_rec": (pair(key_v - p["Rec"], 0), f"Accepts the {m(p['Rec'])} credit for the transfer as a sale. Because the agreement bars the bank from selling or pledging the accounts, the transfer fails the conditions for sale accounting in ASC 860-10-40-5; it is a secured borrowing, so the receivables stay in the control account and the cash is a liability."),
        "no_bh": (pair(key_v + p["BH"], L), f"Keeps the {m(p['BH'])} bill-and-hold invoice as a receivable. The goods sit with {s}'s other stock and can fill other orders, so control hasn't passed and there is no sale yet; payment isn't due until 30 days after delivery, so {s} has no unconditional right to payment either."),
        "cs_wrong": (pair(key_v - p["CS"], L), f"Removes the {m(p['CS'])} of cash sales from the sales debits only. They were also posted as collections, so the debit and credit cancel and the year-end balance needs no correction for them."),
        "cs_coll": (pair(key_v + p["CS"], L), f"Removes the {m(p['CS'])} of cash sales from the collection credits only. They were also posted as sales debits, so the debit and credit cancel and the year-end balance needs no correction for them."),
    }
    key = (pair(key_v, L), f"Correct. {m(E)} + {m(p['Rec'])} − {m(p['BH'])}; the cash sales were debited and credited to the account, so they net to zero. The {m(L)} received from the bank is a liability, none of the accounts having been collected.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s accounts receivable control account began Year 2 at {m(p['B'])}. Its Year 2 postings were debits for sales of {m(p['Rv'])}, credits for cash collected of {m(p['Cc'])}, credits for accounts written off of {m(p['Wo'])}, and a {m(p['Rec'])} credit on October 1, when {s} transferred that amount of customer accounts to a bank for cash, leaving a December 31 balance of {m(E)}. Testing the postings, internal audit learns that {s} must reimburse the bank for any transferred account that isn't collected, and that the transfer agreement forbids the bank from selling or pledging the accounts, so no one but {s} and the bank will deal with {s}'s customers; none of the transferred accounts had been collected by December 31. The sales debits include a {m(p['BH'])} invoice dated December 28 for goods a customer asked {s} to hold until its new store opens in March; the goods sit with {s}'s other stock, are available to fill other orders, and are payable 30 days after delivery. Both the sales debits and the cash-collected credits include {m(p['CS'])} of showroom cash sales, which {s}'s cashiers post through the receivables account on the day of each sale. What should {s} report at December 31, Year 2, as accounts receivable, before any allowance, and as its liability to the bank?""",
        choices, ans,
        f"""The transfer is a secured borrowing, not a sale: the agreement forbids the bank from selling or pledging the accounts, a constraint that benefits {s}, so the transferee lacks the right to pledge or exchange them that sale accounting requires (ASC 860-10-40-5(b)). (The recourse by itself wouldn't prevent sale accounting.) None of the accounts had been collected by December 31, so all of them are still {s}'s receivables. The {m(p['Rec'])} goes back into receivables, and the cash received is a liability to the bank. The December 28 invoice is not a sale: the goods aren't set apart as the customer's and can be used to fill other orders, so control hasn't passed (ASC 606-10-55-83), and with payment due only after delivery there is no unconditional right to payment; the {m(p['BH'])} comes out. The showroom cash sales were debited and credited to the account for the same {m(p['CS'])}, so they leave the balance unchanged. Corrected receivables = {m(E)} + {m(p['Rec'])} − {m(p['BH'])} = {m(key_v)}, and the liability to the bank is the {m(L)} received.""",
    )


def ar_rollforward_creditbal(p):
    """The amount reported as accounts receivable: gross debit balances (credit balances are a liability),
    less a December return entered in January, plus a December sale entered in January; a December note taken
    in settlement of an account was correctly moved out of accounts receivable."""
    co, s = p["co"], short(p)
    E_draft = p["B"] + p["Rv"] - p["Cc"] - p["Wo"] - p["NT"]
    DR = E_draft + p["CB"]
    key_v = DR - p["RA"] + p["SL"]
    pool = {
        "no_cb": (m(key_v - p["CB"]), f"Reports receivables net of the {m(p['CB'])} of customer credit balances, which is the corrected control-account balance. Credit balances, from overpayments and returns, are amounts {s} owes customers; they are reported as a liability, not netted against other customers' debit balances."),
        "no_ra": (m(key_v + p["RA"]), f"Leaves out the {m(p['RA'])} credit memo for goods a customer returned on December 29. The return is a Year 2 event, so it reduces that customer's debit balance at December 31 even though the memo was entered in January."),
        "no_sl": (m(key_v - p["SL"]), f"Leaves out the {m(p['SL'])} sale shipped on December 30. Control passed when the goods were shipped FOB shipping point, so {s} had a receivable at December 31 even though the invoice was entered in January."),
        "nt_wrong": (m(key_v + p["NT"]), f"Puts the {m(p['NT'])} note back into accounts receivable. Once the customer signed a note, {s} holds a note receivable, reported separately; the credit to the customer's account was correct."),
    }
    key = (m(key_v), f"Correct. Customer debit balances of {m(DR)} − {m(p['RA'])} December return + {m(p['SL'])} December sale; the {m(p['CB'])} of credit balances is a liability.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""All of {co}'s sales are on credit. Its accounts receivable control account began Year 2 at {m(p['B'])}; credit sales for the year were {m(p['Rv'])}, cash collected from customers was {m(p['Cc'])}, {m(p['Wo'])} of accounts were written off, and {m(p['NT'])} was credited to a customer's account in December when the customer signed a 90-day note in settlement of its overdue balance. From these a staff accountant arrived at a preliminary December 31 figure of {m(E_draft)}, which agrees with the aged subledger: customer debit balances of {m(DR)} and customer credit balances, from overpayments and returns, of {m(p['CB'])}. Examining the figure, the internal auditor notes that a {m(p['RA'])} credit memo for goods a customer returned on December 29, logged by the receiving dock that day, wasn't entered until January; that customer's debit balance was well above the memo amount. The auditor also finds that goods sold to another customer for {m(p['SL'])} on account, shipped FOB shipping point on December 30, weren't invoiced or recorded until January. What amount should {s} report as accounts receivable, before any allowance, in its December 31, Year 2 balance sheet?""",
        choices, ans,
        f"""The preliminary {m(E_draft)} is the subledger's debit balances of {m(DR)} less its {m(p['CB'])} of credit balances. Credit balances are amounts owed to customers, a liability, so the asset starts from the gross debit balances. The December 29 return is a Year 2 event and reduces the returning customer's debit balance (− {m(p['RA'])}). The goods shipped FOB shipping point on December 30 passed to the customer that day, so the sale and the receivable belong in Year 2 (+ {m(p['SL'])}). The {m(p['NT'])} note is a note receivable, not an account receivable, so the credit to the customer's account was correct and needs no change. Accounts receivable = {m(DR)} − {m(p['RA'])} + {m(p['SL'])} = {m(key_v)}.""",
    )


# ── Area II Analysis: II.C.c prepare a rollforward of inventory ──────────────────────────────


def inv_purchases_line(p):
    """The purchases line of the rollforward: consigned-in goods recorded as purchases, net-method discounts
    lost charged to purchases, an unrecorded December purchase return, and an in-transit FOB shipping
    point purchase that is correctly included."""
    co, s = p["co"], short(p)
    E = p["B"] + p["P"] - p["C"]
    key_v = p["P"] - p["CI"] - p["PD"] - p["RT"]
    pool = {
        "no_ci": (m(key_v + p["CI"]), f"Keeps the {m(p['CI'])} of consigned goods in purchases. Title stays with the supplier until {s} sells them, so receiving them isn't a purchase."),
        "no_pd": (m(key_v + p["PD"]), f"Keeps the {m(p['PD'])} of discounts lost in purchases. Under the net method, inventory is recorded at the discounted price, and discounts lost by paying late are a financing expense, not inventory cost."),
        "no_rt": (m(key_v + p["RT"]), f"Leaves out the {m(p['RT'])} of goods returned to the supplier on December 18. The return happened in Year 2, so Year 2 purchases (net of returns) are reduced even though the credit memo arrived in January."),
        "tr_wrong": (m(key_v - p["TR"]), f"Removes the {m(p['TR'])} of goods in transit at year-end. Shipped FOB shipping point, they became {s}'s when the supplier shipped them on December 27, so they are properly in Year 2 purchases."),
    }
    key = (m(key_v), f"Correct. {m(p['P'])} − {m(p['CI'])} − {m(p['PD'])} − {m(p['RT'])}; the in-transit goods stay in.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} uses a perpetual inventory system and records purchases net of cash discounts. Its staff's Year 2 inventory rollforward shows beginning inventory of {m(p['B'])}, purchases (net of returns) of {m(p['P'])}, cost of goods sold of {m(p['C'])} and ending inventory of {m(E)}; the purchases figure is the purchases journal total. Testing that figure, the controller finds that {m(p['CI'])} of goods a supplier shipped to {s} on consignment, which {s} may return unsold, were entered as purchases when they arrived; that when {s} paid invoices after the discount period, it charged the {m(p['PD'])} of discounts it lost to purchases; that goods costing {m(p['RT'])}, which {s} shipped back to a supplier on December 18, weren't entered as a purchase return until the supplier's credit memo arrived in January; and that the journal includes {m(p['TR'])} of goods a supplier shipped FOB shipping point on December 27, still in transit at year-end. What purchases (net of returns) should the corrected rollforward report for Year 2?""",
        choices, ans,
        f"""Consigned goods belong to the supplier until {s} sells them (ASC 606-10-55-79 to 55-80), so the {m(p['CI'])} isn't a purchase. Under the net method, purchases are recorded at the discounted price and a discount lost by paying late is a financing expense, so the {m(p['PD'])} comes out of purchases. The goods returned on December 18 reduce Year 2 purchases (− {m(p['RT'])}), whenever the credit memo arrives. Goods shipped FOB shipping point belong to {s} from the shipment date, so the {m(p['TR'])} in transit is properly a Year 2 purchase and stays. Corrected purchases = {m(p['P'])} − {m(p['CI'])} − {m(p['PD'])} − {m(p['RT'])} = {m(key_v)}.""",
    )


def inv_perpetual_adjust(p):
    """Cost of goods sold in the rollforward: goods out on consignment recorded as sold when shipped, a
    volume rebate allocated between goods sold and goods on hand (ASC 705-20), freight-in on goods since sold
    charged to delivery expense, and freight-out correctly charged there (a decoy)."""
    co, s = p["co"], short(p)
    E = p["B"] + p["P"] - p["C"]
    rate = D(p["r"]) / 100
    RB = rd(rate * p["Q"])
    RBh = rd(rate * p["H"])
    key_v = p["C"] + p["FI"] - p["CO"] - (RB - RBh)
    end_ok = E + p["CO"] - RBh
    assert p["B"] + p["P"] + p["FI"] - RB - end_ok == key_v and end_ok not in (p["B"], E)
    pool = {
        "no_fi": (m(key_v - p["FI"]), f"Leaves the {m(p['FI'])} of freight on incoming purchases in delivery expense. Freight-in is part of the cost of inventory; those goods have all been sold, so it belongs in cost of goods sold."),
        "fo_in": (m(key_v + p["FO"]), f"Also moves the {m(p['FO'])} of freight on shipments to customers into cost of goods sold. Freight-out is a selling (delivery) cost, not a cost of inventory, so it stays where it is."),
        "no_co": (m(key_v + p["CO"]), f"Leaves the {m(p['CO'])} of goods at the dealer in cost of goods sold. Goods out on consignment still belong to {s} until the dealer sells them, so they go back into inventory."),
        "rb_full": (m(key_v - RBh), f"Takes the whole {m(RB)} rebate out of cost of goods sold. The rebate reduces the cost of all {m(p['Q'])} of qualifying purchases, so the share on goods still on hand, {m(RBh)}, reduces inventory; only {m(RB - RBh)} reduces cost of goods sold."),
        "no_rb": (m(key_v + RB - RBh), f"Ignores the volume rebate. {s} earned it in Year 2, so it reduces the cost of the qualifying purchases, and the {m(RB - RBh)} share on goods already sold reduces cost of goods sold."),
    }
    key = (m(key_v), f"Correct. {m(p['C'])} + {m(p['FI'])} freight-in − {m(p['CO'])} consigned goods still on hand − {m(RB - RBh)} rebate on goods sold.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s staff prepared this Year 2 inventory rollforward from its perpetual records: beginning inventory {m(p['B'])}, purchases {m(p['P'])}, cost of goods sold {m(p['C'])}, ending inventory {m(E)}. Reviewing it, the controller finds that {m(p['FI'])} of freight charges on incoming shipments from suppliers, all for goods sold during Year 2, and {m(p['FO'])} of freight on shipments to customers were both charged to delivery expense. In December, {s} shipped goods costing {m(p['CO'])} to a dealer that sells them on consignment, and the perpetual system recorded them as sold when they left the warehouse; the dealer hadn't sold any of them by December 31. And {s}'s Year 2 purchases of one supplier's alloy bar, {m(p['Q'])} in all, reached that supplier's volume threshold for a {p['r']}% rebate on the year's purchases; the supplier issued the credit memo in January, and {s} hasn't recorded the rebate. Alloy bar costing {m(p['H'])} from those purchases is still on hand at December 31; the rest has been sold. What cost of goods sold should the corrected rollforward report for Year 2?""",
        choices, ans,
        f"""Freight-in is a cost of bringing goods to their location for sale, so it is part of inventory cost (ASC 330-10-30-1); the goods it relates to were all sold, so the {m(p['FI'])} moves from delivery expense into cost of goods sold. Freight-out is a selling cost and stays in delivery expense. Goods out on consignment remain {s}'s inventory until the dealer sells them (ASC 606-10-55-79 to 55-80), so the {m(p['CO'])} comes out of cost of goods sold and back into inventory. The rebate reduces the cost of the purchases that earned it (ASC 705-20): {p['r']}% × {m(p['Q'])} = {m(RB)} in all. The share on the {m(p['H'])} still on hand, {p['r']}% × {m(p['H'])} = {m(RBh)}, reduces ending inventory, and the remaining {m(RB - RBh)} reduces cost of goods sold. Corrected cost of goods sold = {m(p['C'])} + {m(p['FI'])} − {m(p['CO'])} − {m(RB - RBh)} = {m(key_v)}. (The corrected rollforward: {m(p['B'])} + ({m(p['P'])} + {m(p['FI'])} − {m(RB)}) − {m(key_v)} = ending inventory of {m(end_ok)}.)""",
    )


# ── Area II Analysis: II.D.f prepare a rollforward of PP&E ───────────────────────────────────


def ppe_additions(p):
    """The additions line: an overweight-load fine and post-installation insurance wrongly capitalized,
    transit insurance wrongly expensed, and a new parking lot recorded in the wrong PP&E account."""
    co, s = p["co"], short(p)
    key_v = p["AD"] - p["FINE"] + p["TI"] - p["INS"]
    pool = {
        "no_fine": (m(key_v + p["FINE"]), f"Keeps the {m(p['FINE'])} overweight-load fine in the press's cost. A fine for breaking the law isn't a necessary cost of bringing the asset to its location; it is expensed."),
        "no_ti": (m(key_v - p["TI"]), f"Leaves the {m(p['TI'])} premium for insuring the press in transit in expense. Insurance while the asset is being brought to its site is a cost of getting it ready for use and is capitalized."),
        "no_ins": (m(key_v + p["INS"]), f"Keeps the {m(p['INS'])} premium for the press's first year of coverage after installation in its cost. Insurance once the asset is in service is a period cost (a prepaid expense until used)."),
        "lot_wrong": (m(key_v - p["LOT"]), f"Removes the {m(p['LOT'])} parking lot from additions because it was posted to buildings. A new parking lot is a land improvement, still property, plant and equipment; moving it between accounts doesn't change total additions."),
    }
    key = (m(key_v), f"Correct. {m(p['AD'])} − {m(p['FINE'])} + {m(p['TI'])} − {m(p['INS'])}; the parking lot is reclassified within property, plant and equipment.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""The additions line of {co}'s Year 2 rollforward of property, plant and equipment, at cost, is the capital expenditures report, which totals {m(p['AD'])}. Testing the report, the controller finds that {s} paid a {m(p['FINE'])} fine when its own truck was stopped for carrying an overweight load while hauling a new press from the port, and added the fine to the press's cost; that the {m(p['TI'])} premium to insure the press during its voyage from the manufacturer was charged to insurance expense; that the {m(p['INS'])} premium for the press's first year of property coverage, which began when the press went into service, was added to its cost; and that the {m(p['LOT'])} cost of paving a new parking lot at the plant, where there was none before, was added to the buildings account, though {s} records land improvements in a separate account depreciated over a shorter life. What total additions should the corrected rollforward report for Year 2?""",
        choices, ans,
        f"""The cost of property, plant and equipment includes what is necessary to bring the asset to the condition and location for its intended use (ASC 360-10-30). Insurance during transit is such a cost, so the {m(p['TI'])} is capitalized (+ {m(p['TI'])}). A fine for an overweight load is a penalty, not a necessary cost, and insurance after the press is in service is a period cost, so both come out (− {m(p['FINE'])} and − {m(p['INS'])}). The new parking lot is a land improvement; moving it out of buildings changes the account, not total property, plant and equipment, so additions don't change for it. Corrected additions = {m(p['AD'])} − {m(p['FINE'])} + {m(p['TI'])} − {m(p['INS'])} = {m(key_v)}.""",
    )


# ── Area II Application ───────────────────────────────────────────────────────────────────────


def cloud_modules(p):
    """Two modules going live on different dates, each amortized from its own ready-for-use date over the
    remaining hosting term (the renewal is not included), with process-redesign costs expensed."""
    co, s = p["co"], short(p)
    T, mA, mB = p["T"], p["mA"], p["mB"]
    term_m = 12 * T

    def amort(cost, mo, months):
        """Year 1 amortization for a module ready on the 1st of month `mo`, over `months` from Jan 1."""
        remaining = months - (mo - 1)
        return rd(D(cost) * (13 - mo) / remaining)

    aA, aB = amort(p["X"], mA, term_m), amort(p["Y"], mB, term_m)
    key_v = p["X"] + p["Y"] - aA - aB
    full_term = p["X"] + p["Y"] - rd(D(p["X"]) * (13 - mA) / term_m + D(p["Y"]) * (13 - mB) / term_m)
    from_start = p["X"] + p["Y"] - rd(D(p["X"] + p["Y"]) * 12 / term_m)
    same_date = p["X"] + p["Y"] - amort(p["X"] + p["Y"], mA, term_m)
    renew_m = 12 * (T + p["Rn"])
    with_renewal = p["X"] + p["Y"] - amort(p["X"], mA, renew_m) - amort(p["Y"], mB, renew_m)
    bpr_am = amort(p["X"] + p["BPR"], mA, term_m) - aA
    cap_bpr = p["X"] + p["BPR"] + p["Y"] - amort(p["X"] + p["BPR"], mA, term_m) - aB
    dA, dB = f"{MONTHS[mA - 1]} 1", f"{MONTHS[mB - 1]} 1"
    endY = f"December 31, Year {T}"
    rA, rB = term_m - (mA - 1), term_m - (mB - 1)
    pool = {
        "full_term": (m(full_term), f"Spreads each module's costs over the full {T}-year term starting at its go-live date, so amortization would run past the contract's end on {endY}. Implementation costs are amortized over the hosting arrangement's term, which by then has only {rA} and {rB} months left."),
        "from_start": (m(from_start), f"Amortizes both modules for all of Year 1, from the contract's January 1 start. Amortization of each module begins only when that module is ready for its intended use."),
        "same_date": (m(same_date), f"Starts amortizing both modules on {dA}, when the first one went live. Because the modules work independently, each is amortized from its own ready-for-use date, and the second wasn't ready until {dB}."),
        "with_renewal": (m(with_renewal), f"Includes the {p['Rn']}-year renewal in the amortization period. Management hasn't decided whether to renew, so the renewal isn't reasonably certain and the term is the {T}-year noncancellable period."),
        "cap_bpr": (m(cap_bpr), f"Capitalizes the {m(p['BPR'])} paid to redesign business processes and amortizes it with the inventory module from {dA} (about {m(bpr_am)} for Year 1). Process reengineering is expensed as incurred, not capitalized as a cost of implementing the software."),
    }
    key = (m(key_v), f"Correct. ({m(p['X'])} − {m(aA)}) + ({m(p['Y'])} − {m(aB)}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} signs a noncancellable {T}-year contract, running from that date, for access to a vendor's cloud-hosted warehouse management system. {s} has no right to take the software onto its own servers. The system is in general release and needs only configuration for {s}'s operations. The contract lets {s} extend it for {p['Rn']} more years at the vendor's list prices at that time, and management hasn't decided whether it will. After the board approved and funded the project, {s} paid consultants {m(p['BPR'])} to redesign its receiving and picking processes before configuration began, {m(p['X'])} to configure and test the inventory module, which was ready for its intended use on {dA}, Year 1, and {m(p['Y'])} to configure and test the shipping module, ready on {dB}, Year 1. Each module works independently of the other. {s} amortizes capitalized implementation costs straight-line by month. What amount should {s} report as capitalized implementation costs, net of accumulated amortization, at December 31, Year 1?""",
        choices, ans,
        f"""A hosting arrangement {s} can't take possession of is a service contract, and its implementation costs follow ASC 350-40, as amended by ASU 2018-15. Configuring and testing each module is capitalized; redesigning business processes ({m(p['BPR'])}) is expensed as incurred. (ASU 2025-06, which replaces the project stages with a probable-to-complete threshold that this funded project meets, gives the same result.) The costs are amortized straight-line over the term of the hosting arrangement, the {T}-year noncancellable period ending {endY}; the renewal is excluded because management hasn't decided to exercise it. Each module's amortization starts when that module is ready for its intended use and runs over the term remaining at that date. Inventory module: {m(p['X'])} × {13 - mA}/{rA} = {m(aA)}. Shipping module: {m(p['Y'])} × {13 - mB}/{rB} = {m(aB)}. Net asset = {m(p['X'] + p['Y'])} − {m(aA)} − {m(aB)} = {m(key_v)}.""",
    )


def exit_cost_timing(p):
    """Year 2 exit-cost expense: the rest of the ratable stay bonus, the contract termination fee (notice
    given in Year 2) and the contract costs after the cease-use date; severance belongs to Year 1."""
    co, s = p["co"], short(p)
    e, t = p["elapsed"], p["total"]
    stay_total = p["NB"] * p["SB"]
    stay = rd(D(stay_total) * e / t)
    svc = p["SVC"] * p["after"]
    key_v = stay_total - stay + p["K"] + svc
    pool = {
        "incl_sev": (m(key_v + p["A"]), f"Also charges the {m(p['A'])} of severance to Year 2, when it is paid. Employees receive it whether they stay or leave early, so all of it was recognized when the plan was communicated in Year 1."),
        "stay_full": (m(key_v + stay), f"Charges the whole {m(stay_total)} of team-leader bonuses to Year 2, when they are paid. They are recognized ratably over the {t}-month service period, so {e}/{t} ({m(stay)}) was already recognized in Year 1."),
        "no_k": (m(key_v - p["K"]), f"Leaves out the {m(p['K'])} fee to end the cleaning contract. A contract termination cost is recognized when the contract is terminated under its terms, by the written notice {s} sends in March, Year 2."),
        "no_svc": (m(key_v - svc), f"Leaves out the {m(svc)} of telephone-service fees due after the center closes ({p['after']} months × {m(p['SVC'])}). They continue without benefit to {s}, so they are recognized in full at the cease-use date, {p['close']}, Year 2."),
    }
    key = (m(key_v), f"Correct. {m(stay_total - stay)} remaining bonuses + {m(p['K'])} termination fee + {m(svc)} telephone fees after the cease-use date.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On {p['comm']}, Year 1, {co}'s board approves a plan to close a regional call center on {p['close']}, Year 2, and that day tells the center's {p['n']} employees which positions will end, when, and what each employee will receive; {s} doesn't expect to change the plan. Each employee will receive severance based on years of service, {m(p['A'])} in total, payable at termination whether the employee stays until the center closes or leaves earlier. Each of the center's {p['NB']} team leaders will also receive a {m(p['SB'])} bonus, but only if he or she stays until the center closes, and all of them do. No law or agreement requires {s} to give notice of termination. The center's cleaning contract, which isn't a lease, can be ended early for a {m(p['K'])} fee by written notice; {s} sends the notice in March, Year 2, and uses the service until then. The center's telephone-service contract, which can't be cancelled, runs through {p['svc_end']}, Year 2, at {m(p['SVC'])} a month; {s} stops using the service when the center closes. Treat each month as equal in length, and ignore discounting. What exit-cost expense should {s} recognize in Year 2?""",
        choices, ans,
        f"""Severance that employees receive without further service was recognized in full when the plan was communicated in Year 1 (ASC 420-10-25-4 and 25-8), so none of the {m(p['A'])} is Year 2 expense. The team-leader bonuses require service until the center closes, {t} months after communication and longer than the 60-day minimum retention period, so they are recognized ratably (ASC 420-10-25-9): {e}/{t} of {m(stay_total)} = {m(stay)} in Year 1, leaving {m(stay_total - stay)} for Year 2. The cleaning-contract fee is recognized when {s} terminates the contract by giving notice in March, Year 2 (ASC 420-10-25-11): {m(p['K'])}. The telephone fees due after the center closes, {p['after']} × {m(p['SVC'])} = {m(svc)}, continue without economic benefit and are recognized at the cease-use date (ASC 420-10-25-13). Year 2 exit-cost expense = {m(stay_total - stay)} + {m(p['K'])} + {m(svc)} = {m(key_v)}.""",
    )


def bonds_warrants_interest(p):
    """Bonds with detachable warrants, issued mid-year: relative fair value allocation, then the effective
    rate (computed in code from the allocated amount) for one full period and an accrued part period."""
    co, s = p["co"], short(p)
    r = D(p["ER"]) / 100 / 2
    n = 20
    C = rd(D(p["F"]) * D(p["SR"]) / 100 / 2)
    pv = C * (1 - (1 + r) ** -n) / r + D(p["F"]) * (1 + r) ** -n
    PR = rd(pv * (p["BFV"] + p["FVW"]) / p["BFV"])
    CV0 = rd(D(PR) * p["BFV"] / (p["BFV"] + p["FVW"]))
    assert abs(CV0 - pv) <= 1, (CV0, pv)
    assert C < CV0 * r and CV0 < p["BFV"] < p["F"]
    assert D("0.95") < PR / D(p["BFV"] + p["FVW"]) < D("0.995"), "proceeds should sit just below the two fair values"
    cv = CV0  # the stated rate amortizes the allocated amount to face (within rounding) at maturity
    for _ in range(n):
        cv = cv + rd(cv * r) - C
    assert abs(cv - p["F"]) <= 10, cv
    acc = p["acc"]

    def year1(start):
        i1 = rd(start * r)
        cv1 = start + i1 - C
        return i1, cv1, rd(cv1 * r * acc / 6)

    def total(start):
        a, _, b = year1(start)
        return a + b

    i1, CV1, i2 = year1(CV0)
    key_v = i1 + i2
    pool = {
        "face_alloc": (m(total(D(PR))), f"Uses the full {m(PR)} of proceeds as the bonds' carrying amount. Part of the proceeds belongs to the detachable warrants: the bonds get {m(PR)} × {m(p['BFV'])}/{m(p['BFV'] + p['FVW'])} = {m(CV0)}, and the rest is credited to additional paid-in capital."),
        "bfv_alloc": (m(total(D(p['BFV']))), f"Carries the bonds at their own {m(p['BFV'])} fair value. Proceeds are allocated in proportion to the two fair values, which gives the bonds {m(CV0)}, because the {m(PR)} received is less than the {m(p['BFV'] + p['FVW'])} the bonds and warrants are worth together."),
        "stated_only": (m(C + rd(C * acc / 6)), f"Uses only the stated interest, {m(C)} for the first period and {acc}/6 of {m(C)} accrued at year-end, with no discount amortization. The effective interest method applies the effective rate to the carrying amount."),
        "no_accrual": (m(i1), f"Stops at the {p['pay1']} payment. Interest from then to December 31 ({acc} month{'s' if acc != 1 else ''}) also belongs in Year 1 and is accrued at year-end."),
    }
    key = (m(key_v), f"Correct. {m(CV0)} × {p['ER']}%/2 = {m(i1)}; then {m(CV1)} × {p['ER']}%/2 × {acc}/6 = {m(i2)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On {p['issue']}, Year 1, {co} issues {m(p['F'])} face amount of ten-year, {p['SR']}% bonds, paying interest each {p['pay1']} and {p['pay2']}, together with detachable stock warrants, which are classified in equity, for total cash proceeds of {m(PR)}. Immediately after issuance, the bonds trade without the warrants at a total fair value of {m(p['BFV'])}, and the warrants trade at a total fair value of {m(p['FVW'])}. The bonds' effective interest rate, based on their initial carrying amount, is {p['ER']}%, compounded semiannually. {s} applies the effective interest method, accrues interest at year-end and rounds each computation to the nearest dollar. How much bond interest expense should {s} recognize for Year 1?""",
        choices, ans,
        f"""Detachable warrants are accounted for separately, and with both fair values known the proceeds are allocated in proportion to them (ASC 470-20-25-2): bonds = {m(PR)} × {m(p['BFV'])}/({m(p['BFV'])} + {m(p['FVW'])}) = {m(CV0)}, with the remaining {m(PR - CV0)} credited to additional paid-in capital. The {p['ER']}% effective rate applies to that {m(CV0)} carrying amount. First period, {p['issue']} to {p['pay1']}: {m(CV0)} × {p['ER']}%/2 = {m(i1)}, against {m(C)} of cash interest, so the carrying amount rises by {m(i1 - C)} to {m(CV1)}. Accrual for the {acc} month{'s' if acc != 1 else ''} to December 31: {m(CV1)} × {p['ER']}%/2 × {acc}/6 = {m(i2)}. Year 1 interest expense = {m(i1)} + {m(i2)} = {m(key_v)}.""",
    )


def debt_covenant_cushion(p):
    """How far defined EBIT could fall before the coverage covenant breaks; an impairment loss on assets
    still in use is not a loss on a sale, so it stays in the defined figure."""
    co, s = p["co"], short(p)
    mn = D(p["min"])
    EBIT = p["NI"] + p["IE"] + p["TAX"] - p["GAIN"] + p["LS"] + p["REST"]
    floor = rd(mn * p["IE"])
    key_v = EBIT - floor
    assert key_v > 0
    pool = {
        "imp_wrong": (m(key_v + p["IMP"]), f"Adds back the {m(p['IMP'])} impairment loss as if the agreement excluded it. The agreement removes only gains and losses on disposals; the production line is still in use, so its impairment stays in earnings before interest and taxes."),
        "incl_gain": (m(key_v + p["GAIN"]), f"Leaves the {m(p['GAIN'])} gain on the equipment sale in earnings before interest and taxes. The agreement removes gains and losses on disposals of property and equipment."),
        "no_ls": (m(key_v - p["LS"]), f"Leaves the {m(p['LS'])} loss on the delivery truck in the figure. The agreement removes every gain or loss on disposing of property and equipment, losses as well as gains, so the loss is added back."),
        "excl_rest": (m(key_v - p["REST"]), f"Doesn't add back the {m(p['REST'])} restructuring charge, which the agreement's definition adds back."),
        "no_tax": (m(key_v - p["TAX"]), f"Doesn't add back the {m(p['TAX'])} of income tax expense. The agreement starts from net income plus interest and income taxes."),
    }
    key = (m(key_v), f"Correct. Defined earnings of {m(EBIT)} less the {m(floor)} minimum ({p['min']} × {m(p['IE'])}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s loan agreement requires its ratio of earnings before interest and taxes to interest expense to be at least {p['min']} at each year-end. For the covenant, earnings before interest and taxes start from net income, add back interest expense, income tax expense and restructuring charges, and remove the effect of any gain or loss on disposing of property and equipment. For Year 1, {s} reports net income of {m(p['NI'])}, interest expense of {m(p['IE'])} and income tax expense of {m(p['TAX'])}. Net income includes a {m(p['GAIN'])} gain on the sale of idle equipment, a {m(p['LS'])} loss on the sale of a delivery truck, a {m(p['REST'])} restructuring charge for closing an underperforming store, and a {m(p['IMP'])} impairment loss on a production line that {s} continues to operate. With interest expense unchanged, by how much could {s}'s Year 1 earnings before interest and taxes, as the agreement defines them, have been lower without breaching the covenant?""",
        choices, ans,
        f"""Earnings before interest and taxes, as defined = {m(p['NI'])} + {m(p['IE'])} + {m(p['TAX'])} − {m(p['GAIN'])} (gain on a disposal, removed) + {m(p['LS'])} (loss on a disposal, removed) + {m(p['REST'])} (restructuring, added back) = {m(EBIT)}. The impairment loss isn't a gain or loss on a disposal, because the line is still in use, so it stays in the figure. The covenant needs at least {p['min']} × {m(p['IE'])} = {m(floor)}. Cushion = {m(EBIT)} − {m(floor)} = {m(key_v)}.""",
    )


FAMILIES = [
    ("far-cash-bank-reconciliation-0006", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (stop-payment orders, checks returned by the bank, processor fees)"],
     bank_recon_stop, [
        dict(co="Falmouth Marine Co.", BB=52400, DIT=5800, OC=9150, RET=1360, CCg=24000, CCn=23400, SP=2850, chk="498", use=["no_ret", "no_fee", "no_stop"]),
        dict(co="Gerrans Boatworks Co.", BB=68900, DIT=7200, OC=11450, RET=2980, CCg=31500, CCn=30690, SP=2240, chk="512", use=["no_stop", "whole", "no_ret"]),
        dict(co="Penryn Chandlery Co.", BB=81200, DIT=6400, OC=13700, RET=1150, CCg=28000, CCn=27300, SP=3460, chk="305", use=["no_fee", "no_stop", "whole"]),
        dict(co="Portmellon Marine Supply Co.", BB=45600, DIT=4900, OC=8300, RET=1720, CCg=19200, CCn=18720, SP=1460, chk="221", use=["no_ret", "no_fee", "whole"]),
     ], "no_stop"),
    ("far-cash-bank-reconciliation-0007", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash; a postdated check is a receivable, not cash)", "Bank reconciliation practice (adjusted balance per bank: deposits in transit, outstanding checks and bank errors)"],
     bank_recon_error, [
        dict(co="Newlyn Trawler Co.", BB=61200, DIT=4300, OC=8750, DEPa=4710, DEPb=4170, INT=420, AD=2240, PD=1850, use=["no_pd", "ad_bank", "int_bank"]),
        dict(co="Porthallow Fisheries Co.", BB=74500, DIT=5600, OC=10200, DEPa=6390, DEPb=4190, INT=510, AD=2630, PD=2180, use=["no_pd", "no_be", "ad_bank"]),
        dict(co="Looe Harbour Supply Co.", BB=58300, DIT=3900, OC=7650, DEPa=5280, DEPb=2580, INT=380, AD=1960, PD=1590, use=["int_bank", "no_pd", "no_be"]),
        dict(co="Cadgwith Fish Market Co.", BB=86700, DIT=6100, OC=12400, DEPa=7130, DEPb=5150, INT=560, AD=3050, PD=2470, use=["no_be", "ad_bank", "int_bank"]),
     ], "no_pd"),
    ("far-cash-unreconciled-0004", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (errors by the bank and by the depositor; unlocated differences)"],
     cash_unrecon_shortage, [
        dict(co="Lerryn Supply Co.", ABB=58900, DD=1240, WIRE=3400, DUP=650, SH=1860, use=["no_dd", "no_wire", "whole"]),
        dict(co="Polkerris Fisheries Co.", ABB=74500, DD=1580, WIRE=4100, DUP=820, SH=2350, use=["no_wire", "no_dup", "whole"]),
        dict(co="Pentewan Chandlery Co.", ABB=49200, DD=960, WIRE=2700, DUP=540, SH=1420, use=["no_dd", "no_dup", "no_wire"]),
        dict(co="Charlestown Harbour Traders Co.", s="Charlestown", ABB=83600, DD=1870, WIRE=4600, DUP=910, SH=2740, use=["no_dd", "no_dup", "whole"]),
     ], "no_dd"),
    ("far-cash-unreconciled-0005", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (errors by the bank and by the depositor)"],
     cash_unrecon_misstated, [
        dict(co="St Keverne Marine Co.", s="St Keverne", BB=66150, DIT=5070, OC=4250, chk="2217", CK=2180, CKe=2810, INSUR=410, DEP=980, CF=300, use=["no_je", "no_be", "no_insur"]),
        dict(co="Portloe Seafood Co.", BB=53400, DIT=3960, OC=3120, chk="1408", CK=1640, CKe=2840, INSUR=320, DEP=740, CF=200, use=["no_be", "no_cf", "no_insur"]),
        dict(co="Gorran Haven Fisheries Co.", s="Gorran Haven", BB=70230, DIT=5140, OC=4010, chk="3365", CK=2350, CKe=3250, INSUR=460, DEP=1050, CF=400, use=["no_je", "no_cf", "no_insur"]),
        dict(co="Philleigh Traders Co.", BB=45060, DIT=3390, OC=2680, chk="0952", CK=1270, CKe=2470, INSUR=270, DEP=610, CF=100, use=["no_je", "no_be", "no_cf"]),
     ], "no_be"),
    ("far-receivables-rollforward-0006", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "ASC 860-10-40-5 (conditions for a transfer of financial assets to be a sale; otherwise a secured borrowing)", "ASC 606-10-55-81 to 55-84 (bill-and-hold arrangements)", "ASC 606-10-45-4 (receivables: unconditional right to consideration)"],
     ar_ledger_postings, [
        dict(co="Portreath Supply Co.", B=520000, Rv=3150000, Cc=3080000, Wo=26000, Rec=72000, BH=48000, CS=94000, use=["no_rec", "no_bh", "cs_wrong"]),
        dict(co="Porthtowan Traders Co.", B=410000, Rv=2460000, Cc=2395000, Wo=21000, Rec=58000, BH=36000, CS=77000, use=["no_bh", "cs_wrong", "cs_coll"]),
        dict(co="Perranarworthal Wholesale Co.", B=630000, Rv=3820000, Cc=3725000, Wo=31000, Rec=85000, BH=55000, CS=112000, use=["no_rec", "cs_wrong", "cs_coll"]),
        dict(co="St Agnes Wholesale Co.", s="St Agnes", B=355000, Rv=2080000, Cc=2030000, Wo=17000, Rec=46000, BH=29000, CS=63000, use=["no_rec", "no_bh", "cs_coll"]),
     ], "no_rec"),
    ("far-receivables-rollforward-0007", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables; credit balances in customer accounts are liabilities; notes receivable reported separately)", "ASC 606-10-25-30 (control passes at shipment under FOB shipping point terms)", "ASC 606-10-25 (cutoff for sales returns)"],
     ar_rollforward_creditbal, [
        dict(co="Flushing Yacht Supply Co.", B=480000, Rv=2920000, Cc=2865000, Wo=24000, NT=12000, CB=15000, RA=9000, SL=21000, use=["no_cb", "no_ra", "no_sl"]),
        dict(co="Gweek Boatyard Co.", B=365000, Rv=2210000, Cc=2168000, Wo=19000, NT=14000, CB=11000, RA=7000, SL=17000, use=["no_cb", "nt_wrong", "no_sl"]),
        dict(co="Helford Marine Co.", B=545000, Rv=3340000, Cc=3268000, Wo=28000, NT=16000, CB=18000, RA=11000, SL=26000, use=["no_ra", "nt_wrong", "no_cb"]),
        dict(co="Manaccan Chandlers Co.", B=298000, Rv=1860000, Cc=1819000, Wo=15000, NT=8000, CB=9000, RA=6000, SL=13000, use=["no_sl", "no_ra", "nt_wrong"]),
     ], "no_cb"),
    ("far-inventory-rollforward-0006", A2, "Inventory", AN,
     ["ASC 330-10-30 (cost of inventory; cash discounts)", "ASC 606-10-55-79 to 55-80 (consignment arrangements)", "Inventory cutoff: FOB shipping point and purchase returns"],
     inv_purchases_line, [
        dict(co="Trewellard Hardware Co.", B=210000, P=1480000, C=1395000, CI=34000, PD=12000, RT=21000, TR=27000, use=["no_pd", "no_ci", "tr_wrong"]),
        dict(co="St Just Builders Supply Co.", s="St Just", B=165000, P=1120000, C=1055000, CI=26000, PD=9000, RT=16000, TR=22000, use=["no_ci", "no_rt", "no_pd"]),
        dict(co="Sennen Timber Co.", B=295000, P=1860000, C=1742000, CI=44000, PD=15000, RT=27000, TR=36000, use=["no_pd", "no_rt", "tr_wrong"]),
        dict(co="St Buryan Supply Co.", s="St Buryan", B=138000, P=940000, C=882000, CI=19000, PD=7000, RT=13000, TR=17000, use=["tr_wrong", "no_ci", "no_rt"]),
     ], "no_pd"),
    ("far-inventory-rollforward-0007", A2, "Inventory", AN,
     ["ASC 330-10-30-1 (cost of inventory includes freight-in)", "ASC 705-20 (consideration received from a vendor: volume rebates reduce the cost of purchases, allocated to goods on hand and goods sold)", "ASC 606-10-55-79 to 55-80 (consignment arrangements: the consignor keeps the goods in inventory)"],
     inv_perpetual_adjust, [
        dict(co="Illogan Metals Supply Co.", B=452000, P=1860000, C=1837000, FI=27000, FO=19000, CO=38000, Q=600000, r=5, H=240000, use=["rb_full", "no_co", "no_fi"]),
        dict(co="Tuckingmill Steel Co.", B=530000, P=2240000, C=2202000, FI=31000, FO=33000, CO=44000, Q=700000, r=4, H=300000, use=["no_rb", "no_co", "fo_in"]),
        dict(co="Troon Alloys Co.", B=330000, P=1450000, C=1438000, FI=34000, FO=21000, CO=26000, Q=450000, r=5, H=180000, use=["no_fi", "rb_full", "no_co"]),
        dict(co="Praze Metals Co.", B=390000, P=1700000, C=1672000, FI=22000, FO=16000, CO=33000, Q=650000, r=4, H=250000, use=["rb_full", "fo_in", "no_fi"]),
     ], "rb_full"),
    ("far-ppe-rollforward-0006", A2, "Property, plant and equipment", AN,
     ["ASC 360-10-30 (cost of property, plant and equipment: costs to bring an asset to its location and condition for use)", "Land improvements as a separate class of property, plant and equipment"],
     ppe_additions, [
        dict(co="Indian Queens Fabrication Co.", s="Indian Queens", AD=640000, FINE=4800, TI=6500, INS=11200, LOT=52000, use=["no_ti", "no_fine", "lot_wrong"]),
        dict(co="Fraddon Castings Co.", AD=430000, FINE=3600, TI=4900, INS=8400, LOT=36000, use=["lot_wrong", "no_ins", "no_ti"]),
        dict(co="St Dennis Metalworks Co.", s="St Dennis", AD=790000, FINE=5200, TI=7800, INS=13600, LOT=61000, use=["no_fine", "no_ins", "no_ti"]),
        dict(co="Roche Quarry Equipment Co.", AD=510000, FINE=4100, TI=5600, INS=9800, LOT=41000, use=["no_ti", "no_ins", "lot_wrong"]),
     ], "no_ti"),
    ("far-intangibles-cloud-computing-0002", A2, "Intangible assets", AP,
     ["ASC 350-40 (internal-use software; implementation costs of a hosting arrangement that is a service contract; amortization over the term of the hosting arrangement from each module's ready-for-use date)", "ASU 2018-15 (customer's accounting for implementation costs in a cloud computing arrangement)", "ASU 2025-06 (targeted improvements to internal-use software; same result here)", "ASC 720-45 (business process reengineering costs expensed)"],
     cloud_modules, [
        dict(co="Perrancombe Logistics Co.", T=4, Rn=2, X=225000, mA=4, Y=117000, mB=10, BPR=36000, use=["full_term", "same_date", "with_renewal"]),
        dict(co="Lanivet Freight Co.", T=5, Rn=3, X=232000, mA=3, Y=130000, mB=9, BPR=42000, use=["from_start", "same_date", "cap_bpr"]),
        dict(co="St Breward Transport Co.", s="St Breward", T=3, Rn=2, X=180000, mA=7, Y=104000, mB=11, BPR=28000, use=["with_renewal", "cap_bpr", "full_term"]),
        dict(co="Blisland Haulage Co.", T=4, Rn=2, X=198000, mA=5, Y=164000, mB=8, BPR=33000, use=["full_term", "from_start", "same_date"]),
     ], "full_term"),
    ("far-exit-costs-0003", A2, "Payables and accrued liabilities", AP,
     ["ASC 420-10-25-4 to 25-9 (one-time employee termination benefits: no future service required, or ratable recognition when service extends beyond the minimum retention period)", "ASC 420-10-25-11 (contract termination costs)", "ASC 420-10-25-13 (costs that continue under a contract without economic benefit: recognized at the cease-use date)"],
     exit_cost_timing, [
        dict(co="Penzance Contact Services Co.", s="Penzance", A=840000, NB=12, SB=15000, K=65000, SVC=4200, svc_end="September 30", after=5, elapsed=2, total=6, n=70, comm="November 1", close="April 30", use=["stay_full", "incl_sev", "no_k"]),
        dict(co="Truro Customer Care Co.", s="Truro", A=615000, NB=9, SB=12000, K=48000, SVC=3600, svc_end="July 31", after=4, elapsed=3, total=6, n=55, comm="October 1", close="March 31", use=["no_svc", "no_k", "stay_full"]),
        dict(co="Kenwyn Teleservices Co.", A=980000, NB=14, SB=14000, K=72000, SVC=5100, svc_end="June 30", after=3, elapsed=4, total=7, n=85, comm="September 1", close="March 31", use=["stay_full", "no_svc", "incl_sev"]),
        dict(co="Holywell Support Services Co.", A=725000, NB=10, SB=16000, K=55000, SVC=3900, svc_end="September 30", after=6, elapsed=1, total=4, n=60, comm="December 1", close="March 31", use=["no_k", "no_svc", "stay_full"]),
     ], "stay_full"),
    ("far-bonds-warrants-0001", A2, "Debt (Notes and bonds payable)", AP,
     ["ASC 470-20-25-2 (debt issued with detachable stock purchase warrants: allocation by relative fair value)", "ASC 835-30-35-2 (effective interest method)"],
     bonds_warrants_interest, [
        dict(co="St Germans Energy Corp.", s="St Germans", F=1000000, SR=6, ER=8, BFV=882000, FVW=60000, issue="April 1", pay1="September 30", pay2="March 31", acc=3, use=["face_alloc", "bfv_alloc", "no_accrual"]),
        dict(co="Gunnislake Power Corp.", F=800000, SR=5, ER=7, BFV=700000, FVW=45000, issue="May 1", pay1="October 31", pay2="April 30", acc=2, use=["bfv_alloc", "face_alloc", "no_accrual"]),
        dict(co="St Cleer Utilities Corp.", s="St Cleer", F=1200000, SR=4, ER=6, BFV=1042000, FVW=70000, issue="February 1", pay1="July 31", pay2="January 31", acc=5, use=["stated_only", "bfv_alloc", "no_accrual"]),
        dict(co="Darite Energy Corp.", F=600000, SR=7, ER=9, BFV=533000, FVW=30000, issue="June 1", pay1="November 30", pay2="May 31", acc=1, use=["face_alloc", "bfv_alloc", "stated_only"]),
     ], "face_alloc"),
    ("far-debt-covenant-0003", A2, "Debt (Debt covenant compliance)", AP,
     ["Debt covenant compliance: interest coverage as defined in the loan agreement"],
     debt_covenant_cushion, [
        dict(co="St Columb Components Inc.", s="St Columb", NI=1265000, IE=310000, TAX=360000, GAIN=85000, LS=36000, REST=140000, IMP=120000, min="4.00", use=["imp_wrong", "no_ls", "excl_rest"]),
        dict(co="Stratton Fabrication Inc.", NI=980000, IE=245000, TAX=285000, GAIN=62000, LS=27000, REST=108000, IMP=94000, min="4.25", use=["excl_rest", "no_ls", "imp_wrong"]),
        dict(co="Kilkhampton Castings Inc.", NI=1460000, IE=365000, TAX=420000, GAIN=96000, LS=41000, REST=172000, IMP=138000, min="4.10", use=["incl_gain", "no_ls", "imp_wrong"]),
        dict(co="Widemouth Machine Works Inc.", NI=870000, IE=218000, TAX=252000, GAIN=54000, LS=23000, REST=95000, IMP=77000, min="4.00", use=["incl_gain", "excl_rest", "no_ls"]),
     ], "imp_wrong"),
]


def names_unique():
    """No company name or short name repeats within the batch (gate finding)."""
    seen = {}
    for fid, *_rest in FAMILIES:
        for k, p in enumerate(_rest[-2]):
            for nm in (p["co"], short(p)):
                assert nm not in seen, f"{fid} v{k}: {nm!r} already used by {seen[nm]}"
                seen[nm] = f"{fid} v{k}"
            assert len(short(p)) > 3 or short(p) == "Looe", f"{fid} v{k}: short name {short(p)!r} is too short"


def blind_files(items, scratch):
    """Stems and lettered choices only, for the blind verifier, plus a separate key file."""
    lines, keys = ["# FAR batch 15 (revision 2): blind verification input", "",
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
    names_unique()
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
