"""FAR variants 02: three extra versions for 12 numeric items from FAR batches 03 and 04.

Same method as far-variants-01.py (parameter set 0 must rebuild the reviewed item word for word), plus
distractor pools: each family has four or five distractors, each tied to a named error, and each version
shows three of them (`use`). Choosing different distractors moves the key's letter between versions, so a
student can't answer a repeat by remembering the position. The script refuses to write unless the key
letter differs across a family's versions.

Run: python3 scripts/batches/far-variants-02.py  (adds `variants` to the 12 files in content/far/)
See docs/reviews/far-variants-02.md.
"""
import os
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from math import gcd

import yaml

from common import attach_variants, audit, variant

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
         9: "nine", 10: "ten"}


def rd(x):
    """Round to whole dollars, half up."""
    return D(x).quantize(D("1"), ROUND_HALF_UP)


def m(x):
    """$1,234 (or $1,234.56 when there are cents)."""
    x = D(x).quantize(D("0.01"), ROUND_HALF_UP)
    return f"${x:,.0f}" if x == x.to_integral() else f"${x:,.2f}"


def n(x):
    return f"{D(x):,.0f}"


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole amount, got {x}"
    return x


def pct(x):
    """30% or 33.3%."""
    x = D(x) * 100
    return f"{x:.0f}%" if x == x.to_integral() else f"{x.quantize(D('0.1'), ROUND_HALF_UP)}%"


def pick(pool, key, use, order=None):
    """The choice list for one version: the distractors named in `use`, then the key.

    Returns (choices, answer letter). `order` sorts the list first (for choices without a $ amount,
    which finalize() can only sort on their first number).
    """
    items = [pool[k] for k in use] + [key]
    if order:
        items.sort(key=order)
    return items, "ABCDE"[items.index(key)]


# ── Area I ───────────────────────────────────────────────────────────────


def pe_payout(p):
    co, ni, pd, cd, s, price = (p[k] for k in ("co", "ni", "pd", "cd", "s", "price"))
    short = co.split()[0]
    eac = ni - pd
    eps = D(eac) / s
    pe = (D(price) / eps).quantize(D("0.1"), ROUND_HALF_UP)
    eps_bad = D(ni) / s
    pe_bad = (D(price) / eps_bad).quantize(D("0.1"), ROUND_HALF_UP)
    pay, pay_bad, pay_all = pct(D(cd) / eac), pct(D(cd) / ni), pct(D(cd + pd) / eac)
    both = lambda a, b: f"{a} P/E; {b} payout"
    pool = {
        "both": (both(pe_bad, pay_bad), "Uses net income without deducting preferred dividends for both ratios. Both are based on earnings available to common shareholders."),
        "pe_nopref": (both(pe_bad, pay), f"Computes EPS without deducting the {m(pd)} of preferred dividends (${eps_bad:.2f}), which understates the P/E ratio."),
        "pay_total": (both(pe, pay_bad), "Gets the P/E ratio right but divides common dividends by total net income for the payout ratio."),
        "pay_all": (both(pe, pay_all), f"Includes the {m(pd)} of preferred dividends in the payout ratio. The ratio covers dividends to common shareholders only."),
    }
    key = (both(pe, pay), f"Correct. EPS = ({m(ni)} − {m(pd)}) ÷ {n(s)} = ${eps:.2f}; P/E = {m(price)} ÷ ${eps:.2f} = {pe}; payout = {m(cd)} ÷ {m(eac)} = {pay}.")
    nums = lambda c: tuple(float(x.rstrip("%")) for x in (c[0].split()[0], c[0].split("; ")[1].split()[0]))
    choices, ans = pick(pool, key, p["use"], order=nums)
    return variant(
        f"""{co} reports net income of {m(ni)} for the year. It declared {m(pd)} of dividends on its preferred stock and {m(cd)} of dividends on its common stock. Weighted-average common shares outstanding were {n(s)}, and the common stock's market price at year-end is {m(price)}. {short} computes the dividend payout ratio on earnings available to common shareholders. What are {short}'s price-to-earnings ratio and dividend payout ratio?""",
        choices, ans,
        f"""Earnings available to common = {m(ni)} − {m(pd)} preferred dividends = {m(eac)}; EPS = ${eps:.2f}. Price-to-earnings ratio = {m(price)} ÷ ${eps:.2f} = {pe}. Dividend payout ratio = common dividends ÷ earnings available to common = {m(cd)} ÷ {m(eac)} = {pay}.""",
    )


def operating_cash(p):
    co, ar, ins, ca, px, it, wg, dv = (p[k] for k in ("co", "ar", "ins", "ca", "px", "int", "wages", "div"))
    key_v = ar - ins - it + dv
    gain = px - ca
    assert gain > 0 and key_v >= dv
    pool = {
        "no_int": (m(key_v + it), f"Leaves out the {m(it)} of interest paid. Under U.S. GAAP, interest paid is an operating cash outflow."),
        "wages": (m(key_v - wg), f"Deducts the {m(wg)} of accrued wages. An accrual records an expense without any cash payment."),
        "proceeds": (m(key_v + px), f"Adds the {m(px)} of equipment sale proceeds. Proceeds from selling equipment are an investing inflow."),
        "div_inv": (m(key_v - dv), f"Leaves out the {m(dv)} of dividends received. Under U.S. GAAP, dividends received are an operating cash inflow."),
        "gain": (m(key_v + gain), f"Adds the {m(gain)} gain on the equipment sale. A gain is not a cash flow, and the proceeds are an investing inflow."),
    }
    key = (m(key_v), f"Correct. +{m(ar)} − {m(ins)} − {m(it)} + {m(dv)}. The equipment sale is investing, and the accrued wages involve no cash.")
    choices, ans = pick(pool, key, p["use"])
    short = co.split()[0]
    return variant(
        f"""{co}'s controller is deriving how six Year 1 transactions affect net cash provided by operating activities: (1) collected {m(ar)} of accounts receivable from customers; (2) paid {m(ins)} in December for insurance covering the next year; (3) sold equipment with a carrying amount of {m(ca)} for {m(px)} in cash; (4) paid {m(it)} of interest on a bank loan; (5) accrued {m(wg)} of wages that will be paid in January; and (6) received {m(dv)} of dividends on an investment in equity securities. Under U.S. GAAP, by how much do these transactions increase net cash provided by operating activities?""",
        choices, ans,
        f"""Operating cash flows: collections from customers +{m(ar)}; insurance paid in advance −{m(ins)}; interest paid −{m(it)} (operating under U.S. GAAP); dividends received +{m(dv)} (operating under U.S. GAAP). Net +{m(key_v)}. The {m(px)} of equipment proceeds is an investing inflow (the {m(gain)} gain is removed under the indirect method), and the wage accrual has no cash effect.""",
    )


def discontinued_ops(p):
    co, op, ca, fv, t = (p[k] for k in ("co", "op", "ca", "fv", "t"))
    wd = ca - fv
    net = lambda x: whole(D(x) * (100 - t) / 100)
    key_v, draft = net(op + wd), net(op)
    pool = {
        "draft": (m(draft), f"Accepts the draft, which omits the {m(wd)} write-down to fair value less cost to sell."),
        "gross": (m(op + wd), "Reports the whole loss before tax. Discontinued operations are presented net of tax."),
        "wd_notax": (m(draft + wd), f"Adds the {m(wd)} write-down without its tax effect. The write-down is part of the discontinued component's pretax loss."),
        "op_pretax": (m(op + net(wd)), f"Nets tax against the {m(wd)} write-down but not against the {m(op)} operating loss. The component's whole pretax loss is reported net of tax."),
        "wd_only": (m(net(wd)), f"Reports only the write-down, net of tax, and leaves the {m(op)} operating loss in continuing operations. The component's operating results are part of discontinued operations."),
    }
    key = (m(key_v), f"Correct. ({m(op)} operating loss + {m(wd)} write-down) × (1 − {t}%).")
    choices, ans = pick(pool, key, p["use"])
    short = co.split()[0]
    return variant(
        f"""{co}'s draft Year 1 income statement reports a loss from discontinued operations, net of tax, of {m(draft)}. The discontinued component is a division that met the held-for-sale criteria in November. Supporting schedules show that the division had a pretax operating loss of {m(op)} for Year 1, and that when it was classified as held for sale its carrying amount was {m(ca)} and its fair value less cost to sell was {m(fv)}. {short}'s tax rate is {t}%. After any corrections needed, what is {short}'s loss from discontinued operations, net of tax?""",
        choices, ans,
        f"""The loss from discontinued operations includes the component's operating results for the period and any loss on measuring it at fair value less cost to sell: {m(op)} + ({m(ca)} − {m(fv)}) = {m(op + wd)} before tax. Net of the {t}% tax benefit, the loss is {m(key_v)}.""",
    )


def equity_corrections(p):
    co, cs, apic, re_, ts, nci = (p[k] for k in ("co", "cs", "apic", "re", "ts", "nci"))
    e = cs + apic + re_
    key_v = e - ts + nci
    short = co.split()[0]
    pool = {
        "ts_only": (m(e - ts), "Corrects the treasury stock but leaves the noncontrolling interest in liabilities. Noncontrolling interest is part of equity in consolidated statements."),
        "draft": (m(e), "Accepts the draft. Treasury stock is a deduction from equity, not an asset, and noncontrolling interest is equity, not a liability."),
        "nci_only": (m(e + nci), "Moves the noncontrolling interest into equity but leaves the treasury stock as an asset."),
        "nci_deduct": (m(e - ts - nci), f"Deducts the {m(nci)} noncontrolling interest from equity. It is added to equity, reported separately from the parent's equity."),
    }
    key = (m(key_v), f"Correct. {m(e)} − {m(ts)} treasury stock + {m(nci)} noncontrolling interest.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s draft consolidated balance sheet reports total stockholders' equity of {m(e)}: common stock {m(cs)}, additional paid-in capital {m(apic)}, and retained earnings {m(re_)}. Supporting documents show that {m(ts)} of {short}'s own shares, reacquired and held in treasury, are reported among noncurrent assets as "investment in treasury stock," and that the {m(nci)} noncontrolling interest in a subsidiary is reported as a noncurrent liability. After correcting the draft, what total equity should {short}'s consolidated balance sheet report?""",
        choices, ans,
        f"""Treasury stock is a contra-equity account, so the {m(ts)} comes out of assets and reduces equity. Noncontrolling interest is reported within equity, separately from the parent's equity, so the {m(nci)} moves from liabilities to equity. Total equity = {m(e)} − {m(ts)} + {m(nci)} = {m(key_v)} (the parent's share is {m(e - ts)}).""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def receivables_rollforward(p):
    co, b, e, c, r, w = (p[k] for k in ("co", "b", "e", "c", "r", "w"))
    key_v = e + c + w - b - r
    pool = {
        "add_w": (m(key_v - 2 * w), "Adds the write-offs instead of subtracting them. Write-offs reduce receivables, so more sales are needed to reach the ending balance."),
        "no_w": (m(key_v - w), f"Leaves out the {m(w)} of write-offs."),
        "rec": (m(key_v + r), f"Treats the {m(r)} recovery as a collection of current sales. A recovery is first reinstated in receivables and then collected, so it is not a sale."),
        "reversed": (m(b - e + c + w - r), "Reverses the change in receivables, subtracting the ending balance and adding the beginning balance."),
    }
    key = (m(key_v), f"Correct. {m(e)} + {m(c)} + {m(w)} − {m(b)} − {m(r)} reinstated recovery.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} is preparing a rollforward of its trade receivables to determine credit sales. Receivables were {m(b)} at the start of the year and {m(e)} at the end, per the aged subledger. Cash receipts from customers, per the cash receipts journal, were {m(c)}, which includes {m(r)} collected on an account written off in an earlier year. Write-offs during the year were {m(w)}. All sales are on credit. What should credit sales for the year be?""",
        choices, ans,
        f"""Rollforward: beginning {m(b)} + credit sales + {m(r)} recovery reinstated − {m(c)} collections − {m(w)} write-offs = ending {m(e)}. Credit sales = {m(e)} + {m(c)} + {m(w)} − {m(b)} − {m(r)} = {m(key_v)}.""",
    )


def inventory_rollforward(p):
    co, bi, pur, pr, fi, cogs, count = (p[k] for k in ("co", "bi", "pur", "pr", "fi", "cogs", "count"))
    book = bi + pur - pr + fi - cogs
    key_v = book - count
    short = co.split()[0]
    pool = {
        "no_fi": (m(key_v - fi), f"Leaves the {m(fi)} of freight-in out of the rollforward. Freight-in is part of inventory cost."),
        "no_pr": (m(key_v + pr), f"Leaves the {m(pr)} of purchase returns out of the rollforward. Returned goods leave inventory."),
        "add_pr": (m(key_v + 2 * pr), "Adds the purchase returns instead of subtracting them."),
        "sub_fi": (m(key_v - 2 * fi), "Subtracts the freight-in instead of adding it. Freight-in is part of inventory cost."),
    }
    assert all(D(v[0].replace("$", "").replace(",", "")) > 0 for k, v in pool.items() if k in p["use"])
    key = (m(key_v), f"Correct. Book inventory {m(bi)} + {m(pur)} − {m(pr)} + {m(fi)} − {m(cogs)} = {m(book)}, less the {m(count)} count.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} uses a perpetual inventory system. Its inventory rollforward for Year 1 shows beginning inventory of {m(bi)}, purchases of {m(pur)} per the accounts payable subledger, purchase returns of {m(pr)}, freight-in of {m(fi)}, and cost of goods sold of {m(cogs)} per the general ledger. A year-end physical count, priced at cost, totals {m(count)}. What inventory shrinkage should {short} record?""",
        choices, ans,
        f"""Book (perpetual) inventory = beginning {m(bi)} + purchases {m(pur)} − returns {m(pr)} + freight-in {m(fi)} − cost of goods sold {m(cogs)} = {m(book)}. The count shows {m(count)}, so {m(key_v)} of inventory is missing and is recorded as shrinkage (usually in cost of goods sold).""",
    )


def ppe_rollforward(p):
    co, g0, g1, pur, ad0, ad1, dep, px = (p[k] for k in ("co", "g0", "g1", "pur", "ad0", "ad1", "dep", "px"))
    cr = g0 + pur - g1
    adr = ad0 + dep - ad1
    ca = cr - adr
    res = px - ca
    gl = lambda x: f"{m(abs(x))} {'gain' if x > 0 else 'loss'}"
    short = co.split()[0]
    pool = {
        "ad_change": (gl(px - (cr - (ad1 - ad0))), f"Uses the {m(ad1 - ad0)} net change in accumulated depreciation as the amount removed. The amount removed is what the rollforward leaves unexplained: {m(ad0)} + {m(dep)} − {m(ad1)} = {m(adr)}."),
        "all_gain": (f"{m(px)} gain", f"Treats the whole {m(px)} of proceeds as gain, ignoring the equipment's carrying amount."),
        "cost": (gl(px - cr), "Compares the proceeds with the equipment's cost without removing its accumulated depreciation."),
        "dep_exp": (gl(px - (cr - dep)), f"Uses the year's {m(dep)} of depreciation expense as the accumulated depreciation removed. The amount removed is what the rollforward leaves unexplained."),
    }
    key = (gl(res), f"Correct. Cost removed {m(cr)} less accumulated depreciation removed {m(adr)} = carrying amount {m(ca)}; proceeds {m(px)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s equipment rollforward shows gross equipment of {m(g0)} at the start of the year and {m(g1)} at the end, with {m(pur)} of purchases per the capital expenditures report. Accumulated depreciation was {m(ad0)} at the start and {m(ad1)} at the end, and depreciation expense was {m(dep)}. The only disposal was one item sold for {m(px)} in cash. What gain or loss should {short} report on the sale?""",
        choices, ans,
        f"""Derive the disposal from the rollforward. Cost removed = {m(g0)} + {m(pur)} − {m(g1)} = {m(cr)}. Accumulated depreciation removed = {m(ad0)} + {m(dep)} − {m(ad1)} = {m(adr)}. Carrying amount = {m(ca)}; proceeds {m(px)}; {'gain' if res > 0 else 'loss'} = {m(abs(res))}.""",
    )


def exit_costs(p):
    co, start, mt, m1, emp, pay, nd, nm = (p[k] for k in ("co", "start", "mt", "m1", "emp", "pay", "nd", "nm"))
    total = emp * pay
    key_v = whole(D(total) * m1 / mt)
    short = co.split()[0]
    falls = "one month falls" if m1 == 1 else f"{WORDS[m1]} months fall"
    pool = {
        "zero": ("$0", "Waits until the plant closes. When employees must work to a future date to earn the benefit, the cost is recognized over that service period, starting when the plan is communicated."),
        "notice": (m(min(total, whole(D(total) / nm * m1))), f"Spreads the benefit over the {nd}-day minimum notice period. Because employees must stay beyond that period to earn it, it is spread over the full period to March 31."),
        "full": (m(total), "Recognizes the whole benefit when the plan is communicated. That applies only when employees are not required to render service beyond the minimum retention period."),
        "y2": (m(total - key_v), f"Recognizes the portion for the {WORDS[mt - m1]} months after year-end. Year 1 recognizes only the service from {start} to December 31."),
    }
    key = (m(key_v), f"Correct. The {m(total)} benefit is recognized ratably from {start} to March 31 ({mt} months); {falls} in Year 1.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On {start}, Year 1, {co} commits to closing a plant on March 31, Year 2, and communicates the plan to the plant's {emp} employees that day. Each employee who stays until the plant closes will receive a {m(pay)} termination payment; employees who leave earlier receive nothing. Under {short}'s plan and local law, employees must be given at least {nd} days' notice before termination. {short} expects all {emp} to stay. Treat each month as equal in length. What termination benefit expense should {short} recognize in Year 1?""",
        choices, ans,
        f"""One-time termination benefits are recognized when the plan is communicated if employees need not work beyond the minimum retention period. Here they must stay until March 31, beyond the {nd}-day minimum, so the {m(total)} ({emp} × {m(pay)}) is recognized ratably over the {WORDS[mt]} months from {start} to March 31: {m(key_v)} in Year 1.""",
    )


def group_impairment(p):
    co, a, b, bl, und, fvg, fvb = (p[k] for k in ("co", "a", "b", "bldg", "undisc", "fv_group", "fv_bldg"))
    total = a + b + bl
    loss = total - fvg
    assert und < total
    share = lambda x: whole(D(loss) * x / total)
    sa, sb, sbl = share(a), share(b), share(bl)
    cap = bl - fvb
    assert cap < sbl
    excess = sbl - cap
    ra = whole(D(excess) * a / (a + b))
    key_v = sa + ra
    g = gcd(a, b)
    pa = pct(D(a) / (a + b))
    short = co.split()[0]
    pool = {
        "share_only": (m(ra), f"Allocates to Machine A only its share of the {m(excess)} that could not be charged to the building."),
        "prorata": (m(sa), f"Allocates the {m(loss)} loss pro rata to all three assets without limiting the building to its {m(cap)} excess over fair value."),
        "machines": (m(whole(D(loss) * a / (a + b))), f"Allocates the whole {m(loss)} loss to the two machines ({pa} to Machine A). The building takes its share, limited to its {m(cap)} excess over fair value."),
        "even": (m(sa + whole(D(excess) / 2)), f"Splits the {m(excess)} the building cannot absorb equally between the machines. It is reallocated by relative carrying amount."),
    }
    key = (m(key_v), f"Correct. Pro rata {m(sa)}, plus {pa} of the {m(excess)} the building cannot absorb (its loss is capped at {m(cap)}).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} tests an asset group for impairment. The group consists of Machine A (carrying amount {m(a)}), Machine B ({m(b)}) and a building ({m(bl)}). The group's undiscounted future cash flows are {m(und)} and its fair value is {m(fvg)}. The building's own fair value is {m(fvb)}; the machines' individual fair values cannot be determined without undue cost. How much of the impairment loss should {short} allocate to Machine A?""",
        choices, ans,
        f"""The group is not recoverable ({m(und)} < {m(total)}), so the loss is {m(total)} − {m(fvg)} = {m(loss)}, allocated pro rata by carrying amount but not reducing any asset below its determinable fair value. Pro rata: A {m(sa)}, B {m(sb)}, building {m(sbl)}. The building can absorb only {m(bl)} − {m(fvb)} = {m(cap)}, so the other {m(excess)} is reallocated to the machines in a {a // g}:{b // g} ratio: A {m(ra)}, B {m(excess - ra)}. Machine A's total = {m(key_v)}.""",
    )


def interest_capitalization(p):
    co, e1, e2, e3, ls, rs, do, ro = (p[k] for k in ("co", "e1", "e2", "e3", "ls", "rs", "do", "ro"))
    waae = e1 + e2 // 2
    assert waae > ls
    i = lambda amt, r: whole(D(amt) * r / 100)
    key_v = i(ls, rs) + i(waae - ls, ro)
    actual = i(ls, rs) + i(do, ro)
    assert key_v < actual
    pool = {
        "specific": (m(i(ls, rs)), "Capitalizes only the interest on the specific construction loan. Expenditures above the specific borrowing use the rate on other debt."),
        "all_rs": (m(i(waae, rs)), f"Applies the {rs}% construction-loan rate to all {m(waae)} of weighted-average expenditures."),
        "all_ro": (m(i(waae, ro)), f"Applies the {ro}% rate on other debt to all {m(waae)} of weighted-average expenditures."),
        "total_exp": (m(i(ls, rs) + i(e1 + e2 + e3 - ls, ro)), f"Uses total expenditures ({m(e1 + e2 + e3)}) instead of the weighted average."),
        "incurred": (m(actual), "Capitalizes all interest incurred during construction. Only avoidable interest on weighted-average accumulated expenditures is capitalized, up to the interest incurred."),
    }
    key = (m(key_v), f"Correct. Weighted-average accumulated expenditures {m(waae)}: {m(ls)} × {rs}% + {m(waae - ls)} × {ro}%.")
    choices, ans = pick(pool, key, p["use"])
    short = co.split()[0]
    return variant(
        f"""{co} constructs a building for its own use during Year 1. It spends {m(e1)} on January 1, {m(e2)} on July 1, and {m(e3)} on December 31, and the building is completed on December 31. {short} borrowed {m(ls)} at {rs}% on January 1 specifically for the project and also has {m(do)} of other debt outstanding all year at {ro}%. What amount of interest should {short} capitalize for Year 1?""",
        choices, ans,
        f"""Weighted-average accumulated expenditures = {m(e1)} × 12/12 + {m(e2)} × 6/12 + {m(e3)} × 0/12 = {m(waae)}. Avoidable interest: the first {m(ls)} at the specific borrowing's {rs}% ({m(i(ls, rs))}) and the remaining {m(waae - ls)} at the {ro}% rate on other borrowings ({m(i(waae - ls, ro))}), for {m(key_v)}. That is less than the {m(actual)} of actual interest incurred, so {m(key_v)} is capitalized.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def nfp_agent(p):
    org, ben, d, g, v, r = (p[k] for k in ("org", "ben", "d", "g", "v", "r"))
    key_v = g + v
    short, bshort = org.split()[0], ben.split()[0]
    pool = {
        "plus_r": (m(key_v + r), f"Also counts {ben}'s {m(r)}. A transfer the beneficiary makes for its own benefit is not a contribution to {short}."),
        "plus_d": (m(key_v + d), f"Also counts the {m(d)} designated for {bshort} without variance power. {short} acts as an agent for it and records a liability."),
        "all": (m(d + g + v + r), "Counts every receipt as a contribution."),
        "no_v": (m(g), f"Leaves out the {m(v)} over which {short} has explicit variance power. That gift is {short}'s contribution, not an agency transfer."),
    }
    key = (m(key_v), f"Correct. The {m(g)} for general use and the {m(v)} over which {short} has variance power.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""During the year, {org}, a not-for-profit federated fundraising organization, receives: {m(d)} from donors who specify that it go to {ben}, an unrelated charity, with no power for {short} to redirect it; {m(g)} for {short}'s general use; {m(v)} from a donor who names a beneficiary but explicitly gives {short} the unilateral power to redirect the gift to another beneficiary; and {m(r)} transferred by {ben} itself for {short} to invest and hold for {bshort}'s future use. What contribution revenue should {short} recognize?""",
        choices, ans,
        f"""A recipient that receives assets for a specified beneficiary without variance power acts as an agent: it records a liability, not revenue ({m(d)}). Explicit variance power makes the gift {short}'s contribution ({m(v)}). The {m(g)} for general use is a contribution. {bshort}'s own {m(r)} is held for its benefit and is not a contribution to {short}. Contribution revenue = {m(key_v)}.""",
    )


def licenses(p):
    co, sw, sup, sy, br, by = (p[k] for k in ("co", "sw", "sup", "sup_years", "brand", "brand_years"))
    sm, bm = sy * 12, by * 12
    sup_mo, br_mo = D(sup) / sm, D(br) / bm
    key_v = rd(sw + sup_mo + br_mo)
    short = co.split()[0]
    pool = {
        "sup_up": (m(rd(sw + sup + br_mo)), f"Recognizes the {WORDS[sy]} years of support at the start. Support is a service provided over the {WORDS[sy]} years."),
        "fr_up": (m(rd(sw + sup_mo + br)), "Recognizes the whole franchise fee at the start. A brand license supported by ongoing activities gives a right to access, recognized over the license term."),
        "all": (m(sw + sup + br), "Recognizes everything on December 1."),
        "sw_ratable": (m(rd(D(sw) / sm + sup_mo + br_mo)), f"Spreads the software license over the {WORDS[sy]}-year support period. A license to functional intellectual property is a right to use, recognized when control transfers."),
    }
    key = (m(key_v), f"Correct. {m(sw)} for the software license at transfer, plus {m(sup)} ÷ {sm} = {m(rd(sup_mo))} of support and {m(br)} ÷ {bm} = {m(rd(br_mo))} of the brand license.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On December 1, Year 1, {co} sells a customer a perpetual license to its existing accounting software for {m(sw)}, together with {WORDS[sy]} years of technical support for {m(sup)}; the prices equal standalone selling prices, and {short} does not expect updates to change the software's functionality. Also on December 1, {short} grants a franchisee {'an' if WORDS[by][0] in 'aeiou' else 'a'} {WORDS[by]}-year license to use its restaurant brand, which {short} will continue to support with advertising and brand development, for an upfront fee of {m(br)}. What revenue should {short} recognize for December, Year 1?""",
        choices, ans,
        f"""The software is functional intellectual property whose utility does not depend on {short}'s ongoing activities, so the license is a right to use recognized when control transfers: {m(sw)}. Support is recognized over {sm} months: {m(rd(sup_mo))} for December. The brand license is symbolic intellectual property, a right to access recognized over the {WORDS[by]}-year term: {m(br)} ÷ {bm} = {m(rd(br_mo))}. December revenue = {m(key_v)}.""",
    )


# Parameter set 0 reproduces the reviewed item (its `use` is the reviewed distractors); sets 1-3 are variants.
FAMILIES = {
    "far-performance-metrics-0001": (pe_payout, [
        dict(co="Oates Corp.", ni=2400000, pd=400000, cd=600000, s=1000000, price=30, use=["both", "pe_nopref", "pay_total"]),
        dict(co="Pardee Corp.", ni=3000000, pd=500000, cd=1000000, s=1250000, price=36, use=["pe_nopref", "pay_total", "pay_all"]),
        dict(co="Quarles Corp.", ni=1800000, pd=200000, cd=400000, s=800000, price=24, use=["both", "pe_nopref", "pay_total"]),
        dict(co="Rudd Corp.", ni=5000000, pd=1000000, cd=1600000, s=1600000, price=50, use=["both", "pay_total", "pay_all"]),
    ]),
    "far-cash-flows-0006": (operating_cash, [
        dict(co="Ives Co.", ar=50000, ins=30000, ca=40000, px=55000, int=20000, wages=12000, div=15000, use=["no_int", "wages", "proceeds"]),
        dict(co="Jarvis Co.", ar=80000, ins=24000, ca=60000, px=72000, int=18000, wages=9000, div=10000, use=["wages", "no_int", "proceeds"]),
        dict(co="Keating Co.", ar=65000, ins=12000, ca=30000, px=41000, int=25000, wages=16000, div=8000, use=["div_inv", "wages", "gain"]),
        dict(co="Lang Co.", ar=120000, ins=45000, ca=70000, px=95000, int=30000, wages=20000, div=25000, use=["no_int", "gain", "proceeds"]),
    ]),
    "far-income-statement-0003": (discontinued_ops, [
        dict(co="Quinn Co.", op=150000, ca=800000, fv=740000, t=25, use=["draft", "gross", "wd_notax"]),
        dict(co="Rennie Co.", op=240000, ca=1200000, fv=1080000, t=21, use=["gross", "wd_notax", "op_pretax"]),
        dict(co="Sloane Co.", op=90000, ca=500000, fv=470000, t=25, use=["wd_only", "draft", "gross"]),
        dict(co="Tate Co.", op=180000, ca=950000, fv=850000, t=30, use=["draft", "wd_notax", "op_pretax"]),
    ]),
    "far-balance-sheet-0003": (equity_corrections, [
        dict(co="Reyes Corp.", cs=100000, apic=400000, re=600000, ts=50000, nci=80000, use=["ts_only", "draft", "nci_only"]),
        dict(co="Sykes Corp.", cs=200000, apic=900000, re=1400000, ts=150000, nci=60000, use=["ts_only", "draft", "nci_only"]),
        dict(co="Thorne Corp.", cs=50000, apic=250000, re=450000, ts=40000, nci=120000, use=["nci_deduct", "ts_only", "draft"]),
        dict(co="Vance Corp.", cs=150000, apic=600000, re=950000, ts=90000, nci=200000, use=["nci_deduct", "draft", "nci_only"]),
    ]),
    "far-receivables-rollforward-0001": (receivables_rollforward, [
        dict(co="Selby Co.", b=200000, e=260000, c=1180000, r=5000, w=18000, use=["add_w", "no_w", "rec"]),
        dict(co="Tanner Co.", b=340000, e=310000, c=2050000, r=8000, w=26000, use=["add_w", "rec", "reversed"]),
        dict(co="Ulrich Co.", b=150000, e=190000, c=870000, r=3000, w=12000, use=["reversed", "add_w", "no_w"]),
        dict(co="Varney Co.", b=480000, e=450000, c=3100000, r=12000, w=40000, use=["add_w", "no_w", "rec"]),
    ]),
    "far-inventory-rollforward-0001": (inventory_rollforward, [
        dict(co="Tobin Co.", bi=120000, pur=900000, pr=20000, fi=15000, cogs=870000, count=125000, use=["no_fi", "no_pr", "add_pr"]),
        dict(co="Voss Co.", bi=210000, pur=1400000, pr=35000, fi=12000, cogs=1380000, count=181000, use=["no_fi", "sub_fi", "no_pr"]),
        dict(co="Wolcott Co.", bi=90000, pur=640000, pr=15000, fi=6000, cogs=610000, count=96000, use=["sub_fi", "no_pr", "add_pr"]),
        dict(co="Yardley Co.", bi=150000, pur=1100000, pr=28000, fi=10000, cogs=1060000, count=150000, use=["no_fi", "sub_fi", "no_pr"]),
    ]),
    "far-ppe-rollforward-0001": (ppe_rollforward, [
        dict(co="Ulm Co.", g0=1200000, g1=1350000, pur=300000, ad0=400000, ad1=430000, dep=110000, px=50000, use=["ad_change", "all_gain", "cost"]),
        dict(co="Vesey Co.", g0=2000000, g1=2150000, pur=400000, ad0=700000, ad1=760000, dep=190000, px=150000, use=["ad_change", "dep_exp", "cost"]),
        dict(co="Whitby Co.", g0=1600000, g1=1650000, pur=350000, ad0=500000, ad1=560000, dep=150000, px=80000, use=["all_gain", "dep_exp", "cost"]),
        dict(co="Xavier Co.", g0=1500000, g1=1600000, pur=280000, ad0=400000, ad1=440000, dep=100000, px=50000, use=["dep_exp", "ad_change", "cost"]),
    ]),
    "far-exit-costs-0001": (exit_costs, [
        dict(co="Vail Co.", start="December 1", mt=4, m1=1, emp=50, pay=6000, nd=60, nm=2, use=["zero", "notice", "full"]),
        dict(co="Wade Co.", start="November 1", mt=5, m1=2, emp=40, pay=9000, nd=90, nm=3, use=["notice", "y2", "full"]),
        dict(co="Yale Co.", start="September 1", mt=7, m1=4, emp=35, pay=8000, nd=60, nm=2, use=["zero", "y2", "full"]),
        dict(co="Zeller Co.", start="December 1", mt=4, m1=1, emp=60, pay=4000, nd=60, nm=2, use=["notice", "y2", "full"]),
    ]),
    "far-ppe-impairment-0002": (group_impairment, [
        dict(co="Yates Co.", a=300000, b=200000, bldg=500000, undisc=900000, fv_group=800000, fv_bldg=460000, use=["share_only", "prorata", "machines"]),
        dict(co="Zane Co.", a=200000, b=400000, bldg=400000, undisc=850000, fv_group=760000, fv_bldg=340000, use=["share_only", "machines", "even"]),
        dict(co="Abel Co.", a=450000, b=150000, bldg=400000, undisc=920000, fv_group=820000, fv_bldg=360000, use=["share_only", "prorata", "even"]),
        dict(co="Benson Co.", a=400000, b=200000, bldg=600000, undisc=1100000, fv_group=900000, fv_bldg=510000, use=["prorata", "even", "machines"]),
    ]),
    "far-ppe-interest-capitalization-0001": (interest_capitalization, [
        dict(co="Garvey Co.", e1=400000, e2=600000, e3=200000, ls=500000, rs=8, do=1000000, ro=10, use=["specific", "all_rs", "all_ro"]),
        dict(co="Hadley Co.", e1=600000, e2=800000, e3=300000, ls=700000, rs=6, do=2000000, ro=9, use=["all_ro", "total_exp", "incurred"]),
        dict(co="Keller Co.", e1=300000, e2=1000000, e3=400000, ls=400000, rs=7, do=1500000, ro=9, use=["specific", "total_exp", "incurred"]),
        dict(co="Lyle Co.", e1=500000, e2=400000, e3=250000, ls=600000, rs=5, do=800000, ro=8, use=["specific", "all_rs", "all_ro"]),
    ]),
    "far-nfp-agent-transfers-0001": (nfp_agent, [
        dict(org="Unity Fund", ben="Riverside Shelter", d=40000, g=30000, v=20000, r=10000, use=["plus_r", "plus_d", "all"]),
        dict(org="Civic Fund", ben="Harbor House", d=65000, g=45000, v=25000, r=15000, use=["no_v", "plus_r", "all"]),
        dict(org="Metro Fund", ben="Lakeside Pantry", d=30000, g=55000, v=35000, r=20000, use=["plus_r", "plus_d", "all"]),
        dict(org="Valley Fund", ben="Hillcrest Clinic", d=80000, g=25000, v=40000, r=12000, use=["no_v", "plus_d", "all"]),
    ]),
    "far-revenue-licenses-0001": (licenses, [
        dict(co="Egan Co.", sw=300000, sup=60000, sup_years=2, brand=500000, brand_years=5, use=["sup_up", "fr_up", "all"]),
        dict(co="Fitch Co.", sw=240000, sup=36000, sup_years=3, brand=720000, brand_years=10, use=["sw_ratable", "sup_up", "fr_up"]),
        dict(co="Gilroy Co.", sw=450000, sup=48000, sup_years=2, brand=300000, brand_years=5, use=["sup_up", "fr_up", "all"]),
        dict(co="Hollis Co.", sw=180000, sup=72000, sup_years=3, brand=480000, brand_years=8, use=["sw_ratable", "fr_up", "all"]),
    ]),
}


def same_as_reviewed(item, v):
    problems = [k for k in ("stem", "explanation") if v[k] != item[k]]
    pairs = lambda x: {(c["text"], c["rationale"]) for c in x["choices"]}
    if pairs(v) != pairs(item):
        problems.append("choices")
    key = lambda x: next(c["text"] for c in x["choices"] if c["id"] == x["answer"])
    if key(v) != key(item):
        problems.append("answer")
    return problems


def main():
    items, failed = [], False
    for item_id, (build, params) in FAMILIES.items():
        path = os.path.join(CONTENT, item_id + ".yaml")
        with open(path, encoding="utf-8") as f:
            item = yaml.safe_load(f)
        item.pop("variants", None)
        problems = same_as_reviewed(item, build(params[0]))
        if problems:
            print(f"FAIL {item_id}: parameter set 0 does not rebuild the reviewed item ({', '.join(problems)})",
                  file=sys.stderr)
            failed = True
            continue
        attach_variants(item, [build(p) for p in params[1:]])
        letters = [item["answer"]] + [v["answer"] for v in item["variants"]]
        print(f"{item_id}: key letters {' '.join(letters)}")
        if len(set(letters)) < 2:
            print(f"FAIL {item_id}: the key has the same letter in every version", file=sys.stderr)
            failed = True
        items.append((path, item))
    if failed:
        sys.exit(1)
    warnings = audit([it for _, it in items])
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    for path, item in items:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(item, f, sort_keys=False, allow_unicode=True, width=100)
    print(f"added {sum(len(it['variants']) for _, it in items)} variants to {len(items)} items")


if __name__ == "__main__":
    main()
