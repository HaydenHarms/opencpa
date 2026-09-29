"""FAR variants 01: three extra versions (new numbers, same test) for 13 numeric items from FAR batch 05.

Each item gets a builder that writes the whole question (stem, choices, rationales, explanation) from its
parameters. Parameter set 0 must reproduce the reviewed item word for word (the script asserts it), which
shows the template is faithful; sets 1-3 become the item's variants. Every amount is computed here with
Decimal, rounded half up.

Run: python3 scripts/batches/far-variants-01.py  (adds `variants` to the 13 files in content/far/)
See docs/reviews/far-variants-01.md.
"""
import os
import sys
from decimal import Decimal as D, ROUND_HALF_UP

import yaml

from common import attach_variants, audit, variant

CONTENT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "far")
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 8: "eight", 9: "nine", 10: "ten"}


def m(x):
    """$1,234 (or $1,234.56 when there are cents)."""
    x = D(x).quantize(D("0.01"), ROUND_HALF_UP)
    return f"${x:,.0f}" if x == x.to_integral() else f"${x:,.2f}"


def n(x):
    """1,234 without a dollar sign."""
    return f"{D(x):,.0f}"


def r2(x):
    return D(x).quantize(D("0.01"), ROUND_HALF_UP)


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole-dollar amount, got {x}"
    return x


# ── Area I ───────────────────────────────────────────────────────────────


def foreign_currency(p):
    co, e, r0, r1, r2_ = p["co"], D(p["eur"]), D(p["r0"]), D(p["r1"]), D(p["r2"])
    loss1 = whole(e * (r1 - r0))         # Year 1 remeasurement loss
    gain2 = whole(e * (r1 - r2_))        # Year 2 gain against the Dec 31 rate
    vs_orig = whole(e * (r2_ - r0))      # Year 2 compared with the original rate
    assert r1 > r2_ > r0
    short = co.split()[0]
    return variant(
        f"""On November 1, Year 1, {co}, whose functional currency is the U.S. dollar, buys inventory from a German supplier for €{n(e)}, payable on February 1, Year 2. Exchange rates for one euro were ${r0} on November 1, ${r1} on December 31, and ${r2_} on February 1, when {short} paid the invoice. What foreign currency transaction gain or loss should {short} report in Year 1 and in Year 2?""",
        [(f"$0 in Year 1; {m(vs_orig)} loss in Year 2", "Waits until settlement and compares the payment with the original rate. The payable is remeasured at each balance sheet date."),
         (f"{m(loss1)} gain in Year 1; {m(gain2)} loss in Year 2", f"Reverses the signs, as if {short} held a euro receivable. A stronger euro increases what {short} owes."),
         (f"{m(loss1)} loss in Year 1; {m(gain2)} gain in Year 2", f"Correct. Year 1: €{n(e)} × (${r1} − ${r0}). Year 2: €{n(e)} × (${r1} − ${r2_})."),
         (f"{m(loss1)} loss in Year 1; {m(vs_orig)} loss in Year 2", f"Measures Year 2 against the original ${r0} rate instead of the December 31 rate, counting part of the Year 1 loss again.")],
        "C",
        f"""A payable denominated in a foreign currency is remeasured at the spot rate at each balance sheet date and at settlement, with changes reported in net income. December 31: the payable rises from {m(e * r0)} to {m(e * r1)}, a {m(loss1)} loss in Year 1. February 1: {short} pays {m(e * r2_)}, so Year 2 has a {m(gain2)} gain.""",
    )


def performance_metrics(p):
    co, rev, ni, it, tax, da, a0, a1 = (p[k] for k in ("co", "rev", "ni", "int", "tax", "da", "a0", "a1"))
    ebitda = ni + it + tax + da
    avg = D(a0 + a1) / 2
    turn, turn_end = r2(D(rev) / avg), r2(D(rev) / D(a1))
    short = co.split()[0]
    return variant(
        f"""For Year 2, {co} reports revenue of {m(rev)} and net income of {m(ni)}, after interest expense of {m(it)}, income tax expense of {m(tax)}, and depreciation and amortization of {m(da)}. Total assets were {m(a0)} at the start of the year and {m(a1)} at the end. Using average total assets, what are {short}'s EBITDA and asset turnover?""",
        [(f"{m(ebitda - da)} EBITDA; {turn} asset turnover", f"Leaves out the {m(da)} of depreciation and amortization, which EBITDA adds back."),
         (f"{m(ebitda - it)} EBITDA; {turn} asset turnover", f"Leaves out the {m(it)} of interest expense, which EBITDA adds back."),
         (f"{m(ebitda)} EBITDA; {turn_end} asset turnover", "Gets EBITDA right but divides revenue by ending total assets instead of the average."),
         (f"{m(ebitda)} EBITDA; {turn} asset turnover", f"Correct. EBITDA = {m(ni)} + {m(it)} + {m(tax)} + {m(da)}; asset turnover = {m(rev)} ÷ {m(avg)}.")],
        "D",
        f"""EBITDA = net income + interest + income taxes + depreciation and amortization = {m(ni)} + {m(it)} + {m(tax)} + {m(da)} = {m(ebitda)}. Asset turnover = revenue ÷ average total assets = {m(rev)} ÷ [({m(a0)} + {m(a1)}) ÷ 2] = {turn}.""",
    )


def balance_sheet(p):
    co, b, l, dt, w, bc, lc = (p[k] for k in ("co", "bonds", "lease", "dtl", "warr", "bond_cur", "lease_cur"))
    total = b + l + dt + w
    key = (b - bc) + (l - lc) + dt
    short = co.split()[0]
    return variant(
        f"""{co}'s draft December 31, Year 1, classified balance sheet reports total noncurrent liabilities of {m(total)}: bonds payable {m(b)}, operating lease liabilities {m(l)}, deferred tax liability {m(dt)}, and warranty liability {m(w)}. Supporting schedules show that {m(bc)} of the bonds mature on June 30, Year 2; that {m(lc)} of the lease liability will be paid during Year 2; and that the warranty claims are all expected to be paid during Year 2. After correcting the draft, what are {short}'s total noncurrent liabilities?""",
        [(m(key - dt), f"Also moves the {m(dt)} deferred tax liability to current. Deferred taxes are always classified as noncurrent."),
         (m(key), f"Correct. {m(b - bc)} of bonds + {m(l - lc)} of lease liability + {m(dt)} deferred tax liability."),
         (m(key + lc), f"Leaves the {m(lc)} current portion of the lease liability in noncurrent."),
         (m(key + bc), f"Leaves the {m(bc)} of bonds maturing in Year 2 in noncurrent.")],
        "B",
        f"""Liabilities due within a year are current: the {m(bc)} of bonds maturing in Year 2, the {m(lc)} of lease payments due in Year 2, and the {m(w)} warranty liability. Deferred tax liabilities are classified as noncurrent. Noncurrent liabilities = {m(b - bc)} + {m(l - lc)} + {m(dt)} = {m(key)}.""",
    )


def cash_flows(p):
    co, ni, dep, disc, dtl, gain, ap, inv, stock = (
        p[k] for k in ("co", "ni", "dep", "disc", "dtl", "gain", "ap", "inv", "stock"))
    draft = ni + dep + disc + dtl - gain + ap + inv + stock
    key = draft - 2 * inv - stock
    return variant(
        f"""{co}'s staff accountant prepared this draft operating section of the statement of cash flows under the indirect method: net income {m(ni)}; depreciation {m(dep)}; amortization of discount on bonds payable {m(disc)}; increase in deferred tax liability {m(dtl)}; gain on sale of land $({n(gain)}); increase in accounts payable {m(ap)}; increase in inventory {m(inv)}; proceeds from issuing common stock {m(stock)}; net cash provided by operating activities {m(draft)}. After correcting the draft to comply with U.S. GAAP, what is net cash provided by operating activities?""",
        [(m(key), f"Correct. The inventory increase is subtracted ({m(2 * inv)} swing) and the stock proceeds move to financing."),
         (m(draft - stock), "Moves the stock proceeds to financing but still adds the increase in inventory. Buying more inventory uses cash."),
         (m(draft - 2 * inv), f"Subtracts the inventory increase but leaves the {m(stock)} of stock proceeds in operating activities."),
         (m(draft), "Accepts the draft.")],
        "A",
        f"""Two errors. An increase in inventory is subtracted under the indirect method, not added: that changes the total by {m(2 * inv)}. Proceeds from issuing stock are a financing inflow. The other adjustments are right: depreciation, discount amortization and the deferred tax increase are noncash charges added back, the gain on land is subtracted, and the payables increase is added. Corrected: {m(draft)} − {m(2 * inv)} − {m(stock)} = {m(key)}.""",
    )


def consolidation(p):
    par, sub, ta, loan, rate, date, due, months = (
        p[k] for k in ("par", "sub", "ta", "loan", "rate", "date", "due", "months"))
    acc = whole(D(loan) * D(rate) / 100 * months / 12)
    key = ta - loan - acc
    pshort, sshort = par.split()[0], sub.split()[0]
    return variant(
        f"""{par} owns 100% of {sub} {pshort}'s draft December 31, Year 1, consolidated balance sheet reports total assets of {m(ta)}; to prepare it, the staff eliminated {pshort}'s investment in {sshort} against {sshort}'s equity and added the two companies' other balances. Supporting schedules show that on {date}, Year 1, {pshort} lent {sshort} {m(loan)} at {rate}%, with interest due each {due}, and that both companies accrued interest at December 31. After any corrections needed, what total assets should the consolidated balance sheet report?""",
        [(m(key - acc), f"Eliminates the accrued interest twice, once for each company's accrual. Only {pshort}'s {m(acc)} receivable is an asset."),
         (m(key), f"Correct. {m(ta)} − {m(loan)} note receivable − {m(acc)} accrued interest receivable."),
         (m(ta - loan), f"Eliminates the note but not the {m(acc)} of accrued interest receivable."),
         (m(ta), "Accepts the draft. Balances between parent and subsidiary are eliminated, not only the investment account.")],
        "B",
        f"""Consolidated statements present the group as one entity, so the intercompany loan is eliminated along with the investment. {pshort}'s note receivable ({m(loan)}) and accrued interest receivable ({m(loan)} × {rate}% × {months}/12 = {m(acc)}) come out of assets, and {sshort}'s matching payables come out of liabilities. Total assets = {m(ta)} − {m(loan + acc)} = {m(key)}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def software(p):
    co, lic, cfg, train, conv, date, months, years = (
        p[k] for k in ("co", "lic", "cfg", "train", "conv", "date", "months", "years"))
    cap = lic + cfg
    per = lambda base: whole(D(base) / years * months / 12)
    amort = per(cap)
    key = amort + train + conv
    short = co.split()[0]
    yw = WORDS[years]
    return variant(
        f"""On January 1, Year 1, {co} buys a perpetual license for accounting software to use internally for {m(lic)}. It also pays a consultant {m(cfg)} to configure the software for {short}'s processes, {m(train)} to train employees, and {m(conv)} to convert data from its old system. The software is ready for its intended use on {date}, Year 1, and {short} amortizes it straight-line over {yw} years. What total expense related to these costs should {short} recognize in Year 1?""",
        [(m(per(cap + train + conv)), "Capitalizes the training and data conversion costs as well. Both are expensed as incurred."),
         (m(key), f"Correct. Capitalized cost {m(cap)} ÷ {years} × {months}/12 = {m(amort)} of amortization, plus {m(train + conv)} of training and data conversion."),
         (m(whole(D(cap) / years) + train + conv), f"Amortizes from January 1. Amortization begins when the software is ready for its intended use on {date}."),
         (m(per(lic) + cfg + train + conv), f"Expenses the {m(cfg)} of configuration. Costs to configure internal-use software for its intended use are capitalized.")],
        "B",
        f"""The license ({m(lic)}) and the configuration needed to make the software ready for use ({m(cfg)}) are capitalized: {m(cap)}. Training ({m(train)}) and data conversion ({m(conv)}) are expensed. Amortization starts {date}: {m(cap)} ÷ {years} × {months}/12 = {m(amort)}. Year 1 expense = {m(amort)} + {m(train + conv)} = {m(key)}.""",
    )


def equity_method(p):
    inv, ee, fv, cost, old, new, ni, h2, div = (
        p[k] for k in ("inv", "ee", "fv", "cost", "old", "new", "ni", "h2", "div"))
    tot = old + new
    basis = fv + cost
    share = lambda pct, x: whole(D(pct) / 100 * x)
    key = basis + share(tot, h2) - share(tot, div)
    ishort, eshort = inv.split()[0], ee.split()[0]
    return variant(
        f"""{inv} owns {old}% of {ee}, carried at fair value with changes in net income; its fair value on July 1, Year 1, immediately before the purchase below, is {m(fv)}. That day {ishort} buys another {new}% of {eshort} for {m(cost)}, a price that includes a premium for obtaining significant influence. {eshort}'s net income totals {m(ni)} for Year 1 ({m(h2)} from July 1 to December 31), and {eshort} pays dividends of {m(div)} in December. Any excess of cost over {ishort}'s share of {eshort}'s book value is attributable to goodwill, which {ishort} does not amortize. At what amount should {ishort} report its investment in {eshort} at December 31, Year 1?""",
        [(m(basis - share(tot, div)), f"Deducts {ishort}'s share of the December dividend but never adds its share of {eshort}'s income."),
         (m(basis), f"Stops at the combined cost basis of {m(basis)} without applying the equity method from July 1."),
         (m(basis + share(new, h2) - share(new, div)), f"Applies only the newly purchased {new}% to {eshort}'s income and dividends. The equity method applies to {ishort}'s whole {tot}% interest from July 1."),
         (m(key), f"Correct. {m(fv)} + {m(cost)} + {tot}% × {m(h2)} − {tot}% × {m(div)}.")],
        "D",
        f"""Since ASU 2016-07, an investor that becomes eligible for the equity method adds the cost of the new interest to the current basis of its existing interest and applies the equity method prospectively, with no retroactive adjustment. Basis on July 1 = {m(fv)} + {m(cost)} = {m(basis)}. Add {tot}% of {eshort}'s income after July 1 ({m(share(tot, h2))}) and subtract {tot}% of the dividends ({m(share(tot, div))}): {m(key)}.""",
    )


def payables(p):
    co, ap, g1, util, g3, dup = (p[k] for k in ("co", "ap", "g1", "util", "g3", "dup"))
    key = ap + g1 + util - dup
    short = co.split()[0]
    return variant(
        f"""{co}'s draft December 31, Year 1, balance sheet reports accounts payable of {m(ap)}; {short} records all vendor bills, including utilities, in accounts payable. Searching for unrecorded liabilities, you examine January, Year 2, payments and invoices and find: (1) a {m(g1)} invoice for goods shipped FOB shipping point on December 22 and received December 29, not recorded until January; (2) a {m(util)} bill for December utilities, received and recorded in January; (3) a {m(g3)} invoice for goods shipped FOB destination on December 30 and received January 4; and (4) a {m(dup)} December supplier invoice that was entered twice in December. What amount should {short} report as accounts payable at December 31, Year 1?""",
        [(m(ap - dup), "Removes the duplicate invoice but adds neither of the unrecorded December liabilities."),
         (m(ap + g1 - dup), f"Adds the {m(g1)} of goods and removes the duplicate but omits the {m(util)} of December utilities, a Year 1 liability."),
         (m(key), f"Correct. {m(ap)} + {m(g1)} + {m(util)} − {m(dup)}. The FOB destination goods became {short}'s in January."),
         (m(key + g3), f"Also adds the {m(g3)} of goods shipped FOB destination. Title passed when they arrived in January, so they are a Year 2 purchase.")],
        "C",
        f"""Record the Year 1 liabilities found in the search: goods received in December ({m(g1)}; title passed at shipment in any case) and December utilities ({m(util)}). Remove the duplicated {m(dup)} invoice. Goods shipped FOB destination belong to the seller until they arrive, so the {m(g3)} is a Year 2 purchase. Accounts payable = {m(ap)} + {m(g1)} + {m(util)} − {m(dup)} = {m(key)}.""",
    )


def bonds(p):
    co, face, rate, price, date, months = (p[k] for k in ("co", "face", "rate", "price", "date", "months"))
    proceeds = whole(D(face) * price / 100)
    acc = whole(D(face) * rate / 100 * months / 12)
    short = co.split()[0]
    return variant(
        f"""On {date}, Year 1, {co} issues {m(face)} of 10-year, {rate}% bonds at {price} plus accrued interest. The bonds are dated January 1, Year 1, and pay interest each January 1 and July 1. How much cash does {short} receive at issuance?""",
        [(m(face), f"Uses the face amount only. The bonds sell at {price} of face, plus accrued interest."),
         (m(proceeds - acc), "Subtracts the accrued interest instead of adding it. Buyers pay the interest accrued since the last interest date and receive a full six months' interest on July 1."),
         (m(proceeds), f"Includes the {price - 100}% premium but not the {WORDS[months]} months of accrued interest."),
         (m(proceeds + acc), f"Correct. {m(face)} × {price}% + {m(face)} × {rate}% × {months}/12 accrued interest.")],
        "D",
        f"""Price = {m(face)} × {D(price) / 100} = {m(proceeds)}. Interest accrued from January 1 to {date} = {m(face)} × {rate}% × {months}/12 = {m(acc)}, which the buyers pay now and recover on July 1. Cash received = {m(proceeds + acc)}; {short} records the {m(acc)} as interest payable (or a reduction of interest expense).""",
    )


def gross_profit(p):
    co, bi, pur, pr, fi, sales, sr, gp, salv = (
        p[k] for k in ("co", "bi", "pur", "pr", "fi", "sales", "sr", "gp", "salv"))
    avail = bi + pur - pr + fi
    net = sales - sr
    cogs = whole(D(net) * (100 - gp) / 100)
    est = avail - cogs
    key = est - salv
    short = co.split()[0]
    return variant(
        f"""A fire on August 31 destroys most of {co}'s inventory. Records show beginning inventory of {m(bi)}, purchases of {m(pur)}, purchase returns of {m(pr)}, freight-in of {m(fi)}, sales of {m(sales)}, and sales returns of {m(sr)} through that date. {short}'s gross profit rate has been {gp}% of net sales for several years. Goods costing {m(salv)} were salvaged undamaged. Using the gross profit method, what is {short}'s estimated inventory loss?""",
        [(m(avail - whole(D(sales) * (100 - gp) / 100) - salv), f"Estimates cost of goods sold from gross sales ({m(sales)}). Sales returns reduce the sales on which cost of goods sold is based."),
         (m(key - fi), f"Leaves the {m(fi)} of freight-in out of goods available for sale. Freight-in is part of inventory cost."),
         (m(key), f"Correct. Goods available {m(avail)} − cost of goods sold {m(cogs)} ({m(net)} × {100 - gp}%) − {m(salv)} salvaged."),
         (m(est), f"Does not subtract the {m(salv)} of salvaged goods.")],
        "C",
        f"""Goods available = {m(bi)} + {m(pur)} − {m(pr)} + {m(fi)} = {m(avail)}. Net sales = {m(sales)} − {m(sr)} = {m(net)}; estimated cost of goods sold = {m(net)} × (1 − {gp}%) = {m(cogs)}. Estimated inventory at the date of the fire = {m(est)}; less {m(salv)} salvaged, the loss is {m(key)}.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def subsequent_events(p):
    co, recv, settle, accrued, inv = (p[k] for k in ("co", "recv", "settle", "accrued", "inv"))
    more = settle - accrued
    key = more + inv
    short = co.split()[0]
    return variant(
        f"""{co}'s December 31, Year 1, statements will be issued on March 10, Year 2. Between those dates: (1) on January 20, a fire destroyed the plant of a major customer, which filed for bankruptcy on January 30, making its {m(recv)} December 31 receivable uncollectible; the customer had been in good financial condition at year-end; (2) on January 15, {short} settled for {m(settle)} a lawsuit over a Year 1 accident, for which it had accrued {m(accrued)}; (3) on February 20, {short} found that its December 31 inventory count had double-counted goods costing {m(inv)}; and (4) on March 1, {short}'s board declared a cash dividend. Ignore income taxes. By how much should {short} reduce its Year 1 pretax income?""",
        [(m(key), f"Correct. {m(more)} more for the lawsuit settlement plus the {m(inv)} inventory count error."),
         (m(settle + inv), f"Charges the full {m(settle)} settlement instead of the {m(more)} not yet accrued."),
         (m(key + recv), f"Also recognizes the {m(recv)} receivable loss. The customer's problems arose from a fire after year-end, so the loss is disclosed, not recognized."),
         (m(settle + inv + recv), "Charges the full settlement and also recognizes the receivable loss.")],
        "A",
        f"""The settlement gives evidence about a Year 1 condition, so the accrual rises from {m(accrued)} to {m(settle)}: {m(more)}. The inventory double count is an error in the Year 1 statements found before issuance: {m(inv)}. The customer's bankruptcy resulted from a fire after year-end, so it is a nonrecognized event (disclosed if material), as is the dividend. Reduction = {m(key)}.""",
    )


def tax_rate_change(p):
    co, td0, new, td1 = (p[k] for k in ("co", "td0", "new", "td1"))
    old = 21
    dtl0 = whole(D(td0) * old / 100)
    end = whole(D(td1) * new / 100)
    key = end - dtl0
    short = co.split()[0]
    assert td1 > td0 and new > old
    return variant(
        f"""At December 31, Year 1, {co} has a deferred tax liability of {m(dtl0)} on {m(td0)} of taxable temporary differences, measured at the {old}% enacted rate. On November 1, Year 2, legislation is enacted raising {short}'s tax rate to {new}% for Year 3 and later years. At December 31, Year 2, {short}'s taxable temporary differences total {m(td1)}, all reversing in Year 3 or later. What deferred income tax expense should {short} recognize for Year 2?""",
        [(m(whole(D(td1) * old / 100) - dtl0), f"Measures the ending liability at the old {old}% rate. Deferred taxes are measured at the enacted rate for the years the differences reverse."),
         (m(whole(D(td1 - td0) * new / 100)), f"Applies the new rate only to the {m(td1 - td0)} of new differences and does not remeasure the beginning liability for the rate change."),
         (m(key), f"Correct. Ending liability {m(td1)} × {new}% = {m(end)}, less the {m(dtl0)} beginning balance."),
         (m(end), f"Reports the ending deferred tax liability as the year's expense, ignoring the {m(dtl0)} already recorded.")],
        "C",
        f"""Deferred tax liabilities are measured at the enacted rate expected to apply when the differences reverse, and the effect of a rate change is recognized in income from continuing operations in the period of enactment. Ending liability = {m(td1)} × {new}% = {m(end)}. Deferred tax expense = {m(end)} − {m(dtl0)} = {m(key)} (including {m(whole(D(td0) * (new - old) / 100))} from remeasuring the beginning differences).""",
    )


def contract_modification(p):
    co, units, price, done, added, add_price, ssp = (
        p[k] for k in ("co", "units", "price", "done", "added", "add_price", "ssp"))
    rem = units - done
    key = D(rem * price + added * add_price) / (rem + added)
    cum = D(units * price + added * add_price) / (units + added)
    key, cum = whole(key), whole(cum)
    short = co.split()[0]
    return variant(
        f"""{co} contracts to deliver {units} identical standard units to a customer over six months for {m(price)} per unit; the customer can use each unit on its own as it is delivered. After {done} units are delivered, the parties modify the contract to add {added} more units at {m(add_price)} each; {short}'s standalone selling price for the units is {m(ssp)} at that time, and the discount does not reflect any cost savings or other reason tied to the added units. What revenue per unit should {short} recognize for each of the {rem + added} units delivered after the modification?""",
        [(m(add_price), "Uses the price of the added units for all remaining units."),
         (m(key), f"Correct. The modification is accounted for prospectively: ({rem} × {m(price)} + {added} × {m(add_price)}) ÷ {rem + added} units."),
         (m(cum), f"Applies a cumulative catch-up by blending all {units + added} units, including the {done} already delivered. When the remaining goods are distinct, the modification is prospective."),
         (m(price), f"Keeps {m(price)} for the original units and treats the added units as a separate contract. That applies only when the added units are priced at their standalone selling price.")],
        "B",
        f"""The added units are distinct but not priced at standalone selling price, so the modification is not a separate contract. Because the remaining units are distinct from those already delivered, {short} treats it as terminating the old contract and creating a new one: the remaining consideration ({rem} × {m(price)} + {added} × {m(add_price)} = {m(rem * price + added * add_price)}) is allocated to the {rem + added} remaining units, {m(key)} each.""",
    )


# Parameter set 0 reproduces the reviewed item; sets 1-3 are the new variants.
FAMILIES = {
    "far-foreign-currency-transactions-0001": (foreign_currency, [
        dict(co="Abbott Co.", eur=100000, r0="1.10", r1="1.14", r2="1.12"),
        dict(co="Garvey Co.", eur=250000, r0="1.08", r1="1.13", r2="1.10"),
        dict(co="Holt Co.", eur=80000, r0="1.05", r1="1.11", r2="1.07"),
        dict(co="Ingram Co.", eur=300000, r0="1.12", r1="1.15", r2="1.13"),
    ]),
    "far-performance-metrics-0002": (performance_metrics, [
        dict(co="Brand Co.", rev=5000000, ni=400000, int=100000, tax=120000, da=280000, a0=3800000, a1=4200000),
        dict(co="Corbin Co.", rev=6300000, ni=520000, int=140000, tax=160000, da=330000, a0=4600000, a1=5400000),
        dict(co="Dover Co.", rev=2880000, ni=210000, int=60000, tax=70000, da=150000, a0=2200000, a1=2600000),
        dict(co="Ellery Co.", rev=9000000, ni=700000, int=250000, tax=210000, da=540000, a0=5500000, a1=6500000),
    ]),
    "far-balance-sheet-0004": (balance_sheet, [
        dict(co="Dale Co.", bonds=1500000, lease=400000, dtl=150000, warr=50000, bond_cur=300000, lease_cur=60000),
        dict(co="Fenwick Co.", bonds=2000000, lease=600000, dtl=90000, warr=70000, bond_cur=400000, lease_cur=110000),
        dict(co="Gale Co.", bonds=900000, lease=250000, dtl=120000, warr=40000, bond_cur=150000, lease_cur=45000),
        dict(co="Harlow Co.", bonds=3200000, lease=480000, dtl=210000, warr=85000, bond_cur=800000, lease_cur=95000),
    ]),
    "far-cash-flows-0007": (cash_flows, [
        dict(co="Eads Co.", ni=300000, dep=50000, disc=4000, dtl=12000, gain=25000, ap=18000, inv=22000, stock=100000),
        dict(co="Farrow Co.", ni=420000, dep=75000, disc=6000, dtl=9000, gain=30000, ap=24000, inv=35000, stock=150000),
        dict(co="Grady Co.", ni=250000, dep=40000, disc=3000, dtl=15000, gain=18000, ap=11000, inv=28000, stock=80000),
        dict(co="Hume Co.", ni=510000, dep=90000, disc=5000, dtl=20000, gain=42000, ap=16000, inv=47000, stock=200000),
    ]),
    "far-consolidated-statements-0006": (consolidation, [
        dict(par="Pym Corp.", sub="Tovey Inc.", ta=4200000, loan=500000, rate=6, date="July 1", due="June 30", months=6),
        dict(par="Quill Corp.", sub="Ramsey Inc.", ta=6800000, loan=800000, rate=5, date="April 1", due="March 31", months=9),
        dict(par="Sutter Corp.", sub="Vane Inc.", ta=3100000, loan=400000, rate=9, date="September 1", due="August 31", months=4),
        dict(par="Wexford Corp.", sub="Yates Inc.", ta=5500000, loan=1200000, rate=4, date="May 1", due="April 30", months=8),
    ]),
    "far-software-purchased-0001": (software, [
        dict(co="Hart Co.", lic=240000, cfg=60000, train=15000, conv=10000, date="April 1", months=9, years=5),
        dict(co="Kemp Co.", lic=360000, cfg=90000, train=20000, conv=12000, date="July 1", months=6, years=5),
        dict(co="Lister Co.", lic=180000, cfg=45000, train=9000, conv=6000, date="March 1", months=10, years=4),
        dict(co="Marsh Co.", lic=420000, cfg=60000, train=18000, conv=12000, date="October 1", months=3, years=6),
    ]),
    "far-equity-method-0002": (equity_method, [
        dict(inv="Jade Co.", ee="Varro Inc.", fv=150000, cost=330000, old=10, new=20, ni=380000, h2=200000, div=50000),
        dict(inv="Keel Co.", ee="Winton Inc.", fv=90000, cost=260000, old=15, new=25, ni=500000, h2=240000, div=80000),
        dict(inv="Lark Co.", ee="Ashby Inc.", fv=90000, cost=410000, old=5, new=20, ni=300000, h2=180000, div=60000),
        dict(inv="Moss Co.", ee="Bexley Inc.", fv=120000, cost=300000, old=10, new=15, ni=440000, h2=260000, div=100000),
    ]),
    "far-payables-cutoff-0001": (payables, [
        dict(co="Kirk Co.", ap=620000, g1=21000, util=9000, g3=25000, dup=12000),
        dict(co="Lowe Co.", ap=840000, g1=33000, util=14000, g3=40000, dup=18000),
        dict(co="Mercer Co.", ap=455000, g1=16000, util=7000, g3=22000, dup=10000),
        dict(co="Nash Co.", ap=1230000, g1=48000, util=21000, g3=36000, dup=27000),
    ]),
    "far-bonds-between-interest-dates-0001": (bonds, [
        dict(co="Lamb Co.", face=1000000, rate=6, price=102, date="April 1", months=3),
        dict(co="Nolan Co.", face=2000000, rate=6, price=101, date="May 1", months=4),
        dict(co="Orton Co.", face=600000, rate=8, price=103, date="March 1", months=2),
        dict(co="Pryor Co.", face=3000000, rate=4, price=102, date="June 1", months=5),
    ]),
    "far-inventory-gross-profit-method-0001": (gross_profit, [
        dict(co="Mosley Co.", bi=200000, pur=800000, pr=20000, fi=10000, sales=1100000, sr=50000, gp=30, salv=15000),
        dict(co="Norris Co.", bi=320000, pur=1150000, pr=30000, fi=18000, sales=1700000, sr=60000, gp=35, salv=22000),
        dict(co="Oakes Co.", bi=150000, pur=620000, pr=12000, fi=8000, sales=900000, sr=40000, gp=25, salv=10000),
        dict(co="Penrose Co.", bi=410000, pur=1480000, pr=25000, fi=15000, sales=2200000, sr=100000, gp=40, salv=30000),
    ]),
    "far-subsequent-events-0004": (subsequent_events, [
        dict(co="Owen Co.", recv=60000, settle=90000, accrued=50000, inv=25000),
        dict(co="Parish Co.", recv=85000, settle=140000, accrued=100000, inv=32000),
        dict(co="Quincy Co.", recv=45000, settle=70000, accrued=55000, inv=18000),
        dict(co="Rowan Co.", recv=120000, settle=210000, accrued=150000, inv=40000),
    ]),
    "far-income-taxes-rate-change-0001": (tax_rate_change, [
        dict(co="Tyne Co.", td0=200000, new=25, td1=260000),
        dict(co="Usher Co.", td0=300000, new=24, td1=340000),
        dict(co="Vickers Co.", td0=180000, new=23, td1=240000),
        dict(co="Warde Co.", td0=500000, new=26, td1=580000),
    ]),
    "far-revenue-contract-modification-0001": (contract_modification, [
        dict(co="Reed Co.", units=120, price=100, done=50, added=30, add_price=80, ssp=95),
        dict(co="Selby Co.", units=150, price=150, done=90, added=60, add_price=108, ssp=142),
        dict(co="Tolland Co.", units=80, price=75, done=50, added=20, add_price=55, ssp=70),
        dict(co="Upshaw Co.", units=240, price=120, done=90, added=60, add_price=85, ssp=115),
    ]),
}


def same_as_reviewed(item, v):
    """Parameter set 0 must rebuild the reviewed item exactly (choices in any order)."""
    problems = []
    for k in ("stem", "explanation"):
        if v[k] != item[k]:
            problems.append(k)
    pairs = lambda x: {(c["text"], c["rationale"]) for c in x["choices"]}
    if pairs(v) != pairs(item):
        problems.append("choices")
    key = lambda x: next(c["text"] for c in x["choices"] if c["id"] == x["answer"])
    if key(v) != key(item):
        problems.append("answer")
    return problems


def main():
    items, failed = [], False
    for item_id, (build, params) in FAMILIES.items():
        path = os.path.join(CONTENT, item_id + ".yaml")
        with open(path, encoding="utf-8") as f:
            item = yaml.safe_load(f)
        problems = same_as_reviewed(item, build(params[0]))
        if problems:
            print(f"FAIL {item_id}: parameter set 0 does not rebuild the reviewed item ({', '.join(problems)})",
                  file=sys.stderr)
            failed = True
            continue
        attach_variants(item, [build(p) for p in params[1:]])
        items.append((path, item))
    if failed:
        sys.exit(1)
    warnings = audit([it for _, it in items])
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    for path, item in items:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(item, f, sort_keys=False, allow_unicode=True, width=100)
    print(f"added {sum(len(it['variants']) for _, it in items)} variants to {len(items)} items")


if __name__ == "__main__":
    main()
