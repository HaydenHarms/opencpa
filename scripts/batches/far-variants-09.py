"""FAR variants 09: three extra versions for 10 more numeric items from FAR batch 01.

Method as in far-variants-03.py (shared helpers in variants.py). Left without variants:
far-revenue-allocation-0003, because its wrong answers fall in a fixed order around the key (discount all
to the license < key < discount spread across all three < standalone price), so the key's letter can't move.

Run: python3 scripts/batches/far-variants-09.py   See docs/reviews/far-variants-09.md.
"""
import os
from decimal import Decimal as D

from common import variant
from variants import WORDS, dollars_in, m, n, pick, rd, run, whole

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def at(pct, x):
    return whole(D(pct) / 100 * x)


def pm(x):
    """$12.00: unit prices always show cents."""
    return f"${D(str(x)):.2f}"


# ── Area II ──────────────────────────────────────────────────────────────


def ppe_rec(p):
    co, sub, cost, ad, px, frt, inc = (p[k] for k in ("co", "sub", "cost", "ad", "proceeds", "freight", "income"))
    short = co.split()[0]
    gl = sub + cost - frt
    cv = cost - ad
    gain = px - cv
    assert gain > 0
    key_v = inc - cv + frt
    pool = {
        "no_ad": (m(inc - cost + frt), f"Removes the machine's {m(cost)} cost without its {m(ad)} of accumulated depreciation, turning the {m(px)} gain into a {m(cost - px)} loss."),
        "freight_exp": (m(inc - cv), f"Corrects the sale but leaves the {m(frt)} of freight and installation in expense. Costs to bring equipment to its location and ready it for use are part of its cost."),
        "double_gain": (m(inc + frt + gain), f"Adds the correct {m(gain)} gain on top of the {m(px)} already recorded instead of replacing it."),
        "freight_only": (m(inc + frt), f"Capitalizes the freight and installation but leaves the {m(px)} gain as recorded. After the {m(cv)} carrying amount, the gain is only {m(gain)}."),
    }
    key = (m(key_v), f"Correct. The gain falls from {m(px)} to {m(gain)} ({m(px)} − {m(cv)} carrying amount), and the {m(frt)} of freight and installation is capitalized: {m(inc)} − {m(cv)} + {m(frt)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At year-end, {co}'s fixed-asset subledger shows total equipment cost of {m(sub)}, while the general ledger equipment account shows {m(gl)}. {short}'s draft pretax income is {m(inc)}. Investigating the difference, the controller finds two items. First, in October {short} sold a machine with a cost of {m(cost)} and accumulated depreciation of {m(ad)} for {m(px)} in cash, after recording depreciation through the date of sale; the subledger removed the machine, and the general ledger entry debited cash and credited gain on sale for {m(px)}. Second, {m(frt)} of freight and installation for new equipment placed in service on December 31 is included in the subledger cost but was charged to repairs expense in the general ledger. Ignore depreciation on the new equipment for the year and income taxes. What is {short}'s corrected pretax income?""",
        choices, ans,
        f"""Reconcile first: the general ledger still carries the sold machine ({m(cost)}) and is missing the capitalized freight and installation ({m(frt)}), so {m(gl)} − {m(cost)} + {m(frt)} = {m(sub)} agrees with the subledger. Sale: the carrying amount was {m(cost)} − {m(ad)} = {m(cv)}, so the gain is {m(px)} − {m(cv)} = {m(gain)}, not {m(px)}; correcting it reduces income by {m(cv)} (Dr Accumulated depreciation {m(ad)}, Dr Gain {m(cv)}, Cr Equipment {m(cost)}). Freight and installation are costs of getting the asset ready for use, so capitalizing them increases income by {m(frt)}. Corrected pretax income: {m(inc)} − {m(cv)} + {m(frt)} = {m(key_v)}.""",
    )


def exchange(p):
    co, bv, fv, cash = (p[k] for k in ("co", "bv", "fv", "cash"))
    short = co.split()[0]
    gain, new = fv - bv, fv + cash
    assert gain > 0
    both = lambda g, e: f"{m(g)} gain; new equipment {m(e)}"
    pool = {
        "carryover": (f"$0 gain; new equipment {m(bv + cash)}", f"Carryover-basis treatment, which applies only when an exchange lacks commercial substance. Replacing a discontinued line with a different product sold under new contracts changes {short}'s future cash flows significantly."),
        "ignore_cash": (both(new - bv, new), f"Compares the new asset's fair value to the old book value and ignores the {m(cash)} of cash paid."),
        "mixed": (both(gain, bv + cash), "Mixes the two methods: recognizes the gain but records the asset at carryover basis."),
        "fv_only": (both(gain, fv), f"Recognizes the gain but records the new equipment at the old machinery's {m(fv)} fair value, leaving out the {m(cash)} of cash paid."),
    }
    key = (both(gain, new), f"Correct. The new equipment serves a different product, customers, and pricing, so {short}'s future cash flows change significantly and the exchange has commercial substance: the gain is fair value minus book value of the asset given up, and the new asset is recorded at fair value.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: (dollars_in(c[0]), c[0]))
    return variant(
        f"""{co} exchanges old machinery (book value {m(bv)}; fair value {m(fv)}) plus {m(cash)} cash for new equipment with a fair value of {m(new)}. The old machinery stamped metal brackets for a product line {short} is discontinuing; the new equipment will mold plastic housings for a different customer base, under three-year supply contracts at different volumes and prices. What gain does {short} recognize, and at what amount is the new equipment recorded?""",
        choices, ans,
        f"""An exchange has commercial substance when the entity's future cash flows are expected to change significantly as a result of it. Here the new equipment makes a different product for different customers at different volumes and prices, so the risk, timing, and amount of its cash flows differ from the old machinery's. With commercial substance, the exchange is measured at fair value. Gain = {m(fv)} fair value − {m(bv)} book value = {m(gain)}. The new equipment is recorded at {m(fv)} + {m(cash)} cash = {m(new)}, which equals its fair value.""",
    )


def lcnrv(p):
    co = p["co"]
    short = co.split()[0]
    prods = p["products"]  # [(name, qty, cost, price, ctc, repl)]
    rows = []
    for name, q, c, s, k, r in prods:
        c, s, k, r = (D(str(x)) for x in (c, s, k, r))
        nrv = s - k
        rows.append((name, q, c, s, k, r, nrv, max(D(0), c - nrv) * q, max(D(0), c - r) * q))
    key_v = sum(x[7] for x in rows)
    tot_cost = sum(x[1] * x[2] for x in rows)
    tot_nrv = sum(x[1] * x[6] for x in rows)
    agg = max(D(0), tot_cost - tot_nrv)
    repl = sum(x[8] for x in rows)
    a, b, c_ = rows
    assert a[7] > 0 and b[7] > 0 and c_[7] == 0 and all(x[3] > x[2] for x in rows)
    sa, sb = a[2] - a[6], b[2] - b[6]
    below = (f"Products {a[0]} and {b[0]} are each {pm(sa)} per unit below cost" if sa == sb
             else f"Product {a[0]} is {pm(sa)} and Product {b[0]} {pm(sb)} per unit below cost")
    pool = {
        "price_only": ("$0", "Compares selling price with cost and ignores the costs to complete and sell that net realizable value subtracts. Every selling price exceeds its cost, so this test finds no write-down."),
        "aggregate": (m(agg), f"Applies the test to the inventory as a whole: total cost {m(tot_cost)} against total NRV {m(tot_nrv)}. {short} applies the test product by product, so Product {c_[0]}'s surplus cannot offset the shortfalls."),
        "replacement": (m(repl), "Measures the shortfall against replacement cost, the old lower-of-cost-or-market approach. FIFO and average-cost inventory use NRV; replacement cost applies only to LIFO and the retail inventory method."),
    }
    key = (m(key_v), f"Correct. NRV is selling price less costs to complete and sell; {below}, and Product {c_[0]} is not written down.")
    choices, ans = pick(pool, key, p["use"])
    desc = lambda x: (f"Product {x[0]} has {n(x[1])} units with FIFO cost of {pm(x[2])}, selling price of {pm(x[3])}, "
                      f"cost to complete and sell of {pm(x[4])}, and replacement cost of {pm(x[5])} per unit.")
    line = lambda x, below_: (f"Product {x[0]}: NRV {pm(x[3])} − {pm(x[4])} = {pm(x[6])}, below cost by {pm(x[2] - x[6])} × {n(x[1])} = {m(x[7])}."
                              if below_ else
                              f"Product {x[0]}: NRV {pm(x[3])} − {pm(x[4])} = {pm(x[6])}, above the {pm(x[2])} cost, so no write-down and no write-up.")
    return variant(
        f"""{co} uses FIFO and applies the lower of cost and net realizable value to each product separately. At year-end: {desc(a)} {desc(b)} {desc(c_)} What inventory write-down should {short} recognize?""",
        choices, ans,
        f"""For FIFO or average-cost inventory, measure each product at the lower of cost and NRV. {line(a, True)} {line(b, True)} {line(c_, False)} Total write-down: {m(key_v)}.""",
    )


def afs_credit_loss(p):
    co, ac, a0, fv, pv = (p[k] for k in ("co", "ac", "allow", "fv", "pv"))
    short = co.split()[0]
    decline = ac - fv
    capped = ac - pv > decline
    credit = min(ac - pv, decline)
    key_v = credit - a0
    pool = {
        "full": (m(credit), f"Records the full credit loss as this year's expense and ignores the {m(a0)} already in the allowance."),
        "whole_less": (m(decline - a0), f"Treats the whole {m(decline)} decline below amortized cost as a credit loss, less the existing allowance. The {m(decline - credit)} of the decline not explained by expected cash flows goes to OCI."),
        "whole": (m(decline), "Recognizes the whole decline in earnings, as if the securities were trading, and ignores the existing allowance."),
        "zero": ("$0", f"Recognizes no credit loss because {short} does not intend to sell. The intent-to-sell test decides whether the whole decline goes to earnings; a credit loss is recognized either way."),
        "no_cap": (m(ac - pv - a0), f"Ignores the fair value floor. The allowance for an available-for-sale debt security is limited to the {m(decline)} by which fair value is below amortized cost."),
    }
    if capped:
        key = (m(key_v), f"Correct. The credit loss of {m(ac - pv)} is limited to the {m(decline)} by which fair value is below amortized cost; the allowance already holds {m(a0)}, so Year 2 expense is {m(key_v)}.")
        tail = f"{m(ac)} − {m(pv)} = {m(ac - pv)}, limited to the {m(decline)} by which fair value is below amortized cost. The allowance is adjusted from {m(a0)} to {m(credit)}, so Year 2 credit loss expense is {m(key_v)}. None of the decline is left for other comprehensive income."
    else:
        key = (m(key_v), f"Correct. The allowance must be {m(credit)} ({m(ac)} − {m(pv)}); it already holds {m(a0)}, so Year 2 expense is {m(key_v)}.")
        tail = f"{m(ac)} − {m(pv)} = {m(credit)}, within the {m(decline)} limit. The allowance is adjusted from {m(a0)} to {m(credit)}, so Year 2 credit loss expense is {m(key_v)}. The remaining {m(decline - credit)} of the decline ({m(decline)} − {m(credit)}) is reported in other comprehensive income."
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} holds available-for-sale debt securities whose amortized cost was {m(ac)} at the end of both Year 1 and Year 2. At the end of Year 1, {short} recorded a {m(a0)} allowance for credit losses on them. At the end of Year 2, their fair value is {m(fv)}, and the present value of the cash flows {short} expects to collect, discounted at the securities' effective interest rate, is {m(pv)}. {short} does not intend to sell the securities, and it is not more likely than not that it will be required to sell them before recovering their amortized cost. What credit loss expense should {short} recognize in net income for Year 2?""",
        choices, ans,
        f"""For an AFS debt security the holder neither intends nor is likely to be required to sell, the credit loss is amortized cost minus the present value of expected cash flows, limited to the amount by which fair value is below amortized cost: {tail}""",
    )


def cecl_allowance(p):
    co, correct, dup, memo, bank, recov, hist, fwd, bal = (
        p[k] for k in ("co", "correct", "dup", "memo", "bankrupt", "recover", "hist", "fwd", "allow"))
    short = co.split()[0]
    gl, sub = correct + dup, correct + memo
    pool_amt = correct - bank
    rate = hist + fwd
    specific = at(100 - recov, bank)
    req = specific + at(rate, pool_amt)
    key_v = req - bal
    pts = f"{fwd} percentage point{'s' if fwd != 1 else ''}"
    pool = {
        "hist": (m(specific + at(hist, pool_amt) - bal), f"Uses the {hist}% historical rate for the pool. Expected credit losses must reflect reasonable and supportable forecasts, which raise the rate to {rate}%."),
        "uncorrected": (m(specific + at(rate, gl - bank) - bal), f"Uses the unadjusted control account ({m(gl)}, a pool of {m(gl - bank)}). The duplicated {m(dup)} batch is not a real receivable."),
        "no_bal": (m(req), f"Records the whole required allowance as expense and ignores the {m(bal)} credit balance already in the allowance."),
        "pool_all": (m(at(rate, correct) - bal), f"Applies the {rate}% rate to all {m(correct)}, including the bankrupt customer. A customer with different risk characteristics is evaluated on its own."),
    }
    key = (m(key_v), f"Correct. The corrected receivables balance is {m(correct)}, so the pool is {m(pool_amt)}. Required allowance {m(specific)} + {m(pool_amt)} × {rate}% = {m(req)}, less the {m(bal)} already in the allowance.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At year-end, {co}'s accounts receivable subledger totals {m(sub)}, and the general ledger control account shows {m(gl)}. {short}'s investigation finds two reconciling items, both involving customers in its main customer pool: the December 18 sales journal batch of {m(dup)} was posted to the control account twice, and a {m(memo)} credit memo for goods returned on December 30 was posted to the control account but not to the customer's subledger account. Of the correct receivables balance, {m(bank)} is owed by one customer that has filed for bankruptcy; {short} expects to collect {recov}% of that balance in the proceedings. The remaining balances are owed by customers with similar credit profiles. {short}'s historical loss rate on such balances is {hist}%, and its reasonable and supportable forecast indicates losses {pts} above that rate. {short} does not elect the practical expedient for current trade receivables in ASU 2025-05. Before adjustment, the allowance for credit losses has a {m(bal)} credit balance. After the reconciling items are corrected, what credit loss expense should {short} record for the year?""",
        choices, ans,
        f"""First reconcile. The control account is overstated by the duplicated {m(dup)} batch: {m(gl)} − {m(dup)} = {m(correct)}. The subledger is overstated by the unposted {m(memo)} credit memo: {m(sub)} − {m(memo)} = {m(correct)}. Both records agree at {m(correct)} after correction, so the pool is {m(correct)} − {m(bank)} = {m(pool_amt)}. Under the current expected credit loss model, the bankrupt customer is evaluated on its own: {m(bank)} × {100 - recov}% = {m(specific)}. The pool's historical {hist}% is adjusted for the forecast to {rate}%: {m(pool_amt)} × {rate}% = {m(at(rate, pool_amt))}. Required allowance = {m(req)}; with a {m(bal)} credit balance already recorded, credit loss expense is {m(key_v)}.""",
    )


def cloud_costs(p):
    co, ev, cfg, conv, train, term, renew = (p[k] for k in ("co", "eval", "config", "conversion", "training", "term", "renew"))
    short = co.split()[0]
    life = term + renew
    half = lambda base, yrs: whole(D(base) / yrs / 2)
    exp = ev + conv + train
    key_v = exp + half(cfg, life)
    pool = {
        "cap_conv": (m(ev + train + half(cfg + conv, life)), f"Capitalizes the {m(conv)} of data conversion with the configuration costs ({m(ev)} + {m(train)} + {m(cfg + conv)} ÷ {life} × ½). Data conversion costs are expensed as incurred."),
        "term_only": (m(exp + half(cfg, term)), f"Amortizes over the {term}-year noncancellable term. The term includes renewal periods {short} is reasonably certain to exercise, so it is {life} years."),
        "full_year": (m(exp + whole(D(cfg) / life)), "Amortizes for the full year. Amortization begins when the software is ready for its intended use on July 1."),
        "cap_eval": (m(conv + train + half(cfg + ev, life)), f"Capitalizes the {m(ev)} of vendor evaluation. Costs of evaluating and selecting a vendor come before the project and are expensed as incurred."),
        "expense_all": (m(ev + cfg + conv + train), f"Expenses the {m(cfg)} of configuration, coding, and testing. Application-development costs of a hosting arrangement are capitalized."),
    }
    key = (m(key_v), f"Correct. {m(ev)} + {m(conv)} + {m(train)} expensed as incurred, plus {m(cfg)} ÷ {life} years × ½ year = {m(half(cfg, life))} of amortization.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} signs a noncancellable {term}-year contract to access a vendor's cloud-hosted ERP software. {short} has no right to take possession of the software, and it is reasonably certain to exercise its option to renew the contract for {renew} more years. Before the software became ready for its intended use on July 1, Year 1, {short} incurred these costs: {m(ev)} to evaluate vendors before selecting this one; {m(cfg)} for configuration, coding, and testing of interfaces; {m(conv)} to convert and cleanse legacy data; and {m(train)} to train employees. {short} amortizes capitalized costs straight-line. Excluding the hosting fees, what total expense should {short} recognize in Year 1 related to these costs?""",
        choices, ans,
        f"""A cloud computing arrangement without a right to take possession of the software is a service contract, and its implementation costs are capitalized or expensed as for internal-use software. Evaluating and selecting a vendor ({m(ev)}) happens before the entity commits to a project, and data conversion ({m(conv)}) and training ({m(train)}) are not costs of developing the software, so all three are expensed as incurred. (ASU 2025-06, which removes the project-stage model from ASC 350-40, does not change these conclusions.) Application-development costs (configuration, coding, and testing, {m(cfg)}) are capitalized and amortized straight-line over the term of the arrangement, including renewals {short} is reasonably certain to exercise ({life} years), starting when the software is ready for its intended use: {m(cfg)} ÷ {life} × ½ = {m(half(cfg, life))}. Total Year 1 expense: {m(ev)} + {m(conv)} + {m(train)} + {m(half(cfg, life))} = {m(key_v)}.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def nfp_contributions(p):
    org, face, pv, schol, spent, cond, unres = (p[k] for k in ("org", "face", "pv", "schol", "spent", "cond", "unres"))
    short = org.split()[0]
    key_v = pv + schol - spent
    pool = {
        "face": (m(face + schol - spent), f"Measures the promise at its {m(face)} face amount. A promise due in a future period is recorded at present value."),
        "no_release": (m(pv + schol), f"Reports the restricted contributions only and leaves out the {m(spent)} release. Spending on the donor's purpose moves that amount out of net assets with donor restrictions, so the net change is smaller."),
        "cond_in": (m(key_v + cond), f"Counts the {m(cond)} as revenue with donor restrictions. Because the donor can recover it until the matching gifts are raised, it is a refundable advance (a liability), not revenue."),
        "plus_unres": (m(key_v + unres), f"Also counts the {m(unres)} gift with no donor stipulations. It increases net assets without donor restrictions."),
        "no_promise": (m(schol - spent), "Leaves out the promise because it is not due until Year 3. An unconditional promise is recognized when made, with a time restriction."),
    }
    key = (m(key_v), f"Correct. {m(pv)} for the promise (restricted by time) + {m(schol)} for the scholarship gift − {m(spent)} released when the scholarships were funded. The {m(cond)} is a refundable advance, and the {m(unres)} gift is without donor restrictions.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, has these transactions in Year 1. (1) On December 31 it receives a written promise of {m(face)} payable on January 1, Year 3; nothing else is required of the foundation to receive it, and the donor states no use for the money. The promise has a present value of {m(pv)}. (2) It receives {m(schol)} in cash that the donor requires to be used for scholarships, and it spends {m(spent)} on qualifying scholarships during Year 1. (3) It receives {m(cond)} in cash under an agreement that lets the donor recover the money if the foundation does not raise {m(cond)} of matching gifts by the end of Year 2. By December 31, Year 1, the foundation has raised no matching gifts. (4) It receives a {m(unres)} cash gift with no donor stipulations. The foundation reports every restricted gift as with donor restrictions when received, even if the restriction is met in the same period. Ignoring interest accretion, what is the net change in net assets with donor restrictions for Year 1?""",
        choices, ans,
        f"""The {m(face)} promise carries no condition other than the passage of time, so it is recognized now at present value ({m(pv)}) as an increase in net assets with donor restrictions (time restriction). The {m(schol)} scholarship gift is restricted to a purpose; spending {m(spent)} on it releases that amount, leaving a {m(schol - spent)} net increase. The {m(cond)} depends on a measurable barrier (matching gifts) and includes a right of return, so it is not revenue until the barrier is overcome; the cash is a refundable advance. The {m(unres)} gift is without donor restrictions. Net change in net assets with donor restrictions: {m(pv)} + {m(schol)} − {m(spent)} = {m(key_v)} increase.""",
    )


def finance_lease_y2(p):
    co, liab, pay, rate, yrs = (p[k] for k in ("co", "liab", "pay", "rate", "years"))
    short = co.split()[0]
    i1 = whole(D(liab) * rate / 100)
    l1 = liab - (pay - i1)
    i2 = whole(D(l1) * rate / 100)
    amort = whole(D(liab) / yrs)
    key_v = i2 + amort
    pool = {
        "y1_int": (m(i1 + amort), f"Uses Year 1 interest ({m(i1)}) without reducing the liability for the Year 1 principal payment."),
        "amort_only": (m(amort), "Includes only amortization. A finance lease also has interest expense."),
        "cash": (m(pay), "Treats the cash payment as the expense."),
        "int_only": (m(i2), "Includes only interest. A finance lease also amortizes the right-of-use asset."),
        "cash_amort": (m(pay + amort), "Adds the cash payment and the amortization. The payment reduces the liability; only its interest portion is an expense."),
    }
    key = (m(key_v), f"Correct. Year 2 interest of {m(i2)} on a {m(l1)} opening liability, plus {m(amort)} of amortization.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} commences a {yrs}-year finance lease. The lease liability at commencement is {m(liab)} (rounded), the annual payment of {m(pay)} is due each December 31, and the discount rate is {rate}%. The right-of-use asset is amortized straight-line over the lease term. What total lease-related expense does {short} recognize in Year 2?""",
        choices, ans,
        f"""Year 1: interest {m(i1)}, principal reduction {m(pay - i1)}, ending liability {m(l1)}. Year 2: interest = {m(l1)} × {rate}% = {m(i2)}. Amortization = {m(liab)} ÷ {yrs} = {m(amort)}. Total Year 2 expense = {m(key_v)}.""",
    )


def highest_best_use(p):
    co, cur, done, build, profit = (p[k] for k in ("co", "current", "completed", "construction", "profit"))
    short = co.split()[0]
    key_v = done - build - profit
    assert key_v > cur
    pool = {
        "current": (m(cur), f"Measures the land at value in {short}'s intended use. Fair value assumes the use a market participant would make, not the entity's own plans."),
        "no_profit": (m(done - build), "Deducts the construction costs but not the profit a market-participant developer would require."),
        "completed": (m(done), "Uses the completed project's value and ignores the cost and required profit of developing it."),
        "no_build": (m(done - profit), "Deducts the developer's required profit but not the construction costs of completing the project."),
    }
    key = (m(key_v), f"Correct. {m(done)} − {m(build)} construction − {m(profit)} developer profit.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} owns land that it uses as a parking lot and intends to keep using that way. The present value of the parking cash flows is {m(cur)}. Local zoning allows condominiums on the site. A market-participant developer could complete a condominium project there, which would be worth {m(done)} to market participants, and completing it would take {m(build)} of construction costs plus {m(profit)} for the profit a market-participant developer would require. {short} must determine the land's fair value under ASC 820. What is the fair value?""",
        choices, ans,
        f"""Fair value reflects the use of the asset by market participants that would maximize its value, provided that use is physically possible, legally permissible, and financially feasible. Zoning permits the development and it is feasible, so the land is valued as development land. A market participant would pay the completed value less the costs and required profit: {m(done)} − {m(build)} − {m(profit)} = {m(key_v)}, which exceeds the {m(cur)} value in {short}'s current use.""",
    )


def tax_expense(p):
    co, pre, ex, fines, war, dep, t, va = (p[k] for k in ("co", "pretax", "exempt", "fines", "warranty", "dep", "t", "va"))
    short = co.split()[0]
    taxable = pre - ex + fines + war - dep
    tx = lambda x: whole(D(x) * t / 100)
    cur, dta, dtl = tx(taxable), tx(war), tx(dep)
    deferred = dtl - dta + va
    key_v = cur + deferred
    pool = {
        "va_sub": (m(cur + dtl - dta - va), "Subtracts the valuation allowance from deferred tax expense. An allowance increases deferred tax expense."),
        "no_va": (m(cur + dtl - dta), f"Omits the valuation allowance ({m(cur)} current + {m(dtl)} − {m(dta)} deferred)."),
        "no_perm": (m(tx(pre + war - dep) + deferred), f"Ignores the permanent differences and computes current tax on {m(pre + war - dep)} of taxable income ({m(tx(pre + war - dep))} current + {m(deferred)} deferred)."),
        "dta_sign": (m(cur + dtl + dta + va), f"Adds the {m(dta)} deferred tax asset to deferred tax expense. A deferred tax asset reduces deferred tax expense."),
    }
    key = (m(key_v), f"Correct. {m(cur)} current + {m(deferred)} deferred ({m(dtl)} liability − {m(dta)} asset + {m(va)} allowance).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""In its first year of operations, {co} reports pretax book income of {m(pre)}. Book income includes {m(ex)} of tax-exempt municipal bond interest and is after deducting {m(fines)} of nondeductible fines. It is also after warranty expense of {m(war)} that is not deductible until claims are paid, and no claims were paid this year. Tax depreciation exceeded book depreciation by {m(dep)}. The enacted tax rate is {t}% for all years, and {short} has no other differences. Based on its forecast of taxable income, management concludes that it is more likely than not that {m(va)} of the deferred tax asset will not be realized. What is {short}'s total income tax expense?""",
        choices, ans,
        f"""Taxable income = {m(pre)} − {m(ex)} (tax-exempt interest, permanent) + {m(fines)} (nondeductible fines, permanent) + {m(war)} (warranty, deductible later) − {m(dep)} (excess tax depreciation) = {m(taxable)}; current tax = {m(cur)}. Deferred: warranty gives a deferred tax asset of {m(war)} × {t}% = {m(dta)}, depreciation gives a deferred tax liability of {m(dep)} × {t}% = {m(dtl)}, and the valuation allowance adds {m(va)} of expense: {m(dtl)} − {m(dta)} + {m(va)} = {m(deferred)}. Total income tax expense = {m(cur)} + {m(deferred)} = {m(key_v)}.""",
    )


FAMILIES = {
    "far-ppe-reconciliation-0001": (ppe_rec, [
        dict(co="Ashby Co.", sub=2450000, cost=60000, ad=48000, proceeds=15000, freight=10000, income=400000, use=["no_ad", "freight_exp", "double_gain"]),
        dict(co="Barclay Co.", sub=3800000, cost=90000, ad=60000, proceeds=45000, freight=18000, income=650000, use=["freight_exp", "freight_only", "double_gain"]),
        dict(co="Carroway Co.", sub=1200000, cost=40000, ad=25000, proceeds=20000, freight=6000, income=220000, use=["no_ad", "freight_exp", "double_gain"]),
        dict(co="Dunstan Co.", sub=5500000, cost=150000, ad=110000, proceeds=70000, freight=25000, income=900000, use=["freight_exp", "double_gain", "freight_only"]),
    ]),
    "far-ppe-exchange-0001": (exchange, [
        dict(co="Harwick Corp.", bv=180000, fv=210000, cash=40000, use=["carryover", "ignore_cash", "mixed"]),
        dict(co="Ivanhoe Corp.", bv=300000, fv=360000, cash=50000, use=["carryover", "fv_only", "mixed"]),
        dict(co="Jardine Corp.", bv=95000, fv=110000, cash=25000, use=["carryover", "mixed", "ignore_cash"]),
        dict(co="Kerrigan Corp.", bv=520000, fv=600000, cash=70000, use=["carryover", "mixed", "fv_only"]),
    ]),
    "far-inventory-lcnrv-0001": (lcnrv, [
        dict(co="Crestview Co.", products=[("A", 1000, "12.00", "14.50", "3.00", "11.20"), ("B", 2000, "8.00", "10.00", "2.50", "7.60"), ("C", 500, "20.00", "25.00", "4.00", "20.50")], use=["price_only", "aggregate", "replacement"]),
        dict(co="Elkhart Co.", products=[("A", 800, "15.00", "18.00", "3.60", "14.90"), ("B", 1500, "9.00", "11.00", "2.40", "8.95"), ("C", 400, "30.00", "38.00", "7.50", "31.00")], use=["price_only", "aggregate", "replacement"]),
        dict(co="Gresley Co.", products=[("A", 2000, "6.00", "7.50", "1.80", "5.20"), ("B", 1200, "10.00", "12.00", "2.50", "9.40"), ("C", 300, "40.00", "50.00", "8.00", "41.00")], use=["price_only", "aggregate", "replacement"]),
        dict(co="Halsted Co.", products=[("A", 600, "25.00", "30.00", "5.75", "24.10"), ("B", 2500, "4.00", "5.00", "1.20", "3.95"), ("C", 1000, "12.00", "15.00", "2.60", "12.50")], use=["price_only", "aggregate", "replacement"]),
    ]),
    "far-investments-afs-credit-loss-0002": (afs_credit_loss, [
        dict(co="Foxworth Inc.", ac=100000, allow=2000, fv=88000, pv=93000, use=["full", "whole_less", "whole"]),
        dict(co="Glover Inc.", ac=250000, allow=5000, fv=226000, pv=238000, use=["zero", "full", "whole"]),
        dict(co="Hampden Inc.", ac=80000, allow=1500, fv=74000, pv=71000, use=["zero", "full", "no_cap"]),
        dict(co="Ivory Inc.", ac=400000, allow=10000, fv=360000, pv=375000, use=["full", "whole_less", "whole"]),
    ]),
    "far-receivables-credit-losses-0002": (cecl_allowance, [
        dict(co="Orchard Supply Co.", correct=1000000, dup=18000, memo=7000, bankrupt=150000, recover=30, hist=3, fwd=1, allow=25000, use=["hist", "uncorrected", "no_bal"]),
        dict(co="Juniper Supply Co.", correct=2000000, dup=30000, memo=12000, bankrupt=300000, recover=40, hist=2, fwd=1, allow=40000, use=["pool_all", "hist", "no_bal"]),
        dict(co="Kendall Supply Co.", correct=600000, dup=12000, memo=5000, bankrupt=80000, recover=25, hist=4, fwd=1, allow=20000, use=["hist", "uncorrected", "no_bal"]),
        dict(co="Lambert Supply Co.", correct=1500000, dup=25000, memo=9000, bankrupt=200000, recover=20, hist=3, fwd=2, allow=30000, use=["pool_all", "hist", "uncorrected"]),
    ]),
    "far-intangibles-cloud-computing-0001": (cloud_costs, [
        dict(co="Lark Co.", eval=25000, config=180000, conversion=30000, training=20000, term=3, renew=2, use=["cap_conv", "term_only", "full_year"]),
        dict(co="Mabry Co.", eval=36000, config=300000, conversion=60000, training=30000, term=4, renew=2, use=["term_only", "full_year", "expense_all"]),
        dict(co="Nance Co.", eval=20000, config=150000, conversion=25000, training=15000, term=3, renew=2, use=["cap_conv", "cap_eval", "term_only"]),
        dict(co="Orvis Co.", eval=30000, config=264000, conversion=48000, training=25000, term=4, renew=2, use=["cap_conv", "term_only", "full_year"]),
    ]),
    "far-nfp-contributions-0001": (nfp_contributions, [
        dict(org="Harbor Arts Foundation", face=80000, pv=72000, schol=60000, spent=25000, cond=150000, unres=100000, use=["face", "no_release", "cond_in"]),
        dict(org="Cypress Arts Foundation", face=120000, pv=106000, schol=90000, spent=40000, cond=200000, unres=150000, use=["no_promise", "face", "no_release"]),
        dict(org="Dunes Arts Foundation", face=50000, pv=46000, schol=40000, spent=30000, cond=100000, unres=60000, use=["no_release", "cond_in", "plus_unres"]),
        dict(org="Estuary Arts Foundation", face=200000, pv=178000, schol=75000, spent=50000, cond=250000, unres=120000, use=["no_promise", "no_release", "plus_unres"]),
    ]),
    "far-lessee-finance-0001": (finance_lease_y2, [
        dict(co="Reeves Corp.", liab=200000, pay=50000, rate=8, years=5, use=["y1_int", "amort_only", "cash"]),
        dict(co="Prentiss Corp.", liab=200000, pay=56400, rate=5, years=4, use=["int_only", "amort_only", "cash"]),
        dict(co="Quigley Corp.", liab=190000, pay=50000, rate=10, years=5, use=["amort_only", "y1_int", "int_only"]),
        dict(co="Rowntree Corp.", liab=295000, pay=70000, rate=6, years=5, use=["amort_only", "int_only", "y1_int"]),
    ]),
    "far-fair-value-highest-best-use-0001": (highest_best_use, [
        dict(co="Clover Corp.", current=1900000, completed=2900000, construction=450000, profit=150000, use=["current", "no_profit", "completed"]),
        dict(co="Eldridge Corp.", current=3200000, completed=5000000, construction=900000, profit=300000, use=["current", "no_profit", "completed"]),
        dict(co="Fairmont Corp.", current=800000, completed=1600000, construction=450000, profit=120000, use=["current", "no_profit", "completed"]),
        dict(co="Glenwood Corp.", current=2500000, completed=4200000, construction=1000000, profit=250000, use=["no_profit", "no_build", "completed"]),
    ]),
    "far-income-taxes-deferred-0001": (tax_expense, [
        dict(co="Ridgeway Corp.", pretax=500000, exempt=30000, fines=40000, warranty=120000, dep=200000, t=25, va=12000, use=["va_sub", "no_va", "no_perm"]),
        dict(co="Stanhope Corp.", pretax=800000, exempt=50000, fines=20000, warranty=160000, dep=240000, t=21, va=15000, use=["va_sub", "no_va", "no_perm"]),
        dict(co="Thornbury Corp.", pretax=300000, exempt=10000, fines=25000, warranty=60000, dep=100000, t=25, va=8000, use=["va_sub", "no_perm", "dta_sign"]),
        dict(co="Ulverston Corp.", pretax=1000000, exempt=80000, fines=30000, warranty=200000, dep=400000, t=25, va=20000, use=["no_va", "no_perm", "dta_sign"]),
    ]),
}

if __name__ == "__main__":
    run(FAMILIES, CONTENT)
