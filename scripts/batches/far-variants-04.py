"""FAR variants 04: three extra versions for 12 numeric items, 7 from FAR batch 05 and 5 from batch 03.

Method as in far-variants-03.py (shared helpers in variants.py). far-contingencies-0005 is left without
variants: each of its wrong answers is a subset of the key, so the key is always the largest amount and its
letter can't move.

Run: python3 scripts/batches/far-variants-04.py   See docs/reviews/far-variants-04.md.
"""
import os
from decimal import Decimal as D

from common import variant
from variants import WORDS, dollars_in, m, n, pick, rd, run, whole

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def net(x, t):
    return whole(D(x) * (100 - t) / 100)


# ── Area I ───────────────────────────────────────────────────────────────


def changes_in_equity(p):
    co, bre, ni, g, sc, dv = (p[k] for k in ("co", "bre", "ni", "gain", "split", "div"))
    short = co.split()[0]
    key_v = bre + ni - dv
    draft = bre + ni + g - sc
    pool = {
        "split_left": (m(key_v - sc), "Removes the unrealized gain and records the dividend but still charges retained earnings for the split. A split effected by halving par value needs no entry to retained earnings."),
        "oci_left": (m(key_v + g), f"Records the dividend and removes the split charge but leaves the {m(g)} unrealized gain in retained earnings. It belongs in accumulated other comprehensive income."),
        "no_div": (m(bre + ni), "Removes the split charge and the unrealized gain but omits the dividend. A dividend reduces retained earnings when declared, not when paid."),
        "draft": (m(draft), "Accepts the draft."),
    }
    key = (m(key_v), f"Correct. {m(bre)} + {m(ni)} − {m(dv)} declared dividend.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 1 statement of changes in equity reports ending retained earnings of {m(draft)}, computed as beginning retained earnings of {m(bre)}, plus net income of {m(ni)}, plus a {m(g)} unrealized holding gain on available-for-sale debt securities, less {m(sc)} for a 2-for-1 stock split. Supporting documents show that the split was effected by halving the par value per share, and that on December 15, Year 1, the board declared a {m(dv)} cash dividend payable on January 10, Year 2, which the draft omits because it had not been paid. After correcting the draft, what is {short}'s ending retained earnings?""",
        choices, ans,
        f"""Three corrections. (1) The unrealized gain on AFS debt securities is other comprehensive income, accumulated separately from retained earnings. (2) A stock split effected by reducing par value requires no entry. (3) Dividends reduce retained earnings on the declaration date. Ending retained earnings = {m(bre)} + {m(ni)} − {m(dv)} = {m(key_v)}.""",
    )


def nfp_activities(p):
    org, cu, cr, fee, rel, inv, prog, mg, fr = (
        p[k] for k in ("org", "cu", "cr", "fees", "rel", "inv", "prog", "mg", "fr"))
    short = org.split()[0]
    exp = prog + mg + fr
    key_v = cu + fee + rel + inv - exp
    ch = lambda x: f"{m(abs(x))} {'increase' if x >= 0 else 'decrease'}"
    pool = {
        "plus_cr": (ch(key_v + cr), f"Also counts the {m(cr)} of restricted contributions. They increase net assets with donor restrictions until released."),
        "no_rel": (ch(key_v - rel), f"Leaves out the {m(rel)} released from donor restrictions. Releases increase net assets without donor restrictions."),
        "prog_only": (ch(key_v + mg + fr), f"Subtracts only the {m(prog)} of program expenses. Management and general and fundraising expenses also reduce net assets without donor restrictions."),
        "no_inv": (ch(key_v - inv), f"Leaves out the {m(inv)} of net investment return. Return on unrestricted investments increases net assets without donor restrictions."),
    }
    key = (ch(key_v), f"Correct. {m(cu)} + {m(fee)} + {m(rel)} released + {m(inv)} − {m(exp)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""For Year 1, {org}, a not-for-profit entity, reports: contributions without donor restrictions of {m(cu)}; contributions with donor restrictions of {m(cr)}; program service fees of {m(fee)}; net assets released from donor restrictions of {m(rel)}; investment return on unrestricted investments, net of external investment expenses, of {m(inv)}; and expenses of {m(exp)} ({m(prog)} for programs, {m(mg)} for management and general, and {m(fr)} for fundraising). What is the change in {short}'s net assets without donor restrictions for Year 1?""",
        choices, ans,
        f"""Net assets without donor restrictions increase by unrestricted contributions ({m(cu)}), program service fees ({m(fee)}), releases from restrictions ({m(rel)}) and net investment return ({m(inv)}), and decrease by all expenses ({m(exp)}): a {ch(key_v)}. The {m(cr)} of restricted contributions increases net assets with donor restrictions.""",
    )


def investing_section(p):
    co, eq, note, afs, intd, loan, coll, trad = (
        p[k] for k in ("co", "equip", "note", "afs", "intdiv", "loan", "collected", "trading"))
    draft_used = eq - afs - intd + loan - coll + trad
    key_v = (eq - note) - afs + loan - coll
    assert key_v > 0
    pool = {
        "keep_trading": (m(key_v + trad), f"Keeps the {m(trad)} of trading-security purchases in investing. Securities bought principally to sell in the near term are classified by their nature, as operating cash flows."),
        "keep_note": (m(key_v + note), f"Keeps the {m(note)} of equipment financed by the seller. Buying an asset with a note is a noncash investing and financing activity, disclosed but not in the cash flow totals."),
        "draft": (m(draft_used), "Accepts the draft, which also counts interest and dividends received (operating under U.S. GAAP), the note-financed equipment, and the trading securities."),
        "keep_int": (m(key_v - intd), f"Keeps the {m(intd)} of interest and dividends received in investing. Under U.S. GAAP they are operating cash inflows."),
        "no_collect": (m(key_v + coll), f"Leaves out the {m(coll)} of principal collected on the loan, an investing inflow."),
    }
    key = (m(key_v), f"Correct. −{m(eq - note)} cash paid for equipment + {m(afs)} AFS proceeds − {m(loan)} loan + {m(coll)} collected.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s staff accountant prepared the investing section of the draft statement of cash flows: purchases of equipment $({n(eq)}); proceeds from sales of available-for-sale debt securities {m(afs)}; interest and dividends received {m(intd)}; loan made to a supplier $({n(loan)}); principal collected on that loan {m(coll)}; purchases of debt securities bought and held principally to sell in the near term $({n(trad)}); net cash used in investing activities $({n(draft_used)}). Supporting documents show that {m(note)} of the equipment was acquired by signing a note payable to the seller. After correcting the draft to comply with U.S. GAAP, what is net cash used in investing activities?""",
        choices, ans,
        f"""Three corrections. (1) Only {m(eq - note)} of the equipment was paid in cash; the {m(note)} financed by a note is a noncash activity disclosed separately. (2) Interest and dividends received are operating cash flows under U.S. GAAP. (3) Cash flows from securities acquired specifically for resale (trading) are operating. Investing: −{m(eq - note)} + {m(afs)} − {m(loan)} + {m(coll)} = −{m(key_v)}.""",
    )


def basic_eps(p):
    co, s0, iss, sd, tr, ni, pp, pr = (p[k] for k in ("co", "s0", "issued", "sd", "treasury", "ni", "pref_par", "pref_rate"))
    short = co.split()[0]
    f = 1 + D(sd) / 100
    pref = whole(D(pp) * pr / 100)
    avail = ni - pref
    wa = whole(s0 * f + iss * f * D(9) / 12 - tr * D(3) / 12)
    eps = lambda num, den: f"${rd(D(num) / D(den), '0.01')}"
    wa_july = whole(s0 + iss * D(9) / 12 + (s0 + iss) * D(sd) / 100 * D(6) / 12 - tr * D(3) / 12)
    end = whole((s0 + iss) * f - tr)
    wa_nosd = whole(s0 + iss * D(9) / 12 - tr * D(3) / 12)
    pool = {
        "sd_july": (eps(avail, wa_july), f"Applies the stock dividend only from July 1 ({n(wa_july)} weighted shares). A stock dividend is applied retroactively to all shares outstanding before it."),
        "year_end": (eps(avail, end), f"Uses the {n(end)} shares outstanding at year-end instead of the weighted average."),
        "no_pref": (eps(ni, wa), "Ignores the cumulative preferred dividends. For cumulative preferred stock, the current year's dividend is deducted whether or not declared."),
        "no_sd": (eps(avail, wa_nosd), f"Ignores the stock dividend ({n(wa_nosd)} weighted shares). A stock dividend is applied retroactively to all periods and shares before it."),
    }
    key = (eps(avail, wa), f"Correct. ({m(ni)} − {m(pref)}) ÷ {n(wa)} weighted-average shares.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} had {n(s0)} common shares outstanding on January 1. It issued {n(iss)} shares for cash on April 1, distributed a {sd}% stock dividend on July 1, and bought {n(tr)} shares as treasury stock on October 1. Net income for the year is {m(ni)}. {short} also has {pr}% cumulative preferred stock with a par value of {m(pp)}; no preferred dividends were declared this year. What is {short}'s basic earnings per share, rounded to the nearest cent?""",
        choices, ans,
        f"""Income available to common = {m(ni)} − {pr}% × {m(pp)} = {m(avail)} (cumulative dividends are deducted even if not declared). A stock dividend is applied retroactively to all shares outstanding before it: {n(s0)} × {f:.2f} × 12/12 = {n(s0 * f)}; {n(iss)} × {f:.2f} × 9/12 = {n(iss * f * D(9) / 12)}; treasury shares −{n(tr)} × 3/12 = −{n(tr * D(3) / 12)}. Weighted average = {n(wa)}. Basic EPS = {m(avail)} ÷ {n(wa)} = {eps(avail, wa)}.""",
    )


def intercompany_equipment(p):
    par, sub, price, cv, life, pni, sni = (p[k] for k in ("par", "sub", "price", "cv", "life", "pni", "sni"))
    ps, ss = par.split()[0], sub.split()[0]
    gain = price - cv
    exd = whole(D(gain) / life)
    draft = pni + sni
    key_v = draft - gain + exd
    pool = {
        "dep_wrong": (m(draft - gain - exd), f"Eliminates the gain but also deducts the {m(exd)} of excess depreciation. {ps}'s depreciation on the {m(price)} price is {m(exd)} higher than on {ss}'s {m(cv)} carrying amount, so eliminating it increases consolidated income."),
        "gain_only": (m(draft - gain), f"Eliminates the {m(gain)} intercompany gain but not the {m(exd)} of excess depreciation on the stepped-up cost."),
        "draft": (m(draft), "Accepts the draft. A gain on a sale between consolidated entities is not realized until the equipment is used up or sold outside the group."),
        "dep_only": (m(draft + exd), f"Adds back the {m(exd)} of excess depreciation but does not eliminate the {m(gain)} intercompany gain."),
    }
    key = (m(key_v), f"Correct. {m(draft)} − {m(gain)} intercompany gain + {m(exd)} excess depreciation.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{par} owns 100% of {sub} On January 1, Year 2, {ss} sold equipment to {ps} for {m(price)}. {ss}'s carrying amount for the equipment was {m(cv)}, and {ps} depreciates it straight-line over its {life}-year remaining life with no salvage value. For Year 2, {ps} reports net income of {m(pni)} from its own operations, excluding any income from its investment in {ss}, and {ss} reports net income of {m(sni)}. {ps}'s draft Year 2 consolidated income statement reports consolidated net income of {m(draft)}. After any corrections needed, what is consolidated net income?""",
        choices, ans,
        f"""The draft simply adds the two companies' income. In consolidation, {ss}'s {m(gain)} gain ({m(price)} − {m(cv)}) on the sale to {ps} is eliminated, and the equipment is carried at {ss}'s original basis. {ps}'s depreciation of {m(price)} ÷ {life} = {m(D(price) / life)} exceeds depreciation on the {m(cv)} basis ({m(D(cv) / life)}) by {m(exd)}, which is eliminated each year as the gain is realized through use. Consolidated net income = {m(draft)} − {m(gain)} + {m(exd)} = {m(key_v)}.""",
    )


def current_assets(p):
    co, cash, fund, trad, rec, loan, inv, pp, csv = (
        p[k] for k in ("co", "cash", "fund", "trading", "rec", "loan", "inv", "prepaid", "csv"))
    short = co.split()[0]
    half = whole(D(pp) / 2)
    total = cash + trad + rec + inv + pp + csv
    key_v = total - fund - loan - half - csv
    pool = {
        "no_trading": (m(key_v - trad), f"Also removes the {m(trad)} of trading securities. Securities held for sale in the near term are current assets."),
        "all_prepaid": (m(key_v - half), "Removes all of the prepaid insurance. The portion covering the next twelve months is a current asset."),
        "fund_left": (m(key_v + fund), f"Leaves the {m(fund)} bond retirement fund in cash. Cash set aside to retire long-term debt is not available for current operations."),
        "csv_left": (m(key_v + csv), f"Leaves the {m(csv)} cash surrender value in current assets. It is a long-term investment."),
        "loan_left": (m(key_v + loan), f"Leaves the {m(loan)} officer loan due in Year 4 in current receivables."),
    }
    key = (m(key_v), f"Correct. {m(total)} − {m(fund)} bond fund − {m(loan)} officer loan − {m(half)} second-year insurance − {m(csv)} cash surrender value.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year 1, classified balance sheet reports total current assets of {m(total)}: cash {m(cash)}, trading debt securities {m(trad)}, receivables {m(rec)}, inventory {m(inv)}, prepaid insurance {m(pp)}, and cash surrender value of officers' life insurance {m(csv)}. Supporting documents show that the cash includes {m(fund)} the board set aside in a fund to retire bonds maturing in Year 5; receivables include a {m(loan)} loan to an officer due in Year 4; and the prepaid insurance is a two-year policy ({m(half)} per year) that began January 1, Year 2, paid in December. After correcting the draft, what are {short}'s total current assets?""",
        choices, ans,
        f"""Current assets are those expected to be realized or consumed within a year (or the operating cycle). Reclassify to noncurrent: the {m(fund)} fund for bonds due in Year 5, the {m(loan)} officer loan due in Year 4, the {m(half)} of insurance covering Year 3, and the {m(csv)} cash surrender value, which is a long-term investment. Current assets = {m(cash - fund)} + {m(trad)} + {m(rec - loan)} + {m(inv)} + {m(half)} = {m(key_v)}.""",
    )


def operating_income(p):
    co, oi, ii, loss, wd, ie = (p[k] for k in ("co", "oi", "int_inc", "loss", "writedown", "int_exp"))
    short = co.split()[0]
    key_v = oi - ii - loss - wd + ie
    pool = {
        "ii_left": (m(key_v + ii), f"Leaves the {m(ii)} of interest income in sales revenue. For a manufacturer, interest income is nonoperating."),
        "wd_left": (m(key_v + wd), f"Leaves the {m(wd)} inventory write-down below operating income. Write-downs of inventory are part of cost of goods sold."),
        "loss_left": (m(key_v + loss), f"Leaves the {m(loss)} loss below operating income. Gains and losses on sales of long-lived assets are reported within income from operations."),
        "ie_left": (m(key_v - ie), f"Leaves the {m(ie)} of interest expense in general and administrative expenses. For a manufacturer, interest expense is nonoperating."),
    }
    key = (m(key_v), f"Correct. {m(oi)} − {m(ii)} interest income − {m(loss)} loss on sale − {m(wd)} inventory write-down + {m(ie)} interest expense.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s draft multi-step income statement reports operating income of {m(oi)}. Reviewing the supporting schedules, you find: (1) sales revenue includes {m(ii)} of interest earned on notes receivable; (2) a {m(loss)} loss on the sale of warehouse equipment is reported in other expenses, below operating income; (3) a {m(wd)} write-down of obsolete inventory is also reported in other expenses; and (4) general and administrative expenses include {m(ie)} of interest expense on a bank loan. {short} is a manufacturer. After correcting the draft, what is {short}'s operating income?""",
        choices, ans,
        f"""Corrections: interest income (−{m(ii)}) and interest expense (+{m(ie)}) are nonoperating items for a manufacturer, so they move out of operating income. The loss on the sale of equipment (−{m(loss)}) and the inventory write-down (−{m(wd)}) are operating items that the draft placed below operating income. Operating income = {m(oi)} − {m(ii)} − {m(loss)} − {m(wd)} + {m(ie)} = {m(key_v)}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def measurement_alternative(p):
    co, cost, pct_, obs, cust, fv = (p[k] for k in ("co", "cost", "pct", "obs", "cust", "fv"))
    short = co.split()[0]
    assert obs > cost and fv < obs
    pool = {
        "from_cost": (m(cost - (obs - fv)), f"Measures the impairment from cost ({m(cost)} − {m(obs - fv)}). The June observable price change had already raised the carrying amount to {m(obs)}."),
        "cost": (m(cost), "Keeps cost, ignoring both the observable price change and the impairment."),
        "obs": (m(obs), "Records the June observable price change but not the November impairment."),
    }
    key = (m(fv), f"Correct. Adjusted up to {m(obs)} for the observable price change, then written down to its {m(fv)} fair value when impaired.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""In January, {co} pays {m(cost)} for {pct_}% of the shares of a private company whose shares have no readily determinable fair value, and elects the measurement alternative. In June, the investee sells identical shares to an unrelated investor in an orderly transaction at a price implying that {short}'s shares are worth {m(obs)}. In November, the investee loses its largest customer, which provided {cust}% of its revenue, and {short} estimates the shares' fair value at {m(fv)}. At what amount should {short} report the investment at year-end?""",
        choices, ans,
        f"""Under the measurement alternative, the investment is carried at cost less impairment, adjusted for observable price changes in orderly transactions for identical or similar securities. June: adjust to {m(obs)} (a {m(obs - cost)} gain in net income). November: impairment indicators require measuring the investment at fair value, {m(fv)} (an {m(obs - fv)} loss in net income). Year-end carrying amount = {m(fv)}.""",
    )


def property_dividend(p):
    co, cv, fv = (p[k] for k in ("co", "cv", "fv"))
    short = co.split()[0]
    gl = "gain" if fv > cv else "loss"
    d = abs(fv - cv)
    re_ = lambda x: f"{m(x)} decrease in retained earnings"
    pool = {
        "cv_none": (f"{re_(cv)}; no {gl}", "Records the dividend at the land's carrying amount. A nonreciprocal transfer of a nonmonetary asset to owners is recorded at fair value."),
        "fv_apic": (f"{re_(fv)}; no {gl} (the difference goes to paid-in capital)", f"The difference between fair value and carrying amount is {article_(gl)} {gl} on disposal of the land, not paid-in capital."),
        "cv_gl": (f"{re_(cv)}; {m(d)} {gl}", f"Recognizes the {gl} but charges retained earnings only the land's carrying amount. The dividend is recorded at the fair value distributed."),
    }
    key = (f"{re_(fv)}; {m(d)} {gl}", f"Correct. The land is remeasured to its {m(fv)} fair value, recognizing {article_(gl)} {m(d)} {gl}, and the dividend is recorded at fair value.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: (dollars_in(c[0]), c[0]))
    return variant(
        f"""{co} declares a property dividend of a parcel of land to its shareholders. The land's carrying amount is {m(cv)}, and its fair value on the declaration date is {m(fv)}; the fair value does not change before distribution. What does {short} record for the dividend?""",
        choices, ans,
        f"""A property dividend is a nonreciprocal transfer to owners recorded at the fair value of the asset distributed. {short} remeasures the land to {m(fv)}, recognizing {article_(gl)} {m(d)} {gl} in net income, and debits retained earnings for {m(fv)} (credit property dividends payable, later settled by distributing the land).""",
    )


def article_(word):
    return "a"


# ── Area III ─────────────────────────────────────────────────────────────


def prepaid_error(p):
    co, paid, yrs, t = (p[k] for k in ("co", "paid", "years", "t"))
    short = co.split()[0]
    a = whole(D(paid) / yrs)
    re_v, ni_v = net(paid - a, t), net(a, t)
    both = lambda x, y, word="decrease": (
        f"{m(x)} increase to January 1, Year 2, retained earnings; "
        + (f"{m(y)} {word} to Year 2 net income" if y else "$0 change to Year 2 net income"))
    pool = {
        "no_y2": (both(re_v, 0), f"Gets the prior-period adjustment right but records no Year 2 insurance expense. One year of the policy, {m(a)}, belongs in Year 2."),
        "no_tax": (both(paid - a, a), f"Leaves out the {t}% tax effect."),
        "all_over": (both(net(paid, t), 0), f"Treats all {m(paid)} as overstated Year 1 expense. One year of coverage, {m(a)}, was a proper Year 1 expense."),
        "y2_sign": (both(re_v, ni_v, "increase"), "Gets the prior-period adjustment right but treats the Year 2 insurance expense as an increase to income. Recording the expense lowers Year 2 net income."),
    }
    key = (both(re_v, ni_v), f"Correct. Year 1 expense was overstated by {m(paid - a)} ({m(re_v)} after tax); Year 2 needs {m(a)} of expense ({m(ni_v)} after tax).")
    choices, ans = pick(pool, key, p["use"], order=lambda c: (dollars_in(c[0]), c[0]))
    return variant(
        f"""On January 1, Year 1, {co} paid {m(paid)} for a {WORDS[yrs]}-year insurance policy and charged the full amount to Year 1 insurance expense; Year 1 statements were issued that way. Before closing its Year 2 books, {short} discovers the error. It has recorded no insurance expense in Year 2. {short}'s tax rate is {t}% for all effects, and it presents single-year statements. What are the effects of correcting the error?""",
        choices, ans,
        f"""{short} should have expensed {m(a)} a year. Year 1 expense was overstated by {m(paid - a)}, so Year 1 net income was understated by {m(re_v)} after tax, and January 1, Year 2, retained earnings is increased by {m(re_v)} as a prior-period adjustment (with prepaid insurance of {m(paid - a)}). Year 2 then records {m(a)} of insurance expense, reducing Year 2 net income by {m(ni_v)} after tax.""",
    )


def gifts_in_kind(p):
    org, food, fac, shares, art = (p[k] for k in ("org", "food", "facility", "shares", "art"))
    short = org.split()[0]
    key_v = food + fac + shares
    pool = {
        "no_fa": (m(key_v - fac), "Omits the donated use of the warehouse. Contributed use of facilities is recognized at fair value as revenue and expense."),
        "art_no_fa": (m(key_v - fac + art), f"Recognizes the painting but omits the donated use of the warehouse. The collection item is not recognized under {short}'s policy, and contributed use of facilities is."),
        "plus_art": (m(key_v + art), "Also recognizes the painting. An entity that does not capitalize a qualifying collection does not recognize contributed collection items as revenue."),
        "no_food": (m(key_v - food), f"Omits the donated food because {short} will give it away. Contributed goods are recognized at fair value when received, even if they will be distributed."),
    }
    key = (m(key_v), f"Correct. {m(food)} of food + {m(fac)} of donated facilities + {m(shares)} of shares.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, receives: donated food with a fair value of {m(food)} to distribute; free use of a warehouse for the year, which would otherwise rent for {m(fac)}; publicly traded shares worth {m(shares)}; and a painting worth {m(art)} that it adds to a collection held for public exhibition, which it protects and preserves, and whose sale proceeds would go only to new collection items. {short}'s policy is not to capitalize collections. What contribution revenue should {short} recognize for Year 1?""",
        choices, ans,
        f"""Contributions of food, use of facilities and securities are recognized at fair value: {m(food)} + {m(fac)} + {m(shares)} = {m(key_v)} (contributed nonfinancial assets are presented separately under ASU 2020-07). Works of art added to a collection that meets the collection criteria need not be recognized, and under {short}'s policy they are not.""",
    )


def material_right(p):
    co, price, disc, cap, q = (p[k] for k in ("co", "price", "disc", "cap", "redeem"))
    short = co.split()[0]
    face = whole(D(cap) * disc / 100)
    ssp = whole(D(cap) * disc / 100 * q / 100)
    alloc = lambda s: rd(D(price) * price / (price + s))
    key_v = alloc(ssp)
    pool = {
        "full": (m(price - face), f"Subtracts the full {m(face)} voucher value ({disc}% × {m(cap)}) without allocating the price or adjusting for expected redemptions."),
        "sub_ssp": (m(price - ssp), f"Subtracts the voucher's {m(ssp)} standalone selling price directly. The {m(price)} price is allocated between the product and the voucher by relative standalone selling price."),
        "ignore": (m(price), "Ignores the voucher. A discount not available to other customers is a material right, a separate performance obligation."),
        "no_redeem": (m(alloc(face)), f"Leaves out the expected redemption rate. The voucher's standalone selling price reflects the {q}% of vouchers expected to be used."),
    }
    key = (m(key_v), f"Correct. Voucher standalone selling price = {m(cap)} × {disc}% × {q}% = {m(ssp)}; product revenue = {m(price)} × {m(price)} ÷ {m(price + ssp)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} sells a product for {m(price)}, its standalone selling price, and gives the customer a voucher for {disc}% off any future purchase of up to {m(cap)} within a year. {short} offers no similar discount to other customers. It expects {q}% of vouchers to be redeemed, on purchases averaging {m(cap)}. How much revenue should {short} recognize when it delivers the product?""",
        choices, ans,
        f"""The voucher gives a material right because the discount is not offered to other customers, so it is a separate performance obligation. Its standalone selling price reflects the discount and the likelihood of redemption: {m(cap)} × {disc}% × {q}% = {m(ssp)}. Allocating the {m(price)} price: product {m(price)} × {n(price)} ÷ {n(price + ssp)} = {m(key_v)}; voucher {m(price - key_v)}, recognized when redeemed or when it expires.""",
    )


FAMILIES = {
    "far-changes-in-equity-0002": (changes_in_equity, [
        dict(co="Faye Inc.", bre=800000, ni=250000, gain=30000, split=100000, div=40000, use=["split_left", "oci_left", "no_div"]),
        dict(co="Gilbert Inc.", bre=1200000, ni=380000, gain=45000, split=150000, div=60000, use=["draft", "split_left", "no_div"]),
        dict(co="Ingle Inc.", bre=500000, ni=160000, gain=20000, split=50000, div=35000, use=["split_left", "oci_left", "no_div"]),
        dict(co="Jessup Inc.", bre=950000, ni=300000, gain=35000, split=120000, div=50000, use=["oci_left", "no_div", "draft"]),
    ]),
    "far-nfp-statement-of-activities-0001": (nfp_activities, [
        dict(org="Cedar Clinic", cu=500000, cr=100000, fees=200000, rel=150000, inv=20000, prog=600000, mg=120000, fr=60000, use=["plus_cr", "no_rel", "prog_only"]),
        dict(org="Dogwood Clinic", cu=700000, cr=150000, fees=260000, rel=180000, inv=35000, prog=820000, mg=150000, fr=70000, use=["no_rel", "no_inv", "plus_cr"]),
        dict(org="Evergreen Clinic", cu=400000, cr=80000, fees=150000, rel=120000, inv=25000, prog=520000, mg=110000, fr=40000, use=["plus_cr", "no_rel", "prog_only"]),
        dict(org="Foxglove Clinic", cu=600000, cr=120000, fees=240000, rel=100000, inv=30000, prog=700000, mg=140000, fr=80000, use=["no_inv", "plus_cr", "prog_only"]),
    ]),
    "far-cash-flows-0005": (investing_section, [
        dict(co="Brenner Co.", equip=250000, note=100000, afs=90000, intdiv=12000, loan=40000, collected=10000, trading=30000, use=["keep_trading", "keep_note", "draft"]),
        dict(co="Calloway Co.", equip=400000, note=150000, afs=120000, intdiv=18000, loan=60000, collected=20000, trading=45000, use=["keep_int", "keep_trading", "keep_note"]),
        dict(co="Dorsey Co.", equip=180000, note=60000, afs=40000, intdiv=9000, loan=25000, collected=5000, trading=20000, use=["keep_trading", "keep_note", "draft"]),
        dict(co="Easton Co.", equip=320000, note=120000, afs=70000, intdiv=14000, loan=50000, collected=15000, trading=35000, use=["keep_int", "keep_note", "draft"]),
    ]),
    "far-eps-basic-0001": (basic_eps, [
        dict(co="Crane Corp.", s0=100000, issued=20000, sd=10, treasury=6000, ni=500000, pref_par=1000000, pref_rate=5, use=["sd_july", "year_end", "no_pref"]),
        dict(co="Draper Corp.", s0=200000, issued=40000, sd=5, treasury=12000, ni=900000, pref_par=2000000, pref_rate=6, use=["sd_july", "no_sd", "no_pref"]),
        dict(co="Elgin Corp.", s0=150000, issued=30000, sd=20, treasury=9000, ni=600000, pref_par=500000, pref_rate=8, use=["year_end", "no_pref", "sd_july"]),
        dict(co="Fairley Corp.", s0=80000, issued=16000, sd=10, treasury=4000, ni=420000, pref_par=600000, pref_rate=7, use=["sd_july", "no_sd", "no_pref"]),
    ]),
    "far-consolidated-statements-0003": (intercompany_equipment, [
        dict(par="Pike Corp.", sub="Sully Inc.", price=90000, cv=60000, life=5, pni=400000, sni=150000, use=["dep_wrong", "gain_only", "draft"]),
        dict(par="Rowe Corp.", sub="Stamford Inc.", price=150000, cv=110000, life=4, pni=620000, sni=230000, use=["gain_only", "draft", "dep_only"]),
        dict(par="Tilden Corp.", sub="Upham Inc.", price=120000, cv=70000, life=10, pni=500000, sni=180000, use=["dep_wrong", "gain_only", "draft"]),
        dict(par="Walcott Corp.", sub="Yarrow Inc.", price=200000, cv=125000, life=5, pni=900000, sni=300000, use=["gain_only", "draft", "dep_only"]),
    ]),
    "far-balance-sheet-0002": (current_assets, [
        dict(co="Keel Co.", cash=150000, fund=60000, trading=80000, rec=300000, loan=50000, inv=400000, prepaid=20000, csv=50000, use=["no_trading", "all_prepaid", "fund_left"]),
        dict(co="Lorne Co.", cash=220000, fund=80000, trading=60000, rec=410000, loan=35000, inv=520000, prepaid=30000, csv=70000, use=["all_prepaid", "loan_left", "csv_left"]),
        dict(co="Marlow Co.", cash=90000, fund=40000, trading=120000, rec=200000, loan=25000, inv=260000, prepaid=16000, csv=30000, use=["fund_left", "csv_left", "loan_left"]),
        dict(co="Nesbit Co.", cash=300000, fund=120000, trading=50000, rec=500000, loan=60000, inv=700000, prepaid=24000, csv=90000, use=["all_prepaid", "loan_left", "csv_left"]),
    ]),
    "far-income-statement-0002": (operating_income, [
        dict(co="Lund Co.", oi=500000, int_inc=25000, loss=40000, writedown=30000, int_exp=15000, use=["ii_left", "wd_left", "loss_left"]),
        dict(co="Mayfield Co.", oi=800000, int_inc=35000, loss=55000, writedown=20000, int_exp=45000, use=["ie_left", "wd_left", "loss_left"]),
        dict(co="Norwood Co.", oi=350000, int_inc=12000, loss=28000, writedown=45000, int_exp=8000, use=["ii_left", "loss_left", "wd_left"]),
        dict(co="Oakley Co.", oi=620000, int_inc=30000, loss=70000, writedown=25000, int_exp=20000, use=["ie_left", "ii_left", "loss_left"]),
    ]),
    "far-investments-equity-securities-0001": (measurement_alternative, [
        dict(co="Iredale Co.", cost=400000, pct=5, obs=460000, cust=40, fv=380000, use=["from_cost", "cost", "obs"]),
        dict(co="Jolley Co.", cost=250000, pct=8, obs=310000, cust=35, fv=270000, use=["from_cost", "cost", "obs"]),
        dict(co="Kinsey Co.", cost=600000, pct=4, obs=680000, cust=45, fv=520000, use=["from_cost", "cost", "obs"]),
        dict(co="Loftus Co.", cost=150000, pct=10, obs=190000, cust=30, fv=165000, use=["from_cost", "cost", "obs"]),
    ]),
    "far-property-dividend-0001": (property_dividend, [
        dict(co="Noble Corp.", cv=70000, fv=100000, use=["cv_none", "fv_apic", "cv_gl"]),
        dict(co="Ormond Corp.", cv=150000, fv=120000, use=["cv_none", "fv_apic", "cv_gl"]),
        dict(co="Parrish Corp.", cv=45000, fv=80000, use=["cv_none", "fv_apic", "cv_gl"]),
        dict(co="Quentin Corp.", cv=260000, fv=200000, use=["cv_none", "fv_apic", "cv_gl"]),
    ]),
    "far-accounting-errors-0004": (prepaid_error, [
        dict(co="Pollard Co.", paid=36000, years=3, t=25, use=["no_y2", "no_tax", "all_over"]),
        dict(co="Quimby Co.", paid=60000, years=4, t=21, use=["y2_sign", "no_tax", "all_over"]),
        dict(co="Radley Co.", paid=48000, years=2, t=30, use=["no_y2", "no_tax", "all_over"]),
        dict(co="Saxon Co.", paid=90000, years=5, t=25, use=["no_y2", "y2_sign", "all_over"]),
    ]),
    "far-nfp-gifts-in-kind-0001": (gifts_in_kind, [
        dict(org="Upton Food Bank", food=40000, facility=24000, shares=15000, art=50000, use=["no_fa", "art_no_fa", "plus_art"]),
        dict(org="Kendall Food Bank", food=65000, facility=30000, shares=20000, art=40000, use=["no_food", "no_fa", "plus_art"]),
        dict(org="Linden Food Bank", food=25000, facility=36000, shares=10000, art=90000, use=["no_fa", "art_no_fa", "plus_art"]),
        dict(org="Maple Food Bank", food=50000, facility=18000, shares=30000, art=60000, use=["no_food", "no_fa", "art_no_fa"]),
    ]),
    "far-revenue-material-right-0001": (material_right, [
        dict(co="Stark Co.", price=1000, disc=40, cap=500, redeem=80, use=["full", "sub_ssp", "ignore"]),
        dict(co="Tarrant Co.", price=2000, disc=30, cap=1000, redeem=60, use=["full", "no_redeem", "sub_ssp"]),
        dict(co="Upland Co.", price=600, disc=50, cap=300, redeem=70, use=["full", "sub_ssp", "ignore"]),
        dict(co="Vickery Co.", price=1500, disc=40, cap=600, redeem=50, use=["full", "no_redeem", "sub_ssp"]),
    ]),
}

if __name__ == "__main__":
    run(FAMILIES, CONTENT)
