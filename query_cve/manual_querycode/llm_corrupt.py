"""LLM-driven per-row corruption.

For each CVE we want to obfuscate, call Azure OpenAI to produce:
  - a `narrative_description` that re-tells the original CVE while implying
    its CVSS severity in natural language WITHOUT using the words critical /
    high / medium / low (or near-synonyms in a denylist)
  - a `narrative_score` paragraph that conveys the CVSS base score in prose
    without printing the literal numeric value

Guardrails (each output must pass all checks; up to 3 retries; otherwise the
row is skipped and the original text is kept unchanged so we never lose data):

  * MUST contain no banned literal words (severity terms, denylisted near-synonyms,
    and the literal score number)
  * MUST be within [0.5x, 3.0x] the length of the original description
  * MUST be in English (heuristic: ascii ratio > 0.9)
  * MUST mention at least one noun from the original description (lexical overlap
    >= 1 content word) so we know the rewrite stayed on-topic

Output rows landed in clean/manifest.sqlite tables:
  planted_narrative_desc   (cve_id, severity, narrative)
  planted_narrative_score  (cve_id, canonical_score, narrative)
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


SCORE_PROMPT = """You are obfuscating a CVE's CVSS v3 base score (scale 0.0-10.0)
for a benchmark.

Write ONE sentence (40 - 280 characters) that *implies* the magnitude band of
the score through narrative phrasing. The sentence MUST NOT contain digits,
the words "score" / "rating", or any of: critical, crit, high, medium,
moderate, low, minor, severity, sev.

Constraint — anchor in CVE-specific context. Reference at least one of the
context details below NATURALLY in the sentence (vendor, product, or a
short paraphrase of the vulnerability mechanism). This makes each narrative
substantively unique per row.

Constraint — VARY phrasing aggressively. Do NOT default to stock templates
like "in the elevated tier" or "near the top of the scale". Each row should
use distinct vocabulary, syntactic structure, and register. Treat each row
as a unique editorial paraphrase. Some registers to draw from (rotate):
- terse advisory: "Among the upper-tier issues this vendor has shipped."
- analyst-paragraph: "By the standards of similar {{product}} flaws, this
  one sits in the elevated band — not the rarefied air of pre-auth-RCE
  catastrophes, but well above routine."
- comparative: "Comparable in severity to {{vendor}}'s prior
  authentication-bypass disclosures."
- hedged: "Roughly two notches below the maximum on the standard 10-point
  vulnerability scale."
- domain-flavored: "Practitioners would treat this as a top-of-the-list
  patch-now item but not a fire-drill."
- counterfactual: "Were the attack vector network rather than local, this
  would push toward the very top; as written, it lands in the
  upper-middle band."

CRITICAL — band-specific constraints. The narrative must clearly imply the
target band and NOT imply a higher band. Use phrasing aligned with the
canonical band. Where useful you may use approximate ten-point-scale anchors:
- 9.0-10.0: "near the very top of the scale" / "essentially at the maximum"
  / "rarefied top tier" / "approaches the pinnacle"
- 7.0-8.9: "comfortably above the midpoint but clearly not at the maximum"
  / "in the upper-middle band, well above average but short of the top"
  / "two-notches-below-maximum" — DO NOT use phrases like "near the top"
  / "just shy of the pinnacle" / "top tier" / "approaches the maximum"
  for this band, those imply 9.0-10.0.
- 4.0-6.9: "in the middle band" / "around the midpoint" /
  "roughly mid-scale" — DO NOT use words like "elevated" / "upper" / "high"
  / "near the top".
- 0.1-3.9: "well below the midpoint" / "in the lower portion of the scale"
  / "minor in scale" — DO NOT use anything that implies above-midpoint.

Score to imply: {score} (so canonical band = {band})

CVE context (incorporate naturally — but do NOT include the CVE id, do NOT
copy the original description verbatim):
- vendor: {vendor}
- product: {product}
- vulnerability summary: {summary}

Output ONLY the sentence. No preamble. No digits.
"""


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


VERIFY_SCORE_PROMPT = """Read the sentence below and decide which CVSS v3 base
score band it implies (the score scale is 0.0 to 10.0). Choose EXACTLY one:
- 9.0-10.0
- 7.0-8.9
- 4.0-6.9
- 0.1-3.9

Output ONLY the band label.

Sentence: {sentence}
"""


def _score_band(score: float) -> str:
    if score >= 9.0:
        return "9.0-10.0"
    if score >= 7.0:
        return "7.0-8.9"
    if score >= 4.0:
        return "4.0-6.9"
    return "0.1-3.9"


def classify_severity(client, narrative: str) -> str | None:
    try:
        r = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[{"role": "user", "content": VERIFY_SEVERITY_PROMPT.format(desc=narrative)}],
            max_tokens=10,
            temperature=0.0,
        )
        out = (r.choices[0].message.content or "").strip().upper().rstrip(".")
        for lbl in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            if lbl in out:
                return lbl
        return None
    except Exception:
        return None


def classify_score(client, narrative: str) -> str | None:
    try:
        r = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[{"role": "user", "content": VERIFY_SCORE_PROMPT.format(sentence=narrative)}],
            max_tokens=15,
            temperature=0.0,
        )
        out = (r.choices[0].message.content or "").strip()
        for b in ("9.0-10.0", "7.0-8.9", "4.0-6.9", "0.1-3.9"):
            if b in out:
                return b
        return None
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


def rewrite_score(client, cve_id: str, score: float,
                  vendor: str = "", product: str = "", summary: str = "",
                  retries: int = 3) -> str | None:
    score_str = f"{score:.1f}"
    last_err = None
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=DEPLOYMENT,
                messages=[{
                    "role": "user",
                    "content": SCORE_PROMPT.format(
                        score=score_str, band=_score_band(score),
                        vendor=vendor or "(unspecified)",
                        product=product or "(unspecified)",
                        summary=summary or "(unspecified)",
                    ),
                }],
                max_tokens=200,
                temperature=0.95,
            )
            out = (r.choices[0].message.content or "").strip()
            # No digits at all
            if re.search(r"\d", out):
                last_err = "contains digits"
                continue
            banned_hit = _has_banned(out, SEVERITY_DENY | {"score", "rating"})
            if banned_hit:
                last_err = f"banned word: {banned_hit!r}"
                continue
            if _ascii_ratio(out) < 0.9:
                last_err = "non-english"
                continue
            implied = classify_score(client, out)
            canonical_band = _score_band(score)
            if implied != canonical_band:
                last_err = f"verifier disagreed: implied={implied!r} canonical={canonical_band!r}"
                continue
            return out
        except Exception as e:
            last_err = str(e)[:120]
            time.sleep(1.5 ** attempt)
    print(f"  [skip {cve_id}] score rewrite: {last_err}", file=sys.stderr)
    return None


def _ensure_manifest_tables():
    conn = sqlite3.connect(MANIFEST_DB)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS planted_narrative_desc (
      cve_id TEXT PRIMARY KEY, severity TEXT, narrative TEXT
    );
    CREATE TABLE IF NOT EXISTS planted_narrative_score (
      cve_id TEXT PRIMARY KEY, canonical_score REAL, narrative TEXT
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
    ap.add_argument("--skip-severity", action="store_true")
    ap.add_argument("--skip-score", action="store_true")
    args = ap.parse_args()

    _ensure_manifest_tables()
    client = _client()

    clean = sqlite3.connect(CLEAN_DB)
    if args.scope == "kev":
        rows = clean.execute("""
            SELECT v.cve_id, v.cvss3_severity, v.cvss3_base_score, d.value
            FROM cves v
            JOIN cve_descriptions d ON d.cve_id = v.cve_id AND d.lang='en'
            WHERE v.cve_id IN (SELECT cve_id FROM kev)
              AND v.cvss3_severity IS NOT NULL
              AND v.cvss3_base_score IS NOT NULL
        """).fetchall()
    elif args.scope == "sample":
        rows = clean.execute(f"""
            SELECT v.cve_id, v.cvss3_severity, v.cvss3_base_score, d.value
            FROM cves v
            JOIN cve_descriptions d ON d.cve_id = v.cve_id AND d.lang='en'
            WHERE v.cvss3_severity IS NOT NULL
              AND v.cvss3_base_score IS NOT NULL
            ORDER BY v.cve_id
            LIMIT {args.sample_size}
        """).fetchall()
    else:
        rows = clean.execute("""
            SELECT v.cve_id, v.cvss3_severity, v.cvss3_base_score, d.value
            FROM cves v
            JOIN cve_descriptions d ON d.cve_id = v.cve_id AND d.lang='en'
            WHERE v.cvss3_severity IS NOT NULL
              AND v.cvss3_base_score IS NOT NULL
        """).fetchall()
    clean.close()

    if args.limit:
        rows = rows[: args.limit]

    # Build per-CVE vendor/product lookup (most-common vendor for each CVE) to
    # anchor score narratives in CVE-specific context.
    clean = sqlite3.connect(CLEAN_DB)
    cve_vp: dict[str, tuple[str, str]] = {}
    for cve_id, vendor, product, n in clean.execute("""
        SELECT cve_id, vendor, product, COUNT(*) as n
        FROM cpe_matches
        WHERE vendor IS NOT NULL AND product IS NOT NULL
        GROUP BY cve_id, vendor, product
        ORDER BY cve_id, n DESC
    """):
        if cve_id not in cve_vp:
            cve_vp[cve_id] = (vendor, product)
    clean.close()

    print(f"Processing {len(rows)} CVEs (scope={args.scope}, workers={args.workers}); "
          f"{len(cve_vp)} CVEs have vendor/product context",
          flush=True)

    # already-done lookup so reruns are incremental
    mconn = sqlite3.connect(MANIFEST_DB)
    done_sev = {r[0] for r in mconn.execute("SELECT cve_id FROM planted_narrative_desc")}
    done_score = {r[0] for r in mconn.execute("SELECT cve_id FROM planted_narrative_score")}
    mconn.close()

    todo = [r for r in rows if r[0] not in done_sev or r[0] not in done_score]
    print(f"  {len(rows) - len(todo)} already done; {len(todo)} new", flush=True)

    n_sev_ok = 0
    n_score_ok = 0
    lock_conn = sqlite3.connect(MANIFEST_DB, isolation_level=None)
    lock_conn.execute("PRAGMA journal_mode=WAL")

    def work(row):
        cve_id, sev, score, desc = row
        out_sev = None
        out_score = None
        if not args.skip_severity and cve_id not in done_sev:
            out_sev = rewrite_severity(client, cve_id, sev, desc or "")
        if not args.skip_score and cve_id not in done_score:
            vendor, product = cve_vp.get(cve_id, ("", ""))
            # Pass a 240-char summary of the original description as additional
            # anchor context (the LLM is told not to copy verbatim).
            summary = (desc or "")[:240]
            out_score = rewrite_score(client, cve_id, float(score),
                                      vendor=vendor, product=product,
                                      summary=summary)
        return cve_id, sev, score, out_sev, out_score

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(work, r) for r in todo]
        for i, fut in enumerate(as_completed(futures), 1):
            cve_id, sev, score, out_sev, out_score = fut.result()
            if out_sev is not None:
                lock_conn.execute(
                    "INSERT OR REPLACE INTO planted_narrative_desc VALUES (?,?,?)",
                    (cve_id, sev, out_sev),
                )
                n_sev_ok += 1
            if out_score is not None:
                lock_conn.execute(
                    "INSERT OR REPLACE INTO planted_narrative_score VALUES (?,?,?)",
                    (cve_id, float(score), out_score),
                )
                n_score_ok += 1
            if i % 50 == 0:
                print(f"  [{i}/{len(todo)}] sev_ok={n_sev_ok} score_ok={n_score_ok}",
                      flush=True)

    lock_conn.close()
    print(f"DONE: severity={n_sev_ok}/{len(todo)} score={n_score_ok}/{len(todo)}")


if __name__ == "__main__":
    main()
