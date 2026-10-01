"""FAR batch 09 — 25 items written from scratch for blueprint tasks in Areas I and II: the three tasks with no
items (II.E.1a, II.E.3a, II.F.a), the Area I "adjust ... to correct identified errors" tasks, and a second or
later item on each Area I and II Analysis task (statement discrepancies, notes, bank, receivables, inventory and
PP&E rollforwards and reconciliations). Target skill mix 3 / 12 / 10; area mix 11 / 14 / 0. Scope and skill tags
follow the AICPA CPA Exam Blueprints effective January 2026.

Numeric items ship with three variants each (method as in far-batch-06.py): each item is a builder, parameter
set 0 is the item and sets 1-3 are its variants, and every family must move the key's letter.

Run: python3 scripts/batches/far-batch-09.py   See docs/reviews/far-batch-09.md.
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import os
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AN, AP, RU, attach_variants, audit, finalize, fix_articles, mcq as _mcq, variant, write_items  # noqa: E402
from variants import m, pick, rd  # noqa: E402

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
NOTE = "Batch 09. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


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


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole amount, got {x}"
    return x


def distinct(pool, key, positive=True):
    """No pool value may equal the key or another pool value; amounts must be positive."""
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"
    if positive:
        assert all(not v.startswith("$-") and v != "$0" for v in vals if v.startswith("$")), vals


def build(pool, key, use, **kw):
    distinct(pool, key, **kw)
    return pick(pool, key, use)


def gl(x):
    """A signed amount as '$4,000 net gain' / '$4,000 net loss'."""
    x = D(x)
    assert x != 0
    return f"{m(abs(x))} net {'gain' if x > 0 else 'loss'}"


def usd(x):
    return f"${D(x):.2f}"


# ── Area I ───────────────────────────────────────────────────────────────


def balance_sheet_adjust(p):
    co, s = p["co"], short(p["co"])
    exp = whole(D(p["prem"]) * 3 / 12)
    intr = whole(D(p["note"]) * p["rate"] / 100 * 4 / 12)
    key_v = p["ta"] - exp - p["dep"] + p["cb"] + intr
    pool = {
        "prepaid_all": (m(key_v - (p["prem"] - exp)), f"Removes the whole {m(p['prem'])} premium from prepaid insurance. Only the three months from October through December have expired ({m(exp)}); nine months of coverage remain an asset."),
        "no_cb": (m(key_v - p["cb"]), f"Leaves receivables net of the {m(p['cb'])} of customer credit balances. Credit balances are liabilities, so receivables are reported at the total of the debit balances."),
        "div": (m(key_v - p["div"]), f"Also subtracts the {m(p['div'])} dividend from total assets. Declaring a dividend creates a liability and reduces retained earnings; no asset changes until it is paid."),
        "no_dep": (m(key_v + p["dep"]), f"Leaves out the {m(p['dep'])} of unrecorded depreciation, which reduces the van's carrying amount."),
        "int_year": (m(key_v + whole(D(p["note"]) * p["rate"] / 100) - intr), f"Accrues a full year of interest. Only September through December (four months) has been earned by December 31: {m(intr)}."),
    }
    key = (m(key_v), f"Correct. {m(p['ta'])} − {m(exp)} expired insurance − {m(p['dep'])} depreciation + {m(p['cb'])} credit balances reclassified + {m(intr)} interest receivable.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year 1, balance sheet reports total assets of {m(p['ta'])}. The controller identifies these errors, none of which has been corrected: (1) on October 1, {s} paid {m(p['prem'])} for a one-year insurance policy and debited prepaid insurance, and no insurance expense has been recorded; (2) Year 1 depreciation of {m(p['dep'])} on a delivery van bought in March was not recorded; (3) accounts receivable are reported net of {m(p['cb'])} of customer credit balances arising from overpayments; (4) a cash dividend of {m(p['div'])}, declared on December 18 and payable January 12, Year 2, was not recorded; and (5) no interest has been accrued on a {m(p['note'])}, {p['rate']}% note receivable that {s} accepted from a customer on September 1, Year 1, with principal and interest due August 31, Year 2. What total assets should {s}'s corrected balance sheet report?""",
        choices, ans,
        f"""(1) Three of the policy's twelve months have expired: prepaid insurance falls by {m(p['prem'])} × 3/12 = {m(exp)}. (2) Depreciation reduces the van's carrying amount by {m(p['dep'])}. (3) Customer credit balances are liabilities, not reductions of receivables, so receivables increase by {m(p['cb'])}. (4) The declared dividend is a liability and a reduction of retained earnings; total assets don't change. (5) Interest receivable for September–December: {m(p['note'])} × {p['rate']}% × 4/12 = {m(intr)}. Total assets = {m(p['ta'])} − {m(exp)} − {m(p['dep'])} + {m(p['cb'])} + {m(intr)} = {m(key_v)}.""",
    )


def income_statement_adjust(p):
    co, s = p["co"], short(p["co"])
    dep = whole(D(p["E"]) / 5 * 6 / 12)
    key_v = p["draft"] + p["E"] - dep - p["W"] - p["L"] - (p["G"] - p["Gc"])
    pool = {
        "dep_full": (m(key_v - dep), f"Takes a full year of depreciation ({m(2 * dep)}). Equipment placed in service on July 1 is depreciated for six months."),
        "no_dep": (m(key_v + dep), f"Capitalizes the equipment but records no depreciation on it. Six months of depreciation ({m(dep)}) belong in Year 2."),
        "rev_only": (m(key_v - p["Gc"]), f"Reverses the {m(p['G'])} sale but leaves its {m(p['Gc'])} cost in cost of goods sold. Under FOB destination the goods were still {s}'s inventory at year-end, so their cost comes out of cost of goods sold too."),
        "no_loss": (m(key_v + p["L"]), f"Leaves the {m(p['L'])} loss in retained earnings. A loss on selling a warehouse is part of income; only prior-period error corrections go directly to retained earnings."),
        "no_warr": (m(key_v + p["W"]), f"Records warranty expense only when claims are paid. The {m(p['W'])} estimated cost of assurance-type warranties on Year 2 sales is accrued in Year 2."),
    }
    key = (m(key_v), f"Correct. {m(p['draft'])} + {m(p['E'])} − {m(dep)} depreciation − {m(p['W'])} warranty − {m(p['L'])} loss − ({m(p['G'])} − {m(p['Gc'])}) on the sale reversed.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 income statement reports income before income taxes of {m(p['draft'])}. The controller identifies these errors: (1) equipment costing {m(p['E'])}, bought and placed in service on July 1, Year 2, was charged to repairs and maintenance expense; it has a five-year life and no residual value, and {s} depreciates equipment straight-line from the month it is placed in service; (2) no warranty expense was recorded for the assurance-type warranties on Year 2 sales, whose estimated future repair cost is {m(p['W'])}, and no claims were paid in Year 2; (3) a {m(p['L'])} loss on the sale of a warehouse in Year 2 was debited directly to retained earnings; and (4) sales include {m(p['G'])} for goods shipped on December 30 under FOB destination terms and received by the customer on January 4, Year 3, and their {m(p['Gc'])} cost was charged to cost of goods sold. Ignoring income taxes, what is {s}'s corrected income before income taxes?""",
        choices, ans,
        f"""(1) The equipment is capitalized, which removes {m(p['E'])} of expense, and depreciated for six months: {m(p['E'])} ÷ 5 × 6/12 = {m(dep)}. (2) Assurance-type warranty costs are accrued when the goods are sold: − {m(p['W'])}. (3) The loss on the warehouse belongs in income: − {m(p['L'])}. (4) Under FOB destination, control passes when the customer receives the goods, in Year 3, so the {m(p['G'])} sale and its {m(p['Gc'])} cost both come out of Year 2: − {m(p['G'] - p['Gc'])}. Corrected income = {m(p['draft'])} + {m(p['E'])} − {m(dep)} − {m(p['W'])} − {m(p['L'])} − {m(p['G'] - p['Gc'])} = {m(key_v)}.""",
    )


def apic_adjust(p):
    co, s = p["co"], short(p["co"])
    issue = p["n"] * (p["price"] - p["par"])
    lsd = p["sd"] * (p["fv"] - p["par"])
    assert p["Def"] < p["G"]
    key_v = p["X"] + issue - lsd + p["G"] - p["Def"]
    pool = {
        "no_issue": (m(key_v - issue), f"Leaves the whole issuance in common stock. Only par value ({m(p['n'] * p['par'])}) belongs there; the {m(issue)} received above par is additional paid-in capital."),
        "lsd_fv": (m(key_v + lsd), f"Keeps the stock dividend at market price. For a dividend this large (30%), {s} capitalizes only the par value that state law requires, so the {m(lsd)} credited to APIC is reversed."),
        "gain_left": (m(key_v - p["G"]), f"Leaves the {m(p['G'])} excess on reissuing treasury shares in income. A company doesn't report gains on its own shares; the excess is paid-in capital from treasury stock."),
        "def_re": (m(key_v + p["Def"]), f"Leaves the {m(p['Def'])} shortfall in retained earnings. Under the cost method a shortfall is charged first to paid-in capital from treasury stock, which the March reissuance had credited with {m(p['G'])}."),
    }
    key = (m(key_v), f"Correct. {m(p['X'])} + {m(issue)} − {m(lsd)} + {m(p['G'])} − {m(p['Def'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 statement of changes in equity reports additional paid-in capital of {m(p['X'])} at December 31. The controller identifies these errors: (1) in February, {s} issued {p['n']:,} shares of ${p['par']} par common stock for ${p['price']} per share and credited the entire proceeds to common stock; (2) in March, {s} reissued treasury shares, which it carries at cost, for {m(p['G'])} more than their cost and credited the excess to a gain in net income; (3) in May, {s} distributed a 30% stock dividend of {p['sd']:,} shares when the market price was ${p['fv']} per share and recorded it at the market price, although state law requires only par value to be capitalized for a stock dividend of that size; and (4) in November, it reissued other treasury shares for {m(p['Def'])} less than their cost and charged the shortfall to retained earnings. Before Year 2, {s} had no paid-in capital from treasury stock transactions. What additional paid-in capital should the corrected statement report at December 31, Year 2?""",
        choices, ans,
        f"""(1) The excess over par on the share issuance is APIC: {p['n']:,} × (${p['price']} − ${p['par']}) = {m(issue)}. (2) The {m(p['G'])} excess on the March reissuance is paid-in capital from treasury stock, not a gain. (3) A 30% stock dividend is a large stock dividend; with state law requiring only par, {s} transfers par value from retained earnings to common stock, so the draft's {p['sd']:,} × (${p['fv']} − ${p['par']}) = {m(lsd)} credit to APIC is reversed. (4) The November shortfall of {m(p['Def'])} is charged against that {m(p['G'])} balance before any is charged to retained earnings, so it reduces APIC. APIC = {m(p['X'])} + {m(issue)} − {m(lsd)} + {m(p['G'])} − {m(p['Def'])} = {m(key_v)}.""",
    )


def scf_financing_adjust(p):
    co, s = p["co"], short(p["co"])
    X = p["lb"] - p["rp"] - p["dd"] - p["i"] + p["c"]
    key_v = X + p["du"] + p["i"] - p["t"] - p["c"]
    assert key_v > 0
    pool = {
        "div_full": (m(key_v - p["du"]), f"Keeps dividends declared as the outflow. Dividends payable rose by {m(p['du'])}, so cash paid was {m(p['dd'] - p['du'])}."),
        "div_sign": (m(key_v - 2 * p["du"]), f"Adds the {m(p['du'])} increase in dividends payable to dividends declared. An increase in the payable means less was paid than declared."),
        "int_fin": (m(key_v - p["i"]), f"Leaves the {m(p['i'])} of interest paid in financing activities. Under U.S. GAAP, interest paid is an operating cash flow."),
        "no_treasury": (m(key_v + p["t"]), f"Leaves the {m(p['t'])} treasury share purchase out of financing activities. Buying back the company's own shares is a financing outflow."),
        "keep_conv": (m(key_v + p["c"]), "Keeps the bond conversion as a cash inflow. Converting bonds into shares involves no cash; it is disclosed as a noncash financing activity."),
    }
    key =(m(key_v), f"Correct. {m(p['lb'])} borrowed − {m(p['rp'])} repaid − {m(p['dd'] - p['du'])} dividends paid − {m(p['t'])} treasury shares.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 statement of cash flows reports net cash provided by financing activities of {m(X)}: proceeds from long-term borrowing {m(p['lb'])}; repayment of long-term debt ({m(p['rp'])}); dividends paid ({m(p['dd'])}); interest paid ({m(p['i'])}); and common stock issued on conversion of bonds {m(p['c'])}. The controller identifies these errors: the dividends line shows the {m(p['dd'])} of dividends declared in Year 2, although dividends payable increased by {m(p['du'])} during the year; interest paid is reported in financing activities; the conversion, in which bondholders exchanged bonds with a carrying amount of {m(p['c'])} for common shares, is reported as a cash inflow; and {m(p['t'])} paid to buy treasury shares is reported in investing activities. {s} follows U.S. GAAP. What net cash provided by financing activities should the corrected statement report?""",
        choices, ans,
        f"""Dividends paid = {m(p['dd'])} declared − {m(p['du'])} increase in dividends payable = {m(p['dd'] - p['du'])}. Interest paid moves to operating activities. The conversion is a noncash financing activity, disclosed rather than reported as a cash flow. The treasury share purchase is a financing outflow. Net cash provided by financing activities = {m(p['lb'])} − {m(p['rp'])} − {m(p['dd'] - p['du'])} − {m(p['t'])} = {m(key_v)}.""",
    )


def notes_debt_maturities(p):
    co, s = p["co"], short(p["co"])
    inst = whole(D(p["t"]) / 5)
    key_v = p["X"] - p["ol"] + inst + p["np"] - p["intr"]
    pool = {
        "full_loan": (m(key_v + p["t"] - inst), f"Adds the whole {m(p['t'])} term loan to Year 2. Only the first of its five annual installments ({m(inst)}) matures in Year 2."),
        "keep_ol": (m(key_v + p["ol"]), f"Leaves the {m(p['ol'])} of operating lease payments in the debt maturities. Lease payments are disclosed in the lease note's maturity analysis, not as debt principal."),
        "keep_int": (m(key_v + p["intr"]), f"Leaves the {m(p['intr'])} of interest in the amount. The maturities disclosure shows principal only."),
        "no_np": (m(key_v - p["np"]), f"Keeps the {m(p['np'])} note under Year 3. It is due June 30, Year 2; an intention to refinance doesn't change its contractual maturity."),
        "no_loan": (m(key_v - inst), f"Leaves out the new term loan. Its first {m(inst)} installment is due December 1, Year 2."),
    }
    key = (m(key_v), f"Correct. {m(p['X'])} − {m(p['ol'])} − {m(p['intr'])} + {m(inst)} + {m(p['np'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft note on long-term debt at December 31, Year 1, reports principal maturities of {m(p['X'])} for Year 2. The controller identifies these errors and omissions in that amount: it includes {m(p['ol'])} of payments due in Year 2 under {s}'s operating leases; it omits a {m(p['t'])} term loan signed on December 1, Year 1, which is repayable in five equal annual principal installments beginning December 1, Year 2; it leaves out a {m(p['np'])} note payable due June 30, Year 2, which the draft lists under Year 3 because {s} intends to refinance it, and it includes {m(p['intr'])} of interest that {s} will pay on its debt in Year 2. What principal amount should the corrected note report as maturing in Year 2?""",
        choices, ans,
        f"""The debt note discloses the principal amounts maturing in each of the next five years. Remove the {m(p['ol'])} of operating lease payments, which belong in the lease note's maturity analysis, and the {m(p['intr'])} of interest. Add the first installment of the new term loan, {m(p['t'])} ÷ 5 = {m(inst)}, and the {m(p['np'])} note, which matures on June 30, Year 2, whatever {s} intends. {m(p['X'])} − {m(p['ol'])} − {m(p['intr'])} + {m(inst)} + {m(p['np'])} = {m(key_v)}.""",
    )


def nfp_activities_adjust(p):
    org, s = p["org"], short(p["org"])
    key_v = p["X"] - p["e"] + p["sch"] - p["u"]
    assert key_v > 0 and p["X"] - p["e"] - p["u"] > 0
    pool = {
        "keep_e": (m(key_v + p["e"]), f"Leaves the {m(p['e'])} of endowment return in net assets without donor restrictions. Return on a donor-restricted endowment is reported with donor restrictions until it is appropriated for spending."),
        "no_release": (m(key_v - p["sch"]), f"Records no release for the {m(p['sch'])} of scholarships. The expense is reported in net assets without donor restrictions, and meeting the donor's purpose releases the same amount from net assets with donor restrictions."),
        "event": (m(key_v - p["dir"]), f"Subtracts the {m(p['dir'])} cost of the dinners again. Reporting the gala gross raises revenue and expense by the same amount, so the change in net assets doesn't change."),
        "no_loss": (m(key_v + p["u"]), f"Leaves out the {m(p['u'])} unrealized loss. Investment return, including unrealized losses on investments without donor restrictions, is reported in the statement of activities."),
    }
    key = (m(key_v), f"Correct. {m(p['X'])} − {m(p['e'])} endowment return + {m(p['sch'])} release − {m(p['u'])} unrealized loss.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, reports an increase in net assets without donor restrictions of {m(p['X'])} in its draft Year 1 statement of activities. The controller identifies these errors: (1) investment return of {m(p['e'])} on a donor-restricted endowment, whose donor requires the return to be spent on scholarships, is reported as revenue without donor restrictions, and none of the return has been appropriated for spending; (2) scholarships of {m(p['sch'])} paid from donor-restricted scholarship gifts received in earlier years are reported as expenses, but no release from restrictions was recorded; (3) revenue from the annual gala is reported as {m(p['gross'] - p['dir'])}, net of the {m(p['dir'])} cost of the dinners served to attendees, instead of reporting the {m(p['gross'])} gross and the cost of direct benefits to donors separately; and (4) a {m(p['u'])} unrealized loss on investments without donor restrictions was not recorded. What increase in net assets without donor restrictions should {s}'s corrected statement of activities report?""",
        choices, ans,
        f"""(1) Return on a donor-restricted endowment stays in net assets with donor restrictions until appropriated: − {m(p['e'])}. (2) The scholarships are expenses of net assets without donor restrictions, and spending on the donor's purpose releases {m(p['sch'])} into that class: + {m(p['sch'])}. (3) Presenting the gala gross adds {m(p['dir'])} to both revenue and expenses, with no effect on the change in net assets. (4) The unrealized loss is investment return without donor restrictions: − {m(p['u'])}. {m(p['X'])} − {m(p['e'])} + {m(p['sch'])} − {m(p['u'])} = {m(key_v)}.""",
    )


def tax_basis(p):
    co, s = p["co"], short(p["co"])
    key_v = p["X"] + p["dg"] - p["dt"] + p["r"] + p["w"] - p["wp"] + p["b"] - p["bw"]
    assert p["dt"] > p["dg"] and p["w"] > p["wp"] and p["b"] > p["bw"]
    pool = {
        "no_rent": (m(key_v - p["r"]), f"Keeps the GAAP deferral of the {m(p['r'])} of rent collected in advance. For tax, rent received in advance is income when received."),
        "rent_sign": (m(key_v - 2 * p["r"]), f"Subtracts the {m(p['r'])} of advance rent instead of adding it. GAAP deferred it; the tax basis recognizes it when received, which raises income."),
        "dep_gaap": (m(key_v + p["dt"] - p["dg"]), f"Keeps GAAP depreciation ({m(p['dg'])}). Tax basis statements use the {m(p['dt'])} of depreciation on the tax return."),
        "warr_gaap": (m(key_v - (p["w"] - p["wp"])), f"Keeps the {m(p['w'])} GAAP warranty accrual. For tax, warranty costs are deducted when paid ({m(p['wp'])})."),
        "bad_gaap": (m(key_v - (p["b"] - p["bw"])), f"Keeps the {m(p['b'])} GAAP credit loss expense. For tax, bad debts are deducted when specific accounts are written off ({m(p['bw'])})."),
    }
    key = (m(key_v), f"Correct. {m(p['X'])} + {m(p['dg'])} − {m(p['dt'])} + {m(p['r'])} + {m(p['w'])} − {m(p['wp'])} + {m(p['b'])} − {m(p['bw'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a limited liability company taxed as a partnership that uses the accrual method for tax, issues financial statements prepared on the income tax basis of accounting. Its Year 2 net income under U.S. GAAP is {m(p['X'])}. GAAP and tax amounts differ only for these items: depreciation is {m(p['dg'])} under GAAP and {m(p['dt'])} on the tax return; {m(p['r'])} of rent that {s} collected from a subtenant in December for the first half of Year 3 is deferred under GAAP; warranty expense accrued under GAAP is {m(p['w'])}, while warranty repairs paid in Year 2 total {m(p['wp'])}; and credit loss expense under GAAP is {m(p['b'])}, while accounts written off as worthless in Year 2 total {m(p['bw'])}. What net income should {s}'s Year 2 statement of revenues and expenses—income tax basis report?""",
        choices, ans,
        f"""Income tax basis statements recognize revenues and expenses as the tax return does. Starting from GAAP net income of {m(p['X'])}: replace GAAP depreciation with tax depreciation (+ {m(p['dg'])} − {m(p['dt'])}); include the {m(p['r'])} of advance rent, taxable when received; replace the warranty accrual with warranty costs paid (+ {m(p['w'])} − {m(p['wp'])}); and replace credit loss expense with specific write-offs (+ {m(p['b'])} − {m(p['bw'])}). Tax basis net income = {m(key_v)}.""",
    )


def fx_transactions(p):
    co, s = p["co"], short(p["co"])
    s0, sd, s1, c0, c1 = (D(p[k]) for k in ("s0", "sd", "s1", "c0", "c1"))
    gain_r = whole(p["A"] * (s1 - s0))
    loss_p = whole(p["B"] * (c1 - c0))
    rem_pp = whole(p["P"] * (s1 - sd))
    assert gain_r > 0 and loss_p > 0 and rem_pp != 0
    key_v = gain_r - loss_p
    pool = {
        "prepaid": (gl(key_v + rem_pp), f"Also remeasures the CHF {p['P']:,} advance to the supplier. A nonrefundable advance for goods is a nonmonetary asset, carried at the historical rate, so it produces no exchange gain or loss."),
        "defer": (gl(-loss_p), f"Recognizes only the realized {m(loss_p)} loss on the payable settled in December. The {m(gain_r)} gain on the receivable still outstanding at year-end is recognized in Year 1 income too."),
        "loss_sign": (gl(gain_r + loss_p), f"Treats the {m(loss_p)} on the Canadian payable as a gain. The Canadian dollar strengthened before {s} paid, so settling the payable cost more dollars: a loss."),
        "no_realized": (gl(gain_r), f"Leaves out the {m(loss_p)} loss on the payable because it was settled within the year. A realized exchange loss on settlement is a transaction loss in income."),
    }
    key = (gl(key_v), f"Correct. {m(gain_r)} gain on the receivable − {m(loss_p)} loss on the payable.")
    choices, ans = build(pool, key, p["use"], positive=False)
    return variant(
        f"""{co}, whose functional currency is the U.S. dollar, has three Year 1 transactions denominated in foreign currencies. On October 1, it sold goods to a Swiss customer for {p['A']:,} Swiss francs (CHF), due February 15, Year 2. On November 1, it bought equipment from a Canadian supplier for {p['B']:,} Canadian dollars (CAD) and paid the invoice on December 15. On December 1, it paid a Swiss supplier a nonrefundable advance of CHF {p['P']:,} for goods to be delivered in March, Year 2. The dollar value of one Swiss franc was ${p['s0']} on October 1, ${p['sd']} on December 1 and ${p['s1']} on December 31; one Canadian dollar was worth ${p['c0']} on November 1 and ${p['c1']} on December 15. What net foreign currency transaction gain or loss should {s} report in its Year 1 income statement?""",
        choices, ans,
        f"""Monetary items denominated in a foreign currency are remeasured at the current rate, and the change goes to income. The CHF receivable: {p['A']:,} × (${p['s1']} − ${p['s0']}) = {m(gain_r)} gain. The CAD payable, settled December 15: {p['B']:,} × (${p['c1']} − ${p['c0']}) = {m(loss_p)} more dollars paid, a loss. The equipment and the advance to the supplier are nonmonetary and stay at their historical rates. Net = {m(gain_r)} − {m(loss_p)} = {gl(key_v)}.""",
    )


def held_for_sale(p):
    co, s = p["co"], short(p["co"])
    key_v = p["a"] + p["e"]
    pool = {
        "excl_e": (m(key_v - p["e"]), f"Leaves out the headquarters building because {s} still occupies it. Staying only until a closing and then moving out within the usual time doesn't stop the building from being available for immediate sale."),
        "incl_b": (m(key_v + p["b"]), f"Includes the delivery trucks. {s} will keep using them until June and hasn't listed them, so they aren't available for immediate sale and aren't being marketed."),
        "incl_c": (m(key_v + p["c"]), f"Includes the office building. An asking price 40% above fair value, unchanged despite no offers, isn't a price reasonable in relation to fair value, so a sale within a year isn't probable."),
        "incl_d": (m(key_v + p["d"]), f"Includes the packaging equipment. Its plan was approved and marketing began on January 15, Year 2; when the criteria are first met after the balance sheet date, the asset stays held and used at December 31."),
    }
    key = (m(key_v), f"Correct. Warehouse {m(p['a'])} + headquarters building {m(p['e'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} is preparing its December 31, Year 1, balance sheet, which will be issued on March 1, Year 2. Each asset below has a fair value less cost to sell above its carrying amount. (1) A warehouse, carrying amount {m(p['a'])}: in October, management with the authority to do so approved its sale; it is vacant and listed with a broker at a price in line with recent sales of similar warehouses, and a sale is expected by mid-Year 2. (2) Delivery trucks, {m(p['b'])}: management approved their sale in December, but {s} will keep using them until replacement trucks arrive in June, Year 2, and will list them then. (3) An office building, {m(p['c'])}: approved for sale in September and listed since then at a price 40% above its appraised fair value; no offers have been received, and {s} hasn't lowered the price. (4) Packaging equipment, {m(p['d'])}: idle since November; the board approved its sale, and {s} began marketing it at a reasonable price, on January 15, Year 2. (5) {s}'s headquarters building, {m(p['e'])}: approved for sale in November and marketed at a price in line with comparable sales; a buyer's offer was accepted in December and the sale should close in February, Year 2, after which {s} will move to leased offices that are already prepared. The plans are not expected to change. What total carrying amount should {s} report as assets held for sale at December 31, Year 1?""",
        choices, ans,
        f"""An asset is classified as held for sale when management with authority commits to a plan, the asset is available for immediate sale in its present condition (subject only to usual and customary terms), an active program to find a buyer has begun, the sale is probable within one year, the price is reasonable in relation to fair value, and the plan is unlikely to change. The warehouse ({m(p['a'])}) qualifies. So does the headquarters building ({m(p['e'])}): vacating it after closing is a usual and customary term. The trucks are still in use and not marketed; the office building's asking price is unreasonable; and the packaging equipment met the criteria only after year-end, so it is held and used at December 31. Total = {m(key_v)}.""",
    )


def factoring_recourse(p):
    co, s = p["co"], short(p["co"])
    fee = whole(D(p["T"]) * p["f"] / 100)
    hold = whole(D(p["T"]) * p["h"] / 100)
    assert p["mx"] > p["R"]
    key_v = fee + p["R"]
    pool = {
        "secured": ("$0", f"Treats the transfer as a secured borrowing because it is with recourse. Recourse doesn't prevent sale accounting when {s} has surrendered control: the receivables are isolated, the factor may sell or pledge them, and {s} can't reclaim them."),
        "fee_only": (m(fee), f"Records only the {m(fee)} fee. The recourse obligation is a liability {s} takes on in the sale, measured at its {m(p['R'])} fair value, which reduces the proceeds."),
        "max": (m(fee + p["mx"]), f"Measures the recourse obligation at the {m(p['mx'])} maximum. It is measured at its {m(p['R'])} fair value."),
        "holdback": (m(key_v + hold), f"Also treats the {m(hold)} holdback as a loss. The holdback is a receivable from the factor, due to {s} once the accounts are collected; no returns are expected."),
    }
    key = (m(key_v), f"Correct. {m(fee)} fee + {m(p['R'])} recourse obligation.")
    choices, ans = build(pool, key, p["use"], positive=False)
    return variant(
        f"""On {p['date']}, {co} transfers {m(p['T'])} of trade receivables to a factor with recourse: {s} must reimburse the factor for uncollectible accounts, up to {m(p['mx'])}. Legal counsel concludes that the receivables are beyond the reach of {s} and its creditors, even in bankruptcy; the factor may sell or pledge them; and {s} has no right or obligation to buy any of them back. The factor charges a fee of {p['f']}% of the receivables and holds back {p['h']}% of them to cover sales returns, payable to {s} after the accounts are collected; {s} expects no returns. The fair value of the recourse obligation is {m(p['R'])}. What loss should {s} recognize on the transfer?""",
        choices, ans,
        f"""{s} has surrendered control (the receivables are legally isolated, the factor can pledge or sell them, and {s} keeps no effective control), so the transfer is a sale even though it is with recourse. Proceeds are cash of {m(p['T'] - fee - hold)} plus the {m(hold)} receivable from the factor, less the recourse obligation at its {m(p['R'])} fair value. Loss = {m(p['T'])} carrying amount − ({m(p['T'] - fee - hold)} + {m(hold)} − {m(p['R'])}) = {m(fee)} + {m(p['R'])} = {m(key_v)}.""",
    )


def lcm_lifo(p):
    co, s = p["co"], short(p["co"])
    mg = D(p["margin"]) / 100
    rows, key_v, nrv_wd, rc_wd, nofloor_wd, noceil_wd, cases = [], 0, 0, 0, 0, 0, []
    for name, u, cost, rc, sp, cts in p["prods"]:
        cost, rc, sp, cts = D(cost), D(rc), D(sp), D(cts)
        ceil = sp - cts
        floor = ceil - sp * mg
        mkt = min(max(rc, floor), ceil)
        case = "within" if floor <= rc <= ceil else ("above" if rc > ceil else "below")
        cases.append(case)
        wd = lambda mv: whole(u * max(cost - mv, 0))
        key_v += wd(mkt)
        nrv_wd += wd(ceil)
        rc_wd += wd(rc)
        nofloor_wd += wd(min(rc, ceil))
        noceil_wd += wd(max(rc, floor))
        rows.append((name, u, cost, rc, sp, cts, ceil, floor, mkt, case, wd(mkt)))
    assert sorted(cases) == ["above", "below", "within"], cases
    pool = {
        "lcnrv": (m(nrv_wd), f"Applies the lower of cost and net realizable value. {s} uses LIFO, so it applies the lower of cost or market, with replacement cost limited by the ceiling and floor."),
        "rc_only": (m(rc_wd), "Uses replacement cost as market without applying the ceiling (net realizable value) or the floor (net realizable value less a normal profit margin)."),
        "no_floor": (m(nofloor_wd), "Applies the ceiling but not the floor. Market can't be less than net realizable value less a normal profit margin."),
        "no_ceiling": (m(noceil_wd), "Applies the floor but not the ceiling. Market can't exceed net realizable value."),
    }
    key = (m(key_v), "Correct. " + "; ".join(f"{r[0]} {m(r[10])}" for r in rows) + ".")
    choices, ans = build(pool, key, p["use"])
    desc = "; ".join(f"product {r[0]}: {r[1]:,} units, LIFO cost {usd(r[2])}, replacement cost {usd(r[3])}, selling price {usd(r[4])} and cost to complete and sell {usd(r[5])} per unit" for r in rows)
    where = {"within": "between the floor and the ceiling, so market is replacement cost", "above": "above the ceiling, so market is the ceiling", "below": "below the floor, so market is the floor"}
    expl = " ".join(
        f"Product {r[0]}: ceiling {usd(r[4])} − {usd(r[5])} = {usd(r[6])}; floor {usd(r[6])} − {p['margin']}% × {usd(r[4])} = {usd(r[7])}; replacement cost {usd(r[3])} is {where[r[9]]}, {usd(r[8])}"
        + (f"; write-down ({usd(r[2])} − {usd(r[8])}) × {r[1]:,} = {m(r[10])}." if r[10] else f", which is not below cost {usd(r[2])}, so no write-down.")
        for r in rows)
    return variant(
        f"""{co} uses the LIFO method and applies its inventory measurement rule to each product separately. Its normal profit margin is {p['margin']}% of selling price. At December 31, its records show: {desc}. What inventory write-down should {s} recognize at December 31?""",
        choices, ans,
        f"""Inventory measured using LIFO is reported at the lower of cost or market. Market is replacement cost, but not more than net realizable value (the ceiling) or less than net realizable value minus a normal profit margin (the floor). {expl} Total write-down = {m(key_v)}.""",
    )


def zero_coupon_note(p):
    co, s = p["co"], short(p["co"])
    r = D(p["r"]) / 100
    factor = rd(1 / (1 + r) ** 3, "0.0001")
    pv = rd(p["F"] * factor)
    i1 = rd(pv * r)
    i2 = rd((pv + i1) * r)
    for x in (pv * r, (pv + i1) * r, i1 * D(3) / 12, i2 * D(9) / 12, D(p["F"] - pv) / 3):
        assert x % 1 != D("0.5"), "half-dollar step: ambiguous rounding"
    q1, q2 = rd(i1 * D(3) / 12), rd(i2 * D(9) / 12)
    key_v = q1 + q2
    y1 = rd(i1 * D(9) / 12)
    pool = {
        "sl": (m(rd(D(p["F"] - pv) / 3)), f"Spreads the {m(p['F'] - pv)} discount evenly over three years ({m(p['F'] - pv)} ÷ 3 = {m(rd(D(p['F'] - pv) / 3))}, rounded to the nearest dollar). The effective interest method applies the rate to the note's carrying amount, which grows each year."),
        "i1": (m(i1), "Uses the first note year's interest (April, Year 1, to March, Year 2) for the whole calendar year. Nine months of Year 2 fall in the second note year, when the carrying amount is higher."),
        "i2": (m(i2), "Uses the second note year's interest for the whole calendar year. January through March of Year 2 belong to the first note year."),
        "y1": (m(y1), "Reports the interest for Year 1 (April through December). The question asks for Year 2."),
        "face": (m(rd(p["F"] * r)), f"Applies the {p['r']}% rate to the {m(p['F'])} face amount. Interest is the rate times the note's carrying amount, which starts at its present value."),
    }
    key = (m(key_v), f"Correct. 3/12 × {m(i1)} + 9/12 × {m(i2)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On April 1, Year 1, {co} acquires a machine by issuing a {m(p['F'])} note that bears no stated interest and is due in full on March 31, Year 4. The machine has no reliably determinable cash price, the note has no market value, and {s}'s incremental borrowing rate for a similar note is {p['r']}%, compounded annually. The present value of 1 for three periods at {p['r']}% is {factor}. {s} uses the effective interest method, computes interest for each year of the note's term, accrues it evenly within that year, and rounds to the nearest dollar at each step. What interest expense on the note should {s} report for the calendar year Year 2?""",
        choices, ans,
        f"""With no stated interest and no reliable cash price, the note is recorded at its present value at the imputed {p['r']}% rate: {m(p['F'])} × {factor} = {m(pv)}. Interest for the first note year (to March 31, Year 2) = {m(pv)} × {p['r']}% = {m(i1)}; for the second note year = ({m(pv)} + {m(i1)}) × {p['r']}% = {m(i2)}. Year 2 includes three months of the first note year and nine of the second: {m(i1)} × 3/12 = {m(q1)}, plus {m(i2)} × 9/12 = {m(q2)}, for {m(key_v)}.""",
    )


def equity_discrepancies(p):
    co, s = p["co"], short(p["co"])
    X = p["B"] + p["ni"] + p["o"] + p["u"] - p["dc"] - p["ca"] - p["tp"] - p["tr"]
    gain = p["fv"] - p["ca"]
    key_v = X - p["u"] - gain + p["tr"] + p["bc"]
    assert p["fvs"] > p["bc"]
    pool = {
        "keep_u": (m(key_v + p["u"]), f"Keeps the {m(p['u'])} of trading-security gains in other comprehensive income. They are already in net income, so the draft counts them twice."),
        "prop_ca": (m(key_v + gain), f"Leaves the property dividend at the land's {m(p['ca'])} carrying amount. Net income already includes the {m(gain)} remeasurement gain, so the dividend is recorded at the {m(p['fv'])} fair value."),
        "tr_keep": (m(key_v - p["tr"]), f"Keeps the {m(p['tr'])} retirement as a reduction of equity. The treasury shares reduced equity when they were bought in Year 1; retiring them only reclassifies amounts within equity."),
        "no_conv": (m(key_v - p["bc"]), f"Leaves out the conversion. Equity increases by the {m(p['bc'])} carrying amount of the bonds converted."),
        "conv_fv": (m(key_v + p["fvs"] - p["bc"]), f"Records the conversion at the shares' {m(p['fvs'])} market value. A conversion under the bonds' original terms is recorded at the bonds' {m(p['bc'])} carrying amount, with no gain or loss."),
    }
    key = (m(key_v), f"Correct. {m(X)} − {m(p['u'])} − {m(gain)} + {m(p['tr'])} + {m(p['bc'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 statement of changes in equity reports total stockholders' equity of {m(X)} at December 31, built up as follows: January 1 balance {m(p['B'])}; net income {m(p['ni'])}; other comprehensive income {m(p['o'] + p['u'])}, made up of {m(p['o'])} of unrealized holding gains on available-for-sale debt securities and {m(p['u'])} of unrealized holding gains on trading debt securities; cash dividends ({m(p['dc'])}); property dividend ({m(p['ca'])}); purchase of treasury stock ({m(p['tp'])}); and retirement of treasury stock ({m(p['tr'])}). Supporting documents show: net income includes all of the year's fair value changes on the trading securities; the property dividend distributed land with a carrying amount of {m(p['ca'])} and a fair value of {m(p['fv'])} on the declaration date, and net income includes the {m(gain)} gain from remeasuring the land to fair value; the treasury shares retired in June had been bought in Year 1 for {m(p['tr'])}; and in September, bondholders converted bonds with a carrying amount of {m(p['bc'])} into common shares, then worth {m(p['fvs'])}, under the bonds' original conversion terms. What total stockholders' equity should {s}'s corrected statement report at December 31, Year 2?""",
        choices, ans,
        f"""The trading-security gains are in net income, so the {m(p['u'])} in other comprehensive income is a double count: − {m(p['u'])}. A property dividend is recorded at the property's fair value; with the {m(gain)} gain already in net income, the dividend should be {m(p['fv'])}, not {m(p['ca'])}: − {m(gain)}. Retiring treasury shares that were deducted from equity when bought doesn't change total equity, so the draft's deduction is reversed: + {m(p['tr'])}. The conversion adds the bonds' {m(p['bc'])} carrying amount to equity. The cash dividends and the Year 2 treasury purchase are correct. {m(X)} − {m(p['u'])} − {m(gain)} + {m(p['tr'])} + {m(p['bc'])} = {m(key_v)}.""",
    )


def scf_operating_discrepancies(p):
    co, s = p["co"], short(p["co"])
    X = p["ni"] + p["dep"] + p["pm"] - p["pp"] - p["ar"] + p["ap"] + p["dp"]
    undist = p["ei"] - p["dv"]
    assert undist > 0
    key_v = X - 2 * p["pm"] + 2 * p["pp"] - p["dp"] - undist
    pool = {
        "prem_once": (m(key_v + p["pm"]), f"Removes the {m(p['pm'])} of premium amortization but doesn't subtract it. Amortizing a premium makes interest expense smaller than the interest paid, so it is deducted from net income."),
        "eq_full": (m(key_v - p["dv"]), f"Subtracts the whole {m(p['ei'])} of equity in earnings. The {m(p['dv'])} of dividends received is an operating inflow, so only the {m(undist)} of undistributed earnings is deducted."),
        "no_eq": (m(key_v + undist), f"Makes no adjustment for the equity method income. The {m(undist)} of earnings not received in cash is deducted from net income."),
        "prepaid_once": (m(key_v - p["pp"]), f"Removes the {m(p['pp'])} decrease in prepaid expenses but doesn't add it. A decrease in prepaid expenses is added to net income."),
        "keep_dp": (m(key_v + p["dp"]), f"Keeps the {m(p['dp'])} increase in dividends payable. Dividends are a financing activity, so changes in dividends payable don't belong in operating activities."),
    }
    key = (m(key_v), f"Correct. {m(X)} − 2 × {m(p['pm'])} + 2 × {m(p['pp'])} − {m(p['dp'])} − {m(undist)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s staff accountant prepared this draft operating section of the Year 2 statement of cash flows under the indirect method: net income {m(p['ni'])}; depreciation {m(p['dep'])}; amortization of premium on bonds payable {m(p['pm'])}; decrease in prepaid expenses ({m(p['pp'])}); increase in accounts receivable ({m(p['ar'])}); increase in accounts payable {m(p['ap'])}; increase in dividends payable {m(p['dp'])}; net cash provided by operating activities {m(X)}. Net income includes {m(p['ei'])} of equity in the earnings of a 30%-owned investee accounted for by the equity method, which paid {s} cash dividends of {m(p['dv'])} during Year 2; {s} classifies distributions from equity method investees using the cumulative earnings approach, and its cumulative distributions received have not exceeded its cumulative equity in earnings. After correcting the draft to comply with U.S. GAAP, what is {s}'s net cash provided by operating activities?""",
        choices, ans,
        f"""Premium amortization reduces interest expense below the cash paid, so it is subtracted, not added: − 2 × {m(p['pm'])}. A decrease in prepaid expenses is added, not subtracted: + 2 × {m(p['pp'])}. Dividends payable relates to a financing activity: − {m(p['dp'])}. Equity in earnings is noncash except for the dividends received, which are a return on the investment (operating) under the cumulative earnings approach: − ({m(p['ei'])} − {m(p['dv'])}) = − {m(undist)}. {m(X)} − {m(2 * p['pm'])} + {m(2 * p['pp'])} − {m(p['dp'])} − {m(undist)} = {m(key_v)}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def bank_reconciliation(p):
    co, s = p["co"], short(p["co"])
    oc = p["ocl"] - p["cert"] - p["hu"]
    key_v = p["bk"] + p["dit"] - oc
    G = key_v - p["hu"] + p["lp"] - p["intr"]
    pool = {
        "keep_cert": (m(key_v - p["cert"]), f"Deducts the {m(p['cert'])} certified check as outstanding. The bank deducted it from {s}'s account when it certified the check, so the bank balance already reflects it."),
        "keep_held": (m(key_v - p["hu"]), f"Treats the unmailed {m(p['hu'])} check as outstanding. A check still in {s}'s hands at year-end hasn't been paid out; the book entry is reversed and the check isn't outstanding."),
        "no_int": (m(key_v - p["intr"]), f"Leaves out the {m(p['intr'])} dividend the bank received for {s}. It is cash {s} hasn't recorded yet, so it is added to the book balance."),
        "no_loan": (m(key_v + p["lp"]), f"Leaves out the {m(p['lp'])} loan payment the bank deducted. {s} records it, reducing its book balance."),
    }
    key = (m(key_v), f"Correct. Bank {m(p['bk'])} + {m(p['dit'])} − {m(oc)} outstanding checks = book {m(G)} + {m(p['hu'])} − {m(p['lp'])} + {m(p['intr'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31 bank statement shows a balance of {m(p['bk'])}, and its general ledger cash account shows {m(G)}. The bookkeeper's reconciliation lists deposits in transit of {m(p['dit'])} and outstanding checks of {m(p['ocl'])}. Further work finds: the outstanding check list includes a {m(p['cert'])} check that the bank certified for a supplier on December 22 at {s}'s request; the list also includes check no. {p['chk']}, for {m(p['hu'])}, which was written and recorded on December 30 but was still in the controller's desk, unmailed, on January 6; on December 31 the bank deducted a {m(p['lp'])} loan payment, which {s} hasn't recorded; and the bank credited {s}'s account with a {m(p['intr'])} dividend wired by a company whose shares {s} holds, which {s} hasn't recorded. What cash balance should {s} report at December 31?""",
        choices, ans,
        f"""Bank side: the certified check was deducted by the bank when certified, and the unmailed check hasn't been issued, so true outstanding checks are {m(p['ocl'])} − {m(p['cert'])} − {m(p['hu'])} = {m(oc)}. Correct balance = {m(p['bk'])} + {m(p['dit'])} − {m(oc)} = {m(key_v)}. Book side: {m(G)} + {m(p['hu'])} unmailed check restored − {m(p['lp'])} loan payment + {m(p['intr'])} dividend received = {m(key_v)}. The two sides agree.""",
    )


def ar_rollforward(p):
    co, s = p["co"], short(p["co"])
    X = p["beg"] + p["sales"] - p["end"]
    key_v = p["beg"] + p["sales"] - p["cs"] - p["r"] - p["dc"] - p["w"] - p["n"] - p["end"]
    dal = p["ale"] - p["alb"]
    pool = {
        "no_note": (m(key_v + p["n"]), f"Treats the {m(p['n'])} account converted into a note as collected. The note replaced the account receivable; no cash was received."),
        "no_wo": (m(key_v + p["w"]), f"Ignores the {m(p['w'])} of write-offs. Accounts written off leave receivables without any cash being collected."),
        "cash_in": (m(key_v + p["cs"]), f"Leaves the {m(p['cs'])} of cash sales in the rollforward. Cash sales never pass through accounts receivable."),
        "no_disc": (m(key_v + p["dc"]), f"Ignores the {m(p['dc'])} of sales discounts. Discounts taken reduce receivables without any cash being collected."),
        "allow": (m(key_v - dal), f"Also subtracts the {m(dal)} increase in the allowance for credit losses. The rollforward is of gross receivables; the allowance doesn't affect them."),
    }
    key = (m(key_v), f"Correct. {m(p['beg'])} + ({m(p['sales'])} − {m(p['cs'])}) − {m(p['r'])} − {m(p['dc'])} − {m(p['w'])} − {m(p['n'])} − {m(p['end'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s staff accountant computed Year 2 cash collected on accounts receivable as {m(X)}: beginning receivables of {m(p['beg'])}, plus gross sales of {m(p['sales'])}, less ending receivables of {m(p['end'])}, per the aged subledger, which agrees with the general ledger. Supporting records show: gross sales include {m(p['cs'])} of cash sales; customers returned goods from credit sales for credits of {m(p['r'])}; customers who paid within the discount period took {m(p['dc'])} of sales discounts; {m(p['w'])} of accounts were written off; in October, a customer's past-due account of {m(p['n'])} was converted into a 12-month interest-bearing note receivable; and the allowance for credit losses increased from {m(p['alb'])} to {m(p['ale'])}. What cash did {s} collect on accounts receivable in Year 2?""",
        choices, ans,
        f"""Receivables rollforward: beginning {m(p['beg'])} + credit sales ({m(p['sales'])} − {m(p['cs'])} cash sales = {m(p['sales'] - p['cs'])}) − returns {m(p['r'])} − discounts {m(p['dc'])} − write-offs {m(p['w'])} − account converted to a note {m(p['n'])} − collections = ending {m(p['end'])}. Collections = {m(key_v)}. The allowance is a separate contra account and doesn't enter the rollforward of gross receivables.""",
    )


def ar_reconciliation(p):
    co, s = p["co"], short(p["co"])
    C = p["C"]
    S = C - p["mm"]
    G = C + p["u"] + p["wo"]
    pool = {
        "sub": (m(S), f"Uses the subledger as recorded. The {m(p['mm'])} credit memo was posted twice, so the subledger is understated by that amount."),
        "memo_twice": (m(C - 2 * p["mm"]), f"Subtracts the duplicated {m(p['mm'])} credit memo from the subledger again instead of adding it back."),
        "gl_wo": (m(C + p["wo"]), f"Doesn't post the {m(p['wo'])} write-off to the control account. The account was written off, so it comes out of the general ledger too."),
        "foot_sign": (m(C + 2 * p["u"]), f"Adds the {m(p['u'])} underfooting to the control account. Underfooting the receipts column credited receivables too little, so the control account is too high."),
        "misposted": (m(C - p["mp"]), f"Subtracts the {m(p['mp'])} misposted payment. Posting a payment to the wrong customer's account doesn't change the subledger total; it is corrected between the two accounts."),
    }
    key = (m(C), f"Correct. Subledger {m(S)} + {m(p['mm'])} = control account {m(G)} − {m(p['u'])} − {m(p['wo'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s accounts receivable subledger totals {m(S)}, and the general ledger control account shows {m(G)}. The controller's investigation finds: a {m(p['mm'])} credit memo for a customer's returned goods was posted to that customer's subledger account twice; the accounts receivable column of the December cash receipts journal was underfooted by {m(p['u'])} before the total was posted to the control account; a {m(p['wo'])} customer account written off in December was removed from the subledger, but the write-off was never posted to the general ledger; and a {m(p['mp'])} payment from one customer was posted to another customer's subledger account. Before any allowance for credit losses, what amount should {s} report as accounts receivable?""",
        choices, ans,
        f"""Subledger: {m(S)} + {m(p['mm'])} duplicated credit memo reversed = {m(C)}. The misposted payment moves between two customer accounts and doesn't change the total. Control account: {m(G)} − {m(p['u'])} for the underfooted receipts (receivables were credited too little) − {m(p['wo'])} write-off not yet posted = {m(C)}. The records agree at {m(C)}.""",
    )


def inventory_rollforward(p):
    co, s = p["co"], short(p["co"])
    end_inv = p["E"] - p["cn"]
    fin = p["F"] - p["fo"]
    key_v = p["B"] + p["P"] - p["dsc"] + fin - p["fi"] - end_inv
    pool = {
        "keep_cons": (m(key_v - p["cn"]), f"Leaves the {m(p['cn'])} of consigned goods in ending inventory. They belong to the supplier, so they come out of the count; since they were never recorded as a purchase, nothing else changes."),
        "freight_all": (m(key_v - fin), f"Treats all freight as a selling expense. The {m(fin)} paid to bring goods in is part of inventory cost; only the {m(p['fo'])} of delivery freight is a selling expense."),
        "fire_in": (m(key_v + p["fi"]), f"Leaves the {m(p['fi'])} of goods destroyed by fire in cost of goods sold. {s} reports casualty losses separately."),
        "fo_in": (m(key_v + p["fo"]), f"Includes the {m(p['fo'])} of freight on deliveries to customers in inventory cost. Freight-out is a selling expense."),
        "dsc_ignored": (m(key_v + p["dsc"]), f"Ignores the {m(p['dsc'])} of purchase discounts taken, which reduce the cost of purchases."),
    }
    key = (m(key_v), f"Correct. {m(p['B'])} + {m(p['P'])} − {m(p['dsc'])} + {m(fin)} − {m(p['fi'])} − ({m(p['E'])} − {m(p['cn'])}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} uses a periodic inventory system and records purchases at gross amounts. Its Year 2 records show beginning inventory of {m(p['B'])}, purchases of {m(p['P'])}, purchase discounts taken of {m(p['dsc'])}, and freight of {m(p['F'])}, of which {m(p['fo'])} was paid to deliver goods to customers. In August, a warehouse fire destroyed goods costing {m(p['fi'])}; {s} reports casualty losses separately from cost of goods sold. The December 31 physical count, priced at cost, totals {m(p['E'])}. It includes goods costing {m(p['cn'])} that a supplier shipped to {s} in December to sell on the supplier's behalf on consignment; {s} has not recorded them as a purchase. What should {s} report as cost of goods sold for Year 2?""",
        choices, ans,
        f"""Cost of goods available: {m(p['B'])} + {m(p['P'])} purchases − {m(p['dsc'])} discounts + freight-in ({m(p['F'])} − {m(p['fo'])} freight-out, a selling expense) = {m(p['B'] + p['P'] - p['dsc'] + fin)}, less the {m(p['fi'])} destroyed by fire (reported as a separate loss). Ending inventory = {m(p['E'])} − {m(p['cn'])} consigned goods, which belong to the supplier = {m(end_inv)}. The consigned goods were never recorded as a purchase, so only the count changes. Cost of goods sold = {m(key_v)}.""",
    )


def inventory_reconciliation(p):
    co, s = p["co"], short(p["co"])
    delta = whole(p["units"] * (D(p["right"]) - D(p["wrong"])))
    assert delta > 0
    C = p["C"]
    S = C - delta + p["wd"] + p["cg"]
    G = C + p["sh"]
    pool = {
        "keep_cons": (m(C + p["cg"]), f"Leaves the {m(p['cg'])} of consigned goods in inventory. {s} holds them for the supplier, which still owns them."),
        "price_sign": (m(C - 2 * delta), f"Subtracts the {m(delta)} pricing difference. The subledger used ${p['wrong']} instead of ${p['right']}, so it is understated."),
        "wd_twice": (m(C - p["wd"]), f"Also subtracts the {m(p['wd'])} write-down from the general ledger, which already includes it."),
        "no_wd": (m(C + p["wd"]), f"Treats the {m(p['wd'])} write-down as a general ledger error. The write-down to net realizable value is correct; the subledger needs it too."),
        "gl": (m(G), f"Uses the general ledger as recorded. The {m(p['sh'])} of goods shipped FOB shipping point on December 31 belong to the customer and are relieved from the ledger."),
    }
    key = (m(C), f"Correct. Subledger {m(S)} + {m(delta)} − {m(p['wd'])} − {m(p['cg'])} = ledger {m(G)} − {m(p['sh'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s perpetual inventory subledger totals {m(S)}, and the general ledger inventory account shows {m(G)}. Investigating the difference, the controller finds: the subledger extends {p['units']:,} units of part {p['part']} at ${p['wrong']} each, while the purchase invoices show ${p['right']}; a {m(p['wd'])} write-down of obsolete goods to net realizable value was recorded in the general ledger but not in the subledger; goods costing {m(p['sh'])} shipped to a customer FOB shipping point on December 31 were removed from the subledger, but the cost of goods sold entry was not posted to the general ledger; and the subledger includes goods costing {m(p['cg'])} that a supplier delivered on December 29 for {s} to sell on consignment. What amount should {s} report as inventory at December 31?""",
        choices, ans,
        f"""Subledger: {m(S)} + {m(delta)} pricing correction ({p['units']:,} × (${p['right']} − ${p['wrong']})) − {m(p['wd'])} write-down − {m(p['cg'])} consigned goods held for the supplier = {m(C)}. General ledger: {m(G)} − {m(p['sh'])} goods whose title passed to the customer at shipment = {m(C)}. The records agree at {m(C)}.""",
    )


def ppe_rollforward_dep(p):
    co, s = p["co"], short(p["co"])
    ca_sold = p["px"] - p["gain"]
    ad_sold = p["sc"] - ca_sold
    assert 0 < ad_sold < p["sc"] and p["ge"] - p["gb"] + p["sc"] + p["fr"] > 0
    key_v = p["ae"] - p["ab"] + ad_sold + p["fr"]
    pool = {
        "no_fr": (m(key_v - p["fr"]), f"Ignores the scrapped equipment. Removing it took its {m(p['fr'])} of accumulated depreciation out of the account."),
        "gain_sign": (m(key_v - 2 * p["gain"]), f"Adds the {m(p['gain'])} gain to the proceeds to get the machine's carrying amount. A gain means the carrying amount was below the {m(p['px'])} proceeds."),
        "px_ca": (m(key_v - p["gain"]), f"Ignores the {m(p['gain'])} gain and takes the machine's carrying amount to be the {m(p['px'])} proceeds, which understates the accumulated depreciation removed by {m(p['gain'])}."),
        "net_only": (m(p["ae"] - p["ab"]), "Uses only the net change in accumulated depreciation, ignoring the depreciation removed for the machine sold and the equipment scrapped."),
        "cost_out": (m(key_v + ca_sold), f"Removes the machine's full {m(p['sc'])} cost from accumulated depreciation. Only its {m(ad_sold)} of accumulated depreciation is removed."),
    }
    key = (m(key_v), f"Correct. {m(p['ae'])} − {m(p['ab'])} + {m(ad_sold)} on the machine sold + {m(p['fr'])} on the scrapped equipment.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s equipment rollforward for Year 2 shows gross equipment of {m(p['gb'])} at January 1 and {m(p['ge'])} at December 31, and accumulated depreciation of {m(p['ab'])} at January 1 and {m(p['ae'])} at December 31. During Year 2, {s} sold a machine that had cost {m(p['sc'])} for {m(p['px'])} in cash and reported a {m(p['gain'])} gain on the sale, and it scrapped fully depreciated equipment that had cost {m(p['fr'])}, receiving nothing. All other changes in the two accounts came from purchases of equipment and depreciation. What depreciation expense should {s} report for Year 2?""",
        choices, ans,
        f"""The machine sold had a carrying amount of {m(p['px'])} − {m(p['gain'])} gain = {m(ca_sold)}, so its accumulated depreciation was {m(p['sc'])} − {m(ca_sold)} = {m(ad_sold)}. The scrapped equipment was fully depreciated, so {m(p['fr'])} of accumulated depreciation was removed with it. Accumulated depreciation: {m(p['ab'])} + depreciation − {m(ad_sold)} − {m(p['fr'])} = {m(p['ae'])}, so depreciation expense = {m(key_v)}.""",
    )


def ppe_reconciliation_nbv(p):
    co, s = p["co"], short(p["co"])
    excess = whole(D(p["M"]) / 5 * 9 / 12)
    key_v = p["Gc"] - p["Ld"] - p["Ga"] + excess
    S = key_v + p["R"]
    pool = {
        "full_year": (m(key_v - excess), f"Keeps the general ledger's full year of depreciation on the new machine. Under {s}'s policy it is depreciated from October, three months: the {m(excess)} excess is reversed."),
        "excess_sign": (m(key_v - 2 * excess), f"Adds the {m(excess)} excess depreciation to accumulated depreciation instead of removing it."),
        "land_keep": (m(key_v + p["Ld"]), f"Leaves the {m(p['Ld'])} of land in the equipment account. Land is a separate, nondepreciable asset, not equipment."),
        "sub": (m(S), f"Uses the subledger as recorded. The {m(p['R'])} of routine repairs is an expense, so the subledger's capitalization of it is reversed."),
        "repair_both": (m(key_v - p["R"]), f"Also subtracts the {m(p['R'])} of repairs from the general ledger, which already expensed them."),
    }
    key = (m(key_v), f"Correct. ({m(p['Gc'])} − {m(p['Ld'])}) − ({m(p['Ga'])} − {m(excess)}), which equals the subledger {m(S)} − {m(p['R'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, Year 2, {co}'s fixed-asset subledger shows equipment with a net carrying amount (cost less accumulated depreciation) of {m(S)}. The general ledger shows equipment cost of {m(p['Gc'])} and accumulated depreciation of {m(p['Ga'])}. {s}'s policy is to depreciate equipment straight-line from the month it is placed in service. The controller's investigation finds: a machine costing {m(p['M'])}, placed in service on October 1, Year 2, with a five-year life and no residual value, was depreciated for a full year in the general ledger, while the subledger follows the policy; the general ledger equipment account includes {m(p['Ld'])} paid on November 15 for land bought as the site of a future plant, on which no depreciation was recorded; and the subledger includes {m(p['R'])} spent on December 30 for routine repairs of a forklift, which the general ledger recorded as repairs expense. What net carrying amount of equipment should {s} report at December 31, Year 2?""",
        choices, ans,
        f"""General ledger: cost {m(p['Gc'])} − {m(p['Ld'])} land reclassified = {m(p['Gc'] - p['Ld'])}. Depreciation on the new machine should be {m(p['M'])} ÷ 5 × 3/12 = {m(whole(D(p['M']) / 5 * 3 / 12))}, not {m(whole(D(p['M']) / 5))}, so accumulated depreciation falls by {m(excess)} to {m(p['Ga'] - excess)}. Net = {m(p['Gc'] - p['Ld'])} − {m(p['Ga'] - excess)} = {m(key_v)}. Subledger: {m(S)} − {m(p['R'])} repairs expensed = {m(key_v)}. The records agree.""",
    )


FAMILIES = [
    # ── Area I ──
    ("far-balance-sheet-0006", A1, "Balance sheet", AP,
     ["ASC 210-10 (balance sheet classification)", "ASC 310-10 (receivables; credit balances reported as liabilities)", "ASC 505-20 (dividends)"],
     balance_sheet_adjust, [
        dict(co="Pellow Co.", ta=2840000, prem=36000, dep=14000, cb=7500, div=40000, note=60000, rate=9, use=["prepaid_all", "no_cb", "no_dep"]),
        dict(co="Quarrie Co.", ta=1960000, prem=24000, dep=11000, cb=6500, div=30000, note=45000, rate=8, use=["no_dep", "div", "int_year"]),
        dict(co="Rudge Co.", ta=3570000, prem=48000, dep=19000, cb=10500, div=55000, note=90000, rate=6, use=["int_year", "prepaid_all", "no_cb"]),
        dict(co="Sowerby Co.", ta=1215000, prem=16800, dep=7500, cb=3600, div=18000, note=36000, rate=10, use=["no_cb", "no_dep", "prepaid_all"]),
     ]),
    ("far-income-statement-0005", A1, "Income statement", AP,
     ["ASC 360-10 (capitalization and depreciation)", "ASC 460-10 (assurance-type warranties)", "ASC 606-10-25 (transfer of control; shipping terms)", "ASC 250-10 (prior-period adjustments only through retained earnings)"],
     income_statement_adjust, [
        dict(co="Tunstall Corp.", draft=760000, E=90000, W=22000, L=31000, G=48000, Gc=30000, use=["rev_only", "no_dep", "no_loss"]),
        dict(co="Ullswater Corp.", draft=1240000, E=140000, W=35000, L=26000, G=75000, Gc=51000, use=["dep_full", "rev_only", "no_warr"]),
        dict(co="Vowell Corp.", draft=530000, E=60000, W=15000, L=19000, G=32000, Gc=20000, use=["no_loss", "no_warr", "dep_full"]),
        dict(co="Wexcombe Corp.", draft=2050000, E=210000, W=48000, L=57000, G=120000, Gc=84000, use=["no_dep", "dep_full", "rev_only"]),
     ]),
    ("far-changes-in-equity-0004", A1, "Statement of changes in equity", AP,
     ["ASC 505-10 (equity; issuance of shares)", "ASC 505-20 (stock dividends; large stock dividends)", "ASC 505-30 (treasury stock; cost method)"],
     apic_adjust, [
        dict(co="Hallam Corp.", X=2150000, n=40000, par=1, price=14, sd=36000, fv=16, G=18000, Def=7000, use=["lsd_fv", "def_re", "gain_left"]),
        dict(co="Ibbotson Corp.", X=1480000, n=25000, par=2, price=18, sd=27000, fv=21, G=12000, Def=5000, use=["no_issue", "lsd_fv", "def_re"]),
        dict(co="Jagoe Corp.", X=3260000, n=60000, par=1, price=11, sd=45000, fv=13, G=26000, Def=9000, use=["gain_left", "no_issue", "lsd_fv"]),
        dict(co="Kitching Corp.", X=980000, n=15000, par=5, price=24, sd=18000, fv=27, G=9000, Def=4000, use=["def_re", "gain_left", "no_issue"]),
     ]),
    ("far-cash-flows-0010", A1, "Statement of cash flows", AP,
     ["ASC 230-10-45 (classification of cash receipts and payments)", "ASC 230-10-50 (noncash investing and financing activities)"],
     scf_financing_adjust, [
        dict(co="Lavery Co.", lb=500000, rp=180000, dd=120000, du=30000, i=45000, c=200000, t=85000, use=["div_full", "int_fin", "no_treasury"]),
        dict(co="Mottram Co.", lb=750000, rp=260000, dd=150000, du=25000, i=62000, c=300000, t=110000, use=["no_treasury", "keep_conv", "div_full"]),
        dict(co="Nuttall Co.", lb=400000, rp=120000, dd=90000, du=18000, i=41000, c=150000, t=70000, use=["int_fin", "no_treasury", "div_sign"]),
        dict(co="Openshaw Co.", lb=900000, rp=350000, dd=200000, du=40000, i=74000, c=250000, t=130000, use=["keep_conv", "div_sign", "int_fin"]),
     ]),
    ("far-notes-0005", A1, "Notes to financial statements", AP,
     ["ASC 470-10-50 (disclosure of long-term debt maturities)", "ASC 842-20-50 (lessee maturity analysis)", "ASC 470-10-45 (short-term obligations expected to be refinanced)"],
     notes_debt_maturities, [
        dict(co="Quarmby Corp.", X=410000, ol=64000, t=250000, np=120000, intr=38000, use=["keep_ol", "full_loan", "no_np"]),
        dict(co="Ratcliffe Corp.", X=585000, ol=92000, t=400000, np=150000, intr=51000, use=["no_np", "keep_ol", "no_loan"]),
        dict(co="Scarth Corp.", X=296000, ol=45000, t=175000, np=80000, intr=27000, use=["no_loan", "no_np", "full_loan"]),
        dict(co="Thwaite Corp.", X=830000, ol=118000, t=600000, np=210000, intr=74000, use=["full_loan", "keep_int", "no_np"]),
     ]),
    ("far-nfp-statement-of-activities-0002", A1, "Statement of activities (Not-for-Profit)", AP,
     ["ASC 958-205 (endowment net assets; releases from restrictions)", "ASC 958-225 (statement of activities; special events)", "ASC 958-320 (investment return)"],
     nfp_activities_adjust, [
        dict(org="Alderbrook Food Bank", X=315000, e=42000, sch=28000, gross=96000, dir=31000, u=17000, use=["no_release", "event", "no_loss"]),
        dict(org="Birchmoor Arts Council", X=228000, e=33000, sch=21000, gross=74000, dir=24000, u=12000, use=["keep_e", "no_release", "event"]),
        dict(org="Coldwater Literacy Project", X=164000, e=26000, sch=15000, gross=52000, dir=18000, u=9000, use=["no_loss", "keep_e", "no_release"]),
        dict(org="Dunmere Youth Orchestra", X=402000, e=57000, sch=36000, gross=118000, dir=41000, u=23000, use=["event", "no_loss", "keep_e"]),
     ]),
    ("far-special-purpose-frameworks-0004", A1, "Special Purpose Frameworks", AP,
     ["AICPA AU-C 800 (special purpose frameworks: income tax basis)", "IRC §§ 61, 166, 168 and 461(h) (rent received in advance, bad debts, depreciation, economic performance)"],
     tax_basis, [
        dict(co="Ferrand Design LLC", X=410000, dg=60000, dt=95000, r=24000, w=18000, wp=11000, b=14000, bw=9000, use=["rent_sign", "warr_gaap", "dep_gaap"]),
        dict(co="Garside Studio LLC", X=285000, dg=42000, dt=70000, r=18000, w=13000, wp=8000, b=11000, bw=4000, use=["no_rent", "dep_gaap", "bad_gaap"]),
        dict(co="Hepworth Partners LLC", X=620000, dg=85000, dt=130000, r=36000, w=27000, wp=16000, b=21000, bw=12000, use=["rent_sign", "no_rent", "dep_gaap"]),
        dict(co="Ilkley Surveying LLC", X=198000, dg=30000, dt=52000, r=15000, w=9000, wp=5000, b=8000, bw=3000, use=["bad_gaap", "rent_sign", "warr_gaap"]),
     ]),
    ("far-foreign-currency-transactions-0002", A1, "Income statement", AP,
     ["ASC 830-20 (foreign currency transactions; remeasurement of monetary items)"],
     fx_transactions, [
        dict(co="Normanton Co.", A=600000, s0="1.10", sd="1.11", s1="1.13", B=250000, c0="0.72", c1="0.75", P=100000, use=["defer", "no_realized", "loss_sign"]),
        dict(co="Ockenden Co.", A=400000, s0="1.15", sd="1.17", s1="1.20", B=300000, c0="0.70", c1="0.74", P=80000, use=["prepaid", "defer", "loss_sign"]),
        dict(co="Pexton Co.", A=900000, s0="1.05", sd="1.06", s1="1.09", B=500000, c0="0.73", c1="0.76", P=150000, use=["no_realized", "prepaid", "defer"]),
        dict(co="Rawcliffe Co.", A=500000, s0="1.12", sd="1.14", s1="1.16", B=200000, c0="0.74", c1="0.79", P=120000, use=["loss_sign", "prepaid", "no_realized"]),
     ]),
    ("far-changes-in-equity-0005", A1, "Statement of changes in equity", AN,
     ["ASC 505-20 (property dividends at fair value)", "ASC 505-30 (retirement of treasury stock)", "ASC 470-20 (conversion of convertible debt under its original terms)", "ASC 320-10 (trading debt securities: unrealized gains and losses in net income)"],
     equity_discrepancies, [
        dict(co="Gledhill Inc.", B=4200000, ni=610000, o=52000, u=28000, dc=180000, ca=95000, fv=140000, tp=120000, tr=150000, bc=500000, fvs=560000, use=["keep_u", "prop_ca", "tr_keep"]),
        dict(co="Haigh Inc.", B=2750000, ni=420000, o=30000, u=19000, dc=110000, ca=60000, fv=85000, tp=75000, tr=90000, bc=300000, fvs=345000, use=["tr_keep", "no_conv", "keep_u"]),
        dict(co="Illingworth Inc.", B=6100000, ni=890000, o=62000, u=41000, dc=260000, ca=130000, fv=205000, tp=170000, tr=210000, bc=750000, fvs=820000, use=["no_conv", "prop_ca", "tr_keep"]),
        dict(co="Jowett Inc.", B=1850000, ni=270000, o=21000, u=14000, dc=75000, ca=40000, fv=62000, tp=50000, tr=65000, bc=200000, fvs=228000, use=["conv_fv", "tr_keep", "prop_ca"]),
     ]),
    ("far-cash-flows-0011", A1, "Statement of cash flows", AN,
     ["ASC 230-10-45 (indirect method; classification)", "ASC 230-10-45-21D (distributions from equity method investees: cumulative earnings approach)", "ASC 323-10 (equity method)"],
     scf_operating_discrepancies, [
        dict(co="Kell Co.", ni=520000, dep=88000, pm=7000, pp=12000, ar=46000, ap=21000, dp=15000, ei=64000, dv=24000, use=["prem_once", "no_eq", "eq_full"]),
        dict(co="Lofthouse Co.", ni=760000, dep=120000, pm=9000, pp=16000, ar=58000, ap=33000, dp=20000, ei=90000, dv=35000, use=["eq_full", "prepaid_once", "keep_dp"]),
        dict(co="Midgley Co.", ni=345000, dep=61000, pm=5000, pp=9000, ar=31000, ap=14000, dp=10000, ei=42000, dv=15000, use=["no_eq", "eq_full", "prem_once"]),
        dict(co="Naylor Co.", ni=1080000, dep=170000, pm=12000, pp=22000, ar=85000, ap=47000, dp=30000, ei=120000, dv=50000, use=["prepaid_once", "keep_dp", "no_eq"]),
     ]),
    # ── Area II ──
    ("far-ppe-held-for-sale-0002", A2, "Property, plant and equipment", AP,
     ["ASC 360-10-45 (long-lived assets classified as held for sale)", "ASC 360-10-55 (implementation guidance: usual and customary terms)"],
     held_for_sale, [
        dict(co="Jolliffe Co.", a=640000, b=210000, c=1150000, d=175000, e=2300000, use=["excl_e", "incl_c", "incl_d"]),
        dict(co="Kershaw Co.", a=820000, b=165000, c=940000, d=230000, e=1600000, use=["incl_b", "incl_c", "incl_d"]),
        dict(co="Lumb Co.", a=455000, b=290000, c=1380000, d=120000, e=2750000, use=["excl_e", "incl_c", "incl_b"]),
        dict(co="Marsden Co.", a=1100000, b=340000, c=760000, d=410000, e=1950000, use=["incl_c", "excl_e", "incl_d"]),
     ]),
    ("far-receivables-factoring-0002", A2, "Trade receivables", AP,
     ["ASC 860-10-40 (conditions for sale accounting)", "ASC 860-20 (sales of financial assets; recourse obligations measured at fair value)"],
     factoring_recourse, [
        dict(co="Sedgwick Co.", date="March 1, Year 1", T=800000, f=3, h=10, R=14000, mx=40000, use=["secured", "fee_only", "max"]),
        dict(co="Tattersall Co.", date="June 1, Year 1", T=600000, f=5, h=8, R=9000, mx=35000, use=["max", "holdback", "secured"]),
        dict(co="Utley Co.", date="September 1, Year 1", T=1000000, f=2, h=12, R=16000, mx=50000, use=["fee_only", "max", "holdback"]),
        dict(co="Vipond Co.", date="November 1, Year 1", T=450000, f=4, h=10, R=11000, mx=25000, use=["secured", "fee_only", "holdback"]),
     ]),
    ("far-inventory-lcm-0001", A2, "Inventory", AP,
     ["ASC 330-10-35 (lower of cost or market for inventory measured using LIFO or the retail inventory method)"],
     lcm_lifo, [
        dict(co="Wadsworth Co.", margin=20, prods=[("X", 2000, "15.00", "13.00", "18.00", "2.00"), ("Y", 1500, "22.00", "21.00", "24.00", "4.00"), ("Z", 800, "10.00", "7.00", "14.00", "1.50")], use=["lcnrv", "no_ceiling", "rc_only"]),
        dict(co="Yarker Co.", margin=25, prods=[("A", 1200, "30.00", "26.00", "34.00", "3.00"), ("B", 900, "18.00", "17.50", "20.00", "3.50"), ("C", 2500, "8.00", "5.00", "10.00", "1.00")], use=["rc_only", "no_floor", "lcnrv"]),
        dict(co="Ackroyd Co.", margin=15, prods=[("P", 3000, "6.00", "5.20", "7.00", "0.60"), ("Q", 1000, "40.00", "39.00", "42.00", "5.00"), ("R", 600, "25.00", "24.00", "30.00", "2.00")], use=["no_floor", "lcnrv", "rc_only"]),
        dict(co="Brearley Co.", margin=20, prods=[("L", 1800, "12.00", "11.40", "14.00", "1.60"), ("M", 700, "50.00", "49.00", "52.00", "6.00"), ("N", 2200, "9.00", "6.00", "12.00", "1.00")], use=["rc_only", "no_floor", "no_ceiling"]),
     ]),
    ("far-debt-noninterest-note-0001", A2, "Debt (Notes and bonds payable)", AP,
     ["ASC 835-30 (imputation of interest on notes exchanged for property)", "ASC 835-30-35 (effective interest method)"],
     zero_coupon_note, [
        dict(co="Cawthorne Corp.", F=500000, r=8, use=["y1", "i1", "face"]),
        dict(co="Dewhirst Corp.", F=750000, r=7, use=["i1", "i2", "face"]),
        dict(co="Eccleston Corp.", F=400000, r=9, use=["y1", "sl", "face"]),
        dict(co="Fairbank Corp.", F=1000000, r=6, use=["y1", "i1", "i2"]),
     ]),
    ("far-cash-bank-reconciliation-0004", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (certified checks; checks written but not mailed at year-end)"],
     bank_reconciliation, [
        dict(co="Pashley Co.", bk=248600, dit=21450, ocl=38720, cert=4800, hu=6350, lp=9400, intr=3180, chk=8812, use=["keep_cert", "no_int", "no_loan"]),
        dict(co="Rishworth Co.", bk=173250, dit=15800, ocl=29460, cert=3500, hu=4900, lp=7250, intr=2460, chk=5120, use=["no_loan", "keep_cert", "no_int"]),
        dict(co="Shackleton Co.", bk=312900, dit=27600, ocl=51300, cert=6200, hu=8750, lp=12600, intr=4350, chk=10457, use=["no_loan", "keep_held", "keep_cert"]),
        dict(co="Thornber Co.", bk=96400, dit=9750, ocl=17880, cert=2100, hu=3300, lp=4600, intr=1250, chk=3309, use=["keep_held", "no_int", "keep_cert"]),
     ]),
    ("far-receivables-rollforward-0003", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "ASC 606-10-32 (sales returns and discounts)", "ASC 326-20 (write-offs)"],
     ar_rollforward, [
        dict(co="Verity Co.", beg=380000, sales=2650000, cs=310000, r=42000, dc=28000, w=19000, n=35000, end=415000, alb=22000, ale=27000, use=["allow", "cash_in", "no_note"]),
        dict(co="Whiteley Co.", beg=520000, sales=3400000, cs=450000, r=61000, dc=37000, w=26000, n=48000, end=566000, alb=31000, ale=39000, use=["allow", "no_disc", "cash_in"]),
        dict(co="Yewdall Co.", beg=210000, sales=1480000, cs=170000, r=23000, dc=15000, w=11000, n=20000, end=236000, alb=12000, ale=16000, use=["no_wo", "allow", "no_note"]),
        dict(co="Armitage Co.", beg=690000, sales=4750000, cs=560000, r=84000, dc=52000, w=33000, n=65000, end=742000, alb=41000, ale=50000, use=["cash_in", "no_disc", "no_note"]),
     ]),
    ("far-receivables-reconciliation-0003", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "Subsidiary ledger and control account reconciliation practice"],
     ar_reconciliation, [
        dict(co="Barraclough Supply", C=746200, mm=3850, u=2700, wo=6300, mp=4100, use=["sub", "memo_twice", "gl_wo"]),
        dict(co="Crowther Supply", C=512900, mm=2600, u=1900, wo=4700, mp=3300, use=["gl_wo", "foot_sign", "sub"]),
        dict(co="Dobson Supply", C=938400, mm=4750, u=3600, wo=8100, mp=5200, use=["misposted", "gl_wo", "foot_sign"]),
        dict(co="Exley Supply", C=365700, mm=1850, u=1400, wo=3900, mp=2250, use=["foot_sign", "gl_wo", "memo_twice"]),
     ]),
    ("far-inventory-rollforward-0003", A2, "Inventory", AN,
     ["ASC 330-10 (inventory cost; freight; purchase discounts)", "ASC 606-10-55 (consignment arrangements)"],
     inventory_rollforward, [
        dict(co="Firth Co.", B=265000, P=1840000, dsc=29000, F=58000, fo=17000, fi=36000, cn=22000, E=298000, use=["keep_cons", "fire_in", "dsc_ignored"]),
        dict(co="Greenwood Co.", B=410000, P=2960000, dsc=44000, F=86000, fo=25000, fi=52000, cn=31000, E=452000, use=["keep_cons", "fo_in", "fire_in"]),
        dict(co="Holroyd Co.", B=148000, P=1020000, dsc=16000, F=33000, fo=9000, fi=21000, cn=13000, E=171000, use=["fo_in", "keep_cons", "freight_all"]),
        dict(co="Ingham Co.", B=530000, P=3710000, dsc=58000, F=104000, fo=31000, fi=67000, cn=40000, E=585000, use=["dsc_ignored", "fire_in", "fo_in"]),
     ]),
    ("far-inventory-reconciliation-0003", A2, "Inventory", AN,
     ["ASC 330-10 (inventory; write-down to net realizable value)", "ASC 606-10-55 (consignment arrangements; shipping terms)"],
     inventory_reconciliation, [
        dict(co="Jagger Co.", C=1284500, units=1600, part="K-14", wrong="23.40", right="24.30", wd=18500, sh=12800, cg=9600, use=["price_sign", "keep_cons", "no_wd"]),
        dict(co="Kilner Co.", C=876300, units=2400, part="B-207", wrong="11.85", right="12.15", wd=14200, sh=9700, cg=7300, use=["price_sign", "wd_twice", "gl"]),
        dict(co="Laycock Co.", C=1642800, units=950, part="T-33", wrong="47.60", right="48.20", wd=22600, sh=16400, cg=11900, use=["no_wd", "wd_twice", "keep_cons"]),
        dict(co="Moorhouse Co.", C=538900, units=3000, part="M-5", wrong="6.45", right="6.90", wd=9800, sh=7100, cg=5400, use=["gl", "no_wd", "price_sign"]),
     ]),
    ("far-ppe-rollforward-0003", A2, "Property, plant and equipment", AN,
     ["ASC 360-10 (property, plant and equipment; depreciation; disposals)"],
     ppe_rollforward_dep, [
        dict(co="Nutter Co.", gb=3400000, ge=3720000, ab=1260000, ae=1395000, sc=240000, px=95000, gain=15000, fr=60000, use=["no_fr", "gain_sign", "cost_out"]),
        dict(co="Oddy Co.", gb=2150000, ge=2380000, ab=840000, ae=905000, sc=180000, px=62000, gain=8000, fr=45000, use=["px_ca", "cost_out", "no_fr"]),
        dict(co="Priestley Co.", gb=5600000, ge=6050000, ab=2100000, ae=2310000, sc=420000, px=150000, gain=22000, fr=95000, use=["cost_out", "gain_sign", "px_ca"]),
        dict(co="Riley Co.", gb=1280000, ge=1410000, ab=470000, ae=520000, sc=110000, px=38000, gain=6000, fr=24000, use=["net_only", "no_fr", "px_ca"]),
     ]),
    ("far-ppe-reconciliation-0003", A2, "Property, plant and equipment", AN,
     ["ASC 360-10 (property, plant and equipment; depreciation; repairs and maintenance)"],
     ppe_reconciliation_nbv, [
        dict(co="Sunderland Co.", Gc=4860000, Ga=1925000, M=240000, Ld=310000, R=8500, use=["full_year", "excess_sign", "land_keep"]),
        dict(co="Tetley Co.", Gc=3120000, Ga=1240000, M=160000, Ld=185000, R=6200, use=["land_keep", "full_year", "sub"]),
        dict(co="Ushaw Co.", Gc=6450000, Ga=2780000, M=320000, Ld=420000, R=11400, use=["excess_sign", "land_keep", "repair_both"]),
        dict(co="Waddington Co.", Gc=2080000, Ga=860000, M=120000, Ld=140000, R=4700, use=["sub", "full_year", "land_keep"]),
     ]),
]

WORD_ITEMS = [
    mcq("far-investments-fair-value-0003", A2, "Investments (Financial assets at fair value)", RU,
        ["ASC 825-10-15 (fair value option: eligible items and scope exceptions)"],
        """During Year 1, Fenmore Corp. acquires each of the financial assets below and, when it first recognizes each one, considers electing the fair value option for it. For which of them is the fair value option not available?""",
        [("Common shares giving it 70% of the votes of a company it must consolidate", "Correct. An investment in a subsidiary that the entity is required to consolidate is excluded from the fair value option; the subsidiary is consolidated."),
         ("Common shares giving it 30% of the votes and significant influence over the investee", "Available. An investment that would otherwise be accounted for by the equity method may be measured at fair value under the fair value option."),
         ("A five-year note receivable from a supplier, issued in exchange for cash", "Available. A note receivable is a recognized financial asset, which the fair value option covers."),
         ("Bonds of a utility that its board has resolved to keep until they mature", "Available. A debt security may be measured at fair value under the option, whatever classification it would otherwise have.")],
        "A",
        """The fair value option in ASC 825-10 covers most recognized financial assets and liabilities, including investments that would otherwise use the equity method, loans and notes receivable, and debt securities, and it is elected instrument by instrument when the item is first recognized. The exclusions include an investment in a subsidiary (or a variable interest entity) that the entity must consolidate, pension and other postretirement obligations, financial assets and liabilities recognized under leases, demand deposit liabilities of banks, and instruments the issuer classifies in equity."""),
    mcq("far-equity-method-0003", A2, "Investments (Equity method investments)", RU,
        ["ASC 323-10-15 (significant influence; presumptions and indicators)"],
        """Heseltine Co. buys common stock of four companies during Year 1 and does not elect the fair value option for any of them. Which investment should Heseltine account for by the equity method?""",
        [("Holding 16% of the voting shares; it names two of nine directors and is the investee's main supplier", "Correct. Holding less than 20% creates a presumption of no significant influence, but board representation and material transactions with the investee are evidence that overcomes it."),
         ("Holding 30% of the voting shares, under a standstill agreement giving up its votes and any board seat", "Holding 20% or more creates a presumption of significant influence, but an agreement under which the investor surrenders significant shareholder rights is evidence that it has none. The shares are reported under ASC 321."),
         ("Holding 55% of the voting shares, which lets Heseltine elect a majority of the directors", "A majority voting interest gives control, so the investee is consolidated, not accounted for by the equity method."),
         ("Holding 19% of the voting shares, with no directors, contracts or other dealings with the investee", "With less than 20% and no other evidence of influence, the presumption of no significant influence stands. The shares are reported under ASC 321.")],
        "A",
        """The equity method applies when an investor can exercise significant influence over an investee's operating and financial policies but does not control it. Owning 20% or more of the voting stock creates a presumption of significant influence, and owning less creates a presumption against it; either presumption can be overcome. Evidence of influence includes board representation, participation in policy-making, material intra-entity transactions, interchange of managers and technological dependency. Evidence against it includes an agreement surrendering significant shareholder rights, such as a standstill agreement. A controlling (majority) interest is consolidated."""),
    mcq("far-intangibles-classification-0001", A2, "Intangible assets", RU,
        ["ASC 350-30-25 (recognition of intangible assets acquired individually; internally developed intangibles)", "ASC 350-30-35 (useful life; intangibles not subject to amortization)"],
        """Corvell Co. bought, or incurred costs for, each of the following during Year 1. Which should Corvell report as an intangible asset that is not amortized?""",
        [("A bought broadcast license, renewable every 10 years at little cost, which it expects to keep renewing", "Correct. The license can be renewed indefinitely at little cost, and no legal, regulatory, contractual or economic factor limits the period it will contribute cash flows, so its useful life is indefinite and it isn't amortized."),
         ("A bought patent with 14 years of legal life left, which it expects to use for all 14 years", "The patent's legal life limits its useful life to 14 years, so it is a finite-lived intangible, amortized over that period."),
         ("Costs of a two-year advertising campaign to build its own brand name, expected to benefit it for decades", "Costs of developing or maintaining an intangible that is not specifically identifiable or is inherent in a continuing business, such as building a brand internally, are expensed as incurred. No asset is recognized."),
         ("A bought customer list that it expects to produce repeat sales for about six years", "The list's expected six-year benefit period is a finite useful life, so it is amortized over six years.")],
        "A",
        """An intangible asset acquired individually is recognized at cost. Costs of internally developing, maintaining or restoring intangibles that are not specifically identifiable, have indeterminate lives, or are inherent in a continuing business are expensed when incurred, so the brand-building campaign creates no asset. A recognized intangible is amortized over its useful life unless no legal, regulatory, contractual, competitive, economic or other factor limits that life; then it is indefinite-lived and not amortized. Renewals that are expected and can be obtained at little cost, without substantial modification, extend the useful life, which is why the broadcast license is indefinite-lived while the patent and customer list are finite-lived."""),
    mcq("far-notes-0006", A1, "Notes to financial statements", AN,
        ["ASC 505-20 and ASC 505-10-50 (dividends declared; equity disclosures)", "ASC 842-20-50 (lessee disclosures; leases not yet commenced)", "ASC 470-10-50 (debt maturities)", "ASC 360-10-50 (property and equipment disclosures)"],
        """A senior accountant is tying Oldroyd Co.'s draft notes to its draft December 31, Year 1, balance sheet before the statements are issued on March 3, Year 2. The draft balance sheet shows property and equipment, net, of $2,140,000; operating lease liabilities of $48,000 (current) and $212,000 (noncurrent); long-term debt of $75,000 (current) and $525,000 (noncurrent); accrued liabilities of $96,000, made up of accrued wages of $61,000 and accrued interest of $35,000; trade accounts payable of $214,000, all owed to suppliers of goods and services; and no other current liabilities. The draft notes say: property and equipment, cost of $3,560,000 less accumulated depreciation of $1,420,000, with cost including $180,000 of fully depreciated equipment still in use; leases, undiscounted lease payments of $292,000 less imputed interest of $32,000, plus a warehouse lease signed on December 1, Year 1, beginning March 1, Year 2, with undiscounted payments of $400,000, not yet recognized; long-term debt, a $600,000 term loan repayable in installments of $75,000 each September 30; and stockholders' equity, a cash dividend of $0.30 per share on the 400,000 common shares outstanding, declared by the board on December 18, Year 1, payable January 20, Year 2, to holders of record on January 6. Which draft note is inconsistent with the draft balance sheet?""",
        [("The stockholders' equity note", "Correct. A cash dividend becomes a liability when the board declares it. The $120,000 (400,000 × $0.30) declared on December 18 should be a current liability, and retained earnings should be lower, but the draft balance sheet shows no dividends payable."),
         ("The property and equipment note", "Consistent. $3,560,000 − $1,420,000 = $2,140,000. Fully depreciated equipment still in use stays in cost and accumulated depreciation until it is retired."),
         ("The lease note", "Consistent. $292,000 − $32,000 = $260,000, the total of the current and noncurrent lease liabilities. A lease that hasn't commenced is disclosed but not recognized until its commencement date."),
         ("The long-term debt note", "Consistent. The $75,000 installment due next September 30 is current, and the remaining $525,000 is noncurrent, as the balance sheet reports.")],
        "A",
        """Each note's figures can be traced to the draft balance sheet. Property: $3,560,000 − $1,420,000 = $2,140,000. Leases: $292,000 − $32,000 = $260,000 = $48,000 + $212,000; the warehouse lease that begins in March is disclosed only, because a lessee recognizes a lease at commencement. Debt: $75,000 current and $525,000 noncurrent of the $600,000 loan. Equity: the dividend declared on December 18 is a liability from the declaration date, so the balance sheet should report $120,000 of dividends payable, which it does not. The draft statements must be corrected."""),
]


ASOF = "Federal income tax rules in effect for 2026 (rent received in advance, bad debts, depreciation, economic performance)"


def main():
    items = [family(*f) for f in FAMILIES] + WORD_ITEMS
    for it in items:
        if it["id"] == "far-special-purpose-frameworks-0004":
            it["review"]["asOf"] = ASOF
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
    if "--dry-run" in sys.argv:
        print("dry run: nothing written")
        return
    write_items(items, CONTENT)


if __name__ == "__main__":
    main()
