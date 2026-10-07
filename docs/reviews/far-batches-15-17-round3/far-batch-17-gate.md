# FAR batch 17: review gate, third pass

Fresh review agent following `docs/prompts/review-agent.md`; its returned report, condensed by the orchestrating session (the agent could not write files).

**Result: 81.9% average estimated pass likelihood** (previous 78.5%), **no major items, no wrong keys.** Passes the gate. 9 exam-ready, 7 minor. The Area I retag of accounting-errors-0010 to -0012 (I.A.2d, I.A.1c) was judged right.

| id                       | v0 answer          | key agrees | difficulty    | skill ok                    | pass likelihood | verdict                    |
| ------------------------ | ------------------ | ---------- | ------------- | --------------------------- | --------------- | -------------------------- |
| change-in-estimate-0003  | C $351,000         | 4/4        | Moderate      | III.A.a AP                  | 88%             | exam-ready                 |
| change-in-principle-0003 | B $586,250         | 4/4        | Moderate–Hard | III.A.a AP                  | 85%             | exam-ready                 |
| error-correction-0001    | B $37,800 decrease | 4/4        | Moderate      | III.A.a AP                  | 85%             | exam-ready                 |
| accounting-errors-0010   | C $688,800         | 4/4        | Hard          | I.A.2d AN                   | 84%             | exam-ready                 |
| accounting-errors-0011   | C $1,934,000       | 4/4        | Moderate      | I.A.1c AN                   | 82%             | minor                      |
| accounting-errors-0012   | B $2,338,000       | 4/4        | Moderate      | I.A.1c AN                   | 75%             | minor                      |
| contingencies-0015       | B $225,000         | 4/4        | Moderate      | III.B.b AP                  | 84%             | exam-ready                 |
| contingencies-0016       | B $41,400          | 4/4        | Moderate      | III.B.b AP (topic half off) | 80%             | minor                      |
| contingencies-0017       | B $285,104         | 4/4        | Moderate      | III.B.b AP                  | 84%             | exam-ready                 |
| contingencies-0018       | B $133,000         | 4/4        | Moderate      | III.B.c AN                  | 80%             | minor                      |
| contingencies-0019       | B $420,000         | 4/4        | Moderate      | III.B.c AN                  | 76%             | minor                      |
| subsequent-events-0014   | B $272,640         | 4/4        | Moderate      | III.G.b AP                  | 85%             | exam-ready                 |
| subsequent-events-0015   | C $1,889,000       | 4/4        | Moderate      | III.G.b AP                  | 79%             | minor (old major resolved) |
| subsequent-events-0016   | B $1,205,000       | 4/4        | Moderate      | III.G.c AN                  | 80%             | minor                      |
| subsequent-events-0017   | C $8,422,000       | 4/4        | Moderate      | III.G.c AN                  | 83%             | exam-ready                 |
| subsequent-events-0018   | C $1,273,750       | 4/4        | Moderate      | III.G.c AN                  | 80%             | minor                      |

## Ranked changes

1. contingencies-0019 v0 and v2: the cap absorbed the ignore-share, midpoint and top-of-range errors, so they reached the key. Rebuild on the v1/v3 pattern (share × most likely < cap < most likely).
2. accounting-errors-0012: the fair-value and consignment events repeat balance-sheet-0010 and -0007, and the September 1 9% note echoes balance-sheet-0006; replace two events, move the note, replace the two-error choice.
3. subsequent-events-0015: replace the double-count distractors; licensee-decision distractor in every version.
4. contingencies-0016: the mail-in rebate is ASC 606, not a contingency; swap it for a contingency event; drop "every buyer claims".
5. contingencies-0018: the unassessable suit repeats 0008/0009/0013; change the ask; single-error choice C.
6. III.G.c: move at least one of subsequent-events-0016 to -0018 off the "draft figure plus events" format.
7. subsequent-events-0016: cut the facts that label the default; restore v3's write-off distractor.
8. subsequent-events-0018: tie the January penalty to a year-end contract formula.
9. accounting-errors-0011: change the December 18 dividend date; remove the "no entry" cue.
10. contingencies-0019's second matter echoes contingencies-0002/-0004 wording; error-correction-0001 v3 "belong".

## Suggested quality-bar additions

Where a cap, limit or floor applies, compute every plausible error and make sure none collapses onto the key; every version carries the central-twist distractor; count template reuse at the format level; check event reuse against sibling tasks on the same statement; every leg of a multi-event item fits the tagged topic.
