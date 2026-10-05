"""Score a run: how well would each Jev screen have caught what the review gate caught?

  python score.py results/typesafe.jsonl [results/adapter-claude-haiku-4-5-20251001.jsonl ...]

Design: a 'before' item is a positive for a check when the gate's finding on it was of that type. Negatives are
(a) the same item's 'after' version (the fix, paired) and (b) 60 controls that no gate fix ever touched.
Controls are 'presumed clean', not proven clean, so control false alarms are an upper bound.
"""
import json, math, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from screens import SKILL_LEVELS, SKILL_SHORT  # noqa: E402

NOUL = ["giveaway", "form_cue", "ambiguity"]
THRESH = [0.3, 0.5, 0.7, 0.9]
data = {r["uid"]: r for r in map(json.loads, open(HERE / "dataset.jsonl"))}


# ---- answer extraction (shapes confirmed by `run_pilot.py --probe`) ----------------------------
def noul_p(a):
    probs = a.get("probabilities")
    if isinstance(probs, dict):
        for k, v in probs.items():
            if str(k).lower() in ("true", "yes"):
                return float(v)
    val = a.get("noul", a.get("value", a.get("answer")))
    # Real Jev shape (confirmed by probe): {"type": "noul", "noul": 0.73} -- the number is P(yes) itself.
    if isinstance(val, (int, float)) and not isinstance(val, bool) and a.get("confidence") is None:
        return float(val)
    if isinstance(val, str):
        val = val.strip().lower() in ("true", "yes")
    conf = a.get("confidence")
    if val is None or conf is None:
        raise ValueError(f"unrecognised noul answer shape: {json.dumps(a)[:200]}")
    return float(conf) if val else 1.0 - float(conf)


def skill_dist(a):
    probs = a.get("probabilities")
    if isinstance(probs, dict):
        out = []
        for lvl, short in zip(SKILL_LEVELS, SKILL_SHORT):
            v = probs.get(lvl)
            if v is None:
                v = next((x for k, x in probs.items() if str(k).startswith(short)), None)
            out.append(v)
        if all(v is not None for v in out):
            return [float(v) for v in out]
        if len(probs) == 3:
            try:
                return [float(probs[k]) for k in sorted(probs, key=lambda x: int(x))]
            except ValueError:
                return [float(v) for v in probs.values()]
    s = a.get("score", a.get("choice"))
    conf = a.get("confidence")
    if s is None or conf is None:
        raise ValueError(f"unrecognised score answer shape: {json.dumps(a)[:200]}")
    idx = int(s) if str(s).lstrip("-").isdigit() else next(i for i, sh in enumerate(SKILL_SHORT) if str(s).startswith(sh))
    rest = (1 - float(conf)) / 2
    return [float(conf) if i == idx else rest for i in range(3)]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 2
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0, c - h), min(1, c + h)


def pct(k, n):
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{100*k/n:.0f}% ({k}/{n}; {100*lo:.0f}-{100*hi:.0f})"


def auc(pos, neg):
    if not pos or not neg:
        return float("nan")
    w = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg)
    return w / (len(pos) * len(neg))


def load(path):
    res = defaultdict(dict)
    errs = 0
    for l in open(path):
        r = json.loads(l)
        if "error" in r:
            errs += 1
            continue
        res[r["uid"]][r["bundle"]] = r
    return res, errs


def report(path):
    res, errs = load(path)
    L = [f"# Jev pilot report: `{Path(path).name}`", ""]
    n_calls = sum(len(v) for v in res.values())
    tin = sum(b["input_tokens"] for v in res.values() for b in v.values())
    tout = sum(b["output_tokens"] for v in res.values() for b in v.values())
    lat = [b["latency"] for v in res.values() for b in v.values()]
    L += [f"{n_calls} successful calls ({errs} error rows skipped); {tin:,} input / {tout:,} output tokens; "
          f"mean latency {sum(lat)/max(len(lat),1):.2f}s.", ""]

    def p(uid, check):
        b = res.get(uid, {}).get("checks")
        return noul_p(b["answers"][check]) if b else None

    labelled_before = [r for r in data.values() if r["version"] == "before" and r["labelled"]]
    controls = [r for r in data.values() if r["version"] == "control"]

    for chk in NOUL:
        pos = [r for r in labelled_before if chk in r["labels"] and p(r["uid"], chk) is not None]
        pairs = [(r, data.get(f"{r['item_id']}|after")) for r in pos]
        pairs = [(a, b) for a, b in pairs if b and p(b["uid"], chk) is not None]
        ctrl = [r for r in controls if p(r["uid"], chk) is not None]
        pp = [p(r["uid"], chk) for r in pos]
        pa = [p(b["uid"], chk) for _, b in pairs]
        pc = [p(r["uid"], chk) for r in ctrl]
        wins = sum(p(a["uid"], chk) > p(b["uid"], chk) for a, b in pairs)
        ties = sum(p(a["uid"], chk) == p(b["uid"], chk) for a, b in pairs)
        L += [f"## Check: {chk}", "",
              f"Positives: {len(pos)} flawed 'before' items. AUC vs fixed versions {auc(pp, pa):.2f}, vs controls {auc(pp, pc):.2f}; "
              f"paired: before scored higher than its own fix in {wins}/{len(pairs)} pairs ({ties} ties).", "",
              "| threshold | catch (95% CI) | false alarm on fixed versions | false alarm on controls |", "|---|---|---|---|"]
        for t in THRESH:
            L.append(f"| p(yes) >= {t} | {pct(sum(x >= t for x in pp), len(pp))} | {pct(sum(x >= t for x in pa), len(pa))} | "
                     f"{pct(sum(x >= t for x in pc), len(pc))} |")
        L.append("")

    # ---- combined pre-gate screen ----
    screenable = [r for r in labelled_before if set(r["labels"]) & set(NOUL)]
    L += ["## Combined screen (any of giveaway / form_cue / ambiguity)", "",
          f"Positives: {len(screenable)} flawed items carrying at least one of those defects. "
          "'Cleared' = no check fired, i.e. the item could skip the review agent.", "",
          "| threshold | catch | controls cleared | fixed versions cleared | unlabelled 'before' items flagged |", "|---|---|---|---|---|"]
    unl = [r for r in data.values() if r["version"] == "before" and not r["labelled"]]
    aft = [data[f"{r['item_id']}|after"] for r in screenable if f"{r['item_id']}|after" in data]

    def anyflag(r, t):
        vals = [p(r["uid"], c) for c in NOUL]
        return None if any(v is None for v in vals) else any(v >= t for v in vals)

    for t in THRESH:
        fl = [anyflag(r, t) for r in screenable]; fl = [x for x in fl if x is not None]
        cc = [anyflag(r, t) for r in controls]; cc = [x for x in cc if x is not None]
        af = [anyflag(r, t) for r in aft]; af = [x for x in af if x is not None]
        uu = [anyflag(r, t) for r in unl]; uu = [x for x in uu if x is not None]
        L.append(f"| {t} | {pct(sum(fl), len(fl))} | {pct(sum(not x for x in cc), len(cc))} | "
                 f"{pct(sum(not x for x in af), len(af))} | {pct(sum(uu), len(uu))} |")
    L.append("")

    # ---- skill level ----
    L += ["## Skill level (Score)", ""]

    def skill(uid):
        b = res.get(uid, {}).get("checks")
        return skill_dist(b["answers"]["skill"]) if b else None

    tagidx = {s: i for i, s in enumerate(SKILL_SHORT)}
    clean = [r for r in list(data.values()) if r["version"] in ("after", "control") and skill(r["uid"]) and r["skill_tag"] in tagidx]
    agree = sum(max(range(3), key=lambda i: skill(r["uid"])[i]) == tagidx[r["skill_tag"]] for r in clean)
    sp = [r for r in labelled_before if "skill_tag" in r["labels"] and skill(r["uid"]) and r["skill_tag"] in tagidx]
    mis = sum(max(range(3), key=lambda i: skill(r["uid"])[i]) != tagidx[r["skill_tag"]] for r in sp)
    L += [f"Agreement with the assigned tag on fixed versions and controls: {pct(agree, len(clean))}.",
          f"Disagreement with the wrong tag on flawed 'before' items (what the gate retagged): {pct(mis, len(sp))}.", ""]
    by = defaultdict(lambda: [0, 0])
    for r in clean:
        by[r["skill_tag"]][1] += 1
        by[r["skill_tag"]][0] += max(range(3), key=lambda i: skill(r["uid"])[i]) == tagidx[r["skill_tag"]]
    L += ["| tag | agreement |", "|---|---|"] + [f"| {k} | {pct(*v)} |" for k, v in sorted(by.items())] + [""]

    # ---- blueprint task mapping ----
    L += ["## Blueprint task mapping (FAR, 113 options)", ""]
    tk = [(r, res[r["uid"]]["task"]["answers"]["task"]) for r in data.values()
          if r["uid"] in res and "task" in res[r["uid"]] and r.get("task")]
    if tk:
        def top(a):
            return a["choice"].split(" ", 1)[0], float(a["confidence"])
        ok = sum(top(a)[0] == r["task"][0] for r, a in tk)
        area = sum(top(a)[0].split(".")[0] == r["task"][0].split(".")[0] for r, a in tk)
        L += [f"Top-1 agreement with the coverage map: {pct(ok, len(tk))}; same blueprint area: {pct(area, len(tk))}.",
              "The map is Claude-made, not ground truth, so a disagreement can be Jev being right; see the list below.", "",
              "| confidence >= | items covered | agreement among covered |", "|---|---|---|"]
        for t in (0.5, 0.7, 0.9):
            cov = [(r, a) for r, a in tk if top(a)[1] >= t]
            L.append(f"| {t} | {pct(len(cov), len(tk))} | {pct(sum(top(a)[0] == r['task'][0] for r, a in cov), len(cov))} |")
        L += ["", "Disagreements at confidence >= 0.7 (check by hand):", ""]
        for r, a in tk:
            c, conf = top(a)
            if conf >= 0.7 and c != r["task"][0]:
                L.append(f"- `{r['item_id']}` ({r['version']}): map says {r['task'][0]}, Jev says {c} ({conf:.2f})")
    else:
        L.append("No task-mapping results in this run.")
    return "\n".join(L)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        text = report(path)
        outp = HERE / "results" / (Path(path).stem + "_report.md")
        outp.write_text(text, encoding="utf-8")
        print(text)
        print(f"\n[written to {outp}]")
