# Review report: BAR batch 01

**25 items**: the two moved out of FAR batch 01 (`bar-goodwill-impairment-0001`, `bar-nonexchange-revenue-0001`; see `docs/reviews/far-batch-01.md`, Revision 3) plus 23 written from scratch (`scripts/batches/bar-batch-01.py`).

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026. BAR targets: Area I Business Analysis 40–50%, Area II Technical Accounting and Reporting 35–45%, Area III State and Local Governments 10–20%; Remembering and Understanding 10–20%, Application 45–55%, Analysis 30–40%.

## Plan

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `bar-variance-analysis-0001` | I.A.3 Managerial and cost accounting: variance analysis | Application |
| `bar-cvp-what-if-0001` | I.B.1 Prepare and interpret planning techniques (what-if, breakeven) | Analysis |
| `bar-npv-0001` | I.B.3 Calculate net present value | Application |
| `bar-cost-of-capital-0001` | I.B.2 Calculate the cost of capital | Application |
| `bar-variable-absorption-costing-0001` | I.A.3 Use absorption and variable costing | Application |
| `bar-financial-statement-analysis-0001` | I.A.1 Interpret financial statement fluctuations and ratios | Analysis |
| `bar-non-gaap-measures-0001` | I.A.2 Interpret non-GAAP measures (adjusted EBITDA) | Analysis |
| `bar-make-or-buy-0001` | I.B.3 Compare investment alternatives (make or buy) | Analysis |
| `bar-sales-mix-variance-0001` | I.A.3 Interpret sales results by price, volume and mix analysis | Analysis |
| `bar-coso-erm-0001` | I.B.4 Recall the COSO ERM framework | Remembering and Understanding |
| `bar-performance-measures-impact-0001` | I.B.4 Derive the impact of a proposed transaction on key performance measures | Analysis |
| `bar-software-for-sale-0001` | II.B Calculate capitalized software and amortization | Application |
| `bar-stock-compensation-0001` | II.D Equity-classified share-based payment compensation cost | Application |
| `bar-research-development-0001` | II.E Identify research and development costs | Remembering and Understanding |
| `bar-business-combination-0001` | II.F Calculate consideration transferred and goodwill | Application |
| `bar-foreign-currency-translation-0001` | II.G Calculate foreign currency translation adjustments | Application |
| `bar-interest-rate-swap-0001` | II.H Interest rate swap settlements and fair value changes | Application |
| `bar-revenue-contract-analysis-0001` | II.C Interpret agreements to determine revenue | Analysis |
| `bar-lessor-sales-type-0001` | II Leases: lessor accounting | Application |
| `bar-segment-reporting-0001` | II Public company reporting: segment thresholds | Remembering and Understanding |
| `bar-revenue-analytics-discrepancy-0001` | II.C Use data analytics outputs to detect and resolve revenue discrepancies | Analysis |
| `bar-government-wide-reconciliation-0001` | III.B Derive government-wide statements and reconciliations | Analysis |
| `bar-budgetary-accounting-0001` | III Budgetary accounting and encumbrances | Remembering and Understanding |

## Process

Same pipeline as the FAR batches: each item written to one blueprint task; every number and distractor computed in code (a Decimal, round-half-up check script re-verified all 23 after drafting); Analysis items give the facts or draft and let the student find the answer; elections named by method; key positions spread by choosing real errors on both sides of the key.

## Tallies

| Measure | Batch 01 (25) | Blueprint target |
| --- | --- | --- |
| Area I / II / III | 11 / 11 / 3 (44% / 44% / 12%) | 40–50% / 35–45% / 10–20% |
| Remembering and Understanding | 4 (16%) | 10–20% |
| Application | 12 (48%) | 45–55% |
| Analysis | 9 (36%) | 30–40% |
| Key positions | A 6 / B 7 / C 7 / D 5 | — |

## Blind verification

A separate agent solved the 23 new items from the stems and choices only. It **matched the key on 23 of 23** and confirmed every topic is BAR under the 2026 blueprint. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `bar-cost-of-capital-0001` (required) | The 7.6% distractor came from no single error, and the most common error (pretax debt cost) was missing | Replaced with 9.9% (pretax cost of debt) |
| `bar-performance-measures-impact-0001` (required) | The 0.83 quick ratio came from no single error | Replaced with 0.50 (quick assets reduced but not current liabilities) |
| `bar-revenue-contract-analysis-0001` (required) | The stem recited the four bill-and-hold criteria nearly word for word | The stem now gives business facts (built to the customer's specifications, customer's plant not ready, accepted and billed, set aside under its name) and the student concludes control has passed |
| `bar-variance-analysis-0001` | "Price variance on quantity purchased" changed nothing because purchases equal usage | Sentence removed |

The verifier read several items tagged Analysis (CVP what-if, make-or-buy, sales mix, ratio impact, revenue items, the government-wide reconciliation) as Application. The tags stay as written for now; the review gate checks each against the skill marks in the blueprint PDF.
