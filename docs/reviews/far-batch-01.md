# Review report: FAR batch 01

**25 items** adapted from the legacy `cpa-study.html` bank (345 FAR questions) and re-reviewed against the checklist in CONTRIBUTING.md.

| Blueprint area                                                                          | Items |
| --------------------------------------------------------------------------------------- | ----- |
| Area I: Financial Reporting (cash flows, conceptual framework, NFP, government)         | 7     |
| Area II: Select Balance Sheet Accounts (PP&E, investments, equity)                      | 8     |
| Area III: Select Transactions (revenue, lessee accounting, income taxes, contingencies) | 10    |

Answer positions fall out of the ascending order of numeric choices (see Revision 2).

## Process

1. **Triage.** Candidates were limited to legacy items that already had explanations and fall inside the current FAR blueprint.
2. **Re-solve.** Each item was solved again, and every numeric answer _and every distractor_ was recomputed in code.
3. **Rebuild.** Items were moved to the new schema, with a rationale for every choice, authoritative references and a blueprint tag.
4. **Blind verification.** A separate reviewer agent solved all 25 without seeing the key. It **agreed on 25 of 25** and flagged one stem, which has been fixed.

## Problems found in the legacy source

**Distractors whose stated error doesn't produce the number shown (10, all rebuilt):**

| Legacy item                 | Problem                                                                                              | Fix                                                                               |
| --------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Cash flows (Marlow)         | All three distractors' explanations yield $152k / $185k / $238k, not the $156k / $174k / $192k shown | Distractors replaced with the numbers those errors actually produce               |
| Cash flows (Fenwick)        | $135k / $155k / $195k didn't match their stated errors ($159k / $162k / $213k)                       | Rebuilt; the new $155k distractor catches students who subtract dividends         |
| Revenue allocation (Harmon) | $337,500 "omits one obligation," but omitting support gives $300,000                                 | Replaced with a residual-approach distractor ($250,000)                           |
| Revenue allocation (Delray) | $400,000 "equal weight" actually gives $300,000                                                      | Replaced with a one-year-of-maintenance distractor ($450,000)                     |
| Lessee (Calloway)           | $436,800 "5% rate" actually gives $425,519                                                           | Replaced with an annuity-due distractor ($440,761)                                |
| Lessee (Garland)            | $29,148 had no derivation ("blended approach")                                                       | Replaced with a useful-life amortization distractor ($26,183)                     |
| Impairment (Parkside)       | The $0 distractor's rationale was incoherent                                                         | Rewritten; added a $120,000 distractor (undiscounted cash flows minus fair value) |

**Items excluded from this batch:**

- **Principal vs. agent (Nexus):** two choices were both correct (gross $200,000, and gross $200,000 with $150,000 cost of sales).
- **Goodwill (Prescott):** debt assumed was added to the consideration even though the fair value of net assets already reflects it, so no choice is right.
- **Topics now in BAR:** pensions, business combinations and consolidations, derivatives and hedging, R&D, sale-leaseback, lease modifications. These are held for the BAR section.

**Other corrections:**

- **Conceptual framework:** the stem said an optimistic goodwill impairment projection _reduces_ income; it would raise it. The stem was rewritten using warranty reserve and credit-loss allowance estimates.
- **Finance lease (Reeves):** the $200,000 liability doesn't exactly equal the PV of $50,000 × 5 at 8% ($199,636). The stem now says "(rounded)".
- **Contingency (Bravo):** changed from "40% probability" to "reasonably possible," since ASC 450 doesn't define its thresholds as percentages.
- **NFP (Clearfield):** release timing tied to "placed in service," per the default rule when there's no implied time restriction policy.

## Reproducing

```bash
python3 scripts/batches/far-batch-01.py   # regenerates content/far/*.yaml
pnpm content:validate
```

## Revision 1: independent quality review

A separate review agent (run by Hayden) graded the merged batch. Its findings:

- **Accuracy:** all 25 keys correct under current GAAP/GASB.
- **Exam-readiness:** 8 exam-ready, 15 minor revision, 2 major revision; estimated average pass likelihood about 67%.
- **Main weakness:** too easy. About 10 items are single-step or recall, and several stems name the answer's classification.

**What this revision changes** (merged to `main`):

| Item                          | Problem                                                                                                           | Fix                                                                                                                                          |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `far-nfp-net-assets-0001`     | Relied on the "implied time restriction" policy that ASU 2016-14 eliminated                                       | Stem now spans two years with no policy; the key holds under any permitted release approach. Old rule kept only as a labeled distractor      |
| `far-equity-retirement-0001`  | Second defensible answer: ASC 505-30 also permits charging the whole excess over par to retained earnings         | Stem states Mercer's policy; the $18,000 alternative is now an explicit distractor                                                           |
| `far-revenue-allocation-0001` | Implementation could arguably combine with the license; discount could be allocated to fewer than all obligations | Stem states three distinct obligations and no evidence of a partial allocation                                                               |
| `far-equity-issuance-0001`    | One-step par/APIC split, too easy                                                                                 | Retired. Replaced by `far-equity-paid-in-capital-0001` (allocation, noncash consideration at the more clearly evident value, offering costs) |
| `far-ppe-composite-0001`      | Distractor D used numbers unrelated to the stem; the citation did not apply; marginal blueprint fit               | Retired. Replaced by `far-inventory-lcnrv-0001` (fills the inventory gap; item-by-item lower of cost and NRV under ASU 2015-11)              |
| `far-contingencies-0001`      | Stem named the classification ("reasonably possible")                                                             | Stem now describes the likelihood in words; the student classifies it                                                                        |
| `far-ppe-replacement-0001`    | Stem omitted proceeds and removal costs; distractor D was not a real entry                                        | Stem states the old roof is scrapped at no cost; D is now the old extension-of-life approach                                                 |
| Five word-answer items        | Correct choice was the longest                                                                                    | Choices rewritten to similar length (governmental funds, AFS credit loss, income taxes 0002, PP&E replacement, contingencies)                |
| Numeric items                 | Choices not in ascending order                                                                                    | `finalize()` now sorts numeric choices ascending and rotates the key only across word-answer items                                           |
| Skill tags                    | Four items tagged Analysis that were not                                                                          | Retagged (governmental funds to Remembering and Understanding; AFS credit loss, finance lease, equity retirement to Application)             |

**Verification of the revision:** the 10 revised items were solved blind by a separate agent. It matched the key on 10 of 10 and raised four required fixes, all applied (NFP timing, an unclear distractor explanation, the discount-allocation fact, and the PP&E stem and distractor).

**Blueprint check:** state and local government concepts, NFP, and PP&E are all in the current FAR blueprint (Area I, Area I, Area II). The 2026 blueprint revisions to FAR were minor and moved no topics.

**Still open after this revision:**

- **Too easy.** About 10 single-step or recall items remain (for example, the conceptual framework, joint costs, encumbrances, operating-lease PV, trading securities items). Resolved in Revision 2 below.
- **Skill mix.** The batch is 2 Remembering and Understanding, 23 Application, 0 Analysis. The FAR blueprint targets roughly 5–15% / 45–55% / 35–45%.
- **Area mix.** Area III is still 10 of 25 items (40%) against a 25–35% blueprint weight, and there are no items yet on cash, receivables, intangibles, debt, accounting changes, subsequent events, or fair value.
- **Citations.** Paragraph-level ASC/GASB citations were written from memory and have not been checked against the Codification. Verify them, or cite at the Subtopic level, before relying on them.

## Revision 2: difficulty rewrite (committed straight to `main`)

Hayden asked for the remaining too-easy items to be rewritten. **13 items were retired and 13 new ones written from scratch** (new ids; the old files are deleted and stay in git history).

**Retired:** `far-conceptual-framework-0001`, `far-nfp-joint-costs-0001`, `far-governmental-funds-0001`, `far-governmental-encumbrances-0001`, `far-revenue-variable-consideration-0001`, `far-investments-trading-0001`, `far-lessee-operating-0001`, `far-lessee-operating-0002`, `far-revenue-allocation-0002`, `far-income-taxes-0001`, `far-income-taxes-0002`, `far-income-taxes-0003` (single-step or recall), and `far-ppe-replacement-0001` (US GAAP has no explicit rule for derecognizing a replaced component, so the key depended on practice rather than the Codification).

**Added (13):** property tax revenue under two bases of accounting; NFP contributions (conditional versus unconditional, time and purpose restrictions); diluted EPS with an antidilutive convertible; comprehensive income with a reclassification adjustment; governmental fund purposes; credit-loss allowance with a bankrupt customer evaluated separately; bond extinguishment with issuance costs; goodwill impairment sequencing; equity-method carrying amount with basis differences and downstream profit; prior-period error correction; fair value of land at highest and best use; deferred taxes with permanent differences and a valuation allowance; subsequent events.

**Blind verification of the 13:** solved by a separate agent without the key. It matched the key on 13 of 13. Fixes applied:

| Item | Finding | Fix |
| --- | --- | --- |
| `far-nfp-contributions-0001` | Second defensible answer: ASC 958 lets an entity report a restricted gift met in the same period as without donor restrictions | Stem now states the foundation reports it with donor restrictions |
| `far-comprehensive-income-0001` | Tax-rate wording ambiguous for the reclassified gain | Stem states the rate applies to all AFS gains and losses, not the translation gain |
| `far-governmental-fund-types-0001`, `far-subsequent-events-0001` | Correct choice longest | Choices rebalanced |
| `far-intangibles-goodwill-0001` | Missing status fact | Stem says the entity is a public business entity |
| `far-fair-value-highest-best-use-0001` | Stem restated the highest-and-best-use tests | Reworded to facts only |
| `far-income-taxes-deferred-0001` | Valuation allowance unsupported; stem said a deferred tax asset exists | Stem cites the taxable income forecast; "resulting deferred tax asset" removed |
| Six items | Tagged Analysis but are multi-step computation | Retagged Application (property tax, comprehensive income, equity method, error correction, fair value, deferred taxes) |
| `far-equity-method-0001` | Verifier asked whether downstream profit is eliminated at 100% | Checked: ASC 323-10-35-11 eliminates the investor's ownership share; key stands |

**Other changes in this revision:** topic strings moved to the current FAR blueprint wording; every paragraph-level citation in the batch replaced with a Subtopic-level citation (unverified paragraph cites removed); the generator now deletes retired files.

**Batch 01 tallies (25 items)**

| Measure | Result | Blueprint target |
| --- | --- | --- |
| Area I / II / III | 8 / 10 / 7 (32% / 40% / 28%) | 30–40% / 30–40% / 25–35% |
| Remembering and Understanding | 2 (8%) | 5–15% |
| Application | 19 (76%) | 45–55% |
| Analysis | 4 (16%) | 35–45% |
| Multi-step items | about 22 of 25 | at least half |

Topics covered: cash flows (2), NFP (2), government (2), EPS, comprehensive income, PP&E (2), inventory, equity (2), AFS credit loss, receivables, debt, intangibles, equity method, contingencies, revenue allocation, lessee finance lease, accounting errors, fair value, income taxes, subsequent events.

**Still open**

- **Analysis is short** (16% against 35–45%). Most new items are hard multi-step computations, which the verifier rightly tags Application. Batch 02 should be written around evaluating or comparing alternatives.
- **Gaps:** cash and cash equivalents, payables and accrued liabilities, debt covenants, further revenue topics, lessee operating leases, NFP functional expenses, statement of changes in equity, ratios.
- **Answer positions:** numeric choices are sorted ascending, so the key lands in B for 10 of 25 items. This is the AICPA convention, but watch it as more items are added.
