# Brief: independent quality review of FAR batch 01

Hand this to a fresh Claude Code session (or your review agent) in a clone of `HaydenHarms/opencpa`, on `main`. The reviewer is independent: it grades the questions, it does not write or fix them.

## Task

Review the 25 FAR multiple-choice items in `content/far/*.yaml` as an experienced CPA-exam item reviewer would. The batch was rewritten to fix problems your earlier review found (too easy, giveaway stems, second defensible answers, obsolete rules, weak distractors). Judge the current files, not the history.

## Ground rules

- Read only `content/far/*.yaml` and `CLAUDE.md` (its "Quality bar" section is the standard being graded against). Do **not** read `docs/reviews/`, `scripts/batches/` or git history first. They contain the author's own claims about the batch, and you should form your own view. You may read them after you have written your findings, to check for anything you disagreed with.
- Do not edit any file. Do not commit. Output the review only.
- Solve every item yourself first, with all arithmetic done in code, before looking at the key and rationales.
- Confirm current rules from public FASB, GASB, AICPA or SEC sources for any item touching a recently changed area (ASU 2015-11, 2016-02, 2016-13, 2016-14, 2017-04, 2018-08, 2018-13, 2020-06, GASB 54, 65). Cite what you checked.

## What to grade, per item

1. **Key correct** under current GAAP or GASB, given only the facts in the stem.
2. **Second defensible answer.** Is any other choice permitted under an election the stem does not fix?
3. **Currency.** Does the stem, key or any distractor rely on a rule that a recent ASU eliminated? (Using the old rule as a labeled distractor is fine.)
4. **Giveaway.** Does the stem name the classification the student must decide?
5. **Missing facts.** Is anything needed to decide absent from the stem?
6. **Distractors.** Does each wrong choice map to a specific, nameable student error, and does each numeric distractor actually result from that error? Which are weak?
7. **Format cues.** Is the correct choice the longest, most qualified, or otherwise different? Are numeric choices ascending?
8. **Difficulty.** Rate Easy, Moderate or Hard against real FAR testlet items, and say how many steps or judgments it takes.
9. **Skill tag.** Is the tagged skill (Remembering and Understanding, Application, Analysis) honest?
10. **Blueprint tag.** Do area and topic match the current AICPA FAR blueprint?
11. **Estimated pass likelihood** for a prepared candidate, as a percentage, and a verdict: exam-ready, minor revision, or major revision.

## Also assess the batch as a whole

- Skill mix against the blueprint (Remembering and Understanding 5–15%, Application 45–55%, Analysis 35–45%).
- Area mix against the blueprint (Area I 30–40%, Area II 30–40%, Area III 25–35%).
- Topic coverage: what is over-represented, what blueprint topics are missing.
- Average estimated pass likelihood, compared with the roughly 67% the first version scored.
- The ten changes that would most improve the batch, ranked.

## Output format

1. A summary table: `id | your answer | agrees with key? | difficulty | skill tag ok? | pass likelihood | verdict`.
2. A findings list per item that is not "exam-ready", with the specific defect and a concrete suggested fix.
3. The batch-level assessment above.
4. A short list of anything the author's quality bar in `CLAUDE.md` should add or change, based on what you found.

Save the report to `review-output.md` in the working directory (not in the repo), so it can be handed back and applied in a follow-up commit.
