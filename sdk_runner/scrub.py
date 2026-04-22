"""In-place scrub local-machine identifiers from trace + harmony JSONL files.

Replacements (longest prefix first):
  <repo absolute path>   -> /workspace/DataAgentBench
  $HOME                  -> /Users/user
  <username> ($USER)     -> user

Designed to be safe to commit: pulls all identifiers from the environment so
the source file contains no personal strings.
"""
from __future__ import annotations
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TARGETS = [
    REPO / "sdk_runner" / "results" / "traces",
    REPO / "sdk_runner" / "results" / "harmony",
    REPO / "sdk_runner" / "results" / "results.jsonl",
    REPO / "sdk_runner" / "results" / "submission.json",
]

USER = os.environ.get("USER", "")
HOME = os.environ.get("HOME", "")

REPLACEMENTS = [
    (str(REPO), "/workspace/DataAgentBench"),
    *(( [(HOME, "/Users/user")] ) if HOME else []),
    *(( [(USER, "user")] ) if USER else []),
]


def scrub_file(p: Path) -> int:
    raw = p.read_bytes()
    original = raw
    for old, new in REPLACEMENTS:
        if not old:
            continue
        raw = raw.replace(old.encode(), new.encode())
    if raw != original:
        p.write_bytes(raw)
        return 1
    return 0


def main() -> None:
    changed = 0
    scanned = 0
    for t in TARGETS:
        if t.is_file():
            scanned += 1
            changed += scrub_file(t)
        elif t.is_dir():
            for p in t.rglob("*.jsonl"):
                scanned += 1
                changed += scrub_file(p)
    print(f"Scanned {scanned} files, modified {changed}.")


if __name__ == "__main__":
    main()
