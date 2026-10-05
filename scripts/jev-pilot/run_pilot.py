"""Run the Jev screens over dataset.jsonl. Resumable: re-running skips what is already in the output file.

  python run_pilot.py --probe 3            # print 3 raw answers to confirm the answer shapes, then stop
  python run_pilot.py                      # full run with Jev (needs TYPESAFE_API_KEY)
  python run_pilot.py --backend adapter --model claude-haiku-4-5-20251001    # same screens through Claude

The agent folder is where system_one_agent.py lives (default: JEV_AGENT_DIR or the Jev Lookalike folder).
"""
import argparse, asyncio, json, os, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_AGENT_DIR = os.environ.get("JEV_AGENT_DIR", r"C:\Users\harms\OneDrive\Documents\Desktop Archive\Jev Lookalike")

ap = argparse.ArgumentParser()
ap.add_argument("--agent-dir", default=DEFAULT_AGENT_DIR)
ap.add_argument("--backend", default="typesafe", choices=["typesafe", "adapter"])
ap.add_argument("--model", default=None)
ap.add_argument("--provider", default="anthropic")
ap.add_argument("--concurrency", type=int, default=8)
ap.add_argument("--limit", type=int, default=0, help="only the first N records (smoke test)")
ap.add_argument("--probe", type=int, default=0, help="print raw answers for N records and exit")
ap.add_argument("--out", default=None)
args = ap.parse_args()

sys.path.insert(0, args.agent_dir)
sys.path.insert(0, str(HERE))
from system_one_agent import AsyncEngine, answer_to_jsonable  # noqa: E402
from screens import CHECKS, item_state, task_question  # noqa: E402

records = [json.loads(l) for l in open(HERE / "dataset.jsonl")]
if args.limit:
    records = records[: args.limit]
task_q, _ = task_question()

tag = args.backend if not args.model else f"{args.backend}-{args.model}".replace("/", "_")
out_path = Path(args.out) if args.out else HERE / "results" / f"{tag}.jsonl"
out_path.parent.mkdir(exist_ok=True)

done = set()
if out_path.exists():
    for l in open(out_path):
        try:
            r = json.loads(l)
            if "error" not in r:
                done.add((r["uid"], r["bundle"]))
        except Exception:
            pass

jobs = []
for rec in records:
    jobs.append((rec, "checks", CHECKS))
    if rec["section"] == "FAR" and rec["version"] != "before" and rec.get("task"):
        jobs.append((rec, "task", task_q))
jobs = [j for j in jobs if (j[0]["uid"], j[1]) not in done]


async def main():
    lock = asyncio.Lock()
    sem = asyncio.Semaphore(args.concurrency)
    stats = {"ok": 0, "err": 0, "in": 0, "out": 0, "lat": 0.0}
    t0 = time.time()
    async with AsyncEngine(args.backend, args.model, args.provider) as eng:
        async def one(rec, bundle, questions):
            async with sem:
                for attempt in range(3):
                    try:
                        d = await eng.decide(item_state(rec), questions)
                        row = {"uid": rec["uid"], "bundle": bundle, "model": d.model,
                               "answers": {k: answer_to_jsonable(v) for k, v in d.answers.items()},
                               "input_tokens": d.input_tokens, "output_tokens": d.output_tokens, "latency": d.latency}
                        stats["ok"] += 1; stats["in"] += d.input_tokens; stats["out"] += d.output_tokens; stats["lat"] += d.latency
                        break
                    except Exception as exc:  # noqa: BLE001
                        row = {"uid": rec["uid"], "bundle": bundle, "error": f"{type(exc).__name__}: {exc}"[:300]}
                        await asyncio.sleep(1.5 * (attempt + 1))
                if "error" in row:
                    stats["err"] += 1
                async with lock:
                    with open(out_path, "a") as f:
                        f.write(json.dumps(row) + "\n")
                return row

        if args.probe:
            for rec, bundle, q in jobs[: args.probe]:
                row = await one(rec, bundle, q)
                print(json.dumps(row, indent=1)[:2500])
            return
        print(f"{len(jobs)} calls to run ({len(done)} already done) -> {out_path}")
        await asyncio.gather(*(one(*j) for j in jobs))
    n = max(stats["ok"], 1)
    print(f"done in {time.time()-t0:.0f}s: {stats['ok']} ok, {stats['err']} errors; "
          f"avg latency {stats['lat']/n:.2f}s; tokens in {stats['in']} out {stats['out']}")
    if stats["err"]:
        print("Errors were written with an 'error' field; re-run to retry only those.")

asyncio.run(main())
