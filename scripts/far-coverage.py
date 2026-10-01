"""FAR coverage map: every representative task in the 2026 FAR blueprint, and the MCQs that test it.

Roadmap step 4 ("Finish FAR") is done for MCQs when every task has at least two reviewed items. Each FAR MCQ
is mapped to exactly one task, its main one. Skills follow the blueprint's task verbs, as in the quality bar
in CLAUDE.md (check the PDF's skill column when in doubt).

Run: python3 scripts/far-coverage.py   (prints the gaps; fails if an MCQ is unmapped, mapped twice or missing)
Add each new item's id to its task here in the same commit as the item.
"""
import glob
import os
import sys
from collections import Counter

import yaml

RU, AP, AN = "R&U", "App", "Ana"

# (code, skill, task, [item ids without the "far-" prefix])
TASKS = [
    # ── Area I — Financial Reporting ─────────────────────────────────────
    ("I.A.1a", AP, "Prepare a classified balance sheet", ["balance-sheet-0005", "balance-sheet-0008"]),
    ("I.A.1b", AP, "Adjust the balance sheet to correct identified errors", ["balance-sheet-0006"]),
    ("I.A.1c", AN, "Detect and correct balance sheet discrepancies", ["balance-sheet-0001", "balance-sheet-0002", "balance-sheet-0003", "balance-sheet-0004", "balance-sheet-0007"]),
    ("I.A.2a", AP, "Prepare a single-step or multi-step income statement", ["income-statement-0004", "income-statement-0007"]),
    ("I.A.2b", AP, "Adjust the income statement to correct identified errors", ["income-statement-0005"]),
    ("I.A.2c", AP, "Calculate foreign-currency transaction gains or losses", ["foreign-currency-transactions-0001", "foreign-currency-transactions-0002"]),
    ("I.A.2d", AN, "Detect and correct income statement discrepancies", ["income-statement-0001", "income-statement-0002", "income-statement-0003", "comprehensive-income-0002", "income-statement-0006"]),
    ("I.A.3a", RU, "Recall the purpose, objectives and structure of the statement of comprehensive income", ["comprehensive-income-0004"]),
    ("I.A.3b", RU, "Identify items classified as other comprehensive income", ["comprehensive-income-0003"]),
    ("I.A.4a", AP, "Prepare a statement of changes in equity", ["changes-in-equity-0003"]),
    ("I.A.4b", AP, "Adjust the statement of changes in equity to correct identified errors", ["changes-in-equity-0004"]),
    ("I.A.4c", AN, "Detect and correct statement of changes in equity discrepancies", ["changes-in-equity-0001", "changes-in-equity-0002", "equity-paid-in-capital-0002", "changes-in-equity-0005", "changes-in-equity-0006"]),
    ("I.A.5a", AP, "Prepare a statement of cash flows (indirect method) and required disclosures", ["cash-flows-0008", "cash-flows-0013"]),
    ("I.A.5b", AP, "Adjust a statement of cash flows to correct identified errors", ["cash-flows-0010"]),
    ("I.A.5c", AN, "Detect and correct statement of cash flows discrepancies", ["cash-flows-0003", "cash-flows-0005", "cash-flows-0007", "cash-flows-0011", "cash-flows-0014"]),
    ("I.A.5d", AN, "Derive the impact of transactions on the statement of cash flows", ["cash-flows-0004", "cash-flows-0006", "cash-flows-0009", "cash-flows-0012", "cash-flows-0015"]),
    ("I.A.6a", AP, "Prepare consolidated financial statements (adjustments and eliminations)", ["consolidated-statements-0007", "consolidated-statements-0009"]),
    ("I.A.6b", AP, "Adjust consolidated financial statements to correct identified errors", ["consolidated-statements-0008"]),
    ("I.A.6c", AN, "Detect and correct consolidated financial statement discrepancies", ["consolidated-statements-0001", "consolidated-statements-0002", "consolidated-statements-0003", "consolidated-statements-0004", "consolidated-statements-0006", "consolidated-statements-0010"]),
    ("I.A.7a", AP, "Adjust the notes to correct identified errors and omissions", ["notes-0005"]),
    ("I.A.7b", AN, "Compare the notes with the statements to identify inconsistencies", ["notes-0001", "notes-0002", "notes-0004", "notes-0006", "notes-0007"]),
    ("I.B.1a", RU, "Recall the purpose of the NFP statement of financial position", ["nfp-financial-position-0002"]),
    ("I.B.1b", AP, "Prepare an NFP statement of financial position", ["nfp-financial-position-0001", "nfp-financial-position-0004"]),
    ("I.B.1c", AP, "Adjust an NFP statement of financial position to correct identified errors", ["nfp-financial-position-0003"]),
    ("I.B.2a", RU, "Recall the purpose of the NFP statement of activities", ["nfp-net-assets-0001"]),
    ("I.B.2b", AP, "Prepare an NFP statement of activities", ["nfp-statement-of-activities-0001", "nfp-statement-of-activities-0003"]),
    ("I.B.2c", AP, "Adjust an NFP statement of activities to correct identified errors", ["nfp-statement-of-activities-0002"]),
    ("I.B.2d", AP, "Report NFP expenses by nature and function", ["nfp-functional-expenses-0001", "nfp-functional-expenses-0002"]),
    ("I.B.3a", RU, "Recall the purpose of the NFP statement of cash flows", ["nfp-cash-flows-0002"]),
    ("I.B.3b", AP, "Prepare an NFP statement of cash flows", ["nfp-cash-flows-0001", "nfp-cash-flows-0004"]),
    ("I.B.3c", AP, "Adjust an NFP statement of cash flows to correct identified errors", ["nfp-cash-flows-0003"]),
    ("I.B.4a", AP, "Adjust NFP notes to correct identified errors and omissions", ["nfp-notes-0001"]),
    ("I.C.1a", RU, "Recall government measurement focus and basis of accounting", ["governmental-measurement-focus-0001", "governmental-measurement-focus-0002"]),
    ("I.C.2a", AP, "Determine the appropriate fund(s)", ["governmental-fund-types-0001", "governmental-fund-types-0002"]),
    ("I.D.a", RU, "Recall the purpose of Forms 10-Q, 10-K and 8-K", ["sec-forms-0002"]),
    ("I.D.b", RU, "Identify the items of Form 10-Q and Form 10-K", ["sec-forms-0001"]),
    ("I.D.c", AP, "Calculate basic and diluted EPS", ["eps-basic-0001", "eps-diluted-0001"]),
    ("I.E.a", RU, "Recall special purpose framework statement titles", ["special-purpose-frameworks-0002"]),
    ("I.E.b", AP, "Convert cash or modified cash basis statements to accrual basis", ["special-purpose-frameworks-0001", "special-purpose-frameworks-0005"]),
    ("I.E.c", AP, "Prepare cash basis or modified cash basis statements", ["special-purpose-frameworks-0003"]),
    ("I.E.d", AP, "Prepare income tax basis statements", ["special-purpose-frameworks-0004"]),
    ("I.F.a", RU, "Identify the appropriate ratio or metric for an analysis", ["ratios-0005"]),
    ("I.F.b", AP, "Calculate profitability ratios", ["ratios-0003"]),
    ("I.F.c", AP, "Calculate liquidity ratios", ["ratios-0001", "ratios-0002"]),
    ("I.F.d", AP, "Calculate solvency ratios", ["ratios-0004", "ratios-0006"]),
    ("I.F.e", AP, "Calculate performance metrics", ["performance-metrics-0001", "performance-metrics-0002"]),
    ("I.F.f", AP, "Calculate budget-to-actual variances", ["budget-variance-0001"]),
    # ── Area II — Select Balance Sheet Accounts ──────────────────────────
    ("II.A.a", AP, "Calculate cash and cash equivalents", ["cash-equivalents-0001"]),
    ("II.A.b", AN, "Reconcile the bank balance to the general ledger", ["cash-bank-reconciliation-0001", "cash-bank-reconciliation-0003", "cash-bank-reconciliation-0004", "cash-bank-reconciliation-0005"]),
    ("II.A.c", AN, "Investigate unreconciled cash balances to determine an adjustment", ["cash-bank-reconciliation-0002", "cash-unreconciled-0001", "cash-unreconciled-0002", "cash-unreconciled-0003"]),
    ("II.B.a", AP, "Calculate trade receivables and allowances and prepare journal entries", ["receivables-credit-losses-0002", "receivables-credit-losses-0003"]),
    ("II.B.b", AP, "Record transfers of trade receivables", ["receivables-factoring-0001", "receivables-factoring-0002"]),
    ("II.B.c", AN, "Prepare a rollforward of trade receivables", ["receivables-rollforward-0001", "receivables-rollforward-0002", "receivables-rollforward-0003", "receivables-rollforward-0004"]),
    ("II.B.d", AN, "Reconcile the receivables subledger to the general ledger", ["receivables-reconciliation-0001", "receivables-reconciliation-0002", "receivables-reconciliation-0003", "receivables-reconciliation-0004"]),
    ("II.C.a", AP, "Calculate inventory using various costing methods", ["inventory-dollar-value-lifo-0001", "inventory-gross-profit-method-0001"]),
    ("II.C.b", AP, "Apply lower of cost and NRV or lower of cost or market", ["inventory-lcnrv-0001", "inventory-lcm-0001"]),
    ("II.C.c", AN, "Prepare a rollforward of inventory", ["inventory-rollforward-0001", "inventory-rollforward-0002", "inventory-rollforward-0003", "inventory-rollforward-0004"]),
    ("II.C.d", AN, "Reconcile the inventory subledger to the general ledger", ["inventory-reconciliation-0001", "inventory-reconciliation-0002", "inventory-reconciliation-0003", "inventory-reconciliation-0004"]),
    ("II.D.a", AP, "Calculate gross and net PP&E and prepare journal entries", ["ppe-interest-capitalization-0001", "ppe-lump-sum-0001"]),
    ("II.D.b", AP, "Calculate gains or losses on disposals of long-lived assets", ["ppe-exchange-0001", "ppe-involuntary-conversion-0001"]),
    ("II.D.c", AP, "Calculate impairment losses on long-lived assets", ["ppe-impairment-0002", "ppe-impairment-0003"]),
    ("II.D.d", AP, "Determine whether an asset qualifies as held for sale", ["ppe-held-for-sale-0002"]),
    ("II.D.e", AP, "Adjust the carrying amount of assets held for sale", ["ppe-held-for-sale-0001"]),
    ("II.D.f", AN, "Prepare a rollforward of PP&E", ["ppe-rollforward-0001", "ppe-rollforward-0002", "ppe-rollforward-0003", "ppe-rollforward-0004"]),
    ("II.D.g", AN, "Reconcile the PP&E subledger to the general ledger", ["ppe-reconciliation-0001", "ppe-reconciliation-0002", "ppe-reconciliation-0003", "ppe-reconciliation-0004"]),
    ("II.E.1a", RU, "Identify investments eligible or required to be reported at fair value", ["investments-fair-value-0003"]),
    ("II.E.1b", AP, "Calculate the carrying amount of investments at fair value", ["investments-fair-value-0001"]),
    ("II.E.1c", AP, "Calculate investment income on investments at fair value and prepare journal entries", ["investments-fair-value-0002"]),
    ("II.E.1d", AP, "Calculate impairment losses on investments at fair value", ["investments-afs-credit-loss-0002", "investments-equity-securities-0001"]),
    ("II.E.2a", RU, "Identify investments eligible for amortized cost", ["investments-amortized-cost-0001"]),
    ("II.E.2b", AP, "Calculate the carrying amount of investments at amortized cost", ["investments-htm-0001", "investments-htm-0002"]),
    ("II.E.2c", AP, "Calculate impairment losses on investments at amortized cost", ["investments-htm-credit-loss-0001", "investments-htm-credit-loss-0002"]),
    ("II.E.3a", RU, "Identify when the equity method applies", ["equity-method-0003"]),
    ("II.E.3b", AP, "Calculate the carrying amount of equity method investments", ["equity-method-0001", "equity-method-0002"]),
    ("II.F.a", RU, "Identify recognition criteria and classify intangibles as finite- or indefinite-lived", ["intangibles-classification-0001"]),
    ("II.F.b", AP, "Calculate the carrying amount of finite-lived intangibles", ["intangibles-patent-0001", "intangibles-impairment-0001"]),
    ("II.F.c", AP, "Calculate the carrying amount of purchased software and cloud computing arrangements", ["software-purchased-0001", "intangibles-cloud-computing-0001"]),
    ("II.G.a", RU, "Recall asset retirement obligation recognition and measurement", ["asset-retirement-obligations-0001", "asset-retirement-obligations-0002"]),
    ("II.G.b", AP, "Calculate payables and accrued liabilities", ["accrued-liabilities-0001", "accrued-liabilities-0002"]),
    ("II.G.c", AP, "Calculate exit or disposal liabilities and their timing", ["exit-costs-0001", "exit-costs-0002"]),
    ("II.G.d", AN, "Reconcile the payables subledger to the general ledger", ["payables-cutoff-0001", "payables-reconciliation-0001", "payables-reconciliation-0002", "payables-reconciliation-0003"]),
    ("II.H.1a", RU, "Recall modification versus extinguishment criteria", ["debt-modification-0001"]),
    ("II.H.1b", RU, "Understand when a change in terms is a troubled debt restructuring", ["troubled-debt-restructuring-0001"]),
    ("II.H.1c", AP, "Calculate interest expense on notes and bonds", ["bonds-premium-0001", "debt-noninterest-note-0001"]),
    ("II.H.1d", AP, "Calculate the carrying amount of notes and bonds and prepare journal entries", ["debt-extinguishment-0001", "bonds-between-interest-dates-0001"]),
    ("II.H.2a", AP, "Perform debt covenant calculations", ["debt-covenant-0001", "debt-covenant-0002"]),
    ("II.I.a", AP, "Prepare journal entries for equity transactions", ["equity-retirement-0002", "property-dividend-0001", "stock-dividends-splits-0001", "treasury-stock-0001"]),
    # ── Area III — Select Transactions ───────────────────────────────────
    ("III.A.a", AP, "Calculate adjustments for accounting changes and error corrections", ["change-in-estimate-0001", "change-in-principle-0001"]),
    ("III.A.b", AN, "Derive the impact of an accounting change or error correction", ["accounting-errors-0001", "accounting-errors-0002", "accounting-errors-0003", "accounting-errors-0004", "accounting-errors-0005", "accounting-errors-0006", "accounting-errors-0007"]),
    ("III.B.a", RU, "Recall recognition and disclosure criteria for commitments and contingencies", ["contingencies-0010", "contingencies-0011"]),
    ("III.B.b", AP, "Calculate amounts of contingencies and prepare journal entries", ["contingencies-0006", "contingencies-0007"]),
    ("III.B.c", AN, "Review documentation for recognition versus disclosure", ["contingencies-0002", "contingencies-0003", "contingencies-0004", "contingencies-0005", "contingencies-0008", "contingencies-0009"]),
    ("III.C.a", RU, "Recall five-step model concepts", ["revenue-five-step-0001", "revenue-five-step-0002"]),
    ("III.C.b", RU, "Recall recognition of NFP conditional and unconditional promises to give", ["nfp-promises-to-give-0001", "nfp-promises-to-give-0002"]),
    ("III.C.c", RU, "Identify NFP agent or intermediary transfers that are not contributions", ["nfp-agent-transfers-0001"]),
    ("III.C.d", AP, "Determine revenue under the five-step model", ["revenue-allocation-0003", "revenue-contract-modification-0001", "revenue-licenses-0001", "revenue-material-right-0001", "revenue-over-time-0001", "revenue-principal-agent-0001", "revenue-variable-consideration-0002"]),
    ("III.C.e", AP, "Determine recognition and measurement of contract costs", ["revenue-contract-costs-0001", "revenue-contract-costs-0002"]),
    ("III.C.f", AP, "Determine NFP revenue for contributed services", ["nfp-contributed-services-0001", "nfp-contributed-services-0002"]),
    ("III.C.g", AP, "Calculate NFP contributions of financial and nonfinancial assets", ["nfp-contributions-0001", "nfp-gifts-in-kind-0001"]),
    ("III.D.a", RU, "Recall accounting for uncertain tax positions", ["uncertain-tax-positions-0001", "uncertain-tax-positions-0002"]),
    ("III.D.b", RU, "Recall valuation allowance criteria", ["valuation-allowance-0001", "valuation-allowance-0002"]),
    ("III.D.c", AP, "Calculate income tax expense and current taxes payable", ["income-taxes-deferred-0001", "income-taxes-nol-0001", "income-taxes-provision-0001"]),
    ("III.D.d", AP, "Calculate deferred tax assets and liabilities", ["income-taxes-rate-change-0001", "income-taxes-deferred-0002"]),
    ("III.D.e", AP, "Prepare journal entries to record the tax provision", ["income-taxes-provision-0002", "income-taxes-provision-0003"]),
    ("III.E.a", RU, "Identify valuation techniques used to measure fair value", ["fair-value-hierarchy-0001"]),
    ("III.E.b", AP, "Use assumptions and approaches to measure fair value", ["fair-value-highest-best-use-0001", "fair-value-techniques-0001"]),
    ("III.F.a", RU, "Recall lessee treatment of residual value guarantees, purchase options and variable payments", ["lessee-variable-payments-0001", "lessee-residual-value-0001"]),
    ("III.F.b", RU, "Identify lease classification criteria", ["lessee-classification-0001", "lessee-classification-0002"]),
    ("III.F.c", AP, "Calculate lessee assets and liabilities and prepare journal entries", ["lessee-finance-0002", "lessee-operating-0004"]),
    ("III.F.d", AP, "Calculate lessee lease costs", ["lessee-finance-0001", "lessee-operating-0003"]),
    ("III.G.a", RU, "Identify a subsequent event and recall its treatment", ["subsequent-events-0001", "subsequent-events-0009"]),
    ("III.G.b", AP, "Calculate adjustments for identified subsequent events", ["subsequent-events-0005", "subsequent-events-0006"]),
    ("III.G.c", AN, "Derive the impact of identified subsequent events", ["subsequent-events-0002", "subsequent-events-0003", "subsequent-events-0004", "subsequent-events-0007", "subsequent-events-0008", "subsequent-events-0010"]),
]

CONTENT = os.path.join(os.path.dirname(__file__), "..", "content", "far")


def main():
    mcqs = {}
    for f in glob.glob(os.path.join(CONTENT, "*.yaml")):
        with open(f, encoding="utf-8") as fh:
            d = yaml.safe_load(fh)
        if d["type"] == "mcq":
            mcqs[d["id"].removeprefix("far-")] = d
    mapped = Counter(i for *_, ids in TASKS for i in ids)
    missing = sorted(i for i in mapped if i not in mcqs)
    twice = sorted(i for i, c in mapped.items() if c > 1)
    unmapped = sorted(i for i in mcqs if i not in mapped)
    gaps = [(code, skill, task, len(ids)) for code, skill, task, ids in TASKS if len(ids) < 2]
    print(f"{len(TASKS)} tasks; {len(TASKS) - len(gaps)} with two or more items; {len(mcqs)} FAR MCQs")
    print(f"items still needed for two per task: {sum(2 - c for *_, c in gaps)}")
    for code, skill, task, c in gaps:
        print(f"  {code:8} {skill}  has {c}  {task}")
    for label, ids in (("mapped but not in content (not written yet?)", missing), ("mapped twice", twice),
                       ("unmapped", unmapped)):
        if ids:
            print(f"{label}: {', '.join(ids)}")
    if twice or unmapped:
        sys.exit(1)


if __name__ == "__main__":
    main()
