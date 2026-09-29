"""FAR variants 06: three extra versions for 11 numeric items, 3 from FAR batch 03 and 8 from batch 02.

Method as in far-variants-03.py (shared helpers in variants.py). Left without variants, because every wrong
answer falls on the same side of the key so its letter can't move: far-debt-covenant-0001 (every error lowers
the ratio) and far-accounting-errors-0002 (one amount with direction labels).

Run: python3 scripts/batches/far-variants-06.py   See docs/reviews/far-variants-06.md.
"""
import os
from decimal import Decimal as D

from common import variant
from variants import WORDS, m, n, pick, rd, run, whole

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def pc(x):
    """A fraction as a whole percent (asserting it is whole)."""
    return int(whole(D(x) * 100))


# ── Area I ───────────────────────────────────────────────────────────────


def current_liabilities(p):
    co, ap, wg, note, div, inst, count, od = (p[k] for k in ("co", "ap", "wages", "note", "div", "inst", "count", "od"))
    short = co.split()[0]
    draft = ap + wg + note + div
    key_v = ap + wg + inst + od
    pool = {
        "no_inst": (m(key_v - inst), f"Reclassifies the note and removes the dividend but leaves the {m(inst)} bond installment due January 15, Year 2, in noncurrent liabilities."),
        "keep_div": (m(key_v + div), f"Keeps the {m(div)} dividend. A dividend declared after the balance sheet date is not a liability at year-end."),
        "netted": (m(key_v - od), f"Leaves the {m(od)} overdraft netted against cash. An overdraft at a bank where {short} has no other accounts cannot be offset; it is a current liability."),
        "keep_note": (m(key_v + note), f"Keeps the {m(note)} note in current liabilities. A noncancelable refinancing agreement signed before the statements are issued lets it be classified as noncurrent."),
    }
    key = (m(key_v), f"Correct. {m(ap)} + {m(wg)} + {m(inst)} current bond installment + {m(od)} overdraft. The refinanced note is noncurrent and the dividend is not yet a liability.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31, Year 1, financial statements will be issued on March 1, Year 2. Its draft classified balance sheet reports total current liabilities of {m(draft)}: accounts payable {m(ap)}, accrued wages {m(wg)}, a note payable due June 30, Year 2, of {m(note)}, and dividends payable of {m(div)}. Supporting documents show: (1) on February 10, Year 2, {short} signed an agreement with a bank to refinance the {m(note)} note with a five-year loan; the agreement cannot be cancelled by the bank before Year 5, the bank is financially able to honor it, and {short} is in compliance with its terms; (2) the board declared the {m(div)} cash dividend on January 20, Year 2; (3) {short}'s {m(inst * count)} of serial bonds, all shown as noncurrent, are repaid in {WORDS[count]} annual installments of {m(inst)} beginning January 15, Year 2; and (4) {short} netted a {m(od)} overdraft at Bank B, where it has no other accounts, against its cash at Bank A. After correcting the draft, what are {short}'s total current liabilities?""",
        choices, ans,
        f"""Four corrections. (1) A short-term obligation is excluded from current liabilities if, before the statements are issued, the entity enters into a financing agreement that permits long-term refinancing, is noncancelable for more than a year, is with a capable lender, and is not in violation. The {m(note)} note meets these conditions, so it moves to noncurrent. (2) A dividend becomes a liability when declared; the January 20 declaration is not a Year 1 liability. (3) The {m(inst)} bond installment due within a year is current. (4) An overdraft at a bank where the entity has no other accounts cannot be offset against cash elsewhere; it is a current liability. Current liabilities = {m(ap)} + {m(wg)} + {m(inst)} + {m(od)} = {m(key_v)}.""",
    )


def continuing_ops(p):
    co, draft, dl, rev, fx, hur = (p[k] for k in ("co", "draft", "div_loss", "rev_pct", "fx", "hurricane"))
    short = co.split()[0]
    key_v = draft + dl - fx - hur
    pool = {
        "div_left": (m(key_v - dl), f"Corrects the exchange loss and the hurricane loss but leaves the division's loss in continuing operations. Selling the company's only operation on a continent, which produced {rev}% of revenue, is a strategic shift with a major effect, so it is reported in discontinued operations."),
        "fx_oci": (m(key_v + fx), f"Leaves the {m(fx)} exchange loss in OCI. A remeasurement loss on a foreign-currency payable is a transaction loss reported in income."),
        "double_div": (m(key_v - 2 * dl), f"Subtracts the division's {m(dl)} loss again instead of removing it from continuing operations. Moving a loss to discontinued operations raises income from continuing operations."),
        "hurr_left": (m(key_v + hur), f"Leaves the {m(hur)} hurricane loss below continuing operations as an extraordinary item. ASU 2015-01 eliminated extraordinary items, so it is reported within continuing operations."),
    }
    key = (m(key_v), f"Correct. {m(draft)} + {m(dl)} division loss moved to discontinued operations − {m(fx)} exchange loss − {m(hur)} hurricane loss.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 1 multi-step income statement reports income from continuing operations before income taxes of {m(draft)}. Reviewing the supporting schedules, you find: (1) continuing operations include a {m(dl)} pretax operating loss of {short}'s South American division, which is {short}'s only operation on that continent and produced {rev}% of consolidated revenue; in November the board approved a plan to sell the division, began actively marketing it at a reasonable price, and expects a sale within a year; (2) a {m(fx)} loss from remeasuring a yen-denominated account payable at the year-end exchange rate is reported in other comprehensive income; and (3) a {m(hur)} hurricane loss, which {short} considers both unusual and infrequent, is reported below income from continuing operations as an extraordinary item. What is {short}'s corrected income from continuing operations before income taxes?""",
        choices, ans,
        f"""(1) The division is a component that meets the held-for-sale criteria (approved plan, actively marketed at a reasonable price, sale expected within a year) and its disposal is a strategic shift with a major effect (exiting a major geographic area that produced {rev}% of revenue), so its results move to discontinued operations: add back {m(dl)}. (2) Remeasuring a foreign-currency payable produces a transaction loss that belongs in income: subtract {m(fx)}. (3) Since ASU 2015-01 there is no extraordinary-item classification; the hurricane loss is reported within continuing operations: subtract {m(hur)}. Corrected: {m(draft)} + {m(dl)} − {m(fx)} − {m(hur)} = {m(key_v)}.""",
    )


def retained_earnings(p):
    co, bre, ni, cd, sds, sdp, par, mkt, ts, pre, post = (
        p[k] for k in ("co", "bre", "ni", "cash_div", "sd_shares", "sd_pct", "par", "mkt", "treasury", "err_pre", "err_post"))
    short = co.split()[0]
    sd_par, sd_mkt = sds * par, sds * mkt
    draft = bre + ni - cd - sd_par - ts
    key_v = bre - post + ni - cd - sd_mkt
    pool = {
        "ts_left": (m(key_v - ts), "Fixes the stock dividend and the prior-period error but still charges the treasury stock purchase to retained earnings. Under the cost method, treasury stock is a separate deduction from total equity."),
        "no_ppa": (m(key_v + post), "Omits the prior-period adjustment. The Year 1 error is corrected by restating beginning retained earnings, net of tax."),
        "sd_par": (m(key_v + sd_mkt - sd_par), "Records the stock dividend at par. A distribution of less than 20–25% of the shares outstanding is recorded at the shares' market value."),
        "pretax_ppa": (m(key_v - (pre - post)), f"Adjusts beginning retained earnings by the {m(pre)} pretax error. The prior-period adjustment is net of tax ({m(post)})."),
    }
    key = (m(key_v), f"Correct. {m(bre)} − {m(post)} prior-period adjustment + {m(ni)} − {m(cd)} − {m(sd_mkt)} stock dividend at market value.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 statement of changes in equity reports ending retained earnings of {m(draft)}, computed as beginning retained earnings of {m(bre)} (as previously reported), plus net income of {m(ni)}, less cash dividends of {m(cd)}, less a {m(sd_par)} stock dividend, less {m(ts)} for treasury stock. Supporting documents show: (1) the stock dividend was {n(sds)} shares of {m(par)} par common stock ({sdp}% of the shares outstanding), distributed when the market price was {m(mkt)} per share; (2) {short} paid {m(ts)} to reacquire its own shares and holds them in treasury under the cost method; and (3) in Year 2 {short} discovered that it had omitted {m(pre)} of depreciation in Year 1, an error with an after-tax effect of {m(post)}. Year 2 net income is correct. What is {short}'s corrected ending retained earnings for Year 2?""",
        choices, ans,
        f"""(1) A stock dividend of {sdp}% is small, so retained earnings is charged at market value: {n(sds)} × {m(mkt)} = {m(sd_mkt)}, not the {m(sd_par)} par. (2) Treasury stock under the cost method is shown as a deduction from total equity; buying it does not reduce retained earnings. (3) The omitted Year 1 depreciation is a prior-period error, corrected by reducing beginning retained earnings by its after-tax effect of {m(post)}. Corrected ending retained earnings = {m(bre)} − {m(post)} + {m(ni)} − {m(cd)} − {m(sd_mkt)} = {m(key_v)}.""",
    )


def intercompany_inventory(p):
    par, sub, cost, sale, resold, hs, hc, vs, vc = (
        p[k] for k in ("par", "sub", "cost", "sale", "resold", "h_sales", "h_cogs", "v_sales", "v_cogs"))
    ps, ss = par.split()[0], sub.split()[0]
    held = 100 - resold
    profit = sale - cost
    up = whole(D(profit) * held / 100)
    draft_gp = hs + vs - hc - vc
    key_v = draft_gp - up
    pool = {
        "no_purch": (m(draft_gp - sale), f"Eliminates the {m(sale)} of intercompany sales without eliminating the matching intercompany purchases from cost of goods sold."),
        "all_profit": (m(draft_gp - profit), f"Eliminates {ps}'s entire {m(profit)} profit on the intercompany sale. Only the profit in inventory {ss} still holds ({held}%) is unrealized."),
        "draft": (m(draft_gp), f"Accepts the draft. Eliminating intercompany sales and purchases leaves gross profit unchanged, but the profit in {ss}'s ending inventory must still be removed."),
        "sold_profit": (m(draft_gp - (profit - up)), f"Eliminates the profit on the {resold}% {ss} resold. That profit was realized in sales to outsiders; only the {held}% still in {ss}'s inventory is unrealized."),
    }
    key = (m(key_v), f"Correct. The draft's {m(draft_gp)} less {m(up)} of unrealized profit in {ss}'s ending inventory ({held}% × {m(profit)}).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{par} owns 100% of {sub} During Year 1, {ps} sold inventory that cost it {m(cost)} to {ss} for {m(sale)}. By December 31, {ss} had resold {resold}% of that inventory to outside customers and still held the rest. {ps} reported sales of {m(hs)} and cost of goods sold of {m(hc)}; {ss} reported sales of {m(vs)} and cost of goods sold of {m(vc)}. {ps}'s draft consolidated income statement for Year 1 reports sales of {m(hs + vs)} and cost of goods sold of {m(hc + vc)}. After any corrections needed, what is consolidated gross profit?""",
        choices, ans,
        f"""The draft simply adds the two companies' amounts. Eliminate the {m(sale)} intercompany sale from both sales and cost of goods sold (no effect on gross profit), then remove the unrealized profit in {ss}'s ending inventory: {ps}'s markup is {m(profit)} on {m(sale)} of goods, and {held}% remains unsold, so {m(up)} is deferred by increasing cost of goods sold. Consolidated sales {m(hs + vs - sale)} − cost of goods sold {m(hc + vc - sale + up)} = {m(key_v)}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def bank_rec_balance(p):
    co, book, dit, oc, sc, nsf, actual, rec, note = (
        p[k] for k in ("co", "book", "dit", "oc", "sc", "nsf", "actual", "recorded", "note"))
    short = co.split()[0]
    diff = actual - rec
    key_v = book - sc - nsf - diff + note
    bank = key_v - dit + oc
    pool = {
        "no_note": (m(key_v - note), f"Omits the {m(note)} note the bank collected, which {short} has not yet recorded."),
        "wrong_dir": (m(key_v + 2 * diff), f"Corrects check #412 in the wrong direction. The check was {m(actual)} but recorded as {m(rec)}, so the ledger must be reduced by {m(diff)}."),
        "nsf_back": (m(key_v + 2 * nsf), "Adds back the NSF check. A returned customer check reduces cash and reinstates the receivable."),
        "book_timing": (m(book + dit - oc), "Adjusts the general ledger balance for the deposits in transit and outstanding checks. Those items reconcile the bank balance, not the books."),
    }
    key = (m(key_v), f"Correct. Bank: {m(bank)} + {m(dit)} − {m(oc)}. Books: {m(book)} − {m(sc)} − {m(nsf)} − {m(diff)} + {m(note)}. Both equal {m(key_v)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31 bank statement shows a balance of {m(bank)}, and its general ledger cash account shows {m(book)}. The controller finds: deposits in transit of {m(dit)}; outstanding checks of {m(oc)}; a {m(sc)} bank service charge not yet recorded; a customer's {m(nsf)} check returned with the statement marked NSF; check #412, written to a supplier for {m(actual)} and cleared by the bank at {m(actual)}, recorded in the ledger as {m(rec)}; and a note receivable of {m(note)}, including interest, that the bank collected for {short} and credited to its account. What is {short}'s correct cash balance at December 31?""",
        choices, ans,
        f"""Reconcile both sides to the correct balance. Bank side: {m(bank)} + {m(dit)} deposits in transit − {m(oc)} outstanding checks = {m(key_v)}. Book side: {m(book)} − {m(sc)} service charge − {m(nsf)} NSF check − {m(diff)} understatement of check #412 + {m(note)} note collected = {m(key_v)}. The book-side items all require general ledger adjustments; the bank-side items do not.""",
    )


def cash_equivalents(p):
    co, chk, sav, petty, tb1, tb2, cd, sink, od = (p[k] for k in ("co", "chk", "sav", "petty", "tb1", "tb2", "cd", "sink", "od"))
    short = co.split()[0]
    key_v = chk + sav + petty + tb1
    pool = {
        "plus_cd": (m(key_v + cd), "Includes the six-month certificate of deposit. Its original maturity is more than three months, so it is a short-term investment, not a cash equivalent."),
        "plus_sink": (m(key_v + sink), f"Includes the {m(sink)} sinking fund. Cash restricted for debt retirement is not available for current operations and is reported separately."),
        "plus_tb2": (m(key_v + tb2), "Includes the Treasury bill bought June 1. Cash equivalents must have an original maturity to the holder of three months or less; this bill had about nine."),
        "net_od": (m(key_v - od), f"Nets the {m(od)} overdraft at another bank against cash. An overdraft at a bank where the entity has no other accounts is a current liability."),
    }
    key = (m(key_v), f"Correct. {m(chk)} + {m(sav)} + {m(petty)} + the {m(tb1)} Treasury bill bought with a three-month maturity. The overdraft at another bank is a liability and is not netted.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, Year 1, {co} has: checking account {m(chk)}; savings account {m(sav)}; petty cash {m(petty)}; a Treasury bill bought December 1, Year 1, that matures February 28, Year 2, {m(tb1)}; a Treasury bill bought June 1, Year 1, that matures February 28, Year 2, {m(tb2)}; a six-month certificate of deposit maturing March 31, Year 2, {m(cd)}; {m(sink)} held by a trustee in a bond sinking fund; and a {m(od)} overdraft in an account at a different bank. What amount should {short} report as cash and cash equivalents?""",
        choices, ans,
        f"""Cash equivalents are short-term, highly liquid investments with original maturities to the holder of three months or less. The December 1 Treasury bill qualifies; the June 1 bill (about nine months when bought) and the six-month CD do not, even though little time remains. The sinking fund is restricted and reported separately, and the overdraft at another bank is a current liability. Cash and cash equivalents = {m(chk)} + {m(sav)} + {m(petty)} + {m(tb1)} = {m(key_v)}.""",
    )


def inventory_rec(p):
    co, sub, transit, consign, unposted, fobd = (p[k] for k in ("co", "sub", "transit", "consign", "unposted", "fob_dest"))
    short = co.split()[0]
    correct = sub + transit - consign + fobd
    gl = sub - consign - unposted
    key_v = transit + unposted + fobd
    assert correct == gl + key_v and correct > sub
    pool = {
        "sub_adj": (m(correct - sub), f"Computes the adjustment the subledger needs ({m(sub)} to {m(correct)}), not the general ledger."),
        "no_u": (m(key_v - unposted), f"Omits the {m(unposted)} purchase that is in the subledger but was never posted to the general ledger."),
        "plus_c": (m(key_v + consign), f"Treats the {m(consign)} of consigned goods as {short}'s. Goods held on consignment belong to the consignor."),
        "no_f": (m(key_v - fobd), f"Leaves out the {m(fobd)} of goods shipped FOB destination. Title had not passed at year-end, so they are still {short}'s inventory."),
    }
    key = (m(key_v), f"Correct. Correct inventory is {m(correct)}; {m(correct)} − {m(gl)} = {m(key_v)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s perpetual inventory subledger totals {m(sub)}, but its general ledger inventory account shows {m(gl)}. Investigating, the controller finds: (1) goods costing {m(transit)} that a supplier shipped FOB shipping point on December 28 arrived January 3 and are recorded in neither record; (2) the subledger includes {m(consign)} of goods {short} holds on consignment for Mayer Co.; (3) a {m(unposted)} purchase received December 20 is in the subledger, but the supplier's invoice was never posted to the general ledger; and (4) goods costing {m(fobd)} shipped to a customer FOB destination on December 31, which arrived January 4, were removed from both records when shipped and the sale was recorded. By how much must {short} increase its general ledger inventory balance?""",
        choices, ans,
        f"""Correct inventory = subledger {m(sub)} + {m(transit)} in transit (title passed at shipment) − {m(consign)} consigned goods (owned by Mayer) + {m(fobd)} shipped FOB destination (title had not passed) = {m(correct)}. The general ledger is missing the in-transit goods, the unposted {m(unposted)} purchase, and the FOB-destination goods: {m(gl)} + {m(transit)} + {m(unposted)} + {m(fobd)} = {m(correct)}. The general ledger must be increased by {m(key_v)} (and the premature sale reversed).""",
    )


def patent_life(p):
    co, cost, legal, useful, yrs, rem = (p[k] for k in ("co", "cost", "legal", "useful", "yrs", "remaining"))
    short = co.split()[0]
    amort = whole(D(cost) / useful)
    ca = cost - yrs * amort
    key_v = whole(D(ca) / rem)
    yr = yrs + 1
    pool = {
        "orig": (m(amort), f"Keeps the original {useful}-year life. A revised estimate of useful life is applied from Year {yr} onward."),
        "total_life": (m(whole(D(cost) / (yrs + rem))), f"Spreads the original cost over the revised total life of {yrs + rem} years. A change in estimate is prospective: the remaining carrying amount is spread over the remaining life."),
        "legal": (m(whole(D(ca) / (legal - yrs))), f"Spreads the {m(ca)} carrying amount over the {legal - yrs} years of legal life remaining. Amortization uses the shorter of legal and useful life."),
        "cost_rem": (m(whole(D(cost) / rem)), f"Spreads the original {m(cost)} cost over the {rem} remaining years, ignoring the {WORDS[yrs]} years of amortization already recorded."),
    }
    key = (m(key_v), f"Correct. Carrying amount {m(cost)} − {yrs} × {m(amort)} = {m(ca)}, spread over the remaining {rem} years.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} buys a patent for {m(cost)}. The patent has {legal} years of legal life remaining, and {short} expects it to provide benefits for {useful} years. {short} amortizes it straight-line with no residual value. On January 1, Year {yr}, a competitor's new technology leads {short} to conclude that the patent will provide benefits for only {rem} more years; its future cash flows still exceed its carrying amount. What patent amortization expense should {short} recognize in Year {yr}?""",
        choices, ans,
        f"""A finite-lived intangible is amortized over the shorter of its legal and useful lives: {useful} years, {m(amort)} a year. After {WORDS[yrs]} years its carrying amount is {m(ca)}. The revised life is a change in accounting estimate, applied prospectively: {m(ca)} ÷ {rem} = {m(key_v)} a year from Year {yr}. The asset is recoverable, so there is no impairment.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def over_time(p):
    co, price, c1, e1, c2, e2 = (p[k] for k in ("co", "price", "c1", "e1", "c2", "e2"))
    short = co.split()[0]
    t1, t2 = c1 + e1, c2 + e2
    p1, p2 = D(c1) / t1, D(c2) / t2
    gp1 = whole(p1 * (price - t1))
    cum = whole(p2 * (price - t2))
    key_v = cum - gp1
    pts = pc(p2 - p1)
    pool = {
        "orig_est": (m(whole(D(c2) / t1 * (price - t1)) - gp1), f"Measures Year 2 progress against the original {m(t1)} cost estimate. Progress uses the updated {m(t2)} total estimate."),
        "pct_diff": (m(whole((p2 - p1) * (price - t1))), f"Applies the {pts}-point increase in percent complete to the original {m(price - t1)} profit estimate, ignoring the change in estimated profit."),
        "cum_only": (m(cum), f"Reports cumulative gross profit to date without subtracting the {m(gp1)} recognized in Year 1."),
        "pct_diff_new": (m(whole((p2 - p1) * (price - t2))), f"Applies the {pts}-point increase in percent complete to the revised {m(price - t2)} profit estimate. The catch-up recognizes {pc(p2)}% of the revised profit, less the Year 1 amount."),
    }
    key = (m(key_v), f"Correct. Cumulative profit {pc(p2)}% × {m(price - t2)} = {m(cum)}, less the {m(gp1)} recognized in Year 1.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} has a {m(price)} fixed-price contract to construct a building for a customer on the customer's land, recognizing revenue over time using costs incurred relative to total estimated costs. In Year 1 it incurred {m(c1)} of costs and estimated {m(e1)} more to complete. By the end of Year 2 it had incurred {m(c2)} in total and estimated {m(e2)} more to complete. What gross profit should {short} recognize in Year 2?""",
        choices, ans,
        f"""Year 1: {n(c1)} ÷ {n(t1)} = {pc(p1)}% complete; gross profit {pc(p1)}% × ({m(price)} − {m(t1)}) = {m(gp1)}. Year 2: the revised total cost is {m(t2)}, so progress is {n(c2)} ÷ {n(t2)} = {pc(p2)}% and estimated profit is {m(price - t2)}. Cumulative gross profit = {pc(p2)}% × {m(price - t2)} = {m(cum)}; Year 2 gross profit = {m(cum)} − {m(gp1)} = {m(key_v)}. The change in estimate is handled prospectively through the cumulative catch-up.""",
    )


def contributed_services(p):
    org, cpa, carp, greet, board = (p[k] for k in ("org", "cpa", "carpentry", "greeters", "board"))
    short = org.split()[0]
    key_v = cpa + carp
    pool = {
        "cpa_only": (m(cpa), "Recognizes only the specialized service. Services that create or enhance a nonfinancial asset are also recognized."),
        "cpa_board": (m(cpa + board), f"Recognizes the CPA's work and the board members' time. Governance by board members is not a specialized skill {short} would otherwise purchase."),
        "carp_only": (m(carp), f"Recognizes only the exhibit hall work. Specialized services, such as the CPA's, that {short} would otherwise purchase are also recognized."),
        "plus_greet": (m(key_v + greet), "Also recognizes the greeters' time. Services that neither require specialized skills nor create a nonfinancial asset are not recognized, even if they have a market value."),
    }
    key = (m(key_v), f"Correct. The CPA's specialized service ({m(cpa)}) and the carpentry that created a nonfinancial asset ({m(carp)}).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""During Year 1, volunteers gave {org}, a not-for-profit entity, these services: a CPA prepared its financial statements, which {short} would otherwise have paid {m(cpa)} for; carpenters built a permanent exhibit hall addition worth {m(carp)}; volunteer greeters worked at the entrance, time that would cost {m(greet)} at local wage rates; and board members spent time at meetings valued at {m(board)}. What amount should {short} recognize as contributed services revenue?""",
        choices, ans,
        f"""Contributed services are recognized only if they create or enhance nonfinancial assets, or require specialized skills, are provided by people with those skills, and would typically need to be purchased if not donated. The CPA's work ({m(cpa)}) and the carpentry on the addition ({m(carp)}) qualify. Greeters and board members do not. Contributed services revenue = {m(key_v)}.""",
    )


def rvg_liability(p):
    co, pay, yrs, g, e, r = (p[k] for k in ("co", "pay", "years", "guar", "expected", "rate"))
    short = co.split()[0]
    rr = D(r) / 100
    ann = rd((1 - (1 + rr) ** -yrs) / rr, "0.0001")
    single = rd((1 + rr) ** -yrs, "0.0001")
    pv = lambda x, f: rd(x * f)
    base = pv(pay, ann)
    owed = g - e
    key_v = base + pv(owed, single)
    pool = {
        "no_rvg": (m(base), f"Omits the residual value guarantee. The amount {short} expects to owe under the guarantee is a lease payment."),
        "full_rvg": (m(base + pv(g, single)), f"Includes the full {m(g)} guarantee. Only the amount probable of being owed ({m(g)} − {m(e)}) is a lease payment."),
        "undisc": (m(pay * yrs + owed), "Adds the undiscounted payments and expected guarantee payment. The liability is the present value of the lease payments."),
        "expected": (m(base + pv(e, single)), f"Discounts the {m(e)} expected residual value instead of the {m(owed)} {short} expects to owe under the guarantee."),
    }
    key = (m(key_v), f"Correct. {m(pay)} × {ann} = {m(base)}, plus the {m(owed)} expected to be owed under the guarantee × {single} = {m(pv(owed, single))}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} leases a machine for {WORDS[yrs]} years. It pays {m(pay)} at the end of each year and guarantees the lessor that the machine will be worth {m(g)} at the end of the lease; {short} expects its value then to be {m(e)}. The discount rate is {r}%, and present value factors at {r}% for {WORDS[yrs]} periods are {ann} for an ordinary annuity and {single} for a single sum. At what amount should {short} initially measure its lease liability?""",
        choices, ans,
        f"""Lease payments include the amount the lessee expects to owe under a residual value guarantee: {m(g)} guaranteed − {m(e)} expected value = {m(owed)}. Liability = {m(pay)} × {ann} + {m(owed)} × {single} = {m(base)} + {m(pv(owed, single))} = {m(key_v)}.""",
    )


FAMILIES = {
    "far-balance-sheet-0001": (current_liabilities, [
        dict(co="Corbin Co.", ap=180000, wages=40000, note=200000, div=25000, inst=50000, count=10, od=35000, use=["no_inst", "keep_div", "netted"]),
        dict(co="Everly Co.", ap=260000, wages=55000, note=300000, div=40000, inst=80000, count=10, od=20000, use=["no_inst", "keep_div", "keep_note"]),
        dict(co="Fordyce Co.", ap=120000, wages=30000, note=150000, div=15000, inst=25000, count=10, od=45000, use=["no_inst", "netted", "keep_div"]),
        dict(co="Gresham Co.", ap=400000, wages=70000, note=500000, div=60000, inst=100000, count=10, od=30000, use=["netted", "keep_div", "keep_note"]),
    ]),
    "far-income-statement-0001": (continuing_ops, [
        dict(co="Oberon Corp.", draft=900000, div_loss=150000, rev_pct=30, fx=40000, hurricane=70000, use=["div_left", "fx_oci", "double_div"]),
        dict(co="Pemberton Corp.", draft=1400000, div_loss=220000, rev_pct=25, fx=55000, hurricane=90000, use=["div_left", "fx_oci", "hurr_left"]),
        dict(co="Quayle Corp.", draft=600000, div_loss=80000, rev_pct=35, fx=25000, hurricane=45000, use=["double_div", "div_left", "fx_oci"]),
        dict(co="Radnor Corp.", draft=2000000, div_loss=300000, rev_pct=40, fx=80000, hurricane=120000, use=["div_left", "hurr_left", "fx_oci"]),
    ]),
    "far-changes-in-equity-0001": (retained_earnings, [
        dict(co="Pruitt Inc.", bre=1000000, ni=420000, cash_div=60000, sd_shares=10000, sd_pct=10, par=1, mkt=15, treasury=70000, err_pre=40000, err_post=30000, use=["ts_left", "no_ppa", "sd_par"]),
        dict(co="Quinlan Inc.", bre=2000000, ni=650000, cash_div=100000, sd_shares=20000, sd_pct=8, par=2, mkt=25, treasury=120000, err_pre=60000, err_post=45000, use=["ts_left", "pretax_ppa", "no_ppa"]),
        dict(co="Rourke Inc.", bre=600000, ni=250000, cash_div=40000, sd_shares=5000, sd_pct=5, par=1, mkt=12, treasury=50000, err_pre=20000, err_post=15000, use=["ts_left", "no_ppa", "sd_par"]),
        dict(co="Sherwood Inc.", bre=1500000, ni=500000, cash_div=80000, sd_shares=15000, sd_pct=10, par=1, mkt=20, treasury=90000, err_pre=80000, err_post=60000, use=["ts_left", "pretax_ppa", "sd_par"]),
    ]),
    "far-consolidated-statements-0002": (intercompany_inventory, [
        dict(par="Holt Corp.", sub="Vale Inc.", cost=150000, sale=200000, resold=70, h_sales=1000000, h_cogs=600000, v_sales=500000, v_cogs=300000, use=["no_purch", "all_profit", "draft"]),
        dict(par="Irving Corp.", sub="Jolliet Inc.", cost=240000, sale=300000, resold=60, h_sales=1800000, h_cogs=1100000, v_sales=900000, v_cogs=540000, use=["no_purch", "all_profit", "sold_profit"]),
        dict(par="Kenyon Corp.", sub="Lowell Inc.", cost=90000, sale=120000, resold=75, h_sales=700000, h_cogs=420000, v_sales=300000, v_cogs=180000, use=["no_purch", "all_profit", "draft"]),
        dict(par="Marlin Corp.", sub="Norton Inc.", cost=400000, sale=500000, resold=80, h_sales=2500000, h_cogs=1500000, v_sales=1200000, v_cogs=720000, use=["no_purch", "all_profit", "sold_profit"]),
    ]),
    "far-cash-bank-reconciliation-0001": (bank_rec_balance, [
        dict(co="Ridley Co.", book=45900, dit=6400, oc=9300, sc=60, nsf=1200, actual=540, recorded=450, note=750, use=["no_note", "wrong_dir", "nsf_back"]),
        dict(co="Sayre Co.", book=62400, dit=8200, oc=11050, sc=45, nsf=2300, actual=1260, recorded=1080, note=1500, use=["book_timing", "no_note", "wrong_dir"]),
        dict(co="Tabor Co.", book=21750, dit=3100, oc=4900, sc=30, nsf=850, actual=615, recorded=561, note=1020, use=["no_note", "wrong_dir", "nsf_back"]),
        dict(co="Varick Co.", book=88300, dit=12500, oc=15800, sc=75, nsf=3100, actual=2340, recorded=2070, note=2600, use=["book_timing", "no_note", "nsf_back"]),
    ]),
    "far-cash-equivalents-0001": (cash_equivalents, [
        dict(co="Fulton Corp.", chk=120000, sav=80000, petty=1000, tb1=50000, tb2=30000, cd=40000, sink=25000, od=8000, use=["plus_cd", "plus_sink", "plus_tb2"]),
        dict(co="Garrick Corp.", chk=180000, sav=60000, petty=2000, tb1=40000, tb2=55000, cd=30000, sink=45000, od=11000, use=["net_od", "plus_cd", "plus_tb2"]),
        dict(co="Hadden Corp.", chk=95000, sav=120000, petty=1500, tb1=70000, tb2=25000, cd=60000, sink=20000, od=18000, use=["plus_sink", "plus_tb2", "plus_cd"]),
        dict(co="Ingalls Corp.", chk=210000, sav=45000, petty=1000, tb1=35000, tb2=40000, cd=25000, sink=30000, od=8500, use=["net_od", "plus_sink", "plus_tb2"]),
    ]),
    "far-inventory-reconciliation-0001": (inventory_rec, [
        dict(co="Lassen Co.", sub=612000, transit=18000, consign=22000, unposted=28000, fob_dest=12000, use=["sub_adj", "no_u", "plus_c"]),
        dict(co="Tahoe Co.", sub=845000, transit=26000, consign=31000, unposted=41000, fob_dest=17000, use=["sub_adj", "no_u", "no_f"]),
        dict(co="Ukiah Co.", sub=410000, transit=12000, consign=15000, unposted=20000, fob_dest=9000, use=["sub_adj", "no_u", "plus_c"]),
        dict(co="Vallejo Co.", sub=1020000, transit=35000, consign=28000, unposted=52000, fob_dest=24000, use=["sub_adj", "no_f", "no_u"]),
    ]),
    "far-intangibles-patent-0001": (patent_life, [
        dict(co="Ivers Co.", cost=360000, legal=15, useful=12, yrs=3, remaining=5, use=["orig", "total_life", "legal"]),
        dict(co="Jessop Co.", cost=480000, legal=20, useful=16, yrs=4, remaining=6, use=["orig", "total_life", "cost_rem"]),
        dict(co="Kimball Co.", cost=240000, legal=14, useful=8, yrs=2, remaining=4, use=["legal", "orig", "total_life"]),
        dict(co="Lowry Co.", cost=600000, legal=19, useful=12, yrs=5, remaining=5, use=["legal", "total_life", "cost_rem"]),
    ]),
    "far-revenue-over-time-0001": (over_time, [
        dict(co="Barlow Builders", price=5000000, c1=1200000, e1=2800000, c2=2700000, e2=900000, use=["orig_est", "pct_diff", "cum_only"]),
        dict(co="Crane Builders", price=6000000, c1=1000000, e1=4000000, c2=3000000, e2=1000000, use=["orig_est", "pct_diff", "pct_diff_new"]),
        dict(co="Fordham Builders", price=10000000, c1=2000000, e1=6000000, c2=6300000, e2=2700000, use=["pct_diff_new", "cum_only", "orig_est"]),
        dict(co="Galway Builders", price=4000000, c1=800000, e1=2400000, c2=2400000, e2=600000, use=["orig_est", "pct_diff", "cum_only"]),
    ]),
    "far-nfp-contributed-services-0001": (contributed_services, [
        dict(org="Aster Museum", cpa=12000, carpentry=18000, greeters=25000, board=5000, use=["cpa_only", "cpa_board", "carp_only"]),
        dict(org="Beacon Museum", cpa=20000, carpentry=35000, greeters=40000, board=8000, use=["cpa_only", "carp_only", "plus_greet"]),
        dict(org="Corbett Museum", cpa=9000, carpentry=14000, greeters=30000, board=3000, use=["cpa_only", "cpa_board", "carp_only"]),
        dict(org="Delmar Museum", cpa=15000, carpentry=26000, greeters=22000, board=6000, use=["cpa_board", "carp_only", "plus_greet"]),
    ]),
    "far-lessee-finance-0002": (rvg_liability, [
        dict(co="Casey Co.", pay=50000, years=5, guar=40000, expected=30000, rate=6, use=["no_rvg", "full_rvg", "undisc"]),
        dict(co="Dawes Co.", pay=80000, years=4, guar=60000, expected=45000, rate=7, use=["expected", "full_rvg", "undisc"]),
        dict(co="Ebbets Co.", pay=30000, years=6, guar=25000, expected=10000, rate=5, use=["no_rvg", "expected", "full_rvg"]),
        dict(co="Fallon Co.", pay=100000, years=3, guar=80000, expected=70000, rate=8, use=["no_rvg", "undisc", "full_rvg"]),
    ]),
}

if __name__ == "__main__":
    run(FAMILIES, CONTENT)
