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

## Revision 1: independent quality review

A separate review agent (run by Hayden) graded the merged batch. Its findings:

- **Accuracy:** all 25 keys correct under current GAAP/GASB.
- **Exam-readiness:** 8 exam-ready, 15 minor revision, 2 major revision; estimated average pass likelihood about 67%.
- **Main weakness:** too easy. About 10 items are single-step or recall, and several stems name the answer's classification.

**What this revision changes** (branch `content/far-batch-01-revisions`):

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

- **Too easy.** About 10 single-step or recall items remain (for example, the conceptual framework, joint costs, encumbrances, operating-lease PV, trading securities items). Decision pending: rewrite them now, or hold the higher bar for later batches.
- **Skill mix.** The batch is 2 Remembering and Understanding, 23 Application, 0 Analysis. The FAR blueprint targets roughly 5–15% / 45–55% / 35–45%.
- **Area mix.** Area III is still 10 of 25 items (40%) against a 25–35% blueprint weight, and there are no items yet on cash, receivables, intangibles, debt, accounting changes, subsequent events, or fair value.
- **Citations.** Paragraph-level ASC/GASB citations were written from memory and have not been checked against the Codification. Verify them, or cite at the Subtopic level, before relying on them.
