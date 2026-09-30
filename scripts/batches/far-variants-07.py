"""FAR variants 07: three extra versions for 13 numeric items from FAR batch 02.

Method as in far-variants-03.py (shared helpers in variants.py).

Run: python3 scripts/batches/far-variants-07.py   See docs/reviews/far-variants-07.md.
"""
import os
from decimal import Decimal as D

from common import variant
from variants import WORDS, dollars_in, m, n, pick, rd, run, whole

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def net(x, t):
    return whole(D(x) * (100 - t) / 100)


def ratio(a, b):
    return f"{rd(D(a) / b, '0.01')}"


# ── Area I ───────────────────────────────────────────────────────────────


def cash_to_accrual(p):
    co, cash, ar0, ar1, wo, adv0, adv1 = (p[k] for k in ("co", "cash", "ar0", "ar1", "wo", "adv0", "adv1"))
    short = co.split()[0]
    dar, dadv = ar1 - ar0, adv0 - adv1
    assert dar > 0 and dadv > 0
    key_v = cash + dar + wo + dadv
    pool = {
        "sub_ar": (m(key_v - 2 * dar), f"Subtracts the {m(dar)} increase in receivables. Revenue earned but not yet collected raises accrual revenue above cash received."),
        "sub_adv": (m(key_v - 2 * dadv), f"Subtracts the {m(dadv)} decrease in client advances. Advances earned during the year exceed new advances received, so accrual revenue is higher than cash."),
        "no_wo": (m(key_v - wo), f"Omits the {m(wo)} written off. Those receivables were billed as revenue even though they were never collected."),
        "cash_only": (m(cash), "Reports the cash received. Accrual revenue adjusts cash for the changes in receivables, the write-offs and the change in advances."),
        "plus_adv1": (m(key_v + adv1), f"Also counts the {m(adv1)} of year-end client advances as revenue. They are for work not yet performed, so they are liabilities."),
    }
    key = (m(key_v), f"Correct. {m(cash)} + {m(dar)} increase in receivables + {m(wo)} written off + {m(dadv)} decrease in client advances.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} keeps its records on the cash basis. In Year 2 it received {m(cash)} in cash from clients. Client accounts receivable were {m(ar0)} on January 1 and {m(ar1)} on December 31, and during the year {short} wrote off {m(wo)} of client receivables as uncollectible. Client advances for work not yet performed were {m(adv0)} on January 1 and {m(adv1)} on December 31. What is {short}'s Year 2 consulting revenue on the accrual basis?""",
        choices, ans,
        f"""Revenue = cash received + ending receivables − beginning receivables + receivables written off + beginning advances − ending advances. {m(cash)} + ({m(ar1)} − {m(ar0)}) + {m(wo)} + ({m(adv0)} − {m(adv1)}) = {m(key_v)}. The written-off receivables were revenue that never reached cash, and the net decrease in advances is revenue earned from cash collected in an earlier year.""",
    )


def quick_ratio(p):
    co, cash, tb, tr, ar, inv, pp, cl = (p[k] for k in ("co", "cash", "tbills", "trading", "ar", "inv", "prepaid", "cl"))
    short = co.split()[0]
    q = cash + tb + tr + ar
    pool = {
        "plus_inv": (ratio(q + inv, cl), "Includes inventory. The quick ratio excludes inventory and prepaid expenses."),
        "plus_pp": (ratio(q + pp, cl), "Includes prepaid insurance. Prepaid expenses will not convert to cash, so they are excluded along with inventory."),
        "current": (ratio(q + inv + pp, cl), "Computes the current ratio. The quick ratio excludes inventory and prepaid expenses."),
        "cash_ratio": (ratio(cash + tb, cl), "Counts only cash and cash equivalents. The quick ratio also includes marketable securities and net receivables."),
        "no_tr": (ratio(cash + tb + ar, cl), f"Leaves out the {m(tr)} of trading securities. Marketable securities are quick assets."),
    }
    key = (ratio(q, cl), f"Correct. ({m(cash)} + {m(tb)} + {m(tr)} + {m(ar)}) ÷ {m(cl)}.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: float(c[0]))
    return variant(
        f"""At year-end, {co} reports the following current assets: cash {m(cash)}; Treasury bills purchased with a two-month maturity {m(tb)}; trading debt securities {m(tr)}; accounts receivable, net {m(ar)}; inventory {m(inv)}; and prepaid insurance {m(pp)}. Current liabilities total {m(cl)}. What is {short}'s quick ratio?""",
        choices, ans,
        f"""Quick assets are cash and cash equivalents, marketable securities, and net receivables: {m(cash)} + {m(tb)} + {m(tr)} + {m(ar)} = {m(q)}. Quick ratio = {m(q)} ÷ {m(cl)} = {ratio(q, cl)}. Inventory and prepaid expenses are excluded.""",
    )


def nfp_financing(p):
    org, bldg, endow, unres, constr, mort = (p[k] for k in ("org", "bldg", "endow", "unres", "constr", "mort"))
    short = org.split()[0]
    key_v = bldg + endow - mort
    pool = {
        "bldg_op": (m(key_v - bldg), f"Reports the {m(bldg)} building gift as an operating inflow. Contributions restricted to acquiring long-lived assets are financing inflows."),
        "no_endow": (m(key_v - endow), f"Leaves the {m(endow)} endowment gift out of financing. Contributions restricted for permanent endowment are financing inflows."),
        "plus_unres": (m(key_v + unres), f"Also counts the {m(unres)} of unrestricted contributions. Contributions without donor restrictions are operating inflows."),
        "minus_constr": (m(key_v - constr), f"Also subtracts the {m(constr)} of construction payments. Payments to construct a long-lived asset are investing outflows."),
        "no_mort": (m(key_v + mort), f"Leaves out the {m(mort)} of mortgage principal repaid, a financing outflow."),
    }
    key = (m(key_v), f"Correct. {m(bldg)} building gift + {m(endow)} endowment gift − {m(mort)} mortgage principal.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, received these amounts in cash: {m(bldg)} from a donor who restricted the gift to constructing a new wing, {m(endow)} from a donor who required it to be invested in perpetuity with the income used for operations, and {m(unres)} of contributions without donor restrictions. {short} also paid {m(constr)} of construction costs for the new wing and repaid {m(mort)} of principal on its mortgage. What is {short}'s net cash provided by financing activities for Year 1?""",
        choices, ans,
        f"""For a not-for-profit entity, cash contributions that donors restrict to long-term purposes (acquiring, constructing or improving long-lived assets, or establishing or increasing an endowment) are financing inflows. Financing: {m(bldg)} + {m(endow)} − {m(mort)} mortgage principal = {m(key_v)}. The unrestricted contributions are operating, and the construction payments are investing.""",
    )


def change_in_principle(p):
    co, wa1, f1, wa2, f2, t = (p[k] for k in ("co", "wa1", "f1", "wa2", "f2", "t"))
    short = co.split()[0]
    d1, d2 = f1 - wa1, f2 - wa2
    assert d2 > d1 > 0
    ni, re_, open_ = net(d2 - d1, t), net(d2, t), net(d1, t)
    both = lambda a, b: f"{m(a)} net income; {m(b)} retained earnings"
    pool = {
        "prosp": ("$0 net income; $0 retained earnings", "Applies the change prospectively from Year 3. A change in accounting principle is applied retrospectively, so Year 2 is restated."),
        "open_only": (both(ni, open_), f"Carries only the January 1, Year 2, adjustment ({m(d1)} × {100 - t}%) to year-end retained earnings, leaving out the restated Year 2 income."),
        "no_tax": (both(d2 - d1, d2), f"Ignores the {t}% tax effect of the change."),
        "whole_y2": (both(re_, re_), f"Treats the whole {m(d2)} year-end difference as a Year 2 effect. Only the {m(d2 - d1)} increase in the difference during Year 2 affects Year 2 income."),
    }
    key = (both(ni, re_), f"Correct. Year 2 income rises by ({m(d2)} − {m(d1)}) × {100 - t}% = {m(ni)}; year-end retained earnings rises by {m(d2)} × {100 - t}% = {m(re_)}.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: (dollars_in(c[0]), c[0]))
    return variant(
        f"""At the start of Year 3, {co} changes its inventory method from weighted-average cost to FIFO because FIFO better reflects its flow of goods. It can determine the effects for all prior periods. Inventory under each method was: December 31, Year 1 — weighted-average {m(wa1)}, FIFO {m(f1)}; December 31, Year 2 — weighted-average {m(wa2)}, FIFO {m(f2)}. Apply a {t}% tax rate to every effect. {short} issues comparative statements for Years 2 and 3. Compared with the amounts originally reported, by how much do Year 2 net income and December 31, Year 2, retained earnings change in those statements?""",
        choices, ans,
        f"""A change in accounting principle is applied retrospectively. The cumulative effect on periods before the earliest period presented adjusts the opening retained earnings of Year 2: ({m(f1)} − {m(wa1)}) × {100 - t}% = {m(open_)} increase. Year 2 is restated: FIFO raises ending inventory by {m(d2)} versus {m(d1)} at the start, so cost of goods sold falls by {m(d2 - d1)} and net income rises by {m(d2 - d1)} × {100 - t}% = {m(ni)}. December 31, Year 2, retained earnings rises by {m(open_)} + {m(ni)} = {m(re_)} (the {m(d2)} year-end difference, net of tax).""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def factoring(p):
    co, rec, fee_p, hold_p = (p[k] for k in ("co", "rec", "fee", "hold"))
    short = co.split()[0]
    fee, hold = whole(D(rec) * fee_p / 100), whole(D(rec) * hold_p / 100)
    cash = rec - fee - hold
    fee_net = whole(D(rec - hold) * fee_p / 100)
    both = lambda c, l: f"{m(c)} cash; {m(l)} loss"
    pool = {
        "hold_loss": (both(cash, fee + hold), f"Treats the {m(hold)} holdback as part of the loss. {short} expects to collect it, so it is a receivable from the factor."),
        "fee_on_net": (both(rec - hold - fee_net, fee_net), f"Computes the fee on the {m(rec - hold)} advanced. The fee is {fee_p}% of the {m(rec)} of receivables transferred."),
        "hold_paid": (both(rec - fee, fee), "Treats the holdback as paid at the transfer. The factor keeps it until the accounts are collected."),
        "no_loss": (f"{m(cash)} cash; $0 loss", "Records no loss on the sale. The factor's fee is a cost of selling the receivables, recognized as a loss."),
    }
    key = (both(cash, fee), f"Correct. {m(rec)} − {m(fee)} fee − {m(hold)} holdback; the fee is the loss, and the holdback is a receivable from the factor.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: (dollars_in(c[0]), c[0]))
    return variant(
        f"""{co} transfers {m(rec)} of trade receivables to a factor without recourse. The receivables are legally isolated from {short}, the factor may sell or pledge them, and {short} has no agreement or right to repurchase them. The factor charges a fee of {fee_p}% of the receivables transferred and holds back {hold_p}% of the receivables to cover sales returns and allowances, to be paid to {short} after the accounts are collected. {short} expects no returns or allowances. How much cash does {short} receive at the transfer, and what loss does it recognize?""",
        choices, ans,
        f"""The transfer meets the conditions for sale accounting: the receivables are isolated from {short}, the factor can pledge or sell them, and {short} keeps no effective control. {short} derecognizes the receivables. Cash = {m(rec)} − {fee_p}% fee ({m(fee)}) − {hold_p}% holdback ({m(hold)}) = {m(cash)}. The holdback is recorded as a receivable from the factor, and the {m(fee)} fee is the loss on sale.""",
    )


def htm_amortized_cost(p):
    co, face, c, yrs, y, fv_off = (p[k] for k in ("co", "face", "coupon", "years", "yld", "fv_off"))
    short = co.split()[0]
    r = D(y) / 100
    cash = whole(D(face) * c / 100)
    price = rd(cash * (1 - (1 + r) ** -yrs) / r + face * (1 + r) ** -yrs)
    assert price < face
    i1 = rd(price * r)
    cv1 = price + (i1 - cash)
    i2 = rd(cv1 * r)
    cv2 = cv1 + (i2 - cash)
    fv = cv2 + fv_off if fv_off else D(p["fv"])
    sl = (face - price) / yrs
    face_int = whole(D(face) * y / 100)
    pool = {
        "face_yield": (m(price + 2 * (face_int - cash)), f"Computes interest income at {y}% of face ({m(face_int)}), amortizing {m(face_int - cash)} a year. Effective interest applies the yield to the carrying amount."),
        "sl": (m(rd(price + 2 * sl)), f"Amortizes the discount straight-line ({m(rd(sl))} a year). The effective interest method is required unless the difference is immaterial."),
        "fv": (m(fv), "Reports fair value. Held-to-maturity securities are carried at amortized cost."),
        "one_year": (m(cv1), "Stops after one year of amortization. By December 31, Year 2, two years of discount amortization have been recorded."),
    }
    key = (m(cv2), f"Correct. Year 1: {m(price)} + ({m(i1)} − {m(cash)}) = {m(cv1)}. Year 2: {m(cv1)} + ({m(i2)} − {m(cash)}) = {m(cv2)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} pays {m(price)} for {m(face)} face amount of {WORDS[yrs]}-year, {c}% bonds that pay interest each December 31, a price that yields {y}%. {short} has the positive intent and ability to hold the bonds to maturity and expects no credit losses on them. It uses the effective interest method and rounds to the nearest dollar at each step. At December 31, Year 2, the bonds' fair value is {m(fv)}. At what amount should {short} report the investment at December 31, Year 2?""",
        choices, ans,
        f"""Held-to-maturity debt securities are carried at amortized cost. Year 1 interest income = {m(price)} × {y}% = {m(i1)}; cash interest {m(cash)}; discount amortized {m(i1 - cash)}; carrying amount {m(cv1)}. Year 2 interest income = {m(cv1)} × {y}% = {m(i2)}; amortization {m(i2 - cash)}; carrying amount {m(cv2)}. Fair value is disclosed, not recognized.""",
    )


def payables_rec(p):
    co, sub, mis, transit, pay = (p[k] for k in ("co", "sub", "misposted", "transit", "payment"))
    short = co.split()[0]
    gl = sub - pay - mis
    key_v = gl + mis + transit
    pool = {
        "no_t": (m(key_v - transit), f"Omits the {m(transit)} of goods shipped FOB shipping point. Title passed at shipment, so {short} owes the supplier at year-end."),
        "sub": (m(sub), f"Accepts the subledger. The subledger still includes the {m(pay)} already paid and omits the {m(transit)} of goods in transit."),
        "gl": (m(gl), f"Accepts the general ledger. It omits the {m(mis)} invoice credited to accrued liabilities and the {m(transit)} of goods in transit."),
        "no_mis": (m(gl + transit), f"Adds the goods in transit to the general ledger but leaves the {m(mis)} invoice in accrued liabilities. It is owed to a supplier, so it belongs in accounts payable."),
    }
    key = (m(key_v), f"Correct. General ledger {m(gl)} + {m(mis)} misposted invoice + {m(transit)} goods in transit; subledger {m(sub)} − {m(pay)} payment + {m(transit)} agrees.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s accounts payable subledger totals {m(sub)}, and its general ledger accounts payable control account shows {m(gl)}. Investigating, the controller finds: (1) a {m(mis)} supplier invoice was posted correctly to the supplier's subledger account, but the general ledger entry credited accrued liabilities instead of accounts payable; (2) goods costing {m(transit)} shipped by a supplier FOB shipping point on December 29 and received January 3 have not been invoiced or recorded in either record; and (3) a {m(pay)} payment to a supplier on December 30 was recorded in the general ledger but not in the supplier's subledger account. What amount should {short} report as accounts payable at December 31?""",
        choices, ans,
        f"""Reconcile both records to the correct balance. General ledger: {m(gl)} + {m(mis)} invoice credited to the wrong account + {m(transit)} goods in transit (title passed at shipment) = {m(key_v)}. Subledger: {m(sub)} − {m(pay)} payment not yet posted + {m(transit)} goods in transit = {m(key_v)}. Adjustments: reclassify {m(mis)} from accrued liabilities to accounts payable, record the {m(transit)} purchase, and post the payment to the subledger.""",
    )


def treasury_stock(p):
    co, pref, shares, cost, n1, p1, n2, p2 = (p[k] for k in ("co", "pref_apic", "shares", "cost", "n1", "p1", "n2", "p2"))
    short = co.split()[0]
    apic1 = n1 * (p1 - cost)
    loss = n2 * (cost - p2)
    key_v = max(0, loss - apic1)
    assert key_v > 0
    pool = {
        "pref_used": (m(max(0, loss - apic1 - pref)), f"Absorbs the rest of the loss with the {m(pref)} of APIC from preferred treasury transactions. Only APIC from treasury transactions in the same class of stock (common) may absorb the loss."),
        "pref_instead": (m(loss - pref), f"Uses the preferred-stock APIC ({m(pref)}) instead of the {m(apic1)} created by the first resale of common treasury shares."),
        "all_re": (m(loss), f"Charges the entire loss on the second resale to retained earnings, ignoring the {m(apic1)} of APIC from the first resale."),
        "p1_basis": (m(n2 * (p1 - p2) - apic1), f"Measures the second resale's loss against the {m(p1)} first resale price instead of the {m(cost)} cost of the treasury shares."),
    }
    key = (m(key_v), f"Correct. The {m(loss)} loss on the second resale is charged first to the {m(apic1)} of APIC from the first resale, and the remaining {m(key_v)} to retained earnings.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At the start of the year, {co}'s equity includes {m(pref)} of additional paid-in capital from earlier treasury stock transactions in its preferred stock and none from transactions in its common stock. During the year, under the cost method, {short} reacquires {n(shares)} shares of its common stock at {m(cost)} per share, later resells {n(n1)} of them at {m(p1)} per share, and later resells another {n(n2)} at {m(p2)} per share. {short} charges losses on treasury stock to paid-in capital to the maximum extent ASC 505-30 permits. What amount does {short} debit to retained earnings as a result of these transactions?""",
        choices, ans,
        f"""Cost method: treasury stock is debited at cost, {n(shares)} × {m(cost)} = {m(shares * cost)}. First resale: {n(n1)} × ({m(p1)} − {m(cost)}) = {m(apic1)} credited to APIC–treasury stock (common). Second resale: {n(n2)} × ({m(cost)} − {m(p2)}) = {m(loss)} below cost, charged first to APIC from earlier treasury transactions in the same class ({m(apic1)}) and the remaining {m(key_v)} to retained earnings. APIC from preferred-stock treasury transactions cannot absorb a loss on common shares.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def principal_agent(p):
    co, hp, fee, nights, pk, pp, pc_ = (p[k] for k in ("co", "hotel_price", "fee", "nights", "packages", "pkg_price", "pkg_cost"))
    short = co.split()[0]
    key_v = nights * fee + pk * pp
    pool = {
        "both_net": (m(nights * fee + pk * (pp - pc_)), f"Reports both lines net. {short} controls the package rooms before transfer (it bears inventory risk, sets the price and is responsible for fulfillment), so it is the principal for packages and reports them gross."),
        "reversed": (m(nights * hp + pk * (pp - pc_)), "Reports hotel bookings gross and packages net, the reverse of who controls the rooms in each line."),
        "no_hotel": (m(pk * pp), f"Reports the packages gross but recognizes nothing for hotel bookings. As an agent, {short} still earns revenue: its {m(fee)} fee per room night."),
        "both_gross": (m(nights * hp + pk * pp), f"Reports both lines gross. For hotel bookings the hotel controls the room, so {short} reports only its fee."),
    }
    key = (m(key_v), f"Correct. Hotel bookings net as agent ({n(nights)} × {m(fee)} = {m(nights * fee)}) plus tour packages gross as principal ({n(pk)} × {m(pp)} = {m(pk * pp)}).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} operates a website with two lines of business. Hotel bookings: customers book and pay {short} {m(hp)} per room night; the hotel sets the room rate, is responsible for providing the room, and bears the risk if rooms go unsold, and {short} keeps {m(fee)} of each booking and remits {m(hp - fee)} to the hotel. During the year {short} arranged {n(nights)} room nights. Tour packages: {short} buys blocks of hotel rooms months in advance under nonrefundable contracts, sets the package price, and is responsible to customers for fixing any problem with the stay. It sold {n(pk)} packages at {m(pp)} each, whose rooms cost it {m(pc_)} each. What total revenue should {short} recognize for the year?""",
        choices, ans,
        f"""An entity is a principal if it controls the good or service before transfer to the customer; indicators include primary responsibility for fulfillment, inventory risk, and pricing discretion. Hotel bookings: the hotel fulfills, bears inventory risk and sets the price, so {short} is an agent and recognizes its net fee of {m(nights * fee)}. Tour packages: {short} commits to the rooms in advance (inventory risk), sets the price and answers for the stay, so it is the principal and recognizes {m(pk * pp)} gross, with the {m(pk * pc_)} room cost in cost of sales. Total revenue = {m(key_v)}.""",
    )


def contract_costs(p):
    co, comm, legal, travel, term, renew = (p[k] for k in ("co", "comm", "legal", "travel", "term", "renew"))
    short = co.split()[0]
    life = term + renew
    half = whole(D(comm) / life / 2)
    key_v = legal + travel + half
    pool = {
        "full_year": (m(legal + travel + 2 * half), f"Amortizes a full year of the commission. Amortization begins when the contract starts on July 1, so Year 1 has half a year ({m(half)})."),
        "initial_term": (m(legal + travel + whole(D(comm) / term / 2)), f"Amortizes the commission over the {WORDS[term]}-year initial term. It is amortized over the period of expected benefit, including the anticipated renewal, since no commission is paid on renewal."),
        "expense_all": (m(legal + travel + comm), "Expenses the commission. The practical expedient to expense commissions applies only when the amortization period is one year or less."),
        "cap_legal": (m(travel + whole(D(comm + legal) / life / 2)), f"Capitalizes the {m(legal)} legal fee with the commission. Only costs incurred because the contract was obtained are capitalized; the fee was owed either way."),
    }
    key = (m(key_v), f"Correct. {m(legal)} legal + {m(travel)} travel expensed, plus {m(comm)} ÷ {life} years × ½ year = {m(half)} of amortization.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On July 1, Year 1, {co} signs a {WORDS[term]}-year contract to provide IT support. {short} expects the customer to renew it once for {WORDS[renew]} more years, and it pays no commission on renewals. In obtaining the contract, {short} paid its salesperson a {m(comm)} commission that is owed only because the contract was signed, paid outside counsel {m(legal)} to draft the contract, a fee owed whether or not the customer signed, and incurred {m(travel)} of travel costs to present its proposal, which it would also have incurred had it lost the bid. {short} amortizes capitalized contract costs straight-line. What total expense related to these costs should {short} recognize in Year 1?""",
        choices, ans,
        f"""Only incremental costs of obtaining a contract, those that would not have been incurred had the contract not been obtained, are capitalized: the {m(comm)} commission. Legal fees for drafting and proposal travel are incurred regardless and are expensed ({m(legal + travel)}). The commission is amortized over the period of expected benefit, the {WORDS[term]}-year term plus the expected {WORDS[renew]}-year renewal (no commensurate renewal commission): {m(comm)} ÷ {life} × ½ = {m(half)} in Year 1. Total expense = {m(key_v)}.""",
    )


def operating_lease_cost(p):
    co, pay1, step, yrs, idc, life = (p[k] for k in ("co", "pay1", "step", "years", "idc", "life"))
    short = co.split()[0]
    pays = [pay1 + i * step for i in range(yrs)]
    total = sum(pays)
    sl, amort = whole(D(total) / yrs), whole(D(idc) / yrs)
    key_v = sl + amort
    pool = {
        "cash": (m(pay1), "Recognizes the Year 1 cash payment. Operating lease cost is recognized straight-line over the term."),
        "cash_idc": (m(pay1 + amort), "Adds the initial direct costs' amortization to the Year 1 cash payment instead of the straight-line payment amount."),
        "no_idc": (m(sl), f"Uses straight-line payments but omits the {m(amort)} of amortization of initial direct costs, which is part of the single lease cost."),
        "idc_full": (m(sl + idc), f"Expenses all {m(idc)} of initial direct costs in Year 1. They are included in the single lease cost, recognized straight-line over the term."),
    }
    key = (m(key_v), f"Correct. Total payments {m(total)} ÷ {yrs} = {m(sl)} straight-line, plus {m(idc)} ÷ {yrs} = {m(amort)} of initial direct costs.")
    choices, ans = pick(pool, key, p["use"])
    listed = " + ".join(m(x) for x in pays)
    return variant(
        f"""On January 1, Year 1, {co} leases office equipment for {yrs} years. The equipment's economic life is {life} years, ownership stays with the lessor, there is no purchase option, the present value of the payments is 40% of the equipment's fair value, and the equipment is not specialized. Annual payments, due each December 31, are {m(pay1)} in Year 1 and increase by {m(step)} each year. {short} pays {m(idc)} of initial direct costs at commencement, and its incremental borrowing rate is 6%. What total lease cost should {short} recognize in Year 1?""",
        choices, ans,
        f"""None of the finance-lease criteria is met (no transfer of ownership or purchase option, a term that is {int(whole(D(yrs) * 100 / life))}% of economic life, present value well below substantially all of fair value, and nonspecialized equipment), so the lease is an operating lease. Its single lease cost is the total lease payments plus initial direct costs, recognized straight-line: ({listed} + {m(idc)}) ÷ {yrs} = {m(key_v)}. The discount rate affects the measurement of the liability and right-of-use asset, not the straight-line cost.""",
    )


def events_after(p):
    co, owed, collect, allow, settle, accrued, fire, bonds = (
        p[k] for k in ("co", "owed", "collect", "allow", "settle", "accrued", "fire", "bonds"))
    short = co.split()[0]
    c1, c2 = owed - collect - allow, settle - accrued
    key_v = c1 + c2
    fb = "disclose the fire and the bond issue"
    ch = lambda x, d=fb: f"{m(x)} decrease; {d}"
    pool = {
        "zero": ("$0 decrease; disclose all four events", "Treats every event as nonrecognized. The bankruptcy and the settlement give evidence about conditions that existed at year-end, so they are recognized."),
        "one_only": (ch(c2), "Adjusts for only one of the two events that give evidence about conditions existing at year-end."),
        "only_settle": (ch(c2), "Adjusts for the settlement but not the customer's bankruptcy, which resulted from difficulties that built up during Year 1."),
        "only_bank": (ch(c1), "Adjusts for the customer's bankruptcy but not the settlement, which confirms the amount of a Year 1 obligation."),
        "fire_only": (ch(key_v, "disclose the fire only"), "Omits the bond issue. A significant financing after year-end is a nonrecognized event that is disclosed."),
        "full_recv": (ch(key_v + allow), f"Charges the whole {m(owed - collect)} shortfall without using the {m(allow)} already in the allowance for this customer."),
        "fire_rec": (ch(key_v + fire, "disclose the bond issue only"), "Also recognizes the fire loss. The fire happened after year-end, so it is disclosed, not recognized."),
    }
    key = (ch(key_v), f"Correct. The customer's loss ({m(c1)} more allowance) and the settlement ({m(c2)} more accrual) are recognized; the fire and the bond issue are disclosed.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: (dollars_in(c[0]), c[0]))
    return variant(
        f"""{co}'s December 31, Year 1, statements will be issued on March 15, Year 2. Between those dates: (1) on January 25, a customer that owed {m(owed)} at year-end filed for bankruptcy because of financial difficulties that had built up over Year 1; {short} now expects to collect {m(collect)}, and its allowance included {m(allow)} for this customer; (2) on February 10, {short} settled for {m(settle)} a lawsuit over a Year 1 injury for which it had accrued {m(accrued)}; (3) on February 20, a fire destroyed an uninsured warehouse with a carrying amount of {m(fire)}; and (4) on March 1, {short} issued {m(bonds)} of bonds. What is the effect on {short}'s Year 1 pretax income, and which events require disclosure without adjustment?""",
        choices, ans,
        f"""Events that give evidence about conditions existing at the balance sheet date are recognized. The customer's bankruptcy resulted from deterioration during Year 1, so the allowance for that customer rises from {m(allow)} to {m(owed - collect)} ({m(owed)} − {m(collect)}): a {m(c1)} charge. The settlement confirms a Year 1 obligation at {m(settle)}: {m(c2)} more than accrued. Year 1 pretax income falls by {m(key_v)}. The fire and the bond issue reflect conditions arising after year-end; they are disclosed, not recognized.""",
    )


def change_in_estimate(p):
    co, cost, life, salv, yrs, rem, salv2 = (p[k] for k in ("co", "cost", "life", "salvage", "yrs", "remaining", "salvage2"))
    short = co.split()[0]
    sl = whole(D(cost - salv) / life)
    ca = cost - yrs * sl
    rate = D(2) / rem
    key_v = whole(ca * rate)
    rp = int(whole(rate * 100))
    yr = yrs + 1
    pool = {
        "sl_orig": (m(sl), f"Keeps the original straight-line depreciation. The new method and estimates apply from Year {yr}."),
        "sl_new": (m(whole(D(ca - salv2) / rem)), f"Applies the revised life and salvage value but keeps straight-line: ({m(ca)} − {m(salv2)}) ÷ {rem}."),
        "ddb_salv": (m(whole((ca - salv2) * rate)), f"Deducts the {m(salv2)} salvage value before applying the {rp}% rate. Double-declining balance ignores salvage value except as a floor."),
        "ddb_cost": (m(whole(cost * rate)), f"Applies the {rp}% rate to the original {m(cost)} cost. A change in estimate is applied to the carrying amount at the date of change."),
    }
    key = (m(key_v), f"Correct. Carrying amount {m(cost)} − {yrs} × {m(sl)} = {m(ca)}; double-declining rate 2 ÷ {rem} = {rp}%.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} bought a machine for {m(cost)}, estimated a {life}-year life and {m(salv)} salvage value, and depreciated it straight-line. On January 1, Year {yr}, after studying how the machine's benefits are consumed, {short} switches to the double-declining-balance method, which it concludes better reflects that pattern, and revises the remaining life to {rem} years and the salvage value to {m(salv2)}. What depreciation expense should {short} recognize in Year {yr}?""",
        choices, ans,
        f"""A change in depreciation method is a change in accounting estimate effected by a change in accounting principle, so it is applied prospectively to the carrying amount at the date of change. Carrying amount at January 1, Year {yr} = {m(cost)} − {yrs} × ({m(cost - salv)} ÷ {life}) = {m(ca)}. Double-declining-balance rate = 2 ÷ {rem} = {rp}%; Year {yr} depreciation = {m(ca)} × {rp}% = {m(key_v)}. Salvage value limits depreciation only in later years.""",
    )


FAMILIES = {
    "far-special-purpose-frameworks-0001": (cash_to_accrual, [
        dict(co="Dalton Consulting", cash=480000, ar0=60000, ar1=85000, wo=5000, adv0=20000, adv1=12000, use=["sub_ar", "sub_adv", "no_wo"]),
        dict(co="Everett Consulting", cash=720000, ar0=90000, ar1=120000, wo=8000, adv0=30000, adv1=18000, use=["sub_adv", "no_wo", "plus_adv1"]),
        dict(co="Fairbanks Consulting", cash=350000, ar0=40000, ar1=58000, wo=3000, adv0=15000, adv1=9000, use=["cash_only", "sub_ar", "sub_adv"]),
        dict(co="Glendale Consulting", cash=610000, ar0=75000, ar1=105000, wo=6000, adv0=25000, adv1=14000, use=["sub_ar", "no_wo", "plus_adv1"]),
    ]),
    "far-ratios-0001": (quick_ratio, [
        dict(co="Garner Co.", cash=60000, tbills=40000, trading=50000, ar=150000, inv=200000, prepaid=20000, cl=250000, use=["plus_inv", "plus_pp", "current"]),
        dict(co="Hartley Co.", cash=90000, tbills=30000, trading=80000, ar=200000, inv=260000, prepaid=30000, cl=320000, use=["cash_ratio", "no_tr", "plus_pp"]),
        dict(co="Jarrett Co.", cash=40000, tbills=20000, trading=30000, ar=110000, inv=150000, prepaid=10000, cl=125000, use=["no_tr", "plus_pp", "current"]),
        dict(co="Keaton Co.", cash=120000, tbills=60000, trading=70000, ar=250000, inv=400000, prepaid=40000, cl=500000, use=["cash_ratio", "plus_inv", "current"]),
    ]),
    "far-nfp-cash-flows-0001": (nfp_financing, [
        dict(org="Hillcrest Museum", bldg=400000, endow=250000, unres=180000, constr=300000, mort=50000, use=["bldg_op", "no_endow", "plus_unres"]),
        dict(org="Juniper Museum", bldg=600000, endow=300000, unres=220000, constr=450000, mort=80000, use=["bldg_op", "minus_constr", "no_endow"]),
        dict(org="Kestrel Museum", bldg=250000, endow=400000, unres=150000, constr=200000, mort=30000, use=["no_endow", "no_mort", "plus_unres"]),
        dict(org="Linwood Museum", bldg=500000, endow=150000, unres=300000, constr=350000, mort=60000, use=["bldg_op", "no_endow", "plus_unres"]),
    ]),
    "far-change-in-principle-0001": (change_in_principle, [
        dict(co="Tate Co.", wa1=400000, f1=450000, wa2=460000, f2=540000, t=25, use=["prosp", "open_only", "no_tax"]),
        dict(co="Daly Co.", wa1=600000, f1=680000, wa2=700000, f2=820000, t=21, use=["prosp", "whole_y2", "no_tax"]),
        dict(co="Eames Co.", wa1=300000, f1=335000, wa2=350000, f2=410000, t=30, use=["prosp", "open_only", "no_tax"]),
        dict(co="Gantt Co.", wa1=900000, f1=1000000, wa2=1050000, f2=1200000, t=25, use=["prosp", "whole_y2", "no_tax"]),
    ]),
    "far-receivables-factoring-0001": (factoring, [
        dict(co="Kemp Co.", rec=500000, fee=4, hold=10, use=["hold_loss", "fee_on_net", "hold_paid"]),
        dict(co="Lorimer Co.", rec=800000, fee=3, hold=5, use=["no_loss", "hold_loss", "hold_paid"]),
        dict(co="Merton Co.", rec=300000, fee=5, hold=8, use=["hold_loss", "fee_on_net", "hold_paid"]),
        dict(co="Nesbitt Co.", rec=1200000, fee=2, hold=10, use=["no_loss", "fee_on_net", "hold_paid"]),
    ]),
    "far-investments-htm-0001": (htm_amortized_cost, [
        dict(co="Nolan Corp.", face=500000, coupon=6, years=5, yld=7, fv_off=None, fv=490000, use=["face_yield", "sl", "fv"]),
        dict(co="Orland Corp.", face=800000, coupon=5, years=4, yld=6, fv_off=-9000, use=["one_year", "fv", "sl"]),
        dict(co="Prescott Corp.", face=1000000, coupon=7, years=6, yld=8, fv_off=12000, use=["face_yield", "sl", "fv"]),
        dict(co="Quimper Corp.", face=300000, coupon=4, years=5, yld=5, fv_off=-6000, use=["fv", "one_year", "face_yield"]),
    ]),
    "far-payables-reconciliation-0001": (payables_rec, [
        dict(co="Loring Co.", sub=412000, misposted=14000, transit=9000, payment=6000, use=["no_t", "sub", "gl"]),
        dict(co="Rainier Co.", sub=530000, misposted=21000, transit=8000, payment=15000, use=["gl", "no_t", "sub"]),
        dict(co="Sonoma Co.", sub=260000, misposted=9000, transit=12000, payment=4000, use=["gl", "no_t", "sub"]),
        dict(co="Tulare Co.", sub=715000, misposted=32000, transit=11000, payment=26000, use=["no_mis", "no_t", "sub"]),
    ]),
    "far-treasury-stock-0001": (treasury_stock, [
        dict(co="Sutton Corp.", pref_apic=3000, shares=2000, cost=30, n1=800, p1=36, n2=1000, p2=24, use=["pref_used", "pref_instead", "all_re"]),
        dict(co="Tennant Corp.", pref_apic=5000, shares=3000, cost=40, n1=1000, p1=44, n2=1500, p2=32, use=["pref_used", "pref_instead", "all_re"]),
        dict(co="Vesper Corp.", pref_apic=2000, shares=5000, cost=20, n1=2000, p1=25, n2=2500, p2=14, use=["pref_used", "pref_instead", "all_re"]),
        dict(co="Winslow Corp.", pref_apic=4000, shares=2500, cost=50, n1=600, p1=58, n2=1200, p2=44, use=["pref_used", "pref_instead", "all_re"]),
    ]),
    "far-revenue-principal-agent-0001": (principal_agent, [
        dict(co="Voya Travel", hotel_price=300, fee=45, nights=10000, packages=2000, pkg_price=900, pkg_cost=600, use=["both_net", "reversed", "no_hotel"]),
        dict(co="Wander Travel", hotel_price=250, fee=30, nights=20000, packages=3000, pkg_price=700, pkg_cost=480, use=["no_hotel", "reversed", "both_gross"]),
        dict(co="Xplore Travel", hotel_price=400, fee=60, nights=5000, packages=1500, pkg_price=1200, pkg_cost=850, use=["both_net", "no_hotel", "reversed"]),
        dict(co="Yonder Travel", hotel_price=180, fee=25, nights=30000, packages=4000, pkg_price=650, pkg_cost=420, use=["no_hotel", "reversed", "both_gross"]),
    ]),
    "far-revenue-contract-costs-0001": (contract_costs, [
        dict(co="Cobalt Services", comm=24000, legal=6000, travel=3000, term=3, renew=2, use=["full_year", "initial_term", "expense_all"]),
        dict(co="Delphi Services", comm=36000, legal=12000, travel=4000, term=4, renew=2, use=["cap_legal", "initial_term", "full_year"]),
        dict(co="Eclipse Services", comm=30000, legal=5000, travel=2000, term=2, renew=3, use=["full_year", "initial_term", "expense_all"]),
        dict(co="Fulcrum Services", comm=60000, legal=10000, travel=6000, term=3, renew=2, use=["cap_legal", "full_year", "expense_all"]),
    ]),
    "far-lessee-operating-0003": (operating_lease_cost, [
        dict(co="Yardley Co.", pay1=40000, step=2000, years=5, idc=5000, life=20, use=["cash", "cash_idc", "no_idc"]),
        dict(co="Zenith Co.", pay1=60000, step=3000, years=4, idc=8000, life=16, use=["cash", "no_idc", "idc_full"]),
        dict(co="Alder Co.", pay1=25000, step=1000, years=6, idc=3000, life=24, use=["cash", "cash_idc", "no_idc"]),
        dict(co="Birchwood Co.", pay1=90000, step=5000, years=5, idc=10000, life=25, use=["cash_idc", "no_idc", "idc_full"]),
    ]),
    "far-subsequent-events-0002": (events_after, [
        dict(co="Tamsin Co.", owed=80000, collect=20000, allow=10000, settle=150000, accrued=100000, fire=300000, bonds=1000000, use=["zero", "one_only", "fire_only"]),
        dict(co="Umber Co.", owed=120000, collect=30000, allow=15000, settle=200000, accrued=160000, fire=450000, bonds=2000000, use=["zero", "only_settle", "full_recv"]),
        dict(co="Varley Co.", owed=60000, collect=15000, allow=5000, settle=90000, accrued=70000, fire=200000, bonds=800000, use=["only_bank", "fire_only", "fire_rec"]),
        dict(co="Wyatt Co.", owed=200000, collect=50000, allow=30000, settle=300000, accrued=250000, fire=500000, bonds=3000000, use=["zero", "only_settle", "only_bank"]),
    ]),
    "far-change-in-estimate-0001": (change_in_estimate, [
        dict(co="Weller Co.", cost=800000, life=10, salvage=50000, yrs=3, remaining=5, salvage2=30000, use=["sl_orig", "sl_new", "ddb_salv"]),
        dict(co="Aldine Co.", cost=640000, life=8, salvage=40000, yrs=2, remaining=4, salvage2=20000, use=["sl_orig", "sl_new", "ddb_cost"]),
        dict(co="Barrow Co.", cost=1000000, life=10, salvage=100000, yrs=4, remaining=5, salvage2=50000, use=["sl_orig", "sl_new", "ddb_salv"]),
        dict(co="Cordell Co.", cost=450000, life=9, salvage=45000, yrs=3, remaining=8, salvage2=25000, use=["sl_new", "sl_orig", "ddb_cost"]),
    ]),
}

if __name__ == "__main__":
    run(FAMILIES, CONTENT)
