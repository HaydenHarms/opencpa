# Jev pilot: can a System One screen cut review-agent work?

Question: if Jev screened each drafted item (stem + choices only, blind like the blind verifier), how much of what the
review gate caught would it have caught, and how many clean items could skip the gate?

**Data.** `dataset.jsonl` is built from git history: for each of the eight review-gate fix commits, the item as it
landed ("before", flawed), the item after the fix ("after"), plus 60 current items no gate fix ever touched
("control"). Labels come from the "Review gate" tables in `docs/reviews/*`. Only defects visible from the stem and
choices are scored: giveaway (11 items), form_cue (7), ambiguity (5), skill_tag (7). Distractor quality, duplicates,
rounding, missing `asOf` and key collisions are excluded because they need the key. Samples are small, so read the
confidence intervals, not the point estimates.

**Screens** (`screens.py`): three yes/no checks and a 3-level skill Score in one call per item; a second call maps
FAR items to one of the 113 blueprint tasks from `scripts/far-coverage.py`.

## Run (Windows, from this folder)

The adapter is reused from your Jev Lookalike folder; override with `--agent-dir` or `JEV_AGENT_DIR`.
It needs `typesafe-sdk` and `msgspec` installed and `TYPESAFE_API_KEY` set, as in your earlier runs.

    python run_pilot.py --probe 3          # prints 3 raw answers; check the shapes look right, then continue
    python run_pilot.py                    # ~295 calls, resumable (re-run retries only failed calls)
    python score.py results\typesafe.jsonl

Optional comparator, same screens through Claude (needs `ANTHROPIC_API_KEY` and `system-one-adapter`):

    python run_pilot.py --backend adapter --model claude-haiku-4-5-20251001
    python score.py results\adapter-claude-haiku-4-5-20251001.jsonl

## Reading the report

- **Catch** = share of flawed "before" items a check flags. **False alarm** = share of fixed versions / controls it flags.
  Controls are presumed clean, not proven clean, so control false alarms are an upper bound.
- **Combined screen** is the number that matters: catch vs "controls cleared" is the trade, per confidence threshold.
  Pick the threshold where catch is high and cleared is worth having, then route only flagged items to the review agent.
- **Task mapping** compares against the Claude-made coverage map, which is not ground truth; check the disagreement list.
