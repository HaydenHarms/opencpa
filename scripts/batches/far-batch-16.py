"""FAR batch 16 — 16 items written from scratch, Area III — Select Transactions only (a slice run in
parallel with batches 15 and 17, which cover Area II and III.A.*, III.B.*, III.G.*; no shared ids or tasks).

Plan: a third item on III.C.d (five-step model: variable consideration under the constraint, principal
versus agent in a different industry, and the sales-/usage-based royalty exception for licenses of IP),
a fourth on III.C.e (contract costs: PP&E and supplies outside ASC 340-40, amortization from the service
start), a third and fourth on III.C.f (NFP contributed services: revenue and expense for services that
create an asset versus services expensed; services capitalized into construction in progress, including
staff lent by an affiliate), a third on III.C.g (NFP contributions: a short-term promise, a condition not
yet met, donated supplies, a donor's forgiveness of a loan), a second and third on III.E.b (fair value:
the in-use premise judged from market evidence, and nonperformance risk in measuring a liability), a
fourth and fifth on III.F.c (lessee assets and liabilities: a residual value guarantee bought by the
lessor from an insurer, and the private-company risk-free rate election with a security deposit), a sixth
and seventh on III.F.d (lessee lease cost: a purchase option the candidate must judge, with initial direct
costs, and a decreasing rent schedule with a lease incentive and a non-index variable payment), and a
fourth on III.D.c, III.D.d and III.D.e (income taxes: the current component of expense; deferred tax
ledger balances with a valuation allowance; deferred tax expense with a change in the allowance). Every
item is Application (none of these tasks is marked Analysis). Scope and skill tags follow the AICPA CPA
Exam Blueprints effective January 2026.

Rework after the review gate (2026-10-05, 78.2%, two majors): lessee-finance-0005 and
nfp-contributed-services-0004 were rebuilt; every other finding was applied here, and items stay
`status: draft` until the gate re-passes. See docs/reviews/far-batch-16.md.

Every number and distractor below is computed in code (Decimal, rounded half up). Each family's four
parameter sets move the key's letter across at least two versions (batch 11 gate), and parameter set 0
carries the central-twist distractor named in `twist`.

Run: python scripts/batches/far-batch-16.py [--dry-run]
Blind file (set B16_SCRATCH to a directory): stems/choices and keys written there, never in the repo.
"""
import json
import os
import re
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AP, _amounts, attach_variants, audit, finalize, fix_articles, mcq as _mcq, variant, write_items  # noqa: E402
from variants import m, pick, rd  # noqa: E402

A3 = "Area III — Select Transactions"
NOTE = ("Batch 16. Written from scratch; answers solved and every number and distractor computed in code. "
        "Reworked after the 2026-10-05 review gate.")
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
SCRATCH = os.environ.get("B16_SCRATCH")
ASOF_TAX = "U.S. GAAP (ASC 740) and federal tax law in effect for 2026; the rate is as stated in the stem"
STATUS = "draft"  # stays unserved until the review gate re-passes; the lead flips it to reviewed


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


def family(id, area, topic, skill, refs, build, params, twist, asof=None):
    assert twist in params[0]["use"], f"{id}: version 0 doesn't show the central-twist distractor {twist}"
    base = build(params[0])
    review = dict(status=STATUS, references=refs, notes=NOTE)
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
    amts = re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", v["stem"])
    dup = sorted({a for a in amts if amts.count(a) > 1})
    if dup:
        print(f"REPEAT {label}: stem repeats {', '.join(dup)}", file=sys.stderr)


def spacing(label, v):
    """Flag two choices whose amounts are all within 0.4% of each other (a cluster the bar warns about)."""
    vals = sorted(_amounts(c["text"]) for c in v["choices"])
    for a, b in zip(vals, vals[1:]):
        if all(abs(y - x) < 0.004 * max(abs(y), 1) for x, y in zip(a, b)):
            print(f"CLOSE {label}: {a} and {b}", file=sys.stderr)


def short(name):
    return name.split()[0]


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole amount, got {x}"
    return x


def distinct(pool, key):
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"
    nums = [_amounts(v) for v in vals]
    assert len(set(nums)) == len(nums), f"two choices share every amount: {vals}"


def build(pool, key, use):
    distinct({k: pool[k] for k in use}, key)
    return pick(pool, key, use)


def pv_single(rate_pct, n):
    """Present value factor of 1, n periods, rounded to four decimals."""
    i = D(rate_pct) / 100
    return rd(D(1) / (D(1) + i) ** n, "0.0001")


def pv_annuity_ordinary(rate_pct, n):
    i = D(rate_pct) / 100
    return rd((D(1) - (D(1) + i) ** -n) / i, "0.0001")


def pv_annuity_due(rate_pct, n):
    """Annuity-due factor computed exactly, then rounded once (the batch 16 gate found a $6 error from
    rounding the ordinary factor first and then multiplying by 1 + i)."""
    i = D(rate_pct) / 100
    return rd((D(1) - (D(1) + i) ** -n) / i * (D(1) + i), "0.0001")


def pc(x):
    return format(D(x).normalize(), "f")


# ── III.C.d — Determine revenue under the five-step model ──────────────────


def revenue_variable_constraint(p):
    co, s = p["co"], short(p["co"])
    N, P, B = D(p["N"]), D(p["P"]), D(p["B"])
    Ntot = N * 3
    key_v = N * P
    full_bonus = N * (P + B)
    ev_bonus = N * (P + B / 2)
    total_units = Ntot * P
    pool = {
        "full_bonus": (m(full_bonus), f"Includes the full {m(B)}-a-unit bonus, as if the board's approval were already certain. The outcome is highly uncertain and outside {s}'s control, with no comparable experience to draw on, so the bonus is constrained out of the transaction price until the board decides."),
        "ev_bonus": (m(ev_bonus), f"Weights the bonus by a 50% chance of approval ({m(B)} × 50%) and adds it to the price. An expected-value estimate doesn't cure the constraint when the outcome is highly uncertain and outside {s}'s control; the bonus is excluded entirely until the board decides."),
        "total_units": (m(total_units), f"Multiplies the price by the {int(Ntot):,} units {s} expects to ship over the whole contract instead of the {int(N):,} units actually shipped in Year 1."),
        "defer_all": (m(0), f"Defers all Year 1 revenue until the board decides. The {m(P)}-a-unit base price isn't contingent on the board's decision and is unconditional revenue as the units ship; only the uncertain bonus is excluded."),
    }
    key = (m(key_v), f"Correct. {int(N):,} units × {m(P)} base price; the uncertain bonus is excluded from the transaction price.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On July 1, Year 1, {co} begins shipping a newly developed sensor to a customer under a multi-year supply contract; the contract price is {m(P)} a unit, and {s} expects to ship about {int(Ntot):,} units over the contract's life. In addition, {s} will earn a {m(B)}-a-unit bonus on every unit shipped in Year 1 if an industry standards board approves the sensor's new calibration method. The board will rule at its meeting in April, Year 2, after {s} issues its Year 1 financial statements; {s}'s president calls the decision a coin flip, because the board has never evaluated a method like this one and has given no indication which way it will rule. {s} shipped {int(N):,} units in Year 1. How much revenue should {s} recognize in its Year 1 financial statements for the units shipped in Year 1?""",
        choices, ans,
        f"""The {m(P)} base price is unconditional and is recognized as each unit ships: {int(N):,} × {m(P)} = {m(key_v)}. The {m(B)}-a-unit bonus is variable consideration, but the board's decision is highly susceptible to factors outside {s}'s influence and {s} has no relevant experience with a similar method, so it is not probable that including any part of the bonus would avoid a significant revenue reversal; the constraint on estimates of variable consideration (ASC 606-10-32-11 to 32-12) keeps it out of the transaction price. The board won't rule until April, Year 2, after the Year 1 statements are issued, so the uncertainty is unresolved at December 31, Year 1, when the transaction price is reassessed (ASC 606-10-32-14). A 50% expected value doesn't change that; the bonus is recognized when the board approves it, if it does. Revenue for Year 1 = {m(key_v)}.""",
    )


def revenue_principal_agent2(p):
    co, s = p["co"], short(p["co"])
    pct = D(p["pct"])
    Z, Sub, Mn = D(p["Z"]), D(p["Sub"]), D(p["M"])
    commission = rd(Z * pct / 100)
    sub_rev = Sub * Mn
    key_v = commission + sub_rev
    pool = {
        "gross": (m(Z + sub_rev), f"Reports the ride fares gross, {m(Z)}. The drivers — not {s} — are responsible for safely completing each trip and bear the risk of a problem with it, so {s} is an agent for the fares despite setting the price, and recognizes only its {p['pct']}% fee."),
        "flip": (m(rd(Z * (100 - pct) / 100) + sub_rev), f"Recognizes the {100 - int(pct)}% of each fare paid to the driver instead of the {p['pct']}% {s} keeps."),
        "no_sub": (m(commission), f"Omits the {m(sub_rev)} of subscription revenue. {s} provides the subscription perks itself, with no third party involved, so that revenue is recognized gross."),
        "no_comm": (m(sub_rev), f"Omits the {m(commission)} ride commission, as if {s} earned nothing from arranging rides. As an agent, {s} still recognizes its own fee."),
    }
    key = (m(key_v), f"Correct. Ride commission ({p['pct']}% × {m(Z)} = {m(commission)}) as agent, plus subscription revenue ({m(Sub)} × {int(Mn):,} = {m(sub_rev)}) as principal.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} operates a ride-hailing app. Drivers are independent contractors who own their vehicles, decide whether to accept each ride request, and are responsible for safely completing the trip and resolving any problem with it; {s} sets the fare for every ride with its own pricing algorithm and collects the fare from the rider, then pays the driver {100 - int(pct)}% of each fare and keeps the remaining {p['pct']}%. During the month, riders paid total fares of {m(Z)}. {s} also sells its own "Plus" subscription, a flat {m(Sub)} a month for perks that {s} alone provides; {int(Mn):,} riders held active subscriptions during the month. What total revenue should {s} recognize for the month?""",
        choices, ans,
        f"""An entity is a principal if it controls the specified service before it is transferred to the customer (ASC 606-10-55-36 to 55-40). The indicators point in different directions here: {s} sets the price, which is a principal indicator, but the drivers decide whether to accept each ride, provide it with their own vehicles and are primarily responsible for completing it and resolving any problem. {s} never directs a driver to perform a ride, so it doesn't control the ride service before the rider receives it; pricing discretion alone doesn't establish control. {s} is therefore an agent for the fares and recognizes only its fee: {p['pct']}% × {m(Z)} = {m(commission)}. The subscription is {s}'s own service, with no other party involved, so it is recognized gross: {m(Sub)} × {int(Mn):,} = {m(sub_rev)}. Total revenue = {m(key_v)}.""",
    )


def revenue_royalty_license(p):
    co, s = p["co"], short(p["co"])
    ppct, ppat, pproj = D(p["ppct"]), D(p["ppat"]), D(p["pproj"])
    Fy, fpct, fsales = D(p["Fy"]), D(p["fpct"]), D(p["fsales"])
    patent_roy = rd(ppat * ppct / 100)
    fq = whole(Fy / 4)
    franch_roy = rd(fsales * fpct / 100)
    key_v = patent_roy + fq + franch_roy
    proj_roy = rd(pproj * ppct / 100)
    qproj_roy = rd(pproj / 4 * ppct / 100)
    assert qproj_roy != patent_roy, "a quarter of the projection must not equal actual sales (gate finding)"
    pool = {
        "estimate_upfront": (m(proj_roy + fq + franch_roy), f"Recognizes the royalty on the full {m(pproj)} of sales {s} projected for the year, {p['ppct']}% × {m(pproj)} = {m(proj_roy)}, when the license is granted. A sales-based royalty for a license of intellectual property is recognized only as the underlying sales occur (ASC 606-10-55-65)."),
        "quarter_projection": (m(qproj_roy + fq + franch_roy), f"Estimates the patent royalty from one quarter of the projected sales, {p['ppct']}% × {m(pproj / 4)} = {m(qproj_roy)}, instead of the {m(ppat)} of sales that actually occurred. The royalty is recognized as the sales occur, at the actual amount."),
        "full_fee": (m(patent_roy + Fy + franch_roy), f"Recognizes the whole {m(Fy)} brand fee when the license is granted. The brand license gives the franchisee access to {s}'s brand as {s} keeps supporting it over the year, so the fixed fee is recognized over the year: {m(fq)} for the quarter."),
        "omit_patent": (m(fq + franch_roy), f"Leaves out the {m(patent_roy)} patent royalty, as if a license with no fixed fee earned nothing until the year's total is known."),
        "omit_fixed": (m(patent_roy + franch_roy), f"Leaves out the {m(fq)} share of the fixed brand fee earned in the quarter, as if the fee were unearned until the year ends."),
    }
    key = (m(key_v), f"Correct. ({p['ppct']}% × {m(ppat)}) + ({m(Fy)} ÷ 4) + ({p['fpct']}% × {m(fsales)}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} granted two licenses. The first lets a manufacturer use {s}'s patented sensor-calibration process, mature technology that {s} doesn't plan to update, for a {p['ppct']}% royalty on the manufacturer's net sales of products using the process, with no fixed fee and no minimum; at signing, {s} projected those sales at about {m(pproj)} for Year 1. The second gives a franchisee the use of {s}'s brand name for Year 1, with marketing support {s} provides evenly throughout the year, for a fixed {m(Fy)} paid at signing plus a {p['fpct']}% royalty on the franchisee's sales. In the first quarter of Year 1, the manufacturer's sales using the process were {m(ppat)} and the franchisee's sales were {m(fsales)}. How much revenue should {s} recognize from the two licenses for the first quarter of Year 1?""",
        choices, ans,
        f"""A sales- or usage-based royalty for a license of intellectual property is recognized only when the later of the sale occurring and the performance obligation being satisfied takes place (ASC 606-10-55-65), whether the license is a right to use (the patent, functional and not updated) or a right to access (the brand, supported by {s} through the year); {s} doesn't estimate the royalty from its projection. Patent royalty = {p['ppct']}% × {m(ppat)} = {m(patent_roy)}. The brand license is satisfied over the year, so the fixed fee is recognized evenly: {m(Fy)} ÷ 4 = {m(fq)}, and its royalty = {p['fpct']}% × {m(fsales)} = {m(franch_roy)}. Total revenue = {m(key_v)}.""",
    )


# ── III.C.e — Determine recognition and measurement of contract costs ──────


def contract_costs_scope(p):
    co, s = p["co"], short(p["co"])
    term = 36
    Cm, Setup, EQ, INV = D(p["Cm"]), D(p["S"]), D(p["EQ"]), D(p["INV"])
    mo, off = p["mo"], p["off"]
    total = Cm + Setup
    key_v = whole(total * mo / term)
    pool = {
        "wrong_start": (m(whole(total * (mo + off) / term)), f"Amortizes from the {p['sd']} signing date, {mo + off} months, instead of from {p['start']}, when services began. A contract cost asset is amortized as the services it relates to are transferred (ASC 340-40-35-1), so amortization starts with the services: {mo} months."),
        "include_eq": (m(whole((total + EQ) * mo / term)), f"Adds the {m(EQ)} of {p['eq']} to the contract cost asset and amortizes it over the contract. Equipment {s} will redeploy after the contract is property, plant and equipment within ASC 360, outside ASC 340-40 (ASC 340-40-15-3), and is depreciated, not amortized as a contract cost."),
        "include_inv": (m(whole((total + INV) * mo / term)), f"Adds the {m(INV)} of {p['sup']} to the contract cost asset. Supplies used up in performing the services are inventory within ASC 330 until consumed, outside ASC 340-40."),
        "comm_only": (m(whole(Cm * mo / term)), f"Amortizes only the commission, expensing the {m(Setup)} of configuration labor as incurred. That labor relates directly to this contract, sets up the resources {s} uses to serve the customer, and is recovered through the fees, so it is a capitalized cost to fulfill the contract (ASC 340-40-25-5)."),
        "setup_only": (m(whole(Setup * mo / term)), f"Amortizes only the configuration labor, expensing the {m(Cm)} commission when paid. A commission owed only because the contract was signed is an incremental cost of obtaining it and is capitalized, since the amortization period exceeds one year (ASC 340-40-25-1 to 25-4)."),
    }
    key = (m(key_v), f"Correct. ({m(Cm)} + {m(Setup)}) × {mo}/{term}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On {p['sd']}, Year 1, {co} signed a three-year contract to run a customer's outbound logistics, with services beginning {p['start']}, Year 1, and running 36 months; renewal isn't expected. On signing, {s} paid its salesperson a {m(Cm)} commission on the contract. Before services began, it spent {m(Setup)} on technician labor configuring the customer's shipment-tracking workflows on {s}'s platform; the setup gives the customer nothing it can use on its own, and the monthly fees are priced to recover it. {s} also bought {m(EQ)} of {p['eq']} that it will use on this customer's account and move to other jobs when the contract ends, and {m(INV)} of {p['sup']} that will be used up in providing the services. {s} amortizes any capitalized contract cost straight-line by month over the period of the services it relates to. What amortization of contract cost assets should {s} recognize for Year 1?""",
        choices, ans,
        f"""The commission is an incremental cost of obtaining the contract, and the configuration labor is a cost to fulfill it: it relates directly to the contract, creates resources {s} will use to provide the services, and is recovered through the fees (ASC 340-40-25-1 to 25-8). Both are capitalized, {m(Cm)} + {m(Setup)} = {m(total)}, and amortized over the 36 months of services starting {p['start']} (ASC 340-40-35-1): {m(total)} × {mo}/{term} = {m(key_v)}. The {p['eq']} are property, plant and equipment within ASC 360 and the {p['sup']} are inventory within ASC 330, so neither is a contract cost asset (ASC 340-40-15-3), even though both were bought for this contract.""",
    )


# ── III.C.f — Determine NFP revenue for contributed services ───────────────


def nfp_services_asset(p):
    org, s = p["org"], short(p["org"])
    A, C, Dv, E = D(p["A"]), D(p["C"]), D(p["D"]), D(p["E"])
    rev, exp = A + C, A

    def ch(r, e):
        return f"{m(r)} revenue; {m(e)} expense"

    pool = {
        "skip_shed": (ch(A, A), f"Omits the {m(C)} of shed assembly. Services that create or enhance a nonfinancial asset are recognized whether or not the people providing them have specialized skills (ASC 958-605-25-16)."),
        "expense_shed": (ch(A + C, A + C), f"Recognizes the shed assembly as revenue but expenses it. Contributed services that create a nonfinancial asset are capitalized as part of that asset (debit property), so only the technician's {m(A)} is expensed."),
        "skip_tech": (ch(C, 0), f"Leaves out the piano technician's {m(A)}. Tuning and regulating concert pianos takes a specialized skill she has, and {s} would otherwise have paid for it, so it is recognized (and expensed, since it maintains rather than creates an asset)."),
        "include_mail": (ch(A + C + Dv, A + Dv), f"Includes the {m(Dv)} of volunteer time stuffing and mailing fundraising letters. That work needs no specialized skill and creates no nonfinancial asset, so it isn't recognized."),
        "include_lawn": (ch(A + C + E, A + E), f"Includes the {m(E)} of lawn mowing. Routine upkeep needs no specialized skill and creates no nonfinancial asset, so it isn't recognized."),
    }
    key = (ch(rev, exp), f"Correct. Revenue: technician {m(A)} + shed {m(C)}; the shed labor is capitalized, so only the technician's {m(A)} is expensed.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, received these donated services. A professional piano technician tuned and regulated the center's two concert pianos, work {s} would otherwise have paid {m(A)} for. A group of volunteers assembled a prefabricated storage shed, from a kit {s} bought, on a slab behind the building, labor worth {m(C)} at the rates a handyman service would charge. Volunteers stuffed and mailed {s}'s fundraising letters, time worth {m(Dv)} at local wage rates. Other volunteers mowed {s}'s lawn throughout the year, time worth {m(E)} at local wage rates. Ignoring depreciation, what amounts should {s} recognize for these services in Year 1 as contribution revenue and as expense?""",
        choices, ans,
        f"""Contributed services are recognized if they (a) create or enhance a nonfinancial asset, or (b) require specialized skills, are provided by people with those skills, and would typically need to be purchased if not donated (ASC 958-605-25-16). The technician's work meets (b) and maintains existing assets, so it is revenue and expense of {m(A)}. The shed labor meets (a), whatever the volunteers' skills: revenue of {m(C)}, debited to the shed rather than to expense. Mailing letters and mowing meet neither test and aren't recognized. Revenue = {m(A)} + {m(C)} = {m(rev)}; expense = {m(exp)}.""",
    )


def nfp_services_construction(p):
    org, s = p["org"], short(p["org"])
    cash, A, P, Cv = D(p["cash"]), D(p["A"]), D(p["P"]), D(p["Cv"])
    cip, rev = cash + A + P, A + P

    def ch(c, r):
        return f"{m(c)} construction in progress; {m(r)} revenue"

    pool = {
        "omit_aff": (ch(cash + A, A), f"Leaves out the project manager's {m(P)}. Services from an affiliate's personnel that directly benefit {s} are recognized, and her supervision of the construction also creates a nonfinancial asset, so the services are recognized as revenue and capitalized into the building."),
        "expense_aff": (ch(cash + A, A + P), f"Recognizes the project manager's {m(P)} as revenue but expenses it instead of capitalizing it. Supervising the construction is part of the cost of creating the building, so it is added to construction in progress, as the architect's drawings are."),
        "expense_all": (ch(cash, rev), f"Recognizes the donated services as revenue but expenses them, so construction in progress holds only the {m(cash)} paid to the contractor. Contributed services that create a nonfinancial asset are capitalized into that asset."),
        "include_cer": (ch(cip + Cv, rev + Cv), f"Includes the {m(Cv)} of volunteer time at the groundbreaking ceremony. Handing out programs needs no specialized skill and creates no asset, so it isn't recognized."),
    }
    key = (ch(cip, rev), f"Correct. Construction in progress = {m(cash)} + {m(A)} + {m(P)}; revenue = {m(A)} + {m(P)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, began building a clinic, which it will finish in Year 2. It paid its general contractor {m(cash)} for work through December 31. A licensed architect donated the clinic's design drawings, work her firm would normally bill at {m(A)}. {s}'s affiliate, a regional hospital, assigned one of its construction project managers to oversee the clinic's construction part-time from March through December; the hospital kept paying her and charged {s} nothing, and her pay and benefits for that time, {m(P)}, are about what an outside construction manager would have charged. Neighborhood volunteers handed out programs and served refreshments at the groundbreaking ceremony, time worth {m(Cv)} at local wage rates. What should {s} report at December 31, Year 1, as construction in progress, and as contribution revenue from contributed services for Year 1?""",
        choices, ans,
        f"""The architect's drawings require specialized skills {s} would otherwise buy, and both they and the project manager's supervision create a nonfinancial asset, the clinic (ASC 958-605-25-16). Services that an affiliate's personnel provide and that directly benefit {s} are also recognized (ASC 958-605-25, as amended by ASU 2013-06), measured here at {m(P)}, the hospital's cost, which is about their fair value. Each is recognized as contribution revenue and, because it creates the building, capitalized: construction in progress = {m(cash)} + {m(A)} + {m(P)} = {m(cip)}; revenue = {m(A)} + {m(P)} = {m(rev)}. The ceremony volunteers' time needs no specialized skill and creates no asset, so it isn't recognized.""",
    )


# ── III.C.g — Calculate NFP contributions of financial and nonfinancial assets ──


def nfp_contributions_current(p):
    org, s = p["org"], short(p["org"])
    P, Mv, R, L = D(p["P"]), D(p["M"]), D(p["R"]), D(p["L"])
    key_v = P + Mv + L
    pool = {
        "include_r": (m(key_v + R), f"Includes the {m(R)} foundation pledge. The foundation pays only if {s} opens the satellite clinic by June 30, Year 2, and has the right not to pay otherwise; until that barrier is overcome the promise is conditional and isn't recognized (ASC 958-605-25)."),
        "omit_inv": (m(P + L), f"Leaves out the {m(Mv)} of donated medical supplies. Contributed nonfinancial assets are recognized at fair value when received (ASC 958-605-30)."),
        "omit_forgive": (m(P + Mv), f"Leaves out the {m(L)} loan the donor forgave. A donor's voluntary cancellation of a liability is a contribution (ASC 958-605-20, definition of a contribution), recognized when the liability is cancelled."),
        "omit_promise": (m(Mv + L), f"Leaves out the {m(P)} promise because no cash had arrived by year-end. An unconditional promise to give is recognized as revenue and a receivable when it is received (ASC 958-605-25)."),
    }
    key = (m(key_v), f"Correct. {m(P)} + {m(Mv)} + {m(L)}; the conditional pledge isn't recognized.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, had the following transactions. In December, a donor signed an unconditional promise to pay {s} {m(P)} within 60 days. A pharmaceutical distributor donated medical supplies for use in {s}'s patient-care programs, with a fair value of {m(Mv)}. A regional foundation pledged {m(R)}, which it will pay only if {s} opens a satellite clinic by June 30, Year 2; construction of the clinic hasn't begun. In Year 0, a supporter had lent {s} {m(L)} at a market rate of interest; in December, Year 1, with all interest paid to date, she notified {s} in writing that she was cancelling the loan. {s} measures promises to give that are due within one year at the amount it expects to collect, and expects to collect this one in full. What total contribution revenue should {s} recognize for Year 1?""",
        choices, ans,
        f"""The unconditional promise is recognized when received, at the {m(P)} {s} expects to collect, its stated measurement for promises due within one year (ASC 958-310-35; ASC 958-605-30). The supplies are contributed nonfinancial assets, recognized at fair value: {m(Mv)}. A donor's cancellation of a liability is a contribution (ASC 958-605-20), so the forgiven loan adds {m(L)}. The foundation's pledge depends on a barrier {s} hasn't overcome, opening the clinic, with a right for the foundation not to pay, so it is conditional and isn't recognized until the condition is met (ASC 958-605-25). Contribution revenue = {m(P)} + {m(Mv)} + {m(L)} = {m(key_v)}.""",
    )


# ── III.E.b — Use assumptions and approaches to measure fair value ─────────


def fv_in_use(p):
    co, s = p["co"], short(p["co"])
    scrap, new_cost, phys, func = D(p["scrap"]), D(p["new_cost"]), D(p["phys"]), D(p["func"])
    Lin, Lsep = D(p["Lin"]), D(p["Lsep"])
    assert Lin > Lsep
    key_v = new_cost - phys - func
    pool = {
        "scrap": (m(scrap), f"Uses the {m(scrap)} a dealer would pay for the {p['asset']} on its own. That is its value on a standalone (in-exchange) basis, but the line is worth more installed and working ({m(Lin)}) than sold piece by piece ({m(Lsep)}), so highest and best use is in combination with the line's other assets."),
        "no_func": (m(new_cost - phys), f"Deducts only physical deterioration. Functional obsolescence, the {m(func)} newer models' extra speed is worth, is also deducted in a cost approach."),
        "no_phys": (m(new_cost - func), f"Deducts only functional obsolescence. Physical deterioration, {m(phys)}, is also deducted in a cost approach."),
        "gross_new": (m(new_cost), f"Uses the {m(new_cost)} cost of a new substitute without any deduction for deterioration or obsolescence."),
    }
    key = (m(key_v), f"Correct. {m(new_cost)} − {m(phys)} − {m(func)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} owns a specialized {p['asset']} that is part of an integrated {p['line']} line. A market participant buying the whole line, installed and running, would pay about {m(Lin)} for it; sold off one machine at a time, the line's machines would bring only about {m(Lsep)} in total, and the {p['asset']} on its own would bring {m(scrap)} from a dealer, for parts. No active market exists for secondhand {p['asset']}s like this one, so {s}'s appraiser estimates the current cost of a new {p['asset']} with the same capacity and features, {m(new_cost)}, and reduces it by {m(phys)} of physical deterioration and {m(func)} of functional obsolescence, because newer models run faster. What is the fair value of the {p['asset']} under ASC 820?""",
        choices, ans,
        f"""Fair value of a nonfinancial asset reflects its highest and best use by market participants, which may be in combination with other assets as a group rather than on a standalone basis (ASC 820-10-35-10A to 35-10E). Market participants would pay more for the working line ({m(Lin)}) than for its machines sold separately ({m(Lsep)}), and they can acquire the complementary machines with it, so the {p['asset']}'s highest and best use is in combination with the line. Its fair value is then measured assuming it is used with those assets, here with a cost approach (ASC 820-10-55-3D): {m(new_cost)} − {m(phys)} − {m(func)} = {m(key_v)}. The {m(scrap)} standalone price would govern only if a standalone sale maximized its value.""",
    )


def fv_liability_nonperformance(p):
    co, s = p["co"], short(p["co"])
    face, n = D(p["face"]), p["n"]
    key_f = pv_single(D(p["rf"]) + D(p["r"]), n)
    rf_f = pv_single(D(p["rf"]), n)
    comp_f = pv_single(D(p["rf"]) + D(p["r2"]), n)
    stale_f = pv_single(D(p["rf"]) + D(p["stale"]), n)
    extra_f = pv_single(D(p["rf"]) + D(p["r"]), n + 1)
    key_v = whole(rd(face * key_f))
    chg = "downgrade" if D(p["stale"]) < D(p["r"]) else "upgrade"
    before = "only " if chg == "downgrade" else ""
    pool = {
        "risk_free_only": (m(whole(rd(face * rf_f))), f"Discounts at the {p['rf']}% risk-free rate alone ({m(face)} × {rf_f}), leaving out {s}'s own nonperformance risk. Fair value of a liability includes the effect of the reporting entity's own credit standing (ASC 820-10-35-17)."),
        "counterparty": (m(whole(rd(face * comp_f))), f"Uses the {p['r2']}% premium the higher-rated insurer quoted ({m(face)} × {comp_f}). Fair value reflects {s}'s own nonperformance risk, assumed to be the same after a transfer, not a stronger transferee's credit standing."),
        "stale": (m(whole(rd(face * stale_f))), f"Uses the {p['stale']}% premium that applied before {s}'s {chg} ({m(face)} × {stale_f}). Nonperformance risk is measured at {s}'s credit standing as of the measurement date, not an earlier one."),
        "extra_year": (m(whole(rd(face * extra_f))), f"Discounts the obligation for {n + 1} years instead of {n} ({m(face)} × {extra_f}), one year too many."),
    }
    key = (m(key_v), f"Correct. {m(face)} discounted {n} years at {pc(D(p['rf']) + D(p['r']))}% ({p['rf']}% risk-free + {p['r']}% for {s}'s own nonperformance risk).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} must measure, on the transfer basis ASC 820 requires, the fair value of a {m(face)} obligation it owes a counterparty, payable in a lump sum in {n} years. The risk-free rate for a {n}-year term is {p['rf']}%. After a recent credit {chg}, market participants would require a {p['r']}% premium for {s}'s own nonperformance risk as of the measurement date; before the {chg}, that premium was {before}{p['stale']}%. A higher-rated insurer that might assume the obligation said it would price it at only a {p['r2']}% premium. Using present value factors rounded to four decimal places, what is the fair value of {s}'s obligation?""",
        choices, ans,
        f"""Fair value of a liability assumes transfer to a market participant of comparable credit standing (ASC 820-10-35-16) and includes the effect of the reporting entity's own nonperformance risk, including its own credit risk, measured as of the measurement date and assumed to be the same before and after the transfer (ASC 820-10-35-17 to 35-18) — not a stronger counterparty's credit standing and not a stale, pre-downgrade spread. The discount rate is {p['rf']}% risk-free + {p['r']}% for {s}'s own current nonperformance risk = {pc(D(p['rf']) + D(p['r']))}%. Fair value = {m(face)} × {key_f} = {m(key_v)}.""",
    )


# ── III.F.c — Calculate lessee assets and liabilities and prepare journal entries ──


def lessee_third_party_rvg(p):
    co, s = p["co"], short(p["co"])
    n, i = p["n"], D(p["i"])
    pay, g, idc, legal = D(p["pay"]), D(p["g"]), D(p["idc"]), D(p["legal"])
    af = pv_annuity_ordinary(i, n)
    sf = pv_single(i, n)
    af_due = pv_annuity_due(i, n)
    liab = rd(pay * af)
    key_v = whole(liab + idc)
    pool = {
        "include_g": (m(whole(liab + rd(g * sf) + idc)), f"Adds {m(g)} × {sf} = {m(rd(g * sf))} for {p['ins']}'s residual value guarantee. Lease payments include only amounts probable of being owed by the lessee under a residual value guarantee (ASC 842-10-30-5(f)); {s} owes nothing under insurance the lessor bought from an unrelated insurer."),
        "undiscounted_g": (m(whole(liab + g + idc)), f"Adds the full {m(g)} guarantee, undiscounted. {s} owes nothing under the insurer's guarantee, so it isn't a lease payment at all (ASC 842-10-30-5(f))."),
        "incl_legal": (m(whole(liab + idc + legal)), f"Also adds the {m(legal)} of legal fees for negotiating the lease. {s} would have owed those fees whether or not the lease was signed, so they aren't initial direct costs (ASC 842-10-30-9 to 30-10); they are expensed."),
        "omit_idc": (m(whole(liab)), f"Leaves out the {m(idc)} broker commission. A commission owed only because the lease was signed is an initial direct cost, added to the right-of-use asset (ASC 842-20-30-5)."),
        "wrong_annuity": (m(whole(rd(pay * af_due) + idc)), f"Discounts the payments as an annuity due ({m(pay)} × {af_due} = {m(rd(pay * af_due))}) and adds the {m(idc)} commission. Payments are due at the end of each year, so the ordinary annuity factor applies."),
    }
    key = (m(key_v), f"Correct. {m(pay)} × {af} = {m(liab)}, + {m(idc)} of initial direct costs.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} leases {p['asset']} for {n} years and classifies the lease as a finance lease. Payments of {m(pay)} are due each December 31. The lessor separately bought residual value insurance from {p['ins']}, which guarantees the lessor {m(g)} for the equipment at lease end. {s} paid a {m(idc)} commission, payable on signing, to the broker who found the {p['short']}, and {m(legal)} of legal fees for negotiating the lease terms. The rate implicit in the lease isn't readily determinable, and {s}'s incremental borrowing rate is {i}%; present value factors at {i}% for {n} periods are {af} for an ordinary annuity, {af_due} for an annuity due and {sf} for a single sum. What amount should {s} initially recognize as its right-of-use asset?""",
        choices, ans,
        f"""Lease payments include amounts probable of being owed by the lessee under a residual value guarantee (ASC 842-10-30-5(f)). The guarantee here is insurance the lessor bought from {p['ins']}; {s} isn't a party to it and owes nothing under it, so it isn't a lease payment, whatever its amount. The lease liability is the present value of the payments, due at year-end: {m(pay)} × {af} = {m(liab)}. The right-of-use asset adds the {m(idc)} commission, an initial direct cost because it is owed only because the lease was signed (ASC 842-20-30-5; ASC 842-10-30-9). The legal fees for negotiating the terms would have been incurred even if the lease hadn't been signed, so they are expensed. Right-of-use asset = {m(liab)} + {m(idc)} = {m(key_v)}.""",
    )


def lessee_riskfree_deposit(p):
    co, s = p["co"], short(p["co"])
    n, rf = p["n"], D(p["rf"])
    pay, sd = D(p["pay"]), D(p["sd"])
    af_due = pv_annuity_due(rf, n)
    af_ord = pv_annuity_ordinary(rf, n)
    ib = D(p["ib"])
    af_ib = pv_annuity_due(ib, n)
    full = rd(pay * af_due)
    key_v = whole(full - pay)
    pool = {
        "full_annuity": (m(whole(full)), f"Doesn't deduct the {m(pay)} Year 1 rent paid at commencement ({m(pay)} × {af_due} = {m(full)}). The lease liability is the present value of payments not yet made."),
        "add_sd": (m(whole(full - pay + sd)), f"Adds the {m(sd)} security deposit to the liability. A refundable deposit isn't a lease payment (ASC 842-10-30-5); it is a separate receivable from the landlord."),
        "subtract_sd": (m(whole(full - pay - sd)), f"Subtracts the {m(sd)} security deposit from the liability instead of recording it as a separate asset."),
        "ibr": (m(whole(rd(pay * af_ib) - pay)), f"Discounts at the {ib}% incremental borrowing rate ({m(pay)} × {af_ib} = {m(rd(pay * af_ib))}, less the {m(pay)} paid). {s} has elected the risk-free rate for real estate leases, so the {rf}% rate applies."),
        "ordinary_af": (m(whole(rd(pay * af_ord))), f"Discounts all {n} payments with the ordinary annuity factor ({m(pay)} × {af_ord}), as if each were due at year-end. Rent is paid in advance, and the first payment has already been made."),
    }
    key = (m(key_v), f"Correct. {m(pay)} × {af_due} = {m(full)}, less the {m(pay)} paid at commencement.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a private company, leases warehouse space for {n} years under an operating lease that begins January 1, Year 1. Rent is {m(pay)} a year, payable in advance each January 1, and {s} paid the Year 1 rent when the lease began. At commencement, {s} also gave the landlord a {m(sd)} security deposit, which comes back at the end of the lease if the space is returned undamaged. The rate implicit in the lease isn't readily determinable. {s}'s incremental borrowing rate is {ib}%, and the risk-free rate for a {n}-year term is {rf}%. For its real estate leases, {s} has elected to discount lease payments at a risk-free rate. Present value factors for {n} periods are {af_due} for an annuity due and {af_ord} for an ordinary annuity at {rf}%, and {af_ib} for an annuity due at {ib}%. What lease liability should {s} report immediately after paying the Year 1 rent?""",
        choices, ans,
        f"""A lessee uses the rate implicit in the lease whenever it is readily determinable; when it isn't, a private company may elect, by class of underlying asset, to use a risk-free rate instead of its incremental borrowing rate (ASC 842-20-30-3, as amended by ASU 2021-09). {s} made that election for real estate, so it discounts at {rf}%. A refundable security deposit isn't a lease payment (ASC 842-10-30-5); it is a separate receivable. Rent is paid in advance, so the {n} payments are an annuity due: {m(pay)} × {af_due} = {m(full)}, less the {m(pay)} already paid, leaves {m(key_v)}.""",
    )


# ── III.F.d — Calculate lessee lease costs ──────────────────────────────────


def lessee_purchase_option_cost(p):
    co, s = p["co"], short(p["co"])
    n, u, i = p["n"], p["u"], D(p["i"])
    pay, opt, fvexp, idc = D(p["pay"]), D(p["opt"]), D(p["fvexp"]), D(p["idc"])
    assert fvexp >= 3 * opt
    af, sf = pv_annuity_ordinary(i, n), pv_single(i, n)
    r = i / 100

    def sched(liab):
        int1 = rd(liab * r)
        bal1 = liab - (pay - int1)
        return int1, bal1, rd(bal1 * r)

    pv_pay, pv_opt = rd(pay * af), rd(opt * sf)
    liab = pv_pay + pv_opt
    int1, bal1, int2 = sched(liab)
    rou = liab + idc
    amort = rd(rou / u)
    # the liability must roll forward to the option price (gate: the old version's liability was impossible)
    bal = liab
    for _ in range(n):
        bal = bal + rd(bal * r) - pay
    assert abs(bal - opt) < 25, f"{co}: liability rolls to {bal}, not the {opt} option price"
    _, _, int2_no = sched(pv_pay)

    def ch(a, b):
        return f"{m(a)} interest; {m(b)} amortization"

    pool = {
        "term_amort": (ch(int2, rd(rou / n)), f"Amortizes the right-of-use asset over the {n}-year lease term, {m(rou)} ÷ {n}. A {m(opt)} option on a machine expected to be worth {m(fvexp)} makes exercise reasonably certain, so the asset is amortized over the {u}-year useful life (ASC 842-20-35-8)."),
        "no_option": (ch(int2_no, rd((pv_pay + idc) / n)), f"Leaves the purchase option out of the lease payments, measuring the liability at {m(pv_pay)}, and so amortizes over the {n}-year term. With the option priced far below the machine's expected value, exercise is reasonably certain, so the {m(opt)} price is a lease payment (ASC 842-10-30-5(c)) and the asset is amortized over its useful life."),
        "omit_idc": (ch(int2, rd(liab / u)), f"Amortizes only the {m(liab)} lease liability, leaving the {m(idc)} of initial direct costs out of the right-of-use asset (ASC 842-20-30-5)."),
        "year1_interest": (ch(int1, amort), f"Uses Year 1 interest, {m(liab)} × {pc(i)}%, instead of interest on the {m(bal1)} balance after the Year 1 payment."),
    }
    key = (ch(int2, amort), f"Correct. Interest {m(bal1)} × {pc(i)}% = {m(int2)}; amortization ({m(liab)} + {m(idc)}) ÷ {u} = {m(amort)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} leases {p['asset']} for {n} years and classifies the lease as a finance lease. Payments of {m(pay)} are due each December 31. The lease lets {s} buy the {p['short']} at the end of Year {n} for {m(opt)}; {s} expects it to be worth about {m(fvexp)} then, and the {p['short']}, new at commencement, has a useful life of {u} years with no residual value. {s} paid {m(idc)} of initial direct costs at commencement. The rate implicit in the lease isn't readily determinable, and {s}'s incremental borrowing rate is {pc(i)}%; present value factors at {pc(i)}% for {n} periods are {af} for an ordinary annuity and {sf} for a single sum. {s} amortizes right-of-use assets straight-line. Rounding each computation to the nearest dollar, what interest expense and what amortization expense should {s} recognize on the lease for Year 2?""",
        choices, ans,
        f"""An option to buy for {m(opt)} an asset expected to be worth {m(fvexp)} gives {s} a strong economic incentive to exercise, so exercise is reasonably certain and the price is a lease payment (ASC 842-10-30-5(c)). Liability = {m(pay)} × {af} + {m(opt)} × {sf} = {m(pv_pay)} + {m(pv_opt)} = {m(liab)}. Year 1 interest = {m(liab)} × {pc(i)}% = {m(int1)}, so the balance after the first payment is {m(liab)} + {m(int1)} − {m(pay)} = {m(bal1)}, and Year 2 interest = {m(bal1)} × {pc(i)}% = {m(int2)}. The right-of-use asset is the liability plus initial direct costs, {m(rou)}; because {s} is reasonably certain to buy the {p['short']}, it is amortized over the {u}-year useful life rather than the lease term (ASC 842-20-35-8): {m(rou)} ÷ {u} = {m(amort)}.""",
    )


def lessee_stepdown_cost(p):
    co, s = p["co"], short(p["co"])
    pays = [D(x) for x in p["pays"]]
    incentive, pt = D(p["incentive"]), D(p["pt"])
    total_pay = sum(pays)
    core = whole(rd((total_pay - incentive) / 5))
    key_v = core + pt
    no_incentive = whole(rd(total_pay / 5))
    pool = {
        "cash_basis": (m(pays[0] + pt), f"Uses the Year 1 cash payment of {m(pays[0])} instead of the straight-line average. Operating lease cost is recognized straight-line over the term, regardless of the payment schedule."),
        "no_incentive": (m(no_incentive + pt), f"Spreads the full {m(total_pay)} of payments without deducting the {m(incentive)} leasehold improvement allowance. Lease incentives received reduce the lease payments recognized as cost over the term."),
        "omit_pt": (m(core), f"Leaves out the {m(pt)} of property tax reimbursement. It is a variable payment that isn't based on an index or a rate, so it isn't part of the straight-line calculation, but it is still lease cost, recognized as incurred."),
        "incentive_as_revenue": (m(no_incentive + pt + whole(rd(incentive / 5))), f"Adds a {m(whole(rd(incentive / 5)))} share of the {m(incentive)} incentive to cost instead of subtracting it from the payments being spread."),
        "incentive_upfront": (m(no_incentive - incentive + pt), f"Deducts the whole {m(incentive)} incentive from Year 1 cost instead of spreading it over the 5-year term with the payments."),
    }
    key = (m(key_v), f"Correct. ({m(total_pay)} total payments − {m(incentive)} incentive) ÷ 5 = {m(core)}, plus {m(pt)} of variable property tax reimbursement.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} leases retail space for 5 years, which it classifies as an operating lease. Rent, due each December 31, is {m(pays[0])} in Year 1 and falls each year after that: {m(pays[1])} in Year 2, {m(pays[2])} in Year 3, {m(pays[3])} in Year 4 and {m(pays[4])} in Year 5. At commencement, the landlord paid {s} {m(incentive)} in cash as a leasehold improvement allowance. {s} also reimburses the landlord each year for its pro-rata share of the property taxes actually assessed on the building; the reimbursement for Year 1 is {m(pt)}. What total lease cost should {s} recognize for Year 1?""",
        choices, ans,
        f"""For an operating lease, the fixed payments net of lease incentives received are recognized straight-line over the lease term (ASC 842-20-25-6(a)), unless another systematic basis better represents the pattern in which the lessee uses the space; nothing suggests one does, and a falling rent schedule doesn't change the straight-line pattern: ({m(total_pay)} total payments − {m(incentive)} incentive) ÷ 5 = {m(core)}. The property tax reimbursement doesn't depend on an index or a rate, so it is excluded from the lease payments and recognized as incurred (ASC 842-20-25-6(b)): {m(pt)}. Total lease cost = {m(core)} + {m(pt)} = {m(key_v)}.""",
    )


# ── III.D.c/d/e — Income taxes ──────────────────────────────────────────────


def tax_provision_installment(p):
    co, s = p["co"], short(p["co"])
    bi, lip, golf = D(p["bi"]), D(p["lip"]), D(p["golf"])
    gp, coll, est, r = D(p["gp"]), D(p["coll"]), D(p["est"]), D(p["r"])

    def tax(x):
        return whole(rd(x * r / 100))

    ti = bi - lip + golf - (gp - coll)
    cur = tax(ti)
    pool = {
        "tax_lip": (m(tax(ti + lip)), f"Taxes the {m(lip)} of life insurance proceeds. Proceeds from company-owned life insurance on an executive, with {s} as beneficiary, are excluded from taxable income, a permanent difference."),
        "golf_ded": (m(tax(ti - golf)), f"Deducts the {m(golf)} of club dues for tax as well as for books. The tax law doesn't allow them, so they are added back to pretax income in computing taxable income."),
        "ignore_inst": (m(tax(ti + gp - coll)), f"Taxes the whole {m(gp)} gain currently, as books recognize it. On the tax return only the {m(coll)} collected is taxed in Year 2; the tax on the other {m(gp - coll)} is deferred tax expense, not current. This figure is total income tax expense."),
        "net_est": (m(cur - est), f"Subtracts the {m(est)} of estimated payments. They settle part of the liability (income taxes payable), but they don't reduce current tax expense, which is the tax on Year 2 taxable income."),
        "deduct_all_gp": (m(tax(ti - coll)), f"Removes the whole {m(gp)} gain from taxable income, overlooking the {m(coll)} of it collected, and so taxed, in Year 2."),
    }
    key = (m(cur), f"Correct. ({m(bi)} − {m(lip)} + {m(golf)} − {m(gp - coll)}) × {p['r']}% = {m(ti)} × {p['r']}%.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} discloses the current and deferred components of its income tax expense. Its pretax financial income for Year 2 is {m(bi)}. That amount includes {m(lip)} of proceeds from company-owned life insurance on an executive who died during the year, with {s} as beneficiary, under a policy that meets the tax law's requirements for excluding the proceeds, and is after deducting {m(golf)} of country club dues, which the tax law doesn't allow as a deduction. In Year 2, {s} also sold land on installment terms and recognized the full {m(gp)} gain in its books; for tax it reports the gain under the installment method, and {m(coll)} of the gain relates to Year 2 collections. The enacted tax rate is {p['r']}% for all years. During Year 2, {s} paid {m(est)} of estimated tax, recorded as prepaid income taxes. What current income tax expense should {s} disclose for Year 2?""",
        choices, ans,
        f"""Current tax expense is the tax on the year's taxable income. Taxable income = {m(bi)} − {m(lip)} (life insurance proceeds, excluded) + {m(golf)} (club dues, not deductible) − {m(gp - coll)} (installment gain not yet taxed: {m(gp)} − {m(coll)}) = {m(ti)}. Current tax expense = {m(ti)} × {p['r']}% = {m(cur)}. The {m(est)} of estimated payments reduces income taxes payable, not expense, and the tax on the uncollected gain is deferred tax expense.""",
    )


def tax_deferred_installment_litigation(p):
    co, s = p["co"], short(p["co"])
    inst, lit, va, r, litc = D(p["inst"]), D(p["lit"]), D(p["va"]), D(p["r"]), D(p["litc"])

    def tax(x):
        return whole(rd(x * r / 100))

    dta, dtl = tax(lit), tax(inst)

    def ch(a, b):
        return f"{m(a)} asset; {m(b)} liability"

    pool = {
        "no_va": (ch(dta, dtl), f"Doesn't deduct the {m(va)} valuation allowance from the deferred tax asset."),
        "va_sign": (ch(dta + va, dtl), f"Adds the {m(va)} allowance to the deferred tax asset instead of deducting it. A valuation allowance reduces a deferred tax asset to the amount expected to be realized."),
        "cur_portion": (ch(tax(litc) - va, dtl), f"Bases the deferred tax asset on only the {m(litc)} of the accrual {s} expects to pay in Year 3. A deferred tax asset arises on the whole {m(lit)} deductible temporary difference; deferred taxes aren't split into current and noncurrent parts (ASC 740-10-45-4)."),
        "no_inst": (ch(dta - va, 0), f"Records no deferred tax liability, as if the {m(inst)} of gain not yet collected had already been taxed. Gain recognized in the books but taxed when collected is a taxable temporary difference (ASC 740-10-25-20)."),
        "va_on_dtl": (ch(dta, dtl - va), f"Deducts the {m(va)} allowance from the deferred tax liability. The allowance reduces the deferred tax asset it relates to."),
    }
    key = (ch(dta - va, dtl), f"Correct. Asset {m(lit)} × {p['r']}% = {m(dta)}, less the {m(va)} allowance; liability {m(inst)} × {p['r']}%.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} keeps separate deferred tax asset and deferred tax liability accounts in its ledger and is measuring them at December 31, Year 2. In Year 1 it sold land on installment terms, recognizing the whole gain in its books; {m(inst)} of that gain hasn't yet been collected and will be taxed as it is. In Year 2 it accrued a {m(lit)} loss for a lawsuit it expects to settle; the loss is deductible when paid, and {s} expects to pay {m(litc)} of it in Year 3 and the rest in Year 4. The enacted tax rate is {p['r']}% for all years. Weighing its recent losses against its forecasts, {s} concludes that it needs a valuation allowance of {m(va)} against its deferred tax asset. At December 31, Year 2, what amounts should {s} carry in its deferred tax asset account, net of the allowance, and in its deferred tax liability account?""",
        choices, ans,
        f"""The uncollected installment gain is a taxable temporary difference: deferred tax liability = {m(inst)} × {p['r']}% = {m(dtl)}. The litigation accrual is a deductible temporary difference in full, whenever it will be paid: deferred tax asset = {m(lit)} × {p['r']}% = {m(dta)}. The valuation allowance reduces the asset to the amount expected to be realized (ASC 740-10-30-5(e)): {m(dta)} − {m(va)} = {m(dta - va)}. Net of the allowance, the asset account carries {m(dta - va)} and the liability account {m(dtl)}.""",
    )


def tax_provision_entry_va(p):
    co, s = p["co"], short(p["co"])
    ti, r = D(p["ti"]), D(p["r"])
    dtl_b, dtl_e = D(p["dtl_beg"]), D(p["dtl_end"])
    dta_b, dta_e = D(p["dta_beg"]), D(p["dta_end"])
    va_b, va_e = D(p["va_beg"]), D(p["va_end"])

    def tax(x):
        return whole(rd(x * r / 100))

    cur = tax(ti)
    d_dtl = tax(dtl_e - dtl_b)
    d_dta = tax(dta_e - dta_b)
    d_va = va_e - va_b
    assert d_dtl > 0 and d_dta < 0 and d_va > 0
    key_v = d_dtl - d_dta + d_va
    end_v = tax(dtl_e) - tax(dta_e) + va_e
    pool = {
        "omit_va": (m(d_dtl - d_dta), f"Leaves out the {m(d_va)} increase in the valuation allowance. Raising the allowance against a deferred tax asset is deferred tax expense."),
        "va_sign": (m(d_dtl - d_dta - d_va), f"Treats the {m(d_va)} increase in the valuation allowance as a deferred tax benefit. A larger allowance means less of the asset will be realized, which increases expense."),
        "swap_dta": (m(d_dtl + d_dta + d_va), f"Treats the {m(-d_dta)} decrease in the deferred tax asset as a benefit. A decrease in a deferred tax asset increases deferred tax expense, just as an increase in a deferred tax liability does."),
        "total": (m(cur + key_v), f"Adds the {m(cur)} of current tax ({m(ti)} × {p['r']}%). That is total income tax expense, not its deferred part."),
        "end_balances": (m(end_v), f"Uses the December 31 balances of all three accounts as if they were the year's changes: {m(tax(dtl_e))} liability − {m(tax(dta_e))} asset + {m(va_e)} allowance."),
    }
    key = (m(key_v), f"Correct. {m(d_dtl)} increase in the deferred tax liability + {m(-d_dta)} decrease in the deferred tax asset + {m(d_va)} increase in the valuation allowance.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} records its Year 2 tax provision at December 31, keeping its deferred tax asset, deferred tax liability and valuation allowance in separate accounts. Taxable income for Year 2 is {m(ti)}, and the enacted tax rate is {p['r']}% for all years. {s}'s only temporary differences are prepaid expenses, deducted for tax when paid, of {m(dtl_b)} at January 1 and {m(dtl_e)} at December 31, and its allowance for credit losses, deductible for tax when receivables are written off, of {m(dta_b)} at January 1 and {m(dta_e)} at December 31. The valuation allowance against the deferred tax asset was {m(va_b)} at January 1; after updating its forecasts, {s} sets it at {m(va_e)} at December 31. What deferred income tax expense should {s} record for Year 2?""",
        choices, ans,
        f"""Deferred tax expense is the year's change in the deferred tax accounts. The prepaid expenses are a taxable temporary difference: the deferred tax liability rises by ({m(dtl_e)} − {m(dtl_b)}) × {p['r']}% = {m(d_dtl)}, an expense. The allowance for credit losses is a deductible temporary difference: the deferred tax asset falls by ({m(dta_b)} − {m(dta_e)}) × {p['r']}% = {m(-d_dta)}, also an expense. The valuation allowance rises by {m(va_e)} − {m(va_b)} = {m(d_va)}, an expense, because less of the asset is expected to be realized (ASC 740-10-30-5(e)). Deferred tax expense = {m(d_dtl)} + {m(-d_dta)} + {m(d_va)} = {m(key_v)}. The {m(cur)} of current tax ({m(ti)} × {p['r']}%) is recorded in the same entry but isn't deferred.""",
    )


FAMILIES = [
    ("far-revenue-variable-consideration-0003", A3, "Revenue recognition", AP,
     ["ASC 606-10-32-11 to 32-12 (constraining estimates of variable consideration)", "ASC 606-10-32-14 (reassessing variable consideration at each reporting date)"],
     revenue_variable_constraint, [
        dict(co="Larkspur Sensors Co.", N=8000, P=40, B=6, use=["full_bonus", "ev_bonus", "defer_all"]),
        dict(co="Mertens Sensors Co.", N=5000, P=65, B=9, use=["ev_bonus", "total_units", "defer_all"]),
        dict(co="Oswego Sensors Co.", N=12000, P=28, B=4, use=["full_bonus", "ev_bonus", "defer_all"]),
        dict(co="Prescott Sensors Co.", N=6500, P=52, B=7, use=["full_bonus", "ev_bonus", "total_units"]),
     ], "full_bonus"),
    ("far-revenue-principal-agent-0002", A3, "Revenue recognition", AP,
     ["ASC 606-10-55-36 to 55-40 (principal versus agent indicators)"],
     revenue_principal_agent2, [
        dict(co="BrightRide Inc.", Z=850000, pct=20, Sub=15, M=4000, use=["gross", "no_sub", "no_comm"]),
        dict(co="SwiftHail Co.", Z=620000, pct=25, Sub=12, M=3500, use=["gross", "flip", "no_sub"]),
        dict(co="UrbanGo Co.", Z=1040000, pct=18, Sub=10, M=6000, use=["gross", "no_sub", "no_comm"]),
        dict(co="ZipFleet Co.", Z=430000, pct=22, Sub=18, M=2500, use=["gross", "no_sub", "no_comm"]),
     ], "gross"),
    ("far-revenue-licenses-0002", A3, "Revenue recognition", AP,
     ["ASC 606-10-55-65 (sales- and usage-based royalties for a license of intellectual property)",
      "ASC 606-10-55-58 to 55-63 (right to access versus right to use)"],
     revenue_royalty_license, [
        dict(co="Kestrel Photonics Co.", ppct=6, ppat=250000, pproj=1200000, Fy=32000, fpct=2, fsales=180000, use=["quarter_projection", "full_fee", "omit_fixed"]),
        dict(co="Harrow Acoustics Co.", ppct=5, ppat=320000, pproj=1100000, Fy=24000, fpct=3, fsales=140000, use=["quarter_projection", "omit_fixed", "full_fee"]),
        dict(co="Ivymoor Robotics Co.", ppct=8, ppat=180000, pproj=920000, Fy=40000, fpct="2.5", fsales=220000, use=["estimate_upfront", "quarter_projection", "full_fee"]),
        dict(co="Juniper Dynamics Co.", ppct=4, ppat=410000, pproj=1400000, Fy=48000, fpct=3, fsales=260000, use=["quarter_projection", "omit_patent", "omit_fixed"]),
     ], "quarter_projection"),
    ("far-revenue-contract-costs-0004", A3, "Revenue recognition", AP,
     ["ASC 340-40-15-3 (costs within the scope of another Topic)",
      "ASC 340-40-25-1 to 25-8 (incremental costs of obtaining a contract; costs to fulfill a contract)",
      "ASC 340-40-35-1 (amortization)"],
     contract_costs_scope, [
        dict(co="Trebarwith Systems Co.", sd="January 1", start="March 1", mo=10, off=2, Cm=54000, S=72000, EQ=36000, INV=7200, eq="forklifts", sup="packing materials", use=["include_eq", "wrong_start", "comm_only"]),
        dict(co="Delabole Systems Co.", sd="February 1", start="April 1", mo=9, off=2, Cm=43200, S=57600, EQ=28800, INV=10800, eq="handling carts", sup="shipping supplies", use=["comm_only", "setup_only", "include_inv"]),
        dict(co="Zennor Systems Co.", sd="March 1", start="May 1", mo=8, off=2, Cm=64800, S=86400, EQ=46800, INV=14400, eq="pallet jacks", sup="crating materials", use=["wrong_start", "include_eq", "include_inv"]),
        dict(co="Marazion Systems Co.", sd="April 1", start="July 1", mo=6, off=3, Cm=72000, S=108000, EQ=54000, INV=16200, eq="dock lifts", sup="packaging supplies", use=["comm_only", "setup_only", "wrong_start"]),
     ], "include_eq"),
    ("far-nfp-contributed-services-0003", A3, "Revenue recognition", AP,
     ["ASC 958-605-25-16 (contributed services: creating or enhancing a nonfinancial asset; specialized skills)"],
     nfp_services_asset, [
        dict(org="Fenwick Arts Center", A=14000, C=9000, D=5000, E=4000, use=["skip_shed", "expense_shed", "include_mail"]),
        dict(org="Garrity Arts Center", A=11000, C=7000, D=4500, E=3500, use=["skip_shed", "skip_tech", "include_lawn"]),
        dict(org="Holloway Arts Center", A=18000, C=12000, D=8000, E=5000, use=["expense_shed", "include_mail", "include_lawn"]),
        dict(org="Ivester Arts Center", A=9500, C=6000, D=4000, E=3000, use=["skip_shed", "skip_tech", "expense_shed"]),
     ], "skip_shed"),
    ("far-nfp-contributed-services-0004", A3, "Revenue recognition", AP,
     ["ASC 958-605-25-16 (contributed services: creating or enhancing a nonfinancial asset; specialized skills)",
      "ASC 958-605 (services received from personnel of an affiliate, ASU 2013-06)"],
     nfp_services_construction, [
        dict(org="Brantley Health Outreach", cash=410000, A=26000, P=18000, Cv=3000, use=["omit_aff", "expense_aff", "expense_all"]),
        dict(org="Castleton Health Outreach", cash=325000, A=21000, P=15000, Cv=2500, use=["omit_aff", "expense_all", "include_cer"]),
        dict(org="Dunwoody Health Outreach", cash=540000, A=34000, P=24000, Cv=4000, use=["expense_aff", "expense_all", "include_cer"]),
        dict(org="Elmcrest Health Outreach", cash=275000, A=17000, P=12000, Cv=2000, use=["omit_aff", "expense_aff", "expense_all"]),
     ], "omit_aff"),
    ("far-nfp-contributions-0003", A3, "Revenue recognition", AP,
     ["ASC 958-605-25 (unconditional and conditional promises to give)",
      "ASC 958-605-20 (definition of a contribution, including cancellation of a liability)",
      "ASC 958-605-30 and ASC 958-310-35 (measuring contributions and promises to give)"],
     nfp_contributions_current, [
        dict(org="Perrin Community Clinic", P=45000, M=18000, R=60000, L=25000, use=["include_r", "omit_inv", "omit_forgive"]),
        dict(org="Quimby Community Clinic", P=60000, M=25000, R=80000, L=32000, use=["omit_inv", "omit_forgive", "omit_promise"]),
        dict(org="Radburn Community Clinic", P=36000, M=14000, R=50000, L=20000, use=["include_r", "omit_forgive", "omit_promise"]),
        dict(org="Sawbridge Community Clinic", P=72000, M=30000, R=100000, L=40000, use=["omit_inv", "omit_forgive", "omit_promise"]),
     ], "include_r"),
    ("far-fair-value-in-use-0001", A3, "Fair value measurements", AP,
     ["ASC 820-10-35-10A to 35-10E (highest and best use; assets used in combination)", "ASC 820-10-55-3D (cost approach)"],
     fv_in_use, [
        dict(co="Pentire Bottling Co.", asset="capping machine", line="bottling", Lin=1150000, Lsep=700000, scrap=85000, new_cost=240000, phys=38000, func=22000, use=["scrap", "no_func", "no_phys"]),
        dict(co="Quethiock Dairy Co.", asset="filling machine", line="dairy-packaging", Lin=940000, Lsep=560000, scrap=60000, new_cost=190000, phys=25000, func=15000, use=["scrap", "no_phys", "gross_new"]),
        dict(co="Rosudgeon Canning Co.", asset="seaming machine", line="canning", Lin=1400000, Lsep=820000, scrap=100000, new_cost=300000, phys=50000, func=30000, use=["scrap", "no_func", "gross_new"]),
        dict(co="Stithian Brewing Co.", asset="pasteurizer", line="brewing", Lin=1020000, Lsep=610000, scrap=70000, new_cost=210000, phys=28000, func=17000, use=["no_func", "no_phys", "gross_new"]),
     ], "scrap"),
    ("far-fair-value-liability-0001", A3, "Fair value measurements", AP,
     ["ASC 820-10-35-16 (fair value of liabilities: transfer assumption)", "ASC 820-10-35-17 to 35-18 (nonperformance risk)"],
     fv_liability_nonperformance, [
        dict(co="Trewince Insurance Co.", face=500000, n=5, rf=4, r=3, r2="1.5", stale=1, use=["risk_free_only", "counterparty", "stale"]),
        dict(co="Ventongimps Assurance Co.", face=650000, n=4, rf="3.5", r="2.5", r2=1, stale=4, use=["risk_free_only", "counterparty", "stale"]),
        dict(co="Wendron Mutual Co.", face=380000, n=6, rf="4.5", r="3.5", r2=2, stale="1.5", use=["risk_free_only", "stale", "counterparty"]),
        dict(co="Yelverton Guaranty Co.", face=720000, n=3, rf=3, r=2, r2="0.5", stale=3, use=["counterparty", "stale", "risk_free_only"]),
     ], "risk_free_only"),
    ("far-lessee-finance-0004", A3, "Lessee accounting", AP,
     ["ASC 842-10-30-5(f) (lease payments: residual value guarantees owed by the lessee)",
      "ASC 842-20-30-5 (initial measurement of the right-of-use asset; initial direct costs)", "ASC 842-10-30-9 to 30-10 (initial direct costs: incremental costs only)"],
     lessee_third_party_rvg, [
        dict(co="Tredinnick Fabrication Co.", asset="a forging press", short="press", ins="Harbor Mutual", n=5, i=7, pay=60000, g=30000, idc=9000, legal=6500, use=["include_g", "incl_legal", "wrong_annuity"]),
        dict(co="Ushant Mills Co.", asset="an extrusion line", short="line", ins="Keystone Surety", n=6, i=6, pay=46000, g=22000, idc=7000, legal=5200, use=["include_g", "undiscounted_g", "wrong_annuity"]),
        dict(co="Veryan Forgeworks Co.", asset="a stamping press", short="press", ins="Lantern Indemnity", n=4, i=8, pay=80000, g=35000, idc=12000, legal=8400, use=["omit_idc", "incl_legal", "wrong_annuity"]),
        dict(co="Wendron Castings Co.", asset="a die-casting machine", short="machine", ins="Meridian Assurance", n=5, i="6.5", pay=52000, g=26000, idc=8000, legal=5800, use=["include_g", "incl_legal", "wrong_annuity"]),
     ], "include_g"),
    ("far-lessee-operating-0006", A3, "Lessee accounting", AP,
     ["ASC 842-20-30-3 (discount rate; private-company risk-free rate election by class of asset, as amended by ASU 2021-09)",
      "ASC 842-10-30-5 (lease payments)"],
     lessee_riskfree_deposit, [
        dict(co="Antrobus Textiles Co.", n=6, pay=54000, sd=10000, rf="4.5", ib=7, use=["add_sd", "ibr", "subtract_sd"]),
        dict(co="Bowness Textiles Co.", n=5, pay=72000, sd=15000, rf=4, ib="7.5", use=["add_sd", "subtract_sd", "ibr"]),
        dict(co="Calstock Textiles Co.", n=7, pay=40000, sd=8000, rf=5, ib="7.5", use=["add_sd", "full_annuity", "ibr"]),
        dict(co="Delamere Textiles Co.", n=4, pay=96000, sd=20000, rf="3.5", ib=6, use=["full_annuity", "subtract_sd", "ibr"]),
     ], "add_sd"),
    ("far-lessee-finance-0005", A3, "Lessee accounting", AP,
     ["ASC 842-10-30-5(c) (lease payments: purchase option reasonably certain to be exercised)",
      "ASC 842-20-30-5 (right-of-use asset; initial direct costs)",
      "ASC 842-20-35-8 (amortization period of the right-of-use asset)"],
     lessee_purchase_option_cost, [
        dict(co="Elmsworth Fabrication Co.", asset="a CNC machining center", short="machine", n=5, u=10, pay=78000, opt=40000, fvexp=150000, idc=15000, i=6, use=["term_amort", "no_option", "omit_idc"]),
        dict(co="Framlingham Textiles Co.", asset="a weaving machine", short="machine", n=4, u=8, pay=62000, opt=30000, fvexp=110000, idc=9000, i=5, use=["term_amort", "year1_interest", "omit_idc"]),
        dict(co="Gillingham Robotics Co.", asset="a robotic welding cell", short="cell", n=6, u=12, pay=97000, opt=45000, fvexp=180000, idc=20000, i=7, use=["no_option", "omit_idc", "year1_interest"]),
        dict(co="Harpenden Logistics Co.", asset="an automated sorting system", short="system", n=5, u=10, pay=88000, opt=50000, fvexp=170000, idc=16000, i="6.5", use=["term_amort", "no_option", "year1_interest"]),
     ], "no_option"),
    ("far-lessee-operating-0007", A3, "Lessee accounting", AP,
     ["ASC 842-20-25-6 (operating lease cost; variable payments not based on an index or a rate)",
      "ASC 842-10-30-5 (lease payments net of lease incentives)"],
     lessee_stepdown_cost, [
        dict(co="Inkberrow Retail Co.", pays=[70000, 62000, 54000, 46000, 38000], incentive=20000, pt=9000, use=["cash_basis", "no_incentive", "omit_pt"]),
        dict(co="Juniper Retail Co.", pays=[90000, 80000, 70000, 60000, 50000], incentive=25000, pt=12000, use=["omit_pt", "incentive_upfront", "incentive_as_revenue"]),
        dict(co="Kelmarsh Retail Co.", pays=[55000, 49000, 43000, 37000, 31000], incentive=15000, pt=7000, use=["no_incentive", "omit_pt", "incentive_upfront"]),
        dict(co="Lillington Retail Co.", pays=[110000, 98000, 86000, 74000, 62000], incentive=30000, pt=15000, use=["cash_basis", "no_incentive", "incentive_as_revenue"]),
     ], "no_incentive"),
    ("far-income-taxes-provision-0004", A3, "Accounting for income taxes", AP,
     ["ASC 740-10-25 (temporary and permanent differences)", "ASC 740-10-30 (current and deferred tax expense)"],
     tax_provision_installment, [
        dict(co="Oakhurst Corp.", bi=640000, lip=50000, golf=18000, gp=120000, coll=40000, est=110000, r=25, use=["ignore_inst", "net_est", "golf_ded"]),
        dict(co="Pinehollow Corp.", bi=480000, lip=35000, golf=12000, gp=90000, coll=30000, est=70000, r=21, use=["golf_ded", "net_est", "deduct_all_gp"]),
        dict(co="Queensgate Corp.", bi=720000, lip=60000, golf=24000, gp=150000, coll=50000, est=130000, r=25, use=["tax_lip", "ignore_inst", "deduct_all_gp"]),
        dict(co="Ridgemont Corp.", bi=560000, lip=42000, golf=15000, gp=100000, coll=35000, est=95000, r=24, use=["golf_ded", "deduct_all_gp", "tax_lip"]),
     ], "ignore_inst", ASOF_TAX),
    ("far-income-taxes-deferred-0004", A3, "Accounting for income taxes", AP,
     ["ASC 740-10-25 (temporary differences)", "ASC 740-10-30-5 (measuring deferred taxes; valuation allowance)",
      "ASC 740-10-45-4 (deferred taxes classified as noncurrent)"],
     tax_deferred_installment_litigation, [
        dict(co="Saltburn Corp.", inst=180000, lit=260000, litc=220000, va=8000, r=25, use=["cur_portion", "no_va", "va_on_dtl"]),
        dict(co="Tissington Corp.", inst=140000, lit=210000, litc=150000, va=6000, r=21, use=["cur_portion", "va_on_dtl", "no_va"]),
        dict(co="Ulverscroft Corp.", inst=220000, lit=320000, litc=240000, va=10000, r=25, use=["cur_portion", "va_on_dtl", "no_inst"]),
        dict(co="Wrenbury Corp.", inst=160000, lit=235000, litc=175000, va=7000, r=24, use=["no_inst", "no_va", "cur_portion"]),
     ], "cur_portion", ASOF_TAX),
    ("far-income-taxes-provision-0005", A3, "Accounting for income taxes", AP,
     ["ASC 740-10-30-5 (measuring deferred tax assets and liabilities; valuation allowance)", "ASC 740-10-25 (temporary differences)"],
     tax_provision_entry_va, [
        dict(co="Alresford Corp.", ti=540000, r=25, dtl_beg=160000, dtl_end=210000, dta_beg=90000, dta_end=70000, va_beg=5000, va_end=12000, use=["omit_va", "va_sign", "total"]),
        dict(co="Bramhope Corp.", ti=360000, r=21, dtl_beg=120000, dtl_end=150000, dta_beg=60000, dta_end=45000, va_beg=1500, va_end=4000, use=["omit_va", "total", "swap_dta"]),
        dict(co="Charlecote Corp.", ti=620000, r=25, dtl_beg=200000, dtl_end=260000, dta_beg=110000, dta_end=80000, va_beg=6000, va_end=15000, use=["va_sign", "swap_dta", "total"]),
        dict(co="Dalbury Corp.", ti=430000, r=24, dtl_beg=140000, dtl_end=175000, dta_beg=75000, dta_end=55000, va_beg=3000, va_end=10000, use=["omit_va", "va_sign", "swap_dta"]),
     ], "omit_va", ASOF_TAX),
]


def blind_files(items, scratch):
    lines, keys = ["# FAR batch 16: blind verification input", "",
                   "Each block is one version of a question. Solve each independently; choose one letter.", ""], {}
    for it in items:
        for k, v in enumerate([it] + list(it.get("variants") or [])):
            label = f"{it['id']} v{k}"
            lines += [f"## {label}", "", v["stem"], ""]
            lines += [f"{c['id']}. {c['text']}" for c in v["choices"]] + [""]
            keys[label] = v["answer"]
    with open(os.path.join(scratch, "b16-blind.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(scratch, "b16-keys.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys, f, indent=1)
    print(f"blind file: {len(keys)} versions")


def main():
    items = [family(*f) for f in FAMILIES]
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
    assert len(items) == 16 and len({it["id"] for it in items}) == 16
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
    if SCRATCH:
        os.makedirs(SCRATCH, exist_ok=True)
        blind_files(items, SCRATCH)
    if "--dry-run" in sys.argv:
        print("dry run: nothing written")
        return
    write_items(items, CONTENT)


if __name__ == "__main__":
    main()
