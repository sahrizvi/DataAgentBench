"""Self-contained interactive HTML report (plotly) with trace statistics,
partitioned by pass/fail.

Also flags "suspicious" runs — ones whose Bash commands touched
ground_truth.csv / validate.py directly or pulled external labeled datasets
(HuggingFace AG News, etc.). Those are listed at the top with a disqualified
pass@1 number.

Plots (interactive: hover, zoom, legend toggle):
  - Turns per run
  - Duration per run (s)
  - Cost per run (USD)
  - Tool calls per run
  - Avg tool calls per run, by tool
  - Bash commands classified by DB CLI
"""
from __future__ import annotations
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

import plotly.graph_objects as go

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "sdk_runner" / "results"
TRACES = RESULTS / "traces"
JSONL_PATH = RESULTS / "results.jsonl"
OUT_HTML = RESULTS / "report.html"

PASS_COLOR = "#2ca02c"
FAIL_COLOR = "#d62728"

# ---------- validation ---------------------------------------------------

def _validate_mod(q_dir: Path):
    spec = importlib.util.spec_from_file_location("validate", str(q_dir / "validate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def is_pass(dataset: str, qid: str, answer: str) -> bool:
    q_dir = REPO / f"query_{dataset}" / f"query{qid}"
    if not (q_dir / "validate.py").exists() or not answer:
        return False
    try:
        ok, _ = _validate_mod(q_dir).validate(answer)
        return bool(ok)
    except Exception:
        return False

# ---------- bash classification -----------------------------------------

DB_PATTERNS = [
    ("psql", re.compile(r"\bpsql\b", re.I)),
    ("sqlite3", re.compile(r"\bsqlite3\b", re.I)),
    ("duckdb", re.compile(r"\bduckdb\b", re.I)),
    ("mongosh", re.compile(r"\bmongosh\b", re.I)),
    ("python-db", re.compile(r"\b(pymongo|psycopg2?|sqlalchemy|sqlite3\.connect|duckdb\.connect)\b", re.I)),
]

# Patterns that signal the agent bypassed the task by reading the benchmark's
# ground-truth files or pulling external labeled datasets from the internet.
SUSPICIOUS_PATTERNS = [
    # Reading the benchmark's own answer files
    ("ground_truth.csv",  re.compile(r"ground_truth\.csv\b", re.I)),
    ("validate.py",       re.compile(r"validate\.py\b", re.I)),
    # HuggingFace datasets (labels for many public benchmarks)
    ("HuggingFace",       re.compile(r"\bload_dataset\s*\(|huggingface\.co|\bhf\.co\b|hf_hub_download|huggingface_hub|snapshot_download", re.I)),
    # Kaggle
    ("Kaggle",            re.compile(r"\bkaggle\.com\b|\bkaggle\s+(datasets|competitions)\b|\bkagglehub\b|kaggle-api", re.I)),
    # Other public ML dataset registries / loaders
    ("OpenML",            re.compile(r"\bopenml\.org\b|fetch_openml", re.I)),
    ("TFDS",              re.compile(r"\btensorflow_datasets\b|\btfds\.", re.I)),
    ("torchvision.datasets", re.compile(r"\btorchvision\.datasets\b", re.I)),
    ("sklearn built-ins", re.compile(r"\bsklearn\.datasets\.(fetch|load)_\w+", re.I)),
    ("UCI ML Repo",       re.compile(r"archive(-beta)?\.ics\.uci\.edu", re.I)),
    ("Zenodo",            re.compile(r"\bzenodo\.org\b", re.I)),
    ("data.gov",          re.compile(r"\bdata\.gov\b", re.I)),
    ("Papers with Code",  re.compile(r"\bpaperswithcode\.com\b", re.I)),
    # Known upstream sources for the specific DAB datasets
    ("Amazon reviews dump", re.compile(r"amazon[-_]reviews|jmcauley\.ucsd\.edu|nijianmo\.github\.io", re.I)),
    ("Yelp Open Dataset", re.compile(r"yelp\.com/dataset", re.I)),
    ("MusicBrainz API",   re.compile(r"\bmusicbrainz\.org\b", re.I)),
    ("BigQuery public",   re.compile(r"bigquery-public-data", re.I)),
    ("GitHub Archive",    re.compile(r"\bgharchive\.org\b|\bgithubarchive\.org\b", re.I)),
]


def classify_bash(cmd: str) -> str:
    for label, pat in DB_PATTERNS:
        if pat.search(cmd):
            return label
    return "other"

# ---------- trace stats -------------------------------------------------

def trace_stats(trace_path: Path) -> dict:
    tool_counts: Counter = Counter()
    bash_by_kind: Counter = Counter()
    suspicious: dict[str, str] = {}
    for line in trace_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") != "assistant":
            continue
        content = (ev.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for b in content:
            if not isinstance(b, dict) or b.get("type") != "tool_use":
                continue
            name = b.get("name", "?")
            tool_counts[name] += 1
            input_blob = json.dumps(b.get("input") or {})
            for label, pat in SUSPICIOUS_PATTERNS:
                if pat.search(input_blob):
                    suspicious.setdefault(label, input_blob[:200])
            if name == "Bash":
                cmd = (b.get("input") or {}).get("command", "")
                bash_by_kind[classify_bash(cmd)] += 1
    return {"tool_counts": tool_counts, "bash_by_kind": bash_by_kind,
            "suspicious": suspicious}

# ---------- plots -------------------------------------------------------

_PLOT_H = 280
_COMMON_LAYOUT = dict(
    height=_PLOT_H,
    margin=dict(l=45, r=15, t=40, b=40),
    title_font_size=13,
    font_size=10,
    legend=dict(font_size=10, orientation="h", yanchor="bottom", y=1.02, x=0),
)


def hist_pair(pass_vals, fail_vals, title, xlabel) -> go.Figure:
    fig = go.Figure()
    fig.add_histogram(x=pass_vals, name=f"PASS (n={len(pass_vals)})",
                      marker_color=PASS_COLOR, opacity=0.75)
    fig.add_histogram(x=fail_vals, name=f"FAIL (n={len(fail_vals)})",
                      marker_color=FAIL_COLOR, opacity=0.75)
    fig.update_layout(title=title, barmode="overlay",
                      xaxis_title=xlabel, yaxis_title="queries",
                      **_COMMON_LAYOUT)
    return fig


def bar_pair(keys, pass_counts, fail_counts, title, ylabel) -> go.Figure:
    fig = go.Figure()
    fig.add_bar(x=keys, y=pass_counts, name="PASS", marker_color=PASS_COLOR,
                hovertemplate="%{x}<br>PASS: %{y}<extra></extra>")
    fig.add_bar(x=keys, y=fail_counts, name="FAIL", marker_color=FAIL_COLOR,
                hovertemplate="%{x}<br>FAIL: %{y}<extra></extra>")
    fig.update_layout(title=title, barmode="group",
                      yaxis_title=ylabel, **_COMMON_LAYOUT)
    return fig


def scatter_dots(pass_stats, fail_stats, xkey, ykey, title) -> go.Figure:
    def points(rows, label, color):
        xs = [s.get(xkey) for s in rows if s.get(xkey) is not None and s.get(ykey) is not None]
        ys = [s.get(ykey) for s in rows if s.get(xkey) is not None and s.get(ykey) is not None]
        texts = [f"{s['dataset']}/query{s['query']}" for s in rows if s.get(xkey) is not None and s.get(ykey) is not None]
        return go.Scatter(x=xs, y=ys, text=texts, mode="markers", name=label,
                          marker=dict(color=color, size=8, opacity=0.8,
                                      line=dict(width=0.5, color="white")),
                          hovertemplate="%{text}<br>" + f"{xkey}=%{{x}}<br>{ykey}=%{{y}}<extra></extra>")
    fig = go.Figure()
    fig.add_trace(points(pass_stats, "PASS", PASS_COLOR))
    fig.add_trace(points(fail_stats, "FAIL", FAIL_COLOR))
    fig.update_layout(title=title, xaxis_title=xkey, yaxis_title=ykey,
                      **_COMMON_LAYOUT)
    return fig


def summary_table_html(pass_stats, fail_stats) -> str:
    def summarize(rows, key):
        vals = [r.get(key) for r in rows if isinstance(r.get(key), (int, float))]
        if not vals:
            return "-"
        vals.sort()
        mean = sum(vals) / len(vals)
        median = vals[len(vals) // 2]
        return f"mean={mean:.1f}, median={median:.1f}, min={min(vals):.1f}, max={max(vals):.1f}"

    def sum_tool(rows, t):
        return sum(r["tool_counts"].get(t, 0) for r in rows)
    rows = [
        ("N queries", len(pass_stats), len(fail_stats)),
        ("Total tool calls",
         sum(sum(r["tool_counts"].values()) for r in pass_stats),
         sum(sum(r["tool_counts"].values()) for r in fail_stats)),
        ("Total Bash calls", sum_tool(pass_stats, "Bash"), sum_tool(fail_stats, "Bash")),
        ("DB queries (psql/sqlite/duckdb/mongo/pydb)",
         sum(sum(v for k, v in r["bash_by_kind"].items() if k != "other") for r in pass_stats),
         sum(sum(v for k, v in r["bash_by_kind"].items() if k != "other") for r in fail_stats)),
        ("Turns / run", summarize(pass_stats, "num_turns"), summarize(fail_stats, "num_turns")),
        ("Duration (s)", summarize(pass_stats, "duration_s"), summarize(fail_stats, "duration_s")),
        ("Cost (USD)", summarize(pass_stats, "total_cost_usd"), summarize(fail_stats, "total_cost_usd")),
    ]
    body = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return ("<table><thead><tr><th>metric</th><th>PASS</th><th>FAIL</th></tr></thead>"
            f"<tbody>{body}</tbody></table>")


def main() -> None:
    recs = [json.loads(l) for l in JSONL_PATH.read_text().splitlines() if l.strip()]
    pass_stats: list[dict] = []
    fail_stats: list[dict] = []
    for rec in recs:
        ds, qid = rec["dataset"], str(rec["query"])
        meta = rec.get("meta") or {}
        trace = TRACES / f"{ds}_query{qid}.jsonl"
        s = trace_stats(trace) if trace.exists() else {"tool_counts": Counter(), "bash_by_kind": Counter()}
        s.update({
            "dataset": ds, "query": qid,
            "num_turns": meta.get("num_turns"),
            "duration_s": meta.get("duration_s"),
            "total_cost_usd": meta.get("total_cost_usd"),
            "total_tool_calls": sum(s.get("tool_counts", Counter()).values()),
        })
        (pass_stats if is_pass(ds, qid, rec.get("answer", "") or "") else fail_stats).append(s)

    all_tools = sorted(
        {t for s in pass_stats + fail_stats for t in s["tool_counts"]},
        key=lambda t: -sum(s["tool_counts"].get(t, 0) for s in pass_stats + fail_stats),
    )

    def avg(rows, t):
        return (sum(s["tool_counts"].get(t, 0) for s in rows) / len(rows)) if rows else 0.0

    figs: list[tuple[str, go.Figure]] = [
        ("Turns per run", hist_pair(
            [s["num_turns"] for s in pass_stats if s["num_turns"] is not None],
            [s["num_turns"] for s in fail_stats if s["num_turns"] is not None],
            "Turns per run (PASS vs FAIL)", "num_turns",
        )),
        ("Duration per run", hist_pair(
            [s["duration_s"] for s in pass_stats if s["duration_s"] is not None],
            [s["duration_s"] for s in fail_stats if s["duration_s"] is not None],
            "Duration per run (s)", "seconds",
        )),
        ("Cost per run", hist_pair(
            [(s["total_cost_usd"] or 0) for s in pass_stats],
            [(s["total_cost_usd"] or 0) for s in fail_stats],
            "Cost per run (USD)", "USD",
        )),
        ("Tool calls per run", hist_pair(
            [s["total_tool_calls"] for s in pass_stats],
            [s["total_tool_calls"] for s in fail_stats],
            "Tool-use count per run", "tool_use count",
        )),
        ("Avg tool calls per run, by tool", bar_pair(
            all_tools,
            [avg(pass_stats, t) for t in all_tools],
            [avg(fail_stats, t) for t in all_tools],
            "Avg tool calls per run, by tool", "avg calls / run",
        )),
        ("Bash commands by DB CLI", bar_pair(
            ["psql", "sqlite3", "duckdb", "mongosh", "python-db", "other"],
            [sum(s["bash_by_kind"].get(k, 0) for s in pass_stats) for k in
             ["psql", "sqlite3", "duckdb", "mongosh", "python-db", "other"]],
            [sum(s["bash_by_kind"].get(k, 0) for s in fail_stats) for k in
             ["psql", "sqlite3", "duckdb", "mongosh", "python-db", "other"]],
            "Bash commands classified by DB CLI", "total bash calls",
        )),
        ("Per-query: turns vs duration", scatter_dots(
            pass_stats, fail_stats, "num_turns", "duration_s",
            "Each dot = one query (hover for dataset/query_id)",
        )),
        ("Per-query: total tool calls vs cost", scatter_dots(
            pass_stats, fail_stats, "total_tool_calls", "total_cost_usd",
            "Tool calls vs cost per query",
        )),
    ]

    style = """
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;
             max-width: 1200px; margin: 2em auto; color: #222; padding: 0 1em; }
      h1 { margin-bottom: 0.2em; }
      .sub { color: #666; margin-bottom: 1.5em; font-size: 0.9em; }
      table { border-collapse: collapse; margin-bottom: 1.5em; font-size: 0.9em; }
      th, td { border: 1px solid #ddd; padding: 4px 10px; text-align: left; }
      th { background: #f5f5f5; }
      .grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
              gap: 0.75em 1em; }
      .plot { margin: 0; min-width: 0; }
      .plot > div { width: 100% !important; }
      .js-plotly-plot, .plot-container { width: 100% !important; }
      code { font-size: 0.85em; }
    </style>
    """
    n_pass = len(pass_stats)
    n_total = n_pass + len(fail_stats)

    # Suspicious trace table (potential cheats)
    suspicious = [s for s in pass_stats + fail_stats if s.get("suspicious")]
    passed_but_cheated = sum(1 for s in pass_stats if s.get("suspicious"))
    clean_pass = n_pass - passed_but_cheated
    sus_rows = "".join(
        f"<tr><td>{s['dataset']}/query{s['query']}</td>"
        f"<td>{'PASS' if s in pass_stats else 'FAIL'}</td>"
        f"<td>{', '.join(s['suspicious'].keys())}</td>"
        f"<td><code>{list(s['suspicious'].values())[0][:140]}</code></td></tr>"
        for s in suspicious
    )
    sus_html = (
        f"<h2 style='margin-top:1em;'>Suspicious traces (potential cheating)</h2>"
        f"<div class='sub'>pass@1 if we disqualify cheats: {clean_pass}/{n_total} = "
        f"{clean_pass/n_total:.3f} &nbsp;&nbsp;|&nbsp;&nbsp; cheats among passes: {passed_but_cheated}/{n_pass}</div>"
        f"<table><thead><tr><th>query</th><th>verdict</th><th>patterns</th><th>sample</th></tr></thead>"
        f"<tbody>{sus_rows}</tbody></table>"
        if suspicious else ""
    )

    header = (
        f"<h1>DataAgentBench — Claude Agent SDK trace report</h1>"
        f"<div class='sub'>pass@1 = {n_pass}/{n_total} = {n_pass/n_total:.3f} "
        f"(model = claude-opus-4-7, 1 run/query)</div>"
        + summary_table_html(pass_stats, fail_stats)
        + sus_html
    )

    # Assemble plots into a 2-column grid.
    # include_plotlyjs='cdn' => small file, needs internet.
    # include_plotlyjs=True => ~3 MB but fully offline.
    body_parts = []
    first = True
    for _title, fig in figs:
        html_div = fig.to_html(
            full_html=False,
            include_plotlyjs=("cdn" if first else False),
            div_id=None,
            config={"responsive": True, "displaylogo": False},
            default_width="100%",
            default_height=f"{_PLOT_H}px",
        )
        first = False
        body_parts.append(f"<div class='plot'>{html_div}</div>")
    body = "<div class='grid'>" + "".join(body_parts) + "</div>"
    OUT_HTML.write_text(
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>DAB SDK trace report</title>{style}</head><body>{header}{body}</body></html>"
    )
    print(f"Wrote {OUT_HTML}  ({n_pass} pass / {len(fail_stats)} fail)")


if __name__ == "__main__":
    main()
