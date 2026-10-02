"""FAR simulations batch 02 — six Area I simulations (docs/plans/far-simulations.md). See docs/reviews/far-tbs-02.md.

Every simulation has at least two source-style exhibits with data to reject, 7-9 points, a stated rounding rule and
one key line per account. Every number is computed here (Decimal, rounded half up) and stored in cents; the script
asserts that each set of statements ties before writing anything.

Run: python3 scripts/batches/far-tbs-02.py  (writes content/far/far-tbs-*.yaml for this batch)
"""
import os
from decimal import Decimal, ROUND_HALF_UP

import yaml

A1 = "Area I — Financial Reporting"
NOTE = "FAR simulations batch 02. Written from scratch; every number computed in code."


def c(dollars):
    """Dollars (int or Decimal) to whole cents."""
    return int((Decimal(dollars) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def cents2(x):
    """Round to the nearest cent, half up."""
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def d(x):
    """$1,234 or ($1,234) for negatives."""
    return f"(${-x:,})" if x < 0 else f"${x:,}"


def num(id, prompt, dollars, explanation, points=1, tolerance=100):
    """A currency task: the key in cents, accepting answers within $1 unless told otherwise."""
    return dict(id=id, type="numeric", points=points, unit="cents", tolerance=tolerance, prompt=prompt,
                answer=c(dollars), explanation=explanation)


def units(id, prompt, n, explanation, points=1):
    return dict(id=id, type="numeric", points=points, unit="units", tolerance=0, prompt=prompt, answer=n,
                explanation=explanation)


def select(id, prompt, options, rows, explanation, points):
    """rows: (row id, label, answer)."""
    for _, _, a in rows:
        assert a in options, a
    return dict(id=id, type="select", points=points, prompt=prompt, options=options,
                rows=[dict(id=i, label=l, answer=a) for i, l, a in rows], explanation=explanation)


def table(header, rows):
    out = "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n"
    return out + "\n".join("| " + " | ".join(str(x) for x in r) + " |" for r in rows)


def amt(x):
    """Statement-style amount: 1,234 or (1,234)."""
    return f"({-x:,})" if x < 0 else f"{x:,}"


def tbs(id, topic, skill, refs, title, scenario, exhibits, tasks):
    return dict(
        id=id, type="tbs",
        blueprint=dict(section="FAR", area=A1, topic=topic, skill=skill),
        review=dict(status="reviewed", references=refs, notes=NOTE),
        title=title, scenario=scenario.strip(),
        exhibits=[dict(title=t, body=b.strip()) for t, b in exhibits],
        tasks=tasks,
    )


# ── Simulation 1: statement of cash flows, indirect method (I.A.5a, Application) ─────────────────────────────
SALES, COGS, DEP, OPEX, INT_EXP, DISC_AMORT, TAX = 2450000, 1470000, 96000, 512000, 41000, 3000, 88000
SOLD_COST, SOLD_AD, SOLD_PROCEEDS = 150000, 104000, 60000
gain = SOLD_PROCEEDS - (SOLD_COST - SOLD_AD)
ni = SALES - COGS - DEP - OPEX - INT_EXP + gain - TAX
NOTE_EQUIP, NOTE_PAID, CASH_EQUIP = 120000, 20000, 210000
STOCK_DIV_SH, STOCK_DIV_PRICE = 20000, 14            # 10% of 200,000 shares, market price $14
ISSUE_SH, ISSUE_PRICE = 10000, 16
TS_SH, TS_PRICE = 4000, 15
DIV_DECL = 90000
y1 = dict(cash=84000, ar=212000, inv=305000, prepaid=18000, land=450000, equip=900000, ad=310000,
          ap=164000, intpay=6000, taxpay=27000, divpay=20000, note=0, bonds=470000, cs=200000, re=512000, ts=0)
assets1 = y1["cash"] + y1["ar"] + y1["inv"] + y1["prepaid"] + y1["land"] + y1["equip"] - y1["ad"]
y1["apic"] = assets1 - (y1["ap"] + y1["intpay"] + y1["taxpay"] + y1["divpay"] + y1["note"] + y1["bonds"] + y1["cs"] + y1["re"])
y2 = dict(ar=248000, inv=281000, prepaid=22000, land=450000, ap=151000, intpay=9000, taxpay=33000, divpay=25000)
y2["equip"] = y1["equip"] - SOLD_COST + NOTE_EQUIP + CASH_EQUIP
y2["ad"] = y1["ad"] - SOLD_AD + DEP
y2["note"] = NOTE_EQUIP - NOTE_PAID
y2["bonds"] = y1["bonds"] + DISC_AMORT
y2["cs"] = y1["cs"] + STOCK_DIV_SH + ISSUE_SH
y2["apic"] = y1["apic"] + STOCK_DIV_SH * (STOCK_DIV_PRICE - 1) + ISSUE_SH * (ISSUE_PRICE - 1)
y2["re"] = y1["re"] + ni - DIV_DECL - STOCK_DIV_SH * STOCK_DIV_PRICE
y2["ts"] = TS_SH * TS_PRICE
div_paid = y1["divpay"] + DIV_DECL - y2["divpay"]
cfo = (ni + DEP - gain + DISC_AMORT - (y2["ar"] - y1["ar"]) - (y2["inv"] - y1["inv"]) - (y2["prepaid"] - y1["prepaid"])
       + (y2["ap"] - y1["ap"]) + (y2["intpay"] - y1["intpay"]) + (y2["taxpay"] - y1["taxpay"]))
cfi = SOLD_PROCEEDS - CASH_EQUIP
cff = ISSUE_SH * ISSUE_PRICE - y2["ts"] - div_paid - NOTE_PAID
y2["cash"] = y1["cash"] + cfo + cfi + cff
assets2 = y2["cash"] + y2["ar"] + y2["inv"] + y2["prepaid"] + y2["land"] + y2["equip"] - y2["ad"]
le2 = (y2["ap"] + y2["intpay"] + y2["taxpay"] + y2["divpay"] + y2["note"] + y2["bonds"] + y2["cs"] + y2["apic"]
       + y2["re"] - y2["ts"])
assert assets2 == le2, (assets2, le2)
int_paid = INT_EXP - DISC_AMORT - (y2["intpay"] - y1["intpay"])
tax_paid = TAX - (y2["taxpay"] - y1["taxpay"])
# Error values a candidate could reach, for the explanations
cfo_no_amort = cfo - DISC_AMORT

BS_ROWS = [
    ("Cash", "cash", 1), ("Accounts receivable, net", "ar", 1), ("Inventory", "inv", 1), ("Prepaid expenses", "prepaid", 1),
    ("Land", "land", 1), ("Equipment", "equip", 1), ("Accumulated depreciation", "ad", -1),
]
LE_ROWS = [
    ("Accounts payable", "ap", 1), ("Interest payable", "intpay", 1), ("Income taxes payable", "taxpay", 1),
    ("Dividends payable", "divpay", 1), ("Note payable — equipment", "note", 1), ("Bonds payable, net of discount", "bonds", 1),
    ("Common stock, $1 par", "cs", 1), ("Additional paid-in capital", "apic", 1), ("Retained earnings", "re", 1),
    ("Treasury stock, at cost", "ts", -1),
]
bs_body = table(["", "December 31, Year 2", "December 31, Year 1"],
                [(n, amt(s * y2[k]), amt(s * y1[k])) for n, k, s in BS_ROWS]
                + [("**Total assets**", amt(assets2), amt(assets1))]
                + [(n, amt(s * y2[k]), amt(s * y1[k])) for n, k, s in LE_ROWS]
                + [("**Total liabilities and equity**", amt(le2), amt(assets1))])
is_body = table(["", "Year 2"], [
    ("Sales", amt(SALES)), ("Cost of goods sold", amt(-COGS)), ("Depreciation expense", amt(-DEP)),
    ("Other operating expenses", amt(-OPEX)), ("Interest expense", amt(-INT_EXP)), ("Gain on sale of equipment", amt(gain)),
    ("Income tax expense", amt(-TAX)), ("**Net income**", amt(ni)),
])
SIM1 = tbs(
    "far-tbs-cash-flows-0001", "Statement of cash flows", "Application",
    ["ASC 230-10 (classification of cash receipts and payments; indirect method; noncash investing and financing activities; disclosure of interest and income taxes paid)"],
    "Year 2 statement of cash flows",
    """Brennick Corp. prepares its statement of cash flows using the indirect method. Use the comparative balance sheets, the Year 2 income statement and the controller's notes in the exhibits. Brennick has no cash equivalents and no deferred taxes. Enter every amount in whole dollars, and enter a net cash outflow as a negative number.""",
    [("Exhibit 1: Comparative balance sheets", bs_body),
     ("Exhibit 2: Income statement for Year 2", is_body),
     ("Exhibit 3: Controller's notes on Year 2 transactions", f"""
| Date | Note |
|---|---|
| February 10 | Sold equipment that had cost {d(SOLD_COST)} and had accumulated depreciation of {d(SOLD_AD)}, for {d(SOLD_PROCEEDS)} cash. |
| March 1 | Acquired a packaging machine by signing a {d(NOTE_EQUIP)} three-year, 6% note payable to the seller, with interest paid each December 31 and included in interest expense. A {d(NOTE_PAID)} principal payment on the note was made on December 31. |
| May 15 | Declared and distributed a 10% stock dividend on the 200,000 shares then outstanding, when the market price was ${STOCK_DIV_PRICE} per share. |
| June 30 | Issued {ISSUE_SH:,} shares of common stock for cash at ${ISSUE_PRICE} per share. |
| August 12 | Bought equipment for {d(CASH_EQUIP)} cash. |
| October 5 | Repurchased {TS_SH:,} shares of its own common stock at ${TS_PRICE} per share, to be held as treasury stock. |
| Year 2 | Declared cash dividends of {d(DIV_DECL)} during the year. Interest expense includes {d(DISC_AMORT)} of bond discount amortization. No bonds were issued or retired. |
""")],
    [
        num("t1", "What is Brennick's net cash provided by (used in) operating activities for Year 2?", cfo,
            f"Net income {d(ni)} + depreciation {d(DEP)} − gain on sale {d(gain)} + bond discount amortization {d(DISC_AMORT)} − increase in receivables {d(y2['ar'] - y1['ar'])} + decrease in inventory {d(y1['inv'] - y2['inv'])} − increase in prepaid expenses {d(y2['prepaid'] - y1['prepaid'])} − decrease in accounts payable {d(y1['ap'] - y2['ap'])} + increase in interest payable {d(y2['intpay'] - y1['intpay'])} + increase in income taxes payable {d(y2['taxpay'] - y1['taxpay'])} = {d(cfo)}. The discount amortization is interest expense that used no cash (leaving it out gives {d(cfo_no_amort)}). The dividends payable change belongs with financing, and the stock dividend and the note-financed machine involve no cash.",
            points=2),
        num("t2", "What is Brennick's net cash provided by (used in) investing activities for Year 2?", cfi,
            f"Proceeds from the equipment sale {d(SOLD_PROCEEDS)} − cash purchase of equipment {d(CASH_EQUIP)} = {d(cfi)}. The {d(NOTE_EQUIP)} machine was acquired with a note, so it is a noncash investing and financing activity, disclosed rather than reported as an outflow. The equipment account reconciles: {d(y1['equip'])} − {d(SOLD_COST)} + {d(NOTE_EQUIP)} + {d(CASH_EQUIP)} = {d(y2['equip'])}."),
        num("t3", "What is Brennick's net cash provided by (used in) financing activities for Year 2?", cff,
            f"Stock issued {d(ISSUE_SH * ISSUE_PRICE)} − treasury stock {d(y2['ts'])} − dividends paid {d(div_paid)} − note principal {d(NOTE_PAID)} = {d(cff)}. Dividends paid = {d(y1['divpay'])} opening payable + {d(DIV_DECL)} declared − {d(y2['divpay'])} closing payable = {d(div_paid)}. The stock dividend moved {d(STOCK_DIV_SH * STOCK_DIV_PRICE)} from retained earnings to paid-in capital and used no cash."),
        num("t4", "What amount of interest paid should Brennick disclose for Year 2?", int_paid,
            f"Interest expense {d(INT_EXP)} − discount amortization {d(DISC_AMORT)} − increase in interest payable {d(y2['intpay'] - y1['intpay'])} = {d(int_paid)}."),
        num("t5", "What amount of income taxes paid should Brennick disclose for Year 2?", tax_paid,
            f"Income tax expense {d(TAX)} − increase in income taxes payable {d(y2['taxpay'] - y1['taxpay'])} = {d(tax_paid)}. Brennick has no deferred taxes."),
        select("t6", "Indicate how Brennick should report each Year 2 event in its statement of cash flows or the related disclosures.",
               ["Operating activities", "Investing activities", "Financing activities",
                "Noncash investing and financing disclosure", "Not reported"],
               [("r1", "Proceeds from the February 10 equipment sale", "Investing activities"),
                ("r2", "Acquisition of the packaging machine on March 1", "Noncash investing and financing disclosure"),
                ("r3", "December 31 payment on the equipment note", "Financing activities"),
                ("r4", "Repurchase of shares on October 5", "Financing activities"),
                ("r5", "Interest paid on the bonds", "Operating activities")],
               "The sale proceeds are investing. The machine bought with a note involves no cash at acquisition, so it is disclosed as a noncash investing and financing activity, and the later principal payment on the note is a financing outflow. Buying treasury stock is a financing outflow. Under U.S. GAAP, interest paid is an operating cash flow, even on debt whose principal is a financing item.",
               points=2),
    ],
)

# ── Simulation 2: wholly owned consolidation, detect and correct (I.A.6c, Analysis) ───────────────────────────
PRICE, S_EQ_ACQ, S_CS_ACQ, S_RE_ACQ = 1500000, 1200000, 700000, 500000
STEP_UP, LIFE = 200000, 10
goodwill = PRICE - S_EQ_ACQ - STEP_UP
extra_dep = STEP_UP // LIFE
YEARS = 3
IC_SALES, GM = 400000, Decimal("0.20")
END_HELD, BEG_HELD = 100000, 60000
end_up, beg_up = int(END_HELD * GM), int(BEG_HELD * GM)
LOAN, LOAN_RATE = 250000, Decimal("0.06")
loan_int = int(LOAN * LOAN_RATE)
S_EXT_NOTE, S_EXT_RATE, P_NOTE, P_RATE = 180000, Decimal("0.08"), 300000, Decimal("0.07")
S_DIV = 80000
P = dict(sales=3200000, cogs=1920000, dep=150000, opex=610000, int_inc=loan_int, div_inc=S_DIV, int_exp=int(P_NOTE * P_RATE))
S = dict(sales=1400000, cogs=840000, dep=90000, opex=260000, int_inc=0, div_inc=0, int_exp=loan_int + int(S_EXT_NOTE * S_EXT_RATE))


def ni_of(x):
    return x["sales"] - x["cogs"] - x["dep"] - x["opex"] + x["int_inc"] + x["div_inc"] - x["int_exp"]


P["ni"], S["ni"] = ni_of(P), ni_of(S)
P_BS = dict(inv=410000, note_rec=LOAN, invest=PRICE, equip=1300000, goodwill=0, notes_pay=P_NOTE, re=2900000)
S_BS = dict(inv=260000, note_rec=0, invest=0, equip=700000, goodwill=0, notes_pay=LOAN + S_EXT_NOTE, re=820000)
cor = dict(sales=P["sales"] + S["sales"] - IC_SALES,
           cogs=P["cogs"] + S["cogs"] - IC_SALES + end_up - beg_up,
           dep=P["dep"] + S["dep"] + extra_dep, opex=P["opex"] + S["opex"], int_inc=0, div_inc=0,
           int_exp=P["int_exp"] + S["int_exp"] - loan_int)
cor["ni"] = ni_of(cor)
assert cor["ni"] == P["ni"] - S_DIV + S["ni"] - extra_dep - end_up + beg_up
cor_bs = dict(inv=P_BS["inv"] + S_BS["inv"] - end_up, note_rec=0, invest=0,
              equip=P_BS["equip"] + S_BS["equip"] + STEP_UP - extra_dep * YEARS, goodwill=goodwill,
              notes_pay=P_BS["notes_pay"] + S_BS["notes_pay"] - LOAN,
              re=P_BS["re"] + (S_BS["re"] - S_RE_ACQ) - extra_dep * YEARS - end_up)
# The staff accountant's draft: eliminated the intra-entity sales (not the profit in inventory), the interest and the
# receivable, but not the dividend, the payable, or the step-up depreciation; added Strand's whole retained earnings.
draft = dict(sales=cor["sales"], cogs=P["cogs"] + S["cogs"] - IC_SALES, dep=P["dep"] + S["dep"], opex=cor["opex"],
             int_inc=0, div_inc=S_DIV, int_exp=cor["int_exp"])
draft["ni"] = ni_of(draft)
draft_bs = dict(inv=P_BS["inv"] + S_BS["inv"], note_rec=0, invest=0, equip=P_BS["equip"] + S_BS["equip"] + STEP_UP,
                goodwill=goodwill, notes_pay=P_BS["notes_pay"] + S_BS["notes_pay"], re=P_BS["re"] + S_BS["re"])
S_RE_BEG3 = S_BS["re"] - S["ni"] + S_DIV
assert S_RE_BEG3 > S_RE_ACQ

IS_LINES = [("Sales", "sales", 1), ("Cost of goods sold", "cogs", -1), ("Depreciation expense", "dep", -1),
            ("Other operating expenses", "opex", -1), ("Interest income", "int_inc", 1), ("Dividend income", "div_inc", 1),
            ("Interest expense", "int_exp", -1), ("**Net income**", "ni", 1)]
BS_LINES = [("Inventory", "inv"), ("Note receivable", "note_rec"), ("Investment in Strand", "invest"),
            ("Equipment, net", "equip"), ("Goodwill", "goodwill"), ("Notes payable", "notes_pay"), ("Retained earnings", "re")]
sep_body = ("Income statements for Year 3:\n\n"
            + table(["", "Pomeroy", "Strand"], [(n, amt(s * P[k]), amt(s * S[k])) for n, k, s in IS_LINES])
            + "\n\nSelected balances at December 31, Year 3:\n\n"
            + table(["", "Pomeroy", "Strand"], [(n, amt(P_BS[k]), amt(S_BS[k])) for n, k in BS_LINES if k != "goodwill"]))
draft_body = ("Consolidated income statement for Year 3 (draft):\n\n"
              + table(["", "Consolidated"], [(n, amt(s * draft[k])) for n, k, s in IS_LINES if k != "int_inc"])
              + "\n\nSelected consolidated balances at December 31, Year 3 (draft):\n\n"
              + table(["", "Consolidated"], [(n, amt(draft_bs[k])) for n, k in BS_LINES if k != "invest"]))
SEL = ["Correct as drafted", "Overstated", "Understated"]


def verdict(k, a, b):
    return SEL[0] if a[k] == b[k] else (SEL[1] if a[k] > b[k] else SEL[2])


rows2 = [("sales", "Sales", draft, cor), ("cogs", "Cost of goods sold", draft, cor), ("dep", "Depreciation expense", draft, cor),
         ("int_exp", "Interest expense", draft, cor), ("div_inc", "Dividend income", draft, cor),
         ("inv", "Inventory", draft_bs, cor_bs), ("equip", "Equipment, net", draft_bs, cor_bs),
         ("goodwill", "Goodwill", draft_bs, cor_bs), ("note_rec", "Note receivable", draft_bs, cor_bs), ("notes_pay", "Notes payable", draft_bs, cor_bs),
         ("re", "Retained earnings", draft_bs, cor_bs)]
sel2 = [(k, label, verdict(k, a, b)) for k, label, a, b in rows2]
assert {a for *_, a in sel2} == set(SEL)
SIM2 = tbs(
    "far-tbs-consolidation-review-0001", "Consolidated financial statements", "Analysis",
    ["ASC 810-10 (consolidation procedures: intra-entity balances, transactions and profits)",
     "ASC 805-20 (acquisition-date fair values; subsequent amortization of the step-up through depreciation)"],
    "Reviewing a draft consolidation",
    """Pomeroy Inc., a public business entity, owns 100% of Strand Co. A staff accountant has prepared a draft of Pomeroy's Year 3 consolidated statements. You are reviewing it before the controller signs off. Pomeroy accounts for its investment in Strand at cost in its own books. Ignore income taxes, and enter every amount in whole dollars.""",
    [("Exhibit 1: Separate financial statements of Pomeroy and Strand", sep_body),
     ("Exhibit 2: Draft consolidated statements prepared by the staff accountant", draft_body),
     ("Exhibit 3: Consolidation file notes", f"""
| Topic | Note |
|---|---|
| Acquisition | Pomeroy bought all of Strand's stock on January 1, Year 1, for {d(PRICE)} cash. Strand's book equity then was {d(S_EQ_ACQ)} (common stock and paid-in capital {d(S_CS_ACQ)}, retained earnings {d(S_RE_ACQ)}). Book values equaled fair values except Strand's equipment, whose fair value was {d(STEP_UP)} above book value; the equipment then had a {LIFE}-year remaining life with no residual value, is depreciated straight-line and is still in use. Any remaining excess is goodwill, which has not been impaired. |
| Appraisal | An appraisal commissioned in December, Year 3, values Strand's equipment at $950,000 and Strand as a whole at $2,100,000. |
| Merchandise | Strand sells goods to Pomeroy at a {int(GM * 100)}% gross margin on the selling price. Strand's Year 3 sales to Pomeroy were {d(IC_SALES)}. Pomeroy's inventory included goods bought from Strand of {d(BEG_HELD)} at January 1, Year 3, and {d(END_HELD)} at December 31, Year 3, at Pomeroy's cost. Pomeroy sold the January 1 goods to outside customers in Year 3. |
| Loan | On January 1, Year 3, Pomeroy lent Strand {d(LOAN)} at {int(LOAN_RATE * 100)}%, interest paid each December 31. The rest of Strand's notes payable is owed to its bank. |
| Dividends | Strand declared and paid {d(S_DIV)} of dividends in Year 3, all to Pomeroy. |
""")],
    [
        select("t1", "For each line of the draft consolidated statements in Exhibit 2, indicate whether the draft amount is correct, overstated or understated.",
               SEL, sel2,
               f"Sales: the {d(IC_SALES)} of intra-entity sales were eliminated, so the draft is correct. Cost of goods sold: the draft eliminated {d(IC_SALES)} but not the profit in inventory; it must add the {d(end_up)} unrealized at year end and remove the {d(beg_up)} from January 1 that was realized in Year 3, so the draft is understated by {d(cor['cogs'] - draft['cogs'])}. Depreciation: the {d(extra_dep)} a year on the equipment step-up is missing (understated). Interest expense: only the {d(loan_int)} on the intra-entity loan was eliminated, which is correct. Dividend income: the {d(S_DIV)} from Strand is intra-entity and must be eliminated (overstated). Inventory includes {d(end_up)} of unrealized profit (overstated). Equipment includes the full {d(STEP_UP)} step-up with none of the {d(extra_dep * YEARS)} of depreciation for Years 1–3 (overstated). Goodwill = {d(PRICE)} − {d(S_EQ_ACQ)} − {d(STEP_UP)} = {d(goodwill)}, correct (a public business entity can't elect to amortize goodwill). The note receivable from Strand was eliminated, which is correct. Notes payable still includes the {d(LOAN)} owed to Pomeroy (overstated). Retained earnings added all of Strand's retained earnings, including the {d(S_RE_ACQ)} earned before the acquisition (overstated).",
               points=3),
        num("t2", "What amount should Pomeroy report as consolidated cost of goods sold for Year 3?", cor["cogs"],
            f"{d(P['cogs'])} + {d(S['cogs'])} − {d(IC_SALES)} intra-entity sales + {d(end_up)} unrealized profit in ending inventory ({d(END_HELD)} × {int(GM * 100)}%) − {d(beg_up)} profit in beginning inventory realized this year ({d(BEG_HELD)} × {int(GM * 100)}%) = {d(cor['cogs'])}."),
        num("t3", "What amount should Pomeroy report as consolidated net income for Year 3?", cor["ni"],
            f"Pomeroy {d(P['ni'])} − {d(S_DIV)} dividend from Strand + Strand {d(S['ni'])} − {d(extra_dep)} step-up depreciation − {d(end_up)} ending unrealized profit + {d(beg_up)} beginning profit realized = {d(cor['ni'])}. The intra-entity interest ({d(loan_int)}) is income to Pomeroy and expense to Strand, so eliminating it doesn't change net income.",
            points=2),
        num("t4", "What amount should Pomeroy report as consolidated equipment, net, at December 31, Year 3?", cor_bs["equip"],
            f"{d(P_BS['equip'])} + {d(S_BS['equip'])} + {d(STEP_UP)} step-up − {d(extra_dep * YEARS)} accumulated step-up depreciation ({d(extra_dep)} × {YEARS} years) = {d(cor_bs['equip'])}. The December appraisal is not recorded; equipment stays at cost less depreciation."),
        num("t5", "What amount should Pomeroy report as consolidated retained earnings at December 31, Year 3?", cor_bs["re"],
            f"Pomeroy's retained earnings {d(P_BS['re'])} (which already include the dividends it received from Strand) + Strand's growth in retained earnings since the acquisition, {d(S_BS['re'])} − {d(S_RE_ACQ)} = {d(S_BS['re'] - S_RE_ACQ)}, − {d(extra_dep * YEARS)} step-up depreciation for Years 1–3 − {d(end_up)} unrealized profit in ending inventory = {d(cor_bs['re'])}. The profit in the January 1 inventory was realized in Year 3 and no longer affects retained earnings.",
            points=2),
    ],
)

# ── Simulation 3: classified balance sheet, detect and correct (I.A.1c, Analysis) ─────────────────────────────
CHECKING, PETTY, TBILL, CD = 92000, 1000, 40000, 53000
AR_DEBIT, AR_CREDIT, ALLOW = 335000, 7000, 10000
INV_DRAFT, CONSIGNED, IN_TRANSIT = 412000, 36000, 18000
PREPAID, SINKING, TS_COST = 24000, 75000, 45000
PPE = 1240000
AP, ACCRUED, TERM_LOAN, INSTALLMENT, BONDS = 205000, 38000, 400000, 80000, 500000
PAR, ISSUED, TS_SHARES, DPS = 5, 64000, 4000, Decimal("0.50")
APIC3 = 410000
outstanding = ISSUED - TS_SHARES
div_payable = int(outstanding * DPS)
div_on_issued = int(ISSUED * DPS)
dr_cash = CHECKING + PETTY + TBILL + CD
dr_ar = AR_DEBIT - AR_CREDIT - ALLOW
dr_ca = dr_cash + dr_ar + INV_DRAFT + PREPAID + SINKING + TS_COST
dr_cl = AP + ACCRUED
dr_ncl = TERM_LOAN + BONDS
dr_total_assets = dr_ca + PPE
dr_re = dr_total_assets - dr_cl - dr_ncl - ISSUED * PAR - APIC3
cr_cash = CHECKING + PETTY + TBILL
cr_ar = AR_DEBIT - ALLOW
cr_inv = INV_DRAFT - CONSIGNED + IN_TRANSIT
cr_ca = cr_cash + CD + cr_ar + cr_inv + PREPAID
cr_cl = AP + ACCRUED + AR_CREDIT + div_payable + INSTALLMENT
cr_ncl = TERM_LOAN - INSTALLMENT + BONDS
cr_re = dr_re - div_payable - CONSIGNED + IN_TRANSIT
cr_eq = ISSUED * PAR + APIC3 + cr_re - TS_COST
cr_total_assets = cr_ca + SINKING + PPE
assert cr_total_assets == cr_cl + cr_ncl + cr_eq, (cr_total_assets, cr_cl + cr_ncl + cr_eq)
dr_eq = ISSUED * PAR + APIC3 + dr_re
SIM3 = tbs(
    "far-tbs-balance-sheet-review-0001", "Balance sheet", "Analysis",
    ["ASC 210-10 (current assets and current liabilities)", "ASC 305-10 (cash and cash equivalents)",
     "ASC 505-30 (treasury stock)", "ASC 330-10 (inventory)"],
    "Reviewing a draft balance sheet",
    """Quillon Co.'s bookkeeper has prepared the draft classified balance sheet in Exhibit 1. Quillon has closed its Year 2 books, and the draft reflects every entry recorded. You have pulled the supporting detail in Exhibits 2 and 3. Quillon uses a periodic inventory system and a December 31 count. Quillon's policy treats investments with original maturities of three months or less as cash equivalents. Ignore income taxes, and enter every amount in whole dollars.""",
    [("Exhibit 1: Draft classified balance sheet, December 31, Year 2", table(["", "Amount"], [
        ("Cash and cash equivalents", amt(dr_cash)), ("Accounts receivable, net", amt(dr_ar)), ("Inventory", amt(INV_DRAFT)),
        ("Prepaid expenses", amt(PREPAID)), ("Bond sinking fund", amt(SINKING)), ("Treasury stock", amt(TS_COST)),
        ("**Total current assets**", amt(dr_ca)), ("Property, plant and equipment, net", amt(PPE)),
        ("**Total assets**", amt(dr_total_assets)),
        ("Accounts payable", amt(AP)), ("Accrued liabilities", amt(ACCRUED)), ("**Total current liabilities**", amt(dr_cl)),
        ("Term loan payable", amt(TERM_LOAN)), ("Bonds payable, due Year 10", amt(BONDS)),
        ("**Total noncurrent liabilities**", amt(dr_ncl)),
        (f"Common stock, ${PAR} par, {ISSUED:,} shares issued", amt(ISSUED * PAR)), ("Additional paid-in capital", amt(APIC3)),
        ("Retained earnings", amt(dr_re)), ("**Total stockholders' equity**", amt(dr_eq)),
        ("**Total liabilities and stockholders' equity**", amt(dr_cl + dr_ncl + dr_eq)),
    ])),
     ("Exhibit 2: Detail behind selected balances", f"""
| Balance | Detail |
|---|---|
| Cash and cash equivalents | Checking account {d(CHECKING)}; petty cash {d(PETTY)}; U.S. Treasury bill bought November 20, Year 2, maturing January 31, Year 3, {d(TBILL)}; bank certificate of deposit bought October 1, Year 2, maturing March 31, Year 3, {d(CD)}. |
| Accounts receivable, net | Aged trial balance: customer accounts with debit balances {d(AR_DEBIT)}; two customers who prepaid orders not yet shipped have credit balances totaling {d(AR_CREDIT)}; allowance for credit losses {d(ALLOW)}, per the credit manager's estimate. The draft nets all three. |
| Inventory | Count at December 31: {d(INV_DRAFT)}, including goods costing {d(CONSIGNED)} that Sedley Co. shipped to Quillon on consignment; Quillon sells them for Sedley on commission and recorded no purchase for them. Goods bought from Ames Supply, FOB shipping point, were shipped December 29, Year 2, and arrived January 4, Year 3; Quillon recorded the {d(IN_TRANSIT)} invoice in purchases and accounts payable on December 29, but the goods were not in the count. |
| Prepaid expenses | Insurance premiums for January–June, Year 3, $15,000; rent for January, Year 3, $9,000. |
| Bond sinking fund | Cash and securities held by a trustee, to be used only to retire the ten-year bonds issued January 1, Year 1, and due December 31, Year 10. |
| Accrued liabilities | December wages $26,500; interest on the bonds for the fourth quarter $11,500. |
| Term loan payable | Five-year bank loan taken out on July 1, Year 2; the {d(TERM_LOAN)} balance is repaid in equal installments of {d(INSTALLMENT)} each June 30. Quillon is in compliance with its covenants. |
| Treasury stock | {TS_SHARES:,} shares of Quillon's own common stock bought back in August, Year 2, at cost; market value at December 31 is $49,000. |
"""),
     ("Exhibit 3: Board minutes, December 18, Year 2 (extract)", f"""
| Item | Resolution |
|---|---|
| 4 | Declared a cash dividend of ${DPS} per share on common stock outstanding, payable January 15, Year 3, to holders of record on January 5, Year 3. (Bookkeeper's note: no entry has been made for this dividend.) |
| 5 | Approved a capital budget of $300,000 for Year 3 equipment purchases. |
""")],
    [
        num("t1", "What is the correct amount of cash and cash equivalents at December 31, Year 2?", cr_cash,
            f"Checking {d(CHECKING)} + petty cash {d(PETTY)} + Treasury bill {d(TBILL)} = {d(cr_cash)}. The Treasury bill had an original maturity of about two and a half months, so it is a cash equivalent. The certificate of deposit had a six-month original maturity; it is a short-term investment, still a current asset, even though it matures within three months of year end."),
        num("t2", "What is the correct total of current assets at December 31, Year 2?", cr_ca,
            f"Cash and cash equivalents {d(cr_cash)} + certificate of deposit {d(CD)} + receivables {d(AR_DEBIT)} − {d(ALLOW)} = {d(cr_ar)} (customer credit balances are liabilities, not reductions of receivables) + inventory {d(INV_DRAFT)} − {d(CONSIGNED)} consigned goods Quillon doesn't own + {d(IN_TRANSIT)} goods in transit Quillon owned at year end = {d(cr_inv)} + prepaid expenses {d(PREPAID)} = {d(cr_ca)}. The sinking fund is restricted to retiring long-term debt, so it is noncurrent, and treasury stock is a reduction of equity, not an asset.",
            points=2),
        num("t3", "What is the correct total of current liabilities at December 31, Year 2?", cr_cl,
            f"Accounts payable {d(AP)} + accrued liabilities {d(ACCRUED)} + customer credit balances {d(AR_CREDIT)} + dividends payable {d(div_payable)} ({outstanding:,} outstanding shares × ${DPS}; the dividend became a liability when declared on December 18, and treasury shares receive none) + the term loan installment due June 30, Year 3, {d(INSTALLMENT)} = {d(cr_cl)}. A dividend on all {ISSUED:,} issued shares would give {d(div_on_issued)}.",
            points=2),
        num("t4", "What is the correct retained earnings balance at December 31, Year 2?", cr_re,
            f"Draft {d(dr_re)} − {d(div_payable)} dividend declared but not recorded − {d(CONSIGNED)} consigned goods counted in ending inventory (which understated cost of goods sold) + {d(IN_TRANSIT)} purchased goods left out of the count although the purchase was recorded (which overstated cost of goods sold) = {d(cr_re)}. The reclassifications (certificate of deposit, credit balances, sinking fund, term loan installment) and moving treasury stock out of assets don't change retained earnings.",
            points=2),
        num("t5", "What is the correct total stockholders' equity at December 31, Year 2?", cr_eq,
            f"Common stock {d(ISSUED * PAR)} + additional paid-in capital {d(APIC3)} + retained earnings {d(cr_re)} − treasury stock at cost {d(TS_COST)} = {d(cr_eq)}. Treasury stock is reported at cost; its $49,000 market value is irrelevant. Check: corrected total assets {d(cr_total_assets)} = liabilities {d(cr_cl + cr_ncl)} + equity {d(cr_eq)}."),
    ],
)

# ── Simulation 4: multi-step income statement, detect and correct (I.A.2d, Analysis) ──────────────────────────
TR = Decimal("0.25")
DR = dict(sales=2940000, cogs=1764000, selling=310000, ga=402000, int_inc=9000, afs=22000, seg_loss=90000)
CUTOFF = 40000
SEG = dict(sales=620000, cogs=410000, selling=95000, ga=55000)
SEG_LOSS = DR["seg_loss"]
WH_LOSS, INS, INS_MONTHS_Y2, FREIGHT_IN = 34000, 36000, 3, 30000
ins_prepaid = INS * (12 - INS_MONTHS_Y2) // 12


def tax(x):
    return int((Decimal(x) * TR).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


dr_gp = DR["sales"] - DR["cogs"]
dr_oi = dr_gp - DR["selling"] - DR["ga"]
dr_pretax = dr_oi + DR["int_inc"] + DR["afs"] - DR["seg_loss"]
dr_tax = tax(dr_pretax)
dr_cont = dr_pretax - dr_tax
dr_disc = -(WH_LOSS - tax(WH_LOSS))
dr_ni = dr_cont + dr_disc
c_sales = DR["sales"] - SEG["sales"] - CUTOFF
c_cogs = DR["cogs"] - SEG["cogs"] + FREIGHT_IN
c_gp = c_sales - c_cogs
c_selling = DR["selling"] - SEG["selling"] - FREIGHT_IN
c_ga = DR["ga"] - SEG["ga"] - ins_prepaid
c_oi = c_gp - c_selling - c_ga - WH_LOSS
c_pretax = c_oi + DR["int_inc"]
c_tax = tax(c_pretax)
c_cont = c_pretax - c_tax
seg_pretax = SEG["sales"] - SEG["cogs"] - SEG["selling"] - SEG["ga"] - SEG_LOSS
c_disc = seg_pretax - tax(seg_pretax)
c_ni = c_cont + c_disc
c_oci = DR["afs"] - tax(DR["afs"])
c_tci = c_ni + c_oci
assert c_ni - dr_ni == -(CUTOFF + DR["afs"] - ins_prepaid) + tax(CUTOFF + DR["afs"] - ins_prepaid)
oi_with_wh_outside = c_oi + WH_LOSS
SIM4 = tbs(
    "far-tbs-income-statement-review-0001", "Income statement", "Analysis",
    ["ASC 205-20 (discontinued operations: strategic shift; presentation of results and the disposal loss, net of tax)",
     "ASC 360-10-45-5 (a gain or loss on a long-lived asset that is not a discontinued operation is included in income from continuing operations and, if presented, in income from operations)",
     "ASC 330-10 (freight-in is a cost of inventory)", "ASC 606-10 (timing of revenue recognition)",
     "ASC 320-10 (available-for-sale debt securities: unrealized holding gains and losses in other comprehensive income)"],
    "Reviewing a draft income statement",
    """Varga Co. distributes building products. Its accounting clerk drafted the Year 2 multi-step income statement in Exhibit 1, and the controller's review notes are in Exhibit 2. Varga's income tax rate is 25% on every item, including items of other comprehensive income, and the draft's tax amounts are 25% of the pretax amounts shown. Enter every amount in whole dollars, and enter a loss as a negative number.""",
    [("Exhibit 1: Draft income statement for Year 2", table(["", "Amount"], [
        ("Net sales", amt(DR["sales"])), ("Cost of goods sold", amt(-DR["cogs"])), ("**Gross profit**", amt(dr_gp)),
        ("Selling expenses", amt(-DR["selling"])), ("General and administrative expenses", amt(-DR["ga"])),
        ("**Income from operations**", amt(dr_oi)),
        ("Interest income", amt(DR["int_inc"])), ("Gain on investments", amt(DR["afs"])),
        ("Loss on sale of retail division", amt(-DR["seg_loss"])), ("**Income before income taxes**", amt(dr_pretax)),
        ("Income tax expense", amt(-dr_tax)), ("**Income from continuing operations**", amt(dr_cont)),
        ("Discontinued operations: loss on sale of warehouse, net of tax", amt(dr_disc)), ("**Net income**", amt(dr_ni)),
    ])),
     ("Exhibit 2: Controller's review notes", f"""
| Ref | Note |
|---|---|
| 1 | Varga had two operating segments, wholesale and retail. On September 30, Year 2, it sold the entire retail division (its 14 stores, their staff and their inventory) to a competitor. Since then Varga has operated no stores, and all of its sales are to contractors through the wholesale business. The draft includes the retail division's January 1 – September 30 results in its operating lines: sales {d(SEG['sales'])}, cost of goods sold {d(SEG['cogs'])}, selling expenses {d(SEG['selling'])}, general and administrative expenses {d(SEG['ga'])}. The {d(SEG_LOSS)} loss on the sale is correctly measured. |
| 2 | On November 20, Year 2, Varga sold one of its six wholesale warehouses for a loss of {d(WH_LOSS)} and moved that warehouse's stock to the other five. The amount of the loss is correct. |
| 3 | Invoice 7742 for {d(CUTOFF)}, dated December 30, Year 2, was recorded in net sales. The goods were shipped on January 3, Year 3, under FOB shipping point terms, and were included in Varga's December 31 count, which is correctly reflected in cost of goods sold. |
| 4 | Selling expenses include {d(FREIGHT_IN)} of freight Varga paid on wholesale merchandise bought from suppliers under FOB shipping point terms; all of that merchandise was sold in Year 2. General and administrative expenses include a {d(INS)} premium paid on October 1, Year 2, for a one-year property insurance policy. |
| 5 | "Gain on investments" is the increase in fair value during Year 2 of debt securities that Varga classifies as available for sale. Varga sold none of them. |
| 6 | Interest income is from the same debt securities and is correct. Varga's sales returns and allowances of $26,000 were correctly deducted in arriving at net sales. Varga has no debt. |
""")],
    [
        num("t1", "What is Varga's correct gross profit for Year 2?", c_gp,
            f"Net sales {d(DR['sales'])} − {d(SEG['sales'])} retail division − {d(CUTOFF)} January shipment = {d(c_sales)}; cost of goods sold {d(DR['cogs'])} − {d(SEG['cogs'])} retail + {d(FREIGHT_IN)} freight-in = {d(c_cogs)}; gross profit {d(c_gp)}. The retail division was a component whose sale is a strategic shift (Varga left the retail business entirely), so its results move to discontinued operations. The January 3 shipment is Year 3 revenue under FOB shipping point terms, and its cost already sits in ending inventory. Freight on purchases is a cost of the inventory, and the goods were sold, so it belongs in cost of goods sold."),
        num("t2", "What is Varga's correct income from operations for Year 2?", c_oi,
            f"Gross profit {d(c_gp)} − selling {d(DR['selling'])} − {d(SEG['selling'])} retail − {d(FREIGHT_IN)} freight-in = {d(c_selling)} − general and administrative {d(DR['ga'])} − {d(SEG['ga'])} retail − {d(ins_prepaid)} of insurance for January–September, Year 3, which is a prepaid asset = {d(c_ga)} − {d(WH_LOSS)} loss on the warehouse = {d(c_oi)}. Selling one of six warehouses is not a strategic shift, so the loss stays in continuing operations, and ASC 360-10-45-5 requires a subtotal such as income from operations to include it (leaving it out of operations gives {d(oi_with_wh_outside)}).",
            points=2),
        num("t3", "What is Varga's correct income from continuing operations (after income taxes) for Year 2?", c_cont,
            f"Income from operations {d(c_oi)} + interest income {d(DR['int_inc'])} = {d(c_pretax)} before tax; − 25% tax {d(c_tax)} = {d(c_cont)}. The {d(DR['afs'])} fair value increase on available-for-sale debt securities goes to other comprehensive income, not net income.",
            points=2),
        num("t4", "What amount should Varga report for discontinued operations, net of tax, for Year 2?", c_disc,
            f"Retail division results {d(SEG['sales'])} − {d(SEG['cogs'])} − {d(SEG['selling'])} − {d(SEG['ga'])} = {d(seg_pretax + SEG_LOSS)}, less the {d(SEG_LOSS)} loss on the sale = {d(seg_pretax)} before tax; net of the 25% tax benefit, {d(c_disc)}. The warehouse loss is not a discontinued operation."),
        num("t5", "What is Varga's correct net income for Year 2?", c_ni,
            f"Income from continuing operations {d(c_cont)} + discontinued operations {d(c_disc)} = {d(c_ni)}. Check against the draft's {d(dr_ni)}: only three errors change net income, the {d(CUTOFF)} cutoff error and the {d(DR['afs'])} fair value gain (both overstating it) and the {d(ins_prepaid)} of prepaid insurance (understating it), a net {d(CUTOFF + DR['afs'] - ins_prepaid)} before tax, {d(dr_ni - c_ni)} after tax."),
        num("t6", "What is Varga's correct total comprehensive income for Year 2?", c_tci,
            f"Net income {d(c_ni)} + other comprehensive income {d(c_oci)} (the {d(DR['afs'])} unrealized holding gain on available-for-sale debt securities, less 25% tax of {d(tax(DR['afs']))}) = {d(c_tci)}."),
    ],
)

# ── Simulation 5: NFP statement of activities (I.B.2b, Application) ───────────────────────────────────────────
PATIENT, CASH_GIFTS, PHYS_HOURS, PHYS_RATE, UNSKILLED, INV_GAIN = 1850000, 410000, 600, 75, 18000, 7000
PHYS = PHYS_HOURS * PHYS_RATE
FLU, BUILDING, BUILDING_TAX_VALUE = 30000, 220000, 160000
GRANT, GRANT_SPENT, RUIZ = 80000, 50000, 40000
PLEDGE, COND, ENDOW, ENDOW_RET, BOARD = 60000, 100000, 250000, -6000, 75000
PROGRAM, MG, FR = 1980000, 290000, 85000
released = GRANT_SPENT + RUIZ
expenses = PROGRAM + PHYS + MG + FR
wodr = PATIENT + CASH_GIFTS + FLU + BUILDING + PHYS + INV_GAIN + released - expenses
wdr = PLEDGE + ENDOW + ENDOW_RET - released
released_no_election = released + FLU
assert wodr > 0 and wdr > 0
SIM5 = tbs(
    "far-tbs-nfp-activities-0002", "Statement of activities (Not-for-Profit)", "Application",
    ["ASC 958-605 (contributions: unconditional and conditional promises, contributed services and nonfinancial assets, donor-imposed restrictions, restrictions met in the same period)",
     "ASC 958-205 (net asset classes; releases from restriction; endowment losses)",
     "ASC 958-225 (statement of activities)"],
    "Year 2 statement of activities",
    """Wrenfield Community Clinic is a not-for-profit health clinic preparing its Year 2 statement of activities. As its accounting policy permits, Wrenfield reports donor-restricted contributions whose restrictions are met in the same year they are received as support without donor restrictions. Enter every amount in whole dollars, and enter a decrease as a negative number.""",
    [("Exhibit 1: Development office log of Year 2 gifts", f"""
| Date | Donor | Gift |
|---|---|---|
| Throughout Year 2 | Individuals and businesses | Cash gifts with no donor stipulations, {d(CASH_GIFTS)} |
| February 8 | Pemberton Realty | Title to a building, with no stipulation on its use, which Wrenfield opened as a satellite clinic in May. An independent appraisal put its fair value at {d(BUILDING)}; its assessed value for property tax purposes is {d(BUILDING_TAX_VALUE)}. |
| April 2 | Hollin family | {d(ENDOW)} cash, to be invested permanently, with the investment return used for nursing scholarships |
| June 15 | Larkspur Foundation | Written promise of {d(COND)} for a dental unit, payable only if Wrenfield opens the unit with a licensed dentist on staff by June 30, Year 3; otherwise the foundation owes nothing. Wrenfield has not yet hired a dentist. |
| October 1 | Delacroix family | {d(FLU)} cash for the clinic's flu vaccination drive, all spent on vaccines in October and November |
| December 12 | Okafor Trust | Unconditional written promise of {d(PLEDGE)} for the diabetes education program, payable in March, Year 3; collection is assured, and Wrenfield records it at the promised amount |
| Throughout Year 2 | Volunteer physicians | {PHYS_HOURS} hours of patient care. Contract physicians in the area bill ${PHYS_RATE} an hour for the same work, and Wrenfield would have had to hire them. |
| Throughout Year 2 | Community volunteers | Staffing the reception desk and mailing appeals, valued at {d(UNSKILLED)} at minimum wage |
"""),
     ("Exhibit 2: Controller's schedule of Year 2 activity", f"""
| Item | Detail |
|---|---|
| Patient service revenue | {d(PATIENT)}, net of contractual adjustments |
| Program services expenses | {d(PROGRAM)}, including {d(GRANT_SPENT)} spent on the diabetes education program, the {d(FLU)} of flu vaccines and depreciation, including the satellite clinic's; excludes any donated services |
| Management and general expenses | {d(MG)} |
| Fundraising expenses | {d(FR)} |
| Endowment | The Hollin endowment had a net investment loss of {d(-ENDOW_RET)} in Year 2. The board appropriated nothing from it. |
| Ruiz promise | The Ruiz family's promise (Exhibit 3) was collected in full in July, Year 2. |
| Operating reserve | Investments with no donor restrictions had a net gain of {d(INV_GAIN)}. In December the board set aside {d(BOARD)} of these investments as a fund for future building repairs. |
"""),
     ("Exhibit 3: Net assets with donor restrictions at January 1, Year 2", table(["Item", "Balance", "Source"], [
         ("Diabetes education program", d(GRANT), "Cash grant received in Year 1, restricted to that program"),
         ("Ruiz family promise", d(RUIZ), "Unconditional promise made in Year 1, payable in July, Year 2, with no purpose stated"),
     ]))],
    [
        select("t1", "Indicate whether Wrenfield should recognize each item as revenue, gains or other support in its Year 2 statement of activities, and if so in which net asset class.",
               ["Recognized — without donor restrictions", "Recognized — with donor restrictions", "Not recognized"],
               [("r1", "Larkspur Foundation promise", "Not recognized"),
                ("r2", "Okafor Trust promise", "Recognized — with donor restrictions"),
                ("r3", "Volunteer physicians' services", "Recognized — without donor restrictions"),
                ("r4", "Community volunteers' services", "Not recognized"),
                ("r5", "Hollin family gift", "Recognized — with donor restrictions"),
                ("r6", "Pemberton Realty building", "Recognized — without donor restrictions"),
                ("r7", "Delacroix family gift", "Recognized — without donor restrictions")],
               f"The Larkspur promise depends on a barrier Wrenfield hasn't overcome (opening a staffed dental unit) and the foundation owes nothing if it fails, so it is conditional and not recognized. The Okafor promise is unconditional and restricted to the diabetes program (and payable later), so it is with donor restrictions. The physicians' services need specialized skills Wrenfield would otherwise buy, so they are recognized ({PHYS_HOURS} × ${PHYS_RATE} = {d(PHYS)}) as revenue and as program expense. The reception and mailing work needs no specialized skills and doesn't create or enhance a nonfinancial asset, so it isn't recognized. The Hollin gift must be held in perpetuity, so it is with donor restrictions. The building came with no donor stipulation, so it is support without donor restrictions at its {d(BUILDING)} fair value; GAAP no longer lets an entity imply a time restriction on a gift of a long-lived asset. The Delacroix gift was restricted to the flu drive, but the restriction was met in the year received, so under Wrenfield's policy it is reported without donor restrictions.",
               points=2),
        num("t2", "What is Wrenfield's change in net assets without donor restrictions for Year 2?", wodr,
            f"Patient service revenue {d(PATIENT)} + cash gifts {d(CASH_GIFTS)} + Delacroix gift {d(FLU)} + donated building {d(BUILDING)} + contributed physician services {d(PHYS)} + investment gain {d(INV_GAIN)} + net assets released from restrictions {d(released)} − expenses {d(expenses)} = {d(wodr)}. Expenses = program {d(PROGRAM)} + donated physician services {d(PHYS)} + management and general {d(MG)} + fundraising {d(FR)}. The board's set-aside is an internal designation and leaves the reserve without donor restrictions.",
            points=2),
        num("t3", "What is Wrenfield's change in net assets with donor restrictions for Year 2?", wdr,
            f"Okafor promise {d(PLEDGE)} + Hollin endowment gift {d(ENDOW)} − endowment investment loss {d(-ENDOW_RET)} − net assets released {d(released)} = {d(wdr)}. Losses on a donor-restricted endowment reduce net assets with donor restrictions, even below the original gift.",
            points=2),
        num("t4", "What total amount of net assets released from restrictions should Wrenfield report for Year 2?", released,
            f"Diabetes program spending {d(GRANT_SPENT)} (purpose restriction met) + the Ruiz promise collected in July {d(RUIZ)} (time restriction expired) = {d(released)}. The Delacroix gift never entered net assets with donor restrictions under Wrenfield's same-year policy, so it is not a release (without the policy, releases would be {d(released_no_election)})."),
        num("t5", "What total expenses should Wrenfield report for Year 2?", expenses,
            f"Program services {d(PROGRAM)} + donated physician services {d(PHYS)} + management and general {d(MG)} + fundraising {d(FR)} = {d(expenses)}. The building is capitalized (only its depreciation, already in program expenses, is an expense), and the unrecognized volunteer services create no expense."),
    ],
)

# ── Simulation 6: basic and diluted EPS (I.D.c, Application) ──────────────────────────────────────────────────
NI6, CT = 1250000, Decimal("0.25")
PREF_SH, PREF_PAR, PREF_RATE = 10000, 50, Decimal("0.08")
SH_JAN1, REISSUE_MAY1, SPLIT = 300000, 12000, Decimal("1.5")
BONDS6, COUPON, CONV, CONVERTED = 1500000, Decimal("0.04"), 30, 500000
conv_sh = CONVERTED // 1000 * CONV
remain = BONDS6 - CONVERTED
wa_pre = Decimal(SH_JAN1) + Decimal(REISSUE_MAY1) * 8 / 12 + Decimal(conv_sh) * 4 / 12
wa = wa_pre * SPLIT
assert wa == wa.to_integral_value()
wa = int(wa)
wa_no_split = int(wa_pre)
avail = NI6  # noncumulative preferred, no dividend declared
basic = cents2(Decimal(avail) / wa)
pref_full = int(PREF_SH * PREF_PAR * PREF_RATE)
basic_if_pref = cents2(Decimal(NI6 - pref_full) / wa)
OPT, EX, AVG_PERIOD, AVG_YEAR, YE = 40000, 24, 32, 30, 35
inc_pre = Decimal(OPT - OPT * EX / AVG_PERIOD) * 6 / 12
inc = inc_pre * SPLIT
assert inc == inc.to_integral_value()
inc = int(inc)
inc_year_avg = int((Decimal(OPT - Decimal(OPT * EX) / AVG_YEAR) * 6 / 12 * SPLIT).to_integral_value(ROUND_HALF_UP))
bond_int_pre = Decimal(remain) * COUPON + Decimal(CONVERTED) * COUPON * 8 / 12
bond_int = int((bond_int_pre * (1 - CT)).to_integral_value(ROUND_HALF_UP))
assert bond_int == bond_int_pre * (1 - CT)
bond_sh = int((Decimal(remain // 1000 * CONV) + Decimal(conv_sh) * 8 / 12) * SPLIT)
per_bond = Decimal(bond_int) / bond_sh
after_opt = Decimal(avail) / (wa + inc)
assert per_bond < after_opt
diluted = cents2((Decimal(avail) + bond_int) / (wa + inc + bond_sh))
diluted_remaining_only = cents2((Decimal(avail) + int(remain * COUPON * (1 - CT))) / (wa + inc + int(remain // 1000 * CONV * SPLIT)))
SIM6 = tbs(
    "far-tbs-eps-0002", "Public Company Reporting Topics", "Application",
    ["ASC 260-10 (basic and diluted EPS: weighted-average shares, stock splits after the balance sheet date, treasury stock method for options outstanding part of the period, if-converted method including conversions during the period, noncumulative preferred stock)"],
    "Year 2 earnings per share",
    f"""Corwin Corp., a public company, reports net income of {d(NI6)} for Year 2, its calendar year. Its income tax rate is 25%. Corwin's Year 2 financial statements will be issued on March 1, Year 3. Use the exhibits, and give every share figure on the basis on which Corwin will report it in its Year 2 statements. Round each earnings per share amount to the nearest cent (enter, for example, 1.23), and enter share counts as whole numbers.""",
    [("Exhibit 1: Share records", f"""
| Date | Event |
|---|---|
| January 1, Year 2 | {SH_JAN1:,} common shares outstanding; 20,000 shares held in treasury |
| May 1, Year 2 | Reissued {REISSUE_MAY1:,} treasury shares for cash |
| September 1, Year 2 | Holders converted {d(CONVERTED)} face of the convertible bonds (Exhibit 2) into common shares |
| December 15, Year 2 | Declared and paid a cash dividend of $0.40 per common share |
| February 10, Year 3 | The board declared a 3-for-2 stock split, distributed February 24, Year 3 |
| All year | {PREF_SH:,} shares of {int(PREF_RATE * 100)}% noncumulative, nonconvertible preferred stock, ${PREF_PAR} par, outstanding. The board declared no preferred dividend for Year 2. |
"""),
     ("Exhibit 2: Potential common shares and market data", f"""
| Item | Detail |
|---|---|
| Convertible bonds | {d(BONDS6)} face, {int(COUPON * 100)}% interest paid each December 31 issued at par in Year 0. Bonds converted during the year are paid interest accrued to the conversion date. Each $1,000 bond converts into {CONV} common shares. |
| Stock options | {OPT:,} options with an exercise price of ${EX}, granted July 1, Year 2; none exercised or forfeited |
| Market price of common stock | Average for July–December, Year 2, ${AVG_PERIOD}; average for all of Year 2, ${AVG_YEAR}; December 31, Year 2, ${YE} |
| Note | Every share count, price and conversion ratio in Exhibits 1 and 2 is stated before the 3-for-2 split. |
""")],
    [
        units("t1", "What is Corwin's weighted-average number of common shares outstanding for basic EPS for Year 2?", wa,
              f"Before the split: {SH_JAN1:,} + {REISSUE_MAY1:,} reissued treasury shares × 8/12 = {REISSUE_MAY1 * 8 // 12:,} + {conv_sh:,} shares issued on conversion ({CONVERTED // 1000:,} bonds × {CONV}) × 4/12 = {conv_sh * 4 // 12:,}, a total of {wa_no_split:,}. A stock split declared after year end but before the statements are issued is applied retroactively: {wa_no_split:,} × 1.5 = {wa:,}.",
              points=2),
        num("t2", "What is Corwin's basic EPS for Year 2?", basic,
            f"{d(avail)} ÷ {wa:,} = {basic}. The preferred stock is noncumulative and no dividend was declared for Year 2, so nothing is deducted (deducting a full year's {d(pref_full)} would give {basic_if_pref}). The common dividend doesn't affect EPS.", tolerance=0),
        units("t3", "How many incremental shares do the stock options add to the denominator of diluted EPS?", inc,
              f"Treasury stock method, using the average price for the period the options were outstanding: {OPT:,} − {OPT:,} × ${EX} ÷ ${AVG_PERIOD} = {OPT - OPT * EX // AVG_PERIOD:,} shares, weighted for the six months since the July 1 grant = {int(inc_pre):,}, × 1.5 for the split = {inc:,}. Using the full-year average price would give {inc_year_avg:,}."),
        num("t4", "By what amount does Corwin adjust the numerator of diluted EPS for the convertible bonds?", bond_int,
            f"Add back the after-tax interest recognized in Year 2 on all the bonds: {d(remain)} × {int(COUPON * 100)}% = {d(int(remain * COUPON))} on the bonds still outstanding, plus {d(CONVERTED)} × {int(COUPON * 100)}% × 8/12 = {d(int(CONVERTED * COUPON * 8 / 12))} on the converted bonds until September 1, a total of {d(int(bond_int_pre))}, × (1 − 25%) = {d(bond_int)}."),
        num("t5", "What is Corwin's diluted EPS for Year 2?", diluted,
            f"The options add {inc:,} shares. The bonds add {d(bond_int)} to income and {bond_sh:,} shares (after the split, {remain // 1000 * CONV:,} for the bonds outstanding all year plus {conv_sh:,} × 8/12 for the converted bonds before conversion, × 1.5), {per_bond.quantize(Decimal('0.01'))} per incremental share, below the {after_opt.quantize(Decimal('0.01'))} EPS after the options, so they are dilutive. ({d(avail)} + {d(bond_int)}) ÷ ({wa:,} + {inc:,} + {bond_sh:,}) = {diluted}. Ignoring the converted bonds' interest and shares before September 1 would give {diluted_remaining_only}.",
            points=2, tolerance=0),
    ],
)


ITEMS = [SIM1, SIM2, SIM3, SIM4, SIM5, SIM6]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
    for it in ITEMS:
        pts = sum(t["points"] for t in it["tasks"])
        assert 6 <= pts <= 10, (it["id"], pts)
        assert len(it["exhibits"]) >= 2, it["id"]
        with open(os.path.join(out, it["id"] + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(it, f, sort_keys=False, allow_unicode=True, width=100)
        print(it["id"], it["blueprint"]["skill"], len(it["tasks"]), "tasks,", pts, "points")
    print("cash flows", ni, cfo, cfi, cff, y2["cash"], int_paid, tax_paid, div_paid)
    print("consolidation", cor["cogs"], cor["ni"], draft["ni"], cor_bs["equip"], cor_bs["re"], [a for *_, a in sel2])
    print("balance sheet", cr_cash, cr_ca, cr_cl, cr_re, cr_eq, dr_re)
    print("income statement", c_gp, c_oi, c_cont, c_disc, c_ni, c_tci, dr_ni)
    print("nfp", wodr, wdr, released, expenses)
    print("eps", wa, basic, inc, bond_int, bond_sh, diluted)
