"""FAR batch 18 - 4 new items (16 problems with variants) on two Area III Application tasks that
already carry other items but in different formats:

- III.G.b, "Calculate adjustments for identified subsequent events" - existing items cover an inventory
  NRV decline, a litigation-accrual true-up, a bonus-pool recomputation and a royalty estimate; these two
  add a receivable write-down confirmed by a customer's post-year-end bankruptcy filing, and a long-lived
  asset impairment confirmed by a post-year-end contract cancellation. Both state plainly that the event
  is recognized (the task's own verb, "identified subsequent events", hands that fact to the student;
  quality bar item 5's exception for tasks whose blueprint verb gives the classification as a given).
- III.B.b, "Calculate amounts of contingencies and prepare journal entries" - existing items cover a
  warranty rate, a range with no amount more likely, a settlement revision, an onerous purchase
  commitment and a discounted installment settlement; these two add a loss contingency with three
  probability-weighted outcomes (testing accrual at the single most-likely amount, not the range minimum
  or the probability-weighted expected value) and a self-insured product-liability accrual that must
  include incurred-but-not-reported claims.

Numeric items ship with three variants each (method as in far-variants-02.py): each item is a builder
function; parameter set 0 rebuilds the reviewed item exactly, sets 1-3 become its variants via
attach_variants(), and every family moves the key's letter across its four versions.

Run: python3 scripts/batches/far-batch-18.py [--dry-run]
Every number and distractor below is computed in code (Decimal, rounded half up).
"""
import os
import sys
from decimal import ROUND_HALF_UP, Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AP, attach_variants, audit, finalize, mcq as _mcq, variant, write_items  # noqa: E402

A3 = "Area III — Select Transactions"
NOTE = "Batch 18. Written from scratch; answers solved and every number and distractor computed in code."
CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
REFS_SE = ["ASC 855-10 (recognized and nonrecognized subsequent events; evaluation through the date the "
           "statements are issued)"]
REFS_CONT = ["ASC 450-20 (loss contingencies: recognition and measurement)"]


def mcq(*a, **k):
    return _mcq(*a, batch=NOTE, **k)


def m(x):
    """$1,234 (or $1,234.56 when there are cents)."""
    x = D(x).quantize(D("0.01"), ROUND_HALF_UP)
    return f"${x:,.0f}" if x == x.to_integral() else f"${x:,.2f}"


# ── III.G.b: receivable write-down confirmed by a customer's bankruptcy filing ──────────────


def receivable_writedown(p):
    co, cust, filed, issue, deteriorate, stopped, r, rec = (
        p[k] for k in ("co", "cust", "filed", "issue", "deteriorate", "stopped", "r", "rec"))
    r, rec = D(r), D(rec)
    writedown = r - rec
    balance, half, full, zero = rec, r / 2, r, D(0)
    pool = {
        "balance": (m(balance),
                    f"Reports the {m(balance)} {cust} is now expected to pay as the adjustment, rather "
                    f"than the amount of the write-down."),
        "half": (m(half),
                 f"Writes the receivable down by half of its {m(r)} balance instead of down to the "
                 f"{m(rec)} {co} now expects to collect based on the bankruptcy filing."),
        "full": (m(full),
                 f"Writes off the entire {m(r)} receivable, ignoring the {m(rec)} {co} still expects to "
                 f"collect from {cust}."),
        "zero": ("$0",
                  f"Treats the bankruptcy filing as a nonrecognized subsequent event requiring disclosure "
                  f"only. The filing provides evidence about {cust}'s deteriorating finances, a condition "
                  f"that already existed at the balance sheet date, so it is recognized."),
    }
    key = (m(writedown),
           f"Correct. This is a recognized subsequent event: the bankruptcy filing provides evidence "
           f"about a condition, {cust}'s deteriorating finances, that already existed at year end. {co} "
           f"writes the receivable down to the {m(rec)} it now expects to collect, a {m(writedown)} "
           f"adjustment ({m(r)} − {m(rec)}).")
    choices = [pool[k] for k in p["use"]] + [key]
    answer = "ABCD"[len(choices) - 1]
    return variant(
        f"{co}'s December 31, Year 1, financial statements will be issued on {issue}, Year 2. At year end, "
        f"{co} carried a {m(r)} trade receivable from {cust}, which it judged fully collectible based on "
        f"information available at that date. {cust}'s finances had, in fact, been deteriorating since "
        f"{deteriorate}, Year 1, and {cust} had stopped paying nearly all of its trade creditors by "
        f"{stopped}, Year 1, though {co} did not learn this until {cust} filed for bankruptcy on {filed}, "
        f"Year 2. The bankruptcy filing disclosed this history and {co} now expects to collect only "
        f"{m(rec)} of the receivable. What adjustment should {co} make to its December 31, Year 1, "
        f"financial statements?",
        choices, answer, key[1])


SE_RECEIVABLE = [
    dict(co="Firthway Appliances Co.", cust="Major Buyer Corp.", filed="February 10", issue="March 15",
         deteriorate="October", stopped="December", r="340000", rec="90000", use=["balance", "half", "full"]),
    dict(co="Gorsefield Marine Co.", cust="Anchor Traders Inc.", filed="January 20", issue="February 28",
         deteriorate="September", stopped="November", r="480000", rec="60000", use=["balance", "half", "zero"]),
    dict(co="Thornbury Logistics Co.", cust="Westcote Freight Ltd.", filed="February 15", issue="April 2",
         deteriorate="November", stopped="January", r="300000", rec="200000", use=["balance", "full", "zero"]),
    dict(co="Pemberton Hardware Co.", cust="Caldwell Supply Co.", filed="January 30", issue="March 20",
         deteriorate="August", stopped="November", r="150000", rec="40000", use=["half", "full", "zero"]),
]


# ── III.G.b: asset impairment confirmed by a post-year-end contract cancellation ────────────


def impairment_confirmed(p):
    co, cust, cancel, issue, notice, x, fv = (
        p[k] for k in ("co", "cust", "cancel", "issue", "notice", "x", "fv"))
    x, fv = D(x), D(fv)
    loss = x - fv
    balance, half, full, zero = fv, x / 2, x, D(0)
    pool = {
        "balance": (m(balance),
                    f"Reports the machine's {m(balance)} fair value as the adjustment, rather than the "
                    f"loss needed to write the machine down to that amount."),
        "half": (m(half),
                 f"Writes the machine down by half of its {m(x)} carrying amount instead of down to its "
                 f"confirmed {m(fv)} fair value."),
        "full": (m(full),
                 f"Writes the machine's entire {m(x)} carrying amount off, as if it had no remaining "
                 f"value, when its confirmed fair value is {m(fv)}."),
        "zero": ("$0",
                  f"Treats {cust}'s cancellation as a nonrecognized subsequent event requiring disclosure "
                  f"only. {co} already had notice of the condition causing the loss, {cust}'s intent to "
                  f"cancel, before year end, so the impairment is recognized."),
    }
    key = (m(loss),
           f"Correct. This is a recognized subsequent event: {cust}'s formal cancellation confirms a "
           f"condition that existed at year end, {cust}'s stated intent to cancel. {co} writes the "
           f"machine down from its {m(x)} carrying amount to its confirmed {m(fv)} fair value, a {m(loss)} "
           f"loss ({m(x)} − {m(fv)}).")
    choices = [pool[k] for k in p["use"]] + [key]
    answer = "ABCD"[len(choices) - 1]
    return variant(
        f"{co}'s Year 1 financial statements, which report a specialized machine at its {m(x)} carrying "
        f"amount, will be issued on {issue}, Year 2. At December 31, Year 1, {cust}, the only customer "
        f"for the machine's output, was past due on payments and had told {co} that it intended to cancel "
        f"their purchase contract once the contract's notice period ran, though {co} had not yet received "
        f"formal cancellation. On {notice}, Year 2, before the statements are issued, {cust} delivered the "
        f"formal cancellation notice. With no other customer for the machine's specialized output, {co} "
        f"determines the machine's fair value is {m(fv)}. This is a recognized subsequent event. What "
        f"adjustment should {co} make to the carrying amount of the machine in its December 31, Year 1, "
        f"financial statements?",
        choices, answer, key[1])


SE_IMPAIRMENT = [
    dict(co="Oakhurst Fabrication Co.", cust="Calder Industrial Group", cancel="cancel", issue="March 10",
         notice="January 25", x="460000", fv="150000", use=["balance", "half", "full"]),
    dict(co="Westmarch Tooling Co.", cust="Dunbarton Freight Lines", cancel="cancel", issue="February 20",
         notice="January 8", x="600000", fv="90000", use=["balance", "half", "zero"]),
    dict(co="Ashgrove Precision Co.", cust="Pemberton Retail Group", cancel="cancel", issue="March 28",
         notice="February 2", x="520000", fv="340000", use=["balance", "full", "zero"]),
    dict(co="Nettlefold Machining Co.", cust="Harrowgate Supply Co.", cancel="cancel", issue="February 12",
         notice="January 15", x="280000", fv="60000", use=["half", "full", "zero"]),
]


# ── III.B.b: loss contingency with probability-weighted outcomes ───────────────────────────


def probable_outcome(p):
    co, cust, lo, lop, mid, midp, hi, hip = (
        p[k] for k in ("co", "cust", "lo", "lop", "mid", "midp", "hi", "hip"))
    lo, mid, hi = D(lo), D(mid), D(hi)
    lop, midp, hip = D(lop), D(midp), D(hip)
    assert lop + midp + hip == 100
    expected = (lo * lop + mid * midp + hi * hip) / 100
    pool = {
        "min": (m(lo), f"Accrues the smallest amount in the range of possible outcomes. A single amount, "
                       f"{m(mid)}, is more likely than any other single amount, so {co} accrues that "
                       f"amount rather than the range minimum."),
        "expected": (m(expected),
                     f"Accrues the probability-weighted expected value of the three outcomes "
                     f"({lop:.0f}% × {m(lo)} + {midp:.0f}% × {m(mid)} + {hip:.0f}% × {m(hi)} = "
                     f"{m(expected)}) rather than the single most likely amount. GAAP uses the expected "
                     f"value only when no single amount in a range is more likely than any other."),
        "max": (m(hi), f"Accrues the largest amount in the range of possible outcomes. A single amount, "
                       f"{m(mid)}, is more likely than any other single amount, so {co} accrues that "
                       f"amount rather than the range maximum."),
    }
    key = (m(mid),
           f"Correct. {co}'s attorney believes it is probable that {co} will have to pay {cust}, and "
           f"{m(mid)} is the single most likely amount, with a {midp:.0f}% likelihood against {lop:.0f}% "
           f"for {m(lo)} and {hip:.0f}% for {m(hi)}. When a loss is probable and a single amount within "
           f"a range of possible outcomes is a better estimate than any other, {co} accrues that amount.")
    choices = [pool[k] for k in ("min", "expected", "max")] + [key]
    answer = "ABCD"[len(choices) - 1]
    return variant(
        f"{co}'s attorney believes it is probable that {co} will have to pay damages to {cust} in a "
        f"pending lawsuit, and estimates three possible outcomes: a {lop:.0f}% chance of {m(lo)}, a "
        f"{midp:.0f}% chance of {m(mid)} and a {hip:.0f}% chance of {m(hi)}. No settlement offer has been "
        f"made. What amount should {co} accrue for this loss contingency?",
        choices, answer, key[1])


CONT_PROBABLE = [
    dict(co="Marchwood Fabrication Co.", cust="a former customer", lo="200000", lop="20", mid="350000",
         midp="50", hi="500000", hip="30"),
    dict(co="Hallowfield Instruments Co.", cust="a supplier", lo="120000", lop="10", mid="300000", midp="60",
         hi="600000", hip="30"),
    dict(co="Birchmoor Devices Co.", cust="a competitor", lo="100000", lop="35", mid="320000", midp="50",
         hi="600000", hip="15"),
    dict(co="Thaxted Mechanical Co.", cust="a distributor", lo="80000", lop="40", mid="260000", midp="45",
         hi="700000", hip="15"),
]


# ── III.B.b: self-insured product-liability accrual including IBNR claims ──────────────────


def self_insured_ibnr(p):
    co, reported, ibnr = (p[k] for k in ("co", "reported", "ibnr"))
    reported, ibnr = D(reported), D(ibnr)
    key_amt = reported + ibnr
    margin = key_amt + D(30000)
    zero = D(0)
    pool = {
        "reported": (m(reported),
                     f"Accrues only the {m(reported)} of claims already reported and unpaid, leaving out "
                     f"the claims incurred before year end but not yet reported."),
        "ibnr": (m(ibnr),
                 f"Accrues only the estimated {m(ibnr)} of claims incurred but not reported, leaving out "
                 f"the {m(reported)} already reported and unpaid."),
        "zero": ("$0",
                 f"Treats carrying no third-party policy as a reason not to accrue anything. {co} retains "
                 f"the risk itself, so it accrues the claims exactly as an insurer would reserve for them: "
                 f"both reported and incurred-but-not-reported claims that are probable and estimable."),
        "margin": (m(margin),
                   f"Adds an additional {m(D(30000))} margin on top of the reported and unreported claims. "
                   f"GAAP measures the accrual at the best estimate, not a cushion above it."),
    }
    key = (m(key_amt),
           f"Correct. {co} retains the risk for product-liability claims instead of transferring it to an "
           f"insurer, so it accrues claims the same way an insurer would reserve for them: the {m(reported)} "
           f"already reported and unpaid, plus the {m(ibnr)} of claims incurred before year end but not "
           f"yet reported, both judged probable and reasonably estimable, for {m(key_amt)}.")
    choices = [pool[k] for k in p["use"]] + [key]
    answer = "ABCD"[len(choices) - 1]
    return variant(
        f"{co} retains the risk for product-liability claims rather than carrying third-party insurance. "
        f"At December 31, Year 1, it has received and not yet paid {m(reported)} of claims for incidents "
        f"that occurred before year end, all deemed probable and reasonably estimable. Its claims actuary "
        f"also estimates that {m(ibnr)} of additional claims will likely be filed for incidents that "
        f"occurred before year end but had not yet been reported to {co} as of December 31, Year 1, an "
        f"amount it judges probable and reasonably estimable. What amount should {co} accrue for "
        f"product-liability claims at December 31, Year 1?",
        choices, answer, key[1])


CONT_IBNR = [
    dict(co="Marchwood Fabrication Co.", reported="180000", ibnr="95000", use=["reported", "ibnr", "zero"]),
    dict(co="Hallowfield Instruments Co.", reported="240000", ibnr="60000", use=["reported", "ibnr", "margin"]),
    dict(co="Birchmoor Devices Co.", reported="90000", ibnr="140000", use=["reported", "zero", "margin"]),
    dict(co="Thaxted Mechanical Co.", reported="310000", ibnr="40000", use=["ibnr", "zero", "reported"]),
]


def build(id, area, topic, skill, refs, fn, params):
    """One item from params[0] (finalized, so choices sort ascending), with params[1:] as its variants."""
    base = fn(params[0])
    it = mcq(id, area, topic, skill, refs, base["stem"],
             [(c["text"], c["rationale"]) for c in base["choices"]], base["answer"], base["explanation"])
    finalize([it])
    variants = [fn(p) for p in params[1:]]
    attach_variants(it, variants)
    letters = {it["answer"]} | {v["answer"] for v in it["variants"]}
    assert len(letters) > 1, f"{id}: the key letter never changes across versions"
    return it


def main():
    items = [
        build("far-subsequent-events-0019", A3, "Subsequent events", AP, REFS_SE,
              receivable_writedown, SE_RECEIVABLE),
        build("far-subsequent-events-0020", A3, "Subsequent events", AP, REFS_SE,
              impairment_confirmed, SE_IMPAIRMENT),
        build("far-contingencies-0020", A3, "Contingencies and commitments", AP, REFS_CONT,
              probable_outcome, CONT_PROBABLE),
        build("far-contingencies-0021", A3, "Contingencies and commitments", AP, REFS_CONT,
              self_insured_ibnr, CONT_IBNR),
    ]
    n = audit(items)
    print(f"{len(items)} items, {sum(len(it.get('variants') or []) for it in items)} variants, "
          f"{n} warnings", file=sys.stderr)
    if "--dry-run" not in sys.argv:
        write_items(items, CONTENT)
    if n:
        sys.exit(1)


if __name__ == "__main__":
    main()
