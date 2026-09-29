"""FAR simulations batch 01 — three original task-based simulations (numeric and journal-entry tasks only; research
tasks wait until cited paragraphs can be verified against the Codification). See docs/reviews/far-tbs-01.md.

Run: python3 scripts/batches/far-tbs-01.py  (writes content/far/far-tbs-*.yaml)
Currency amounts are whole cents. Every number was computed in code (Decimal, rounded half up).
"""
import os
from decimal import Decimal, ROUND_HALF_UP

import yaml

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "FAR simulations batch 01. Written from scratch; every number computed in code."


def usd(x):
    """Whole dollars, rounded half up."""
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def c(dollars):
    """Dollars to cents."""
    return int(dollars) * 100


def line(account, debit=0, credit=0):
    return dict(account=account, debit=c(debit), credit=c(credit))


def tbs(id, area, topic, skill, refs, title, scenario, exhibits, tasks):
    return dict(
        id=id, type="tbs",
        blueprint=dict(section="FAR", area=area, topic=topic, skill=skill),
        review=dict(status="reviewed", references=refs, notes=NOTE),
        title=title, scenario=scenario.strip(),
        exhibits=[dict(title=t, body=b.strip()) for t, b in exhibits],
        tasks=tasks,
    )


# ── Simulation 1: lessee finance lease ────────────────────────────────────
PV = Decimal("4.2124")
liability = usd(40000 * PV)                     # 168,496
rou = liability + 3000                          # 171,496
interest1 = usd(liability * Decimal("0.06"))    # 10,110
principal1 = 40000 - interest1                  # 29,890
ending1 = liability - principal1                # 138,606
amort1 = usd(Decimal(rou) / 8)                  # 21,437

SIM1 = tbs(
    "far-tbs-lessee-finance-0001", A3, "Lessee accounting", "Application",
    ["ASC 842-10 (lease classification)", "ASC 842-20 (lessee finance leases: initial and subsequent measurement)"],
    "Finance lease: commencement and first year",
    """On January 1, Year 1, Ridge Co. leases production equipment for five years. Ridge pays $40,000 at the end of each year, and title to the equipment transfers to Ridge when the lease ends. The equipment's economic life is eight years. The rate implicit in the lease is not readily determinable, so Ridge uses its 6% incremental borrowing rate. Ridge paid $3,000 of initial direct costs in cash at commencement. Ridge depreciates owned equipment of this kind straight-line with no residual value.""",
    [("Present value factors at 6%", """
| Periods | Single sum | Ordinary annuity | Annuity due |
|---|---|---|---|
| 5 | 0.7473 | 4.2124 | 4.4651 |
| 8 | 0.6274 | 6.2098 | 6.5824 |
""")],
    [
        dict(id="t1", type="journal_entry", points=2,
             prompt="Prepare Ridge's journal entry at lease commencement on January 1, Year 1.",
             accounts=["Right-of-use asset", "Lease liability", "Cash", "Prepaid rent", "Lease expense", "Interest expense"],
             answer=[line("Right-of-use asset", debit=rou), line("Lease liability", credit=liability), line("Cash", credit=3000)],
             explanation=f"Transfer of ownership makes this a finance lease. The liability is the present value of the payments: $40,000 × 4.2124 = ${liability:,}. The right-of-use asset adds the ${3000:,} of initial direct costs: ${rou:,}."),
        dict(id="t2", type="journal_entry", points=2,
             prompt="Prepare Ridge's journal entry for the lease payment on December 31, Year 1. Record only the payment; Ridge records amortization in a separate entry.",
             accounts=["Interest expense", "Lease liability", "Cash", "Lease expense", "Right-of-use asset", "Amortization expense"],
             answer=[line("Interest expense", debit=interest1), line("Lease liability", debit=principal1), line("Cash", credit=40000)],
             explanation=f"Interest = ${liability:,} × 6% = ${interest1:,} (rounded to the dollar). The rest of the $40,000 payment, ${principal1:,}, reduces the liability. A finance lease has no single straight-line lease expense."),
        dict(id="t3", type="numeric", points=1, unit="cents", tolerance=0,
             prompt="What amortization expense on the right-of-use asset should Ridge recognize for Year 1?",
             answer=c(amort1),
             explanation=f"Because ownership transfers, the asset is amortized over its eight-year economic life, not the five-year lease term: ${rou:,} ÷ 8 = ${amort1:,}."),
        dict(id="t4", type="numeric", points=1, unit="cents", tolerance=0,
             prompt="What is the carrying amount of Ridge's lease liability at December 31, Year 1?",
             answer=c(ending1),
             explanation=f"${liability:,} − ${principal1:,} principal reduction = ${ending1:,}."),
    ],
)

# ── Simulation 2: bank reconciliation ─────────────────────────────────────
bank, book = 14285, 12400
dit, osc = 2300, 3100
svc, nsf, note, note_int = 35, 800, 2000, 100
check_error = 640 - 460
adj_bank = bank + dit - osc                                   # 13,485
net_book = -svc - nsf + note + note_int - check_error         # +1,085
adj_book = book + net_book
assert adj_bank == adj_book

SIM2 = tbs(
    "far-tbs-bank-reconciliation-0001", A2, "Cash and cash equivalents", "Analysis",
    ["ASC 305-10 (cash)", "Bank reconciliation practice"],
    "Bank reconciliation and adjusting entry",
    """Hollis Co. is reconciling its checking account at June 30. The bank statement balance is $14,285 and the general ledger cash balance is $12,400. Use the exhibit to reconcile the account and record the entry the general ledger needs.""",
    [("Reconciling items found", """
| Item | Amount |
|---|---|
| Deposit of June 30 not on the bank statement | $2,300 |
| Checks written in June that have not cleared the bank | $3,100 |
| Bank service charge for June, not recorded by Hollis | $35 |
| Customer check returned by the bank for nonsufficient funds | $800 |
| Note receivable collected by the bank for Hollis ($2,000 principal plus $100 interest), not recorded by Hollis | $2,100 |
| Check #884 in payment of an account payable to a supplier, cleared by the bank for its correct amount of $640, recorded by Hollis as $460 | $180 |
""")],
    [
        dict(id="t1", type="numeric", points=1, unit="cents", tolerance=0,
             prompt="What is Hollis's correct cash balance at June 30?",
             answer=c(adj_bank),
             explanation=f"Bank side: ${bank:,} + ${dit:,} deposit in transit − ${osc:,} outstanding checks = ${adj_bank:,}. Book side: ${book:,} − $35 − $800 + $2,100 − $180 = ${adj_book:,}."),
        dict(id="t2", type="journal_entry", points=3,
             prompt="Prepare one compound journal entry to bring Hollis's general ledger into agreement with the reconciliation. Record only the items that require an entry on Hollis's books, and show the net change in Cash as a single line.",
             accounts=["Cash", "Bank service charge expense", "Accounts receivable", "Accounts payable", "Notes receivable",
                       "Interest revenue", "Outstanding checks", "Deposits in transit", "Allowance for credit losses"],
             answer=[line("Cash", debit=net_book), line("Bank service charge expense", debit=svc), line("Accounts receivable", debit=nsf),
                     line("Accounts payable", debit=check_error), line("Notes receivable", credit=note), line("Interest revenue", credit=note_int)],
             explanation=f"Only book-side items need entries. The NSF check reinstates the receivable ($800); the service charge is an expense ($35); the collected note removes the receivable and records interest ($2,000 and $100); the recording error understated the payment to the supplier, so accounts payable is reduced by another $180. Net effect on cash: +${net_book:,}. Deposits in transit and outstanding checks need no entry."),
    ],
)

# ── Simulation 3: income tax provision ────────────────────────────────────
pretax, muni, depr, warr = 800000, 20000, 60000, 40000
rate = Decimal("0.21")
taxable = pretax - muni - depr + warr                 # 750,000
current = usd(taxable * rate)                         # 157,500
dtl = usd(depr * rate)                                # 12,600
dta = usd(warr * rate)                                # 6,300
deferred = dtl - dta                                  # 6,300
total = current + deferred                            # 163,800

SIM3 = tbs(
    "far-tbs-income-tax-provision-0001", A3, "Accounting for income taxes", "Application",
    ["ASC 740-10 (current and deferred taxes; temporary and permanent differences)"],
    "Income tax provision",
    """Keane Corp. completed its first year of operations with pretax financial income of $800,000. The enacted federal rate for this and all future years is 21%, and there are no state taxes. Management expects enough future taxable income to realize any deferred tax asset. Use the exhibit to prepare the income tax provision.""",
    [("Book-tax differences for Year 1", """
| Item | Amount |
|---|---|
| Interest on municipal bonds included in pretax income, not taxable | $20,000 |
| Tax depreciation in excess of book depreciation | $60,000 |
| Warranty expense accrued for books, deductible when paid next year | $40,000 |
""")],
    [
        dict(id="t1", type="numeric", points=1, unit="cents", tolerance=0,
             prompt="What is Keane's taxable income for Year 1?",
             answer=c(taxable),
             explanation=f"${pretax:,} − ${muni:,} tax-exempt interest (permanent) − ${depr:,} excess tax depreciation + ${warr:,} warranty accrual not yet deductible = ${taxable:,}."),
        dict(id="t2", type="journal_entry", points=3,
             prompt="Prepare Keane's journal entry to record income tax expense for Year 1. Record the deferred tax asset and the deferred tax liability separately (do not offset them).",
             accounts=["Income tax expense — current", "Income tax expense — deferred", "Income taxes payable",
                       "Deferred tax asset", "Deferred tax liability", "Valuation allowance", "Interest revenue"],
             answer=[line("Income tax expense — current", debit=current), line("Income tax expense — deferred", debit=deferred),
                     line("Deferred tax asset", debit=dta), line("Income taxes payable", credit=current), line("Deferred tax liability", credit=dtl)],
             explanation=f"Current tax = ${taxable:,} × 21% = ${current:,}. The depreciation difference creates a deferred tax liability of ${dtl:,}; the warranty accrual creates a deferred tax asset of ${dta:,}. Deferred tax expense = ${dtl:,} − ${dta:,} = ${deferred:,}. No valuation allowance is needed."),
        dict(id="t3", type="numeric", points=1, unit="cents", tolerance=0,
             prompt="What total income tax expense should Keane report for Year 1?",
             answer=c(total),
             explanation=f"${current:,} current + ${deferred:,} deferred = ${total:,}. The tax-exempt interest is a permanent difference, so the effective rate ({Decimal(total) / pretax:.2%}) is below 21%."),
    ],
)

ITEMS = [SIM1, SIM2, SIM3]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
    for it in ITEMS:
        with open(os.path.join(out, it["id"] + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(it, f, sort_keys=False, allow_unicode=True, width=100)
    for it in ITEMS:
        pts = sum(t["points"] for t in it["tasks"])
        print(it["id"], len(it["tasks"]), "tasks,", pts, "points")
    print("check", liability, rou, interest1, principal1, ending1, amort1, adj_bank, net_book, taxable, current, dtl, dta, total)
