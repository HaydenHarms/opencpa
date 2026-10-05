"""FAR batch 16 — 16 items written from scratch, Area III — Select Transactions only (a slice run in
parallel with batch 17, which covers III.A.*, III.B.*, III.G.*; no shared ids or tasks).

Plan: a third item on III.C.d (five-step model: variable consideration under the constraint, principal
versus agent in a different industry, and the sales-/usage-based royalty exception for licenses of IP —
aspects the existing seven III.C.d items don't cover), a fourth on III.C.e (contract costs: the scope
exclusion for costs within other Topics, such as PP&E and inventory), a third and fourth on III.C.f (NFP
contributed services: unskilled labor that creates or enhances a nonfinancial asset, and a specialized
interpreter), a third on III.C.g (NFP contributions: a short-term promise not discounted, a measurable
barrier, fair value versus carrying amount), a second and third on III.E.b (fair value: the in-use versus
in-exchange premise, and nonperformance risk in measuring a liability), a fourth and fifth on III.F.c
(lessee assets/liabilities: a third-party residual value guarantee excluded from lease payments, and the
private-company risk-free rate election with a security deposit excluded), a sixth and seventh on III.F.d
(lessee lease cost: amortizing the right-of-use asset over the asset's useful life when a purchase option
is reasonably certain, and a decreasing rent schedule with a lease incentive and a non-index variable
payment), and a fourth on III.D.c, III.D.d and III.D.e (income taxes: an installment sale and permanent
differences; an installment sale, a litigation accrual and a valuation allowance; and a tax provision
journal entry with a valuation allowance change). Every Analysis item... there are none in this batch;
every item is Application. Target mix: 16 Application items, Area III only. Scope and skill tags follow
the AICPA CPA Exam Blueprints effective January 2026.

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
from common import AP, attach_variants, audit, finalize, fix_articles, mcq as _mcq, variant, write_items  # noqa: E402
from variants import m, pick, rd  # noqa: E402

A3 = "Area III — Select Transactions"
NOTE = "Batch 16. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
SCRATCH = os.environ.get("B16_SCRATCH")
ASOF_TAX = "U.S. GAAP (ASC 740) and federal tax law in effect for 2026; the rate is as stated in the stem"


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


def family(id, area, topic, skill, refs, build, params, twist, asof=None):
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
    amts = re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", v["stem"])
    dup = sorted({a for a in amts if amts.count(a) > 1})
    if dup:
        print(f"REPEAT {label}: stem repeats {', '.join(dup)}", file=sys.stderr)
    for c in v["choices"]:
        for a in re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", c["text"]):
            if a in amts:
                print(f"REPEAT {label}: choice {a} equals a stem amount", file=sys.stderr)


def spacing(label, v):
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
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"
    nums = [float(re.match(r"^\$?([\d,]+(?:\.\d+)?)", v).group(1).replace(",", "")) for v in vals]
    assert len(set(nums)) == len(nums), f"two choices share a leading amount: {vals}"


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
    i = D(rate_pct) / 100
    return rd(pv_annuity_ordinary(rate_pct, n) * (D(1) + i), "0.0001")


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
        f"""On July 1, Year 1, {co} begins shipping a newly developed sensor to a customer under a multi-year supply contract; the contract price is {m(P)} a unit, and {s} expects to ship about {int(Ntot):,} units over the contract's life. In addition, {s} will earn a {m(B)}-a-unit bonus on every unit shipped in Year 1 if an industry standards board approves the sensor's new calibration method by December 31, Year 1 — a decision {s}'s president calls a coin flip, because the board has never evaluated a method like this one and has given no indication which way it will rule. {s} shipped {int(N):,} units in Year 1. How much revenue should {s} recognize for the units shipped in Year 1?""",
        choices, ans,
        f"""The {m(P)} base price is unconditional and is recognized as each unit ships: {int(N):,} × {m(P)} = {m(key_v)}. The {m(B)}-a-unit bonus is variable consideration, but the board's decision is highly susceptible to factors outside {s}'s influence and {s} has no relevant experience with a similar method, so including any part of it in the transaction price is excluded under the constraint on estimates of variable consideration (ASC 606-10-32-11 to 32-13) until the board rules. Revenue for Year 1 = {m(key_v)}.""",
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
        f"""An entity is a principal if it controls the good or service before it transfers to the customer; a key indicator is primary responsibility for fulfilling the promise. Here the drivers, not {s}, are responsible for completing each ride and bear the risk of a problem with it, so {s} is an agent for the ride fares even though it sets the price and collects the cash: it recognizes only its {m(commission)} fee ({p['pct']}% × {m(Z)}). The subscription is {s}'s own service, with no other party involved, so it is recognized gross: {m(Sub)} × {int(Mn):,} = {m(sub_rev)}. Total revenue = {m(key_v)}.""",
    )


def revenue_royalty_license(p):
    co, s = p["co"], short(p["co"])
    ppct, ppat, pproj = D(p["ppct"]), D(p["ppat"]), D(p["pproj"])
    F, fpct, fsales = D(p["F"]), D(p["fpct"]), D(p["fsales"])
    patent_roy = rd(ppat * ppct / 100)
    franch_roy = rd(fsales * fpct / 100)
    key_v = patent_roy + F + franch_roy
    pool = {
        "estimate_upfront": (m(rd(pproj * ppct / 100) + F + franch_roy), f"Applies the {p['ppct']}% rate to the {m(pproj)} of sales the manufacturer projected for the year when the agreement was signed, instead of the {m(ppat)} actually sold this quarter. A sales-based royalty for a license of intellectual property is recognized only as the underlying sales occur, never estimated in advance (ASC 606-10-55-65)."),
        "omit_patent": (m(F + franch_roy), f"Leaves out the {m(patent_roy)} patent royalty entirely."),
        "omit_fixed": (m(patent_roy + franch_roy), f"Leaves out the {m(F)} fixed brand license fee for the quarter."),
        "gross_no_rate": (m(ppat + F + fsales), f"Adds the full {m(ppat)} and {m(fsales)} of sales to the {m(F)} fee without applying either royalty rate."),
    }
    key = (m(key_v), f"Correct. ({p['ppct']}% × {m(ppat)}) + {m(F)} + ({p['fpct']}% × {m(fsales)}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} licenses two pieces of intellectual property for the quarter. It licenses a patented sensor-calibration process, mature functional technology {s} doesn't plan to update, to a manufacturer in exchange for a {p['ppct']}% royalty on the manufacturer's net sales of products using the process, with no fixed fee and no minimum guarantee; when the agreement was signed, {s} projected those sales would be about {m(pproj)} for the year, but actual sales using the process were {m(ppat)} for the quarter. {s} also licenses its brand name to a franchisee, together with marketing support {s} will keep providing, for a fixed {m(F)} a quarter plus a {p['fpct']}% royalty on the franchisee's sales; franchisee sales for the quarter were {m(fsales)}. How much revenue should {s} recognize for the quarter from these two licenses?""",
        choices, ans,
        f"""Consideration in the form of a sales- or usage-based royalty for a license of intellectual property is recognized only as the underlying sales occur, regardless of whether the license is a right to use (the patent) or a right to access (the brand name, supported by {s}'s ongoing marketing) (ASC 606-10-55-65); {s} doesn't estimate the royalty from its sales projection. Patent royalty = {p['ppct']}% × {m(ppat)} = {m(patent_roy)}. The brand license's fixed fee, {m(F)}, is earned for the quarter, and its royalty = {p['fpct']}% × {m(fsales)} = {m(franch_roy)}. Total revenue = {m(key_v)}.""",
    )


# ── III.C.e — Determine recognition and measurement of contract costs ──────


def contract_costs_scope(p):
    co, s = p["co"], short(p["co"])
    term = 36
    Cm, Setup = D(p["Cm"]), D(p["S"])
    total = Cm + Setup
    key_v = whole(total * (term - p["mo"]) / term)
    wrong_v = whole(total * (term - p["mo"] - p["off"]) / term)
    pool = {
        "wrong_start": (m(wrong_v), f"Starts amortizing from the {p['sd']} signing date instead of the {p['start']} service start. Amortization of a capitalized contract cost begins when the services to which it relates begin (ASC 340-40-35-1)."),
        "include_eq": (m(key_v + p["EQ"]), f"Capitalizes the {m(p['EQ'])} of {p['eq']} as a contract cost asset. Property, plant and equipment is within the scope of ASC 360, not ASC 340-40 (ASC 340-40-15-3), even though {s} bought it only for this contract."),
        "include_inv": (m(key_v + p["INV"]), f"Capitalizes the {m(p['INV'])} of {p['sup']} as a contract cost asset. Materials and supplies to be consumed in performing the services are inventory within the scope of ASC 330 until used, not a contract cost asset."),
        "no_amort": (m(total), f"Reports the full {m(total)} capitalized, without amortization. Both the commission and the setup labor are amortized consistent with the transfer of the services to which they relate."),
    }
    key = (m(key_v), f"Correct. ({m(Cm)} + {m(Setup)}) × {term - p['mo']}/{term}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} signed a three-year contract on {p['sd']}, Year 1, to provide outsourced logistics services beginning {p['start']}, Year 1; no renewal is expected. Four amounts went on {s}'s books because of this engagement: a {m(Cm)} commission the salesperson earned only by closing the deal; {m(Setup)} paid for labor configuring the customer's shipment-tracking workflows — work tied specifically to this contract, built to be used for as long as {s} serves this customer, and priced into the fees {s} will collect; {m(p['EQ'])} for {p['eq']} that {s} will dedicate to this customer for now but redeploy to other jobs once the contract ends; and {m(p['INV'])} for {p['sup']} that will be used up in delivering the services. Each capitalized cost is written off evenly by the month, over the span it benefits. What should {s} carry as its contract cost assets under ASC 340-40 at December 31, Year 1?""",
        choices, ans,
        f"""The commission is an incremental cost of obtaining the contract, and the configuration labor meets the criteria for a cost to fulfill a contract (ASC 340-40-25-1 to 25-8); both are capitalized and amortized from {p['start']}, when the related services begin, over the 36-month term: ({m(Cm)} + {m(Setup)}) × {term - p['mo']}/{term} = {m(key_v)}. The {p['eq']} is property, plant and equipment {s} will use beyond this contract, within the scope of ASC 360 (ASC 340-40-15-3), and the {p['sup']} is inventory within the scope of ASC 330 until consumed; neither is a contract cost asset under ASC 340-40, even though both relate to this contract.""",
    )


# ── III.C.f — Determine NFP revenue for contributed services ───────────────


def nfp_services_asset(p):
    org, s = p["org"], short(p["org"])
    A, C, Dv, E = D(p["A"]), D(p["C"]), D(p["D"]), D(p["E"])
    key_v = A + C
    pool = {
        "skip_unskilled": (m(A), f"Omits the {m(C)} shed. Recognizing contributed services that create or enhance a nonfinancial asset doesn't require the volunteers who provide them to have specialized skills (ASC 958-605-25-16)."),
        "skip_architect": (m(C), f"Omits the architect's {m(A)} design work, a specialized service {s} would otherwise have purchased."),
        "include_d": (m(A + C + Dv), f"Includes the {m(Dv)} of the database consultant's time helping organize the raffle. Her specialized skill wasn't used in its specialty that day, so those services aren't recognized."),
        "include_e": (m(A + C + E), f"Includes the {m(E)} of lawn mowing. Routine upkeep needs no specialized skill and doesn't enhance a nonfinancial asset, so it isn't recognized."),
    }
    key = (m(key_v), f"Correct. The architect's design work ({m(A)}) and the volunteer-built shed, which enhanced {s}'s property ({m(C)}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, received these donated services. A volunteer architect designed a new gallery wing, services {s} would otherwise have paid {m(A)} for. A group of volunteers with no construction training built a storage shed from a prefabricated kit, work worth {m(C)} at the rates a handyman service would charge, enhancing {s}'s property even though the volunteers used no specialized skill. A volunteer who is a database consultant spent a day helping organize {s}'s annual raffle, time worth {m(Dv)} at her usual consulting rate, work that didn't call on her database expertise. Other volunteers mowed {s}'s lawn throughout the year, time worth {m(E)} at local wage rates. What amount should {s} recognize as contributed services revenue for Year 1?""",
        choices, ans,
        f"""Contributed services are recognized if they (a) create or enhance a nonfinancial asset, whether or not the people providing them have specialized skills, or (b) require specialized skills, are provided by people with those skills, and would typically need to be purchased if not donated (ASC 958-605-25-16). The architect's design work meets both tests ({m(A)}); the shed meets only the first, but that is enough ({m(C)}). The consultant's specialized skill wasn't used in its specialty, and routine lawn care needs no special skill and creates no asset, so neither is recognized. Contributed services revenue = {m(key_v)}.""",
    )


def nfp_services_three(p):
    org, s = p["org"], short(p["org"])
    A, B, C, Dv, E = D(p["A"]), D(p["B"]), D(p["C"]), D(p["D"]), D(p["E"])
    key_v = A + B + C
    pool = {
        "omit_interp": (m(A + B), f"Leaves out the {m(C)} interpreter. Translating for attendees at the fair uses her specialized skill, which {s} would otherwise have paid an agency for, so it meets the second recognition test."),
        "include_d": (m(A + B + C + Dv), f"Includes the {m(Dv)} of front-desk volunteers. Answering phones needs no specialized skill and creates no nonfinancial asset."),
        "include_e": (m(A + B + C + E), f"Includes the {m(E)} of the board member's time. Reviewing financial reports as a board member is governance, not the specialized skill {s} would otherwise purchase."),
        "omit_plumb": (m(A + C), f"Leaves out the {m(B)} kitchen renovation. The plumbers' work enhanced a nonfinancial asset, {s}'s kitchen, which is recognized whether or not the volunteers had a specialized skill."),
    }
    key = (m(key_v), f"Correct. Dentist ({m(A)}) + kitchen renovation ({m(B)}) + interpreter ({m(C)}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, received these donated services. A volunteer dentist provided free dental care at {s}'s clinic, care {s} would otherwise have paid a local practice {m(A)} for. Volunteer plumbers, tradespeople who normally charge for their work, renovated {s}'s community kitchen, replacing its fixtures and layout, labor worth {m(B)}. A professional interpreter translated for non-English-speaking families at {s}'s one-day benefits fair, work {s} would otherwise have hired an agency to do, valued at {m(C)} at her usual rate. Other volunteers answered phones at {s}'s front desk, time worth {m(Dv)} at local wage rates. A retired engineer who serves on {s}'s board spent time reviewing {s}'s financial reports at board meetings, time valued at {m(E)} at her former consulting rate. What amount should {s} recognize as contributed services revenue for Year 1?""",
        choices, ans,
        f"""Contributed services are recognized if they (a) create or enhance a nonfinancial asset, or (b) require specialized skills, are provided by people with those skills, and would typically need to be purchased if not donated (ASC 958-605-25-16). The dentist's care meets test (b) ({m(A)}); the plumbers' renovation enhances {s}'s kitchen, meeting test (a) regardless of their skill ({m(B)}); the interpreter's specialized skill is used in its specialty and {s} would otherwise have hired an agency, meeting test (b) ({m(C)}). Front-desk volunteers need no specialized skill and create no asset, and the engineer is exercising board governance, not the specialized skill {s} would otherwise purchase. Contributed services revenue = {m(key_v)}.""",
    )


# ── III.C.g — Calculate NFP contributions of financial and nonfinancial assets ──


def nfp_contributions_current(p):
    org, s = p["org"], short(p["org"])
    P, Mv, R, V, Vb = D(p["P"]), D(p["M"]), D(p["R"]), D(p["V"]), D(p["Vb"])
    disc = D(p["disc"])
    key_v = P + Mv + V
    pool = {
        "pv_short": (m(rd(P * disc) + Mv + V), f"Discounts the {m(P)} promise by a present value factor even though it is due in 60 days, within {s}'s operating cycle. An unconditional promise collectible currently is recognized at the amount expected to be collected, without discounting (ASC 958-605-30-7)."),
        "include_r": (m(key_v + R), f"Includes the {m(R)} foundation pledge. It is conditioned on a measurable barrier, opening the satellite clinic, that {s} hasn't yet overcome, so it isn't revenue yet."),
        "book_vehicle": (m(P + Mv + Vb), f"Records the van at the donor's {m(Vb)} carrying amount. Contributed nonfinancial assets are measured at their fair value when received, {m(V)}."),
        "omit_inv": (m(P + V), f"Leaves out the {m(Mv)} of donated medical supplies, as if giving them away later means {s} recognizes no contribution now. Contributed goods are recognized at fair value when received, even though {s} will distribute them."),
    }
    key = (m(key_v), f"Correct. {m(P)} (not discounted) + {m(Mv)} + {m(V)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {org}, a not-for-profit entity, received the following. A donor signed an unconditional promise to pay {s} {m(P)} within 60 days, collectible in the ordinary course of {s}'s operations. A local pharmaceutical distributor donated medical supplies for {s} to distribute to patients, with a fair value of {m(Mv)}. A regional foundation pledged {m(R)}, payable only if {s} opens a satellite clinic by a specified date, a measurable barrier {s} hasn't yet overcome. A donor gave {s} a used van for transporting patients, with a fair value of {m(V)}, which was carried on the donor's own books at {m(Vb)}. What total contribution revenue should {s} recognize for Year 1?""",
        choices, ans,
        f"""An unconditional promise to give that is collectible currently is recognized at the amount expected to be collected, with no present value discount (ASC 958-605-30-7): {m(P)}. The medical supplies and the van are contributed nonfinancial assets, measured at fair value when received rather than the donor's carrying amount: {m(Mv)} and {m(V)}. The foundation's pledge depends on a measurable barrier {s} hasn't overcome, so it isn't revenue until the barrier is met. Contribution revenue = {m(P)} + {m(Mv)} + {m(V)} = {m(key_v)}.""",
    )


# ── III.E.b — Use assumptions and approaches to measure fair value ─────────


def fv_in_use(p):
    co, s = p["co"], short(p["co"])
    scrap, new_cost, phys, func = D(p["scrap"]), D(p["new_cost"]), D(p["phys"]), D(p["func"])
    key_v = new_cost - phys - func
    pool = {
        "scrap": (m(scrap), f"Uses the {m(scrap)} the {p['asset']} would bring sold apart from the line, for parts or scrap. That is its value on an in-exchange (standalone) premise, which applies only if a standalone sale maximized its value; here using it within the line does."),
        "no_func": (m(new_cost - phys), f"Deducts only physical deterioration. Functional obsolescence, the {m(func)} newer models' extra speed is worth, is also deducted in a cost approach."),
        "no_phys": (m(new_cost - func), f"Deducts only functional obsolescence. Physical deterioration, {m(phys)}, is also deducted in a cost approach."),
        "gross_new": (m(new_cost), f"Uses the {m(new_cost)} cost of a new substitute without any deduction for deterioration or obsolescence."),
    }
    key = (m(key_v), f"Correct. {m(new_cost)} − {m(phys)} − {m(func)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} owns a specialized {p['asset']} that is part of an integrated production line; used together with the line's other equipment, which market participants could also acquire, the {p['asset']} lets the whole line run at its highest and best use, generating far more value in combination than any single piece would generate alone. No active market exists for secondhand {p['asset']}s identical to this one, and sold apart from the line, for parts or scrap, it would bring only {m(scrap)}. {s}'s appraiser instead estimates what it would cost currently to construct a new substitute {p['asset']} of comparable utility, {m(new_cost)}, and reduces that amount by {m(phys)} of physical deterioration and {m(func)} of functional obsolescence, because newer models run faster. What is the fair value of the {p['asset']}?""",
        choices, ans,
        f"""Fair value of a nonfinancial asset reflects its highest and best use by market participants, which may be in combination with other assets as a group (an in-use premise) rather than on a standalone basis (in-exchange), when using it that way maximizes its value and the complementary assets are available to market participants (ASC 820-10-35-10 to 35-14). Because the {p['asset']} is worth more used within the line, fair value is measured on the in-use premise, here estimated with a cost approach: {m(new_cost)} − {m(phys)} − {m(func)} = {m(key_v)}. The {m(scrap)} standalone price is its in-exchange value, which would govern only if a standalone sale maximized its value instead.""",
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
    pool = {
        "risk_free_only": (m(whole(rd(face * rf_f))), f"Discounts at the {p['rf']}% risk-free rate alone, leaving out {s}'s own nonperformance risk. Fair value of a liability must include the effect of the reporting entity's own credit standing (ASC 820-10-35-16 to 35-17A)."),
        "counterparty": (m(whole(rd(face * comp_f))), f"Uses the {p['r2']}% premium a stronger prospective buyer of {s} said it would need. Fair value reflects {s}'s own nonperformance risk as the obligor, not a third party's stronger credit standing, because {s} hasn't transferred the obligation."),
        "stale": (m(whole(rd(face * stale_f))), f"Uses the {p['stale']}% premium that applied before {s}'s downgrade. Nonperformance risk is measured at {s}'s credit standing as of the measurement date, not an earlier one."),
        "undiscounted": (m(face), f"Reports the {m(face)} face amount with no discount for the time value of money."),
        "extra_year": (m(whole(rd(face * extra_f))), f"Discounts the obligation as if it were payable in {n + 1} years instead of {n}, one year too many."),
    }
    key = (m(key_v), f"Correct. {m(face)} discounted {n} years at {p['rf'] + p['r']}% ({p['rf']}% risk-free + {p['r']}% for {s}'s own nonperformance risk).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} must measure the fair value of a {m(face)} obligation it owes a counterparty, payable in a lump sum in {n} years, assuming the obligation is transferred to a market participant of comparable credit standing. The risk-free rate for a {n}-year term is {p['rf']}%. Because of a recent downgrade, market participants would require a {p['r']}% premium for {s}'s own nonperformance risk as of the measurement date; before the downgrade, that premium was only {p['stale']}%. A prospective buyer of {s} with a stronger credit profile said it would need only a {p['r2']}% premium for the same obligation, but {s} itself hasn't transferred the obligation to that buyer. What is the fair value of {s}'s obligation?""",
        choices, ans,
        f"""Fair value of a liability assumes transfer to a market participant of comparable credit standing and must include the effect of the reporting entity's own nonperformance risk, including its own credit risk, measured as of the measurement date — not a stronger counterparty's credit standing and not a stale, pre-downgrade spread (ASC 820-10-35-16 to 35-17A). The discount rate is {p['rf']}% risk-free + {p['r']}% for {s}'s own current nonperformance risk = {p['rf'] + p['r']}%. Fair value = {m(face)} × {key_f} = {m(key_v)}.""",
    )


# ── III.F.c — Calculate lessee assets and liabilities and prepare journal entries ──


def lessee_third_party_rvg(p):
    co, s = p["co"], short(p["co"])
    n, i = p["n"], D(p["i"])
    pay, g, idc = D(p["pay"]), D(p["g"]), D(p["idc"])
    af = pv_annuity_ordinary(i, n)
    sf = pv_single(i, n)
    af_due = pv_annuity_due(i, n)
    liab = rd(pay * af)
    key_v = whole(liab + idc)
    pool = {
        "include_g": (m(whole(liab + rd(g * sf) + idc)), f"Adds {m(g)} × {sf} = {m(rd(g * sf))} for the insurer's residual value guarantee. A residual value guarantee by a party unrelated to {s} isn't a lease payment, no matter how likely it is to be paid (ASC 842-10-15-30 to 15-35); only a guarantee by the lessee or a party related to the lessee is included."),
        "half_g": (m(whole(liab + rd(g * sf / 2) + idc)), f"Includes half of {m(g)} × {sf}, as if only the probable part of the insurer's guarantee counted. The guarantee is excluded entirely because an unrelated third party made it, not because of how likely it is to be paid."),
        "omit_idc": (m(whole(liab)), f"Leaves out the {m(idc)} of initial direct costs, which {s} adds to the right-of-use asset."),
        "wrong_annuity": (m(whole(rd(pay * af_due) + idc)), f"Discounts the payments as an annuity due. Payments are due at the end of each year, so the ordinary annuity factor applies."),
    }
    key = (m(key_v), f"Correct. {m(pay)} × {af} = {m(liab)}, + {m(idc)} of initial direct costs.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} leases {p['asset']}, which has no alternative use to the lessor at the end of the term, for {n} years and classifies the lease as a finance lease. Payments of {m(pay)} are due each December 31. An insurance company unrelated to {s} — not {s} itself and not a party related to {s} — has separately guaranteed the lessor a residual value of {m(g)} for the equipment at lease end. {s} paid {m(idc)} at commencement, an incremental cost of obtaining the lease. The rate implicit in the lease isn't readily determinable, and {s}'s incremental borrowing rate is {i}%. What amount should {s} initially recognize as its right-of-use asset?""",
        choices, ans,
        f"""Lease payments include an amount probable of being owed under a residual value guarantee only when the lessee or a party related to the lessee made the guarantee; a guarantee by an unrelated third party, such as the insurer here, isn't a lease payment at all (ASC 842-10-15-30 to 15-35), whatever its amount or probability. The lease liability is the present value of the payments: {m(pay)} × {af} = {m(liab)}. The right-of-use asset adds the {m(idc)} of initial direct costs {s} paid: {m(liab)} + {m(idc)} = {m(key_v)}.""",
    )


def lessee_riskfree_deposit(p):
    co, s = p["co"], short(p["co"])
    n, rf = p["n"], D(p["rf"])
    pay, sd = D(p["pay"]), D(p["sd"])
    af_due = pv_annuity_due(rf, n)
    af_ord = pv_annuity_ordinary(rf, n)
    full = rd(pay * af_due)
    key_v = whole(full - pay)
    pool = {
        "full_annuity": (m(whole(full)), f"Doesn't deduct the {m(pay)} payment {s} made at commencement. That payment reduces the liability at once."),
        "add_sd": (m(whole(full - pay + sd)), f"Adds the {m(sd)} security deposit to the liability. The deposit is refundable and isn't rent, so it is a separate deposit asset, not a lease payment (ASC 842-10-15)."),
        "subtract_sd": (m(whole(full - pay - sd)), f"Subtracts the {m(sd)} security deposit from the liability instead of recording it as a separate asset."),
        "ordinary_af": (m(whole(rd(pay * af_ord))), f"Discounts the payments with the ordinary annuity factor, {af_ord}, as if each payment were due at year end. Payments here are due at the start of each year, including at commencement."),
    }
    key = (m(key_v), f"Correct. {m(pay)} × {af_due} = {m(full)}, less the {m(pay)} paid at commencement.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}, a private company that has elected the risk-free rate practical expedient for all its asset classes (ASC 842-20-30-3), leases warehouse space for {n} years under an operating lease. Annual payments of {m(pay)} are due each January 1, beginning at commencement, and {s} made the first payment on January 1, Year 1. {s} also paid the landlord a refundable security deposit of {m(sd)} at commencement, which isn't rent and will be returned, undamaged space permitting, when the lease ends. The risk-free rate for a {n}-year lease term is {rf}%, which {s} uses instead of determining a rate implicit in the lease or its own incremental borrowing rate. What amount should {s} initially measure as its lease liability, immediately after the first payment?""",
        choices, ans,
        f"""As a private company, {s} may elect to discount its leases at a risk-free rate instead of determining its incremental borrowing rate (ASC 842-20-30-3), which it has done here. The security deposit is refundable and isn't rent, so it is recognized as a separate deposit asset, not part of the lease liability. Because payments are due at the start of each period, the liability uses an annuity-due factor: {m(pay)} × {af_due} = {m(full)}, less the {m(pay)} paid at commencement, leaving {m(key_v)}.""",
    )


# ── III.F.d — Calculate lessee lease costs ──────────────────────────────────


def lessee_purchase_option_cost(p):
    co, s = p["co"], short(p["co"])
    n, u, i = p["n"], p["u"], D(p["i"])
    liab, pay = D(p["liab"]), D(p["pay"])
    interest1 = rd(liab * i)
    principal1 = pay - interest1
    bal1 = liab - principal1
    interest2 = rd(bal1 * i)
    amort_correct = whole(rd(liab / u))
    amort_wrong = whole(rd(liab / n))
    key_v = interest2 + amort_correct
    pool = {
        "term_amort": (m(interest2 + amort_wrong), f"Amortizes the right-of-use asset over the {n}-year lease term, {m(liab)} ÷ {n} = {m(amort_wrong)}. Because the purchase option is reasonably certain to be exercised, {s} amortizes it over the equipment's {u}-year useful life instead (ASC 842-20-25-4 to 25-6)."),
        "only_interest": (m(interest2), f"Includes only interest. A finance lease also amortizes the right-of-use asset."),
        "only_amort": (m(amort_correct), f"Includes only amortization. A finance lease also has interest expense."),
        "wrong_year": (m(interest1 + amort_correct), f"Uses Year 1 interest, {m(interest1)}, instead of reducing the liability for the Year 1 principal payment first."),
    }
    key = (m(key_v), f"Correct. Year 2 interest {m(interest2)} on a {m(bal1)} opening liability, plus {m(amort_correct)} of amortization over the equipment's {u}-year useful life.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} leases {p['asset']} under a lease it classifies as a finance lease. The lease term is {n} years, but the equipment's total useful life is {u} years, and the lease grants {s} an option to purchase the equipment at a price so far below its expected fair value at that date that {s} is reasonably certain to exercise it. The lease liability at commencement is {m(liab)} (rounded), the annual payment of {m(pay)} is due each December 31, and the discount rate is {i * 100}%. {s} amortizes the right-of-use asset straight-line. What total lease-related expense does {s} recognize in Year 2?""",
        choices, ans,
        f"""Because the purchase option is reasonably certain to be exercised, {s} expects to own the equipment after the lease, so it amortizes the right-of-use asset over the equipment's {u}-year useful life rather than the {n}-year lease term (ASC 842-20-25-4 to 25-6): {m(liab)} ÷ {u} = {m(amort_correct)}. Year 1: interest {m(interest1)}, principal reduction {m(principal1)}, ending liability {m(bal1)}. Year 2 interest = {m(bal1)} × {i * 100}% = {m(interest2)}. Total Year 2 expense = {m(interest2)} + {m(amort_correct)} = {m(key_v)}.""",
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
        "cash_basis": (m(pays[0] + pt), f"Uses the Year 1 cash payment of {m(pays[0])} instead of the straight-line average. Operating lease cost is recognized straight-line over the term, free of the year-to-year payment schedule."),
        "no_incentive": (m(no_incentive + pt), f"Spreads the full {m(total_pay)} of payments without deducting the {m(incentive)} leasehold improvement allowance. Lease incentives received reduce the amount recognized as lease cost (ASC 842-20-25-6 to 25-7)."),
        "omit_pt": (m(core), f"Leaves out the {m(pt)} of property tax reimbursement. It is a variable payment that isn't based on an index or a rate, so it isn't part of the straight-line calculation, but it is still lease cost, recognized as incurred."),
        "incentive_as_revenue": (m(no_incentive + pt + whole(rd(incentive / 5))), f"Adds a {m(whole(rd(incentive / 5)))} share of the {m(incentive)} incentive to cost instead of subtracting it from the payments being spread."),
    }
    key = (m(key_v), f"Correct. ({m(total_pay)} total payments − {m(incentive)} incentive) ÷ 5 = {m(core)}, plus {m(pt)} of variable property tax reimbursement.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} leases retail space for 5 years, which it classifies as an operating lease. Rent, due each December 31, is {m(pays[0])} in Year 1 and falls each year after that: {m(pays[1])} in Year 2, {m(pays[2])} in Year 3, {m(pays[3])} in Year 4 and {m(pays[4])} in Year 5, reflecting the landlord's higher cost of the space while {s}'s leasehold improvements are newest. At commencement, the landlord paid {s} {m(incentive)} in cash as a leasehold improvement allowance. {s} also reimburses the landlord each year for its pro-rata share of the property taxes actually assessed on the building, a variable payment that isn't fixed or tied to an index; the reimbursement for Year 1 is {m(pt)}. What total lease cost should {s} recognize for Year 1?""",
        choices, ans,
        f"""Operating lease cost for the fixed payments, net of lease incentives received, is recognized straight-line over the lease term (ASC 842-20-25-6 to 25-7): ({m(total_pay)} total payments − {m(incentive)} incentive) ÷ 5 = {m(core)}. The property tax reimbursement doesn't depend on an index or a rate, so it is excluded from that calculation and recognized as incurred: {m(pt)}. Total lease cost = {m(core)} + {m(pt)} = {m(key_v)}.""",
    )


# ── III.D.c/d/e — Income taxes ──────────────────────────────────────────────


def tax_provision_installment(p):
    co, s = p["co"], short(p["co"])
    bi, lip, golf = D(p["bi"]), D(p["lip"]), D(p["golf"])
    gp, coll, est, r = D(p["gp"]), D(p["coll"]), D(p["est"]), D(p["r"])

    def pair(taxable, expense):
        cur = whole(rd(taxable * r / 100))
        return cur, whole(rd(expense * r / 100))

    cur, exp = pair(bi - lip + golf - (gp - coll), bi - lip + golf)
    payable = cur - est
    key_v = (payable, exp)

    cur_lip, exp_lip = pair(bi + golf - (gp - coll), bi + golf)
    pay_lip = cur_lip - est

    cur_ig, exp_ig = pair(bi - lip + golf, bi - lip + golf)
    pay_ig = cur_ig - est

    cur_ng, exp_ng = pair(bi - lip - (gp - coll), bi - lip)
    pay_ng = cur_ng - est

    pool = {
        "tax_lip": (f"{m(pay_lip)} payable; {m(exp_lip)} expense", f"Taxes the {m(lip)} of life insurance proceeds. Proceeds from life insurance on an executive, where {s} is the beneficiary, are a permanent difference excluded from taxable income and from tax expense."),
        "ignore_installment": (f"{m(pay_ig)} payable; {m(exp_ig)} expense", f"Taxes the full {m(gp)} installment sale gross profit currently, as books do, and records no deferred tax on it. For tax, {s} uses the installment method and is taxed only on the {m(coll)} collected this year; the remaining {m(gp - coll)} gives rise to a deferred tax liability, which happens to leave total expense unchanged but understates current tax payable."),
        "no_golf_adjust": (f"{m(pay_ng)} payable; {m(exp_ng)} expense", f"Deducts the {m(golf)} of club dues for tax as well as for books. Nondeductible club dues are a permanent difference, added back for both current tax and total tax expense."),
        "full_payable": (f"{m(cur)} payable; {m(exp)} expense", f"Reports the whole {m(cur)} of current tax as payable, without applying the {m(est)} of estimated payments {s} already made."),
    }
    key = (f"{m(payable)} payable; {m(exp)} expense", f"Correct. Current tax {m(cur)} − {m(est)} prepaid = {m(payable)} payable; expense = taxable income adjusted only for permanent differences, ({m(bi)} − {m(lip)} + {m(golf)}) × {p['r']}% = {m(exp)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} must work out both its Year 2 income taxes payable and its Year 2 income tax expense. Pretax financial income for the year is {m(bi)}, which includes {m(lip)} of proceeds from company-owned life insurance on an executive's death, a nontaxable amount, and is stated after deducting {m(golf)} of nondeductible country club dues. {s} books the full {m(gp)} gross profit on an installment sale in the year of sale, but on its tax return the gross profit is taxed only as collected under the installment method, and only {m(coll)} was collected (and taxed) this year. The enacted tax rate is {p['r']}% for every year, {s} anticipates plenty of future taxable income, and during the year it remitted {m(est)} of estimated tax payments, carried on its books as a prepaid asset. Netting those prepayments against current tax, what should {s} report as Year 2 income taxes payable, and what is its Year 2 income tax expense?""",
        choices, ans,
        f"""Taxable income = {m(bi)} − {m(lip)} (nontaxable, permanent) + {m(golf)} (nondeductible, permanent) − {m(gp - coll)} (installment gross profit not yet taxed) = {m(bi - lip + golf - (gp - coll))}; current tax = {m(cur)}, less {m(est)} of estimated payments = {m(payable)} payable. The installment sale creates a deferred tax liability of {m(gp - coll)} × {p['r']}%, which exactly offsets the current-tax effect of deferring that gross profit, so total expense equals the rate applied to book income adjusted only for the permanent differences: ({m(bi)} − {m(lip)} + {m(golf)}) × {p['r']}% = {m(exp)}.""",
    )


def tax_deferred_installment_litigation(p):
    co, s = p["co"], short(p["co"])
    inst, lit, va, r, litc = D(p["inst"]), D(p["lit"]), D(p["va"]), D(p["r"]), D(p["litc"])
    net_before_va = whole(rd((lit - inst) * r / 100))
    key_v = net_before_va - va
    pool = {
        "no_va": (m(net_before_va), f"Omits the {m(va)} valuation allowance. Management has concluded it is more likely than not that {m(va)} of the deferred tax asset won't be realized (ASC 740-10-30-5)."),
        "va_wrong_sign": (m(net_before_va + va), f"Adds the {m(va)} allowance to the asset instead of deducting it. A valuation allowance reduces a deferred tax asset to the amount more likely than not to be realized."),
        "no_inst": (m(whole(rd(lit * r / 100)) - va), f"Leaves out the deferred tax liability on the installment sale. Its untaxed gross profit is a taxable temporary difference that offsets part of the litigation accrual's deferred tax asset."),
        "pretax_no_rate": (m((lit - inst) - va), f"Doesn't multiply the {m(lit - inst)} net temporary difference by the {p['r']}% tax rate before deducting the allowance."),
        "cur_portion": (m(whole(rd((litc - inst) * r / 100)) - va), f"Limits the deferred tax asset to the {m(litc)} of the litigation accrual {s} expects to pay within a year, leaving out the {m(lit - litc)} expected in later years. A deferred tax asset is based on the entire temporary difference; deferred taxes aren't classified as current or noncurrent at all (ASC 740-10-45-4)."),
    }
    key = (m(key_v), f"Correct. ({m(lit)} − {m(inst)}) × {p['r']}% = {m(net_before_va)}, less the {m(va)} valuation allowance.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} is measuring its deferred taxes at December 31, Year 2. It has a taxable temporary difference of {m(inst)} from an installment sale: it recognized the full gross profit for books in the year of sale, but for tax the gross profit is taxed only as collected. It has also accrued a {m(lit)} loss contingency from pending litigation, deductible for tax only when paid; of that accrual, {s} expects to pay {m(litc)} within the next year and the rest later. The enacted tax rate is {p['r']}% for all years. Based on its forecast of future taxable income, {s}'s management concludes that it is more likely than not that {m(va)} of the resulting deferred tax asset will not be realized. What net deferred tax asset should {s} report at December 31, Year 2?""",
        choices, ans,
        f"""The installment sale gives a taxable temporary difference ({m(inst)}), a deferred tax liability of {m(inst)} × {p['r']}%; the full litigation accrual gives a deductible temporary difference ({m(lit)}), a deferred tax asset of {m(lit)} × {p['r']}%, regardless of when the cash will be paid (deferred taxes are never classified as current). Net deferred tax asset before considering realization = ({m(lit)} − {m(inst)}) × {p['r']}% = {m(net_before_va)}. A valuation allowance reduces it by the {m(va)} management concludes is not more likely than not to be realized (ASC 740-10-30-5): {m(net_before_va)} − {m(va)} = {m(key_v)}.""",
    )


def tax_provision_entry_va(p):
    co, s = p["co"], short(p["co"])
    ti, r = D(p["ti"]), D(p["r"])
    dtl_b, dtl_e = D(p["dtl_beg"]), D(p["dtl_end"])
    dta_b, dta_e = D(p["dta_beg"]), D(p["dta_end"])
    va_b, va_e = D(p["va_beg"]), D(p["va_end"])
    cur = whole(rd(ti * r / 100))
    d_dtl = whole(rd((dtl_e - dtl_b) * r / 100))
    d_dta = whole(rd((dta_e - dta_b) * r / 100))
    d_va = va_e - va_b
    key_v = cur + d_dtl - d_dta + d_va
    pool = {
        "omit_va": (m(cur + d_dtl - d_dta), f"Leaves out the {m(d_va)} increase in the valuation allowance against the deferred tax asset. {s} debits income tax expense for an increase in the allowance, just like an increase in the net deferred tax liability."),
        "va_sign": (m(cur + d_dtl - d_dta - d_va), f"Credits income tax expense for the {m(d_va)} increase in the valuation allowance. Increasing an allowance against a deferred tax asset increases, not decreases, income tax expense."),
        "swap_dta": (m(cur + d_dtl + d_dta + d_va), f"Debits income tax expense for the {m(abs(d_dta))} change in the deferred tax asset in the same direction as the change in the deferred tax liability. An increase in a deferred tax asset is a deferred tax benefit, which reduces expense; a decrease increases it."),
        "end_balances": (m(cur + whole(rd(dtl_e * r / 100)) - whole(rd(dta_e * r / 100)) + d_va), f"Uses the December 31 deferred tax balances directly instead of the year's change in each account. The January 1 balances were already recorded in earlier years."),
    }
    key = (m(key_v), f"Correct. Current tax {m(cur)} + {m(d_dtl)} increase in the deferred tax liability − ({m(d_dta)}) change in the deferred tax asset + {m(d_va)} increase in the valuation allowance.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} posts its tax provision as one combined entry at year-end, carrying its deferred tax asset, deferred tax liability and the valuation allowance against that asset in separate ledger accounts. Taxable income for Year 2 comes to {m(ti)}, taxed at the {p['r']}% rate enacted for every year. {s} began the year with cumulative taxable temporary differences of {m(dtl_b)} and deductible temporary differences of {m(dta_b)}, carrying a {m(va_b)} allowance against the deferred tax asset those create; by year-end the temporary differences had grown to {m(dtl_e)} and {m(dta_e)}, and a revised forecast calls for the allowance to stand at {m(va_e)} instead. For the entry recording this provision, what amount belongs on the debit side of income tax expense?""",
        choices, ans,
        f"""The entry debits income tax expense and credits income taxes payable for current tax, {m(ti)} × {p['r']}% = {m(cur)}. The deferred tax liability increases by ({m(dtl_e)} − {m(dtl_b)}) × {p['r']}% = {m(d_dtl)}, a credit and a debit to expense. The deferred tax asset changes by ({m(dta_e)} − {m(dta_b)}) × {p['r']}% = {m(d_dta)}; a decrease is a debit to expense. The valuation allowance increases by {m(va_e)} − {m(va_b)} = {m(d_va)}, also debited to expense, because a larger allowance means less of the deferred tax asset will be realized. Total debit to income tax expense = {m(cur)} + {m(d_dtl)} − ({m(d_dta)}) + {m(d_va)} = {m(key_v)}.""",
    )


FAMILIES = [
    ("far-revenue-variable-consideration-0003", A3, "Revenue recognition", AP,
     ["ASC 606-10-32-11 to 32-13 (constraining estimates of variable consideration)"],
     revenue_variable_constraint, [
        dict(co="Larkspur Sensors Co.", N=8000, P=40, B=6, use=["full_bonus", "total_units", "defer_all"]),
        dict(co="Mertens Sensors Co.", N=5000, P=65, B=9, use=["ev_bonus", "total_units", "defer_all"]),
        dict(co="Oswego Sensors Co.", N=12000, P=28, B=4, use=["full_bonus", "ev_bonus", "defer_all"]),
        dict(co="Prescott Sensors Co.", N=6500, P=52, B=7, use=["full_bonus", "ev_bonus", "total_units"]),
     ], "full_bonus"),
    ("far-revenue-principal-agent-0002", A3, "Revenue recognition", AP,
     ["ASC 606-10-55-36 to 55-40 (principal versus agent indicators)"],
     revenue_principal_agent2, [
        dict(co="BrightRide Inc.", Z=850000, pct=20, Sub=15, M=4000, use=["gross", "flip", "no_sub"]),
        dict(co="SwiftHail Co.", Z=620000, pct=25, Sub=12, M=3500, use=["gross", "no_sub", "no_comm"]),
        dict(co="UrbanGo Co.", Z=1040000, pct=18, Sub=10, M=6000, use=["gross", "flip", "no_comm"]),
        dict(co="ZipFleet Co.", Z=430000, pct=22, Sub=18, M=2500, use=["flip", "no_sub", "no_comm"]),
     ], "gross"),
    ("far-revenue-licenses-0002", A3, "Revenue recognition", AP,
     ["ASC 606-10-55-65 (sales- and usage-based royalties for a license of intellectual property)"],
     revenue_royalty_license, [
        dict(co="Kestrel Photonics Co.", ppct=6, ppat=250000, pproj=1000000, F=8000, fpct=2, fsales=180000, use=["estimate_upfront", "omit_patent", "omit_fixed"]),
        dict(co="Harrow Acoustics Co.", ppct=5, ppat=320000, pproj=1500000, F=6000, fpct=3, fsales=140000, use=["estimate_upfront", "omit_fixed", "gross_no_rate"]),
        dict(co="Ivymoor Robotics Co.", ppct=8, ppat=180000, pproj=820000, F=10000, fpct="2.5", fsales=220000, use=["estimate_upfront", "omit_patent", "gross_no_rate"]),
        dict(co="Juniper Dynamics Co.", ppct=4, ppat=410000, pproj=2000000, F=12000, fpct=3, fsales=260000, use=["omit_patent", "omit_fixed", "gross_no_rate"]),
     ], "estimate_upfront"),
    ("far-revenue-contract-costs-0004", A3, "Revenue recognition", AP,
     ["ASC 340-40-15-3 (scope exclusion for costs within the scope of another Topic)", "ASC 340-40-25-1 to 25-8 (incremental costs of obtaining a contract; costs to fulfill a contract)", "ASC 340-40-35-1 (amortization)"],
     contract_costs_scope, [
        dict(co="Trebarwith Systems Co.", sd="January 10", start="March 1", mo=10, off=2, Cm=54000, S=72000, EQ=38000, INV=9000, eq="forklifts", sup="packing materials", use=["include_eq", "include_inv", "no_amort"]),
        dict(co="Delabole Systems Co.", sd="February 14", start="April 1", mo=9, off=1, Cm=48000, S=60000, EQ=25000, INV=7000, eq="handling carts", sup="shipping supplies", use=["wrong_start", "include_eq", "no_amort"]),
        dict(co="Zennor Systems Co.", sd="March 5", start="May 1", mo=8, off=2, Cm=72000, S=90000, EQ=48000, INV=14000, eq="pallet jacks", sup="crating materials", use=["wrong_start", "include_eq", "include_inv"]),
        dict(co="Marazion Systems Co.", sd="April 20", start="June 1", mo=7, off=2, Cm=75000, S=105000, EQ=50000, INV=15000, eq="loading equipment", sup="packaging stock", use=["include_eq", "include_inv", "no_amort"]),
     ], "include_eq"),
    ("far-nfp-contributed-services-0003", A3, "Revenue recognition", AP,
     ["ASC 958-605-25-16 (contributed services: creating or enhancing a nonfinancial asset; specialized skills)"],
     nfp_services_asset, [
        dict(org="Fenwick Arts Center", A=22000, C=9000, D=6000, E=4000, use=["skip_unskilled", "include_d", "include_e"]),
        dict(org="Garrity Arts Center", A=18000, C=7000, D=5000, E=3500, use=["skip_architect", "include_d", "include_e"]),
        dict(org="Holloway Arts Center", A=30000, C=12000, D=8000, E=5000, use=["skip_unskilled", "skip_architect", "include_d"]),
        dict(org="Ivester Arts Center", A=16000, C=6000, D=4500, E=3000, use=["skip_unskilled", "skip_architect", "include_e"]),
     ], "skip_unskilled"),
    ("far-nfp-contributed-services-0004", A3, "Revenue recognition", AP,
     ["ASC 958-605-25-16 (contributed services: creating or enhancing a nonfinancial asset; specialized skills)"],
     nfp_services_three, [
        dict(org="Brantley Health Outreach", A=26000, B=15000, C=5000, D=7000, E=9000, use=["omit_interp", "include_d", "include_e"]),
        dict(org="Castleton Health Outreach", A=19000, B=11000, C=4000, D=5000, E=6000, use=["omit_interp", "include_e", "omit_plumb"]),
        dict(org="Dunwoody Health Outreach", A=32000, B=20000, C=6000, D=8000, E=10000, use=["include_d", "include_e", "omit_plumb"]),
        dict(org="Elmcrest Health Outreach", A=15000, B=9000, C=3500, D=4000, E=5000, use=["omit_interp", "include_d", "omit_plumb"]),
     ], "omit_interp"),
    ("far-nfp-contributions-0003", A3, "Revenue recognition", AP,
     ["ASC 958-605-25 (conditional versus unconditional promises; measurable barriers)", "ASC 958-605-30-7 (promises collectible currently; nonfinancial assets at fair value)"],
     nfp_contributions_current, [
        dict(org="Perrin Community Clinic", P=45000, disc="0.97", M=18000, R=60000, V=22000, Vb=9000, use=["pv_short", "include_r", "book_vehicle"]),
        dict(org="Quimby Community Clinic", P=60000, disc="0.95", M=25000, R=80000, V=30000, Vb=12000, use=["pv_short", "include_r", "omit_inv"]),
        dict(org="Radburn Community Clinic", P=36000, disc="0.98", M=14000, R=50000, V=16000, Vb=6000, use=["pv_short", "book_vehicle", "omit_inv"]),
        dict(org="Sawbridge Community Clinic", P=72000, disc="0.96", M=30000, R=100000, V=38000, Vb=15000, use=["include_r", "book_vehicle", "omit_inv"]),
     ], "pv_short"),
    ("far-fair-value-in-use-0001", A3, "Fair value measurements", AP,
     ["ASC 820-10-35-10 to 35-14 (highest and best use; in-use versus in-exchange premise)", "ASC 820-10-55 (cost approach)"],
     fv_in_use, [
        dict(co="Pentire Bottling Co.", asset="capping machine", scrap=85000, new_cost=240000, phys=38000, func=22000, use=["scrap", "no_func", "no_phys"]),
        dict(co="Quethiock Dairy Co.", asset="filling machine", scrap=60000, new_cost=190000, phys=25000, func=15000, use=["scrap", "no_phys", "gross_new"]),
        dict(co="Rosudgeon Canning Co.", asset="seaming machine", scrap=100000, new_cost=300000, phys=50000, func=30000, use=["scrap", "no_func", "gross_new"]),
        dict(co="Stithians Brewing Co.", asset="pasteurizer", scrap=70000, new_cost=210000, phys=28000, func=17000, use=["no_func", "no_phys", "gross_new"]),
     ], "scrap"),
    ("far-fair-value-liability-0001", A3, "Fair value measurements", AP,
     ["ASC 820-10-35-16 to 35-17A (fair value of liabilities; nonperformance risk)"],
     fv_liability_nonperformance, [
        dict(co="Trewince Insurance Co.", face=500000, n=5, rf=4, r=3, r2="1.5", stale=1, use=["risk_free_only", "counterparty", "stale"]),
        dict(co="Ventongimps Assurance Co.", face=650000, n=4, rf="3.5", r="2.5", r2=1, stale="0.5", use=["risk_free_only", "counterparty", "extra_year"]),
        dict(co="Wendron Mutual Co.", face=380000, n=6, rf="4.5", r="3.5", r2=2, stale="1.5", use=["risk_free_only", "stale", "extra_year"]),
        dict(co="Yelverton Guaranty Co.", face=720000, n=3, rf=3, r=2, r2="0.5", stale=0, use=["counterparty", "stale", "extra_year"]),
     ], "risk_free_only"),
    ("far-lessee-finance-0004", A3, "Lessee accounting", AP,
     ["ASC 842-10-15-30 to 15-35 (lease payments; residual value guarantees)", "ASC 842-20-30 (initial measurement of the right-of-use asset)"],
     lessee_third_party_rvg, [
        dict(co="Tredinnick Fabrication Co.", asset="a forging press", n=5, i=7, pay=60000, g=30000, idc=9000, use=["include_g", "omit_idc", "wrong_annuity"]),
        dict(co="Ushant Mills Co.", asset="an extrusion line", n=6, i=6, pay=45000, g=22000, idc=7000, use=["include_g", "half_g", "omit_idc"]),
        dict(co="Veryan Forgeworks Co.", asset="a stamping press", n=4, i=8, pay=80000, g=35000, idc=12000, use=["half_g", "omit_idc", "wrong_annuity"]),
        dict(co="Wendron Castings Co.", asset="a die-casting machine", n=5, i="6.5", pay=52000, g=26000, idc=8000, use=["include_g", "half_g", "wrong_annuity"]),
     ], "include_g"),
    ("far-lessee-operating-0006", A3, "Lessee accounting", AP,
     ["ASC 842-20-30-3 (private-company risk-free rate practical expedient)", "ASC 842-10-15 (lease payments exclude a refundable security deposit)"],
     lessee_riskfree_deposit, [
        dict(co="Antrobus Textiles Co.", n=6, pay=54000, sd=10000, rf="4.5", use=["add_sd", "full_annuity", "ordinary_af"]),
        dict(co="Bowness Textiles Co.", n=5, pay=72000, sd=15000, rf=4, use=["add_sd", "subtract_sd", "ordinary_af"]),
        dict(co="Calstock Textiles Co.", n=7, pay=40000, sd=8000, rf=5, use=["add_sd", "full_annuity", "subtract_sd"]),
        dict(co="Delamere Textiles Co.", n=4, pay=95000, sd=20000, rf="3.5", use=["full_annuity", "subtract_sd", "ordinary_af"]),
     ], "add_sd"),
    ("far-lessee-finance-0005", A3, "Lessee accounting", AP,
     ["ASC 842-20-25-4 to 25-6 (amortization of the right-of-use asset; purchase option reasonably certain)"],
     lessee_purchase_option_cost, [
        dict(co="Elmsworth Fabrication Co.", asset="a CNC machining center", n=5, u=10, liab=320000, pay=78000, i="0.06", use=["term_amort", "only_interest", "only_amort"]),
        dict(co="Framlingham Textiles Co.", asset="a weaving machine", n=4, u=8, liab=210000, pay=62000, i="0.05", use=["term_amort", "only_amort", "wrong_year"]),
        dict(co="Gillingham Robotics Co.", asset="a robotic welding cell", n=6, u=12, liab=480000, pay=97000, i="0.07", use=["term_amort", "only_interest", "wrong_year"]),
        dict(co="Harpenden Logistics Co.", asset="an automated sorting system", n=5, u=10, liab=360000, pay=88000, i="0.065", use=["only_interest", "only_amort", "wrong_year"]),
     ], "term_amort"),
    ("far-lessee-operating-0007", A3, "Lessee accounting", AP,
     ["ASC 842-20-25-6 to 25-7 (single lease cost; lease incentives)", "ASC 842-10-15 (variable lease payments not based on an index or a rate)"],
     lessee_stepdown_cost, [
        dict(co="Inkberrow Retail Co.", pays=[70000, 62000, 54000, 46000, 38000], incentive=20000, pt=9000, use=["cash_basis", "no_incentive", "omit_pt"]),
        dict(co="Juniper Retail Co.", pays=[90000, 80000, 70000, 60000, 50000], incentive=25000, pt=12000, use=["cash_basis", "omit_pt", "incentive_as_revenue"]),
        dict(co="Kelmarsh Retail Co.", pays=[55000, 49000, 43000, 37000, 31000], incentive=15000, pt=7000, use=["no_incentive", "omit_pt", "incentive_as_revenue"]),
        dict(co="Lillington Retail Co.", pays=[110000, 98000, 86000, 74000, 62000], incentive=30000, pt=15000, use=["cash_basis", "no_incentive", "incentive_as_revenue"]),
     ], "no_incentive"),
    ("far-income-taxes-provision-0004", A3, "Accounting for income taxes", AP,
     ["ASC 740-10-25 (temporary and permanent differences)", "ASC 740-10-30 (current and deferred tax expense)"],
     tax_provision_installment, [
        dict(co="Oakhurst Corp.", bi=640000, lip=50000, golf=18000, gp=120000, coll=40000, est=110000, r=25, use=["tax_lip", "ignore_installment", "full_payable"]),
        dict(co="Pinehollow Corp.", bi=480000, lip=35000, golf=12000, gp=90000, coll=30000, est=70000, r=21, use=["tax_lip", "ignore_installment", "no_golf_adjust"]),
        dict(co="Queensgate Corp.", bi=720000, lip=60000, golf=24000, gp=150000, coll=50000, est=130000, r=25, use=["ignore_installment", "no_golf_adjust", "full_payable"]),
        dict(co="Ridgemont Corp.", bi=560000, lip=42000, golf=15000, gp=100000, coll=35000, est=95000, r=24, use=["tax_lip", "no_golf_adjust", "full_payable"]),
     ], "ignore_installment", ASOF_TAX),
    ("far-income-taxes-deferred-0004", A3, "Accounting for income taxes", AP,
     ["ASC 740-10-25 (temporary differences)", "ASC 740-10-30-5 (valuation allowance)"],
     tax_deferred_installment_litigation, [
        dict(co="Saltburn Corp.", inst=180000, lit=260000, litc=220000, va=8000, r=25, use=["no_va", "va_wrong_sign", "no_inst"]),
        dict(co="Tissington Corp.", inst=140000, lit=210000, litc=200000, va=6000, r=21, use=["no_va", "no_inst", "cur_portion"]),
        dict(co="Ulverscroft Corp.", inst=220000, lit=320000, litc=300000, va=10000, r=25, use=["no_va", "va_wrong_sign", "pretax_no_rate"]),
        dict(co="Wrenbury Corp.", inst=160000, lit=235000, litc=225000, va=7000, r=24, use=["va_wrong_sign", "no_inst", "cur_portion"]),
     ], "no_va", ASOF_TAX),
    ("far-income-taxes-provision-0005", A3, "Accounting for income taxes", AP,
     ["ASC 740-10 (current and deferred tax expense)", "ASC 740-10-30-5 (valuation allowance)"],
     tax_provision_entry_va, [
        dict(co="Alresford Corp.", ti=540000, r=25, dtl_beg=160000, dtl_end=210000, dta_beg=90000, dta_end=70000, va_beg=5000, va_end=12000, use=["omit_va", "va_sign", "swap_dta"]),
        dict(co="Bramhope Corp.", ti=360000, r=21, dtl_beg=120000, dtl_end=150000, dta_beg=60000, dta_end=45000, va_beg=4000, va_end=9000, use=["omit_va", "swap_dta", "end_balances"]),
        dict(co="Charlecote Corp.", ti=620000, r=25, dtl_beg=200000, dtl_end=260000, dta_beg=110000, dta_end=80000, va_beg=6000, va_end=15000, use=["omit_va", "va_sign", "end_balances"]),
        dict(co="Dalbury Corp.", ti=430000, r=24, dtl_beg=140000, dtl_end=175000, dta_beg=75000, dta_end=55000, va_beg=3000, va_end=10000, use=["va_sign", "swap_dta", "end_balances"]),
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
