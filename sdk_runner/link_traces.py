"""For each record in results.jsonl, find its auto-saved SDK transcript in
~/.claude/projects/ by matching the query text, copy it into sdk_runner/results/traces/,
and rewrite results.jsonl with session_id + trace_path in meta.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO / "sdk_runner" / "results"
TRACES_DIR = RESULTS_DIR / "traces"
JSONL_PATH = RESULTS_DIR / "results.jsonl"
PROJECTS_ROOT = Path.home() / ".claude" / "projects"


def encoded_cwd(dataset: str) -> str:
    cwd = REPO / f"query_{dataset}"
    return "-" + str(cwd).lstrip("/").replace("/", "-").replace("_", "-").replace(".", "-")


def load_query_text(dataset: str, qid: str) -> str:
    qi = json.loads((REPO / f"query_{dataset}" / f"query{qid}" / "query.json").read_text())
    return qi if isinstance(qi, str) else qi["query"]


def find_session(dataset: str, query_text: str, used: set[Path]) -> tuple[str, Path] | None:
    pdir = PROJECTS_ROOT / encoded_cwd(dataset)
    if not pdir.exists():
        return None
    # Match on the first-line queue-operation.content == query_text, prefer unused
    candidates: list[tuple[float, Path, str]] = []
    for jf in pdir.glob("*.jsonl"):
        try:
            first = jf.open().readline()
            obj = json.loads(first)
        except Exception:
            continue
        if obj.get("content", "").strip() == query_text.strip():
            candidates.append((jf.stat().st_mtime, jf, jf.stem))
    # Prefer the most recent unused one
    candidates.sort(reverse=True)
    for _, jf, sid in candidates:
        if jf not in used:
            return sid, jf
    return None


def main() -> None:
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    recs = [json.loads(line) for line in JSONL_PATH.read_text().splitlines() if line.strip()]
    used: set[Path] = set()
    updated = 0
    missing = 0
    for rec in recs:
        ds = rec["dataset"]
        qid = str(rec["query"])
        meta = rec.setdefault("meta", {})
        if meta.get("session_id") and meta.get("trace_path"):
            used.add(PROJECTS_ROOT / encoded_cwd(ds) / f"{meta['session_id']}.jsonl")
            continue
        try:
            qtext = load_query_text(ds, qid)
        except Exception as e:
            print(f"  MISS {ds}/query{qid} — query.json unreadable: {e}")
            missing += 1
            continue
        hit = find_session(ds, qtext, used)
        if not hit:
            print(f"  MISS {ds}/query{qid} — no transcript match")
            missing += 1
            continue
        sid, src = hit
        dst = TRACES_DIR / f"{ds}_query{qid}.jsonl"
        dst.write_bytes(src.read_bytes())
        used.add(src)
        meta["session_id"] = sid
        meta["trace_path"] = str(dst.relative_to(REPO))
        updated += 1

    with JSONL_PATH.open("w") as f:
        for rec in recs:
            f.write(json.dumps(rec) + "\n")
    print(f"Linked {updated} traces, missing {missing}")


if __name__ == "__main__":
    main()
