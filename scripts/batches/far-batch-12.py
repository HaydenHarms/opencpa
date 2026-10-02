"""FAR batch 12 — 25 items written from scratch: a second item on fifteen one-item Application tasks in Areas I
and II (I.A.1b, I.A.2b, I.A.4a, I.A.4b, I.A.5b, I.A.6b, I.A.7a, I.B.1c, I.B.2c, I.E.c, II.A.a, II.D.d, II.D.e,
II.E.1b, II.E.1c) and ten Analysis items in Area III: four on deriving the impact of accounting changes and error
corrections (III.A.b), three on reviewing documentation for recognition versus disclosure (III.B.c) and three on
deriving the impact of subsequent events (III.G.c). Each Area III item changes at least two of the scenario's
component events against every existing item on its task, and uses a format those items don't.
Target skill mix 0 / 15 / 10; area mix 10 / 5 / 10. Scope and skill tags follow the AICPA CPA Exam Blueprints
effective January 2026.

Numeric items ship with three variants each (method as in far-batch-11.py): each item is a builder, parameter
set 0 is the item and sets 1-3 are its variants, every family must move the key's letter, and parameter set 0
must show the distractor for the item's central twist (`twist`, checked by the script).

Run: python3 scripts/batches/far-batch-12.py   See docs/reviews/far-batch-12.md.
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import json
import os
import re
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AN, AP, audit, attach_variants, finalize, fix_articles, mcq as _mcq, variant, write_items  # noqa: E402
from variants import m, n, pick, rd  # noqa: E402

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 12. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
SCRATCH = os.environ.get("B12_SCRATCH")


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


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
    """Report any dollar amount that appears more than once in a stem, or a choice that equals a stem amount.

    A repeat is fine only when it names the same fact twice; the lead reviews every line this prints."""
    amts = re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", v["stem"])
    dup = sorted({a for a in amts if amts.count(a) > 1})
    if dup:
        print(f"REPEAT {label}: stem repeats {', '.join(dup)}", file=sys.stderr)
    for c in v["choices"]:
        for a in re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", c["text"]):
            if a in amts:
                print(f"REPEAT {label}: choice {a} equals a stem amount", file=sys.stderr)


def spacing(label, v):
    """Flag two numeric choices closer together than 0.15% of the larger one (or $1,000)."""
    vals = []
    for c in v["choices"]:
        mm = re.match(r"\$([\d,]+(?:\.\d+)?)", c["text"])
        if not mm:
            return
        vals.append(float(mm.group(1).replace(",", "")))
    vals.sort()
    for a, b in zip(vals, vals[1:]):
        if b - a < max(1000, 0.0015 * b):
            print(f"CLOSE {label}: {a:,.0f} and {b:,.0f}", file=sys.stderr)


def short(name):
    return name.split()[0]


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole amount, got {x}"
    return x


def distinct(pool, key):
    """No pool value may equal the key or another pool value; amounts must be positive."""
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"
    assert all(not v.startswith("$-") and not v.startswith("$0 ") and v != "$0" for v in vals), vals


def build(pool, key, use):
    distinct(pool, key)
    return pick(pool, key, use)


def sc(p, f, units, **over):
    """A new parameter set: every amount in `units` scaled by f and rounded half up to a multiple of its unit."""
    q = dict(p)
    for k, u in units.items():
        q[k] = int(rd(D(p[k]) * D(str(f)) / u) * u)
    q.update(over)
    return q


def minus(x):
    """A signed amount for explanations: '$1,000' or '− $1,000'."""
    return m(x) if x >= 0 else "− " + m(-x)


# ── Area I Application ───────────────────────────────────────────────────


def bs_working_capital(p):
    co, s = p["co"], short(p["co"])
    wc0 = p["CA"] - p["CL"]
    ca = p["CA"] - p["t"] + p["o"]
    cl = p["CL"] + p["i"] + p["d"] + p["c"] + p["o"]
    key_v = ca - cl
    assert key_v == wc0 - p["t"] - p["i"] - p["d"] - p["c"] and key_v > 0
    pool = {
        "od_liab": (m(key_v - p["o"]), f"Adds the {m(p['o'])} overdraft to current liabilities but leaves cash net of it: {m(p['CA'] - p['t'])} − {m(cl)}. Reporting the overdraft separately also raises cash by {m(p['o'])}, so this correction leaves working capital unchanged."),
        "ts_keep": (m(key_v + p["t"]), f"Leaves the {m(p['t'])} of reacquired shares in short-term investments. Treasury stock is a deduction from stockholders' equity, not an asset, so current assets fall by {m(p['t'])}."),
        "cpltd": (m(key_v + p["c"]), f"Leaves the {m(p['c'])} installment in long-term debt. The part of long-term debt due within a year of the balance sheet date is a current liability."),
        "dep": (m(key_v + p["d"]), f"Leaves the {m(p['d'])} deposit in sales revenue. Until the goods are delivered, the deposit is a contract liability, which is current."),
        "int": (m(key_v + p["i"]), f"Leaves out the {m(p['i'])} of accrued interest. Interest accrued by year-end is a current liability even though it hasn't been paid."),
    }
    key = (m(key_v), f"Correct. ({m(p['CA'])} − {m(p['t'])} + {m(p['o'])}) − ({m(p['CL'])} + {m(p['i'])} + {m(p['d'])} + {m(p['c'])} + {m(p['o'])}) = {m(ca)} − {m(cl)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year 1, balance sheet reports total current assets of {m(p['CA'])} and total current liabilities of {m(p['CL'])}. The controller identifies these errors, none of which has been corrected: (1) interest of {m(p['i'])} that had accrued on a note payable by December 31 has not been recorded; (2) a {m(p['d'])} deposit that a customer paid on December 19 for goods to be delivered in February, Year 2, was credited to sales revenue; (3) the {m(p['c'])} principal installment of a long-term bank loan that falls due on {p['due']}, Year 2, is included in long-term debt; (4) cash is reported net of an {m(p['o'])} overdraft in {s}'s account at a second bank, which has no right to offset it against {s}'s other accounts; and (5) the {m(p['t'])} that {s} paid in November to reacquire some of its own common shares, which it holds for reissue, is included in short-term investments. What working capital should {s}'s corrected balance sheet report?""",
        choices, ans,
        f"""Current assets: the reacquired shares are treasury stock, a deduction from equity, so they come out of short-term investments (− {m(p['t'])}); and the overdraft at the second bank can't be netted against cash at another bank, so cash is reported gross (+ {m(p['o'])}). Corrected current assets = {m(ca)}. Current liabilities: accrued interest (+ {m(p['i'])}), the customer deposit, a contract liability until the goods are delivered (+ {m(p['d'])}), the installment due within a year (+ {m(p['c'])}) and the overdraft (+ {m(p['o'])}). Corrected current liabilities = {m(cl)}. Working capital = {m(ca)} − {m(cl)} = {m(key_v)}. The overdraft raises both sides equally, so it doesn't change working capital.""",
    )


def is_pretax_adjust(p):
    co, s = p["co"], short(p["co"])
    assert p["r"] % 6 == 0
    mo = p["r"] // 6
    key_v = p["P"] + p["k"] + p["g"] - 5 * mo + p["dv"]
    pool = {
        "div": (m(key_v - p["dv"]), f"Leaves the {m(p['dv'])} of dividends among the expenses. Dividends are distributions of retained earnings to owners, not expenses, so they come out of the income statement."),
        "rent_none": (m(key_v + 5 * mo), f"Leaves all {m(p['r'])} of rent in revenue. Only December's rent, {m(p['r'])} ÷ 6 = {m(mo)}, was earned in Year 2; the {m(5 * mo)} for January through May is unearned revenue, a liability."),
        "cons_sign": (m(key_v - 2 * p["k"]), f"Deducts the {m(p['k'])} of goods held by the dealer instead of adding them back. Goods out on consignment still belong to {s}, so ending inventory rises and cost of goods sold falls by {m(p['k'])}."),
        "oci": (m(key_v - p["g"]), f"Leaves the {m(p['g'])} fair value increase in other comprehensive income. Changes in the fair value of equity securities with readily determinable fair values are recognized in net income."),
    }
    key = (m(key_v), f"Correct. {m(p['P'])} + {m(p['k'])} + {m(p['g'])} − {m(5 * mo)} + {m(p['dv'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 income statement reports income before income taxes of {m(p['P'])}. The controller identifies these errors: (1) goods costing {m(p['k'])} that {s} had shipped to a dealer, who sells them on {s}'s behalf for a commission, were left out of {s}'s December 31 inventory, so their cost was included in cost of goods sold; (2) a {m(p['g'])} increase during Year 2 in the fair value of listed common shares that {s} holds, without significant influence over the issuer, was reported in other comprehensive income; (3) on December 1, {s} received {m(p['r'])} from a tenant as rent for warehouse space for December through May, Year 3, and credited the whole amount to rent revenue; and (4) cash dividends of {m(p['dv'])} that {s}'s board declared in December were debited to an expense account. What corrected income before income taxes should {s} report for Year 2?""",
        choices, ans,
        f"""(1) Consigned goods remain the consignor's inventory, so ending inventory rises and cost of goods sold falls: + {m(p['k'])}. (2) Fair value changes on equity securities with readily determinable fair values go to net income: + {m(p['g'])}. (3) One month of the six-month rent, {m(mo)}, was earned in Year 2, so {m(5 * mo)} is reclassified to unearned rent: − {m(5 * mo)}. (4) Dividends are distributions to owners, charged to retained earnings, not expenses: + {m(p['dv'])}. Corrected income before income taxes = {m(p['P'])} + {m(p['k'])} + {m(p['g'])} − {m(5 * mo)} + {m(p['dv'])} = {m(key_v)}.""",
    )


def sce_retained_earnings(p):
    co, s = p["co"], short(p["co"])
    ppa = whole(D(p["e"]) * D("0.75"))
    sh = whole(D(p["S"]) * p["pct"] / 100)
    sd = sh * p["mp"]
    tsr = p["tc"] - p["tp"] - p["ats"]
    assert tsr > 0 and p["fv"] > p["cl"]
    key_v = p["R0"] + ppa + p["N"] - p["Dc"] - p["fv"] - sd - tsr
    pool = {
        "prop_cv": (m(key_v + p["fv"] - p["cl"]), f"Charges retained earnings with the land's {m(p['cl'])} carrying amount. A property dividend is recorded at the fair value of the asset distributed, {m(p['fv'])}; the {m(p['fv'] - p['cl'])} gain on remeasuring the land is already in net income."),
        "sd_par": (m(key_v + sd - sh), f"Charges retained earnings with only the $1 par value of the {n(sh)} shares distributed, {m(sh)}. A {p['pct']}% stock dividend is a small stock dividend, recorded at the shares' market price: {n(sh)} × ${p['mp']} = {m(sd)}."),
        "ppa_pre": (m(key_v + p["e"] - ppa), f"Adds the whole {m(p['e'])} pretax overstatement to opening retained earnings. Correcting it also raises Year 1 income tax expense, so the prior-period adjustment is {m(p['e'])} × 75% = {m(ppa)}."),
        "ts_all": (m(key_v - p["ats"]), f"Charges the whole {m(p['tc'] - p['tp'])} shortfall on the treasury shares to retained earnings. It is charged first against the {m(p['ats'])} of paid-in capital from treasury stock transactions; only the remaining {m(tsr)} reduces retained earnings."),
        "paid": (m(key_v + p["Dc"] - p["paid"]), f"Deducts only the {m(p['paid'])} of cash dividends paid. Retained earnings is reduced when dividends are declared, {m(p['Dc'])}; the unpaid {m(p['Dc'] - p['paid'])} is a liability."),
    }
    key = (m(key_v), f"Correct. {m(p['R0'])} + {m(ppa)} + {m(p['N'])} − {m(p['Dc'])} − {m(p['fv'])} − {m(sd)} − {m(tsr)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s Year 2 statement of changes in stockholders' equity begins with retained earnings of {m(p['R0'])} at January 1, as previously reported. In Year 2, {s} found that a computational error had overstated its Year 1 depreciation expense by {m(p['e'])}; its income tax rate is 25% for all years. Year 2 net income, correctly computed and including the gain on the land distribution described below, was {m(p['N'])}. During Year 2, the board declared cash dividends of {m(p['Dc'])}, of which {m(p['paid'])} had been paid by December 31; distributed to shareholders land that {s} held as an investment, which had a carrying amount of {m(p['cl'])} and a fair value of {m(p['fv'])} on the distribution date; and declared and distributed a {p['pct']}% stock dividend on its {n(p['S'])} outstanding $1 par common shares when their market price was ${p['mp']} per share. {s} accounts for treasury stock by the cost method. It also reissued treasury shares that had cost {m(p['tc'])} for {m(p['tp'])}; before that sale, its paid-in capital from treasury stock transactions had a balance of {m(p['ats'])}. What retained earnings should {s} report at December 31, Year 2?""",
        choices, ans,
        f"""Opening retained earnings are restated for the error, net of tax: {m(p['R0'])} + {m(p['e'])} × 75% = {m(p['R0'] + ppa)}. Add net income ({m(p['N'])}, which already includes the gain on remeasuring the land). Deduct dividends when declared: cash {m(p['Dc'])}; the property dividend at the land's fair value, {m(p['fv'])}; and the small ({p['pct']}%) stock dividend at market price, {n(sh)} shares × ${p['mp']} = {m(sd)}. The {m(p['tc'] - p['tp'])} shortfall on the treasury shares is charged first to the {m(p['ats'])} of paid-in capital from treasury stock, and the remaining {m(tsr)} to retained earnings. Retained earnings at December 31 = {m(key_v)}.""",
    )


def sce_total_adjust(p):
    co, s = p["co"], short(p["co"])
    key_v = p["Td"] - p["D"] - p["T"]
    pool = {
        "no_div": (m(key_v + p["D"]), f"Leaves out the {m(p['D'])} dividend. A cash dividend reduces retained earnings, and creates a liability, when it is declared."),
        "no_ts": (m(key_v + p["T"]), f"Leaves the {m(p['T'])} buyback as an investment. A company's own reacquired shares are treasury stock, a deduction from stockholders' equity, not an asset."),
        "afs_nib": (m(key_v + p["L"]), f"Adds the {m(p['L'])} loss back to net income without recording it in other comprehensive income. The loss moves from net income to OCI, so total equity doesn't change."),
        "afs_dbl": (m(key_v - p["L"]), f"Records the {m(p['L'])} loss in other comprehensive income but leaves it in net income as well, counting it twice. Moving it from net income to OCI leaves total equity unchanged."),
        "ic_nib": (m(key_v + p["ic"]), f"Adds the {m(p['ic'])} of issue costs back to net income without reducing additional paid-in capital. Issue costs reduce the proceeds credited to paid-in capital, so moving them out of expense leaves total equity unchanged."),
        "ic_dbl": (m(key_v - p["ic"]), f"Reduces additional paid-in capital by the {m(p['ic'])} of issue costs but leaves them in expense too, counting them twice."),
    }
    key = (m(key_v), f"Correct. {m(p['Td'])} − {m(p['D'])} − {m(p['T'])}; the other two corrections move amounts between components of equity.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft statement of changes in stockholders' equity reports total stockholders' equity of {m(p['Td'])} at December 31, Year 2. The controller identifies these errors: (1) a cash dividend of {m(p['D'])}, declared on December 14 and payable January 12, Year 3, has not been recorded; (2) the {m(p['T'])} that {s} paid in October to buy back some of its own common shares, which it holds as treasury stock, was debited to an investment account reported among its assets; (3) an unrealized holding loss of {m(p['L'])} on available-for-sale debt securities, none of it a credit loss, was reported in net income; and (4) {m(p['ic'])} of legal and underwriting costs of issuing new common shares in March was charged to general and administrative expense. Ignore income taxes. What total stockholders' equity should the corrected statement report at December 31, Year 2?""",
        choices, ans,
        f"""Two corrections reduce total equity: the declared dividend (− {m(p['D'])} of retained earnings, with a dividend payable) and the treasury shares, which are a deduction from equity rather than an asset (− {m(p['T'])}). The other two only move amounts between components: the {m(p['L'])} unrealized loss moves from net income (retained earnings) to accumulated other comprehensive income, and the {m(p['ic'])} of issue costs moves from expense (retained earnings) to a reduction of additional paid-in capital. Corrected total stockholders' equity = {m(p['Td'])} − {m(p['D'])} − {m(p['T'])} = {m(key_v)}.""",
    )


def scf_operating_adjust(p):
    co, s = p["co"], short(p["co"])
    key_v = p["O"] - p["g"] - 2 * p["a"] - 2 * p["p"] + p["dv"]
    assert key_v > 0
    pool = {
        "ar_once": (m(key_v + p["a"]), f"Removes the {m(p['a'])} that the draft added for receivables but doesn't deduct the increase. An increase in receivables means cash collected was less than revenue, so it is subtracted: the correction is 2 × {m(p['a'])}."),
        "prem_once": (m(key_v + p["p"]), f"Removes the {m(p['p'])} add-back but doesn't deduct the premium amortization. Amortizing a premium makes interest expense less than the interest paid in cash, so it is subtracted from net income: the correction is 2 × {m(p['p'])}."),
        "div_keep": (m(key_v - p["dv"]), f"Leaves the {m(p['dv'])} of dividends paid in operating activities. Under U.S. GAAP, dividends paid are a financing outflow."),
        "gain_skip": (m(key_v + p["g"]), f"Leaves the {m(p['g'])} gain in operating activities. The gain is part of the sale proceeds reported in investing activities, so it is deducted from net income."),
    }
    key = (m(key_v), f"Correct. {m(p['O'])} − {m(p['g'])} − 2 × {m(p['a'])} − 2 × {m(p['p'])} + {m(p['dv'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 statement of cash flows, prepared by the indirect method, reports net cash provided by operating activities of {m(p['O'])}. The controller identifies these errors in the operating section: (1) net income includes a {m(p['g'])} gain on the sale of equipment, which the draft doesn't adjust for (the {m(p['pr'])} of proceeds is correctly reported in investing activities); (2) accounts receivable increased by {m(p['a'])} during Year 2, and the draft adds the increase to net income; (3) the draft adds back {m(p['p'])} of amortization of the premium on {s}'s bonds payable as a noncash expense; and (4) the draft deducts the {m(p['dv'])} of dividends that {s} paid to its shareholders. {s} follows U.S. GAAP. What net cash provided by operating activities should the corrected statement report?""",
        choices, ans,
        f"""(1) The gain is deducted, because the whole sale price is an investing inflow: − {m(p['g'])}. (2) The increase in receivables should have been subtracted; reversing the addition and subtracting it: − 2 × {m(p['a'])}. (3) Premium amortization reduces interest expense below the cash paid, so it is subtracted, not added: − 2 × {m(p['p'])}. (4) Dividends paid are a financing outflow under ASC 230, so they come out of operating activities: + {m(p['dv'])}. Corrected net cash provided by operating activities = {m(p['O'])} − {m(p['g'])} − {m(2 * p['a'])} − {m(2 * p['p'])} + {m(p['dv'])} = {m(key_v)}.""",
    )


def consol_current_assets(p):
    par, sub = p["par"], p["sub"]
    ps, ss = short(par), short(sub)
    assert p["X"] % 20 == 0
    u = p["X"] // 4
    key_v = p["CAd"] - p["r"] + p["X"] - u - p["dv"]
    pool = {
        "inv_none": (m(key_v - (p["X"] - u)), f"Leaves the draft's elimination of the whole {m(p['X'])}. Only the unrealized profit, {m(p['X'])} × 25% = {m(u)}, is eliminated; the goods stay in consolidated inventory at {ss}'s cost, {m(p['X'] - u)}."),
        "inv_full": (m(key_v + u), f"Restores the full {m(p['X'])} without eliminating any profit. {ss}'s {m(u)} profit on goods still held by the group is unrealized and is removed."),
        "u_markup": (m(key_v + u - p["X"] // 5), f"Treats the 25% gross margin as a markup on cost, eliminating {m(p['X'])} × 25/125 = {m(p['X'] // 5)}. The margin is 25% of the selling price, so the unrealized profit is {m(u)}."),
        "no_r": (m(key_v + p["r"]), f"Leaves the {m(p['r'])} intercompany receivable in consolidated current assets. Amounts the group owes itself are eliminated."),
        "no_div": (m(key_v + p["dv"]), f"Leaves the {m(p['dv'])} dividend receivable from {ss}. A dividend declared by a wholly owned subsidiary is owed within the group, so the receivable is eliminated against {ss}'s dividend payable."),
    }
    key = (m(key_v), f"Correct. {m(p['CAd'])} − {m(p['r'])} + ({m(p['X'])} − {m(u)}) − {m(p['dv'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{par} owns all of the common stock of {sub}, which it formed in Year 1. {ss} sells goods to {ps} at a gross margin of 25% of the selling price. {ps}'s draft December 31, Year 2, consolidated balance sheet reports total current assets of {m(p['CAd'])}. The controller identifies these errors: (1) {ss}'s {m(p['r'])} trade receivable from {ps} for goods sold in December, and {ps}'s matching payable, were not eliminated; (2) {ps}'s December 31 inventory includes goods it bought from {ss} for {m(p['X'])}, and the draft eliminated the whole {m(p['X'])} from consolidated inventory; and (3) a dividend of {m(p['dv'])} that {ss} declared on December 20, payable January 10, Year 3, is included in {ps}'s dividends receivable. What total current assets should the corrected consolidated balance sheet report?""",
        choices, ans,
        f"""(1) The intercompany receivable is eliminated with the matching payable: − {m(p['r'])}. (2) Goods bought within the group stay in consolidated inventory at the selling affiliate's cost; only the unrealized profit is eliminated. {ss}'s profit is 25% of the {m(p['X'])} price, {m(u)}, so the draft's {m(p['X'])} elimination is reversed and {m(u)} eliminated: + {m(p['X'] - u)}. (3) The dividend receivable from the subsidiary is eliminated against its dividend payable: − {m(p['dv'])}. Corrected current assets = {m(p['CAd'])} − {m(p['r'])} + {m(p['X'] - u)} − {m(p['dv'])} = {m(key_v)}.""",
    )


def notes_lease_maturity(p):
    co, s = p["co"], short(p["co"])
    k = D(p["rate"]) / 100
    lpv = rd(sum(D(p["pw"]) / (1 + k) ** t for t in range(1, p["nw"] + 1)))
    und_w = p["nw"] * p["pw"]
    rem = 59 * p["q"]
    Ud = p["ot"] + p["s"] + lpv + p["v"]
    key_v = p["ot"] + und_w + rem
    pool = {
        "pv_keep": (m(key_v - und_w + lpv), f"Keeps the warehouse lease at its {m(lpv)} present value. The maturity analysis shows undiscounted payments, {p['nw']} × {m(p['pw'])} = {m(und_w)}, and then reconciles them to the discounted lease liabilities."),
        "sixty": (m(key_v + p["q"]), f"Includes all 60 store payments, {m(60 * p['q'])}. The December 1 payment has been made, so 59 payments of {m(p['q'])}, {m(rem)}, remain."),
        "st_keep": (m(key_v + p["s"]), f"Keeps the {m(p['s'])} of payments on the ten-month lease. Under the short-term lease election no lease liability is recognized for it, so it is left out of the maturity analysis of lease liabilities."),
        "var_keep": (m(key_v + p["v"]), f"Keeps the {m(p['v'])} of sales-based rent. Variable payments that depend on sales are not lease payments, so they are excluded from the lease liability and its maturity analysis."),
        "omit_new": (m(key_v - rem), f"Leaves out the store lease. It began on December 1, so its 59 remaining payments, {m(rem)}, are part of the lease liabilities at year-end."),
    }
    key = (m(key_v), f"Correct. {m(Ud)} − {m(p['s'])} − {m(lpv)} + {m(und_w)} + {m(rem)} − {m(p['v'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft notes to its December 31, Year 1, financial statements include a maturity analysis of its operating lease liabilities, which reports total undiscounted lease payments of {m(Ud)}. The controller identifies these errors and omissions: (1) the total includes {m(p['s'])} of remaining payments on a ten-month equipment lease that began in September, Year 1, for which {s} made the short-term lease election; (2) for its warehouse lease, which requires {p['nw']} more annual payments of {m(p['pw'])} each December 31, the analysis lists the warehouse lease liability of {m(lpv)} instead of the payments; (3) the analysis omits a store lease, classified as an operating lease, that began on December 1, Year 1, with 60 monthly payments of {m(p['q'])}, the first paid on December 1; and (4) the total includes {m(p['v'])} of estimated Year 2 rent that the store lease bases on a percentage of the store's sales. What total undiscounted lease payments should the corrected maturity analysis report?""",
        choices, ans,
        f"""The maturity analysis of lease liabilities shows the undiscounted lease payments behind the recognized liabilities. (1) Leases under the short-term lease election have no lease liability, so their payments come out: − {m(p['s'])}. (2) The warehouse lease belongs at its undiscounted payments, {p['nw']} × {m(p['pw'])} = {m(und_w)}, not its {m(lpv)} present value. (3) The store lease commenced on December 1, so its 59 remaining payments are added: 59 × {m(p['q'])} = {m(rem)}. (4) Variable payments based on sales are not lease payments: − {m(p['v'])}. Corrected total = {m(Ud)} − {m(p['s'])} − {m(lpv)} + {m(und_w)} + {m(rem)} − {m(p['v'])} = {m(key_v)}.""",
    )


def nfp_with_restrictions_adjust(p):
    org, s = p["org"], short(p["org"])
    key_v = p["W"] + p["fv"] - p["dc"] - p["a"] + p["pl"] - p["sp"]
    pool = {
        "land_cost": (m(key_v - (p["fv"] - p["dc"])), f"Leaves the land at the donor's {m(p['dc'])} cost. Contributed assets are recognized at fair value on the date of the gift, {m(p['fv'])}, so net assets with donor restrictions rise by {m(p['fv'] - p['dc'])}."),
        "agent": (m(key_v + p["a"]), f"Keeps the {m(p['a'])} for the animal shelter in net assets. {s} received it as an agent for a beneficiary the donor named, with no power to redirect it, so it is a liability, not a contribution."),
        "pledge": (m(key_v - p["pl"]), f"Leaves the {m(p['pl'])} pledge in net assets without donor restrictions. A pledge payable in a later period carries an implied time restriction, so it is with donor restrictions until that period."),
        "release": (m(key_v + p["sp"]), f"Doesn't record the {m(p['sp'])} release. Spending the gifts on the camp program met the donor's purpose restriction, so they move to net assets without donor restrictions."),
        "land_wo": (m(key_v - p["fv"]), f"Moves the land to net assets without donor restrictions, at its {m(p['fv'])} fair value. The donor's requirement that the land be used forever as a preserve is a restriction that never expires, so the gift stays in net assets with donor restrictions."),
    }
    key = (m(key_v), f"Correct. {m(p['W'])} + ({m(p['fv'])} − {m(p['dc'])}) − {m(p['a'])} + {m(p['pl'])} − {m(p['sp'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, reports net assets with donor restrictions of {m(p['W'])} in its draft December 31, Year 2, statement of financial position. The controller identifies these errors: (1) land that a donor gave in May, requiring that it be used forever as a nature preserve, was recorded as a contribution with donor restrictions at the donor's original cost of {m(p['dc'])}; its fair value on the date of the gift was {m(p['fv'])}; (2) {m(p['a'])} that a donor gave {s} in November to pass on to a named animal shelter, which {s} has no power to redirect, was recorded as a contribution with donor restrictions; (3) an unconditional pledge of {m(p['pl'])}, payable in Year 3 with no purpose stated, was recorded as contribution revenue without donor restrictions; and (4) {m(p['sp'])} of gifts that donors made in Year 1, restricted to a summer camp program, was spent on the program in Year 2, but no release from restrictions was recorded. What net assets with donor restrictions should the corrected statement report?""",
        choices, ans,
        f"""(1) The land is a contribution with a perpetual donor restriction, measured at its fair value on the date of the gift: + ({m(p['fv'])} − {m(p['dc'])}). (2) Cash received for a beneficiary the donor specified, with no variance power, is a liability of an agent, not a contribution: − {m(p['a'])}. (3) An unconditional pledge payable in a later period carries an implied time restriction: + {m(p['pl'])}. (4) Spending the camp gifts on the camp met the purpose restriction, so they are released: − {m(p['sp'])}. Corrected net assets with donor restrictions = {m(key_v)}.""",
    )


def nfp_total_expenses(p):
    org, s = p["org"], short(p["org"])
    assert p["bt"] % (2 * p["nl"]) == 0
    dep = p["bt"] // (2 * p["nl"])
    key_v = p["E"] + p["cs"] - p["f"] - p["bt"] + dep
    pool = {
        "vol": (m(key_v + p["vv"]), f"Adds the {m(p['vv'])} of phone-bank volunteers' time. Contributed services are recognized only if they create or enhance a nonfinancial asset or need specialized skills that would otherwise be bought; staffing a phone bank does neither."),
        "fees": (m(key_v + p["f"]), f"Leaves the {m(p['f'])} of external investment management fees in expenses. An NFP reports investment return net of external and direct internal investment expenses, so the fees are netted against the return."),
        "no_dep": (m(key_v - dep), f"Removes the {m(p['bt'])} van from expenses without recording depreciation. The van was in service for six months of Year 2, so {m(p['bt'])} ÷ {p['nl']} × 6/12 = {m(dep)} of depreciation is an expense."),
        "truck": (m(key_v + p["bt"] - dep), f"Leaves the {m(p['bt'])} cost of the van in program expenses. A van is a long-lived asset: it is capitalized, and only the Year 2 depreciation of {m(dep)} is an expense."),
        "cs_none": (m(key_v - p["cs"]), f"Leaves out the {m(p['cs'])} of donated accounting services. They need specialized skills and would otherwise have been bought, so they are recognized as contribution revenue and as an expense."),
    }
    key = (m(key_v), f"Correct. {m(p['E'])} + {m(p['cs'])} − {m(p['f'])} − {m(p['bt'])} + {m(dep)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, reports total expenses of {m(p['E'])} in its draft Year 2 statement of activities. Reviewing the draft, the controller notes: (1) an accounting firm prepared {s}'s grant reports at no charge, work {s} would otherwise have had to pay for, with a fair value of {m(p['cs'])}, and nothing was recorded; (2) {m(p['f'])} of fees paid to an outside firm for managing {s}'s investment portfolio is reported in management and general expenses, and investment return is reported before those fees; (3) a delivery van bought for {m(p['bt'])} on July 1, Year 2, was charged to program expenses; the van has a {p['nl']}-year useful life and no residual value, and {s} depreciates vans straight-line by month; and (4) volunteers without special skills who staffed a fundraising phone bank gave time valued at {m(p['vv'])}, and nothing was recorded. What total expenses should {s}'s corrected statement of activities report?""",
        choices, ans,
        f"""(1) Donated services that need specialized skills and would otherwise be bought are recognized as revenue and expense: + {m(p['cs'])}. (2) Investment return is reported net of external investment expenses (ASC 958-225-45-14), so the fees come out of expenses: − {m(p['f'])}. (3) The van is capitalized, and six months of depreciation are expensed: − {m(p['bt'])} + {m(dep)}. (4) The phone-bank volunteers' time needs no specialized skills, so it is correctly not recognized. Corrected total expenses = {m(p['E'])} + {m(p['cs'])} − {m(p['f'])} − {m(p['bt'])} + {m(dep)} = {m(key_v)}.""",
    )


def modified_cash_assets(p):
    co, s = p["co"], short(p["co"])
    cash = p["c0"] + p["rc"] - p["pe"] - p["eq"] + p["b"] - p["rp"] - p["dr"]
    cost = p["E0"] + p["eq"]
    ad = p["AD0"] + p["dep"]
    key_v = cash + cost - ad
    facts = [cash, cost, ad, cost - ad, key_v] + [p[k] for k in ("c0", "rc", "pe", "pi", "eq", "b", "rp", "dr", "E0", "AD0", "dep", "ar", "w")]
    assert cash > 0 and len(set(facts)) == len(facts), f"two facts share an amount: {facts}"
    pool = {
        "ar": (m(key_v + p["ar"]), f"Includes the {m(p['ar'])} that clients owe. Revenue is recorded when cash is collected, and {s}'s only modification is for equipment, so receivables are not recognized."),
        "eq_cash": (m(key_v + p["eq"]), f"Doesn't deduct the {m(p['eq'])} paid for equipment from cash, so the purchase is counted in both cash and equipment. Cash at year-end is {m(cash)}."),
        "gross": (m(key_v + ad), f"Reports the equipment at its {m(cost)} cost. Under {s}'s modification, equipment is depreciated, so it is reported net of {m(ad)} of accumulated depreciation."),
        "no_eq": (m(key_v - (cost - ad)), f"Leaves the equipment out, as the pure cash basis would. {s}'s modification capitalizes equipment, so it is an asset at {m(cost)} − {m(ad)} = {m(cost - ad)}."),
        "eq_exp": (m(key_v - p["eq"]), f"Treats the {m(p['eq'])} of equipment bought in March as an expense, leaving it out of equipment. Under {s}'s modification, equipment purchases are capitalized."),
        "prepaid": (m(key_v + p["pi"]), f"Reports the {m(p['pi'])} paid for Year 3 insurance as a prepaid asset. Prepaid expenses are an accrual-basis item outside {s}'s one modification, so the payment is an expense when paid."),
    }
    key = (m(key_v), f"Correct. Cash {m(p['c0'])} + {m(p['rc'])} − {m(p['pe'])} − {m(p['eq'])} + {m(p['b'])} − {m(p['rp'])} − {m(p['dr'])} = {m(cash)}; equipment {m(cost)} − {m(ad)} = {m(cost - ad)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a partnership, prepares its financial statements on a modified cash basis: the only departure from the pure cash basis is that it capitalizes the equipment it buys and depreciates it. At January 1, Year 2, it had cash of {m(p['c0'])} and equipment that had cost {m(p['E0'])}, with accumulated depreciation of {m(p['AD0'])}. During Year 2, it collected {m(p['rc'])} from clients; paid {m(p['pe'])} of operating expenses, including {m(p['pi'])} paid in December for insurance coverage in Year 3; paid {m(p['eq'])} for new equipment in March; borrowed {m(p['b'])} from a bank and repaid {m(p['rp'])} of the principal; and the partners withdrew {m(p['dr'])}. Depreciation for Year 2 on all of the equipment is {m(p['dep'])}. At December 31, clients owed {s} {m(p['ar'])} for services performed in Year 2, and {s} owed employees {m(p['w'])} of wages. What total assets should {s} report in its December 31, Year 2, statement of assets, liabilities, and equity—modified cash basis?""",
        choices, ans,
        f"""On this modified cash basis the assets are cash and equipment, net of depreciation. Cash = {m(p['c0'])} + {m(p['rc'])} collected − {m(p['pe'])} operating payments (the Year 3 insurance included) − {m(p['eq'])} equipment + {m(p['b'])} borrowed − {m(p['rp'])} repaid − {m(p['dr'])} withdrawn = {m(cash)}. Equipment = {m(cost)} cost − {m(ad)} accumulated depreciation = {m(cost - ad)}. Receivables, prepaid insurance and unpaid wages are accrual items that {s}'s one modification doesn't cover. Total assets = {m(key_v)}.""",
    )


# ── Area II Application ──────────────────────────────────────────────────


def cash_equivalents(p):
    co, s = p["co"], short(p["co"])
    key_v = p["ck"] + p["mm"] + p["cp"] + p["pc"]
    pool = {
        "cd": (m(key_v + p["cd"]), f"Includes the {m(p['cd'])} certificate of deposit because it matures within three months of year-end. The test is the maturity when {s} bought it; it had six months to run, so it is a short-term investment."),
        "pd": (m(key_v + p["pd"]), f"Includes the {m(p['pd'])} postdated check. A check dated after year-end can't be deposited until then, so it is a receivable."),
        "nsf": (m(key_v + p["nsf"]), f"Includes the {m(p['nsf'])} check returned NSF. A returned check is a claim against the customer, a receivable."),
        "ta": (m(key_v + p["ta"]), f"Includes the {m(p['ta'])} of travel advances, which are receivables from employees (or prepaid expenses), not cash."),
        "cp_out": (m(key_v - p["cp"]), f"Leaves out the {m(p['cp'])} of commercial paper. It had three months to maturity when {s} bought it, so it is a cash equivalent."),
        "mm_out": (m(key_v - p["mm"]), f"Leaves out the {m(p['mm'])} money market fund, which is redeemable on demand at a fixed $1 a share and is a cash equivalent."),
    }
    key = (m(key_v), f"Correct. {m(p['ck'])} + {m(p['mm'])} + {m(p['cp'])} + {m(p['pc'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, Year 1, {co}'s records show: a checking account balance of {m(p['ck'])}; shares of a money market fund, redeemable on demand at $1 per share, {m(p['mm'])}; commercial paper bought on November 15, Year 1, that matures on February 15, Year 2, {m(p['cp'])}; a six-month certificate of deposit bought on September 1, Year 1, that matures on February 28, Year 2, {m(p['cd'])}; a customer's check dated January 10, Year 2, received in December, {m(p['pd'])}; a customer's check that the bank returned in December marked NSF, {m(p['nsf'])}; travel advances to employees, {m(p['ta'])}; and petty cash, {m(p['pc'])}. {s} treats as cash equivalents all investments that meet the GAAP definition of a cash equivalent. What amount should {s} report as cash and cash equivalents?""",
        choices, ans,
        f"""Cash includes the checking balance ({m(p['ck'])}) and petty cash ({m(p['pc'])}). Cash equivalents are short-term, highly liquid investments with an original maturity, to the holder, of three months or less: the money market fund ({m(p['mm'])}) and the three-month commercial paper ({m(p['cp'])}). The certificate of deposit had six months to run when bought, so it is a short-term investment even though it now matures within three months. The postdated check, the NSF check and the travel advances are receivables. Total = {m(key_v)}.""",
    )


def hfs_carrying(p):
    co, s, a = p["co"], short(p["co"]), p["asset"]
    assert p["d"] % 12 == 0
    mo = p["mo"]
    cv0 = p["C"] - p["AD0"] - p["d"] * mo // 12
    f0, f1, f2 = (p[k] - p["cts"] for k in ("F0", "F1", "F2"))
    assert f1 < f0 < cv0 < f2
    left = 9 - mo
    key_v = cv0
    pool = {
        "no_cap": (m(f2), f"Writes the {a} up to its {m(f2)} fair value less cost to sell. A later increase is recognized as a gain only up to the losses previously recognized, so the carrying amount can't exceed {m(cv0)}, its carrying amount when it was classified as held for sale."),
        "fv": (m(p["F2"]), f"Reports the {a} at its {m(p['F2'])} fair value. An asset held for sale is measured at the lower of its carrying amount and fair value less cost to sell, and any write-up is limited to the losses recognized earlier."),
        "keep_low": (m(f1), f"Keeps the {a} at its June 30 fair value less cost to sell, {m(p['F1'])} − {m(p['cts'])}. The increase in the third quarter is recognized as a gain, up to the {m(cv0 - f1)} of losses recognized earlier."),
        "dep_cont": (m(cv0 - p["d"] * left // 12), f"Keeps depreciating the {a} after it was classified as held for sale: {m(cv0)} − {m(p['d'])} × {left}/12. A long-lived asset isn't depreciated while it is classified as held for sale."),
        "no_dep_pre": (m(p["C"] - p["AD0"]), f"Leaves out depreciation for the {mo} months before {p['cd']}: {m(p['C'])} − {m(p['AD0'])}. Depreciation continues until the asset is classified as held for sale."),
    }
    key = (m(key_v), f"Correct. {m(p['C'])} − {m(p['AD0'])} − {m(p['d'])} × {mo}/12 = {m(cv0)}; the September 30 fair value less cost to sell ({m(f2)}) exceeds it, so the write-up stops at {m(cv0)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} prepares quarterly financial statements. On {p['cd']}, Year 1, its board approved selling a {a} that {s} had been using; {s} vacated it that day and listed it with a broker at a price close to its fair value. The {a} had cost {m(p['C'])}, its accumulated depreciation was {m(p['AD0'])} at January 1, Year 1, and {s} depreciates it straight-line at {m(p['d'])} a year. Its fair value was {m(p['F0'])} on {p['cd']}, {m(p['F1'])} at June 30 and {m(p['F2'])} at September 30, and the estimated costs to sell were {m(p['cts'])} throughout. The {a} was still unsold at September 30, and {s} expects to sell it by March, Year 2. At what amount should {s} report the {a} in its September 30, Year 1, balance sheet?""",
        choices, ans,
        f"""Depreciation stops when the {a} is classified as held for sale on {p['cd']}: carrying amount = {m(p['C'])} − {m(p['AD0'])} − {m(p['d'])} × {mo}/12 = {m(cv0)}. It is then measured at the lower of that amount and fair value less cost to sell: {m(f0)} on {p['cd']} (a loss of {m(cv0 - f0)}) and {m(f1)} at June 30 (a further loss of {m(f0 - f1)}). At September 30, fair value less cost to sell is {m(f2)}. A gain is recognized for the increase, but only up to the {m(cv0 - f1)} of losses recognized earlier (ASC 360-10-35-40), so the {a} is reported at {m(cv0)}.""",
    )


def fv_investments_carrying(p):
    co, s = p["co"], short(p["co"])
    i1, i4 = p["i1"], p["i4"]
    eqm = p["c4"] + p["s4"] - p["dv4"]
    assert p["el"] < p["a2"] - p["f2"]
    key_v = p["f1"] + p["f2"] + p["f3"] + p["f4"]
    pool = {
        "allow": (m(key_v - p["el"]), f"Deducts the {m(p['el'])} credit loss allowance from the debt securities' {m(p['f2'])} fair value. Debt securities that may be sold before maturity are reported at fair value; the allowance and the unrealized loss in OCI together bridge amortized cost ({m(p['a2'])}) to fair value."),
        "amort": (m(key_v - p["f2"] + p["a2"] - p["el"]), f"Reports the debt securities at amortized cost less the allowance, {m(p['a2'])} − {m(p['el'])}. Debt securities that may be sold before maturity are reported at fair value."),
        "eqm": (m(key_v - p["f4"] + eqm), f"Reports the {short(i4)} shares by the equity method, {m(p['c4'])} + {m(p['s4'])} − {m(p['dv4'])} = {m(eqm)}. {s} elected the fair value option for this investment, so it is reported at fair value."),
        "cost1": (m(key_v - p["f1"] + p["c1"]), f"Reports the {short(i1)} shares at their {m(p['c1'])} cost. Equity securities with readily determinable fair values are measured at fair value, with changes in net income."),
    }
    key = (m(key_v), f"Correct. {m(p['f1'])} + {m(p['f2'])} + {m(p['f3'])} + {m(p['f4'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, Year 2, {co} holds these investments, all bought during Year 2: 4% of the common shares of {i1}, a listed company, which cost {m(p['c1'])} and are worth {m(p['f1'])}; debt securities that {s} holds to collect interest but may sell if it needs cash or interest rates change, with an amortized cost of {m(p['a2'])} and a fair value of {m(p['f2'])}, on which {s} estimates an expected credit loss of {m(p['el'])} and which it neither intends to sell nor is likely to be required to sell before recovery; corporate bonds that its trading desk bought in December to resell within weeks, which cost {m(p['c3'])} and are worth {m(p['f3'])}; and 25% of the common shares of {i4}, a listed company over which {s} has significant influence, for which {s} elected the fair value option when it bought them for {m(p['c4'])}. {s}'s share of {short(i4)}'s net income since then is {m(p['s4'])}, {s} has received dividends of {m(p['dv4'])} from it, and the shares are worth {m(p['f4'])}. What total carrying amount should {s} report for these investments?""",
        choices, ans,
        f"""All four are carried at fair value. The listed shares ({m(p['f1'])}) are equity securities with readily determinable fair values. The debt securities that may be sold are available for sale, reported at fair value ({m(p['f2'])}); the {m(p['el'])} credit loss is recorded through an allowance and net income, and the rest of the decline below amortized cost is in OCI, but the balance sheet amount is fair value. The bonds held for resale within weeks are trading securities at fair value ({m(p['f3'])}). The {short(i4)} shares would otherwise be under the equity method, but {s} elected the fair value option, so they are at fair value ({m(p['f4'])}). Total = {m(key_v)}.""",
    )


def bond_schedule(F, c, y, n_):
    """Annual-coupon bond: price and the amortized cost at each year-end (effective interest, whole dollars)."""
    cpn = rd(D(F) * D(c) / 100)
    yy = D(y) / 100
    price = rd(sum(cpn / (1 + yy) ** t for t in range(1, n_ + 1)) + D(F) / (1 + yy) ** n_)
    ac, out = price, []
    for _ in range(n_):
        inc = rd(ac * yy)
        ac = ac + inc - cpn
        out.append((inc, inc - cpn, ac))
    return cpn, price, out


def afs_oci_entry(p):
    co, s = p["co"], short(p["co"])
    cpn, P, sched = bond_schedule(p["F"], p["c"], p["y"], p["n"])
    (i1, am1, ac1), (i2, am2, ac2) = sched[0], sched[1]
    gap1, gap2 = p["fv1"] - ac1, p["fv2"] - ac2
    assert P < p["F"] and gap1 < 0 < gap2
    key_v = gap2 - gap1
    slam = rd((p["F"] - P) / D(p["n"]))
    sl = (p["fv2"] - (P + 2 * slam)) - (p["fv1"] - (P + slam))
    pool = {
        "no_amort": (m(p["fv2"] - p["fv1"]), f"Takes the {m(p['fv2'])} − {m(p['fv1'])} change in fair value. The amortized cost also rose in Year 2, by the {m(am2)} of discount amortized, so OCI records only the change in the gap between fair value and amortized cost."),
        "no_prior": (m(gap2), f"Records only the {m(gap2)} by which fair value exceeds amortized cost at December 31, Year 2 ({m(p['fv2'])} − {m(ac2)}), without reversing the {m(-gap1)} unrealized loss recorded in OCI for Year 1. The entry moves the fair value adjustment from a {m(-gap1)} credit balance to a {m(gap2)} debit balance."),
        "vs_cost": (m(p["fv2"] - P), f"Compares the December 31, Year 2, fair value with the {m(P)} purchase price. The comparison is with amortized cost, {m(ac2)}, and the Year 1 loss already in OCI is reversed."),
        "loss_only": (m(-gap1), f"Reverses the {m(-gap1)} Year 1 unrealized loss but records none of the {m(gap2)} by which fair value exceeds amortized cost at December 31, Year 2."),
        "sl": (m(sl), f"Amortizes the discount straight-line, {m(slam)} a year, giving amortized cost of {m(P + slam)} and {m(P + 2 * slam)}. {s} uses the effective interest method."),
    }
    key = (m(key_v), f"Correct. ({m(p['fv2'])} − {m(ac2)}) − ({m(p['fv1'])} − {m(ac1)}) = {m(gap2)} + {m(-gap1)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} paid {m(P)} for {m(p['F'])} face amount of {p['n']}-year, {p['c']}% bonds that pay interest each December 31; the price gives a yield of {p['y']}%. {s} classifies the bonds as available for sale and amortizes the discount by the effective interest method, rounding to the nearest dollar. It does not intend to sell the bonds and is not likely to be required to sell them before they recover in value, and it expects to collect all of their contractual cash flows. The bonds' fair value was {m(p['fv1'])} at December 31, Year 1, and {m(p['fv2'])} at December 31, Year 2. In its December 31, Year 2, entry to adjust the bonds to fair value, what amount should {s} credit to other comprehensive income?""",
        choices, ans,
        f"""Amortized cost: Year 1 interest income {m(P)} × {p['y']}% = {m(i1)}, less the {m(cpn)} coupon, amortizes {m(am1)}, so amortized cost is {m(ac1)}; Year 2 interest income {m(ac1)} × {p['y']}% = {m(i2)} amortizes {m(am2)}, giving {m(ac2)}. At December 31, Year 1, fair value was {m(-gap1)} below amortized cost, an unrealized loss in OCI. At December 31, Year 2, it is {m(gap2)} above. The Year 2 entry moves the fair value adjustment by {m(gap2)} + {m(-gap1)} = {m(key_v)}, debiting the adjustment account and crediting OCI (an unrealized holding gain).""",
    )


# ── Area III Analysis: accounting changes and error corrections ─────────


def principle_change_re(p):
    co, s = p["co"], short(p["co"])
    t = D("0.75")
    d1, d2 = p["f1"] - p["l1"], p["f2"] - p["l2"]
    a1, au, a2 = whole(d1 * t), whole(p["u"] * t), whole(d2 * t)
    key_v = p["R"] + a1 - au
    pool = {
        "y2diff": (m(p["R"] + a2 - au), f"Uses the inventory difference at December 31, Year 2, {m(d2)} × 75%. The adjustment to January 1, Year 2, retained earnings is the cumulative effect on periods before Year 2, measured by the difference at December 31, Year 1."),
        "pretax": (m(p["R"] + d1 - p["u"]), f"Adjusts by the pretax amounts, + {m(d1)} − {m(p['u'])}. Each effect also changes income taxes, so retained earnings change by 75% of each."),
        "no_u": (m(p["R"] + a1), f"Leaves out the repairs invoice on the view that the error counterbalanced. It did, but only by the end of Year 2: at January 1, Year 2, Year 1 income was still overstated by {m(p['u'])} before tax, so opening retained earnings fall by {m(au)}."),
        "prosp": (m(p["R"] - au), f"Applies the change in inventory method prospectively, from Year 3. A change in accounting principle is applied retrospectively when its period-specific effects can be determined, so the earliest period presented carries the {m(a1)} cumulative effect."),
        "u_sign": (m(p["R"] + a1 + au), f"Adds the {m(au)} after-tax repairs correction. The unrecorded Year 1 repairs overstated Year 1 income, so retained earnings are reduced."),
    }
    key = (m(key_v), f"Correct. {m(p['R'])} + {m(d1)} × 75% − {m(p['u'])} × 75%.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""In Year 3, {co} changes its inventory method from LIFO to FIFO because FIFO better matches its flow of goods, and it can determine the effect on every prior period. Its inventories were: December 31, Year 1, LIFO {m(p['l1'])} and FIFO {m(p['f1'])}; December 31, Year 2, LIFO {m(p['l2'])} and FIFO {m(p['f2'])}. Also in Year 3, {s} found that a {m(p['u'])} invoice for repairs made in December, Year 1, had never been accrued; {s} paid it in January, Year 2, and charged it to Year 2 repairs expense. {s}'s retained earnings at January 1, Year 2, as originally reported, were {m(p['R'])}. Its income tax rate is 25% for all years and all effects. In its comparative financial statements for Years 2 and 3, what retained earnings should {s} report at January 1, Year 2, as adjusted?""",
        choices, ans,
        f"""The change to FIFO is applied retrospectively: the Years 2 and 3 statements are presented on FIFO, and the cumulative effect on periods before Year 2 adjusts retained earnings at January 1, Year 2. That effect is the higher Year 1 ending inventory under FIFO, {m(d1)}, net of tax: + {m(a1)}. The repairs error is corrected by restatement: Year 1 income was overstated by {m(p['u'])} (Year 2 income understated by the same amount, so the error had counterbalanced only by December 31, Year 2), so January 1, Year 2, retained earnings fall by {m(au)} after tax. Adjusted retained earnings = {m(p['R'])} + {m(a1)} − {m(au)} = {m(key_v)}.""",
    )


def estimate_change_income(p):
    co, s = p["co"], short(p["co"])
    d_old = whole(D(p["C"] - p["R0"]) / p["L0"])
    cv = p["C"] - 2 * d_old
    d_new = rd(D(cv - p["R1"]) / p["L1"])
    key_v = p["Pd"] + d_old - d_new + p["cm"] + p["tr"]
    dep_c = d_new + 2 * (d_new - d_old)
    d_cost = rd(D(p["C"] - p["R1"]) / p["L1"])
    pool = {
        "catchup": (m(key_v + d_new - dep_c), f"Applies the revised annual depreciation of {m(d_new)} to Years 1 and 2 as well and charges the catch-up to Year 3: {m(d_new)} + 2 × ({m(d_new)} − {m(d_old)}) = {m(dep_c)} of Year 3 depreciation. A change in estimate is applied prospectively, with no catch-up: Year 3 depreciation is {m(d_new)}."),
        "cost_basis": (m(key_v + d_new - d_cost), f"Spreads the machine's full cost less the new residual value over the {p['L1']} remaining years: ({m(p['C'])} − {m(p['R1'])}) ÷ {p['L1']} = {m(d_cost)}. What remains to be depreciated is the {m(cv)} carrying amount at January 1, Year 3, less the residual value."),
        "keep_cm": (m(key_v - p["cm"]), f"Leaves the {m(p['cm'])} of commissions in Year 3 expense. They were earned on Year 2 sales, so correcting the error charges them to Year 2 (through opening retained earnings), not Year 3."),
        "keep_tr": (m(key_v - p["tr"]), f"Leaves the {m(p['tr'])} of Year 1 truck depreciation in Year 3. A prior-period error is corrected by adjusting opening retained earnings, not through current income."),
        "old_dep": (m(key_v - d_old + d_new), f"Keeps depreciating the machine on the original estimates, {m(d_old)} a year. The revised life and residual value apply from Year 3 onward."),
    }
    key = (m(key_v), f"Correct. {m(p['Pd'])} + {m(d_old)} − {m(d_new)} + {m(p['cm'])} + {m(p['tr'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} bought a machine on January 1, Year 1, for {m(p['C'])} and depreciated it straight-line over {p['L0']} years with a residual value of {m(p['R0'])}. On January 1, Year 3, after an engineering study, {s} concluded that the machine will last {p['L1']} more years and have a residual value of {m(p['R1'])}. {s}'s draft Year 3 income statement reports income before income taxes of {m(p['Pd'])}. The supporting records show that the draft (1) records Year 3 depreciation on the machine on the original estimates; (2) includes in Year 3 sales commission expense {m(p['cm'])} of commissions that sales staff earned on December, Year 2, sales, which were not accrued at December 31, Year 2, and were paid in January, Year 3; and (3) includes in Year 3 depreciation expense {m(p['tr'])} of Year 1 depreciation on a delivery truck that was never recorded in Year 1 (the truck's Year 3 depreciation is recorded correctly). {s}'s Year 2 statements have been issued, it presents single-year statements, and both errors are material. Ignore income taxes. What corrected income before income taxes should {s} report for Year 3?""",
        choices, ans,
        f"""The revised life and residual value are a change in estimate, applied prospectively. Carrying amount at January 1, Year 3 = {m(p['C'])} − 2 × {m(d_old)} = {m(cv)}; Year 3 depreciation = ({m(cv)} − {m(p['R1'])}) ÷ {p['L1']} = {m(d_new)}, replacing the {m(d_old)} in the draft. The unaccrued commissions and the omitted Year 1 depreciation are prior-period errors: they are corrected by adjusting retained earnings at January 1, Year 3, so both come out of Year 3 expense. Corrected income before income taxes = {m(p['Pd'])} + {m(d_old)} − {m(d_new)} + {m(p['cm'])} + {m(p['tr'])} = {m(key_v)}.""",
    )


def bond_discount_equity(p):
    co, s = p["co"], short(p["co"])
    cpn, P, sched = bond_schedule(p["F"], p["c"], p["y"], p["n"])
    am1, am2 = sched[0][1], sched[1][1]
    tot = am1 + am2
    key_v = p["S"] - tot
    slam = rd((p["F"] - P) / D(p["n"]))
    pool = {
        "inv": (m(key_v + p["iu"]), f"Corrects the Year 1 inventory error, raising equity by {m(p['iu'])}. The understated Year 1 ending inventory was Year 2's beginning inventory, so Year 2 income was overstated by the same amount, and the error had reversed by December 31, Year 2."),
        "git": (m(key_v + p["g"]), f"Adds the {m(p['g'])} of goods in transit to Year 2 inventory without also recording the purchase, raising equity by {m(p['g'])}. Both the purchase and the inventory were left out, so Year 2 cost of goods sold and equity are unaffected."),
        "sl": (m(p["S"] - 2 * slam), f"Amortizes the discount straight-line, {m(slam)} a year, so equity falls by {m(2 * slam)}. {s} uses the effective interest method: {m(am1)} in Year 1 and {m(am2)} in Year 2."),
        "one_year": (m(p["S"] - am2), f"Corrects only Year 2's {m(am2)} of amortization. The discount should have been amortized in Year 1 too, so the cumulative {m(tot)} is corrected at December 31, Year 2."),
        "all_disc": (m(p["S"] - (p["F"] - P)), f"Charges the whole {m(p['F'] - P)} discount against equity. Only the {m(tot)} that the effective interest method amortizes in Years 1 and 2 is interest expense of those years; the rest is amortized over the remaining {p['n'] - 2} years."),
    }
    key = (m(key_v), f"Correct. {m(p['S'])} − ({m(am1)} + {m(am2)}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} issued {m(p['F'])} face amount of {p['n']}-year, {p['c']}% bonds, with interest paid each December 31, for {m(P)}, a price that gives a yield of {p['y']}%. In Year 3, before its Year 3 statements are issued, {s} finds that it has recorded interest expense equal to the cash paid each year and has never amortized the discount. It also finds that goods costing {m(p['g'])}, bought on December 29, Year 2, FOB shipping point and in transit at year-end, were recorded as a purchase and as inventory only when they arrived on January 4, Year 3; and that its December 31, Year 1, inventory had been understated by {m(p['iu'])} because of a counting error. {s} presents comparative statements for Years 2 and 3; its December 31, Year 2, total stockholders' equity, as originally reported, was {m(p['S'])}. {s} uses the effective interest method, rounded to the nearest dollar. Ignore income taxes. What total stockholders' equity should {s} report at December 31, Year 2, in its comparative balance sheet?""",
        choices, ans,
        f"""Discount amortization omitted: Year 1, {m(P)} × {p['y']}% − {m(cpn)} = {m(am1)}; Year 2, {m(P + am1)} × {p['y']}% − {m(cpn)} = {m(am2)}; in all {m(tot)} of extra interest expense, which lowers retained earnings, and so equity, at December 31, Year 2 (and raises bonds payable). The goods in transit were left out of both purchases and ending inventory, so Year 2 cost of goods sold and equity are unaffected (the correction adds the inventory and an account payable). The Year 1 inventory error counterbalanced in Year 2. Restated equity = {m(p['S'])} − {m(tot)} = {m(key_v)}.""",
    )


def restated_cogs(p):
    co, s = p["co"], short(p["co"])
    key_v = p["Cd"] - p["P"] + p["C"] + p["F"] - p["G"]
    pool = {
        "a_none": (m(key_v + p["P"]), f"Treats the late-recorded purchase as a Year 1 error only. Recording the {m(p['P'])} purchase in Year 2 overstated Year 2 purchases, and so Year 2 cost of goods sold."),
        "a_sign": (m(key_v + 2 * p["P"]), f"Adds the {m(p['P'])} purchase to Year 2 cost of goods sold. It was already recorded in Year 2 purchases, wrongly; the correction removes it."),
        "b_sign": (m(key_v - 2 * p["C"]), f"Deducts the {m(p['C'])} of consigned goods from cost of goods sold. They belong to the supplier, so removing them lowers ending inventory and raises cost of goods sold."),
        "c_none": (m(key_v - p["F"]), f"Leaves the {m(p['F'])} of freight on purchases in delivery expense. Freight-in is part of the cost of inventory, and the goods were sold in Year 2, so it belongs in cost of goods sold."),
        "d_none": (m(key_v + p["G"]), f"Leaves the {m(p['G'])} shipment out of inventory. Goods shipped FOB destination remain {s}'s until delivered, so they belong in December 31, Year 2, inventory, which lowers cost of goods sold."),
    }
    key = (m(key_v), f"Correct. {m(p['Cd'])} − {m(p['P'])} + {m(p['C'])} + {m(p['F'])} − {m(p['G'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} uses a periodic inventory system. Its Year 2 income statement, already issued, reported cost of goods sold of {m(p['Cd'])}. While preparing its Year 3 statements, {s} finds: goods costing {m(p['P'])} that arrived on December 28, Year 1, and were included in the December 31, Year 1, count were recorded as a purchase when the supplier's invoice arrived on January 6, Year 2; the December 31, Year 2, count included goods costing {m(p['C'])} that a supplier had shipped to {s} on consignment; {m(p['F'])} of freight paid on Year 2 purchases of merchandise was charged to delivery expense, and all of those goods were sold in Year 2; and goods costing {m(p['G'])} that {s} shipped to a customer on December 30, Year 2, FOB destination, which arrived on January 3, Year 3, were recorded as a Year 2 sale and left out of the Year 2 count. What cost of goods sold should {s} report for Year 2 in its comparative statements for Years 2 and 3?""",
        choices, ans,
        f"""Cost of goods sold = beginning inventory + purchases − ending inventory. The late invoice put a Year 1 purchase into Year 2 purchases: − {m(p['P'])} (Year 2's beginning inventory already included the goods). Consigned-in goods belong to the consignor, so ending inventory falls: + {m(p['C'])}. Freight-in is an inventory cost of goods sold in Year 2: + {m(p['F'])}. Goods shipped FOB destination were still {s}'s at year-end, so ending inventory rises: − {m(p['G'])}. Restated cost of goods sold = {m(key_v)}.""",
    )


# ── Area III Analysis: contingencies ─────────────────────────────────────


def draft_litigation(p):
    co, s = p["co"], short(p["co"])
    D_ = p["hi"] + p["B"] + p["Sr"]
    assert p["lo"] < p["M"] < p["hi"]
    key_v = p["M"] + p["T"]
    pool = {
        "hi": (m(p["hi"] + p["T"]), f"Keeps the customer's suit at the top of the range, {m(p['hi'])}. When one amount in the range is a better estimate than any other, that amount, {m(p['M'])}, is accrued; the possible excess is disclosed."),
        "lo": (m(p["lo"] + p["T"]), f"Accrues the bottom of the range, {m(p['lo'])}. The minimum is accrued only when no amount in the range is a better estimate than any other; counsel names {m(p['M'])} as the most likely amount."),
        "B_in": (m(key_v + p["B"]), f"Keeps the {m(p['B'])} accrual for the distributor's suit. Counsel can't predict the outcome, so a loss isn't probable; the suit is disclosed, not accrued."),
        "res_in": (m(key_v + p["Sr"]), f"Keeps the {m(p['Sr'])} reserve for future truck accidents. No accident had happened, so no liability existed at year-end; GAAP doesn't allow general reserves for future losses."),
        "no_T": (m(p["M"]), f"Leaves out the {m(p['T'])} settlement. Once {s} signed the agreement, it owed a fixed amount, which is recognized as a liability."),
    }
    key = (m(key_v), f"Correct. {m(p['M'])} for the customer's suit + {m(p['T'])} for the signed settlement.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year 1, balance sheet, for statements not yet issued, reports a liability for litigation and claims of {m(D_)}, made up of {m(p['hi'])} for a customer's suit over an injury caused by one of {s}'s products, {m(p['B'])} for a former distributor's suit seeking that amount for breach of contract, and a {m(p['Sr'])} reserve for possible future accidents involving {s}'s uninsured delivery trucks. Counsel's letter says counsel expects the jury to find against {s} in the customer's suit and puts the damages at {m(p['lo'])} to {m(p['hi'])}, with {m(p['M'])} the most likely amount; on the distributor's suit, it says the law on the central question is unsettled and counsel can't predict the outcome. {s}'s trucks have had no accidents that haven't been settled. On December 21, {s} signed an agreement to pay a supplier {m(p['T'])} on February 15, Year 2, to settle a dispute over a cancelled order, and {s} has not recorded it; {s} reports amounts owed under settled claims in its liability for litigation and claims. What liability for litigation and claims should the corrected balance sheet report?""",
        choices, ans,
        f"""The customer's suit is a probable loss that can be estimated, and counsel names a most likely amount within the range, so {m(p['M'])} is accrued and the reasonably possible excess up to {m(p['hi'])} is disclosed. The distributor's suit has an outcome counsel can't predict, so it is disclosed but not accrued. A reserve for future accidents isn't a liability: no event had occurred by year-end. The signed settlement is a liability for a fixed amount. Corrected liability = {m(p['M'])} + {m(p['T'])} = {m(key_v)}.""",
    )


def recovery_receivables(p):
    co, s = p["co"], short(p["co"])
    rec = p["Rc"] - p["d"]
    assert rec < p["L"]
    key_v = rec + p["K"]
    pool = {
        "J_in": (m(key_v + p["J"]), f"Includes the {m(p['J'])} jury award. The competitor has appealed, so the award is a gain contingency, which isn't recognized until it is realized or realizable; it may be disclosed."),
        "ded": (m(key_v + p["d"]), f"Records the insurance recovery at the full {m(p['Rc'])} replacement cost, ignoring the {m(p['d'])} deductible that the insurer will withhold."),
        "BI_in": (m(key_v + p["BI"]), f"Includes the {m(p['BI'])} business-interruption claim. The insurer denies coverage, so a recovery isn't probable and no receivable is recognized."),
        "K_out": (m(rec), f"Leaves out the {m(p['K'])} settlement because it is a gain. The supplier's signed agreement makes the amount realizable, so it is no longer a contingency and the receivable is recognized."),
        "no_ins": (m(p["K"]), f"Leaves out the {m(rec)} insurance recovery until the cash arrives. A recovery of a loss already recognized is recorded when it is probable, as it is once the insurer accepts the claim in writing."),
    }
    key = (m(key_v), f"Correct. ({m(p['Rc'])} − {m(p['d'])}) + {m(p['K'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} is preparing its December 31, Year 1, financial statements, which have not been issued. Its files show: (1) a November fire destroyed inventory that had cost {m(p['L'])}, and {s} recognized a {m(p['L'])} loss; in December, its insurer accepted the claim in writing and will pay, in January, the inventory's {m(p['Rc'])} replacement cost less the policy's {m(p['d'])} deductible; (2) in December, a jury awarded {s} {m(p['J'])} in its patent suit against a competitor, which has appealed; (3) on December 18, a former supplier signed an agreement to pay {s} {m(p['K'])} by February 15, Year 2, to settle {s}'s claim over defective materials, and the supplier is financially sound; and (4) {s} has filed a {m(p['BI'])} claim with a different insurer for business lost during the fire, and that insurer says its policy doesn't cover the loss. What total receivables from these matters should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""The insurance recovery on the fire loss is probable, since the insurer has accepted the claim in writing, and it doesn't exceed the {m(p['L'])} loss recognized, so a receivable is recognized for the amount to be paid: {m(p['Rc'])} − {m(p['d'])} = {m(rec)}. The supplier's signed settlement is realizable, so {m(p['K'])} is a receivable. The jury award under appeal is a gain contingency (ASC 450-30), not recognized until realized, and the disputed business-interruption claim isn't probable of recovery. Total receivables = {m(key_v)}.""",
    )


# ── Area III Analysis: subsequent events ─────────────────────────────────


def se_equity_public(p):
    co, s = p["co"], short(p["co"])
    key_v = p["S"] - p["E"] - p["L"]
    pool = {
        "fv": (m(key_v - p["F"]), f"Also deducts the {m(p['F'])} February decline in the securities' fair value. The decline reflects market conditions after year-end, so it is a nonrecognized subsequent event, disclosed if material."),
        "issue": (m(key_v + p["S2"]), f"Adds the {m(p['S2'])} of shares issued on March 2. Shares issued after year-end don't change the December 31 balance sheet; the issuance is disclosed."),
        "div": (m(key_v - p["Dv"]), f"Deducts the {m(p['Dv'])} dividend declared on February 10. A dividend is recognized when it is declared, which was after year-end."),
        "no_emb": (m(key_v + p["E"]), f"Leaves out the {m(p['E'])} theft. The cash was already gone at December 31, so its discovery is evidence about conditions at year-end and is recognized."),
        "no_inv": (m(key_v + p["L"]), f"Leaves out the {m(p['L'])} engineering invoice. The work was done in December, so the expense and the liability belong in Year 1."),
    }
    key = (m(key_v), f"Correct. {m(p['S'])} − {m(p['E'])} − {m(p['L'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a public company that files with the SEC, will issue its December 31, Year 1, financial statements on March 9, Year 2. Its draft balance sheet reports total stockholders' equity of {m(p['S'])}. After year-end: on January 14, internal auditors found that a cashier had stolen {m(p['E'])} from {s} from October through December, Year 1, hiding the thefts in the cash records, and {s} has no insurance or other way to recover the money; on February 2, {s} received an engineering firm's invoice for {m(p['L'])} for work done in December, Year 1, which {s} had not accrued; on February 10, the board declared a cash dividend of {m(p['Dv'])}, payable March 31; during February, a broad market decline cut the fair value of {s}'s portfolio of listed equity securities by {m(p['F'])}; and on March 2, {s} issued common shares for {m(p['S2'])} in cash. Ignore income taxes. What total stockholders' equity should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""An SEC filer evaluates subsequent events through the date its statements are issued. The theft and the December engineering work existed at year-end, so they are recognized subsequent events: cash falls by {m(p['E'])}, and an expense and a liability of {m(p['L'])} are recorded, each reducing equity. The dividend declaration, the February market decline and the March share issuance arise from events after year-end; they are disclosed if material but not recognized. Equity = {m(p['S'])} − {m(p['E'])} − {m(p['L'])} = {m(key_v)}.""",
    )


def se_pretax_private(p):
    co, s = p["co"], short(p["co"])
    key_v = p["P"] - p["B"] - p["R"]
    assert p["Sx"] > p["A"]
    pool = {
        "settle": (m(key_v - (p["Sx"] - p["A"])), f"Also deducts the {m(p['Sx'] - p['A'])} by which the April 15 settlement exceeded the accrual. A company that isn't an SEC filer evaluates subsequent events through the date its statements are available to be issued, April 6, so the settlement isn't reflected in these statements."),
        "acq": (m(key_v - p["c"]), f"Deducts the {m(p['c'])} of acquisition fees. They were incurred in Year 2 on a deal agreed after year-end; the acquisition is disclosed, not recognized."),
        "no_recall": (m(key_v + p["R"]), f"Leaves out the recall. The design flaw existed when the cookers were sold in Year 1, so the order is evidence about conditions at year-end, and the {m(p['R'])} cost is accrued in Year 1."),
        "no_bill": (m(key_v + p["B"]), f"Leaves the duplicate {m(p['B'])} sale in Year 1 revenue. The error existed at year-end and was found before the statements were available to be issued, so it is corrected."),
        "settle_full": (m(key_v - p["Sx"]), f"Charges the whole {m(p['Sx'])} April 15 settlement to Year 1 on top of the {m(p['A'])} already accrued. The settlement came after April 6, the date the statements were available to be issued, so these statements reflect only the {m(p['A'])} accrual made at year-end."),
    }
    key = (m(key_v), f"Correct. {m(p['P'])} − {m(p['B'])} − {m(p['R'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a private company that is not an SEC filer, had its December 31, Year 1, financial statements available to be issued on April 6, Year 2, and delivered them to its bank on April 24. Its draft Year 1 income before income taxes is {m(p['P'])}. After year-end: on January 19, {s} found that a December, Year 1, shipment to a customer had been billed and recorded as a sale twice, overstating Year 1 sales by {m(p['B'])}; on February 9, a regulator ordered a recall of a pressure cooker model that {s} sold in Year 1, because of a design flaw present when the cookers were sold, and {s} estimates the recall will cost {m(p['R'])}, none of which it has accrued; in March, {s} agreed to buy a competitor and incurred {m(p['c'])} of legal and advisory fees on the deal; and on April 15, {s} settled a former distributor's Year 1 claim for {m(p['Sx'])}, against the {m(p['A'])} it had accrued at December 31. What income before income taxes should {s} report for Year 1?""",
        choices, ans,
        f"""A company that is not an SEC filer evaluates subsequent events through the date the statements are available to be issued, April 6. Before that date, the duplicate billing and the recall reveal conditions that existed at year-end (the sale was recorded twice; the flaw was in cookers already sold), so both are recognized: − {m(p['B'])} and − {m(p['R'])}. The March acquisition is a nonrecognized event, and its fees are a Year 2 expense. The April 15 settlement came after the statements were available to be issued, so it isn't reflected in them. Income before income taxes = {m(p['P'])} − {m(p['B'])} − {m(p['R'])} = {m(key_v)}.""",
    )


def se_deferred_tax(p):
    co, s = p["co"], short(p["co"])
    t, t2 = D("0.25"), D("0.21")
    base = p["TD"] + p["dpm"] - p["Sx"]
    key_v = whole(base * t)
    assert key_v > 0 and p["Sx"] > p["La"]
    pool = {
        "rate": (m(rd(base * t2)), f"Measures the deferred taxes at the new 21% rate. Deferred taxes use the tax law enacted at the balance sheet date; the effect of a rate change enacted after year-end is recognized when it is enacted, in Year 2, and disclosed."),
        "gross": (m(whole((p["TD"] + p["dpm"]) * t)), f"Reports the deferred tax liability, ({m(p['TD'])} + {m(p['dpm'])}) × 25%, without offsetting the {m(whole(p['Sx'] * t))} deferred tax asset from the lawsuit. Deferred tax liabilities and assets of one tax jurisdiction are offset and presented as one net amount."),
        "no_dep": (m(whole((p["TD"] - p["Sx"]) * t)), f"Leaves the duplicate {m(p['dpm'])} of depreciation in place. Reversing it raises the assets' carrying amount, so the taxable temporary difference rises to {m(p['TD'] + p['dpm'])}."),
        "no_settle": (m(whole((p["TD"] + p["dpm"] - p["La"]) * t)), f"Keeps the lawsuit's deductible temporary difference at the {m(p['La'])} accrued. The settlement is evidence that the liability at year-end was {m(p['Sx'])}, so the accrual and the deductible difference rise to {m(p['Sx'])}."),
        "dep_sign": (m(whole((p["TD"] - p["dpm"] - p["Sx"]) * t)), f"Deducts the {m(p['dpm'])} from the taxable difference. Removing duplicate book depreciation raises the carrying amount further above the tax basis, so the difference grows."),
    }
    key = (m(key_v), f"Correct. ({m(p['TD'])} + {m(p['dpm'])} − {m(p['Sx'])}) × 25%.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a public company, will issue its December 31, Year 1, financial statements on March 8, Year 2. At December 31, its only temporary differences are the {m(p['TD'])} by which the carrying amount of its depreciable assets exceeds their tax basis, and an accrued liability of {m(p['La'])} for a customer's lawsuit over a Year 1 incident, which will be deductible for tax when paid. Under the tax law enacted at December 31, the tax rate for all future years is 25%, and {s} expects enough future taxable income to realize any deferred tax asset. Before the statements are issued: on January 20, {s} finds that Year 1 book depreciation of {m(p['dpm'])} on a machine placed in service in Year 1 had been recorded twice (the machine's tax depreciation was deducted correctly); on February 4, it settles the lawsuit for {m(p['Sx'])}, payable in April; and on February 25, the legislature enacts a law cutting the rate to 21% for years after Year 1. All of {s}'s deferred taxes are in one tax jurisdiction. What net deferred tax liability should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""The duplicate depreciation and the settlement are recognized subsequent events: reversing the duplicate raises the machine's book carrying amount at year-end, so the taxable difference rises to {m(p['TD'] + p['dpm'])}, and the settlement shows the lawsuit liability, and so the deductible difference, was {m(p['Sx'])}. The rate change was enacted after year-end, so deferred taxes at December 31 stay at the 25% rate enacted then (ASC 740-10-25-47); the change is recognized in Year 2. Net deferred tax liability = ({m(p['TD'] + p['dpm'])} − {m(p['Sx'])}) × 25% = {m(key_v)}.""",
    )


# ── Families ─────────────────────────────────────────────────────────────

P_BS = dict(co="Achnasheen Supply Co.", CA=1846000, CL=968000, i=14400, d=36000, c=125000, o=22500, t=58000, due="June 30", use=["od_liab", "ts_keep", "cpltd"])
P_IS = dict(co="Balmacara Outfitting Co.", P=946000, k=38500, g=27000, r=54000, dv=120000, use=["div", "oci", "cons_sign"])
P_RE = dict(co="Plockton Corp.", R0=3410000, e=96000, N=692000, Dc=240000, paid=180000, cl=95000, fv=160000, S=400000, pct=5, mp=18, tc=84000, tp=61000, ats=15000, use=["prop_cv", "ts_all", "sd_par"])
P_TE = dict(co="Kyleakin Corp.", Td=4286000, D=95000, T=148000, L=36000, ic=22000, use=["afs_dbl", "ic_dbl", "no_ts"])
P_CF = dict(co="Applecross Co.", O=1128000, g=46000, pr=131000, a=74000, p=18000, dv=210000, use=["prem_once", "ar_once", "gain_skip"])
P_CS = dict(par="Lochcarron Corp.", sub="Shieldaig Ltd.", CAd=2964000, r=98000, X=160000, dv=35000, use=["inv_full", "inv_none", "no_r"])
P_NT = dict(co="Torridon Retail Co.", ot=612000, s=27000, nw=4, pw=120000, rate=6, q=6500, v=18000, use=["pv_keep", "sixty", "omit_new"])
P_NF = dict(org="Gairloch Wildlife Trust", W=2145000, dc=40000, fv=310000, a=75000, pl=90000, sp=62000, use=["agent", "land_cost", "pledge"])
P_NE = dict(org="Poolewe Food Pantry", E=1864000, cs=24000, f=17500, bt=60000, nl=5, vv=31000, use=["fees", "vol", "no_dep"])
P_MC = dict(co="Lochinver Design Partners", c0=48000, rc=612000, pe=438000, pi=9600, eq=72000, b=50000, rp=12000, dr=95000, E0=196000, AD0=71000, dep=27000, ar=41000, w=8500, use=["ar", "prepaid", "eq_cash"])
P_CE = dict(co="Durness Freight Co.", ck=186400, mm=75000, cp=50000, cd=40000, pd=6200, nsf=3450, ta=4800, pc=1500, use=["cd", "pd", "nsf"])
P_HF = dict(co="Bettyhill Printing Co.", asset="warehouse", C=1200000, AD0=420000, d=48000, cd="May 1", mo=4, F0=740000, F1=705000, F2=800000, cts=22000, use=["no_cap", "keep_low", "dep_cont"])
P_FV = dict(co="Helmsdale Corp.", i1="Brora Mills", c1=210000, f1=246000, a2=500000, f2=462000, el=14000, c3=180000, f3=171500, i4="Golspie Foods", c4=1350000, s4=180000, dv4=60000, f4=1412000, use=["allow", "cost1", "eqm"])
P_OC = dict(co="Dornoch Co.", F=500000, c=5, y=6, n=5, fv1=471000, fv2=493000, use=["no_prior", "vs_cost", "loss_only"])
P_PC = dict(co="Alness Hardware Co.", l1=540000, f1=660000, l2=575000, f2=759000, u=36000, R=2760000, use=["no_u", "y2diff", "prosp"])
P_EC = dict(co="Dingwall Fabrication Co.", C=960000, L0=12, R0=60000, L1=6, R1=30000, Pd=1412000, cm=38000, tr=31000, use=["catchup", "keep_cm", "keep_tr"])
P_BD = dict(co="Strathpeffer Corp.", F=2000000, c=6, y=8, n=10, g=36000, iu=52000, S=5480000, use=["inv", "git", "one_year"])
P_CG = dict(co="Beauly Trading Co.", Cd=3846000, P=58000, C=41000, F=27500, G=36000, use=["a_none", "b_sign", "c_none"])
P_DL = dict(co="Kiltarlity Food Co.", lo=250000, hi=600000, M=380000, B=175000, Sr=120000, T=65000, use=["B_in", "res_in", "hi"])
P_RV = dict(co="Fortrose Textile Co.", L=640000, Rc=610000, d=25000, J=900000, K=86000, BI=140000, use=["J_in", "K_out", "no_ins"])
P_SE = dict(co="Glenelg Instruments Inc.", S=6240000, E=86000, L=54000, Dv=180000, F=210000, S2=1500000, use=["fv", "issue", "no_emb"])
P_SP = dict(co="Arisaig Housewares Co.", P=2184000, B=37000, R=148000, c=92000, Sx=260000, A=200000, use=["settle", "acq", "settle_full"])
P_DT = dict(co="Morar Logistics Inc.", TD=1480000, La=160000, dpm=64000, Sx=260000, use=["rate", "no_dep", "dep_sign"])

FAMILIES = [
    # ── Area I Application ──
    ("far-balance-sheet-0009", A1, "Balance sheet", AP,
     ["ASC 210-10-45 (current assets and current liabilities; current maturities of long-term debt)", "ASC 210-20 (offsetting: bank overdrafts at different banks)", "ASC 505-30 (treasury stock is a deduction from equity)", "ASC 606-10-45 (contract liabilities)"],
     bs_working_capital, [
        P_BS,
        sc(P_BS, D("0.72"), dict(CA=2000, CL=2000, i=100, d=1000, c=5000, o=500, t=1000), co="Mallaig Supply Co.", due="April 30", use=["ts_keep", "dep", "cpltd"]),
        sc(P_BS, D("1.35"), dict(CA=2000, CL=2000, i=100, d=1000, c=5000, o=500, t=1000), co="Acharacle Supply Co.", due="September 30", use=["od_liab", "int", "ts_keep"]),
        sc(P_BS, D("0.58"), dict(CA=2000, CL=2000, i=100, d=1000, c=5000, o=500, t=1000), co="Kilchoan Supply Co.", due="March 31", use=["od_liab", "dep", "int"]),
     ], "od_liab"),
    ("far-income-statement-0008", A1, "Income statement", AP,
     ["ASC 220-10 (income statement)", "ASC 606-10-55 (consignment arrangements)", "ASC 321-10-35 (equity securities: changes in fair value in net income)", "ASC 505-20 (dividends are distributions, not expenses)"],
     is_pretax_adjust, [
        P_IS,
        sc(P_IS, D("0.7"), dict(P=1000, k=500, g=1000, r=6000, dv=5000), co="Tobermory Outfitting Co.", use=["rent_none", "cons_sign", "oci"]),
        sc(P_IS, D("1.4"), dict(P=1000, k=500, g=1000, r=6000, dv=5000), co="Craignure Outfitting Co.", use=["div", "cons_sign", "rent_none"]),
        sc(P_IS, D("0.55"), dict(P=1000, k=500, g=1000, r=6000, dv=5000), co="Bunessan Outfitting Co.", use=["oci", "div", "cons_sign"]),
     ], "div"),
    ("far-changes-in-equity-0007", A1, "Statement of changes in equity", AP,
     ["ASC 505-10 (statement of changes in equity)", "ASC 250-10-45-23 (prior-period adjustments)", "ASC 845-10-30 (nonreciprocal transfers to owners measured at fair value)", "ASC 505-20-30 (small stock dividends at fair value)", "ASC 505-30 (treasury stock reissued below cost)"],
     sce_retained_earnings, [
        P_RE,
        sc(P_RE, D("0.75"), dict(R0=10000, e=4000, N=2000, Dc=5000, paid=5000, cl=1000, fv=5000, tc=1000, tp=1000, ats=1000), co="Fionnphort Corp.", S=300000, pct=4, mp=22, use=["sd_par", "paid", "ppa_pre"]),
        sc(P_RE, D("1.3"), dict(R0=10000, e=4000, N=2000, Dc=5000, paid=5000, cl=1000, fv=5000, tc=1000, tp=1000, ats=1000), co="Lismore Corp.", cl=118000, S=500000, pct=6, mp=15, use=["prop_cv", "paid", "ts_all"]),
        sc(P_RE, D("0.6"), dict(R0=10000, e=4000, N=2000, Dc=5000, paid=5000, cl=1000, fv=5000, tc=1000, tp=1000, ats=1000), co="Appin Corp.", S=250000, pct=8, mp=12, use=["ppa_pre", "prop_cv", "sd_par"]),
     ], "prop_cv"),
    ("far-changes-in-equity-0008", A1, "Statement of changes in equity", AP,
     ["ASC 505-10 (equity)", "ASC 505-30 (treasury stock)", "ASC 220-10-45 and ASC 320-10-35 (unrealized holding losses on available-for-sale debt securities in OCI)", "ASC 340-10-S99-1 (SAB Topic 5.A: share issue costs charged against the proceeds)"],
     sce_total_adjust, [
        P_TE,
        sc(P_TE, D("0.7"), dict(Td=1000, D=1000, T=1000, L=1000, ic=1000), co="Ballachulish Corp.", use=["no_div", "afs_nib", "ic_nib"]),
        sc(P_TE, D("1.45"), dict(Td=1000, D=1000, T=1000, L=1000, ic=1000), co="Kinlochleven Corp.", use=["ic_dbl", "afs_dbl", "no_div"]),
        sc(P_TE, D("0.55"), dict(Td=1000, D=1000, T=1000, L=1000, ic=1000), co="Onich Corp.", use=["afs_dbl", "ic_nib", "no_ts"]),
     ], "afs_dbl"),
    ("far-cash-flows-0016", A1, "Statement of cash flows", AP,
     ["ASC 230-10-45-28 (indirect method: adjustments to reconcile net income)", "ASC 230-10-45-15 (financing outflows: dividends paid)", "ASC 835-30-35 (amortization of bond premium)"],
     scf_operating_adjust, [
        P_CF,
        sc(P_CF, D("0.75"), dict(O=1000, g=1000, pr=1000, a=1000, p=1000, dv=5000), co="Corpach Co.", use=["ar_once", "gain_skip", "div_keep"]),
        sc(P_CF, D("1.3"), dict(O=1000, g=1000, pr=1000, a=1000, p=1000, dv=5000), co="Roybridge Co.", dv=270000, use=["prem_once", "gain_skip", "ar_once"]),
        sc(P_CF, D("0.6"), dict(O=1000, g=1000, pr=1000, a=1000, p=1000, dv=5000), co="Laggan Co.", use=["div_keep", "prem_once", "gain_skip"]),
     ], "prem_once"),
    ("far-consolidated-statements-0011", A1, "Consolidated financial statements", AP,
     ["ASC 810-10-45-1 (intra-entity balances and transactions eliminated in full)", "ASC 810-10-45 (consolidation procedures: intra-entity profit in inventory)"],
     consol_current_assets, [
        P_CS,
        sc(P_CS, D("0.7"), dict(CAd=1000, r=1000, X=20000, dv=5000), par="Newtonmore Corp.", sub="Kingussie Ltd.", use=["u_markup", "no_div", "inv_none"]),
        sc(P_CS, D("1.35"), dict(CAd=1000, r=1000, X=20000, dv=5000), par="Carrbridge Corp.", sub="Tomatin Ltd.", use=["inv_full", "no_r", "u_markup"]),
        sc(P_CS, D("0.55"), dict(CAd=1000, r=1000, X=20000, dv=5000), par="Findhorn Corp.", sub="Forres Ltd.", dv=16000, use=["inv_none", "no_div", "no_r"]),
     ], "inv_full"),
    ("far-notes-0008", A1, "Notes to financial statements", AP,
     ["ASC 842-20-50 (lessee disclosures: maturity analysis of lease liabilities)", "ASC 842-20-25-2 (short-term lease election)", "ASC 842-10-30-5 (lease payments exclude variable payments that depend on sales)"],
     notes_lease_maturity, [
        P_NT,
        sc(P_NT, D("0.75"), dict(ot=1000, s=500, pw=1000, q=100, v=500), co="Lossiemouth Retail Co.", nw=5, rate=5, use=["sixty", "st_keep", "var_keep"]),
        sc(P_NT, D("1.3"), dict(ot=1000, s=500, pw=1000, q=100, v=500), co="Portsoy Retail Co.", nw=3, rate=7, use=["pv_keep", "var_keep", "st_keep"]),
        sc(P_NT, D("0.6"), dict(ot=1000, s=500, pw=1000, q=100, v=500), co="Cullen Retail Co.", nw=4, rate=6, use=["omit_new", "pv_keep", "var_keep"]),
     ], "pv_keep"),
    ("far-nfp-financial-position-0005", A1, "Statement of financial position (Not-for-Profit)", AP,
     ["ASC 958-210 (statement of financial position)", "ASC 958-605-30 (contributions measured at fair value)", "ASC 958-605 (transfers to an agent or intermediary for a specified beneficiary are not contributions)", "ASC 958-605-45 (implied time restrictions on promises to give)", "ASC 958-205-45 (releases from donor restrictions)"],
     nfp_with_restrictions_adjust, [
        P_NF,
        sc(P_NF, D("0.7"), dict(W=1000, dc=1000, fv=5000, a=1000, pl=1000, sp=1000), org="Banff Heritage Trust", use=["pledge", "release", "land_wo"]),
        sc(P_NF, D("1.4"), dict(W=1000, dc=1000, fv=5000, a=1000, pl=1000, sp=1000), org="Macduff Nature Society", use=["agent", "land_wo", "release"]),
        sc(P_NF, D("0.55"), dict(W=1000, dc=1000, fv=5000, a=1000, pl=1000, sp=1000), org="Turriff Countryside Fund", use=["land_cost", "agent", "release"]),
     ], "agent"),
    ("far-nfp-statement-of-activities-0004", A1, "Statement of activities (Not-for-Profit)", AP,
     ["ASC 958-225-45-14 (investment return reported net of external and direct internal investment expenses)", "ASC 958-605-25-16 (contributed services)", "ASC 958-360 (property and equipment of NFPs; depreciation)"],
     nfp_total_expenses, [
        P_NE,
        sc(P_NE, D("0.75"), dict(E=1000, cs=1000, f=500, vv=1000), org="Fyvie Meals Network", bt=48000, nl=4, use=["vol", "truck", "fees"]),
        sc(P_NE, D("1.3"), dict(E=1000, cs=1000, f=500, vv=1000), org="Insch Family Shelter", bt=84000, nl=6, use=["fees", "no_dep", "cs_none"]),
        sc(P_NE, D("0.6"), dict(E=1000, cs=1000, f=500, vv=1000), org="Huntly Youth Trust", bt=40000, nl=5, use=["cs_none", "fees", "vol"]),
     ], "fees"),
    ("far-special-purpose-frameworks-0006", A1, "Special Purpose Frameworks", AP,
     ["AICPA special purpose frameworks (cash and modified cash bases; modifications with substantial support)", "AU-C 800 (financial statements prepared under special purpose frameworks: statement titles)"],
     modified_cash_assets, [
        P_MC,
        sc(P_MC, D("0.8"), dict(c0=1000, rc=1000, pe=1000, pi=100, eq=1000, b=5000, rp=1000, dr=1000, E0=5000, AD0=1000, dep=1000, ar=1000, w=500), co="Dufftown Survey Partners", use=["gross", "eq_exp", "prepaid"]),
        sc(P_MC, D("1.25"), dict(c0=1000, rc=1000, pe=1000, pi=100, eq=1000, b=5000, rp=1000, dr=1000, E0=5000, AD0=1000, dep=1000, ar=1000, w=500), co="Aberlour Design Partners", use=["ar", "no_eq", "eq_exp"]),
        sc(P_MC, D("0.65"), dict(c0=1000, rc=1000, pe=1000, pi=100, eq=1000, b=5000, rp=1000, dr=1000, E0=5000, AD0=1000, dep=1000, ar=1000, w=500), co="Tomintoul Survey Partners", dr=60000, dep=20000, use=["eq_cash", "no_eq", "eq_exp"]),
     ], "ar"),
    # ── Area II Application ──
    ("far-cash-equivalents-0002", A2, "Cash and cash equivalents", AP,
     ["ASC 305-10-20 (cash equivalents: original maturity of three months or less to the entity holding the investment)", "ASC 310-10 (receivables)"],
     cash_equivalents, [
        P_CE,
        sc(P_CE, D("0.7"), dict(ck=100, mm=1000, cp=5000, cd=5000, pd=50, nsf=50, ta=100, pc=100), co="Braemar Freight Co.", use=["cp_out", "pd", "mm_out"]),
        sc(P_CE, D("1.4"), dict(ck=100, mm=1000, cp=5000, cd=5000, pd=50, nsf=50, ta=100, pc=100), co="Ballater Freight Co.", use=["cd", "mm_out", "nsf"]),
        sc(P_CE, D("0.55"), dict(ck=100, mm=1000, cp=5000, cd=5000, pd=50, nsf=50, ta=100, pc=100), co="Aboyne Freight Co.", use=["mm_out", "cp_out", "cd"]),
     ], "cd"),
    ("far-ppe-held-for-sale-0004", A2, "Property, plant and equipment", AP,
     ["ASC 360-10-35-43 (asset held for sale measured at the lower of carrying amount and fair value less cost to sell; not depreciated)", "ASC 360-10-35-40 (gain on a later increase in fair value less cost to sell limited to cumulative losses previously recognized)"],
     hfs_carrying, [
        P_HF,
        dict(co="Banchory Printing Co.", asset="workshop", C=840000, AD0=276000, d=36000, cd="April 1", mo=3, F0=548000, F1=521000, F2=592000, cts=17000, use=["fv", "no_cap", "no_dep_pre"]),
        dict(co="Stonehaven Printing Co.", asset="warehouse", C=1560000, AD0=612000, d=60000, cd="March 1", mo=2, F0=902000, F1=861000, F2=985000, cts=26000, use=["keep_low", "dep_cont", "no_cap"]),
        dict(co="Inverbervie Printing Co.", asset="depot", C=660000, AD0=228000, d=24000, cd="June 1", mo=5, F0=405000, F1=382000, F2=451000, cts=14000, use=["keep_low", "no_cap", "fv"]),
     ], "no_cap"),
    ("far-investments-fair-value-0004", A2, "Investments (Financial assets at fair value)", AP,
     ["ASC 321-10-35 (equity securities at fair value)", "ASC 320-10-35 (trading and available-for-sale debt securities at fair value)", "ASC 326-30 (credit losses on available-for-sale debt securities: allowance)", "ASC 825-10-25 (fair value option, including for investments otherwise accounted for by the equity method)"],
     fv_investments_carrying, [
        P_FV,
        sc(P_FV, D("0.7"), dict(c1=1000, f1=1000, a2=10000, f2=1000, el=1000, c3=500, f3=500, c4=10000, s4=1000, dv4=1000, f4=1000), co="Montrose Corp.", i1="Brechin Paper", i4="Edzell Dairies", use=["eqm", "amort", "cost1"]),
        sc(P_FV, D("1.3"), dict(c1=1000, f1=1000, a2=10000, f2=1000, el=1000, c3=500, f3=500, c4=10000, s4=1000, dv4=1000, f4=1000), co="Kirriemuir Corp.", i1="Forfar Textiles", i4="Glamis Brewing", use=["allow", "amort", "cost1"]),
        sc(P_FV, D("0.55"), dict(c1=1000, f1=1000, a2=10000, f2=1000, el=1000, c3=500, f3=500, c4=10000, s4=1000, dv4=1000, f4=1000), co="Alyth Corp.", i1="Blairgowrie Seeds", i4="Dunkeld Timber", use=["allow", "eqm", "amort"]),
     ], "allow"),
    ("far-investments-fair-value-0005", A2, "Investments (Financial assets at fair value)", AP,
     ["ASC 320-10-35-1 (available-for-sale debt securities: unrealized holding gains and losses in OCI)", "ASC 310-20-35 and ASC 835-30-35 (interest method: amortization of discount)"],
     afs_oci_entry, [
        P_OC,
        dict(co="Aberfeldy Co.", F=400000, c=4, y=5, n=6, fv1=372000, fv2=394000, use=["vs_cost", "loss_only", "no_amort"]),
        dict(co="Kenmore Co.", F=800000, c=6, y=7, n=5, fv1=751000, fv2=788000, use=["no_prior", "loss_only", "no_amort"]),
        dict(co="Killin Co.", F=600000, c=7, y=8, n=4, fv1=568000, fv2=596000, use=["no_amort", "no_prior", "loss_only"]),
     ], "no_prior"),
    # ── Area III Analysis: accounting changes and error corrections ──
    ("far-change-in-principle-0002", A3, "Accounting changes and error corrections", AN,
     ["ASC 250-10-45-5 (retrospective application of a change in accounting principle: cumulative effect in opening retained earnings of the earliest period presented)", "ASC 250-10-45-23 (correction of an error in previously issued financial statements)"],
     principle_change_re, [
        P_PC,
        dict(co="Crianlarich Hardware Co.", l1=410000, f1=490000, l2=436000, f2=576000, u=24000, R=2070000, use=["y2diff", "pretax", "u_sign"]),
        dict(co="Tyndrum Hardware Co.", l1=702000, f1=862000, l2=748000, f2=988000, u=48000, R=3590000, use=["no_u", "prosp", "pretax"]),
        dict(co="Dalmally Hardware Co.", l1=324000, f1=388000, l2=345000, f2=457000, u=20000, R=1660000, use=["prosp", "u_sign", "y2diff"]),
     ], "no_u"),
    ("far-change-in-estimate-0002", A3, "Accounting changes and error corrections", AN,
     ["ASC 250-10-45-17 (change in accounting estimate applied prospectively)", "ASC 250-10-45-23 (correction of a prior-period error through opening retained earnings)", "ASC 360-10-35 (depreciation)"],
     estimate_change_income, [
        P_EC,
        dict(co="Taynuilt Fabrication Co.", C=720000, L0=10, R0=40000, L1=5, R1=20000, Pd=1046000, cm=29000, tr=23000, use=["cost_basis", "keep_tr", "catchup"]),
        dict(co="Connel Fabrication Co.", C=1260000, L0=15, R0=60000, L1=8, R1=36000, Pd=1835000, cm=47000, tr=39000, use=["keep_tr", "old_dep", "cost_basis"]),
        dict(co="Benderloch Fabrication Co.", C=540000, L0=8, R0=28000, L1=4, R1=12000, Pd=788000, cm=21000, tr=17000, use=["catchup", "cost_basis", "keep_cm"]),
     ], "catchup"),
    ("far-accounting-errors-0008", A3, "Accounting changes and error corrections", AN,
     ["ASC 250-10-45-23 (correction of an error in previously issued financial statements: restatement)", "ASC 835-30-35-2 (interest method: amortization of discount)", "ASC 330-10 (inventory; goods in transit)"],
     bond_discount_equity, [
        P_BD,
        dict(co="Kilmartin Corp.", F=1500000, c=5, y=7, n=8, g=27000, iu=41000, S=4120000, use=["git", "sl", "all_disc"]),
        dict(co="Crinan Corp.", F=3000000, c=7, y=9, n=10, g=54000, iu=76000, S=8350000, use=["inv", "one_year", "sl"]),
        dict(co="Tayvallich Corp.", F=1000000, c=4, y=6, n=6, g=19000, iu=28000, S=2940000, use=["one_year", "all_disc", "inv"]),
     ], "inv"),
    ("far-accounting-errors-0009", A3, "Accounting changes and error corrections", AN,
     ["ASC 250-10-45-23 (restatement of previously issued financial statements)", "ASC 330-10 (inventory cost, including freight-in)", "ASC 606-10-25-30 (transfer of control: FOB destination)", "ASC 606-10-55 (consignment arrangements)"],
     restated_cogs, [
        P_CG,
        sc(P_CG, D("0.7"), dict(Cd=1000, P=1000, C=1000, F=500, G=1000), co="Tarbert Trading Co.", use=["b_sign", "d_none", "a_sign"]),
        sc(P_CG, D("1.35"), dict(Cd=1000, P=1000, C=1000, F=500, G=1000), co="Carradale Trading Co.", use=["a_none", "c_none", "d_none"]),
        sc(P_CG, D("0.55"), dict(Cd=1000, P=1000, C=1000, F=500, G=1000), co="Campbeltown Trading Co.", use=["c_none", "a_sign", "b_sign"]),
     ], "a_none"),
    # ── Area III Analysis: contingencies ──
    ("far-contingencies-0013", A3, "Contingencies and commitments", AN,
     ["ASC 450-20-25-2 (accrual of loss contingencies)", "ASC 450-20-30-1 (best estimate within a range; minimum when no amount is better)", "ASC 450-20-50 (disclosure of loss contingencies)", "ASC 450-20 (no accrual for general or unspecified business risks)"],
     draft_litigation, [
        P_DL,
        sc(P_DL, D("0.7"), dict(lo=5000, hi=5000, M=5000, B=5000, Sr=5000, T=1000), co="Machrihanish Food Co.", use=["lo", "no_T", "B_in"]),
        sc(P_DL, D("1.4"), dict(lo=5000, hi=5000, M=5000, B=5000, Sr=5000, T=1000), co="Lochgilphead Food Co.", use=["res_in", "hi", "no_T"]),
        sc(P_DL, D("0.55"), dict(lo=5000, hi=5000, M=5000, B=5000, Sr=5000, T=1000), co="Inveraray Food Co.", use=["B_in", "lo", "res_in"]),
     ], "B_in"),
    ("far-contingencies-0014", A3, "Contingencies and commitments", AN,
     ["ASC 450-30-25-1 (gain contingencies not recognized before realization)", "ASC 610-30 (involuntary conversions: insurance recoveries of recognized losses)", "ASC 310-10 (receivables)"],
     recovery_receivables, [
        P_RV,
        sc(P_RV, D("0.7"), dict(L=5000, Rc=5000, d=1000, J=10000, K=1000, BI=5000), co="Strachur Textile Co.", use=["ded", "BI_in", "J_in"]),
        sc(P_RV, D("1.3"), dict(L=5000, Rc=5000, d=1000, J=10000, K=1000, BI=5000), co="Dunoon Textile Co.", use=["J_in", "no_ins", "ded"]),
        sc(P_RV, D("0.6"), dict(L=5000, Rc=5000, d=1000, J=10000, K=1000, BI=5000), co="Rothesay Textile Co.", use=["K_out", "no_ins", "BI_in"]),
     ], "J_in"),
    # ── Area III Analysis: subsequent events ──
    ("far-subsequent-events-0011", A3, "Subsequent events", AN,
     ["ASC 855-10-25-1 and 25-3 (recognized and nonrecognized subsequent events)", "ASC 855-10-55 (examples: events after the balance sheet date that are not recognized)", "ASC 855-10-25-1A (SEC filers evaluate subsequent events through the date the statements are issued)"],
     se_equity_public, [
        P_SE,
        sc(P_SE, D("0.7"), dict(S=10000, E=1000, L=1000, Dv=5000, F=10000, S2=50000), co="Largs Instruments Inc.", use=["no_inv", "div", "issue"]),
        sc(P_SE, D("1.3"), dict(S=10000, E=1000, L=1000, Dv=5000, F=10000, S2=50000), co="Fairlie Instruments Inc.", use=["fv", "no_emb", "div"]),
        sc(P_SE, D("0.55"), dict(S=10000, E=1000, L=1000, Dv=5000, F=10000, S2=50000), co="Millport Instruments Inc.", use=["issue", "fv", "no_inv"]),
     ], "fv"),
    ("far-subsequent-events-0012", A3, "Subsequent events", AN,
     ["ASC 855-10-25-1 and 25-3 (recognized and nonrecognized subsequent events)", "ASC 855-10-25-2 (entities that are not SEC filers evaluate subsequent events through the date the statements are available to be issued)", "ASC 450-20 (loss contingencies: product recalls)"],
     se_pretax_private, [
        P_SP,
        sc(P_SP, D("0.7"), dict(P=1000, B=1000, R=1000, c=1000, Sx=5000, A=5000), co="Brodick Housewares Co.", use=["no_bill", "settle", "no_recall"]),
        sc(P_SP, D("1.35"), dict(P=1000, B=1000, R=1000, c=1000, Sx=5000, A=5000), co="Lamlash Housewares Co.", use=["acq", "no_recall", "no_bill"]),
        sc(P_SP, D("0.6"), dict(P=1000, B=1000, R=1000, c=1000, Sx=5000, A=5000), co="Lochranza Housewares Co.", use=["settle", "settle_full", "no_recall"]),
     ], "settle"),
    ("far-subsequent-events-0013", A3, "Subsequent events", AN,
     ["ASC 855-10-25-1 and 25-3 (recognized and nonrecognized subsequent events)", "ASC 740-10-25-47 and 740-10-35-4 (effects of changes in tax laws or rates recognized at the enactment date)", "ASC 740-10-45-6 (deferred tax liabilities and assets of one jurisdiction offset)"],
     se_deferred_tax, [
        P_DT,
        sc(P_DT, D("0.7"), dict(TD=4000, La=4000, dpm=4000, Sx=4000), co="Kilninver Logistics Inc.", use=["no_settle", "dep_sign", "rate"]),
        sc(P_DT, D("1.3"), dict(TD=4000, La=4000, dpm=4000, Sx=4000), co="Whiting Logistics Inc.", use=["gross", "rate", "no_settle"]),
        sc(P_DT, D("0.6"), dict(TD=4000, La=4000, dpm=4000, Sx=4000), co="Blackwaterfoot Logistics Inc.", use=["rate", "no_dep", "dep_sign"]),
     ], "rate", "U.S. GAAP (ASC 740 and ASC 855) in effect for 2026; tax rates are as stated in the stem"),
]

WORD_ITEMS = [
    mcq("far-ppe-held-for-sale-0003", A2, "Property, plant and equipment", AP,
        ["ASC 360-10-45-9 (criteria for classifying a long-lived asset as held for sale)", "ASC 360-10-55 (implementation guidance: assets not available for immediate sale; actions to complete the plan)"],
        """Strontian Haulage Co. issues its calendar-year financial statements each March. At December 31, Year 1, it is deciding how to classify four long-lived assets that it plans to dispose of. Which one should it classify as held for sale at December 31, Year 1?""",
        [("A depot vacated in November once the board approved its sale; a broker is marketing it near appraised value, and a buyer's letter of intent sets a March closing", "Correct. The board, which has the authority, has committed to the sale; the depot is empty and can be sold as it is; it is being actively marketed at a price close to its value; and a signed letter of intent makes a sale within a year likely. Every condition for held-for-sale classification is met."),
         ("A truck wash that the board approved selling in December, which needs an overhaul, not finished until April, Year 2, before any buyer will consider it", "The truck wash can't be sold in its present condition: the overhaul isn't a usual and customary term of selling such an asset, so it is not available for immediate sale and stays held and used."),
         ("A parts warehouse that a regional manager has proposed selling and is showing to buyers, though only the board, which next meets in February, can approve asset sales", "No one with the authority to approve the sale has committed to a plan. Until the board approves it, the warehouse is held and used, however actively it is shown to buyers."),
         ("A loading crane that the board approved selling in December, which Strontian plans to advertise in Year 3, after a replacement crane is installed", "There is no active program to find a buyer, and the sale isn't expected within a year, so the crane stays held and used.")],
        "A",
        """ASC 360-10-45-9 classifies a long-lived asset as held for sale only when management with the authority to approve the action commits to a plan to sell it; it is available for immediate sale in its present condition, subject only to usual and customary terms; an active program to find a buyer has begun; the sale is probable and expected to be completed within one year; it is being marketed at a reasonable price; and significant changes to the plan are unlikely. The depot meets every condition. The truck wash isn't available for immediate sale because of the overhaul, the warehouse lacks approval by someone with the authority to sell it, and the crane has no active marketing and no expected sale within a year."""),
    mcq("far-contingencies-0012", A3, "Contingencies and commitments", AN,
        ["ASC 450-20-25-2 (accrual of a loss contingency: probable and reasonably estimable)", "ASC 450-20-50 (disclosure when a loss can't be estimated)", "ASC 440-10-50 (unconditional purchase obligations)", "ASC 450-20 (no accrual for uninsured risks before a loss occurs)"],
        """Before issuing its December 31, Year 1, financial statements, Kilchoan Cycle Works reviews documents on four matters: counsel's letter, a purchase contract, insurance records and an engineering report. For which one should Kilchoan accrue a liability at December 31, Year 1?""",
        [("A dealer's $500,000 suit that counsel expects to succeed, though counsel sees no basis yet for estimating the damages, even as a range", "A loss that is probable but can't be reasonably estimated, even as a range, isn't accrued; the suit is disclosed, with a statement that an estimate can't be made."),
         ("A noncancelable order to buy $420,000 of aluminum during Year 2, whose market price has since risen to $455,000", "A firm purchase commitment produces an accrued loss only when the market price falls below the contract price. Here the price has risen, so there is no loss; the commitment may be disclosed."),
         ("Engineers' finding of a brake defect in bicycles sold in Year 1, which Kilchoan has begun to recall, with repairs estimated at $310,000", "Correct. The defect existed in bicycles already sold, so the obligation arose in Year 1; Kilchoan has started the recall, making the cost probable, and has estimated it. Both conditions for accrual are met."),
         ("Its uninsured showroom, which hasn't been damaged, though an actuary puts its expected annual storm losses at $90,000", "No storm damage had occurred by year-end, so there is no liability. GAAP doesn't permit accruing a reserve for future losses on uninsured risks.")],
        "C",
        """A loss contingency is accrued only when information available before the statements are issued shows it is probable that a liability had been incurred at the balance sheet date and the amount can be reasonably estimated (ASC 450-20-25-2). The brake defect existed in bicycles sold in Year 1, Kilchoan has begun a recall, and engineers have estimated the cost, so both conditions are met. The dealer's suit fails the estimation condition and is disclosed. The aluminum contract would produce a loss only if the market price fell below the contract price. Exposure to uninsured future storms isn't a liability until a loss occurs."""),
]


def blind_files(items, scratch):
    """Stems and lettered choices only, for the blind verifier, plus a separate key file."""
    lines, keys = ["# FAR batch 12: blind verification input", "",
                   "Each block is one version of a question. Solve each independently; choose one letter.", ""], {}
    for it in items:
        for k, v in enumerate([it] + list(it.get("variants") or [])):
            label = f"{it['id']} v{k}"
            lines += [f"## {label}", "", v["stem"], ""]
            lines += [f"{c['id']}. {c['text']}" for c in v["choices"]] + [""]
            keys[label] = v["answer"]
    with open(os.path.join(scratch, "b12-blind.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(scratch, "b12-keys.json"), "w", encoding="utf-8", newline="\n") as f:
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
        blind_files(items, SCRATCH)


if __name__ == "__main__":
    main()
