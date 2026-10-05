"""FAR batch 17 -- 16 items written from scratch, all numeric with three variants each: three Analysis items
deriving the impact of an accounting change or error correction (III.A.b), three Application items calculating
adjustments for accounting changes and error corrections (III.A.a), three Application items on contingency
amounts and journal entries (III.B.b), two Analysis items reviewing documentation for recognition versus
disclosure (III.B.c), two Application items calculating adjustments for identified subsequent events (III.G.b)
and three Analysis items deriving the impact of subsequent events (III.G.c). Built in parallel with batch 16
(a separate slice: III.C-III.F; no shared tasks or ids).

Every Analysis item here changes at least two of the scenario's component events against every existing item
on its task, and uses a stem format and asks for a figure those items don't (see docs/reviews/far-batch-17.md).
Target skill mix 0 / 8 / 8; area mix 0 / 0 / 16 (all Area III). Scope and skill tags follow the AICPA CPA Exam
Blueprints effective January 2026.

Numeric items ship with three variants each: each item is a builder, parameter set 0 is the item and sets 1-3
are its variants, every family must move the key's letter, and parameter set 0 must show the distractor for
the item's central twist.

Run: python3 scripts/batches/far-batch-17.py [--dry-run]
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import json
import os
import re
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AN, AP, audit, attach_variants, finalize, fix_articles, mcq as _mcq, variant, write_items  # noqa: E402
from variants import m, pick, rd  # noqa: E402

A3 = "Area III — Select Transactions"
TOPIC_CHANGES = "Accounting changes and error corrections"
TOPIC_CONTINGENCIES = "Contingencies and commitments"
TOPIC_SUBSEQUENT = "Subsequent events"
NOTE = "Batch 17. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
SCRATCH = os.environ.get("B17_SCRATCH")


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
    """Report any dollar amount that appears more than once in a stem, or a choice that equals a stem amount."""
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


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole amount, got {x}"
    return x


def distinct(pool, key):
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"


def build(pool, key, use):
    distinct({k: pool[k] for k in use}, key)
    return pick(pool, key, use)


def chg(x):
    """A signed amount as '$12,000 increase' or '$12,000 decrease'."""
    x = D(x)
    assert x != 0
    return f"{m(x)} increase" if x > 0 else f"{m(-x)} decrease"


def dec(x):
    """A signed amount as '$12,000 decrease' or '$12,000 increase', phrased for a reduction question."""
    return chg(x)


# ── III.A.a Application: calculate adjustments for accounting changes and error corrections ──────────────


def allowance_rate_change(p):
    co, s = p["co"], p["co"].split()[0]
    target = whole(D(p["R"]) * D(p["r2"]) / 100)
    before = whole(D(p["B0"]) - D(p["W"]))
    key_v = target - before
    pool = {
        "old_rate": (m(whole(D(p["R"]) * D(p["r1"]) / 100) - before), f"Applies the old {p['r1']}% rate to year-end receivables instead of the revised {p['r2']}% rate. A change in the estimated loss rate is a change in accounting estimate, applied to the current year."),
        "no_wo": (m(target - D(p["B0"])), f"Compares the target allowance with the $,{p['B0']} balance at January 1 without first deducting the ${p['W']:,} of accounts written off during the year. Write-offs reduce the allowance before the current year's expense is added."),
        "gross": (m(target), f"Records the full ${target:,} target allowance as the year's bad debt expense, ignoring the ${before:,} already in the allowance (after write-offs) that need not be re-expensed."),
        "add_wo": (m(target - D(p["B0"]) - D(p["W"])), f"Subtracts the ${p['W']:,} of write-offs a second time. Write-offs already reduced the allowance from ${p['B0']:,} to ${before:,}; they aren't subtracted again from the target allowance."),
    }
    key = (m(key_v), f"Correct. Target allowance ${p['R']:,} × {p['r2']}% = ${target:,}; allowance before Year 2 expense, ${p['B0']:,} − ${p['W']:,} write-offs = ${before:,}; expense = ${target:,} − ${before:,}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} estimates its allowance for credit losses as a percentage of accounts receivable outstanding at each year-end. Its allowance for credit losses was ${p['B0']:,} at January 1, Year 2. During Year 2, {s} wrote off ${p['W']:,} of specific accounts as uncollectible, with no recoveries. Based on its receivables aging and recent collection experience, {s} revises its estimated loss rate from {p['r1']}% to {p['r2']}% of year-end receivables, effective for Year 2. Accounts receivable were ${p['R']:,} at December 31, Year 2. What bad debt expense should {s} recognize for Year 2?""",
        choices, ans,
        f"""A revised estimate of the loss rate is a change in accounting estimate (ASC 250-10-45-17), applied in the current and future periods, not restated into prior years. The allowance should equal {p['r2']}% of the ${p['R']:,} of year-end receivables, ${target:,}. The allowance already carries ${p['B0']:,} − ${p['W']:,} of write-offs = ${before:,} before any Year 2 expense. Bad debt expense = ${target:,} − ${before:,} = ${key_v:,}.""",
    )


def fifo_to_average(p):
    co, s = p["co"], p["co"].split()[0]
    key_v = D(p["W2"]) + D(p["P"]) - D(p["W3"])
    fifo_both = D(p["F2"]) + D(p["P"]) - D(p["F3"])
    mix1 = D(p["F2"]) + D(p["P"]) - D(p["W3"])
    mix2 = D(p["W2"]) + D(p["P"]) - D(p["F3"])
    swap = D(p["W3"]) + D(p["P"]) - D(p["W2"])
    pool = {
        "fifo_both": (m(fifo_both), f"Computes cost of goods sold from the FIFO inventory figures throughout, as if {s} had not changed methods. Once the change is made, Year 3 cost of goods sold uses the weighted-average figures."),
        "mix1": (m(mix1), f"Uses the FIFO beginning inventory, ${p['F2']:,}, with the weighted-average ending inventory. Both figures for Year 3 cost of goods sold must come from the newly adopted weighted-average method."),
        "mix2": (m(mix2), f"Uses the FIFO ending inventory, ${p['F3']:,}, with the weighted-average beginning inventory. Both figures for Year 3 cost of goods sold must come from the newly adopted weighted-average method."),
        "swap": (m(swap), f"Swaps the beginning and ending weighted-average inventory amounts. The ${p['W2']:,} balance is the January 1 (beginning) inventory, and the ${p['W3']:,} balance is the December 31 (ending) inventory."),
    }
    key = (m(key_v), f"Correct. ${p['W2']:,} beginning + ${p['P']:,} purchases − ${p['W3']:,} ending, all under weighted-average.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At the start of Year 3, {co} changes its inventory costing method from FIFO to weighted-average cost, because weighted-average better matches the cost of its interchangeable stock, and it can determine the effect on all prior periods. Under the weighted-average method, inventory was ${p['W2']:,} at December 31, Year 2, and ${p['W3']:,} at December 31, Year 3. Under the FIFO method it had used through Year 2, inventory was ${p['F2']:,} at December 31, Year 2, and would have been ${p['F3']:,} at December 31, Year 3. Year 3 purchases were ${p['P']:,}. What cost of goods sold should {s} report for Year 3?""",
        choices, ans,
        f"""A change in inventory costing method is applied retrospectively when, as here, the entity can determine the effect on prior periods (ASC 250-10-45-5). Year 3 cost of goods sold is recomputed entirely under the new weighted-average method: beginning inventory ${p['W2']:,} + purchases ${p['P']:,} − ending inventory ${p['W3']:,} = ${key_v:,}. The FIFO figures, ${p['F2']:,} and ${p['F3']:,}, no longer enter the Year 3 computation.""",
    )


def leasehold_and_tax(p):
    co, s = p["co"], p["co"].split()[0]
    yramort = whole(D(p["Y"]) / p["n"])
    net_lease = D(p["Y"]) - yramort
    key_v = net_lease - D(p["X"])
    pool = {
        "sign_tax": (chg(net_lease + D(p["X"])), f"Adds the ${p['X']:,} of unaccrued property tax instead of subtracting it. Failing to accrue a Year 1 expense overstated Year 1 income, so correcting it reduces January 1, Year 2, retained earnings."),
        "no_amort": (chg(D(p['Y']) - D(p["X"])), f"Capitalizes the full ${p['Y']:,} of leasehold improvements without deducting the ${yramort:,} of Year 1 amortization {s} should have recorded. Only the net carrying amount after one year's amortization increases retained earnings."),
        "only_lease": (chg(net_lease), f"Corrects the leasehold improvements but leaves out the ${p['X']:,} of property tax {s} failed to accrue in Year 1."),
        "only_tax": (chg(-D(p["X"])), f"Corrects the unaccrued property tax but leaves out the leasehold improvements error."),
    }
    key = (chg(key_v), f"Correct. Leasehold improvements: ${p['Y']:,} − ${yramort:,} of Year 1 amortization = ${net_lease:,} added to retained earnings. Property tax: ${p['X']:,} subtracted.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} discovers in Year 2, before closing its books, that in Year 1 it (1) failed to accrue ${p['X']:,} of property tax expense owed for Year 1, which was paid and expensed in Year 2 instead, and (2) expensed in full ${p['Y']:,} of leasehold improvements with a {p['n']}-year life, installed on January 1, Year 1, instead of capitalizing and amortizing them straight-line with no residual value. Ignore income taxes. What adjustment should {s} make to its January 1, Year 2, retained earnings to correct these errors?""",
        choices, ans,
        f"""Failing to accrue the ${p['X']:,} of Year 1 property tax overstated Year 1 income, so correcting it reduces January 1, Year 2, retained earnings by ${p['X']:,}. Expensing the ${p['Y']:,} of leasehold improvements understated Year 1 income by the amount that should instead have been capitalized and amortized over {p['n']} years: ${p['Y']:,} − ${yramort:,} of first-year amortization = ${net_lease:,}, which increases retained earnings. Net adjustment = ${net_lease:,} − ${p['X']:,} = {chg(key_v)}.""",
    )


# ── III.A.b Analysis: derive the impact of an accounting change or error correction ──────────────────────


def returns_and_obsolete_lot(p):
    co, s = p["co"], p["co"].split()[0]
    t = D(p["t"]) / 100
    jan1 = D(p["RE0"]) - whole(D(p["Est"]) * (1 - t))
    writedown = D(p["C"]) - D(p["N"])
    ni2 = D(p["NI2"]) - whole(writedown * (1 - t))
    key_v = jan1 + ni2 - D(p["Div"])
    draft = D(p["RE0"]) + D(p["NI2"]) - D(p["Div"])
    pool = {
        "no_tax": (m(D(p["RE0"]) - D(p["Est"]) + D(p["NI2"]) - writedown - D(p["Div"])), f"Corrects both matters but ignores the {p['t']}% tax effect on each correction."),
        "only_error1": (m(jan1 + D(p["NI2"]) - D(p["Div"])), f"Corrects only the uncorded sales returns, leaving the ${writedown:,} inventory write-down, and its tax effect, out of Year 2 net income."),
        "only_error2": (m(D(p["RE0"]) + ni2 - D(p["Div"])), f"Corrects only the inventory write-down, leaving the prior-period adjustment for the uncorded sales returns out of January 1, Year 2, retained earnings."),
        "draft": (m(draft), f"Accepts the draft ${draft:,}, correcting for neither the Year 1 sales returns nor the Year 2 inventory write-down."),
    }
    key = (m(key_v), f"Correct. January 1 retained earnings ${jan1:,} + Year 2 net income ${ni2:,} − dividends ${p['Div']:,}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s Year 1 financial statements have been issued and reported retained earnings of ${p['RE0']:,} at December 31, Year 1. While preparing its Year 2 statements, {s}'s controller finds two matters. First, Year 1 sales included goods sold with a right of return; based on historical experience, {s} should have estimated ${p['Est']:,} of those sales would be returned and recorded a refund liability reducing Year 1 revenue by that amount, but it recognized the full amount of those sales as Year 1 revenue with no refund liability. Second, a lot of inventory costing ${p['C']:,} was found during the Year 2 physical count to have become obsolete during Year 2, with a net realizable value of only ${p['N']:,}; the count still carried it at its ${p['C']:,} cost, with no write-down. {s}'s draft Year 2 net income, before considering either matter, is ${p['NI2']:,}, and it declared and paid dividends of ${p['Div']:,} during Year 2. {s}'s tax rate is {p['t']}% for all effects. What December 31, Year 2, retained earnings, as corrected, should {s} report?""",
        choices, ans,
        f"""The unrecorded expected sales returns overstated Year 1 revenue and net income by ${p['Est']:,} pretax; correcting it reduces January 1, Year 2, retained earnings by ${whole(D(p['Est']) * (1 - t)):,} after tax, to ${jan1:,} (ASC 606-10-32, refund liabilities; ASC 250-10, correction of a prior-period error). The uncorded inventory write-down is a Year 2 matter: ending inventory is overstated and Year 2 cost of goods sold understated by ${writedown:,} pretax (ASC 330-10-35, measurement at the lower of cost and net realizable value), reducing Year 2 net income by ${whole(writedown * (1 - t)):,} after tax, to ${ni2:,}. December 31, Year 2, retained earnings = ${jan1:,} + ${ni2:,} − ${p['Div']:,} = ${key_v:,}.""",
    )


def oci_and_capitalized_interest(p):
    co, s = p["co"], p["co"].split()[0]
    extra_dep = whole(D(p["Int"]) / p["n"] * p["mo"] / 12)
    ni_corr = D(p["NI"]) + D(p["U"]) + D(p["Int"]) - extra_dep
    oci_corr = D(p["FX"]) - D(p["U"])
    key_v = ni_corr + oci_corr
    draft = D(p["NI"]) + D(p["FX"])
    pool = {
        "draft": (m(draft), f"Accepts the draft total comprehensive income of ${draft:,}, neither reclassifying the ${p['U']:,} loss out of net income nor capitalizing the ${p['Int']:,} of interest."),
        "no_dep": (m(ni_corr + extra_dep + oci_corr), f"Capitalizes the ${p['Int']:,} of interest but doesn't record the ${extra_dep:,} of depreciation {s} should recognize on it for the {p['mo']} months the building was in service during Year 2."),
        "oci_unchanged": (m(ni_corr + D(p["FX"])), f"Removes the ${p['U']:,} loss from net income but leaves other comprehensive income unchanged, instead of including the loss in other comprehensive income."),
        "wrong_months": (m(D(p["NI"]) + D(p["U"]) + D(p["Int"]) - whole(D(p["Int"]) / p["n"]) + oci_corr), f"Depreciates the capitalized interest for a full year instead of only the {p['mo']} months the building was in service during Year 2."),
    }
    key = (m(key_v), f"Correct. Net income ${ni_corr:,} + other comprehensive income (${oci_corr:,}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 financial statements report net income of ${p['NI']:,}. Its controller finds two matters the draft doesn't reflect. First, {s} incorrectly recorded a ${p['U']:,} unrealized loss on its available-for-sale debt securities, which had no credit impairment, directly in net income; it should have been reported in other comprehensive income. Second, {s} expensed ${p['Int']:,} of interest that should have been capitalized as part of the cost of a {p['bldg']} it was constructing for its own use; the {p['bldg']} was completed and placed in service on {p['date']}, Year 2, has a {p['n']}-year useful life with no residual value, and is depreciated straight-line. Before considering either matter, {s}'s draft other comprehensive income for Year 2, correctly stated apart from these matters, is a ${p['FX']:,} gain from foreign currency translation. What total comprehensive income should {s} report for Year 2?""",
        choices, ans,
        f"""The ${p['U']:,} unrealized loss on available-for-sale debt securities with no credit impairment belongs in other comprehensive income, not net income (ASC 320-10-45); moving it between the two doesn't change their sum, total comprehensive income. The ${p['Int']:,} of interest on self-constructed property should be capitalized (ASC 835-20-30) and then depreciated over its {p['n']}-year life for the {p['mo']} months the asset was in service during Year 2, ${extra_dep:,}. Corrected net income = ${p['NI']:,} + ${p['U']:,} + ${p['Int']:,} − ${extra_dep:,} = ${ni_corr:,}. Corrected other comprehensive income = ${p['FX']:,} − ${p['U']:,} = ${oci_corr:,}. Total comprehensive income = ${key_v:,}.""",
    )


def fx_payable_and_commitment(p):
    co, s = p["co"], p["co"].split()[0]
    fx_loss = D(p["P2"]) - D(p["P"])
    commit_loss = D(p["M"]) - D(p["M2"])
    key_v = -(fx_loss + commit_loss)
    pool = {
        "omit_fx": (chg(-commit_loss), f"Recognizes only the ${commit_loss:,} loss on the purchase commitment, leaving the payable at its original ${p['P']:,}, with no year-end remeasurement for the change in the exchange rate."),
        "omit_commit": (chg(-fx_loss), f"Remeasures the payable for the ${fx_loss:,} transaction loss but doesn't recognize any loss on the now-unfavorable purchase commitment."),
        "fx_sign": (chg(fx_loss - commit_loss), f"Treats the change in the payable as a ${fx_loss:,} gain rather than a loss. The dollar amount needed to settle the euro-denominated payable rose, which is a loss, not a gain, on the unsettled liability."),
        "commit_sign": (chg(-fx_loss + commit_loss), f"Treats the fall in the materials' market price as a ${commit_loss:,} gain on the commitment. A noncancelable commitment to buy above the current market price is a loss, even though the price itself has fallen."),
    }
    key = (chg(key_v), f"Correct. ${fx_loss:,} foreign-currency transaction loss + ${commit_loss:,} loss on the purchase commitment, both decreases to pretax income.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} is preparing its Year 2 financial statements, which have not been issued. On {p['date']}, Year 2, {s} bought inventory from a European supplier on open account, recording an accounts payable of ${p['P']:,} at that day's spot rate; the payable is due in Year 3 and is still outstanding at December 31, Year 2. Using the spot rate at December 31, Year 2, that payable would restate to ${p['P2']:,}, but {s}'s accountant left it at its original ${p['P']:,}, with no year-end remeasurement. Separately, {s} has a noncancelable commitment, unhedged, to buy ${p['M']:,} of raw materials during Year 3 at a fixed price; since December 31, Year 2, the market price for that quantity of materials has fallen to ${p['M2']:,}, and {s}'s accountant has not recognized any loss on the commitment. What adjustment should {s} make to its Year 2 pretax income?""",
        choices, ans,
        f"""A foreign-currency payable is remeasured at the spot rate at each balance sheet date, with the change recognized in income (ASC 830-20-35-1); the payable's required restatement from ${p['P']:,} to ${p['P2']:,} is a ${fx_loss:,} transaction loss. A material, noncancelable purchase commitment on which the market price has fallen below the contract price requires recognizing the ${commit_loss:,} loss in the period of the price decline (ASC 330-10, losses on firm purchase commitments). Both reduce Year 2 pretax income: {chg(key_v)}.""",
    )


# ── III.B.b Application: calculate amounts of contingencies and prepare journal entries ───────────────────


def litigation_trueup_and_new(p):
    co, s = p["co"], p["co"].split()[0]
    trueup = D(p["B"]) - D(p["A"])
    key_v = trueup + D(p["C"])
    pool = {
        "ignore_trueup": (m(p["C"]), f"Recognizes only the ${p['C']:,} accrual for the new claim, leaving out the additional ${trueup:,} needed to true up last year's accrual to the ${p['B']:,} settlement."),
        "full_settlement": (m(D(p["B"]) + D(p["C"])), f"Expenses the entire ${p['B']:,} settlement again in Year 2, on top of the ${p['A']:,} already accrued and expensed in Year 1."),
        "reverse_trueup": (m(D(p["A"]) - D(p["B"]) + D(p["C"])), f"Computes the true-up as the prior accrual minus the settlement, ${p['A']:,} − ${p['B']:,}, rather than the additional loss the higher settlement requires."),
        "ignore_new": (m(trueup), f"Recognizes the ${trueup:,} true-up on the settled suit but leaves out the ${p['C']:,} accrual for the new claim."),
    }
    key = (m(key_v), f"Correct. ${trueup:,} additional loss on the settled suit (${p['B']:,} − ${p['A']:,}) + ${p['C']:,} accrual for the new claim.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 1, {co} accrued ${p['A']:,} for a lawsuit, which met the criteria for a loss contingency. In Year 2, {s} settles that lawsuit for ${p['B']:,} cash. Also during Year 2, a customer files a separate claim against {s}; {s}'s counsel believes it is probable {s} will be found liable and reasonably estimates the loss at ${p['C']:,}. What total litigation expense should {s} recognize in Year 2?""",
        choices, ans,
        f"""Settling the first suit for ${p['B']:,}, more than the ${p['A']:,} already accrued, requires an additional ${trueup:,} of Year 2 litigation expense. The new claim is probable and reasonably estimable, so {s} accrues the full ${p['C']:,} (ASC 450-20-25-2). Total Year 2 litigation expense = ${trueup:,} + ${p['C']:,} = ${key_v:,}.""",
    )


def warranty_pct_of_sales(p):
    co, s = p["co"], p["co"].split()[0]
    accrual = whole(D(p["Sales"]) * D(p["pct"]) / 100)
    key_v = D(p["Beg"]) + accrual - D(p["Paid"])
    pool = {
        "accrual_only": (m(accrual), f"Reports only the ${accrual:,} Year 2 accrual as the liability, leaving out the ${p['Beg']:,} balance already on the books and the ${p['Paid']:,} of claims {s} already paid during Year 2."),
        "no_paid": (m(D(p["Beg"]) + accrual), f"Adds the Year 2 accrual to the beginning balance but doesn't deduct the ${p['Paid']:,} of warranty claims {s} paid during Year 2."),
        "no_accrual": (m(D(p["Beg"]) - D(p["Paid"])), f"Deducts the claims paid but leaves out the ${accrual:,} accrual for Year 2 sales."),
        "double_pay": (m(D(p["Beg"]) + accrual + D(p["Paid"])), f"Adds the ${p['Paid']:,} of claims paid instead of deducting them. Paying a claim reduces the liability, since the cash reduces the amount still owed."),
    }
    key = (m(key_v), f"Correct. ${p['Beg']:,} beginning balance + ${accrual:,} Year 2 accrual ({p['pct']}% × ${p['Sales']:,}) − ${p['Paid']:,} claims paid.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s warranty liability was ${p['Beg']:,} at January 1, Year 2. {s} estimates warranty costs at {p['pct']}% of net sales of warrantied products, based on its claims history, and its estimate has not changed. Year 2 net sales of warrantied products were ${p['Sales']:,}, and {s} paid ${p['Paid']:,} of warranty claims during Year 2. What warranty liability should {s} report at December 31, Year 2?""",
        choices, ans,
        f"""The Year 2 warranty accrual is {p['pct']}% of Year 2 net sales of warrantied products: ${p['Sales']:,} × {p['pct']}% = ${accrual:,} (ASC 460-10-25, product warranties). The liability rolls forward from the beginning balance, plus the accrual, less claims paid during the year: ${p['Beg']:,} + ${accrual:,} − ${p['Paid']:,} = ${key_v:,}.""",
    )


def litigation_with_recovery(p):
    co, s = p["co"], p["co"].split()[0]
    trueup = D(p["B2"]) - D(p["A2"])
    net2 = D(p["L"]) - D(p["R"])
    key_v = trueup + net2
    pool = {
        "no_recovery": (m(trueup + D(p["L"])), f"Recognizes the full ${p['L']:,} loss on the worker's claim without reducing it for the ${p['R']:,} recovery {s}'s insurer has confirmed in writing and {s} considers probable."),
        "reverse_trueup": (m(D(p["A2"]) - D(p["B2"]) + net2), f"Computes the settled suit's true-up as the prior accrual minus the settlement rather than the additional loss the higher settlement requires."),
        "no_trueup": (m(net2), f"Recognizes the net effect of the worker's claim but leaves out the ${trueup:,} additional loss on the suit {s} settled for more than it had accrued."),
        "recovery_sign": (m(trueup + D(p["L"]) + D(p["R"])), f"Adds the ${p['R']:,} probable insurance recovery to the loss instead of offsetting it. A probable recovery reduces the net income effect of the loss."),
    }
    key = (m(key_v), f"Correct. ${trueup:,} additional loss on the settled suit + (${p['L']:,} claim − ${p['R']:,} probable recovery).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""In Year 2, {co} settles for ${p['B2']:,} a lawsuit for which it had accrued ${p['A2']:,} in Year 1. Also in Year 2, a warehouse worker is injured; {s}'s counsel believes it is probable {s} will be found liable and reasonably estimates the loss at ${p['L']:,}. {s}'s insurer has confirmed in writing that it will reimburse {s} ${p['R']:,} of any amount {s} pays on the worker's claim, and {s} considers that recovery probable. By how much should these two matters decrease {s}'s Year 2 pretax income?""",
        choices, ans,
        f"""Settling the first suit for ${p['B2']:,}, more than the ${p['A2']:,} already accrued, adds ${trueup:,} of Year 2 litigation expense. The worker's claim is accrued at its full ${p['L']:,} estimate (ASC 450-20-25-2); because recovery from the insurer is probable, {s} separately recognizes a ${p['R']:,} receivable and gain (ASC 450-30), for a net income-statement effect of ${net2:,}. Total decrease to Year 2 pretax income = ${trueup:,} + ${net2:,} = ${key_v:,}.""",
    )


# ── III.B.c Analysis: review documentation for recognition versus disclosure ──────────────────────────────


def guarantee_and_conditional_settlement(p):
    co, s = p["co"], p["co"].split()[0]
    pool = {
        "adds_contingent_settlement": (m(D(p["L"]) + D(p["S"])), f"Adds the ${p['S']:,} conditional settlement to the guarantee liability. The regulatory approval the settlement depends on hadn't been granted at year-end, and {s} has no way to influence or predict it, so the obligating event for that payment hadn't occurred."),
        "sums_fv_and_contingent": (m(D(p["L"]) + D(p["Fee"])), f"Adds the ${p['Fee']:,} initial fair value of the guarantee to the ${p['L']:,} contingent loss. A guarantee's liability is remeasured at the higher of its remaining noncontingent carrying amount and the ASC 450-20 contingent loss, not the sum of the two (ASC 460-10-35-2)."),
        "fv_only": (m(p["Fee"]), f"Reports only the ${p['Fee']:,} initial fair value of the guarantee, ignoring the ${p['L']:,} loss that became probable and estimable once the supplier defaulted."),
        "settlement_only": (m(p["S"]), f"Accrues only the conditional settlement, ignoring the guarantee liability entirely."),
    }
    key = (m(p["L"]), f"Correct. The ${p['L']:,} contingent loss on the guarantee, the higher of it and the guarantee's remaining noncontingent carrying amount; nothing for the conditional settlement.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Before issuing its December 31, Year 1, financial statements, {co} reviews two documents. The first is a signed agreement under which {s}, for a ${p['Fee']:,} fee, guaranteed a ${p['Loan']:,} bank loan of an unrelated supplier; the fee approximated the guarantee's fair value at inception and was recognized as guarantee income over the guarantee's term. During Year 1, the supplier defaulted on the loan, and the bank has demanded payment from {s}; based on the supplier's remaining assets, {s}'s counsel and credit staff now consider it probable that {s} will have to pay the bank, and estimate the amount at ${p['L']:,}. The second document is an agreement {s} signed on {p['date']} to pay a customer ${p['S']:,} to settle a dispute, but only if a pending regulatory approval the customer needs for its own project is granted; at year-end, the agency had not yet acted on the application, and {s} has no way to influence or predict its decision. What total liability should {s} accrue at December 31, Year 1, for these two matters?""",
        choices, ans,
        f"""A guarantee is initially recognized at its fair value (${p['Fee']:,} here); it is subsequently reported at the higher of its remaining noncontingent carrying amount and the contingent liability measured under ASC 450-20 once payment becomes probable and estimable (ASC 460-10-30, 35-2). Once the supplier defaulted, the ${p['L']:,} contingent loss became both probable and estimable and exceeds the remaining fair-value carrying amount, so {s} accrues ${p['L']:,} for the guarantee. The customer settlement depends on a regulatory approval that is outside {s}'s control and hadn't been granted at year-end; the condition creating the obligation hadn't occurred, so no liability is accrued for it (ASC 450-20-25). Total liability = ${p['L']:,}.""",
    )


def consent_order_and_appeal_receivable(p):
    co, s = p["co"], p["co"].split()[0]
    key_v = D(p["Order"]) + D(p["Judgment"])
    pool = {
        "no_consent": (m(p["Judgment"]), f"Decreases pretax income only for reversing the ${p['Judgment']:,} receivable, treating the ${p['Order']:,} of consent-order remediation as a future commitment that needs no liability now."),
        "keeps_receivable": (m(p["Order"]), f"Records the ${p['Order']:,} consent-order liability but keeps the ${p['Judgment']:,} receivable for the possible refund. A gain contingency, such as a possible refund from a pending appeal, isn't recognized until its realization is no longer contingent."),
        "no_adjust": (m(0), f"Makes no adjustment for either matter, treating the consent order as merely a future cash commitment outside the current period and leaving the ${p['Judgment']:,} receivable for the possible refund on the books."),
        "half_consent": (m(whole(D(p["Order"]) / 2) + D(p["Judgment"])), f"Recognizes only half of the ${p['Order']:,} consent-order liability in Year 1, spreading it over the two years the remediation work will take. The order creates the full obligation now; only the timing of the cash spent is in the future."),
        "adds_fine": (m(key_v + D(p["Fine"])), f"Also accrues the ${p['Fine']:,} penalty the agency's order says it may assess if the cleanup schedule slips. Agency staff have given {s} no indication a penalty is likely, so that exposure is disclosed, not accrued."),
    }
    key = (m(key_v), f"Correct. ${p['Order']:,} consent-order liability + ${p['Judgment']:,} to reverse the receivable.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Before issuing its December 31, Year 1, financial statements, {co} reviews two matters. On {p['date']}, Year 1, {s} signed a final consent order with a state environmental agency requiring it to spend ${p['Order']:,} remediating a site, with the work to be performed during Years 2 and 3; the order also says the agency may assess a further penalty of up to ${p['Fine']:,} if the cleanup schedule slips, though agency staff have given {s} no indication so far that a penalty is likely. {s} has recorded no liability for the order. Separately, in Year 1 {s} paid ${p['Judgment']:,} to satisfy a judgment in a contract dispute while it appealed the decision; its counsel believes the appeal has a reasonable chance of succeeding, which would require the plaintiff to refund the ${p['Judgment']:,}, but cannot say success is probable. {s} has recorded a ${p['Judgment']:,} receivable from the plaintiff for the possible refund. By how much should recognizing the consent order and correcting the receivable decrease {s}'s Year 1 pretax income?""",
        choices, ans,
        f"""The consent order is a final, signed obligation at December 31, Year 1; the obligating event has already occurred, so the full ${p['Order']:,} is accrued now even though the remediation work spans Years 2 and 3 (ASC 450-20-25-2). The possible schedule-slip penalty has no indication of likelihood behind it, so it stays a disclosed, reasonably possible exposure rather than an accrual. The possible refund from winning the appeal is a gain contingency, which isn't recognized until realization is assured beyond a reasonable doubt (ASC 450-30-25); {s} must reverse the ${p['Judgment']:,} receivable it recorded, which decreases pretax income by that amount on top of the ${p['Judgment']:,} already expensed when the judgment was paid. Total decrease = ${p['Order']:,} + ${p['Judgment']:,} = ${key_v:,}.""",
    )


# ── III.G.b Application: calculate adjustments for identified subsequent events ────────────────────────────


def allowance_two_customers(p):
    co, s = p["co"], p["co"].split()[0]
    new1 = D(p["D1"]) - D(p["E1"])
    key_v = D(p["Other"]) + new1 + 0
    pool = {
        "no_adjust": (m(D(p["Other"]) + D(p["S1"]) + D(p["S2"])), f"Accepts the draft allowance, leaving the first customer's allowance at ${p['S1']:,} and the second customer's at ${p['S2']:,}, without adjusting for either recognized subsequent event."),
        "cust1_only": (m(D(p["Other"]) + new1 + D(p["S2"])), f"Updates the first customer's allowance for the bankruptcy but leaves the second customer's ${p['S2']:,} specific allowance unchanged, even though that balance was collected in full."),
        "cust2_only": (m(D(p["Other"]) + D(p["S1"])), f"Removes the second customer's allowance, now that it has been collected in full, but leaves the first customer's allowance at its original ${p['S1']:,}, before the bankruptcy."),
        "wrong_amt": (m(D(p["Other"]) + D(p["D1"])), f"Sets the first customer's allowance at the full ${p['D1']:,} owed, instead of the ${new1:,} {s} still expects not to collect after the ${p['E1']:,} it expects to recover."),
    }
    key = (m(key_v), f"Correct. ${p['Other']:,} other customers + ${new1:,} first customer (${p['D1']:,} − ${p['E1']:,} expected to be collected) + $0 second customer.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Before {co} issues its December 31, Year 1, financial statements, the following events, both recognized (Type I) subsequent events, occur. On {p['date1']}, Year 2, a customer that owed ${p['D1']:,} at December 31 and had been in worsening financial difficulty throughout Year 1 filed for bankruptcy; {s} now expects to collect only ${p['E1']:,} of that balance, and its December 31 allowance for credit losses had included ${p['S1']:,} for this customer specifically. On {p['date2']}, Year 2, a separate customer whose ${p['D2']:,} receivable had been doubtful at year-end because of a payment dispute that existed at December 31 paid the balance in full after resolving the dispute; {s}'s December 31 allowance had included ${p['S2']:,} for this customer. Before these two adjustments, {s}'s draft December 31 allowance for credit losses, covering its other customers, is ${p['Other']:,}. What allowance for credit losses should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""Both events are recognized subsequent events because the conditions causing each outcome existed at December 31 (ASC 855-10-25-1). For the first customer, the allowance should equal the ${p['D1']:,} owed less the ${p['E1']:,} {s} expects to collect, ${new1:,}, up from its original ${p['S1']:,} specific allowance. For the second customer, resolving the dispute makes the balance fully collectible, so its allowance falls from ${p['S2']:,} to $0. Total allowance = ${p['Other']:,} + ${new1:,} + $0 = ${key_v:,}.""",
    )


def equipment_sale_and_flood(p):
    co, s = p["co"], p["co"].split()[0]
    writedown = D(p["BV"]) - D(p["Price"])
    pool = {
        "includes_flood": (m(writedown + D(p["Flood"])), f"Also reduces total assets for the ${p['Flood']:,} of flood-damaged inventory. The flood wasn't related to any condition existing at December 31, so it is a nonrecognized subsequent event, disclosed but not adjusted; the inventory it destroyed, which was fully insured, isn't removed from the December 31 balance sheet."),
        "flood_only": (m(p["Flood"]), f"Reduces total assets for the ${p['Flood']:,} flood loss but not for the ${writedown:,} equipment write-down, even though the equipment's obsolescence existed at December 31."),
        "gross_equipment": (m(p["BV"]), f"Removes the equipment's entire ${p['BV']:,} carrying amount, as if it had already been sold at December 31, instead of writing it down to the ${p['Price']:,} it will be sold for."),
        "wrong_equipment_calc": (m(p["Price"]), f"Uses the ${p['Price']:,} sale price itself as the amount of the adjustment, rather than the ${writedown:,} decline from the equipment's ${p['BV']:,} carrying amount."),
    }
    key = (m(writedown), f"Correct. Only the ${writedown:,} equipment write-down (${p['BV']:,} carrying amount − ${p['Price']:,} sale price); the flood is a nonrecognized subsequent event.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Before {co} issues its December 31, Year 1, financial statements, two events occur. On {p['date1']}, Year 2, {s} agrees to sell a {p['asset']}, carried at ${p['BV']:,}, for ${p['Price']:,} net of selling costs; the {p['asset']} had become technologically obsolete before December 31, Year 1, a condition that existed at the balance sheet date, so the sale is a recognized (Type I) subsequent event. On {p['date2']}, Year 2, a flood neither anticipated nor related to any condition existing at December 31 destroys ${p['Flood']:,} of inventory at a different plant; the inventory was fully insured, and the insurer has confirmed it will pay the full ${p['Flood']:,}. By how much should recognizing these events decrease {s}'s total assets at December 31, Year 1?""",
        choices, ans,
        f"""The {p['asset']}'s obsolescence existed at December 31, Year 1, so the January sale is a recognized subsequent event: the asset is written down from its ${p['BV']:,} carrying amount to the ${p['Price']:,} it will be sold for, a ${writedown:,} decrease (ASC 855-10-25-1 and 25-2). The flood is unrelated to any condition at December 31, so it is a nonrecognized subsequent event, disclosed but not adjusted (ASC 855-10-25-3); because the destroyed inventory was fully insured for its ${p['Flood']:,} amount, there is no net effect on total assets even if it were adjusted. Total decrease = ${writedown:,}.""",
    )


# ── III.G.c Analysis: derive the impact of identified subsequent events ────────────────────────────────────


def covenant_waiver_and_settlement(p):
    co, s = p["co"], p["co"].split()[0]
    trueup = D(p["B"]) - D(p["A"])
    key_v = D(p["CL"]) - trueup
    pool = {
        "reclass_full": (m(key_v + D(p["Debt"])), f"Also reclassifies the ${p['Debt']:,} long-term note as a current liability. {s} received the lender's waiver, covering more than a year from the balance sheet date, before the statements were issued, so the covenant violation doesn't require reclassification (ASC 470-10-45-11 through 45-13)."),
        "reclass_only": (m(D(p["CL"]) + D(p["Debt"])), f"Reclassifies the ${p['Debt']:,} note as current but doesn't true up the lawsuit accrual for the favorable settlement."),
        "no_adjust": (m(p["CL"]), f"Accepts the draft ${p['CL']:,} without adjusting for the settlement reached after year-end."),
        "wrong_direction": (m(D(p["CL"]) + trueup), f"Treats the favorable settlement as increasing the accrued liability rather than reducing it. Settling for less than the amount accrued reduces the liability."),
    }
    key = (m(key_v), f"Correct. ${p['CL']:,} draft − ${trueup:,} reduction from settling the lawsuit for less than accrued; the note stays noncurrent.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Before issuing its December 31, Year 1, financial statements, {co} reviews the following. Its draft balance sheet reports total current liabilities of ${p['CL']:,}, which includes a ${p['A']:,} liability accrued for a customer's lawsuit over a Year 1 product failure. On {p['date1']}, Year 2, {s} settles that lawsuit for ${p['B']:,}. Separately, at December 31, Year 1, {s} was in violation of a covenant on its ${p['Debt']:,} long-term note, which otherwise matures in several years and gives the lender the right to demand immediate repayment while the violation continues; on {p['date2']}, Year 2, before the statements are issued, the lender waived the violation and agreed not to demand repayment before {p['date3']}, Year 3. What total current liabilities should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""Settling the lawsuit for ${p['B']:,}, less than the ${p['A']:,} accrued, is a recognized subsequent event that reduces the accrual by ${trueup:,} (ASC 855-10-25-1). The covenant violation would otherwise require classifying the ${p['Debt']:,} note as current, but the lender's waiver, obtained before the statements are issued and covering more than twelve months from December 31, Year 1, keeps it noncurrent (ASC 470-10-45-11 through 45-13). Total current liabilities = ${p['CL']:,} − ${trueup:,} = ${key_v:,}.""",
    )


def quick_ratio_bankruptcy(p):
    co, s = p["co"], p["co"].split()[0]
    new_loss = D(p["D"]) - D(p["E"])
    adj = new_loss - D(p["S"])
    qa = D(p["Cash"]) + D(p["MS"]) + (D(p["AR"]) - D(p["Allow"])) - adj
    cl = D(p["CL"])
    key_v = rd(qa / cl, "0.01")
    pool = {
        "no_adjust": (str(rd((D(p["Cash"]) + D(p["MS"]) + D(p["AR"]) - D(p["Allow"])) / cl, "0.01")), f"Accepts the draft quick assets without updating the allowance for the customer's bankruptcy."),
        "full_d": (str(rd((qa + D(p["S"]) - D(p["D"])) / cl, "0.01")), f"Removes the full ${p['D']:,} owed by the customer, instead of only the additional loss after the existing ${p['S']:,} allowance and the ${p['E']:,} {s} still expects to collect."),
        "includes_securities_loss": (str(rd((qa - D(p["SecLoss"])) / cl, "0.01")), f"Also deducts the ${p['SecLoss']:,} decline in the marketable securities' value. That decline occurred after year-end and isn't related to any condition existing at December 31, so it isn't recognized at December 31."),
        "wrong_allowance": (str(rd((qa - D(p["S"])) / cl, "0.01")), f"Adds the full ${new_loss:,} updated loss estimate without first removing the ${p['S']:,} specific allowance already recorded for this customer."),
    }
    key = (str(key_v), f"Correct. (${p['Cash']:,} cash + ${p['MS']:,} securities + ${p['AR']:,} receivables − ${p['Allow'] + adj:,} allowance) ÷ ${p['CL']:,}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Before issuing its December 31, Year 1, financial statements, {co} reviews two matters. Its draft balance sheet reports cash of ${p['Cash']:,}, marketable securities of ${p['MS']:,}, accounts receivable of ${p['AR']:,} less an allowance for credit losses of ${p['Allow']:,}, and total current liabilities of ${p['CL']:,}. A customer that owed ${p['D']:,} at December 31, carried net of a specific ${p['S']:,} allowance, had been in deteriorating financial condition throughout Year 1; on {p['date1']}, Year 2, it filed for bankruptcy, and {s} now expects to collect only ${p['E']:,} of the balance. Separately, in {p['month2']}, Year 2, a broad decline in equity markets led {s} to sell its marketable securities, which it had carried at ${p['MS']:,}, for ${p['MS'] - p['SecLoss']:,}. Rounded to two decimal places, what quick (acid-test) ratio should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""The customer's deteriorating condition existed throughout Year 1, so the bankruptcy is a recognized subsequent event (ASC 855-10-25-1): the allowance for this customer rises from ${p['S']:,} to ${new_loss:,} (the ${p['D']:,} owed less the ${p['E']:,} {s} still expects to collect), an additional ${adj:,}. The market decline that cut the securities' value occurred after year-end and isn't tied to any condition at December 31, so it is a nonrecognized subsequent event, disclosed but not reflected in the December 31 balance sheet (ASC 855-10-25-3). Quick assets = ${p['Cash']:,} + ${p['MS']:,} + (${p['AR']:,} − ${p['Allow'] + adj:,}) = ${qa:,}; quick ratio = ${qa:,} ÷ ${p['CL']:,} = {key_v}.""",
    )


def working_capital_refinancing(p):
    co, s = p["co"], p["co"].split()[0]
    writedown = D(p["C"]) - D(p["N"])
    draft_wc = D(p["CA"]) - D(p["CL"])
    key_v = draft_wc - writedown + D(p["Note"])
    pool = {
        "no_adjust": (m(draft_wc), f"Accepts the draft working capital, neither writing down the discontinued inventory lot nor reclassifying the refinanced note."),
        "inv_only": (m(draft_wc - writedown), f"Writes down the inventory lot but doesn't reclassify the ${p['Note']:,} note, even though {s} refinanced it on a long-term basis before the statements were issued."),
        "refi_only": (m(draft_wc + D(p["Note"])), f"Reclassifies the ${p['Note']:,} note but doesn't write down the ${p['C']:,} inventory lot for the product line {s} decided to discontinue in Year 1."),
        "wrong_sign": (m(draft_wc + writedown + D(p["Note"])), f"Treats the ${writedown:,} inventory write-down as increasing working capital. Reducing inventory's carrying amount reduces current assets and working capital."),
    }
    key = (m(key_v), f"Correct. Draft working capital ${draft_wc:,} − ${writedown:,} inventory write-down + ${p['Note']:,} note reclassified to noncurrent.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""Before issuing its December 31, Year 1, financial statements, {co} reviews two matters. Its draft balance sheet reports total current assets of ${p['CA']:,}, including a lot of inventory carried at its ${p['C']:,} cost, and total current liabilities of ${p['CL']:,}, including a ${p['Note']:,} note payable maturing in Year 2. On {p['date1']}, Year 2, {s} finds that the ${p['C']:,} inventory lot relates to a product line it decided to discontinue in Year 1, and its net realizable value is now only ${p['N']:,}. On {p['date2']}, Year 2, before the statements are issued, {s} issues ${p['Note']:,} of long-term bonds and uses the proceeds to repay the note payable in full. What working capital should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""The decision to discontinue the product line existed at December 31, Year 1, so the inventory's decline to its ${p['N']:,} net realizable value is a recognized subsequent event, a ${writedown:,} reduction to current assets (ASC 855-10-25-1; ASC 330-10-35). Issuing long-term bonds before the statements are issued and using the proceeds to repay the ${p['Note']:,} note is a refinancing on a long-term basis completed before the statements are issued, so the note is reported as a noncurrent liability at December 31 (ASC 470-10-45-14), removing it from current liabilities. Working capital = ${p['CA']:,} − ${p['CL']:,} − ${writedown:,} + ${p['Note']:,} = ${key_v:,}.""",
    )


FAMILIES = [
    ("far-change-in-estimate-0003", A3, TOPIC_CHANGES, AP,
     ["ASC 250-10-45-17 (change in accounting estimate)", "ASC 326-20 (measurement of expected credit losses)"],
     allowance_rate_change, [
        dict(co="Harrow Supply Co.", R=1500000, r1="2", r2="3", B0=28000, W=10000, use=["old_rate", "no_wo", "add_wo"]),
        dict(co="Dalkeith Supply Co.", R=2200000, r1="1.5", r2="2.5", B0=36000, W=14000, use=["no_wo", "gross", "add_wo"]),
        dict(co="Melrose Supply Co.", R=980000, r1="3", r2="4", B0=19000, W=6000, use=["old_rate", "gross", "no_wo"]),
        dict(co="Selkirk Supply Co.", R=3400000, r1="2.5", r2="3.5", B0=52000, W=22000, use=["old_rate", "add_wo", "gross"]),
     ], "no_wo"),
    ("far-change-in-principle-0003", A3, TOPIC_CHANGES, AP,
     ["ASC 250-10-45-5 to 45-8 (retrospective application of a change in accounting principle)"],
     fifo_to_average, [
        dict(co="Pemberton Hardware Co.", F2=175000, W2=200000, F3=155000, W3=140000, P=850000, use=["fifo_both", "mix1", "mix2"]),
        dict(co="Alderwood Hardware Co.", F2=320000, W2=295000, F3=170000, W3=190000, P=1120000, use=["mix1", "mix2", "swap"]),
        dict(co="Brackenfield Hardware Co.", F2=150000, W2=130000, F3=110000, W3=95000, P=640000, use=["fifo_both", "mix2", "swap"]),
        dict(co="Chaseworth Hardware Co.", F2=340000, W2=380000, F3=300000, W3=250000, P=1460000, use=["fifo_both", "mix1", "swap"]),
     ], "fifo_both"),
    ("far-error-correction-0001", A3, TOPIC_CHANGES, AP,
     ["ASC 250-10 (correction of an error in previously issued statements)", "ASC 350-20 (asset carrying amounts; by analogy, amortization of recognized costs)"],
     leasehold_and_tax, [
        dict(co="Discloser Co.", X=18000, Y=100000, n=5, use=["sign_tax", "no_amort", "only_lease"]),
        dict(co="Anglesham Co.", X=24000, Y=150000, n=6, use=["no_amort", "only_lease", "only_tax"]),
        dict(co="Burnholt Co.", X=12000, Y=80000, n=4, use=["sign_tax", "only_lease", "only_tax"]),
        dict(co="Caldervale Co.", X=30000, Y=200000, n=5, use=["sign_tax", "no_amort", "only_tax"]),
     ], "no_amort"),

    ("far-accounting-errors-0010", A3, TOPIC_CHANGES, AN,
     ["ASC 606-10-32-25 to 32-27 (refund liabilities for expected returns)", "ASC 330-10-35 (inventory write-down to net realizable value)", "ASC 250-10 (correction of a prior-period error)"],
     returns_and_obsolete_lot, [
        dict(co="Castleton Equipment Co.", RE0=2400000, Est=40000, C=260000, N=200000, NI2=650000, Div=180000, t="25", use=["no_tax", "only_error1", "draft"]),
        dict(co="Dunwoody Equipment Co.", RE0=3100000, Est=55000, C=340000, N=250000, NI2=820000, Div=220000, t="21", use=["only_error1", "only_error2", "draft"]),
        dict(co="Ellerston Equipment Co.", RE0=1850000, Est=28000, C=190000, N=150000, NI2=480000, Div=130000, t="30", use=["no_tax", "only_error2", "draft"]),
        dict(co="Farnworth Equipment Co.", RE0=4250000, Est=70000, C=420000, N=300000, NI2=1040000, Div=300000, t="25", use=["no_tax", "only_error1", "only_error2"]),
     ], "draft"),
    ("far-accounting-errors-0011", A3, TOPIC_CHANGES, AN,
     ["ASC 320-10-45 (unrealized gains and losses on available-for-sale debt securities reported in other comprehensive income)", "ASC 835-20-30 (capitalization of interest cost)", "ASC 220-10-45 (components of comprehensive income)"],
     oci_and_capitalized_interest, [
        dict(co="Brandling Co.", NI=840000, U=35000, Int=60000, n=10, mo=3, FX=25000, bldg="warehouse", date="October 1", use=["draft", "oci_unchanged", "wrong_months"]),
        dict(co="Garthwaite Co.", NI=1120000, U=48000, Int=90000, n=15, mo=6, FX=32000, bldg="distribution center", date="July 1", use=["no_dep", "oci_unchanged", "wrong_months"]),
        dict(co="Hallerton Co.", NI=620000, U=22000, Int=42000, n=8, mo=2, FX=18000, bldg="maintenance facility", date="November 1", use=["draft", "no_dep", "wrong_months"]),
        dict(co="Ingledene Co.", NI=1480000, U=60000, Int=120000, n=12, mo=9, FX=44000, bldg="storage terminal", date="April 1", use=["draft", "no_dep", "oci_unchanged"]),
     ], "draft"),
    ("far-accounting-errors-0012", A3, TOPIC_CHANGES, AN,
     ["ASC 830-20-35-1 (foreign-currency transaction gains and losses measured at each balance sheet date)", "ASC 330-10 (losses on firm purchase commitments)"],
     fx_payable_and_commitment, [
        dict(co="Brightwell Importers Co.", P=380000, P2=410000, M=250000, M2=210000, date="November 1", use=["omit_fx", "omit_commit", "fx_sign"]),
        dict(co="Caxworth Importers Co.", P=520000, P2=560000, M=340000, M2=270000, date="September 1", use=["omit_commit", "fx_sign", "commit_sign"]),
        dict(co="Draycombe Importers Co.", P=260000, P2=295000, M=180000, M2=150000, date="October 1", use=["omit_fx", "fx_sign", "commit_sign"]),
        dict(co="Elmbridge Importers Co.", P=640000, P2=690000, M=420000, M2=330000, date="August 1", use=["omit_fx", "omit_commit", "commit_sign"]),
     ], "omit_commit"),

    ("far-contingencies-0015", A3, TOPIC_CONTINGENCIES, AP,
     ["ASC 450-20-25-2 (accrual of a loss contingency)"],
     litigation_trueup_and_new, [
        dict(co="Castor Fabricators", A=180000, B=230000, C=140000, use=["ignore_trueup", "full_settlement", "reverse_trueup"]),
        dict(co="Draymoor Fabricators", A=240000, B=310000, C=190000, use=["full_settlement", "reverse_trueup", "ignore_new"]),
        dict(co="Elswick Fabricators", A=95000, B=120000, C=75000, use=["ignore_trueup", "reverse_trueup", "ignore_new"]),
        dict(co="Falkbourne Fabricators", A=330000, B=410000, C=260000, use=["ignore_trueup", "full_settlement", "ignore_new"]),
     ], "full_settlement"),
    ("far-contingencies-0016", A3, TOPIC_CONTINGENCIES, AP,
     ["ASC 460-10-25 (product warranties)"],
     warranty_pct_of_sales, [
        dict(co="Harlow Equipment Co.", Beg=120000, Sales=3200000, pct="2.5", Paid=96000, use=["accrual_only", "no_paid", "no_accrual"]),
        dict(co="Ingram Equipment Co.", Beg=180000, Sales=4600000, pct="3", Paid=142000, use=["no_paid", "no_accrual", "double_pay"]),
        dict(co="Jarvington Equipment Co.", Beg=65000, Sales=1800000, pct="2", Paid=48000, use=["accrual_only", "no_accrual", "double_pay"]),
        dict(co="Kelbridge Equipment Co.", Beg=240000, Sales=5200000, pct="2.5", Paid=165000, use=["accrual_only", "no_paid", "double_pay"]),
     ], "no_paid"),
    ("far-contingencies-0017", A3, TOPIC_CONTINGENCIES, AP,
     ["ASC 450-20-25-2 (accrual of a loss contingency)", "ASC 450-30 (gain contingencies: a probable insurance recovery is recognized separately from the liability)"],
     litigation_with_recovery, [
        dict(co="Dalton Freight Co.", A2=90000, B2=130000, L=260000, R=150000, use=["no_recovery", "reverse_trueup", "no_trueup"]),
        dict(co="Eastgate Freight Co.", A2=130000, B2=185000, L=340000, R=200000, use=["reverse_trueup", "no_trueup", "recovery_sign"]),
        dict(co="Fenwick Freight Co.", A2=60000, B2=85000, L=160000, R=90000, use=["no_recovery", "no_trueup", "recovery_sign"]),
        dict(co="Gosbourne Freight Co.", A2=175000, B2=230000, L=420000, R=260000, use=["no_recovery", "reverse_trueup", "recovery_sign"]),
     ], "no_recovery"),

    ("far-contingencies-0018", A3, TOPIC_CONTINGENCIES, AN,
     ["ASC 460-10-30 and 35 (guarantee initial and subsequent measurement)", "ASC 450-20-25 (accrual requires a probable obligating event that has occurred)"],
     guarantee_and_conditional_settlement, [
        dict(co="Marchmont Equipment Co.", Fee=12000, Loan=400000, L=380000, S=150000, date="December 20", use=["adds_contingent_settlement", "sums_fv_and_contingent", "fv_only"]),
        dict(co="Netherfield Equipment Co.", Fee=18000, Loan=600000, L=540000, S=210000, date="December 15", use=["sums_fv_and_contingent", "fv_only", "settlement_only"]),
        dict(co="Oswestry Equipment Co.", Fee=9000, Loan=300000, L=260000, S=95000, date="December 22", use=["adds_contingent_settlement", "fv_only", "settlement_only"]),
        dict(co="Penhallow Equipment Co.", Fee=22000, Loan=750000, L=690000, S=280000, date="December 18", use=["adds_contingent_settlement", "sums_fv_and_contingent", "settlement_only"]),
     ], "sums_fv_and_contingent"),
    ("far-contingencies-0019", A3, TOPIC_CONTINGENCIES, AN,
     ["ASC 450-20-25-2 (an obligating event that has already occurred is accrued regardless of future payment timing)", "ASC 450-30-25 (gain contingencies not recognized until realization is assured)"],
     consent_order_and_appeal_receivable, [
        dict(co="Pentland Chemical Co.", Order=340000, Judgment=150000, date="November 10", use=["no_consent", "keeps_receivable", "no_adjust"]),
        dict(co="Quarrington Chemical Co.", Order=420000, Judgment=190000, date="November 18", use=["keeps_receivable", "no_adjust", "half_consent"]),
        dict(co="Rushmere Chemical Co.", Order=260000, Judgment=110000, date="December 2", use=["no_consent", "no_adjust", "half_consent"]),
        dict(co="Stonebridge Chemical Co.", Order=480000, Judgment=220000, date="November 5", use=["no_consent", "keeps_receivable", "half_consent"]),
     ], "keeps_receivable"),

    ("far-subsequent-events-0014", A3, TOPIC_SUBSEQUENT, AP,
     ["ASC 855-10-25-1 (recognized subsequent events: conditions existing at the balance sheet date)", "ASC 326-20 (measurement of expected credit losses)"],
     allowance_two_customers, [
        dict(co="Thornbury Co.", D1=90000, E1=15000, S1=20000, D2=60000, S2=25000, Other=140000, date1="January 20", date2="February 5", use=["no_adjust", "cust1_only", "wrong_amt"]),
        dict(co="Underwood Co.", D1=120000, E1=25000, S1=28000, D2=80000, S2=32000, Other=210000, date1="January 25", date2="February 10", use=["cust1_only", "cust2_only", "wrong_amt"]),
        dict(co="Verwood Co.", D1=70000, E1=10000, S1=14000, D2=45000, S2=18000, Other=95000, date1="January 18", date2="February 2", use=["no_adjust", "cust2_only", "wrong_amt"]),
        dict(co="Wrenbourne Co.", D1=150000, E1=30000, S1=36000, D2=100000, S2=40000, Other=260000, date1="January 28", date2="February 14", use=["no_adjust", "cust1_only", "cust2_only"]),
     ], "wrong_amt"),
    ("far-subsequent-events-0015", A3, TOPIC_SUBSEQUENT, AP,
     ["ASC 855-10-25-1 and 25-3 (recognized versus nonrecognized subsequent events)"],
     equipment_sale_and_flood, [
        dict(co="Castleford Fabrication Co.", BV=500000, Price=410000, Flood=70000, asset="production machine", date1="January 15", date2="February 10", use=["includes_flood", "flood_only", "gross_equipment"]),
        dict(co="Drumheller Fabrication Co.", BV=680000, Price=560000, Flood=90000, asset="stamping press", date1="January 20", date2="February 18", use=["flood_only", "gross_equipment", "wrong_equipment_calc"]),
        dict(co="Eastholm Fabrication Co.", BV=350000, Price=295000, Flood=50000, asset="packaging line", date1="January 12", date2="February 6", use=["includes_flood", "gross_equipment", "wrong_equipment_calc"]),
        dict(co="Furnivall Fabrication Co.", BV=820000, Price=660000, Flood=120000, asset="extrusion line", date1="January 22", date2="February 25", use=["includes_flood", "flood_only", "wrong_equipment_calc"]),
     ], "includes_flood"),

    ("far-subsequent-events-0016", A3, TOPIC_SUBSEQUENT, AN,
     ["ASC 855-10-25-1 (recognized subsequent events)", "ASC 470-10-45-11 to 45-13 (covenant violations: classification unless a waiver is obtained before the statements are issued)"],
     covenant_waiver_and_settlement, [
        dict(co="Ashcombe Materials Co.", CL=1240000, A=180000, B=130000, Debt=600000, date1="January 15", date2="February 20", date3="April", use=["reclass_full", "reclass_only", "no_adjust"]),
        dict(co="Beckworth Materials Co.", CL=1650000, A=240000, B=175000, Debt=820000, date1="January 22", date2="February 26", date3="May", use=["reclass_only", "no_adjust", "wrong_direction"]),
        dict(co="Cranmore Materials Co.", CL=980000, A=140000, B=95000, Debt=460000, date1="January 10", date2="February 12", date3="March", use=["reclass_full", "no_adjust", "wrong_direction"]),
        dict(co="Draycott Materials Co.", CL=1480000, A=210000, B=150000, Debt=720000, date1="January 28", date2="February 24", date3="April", use=["reclass_full", "reclass_only", "wrong_direction"]),
     ], "reclass_full"),
    ("far-subsequent-events-0017", A3, TOPIC_SUBSEQUENT, AN,
     ["ASC 855-10-25-1 and 25-3 (recognized versus nonrecognized subsequent events)", "ASC 326-20 (measurement of expected credit losses)"],
     quick_ratio_bankruptcy, [
        dict(co="Dunkeld Traders", Cash=200000, MS=150000, AR=600000, Allow=40000, CL=700000, D=90000, S=10000, E=15000, SecLoss=20000, date1="January 25", month2="March", use=["no_adjust", "full_d", "includes_securities_loss"]),
        dict(co="Elvanfoot Traders", Cash=260000, MS=180000, AR=760000, Allow=52000, CL=860000, D=120000, S=14000, E=20000, SecLoss=26000, date1="January 30", month2="March", use=["full_d", "includes_securities_loss", "wrong_allowance"]),
        dict(co="Fintry Traders", Cash=150000, MS=110000, AR=420000, Allow=26000, CL=480000, D=60000, S=7000, E=10000, SecLoss=14000, date1="January 19", month2="February", use=["no_adjust", "includes_securities_loss", "wrong_allowance"]),
        dict(co="Gartcosh Traders", Cash=320000, MS=230000, AR=900000, Allow=64000, CL=1050000, D=150000, S=18000, E=24000, SecLoss=32000, date1="February 2", month2="March", use=["no_adjust", "full_d", "wrong_allowance"]),
     ], "full_d"),
    ("far-subsequent-events-0018", A3, TOPIC_SUBSEQUENT, AN,
     ["ASC 855-10-25-1 (recognized subsequent events)", "ASC 330-10-35 (inventory write-down to net realizable value)", "ASC 470-10-45-14 (refinancing on a long-term basis before the statements are issued)"],
     working_capital_refinancing, [
        dict(co="Marwick Industries", CA=2400000, CL=1100000, C=180000, N=120000, Note=500000, date1="January 20", date2="February 15", use=["no_adjust", "inv_only", "refi_only"]),
        dict(co="Netherglen Industries", CA=3100000, CL=1450000, C=240000, N=160000, Note=650000, date1="January 24", date2="February 20", use=["inv_only", "refi_only", "wrong_sign"]),
        dict(co="Ottercombe Industries", CA=1820000, CL=820000, C=140000, N=90000, Note=380000, date1="January 16", date2="February 10", use=["no_adjust", "refi_only", "wrong_sign"]),
        dict(co="Pikeworth Industries", CA=2760000, CL=1260000, C=210000, N=130000, Note=560000, date1="January 29", date2="February 22", use=["no_adjust", "inv_only", "wrong_sign"]),
     ], "refi_only"),
]

WORD_ITEMS = []


def blind_files(items, scratch):
    """Stems and lettered choices only, for the blind verifier, plus a separate key file."""
    lines, keys = ["# FAR batch 17: blind verification input", "",
                   "Each block is one version of a question. Solve each independently; choose one letter.", ""], {}
    for it in items:
        for k, v in enumerate([it] + list(it.get("variants") or [])):
            label = f"{it['id']} v{k}"
            lines += [f"## {label}", "", v["stem"], ""]
            lines += [f"{c['id']}. {c['text']}" for c in v["choices"]] + [""]
            keys[label] = v["answer"]
    with open(os.path.join(scratch, "b17-blind.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(scratch, "b17-keys.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys, f, indent=1)
    print(f"blind file: {len(keys)} versions")


def main():
    # 2026-10-05: this script was mid-rewrite when the local session that built batch 17 ended. Its
    # builders now produce different questions under the same ids, so running it would overwrite the
    # committed batch 17 items (the reviewed versions in content/far) and reuse their ids. The YAML in
    # content/far is the source of truth for batch 17; give any new questions here new ids first.
    sys.exit("far-batch-17.py is out of sync with content/far; see the note in main()")
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
    if "--dry-run" in sys.argv:
        print("dry run: nothing written")
        return
    write_items(items, CONTENT)
    if SCRATCH:
        blind_files(items, SCRATCH)


if __name__ == "__main__":
    main()
