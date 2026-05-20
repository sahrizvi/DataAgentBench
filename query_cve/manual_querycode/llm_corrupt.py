"""LLM-driven per-row corruption.

For each CVE we want to obfuscate, call Azure OpenAI to produce:
  - a `narrative_description` that re-tells the original CVE while implying
    its CVSS severity in natural language WITHOUT using the words critical /
    high / medium / low (or near-synonyms in a denylist)

Guardrails (each output must pass all checks; up to 3 retries; otherwise the
row is skipped and the original text is kept unchanged so we never lose data):

  * MUST contain no banned literal words (severity terms, denylisted near-synonyms,
    and close variants)
  * MUST be within [0.5x, 3.0x] the length of the original description
  * MUST be in English (heuristic: ascii ratio > 0.9)
  * MUST mention at least one noun from the original description (lexical overlap
    >= 1 content word) so we know the rewrite stayed on-topic

Output rows landed in clean/manifest.sqlite tables:
  planted_narrative_desc   (cve_id, severity, narrative)

CVSS base scores are intentionally NOT rewritten by this script. The corrupted
agent-visible vulns_db keeps exact numeric scores in mixed parseable text
formats, so numeric threshold queries are not band-inference tasks.
"""
from __future__ import annotations
import argparse
import os
import re
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN_DB = ROOT / "clean" / "clean.sqlite"
MANIFEST_DB = ROOT / "clean" / "manifest.sqlite"
ENV_FILE = ROOT.parent / ".env"  # repo root


def _load_env():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


_load_env()


def _client():
    from openai import AzureOpenAI
    return AzureOpenAI(
        api_key=os.environ["AZURE_API_KEY"],
        azure_endpoint=os.environ["AZURE_API_BASE"],
        api_version=os.environ["AZURE_API_VERSION"],
    )


# Words that would leak the answer in narrative form.
SEVERITY_DENY = {
    "critical", "crit", "criticality", "criticalities",
    "high", "highly", "high-severity", "high-impact",
    "medium", "moderate", "moderately", "medium-severity",
    "low", "minor", "low-severity", "low-impact",
    "severity", "sev",
}

DEPLOYMENT = os.environ.get("AZURE_DEPLOYMENT", "gpt-4o")


SEVERITY_PROMPT = """You are obfuscating a CVE description for a benchmark.

Rewrite the description so that the CVSS severity rating is *implied* by the
narrative consequences and exploitability you describe — but do NOT use any of
these words: critical, crit, high, medium, moderate, low, minor, severity, sev,
or their hyphenated variants. Convey severity through impact phrasing only.

Constraints:
- Stay faithful to the technical content of the original description (same
  product / weakness / mechanism). Do not invent capabilities.
- 1-3 sentences, similar length to the original.
- Do not state a CVSS score or rating.
- Do not include the words listed above (case-insensitive).

Severity to imply: {severity}

Phrasing motifs (pick one and weave it in naturally; vary phrasing):
{motifs}

Original CVE description:
{desc}

Output ONLY the rewritten description. No preamble.
"""


SEVERITY_MOTIFS = {
    "CRITICAL": (
        "- pre-authentication remote code execution against an exposed service\n"
        "- complete and immediate takeover with no user action required\n"
        "- the attacker needs no credentials and no user interaction\n"
        "- internet-exposed; mass scanning + drive-by exploitation realistic"
    ),
    "HIGH": (
        "Important: even though this is impactful, it is NOT pre-auth full takeover.\n"
        "Convey at least ONE of these constraints prominently:\n"
        "- requires the attacker to already hold valid credentials, OR\n"
        "- requires the victim to perform an action (open a file, click a link), OR\n"
        "- requires local network access (not internet-exposed), OR\n"
        "- only compromises one component / data type, not the whole system\n"
        "Phrasing should make clear there is a meaningful preconditioning that\n"
        "stops it from being a one-shot full-system takeover."
    ),
    "MEDIUM": (
        "- requires authentication AND user interaction together\n"
        "- discloses partial / non-sensitive information only\n"
        "- limited to a specific feature; no privilege escalation\n"
        "- exploitation requires unusual configuration to be present"
    ),
    "LOW": (
        "- only feasible with prior local console / physical access\n"
        "- impact is cosmetic or denial-of-service of a non-critical feature\n"
        "- no realistic attack path; theoretical concern only\n"
        "- requires the attacker to already be administrator"
    ),
}


def _length_bounds_ok(orig: str, new: str) -> bool:
    if not orig:
        return True
    lo = max(50, int(0.3 * len(orig)))
    hi = max(600, int(3.0 * len(orig)))
    return lo <= len(new) <= hi


def _ascii_ratio(s: str) -> float:
    if not s:
        return 1.0
    return sum(1 for c in s if ord(c) < 128) / len(s)


_TOK = re.compile(r"[a-z][a-z0-9_]{2,}")


def _content_overlap_ok(orig: str, new: str) -> bool:
    """Demand at least one content-word overlap so the rewrite stays on-topic."""
    o = set(_TOK.findall(orig.lower()))
    n = set(_TOK.findall(new.lower()))
    return len(o & n) >= 1


def _has_banned(text: str, banned: set[str]) -> str | None:
    text_l = text.lower()
    for w in banned:
        if re.search(rf"\b{re.escape(w)}\b", text_l):
            return w
    return None


VERIFY_SEVERITY_PROMPT = """Read the CVE description below and decide which
CVSS v3 severity classification it most naturally implies. Choose EXACTLY one:
- CRITICAL
- HIGH
- MEDIUM
- LOW

Output ONLY the label, nothing else.

Description: {desc}
"""


def classify_severity(client, narrative: str) -> str | None:
    try:
        r = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[{"role": "user", "content": VERIFY_SEVERITY_PROMPT.format(desc=narrative)}],
            max_tokens=10,
            temperature=0.0,
        )
        out = (r.choices[0].message.content or "").strip().upper()
        normalized = re.sub(r"[^A-Z]", "", out)
        return normalized if normalized in {"CRITICAL", "HIGH", "MEDIUM", "LOW"} else None
    except Exception:
        return None


def rewrite_severity(client, cve_id: str, severity: str, desc: str,
                     retries: int = 3) -> str | None:
    motifs = SEVERITY_MOTIFS.get(severity.upper())
    if not motifs:
        return None
    last_err = None
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=DEPLOYMENT,
                messages=[{
                    "role": "user",
                    "content": SEVERITY_PROMPT.format(
                        severity=severity.upper(), motifs=motifs, desc=desc
                    ),
                }],
                max_tokens=300,
                temperature=0.7,
            )
            out = (r.choices[0].message.content or "").strip()
            banned_hit = _has_banned(out, SEVERITY_DENY)
            if banned_hit:
                last_err = f"banned word: {banned_hit!r}"
                continue
            if not _length_bounds_ok(desc, out):
                last_err = f"length out of bounds ({len(out)} vs orig {len(desc)})"
                continue
            if _ascii_ratio(out) < 0.9:
                last_err = "non-english"
                continue
            if not _content_overlap_ok(desc, out):
                last_err = "no content overlap"
                continue
            # Roundtrip verifier: classifier must recover the same severity.
            implied = classify_severity(client, out)
            if implied != severity.upper():
                last_err = f"verifier disagreed: implied={implied!r} canonical={severity!r}"
                continue
            return out
        except Exception as e:
            last_err = str(e)[:120]
            time.sleep(1.5 ** attempt)
    print(f"  [skip {cve_id}] severity rewrite: {last_err}", file=sys.stderr)
    return None


def _ensure_manifest_tables():
    conn = sqlite3.connect(MANIFEST_DB)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS planted_narrative_desc (
      cve_id TEXT PRIMARY KEY, severity TEXT, narrative TEXT
    );
    """)
    conn.commit()
    conn.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=("kev", "all", "sample"), default="kev",
                    help="kev: only CVEs in KEV. all: every CVE with severity. "
                         "sample: random sample (use --sample-size)")
    ap.add_argument("--sample-size", type=int, default=200)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None,
                    help="Hard cap on rows processed (debug)")
    ap.add_argument("--force", action="store_true",
                    help="Regenerate selected rows even if already present in the manifest")
    ap.add_argument("--only-ids-file", type=Path, default=None,
                    help="Optional file containing one canonical CVE id per line to regenerate")
    args = ap.parse_args()

    _ensure_manifest_tables()

    clean = sqlite3.connect(CLEAN_DB)
    if args.scope == "kev":
        rows = clean.execute("""
            SELECT v.cve_id, v.cvss3_severity, d.value
            FROM cves v
            JOIN cve_descriptions d ON d.cve_id = v.cve_id AND d.lang='en'
            WHERE v.cve_id IN (SELECT cve_id FROM kev)
              AND v.cvss3_severity IS NOT NULL
        """).fetchall()
    elif args.scope == "sample":
        rows = clean.execute(f"""
            SELECT v.cve_id, v.cvss3_severity, d.value
            FROM cves v
            JOIN cve_descriptions d ON d.cve_id = v.cve_id AND d.lang='en'
            WHERE v.cvss3_severity IS NOT NULL
            ORDER BY v.cve_id
            LIMIT {args.sample_size}
        """).fetchall()
    else:
        rows = clean.execute("""
            SELECT v.cve_id, v.cvss3_severity, d.value
            FROM cves v
            JOIN cve_descriptions d ON d.cve_id = v.cve_id AND d.lang='en'
            WHERE v.cvss3_severity IS NOT NULL
        """).fetchall()
    clean.close()

    if args.only_ids_file:
        target_ids = {
            line.strip().upper()
            for line in args.only_ids_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        rows = [r for r in rows if r[0].upper() in target_ids]

    if args.limit:
        rows = rows[: args.limit]

    print(f"Processing {len(rows)} CVEs (scope={args.scope}, workers={args.workers})",
          flush=True)

    # already-done lookup so reruns are incremental
    mconn = sqlite3.connect(MANIFEST_DB)
    done_sev = set() if args.force or args.only_ids_file else {
        r[0] for r in mconn.execute("SELECT cve_id FROM planted_narrative_desc")
    }
    mconn.close()

    todo = [r for r in rows if r[0] not in done_sev]
    print(f"  {len(rows) - len(todo)} already done; {len(todo)} new", flush=True)
    if not todo:
        return

    n_sev_ok = 0
    client = _client()
    lock_conn = sqlite3.connect(MANIFEST_DB, isolation_level=None)
    lock_conn.execute("PRAGMA journal_mode=WAL")

    def work(row):
        cve_id, sev, desc = row
        out_sev = rewrite_severity(client, cve_id, sev, desc or "")
        return cve_id, sev, out_sev

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(work, r) for r in todo]
        for i, fut in enumerate(as_completed(futures), 1):
            cve_id, sev, out_sev = fut.result()
            if out_sev is not None:
                lock_conn.execute(
                    "INSERT OR REPLACE INTO planted_narrative_desc VALUES (?,?,?)",
                    (cve_id, sev, out_sev),
                )
                n_sev_ok += 1
            if i % 50 == 0:
                print(f"  [{i}/{len(todo)}] sev_ok={n_sev_ok}", flush=True)

    lock_conn.close()
    print(f"DONE: severity={n_sev_ok}/{len(todo)}")


if __name__ == "__main__":
    main()
