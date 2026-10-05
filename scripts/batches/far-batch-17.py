"""FAR batch 17 -- 16 items, Area III -- Select Transactions only (a slice run in parallel with batch 16, which
covers III.C-III.F; no shared tasks or ids): three Application items calculating adjustments for accounting
changes and error corrections (III.A.a), three Analysis items deriving the impact of error corrections from a
draft and its supporting records (III.A.b), three Application items on contingency amounts (III.B.b), two
Analysis items reviewing documentation for recognition versus disclosure (III.B.c), two Application items
calculating adjustments for identified subsequent events (III.G.b) and three Analysis items deriving the impact
of subsequent events (III.G.c). Skill mix 0 / 8 / 8; area mix 0 / 0 / 16. Scope and skill tags follow the
AICPA CPA Exam Blueprints effective January 2026.

Rewritten after the first review gate (62.0%, five major items, three wrong keys; see
docs/reviews/far-batch-17.md). This script is the source of truth for the 16 items: parameter set 0 is the
item, sets 1-3 are its variants (attach_variants), every family moves the key's letter, and parameter set 0
shows the distractor for the item's central twist. Every amount, including each distractor, is computed here
in Decimal and rounded half up; every amount that depends on a date (months of interest or depreciation) is
computed from the dates the stem states, and no derived amount is stated in a stem. Items are written with
review.status "draft" so they stay unserved until the gate re-passes.

Run: python3 scripts/batches/far-batch-17.py [--dry-run]
Blind file (set B17_SCRATCH to a directory): stems/choices and keys written there, never in the repo.
"""
import json
import os
import re
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AN, AP, attach_variants, audit, finalize, fix_articles, variant, write_items  # noqa: E402
from variants import article, m, pick, rd  # noqa: E402

A3 = "Area III — Select Transactions"
T_CHG = "Accounting changes and error corrections"
T_CON = "Contingencies and commitments"
T_SUB = "Subsequent events"
NOTE = "Batch 17. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
SCRATCH = os.environ.get("B17_SCRATCH")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def family(id, area, topic, skill, refs, build, params, twist):
    assert twist in params[0]["use"], f"{id}: version 0 doesn't show the central-twist distractor {twist}"
    base = build(params[0])
    review = dict(status="draft", references=refs, notes=NOTE)
    it = dict(id=id, type="mcq", blueprint=dict(section="FAR", area=area, topic=topic, skill=skill),
              review=review, **base)
    it["stem"], it["explanation"] = fix_articles(it["stem"]), fix_articles(it["explanation"])
    for c in it["choices"]:
        c["text"], c["rationale"] = fix_articles(c["text"]), fix_articles(c["rationale"])
    it["_variants"] = [build(p) for p in params[1:]]
    for k, v in enumerate([it] + it["_variants"]):
        repeats(f"{id} v{k}", v)
        spacing(f"{id} v{k}", v)
        rendering(f"{id} v{k}", v)
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
    vals = sorted(float(re.match(r"^\$?([\d,]+(?:\.\d+)?)", c["text"]).group(1).replace(",", ""))
                  for c in v["choices"])
    for a, b in zip(vals, vals[1:]):
        if b - a < 0.004 * b:
            print(f"CLOSE {label}: {a:,.2f} and {b:,.2f}", file=sys.stderr)


BAD_RENDER = [
    re.compile(r"\b(?:" + "|".join(MONTHS) + r")(?: \d{1,2})?, \d\b"),   # "December 31, 1" (Year dropped)
    re.compile(r"\b(?:a|an|in|of|the) \d (?:incident|delivery|deadline|year)\b"),  # "a 1 incident"
    re.compile(r"\$-|\.\.(?!\.)"),                                         # "$-50,000", "Ltd.."
    re.compile(r"\b(?:only|for) 1 years\b|\b[2-9] year\b(?!-)"),           # "2 year" / "1 years"
]


def rendering(label, v):
    """Fail on template-render defects the first gate found (missing 'Year', '$-', doubled periods)."""
    texts = [v["stem"], v["explanation"]] + [c["text"] for c in v["choices"]] + [c["rationale"] for c in v["choices"]]
    for t in texts:
        for rx in BAD_RENDER:
            hit = rx.search(t)
            assert not hit, f"{label}: render defect {hit.group(0)!r} in: {t[:120]}"


def short(name):
    return name.split()[0]


def distinct(pool, key):
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"
    nums = [float(re.match(r"^\$?([\d,]+(?:\.\d+)?)", v).group(1).replace(",", "")) for v in vals]
    signs = [-1 if "decrease" in v else 1 for v in vals]
    signed = [a * s for a, s in zip(nums, signs)]
    assert len(set(signed)) == len(signed), f"two choices share a leading amount: {vals}"


def build(pool, key, use):
    distinct({k: pool[k] for k in use}, key)
    return pick(pool, key, use)


def chg(x):
    """A signed amount as '$12,000 increase' or '$12,000 decrease'."""
    x = D(x)
    assert x != 0
    return f"{m(x)} increase" if x > 0 else f"{m(-x)} decrease"


def months_from(month):
    """Months from the first day of `month` through December 31, inclusive (September 1 -> 4)."""
    return 13 - (MONTHS.index(month) + 1)


def months_to(month):
    """Months from January 1 to the first day of `month` (May 1 -> 4)."""
    return MONTHS.index(month)


def poss(name):
    return name + ("'" if name.endswith("s") else "'s")


def pct(x):
    return f"{D(x).normalize():f}%"


# ── III.A.a Application: calculate adjustments for accounting changes and error corrections ──────────────


def change_in_estimate(p):
    co, s = p["co"], short(p["co"])
    cost, L0, S0, n, L1, S1 = D(p["cost"]), p["L0"], D(p["S0"]), p["n"], p["L1"], D(p["S1"])
    dep0 = rd((cost - S0) / L0)
    cv = cost - n * dep0
    rem, rem_old = L1 - n, L0 - n
    dep1 = rd((cv - S1) / rem)
    key_v = cv - dep1
    yr = n + 1
    pool = {
        "salv_old": (m(cv - rd((cv - S0) / rem)), f"Keeps the original {m(S0)} salvage value when computing the new depreciation. {s} revised the salvage estimate to {m(S1)} along with the useful life, and both revised estimates apply."),
        "old_life": (m(cv - rd((cv - S1) / rem_old)), f"Spreads the remaining depreciable base over the original remaining life of {rem_old} years. {s} now expects only {rem} more years of use."),
        "retro": (m(cost - (n + 1) * rd((cost - S1) / L1)), f"Restates depreciation for the {n} years already recorded using the revised {L1}-year total useful life and {m(S1)} salvage value, as if the revision applied retroactively. A change in estimate is applied prospectively."),
        "no_salv": (m(cv - rd(cv / rem)), f"Ignores the revised {m(S1)} salvage value, depreciating the whole {m(cv)} carrying amount over the {rem} remaining years. Only the carrying amount in excess of salvage value is depreciated."),
        "total_life": (m(cv - rd((cv - S1) / L1)), f"Spreads the remaining depreciable base over the revised {L1}-year total life instead of the {rem} years that remain at the date of the change."),
    }
    key = (m(key_v), f"Correct. Carrying amount {m(cv)} ({m(cost)} − {n} × {m(dep0)}) less Year {yr} depreciation of {m(dep1)} (({m(cv)} − {m(S1)}) ÷ {rem}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} bought equipment for {m(cost)}, estimated a {L0}-year useful life and a {m(S0)} salvage value, and has depreciated it straight-line. On January 1, Year {yr}, after {n} years of use, {s} determines, based on new information about the equipment's condition, that its total useful life will be {L1} years rather than {L0}, and revises the salvage value to {m(S1)}; the depreciation method is unchanged. What carrying amount should {s} report for the equipment at the end of Year {yr}, after that year's depreciation?""",
        choices, ans,
        f"""A change in the estimated useful life or salvage value of a depreciable asset is a change in accounting estimate, applied prospectively from the date of the change (ASC 250-10-45-17). Annual depreciation before the change = ({m(cost)} − {m(S0)}) ÷ {L0} = {m(dep0)}. Carrying amount at the date of change = {m(cost)} − {n} × {m(dep0)} = {m(cv)}. The remaining depreciable base is spread over the revised remaining life of {L1} − {n} = {rem} years: ({m(cv)} − {m(S1)}) ÷ {rem} = {m(dep1)} for Year {yr}. Carrying amount at the end of Year {yr} = {m(cv)} − {m(dep1)} = {m(key_v)}. Years already reported are not restated.""",
    )


def change_in_principle(p):
    co, s = p["co"], short(p["co"])
    old, new, Y = p["old"], p["new"], p["Y"]
    t, b = D(p["t"]) / 100, D(p["b"]) / 100
    o, nw = [D(x) for x in p["old_inv"]], [D(x) for x in p["new_inv"]]
    y1, y2, y3 = Y - 3, Y - 2, Y - 1          # year-ends in the table; the asked year is y3
    diff = [nw[i] - o[i] for i in range(3)]
    delta = diff[2] - diff[1]
    NI = D(p["NI"])
    eff = rd(delta * (1 - t))
    key_v = NI + eff
    assert all(d > 0 for d in diff) or all(d < 0 for d in diff), "the key rationale assumes one direction"
    rel = lambda d: f"{m(abs(d))} {'above' if d > 0 else 'below'} {old}"
    moved = f"from {rel(diff[1])} at the start of Year {y3} to {rel(diff[2])} at its end"
    up = delta > 0
    pool = {
        "cum": (m(NI + rd(diff[2] * (1 - t))), f"Applies the whole {m(abs(diff[2]))} cumulative difference between the methods at December 31, Year {y3}, net of tax, to Year {y3} income. Year {y3} income changes only by the change in that difference during Year {y3}; the effect of earlier years goes to opening retained earnings."),
        "pretax": (m(NI + delta), f"Applies the {m(abs(delta))} pretax effect on Year {y3} income without its {p['t']}% tax effect."),
        "bonus": (m(NI + rd(delta * (1 - b) * (1 - t))), f"Also recomputes the {p['b']}% profit-sharing bonus on the restated income. A change in the bonus is an indirect effect of the change in principle, and indirect effects aren't recognized in the restated prior periods (ASC 250-10-45-8)."),
        "prior": (m(NI + rd((diff[1] - diff[0]) * (1 - t))), f"Uses the change in the difference between the methods during Year {y2} (from December 31, Year {y1}, to December 31, Year {y2}) instead of during Year {y3}."),
        "sign": (m(NI - eff), f"Applies the Year {y3} effect in the wrong direction. {new[0].upper() + new[1:]} inventory moved {moved}, so restated Year {y3} cost of goods sold is {'lower' if up else 'higher'} and income {'higher' if up else 'lower'}."),
    }
    key = (m(key_v), f"Correct. {m(NI)} {'+' if eff > 0 else '−'} ({m(abs(diff[2]))} {'−' if (diff[1] > 0) == (diff[2] > 0) else '+'} {m(abs(diff[1]))}) × {100 - int(p['t'])}% = {m(key_v)}; the bonus isn't recomputed.")
    choices, ans = build(pool, key, p["use"])
    tbl = "; ".join(f"December 31, Year {yr}, {old} {m(o[i])} and {new} {m(nw[i])}" for i, yr in enumerate((y1, y2, y3)))
    return variant(
        f"""At the start of Year {Y}, {co} changes its inventory cost-flow method from {old} to {new} because {p['why']}, and it can determine the effect on every prior period. Its year-end inventories under the two methods were: {tbl}. {s} pays employees a profit-sharing bonus equal to {p['b']}% of income before the bonus and income taxes; bonuses for prior years were based on income as originally reported and will not be recalculated. {s}'s Year {y3} net income as originally reported was {m(NI)}, and its tax rate is {p['t']}% for all years and all effects. In its comparative statements for Years {y2}, {y3} and {Y}, what net income should {s} report for Year {y3}?""",
        choices, ans,
        f"""A change in inventory cost-flow method is a change in accounting principle, applied retrospectively when its effect on every prior period can be determined (ASC 250-10-45-5). Each prior year presented is restated as if {new} had always been used. Year {y3} income changes by the change during Year {y3} in the difference between the methods' inventories: {new} inventory moved {moved}, so restated Year {y3} cost of goods sold is {m(abs(delta))} {'lower' if up else 'higher'} and pretax income {m(abs(delta))} {'higher' if up else 'lower'}, or {m(abs(eff))} after the {p['t']}% tax. The profit-sharing bonus would have differed under {new}, but that is an indirect effect, which is not recognized in the restated periods (ASC 250-10-45-8); prior bonuses won't be recalculated, so nothing changes in any period. Restated Year {y3} net income = {m(NI)} {'+' if eff > 0 else '−'} {m(abs(eff))} = {m(key_v)}.""",
    )


def error_correction(p):
    co, s = p["co"], short(p["co"])
    P, r, t = D(p["P"]), D(p["r"]) / 100, D(p["t"]) / 100
    m1 = months_from(p["start"])
    md = months_to(p["found"])
    i1 = rd(P * r * m1 / 12)
    i2 = rd(P * r)
    cum = i1 + i2
    key_v = -rd(cum * (1 - t))
    keep = 100 - int(p["t"])
    pool = {
        "pretax": (chg(-cum), f"Decreases retained earnings by the full pretax {m(cum)} of unrecorded interest. The prior-period adjustment is made net of the {p['t']}% tax effect."),
        "full_y1": (chg(-rd(P * r * 2 * (1 - t))), f"Charges a full year of interest for Year 1. The note was signed on {p['start']} 1, Year 1, so Year 1 bore only {m1} months of interest ({m(i1)})."),
        "only_y1": (chg(-rd(i1 * (1 - t))), f"Adjusts only for the Year 1 interest, as if Year 2 were still open. The Year 2 statements have been issued, so the Year 2 interest is also part of the adjustment to January 1, Year 3, retained earnings."),
        "thru_found": (chg(-rd((cum + rd(P * r * md / 12)) * (1 - t))), f"Also includes the {md} months of Year 3 interest through {p['found']} 1, Year 3. That interest is a Year 3 expense, recorded in Year 3 income, not part of the adjustment to opening retained earnings."),
    }
    key = (chg(key_v), f"Correct. ({m(i1)} for Year 1 + {m(i2)} for Year 2) × {keep}% after tax.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On {p['start']} 1, Year 1, {co} borrowed {m(P)} on a {p['term']}-year note bearing simple interest at {pct(p['r'])} a year, with all interest and principal due at maturity. On {p['found']} 1, Year 3, after its Year 2 financial statements had been issued, {s}'s controller found that no interest on the note had ever been recorded; none has been paid. {s} has found no other errors, its tax rate is {p['t']}% for all effects, and it presents single-year financial statements. What adjustment should {s} make to its January 1, Year 3, balance of retained earnings?""",
        choices, ans,
        f"""Interest accrues from the day the note is signed. Unrecorded interest expense in the issued Year 1 and Year 2 statements overstated those years' income, and the correction of a prior-period error adjusts the opening balance of retained earnings of the current year, net of tax (ASC 250-10-45-23). Year 1 interest = {m(P)} × {pct(p['r'])} × {m1}/12 = {m(i1)}; Year 2 interest = {m(P)} × {pct(p['r'])} = {m(i2)}; total {m(cum)}, or {m(-key_v)} after the {p['t']}% tax effect ({m(cum)} × {keep}%). The {md} months of Year 3 interest through {p['found']} 1 belong in Year 3 income. Adjustment = {chg(key_v)}.""",
    )


# ── III.A.b Analysis: derive the impact of an error correction from a draft and its supporting records ───


def ae_returns_install(p):
    co, s, Y = p["co"], short(p["co"]), p["Y"]
    NI, S, rp, cp = D(p["NI"]), D(p["S"]), D(p["rp"]) / 100, D(p["cp"]) / 100
    f, i, L, Dp = D(p["f"]), D(p["i"]), p["L"], D(p["Dp"])
    mo = months_from(p["month"])
    ret = rd(S * rp)
    ret_cost = rd(ret * cp)
    ret_net = ret - ret_cost
    capz = f + i
    dep = rd(capz / L * mo / 12)
    key_v = NI - ret_net + capz - dep
    pool = {
        "gross_ret": (m(NI - ret + capz - dep), f"Reverses the {m(ret)} of revenue on goods expected to be returned but not the {m(ret_cost)} cost of those goods. The goods come back to inventory, so a return asset reduces cost of goods sold, and income falls only by the {m(ret_net)} margin."),
        "full_year": (m(NI - ret_net + capz - rd(capz / L)), f"Depreciates the {m(capz)} of freight and installation for a full year. The machine was placed in service on {p['month']} 1, so Year {Y} bears {mo} months of depreciation ({m(dep)})."),
        "no_dep": (m(NI - ret_net + capz), f"Capitalizes the {m(capz)} of freight and installation but records no depreciation on it, though the machine has been in service since {p['month']} 1."),
        "deposit": (m(key_v + Dp), f"Also moves the {m(Dp)} December deposit into revenue. The goods won't be delivered until January, Year {Y + 1}, so the deposit is correctly a liability."),
        "no_returns": (m(NI + capz - dep), f"Leaves the December sales as recorded. Because customers are expected to return {pct(p['rp'])} of those goods, revenue is recognized only for the goods not expected to be returned."),
    }
    key = (m(key_v), f"Correct. {m(NI)} − {m(ret_net)} return margin + {m(capz)} capitalized − {m(dep)} depreciation.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year {Y} income statement reports net income of {m(NI)}. Before the statements are issued, the controller reviews three entries in the supporting records. In December, {s} sold goods for {m(S)} under a policy that lets customers return them within 60 days for a full refund; from experience, {s} expects {pct(p['rp'])} of those goods to come back in resalable condition, and the goods cost {pct(p['cp'])} of their selling price. The entry recorded the full {m(S)} as revenue and the cost of all of the goods as cost of goods sold. On {p['month']} 1, Year {Y}, {s} placed in service a {p['asset']} recorded at its {m(p['P'])} purchase price; the {m(f)} paid to ship it and the {m(i)} paid to install it were charged to repairs and maintenance expense. {s} depreciates equipment straight-line over {L} years with no salvage value, starting in the month an asset is placed in service, and the draft includes that depreciation on the {m(p['P'])}. On December {p['dday']}, a customer paid a {m(Dp)} deposit on goods to be delivered in January, Year {Y + 1}, and {s} recorded it as a liability. Ignore income taxes. What net income should {s} report for Year {Y}?""",
        choices, ans,
        f"""Sales with a right of return are recognized only for the goods not expected to be returned, with a refund liability for the rest and an asset for the right to recover the returned goods, which reduces cost of goods sold (ASC 606-10-55-22 to 55-29): revenue falls by {pct(p['rp'])} × {m(S)} = {m(ret)}, cost of goods sold by {pct(p['cp'])} × {m(ret)} = {m(ret_cost)}, and income by {m(ret_net)}. Freight and installation are costs of bringing the machine to its working condition and location and are capitalized (ASC 360-10-30-1): {m(f)} + {m(i)} = {m(capz)} comes out of expense, and depreciation from {p['month']} 1 adds {m(capz)} ÷ {L} × {mo}/12 = {m(dep)}. The deposit on goods not yet delivered is a contract liability, as recorded (ASC 606-10-45-2). Corrected net income = {m(NI)} − {m(ret_net)} + {m(capz)} − {m(dep)} = {m(key_v)}.""",
    )


def ae_liabilities(p):
    co, s, Y = p["co"], short(p["co"]), p["Y"]
    TL, PO, INV = D(p["TL"]), D(p["PO"]), D(p["INV"])
    out = p["sh"] - p["tr"]
    div = rd(D(p["dps"]) * out)
    key_v = TL - PO + div
    pool = {
        "draft": (m(TL), f"Accepts the draft total. The purchase order isn't a liability, and the declared dividend is one."),
        "keep_po": (m(TL + div), f"Leaves the {m(PO)} purchase order in accounts payable. {s} owes nothing until the supplier ships the {p['po_item']} in January; an unperformed order is a commitment, not a liability."),
        "no_div": (m(TL - PO), f"Leaves out the dividend. A cash dividend becomes a liability when the board declares it, so the {m(div)} ({m(p['dps'])} × {out:,} outstanding shares) is owed at December 31 even though it is paid in January."),
        "drop_inv": (m(key_v - INV), f"Also removes the {m(INV)} invoice for the {p['inv_item']}. The {p['inv_item']} were shipped FOB destination and delivered on December 30, so {s} owned them, and owed for them, at year-end."),
        "issued": (m(TL - PO + rd(D(p["dps"]) * p["sh"])), f"Computes the dividend on all {p['sh']:,} issued shares. Treasury shares receive no dividends, so the dividend is {m(p['dps'])} × {out:,} outstanding shares = {m(div)}."),
    }
    key = (m(key_v), f"Correct. {m(TL)} − {m(PO)} purchase order + {m(div)} dividend payable.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year {Y}, balance sheet reports total liabilities of {m(TL)}. Before the statements are issued, the controller questions three items. Accounts payable includes {m(PO)} for a purchase order {s} issued on December 29 for {p['po_item']} that the supplier will ship, FOB shipping point, in mid-January. On December {p['dday']}, {s}'s board declared a cash dividend of {m(p['dps'])} a share on its common stock, payable January {p['pday']}, Year {Y + 1}; {s} has {p['sh']:,} common shares issued, {p['tr']:,} of them held in treasury, and records dividends when it pays them. Accounts payable also includes a {m(INV)} supplier invoice for {p['inv_item']} that were shipped FOB destination and delivered to {s}'s store on December 30. What total liabilities should the corrected balance sheet report?""",
        choices, ans,
        f"""A purchase order is an executory contract: until the supplier performs by shipping the goods, {s} has no present obligation, so the {m(PO)} comes out of accounts payable (ASC 440-10). A declared cash dividend is a present obligation from the declaration date (FASB Concepts Statement No. 8, chapter 4), so {m(p['dps'])} × {out:,} outstanding shares (treasury shares receive no dividend) = {m(div)} is added as a dividend payable. Goods shipped FOB destination transfer to the buyer on delivery; the {p['inv_item']} arrived on December 30, so that invoice is correctly in accounts payable. Corrected total liabilities = {m(TL)} − {m(PO)} + {m(div)} = {m(key_v)}.""",
    )


def ae_assets(p):
    co, s, Y = p["co"], short(p["co"]), p["Y"]
    TA, N, r, term = D(p["TA"]), D(p["N"]), D(p["r"]) / 100, p["term"]
    C, FV, G = D(p["C"]), D(p["FV"]), D(p["G"])
    mo = months_from(p["month"])
    acc = rd(N * r * mo / 12)
    fv_adj = FV - C
    key_v = TA + acc + fv_adj
    word = "gain" if fv_adj > 0 else "loss"
    pool = {
        "draft": (m(TA), f"Accepts the draft total, with no interest receivable and the shares at cost."),
        "full_year": (m(TA + rd(N * r) + fv_adj), f"Accrues a full year of interest on the note. It was accepted on {p['month']} 1, so only {mo} months of interest ({m(acc)}) had accrued by December 31."),
        "term": (m(TA + rd(N * r * term / 12) + fv_adj), f"Accrues the interest for the note's whole {term}-month term. Only the {mo} months through December 31 have been earned."),
        "at_cost": (m(TA + acc), f"Leaves the shares at their {m(C)} cost. Equity securities with a readily determinable fair value are measured at fair value, here {m(FV)}, with the change in net income."),
        "consigned": (m(key_v - G), f"Also removes the {m(G)} of goods held by the consignee. Goods out on consignment remain the consignor's inventory until the consignee sells them, so they are correctly included."),
    }
    key = (m(key_v), f"Correct. {m(TA)} + {m(acc)} interest receivable {'+' if fv_adj > 0 else '−'} {m(abs(fv_adj))} fair value {'increase' if fv_adj > 0 else 'decrease'}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year {Y}, balance sheet reports total assets of {m(TA)}. Before the statements are issued, its controller traces three balances to their support. On {p['month']} 1, Year {Y}, {s} accepted from a customer a {m(N)}, {term}-month note bearing simple interest at {pct(p['r'])} a year, with principal and interest due at maturity; the draft reports the note at {m(N)} and no interest receivable. The draft carries {s}'s holding of a listed company's common shares, a small stake that gives {s} no influence over the company, at their {m(C)} cost; the shares' quoted price at December 31 puts the holding at {m(FV)}. And inventory includes, at their {m(G)} cost, goods {s} shipped in December to a retailer that sells them for {s} on consignment; the retailer had sold none of them by year-end. Ignore income taxes. What total assets should the corrected balance sheet report?""",
        choices, ans,
        f"""Interest on the note accrues from {p['month']} 1: {m(N)} × {pct(p['r'])} × {mo}/12 = {m(acc)} of interest receivable, which the draft omits. Equity securities with a readily determinable fair value are measured at fair value, with changes in net income (ASC 321-10-35-1), so the shares are remeasured from {m(C)} to {m(FV)}, a {m(abs(fv_adj))} {word}. Goods on consignment remain the consignor's inventory until the consignee sells them (ASC 606-10-55-79 to 55-80), so the {m(G)} is correctly included. Corrected total assets = {m(TA)} + {m(acc)} {'+' if fv_adj > 0 else '−'} {m(abs(fv_adj))} = {m(key_v)}.""",
    )


# ── III.B.b Application: calculate amounts of contingencies ────────────────────────────────────────────────


def litigation_and_recall(p):
    co, s = p["co"], short(p["co"])
    A, Pd, Inc, L, H = D(p["A"]), D(p["Pd"]), D(p["Inc"]), D(p["L"]), D(p["H"])
    lit = A - Pd + Inc
    key_v = lit + L
    pool = {
        "unasserted": (m(lit), f"Accrues nothing for the recall claims because no customer has filed one yet. An unasserted claim is accrued when its assertion and an unfavorable outcome are both probable and the loss can be estimated, as counsel's letter indicates here."),
        "mid": (m(lit + (L + H) / 2), f"Accrues the {m((L + H) / 2)} midpoint of the range for the recall claims. When no amount in a range is a better estimate than another, the minimum, {m(L)}, is accrued (ASC 450-20-30-1)."),
        "high": (m(lit + H), f"Accrues the {m(H)} top of the range for the recall claims. With no best estimate in the range, the minimum is accrued and the rest is disclosed."),
        "no_inc": (m(A - Pd + L), f"Leaves out the {m(Inc)} upward revision of the lawsuit's total cost, as if the original {m(A)} estimate still held."),
        "no_paid": (m(A + Inc + L), f"Doesn't reduce the lawsuit accrual for the {m(Pd)} already paid; those payments settle part of the liability."),
    }
    key = (m(key_v), f"Correct. Lawsuit {m(lit)} ({m(A)} − {m(Pd)} + {m(Inc)}) + recall claims at the {m(L)} minimum.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At the start of the year, {co} had a {m(A)} liability for a customer's lawsuit over a defect in a product it sold two years ago. During the year, {s} paid {m(Pd)} toward the case under an interim agreement and, based on new evidence, revised its estimate of the suit's total cost upward by {m(Inc)}. In November, {s} recalled a {p['product']} model after reports that a faulty {p['part']} had damaged customers' property. No customer has filed a claim yet, but counsel's letter says customers are expected to file claims that {s} will have to pay, and puts the total at between {m(L)} and {m(H)}, with no amount in that range a better estimate than any other. What total liability for the lawsuit and the recall claims should {s} report at year-end?""",
        choices, ans,
        f"""Lawsuit: the liability rolls forward from the opening {m(A)}, less the {m(Pd)} paid, plus the {m(Inc)} increase in the estimated total cost, a change in estimate recognized in the current year: {m(lit)}. Recall claims: an unasserted claim is accrued when it is probable that the claim will be asserted and that the outcome will be unfavorable, and the loss can be reasonably estimated (ASC 450-20-25-2, 450-20-50-6); counsel expects both, and the range estimates the loss. With no best estimate in the range, the minimum, {m(L)}, is accrued and the possible additional loss is disclosed (ASC 450-20-30-1). Total liability = {m(lit)} + {m(L)} = {m(key_v)}.""",
    )


def commitment_and_rebate(p):
    co, s = p["co"], short(p["co"])
    Q, Pc, Pm = D(p["Q"]), D(p["Pc"]), D(p["Pm"])
    N, r, rp, paid = D(p["N"]), D(p["r"]), D(p["rp"]) / 100, D(p["paid"])
    loss = rd(Q * (Pc - Pm))
    expected = rd(N * rp * r)
    reb = expected - paid
    key_v = loss + reb
    pool = {
        "no_commit": (m(reb), f"Leaves out the {m(loss)} loss on the purchase commitment. A noncancelable commitment to buy at a price above the current market price is a loss to recognize now, with a liability."),
        "no_rebate": (m(loss), f"Accrues nothing for rebates not yet claimed. Rebates expected on sales already made are consideration payable to customers and reduce revenue, with a refund liability for the amount still to be paid."),
        "all_claim": (m(loss + rd(N * r) - paid), f"Assumes every buyer will claim the rebate. The refund liability is based on the {pct(p['rp'])} of buyers {s} expects to claim it."),
        "no_paid": (m(loss + expected), f"Doesn't reduce the expected rebates for the {m(paid)} already paid; those claims are settled."),
        "full_contract": (m(rd(Q * Pc) + reb), f"Treats the whole {m(rd(Q * Pc))} contract price as the liability, rather than only the {m(loss)} by which the contract price exceeds the market price."),
    }
    key = (m(key_v), f"Correct. Commitment loss {m(loss)} + rebate refund liability {m(reb)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} has a noncancelable, unhedged commitment to buy {int(Q):,} {p['unit']}s of {p['mat']} next year at a fixed {m(Pc)} a {p['unit']}; at year-end, the market price for the same delivery is {m(Pm)} a {p['unit']}. {s} also sold {int(N):,} {p['goods']} during the year with a {m(r)} mail-in cash rebate, claimable through {p['through']} of next year; from experience with similar offers, {s} expects {pct(p['rp'])} of buyers to claim it, and it has paid {m(paid)} of claims so far. What total liability should {s} report at year-end for the purchase commitment and the rebate offer?""",
        choices, ans,
        f"""A loss on a noncancelable, unhedged purchase commitment is recognized when the market price falls below the contract price (ASC 330-10-35-17 to 35-18): {int(Q):,} × ({m(Pc)} − {m(Pm)}) = {m(loss)}. Cash rebates are consideration payable to a customer, which reduces revenue (ASC 606-10-32-25); the rebates {s} expects to pay on sales already made are a refund liability (ASC 606-10-32-10): {int(N):,} × {pct(p['rp'])} × {m(r)} = {m(expected)} expected, less {m(paid)} paid = {m(reb)}. Total liability = {m(loss)} + {m(reb)} = {m(key_v)}.""",
    )


def settlement_and_selfinsurance(p):
    co, s = p["co"], short(p["co"])
    now, later, i = D(p["now"]), D(p["later"]), D(p["i"]) / 100
    Ar, Ai, B = D(p["Ar"]), D(p["Ai"]), D(p["B"])
    pv = rd(later / (1 + i))
    key_v = now + pv + Ar + Ai
    pool = {
        "undiscounted": (m(now + later + Ar + Ai), f"Adds the {m(later)} due in a year at its face amount. {s}'s policy is to discount fixed, scheduled settlement payments, so it is carried at present value, {m(pv)}."),
        "compounded": (m(now + rd(later * (1 + i)) + Ar + Ai), f"Compounds the deferred payment forward at {pct(p['i'])} instead of discounting it back to present value."),
        "omit_now": (m(pv + Ar + Ai), f"Leaves out the {m(now)} due within 30 days; it is unpaid at year-end and part of the settlement liability."),
        "reported": (m(now + pv + Ar), f"Accrues only the {m(Ar)} for injuries already reported. The {m(Ai)} for injuries that occurred during the year but haven't been reported is also a loss incurred by year-end and is accrued."),
        "future": (m(key_v + B), f"Also accrues the {m(B)} the actuary expects next year's injuries to cost. No liability exists for injuries that haven't occurred, whatever the self-insurance arrangement."),
    }
    key = (m(key_v), f"Correct. Settlement {m(now)} + {m(pv)} present value + injuries {m(Ar)} reported and {m(Ai)} not yet reported.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} settled a product-liability suit at year-end, agreeing to pay {m(now)} within 30 days and {m(later)} one year later; because the amounts and dates are fixed, {s}'s policy is to discount such payments, and it uses {pct(p['i'])}. {s} is also self-insured for injuries to its {p['workers']}. Its actuary estimates that settling injuries that occurred during the year will cost {m(Ar)} for claims already filed and unpaid and {m(Ai)} for injuries that have occurred but haven't been reported yet, and expects injuries next year to cost {m(B)}. What total liability should {s} report at year-end for the settlement and the injuries?""",
        choices, ans,
        f"""The settlement is a fixed obligation; under {s}'s discounting policy, which GAAP permits when the amount and timing of payments are fixed or reliably determinable (SEC SAB Topic 5Y; ASC 835-30), it is measured at {m(now)} + {m(later)} ÷ {1 + i:.2f} = {m(now)} + {m(pv)} = {m(now + pv)}. For self-insured risks, losses from injuries that occurred by year-end, both reported and incurred but not reported, are accrued when probable and estimable (ASC 450-20-25-2): {m(Ar)} + {m(Ai)} = {m(Ar + Ai)}. Injuries that haven't happened create no liability, so next year's {m(B)} is not accrued. Total liability = {m(now + pv)} + {m(Ar + Ai)} = {m(key_v)}.""",
    )


# ── III.B.c Analysis: review documentation for recognition versus disclosure ──────────────────────────────


def draft_note_penalty(p):
    co, s = p["co"], short(p["co"])
    days, P, Pmax, Dm = p["days"], D(p["P"]), D(p["Pmax"]), D(p["Dm"])
    key_v = days * P
    pool = {
        "zero": (m(0), f"Accrues nothing because the agency hasn't issued a penalty notice. An unasserted claim is accrued when assertion and an unfavorable outcome are both probable and the loss can be estimated: the agency has assessed scheduled penalties after every inspection with findings, and its schedule fixes the amount."),
        "max": (m(days * Pmax), f"Uses the {m(Pmax)}-a-day statutory maximum. The agency's published schedule, which it has applied in every case, sets {m(P)} a day for a first inspection, so that is the best estimate."),
        "demand": (m(key_v + Dm), f"Also accrues the competitor's {m(Dm)} demand. Counsel can't yet assess the outcome or the amount of any loss, so the suit is disclosed, not accrued; a plaintiff's demand isn't an estimate of the loss."),
        "demand_only": (m(Dm), f"Accrues the competitor's {m(Dm)} demand and nothing for the discharges. The demand isn't an estimate counsel supports, and the scheduled penalty is both probable and estimable."),
    }
    key = (m(key_v), f"Correct. {days} days × {m(P)} scheduled penalty; nothing for the patent suit.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft note on contingencies, for December 31 statements not yet issued, describes two matters and says no liability has been recorded for either. First, a state environmental agency inspection in {p['insp']} found that {s}'s plant had discharged wastewater above its permit limits on {days} separate days; the agency hasn't issued a penalty notice. Counsel's letter says that after every inspection with findings in the past ten years the agency has assessed penalties under its published schedule, which sets {m(P)} for each day of violation found at a first inspection, though the statute allows up to {m(Pmax)} a day; this was {s}'s first inspection. Second, in {p['sued']} a competitor sued {s} for patent infringement, demanding {m(Dm)}; counsel's letter says discovery hasn't begun and counsel can't yet assess the likely outcome or the amount of any loss. What total liability should {s} accrue at December 31 for these two matters?""",
        choices, ans,
        f"""An unasserted claim is accrued when it is probable that it will be asserted and that the outcome will be unfavorable, and the loss can be reasonably estimated (ASC 450-20-25-2; ASC 450-20-50-6). The agency has assessed scheduled penalties after every inspection with findings, so a penalty is probable even though no notice has been issued, and its schedule estimates it: {days} days × {m(P)} = {m(key_v)}. The statutory maximum isn't the best estimate when the agency consistently applies its schedule. The patent suit can't yet be assessed or estimated, so nothing is accrued; the note discloses it (ASC 450-20-50-3 to 50-5). Liability = {m(key_v)}.""",
    )


def indemnity_and_whistleblower(p):
    co, s, Y = p["co"], short(p["co"]), p["Y"]
    cap, lo, best, W = D(p["cap"]), D(p["lo"]), D(p["best"]), D(p["W"])
    mid = (lo + cap) / 2
    pool = {
        "low": (m(lo), f"Accrues the {m(lo)} low end of the consultant's range. When counsel's letter names {m(best)} as the best estimate within the range, that amount is accrued rather than the minimum."),
        "mid": (m(mid), f"Accrues the {m(lo)}-to-{m(cap)} range's midpoint. Counsel's letter names {m(best)}, not the midpoint, as the best estimate."),
        "high": (m(cap), f"Accrues the {m(cap)} cap, the top of the range, rather than the {m(best)} counsel names as the best estimate."),
        "whistle": (m(best + W), f"Also accrues the {m(W)} the complaint alleges. Counsel told the committee it is too early to gauge the outcome or the exposure, so the matter isn't accrued; an allegation isn't an estimate of loss."),
    }
    key = (m(best), f"Correct. {s} accrues counsel's stated best estimate for the indemnity, {m(best)}, and nothing for the whistleblower matter.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Before its Year {Y} statements are issued, {co}'s files on two matters include a letter from outside counsel and minutes of its compliance committee. Counsel's letter concerns an indemnity in the agreement under which {s} sold its {p['division']} division in an earlier year: {s} agreed to reimburse the buyer for up to {m(cap)} of environmental cleanup costs at a site the division used. The indemnity's fair value when it was given was immaterial, and {s} recognized no liability for it then. In {p['order']}, Year {Y}, the state ordered the buyer to clean up the site, and the buyer has submitted its claim under the indemnity; counsel, citing a consultant's site assessment, estimates the cost at between {m(lo)} and {m(cap)} and names {m(best)} as the best estimate within that range. The committee's minutes describe a whistleblower complaint received in {p['wmonth']}, alleging {m(W)} of improper payments to a supplier; the outside counsel investigating it told the committee it is too early in the inquiry to gauge either the outcome or the exposure. What liability should {s} accrue at year-end for these two matters?""",
        choices, ans,
        f"""With the cleanup ordered and the buyer's claim submitted, payment under the indemnity is probable, and counsel's letter names a best estimate within the range, {m(best)}, which {s} accrues (ASC 450-20-25-2; ASC 450-20-30-1); the minimum or midpoint is used only when no amount in the range is a better estimate than another. The whistleblower matter has reached no conclusion: counsel can't yet assess the outcome or the exposure, so no amount is accrued, and the {m(W)} the complaint alleges is not an estimate of loss; the matter is considered for disclosure (ASC 450-20-50-3 to 50-5). Liability = {m(best)}.""",
    )


# ── III.G.b Application: calculate adjustments for identified subsequent events ─────────────────────────────


def se_bonus(p):
    co, s = p["co"], short(p["co"])
    b, I, A, T, G = D(p["b"]) / 100, D(p["I"]), D(p["A"]), D(p["T"]), D(p["G"])
    base = I - T
    key_v = rd(base * b)
    pool = {
        "ignore_tax": (m(rd(I * b)), f"Computes the bonus on the draft {m(I)}. The final Year 1 property tax bill shows a Year 1 expense {m(T)} higher than accrued, a condition that existed at year-end, so Year 1 income and the bonus base fall by {m(T)}."),
        "add_gain": (m(rd((base + G) * b)), f"Adds the {m(G)} gain on the February warehouse sale to the bonus base. That sale is a Year 2 transaction; it isn't part of Year 1 income."),
        "accrued": (m(A), f"Keeps the {m(A)} year-end estimate. The bonus is fixed by Year 1 income as finally reported, which subsequent events determine, so the accrual is adjusted to that amount."),
        "net": (m(rd(base * b / (1 + b))), f"Computes the bonus on income after deducting the bonus itself. The plan bases it on income before the bonus and income taxes."),
    }
    key = (m(key_v), f"Correct. {pct(p['b'])} × ({m(I)} − {m(T)}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s bonus plan pays employees a Year 1 bonus pool equal to {pct(p['b'])} of Year 1 income before the bonus and income taxes, as finally reported in the Year 1 financial statements. At December 31, Year 1, {s} accrued {m(A)} as its estimate of the pool. Its draft Year 1 income before the bonus and income taxes is {m(I)}. The statements will be issued on March {p['iday']}, Year 2. Before then: on January {p['tday']}, {s} received the county's final property tax bill for Year 1, which is {m(T)} higher than the amount {s} accrued for Year 1; and on February {p['gday']}, {s} sold a warehouse at a gain of {m(G)}. What bonus expense should {s} report for Year 1?""",
        choices, ans,
        f"""The final property tax bill gives better evidence of a Year 1 expense, a condition that existed at December 31, so it is a recognized subsequent event (ASC 855-10-25-1): Year 1 income before the bonus and taxes becomes {m(I)} − {m(T)} = {m(base)}. The warehouse sale is a Year 2 transaction, a nonrecognized subsequent event (ASC 855-10-25-3), and doesn't enter Year 1 income. The bonus is earned in Year 1, and its final amount, fixed after year-end by Year 1 results, adjusts the {m(A)} accrual: {pct(p['b'])} × {m(base)} = {m(key_v)}.""",
    )


def se_bankruptcy(p):
    co, s, Y = p["co"], short(p["co"]), p["Y"]
    I, R, K, S, Dv = D(p["I"]), D(p["R"]), D(p["K"]), D(p["S"]), D(p["Div"])
    loss = R - K - S
    key_v = I - loss
    pool = {
        "whole": (m(I - (R - S)), f"Writes off the whole {m(R)} balance, ignoring the {m(K)} {s} still expects to collect from the bankruptcy estate."),
        "no_allow": (m(I - (R - K)), f"Charges the full {m(R - K)} expected shortfall to Year {Y} income without counting the {m(S)} already provided for this customer in the year-end allowance."),
        "div": (m(key_v - Dv), f"Also deducts the {m(Dv)} dividend declared in February. A dividend declared after year-end is a Year {Y + 1} distribution, not a Year {Y} expense; it is disclosed."),
        "draft": (m(I), f"Leaves the draft unchanged. The bankruptcy confirms losses the customer was already suffering at year-end, so the allowance is increased for Year {Y}."),
    }
    key = (m(key_v), f"Correct. {m(I)} − ({m(R)} − {m(K)} expected recovery − {m(S)} already allowed).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year {Y} income before income taxes is {m(I)}. Its allowance for credit losses at December 31, Year {Y}, includes {m(S)} for the {m(R)} owed by {p['cust']}, a customer that had reported losses in each quarter of Year {Y} and had paid its last three invoices of the year more than 90 days late. On January {p['bday']}, Year {Y + 1}, {p['cust']} filed for bankruptcy, and {s} now expects to collect {m(K)} of the balance. On February {p['dday']}, Year {Y + 1}, {s}'s board declared a cash dividend of {m(Dv)}. The statements will be issued in March, Year {Y + 1}, and {s} has not elected the ASU 2025-05 practical expedient for current receivables. Ignore income taxes. What income before income taxes should {s} report for Year {Y}?""",
        choices, ans,
        f"""The bankruptcy resulted from financial difficulties that existed at December 31, so it is evidence about the year-end allowance and is recognized (ASC 855-10-55-1; ASC 326-20-30): expected loss on the balance = {m(R)} − {m(K)} = {m(R - K)}, of which {m(S)} is already in the allowance, so Year {Y} credit loss expense rises by {m(loss)}. The dividend, declared after year-end, is a nonrecognized subsequent event, disclosed but not reflected in Year {Y} (ASC 855-10-25-3); a dividend isn't an expense in any case. Income before income taxes = {m(I)} − {m(loss)} = {m(key_v)}.""",
    )


# ── III.G.c Analysis: derive the impact of identified subsequent events ──────────────────────────────────────


def se_working_capital(p):
    co, s, Y = p["co"], short(p["co"]), p["Y"]
    CA, CL, wA, wS, X, Rc = D(p["CA"]), D(p["CL"]), D(p["wA"]), D(p["wS"]), D(p["X"]), D(p["Rc"])
    add = (wS - wA) + X
    key_v = CA - (CL + add)
    pool = {
        "write_off": (m(key_v - Rc), f"Also writes off the {m(Rc)} owed by {p['cust']}. The customer was paying within terms and its credit line had just been renewed at year-end; its default came from a regulation that took effect after year-end, a condition that arose after the balance sheet date, so it is disclosed, not recognized."),
        "no_warranty": (m(CA - (CL + X)), f"Leaves out the additional {m(wS - wA)} owed on the warranty claim, which settled for more than the {m(wA)} accrued at year-end for units sold before then."),
        "no_tax": (m(CA - (CL + wS - wA)), f"Leaves out the {m(X)} sales-tax assessment. It arises from Year {Y} sales, a condition that existed at year-end, so it is recognized even though the audit concluded after year-end."),
        "draft": (m(CA - CL), f"Accepts the draft balances, {m(CA)} of current assets and {m(CL)} of current liabilities, without recognizing either the warranty settlement or the tax assessment."),
    }
    key = (m(key_v), f"Correct. {m(CA)} − ({m(CL)} + {m(wS - wA)} warranty + {m(X)} sales tax).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year {Y}, balance sheet reports current assets of {m(CA)} and current liabilities of {m(CL)}; the statements will be issued on March {p['iday']}, Year {Y + 1}. Between those dates: a warranty claim on units {s} sold before year-end, for which {s} had accrued {m(wA)}, was settled for {m(wS)}; on {p['tdate']}, Year {Y + 1}, a state audit of {s}'s Year {Y} sales concluded that {s} had failed to collect sales tax on certain Year {Y} sales and assessed {m(X)}, payable in April, for which {s} had accrued nothing; and {p['cust']}, a customer that owed {m(Rc)} at year-end, defaulted on its balance after {article(p['reg'])} {p['reg']} that the government announced and put into effect in {p['rmonth']}, Year {Y + 1}, cut off its export business. Through December, {p['cust']} had paid every invoice within terms, and its bank had renewed its credit line in December. {s} has not elected the ASU 2025-05 practical expedient for current receivables. What working capital (current assets minus current liabilities) should {s} report at December 31, Year {Y}?""",
        choices, ans,
        f"""The warranty settlement and the sales-tax assessment both give evidence about conditions that existed at year-end (units already sold, Year {Y} sales already made), so both are recognized (ASC 855-10-25-1): current liabilities rise by {m(wS)} − {m(wA)} = {m(wS - wA)} and by {m(X)}. {poss(p['cust'])} default resulted from a regulation announced and effective after year-end, a condition arising after the balance sheet date, so it is disclosed, not recognized, and the receivable isn't written down (ASC 855-10-25-3, 855-10-55-2). Working capital = {m(CA)} − ({m(CL)} + {m(add)}) = {m(key_v)}.""",
    )


def se_total_assets(p):
    co, s, Y = p["co"], short(p["co"]), p["Y"]
    TA, R, Ap, dec, aw = D(p["TA"]), D(p["R"]), D(p["Ap"]), D(p["dec"]), D(p["aw"])
    key_v = TA - (R - Ap)
    pool = {
        "draft": (m(TA), f"Leaves the {m(R)} insurance receivable as recorded. The insurer's assessment shows how much of the December loss was recoverable at year-end, so the receivable is reduced to the {m(Ap)} it paid."),
        "decline": (m(key_v - dec), f"Also writes down the securities for the {m(dec)} decline in February. The fall in prices came from a market move after year-end and doesn't reflect conditions at December 31."),
        "award": (m(key_v + aw), f"Also adds the {m(aw)} court award. The supplier has appealed; a gain contingency isn't recognized before it is realized, even when a favorable judgment comes before the statements are issued."),
        "writeoff": (m(TA - R), f"Removes the whole {m(R)} receivable, as if an insurance recovery could be recognized only when paid. The {m(Ap)} the insurer paid was recoverable at year-end."),
    }
    key = (m(key_v), f"Correct. {m(TA)} − ({m(R)} − {m(Ap)}) insurance shortfall.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year {Y}, balance sheet reports total assets of {m(TA)}. In December, a hailstorm damaged {s}'s {p['assets']}; {s} wrote them down and recorded a {m(R)} receivable for the insurance recovery it expected. The statements will be issued on March {p['iday']}, Year {Y + 1}. Before then: in January, the insurer completed its assessment under the policy in force at the time of the storm and paid {m(Ap)} in full settlement of the claim; in February, a court awarded {s} {m(aw)} in its suit against a former supplier, and the supplier has appealed; and also in February, a broad decline in equity markets cut {m(dec)} from the fair value of {s}'s portfolio of listed securities. What total assets should {s} report at December 31, Year {Y}?""",
        choices, ans,
        f"""The insurer's assessment applies the policy in force at the time of the December storm, so it is evidence of the amount recoverable at year-end and is recognized: the receivable falls from {m(R)} to {m(Ap)}, a {m(R - Ap)} reduction (ASC 855-10-25-1). The court award is a gain contingency, still under appeal; it isn't recognized until realized (ASC 450-30-25-1) and is disclosed. The market decline reflects conditions that arose after year-end and is disclosed, not recognized (ASC 855-10-25-3, 855-10-55-2). Total assets = {m(TA)} − {m(R - Ap)} = {m(key_v)}.""",
    )


def se_retained_earnings(p):
    co, s, Y = p["co"], short(p["co"]), p["Y"]
    RE, acc, neg, sd, t = D(p["RE"]), D(p["acc"]), D(p["neg"]), D(p["sd"]), D(p["t"]) / 100
    diff = acc - neg
    net = rd(diff * (1 - t))
    key_v = RE + net
    keep = 100 - int(p["t"])
    pool = {
        "stockdiv": (m(key_v - sd), f"Also deducts {m(sd)} for the stock dividend declared in {p['sdmonth']}. {s} is a private company, so a stock dividend declared after year-end is recorded in Year {Y + 1} and doesn't change December 31, Year {Y}, retained earnings; it is disclosed."),
        "sign": (m(RE - net), f"Subtracts the adjustment. The negotiated penalty is lower than the amount accrued at year-end, so the correction raises revenue and retained earnings, net of tax."),
        "pretax": (m(RE + diff), f"Adds the full pretax {m(diff)} reduction in the penalty, without its {p['t']}% tax effect."),
        "draft": (m(RE), f"Accepts the draft {m(RE)}. The negotiation fixes the amount of an obligation that existed at year-end, so the accrual is adjusted."),
    }
    key = (m(key_v), f"Correct. {m(RE)} + ({m(acc)} − {m(neg)}) × {keep}%.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a private company that is not an SEC filer, has a draft December 31, Year {Y}, balance sheet that reports retained earnings of {m(RE)}. That balance reflects a {m(acc)} penalty, recorded as a reduction of revenue, that {s} expected to owe a customer under their contract for missing a Year {Y} delivery deadline. The statements will be available to be issued on March {p['iday']}, Year {Y + 1}. In {p['negmonth']}, Year {Y + 1}, {s} and the customer finished negotiating the penalty and fixed it at {m(neg)}. In {p['sdmonth']}, Year {Y + 1}, {s}'s board declared a {p['sdpct']}% stock dividend, recorded at {m(sd)}. {s}'s tax rate is {p['t']}% for all effects. What retained earnings should {s} report at December 31, Year {Y}?""",
        choices, ans,
        f"""A penalty payable to a customer is variable consideration, which reduces revenue (ASC 606-10-32-5 to 32-9). The negotiation, completed before the statements were available to be issued, fixes the amount of an obligation that existed at year-end, so it is a recognized subsequent event (ASC 855-10-25-1): the {m(acc)} accrual falls to {m(neg)}, raising Year {Y} revenue by {m(diff)}, or {m(net)} after the {p['t']}% tax. For a company that isn't an SEC filer, a stock dividend declared after year-end is recorded when declared, in Year {Y + 1}, and disclosed (ASC 855-10-25-3); only SEC registrants give such dividends retroactive effect in the balance sheet (SEC SAB Topic 4C). Retained earnings = {m(RE)} + {m(net)} = {m(key_v)}.""",
    )


FAMILIES = [
    ("far-change-in-estimate-0003", A3, T_CHG, AP,
     ["ASC 250-10-45-17 (change in accounting estimate: prospective application)"],
     change_in_estimate, [
        dict(co="Pelton Fixtures Co.", cost=720000, L0=10, S0=60000, n=4, L1=8, S1=36000, use=["retro", "no_salv", "old_life"]),
        dict(co="Ashgrove Metalworks Co.", cost=900000, L0=9, S0=72000, n=3, L1=8, S1=54000, use=["salv_old", "old_life", "total_life"]),
        dict(co="Dunmore Fabrication Co.", cost=540000, L0=8, S0=48000, n=2, L1=6, S1=24000, use=["retro", "salv_old", "old_life"]),
        dict(co="Kellerton Casting Co.", cost=1080000, L0=12, S0=90000, n=5, L1=10, S1=60000, use=["no_salv", "retro", "total_life"]),
     ], "retro"),
    ("far-change-in-principle-0003", A3, T_CHG, AP,
     ["ASC 250-10-45-5 to 45-8 (retrospective application of a change in accounting principle; indirect effects)"],
     change_in_principle, [
        dict(co="Verity Hardware Co.", old="FIFO", new="weighted-average", Y=4, why="weighted-average better matches the cost of its interchangeable stock",
             old_inv=[560000, 640000, 700000], new_inv=[500000, 555000, 570000], t=25, b=10, NI=620000, use=["bonus", "prior", "sign"]),
        dict(co="Linwood Supply Co.", old="weighted-average", new="FIFO", Y=5, why="FIFO better reflects the current cost of its goods on hand",
             old_inv=[430000, 470000, 520000], new_inv=[510000, 580000, 670000], t=21, b=10, NI=540000, use=["bonus", "cum", "prior"]),
        dict(co="Marchant Trading Co.", old="LIFO", new="FIFO", Y=4, why="FIFO better reflects the current cost of its goods on hand",
             old_inv=[380000, 410000, 430000], new_inv=[470000, 530000, 600000], t=25, b=12, NI=760000, use=["bonus", "prior", "sign"]),
        dict(co="Oswestry Goods Co.", old="LIFO", new="weighted-average", Y=5, why="weighted-average better matches the cost of its interchangeable stock",
             old_inv=[245000, 260000, 280000], new_inv=[290000, 325000, 375000], t=21, b=12, NI=450000, use=["cum", "pretax", "bonus"]),
     ], "bonus"),
    ("far-error-correction-0001", A3, T_CHG, AP,
     ["ASC 250-10-45-23 (correction of a prior-period error: adjustment to opening retained earnings, net of tax)"],
     error_correction, [
        dict(co="Halloway Freight Co.", P=480000, r=6, start="April", term=4, found="May", t=25, use=["only_y1", "full_y1", "thru_found"]),
        dict(co="Brindlewood Supply Co.", P=800000, r=6, start="July", term=5, found="March", t=21, use=["pretax", "full_y1", "thru_found"]),
        dict(co="Castlemain Equipment Co.", P=360000, r=8, start="October", term=4, found="April", t=25, use=["thru_found", "pretax", "full_y1"]),
        dict(co="Fenwright Leasing Co.", P=600000, r=5, start="May", term=6, found="February", t=21, use=["only_y1", "full_y1", "pretax"]),
     ], "only_y1"),
    ("far-accounting-errors-0010", A3, T_CHG, AN,
     ["ASC 606-10-55-22 to 55-29 (sales with a right of return)", "ASC 360-10-30-1 (cost of property includes costs to bring it to its intended use)", "ASC 606-10-45-2 (contract liabilities)"],
     ae_returns_install, [
        dict(co="Westerham Devices Co.", Y=2, NI=640000, S=180000, rp=10, cp=60, month="September", asset="packaging machine", P=270000, f=9000, i=51000, L=5, dday=20, Dp=25000, use=["gross_ret", "full_year", "deposit"]),
        dict(co="Allerton Systems Co.", Y=3, NI=520000, S=150000, rp=12, cp=40, month="July", asset="laser cutter", P=210000, f=6000, i=42000, L=4, dday=18, Dp=19000, use=["no_dep", "deposit", "no_returns"]),
        dict(co="Brockhollow Data Co.", Y=1, NI=780000, S=240000, rp=8, cp=65, month="October", asset="bottling line", P=390000, f=12000, i=60000, L=4, dday=22, Dp=34000, use=["gross_ret", "no_dep", "deposit"]),
        dict(co="Pennycross Tech Co.", Y=4, NI=455000, S=120000, rp=15, cp=45, month="August", asset="milling machine", P=180000, f=5000, i=31000, L=3, dday=19, Dp=16000, use=["gross_ret", "no_dep", "no_returns"]),
     ], "gross_ret"),
    ("far-accounting-errors-0011", A3, T_CHG, AN,
     ["ASC 440-10 (purchase commitments: executory until performance)", "FASB Concepts Statement No. 8, chapter 4 (definition of a liability; dividends payable on declaration)", "ASC 606-10-25-30 (transfer of control: shipping terms)"],
     ae_liabilities, [
        dict(co="Thistlewood Retail Co.", Y=2, TL=1860000, PO=52000, po_item="replacement parts", dday=18, dps="0.60", sh=225000, tr=15000, pday=20, INV=38000, inv_item="display racks", use=["drop_inv", "no_div", "draft"]),
        dict(co="Grantley Mercantile Co.", Y=3, TL=1240000, PO=61000, po_item="packaging supplies", dday=16, dps="0.25", sh=128000, tr=24000, pday=15, INV=27000, inv_item="checkout counters", use=["drop_inv", "issued", "keep_po"]),
        dict(co="Oakhurst Wholesale Co.", Y=1, TL=2920000, PO=67000, po_item="warehouse racking", dday=19, dps="0.50", sh=320000, tr=40000, pday=22, INV=44000, inv_item="sales-floor fixtures", use=["draft", "issued", "keep_po"]),
        dict(co="Welbridge Trading Co.", Y=4, TL=980000, PO=29000, po_item="replacement blades", dday=17, dps="0.40", sh=150000, tr=10000, pday=18, INV=21000, inv_item="storage cabinets", use=["drop_inv", "no_div", "keep_po"]),
     ], "drop_inv"),
    ("far-accounting-errors-0012", A3, T_CHG, AN,
     ["ASC 310-10 and ASC 835-30 (interest on notes receivable accrues as earned)", "ASC 321-10-35-1 (equity securities measured at fair value through net income)", "ASC 606-10-55-79 to 55-80 (consignment arrangements)"],
     ae_assets, [
        dict(co="Hartswell Logistics Co.", Y=2, TA=2360000, N=600000, r=9, month="September", term=9, C=310000, FV=270000, G=63000, use=["consigned", "term", "at_cost"]),
        dict(co="Candleford Distribution Co.", Y=3, TA=1980000, N=480000, r=10, month="October", term=6, C=240000, FV=275000, G=41000, use=["draft", "full_year", "at_cost"]),
        dict(co="Marldon Freight Co.", Y=1, TA=3120000, N=720000, r=8, month="August", term=6, C=420000, FV=372000, G=78000, use=["full_year", "at_cost", "consigned"]),
        dict(co="Ellenbridge Supply Co.", Y=4, TA=1540000, N=360000, r=10, month="July", term=9, C=180000, FV=207000, G=34000, use=["full_year", "term", "consigned"]),
     ], "consigned"),
    ("far-contingencies-0015", A3, T_CON, AP,
     ["ASC 450-20-25-2 and 450-20-50-6 (accrual of loss contingencies, including unasserted claims)", "ASC 450-20-30-1 (range of loss with no best estimate: accrue the minimum)", "ASC 250-10-45-17 (change in estimate)"],
     litigation_and_recall, [
        dict(co="Oldcastle Mills Co.", A=180000, Pd=70000, Inc=55000, L=60000, H=140000, product="space heater", part="thermostat", use=["mid", "high", "no_paid"]),
        dict(co="Ferngate Products Co.", A=240000, Pd=90000, Inc=65000, L=85000, H=205000, product="dehumidifier", part="fan motor", use=["unasserted", "mid", "no_inc"]),
        dict(co="Brackendale Goods Co.", A=130000, Pd=50000, Inc=40000, L=45000, H=115000, product="toaster oven", part="heating element", use=["unasserted", "mid", "high"]),
        dict(co="Southmoor Appliance Co.", A=310000, Pd=120000, Inc=80000, L=110000, H=250000, product="dishwasher", part="water valve", use=["unasserted", "no_inc", "no_paid"]),
     ], "mid"),
    ("far-contingencies-0016", A3, T_CON, AP,
     ["ASC 330-10-35-17 to 35-18 (losses on firm purchase commitments)", "ASC 606-10-32-25 (consideration payable to a customer)", "ASC 606-10-32-10 (refund liabilities)"],
     commitment_and_rebate, [
        dict(co="Harmondsgate Textiles Co.", Q=40000, unit="pound", mat="cotton yarn", Pc="4.80", Pm="4.05", N=30000, goods="packs of towels", r=2, rp=35, paid=9600, through="March", use=["all_claim", "no_paid", "full_contract"]),
        dict(co="Westrill Fabrics Co.", Q=60000, unit="yard", mat="synthetic fiber", Pc="3.40", Pm="2.95", N=24000, goods="sets of bed linens", r=5, rp=30, paid=14000, through="April", use=["no_commit", "no_rebate", "all_claim"]),
        dict(co="Allonby Weaving Co.", Q=28000, unit="pound", mat="wool roving", Pc="6.40", Pm="5.60", N=18000, goods="wool blankets", r=4, rp=40, paid=11000, through="February", use=["no_rebate", "no_paid", "full_contract"]),
        dict(co="Pennybridge Mills Co.", Q=52000, unit="spool", mat="dyed thread", Pc="2.95", Pm="2.50", N=36000, goods="tablecloths", r=3, rp=25, paid=8500, through="May", use=["no_commit", "no_rebate", "no_paid"]),
     ], "all_claim"),
    ("far-contingencies-0017", A3, T_CON, AP,
     ["ASC 450-20-25-2 (accrual of probable, estimable losses, including incurred-but-not-reported claims of a self-insured entity)", "SEC SAB Topic 5Y and ASC 835-30 (discounting when the amount and timing of payments are fixed)"],
     settlement_and_selfinsurance, [
        dict(co="Cranmoor Devices Co.", now=120000, later=90000, i=6, Ar=38000, Ai=26000, B=70000, workers="warehouse workers", use=["undiscounted", "compounded", "future"]),
        dict(co="Bellingfield Products Co.", now=160000, later=130000, i=8, Ar=52000, Ai=31000, B=95000, workers="delivery drivers", use=["undiscounted", "omit_now", "reported"]),
        dict(co="Oaktree Instruments Co.", now=95000, later=70000, i=5, Ar=27000, Ai=18000, B=50000, workers="assembly workers", use=["compounded", "reported", "future"]),
        dict(co="Longmarsh Appliances Co.", now=210000, later=180000, i=7, Ar=64000, Ai=43000, B=120000, workers="installation crews", use=["omit_now", "reported", "compounded"]),
     ], "future"),
    ("far-contingencies-0018", A3, T_CON, AN,
     ["ASC 450-20-25-2 and 450-20-50-6 (accrual of unasserted claims)", "ASC 450-20-50-3 to 50-5 (disclosure of a loss contingency that cannot be estimated)"],
     draft_note_penalty, [
        dict(co="Marrowfield Industries Co.", days=14, P=9500, Pmax=25000, Dm=1200000, insp="November", sued="October", use=["zero", "max", "demand"]),
        dict(co="Caldervale Products Co.", days=9, P=12000, Pmax=30000, Dm=850000, insp="October", sued="September", use=["max", "demand", "demand_only"]),
        dict(co="Thornbury Mills Co.", days=21, P=6000, Pmax=20000, Dm=640000, insp="December", sued="November", use=["max", "demand", "demand_only"]),
        dict(co="Westvale Holdings Co.", days=12, P=11000, Pmax=27500, Dm=1500000, insp="September", sued="August", use=["zero", "demand", "demand_only"]),
     ], "zero"),
    ("far-contingencies-0019", A3, T_CON, AN,
     ["ASC 450-20-25-2 and 450-20-30-1 (accrual at the best estimate within a range when one exists)", "ASC 450-20-50-3 to 50-5 (disclosure when a loss cannot yet be estimated)"],
     indemnity_and_whistleblower, [
        dict(co="Ambersgate Holdings Co.", Y=1, division="packaging", cap=420000, lo=180000, best=310000, order="September", W=95000, wmonth="October", use=["low", "mid", "whistle"]),
        dict(co="Follyfield Group Co.", Y=2, division="logistics", cap=560000, lo=240000, best=380000, order="August", W=130000, wmonth="November", use=["mid", "whistle", "high"]),
        dict(co="Ridgemont Holdings Co.", Y=3, division="distribution", cap=350000, lo=150000, best=230000, order="July", W=70000, wmonth="September", use=["low", "whistle", "high"]),
        dict(co="Oversley Group Co.", Y=1, division="specialty chemicals", cap=680000, lo=300000, best=470000, order="October", W=150000, wmonth="December", use=["low", "mid", "high"]),
     ], "whistle"),
    ("far-subsequent-events-0014", A3, T_SUB, AP,
     ["ASC 855-10-25-1 (recognized subsequent events)", "ASC 855-10-25-3 (nonrecognized subsequent events)"],
     se_bonus, [
        dict(co="Brockley Instruments Co.", b=8, I=3450000, A=270000, T=42000, G=380000, iday=6, tday=28, gday=12, use=["ignore_tax", "add_gain", "net"]),
        dict(co="Kelsall Plastics Co.", b=6, I=2860000, A=165000, T=35000, G=290000, iday=11, tday=22, gday=9, use=["ignore_tax", "accrued", "net"]),
        dict(co="Ravensworth Foods Co.", b=10, I=1980000, A=205000, T=26000, G=240000, iday=4, tday=30, gday=17, use=["ignore_tax", "add_gain", "accrued"]),
        dict(co="Tilshead Components Co.", b=5, I=4120000, A=196000, T=58000, G=450000, iday=13, tday=26, gday=20, use=["ignore_tax", "accrued", "net"]),
     ], "ignore_tax"),
    ("far-subsequent-events-0015", A3, T_SUB, AP,
     ["ASC 855-10-25-1 and 855-10-55-1 (recognized subsequent events: a customer's bankruptcy from deterioration before year-end)", "ASC 855-10-25-3 (nonrecognized subsequent events)", "ASC 326-20-30 (expected credit losses)"],
     se_bankruptcy, [
        dict(co="Marrowbrook Supply Co.", Y=1, I=1860000, R=220000, K=44000, S=30000, Div=90000, cust="Hollins Retail", bday=17, dday=8, use=["div", "whole", "no_allow"]),
        dict(co="Clearmont Industries Co.", Y=2, I=2340000, R=310000, K=93000, S=45000, Div=120000, cust="Dalby Outfitters", bday=24, dday=12, use=["div", "draft", "no_allow"]),
        dict(co="Fallowgate Products Co.", Y=3, I=1420000, R=160000, K=36000, S=16000, Div=60000, cust="Penrose Hardware", bday=9, dday=19, use=["whole", "no_allow", "draft"]),
        dict(co="Berrowfield Co.", Y=4, I=2960000, R=380000, K=114000, S=60000, Div=150000, cust="Gatley Stores", bday=13, dday=4, use=["div", "whole", "draft"]),
     ], "div"),
    ("far-subsequent-events-0016", A3, T_SUB, AN,
     ["ASC 855-10-25-1 (recognized subsequent events: conditions existing at the balance sheet date)", "ASC 855-10-25-3 and 855-10-55-2 (nonrecognized subsequent events: conditions arising after that date)"],
     se_working_capital, [
        dict(co="Ellersby Components Co.", Y=1, CA=2460000, CL=1180000, wA=52000, wS=81000, X=46000, Rc=140000, cust="Marbury Exports", reg="export-licensing regulation", rmonth="January", tdate="February 9", iday=10, use=["write_off", "no_warranty", "no_tax"]),
        dict(co="Thornleigh Devices Co.", Y=2, CA=3180000, CL=1540000, wA=68000, wS=97000, X=58000, Rc=175000, cust="Castleport Traders", reg="customs-tariff order", rmonth="February", tdate="February 16", iday=18, use=["no_warranty", "no_tax", "draft"]),
        dict(co="Mossgate Fabrications Co.", Y=3, CA=1920000, CL=940000, wA=41000, wS=63000, X=37000, Rc=110000, cust="Harrowfield Freight", reg="trade-sanctions order", rmonth="January", tdate="February 2", iday=5, use=["write_off", "no_tax", "draft"]),
        dict(co="Pemberfield Alloys Co.", Y=4, CA=2720000, CL=1360000, wA=59000, wS=88000, X=52000, Rc=155000, cust="Greystoke Imports", reg="export-control amendment", rmonth="February", tdate="March 3", iday=22, use=["write_off", "no_warranty", "draft"]),
     ], "write_off"),
    ("far-subsequent-events-0017", A3, T_SUB, AN,
     ["ASC 855-10-25-1 (recognized subsequent events)", "ASC 855-10-25-3 and 855-10-55-2 (nonrecognized subsequent events)", "ASC 450-30-25-1 (gain contingencies not recognized before realization)"],
     se_total_assets, [
        dict(co="Longstone Materials Co.", Y=1, TA=8460000, R=96000, Ap=58000, dec=120000, aw=150000, assets="delivery vans", iday=14, use=["draft", "decline", "writeoff"]),
        dict(co="Castlebrook Supply Co.", Y=2, TA=6240000, R=74000, Ap=49000, dec=88000, aw=120000, assets="forklifts", iday=20, use=["draft", "decline", "award"]),
        dict(co="Ferrybridge Traders Co.", Y=3, TA=10180000, R=132000, Ap=87000, dec=96000, aw=210000, assets="warehouse roofs", iday=11, use=["draft", "writeoff", "award"]),
        dict(co="Oldfen Mercantile Co.", Y=4, TA=4920000, R=61000, Ap=38000, dec=67000, aw=95000, assets="greenhouses", iday=8, use=["draft", "decline", "writeoff"]),
     ], "decline"),
    ("far-subsequent-events-0018", A3, T_SUB, AN,
     ["ASC 855-10-25-1 and 25-3 (recognized versus nonrecognized subsequent events)", "ASC 606-10-32-5 to 32-9 (variable consideration: penalties payable to a customer)", "SEC SAB Topic 4C (retroactive effect of later stock dividends, for SEC registrants only)"],
     se_retained_earnings, [
        dict(co="Hallowfield Textiles Co.", Y=1, RE=1240000, acc=140000, neg=95000, sd=260000, sdpct=5, t=25, iday=12, negmonth="January", sdmonth="February", use=["stockdiv", "sign", "pretax"]),
        dict(co="Marplewood Fabrics Co.", Y=2, RE=1180000, acc=110000, neg=72000, sd=190000, sdpct=4, t=21, iday=27, negmonth="February", sdmonth="March", use=["stockdiv", "sign", "draft"]),
        dict(co="Oakenshaw Goods Co.", Y=3, RE=2360000, acc=175000, neg=120000, sd=340000, sdpct=6, t=25, iday=9, negmonth="January", sdmonth="February", use=["stockdiv", "draft", "pretax"]),
        dict(co="Brimsdale Products Co.", Y=4, RE=1140000, acc=90000, neg=58000, sd=160000, sdpct=5, t=21, iday=24, negmonth="February", sdmonth="March", use=["sign", "draft", "pretax"]),
     ], "stockdiv"),
]


def blind_files(items, scratch):
    lines, keys = ["# FAR batch 17: blind verification input", "",
                   "Each block is one version of a question. Solve each independently; choose one letter.", ""], {}
    for it in items:
        for k, v in enumerate([it] + list(it.get("variants") or [])):
            label = f"{it['id']} v{k}"
            lines += [f"## {label}", "", v["stem"], ""]
            lines += [f"{c['id']}. {c['text']}" for c in v["choices"]] + [""]
            keys[label] = v["answer"]
    with open(os.path.join(scratch, "b17-blind.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(scratch, "b17-keys.json"), "w", encoding="utf-8", newline="\n") as f:
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
    assert len(items) == 16 and len({it["id"] for it in items}) == 16
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
    if SCRATCH:
        os.makedirs(SCRATCH, exist_ok=True)
        blind_files(items, SCRATCH)
    if "--dry-run" in sys.argv:
        print("dry run: nothing written")
        return
    write_items(items, CONTENT)


if __name__ == "__main__":
    main()
