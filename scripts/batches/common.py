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


_SIGNED = re.compile(r"\$([\d,]+(?:\.\d+)?)(?:\s+(increase|decrease|gain|loss)\b)?")


def _signs(text):
    """The direction word after each amount: -1 for a decrease or loss, +1 otherwise."""
    return tuple(-1 if w in ("decrease", "loss") else 1 for _, w in _SIGNED.findall(text))


def sort_keys(choices):
    """Ascending sort keys for numeric choices. An amount position whose choices mix directions
    ("$5,000 decrease" beside "$3,000 increase", losses beside gains) sorts by signed value, losses
    first; a position where every choice runs the same way sorts by amount."""
    vals = [_amounts(c["text"]) for c in choices]
    signs = [_signs(c["text"]) for c in choices]
    keys = []
    for v, sg in zip(vals, signs):
        k = []
        for i, a in enumerate(v):
            col = {s[i] for s in signs if i < len(s)}
            k.append(a * sg[i] if len(col) > 1 and i < len(sg) else a)
        keys.append(tuple(k))
    return keys


def sort_numeric(choices):
    """Numeric choices in exam order (see sort_keys)."""
    keys = sort_keys(choices)
    return [c for _, c in sorted(zip(keys, choices), key=lambda kc: kc[0])]


def is_numeric(choices):
    """True when every choice leads with a number or dollar amount, i.e. the item is a 'pick the number' item."""
    return all(_amount(c["text"]) is not None for c in choices)


def finalize(items):
    """Order choices the way the exam does, then report anything that cues the answer.

    - Numeric items: choices sorted ascending (AICPA convention; mixed directions by signed value, see sort_keys).
      The correct answer lands wherever its value falls; do NOT shuffle these.
    - Word items: the correct choice rotates through A-D across word items so the key's
      position carries no signal. The relative order of the other choices is preserved.
    """
    word_n = 0
    for it in items:
        ch = it["choices"]
        right = next(c for c in ch if c["id"] == it["answer"])
        if is_numeric(ch):
            new = sort_numeric(ch)
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


def variant(stem, choices, answer, explanation):
    """One variant of an item: `choices` is a list of (text, rationale); `answer` is a letter into that list."""
    return dict(
        stem=stem.strip(),
        choices=[dict(id=k, text=t, rationale=r) for k, (t, r) in zip("ABCDEF", choices)],
        answer=answer, explanation=explanation.strip(),
    )


_ARTICLE = re.compile(r"\b(a|an) (\$?)(\d[\d,.]*)")


def _spoken_vowel(num):
    """Whether a number is spoken starting with a vowel: 8…, 11 (eleven), 18 (eighteen), 80, 800, 8,000…"""
    lead = num.split(",")[0].split(".")[0]
    return lead.startswith("8") or lead in ("11", "18")


def fix_articles(text):
    """'a $80,000' -> 'an $80,000' and 'an $50,000' -> 'a $50,000', for numbers a template filled in."""
    return _ARTICLE.sub(
        lambda mm: f"{'an' if _spoken_vowel(mm.group(3)) else 'a'} {mm.group(2)}{mm.group(3)}", text)


def attach_variants(item, variants):
    """Order each variant's choices the way finalize() orders the item's, then attach them.

    Numeric variants are sorted ascending. Word variants keep the key in the item's position,
    so the position carries no signal across versions.
    """
    for v in variants:
        v["stem"], v["explanation"] = fix_articles(v["stem"]), fix_articles(v["explanation"])
        for c in v["choices"]:
            c["text"], c["rationale"] = fix_articles(c["text"]), fix_articles(c["rationale"])
        ch = v["choices"]
        right = next(c for c in ch if c["id"] == v["answer"])
        if is_numeric(ch):
            new = sort_numeric(ch)
        else:
            others = [c for c in ch if c is not right]
            pos = "ABCDEF".index(item["answer"])
            new = others[:pos] + [right] + others[pos:]
        for k, c in zip("ABCDEF", new):
            c["id"] = k
        v["choices"] = new
        v["answer"] = next(c["id"] for c in new if c is right)
    item["variants"] = variants
    return item


def _versions(it):
    """The item and each of its variants, labelled for warnings."""
    yield it["id"], it
    for n, v in enumerate(it.get("variants") or [], 1):
        yield f"{it['id']} variant {n}", v


def audit(items):
    """Print warnings for cues a reviewer will flag, in the item and every variant. Returns the count."""
    warnings = []
    for it in items:
        answers = set()
        for label, v in _versions(it):
            warnings += [w.replace(it["id"], label, 1) for w in _audit_one(dict(v, id=it["id"]))]
            key = next(c["text"] for c in v["choices"] if c["id"] == v["answer"])
            if key in answers:
                warnings.append(f"{label}: same correct answer as another version")
            answers.add(key)
    if not os.environ.get("SKIP_LINT"):  # SKIP_LINT=1 when re-running an old batch script on purpose
        import lint  # imported here: lint.py imports this module
        pool = {d["id"]: d for d in lint.load([os.path.join(lint.REPO, "content")])}
        pool.update({it["id"]: it for it in items})
        for label, rule, msg in lint.lint_items(items, lint.build_context(list(pool.values()))):
            if rule in lint.NOTE_RULES:
                print(f"NOTE {label}: [{rule}] {msg}", file=sys.stderr)
            else:
                warnings.append(f"{label}: [{rule}] {msg}")
    for w in warnings:
        print("WARN", w, file=sys.stderr)
    return len(warnings)


def _audit_one(it):
    """Warnings for one version of an item."""
    warnings = []
    ch = it["choices"]
    lens = {c["id"]: len(c["text"]) for c in ch}
    if len(ch) != 4:
        warnings.append(f"{it['id']}: has {len(ch)} choices; FAR/BAR MCQs have exactly four")
    if len({c["text"] for c in ch}) != len(ch):
        warnings.append(f"{it['id']}: duplicate choice text")
    if is_numeric(ch):
        vals = sort_keys(ch)
        if vals != sorted(vals):
            warnings.append(f"{it['id']}: numeric choices not ascending")
    return warnings


def write_items(items, content_dir):
    """Write items to YAML. Variants added later by a variants script are kept as long as the
    item's stem is unchanged; if the stem changed, they are dropped with a warning to re-run it."""
    os.makedirs(content_dir, exist_ok=True)
    for it in items:
        path = os.path.join(content_dir, it["id"] + ".yaml")
        if "variants" not in it and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                old = yaml.safe_load(f)
            if old.get("variants"):
                if old["stem"] == it["stem"]:
                    it["variants"] = old["variants"]
                else:
                    print(f"WARN {it['id']}: stem changed, so its variants were dropped; "
                          "re-run its variants script", file=sys.stderr)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(it, f, sort_keys=False, allow_unicode=True, width=100)
    dist = {}
    for it in items:
        dist[it["answer"]] = dist.get(it["answer"], 0) + 1
    print(f"wrote {len(items)} items; answer positions {dict(sorted(dist.items()))}")
