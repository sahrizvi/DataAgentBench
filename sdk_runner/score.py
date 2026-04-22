"""Score results.jsonl against each query's validate.py and print pass@1."""
from __future__ import annotations
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSONL_PATH = REPO / "sdk_runner" / "results" / "results.jsonl"


def load_validate(query_dir: Path):
    spec = importlib.util.spec_from_file_location("validate", str(query_dir / "validate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod.validate


def main() -> None:
    if not JSONL_PATH.exists():
        raise SystemExit(f"{JSONL_PATH} does not exist; run sweep first")

    per_dataset = defaultdict(lambda: [0, 0])  # [correct, total]
    details: list[tuple[str, str, bool, str]] = []

    for line in JSONL_PATH.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        dataset = rec["dataset"]
        qid = rec["query"]
        ans = rec.get("answer", "") or ""
        q_dir = REPO / f"query_{dataset}" / f"query{qid}"
        if not (q_dir / "validate.py").exists():
            print(f"MISSING validate: {dataset}/query{qid}")
            continue
        try:
            validate = load_validate(q_dir)
            if ans == "":
                is_valid, reason = False, "empty answer"
            else:
                is_valid, reason = validate(ans)
        except Exception as e:
            is_valid, reason = False, f"validate crashed: {type(e).__name__}: {e}"
        per_dataset[dataset][1] += 1
        per_dataset[dataset][0] += int(bool(is_valid))
        details.append((dataset, qid, bool(is_valid), reason))

    print("\n== Per query ==")
    for ds, qid, ok, reason in sorted(details):
        mark = "PASS" if ok else "FAIL"
        print(f"  {mark:4} {ds}/query{qid}  ({reason[:80]})")

    print("\n== Per dataset ==")
    total_c, total_t = 0, 0
    for ds in sorted(per_dataset):
        c, t = per_dataset[ds]
        total_c += c
        total_t += t
        print(f"  {ds:25s} {c}/{t}  ({c/t:.2%})")
    print(f"\n  OVERALL pass@1: {total_c}/{total_t} = {total_c/total_t:.4f}")


if __name__ == "__main__":
    main()
