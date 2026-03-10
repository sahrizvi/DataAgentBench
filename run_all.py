"""
Run the full DAB benchmark: all queries × N runs for a given model.

Usage:
    # Run 50 trials of all queries (leaderboard submission)
    python run_all.py --llm gpt-5-mini --runs 50 --use_hints

    # Quick smoke test (1 run per query)
    python run_all.py --llm gpt-5-mini --runs 1

    # Run specific datasets only
    python run_all.py --llm gpt-5-mini --runs 50 --datasets bookreview stockindex

    # Resume an interrupted run (skips completed runs)
    python run_all.py --llm gpt-5-mini --runs 50 --use_hints
"""

from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime
import subprocess
import sys
import json
import os

ROOT = Path(os.path.dirname(os.path.abspath(__file__)))

DATASET_LIST = [
    "bookreview",
    "crmarenapro",
    "DEPS_DEV_V1",
    "GITHUB_REPOS",
    "googlelocal",
    "PANCANCER_ATLAS",
    "PATENTS",
    "stockindex",
    "stockmarket",
    "yelp",
    "agnews",
    "music_brainz_20k",
]


def discover_queries(dataset):
    """Find all query IDs for a dataset."""
    dataset_dir = ROOT / f"query_{dataset}"
    if not dataset_dir.exists():
        return []
    query_ids = []
    for p in dataset_dir.iterdir():
        if p.is_dir() and p.name.startswith("query"):
            try:
                query_ids.append(int(p.name.replace("query", "")))
            except ValueError:
                continue
    return sorted(query_ids)


def run_is_complete(dataset, query_id, run_id, results_dir):
    """Check if a run already has a final_agent.json."""
    result_path = (
        results_dir / f"query_{dataset}" / f"query{query_id}" / f"run_{run_id}" / "final_agent.json"
    )
    return result_path.exists()


def run_single(dataset, query_id, run_id, llm, iterations, use_hints):
    """Run a single query trial via run_agent.py."""
    cmd = [
        sys.executable, str(ROOT / "run_agent.py"),
        "--dataset", dataset,
        "--query_id", str(query_id),
        "--llm", llm,
        "--iterations", str(iterations),
        "--root_name", f"run_{run_id}",
    ]
    if use_hints:
        cmd.append("--use_hints")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return result.returncode == 0, result.stderr


def main():
    parser = ArgumentParser(description="Run the full DAB benchmark.")
    parser.add_argument("--llm", type=str, required=True, help="LLM deployment name (e.g., gpt-5-mini)")
    parser.add_argument("--runs", type=int, default=50, help="Number of runs per query (default: 50)")
    parser.add_argument("--iterations", type=int, default=100, help="Max agent iterations per run (default: 100)")
    parser.add_argument("--use_hints", action="store_true", help="Use dataset hints")
    parser.add_argument("--datasets", nargs="+", choices=DATASET_LIST, default=DATASET_LIST, help="Datasets to run (default: all)")
    parser.add_argument("--results_dir", type=str, default=None, help="Results directory (default: results-<llm>)")
    args = parser.parse_args()

    results_dir = Path(args.results_dir) if args.results_dir else ROOT / f"results-{args.llm}"

    # Discover all (dataset, query_id) pairs
    tasks = []
    for dataset in args.datasets:
        for qid in discover_queries(dataset):
            tasks.append((dataset, qid))

    total_runs = len(tasks) * args.runs
    print(f"DAB Benchmark: {len(tasks)} queries × {args.runs} runs = {total_runs} total executions")
    print(f"Model: {args.llm} | Hints: {args.use_hints} | Max iterations: {args.iterations}")
    print(f"Results: {results_dir}")
    print()

    completed = 0
    skipped = 0
    failed = 0

    for task_idx, (dataset, qid) in enumerate(tasks):
        for run_id in range(args.runs):
            label = f"[{task_idx * args.runs + run_id + 1}/{total_runs}] {dataset}/query{qid}/run_{run_id}"

            if run_is_complete(dataset, qid, run_id, results_dir):
                skipped += 1
                continue

            print(f"{label} ... ", end="", flush=True)
            success, stderr = run_single(dataset, qid, run_id, args.llm, args.iterations, args.use_hints)

            if success:
                completed += 1
                print("✓")
            else:
                failed += 1
                err_line = stderr.strip().split("\n")[-1] if stderr else "unknown error"
                print(f"✗ ({err_line[:80]})")

    print(f"\nDone: {completed} completed, {skipped} skipped (already done), {failed} failed")


if __name__ == "__main__":
    main()
