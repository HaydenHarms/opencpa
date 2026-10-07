# FAR batch 16: review gate, third pass

Fresh review agent following `docs/prompts/review-agent.md`; its returned report, condensed by the orchestrating session (the agent could not write files).

**Result: 80.7% average estimated pass likelihood** (previous 80.3%), **no major items, no wrong keys.** Passes the gate. The previous major (variable-consideration-0003) is now minor. 5 exam-ready, 11 minor.

| id                                  | answers v0–v3 | key agrees | difficulty    | pass likelihood | p-value | verdict    |
| ----------------------------------- | ------------- | ---------- | ------------- | --------------- | ------- | ---------- |
| revenue-variable-consideration-0003 | B/B/B/A       | yes        | Easy          | 80%             | 0.75    | minor      |
| revenue-principal-agent-0002        | C/B/C/C       | yes        | Moderate      | 76%             | 0.55    | minor      |
| revenue-licenses-0002               | B/C/A/D       | yes        | Moderate      | 84%             | 0.60    | exam-ready |
| revenue-contract-costs-0004         | B/C/A/C       | yes        | Moderate      | 82%             | 0.55    | minor      |
| nfp-contributed-services-0003       | B/C/A/C       | yes        | Moderate      | 85%             | 0.60    | exam-ready |
| nfp-contributed-services-0004       | D/C/C/D       | yes        | Moderate–Hard | 86%             | 0.50    | exam-ready |
| nfp-contributions-0003              | C/D/C/D       | yes        | Moderate      | 80%             | 0.60    | minor      |
| fair-value-in-use-0001              | B/B/B/A       | yes        | Easy–Moderate | 78%             | 0.70    | minor      |
| fair-value-liability-0001           | A/B/A/B       | yes        | Moderate      | 78%             | 0.65    | minor      |
| lessee-finance-0004                 | A/A/B/A       | yes        | Moderate      | 82%             | 0.60    | minor      |
| lessee-operating-0006               | C/C/B/C       | yes        | Moderate      | 76%             | 0.65    | minor      |
| lessee-finance-0005                 | C/B/C/B       | yes        | Hard          | 87%             | 0.45    | exam-ready |
| lessee-operating-0007               | B/C/C/A       | yes        | Moderate      | 82%             | 0.60    | minor      |
| income-taxes-provision-0004         | C/D/B/C       | yes        | Moderate      | 85%             | 0.60    | exam-ready |
| income-taxes-deferred-0004          | B/B/C/C       | yes        | Easy          | 70%             | 0.80    | minor      |
| income-taxes-provision-0005         | C/C/C/D       | yes        | Moderate      | 80%             | 0.55    | minor      |

All skill tags are honest (every task here is Application in the blueprint).

## Ranked changes

1. deferred-0004: drop "net of the allowance" from the question (it rules out the no-allowance choice); replace distractor C; make the Year 3/4 split matter or drop it.
2. fair-value-liability-0001: describe the three spreads in parallel, neutral wording; supply the PV factors the stem refers to.
3. lessee-operating-0006: break the key ± deposit pair; change v3's near-identical factors (3.6731 / 3.6730).
4. principal-agent-0002: move off principal-agent-0001's template; driver-share distractor in every version.
5. variable-consideration-0003: replace the $0 and whole-contract distractors; full-bonus lure in every version.
6. provision-0005: third use of the beginning/ending-balance template on III.D.e; change format.
7. nfp-contributions-0003 and lessee-operating-0007: third use of their asks; change them.
8. contract-costs-0004: shorten the amortization policy so it doesn't give the start date.
9. fair-value-in-use-0001: drop the superseded "(in-exchange)" term; add competing valuation evidence.
10. lessee-finance-0004: the commission/legal-fee event echoes lessee-operating-0004; replace v1's two-error distractor.

## Suggested quality-bar additions

Neutral, parallel wording for competing inputs; no distractor pair built as key ± the same amount; the question must not rule out a choice; no superseded terms in rationales; every decoy fact feeds a distractor somewhere; lint the question sentence across items on the same task.
