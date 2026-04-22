"""Convert Claude Agent SDK traces -> Harmony-format JSONL for Euphony.

Splits output into correct/ and incorrect/ folders based on each query's
validate.py. One .jsonl per query (a single Harmony `Conversation` per file).

Usage:
    PYTHONPATH=/Users/shreyashankar/Documents/projects/DataAgentBench \
    python sdk_runner/to_harmony.py
"""
from __future__ import annotations
import importlib.util
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "sdk_runner" / "results"
TRACES = RESULTS / "traces"
OUT = RESULTS / "harmony"
OUT_CORRECT = OUT / "correct"
OUT_INCORRECT = OUT / "incorrect"
JSONL_PATH = RESULTS / "results.jsonl"


def _load_validate(query_dir: Path):
    spec = importlib.util.spec_from_file_location("validate", str(query_dir / "validate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod.validate


def _is_valid(dataset: str, qid: str, answer: str) -> tuple[bool, str]:
    q_dir = REPO / f"query_{dataset}" / f"query{qid}"
    if not (q_dir / "validate.py").exists():
        return False, "no validate.py"
    try:
        v = _load_validate(q_dir)
        if not answer:
            return False, "empty answer"
        ok, reason = v(answer)
        return bool(ok), str(reason)
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def _flatten_tool_result(content) -> str:
    """Tool result content can be a string or a list of {type:text,text:...} blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict):
                if "text" in b:
                    parts.append(str(b["text"]))
                else:
                    parts.append(json.dumps(b))
            else:
                parts.append(str(b))
        return "\n".join(parts)
    return json.dumps(content)


def trace_to_conversation(trace_path: Path, meta: dict) -> dict:
    """Read a Claude SDK trace JSONL and emit a Harmony Conversation dict."""
    messages: list[dict] = []
    tool_use_name: dict[str, str] = {}  # tool_use_id -> tool name

    for line in trace_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = ev.get("type")
        msg = ev.get("message") or {}
        content = msg.get("content")

        if t == "user":
            if isinstance(content, str):
                messages.append({"role": "user", "content": content})
            elif isinstance(content, list):
                for b in content:
                    if not isinstance(b, dict):
                        continue
                    bt = b.get("type")
                    if bt == "tool_result":
                        name = tool_use_name.get(b.get("tool_use_id", ""), "tool")
                        text = _flatten_tool_result(b.get("content", ""))
                        messages.append({
                            "role": "tool",
                            "name": f"functions.{name}",
                            "content": text,
                            "channel": "commentary",
                        })
                    elif bt == "text":
                        messages.append({"role": "user", "content": b.get("text", "")})
        elif t == "assistant":
            if not isinstance(content, list):
                continue
            for b in content:
                if not isinstance(b, dict):
                    continue
                bt = b.get("type")
                if bt == "text":
                    messages.append({
                        "role": "assistant",
                        "channel": "final",
                        "content": b.get("text", ""),
                    })
                elif bt == "thinking":
                    messages.append({
                        "role": "assistant",
                        "channel": "analysis",
                        "content": b.get("thinking", ""),
                    })
                elif bt == "tool_use":
                    name = b.get("name", "tool")
                    tool_use_name[b.get("id", "")] = name
                    inp = b.get("input", {})
                    body = json.dumps(inp, indent=2)
                    messages.append({
                        "role": "assistant",
                        "channel": "commentary",
                        "recipient": f"functions.{name}",
                        "content": [
                            {"content_type": "code", "text": body, "language": "json"}
                        ],
                    })
        # queue-operation / attachment / last-prompt / ai-title: skip

    return {
        "id": meta.get("session_id"),
        "messages": messages,
        "metadata": meta,
    }


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT_CORRECT.mkdir(parents=True, exist_ok=True)
    OUT_INCORRECT.mkdir(parents=True, exist_ok=True)
    agg_correct = OUT / "correct.jsonl"
    agg_incorrect = OUT / "incorrect.jsonl"
    agg_all = OUT / "all.jsonl"
    fc = agg_correct.open("w")
    fi = agg_incorrect.open("w")
    fa = agg_all.open("w")

    records = [json.loads(l) for l in JSONL_PATH.read_text().splitlines() if l.strip()]
    n_ok = n_bad = 0
    for rec in records:
        dataset = rec["dataset"]
        qid = str(rec["query"])
        answer = rec.get("answer", "") or ""
        meta_in = rec.get("meta") or {}
        ok, reason = _is_valid(dataset, qid, answer)
        meta = {
            "dataset": dataset,
            "query": qid,
            "is_valid": ok,
            "validation_reason": reason,
            "answer": answer,
            "model": meta_in.get("model"),
            "num_turns": meta_in.get("num_turns"),
            "duration_s": meta_in.get("duration_s"),
            "total_cost_usd": meta_in.get("total_cost_usd"),
            "session_id": meta_in.get("session_id"),
        }
        q_dir = REPO / f"query_{dataset}" / f"query{qid}"
        gt_path = q_dir / "ground_truth.csv"
        vp_path = q_dir / "validate.py"
        ground_truth = gt_path.read_text().strip() if gt_path.exists() else ""
        validate_src = vp_path.read_text() if vp_path.exists() else ""
        meta["ground_truth"] = ground_truth
        meta["validate_py"] = validate_src

        trace_path = TRACES / f"{dataset}_query{qid}.jsonl"
        if not trace_path.exists():
            print(f"  MISS trace {trace_path}")
            continue
        conv = trace_to_conversation(trace_path, meta)
        verdict = "PASS ✅" if ok else "FAIL ❌"
        eval_md = (
            f"## Evaluation — {verdict}\n\n"
            f"**Validation reason:** {reason}\n\n"
            f"**Agent's answer:**\n\n```\n{answer}\n```\n\n"
            f"**Ground truth (`ground_truth.csv`):**\n\n```\n{ground_truth}\n```\n\n"
            f"**Validator (`validate.py`):**\n\n```python\n{validate_src}```\n"
        )
        conv["messages"].append({
            "role": "developer",
            "channel": "commentary",
            "content": eval_md,
        })
        line = json.dumps(conv)
        out_dir = OUT_CORRECT if ok else OUT_INCORRECT
        (out_dir / f"{dataset}_query{qid}.jsonl").write_text(line + "\n")
        (fc if ok else fi).write(line + "\n")
        fa.write(line + "\n")
        if ok:
            n_ok += 1
        else:
            n_bad += 1
    fc.close()
    fi.close()
    fa.close()
    print(f"Wrote {n_ok} correct and {n_bad} incorrect conversations to {OUT}")


if __name__ == "__main__":
    main()
