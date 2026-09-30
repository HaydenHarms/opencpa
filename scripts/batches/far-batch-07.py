"""FAR batch 07 — 11 items written from scratch for Area III gaps (plus one Area II payables reconciliation) from
scripts/far-coverage.py: accounting changes and error corrections, contingencies, the five-step model, NFP promises
to give, contract costs and NFP contributed services. Target skill mix 3 / 3 / 5. Scope and skill tags follow the
AICPA CPA Exam Blueprints effective January 2026.

Numeric items ship with three variants each: each item is a builder, parameter set 0 is the item and sets 1-3 are
its variants, and every family must move the key's letter.

Run: python3 scripts/batches/far-batch-07.py   See docs/reviews/far-batch-07.md.
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import os
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(__file__))

from common import AN, AP, RU, attach_variants, audit, finalize, fix_articles, mcq as _mcq, variant, write_items
from variants import m, pick, rd

A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 07. Written from scratch; answers solved and every number and distractor computed in code."
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


def distinct(key_v, pool_vals):
    """No pool value may equal the key or another pool value (a distractor would collapse into another)."""
    vals = [key_v] + list(pool_vals)
    assert len(set(vals)) == len(vals), f"coinciding values: {vals}"


# ── III.A.b Derive the impact of an accounting change or error correction ──


def depreciation_change(p):
    """DDB to straight-line at the start of Year 4: a change in estimate effected by a change in principle.
    The draft applied it retrospectively (cumulative-effect credit to opening retained earnings, SL on cost)."""
    co, s = p["co"], short(p["co"])
    C, n, t = D(p["cost"]), p["life"], D(p["rate"]) / 100
    rate = D(2) / n
    bv = C
    for _ in range(3):
        bv -= bv * rate
    bv = whole(bv)
    ddb_acc = C - bv
    sl_old = whole(C / n)              # draft's Year 4 depreciation (straight-line on original cost)
    sl_cum = 3 * sl_old
    adj_gross = ddb_acc - sl_cum
    adj_net = whole(adj_gross * (1 - t))
    dep4 = whole(bv / (n - 3))         # correct: remaining book value over remaining life
    ddb4 = whole(bv * rate)
    orig4 = whole(bv / n)
    E = p["re0"] + adj_net + p["ni"] - p["div"]
    fix = whole((sl_old - dep4) * (1 - t))
    key_v = E - adj_net + fix
    vals = {
        "as_drafted": E,
        "no_redep": E - adj_net,
        "pretax": E - adj_net + (sl_old - dep4),
        "keep_ddb": E - adj_net + whole((sl_old - ddb4) * (1 - t)),
        "orig_life": E - adj_net + whole((sl_old - orig4) * (1 - t)),
    }
    distinct(key_v, vals.values())
    pool = {
        "as_drafted": (m(vals["as_drafted"]), "Accepts the draft. A change in depreciation method is a change in accounting estimate effected by a change in accounting principle, applied prospectively: no cumulative-effect adjustment to opening retained earnings."),
        "no_redep": (m(vals["no_redep"]), f"Removes the {m(adj_net)} cumulative-effect adjustment but keeps Year 4 depreciation of {m(sl_old)}. Prospectively, the {m(bv)} book value at January 1, Year 4, is depreciated over the {n - 3} remaining years: {m(dep4)}."),
        "pretax": (m(vals["pretax"]), f"Removes the adjustment and recomputes Year 4 depreciation, but adds back the full {m(sl_old - dep4)} reduction in depreciation. Lower depreciation raises income tax expense at {p['rate']}%, so net income rises by only {m(fix)}."),
        "keep_ddb": (m(vals["keep_ddb"]), f"Removes the adjustment but keeps double-declining-balance depreciation ({m(ddb4)}) for Year 4. The new straight-line method applies from January 1, Year 4."),
        "orig_life": (m(vals["orig_life"]), f"Spreads the {m(bv)} book value over the original {n}-year life ({m(orig4)}). Only {n - 3} years of life remain."),
    }
    key = (m(key_v), f"Correct. {m(E)} − {m(adj_net)} cumulative-effect adjustment + {m(fix)} after-tax reduction in Year 4 depreciation.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""On January 1, Year 1, {co} bought a machine for {m(C)}, with a {n}-year life and no salvage value, and depreciated it by the double-declining-balance method. On January 1, Year 4, {s} switched to the straight-line method for the machine because it better reflects how the machine's benefits are now being consumed; the life and salvage value estimates are unchanged. {s}'s draft Year 4 statement of retained earnings shows: January 1 balance as originally reported, {m(p['re0'])}; cumulative effect of change in depreciation method, net of tax, {m(adj_net)} (an increase); net income, {m(p['ni'])}; dividends, {m(p['div'])}; December 31 balance, {m(E)}. Draft net income includes Year 4 depreciation on the machine of {m(sl_old)}. {s}'s tax rate is {p['rate']}% for all effects. What December 31, Year 4, retained earnings should {s} report?""",
        choices, ans,
        f"""A change in depreciation method is a change in accounting estimate effected by a change in accounting principle, so it is applied prospectively: no cumulative-effect adjustment, and no restatement. Book value at January 1, Year 4: {m(C)} less three years of double-declining-balance depreciation ({m(ddb_acc)}) = {m(bv)}. Year 4 straight-line depreciation = {m(bv)} ÷ {n - 3} remaining years = {m(dep4)}, not {m(sl_old)}. Corrections to the draft: remove the {m(adj_net)} adjustment, and raise net income by ({m(sl_old)} − {m(dep4)}) × (1 − {p['rate']}%) = {m(fix)}. {m(E)} − {m(adj_net)} + {m(fix)} = {m(key_v)}.""",
    )


def counterbalancing(p):
    """Errors from Years 1-3 found in Year 4 before closing: which are still uncorrected at January 1, Year 4?"""
    co, s = p["co"], short(p["co"])
    ins = whole(D(p["ins"]) / 3)
    dep = whole(D(p["mach"]) / 5)
    key_v = p["re"] - p["wages"] + ins - 2 * dep
    vals = {
        "inv_y2": key_v + p["inv2"],
        "inv_y1": key_v - p["inv1"],
        "wages": key_v + p["wages"],
        "ins_none": key_v - ins,
        "dep_one": key_v + dep,
        "dep_y4": key_v - dep,
    }
    distinct(key_v, vals.values())
    pool = {
        "inv_y2": (m(vals["inv_y2"]), f"Adds back the {m(p['inv2'])} understatement of Year 2 ending inventory. It understated Year 2 income and overstated Year 3 income by the same amount, so it had reversed by December 31, Year 3."),
        "inv_y1": (m(vals["inv_y1"]), f"Subtracts the {m(p['inv1'])} overstatement of Year 1 ending inventory. That error reversed in Year 2 and no longer affects retained earnings."),
        "wages": (m(vals["wages"]), f"Treats the {m(p['wages'])} of unrecorded Year 3 wages as having corrected itself. It reverses only when Year 4 closes; at January 1, Year 4, retained earnings are still overstated."),
        "ins_none": (m(vals["ins_none"]), f"Treats the insurance error as fully reversed. At December 31, Year 3, one year of coverage ({m(ins)}) remained unexpired and had already been expensed."),
        "dep_one": (m(vals["dep_one"]), f"Subtracts only one year of the missing depreciation ({m(dep)}). Depreciation was omitted for both Year 2 and Year 3."),
        "dep_y4": (m(vals["dep_y4"]), "Includes Year 4 depreciation in the opening adjustment. Year 4 depreciation is a Year 4 expense, not a prior-period adjustment."),
    }
    key = (m(key_v), f"Correct. {m(p['re'])} − {m(p['wages'])} wages + {m(ins)} unexpired insurance − {m(2 * dep)} depreciation.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""Before closing its Year 4 books, {co} reviews its records and finds the following. Its December 31, Year 1, ending inventory was overstated by {m(p['inv1'])}. Its December 31, Year 2, ending inventory was understated by {m(p['inv2'])}. On January 1, Year 2, it paid {m(p['ins'])} for a three-year insurance policy and charged the whole amount to Year 2 expense. A machine bought on January 1, Year 2, for {m(p['mach'])}, with a five-year life and no salvage value, was recorded as equipment but has never been depreciated. Wages of {m(p['wages'])} earned in late December, Year 3, were not accrued; they were paid in January, Year 4, and charged to Year 4 wage expense. Every other amount is correct, and the Year 1 to Year 3 statements have been issued. {s}'s draft Year 4 statement of retained earnings begins with the January 1, Year 4, balance as previously reported, {m(p['re'])}. Ignoring income taxes, what January 1, Year 4, retained earnings, as adjusted, should {s} report?""",
        choices, ans,
        f"""Take each error to its cumulative effect on retained earnings at December 31, Year 3. Year 1 ending inventory overstated: Year 1 income over, Year 2 income under by {m(p['inv1'])}; reversed by the end of Year 2, so no effect. Year 2 ending inventory understated: Year 2 income under, Year 3 income over by {m(p['inv2'])}; reversed by the end of Year 3, so no effect. Insurance: Year 2 expense was overstated by two years' cost and Year 3 expense understated by one year's ({m(ins)}), leaving retained earnings understated by the unexpired {m(ins)}. Depreciation: two years omitted, {m(dep)} a year, so retained earnings are overstated by {m(2 * dep)}. Wages: Year 3 expense understated by {m(p['wages'])}; that reverses only when Year 4 is closed, so opening retained earnings are overstated by {m(p['wages'])}. {m(p['re'])} − {m(p['wages'])} + {m(ins)} − {m(2 * dep)} = {m(key_v)}.""",
    )


# ── III.B.b Calculate amounts of contingencies ──────────────────────────


def remediation(p):
    co, s = p["co"], short(p["co"])
    key_v = p["best2"] + p["paid"] - p["lo1"]
    mid1 = whole((D(p["lo1"]) + p["hi1"]) / 2)
    vals = {
        "mid1": p["best2"] + p["paid"] - mid1,
        "no_pay": p["best2"] - p["lo1"],
        "net_ins": key_v - p["claim"],
        "low2": p["lo2"] + p["paid"] - p["lo1"],
        "hi2": p["hi2"] + p["paid"] - p["lo1"],
        "cash": p["paid"],
    }
    distinct(key_v, vals.values())
    assert min(vals.values()) > 0
    pool = {
        "mid1": (m(vals["mid1"]), f"Assumes the Year 1 accrual was the {m(mid1)} midpoint. When no amount in a range is a better estimate, the minimum ({m(p['lo1'])}) is accrued."),
        "no_pay": (m(vals["no_pay"]), f"Leaves out the {m(p['paid'])} charged against the liability in Year 2. Those payments used up part of the accrual, so the expense must restore it to {m(p['best2'])}."),
        "net_ins": (m(vals["net_ins"]), f"Nets the {m(p['claim'])} insurance claim against the expense. A recovery is recognized only when it is probable, and the insurer disputes coverage."),
        "low2": (m(vals["low2"]), f"Uses the {m(p['lo2'])} low end of the Year 2 range. When one amount in the range is the best estimate ({m(p['best2'])}), that amount is accrued."),
        "hi2": (m(vals["hi2"]), f"Uses the {m(p['hi2'])} high end of the Year 2 range. The best estimate, {m(p['best2'])}, is accrued; the rest of the range is disclosed."),
        "cash": (m(vals["cash"]), "Expenses only the cleanup costs paid in Year 2. The liability is remeasured to the new best estimate, and the change is Year 2 expense."),
    }
    key = (m(key_v), f"Correct. Ending liability {m(p['best2'])} − ({m(p['lo1'])} − {m(p['paid'])} paid) = {m(key_v)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""In Year 1, a state environmental agency designated {co} as a party responsible for cleaning up contamination at a site it formerly operated. At December 31, Year 1, {s}'s engineers estimated the cleanup cost at between {m(p['lo1'])} and {m(p['hi1'])}, with no amount in the range more likely than any other, and {s} recorded its liability in accordance with GAAP. During Year 2, {s} paid {m(p['paid'])} of cleanup costs, charging them to the liability. At December 31, Year 2, an updated study estimates the remaining cost at between {m(p['lo2'])} and {m(p['hi2'])}, with {m(p['best2'])} the most likely amount. {s} has filed a {m(p['claim'])} claim with its insurer, which disputes coverage and has paid nothing. The timing of future payments is not reliably determinable, so the liability is not discounted. What environmental remediation expense should {s} recognize for Year 2?""",
        choices, ans,
        f"""At December 31, Year 1, no amount in the range was a better estimate, so {s} accrued the minimum, {m(p['lo1'])}. Year 2 payments of {m(p['paid'])} reduced the liability to {m(p['lo1'] - p['paid'])}. At December 31, Year 2, the best estimate of remaining costs is {m(p['best2'])}, so the liability is increased by {m(p['best2'])} − {m(p['lo1'] - p['paid'])} = {m(key_v)}, charged to expense (debit remediation expense, credit environmental liability). The disputed insurance claim is not probable of recovery, so it is not recognized and is not netted against the expense.""",
    )


# ── III.B.c Review documentation for recognition versus disclosure ──────


def paired(accr, disc):
    return f"{m(accr)} accrued; {m(disc)} disclosed"


def documents_accrue_disclose(p):
    co, s = p["co"], short(p["co"])
    a, b, c, d, e, f = (p[k] for k in ("lo", "hi", "best", "split", "remote", "overbill"))
    key_v = (c + f, b - c + d)
    vals = {
        "low_end": (a + f, b - a + d),
        "unasserted": (c, b - c + d),
        "remote": (c + f, b - c + d + e),
        "rp_accrued": (c + d + f, b - c),
        "no_excess": (c + f, d),
    }
    distinct(key_v, vals.values())
    pool = {
        "low_end": (paired(*vals["low_end"]), f"Accrues the {m(a)} low end of the product-liability range. The low end is used only when no amount is a better estimate; counsel named {m(c)} as most likely."),
        "unasserted": (paired(*vals["unasserted"]), f"Accrues nothing for the {m(f)} overbilling because the agency hasn't asserted a claim. An unasserted claim is accrued when assertion is probable and a loss is probable and estimable; {s} has decided to report it."),
        "remote": (paired(*vals["remote"]), f"Includes the {m(e)} customer demand in the disclosure. Counsel's advice makes a loss remote, and a remote loss contingency is not disclosed."),
        "rp_accrued": (paired(*vals["rp_accrued"]), f"Accrues the {m(d)} distributor claim. Counsel cannot predict the outcome, so a loss is not probable; it is disclosed, not accrued."),
        "no_excess": (paired(*vals["no_excess"]), f"Discloses only the distributor claim. The exposure above the {m(c)} accrued for the product-liability suit, up to {m(b)}, must also be disclosed."),
    }
    key = (paired(*key_v), f"Correct. Accrue {m(c)} + {m(f)}; disclose {m(b - c)} + {m(d)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""The controller of {co} is reviewing documents before {s}'s December 31 statements are issued. (1) Outside counsel's letter on a product-liability suit states that counsel expects the court to find {s} liable and estimates damages at between {m(a)} and {m(b)}, with {m(c)} the most likely amount. (2) {s}'s insurer has written that it will not cover a {m(d)} claim by a former distributor; counsel's letter on that claim says courts have split on the legal question and counsel cannot predict the outcome. (3) Board minutes note a customer's written demand for {m(e)} for late deliveries, and counsel's advice that the contract's limitation-of-liability clause bars the claim, since courts in the jurisdiction have enforced identical clauses in every reported case. (4) Board minutes record that an internal review confirmed {s} overbilled a state agency {m(f)} during the year, an error the agency has not detected, and that the board has decided to report it to the agency in January; counsel expects the agency to demand repayment in full. In its December 31 statements, what total should {s} accrue for these matters, and what total loss beyond the amounts accrued should its notes disclose as reasonably possible?""",
        choices, ans,
        f"""(1) A loss is probable and {m(c)} is the best estimate in the range, so {m(c)} is accrued, and the reasonably possible loss above it ({m(b)} − {m(c)} = {m(b - c)}) is disclosed. (2) Counsel cannot predict the outcome, so the loss is reasonably possible, not probable: disclose {m(d)}, accrue nothing; the insurer's denial means there is no recovery to consider. (3) Given the enforceability of the clause, a loss is remote: neither accrued nor disclosed. (4) The claim is unasserted, but {s} will report the overbilling, so assertion is probable and repayment of {m(f)} is probable and estimable: accrue it. Accrued: {m(c)} + {m(f)} = {m(c + f)}. Disclosed beyond the accruals: {m(b - c)} + {m(d)} = {m(b - c + d)}.""",
    )


def documents_year2_loss(p):
    co, s = p["co"], short(p["co"])
    key_v = p["judg"] - p["lo1"] + p["emp_lo"]
    emp_mid = whole((D(p["emp_lo"]) + p["emp_hi"]) / 2)
    vals = {
        "full_judg": p["judg"] + p["emp_lo"],
        "appeal": p["emp_lo"],
        "compliance": key_v + p["retrofit"],
        "emp_mid": p["judg"] - p["lo1"] + emp_mid,
        "threat": key_v + p["threat"],
    }
    distinct(key_v, vals.values())
    pool = {
        "full_judg": (m(vals["full_judg"]), f"Charges the whole {m(p['judg'])} judgment to Year 2. {m(p['lo1'])} was already accrued and expensed in Year 1; only the increase is a Year 2 loss."),
        "appeal": (m(vals["appeal"]), "Makes no further accrual for the lawsuit while the appeal is pending. Counsel expects the judgment to stand, so the loss is probable and measured at the judgment."),
        "compliance": (m(vals["compliance"]), f"Accrues the {m(p['retrofit'])} plant modification. The cost relates to future operations under a rule not yet in effect; there is no present obligation, so nothing is accrued."),
        "emp_mid": (m(vals["emp_mid"]), f"Accrues the {m(emp_mid)} midpoint of the settlement range. With no better estimate in the range, the minimum ({m(p['emp_lo'])}) is accrued."),
        "threat": (m(vals["threat"]), f"Accrues the {m(p['threat'])} threatened suit. Counsel cannot predict the outcome, so a loss is not probable; it is disclosed, not accrued."),
    }
    key = (m(key_v), f"Correct. ({m(p['judg'])} − {m(p['lo1'])}) + {m(p['emp_lo'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} is finalizing its Year 2 financial statements, which have not been issued. Its files show: (1) Counsel's letter a year ago estimated damages in a customer's lawsuit at between {m(p['lo1'])} and {m(p['hi1'])}, with no amount more likely than another, and {s}'s Year 1 statements reported an accrued liability of {m(p['lo1'])}. Counsel's current letter reports that in November, Year 2, the trial court entered a judgment of {m(p['judg'])} against {s}; {s} has appealed, but counsel expects the judgment to be upheld. (2) Board minutes from December, Year 2, approve spending {m(p['retrofit'])} in Year 3 to modify a plant to meet emissions rules that take effect in Year 4. (3) A former employee filed a discrimination claim in Year 2; counsel expects {s} to settle for between {m(p['emp_lo'])} and {m(p['emp_hi'])}, with no amount in the range more likely than another. (4) A supplier has threatened to sue {s} for {m(p['threat'])}; counsel's letter says the law on the issue is unsettled and it cannot predict the outcome. What total loss from these matters should {s} recognize in its Year 2 income statement?""",
        choices, ans,
        f"""(1) The judgment, which counsel expects to be upheld, makes a loss of {m(p['judg'])} probable and estimable. {m(p['lo1'])} was accrued in Year 1, so Year 2 recognizes the increase: {m(p['judg'])} − {m(p['lo1'])} = {m(p['judg'] - p['lo1'])}. (2) The plant modification is a future cost with no past event creating an obligation: not accrued. (3) Settlement is probable and no amount in the range is a better estimate, so the minimum, {m(p['emp_lo'])}, is accrued, and the range is disclosed. (4) An outcome counsel cannot predict is reasonably possible: disclosed, not accrued. Year 2 loss = {m(p['judg'] - p['lo1'])} + {m(p['emp_lo'])} = {m(key_v)}.""",
    )


# ── III.C.e Contract costs ──────────────────────────────────────────────


def contract_costs(p):
    co, s = p["co"], short(p["co"])
    rem = D(42) / 48
    cap = p["comm"] + p["setup"]
    key_v = whole(cap * rem)
    vals = {
        "no_expedient": key_v + whole(D(p["comm2"]) * 8 / 10),
        "training": key_v + whole(p["train"] * rem),
        "bonus": key_v + whole(p["bonus"] * rem),
        "from_signing": whole(cap * D(39) / 48),
        "setup_exp": whole(p["comm"] * rem),
        "no_amort": cap,
    }
    distinct(key_v, vals.values())
    pool = {
        "no_expedient": (m(vals["no_expedient"]), f"Capitalizes the {m(p['comm2'])} commission on the 10-month contract. {s} elected the practical expedient, so a cost of obtaining a contract with an amortization period of one year or less is expensed."),
        "training": (m(vals["training"]), f"Capitalizes the {m(p['train'])} of staff training. Training doesn't create or enhance a resource used to satisfy this contract, so it is expensed as incurred."),
        "bonus": (m(vals["bonus"]), f"Capitalizes the {m(p['bonus'])} bonus. It depends on the region's total sales, not on obtaining this contract, so it isn't an incremental cost of this contract."),
        "from_signing": (m(vals["from_signing"]), "Starts amortization on April 1, when the contract was signed. The asset is amortized as the services are provided, starting July 1."),
        "setup_exp": (m(vals["setup_exp"]), f"Expenses the {m(p['setup'])} of setup. Setup costs that relate directly to the contract, create a resource used to provide the services and are expected to be recovered are fulfillment costs, capitalized."),
        "no_amort": (m(vals["no_amort"]), "Records no amortization for Year 1. Services began July 1, so six months of the 48-month service period have passed."),
    }
    key = (m(key_v), f"Correct. ({m(p['comm'])} + {m(p['setup'])}) × 42/48.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} elects the practical expedient to expense the costs of obtaining a contract when the amortization period would be one year or less. On April 1, Year 1, it signed a four-year contract to process a client's payroll, with services running from July 1, Year 1, through June 30, Year 5; renewal isn't expected. {s} paid its salesperson a {m(p['comm'])} commission owed only because the contract was signed. Before services began, {s} spent {m(p['setup'])} migrating and testing the client's payroll data and setting up the client's pay rules in its existing processing systems (costs not within the scope of any other Topic), work that transfers no service to the client and that the contract's fees are priced to recover. It also spent {m(p['train'])} training its staff on its updated processing systems, and a regional manager earned a {m(p['bonus'])} bonus based on the region's total sales for the quarter. On November 1, Year 1, {s} signed a 10-month contract with another client, which isn't expected to be renewed either, and paid a {m(p['comm2'])} commission that relates only to that contract. {s} amortizes capitalized contract costs straight-line over the period services are provided. What total contract cost assets should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""The {m(p['comm'])} commission is an incremental cost of obtaining the four-year contract and is capitalized. The {m(p['setup'])} of setup relates directly to the contract, creates a resource {s} uses to provide the services and is expected to be recovered, so it is a capitalized fulfillment cost. Training and the sales-based regional bonus are expensed. The 10-month contract's commission would be amortized over one year or less, so under the elected expedient it is expensed. Both assets are amortized over the 48 months of service from July 1, Year 1; six months have passed at December 31, leaving 42/48: ({m(p['comm'])} + {m(p['setup'])}) × 42/48 = {m(key_v)}.""",
    )


# ── III.C.f NFP contributed services ────────────────────────────────────


def contributed_services(p):
    org, s = p["org"], short(p["org"])
    key_v = p["vet"] + p["elec"]
    vals = {
        "lawyer": key_v + p["lawyer"],
        "marketing": key_v + p["mkt"],
        "walkers": key_v + p["walk"],
        "materials": key_v + p["wire"],
        "asset_only": p["elec"],
        "vet_only": p["vet"],
    }
    distinct(key_v, vals.values())
    pool = {
        "lawyer": (m(vals["lawyer"]), f"Includes the attorney's {m(p['lawyer'])}. She has specialized skills, but answering phones doesn't use them and creates no asset, so the services aren't recognized."),
        "marketing": (m(vals["marketing"]), f"Includes the {m(p['mkt'])} ad campaign. Specialized services are recognized only if the entity would typically need to buy them if not donated; {s} would not have paid for the campaign."),
        "walkers": (m(vals["walkers"]), f"Includes the {m(p['walk'])} of dog walking. The volunteers need no specialized skills and create no nonfinancial asset."),
        "materials": (m(vals["materials"]), f"Includes the {m(p['wire'])} of donated wiring and fixtures. They are a contribution of nonfinancial assets (a gift in kind), not contributed services."),
        "asset_only": (m(vals["asset_only"]), "Recognizes only services that create or enhance a nonfinancial asset. Specialized services the entity would otherwise buy, such as the veterinarian's surgeries, are recognized too."),
        "vet_only": (m(vals["vet_only"]), "Recognizes only the veterinarian's services. The electrician's labor enhanced the kennel building, a nonfinancial asset, so it is recognized as well."),
    }
    key = (m(key_v), f"Correct. Veterinarian {m(p['vet'])} + electrician {m(p['elec'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, received these volunteer services and gifts in Year 1: a licensed veterinarian performed surgeries for which {s} would otherwise have paid a local clinic {m(p['vet'])}; a licensed electrician rewired {s}'s kennel building, labor with a fair value of {m(p['elec'])}, using wiring and fixtures worth {m(p['wire'])} donated by a supply store; an attorney answered phones at the front desk, time valued at {m(p['lawyer'])} at her usual billing rate; a marketing firm ran an advertising campaign with a fair value of {m(p['mkt'])}, which {s}'s board says it would not have paid for; and community volunteers walked dogs, time valued at {m(p['walk'])} at local wage rates. What contribution revenue from contributed services should {s} recognize for Year 1?""",
        choices, ans,
        f"""Contributed services are recognized only if they create or enhance a nonfinancial asset, or require specialized skills, are provided by people with those skills, and would typically need to be purchased if not donated. The veterinarian's surgeries meet the second test ({m(p['vet'])}), and the electrician's rewiring enhances the kennel building ({m(p['elec'])}). The attorney isn't using her specialized skills, {s} would not have bought the ad campaign, and dog walking needs no specialized skills. The donated wiring is a gift in kind, not a service. Revenue = {m(p['vet'])} + {m(p['elec'])} = {m(key_v)}.""",
    )


# ── II.G.d Reconcile the payables subledger to the general ledger ───────


def credit(x):
    assert x > 0
    return f"{m(x)} net credit"


def ap_reconciliation(p):
    co, s = p["co"], short(p["co"])
    G, r, u, w, pay, q = (p[k] for k in ("gl", "memo", "foot", "freight", "pay", "unrec"))
    S = G - r + u - pay
    key_v = u + q - r
    vals = {
        "omit_q": u - r,
        "include_p": u + q - r - pay,
        "ignore_foot": q - r,
        "no_memo": u + q,
        "misposted": u + q - r + w,
    }
    distinct(key_v, vals.values())
    pool = {
        "omit_q": (credit(vals["omit_q"]), f"Leaves out the {m(q)} unrecorded invoice because it isn't a difference between the two records. The goods were received December 28, so the liability belongs in both."),
        "include_p": (credit(vals["include_p"]), f"Also debits the control account for the {m(pay)} payment. The payment was recorded correctly in the general ledger; only the subledger posted it twice."),
        "ignore_foot": (credit(vals["ignore_foot"]), f"Ignores the {m(u)} underfooting. The general ledger received the journal's wrong total, so the control account is understated."),
        "no_memo": (credit(vals["no_memo"]), f"Ignores the {m(r)} credit memo. The return reduces the liability, and only the subledger recorded it."),
        "misposted": (credit(vals["misposted"]), f"Credits the control account for the {m(w)} freight invoice. It is already in the general ledger; posting it to the wrong vendor affects only the subledger detail, not either total."),
    }
    key = (credit(key_v), f"Correct. Credit {m(u)} underfooting + credit {m(q)} unrecorded invoice − debit {m(r)} credit memo.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s accounts payable subledger (the trial balance of vendor accounts) totals {m(S)}, and its general ledger accounts payable control account shows {m(G)}. The controller's investigation finds: (1) a {m(r)} vendor credit memo for returned merchandise was posted to the vendor's subledger account, but no general ledger entry was made; (2) the December purchases journal was footed at {m(p['pj'])}, but the invoices in it total {m(p['pj'] + u)}; the journal total was posted to the general ledger, and each invoice was posted to its vendor's account; (3) a {m(w)} freight invoice was recorded in the general ledger but posted to the wrong vendor's subledger account; (4) a {m(pay)} payment on December 30 was correctly recorded in the cash disbursements journal but posted twice to the vendor's subledger account; and (5) a {m(q)} invoice for goods shipped FOB shipping point and received December 28 was found in the unmatched-invoice file and has not been recorded anywhere. What net adjustment should {s} make to its general ledger accounts payable control account?""",
        choices, ans,
        f"""Correct each record separately. General ledger: {m(G)} − {m(r)} credit memo + {m(u)} underfooting + {m(q)} unrecorded invoice = {m(G - r + u + q)}. Subledger: {m(S)} + {m(pay)} duplicate payment posting reversed + {m(q)} unrecorded invoice = {m(S + pay + q)}. The two agree. The misposted freight invoice is corrected between vendor accounts and changes neither total. Net adjustment to the control account: {m(u)} + {m(q)} − {m(r)} = {m(key_v)} credit.""",
    )


# ── Families: parameter set 0 is the item, sets 1-3 its variants ──────────

FAMILIES = [
    ("far-accounting-errors-0005", A3, "Accounting changes and error corrections", AN,
     ["ASC 250-10 (change in accounting estimate effected by a change in accounting principle)", "ASC 360-10 (depreciation)"],
     depreciation_change, [
        dict(co="Brisco Manufacturing", cost=1280000, life=8, rate=25, re0=3450000, ni=610000, div=180000, use=["no_redep", "pretax", "keep_ddb"]),
        dict(co="Cantrell Foods", cost=500000, life=5, rate=25, re0=1240000, ni=265000, div=90000, use=["as_drafted", "keep_ddb", "orig_life"]),
        dict(co="Dorrance Printing", cost=875000, life=10, rate=25, re0=2180000, ni=344000, div=120000, use=["orig_life", "pretax", "as_drafted"]),
        dict(co="Esterly Plastics", cost=2560000, life=8, rate=21, re0=6900000, ni=1150000, div=400000, use=["as_drafted", "no_redep", "orig_life"]),
     ]),
    ("far-accounting-errors-0006", A3, "Accounting changes and error corrections", AN,
     ["ASC 250-10 (correction of an error in previously issued financial statements)"],
     counterbalancing, [
        dict(co="Halvorsen Co.", re=1846000, inv1=27000, inv2=34000, ins=45000, mach=110000, wages=19000, use=["inv_y2", "wages", "dep_one"]),
        dict(co="Isherwood Co.", re=962000, inv1=18000, inv2=22000, ins=36000, mach=120000, wages=14000, use=["inv_y1", "ins_none", "dep_y4"]),
        dict(co="Jurado Co.", re=2415000, inv1=41000, inv2=29000, ins=60000, mach=140000, wages=26000, use=["wages", "inv_y1", "dep_one"]),
        dict(co="Kittredge Co.", re=1378000, inv1=23000, inv2=31000, ins=54000, mach=150000, wages=12000, use=["inv_y2", "ins_none", "dep_y4"]),
     ]),
    ("far-contingencies-0007", A3, "Contingencies and commitments", AP,
     ["ASC 410-30 (environmental obligations)", "ASC 450-20 (loss contingencies: measurement within a range)"],
     remediation, [
        dict(co="Ostrander Chemical", lo1=600000, hi1=1000000, paid=250000, lo2=500000, best2=720000, hi2=1100000, claim=300000, use=["mid1", "no_pay", "hi2"]),
        dict(co="Prendergast Coatings", lo1=450000, hi1=790000, paid=180000, lo2=380000, best2=520000, hi2=800000, claim=150000, use=["net_ins", "cash", "low2"]),
        dict(co="Quintrell Metals", lo1=800000, hi1=1200000, paid=320000, lo2=700000, best2=960000, hi2=1300000, claim=350000, use=["no_pay", "low2", "mid1"]),
        dict(co="Rosswell Tanning", lo1=300000, hi1=700000, paid=140000, lo2=260000, best2=430000, hi2=620000, claim=120000, use=["hi2", "cash", "no_pay"]),
     ]),
    ("far-contingencies-0008", A3, "Contingencies and commitments", AN,
     ["ASC 450-20 (loss contingencies: accrual, disclosure, unasserted claims)"],
     documents_accrue_disclose, [
        dict(co="Pellington Tools", lo=250000, hi=700000, best=400000, split=180000, remote=90000, overbill=60000, use=["low_end", "unasserted", "no_excess"]),
        dict(co="Quennell Outfitters", lo=150000, hi=500000, best=260000, split=120000, remote=75000, overbill=45000, use=["rp_accrued", "remote", "low_end"]),
        dict(co="Rushmore Instruments", lo=400000, hi=900000, best=550000, split=220000, remote=130000, overbill=85000, use=["unasserted", "rp_accrued", "remote"]),
        dict(co="Stanwick Hydraulics", lo=200000, hi=650000, best=350000, split=160000, remote=110000, overbill=70000, use=["no_excess", "low_end", "rp_accrued"]),
     ]),
    ("far-contingencies-0009", A3, "Contingencies and commitments", AN,
     ["ASC 450-20 (loss contingencies: recognition, measurement within a range, disclosure)"],
     documents_year2_loss, [
        dict(co="Winslade Corp.", lo1=200000, hi1=500000, judg=380000, retrofit=250000, emp_lo=40000, emp_hi=90000, threat=150000, use=["full_judg", "compliance", "emp_mid"]),
        dict(co="Yelverton Corp.", lo1=120000, hi1=360000, judg=290000, retrofit=180000, emp_lo=25000, emp_hi=65000, threat=110000, use=["appeal", "threat", "full_judg"]),
        dict(co="Zimmerly Corp.", lo1=300000, hi1=650000, judg=540000, retrofit=400000, emp_lo=70000, emp_hi=140000, threat=220000, use=["compliance", "threat", "full_judg"]),
        dict(co="Averill Corp.", lo1=150000, hi1=420000, judg=330000, retrofit=210000, emp_lo=35000, emp_hi=85000, threat=95000, use=["threat", "appeal", "emp_mid"]),
     ]),
    ("far-revenue-contract-costs-0002", A3, "Revenue recognition", AP,
     ["ASC 340-40 (other assets and deferred costs: contracts with customers)"],
     contract_costs, [
        dict(co="Carraway Payroll Services", comm=38400, setup=57600, train=12000, bonus=8800, comm2=9000, use=["no_expedient", "training", "setup_exp"]),
        dict(co="Dunleavy Payroll Services", comm=28800, setup=19200, train=7200, bonus=6400, comm2=5500, use=["from_signing", "setup_exp", "no_expedient"]),
        dict(co="Ellsworth Payroll Services", comm=52800, setup=38400, train=16000, bonus=12800, comm2=11000, use=["setup_exp", "training", "no_amort"]),
        dict(co="Farnsworth Payroll Services", comm=24000, setup=33600, train=9600, bonus=5600, comm2=7500, use=["from_signing", "bonus", "no_amort"]),
     ]),
    ("far-nfp-contributed-services-0002", A3, "Revenue recognition", AP,
     ["ASC 958-605 (contributed services)"],
     contributed_services, [
        dict(org="Foxhollow Animal Shelter", vet=28000, elec=14000, wire=6000, lawyer=9000, mkt=22000, walk=17000, use=["vet_only", "lawyer", "marketing"]),
        dict(org="Glenhaven Animal Rescue", vet=19000, elec=11000, wire=4500, lawyer=7500, mkt=16000, walk=12000, use=["asset_only", "vet_only", "materials"]),
        dict(org="Harwood Humane Society", vet=36000, elec=21000, wire=8000, lawyer=12000, mkt=30000, walk=24000, use=["walkers", "materials", "lawyer"]),
        dict(org="Inglewood Pet Refuge", vet=15000, elec=9000, wire=3500, lawyer=6000, mkt=13000, walk=10000, use=["asset_only", "marketing", "walkers"]),
     ]),
    ("far-payables-reconciliation-0002", A2, "Payables and accrued liabilities", AN,
     ["ASC 405-10 (liabilities)", "Reconciliation of a subsidiary ledger to its general ledger control account"],
     ap_reconciliation, [
        dict(co="Delacroix Supply", gl=486000, memo=7000, foot=10000, freight=3200, pay=12500, unrec=15000, pj=214000, use=["omit_q", "include_p", "ignore_foot"]),
        dict(co="Emberly Supply", gl=352000, memo=5500, foot=9000, freight=2600, pay=8000, unrec=11000, pj=168000, use=["no_memo", "misposted", "omit_q"]),
        dict(co="Fairweather Supply", gl=611000, memo=9000, foot=18000, freight=4100, pay=16000, unrec=13000, pj=275000, use=["include_p", "no_memo", "misposted"]),
        dict(co="Gladstone Supply", gl=274000, memo=4000, foot=6000, freight=1900, pay=8500, unrec=9500, pj=131000, use=["ignore_foot", "no_memo", "include_p"]),
     ]),
]


# ── Word items ───────────────────────────────────────────────────────────

WORD_ITEMS = [
    mcq("far-contingencies-0010", A3, "Contingencies and commitments", RU,
        ["ASC 450-20 (disclosure of loss contingencies)", "ASC 460-10 (guarantor disclosures)"],
        """Under U.S. GAAP, which of the following must an entity disclose in its notes even when the likelihood of any loss is remote?""",
        [("A guarantee of another company's bank loan, where default is not expected", "Correct. A guarantor discloses the nature, term and maximum potential payments of a guarantee even when the likelihood of having to pay is remote."),
         ("A pending lawsuit that counsel expects the entity to win with near certainty", "A loss contingency whose likelihood is remote is neither accrued nor disclosed. Guarantees are the exception."),
         ("An unasserted claim that the potential claimant is not expected to assert", "When assertion is not probable, an unasserted claim is not disclosed, however large the potential loss."),
         ("General business risks, such as a possible fall in demand for its products", "General or unspecified business risks are not loss contingencies; they are neither accrued nor disclosed under ASC 450-20.")],
        "A",
        """ASC 450-20 requires no accrual or disclosure of a loss contingency whose likelihood is remote, with one notable exception: guarantees. ASC 460-10 requires a guarantor to disclose the nature of each guarantee, its term, the maximum potential future payments and the carrying amount of any liability, even when the likelihood of payment is remote. An unasserted claim is disclosed only if assertion is probable and a loss is at least reasonably possible, and general business risks are not loss contingencies."""),
    mcq("far-revenue-five-step-0001", A3, "Revenue recognition", RU,
        ["ASC 606-10-25 (identifying performance obligations: distinct goods or services)"],
        """Under ASC 606, which of the following indicates that a promised good or service is not separately identifiable from other promises in a contract with a customer?""",
        [("The customer can benefit from it together with resources that are readily available", "That shows the good or service is capable of being distinct, the other half of the test; it says nothing against separate identifiability."),
         ("The entity regularly sells it on its own to other customers at a standalone price", "Regular separate sales show the item is capable of being distinct. They don't show that it is integrated with the other promises."),
         ("It will be delivered at a different time from the other goods promised in the contract", "Timing of transfer doesn't decide whether a promise is separately identifiable; goods delivered at different times can still be distinct."),
         ("The entity uses it as an input to make the combined item the customer ordered", "Correct. When the entity provides a significant service of integrating goods or services into a combined output the customer specified, they are not separately identifiable.")],
        "D",
        """A promised good or service is distinct if it is capable of being distinct (the customer can benefit from it on its own or with readily available resources) and it is separately identifiable within the contract. Indicators that it is not separately identifiable include the entity's significant service of integrating it with other goods or services into a combined output the customer contracted for, one item significantly modifying or customizing another, and items being highly interdependent or interrelated. Selling an item separately and being able to use it with readily available resources speak to the first criterion; timing of delivery is not a factor."""),
    mcq("far-nfp-promises-to-give-0001", A3, "Revenue recognition", RU,
        ["ASC 958-605 (contributions received: promises to give, conditional contributions)", "ASU 2018-08 (clarifying the scope and the accounting guidance for contributions)"],
        """A not-for-profit entity receives each of the following during Year 1. Which should it recognize as contribution revenue in Year 1?""",
        [("A donor's letter saying she has named the entity as a beneficiary in her will", "A will can be changed until death, so the letter is an intention to give, not a promise to give; nothing is recognized."),
         ("An advance on a cost-reimbursement grant for a program that starts in Year 2", "The grant is conditional: the entity must incur qualifying costs (a barrier), and unspent funds must be returned. The advance is a refundable advance (a liability) until the costs are incurred."),
         ("A pledge that lapses unless the state licenses the entity's new shelter by June 30", "Obtaining the license is a barrier, and the donor is released if it isn't met, so the pledge is conditional and is not recognized until the license is granted."),
         ("A written pledge for a research program, payable in three annual installments", "Correct. An unconditional promise to give is recognized when received, as revenue with donor restrictions (purpose and time), at the present value of the installments.")],
        "D",
        """Under ASC 958-605, as amended by ASU 2018-08, a promise to give is conditional when it contains both a barrier the recipient must overcome and a right of return of assets transferred or a right of release from the promisor's obligation. Conditional promises are recognized only when the barrier is overcome. Unconditional promises are recognized when received, even if they are payable later or restricted to a purpose; the restriction affects the net asset class, not the timing. An intention to give, such as naming the entity in a revocable will, is not a promise and is not recognized."""),
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
            print(f"{it['id']}: key letter {it['answer']}")
    if failed:
        sys.exit(1)
    warnings = audit(items)
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    write_items(items, CONTENT)


if __name__ == "__main__":
    main()
