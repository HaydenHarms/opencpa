"""FAR batch 11 — 25 items written from scratch: a second item on six Area III Remembering and Understanding
tasks (III.B.a, III.C.a, III.C.b, III.D.a, III.F.a, III.F.b), a second item on nine Application tasks (I.A.1a,
I.A.2a, I.A.5a, I.B.1b, I.B.2b, II.B.a, II.D.a, II.E.2b, II.G.b), and a further item on ten Analysis tasks
(changes in equity, cash flows, the cash, receivables, inventory and PP&E reconciliations and rollforwards,
error corrections and subsequent events), each in a format the task's existing items don't use.
Target skill mix 6 / 9 / 10; area mix 8 / 9 / 8. Scope and skill tags follow the AICPA CPA Exam Blueprints
effective January 2026.

Numeric items ship with three variants each (method as in far-batch-10.py): each item is a builder, parameter
set 0 is the item and sets 1-3 are its variants, and every family must move the key's letter.

Run: python3 scripts/batches/far-batch-11.py   See docs/reviews/far-batch-11.md.
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import os
import re
import sys
from decimal import Decimal as D

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import AN, AP, RU, attach_variants, audit, finalize, fix_articles, mcq as _mcq, variant, write_items  # noqa: E402
from variants import m, pick, rd  # noqa: E402

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 11. Written from scratch; answers solved and every number and distractor computed in code."
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
    for n, v in enumerate([it] + it["_variants"]):
        repeats(f"{id} v{n}", v)
    return it


def repeats(label, v):
    """Report any dollar amount that appears more than once in a stem, or a choice that equals a stem amount.

    A repeat is fine only when it names the same fact twice; the lead reviews every line this prints."""
    amts = re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", v["stem"])
    dup = sorted({a for a in amts if amts.count(a) > 1})
    if dup:
        print(f"REPEAT {label}: stem repeats {', '.join(dup)}", file=sys.stderr)
    for c in v["choices"]:
        for a in re.findall(r"[$][0-9,]+(?:[.][0-9]+)?", c["text"]):
            if a in amts:
                print(f"REPEAT {label}: choice {a} equals a stem amount", file=sys.stderr)


def short(name):
    return name.split()[0]


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole amount, got {x}"
    return x


def distinct(pool, key):
    """No pool value may equal the key or another pool value; amounts must be positive."""
    vals = [t for t, _ in pool.values()] + [key[0]]
    assert len(set(vals)) == len(vals), f"coinciding choices: {vals}"
    assert all(not v.startswith("$-") and not v.startswith("$0 ") and v != "$0" for v in vals), vals


def build(pool, key, use):
    distinct(pool, key)
    return pick(pool, key, use)


# ── Area I ───────────────────────────────────────────────────────────────


def bs_current_liabilities(p):
    co, s = p["co"], short(p["co"])
    key_v = p["ap"] + p["ai"] + p["cb"] + p["Lc"] + p["Wc"] + p["ur"]
    pool = {
        "sdd": (m(key_v + p["sdd"]), f"Includes the {m(p['sdd'])} of common stock dividend distributable. A stock dividend is settled by issuing shares, not by paying assets, so the amount is part of stockholders' equity until the shares are issued."),
        "no_cb": (m(key_v - p["cb"]), f"Leaves the {m(p['cb'])} of customer credit balances netted against accounts receivable. Amounts {s} owes customers are liabilities, reported among current liabilities; receivables are reported at the {m(p['dr'])} of debit balances."),
        "lease_all": (m(key_v + p["LL"] - p["Lc"]), f"Reports the whole {m(p['LL'])} operating lease liability as current. Only the {m(p['Lc'])} reduction of the liability that the next twelve months' payments will make is current; the rest is noncurrent."),
        "warr_all": (m(key_v + p["W"] - p["Wc"]), f"Reports the whole {m(p['W'])} warranty liability as current. Only the {m(p['Wc'])} of claims expected to be settled within the next twelve months is current."),
        "lease_none": (m(key_v - p["Lc"]), f"Reports all of the operating lease liabilities as noncurrent. The {m(p['Lc'])} that the Year 3 lease payments will settle is a current liability."),
        "warr_none": (m(key_v - p["Wc"]), f"Reports all of the warranty liability as noncurrent. The {m(p['Wc'])} of claims expected to be settled in Year 3 is a current liability."),
        "dtl": (m(key_v + p["dtl"]), f"Includes the {m(p['dtl'])} deferred tax liability. Deferred tax liabilities are classified as noncurrent in a classified balance sheet."),
    }
    key = (m(key_v), f"Correct. {m(p['ap'])} + {m(p['ai'])} + {m(p['cb'])} + {m(p['Lc'])} + {m(p['Wc'])} + {m(p['ur'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} is preparing a classified balance sheet at December 31, Year 2. Its adjusted trial balance and supporting schedules show: accounts payable {m(p['ap'])}; interest payable {m(p['ai'])}; accounts receivable of {m(p['dr'] - p['cb'])}, which is the net of customer accounts with debit balances of {m(p['dr'])} and customer accounts with credit balances of {m(p['cb'])} from overpayments; common stock dividend distributable of {m(p['sdd'])}, for a 5% stock dividend declared on December 15 and to be distributed on January 20, Year 3; operating lease liabilities of {m(p['LL'])}, of which the lease payments due in Year 3 will settle {m(p['Lc'])}; an estimated liability for product warranties of {m(p['W'])}, of which {m(p['Wc'])} relates to claims expected to be settled in Year 3; unearned service revenue of {m(p['ur'])} for services to be performed by June, Year 3; and a deferred tax liability of {m(p['dtl'])}. What total current liabilities should {s} report?""",
        choices, ans,
        f"""Current liabilities are obligations expected to be settled with current assets (or by creating other current liabilities) within a year. They are accounts payable {m(p['ap'])}, interest payable {m(p['ai'])}, the {m(p['cb'])} of customer credit balances (amounts owed to customers, reclassified out of receivables), the {m(p['Lc'])} current portion of the operating lease liabilities, the {m(p['Wc'])} of warranty claims expected to be settled in Year 3, and the {m(p['ur'])} of unearned revenue for services due within the year: {m(key_v)} in all. The stock dividend distributable is equity, because it will be settled in shares, and the deferred tax liability is noncurrent.""",
    )


def is_operating_income(p):
    co, s = p["co"], short(p["co"])
    key_v = p["S"] - p["sr"] - p["sd"] - p["cg"] - p["se"] - p["ga"] - p["imp"] + p["gs"]
    pool = {
        "no_imp": (m(key_v + p["imp"]), f"Reports the {m(p['imp'])} impairment loss below income from operations. An impairment loss on a long-lived asset held and used is included in income from continuing operations before income taxes, and in a subtotal such as income from operations when one is presented (ASC 360-10-45-4)."),
        "no_gain": (m(key_v - p["gs"]), f"Reports the {m(p['gs'])} gain on the sale of equipment as other income, below income from operations. A gain on the sale of a long-lived asset that isn't a discontinued operation is included in a subtotal such as income from operations when one is presented (ASC 360-10-45-5). The textbook layout that puts such gains under other gains and losses, below operating income doesn't comply once {s} presents that subtotal."),
        "int": (m(key_v - p["ie"]), f"Deducts the {m(p['ie'])} of interest expense. Interest is a financing cost, reported after income from operations."),
        "div": (m(key_v + p["dv"]), f"Adds the {m(p['dv'])} of dividend revenue. Investment income from equity securities is reported after income from operations."),
        "disc": (m(key_v - p["ld"]), f"Deducts the {m(p['ld'])} loss of the discontinued component. Discontinued operations are reported separately, after income from continuing operations, net of tax."),
    }
    key = (m(key_v), f"Correct. {m(p['S'])} − {m(p['sr'])} − {m(p['sd'])} − {m(p['cg'])} − {m(p['se'])} − {m(p['ga'])} − {m(p['imp'])} + {m(p['gs'])}. ASC 360-10-45-4 and 45-5 put the impairment loss and the gain on the sale inside income from operations when that subtotal is presented.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s adjusted trial balance for Year 3 includes these pretax amounts: sales {m(p['S'])}; sales returns and allowances {m(p['sr'])}; sales discounts {m(p['sd'])}; cost of goods sold {m(p['cg'])}; selling expenses, including freight on shipments to customers, {m(p['se'])}; general and administrative expenses {m(p['ga'])}; a loss of {m(p['imp'])} from writing down a warehouse that {s} continues to use to its fair value; a gain of {m(p['gs'])} on the sale of delivery equipment; interest expense {m(p['ie'])}; dividend revenue {m(p['dv'])}; and a loss of {m(p['ld'])} from operating its {p['seg']} division, a business segment that {s} sold in September, Year 3, after deciding to leave that business. {s} presents a multi-step income statement that includes a subtotal for income from operations. What income from operations should it report for Year 3?""",
        choices, ans,
        f"""Net sales = {m(p['S'])} − {m(p['sr'])} − {m(p['sd'])} = {m(p['S'] - p['sr'] - p['sd'])}. Gross profit = net sales − {m(p['cg'])} = {m(p['S'] - p['sr'] - p['sd'] - p['cg'])}. Operating expenses are the selling expenses (freight-out included), general and administrative expenses and the {m(p['imp'])} impairment loss on the warehouse held and used; the {m(p['gs'])} gain on the equipment sale is also included, because ASC 360-10-45-4 and 45-5 require impairment losses and gains or losses on sales of long-lived assets that aren't discontinued operations to be included in a subtotal such as income from operations. Income from operations = {m(key_v)}. Interest expense and dividend revenue are nonoperating, and the {p['seg']} division's loss is reported in discontinued operations.""",
    )


def taxes_paid(p):
    co, s = p["co"], short(p["co"])
    dtp = p["TP1"] - p["TP0"]
    n = p["DTL1"] - p["DTL0"] - p["oci"]
    a = p["DTA1"] - p["DTA0"]
    assert dtp > 0 and n > 0 and a > 0
    deferred = n - a
    current = p["E"] - deferred
    key_v = current - dtp
    pool = {
        "oci_in": (m(key_v - p["oci"]), f"Treats the whole {m(p['DTL1'] - p['DTL0'])} increase in the deferred tax liability as deferred tax expense. {m(p['oci'])} of it was charged to other comprehensive income with the unrealized gains on available-for-sale securities, so it isn't part of income tax expense."),
        "no_def": (m(key_v + deferred), f"Ignores deferred taxes, taking all {m(p['E'])} of income tax expense as current. Deferred tax expense of {m(deferred)} involves no payment to the tax authorities."),
        "tp_sign": (m(key_v + 2 * dtp), f"Adds the {m(dtp)} increase in income taxes payable. A rise in the payable means less was paid than the current tax expense."),
        "dta_sign": (m(key_v - 2 * a), f"Adds the {m(a)} increase in the deferred tax asset to deferred tax expense. An increase in a deferred tax asset is a deferred tax benefit, which reduces deferred tax expense."),
        "current": (m(key_v + dtp), f"Reports current income tax expense of {m(current)} as the amount paid. The {m(dtp)} increase in income taxes payable was not paid during Year 2."),
    }
    key = (m(key_v), f"Correct. {m(p['E'])} − {m(deferred)} deferred = {m(current)} current; {m(current)} − {m(dtp)} increase in taxes payable.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} reports income tax expense of {m(p['E'])} in its Year 2 income statement. Its balance sheets show income taxes payable of {m(p['TP0'])} at January 1, Year 2, and {m(p['TP1'])} at December 31; a deferred tax liability of {m(p['DTL0'])} and {m(p['DTL1'])}; and a deferred tax asset, with no valuation allowance, of {m(p['DTA0'])} and {m(p['DTA1'])}. Of the increase in the deferred tax liability, {m(p['oci'])} arose from unrealized holding gains on available-for-sale debt securities and was charged to other comprehensive income. {s} has no other tax balances and made no other tax entries. What amount should {s} disclose as income taxes paid for Year 2 in its statement of cash flows, which uses the indirect method?""",
        choices, ans,
        f"""Deferred tax expense is the change in deferred tax balances that runs through income: the deferred tax liability rose by {m(p['DTL1'] - p['DTL0'])}, of which {m(p['oci'])} was charged to OCI, leaving {m(n)}; less the {m(a)} increase in the deferred tax asset, a benefit: {m(n)} − {m(a)} = {m(deferred)}. Current tax expense = {m(p['E'])} − {m(deferred)} = {m(current)}. Income taxes payable rose by {m(dtp)}, so less was paid than the current expense: taxes paid = {m(current)} − {m(dtp)} = {m(key_v)}. ASC 230-10-50-2 requires an entity using the indirect method to disclose income taxes paid.""",
    )


def nfp_without(p):
    org, s = p["org"], short(p["org"])
    with_v = p["F"] + p["R"] + p["P"]
    key_v = p["TA"] - p["TL"] - with_v
    assert p["F"] < p["G"] and key_v > p["BD"]
    pool = {
        "old_rule": (m(key_v - (p["G"] - p["F"])), f"Charges the {m(p['G'] - p['F'])} by which the endowment has fallen below the original gift to net assets without donor restrictions. That was the rule before ASU 2016-14; now an underwater endowment fund stays in net assets with donor restrictions at its fair value."),
        "bd": (m(key_v - p["BD"]), f"Leaves out the {m(p['BD'])} that the board set aside as a quasi-endowment. A board designation is a self-imposed limit that the board can reverse; the amount stays in net assets without donor restrictions."),
        "ra": (m(key_v + p["ra"]), f"Treats the {m(p['ra'])} grant advance as unrestricted contribution revenue. The grant is conditional on {s} incurring qualifying costs, which it hasn't done, so the advance is a refundable advance (a liability)."),
        "total": (m(key_v + with_v), f"Reports total net assets, {m(p['TA'])} − {m(p['TL'])}. The {m(with_v)} of donor-restricted amounts is reported separately as net assets with donor restrictions."),
    }
    key = (m(key_v), f"Correct. {m(p['TA'])} − {m(p['TL'])} − ({m(p['F'])} + {m(p['R'])} + {m(p['P'])}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At June 30, Year 2, {org}, a not-for-profit entity, has total assets of {m(p['TA'])} and total liabilities of {m(p['TL'])}. The assets include an endowment fund created with gifts of {m(p['G'])} that donors require {s} to hold in perpetuity, now invested in securities with a fair value of {m(p['F'])} after a market decline; {m(p['R'])} of unspent cash gifts that donors restricted to a reading program for adults; {m(p['P'])} of unconditional pledges, due in Year 3, that donors restricted to buying a bookmobile; and {m(p['BD'])} of investments that {s}'s board has set aside to function as an endowment. The liabilities include {m(p['ra'])} that a foundation paid in advance under a grant that it will pay only to the extent {s} incurs costs for a new tutoring program and that {s} must return otherwise; {s} has incurred none of those costs. What amount should {s} report as net assets without donor restrictions at June 30, Year 2?""",
        choices, ans,
        f"""Net assets with donor restrictions are the endowment at its {m(p['F'])} fair value (under ASU 2016-14 an underwater endowment fund is reported in net assets with donor restrictions, and the shortfall below the original gift is disclosed), the {m(p['R'])} of purpose-restricted gifts and the {m(p['P'])} of restricted pledges: {m(with_v)}. The board-designated quasi-endowment is a self-imposed limit, so it remains without donor restrictions, and the conditional grant advance is a refundable advance, already in liabilities. Net assets without donor restrictions = {m(p['TA'])} − {m(p['TL'])} − {m(with_v)} = {m(key_v)}.""",
    )


def nfp_with_change(p):
    org, s = p["org"], short(p["org"])
    key_v = p["c1"] + p["c2"] + p["re"] + p["pl"] - p["e1"] - p["q"] - p["a"]
    assert key_v > 0 and p["q"] <= p["c2"] and p["e1"] <= p["c1"]
    inc = lambda x: f"{m(x)} increase"
    pool = {
        "no_release_eq": (inc(key_v + p["q"]), f"Keeps the {m(p['q'])} spent on the van in net assets with donor restrictions. The donor's restriction was met when {s} bought the van and placed it in service; since ASU 2016-14, an NFP can't imply a further time restriction over the asset's life."),
        "c2_wo": (inc(key_v - p["c2"] + p["q"]), f"Reports the {m(p['c2'])} van gift as without donor restrictions, so neither the gift nor its release passes through net assets with donor restrictions. The donor restricted the gift to buying a van, so it is with donor restrictions until the van is placed in service, and the {m(p['c2'] - p['q'])} not spent stays restricted."),
        "cond": (inc(key_v + p["cp"]), f"Includes the {m(p['cp'])} matching pledge. It is conditional: the donor pays only if {s} raises matching gifts, which hasn't happened, so no revenue is recognized yet."),
        "pledge_wo": (inc(key_v - p["pl"]), f"Reports the {m(p['pl'])} pledge payable next year as without donor restrictions. An unconditional promise payable in a future period carries an implied time restriction, unless the donor says it is for the current period's activities."),
        "endow_wo": (inc(key_v - p["re"] + p["a"]), f"Reports the {m(p['re'])} return on the donor-restricted endowment as without donor restrictions, so the {m(p['a'])} appropriated and spent is never released from net assets with donor restrictions either. Return on a donor-restricted endowment fund is with donor restrictions until the board appropriates it for spending."),
        "no_approp": (inc(key_v + p["a"]), f"Leaves out the release of the {m(p['a'])} of endowment return that the board appropriated and spent. Appropriation and spending for the stated purpose release the amount from restriction."),
    }
    key = (inc(key_v), f"Correct. {m(p['c1'])} + {m(p['c2'])} + {m(p['re'])} + {m(p['pl'])} − {m(p['e1'])} − {m(p['q'])} − {m(p['a'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""During Year 2, {org}, a not-for-profit entity, received {m(p['c1'])} in cash gifts restricted by donors to its meals-on-wheels program and spent {m(p['e1'])} on that program, and received a {m(p['c2'])} cash gift restricted to buying a delivery van, which it bought for {m(p['q'])} and placed in service in August. Its donor-restricted endowment earned a total return of {m(p['re'])}; the board appropriated {m(p['a'])} of the endowment's return for the general operating purposes the endowment's donors specified, and {s} spent it in Year 2. A donor made an unconditional pledge of {m(p['pl'])}, payable in Year 3, and stated no purpose. Another donor promised {m(p['cp'])} if {s} raises the same amount in new gifts by March, Year 3; it has raised very little so far. What is the net change in {s}'s net assets with donor restrictions for Year 2?""",
        choices, ans,
        f"""Increases: program gifts {m(p['c1'])}, the van gift {m(p['c2'])}, the endowment return {m(p['re'])} (with donor restrictions until appropriated) and the {m(p['pl'])} pledge, which carries an implied time restriction because it is payable in Year 3. Releases: {m(p['e1'])} spent on the program, {m(p['q'])} for the van (the restriction is met when the asset is placed in service), and the {m(p['a'])} of endowment return appropriated and spent. The conditional matching pledge isn't recognized. Net change = {m(p['c1'] + p['c2'] + p['re'] + p['pl'])} − {m(p['e1'] + p['q'] + p['a'])} = {m(key_v)} increase.""",
    )


# ── Area I Analysis ──────────────────────────────────────────────────────


def aoci_discrepancies(p):
    co, s = p["co"], short(p["co"])
    draft_oci = p["gA"] + p["gE"] - p["dZ"]
    draft = p["B"] + draft_oci
    key_v = p["B"] + p["gA"] - (p["dZ"] - p["c"]) - p["r"]
    assert 0 < p["c"] < p["dZ"] and key_v > 0
    pool = {
        "eq": (m(key_v + p["gE"]), f"Leaves the {m(p['gE'])} increase in the fair value of the equity securities in OCI. Changes in the fair value of equity securities with readily determinable fair values are reported in net income."),
        "no_reclass": (m(key_v + p["r"]), f"Leaves the {m(p['r'])} of unrealized gain on the bonds sold in accumulated OCI. When a gain on an available-for-sale security is realized in net income, a reclassification adjustment removes it from accumulated OCI."),
        "credit_oci": (m(key_v - p["c"]), f"Leaves the {m(p['c'])} credit loss in OCI. For an available-for-sale debt security, the credit loss is recorded through an allowance and net income; only the {m(p['dZ'] - p['c'])} of the decline not due to credit goes to OCI."),
        "all_credit": (m(key_v + p["dZ"] - p["c"]), f"Removes the whole {m(p['dZ'])} decline on the {p['zb']} bond from OCI. Only the {m(p['c'])} credit loss goes to net income; the rest of the decline is an unrealized loss in OCI."),
        "draft": (m(draft), f"Accepts the draft. It includes the equity securities' gain, puts the whole decline on the {p['zb']} bond in OCI and makes no reclassification for the bonds sold."),
    }
    key = (m(key_v), f"Correct. {m(p['B'])} + {m(p['gA'])} − ({m(p['dZ'])} − {m(p['c'])}) − {m(p['r'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 statement of changes in stockholders' equity shows accumulated other comprehensive income (AOCI) of {m(p['B'])} at January 1 plus other comprehensive income of {m(draft_oci)}, giving {m(draft)} at December 31. The OCI line is the net change in the fair value of all of {s}'s securities during Year 2: an increase of {m(p['gA'])} in its portfolio of available-for-sale corporate bonds; an increase of {m(p['gE'])} in the common shares it holds, which have readily determinable fair values; and a decrease of {m(p['dZ'])} in a {p['zb']} bond, classified as available for sale, that {s} bought at par in March, Year 2. {s}'s analysis of the cash flows it expects to collect from {p['zb']} puts the expected credit loss on that bond at {m(p['c'])}; {s} does not intend to sell the bond and is not likely to be required to sell it before recovery. The supporting schedules also show that in November, {s} sold available-for-sale bonds whose fair value had not changed during Year 2; their unrealized gain of {m(p['r'])}, included in AOCI at January 1, was reported in Year 2 net income as a realized gain. Ignore income taxes. What AOCI should {s}'s corrected statement report at December 31, Year 2?""",
        choices, ans,
        f"""Corrected OCI for Year 2: the {m(p['gA'])} unrealized gain on the available-for-sale portfolio; the {p['zb']} bond's decline less its credit loss, − ({m(p['dZ'])} − {m(p['c'])}) = − {m(p['dZ'] - p['c'])}, because the {m(p['c'])} credit loss is recognized in net income through an allowance; and a reclassification adjustment of − {m(p['r'])} for the gain realized on the bonds sold. The {m(p['gE'])} gain on the equity securities belongs in net income. AOCI = {m(p['B'])} + {m(p['gA'])} − {m(p['dZ'] - p['c'])} − {m(p['r'])} = {m(key_v)}.""",
    )


def scf_financing_discrepancies(p):
    co, s = p["co"], short(p["co"])
    F = p["Bp"] - p["T"] - p["L"] - p["Dv"] + p["M"]
    O, I = p["O"], -(p["Eq"] + p["Bld"])
    N = O + I + F
    key_v = F - p["pen"] + p["i"] - p["M"]
    assert key_v > 0 and N > 0
    pool = {
        "no_pen": (m(key_v + p["pen"]), f"Leaves the {m(p['pen'])} prepayment penalty out of financing activities. Cash paid for debt prepayment or extinguishment costs is a financing outflow, so the operating section adds it back and the financing section reports it."),
        "no_int": (m(key_v - p["i"]), f"Keeps all {m(p['L'])} of finance lease payments in financing activities. The {m(p['i'])} interest portion is an operating outflow; only the principal portion is financing."),
        "keep_m": (m(key_v + p["M"]), f"Keeps the {m(p['M'])} mortgage assumed on the building as a financing inflow. No cash was borrowed: assuming the seller's mortgage is a noncash investing and financing activity, disclosed rather than reported in the statement."),
        "lease_out": (m(key_v + p["L"] - p["i"]), f"Moves all {m(p['L'])} of finance lease payments out of financing activities. Only the {m(p['i'])} interest portion is operating; the {m(p['L'] - p['i'])} of principal repayments is financing."),
    }
    key = (m(key_v), f"Correct. {m(F)} − {m(p['pen'])} + {m(p['i'])} − {m(p['M'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft Year 2 statement of cash flows reports net cash provided by operating activities of {m(O)}, net cash used in investing activities of {m(-I)} (purchases of equipment {m(p['Eq'])} and purchase of an office building {m(p['Bld'])}), and net cash provided by financing activities of {m(F)} (proceeds from bonds issued, net of issue costs paid, {m(p['Bp'])}; repayment of a term loan ({m(p['T'])}); payments on finance lease obligations ({m(p['L'])}); dividends paid ({m(p['Dv'])}); and mortgage loan on office building {m(p['M'])}), for a net increase in cash of {m(N)}. The supporting documents show: the seller of the building received {m(p['Bld'] - p['M'])} in cash, and {s} assumed the seller's {m(p['M'])} mortgage for the rest of the price; besides the {m(p['T'])} of principal, {s} paid the term lender a {m(p['pen'])} prepayment penalty, which net income includes as a loss on extinguishment and which the operating section does not adjust; and the finance lease payments consisted of {m(p['L'] - p['i'])} of principal and {m(p['i'])} of interest. Under U.S. GAAP, what should the corrected statement report as net cash provided by financing activities?""",
        choices, ans,
        f"""Three items in the financing section need correcting. The mortgage was assumed, not borrowed, so the {m(p['M'])} inflow is removed (and the building's cash purchase price falls to {m(p['Bld'] - p['M'])}); the assumption is disclosed as a noncash activity. The {m(p['pen'])} prepayment penalty is a cash outflow for debt extinguishment costs, which ASC 230-10-45-15 classifies as financing, so it moves out of operating activities (where it is added back) into financing. Of the {m(p['L'])} paid on finance leases, the {m(p['i'])} of interest is operating (ASC 842-20-45-5), so financing outflows fall by {m(p['i'])}. The bond proceeds, net of the issue costs paid, are correctly financing. Corrected financing = {m(F)} − {m(p['M'])} − {m(p['pen'])} + {m(p['i'])} = {m(key_v)}.""",
    )


def suppliers_paid(p):
    co, s = p["co"], short(p["co"])
    dinv = p["I1"] - p["I0"]
    dap = p["P1"] - p["P0"]
    assert dinv > 0 and dap > 0
    purch = p["C"] + dinv
    key_v = purch - dap - p["nt"]
    pool = {
        "wd": (m(key_v - p["wd"]), f"Deducts the {m(p['wd'])} write-down as a noncash part of cost of goods sold. Ending inventory is already net of the write-down, so cost of goods sold + ending inventory − beginning inventory gives purchases without any further adjustment."),
        "no_note": (m(key_v + p["nt"]), f"Treats the {m(p['nt'])} of payables settled by issuing a note as paid in cash. The note replaced the payable without cash changing hands; it is a noncash transaction."),
        "ap_sign": (m(key_v + 2 * dap), f"Adds the {m(dap)} increase in accounts payable. A rise in payables means {s} paid less than it bought."),
        "inv_sign": (m(key_v - 2 * dinv), f"Subtracts the {m(dinv)} increase in inventory from cost of goods sold. Inventory rose, so purchases exceeded cost of goods sold."),
        "no_inv": (m(key_v - dinv), f"Starts from cost of goods sold without adjusting for the {m(dinv)} increase in inventory. Purchases = cost of goods sold + the increase in inventory."),
    }
    key = (m(key_v), f"Correct. Purchases {m(purch)} − {m(dap)} increase in payables − {m(p['nt'])} settled by note.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} buys all of its merchandise on account. For Year 2 it reports cost of goods sold of {m(p['C'])}, which includes a {m(p['wd'])} write-down of obsolete goods to net realizable value at December 31. Inventory was {m(p['I0'])} at January 1 and {m(p['I1'])}, after the write-down, at December 31. Accounts payable to suppliers was {m(p['P0'])} at January 1 and {m(p['P1'])} at December 31. In October, a supplier agreed to accept a two-year interest-bearing note payable in settlement of {m(p['nt'])} that {s} owed it on account. What cash paid to suppliers should {s} report in the operating section of its Year 2 statement of cash flows under the direct method?""",
        choices, ans,
        f"""Purchases = cost of goods sold + ending inventory − beginning inventory = {m(p['C'])} + {m(p['I1'])} − {m(p['I0'])} = {m(purch)}. The write-down is in both cost of goods sold and the reduced ending inventory, so this identity already accounts for it. Accounts payable: {m(p['P0'])} + {m(purch)} − payments − {m(p['nt'])} settled by the note = {m(p['P1'])}, so cash paid = {m(purch)} − {m(dap)} − {m(p['nt'])} = {m(key_v)}. The note is a noncash financing activity.""",
    )


# ── Area II Application ──────────────────────────────────────────────────


def cecl_aging(p):
    co, s = p["co"], short(p["co"])
    pct = lambda x: D(x) / 100
    req = sum(whole(D(b) * pct(r)) for b, r in zip(p["B"], p["r"]))
    req_f = sum(whole(D(b) * pct(D(r) + D(p["f"]))) for b, r in zip(p["B"], p["r"]))
    unadj = p["A0"] - p["W"] + p["Rv"]
    key_v = req - unadj
    assert key_v > 0
    pool = {
        "forecast": (m(req_f - unadj), f"Adds the forecast increase of {p['f']} percentage point{'' if p['f'] == '1' else 's'} to each rate. Under the practical expedient {s} elected, it assumes the conditions at the balance sheet date continue for the receivables' remaining lives, so it adjusts historical losses for current conditions only."),
        "no_recov": (m(key_v + p["Rv"]), f"Ignores the {m(p['Rv'])} recovery. Collecting an account written off earlier reinstates it and credits the allowance, which reduces the expense needed."),
        "ending": (m(req), f"Records the whole required allowance of {m(req)} as expense. Expense is the amount needed to bring the existing balance ({m(unadj)}) up to {m(req)}."),
        "no_wo": (m(key_v - p["W"]), f"Ignores the {m(p['W'])} of write-offs, which used up part of the beginning allowance."),
    }
    key = (m(key_v), f"Correct. {m(req)} required − ({m(p['A0'])} − {m(p['W'])} + {m(p['Rv'])}).")
    choices, ans = build(pool, key, p["use"])
    lab = ["not yet due", "1 to 30 days past due", "31 to 90 days past due", "more than 90 days past due"]
    aging = "; ".join(f"{lab[i]}, {m(p['B'][i])} ({p['r'][i]}%)" for i in range(4))
    return variant(
        f"""{co}, a public business entity, has adopted ASU 2025-05 and elects its practical expedient for current trade receivables. Its allowance for credit losses had a credit balance of {m(p['A0'])} at January 1, Year 2. During Year 2, {s} wrote off {m(p['W'])} of customer accounts and collected {m(p['Rv'])} on an account it had written off in Year 1. Its December 31, Year 2, aging of trade receivables, all due within 60 days of sale, with loss rates based on its historical loss experience adjusted for conditions at year-end, is: {aging}. Its economists' reasonable and supportable forecast calls for a recession in Year 3 that would add {p['f']} percentage point{'' if p['f'] == '1' else 's'} to each loss rate. What credit loss expense should {s} recognize for Year 2?""",
        choices, ans,
        f"""Required allowance: {' + '.join(m(whole(D(b) * pct(r))) for b, r in zip(p['B'], p['r']))} = {m(req)}. With the ASU 2025-05 practical expedient, {s} assumes the conditions at the balance sheet date persist over the receivables' remaining lives, so the recession forecast isn't added to the rates. Allowance before adjustment = {m(p['A0'])} − {m(p['W'])} write-offs + {m(p['Rv'])} recovery = {m(unadj)}. Credit loss expense = {m(req)} − {m(unadj)} = {m(key_v)}.""",
    )


def ppe_lump_sum(p):
    co, s = p["co"], short(p["co"])
    cost_all = p["P"] + p["cc"]
    for base, part, tot in ((cost_all, p["FB"], p["FL"] + p["FB"]), (cost_all, p["AB"], p["AL"] + p["AB"]),
                            (p["P"], p["FB"], p["FL"] + p["FB"])):
        assert D(base) * part % tot == 0, "allocation is not exact to the dollar"
    bshare = whole(D(cost_all) * p["FB"] / (p["FL"] + p["FB"]))
    cost = bshare + p["rv"]
    mo = p["mo"]
    dep = rd((cost - p["sv"]) * mo / D(p["n"] * 12))
    key_v = cost - dep

    def ca(c, months=mo):
        return c - rd((c - p["sv"]) * months / D(p["n"] * 12))
    b_ass = rd(D(cost_all) * p["AB"] / (p["AL"] + p["AB"])) + p["rv"]
    b_nocc = rd(D(p["P"]) * p["FB"] / (p["FL"] + p["FB"])) + p["rv"]
    pool = {
        "assessed": (m(ca(b_ass)), f"Allocates the purchase cost using the property tax assessments. A lump-sum purchase price is allocated on the relative fair values of the assets, from the appraisal."),
        "no_cc": (m(ca(b_nocc)), f"Leaves the {m(p['cc'])} of legal fees and title costs out of the cost of the property. Costs needed to acquire the assets are part of their cost and are allocated with the price."),
        "rv_exp": (m(ca(bshare)), f"Expenses the {m(p['rv'])} renovation. Costs to get the building ready for its intended use before it is placed in service are part of its cost."),
        "full_year": (m(ca(cost, 12)), f"Records a full year of depreciation. The building was placed in service on {p['date']}, so only {mo} months of depreciation are recorded in Year 1."),
        "no_dep": (m(cost), f"Records no depreciation in Year 1. Depreciation begins when the building is placed in service, on {p['date']}."),
    }
    key = (m(key_v), f"Correct. {m(cost)} cost − {m(dep)} depreciation.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""On January 10, Year 1, {co} paid {m(p['P'])} for land and a building on it, and paid {m(p['cc'])} of legal fees and title costs to complete the purchase. An independent appraisal valued the land at {m(p['FL'])} and the building at {m(p['FB'])}; the local property tax assessments were {m(p['AL'])} for the land and {m(p['AB'])} for the building. {s} spent {m(p['rv'])} renovating the building before moving in, and placed it in service as its head office on {p['date']}, Year 1. It depreciates the building straight-line over {p['n']} years with a residual value of {m(p['sv'])}, taking depreciation for each month the building is in service and rounding Year 1 depreciation to the nearest dollar. What carrying amount should {s} report for the building at December 31, Year 1?""",
        choices, ans,
        f"""The {m(p['P'])} price plus the {m(p['cc'])} of acquisition costs ({m(cost_all)}) is allocated on relative appraised fair values: building = {m(cost_all)} × {m(p['FB'])} / {m(p['FL'] + p['FB'])} = {m(bshare)}. The renovation before use is added: cost = {m(cost)}. Depreciation for the {mo} months from {p['date']} = ({m(cost)} − {m(p['sv'])}) ÷ {p['n']} × {mo}/12 = {m(dep)}. Carrying amount = {m(cost)} − {m(dep)} = {m(key_v)}.""",
    )


def htm_premium(p):
    co, s = p["co"], short(p["co"])
    F, k = D(p["F"]), p["n"] * 2
    cpn = rd(F * D(p["c"]) / 200)
    y = D(p["y"]) / 200
    price = rd(sum(cpn / (1 + y) ** t for t in range(1, k + 1)) + F / (1 + y) ** k)
    assert price > F
    cv = price
    steps = []
    for _ in range(3):
        inc = rd(cv * y)
        steps.append((cv, inc, cpn - inc))
        cv = cv - (cpn - inc)
    key_v = cv
    amort_total = price - cv
    sl = price - rd((price - F) * 3 / k)
    pool = {
        "sl": (m(sl), f"Amortizes the premium straight-line, {m(rd((price - F) / k))} each half-year. {s} uses the effective interest method, under which the amortization grows each period."),
        "fv": (m(p["FV"]), f"Reports the bonds at their {m(p['FV'])} fair value. Held-to-maturity securities are reported at amortized cost."),
        "noam": (m(price), f"Leaves the bonds at their {m(price)} cost. The premium is amortized as an adjustment of interest income over the bonds' life."),
        "added": (m(price + amort_total), f"Adds the premium amortization to the carrying amount. Amortizing a premium reduces the carrying amount toward face value."),
        "two": (m(steps[2][0]), f"Stops after two interest payments, at June 30, Year 2. Three semiannual payments (December 31, Year 1, and June 30 and December 31, Year 2) have been received."),
    }
    key = (m(key_v), f"Correct. {m(price)} less three periods of premium amortization: {', '.join(m(a) for _, _, a in steps)}.")
    choices, ans = build(pool, key, p["use"])
    rows = "; ".join(f"{m(c0)} × {pctf(y)} = {m(i)} interest income, {m(cpn)} − {m(i)} = {m(a)} amortized" for c0, i, a in steps)
    return variant(
        f"""On July 1, Year 1, {co} paid {m(price)} for {m(p['F'])} face amount of {p['n']}-year, {p['c']}% bonds issued that day, which pay interest each June 30 and December 31; the price gives a yield of {p['y']}% a year, compounded semiannually. {s} classifies the bonds as held to maturity and expects no credit losses on them, so it records no allowance. It amortizes the premium by the effective interest method, rounding each period's figures to the nearest dollar. At December 31, Year 2, the bonds' fair value is {m(p['FV'])}. At what amount should {s} report the investment at December 31, Year 2?""",
        choices, ans,
        f"""Each semiannual coupon is {m(p['F'])} × {p['c']}% ÷ 2 = {m(cpn)}, and interest income is the carrying amount × {p['y']}% ÷ 2. {rows}. Carrying amount at December 31, Year 2 = {m(price)} − {m(amort_total)} = {m(key_v)}. Held-to-maturity securities are reported at amortized cost, so the fair value is not used.""",
    )


def pctf(y):
    x = (D(y) * 100).normalize()
    return f"{x:f}%"


def accrued(p):
    co, s = p["co"], short(p["co"])
    assert D(p["Rt"]) * p["t"] % (100 + p["t"]) == 0, "sales tax split is not exact"
    stax = whole(D(p["Rt"]) * p["t"] / (100 + p["t"]))
    fica = rd(D(p["G"]) * D("0.0765"))
    net = p["G"] - p["wf"] - fica
    intr = rd(D(p["N"]) * p["i"] / 100 * p["mo"] / 12)
    key_v = stax + p["wf"] + 2 * fica + p["v"] + intr
    pool = {
        "tax_gross": (m(key_v + rd(D(p["Rt"]) * p["t"] / 100) - stax), f"Computes sales tax as {p['t']}% of total receipts. The receipts include the tax, so the tax is {p['t']}/{100 + p['t']} of them: {m(stax)}."),
        "no_match": (m(key_v - fica), f"Leaves out {s}'s matching {m(fica)} of payroll taxes. The employer's share is an expense and a liability until it is remitted."),
        "net_pay": (m(key_v + net), f"Includes the {m(net)} of net pay. The employees were paid on December 31; only the amounts withheld from them and the employer's taxes remain owed."),
        "no_wf": (m(key_v - p["wf"]), f"Leaves out the {m(p['wf'])} of income tax withheld. Amounts withheld from employees are owed to the government until {s} remits them."),
        "no_vac": (m(key_v - p["v"]), f"Leaves out the {m(p['v'])} of vested vacation pay. Compensation for vested absences that relates to services already rendered is accrued when earned."),
        "no_int": (m(key_v - intr), f"Accrues no interest on the note because nothing is payable until maturity. Interest accrues with time: {p['mo']} months ({m(intr)}) had accrued by December 31."),
        "int_full": (m(key_v + rd(D(p["N"]) * p["i"] / 100) - intr), f"Accrues a full year's interest on the note. It was signed on {p['nd']}, so only {p['mo']} months of interest have accrued."),
    }
    key = (m(key_v), f"Correct. {m(stax)} + {m(p['wf'])} + 2 × {m(fica)} + {m(p['v'])} + {m(intr)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s December, Year 1, records show the following, none of which had been paid or remitted at December 31 unless stated. Cash register receipts for December totaled {m(p['Rt'])}, including the {p['t']}% sales tax charged on every sale. The payroll for the last half of December, paid to employees on December 31, had gross wages of {m(p['G'])}, from which {s} withheld {m(p['wf'])} of federal income tax and {m(fica)} of employees' social security and Medicare taxes (7.65%); {s} owes a matching 7.65% of gross wages. Employees had earned {m(p['v'])} of vacation pay that vests and will be paid in Year 2. On {p['nd']}, Year 1, {s} signed a one-year, {p['i']}% note payable for {m(p['N'])}, with principal and interest due at maturity. {s} reports the note's principal separately as a note payable. What total should {s} report at December 31, Year 1, for the other liabilities arising from these items?""",
        choices, ans,
        f"""Sales tax payable = {m(p['Rt'])} × {p['t']}/{100 + p['t']} = {m(stax)}. Payroll liabilities = {m(p['wf'])} income tax withheld + {m(fica)} employees' share + {m(fica)} employer's share = {m(p['wf'] + 2 * fica)}; the net pay was paid. Vacation pay that vests and relates to services already rendered is accrued: {m(p['v'])}. Interest payable = {m(p['N'])} × {p['i']}% × {p['mo']}/12 = {m(intr)}. Total = {m(key_v)}.""",
    )


# ── Area II Analysis ─────────────────────────────────────────────────────


def bank_matching(p):
    co, s = p["co"], short(p["co"])
    out = p["B1"] + p["c2"] + p["c4"]
    correct = p["Bk"] + p["dd"] - out - p["e"]
    tr = p["c3b"] - p["c3"]
    assert tr > 0
    G = correct + p["sc"] - tr
    pool = {
        "old_out": (m(correct + p["B1"]), f"Treats check no. {p['n2']} as cleared. It was outstanding at November 30 and isn't on the December statement, so it is still outstanding."),
        "cleared_a": (m(correct - p["A1"]), f"Also deducts check no. {p['n1']}, which was outstanding at November 30 but cleared the bank in December."),
        "bank_err": (m(correct + p["e"]), f"Ignores the {m(p['e'])} deposit of another company that the bank credited to {s}'s account in error. The bank will reverse it, so it is deducted from the bank balance."),
        "transp": (m(correct - tr), f"Works from the books without correcting check no. {p['n3']}. It cleared at {m(p['c3'])}, its correct amount, but was recorded as {m(p['c3b'])}, so the books understate cash by {m(tr)}."),
        "no_dit": (m(correct - p["dd"]), f"Leaves out the {m(p['dd'])} deposit made on December 31. The bank hadn't credited it by year-end, so it is a deposit in transit, added to the bank balance."),
        "old_dit": (m(correct + p["dn"]), f"Adds the {m(p['dn'])} November 30 deposit in transit. The bank credited it on December 1, so it is already in the December 31 bank balance."),
    }
    key = (m(correct), f"Correct. {m(p['Bk'])} + {m(p['dd'])} − ({m(p['B1'])} + {m(p['c2'])} + {m(p['c4'])}) − {m(p['e'])} = {m(G)} − {m(p['sc'])} + {m(tr)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s December 31 bank statement shows a balance of {m(p['Bk'])}, and its general ledger cash account shows {m(G)}. The November 30 reconciliation listed a deposit in transit of {m(p['dn'])}, which the bank credited on December 1, and two outstanding checks: no. {p['n1']} for {m(p['A1'])} and no. {p['n2']} for {m(p['B1'])}. In December, {s} wrote checks no. {p['n3'] - 1} for {m(p['c1'])}, no. {p['n3']} for {m(p['c3'])} (recorded in the cash disbursements journal as {m(p['c3b'])}), no. {p['n3'] + 1} for {m(p['c2'])} and no. {p['n3'] + 2} for {m(p['c4'])}. The checks paid by the bank in December were nos. {p['n1']}, {p['n3'] - 1} and {p['n3']}, each for the amount written on it. {s}'s December 31 deposit of {m(p['dd'])} was credited by the bank on January 2. The December statement also shows a {m(p['sc'])} service charge, which {s} hasn't recorded, and a {m(p['e'])} deposit belonging to another company, which the bank credited to {s}'s account in error. What cash balance should {s} report at December 31?""",
        choices, ans,
        f"""Outstanding checks at December 31 are those written and not yet paid: no. {p['n2']} from November ({m(p['B1'])}) and nos. {p['n3'] + 1} and {p['n3'] + 2} ({m(p['c2'])} and {m(p['c4'])}), {m(out)} in all; no. {p['n1']} cleared in December. Bank side: {m(p['Bk'])} + {m(p['dd'])} deposit in transit − {m(out)} − {m(p['e'])} bank error = {m(correct)}. Book side: {m(G)} − {m(p['sc'])} service charge + {m(tr)} overstatement of check no. {p['n3']} = {m(correct)}. The November deposit in transit is already in the bank balance.""",
    )


def cash_plug(p):
    co, s = p["co"], short(p["co"])
    correct = p["Bk"] + p["dit"] - p["oc"] - p["ck"]
    dt = p["dT"] - p["dR"]
    assert dt > 0
    G0 = correct + 2 * p["c"] - dt + p["lp"]
    AB = p["Bk"] + p["dit"] - p["oc"]
    P = G0 - AB
    assert P > 0
    pool = {
        "after_plug": (m(AB), f"Accepts the ledger after the plug. That balance only matches the bookkeeper's adjusted bank balance, which leaves out check no. {p['ckn']} for {m(p['ck'])}, still outstanding."),
        "c_single": (m(correct + p["c"]), f"Corrects the check entered as a receipt by only {m(p['c'])}. Recording a {m(p['c'])} payment as a receipt overstated cash by twice its amount: the receipt must be removed and the payment recorded."),
        "no_lp": (m(correct + p["lp"]), f"Works from the books without the {m(p['lp'])} loan payment the bank deducted automatically, which {s} hasn't recorded."),
        "dt_sign": (m(correct - 2 * dt), f"Deducts the {m(dt)} difference on the deposit. It was recorded at {m(p['dR'])} but was {m(p['dT'])}, so the books understate cash."),
        "ck_book": (m(correct - p["ck"]), f"Deducts check no. {p['ckn']} from the book balance. It was recorded on September 28, so the books already reflect it; it is an outstanding check, deducted only from the bank balance."),
        "before": (m(G0), f"Reverses the plug and stops there. The ledger before the plug still contains the receipt that was really a payment, the understated deposit and the unrecorded loan payment."),
    }
    key = (m(correct), f"Correct. {m(p['Bk'])} + {m(p['dit'])} − ({m(p['oc'])} + {m(p['ck'])}) = {m(G0)} − {m(2 * p['c'])} + {m(dt)} − {m(p['lp'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s bookkeeper reconciled the September 30 bank statement as follows: bank balance {m(p['Bk'])}, plus deposits in transit {m(p['dit'])}, less outstanding checks {m(p['oc'])}, gives {m(AB)}. The general ledger showed {m(G0)}, so the bookkeeper recorded the {m(P)} difference as miscellaneous expense, bringing the ledger to {m(AB)}. The controller reverses that entry and investigates. She finds: check no. {p['cn']}, a {m(p['c'])} payment to a supplier that cleared the bank in September, was entered in the cash receipts journal instead of the cash disbursements journal; a customer's {m(p['dT'])} check, deposited and credited by the bank on September 14, was recorded in the cash receipts journal as {m(p['dR'])}; check no. {p['ckn']} for {m(p['ck'])}, issued and recorded on September 28, is missing from the bookkeeper's list of outstanding checks and hasn't cleared the bank; and on September 30 the bank deducted a {m(p['lp'])} monthly loan payment under {s}'s automatic payment arrangement, which {s} hasn't recorded. What cash balance should {s} report at September 30?""",
        choices, ans,
        f"""Bank side: the omitted outstanding check is deducted: {m(p['Bk'])} + {m(p['dit'])} − {m(p['oc'])} − {m(p['ck'])} = {m(correct)}. Book side, after reversing the plug: {m(G0)} − {m(2 * p['c'])} (remove the {m(p['c'])} recorded as a receipt and record it as a payment) + {m(dt)} (the deposit was {m(p['dT'])}, not {m(p['dR'])}) − {m(p['lp'])} loan payment = {m(correct)}. The {m(P)} plug hid these four items.""",
    )


def ar_recon_adjust(p):
    co, s = p["co"], short(p["co"])
    C = p["C"]
    GL = C - p["n"] + p["N"]
    Sub = C + p["sd"] + (p["Y"] - p["X"])
    adj = p["N"] - p["n"]
    dec = lambda x: f"{m(x)} decrease"
    gl_vs_sub = GL - Sub
    assert adj > 0 and gl_vs_sub > 0 and adj - p["n"] > 0
    pool = {
        "no_nsf": (dec(p["N"]), f"Leaves out the {m(p['n'])} NSF check. Charging the customer's account back for a returned check increases receivables, and only the subledger recorded it, so the control account needs it too."),
        "sd_gl": (dec(adj + p["sd"]), f"Also deducts the {m(p['sd'])} of sales discounts from the control account. The discounts were posted to the control account through the cash receipts journal; it is the subledger that omitted them."),
        "to_sub": (dec(gl_vs_sub), f"Adjusts the control account to agree with the subledger as recorded. The subledger has its own errors: the {m(p['sd'])} of discounts not posted and the invoice posted at {m(p['Y'])} instead of {m(p['X'])}."),
        "nsf_sign": (dec(p["N"] + p["n"]), f"Deducts the {m(p['n'])} NSF check from the control account. A returned check reinstates the customer's balance, so it increases receivables."),
    }
    key = (dec(adj), f"Correct. − {m(p['N'])} note + {m(p['n'])} NSF check; the control account becomes {m(C)}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s accounts receivable subledger totals {m(Sub)}, and the general ledger control account shows {m(GL)}. The controller traces the difference and finds: a customer's {m(p['n'])} check, returned by the bank in December marked NSF, was charged back to the customer's subledger account, but the clerk's journal entry recorded only the reduction of cash, debiting miscellaneous expense rather than accounts receivable; customers took {m(p['sd'])} of sales discounts in December, which were recorded in the discount column of the cash receipts journal and posted with its totals, while the clerk credited each customer's subledger account only for the cash received; a customer's {m(p['N'])} past-due account was converted in December into a six-month note receivable, which the clerk recorded by closing the customer's subledger account and opening a note receivable record, without a journal entry; and a {m(p['X'])} sales invoice was posted to the customer's subledger account as {m(p['Y'])}. What net adjustment should {s} make to its accounts receivable control account?""",
        choices, ans,
        f"""Work out which record each item affects. The NSF charge-back is in the subledger but not the control account: + {m(p['n'])}. The discounts are in the control account but not the subledger: the subledger needs − {m(p['sd'])}. The note conversion is in the subledger but not the control account: − {m(p['N'])}. The invoice error is in the subledger only: − {m(p['Y'] - p['X'])}. Control account: {m(GL)} + {m(p['n'])} − {m(p['N'])} = {m(C)}, a net decrease of {m(adj)}. Subledger: {m(Sub)} − {m(p['sd'])} − {m(p['Y'] - p['X'])} = {m(C)}, so the records agree.""",
    )


def inv_shrinkage(p):
    co, s = p["co"], short(p["co"])
    book = p["B"] + p["P"] - p["C"]
    key_v = book - p["t"] + p["g"] - (p["Q"] + p["g"] + p["k"])
    assert key_v > 0
    pool = {
        "no_t": (m(key_v + p["t"]), f"Leaves the {m(p['t'])} of goods shipped FOB destination in the perpetual records. They weren't {s}'s until they arrived on January 4, so the purchase and the inventory are removed from Year 1."),
        "no_k": (m(key_v + p["k"]), f"Leaves out the {m(p['k'])} of goods held by the consignee. {s} still owns consigned goods, so they are added to the count."),
        "g_book": (m(key_v + p["g"]), f"Restores the {m(p['g'])} of goods in transit to the customer to the perpetual records but not to the count. They were {s}'s at year-end and weren't in the warehouse, so both the records and the count must include them."),
        "g_count": (m(key_v - p["g"]), f"Adds the {m(p['g'])} of goods in transit to the customer to the count but leaves them out of the perpetual records. The sale was recorded early, so the records also need the goods restored."),
    }
    key = (m(key_v), f"Correct. ({m(book)} − {m(p['t'])} + {m(p['g'])}) − ({m(p['Q'])} + {m(p['g'])} + {m(p['k'])}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} uses a perpetual inventory system. Its Year 1 inventory rollforward, taken from the perpetual records, shows beginning inventory of {m(p['B'])}, purchases of {m(p['P'])}, cost of goods sold of {m(p['C'])} and ending inventory of {m(book)}. The December 31 physical count, priced at cost, totals {m(p['Q'])}. Cutoff work finds: purchases include goods costing {m(p['t'])} that a supplier shipped on December 28, FOB destination, and that arrived on January 4; goods costing {m(p['g'])}, shipped to a customer on December 30, FOB destination, and delivered on January 3, were recorded as a December sale and removed from the perpetual records; and goods costing {m(p['k'])} that {s} sent to a dealer in November to sell on {s}'s behalf were not counted. What inventory shrinkage should {s} recognize for Year 1?""",
        choices, ans,
        f"""Corrected perpetual balance: {m(book)} − {m(p['t'])} (goods shipped FOB destination belong to the seller until delivered) + {m(p['g'])} (goods shipped FOB destination to the customer are still {s}'s) = {m(book - p['t'] + p['g'])}. Corrected count: {m(p['Q'])} + {m(p['g'])} goods in transit to the customer + {m(p['k'])} consigned goods = {m(p['Q'] + p['g'] + p['k'])}. Shrinkage = {m(book - p['t'] + p['g'])} − {m(p['Q'] + p['g'] + p['k'])} = {m(key_v)}. The goods in transit to the customer affect both sides equally.""",
    )


def ppe_rollforward_gross(p):
    co, s = p["co"], short(p["co"])
    E = p["G0"] + p["A"] - p["cv"]
    ad = p["cs"] - p["cv"]
    sti = p["st"] + p["it"]
    key_v = E - p["r"] + sti - ad - p["fd"]
    pool = {
        "rep": (m(key_v + p["r"]), f"Keeps the {m(p['r'])} of routine repairs in the additions. Ordinary repairs and maintenance that don't extend an asset's life or improve it are expensed."),
        "inst": (m(key_v - sti), f"Leaves the {m(p['st'])} of sales tax and {m(p['it'])} of installation and testing out of the press's cost. Costs needed to get an asset ready for its intended use are capitalized."),
        "cv": (m(key_v + ad), f"Removes only the sold machine's {m(p['cv'])} carrying amount from gross equipment. The equipment account carries cost, so the {m(p['cs'])} cost comes out (and the {m(ad)} of accumulated depreciation comes out of that account)."),
        "sale_price": (m(key_v + p["cs"] - p["sp"]), f"Removes the sold machine at its {m(p['sp'])} sale price. The equipment account carries cost, so the machine comes out at its {m(p['cs'])} cost; the difference between the price and the carrying amount is a gain or loss."),
        "scrap": (m(key_v + p["fd"]), f"Leaves the {m(p['fd'])} lathe in the equipment account. An asset that is scrapped is removed at cost, with its accumulated depreciation, even though it was fully depreciated."),
    }
    key = (m(key_v), f"Correct. {m(E)} − {m(p['r'])} + {m(sti)} − {m(ad)} − {m(p['fd'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s staff prepared this Year 2 rollforward of the equipment account (at cost): January 1 balance {m(p['G0'])}; additions {m(p['A'])}; disposals ({m(p['cv'])}); December 31 balance {m(E)}. The controller reviews the supporting documents. The additions are the capital expenditures report, which includes a new press recorded at its {m(p['ip'])} invoice price, a delivery truck, and {m(p['r'])} of routine repair and maintenance work on existing machines; the {m(p['st'])} of sales tax on the press and the {m(p['it'])} paid to install and test it before use were charged to expense. The disposal is a machine sold in July for {m(p['sp'])} that had cost {m(p['cs'])} and had accumulated depreciation of {m(ad)} at the date of sale. In October, {s} scrapped a fully depreciated lathe that had cost {m(p['fd'])}, and no entry was made. What equipment balance should the corrected rollforward show at December 31, Year 2?""",
        choices, ans,
        f"""Additions: the routine repairs are expensed (− {m(p['r'])}), and the press's cost includes the sales tax and installation and testing (+ {m(sti)}). Disposals at cost: the machine sold comes out at {m(p['cs'])}, not its {m(p['cv'])} carrying amount (− {m(ad)} more), and the scrapped lathe comes out at {m(p['fd'])}. Corrected balance = {m(E)} − {m(p['r'])} + {m(sti)} − {m(ad)} − {m(p['fd'])} = {m(key_v)}.""",
    )


# ── Area III Analysis ────────────────────────────────────────────────────


def restated_ni(p):
    co, s = p["co"], short(p["co"])
    t = D("0.75")
    pre = -p["d"] - p["i"] + p["rr"]
    key_v = p["N"] + whole(pre * t)
    pool = {
        "pretax": (m(p["N"] + pre), f"Restates by the pretax amounts. Each correction changes income tax expense too, so net income changes by 75% of each pretax amount."),
        "int_sign": (m(key_v + whole(2 * p["i"] * t)), f"Increases Year 2 income for the interest. The {m(p['i'])} was earned in Year 1 but recorded as Year 2 revenue when collected, so Year 2 income was overstated and the restatement reduces it."),
        "estimate": (m(key_v - whole(p["we"] * t)), f"Applies the Year 3 revision of the warranty estimate to Year 2. A change in estimate is accounted for prospectively, in Year 3 and later; prior periods are not restated."),
        "no_int": (m(key_v + whole(p["i"] * t)), f"Treats the interest as affecting Year 1 only. Recording it as revenue when collected in Year 2 also overstated Year 2 income, so the Year 2 column is restated for it."),
        "rent_sign": (m(key_v - whole(2 * p["rr"] * t)), f"Reduces Year 2 income for the rent. The {m(p['rr'])} paid in December, Year 2, for Year 3 rent was expensed in Year 2, so Year 2 expense was overstated and income rises."),
    }
    key = (m(key_v), f"Correct. {m(p['N'])} + 75% × (− {m(p['d'])} − {m(p['i'])} + {m(p['rr'])}).")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co} presents comparative financial statements for Years 2 and 3. Its Year 2 statements, already issued, reported net income of {m(p['N'])}. While preparing its Year 3 statements, {s} finds: a {m(p['d'])} deposit received in December, Year 2, from a customer for goods delivered in February, Year 3, was recorded as Year 2 sales revenue, and the goods' cost was correctly charged to Year 3; {m(p['i'])} of interest earned on a note receivable during Year 1 was never accrued and was recorded as interest revenue when collected in March, Year 2; and {m(p['rr'])} of rent paid in December, Year 2, for January through June, Year 3, was charged to Year 2 rent expense. In Year 3, {s} also revised its warranty cost estimates on the basis of new claims experience; had the new estimates been used in Year 2, Year 2 warranty expense would have been {m(p['we'])} higher. {s}'s income tax rate is 25% for all years and all items. What net income should {s} report for Year 2 in its comparative statements?""",
        choices, ans,
        f"""The three errors are corrected by restating Year 2; the warranty revision is a change in estimate, applied prospectively. Pretax effects on Year 2: the deposit wasn't revenue until the goods were delivered in Year 3 (− {m(p['d'])}); the interest belonged to Year 1, so recording it on collection overstated Year 2 (− {m(p['i'])}); the prepaid rent was Year 3 expense (+ {m(p['rr'])}). Net pretax effect = {m(pre) if pre > 0 else '− ' + m(-pre)}; after tax, × 75% = {m(whole(pre * t)) if pre > 0 else '− ' + m(-whole(pre * t))}. Restated Year 2 net income = {m(key_v)}.""",
    )


def se_liabilities(p):
    co, s = p["co"], short(p["co"])
    key_v = p["L"] - (p["a"] - p["sx"]) + p["w"]
    assert p["a"] > p["sx"]
    pool = {
        "div": (m(key_v + p["Dv"]), f"Adds the {m(p['Dv'])} dividend declared on February 5. A dividend becomes a liability when declared, which was after year-end; it is disclosed, not recognized."),
        "new_suit": (m(key_v + p["x"]), f"Accrues the {m(p['x'])} expected on the suit over the January {p['jd']} accident. The accident happened after year-end, so it is a nonrecognized subsequent event, disclosed if material."),
        "keep": (m(key_v + p["a"] - p["sx"]), f"Leaves the {m(p['a'])} accrual for the Year 1 injury suit unchanged. The settlement gives better evidence of the liability that existed at year-end, so the accrual is reduced to the {m(p['sx'])} settlement."),
        "settled_out": (m(key_v - p["sx"]), f"Removes the injury suit from liabilities altogether because it was settled. The {m(p['sx'])} settlement isn't payable until April, so it is still owed at December 31."),
        "loan": (m(key_v + p["Bl"]), f"Adds the {m(p['Bl'])} borrowed in February. The loan didn't exist at December 31; it is disclosed, not recognized."),
        "warr_none": (m(key_v - p["w"]), f"Leaves out the {m(p['w'])} of warranty repairs. The defect existed in units sold before year-end, so the February testing gives evidence about a liability that existed at December 31."),
    }
    key = (m(key_v), f"Correct. {m(p['L'])} − ({m(p['a'])} − {m(p['sx'])}) + {m(p['w'])}.")
    choices, ans = build(pool, key, p["use"])
    return variant(
        f"""{co}'s draft December 31, Year 1, balance sheet reports total liabilities of {m(p['L'])}, including a {m(p['a'])} accrual for a customer's suit over an injury at one of {s}'s stores in Year 1. The statements will be issued on March 12, Year 2. After year-end: on January 22, {s} settled the injury suit for {m(p['sx'])}, payable in April; in February, testing found a defective part in all of the space heaters {s} sold in November and December, Year 1, and {s} estimates that repairing them under its standard one-year warranty will cost {m(p['w'])}, none of which was in its year-end warranty accrual; on January {p['jd']}, a shopper was injured in one of {s}'s stores, and counsel expects the resulting suit to cost {s} {m(p['x'])}; on February 5, the board declared a cash dividend of {m(p['Dv'])}, payable March 31; and on February 20, {s} borrowed {m(p['Bl'])} from its bank. What total liabilities should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""Events that give more evidence about conditions at December 31 are recognized: the settlement shows the Year 1 injury suit was worth {m(p['sx'])}, not {m(p['a'])} (− {m(p['a'] - p['sx'])}), and the defect existed in heaters sold before year-end, so the warranty liability rises by {m(p['w'])}. The January injury, the dividend declaration and the new loan arise from events after year-end; they are disclosed if material but not recognized. Total liabilities = {m(p['L'])} − {m(p['a'] - p['sx'])} + {m(p['w'])} = {m(key_v)}.""",
    )


FAMILIES = [
    # ── Area I Application ──
    ("far-balance-sheet-0008", A1, "Balance sheet", AP,
     ["ASC 210-10-45 (current liabilities; customer credit balances)", "ASC 505-20 (stock dividends distributable reported in equity)", "ASC 842-20-45 (lessee presentation of lease liabilities)", "ASC 740-10-45 (deferred taxes classified as noncurrent)"],
     bs_current_liabilities, [
        dict(co="Alnmouth Co.", ap=412000, ai=18500, dr=536000, cb=11800, sdd=75000, LL=264000, Lc=58000, W=96000, Wc=41000, ur=37500, dtl=88000, use=["no_cb", "lease_none", "warr_none"]),
        dict(co="Beadnell Co.", ap=298000, ai=12400, dr=387000, cb=8600, sdd=52000, LL=196000, Lc=43000, W=71000, Wc=29000, ur=26500, dtl=63000, use=["sdd", "lease_all", "dtl"]),
        dict(co="Capheaton Co.", ap=547000, ai=24800, dr=702000, cb=15300, sdd=96000, LL=348000, Lc=77000, W=128000, Wc=54000, ur=49500, dtl=117000, use=["no_cb", "warr_none", "lease_all"]),
        dict(co="Edlingham Co.", ap=226000, ai=9600, dr=294000, cb=6900, sdd=40000, LL=148000, Lc=32000, W=54000, Wc=22000, ur=19500, dtl=47000, use=["warr_none", "sdd", "dtl"]),
     ]),
    ("far-income-statement-0007", A1, "Income statement", AP,
     ["ASC 220-10 (income statement presentation)", "ASC 360-10-45-4 (impairment loss on a long-lived asset held and used included in income from operations when that subtotal is presented)", "ASC 360-10-45-5 (gain or loss on the sale of a long-lived asset that is not a discontinued operation included in income from operations when that subtotal is presented)", "ASC 205-20 (discontinued operations)"],
     is_operating_income, [
        dict(co="Ellingham Corp.", S=4860000, sr=92000, sd=38000, cg=2915000, se=486000, ga=612000, imp=145000, gs=34000, ie=68000, dv=21000, ld=118000, seg="furniture", use=["no_gain", "int", "disc"]),
        dict(co="Embleton Corp.", S=3720000, sr=71000, sd=29000, cg=2230000, se=371000, ga=468000, imp=112000, gs=26000, ie=52000, dv=16000, ld=91000, seg="marine", use=["int", "no_imp", "div"]),
        dict(co="Felton Corp.", S=6150000, sr=118000, sd=47000, cg=3690000, se=615000, ga=774000, imp=184000, gs=43000, ie=86000, dv=27000, ld=149000, seg="printing", use=["disc", "no_gain", "no_imp"]),
        dict(co="Glanton Corp.", S=2940000, sr=56000, sd=23000, cg=1765000, se=294000, ga=370000, imp=88000, gs=21000, ie=41000, dv=13000, ld=72000, seg="catering", use=["no_gain", "int", "div"]),
     ]),
    ("far-cash-flows-0013", A1, "Statement of cash flows", AP,
     ["ASC 230-10-50-2 (supplemental disclosure of income taxes paid under the indirect method)", "ASC 740-10-45 and 740-20-45 (deferred tax expense; tax effects allocated to other comprehensive income)"],
     taxes_paid, [
        dict(co="Harbottle Inc.", E=486000, TP0=42000, TP1=57000, DTL0=118000, DTL1=171000, oci=19000, DTA0=36000, DTA1=41000, use=["oci_in", "dta_sign", "tp_sign"]),
        dict(co="Kielder Inc.", E=362000, TP0=31000, TP1=43000, DTL0=87000, DTL1=126000, oci=14000, DTA0=27000, DTA1=35000, use=["no_def", "tp_sign", "current"]),
        dict(co="Lesbury Inc.", E=615000, TP0=54000, TP1=72000, DTL0=149000, DTL1=216000, oci=24000, DTA0=46000, DTA1=52000, use=["dta_sign", "current", "no_def"]),
        dict(co="Longhorsley Inc.", E=248000, TP0=21000, TP1=29000, DTL0=59000, DTL1=86000, oci=9000, DTA0=18000, DTA1=21000, use=["oci_in", "dta_sign", "no_def"]),
     ]),
    ("far-nfp-financial-position-0004", A1, "Statement of financial position (Not-for-Profit)", AP,
     ["ASC 958-210 (not-for-profit statement of financial position)", "ASC 958-205-45 (net assets with and without donor restrictions; underwater endowment funds, as amended by ASU 2016-14)", "ASC 958-605-25 (conditional contributions; refundable advances)"],
     nfp_without, [
        dict(org="Matfen Reading Society", TA=3840000, TL=612000, G=1500000, F=1380000, R=164000, P=225000, BD=400000, ra=90000, use=["old_rule", "bd", "ra"]),
        dict(org="Mitford Literacy League", TA=2960000, TL=471000, G=1150000, F=1062000, R=127000, P=174000, BD=310000, ra=68000, use=["bd", "ra", "total"]),
        dict(org="Ovingham Learning Trust", TA=5120000, TL=818000, G=2000000, F=1846000, R=219000, P=300000, BD=530000, ra=120000, use=["old_rule", "bd", "total"]),
        dict(org="Rennington Book Fund", TA=2210000, TL=356000, G=860000, F=791000, R=94000, P=129000, BD=230000, ra=51000, use=["old_rule", "ra", "total"]),
     ]),
    ("far-nfp-statement-of-activities-0003", A1, "Statement of activities (Not-for-Profit)", AP,
     ["ASC 958-225 (statement of activities)", "ASC 958-205-45 (net assets released from restrictions; long-lived assets placed in service, as amended by ASU 2016-14)", "ASC 958-605-25 (implied time restrictions; conditional promises to give)", "ASC 958-205-45 (endowment return with donor restrictions until appropriated)"],
     nfp_with_change, [
        dict(org="Shilbottle Senior Services", c1=240000, e1=185000, c2=60000, q=54000, re=96000, a=40000, pl=35000, cp=50000, use=["pledge_wo", "endow_wo", "c2_wo"]),
        dict(org="Snitter Community Kitchen", c1=182000, e1=139000, c2=45000, q=41000, re=72000, a=30000, pl=26000, cp=38000, use=["no_release_eq", "cond", "no_approp"]),
        dict(org="Thropton Meals Network", c1=310000, e1=244000, c2=78000, q=71000, re=124000, a=52000, pl=45000, cp=65000, use=["endow_wo", "c2_wo", "cond"]),
        dict(org="Ulgham Home Care Alliance", c1=128000, e1=97000, c2=32000, q=29000, re=51000, a=21000, pl=18000, cp=27000, use=["pledge_wo", "no_approp", "no_release_eq"]),
     ]),
    # ── Area I Analysis ──
    ("far-changes-in-equity-0006", A1, "Statement of changes in equity", AN,
     ["ASC 220-10-45 (other comprehensive income; reclassification adjustments)", "ASC 321-10-35 (equity securities: fair value changes in net income)", "ASC 326-30 (credit losses on available-for-sale debt securities: allowance through net income)", "ASC 320-10-35 (available-for-sale debt securities: unrealized holding gains and losses in OCI)"],
     aoci_discrepancies, [
        dict(co="Whalton Corp.", B=146000, gA=58000, gE=34000, dZ=72000, c=27000, r=19000, zb="Ponteland Mills", use=["credit_oci", "eq", "no_reclass"]),
        dict(co="Widdrington Corp.", B=212000, gA=81000, gE=47000, dZ=96000, c=38000, r=26000, zb="Slaley Foods", use=["all_credit", "draft", "eq"]),
        dict(co="Yetlington Corp.", B=98000, gA=42000, gE=25000, dZ=54000, c=19000, r=14000, zb="Stamfordham Paper", use=["credit_oci", "all_credit", "draft"]),
        dict(co="Bywell Corp.", B=275000, gA=104000, gE=61000, dZ=118000, c=46000, r=33000, zb="Simonburn Glass", use=["no_reclass", "eq", "all_credit"]),
     ]),
    ("far-cash-flows-0014", A1, "Statement of cash flows", AN,
     ["ASC 230-10-45-15 (financing outflows, including debt prepayment and extinguishment costs, as amended by ASU 2016-15)", "ASC 842-20-45-5 (finance lease payments: principal in financing, interest in operating)", "ASC 230-10-50-3 (noncash investing and financing activities)"],
     scf_financing_discrepancies, [
        dict(co="Acklington Co.", O=684000, Eq=412000, Bld=950000, Bp=1470000, T=600000, pen=18000, L=96000, i=21000, Dv=140000, M=520000, use=["no_int", "no_pen", "keep_m"]),
        dict(co="Bardon Co.", O=512000, Eq=310000, Bld=720000, Bp=1080000, T=450000, pen=13500, L=72000, i=16000, Dv=105000, M=390000, use=["no_pen", "keep_m", "lease_out"]),
        dict(co="Cambo Co.", O=938000, Eq=566000, Bld=1300000, Bp=1960000, T=800000, pen=24000, L=128000, i=29000, Dv=190000, M=700000, use=["no_int", "lease_out", "no_pen"]),
        dict(co="Chollerton Co.", O=376000, Eq=228000, Bld=540000, Bp=790000, T=330000, pen=9900, L=54000, i=12000, Dv=78000, M=290000, use=["no_int", "keep_m", "lease_out"]),
     ]),
    ("far-cash-flows-0015", A1, "Statement of cash flows", AN,
     ["ASC 230-10-45 (direct method: cash paid to suppliers)", "ASC 230-10-50-3 (noncash investing and financing activities)", "ASC 330-10-35 (inventory write-down to net realizable value)"],
     suppliers_paid, [
        dict(co="Craster Trading Co.", C=2840000, wd=46000, I0=512000, I1=578000, P0=294000, P1=331000, nt=85000, use=["wd", "inv_sign", "no_note"]),
        dict(co="Dilston Trading Co.", C=2115000, wd=34000, I0=381000, I1=430000, P0=219000, P1=247000, nt=63000, use=["wd", "no_inv", "no_note"]),
        dict(co="Eglingham Trading Co.", C=3560000, wd=58000, I0=642000, I1=725000, P0=368000, P1=415000, nt=107000, use=["inv_sign", "no_note", "ap_sign"]),
        dict(co="Elwick Trading Co.", C=1470000, wd=24000, I0=265000, I1=299000, P0=152000, P1=172000, nt=44000, use=["inv_sign", "no_inv", "ap_sign"]),
     ]),
    # ── Area II Application ──
    ("far-receivables-credit-losses-0003", A2, "Trade receivables", AP,
     ["ASC 326-20 (current expected credit losses: loss-rate method by aging; write-offs and recoveries)", "ASU 2025-05 (practical expedient for current accounts receivable and contract assets: conditions at the balance sheet date assumed to persist; elected here)"],
     cecl_aging, [
        dict(co="Falstone Supply Corp.", B=[1240000, 386000, 142000, 58000], r=["0.8", "3", "12", "45"], f="1", A0=52000, W=31000, Rv=4500, use=["forecast", "no_recov", "ending"]),
        dict(co="Haltwhistle Supply Corp.", B=[968000, 302000, 111000, 46000], r=["0.6", "2.5", "10", "40"], f="1.5", A0=34000, W=24000, Rv=3800, use=["no_wo", "forecast", "ending"]),
        dict(co="Howick Supply Corp.", B=[1585000, 494000, 182000, 74000], r=["0.8", "3.5", "14", "50"], f="1", A0=72000, W=51000, Rv=7200, use=["no_wo", "no_recov", "ending"]),
        dict(co="Kirkharle Supply Corp.", B=[742000, 231000, 85000, 35000], r=["1", "4", "15", "50"], f="2", A0=36000, W=26000, Rv=3500, use=["no_wo", "forecast", "no_recov"]),
     ]),
    ("far-ppe-lump-sum-0001", A2, "Property, plant and equipment", AP,
     ["ASC 360-10-30 (initial measurement of property, plant and equipment: costs to acquire and prepare for use)", "ASC 805-50-30 (asset acquisitions: cost allocated to the assets acquired on the basis of relative fair values)", "ASC 360-10-35 (depreciation)"],
     ppe_lump_sum, [
        dict(co="Lucker Co.", P=2400000, cc=48000, FL=780000, FB=1820000, AL=900000, AB=1100000, rv=186000, date="April 1", mo=9, n=30, sv=120000, use=["assessed", "no_cc", "no_dep"]),
        dict(co="Newbrough Co.", P=1800000, cc=36000, FL=630000, FB=1470000, AL=700000, AB=800000, rv=144000, date="May 1", mo=8, n=25, sv=90000, use=["no_cc", "rv_exp", "full_year"]),
        dict(co="Rothbury Co.", P=3200000, cc=64000, FL=1050000, FB=2450000, AL=1000000, AB=1500000, rv=232000, date="March 1", mo=10, n=40, sv=160000, use=["assessed", "full_year", "no_dep"]),
        dict(co="Stocksfield Co.", P=1500000, cc=30000, FL=480000, FB=1120000, AL=600000, AB=650000, rv=118000, date="June 1", mo=7, n=20, sv=75000, use=["assessed", "rv_exp", "full_year"]),
     ]),
    ("far-investments-htm-0002", A2, "Investments (Financial assets at amortized cost)", AP,
     ["ASC 320-10-35 (held-to-maturity debt securities at amortized cost)", "ASC 310-20-35 (interest method: amortization of premium)"],
     htm_premium, [
        dict(co="Thockrington Corp.", F=800000, c=7, y=6, n=5, FV=839500, use=["fv", "noam", "added"]),
        dict(co="Tritlington Corp.", F=600000, c=8, y=6, n=4, FV=618000, use=["sl", "fv", "noam"]),
        dict(co="Wylam Corp.", F=1000000, c=6, y=5, n=6, FV=1031000, use=["sl", "added", "two"]),
        dict(co="Acomb Corp.", F=500000, c=9, y=7, n=5, FV=524000, use=["noam", "added", "two"]),
     ]),
    ("far-accrued-liabilities-0002", A2, "Payables and accrued liabilities", AP,
     ["ASC 405-10 (liabilities, including sales taxes collected for a taxing authority)", "ASC 710-10-25 (compensated absences: vested vacation pay)", "Payroll accounting practice (amounts withheld from employees; employer payroll taxes)", "ASC 835-10 (interest)"],
     accrued, [
        dict(co="Mickley Hardware Co.", Rt=642000, t=7, G=186000, wf=27900, v=41500, N=240000, i=8, nd="August 1", mo=5, use=["no_match", "no_wf", "tax_gross"]),
        dict(co="Prudhoe Hardware Co.", Rt=481500, t=7, G=142000, wf=21300, v=31800, N=180000, i=9, nd="September 1", mo=4, use=["tax_gross", "net_pay", "int_full"]),
        dict(co="Healey Hardware Co.", Rt=848000, t=6, G=244000, wf=36600, v=54400, N=300000, i=8, nd="July 1", mo=6, use=["no_vac", "no_int", "no_wf"]),
        dict(co="Ninebanks Hardware Co.", Rt=349800, t=6, G=104000, wf=15600, v=23300, N=150000, i=10, nd="October 1", mo=3, use=["no_wf", "no_int", "no_match"]),
     ]),
    # ── Area II Analysis ──
    ("far-cash-bank-reconciliation-0005", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (outstanding checks carried from the prior month; deposits in transit; bank errors; recording errors)"],
     bank_matching, [
        dict(co="Carrshield Co.", Bk=58740, dn=4215, n1=3306, A1=1875, n2=3311, B1=2460, n3=3348, c1=3190, c3=3850, c3b=8350, c2=2745, c4=4380, dd=5230, sc=45, e=1350, use=["cleared_a", "transp", "no_dit"]),
        dict(co="Coanwood Co.", Bk=43620, dn=3180, n1=2214, A1=1425, n2=2219, B1=1870, n3=2251, c1=2360, c3=2470, c3b=4270, c2=2085, c4=3260, dd=3940, sc=35, e=960, use=["old_out", "bank_err", "old_dit"]),
        dict(co="Featherstone Co.", Bk=81350, dn=5870, n1=4482, A1=2640, n2=4490, B1=3415, n3=4527, c1=4410, c3=2350, c3b=5320, c2=3820, c4=6075, dd=7260, sc=60, e=1790, use=["transp", "no_dit", "old_out"]),
        dict(co="Lambley Co.", Bk=31480, dn=2350, n1=1617, A1=1060, n2=1622, B1=1385, n3=1659, c1=1730, c3=1580, c3b=5180, c2=1515, c4=2390, dd=2875, sc=30, e=710, use=["cleared_a", "no_dit", "bank_err"]),
     ]),
    ("far-cash-unreconciled-0003", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (unreconciled differences; recording errors; unrecorded bank charges; omitted outstanding checks)"],
     cash_plug, [
        dict(co="Knarsdale Co.", Bk=94360, dit=8420, oc=15730, cn=6118, c=2760, dT=4850, dR=4085, ckn=6194, ck=3915, lp=1840, use=["dt_sign", "after_plug", "c_single"]),
        dict(co="Kirkhaugh Co.", Bk=67250, dit=6130, oc=11480, cn=4407, c=1985, dT=3640, dR=3064, ckn=4475, ck=2370, lp=1320, use=["after_plug", "no_lp", "before"]),
        dict(co="Garrigill Co.", Bk=125840, dit=11260, oc=20940, cn=8851, c=3640, dT=6420, dR=4620, ckn=8926, ck=4285, lp=2450, use=["dt_sign", "ck_book", "no_lp"]),
        dict(co="Nenthead Co.", Bk=48930, dit=4470, oc=8360, cn=3329, c=1450, dT=2780, dR=2078, ckn=3388, ck=2140, lp=960, use=["c_single", "after_plug", "before"]),
     ]),
    ("far-receivables-reconciliation-0004", A2, "Trade receivables", AN,
     ["ASC 310-10 (receivables)", "Subsidiary ledger and control account reconciliation practice (returned checks; cash discounts; conversion to notes receivable; posting errors)"],
     ar_recon_adjust, [
        dict(co="Allendale Supply", C=864300, n=4600, sd=7350, N=38000, X=12460, Y=12640, use=["no_nsf", "sd_gl", "nsf_sign"]),
        dict(co="Blanchland Supply", C=642700, n=3400, sd=5480, N=27500, X=9370, Y=9730, use=["to_sub", "no_nsf", "sd_gl"]),
        dict(co="Bellingham Supply", C=1138600, n=6200, sd=9640, N=49000, X=16580, Y=16850, use=["to_sub", "nsf_sign", "no_nsf"]),
        dict(co="Seahouses Supply", C=478900, n=2600, sd=4120, N=21000, X=7140, Y=7410, use=["to_sub", "sd_gl", "nsf_sign"]),
     ]),
    ("far-inventory-rollforward-0004", A2, "Inventory", AN,
     ["ASC 330-10 (inventory; shrinkage)", "ASC 606-10-25-30 (transfer of control: FOB destination shipments)", "ASC 606-10-55 (consignment arrangements)"],
     inv_shrinkage, [
        dict(co="Wark Outdoor Co.", B=684000, P=4215000, C=4128000, Q=659300, t=38000, g=26500, k=31000, use=["g_count", "no_t", "no_k"]),
        dict(co="Warkworth Outdoor Co.", B=512000, P=3160000, C=3094000, Q=493300, t=28500, g=19800, k=23200, use=["no_t", "no_k", "g_book"]),
        dict(co="Wooler Outdoor Co.", B=856000, P=5270000, C=5162000, Q=825100, t=47500, g=33100, k=38800, use=["g_count", "g_book", "no_t"]),
        dict(co="Glenridding Outdoor Co.", B=398000, P=2455000, C=2404000, Q=384000, t=22100, g=15400, k=18100, use=["g_count", "no_k", "g_book"]),
     ]),
    ("far-ppe-rollforward-0004", A2, "Property, plant and equipment", AN,
     ["ASC 360-10-30 (cost of property, plant and equipment: sales tax, installation and testing)", "ASC 360-10-40 (derecognition at cost with accumulated depreciation)", "ASC 360-10 (property, plant and equipment; repairs and maintenance)"],
     ppe_rollforward_gross, [
        dict(co="Threlkeld Co.", G0=4260000, A=815000, ip=420000, r=46000, st=25200, it=31000, cv=72000, cs=265000, sp=80000, fd=94000, use=["rep", "cv", "scrap"]),
        dict(co="Troutbeck Co.", G0=3180000, A=607000, ip=310000, r=34000, st=18600, it=23000, cv=54000, cs=198000, sp=61000, fd=70000, use=["inst", "sale_price", "rep"]),
        dict(co="Wythburn Co.", G0=5640000, A=1078000, ip=560000, r=61000, st=33600, it=41000, cv=96000, cs=352000, sp=104000, fd=125000, use=["inst", "scrap", "cv"]),
        dict(co="Watendlath Co.", G0=2370000, A=452000, ip=230000, r=25000, st=13800, it=17000, cv=40000, cs=147000, sp=45000, fd=52000, use=["sale_price", "inst", "scrap"]),
     ]),
    # ── Area III Analysis ──
    ("far-accounting-errors-0007", A3, "Accounting changes and error corrections", AN,
     ["ASC 250-10-45-23 (correction of an error in previously issued financial statements: restatement)", "ASC 250-10-45-17 (change in accounting estimate applied prospectively)", "ASC 606-10-25-23 (revenue recognized when control transfers; contract liabilities)"],
     restated_ni, [
        dict(co="Ambleside Co.", N=1284000, d=96000, i=28000, rr=60000, we=44000, use=["pretax", "estimate", "no_int"]),
        dict(co="Buttermere Co.", N=946000, d=72000, i=20000, rr=48000, we=36000, use=["pretax", "estimate", "rent_sign"]),
        dict(co="Caldbeck Co.", N=1652000, d=124000, i=36000, rr=84000, we=52000, use=["rent_sign", "int_sign", "no_int"]),
        dict(co="Ennerdale Co.", N=718000, d=56000, i=16000, rr=36000, we=28000, use=["estimate", "rent_sign", "int_sign"]),
     ]),
    ("far-subsequent-events-0010", A3, "Subsequent events", AN,
     ["ASC 855-10-25 (recognized and nonrecognized subsequent events)", "ASC 855-10-55 (examples: settlement of litigation; events after the balance sheet date)", "ASC 460-10 (product warranties)"],
     se_liabilities, [
        dict(co="Eskdale Homewares", L=3460000, a=240000, sx=185000, w=72000, jd=9, x=60000, Dv=150000, Bl=500000, use=["warr_none", "keep", "div"]),
        dict(co="Hawkshead Homewares", L=2580000, a=180000, sx=139000, w=54000, jd=14, x=45000, Dv=110000, Bl=375000, use=["div", "new_suit", "loan"]),
        dict(co="Loweswater Homewares", L=4720000, a=330000, sx=254000, w=98000, jd=7, x=82000, Dv=205000, Bl=680000, use=["warr_none", "div", "keep"]),
        dict(co="Mardale Homewares", L=1940000, a=135000, sx=104000, w=41000, jd=17, x=46000, Dv=85000, Bl=280000, use=["keep", "new_suit", "div"]),
     ]),
]

WORD_ITEMS = [
    mcq("far-contingencies-0011", A3, "Contingencies and commitments", RU,
        ["ASC 450-30-25-1 (gain contingencies not recognized before realization)", "ASC 450-30-50-1 (disclosure of gain contingencies, avoiding misleading implications)"],
        """In November, Year 2, a jury awarded Bamburgh Corp. $2,350,000 of damages in its patent infringement suit against a competitor. The competitor has appealed. Bamburgh's counsel expects the award to be upheld, but nothing will be paid until the appeal is decided, probably in Year 4. How should Bamburgh report the award in its December 31, Year 2, financial statements?""",
        [("Disclose it in the notes, without recognizing a gain or a receivable", "Correct. A gain contingency is not recognized until it is realized or realizable, which an award under appeal is not. It is disclosed, with care to avoid misleading implications about the likelihood that it will be realized."),
         ("Recognize a $2,350,000 gain and receivable, since counsel expects the award to stand", "Counsel's confidence doesn't make a gain contingency realizable. Recognizing it could record income before it is realized, which ASC 450-30 doesn't permit."),
         ("Recognize a gain equal to the award's present value, discounted to its expected payment in Year 4", "Discounting doesn't solve the problem: a gain contingency isn't recognized at any amount until it is realized or realizable."),
         ("Neither recognize nor mention it, because GAAP doesn't allow gain contingencies to be disclosed", "Gain contingencies may be disclosed, and adequate disclosure is made; the disclosure must simply avoid misleading implications about the likelihood of realization.")],
        "A",
        """Under ASC 450-30, a gain contingency is not reflected in the financial statements, because recognizing it could mean recognizing income before it is realized. A jury award that the defendant has appealed remains a contingency until the appeal is resolved and payment is realizable. Adequate disclosure is made in the notes, worded to avoid misleading implications about the likelihood that the gain will be realized. The loss-contingency rules (accrual when a loss is probable and estimable) do not apply symmetrically to gains."""),
    mcq("far-revenue-five-step-0002", A3, "Revenue recognition", RU,
        ["ASC 606-10-25-1 (criteria for identifying a contract with a customer)", "ASC 606-10-25-2 (contracts may be written, oral or implied by customary business practices)", "ASC 606-10-32 (variable consideration)"],
        """Belford Tooling agrees to build and sell custom molds to a new customer for $640,000. Which one of the following facts, by itself, would mean that the arrangement is not yet a contract with a customer to which Belford applies the ASC 606 five-step model?""",
        [("The agreement is oral, which is the customary practice in the customer's industry", "A contract can be written, oral or implied by customary business practices, so an oral agreement can still be a contract under ASC 606."),
         ("The customer's finances make it unlikely Belford will collect most of the price", "Correct. Step 1 requires that it be probable the entity will collect substantially all of the consideration it is entitled to. Until that is met, the arrangement isn't a contract and consideration received is a liability."),
         ("$64,000 of the price is a bonus that is payable only if the molds are delivered early", "A bonus is variable consideration, which is estimated and constrained in step 3; it doesn't stop the arrangement from being a contract."),
         ("Belford will build and deliver the molds over two of its annual reporting periods", "Timing of performance affects when revenue is recognized (step 5), not whether a contract exists.")],
        "B",
        """Step 1 of the five-step model identifies a contract with a customer. Under ASC 606-10-25-1, a contract exists only if the parties have approved it (in writing, orally or by customary practice) and are committed to perform, each party's rights and the payment terms can be identified, the contract has commercial substance, and it is probable the entity will collect substantially all of the consideration to which it will be entitled. A customer that is unlikely to pay fails the collectibility criterion. Variable consideration and performance spread over several periods are dealt with in later steps."""),
    mcq("far-nfp-promises-to-give-0002", A3, "Revenue recognition", RU,
        ["ASC 958-605-25 (conditional promises to give: barrier and right of return or release, as amended by ASU 2018-08)", "ASC 958-310-50 (disclosure of conditional promises to give)"],
        """In October, Year 1, a foundation promised Chatton Literacy Center, a not-for-profit entity, $150,000 for its tutoring program, to be paid only if Chatton raises $150,000 in new gifts from other donors by June 30, Year 2; if Chatton falls short, the foundation will pay nothing. By December 31, Year 1, Chatton had raised $95,000 toward the match, and its development director is unsure whether the rest will come in by the deadline. How should Chatton report the foundation's promise in its Year 1 financial statements?""",
        [("As $150,000 of contribution revenue with donor restrictions, because the gift is for the tutoring program", "A purpose restriction limits how a gift is used once it is recognized. This promise depends on a barrier (the match) and releases the foundation if it isn't met, so it is conditional and isn't recognized yet."),
         ("As a $150,000 receivable, offset by a refundable advance until the match is reached", "A refundable advance arises only when cash is received before a condition is met. Chatton has received nothing, so there is no asset or liability to record."),
         ("As no contribution revenue yet, with the promise disclosed in the notes", "Correct. The promise has a measurable barrier and a release from obligation if the barrier isn't overcome, so it is conditional. It is recognized when the match is reached, and conditional promises are disclosed meanwhile."),
         ("As $95,000 of contribution revenue, matching the share of the gifts already raised", "Partial recognition fits a promise that pays dollar for dollar as gifts come in. This one pays nothing unless the whole $150,000 is raised, so none of the barrier has been overcome.")],
        "C",
        """Under ASC 958-605 as amended by ASU 2018-08, a promise to give is conditional if the agreement contains a barrier the recipient must overcome and a right of return or release from the obligation if it doesn't. A matching requirement with an all-or-nothing deadline is such a barrier. A conditional promise is recognized as contribution revenue only when the barrier is overcome; until then, the recipient discloses it (the total amount and a description). Donor restrictions on purpose are a separate question that arises only once a contribution is recognized."""),
    mcq("far-uncertain-tax-positions-0002", A3, "Accounting for income taxes", RU,
        ["ASC 740-10-25 (uncertain tax positions: recognition, and subsequent recognition when new information becomes available)", "ASC 740-10-35 (subsequent measurement of uncertain tax positions)", "ASC 855-10 (subsequent events)"],
        """At December 31, Year 2, Corbridge Corp. recognized no benefit for a deduction it took on its Year 2 tax return, because it concluded the deduction would likely be disallowed if examined. On February 12, Year 3, before its Year 2 financial statements were issued, a federal court decided another taxpayer's case with nearly identical facts in the taxpayer's favor, and Corbridge now expects its deduction to be sustained. How should Corbridge reflect this development?""",
        [("Adjust its Year 2 statements, because the ruling clarifies tax law that existed at year-end", "ASC 740 overrides the general subsequent-events model for uncertain tax positions: a change in judgment from information that arises after the reporting date is recognized in the period it arises, not in the earlier statements."),
         ("Recognize the benefit only when the statute of limitations on the Year 2 return expires", "Expiry of the statute of limitations is one way a position can become effectively settled, but new information that changes the judgment is enough on its own."),
         ("Restate its Year 2 statements in Year 3 as the correction of an error", "The Year 2 judgment was reasonable on the information then available, so it wasn't an error, and nothing is restated."),
         ("Recognize the benefit in Year 3, when the new information became available", "Correct. Recognition, derecognition and measurement of a tax position reflect the information available at the reporting date; a change in judgment caused by information arising later, even before the statements are issued, is recognized in the period in which the information arises.")],
        "D",
        """ASC 740-10 requires an entity to recognize the benefit of a tax position only when it is more likely than not to be sustained on examination, based on the information available at the reporting date. When new information, such as a court decision in a similar case, changes that judgment, the change is recognized in the period in which the new information becomes available. This applies even when the information arrives after the balance sheet date but before the statements are issued, so Corbridge recognizes the benefit in Year 3 rather than adjusting its Year 2 statements. The Year 2 judgment wasn't an error, so there is no restatement."""),
    mcq("far-lessee-residual-value-0001", A3, "Lessee accounting", RU,
        ["ASC 842-10-30-5 (lease payments: purchase options reasonably certain to be exercised; amounts probable of being owed under residual value guarantees)", "ASC 842-20-30-1 (initial measurement of the lease liability)"],
        """Budle Co. leases a delivery truck from a dealer for four years. Budle guarantees the dealer that the truck will be worth at least $18,000 at the end of the lease and will pay any shortfall; at commencement, it expects the truck to be worth $13,000 at that date. The lease also lets Budle buy the truck at the end of the lease for $15,000, which Budle does not expect to do. Besides the fixed monthly rent, what does Budle include in the lease payments used to measure its lease liability at commencement?""",
        [("The $5,000 it expects to owe under the residual value guarantee", "Correct. A lessee's lease payments include amounts it is probable of owing under a residual value guarantee: the $18,000 guaranteed less the $13,000 expected value."),
         ("The full $18,000 residual value it has guaranteed to the dealer", "Only the amount probable of being owed under the guarantee is included, not the whole guaranteed value."),
         ("The $15,000 exercise price of the option to buy the truck", "An option's exercise price is included only if the lessee is reasonably certain to exercise it, and Budle doesn't expect to."),
         ("Nothing more, because a guarantee is disclosed rather than measured", "A lessee's residual value guarantee is part of the lease payments to the extent amounts are probable of being owed.")],
        "A",
        """Under ASC 842-10-30-5, lease payments include fixed payments, the exercise price of a purchase option the lessee is reasonably certain to exercise, and, for a lessee, amounts probable of being owed under residual value guarantees. Budle guarantees $18,000 and expects the truck to be worth $13,000, so it expects to owe $5,000, which is included. The $15,000 purchase option is excluded because Budle isn't reasonably certain to exercise it."""),
    mcq("far-lessee-classification-0002", A3, "Lessee accounting", RU,
        ["ASC 842-10-25-2 (lease classification criteria for lessees)", "ASC 842-10-55-2 (one reasonable approach: 75% of economic life, 90% of fair value, commencement in the last 25% of economic life)"],
        """Etal Co. is the lessee in each of the following leases. None transfers ownership, includes a residual value guarantee or is for an asset specialized to Etal's needs. Etal treats 75% or more of an asset's total economic life as a major part of it, 90% or more of its fair value as substantially all of it, and a commencement date in the last 25% of an asset's total economic life as at or near its end. Which lease should Etal classify as a finance lease?""",
        [("A three-year lease of a used press with a 20-year total life, 4 years of it left, payments worth 40% of its value", "The lease covers 75% of the press's remaining life, but it begins in the last 25% of the press's total life, so the economic-life test isn't applied; the payments are well short of substantially all of its fair value. It is an operating lease."),
         ("A three-year lease of a van with a five-year life and an option to buy it then for $500, when it should be worth $9,000", "Correct. An option priced far below the van's expected value makes Etal reasonably certain to exercise it, so the lease meets the purchase-option criterion and is a finance lease."),
         ("A four-year lease of a forklift with a ten-year life, payments worth 85% of its value and an option to buy at fair value", "The term is 40% of the forklift's life and the payments are 85% of its fair value, under 90%. An option to buy at fair value gives no incentive to exercise. It is an operating lease."),
         ("A six-year lease of a loader with a ten-year life, payments worth 70% of its value and a renewal option at market rent", "Six years is 60% of the loader's life and the payments are 70% of its fair value. A renewal at market rent gives no economic incentive to renew, so the term stays six years. It is an operating lease.")],
        "B",
        """A lessee classifies a lease as a finance lease if it meets any one of the ASC 842-10-25-2 criteria: transfer of ownership, a purchase option the lessee is reasonably certain to exercise, a term for a major part of the asset's remaining economic life (not applied when the lease begins at or near the end of that life), payments worth substantially all of its fair value, or a specialized asset. A $500 option on a van expected to be worth $9,000 is one Etal is reasonably certain to exercise. The press lease begins in the last 25% of the press's 20-year life (16 years have passed), so its 75% coverage of the remaining life doesn't count. The forklift and loader leases fall short of every threshold."""),
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
            print(f"{it['id']}: key letter {it['answer']} (word item)")
    if failed:
        sys.exit(1)
    warnings = audit(items)
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    tally = {}
    for it in items:
        for v in [it] + list(it.get("variants") or []):
            tally[v["answer"]] = tally.get(v["answer"], 0) + 1
    v0 = {}
    for it in items:
        v0[it["answer"]] = v0.get(it["answer"], 0) + 1
    print("version-0 keys", dict(sorted(v0.items())), "all versions", dict(sorted(tally.items())))
    if "--dry-run" in sys.argv:
        print("dry run: nothing written")
        return
    write_items(items, CONTENT)


if __name__ == "__main__":
    main()
