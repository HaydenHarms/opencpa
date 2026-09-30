"""Deterministic lint for MCQ items: the quality-bar rules that need no judgment.

No model calls. Run it before the blind verifier and the review gate so they only see items that pass:

    python3 scripts/batches/lint.py                 # every item in content/
    python3 scripts/batches/lint.py content/far     # one section
    python3 scripts/batches/lint.py --rules         # list the rules

`audit()` in common.py calls `lint_item` for every item and variant it checks, so a batch script picks these up
without changes. A finding is a warning to fix or consciously accept, not proof of a defect. What it cannot see:
a giveaway in new wording, a missing fact, or two defensible answers. The verifier and the gate still cover those.
"""
import glob
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from common import _amounts, is_numeric  # noqa: E402

SKILL_FULL = {"R&U": "Remembering and Understanding", "App": "Application", "Ana": "Analysis"}

# Labels and conclusions the quality bar (rule 5) and past gate findings named as giveaways when a stem states them.
FORBIDDEN = [
    r"reasonably possible", r"\bremote\b", r"more than remote", r"less than likely",
    r"meets? the criteria", r"commercial substance", r"distinct performance obligations?",
    r"more clearly evident", r"presents? (it )?as a deduction", r"qualitative assessment indicates",
    r"is not in the draft", r"\bdistinct\b(?= (good|service|promise))",
]
FORBIDDEN_RX = re.compile("|".join(FORBIDDEN), re.I)

TAX_LAW = re.compile(
    r"net operating loss|\bNOL\b|enacted (tax )?rate|statutory (tax )?rate|corporate (tax )?rate"
    r"|80% (limit|of (that|the) (year's )?taxable income)", re.I)
NOTE_RULES = {"key_in_stem"}  # too often legitimate to block on; shown as a note, not a warning
NUM = re.compile(r"\$?(\d[\d,]*(?:\.\d+)?)")

RULES = {
    "key_longest": "the correct word choice is at least 2% longer than every distractor",
    "forbidden_label": "the stem uses a label the student is supposed to decide",
    "tag_vs_task": "the skill tag differs from the skill the blueprint marks on the item's mapped task (FAR)",
    "key_in_stem": "(note) a numeric key repeats a dollar amount already given in the stem",
    "near_duplicate": "the stem shares most of its dollar figures, or long phrases, with another item",
    "rounding": "the explanation shows a half-dollar figure that the choices round",
    "missing_asof": "tax-law-dependent item without review.asOf",
}


def _task_skills():
    """item id -> skill the blueprint marks on its task, parsed from scripts/far-coverage.py."""
    src = open(os.path.join(REPO, "scripts", "far-coverage.py"), encoding="utf-8").read()
    body = re.search(r"^TASKS = \[(.*?)^\]", src, re.M | re.S).group(1)
    tasks = eval("[" + body + "]", {"RU": "R&U", "AP": "App", "AN": "Ana"})  # trusted: our own file
    return {"far-" + i: SKILL_FULL[skill] for _, skill, _, ids in tasks for i in ids}


def _numbers(text):
    return {n.replace(",", "") for n in NUM.findall(text) if float(n.replace(",", "") or 0) >= 100}


def _shingles(text, n=14):
    w = re.findall(r"[a-z0-9$%.,']+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(max(len(w) - n + 1, 0))}


def build_context(items):
    """Everything the cross-item rules need: mapped task skills and the other stems' numbers and phrases."""
    return {
        "task_skill": _task_skills(),
        "pool": {it["id"]: (_numbers(it["stem"]), _shingles(it["stem"])) for it in items},
    }


def lint_item(it, ctx=None):
    """Findings for one version of an item as (rule, message). `it` needs stem, choices, answer and, for the
    item-level rules, id, blueprint and review; variants pass just the version fields and skip those rules."""
    out = []
    ch, stem = it["choices"], it["stem"]
    numeric = is_numeric(ch)
    key = next((c for c in ch if c["id"] == it.get("answer")), None)

    if key and not numeric:
        others = [len(c["text"]) for c in ch if c is not key]
        if len(key["text"]) >= max(others) * 1.02:
            out.append(("key_longest", f"key is {len(key['text'])} characters; longest distractor {max(others)}"))

    m = FORBIDDEN_RX.search(stem)
    if m:
        out.append(("forbidden_label", f"stem says \"{m.group(0)}\""))

    if key and numeric:
        given = _numbers(stem)
        hit = [a for a in _amounts(key["text"]) if a >= 1000 and f"{a:.0f}" in given]
        if hit:
            out.append(("key_in_stem", f"key ${hit[0]:,.0f} already appears in the stem"))

    expl = it.get("explanation", "")
    for half in re.findall(r"\$?([\d,]+)\.50\b", expl):
        whole = half.replace(",", "")
        if len(whole) >= 4 and any(whole in c["text"].replace(",", "") for c in ch):  # dollars, not per-share cents
            out.append(("rounding", f"explanation shows ${half}.50 but a choice shows ${half}; state the rounding"))
            break

    bp, rv = it.get("blueprint"), it.get("review") or {}
    if ctx and bp and it.get("id"):
        want = ctx["task_skill"].get(it["id"])
        if want and bp.get("skill") != want:
            out.append(("tag_vs_task", f"tagged {bp.get('skill')}; its task is marked {want}"))
        nums, shingles = ctx["pool"].get(it["id"], (_numbers(stem), _shingles(stem)))
        for oid, (n2, s2) in ctx["pool"].items():
            if oid == it["id"]:
                continue
            both = len(nums & n2)
            # Shared figures mark a reused scenario; a 14-word run marks pasted text. Short phrases are boilerplate.
            if (both >= 4 and both / max(len(nums | n2), 1) >= 0.6) or len(shingles & s2) >= 1:
                out.append(("near_duplicate", f"stem overlaps {oid}"))
                break
    if (TAX_LAW.search(stem) or TAX_LAW.search(expl)) and not rv.get("asOf") and it.get("id"):
        out.append(("missing_asof", "depends on current tax law but has no review.asOf"))
    return out


def lint_items(items, ctx=None):
    """(label, rule, message) for every version of every item."""
    ctx = ctx or build_context(items)
    found = []
    for it in items:
        found += [(it["id"], r, m) for r, m in lint_item(it, ctx)]
        for n, v in enumerate(it.get("variants") or [], 1):
            sub = dict(v, id=None)  # variants: form rules only
            found += [(f"{it['id']} variant {n}", r, m) for r, m in lint_item(sub, None)
                      if r in ("key_longest", "forbidden_label", "key_in_stem", "rounding")]
    return found


def load(paths):
    files = []
    for p in paths:
        files += sorted(glob.glob(os.path.join(p, "*.yaml"))) if os.path.isdir(p) else [p]
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "*", "*.yaml")))
    items = []
    for f in sorted(set(files)):
        d = yaml.safe_load(open(f, encoding="utf-8"))
        if d.get("type") == "mcq":
            items.append(d)
    return items


if __name__ == "__main__":
    if "--rules" in sys.argv:
        for k, v in RULES.items():
            print(f"{k:16} {v}")
        raise SystemExit
    args = [a for a in sys.argv[1:] if not a.startswith("-")] or [os.path.join(REPO, "content")]
    items = load(args)
    found = lint_items(items)
    for label, rule, msg in found:
        print(f"{label}: [{'note' if rule in NOTE_RULES else 'warn'}:{rule}] {msg}")
    warns = [f for f in found if f[1] not in NOTE_RULES]
    flagged = len({l.split(" variant")[0] for l, _, _ in warns})
    print(f"\n{len(warns)} warnings on {flagged} of {len(items)} items; {len(found) - len(warns)} notes", file=sys.stderr)
    raise SystemExit(1 if warns else 0)
