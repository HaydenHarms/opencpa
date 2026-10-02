"""FAR simulations batch 03 — six Area II simulations (docs/plans/far-simulations.md). See docs/reviews/far-tbs-03.md.

Every simulation has at least two source-style exhibits with data to reject, 6-10 points, a stated rounding rule and
one key line per account. Every number is computed here (Decimal, rounded half up) and stored in cents; the script
asserts that each reconciliation and schedule ties before writing anything.

Run: python3 scripts/batches/far-tbs-03.py  (writes content/far/far-tbs-*.yaml for this batch)
"""
import os
from decimal import Decimal, ROUND_HALF_UP

import yaml

A2 = "Area II — Select Balance Sheet Accounts"
NOTE = "FAR simulations batch 03. Written from scratch; every number computed in code."


def c(dollars):
    """Dollars (int or Decimal) to whole cents."""
    return int((Decimal(dollars) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def r0(x):
    """Round to the nearest dollar, half up."""
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def d(x):
    """$1,234 or ($1,234) for negatives."""
    return f"(${-x:,})" if x < 0 else f"${x:,}"


def amt(x):
    """Statement-style amount: 1,234 or (1,234)."""
    return f"({-x:,})" if x < 0 else f"{x:,}"


def num(id, prompt, dollars, explanation, points=1, tolerance=100):
    """A currency task: the key in cents, accepting answers within $1 unless told otherwise."""
    return dict(id=id, type="numeric", points=points, unit="cents", tolerance=tolerance, prompt=prompt,
                answer=c(dollars), explanation=explanation)


def select(id, prompt, options, rows, explanation, points):
    """rows: (row id, label, answer)."""
    for _, _, a in rows:
        assert a in options, a
    return dict(id=id, type="select", points=points, prompt=prompt, options=options,
                rows=[dict(id=i, label=l, answer=a) for i, l, a in rows], explanation=explanation)


def je(id, prompt, accounts, lines, explanation, points):
    """lines: (account, debit dollars, credit dollars). One line per account; debits must equal credits."""
    names = [a for a, _, _ in lines]
    assert len(set(names)) == len(names), names
    assert all(a in accounts for a in names), names
    assert sum(dr for _, dr, _ in lines) == sum(cr for _, _, cr in lines), lines
    return dict(id=id, type="journal_entry", points=points, prompt=prompt, accounts=accounts,
                answer=[dict(account=a, debit=c(dr), credit=c(cr)) for a, dr, cr in lines], explanation=explanation)


def table(header, rows):
    out = "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n"
    return out + "\n".join("| " + " | ".join(str(x) for x in r) + " |" for r in rows)


def tbs(id, topic, skill, refs, title, scenario, exhibits, tasks):
    return dict(
        id=id, type="tbs",
        blueprint=dict(section="FAR", area=A2, topic=topic, skill=skill),
        review=dict(status="reviewed", references=refs, notes=NOTE),
        title=title, scenario=scenario.strip(),
        exhibits=[dict(title=t, body=b.strip()) for t, b in exhibits],
        tasks=tasks,
    )


# ── Simulation 1: receivables subledger to GL, with expected credit losses (II.B.d, Analysis) ─────────────────
# Correct December 31 customer balances, by aging bucket (current, 1-30, 31-60, over 60 days past due).
BUCKETS = ["Current", "1–30 days past due", "31–60 days past due", "Over 60 days past due"]
RATES = [Decimal("0.01"), Decimal("0.04"), Decimal("0.12"), Decimal("0.40")]
TRUE = {
    "Ashdown Builders": [48200, 12600, 0, 0],
    "Calloway Hardware": [31500, 0, 8400, 0],
    "Drummond Supply": [22800, 9700, 0, 0],
    "Feltham Contractors": [0, 6300, 11200, 0],
    "Hexley Homes": [39900, 0, 0, 0],
    "Kenmure Lumber": [26400, 14100, 0, 9800],
    "Pryor & Sons": [0, 0, 5600, 17400],
    "Tolland Renovations": [18300, 7500, 0, 0],
}
CREDIT_CUST, CREDIT_BAL = "Marlowe Interiors", 3600          # overpaid; credit balance in both records
MISAPPLIED = 9200            # Pryor & Sons' Dec 22 payment, for over-60 invoices, posted to Ashdown's current account
WRITE_OFF_CUST, WRITE_OFF = "Ormsby Fixtures", 8700           # written off Dec 20 in the GL only; still in subledger (over 60)
FOB_DEST, FOB_CUST = 15800, "Hexley Homes"                    # billed Dec 30, shipped FOB destination, delivered Jan 3
FORKLIFT = 6400              # forklift sale proceeds entered in the AR column of the cash receipts journal (GL only)
JAN_RECEIPT = 12600          # Ashdown's January 6 payment of its 1-30 balance: data to reject
ALLOW_JAN1, WRITE_OFFS_BEFORE_DEC, RECOVERY = 14500, 11900, 1300

true_debit = sum(sum(v) for v in TRUE.values())
true_net = true_debit - CREDIT_BAL
# The subledger as shown: misapplication (Pryor over-60 still includes the 9,200; Ashdown current is 9,200 too low),
# the written-off account still listed, and the FOB destination invoice included in Hexley's current balance.
shown = {k: list(v) for k, v in TRUE.items()}
shown["Pryor & Sons"][3] += MISAPPLIED
shown["Ashdown Builders"][0] -= MISAPPLIED
shown["Hexley Homes"][0] += FOB_DEST
shown[WRITE_OFF_CUST] = [0, 0, 0, WRITE_OFF]
sub_debit = sum(sum(v) for v in shown.values())
sub_net = sub_debit - CREDIT_BAL
gl_shown = true_net + FOB_DEST - FORKLIFT                      # the write-off was posted to the GL; forklift understates it
assert sub_net == true_net + FOB_DEST + WRITE_OFF
bucket_true = [sum(v[i] for v in TRUE.values()) for i in range(4)]
allow_req = r0(sum(b * r for b, r in zip(bucket_true, RATES)))
bucket_shown = [sum(v[i] for v in shown.values()) for i in range(4)]
allow_shown_aging = r0(sum(b * r for b, r in zip(bucket_shown, RATES)))
allow_before = ALLOW_JAN1 - WRITE_OFFS_BEFORE_DEC - WRITE_OFF + RECOVERY
expense = allow_req - allow_before
# Errors a candidate could make, for the explanations
allow_no_misapp = r0(sum(b * r for b, r in zip(
    [bucket_true[0] - MISAPPLIED, bucket_true[1], bucket_true[2], bucket_true[3] + MISAPPLIED], RATES)))
ar_reported = true_debit
GL_DEC1 = 302100
dec_sales = 268400
dec_receipts_col = GL_DEC1 + dec_sales - WRITE_OFF - gl_shown        # the AR column total posted (includes the forklift)
assert dec_receipts_col > 0

aging_rows = []
for name in sorted(shown):
    v = shown[name]
    aging_rows.append((name, *[amt(x) if x else "—" for x in v], amt(sum(v))))
aging_rows.append(("**Total customer debit balances**", *[amt(b) for b in bucket_shown], amt(sub_debit)))
aging_rows.append((f"{CREDIT_CUST} (credit balance from an overpayment)", "", "", "", "", amt(-CREDIT_BAL)))
aging_rows.append(("**Net subledger balance**", "", "", "", "", amt(sub_net)))
assert sum(bucket_shown) == sub_debit
aging_body = table(["Customer", *BUCKETS, "Balance"], aging_rows)
gl_body = table(["Date", "Posting", "Debit", "Credit", "Balance"], [
    ("Dec 1", "Balance forward", "", "", amt(GL_DEC1)),
    ("Dec 20", f"Write-off approved by the controller ({WRITE_OFF_CUST}); debit allowance for credit losses", "", amt(WRITE_OFF), amt(GL_DEC1 - WRITE_OFF)),
    ("Dec 31", "Sales journal total", amt(dec_sales), "", amt(GL_DEC1 - WRITE_OFF + dec_sales)),
    ("Dec 31", "Cash receipts journal, accounts receivable column total", "", amt(dec_receipts_col), amt(gl_shown)),
])
docs1 = table(["Document", "Detail"], [
    ("Remittance advice, Pryor & Sons, received Dec 22", f"Check for {d(MISAPPLIED)} \"in payment of invoices 4471 and 4476\" (both dated September 28, due October 28). The cashier's deposit slip shows the check; the receivables clerk applied it to Ashdown Builders' account, against Ashdown's current (not yet due) invoices."),
    ("Bill of lading 8821 and invoice 5190, Dec 30", f"Goods invoiced to {FOB_CUST} for {d(FOB_DEST)}, terms FOB destination. The carrier's delivery receipt is signed by Hexley on January 3. The invoice is in the December sales journal and in Hexley's account."),
    ("Cash receipts journal, Dec 14", f"Receipt of {d(FORKLIFT)} from Garside Equipment for a used forklift Tamsin sold, entered in the accounts receivable column. Garside has never been a customer, and the forklift's cost and accumulated depreciation are still in the equipment accounts."),
    ("Credit committee minutes, Dec 20", f"{WRITE_OFF_CUST}' account ({d(WRITE_OFF)}, all over 60 days past due) is uncollectible; the business has closed. Approved for write-off."),
    ("Customer correspondence, Jan 6, Year 3", f"Ashdown Builders paid {d(JAN_RECEIPT)} by wire, settling its 1–30 day balance."),
    ("Allowance for credit losses, Year 2", f"January 1 balance {d(ALLOW_JAN1)} (credit). Write-offs January–November {d(WRITE_OFFS_BEFORE_DEC)}. A {d(RECOVERY)} account written off in Year 1 was recovered in August and reinstated. No credit loss expense has been recorded for Year 2."),
])
rates_body = table(["Aging category", "Expected loss rate"], [(b, f"{int(r * 100)}%") for b, r in zip(BUCKETS, RATES)]) + (
    "\n\nThe rates are based on Tamsin's loss history for customers of this kind, adjusted for current conditions and reasonable and supportable forecasts. Tamsin, a private company, does not elect the practical expedient in ASU 2025-05, so the related election to consider collections received after the balance sheet date is not available to it. The rates apply to every customer balance, by its age at December 31, Year 2.")

SIM1 = tbs(
    "far-tbs-receivables-reconciliation-0001", "Trade receivables", "Analysis",
    ["ASC 310-10 (trade receivables)", "ASC 326-20 (expected credit losses; pooling by aging; write-offs and recoveries)",
     "ASC 606-10-25-30 (control transfers, for the FOB destination shipment)", "ASC 210-10-45 (customer credit balances presented as liabilities)"],
    "Year 2 receivables reconciliation and allowance",
    f"""Tamsin Supply Co. sells building materials on 30-day terms and closes its books on December 31, Year 2. Its accounts receivable subledger (the customer aging in Exhibit 1) does not agree with the general ledger control account (Exhibit 2). The controller has pulled the documents in Exhibit 3, and Exhibit 4 gives Tamsin's credit loss rates. Before the investigation, no entry has been made for any item in Exhibit 3. Round every amount to the nearest dollar.""",
    [("Exhibit 1: Accounts receivable aging, December 31, Year 2 (subledger)", aging_body),
     ("Exhibit 2: General ledger, accounts receivable control account, December, Year 2", gl_body),
     ("Exhibit 3: Documents pulled by the controller", docs1),
     ("Exhibit 4: Credit loss rates", rates_body)],
    [
        select("t1", "For each document in Exhibit 3, indicate which record must be corrected to state accounts receivable correctly at December 31, Year 2.",
               ["Subledger only", "General ledger only", "Both the subledger and the general ledger", "Neither"],
               [("r1", "Pryor & Sons remittance (December 22)", "Subledger only"),
                ("r2", "Invoice 5190 to Hexley Homes (December 30)", "Both the subledger and the general ledger"),
                ("r3", "Garside Equipment receipt (December 14)", "General ledger only"),
                ("r4", f"{WRITE_OFF_CUST} write-off (December 20)", "Subledger only"),
                ("r5", "Ashdown Builders wire (January 6, Year 3)", "Neither")],
               f"The misapplied payment moved {d(MISAPPLIED)} between two customer accounts; the control account total was right, so only the subledger changes (and the aging, since the payment settled Pryor's over-60 invoices, not Ashdown's current ones). Hexley's goods were shipped FOB destination and delivered January 3, so control had not transferred at year end: the invoice comes out of both records. The forklift proceeds were never a customer receivable, so only the control account was wrongly credited. The write-off was posted to the control account but the customer is still in the aging. The January wire is a Year 3 collection; the December 31 balance stands.",
               points=2),
        num("t2", "What should the balance of Tamsin's accounts receivable control account be at December 31, Year 2, after the investigation?", true_net,
            f"Start from the control account {d(gl_shown)}: remove the Hexley invoice for goods not yet delivered (− {d(FOB_DEST)}) and reverse the forklift proceeds wrongly credited to receivables (+ {d(FORKLIFT)}): {d(gl_shown)} − {d(FOB_DEST)} + {d(FORKLIFT)} = {d(true_net)}. Check from the subledger: {d(sub_net)} − {d(FOB_DEST)} − {d(WRITE_OFF)} write-off = {d(true_net)}; the misapplied payment does not change the total."),
        num("t3", "What amount should Tamsin report as accounts receivable (before the allowance) in its December 31, Year 2, balance sheet?", ar_reported,
            f"Report the customer debit balances, {d(true_debit)}. {CREDIT_CUST}'s {d(CREDIT_BAL)} credit balance is an amount Tamsin owes, reported with liabilities rather than netted against receivables (netting gives {d(true_net)})."),
        num("t4", "What balance should Tamsin's allowance for credit losses have at December 31, Year 2?", allow_req,
            "Apply the rates to the corrected aging: " + "; ".join(f"{BUCKETS[i].lower()} {d(bucket_true[i])} × {int(RATES[i] * 100)}%" for i in range(4))
            + f", a total of {d(allow_req)}. The corrected aging reflects Pryor's payment against its over-60 invoices, removes {WRITE_OFF_CUST} and Hexley's December 30 invoice. Applying the rates to the unadjusted aging gives {d(allow_shown_aging)}; correcting the totals but leaving Pryor's payment against Ashdown's current balance gives {d(allow_no_misapp)}. The January wire does not change the December 31 aging.",
            points=2),
        num("t5", "What credit loss expense should Tamsin recognize for Year 2?", expense,
            f"Allowance before adjustment: {d(ALLOW_JAN1)} − write-offs {d(WRITE_OFFS_BEFORE_DEC)} − {d(WRITE_OFF)} (December) + recovery {d(RECOVERY)} = {d(allow_before)}. Expense = required {d(allow_req)} − {d(allow_before)} = {d(expense)}.",
            points=2),
    ],
)


# ── Simulation 2: inventory costing and lower of cost and NRV across product lines (II.C.a/b, Application) ────
# Line 1 (tents, FIFO), line 2 (stoves, FIFO), line 3 (fuel canisters, periodic weighted average).
TENT_LAYERS = [("Beginning inventory", 120, Decimal("84")), ("March 9 purchase", 300, Decimal("88")),
               ("July 22 purchase", 260, Decimal("91")), ("November 3 purchase", 180, Decimal("95"))]
TENT_RETURN = 20                     # 20 of the Nov 3 tents returned to the supplier Nov 20 (defective)
TENT_SOLD = 590
STOVE_LAYERS = [("Beginning inventory", 200, Decimal("41")), ("April 14 purchase", 450, Decimal("43")),
                ("October 2 purchase", 300, Decimal("46"))]
STOVE_SOLD = 640
STOVE_DAMAGED = 30                   # water-damaged units, NRV per unit below
FUEL_LAYERS = [("Beginning inventory", 2400, Decimal("5.10")), ("February purchase", 6000, Decimal("5.30")),
               ("June purchase", 5000, Decimal("5.55")), ("September purchase", 4600, Decimal("5.80"))]
FUEL_FREIGHT = 1800                  # freight-in on the June purchase, part of cost
FUEL_SOLD = 14100
CONSIGNED_FUEL = 900                 # canisters held for Ridgeline Supply on consignment, in the count
# Year-end market data
TENT_PRICE, TENT_SELL_COST, TENT_REPL = Decimal("128"), Decimal("14"), Decimal("90")
STOVE_PRICE, STOVE_SELL_COST, STOVE_REPL = Decimal("52"), Decimal("8"), Decimal("44")
STOVE_DMG_PRICE, STOVE_DMG_COST = Decimal("30"), Decimal("6")
FUEL_PRICE, FUEL_SELL_COST, FUEL_REPL = Decimal("6.20"), Decimal("0.90"), Decimal("5.40")
MARGIN = Decimal("0.25")             # normal profit margin: data to reject

tent_units = sum(u for _, u, _ in TENT_LAYERS) - TENT_RETURN - TENT_SOLD
tent_avail = [(n, u - (TENT_RETURN if n.startswith("November") else 0), p) for n, u, p in TENT_LAYERS]
# FIFO ending: the latest layers
left, tent_cost, tent_detail = tent_units, Decimal(0), []
for n, u, p in reversed(tent_avail):
    take = min(u, left)
    if take:
        tent_cost += take * p
        tent_detail.append((n, take, p))
    left -= take
assert left == 0
tent_cost = r0(tent_cost)
stove_units = sum(u for _, u, _ in STOVE_LAYERS) - STOVE_SOLD
left, stove_cost, stove_detail = stove_units, Decimal(0), []
for n, u, p in reversed(STOVE_LAYERS):
    take = min(u, left)
    if take:
        stove_cost += take * p
        stove_detail.append((n, take, p))
    left -= take
assert left == 0
stove_cost = r0(stove_cost)
fuel_units_avail = sum(u for _, u, _ in FUEL_LAYERS)
fuel_cost_avail = sum(u * p for _, u, p in FUEL_LAYERS) + FUEL_FREIGHT
fuel_avg = (fuel_cost_avail / fuel_units_avail).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
fuel_units = fuel_units_avail - FUEL_SOLD
fuel_count = fuel_units + CONSIGNED_FUEL
fuel_cost = r0(fuel_units * fuel_cost_avail / fuel_units_avail)
fuel_cost_no_freight = r0(fuel_units * (fuel_cost_avail - FUEL_FREIGHT) / fuel_units_avail)
fuel_cost_with_consigned = r0(fuel_count * fuel_cost_avail / fuel_units_avail)
# Simple average of unit prices (a common error)
fuel_simple = r0(fuel_units * sum(p for _, _, p in FUEL_LAYERS) / len(FUEL_LAYERS))
# NRV by line
tent_nrv = r0(tent_units * (TENT_PRICE - TENT_SELL_COST))
stove_good = stove_units - STOVE_DAMAGED
stove_nrv = r0(stove_good * (STOVE_PRICE - STOVE_SELL_COST) + STOVE_DAMAGED * (STOVE_DMG_PRICE - STOVE_DMG_COST))
fuel_nrv = r0(fuel_units * (FUEL_PRICE - FUEL_SELL_COST))
lines = [("Tents", tent_cost, tent_nrv), ("Stoves", stove_cost, stove_nrv), ("Fuel canisters", fuel_cost, fuel_nrv)]
writedown = sum(max(0, cst - nrv) for _, cst, nrv in lines)
carrying = sum(min(cst, nrv) for _, cst, nrv in lines)
assert tent_nrv > tent_cost and stove_nrv < stove_cost and fuel_nrv < fuel_cost, lines
# Errors for the explanations: LCM with replacement cost (superseded for FIFO/average), and item-by-item for stoves
stove_damaged_cost = r0(STOVE_DAMAGED * stove_detail[0][2])
total_nrv = tent_nrv + stove_nrv + fuel_nrv
total_cost = tent_cost + stove_cost + fuel_cost
assert total_nrv > total_cost                  # applying the test to the total would show no write-down

purchases2 = table(["Product line (method)", "Date", "Units", "Unit cost"],
                   [("Tents (FIFO)", n, f"{u:,}", f"${p:,.2f}") for n, u, p in TENT_LAYERS]
                   + [("Tents (FIFO)", "November 20 return to supplier (from the November 3 purchase)", f"({TENT_RETURN})", f"${TENT_LAYERS[3][2]:,.2f}")]
                   + [("Stoves (FIFO)", n, f"{u:,}", f"${p:,.2f}") for n, u, p in STOVE_LAYERS]
                   + [("Fuel canisters (weighted average, periodic)", n, f"{u:,}", f"${p:,.2f}") for n, u, p in FUEL_LAYERS]) + (
    f"\n\nFreight-in of {d(FUEL_FREIGHT)} was paid on the June canister purchase and charged to a freight expense account. Units sold during Year 2: tents {TENT_SOLD:,}, stoves {STOVE_SOLD:,}, fuel canisters {FUEL_SOLD:,}.")
count2 = table(["Product line", "Units counted", "Count notes"], [
    ("Tents", f"{tent_units:,}", "All saleable."),
    ("Stoves", f"{stove_units:,}", f"{STOVE_DAMAGED} units in the October 2 lot were water-damaged in a roof leak in December and can only be sold as seconds."),
    ("Fuel canisters", f"{fuel_count:,}", f"Includes {CONSIGNED_FUEL:,} canisters Ridgeline Supply shipped to Pellworth on consignment; Pellworth sells them for Ridgeline on commission."),
])
market2 = table(["Product line", "Expected selling price per unit", "Costs to sell per unit", "Current replacement cost per unit"], [
    ("Tents", f"${TENT_PRICE:,.2f}", f"${TENT_SELL_COST:,.2f}", f"${TENT_REPL:,.2f}"),
    ("Stoves (undamaged)", f"${STOVE_PRICE:,.2f}", f"${STOVE_SELL_COST:,.2f}", f"${STOVE_REPL:,.2f}"),
    ("Stoves (damaged, sold as seconds)", f"${STOVE_DMG_PRICE:,.2f}", f"${STOVE_DMG_COST:,.2f}", "—"),
    ("Fuel canisters", f"${FUEL_PRICE:,.2f}", f"${FUEL_SELL_COST:,.2f}", f"${FUEL_REPL:,.2f}"),
]) + f"\n\nPellworth's normal profit margin is {int(MARGIN * 100)}% of selling price. Selling prices are those expected in the ordinary course of business in January, Year 3."

SIM2 = tbs(
    "far-tbs-inventory-measurement-0001", "Inventory", "Application",
    ["ASC 330-10-30 (inventory cost, including freight-in)",
     "ASC 330-10-35-1B (lower of cost and net realizable value for inventory measured using FIFO or average cost)",
     "ASC 330-10-35 (applying the measurement test to individual items, categories or the total inventory)",
     "ASC 606-10-55-79 to 55-80 (consignment arrangements)"],
    "Year 2 inventory costing and measurement",
    f"""Pellworth Outfitters Co. sells camping equipment in three product lines and closes its books on December 31, Year 2. It uses FIFO for tents and stoves and the periodic weighted-average method for fuel canisters, and it applies its year-end inventory measurement test to each product line as a whole (the category level), as its accounting policy states. The exhibits show the year's purchase records, the year-end count and market data. No adjustment has been recorded for any item in the exhibits. Round each amount to the nearest dollar, and do not round the weighted-average unit cost before multiplying.""",
    [("Exhibit 1: Year 2 purchase records", purchases2),
     ("Exhibit 2: December 31, Year 2 physical count", count2),
     ("Exhibit 3: Year-end market data", market2)],
    [
        num("t1", "What is the cost of Pellworth's tent inventory at December 31, Year 2?", tent_cost,
            f"Units on hand: {sum(u for _, u, _ in TENT_LAYERS):,} acquired − {TENT_RETURN} returned − {TENT_SOLD} sold = {tent_units}. FIFO leaves the latest costs: "
            + " + ".join(f"{u} × ${p}" for _, u, p in tent_detail) + f" = {d(tent_cost)}. The 20 returned tents come out of the November 3 layer, leaving {TENT_LAYERS[3][1] - TENT_RETURN} at ${TENT_LAYERS[3][2]}."),
        num("t2", "What is the cost of Pellworth's fuel canister inventory at December 31, Year 2?", fuel_cost,
            f"Pellworth owns {fuel_units_avail:,} − {FUEL_SOLD:,} = {fuel_units:,} canisters; the {CONSIGNED_FUEL:,} consigned canisters belong to Ridgeline. Cost of goods available = purchases at invoice cost {d(r0(fuel_cost_avail - FUEL_FREIGHT))} + freight-in {d(FUEL_FREIGHT)} (a cost of bringing the goods to their location) = {d(r0(fuel_cost_avail))}, for an average of about ${fuel_avg} per canister. {fuel_units:,} × {d(r0(fuel_cost_avail))} ÷ {fuel_units_avail:,} = ${fuel_units * fuel_cost_avail / fuel_units_avail:,.2f}, rounded to {d(fuel_cost)}. Leaving out freight gives {d(fuel_cost_no_freight)}; counting the consigned goods gives {d(fuel_cost_with_consigned)}; a simple average of the four unit prices gives {d(fuel_simple)}.",
            points=2),
        num("t3", "What is the net realizable value of Pellworth's stove inventory at December 31, Year 2?", stove_nrv,
            f"Undamaged: {stove_good} × (${STOVE_PRICE} − ${STOVE_SELL_COST}) = {d(r0(stove_good * (STOVE_PRICE - STOVE_SELL_COST)))}. Damaged: {STOVE_DAMAGED} × (${STOVE_DMG_PRICE} − ${STOVE_DMG_COST}) = {d(r0(STOVE_DAMAGED * (STOVE_DMG_PRICE - STOVE_DMG_COST)))}. Total {d(stove_nrv)}. Replacement cost is not part of NRV."),
        num("t4", "What total inventory write-down should Pellworth recognize at December 31, Year 2?", writedown,
            "By product line, cost against NRV: " + "; ".join(f"{n} {d(cst)} against {d(nrv)}" for n, cst, nrv in lines)
            + f". Tents need no write-down (NRV is higher); stoves are written down {d(stove_cost - stove_nrv)} and fuel canisters {d(fuel_cost - fuel_nrv)}, a total of {d(writedown)}. FIFO and average-cost inventories use the lower of cost and NRV, not the lower of cost or market, so replacement cost and the normal profit margin don't enter. Comparing total cost {d(total_cost)} with total NRV {d(total_nrv)} would show no write-down, but Pellworth's policy is the product-line level.",
            points=2),
        num("t5", "What amount should Pellworth report as inventory in its December 31, Year 2, balance sheet?", carrying,
            f"Tents at cost {d(tent_cost)} + stoves at NRV {d(stove_nrv)} + fuel canisters at NRV {d(fuel_nrv)} = {d(carrying)}."),
    ],
)


# ── Simulation 3: PP&E rollforward review (II.D.f, Analysis) ─────────────────────────────────────────────────
# Revision 2 (after the review gate): new id. far-tbs-ppe-rollforward-0001 is retired and must not be reused.
# Garroway Freight's equipment. Straight-line, no residual value unless stated, monthly convention: a full month's
# depreciation in the month of acquisition, none in the month of disposal.
COST_JAN1, AD_JAN1 = 4860000, 1934000
DEP_OTHER = 512400                   # Year 2 depreciation on equipment held all year other than truck T-14
# April 1: sale of a tractor (staff handled it correctly)
SOLD_COST, SOLD_AD_JAN1, SOLD_ANNUAL, SOLD_PRICE = 142000, 118000, 14200, 15500
sold_dep = SOLD_ANNUAL * 3 // 12
sold_ad = SOLD_AD_JAN1 + sold_dep
sale_gl = SOLD_PRICE - (SOLD_COST - sold_ad)
# July 1: exchange of a refrigerated trailer for a flatbed that opens backhaul revenue (commercial substance; boot is
# over 25% too, so fair value applies under every reading of ASC 845 and ASC 610-20)
OLD_COST, OLD_AD_JAN1, OLD_LIFE = 96000, 54000, 8
OLD_FV, BOOT = 38000, 27000
NEW_TRAILER_LIFE = 10
old_dep = OLD_COST // OLD_LIFE * 6 // 12
old_ad = OLD_AD_JAN1 + old_dep
old_bv = OLD_COST - old_ad
new_trailer = OLD_FV + BOOT                       # fair value given up plus cash
exch_gain = OLD_FV - old_bv
new_trailer_dep = r0(Decimal(new_trailer) / NEW_TRAILER_LIFE * 6 / 12)
staff_trailer = old_bv + BOOT                     # staff carried over book value and recorded no gain
staff_exch_gain = 0
staff_trailer_dep = r0(Decimal(staff_trailer) / NEW_TRAILER_LIFE * 6 / 12)
assert OLD_FV > old_bv
# July 1: engine overhaul on truck T-14 that extends its life (Garroway's policy capitalizes life-extending overhauls)
T14_COST, T14_AD_JAN1, T14_ANNUAL = 240000, 150000, 30000      # 3 years of life left at January 1
OVERHAUL, T14_NEW_REMAINING = 54000, 5
t14_dep_h1 = T14_ANNUAL * 6 // 12
t14_bv_jul1 = T14_COST - T14_AD_JAN1 - t14_dep_h1 + OVERHAUL
t14_dep_h2 = r0(Decimal(t14_bv_jul1) / T14_NEW_REMAINING * 6 / 12)
t14_dep = t14_dep_h1 + t14_dep_h2
staff_t14_dep = T14_ANNUAL                       # staff expensed the overhaul and kept the old rate
# October 1: new tractor; 2% cash discount taken (paid October 8); separately priced extended service contract
TRACTOR_LIST, DISC_RATE, SERVICE, TRACTOR_LIFE = 190000, Decimal("0.02"), 7200, 6
tractor_cost = r0(TRACTOR_LIST * (1 - DISC_RATE))
tractor_dep_exact = Decimal(tractor_cost) / TRACTOR_LIFE * 3 / 12
tractor_dep = r0(tractor_dep_exact)
staff_tractor = TRACTOR_LIST + SERVICE            # staff capitalized the list price and the service contract
staff_tractor_dep_exact = Decimal(staff_tractor) / TRACTOR_LIFE
staff_tractor_dep = r0(staff_tractor_dep_exact)   # and took a full year
# Correct figures
dep_exp = DEP_OTHER + t14_dep + tractor_dep + new_trailer_dep + old_dep + sold_dep
cost_dec31 = COST_JAN1 + tractor_cost + new_trailer + OVERHAUL - OLD_COST - SOLD_COST
ad_dec31 = AD_JAN1 + dep_exp - old_ad - sold_ad
net_gl = sale_gl + exch_gain
assert net_gl < 0
# The staff's draft
d_add = staff_tractor + staff_trailer
d_dep = DEP_OTHER + staff_t14_dep + staff_tractor_dep + staff_trailer_dep + old_dep + sold_dep
d_disp_cost = OLD_COST + SOLD_COST
d_disp_ad = old_ad + sold_ad
d_cost = COST_JAN1 + d_add - d_disp_cost
d_ad = AD_JAN1 + d_dep - d_disp_ad
d_gl = staff_exch_gain + sale_gl
dep_over = d_dep - dep_exp
assert dep_over > 0 and d_disp_cost == OLD_COST + SOLD_COST
rf_draft = table(["", "Equipment, at cost", "Accumulated depreciation"], [
    ("Balance, January 1, Year 2", amt(COST_JAN1), amt(AD_JAN1)),
    ("Additions", amt(d_add), ""),
    ("Depreciation expense", "", amt(d_dep)),
    ("Disposals", amt(-d_disp_cost), amt(-d_disp_ad)),
    ("Balance, December 31, Year 2", amt(d_cost), amt(d_ad)),
]) + f"\n\nNet gain (loss) on disposals recorded for Year 2: {amt(d_gl)}."
docs3 = table(["Date", "Document", "Detail"], [
    ("April 1", "Bill of sale", f"Sold a tractor (cost {d(SOLD_COST)}; accumulated depreciation at January 1, Year 2, {d(SOLD_AD_JAN1)}; depreciation {d(SOLD_ANNUAL)} a year) for {d(SOLD_PRICE)} cash."),
    ("July 1", "Exchange agreement with Coyle Trailer Sales", f"Garroway traded a refrigerated trailer (cost {d(OLD_COST)}; accumulated depreciation at January 1, Year 2, {d(OLD_AD_JAN1)}; {OLD_LIFE}-year life) plus {d(BOOT)} cash for a new flatbed trailer. An independent appraiser Garroway engaged valued the trailer given up at {d(OLD_FV)}. Garroway's dispatch plan: the flatbed will carry building materials on the return leg of routes that the refrigerated trailer ran back empty, for customers Garroway hasn't served before, raising the routes' expected annual revenue by about 30%. The flatbed has a {NEW_TRAILER_LIFE}-year life."),
    ("July 1", "Shop work order, truck T-14", f"Engine overhaul, {d(OVERHAUL)}, charged to repairs expense. T-14 cost {d(T14_COST)}, had accumulated depreciation of {d(T14_AD_JAN1)} at January 1, Year 2, and was being depreciated at {d(T14_ANNUAL)} a year. The fleet manager's memo: the overhaul extends T-14's remaining life from two and a half years to {T14_NEW_REMAINING} years from July 1."),
    ("October 1", "Dealer invoice, Kestrel Truck Center", f"New tractor, list price {d(TRACTOR_LIST)}, terms 2/10, net 30; paid October 8, taking the discount (the discount was credited to other income). Three-year extended service contract, separately priced, {d(SERVICE)}. The tractor has a {TRACTOR_LIFE}-year life."),
    ("December 31", "Depreciation schedule", f"Depreciation on equipment held all year, other than truck T-14: {d(DEP_OTHER)}. The insurer's December appraisal values the fleet at {d(3410000)}."),
])
SIM3 = tbs(
    "far-tbs-ppe-rollforward-0002", "Property, plant and equipment", "Analysis",
    ["ASC 360-10-30 (cost of PP&E, net of cash discounts taken)",
     "ASC 360-10-35 (depreciation; revising the remaining life after a life-extending expenditure is a change in estimate, ASC 250-10-45-17)",
     "ASC 845-10 (nonmonetary exchanges: fair value, commercial substance, and the 25% monetary consideration threshold)",
     "ASC 360-10-40 (derecognition: gain or loss on disposal)"],
    "Year 2 equipment rollforward review",
    f"""Garroway Freight Co. owns trucks and trailers. Its staff accountant drafted the Year 2 rollforward of the equipment account and its accumulated depreciation (Exhibit 1); you are reviewing it against the supporting documents (Exhibit 2). Garroway uses the straight-line method with no residual values, takes a full month of depreciation in the month an asset is acquired and none in the month it is disposed of, and capitalizes overhauls that extend an asset's useful life to the equipment account. The January 1 balances and the depreciation figure for equipment held all year (other than truck T-14) are correct. Round every amount to the nearest dollar.""",
    [("Exhibit 1: Draft rollforward prepared by the staff accountant", rf_draft),
     ("Exhibit 2: Supporting documents", docs3)],
    [
        select("t1", "For each line of the staff's draft, indicate whether it is correct or misstated.",
               ["Correct", "Misstated"],
               [("r1", "Additions", "Misstated"),
                ("r2", "Depreciation expense", "Misstated"),
                ("r3", "Disposals, equipment at cost", "Correct"),
                ("r4", "Disposals, accumulated depreciation", "Correct"),
                ("r5", "Net gain (loss) on disposals", "Misstated")],
               f"Additions should hold the tractor at its cash price net of the discount (not list price plus the service contract, which is a prepaid service), the flatbed at the fair value given up plus cash (not book value plus cash), and the T-14 overhaul. Depreciation is misstated by all three. The disposals remove the right cost ({d(OLD_COST)} + {d(SOLD_COST)}) and the right accumulated depreciation, brought up to the disposal dates ({d(old_ad)} + {d(sold_ad)}). The draft's net loss leaves out the {d(exch_gain)} gain on the exchange.",
               points=2),
        num("t2", "What should Garroway report as equipment, at cost, at December 31, Year 2?", cost_dec31,
            f"Tractor: {d(TRACTOR_LIST)} × 98% = {d(tractor_cost)}. Flatbed: fair value of the trailer given up {d(OLD_FV)} + cash {d(BOOT)} = {d(new_trailer)}. The exchange has commercial substance: the flatbed earns backhaul revenue from new customers, so its cash flows differ significantly from the refrigerated trailer's. (The cash is also more than 25% of the exchange's fair value, which makes it a monetary exchange measured at fair value in any case, and derecognizing the trailer under ASC 610-20 gives the same fair value and gain.) The flatbed's own fair value isn't given, so its cost is the fair value given up plus the cash. Carrying over the {d(old_bv)} book value gives {d(staff_trailer)}. Overhaul: {d(OVERHAUL)}. Equipment = {d(COST_JAN1)} + {d(tractor_cost)} + {d(new_trailer)} + {d(OVERHAUL)} − {d(OLD_COST)} − {d(SOLD_COST)} = {d(cost_dec31)}.",
            points=2),
        num("t3", "What is Garroway's depreciation expense on equipment for Year 2?", dep_exp,
            f"Equipment held all year other than T-14: {d(DEP_OTHER)}. T-14: January–June {d(T14_ANNUAL)} × 6/12 = {d(t14_dep_h1)}; carrying amount at July 1 is {d(T14_COST)} − {d(T14_AD_JAN1)} − {d(t14_dep_h1)} + {d(OVERHAUL)} = {d(t14_bv_jul1)}, and July–December is {d(t14_bv_jul1)} ÷ {T14_NEW_REMAINING} × 6/12 = {d(t14_dep_h2)}. New tractor: {d(tractor_cost)} ÷ {TRACTOR_LIFE} × 3/12 = ${tractor_dep_exact:,.2f}, rounded to {d(tractor_dep)}. Flatbed: {d(new_trailer)} ÷ {NEW_TRAILER_LIFE} × 6/12 = {d(new_trailer_dep)}. Old trailer, January–June: {d(old_dep)}. Tractor sold, January–March: {d(sold_dep)}. Total: {d(DEP_OTHER)} + {d(t14_dep)} + {d(tractor_dep)} + {d(new_trailer_dep)} + {d(old_dep)} + {d(sold_dep)} = {d(dep_exp)}."),
        num("t4", "What should Garroway report as accumulated depreciation on equipment at December 31, Year 2?", ad_dec31,
            f"{d(AD_JAN1)} + depreciation {d(dep_exp)} − old trailer {d(old_ad)} − tractor sold {d(sold_ad)} = {d(ad_dec31)}.",
            points=2),
        num("t5", "By how much does the staff's draft overstate (understate) depreciation expense for Year 2? Enter an understatement as a negative number.", dep_over,
            f"Draft {d(d_dep)} − correct {d(dep_exp)} = {d(dep_over)}. The draft takes a full year on {d(staff_tractor)} for the tractor ({d(staff_tractor_dep)} against {d(tractor_dep)}), keeps T-14 at {d(T14_ANNUAL)} (against {d(t14_dep)}), and depreciates the flatbed from {d(staff_trailer)} ({d(staff_trailer_dep)} against {d(new_trailer_dep)})."),
        num("t6", "What net gain or loss on equipment disposals should Garroway report for Year 2? Enter a net loss as a negative number.", net_gl,
            f"Sale: {d(SOLD_PRICE)} − book value {d(SOLD_COST - sold_ad)} ({d(SOLD_COST)} − {d(sold_ad)}) = {d(sale_gl)}. Exchange: fair value {d(OLD_FV)} − book value {d(old_bv)} = gain {d(exch_gain)}. Net {d(net_gl)}."),
    ],
)


# ── Simulation 4: bonds at a discount, effective interest, partial open-market retirement (II.H.1c/d, App) ────
FACE, COUPON, YIELD = 2400000, Decimal("0.05"), Decimal("0.06")      # 8-year bonds, semiannual
PV_1, PV_A = Decimal("0.62317"), Decimal("12.56110")                  # 16 periods at 3%
price = r0(FACE * PV_1 + FACE * COUPON / 2 * PV_A)
cash_int = r0(FACE * COUPON / 2)
sched, cv = [], price
for _ in range(4):            # Jun 30 Y1, Dec 31 Y1, Jun 30 Y2, Dec 31 Y2 (full bonds, before retirement)
    ie = r0(cv * YIELD / 2)
    sched.append((cv, ie, ie - cash_int))
    cv += ie - cash_int
int_y1 = sched[0][1] + sched[1][1]
cv_y1 = price + sched[0][2] + sched[1][2]
cv_jun30_y2 = cv_y1 + sched[2][2]
RET = Decimal("0.40")
ret_face = int(FACE * RET)
ret_cv_jul1 = r0(cv_jun30_y2 * RET)
ret_ie = r0(ret_cv_jul1 * YIELD / 2 * 3 / 6)                 # July-September on the retired 40%
ret_cash_int = r0(ret_face * COUPON / 2 * 3 / 6)
ret_cv = ret_cv_jul1 + ret_ie - ret_cash_int
REP_PRICE = Decimal("0.98")
rep_cash = r0(ret_face * REP_PRICE)
gain_ret = ret_cv - rep_cash                # negative: a loss
assert gain_ret < 0
ret_disc = ret_face - ret_cv_jul1          # discount on the retired bonds at July 1; the entry amortizes and removes it
remain_cv_jul1 = cv_jun30_y2 - ret_cv_jul1
remain_ie = r0(remain_cv_jul1 * YIELD / 2)
int_y2 = sched[2][1] + ret_ie + remain_ie
# Errors for the explanations
gain_no_partial = (ret_cv_jul1 - rep_cash)
CALL = Decimal("1.02")
gain_at_call = ret_cv - r0(ret_face * CALL)
SIM4 = tbs(
    "far-tbs-bonds-payable-0001", "Debt (Notes and bonds payable)", "Application",
    ["ASC 835-30-35 (interest method: amortization of discount)",
     "ASC 470-50-40 (extinguishment of debt: gain or loss is the difference between the reacquisition price and the net carrying amount)"],
    "Bonds payable: issue, interest and a partial retirement",
    f"""Halvard Corp. issued bonds on January 1, Year 1 (Exhibit 1). It amortizes discount or premium by the effective interest method and keeps a separate discount or premium account. On October 1, Year 2, it bought back part of the issue in the open market (Exhibit 3) and cancelled the bonds. Halvard records interest only on the interest payment dates and when bonds are retired. Round every amount to the nearest dollar at each step, and compute interest for part of a period by prorating the period's effective interest by months.""",
    [("Exhibit 1: Bond terms (from the indenture)", table(["Term", "Detail"], [
        ("Face amount", d(FACE)), ("Stated rate", "5% a year, paid each June 30 and December 31"),
        ("Dated and issued", "January 1, Year 1"), ("Maturity", "December 31, Year 8"),
        ("Call provision", "Callable at Halvard's option at 102 on any interest date after December 31, Year 3"),
        ("Market yield at issue", "6% a year, compounded semiannually")])),
     ("Exhibit 2: Present value factors", table(["Factor", "2.5%, 8 periods", "2.5%, 16 periods", "3%, 8 periods", "3%, 16 periods"], [
        ("Present value of 1", "0.82075", "0.67362", "0.78941", str(PV_1)),
        ("Present value of an ordinary annuity of 1", "7.17014", "13.05500", "7.01969", str(PV_A))])),
     ("Exhibit 3: Broker's confirmation, October 1, Year 2", f"Halvard purchased {d(ret_face)} face amount of its 5% bonds due Year 8 at 98, plus accrued interest from July 1. Settlement {d(rep_cash + ret_cash_int)}: principal {d(rep_cash)}, accrued interest {d(ret_cash_int)}. The bonds were delivered to the trustee for cancellation.")],
    [
        num("t1", "At what amount should Halvard record the bonds on January 1, Year 1?", price,
            f"16 semiannual periods at 3%: {d(FACE)} × {PV_1} = {d(r0(FACE * PV_1))}, plus interest {d(cash_int)} × {PV_A} = {d(r0(FACE * COUPON / 2 * PV_A))}, a total of {d(price)} (a discount of {d(FACE - price)}). The 2.5% factors would discount at the stated rate."),
        num("t2", "What is Halvard's interest expense on the bonds for Year 1?", int_y1,
            f"June 30: {d(price)} × 3% = {d(sched[0][1])}; the carrying amount rises by {d(sched[0][2])} to {d(sched[1][0])}. December 31: {d(sched[1][0])} × 3% = {d(sched[1][1])}. Total {d(int_y1)}, against cash interest of {d(2 * cash_int)}."),
        num("t3", "What gain or loss should Halvard recognize on the October 1, Year 2, retirement? Enter a loss as a negative number.", gain_ret,
            f"Carrying amount at June 30, Year 2: {d(cv_jun30_y2)}; the retired 40% is {d(ret_cv_jul1)}. Interest to October 1 on that portion: {d(ret_cv_jul1)} × 3% × 3/6 = {d(ret_ie)}, of which {d(ret_cash_int)} is paid in cash, so the carrying amount rises to {d(ret_cv)}. Reacquisition price {d(rep_cash)} (the accrued interest is not part of it). Net carrying amount {d(ret_cv)} − reacquisition price {d(rep_cash)} = {d(gain_ret)}, a loss of {d(-gain_ret)}. Skipping the July–September amortization gives {d(gain_no_partial)}; the call price doesn't apply to an open-market purchase (using it gives {d(gain_at_call)}).",
            points=2),
        je("t4", "Prepare Halvard's journal entry on October 1, Year 2, to record the retirement, as a single entry.",
           ["Bonds payable", "Discount on bonds payable", "Premium on bonds payable", "Interest expense", "Interest payable",
            "Cash", "Gain on extinguishment of debt", "Loss on extinguishment of debt"],
           [("Bonds payable", ret_face, 0), ("Interest expense", ret_ie, 0),
            ("Discount on bonds payable", 0, ret_disc), ("Cash", 0, rep_cash + ret_cash_int),
            ("Loss on extinguishment of debt", -gain_ret, 0)],
           f"Debit bonds payable for the face retired, {d(ret_face)}, and interest expense for July–September, {d(ret_ie)}. Credit the whole discount on those bonds at July 1, {d(ret_face)} − {d(ret_cv_jul1)} = {d(ret_disc)}: {d(ret_ie - ret_cash_int)} of it is the July–September amortization and the remaining {d(ret_face - ret_cv)} is removed with the bonds. Credit cash for the settlement, {d(rep_cash)} + {d(ret_cash_int)} accrued interest = {d(rep_cash + ret_cash_int)}. The difference is the loss on extinguishment, {d(-gain_ret)}.",
           points=2),
        num("t5", "What is Halvard's interest expense on the bonds for Year 2?", int_y2,
            f"January–June on all the bonds: {d(sched[2][0])} × 3% = {d(sched[2][1])}. July–September on the retired 40%: {d(ret_ie)}. July–December on the 60% still outstanding: ({d(cv_jun30_y2)} − {d(ret_cv_jul1)}) × 3% = {d(remain_ie)}. Total {d(int_y2)}.",
            points=2),
    ],
)


# ── Simulation 5: equity method across two years, basis differences and upstream sales (II.E.3b, App) ──────────
PRICE5, PCT = 1890000, Decimal("0.30")
BV_APR1 = 4800000                      # Bexley's net assets at book value, April 1, Year 1
INV_EXCESS = 150000                    # inventory FV over book; all sold by December, Year 1
BLDG_EXCESS, BLDG_LIFE = 600000, 20    # remaining life from April 1, Year 1
PATENT_EXCESS, PATENT_LIFE = 240000, 5
share_excess = {k: r0(v * PCT) for k, v in dict(inv=INV_EXCESS, bldg=BLDG_EXCESS, patent=PATENT_EXCESS).items()}
goodwill5 = PRICE5 - r0(BV_APR1 * PCT) - sum(share_excess.values())
assert goodwill5 > 0
NI_Y1_FULL, NI_Y1_APR_DEC = 920000, 700000
DIV_Y1 = 200000                         # declared and paid in November, Year 1
OCI_Y1 = 60000                          # Bexley's OCI April-December, Year 1 (unrealized gain on AFS debt)
NI_Y2, DIV_Y2, OCI_Y2 = 1040000, 260000, -40000
UP_SALES_Y1, UP_GP_RATE, UP_HELD_Y1 = 400000, Decimal("0.30"), 90000     # Bexley sold to Hartwell; Hartwell still held 90,000 at cost to it
UP_HELD_Y2 = 50000                      # from Year 2 upstream sales at the same margin, still held at Dec 31, Year 2
amort_y1 = share_excess["inv"] + r0(Decimal(share_excess["bldg"]) / BLDG_LIFE * 9 / 12) + r0(Decimal(share_excess["patent"]) / PATENT_LIFE * 9 / 12)
amort_y2 = r0(Decimal(share_excess["bldg"]) / BLDG_LIFE) + r0(Decimal(share_excess["patent"]) / PATENT_LIFE)
up_y1 = r0(UP_HELD_Y1 * UP_GP_RATE * PCT)
up_y2 = r0(UP_HELD_Y2 * UP_GP_RATE * PCT)
eq_y1 = r0(NI_Y1_APR_DEC * PCT) - amort_y1 - up_y1
eq_y2 = r0(NI_Y2 * PCT) - amort_y2 + up_y1 - up_y2
ca_y1 = PRICE5 + eq_y1 + r0(OCI_Y1 * PCT) - r0(DIV_Y1 * PCT)
ca_y2 = ca_y1 + eq_y2 + r0(OCI_Y2 * PCT) - r0(DIV_Y2 * PCT)
# Errors for the explanations
eq_y1_fullyear = r0(NI_Y1_FULL * PCT) - amort_y1 - up_y1
eq_y1_no_inv = eq_y1 + share_excess["inv"]
eq_y1_full_up = r0(NI_Y1_APR_DEC * PCT) - amort_y1 - r0(UP_HELD_Y1 * UP_GP_RATE)
eq_y2_no_realize = eq_y2 - up_y1
FV_Y1, FV_Y2 = 2110000, 2275000                       # fair value of Hartwell's shares: data to reject
SIM5 = tbs(
    "far-tbs-equity-method-0001", "Investments (Equity method investments)", "Application",
    ["ASC 323-10-35 (equity method: share of earnings from the date significant influence is obtained, basis differences, dividends, OCI)",
     "ASC 323-10-35-7 to 35-10 (intra-entity profits in assets still held by the investor)",
     "ASC 350-20 (equity method goodwill is not amortized)"],
    "Equity method investment over two years",
    f"""On April 1, Year 1, Hartwell Corp., a public company, paid {d(PRICE5)} for 30% of the common stock of Bexley Inc., which gives Hartwell significant influence over Bexley. Hartwell accounts for the investment by the equity method and has not elected the fair value option. Both companies have calendar years. Use the exhibits; ignore income taxes, and round every amount to the nearest dollar.""",
    [("Exhibit 1: Purchase price analysis, April 1, Year 1", table(["Item", "Amount"], [
        ("Bexley's net assets at book value", d(BV_APR1)),
        ("Inventory: fair value in excess of book value (all sold to Bexley's customers by December, Year 1)", d(INV_EXCESS)),
        (f"Warehouse: fair value in excess of book value (remaining life {BLDG_LIFE} years, straight-line)", d(BLDG_EXCESS)),
        (f"Patent: fair value in excess of book value (remaining life {PATENT_LIFE} years, straight-line)", d(PATENT_EXCESS)),
        ("Land: Hartwell's valuation found fair value equal to book value. (An appraisal Bexley obtained for its lender, on a replacement-cost basis, showed $310,000 more.)", "—"),
        ("Any remaining excess of cost", "Goodwill")])),
     ("Exhibit 2: Bexley's reported results", table(["", "Year 1", "Year 2"], [
        ("Net income, full year", d(NI_Y1_FULL), d(NI_Y2)),
        ("Net income, April 1 – December 31", d(NI_Y1_APR_DEC), "—"),
        ("Other comprehensive income (unrealized gains (losses) on debt securities); Year 1 is April 1 – December 31", d(OCI_Y1), d(OCI_Y2)),
        ("Cash dividends declared and paid", f"{d(DIV_Y1)} (November)", f"{d(DIV_Y2)} (October)")])),
     ("Exhibit 3: Hartwell's purchases from Bexley", f"""Bexley sells components to Hartwell at its usual gross margin of 30% of selling price. Hartwell bought {d(UP_SALES_Y1)} of components from Bexley in Year 1 (all after April 1); {d(UP_HELD_Y1)} of them, at Hartwell's cost, were in Hartwell's inventory at December 31, Year 1, and were used in production in Year 2. Of Hartwell's Year 2 purchases from Bexley, {d(UP_HELD_Y2)} at Hartwell's cost were in its inventory at December 31, Year 2.

Hartwell's broker values its Bexley shares at {d(FV_Y1)} at December 31, Year 1, and {d(FV_Y2)} at December 31, Year 2.""")],
    [
        num("t1", "What amount of goodwill is implicit in Hartwell's investment at April 1, Year 1?", goodwill5,
            f"Cost {d(PRICE5)} − 30% of book value {d(r0(BV_APR1 * PCT))} − 30% of the excess fair values: inventory {d(share_excess['inv'])}, warehouse {d(share_excess['bldg'])}, patent {d(share_excess['patent'])} = {d(goodwill5)}. Hartwell's valuation puts the land at book value, so there is no land basis difference; the lender's replacement-cost appraisal is not fair value."),
        num("t2", "What equity in Bexley's earnings should Hartwell report for Year 1?", eq_y1,
            f"30% of Bexley's April–December income {d(r0(NI_Y1_APR_DEC * PCT))} − basis-difference amortization {d(amort_y1)} (inventory {d(share_excess['inv'])}, all sold in Year 1; warehouse {d(share_excess['bldg'])} ÷ {BLDG_LIFE} × 9/12; patent {d(share_excess['patent'])} ÷ {PATENT_LIFE} × 9/12) − 30% of the profit in components Hartwell still holds, {d(UP_HELD_Y1)} × 30% × 30% = {d(up_y1)}. Equity in earnings = {d(eq_y1)}. Using Bexley's full-year income gives {d(eq_y1_fullyear)}; eliminating all the unrealized profit rather than Hartwell's 30% gives {d(eq_y1_full_up)}.",
            points=2),
        num("t3", "What is the carrying amount of Hartwell's investment in Bexley at December 31, Year 1?", ca_y1,
            f"{d(PRICE5)} + equity in earnings {d(eq_y1)} + 30% of OCI {d(r0(OCI_Y1 * PCT))} − dividends {d(r0(DIV_Y1 * PCT))} = {d(ca_y1)}. Dividends reduce the investment; they are not income. The broker's value is not used under the equity method."),
        num("t4", "What equity in Bexley's earnings should Hartwell report for Year 2?", eq_y2,
            f"30% of {d(NI_Y2)} = {d(r0(NI_Y2 * PCT))} − amortization {d(amort_y2)} (warehouse {d(r0(Decimal(share_excess['bldg']) / BLDG_LIFE))}, patent {d(r0(Decimal(share_excess['patent']) / PATENT_LIFE))}; goodwill is not amortized) + Year 1 profit now realized {d(up_y1)} − profit in components held at year end, {d(UP_HELD_Y2)} × 30% × 30% = {d(up_y2)}. Total {d(eq_y2)}. Forgetting to recognize the Year 1 deferral gives {d(eq_y2_no_realize)}.",
            points=2),
        num("t5", "What is the carrying amount of Hartwell's investment in Bexley at December 31, Year 2?", ca_y2,
            f"{d(ca_y1)} + {d(eq_y2)} + 30% of OCI {d(r0(OCI_Y2 * PCT))} − dividends {d(r0(DIV_Y2 * PCT))} = {d(ca_y2)}."),
    ],
)


# ── Simulation 6: search for unrecorded liabilities and reconcile payables (II.G.d, Analysis) ──────────────────
# Brackwell Manufacturing records every vendor invoice for goods and services in accounts payable.
SUB6, = (581340,)
COD_EQUIP = 22600            # COD equipment purchase entered in the AP column of the cash disbursements journal (GL only)
GL6 = SUB6 - COD_EQUIP       # before findings the GL is lower by the COD debit
UNREC_RECEIVED = 18450       # goods received Dec 28, FOB shipping point, invoice Dec 27, paid Jan 12: unrecorded
FOB_DEST_JAN = 9800          # goods shipped FOB destination Dec 30, received Jan 3: not a Year 2 liability
LEGAL = 7200                 # legal services rendered in December, billed Jan 9, paid Jan 25: unrecorded
JAN_SERVICES = 4300          # January maintenance contract billed Jan 2 for January: not a Year 2 liability
IN_TRANSIT = 13750           # vendor statement: shipped Dec 29 FOB shipping point, received Jan 5, not recorded
CREDIT_MEMO = 5900           # vendor statement: credit memo Dec 20 for returned goods, not recorded by Brackwell
CHECK_IN_MAIL = 16200        # vendor statement: Brackwell's Dec 31 payment not yet on the vendor's statement
correct6 = SUB6 + UNREC_RECEIVED + LEGAL + IN_TRANSIT - CREDIT_MEMO
gl_adj = correct6 - GL6
sub_adj = correct6 - SUB6
assert gl_adj - sub_adj == COD_EQUIP
# The vendor statement balance per vendor and Brackwell's subledger balance for that vendor
VEND_SUB = 48900
vend_stmt = VEND_SUB + IN_TRANSIT - CREDIT_MEMO + CHECK_IN_MAIL
correct_vendor = VEND_SUB + IN_TRANSIT - CREDIT_MEMO
# Errors for the explanations
wrong_with_dest = correct6 + FOB_DEST_JAN
wrong_with_mail = correct6 + CHECK_IN_MAIL
disb6 = table(["Check", "Date paid", "Payee", "Amount", "Supporting documents"], [
    ("10412", "January 4, Year 3", "Ferris Steel", d(31250), "Invoice dated December 3, Year 2; recorded in accounts payable in December"),
    ("10418", "January 9, Year 3", "Lindqvist Fasteners", d(FOB_DEST_JAN), "Invoice dated December 30, Year 2; terms FOB destination; receiving report January 3, Year 3"),
    ("10426", "January 12, Year 3", "Oakhurst Resin", d(UNREC_RECEIVED), "Invoice dated December 27, Year 2; terms FOB shipping point; receiving report December 28, Year 2; not in the December 31 subledger"),
    ("10431", "January 15, Year 3", "Penrose Maintenance", d(JAN_SERVICES), "Invoice dated January 2, Year 3, for the January service contract"),
    ("10440", "January 25, Year 3", "Whitcombe & Hale LLP", d(LEGAL), "Invoice dated January 9, Year 3, for contract review performed November 28 – December 19, Year 2"),
    ("10447", "January 28, Year 3", "Ferris Steel", d(26400), "Invoice dated January 11, Year 3; receiving report January 10, Year 3"),
])
stmt6 = table(["Date", "Description", "Charges", "Credits", "Balance"], [
    ("Dec 1", "Balance forward", "", "", d(VEND_SUB + CHECK_IN_MAIL - 21800 - 9400)),
    ("Dec 8", "Invoice 7731", d(21800), "", d(VEND_SUB + CHECK_IN_MAIL - 9400)),
    ("Dec 15", "Invoice 7768", d(9400), "", d(VEND_SUB + CHECK_IN_MAIL)),
    ("Dec 20", "Credit memo CM-212, returned pallets of resin", "", d(CREDIT_MEMO), d(VEND_SUB + CHECK_IN_MAIL - CREDIT_MEMO)),
    ("Dec 29", "Invoice 7810, shipped FOB shipping point", d(IN_TRANSIT), "", d(vend_stmt)),
]) + f"\n\nBrackwell's subledger shows Corran Polymers at {d(VEND_SUB)}. Brackwell mailed a {d(CHECK_IN_MAIL)} check to Corran on December 31 and recorded it that day; the goods on invoice 7810 arrived January 5, Year 3, and the invoice was recorded then. Brackwell's receiving dock shipped the returned pallets on December 18."
gl6 = table(["", "Amount"], [
    ("Accounts payable subledger (vendor trial balance), December 31, Year 2", d(SUB6)),
    ("General ledger accounts payable control account, December 31, Year 2", d(GL6)),
]) + f"\n\nCash disbursements journal, December 14, Year 2: check 10377 for {d(COD_EQUIP)} to Varley Machinery, cash on delivery for a drill press, entered in the accounts payable column. Varley has no vendor account in the subledger."
SIM6 = tbs(
    "far-tbs-payables-reconciliation-0001", "Payables and accrued liabilities", "Analysis",
    ["ASC 405-10 (liabilities)", "ASC 330-10 (title to goods in transit: FOB shipping point and FOB destination)",
],
    "Year-end accounts payable: unrecorded liabilities and reconciliation",
    f"""Brackwell Manufacturing Co. closes its books on December 31, Year 2. It has no accrued-liabilities account: every amount it owes a vendor for goods or services is reported as accounts payable, whether or not the invoice has arrived. The controller is closing accounts payable. The exhibits show the subledger and control account balances, a December entry in the cash disbursements journal, Brackwell's January, Year 3, disbursements, and a statement from its largest resin supplier, Corran Polymers. No entry has been made for any finding yet. Enter every amount in whole dollars, and enter a decrease as a negative number.""",
    [("Exhibit 1: Balances at December 31, Year 2", gl6),
     ("Exhibit 2: Cash disbursements, January, Year 3", disb6),
     ("Exhibit 3: Corran Polymers statement of account, December, Year 2", stmt6)],
    [
        select("t1", "For each item, indicate its effect on Brackwell's accounts payable at December 31, Year 2.",
               ["Increase accounts payable", "Decrease accounts payable", "No adjustment"],
               [("r1", "Check 10418 to Lindqvist Fasteners", "No adjustment"),
                ("r2", "Check 10426 to Oakhurst Resin", "Increase accounts payable"),
                ("r3", "Check 10440 to Whitcombe & Hale LLP", "Increase accounts payable"),
                ("r4", "Corran Polymers invoice 7810", "Increase accounts payable"),
                ("r5", "Corran Polymers credit memo CM-212", "Decrease accounts payable"),
                ("r6", "Brackwell's December 31 check to Corran Polymers", "No adjustment")],
               f"Lindqvist's goods were shipped FOB destination and received January 3, so Brackwell owed nothing at year end. Oakhurst's goods were received December 28 under FOB shipping point terms; the invoice was simply not recorded. Whitcombe & Hale's services were performed in December, so the obligation existed at year end even though the bill came in January. Corran's invoice 7810 was shipped FOB shipping point on December 29, so title passed in transit. Corran's credit memo for goods Brackwell returned in December reduces what Brackwell owes. The December 31 check was recorded correctly; it is a timing difference on Corran's statement.",
               points=2),
        num("t2", "What amount should Brackwell report as accounts payable at December 31, Year 2?", correct6,
            f"Subledger {d(SUB6)} + Oakhurst {d(UNREC_RECEIVED)} + Whitcombe & Hale {d(LEGAL)} + Corran invoice 7810 {d(IN_TRANSIT)} − Corran credit memo {d(CREDIT_MEMO)} = {d(correct6)}. Including Lindqvist's FOB destination invoice gives {d(wrong_with_dest)}; adding back the check in the mail gives {d(wrong_with_mail)}. The January service contract and the January Ferris invoice are Year 3 liabilities, and the December Ferris invoice is already recorded.",
            points=2),
        num("t3", "By what net amount must Brackwell adjust its general ledger accounts payable control account? Enter a decrease as a negative number.", gl_adj,
            f"The control account ({d(GL6)}) is also understated by the {d(COD_EQUIP)} cash-on-delivery payment debited to it; that purchase never created a payable. Adjustment = {d(correct6)} − {d(GL6)} = {d(gl_adj)}: the four findings, net {d(sub_adj)}, plus {d(COD_EQUIP)}."),
        num("t4", "By what net amount must Brackwell adjust its accounts payable subledger? Enter a decrease as a negative number.", sub_adj,
            f"{d(UNREC_RECEIVED)} + {d(LEGAL)} + {d(IN_TRANSIT)} − {d(CREDIT_MEMO)} = {d(sub_adj)}. The cash-on-delivery error was in the general ledger only."),
        num("t5", "After the adjustments, what balance should Brackwell's subledger show for Corran Polymers at December 31, Year 2?", correct_vendor,
            f"Corran's statement {d(vend_stmt)} − Brackwell's check in transit to Corran {d(CHECK_IN_MAIL)} = {d(correct_vendor)}, which agrees with Brackwell's {d(VEND_SUB)} + invoice 7810 {d(IN_TRANSIT)} − credit memo {d(CREDIT_MEMO)}."),
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
    print("receivables", gl_shown, sub_net, true_net, true_debit, bucket_true, allow_req, allow_shown_aging, allow_no_misapp, allow_before, expense)
    print("inventory", tent_units, tent_cost, fuel_units, fuel_cost, stove_cost, stove_nrv, tent_nrv, fuel_nrv, writedown, carrying)
    print("ppe", d_cost, d_ad, d_dep, d_gl, cost_dec31, dep_exp, ad_dec31, dep_over, net_gl)
    print("bonds", price, int_y1, cv_y1, cv_jun30_y2, ret_cv, gain_ret, ret_disc, int_y2)
    print("equity", goodwill5, amort_y1, eq_y1, ca_y1, amort_y2, eq_y2, ca_y2)
    print("payables", GL6, correct6, gl_adj, sub_adj, vend_stmt, correct_vendor)
