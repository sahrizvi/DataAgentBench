# Claude Agent SDK baseline

A minimal driver that runs DataAgentBench with the **Claude Agent SDK**
(`claude-agent-sdk`), no custom ReAct loop. The agent uses only the SDK's
built-in tools (`Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebSearch`,
`WebFetch`) and a system prompt that tells it how to reach each dataset's DBs.

## Result

**pass@1 = 25/54 = 0.463** with `claude-opus-4-7`, one run per query.
Per-dataset breakdown in `results/results.jsonl` / `results/submission.json`.

## Layout

```
sdk_runner/
├── run_sdk_agent.py     # single-query runner
├── sweep.py             # run all 54 queries (concurrency)
├── seed_dbs.py          # load PG + Mongo dumps from query_dataset/
├── link_traces.py       # copy SDK auto-saved transcripts into results/traces/
├── score.py             # score results.jsonl with each query's validate.py
├── to_harmony.py        # convert traces -> Harmony JSONL for Euphony
└── results/
    ├── results.jsonl        # one record/query: answer + session_id + trace_path
    ├── submission.json      # leaderboard-format (54 records)
    ├── traces/              # raw SDK transcripts (.jsonl per query)
    └── harmony/             # Harmony-format conversations for Euphony
        ├── all.jsonl            # 54 conversations, metadata.is_valid set
        ├── correct.jsonl        # 25 passing
        ├── incorrect.jsonl      # 29 failing
        ├── correct/*.jsonl      # per-query
        └── incorrect/*.jsonl
```

## View the traces in Euphony

[Euphony](https://openai.github.io/euphony/) is a browser-based viewer for
Harmony conversations. Deep links (no install):

- **All 54 runs:** https://openai.github.io/euphony/?path=https://raw.githubusercontent.com/ucbepic/DataAgentBench/BRANCH/sdk_runner/results/harmony/all.jsonl
- **Correct only (25):** https://openai.github.io/euphony/?path=https://raw.githubusercontent.com/ucbepic/DataAgentBench/BRANCH/sdk_runner/results/harmony/correct.jsonl
- **Incorrect only (29):** https://openai.github.io/euphony/?path=https://raw.githubusercontent.com/ucbepic/DataAgentBench/BRANCH/sdk_runner/results/harmony/incorrect.jsonl

Replace `BRANCH` with the branch these files live on.

Inside Euphony, each conversation ends with a `developer`-role message titled
**Evaluation — PASS/FAIL** that shows the agent's answer, `ground_truth.csv`,
and the full `validate.py` source side-by-side. Conversation metadata
(`is_valid`, `dataset`, `query`, `duration_s`, `total_cost_usd`, …) is visible
in Euphony's metadata panel; the JMESPath filter can narrow by any of those.

## Reproduce

```bash
# 1. Local services
brew install python@3.12 postgresql@17 mongodb-community duckdb git-lfs
brew services start postgresql@17 && brew services start mongodb-community

# 2. Data
git lfs install && git lfs pull
bash download.sh    # patent_publication.db from GDrive (~5 GB)

# 3. Python env
python3.12 -m venv .venv && source .venv/bin/activate
pip install claude-agent-sdk pymongo psycopg2-binary duckdb PyYAML pandas gdown

# 4. Seed Postgres + Mongo
python sdk_runner/seed_dbs.py

# 5. Run the full sweep (1 run/query, concurrency 6)
python sdk_runner/sweep.py --concurrency 6 --model claude-opus-4-7

# 6. Link transcripts -> results/traces/, score, convert to Harmony
python sdk_runner/link_traces.py
PYTHONPATH=$(pwd) python sdk_runner/score.py
PYTHONPATH=$(pwd) python sdk_runner/to_harmony.py
```
