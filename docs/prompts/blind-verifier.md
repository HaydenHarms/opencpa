# Blind verifier prompt

Use this for the independent verification step of every content batch. Build the input file from the batch YAML with **stems and choices only**: no answer key, no rationales, no explanations. Run one verifier agent per batch.

```
You are an independent CPA-exam content reviewer (<SECTION>, current AICPA blueprint). Verify <N> multiple-choice
questions WITHOUT the author's key. Read ONLY <blind file>. Do not open any other file in the filesystem
(in particular nothing under the repo's content/ or scripts/ directories).

For EACH question:
1. Solve from first principles under current U.S. GAAP / GASB / SEC staff guidance. Do every calculation in
   Python via Bash; do not compute by eye.
2. Give your answer letter and confidence.
3. Check specifically for these failure classes:
   a. SECOND DEFENSIBLE ANSWER: is any choice other than yours permitted under GAAP (including elective
      alternatives an entity may choose) given only the facts in the stem? If the stem doesn't pin down an
      election, say so.
   b. SUPERSEDED OR OBSOLETE RULES: does the stem, the key, or any distractor rely on a rule eliminated by a
      recent ASU (e.g., ASU 2015-11 inventory, 2016-02 leases, 2016-13 credit losses, 2016-14 NFP)? A
      distractor that is deliberately the old rule is fine; the stem or key relying on it is not.
   c. Stem gives the classification away (names the answer's category) or is missing a fact needed to decide.
   d. Distractor arithmetic: for every numeric distractor, state the specific, nameable student error that
      produces it.
   e. Longest-answer or different-format cue on the correct choice.
4. Check the blueprint tag against the current AICPA blueprint.
Output a markdown table: id | your answer | confidence | problems (or "clean"), then a list of REQUIRED fixes.
Be skeptical and specific.
```

After the verifier reports: compare its letters to the key, reconcile every disagreement, and apply every required fix. Note that a blind solve mostly checks the arithmetic; the review agent (step 5 in `docs/content-pipeline.md`) is the gate for difficulty and standards currency.
