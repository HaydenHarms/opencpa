"""FAR variants 05: three extra versions for 12 numeric items from FAR batch 03.

Method as in far-variants-03.py (shared helpers in variants.py).

Run: python3 scripts/batches/far-variants-05.py   See docs/reviews/far-variants-05.md.
"""
import os
from decimal import Decimal as D

from common import variant
from variants import WORDS, m, n, pick, rd, run, whole

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def pctf(x):
    """3% or 2.5%."""
    x = D(str(x))
    return f"{x:.0f}%" if x == x.to_integral() else f"{x}%"


# ── Area I ───────────────────────────────────────────────────────────────


def functional_expenses(p):
    org, sal, sp, sm, sf, rent, rp, rm, sup, fee = (
        p[k] for k in ("org", "sal", "sal_prog", "sal_mg", "sal_fr", "rent", "rent_prog", "rent_mg", "supplies", "fee"))
    short = org.split()[0]
    s_mg, r_mg = whole(D(sal) * sm / 100), whole(D(rent) * rm / 100)
    key_v = s_mg + r_mg
    pool = {
        "plus_fee": (m(key_v + fee), f"Adds the {m(fee)} of external investment fees. Since ASU 2016-14, they are netted against investment return rather than reported as an expense."),
        "plus_fr": (m(key_v + whole(D(sal) * sf / 100)), f"Adds the {m(whole(D(sal) * sf / 100))} of fundraising salaries. Fundraising is a separate supporting function."),
        "all_rent": (m(s_mg + rent), f"Charges all of the rent to management and general. Rent is allocated by floor space, and {rp}% supports programs."),
        "sal_only": (m(s_mg), f"Leaves out management and general's {rm}% share of the rent. Rent is allocated to the functions it supports."),
    }
    key = (m(key_v), f"Correct. {sm}% of salaries ({m(s_mg)}) + {rm}% of rent ({m(r_mg)}). External investment fees are netted against investment return.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, incurred these costs in Year 1: salaries of {m(sal)}, of which staff time records show {sp}% was spent on programs, {sm}% on management and general activities, and {sf}% on fundraising; rent of {m(rent)}, allocated by floor space {rp}% to programs and {rm}% to management and general; program supplies of {m(sup)}; and {m(fee)} of fees paid to an outside investment adviser who manages {short}'s endowment. What amount should {short} report as management and general expenses in its analysis of expenses by function?""",
        choices, ans,
        f"""Expenses are reported by function using a reasonable allocation basis. Management and general: salaries {m(sal)} × {sm}% = {m(s_mg)}, plus rent {m(rent)} × {rm}% = {m(r_mg)}, for {m(key_v)}. Program supplies are program expenses. External investment expenses are netted against investment return, so the {m(fee)} adviser fee is not a functional expense.""",
    )


def days_in_inventory(p):
    co, sales, cogs, i0, i1 = (p[k] for k in ("co", "sales", "cogs", "i0", "i1"))
    short = co.split()[0]
    avg = whole(D(i0 + i1) / 2)
    turn = D(cogs) / avg
    days = lambda t: f"{rd(365 / t, '0.1')}"
    t_end, t_beg = D(cogs) / i1, D(cogs) / i0
    tt = f"{rd(turn, '0.1')}" if rd(turn, "0.01") == rd(turn, "0.1") else f"{rd(turn, '0.01')}"
    pool = {
        "sales": (days(D(sales) / avg), f"Computes turnover with sales ({m(sales)} ÷ {m(avg)}). Inventory turnover uses cost of goods sold, because inventory is carried at cost."),
        "ending": (days(t_end), f"Uses ending inventory ({m(cogs)} ÷ {m(i1)} = {rd(t_end, '0.01')} times). The question calls for average inventory."),
        "beginning": (days(t_beg), f"Uses beginning inventory ({m(cogs)} ÷ {m(i0)}). The question calls for average inventory."),
        "turnover": (tt, f"Stops at the inventory turnover ({tt} times). Days in inventory is 365 divided by the turnover."),
    }
    key = (days(turn), f"Correct. Turnover = {m(cogs)} ÷ {m(avg)} average inventory = {tt}; 365 ÷ {tt} = {days(turn)} days.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: float(c[0]))
    return variant(
        f"""For Year 2, {co} reports sales of {m(sales)} and cost of goods sold of {m(cogs)}. Inventory was {m(i0)} at the beginning of the year and {m(i1)} at the end. Using a 365-day year and average inventory, what is {short}'s number of days' sales in inventory, rounded to one decimal place?""",
        choices, ans,
        f"""Inventory turnover = cost of goods sold ÷ average inventory = {m(cogs)} ÷ [({m(i0)} + {m(i1)}) ÷ 2] = {tt} times. Days in inventory = 365 ÷ {tt} = {days(turn)} days.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def bank_rec(p):
    co, book, dit, oc, sc, ep, err, dup = (p[k] for k in ("co", "book", "dit", "oc", "sc", "ep", "err", "dup"))
    short = co.split()[0]
    adj = -sc + ep - dup
    correct = book + adj
    bank = correct - dit + oc - err
    ch = lambda x: f"{m(abs(x))} {'increase' if x > 0 else 'decrease'}"
    sgn = lambda x: f"{'−' if x < 0 else '+'}{m(abs(x))}"
    pool = {
        "no_dup": (ch(ep - sc), f"Records the service charge and the electronic payment but not the duplicate {m(dup)} deposit, which overstates the ledger."),
        "bank_err": (ch(adj - err), f"Also deducts the {m(err)} bank error in the ledger. The bank's error is corrected by the bank; {short}'s books are right for that item."),
        "ep_sign": (ch(-sc - ep - dup), f"Deducts the {m(ep)} electronic payment instead of adding it. Cash the bank received for {short} increases {short}'s cash."),
        "bank_items": (ch(dit - oc), "Adjusts the books for the deposits in transit and outstanding checks. Those are timing items that adjust the bank balance, not the ledger."),
    }
    key = (ch(adj), f"Correct. −{m(sc)} + {m(ep)} − {m(dup)} = {sgn(adj)}, bringing the ledger to {m(correct)}, which agrees with the adjusted bank balance.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s general ledger cash balance at March 31 is {m(book)}, and its bank statement shows {m(bank)}. The controller finds: deposits in transit of {m(dit)}; outstanding checks of {m(oc)}; a {m(sc)} bank service charge not yet recorded; a customer's {m(ep)} electronic payment received by the bank and not yet recorded; a {m(err)} check drawn by another company that the bank charged to {short}'s account in error; and a {m(dup)} customer deposit that {short} recorded twice in its cash receipts journal. After the reconciliation, what adjustment should {short} make to its general ledger cash balance?""",
        choices, ans,
        f"""Bank side: {m(bank)} + {m(dit)} deposits in transit − {m(oc)} outstanding checks + {m(err)} bank error = {m(correct)}. Book side: {m(book)} − {m(sc)} service charge + {m(ep)} electronic payment − {m(dup)} duplicate deposit = {m(correct)}. Only the book-side items need journal entries: a net {'decrease' if adj < 0 else 'increase'} of {m(abs(adj))}.""",
    )


def dollar_value_lifo(p):
    co, base, c2, i2, c3, i3 = (p[k] for k in ("co", "base", "c2", "i2", "c3", "i3"))
    short = co.split()[0]
    i2, i3 = D(i2), D(i3)
    b2, b3 = whole(c2 / i2), whole(c3 / i3)
    layer, left = b2 - base, b3 - base
    assert 0 < left < layer
    key_v = whole(base + left * i2)
    liq = "half of the Year 2 layer" if (layer - left) * 2 == layer else f"{m(layer - left)} of the {m(layer)} Year 2 layer"
    pool = {
        "y3_index": (m(whole(base + left * i3)), f"Prices the remaining Year 2 layer at the Year 3 index ({i3}). A layer keeps the index of the year it was added."),
        "no_liq": (m(whole(base + layer * i2)), f"Keeps the whole Year 2 layer. Year 3 base-year cost fell to {m(b3)}, so {m(layer - left)} of the {m(layer)} Year 2 layer was liquidated."),
        "current": (m(c3), "Reports current cost. Dollar-value LIFO restates inventory to base-year cost and prices each layer at its own index."),
        "base_cost": (m(b3), f"Stops at base-year cost ({m(b3)}) without pricing the remaining Year 2 layer at its {i2} index."),
    }
    key = (m(key_v), f"Correct. Base-year cost {m(b3)}: the {m(base)} base layer plus {m(left)} left of the Year 2 layer, priced at {i2} ({m(whole(left * i2))}).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} adopted dollar-value LIFO at the end of Year 1, when its inventory was {m(base)} and the price index was 1.00. Inventory at current year-end cost was {m(c2)} at the end of Year 2 (index {i2}) and {m(c3)} at the end of Year 3 (index {i3}). What is {short}'s dollar-value LIFO inventory at the end of Year 3?""",
        choices, ans,
        f"""Convert to base-year cost: Year 2 {m(c2)} ÷ {i2} = {m(b2)} (a {m(layer)} layer at {i2} = {m(whole(layer * i2))}; LIFO inventory {m(whole(base + layer * i2))}). Year 3 {m(c3)} ÷ {i3} = {m(b3)}, a {m(layer - left)} decrease that liquidates {liq}. Year 3 LIFO inventory = {m(base)} × 1.00 + {m(left)} × {i2} = {m(key_v)}.""",
    )


def accrued_liabilities(p):
    co, w, vr, vt, b, inc, sr, rep, ibnr = (p[k] for k in ("co", "wages", "vac_rec", "vac_true", "bonus_pct", "income", "si_rec", "reported", "ibnr"))
    short = co.split()[0]
    bonus = whole(D(inc) * b / (100 + b))
    gl = w + vr + bonus + sr
    si = rep + ibnr
    key_v = w + vt + bonus + si
    pool = {
        "reported_only": (m(key_v - ibnr), "Accrues only the claims already reported. Claims incurred but not yet reported are part of a self-insurer's liability."),
        "vac_only": (m(w + vt + bonus + sr), f"Updates vacation pay but leaves self-insurance at the general ledger's {m(sr)}. The liability is {m(rep)} reported plus {m(ibnr)} incurred but not reported."),
        "si_only": (m(w + vr + bonus + si), f"Updates self-insurance but leaves vacation at {m(vr)}. Vested vacation pay earned and unused at year-end is accrued in full ({m(vt)})."),
        "bonus_pre": (m(key_v - bonus + whole(D(inc) * b / 100)), f"Computes the bonus on income before the bonus ({b}% × {m(inc)}). The plan pays {b}% of income after deducting the bonus."),
    }
    key = (m(key_v), f"Correct. {m(w)} wages + {m(vt)} vacation + {m(bonus)} bonus + {m(si)} self-insurance.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s general ledger shows accrued liabilities of {m(gl)} at December 31: accrued wages {m(w)}, accrued vacation {m(vr)}, accrued bonus {m(bonus)}, and accrued self-insurance claims {m(sr)}. Supporting schedules show: wages earned but unpaid for the last three days of the year were {m(w)}; employees had earned {m(vt)} of vested, unused vacation pay; the bonus plan pays {b}% of income after deducting the bonus, and income before the bonus was {m(inc)}; and for its self-insured health plan, {short} owes {m(rep)} on claims reported but unpaid, and its actuary estimates {m(ibnr)} of claims incurred but not yet reported. What amount should {short} report as accrued liabilities?""",
        choices, ans,
        f"""Wages: {m(w)} (agrees). Vacation: vested, earned rights are accrued at {m(vt)}, {m(vt - vr)} more than recorded. Bonus: B = {b}% × ({m(inc)} − B), so B = {m(bonus)} (agrees). Self-insurance: {m(rep)} reported and unpaid plus {m(ibnr)} incurred but not reported = {m(si)}, {m(si - sr)} more than recorded. Accrued liabilities = {m(w)} + {m(vt)} + {m(bonus)} + {m(si)} = {m(key_v)}.""",
    )


def bond_premium(p):
    co, face, c, yrs, y = (p[k] for k in ("co", "face", "coupon", "years", "yld"))
    short = co.split()[0]
    k, r = yrs * 2, D(y) / 200
    cash_half = whole(D(face) * c / 200)
    price = rd(cash_half * (1 - (1 + r) ** -k) / r + face * (1 + r) ** -k)
    assert price > face
    e1 = rd(price * r)
    cv1 = price - (cash_half - e1)
    e2 = rd(cv1 * r)
    key_v = e1 + e2
    sl = (price - face) / yrs
    hp = f"{D(y) / 2:.1f}".rstrip("0").rstrip(".")
    pool = {
        "sl": (m(rd(2 * cash_half - sl)), f"Amortizes the premium straight-line ({m(rd(sl))} a year). The effective interest method is required unless the difference is immaterial."),
        "annual": (m(rd(price * D(y) / 100)), f"Applies the {y}% annual rate to the issue price once. Interest is compounded semiannually, and the carrying amount falls after the first payment."),
        "cash": (m(2 * cash_half), "Uses the cash interest paid. A premium reduces interest expense below the stated rate."),
        "stated": (m(rd(price * D(c) / 100)), f"Applies the {c}% stated rate to the carrying amount instead of the {y}% yield. Interest expense uses the market rate at issuance."),
    }
    key = (m(key_v), f"Correct. June 30: {m(price)} × {hp}% = {m(e1)}; the carrying amount falls to {m(cv1)}. December 31: {m(cv1)} × {hp}% = {m(e2)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} issues {m(face)} of {WORDS[yrs]}-year, {c}% bonds that pay interest each June 30 and December 31, for {m(price)}, a price that yields {y}% compounded semiannually. {short} uses the effective interest method and rounds to the nearest dollar at each step. What is {short}'s interest expense on the bonds for Year 1?""",
        choices, ans,
        f"""Effective interest is computed each semiannual period at {hp}% of the carrying amount. June 30: {m(price)} × {hp}% = {m(e1)} expense; cash {m(cash_half)}; premium amortized {m(cash_half - e1)}; carrying amount {m(cv1)}. December 31: {m(cv1)} × {hp}% = {m(e2)} expense; premium amortized {m(cash_half - e2)}. Year 1 interest expense = {m(e1)} + {m(e2)} = {m(key_v)}.""",
    )


def held_for_sale(p):
    co, cost, ad0, dep, lst, fv1, cts, fv2 = (p[k] for k in ("co", "cost", "ad0", "dep", "listed", "fv1", "cts", "fv2"))
    short = co.split()[0]
    ad = ad0 + whole(D(dep) * 9 / 12)
    ca = cost - ad
    f1, f2 = fv1 - cts, fv2 - cts
    loss = ca - f1
    assert loss > 0 and 0 < f2 - f1 < loss
    key_v = f2
    pool = {
        "keep_oct": (m(f1), "Keeps the October 1 measurement. A later increase in fair value less cost to sell is recognized as a gain, up to the loss previously recognized."),
        "fv_no_cts": (m(fv2), "Uses fair value without deducting the cost to sell."),
        "ca": (m(ca), "Reclassifies the equipment at its carrying amount without comparing it with fair value less cost to sell."),
        "dep_after": (m(key_v - whole(D(dep) * 3 / 12)), f"Keeps depreciating after October 1 ({m(whole(D(dep) * 3 / 12))} for three months). An asset classified as held for sale is not depreciated."),
    }
    key = (m(key_v), f"Correct. Carrying amount at October 1 is {m(ca)}; it is written down to {m(f1)} and then increased to {m(f2)} at year-end.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On October 1, Year 1, {co}'s board approves selling a piece of equipment it no longer needs. {short} takes it out of service that day and lists it with a dealer at {m(lst)}, in line with recent sales of similar equipment; it expects a buyer within six months and does not expect to change the plan. The equipment cost {m(cost)}; accumulated depreciation was {m(ad0)} at January 1, Year 1, and annual depreciation is {m(dep)}. On October 1, the equipment's fair value is {m(fv1)} and the estimated cost to sell is {m(cts)}. On December 31, Year 1, it is still unsold, its fair value is {m(fv2)}, and the estimated cost to sell is still {m(cts)}. At what amount should the equipment be reported at December 31, Year 1?""",
        choices, ans,
        f"""The board's approval, the listing at a price in line with the market, the asset's immediate availability, and the expected sale within six months meet the held-for-sale criteria on October 1. Depreciation runs until then: {m(ad0)} + 9/12 × {m(dep)} = {m(ad)} of accumulated depreciation, so the carrying amount on October 1 is {m(ca)}. A held-for-sale asset is measured at the lower of carrying amount and fair value less cost to sell ({m(f1)}), a {m(loss)} loss, and is no longer depreciated. At year-end, fair value less cost to sell is {m(f2)}; the {m(f2 - f1)} increase is recognized as a gain because it does not exceed the {m(loss)} loss recognized earlier.""",
    )


def receivables_rec(p):
    co, deb, cred, sale = (p[k] for k in ("co", "debits", "credits", "sale"))
    short = co.split()[0]
    gl = deb + sale - cred
    key_v = deb + sale
    pool = {
        "sub_net": (m(deb - cred), f"Reports the unadjusted subledger net. It omits the {m(sale)} sale and nets customer credit balances against receivables."),
        "gl": (m(gl), "Reports the general ledger balance, which agrees with the corrected subledger net. Customer credit balances are liabilities and are not netted against receivables from other customers."),
        "debits": (m(deb), f"Reports the subledger's debit balances without posting the {m(sale)} sale that is missing from them."),
        "add_cr": (m(key_v + cred), f"Adds the {m(cred)} of customer credit balances to receivables. They are amounts owed to customers, reported as liabilities."),
    }
    key = (m(key_v), f"Correct. Posting the {m(sale)} sale raises debit balances to {m(key_v)}; the {m(cred)} of credit balances is reported as a current liability.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s accounts receivable subledger shows customer accounts with debit balances totaling {m(deb)} and customer accounts with credit balances totaling {m(cred)}, for a net of {m(deb - cred)}. The general ledger accounts receivable control account shows {m(gl)}. Investigating the difference, the controller finds that a {m(sale)} credit sale made on December 27 was posted to the general ledger but never to the customer's subledger account; that customer had no other balance. Before any allowance for credit losses, what amount should {short} report as accounts receivable?""",
        choices, ans,
        f"""Reconcile first: the subledger is missing the {m(sale)} sale, so its debit balances become {m(key_v)} and its net becomes {m(gl)}, which agrees with the general ledger. For presentation, customer accounts with credit balances are reclassified as liabilities rather than netted against other customers' debit balances. Accounts receivable = {m(key_v)}; customer credit balances of {m(cred)} are reported as current liabilities.""",
    )


def stock_dividends(p):
    co, s0, par, sp, mk1, lp, mk2 = (p[k] for k in ("co", "s0", "par", "small", "mkt1", "large", "mkt2"))
    short = co.split()[0]
    par, new_par = D(par), D(par) / 2
    small = whole(D(s0) * sp / 100)
    after = (s0 + small) * 2
    large = whole(D(after) * lp / 100)
    key_v = small * mk1 + large * new_par
    pool = {
        "both_par": (m(small * par + large * new_par), f"Records both stock dividends at par. The {sp}% dividend is small, so it is recorded at market value."),
        "no_large": (m(small * mk1), f"Records the {sp}% dividend at market value but nothing for the {lp}% dividend, treating it like a split. A large stock dividend is still capitalized, at par."),
        "large_mkt": (m(small * mk1 + large * mk2), f"Records the {lp}% dividend at market value. A distribution of more than 20–25% is accounted for like a split and capitalized at par."),
        "large_oldpar": (m(small * mk1 + large * par), f"Capitalizes the {lp}% dividend at the {m(par)} par in effect before the split. After the split, par is {m(new_par)}."),
    }
    key = (m(key_v), f"Correct. {n(small)} shares × {m(mk1)} = {m(small * mk1)} for the small dividend, plus {n(large)} shares × {m(new_par)} par = {m(large * new_par)} for the large dividend.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At January 1, {co} has {n(s0)} shares of {m(par)} par common stock outstanding. On March 1 it distributes a {sp}% stock dividend when the market price is {m(mk1)} per share. On July 1 it effects a 2-for-1 stock split, reducing par value to {m(new_par)} per share. On November 1 it distributes a {lp}% stock dividend when the market price is {m(mk2)} per share. By how much do these three transactions reduce retained earnings?""",
        choices, ans,
        f"""March 1: a {sp}% dividend is small, so {n(small)} shares are capitalized at the {m(mk1)} market price: {m(small * mk1)}. July 1: a stock split changes the number of shares and the par value but requires no entry to retained earnings; shares become {n(after)} at {m(new_par)} par. November 1: a {lp}% dividend is large, so {n(large)} shares are capitalized at par: {m(large * new_par)}. Total reduction = {m(key_v)}.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def warranty_environmental(p):
    co, award, sales, w, paid, lo, hi, best = (p[k] for k in ("co", "award", "sales", "warranty", "paid", "low", "high", "best"))
    short = co.split()[0]
    wexp = whole(D(sales) * D(str(w)) / 100)
    key_v = wexp + best
    pool = {
        "offset": (m(key_v - award), f"Offsets the expected {m(award)} award against the losses. A gain contingency is not recognized until it is realized."),
        "low_end": (m(wexp + lo), f"Accrues the {m(lo)} low end of the environmental range. When one amount in a range is the best estimate, that amount is accrued."),
        "liab_only": (m(wexp - paid + best), f"Uses the {m(wexp - paid)} warranty liability remaining at year-end instead of the {m(wexp)} warranty expense."),
        "high_end": (m(wexp + hi), f"Accrues the {m(hi)} high end of the environmental range. When one amount in a range is the best estimate, that amount is accrued."),
    }
    key = (m(key_v), f"Correct. Warranty expense of {m(wexp)} ({pctf(w)} × {m(sales)}) plus the {m(best)} best estimate of the environmental obligation.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} is preparing its Year 1 statements, which have not been issued. Its files show: (1) {short} is suing a competitor for patent infringement, and counsel expects {short} to be awarded about {m(award)}; (2) {short}'s Year 1 sales of {m(sales)} carry a one-year warranty, past experience shows warranty costs of {pctf(w)} of sales, and {short} paid {m(paid)} of claims on these sales in Year 1; (3) the Environmental Protection Agency named {short} a potentially responsible party for a contaminated site, and engineers estimate {short}'s share of the cleanup at {m(lo)} to {m(hi)}, with {m(best)} the most likely amount; and (4) no one has asserted a claim over a minor chemical spill at one of {short}'s plants, and counsel believes a claim is unlikely to be asserted. By how much do these matters reduce {short}'s Year 1 pretax income?""",
        choices, ans,
        f"""Review each item. (1) The expected award is a gain contingency: disclosed, not recognized. (2) Warranty expense is recognized in the period of sale: {pctf(w)} × {m(sales)} = {m(wexp)} (the liability is {m(wexp - paid)} after claims paid). (3) The environmental loss is probable and estimable, and {m(best)} is the best estimate within the range, so it is accrued. (4) An unasserted claim that is unlikely to be asserted requires neither accrual nor disclosure. Pretax income falls by {m(wexp)} + {m(best)} = {m(key_v)}.""",
    )


def eps_after_events(p):
    co, ni, sh, carried, sold, k = (p[k] for k in ("co", "ni", "shares", "carried", "sold", "split"))
    short = co.split()[0]
    wd = carried - sold
    eps = lambda num, den: f"${rd(D(num) / den, '0.01')}"
    pool = {
        "no_wd": (eps(ni, sh * k), f"Restates shares for the split but does not recognize the {m(wd)} write-down, which gives evidence of the inventory's value at year-end."),
        "no_split": (eps(ni - wd, sh), "Recognizes the write-down but does not restate shares for the split. A split before the statements are issued is reflected retroactively in EPS."),
        "neither": (eps(ni, sh), "Makes neither adjustment."),
        "full_writeoff": (eps(ni - carried, sh * k), f"Writes off the inventory's whole {m(carried)} carrying amount. It sold for {m(sold)}, so only the {m(wd)} shortfall is a loss."),
    }
    key = (eps(ni - wd, sh * k), f"Correct. ({m(ni)} − {m(wd)} write-down) ÷ {n(sh * k)} shares, restated for the split.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31, Year 1, statements will be issued on March 1, Year 2. Before any subsequent-event adjustments, Year 1 net income is {m(ni)} and weighted-average common shares outstanding are {n(sh)}; {short} has no preferred stock. On January 20, {short} sold inventory carried at {m(carried)} for {m(sold)} because the goods had become obsolete during Year 1. On February 1, it effected a {k}-for-1 stock split. On February 10, it agreed to acquire a competitor. Ignore income taxes. What basic earnings per share should {short} report for Year 1?""",
        choices, ans,
        f"""The January sale shows that obsolescence existing at year-end had reduced the inventory's net realizable value to {m(sold)}, so a {m(wd)} write-down is recognized in Year 1. A stock split after year-end but before issuance is applied retroactively to EPS: {n(sh * k)} shares. The February 10 acquisition agreement is disclosed only. Basic EPS = ({m(ni)} − {m(wd)}) ÷ {n(sh * k)} = {eps(ni - wd, sh * k)}.""",
    )


def volume_discount(p):
    co, lst, disc, thr, exp_, q = (p[k] for k in ("co", "list", "disc", "threshold", "expected", "q1"))
    short = co.split()[0]
    key_v = q * disc
    assert q * lst > exp_ * (lst - disc)
    pool = {
        "full_disc": (m(q * lst - exp_ * (lst - disc)), f"Deducts the whole year's expected discount ({n(exp_)} × {m(lst - disc)} = {m(exp_ * (lst - disc))}) from first-quarter sales at {m(lst)}. The discount is recognized as the units it applies to are sold."),
        "average": (m(whole(D(q) * (lst + disc) / 2)), f"Averages the two prices. With strong experience that the threshold will be met, the {m(disc)} price is the best estimate."),
        "list": (m(q * lst), f"Uses the {m(lst)} list price until the threshold is reached. The expected retroactive discount is variable consideration estimated from the start."),
        "zero": ("$0", f"Defers all revenue until the customer passes {n(thr)} units. Revenue is recognized as control of the parts transfers, at the estimated transaction price."),
    }
    key = (m(key_v), f"Correct. The expected volume discount is included in the transaction price: {n(q)} × {m(disc)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, {co} agrees to sell a customer parts at {m(lst)} per unit. If the customer buys more than {n(thr)} units during the calendar year, the price for all units bought that year falls retroactively to {m(disc)}. From many years of dealing with this customer, {short} expects it to buy about {n(exp_)} units, and a shortfall below {n(thr)} has never occurred. In the first quarter, the customer buys {n(q)} units. How much revenue should {short} recognize for the first quarter?""",
        choices, ans,
        f"""The retroactive volume discount makes the consideration variable. {short} estimates it from its experience with the customer: purchases of about {n(exp_)} units, so the price will be {m(disc)}. Because it has long experience and a shortfall has never occurred, including the discounted price is not expected to cause a significant revenue reversal. Q1 revenue = {n(q)} × {m(disc)} = {m(key_v)}, with {m(q * (lst - disc))} recognized as a refund liability.""",
    )


FAMILIES = {
    "far-nfp-functional-expenses-0001": (functional_expenses, [
        dict(org="Linden Center", sal=600000, sal_prog=70, sal_mg=20, sal_fr=10, rent=120000, rent_prog=75, rent_mg=25, supplies=80000, fee=10000, use=["plus_fee", "plus_fr", "all_rent"]),
        dict(org="Magnolia Center", sal=800000, sal_prog=65, sal_mg=25, sal_fr=10, rent=150000, rent_prog=80, rent_mg=20, supplies=90000, fee=15000, use=["sal_only", "plus_fee", "plus_fr"]),
        dict(org="Nutmeg Center", sal=450000, sal_prog=75, sal_mg=15, sal_fr=10, rent=96000, rent_prog=70, rent_mg=30, supplies=60000, fee=8000, use=["plus_fee", "plus_fr", "all_rent"]),
        dict(org="Orchard Center", sal=1000000, sal_prog=70, sal_mg=18, sal_fr=12, rent=200000, rent_prog=85, rent_mg=15, supplies=120000, fee=25000, use=["sal_only", "plus_fee", "all_rent"]),
    ]),
    "far-ratios-0002": (days_in_inventory, [
        dict(co="Mott Co.", sales=2190000, cogs=1460000, i0=180000, i1=220000, use=["sales", "ending", "beginning"]),
        dict(co="Pruitt Co.", sales=3650000, cogs=2190000, i0=250000, i1=188000, use=["turnover", "sales", "ending"]),
        dict(co="Quarry Co.", sales=1460000, cogs=1000000, i0=160000, i1=240000, use=["sales", "beginning", "ending"]),
        dict(co="Rudley Co.", sales=2555000, cogs=2190000, i0=400000, i1=330000, use=["ending", "sales", "turnover"]),
    ]),
    "far-cash-bank-reconciliation-0002": (bank_rec, [
        dict(co="Dunmore Co.", book=34625, dit=4100, oc=6300, sc=45, ep=1200, err=500, dup=2280, use=["no_dup", "bank_err", "ep_sign"]),
        dict(co="Elmore Co.", book=52380, dit=6200, oc=9000, sc=30, ep=500, err=600, dup=4000, use=["no_dup", "bank_items", "bank_err"]),
        dict(co="Fenton Co.", book=18450, dit=2500, oc=4100, sc=25, ep=3600, err=400, dup=900, use=["bank_items", "no_dup", "ep_sign"]),
        dict(co="Gorham Co.", book=67900, dit=7400, oc=3100, sc=55, ep=1800, err=350, dup=5150, use=["no_dup", "bank_err", "ep_sign"]),
    ]),
    "far-inventory-dollar-value-lifo-0001": (dollar_value_lifo, [
        dict(co="Dorset Co.", base=200000, c2=264000, i2="1.10", c3=286000, i3="1.30", use=["y3_index", "no_liq", "current"]),
        dict(co="Ellison Co.", base=300000, c2=450000, i2="1.25", c3=476000, i3="1.40", use=["base_cost", "y3_index", "no_liq"]),
        dict(co="Fairfax Co.", base=150000, c2=194400, i2="1.08", c3=204000, i3="1.20", use=["y3_index", "no_liq", "current"]),
        dict(co="Garland Co.", base=400000, c2=552000, i2="1.15", c3=616000, i3="1.40", use=["base_cost", "y3_index", "no_liq"]),
    ]),
    "far-accrued-liabilities-0001": (accrued_liabilities, [
        dict(co="Morrow Co.", wages=30000, vac_rec=40000, vac_true=48000, bonus_pct=10, income=1100000, si_rec=40000, reported=10000, ibnr=55000, use=["reported_only", "vac_only", "si_only"]),
        dict(co="Norcross Co.", wages=45000, vac_rec=60000, vac_true=72000, bonus_pct=8, income=1620000, si_rec=50000, reported=15000, ibnr=70000, use=["vac_only", "si_only", "bonus_pre"]),
        dict(co="Oswego Co.", wages=20000, vac_rec=25000, vac_true=31000, bonus_pct=10, income=880000, si_rec=30000, reported=6000, ibnr=40000, use=["reported_only", "vac_only", "si_only"]),
        dict(co="Pomfret Co.", wages=60000, vac_rec=55000, vac_true=64000, bonus_pct=5, income=2100000, si_rec=70000, reported=20000, ibnr=90000, use=["reported_only", "vac_only", "bonus_pre"]),
    ]),
    "far-bonds-premium-0001": (bond_premium, [
        dict(co="Wynn Corp.", face=1000000, coupon=8, years=10, yld=6, use=["sl", "annual", "cash"]),
        dict(co="Abner Corp.", face=500000, coupon=10, years=5, yld=8, use=["annual", "cash", "stated"]),
        dict(co="Bramwell Corp.", face=2000000, coupon=7, years=8, yld=6, use=["sl", "annual", "cash"]),
        dict(co="Castor Corp.", face=800000, coupon=9, years=6, yld=7, use=["annual", "cash", "stated"]),
    ]),
    "far-ppe-held-for-sale-0001": (held_for_sale, [
        dict(co="Harlow Co.", cost=500000, ad0=200000, dep=40000, listed=255000, fv1=250000, cts=15000, fv2=260000, use=["keep_oct", "fv_no_cts", "ca"]),
        dict(co="Ivers Co.", cost=800000, ad0=320000, dep=48000, listed=405000, fv1=400000, cts=20000, fv2=430000, use=["keep_oct", "dep_after", "fv_no_cts"]),
        dict(co="Jasper Co.", cost=300000, ad0=90000, dep=24000, listed=175000, fv1=170000, cts=8000, fv2=176000, use=["keep_oct", "fv_no_cts", "ca"]),
        dict(co="Kerwin Co.", cost=1200000, ad0=500000, dep=80000, listed=595000, fv1=590000, cts=30000, fv2=620000, use=["keep_oct", "dep_after", "ca"]),
    ]),
    "far-receivables-reconciliation-0001": (receivables_rec, [
        dict(co="Arden Co.", debits=503000, credits=14000, sale=9000, use=["sub_net", "gl", "debits"]),
        dict(co="Blythe Co.", debits=740000, credits=22000, sale=16000, use=["sub_net", "gl", "add_cr"]),
        dict(co="Carver Co.", debits=310000, credits=6000, sale=11000, use=["sub_net", "debits", "gl"]),
        dict(co="Dalby Co.", debits=1050000, credits=35000, sale=28000, use=["gl", "debits", "add_cr"]),
    ]),
    "far-stock-dividends-splits-0001": (stock_dividends, [
        dict(co="Tolland Corp.", s0=200000, par=1, small=5, mkt1=20, large=50, mkt2=12, use=["both_par", "no_large", "large_mkt"]),
        dict(co="Varden Corp.", s0=300000, par=2, small=10, mkt1=30, large=40, mkt2=18, use=["both_par", "large_oldpar", "large_mkt"]),
        dict(co="Welland Corp.", s0=120000, par=1, small=8, mkt1=25, large=30, mkt2=15, use=["both_par", "no_large", "large_oldpar"]),
        dict(co="Yorke Corp.", s0=500000, par=1, small=5, mkt1=16, large=60, mkt2=9, use=["no_large", "large_oldpar", "large_mkt"]),
    ]),
    "far-contingencies-0003": (warranty_environmental, [
        dict(co="Knox Co.", award=500000, sales=2000000, warranty=3, paid=25000, low=300000, high=700000, best=450000, use=["offset", "low_end", "liab_only"]),
        dict(co="Lanier Co.", award=300000, sales=3000000, warranty=2, paid=40000, low=200000, high=500000, best=350000, use=["low_end", "liab_only", "high_end"]),
        dict(co="Merritt Co.", award=150000, sales=1500000, warranty=4, paid=20000, low=400000, high=900000, best=600000, use=["offset", "low_end", "liab_only"]),
        dict(co="Northam Co.", award=800000, sales=4000000, warranty="2.5", paid=30000, low=250000, high=650000, best=500000, use=["low_end", "liab_only", "high_end"]),
    ]),
    "far-subsequent-events-0003": (eps_after_events, [
        dict(co="Pell Co.", ni=600000, shares=200000, carried=90000, sold=70000, split=2, use=["no_wd", "no_split", "neither"]),
        dict(co="Ridgeway Co.", ni=900000, shares=300000, carried=150000, sold=105000, split=3, use=["full_writeoff", "no_wd", "no_split"]),
        dict(co="Selden Co.", ni=480000, shares=120000, carried=60000, sold=36000, split=2, use=["no_wd", "no_split", "neither"]),
        dict(co="Tamworth Co.", ni=1250000, shares=500000, carried=200000, sold=130000, split=2, use=["full_writeoff", "no_wd", "neither"]),
    ]),
    "far-revenue-variable-consideration-0002": (volume_discount, [
        dict(co="Harlan Co.", list=100, disc=90, threshold=10000, expected=12000, q1=3000, use=["full_disc", "average", "list"]),
        dict(co="Iverson Co.", list=50, disc=44, threshold=20000, expected=26000, q1=7000, use=["zero", "full_disc", "list"]),
        dict(co="Jennings Co.", list=200, disc=185, threshold=5000, expected=6500, q1=1500, use=["zero", "full_disc", "list"]),
        dict(co="Kessler Co.", list=80, disc=72, threshold=15000, expected=18000, q1=4000, use=["zero", "full_disc", "list"]),
    ]),
}

if __name__ == "__main__":
    run(FAMILIES, CONTENT)
