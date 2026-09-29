"""Shared helpers for content batch scripts.

Usage in a batch script (see far-batch-01.py):

    from common import mcq, finalize, write_items, RU, AP, AN
"""
import os
import re
import sys

import yaml

# Skill levels (AICPA blueprint wording)
RU, AP, AN, EV = "Remembering and Understanding", "Application", "Analysis", "Evaluation"

_AMOUNT = re.compile(r"^\$?([\d,]+(?:\.\d+)?)(?![\d-])")


def mcq(id, area, topic, skill, refs, stem, choices, answer, explanation, section="FAR", batch="Batch"):
    """Build one MCQ item. `choices` is a list of (text, rationale); `answer` is a letter into that list."""
    return dict(
        id=id, type="mcq",
        blueprint=dict(section=section, area=area, topic=topic, skill=skill),
        review=dict(status="reviewed", references=refs, notes=batch),
        stem=stem.strip(),
        choices=[dict(id=k, text=t, rationale=r) for k, (t, r) in zip("ABCDEF", choices)],
        answer=answer, explanation=explanation.strip(),
    )


def _amount(text):
    m = _AMOUNT.match(text)
    return float(m.group(1).replace(",", "")) if m else None


def _amounts(text):
    """Every dollar amount in a choice, in order: paired choices ("$30,000 gain; asset $250,000") sort on each."""
    found = re.findall(r"\$([\d,]+(?:\.\d+)?)", text) or [_AMOUNT.match(text).group(1)]
    return tuple(float(a.replace(",", "")) for a in found)


def is_numeric(choices):
    """True when every choice leads with a number or dollar amount, i.e. the item is a 'pick the number' item."""
    return all(_amount(c["text"]) is not None for c in choices)


def finalize(items):
    """Order choices the way the exam does, then report anything that cues the answer.

    - Numeric items: choices sorted ascending by their leading amount (AICPA convention).
      The correct answer lands wherever its value falls; do NOT shuffle these.
    - Word items: the correct choice rotates through A-D across word items so the key's
      position carries no signal. The relative order of the other choices is preserved.
    """
    word_n = 0
    for it in items:
        ch = it["choices"]
        right = next(c for c in ch if c["id"] == it["answer"])
        if is_numeric(ch):
            new = sorted(ch, key=lambda c: _amounts(c["text"]))
        else:
            others = [c for c in ch if c is not right]
            pos = word_n % len(ch)
            word_n += 1
            new = others[:pos] + [right] + others[pos:]
        for k, c in zip("ABCDEF", new):
            c["id"] = k
        it["choices"] = new
        it["answer"] = next(c["id"] for c in new if c is right)
    return items


def audit(items):
    """Print warnings for cues a reviewer will flag. Returns the number of warnings."""
    warnings = []
    for it in items:
        ch = it["choices"]
        lens = {c["id"]: len(c["text"]) for c in ch}
        if not is_numeric(ch):
            right_len = lens[it["answer"]]
            others = [v for k, v in lens.items() if k != it["answer"]]
            if right_len > max(others) * 1.15:
                warnings.append(f"{it['id']}: correct answer is >15% longer than every distractor")
        if len(ch) != 4:
            warnings.append(f"{it['id']}: has {len(ch)} choices; FAR/BAR MCQs have exactly four")
        if len({c["text"] for c in ch}) != len(ch):
            warnings.append(f"{it['id']}: duplicate choice text")
        if is_numeric(ch):
            vals = [_amounts(c["text"]) for c in ch]
            if vals != sorted(vals):
                warnings.append(f"{it['id']}: numeric choices not ascending")
    for w in warnings:
        print("WARN", w, file=sys.stderr)
    return len(warnings)


def write_items(items, content_dir):
    os.makedirs(content_dir, exist_ok=True)
    for it in items:
        with open(os.path.join(content_dir, it["id"] + ".yaml"), "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(it, f, sort_keys=False, allow_unicode=True, width=100)
    dist = {}
    for it in items:
        dist[it["answer"]] = dist.get(it["answer"], 0) + 1
    print(f"wrote {len(items)} items; answer positions {dict(sorted(dist.items()))}")
