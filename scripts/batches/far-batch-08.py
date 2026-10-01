"""FAR batch 08 — 14 items written from scratch for blueprint tasks with fewer than two items
(scripts/far-coverage.py): deferred taxes and the tax provision entry, lessee initial measurement, subsequent
events (adjustment amounts and derived impacts), the income statement, the statement of cash flows, correcting
consolidated statements, and investments at fair value. Target skill mix 0 / 11 / 3. Scope and skill tags follow
the AICPA CPA Exam Blueprints effective January 2026.

Every item is numeric and ships with three variants (method as in far-batch-06.py): each item is a builder,
parameter set 0 is the item and sets 1-3 are its variants, and every family must move the key's letter.

Run: python3 scripts/batches/far-batch-08.py   See docs/reviews/far-batch-08.md.
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import os
import sys
from decimal import Decimal as D

from common import AN, AP, attach_variants, audit, finalize, fix_articles, variant, write_items
from variants import m, pick, rd

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 08. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def family(id, area, topic, skill, refs, build, params):
    """An item built from parameter set 0, with sets 1-3 kept for its variants."""
    base = build(params[0])
    it = dict(id=id, type="mcq", blueprint=dict(section="FAR", area=area, topic=topic, skill=skill),
              review=dict(status="reviewed", references=refs, notes=NOTE), **base)
    it["stem"], it["explanation"] = fix_articles(it["stem"]), fix_articles(it["explanation"])
    for c in it["choices"]:
        c["text"], c["rationale"] = fix_articles(c["text"]), fix_articles(c["rationale"])
    it["_variants"] = [build(p) for p in params[1:]]
    return it


def short(name):
    return name.split()[0]


def pc(x):
    """A whole-number percent from a Decimal or int: 24 -> '24%'."""
    return f"{D(x):f}%"


def tax(x, rate):
    """x at rate% (Decimal), rounded half up to whole dollars."""
    return rd(D(x) * D(rate) / 100)


# ── Area I ───────────────────────────────────────────────────────────────


def income_continuing(p):
    co, s = p["co"], short(p["co"])
    net_sales = p["sales"] - p["ret"]
    key_v = net_sales - p["cogs"] - p["sell"] - p["ga"] + p["intrev"] - p["intexp"] + p["gain"] + p["eqg"]
    pool = {
        "disc": (m(key_v - p["disc"]), f"Subtracts the {m(p['disc'])} loss of the furniture division. The division was a separate segment, and selling it took {s} out of the furniture business, a strategic shift, so its results are reported in discontinued operations, below income from continuing operations."),
        "afs": (m(key_v + p["afs"]), f"Adds the {m(p['afs'])} unrealized holding gain on available-for-sale debt securities, which is reported in other comprehensive income, not in net income."),
        "no_equity": (m(key_v - p["eqg"]), f"Leaves out the {m(p['eqg'])} unrealized gain on the equity securities. Changes in the fair value of equity securities with readily determinable fair values are reported in net income."),
        "div": (m(key_v - p["div"]), f"Subtracts the {m(p['div'])} of dividends declared. Dividends are distributions of equity, reported in the statement of changes in equity, not expenses."),
        "gross": (m(key_v + p["ret"]), f"Starts from gross sales. The {m(p['ret'])} of sales returns and allowances is deducted to arrive at net sales."),
    }
    key = (m(key_v), f"Correct. Net sales {m(net_sales)} − {m(p['cogs'])} − {m(p['sell'])} − {m(p['ga'])} + {m(p['intrev'])} − {m(p['intexp'])} + {m(p['gain'])} + {m(p['eqg'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s adjusted trial balance for Year 1 includes the following pretax amounts: sales {m(p['sales'])}; sales returns and allowances {m(p['ret'])}; cost of goods sold {m(p['cogs'])}; selling expenses {m(p['sell'])}; general and administrative expenses {m(p['ga'])}; interest revenue {m(p['intrev'])}; interest expense {m(p['intexp'])}; gain on sale of equipment {m(p['gain'])}; unrealized gain on equity securities with readily determinable fair values {m(p['eqg'])}; unrealized holding gain on available-for-sale debt securities {m(p['afs'])}; operating loss of the furniture division {m(p['disc'])}; and dividends declared {m(p['div'])}. The furniture division was one of {s}'s three business segments; {s} sold it in November, Year 1, and no longer makes furniture. What amount should {s} report as income from continuing operations before income taxes in its Year 1 multi-step income statement?""",
        choices, ans,
        f"""Net sales = {m(p['sales'])} − {m(p['ret'])} = {m(net_sales)}. Subtract cost of goods sold ({m(p['cogs'])}), selling expenses ({m(p['sell'])}) and general and administrative expenses ({m(p['ga'])}) for operating income of {m(net_sales - p['cogs'] - p['sell'] - p['ga'])}. Other income and expense: + {m(p['intrev'])} interest revenue − {m(p['intexp'])} interest expense + {m(p['gain'])} gain on the equipment + {m(p['eqg'])} unrealized gain on equity securities, whose fair value changes go to net income. Income from continuing operations before income taxes = {m(key_v)}. The unrealized gain on available-for-sale debt securities is other comprehensive income; the division's loss is reported in discontinued operations because its sale was a strategic shift out of a whole segment; dividends declared are not expenses.""",
    )


def interest_paid(p):
    co, s = p["co"], short(p["co"])
    dip = p["ip1"] - p["ip0"]
    key_v = p["ie"] - p["amort"] - dip
    word = "increase" if dip > 0 else "decrease"
    pool = {
        "gross": (m(key_v + p["cap"]), f"Reports all interest paid, {m(key_v + p['cap'])}, including the {m(p['cap'])} capitalized. The disclosure is interest paid net of amounts capitalized; capitalized interest paid is part of the payments for the warehouse."),
        "add_amort": (m(p["ie"] + p["amort"] - dip), f"Adds the {m(p['amort'])} of discount amortization. Amortization is interest expense that is not paid in cash, so it is subtracted."),
        "no_payable": (m(p["ie"] - p["amort"]), f"Ignores the {m(abs(dip))} {word} in interest payable. Interest paid is expense adjusted for the change in the payable."),
        "payable_sign": (m(p["ie"] - p["amort"] + dip), f"Adjusts for the change in interest payable in the wrong direction. An {word} in the payable means {s} paid {'less' if dip > 0 else 'more'} than it incurred."),
        "cap_twice": (m(key_v - p["cap"]), f"Subtracts the {m(p['cap'])} of capitalized interest from interest expense. Interest expense already excludes the capitalized interest, so this removes it twice."),
    }
    key = (m(key_v), f"Correct. {m(p['ie'])} expense − {m(p['amort'])} amortization {'−' if dip > 0 else '+'} {m(abs(dip))} {word} in interest payable.")
    choices, ans = pick(pool, key, p["use"])
    total = p["ie"] + p["cap"]
    return variant(
        f"""{co}'s Year 1 income statement reports interest expense of {m(p['ie'])}, which includes {m(p['amort'])} of amortization of the discount on its bonds payable. During Year 1, {s} also capitalized {m(p['cap'])} of interest as part of the cost of a warehouse it built for its own use. Interest payable was {m(p['ip0'])} at January 1 and {m(p['ip1'])} at December 31. In the supplemental disclosures to its Year 1 statement of cash flows, what amount should {s} report as interest paid, net of amounts capitalized?""",
        choices, ans,
        f"""Interest incurred = {m(p['ie'])} expensed + {m(p['cap'])} capitalized = {m(total)}. Cash paid for interest = {m(total)} − {m(p['amort'])} discount amortization (not paid in cash) {'−' if dip > 0 else '+'} {m(abs(dip))} {word} in interest payable = {m(total - p['amort'] - dip)}. Net of the {m(p['cap'])} capitalized, which is reported with the payments for the warehouse, the disclosure is {m(key_v)}.""",
    )


def cf_investing(p):
    co, s = p["co"], short(p["co"])
    key_v = p["mach_cash"] - p["sale_px"] - p["ins"]
    assert key_v > 0
    note = p["mach_cost"] - p["mach_cash"]
    pool = {
        "gain": (m(key_v + p["sale_cv"]), f"Counts only the {m(p['sale_px'] - p['sale_cv'])} gain on the equipment as an investing inflow. The whole {m(p['sale_px'])} of proceeds is the investing inflow; the gain is subtracted in the operating section under the indirect method."),
        "full_cost": (m(key_v + note), f"Reports the full {m(p['mach_cost'])} cost of the machinery as an outflow. The {m(note)} financed by the seller's note is a noncash investing and financing activity, disclosed rather than reported as a cash flow."),
        "tbills": (m(key_v + p["tbill"]), f"Treats the {m(p['tbill'])} of 90-day Treasury bills as an investing outflow. Under {s}'s policy they are cash equivalents, so buying them doesn't change cash and cash equivalents."),
        "ins_op": (m(key_v + p["ins"]), f"Classifies the {m(p['ins'])} of insurance proceeds as operating. Proceeds from insurance claims are classified by the nature of the loss, and a destroyed building is an investing item."),
        "land": (m(key_v + p["land"]), f"Reports the {m(p['land'])} of land acquired for shares as an investing outflow. It is a noncash investing and financing activity."),
        "note_prin": (m(key_v + p["note_prin"]), f"Includes the {m(p['note_prin'])} of principal paid on the machinery note, which is a financing outflow."),
        "interest": (m(key_v - p["interest"]), f"Counts the {m(p['interest'])} of interest received as an investing inflow. Interest received is an operating cash flow."),
    }
    key = (m(key_v), f"Correct. {m(p['mach_cash'])} paid for machinery − {m(p['sale_px'])} sale proceeds − {m(p['ins'])} insurance proceeds.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""During Year 1, {co} sold equipment with a carrying amount of {m(p['sale_cv'])} for {m(p['sale_px'])} in cash; bought machinery costing {m(p['mach_cost'])}, paying {m(p['mach_cash'])} in cash and signing a note payable to the seller for the rest; received {m(p['ins'])} from its insurer for a warehouse destroyed by fire; bought 90-day Treasury bills for {m(p['tbill'])}; acquired land with a fair value of {m(p['land'])} by issuing common shares; received {m(p['interest'])} of interest on a note receivable; and paid {m(p['note_prin'])} of principal on the machinery note. {s} treats investments with original maturities of three months or less as cash equivalents. What net cash used in investing activities results from these transactions in {s}'s Year 1 statement of cash flows?""",
        choices, ans,
        f"""Investing outflow: {m(p['mach_cash'])} of cash paid for the machinery; the {m(note)} financed by the seller is disclosed as a noncash activity. Investing inflows: {m(p['sale_px'])} of proceeds from the equipment sale and {m(p['ins'])} of insurance proceeds for the destroyed warehouse, which are classified by the nature of the loss. Net cash used = {m(p['mach_cash'])} − {m(p['sale_px'])} − {m(p['ins'])} = {m(key_v)}. The Treasury bills are cash equivalents, the land-for-shares exchange is noncash, interest received is operating, and principal paid on the note is financing.""",
    )



def consolidated_correction(p):
    P, S = p["parent"], p["sub"]
    ps, ss = short(P), short(S)
    own = D(p["pct"]) / 100
    div_inc = rd(p["divs"] * own)
    draft_nci = rd(p["sub_ni"] * (1 - own))
    draft_p = p["parent_own"] + div_inc + p["sub_ni"] - draft_nci
    share = lambda x: rd(D(x) * own)
    key_v = draft_p - div_inc - share(p["amort"] + p["up"])
    pool = {
        "full": (m(draft_p - div_inc - p["amort"] - p["up"]), f"Charges all of the {m(p['amort'])} amortization and {m(p['up'])} unrealized profit to {ps}. Both relate to {ss}, so {100 - p['pct']}% is attributed to the noncontrolling interest."),
        "fee": (m(key_v - p["fee"]), f"Also subtracts the {m(p['fee'])} management fee. Eliminating it removes equal amounts of revenue and expense, so consolidated net income doesn't change."),
        "keep_div": (m(draft_p - share(p["amort"] + p["up"])), f"Leaves the {m(div_inc)} of dividend income in. Dividends from a consolidated subsidiary are intercompany and are eliminated."),
        "no_amort": (m(draft_p - div_inc - share(p["up"])), f"Doesn't record the {m(p['amort'])} of amortization, whose {p['pct']}% share ({m(share(p['amort']))}) reduces income attributable to {ps}."),
        "no_upstream": (m(draft_p - div_inc - share(p["amort"])), f"Doesn't eliminate the {m(p['up'])} of unrealized profit, whose {p['pct']}% share ({m(share(p['up']))}) reduces income attributable to {ps}."),
    }
    key = (m(key_v), f"Correct. {m(draft_p)} − {m(div_inc)} dividend income − {p['pct']}% × ({m(p['amort'])} + {m(p['up'])}).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{P} has owned {p['pct']}% of {S} since acquiring it at the beginning of Year 1. For Year 2, {ss} reports net income of {m(p['sub_ni'])} and pays dividends of {m(p['divs'])}. {ps}'s draft Year 2 consolidated income statement reports net income attributable to {ps} of {m(draft_p)} and net income attributable to the noncontrolling interest of {m(draft_nci)}. The controller has identified these errors in the draft: (1) {ps}'s {m(div_inc)} of dividend income from {ss} was included in consolidated net income; (2) the Year 2 amortization of {m(p['amort'])} on the excess of the acquisition-date fair value of {ss}'s equipment over its book value was not recorded; (3) unrealized profit of {m(p['up'])} in {ps}'s ending inventory, on goods bought from {ss}, was not eliminated; and (4) management fees of {m(p['fee'])} that {ss} paid {ps} were not eliminated. {ps} attributes the elimination of profit on {ss}'s sales to {ps} proportionately between the parent and the noncontrolling interest. After correcting the errors, what net income attributable to {ps} should the consolidated income statement report?""",
        choices, ans,
        f"""(1) The {m(div_inc)} of dividend income is intercompany: eliminate it, all from {ps}'s income. (2) and (3) The amortization and the unrealized profit on {ss}'s upstream sales both reduce {ss}'s income as consolidated, {m(p['amort'])} + {m(p['up'])} = {m(p['amort'] + p['up'])}, shared {p['pct']}% / {100 - p['pct']}%, so {ps}'s share is {m(share(p['amort'] + p['up']))}. (4) Eliminating the management fee removes equal revenue and expense and doesn't change net income. Net income attributable to {ps} = {m(draft_p)} − {m(div_inc)} − {m(share(p['amort'] + p['up']))} = {m(key_v)}. The noncontrolling interest's share becomes {m(draft_nci)} − {m(p['amort'] + p['up'] - share(p['amort'] + p['up']))} = {m(draft_nci - (p['amort'] + p['up'] - share(p['amort'] + p['up'])))}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def fv_carrying(p):
    co, s = p["co"], short(p["co"])
    key_v = p["tr_fv"] + p["afs_fv"] + p["htm_ac"] + p["eq_fv"]
    pool = {
        "htm_fv": (m(key_v - p["htm_ac"] + p["htm_fv"]), f"Reports the bonds {s} will hold to maturity at their {m(p['htm_fv'])} fair value. Held-to-maturity debt securities are carried at amortized cost."),
        "afs_cost": (m(key_v - p["afs_fv"] + p["afs_ac"]), f"Reports the debt securities {s} may sell at their {m(p['afs_ac'])} amortized cost. Available-for-sale debt securities are carried at fair value, with unrealized gains and losses in other comprehensive income."),
        "eq_cost": (m(key_v - p["eq_fv"] + p["eq_cost"]), f"Reports the listed shares at their {m(p['eq_cost'])} cost. Equity securities with readily determinable fair values are carried at fair value."),
        "tr_only": (m(key_v - p["afs_fv"] + p["afs_ac"] - p["eq_fv"] + p["eq_cost"]), "Carries only the trading securities at fair value and everything else at cost. Available-for-sale debt securities and equity securities with readily determinable fair values are also carried at fair value."),
        "tr_cost": (m(key_v - p["tr_fv"] + p["tr_cost"]), f"Reports the actively traded debt securities at their {m(p['tr_cost'])} cost. Trading securities are carried at fair value, with changes in net income."),
    }
    key = (m(key_v), f"Correct. {m(p['tr_fv'])} + {m(p['afs_fv'])} + {m(p['htm_ac'])} + {m(p['eq_fv'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, Year 2, {co} holds four investments: debt securities its treasury desk bought in November and turns over within weeks as prices move, with a cost of {m(p['tr_cost'])} and a fair value of {m(p['tr_fv'])}; debt securities that {s} may sell before maturity if it needs cash, with an amortized cost of {m(p['afs_ac'])} and a fair value of {m(p['afs_fv'])}; bonds maturing in Year 9 that the board has resolved to keep until they mature, which {s}'s cash forecasts show it can do, with an amortized cost of {m(p['htm_ac'])} and a fair value of {m(p['htm_fv'])}; and {p['eq_pct']}% of the common shares of a company listed on a national stock exchange, bought for {m(p['eq_cost'])} and worth {m(p['eq_fv'])}. {s} has no significant influence over the listed company and expects to collect all contractual cash flows on its debt securities. What total carrying amount should {s} report for these investments on its December 31, Year 2, balance sheet?""",
        choices, ans,
        f"""The securities bought for short-term resale are trading securities, carried at fair value ({m(p['tr_fv'])}). The debt securities that may be sold are available for sale, also carried at fair value ({m(p['afs_fv'])}). The board's resolution and the cash forecasts show both the intent and the ability to hold the bonds to maturity, so they are held to maturity and carried at amortized cost ({m(p['htm_ac'])}), with no allowance because no credit losses are expected. The listed shares have a readily determinable fair value and no significant influence, so they are carried at fair value ({m(p['eq_fv'])}). Total = {m(key_v)}.""",
    )


def fv_income(p):
    co, s = p["co"], short(p["co"])
    deq = p["eq1"] - p["eq0"]
    gain = p["afs_px"] - p["afs_ac"]
    prior = p["afs_fv0"] - p["afs_ac"]
    intr = rd(p["b_face"] * D(p["b_rate"]) / 100)
    loss = p["b_face"] - p["b_fv1"]
    key_v = p["dv"] + deq + gain + intr
    pool = {
        "gain_fv": (m(key_v - prior), f"Measures the gain on the securities sold from their {m(p['afs_fv0'])} January 1 fair value, recognizing only {m(p['afs_px'] - p['afs_fv0'])}. The realized gain in net income is proceeds minus amortized cost, {m(gain)}; the {m(prior)} unrealized gain from Year 1 is reclassified out of accumulated other comprehensive income."),
        "eq_oci": (m(key_v - deq), f"Leaves the {m(deq)} increase in the fair value of the listed shares out of net income. Changes in the fair value of equity securities are reported in net income."),
        "afs_loss": (m(key_v - loss), f"Includes the {m(loss)} decline in the bonds' fair value in net income. With no expected credit loss and no intent or requirement to sell, the unrealized loss on available-for-sale bonds goes to other comprehensive income."),
        "double": (m(key_v + prior), f"Adds the {m(prior)} reclassified from accumulated other comprehensive income on top of the {m(gain)} realized gain. The reclassification is how the {m(gain)} reaches net income; it isn't additional income."),
    }
    key = (m(key_v), f"Correct. {m(p['dv'])} dividends + {m(deq)} fair value increase on the shares + {m(gain)} realized gain + {m(intr)} interest.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""During Year 2, {co} held these investments. First, {p['eq_pct']}% of the common shares of a listed company, over which it has no significant influence, carried at a fair value of {m(p['eq0'])} at January 1 and worth {m(p['eq1'])} at December 31; {s} received dividends of {m(p['dv'])} on them. Second, debt securities that {s} bought at par for {m(p['afs_ac'])} in Year 1 and classified as available for sale, carried at a fair value of {m(p['afs_fv0'])} at January 1, Year 2, and sold on March 1, Year 2, for {m(p['afs_px'])}; ignore interest on these securities. Third, {m(p['b_face'])} face amount of {p['b_rate']}% bonds bought at par on January 1, Year 2, and classified as available for sale, which pay interest each December 31 and were worth {m(p['b_fv1'])} at December 31 because market interest rates rose. {s} does not intend to sell the bonds, is not likely to be required to sell them before recovery, and expects to collect all of their contractual cash flows. Ignoring income taxes, what total amount should {s} recognize in net income for Year 2 from these investments?""",
        choices, ans,
        f"""Listed shares: dividends of {m(p['dv'])} plus the {m(deq)} increase in fair value, both in net income. Securities sold: the realized gain is proceeds minus amortized cost, {m(p['afs_px'])} − {m(p['afs_ac'])} = {m(gain)}, which includes the {m(prior)} unrealized gain reclassified from accumulated other comprehensive income. Bonds: interest income of {m(p['b_face'])} × {p['b_rate']}% = {m(intr)}; the {m(loss)} decline in fair value is not a credit loss and {s} won't sell, so it goes to other comprehensive income. Net income = {m(p['dv'])} + {m(deq)} + {m(gain)} + {m(intr)} = {m(key_v)}.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def deferred_net(p):
    co, s = p["co"], short(p["co"])
    dep = p["d3"] + p["d4"]
    dtl = tax(p["d3"], p["r3"]) + tax(p["d4"], p["r4"])
    dta = tax(p["w"], p["r3"])
    key_v = dtl - dta
    pool = {
        "current": (m(tax(dep - p["w"], p["r2"])), f"Measures every difference at the {pc(p['r2'])} Year 2 rate. Deferred taxes are measured at the enacted rates for the years in which the differences reverse."),
        "proposed": (m(tax(p["d3"], p["r3"]) + tax(p["d4"], p["rp"]) - dta), f"Uses the proposed {pc(p['rp'])} rate for Year 4. Only enacted rates are used; a bill that hasn't been enacted is ignored."),
        "no_dta": (m(dtl), f"Leaves out the {m(dta)} deferred tax asset on the warranty liability. The warranty costs will be deducted when paid in Year 3."),
        "latest": (m(tax(dep - p["w"], p["r4"])), f"Measures every difference at {pc(p['r4'])}, the rate for Year 4 and later. The differences reversing in Year 3 are measured at the Year 3 rate of {pc(p['r3'])}."),
        "dta_added": (m(dtl + dta), f"Adds the {m(dta)} deferred tax asset to the liability. A deferred tax asset reduces the net liability."),
    }
    key = (m(key_v), f"Correct. {m(p['d3'])} × {pc(p['r3'])} + {m(p['d4'])} × {pc(p['r4'])} − {m(p['w'])} × {pc(p['r3'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} is measuring its deferred taxes at December 31, Year 2. At that date, cumulative tax depreciation exceeds book depreciation by {m(dep)}; the difference will reverse by {m(p['d3'])} in Year 3 and {m(p['d4'])} in Year 4. {s} also has an accrued warranty liability of {m(p['w'])}, deductible for tax when paid, which it expects to pay in Year 3. During Year 2, {s} paid {m(p['fine'])} of fines that are not deductible. {s}'s enacted tax rates are {pc(p['r2'])} for Year 2, {pc(p['r3'])} for Year 3, and {pc(p['r4'])} for Year 4 and later years. In December, Year 2, a bill was proposed, but not enacted, that would set the rate for Year 4 and later years at {pc(p['rp'])}. {s} expects ample future taxable income, files in a single tax jurisdiction, and presents its deferred taxes as one net amount. What net deferred tax liability should {s} report at December 31, Year 2?""",
        choices, ans,
        f"""Deferred taxes are measured at the enacted rates expected to apply when the differences reverse; proposed legislation is ignored. Deferred tax liability: {m(p['d3'])} × {pc(p['r3'])} = {m(tax(p['d3'], p['r3']))} plus {m(p['d4'])} × {pc(p['r4'])} = {m(tax(p['d4'], p['r4']))}, for {m(dtl)}. Deferred tax asset: {m(p['w'])} × {pc(p['r3'])} = {m(dta)}. The fines are a permanent difference and create no deferred tax. Net deferred tax liability = {m(dtl)} − {m(dta)} = {m(key_v)}.""",
    )


def provision_expense(p):
    co, s = p["co"], short(p["co"])
    r = p["r"]
    cur = tax(p["T"], r)
    ddtl = tax(p["dep1"] - p["dep0"], r)
    ddta = tax(p["war1"] - p["war0"], r)
    assert ddtl > ddta > 0
    key_v = cur + ddtl - ddta
    pool = {
        "current": (m(cur), f"Debits only the {m(cur)} of current tax. The entry also records deferred tax expense for the net change in the deferred tax accounts."),
        "dta_added": (m(cur + ddtl + ddta), f"Adds the {m(ddta)} increase in the deferred tax asset to expense. An increase in a deferred tax asset is a deferred tax benefit, which reduces expense."),
        "ending": (m(cur + tax(p["dep1"], r) - tax(p["war1"], r)), f"Uses the December 31 deferred tax balances instead of the year's changes. The January 1 balances were already recorded in earlier years."),
        "no_dta": (m(cur + ddtl), f"Records the {m(ddtl)} increase in the deferred tax liability but not the {m(ddta)} increase in the deferred tax asset."),
        "no_dtl": (m(cur - ddta), f"Records the {m(ddta)} increase in the deferred tax asset but not the {m(ddtl)} increase in the deferred tax liability."),
    }
    key = (m(key_v), f"Correct. Current {m(cur)} + {m(ddtl)} increase in the liability − {m(ddta)} increase in the asset.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} records its income tax provision in a single year-end journal entry, using separate deferred tax asset and deferred tax liability accounts. Its Year 2 taxable income is {m(p['T'])}, and the enacted tax rate is {pc(r)} for all years. At January 1, Year 2, cumulative tax depreciation exceeded book depreciation by {m(p['dep0'])}, and {s} had an accrued warranty liability of {m(p['war0'])}; warranty costs are deductible when paid. At December 31, Year 2, those amounts are {m(p['dep1'])} and {m(p['war1'])}. {s} has no other temporary differences and expects ample future taxable income. In its Year 2 entry, what amount should {s} debit to income tax expense?""",
        choices, ans,
        f"""The entry is: debit income tax expense and the deferred tax asset; credit income taxes payable and the deferred tax liability. Current tax = {m(p['T'])} × {pc(r)} = {m(cur)}. The deferred tax liability increases by ({m(p['dep1'])} − {m(p['dep0'])}) × {pc(r)} = {m(ddtl)}. The deferred tax asset increases by ({m(p['war1'])} − {m(p['war0'])}) × {pc(r)} = {m(ddta)}, a deferred benefit. Income tax expense = {m(cur)} + {m(ddtl)} − {m(ddta)} = {m(key_v)}.""",
    )


def dtl_credit(p):
    co, s = p["co"], short(p["co"])
    r = p["r"]
    dd = tax(p["d1"] - p["d0"], r)
    du = tax(p["u1"] - p["u0"], r)
    dc = tax(p["c1"] - p["c0"], r)
    key_v = dd + du
    cword = "increase" if dc > 0 else "decrease"
    pool = {
        "no_oci": (m(dd), f"Records only the deferred tax on depreciation. The {m(du)} tax effect of the Year 2 unrealized gain on the available-for-sale securities is also credited to the deferred tax liability, with the debit to other comprehensive income."),
        "ending": (m(tax(p["d1"] + p["u1"], r)), f"Credits the whole December 31 liability. Only the change during Year 2 is recorded; the January 1 balance is already on the books."),
        "no_beg": (m(dd + tax(p["u1"], r)), f"Records deferred tax on the whole {m(p['u1'])} of December 31 unrealized gains. {m(p['u0'])} of those gains arose before Year 2 and was tax-effected then."),
        "net_dta": (m(key_v - dc), f"Nets the {m(abs(dc))} {cword} in the deferred tax asset for accrued compensation into the liability. {s} keeps separate asset and liability accounts, so that change is recorded in the asset account."),
    }
    key = (m(key_v), f"Correct. ({m(p['d1'])} − {m(p['d0'])}) × {pc(r)} + ({m(p['u1'])} − {m(p['u0'])}) × {pc(r)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} keeps separate deferred tax asset and deferred tax liability accounts and records all of its Year 2 income tax entries at December 31. The enacted tax rate is {pc(r)} for all years, and {s} expects ample future taxable income. Its temporary differences were: cumulative tax depreciation in excess of book depreciation, {m(p['d0'])} at January 1, Year 2, and {m(p['d1'])} at December 31; unrealized holding gains on available-for-sale debt securities, which are taxed when the securities are sold, {m(p['u0'])} at January 1 and {m(p['u1'])} at December 31; and accrued compensation that is deductible when paid, {m(p['c0'])} at January 1 and {m(p['c1'])} at December 31. What total amount should {s} credit to the deferred tax liability account for Year 2?""",
        choices, ans,
        f"""Both taxable temporary differences grew during Year 2, and each increase is recorded in the deferred tax liability account. Depreciation: ({m(p['d1'])} − {m(p['d0'])}) × {pc(r)} = {m(dd)}, charged to deferred tax expense. Unrealized gains: ({m(p['u1'])} − {m(p['u0'])}) × {pc(r)} = {m(du)}, charged to other comprehensive income, where the gain itself is reported (intraperiod tax allocation). Total credit = {m(key_v)}. The {m(abs(dc))} {cword} in the deferred tax asset on accrued compensation is recorded in the separate asset account.""",
    )


def lessee_rou(p):
    co, s = p["co"], short(p["co"])
    pv = rd(p["P"] * D(p["due"]))
    liab = pv - p["P"]
    key_v = pv + p["idc"] - p["inc"]
    pool = {
        "no_idc": (m(key_v - p["idc"]), f"Leaves out the {m(p['idc'])} commission. A commission owed only because the lease was signed is an initial direct cost, added to the right-of-use asset."),
        "no_inc": (m(key_v + p["inc"]), f"Doesn't subtract the {m(p['inc'])} incentive received from the lessor. Lease incentives received reduce the right-of-use asset."),
        "liab": (m(liab), f"Reports the {m(liab)} lease liability. The right-of-use asset also includes the payment made at commencement and initial direct costs, less incentives received."),
        "ordinary": (m(rd(p["P"] * D(p["ord"])) + p["idc"] - p["inc"]), f"Discounts the payments as an ordinary annuity. The payments are due at the start of each year, so the annuity-due factor applies."),
        "legal": (m(key_v + p["legal"]), f"Adds the {m(p['legal'])} of legal fees. Costs of negotiating a lease are incurred whether or not the lease is signed, so they aren't initial direct costs; they are expensed."),
    }
    key = (m(key_v), f"Correct. {m(p['P'])} × {p['due']} = {m(pv)}, + {m(p['idc'])} commission − {m(p['inc'])} incentive.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co}, a public business entity, signs a {p['n']}-year lease of office space, which begins that day and which {s} classifies as an operating lease. Annual payments of {m(p['P'])} are due each January 1, beginning at commencement, and {s} made the first payment on January 1, Year 1. The rate implicit in the lease isn't readily determinable, and {s}'s incremental borrowing rate is {p['r']}%. At commencement, {s} paid a leasing agent a {m(p['idc'])} commission that was due only upon signing and paid {m(p['legal'])} of outside legal fees for negotiating the lease terms, and the lessor paid {s} {m(p['inc'])} in cash as an incentive to sign. Present value factors at {p['r']}% for {p['n']} periods are {p['due']} for an annuity due and {p['ord']} for an ordinary annuity. At what amount should {s} initially measure its right-of-use asset?""",
        choices, ans,
        f"""The lease liability is the present value of the payments not yet made: {m(p['P'])} × {p['due']} = {m(pv)} for all {p['n']} payments, less the {m(p['P'])} paid at commencement, = {m(liab)}. The right-of-use asset = the liability + payments made at or before commencement + initial direct costs − lease incentives received = {m(liab)} + {m(p['P'])} + {m(p['idc'])} − {m(p['inc'])} = {m(key_v)}. The commission is an initial direct cost because it was owed only if the lease was signed; the legal fees for negotiating the terms are not, and are expensed.""",
    )


def se_inventory(p):
    co, s = p["co"], short(p["co"])
    wd = p["obs_cost"] - p["obs_nrv"]
    key_v = p["inv"] - wd - p["leak"]
    pool = {
        "flood": (m(key_v - p["flood"]), f"Also writes off the {m(p['flood'])} of goods destroyed by the February flood. The flood is a condition that arose after year-end, so it is disclosed, not recognized."),
        "price": (m(key_v - (p["b_cost"] - p["b_nrv"])), f"Also writes the headphone line down by {m(p['b_cost'] - p['b_nrv'])} for the February price cuts. The cuts respond to a February market decline, a condition that arose after year-end."),
        "sold": (m(p["inv"] - p["obs_cost"] - p["leak"]), f"Removes the whole {m(p['obs_cost'])} of speakers sold in January. They were on hand at December 31; the sale shows that their net realizable value was {m(p['obs_nrv'])}, so they are written down by {m(wd)}, not removed."),
        "no_obs": (m(key_v + wd), f"Doesn't write down the speakers. Their value collapsed in November, Year 1, and the January sale is evidence of their net realizable value at year-end."),
        "no_leak": (m(key_v + p["leak"]), f"Keeps the {m(p['leak'])} of goods damaged in December in inventory. The damage happened in Year 1, so those goods had no value at year-end."),
    }
    key = (m(key_v), f"Correct. {m(p['inv'])} − {m(wd)} write-down of the speakers − {m(p['leak'])} of goods damaged in December.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} measures its inventory at the lower of FIFO cost and net realizable value. Its December 31, Year 1, inventory count, priced at cost, totals {m(p['inv'])}, and its financial statements will be issued on March 12, Year 2. The following came to light after year-end: on January 18, {s} sold its entire stock of one line of speakers, carried at {m(p['obs_cost'])}, for {m(p['obs_nrv'])} net of selling costs; demand for those speakers had collapsed in November, Year 1, when a competitor released a cheaper successor model. On January 25, {s} found that goods costing {m(p['leak'])} included in the count had been ruined by a roof leak in December and scrapped them. On February 6, a flood destroyed uninsured goods costing {m(p['flood'])} that had been on hand at year-end. On February 22, after commodity prices fell sharply in February, {s} cut its selling prices on a headphone line, so that the net realizable value of the headphones it held at year-end, which cost {m(p['b_cost'])}, is now {m(p['b_nrv'])}. What amount should {s} report as inventory at December 31, Year 1?""",
        choices, ans,
        f"""Events that give evidence about conditions at the balance sheet date are recognized; those that reflect conditions arising after it are disclosed. The speakers' value had collapsed in November, so the January sale is evidence of their year-end net realizable value: write down {m(p['obs_cost'])} − {m(p['obs_nrv'])} = {m(wd)}. The goods ruined in December had no value at year-end: remove {m(p['leak'])}. The February flood and the February price cuts arose after year-end, so they are not recognized. Inventory = {m(p['inv'])} − {m(wd)} − {m(p['leak'])} = {m(key_v)}.""",
    )


def se_litigation(p):
    co, s = p["co"], short(p["co"])
    draft = p["acc1"] + p["env_acc"]
    key_v = p["settle1"] + p["defect"] + p["env_acc"]
    pool = {
        "accident": (m(key_v + p["accident"]), f"Also accrues the {m(p['accident'])} for the January truck accident. The accident happened after year-end, so it is disclosed, not recognized."),
        "keep": (m(key_v - (p["settle1"] - p["acc1"])), f"Keeps the {m(p['acc1'])} accrual for the injury suit. The February settlement is evidence of the liability that existed at year-end, so the accrual rises to {m(p['settle1'])}."),
        "no_defect": (m(key_v - p["defect"]), f"Doesn't accrue the {m(p['defect'])} for the defective December shipment. The defect existed at year-end; the January claim and February agreement are evidence of that liability."),
        "env": (m(key_v - p["env_acc"] + p["env_settle"]), f"Uses the {m(p['env_settle'])} March 20 settlement of the state agency's claim. That settlement came after the statements were issued on March 10, so it isn't reflected in them."),
        "draft": (m(draft), "Makes no adjustment to the unadjusted balances."),
    }
    key = (m(key_v), f"Correct. {m(p['settle1'])} injury settlement + {m(p['defect'])} shipment claim + {m(p['env_acc'])} state agency claim.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31, Year 1, financial statements were issued on March 10, Year 2. Its unadjusted trial balance reports accrued liabilities for claims and litigation of {m(draft)}: {m(p['acc1'])} for a suit by a customer injured at one of {s}'s stores in September, Year 1, and {m(p['env_acc'])} for a state agency's claim over a chemical spill at {s}'s plant in Year 1, which was {s}'s best estimate at year-end and was still its best estimate when the statements were issued. After year-end: on January 8, a customer filed a claim over a defective shipment it received from {s} in December, and on February 2, {s} agreed to pay it {m(p['defect'])}; on January 22, one of {s}'s delivery trucks injured a pedestrian, who sued in February, and {s}'s counsel expects {s} to pay about {m(p['accident'])}; on February 12, {s} settled the customer injury suit for {m(p['settle1'])}; and on March 20, {s} settled the state agency's claim for {m(p['env_settle'])}. What total liability for claims and litigation should {s} report on its December 31, Year 1, balance sheet?""",
        choices, ans,
        f"""Events before the statements are issued that give evidence about conditions existing at year-end are recognized. The injury suit arose in Year 1, so its accrual rises to the {m(p['settle1'])} settlement. The defective shipment was made in December, so the {m(p['defect'])} agreed in February is accrued. The truck accident happened in January: disclose it, don't accrue it. The state agency's claim stays at {m(p['env_acc'])}, the best estimate when the statements were issued; the March 20 settlement came after issuance. Total = {m(p['settle1'])} + {m(p['defect'])} + {m(p['env_acc'])} = {m(key_v)}.""",
    )


def se_current_ratio(p):
    co, s = p["co"], short(p["co"])
    wd = p["obs_cost"] - p["obs_nrv"]
    ca, cl = p["ca"] - wd, p["cl"] + p["settle"] - p["acc"]
    r2 = lambda a, b: str(rd(D(a) / D(b), "0.01"))
    key_v = r2(ca, cl)
    pool = {
        "flood": (r2(ca - p["flood"], cl), f"Also removes the {m(p['flood'])} of inventory destroyed in the February flood, a condition that arose after year-end. It is disclosed, not recognized."),
        "dividend": (r2(ca, cl + p["div"]), f"Also adds the {m(p['div'])} dividend declared in February as a liability. A dividend is a liability only once declared, after year-end here."),
        "full": (r2(ca, p["cl"] + p["settle"]), f"Adds the whole {m(p['settle'])} settlement to current liabilities without removing the {m(p['acc'])} already accrued."),
        "no_inv": (r2(p["ca"], cl), f"Doesn't write down the obsolete inventory. It became obsolete in October, Year 1, and the February sale is evidence of its net realizable value at year-end."),
        "draft": (r2(p["ca"], p["cl"]), "Uses the draft balances without any subsequent-event adjustments."),
    }
    key = (key_v, f"Correct. ({m(p['ca'])} − {m(wd)}) ÷ ({m(p['cl'])} + {m(p['settle'] - p['acc'])}) = {m(ca)} ÷ {m(cl)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s loan agreement requires a current ratio of at least {p['cov']} at each December 31. Before considering subsequent events, {s}'s draft December 31, Year 1, balance sheet reports current assets of {m(p['ca'])} and current liabilities of {m(p['cl'])}, which include a {m(p['acc'])} accrued liability for a suit over an injury at {s}'s plant in Year 1. The statements will be issued on March 5, Year 2. After year-end: on January 18, {s} settled the suit for {m(p['settle'])}, payable in April; on February 3, {s} sold inventory that had cost {m(p['obs_cost'])} for {m(p['obs_nrv'])}, net of selling costs, because a competitor's product introduced in October, Year 1, had made it obsolete; on February 14, a flood destroyed uninsured inventory that had cost {m(p['flood'])}; and on February 25, the board declared a cash dividend of {m(p['div'])}, payable March 20. After any adjustments required, what current ratio should {s} report at December 31, Year 1, rounded to two decimal places?""",
        choices, ans,
        f"""Recognized: the settlement of a Year 1 injury suit raises the accrued liability by {m(p['settle'])} − {m(p['acc'])} = {m(p['settle'] - p['acc'])}, and the sale of inventory made obsolete in October shows a year-end net realizable value {m(wd)} below cost. Not recognized (disclosed): the February flood and the February dividend declaration. Current assets = {m(p['ca'])} − {m(wd)} = {m(ca)}; current liabilities = {m(p['cl'])} + {m(p['settle'] - p['acc'])} = {m(cl)}. Current ratio = {m(ca)} ÷ {m(cl)} = {key_v}, which {'meets' if D(key_v) >= D(p['cov']) else 'falls below'} the {p['cov']} the loan agreement requires.""",
    )


def se_allowance(p):
    co, s = p["co"], short(p["co"])
    lost = p["b_bal"] - rd(p["b_bal"] * D(p["pct"]) / 100)
    key_v = p["al"] + lost - p["b_in"]
    pool = {
        "tornado": (m(key_v + p["t_bal"]), f"Also provides for the {m(p['t_bal'])} owed by Stainton Traders. Stainton was sound at year-end; the March tornado is a condition that arose after year-end."),
        "late": (m(key_v + p["l_bal"] - p["l_in"]), f"Also raises the allowance for Ruskin Mills to its full {m(p['l_bal'])} balance. Ruskin's bankruptcy came on April 10, after the statements were available to be issued on April 2, the date through which a company that is not an SEC filer evaluates subsequent events."),
        "no_existing": (m(key_v + p["b_in"]), f"Adds the whole {m(lost)} expected loss on Pryce without removing the {m(p['b_in'])} already in the allowance for it."),
        "full": (m(key_v + p["b_bal"] - lost), f"Provides for Pryce's whole {m(p['b_bal'])} balance. {s} expects to collect {p['pct']}% of it, so the expected loss is {m(lost)}."),
        "draft": (m(p["al"]), "Makes no adjustment to the draft allowance."),
    }
    key = (m(key_v), f"Correct. {m(p['al'])} + ({m(lost)} expected loss on Pryce − {m(p['b_in'])} already provided).")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}, a private company that is not an SEC filer, is finalizing its December 31, Year 1, financial statements. They were available to be issued on April 2, Year 2, and {s} delivered them to its lender on April 20. The draft allowance for credit losses is {m(p['al'])}. It includes {m(p['b_in'])} for the {m(p['b_bal'])} owed by Pryce Foods and {m(p['l_in'])} for the {m(p['l_bal'])} owed by Ruskin Mills, and nothing specific for the {m(p['t_bal'])} owed by Stainton Traders, which was current and financially sound at year-end. After year-end: on February 8, Pryce Foods, which had reported losses throughout Year 1, filed for bankruptcy, and {s} now expects to collect {p['pct']}% of Pryce's balance; on March 3, a tornado destroyed Stainton's only warehouse, and {s} now expects to collect nothing from Stainton; and on April 10, Ruskin Mills, whose balance was 120 days past due at year-end and which had defaulted on its bank loans in November, Year 1, filed for bankruptcy. {s} has not elected the ASU 2025-05 practical expedient or the related accounting policy election for current receivables. The draft's {m(p['l_in'])} for Ruskin was management's expected credit loss at year-end, based on all information then available, including the past-due balance and the loan default. What allowance for credit losses should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""A company that is not an SEC filer evaluates subsequent events through the date its statements are available to be issued, here April 2. Pryce's bankruptcy on February 8 resulted from losses during Year 1, so it is evidence about a year-end condition: the expected loss is {m(p['b_bal'])} − {p['pct']}% collected = {m(lost)}, and the allowance rises by {m(lost)} − {m(p['b_in'])} = {m(lost - p['b_in'])}. The tornado arose after year-end: disclose it, don't recognize it. Ruskin's bankruptcy on April 10 came after the available-to-be-issued date, so these statements don't reflect it. Allowance = {m(p['al'])} + {m(lost - p['b_in'])} = {m(key_v)}.""",
    )


# ── Families: parameter set 0 is the item, sets 1-3 its variants ──────────

FAMILIES = [
    # Area I
    ("far-income-statement-0004", A1, "Income statement", AP,
     ["ASC 220-10 (income statement presentation)", "ASC 205-20 (discontinued operations)", "ASC 321-10 (equity securities: fair value changes in net income)", "ASC 320-10 (available-for-sale debt securities: unrealized holding gains in other comprehensive income)"],
     income_continuing, [
        dict(co="Easby Corp.", sales=2400000, ret=60000, cogs=1380000, sell=240000, ga=310000, intrev=18000, intexp=45000, gain=22000, eqg=15000, afs=30000, disc=90000, div=50000, use=["disc", "no_equity", "div"]),
        dict(co="Fenby Corp.", sales=3150000, ret=85000, cogs=1890000, sell=320000, ga=405000, intrev=24000, intexp=60000, gain=31000, eqg=26000, afs=42000, disc=130000, div=75000, use=["afs", "gross", "div"]),
        dict(co="Glaisdale Corp.", sales=1760000, ret=40000, cogs=1010000, sell=185000, ga=230000, intrev=12000, intexp=36000, gain=15000, eqg=11000, afs=24000, disc=65000, div=30000, use=["disc", "afs", "gross"]),
        dict(co="Hathersage Corp.", sales=4200000, ret=110000, cogs=2480000, sell=430000, ga=560000, intrev=35000, intexp=82000, gain=40000, eqg=33000, afs=55000, disc=170000, div=100000, use=["no_equity", "gross", "disc"]),
     ]),
    ("far-cash-flows-0008", A1, "Statement of cash flows", AP,
     ["ASC 230-10-50 (supplemental disclosure of interest paid, net of amounts capitalized)", "ASC 835-20 (capitalization of interest)", "ASC 835-30 (amortization of discount)"],
     interest_paid, [
        dict(co="Farndale Co.", ie=84000, amort=6000, cap=16000, ip0=9000, ip1=14000, use=["gross", "no_payable", "payable_sign"]),
        dict(co="Grinton Co.", ie=126000, amort=9000, cap=22000, ip0=21000, ip1=15000, use=["cap_twice", "gross", "add_amort"]),
        dict(co="Hawes Co.", ie=58000, amort=4000, cap=12000, ip0=6000, ip1=9000, use=["cap_twice", "no_payable", "gross"]),
        dict(co="Ingleton Co.", ie=212000, amort=15000, cap=38000, ip0=30000, ip1=22000, use=["cap_twice", "payable_sign", "no_payable"]),
     ]),
    ("far-consolidated-statements-0008", A1, "Consolidated financial statements", AP,
     ["ASC 810-10 (consolidation procedures: intercompany eliminations; attribution of net income to the parent and the noncontrolling interest)"],
     consolidated_correction, [
        dict(parent="Gilmore Corp.", sub="Holme Inc.", pct=80, sub_ni=300000, divs=50000, amort=20000, up=15000, fee=30000, parent_own=720000, use=["keep_div", "no_amort", "fee"]),
        dict(parent="Keswick Corp.", sub="Lorton Inc.", pct=70, sub_ni=420000, divs=80000, amort=30000, up=20000, fee=45000, parent_own=960000, use=["full", "fee", "keep_div"]),
        dict(parent="Morland Corp.", sub="Newby Inc.", pct=90, sub_ni=250000, divs=40000, amort=10000, up=12000, fee=25000, parent_own=610000, use=["fee", "no_amort", "keep_div"]),
        dict(parent="Penrith Corp.", sub="Quernmore Inc.", pct=75, sub_ni=520000, divs=100000, amort=36000, up=24000, fee=60000, parent_own=1340000, use=["full", "no_upstream", "no_amort"]),
     ]),
    ("far-cash-flows-0009", A1, "Statement of cash flows", AN,
     ["ASC 230-10-45 (classification of cash receipts and payments, including insurance proceeds)", "ASC 230-10-50 (noncash investing and financing activities)", "ASC 230-10-20 (cash equivalents)"],
     cf_investing, [
        dict(co="Ingleby Co.", sale_cv=70000, sale_px=95000, mach_cost=500000, mach_cash=260000, ins=120000, tbill=50000, land=200000, interest=8000, note_prin=40000, use=["gain", "tbills", "ins_op"]),
        dict(co="Jervaulx Co.", sale_cv=110000, sale_px=140000, mach_cost=720000, mach_cash=390000, ins=150000, tbill=80000, land=260000, interest=12000, note_prin=55000, use=["interest", "full_cost", "land"]),
        dict(co="Knaresby Co.", sale_cv=45000, sale_px=62000, mach_cost=340000, mach_cash=180000, ins=70000, tbill=30000, land=150000, interest=5000, note_prin=25000, use=["interest", "note_prin", "tbills"]),
        dict(co="Lindale Co.", sale_cv=150000, sale_px=190000, mach_cost=900000, mach_cash=520000, ins=210000, tbill=100000, land=320000, interest=15000, note_prin=70000, use=["interest", "gain", "land"]),
     ]),
    # Area II
    ("far-investments-fair-value-0001", A2, "Investments (Financial assets at fair value)", AP,
     ["ASC 320-10 (trading, available-for-sale and held-to-maturity debt securities)", "ASC 321-10 (equity securities with readily determinable fair values)"],
     fv_carrying, [
        dict(co="Kirkby Co.", tr_cost=150000, tr_fv=138000, afs_ac=300000, afs_fv=345000, htm_ac=480000, htm_fv=455000, eq_pct=3, eq_cost=90000, eq_fv=125000, use=["htm_fv", "afs_cost", "tr_only"]),
        dict(co="Lowther Co.", tr_cost=220000, tr_fv=236000, afs_ac=410000, afs_fv=384000, htm_ac=600000, htm_fv=572000, eq_pct=2, eq_cost=140000, eq_fv=121000, use=["tr_cost", "htm_fv", "afs_cost"]),
        dict(co="Millom Co.", tr_cost=110000, tr_fv=96000, afs_ac=260000, afs_fv=281000, htm_ac=350000, htm_fv=362000, eq_pct=4, eq_cost=80000, eq_fv=52000, use=["tr_cost", "eq_cost", "afs_cost"]),
        dict(co="Naworth Co.", tr_cost=310000, tr_fv=327000, afs_ac=520000, afs_fv=496000, htm_ac=750000, htm_fv=690000, eq_pct=5, eq_cost=180000, eq_fv=214000, use=["tr_cost", "eq_cost", "htm_fv"]),
     ]),
    ("far-investments-fair-value-0002", A2, "Investments (Financial assets at fair value)", AP,
     ["ASC 320-10 (available-for-sale debt securities: unrealized holding gains and losses; reclassification on sale)", "ASC 321-10 (equity securities: changes in fair value in net income)", "ASC 326-30 (credit losses on available-for-sale debt securities)"],
     fv_income, [
        dict(co="Kirkwood Co.", eq_pct=4, eq0=200000, eq1=226000, dv=6000, afs_ac=100000, afs_fv0=108000, afs_px=111000, b_face=250000, b_rate=4, b_fv1=236000, use=["gain_fv", "eq_oci", "afs_loss"]),
        dict(co="Lamplugh Co.", eq_pct=3, eq0=320000, eq1=351000, dv=9000, afs_ac=150000, afs_fv0=162000, afs_px=166000, b_face=400000, b_rate=5, b_fv1=381000, use=["double", "gain_fv", "eq_oci"]),
        dict(co="Muncaster Co.", eq_pct=2, eq0=140000, eq1=158000, dv=4000, afs_ac=80000, afs_fv0=87000, afs_px=90000, b_face=200000, b_rate=6, b_fv1=183000, use=["double", "afs_loss", "gain_fv"]),
        dict(co="Netherby Co.", eq_pct=5, eq0=450000, eq1=492000, dv=12000, afs_ac=220000, afs_fv0=236000, afs_px=241000, b_face=500000, b_rate=4, b_fv1=468000, use=["double", "eq_oci", "afs_loss"]),
     ]),
    # Area III
    ("far-income-taxes-deferred-0002", A3, "Accounting for income taxes", AP,
     ["ASC 740-10 (measuring deferred tax assets and liabilities at enacted rates for the years the differences reverse)", "ASC 740-10-45 (balance sheet presentation of deferred taxes)"],
     deferred_net, [
        dict(co="Hexham Corp.", d3=80000, d4=120000, w=50000, fine=30000, r2=20, r3=24, r4=28, rp=23, use=["no_dta", "latest", "proposed"]),
        dict(co="Ilsley Corp.", d3=60000, d4=140000, w=40000, fine=25000, r2=25, r3=23, r4=21, rp=18, use=["current", "proposed", "no_dta"]),
        dict(co="Jevington Corp.", d3=150000, d4=100000, w=70000, fine=40000, r2=21, r3=23, r4=26, rp=24, use=["current", "proposed", "dta_added"]),
        dict(co="Kentmere Corp.", d3=90000, d4=210000, w=60000, fine=20000, r2=30, r3=27, r4=24, rp=21, use=["current", "no_dta", "dta_added"]),
     ]),
    ("far-income-taxes-provision-0002", A3, "Accounting for income taxes", AP,
     ["ASC 740-10 (current and deferred tax expense; deferred tax assets and liabilities)"],
     provision_expense, [
        dict(co="Lathom Corp.", T=480000, r=25, dep0=120000, dep1=180000, war0=40000, war1=64000, use=["current", "dta_added", "ending"]),
        dict(co="Mapperley Corp.", T=720000, r=21, dep0=200000, dep1=300000, war0=50000, war1=90000, use=["no_dtl", "current", "no_dta"]),
        dict(co="Nettleton Corp.", T=360000, r=25, dep0=80000, dep1=140000, war0=30000, war1=46000, use=["no_dta", "dta_added", "ending"]),
        dict(co="Ormskirk Corp.", T=950000, r=21, dep0=60000, dep1=160000, war0=90000, war1=130000, use=["no_dtl", "current", "ending"]),
     ]),
    ("far-income-taxes-provision-0003", A3, "Accounting for income taxes", AP,
     ["ASC 740-10 (deferred tax liabilities)", "ASC 740-20 (intraperiod tax allocation: tax effects of items in other comprehensive income)", "ASC 320-10 (available-for-sale debt securities)"],
     dtl_credit, [
        dict(co="Pendle Corp.", r=21, d0=300000, d1=380000, u0=40000, u1=100000, c0=50000, c1=70000, use=["no_oci", "ending", "no_beg"]),
        dict(co="Quorndon Corp.", r=25, d0=220000, d1=300000, u0=30000, u1=70000, c0=60000, c1=84000, use=["ending", "no_beg", "net_dta"]),
        dict(co="Rufford Corp.", r=21, d0=500000, d1=560000, u0=80000, u1=150000, c0=90000, c1=60000, use=["ending", "no_beg", "net_dta"]),
        dict(co="Sedbergh Corp.", r=25, d0=140000, d1=200000, u0=20000, u1=52000, c0=36000, c1=52000, use=["no_oci", "net_dta", "ending"]),
     ]),
    ("far-lessee-operating-0004", A3, "Lessee accounting", AP,
     ["ASC 842-20 (lessee initial measurement of the lease liability and right-of-use asset)", "ASC 842-10 (initial direct costs; lease incentives)"],
     lessee_rou, [
        dict(co="Thornaby Co.", P=50000, n=8, r=7, due="6.3893", ord="5.9713", idc=6000, legal=3000, inc=10000, use=["no_idc", "no_inc", "liab"]),
        dict(co="Upholland Co.", P=72000, n=6, r=6, due="5.2124", ord="4.9173", idc=8000, legal=5000, inc=15000, use=["legal", "no_inc", "ordinary"]),
        dict(co="Vowchurch Co.", P=36000, n=10, r=8, due="7.2469", ord="6.7101", idc=4000, legal=2500, inc=6000, use=["liab", "ordinary", "no_idc"]),
        dict(co="Wetheral Co.", P=90000, n=5, r=5, due="4.5460", ord="4.3295", idc=9000, legal=6000, inc=20000, use=["legal", "no_idc", "liab"]),
     ]),
    ("far-subsequent-events-0005", A3, "Subsequent events", AP,
     ["ASC 855-10 (recognized and nonrecognized subsequent events)", "ASC 330-10 (lower of cost and net realizable value)"],
     se_inventory, [
        dict(co="Wexley Co.", inv=900000, obs_cost=120000, obs_nrv=85000, leak=25000, flood=60000, b_cost=200000, b_nrv=170000, use=["flood", "price", "sold"]),
        dict(co="Yeadon Co.", inv=1250000, obs_cost=160000, obs_nrv=104000, leak=38000, flood=90000, b_cost=240000, b_nrv=195000, use=["no_obs", "flood", "no_leak"]),
        dict(co="Axholme Co.", inv=640000, obs_cost=90000, obs_nrv=66000, leak=14000, flood=45000, b_cost=150000, b_nrv=128000, use=["price", "no_leak", "sold"]),
        dict(co="Brampton Co.", inv=1580000, obs_cost=210000, obs_nrv=150000, leak=42000, flood=120000, b_cost=300000, b_nrv=252000, use=["no_obs", "no_leak", "price"]),
     ]),
    ("far-subsequent-events-0006", A3, "Subsequent events", AP,
     ["ASC 855-10 (recognized and nonrecognized subsequent events; evaluation through the date the statements are issued)", "ASC 450-20 (loss contingencies)"],
     se_litigation, [
        dict(co="Caister Co.", acc1=150000, settle1=190000, defect=45000, accident=100000, env_acc=80000, env_settle=110000, use=["accident", "no_defect", "draft"]),
        dict(co="Denby Co.", acc1=220000, settle1=265000, defect=60000, accident=140000, env_acc=120000, env_settle=150000, use=["accident", "env", "draft"]),
        dict(co="Elland Co.", acc1=90000, settle1=118000, defect=32000, accident=75000, env_acc=55000, env_settle=70000, use=["accident", "no_defect", "env"]),
        dict(co="Frodsham Co.", acc1=310000, settle1=360000, defect=85000, accident=200000, env_acc=150000, env_settle=195000, use=["keep", "no_defect", "accident"]),
     ]),
    ("far-subsequent-events-0007", A3, "Subsequent events", AN,
     ["ASC 855-10 (recognized and nonrecognized subsequent events)", "ASC 210-10 (current assets and current liabilities)", "ASC 330-10 (lower of cost and net realizable value)"],
     se_current_ratio, [
        dict(co="Garsdale Co.", cov="1.75", ca=1800000, cl=900000, acc=180000, settle=260000, obs_cost=150000, obs_nrv=90000, flood=240000, div=100000, use=["flood", "dividend", "full"]),
        dict(co="Hebden Co.", cov="1.40", ca=2400000, cl=1500000, acc=240000, settle=330000, obs_cost=200000, obs_nrv=120000, flood=260000, div=150000, use=["no_inv", "draft", "flood"]),
        dict(co="Ickworth Co.", cov="2.00", ca=1300000, cl=560000, acc=100000, settle=150000, obs_cost=110000, obs_nrv=70000, flood=180000, div=80000, use=["dividend", "no_inv", "full"]),
        dict(co="Kelmscott Co.", cov="1.60", ca=3100000, cl=1700000, acc=300000, settle=420000, obs_cost=260000, obs_nrv=170000, flood=350000, div=200000, use=["no_inv", "draft", "dividend"]),
     ]),
    ("far-subsequent-events-0008", A3, "Subsequent events", AN,
     ["ASC 855-10 (subsequent events; evaluation through the date the statements are available to be issued for an entity that is not an SEC filer)", "ASC 326-20 (allowance for credit losses)"],
     se_allowance, [
        dict(co="Langdale Co.", al=64000, b_bal=90000, b_in=12000, pct=30, l_bal=35000, l_in=14000, t_bal=40000, use=["tornado", "late", "draft"]),
        dict(co="Malham Co.", al=88000, b_bal=120000, b_in=18000, pct=25, l_bal=48000, l_in=20000, t_bal=55000, use=["draft", "tornado", "late"]),
        dict(co="Nidderdale Co.", al=47000, b_bal=60000, b_in=9000, pct=40, l_bal=26000, l_in=10000, t_bal=32000, use=["draft", "no_existing", "full"]),
        dict(co="Otterburn Co.", al=126000, b_bal=160000, b_in=22000, pct=20, l_bal=70000, l_in=25000, t_bal=85000, use=["no_existing", "late", "tornado"]),
     ]),
]


ASOF = "U.S. GAAP (ASC 740) and federal tax law in effect for 2026; rates are as stated in the stem"


def main():
    items = [family(*f) for f in FAMILIES]
    for it in items:
        if it["id"].startswith("far-income-taxes-"):
            it["review"]["asOf"] = ASOF
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
    warnings = audit(items)
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    if "--dry" in sys.argv:
        for it in items:
            for label, v in [("v0", it)] + [(f"v{i}", x) for i, x in enumerate(it["variants"], 1)]:
                print(it["id"], label, " | ".join(("*" if c["id"] == v["answer"] else "") + c["text"] for c in v["choices"]))
        return
    write_items(items, CONTENT)


if __name__ == "__main__":
    main()
