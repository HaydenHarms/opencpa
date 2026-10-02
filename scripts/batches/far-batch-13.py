"""FAR batch 13 — 25 items written from scratch. Built in parallel with batch 12 (a separate slice: no shared
tasks or topic slugs).

Plan: a second item on five Area I Application tasks (I.B.3c, I.B.4a, I.E.d, I.F.b, I.F.f), on four Remembering
and Understanding tasks (III.E.a, III.C.c, II.H.1b, II.F.a) and on six Area III Application tasks (III.C.e,
III.C.g, III.D.d, III.E.b, III.F.c, III.F.d), and a fifth or sixth item on the Area II Analysis subledger and
rollforward tasks (II.B.c, II.B.d x2, II.C.c, II.C.d x2, II.D.f, II.D.g, II.G.d x2). Each Analysis item changes at
least two component events against every existing item on its task and gives draft figures and supporting facts
rather than naming the errors. Target skill mix 4 / 11 / 10; area mix 5 / 12 / 8. Scope and skill tags follow
the AICPA CPA Exam Blueprints effective January 2026.

Numeric items ship with three variants each (method as in far-batch-11.py): each item is a builder, parameter
set 0 is the item and sets 1-3 are its variants, every family must move the key's letter, and parameter set 0
must show the distractor for the item's central twist (batch 11 gate).

Run: python3 scripts/batches/far-batch-13.py [--dry-run]
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import os
import re
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AN, AP, RU, attach_variants, audit, finalize, fix_articles, mcq as _mcq, variant, write_items  # noqa: E402
from variants import m, pick, rd  # noqa: E402

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 13. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
ASOF_TAX = "U.S. GAAP (ASC 740) and federal tax law in effect for 2026; the rate is as stated in the stem"


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


def family(id, area, topic, skill, refs, build, params, twist, asof=None):
    """An item built from parameter set 0, with sets 1-3 kept for its variants.

    `twist` names the pool distractor for the item's central twist; parameter set 0 must show it."""
    assert twist in params[0]["use"], f"{id}: version 0 doesn't show the central-twist distractor {twist}"
    base = build(params[0])
    review = dict(status="reviewed", references=refs, notes=NOTE)
    if asof:
        review["asOf"] = asof
    it = dict(id=id, type="mcq", blueprint=dict(section="FAR", area=area, topic=topic, skill=skill),
              review=review, **base)
    it["stem"], it["explanation"] = fix_articles(it["stem"]), fix_articles(it["explanation"])
    for c in it["choices"]:
        c["text"], c["rationale"] = fix_articles(c["text"]), fix_articles(c["rationale"])
    it["_variants"] = [build(p) for p in params[1:]]
    for k, v in enumerate([it] + it["_variants"]):
        repeats(f"{id} v{k}", v)
        spacing(f"{id} v{k}", v)
    return it


def repeats(label, v):
    """Report any dollar amount that appears more than once in a stem, or a choice that equals a stem amount.

    A repeat is fine only when it names the same fact twice; every line this prints is reviewed."""
    amts = re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", v["stem"])
    dup = sorted({a for a in amts if amts.count(a) > 1})
    if dup:
        print(f"REPEAT {label}: stem repeats {', '.join(dup)}", file=sys.stderr)
    for c in v["choices"]:
        for a in re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", c["text"]):
            if a in amts:
                print(f"REPEAT {label}: choice {a} equals a stem amount", file=sys.stderr)


def spacing(label, v):
    """Report two choices whose leading amounts are within 0.4% of each other."""
    vals = []
    for c in v["choices"]:
        mm = re.match(r"^\$?([\d,]+(?:\.\d+)?)", c["text"])
        if mm:
            vals.append(float(mm.group(1).replace(",", "")))
    vals.sort()
    for a, b in zip(vals, vals[1:]):
        if b - a < 0.004 * b:
            print(f"CLOSE {label}: {a:,.2f} and {b:,.2f}", file=sys.stderr)


def short(name):
    return name.split()[0]


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole amount, got {x}"
    return x


def distinct(pool, key):
    """No pool value may equal the key or another pool value; amounts must be positive."""
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"
    assert all(not v.startswith("$-") and not v.startswith("$0 ") and v != "$0" for v in vals), vals
    nums = [float(re.match(r"^\$?([\d,]+(?:\.\d+)?)", v).group(1).replace(",", "")) for v in vals]
    assert len(set(nums)) == len(nums), f"two choices share an amount: {vals}"


def build(pool, key, use):
    distinct({k: pool[k] for k in use}, key)
    return pick(pool, key, use)


def chg(x):
    """A signed amount as '$12,000 increase' or '$12,000 decrease'."""
    x = D(x)
    assert x != 0
    return f"{m(x)} increase" if x > 0 else f"{m(-x)} decrease"


def fu(x):
    x = D(x)
    assert x != 0
    return f"{m(abs(x))} {'favorable' if x > 0 else 'unfavorable'}"


def pc1(x):
    """A ratio as a percent rounded half up to one decimal place."""
    return f"{rd(D(x) * 100, '0.1')}%"


# ── Area I Application ───────────────────────────────────────────────────


def nfp_scf_financing(p):
    org, s = p["org"], short(p["org"])
    F = p["E"] + p["S"] - p["P"] - p["M"]
    assert F > 0
    key_v = p["E"] - p["M"] + p["R"] + p["I"]
    pool = {
        "s_keep": (m(key_v + p["S"]), f"Leaves the {m(p['S'])} from selling the donated shares in financing activities. Cash from selling donated financial assets that carried no donor restriction and were converted to cash almost at once is an operating inflow; only such proceeds that the donor restricted to long-term purposes are financing."),
        "p_keep": (m(key_v - p["P"]), f"Leaves the {m(p['P'])} paid for endowment investments in financing activities. Buying investments is an investing activity, even when the investments are held for an endowment."),
        "no_r": (m(key_v - p["R"]), f"Leaves the {m(p['R'])} building gift in operating activities. Cash gifts that donors restrict to acquiring or constructing long-lived assets are financing inflows."),
        "no_i": (m(key_v - p["I"]), f"Leaves the {m(p['I'])} of endowment income in operating activities. Investment income that donors require to be added to a donor-restricted endowment is a financing inflow, like the endowment gifts themselves."),
        "draft": (m(F), f"Accepts the draft's {m(F)}. The draft keeps the donated-share proceeds and the investment purchases in financing activities and leaves the building gift and the endowment income in operating activities."),
    }
    key = (m(key_v), f"Correct. {m(p['E'])} endowment gifts − {m(p['M'])} mortgage principal + {m(p['R'])} building gift + {m(p['I'])} endowment income added to principal.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, is reviewing its draft Year 2 statement of cash flows. The draft reports net cash provided by financing activities of {m(F)}, made up of: cash gifts that donors require {s} to hold as a permanent endowment, {m(p['E'])}; proceeds from selling shares of stock donated without restriction, which {s} sold within a few days of receipt under its policy of converting donated securities to cash at once, {m(p['S'])}; purchases of investments for the endowment, ({m(p['P'])}); and principal payments on its mortgage, ({m(p['M'])}). The draft's operating section includes a {m(p['R'])} cash gift that a donor restricted to constructing a new {p['bldg']}, and {m(p['I'])} of interest and dividends that the endowment's donors require to be added to the endowment's principal. What net cash provided by financing activities should {s}'s corrected statement report?""",
        choices, ans,
        f"""Under ASC 230-10-45-14, financing inflows of a not-for-profit entity include cash contributions, and investment income, that donors restrict to acquiring or constructing long-lived assets or to establishing or increasing a donor-restricted endowment. So the {m(p['E'])} of endowment gifts stays in financing, and the {m(p['R'])} building gift and the {m(p['I'])} of endowment income that must be added to principal move in from operating activities. Proceeds from donated securities with no donor restriction that are sold almost at once are operating inflows (ASC 230-10-45-21A), so the {m(p['S'])} moves out; purchases of investments are investing outflows, so the {m(p['P'])} moves out. Mortgage principal payments are financing. Corrected financing = {m(p['E'])} − {m(p['M'])} + {m(p['R'])} + {m(p['I'])} = {m(key_v)}.""",
    )


def nfp_endowment_note(p):
    org, s = p["org"], short(p["org"])
    draft = p["FA"] + p["GB"] + p["Q"]
    key_v = p["FA"] + p["FB"] + p["T"]
    assert p["FA"] > p["GA"] and p["FB"] < p["GB"]
    pool = {
        "old_rule": (m(key_v + p["GB"] - p["FB"]), f"Reports the Library Fund at its {m(p['GB'])} of original gifts. Before ASU 2016-14, the shortfall of an underwater endowment fund was charged to unrestricted net assets, leaving the original gift in restricted net assets; now the fund is reported in net assets with donor restrictions at its {m(p['FB'])} fair value, and the shortfall is disclosed."),
        "quasi": (m(key_v + p["Q"]), f"Keeps the {m(p['Q'])} that the board set aside. A board-designated (quasi-) endowment is without donor restrictions, because the board can reverse its own decision; the note shows it separately as a board-designated fund."),
        "no_t": (m(key_v - p["T"]), f"Leaves out the {m(p['T'])} Music Fund. A gift the donor requires to be invested for a specified term is a donor-restricted (term) endowment fund."),
        "hist": (m(key_v - (p["FA"] - p["GA"])), f"Reports the Scholarship Fund at its {m(p['GA'])} of original gifts, treating the {m(p['FA'] - p['GA'])} of appreciation as without donor restrictions. Accumulated returns on a donor-restricted endowment fund stay with donor restrictions until the board appropriates them for spending."),
        "draft": (m(draft), f"Accepts the draft's {m(draft)}, which reports the Library Fund at its original gifts, includes the board-designated investments and omits the term endowment."),
    }
    key = (m(key_v), f"Correct. {m(p['FA'])} + {m(p['FB'])} + {m(p['T'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, is reviewing the draft endowment note for its June 30, Year 2, financial statements. The note's table of endowment net assets by type of fund reports donor-restricted endowment funds of {m(draft)} and no board-designated endowment funds. That amount is the sum of: the {m(p['FA'])} fair value of the Scholarship Fund, created with gifts of {m(p['GA'])} that donors require {s} to hold in perpetuity; the {m(p['GB'])} of original gifts to the Library Fund, which donors also require {s} to hold in perpetuity and whose investments have fallen in value to {m(p['FB'])}; and investments of {m(p['Q'])} that {s}'s board voted to set aside for long-term support and may release by a later vote. The draft omits the Music Fund, a gift that its donor requires {s} to invest for {p['yrs']} years before spending it, whose investments are worth {m(p['T'])} at June 30. What amount should the corrected note report as donor-restricted endowment funds?""",
        choices, ans,
        f"""Donor-restricted endowment funds are funds a donor requires to be invested in perpetuity or for a specified term, reported in net assets with donor restrictions (ASC 958-205). The Scholarship Fund is included at its {m(p['FA'])} fair value, appreciation included, because returns stay with donor restrictions until appropriated. Since ASU 2016-14, an underwater fund is reported at its fair value in net assets with donor restrictions, so the Library Fund is {m(p['FB'])}, and the {m(p['GB'] - p['FB'])} shortfall below the original gifts is disclosed. The Music Fund is a term endowment ({m(p['T'])}). The board-designated investments are without donor restrictions and are shown as a separate, board-designated fund. Donor-restricted endowment funds = {m(p['FA'])} + {m(p['FB'])} + {m(p['T'])} = {m(key_v)}.""",
    )


def tax_basis_assets(p):
    co, s = p["co"], short(p["co"])
    key_v = p["C"] + p["ARg"] + p["Inv"] + p["Sc"] + p["K"] - p["At"]
    assert p["At"] > p["Ag"] and p["Sf"] > p["Sc"]
    pool = {
        "allow": (m(key_v - p["Al"]), f"Deducts the {m(p['Al'])} allowance for credit losses. Bad debts are deductible for tax only when specific accounts are written off, so the income tax basis carries receivables without an allowance."),
        "fv": (m(key_v + p["Sf"] - p["Sc"]), f"Reports the equity securities at their {m(p['Sf'])} fair value. For tax, the {m(p['Sf'] - p['Sc'])} unrealized gain isn't income until the shares are sold, so the securities stay at their {m(p['Sc'])} cost."),
        "gaap_dep": (m(key_v + p["At"] - p["Ag"]), f"Uses the {m(p['Ag'])} of GAAP accumulated depreciation. The income tax basis uses the depreciation taken on the tax return, {m(p['At'])} to date."),
        "dta": (m(key_v + p["DTA"]), f"Includes the {m(p['DTA'])} deferred tax asset. Statements on the income tax basis report income taxes as currently payable and recognize no deferred taxes."),
    }
    key = (m(key_v), f"Correct. {m(p['C'])} + {m(p['ARg'])} + {m(p['Inv'])} + {m(p['Sc'])} + ({m(p['K'])} − {m(p['At'])}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a C corporation that uses the accrual method for federal income tax, prepares its financial statements on the income tax basis of accounting. At December 31, Year 2, its records show these balances measured under U.S. GAAP: cash {m(p['C'])}; accounts receivable of {m(p['ARg'])} less an allowance for credit losses of {m(p['Al'])}; inventory {m(p['Inv'])}, which is also its tax basis; equity securities held as an investment, at their fair value of {m(p['Sf'])}, which cost {m(p['Sc'])}; equipment that cost {m(p['K'])} less accumulated depreciation of {m(p['Ag'])}; and a deferred tax asset of {m(p['DTA'])}. On its tax returns, {s} has taken {m(p['At'])} of depreciation on the equipment to date, most of it bonus depreciation. What total assets should {s} report in its statement of assets, liabilities, and equity—income tax basis at December 31, Year 2?""",
        choices, ans,
        f"""Income tax basis statements measure each item as the tax return does. Receivables are carried gross ({m(p['ARg'])}), because bad debts are deducted only when specific accounts are written off. The equity securities stay at their {m(p['Sc'])} cost, because gains are taxed only when realized. Equipment is cost less tax depreciation: {m(p['K'])} − {m(p['At'])} = {m(p['K'] - p['At'])}. No deferred tax asset is recognized. Total assets = {m(p['C'])} + {m(p['ARg'])} + {m(p['Inv'])} + {m(p['Sc'])} + {m(p['K'] - p['At'])} = {m(key_v)}.""",
    )


def roa(p):
    co, s = p["co"], short(p["co"])
    t = D(p["t"]) / 100
    avg = D(p["TA0"] + p["TA1"]) / 2
    num = p["NI"] + D(p["IE"]) * (1 - t)
    key_v = num / avg
    pool = {
        "no_add": (pc1(D(p["NI"]) / avg), f"Uses net income alone, {m(p['NI'])} ÷ {m(avg)}. {s} measures return on assets independently of financing, so the after-tax interest is added back."),
        "pretax_int": (pc1((p["NI"] + p["IE"]) / avg), f"Adds back all {m(p['IE'])} of interest expense. Interest reduced income taxes, so only the after-tax amount, {m(D(p['IE']) * (1 - t))}, is added back."),
        "pref": (pc1((num - p["PD"]) / avg), f"Deducts the {m(p['PD'])} of preferred dividends. They are a distribution to one class of owners; return on total assets measures the return to all providers of capital."),
        "end": (pc1(num / p["TA1"]), f"Divides by year-end total assets of {m(p['TA1'])}. {s} bases the ratio on average total assets, {m(avg)}."),
        "begin": (pc1(num / p["TA0"]), f"Divides by total assets at January 1, {m(p['TA0'])}. {s} bases the ratio on average total assets, {m(avg)}."),
    }
    key = (pc1(key_v), f"Correct. ({m(p['NI'])} + {m(p['IE'])} × (1 − {p['t']}%)) ÷ {m(avg)} = {m(num)} ÷ {m(avg)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} reports net income of {m(p['NI'])} for Year 2, after interest expense of {m(p['IE'])} and income taxes at {p['t']}% of pretax income. It declared and paid {m(p['PD'])} of dividends on its preferred stock during the year. Its total assets were {m(p['TA0'])} at January 1 and {m(p['TA1'])} at December 31. {s} measures return on assets independently of how the assets are financed, adding back interest expense net of its tax effect, and uses average total assets. What is {s}'s return on assets for Year 2, rounded to one decimal place?""",
        choices, ans,
        f"""After-tax interest = {m(p['IE'])} × (1 − {p['t']}%) = {m(D(p['IE']) * (1 - t))}. Return before financing costs = {m(p['NI'])} + {m(D(p['IE']) * (1 - t))} = {m(num)}. Average total assets = ({m(p['TA0'])} + {m(p['TA1'])}) ÷ 2 = {m(avg)}. Return on assets = {m(num)} ÷ {m(avg)} = {pc1(key_v)}. Preferred dividends are a distribution of income, not an expense, and don't enter return on total assets.""",
    )


def volume_variance(p):
    co, s = p["co"], short(p["co"])
    cm = p["p"] - p["v"] - p["sv"]
    static_oi = p["Ub"] * cm - p["F"]
    flex_oi = p["Ua"] * cm - p["F"]
    Ra = p["Ua"] * D(p["pa"])
    act_oi = Ra - p["VMa"] - p["VSa"] - p["Fa"]
    key_v = (p["Ua"] - p["Ub"]) * cm
    pool = {
        "rev": (fu((p["Ua"] - p["Ub"]) * p["p"]), f"Prices the change in units at the {m(p['p'])} selling price. That is the sales-volume variance for revenue; for operating income, each unit is worth its budgeted contribution margin of {m(cm)}."),
        "mfg": (fu((p["Ua"] - p["Ub"]) * (p["p"] - p["v"])), f"Uses a margin of {m(p['p'] - p['v'])} a unit, deducting only variable manufacturing costs. The {m(p['sv'])} of variable selling costs a unit also changes with volume, so the budgeted contribution margin is {m(cm)}."),
        "static": (fu(act_oi - static_oi), f"Compares actual operating income ({m(act_oi)}) with the static budget's ({m(static_oi)}). That is the total static-budget variance, which combines the sales-volume variance with the flexible-budget variance."),
        "flex": (fu(act_oi - flex_oi), f"Compares actual operating income ({m(act_oi)}) with the flexible budget for {p['Ua']:,} units ({m(flex_oi)}). That is the flexible-budget variance, which measures prices, costs and efficiency, not volume."),
    }
    key = (fu(key_v), f"Correct. ({p['Ua']:,} − {p['Ub']:,}) units × {m(cm)} budgeted contribution margin.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s static budget for Year 2 was based on selling {p['Ub']:,} units at {m(p['p'])} each, with variable manufacturing costs of {m(p['v'])} a unit, sales commissions of {m(p['sv'])} a unit and fixed costs of {m(p['F'])}. {s} actually sold {p['Ua']:,} units for total revenue of {m(Ra)}; its variable manufacturing costs were {m(p['VMa'])}, sales commissions {m(p['VSa'])} and fixed costs {m(p['Fa'])}. In its budget-to-actual report, what sales-volume variance for operating income should {s} show?""",
        choices, ans,
        f"""The sales-volume variance is the difference between the flexible budget for the units actually sold and the static budget, which comes down to the change in units times the budgeted contribution margin per unit. Budgeted contribution margin = {m(p['p'])} − {m(p['v'])} − {m(p['sv'])} = {m(cm)}, because sales commissions vary with units too. Variance = ({p['Ua']:,} − {p['Ub']:,}) × {m(cm)} = {fu(key_v)}. Flexible-budget operating income is {m(flex_oi)} against the static budget's {m(static_oi)}; actual operating income of {m(act_oi)} differs from the flexible budget by the flexible-budget variance, {fu(act_oi - flex_oi)}.""",
    )


# ── Area III Application ─────────────────────────────────────────────────


def contract_costs(p):
    co, s = p["co"], short(p["co"])
    mo, term, life = p["mo"], 60, 96

    def left(x, n):
        return whole(x - D(x) * mo / n)
    key_v = left(p["Cm"], term) + left(p["S"], life)
    pool = {
        "cm_life": (m(left(p["Cm"], life) + left(p["S"], life)), f"Amortizes the commission over the eight years {s} expects to serve the customer. Because the renewal will earn a commission at the same rate, the initial commission relates only to the five-year contract and is amortized over it; {m(D(p['Cm']) * mo / term)} is amortized in Year 1, not {m(D(p['Cm']) * mo / life)}."),
        "setup_term": (m(left(p["Cm"], term) + left(p["S"], term)), f"Amortizes the setup costs over the five-year contract. The setup will serve the customer through the expected renewal, so it is amortized over eight years; {m(D(p['S']) * mo / life)} is amortized in Year 1, not {m(D(p['S']) * mo / term)}."),
        "bonus": (m(key_v + left(p["B"], term)), f"Capitalizes the sales director's {m(p['B'])} bonus with the commission and amortizes it over the same five years. A bonus based on total regional sales would have been earned without this contract, so it isn't an incremental cost of obtaining it."),
        "waste": (m(key_v + left(p["W"], life)), f"Capitalizes the {m(p['W'])} cost of repeating the failed migration with the other setup costs, amortized over eight years. Costs of wasted labor and resources not reflected in the contract price are expensed as incurred."),
        "no_amort": (m(p["Cm"] + p["S"]), f"Records no amortization in Year 1. Amortization starts when the services to which the costs relate begin, on {p['start']}, Year 1."),
    }
    key = (m(key_v), f"Correct. Commission {m(p['Cm'])} × {term - mo}/{term} + setup {m(p['S'])} × {life - mo}/{life}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On {p['sd']}, Year 1, {co} signed a five-year contract to host and support a customer's online ordering system, with services running from {p['start']}, Year 1; {s} expects the customer to renew once, for three more years. {s} paid its salesperson a {m(p['Cm'])} commission owed only because the contract was signed, and will pay the salesperson a commission at the same rate on the renewal fees if the customer renews. {s}'s sales director earned a {m(p['B'])} bonus based on the region's total sales for the quarter. Before services began, {s} spent {m(p['S'] + p['W'])} setting up the customer's platform, costs that relate directly to the contract, create resources {s} will use to serve the customer for as long as it remains a customer, and are expected to be recovered; {m(p['W'])} of that amount was for repeating a data migration that failed because of an error by {s}'s staff, a cost not reflected in the contract price. {s} amortizes capitalized contract costs straight-line by month over the period to which they relate. What total contract cost assets should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""The commission is an incremental cost of obtaining the contract and is capitalized. The renewal commission is at the same rate, so it is commensurate with the initial one, and the initial commission is amortized over the five-year contract: {m(p['Cm'])} − {m(D(p['Cm']) * mo / term)} ({mo} months) = {m(left(p['Cm'], term))}. The setup costs meet the criteria for capitalizing costs to fulfill a contract (ASC 340-40-25-5), except the {m(p['W'])} of wasted labor, which is expensed (ASC 340-40-25-8). The {m(p['S'])} capitalized relates to services over the expected eight-year customer relationship: {m(p['S'])} − {m(D(p['S']) * mo / life)} = {m(left(p['S'], life))}. The bonus based on total regional sales isn't incremental to this contract and is expensed. Contract cost assets = {m(key_v)}.""",
    )


def nfp_contributions(p):
    org, s = p["org"], short(p["org"])
    pv = rd(D(p["Pa"]) * D(p["f"]))
    key_v = pv + p["E"] + p["Bf"]
    pool = {
        "face": (m(key_v + 3 * p["Pa"] - pv), f"Records the pledge at the {m(3 * p['Pa'])} total to be received. An unconditional promise to give that will be collected over more than a year is measured at the present value of the future payments, {m(pv)}."),
        "book": (m(key_v - p["E"] + p["Eb"]), f"Records the equipment at the donor's {m(p['Eb'])} carrying amount. Contributed nonfinancial assets are measured at their fair value when received, {m(p['E'])}."),
        "proceeds": (m(key_v - p["Bf"] + p["Bp"]), f"Records the bonds at the {m(p['Bp'])} {s} received when it sold them. The contribution is measured at the bonds' fair value on the date of the gift, {m(p['Bf'])}; the later difference is a {'loss' if p['Bp'] < p['Bf'] else 'gain'} on sale, not contribution revenue."),
        "will": (m(key_v + p["W"]), f"Includes the {m(p['W'])} the donor says she has left {s} in her will. A will can be changed until death, so the bequest is an intention to give, not an unconditional promise, and isn't recognized."),
    }
    key = (m(key_v), f"Correct. {m(p['Pa'])} × {p['f']} = {m(pv)}; + {m(p['E'])} + {m(p['Bf'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, received the following. On December 31, a donor signed an unconditional promise to pay {s} {m(p['Pa'])} on each December 31 of Years 2, 3 and 4; {s} measures such promises at present value using a {p['r']}% discount rate, and the present value of an ordinary annuity of 1 for three periods at {p['r']}% is {p['f']}. A local company donated {p['eq']} that {s} uses in its programs; the equipment's fair value was {m(p['E'])}, and its carrying amount in the company's records was {m(p['Eb'])}. A donor gave {s} corporate bonds with a fair value of {m(p['Bf'])} on the date of the gift, which {s} sold three weeks later for {m(p['Bp'])}. A longtime supporter told {s}'s director that she has left {s} {m(p['W'])} in her will. What total contribution revenue should {s} recognize for Year 1?""",
        choices, ans,
        f"""Contributions are measured at fair value when received (ASC 958-605-30). The pledge is unconditional and is measured at the present value of the payments: {m(p['Pa'])} × {p['f']} = {m(pv)}. The equipment is recognized at its {m(p['E'])} fair value, not the donor's carrying amount. The bonds are recognized at their {m(p['Bf'])} fair value on the date of the gift; the sale three weeks later gives a separate {'loss' if p['Bp'] < p['Bf'] else 'gain'} of {m(abs(p['Bf'] - p['Bp']))}. A bequest in a living person's will is revocable, so it isn't a promise to give. Contribution revenue = {m(pv)} + {m(p['E'])} + {m(p['Bf'])} = {m(key_v)}.""",
    )


def deferred_taxes(p):
    co, s = p["co"], short(p["co"])
    t = D(p["t"]) / 100
    WL = p["W0"] + p["We"] - p["Wp"]
    U = p["Sf"] - p["Sc"]
    dep = p["BV"] - p["TB"]
    key_v = whole((dep + U - WL) * t)
    assert key_v > 0 and WL != p["We"]
    pool = {
        "warr_exp": (m(whole((dep + U - p["We"]) * t)), f"Measures the deductible difference by the Year 2 warranty expense of {m(p['We'])}. The deferred tax asset comes from the warranty liability at year-end, {m(p['W0'])} + {m(p['We'])} − {m(p['Wp'])} = {m(WL)}, which has a tax basis of zero."),
        "muni": (m(key_v + whole(p["M"] * t)), f"Adds a deferred tax liability on the {m(p['M'])} of municipal bond interest. Tax-exempt interest is a permanent difference: it will never be taxed, so it creates no deferred tax."),
        "no_sec": (m(key_v - whole(U * t)), f"Leaves out the {m(U)} unrealized gain on the equity securities. The gain is in book income now and taxable when the shares are sold, so it is a taxable temporary difference."),
        "dtl_only": (m(key_v + whole(WL * t)), f"Reports the deferred tax liabilities without netting the {m(whole(WL * t))} deferred tax asset on the warranty liability. {s} presents deferred taxes as one net amount."),
        "warr_paid": (m(whole((dep + U - p["Wp"]) * t)), f"Measures the deductible difference by the {m(p['Wp'])} of claims paid. Claims paid have already been deducted for tax; the difference is the {m(WL)} liability still to be paid."),
    }
    key = (m(key_v), f"Correct. ({m(dep)} + {m(U)} − {m(WL)}) × {p['t']}%.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} is measuring its deferred taxes at December 31, Year 2. Its equipment has a carrying amount of {m(p['BV'])} and a tax basis of {m(p['TB'])}. Its warranty liability was {m(p['W0'])} at January 1, Year 2; during Year 2 it recognized warranty expense of {m(p['We'])} and paid claims of {m(p['Wp'])}, and warranty costs are deductible for tax when paid. It holds equity securities, measured at fair value through net income, that cost {m(p['Sc'])} and have a fair value of {m(p['Sf'])}; gains are taxable when the securities are sold. Year 2 income also includes {m(p['M'])} of interest on municipal bonds, which is exempt from tax. The enacted tax rate is {p['t']}% for all years, {s} expects ample future taxable income, and it combines its deferred tax accounts into a single net amount. What net deferred tax liability should {s} report at December 31, Year 2?""",
        choices, ans,
        f"""Taxable temporary differences: equipment {m(p['BV'])} − {m(p['TB'])} = {m(dep)}, and the unrealized gain on the securities, {m(p['Sf'])} − {m(p['Sc'])} = {m(U)}. Deductible temporary difference: the warranty liability at year-end, {m(p['W0'])} + {m(p['We'])} − {m(p['Wp'])} = {m(WL)}, whose tax basis is zero. The municipal interest is a permanent difference. Net deferred tax liability = ({m(dep)} + {m(U)} − {m(WL)}) × {p['t']}% = {m(key_v)}; no valuation allowance is needed because {s} expects ample taxable income.""",
    )


def fv_principal(p):
    co, s = p["co"], short(p["co"])
    n = p["n"]
    net1 = p["P1"] - p["T1"] - p["R1"]
    net2 = p["P2"] - p["T2"] - p["R2"]
    assert net2 > net1 and p["V1"] > p["V2"]
    key_v = n * (p["P1"] - p["R1"])
    pool = {
        "ma": (m(n * (p["P2"] - p["R2"])), f"Uses the {p['m2']}, where the price net of all costs is highest ({m(net2)} a unit). That is the most advantageous market, which is used only when there is no principal market. The {p['m1']}, with far more activity, is the principal market."),
        "tc": (m(n * net1), f"Deducts the {m(p['T1'])} of transaction costs a unit. Transaction costs are used to identify the most advantageous market but aren't deducted from the price; transport costs are."),
        "no_tr": (m(n * p["P1"]), f"Uses the {m(p['P1'])} price without deducting the {m(p['R1'])} a unit to transport the {p['asset']} to the {p['m1']}. Location is a characteristic of the asset, so transport costs are deducted."),
        "ma_net": (m(n * net2), f"Uses the {p['m2']} and deducts both its transaction and transport costs. The {p['m1']} is the principal market, and transaction costs are not deducted from the price in any case."),
    }
    key = (m(key_v), f"Correct. {n} × ({m(p['P1'])} − {m(p['R1'])}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} acquired {n} identical used {p['asset']} as part of a group of assets and must measure their fair value under ASC 820 to allocate the purchase price. {s} can access two markets for {p['asset']} like these at the measurement date. In the {p['m1']}, about {p['V1']:,} of them change hands each year at {m(p['P1'])} each; selling costs (commissions) are {m(p['T1'])} a unit, and transporting them there would cost {m(p['R1'])} a unit. In the {p['m2']}, about {p['V2']:,} change hands each year at {m(p['P2'])} each; fees are {m(p['T2'])} a unit, and transporting them there would cost {m(p['R2'])} a unit. What is the fair value of the {n} {p['asset']}?""",
        choices, ans,
        f"""Fair value is measured in the principal market, the market with the greatest volume and level of activity for the asset, when one exists, even if another market would give a better price. The {p['m1']} ({p['V1']:,} a year) is the principal market. The price there is reduced by transport costs, because location is a characteristic of the asset, but not by transaction costs, which belong to the transaction rather than the asset (ASC 820-10-35-9B and 35-9C). Fair value = {n} × ({m(p['P1'])} − {m(p['R1'])}) = {m(key_v)}. The {p['m2']}'s higher net price ({m(net2)} against {m(net1)}) would matter only if there were no principal market.""",
    )


def lease_liability(p):
    co, s = p["co"], short(p["co"])
    i = D(p["i"]) / 100

    def liab(pay):
        L0 = rd(D(pay) * D(p["AD6"]))
        bal = L0 - pay
        return L0, bal, bal + rd(bal * i)
    L0, bal, key_v = liab(p["P"])
    _, _, excl = liab(p["P"] - p["M"])
    pool = {
        "cpi": (m(rd(D(p["P2"]) * D(p["AD5"]))), f"Remeasures the liability for the higher Year 2 payment: {m(p['P2'])} × {p['AD5']}. A change in a payment tied to an index is variable lease cost when it occurs; the liability isn't remeasured for it unless it is remeasured for another reason."),
        "no_int": (m(bal), f"Deducts the first payment but accrues no interest for Year 1. The liability accretes at {p['i']}% on the {m(bal)} balance: {m(rd(bal * i))}."),
        "excl": (m(excl), f"Leaves the {m(p['M'])} maintenance charge out of the lease payments. {s} elected not to separate lease and nonlease components for this class of asset, so the whole {m(p['P'])} payment is a lease payment."),
        "no_pay": (m(L0 + rd(L0 * i)), f"Accrues interest on the full {m(L0)} without deducting the {m(p['P'])} paid at commencement. That payment reduced the liability at once."),
    }
    key = (m(key_v), f"Correct. ({m(L0)} − {m(p['P'])}) × 1.{p['i']:0>2}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} leased {p['asset']} for six years and classified the lease as a finance lease. Payments are due each January 1, starting at commencement. The first payment is {m(p['P'])}, of which {m(p['M'])} is for maintenance the lessor performs; {s} has elected not to separate lease and nonlease components for this class of asset. Each later payment is adjusted for the change in the consumer price index, and in December, Year 1, the lessor told {s} that the January 1, Year 2, payment will be {m(p['P2'])}. The rate implicit in the lease isn't readily determinable, and {s}'s incremental borrowing rate is {p['i']}%. Present value factors at {p['i']}% for an annuity due are {p['AD6']} for six periods and {p['AD5']} for five periods. Rounding each computation to the nearest dollar, what carrying amount of the lease liability should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""Lease payments include variable payments that depend on an index, measured using the index at commencement, and, because {s} combines lease and nonlease components, the maintenance charge: {m(p['P'])} a year. Initial liability = {m(p['P'])} × {p['AD6']} = {m(L0)}. The first payment, made at commencement, reduces it to {m(bal)}. Interest for Year 1 = {m(bal)} × {p['i']}% = {m(rd(bal * i))}, so the liability at December 31 is {m(key_v)}. The CPI increase to {m(p['P2'])} is recognized as variable lease cost in Year 2 and doesn't remeasure the liability (ASC 842-10-35-5).""",
    )


def lease_cost(p):
    co, s = p["co"], short(p["co"])
    fm = p["fm"]
    sl = whole(D(p["R"]) * (60 - fm) / 5)
    var = whole(D(p["pct"]) / 100 * (p["S"] - p["Th"]))
    st = p["Ms"] * p["k"]
    key_v = sl + var + st
    assert p["S"] > p["Th"]
    pool = {
        "cash": (m(p["R"] * (12 - fm) + var + st), f"Uses the {m(p['R'] * (12 - fm))} of rent paid in Year 1. An operating lease's fixed payments, free months included, are recognized straight-line over the lease term: {m(p['R'] * (60 - fm))} ÷ 5 = {m(sl)} a year."),
        "nofree": (m(p["R"] * 12 + var + st), f"Recognizes twelve months of rent at {m(p['R'])} as if there were no free months. Total fixed payments are {60 - fm} months' rent, {m(p['R'] * (60 - fm))}, spread evenly over the five years."),
        "no_var": (m(key_v - var), f"Leaves out the {m(var)} of percentage rent. Variable payments based on sales aren't in the lease liability, but they are lease cost in the period the obligation is incurred."),
        "var_all": (m(key_v + whole(D(p["pct"]) / 100 * p["Th"])), f"Takes {p['pct']}% of all {m(p['S'])} of sales. Rent is owed only on sales above {m(p['Th'])}."),
        "no_st": (m(key_v - st), f"Leaves out the {m(st)} of forklift rent. A short-term lease isn't on the balance sheet, but its cost is recognized straight-line over its term and is part of total lease cost."),
    }
    key = (m(key_v), f"Correct. {m(sl)} straight-line + {m(var)} variable + {m(st)} short-term.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} began a five-year lease of retail space, which it classifies as an operating lease. Rent is {m(p['R'])} a month, except that no rent is due for the first {p['fmw']} months. {s} also pays the landlord {p['pct']}% of its annual sales at the location above {m(p['Th'])}; Year 1 sales there were {m(p['S'])}. On {p['sd']}, Year 1, {s} rented a forklift for {p['kw']} months at {m(p['Ms'])} a month, and it has elected the short-term lease exemption for that class of asset. What total lease cost should {s} recognize for Year 1?""",
        choices, ans,
        f"""Operating lease cost for the fixed payments is recognized straight-line over the lease term (ASC 842-20-25-6): {60 - fm} months × {m(p['R'])} = {m(p['R'] * (60 - fm))} ÷ 5 = {m(sl)} a year, free months included. Variable payments based on sales are excluded from the lease liability and recognized as incurred: {p['pct']}% × ({m(p['S'])} − {m(p['Th'])}) = {m(var)}. The forklift is a short-term lease, recognized straight-line over its term: {p['k']} × {m(p['Ms'])} = {m(st)}. Total lease cost = {m(key_v)}.""",
    )


# ── Area II Analysis ─────────────────────────────────────────────────────


def ar_rollforward(p):
    co, s = p["co"], short(p["co"])
    tax = whole(D(p["Rv"]) * p["t"] / 100)
    E = p["B"] + p["Rv"] - p["Cc"] - p["Wo"]
    key_v = p["B"] + p["Rv"] + tax - (p["Cc"] - p["Dp"]) - p["Wo"] - p["F"]
    pool = {
        "no_tax": (m(key_v - tax), f"Leaves out the {m(tax)} of sales tax billed. Customers owe the tax along with the price, so the receivables include it, even though the tax is a liability, not revenue."),
        "dep": (m(key_v - p["Dp"]), f"Treats the {m(p['Dp'])} of deposits as collections of receivables. Advance payments for orders not yet shipped are contract liabilities; they don't reduce receivables."),
        "fact": (m(key_v + p["F"]), f"Leaves the {m(p['F'])} of factored receivables in the control account. They were sold without recourse and {s} kept no involvement, so they are derecognized; the cash is not a borrowing."),
        "draft": (m(E), f"Accepts the draft's {m(E)}, which omits the sales tax billed, counts the deposits as collections and keeps the factored receivables."),
    }
    key = (m(key_v), f"Correct. {m(p['B'])} + {m(p['Rv'])} + {m(tax)} − ({m(p['Cc'])} − {m(p['Dp'])}) − {m(p['Wo'])} − {m(p['F'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s staff prepared this Year 2 rollforward of the accounts receivable control account: January 1 balance {m(p['B'])}; plus credit sales {m(p['Rv'])}; less cash collected from customers {m(p['Cc'])}; less accounts written off {m(p['Wo'])}; December 31 balance {m(E)}. All of {s}'s sales are on account. The controller compares the schedule with the supporting records. The credit sales figure is sales revenue from the income statement; every invoice also charged the customer {p['t']}% sales tax, which {s} records as a liability until it remits it. The cash collected is the total of the customer receipts column, which includes {m(p['Dp'])} of deposits that customers paid in December on orders {s} will ship in Year 3. In November, {s} sold {m(p['F'])} of receivables to a factor without recourse, for {m(p['Fp'])} in cash, keeping no involvement with them; the factored accounts were closed in the subledger, but the general ledger recorded the cash as a short-term borrowing and left the receivables in the control account. What balance should the corrected rollforward show for accounts receivable, before any allowance, at December 31, Year 2?""",
        choices, ans,
        f"""Billings to customers include the sales tax: {m(p['Rv'])} × {p['t']}% = {m(tax)} is added. The deposits are contract liabilities, not collections of receivables, so collections fall to {m(p['Cc'] - p['Dp'])}. The factored receivables were sold (a transfer without recourse with no continuing involvement), so the {m(p['F'])} comes out of receivables; the {m(p['F'] - p['Fp'])} difference from the cash received is a loss, and the borrowing is reversed. Corrected balance = {m(p['B'])} + {m(p['Rv'] + tax)} − {m(p['Cc'] - p['Dp'])} − {m(p['Wo'])} − {m(p['F'])} = {m(key_v)}.""",
    )


def ar_recon_report(p):
    co, s = p["co"], short(p["co"])
    C = p["C"]
    GL = C + p["Emp"] - p["Fc"]
    Sub = C + p["Emp"] + p["Lb"]
    pool = {
        "emp": (m(C + p["Emp"]), f"Keeps the {m(p['Emp'])} relocation advance in trade receivables. A loan to an employee, repaid through payroll, isn't a receivable from a customer; it is reported separately as another receivable."),
        "fc": (m(C - p["Fc"]), f"Leaves out the {m(p['Fc'])} of finance charges billed to customers. They are owed by customers and are in the subledger; the general ledger entry is missing."),
        "lb": (m(C + p["Lb"]), f"Leaves the {m(p['Lb'])} of December 31 lockbox receipts in customer balances. The cash was received at year-end and is in the general ledger; the subledger posting was simply late."),
        "mis": (m(C - p["X"]), f"Deducts the {m(p['X'])} payment posted to the wrong customer. The payment is in both records, credited to the wrong account in the subledger, so moving it between accounts doesn't change the total."),
        "gl": (m(GL), f"Accepts the control account's {m(GL)}, which includes the relocation advance and lacks the finance charges."),
        "sub": (m(Sub), f"Accepts the subledger's {m(Sub)}, which includes the relocation advance and the receipts received in the lockbox at year-end."),
    }
    key = (m(C), f"Correct. Control account {m(GL)} − {m(p['Emp'])} + {m(p['Fc'])}; subledger {m(Sub)} − {m(p['Emp'])} − {m(p['Lb'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Tracing differences between its records at December 31, {s}'s controller finds: in November, {s} advanced {m(p['Emp'])} to its operations manager for relocation costs, repayable through payroll deductions during Year 2, and recorded the advance in the control account and in a subledger account opened in the manager's name; finance charges of {m(p['Fc'])} on overdue customer accounts were added to the customers' subledger accounts in December, but no general ledger entry was made; customer remittances of {m(p['Lb'])} received in {s}'s bank lockbox on December 31 were recorded in the general ledger from the bank's report but not posted to the customers' accounts until January 2; and a {m(p['X'])} payment from {p['c1']} was credited to the account of {p['c2']}. Before these items are addressed, the accounts receivable subledger totals {m(Sub)} and the general ledger control account shows {m(GL)}. What amount should {s} report as trade accounts receivable, before any allowance, at December 31?""",
        choices, ans,
        f"""Work out which record each finding affects. The relocation advance is in both records but isn't a trade receivable, so it comes out of both: − {m(p['Emp'])}. The finance charges are owed by customers and are missing only from the control account: + {m(p['Fc'])}. The lockbox receipts reduce customer balances, and only the subledger is missing them: − {m(p['Lb'])} from the subledger. The misposted payment moves an amount between two customer accounts and doesn't change the subledger total. Control account: {m(GL)} − {m(p['Emp'])} + {m(p['Fc'])} = {m(C)}. Subledger: {m(Sub)} − {m(p['Emp'])} − {m(p['Lb'])} = {m(C)}.""",
    )


def ar_recon_subledger(p):
    co, s = p["co"], short(p["co"])
    adj = -p["Ec"] + p["Bt"] - p["So"]
    C = p["C"]
    Sub = C - adj
    GL = C + p["Ec"] - p["Cs"]
    pool = {
        "cs": (chg(adj + p["Cs"]), f"Also adds the {m(p['Cs'])} of cash sales to the subledger. The cash sales were wrongly credited to the control account, but no customer account was touched, so only the general ledger needs that correction."),
        "cut": (chg(adj + p["Ec"]), f"Leaves the {m(p['Ec'])} invoice for goods shipped in January in the subledger. The goods hadn't left {s}'s dock at December 31, so there was no sale or receivable in Year 2, and both records must remove it."),
        "so": (chg(adj + p["So"]), f"Leaves the {m(p['So'])} settled against {s}'s payable in {p['c1']}'s subledger account. The settlement extinguished that part of the receivable; only the general ledger has recorded it."),
        "bt": (chg(adj - p["Bt"]), f"Leaves out the {m(p['Bt'])} batch of invoices posted only to the control account. The sales were made and billed, so the customers' subledger accounts must be charged."),
        "gl": (chg(-p["Ec"] + p["Cs"]), f"Gives the adjustment the control account needs (remove the {m(p['Ec'])} early invoice, restore the {m(p['Cs'])} wrongly credited), not the subledger's."),
    }
    key = (chg(adj), f"Correct. − {m(p['Ec'])} + {m(p['Bt'])} − {m(p['So'])}; the subledger becomes {m(C)}, which agrees with the corrected control account.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Events the controller traces into {co}'s accounts receivable records: on December 29, Year 2, a sales journal batch totaling {m(p['Bt'])} was posted to the general ledger control account, but its invoices were never posted to the customers' accounts; on December 30, a {m(p['Ec'])} invoice was recorded as a sale in both records, but the goods, sold FOB shipping point, were not shipped until January 3; during December, {s} agreed with {p['c1']}, which is both a customer and a supplier, to settle {m(p['So'])} of {p['c1']}'s balance against an equal amount {s} owed it, and the general ledger recorded the settlement (debit accounts payable, credit accounts receivable) but the customer's subledger account did not; and also in December, {m(p['Cs'])} of cash sales was entered in the accounts receivable column of the cash receipts journal, so its total was credited to the control account. At December 31, Year 2, before these items are corrected, the subledger totals {m(Sub)} and the control account shows {m(GL)}. By what net amount must {s} change its subledger total so that it shows the correct balance?""",
        choices, ans,
        f"""The early invoice is in both records and must come out of both (− {m(p['Ec'])}): the goods, sold FOB shipping point, hadn't shipped, so control hadn't passed. The December 29 batch is missing from the subledger (+ {m(p['Bt'])}). The settlement against the payable is missing from the subledger (− {m(p['So'])}). The cash sales error affects only the control account, which must be debited back {m(p['Cs'])}. Subledger change = − {m(p['Ec'])} + {m(p['Bt'])} − {m(p['So'])} = {chg(adj)}, to {m(C)}. Control account: {m(GL)} − {m(p['Ec'])} + {m(p['Cs'])} = {m(C)}, so the records agree.""",
    )


def inv_rollforward(p):
    co, s = p["co"], short(p["co"])
    E = p["B"] + p["P"] - p["C"]
    nrv = p["SP"] - p["CS"]
    wd = p["Lc"] - nrv
    floor = nrv - p["NP"]
    assert wd > 0 and p["RC"] < floor
    key_v = E + p["D"] - p["Df"] + p["G"] - wd
    pool = {
        "lcm": (m(key_v - p["NP"]), f"Writes the {p['line']} down to {m(floor)}, net realizable value less the normal profit margin, the market floor under the lower of cost or market rule. A FIFO entity measures inventory at the lower of cost and net realizable value, {m(nrv)}, since ASU 2015-11."),
        "dfr": (m(key_v + p["Df"]), f"Keeps the {m(p['Df'])} of second-time freight in inventory. Double freight is an abnormal cost, expensed as incurred, not a cost of bringing the goods to their location."),
        "duty": (m(key_v - p["D"]), f"Leaves the {m(p['D'])} of customs duties expensed. Import duties are part of the cost of acquiring the goods, and all the goods are still on hand."),
        "transit": (m(key_v - p["G"]), f"Leaves out the {m(p['G'])} of goods in transit. They were shipped FOB shipping point on December 29, so {s} owned them at year-end."),
        "nowd": (m(key_v + wd), f"Leaves the {p['line']} at cost. Their net realizable value is {m(p['SP'])} − {m(p['CS'])} = {m(nrv)}, below their {m(p['Lc'])} cost, so they are written down by {m(wd)}."),
        "rc": (m(key_v - (nrv - p["RC"])), f"Writes the {p['line']} down to their {m(p['RC'])} replacement cost. Replacement cost doesn't enter the lower of cost and net realizable value test."),
    }
    key = (m(key_v), f"Correct. {m(E)} + {m(p['D'])} − {m(p['Df'])} + {m(p['G'])} − {m(wd)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, which uses FIFO and a perpetual inventory system, prepared this Year 2 inventory rollforward from its perpetual records: January 1 balance {m(p['B'])}; purchases {m(p['P'])}; cost of goods sold ({m(p['C'])}); December 31 balance {m(E)}. The controller's review finds: customs duties of {m(p['D'])} paid on imported goods, all still on hand at December 31, were charged to expense; a supplier's delivery went to the wrong city, and the {m(p['Df'])} {s} paid to ship the goods a second time to its warehouse was added to their cost (the goods are on hand); goods costing {m(p['G'])}, shipped by a supplier FOB shipping point on December 29 and received January 5, are not in the records; and the December 31 balance includes {p['line']} costing {m(p['Lc'])}, which {s} expects to sell for {m(p['SP'])} after {m(p['CS'])} of selling costs, whose current replacement cost is {m(p['RC'])} and on which {s}'s normal profit margin is {m(p['NP'])}. What inventory should the corrected rollforward report at December 31, Year 2?""",
        choices, ans,
        f"""Duties are part of the cost of acquiring the goods (+ {m(p['D'])}). Double freight is an abnormal cost, expensed (ASC 330-10-30-7) (− {m(p['Df'])}). Goods shipped FOB shipping point belong to {s} once shipped (+ {m(p['G'])}). A FIFO entity measures inventory at the lower of cost and net realizable value: NRV = {m(p['SP'])} − {m(p['CS'])} = {m(nrv)}, so the {p['line']} are written down by {m(p['Lc'])} − {m(nrv)} = {m(wd)}; replacement cost and the normal profit margin are irrelevant. Corrected inventory = {m(E)} + {m(p['D'])} − {m(p['Df'])} + {m(p['G'])} − {m(wd)} = {m(key_v)}.""",
    )


def inv_recon_report(p):
    co, s = p["co"], short(p["co"])
    C = p["C"]
    Sub = C - p["T"] - p["A"]
    GL = C - p["A"] + p["Sh"] + p["Fo"]
    pool = {
        "approval": (m(C - p["A"]), f"Treats the {m(p['A'])} of goods on approval as sold. The customer may return them with no obligation to buy, so control hasn't passed until it accepts them or the period ends; they are still {s}'s inventory."),
        "transit": (m(C - p["T"]), f"Leaves out the {m(p['T'])} of goods moving between {s}'s own warehouses. They were removed from one location's records and not yet added to the other's, but {s} owns them."),
        "shrink": (m(C + p["Sh"]), f"Keeps the {m(p['Sh'])} of goods the cycle count found missing. The subledger wrote them off; the general ledger must too."),
        "fo": (m(C + p["Fo"]), f"Keeps the {m(p['Fo'])} of freight on deliveries to customers in inventory. Freight-out is a selling cost, not a cost of inventory."),
        "gl": (m(GL), f"Accepts the general ledger's {m(GL)}. It lacks the shrinkage write-off, includes the freight-out and treats the goods on approval as sold."),
        "sub": (m(Sub), f"Accepts the subledger's {m(Sub)}. It omits the goods in transit between warehouses and the goods on approval."),
    }
    key = (m(C), f"Correct. Subledger {m(Sub)} + {m(p['T'])} + {m(p['A'])}; general ledger {m(GL)} + {m(p['A'])} − {m(p['Sh'])} − {m(p['Fo'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{s}'s staff accountant prepared a draft schedule reconciling the perpetual inventory subledger, {m(Sub)} at December 31, to the general ledger inventory account, {m(GL)}. The controller finds the draft: accepted both records' treatment, as sold, of {m(p['A'])} of goods sent on December 22 to a customer that may examine them and return them by January 21 with no obligation to buy; didn't pick up {m(p['T'])} of goods shipped on December 30 from {s}'s {p['w1']} warehouse to its {p['w2']} warehouse, arriving January 3, which the subledger had removed from the {p['w1']} warehouse's records but not yet added to the {p['w2']} warehouse's; omitted from the general ledger a December cycle count's write-off of {m(p['Sh'])} of goods found missing, which the subledger had already recorded; and left {m(p['Fo'])} of freight paid in December to deliver goods to customers debited to inventory in the general ledger. What amount should {s} report as inventory at December 31?""",
        choices, ans,
        f"""Subledger: the goods between warehouses are still {s}'s (+ {m(p['T'])}), and the goods on approval haven't been sold, because the customer hasn't accepted them and the return period hasn't ended (+ {m(p['A'])}): {m(Sub)} + {m(p['T'])} + {m(p['A'])} = {m(C)}. General ledger: + {m(p['A'])} for the goods on approval, − {m(p['Sh'])} for the shrinkage and − {m(p['Fo'])} for the freight-out, a selling cost: {m(GL)} + {m(p['A'])} − {m(p['Sh'])} − {m(p['Fo'])} = {m(C)}. Inventory = {m(C)}.""",
    )


def inv_recon_cogs(p):
    co, s = p["co"], short(p["co"])
    mk = p["SPr"] - p["Cr"]
    adj = -p["K"] + mk + p["WD"]
    C = p["C"]
    Sub = C - p["K"] + p["BH"]
    GL = C - p["K"] + mk + p["WD"]
    pool = {
        "cons": (chg(adj + p["K"]), f"Leaves the {m(p['K'])} of goods at {p['dealer']} in cost of goods sold. The dealer sells them on {s}'s behalf and returns any it doesn't sell, so {s} still controls them; they go back into inventory, reducing cost of goods sold."),
        "ret": (chg(adj - mk), f"Ignores the return recorded at selling price. The general ledger credited cost of goods sold for {m(p['SPr'])} instead of the goods' {m(p['Cr'])} cost, understating it by {m(mk)}."),
        "wd": (chg(adj - p["WD"]), f"Records the {m(p['WD'])} write-down in the general ledger without charging cost of goods sold. {s} reports write-downs in cost of goods sold, so it rises by {m(p['WD'])}."),
        "bh": (chg(adj - p["BH"]), f"Treats the {m(p['BH'])} of goods held for the customer as {s}'s inventory, reversing their cost of goods sold. The customer asked for the arrangement and controls the goods, which are set aside for it and ready to ship, so the sale stands; only the subledger needs correcting."),
    }
    key = (chg(adj), f"Correct. − {m(p['K'])} consigned goods + {m(mk)} return error + {m(p['WD'])} write-down.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, Year 2, {co}'s perpetual inventory subledger totals {m(Sub)}. {s} reports inventory write-downs in cost of goods sold. The controller's investigation finds: goods costing {m(p['K'])} that {s} shipped in December to {p['dealer']}, a retailer that sells them on {s}'s behalf and returns any it doesn't sell, were removed from both records and charged to cost of goods sold; goods that a customer returned on December 18, which had been sold for {m(p['SPr'])} and cost {m(p['Cr'])}, were restored to the subledger at cost, but the general ledger entry debited inventory and credited cost of goods sold at the selling price; a {m(p['WD'])} write-down of obsolete goods to net realizable value was recorded in the subledger but not in the general ledger; and goods costing {m(p['BH'])} that a customer bought in December and asked {s} to hold until its new store opens in February, which are tagged with the customer's name, ready to ship and can't be used to fill other orders, were removed from the general ledger as sold but are still listed in the subledger. {s}'s general ledger inventory account shows {m(GL)} at December 31, Year 2. What net adjustment to {s}'s Year 2 cost of goods sold results from these findings?""",
        choices, ans,
        f"""Consigned goods remain {s}'s inventory until the dealer sells them, so {m(p['K'])} comes back into inventory in both records and out of cost of goods sold. The return should have restored the goods at cost: the general ledger credited cost of goods sold {m(mk)} too much, so cost of goods sold rises by {m(mk)} and the general ledger inventory falls by the same amount. The write-down is missing from the general ledger and is charged to cost of goods sold: + {m(p['WD'])}. The bill-and-hold sale stands (the customer requested it, the goods are identified as the customer's, ready to ship and can't be redirected), so only the subledger must remove the goods; cost of goods sold is unaffected. Net adjustment = − {m(p['K'])} + {m(mk)} + {m(p['WD'])} = {chg(adj)}.""",
    )


def ppe_rollforward_ad(p):
    co, s = p["co"], short(p["co"])
    AD1 = p["AD0"] + p["Dx"] - p["Dd"]
    press_x = whole(D(p["Pc"]) / p["n"] * (12 - p["mo"]) / 12)
    land = whole(D(p["L"]) / 40)
    li = whole(D(p["LI"]) / p["rem"] - D(p["LI"]) / 15)
    dA = whole(D(p["Tc"]) / 60 * p["tm"])
    key_v = AD1 - press_x - land + li
    pool = {
        "press": (m(key_v + press_x), f"Keeps the full year of depreciation on the {p['line']}. It was placed in service on {p['date']}, so only {p['mo']} months ({m(whole(D(p['Pc']) / p['n'] * p['mo'] / 12))}) are recorded."),
        "land": (m(key_v + land), f"Keeps the {m(land)} of depreciation on the {m(p['L'])} assigned to land. Land isn't depreciated, so the building's depreciation is ({m(p['Bc'])} − {m(p['L'])}) ÷ 40."),
        "li": (m(key_v - li), f"Keeps the leasehold improvements on their 15-year physical life. Improvements to a leased asset are depreciated over the shorter of their useful life and the remaining lease term, {p['rem']} years here."),
        "truck": (m(key_v + dA), f"Records the {m(dA)} of Year 2 depreciation on the truck sold but removes only its January 1 accumulated depreciation. The disposal must also remove that {m(dA)}, so the two corrections cancel."),
    }
    key = (m(key_v), f"Correct. {m(AD1)} − {m(press_x)} − {m(land)} + {m(li)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s staff prepared this Year 2 rollforward of accumulated depreciation: January 1 balance {m(p['AD0'])}; depreciation expense {m(p['Dx'])}; disposals ({m(p['Dd'])}); December 31 balance {m(AD1)}. The controller reviews the depreciation schedule and finds: a {p['line']} that cost {m(p['Pc'])}, placed in service on {p['date']}, Year 2, received a full year of depreciation over its {p['n']}-year life with no residual value; a building bought on January 2, Year 2, for {m(p['Bc'])}, of which an appraisal assigned {m(p['L'])} to the land, was depreciated on the whole {m(p['Bc'])} over 40 years with no residual value; improvements costing {m(p['LI'])} that {s} made on January 2, Year 2, to a warehouse it leases, whose lease ends in {p['rem']} years with no renewal or purchase option, were depreciated over their 15-year physical life; and a truck that cost {m(p['Tc'])}, depreciated straight-line over five years with no residual value, was sold on {p['tdate']}, Year 2, and the disposal entry removed its accumulated depreciation at January 1 without recording any depreciation on it for Year 2. {s} depreciates straight-line by month. What accumulated depreciation should the corrected rollforward report at December 31, Year 2?""",
        choices, ans,
        f"""The {p['line']} is depreciated for {p['mo']} months, not 12: − {m(press_x)}. The land portion of the building isn't depreciable: − {m(p['L'])} ÷ 40 = − {m(land)}. The leasehold improvements are depreciated over the {p['rem']}-year remaining lease term: {m(p['LI'])} ÷ {p['rem']} − {m(p['LI'])} ÷ 15 = + {m(li)}. The truck needs {m(dA)} of depreciation for {p['tm']} months, which increases accumulated depreciation, and the disposal must then remove that amount too, so the ending balance is unchanged (depreciation expense and the loss on sale change instead). Corrected balance = {m(AD1)} − {m(press_x)} − {m(land)} + {m(li)} = {m(key_v)}.""",
    )


def ppe_recon_dep(p):
    co, s = p["co"], short(p["co"])
    ci = whole(D(p["Ci"]) / p["n"] * 6 / 12)
    idle = whole(D(p["Ip"]) * p["im"] / 12)
    extra = p["Fm"] * 3
    correct = p["X"]
    Ds = correct + p["c1"] - ci - idle
    Dg = correct + extra
    pool = {
        "cip": (m(correct + p["c1"]), f"Keeps the {m(p['c1'])} of depreciation on the wing still under construction. Depreciation begins when an asset is ready for its intended use; construction in progress isn't depreciated."),
        "idle": (m(correct - idle), f"Suspends depreciation on the press for the {p['im']} idle months. An asset that is temporarily idle continues to be depreciated: its full {m(p['Ip'])} is recorded."),
        "int": (m(correct - ci), f"Depreciates the machine without the {m(p['Ci'])} of capitalized interest. Interest capitalized during construction is part of the asset's cost, adding {m(ci)} of depreciation for six months."),
        "gl": (m(Dg), f"Accepts the general ledger's {m(Dg)}, which includes {m(extra)} of depreciation on the forklift for the three months after it was sold."),
        "sub": (m(Ds), f"Accepts the subledger's {m(Ds)}, which depreciates construction in progress, leaves out the capitalized interest and suspends depreciation on the idle press."),
    }
    key = (m(correct), f"Correct. Subledger {m(Ds)} − {m(p['c1'])} + {m(ci)} + {m(idle)}; general ledger {m(Dg)} − {m(extra)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s fixed-asset subledger shows Year 2 depreciation of {m(Ds)}, while its general ledger shows depreciation expense of {m(Dg)}. {s} depreciates its assets straight-line by month. The controller's investigation finds: the subledger recorded {m(p['c1'])} of depreciation on the costs to date of a warehouse wing still under construction at December 31, while the general ledger recorded none; {m(p['Ci'])} of interest capitalized during the construction of a machine {s} built for its own use, placed in service on July 1, Year 2, with a {p['n']}-year life and no residual value, is in the machine's cost in the general ledger but not in the subledger; the subledger suspended depreciation on a press for the {p['im']} months it stood idle during a temporary drop in orders, while the general ledger recorded the press's full annual depreciation of {m(p['Ip'])}; and a forklift sold on September 30 was removed from the subledger at that date, but the general ledger kept recording its depreciation of {m(p['Fm'])} a month through December. What depreciation expense should {s} report for Year 2?""",
        choices, ans,
        f"""Subledger: remove the {m(p['c1'])} on construction in progress, which isn't depreciated until it is ready for use; add depreciation on the capitalized interest, {m(p['Ci'])} ÷ {p['n']} × 6/12 = {m(ci)}; and add the {p['im']} idle months on the press, {m(p['Ip'])} × {p['im']}/12 = {m(idle)}, because a temporarily idle asset is still depreciated: {m(Ds)} − {m(p['c1'])} + {m(ci)} + {m(idle)} = {m(correct)}. General ledger: remove the forklift's depreciation after the sale, 3 × {m(p['Fm'])} = {m(extra)}: {m(Dg)} − {m(extra)} = {m(correct)}.""",
    )


def ap_recon_report(p):
    co, s = p["co"], short(p["co"])
    C = p["C"]
    net = whole(D(p["list"]) * (100 - p["td"]) / 100)
    TD = p["list"] - net
    Sub = C + p["PO"]
    GL = C + p["PO"] - p["V"] + TD
    pool = {
        "po": (m(C + p["PO"]), f"Keeps the {m(p['PO'])} purchase order. {s} owes nothing until the supplier ships the goods (FOB shipping point), so an order is a commitment, not a liability."),
        "void": (m(C - p["V"]), f"Leaves the {m(p['V'])} voided check as a payment. The check was cancelled, so the supplier is still owed; the void reinstates the payable."),
        "td": (m(C + TD), f"Uses the {m(p['list'])} list price. A trade discount reduces the invoice price itself; the amount owed is {m(net)}."),
        "mis": (m(C - p["X"]), f"Deducts the {m(p['X'])} payment posted to the wrong supplier. It is in both records, credited to the wrong account in the subledger, so the total is unaffected."),
        "gl": (m(GL), f"Accepts the control account's {m(GL)}, which keeps the purchase order, omits the reinstated payable and carries the invoice at list price."),
    }
    key = (m(C), f"Correct. Subledger {m(Sub)} − {m(p['PO'])}; control account {m(GL)} − {m(p['PO'])} + {m(p['V'])} − {m(TD)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Reviewing {s}'s accounts payable at December 31, the controller finds: a {m(p['PO'])} purchase order issued on December 28, for goods the supplier will ship FOB shipping point in mid-January, was entered as an invoice in both records; a {m(p['V'])} check to a supplier, recorded as a payment in both records on December 27, was voided on December 30 because it was made out for the wrong amount, and the void was posted to the supplier's subledger account but not to the general ledger; an invoice for goods received on December 20 was posted to the supplier's subledger account at its net amount of {m(net)}, after a {p['td']}% trade discount, but to the general ledger at its list price of {m(p['list'])}; and a {m(p['X'])} payment to {p['v1']} was posted to {p['v2']}'s subledger account. Before these items are corrected, the subledger totals {m(Sub)} and the control account shows {m(GL)}. What amount should {s} report as accounts payable at December 31?""",
        choices, ans,
        f"""The purchase order is in both records but isn't a liability until the goods ship: − {m(p['PO'])} from both. The voided check means the supplier is still owed; the subledger has reinstated the payable, the control account must too (+ {m(p['V'])}). A trade discount is a reduction of price, so the invoice is owed at {m(net)}; the control account is overstated by {m(TD)}. The misposted payment moves an amount between two supplier accounts. Subledger: {m(Sub)} − {m(p['PO'])} = {m(C)}. Control account: {m(GL)} − {m(p['PO'])} + {m(p['V'])} − {m(TD)} = {m(C)}.""",
    )


def ap_recon_income(p):
    co, s = p["co"], short(p["co"])
    usd0 = whole(D(p["E"]) * D(p["r0"]))
    usd1 = whole(D(p["E"]) * D(p["r1"]))
    fx = usd1 - usd0
    assert fx > 0
    adj = -fx + p["A"] - p["U"]
    C = p["C"]
    Sub = C - fx - p["U"]
    GL = C - fx + p["A"] - p["V"] - p["U"]
    pool = {
        "no_fx": (chg(adj + fx), f"Leaves the euro invoice at the invoice-date rate. A payable in a foreign currency is remeasured at the year-end rate; the euro rose, so the payable grows by {m(fx)}, a transaction loss."),
        "fx_sign": (chg(adj + 2 * fx), f"Records the {m(fx)} remeasurement as a gain. The euro rose, so {s} owes more dollars: it is a loss."),
        "van": (chg(adj - p["V"]), f"Charges the {m(p['V'])} van to expense. The van is equipment; recording its invoice in the general ledger adds an asset and a payable, and it wasn't in service in Year 2, so no depreciation is due."),
        "no_rev": (chg(adj - p["A"]), f"Ignores the unreversed accrual. Because the Year 1 accrual stayed in the control account, recording the invoice in Year 2 charged consulting expense a second time; removing it raises Year 2 income by {m(p['A'])}."),
        "no_u": (chg(adj + p["U"]), f"Leaves out the {m(p['U'])} advertising invoice. The advertising ran in December, so it is a Year 2 expense and liability even though the invoice was unrecorded."),
    }
    key = (chg(adj), f"Correct. − {m(fx)} transaction loss + {m(p['A'])} duplicate expense − {m(p['U'])} advertising.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, Year 1, {co} recorded a {m(p['A'])} accrual for consulting services received in December (debit consulting expense, credit accounts payable); the entry was never reversed, and the consultant's invoice was then recorded as consulting expense through accounts payable in both records in January, Year 2. During December, Year 2, a German contractor billed {s} €{p['E']:,} for repair work, payable in euros in February; {s} recorded the invoice in both records at {m(D(p['r0']))} per euro, the rate on the invoice date, though the rate at December 31 is {m(D(p['r1']))}. Also in December, Year 2, a {m(p['U'])} advertising invoice for ads that ran that month was found in the unmatched-invoice file and has not been recorded in either record; and, on December 30, Year 2, a {m(p['V'])} invoice for a delivery van received that day and placed in service in January was posted to the dealer's subledger account but not to the general ledger. At December 31, Year 2, before these items are corrected, {s}'s accounts payable subledger totals {m(Sub)} and its general ledger control account shows {m(GL)}. By how much does {s}'s Year 2 pretax income change when these findings are corrected?""",
        choices, ans,
        f"""The euro payable is remeasured at the year-end rate: €{p['E']:,} × ({m(D(p['r1']))} − {m(D(p['r0']))}) = {m(fx)} more owed, a foreign-currency transaction loss (ASC 830-20-35-1), in both records. The unreversed accrual left the Year 1 liability in the control account, so the January invoice charged consulting expense twice; removing the duplicate cuts Year 2 expense and the control account by {m(p['A'])}. The van invoice is added to the control account with the van as equipment; no expense arises in Year 2. The advertising invoice is a Year 2 expense and payable in both records: − {m(p['U'])}. Pretax income changes by − {m(fx)} + {m(p['A'])} − {m(p['U'])} = {chg(adj)}.""",
    )


FAMILIES = [
    # ── Area I Application ──
    ("far-nfp-cash-flows-0005", A1, "Statement of cash flows (Not-for-Profit)", AP,
     ["ASC 230-10-45-14 (financing inflows: contributions and investment income restricted to long-lived assets or to a donor-restricted endowment)", "ASC 230-10-45-21A (proceeds from donated financial assets sold almost immediately: operating unless restricted to long-term purposes)", "ASC 958-230 (not-for-profit statement of cash flows)"],
     nfp_scf_financing, [
        dict(org="Mevagissey Health Clinic", E=480000, S=72000, P=410000, M=95000, R=315000, I=38000, bldg="clinic building", use=["no_i", "p_keep", "no_r"]),
        dict(org="Lostwithiel Arts Center", E=360000, S=54000, P=305000, M=70000, R=240000, I=29000, bldg="gallery wing", use=["no_r", "s_keep", "draft"]),
        dict(org="Padstow Youth League", E=620000, S=93000, P=540000, M=120000, R=410000, I=47000, bldg="sports hall", use=["s_keep", "no_r", "draft"]),
        dict(org="Bodmin Hospice Trust", E=270000, S=41000, P=228000, M=52000, R=185000, I=22000, bldg="day-care wing", use=["p_keep", "no_r", "draft"]),
     ], "no_i"),
    ("far-nfp-notes-0002", A1, "Notes to financial statements (Not-for-Profit)", AP,
     ["ASC 958-205-50 (endowment disclosures: net asset composition by type of fund; underwater funds)", "ASC 958-205-45 (underwater endowment funds reported in net assets with donor restrictions, as amended by ASU 2016-14)", "ASC 958-205-20 (glossary: donor-restricted endowment fund, including term endowments; board-designated quasi-endowment)"],
     nfp_endowment_note, [
        dict(org="Helston Learning Trust", GA=1200000, FA=1465000, GB=800000, FB=712000, Q=540000, T=250000, yrs="ten", use=["old_rule", "quasi", "draft"]),
        dict(org="Marazion College Fund", GA=900000, FA=1086000, GB=650000, FB=574000, Q=410000, T=190000, yrs="eight", use=["no_t", "old_rule", "quasi"]),
        dict(org="Porthleven Scholars Trust", GA=1500000, FA=1742000, GB=1100000, FB=968000, Q=620000, T=310000, yrs="twelve", use=["no_t", "hist", "old_rule"]),
        dict(org="Zennor Heritage Fund", GA=700000, FA=846000, GB=500000, FB=441000, Q=320000, T=150000, yrs="five", use=["hist", "old_rule", "quasi"]),
     ], "old_rule"),
    ("far-income-tax-basis-0001", A1, "Special Purpose Frameworks", AP,
     ["AICPA AU-C 800 (financial statements prepared in accordance with a special purpose framework: income tax basis)", "IRC §§ 166, 168 and 1001 (specific charge-off of bad debts, tax depreciation, gain realized on sale) as applied in income tax basis statements"],
     tax_basis_assets, [
        dict(co="Fowey Marine Supply Co.", C=146000, ARg=388000, Al=23000, Inv=512000, Sc=94000, Sf=131000, K=860000, Ag=318000, At=497000, DTA=52000, use=["fv", "gaap_dep", "dta"]),
        dict(co="Mousehole Chandlery Co.", C=98000, ARg=262000, Al=15000, Inv=347000, Sc=61000, Sf=88000, K=590000, Ag=214000, At=341000, DTA=36000, use=["allow", "fv", "gaap_dep"]),
        dict(co="Polperro Fabrication Co.", C=203000, ARg=541000, Al=32000, Inv=716000, Sc=128000, Sf=179000, K=1210000, Ag=446000, At=698000, DTA=57000, use=["allow", "dta", "gaap_dep"]),
        dict(co="Tintagel Print Works Co.", C=71000, ARg=194000, Al=11000, Inv=256000, Sc=46000, Sf=65000, K=430000, Ag=157000, At=249000, DTA=33000, use=["fv", "dta", "gaap_dep"]),
     ], "fv"),
    ("far-ratios-0007", A1, "Financial Statement Ratios and Performance Metrics", AP,
     ["Financial statement analysis: profitability ratios (return on total assets, with interest added back net of tax)"],
     roa, [
        dict(co="Launceston Corp.", NI=1140000, IE=360000, t=25, PD=150000, TA0=11600000, TA1=12500000, use=["no_add", "pretax_int", "pref"]),
        dict(co="Liskeard Corp.", NI=820000, IE=240000, t=21, PD=90000, TA0=8200000, TA1=8800000, use=["pretax_int", "begin", "pref"]),
        dict(co="Saltash Corp.", NI=2150000, IE=520000, t=25, PD=300000, TA0=18900000, TA1=20300000, use=["no_add", "pref", "end"]),
        dict(co="Callington Corp.", NI=640000, IE=210000, t=25, PD=60000, TA0=6100000, TA1=6700000, use=["pretax_int", "begin", "end"]),
     ], "pretax_int"),
    ("far-budget-variance-0002", A1, "Financial Statement Ratios and Performance Metrics", AP,
     ["Budget-versus-actual analysis: static budget, flexible budget and sales-volume variances"],
     volume_variance, [
        dict(co="Camelford Tools Co.", Ub=40000, Ua=36500, p=85, v=41, sv=7, F=880000, pa="88", VMa=1551250, VSa=255500, Fa=905000, use=["mfg", "rev", "static"]),
        dict(co="Redruth Pumps Co.", Ub=25000, Ua=27200, p=120, v=58, sv=9, F=760000, pa="117", VMa=1604800, VSa=244800, Fa=772000, use=["rev", "static", "mfg"]),
        dict(co="Camborne Valves Co.", Ub=60000, Ua=54800, p=64, v=29, sv=5, F=1150000, pa="66", VMa=1654960, VSa=274000, Fa=1138000, use=["static", "flex", "rev"]),
        dict(co="Hayle Fittings Co.", Ub=18000, Ua=19900, p=150, v=72, sv=12, F=640000, pa="146", VMa=1452700, VSa=238800, Fa=655000, use=["static", "flex", "mfg"]),
     ], "mfg"),
    # ── Area III Application ──
    ("far-revenue-contract-costs-0003", A3, "Revenue recognition", AP,
     ["ASC 340-40-25-1 to 25-4 (incremental costs of obtaining a contract)", "ASC 340-40-25-5 to 25-8 (costs to fulfill a contract; wasted resources expensed)", "ASC 340-40-35-1 (amortization consistent with the transfer of the goods or services, including anticipated contracts)"],
     contract_costs, [
        dict(co="Perranporth Systems Co.", sd="February 20", start="April 1", mo=9, Cm=96000, S=192000, W=28800, B=12000, use=["cm_life", "bonus", "waste"]),
        dict(co="Newquay Data Co.", sd="May 12", start="July 1", mo=6, Cm=72000, S=153600, W=19200, B=9000, use=["setup_term", "cm_life", "waste"]),
        dict(co="Boscastle Cloud Co.", sd="January 15", start="March 1", mo=10, Cm=124800, S=230400, W=34560, B=15600, use=["setup_term", "bonus", "waste"]),
        dict(co="Wadebridge Hosting Co.", sd="June 2", start="August 1", mo=5, Cm=86400, S=172800, W=23040, B=10800, use=["bonus", "waste", "no_amort"]),
     ], "cm_life"),
    ("far-nfp-contributions-0002", A3, "Revenue recognition", AP,
     ["ASC 958-605-25 (unconditional promises to give; intentions to give, such as revocable bequests, not recognized)", "ASC 958-605-30 (contributions measured at fair value; promises to give at present value)", "ASC 958-320 (gains and losses on investments after receipt)"],
     nfp_contributions, [
        dict(org="Gorran Animal Rescue", Pa=60000, r=5, f="2.7232", E=48000, Eb=21000, eq="kennel equipment", Bf=125000, Bp=119500, W=250000, use=["face", "book", "proceeds"]),
        dict(org="Mullion Wildlife Trust", Pa=45000, r=4, f="2.7751", E=36000, Eb=14500, eq="a boat and outboard motor", Bf=92000, Bp=98800, W=180000, use=["book", "face", "will"]),
        dict(org="Coverack Lifeboat Fund", Pa=80000, r=6, f="2.6730", E=64000, Eb=29000, eq="rescue equipment", Bf=170000, Bp=184000, W=400000, use=["face", "will", "proceeds"]),
        dict(org="Porthcurno Heritage Society", Pa=50000, r=5, f="2.7232", E=42000, Eb=17500, eq="display cases", Bf=108000, Bp=102500, W=150000, use=["book", "face", "will"]),
     ], "face"),
    ("far-income-taxes-deferred-0003", A3, "Accounting for income taxes", AP,
     ["ASC 740-10-25 (temporary differences; permanent differences such as tax-exempt interest)", "ASC 740-10-30 (measurement at the enacted rate)", "ASC 740-10-45 (deferred taxes presented as one net noncurrent amount per jurisdiction)"],
     deferred_taxes, [
        dict(co="Constantine Corp.", t=25, BV=1840000, TB=1236000, W0=58000, We=94000, Wp=71000, Sc=210000, Sf=286000, M=40000, use=["warr_exp", "no_sec", "dtl_only"]),
        dict(co="Mylor Corp.", t=21, BV=1250000, TB=890000, W0=42000, We=61000, Wp=55000, Sc=150000, Sf=201000, M=30000, use=["muni", "dtl_only", "warr_exp"]),
        dict(co="Feock Corp.", t=25, BV=2620000, TB=1980000, W0=77000, We=128000, Wp=84000, Sc=300000, Sf=392000, M=56000, use=["muni", "dtl_only", "warr_paid"]),
        dict(co="Probus Corp.", t=25, BV=960000, TB=652000, W0=31000, We=52000, Wp=39000, Sc=88000, Sf=124000, M=20000, use=["no_sec", "warr_exp", "dtl_only"]),
     ], "warr_exp", ASOF_TAX),
    ("far-fair-value-techniques-0002", A3, "Fair value measurements", AP,
     ["ASC 820-10-35-5 and 35-5A (principal market; most advantageous market only when there is no principal market)", "ASC 820-10-35-9B and 35-9C (transaction costs not deducted; transport costs deducted when location is a characteristic)"],
     fv_principal, [
        dict(co="Grampound Civil Co.", n=24, asset="excavators", m1="dealer market", m2="online auction market", V1=1900, V2=260, P1=86000, T1=4300, R1=1800, P2=91000, T2=2700, R2=3100, use=["ma", "tc", "no_tr"]),
        dict(co="Tregony Haulage Co.", n=15, asset="tractor units", m1="auction market", m2="dealer network", V1=3400, V2=420, P1=58000, T1=2900, R1=1600, P2=63500, T2=1800, R2=2600, use=["ma", "no_tr", "ma_net"]),
        dict(co="Veryan Forestry Co.", n=40, asset="forwarder trailers", m1="dealer market", m2="regional auction", V1=1250, V2=180, P1=31000, T1=1550, R1=700, P2=33400, T2=900, R2=1300, use=["tc", "ma", "no_tr"]),
        dict(co="Portscatho Plant Hire Co.", n=12, asset="crawler cranes", m1="broker market", m2="online auction market", V1=640, V2=95, P1=212000, T1=10600, R1=5400, P2=224000, T2=6700, R2=8100, use=["tc", "ma", "ma_net"]),
     ], "ma"),
    ("far-lessee-finance-0003", A3, "Lessee accounting", AP,
     ["ASC 842-10-30-5 (lease payments: variable payments that depend on an index, measured at the commencement-date index)", "ASC 842-10-15-37 (practical expedient: not separating lease and nonlease components)", "ASC 842-10-35-5 (remeasurement for index changes only when remeasured for another reason)", "ASC 842-20-30-1 and 842-20-35-1 (initial and subsequent measurement of the lease liability)"],
     lease_liability, [
        dict(co="Ludgvan Bakeries Co.", asset="a commercial oven line", P=84000, M=9000, P2=86100, i=6, AD6="5.2124", AD5="4.4651", use=["cpi", "no_int", "excl"]),
        dict(co="Madron Print Co.", asset="a digital press", P=126000, M=14000, P2=129780, i=7, AD6="5.1002", AD5="4.3872", use=["no_pay", "cpi", "excl"]),
        dict(co="Morvah Dairy Co.", asset="a milking system", P=58000, M=6500, P2=59450, i=5, AD6="5.3295", AD5="4.5460", use=["cpi", "no_pay", "no_int"]),
        dict(co="Pendeen Mining Co.", asset="a rock crusher", P=97000, M=11000, P2=99910, i=8, AD6="4.9927", AD5="4.3121", use=["no_int", "excl", "no_pay"]),
     ], "cpi"),
    ("far-lessee-operating-0005", A3, "Lessee accounting", AP,
     ["ASC 842-20-25-6 (operating lease cost: straight-line single lease cost; variable lease payments recognized when incurred)", "ASC 842-20-25-2 (short-term lease election: cost recognized straight-line over the term)", "ASC 842-20-50-4 (total lease cost includes short-term and variable lease cost)"],
     lease_cost, [
        dict(co="Botallack Outdoor Co.", R=14500, fm=6, fmw="six", pct=3, S=3860000, Th=3000000, sd="May 1", k=8, kw="eight", Ms=2400, use=["cash", "no_var", "no_st"]),
        dict(co="Crantock Surf Co.", R=9800, fm=4, fmw="four", pct=2, S=3400000, Th=2200000, sd="June 1", k=7, kw="seven", Ms=1900, use=["cash", "no_var", "nofree"]),
        dict(co="Cubert Garden Co.", R=21000, fm=3, fmw="three", pct=4, S=5150000, Th=4400000, sd="April 1", k=9, kw="nine", Ms=3100, use=["nofree", "var_all", "cash"]),
        dict(co="Polzeath Board Co.", R=7600, fm=6, fmw="six", pct=5, S=1880000, Th=1500000, sd="March 1", k=10, kw="ten", Ms=1450, use=["cash", "no_var", "var_all"]),
     ], "cash"),
    # ── Area II Analysis ──
    ("far-receivables-rollforward-0005", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "ASC 860-10-40 (sales of financial assets: derecognition of receivables factored without recourse)", "ASC 606-10-45-2 (contract liabilities: payments received before performance)", "ASC 606-10-32-2A (sales taxes collected from customers excluded from revenue)"],
     ar_rollforward, [
        dict(co="Delabole Slate Supply Co.", B=618000, Rv=4250000, t=6, Cc=4236000, Dp=46000, Wo=29000, F=180000, Fp=172800, use=["no_tax", "dep", "draft"]),
        dict(co="Davidstow Creamery Supply Co.", B=455000, Rv=3120000, t=5, Cc=3088000, Dp=38000, Wo=21000, F=130000, Fp=124800, use=["fact", "no_tax", "draft"]),
        dict(co="Altarnun Timber Co.", B=812000, Rv=5680000, t=7, Cc=5602000, Dp=63000, Wo=37000, F=240000, Fp=231600, use=["fact", "dep", "no_tax"]),
        dict(co="Bolventor Feed Co.", B=346000, Rv=2480000, t=6, Cc=2452000, Dp=27000, Wo=16000, F=96000, Fp=92200, use=["draft", "dep", "no_tax"]),
     ], "no_tax"),
    ("far-receivables-reconciliation-0005", A2, "Trade receivables", AN,
     ["ASC 310-10-45 (receivables from officers and employees reported separately from trade receivables)", "Subsidiary ledger and control account reconciliation practice (finance charges; lockbox receipts; misposted payments)"],
     ar_recon_report, [
        dict(co="Pensilva Wholesale Co.", C=936450, Emp=18000, Fc=4275, Lb=31600, X=7820, c1="Trematon Stores", c2="Millbrook Grocers", use=["emp", "fc", "lb"]),
        dict(co="Menheniot Wholesale Co.", C=712380, Emp=12500, Fc=3160, Lb=24850, X=15600, c1="Kingsand Market", c2="Cawsand Provisions", use=["fc", "mis", "emp"]),
        dict(co="Herodsfoot Wholesale Co.", C=1184600, Emp=22400, Fc=5380, Lb=38900, X=9270, c1="Duloe Farm Shop", c2="Lanreath Stores", use=["lb", "sub", "gl"]),
        dict(co="Pelynt Wholesale Co.", C=548720, Emp=9600, Fc=2470, Lb=19350, X=8800, c1="Lansallos Store", c2="Polruan Chandlery", use=["mis", "emp", "sub"]),
     ], "emp"),
    ("far-receivables-reconciliation-0006", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "ASC 606-10-25-30 (transfer of control: FOB shipping point)", "ASC 405-20 (extinguishment of a liability; settlement of a receivable against a payable by agreement)", "Subsidiary ledger and control account reconciliation practice (unposted batches; journal coding errors)"],
     ar_recon_subledger, [
        dict(co="Golant Packaging Co.", C=842300, Ec=23400, Bt=64250, So=14900, Cs=8650, c1="Tywardreath Mills", use=["cut", "cs", "gl"]),
        dict(co="Lanlivery Packaging Co.", C=615900, Ec=31800, Bt=26400, So=12700, Cs=7300, c1="Luxulyan Quarries", use=["so", "cs", "cut"]),
        dict(co="Stenalees Packaging Co.", C=1036700, Ec=28600, Bt=77900, So=18400, Cs=10900, c1="Nanpean Clay Works", use=["bt", "cut", "so"]),
        dict(co="Ladock Packaging Co.", C=488200, Ec=12900, Bt=41300, So=9800, Cs=5100, c1="Tresillian Boatyard", use=["gl", "cs", "cut"]),
     ], "cut"),
    ("far-inventory-rollforward-0005", A2, "Inventory", AN,
     ["ASC 330-10-30 (inventory cost: import duties; abnormal costs such as double freight expensed)", "ASC 330-10-35-1B (lower of cost and net realizable value for FIFO, as amended by ASU 2015-11)", "ASC 606-10-25-30 (transfer of control: FOB shipping point)"],
     inv_rollforward, [
        dict(co="Chacewater Imports Co.", B=742000, P=5384000, C=5291000, D=26400, Df=18700, G=33500, line="patio heaters", Lc=96000, SP=88000, CS=7200, RC=64500, NP=11000, use=["lcm", "transit", "duty"]),
        dict(co="Mithian Imports Co.", B=516000, P=3912000, C=3851000, D=31200, Df=13400, G=41000, line="garden lanterns", Lc=68000, SP=62500, CS=5100, RC=44000, NP=12400, use=["lcm", "transit", "dfr"]),
        dict(co="Goonhavern Imports Co.", B=1028000, P=7466000, C=7342000, D=37800, Df=46100, G=46900, line="wood stoves", Lc=134000, SP=123000, CS=10100, RC=88000, NP=19500, use=["lcm", "nowd", "dfr"]),
        dict(co="Zelah Imports Co.", B=388000, P=2874000, C=2829000, D=14600, Df=9800, G=17900, line="camping stoves", Lc=52000, SP=47500, CS=3900, RC=33000, NP=6400, use=["transit", "rc", "nowd"]),
     ], "lcm"),
    ("far-inventory-reconciliation-0005", A2, "Inventory", AN,
     ["ASC 330-10 (inventory; goods in transit between locations; freight-out is a selling cost)", "ASC 606-10-55-85 to 55-88 (customer acceptance: products delivered for trial or evaluation)"],
     inv_recon_report, [
        dict(co="Summercourt Housewares Co.", C=1426300, T=21850, A=48200, Sh=18460, Fo=24340, w1="east", w2="west", use=["approval", "transit", "sub"]),
        dict(co="Mitchell Housewares Co.", C=982400, T=17600, A=29300, Sh=15850, Fo=34920, w1="north", w2="south", use=["approval", "shrink", "fo"]),
        dict(co="Topsham Housewares Co.", C=1874500, T=36400, A=70700, Sh=21300, Fo=41800, w1="city", w2="harbor", use=["approval", "transit", "fo"]),
        dict(co="Shaldon Housewares Co.", C=654800, T=12900, A=19600, Sh=14700, Fo=29300, w1="riverside", w2="airport", use=["transit", "shrink", "fo"]),
     ], "approval"),
    ("far-inventory-reconciliation-0006", A2, "Inventory", AN,
     ["ASC 330-10 (inventory; write-down to net realizable value)", "ASC 606-10-55-79 to 55-80 (consignment arrangements)", "ASC 606-10-55-81 to 55-84 (bill-and-hold arrangements)"],
     inv_recon_cogs, [
        dict(co="Budleigh Tableware Co.", C=1082000, K=41600, SPr=29400, Cr=18900, WD=17300, BH=22700, dealer="Sidmouth Interiors", use=["cons", "ret", "wd"]),
        dict(co="Exmouth Tableware Co.", C=846000, K=28900, SPr=33600, Cr=21500, WD=24600, BH=17800, dealer="Dawlish Home Store", use=["ret", "bh", "wd"]),
        dict(co="Teignmouth Tableware Co.", C=1267000, K=18300, SPr=41200, Cr=26800, WD=32700, BH=36900, dealer="Paignton Home Store", use=["ret", "bh", "wd"]),
        dict(co="Brixham Tableware Co.", C=693000, K=14700, SPr=26800, Cr=17100, WD=21500, BH=15900, dealer="Totnes Living", use=["ret", "wd", "cons"]),
     ], "cons"),
    ("far-ppe-rollforward-0005", A2, "Property, plant and equipment", AN,
     ["ASC 360-10-35 (depreciation: from the date placed in service; land not depreciated)", "ASC 842-20-35-12 (leasehold improvements amortized over the shorter of useful life and remaining lease term)", "ASC 360-10-40 (derecognition: accumulated depreciation through the date of sale removed)"],
     ppe_rollforward_ad, [
        dict(co="Kingsbridge Foods Co.", AD0=2846000, Dx=612000, Dd=95000, line="packaging line", Pc=480000, n=8, mo=3, date="October 1", Bc=1950000, L=550000, LI=270000, rem=5, Tc=150000, tm=7, tdate="July 31", use=["truck", "press", "li"]),
        dict(co="Salcombe Boats Co.", AD0=1934000, Dx=418000, Dd=66000, line="moulding press", Pc=360000, n=6, mo=8, date="May 1", Bc=1380000, L=520000, LI=216000, rem=4, Tc=180000, tm=10, tdate="October 31", use=["li", "land", "truck"]),
        dict(co="Totnes Joinery Co.", AD0=3512000, Dx=744000, Dd=105000, line="CNC router", Pc=495000, n=6, mo=4, date="September 1", Bc=2400000, L=720000, LI=330000, rem=6, Tc=240000, tm=9, tdate="September 30", use=["press", "land", "truck"]),
        dict(co="Ashburton Mills Co.", AD0=1468000, Dx=326000, Dd=61600, line="bottling line", Pc=288000, n=6, mo=2, date="November 1", Bc=990000, L=290000, LI=150000, rem=3, Tc=180000, tm=4, tdate="April 30", use=["li", "press", "truck"]),
     ], "truck"),
    ("far-ppe-reconciliation-0005", A2, "Property, plant and equipment", AN,
     ["ASC 360-10-35 (depreciation; temporarily idle assets continue to be depreciated; construction in progress not depreciated until ready for its intended use)", "ASC 835-20 (capitalized interest is part of the asset's cost)"],
     ppe_recon_dep, [
        dict(co="Chagford Metalworks Co.", X=1284600, c1=23500, Ci=120000, n=10, Ip=72000, im=4, Fm=1150, use=["idle", "cip", "int"]),
        dict(co="Lustleigh Castings Co.", X=936400, c1=17800, Ci=60000, n=12, Ip=48000, im=3, Fm=2400, use=["idle", "cip", "gl"]),
        dict(co="Widecombe Forge Co.", X=1642800, c1=31200, Ci=120000, n=8, Ip=96000, im=5, Fm=1900, use=["idle", "int", "sub"]),
        dict(co="Hatherleigh Steel Co.", X=758200, c1=14600, Ci=48000, n=10, Ip=36000, im=6, Fm=1250, use=["cip", "gl", "sub"]),
     ], "idle"),
    ("far-payables-reconciliation-0004", A2, "Payables and accrued liabilities", AN,
     ["ASC 405-10 (liabilities)", "ASC 440-10 (purchase commitments are not liabilities until performance)", "Subsidiary ledger and control account reconciliation practice (voided checks; trade discounts; misposted payments)"],
     ap_recon_report, [
        dict(co="Okehampton Builders Supply Co.", C=684920, PO=38500, V=12640, list=54000, td=15, X=6275, v1="Lydford Timber", v2="Tavistock Fixings", use=["po", "void", "td"]),
        dict(co="Crediton Builders Supply Co.", C=512340, PO=27800, V=9460, list=36000, td=20, X=4185, v1="Tiverton Steel", v2="Cullompton Glass", use=["void", "mis", "po"]),
        dict(co="Honiton Builders Supply Co.", C=938460, PO=52300, V=17280, list=72000, td=10, X=8640, v1="Ottery Brickworks", v2="Moretonhampstead Timber", use=["po", "td", "gl"]),
        dict(co="Bideford Builders Supply Co.", C=426780, PO=21400, V=7920, list=30000, td=12, X=3540, v1="Appledore Slate", v2="Torrington Fixings", use=["void", "mis", "td"]),
     ], "po"),
    ("far-payables-reconciliation-0005", A2, "Payables and accrued liabilities", AN,
     ["ASC 830-20-35-1 (foreign-currency payables remeasured at the current rate; transaction gains and losses in income)", "ASC 405-10 (liabilities)", "Subsidiary ledger and control account reconciliation practice (unreversed accruals; unposted invoices; unrecorded liabilities)"],
     ap_recon_income, [
        dict(co="Clovelly Engineering Co.", C=773400, E=150000, r0="1.08", r1="1.11", A=26800, V=47600, U=11850, use=["no_fx", "van", "no_rev"]),
        dict(co="Hartland Engineering Co.", C=598200, E=120000, r0="1.06", r1="1.10", A=31200, V=38900, U=6300, use=["no_rev", "van", "no_fx"]),
        dict(co="Morwenstow Engineering Co.", C=1046500, E=200000, r0="1.09", r1="1.12", A=19400, V=61200, U=27800, use=["fx_sign", "no_fx", "no_u"]),
        dict(co="Holsworthy Engineering Co.", C=452900, E=90000, r0="1.07", r1="1.12", A=22600, V=29800, U=5400, use=["no_rev", "no_fx", "fx_sign"]),
     ], "no_fx"),
]

WORD_ITEMS = [
    mcq("far-fair-value-approaches-0001", A3, "Fair value measurements", RU,
        ["ASC 820-10-35 (valuation techniques: market, cost and income approaches)", "ASC 820-10-55 (cost approach: current replacement cost, adjusted for obsolescence)"],
        """Trevose Co. must measure the fair value of a custom molding press that it obtained in an asset acquisition; no prices exist for identical or similar used presses. Its appraiser estimates what it would cost a market participant buyer to obtain a substitute press of comparable utility, and then deducts amounts for physical deterioration and for functional and economic obsolescence. How should this measurement be described under ASC 820?""",
        [("It is a cost approach measurement of fair value", "Correct. The cost approach reflects the amount that would be required currently to replace the asset's service capacity (current replacement cost). A market participant seller would receive no more than a buyer would pay to obtain a substitute of comparable utility, adjusted for obsolescence."),
         ("It is a market approach measurement, because it estimates a buyer's price", "The market approach uses prices and other information from market transactions in identical or comparable assets, and there are none here. Estimating what it would cost a buyer to obtain a substitute asset is the cost approach."),
         ("It is an income approach measurement, as obsolescence lowers future cash flows", "The income approach converts future amounts, such as cash flows or earnings, to a single discounted amount. Deducting obsolescence from the cost of a substitute is an adjustment within the cost approach."),
         ("It isn't a fair value measurement, since fair value is an exit price and this is a cost", "Fair value is an exit price, but ASC 820 permits estimating it by current replacement cost: from a market participant seller's view, the price received is based on what a buyer would pay for a substitute of comparable utility.")],
        "A",
        """ASC 820 recognizes three valuation approaches: the market approach (prices from transactions in identical or comparable assets), the income approach (discounting future amounts) and the cost approach (the amount that would be required currently to replace the asset's service capacity, often called current replacement cost). The cost approach estimates what a market participant buyer would pay to acquire or construct a substitute asset of comparable utility, adjusted for physical deterioration and functional and economic obsolescence, which is what the appraiser did. It is a way of estimating the exit price, so it is a fair value measurement. Because the inputs are the entity's estimates rather than observable prices, the measurement would typically fall in Level 3 of the hierarchy."""),
    mcq("far-nfp-agent-transfers-0002", A3, "Revenue recognition", RU,
        ["ASC 958-605-25-23 to 25-26 (recipient entity acting as an agent, trustee or intermediary; variance power)", "ASC 958-605-25 (contributions with donor restrictions)", "ASC 958-605-30 (contributed financial assets measured at fair value)"],
        """During Year 2, Gwennap Community Foundation, a not-for-profit entity, receives four gifts, each worth $45,000. Which one should Gwennap report as a liability rather than as contribution revenue?""",
        [("A gift the donor directs to Polgooth Food Pantry, an unrelated charity, giving Gwennap no power to redirect it", "Correct. Gwennap accepted the cash to pass on to a beneficiary the donor specified, with no power to redirect it, and it isn't financially interrelated with the pantry. It acts as an agent: it records the cash and a liability to the pantry."),
         ("A gift the donor directs to Polgooth Food Pantry, while explicitly granting Gwennap the unilateral power to redirect it to another charity", "When the donor explicitly grants the recipient variance power, the unilateral power to redirect the gift to another beneficiary, the recipient has received a contribution and recognizes revenue."),
         ("A gift the donor restricts to Gwennap's own youth sports program for the next two seasons", "A gift for Gwennap's own program is a contribution to Gwennap. The donor's purpose and time limits make it contribution revenue with donor restrictions, not a liability."),
         ("Listed shares given to Gwennap with no restriction, which it sells two days later", "Shares given without restriction are a contribution, recognized at their fair value when received. Selling them soon afterward doesn't change that.")],
        "A",
        """Under ASC 958-605-25-23 to 25-26, a recipient entity that accepts assets from a donor and agrees to transfer them to a beneficiary the donor specifies acts as an agent or intermediary. It recognizes the assets and an equal liability to the beneficiary, not contribution revenue. Two exceptions make the transfer a contribution to the recipient: the donor explicitly grants it variance power (the unilateral power to redirect the assets), or the recipient and the beneficiary are financially interrelated. Gifts for the recipient's own programs, with or without donor restrictions, and gifts of securities are contributions."""),
    mcq("far-troubled-debt-restructuring-0002", A2, "Debt (Notes and bonds payable)", RU,
        ["ASC 470-60-15 (scope: what is and isn't a troubled debt restructuring for a debtor)", "ASC 470-60-55 (concession: decrease in the debtor's effective borrowing rate)", "ASU 2022-02 (eliminated troubled debt restructuring recognition and measurement for creditors; debtors' guidance in ASC 470-60 unchanged)"],
        """Treliske Co. has missed several payments on a bank loan, and its lender has concluded that Treliske can't meet the loan's original terms. ASU 2022-02 removed the troubled debt restructuring guidance for creditors, but debtors still apply ASC 470-60. From Treliske's perspective as the debtor, which of the following would NOT be a troubled debt restructuring?""",
        [("Treliske transfers equipment whose fair value equals the loan's carrying amount, in full settlement", "Correct. A debtor that settles a debt by transferring assets whose fair value at least equals the debt's carrying amount has received no concession, so this isn't a troubled debt restructuring even though Treliske is in financial difficulty. Treliske derecognizes the loan and recognizes a gain or loss on the equipment for the difference between its fair value and carrying amount."),
         ("The lender cuts the rate from 9% to 6% for the rest of the term and forgives the accrued interest", "Lowering the rate and forgiving interest because the debtor can't pay lowers the debtor's effective borrowing rate: the lender has granted a concession, so this is a troubled debt restructuring."),
         ("The lender accepts land worth less than the loan's carrying amount in full settlement of the loan", "Accepting assets worth less than the carrying amount in full settlement is a concession to a debtor in difficulty; Treliske recognizes a gain on restructuring for the shortfall."),
         ("The lender cuts the rate from 10% to 7%, though Treliske's remaining payments still exceed the carrying amount", "Whether a gain arises doesn't decide whether the restructuring is troubled. The rate cut is a concession; because the remaining undiscounted payments exceed the carrying amount, Treliske recognizes no gain and accounts for the change prospectively at a new effective rate.")],
        "A",
        """For a debtor, a restructuring is troubled when the debtor is experiencing financial difficulties and the creditor grants a concession it wouldn't otherwise consider (ASC 470-60). A concession exists when the debtor's effective borrowing rate on the restructured debt is lower than on the old debt, or when the creditor accepts assets or equity worth less than the debt's carrying amount in settlement. ASC 470-60-15 excludes, among others, a settlement in which the fair value of the assets the debtor transfers at least equals the carrying amount of the debt. Whether the debtor ends up recognizing a gain is a measurement question, answered after the restructuring is found to be troubled. ASU 2022-02 eliminated the creditors' troubled debt restructuring guidance (creditors now apply the general loan modification guidance) but left the debtors' guidance in ASC 470-60 in place."""),
    mcq("far-intangibles-classification-0002", A2, "Intangible assets", RU,
        ["ASC 350-30-25 (recognition of intangible assets acquired individually; costs of internally developing intangibles that are not specifically identifiable expensed)", "ASC 350-30-35-1 to 35-4 (useful life: finite or indefinite; renewal)"],
        """Penhallow Co. spent money on each of the following in Year 1. Which should it recognize as an intangible asset and amortize?""",
        [("A franchise it bought to operate in one county for 12 years, with no right to renew", "Correct. A purchased franchise is recognized at cost. Its legal life is 12 years with no renewal, so its useful life is finite and it is amortized over that period."),
         ("A trademark it bought from a competitor, renewable every 10 years at little cost, that it plans to use indefinitely", "The trademark is recognized, but renewal is routine and inexpensive and Penhallow plans to keep using it, so no limit on its useful life is foreseeable. It is indefinite-lived and isn't amortized."),
         ("Training for its sales staff, expected to raise sales for about five years", "Penhallow doesn't control trained employees, who can leave, and training costs aren't a specifically identifiable asset. They are expensed as incurred."),
         ("Payroll of staff who built a customer database from Penhallow's own sales records", "Costs of developing an intangible internally that isn't specifically identifiable, or is inherent in the continuing business, are expensed. A customer list is recognized as an asset only when it is acquired.")],
        "A",
        """An intangible asset acquired individually, such as a purchased franchise or trademark, is recognized at cost (ASC 350-30-25). Costs of internally developing, maintaining or restoring intangibles that aren't specifically identifiable, have indeterminate lives or are inherent in a continuing business, such as building a customer database or training staff, are expensed. A recognized intangible is amortized over its useful life if that life is finite; if no legal, regulatory, contractual, competitive or economic factor limits it, it is indefinite-lived and is not amortized. A 12-year franchise without renewal rights is finite-lived; a trademark renewable at little cost that the entity intends to keep using is indefinite-lived."""),
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
    assert len(items) == 25 and len({it["id"] for it in items}) == 25
    warnings = audit(items)
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    tally, v0 = {}, {}
    for it in items:
        v0[it["answer"]] = v0.get(it["answer"], 0) + 1
        for v in [it] + list(it.get("variants") or []):
            tally[v["answer"]] = tally.get(v["answer"], 0) + 1
    print("version-0 keys", dict(sorted(v0.items())), "all versions", dict(sorted(tally.items())),
          "variants", sum(len(it.get("variants") or []) for it in items))
    if "--dry-run" in sys.argv:
        print("dry run: nothing written")
        return
    write_items(items, CONTENT)


if __name__ == "__main__":
    main()
