"""FAR variants 10: three variants for the four numeric FAR MCQs skipped by variants 04, 06 and 09
because every wrong answer sat in a fixed order around the key.

Method as in far-variants-09.py (shared helpers in variants.py). For each family a pool of 4-6
named-error distractors is built, some below the key's value and some above it (an over-inclusion
error on "the other side" of the key), so a different three per version puts the key at a different
letter. far-accounting-errors-0002 also varies the error's direction (overstated/understated) across
versions, which the brief allows for that item specifically.

Run: python3 scripts/batches/far-variants-10.py   See docs/reviews/far-variants-10.md.
"""
import os
from decimal import Decimal as D, ROUND_HALF_UP

import yaml

from common import is_numeric, sort_numeric, variant
from variants import m, pick, rd, run

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")


def presort_v0(item_id):
    """Re-sort an on-disk item's version-0 choices under the current ascending-order rule (common.py's
    sort_keys), since run() loads version 0 from disk as-is and never re-sorts it the way attach_variants
    re-sorts versions 1-3. Needed after a common.py change to the sort rule (e.g. "understated" now
    counting as a negative direction) makes a previously-correct order wrong under the new rule."""
    path = os.path.join(CONTENT, item_id + ".yaml")
    with open(path, encoding="utf-8") as f:
        item = yaml.safe_load(f)
    ch = item["choices"]
    if not is_numeric(ch):
        return
    right = next(c for c in ch if c["id"] == item["answer"])
    new = sort_numeric(ch)
    if new == ch:
        return
    for k, c in zip("ABCDEF", new):
        c["id"] = k
    item["choices"] = new
    item["answer"] = next(c["id"] for c in new if c is right)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(item, f, sort_keys=False, allow_unicode=True, width=100)
    print(f"{item_id}: version 0 re-sorted under the updated rule; new key letter {item['answer']}")


def r2(x):
    """Round half up to 2 decimal places, as a plain string ('1.68')."""
    return str(D(x).quantize(D("0.01"), ROUND_HALF_UP))


# ── far-accounting-errors-0002 (Rook): counterbalancing inventory error ───────────────────────


def inventory_counterbalance(p):
    co, amt, direction = p["co"], D(p["amt"]), p["direction"]
    short = co.split()[0]
    opp = "understated" if direction == "overstated" else "overstated"
    noun = {"overstated": "overstatement", "understated": "understatement"}
    ger = {"overstated": "overstating", "understated": "understating"}
    true_effect = {"overstated": "raises cost of goods sold and lowers income",
                   "understated": "lowers cost of goods sold and raises income"}[direction]
    pool = {
        "isolate": (f"{m(0)} net income; {m(amt)} {direction} retained earnings",
                    "Treats the error as affecting only Year 1 and carrying into retained earnings. "
                    f"The {direction} beginning inventory also {direction} Year 2 cost of goods sold."),
        "same_dir": (f"{m(amt)} {direction} net income; {m(amt)} {direction} retained earnings",
                     f"Reverses the direction for Year 2. An {direction} beginning inventory {true_effect}."),
        "no_offset": (f"{m(amt)} {opp} net income; {m(amt)} {opp} retained earnings",
                      f"Counts the Year 2 {noun[opp]} in retained earnings without the Year 1 "
                      f"{noun[direction]} it offsets."),
        "nothing": (f"{m(0)} net income; {m(0)} retained earnings",
                    "Believes the error is fully resolved because Year 2 ending inventory was stated "
                    f"correctly, overlooking that Year 2 beginning inventory, Year 1's {direction} ending "
                    "inventory, still " + direction + " Year 2 cost of goods sold."),
        "direct_adj": (f"{m(0)} net income; {m(amt)} {opp} retained earnings",
                       "Treats the Year 1 error as a direct adjustment to retained earnings, "
                       f"{opp} it by {m(amt)}, without recognizing that Year 2's own {direction} cost of "
                       "goods sold already reversed the effect."),
    }
    key = (f"{m(amt)} {opp} net income; {m(0)} retained earnings",
           f"Correct. Year 2 cost of goods sold was {direction}, {ger[opp]} Year 2 income by {m(amt)} and "
           f"offsetting Year 1's {noun[direction]}, so retained earnings at the end of Year 2 was correct.")
    choices, ans = pick(pool, key, p["use"])
    stem = (
        f"In Year 3, before its Year 3 statements are issued, {co} discovers that its inventory at "
        f"December 31, Year 1, was {direction} by {m(amt)}. Inventory at December 31, Year 2, was "
        "correct. Ignore income taxes. As originally reported, by how much were "
        f"{short}'s Year 2 net income and its December 31, Year 2, retained earnings misstated?"
    )
    explanation = (
        f"{direction.capitalize()} ending inventory in Year 1 {opp} Year 1 cost of goods sold and "
        f"{direction} Year 1 net income by {m(amt)}. That inventory became Year 2's beginning inventory, "
        f"{ger[direction]} Year 2 cost of goods sold and {ger[opp]} Year 2 net income by {m(amt)}. The two "
        "errors counterbalance, so retained earnings at December 31, Year 2, was correct, and no "
        "adjustment to Year 3 opening retained earnings is needed; the Year 2 comparative figures are "
        "restated if presented."
    )
    return variant(stem, choices, ans, explanation)


# ── far-contingencies-0005 (Quenby): lawsuit, unasserted claim, gain contingency ───────────────


def contingency_liabilities(p):
    co, L, R, U, G = p["co"], D(p["L"]), D(p["R"]), D(p["U"]), D(p["G"])
    short = co
    key_v = L + U
    pool = {
        "nets_omits": (m(L - R),
                       "Nets the insurance recovery against the lawsuit liability and omits the unasserted claim."),
        "nets_only": (m(L - R + U),
                      f"Nets the {m(R)} insurance recovery against the {m(L)} lawsuit liability, then adds "
                      f"back the {m(U)} unasserted claim: {m(L)} − {m(R)} + {m(U)} = {m(L - R + U)}. "
                      "The liability and the recovery receivable are reported separately."),
        "omits_claim": (m(L),
                        f"Omits the {m(U)} unasserted claim. An unasserted claim is accrued when assertion "
                        "is probable and a loss is probable and estimable."),
        "insurance_as_liab": (m(L + U + R),
                              f"Adds the confirmed {m(R)} insurance reimbursement as an additional liability "
                              "instead of recording it as a separate receivable."),
        "gain_as_liab": (m(L + U + G),
                         f"Misreads the patent-infringement matter, a gain contingency to {short}, as a "
                         f"loss and adds the expected {m(G)} award to the accrual."),
    }
    key = (m(key_v),
           f"Correct. The {m(L)} lawsuit liability, reported gross, plus the {m(U)} expected claim; the "
           "insurance recovery is a separate receivable.")
    choices, ans = pick(pool, key, p["use"])
    stem = (
        f"{short} Co. is preparing its December 31 statements, which have not been issued. Counsel's "
        "letter and other files show: (1) a customer sued "
        f"{short} in November over a defective product; counsel expects {short} to lose and estimates "
        f"damages of {m(L)}, and {short}'s insurer has confirmed in writing that it will reimburse "
        f"{m(R)} of any damages; (2) an employee was injured in a December accident at {short}'s plant; "
        f"no claim has been filed yet, but counsel expects one and expects {short} to pay about {m(U)}; "
        f"and (3) {short} is suing a competitor for patent infringement and counsel expects an award of "
        f"about {m(G)}. What total liabilities should {short} report for these matters?"
    )
    explanation = (
        f"(1) The loss is probable and estimable, so {short} accrues {m(L)}; the confirmed insurance "
        f"reimbursement is recognized as a separate {m(R)} receivable, not netted against the liability. "
        "(2) An unasserted claim is accrued when it is probable a claim will be asserted and probable "
        f"that the outcome will be unfavorable: {m(U)}. (3) The expected award is a gain contingency, not "
        f"recognized. Liabilities = {m(key_v)}."
    )
    return variant(stem, choices, ans, explanation)


# ── far-debt-covenant-0001 (Kade): debt-to-equity covenant with two unrecorded adjustments ─────


def debt_covenant(p):
    co, limit, liab0, eq0, w, d, day = (p[k] for k in ("co", "limit", "liab0", "eq0", "w", "d", "day"))
    liab0, eq0, w, d = D(liab0), D(eq0), D(w), D(d)
    short = co.split()[0]
    wd = w + d
    key_v = (liab0 + wd) / (eq0 - wd)
    pool = {
        "no_adjust": (r2(liab0 / eq0), "Uses the balances before the year-end adjustments."),
        "liab_only": (r2((liab0 + wd) / eq0),
                      f"Adds the {m(wd)} to liabilities but does not reduce stockholders' equity for the "
                      "warranty expense and the dividend."),
        "warranty_only": (r2((liab0 + w) / (eq0 - w)),
                          f"Records the warranty accrual but not the dividend declared December {day}, "
                          "which is a liability at year-end."),
        "dividend_only": (r2((liab0 + d) / (eq0 - d)),
                          "Records the dividend payable but not the warranty accrual, which is also a "
                          "liability at year-end for sales already made."),
        "equity_multiplier": (r2(key_v + 1),
                              "Confuses the ratio with the equity multiplier, total assets ÷ equity, "
                              f"which equals the debt-to-equity ratio plus 1: {r2(key_v)} + 1 = "
                              f"{r2(key_v + 1)}."),
    }
    key = (r2(key_v),
           f"Correct. ({m(liab0)} + {m(wd)}) ÷ ({m(eq0)} − {m(wd)}) = {r2(key_v)}, which violates "
           f"the {limit} limit.")
    choices, ans = pick(pool, key, p["use"], order=lambda c: D(c[0]))
    stem = (
        f"{co}'s loan agreement requires its ratio of total liabilities to total stockholders' equity to "
        f"be no more than {limit} at each year-end. Before year-end adjustments, {short}'s December 31 "
        f"balance sheet shows total liabilities of {m(liab0)} and total stockholders' equity of "
        f"{m(eq0)}. Two adjustments have not yet been recorded: an accrual for {m(w)} of warranty costs "
        f"on Year 1 sales, and a {m(d)} cash dividend the board declared on December {day}, payable "
        f"January 15. Ignore income taxes. What is {short}'s debt-to-equity ratio for the covenant test?"
    )
    explanation = (
        "Both adjustments increase liabilities and decrease equity. The warranty accrual is an expense "
        "(reducing retained earnings) and a liability; the declared dividend reduces retained earnings "
        f"and creates dividends payable. Liabilities = {m(liab0)} + {m(w)} + {m(d)} = {m(liab0 + wd)}. "
        f"Equity = {m(eq0)} − {m(wd)} = {m(eq0 - wd)}. Ratio = {m(liab0 + wd)} ÷ {m(eq0 - wd)} = "
        f"{r2(key_v)}, above the {limit} covenant."
    )
    return variant(stem, choices, ans, explanation)


# ── far-revenue-allocation-0003 (Harmon): allocating a bundle discount ─────────────────────────


def revenue_allocation(p):
    co, L, S, I_ssp, BP = p["co"], D(p["L"]), D(p["S"]), D(p["I"]), D(p["BP"])
    short = co.split()[0]
    disc = L + S - BP
    T = BP + I_ssp
    key_v = rd(BP * L / (L + S))
    pool = {
        "all_to_license": (m(rd(L - disc)),
                           f"Assigns the entire {m(disc)} discount to the license. The discount belongs to "
                           "the license-and-support bundle and is shared between those two in proportion "
                           "to their standalone selling prices."),
        "spread_three": (m(rd(T * L / (L + I_ssp + S))),
                         f"Spreads the discount across all three obligations ({m(T)} × {m(L)} "
                         f"÷ {m(L + I_ssp + S)}). Observable evidence shows the discount relates "
                         "only to the license and support."),
        "no_discount": (m(L), "Uses the license's standalone selling price and ignores the discount."),
        "equal_split": (m(rd(L - disc / 3)),
                       f"Divides the {m(disc)} discount equally among the three performance obligations "
                       f"instead of by standalone selling price: {m(L)} − ({m(disc)} ÷ 3) = "
                       f"{m(L)} − {m(rd(disc / 3))}."),
        "full_contract_price": (m(rd(T * L / (L + S))),
                                f"Uses the full {m(T)} transaction price for the license-and-support "
                                f"allocation instead of the {m(BP)} bundle price, without first setting "
                                f"aside implementation's {m(I_ssp)} standalone selling price: {m(T)} "
                                f"× {m(L)} ÷ {m(L + S)}."),
        "residual": (m(rd(T - I_ssp - S)),
                    f"Uses the residual approach: {m(T)} − {m(I_ssp)} − {m(S)} = "
                    f"{m(rd(T - I_ssp - S))}. The residual approach isn't available for the license "
                    "because it has an observable standalone selling price (ASC 606-10-32-34(c))."),
    }
    key = (m(key_v),
           f"Correct. The {m(disc)} discount matches the regular license-and-support bundle, so it is "
           f"allocated to those two only: {m(BP)} × {m(L)} ÷ {m(L + S)}.")
    choices, ans = pick(pool, key, p["use"])
    stem = (
        f"{co} enters into a contract to sell a software license, implementation services, and one year "
        f"of post-contract support for a total of {m(T)}. {short} regularly sells each item separately at "
        f"these standalone selling prices: license {m(L)}, implementation {m(I_ssp)}, and support "
        f"{m(S)}. It also regularly sells the license and one year of support together, without "
        f"implementation, for {m(BP)}. The implementation is a standard installation that does not "
        "modify the software, and several other firms offer it. How much of the transaction price should "
        f"{short} allocate to the license?"
    )
    explanation = (
        "The implementation does not modify the software and is available from other firms, so the "
        "license, implementation, and support are distinct performance obligations. The contract's "
        f"discount is {m(L + I_ssp + S)} − {m(T)} = {m(disc)}. {short} regularly sells each item "
        f"separately, and regularly sells the license and support together at the same {m(disc)} "
        "discount, which is observable evidence that the whole discount relates to those two. "
        f"Implementation gets its {m(I_ssp)} standalone selling price, and the remaining {m(BP)} is split "
        f"between license and support by their standalone selling prices: {m(BP)} × {m(L)} "
        f"÷ {m(L + S)} = {m(key_v)}."
    )
    return variant(stem, choices, ans, explanation)


FAMILIES = {
    "far-accounting-errors-0002": (inventory_counterbalance, [
        dict(co="Rook Co.", amt=40000, direction="overstated", use=["isolate", "same_dir", "no_offset"]),
        dict(co="Finch Co.", amt=55000, direction="understated", use=["isolate", "nothing", "direct_adj"]),
        dict(co="Garrow Co.", amt=28000, direction="overstated", use=["nothing", "direct_adj", "same_dir"]),
        dict(co="Holt Co.", amt=63000, direction="understated", use=["nothing", "direct_adj", "no_offset"]),
    ]),
    "far-contingencies-0005": (contingency_liabilities, [
        dict(co="Quenby", L=200000, R=150000, U=30000, G=80000,
             use=["nets_omits", "nets_only", "omits_claim"]),
        dict(co="Ransome", L=320000, R=260000, U=45000, G=95000,
             use=["nets_omits", "nets_only", "insurance_as_liab"]),
        dict(co="Sorrel", L=150000, R=90000, U=20000, G=60000,
             use=["omits_claim", "insurance_as_liab", "gain_as_liab"]),
        dict(co="Trevane", L=400000, R=310000, U=55000, G=120000,
             use=["nets_only", "insurance_as_liab", "gain_as_liab"]),
    ]),
    "far-debt-covenant-0001": (debt_covenant, [
        dict(co="Kade Inc.", limit="1.60", liab0=1800000, eq0=1250000, w=60000, d=50000, day=20,
             use=["no_adjust", "liab_only", "warranty_only"]),
        dict(co="Larchmont Inc.", limit="1.50", liab0=2400000, eq0=1600000, w=80000, d=70000, day=18,
             use=["no_adjust", "dividend_only", "equity_multiplier"]),
        dict(co="Marchetti Inc.", limit="1.40", liab0=900000, eq0=620000, w=25000, d=30000, day=22,
             use=["liab_only", "warranty_only", "dividend_only"]),
        dict(co="Norwood Inc.", limit="1.30", liab0=3100000, eq0=2200000, w=95000, d=60000, day=27,
             use=["dividend_only", "warranty_only", "equity_multiplier"]),
    ]),
    "far-revenue-allocation-0003": (revenue_allocation, [
        dict(co="Harmon Technologies", L=240000, S=60000, I=100000, BP=270000,
             use=["all_to_license", "spread_three", "no_discount"]),
        dict(co="Blythe Software", L=280000, S=70000, I=90000, BP=315000,
             use=["spread_three", "equal_split", "no_discount"]),
        dict(co="Cantrell Systems", L=320000, S=60000, I=120000, BP=330000,
             use=["residual", "no_discount", "equal_split"]),
        dict(co="Delacroix Media", L=260000, S=50000, I=110000, BP=270000,
             use=["residual", "spread_three", "equal_split"]),
    ]),
}

if __name__ == "__main__":
    presort_v0("far-accounting-errors-0002")
    run(FAMILIES, CONTENT)
