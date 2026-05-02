"""Fetch a bounded NVD/KEV/EPSS snapshot into clean/clean.sqlite.

Scope (kept small to keep the benchmark dataset under ~50MB):
  - NVD CVEs: published 2023-01-01..2024-12-31 via the NVD 2.0 API
  - CISA KEV: full catalog (~1300 rows)
  - EPSS:    one snapshot date (yesterday) for every CVE we ingested

This is the canonical "clean" snapshot. It is NEVER what the agent sees —
the corruption pipeline reads from here and emits the agent-visible DBs in
query_dataset/. compute_ground_truth.py also reads from here.
"""
from __future__ import annotations
import csv
import gzip
import io
import json
import sqlite3
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN_DB = ROOT / "clean" / "clean.sqlite"

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_URL_TMPL = "https://epss.empiricalsecurity.com/epss_scores-{date}.csv.gz"

# NVD limits date ranges to 120 days, so we chunk.
WINDOW_START = date(2023, 1, 1)
WINDOW_END   = date(2024, 12, 31)
CHUNK_DAYS   = 120
PAGE         = 2000  # NVD API max


def _http_get(url: str, retries: int = 5) -> bytes:
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "DataAgentBench/cve"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            if i == retries - 1:
                raise
            wait = 2 ** i
            print(f"  retry {i+1}/{retries} after {wait}s: {e}", file=sys.stderr)
            time.sleep(wait)


def init_schema(conn: sqlite3.Connection) -> None:
    c = conn.cursor()
    c.executescript("""
    DROP TABLE IF EXISTS cves;
    DROP TABLE IF EXISTS cve_descriptions;
    DROP TABLE IF EXISTS cve_references;
    DROP TABLE IF EXISTS cpe_matches;
    DROP TABLE IF EXISTS kev;
    DROP TABLE IF EXISTS epss;

    CREATE TABLE cves (
      cve_id TEXT PRIMARY KEY,
      published TEXT,
      last_modified TEXT,
      vuln_status TEXT,
      cvss3_base_score REAL,
      cvss3_severity TEXT,
      cvss3_attack_vector TEXT,
      cvss3_vector TEXT
    );
    CREATE TABLE cve_descriptions (
      cve_id TEXT, lang TEXT, value TEXT
    );
    CREATE TABLE cve_references (
      cve_id TEXT, url TEXT, source TEXT
    );
    CREATE TABLE cpe_matches (
      cve_id TEXT,
      cpe_criteria TEXT,
      vendor TEXT,
      product TEXT,
      version TEXT,
      version_start_inc TEXT,
      version_start_exc TEXT,
      version_end_inc TEXT,
      version_end_exc TEXT,
      vulnerable INTEGER
    );
    CREATE TABLE kev (
      cve_id TEXT PRIMARY KEY,
      vendor_project TEXT,
      product TEXT,
      vulnerability_name TEXT,
      date_added TEXT,
      short_description TEXT,
      required_action TEXT,
      due_date TEXT,
      known_ransomware_use TEXT,
      notes TEXT
    );
    CREATE TABLE epss (
      cve_id TEXT, score_date TEXT, epss REAL, percentile REAL,
      PRIMARY KEY (cve_id, score_date)
    );
    CREATE INDEX idx_cpe_cve ON cpe_matches(cve_id);
    CREATE INDEX idx_cpe_vendor ON cpe_matches(vendor);
    """)
    conn.commit()


def _chunk_ranges():
    cur = WINDOW_START
    while cur <= WINDOW_END:
        end = min(cur + timedelta(days=CHUNK_DAYS - 1), WINDOW_END)
        yield (
            f"{cur.isoformat()}T00:00:00.000",
            f"{end.isoformat()}T23:59:59.999",
        )
        cur = end + timedelta(days=1)


def fetch_nvd(conn: sqlite3.Connection) -> set[str]:
    """Stream NVD CVEs across chunked windows into clean.sqlite. Return CVE id set."""
    cur = conn.cursor()
    seen: set[str] = set()
    for win_start, win_end in _chunk_ranges():
        start = 0
        while True:
            url = (
                f"{NVD_API}?pubStartDate={win_start}&pubEndDate={win_end}"
                f"&resultsPerPage={PAGE}&startIndex={start}"
            )
            print(f"NVD: window={win_start[:10]}..{win_end[:10]} startIndex={start}", flush=True)
            raw = _http_get(url)
            data = json.loads(raw)
            total = data.get("totalResults", 0)
            items = data.get("vulnerabilities", [])
            if not items:
                break
            for w in items:
                c = w.get("cve", {})
                cid = c.get("id")
                if not cid or cid in seen:
                    continue
                seen.add(cid)
                metrics = c.get("metrics", {}) or {}
                cvss = None
                for key in ("cvssMetricV31", "cvssMetricV30"):
                    if metrics.get(key):
                        cvss = metrics[key][0].get("cvssData", {})
                        break
                cur.execute(
                    "INSERT OR REPLACE INTO cves VALUES (?,?,?,?,?,?,?,?)",
                    (
                        cid,
                        c.get("published"),
                        c.get("lastModified"),
                        c.get("vulnStatus"),
                        (cvss or {}).get("baseScore"),
                        (cvss or {}).get("baseSeverity"),
                        (cvss or {}).get("attackVector"),
                        (cvss or {}).get("vectorString"),
                    ),
                )
                for d in c.get("descriptions", []) or []:
                    cur.execute(
                        "INSERT INTO cve_descriptions VALUES (?,?,?)",
                        (cid, d.get("lang"), d.get("value")),
                    )
                for r in c.get("references", []) or []:
                    cur.execute(
                        "INSERT INTO cve_references VALUES (?,?,?)",
                        (cid, r.get("url"), r.get("source")),
                    )
                for cfg in c.get("configurations", []) or []:
                    for node in cfg.get("nodes", []) or []:
                        for m in node.get("cpeMatch", []) or []:
                            crit = m.get("criteria", "")
                            parts = crit.split(":") if crit.startswith("cpe:2.3:") else []
                            vendor = parts[3] if len(parts) > 3 else None
                            product = parts[4] if len(parts) > 4 else None
                            version = parts[5] if len(parts) > 5 else None
                            cur.execute(
                                "INSERT INTO cpe_matches VALUES (?,?,?,?,?,?,?,?,?,?)",
                                (
                                    cid, crit, vendor, product, version,
                                    m.get("versionStartIncluding"),
                                    m.get("versionStartExcluding"),
                                    m.get("versionEndIncluding"),
                                    m.get("versionEndExcluding"),
                                    1 if m.get("vulnerable") else 0,
                                ),
                            )
            conn.commit()
            start += PAGE
            if start >= total:
                break
            time.sleep(6)  # NVD rate limit: 5 req / 30s without API key
    print(f"NVD: ingested {len(seen)} CVEs", flush=True)
    return seen


def fetch_kev(conn: sqlite3.Connection, allow: set[str]) -> int:
    raw = _http_get(KEV_URL)
    data = json.loads(raw)
    cur = conn.cursor()
    n = 0
    for v in data.get("vulnerabilities", []):
        cid = v.get("cveID")
        if not cid:
            continue
        # We intentionally keep KEV rows whose CVE isn't in `allow` —
        # those become referential-integrity gaps in the corrupted DB.
        cur.execute(
            "INSERT OR REPLACE INTO kev VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                cid,
                v.get("vendorProject"),
                v.get("product"),
                v.get("vulnerabilityName"),
                v.get("dateAdded"),
                v.get("shortDescription"),
                v.get("requiredAction"),
                v.get("dueDate"),
                v.get("knownRansomwareCampaignUse"),
                v.get("notes"),
            ),
        )
        n += 1
    conn.commit()
    print(f"KEV: ingested {n} entries", flush=True)
    return n


def fetch_epss(conn: sqlite3.Connection, allow: set[str], snapshot_dates: list[str]) -> int:
    cur = conn.cursor()
    n = 0
    for d in snapshot_dates:
        url = EPSS_URL_TMPL.format(date=d)
        print(f"EPSS: {d}", flush=True)
        raw = _http_get(url)
        text = gzip.decompress(raw).decode("utf-8")
        # First line is a comment with model version; skip until header.
        lines = [ln for ln in text.splitlines() if not ln.startswith("#")]
        reader = csv.DictReader(lines)
        for row in reader:
            cid = row.get("cve")
            if not cid or cid not in allow:
                continue
            try:
                cur.execute(
                    "INSERT OR REPLACE INTO epss VALUES (?,?,?,?)",
                    (cid, d, float(row["epss"]), float(row["percentile"])),
                )
                n += 1
            except Exception:
                pass
        conn.commit()
    print(f"EPSS: ingested {n} score rows", flush=True)
    return n


def main() -> None:
    CLEAN_DB.parent.mkdir(parents=True, exist_ok=True)
    if CLEAN_DB.exists():
        CLEAN_DB.unlink()
    conn = sqlite3.connect(CLEAN_DB)
    init_schema(conn)
    cves = fetch_nvd(conn)
    fetch_kev(conn, cves)
    today = date.today()
    snapshot_dates = [
        (today - timedelta(days=2)).isoformat(),
        "2024-06-01",
        "2024-01-02",  # earliest we sample, gives us a "before KEV add" lookback
    ]
    fetch_epss(conn, cves, snapshot_dates)
    conn.close()
    print(f"OK: clean snapshot at {CLEAN_DB}", flush=True)


if __name__ == "__main__":
    main()
