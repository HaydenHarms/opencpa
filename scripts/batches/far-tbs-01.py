"""FAR simulations batch 01 — three original task-based simulations (numeric and journal-entry tasks only; research
tasks wait until cited paragraphs can be verified against the Codification). See docs/reviews/far-tbs-01.md.

Revision 2 (after the review gate): each simulation is rebuilt from source-style exhibits with facts the candidate
must sort, carries 6-9 points, and tells the candidate how to round. Currency answers accept +/- $1; journal
entries are graded after netting by account, so each key has one line per account.

Run: python3 scripts/batches/far-tbs-01.py  (writes content/far/far-tbs-*.yaml)
Revision 2 replaced the three revision-1 simulations with new ones under new ids (student progress is keyed to the id).
Currency amounts are whole cents. Every number was computed in code (Decimal, rounded half up).
"""
import os
from decimal import Decimal, ROUND_HALF_UP

import yaml

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "FAR simulations batch 01, revision 2 (after the review gate). Written from scratch; every number computed in code."


def usd(x):
    """Whole dollars, rounded half up."""
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def c(dollars):
    """Dollars to cents."""
    return int(dollars) * 100


def d(x):
    return f"${x:,}"


def line(account, debit=0, credit=0):
    return dict(account=account, debit=c(debit), credit=c(credit))


def num(id, prompt, dollars, explanation, points=1):
    """A currency task: the key in cents, accepting answers within $1."""
    return dict(id=id, type="numeric", points=points, unit="cents", tolerance=100, prompt=prompt,
                answer=c(dollars), explanation=explanation)


def je(id, prompt, accounts, lines, explanation, points):
    return dict(id=id, type="journal_entry", points=points, prompt=prompt, accounts=accounts, answer=lines,
                explanation=explanation)


def f4(x):
    return Decimal(x).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def pv1(r, n):
    return f4(1 / (1 + Decimal(r)) ** n)


def pva(r, n):
    r = Decimal(r)
    return f4((1 - 1 / (1 + r) ** n) / r)


def pvad(r, n):
    return f4(pva(r, n - 1) + 1)


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
PAY, N, LIFE, OPT, IDC, R = 50000, 6, 9, 20000, 4000, Decimal("0.07")
F_ANN, F_ONE = pva(R, N), pv1(R, N)
pv_pay, pv_opt = usd(PAY * F_ANN), usd(OPT * F_ONE)
liability = pv_pay + pv_opt
rou = liability + IDC
interest1 = usd(liability * R)
principal1 = PAY - interest1
ending1 = liability - principal1
interest2 = usd(ending1 * R)
current2 = PAY - interest2
amort1 = usd(Decimal(rou) / LIFE)

rows = []
for rate in ("0.07", "0.08"):
    for per in (6, 9):
        rows.append(f"| {int(Decimal(rate) * 100)}% | {per} | {pv1(rate, per)} | {pva(rate, per)} | {pvad(rate, per)} |")
FACTORS = "| Rate | Periods | Single sum | Ordinary annuity | Annuity due |\n|---|---|---|---|---|\n" + "\n".join(rows)

SIM1 = tbs(
    "far-tbs-lessee-accounting-0001", A3, "Lessee accounting", "Application",
    ["ASC 842-10 (lease classification; lease term and purchase options)",
     "ASC 842-20 (lessee finance leases: initial and subsequent measurement, amortization period)"],
    "Equipment lease: commencement and first year",
    """Ridge Co., a public business entity, signed the equipment lease summarized in Exhibit 1 and must record it for Year 1. Ridge reports the initial direct costs it pays as an investing cash outflow. Use the present value factors in Exhibit 2 and round every amount to the nearest dollar.""",
    [("Exhibit 1: Lease summary prepared by Ridge's controller", f"""
| Term | Detail |
|---|---|
| Asset | Packaging line, delivered and ready for use on January 1, Year 1 |
| Lease term | Six years from January 1, Year 1; not cancellable |
| Payments | {d(PAY)} at the end of each year (December 31), starting in Year 1 |
| Purchase option | Ridge may buy the line for {d(OPT)} at the end of Year 6. Ridge's engineers estimate the line will then be worth about $95,000, and Ridge has no other line that could replace it. |
| Economic life | Nine years from January 1, Year 1, with no residual value |
| Fair value at commencement | $300,000 |
| Rates | The lessor has not disclosed its implicit rate. Ridge's incremental borrowing rate is 7%; its bank quoted 8% for a five-year unsecured loan. |
| Initial direct costs | {d(IDC)} of commissions, paid in cash on January 1, Year 1 |
| Maintenance | Ridge pays a separate service company $3,000 a year to maintain the line |
| Ridge's policy | Owned equipment of this kind is depreciated straight-line |
"""),
     ("Exhibit 2: Present value factors", FACTORS)],
    [
        je("t1", "Prepare Ridge's journal entry at lease commencement on January 1, Year 1.",
           ["Right-of-use asset", "Lease liability", "Cash", "Prepaid rent", "Lease expense", "Interest expense", "Equipment"],
           [line("Right-of-use asset", debit=rou), line("Lease liability", credit=liability), line("Cash", credit=IDC)],
           f"Ridge is reasonably certain to exercise the {d(OPT)} purchase option (the line should be worth about $95,000 then, and Ridge has no substitute), so the lease is a finance lease and the option price is a lease payment. The rate implicit in the lease isn't known, so Ridge uses its 7% incremental borrowing rate. Liability = {d(PAY)} × {F_ANN} + {d(OPT)} × {F_ONE} = {d(pv_pay)} + {d(pv_opt)} = {d(liability)}. The right-of-use asset adds the {d(IDC)} of initial direct costs: {d(rou)}. The $300,000 fair value and the maintenance paid to a third party are not lease payments.",
           points=2),
        je("t2", "Prepare Ridge's journal entries on December 31, Year 1, for the lease payment and any related amortization or expense.",
           ["Interest expense", "Amortization expense", "Lease expense", "Lease liability", "Right-of-use asset", "Cash", "Prepaid rent"],
           [line("Interest expense", debit=interest1), line("Amortization expense", debit=amort1), line("Lease liability", debit=principal1),
            line("Right-of-use asset", credit=amort1), line("Cash", credit=PAY)],
           f"Payment: interest = {d(liability)} × 7% = {d(interest1)}, and the rest of the {d(PAY)} payment, {d(principal1)}, reduces the liability. Amortization: because Ridge is reasonably certain to exercise the purchase option, the right-of-use asset is amortized over the nine-year economic life, not the six-year lease term: {d(rou)} ÷ {LIFE} = {d(amort1)}. A finance lease has no single straight-line lease expense.",
           points=3),
        num("t3", "What is the carrying amount of Ridge's right-of-use asset at December 31, Year 1?", rou - amort1,
            f"{d(rou)} − {d(amort1)} amortization over the nine-year economic life = {d(rou - amort1)}."),
        num("t4", "What is the total carrying amount of Ridge's lease liability at December 31, Year 1?", ending1,
            f"{d(liability)} − {d(principal1)} = {d(ending1)}."),
        num("t5", "What amount of the lease liability should Ridge classify as current at December 31, Year 1 (the principal to be repaid within 12 months)?", current2,
            f"The current portion is the principal that the Year 2 payment will repay: Year 2 interest is {d(ending1)} × 7% = {d(interest2)}, so {d(PAY)} − {d(interest2)} = {d(current2)}."),
        num("t6", "What amount should Ridge report as financing cash outflows for the lease in its Year 1 statement of cash flows?", principal1,
            f"For a finance lease, the part of each payment that repays principal is a financing outflow: {d(principal1)}. The {d(interest1)} of interest is an operating outflow, and Ridge reports the {d(IDC)} of initial direct costs as investing. The maintenance is paid to a third party and is an operating outflow."),
    ],
)

# ── Simulation 2: bank reconciliation ─────────────────────────────────────
MAY_BANK, MAY_DIT = 15000, 2050
MAY_OS = {861: 1200, 866: 415}
may_book = MAY_BANK + MAY_DIT - sum(MAY_OS.values())
RECEIPTS = [("June 12", 1250), ("June 20", 3300), ("June 30", 2700)]
CHECKS = [(870, "June 3", "Bayside Supply (on account)", 2480), (871, "June 8", "June rent", 910),
          (872, "June 15", "Corbel Freight (on account)", 1375), (873, "June 19", "Lark Paper (on account)", 460),
          (874, "June 24", "Transfer to payroll account", 3150), (875, "June 29", "Utilities", 725)]
ACH, INTEREST, NSF, WIRE, SVC = 1560, 42, 800, 25, 35
BANK_ROWS = [("June 1", "Deposit", 0, 2050), ("June 3", "Check 861", 1200, 0), ("June 6", "Check 870", 2480, 0),
             ("June 11", "Check 871", 910, 0), ("June 12", "Deposit", 0, 1520),
             ("June 18", "Returned item: customer check (Patel Co.), insufficient funds", NSF, 0),
             ("June 20", "Deposit", 0, 3300), ("June 23", "Check 873", 640, 0), ("June 25", "ACH credit: Oakley Ltd.", 0, ACH),
             ("June 26", "Check 874", 3150, 0), ("June 27", "Wire transfer fee (vendor inquiry)", WIRE, 0),
             ("June 30", "Interest earned", 0, INTEREST), ("June 30", "Monthly service charge", SVC, 0)]
bal, stmt = MAY_BANK, []
for dt, desc, dr, cr in BANK_ROWS:
    bal += cr - dr
    stmt.append(f"| {dt} | {desc} | {d(dr) if dr else ''} | {d(cr) if cr else ''} | {d(bal)} |")
bank_end = bal
book_end = may_book + sum(a for _, a in RECEIPTS) - sum(a for *_, a in CHECKS)
dit = 2700
os_checks = 415 + 1375 + 725
bank_error = 1520 - 1250
check_error = 640 - 460
adj_bank = bank_end + dit - os_checks - bank_error
fees = WIRE + SVC
net_book = ACH + INTEREST - NSF - fees - check_error
adj_book = book_end + net_book
assert adj_bank == adj_book, (adj_bank, adj_book)
ar_net = ACH - NSF
BANK_STMT = ("| Date | Description | Debits | Credits | Balance |\n|---|---|---|---|---|\n"
             f"| May 31 | Opening balance | | | {d(MAY_BANK)} |\n" + "\n".join(stmt))

SIM2 = tbs(
    "far-tbs-bank-reconciliation-0002", A2, "Cash and cash equivalents", "Analysis",
    ["ASC 305-10 (cash)", "Bank reconciliation practice"],
    "June bank reconciliation",
    f"""Hollis Co. reconciles its only checking account each month. Its general ledger cash balance at June 30 is {d(book_end)}. The exhibits show the May reconciliation, the June bank statement, Hollis's June cash journals and three supporting documents. Hollis also keeps a $300 petty cash fund, which is not part of this account.""",
    [("Exhibit 1: May 31 reconciliation (summary)", f"""
| Item | Amount |
|---|---|
| Balance per bank statement | {d(MAY_BANK)} |
| Deposit in transit (May 31) | {d(MAY_DIT)} |
| Outstanding check 861 | {d(1200)} |
| Outstanding check 866 | {d(415)} |
| Balance per books | {d(may_book)} |
"""),
     ("Exhibit 2: June bank statement", BANK_STMT),
     ("Exhibit 3: Hollis's June cash journals",
      "Cash receipts (deposits):\n\n| Date | Amount |\n|---|---|\n"
      + "\n".join(f"| {dt} | {d(a)} |" for dt, a in RECEIPTS)
      + "\n\nCash disbursements (checks):\n\n| Check | Date | Payee | Amount |\n|---|---|---|---|\n"
      + "\n".join(f"| {no} | {dt} | {p} | {d(a)} |" for no, dt, p, a in CHECKS)),
     ("Exhibit 4: Source documents", f"""
| Document | Detail |
|---|---|
| Deposit slip, June 12 | Customer checks from Avery Co. $700 and Boyle Inc. $550; total {d(1250)} |
| Lark Paper invoice 2231, dated June 2 | Office paper; amount due $640; paid by check 873 |
| Oakley Ltd. remittance advice, June 25 | ACH payment of {d(ACH)} for Hollis invoice 5518, dated May 20 |
""")],
    [
        num("t1", "What are Hollis's deposits in transit at June 30?", dit,
            f"The June 30 deposit of {d(dit)} is in the cash receipts journal but not on the bank statement. The June 1 bank deposit is May's deposit in transit, and the June 12 and June 20 deposits reached the bank."),
        num("t2", "What is the total of Hollis's outstanding checks at June 30?", os_checks,
            f"Check 866 ($415) from May still hasn't cleared, and neither have June checks 872 ($1,375) and 875 ($725): {d(os_checks)}. Check 861 cleared in June, and check 873 cleared for $640."),
        num("t3", "What is the correct (adjusted) balance of Hollis's checking account at June 30?", adj_bank,
            f"Bank side: {d(bank_end)} + {d(dit)} deposits in transit − {d(os_checks)} outstanding checks − {d(bank_error)} bank error (the bank credited {d(1520)} for a {d(1250)} deposit) = {d(adj_bank)}. Book side: {d(book_end)} + {d(ACH)} ACH collection + {d(INTEREST)} interest − {d(NSF)} NSF check − {d(fees)} fees − {d(check_error)} understatement of check 873 = {d(adj_book)}."),
        je("t4", "Prepare Hollis's journal entry, or entries, to bring the general ledger into agreement with the reconciliation.",
           ["Cash", "Accounts receivable", "Accounts payable", "Bank service charge expense", "Interest revenue",
            "Deposits in transit", "Outstanding checks", "Allowance for credit losses", "Sales revenue", "Petty cash"],
           [line("Cash", debit=net_book), line("Bank service charge expense", debit=fees), line("Accounts payable", debit=check_error),
            line("Accounts receivable", credit=ar_net), line("Interest revenue", credit=INTEREST)],
           f"Only items the bank recorded first need entries on Hollis's books: the ACH collection (Cash and Accounts receivable, {d(ACH)}), the interest ({d(INTEREST)}), the NSF check, which reinstates the receivable ({d(NSF)}), the wire fee and service charge ({d(fees)}), and check 873, recorded at $460 instead of $640, which understates the payment to Lark Paper by {d(check_error)}. Net, Cash increases {d(net_book)} and Accounts receivable decreases {d(ar_net)}. Deposits in transit, outstanding checks and the bank's error need no entry by Hollis; the bank corrects its own error.",
           points=3),
    ],
)

# ── Simulation 3: income tax provision ────────────────────────────────────
PRETAX, MUNI, FINE = 900000, 20000, 15000
BOOK_DEP, TAX_DEP, WARR_EXP, WARR_PAID = 90000, 150000, 55000, 35000
RENT_CASH, RENT_EARNED = 36000, 3000
EST_PAID = 150000
R_NOW, R_FUT = Decimal("0.21"), Decimal("0.25")
BEG_DEP_DIFF, BEG_WARR = 60000, 40000
beg_dtl, beg_dta = usd(BEG_DEP_DIFF * R_NOW), usd(BEG_WARR * R_NOW)
dep_diff = BEG_DEP_DIFF + TAX_DEP - BOOK_DEP
warr_liab = BEG_WARR + WARR_EXP - WARR_PAID
unearned = RENT_CASH - RENT_EARNED
taxable = PRETAX - MUNI + FINE - (TAX_DEP - BOOK_DEP) + (WARR_EXP - WARR_PAID) + unearned
current = usd(taxable * R_NOW)
end_dtl = usd(dep_diff * R_FUT)
end_dta = usd((warr_liab + unearned) * R_FUT)
deferred = (end_dtl - beg_dtl) - (end_dta - beg_dta)
total = current + deferred
payable = current - EST_PAID
net_dtl = end_dtl - end_dta
assert deferred > 0 and payable > 0 and net_dtl > 0

SIM3 = tbs(
    "far-tbs-income-tax-provision-0002", A3, "Accounting for income taxes", "Application",
    ["ASC 740-10 (current and deferred taxes; temporary and permanent differences; enacted rates)",
     "ASC 740-10-45 (balance sheet presentation of deferred taxes)"],
    "Year 2 income tax provision",
    f"""Keane Corp. is preparing its Year 2 income tax provision. Its pretax financial income for Year 2 is {d(PRETAX)}. The enacted income tax rate is 21% for Year 2; legislation enacted in November, Year 2, sets the rate at 25% for Year 3 and all later years, when all of Keane's temporary differences will reverse. There are no state taxes, and Keane files in one jurisdiction. Keane has reported taxable income in every year since it was formed, and its signed sales backlog supports projected pretax income of about $700,000 a year for Years 3 through 5. During Year 2 Keane paid {d(EST_PAID)} of estimated taxes, which it recorded as debits to Prepaid income taxes. Round every amount to the nearest dollar.""",
    [("Exhibit 1: Deferred tax balances at January 1, Year 2", f"""
| Account | Balance | Source |
|---|---|---|
| Deferred tax liability | {d(beg_dtl)} | Cumulative tax depreciation in excess of book depreciation, {d(BEG_DEP_DIFF)} |
| Deferred tax asset | {d(beg_dta)} | Warranty liability, {d(BEG_WARR)} |
"""),
     ("Exhibit 2: Controller's notes on Year 2 book and tax amounts", f"""
| Item | Detail |
|---|---|
| Depreciation | Book {d(BOOK_DEP)}; tax {d(TAX_DEP)} |
| Warranties | Expense accrued for books {d(WARR_EXP)}; claims paid in cash {d(WARR_PAID)}. Warranty costs are deductible for tax when paid. |
| Rent | On December 1, Year 2, a tenant paid {d(RENT_CASH)} for 12 months' rent on unused warehouse space. Keane recognized {d(RENT_EARNED)} as Year 2 rent revenue; the full amount is taxable in Year 2. |
| Municipal bonds | Interest income of {d(MUNI)} is included in pretax income and is exempt from tax. |
| Fine | A {d(FINE)} penalty paid to a state environmental agency is included in expenses and is not deductible. |
| Equipment sale | A $12,000 gain on equipment sold in March is included in pretax income and is taxable in Year 2. |
| Dividends | Keane declared and paid $80,000 of cash dividends in Year 2. |
""")],
    [
        num("t1", "What is Keane's taxable income for Year 2?", taxable,
            f"{d(PRETAX)} − {d(MUNI)} municipal interest + {d(FINE)} fine − {d(TAX_DEP - BOOK_DEP)} excess tax depreciation + {d(WARR_EXP - WARR_PAID)} warranty accrual in excess of payments + {d(unearned)} rent taxed before it is earned = {d(taxable)}. The equipment gain is in both, and dividends affect neither."),
        num("t2", "What deferred tax asset should Keane report at December 31, Year 2, before any offsetting?", end_dta,
            f"Deductible temporary differences: warranty liability {d(BEG_WARR)} + {d(WARR_EXP)} − {d(WARR_PAID)} = {d(warr_liab)}, and unearned rent {d(RENT_CASH)} − {d(RENT_EARNED)} = {d(unearned)}; total {d(warr_liab + unearned)} × 25% enacted future rate = {d(end_dta)}. No valuation allowance is needed: Keane's history of taxable income and its backlog are positive evidence, and the taxable depreciation difference also reverses in future years."),
        num("t3", "What deferred tax liability should Keane report at December 31, Year 2, before any offsetting?", end_dtl,
            f"Cumulative excess tax depreciation {d(BEG_DEP_DIFF)} + {d(TAX_DEP - BOOK_DEP)} = {d(dep_diff)} × 25% = {d(end_dtl)}. Deferred balances are measured at the enacted rate for the years they reverse."),
        je("t4", "Prepare Keane's journal entry to record its Year 2 income tax provision, applying the estimated payments recorded in Prepaid income taxes. Keane keeps separate deferred tax asset and deferred tax liability accounts.",
           ["Income tax expense — current", "Income tax expense — deferred", "Income taxes payable", "Prepaid income taxes",
            "Deferred tax asset", "Deferred tax liability", "Valuation allowance", "Unearned rent revenue", "Retained earnings"],
           [line("Income tax expense — current", debit=current), line("Income tax expense — deferred", debit=deferred),
            line("Deferred tax asset", debit=end_dta - beg_dta), line("Prepaid income taxes", credit=EST_PAID),
            line("Income taxes payable", credit=payable), line("Deferred tax liability", credit=end_dtl - beg_dtl)],
           f"Current tax = {d(taxable)} × 21% = {d(current)}; {d(EST_PAID)} was prepaid, so {d(payable)} is payable. The deferred tax liability rises from {d(beg_dtl)} to {d(end_dtl)} ({d(end_dtl - beg_dtl)}), and the deferred tax asset from {d(beg_dta)} to {d(end_dta)} ({d(end_dta - beg_dta)}). Deferred tax expense = {d(end_dtl - beg_dtl)} − {d(end_dta - beg_dta)} = {d(deferred)}, which includes the effect of the rate change on the opening balances.",
           points=3),
        num("t5", "What total income tax expense should Keane report for Year 2?", total,
            f"{d(current)} current + {d(deferred)} deferred = {d(total)}."),
        num("t6", "Keane presents its deferred tax asset and liability as one net amount. What net deferred tax amount should Keane report on its December 31, Year 2, balance sheet? Enter a net liability as a positive amount and a net asset as a negative amount.", net_dtl,
            f"{d(end_dtl)} deferred tax liability − {d(end_dta)} deferred tax asset = {d(net_dtl)}, a net liability. Deferred tax balances of one tax-paying component in one jurisdiction are offset and presented as noncurrent."),
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
    print("lease", F_ANN, F_ONE, liability, rou, interest1, principal1, ending1, current2, amort1, rou - amort1)
    print("bank", book_end, bank_end, dit, os_checks, adj_bank, net_book, ar_net)
    print("tax", taxable, current, beg_dtl, beg_dta, end_dtl, end_dta, deferred, total, payable, net_dtl)
