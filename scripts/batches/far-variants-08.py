"""FAR variants 08: three extra versions for 11 numeric items from FAR batch 01.

Method as in far-variants-03.py (shared helpers in variants.py).

Run: python3 scripts/batches/far-variants-08.py   See docs/reviews/far-variants-08.md.
"""
import os
from decimal import Decimal as D

from common import variant
from variants import WORDS, m, n, pick, rd, run, whole

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def net(x, t):
    return whole(D(x) * (100 - t) / 100)


def at(pct, x):
    return whole(D(pct) / 100 * x)


# ── Area I ───────────────────────────────────────────────────────────────


def operating_section(p):
    co, ni, dep, px, cv, dar, dinv, div = (p[k] for k in ("co", "ni", "dep", "proceeds", "cv", "d_ar", "d_inv", "div"))
    gain = px - cv
    draft = ni + dep + px - dar + dinv - div
    key_v = ni + dep - gain - dar + dinv
    pool = {
        "div_left": (m(key_v - div), f"Moves the proceeds to investing and removes the gain, but leaves the {m(div)} of dividends paid in operating activities. Under U.S. GAAP, dividends paid are a financing outflow."),
        "gain_left": (m(key_v + gain), f"Removes the proceeds and the dividends but not the {m(gain)} gain ({m(px)} − {m(cv)}) inside net income. The gain's cash is part of the investing inflow, so it must come out of operating."),
        "draft": (m(draft), "Accepts the draft. Proceeds from selling equipment are an investing inflow and dividends paid are a financing outflow; neither belongs in operating activities."),
        "cv_sub": (m(key_v + gain - cv), f"Subtracts the equipment's {m(cv)} carrying amount instead of the {m(gain)} gain. Under the indirect method only the gain included in net income is removed."),
        "ar_sign": (m(key_v + 2 * dar), f"Adds the {m(dar)} increase in accounts receivable. Sales not yet collected raise net income without cash, so the increase is subtracted."),
    }
    key = (m(key_v), f"Correct. {m(ni)} + {m(dep)} − {m(gain)} gain − {m(dar)} + {m(dinv)}. The {m(px)} of proceeds is investing and the dividends are financing.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s staff accountant prepared the operating section of the draft statement of cash flows under the indirect method as follows: net income {m(ni)}; plus depreciation {m(dep)}; plus proceeds from the sale of equipment {m(px)}; less increase in accounts receivable {m(dar)}; plus decrease in inventory {m(dinv)}; less dividends paid {m(div)}; net cash provided by operating activities {m(draft)}. The equipment sold had a carrying amount of {m(cv)}, and the sale is reflected in net income. After correcting the draft to comply with U.S. GAAP, what is net cash provided by operating activities?""",
        choices, ans,
        f"""The draft has three errors. (1) The {m(px)} of sale proceeds is an investing inflow, so it comes out of operating. (2) Net income includes a {m(gain)} gain ({m(px)} − {m(cv)} carrying amount); under the indirect method the gain is subtracted, because its cash is reported in investing. (3) Dividends paid are a financing outflow under U.S. GAAP. Corrected: {m(ni)} + {m(dep)} − {m(gain)} − {m(dar)} + {m(dinv)} = {m(key_v)}.""",
    )


def financing_section(p):
    co, cv, paid, div, stock, conv, intr, ts = (p[k] for k in ("co", "cv", "paid", "div", "stock", "conv", "interest", "treasury"))
    short = co.split()[0]
    key_v = paid + div - stock + ts
    assert key_v >= conv
    pool = {
        "conv_in": (m(key_v - conv), f"Treats the {m(conv)} preferred-to-common conversion as a financing inflow. No cash changes hands; it is disclosed as a noncash financing activity."),
        "carrying": (m(key_v - (paid - cv)), f"Uses the bonds' {m(cv)} carrying amount instead of the {m(paid)} of cash paid to retire them. The {m(paid - cv)} loss is not cash; the financing outflow is the cash paid."),
        "plus_int": (m(key_v + intr), f"Also includes the {m(intr)} of interest paid. Under U.S. GAAP, interest paid is an operating outflow."),
        "no_treasury": (m(key_v - ts), f"Leaves out the {m(ts)} paid to reacquire treasury stock, a financing outflow."),
    }
    key = (m(key_v), f"Correct. −{m(paid)} bond retirement − {m(div)} dividends + {m(stock)} stock issued − {m(ts)} treasury stock.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""During the year, {co} (1) retired bonds with a carrying amount of {m(cv)} by paying bondholders {m(paid)} in cash, (2) paid {m(div)} of cash dividends to its shareholders, (3) issued common stock for {m(stock)} in cash, (4) issued common stock to holders of its preferred stock, who converted preferred shares with a carrying amount of {m(conv)}, (5) paid {m(intr)} of interest on its bonds, and (6) paid {m(ts)} to reacquire its own common shares as treasury stock. Under U.S. GAAP, what is {short}'s net cash used in financing activities for the year?""",
        choices, ans,
        f"""Financing activities under U.S. GAAP: cash paid to retire debt (the {m(paid)} paid, not the carrying amount) −{m(paid)}; dividends paid −{m(div)}; proceeds from issuing stock +{m(stock)}; purchase of treasury stock −{m(ts)}. Net cash used = {m(key_v)}. The preferred-to-common conversion involves no cash and is disclosed as a noncash financing activity, and interest paid is an operating cash flow.""",
    )


def nci_balance(p):
    par, sub, own, price, fv_nci, bv, step, life, ni, div = (
        p[k] for k in ("par", "sub", "own", "price", "fv_nci", "bv", "step", "life", "ni", "div"))
    ps, ss = par.split()[0], sub.split()[0]
    nci = 100 - own
    amort = whole(D(step) / life)
    share_inc, share_div = at(nci, ni - amort), at(nci, div)
    key_v = fv_nci + share_inc - share_div
    draft = at(nci, bv + ni - div)
    ident = at(nci, bv + step)
    pool = {
        "draft": (m(draft), f"Accepts the draft, which is {nci}% of the {m(bv + ni - div)} of net assets on {ss}'s own year-end books. Noncontrolling interest starts at its acquisition-date fair value, not at a share of the subsidiary's book value."),
        "ident": (m(ident + share_inc - share_div), f"Starts from {nci}% of the fair value of {ss}'s identifiable net assets ({m(ident)}), which leaves out the noncontrolling interest's share of goodwill. U.S. GAAP measures noncontrolling interest at its full acquisition-date fair value."),
        "no_amort": (m(fv_nci + at(nci, ni) - share_div), f"Allocates {nci}% of {ss}'s reported {m(ni)} without first deducting the {m(amort)} of depreciation on the equipment's fair value step-up."),
        "no_div": (m(fv_nci + share_inc), f"Leaves out the {m(share_div)} of dividends paid to the noncontrolling interest, which reduce it."),
    }
    key = (m(key_v), f"Correct. {m(fv_nci)} + {nci}% × ({m(ni)} − {m(amort)} extra depreciation) − {nci}% × {m(div)} dividends.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {par} acquires {own}% of the voting stock of {sub} for {m(price)} in cash. The acquisition-date fair value of the {nci}% noncontrolling interest is {m(fv_nci)}. {ss}'s net assets had a book value of {m(bv)}. Its equipment, with a {life}-year remaining life and straight-line depreciation, had a fair value {m(step)} above book value, and every other identifiable asset and liability had a fair value equal to book value. For Year 1, {ss} reports net income of {m(ni)} on its own books and pays dividends of {m(div)}. {ps}'s draft December 31, Year 1, consolidated balance sheet reports noncontrolling interest of {m(draft)}. After any correction needed, at what amount should noncontrolling interest be reported?""",
        choices, ans,
        f"""Under ASC 805 and 810, noncontrolling interest is measured at acquisition-date fair value ({m(fv_nci)}), which includes its share of goodwill. It is then increased by its share of the subsidiary's income as adjusted for the acquisition-date fair value differences and reduced by its share of dividends. Consolidated Year 1 income of {ss} = {m(ni)} − {m(step)} ÷ {life} = {m(ni - amort)}; the noncontrolling interest's share is {m(share_inc)}. Dividends to the noncontrolling interest are {nci}% × {m(div)} = {m(share_div)}. NCI = {m(fv_nci)} + {m(share_inc)} − {m(share_div)} = {m(key_v)}.""",
    )


def diluted_eps(p):
    co, ni, sh, pref, opts, ex, avg, face, rate, conv, t = (
        p[k] for k in ("co", "ni", "shares", "pref", "options", "exercise", "avg", "face", "rate", "conv", "t"))
    short = co.split()[0]
    incr = whole(opts - D(opts) * ex / avg)
    num = ni - pref
    eps = lambda a, b: rd(D(a) / b, "0.01")
    e1 = eps(num, sh + incr)
    bint = whole(D(face) * rate / 100 * (100 - t) / 100)
    bps = eps(bint, conv)
    assert bps > e1
    pool = {
        "all_opts": (f"${eps(num, sh + opts)}", f"Adds all {n(opts)} option shares. Under the treasury stock method only the shares not covered by assumed repurchase ({n(incr)}) are added."),
        "with_bonds": (f"${eps(num + bint, sh + incr + conv)}", f"Includes the convertible bonds. Their incremental effect is {m(bint)} ÷ {n(conv)} = ${bps} per share, above the ${e1} diluted EPS before the bonds, so they are antidilutive and excluded."),
        "no_pref": (f"${eps(ni, sh + incr)}", f"Does not deduct the {m(pref)} of cumulative preferred dividends. Cumulative dividends are deducted whether or not declared."),
        "basic": (f"${eps(num, sh)}", "Reports basic EPS. The options are dilutive, so their incremental shares are included in diluted EPS."),
    }
    key = (f"${e1}", f"Correct. ({m(ni)} − {m(pref)}) ÷ ({n(sh)} + {n(incr)} option shares).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} reports net income of {m(ni)} and {n(sh)} weighted-average common shares outstanding for the year. It has cumulative preferred stock on which {m(pref)} of dividends accrued this year, none of which was declared. {short} also has (1) options to buy {n(opts)} common shares at {m(ex)} per share, outstanding all year, with an average market price of {m(avg)} during the year, and (2) {m(face)} of {rate}% convertible bonds issued at par and outstanding all year, convertible into {n(conv)} common shares. {short}'s tax rate is {t}%. What are {short}'s diluted earnings per share, rounded to the nearest cent?""",
        choices, ans,
        f"""Income available to common = {m(ni)} − {m(pref)} cumulative preferred dividends = {m(num)}. Options (treasury stock method): {n(opts)} − ({n(opts)} × {m(ex)} ÷ {m(avg)}) = {n(incr)} incremental shares, which are dilutive. Convertible bonds (if-converted): add back after-tax interest of {m(whole(D(face) * rate / 100))} × (1 − {t}%) = {m(bint)} and add {n(conv)} shares; the incremental effect is ${bps} per share, higher than the ${e1} EPS so far, so the bonds are antidilutive and excluded. Diluted EPS = {m(num)} ÷ {n(sh + incr)} = ${e1}.""",
    )


def comprehensive_income(p):
    co, ni, hold, fx, g, eq = (p[k] for k in ("co", "ni", "holding", "fx", "realized", "equity_gain"))
    short = co.split()[0]
    draft = ni + hold + fx
    key_v = ni + fx + hold - g
    pool = {
        "fx_dropped": (m(key_v - fx), f"Takes the {m(fx)} exchange gain out of OCI but never adds it to net income. A remeasurement gain on a foreign-currency payable is a transaction gain reported in net income, so it stays in comprehensive income."),
        "draft": (m(draft), f"Accepts the draft total. Moving the exchange gain to net income does not change the total, but the draft omits the reclassification adjustment: the {m(g)} gain sat in OCI in earlier years and is now in net income, so it must come out of OCI."),
        "double_fx": (m(draft + fx - g), f"Adds the {m(fx)} exchange gain to net income and makes the reclassification adjustment, but also leaves the gain in OCI, so it is counted twice."),
        "equity_rm": (m(key_v - eq), f"Removes the {m(eq)} gain on the equity investment. Changes in the fair value of equity securities with readily determinable fair values are recognized in net income."),
    }
    key = (m(key_v), f"Correct. Net income {m(ni + fx)} ({m(ni)} + {m(fx)} transaction gain) + OCI {m(hold - g)} ({m(hold)} − {m(g)} reclassification adjustment).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s draft statement of comprehensive income reports net income of {m(ni)} and other comprehensive income (OCI) of {m(hold + fx)}, for comprehensive income of {m(draft)}. All amounts below are net of tax. Net income includes a {m(g)} gain on the sale of available-for-sale debt securities that {short} bought three years ago and whose fair value did not change during the current year before the sale, and a {m(eq)} gain from the increase in fair value of an equity investment that has a readily determinable fair value. The draft's OCI consists of {m(hold)} of unrealized holding gains that arose this year on {short}'s remaining available-for-sale debt securities and a {m(fx)} gain from remeasuring a euro-denominated account payable at the year-end exchange rate. What is {short}'s corrected comprehensive income for the year?""",
        choices, ans,
        f"""The draft has two errors. (1) The {m(fx)} gain on remeasuring a euro payable is a foreign-currency transaction gain, which is reported in net income, not OCI; corrected net income is {m(ni + fx)}. (2) The {m(g)} gain on the AFS securities was recognized in OCI as an unrealized gain in earlier years (their fair value did not change this year), so moving it into net income on the sale requires a reclassification adjustment out of OCI: {m(hold)} − {m(g)} = {m(hold - g)}. The {m(eq)} equity-investment gain is correctly in net income (ASC 321). Comprehensive income = {m(ni + fx)} + {m(hold - g)} = {m(key_v)}.""",
    )


def shares_for_land(p):
    co, par, n1, p1, n2, mkt, appr, cost = (p[k] for k in ("co", "par", "n1", "p1", "n2", "mkt", "appraisal", "costs"))
    short = co.split()[0]
    cash_apic = n1 * (p1 - par)
    land_apic = n2 * (mkt - par)
    key_v = cash_apic + land_apic - cost
    draft = cash_apic + appr - n2 * par
    pool = {
        "appraisal_net": (m(draft - cost), f"Nets the offering costs against APIC but keeps the land at its {m(appr)} appraisal. Shares issued for an asset are measured at the shares' fair value, and the quoted {m(mkt)} price gives {m(n2 * mkt)}."),
        "costs_exp": (m(cash_apic + land_apic), f"Measures the land at the share price but leaves the {m(cost)} of offering costs in expense. Direct costs of issuing shares reduce the proceeds, so they reduce APIC."),
        "draft": (m(draft), f"Accepts the draft, which records the land at the appraisal ({m(appr - n2 * par)} of APIC) and expenses the offering costs."),
        "par_err": (m(n1 * p1 + n2 * mkt - cost), "Credits the full proceeds to APIC without first crediting common stock for the par value of the shares issued."),
    }
    key = (m(key_v), f"Correct. Cash sale {m(cash_apic)} + land {m(land_apic)} ({n(n2)} × {m(mkt - par)}) − {m(cost)} of offering costs.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""During the year, {co} issues {m(par)} par value common stock as follows: (1) {n(n1)} shares sold for cash at {m(p1)} per share, and (2) {n(n2)} shares issued for a parcel of land. On the exchange date, {short}'s shares trade actively on a national exchange at {m(mkt)} per share, and an independent appraisal values the land at {m(appr)}. {short} also pays {m(cost)} of legal and underwriting costs directly attributable to issuing the shares. {short}'s draft year-end statements show land of {m(appr)}, additional paid-in capital of {m(draft)} from these issuances, and {m(cost)} of legal and underwriting fees in general and administrative expense. After any corrections needed, what is the total additional paid-in capital from these issuances?""",
        choices, ans,
        f"""Since ASU 2018-07, shares issued to a nonemployee for goods used in operations are measured under ASC 718 at the fair value of the shares issued; the quoted price in an active market is also more reliable than an appraisal. The land is recorded at {n(n2)} × {m(mkt)} = {m(n2 * mkt)}: {m(n2 * par)} of par and {m(land_apic)} of APIC. Cash sale: {n(n1)} × ({m(p1)} − {m(par)}) = {m(cash_apic)} of APIC. Direct costs of issuing equity reduce the proceeds, so the {m(cost)} is reclassified from expense to a reduction of APIC. Total: {m(cash_apic)} + {m(land_apic)} − {m(cost)} = {m(key_v)}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def retirement(p):
    co, out, par, issue, ts_apic, k, cost = (p[k] for k in ("co", "outstanding", "par", "issue", "ts_apic", "retired", "cost"))
    short = co.split()[0]
    excess = k * (cost - par)
    pro = k * (issue - par)
    key_v = excess - pro - ts_apic
    assert key_v > 0
    pool = {
        "prorata_only": (m(excess - pro), f"Charges only the pro rata original APIC ({m(pro)}). APIC from earlier treasury stock gains on the same issue can also absorb the excess."),
        "ts_only": (m(excess - ts_apic), f"Charges only the {m(ts_apic)} of APIC from treasury transactions and none of the {m(pro)} of original APIC on the retired shares."),
        "all_re": (m(excess), f"Charges the entire excess over par to retained earnings. ASC 505-30 permits that alternative, but {short} allocates the excess and uses APIC first."),
        "zero": ("$0", f"Charges the whole excess to additional paid-in capital. That APIC-only method, added by ASU 2025-12, is not {short}'s; under the allocation method APIC absorbs only {m(pro + ts_apic)}."),
    }
    key = (m(key_v), f"Correct. The {m(excess)} excess over par is charged first to the pro rata original APIC ({m(pro)}) and the {m(ts_apic)} of APIC from treasury transactions in the same issue; the remaining {m(key_v)} goes to retained earnings.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} has {n(out)} shares of {m(par)} par common stock outstanding, all originally issued at {m(issue)} per share. Its equity also includes {m(ts_apic)} of additional paid-in capital from earlier sales, at more than cost, of treasury shares from that same issue. {short} reacquires {n(k)} shares at {m(cost)} per share and retires them immediately. {short}'s policy is to allocate the excess of cost over par between additional paid-in capital and retained earnings, charging additional paid-in capital to the maximum extent that allocation method permits. What amount is debited to retained earnings on the retirement?""",
        choices, ans,
        f"""On retirement, common stock is debited at par ({n(k)} × {m(par)} = {m(k * par)}). ASC 505-30 lets the {m(excess)} excess of cost over par be charged entirely to retained earnings, allocated between APIC and retained earnings, or (after ASU 2025-12) charged entirely to APIC; {short} uses the allocation method. When it is allocated, the APIC charge is limited to APIC from earlier retirements and net gains on treasury stock of the same issue ({m(ts_apic)}) plus the pro rata APIC on the same issue ({n(k)} × {m(issue - par)} = {m(pro)}). {short} charges APIC to that limit, {m(pro + ts_apic)}, and retained earnings {m(excess)} − {m(pro + ts_apic)} = {m(key_v)}.""",
    )


def extinguishment(p):
    co, face, c, yrs, y, ic, px = (p[k] for k in ("co", "face", "coupon", "years", "yld", "costs", "repurchase"))
    short = co.split()[0]
    r = D(y) / 100
    cash = whole(D(face) * c / 100)
    price = rd(cash * (1 - (1 + r) ** -yrs) / r + face * (1 + r) ** -yrs)
    i1 = rd(price * r)
    a1 = i1 - cash
    cv1 = price + a1
    i2 = rd(cv1 * r)
    a2 = i2 - cash
    cv2 = cv1 + a2
    ic_yr = whole(D(ic) / yrs)
    unam = ic - 2 * ic_yr
    key_v = px - (cv2 - unam)
    assert key_v > 0 and price < face
    sl = rd((face - price) / yrs)
    pool = {
        "no_costs": (m(px - cv2), f"Ignores the {m(unam)} of unamortized issuance costs, which are part of the net carrying amount and are written off in the loss."),
        "sl": (m(px - (price + 2 * sl - unam)), f"Amortizes the discount straight-line ({m(sl)} a year). The stem calls for the effective interest method, which amortizes {m(a1)} and then {m(a2)}."),
        "all_costs": (m(px - (cv2 - ic)), f"Treats all {m(ic)} of issuance costs as unamortized. Two of {WORDS[yrs]} years have passed, so {m(2 * ic_yr)} has been amortized and {m(unam)} remains."),
        "face": (m(px - face + unam), f"Measures the loss against the bonds' {m(face)} face amount instead of their carrying amount."),
    }
    key = (m(key_v), f"Correct. {m(px)} − ({m(cv2)} carrying amount − {m(unam)} unamortized issuance costs).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} issues {m(face)} of {WORDS[yrs]}-year, {c}% bonds, with interest paid each December 31, for {m(price)}, a price that yields {y}%. {short} pays {m(ic)} of issuance costs and amortizes them straight-line over the {WORDS[yrs]} years, because the result is not materially different from the interest method. {short} amortizes the bond discount using the effective interest method and rounds to the nearest dollar at each step. On December 31, Year 2, immediately after paying interest, {short} repurchases all of the bonds in the open market for {m(px)}. What loss on extinguishment does {short} recognize?""",
        choices, ans,
        f"""Year 1 interest expense = {m(price)} × {y}% = {m(i1)}; cash interest {m(cash)}; discount amortization {m(a1)}; carrying amount {m(cv1)}. Year 2 interest expense = {m(cv1)} × {y}% = {m(i2)}; amortization {m(a2)}; carrying amount {m(cv2)}. Unamortized issuance costs = {m(ic)} − 2 × {m(ic_yr)} = {m(unam)}, so the net carrying amount is {m(cv2 - unam)}. Loss = {m(px)} − {m(cv2 - unam)} = {m(key_v)}.""",
    )


def equity_method_basis(p):
    inv, ee, price, pct_, bv, step, life, ni, div, profit, resold = (
        p[k] for k in ("inv", "ee", "price", "pct", "bv", "step", "life", "ni", "div", "profit", "resold"))
    ishort, eshort = inv.split()[0], ee.split()[0]
    held = 100 - resold
    excess = price - at(pct_, bv)
    equip = at(pct_, step)
    gw = excess - equip
    assert gw >= 0
    amort = whole(D(equip) / life)
    up = at(held, profit)
    up_share = at(pct_, up)
    inc, dv = at(pct_, ni), at(pct_, div)
    key_v = price + inc - dv - amort - up_share
    pool = {
        "full_up": (m(key_v + up_share - up), f"Eliminates 100% of the unrealized profit ({m(up)}). {ishort} eliminates only its {pct_}% share ({m(up_share)})."),
        "no_up": (m(key_v + up_share), "Does not eliminate any of the unrealized profit on the inventory " + f"{eshort} still holds."),
        "no_amort": (m(key_v + amort), f"Omits the {m(amort)} amortization of the equipment's basis difference."),
        "sold_profit": (m(key_v + up_share - at(pct_, at(resold, profit))), f"Eliminates {pct_}% of the profit on the {resold}% {eshort} resold. That profit was realized in sales to outsiders; only the {held}% still held is unrealized."),
        "no_div": (m(key_v + dv), f"Does not reduce the investment for {ishort}'s {m(dv)} share of dividends. Dividends from an equity-method investee are a return of the investment."),
    }
    key = (m(key_v), f"Correct. {m(price)} + {m(inc)} share of income − {m(dv)} dividends − {m(amort)} equipment amortization − {m(up_share)} unrealized profit.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {inv} pays {m(price)} for {pct_}% of the common stock of {ee} and can significantly influence {eshort}'s operating decisions. {eshort}'s net assets have a book value of {m(bv)}. {eshort}'s equipment, which has a {life}-year remaining life and is depreciated straight-line, has a fair value {m(step)} above its book value, and no other asset or liability has a fair value that differs from book value. For the year, {eshort} reports net income of {m(ni)} and pays dividends of {m(div)}. During Year 1, {ishort} sold inventory to {eshort} at a profit of {m(profit)}. {eshort} resold {resold}% of that inventory to outsiders during the year and holds the rest at year-end. Ignore income taxes, and assume {ishort} has not elected the fair value option. What is the carrying amount of {ishort}'s investment in {eshort} at December 31, Year 1?""",
        choices, ans,
        f"""Excess of cost over share of book value = {m(price)} − ({pct_}% × {m(bv)}) = {m(excess)}. Of that, {pct_}% × {m(step)} = {m(equip)} relates to the equipment (amortized over {life} years, {m(amort)} a year) and {m(gw)} is goodwill (not amortized). Carrying amount = {m(price)} + {pct_}% × {m(ni)} ({m(inc)}) − {pct_}% × {m(div)} ({m(dv)} dividends) − {m(amort)} amortization − {pct_}% × ({held}% × {m(profit)}) = {m(up_share)} unrealized profit = {m(key_v)}.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def lawsuit_range(p):
    co, lo, hi, c2 = (p[k] for k in ("co", "low", "high", "claim2"))
    short = co.split()[0]
    mid = whole(D(lo + hi) / 2)
    pool = {
        "mid": (m(mid), "Accrues the midpoint of Claim 1's range. When no amount in a range is a better estimate than any other, U.S. GAAP accrues the minimum."),
        "plus_c2": (m(lo + c2), "Also accrues Claim 2. A loss that is more than remote but less than probable is disclosed, not accrued."),
        "high": (m(hi), "Accrues the top of Claim 1's range. The minimum is accrued, and the rest of the range is disclosed."),
        "zero": ("$0", "Only discloses Claim 1 because no amount in its range is a better estimate. A probable loss with an estimable range is accrued at the minimum."),
    }
    key = (m(lo), f"Correct. Claim 1 is probable with no best estimate in the range, so {short} accrues the minimum and discloses the further {m(hi - lo)} of possible loss. Claim 2 is only disclosed.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31 financial statements have not yet been issued. Its outside counsel's letter describes two lawsuits filed against {short} during the year. Claim 1: last year the same court ruled against a competitor on nearly identical facts, {short} has offered to settle, and counsel expects {short} to pay damages of between {m(lo)} and {m(hi)}, with no amount in that range a better estimate than any other. Claim 2: counsel believes {short}'s defenses are stronger than the plaintiff's case and that {short} will more likely than not prevail, but counsel cannot dismiss the chance of an adverse judgment; if {short} loses, damages would be about {m(c2)}. What total liability should {short} accrue for the two lawsuits at December 31?""",
        choices, ans,
        f"""Claim 1: the adverse precedent, the settlement offer, and counsel's expectation of payment make the loss probable, and it can be estimated as a range. With no amount in the range better than any other, ASC 450-20 requires accruing the minimum ({m(lo)}) and disclosing the reasonably possible additional loss of up to {m(hi - lo)}. Claim 2: a loss that counsel thinks is less likely than not but cannot dismiss is reasonably possible, so {short} discloses its nature and the {m(c2)} estimate but records nothing. Total accrual: {m(lo)}.""",
    )


def two_errors(p):
    co, mach, life, inv, t = (p[k] for k in ("co", "machine", "life", "inv", "t"))
    short = co.split()[0]
    dep = whole(D(mach) / life)
    ca = mach - 2 * dep
    ch = lambda x: f"{m(abs(x))} {'increase' if x > 0 else 'decrease'}"
    key_v = net(ca - inv, t)
    pool = {
        "no_tax": (ch(ca - inv), f"Gets the net pre-tax effect right but omits the {t}% tax effect of the corrections."),
        "machine_only": (ch(net(ca, t)), f"Corrects only the machine ({m(ca)} × {100 - t}%). The inventory overstatement also affected retained earnings at December 31, Year 2."),
        "inv_sign": (ch(net(ca + inv, t)), f"Adds the inventory overstatement instead of subtracting it. Overstated ending inventory overstated income, so it reduces the correction ({m(ca)} + {m(inv)}) × {100 - t}%."),
        "three_yrs": (ch(net(ca - dep - inv, t)), "Removes three years of depreciation, including Year 3. The January 1, Year 3, balance reflects only Years 1 and 2."),
    }
    key = (ch(key_v), f"Correct. Machine: {m(ca)} pre-tax understatement ({m(mach)} − 2 × {m(dep)} of depreciation). Inventory: {m(inv)} overstatement. Net {m(ca - inv)} × {100 - t}%.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""In Year 3, before its Year 3 financial statements are issued, {co} finds two errors in its prior-year statements. (1) On January 1, Year 1, it bought a machine for {m(mach)} with a {life}-year life, no salvage value, and straight-line depreciation, and it recorded the entire {m(mach)} as Year 1 expense. The machine is still in use. (2) Its December 31, Year 2, ending inventory was overstated by {m(inv)}. {short} presents single-year financial statements and applies a {t}% tax rate to all corrections. What adjustment should {short} make to its January 1, Year 3, retained earnings?""",
        choices, ans,
        f"""A correction of a prior-period error adjusts the opening balance of retained earnings, net of tax. Machine: expensing {m(mach)} in Year 1 understated retained earnings at January 1, Year 3, by the asset's carrying amount then, {m(mach)} − 2 × {m(dep)} = {m(ca)}. Inventory: the {m(inv)} overstatement at December 31, Year 2, overstated retained earnings. Net pre-tax effect: {m(ca)} − {m(inv)} = {m(ca - inv)} increase; after {t}% tax, {m(key_v)} increase.""",
    )


FAMILIES = {
    "far-cash-flows-0003": (operating_section, [
        dict(co="Marlow Corp.", ni=180000, dep=24000, proceeds=45000, cv=36000, d_ar=31000, d_inv=12000, div=20000, use=["div_left", "gain_left", "draft"]),
        dict(co="Norwich Corp.", ni=260000, dep=38000, proceeds=70000, cv=52000, d_ar=44000, d_inv=15000, div=30000, use=["cv_sub", "div_left", "gain_left"]),
        dict(co="Oxbow Corp.", ni=120000, dep=15000, proceeds=30000, cv=26000, d_ar=18000, d_inv=9000, div=12000, use=["gain_left", "draft", "ar_sign"]),
        dict(co="Pembroke Corp.", ni=400000, dep=55000, proceeds=120000, cv=90000, d_ar=60000, d_inv=20000, div=50000, use=["div_left", "gain_left", "draft"]),
    ]),
    "far-cash-flows-0004": (financing_section, [
        dict(co="Fenwick Ltd.", cv=192000, paid=200000, div=20000, stock=150000, conv=100000, interest=12000, treasury=30000, use=["conv_in", "carrying", "plus_int"]),
        dict(co="Garrison Ltd.", cv=288000, paid=300000, div=45000, stock=200000, conv=60000, interest=18000, treasury=25000, use=["conv_in", "carrying", "no_treasury"]),
        dict(co="Hollister Ltd.", cv=470000, paid=480000, div=60000, stock=400000, conv=150000, interest=30000, treasury=50000, use=["carrying", "plus_int", "no_treasury"]),
        dict(co="Irwin Ltd.", cv=145000, paid=150000, div=15000, stock=100000, conv=40000, interest=9000, treasury=20000, use=["conv_in", "no_treasury", "carrying"]),
    ]),
    "far-consolidated-statements-0001": (nci_balance, [
        dict(par="Pratt Corp.", sub="Tern Inc.", own=80, price=800000, fv_nci=200000, bv=700000, step=100000, life=5, ni=150000, div=50000, use=["draft", "ident", "no_amort"]),
        dict(par="Raleigh Corp.", sub="Stowe Inc.", own=70, price=1400000, fv_nci=570000, bv=1600000, step=200000, life=4, ni=300000, div=100000, use=["ident", "no_amort", "no_div"]),
        dict(par="Thayer Corp.", sub="Umbra Inc.", own=90, price=1800000, fv_nci=190000, bv=1500000, step=150000, life=5, ni=250000, div=80000, use=["draft", "ident", "no_div"]),
        dict(par="Whitmore Corp.", sub="Yolo Inc.", own=75, price=1200000, fv_nci=400000, bv=1300000, step=240000, life=6, ni=360000, div=120000, use=["ident", "no_amort", "no_div"]),
    ]),
    "far-eps-diluted-0001": (diluted_eps, [
        dict(co="Kestrel Corp.", ni=1200000, shares=500000, pref=100000, options=40000, exercise=30, avg=50, face=1000000, rate=6, conv=20000, t=25, use=["all_opts", "with_bonds", "no_pref"]),
        dict(co="Larkin Corp.", ni=2000000, shares=800000, pref=200000, options=60000, exercise=40, avg=60, face=2000000, rate=5, conv=25000, t=25, use=["with_bonds", "basic", "no_pref"]),
        dict(co="Merrick Corp.", ni=900000, shares=300000, pref=60000, options=30000, exercise=20, avg=40, face=1500000, rate=7, conv=25000, t=21, use=["all_opts", "with_bonds", "basic"]),
        dict(co="Nutley Corp.", ni=3000000, shares=1000000, pref=250000, options=100000, exercise=45, avg=75, face=3000000, rate=6, conv=40000, t=25, use=["with_bonds", "basic", "no_pref"]),
    ]),
    "far-comprehensive-income-0002": (comprehensive_income, [
        dict(co="Delmar Inc.", ni=400000, holding=67500, fx=30000, realized=22500, equity_gain=15000, use=["fx_dropped", "draft", "double_fx"]),
        dict(co="Elgar Inc.", ni=650000, holding=90000, fx=40000, realized=35000, equity_gain=20000, use=["fx_dropped", "equity_rm", "draft"]),
        dict(co="Fenwood Inc.", ni=300000, holding=45000, fx=18000, realized=12000, equity_gain=9000, use=["draft", "double_fx", "fx_dropped"]),
        dict(co="Grafton Inc.", ni=1000000, holding=150000, fx=60000, realized=50000, equity_gain=30000, use=["fx_dropped", "equity_rm", "double_fx"]),
    ]),
    "far-equity-paid-in-capital-0002": (shares_for_land, [
        dict(co="Redford Corp.", par=2, n1=5000, p1=18, n2=3000, mkt=19, appraisal=60000, costs=9000, use=["appraisal_net", "costs_exp", "draft"]),
        dict(co="Selwyn Corp.", par=1, n1=8000, p1=25, n2=4000, mkt=27, appraisal=100000, costs=12000, use=["appraisal_net", "costs_exp", "draft"]),
        dict(co="Tolliver Corp.", par=5, n1=3000, p1=30, n2=2000, mkt=32, appraisal=70000, costs=4000, use=["costs_exp", "appraisal_net", "par_err"]),
        dict(co="Underhill Corp.", par=2, n1=10000, p1=15, n2=5000, mkt=16, appraisal=72000, costs=10000, use=["appraisal_net", "costs_exp", "par_err"]),
    ]),
    "far-equity-retirement-0002": (retirement, [
        dict(co="Mercer Inc.", outstanding=10000, par=2, issue=14, ts_apic=1500, retired=1000, cost=20, use=["prorata_only", "ts_only", "all_re"]),
        dict(co="Norland Inc.", outstanding=20000, par=1, issue=10, ts_apic=3000, retired=2000, cost=16, use=["zero", "prorata_only", "ts_only"]),
        dict(co="Ossining Inc.", outstanding=50000, par=5, issue=20, ts_apic=4000, retired=3000, cost=30, use=["prorata_only", "ts_only", "all_re"]),
        dict(co="Peyton Inc.", outstanding=8000, par=3, issue=15, ts_apic=2500, retired=500, cost=28, use=["zero", "ts_only", "all_re"]),
    ]),
    "far-debt-extinguishment-0001": (extinguishment, [
        dict(co="Sable Corp.", face=1000000, coupon=6, years=5, yld=8, costs=20000, repurchase=1020000, use=["no_costs", "sl", "all_costs"]),
        dict(co="Tarleton Corp.", face=500000, coupon=5, years=4, yld=7, costs=12000, repurchase=505000, use=["face", "no_costs", "sl"]),
        dict(co="Vardaman Corp.", face=2000000, coupon=7, years=6, yld=9, costs=30000, repurchase=1990000, use=["no_costs", "sl", "all_costs"]),
        dict(co="Wickham Corp.", face=800000, coupon=4, years=5, yld=6, costs=15000, repurchase=790000, use=["sl", "no_costs", "all_costs"]),
    ]),
    "far-equity-method-0001": (equity_method_basis, [
        dict(inv="Pillar Corp.", ee="Quarry Inc.", price=1500000, pct=30, bv=4000000, step=400000, life=4, ni=600000, div=200000, profit=100000, resold=60, use=["full_up", "no_up", "no_amort"]),
        dict(inv="Rollins Corp.", ee="Shasta Inc.", price=2400000, pct=25, bv=8000000, step=800000, life=5, ni=1000000, div=400000, profit=160000, resold=75, use=["no_up", "no_amort", "no_div"]),
        dict(inv="Trent Corp.", ee="Umpqua Inc.", price=900000, pct=20, bv=3500000, step=500000, life=5, ni=450000, div=150000, profit=80000, resold=75, use=["full_up", "sold_profit", "no_up"]),
        dict(inv="Vinton Corp.", ee="Wasco Inc.", price=3000000, pct=40, bv=6000000, step=600000, life=6, ni=900000, div=300000, profit=200000, resold=70, use=["full_up", "no_up", "no_amort"]),
    ]),
    "far-contingencies-0002": (lawsuit_range, [
        dict(co="Bravo Corp.", low=400000, high=900000, claim2=300000, use=["mid", "plus_c2", "high"]),
        dict(co="Cartwright Corp.", low=250000, high=750000, claim2=180000, use=["zero", "plus_c2", "mid"]),
        dict(co="Delancey Corp.", low=600000, high=1000000, claim2=350000, use=["mid", "plus_c2", "high"]),
        dict(co="Fontaine Corp.", low=150000, high=450000, claim2=400000, use=["zero", "mid", "high"]),
    ]),
    "far-accounting-errors-0001": (two_errors, [
        dict(co="Tanner Inc.", machine=90000, life=5, inv=30000, t=25, use=["no_tax", "machine_only", "inv_sign"]),
        dict(co="Garvin Inc.", machine=120000, life=6, inv=25000, t=21, use=["three_yrs", "no_tax", "machine_only"]),
        dict(co="Hartwell Inc.", machine=60000, life=4, inv=10000, t=30, use=["no_tax", "machine_only", "inv_sign"]),
        dict(co="Ingersoll Inc.", machine=200000, life=8, inv=60000, t=25, use=["three_yrs", "machine_only", "inv_sign"]),
    ]),
}

if __name__ == "__main__":
    run(FAMILIES, CONTENT)
