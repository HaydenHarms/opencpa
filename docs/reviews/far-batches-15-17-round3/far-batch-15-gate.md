# FAR batch 15: review gate, third pass

Fresh review agent following `docs/prompts/review-agent.md`. The agent could not write its report file, so this is its returned report, condensed by the orchestrating session. Blueprint task and skill marks come from the `scripts/far-coverage.py` map (the AICPA PDF host was blocked).

**Result: 79.8% average estimated pass likelihood** (previous 78.8%), **no major items, no wrong keys** (all 52 versions solved in code and matched). Just under the ~80% bar.

| id                               | v0 answer          | key agrees | difficulty    | skill ok         | pass likelihood | p-value | verdict                 |
| -------------------------------- | ------------------ | ---------- | ------------- | ---------------- | --------------- | ------- | ----------------------- |
| cash-bank-reconciliation-0006    | $890 increase      | 4/4        | Moderate–Hard | yes (II.A.b AN)  | 84%             | 0.50    | exam-ready              |
| cash-bank-reconciliation-0007    | $3,670 decrease    | 4/4        | Moderate–Hard | yes              | 78%             | 0.50    | minor                   |
| cash-unreconciled-0004           | $1,860             | 4/4        | Hard          | yes (II.A.c AN)  | 80%             | 0.45    | exam-ready (borderline) |
| cash-unreconciled-0005           | $1,250 understated | 4/4        | Hard          | yes              | 82%             | 0.40    | exam-ready              |
| receivables-rollforward-0006     | $516,000           | 4/4        | Hard          | yes (II.B.c AN)  | 76%             | 0.35    | minor                   |
| receivables-rollforward-0007     | $526,000           | 4/4        | Moderate–Hard | yes              | 83%             | 0.45    | exam-ready              |
| inventory-rollforward-0006       | $1,413,000         | 4/4        | Moderate–Hard | yes (II.C.c AN)  | 83%             | 0.50    | exam-ready              |
| inventory-rollforward-0007       | $1,781,000         | 4/4        | Hard          | yes              | 74%             | 0.45    | minor                   |
| ppe-rollforward-0006             | $630,500           | 4/4        | Moderate      | yes (II.D.f AN)  | 82%             | 0.55    | exam-ready              |
| intangibles-cloud-computing-0002 | $288,000           | 4/4        | Hard          | yes (II.F.c AP)  | 84%             | 0.40    | exam-ready              |
| exit-costs-0003                  | $900,000           | 4/4        | Moderate–Hard | yes (II.G.c AP)  | 70%             | 0.45    | minor                   |
| bonds-warrants-0001              | $51,937            | 4/4        | Moderate–Hard | yes (II.H.1c AP) | 82%             | 0.50    | exam-ready              |
| debt-covenant-0003               | $750,000           | 4/4        | Moderate      | yes (II.H.2a AP) | 79%             | 0.60    | minor                   |

## Findings

- **exit-costs-0003 (weakest):** same ask and the same four event families as exit-costs-0002; no "ignore discounting" although severance is paid months later; the stem recites all four ASC 420-10-25-4 criteria. Change the ask, replace event families, add "ignore discounting".
- **inventory-rollforward-0007:** only the rebate is new to II.C.c; the casualty loss repeats rollforward-0003 (including the policy sentence, which also stops it affecting the key) and consignment-out repeats 0002/0004. Variant 2's choice A is weak, and its corrected ending inventory equals beginning inventory.
- **receivables-rollforward-0006:** third "balance before any allowance" ask on II.B.c; the transfer mirrors rollforward-0005; "a restriction Portreath insisted on to protect its customer relationships" cues the benefit condition. Ask for another figure and show the benefit with facts.
- **cash-bank-reconciliation-0007:** the "net adjustment to the general ledger" ask repeats 0006 and 0002; the other-depositor check event repeats 0002; "hasn't recorded the interest or the payment" sorts the facts; v0 lacks the omitted-automatic-payment distractor.
- **debt-covenant-0003:** definition wording and gain-on-sale event copied from debt-covenant-0002; the impairment trap is a misreading, not a judgment. Reword, and add an item to classify.
- Notes: cash-unreconciled-0004 reuses two events (borderline); cloud-computing-0002 should state a fact that clears ASU 2025-06's development-uncertainty test; bonds-warrants-0001 should say the warrants are equity-classified and fix "1 months" in v3.

## Ranked changes

1. exit-costs-0003: new ask, replace shared event families, add "ignore discounting".
2. inventory-rollforward-0007: replace the casualty event with a new one that changes the key; fix variant 2.
3. receivables-rollforward-0006: new ask; facts instead of the stated purpose.
4. cash-bank-reconciliation-0007: new ask; replace the other-depositor event.
5. debt-covenant-0003: reword the definition; add a classification judgment.
   6–10. exit-costs criteria checklist; cloud-0002 ASU 2025-06 fact; bonds equity classification and "1 months"; bank-0007 v0 distractor; cash-unreconciled-0004 event.

## Suggested quality-bar additions

At most two items per task with the same ask; a mirrored event counts as reuse; an event a stated policy neutralizes doesn't count as new; ASC 420 items state discounting; warrant items state the warrants' classification.
