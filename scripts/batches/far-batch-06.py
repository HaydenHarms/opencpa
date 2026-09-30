"""FAR batch 06 — 25 items written from scratch for the blueprint tasks with fewer than two items
(scripts/far-coverage.py), including the gaps the batch 05 review named: fund determination, the NFP statement of
financial position, NFP cash flows and notes, amortized-cost investments and debt covenants. Target skill mix
3 / 14 / 8. Scope and skill tags follow the AICPA CPA Exam Blueprints effective January 2026.

Numeric items ship with three variants each (method as in far-variants-03.py): each item is a builder, parameter
set 0 is the item and sets 1-3 are its variants, and every family must move the key's letter.

Run: python3 scripts/batches/far-batch-06.py   See docs/reviews/far-batch-06.md.
Every numeric answer and distractor below is computed in code (Decimal, rounded half up).
"""
import os
import sys
from decimal import Decimal as D

from common import AN, AP, RU, attach_variants, audit, finalize, fix_articles, mcq as _mcq, variant, write_items
from variants import m, pct, pick, rd

A1 = "Area I — Financial Reporting"
A2 = "Area II — Select Balance Sheet Accounts"
A3 = "Area III — Select Transactions"
NOTE = "Batch 06. Written from scratch; answers solved and every number and distractor computed in code."
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


def ratio(x, places="0.01"):
    return str(rd(x, places))


# ── Area I ───────────────────────────────────────────────────────────────


def working_capital(p):
    co, s = p["co"], short(p["co"])
    ca = p["cash"] + p["ar"] - p["allow"] + p["inv"] + p["prepaid"]
    cl = p["ap"] + p["wages"] + p["cp"] + p["div"] + p["unearned"]
    key_v = ca - cl
    pool = {
        "restricted": (m(key_v + p["restricted"]), f"Counts the {m(p['restricted'])} held by the trustee as a current asset. Cash restricted to retiring long-term debt is noncurrent."),
        "dtl": (m(key_v - p["dtl"]), f"Treats the {m(p['dtl'])} deferred tax liability as current. Deferred taxes are always classified as noncurrent."),
        "no_cp": (m(key_v + p["cp"]), f"Classifies the whole note as noncurrent. The {m(p['cp'])} installment due next July 1 is a current liability."),
        "whole_note": (m(key_v - (p["note"] - p["cp"])), f"Classifies the whole {m(p['note'])} note as current. Only the installment due within one year is current."),
        "gross_ar": (m(key_v + p["allow"]), f"Uses gross accounts receivable. Receivables are reported net of the {m(p['allow'])} allowance for credit losses."),
    }
    key = (m(key_v), f"Correct. Current assets {m(ca)} − current liabilities {m(cl)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s adjusted trial balance at December 31, Year 3, includes these accounts: cash {m(p['cash'])}; cash held by a trustee under a bond indenture to retire long-term bonds in Year 6, {m(p['restricted'])}; accounts receivable {m(p['ar'])}; allowance for credit losses {m(p['allow'])}; inventory {m(p['inv'])}; prepaid rent covering the next twelve months {m(p['prepaid'])}; equipment, net of depreciation, {m(p['equip'])}; accounts payable {m(p['ap'])}; accrued wages {m(p['wages'])}; a note payable of {m(p['note'])}, repayable in equal annual installments of {m(p['cp'])} each July 1; dividends payable {m(p['div'])}; unearned revenue for services to be performed in Year 4, {m(p['unearned'])}; and a deferred tax liability of {m(p['dtl'])}. {s} is preparing a classified balance sheet. What is {s}'s working capital at December 31, Year 3?""",
        choices, ans,
        f"""Current assets: cash {m(p['cash'])} + receivables net of the allowance {m(p['ar'] - p['allow'])} + inventory {m(p['inv'])} + prepaid rent {m(p['prepaid'])} = {m(ca)}. The trustee-held cash is restricted to retiring long-term debt, so it is noncurrent. Current liabilities: accounts payable {m(p['ap'])} + accrued wages {m(p['wages'])} + the note installment due next July 1 {m(p['cp'])} + dividends payable {m(p['div'])} + unearned revenue {m(p['unearned'])} = {m(cl)}. The rest of the note and the deferred tax liability are noncurrent. Working capital = {m(ca)} − {m(cl)} = {m(key_v)}.""",
    )


def equity_statement(p):
    co, s = p["co"], short(p["co"])
    key_v = p["beg"] + p["ni"] - p["decl"] - p["ts"] + p["px"] + p["oci"] + p["issue"]
    pool = {
        "stock_div": (m(key_v - p["sdfv"]), f"Subtracts the {m(p['sdfv'])} stock dividend. A stock dividend moves amounts from retained earnings to paid-in capital and doesn't change total equity."),
        "paid_div": (m(key_v + p["decl"] - p["paid"]), f"Subtracts only the {m(p['paid'])} of dividends paid. Equity falls by the full {m(p['decl'])} declared; the unpaid part is a liability."),
        "no_oci": (m(key_v - p["oci"]), f"Leaves out the {m(p['oci'])} of other comprehensive income. It isn't in net income, but it increases accumulated other comprehensive income, part of equity."),
        "reissue_cost": (m(key_v - p["px"] + p["cost"]), f"Adds back only the {m(p['cost'])} cost of the reissued treasury shares. Equity increases by the full {m(p['px'])} received."),
    }
    key = (m(key_v), f"Correct. {m(p['beg'])} + {m(p['ni'])} − {m(p['decl'])} − {m(p['ts'])} + {m(p['px'])} + {m(p['oci'])} + {m(p['issue'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s total stockholders' equity was {m(p['beg'])} at January 1, Year 2. During Year 2, {s} reported net income of {m(p['ni'])}; declared cash dividends of {m(p['decl'])}, of which {m(p['paid'])} had been paid by December 31; distributed a 10% stock dividend when the shares distributed had a fair value of {m(p['sdfv'])}; bought treasury shares for {m(p['ts'])} and later reissued treasury shares that had cost {m(p['cost'])} for {m(p['px'])}; reported other comprehensive income of {m(p['oci'])}, net of tax, from an unrealized holding gain on available-for-sale debt securities; and issued new common shares for {m(p['issue'])} in cash. What total stockholders' equity should {s} report at December 31, Year 2?""",
        choices, ans,
        f"""Total equity rises by net income ({m(p['ni'])}), other comprehensive income ({m(p['oci'])}), the {m(p['issue'])} share issuance and the {m(p['px'])} received on reissuing treasury shares. It falls by dividends declared ({m(p['decl'])}; whether paid doesn't matter) and the {m(p['ts'])} treasury share purchase. The stock dividend only reclassifies amounts within equity. {m(p['beg'])} + {m(p['ni'])} − {m(p['decl'])} − {m(p['ts'])} + {m(p['px'])} + {m(p['oci'])} + {m(p['issue'])} = {m(key_v)}.""",
    )


def consolidated_inventory(p):
    P, S = p["parent"], p["sub"]
    ps, ss = short(P), short(S)
    down_profit = p["down"] - p["down"] * 100 / (100 + p["markup"])
    up_profit = p["up"] * p["margin"] / 100
    assert down_profit == int(down_profit) and up_profit == int(up_profit)
    down_profit, up_profit = int(down_profit), int(up_profit)
    total = p["p_inv"] + p["s_inv"]
    key_v = total - down_profit - up_profit
    wrong_down = p["down"] * p["markup"] // 100
    pool = {
        "markup_price": (m(total - wrong_down - up_profit), f"Computes the profit on {ps}'s sales as {p['markup']}% of the {m(p['down'])} selling price. A {p['markup']}% markup on cost is {p['markup']}/{100 + p['markup']} of the selling price, or {m(down_profit)}."),
        "up_only": (m(total - up_profit), f"Eliminates only the profit on goods {ss} sold to {ps}. The unrealized profit on {ps}'s sales to its subsidiary is eliminated too."),
        "down_only": (m(total - down_profit), f"Eliminates only the profit on {ps}'s sales to {ss}. Unrealized profit on the subsidiary's sales to the parent is also eliminated in full."),
        "full_price": (m(total - p["down"] - p["up"]), "Removes the full intercompany prices. Only the unrealized profit is eliminated; the goods stay in consolidated inventory at the selling affiliate's cost."),
        "none": (m(total), "Adds the two inventories without eliminating the unrealized intercompany profit."),
    }
    key = (m(key_v), f"Correct. {m(total)} − {m(down_profit)} unrealized profit on {ps}'s sales − {m(up_profit)} on {ss}'s sales.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{P} owns 100% of {S.rstrip('.')}. During Year 1, {ps} sold {ss} goods for {m(p['ic'])} at its usual price of cost plus {p['markup']}%, and {ss} sold {ps} goods at its usual gross margin of {p['margin']}% of the selling price. At December 31, Year 1, {ss}'s inventory of {m(p['s_inv'])} includes goods bought from {ps} for {m(p['down'])}, and {ps}'s inventory of {m(p['p_inv'])} includes goods bought from {ss} for {m(p['up'])}. In preparing the consolidated balance sheet, what amount should {ps} report as inventory at December 31, Year 1?""",
        choices, ans,
        f"""Consolidated inventory is carried at the group's original cost, so the unrealized intercompany profit in ending inventory is eliminated, from both directions when the subsidiary is wholly owned. Goods from {ps}: a {p['markup']}% markup on cost is {p['markup']}/{100 + p['markup']} of the price, so {m(p['down'])} × {p['markup']}/{100 + p['markup']} = {m(down_profit)}. Goods from {ss}: {m(p['up'])} × {p['margin']}% = {m(up_profit)}. Inventory = {m(p['p_inv'])} + {m(p['s_inv'])} − {m(down_profit)} − {m(up_profit)} = {m(key_v)}. The {m(p['ic'])} of intercompany sales affects the elimination of sales and cost of goods sold, not ending inventory.""",
    )


def nfp_sfp_adjust(p):
    org, s = p["org"], short(p["org"])
    key_v = p["draft"] + p["board"] - p["pledge"] - p["cond"] + p["release"]
    pool = {
        "board": (m(key_v - p["board"]), f"Leaves the {m(p['board'])} quasi-endowment in net assets with donor restrictions. A board designation is self-imposed, so those net assets stay without donor restrictions."),
        "no_release": (m(key_v - p["release"]), f"Records no release for the {m(p['release'])} spent on medical supplies. Meeting the donor's purpose releases the restriction."),
        "cond": (m(key_v + p["cond"]), f"Keeps the {m(p['cond'])} grant as revenue. A promise that depends on a barrier (raising matching gifts) and lets the grantor keep its money if the barrier isn't met is conditional, so it isn't recognized yet."),
        "pledge": (m(key_v + p["pledge"]), f"Leaves the {m(p['pledge'])} promise in net assets without donor restrictions. The donor restricted it to a program, and it is also due in a later period."),
    }
    key = (m(key_v), f"Correct. {m(p['draft'])} + {m(p['board'])} − {m(p['pledge'])} − {m(p['cond'])} + {m(p['release'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, reports net assets without donor restrictions of {m(p['draft'])} in its draft December 31, Year 1, statement of financial position. Reviewing the supporting records, the controller finds: (1) {m(p['board'])} that the board of trustees set aside as a quasi-endowment is reported in net assets with donor restrictions; (2) an unconditional promise of {m(p['pledge'])}, due in Year 2, that the donor restricted to {s}'s Year 2 youth program is reported in net assets without donor restrictions; (3) a {m(p['cond'])} grant that the grantor will pay only if {s} raises matching gifts by June 30, Year 2, is reported as a receivable and as revenue without donor restrictions; and (4) {m(p['release'])} of gifts restricted to buying medical supplies was spent on those supplies in December, but no release from restrictions was recorded. After correcting the draft, what should {s} report as net assets without donor restrictions?""",
        choices, ans,
        f"""(1) Board designations are not donor restrictions: add {m(p['board'])}. (2) The promise is restricted by purpose and time, so it belongs in net assets with donor restrictions: subtract {m(p['pledge'])}. (3) The grant has a barrier and a right of release, so it is conditional and is not recognized until the matching gifts are raised: subtract {m(p['cond'])}. (4) Spending on the donor's purpose releases {m(p['release'])} to net assets without donor restrictions: add it. {m(p['draft'])} + {m(p['board'])} − {m(p['pledge'])} − {m(p['cond'])} + {m(p['release'])} = {m(key_v)}.""",
    )


def nfp_scf_adjust(p):
    org, s = p["org"], short(p["org"])
    key_v = p["draft"] - p["endow"] - 2 * p["gain"] - p["land"]
    assert key_v - p["unres"] > 0
    pool = {
        "no_endow": (m(key_v + p["endow"]), f"Leaves the {m(p['endow'])} endowment gift in operating activities. Cash contributions restricted to endowment are financing activities."),
        "gain_once": (m(key_v + p["gain"]), f"Removes the {m(p['gain'])} gain from the reconciliation but doesn't subtract it. A gain on sale is subtracted from the change in net assets; the proceeds are an investing inflow."),
        "no_land": (m(key_v + p["land"]), f"Leaves the donated land in. A noncash contribution is subtracted in the reconciliation and disclosed as a noncash activity."),
        "unres_fin": (m(key_v - p["unres"]), f"Also moves the {m(p['unres'])} of unrestricted contributions to financing activities. Only contributions restricted to long-term purposes are financing inflows."),
    }
    key = (m(key_v), f"Correct. {m(p['draft'])} − {m(p['endow'])} endowment gift − 2 × {m(p['gain'])} gain − {m(p['land'])} donated land.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, prepares its statement of cash flows using the indirect method. Its draft reports net cash provided by operating activities of {m(p['draft'])}. The reconciliation starts with the change in total net assets, which includes: a {m(p['endow'])} cash gift that the donor requires {s} to hold in perpetuity, which the draft leaves in operating activities; a {m(p['gain'])} gain on the sale of investments, which the draft reconciliation adds to the change in net assets; land donated to {s}, with a fair value of {m(p['land'])}, for which the draft reconciliation makes no adjustment; and {m(p['unres'])} of cash contributions without donor restrictions. After correcting the draft, what is {s}'s net cash provided by operating activities?""",
        choices, ans,
        f"""The endowment gift is a financing inflow, so it comes out of operating activities: − {m(p['endow'])}. The gain was added instead of subtracted, so correcting it takes out twice the gain: − {m(2 * p['gain'])}. The donated land is a noncash contribution, subtracted in the reconciliation: − {m(p['land'])}. Unrestricted contributions stay in operating activities. {m(p['draft'])} − {m(p['endow'])} − {m(2 * p['gain'])} − {m(p['land'])} = {m(key_v)}.""",
    )


def nfp_liquidity(p):
    org, s = p["org"], short(p["org"])
    inv = p["endow"] + p["quasi"] + p["other"]
    key_v = p["cash"] - p["bldg"] + p["recv"] - p["lt"] + p["other"] + p["approp"]
    pool = {
        "board": (m(key_v + p["quasi"]), f"Includes the {m(p['quasi'])} quasi-endowment. The board has designated it for long-term investment, so it isn't available for general expenditure without a board action; that amount is disclosed separately."),
        "lt_recv": (m(key_v + p["lt"]), f"Includes the {m(p['lt'])} of contributions receivable due in more than one year."),
        "no_approp": (m(key_v - p["approp"]), f"Leaves out the {m(p['approp'])} of endowment return appropriated for next year's general operations, which is available within one year."),
        "bldg": (m(key_v + p["bldg"]), f"Includes the {m(p['bldg'])} of cash restricted by a donor to building construction, which can't be used for general expenditure."),
    }
    key = (m(key_v), f"Correct. Cash {m(p['cash'] - p['bldg'])} + receivables due within one year {m(p['recv'] - p['lt'])} + other investments {m(p['other'])} + endowment appropriation {m(p['approp'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{org}, a not-for-profit entity, is preparing its note on the liquidity and availability of financial assets. At June 30, Year 2, it holds: cash of {m(p['cash'])}, including {m(p['bldg'])} that a donor restricted to constructing a new building over the next three years; contributions receivable without donor restrictions of {m(p['recv'])}, of which {m(p['lt'])} is due after June 30, Year 3; and investments of {m(inv)}, made up of a donor-restricted endowment of {m(p['endow'])} whose original gift must be held in perpetuity, a quasi-endowment of {m(p['quasi'])} that the board designated for long-term investment and does not intend to spend from beyond amounts appropriated under its spending policy, and {m(p['other'])} of other investments. Under its spending policy, {s} will appropriate {m(p['approp'])} of endowment return for general operations in the coming year. What amount should the note report as financial assets available to meet general expenditures within one year?""",
        choices, ans,
        f"""The note reports financial assets available for general expenditure within one year of the balance sheet date. Cash available: {m(p['cash'])} − {m(p['bldg'])} restricted to the building = {m(p['cash'] - p['bldg'])}. Receivables due within one year: {m(p['recv'])} − {m(p['lt'])} = {m(p['recv'] - p['lt'])}. Investments: the endowment corpus and the board-designated quasi-endowment are excluded, leaving {m(p['other'])}; the {m(p['approp'])} appropriated from the endowment for next year's operations is added. Total = {m(key_v)}.""",
    )


def modified_cash(p):
    co, s = p["co"], short(p["co"])
    key_v = p["rec"] - p["paid"] - p["dep"]
    pool = {
        "cash_basis": (m(p["rec"] - p["paid"] - p["equip"]), f"Expenses the {m(p['equip'])} of equipment when paid. {s}'s modified cash basis capitalizes equipment and depreciates it."),
        "accrual": (m(key_v + p["ar"] - p["wages"]), f"Converts to the accrual basis by adding the {m(p['ar'])} increase in receivables and accruing the {m(p['wages'])} of wages. This basis doesn't record receivables or accrued expenses."),
        "no_dep": (m(key_v + p["dep"]), "Capitalizes the equipment but records no depreciation. The basis depreciates capitalized equipment."),
        "wages": (m(key_v - p["wages"]), f"Accrues the {m(p['wages'])} of unpaid wages. Under this basis, expenses other than depreciation are recorded when paid."),
    }
    key = (m(key_v), f"Correct. {m(p['rec'])} − {m(p['paid'])} − {m(p['dep'])} depreciation.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} prepares its financial statements on a modified cash basis: it capitalizes purchases of equipment and depreciates them, and it otherwise records revenues when cash is received and expenses when cash is paid. In Year 3 it collected {m(p['rec'])} from clients and paid {m(p['paid'])} of operating expenses. It also paid {m(p['equip'])} for new equipment in January; depreciation on the equipment for Year 3 is {m(p['dep'])}. At year-end, employees had earned {m(p['wages'])} of wages that {s} will pay in January, Year 4, and client receivables had increased by {m(p['ar'])} during the year. What excess of revenues over expenses should {s} report in its Year 3 statement of revenues and expenses—modified cash basis?""",
        choices, ans,
        f"""Under {s}'s modified cash basis, revenues are the {m(p['rec'])} collected and expenses are the {m(p['paid'])} paid, plus depreciation on the capitalized equipment ({m(p['dep'])}). The equipment purchase itself isn't an expense, and the unpaid wages and the increase in receivables aren't recorded. {m(p['rec'])} − {m(p['paid'])} − {m(p['dep'])} = {m(key_v)}.""",
    )


def roe(p):
    co, s = p["co"], short(p["co"])
    div = p["pref"] * p["rate"] // 100
    avg_c = (p["beg"] + p["end"]) / D(2) - p["pref"]
    avg_t = (p["beg"] + p["end"]) / D(2)
    f = lambda x: pct(x, "0.1") if pct(x).endswith("%") else x
    key_v = (p["ni"] - div) / avg_c
    vals = {
        "no_pref": (p["ni"] / avg_c, f"Doesn't subtract the {m(div)} preferred dividend. Return on common equity uses income available to common stockholders."),
        "total_eq": ((p["ni"] - div) / avg_t, f"Divides by average total equity, including the {m(p['pref'])} of preferred stock. The denominator is common equity only."),
        "ending": ((p["ni"] - div) / (p["end"] - p["pref"]), "Divides by ending common equity instead of the average for the year."),
        "ni_total": (p["ni"] / avg_t, "Divides net income by average total equity, which is return on total equity."),
    }
    one = lambda x: f"{rd(x * 100, '0.1')}%"
    pool = {k: (one(v), r) for k, (v, r) in vals.items()}
    key = (one(key_v), f"Correct. ({m(p['ni'])} − {m(div)}) ÷ {m(avg_c)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} reports Year 2 net income of {m(p['ni'])}. Its total stockholders' equity was {m(p['beg'])} at January 1 and {m(p['end'])} at December 31. Both amounts include {m(p['pref'])} of {p['rate']}% cumulative, nonconvertible preferred stock that was outstanding all year, and {s} declared and paid the full year's preferred dividend. What was {s}'s return on common stockholders' equity for Year 2, based on average common equity?""",
        choices, ans,
        f"""Income available to common stockholders = {m(p['ni'])} − {m(div)} preferred dividend ({p['rate']}% × {m(p['pref'])}) = {m(p['ni'] - div)}. Average common equity = ({m(p['beg'])} + {m(p['end'])}) ÷ 2 − {m(p['pref'])} preferred = {m(avg_c)}. Return on common equity = {m(p['ni'] - div)} ÷ {m(avg_c)} = {one(key_v)}.""",
    )


def debt_ratio(p):
    co, s = p["co"], short(p["co"])
    liab = p["cl"] + p["ltd"] + p["ol"] + p["mrp"]
    two = lambda x: ratio(D(x))
    key_v = D(liab) / p["assets"]
    pool = {
        "no_mrp": (two(D(liab - p["mrp"]) / p["assets"]), f"Leaves the {m(p['mrp'])} of mandatorily redeemable preferred shares in equity. Shares the issuer must redeem for cash on a fixed date are liabilities."),
        "no_ol": (two(D(liab - p["ol"]) / p["assets"]), f"Leaves out the {m(p['ol'])} of operating lease liabilities, which are liabilities on the balance sheet."),
        "neither": (two(D(liab - p["ol"] - p["mrp"]) / p["assets"]), "Leaves out both the operating lease liabilities and the mandatorily redeemable preferred shares."),
        "de": (two(D(liab) / (p["assets"] - liab)), "Divides total liabilities by stockholders' equity, which is the debt-to-equity ratio."),
    }
    key = (two(key_v), f"Correct. ({m(p['cl'])} + {m(p['ltd'])} + {m(p['ol'])} + {m(p['mrp'])}) ÷ {m(p['assets'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s balance sheet reports total assets of {m(p['assets'])}. Its obligations are current liabilities of {m(p['cl'])}, including {m(p['unearned'])} of unearned revenue; long-term debt of {m(p['ltd'])}; and operating lease liabilities of {m(p['ol'])}. {s} also has {m(p['mrp'])} of preferred shares that it must redeem for cash on a fixed date in Year 6, which its draft balance sheet presents within stockholders' equity. After any correction needed, what is {s}'s total debt ratio (total liabilities divided by total assets), rounded to two decimal places?""",
        choices, ans,
        f"""Preferred shares that must be redeemed for cash on a fixed date are mandatorily redeemable financial instruments, reported as liabilities, so {m(p['mrp'])} moves out of equity. Operating lease liabilities and unearned revenue are liabilities too. Total liabilities = {m(p['cl'])} + {m(p['ltd'])} + {m(p['ol'])} + {m(p['mrp'])} = {m(liab)}; total assets are unchanged. {m(liab)} ÷ {m(p['assets'])} = {two(key_v)}.""",
    )


# ── Area II ──────────────────────────────────────────────────────────────


def proof_of_cash(p):
    co, s = p["co"], short(p["co"])
    key_v = p["bank"] - p["dit_b"] + p["dit_e"] - p["err"]
    book = key_v - p["note"]
    pool = {
        "no_dit": (m(p["bank"] - p["err"]), f"Ignores the deposits in transit. May's {m(p['dit_b'])} reached the bank in June but is a May receipt, and June's {m(p['dit_e'])} is a June receipt the bank hasn't recorded."),
        "dit_reversed": (m(p["bank"] + p["dit_b"] - p["dit_e"] - p["err"]), "Reverses the deposit-in-transit adjustments: May's deposit in transit is subtracted from June's bank credits and June's is added."),
        "keep_err": (m(key_v + p["err"]), f"Leaves in the {m(p['err'])} the bank credited in error. Another company's deposit is not {s}'s receipt."),
        "book_only": (m(book), f"Uses the cash receipts journal as recorded. The {m(p['note'])} note collection is a June receipt that {s} hasn't recorded yet."),
    }
    key = (m(key_v), f"Correct. {m(p['bank'])} − {m(p['dit_b'])} + {m(p['dit_e'])} − {m(p['err'])}, which equals {m(book)} per books + {m(p['note'])} note collection.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} prepares a proof of cash for June. The bank statement shows June deposits and other credits of {m(p['bank'])}. Deposits in transit were {m(p['dit_b'])} at May 31 and {m(p['dit_e'])} at June 30. The June bank credits include {m(p['note'])} from a note receivable that the bank collected for {s}, which {s} hasn't recorded, and a {m(p['err'])} deposit of another company that the bank credited to {s}'s account in error. {s}'s cash receipts journal shows June receipts of {m(book)}. What are {s}'s correct cash receipts for June?""",
        choices, ans,
        f"""From the bank side: {m(p['bank'])} of June credits − {m(p['dit_b'])} May deposit in transit (a May receipt) + {m(p['dit_e'])} June deposit in transit − {m(p['err'])} bank error = {m(key_v)}. From the book side: {m(book)} recorded + {m(p['note'])} note collection not yet recorded = {m(key_v)}. The two sides agree.""",
    )


def unreconciled(p):
    co, s = p["co"], short(p["co"])
    over = p["rec_r"] - p["true_r"]
    under_bank = p["true_d"] - p["rec_d"]
    correct = p["B"] + under_bank
    K = correct + over - p["dup"]
    diff = p["B"] - K
    key_v = p["dup"] - over
    assert key_v > 0 and diff > 0
    inc = lambda x: f"{m(x)} increase"
    pool = {
        "whole_diff": (inc(diff), f"Books the whole {m(diff)} unreconciled difference. Part of it is the bank's error, which the bank corrects."),
        "no_transp": (inc(p["dup"]), f"Corrects only the duplicated check. The receipt was also recorded {m(over)} too high."),
        "transp_sign": (inc(p["dup"] + over), f"Adds the {m(over)} receipt error instead of subtracting it. The receipt was recorded as {m(p['rec_r'])} instead of {m(p['true_r'])}, overstating cash."),
        "bank_only": (inc(under_bank), f"Records only the bank's {m(under_bank)} error in the ledger. The bank corrects its own error; the ledger needs the corrections for {s}'s own recording errors."),
    }
    key = (inc(key_v), f"Correct. {m(p['dup'])} duplicated check added back − {m(over)} receipt overstatement.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s June 30 bank reconciliation shows an adjusted bank balance of {m(p['B'])} after deposits in transit and outstanding checks, and an adjusted book balance of {m(K)} after recording the bank's charges and collections, leaving an unreconciled difference of {m(diff)}. Investigating, the controller finds: a customer's check for {m(p['true_r'])} was recorded in the cash receipts journal as {m(p['rec_r'])}; check 5120, for {m(p['dup'])}, was recorded twice in the cash disbursements journal; and the bank recorded {s}'s June 18 deposit of {m(p['true_d'])} as {m(p['rec_d'])}, an error the bank has agreed to correct. What adjustment should {s} make to its general ledger cash balance?""",
        choices, ans,
        f"""Book errors: the duplicated check understated cash by {m(p['dup'])}, and the receipt recorded as {m(p['rec_r'])} instead of {m(p['true_r'])} overstated it by {m(over)}. The ledger adjustment is {m(p['dup'])} − {m(over)} = a {m(key_v)} increase, giving {m(K + key_v)}. The bank's {m(under_bank)} understatement of the deposit is corrected by the bank: {m(p['B'])} + {m(under_bank)} = {m(correct)}, so both sides agree.""",
    )


def allowance_rollforward(p):
    co, s = p["co"], short(p["co"])
    wo = p["ar_b"] + p["sales"] + p["recov"] - p["coll"] - p["ar_e"]
    key_v = p["req"] - p["al_b"] + wo - p["recov"]
    assert wo > p["recov"]
    pool = {
        "no_reinstate": (m(key_v - p["recov"]), f"Leaves the reinstatements out of the receivables rollforward, so write-offs come out {m(p['recov'])} too low ({m(wo - p['recov'])})."),
        "no_recov": (m(key_v + p["recov"]), f"Ignores the {m(p['recov'])} of recoveries in the allowance rollforward. Reinstating a written-off account credits the allowance."),
        "direct": (m(wo), f"Uses the {m(wo)} of write-offs as the expense, which is the direct write-off method."),
        "ending": (m(p["req"]), f"Uses the required {m(p['req'])} ending allowance as the expense, ignoring the balance already in the allowance."),
    }
    key = (m(key_v), f"Correct. Write-offs {m(wo)}; expense = {m(p['req'])} − {m(p['al_b'])} + {m(wo)} − {m(p['recov'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} is preparing rollforwards of its trade receivables and its allowance for credit losses for Year 2. Per the aged subledger, accounts receivable were {m(p['ar_b'])} at January 1 and {m(p['ar_e'])} at December 31. Credit sales were {m(p['sales'])}. Cash collected from customers was {m(p['coll'])}, which includes {m(p['recov'])} received on accounts written off in earlier years; {s} reinstates such an account before recording the collection. The allowance was {m(p['al_b'])} at January 1, and {s}'s expected credit loss estimate requires a balance of {m(p['req'])} at December 31. The year's write-offs are not separately recorded in the rollforward schedules. What credit loss expense should {s} record for Year 2?""",
        choices, ans,
        f"""Receivables rollforward: {m(p['ar_b'])} + {m(p['sales'])} credit sales + {m(p['recov'])} reinstated − {m(p['coll'])} collected − write-offs = {m(p['ar_e'])}, so write-offs are {m(wo)}. Allowance rollforward: {m(p['al_b'])} − {m(wo)} write-offs + {m(p['recov'])} recoveries + expense = {m(p['req'])}, so credit loss expense is {m(key_v)}.""",
    )


def ar_reconciliation(p):
    co, s = p["co"], short(p["co"])
    over = p["posted"] - p["true"]
    correct = p["S"] - p["consign"]
    G = correct + p["memo"] + over + p["consign"]
    key_v = correct + p["cb"]
    pool = {
        "gl": (m(G), "Uses the control account as recorded, before correcting it."),
        "net": (m(correct), f"Corrects both records but reports the net balance. The {m(p['cb'])} of customer credit balances is a liability, so receivables are reported without netting it."),
        "sub": (m(p["S"]), "Uses the subledger balance as recorded."),
        "no_consign": (m(p["S"] + p["cb"]), f"Doesn't remove the {m(p['consign'])} consignment invoice. Goods held by a consignee are still {s}'s inventory, not a sale."),
    }
    key = (m(key_v), f"Correct. {m(p['S'])} − {m(p['consign'])} consignment invoice + {m(p['cb'])} of credit balances reclassified.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s accounts receivable subledger shows a net balance of {m(p['S'])}, which includes customer accounts with credit balances from overpayments totaling {m(p['cb'])}. The general ledger control account shows {m(G)}. The controller's investigation finds: a {m(p['memo'])} credit memo for returned goods was posted to the customer's subledger account but not to the control account; the December 14 sales journal total of {m(p['true'])} was posted to the control account as {m(p['posted'])}; and a {m(p['consign'])} invoice was recorded in both records for goods shipped on December 30 to a dealer that holds them on consignment for {s}. Before any allowance for credit losses, what amount should {s} report as accounts receivable?""",
        choices, ans,
        f"""Control account: {m(G)} − {m(p['memo'])} credit memo − {m(over)} posting error − {m(p['consign'])} consignment invoice = {m(correct)}. Subledger: {m(p['S'])} − {m(p['consign'])} = {m(correct)}. The records now agree. The {m(p['cb'])} of credit balances is reclassified to liabilities, so accounts receivable is {m(correct)} + {m(p['cb'])} = {m(key_v)}.""",
    )


def inventory_rollforward(p):
    co, s = p["co"], short(p["co"])
    purch = p["purch"] - p["transit"]
    end = p["count"] + p["consign"] - p["shipped"]
    key_v = p["beg"] + purch + p["frt"] - p["ret"] - end
    pool = {
        "transit": (m(key_v + p["transit"]), f"Leaves the {m(p['transit'])} of goods in transit in purchases. Under FOB destination, title passes when the goods arrive in January."),
        "consign": (m(key_v + p["consign"]), f"Leaves out the {m(p['consign'])} of consigned goods, which {s} still owns."),
        "shipped": (m(key_v - p["shipped"]), f"Leaves the {m(p['shipped'])} of goods sold FOB shipping point in ending inventory. Title passed to the customer when the carrier picked them up."),
        "freight": (m(key_v - p["frt"]), f"Leaves out the {m(p['frt'])} of freight-in, which is part of the cost of inventory."),
    }
    key = (m(key_v), f"Correct. {m(p['beg'])} + {m(purch)} + {m(p['frt'])} − {m(p['ret'])} − {m(end)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} uses a periodic inventory system. For Year 1, its records show beginning inventory of {m(p['beg'])}, purchases of {m(p['purch'])} per the accounts payable subledger, freight-in of {m(p['frt'])}, and purchase returns of {m(p['ret'])}. The physical count, taken on the morning of December 31 and priced at cost, totals {m(p['count'])}. Cutoff testing finds that: purchases include {m(p['transit'])} of goods a supplier shipped FOB destination on December 30, which arrived January 5; goods costing {m(p['consign'])} held by a consignee on {s}'s behalf were not counted; and the count includes goods costing {m(p['shipped'])} that a customer's carrier picked up that afternoon under FOB shipping point terms, recorded as a Year 1 sale. What is {s}'s corrected cost of goods sold for Year 1?""",
        choices, ans,
        f"""Purchases: {m(p['purch'])} − {m(p['transit'])} in transit under FOB destination = {m(purch)}. Ending inventory: {m(p['count'])} + {m(p['consign'])} on consignment − {m(p['shipped'])} sold and shipped = {m(end)}. Cost of goods sold = {m(p['beg'])} + {m(purch)} + {m(p['frt'])} freight-in − {m(p['ret'])} returns − {m(end)} = {m(key_v)}.""",
    )


def lifo_reconciliation(p):
    co, s = p["co"], short(p["co"])
    fifo = p["sub"] - p["ret"]
    G = fifo - p["receipt"]
    key_v = fifo - p["re"]
    pool = {
        "fifo": (m(fifo), f"Reports the corrected FIFO cost. The {m(p['re'])} LIFO reserve reduces it to LIFO."),
        "sub_less": (m(p["sub"] - p["re"]), f"Doesn't remove the {m(p['ret'])} of returned goods from the subledger amount."),
        "gl_less": (m(G - p["re"]), f"Uses the general ledger balance without posting the {m(p['receipt'])} December 29 receipt."),
        "change_only": (m(fifo - (p["re"] - p["rb"])), f"Subtracts only this year's {m(p['re'] - p['rb'])} change in the reserve. The balance sheet deducts the whole reserve."),
    }
    key = (m(key_v), f"Correct. ({m(p['sub'])} − {m(p['ret'])}) − {m(p['re'])} LIFO reserve.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} keeps its perpetual inventory subledger at FIFO cost and reports inventory at LIFO, recording the difference in a LIFO reserve account. At December 31, the subledger totals {m(p['sub'])}, and the general ledger inventory account, which is also kept at FIFO, shows {m(G)}. The controller finds that goods costing {m(p['receipt'])} received on December 29 are in the subledger but the supplier's invoice was never posted to the general ledger, and that goods costing {m(p['ret'])} returned to a supplier on December 30 were recorded in the general ledger but not in the subledger. The LIFO reserve was {m(p['rb'])} at January 1, and {s}'s LIFO calculation requires a reserve of {m(p['re'])} at December 31. What amount should {s} report as inventory at December 31?""",
        choices, ans,
        f"""Corrected FIFO cost: subledger {m(p['sub'])} − {m(p['ret'])} return = {m(fifo)}; general ledger {m(G)} + {m(p['receipt'])} receipt = {m(fifo)}. The balance sheet reports LIFO: {m(fifo)} − {m(p['re'])} reserve = {m(key_v)}.""",
    )


def capex_rollforward(p):
    co, s = p["co"], short(p["co"])
    adds = p["ge"] - p["gb"] + p["sc"]
    key_v = adds - p["note"]
    assert p["ae"] - p["ab"] + p["sad"] > 0
    pool = {
        "total": (m(adds), f"Includes the {m(p['note'])} of equipment bought with a note. A noncash acquisition is disclosed, not reported as an investing cash outflow."),
        "no_disposal": (m(p["ge"] - p["gb"] - p["note"]), f"Ignores the equipment sold. Its {m(p['sc'])} cost left the account, so purchases exceed the net increase."),
        "nbv": (m(p["ge"] - p["gb"] + p["sc"] - p["sad"] - p["note"]), f"Adds back the carrying amount of the equipment sold ({m(p['sc'] - p['sad'])}) instead of its cost. The gross equipment account removes cost."),
        "net_px": (m(key_v - p["px"]), f"Nets the {m(p['px'])} of sale proceeds against the purchases. The proceeds are a separate investing inflow."),
    }
    key = (m(key_v), f"Correct. {m(p['ge'])} − {m(p['gb'])} + {m(p['sc'])} cost of equipment sold − {m(p['note'])} bought with a note.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s equipment rollforward for Year 2 shows gross equipment of {m(p['gb'])} at January 1 and {m(p['ge'])} at December 31, and accumulated depreciation of {m(p['ab'])} at January 1 and {m(p['ae'])} at December 31. During the year, {s} sold equipment that cost {m(p['sc'])}, with accumulated depreciation of {m(p['sad'])}, for {m(p['px'])} in cash, and acquired equipment costing {m(p['note'])} by signing a note payable to the seller. All other acquisitions were paid in cash. What amount should {s} report as cash paid to purchase equipment in the investing section of its Year 2 statement of cash flows?""",
        choices, ans,
        f"""Gross equipment: {m(p['gb'])} + acquisitions − {m(p['sc'])} cost of equipment sold = {m(p['ge'])}, so acquisitions were {m(adds)}. Of those, {m(p['note'])} was bought with a note, a noncash investing activity disclosed separately. Cash paid = {m(adds)} − {m(p['note'])} = {m(key_v)}. The accumulated depreciation figures aren't needed for this amount.""",
    )


def ppe_reconciliation(p):
    co, s = p["co"], short(p["co"])
    key_v = p["G"] - p["scr"] - p["maint"]
    S = key_v - p["new"]
    pool = {
        "sub": (m(S), f"Uses the subledger as recorded. It still lacks the {m(p['new'])} machine placed in service on December 28."),
        "maint_only": (m(p["G"] - p["maint"]), f"Removes the maintenance but not the scrapped machine. Retiring a fully depreciated asset removes its {m(p['scr'])} cost from the account."),
        "scrap_only": (m(p["G"] - p["scr"]), f"Removes the scrapped machine but leaves the {m(p['maint'])} of routine maintenance, which is an expense."),
        "maint_twice": (m(S + p["new"] - p["maint"]), f"Also subtracts the maintenance from the subledger balance, which never included it."),
    }
    key = (m(key_v), f"Correct. {m(p['G'])} − {m(p['scr'])} scrapped machine − {m(p['maint'])} maintenance, which equals the subledger {m(S)} + {m(p['new'])}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""At December 31, {co}'s fixed-asset subledger shows total equipment cost of {m(S)}, while the general ledger equipment account shows {m(p['G'])}. The controller's investigation finds: a fully depreciated machine that cost {m(p['scr'])} was scrapped in June and removed from the subledger, but no entry was made in the general ledger; {m(p['maint'])} of routine maintenance was debited to the equipment account in the general ledger; and a machine costing {m(p['new'])}, placed in service on December 28, was recorded in the general ledger but hasn't yet been added to the subledger. What should the corrected equipment cost balance be at December 31?""",
        choices, ans,
        f"""General ledger: {m(p['G'])} − {m(p['scr'])} cost of the scrapped machine (its accumulated depreciation is removed too) − {m(p['maint'])} maintenance, which is expense = {m(key_v)}. Subledger: {m(S)} + {m(p['new'])} new machine = {m(key_v)}. The records now agree.""",
    )


def htm_credit_loss(p):
    co, s = p["co"], short(p["co"])
    i = p["face"] * p["rate"] // 100
    pv = lambda ann, one: rd(i * D(ann) + p["p"] * D(one))
    for ann, one in ((p["ann"], p["one"]), (p["ann2"], p["one2"])):
        assert (i * D(ann) + p["p"] * D(one)) % 1 != D("0.5"), "half-dollar present value: ambiguous rounding"
    key_v = p["face"] - pv(p["ann"], p["one"])
    mkt_v = p["face"] - pv(p["ann2"], p["one2"])
    pool = {
        "undisc": (m(p["face"] - p["p"]), f"Uses the undiscounted {m(p['face'] - p['p'])} principal shortfall. Expected cash flows are discounted."),
        "fv": (m(p["face"] - p["fv"]), f"Writes the bonds down to their {m(p['fv'])} fair value, as for an available-for-sale security. A held-to-maturity security's allowance reflects expected credit losses, not fair value."),
        "mkt": (m(mkt_v), f"Discounts the expected cash flows at the {p['mkt']}% market rate. {s}'s method discounts them at the bonds' {p['rate']}% effective interest rate."),
        "none": ("$0", f"Recognizes no loss because {s} intends to hold the bonds to maturity. Held-to-maturity securities carry an allowance for expected credit losses."),
    }
    key = (m(key_v), f"Correct. {m(p['face'])} amortized cost − {m(pv(p['ann'], p['one']))} present value of expected cash flows at {p['rate']}%.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} bought {m(p['face'])} face amount of bonds at par on January 1, Year 1, and classifies them as held to maturity. The bonds pay {p['rate']}% interest each December 31 and mature on December 31, Year 5. On December 31, Year 3, after receiving that day's interest, {s} learns that the issuer is in financial difficulty. {s} now expects to receive the two remaining interest payments in full but only {m(p['p'])} of the principal at maturity. The bonds' fair value is {m(p['fv'])}, and the market rate for similar bonds is {p['mkt']}%. {s} measures expected credit losses by discounting expected cash flows at the bonds' effective interest rate, and it had recorded no allowance before. Present value factors for two periods are {p['ann']} (ordinary annuity) and {p['one']} (single sum) at {p['rate']}%, and {p['ann2']} and {p['one2']} at {p['mkt']}%. What credit loss expense should {s} recognize for Year 3?""",
        choices, ans,
        f"""Under the current expected credit loss model, a held-to-maturity security carries an allowance equal to its amortized cost minus the present value of the cash flows expected, discounted here at the {p['rate']}% effective rate; fair value doesn't enter. Expected cash flows: interest {m(i)} × {p['ann']} = {m(rd(i * D(p['ann'])))}, plus principal {m(p['p'])} × {p['one']} = {m(rd(p['p'] * D(p['one'])))}, for {m(pv(p['ann'], p['one']))}. The bonds were bought at par, so amortized cost is {m(p['face'])}. Allowance and expense = {m(key_v)}.""",
    )


def covenant_leverage(p):
    co, s = p["co"], short(p["co"])
    ebitda = p["ni"] + p["int"] + p["tax"] + p["da"] - p["gain"]
    debt = p["term"] + p["fl"]
    two = lambda x: ratio(D(x))
    key_v = D(debt) / ebitda
    pool = {
        "op_lease": (two(D(debt + p["ol"]) / ebitda), f"Includes the {m(p['ol'])} of operating lease liabilities, which the agreement excludes from funded debt."),
        "keep_gain": (two(D(debt) / (ebitda + p["gain"])), f"Leaves the {m(p['gain'])} gain on the building sale in EBITDA. The agreement excludes gains on sales of long-lived assets."),
        "no_fin": (two(D(p["term"]) / ebitda), f"Leaves out the {m(p['fl'])} of finance lease liabilities, which the agreement includes in funded debt."),
        "ap": (two(D(debt + p["ap"]) / ebitda), f"Includes the {m(p['ap'])} of accounts payable. Trade payables aren't borrowed money."),
    }
    key = (two(key_v), f"Correct. ({m(p['term'])} + {m(p['fl'])}) ÷ {m(ebitda)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co}'s loan agreement requires its ratio of funded debt to EBITDA to be no more than {p['max']} at each year-end. The agreement defines funded debt as borrowed money plus finance lease liabilities, excluding operating lease liabilities, and defines EBITDA as net income plus interest, income taxes, and depreciation and amortization, excluding gains and losses on sales of long-lived assets. For Year 1, {s} reports net income of {m(p['ni'])}, which includes a {m(p['gain'])} gain on the sale of a building; interest expense of {m(p['int'])}; income tax expense of {m(p['tax'])}; and depreciation and amortization of {m(p['da'])}. At December 31, {s} has a term loan of {m(p['term'])}, finance lease liabilities of {m(p['fl'])}, operating lease liabilities of {m(p['ol'])}, and accounts payable of {m(p['ap'])}. What is {s}'s ratio of funded debt to EBITDA for the covenant test, rounded to two decimal places?""",
        choices, ans,
        f"""EBITDA as defined = {m(p['ni'])} + {m(p['int'])} + {m(p['tax'])} + {m(p['da'])} − {m(p['gain'])} gain on the building = {m(ebitda)}. Funded debt = term loan {m(p['term'])} + finance lease liabilities {m(p['fl'])} = {m(debt)}; operating lease liabilities and accounts payable are excluded. Ratio = {m(debt)} ÷ {m(ebitda)} = {two(key_v)}.""",
    )


# ── Area III ─────────────────────────────────────────────────────────────


def warranty(p):
    co, s = p["co"], short(p["co"])
    y1 = p["units"] * p["p1"] * p["cost"] // 100
    y2 = p["units"] * p["p2"] * p["cost"] // 100
    key_v = y1 + y2 - p["paid"]
    assert key_v > 0 and p["paid"] != y1
    pool = {
        "plus_ext": (m(key_v + p["eu"] * p["ep"]), f"Adds the {m(p['eu'] * p['ep'])} received for extended service plans. Those plans are a separate service, reported as a contract liability (unearned revenue), not as an accrued warranty cost."),
        "y2_only": (m(y2), f"Accrues only the second-year repairs. The first-year repairs ({m(y1)}) are also accrued at the sale, and because units sold during Year 1 are still within their first 12 months, the liability is the total estimate less the {m(p['paid'])} already spent."),
        "gross": (m(y1 + y2), f"Doesn't subtract the {m(p['paid'])} of repairs made in Year 1."),
        "cash": ("$0", "Expenses warranty repairs when paid. The cost of a warranty included in the price is accrued when the product is sold."),
    }
    key = (m(key_v), f"Correct. {p['units']:,} × {p['p1'] + p['p2']}% × {m(p['cost'])} = {m(y1 + y2)}, less {m(p['paid'])} paid.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} began selling a new appliance in Year 1 and sold {p['units']:,} units that year. Each unit comes with a two-year warranty against defects, included in the price. {s} estimates that {p['p1']}% of the units will need repair within 12 months after sale and {p['p2']}% in the second 12 months after sale, at an average cost of {m(p['cost'])} per repair. Warranty repairs made in Year 1 cost {m(p['paid'])}, and {s}'s estimates have not changed. {s} also sold {p['eu']:,} extended service plans for {m(p['ep'])} each, which cover repairs in the third and fourth years after purchase. What estimated liability for warranty costs should {s} report at December 31, Year 1?""",
        choices, ans,
        f"""The two-year warranty is included in the price and covers defects, so its expected cost over both years is accrued when the units are sold: {p['units']:,} × ({p['p1']}% + {p['p2']}%) × {m(p['cost'])} = {m(y1 + y2)}. Repairs of {m(p['paid'])} in Year 1 reduce the liability to {m(key_v)}. The extended service plans are sold separately and give a service beyond the defect warranty, so the {m(p['eu'] * p['ep'])} received is a contract liability recognized as revenue over the coverage period.""",
    )


def tax_provision(p):
    co, s = p["co"], short(p["co"])
    r = D(p["rate"]) / 100
    taxable = p["pretax"] - p["muni"] - p["dep"] + p["warr"]
    cur = rd(taxable * r)
    dtl, dta = rd(p["dep"] * r), rd(p["warr"] * r)
    pay, exp = cur - p["est"], cur + dtl - dta
    pair = lambda a, b: f"{m(a)} payable; {m(b)} expense"
    pool = {
        "pay_gross": (pair(cur, exp), f"Reports the whole {m(cur)} of current tax as payable. The {m(p['est'])} of estimated payments already made is applied against it."),
        "pretax_rate": (pair(rd((taxable + p["muni"]) * r) - p["est"], rd((p["pretax"]) * r)), f"Taxes the {m(p['muni'])} of municipal bond interest. Tax-exempt interest is a permanent difference, excluded from taxable income and from tax expense."),
        "no_deferred": (pair(pay, cur), "Records only current tax expense. The deferred tax liability and asset change deferred tax expense."),
        "no_dta": (pair(pay, cur + dtl), f"Records the {m(dtl)} deferred tax liability but not the {m(dta)} deferred tax asset from the warranty accrual."),
        "dta_added": (pair(pay, cur + dtl + dta), f"Adds the {m(dta)} deferred tax asset to expense. A deferred tax asset reduces deferred tax expense."),
    }
    key = (pair(pay, exp), f"Correct. Current tax {m(cur)} − {m(p['est'])} prepaid = {m(pay)} payable; expense {m(cur)} + {m(dtl)} − {m(dta)} = {m(exp)}.")
    choices, ans = pick(pool, key, p["use"])
    return variant(
        f"""{co} reports pretax financial income of {m(p['pretax'])} for Year 1, its first year of operations, including {m(p['muni'])} of interest on municipal bonds that is exempt from tax. Tax depreciation exceeds book depreciation by {m(p['dep'])}, and warranty expense accrued for books exceeds warranty claims paid by {m(p['warr'])}; warranty costs are deductible when paid. The enacted tax rate is {p['rate']}% for all years, and {s} expects ample future taxable income. During Year 1, {s} paid estimated taxes of {m(p['est'])}, which it recorded as prepaid income taxes. After the estimated payments are applied, what income taxes payable should {s} report on its December 31, Year 1, balance sheet, and what total income tax expense should it report for Year 1?""",
        choices, ans,
        f"""Taxable income = {m(p['pretax'])} − {m(p['muni'])} tax-exempt interest − {m(p['dep'])} excess tax depreciation + {m(p['warr'])} warranty accrual not yet deductible = {m(taxable)}. Current tax = {m(taxable)} × {p['rate']}% = {m(cur)}; after applying the {m(p['est'])} of estimated payments recorded as prepaid income taxes, {m(pay)} remains payable. Deferred tax liability = {m(p['dep'])} × {p['rate']}% = {m(dtl)}; deferred tax asset = {m(p['warr'])} × {p['rate']}% = {m(dta)}. Total expense = {m(cur)} + {m(dtl)} − {m(dta)} = {m(exp)}.""",
    )


# ── Families: parameter set 0 is the item, sets 1-3 its variants ──────────

FAMILIES = [
    ("far-balance-sheet-0005", A1, "Balance sheet", AP,
     ["ASC 210-10-45 (current assets and current liabilities)", "ASC 740-10-45 (deferred taxes classified as noncurrent)"],
     working_capital, [
        dict(co="Hadley Co.", cash=120000, restricted=60000, ar=250000, allow=15000, inv=310000, prepaid=24000, equip=900000, ap=180000, wages=30000, note=400000, cp=100000, div=20000, unearned=40000, dtl=35000, use=["restricted", "dtl", "no_cp"]),
        dict(co="Ingram Co.", cash=85000, restricted=45000, ar=190000, allow=12000, inv=240000, prepaid=18000, equip=650000, ap=150000, wages=22000, note=300000, cp=60000, div=15000, unearned=28000, dtl=26000, use=["no_cp", "restricted", "gross_ar"]),
        dict(co="Jessup Co.", cash=210000, restricted=90000, ar=420000, allow=30000, inv=380000, prepaid=36000, equip=1400000, ap=260000, wages=45000, note=600000, cp=150000, div=40000, unearned=65000, dtl=50000, use=["dtl", "whole_note", "no_cp"]),
        dict(co="Kinsale Co.", cash=64000, restricted=40000, ar=135000, allow=9000, inv=172000, prepaid=12000, equip=480000, ap=98000, wages=16000, note=250000, cp=50000, div=10000, unearned=22000, dtl=19000, use=["gross_ar", "dtl", "restricted"]),
     ]),
    ("far-changes-in-equity-0003", A1, "Statement of changes in equity", AP,
     ["ASC 505-10 (equity)", "ASC 505-20 (stock dividends)", "ASC 505-30 (treasury stock)", "ASC 220-10 (other comprehensive income)"],
     equity_statement, [
        dict(co="Marston Inc.", beg=2400000, ni=350000, decl=90000, paid=60000, sdfv=150000, ts=120000, cost=60000, px=75000, oci=25000, issue=180000, use=["stock_div", "paid_div", "no_oci"]),
        dict(co="Norwell Inc.", beg=1800000, ni=240000, decl=70000, paid=35000, sdfv=110000, ts=90000, cost=50000, px=64000, oci=18000, issue=150000, use=["stock_div", "reissue_cost", "no_oci"]),
        dict(co="Oakridge Inc.", beg=3600000, ni=520000, decl=150000, paid=100000, sdfv=260000, ts=200000, cost=120000, px=138000, oci=40000, issue=300000, use=["paid_div", "reissue_cost", "stock_div"]),
        dict(co="Pembury Inc.", beg=950000, ni=160000, decl=45000, paid=30000, sdfv=80000, ts=60000, cost=30000, px=41000, oci=12000, issue=100000, use=["no_oci", "stock_div", "paid_div"]),
     ]),
    ("far-consolidated-statements-0007", A1, "Consolidated financial statements", AP,
     ["ASC 810-10-45 (elimination of intercompany profit; wholly owned subsidiaries)"],
     consolidated_inventory, [
        dict(parent="Brandt Corp.", sub="Cole Inc.", p_inv=400000, s_inv=250000, down=60000, markup=25, up=50000, margin=30, ic=200000, use=["markup_price", "up_only", "full_price"]),
        dict(parent="Dunmore Corp.", sub="Ellery Inc.", p_inv=520000, s_inv=310000, down=90000, markup=50, up=40000, margin=25, ic=300000, use=["none", "down_only", "up_only"]),
        dict(parent="Farrow Corp.", sub="Gault Inc.", p_inv=280000, s_inv=190000, down=48000, markup=20, up=30000, margin=40, ic=150000, use=["full_price", "none", "markup_price"]),
        dict(parent="Halden Corp.", sub="Ives Inc.", p_inv=640000, s_inv=360000, down=84000, markup=40, up=70000, margin=20, ic=400000, use=["full_price", "up_only", "none"]),
     ]),
    ("far-nfp-financial-position-0003", A1, "Statement of financial position (Not-for-Profit)", AP,
     ["ASC 958-210 (statement of financial position)", "ASC 958-605 (conditional contributions)", "ASC 958-205 (releases from donor restrictions)"],
     nfp_sfp_adjust, [
        dict(org="Maple Grove Clinic", draft=1200000, board=150000, pledge=80000, cond=60000, release=40000, use=["board", "no_release", "cond"]),
        dict(org="Juniper Family Clinic", draft=860000, board=120000, pledge=50000, cond=75000, release=30000, use=["cond", "pledge", "no_release"]),
        dict(org="Kestrel Valley Clinic", draft=2100000, board=300000, pledge=140000, cond=100000, release=65000, use=["board", "pledge", "cond"]),
        dict(org="Linden Street Clinic", draft=640000, board=90000, pledge=45000, cond=35000, release=20000, use=["no_release", "board", "pledge"]),
     ]),
    ("far-nfp-cash-flows-0003", A1, "Statement of cash flows (Not-for-Profit)", AP,
     ["ASC 958-230 (NFP statement of cash flows: restricted contributions as financing)", "ASC 230-10 (indirect method; noncash activities)"],
     nfp_scf_adjust, [
        dict(org="Pine Ridge Shelter", draft=710000, endow=150000, gain=25000, land=100000, unres=180000, use=["no_endow", "gain_once", "unres_fin"]),
        dict(org="Quarry Hill Shelter", draft=540000, endow=120000, gain=15000, land=60000, unres=150000, use=["no_land", "no_endow", "gain_once"]),
        dict(org="Rowan Street Shelter", draft=980000, endow=250000, gain=40000, land=150000, unres=220000, use=["unres_fin", "gain_once", "no_land"]),
        dict(org="Sable Point Shelter", draft=455000, endow=90000, gain=20000, land=75000, unres=130000, use=["no_endow", "no_land", "unres_fin"]),
     ]),
    ("far-nfp-notes-0001", A1, "Notes to financial statements (Not-for-Profit)", AP,
     ["ASC 958-210-50 (liquidity and availability of financial assets)", "ASC 958-205 (board-designated net assets)"],
     nfp_liquidity, [
        dict(org="Sparrow Hill Center", cash=250000, bldg=90000, recv=180000, lt=60000, endow=700000, quasi=200000, other=200000, approp=35000, use=["board", "lt_recv", "no_approp"]),
        dict(org="Thistle Park Center", cash=320000, bldg=150000, recv=140000, lt=45000, endow=900000, quasi=250000, other=160000, approp=40000, use=["no_approp", "bldg", "board"]),
        dict(org="Upland Arts Center", cash=180000, bldg=60000, recv=220000, lt=90000, endow=500000, quasi=120000, other=140000, approp=25000, use=["lt_recv", "bldg", "board"]),
        dict(org="Vesper Hall Center", cash=410000, bldg=200000, recv=160000, lt=70000, endow=1200000, quasi=300000, other=260000, approp=50000, use=["no_approp", "lt_recv", "board"]),
     ]),
    ("far-special-purpose-frameworks-0003", A1, "Special Purpose Frameworks", AP,
     ["AICPA special purpose frameworks (modified cash basis)", "AU-C 800 (financial statements prepared under special purpose frameworks)"],
     modified_cash, [
        dict(co="Dover Surveying", rec=500000, paid=320000, equip=60000, dep=15000, wages=12000, ar=30000, use=["cash_basis", "accrual", "no_dep"]),
        dict(co="Easton Design", rec=380000, paid=250000, equip=45000, dep=9000, wages=14000, ar=22000, use=["wages", "no_dep", "accrual"]),
        dict(co="Fenwick Engineering", rec=720000, paid=470000, equip=90000, dep=18000, wages=20000, ar=35000, use=["cash_basis", "wages", "no_dep"]),
        dict(co="Grafton Appraisals", rec=260000, paid=170000, equip=40000, dep=8000, wages=6000, ar=15000, use=["accrual", "cash_basis", "wages"]),
     ]),
    ("far-ratios-0003", A1, "Financial Statement Ratios and Performance Metrics", AP,
     ["Financial statement analysis: return on common stockholders' equity"],
     roe, [
        dict(co="Ashford Corp.", ni=600000, pref=1000000, rate=6, beg=5000000, end=5400000, use=["no_pref", "total_eq", "ending"]),
        dict(co="Bexley Corp.", ni=450000, pref=500000, rate=8, beg=3200000, end=3600000, use=["ni_total", "total_eq", "no_pref"]),
        dict(co="Cardew Corp.", ni=900000, pref=2000000, rate=5, beg=8000000, end=8600000, use=["ending", "no_pref", "ni_total"]),
        dict(co="Dalby Corp.", ni=280000, pref=400000, rate=7, beg=2100000, end=2300000, use=["total_eq", "ending", "ni_total"]),
     ]),
    ("far-ratios-0004", A1, "Financial Statement Ratios and Performance Metrics", AP,
     ["Financial statement analysis: solvency ratios", "ASC 480-10 (mandatorily redeemable financial instruments)", "ASC 842-20-45 (lease liabilities presented on the balance sheet)"],
     debt_ratio, [
        dict(co="Ferris Corp.", assets=3600000, cl=400000, unearned=50000, ltd=900000, ol=300000, mrp=200000, use=["no_mrp", "no_ol", "neither"]),
        dict(co="Gresham Corp.", assets=5000000, cl=700000, unearned=80000, ltd=1400000, ol=350000, mrp=250000, use=["de", "no_mrp", "no_ol"]),
        dict(co="Hartwell Corp.", assets=2500000, cl=300000, unearned=40000, ltd=500000, ol=240000, mrp=160000, use=["neither", "de", "no_mrp"]),
        dict(co="Inchcape Corp.", assets=8000000, cl=1100000, unearned=120000, ltd=2400000, ol=500000, mrp=400000, use=["no_ol", "neither", "de"]),
     ]),
    ("far-cash-bank-reconciliation-0003", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Proof of cash (four-column bank reconciliation) practice"],
     proof_of_cash, [
        dict(co="Garnet Co.", bank=85000, dit_b=4000, dit_e=6500, note=1200, err=500, use=["no_dit", "dit_reversed", "keep_err"]),
        dict(co="Harlow Co.", bank=126400, dit_b=7200, dit_e=5300, note=2500, err=900, use=["book_only", "keep_err", "no_dit"]),
        dict(co="Iverson Co.", bank=64300, dit_b=3100, dit_e=4800, note=1500, err=650, use=["dit_reversed", "book_only", "keep_err"]),
        dict(co="Jarrow Co.", bank=212000, dit_b=12500, dit_e=9800, note=3000, err=1400, use=["no_dit", "book_only", "dit_reversed"]),
     ]),
    ("far-cash-unreconciled-0001", A2, "Cash and cash equivalents", AN,
     ["ASC 305-10 (cash)", "Bank reconciliation practice (errors by the bank and by the depositor)"],
     unreconciled, [
        dict(co="Wexford Co.", B=48640, true_r=1450, rec_r=1540, dup=1315, true_d=2300, rec_d=2030, use=["whole_diff", "no_transp", "transp_sign"]),
        dict(co="Yarmouth Co.", B=73210, true_r=2680, rec_r=2860, dup=2140, true_d=4150, rec_d=4015, use=["no_transp", "bank_only", "transp_sign"]),
        dict(co="Zeller Co.", B=36480, true_r=960, rec_r=990, dup=845, true_d=1720, rec_d=1270, use=["bank_only", "whole_diff", "no_transp"]),
        dict(co="Abington Co.", B=92750, true_r=3470, rec_r=3740, dup=2960, true_d=5820, rec_d=5370, use=["transp_sign", "whole_diff", "bank_only"]),
     ]),
    ("far-receivables-rollforward-0002", A2, "Trade receivables", AN,
     ["ASC 326-20 (allowance for credit losses; write-offs and recoveries)", "ASC 310-10 (receivables)"],
     allowance_rollforward, [
        dict(co="Linwood Co.", ar_b=400000, sales=2000000, coll=1940000, ar_e=436000, recov=4000, al_b=30000, req=36000, use=["no_reinstate", "no_recov", "ending"]),
        dict(co="Mayfield Co.", ar_b=620000, sales=3400000, coll=3310000, ar_e=662000, recov=7000, al_b=45000, req=60000, use=["direct", "no_recov", "ending"]),
        dict(co="Newbury Co.", ar_b=280000, sales=1500000, coll=1462000, ar_e=295000, recov=3000, al_b=21000, req=26000, use=["no_reinstate", "direct", "no_recov"]),
        dict(co="Orland Co.", ar_b=900000, sales=5200000, coll=5080000, ar_e=968000, recov=12000, al_b=70000, req=84000, use=["ending", "direct", "no_reinstate"]),
     ]),
    ("far-receivables-reconciliation-0002", A2, "Trade receivables", AN,
     ["ASC 310-10-45 (credit balances in receivables reported as liabilities)", "ASC 606-10-55 (consignment arrangements)"],
     ar_reconciliation, [
        dict(co="Arlo Supply", S=598500, cb=3000, memo=4500, true=84600, posted=86400, consign=7200, use=["gl", "net", "sub"]),
        dict(co="Beckett Supply", S=742300, cb=5400, memo=6200, true=51300, posted=53100, consign=9800, use=["no_consign", "net", "gl"]),
        dict(co="Carrow Supply", S=415800, cb=2600, memo=3100, true=62700, posted=67200, consign=5500, use=["sub", "no_consign", "net"]),
        dict(co="Delancey Supply", S=1026400, cb=8200, memo=7400, true=93500, posted=95300, consign=12600, use=["gl", "sub", "no_consign"]),
     ]),
    ("far-inventory-rollforward-0002", A2, "Inventory", AN,
     ["ASC 330-10 (inventory cost; goods in transit and on consignment)"],
     inventory_rollforward, [
        dict(co="Tamsworth Co.", beg=180000, purch=1200000, transit=30000, frt=25000, ret=40000, count=210000, consign=18000, shipped=12000, use=["transit", "consign", "shipped"]),
        dict(co="Upshaw Co.", beg=240000, purch=1650000, transit=42000, frt=33000, ret=55000, count=265000, consign=24000, shipped=15000, use=["freight", "shipped", "transit"]),
        dict(co="Venner Co.", beg=95000, purch=720000, transit=18000, frt=14000, ret=22000, count=110000, consign=9000, shipped=7000, use=["consign", "freight", "shipped"]),
        dict(co="Wardle Co.", beg=410000, purch=2800000, transit=65000, frt=52000, ret=90000, count=455000, consign=38000, shipped=26000, use=["shipped", "freight", "consign"]),
     ]),
    ("far-inventory-reconciliation-0002", A2, "Inventory", AN,
     ["ASC 330-10 (inventory; LIFO reserve)"],
     lifo_reconciliation, [
        dict(co="Kerrigan Co.", sub=840000, receipt=26000, ret=11000, rb=110000, re=135000, use=["fifo", "sub_less", "gl_less"]),
        dict(co="Lomax Co.", sub=1260000, receipt=38000, ret=17000, rb=165000, re=190000, use=["change_only", "gl_less", "sub_less"]),
        dict(co="Merriman Co.", sub=565000, receipt=19000, ret=8000, rb=72000, re=88000, use=["gl_less", "fifo", "change_only"]),
        dict(co="Northam Co.", sub=2140000, receipt=54000, ret=23000, rb=260000, re=305000, use=["sub_less", "change_only", "fifo"]),
     ]),
    ("far-ppe-rollforward-0002", A2, "Property, plant and equipment", AN,
     ["ASC 360-10 (property, plant and equipment)", "ASC 230-10-50 (noncash investing and financing activities)"],
     capex_rollforward, [
        dict(co="Ormond Co.", gb=2000000, ge=2260000, ab=800000, ae=870000, sc=180000, sad=140000, px=55000, note=90000, use=["total", "no_disposal", "nbv"]),
        dict(co="Pelham Co.", gb=3500000, ge=3820000, ab=1400000, ae=1510000, sc=260000, sad=190000, px=85000, note=150000, use=["net_px", "total", "no_disposal"]),
        dict(co="Quenby Co.", gb=1200000, ge=1350000, ab=450000, ae=500000, sc=110000, sad=80000, px=35000, note=60000, use=["nbv", "net_px", "total"]),
        dict(co="Radley Co.", gb=5600000, ge=6100000, ab=2200000, ae=2380000, sc=420000, sad=310000, px=140000, note=240000, use=["no_disposal", "nbv", "net_px"]),
     ]),
    ("far-ppe-reconciliation-0002", A2, "Property, plant and equipment", AN,
     ["ASC 360-10 (property, plant and equipment; retirements; repairs and maintenance)"],
     ppe_reconciliation, [
        dict(co="Pryor Co.", G=3400000, scr=75000, maint=18000, new=45000, use=["sub", "maint_only", "scrap_only"]),
        dict(co="Quillan Co.", G=2150000, scr=52000, maint=14000, new=38000, use=["maint_twice", "scrap_only", "sub"]),
        dict(co="Renshaw Co.", G=5780000, scr=120000, maint=26000, new=64000, use=["maint_only", "maint_twice", "scrap_only"]),
        dict(co="Stanway Co.", G=1640000, scr=41000, maint=9000, new=27000, use=["sub", "maint_twice", "maint_only"]),
     ]),
    ("far-investments-htm-credit-loss-0001", A2, "Investments (Financial assets at amortized cost)", AP,
     ["ASC 326-20 (current expected credit losses on held-to-maturity debt securities; discounted cash flow method)", "ASC 320-10 (held-to-maturity classification)"],
     htm_credit_loss, [
        dict(co="Tanager Co.", face=500000, rate=6, p=400000, fv=381500, mkt=9, ann="1.8334", one="0.8900", ann2="1.7591", one2="0.8417", use=["mkt", "undisc", "fv"]),
        dict(co="Umber Co.", face=800000, rate=5, p=620000, fv=598000, mkt=8, ann="1.8594", one="0.9070", ann2="1.7833", one2="0.8573", use=["mkt", "none", "fv"]),
        dict(co="Vireo Co.", face=320000, rate=7, p=260000, fv=250500, mkt=10, ann="1.8080", one="0.8734", ann2="1.7355", one2="0.8264", use=["mkt", "undisc", "none"]),
        dict(co="Wren Co.", face=1000000, rate=4, p=850000, fv=812000, mkt=7, ann="1.8861", one="0.9246", ann2="1.8080", one2="0.8734", use=["none", "mkt", "fv"]),
     ]),
    ("far-debt-covenant-0002", A2, "Debt (Debt covenant compliance)", AP,
     ["Debt covenant compliance: leverage ratio as defined in the loan agreement"],
     covenant_leverage, [
        dict(co="Kilburn Corp.", max="3.00", ni=1200000, gain=250000, int=400000, tax=300000, da=700000, term=5500000, fl=900000, ol=1200000, ap=800000, use=["op_lease", "keep_gain", "no_fin"]),
        dict(co="Lambeth Corp.", max="2.75", ni=900000, gain=180000, int=300000, tax=240000, da=560000, term=3600000, fl=700000, ol=900000, ap=600000, use=["ap", "no_fin", "keep_gain"]),
        dict(co="Marlow Corp.", max="3.50", ni=2000000, gain=400000, int=650000, tax=520000, da=1100000, term=9000000, fl=1500000, ol=2200000, ap=1300000, use=["keep_gain", "op_lease", "ap"]),
        dict(co="Nuneaton Corp.", max="2.50", ni=650000, gain=120000, int=210000, tax=170000, da=390000, term=2400000, fl=450000, ol=800000, ap=500000, use=["no_fin", "ap", "op_lease"]),
     ]),
    ("far-contingencies-0006", A3, "Contingencies and commitments", AP,
     ["ASC 460-10 (product warranties)", "ASC 606-10-55 (warranties: assurance-type versus service-type)"],
     warranty, [
        dict(co="Corbett Appliances", units=8000, p1=2, p2=4, cost=150, paid=21000, eu=1000, ep=60, use=["y2_only", "gross", "plus_ext"]),
        dict(co="Dalton Appliances", units=12000, p1=3, p2=5, cost=120, paid=40000, eu=1500, ep=45, use=["cash", "gross", "plus_ext"]),
        dict(co="Eaton Appliances", units=5000, p1=4, p2=6, cost=200, paid=37000, eu=800, ep=75, use=["cash", "y2_only", "gross"]),
        dict(co="Fairley Appliances", units=20000, p1=1, p2=3, cost=250, paid=47000, eu=2500, ep=50, use=["cash", "y2_only", "plus_ext"]),
     ]),
    ("far-income-taxes-provision-0001", A3, "Accounting for income taxes", AP,
     ["ASC 740-10 (current and deferred tax expense; temporary and permanent differences)"],
     tax_provision, [
        dict(co="Corliss Corp.", pretax=600000, muni=40000, dep=70000, warr=30000, rate=25, est=100000, use=["no_deferred", "pretax_rate", "pay_gross"]),
        dict(co="Denholm Corp.", pretax=850000, muni=50000, dep=120000, warr=40000, rate=21, est=140000, use=["no_dta", "dta_added", "pay_gross"]),
        dict(co="Elsdon Corp.", pretax=420000, muni=20000, dep=60000, warr=24000, rate=25, est=80000, use=["dta_added", "no_deferred", "pretax_rate"]),
        dict(co="Frimley Corp.", pretax=1200000, muni=100000, dep=160000, warr=80000, rate=21, est=200000, use=["pretax_rate", "no_dta", "no_deferred"]),
     ]),
]

WORD_ITEMS = [
    mcq("far-nfp-financial-position-0002", A1, "Statement of financial position (Not-for-Profit)", RU,
        ["ASC 958-210-05 and 958-210-45 (purpose and presentation of the statement of financial position)"],
        """What is the focus of a nongovernmental not-for-profit entity's statement of financial position?""",
        [("The entity as a whole, including information about its liquidity and financial flexibility", "Correct. The statement reports assets, liabilities and net assets for the entity as a whole and helps users assess liquidity, financial flexibility and the relationship between assets and liabilities."),
         ("Each of the entity's funds, reported side by side in separate columns", "Fund reporting is not required. The statement focuses on the entity as a whole; net assets are shown in two classes by donor restriction."),
         ("Compliance with the entity's budget, comparing actual amounts with budgeted amounts", "Budget-to-actual comparisons belong to state and local government reporting, not to a nongovernmental not-for-profit entity's statement of financial position."),
         ("The cost of each program the entity provides, with expenses reported by function", "Expenses by function are reported in the statement of activities, a statement of functional expenses or the notes, not in the statement of financial position.")],
        "A",
        """ASC 958-210 says the statement of financial position focuses on the not-for-profit entity as a whole and reports total assets, liabilities and net assets, with net assets split between those with and without donor restrictions. With the notes, it provides information about liquidity, financial flexibility and the interrelationship of assets and liabilities. Budget comparisons are a government reporting feature, and functional expenses are reported with the statement of activities."""),
    mcq("far-nfp-cash-flows-0002", A1, "Statement of cash flows (Not-for-Profit)", RU,
        ["ASC 958-230-45 (contributions restricted for long-term purposes are financing activities)"],
        """In a nongovernmental not-for-profit entity's statement of cash flows, how is a cash gift that a donor has restricted to constructing a building reported?""",
        [("As a cash inflow from operating activities", "Unrestricted contributions and gifts restricted to current operations are operating inflows. A gift restricted to acquiring long-lived assets is a financing inflow."),
         ("As a cash inflow from investing activities", "Investing activities include buying and selling the building itself, not receiving a gift restricted to its construction."),
         ("As a cash inflow from financing activities", "Correct. Cash contributions that donors restrict to long-term purposes, such as acquiring or constructing long-lived assets or establishing an endowment, are financing inflows."),
         ("Only in a note, as a noncash activity, until the building is built", "The gift was received in cash, so it is a cash inflow when received. Only noncash gifts, such as donated land, are disclosed as noncash activities.")],
        "C",
        """Under ASC 958-230, receipts of cash contributions that donors restrict to long-term purposes (acquiring, constructing or improving long-lived assets, or establishing or increasing an endowment) are financing activities. The payments to build the building are investing outflows."""),
    mcq("far-governmental-fund-types-0002", A1, "Purpose of funds", AP,
        ["GASB Statement No. 54 (governmental fund type definitions)", "GASB Statement No. 84 (fiduciary activities)"],
        """A county receives a $2,000,000 gift from a resident's estate. The will requires the county to keep the gift intact and to use only the investment earnings to maintain the county's public cemetery. In which fund should the county report the gift?""",
        [("A private-purpose trust fund", "A private-purpose trust fund holds resources whose earnings benefit individuals, private organizations or other governments. The cemetery is the county's own program."),
         ("A special revenue fund", "A special revenue fund reports revenues restricted or committed to a purpose that are spent. Here the principal must be kept intact, so only the earnings can be spent."),
         ("A permanent fund", "Correct. A permanent fund reports resources restricted so that only earnings, not principal, may be used, to support the government's own programs."),
         ("A custodial fund", "A custodial fund holds resources the government collects for other parties, outside a trust. The county controls this gift and uses it for its own program.")],
        "C",
        """Under GASB 54, a permanent fund is a governmental fund for resources that are legally restricted so that only earnings, not principal, may be used for purposes that support the government's own programs, such as a perpetual-care fund for a public cemetery. If the earnings benefited individuals, private organizations or other governments, the gift would be reported in a private-purpose trust fund."""),
    mcq("far-investments-amortized-cost-0001", A2, "Investments (Financial assets at amortized cost)", RU,
        ["ASC 320-10-25 (classification of debt securities)", "ASC 321-10-35 (equity securities without readily determinable fair values)"],
        """Which of the following investments may an entity report at amortized cost?""",
        [("A debt security the entity may sell if interest rates change or it needs cash", "Available-for-sale. A debt security that may be sold before maturity is reported at fair value, with unrealized holding gains and losses in other comprehensive income."),
         ("A debt security bought for a portfolio traded to profit from short-term price changes", "Trading. Trading debt securities are reported at fair value, with changes in net income."),
         ("Common shares of a private company with no readily determinable fair value", "Equity securities are never reported at amortized cost. Without a readily determinable fair value, the entity may use the measurement alternative: cost less impairment, adjusted for observable price changes."),
         ("A debt security the entity has the positive intent and ability to hold until it matures", "Correct. A debt security classified as held to maturity is reported at amortized cost, less an allowance for credit losses.")],
        "D",
        """Only debt securities can be reported at amortized cost, and only when classified as held to maturity: the entity must have the positive intent and ability to hold them to maturity. Debt securities that may be sold are available-for-sale, and those bought for short-term trading are trading securities; both are reported at fair value. Equity securities are reported at fair value, or under the measurement alternative when no readily determinable fair value exists."""),
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
    if failed:
        sys.exit(1)
    warnings = audit(items)
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    write_items(items, CONTENT)


if __name__ == "__main__":
    main()
