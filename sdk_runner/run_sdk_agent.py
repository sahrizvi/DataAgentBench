"""Run one query from DataAgentBench with the Claude Agent SDK.

No ReAct scaffolding. The SDK's own tool loop runs the agent with all
built-in tools enabled (Bash, Read, Write, Edit, Grep, Glob, etc.).
The system prompt tells the agent exactly how to connect to each database
(SQLite/DuckDB paths, Postgres db_name, MongoDB db_name).

Output: appends one JSON record to results.jsonl with the final answer.
"""
from __future__ import annotations
import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
import yaml

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, SystemMessage

REPO = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO / "sdk_runner" / "results"
TRACES_DIR = RESULTS_DIR / "traces"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
TRACES_DIR.mkdir(parents=True, exist_ok=True)
JSONL_PATH = RESULTS_DIR / "results.jsonl"


def _encoded_cwd(cwd: Path) -> str:
    # Claude Code encodes an absolute cwd into a folder name under ~/.claude/projects/
    # by replacing path separators and dots with dashes.
    return "-" + str(cwd).lstrip("/").replace("/", "-").replace("_", "-").replace(".", "-")


def _save_trace(session_id: str, cwd: Path, dst: Path) -> bool:
    if not session_id:
        return False
    src = Path.home() / ".claude" / "projects" / _encoded_cwd(cwd) / f"{session_id}.jsonl"
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    return True

PG_HOST = "127.0.0.1"
PG_PORT = 5432
PG_USER = os.environ.get("PGUSER") or os.environ.get("USER") or "postgres"
MONGO_URI = "mongodb://localhost:27017/"


def build_db_instructions(dataset_dir: Path) -> str:
    cfg = yaml.safe_load((dataset_dir / "db_config.yaml").read_text())["db_clients"]
    lines: list[str] = ["# Database access\n"]
    lines.append(
        "You have shell access via the `Bash` tool. Use the appropriate CLI for each "
        "database. Do NOT modify any data — queries must be read-only.\n"
    )
    for alias, c in cfg.items():
        t = c["db_type"]
        if t == "sqlite":
            path = (dataset_dir / c["db_path"]).resolve()
            lines.append(
                f"- **{alias}** (SQLite): file = `{path}`.\n"
                f"  Query: `sqlite3 '{path}' \"SELECT ...\"`"
            )
        elif t == "duckdb":
            path = (dataset_dir / c["db_path"]).resolve()
            lines.append(
                f"- **{alias}** (DuckDB): file = `{path}`.\n"
                f"  Query: `duckdb '{path}' \"SELECT ...\"` (read-only by default is fine; "
                "you can also pass `-readonly`)."
            )
        elif t == "postgres":
            lines.append(
                f"- **{alias}** (PostgreSQL): db_name = `{c['db_name']}`, "
                f"host = {PG_HOST}, port = {PG_PORT}, user = {PG_USER} (no password).\n"
                f"  Query: `psql -h {PG_HOST} -U {PG_USER} -d {c['db_name']} -c \"SELECT ...\"`"
            )
        elif t == "mongo":
            lines.append(
                f"- **{alias}** (MongoDB): db_name = `{c['db_name']}`, URI = `{MONGO_URI}`.\n"
                f"  Query via: `mongosh --quiet '{MONGO_URI}{c['db_name']}' --eval '...'` "
                "or use python3 with pymongo."
            )
    lines.append(
        "\nPython 3.12 is available with `pandas`, `duckdb`, `pymongo`, `psycopg2`, "
        "`sqlalchemy`. You can run python scripts via Bash if helpful.\n"
    )
    return "\n".join(lines)


SYSTEM_PROMPT_TMPL = """You are a senior data analyst solving one question against a small
set of pre-loaded databases. You have full shell access and should freely explore schemas,
run queries, join across databases, and compute results.

{db_instructions}

# How to answer
- Explore the relevant schemas before querying (columns may have surprising formats).
- Run as many queries as you need. Cross-check your result when useful.
- When you are confident, reply with a short, final, natural-language answer that directly
  answers the user's question. Include the key number(s) or entity names. Do not include
  step-by-step reasoning — just the final answer.
"""


def _extract_text(msg) -> str | None:
    """Best-effort extract text from an SDK message."""
    if isinstance(msg, ResultMessage):
        # ResultMessage has `.result` with the final assistant text
        return getattr(msg, "result", None)
    return None


async def run_one(dataset: str, query_id: int, model: str, max_turns: int) -> dict:
    ds_dir = REPO / f"query_{dataset}"
    if not ds_dir.exists():
        raise FileNotFoundError(ds_dir)
    q_dir = ds_dir / f"query{query_id}"
    if not q_dir.exists():
        raise FileNotFoundError(q_dir)

    query_info = json.loads((q_dir / "query.json").read_text())
    user_query = query_info if isinstance(query_info, str) else query_info["query"]

    db_desc = (ds_dir / "db_description.txt").read_text().strip()
    db_instructions = build_db_instructions(ds_dir)

    system_prompt = SYSTEM_PROMPT_TMPL.format(db_instructions=db_instructions)
    system_prompt += "\n# Dataset description\n" + db_desc + "\n"

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebSearch", "WebFetch"],
        permission_mode="bypassPermissions",
        model=model,
        max_turns=max_turns,
        cwd=str(ds_dir),
        setting_sources=[],  # don't auto-load local .claude / CLAUDE.md
    )

    start = time.time()
    final_result: str | None = None
    num_turns = None
    total_cost = None
    stop_reason = None
    session_id: str | None = None
    async for msg in query(prompt=user_query, options=options):
        if isinstance(msg, SystemMessage) and getattr(msg, "subtype", None) == "init":
            session_id = (getattr(msg, "data", {}) or {}).get("session_id")
        if isinstance(msg, ResultMessage):
            final_result = getattr(msg, "result", None)
            num_turns = getattr(msg, "num_turns", None)
            total_cost = getattr(msg, "total_cost_usd", None)
            stop_reason = getattr(msg, "subtype", None)
            if not session_id:
                session_id = getattr(msg, "session_id", None)
    dur = time.time() - start

    trace_dst = TRACES_DIR / f"{dataset}_query{query_id}.jsonl"
    trace_saved = _save_trace(session_id or "", ds_dir, trace_dst) if session_id else False

    rec = {
        "dataset": dataset,
        "query": str(query_id),
        "run": "0",
        "answer": final_result or "",
        "meta": {
            "model": model,
            "num_turns": num_turns,
            "total_cost_usd": total_cost,
            "duration_s": round(dur, 2),
            "stop_reason": stop_reason,
            "session_id": session_id,
            "trace_path": str(trace_dst.relative_to(REPO)) if trace_saved else None,
        },
    }
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--query_id", type=int, required=True)
    ap.add_argument("--model", default="claude-opus-4-7")
    ap.add_argument("--max_turns", type=int, default=40)
    args = ap.parse_args()

    rec = asyncio.run(run_one(args.dataset, args.query_id, args.model, args.max_turns))
    with JSONL_PATH.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec, indent=2))


if __name__ == "__main__":
    main()
