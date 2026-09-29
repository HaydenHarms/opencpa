# Review report: FAR batch 01

**25 items** adapted from the legacy `cpa-study.html` bank (345 FAR questions) and re-reviewed against the checklist in CONTRIBUTING.md.

| Blueprint area                                                                          | Items |
| --------------------------------------------------------------------------------------- | ----- |
| Area I: Financial Reporting (cash flows, conceptual framework, NFP, government)         | 7     |
| Area II: Select Balance Sheet Accounts (PP&E, investments, equity)                      | 8     |
| Area III: Select Transactions (revenue, lessee accounting, income taxes, contingencies) | 10    |

Answer positions are balanced (A 7 · B 6 · C 6 · D 6).

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
