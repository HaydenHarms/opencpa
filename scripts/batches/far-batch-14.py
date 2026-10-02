"""FAR batch 14 — 18 items written from scratch.

Slice A: 13 Remembering and Understanding word items, one on each blueprint task that still had only one
item (python scripts/far-coverage.py): I.A.3a, I.A.3b, I.B.1a, I.B.2a, I.B.3a, I.D.a, I.D.b, I.E.a, I.F.a,
II.E.1a, II.E.2a, II.E.3a, II.H.1a. Each tests a different aspect of its task than the existing item (not
a reword). No variants (hard rule for Recall items).

Slice B: 5 Area I Analysis families with three variants each, one on each of I.A.1c, I.A.4c, I.A.5c, I.A.6c
(wholly owned / with NCI, no acquisition-date accounting), I.A.7b. Each uses a stem format different from
every existing item on its task and changes at least two of the scenario's component events.

Run: python3 scripts/batches/far-batch-14.py [--dry-run]
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import json
import os
import re
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AN, RU, attach_variants, audit, finalize, fix_articles, mcq as _mcq, variant, write_items  # noqa: E402
from variants import m, pick, rd  # noqa: E402

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
NOTE = "Batch 14. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
SCRATCH = os.environ.get("B14_SCRATCH")


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


def family(id, area, topic, skill, refs, build, params, twist, asof=None):
    """An item built from parameter set 0, with sets 1-3 kept for its variants."""
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
    return it


def short(name):
    return name.split()[0]


def build(pool, key, use):
    items = [pool[k] for k in use] + [key]
    vals = [t for t, _ in items]
    assert len(set(vals)) == len(vals), f"duplicate choice text: {vals}"
    return pick(pool, key, use)


def ou(x, noun):
    """A signed misstatement as '$12,000 overstated' / '$12,000 understated', for a named total."""
    x = D(x)
    assert x != 0
    return f"{m(abs(x))} {noun} {'overstated' if x > 0 else 'understated'}"


def chg(x):
    x = D(x)
    assert x != 0
    return f"{m(x)} increase" if x > 0 else f"{m(-x)} decrease"


# ── Area I Analysis families ─────────────────────────────────────────────


def bs_current_assets(p):
    co, s = p["co"], short(p["co"])
    T, cur_months = 20, 12
    monthly = D(p["P"]) / T
    remain = T - p["R"]
    pr_bal = rd(monthly * remain)
    nc_prepaid = rd(monthly * (remain - cur_months)) if remain > cur_months else D(0)
    E = p["C"] + p["Sc"] + p["AR"] + p["N"] + p["I"] + pr_bal + p["RC"]
    key_total = E + (p["Sf"] - p["Sc"]) - p["N"] - nc_prepaid - p["RC"]
    diff = E - key_total
    pool = {
        "sec": (ou(diff + (p["Sf"] - p["Sc"]), "current assets"), f"Leaves the trading securities at their {m(p['Sc'])} cost instead of their {m(p['Sf'])} fair value. Since ASU 2016-01, equity securities with a readily determinable fair value are measured at fair value through net income, with no cost-basis alternative."),
        "note": (ou(diff - p["N"], "current assets"), f"Keeps the {m(p['N'])} note receivable due in eighteen months in current assets. An asset collectible more than twelve months after the balance sheet date is noncurrent."),
        "prepaid": (ou(diff - nc_prepaid, "current assets"), f"Reports the entire {m(pr_bal)} of unexpired insurance as current. Only the {cur_months} months' worth expiring within a year, {m(rd(monthly * cur_months))}, is current; the {m(nc_prepaid)} covering later months is noncurrent."),
        "restricted": (ou(diff - p["RC"], "current assets"), f"Includes the {m(p['RC'])} compensating-balance deposit, restricted under the loan agreement until it matures in eighteen months, as unrestricted current cash. Cash whose use is restricted beyond one year is excluded from current assets."),
    }
    key = (ou(diff, "current assets"), f"Correct. {m(E)} draft − {m(key_total)} corrected: + fair-value write-up {m(p['Sf'] - p['Sc'])} − note {m(p['N'])} − noncurrent prepaid {m(nc_prepaid)} − restricted cash {m(p['RC'])} = {m(diff)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""In its draft classified balance sheet dated December 31, Year 1, {co} reports total current assets of {m(E)}: cash of {m(p['C'] + p['RC'])}, equity securities held for trading, at cost, of {m(p['Sc'])}, accounts receivable (including the note described below) of {m(p['AR'] + p['N'])}, inventory of {m(p['I'])}, and prepaid insurance of {m(pr_bal)}. Supporting records show: the trading securities' fair value at December 31 is {m(p['Sf'])}; {m(p['N'])} of the receivables is a note from a customer due in eighteen months; the prepaid insurance is the unexpired balance of a {T}-month policy, {p['R']} months of which had elapsed by December 31; and {m(p['RC'])} of the cash is a compensating balance that {s}'s loan agreement restricts from use until the loan matures in eighteen months. By how much is {s}'s draft total current assets overstated or understated?""",
        choices, ans,
        f"""Trading equity securities are measured at fair value through net income, so cost is replaced with the {m(p['Sf'])} fair value, a {m(p['Sf'] - p['Sc'])} write-up. The {m(p['N'])} note collectible in eighteen months is noncurrent. Of the {m(pr_bal)} unexpired insurance ({T - p['R']} months remaining), only {cur_months} months, {m(rd(monthly * cur_months))}, expires within a year; the remaining {m(nc_prepaid)} is noncurrent. The {m(p['RC'])} compensating balance is restricted beyond one year and is excluded from current assets. Corrected total current assets = {m(key_total)}, so the draft's {m(E)} is {ou(diff, 'current assets')}.""",
    )


def equity_pairs(p):
    co, s = p["co"], short(p["co"])
    par_amt = p["O"] * p["PV"]
    fv_amt = p["O"] * p["FVsh"]
    apic_inc_draft = fv_amt - par_amt
    tgain = p["TProceeds"] - p["TCost"]
    draft_re = p["B"] + p["NI"] - p["Dc"] - fv_amt + tgain
    draft_apic = p["ApB"] + apic_inc_draft
    key_re = p["B"] - p["Xc"] + p["NI"] - p["Dc"] - par_amt
    key_apic = p["ApB"] + tgain
    assert draft_re > 0, f"{co}: draft retained earnings is negative ({draft_re})"

    def pair(re_, apic_):
        assert re_ > 0 and apic_ > 0, f"{co}: a choice amount is not positive ({re_}; {apic_})"
        return f"{m(re_)}; {m(apic_)}"
    pool = {
        "stockdiv": (pair(p["B"] - p["Xc"] + p["NI"] - p["Dc"] - fv_amt, p["ApB"] + apic_inc_draft + tgain),
                     f"Keeps the stock dividend at its {m(fv_amt)} fair value, crediting {m(apic_inc_draft)} to additional paid-in capital. A dividend of {p['pct']}% of the shares outstanding is large enough that ASC 505-20 treats it like a stock split effected in dividend form: retained earnings is reduced only by the {m(par_amt)} par value of the new shares, with no additional paid-in capital."),
        "treasury": (pair(p["B"] - p["Xc"] + p["NI"] - p["Dc"] - par_amt + tgain, p["ApB"]),
                     f"Keeps the {m(tgain)} gain on reissuing the treasury shares in retained earnings. Gains on treasury stock transactions are credited to additional paid-in capital, not retained earnings."),
        "noxc": (pair(p["B"] + p["NI"] - p["Dc"] - par_amt, key_apic),
                 f"Leaves beginning retained earnings at its previously reported {m(p['B'])}. The {m(p['Xc'])} of Year 1 advertising expense that was never recorded understated Year 1 expense, so it is corrected by reducing beginning retained earnings."),
        "combo": (pair(p["B"] - p["Xc"] + p["NI"] - p["Dc"] - fv_amt + tgain, p["ApB"] + apic_inc_draft),
                  f"Keeps the stock dividend at its {m(fv_amt)} fair value and keeps the {m(tgain)} treasury-stock gain in retained earnings, correcting only the advertising-expense error. Both the stock dividend and the treasury gain still need correcting, as in the other wrong answers above."),
    }
    key = (pair(key_re, key_apic), f"Correct retained earnings: {m(p['B'])} − {m(p['Xc'])} + {m(p['NI'])} − {m(p['Dc'])} − {m(par_amt)} = {m(key_re)}. Correct additional paid-in capital: {m(p['ApB'])} + {m(tgain)} = {m(key_apic)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 statement of changes in equity reports ending retained earnings of {m(draft_re)}, built from beginning retained earnings of {m(p['B'])} (as previously reported), plus net income of {m(p['NI'])}, less cash dividends of {m(p['Dc'])}, less a {p['pct']}% stock dividend recorded at its {m(fv_amt)} fair value (par value {m(par_amt)}), plus a {m(tgain)} gain on reissuing treasury shares, credited to retained earnings. It reports ending additional paid-in capital of {m(draft_apic)}, made up of a beginning balance of {m(p['ApB'])} plus the {m(apic_inc_draft)} excess of the stock dividend's fair value over par. During the review, the controller finds that {m(p['Xc'])} of Year 1 advertising expense, properly incurred that year, was never recorded in any period. What should {s}'s corrected ending retained earnings and ending additional paid-in capital be?""",
        choices, ans,
        f"""The {p['pct']}% stock dividend is large enough to be accounted for like a stock split in dividend form (ASC 505-20-25): retained earnings is reduced only by the {m(par_amt)} par value of the new shares, and no additional paid-in capital is recognized, so the draft's {m(apic_inc_draft)} addition to additional paid-in capital is reversed. The {m(tgain)} gain on reissuing treasury stock belongs in additional paid-in capital, not retained earnings. The unrecorded {m(p['Xc'])} of Year 1 advertising expense is a correction of an error, reducing beginning retained earnings. Corrected retained earnings = {m(key_re)}; corrected additional paid-in capital = {m(key_apic)}.""",
    )


def scf_financing(p):
    co, s = p["co"], short(p["co"])
    F = p["Bp"] - p["Nr"] - p["Dc"] + p["Sp"] - p["Lt"]
    key_v = F + p["Li"] - p["Tp"] + p["Op"]
    pool = {
        "lease": (chg(F - p["Tp"] + p["Op"] - F), f"Reports the full {m(p['Lt'])} finance lease payment as financing. Only the {m(p['Lt'] - p['Li'])} principal portion is a financing outflow; the {m(p['Li'])} interest portion is an operating outflow."),
        "treasury": (chg(F + p["Li"] + p["Op"] - F), f"Leaves out the {m(p['Tp'])} payment to reacquire treasury stock, which was recorded directly against additional paid-in capital with no cash flow statement entry. Treasury stock purchases are financing outflows."),
        "op": (chg(F + p["Li"] - p["Tp"] - F), f"Leaves the {m(p['Op'])} of proceeds from employee stock option exercises in operating activities. Proceeds from issuing stock, including on option exercises, are financing inflows."),
        "combo": (chg(F + p["Op"] - F), f"Leaves the full {m(p['Lt'])} lease payment in financing with no split for the {m(p['Li'])} interest portion, and leaves out the {m(p['Tp'])} treasury stock purchase entirely, while correctly moving the {m(p['Op'])} of option proceeds into financing."),
    }
    key = (chg(key_v - F), f"Correct. + {m(p['Li'])} lease interest reclassified to operating − {m(p['Tp'])} treasury purchase added − {m(p['Op'])} option proceeds reclassified from operating = {m(key_v - F)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""In its draft Year 2 statement of cash flows, {co} reports net cash provided by financing activities totaling {m(F)}: proceeds from issuing bonds {m(p['Bp'])}; repayment of a long-term note ({m(p['Nr'])}); cash dividends paid ({m(p['Dc'])}); proceeds from issuing common stock {m(p['Sp'])}; and payments on a finance lease ({m(p['Lt'])}), all of which was classified as financing. Supporting records show: of the {m(p['Lt'])} finance lease payment, {m(p['Li'])} is interest and {m(p['Lt'] - p['Li'])} is principal; {s} paid {m(p['Tp'])} during the year to reacquire its own shares as treasury stock, recorded only as a reduction of additional paid-in capital with no related cash flow statement entry; and {m(p['Op'])} of proceeds from employees exercising stock options was included in the draft's operating activities. By how much does {s}'s net cash provided by financing activities change when these items are corrected?""",
        choices, ans,
        f"""Only the {m(p['Lt'] - p['Li'])} principal portion of a finance lease payment is a financing outflow; the {m(p['Li'])} interest portion is operating, so {m(p['Li'])} moves back into financing. The {m(p['Tp'])} treasury stock purchase, a financing outflow, was omitted entirely and must be added. Proceeds from stock option exercises are financing inflows, so the {m(p['Op'])} misclassified as operating moves into financing. Corrected financing activities = {m(F)} + {m(p['Li'])} − {m(p['Tp'])} + {m(p['Op'])} = {m(key_v)}, a {chg(key_v - F)}.""",
    )


def consolidated_ni_parent(p):
    co1, co2 = p["p"], p["sub"]
    s1 = short(p["p"])
    UP = rd(D(p["SP"] - p["SC"]) * D(p["X"]) / 100)
    key_v = p["Pni"] - p["DivInc"] + D("0.90") * (p["Sni"] - UP + p["Dep"])
    pool = {
        "div": (m(key_v + p["DivInc"]), f"Keeps the {m(p['DivInc'])} of dividend income {s1} recorded from {co2}. An intercompany dividend is eliminated entirely against the investment account; it isn't part of either company's income in the consolidated statements."),
        "up": (m(key_v + D("0.90") * UP), f"Leaves the {m(UP)} of unrealized profit on {co2}'s upstream sale in {co2}'s income before allocating it. The unrealized profit must be removed before splitting {co2}'s income between {s1} and the noncontrolling interest."),
        "dep": (m(key_v - D("0.90") * p["Dep"]), f"Leaves out the {m(p['Dep'])} of excess depreciation that continues to be added back from {co2}'s intercompany equipment sale in an earlier year."),
        "nonci": (m(p["Pni"] - p["DivInc"] + p["Sni"] - UP + p["Dep"]), f"Treats all of {co2}'s adjusted income as {s1}'s, allocating none of it to the 10% noncontrolling interest."),
    }
    key = (m(key_v), f"Correct. {m(p['Pni'])} − {m(p['DivInc'])} + 90% × ({m(p['Sni'])} − {m(UP)} + {m(p['Dep'])}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co1} owns 90% of {co2}'s voting stock, acquired in an earlier year; {co1} does not use the equity method on its own books. For Year 2, {co1} reports net income from its own operations, including {m(p['DivInc'])} of dividend income it received from {co2}, of {m(p['Pni'])}; {co2} reports net income of {m(p['Sni'])}. During Year 2, {co2} sold goods to {co1} for {m(p['SP'])} that cost {co2} {m(p['SC'])}, and {co1} still held {p['X']}% of those goods at year-end. {co2} also sold equipment to {co1} in an earlier year at a gain, and Year 2 is the first year in which {co1}'s depreciation on that equipment, based on its cost to {co1}, exceeds what consolidated depreciation should be (based on {co2}'s original cost) by {m(p['Dep'])}. What net income is attributable to {s1}'s shareholders for Year 2?""",
        choices, ans,
        f"""The {m(p['DivInc'])} of intercompany dividend income is eliminated entirely; it isn't consolidated income. {co2}'s income is reduced by the {m(UP)} unrealized profit on its upstream sale ({m(p['SP'] - p['SC'])} gross profit × {p['X']}% unsold) and increased by the {m(p['Dep'])} of excess depreciation being eliminated this year, both before the income is split 90/10. Net income attributable to {s1}'s shareholders = {m(p['Pni'])} − {m(p['DivInc'])} + 90% × ({m(p['Sni'])} − {m(UP)} + {m(p['Dep'])}) = {m(key_v)}.""",
    )


def notes_vs_statements(p):
    co, s = p["co"], short(p["co"])
    err, E = p["err"], p["Err"]
    true = {"cl": p["CLt"], "warr": p["WARRt"], "intan": p["INt"], "eq": p["EQt"]}
    stmt = dict(true)
    stmt[err] = true[err] + E
    labels = {"cl": "contract liabilities", "warr": "accrued warranty liability",
              "intan": "intangible assets, net", "eq": "investments in equity securities"}
    match_rat = {
        "cl": f"The contract liabilities note describes {m(true['cl'])} of advance customer payments, all expected to be recognized as revenue within a year, which matches the {m(stmt['cl'])} on the balance sheet.",
        "warr": f"The warranty note's expected-cost estimate of {m(true['warr'])} matches the {m(stmt['warr'])} accrued warranty liability on the balance sheet.",
        "intan": f"The intangibles note's {m(true['intan'])} of remaining patent cost matches the {m(stmt['intan'])} intangible assets on the balance sheet.",
        "eq": f"The equity securities note's {m(true['eq'])} fair value matches the {m(stmt['eq'])} investment balance on the balance sheet.",
    }
    mismatch_rat = {
        "cl": f"Correct. The note describes {m(true['cl'])} of advance customer payments expected to be recognized within a year, but the balance sheet reports contract liabilities of {m(stmt['cl'])}, {m(E)} more than the note supports.",
        "warr": f"Correct. The warranty note estimates the liability, under the expected cost method, at {m(true['warr'])}, but the balance sheet reports an accrued warranty liability of {m(stmt['warr'])}, {m(E)} less than the note supports.",
        "intan": f"Correct. The intangibles note supports {m(true['intan'])} of remaining patent cost, but the balance sheet reports intangible assets, net, of {m(stmt['intan'])}, {m(E)} more than the note supports.",
        "eq": f"Correct. The equity securities note gives a fair value of {m(true['eq'])}, but the balance sheet reports the investment at {m(stmt['eq'])}, {m(E)} less than the note supports.",
    }
    pool = {k: (f"{m(stmt[k])} of {labels[k]}", match_rat[k]) for k in true if k != err}
    key = (f"{m(stmt[err])} of {labels[err]}", mismatch_rat[err])
    choices, ans = build(pool, key, p["use"])
    stem = f"""Before {co}'s financial statements for the year ended December 31, Year 1, go out, a senior accountant ties its draft notes back to the draft statements. The draft balance sheet reports contract liabilities of {m(stmt['cl'])}; an accrued warranty liability of {m(stmt['warr'])}; intangible assets, net, of {m(stmt['intan'])}; and investments in equity securities of {m(stmt['eq'])}. The draft notes say: the contract liabilities are advance payments from customers for goods not yet delivered, all of which are expected to be recognized as revenue within one year, totaling {m(true['cl'])}; the warranty liability, estimated under the expected cost method over the one-year warranty period, is {m(true['warr'])}; the intangible assets consist of a patent with {m(true['intan'])} of remaining cost, amortized over its {p['yrs']}-year remaining legal life; and the equity securities, which have readily determinable fair values, have a fair value of {m(true['eq'])}, with changes in fair value recognized in net income. Which of these draft statement balances is inconsistent with its note?"""
    explanation = f"""{mismatch_rat[err]} The other three balances agree with their notes: {', '.join(match_rat[k] for k in true if k != err)}"""
    return variant(stem, choices, ans, explanation)


# ── Area I Analysis families registry ────────────────────────────────────

FAMILIES = [
    ("far-balance-sheet-0010", A1, "Classified balance sheet", AN,
     ["ASC 321-10-35 (equity securities with a readily determinable fair value measured at fair value through net income, after ASU 2016-01)",
      "ASC 210-10-45 (current asset classification: collection or use within one year or the operating cycle)",
      "ASC 340-10-05 (prepaid expenses: the unexpired cost applicable to each future period)"],
     bs_current_assets, [
        dict(co="Trevelyan Retail Co.", C=155000, Sc=50000, Sf=62000, AR=240000, N=35000, I=310000, P=40000, R=5, RC=25000, use=["sec", "note", "prepaid"]),
        dict(co="Minehead Retail Co.", C=118000, Sc=36000, Sf=27000, AR=175000, N=22000, I=228000, P=24000, R=4, RC=19000, use=["note", "prepaid", "restricted"]),
        dict(co="Dulverton Retail Co.", C=202000, Sc=64000, Sf=79000, AR=312000, N=46000, I=398000, P=60000, R=6, RC=33000, use=["sec", "prepaid", "restricted"]),
        dict(co="Porlock Retail Co.", C=96000, Sc=28000, Sf=34000, AR=140000, N=18000, I=176000, P=20000, R=5, RC=14000, use=["sec", "note", "restricted"]),
     ], "sec"),
    ("far-changes-in-equity-0009", A1, "Statement of changes in equity", AN,
     ["ASC 505-20-25 (a stock dividend of 20-25% or more is accounted for like a split, at par value, not fair value)",
      "ASC 505-30-30 (gains on treasury stock transactions credited to additional paid-in capital)",
      "ASC 250-10-45 (correction of an error in previously issued financial statements: restate beginning retained earnings)"],
     equity_pairs, [
        dict(co="Ashcombe Corp.", B=900000, Xc=25000, NI=310000, Dc=85000, ApB=650000, O=12000, PV=1, FVsh=15, pct=30, TCost=40000, TProceeds=56000, use=["stockdiv", "combo", "treasury"]),
        dict(co="Bickleigh Corp.", B=1150000, Xc=31000, NI=420000, Dc=110000, ApB=820000, O=15400, PV=1, FVsh=18, pct=28, TCost=55000, TProceeds=81000, use=["stockdiv", "combo", "noxc"]),
        dict(co="Chagford Corp.", B=760000, Xc=24000, NI=265000, Dc=70000, ApB=540000, O=9600, PV=1, FVsh=12, pct=32, TCost=30000, TProceeds=48000, use=["combo", "treasury", "noxc"]),
        dict(co="Doddiscombe Corp.", B=1340000, Xc=26000, NI=485000, Dc=128000, ApB=960000, O=16900, PV=2, FVsh=14, pct=26, TCost=62000, TProceeds=95000, use=["stockdiv", "treasury", "noxc"]),
     ], "stockdiv"),
    ("far-cash-flows-0017", A1, "Statement of cash flows", AN,
     ["ASC 230-10-45-15 (financing activities: proceeds from issuing stock and treasury stock purchases)",
      "ASC 842-20-45-5 (a finance lease's principal payment is financing; interest is operating)"],
     scf_financing, [
        dict(co="Elberton Freight Co.", Bp=600000, Nr=150000, Dc=90000, Sp=80000, Lt=120000, Li=40000, Tp=60000, Op=90000, use=["lease", "combo", "treasury"]),
        dict(co="Falstone Freight Co.", Bp=480000, Nr=110000, Dc=65000, Sp=55000, Lt=90000, Li=28000, Tp=45000, Op=62000, use=["op", "combo", "treasury"]),
        dict(co="Greenhead Freight Co.", Bp=720000, Nr=190000, Dc=120000, Sp=100000, Lt=150000, Li=52000, Tp=78000, Op=115000, use=["op", "lease", "combo"]),
        dict(co="Haltwhistle Freight Co.", Bp=390000, Nr=85000, Dc=48000, Sp=42000, Lt=70000, Li=21000, Tp=33000, Op=48000, use=["op", "lease", "treasury"]),
     ], "lease"),
    ("far-consolidated-statements-0012", A1, "Consolidated financial statements", AN,
     ["ASC 810-10-45-20 (unrealized intercompany profit eliminated before allocating subsidiary income between the parent and the noncontrolling interest)",
      "ASC 810-10-45-1 (intercompany dividends eliminated in consolidation)",
      "ASC 810-10-45-16 (allocating net income between the controlling and noncontrolling interests)"],
     consolidated_ni_parent, [
        dict(p="Allendale Corp.", sub="Blanchland Inc.", Pni=500000, DivInc=36000, Sni=300000, SP=120000, SC=80000, X=25, Dep=8000, use=["div", "up", "nonci"]),
        dict(p="Catton Corp.", sub="Dotland Inc.", Pni=640000, DivInc=45000, Sni=380000, SP=150000, SC=95000, X=30, Dep=11000, use=["up", "dep", "nonci"]),
        dict(p="Elsdon Corp.", sub="Featherstone Inc.", Pni=420000, DivInc=27000, Sni=255000, SP=95000, SC=62000, X=20, Dep=6500, use=["div", "dep", "nonci"]),
        dict(p="Gunnerton Corp.", sub="Harwood Inc.", Pni=575000, DivInc=39000, Sni=330000, SP=130000, SC=88000, X=35, Dep=9500, use=["div", "up", "dep"]),
     ], "nonci"),
    ("far-notes-0009", A1, "Notes to financial statements", AN,
     ["ASC 606-10-45-2 (contract liabilities for consideration received before performance)",
      "ASC 450-20-25 (accrual of a warranty liability under the expected cost method)",
      "ASC 321-10-35 (equity securities with a readily determinable fair value measured at fair value through net income)"],
     notes_vs_statements, [
        dict(co="Hexham Textiles Co.", CLt=64000, WARRt=55000, INt=210000, EQt=95000, Err=13000, yrs=3, err="warr", use=["cl", "intan", "eq"]),
        dict(co="Ingleby Textiles Co.", CLt=58000, WARRt=37000, INt=185000, EQt=103000, Err=15000, yrs=4, err="intan", use=["cl", "warr", "eq"]),
        dict(co="Juniper Textiles Co.", CLt=71000, WARRt=29000, INt=226000, EQt=88000, Err=9000, yrs=5, err="eq", use=["cl", "warr", "intan"]),
        dict(co="Kielder Textiles Co.", CLt=49000, WARRt=33000, INt=198000, EQt=112000, Err=12000, yrs=2, err="cl", use=["warr", "intan", "eq"]),
     ], "intan"),
]


# ── Word items (Remembering and Understanding; no variants) ──────────────

WORD_ITEMS = [
    mcq("far-comprehensive-income-0005", A1, "Statement of comprehensive income", RU,
        ["ASC 220-10-05 (comprehensive income: the change in equity from nonowner sources)",
         "ASC 505-10-50 (transactions with owners, such as issuing stock, dividends and treasury purchases, excluded from comprehensive income)"],
        """During Year 2, Thornbury Co. reports net income of $340,000 and an unrealized holding loss of $25,000 on its available-for-sale debt securities. It also issues common stock for $200,000 cash, declares cash dividends of $60,000, and reacquires $45,000 of its own shares as treasury stock. What should Thornbury report as comprehensive income for Year 2?""",
        [("Net income less the unrealized holding loss, $315,000", "Correct. Comprehensive income is net income plus other comprehensive income. The stock issuance, dividends and treasury purchase are transactions with owners and are excluded."),
         ("Net income alone, $340,000, since the loss is unrealized and stays out of any performance measure", "Other comprehensive income is still part of comprehensive income even though its components are unrealized; it is simply kept out of net income."),
         ("Net income, less the OCI loss, less the dividends and the treasury purchase, plus the stock issuance, $390,000", "Mixes in transactions with owners. Issuing stock, paying dividends and buying treasury stock change equity, but not through nonowner sources, so none of them enters comprehensive income."),
         ("Net income, less the OCI loss and the treasury purchase, $270,000", "The treasury stock purchase is a transaction with an owner (the selling shareholder) and does not affect comprehensive income.")],
        "A",
        """Comprehensive income is the change in equity from nonowner sources during a period: net income plus other comprehensive income (ASC 220-10-05). Transactions with owners, such as issuing stock, declaring dividends and purchasing treasury stock, change equity but are excluded from both net income and other comprehensive income. Thornbury's comprehensive income is $340,000 net income minus the $25,000 unrealized loss on available-for-sale debt securities, $315,000."""),

    mcq("far-comprehensive-income-0006", A1, "Statement of comprehensive income", RU,
        ["ASC 326-30-35 (credit losses on available-for-sale debt securities recognized through an allowance, in net income, after ASU 2016-13)",
         "ASC 825-10-45-5 (the portion of a change in the fair value of a fair-value-option liability attributable to the entity's own instrument-specific credit risk reported in other comprehensive income)",
         "ASC 220-10-45 (items of other comprehensive income, including foreign currency translation adjustments)"],
        """During Year 2, Dunwich Corp. (1) recognizes an unrealized holding gain on an available-for-sale debt security; (2) recognizes a credit loss on a different available-for-sale debt security through an allowance for credit losses; (3) has elected the fair value option for a liability, and identifies the portion of the change in that liability's fair value attributable to Dunwich's own instrument-specific credit risk; and (4) translates the financial statements of a foreign subsidiary whose functional currency is not the dollar, producing a translation adjustment. Which of these is reported in net income rather than other comprehensive income?""",
        [("The credit loss recognized on the available-for-sale debt security", "Correct. Since ASU 2016-13, a credit loss on an available-for-sale debt security is recognized through an allowance for credit losses, with the loss (and any later recovery) in net income, rather than as a direct write-down through other comprehensive income."),
         ("The unrealized holding gain on the available-for-sale debt security", "Unrealized holding gains and losses on available-for-sale debt securities, apart from any credit loss component, are reported in other comprehensive income."),
         ("The instrument-specific credit risk portion of the fair-value-option liability's fair value change", "The portion of the change in fair value of a liability measured under the fair value option that is attributable to the entity's own credit risk is reported in other comprehensive income, not net income."),
         ("The foreign currency translation adjustment", "Foreign currency translation adjustments from consolidating a foreign subsidiary are reported in other comprehensive income, not net income.")],
        "A",
        """Other comprehensive income includes unrealized holding gains and losses on available-for-sale debt securities (apart from credit losses), the instrument-specific credit risk portion of a fair-value-option liability's change in fair value (ASC 825-10-45-5), and foreign currency translation adjustments (ASC 220-10-45). Since ASU 2016-13, a credit loss on an available-for-sale debt security is no longer a direct write-down of the security; it is recognized through an allowance, with the credit loss (and any later recovery) in net income (ASC 326-30-35)."""),

    mcq("far-nfp-financial-position-0006", A1, "Statement of financial position (Not-for-Profit)", RU,
        ["ASC 958-210 (statement of financial position; liquidity and availability of resources)"],
        """Marshwood Museum, a nongovernmental not-for-profit entity, is deciding how to present assets and liabilities on its statement of financial position. Which of the following correctly describes a requirement for that presentation?""",
        [("It may order assets and liabilities by nearness to cash and maturity", "Correct. A not-for-profit entity is not required to present a classified balance sheet; it may instead order items by nearness to cash and maturity, so long as the statement, the notes, or both convey information about liquidity and the availability of resources."),
         ("It must present a classified balance sheet, separating current and noncurrent assets and liabilities", "A classified presentation is permitted but not required. An unclassified presentation, sequenced by nearness to cash and maturity, is also acceptable."),
         ("It must report each donor restriction in a separate column of net assets", "Net assets are reported in only two classes, with and without donor restrictions; the composition of each class, including individual restrictions, is disclosed in the notes, not displayed in separate columns."),
         ("It must report three classes of net assets, matching the entity's unrestricted, temporarily restricted and permanently restricted funds", "Since ASU 2016-14, net assets are reported in two classes, with and without donor restrictions, not three.")],
        "A",
        """ASC 958-210 does not require a not-for-profit entity to classify assets and liabilities as current and noncurrent. It may instead present them in order of nearness to cash and maturity, so long as the statement, the notes, or both convey information about liquidity and the availability of resources to meet near-term cash needs. Net assets are reported in two classes, with and without donor restrictions, since ASU 2016-14 eliminated the three-class presentation."""),

    mcq("far-nfp-net-assets-0002", A1, "Statement of activities (Not-for-Profit)", RU,
        ["ASC 958-225-05 (purpose of the statement of activities: a period's revenues, expenses, gains, losses and reclassifications, by net asset class)"],
        """A new controller preparing the first annual report for Wyre Forest Trust, a not-for-profit entity, asks what the statement of activities is meant to show. Which answer correctly states its purpose?""",
        [("The entity's revenues, expenses, gains, losses and reclassifications, by net asset class and in total", "Correct. The statement of activities reports the change in net assets for the period, both in total and separately for the classes with and without donor restrictions."),
         ("The entity's cash receipts and payments for the period, classified into operating, investing and financing activities", "That description fits the statement of cash flows, not the statement of activities."),
         ("The entity's assets, liabilities and net assets at a single date, split between the two net asset classes", "That description fits the statement of financial position, which reports balances at a point in time, not activity over a period."),
         ("Each program's and supporting activity's expenses, classified by both their natural and functional categories", "That description fits the statement of functional expenses (or an equivalent note), one of several ways functional expense information may be presented, not the statement of activities.")],
        "A",
        """The statement of activities reports the change in a not-for-profit entity's net assets for a period: its revenues, expenses, gains, losses, and reclassifications between net assets with and without donor restrictions, presented in total and by net asset class (ASC 958-225). It is a period statement, like an income statement, not a point-in-time statement (the statement of financial position) or a cash-basis statement (the statement of cash flows), and functional expense detail is reported separately."""),

    mcq("far-nfp-cash-flows-0006", A1, "Statement of cash flows (Not-for-Profit)", RU,
        ["ASC 230-10-10-1 (purpose of the statement of cash flows: information about an entity's ability to generate future net cash inflows and meet its obligations)"],
        """A donor asks Mendip Wildlife Trust's treasurer what the statement of cash flows is meant to tell a reader that the statement of activities does not. Which answer best describes that purpose?""",
        [("It helps users assess the entity's ability to generate future cash flows and meet its obligations", "Correct. The statement of cash flows provides information about cash receipts and payments that helps users evaluate liquidity, the ability to meet obligations, and the need for external financing, which an accrual-basis statement of activities does not show directly."),
         ("It shows which donor restrictions were satisfied during the period and which remain outstanding", "That information comes from the statement of activities and the net asset disclosures, not from the statement of cash flows."),
         ("It measures how efficiently the entity used its resources on its programs compared with fundraising and management", "Program efficiency is conveyed by expenses reported by function, not by the statement of cash flows."),
         ("It reports each fund's beginning and ending cash balance, reconciled to budgeted amounts", "Not-for-profit entities are not required to report by fund, and reconciling to a budget is not a function of the statement of cash flows.")],
        "A",
        """Like the statement of cash flows of a business entity, a not-for-profit entity's statement of cash flows (ASC 958-230) provides information about cash receipts and payments during a period that helps users assess the entity's ability to generate positive future cash flows, meet its obligations and pay for its activities, and judge its need for external financing. It complements, rather than duplicates, the accrual-basis statement of activities."""),

    mcq("far-sec-forms-0003", A1, "Public Company Reporting Topics", RU,
        ["SEC Form 10-Q (quarterly report: condensed, unaudited interim financial statements)",
         "SEC Form 8-K (current report of specified events, not a periodic quarterly filing)"],
        """A newly public company's controller is planning next year's SEC filing calendar. Which statement correctly describes one of Form 10-K, Form 10-Q or Form 8-K?""",
        [("Form 10-Q reports condensed interim statements, which may be unaudited, for the first three fiscal quarters", "Correct. Form 10-Q is filed after each of the first three fiscal quarters and presents condensed interim financial statements that need not be audited."),
         ("Form 10-K's financial statements may be unaudited if the audit committee has reviewed them", "Form 10-K's annual financial statements must be audited by an independent registered public accounting firm; a review by the audit committee is not a substitute."),
         ("Form 8-K is filed on a quarterly schedule to update the registrant's management's discussion and analysis", "Form 8-K is an event-driven current report, filed when specified events occur, not on a quarterly schedule; MD&A updates between periodic reports are not its purpose."),
         ("Form 10-Q must be filed for the registrant's fourth fiscal quarter, covering the full fiscal year's results", "No Form 10-Q is filed for the fourth quarter; the full year's results are reported on the annual Form 10-K instead.")],
        "A",
        """Form 10-Q is the quarterly report, filed after each of a registrant's first three fiscal quarters, and its interim financial statements are condensed and need not be audited. Form 10-K is the annual report, with audited financial statements, and covers the full fiscal year, including what would otherwise be a fourth quarter. Form 8-K is a current report filed when specified events occur between periodic reports, not on a recurring schedule."""),

    mcq("far-sec-forms-0004", A1, "Public Company Reporting Topics", RU,
        ["SEC Form 10-K, Item 1C (cybersecurity risk management, strategy and governance)"],
        """A U.S. registrant's disclosure committee is assigning responsibility for drafting sections of its annual report on Form 10-K. Which Item requires the registrant to describe its processes for assessing, identifying and managing material risks from cybersecurity threats, and the board's oversight of those risks?""",
        [("Item 1C, Cybersecurity", "Correct. Item 1C requires disclosure of the registrant's cybersecurity risk management processes, strategy, and board and management oversight of cybersecurity risks."),
         ("Item 1A, Risk Factors", "Item 1A discloses material risks facing the registrant generally; cybersecurity governance and process disclosures have their own item, 1C."),
         ("Item 7, Management's Discussion and Analysis of Financial Condition and Results of Operations", "Item 7 discusses financial condition and operating results, not cybersecurity risk management and governance."),
         ("Item 9A, Controls and Procedures", "Item 9A addresses disclosure controls and internal control over financial reporting, a narrower topic than the cybersecurity risk management and governance Item 1C covers.")],
        "A",
        """Form 10-K Item 1C requires a registrant to describe its processes, if any, for assessing, identifying and managing material risks from cybersecurity threats, whether any risks from cybersecurity threats have materially affected it, and the board of directors' and management's oversight of cybersecurity risks. Item 1A covers risk factors generally, Item 7 is MD&A, and Item 9A covers disclosure controls and internal control over financial reporting."""),

    mcq("far-special-purpose-frameworks-0007", A1, "Special Purpose Frameworks", RU,
        ["AU-C 800 (financial statements prepared in accordance with special purpose frameworks: titles that avoid implying GAAP presentation)"],
        """A company prepares its financial statements using the same recognition and measurement as its federal income tax return. Which title should it use for the statement reporting its assets, liabilities and equity?""",
        [("Statement of assets, liabilities, and equity—tax basis", "Correct. A title that identifies the income tax basis distinguishes the statement from a GAAP balance sheet."),
         ("Balance sheet", "A GAAP title. Special purpose framework statements use titles that do not suggest GAAP presentation."),
         ("Statement of assets and liabilities arising from cash transactions", "That title identifies cash basis statements, not income tax basis statements; using it here would misdescribe the basis of accounting."),
         ("Statement of financial position", "A GAAP title commonly used by not-for-profit entities; it does not indicate that the statement follows the income tax basis.")],
        "A",
        """Financial statements prepared under a special purpose framework use titles that distinguish them from GAAP statements and identify the basis used. For the income tax basis, "statement of assets, liabilities, and equity—tax basis" and "statement of revenue and expenses—tax basis" are appropriate; "statement of assets and liabilities arising from cash transactions" identifies the cash basis instead, and "balance sheet" and "statement of financial position" are GAAP titles."""),

    mcq("far-ratios-0008", A1, "Financial Statement Ratios and Performance Metrics", RU,
        ["Financial statement analysis: the quick (acid-test) ratio excludes inventory and prepaid items from current assets"],
        """A supplier is deciding whether to extend 30-day trade credit to Bewdley Retail Co. and wants to know whether Bewdley could pay its currently maturing obligations even if it sold no additional inventory before they are due. Which measure best answers that question?""",
        [("The quick (acid-test) ratio", "Correct. The quick ratio excludes inventory (and other current assets not readily convertible to cash) from the numerator, testing whether more liquid assets alone cover current liabilities."),
         ("The current ratio: current assets divided by current liabilities", "The current ratio includes inventory in the numerator, so a company could show adequate current assets while still depending on selling inventory to pay its bills."),
         ("Inventory turnover: cost of goods sold divided by average inventory", "Inventory turnover measures how quickly inventory is sold and replaced; it does not test whether obligations can be paid without selling it."),
         ("Working capital: current assets minus current liabilities", "Working capital is a dollar amount, not scaled to the size of the obligations, and it still includes inventory in current assets.")],
        "A",
        """The quick (acid-test) ratio divides the most liquid current assets, cash, marketable securities and receivables, by current liabilities, testing whether obligations could be met without relying on inventory sales. The current ratio and working capital both include inventory in current assets, and inventory turnover measures sales activity rather than the ability to pay obligations without selling inventory."""),

    mcq("far-investments-fair-value-0006", A2, "Investments (Financial assets at fair value)", RU,
        ["ASC 321-10-35 (equity securities with a readily determinable fair value measured at fair value through net income, after ASU 2016-01, with no available-for-sale category)"],
        """During Year 2, Hask Co. buys several financial assets, in each case giving it less than 20% of the investee's voting shares (except as noted) and no significant influence, and elects the fair value option for none of them. Which should Hask measure at fair value with changes recognized in net income, with no election available to do otherwise?""",
        [("Shares of a publicly traded company that Hask does not intend to sell soon", "Correct. An equity security with a readily determinable fair value is measured at fair value through net income; since ASU 2016-01 eliminated the available-for-sale category for equity securities, there is no election to defer the change in other comprehensive income."),
         ("Shares of a private company with no readily determinable fair value, for which Hask elects the measurement alternative", "An equity security without a readily determinable fair value may be measured under the measurement alternative, cost less impairment, adjusted for observable price changes; that is an election, not a required fair value measurement."),
         ("A bond that Hask classifies as held to maturity", "A debt security classified as held to maturity is measured at amortized cost, not fair value."),
         ("Shares in a company in which Hask also has board representation and significant influence", "An investment over which Hask has significant influence is accounted for by the equity method, not fair value, unless Hask elects the fair value option.")],
        "A",
        """Since ASU 2016-01, an equity security with a readily determinable fair value has no available-for-sale alternative: it is measured at fair value, with changes recognized in net income, as a matter of required measurement rather than election. An equity security without a readily determinable fair value may instead use the measurement alternative, which is elective. Held-to-maturity debt securities use amortized cost, and investments carrying significant influence use the equity method unless the fair value option is elected."""),

    mcq("far-investments-amortized-cost-0002", A2, "Investments (Financial assets at amortized cost)", RU,
        ["ASC 320-10-25-6 (changes in circumstance, such as a sale near maturity, that do not call into question an entity's held-to-maturity classification)"],
        """Teel Co. classifies several debt securities as held-to-maturity. Which of the following sales would NOT call into question Teel's intent and ability to hold its remaining held-to-maturity securities to maturity?""",
        [("Selling a bond after collecting at least 85% of its principal through scheduled payments and prepayments", "Correct. A sale after substantially all of the principal has already been collected is specifically excluded from tainting the held-to-maturity classification, because so little of the original investment or interest rate risk remains."),
         ("Selling a bond because market interest rates rose and Teel wants to reinvest at the higher rate", "Selling to take advantage of interest rate or market price changes is inconsistent with the positive intent and ability to hold required for held-to-maturity classification."),
         ("Selling a bond to raise cash for an unexpected, but foreseeable, operating need", "A need for cash that could have been anticipated when the securities were classified is not one of the specific exceptions, and selling for it taints the held-to-maturity classification."),
         ("Selling a bond after the rating agency placed it on negative watch, though there is no evidence yet of significant deterioration in the issuer's creditworthiness", "The exception requires evidence of significant deterioration in creditworthiness that has already occurred, not merely the possibility signaled by a ratings watch.")],
        "A",
        """A sale of a held-to-maturity debt security generally casts doubt on the investor's intent and ability to hold its remaining such securities to maturity. ASC 320-10-25-6 lists specific exceptions that do not taint the classification, including a sale after the investor has already collected at least 85% of the security's original principal, a sale within three months of maturity, and a sale following significant deterioration in the issuer's creditworthiness that has actually occurred. Selling in response to interest rate changes, a foreseeable liquidity need, or a mere ratings watch is not among the exceptions."""),

    mcq("far-equity-method-0004", A2, "Investments (Equity method investments)", RU,
        ["ASC 323-10-15-13 (the equity method applies to investments in common stock or in-substance common stock)",
         "ASC 323-30-25 (presumption of significant influence over a noncontrolling investment in a partnership or limited liability company)"],
        """Orwell Co. holds investments in four entities, each giving it the ability to exercise significant influence over the investee's operating and financial policies, and it elects the fair value option for none of them. For which investment is the equity method not appropriate?""",
        [("Nonconvertible preferred stock that carries none of the characteristics of common stock", "Correct. The equity method applies to investments in common stock or in-substance common stock. Preferred stock without substantive common stock characteristics is accounted for under the guidance for that instrument, not the equity method, even where the holder has significant influence through other means."),
         ("Common stock representing 25% of the investee's voting shares", "Common stock carrying the ability to exercise significant influence is accounted for by the equity method; this is the ordinary case the method is designed for."),
         ("In-substance common stock of an investee that has not yet issued legal common shares", "In-substance common stock is treated the same as common stock for this purpose and is eligible for the equity method."),
         ("A noncontrolling general partnership interest that lets Orwell participate in managing the partnership's operations", "An investor in a partnership or limited liability company that can participate in management is presumed to have significant influence and applies the equity method, similarly to an investor in common stock.")],
        "A",
        """The equity method is applied to investments in common stock or in-substance common stock of an investee over which the investor can exercise significant influence (ASC 323-10-15-13); investments in unincorporated entities such as partnerships and LLCs are included by analogy when the investor can participate in management (ASC 323-30). Preferred stock without substantive common stock characteristics does not qualify for the equity method, regardless of any influence the holder has through other investments or relationships; it is accounted for under the guidance applicable to that instrument."""),

    mcq("far-debt-modification-0002", A2, "Debt (Notes and bonds payable)", RU,
        ["ASC 470-50-40-17 and 40-18 (fees paid to the lender in a modification deferred and amortized as an adjustment of interest; third-party costs expensed as incurred)"],
        """Garrick Co. and its lender agree to modify the terms of a note; after performing the required cash flow test, the change is accounted for as a modification rather than an extinguishment. Garrick pays the lender $15,000 as a fee for agreeing to the new terms and separately pays its own outside legal counsel $6,000 for advice on negotiating the modification. How should Garrick account for these two payments?""",
        [("The $15,000 fee is deferred and amortized over the remaining term; the $6,000 fee is expensed", "Correct. A fee paid to the lender in a modification is capitalized and amortized over the remaining term as an adjustment of the effective interest rate; costs paid to third parties, such as Garrick's own counsel, are expensed when incurred."),
         ("Both fees are deferred and amortized over the note's remaining term as debt issuance costs", "Only the fee paid to the lender is deferred. A fee paid to an outside party, such as Garrick's own legal counsel, is expensed as incurred."),
         ("Both fees are expensed immediately, since the change is only a modification and not an extinguishment", "A modification does not mean every related cost is expensed; the fee paid to the lender is still deferred and amortized over the remaining term."),
         ("The $15,000 lender fee is expensed immediately, and the $6,000 legal fee is deferred and amortized", "Reverses the correct treatment: the lender fee is the one that is deferred, and the third-party legal fee is the one that is expensed.")],
        "A",
        """In a modification (as opposed to an extinguishment), a fee paid to the lender is deferred and amortized as an adjustment of interest expense over the remaining term of the modified debt (ASC 470-50-40-17). Costs paid to third parties, such as Garrick's own legal counsel, are expensed as incurred (ASC 470-50-40-18) and are not part of the cash flow test used to decide whether the change is a modification or an extinguishment."""),
]


def blind_files(items, scratch):
    """Stems and lettered choices only, for the blind verifier, plus a separate key file."""
    lines, keys = ["# FAR batch 14: blind verification input", "",
                   "Each block is one version of a question. Solve each independently; choose one letter.", ""], {}
    for it in items:
        for k, v in enumerate([it] + list(it.get("variants") or [])):
            label = f"{it['id']} v{k}"
            lines += [f"## {label}", "", v["stem"], ""]
            lines += [f"{c['id']}. {c['text']}" for c in v["choices"]] + [""]
            keys[label] = v["answer"]
    with open(os.path.join(scratch, "b14-blind.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(scratch, "b14-keys.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys, f, indent=1)
    print(f"blind file: {len(keys)} versions")


def main():
    items = [family(*f) for f in FAMILIES] + WORD_ITEMS
    finalize(items)
    failed = False
    for it in items:
        vs = it.pop("_variants", None)
        if vs:
            attach_variants(it, vs)
            letters = [it["answer"]] + [v["answer"] for v in it["variants"]]
            print(f"{it['id']}: key letters {' '.join(letters)}")
            if len(set(letters)) < 2:
                print(f"FAIL {it['id']}: the key has the same letter in every version", file=sys.stderr)
                failed = True
        else:
            print(f"{it['id']}: key letter {it['answer']} (word item)")
    if failed:
        sys.exit(1)
    assert len(items) == 18 and len({it["id"] for it in items}) == 18
    warnings = audit(items)
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    tally, v0 = {}, {}
    for it in items:
        v0[it["answer"]] = v0.get(it["answer"], 0) + 1
        for v in [it] + list(it.get("variants") or []):
            tally[v["answer"]] = tally.get(v["answer"], 0) + 1
    print("version-0 keys", dict(sorted(v0.items())), "all versions", dict(sorted(tally.items())),
          "variants", sum(len(it.get("variants") or []) for it in items))
    if "--dry-run" in sys.argv:
        print("dry run: nothing written")
        return
    write_items(items, CONTENT)
    if SCRATCH:
        blind_files(items, SCRATCH)


if __name__ == "__main__":
    main()
