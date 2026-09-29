"""BAR batch 01 — in progress. Seeded with the two items moved out of FAR batch 01 because the AICPA CPA Exam
Blueprints effective January 2026 place their topics in BAR (see docs/reviews/far-batch-01.md, Revision 3).
New BAR items are added here until the batch reaches ~25.

Run: python3 scripts/batches/bar-batch-01.py  (writes content/bar/*.yaml)
Every numeric answer and distractor below was recomputed in code during review.
"""
import os
import glob
from common import mcq as _mcq, finalize, audit, write_items, RU, AP, AN

A1 = "Area I — Business Analysis"
A2 = "Area II — Technical Accounting and Reporting"
A3 = "Area III — State and Local Governments"
NOTE = ("BAR batch 01. Moved from FAR batch 01 (2026 blueprint scope); "
        "answers re-solved and every number and distractor computed in code.")


def mcq(*a, **k):
    return _mcq(*a, section="BAR", batch=NOTE, **k)


ITEMS = [
# ── Area II ─────────────────────────────────────────────────────────────
mcq("bar-goodwill-impairment-0001", A2, "Indefinite-lived intangible assets, including goodwill", AP,
    ["ASC 350-20 (goodwill)", "ASC 350-30 (indefinite-lived intangible assets)", "ASU 2017-04 (simplifying the test for goodwill impairment)"],
    """Whitfield Corp., a public business entity, tests one reporting unit for impairment at year-end. The unit's carrying amount is $12,000,000, which includes goodwill of $3,000,000 and an indefinite-lived trade name carried at $2,000,000. Whitfield estimates the fair value of the reporting unit at $9,500,000 and the fair value of the trade name at $1,700,000. Ignore income tax effects. What goodwill impairment loss should Whitfield recognize?""",
    [("$0", "Compares the unit's $9,500,000 fair value with its carrying amount excluding goodwill ($9,000,000). The unit's carrying amount includes goodwill."),
     ("$2,200,000", "Correct. The trade name is impaired first by $300,000, leaving a carrying amount of $11,700,000; the goodwill loss is $11,700,000 − $9,500,000."),
     ("$2,500,000", "Measures goodwill against the full $12,000,000 carrying amount without first recognizing the $300,000 trade-name impairment, so that shortfall is counted twice."),
     ("$3,000,000", "Writes off all the goodwill. The loss is the amount by which carrying amount exceeds fair value, limited to the goodwill balance.")],
    "B",
    """When goodwill and other assets of a reporting unit are tested together, the other assets are tested first. The indefinite-lived trade name is impaired by $2,000,000 − $1,700,000 = $300,000, which reduces the reporting unit's carrying amount to $11,700,000. Goodwill impairment is the excess of the unit's carrying amount over its fair value, limited to goodwill: $11,700,000 − $9,500,000 = $2,200,000, which is less than the $3,000,000 of goodwill."""),

# ── Area III ────────────────────────────────────────────────────────────
mcq("bar-nonexchange-revenue-0001", A3, "Nonexchange revenue transactions", AP,
    ["GASB Statement No. 33 (nonexchange transactions)", "GASB Statement No. 34 (government-wide and fund financial statements)", "GASB Statement No. 65 (deferred inflows of resources)"],
    """Lakeview Township's fiscal year is the calendar year. On January 1, Year 5, it levies $4,000,000 of property taxes to finance Year 5 operations. The levy becomes legally enforceable that day, and no taxes were prepaid. The township expects 2% of the levy to prove uncollectible. It collects $3,650,000 through December 31, Year 5, and $150,000 during the first 45 days of Year 6, and it expects to collect the rest of the collectible amount between 90 and 120 days after year-end. In its governmental funds, the township treats property taxes as available if collected within 60 days after year-end. By how much does property tax revenue in the government-wide statement of activities exceed property tax revenue in the general fund's statement of revenues, expenditures, and changes in fund balance?""",
    [("$0", "Applies one basis to both statements. Government-wide statements use full accrual and the funds use modified accrual, so the amounts differ."),
     ("$120,000", "Correct. Government-wide: $4,000,000 less $80,000 expected uncollectible is $3,920,000. General fund: $3,650,000 + $150,000 = $3,800,000. The remaining $120,000 will arrive too late to be available, so the fund reports it as a deferred inflow of resources."),
     ("$200,000", "Leaves the expected uncollectible amount out of the government-wide figure ($4,000,000 − $3,800,000). Government-wide revenue is net of the $80,000 the township expects not to collect."),
     ("$270,000", "Measures fund revenue at cash collected by year-end only ($3,650,000), ignoring the $150,000 collected within the 60-day availability period.")],
    "B",
    """Government-wide statements use the economic resources focus and full accrual. The levy is for Year 5 and enforceable on January 1, so Year 5 revenue is $4,000,000 − $80,000 = $3,920,000. Governmental funds use the current financial resources focus and modified accrual, so revenue is limited to amounts collected by year-end or within the 60-day availability period: $3,650,000 + $150,000 = $3,800,000. The $120,000 of collectible taxes expected later is a deferred inflow of resources in the fund. Difference: $3,920,000 − $3,800,000 = $120,000."""),
]

if __name__ == "__main__":
    finalize(ITEMS)
    warnings = audit(ITEMS)
    out = os.path.join(os.path.dirname(__file__), "..", "..", "content", "bar")
    keep = {it["id"] + ".yaml" for it in ITEMS}
    for f in glob.glob(os.path.join(out, "*.yaml")):
        if os.path.basename(f) not in keep:
            os.remove(f)  # retired item: git history keeps it
            print("retired", os.path.basename(f))
    write_items(ITEMS, out)
    from collections import Counter
    c = lambda k: dict(Counter(k(it) for it in ITEMS))
    print("skills", c(lambda i: i["blueprint"]["skill"]))
    print("areas", c(lambda i: i["blueprint"]["area"]))
    print("warnings", warnings)
