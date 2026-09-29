"""FAR variants 03: three extra versions for the 9 remaining numeric items from FAR batch 04.

Method as in far-variants-02.py, with the shared helpers in variants.py: parameter set 0 must rebuild the
reviewed item word for word; each family has a pool of named-error distractors and each version shows three
(`use`), so the key's letter moves between versions.

Run: python3 scripts/batches/far-variants-03.py   See docs/reviews/far-variants-03.md.
"""
import os
from decimal import Decimal as D

from common import variant
from variants import WORDS, dollars_in, m, n, pick, rd, run, whole

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def fu(x):
    return f"{m(abs(x))} {'favorable' if x > 0 else 'unfavorable'}"


def FU(x):
    return "F" if x > 0 else "U"


# ── Area I ───────────────────────────────────────────────────────────────


def flexible_budget(p):
    co, bu, br, bv, bf, au, ar, av, af = (p[k] for k in ("co", "bu", "br", "bv", "bf", "au", "ar", "av", "af"))
    short = co.split()[0]
    price, vc = D(br) / bu, D(bv) / bu
    cm = whole(price - vc)
    boi, aoi = br - bv - bf, ar - av - af
    flex = whole(au * cm - bf)
    fv, sv, vol = aoi - flex, aoi - boi, flex - boi
    rv, vv, fxv = whole(ar - au * price), whole(au * vc - av), bf - af
    assert 0 not in (fv, rv, vv, fxv, vol) and rv + vv + fxv == fv
    more = "more" if au > bu else "fewer"
    pool = {
        "wrong_dir": (fu(-fv), f"Gets the amount right but the direction wrong. Actual operating income is {'below' if fv < 0 else 'above'} the flexible budget."),
        "static": (fu(sv), f"Compares actual results with the static budget. That static-budget variance mixes the effect of selling {more} units with the flexible-budget variance."),
        "volume": (fu(vol), f"Computes the sales-volume variance: {n(abs(au - bu))} {'extra' if au > bu else 'fewer'} units × the {m(cm)} budgeted contribution margin."),
        "rev_only": (fu(rv), f"Compares only actual revenue with flexible-budget revenue ({m(au * price)}). The flexible-budget variance for operating income includes the cost variances too."),
    }
    key = (fu(fv), f"Correct. The flexible budget for {n(au)} units is {n(au)} × {m(cm)} − {m(bf)} = {m(flex)}; actual operating income of {m(aoi)} is {m(abs(fv))} {'lower' if fv < 0 else 'higher'}.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: (dollars_in(c[0]), c[0]))
    return variant(
        f"""{co}'s static budget for Year 1 was based on {n(bu)} units: revenue {m(br)}, variable costs {m(bv)}, and fixed costs {m(bf)}, for operating income of {m(boi)}. {short} actually sold {n(au)} units, with revenue of {m(ar)}, variable costs of {m(av)}, and fixed costs of {m(af)}, for operating income of {m(aoi)}. What is the flexible-budget variance for operating income?""",
        choices, ans,
        f"""The flexible budget restates the budget at the actual {n(au)} units: revenue {m(au * price)}, variable costs {m(au * vc)}, fixed costs {m(bf)}, operating income {m(flex)}. Flexible-budget variance = actual {m(aoi)} − flexible {m(flex)} = {fu(fv)} (revenue {m(abs(rv))} {FU(rv)}, variable costs {m(abs(vv))} {FU(vv)}, fixed costs {m(abs(fxv))} {FU(fxv)}). The {fu(sv)} static-budget variance splits into this {m(abs(fv))} {FU(fv)} and a {m(abs(vol))} {FU(vol)} sales-volume variance.""",
    )


def nfp_restricted(p):
    org, short, pr, en, er, q, s, x = (p[k] for k in ("org", "short", "promises", "endow", "earn", "quasi", "schol", "ppe"))
    key_v = pr + en + er + s
    pool = {
        "no_p": (m(key_v - pr), f"Omits the {m(pr)} of promises to give. Amounts receivable in a later period carry an implied time restriction until they are due."),
        "no_er": (m(key_v - er), f"Omits the {m(er)} of unappropriated endowment earnings. Earnings on a donor-restricted endowment stay restricted until appropriated for spending."),
        "plus_q": (m(key_v + q), f"Includes the {m(q)} quasi-endowment. Board designations are net assets without donor restrictions; only donors can impose restrictions."),
        "no_s": (m(key_v - s), f"Omits the {m(s)} of unspent scholarship gifts. A donor's purpose restriction lasts until the gifts are spent for that purpose."),
        "plus_x": (m(key_v + x), f"Includes the {m(x)} of property bought with unrestricted funds. Property carries a donor restriction only when the gifts used to buy it were restricted."),
    }
    key = (m(key_v), f"Correct. {m(pr)} + {m(en)} + {m(er)} + {m(s)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At year-end, {org}, a not-for-profit entity, has: unconditional promises to give of {m(pr)}, due next year, for which donors specified no purpose; an endowment gift of {m(en)} that donors require to be held in perpetuity; {m(er)} of accumulated earnings on that endowment that the board has not yet appropriated for spending; {m(q)} that the board itself has set aside as a quasi-endowment; {m(s)} of unspent gifts that donors restricted to scholarships; and {m(x)} of property and equipment bought with unrestricted funds. What total should {short} report as net assets with donor restrictions?""",
        choices, ans,
        f"""Net assets with donor restrictions: promises to give due in a future period (implied time restriction) {m(pr)}; the perpetual endowment {m(en)}; unappropriated earnings on the donor-restricted endowment {m(er)}; and the unspent scholarship gifts {m(s)}. Total {m(key_v)}. The board-designated quasi-endowment and the property bought with unrestricted funds are without donor restrictions.""",
    )


def nci_income(p):
    par, sub, own, ni, am, sales, cost, held = (p[k] for k in ("par", "sub", "own", "ni", "am", "sales", "cost", "held"))
    ps, ss = par.split()[0], sub.split()[0]
    nci = 100 - own
    up = whole(D(held) / 100 * (sales - cost))
    at = lambda x: whole(D(nci) / 100 * x)
    key_v = at(ni - am - up)
    pool = {
        "no_up": (m(at(ni - am)), f"Adjusts {ss}'s income for the amortization but not for the unrealized profit. {ps} attributes the elimination of upstream profit proportionately, so the noncontrolling interest bears {nci}% of it."),
        "no_am": (m(at(ni - up)), f"Adjusts for the unrealized profit but not the {m(am)} amortization of {ss}'s fair value step-up."),
        "draft": (m(at(ni)), f"Accepts the draft, which applies {nci}% to {ss}'s reported income without either consolidation adjustment."),
        "full_profit": (m(at(ni - am - (sales - cost))), f"Eliminates all {m(sales - cost)} of profit on the intercompany sales. Only the profit on the {held}% still in {ps}'s inventory is unrealized."),
    }
    key = (m(key_v), f"Correct. {nci}% × ({m(ni)} − {m(am)} amortization − {m(up)} unrealized profit on {ss}'s sale).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{par} owns {own}% of {sub} and measured the noncontrolling interest at fair value at acquisition. For Year 2, {ss} reports net income of {m(ni)}. Consolidation adjustments for Year 2 include {m(am)} of amortization of the excess of fair value over book value of {ss}'s equipment at the acquisition date. During Year 2 {ss} also sold goods to {ps} for {m(sales)} that had cost {ss} {m(cost)}, and {ps} still holds {held}% of them at year-end. {ps} attributes the elimination of profit on {ss}'s sales to {ps} proportionately between the parent and the noncontrolling interest. {ps}'s draft consolidated income statement reports net income attributable to the noncontrolling interest of {m(at(ni))}. After any corrections needed, what should that amount be?""",
        choices, ans,
        f"""The noncontrolling interest shares in the subsidiary's income as adjusted in consolidation. {ss}'s reported income of {m(ni)} is reduced by the {m(am)} amortization of its acquisition-date fair value adjustments and by the unrealized profit on its upstream sale still in {ps}'s inventory: {held}% × ({m(sales)} − {m(cost)}) = {m(up)}. Adjusted income = {m(ni - am - up)}; noncontrolling interest = {nci}% × {m(ni - am - up)} = {m(key_v)}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def ten_percent_test(p):
    co, pr, yrs, ro, rn, fee = (p[k] for k in ("co", "principal", "years", "r_old", "r_new", "fee"))
    short = co.split()[0]
    r = D(ro) / 100
    ann = rd((1 - (1 + r) ** -yrs) / r, "0.0001")
    single = rd((1 + r) ** -yrs, "0.0001")
    new_int = whole(D(pr) * rn / 100)
    pv_int, pv_prin = rd(new_int * ann, "0.01"), rd(pr * single, "0.01")
    new_pv = pv_int + pv_prin + fee
    diff = lambda x: rd(abs(pr - x) / pr * 100, "0.01")
    cls = lambda d: "extinguishment" if d >= 10 else "modification"
    ch = lambda d: f"{d}% change; {cls(d)}"
    key_d = diff(new_pv)
    und_new, und_old = new_int * yrs + pr + fee, whole(D(pr) * ro / 100) * yrs + pr
    und_d = rd(abs(und_old - und_new) / und_old * 100, "0.01")
    rate_d = rd(D(ro - rn), "0.01")
    pool = {
        "rate_diff": (ch(rate_d), f"Compares the interest rates ({ro}% − {rn}%) instead of the present values of the cash flows."),
        "fee_sub": (ch(diff(new_pv - 2 * fee)), f"Subtracts the {m(fee)} fee from the new cash flows. A fee the borrower pays the lender adds to the new debt's cash flows."),
        "no_fee": (ch(diff(new_pv - fee)), f"Leaves out the {m(fee)} fee paid to the lender, which is part of the new debt's cash flows in the 10% test."),
        "undisc": (ch(und_d), f"Compares undiscounted cash flows ({m(und_new)} against {m(und_old)}). The test discounts both at the original effective rate."),
    }
    key = (ch(key_d), f"Correct. New cash flows: {m(new_int)} × {ann} + {m(pr)} × {single} + {m(fee)} fee = {m(new_pv)}, {key_d}% below {m(pr)}.")
    choices, ans = pick(pool, key, p["use"])
    if key_d < 10:
        outcome = f"{key_d}% < 10%, so it is a modification: the fee is amortized as an adjustment of interest over the remaining term."
    else:
        outcome = f"{key_d}% ≥ 10%, so it is an extinguishment: the old note is derecognized, the new note is recorded at fair value, and the fee is included in the gain or loss on extinguishment."
    return variant(
        f"""{co} owes a bank {m(pr)} on a note with {yrs} years remaining and {ro}% interest paid annually; the note's carrying amount is {m(pr)}. The bank agrees to cut the rate to {rn}%, with the principal and maturity unchanged, and {short} pays the bank a {m(fee)} fee to modify the note. {short} is not experiencing financial difficulty. At {ro}%, the present value factors for {yrs} periods are {ann} for an ordinary annuity and {single} for a single sum. By what percentage do the present value of the new cash flows and the present value of the old cash flows differ, and how is the change accounted for?""",
        choices, ans,
        f"""A change in debt terms is an extinguishment if the present value of the new cash flows, including fees paid to the creditor and discounted at the original effective rate, differs by at least 10% from the present value of the remaining original cash flows. New: {m(new_int)} × {ann} = {m(pv_int)} + {m(pr)} × {single} = {m(pv_prin)} + {m(fee)} fee = {m(new_pv)}. Old: {m(pr)}. Difference {outcome}""",
    )


def intangible_impairment(p):
    co, cost, life, yrs, und, fv = (p[k] for k in ("co", "cost", "life", "yrs", "und", "fv"))
    short = co.split()[0]
    amort = whole(D(cost) / life)
    ca = cost - yrs * amort
    assert fv < und < ca
    key_v = ca - fv
    pool = {
        "ca_und": (m(ca - und), "Measures the loss as carrying amount minus undiscounted cash flows. Undiscounted cash flows only test recoverability; the loss is measured against fair value."),
        "und_fv": (m(und - fv), "Measures the loss as undiscounted cash flows minus fair value. The loss is carrying amount minus fair value."),
        "cost_fv": (m(cost - fv), f"Compares fair value with the original {m(cost)} cost, ignoring {WORDS[yrs]} years of amortization."),
        "short_amort": (m(cost - (yrs - 1) * amort - fv), f"Records only {WORDS[yrs - 1]} years of amortization. The list has been amortized for {WORDS[yrs]} years."),
    }
    key = (m(key_v), f"Correct. Carrying amount {m(cost)} − {yrs} × {m(amort)} = {m(ca)}, less fair value {m(fv)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} bought a customer list for {m(cost)} {WORDS[yrs]} years ago and amortizes it straight-line over {life} years with no residual value. After losing a major customer, {short} estimates the list's remaining undiscounted cash flows at {m(und)} and its fair value at {m(fv)}. What impairment loss should {short} recognize?""",
        choices, ans,
        f"""A finite-lived intangible is tested for recoverability like other long-lived assets. Carrying amount = {m(cost)} − {yrs} × ({m(cost)} ÷ {life}) = {m(ca)}. Undiscounted cash flows of {m(und)} are less than the carrying amount, so the asset is impaired. Loss = {m(ca)} − {m(fv)} fair value = {m(key_v)}.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def income_approach(p):
    co, cf, r, cfe, re_, yrs = (p[k] for k in ("co", "cf", "r", "cfe", "re", "yrs"))
    short = co.split()[0]
    A = lambda rate, k: rd((1 - (1 + D(rate) / 100) ** -k) / (D(rate) / 100), "0.0001")
    a, ae, a1 = A(r, yrs), A(re_, yrs), A(r, yrs - 1)
    key_v = rd(cf * a)
    pool = {
        "due": (m(rd(cf + cf * a1)), f"Treats the cash flows as received at the start of each year ({m(cf)} + {m(cf)} × {a1}). They arrive at the end of each year."),
        "entity_rate": (m(rd(cf * ae)), f"Discounts market participants' cash flows at {short}'s own {re_}% cost of capital. Fair value uses market participants' discount rate."),
        "entity_cf": (m(rd(cfe * a)), f"Uses {short}'s own expected cash flows, including entity-specific synergies. Fair value reflects market participant assumptions."),
        "entity_both": (m(rd(cfe * ae)), f"Uses {short}'s own expected cash flows and its own {re_}% cost of capital. Fair value uses market participants' cash flows and discount rate."),
    }
    key = (m(key_v), f"Correct. {m(cf)} × {a}, using market participants' cash flows and discount rate.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} must measure the fair value of a patent using an income approach. Market participants would expect the patent to generate cash flows of {m(cf)} at the end of each of the next {WORDS[yrs]} years and would discount them at {r}%. {short} itself expects {m(cfe)} a year because of synergies with its other products, and its own cost of capital is {re_}%. Present value factors for a {WORDS[yrs]}-year ordinary annuity are {a} at {r}% and {ae} at {re_}%; the {WORDS[yrs - 1]}-year factor at {r}% is {a1}. What is the patent's fair value?""",
        choices, ans,
        f"""Fair value is a market-based measurement: it uses the assumptions market participants would use, not entity-specific synergies or the entity's own cost of capital. Fair value = {m(cf)} × {a} = {m(key_v)}.""",
    )


def capitalized_repairs(p):
    co, rep, life, t = (p[k] for k in ("co", "repairs", "life", "t"))
    short = co.split()[0]
    dep = whole(D(rep) / life)
    net = lambda x: whole(D(x) * (100 - t) / 100)
    re_v, ni_v = net(rep - dep), net(dep)
    both = lambda a, b, word="increase": (
        f"{m(a)} decrease to January 1, Year 2, retained earnings; "
        + (f"{m(b)} {word} to Year 2 net income" if b else "$0 change to Year 2 net income"))
    pool = {
        "no_y2": (both(re_v, 0), f"Gets the prior-period adjustment right but leaves the {m(dep)} of Year 2 depreciation on the repairs in Year 2 expense."),
        "ignore_dep": (both(net(rep), 0), "Ignores the Year 1 depreciation already recorded; the prior-period effect is net of it."),
        "no_tax": (both(rep - dep, dep), f"Leaves out the {t}% tax effect on both amounts."),
        "y2_sign": (both(re_v, ni_v, "decrease"), "Gets the prior-period adjustment right but treats reversing the Year 2 depreciation as a decrease. Removing an expense raises Year 2 net income."),
    }
    key = (both(re_v, ni_v), f"Correct. Year 1 was overstated by ({m(rep)} − {m(dep)}) × {100 - t}%; reversing Year 2's {m(dep)} of depreciation raises Year 2 income by {m(ni_v)}.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: (dollars_in(c[0]), c[0]))
    return variant(
        f"""In Year 1, {co} capitalized {m(rep)} of routine repair costs as equipment and recorded {m(dep)} of depreciation on it ({life}-year life). Before closing its Year 2 books, {short} discovers the error; it has already recorded another {m(dep)} of Year 2 depreciation on the capitalized amount. {short}'s tax rate is {t}% for all effects, and it presents single-year statements. What are the effects of correcting the error?""",
        choices, ans,
        f"""The repairs should have been expensed in Year 1. Year 1 income was overstated by {m(rep)} − {m(dep)} = {m(rep - dep)} before tax, {m(re_v)} after tax, so January 1, Year 2, retained earnings is reduced by {m(re_v)} as a prior-period adjustment. The {m(dep)} of Year 2 depreciation on the capitalized repairs is reversed, raising Year 2 pretax income by {m(dep)} and net income by {m(ni_v)}.""",
    )


def guarantee_commitment(p):
    co, loan, g, c, mk, suit = (p[k] for k in ("co", "loan", "g", "commit", "market", "suit"))
    short = co.split()[0]
    loss = c - mk
    key_v = g + loss
    pool = {
        "zero": ("$0", "Treats every matter as a disclosure. A guarantee is recognized at fair value at inception even when default is unlikely, and a loss on a firm purchase commitment is accrued."),
        "g_only": (m(g), f"Recognizes the guarantee but not the {m(loss)} loss on the purchase commitment."),
        "l_only": (m(loss), "Recognizes the purchase commitment loss but not the guarantee. A guarantee creates a noncontingent obligation to stand ready, recognized at fair value."),
        "plus_suit": (m(key_v + suit), f"Also accrues the {m(suit)} lawsuit. A loss that is reasonably possible but not probable is disclosed, not accrued."),
    }
    key = (m(key_v), f"Correct. The {m(g)} guarantee obligation plus the {m(loss)} loss on the purchase commitment.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} is preparing its year-end statements, which have not been issued. Its files show: (1) on December 31, for a fee, {short} guaranteed a {m(loan)} bank loan of an unrelated supplier; the guarantee's fair value at inception was {m(g)}; the supplier is current on all its payments and has a strong credit rating, and expected credit losses on the guarantee are immaterial; (2) {short} has a noncancelable, unhedged commitment to buy materials next year for {m(c)}, and their market price has fallen to {m(mk)}; (3) in a {m(suit)} lawsuit against {short}, counsel believes {short} has strong defenses and will more likely than not prevail, but cannot rule out an adverse verdict; and (4) {short} does not insure its warehouses against fire, and none has occurred. What total liabilities should {short} recognize for these matters?""",
        choices, ans,
        f"""(1) A guarantor recognizes a liability for the fair value of the obligation it undertakes at inception ({m(g)}), even if payment is remote. (2) A loss on a noncancelable purchase commitment is recognized when the market price falls below the contract price: {m(loss)}. (3) A reasonably possible loss is disclosed, not accrued. (4) The risk of future uninsured losses is not a liability until an event occurs. Total = {m(key_v)}.""",
    )


def nol_benefit(p):
    co, loss, r = (p[k] for k in ("co", "loss", "r"))
    short = co.split()[0]
    key_v = whole(D(loss) * r / 100)
    pool = {
        "zero": ("$0", "Recognizes no benefit because the loss cannot be carried back. A carryforward creates a deferred tax asset when realization is more likely than not."),
        "eighty": (m(whole(key_v * D("0.8"))), "Applies the 80% limitation to the deferred tax asset. The limit affects how fast the loss is used, not how much of it is used, when future income is sufficient."),
        "twenty": (m(whole(key_v * D("0.2"))), "Recognizes a benefit only for the 20% of each future year's income the loss cannot offset. The limit slows the loss's use; the whole loss is still used."),
        "double": (m(2 * key_v), "Records both a current tax refund and a deferred tax asset for the same loss. With no carryback, the whole benefit is a deferred tax benefit."),
    }
    key = (m(key_v), f"Correct. Deferred tax asset {m(loss)} × {r}% = {m(key_v)}, with a matching deferred tax benefit.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""In Year 1, {co} has a pretax book loss and a taxable loss of {m(loss)}, with no temporary or permanent differences. Under current federal law the loss can be carried forward indefinitely but not back, and in any future year it can offset only 80% of that year's taxable income. {short} expects enough future taxable income to use the whole loss and needs no valuation allowance. The enacted tax rate is {r}%. What income tax benefit should {short} report in Year 1?""",
        choices, ans,
        f"""The net operating loss carryforward gives rise to a deferred tax asset of {m(loss)} × {r}% = {m(key_v)}. Because {short} expects to use the entire carryforward, no valuation allowance is needed, and the {m(key_v)} is a deferred income tax benefit that offsets the pretax loss. The 80% limitation affects the timing of use, not the total, when future taxable income is sufficient.""",
    )


FAMILIES = {
    "far-budget-variance-0001": (flexible_budget, [
        dict(co="Norris Co.", bu=10000, br=500000, bv=300000, bf=120000, au=11000, ar=561000, av=341000, af=125000, use=["wrong_dir", "static", "volume"]),
        dict(co="Orwell Co.", bu=20000, br=800000, bv=500000, bf=200000, au=18000, ar=756000, av=459000, af=190000, use=["static", "volume", "wrong_dir"]),
        dict(co="Pell Co.", bu=5000, br=400000, bv=250000, bf=90000, au=6000, ar=474000, av=306000, af=88000, use=["rev_only", "static", "volume"]),
        dict(co="Quade Co.", bu=8000, br=480000, bv=288000, bf=100000, au=9000, ar=549000, av=333000, af=104000, use=["wrong_dir", "rev_only", "volume"]),
    ]),
    "far-nfp-financial-position-0001": (nfp_restricted, [
        dict(org="Oak Hollow Society", short="Oak Hollow", promises=80000, endow=500000, earn=60000, quasi=200000, schol=45000, ppe=900000, use=["no_p", "no_er", "plus_q"]),
        dict(org="Birch Lane Trust", short="Birch Lane", promises=120000, endow=750000, earn=90000, quasi=300000, schol=30000, ppe=1200000, use=["no_s", "plus_q", "plus_x"]),
        dict(org="Cedar Ridge Alliance", short="Cedar Ridge", promises=50000, endow=300000, earn=25000, quasi=150000, schol=70000, ppe=600000, use=["no_s", "no_p", "no_er"]),
        dict(org="Elm Street Guild", short="Elm Street", promises=95000, endow=400000, earn=40000, quasi=250000, schol=55000, ppe=700000, use=["no_p", "no_s", "plus_q"]),
    ]),
    "far-consolidated-statements-0004": (nci_income, [
        dict(par="Pace Corp.", sub="Sorel Inc.", own=80, ni=200000, am=15000, sales=100000, cost=60000, held=25, use=["no_up", "no_am", "draft"]),
        dict(par="Rand Corp.", sub="Tellis Inc.", own=70, ni=300000, am=20000, sales=150000, cost=90000, held=40, use=["full_profit", "no_am", "draft"]),
        dict(par="Stroud Corp.", sub="Umber Inc.", own=90, ni=450000, am=30000, sales=200000, cost=120000, held=50, use=["no_up", "no_am", "draft"]),
        dict(par="Whitcomb Corp.", sub="Arden Inc.", own=75, ni=240000, am=12000, sales=80000, cost=50000, held=20, use=["full_profit", "no_up", "no_am"]),
    ]),
    "far-debt-modification-0001": (ten_percent_test, [
        dict(co="Wade Co.", principal=1000000, years=5, r_old=8, r_new=5, fee=20000, use=["rate_diff", "fee_sub", "no_fee"]),
        dict(co="Ashford Co.", principal=2000000, years=4, r_old=7, r_new=4, fee=30000, use=["rate_diff", "undisc", "no_fee"]),
        dict(co="Brandt Co.", principal=500000, years=6, r_old=9, r_new=4, fee=5000, use=["rate_diff", "undisc", "no_fee"]),
        dict(co="Colby Co.", principal=1500000, years=5, r_old=6, r_new=4, fee=30000, use=["rate_diff", "no_fee", "fee_sub"]),
    ]),
    "far-intangibles-impairment-0001": (intangible_impairment, [
        dict(co="Zane Co.", cost=400000, life=8, yrs=3, und=230000, fv=180000, use=["ca_und", "und_fv", "cost_fv"]),
        dict(co="Arlen Co.", cost=600000, life=10, yrs=4, und=330000, fv=250000, use=["ca_und", "short_amort", "cost_fv"]),
        dict(co="Bristow Co.", cost=240000, life=6, yrs=2, und=150000, fv=100000, use=["ca_und", "und_fv", "short_amort"]),
        dict(co="Cortland Co.", cost=900000, life=12, yrs=5, und=480000, fv=390000, use=["und_fv", "short_amort", "cost_fv"]),
    ]),
    "far-fair-value-techniques-0001": (income_approach, [
        dict(co="Barr Co.", cf=100000, r=10, cfe=120000, re=12, yrs=5, use=["due", "entity_rate", "entity_cf"]),
        dict(co="Dalton Co.", cf=80000, r=9, cfe=95000, re=7, yrs=6, use=["entity_rate", "due", "entity_cf"]),
        dict(co="Ebert Co.", cf=150000, r=8, cfe=170000, re=11, yrs=4, use=["entity_rate", "entity_both", "due"]),
        dict(co="Grayson Co.", cf=60000, r=12, cfe=64000, re=10, yrs=5, use=["entity_rate", "entity_cf", "entity_both"]),
    ]),
    "far-accounting-errors-0003": (capitalized_repairs, [
        dict(co="Toft Co.", repairs=60000, life=5, t=25, use=["no_y2", "ignore_dep", "no_tax"]),
        dict(co="Ulster Co.", repairs=90000, life=6, t=21, use=["no_y2", "y2_sign", "ignore_dep"]),
        dict(co="Vardon Co.", repairs=40000, life=4, t=30, use=["no_y2", "y2_sign", "no_tax"]),
        dict(co="Wexler Co.", repairs=75000, life=5, t=25, use=["y2_sign", "ignore_dep", "no_tax"]),
    ]),
    "far-contingencies-0004": (guarantee_commitment, [
        dict(co="Dunn Co.", loan=500000, g=15000, commit=200000, market=170000, suit=400000, use=["zero", "g_only", "l_only"]),
        dict(co="Eston Co.", loan=800000, g=24000, commit=350000, market=310000, suit=600000, use=["zero", "g_only", "plus_suit"]),
        dict(co="Farrell Co.", loan=300000, g=9000, commit=120000, market=105000, suit=250000, use=["zero", "g_only", "l_only"]),
        dict(co="Gantry Co.", loan=1200000, g=30000, commit=500000, market=440000, suit=900000, use=["g_only", "l_only", "plus_suit"]),
    ]),
    "far-income-taxes-nol-0001": (nol_benefit, [
        dict(co="Abbot Corp.", loss=400000, r=21, use=["zero", "eighty", "twenty"]),
        dict(co="Bexley Corp.", loss=650000, r=21, use=["zero", "eighty", "double"]),
        dict(co="Carrow Corp.", loss=300000, r=25, use=["zero", "twenty", "eighty"]),
        dict(co="Denton Corp.", loss=520000, r=24, use=["twenty", "eighty", "double"]),
    ]),
}

if __name__ == "__main__":
    run(FAMILIES, CONTENT)
