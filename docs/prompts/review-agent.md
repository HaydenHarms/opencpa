# Brief: independent quality review of a content batch

This is the quality gate for every batch (step 5 in `docs/content-pipeline.md`). Hand it to a **fresh** agent each time, one that has not seen the author's reports, with `<SECTION>`, `<BATCH>`, `<FILES>` and `<PREVIOUS SCORE>` filled in. The reviewer is independent: it grades the questions, it does not write or fix them.

## Task

Review the multiple-choice items in `<FILES>` (for example, `content/far/*.yaml`) for `<SECTION>` `<BATCH>` as an experienced CPA-exam item reviewer would. Judge the current files, not the history.

## Ground rules

- Read only `<FILES>` and `docs/content-pipeline.md` (its "Quality bar" section is the standard being graded against). Do **not** read `docs/reviews/`, `scripts/batches/` or git history first. They contain the author's own claims about the batch, and you should form your own view. You may read them after you have written your findings, to check for anything you disagreed with.
- Do not edit any repo file. Do not commit. Output the review only.
- Solve every item yourself first, with all arithmetic done in code, before looking at the key and rationales.
- Check scope and skill levels against the AICPA CPA Exam Blueprints edition named in `docs/content-pipeline.md` (the official PDF), matching each item to a specific representative task.
- Confirm current rules from public FASB, GASB, AICPA or SEC sources for any item touching a recently changed area (the ASUs listed in quality bar item 9, and GASB 33/34/54/65). Cite what you checked.

## What to grade, per item

1. **Key correct** under current GAAP or GASB, given only the facts in the stem.
2. **Second defensible answer.** Is any other choice permitted under an election the stem does not fix?
3. **Currency.** Does the stem, key or any distractor rely on a rule that a recent ASU eliminated? (Using the old rule as a labeled distractor is fine.)
4. **Giveaway.** Does the stem state anything the student must decide: a classification, a conclusion about evidence, a required presentation, or definition wording? Does a stated policy amount to the solution?
5. **Missing facts.** Is anything needed to decide absent from the stem? Is the question itself ambiguous (for example, gross versus net)?
6. **Distractors.** Does each wrong choice map to a specific, nameable student error, and does each numeric distractor actually result from that error? Which are weak?
7. **Format.** Exactly four choices? Is the correct choice the longest, most qualified, or otherwise different? Are numeric choices ascending?
8. **Difficulty.** Rate Easy, Moderate or Hard against real exam testlet items, and say how many steps or judgments it takes.
9. **Skill tag.** Is the tagged skill (Remembering and Understanding, Application, Analysis) honest under the blueprint's task verbs?
10. **Blueprint tag.** Do section, area and topic match a representative task in the current blueprint? Flag anything that belongs in another section.
11. **Pass likelihood and verdict.** Estimate the chance the item would pass AICPA item review as written (the metric earlier reviews used), and separately the p-value (share of prepared candidates answering correctly). Verdict: exam-ready, minor revision, or major revision.

## Also assess the batch as a whole

- Skill mix against the blueprint (FAR: Remembering and Understanding 5–15%, Application 45–55%, Analysis 35–45%).
- Area mix against the blueprint (FAR: Area I 30–40%, Area II 30–40%, Area III 25–35%).
- Topic coverage: what is over-represented, what blueprint topics are missing.
- Average estimated pass likelihood, compared with `<PREVIOUS SCORE>`.
- The ten changes that would most improve the batch, ranked.

## Output format

1. A summary table: `id | your answer | agrees with key? | difficulty | skill tag ok? | pass likelihood | p-value | verdict`.
2. A findings list per item that is not "exam-ready", with the specific defect and a concrete suggested fix.
3. The batch-level assessment above.
4. A short list of anything the quality bar in `docs/content-pipeline.md` should add or change, based on what you found.

Save the report outside the repo (the orchestrating session names the path), so it can be applied in a follow-up commit.
