"""Shared helpers for variants scripts (far-variants-03.py onward; 01 and 02 carry their own copies).

A variants script defines a builder per item and a FAMILIES dict:
    {item_id: (builder, [params_0, params_1, params_2, params_3])}
Parameter set 0 must rebuild the reviewed item word for word; sets 1-3 become its variants. Each params dict
has a `use` list naming the three pool distractors that version shows, so the key's letter can move.
"""
import os
import re
import sys
from decimal import Decimal as D, ROUND_HALF_UP

import yaml

from common import attach_variants, audit

WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
         9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


def rd(x, places="1"):
    """Round half up (to whole dollars by default)."""
    return D(x).quantize(D(places), ROUND_HALF_UP)


def m(x):
    """$1,234 (or $1,234.56 when there are cents)."""
    x = D(x).quantize(D("0.01"), ROUND_HALF_UP)
    return f"${x:,.0f}" if x == x.to_integral() else f"${x:,.2f}"


def n(x):
    """1,234 without a dollar sign."""
    return f"{D(x):,.0f}"


def whole(x):
    x = D(x)
    assert x == x.to_integral(), f"expected a whole amount, got {x}"
    return x


def pct(x, places="0.1"):
    """A fraction as a percent: 30% or 33.3%."""
    x = D(x) * 100
    return f"{x:.0f}%" if x == x.to_integral() else f"{x.quantize(D(places), ROUND_HALF_UP)}%"


def article(word):
    return "an" if word[0].lower() in "aeiou" else "a"


def dollars_in(text):
    """Every dollar amount in a choice, in order."""
    return tuple(float(a.replace(",", "")) for a in re.findall(r"\$([\d,]+(?:\.\d+)?)", text))


def pick(pool, key, use, order=None):
    """The choice list for one version: the pool distractors named in `use`, then the key.

    Returns (choices, answer letter). `order` sorts the list first, for choices finalize() can't fully
    sort itself (ties on the first amount, or choices that don't lead with a $ amount).
    """
    items = [pool[k] for k in use] + [key]
    assert len({t for t, _ in items}) == len(items), f"duplicate choice text: {[t for t, _ in items]}"
    if order:
        items.sort(key=order)
    return items, "ABCDE"[items.index(key)]


def same_as_reviewed(item, v):
    problems = [k for k in ("stem", "explanation") if v[k] != item[k]]
    pairs = lambda x: {(c["text"], c["rationale"]) for c in x["choices"]}
    if pairs(v) != pairs(item):
        problems.append("choices")
    key = lambda x: next(c["text"] for c in x["choices"] if c["id"] == x["answer"])
    if key(v) != key(item):
        problems.append("answer")
    return problems


def run(families, content_dir):
    """Rebuild each reviewed item from parameter set 0, attach variants 1-3, check and write."""
    items, failed = [], False
    for item_id, (build, params) in families.items():
        path = os.path.join(content_dir, item_id + ".yaml")
        with open(path, encoding="utf-8") as f:
            item = yaml.safe_load(f)
        item.pop("variants", None)
        base = build(params[0])
        problems = same_as_reviewed(item, base)
        if problems:
            print(f"FAIL {item_id}: parameter set 0 does not rebuild the reviewed item ({', '.join(problems)})",
                  file=sys.stderr)
            for k in ("stem", "explanation"):
                if k in problems:
                    print(f"  reviewed: {item[k]}\n  rebuilt:  {base[k]}", file=sys.stderr)
            if "choices" in problems:
                want = {(c["text"], c["rationale"]) for c in item["choices"]}
                got = {(c["text"], c["rationale"]) for c in base["choices"]}
                for t in sorted(want - got):
                    print(f"  reviewed choice: {t}", file=sys.stderr)
                for t in sorted(got - want):
                    print(f"  rebuilt choice:  {t}", file=sys.stderr)
            failed = True
            continue
        attach_variants(item, [build(p) for p in params[1:]])
        letters = [item["answer"]] + [v["answer"] for v in item["variants"]]
        print(f"{item_id}: key letters {' '.join(letters)}")
        if len(set(letters)) < 2:
            print(f"FAIL {item_id}: the key has the same letter in every version", file=sys.stderr)
            failed = True
        items.append((path, item))
    if failed:
        sys.exit(1)
    warnings = audit([it for _, it in items])
    if warnings:
        sys.exit(f"{warnings} audit warning(s); nothing written")
    for path, item in items:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            yaml.safe_dump(item, f, sort_keys=False, allow_unicode=True, width=100)
    print(f"added {sum(len(it['variants']) for _, it in items)} variants to {len(items)} items")
