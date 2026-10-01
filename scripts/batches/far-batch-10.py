"""FAR batch 10 — 25 items written from scratch, mostly for Areas I and II: the two tasks with no items (I.A.3a,
I.F.a), a second item on four Remembering and Understanding tasks (I.C.1a, II.G.a, III.D.b, III.G.a), a second
item on nine Application tasks, and a further item on ten Analysis tasks (statement discrepancies, cash-flow
derivation, notes versus statements, and the cash, receivables, inventory, PP&E and payables reconciliations).
Target skill mix 6 / 9 / 10; area mix 13 / 10 / 2. Scope and skill tags follow the AICPA CPA Exam Blueprints
effective January 2026.

Numeric items ship with three variants each (method as in far-batch-09.py): each item is a builder, parameter
set 0 is the item and sets 1-3 are its variants, and every family must move the key's letter.

Run: python3 scripts/batches/far-batch-10.py   See docs/reviews/far-batch-10.md.
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
A3 = "Area III — Select Transactions"
NOTE = "Batch 10. Written from scratch; answers solved and every number and distractor computed in code."
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
        assert all(not v.startswith("$-") and v != "$0" and not v.startswith("-") for v in vals), vals


def build(pool, key, use, **kw):
    distinct(pool, key, **kw)
    return pick(pool, key, use)


def r2(x):
    """A ratio to two decimal places, rounded half up."""
    return f"{rd(x, '0.01')}"


# ── Area I ───────────────────────────────────────────────────────────────


def consol_nci(p):
    P, S = p["P"], p["S"]
    sp, ss = short(P), short(S)
    G, L = p["G"], p["L"]
    dep = whole(D(G) / L)
    base = p["N"] - G + dep - p["A"]
    key_v = whole(D(base) * D("0.2"))
    nci = lambda x: m(whole(D(x) * D("0.2")))
    pool = {
        "no_gain": (nci(p["N"] - p["A"]), f"Leaves the {m(G)} gain on {ss}'s sale of equipment to {sp} in {ss}'s income. Profit on a sale within the group isn't realized until the equipment is used up or sold outside the group, and {sp} attributes the elimination proportionately, so the NCI bears 20% of it."),
        "no_dep": (nci(p["N"] - G - p["A"]), f"Eliminates the {m(G)} gain but not the {m(dep)} of it realized in Year 3. {sp} depreciates the equipment on its {m(p['price'])} cost, so {m(G)} ÷ {p['L']} = {m(dep)} of the extra depreciation is added back."),
        "no_amort": (nci(p["N"] - G + dep), f"Leaves out the {m(p['A'])} amortization of the excess of fair value over book value of {ss}'s building. It reduces {ss}'s income as measured in the consolidated statements, so the NCI's share is based on income after it."),
        "fee_back": (nci(base + p["fee"]), f"Adds back the {m(p['fee'])} of management fees {ss} paid {sp}. Eliminating the fee removes {sp}'s revenue and {ss}'s expense together; it doesn't change {ss}'s income or the NCI's share of it."),
        "downstream": (nci(base - p["Dp"]), f"Also charges the NCI with 20% of the {m(p['Dp'])} of unrealized profit on {sp}'s sales to {ss}. Profit on a downstream sale is the parent's, so its elimination is attributed entirely to {sp}."),
    }
    key = (m(key_v), f"Correct. 20% × ({m(p['N'])} − {m(G)} + {m(dep)} − {m(p['A'])}) = 20% × {m(base)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{P} has owned 80% of {S} since acquiring it at the beginning of Year 1, when it measured the noncontrolling interest at fair value. For Year 3, {ss} reports net income of {m(p['N'])}. On January 1, Year 3, {ss} sold equipment to {sp} for {m(p['price'])}; its carrying amount on {ss}'s books was {m(p['price'] - G)}, and {sp} depreciates it straight-line over its remaining {p['L']}-year life with no residual value. Consolidation also records {m(p['A'])} a year of amortization of the acquisition-date excess of fair value over book value of {ss}'s building. During Year 3, {ss} paid {sp} management fees of {m(p['fee'])}, and {sp} sold goods to {ss} at a profit; {ss}'s December 31 inventory includes {m(p['Dp'])} of {sp}'s profit on those goods. {sp} attributes the elimination of profit on {ss}'s sales to {sp} proportionately between the parent and the noncontrolling interest. What net income attributable to the noncontrolling interest should {sp}'s Year 3 consolidated income statement report?""",
        choices, ans,
        f"""The NCI's share is 20% of {ss}'s income as adjusted in consolidation. Start with {ss}'s {m(p['N'])}. The {m(G)} gain on the upstream equipment sale is unrealized and eliminated, and the {m(dep)} of it realized through {sp}'s higher depreciation ({m(G)} ÷ {p['L']}) is added back; under {sp}'s policy these upstream eliminations are shared with the NCI. The {m(p['A'])} amortization of the building's fair value excess reduces {ss}'s income. The management fees eliminate without changing income, and the profit in {ss}'s inventory came from {sp}'s (downstream) sales, so its elimination falls entirely on {sp}. 20% × ({m(p['N'])} − {m(G)} + {m(dep)} − {m(p['A'])}) = 20% × {m(base)} = {m(key_v)}.""",
    )


def nfp_fundraising(p):
    org, s = p["org"], short(p["org"])
    ex = whole(D(p["E"]) * p["fe"] / 100)
    prog = whole(D(p["J"]) * p["ja"] / 100)
    key_v = p["Dv"] + ex + p["J"] + p["Gw"]
    pool = {
        "joint_alloc": (m(key_v - prog), f"Allocates {p['ja']}% of the mailing ({m(prog)}) to the screening program. Joint costs can be allocated only when the activity meets the purpose, audience and content criteria; this audience was chosen for its giving history, so all of the mailing's cost is fundraising."),
        "volunteers": (m(key_v + p["Vv"]), f"Includes the {m(p['Vv'])} market value of the volunteers' time. Soliciting pledges by phone doesn't require specialized skills and doesn't create or enhance a nonfinancial asset, so the contributed services aren't recognized and produce no expense."),
        "exec_none": (m(key_v - ex), f"Leaves out the executive director's fundraising time. Time records put {p['fe']}% of the {m(p['E'])} salary ({m(ex)}) in fundraising, and salaries are allocated to functions on that basis."),
        "grant_mg": (m(key_v - p["Gw"]), f"Reports the {m(p['Gw'])} paid to the grant writer as management and general. Soliciting grants from foundations is a fundraising activity."),
    }
    key = (m(key_v), f"Correct. {m(p['Dv'])} + {m(ex)} + {m(p['J'])} + {m(p['Gw'])}.")
    choices, ans = build(pool, key, p["use"])
    mg = 100 - p["fe"] - p["fp"]
    return variant(
        f"""{org}, a not-for-profit entity that runs free {p['dz']} screening clinics, reports these Year 1 costs. Its development director, whose time records show she worked only on soliciting gifts, was paid {m(p['Dv'])}. Its executive director was paid {m(p['E'])}; her time records show {p['fp']}% program oversight, {mg}% management and general, and {p['fe']}% fundraising. It paid a consultant {m(p['Gw'])} to write grant proposals to private foundations. It spent {m(p['J'])} on a mailing to {p['hh']:,} households that described the warning signs of {p['dz']}, urged readers to book a free screening at its clinics, and asked for donations; the mailing list was bought from a broker who selected households with a record of giving to health charities, and management proposes to charge {p['ja']}% of the mailing's cost, the share of its space given to the health message, to the screening program. Volunteers also staffed a weekend phone campaign asking for pledges; paying for their time at market rates would have cost {m(p['Vv'])}. What amount should {s} report as fundraising expenses in its analysis of expenses by nature and function for Year 1?""",
        choices, ans,
        f"""Salaries are reported by function in line with the time records: the development director's {m(p['Dv'])} and {p['fe']}% of the executive director's salary ({m(ex)}) are fundraising. The grant writer solicits contributions, so the {m(p['Gw'])} is fundraising. The mailing combines a program message with a solicitation, but its audience was selected for its likelihood to give rather than for its need for the health message, so it fails the audience criterion for allocating joint costs, and all {m(p['J'])} is fundraising. The volunteers' phone work requires no specialized skills, so their services aren't recognized and add no expense. Fundraising = {m(p['Dv'])} + {m(ex)} + {m(p['Gw'])} + {m(p['J'])} = {m(key_v)}.""",
    )


def nfp_cf_investing(p):
    org, s = p["org"], short(p["org"])
    key_v = p["E"] + p["B"] - p["S"]
    gain = p["S"] - p["x"]
    assert gain > 0 and key_v > 0
    pool = {
        "donated_inv": (m(key_v - p["Ds"]), f"Reports the {m(p['Ds'])} from selling the donated shares as an investing inflow. Donated securities received without restrictions and converted into cash almost immediately produce an operating cash inflow."),
        "restr_inv": (m(key_v - p["R"]), f"Reports the {m(p['R'])} gift restricted to buying equipment as an investing inflow. Cash contributions restricted to acquiring long-lived assets are financing inflows."),
        "div_inv": (m(key_v - p["i"]), f"Reports the {m(p['i'])} of interest and dividends as an investing inflow. Investment income without donor restrictions is an operating cash flow."),
        "land": (m(key_v + p["L"]), f"Reports the {m(p['L'])} of donated land as an investing outflow. A gift of land involves no cash; it is disclosed as a noncash investing and financing activity."),
        "carrying": (m(key_v + gain), f"Reports the investments sold at their {m(p['x'])} carrying amount. The cash inflow is the {m(p['S'])} received."),
    }
    key = (m(key_v), f"Correct. {m(p['E'])} equipment + {m(p['B'])} endowment securities − {m(p['S'])} proceeds from investments sold.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, bought laboratory equipment for {m(p['E'])} in cash and bought marketable securities for its endowment for {m(p['B'])}. It sold other investments, with a carrying amount of {m(p['x'])}, for {m(p['S'])}. It received {m(p['R'])} in cash from a donor who stipulated that the gift be used to buy equipment, and {m(p['i'])} of interest and dividends on its endowment investments, which the donors allowed {s} to spend for any purpose. A donor gave {s} shares of stock with no restrictions, and under its policy of converting donated securities into cash on receipt, {s} sold them four days later for {m(p['Ds'])}. Another donor gave it land with a fair value of {m(p['L'])}. What net cash used in investing activities should {s} report in its Year 1 statement of cash flows?""",
        choices, ans,
        f"""Investing activities: equipment bought (− {m(p['E'])}), endowment securities bought (− {m(p['B'])}) and proceeds from investments sold (+ {m(p['S'])}), for net cash used of {m(key_v)}. The gift restricted to buying equipment is a financing inflow. Interest and dividends that can be spent for any purpose are operating inflows, and so is the {m(p['Ds'])} from donated shares that came without restrictions and were sold almost at once. The donated land is a noncash transaction, disclosed rather than reported in the statement.""",
    )


def cash_to_accrual(p):
    co, s = p["co"], short(p["co"])
    da, dl, dp = p["A1"] - p["A0"], p["L1"] - p["L0"], p["P0"] - p["P1"]
    assert da > 0 and dl > 0 and dp > 0
    key_v = p["X"] + da - dl - dp + p["Q"] - p["Dp"]
    pool = {
        "ar_sign": (m(key_v - 2 * da), f"Subtracts the {m(da)} increase in client receivables. Fees earned but not yet collected make accrual revenue larger than cash received."),
        "accr_sign": (m(key_v + 2 * dl), f"Adds the {m(dl)} increase in accrued expenses. Expenses incurred but not yet paid make accrual expenses larger than cash paid, which lowers income."),
        "prep_sign": (m(key_v + 2 * dp), f"Adds the {m(dp)} decrease in prepaid insurance. Using up insurance paid for in an earlier year adds expense without any payment this year, which lowers income."),
        "no_equip": (m(key_v - p["Q"] + p["Dp"]), f"Leaves the {m(p['Q'])} equipment purchase as an expense. On the accrual basis the equipment is capitalized, and only its {m(p['Dp'])} of depreciation is expense."),
        "no_dep": (m(key_v + p["Dp"]), f"Capitalizes the equipment but records no depreciation. The {m(p['Dp'])} of Year 2 depreciation is an accrual-basis expense."),
    }
    key = (m(key_v), f"Correct. {m(p['X'])} + {m(da)} − {m(dl)} − {m(dp)} + {m(p['Q'])} − {m(p['Dp'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} keeps its books on the cash basis. Its Year 2 cash receipts from clients exceeded its cash payments by {m(p['X'])}. The payments include {m(p['Q'])} paid in March for new imaging equipment, whose depreciation for Year 2 on the accrual basis is {m(p['Dp'])}. Balances at January 1 and December 31, Year 2, were: client receivables, {m(p['A0'])} and {m(p['A1'])}; accrued wages and other expenses payable, {m(p['L0'])} and {m(p['L1'])}; and prepaid insurance, {m(p['P0'])} and {m(p['P1'])}. There are no other differences between the cash and accrual bases. What is {s}'s Year 2 net income on the accrual basis?""",
        choices, ans,
        f"""Start with the {m(p['X'])} excess of receipts over payments. Revenue: receivables rose by {m(da)}, so fees earned exceeded cash collected: + {m(da)}. Expenses: accrued expenses payable rose by {m(dl)}, so expenses incurred exceeded cash paid: − {m(dl)}; prepaid insurance fell by {m(dp)}, so insurance expense exceeded the premiums paid: − {m(dp)}. The equipment is an asset, not an expense (+ {m(p['Q'])}), and its depreciation is (− {m(p['Dp'])}). Accrual net income = {m(key_v)}.""",
    )


def tie(p):
    co, s = p["co"], short(p["co"])
    ie = p["I"] - p["C"]
    ebit = p["N"] + p["T"] + ie
    key_v = D(ebit) / ie
    vals = {
        "inc_denom": D(ebit) / p["I"],
        "inc_both": D(p["N"] + p["T"] + p["I"]) / p["I"],
        "no_tax": D(p["N"] + ie) / ie,
        "ni_only": D(p["N"]) / ie,
        "paid": D(ebit) / p["Pd"],
    }
    for v in list(vals.values()) + [key_v]:
        assert (v * 1000) % 10 != 5, "half-cent ratio: ambiguous rounding"
    pool = {
        "inc_denom": (r2(vals["inc_denom"]), f"Divides by the {m(p['I'])} of interest incurred. The {m(p['C'])} capitalized into the warehouse isn't interest expense; the ratio's denominator is the {m(ie)} expensed."),
        "inc_both": (r2(vals["inc_both"]), f"Uses the {m(p['I'])} of interest incurred in both the numerator and the denominator. Only the {m(ie)} expensed reduced net income, so only that amount is added back and divided by."),
        "no_tax": (r2(vals["no_tax"]), f"Leaves out the {m(p['T'])} of income tax expense. Earnings before interest and taxes add back both interest expense and income tax expense to net income."),
        "ni_only": (r2(vals["ni_only"]), "Divides net income by interest expense. The numerator is earnings before interest expense and income taxes."),
        "paid": (r2(vals["paid"]), f"Divides by the {m(p['Pd'])} of interest paid in cash. The ratio uses interest expense, {m(ie)}."),
    }
    key = (r2(key_v), f"Correct. ({m(p['N'])} + {m(p['T'])} + {m(ie)}) ÷ {m(ie)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} computes its times-interest-earned ratio as earnings before interest expense and income taxes divided by interest expense. For Year 2, it reports net income of {m(p['N'])} after income tax expense of {m(p['T'])}. During Year 2 it incurred {m(p['I'])} of interest on its borrowings, of which {m(p['C'])} was capitalized as part of the cost of a warehouse it was building; it paid {m(p['Pd'])} of interest in cash. What is {s}'s Year 2 times-interest-earned ratio, rounded to two decimal places?""",
        choices, ans,
        f"""Interest expense is the interest incurred less the amount capitalized: {m(p['I'])} − {m(p['C'])} = {m(ie)}. Earnings before interest expense and income taxes = {m(p['N'])} + {m(p['T'])} + {m(ie)} = {m(ebit)}. Times interest earned = {m(ebit)} ÷ {m(ie)} = {r2(key_v)}. Cash interest paid doesn't enter the ratio.""",
    )


def comp_working_capital(p):
    co, s = p["co"], short(p["co"])
    CA = p["cash"] + p["ar"] + p["inv"] + p["pp"]
    CL = p["ap"] + p["al"]
    W = CA - CL
    key_v = W - p["r"] - p["mi"] + p["g"]
    pool = {
        "c_removed": (m(key_v - p["c"]), f"Removes the {m(p['c'])} of postdated customer checks from current assets. They aren't cash until their dates, but they are receivables, so moving them from cash to accounts receivable leaves current assets unchanged."),
        "no_restrict": (m(key_v + p["r"]), f"Leaves the {m(p['r'])} of construction loan proceeds in current assets. Cash that may be used only to pay for building a noncurrent asset is excluded from current assets."),
        "no_m": (m(key_v + p["mi"]), f"Leaves the whole term loan in noncurrent liabilities. The {m(p['mi'])} installment due on March 1, Year 2, is a current liability."),
        "no_consign": (m(key_v - p["g"]), f"Leaves out the {m(p['g'])} of goods held by dealers. Goods {s} shipped on consignment remain its inventory until the dealers sell them."),
    }
    key = (m(key_v), f"Correct. {m(W)} − {m(p['r'])} − {m(p['mi'])} + {m(p['g'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s staff computed working capital of {m(W)} at December 31, Year 1, from its draft balance sheet: current assets of {m(CA)} (cash {m(p['cash'])}, accounts receivable, net {m(p['ar'])}, inventory {m(p['inv'])} and prepaid expenses {m(p['pp'])}) less current liabilities of {m(CL)} (accounts payable {m(p['ap'])} and accrued liabilities {m(p['al'])}). The year-end close file shows that cash includes {m(p['c'])} of customers' checks dated in January, Year 2, which {s} received in December and will deposit on their dates, and {m(p['r'])} of proceeds from a construction loan, held in a separate account that may be used only to pay the contractors building {s}'s new warehouse. Inventory excludes goods costing {m(p['g'])} that {s} shipped in December to dealers who sell them on its behalf and who still held them at year-end. A five-year term loan taken out on March 1, Year 1, reported entirely among noncurrent liabilities at {m(p['tl'])}, is repayable in five equal annual installments of {m(p['mi'])} beginning March 1, Year 2. What working capital should {s}'s corrected balance sheet report?""",
        choices, ans,
        f"""Postdated checks are receivables, not cash, so reclassifying the {m(p['c'])} leaves current assets unchanged. Cash restricted to paying for the construction of a noncurrent asset is not a current asset: − {m(p['r'])}. Consigned goods still held by the dealers belong to {s}: + {m(p['g'])}. The installment due March 1, Year 2, is a current liability: − {m(p['mi'])}. Working capital = {m(W)} − {m(p['r'])} + {m(p['g'])} − {m(p['mi'])} = {m(key_v)}.""",
    )


def is_discrepancies(p):
    co, s = p["co"], short(p["co"])
    X = p["S"] - p["Cg"] - p["Op"] + p["Ge"]
    pre = whole(D(p["P"]) * 9 / 12)
    key_v = X - p["d"] + p["T"] + pre
    pool = {
        "gain_out": (m(key_v - p["Ge"]), f"Removes the {m(p['Ge'])} fair value gain on the equity securities. Changes in the fair value of equity securities with readily determinable fair values are reported in net income."),
        "no_transit": (m(key_v - p["T"]), f"Leaves ending inventory without the {m(p['T'])} of goods in transit. Shipped FOB shipping point on December 28, they were {s}'s at year-end, and their purchase is already recorded, so the count understated inventory and overstated cost of goods sold."),
        "no_prepaid": (m(key_v - pre), f"Leaves the whole {m(p['P'])} premium in operating expenses. Only October through December has expired; the other nine months ({m(pre)}) are a prepaid asset."),
        "deposit_kept": (m(key_v + p["d"]), f"Leaves the {m(p['d'])} deposit in sales. Revenue is recognized when control of the goods passes, in March, Year 3; until then the deposit is a contract liability."),
        "prepaid_all": (m(key_v + p["P"] - pre), f"Removes the whole {m(p['P'])} premium from expenses. The three months from October through December ({m(p['P'] - pre)}) have expired and are Year 2 expense."),
    }
    key = (m(key_v), f"Correct. {m(X)} − {m(p['d'])} + {m(p['T'])} + {m(pre)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 income statement reports income before income taxes of {m(X)}, built up as follows: sales {m(p['S'])}; cost of goods sold ({m(p['Cg'])}); operating expenses ({m(p['Op'])}); and other income of {m(p['Ge'])}, the increase in fair value of equity securities with readily determinable fair values that {s} held all year. {s} uses a periodic inventory system. Supporting documents show: sales include {m(p['d'])} received on December 15 from a customer as a deposit on machines from {s}'s standard catalog that it will deliver in March, Year 3; the December 31 physical count, used to compute cost of goods sold, left out goods costing {m(p['T'])} that a supplier shipped FOB shipping point on December 28 and {s} received on January 3, although their purchase was recorded in December; and operating expenses include the {m(p['P'])} premium {s} paid on October 1, Year 2, for a one-year insurance policy beginning that day. What should {s}'s corrected income before income taxes be?""",
        choices, ans,
        f"""The deposit is a contract liability until {s} delivers the machines in Year 3: − {m(p['d'])}. Goods shipped FOB shipping point belong to the buyer from shipment; the purchase is recorded, so adding them to ending inventory lowers cost of goods sold: + {m(p['T'])}. Nine months of the insurance premium are prepaid at December 31: {m(p['P'])} × 9/12 = + {m(pre)}. The fair value gain on equity securities is correctly in net income. {m(X)} − {m(p['d'])} + {m(p['T'])} + {m(pre)} = {m(key_v)}.""",
    )


def scf_investing_derive(p):
    co, s = p["co"], short(p["co"])
    ad_sold = p["A0"] + p["Dx"] - p["A1"]
    ca_sold = p["Sc"] - ad_sold
    proceeds = ca_sold + p["g"]
    note = p["Mn"] - p["dn"]
    purchases = p["G1"] - p["G0"] + p["Sc"]
    cashp = purchases - note
    key_v = cashp - proceeds
    assert 0 < ad_sold < p["Sc"] and key_v > 0 and cashp > p["dn"]
    pool = {
        "gross_note": (m(key_v + note), f"Treats the whole {m(p['Mn'])} machine as a cash purchase. Only the {m(p['dn'])} down payment was cash; the {m(note)} note to the seller is a noncash investing and financing activity."),
        "proceeds_ca": (m(key_v + p["g"]), f"Takes the sale proceeds to be the equipment's {m(ca_sold)} carrying amount. The {m(p['g'])} gain means {s} received more than that: {m(proceeds)}."),
        "no_proceeds": (m(key_v + proceeds), f"Leaves out the {m(proceeds)} received for the equipment sold. Proceeds from selling equipment are an investing inflow; only the gain is removed from operating activities."),
        "no_sale_cost": (m(key_v - p["Sc"]), f"Takes equipment purchases to be the {m(p['G1'] - p['G0'])} net increase in the equipment account. The equipment sold took {m(p['Sc'])} out of the account, so purchases were {m(purchases)}."),
        "ad_zero": (m(key_v - ad_sold), f"Ignores the accumulated depreciation removed with the equipment sold, so it puts the proceeds at {m(p['Sc'])} cost plus the gain. Accumulated depreciation: {m(p['A0'])} + {m(p['Dx'])} − {m(p['A1'])} = {m(ad_sold)} was removed."),
    }
    key = (m(key_v), f"Correct. Cash purchases {m(cashp)} − proceeds {m(proceeds)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s comparative balance sheets show equipment of {m(p['G0'])} at January 1, Year 2, and {m(p['G1'])} at December 31, and accumulated depreciation on equipment of {m(p['A0'])} and {m(p['A1'])}. Year 2 depreciation expense on equipment was {m(p['Dx'])}. During Year 2, {s} sold equipment that had cost {m(p['Sc'])} and reported a gain of {m(p['g'])} on the sale; it acquired a machine costing {m(p['Mn'])} by paying {m(p['dn'])} in cash and signing a note payable to the seller for the rest; and it bought other equipment for cash. No other equipment was retired. What net cash used in investing activities do these equipment transactions produce in {s}'s Year 2 statement of cash flows?""",
        choices, ans,
        f"""Accumulated depreciation removed with the equipment sold = {m(p['A0'])} + {m(p['Dx'])} − {m(p['A1'])} = {m(ad_sold)}, so its carrying amount was {m(p['Sc'])} − {m(ad_sold)} = {m(ca_sold)} and the proceeds were {m(ca_sold)} + {m(p['g'])} gain = {m(proceeds)}. Equipment acquired = {m(p['G1'])} − {m(p['G0'])} + {m(p['Sc'])} = {m(purchases)}, of which the {m(note)} financed by the seller's note is noncash, leaving cash purchases of {m(cashp)}. Net cash used in investing activities = {m(cashp)} − {m(proceeds)} = {m(key_v)}.""",
    )


def consol_cl(p):
    P, S = p["P"], p["S"]
    sp, ss = short(P), short(S)
    X = p["Pc"] + p["Sc"] - p["y"] - p["Dv"]
    nci_div = whole(D(p["Dv"]) * D("0.2"))
    key_v = X + p["t"] - p["x"] + nci_div
    pool = {
        "full_div": (m(key_v - nci_div), f"Eliminates all of {ss}'s {m(p['Dv'])} dividend payable. Only {sp}'s 80% is owed within the group; the {m(nci_div)} owed to the noncontrolling shareholders is a liability of the consolidated entity."),
        "no_transit": (m(key_v - p["t"]), f"Leaves the elimination at the {m(p['y'])} on {sp}'s books. {ss} had recorded only {m(p['y'] - p['t'])} of that payable at year-end, so eliminating {m(p['y'])} removed {m(p['t'])} of {ss}'s liabilities to outsiders."),
        "no_fee": (m(key_v + p["x"]), f"Leaves the {m(p['x'])} of management fees {ss} owes {sp} in current liabilities. Balances owed within the group are eliminated."),
        "div_none": (m(key_v + p["Dv"] - nci_div), f"Eliminates none of the dividend payable. The {m(p['Dv'] - nci_div)} owed to {sp} is an intragroup balance and is eliminated."),
    }
    key = (m(key_v), f"Correct. {m(p['Pc'])} + {m(p['Sc'])} − {m(p['y'] - p['t'])} trade payable to {sp} − {m(p['x'])} fees − {m(p['Dv'] - nci_div)} dividend owed to {sp}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{P} owns 80% of {S}{"" if S.endswith(".") else "."} To prepare {sp}'s draft December 31, Year 2, consolidated balance sheet, the staff added {sp}'s current liabilities of {m(p['Pc'])} and {ss}'s of {m(p['Sc'])}, then eliminated {m(p['y'])} for {ss}'s trade payable to {sp} (the balance of {sp}'s trade receivable from {ss}) and {m(p['Dv'])} for the dividend {ss} declared on December 20, payable January 15, Year 3, reporting total current liabilities of {m(X)}. Supporting schedules show: {sp}'s trade receivable from {ss} includes {m(p['t'])} for goods that {sp} shipped FOB shipping point on December 30 and {ss} received and recorded on January 4; {ss}'s accrued liabilities include {m(p['x'])} of December management fees owed to {sp}, which {sp} has recorded in a separate management fees receivable, not in its trade receivable; and {ss} has no other balances with {sp}. After any corrections needed, what total current liabilities should the consolidated balance sheet report?""",
        choices, ans,
        f"""Only balances owed within the group are eliminated. {ss}'s books show a trade payable to {sp} of {m(p['y'])} − {m(p['t'])} in transit = {m(p['y'] - p['t'])}, so that is the liability to eliminate; the in-transit goods are handled on the asset side. The {m(p['x'])} of management fees {ss} owes {sp} is also eliminated. Of the {m(p['Dv'])} dividend payable, 80% ({m(p['Dv'] - nci_div)}) is owed to {sp} and eliminated, while {m(nci_div)} is owed to the noncontrolling shareholders and stays a liability. {m(p['Pc'])} + {m(p['Sc'])} − {m(p['y'] - p['t'])} − {m(p['x'])} − {m(p['Dv'] - nci_div)} = {m(key_v)}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def involuntary(p):
    co, s = p["co"], short(p["co"])
    dep_p = whole(D(p["d"]) * p["mo"] / 12)
    ca = p["C"] - p["A0"] - dep_p
    key_v = p["P"] - ca
    assert key_v > 0
    pool = {
        "no_partial": (m(key_v - dep_p), f"Leaves out depreciation from January 1 to the date of the fire ({m(dep_p)}). Depreciation is recorded up to the date of an involuntary conversion, which lowers the carrying amount and raises the gain."),
        "full_year": (m(key_v + p["d"] - dep_p), f"Records a full year of depreciation ({m(p['d'])}). The warehouse was destroyed on {p['date']}, so only {p['mo']} months ({m(dep_p)}) are recorded."),
        "zero": ("$0", f"Defers the gain because {s} reinvested the proceeds in a replacement warehouse. Under U.S. GAAP, a gain or loss on an involuntary conversion is recognized even when the proceeds are reinvested; deferral is a tax rule."),
        "deductible": (m(key_v + p["ded"]), f"Adds back the {m(p['ded'])} deductible. The gain is measured with the {m(p['P'])} {s} actually received."),
    }
    key = (m(key_v), f"Correct. {m(p['P'])} − ({m(p['C'])} − {m(p['A0'])} − {m(dep_p)}).")
    choices, ans = build(pool, key, p["use"], positive=False)
    return variant(
        f"""{co}'s warehouse, which cost {m(p['C'])} and had accumulated depreciation of {m(p['A0'])} at January 1, Year 4, was destroyed by fire on {p['date']}, Year 4. {s} depreciates the warehouse straight-line at {m(p['d'])} a year and records depreciation up to the date of any disposal. In November, its insurer paid {m(p['P'])} in settlement of the claim, after deducting the policy's {m(p['ded'])} deductible. In December, {s} used the proceeds and other cash to buy a replacement warehouse for {m(p['R'])}. What gain should {s} recognize in Year 4 on the destruction of the warehouse?""",
        choices, ans,
        f"""An involuntary conversion is accounted for like any other disposal: depreciation is recorded to the date of the fire, and the difference between the insurance proceeds and the carrying amount is a gain or loss, whether or not the proceeds are reinvested. Depreciation for {p['mo']} months = {m(p['d'])} × {p['mo']}/12 = {m(dep_p)}. Carrying amount = {m(p['C'])} − {m(p['A0'])} − {m(dep_p)} = {m(ca)}. Gain = {m(p['P'])} − {m(ca)} = {m(key_v)}. The replacement warehouse is recorded at its {m(p['R'])} cost.""",
    )


def impairment(p):
    co, s = p["co"], short(p["co"])
    dep = whole(D(p["K"]) / p["n"])
    ca = p["K"] - 3 * dep
    rem = p["n"] - 3
    U = p["c"] * rem + p["sv"]
    r = D(p["rate"]) / 100
    V = rd((sum(D(p["c"]) / (1 + r) ** t for t in range(1, rem + 1)) + D(p["sv"]) / (1 + r) ** rem) / 1000) * 1000
    assert p["F"] < V < U < ca, (p["F"], V, U, ca)
    key_v = ca - p["F"]
    pool = {
        "cts": (m(key_v + p["cs"]), f"Measures the loss against fair value less the {m(p['cs'])} cost to sell. That is the measure for assets held for sale; {s} is keeping the machine, so the loss is carrying amount less fair value."),
        "undiscounted": (m(ca - U), f"Measures the loss as the carrying amount less the {m(U)} of undiscounted cash flows. Undiscounted cash flows only test recoverability; the loss is measured against fair value."),
        "viu": (m(ca - V), f"Measures the loss against the {m(V)} present value of {s}'s own expected cash flows at its borrowing rate (a value-in-use measure, as under IFRS). U.S. GAAP measures the loss against fair value, the {m(p['F'])} a market participant would pay."),
        "no_dep": (m(key_v + dep), f"Tests the carrying amount before Year 3 depreciation ({m(ca + dep)}). Depreciation for the year is recorded first, then the machine is tested."),
        "cost": (m(p["K"] - p["F"]), f"Measures the loss from the {m(p['K'])} cost, ignoring accumulated depreciation. The test uses the carrying amount, {m(ca)}."),
    }
    key = (m(key_v), f"Correct. {m(ca)} carrying amount − {m(p['F'])} fair value.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} bought a {p['what']} for {m(p['K'])}, which it depreciates straight-line over {p['n']} years with no residual value. At December 31, Year 3, after recording that year's depreciation, demand for the product the machine makes has fallen sharply. {s} now expects the machine to generate net cash inflows of {m(p['c'])} a year for its remaining {rem} years, plus {m(p['sv'])} from selling it at the end of that time. Dealers in similar used machines would pay {m(p['F'])} for it today, and selling it would cost {m(p['cs'])}. Discounted at {s}'s {p['rate']}% incremental borrowing rate, the expected cash flows are worth {m(V)}. {s} plans to keep using the machine. What impairment loss should {s} recognize at December 31, Year 3?""",
        choices, ans,
        f"""Carrying amount = {m(p['K'])} − 3 × {m(dep)} = {m(ca)}. Recoverability test: undiscounted cash flows of {m(p['c'])} × {rem} + {m(p['sv'])} = {m(U)} are less than {m(ca)}, so the carrying amount is not recoverable. For an asset held and used, the loss is the carrying amount less fair value: {m(ca)} − {m(p['F'])} = {m(key_v)}. Costs to sell are not deducted because the machine is not held for sale, and the present value of {s}'s own cash flows is not fair value.""",
    )


def cecl_htm(p):
    co, s = p["co"], short(p["co"])
    wo = p["W"] - p["pc"]
    ending = whole(D(p["X"]) * D(p["r"]) / 100)
    key_v = ending - (p["B0"] - wo)
    assert key_v > 0 and wo < p["B0"]
    pool = {
        "no_wo": (m(ending - p["B0"]), f"Ignores the {m(wo)} write-off, which used up part of the beginning allowance. The allowance before adjustment was {m(p['B0'] - wo)}."),
        "full_wo": (m(key_v + p["pc"]), f"Writes off the bond's whole {m(p['W'])} amortized cost. {s} received {m(p['pc'])}, so only {m(wo)} was written off against the allowance."),
        "ending_only": (m(ending), f"Records the whole required allowance of {m(ending)} as expense. Expense is the amount needed to bring the existing allowance ({m(p['B0'] - wo)} after the write-off) up to {m(ending)}."),
        "fv": (m(p["u"]), f"Records the {m(p['u'])} by which fair value is below amortized cost. Held-to-maturity securities are carried at amortized cost less an allowance for expected credit losses; declines in fair value from changes in interest rates aren't credit losses."),
    }
    key = (m(key_v), f"Correct. {m(ending)} required − ({m(p['B0'])} − {m(wo)}) remaining.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a public business entity, holds a portfolio of unsecured corporate bonds classified as held to maturity. It measures expected credit losses on the portfolio as a pool, by applying a loss rate to amortized cost. Ignore interest in this question. The allowance for credit losses was {m(p['B0'])} at January 1, Year 2. In June, the issuer of one bond, with an amortized cost of {m(p['W'])}, filed for bankruptcy; in October it paid {m(p['pc'])} in final settlement, and {s} wrote off the rest. At December 31, Year 2, the remaining bonds have an amortized cost of {m(p['X'])} and a fair value {m(p['u'])} below it, mostly because market interest rates rose. Based on historical losses adjusted for current conditions and reasonable and supportable forecasts, {s} expects {p['r']}% of the amortized cost of the remaining bonds not to be collected over their lives. What credit loss expense should {s} recognize for Year 2?""",
        choices, ans,
        f"""The allowance at December 31 must equal expected credit losses over the bonds' lives: {p['r']}% × {m(p['X'])} = {m(ending)}. The write-off is the part of the defaulted bond not collected: {m(p['W'])} − {m(p['pc'])} = {m(wo)}, charged against the allowance, which leaves {m(p['B0'])} − {m(wo)} = {m(p['B0'] - wo)}. Credit loss expense = {m(ending)} − {m(p['B0'] - wo)} = {m(key_v)}. The decline in fair value caused by rising interest rates doesn't affect held-to-maturity securities carried at amortized cost.""",
    )


def exit_costs(p):
    co, s = p["co"], short(p["co"])
    T = p["n1"] * p["a1"]
    M = p["n2"] * p["a2"]
    m1 = whole(D(M) / 3)
    key_v = T + p["K"] + m1
    pool = {
        "relocation": (m(key_v + p["R"]), f"Includes the {m(p['R'])} cost of moving equipment. Costs to relocate assets are recognized when incurred, in March, Year 2."),
        "cease": (m(key_v + p["Cs"]), f"Includes the {m(p['Cs'])} of monitoring payments after the center closes. A liability for costs that continue under a contract without benefit to {s} is recognized on the date {s} stops using the right, February 28, Year 2."),
        "m_full": (m(key_v + M - m1), f"Recognizes all {m(M)} of the supervisors' benefits at once. They must work until February 28, more than 60 days after December 1, so their benefits are recognized ratably over December through February: one-third in Year 1."),
        "t_none": (m(key_v - T), f"Leaves out the warehouse staff's {m(T)}. They work only until January 20, within the 60-day minimum retention period that applies when no notice is legally required, so the whole liability is recognized when the plan is communicated, on December 1."),
        "no_k": (m(key_v - p["K"]), f"Leaves out the {m(p['K'])} cancellation penalty. A cost to terminate a contract is recognized when the contract is terminated under its terms, which the December 15 notice did."),
    }
    key = (m(key_v), f"Correct. {m(T)} staff + {m(p['K'])} penalty + {m(M)} × 1/3 supervisors.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On November 20, Year 1, {co}'s board approved a plan to close a distribution center on February 28, Year 2, and on December 1, Year 1, {s} told the affected employees. Its {p['n1']} warehouse staff will be terminated on January 20, Year 2, and each will receive {m(p['a1'])} if they work until then; no law or agreement requires {s} to give notice of termination. Its {p['n2']} supervisors will each receive {m(p['a2'])}, but only if they stay until the center closes. On December 15, Year 1, {s} sent written notice terminating the center's equipment maintenance contract, which is not a lease, and became liable for its {m(p['K'])} cancellation penalty. The center's security monitoring contract, also not a lease, runs to December, Year 2; {s} will pay {m(p['Cs'])} under it for the months after the center closes and will get no benefit from it then. Moving the center's equipment to other sites, at an expected cost of {m(p['R'])}, will happen in March, Year 2. Ignore discounting and treat each month as equal in length. What total liability for exit and disposal costs should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""One-time termination benefits are recognized when the plan is communicated if employees need not work beyond the minimum retention period (the legal notification period, or 60 days when, as here, no notice is required); otherwise they are recognized ratably over the future service period. The warehouse staff work only to January 20, within 60 days of December 1, so all {p['n1']} × {m(p['a1'])} = {m(T)} is recognized on December 1. The supervisors must stay until February 28, beyond 60 days, so their {p['n2']} × {m(p['a2'])} = {m(M)} is spread over December, January and February: {m(m1)} in Year 1. The contract cancellation penalty is recognized when the contract is terminated (December 15): {m(p['K'])}. The monitoring payments are recognized at the cease-use date in Year 2, and relocation costs when incurred. Liability = {m(T)} + {m(p['K'])} + {m(m1)} = {m(key_v)}.""",
    )


def cash_unreconciled(p):
    co, s = p["co"], short(p["co"])
    correct = p["Bk"] + p["dit"] - p["ocl"] - p["o"]
    tr = p["a"] - p["b"]
    assert tr > 0
    G0 = correct + p["n"] - p["N"] - p["i"] + p["f"] + tr
    adj_bank = p["Bk"] + p["dit"] - p["ocl"]
    adj_book = G0 - p["n"] + p["N"] + p["i"] - p["f"]
    U = adj_bank - adj_book
    assert U > 0 and U != p["o"] and U != tr
    pool = {
        "bank_attempt": (m(correct + p["o"]), f"Uses the bookkeeper's adjusted bank balance. Check no. {p['co_chk']} for {m(p['o'])} was issued and recorded but hasn't cleared, so it is outstanding."),
        "book_attempt": (m(correct + tr), f"Uses the bookkeeper's adjusted book balance. Check no. {p['tr_chk']} was paid at {m(p['a'])} but recorded at {m(p['b'])}, so the books overstate cash by {m(tr)}."),
        "trans_sign": (m(correct + 2 * tr), f"Adds the {m(tr)} difference on check no. {p['tr_chk']} to the book balance. The check was recorded for less than it paid out, so the correction lowers cash."),
        "o_double": (m(correct + 2 * p["o"]), f"Adds check no. {p['co_chk']} to the adjusted bank balance. An outstanding check is deducted from the bank balance, because the bank hasn't yet paid it."),
        "old_dit": (m(correct - p["k"]), f"Deducts the {m(p['k'])} February deposit that the bank credited on March 2. It was in transit at February 28 and is already in the March bank balance; it isn't a reconciling item at March 31."),
    }
    key = (m(correct), f"Correct. Bank {m(p['Bk'])} + {m(p['dit'])} − ({m(p['ocl'])} + {m(p['o'])}) = book {m(G0)} − {m(p['n'])} + {m(p['N'])} + {m(p['i'])} − {m(p['f'])} − {m(tr)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s bookkeeper could not reconcile the March 31 bank statement. The bank balance of {m(p['Bk'])}, plus deposits in transit of {m(p['dit'])} and less outstanding checks of {m(p['ocl'])}, gave {m(adj_bank)}; the general ledger balance of {m(G0)}, less a {m(p['n'])} customer check the bank returned for insufficient funds, plus the bank's collection of a {m(p['N'])} note receivable with {m(p['i'])} of interest, less the bank's {m(p['f'])} collection fee, gave {m(adj_book)}. The controller investigates the {m(U)} difference and finds: check no. {p['co_chk']}, for {m(p['o'])}, issued and recorded on March 29, is missing from the list of outstanding checks and has not cleared the bank; check no. {p['tr_chk']}, to a supplier, cleared the bank for {m(p['a'])}, the amount written on it, but was recorded in the cash disbursements journal as {m(p['b'])}; and a {m(p['k'])} deposit made on February 28 was credited by the bank on March 2. What cash balance should {s} report at March 31?""",
        choices, ans,
        f"""Bank side: the omitted check is outstanding, so the correct balance is {m(p['Bk'])} + {m(p['dit'])} − {m(p['ocl'])} − {m(p['o'])} = {m(correct)}. Book side: the check recorded at {m(p['b'])} was paid at {m(p['a'])}, so the books need a further {m(tr)} deduction: {m(adj_book)} − {m(tr)} = {m(correct)}. The February 28 deposit was in transit last month and is already in the March bank balance, so it is not a reconciling item. The {m(U)} difference was {m(p['o'])} − {m(tr)}, and both sides now agree at {m(correct)}.""",
    )


def ar_rollforward_end(p):
    co, s = p["co"], short(p["co"])
    key_v = p["B"] + p["S"] + p["rv"] - (p["C"] - p["cs"]) - p["w"] - p["e"]
    pool = {
        "cs_in": (m(key_v - p["cs"]), f"Doesn't remove the {m(p['cs'])} of cash sales from the cash receipts. Cash sales never passed through accounts receivable, so only {m(p['C'] - p['cs'])} of the receipts were collections of receivables."),
        "no_reinstate": (m(key_v - p["rv"]), f"Treats the {m(p['rv'])} received on the account written off in Year 1 as a collection of current receivables. That account was already out of receivables; collecting it reinstates and then clears it (or goes straight to the allowance), so it doesn't reduce the balance."),
        "refund": (m(key_v - p["y"]), f"Also subtracts the {m(p['y'])} increase in the refund liability for expected returns. Expected returns are a liability, not a reduction of the amounts customers owe."),
        "no_equip": (m(key_v + p["e"]), f"Leaves the {m(p['e'])} account settled with a delivery van in receivables. The account was settled, even though no cash was received."),
        "no_wo": (m(key_v + p["w"]), f"Leaves out the {m(p['w'])} of Year 2 write-offs, which remove accounts from receivables."),
    }
    key = (m(key_v), f"Correct. {m(p['B'])} + {m(p['S'])} − ({m(p['C'])} − {m(p['cs'])} − {m(p['rv'])}) − {m(p['w'])} − {m(p['e'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} is rolling forward its accounts receivable control account for Year 2 to test the aged subledger. Receivables were {m(p['B'])} at January 1. Year 2 sales on account were {m(p['S'])}. The cash receipts journal shows {m(p['C'])} received, including {m(p['cs'])} of cash sales and {m(p['rv'])} collected on an account written off in Year 1. Accounts written off in Year 2 totaled {m(p['w'])}. In November, a customer settled its {m(p['e'])} account by transferring to {s} a delivery van with a fair value of {m(p['e'])}. During the year, {s}'s refund liability for expected sales returns increased by {m(p['y'])}. What balance should the rollforward show for accounts receivable, before any allowance, at December 31, Year 2?""",
        choices, ans,
        f"""Collections that reduce current receivables exclude the {m(p['cs'])} of cash sales and the {m(p['rv'])} recovery of an account written off in Year 1 (it is reinstated and collected, or credited to the allowance, with no net effect on receivables): {m(p['C'])} − {m(p['cs'])} − {m(p['rv'])} = {m(p['C'] - p['cs'] - p['rv'])}. Ending receivables = {m(p['B'])} + {m(p['S'])} − {m(p['C'] - p['cs'] - p['rv'])} − {m(p['w'])} write-offs − {m(p['e'])} settled with the van = {m(key_v)}. The refund liability is a separate liability and doesn't change receivables.""",
    )


def inventory_recon(p):
    co, s = p["co"], short(p["co"])
    C = p["C"]
    fh = whole(D(p["F"]) * p["h"] / p["u"])
    fs = p["F"] - fh
    Sub = C + p["d"] - p["t"] - fh
    GL = C + fs - p["r"]
    pool = {
        "sub": (m(Sub), f"Uses the subledger as recorded. It counts the {m(p['d'])} receipt twice, leaves out the {m(p['t'])} of goods in the public warehouse, and omits the {m(fh)} of freight on units still on hand."),
        "gl": (m(GL), f"Uses the general ledger as recorded. It still carries the {m(fs)} of freight on units already sold and lacks the {m(p['r'])} customer return."),
        "freight_all": (m(C + fs), f"Keeps all {m(p['F'])} of freight in inventory. Freight on the {p['u'] - p['h']:,} units sold belongs in cost of goods sold; only {m(fh)} stays in inventory."),
        "no_freight": (m(C - fh), f"Expenses all of the freight. Inbound freight is part of inventory cost, so the {m(fh)} on units still on hand stays in inventory."),
        "warehouse": (m(C - p["t"]), f"Leaves out the {m(p['t'])} of goods in the public warehouse. {s} still owns goods it stores with a third party."),
    }
    key = (m(C), f"Correct. Subledger {m(Sub)} − {m(p['d'])} + {m(p['t'])} + {m(fh)} = ledger {m(GL)} − {m(fs)} + {m(p['r'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s perpetual inventory subledger totals {m(Sub)}, and its general ledger inventory account shows {m(GL)}. The controller's investigation finds: a December 18 receiving report for goods costing {m(p['d'])} was posted to the subledger twice; goods costing {m(p['t'])} that {s} moved on December 20 to a public warehouse, which stores them for {s} for a fee, were removed from the subledger as if sold, while the general ledger made no entry; {s} paid {m(p['F'])} of inbound freight on a December 2 purchase of {p['u']:,} units, {p['h']:,} of which were still on hand at December 31, and the general ledger charged all of the freight to inventory, while the subledger recorded none of it and cost of goods sold entries, posted from the subledger's costs, relieved none of it from the general ledger; and goods costing {m(p['r'])} that a customer returned on December 30 were restored to the subledger, but the general ledger entry was not posted. What amount should {s} report as inventory at December 31?""",
        choices, ans,
        f"""Freight on the December 2 purchase is part of its cost: {m(p['F'])} × {p['h']:,}/{p['u']:,} = {m(fh)} belongs to units still on hand and {m(fs)} to units sold. Subledger: {m(Sub)} − {m(p['d'])} duplicate posting + {m(p['t'])} goods in the public warehouse, which {s} still owns, + {m(fh)} freight on hand = {m(C)}. General ledger: {m(GL)} − {m(fs)} freight on units sold + {m(p['r'])} customer return = {m(C)}. The records agree at {m(C)}.""",
    )


def ppe_recon_ad(p):
    co, s = p["co"], short(p["co"])
    C = p["C"]
    K = p["K"]
    sub_tr = whole(D(K) / 5)
    cor_tr = whole((D(K) - 2 * D(K) / 5) / 2)
    gl_tr = whole(2 * D(K) / 4 - 2 * D(K) / 5 + D(K) / 4)
    over = gl_tr - cor_tr
    under = cor_tr - sub_tr
    Sub = C + p["As"] - under
    GL = C + p["x"] + over
    pool = {
        "sub": (m(Sub), f"Uses the subledger as recorded. It still includes the {m(p['As'])} for the machine sold, and its trucks are depreciated over the old five-year life."),
        "gl": (m(GL), f"Uses the general ledger as recorded. It includes {m(p['x'])} of depreciation on a press that was already fully depreciated, and a catch-up adjustment on the trucks."),
        "catchup": (m(C + over), f"Accepts the general ledger's catch-up adjustment on the trucks. A change in useful life is a change in estimate, applied prospectively: the remaining carrying amount is spread over the remaining life, with no catch-up."),
        "old_life": (m(C - under), f"Depreciates the trucks over the original five-year life ({m(sub_tr)}). After the revision, the {m(K - 2 * sub_tr)} carrying amount is depreciated over the two remaining years: {m(cor_tr)} a year."),
        "sold_both": (m(C - p["As"]), f"Also subtracts the sold machine's {m(p['As'])} from the general ledger, which already removed it."),
        "press_keep": (m(C + p["x"]), f"Keeps the {m(p['x'])} of depreciation on the fully depreciated press. An asset's accumulated depreciation can't exceed its depreciable cost, so no further depreciation is recorded while it stays in use."),
    }
    key = (m(C), f"Correct. Ledger {m(GL)} − {m(p['x'])} − {m(over)} = subledger {m(Sub)} − {m(p['As'])} + {m(under)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, Year 3, {co}'s fixed-asset subledger shows accumulated depreciation of {m(Sub)}, and the general ledger shows {m(GL)}. The controller's investigation finds three differences. A machine sold for cash on November 30, with accumulated depreciation of {m(p['As'])} at that date, was removed from the general ledger but is still in the subledger. The general ledger recorded {m(p['x'])} of Year 3 depreciation on a stamping press that was fully depreciated at the end of Year 2 and is still in use, while the subledger recorded none. Delivery trucks bought on January 1, Year 1, for {m(K)} were depreciated straight-line over five years with no residual value until January 1, Year 3, when management concluded that their total useful life would be four years, still with no residual value; the subledger kept depreciating them over five years, while the general ledger first recorded an adjustment to bring their accumulated depreciation to what a four-year life would have produced and then recorded a year's depreciation over four years. What accumulated depreciation should {s} report at December 31, Year 3?""",
        choices, ans,
        f"""The machine sold leaves the subledger: − {m(p['As'])}. The press was fully depreciated, so the general ledger's {m(p['x'])} is reversed. The trucks' new life is a change in estimate, applied prospectively: at January 1, Year 3, their carrying amount was {m(K)} − 2 × {m(sub_tr)} = {m(K - 2 * sub_tr)}, depreciated over the two remaining years at {m(cor_tr)} a year. The subledger recorded {m(sub_tr)} ({m(under)} too little); the general ledger recorded a catch-up of {m(whole(2 * D(K) / 4 - 2 * D(K) / 5))} plus {m(whole(D(K) / 4))}, {m(gl_tr)} in all ({m(over)} too much). Subledger: {m(Sub)} − {m(p['As'])} + {m(under)} = {m(C)}. General ledger: {m(GL)} − {m(p['x'])} − {m(over)} = {m(C)}.""",
    )


def ap_recon(p):
    co, s = p["co"], short(p["co"])
    C = p["C"]
    disc = whole(D(p["g"]) * D("0.02"))
    Sub = C - p["db"] - p["h"] + disc + p["dm"]
    GL = C - p["db"] - p["h"]
    pool = {
        "net_db": (m(C - p["db"]), f"Leaves the vendor accounts with {m(p['db'])} of debit balances netted against payables. Amounts vendors owe {s} are receivables, so accounts payable is the total of the credit balances."),
        "held": (m(C - p["h"]), f"Treats the {m(p['h'])} of checks held in the office as paid. A check not delivered to the vendor by year-end hasn't settled the payable."),
        "gross": (m(C + disc), f"Reports the {m(p['g'])} invoice at its gross amount. {s} records purchases net of available discounts, so the invoice is a {m(p['g'] - disc)} payable."),
        "sub": (m(Sub), f"Uses the subledger as recorded. It nets the debit balances, treats the held checks as paid, carries the invoice at gross and lacks the {m(p['dm'])} debit memo."),
        "gl": (m(GL), f"Uses the general ledger as recorded. It nets the {m(p['db'])} of debit balances against payables and treats the {m(p['h'])} of held checks as paid."),
    }
    key = (m(C), f"Correct. Ledger {m(GL)} + {m(p['db'])} + {m(p['h'])} = subledger {m(Sub)} + {m(p['db'])} + {m(p['h'])} − {m(disc)} − {m(p['dm'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s accounts payable subledger totals {m(Sub)}, and its general ledger control account shows {m(GL)}. {s} records purchases net of available cash discounts. The controller's review finds: several vendor accounts have debit balances, totaling {m(p['db'])}, from duplicate payments that the vendors have agreed to refund, and both totals are net of them; checks totaling {m(p['h'])}, recorded as payments on December 31 in both records, were kept in the treasurer's office and not mailed to the vendors until January 12; an invoice for {m(p['g'])} with terms 2/10, n/30, received on December 27, was posted to the vendor's subledger account at its gross amount, while the general ledger recorded it correctly; and a {m(p['dm'])} debit memo for goods returned to a vendor on December 29 was recorded in the general ledger but not in the subledger. What amount should {s} report as accounts payable at December 31?""",
        choices, ans,
        f"""Accounts payable is the total of the amounts {s} owes. Debit balances in vendor accounts are receivables, so the {m(p['db'])} netted in both records is added back. Checks still held at year-end haven't paid anything, so the {m(p['h'])} is restored to both records. In the subledger, the invoice is reduced to its net amount (− {m(disc)}) and the debit memo is posted (− {m(p['dm'])}). General ledger: {m(GL)} + {m(p['db'])} + {m(p['h'])} = {m(C)}. Subledger: {m(Sub)} + {m(p['db'])} + {m(p['h'])} − {m(disc)} − {m(p['dm'])} = {m(C)}. The records agree at {m(C)}.""",
    )


FAMILIES = [
    # ── Area I ──
    ("far-consolidated-statements-0009", A1, "Consolidated financial statements", AP,
     ["ASC 810-10-45 (consolidation procedures: intra-entity profit; attribution to the noncontrolling interest)", "ASC 810-10 (noncontrolling interests)"],
     consol_nci, [
        dict(P="Aldous Corp.", S="Gisburn Inc.", N=360000, price=160000, G=40000, L=5, A=15000, fee=24000, Dp=25000, use=["no_dep", "downstream", "no_gain"]),
        dict(P="Dellow Corp.", S="Hartop Inc.", N=520000, price=210000, G=60000, L=4, A=22000, fee=30000, Dp=35000, use=["no_amort", "fee_back", "no_dep"]),
        dict(P="Embry Corp.", S="Iveson Inc.", N=245000, price=96000, G=27000, L=3, A=11000, fee=14000, Dp=16000, use=["downstream", "no_dep", "no_amort"]),
        dict(P="Fanshaw Corp.", S="Kemble Inc.", N=680000, price=300000, G=75000, L=5, A=26000, fee=42000, Dp=48000, use=["no_gain", "fee_back", "no_amort"]),
     ]),
    ("far-nfp-functional-expenses-0002", A1, "Statement of activities (Not-for-Profit)", AP,
     ["ASC 958-720-45 (functional classification of expenses; joint costs of activities that include fundraising)", "ASC 958-605-25-16 (contributed services)", "ASU 2016-14 (analysis of expenses by nature and function)"],
     nfp_fundraising, [
        dict(org="Larkham Health Outreach", dz="glaucoma", Dv=84000, E=130000, fp=60, fe=15, Gw=12000, J=46000, hh=40000, ja=60, Vv=9500, use=["joint_alloc", "exec_none", "grant_mg"]),
        dict(org="Mabey Heart Foundation", dz="heart disease", Dv=96000, E=150000, fp=55, fe=20, Gw=15000, J=58000, hh=50000, ja=70, Vv=11000, use=["volunteers", "joint_alloc", "exec_none"]),
        dict(org="Nettleford Kidney Alliance", dz="kidney disease", Dv=72000, E=118000, fp=65, fe=10, Gw=9000, J=38000, hh=30000, ja=50, Vv=8000, use=["grant_mg", "volunteers", "joint_alloc"]),
        dict(org="Orrell Skin Cancer Network", dz="skin cancer", Dv=105000, E=160000, fp=60, fe=25, Gw=18000, J=64000, hh=60000, ja=65, Vv=14000, use=["exec_none", "grant_mg", "volunteers"]),
     ]),
    ("far-nfp-cash-flows-0004", A1, "Statement of cash flows (Not-for-Profit)", AP,
     ["ASC 958-230-55 (not-for-profit statement of cash flows)", "ASC 230-10-45-14 and 45-21A (contributions restricted to long-lived assets; sales of donated financial assets)", "ASC 230-10-50 (noncash investing and financing activities)"],
     nfp_cf_investing, [
        dict(org="Pinchbeck Research Institute", E=420000, B=650000, x=230000, S=275000, R=300000, i=38000, Ds=64000, L=500000, use=["donated_inv", "restr_inv", "div_inv"]),
        dict(org="Rendle Marine Institute", E=310000, B=480000, x=150000, S=186000, R=220000, i=27000, Ds=52000, L=350000, use=["land", "restr_inv", "carrying"]),
        dict(org="Satterly Medical Research Trust", E=560000, B=820000, x=340000, S=395000, R=410000, i=49000, Ds=88000, L=640000, use=["div_inv", "carrying", "donated_inv"]),
        dict(org="Tregear Science Foundation", E=245000, B=390000, x=120000, S=152000, R=175000, i=21000, Ds=43000, L=280000, use=["restr_inv", "land", "div_inv"]),
     ]),
    ("far-special-purpose-frameworks-0005", A1, "Special Purpose Frameworks", AP,
     ["AU-C 800 (special purpose frameworks: cash and modified cash bases)", "ASC 606-10 and ASC 360-10 (accrual-basis revenue, expenses and depreciation)"],
     cash_to_accrual, [
        dict(co="Upcott Veterinary Clinic", X=186000, Q=48000, Dp=6000, A0=21000, A1=33000, L0=9000, L1=14500, P0=7200, P1=4800, use=["ar_sign", "accr_sign", "no_dep"]),
        dict(co="Vardy Animal Hospital", X=243000, Q=65000, Dp=9750, A0=28000, A1=41500, L0=12000, L1=19000, P0=9600, P1=6000, use=["prep_sign", "accr_sign", "no_dep"]),
        dict(co="Wetherall Pet Clinic", X=128000, Q=36000, Dp=4500, A0=15500, A1=24000, L0=6200, L1=9800, P0=5400, P1=3600, use=["no_equip", "ar_sign", "no_dep"]),
        dict(co="Allerton Veterinary Practice", X=312000, Q=84000, Dp=10500, A0=37000, A1=52000, L0=16000, L1=23500, P0=12000, P1=8400, use=["no_equip", "ar_sign", "accr_sign"]),
     ]),
    ("far-ratios-0006", A1, "Financial Statement Ratios and Performance Metrics", AP,
     ["Financial statement analysis: solvency ratios (times interest earned)", "ASC 835-20 (capitalization of interest)"],
     tie, [
        dict(co="Brough Corp.", N=642000, T=214000, I=196000, C=46000, Pd=138000, use=["inc_denom", "no_tax", "ni_only"]),
        dict(co="Catterick Corp.", N=455000, T=152000, I=148000, C=33000, Pd=104000, use=["paid", "inc_both", "no_tax"]),
        dict(co="Dacre Corp.", N=918000, T=306000, I=264000, C=59000, Pd=187000, use=["inc_both", "paid", "ni_only"]),
        dict(co="Gargrave Corp.", N=377000, T=126000, I=121000, C=27000, Pd=86000, use=["paid", "inc_denom", "inc_both"]),
     ]),
    ("far-balance-sheet-0007", A1, "Balance sheet", AN,
     ["ASC 210-10-45 (current assets and current liabilities; cash restricted for noncurrent uses)", "ASC 470-10-45 (current maturities of long-term debt)", "ASC 606-10-55 (consignment arrangements)"],
     comp_working_capital, [
        dict(co="Marske Co.", cash=318000, ar=486000, inv=642000, pp=34000, ap=402000, al=126000, c=27000, r=150000, g=58000, tl=480000, mi=96000, use=["c_removed", "no_consign", "no_m"]),
        dict(co="Nappa Co.", cash=255000, ar=371000, inv=498000, pp=26000, ap=318000, al=97000, c=19000, r=120000, g=44000, tl=350000, mi=70000, use=["no_restrict", "no_m", "c_removed"]),
        dict(co="Redmire Co.", cash=412000, ar=598000, inv=815000, pp=41000, ap=534000, al=148000, c=36000, r=210000, g=73000, tl=625000, mi=125000, use=["no_consign", "c_removed", "no_restrict"]),
        dict(co="Starbotton Co.", cash=184000, ar=263000, inv=357000, pp=18000, ap=226000, al=71000, c=14000, r=85000, g=31000, tl=260000, mi=52000, use=["no_m", "no_restrict", "no_consign"]),
     ]),
    ("far-income-statement-0006", A1, "Income statement", AN,
     ["ASC 606-10-25 (transfer of control; contract liabilities)", "ASC 330-10 (inventory; goods in transit)", "ASC 321-10-35 (equity securities: fair value changes in net income)", "ASC 340-10 (prepaid expenses)"],
     is_discrepancies, [
        dict(co="Thoralby Co.", S=3840000, Cg=2310000, Op=905000, Ge=26000, d=82000, T=52000, P=48000, use=["gain_out", "no_transit", "no_prepaid"]),
        dict(co="Arncliffe Co.", S=2960000, Cg=1785000, Op=694000, Ge=18000, d=55000, T=29000, P=36000, use=["deposit_kept", "gain_out", "prepaid_all"]),
        dict(co="Burnsall Co.", S=5120000, Cg=3090000, Op=1210000, Ge=34000, d=96000, T=51000, P=64000, use=["no_transit", "deposit_kept", "no_prepaid"]),
        dict(co="Conistone Co.", S=2215000, Cg=1330000, Op=521000, Ge=14000, d=42000, T=22000, P=28800, use=["prepaid_all", "no_prepaid", "deposit_kept"]),
     ]),
    ("far-cash-flows-0012", A1, "Statement of cash flows", AN,
     ["ASC 230-10-45-13 (cash flows from investing activities)", "ASC 230-10-50-3 (noncash investing and financing activities)", "ASC 360-10 (derecognition of equipment)"],
     scf_investing_derive, [
        dict(co="Hetton Co.", G0=2840000, G1=3175000, A0=1120000, A1=1205000, Dx=248000, Sc=290000, g=17000, Mn=180000, dn=40000, use=["gross_note", "proceeds_ca", "no_proceeds"]),
        dict(co="Litton Co.", G0=1960000, G1=2215000, A0=780000, A1=846000, Dx=180000, Sc=210000, g=12000, Mn=140000, dn=30000, use=["no_sale_cost", "gross_note", "ad_zero"]),
        dict(co="Halton Co.", G0=4150000, G1=4580000, A0=1640000, A1=1772000, Dx=362000, Sc=405000, g=24000, Mn=260000, dn=55000, use=["proceeds_ca", "ad_zero", "gross_note"]),
        dict(co="Gayle Co.", G0=1380000, G1=1572000, A0=536000, A1=581000, Dx=121000, Sc=148000, g=9000, Mn=96000, dn=20000, use=["ad_zero", "no_sale_cost", "proceeds_ca"]),
     ]),
    ("far-consolidated-statements-0010", A1, "Consolidated financial statements", AN,
     ["ASC 810-10-45 (consolidation procedures: intra-entity balances)", "ASC 810-10 (noncontrolling interests)"],
     consol_cl, [
        dict(P="Cracoe Corp.", S="Aysgarth Inc.", Pc=1840000, Sc=760000, y=118000, t=26000, x=21000, Dv=90000, use=["full_div", "no_transit", "no_fee"]),
        dict(P="Linton Corp.", S="Sedbusk Inc.", Pc=1265000, Sc=548000, y=84000, t=19000, x=15000, Dv=70000, use=["no_fee", "div_none", "full_div"]),
        dict(P="Healaugh Corp.", S="Muker Inc.", Pc=2470000, Sc=1020000, y=156000, t=34000, x=28000, Dv=120000, use=["no_transit", "no_fee", "div_none"]),
        dict(P="Carperby Corp.", S="Keasden Inc.", Pc=930000, Sc=402000, y=62000, t=14000, x=11000, Dv=45000, use=["div_none", "full_div", "no_transit"]),
     ]),
    # ── Area II ──
    ("far-ppe-involuntary-conversion-0001", A2, "Property, plant and equipment", AP,
     ["ASC 610-30 (gains and losses on involuntary conversions of nonmonetary assets to monetary assets)", "ASC 360-10 (depreciation)"],
     involuntary, [
        dict(co="Keld Co.", C=1470000, A0=588000, d=58800, date="April 30", mo=4, P=1060000, ded=25000, R=1600000, use=["no_partial", "full_year", "zero"]),
        dict(co="Lindley Co.", C=984000, A0=393600, d=39360, date="July 31", mo=7, P=705000, ded=20000, R=1100000, use=["zero", "no_partial", "deductible"]),
        dict(co="Otley Co.", C=2256000, A0=1128000, d=90240, date="March 31", mo=3, P=1480000, ded=50000, R=2500000, use=["full_year", "deductible", "zero"]),
        dict(co="Pateley Co.", C=768000, A0=230400, d=30720, date="September 30", mo=9, P=640000, ded=15000, R=850000, use=["zero", "full_year", "no_partial"]),
     ]),
    ("far-ppe-impairment-0003", A2, "Property, plant and equipment", AP,
     ["ASC 360-10-35 (impairment of long-lived assets held and used: recoverability test and measurement at fair value)", "ASC 820-10 (fair value)"],
     impairment, [
        dict(co="Rylstone Co.", what="bottling machine", K=1200000, n=8, c=110000, sv=60000, F=405000, cs=18000, rate=8, use=["viu", "cts", "no_dep"]),
        dict(co="Farnhill Co.", what="printing press", K=900000, n=6, c=125000, sv=40000, F=310000, cs=14000, rate=7, use=["undiscounted", "cts", "no_dep"]),
        dict(co="Uldale Co.", what="molding machine", K=1500000, n=10, c=120000, sv=80000, F=560000, cs=25000, rate=9, use=["viu", "undiscounted", "cts"]),
        dict(co="Wensley Co.", what="packaging line", K=720000, n=6, c=105000, sv=30000, F=226000, cs=11000, rate=8, use=["viu", "no_dep", "undiscounted"]),
     ]),
    ("far-investments-htm-credit-loss-0002", A2, "Investments (Financial assets at amortized cost)", AP,
     ["ASC 326-20 (current expected credit losses: pooled measurement, write-offs, accrued interest elections)", "ASC 320-10 (held-to-maturity debt securities)"],
     cecl_htm, [
        dict(co="Askrigg Corp.", B0=46000, W=60000, pc=24000, X=4800000, r="1.2", u=135000, use=["no_wo", "ending_only", "fv"]),
        dict(co="Bainbridge Corp.", B0=38000, W=50000, pc=18000, X=3600000, r="1.4", u=96000, use=["full_wo", "no_wo", "ending_only"]),
        dict(co="Coverham Corp.", B0=62000, W=85000, pc=40000, X=6200000, r="1.1", u=171000, use=["ending_only", "fv", "full_wo"]),
        dict(co="Draughton Corp.", B0=29000, W=40000, pc=15000, X=2750000, r="1.3", u=58000, use=["no_wo", "full_wo", "fv"]),
     ]),
    ("far-exit-costs-0002", A2, "Payables and accrued liabilities", AP,
     ["ASC 420-10-25 (one-time employee termination benefits; contract termination costs; other associated costs)", "ASC 420-10-30 (measurement at fair value)"],
     exit_costs, [
        dict(co="Embsay Co.", n1=40, a1=3000, n2=6, a2=12000, K=18000, Cs=21000, R=35000, use=["no_k", "m_full", "relocation"]),
        dict(co="Flasby Co.", n1=55, a1=2500, n2=8, a2=9000, K=14000, Cs=16500, R=28000, use=["t_none", "no_k", "cease"]),
        dict(co="Kettlewell Co.", n1=30, a1=4000, n2=5, a2=15000, K=22000, Cs=26000, R=41000, use=["m_full", "cease", "relocation"]),
        dict(co="Langcliffe Co.", n1=64, a1=2000, n2=7, a2=10500, K=12000, Cs=19000, R=24000, use=["t_none", "no_k", "m_full"]),
     ]),
    ("far-cash-unreconciled-0002", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (unrecorded outstanding checks; errors in recording disbursements; bank collections and charges)"],
     cash_unreconciled, [
        dict(co="Austwick Co.", Bk=86420, dit=7350, ocl=12680, o=4385, n=840, N=6000, i=180, f=35, a=5630, b=3650, k=3215, co_chk=7214, tr_chk=7190, use=["bank_attempt", "book_attempt", "o_double"]),
        dict(co="Clapham Co.", Bk=64180, dit=5240, ocl=9875, o=4860, n=615, N=4500, i=135, f=25, a=8150, b=5180, k=2460, co_chk=5532, tr_chk=5507, use=["old_dit", "bank_attempt", "book_attempt"]),
        dict(co="Feizor Co.", Bk=112650, dit=9820, ocl=16340, o=5125, n=1125, N=8000, i=240, f=40, a=9270, b=7290, k=4370, co_chk=9047, tr_chk=9011, use=["trans_sign", "old_dit", "bank_attempt"]),
        dict(co="Giggleswick Co.", Bk=47390, dit=4160, ocl=7520, o=3175, n=470, N=3000, i=90, f=20, a=3810, b=1830, k=1940, co_chk=3318, tr_chk=3296, use=["old_dit", "trans_sign", "o_double"]),
     ]),
    ("far-receivables-rollforward-0004", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "ASC 326-20-35 (write-offs and recoveries)", "ASC 606-10-55 (sales with a right of return: refund liability)"],
     ar_rollforward_end, [
        dict(co="Horton Co.", B=462000, S=3180000, C=3365000, cs=284000, rv=7000, w=23000, e=31000, y=12000, use=["cs_in", "no_reinstate", "refund"]),
        dict(co="Ribblehead Co.", B=338000, S=2410000, C=2540000, cs=205000, rv=5500, w=17500, e=24000, y=9000, use=["no_equip", "refund", "cs_in"]),
        dict(co="Selside Co.", B=615000, S=4270000, C=4525000, cs=372000, rv=9200, w=31000, e=46000, y=15000, use=["no_wo", "no_reinstate", "no_equip"]),
        dict(co="Stainforth Co.", B=249000, S=1765000, C=1860000, cs=148000, rv=4100, w=12500, e=18000, y=6500, use=["refund", "no_wo", "cs_in"]),
     ]),
    ("far-inventory-reconciliation-0004", A2, "Inventory", AN,
     ["ASC 330-10-30 (inventory cost, including inbound freight)", "ASC 330-10 (ownership of goods held by others)"],
     inventory_recon, [
        dict(co="Winskill Co.", C=1186400, d=14600, t=37800, F=18000, u=5000, h=1200, r=24600, use=["no_freight", "warehouse", "freight_all"]),
        dict(co="Airton Co.", C=842700, d=10800, t=26500, F=12800, u=4000, h=1000, r=19900, use=["gl", "sub", "warehouse"]),
        dict(co="Bordley Co.", C=1574300, d=19500, t=48200, F=25000, u=10000, h=3200, r=31600, use=["freight_all", "no_freight", "gl"]),
        dict(co="Calton Co.", C=627900, d=8200, t=19400, F=9600, u=3000, h=900, r=14700, use=["warehouse", "freight_all", "sub"]),
     ]),
    ("far-ppe-reconciliation-0004", A2, "Property, plant and equipment", AN,
     ["ASC 360-10 (depreciation; derecognition; fully depreciated assets)", "ASC 250-10-45-17 (change in accounting estimate applied prospectively)"],
     ppe_recon_ad, [
        dict(co="Eshton Co.", C=2386000, As=164000, x=42000, K=360000, use=["old_life", "catchup", "press_keep"]),
        dict(co="Gordale Co.", C=1748000, As=118000, x=31000, K=240000, use=["sold_both", "gl", "old_life"]),
        dict(co="Hanlith Co.", C=3124000, As=212000, x=56000, K=480000, use=["press_keep", "sub", "old_life"]),
        dict(co="Scosthrop Co.", C=1291000, As=86000, x=23000, K=180000, use=["catchup", "sold_both", "gl"]),
     ]),
    ("far-payables-reconciliation-0003", A2, "Payables and accrued liabilities", AN,
     ["ASC 405-10 (liabilities)", "ASC 210-10-45 (debit balances in payables reported as assets)", "ASC 330-10-30 (inventory cost: purchases recorded net of cash discounts)"],
     ap_recon, [
        dict(co="Swinden Co.", C=538600, db=12400, h=17300, g=185000, dm=3900, use=["net_db", "held", "sub"]),
        dict(co="Threshfield Co.", C=724900, db=11200, h=23600, g=260000, dm=5300, use=["gross", "gl", "held"]),
        dict(co="Wigglesworth Co.", C=391700, db=6100, h=12800, g=140000, dm=2700, use=["held", "gross", "net_db"]),
        dict(co="Cononley Co.", C=965300, db=14700, h=31200, g=330000, dm=6800, use=["gl", "net_db", "gross"]),
     ]),
]

WORD_ITEMS = [
    mcq("far-comprehensive-income-0004", A1, "Statement of comprehensive income", RU,
        ["ASC 220-10-45 (presentation of comprehensive income: one continuous statement or two consecutive statements; tax effects of OCI components)", "ASC 810-10-45 (attribution of comprehensive income to the parent and the noncontrolling interest)"],
        """Hawkhurst Corp., a public company with a 70%-owned subsidiary, has several items of other comprehensive income (OCI) for Year 2. Which statement describes how Hawkhurst reports comprehensive income under U.S. GAAP?""",
        [("It may report net income and OCI in one continuous statement or in two consecutive statements", "Correct. U.S. GAAP requires comprehensive income to be reported either in a single continuous statement of comprehensive income or in two separate but consecutive statements: an income statement followed immediately by a statement of OCI."),
         ("It may report the components of OCI solely in its statement of changes in stockholders' equity", "Reporting OCI only in the statement of changes in equity was an option before ASU 2011-05 removed it. Comprehensive income must now be reported in a performance statement."),
         ("It reports only the comprehensive income attributable to the parent, leaving out the noncontrolling interest's share", "Total comprehensive income includes the noncontrolling interest's share; the amounts attributable to the parent and to the noncontrolling interest are each presented."),
         ("It must report each component of OCI net of tax, with no line for the related income tax effects", "Components of OCI may be presented net of tax, or before tax with one amount for the related income tax; either way, the tax on each component is disclosed.")],
        "A",
        """The statement of comprehensive income reports all changes in equity during a period other than those from investments by and distributions to owners: net income plus other comprehensive income. Under ASC 220-10-45 an entity presents it in one continuous statement (net income, the components of OCI, then total comprehensive income) or in two separate but consecutive statements. A consolidated entity presents total comprehensive income and the amounts attributable to the parent and to the noncontrolling interest. OCI components may be shown net of tax or before tax with a single tax line. The option of reporting OCI only in the statement of changes in equity was removed by ASU 2011-05."""),
    mcq("far-ratios-0005", A1, "Financial Statement Ratios and Performance Metrics", RU,
        ["Financial statement analysis: choosing ratios (coverage, leverage, liquidity and profitability ratios)"],
        """A bank is deciding whether to renew Calverley Co.'s term loan. Its credit officer wants to know how far Calverley's operating profit could fall before it would no longer cover the annual cost of its borrowings. Which measure best serves that purpose?""",
        [("Times interest earned", "Correct. Times interest earned divides earnings before interest and taxes by interest expense, showing how many times earnings cover the interest charges, which is the margin the officer wants."),
         ("Debt-to-equity ratio", "Debt to equity measures how the company is financed (leverage), not whether its earnings cover the interest on that debt."),
         ("Operating cash flow to current liabilities", "This is a liquidity measure: it compares a year's operating cash flow with obligations due within a year, not earnings with interest charges."),
         ("Cash debt coverage (operating cash flow ÷ average total liabilities)", "Cash debt coverage compares a year's operating cash flow with all of the company's debt, which bears on its ability to repay principal, not on how many times profit covers the interest charge.")],
        "A",
        """Coverage ratios answer whether earnings can service debt. Times interest earned (earnings before interest and taxes ÷ interest expense) shows how many times earnings cover the year's interest, so a higher figure means a wider margin before a fall in earnings would leave interest unpaid. Leverage ratios such as debt to equity describe the capital structure, liquidity ratios compare resources with short-term obligations, and profitability ratios such as return on assets measure returns."""),
    mcq("far-governmental-measurement-focus-0002", A1, "Measurement focus and basis of accounting", RU,
        ["GASB Statement No. 34 (governmental funds: current financial resources measurement focus and modified accrual basis; capital assets reported only in the government-wide statements)", "GASB Codification 1600 (basis of accounting)"],
        """Rosedale County's general fund pays cash for a new fire engine with a ten-year useful life. Given the measurement focus and basis of accounting used for the general fund, how is the purchase reported in the county's governmental funds financial statements?""",
        [("As an expenditure for the full cost in the year of purchase", "Correct. Governmental funds use the current financial resources measurement focus and the modified accrual basis, so buying a capital asset is an expenditure (capital outlay) when the liability is incurred; the asset isn't recorded in the fund."),
         ("As a capital asset in the general fund, depreciated over ten years", "That is how the government-wide statements report it, using the economic resources measurement focus and the accrual basis. The general fund doesn't report capital assets or depreciation."),
         ("As a capital asset in the general fund, with no depreciation recorded", "The general fund reports only current financial resources, so it doesn't carry the fire engine as an asset, depreciated or not."),
         ("As a deferred outflow of resources, amortized over the engine's ten-year life", "A deferred outflow is a consumption of net assets that applies to a future period in specific situations GASB defines; buying a capital asset is not one of them, and governmental funds don't amortize capital costs.")],
        "A",
        """Governmental funds, including the general fund, report using the current financial resources measurement focus and the modified accrual basis of accounting. They report what has happened to spendable resources, so a capital asset purchase is recognized as an expenditure, typically capital outlay, for its full cost when the liability is incurred, and no asset or depreciation appears in the fund. The government-wide statements, which use the economic resources measurement focus and the accrual basis, report the fire engine as a capital asset and depreciate it."""),
    mcq("far-asset-retirement-obligations-0002", A2, "Payables and accrued liabilities", RU,
        ["ASC 410-20-35 (subsequent measurement of asset retirement obligations: revisions to the timing or amount of estimated cash flows)"],
        """Corrie Mining recognized an asset retirement obligation for a quarry in Year 1, discounting the expected cash flows at its credit-adjusted risk-free rate at that time, 6%. In Year 4, it raises its estimate of the undiscounted cash flows needed to restore the site, and its credit-adjusted risk-free rate is now 8%. At what rate should Corrie discount the increase in the estimated cash flows?""",
        [("Its current credit-adjusted risk-free rate of 8%", "Correct. An upward revision in estimated undiscounted cash flows creates a new layer of the liability, measured using the current credit-adjusted risk-free rate."),
         ("The 6% credit-adjusted risk-free rate used for the original obligation", "The original rate applies to downward revisions, which reduce existing layers. An increase is a new layer, discounted at today's rate."),
         ("A risk-free rate, with no adjustment for Corrie's own credit standing", "Asset retirement obligations are discounted at a credit-adjusted risk-free rate, which reflects the entity's credit standing."),
         ("A weighted average of the credit-adjusted rates used for the existing layers", "A weighted-average rate is used for a downward revision when the layer it relates to can't be identified, not for an increase.")],
        "A",
        """Under ASC 410-20, changes in an asset retirement obligation from revisions to the timing or amount of estimated undiscounted cash flows are recognized as changes in the liability and the related asset retirement cost. An upward revision is a new liability layer, discounted at the entity's current credit-adjusted risk-free rate. A downward revision is discounted at the rate used when the related layer was first recognized (or a weighted-average rate if that layer can't be identified). The rate is always credit-adjusted."""),
    mcq("far-valuation-allowance-0002", A3, "Accounting for income taxes", RU,
        ["ASC 740-10-30-5 (valuation allowance: more likely than not)", "ASC 740-10-30-16 to 30-25 (weighing positive and negative evidence)"],
        """At December 31, Year 2, Ardley Corp. reports a deferred tax asset for a tax credit carryforward that expires in Year 6. After weighing all available positive and negative evidence, management estimates a 55% likelihood that part of the credit will expire unused. How should Ardley report the deferred tax asset?""",
        [("Reduce it by a valuation allowance for the part expected to expire unused", "Correct. A valuation allowance is needed when it is more likely than not (a likelihood of more than 50%) that some portion of a deferred tax asset will not be realized, and it reduces the asset to the amount more likely than not to be realized."),
         ("Report it in full, since expiry of any part of the credit isn't yet probable", "Probable is the loss-contingency threshold. The valuation allowance threshold is lower: more likely than not."),
         ("Reduce it by a valuation allowance equal to 55% of the deferred tax asset's amount", "The allowance isn't a probability-weighted share of the asset. It covers the portion that is more likely than not to go unrealized."),
         ("Write off the whole deferred tax asset, because part of the credit could expire unused", "The allowance covers only the portion more likely than not to go unrealized, not the whole asset.")],
        "A",
        """ASC 740 requires a deferred tax asset to be reduced by a valuation allowance if, based on the weight of available evidence, it is more likely than not (a likelihood of more than 50%) that some portion or all of it will not be realized. The allowance is the amount needed to reduce the asset to the amount that is more likely than not to be realized. A 55% likelihood that part of the credit will expire unused meets that threshold for that part, so Ardley records an allowance for it, and the rest of the asset is reported without one."""),
    mcq("far-subsequent-events-0009", A3, "Subsequent events", RU,
        ["ASC 855-10-25 (recognized and nonrecognized subsequent events)", "ASC 855-10-55 (examples of recognized and nonrecognized subsequent events)"],
        """Bellerby Corp.'s financial statements for the year ended December 31, Year 3, are issued on March 8, Year 4. Which of these events, each occurring in February, Year 4, should Bellerby not reflect by adjusting its Year 3 financial statements?""",
        [("A flood destroys a customer's only plant, making the customer unable to pay its December 31 balance", "Correct. The flood is a condition that arose after the balance sheet date, so it is a nonrecognized subsequent event: Bellerby discloses it if needed to keep the statements from being misleading, but doesn't adjust them."),
         ("A customer whose finances had worsened steadily all through Year 3 files for bankruptcy", "The bankruptcy confirms a condition, the customer's deteriorating finances, that existed at December 31, so the year-end allowance is adjusted."),
         ("Goods that were obsolete at year-end are sold for less than their December 31 carrying amount", "The sale gives evidence about the goods' net realizable value at December 31, so inventory is adjusted."),
         ("A lawsuit over a defect in goods sold in Year 3 is settled for more than the amount accrued at December 31", "The settlement gives evidence about a liability for a Year 3 defect that existed at December 31, so the accrued liability is adjusted to the settlement amount.")],
        "A",
        """ASC 855 distinguishes events that provide more evidence about conditions existing at the balance sheet date (recognized subsequent events, which adjust the statements) from events about conditions that arose after that date (nonrecognized subsequent events, which may need disclosure). A customer's bankruptcy caused by deterioration that existed at year-end, a sale showing that inventory was impaired at year-end, and the settlement of a lawsuit over a Year 3 defect are all recognized. A loss on a receivable caused by a customer's casualty, such as a flood, after year-end is nonrecognized."""),
    mcq("far-notes-0007", A1, "Notes to financial statements", AN,
        ["ASC 606-10-55 (consignment arrangements; contract liabilities; disaggregation of revenue)", "ASC 323-10 (equity method investments)", "ASC 460-10-30 (guarantees: initial recognition at fair value)", "ASC 410-20 (asset retirement obligations)"],
        """A senior accountant is comparing Hartlepool Co.'s draft notes with its draft December 31, Year 1, financial statements before they are issued on March 6, Year 2. The draft balance sheet shows inventories of $1,265,000; an investment in Kelso Ltd., accounted for by the equity method, of $742,000; contract liabilities of $88,000; and other noncurrent liabilities of $157,000. The draft income statement shows revenue of $6,430,000. The draft notes say: inventories, stated at the lower of FIFO cost and net realizable value, total $1,265,000, which includes $96,000 of goods that a manufacturer has placed with Hartlepool to sell on the manufacturer's behalf, paying the manufacturer only when it sells them; the investment is a 30% interest in Kelso, carried at $690,000 at January 1, plus Hartlepool's $81,000 share of Kelso's net income, less $29,000 of dividends received; revenue consists of $5,210,000 from product sales, recognized when goods are delivered, and $1,220,000 from service contracts, recognized over the contract terms, with $88,000 billed in advance for services not yet performed reported as contract liabilities; and other noncurrent liabilities consist of a $112,000 asset retirement obligation and a $45,000 liability for Hartlepool's guarantee of an unrelated supplier's bank loan, recognized at its fair value when the guarantee was issued. Which draft note reveals that the draft financial statements must be corrected?""",
        [("The inventories note", "Correct. Goods held on consignment belong to the manufacturer (the consignor), which keeps control until Hartlepool sells them. The $96,000 must come out of inventories, so the balance sheet should report $1,169,000."),
         ("The equity method investment note", "Consistent. $690,000 + $81,000 − $29,000 = $742,000. Dividends from an equity method investee reduce the investment's carrying amount."),
         ("The revenue note", "Consistent. $5,210,000 + $1,220,000 = $6,430,000, and amounts billed for services not yet performed are contract liabilities, matching the $88,000 on the balance sheet."),
         ("The other noncurrent liabilities note", "Consistent. $112,000 + $45,000 = $157,000. A guarantor recognizes a liability at the guarantee's fair value at inception.")],
        "A",
        """Each note's figures can be traced to the draft statements. Equity method: $690,000 + $81,000 − $29,000 = $742,000. Revenue: $5,210,000 + $1,220,000 = $6,430,000, and the $88,000 billed in advance agrees with contract liabilities. Other noncurrent liabilities: $112,000 + $45,000 = $157,000, and a guarantee of an unrelated party's debt is recognized at fair value at inception. The inventory note, though it agrees with the balance sheet, describes goods a manufacturer has consigned to Hartlepool: the consignor controls them until they are sold, so they are not Hartlepool's inventory, and both the note and the balance sheet must be corrected to $1,169,000."""),
]


def main():
    items = [family(*f) for f in FAMILIES] + WORD_ITEMS
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
