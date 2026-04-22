"""Run the Claude Agent SDK across every (dataset, query) pair — 1 run each.

Writes:
  sdk_runner/results/results.jsonl      (one line per query, appended)
  sdk_runner/results/submission.json    (final aggregated submission)
"""
from __future__ import annotations
import argparse
import asyncio
import json
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_sdk_agent import run_one  # type: ignore

REPO = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO / "sdk_runner" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
JSONL_PATH = RESULTS_DIR / "results.jsonl"
SUB_PATH = RESULTS_DIR / "submission.json"


def enumerate_tasks() -> list[tuple[str, int]]:
    tasks: list[tuple[str, int]] = []
    for ds_dir in sorted(REPO.glob("query_*")):
        if not ds_dir.is_dir():
            continue
        dataset = ds_dir.name.removeprefix("query_")
        for q_dir in sorted(ds_dir.glob("query*")):
            if not q_dir.is_dir():
                continue
            qid = q_dir.name.removeprefix("query")
            if not qid.isdigit():
                continue
            tasks.append((dataset, int(qid)))
    return tasks


def already_done(dataset: str, qid: int) -> bool:
    if not JSONL_PATH.exists():
        return False
    for line in JSONL_PATH.read_text().splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("dataset") == dataset and str(rec.get("query")) == str(qid):
            return True
    return False


async def worker(name: str, dataset: str, qid: int, model: str, max_turns: int,
                 lock: asyncio.Lock) -> dict | None:
    t0 = time.time()
    print(f"[{name}] start {dataset}/query{qid}")
    try:
        rec = await run_one(dataset, qid, model, max_turns)
    except Exception as e:
        traceback.print_exc()
        rec = {
            "dataset": dataset,
            "query": str(qid),
            "run": "0",
            "answer": "",
            "meta": {"error": f"{type(e).__name__}: {e}"},
        }
    dt = time.time() - t0
    print(f"[{name}] done  {dataset}/query{qid} in {dt:.1f}s")
    async with lock:
        with JSONL_PATH.open("a") as f:
            f.write(json.dumps(rec) + "\n")
    return rec


async def main_async(concurrency: int, model: str, max_turns: int, only: str | None) -> None:
    tasks_all = enumerate_tasks()
    if only:
        tasks_all = [t for t in tasks_all if t[0] == only]
    tasks = [t for t in tasks_all if not already_done(*t)]
    print(f"Total tasks: {len(tasks_all)} | to run: {len(tasks)} | concurrency: {concurrency}")

    sem = asyncio.Semaphore(concurrency)
    lock = asyncio.Lock()

    async def bound(i: int, ds: str, qid: int):
        async with sem:
            return await worker(f"w{i % concurrency}", ds, qid, model, max_turns, lock)

    await asyncio.gather(*(bound(i, ds, qid) for i, (ds, qid) in enumerate(tasks)))

    # Aggregate into submission.json
    records = []
    if JSONL_PATH.exists():
        for line in JSONL_PATH.read_text().splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            records.append(
                {k: rec[k] for k in ("dataset", "query", "run", "answer") if k in rec}
            )
    SUB_PATH.write_text(json.dumps(records, indent=2))
    print(f"Wrote {SUB_PATH} with {len(records)} records")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--model", default="claude-opus-4-7")
    ap.add_argument("--max_turns", type=int, default=40)
    ap.add_argument("--only", default=None, help="Restrict to a single dataset name")
    args = ap.parse_args()
    asyncio.run(main_async(args.concurrency, args.model, args.max_turns, args.only))


if __name__ == "__main__":
    main()
