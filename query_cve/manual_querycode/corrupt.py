"""Corrupt clean/clean.sqlite into the four agent-visible DBs in query_dataset/.

NO date-format corruption anywhere (deliberately). Each non-date corruption is
hash-deterministic so the build is reproducible.

Engines (chosen so each engine matches the data's natural shape):
  vulns_db        sqlite    query_dataset/vulns.db        (cves + cvss_metadata — small embedded registry)
  cpe_db          duckdb    query_dataset/cpe.duckdb      (analytical / columnar / 585k+ rows)
  kev_db          postgres  query_dataset/kev.sql         (structured catalog dump; loaded by seed_dbs.py)
  descriptions_db mongo     query_dataset/descriptions/   (per-CVE document with nested descriptions[] + references[])

Corruption properties applied:

  vulns_db (sqlite):
    - Only the structured registry: cves + cvss_metadata.
    - cvss3_severity column DROPPED.
    - cvss3_base_score column DROPPED. Score moved into a sibling
      cvss_metadata.score_text column, formatted variably as
      "9.8 (CRITICAL)", "score=7.1/10 hi", "5.4-medium-base", etc.
    - ~5% of CVEs have a duplicate row in `cves` with a conflicting
      cvss3_attack_vector value.
    - cve_id format varies per row across both tables in vulns.

  descriptions_db (mongo):
    - One document per CVE: { cve, descriptions: [{lang, value}, ...],
      references: [{url, source}, ...] }
    - Severity word replaced with a cryptic phrase ("Risk-level: 4-of-4" etc.)
      appended to the English description. Literal words critical/high/medium/low
      never appear.
    - English description dropped for a deterministic subset (~20%); only the
      non-English description survives there (no fallback if no other lang exists).
    - cve field uses the canonical CVE-ID format (uppercase "CVE-YYYY-NNNN") —
      cross-DB joins from descriptions to vulns/cpe still require canonicalization.

  cpe_db (duckdb):
    - cpe_matches.criteria uses vendor ALIASES, never the canonical vendor name.
      (e.g. apache -> "ASF", microsoft -> "MSFT-Corp"). vendor_aliases lookup table
      provided so the agent can join through it.
    - vulnerable INT replaced with vulnerable_flag TEXT taking varied truthy/falsy
      tokens ("yes", "y", "V", "affected", "1", ... / "no", "n", "F", "safe", ...).
    - Version moved out of `criteria`/`version_*` columns into a sibling
      cpe_version_details.version_text column with mixed encodings
      ("2.14.1", "2,14,1", "v2_14_1", "build-2014001").
    - cve_id format varies per row.

  kev_db (postgres):
    - vendor_project rewritten via vendor-variant pool (microsoft / "Microsoft Corp"
      / "MSFT" all map to apache canonical "microsoft"). Variants chosen
      deterministically so the same canonical vendor appears under multiple
      surface forms requiring clustering.
    - product column REPLACED with products_csv: a comma-separated list. Real
      single-product rows still get a single value; synthetic multi-product
      rows are injected for queries that test list-splitting.
    - ~5% of KEV rows reference CVEs absent from vulns_db (referential gap).
    - cve_ref format varies per row.


Manifest tables (clean/manifest.sqlite — never agent-visible):
    planted_severity_phrase  (cve_id, severity, phrase_id)
    planted_score_text       (cve_id, canonical_score, score_text, format_id)
    planted_eng_dropped      (cve_id) — CVEs whose English description was deleted
    planted_duplicate        (cve_id, original_attack_vector, duplicate_attack_vector)
    canonical_cpe            (cve_id, canonical_criteria, vendor, product, version)
    canonical_kev_vendor     (cve_id, canonical_vendor, corrupted_vendor)
    canonical_vulnerable     (cve_id, criteria, canonical_vulnerable, flag_text)
    canonical_version_text   (cve_id, criteria, canonical_version, version_text, format_id)
"""
from __future__ import annotations
import hashlib
import json
import shutil
import sqlite3
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
CLEAN_DB = ROOT / "clean" / "clean.sqlite"
MANIFEST_DB = ROOT / "clean" / "manifest.sqlite"
QD = ROOT / "query_dataset"

VULNS_DB = QD / "vulns.db"
CPE_DB = QD / "cpe.duckdb"
KEV_SQL = QD / "kev.sql"
DESC_DUMP = QD / "descriptions"


# ---- helpers ---------------------------------------------------------------

def h(*parts) -> int:
    """Stable, deterministic integer hash of stringified parts."""
    s = "|".join(str(p) for p in parts)
    return int(hashlib.sha1(s.encode()).hexdigest(), 16)


# ---- severity-as-cryptic-prose ---------------------------------------------
# The literal word "critical"/"high"/"medium"/"low" NEVER appears in a planted
# phrase. The agent must learn the mapping from samples (or world knowledge).
# Each severity gets a fixed pool of phrases, one chosen per CVE.

SEVERITY_PHRASES: dict[str, list[str]] = {
    "CRITICAL": [
        "Risk-level: 4-of-4",
        "Threat tier: T4 (top)",
        "Impact band: red-zone",
    ],
    "HIGH": [
        "Risk-level: 3-of-4",
        "Threat tier: T3",
        "Impact band: orange-zone",
    ],
    "MEDIUM": [
        "Risk-level: 2-of-4",
        "Threat tier: T2",
        "Impact band: yellow-zone",
    ],
    "LOW": [
        "Risk-level: 1-of-4",
        "Threat tier: T1",
        "Impact band: green-zone",
    ],
}


def severity_phrase(sev: str, cve_id: str) -> tuple[str, int]:
    sev_u = sev.upper()
    pool = SEVERITY_PHRASES.get(sev_u, [])
    if not pool:
        return "", 0
    pid = h("sev-phrase", cve_id) % len(pool)
    return pool[pid], pid


# ---- CVSS-as-text ----------------------------------------------------------
SCORE_TEXT_FORMATS = [
    lambda score, sev: f"{score:.1f} ({sev.upper()})",
    lambda score, sev: f"score={score:.2f}/10 {sev.lower()[:2]}",
    lambda score, sev: f"{score:.1f}-{sev.lower()}-base",
    lambda score, sev: f"CVSSv3 base = {score:.1f} severity={sev.title()}",
]


def score_text(score: float, sev: str | None, cve_id: str) -> tuple[str, int]:
    if score is None:
        return "", 0
    fid = h("score-fmt", cve_id) % len(SCORE_TEXT_FORMATS)
    sev_safe = sev or "UNKNOWN"
    return SCORE_TEXT_FORMATS[fid](score, sev_safe), fid


# ---- CPE vendor aliasing ---------------------------------------------------
CPE_FORMAT_FNS = [
    lambda alias, p, ver: f"cpe:2.3:a:{alias}:{p}:{ver}:*:*:*:*:*:*:*",
    lambda alias, p, ver: f"{alias}/{p}@{ver}",
    lambda alias, p, ver: f"{alias} {p.replace('_', ' ').title()} {ver}",
]

VENDOR_ALIAS = {
    "apache":   "ASF",
    "microsoft":"MSFT-Corp",
    "google":   "Alphabet",
    "apple":    "Cupertino-Inc",
    "adobe":    "Magenta-Sys",
    "cisco":    "SanJose-Net",
    "oracle":   "Redwood-Sw",
    "ivanti":   "MobileFront",
    "fortinet": "FTNT-Sec",
    "vmware":   "Broadcom-VS",
    "linux":    "Tux-Foundation",
    "redhat":   "RH-Ent",
    "ibm":      "BigBlue",
    "samsung":  "SDC-Korea",
    "intel":    "SantaClara-Si",
}


def alias_for(vendor: str) -> str:
    if not vendor:
        return vendor
    canonical = vendor.lower()
    if canonical in VENDOR_ALIAS:
        return VENDOR_ALIAS[canonical]
    return "vnd_" + hashlib.sha1(canonical.encode()).hexdigest()[:6]


# ---- vulnerable as varied truthy/falsy strings -----------------------------
TRUTHY = ["yes", "y", "true", "1", "V", "affected", "vulnerable", "T"]
FALSY  = ["no",  "n", "false", "0", "F", "safe",     "not_affected", "clean"]


def vuln_flag(canonical: int, cve_id: str, criteria: str) -> str:
    pool = TRUTHY if canonical else FALSY
    return pool[h("vflag", cve_id, criteria) % len(pool)]


# ---- CPE version encoding mix ----------------------------------------------
VERSION_FORMATS = [
    lambda v: v,                                                      # 2.14.1
    lambda v: v.replace(".", ","),                                    # 2,14,1
    lambda v: "v" + v.replace(".", "_"),                              # v2_14_1
    lambda v: "build-" + "".join(p.zfill(3) for p in v.split(".")),   # build-002014001
]


def version_text_for(version: str | None, cve_id: str, criteria: str) -> tuple[str | None, int]:
    if not version or version == "*":
        return version, 0
    fid = h("vfmt", cve_id, criteria) % len(VERSION_FORMATS)
    try:
        return VERSION_FORMATS[fid](version), fid
    except Exception:
        return version, 0


# ---- KEV vendor variants ---------------------------------------------------
VENDOR_VARIANTS = {
    "microsoft": ["microsoft", "Microsoft Corp", "MSFT", "Microsoft Corporation"],
    "apple":     ["apple", "Apple Inc.", "Apple Inc", "AAPL"],
    "google":    ["google", "Google LLC", "Google Inc.", "Alphabet (Google)"],
    "apache":    ["apache", "The Apache Software Foundation", "Apache Software Foundation", "ASF"],
    "adobe":     ["adobe", "Adobe Inc.", "Adobe Systems"],
    "cisco":     ["cisco", "Cisco Systems", "Cisco Systems, Inc."],
    "oracle":    ["oracle", "Oracle Corporation", "Oracle Corp"],
    "ivanti":    ["ivanti", "Ivanti Inc.", "Ivanti Software"],
    "fortinet":  ["fortinet", "Fortinet Inc.", "Fortinet, Inc."],
    "vmware":    ["vmware", "VMware Inc.", "VMware, LLC", "Broadcom (VMware)"],
}


def vendor_variant(canonical: str, salt: str) -> str:
    pool = VENDOR_VARIANTS.get(canonical.lower())
    if not pool:
        choice = h(canonical, salt) % 3
        return [canonical, canonical.lower(), canonical + " Inc."][choice]
    return pool[h(canonical, salt) % len(pool)]


# ---- CVE-ID format mixing --------------------------------------------------
def reformat_cve_id(cve_id: str, salt: str) -> str:
    fid = h("cveid", salt) % 3
    if fid == 0:
        return cve_id
    if fid == 1:
        return cve_id.lower()
    return cve_id.removeprefix("CVE-").removeprefix("cve-")


# ---- pipeline --------------------------------------------------------------

def init_manifest(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    DROP TABLE IF EXISTS planted_severity_phrase;
    DROP TABLE IF EXISTS planted_score_text;
    DROP TABLE IF EXISTS planted_eng_dropped;
    DROP TABLE IF EXISTS planted_duplicate;
    DROP TABLE IF EXISTS canonical_cpe;
    DROP TABLE IF EXISTS canonical_kev_vendor;
    DROP TABLE IF EXISTS canonical_vulnerable;
    DROP TABLE IF EXISTS canonical_version_text;

    CREATE TABLE planted_severity_phrase (
      cve_id TEXT PRIMARY KEY, severity TEXT, phrase_id INTEGER, phrase TEXT
    );
    CREATE TABLE planted_score_text (
      cve_id TEXT PRIMARY KEY, canonical_score REAL, score_text TEXT, format_id INTEGER
    );
    CREATE TABLE planted_eng_dropped (cve_id TEXT PRIMARY KEY);
    CREATE TABLE planted_duplicate (
      cve_id TEXT PRIMARY KEY,
      original_attack_vector TEXT,
      duplicate_attack_vector TEXT
    );
    CREATE TABLE canonical_cpe (
      cve_id TEXT, canonical_criteria TEXT, vendor TEXT, product TEXT,
      version TEXT, format_id INTEGER
    );
    CREATE TABLE canonical_kev_vendor (
      cve_id TEXT PRIMARY KEY, canonical_vendor TEXT, corrupted_vendor TEXT
    );
    CREATE TABLE canonical_vulnerable (
      cve_id TEXT, criteria TEXT, canonical_vulnerable INTEGER, flag_text TEXT
    );
    CREATE TABLE canonical_version_text (
      cve_id TEXT, criteria TEXT, canonical_version TEXT, version_text TEXT, format_id INTEGER
    );
    """)
    conn.commit()


# Selectors driven by hash-determinism --------------------------------------

DROP_ENGLISH_RATE = 20   # 1 in N CVEs gets its English description dropped
DUPLICATE_RATE    = 20   # 1 in N CVEs gets a duplicate row with conflicting AV


def should_drop_english(cve_id: str) -> bool:
    return h("drop-eng", cve_id) % DROP_ENGLISH_RATE == 0


def should_duplicate(cve_id: str) -> bool:
    return h("dup", cve_id) % DUPLICATE_RATE == 0


def conflicting_attack_vector(orig: str | None, cve_id: str) -> str:
    """Pick a *different* attack vector for the duplicate row."""
    pool = ["NETWORK", "ADJACENT_NETWORK", "LOCAL", "PHYSICAL"]
    seed = h("dup-av", cve_id)
    for off in range(len(pool)):
        candidate = pool[(seed + off) % len(pool)]
        if candidate != (orig or ""):
            return candidate
    return pool[0]


# ---- builders --------------------------------------------------------------

def _load_planted_narratives(manifest: sqlite3.Connection):
    desc = {r[0]: r[1] for r in manifest.execute(
        "SELECT cve_id, narrative FROM planted_narrative_desc"
    )} if manifest.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='planted_narrative_desc'"
    ).fetchone() else {}
    score = {r[0]: r[1] for r in manifest.execute(
        "SELECT cve_id, narrative FROM planted_narrative_score"
    )} if manifest.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='planted_narrative_score'"
    ).fetchone() else {}
    return desc, score


def build_vulns(clean: sqlite3.Connection, manifest: sqlite3.Connection) -> None:
    """vulns.db now holds only the structured registry: cves + cvss_metadata.
    Free-text descriptions and references move to descriptions_db (Mongo)."""
    if VULNS_DB.exists():
        VULNS_DB.unlink()
    out = sqlite3.connect(VULNS_DB)
    out.executescript("""
    CREATE TABLE cves (
      cve_id TEXT,
      published TEXT,
      last_modified TEXT,
      vuln_status TEXT,
      cvss3_attack_vector TEXT
    );
    CREATE TABLE cvss_metadata (
      cve_id TEXT, score_text TEXT
    );
    CREATE INDEX idx_cvss_cve ON cvss_metadata(cve_id);
    """)
    cur = clean.cursor()
    mcur = manifest.cursor()

    sev_by_cve: dict[str, str] = dict(cur.execute(
        "SELECT cve_id, cvss3_severity FROM cves WHERE cvss3_severity IS NOT NULL"
    ).fetchall())
    score_by_cve: dict[str, float] = dict(cur.execute(
        "SELECT cve_id, cvss3_base_score FROM cves WHERE cvss3_base_score IS NOT NULL"
    ).fetchall())
    narr_desc_by_cve, narr_score_by_cve = _load_planted_narratives(manifest)

    n_dup = 0
    for cve_id, published, last_modified, vuln_status, av in cur.execute(
        "SELECT cve_id, published, last_modified, vuln_status, "
        "cvss3_attack_vector FROM cves"
    ):
        cve_corrupted = reformat_cve_id(cve_id, "vulns-" + cve_id)
        out.execute(
            "INSERT INTO cves VALUES (?,?,?,?,?)",
            (cve_corrupted, published, last_modified, vuln_status, av),
        )
        if should_duplicate(cve_id):
            dup_av = conflicting_attack_vector(av, cve_id)
            dup_corrupted = reformat_cve_id(cve_id, "vulns-dup-" + cve_id)
            out.execute(
                "INSERT INTO cves VALUES (?,?,?,?,?)",
                (dup_corrupted, published, last_modified, vuln_status, dup_av),
            )
            mcur.execute(
                "INSERT OR REPLACE INTO planted_duplicate VALUES (?,?,?)",
                (cve_id, av, dup_av),
            )
            n_dup += 1

    n_score = 0
    n_narr_score = 0
    for cve_id, score in score_by_cve.items():
        sev = sev_by_cve.get(cve_id)
        # Prefer per-row LLM-generated narrative if available; fall back to
        # template otherwise.
        narr = narr_score_by_cve.get(cve_id)
        if narr:
            st = narr
            fid = -1  # signals narrative origin
            n_narr_score += 1
        else:
            st, fid = score_text(score, sev, cve_id)
        if not st:
            continue
        cve_corrupted = reformat_cve_id(cve_id, "vulns-" + cve_id)
        out.execute("INSERT INTO cvss_metadata VALUES (?,?)", (cve_corrupted, st))
        mcur.execute(
            "INSERT OR REPLACE INTO planted_score_text VALUES (?,?,?,?)",
            (cve_id, score, st, fid),
        )
        n_score += 1

    out.commit()
    out.close()
    manifest.commit()
    print(
        f"vulns.db: built ({n_score} cvss texts, of which {n_narr_score} are "
        f"LLM narratives, {n_dup} duplicate rows)"
    )


def build_descriptions(clean: sqlite3.Connection, manifest: sqlite3.Connection) -> None:
    """One Mongo document per CVE with nested descriptions[] and references[].
    English-dropping + severity-phrase planting happen here."""
    if DESC_DUMP.exists():
        shutil.rmtree(DESC_DUMP)
    DESC_DUMP.mkdir(parents=True, exist_ok=True)

    cur = clean.cursor()
    mcur = manifest.cursor()

    sev_by_cve: dict[str, str] = dict(cur.execute(
        "SELECT cve_id, cvss3_severity FROM cves WHERE cvss3_severity IS NOT NULL"
    ).fetchall())
    narr_desc_by_cve, _ = _load_planted_narratives(manifest)

    descs_by_cve: dict[str, list[dict]] = {}
    n_planted_sev = 0
    n_narr_sev = 0
    n_eng_dropped = 0
    for cve_id, lang, value in cur.execute(
        "SELECT cve_id, lang, value FROM cve_descriptions"
    ):
        if lang == "en" and should_drop_english(cve_id):
            mcur.execute(
                "INSERT OR REPLACE INTO planted_eng_dropped VALUES (?)",
                (cve_id,),
            )
            n_eng_dropped += 1
            continue
        sev = sev_by_cve.get(cve_id)
        if lang == "en" and cve_id in narr_desc_by_cve:
            # LLM narrative replaces the English description entirely; severity
            # is implied via prose, not via a tagline.
            value = narr_desc_by_cve[cve_id]
            n_narr_sev += 1
        elif sev and lang == "en":
            phrase, pid = severity_phrase(sev, cve_id)
            value = (value or "") + " " + phrase
            mcur.execute(
                "INSERT OR REPLACE INTO planted_severity_phrase VALUES (?,?,?,?)",
                (cve_id, sev, pid, phrase),
            )
            n_planted_sev += 1
        descs_by_cve.setdefault(cve_id, []).append({"lang": lang, "value": value})

    refs_by_cve: dict[str, list[dict]] = {}
    for cve_id, url, source in cur.execute(
        "SELECT cve_id, url, source FROM cve_references"
    ):
        refs_by_cve.setdefault(cve_id, []).append({"url": url, "source": source})

    cve_universe = set(descs_by_cve) | set(refs_by_cve)
    docs = [
        {
            "cve": cve_id,
            "descriptions": descs_by_cve.get(cve_id, []),
            "references": refs_by_cve.get(cve_id, []),
        }
        for cve_id in sorted(cve_universe)
    ]

    from bson import encode as bson_encode
    coll_dir = DESC_DUMP / "cve_descriptions"
    coll_dir.mkdir(parents=True, exist_ok=True)
    bson_path = coll_dir / "cve_documents.bson"
    with bson_path.open("wb") as f:
        for d in docs:
            f.write(bson_encode(d))
    meta = {
        "options": {},
        "indexes": [
            {"v": 2, "key": {"_id": 1}, "name": "_id_"},
            {"v": 2, "key": {"cve": 1}, "name": "cve_1"},
        ],
        "uuid": "",
        "collectionName": "cve_documents",
        "type": "collection",
    }
    (coll_dir / "cve_documents.metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    manifest.commit()
    print(
        f"descriptions/: built ({len(docs)} cve_documents, "
        f"{n_planted_sev} severity phrases, {n_narr_sev} LLM severity narratives, "
        f"{n_eng_dropped} english-dropped)"
    )


def build_cpe(clean: sqlite3.Connection, manifest: sqlite3.Connection) -> None:
    if CPE_DB.exists():
        CPE_DB.unlink()
    con = duckdb.connect(str(CPE_DB))
    con.execute("""
        CREATE TABLE cpe_matches (
          cve_id TEXT,
          criteria TEXT,
          vulnerable_flag TEXT
        );
        CREATE TABLE vendor_aliases (
          alias TEXT PRIMARY KEY,
          canonical_vendor TEXT
        );
        CREATE TABLE cpe_version_details (
          cve_id TEXT,
          criteria TEXT,
          version_text TEXT,
          version_start_inc TEXT,
          version_start_exc TEXT,
          version_end_inc TEXT,
          version_end_exc TEXT
        );
    """)
    cur = clean.cursor()
    mcur = manifest.cursor()
    rows = cur.execute(
        "SELECT cve_id, cpe_criteria, vendor, product, version, "
        "version_start_inc, version_start_exc, version_end_inc, version_end_exc, vulnerable "
        "FROM cpe_matches"
    ).fetchall()

    alias_map: dict[str, str] = {}
    match_rows = []
    version_rows = []
    for cve_id, crit, vendor, product, version, vsi, vse, vei, vee, vuln in rows:
        if not vendor or not product:
            corrupted_crit = crit
            fid = 0
        else:
            alias = alias_for(vendor)
            alias_map[alias] = vendor.lower()
            ver = version if version and version != "*" else "0"
            fid = h("cpe", cve_id, crit) % len(CPE_FORMAT_FNS)
            corrupted_crit = CPE_FORMAT_FNS[fid](alias, product, ver)
        corrupted_cve = reformat_cve_id(cve_id, "cpe-row-" + str(h(crit) % 1_000_000))
        flag_text = vuln_flag(vuln, cve_id, crit)
        match_rows.append((corrupted_cve, corrupted_crit, flag_text))

        v_text, v_fid = version_text_for(version, cve_id, crit)
        version_rows.append((corrupted_cve, corrupted_crit, v_text, vsi, vse, vei, vee))

        mcur.execute(
            "INSERT INTO canonical_cpe VALUES (?,?,?,?,?,?)",
            (cve_id, crit, vendor, product, version, fid),
        )
        mcur.execute(
            "INSERT INTO canonical_vulnerable VALUES (?,?,?,?)",
            (cve_id, crit, vuln, flag_text),
        )
        mcur.execute(
            "INSERT INTO canonical_version_text VALUES (?,?,?,?,?)",
            (cve_id, crit, version, v_text, v_fid),
        )

    con.executemany("INSERT INTO cpe_matches VALUES (?,?,?)", match_rows)
    con.executemany(
        "INSERT INTO vendor_aliases VALUES (?,?)",
        sorted(alias_map.items()),
    )
    con.executemany(
        "INSERT INTO cpe_version_details VALUES (?,?,?,?,?,?,?)",
        version_rows,
    )
    con.close()
    manifest.commit()
    print(
        f"cpe.duckdb: built ({len(match_rows)} cpe_match rows, "
        f"{len(alias_map)} vendor_aliases, {len(version_rows)} version_detail rows)"
    )


def build_kev(clean: sqlite3.Connection, manifest: sqlite3.Connection) -> None:
    if KEV_SQL.exists():
        KEV_SQL.unlink()
    cur = clean.cursor()
    mcur = manifest.cursor()
    rows = cur.execute(
        "SELECT cve_id, vendor_project, product, vulnerability_name, date_added, "
        "short_description, required_action, due_date, known_ransomware_use, notes FROM kev"
    ).fetchall()

    def pgesc(s):
        if s is None:
            return "NULL"
        return "'" + str(s).replace("'", "''") + "'"

    lines = [
        "CREATE TABLE kev_entries (",
        "  cve_ref TEXT,",
        "  vendor_project TEXT,",
        "  products_csv TEXT,",
        "  vulnerability_name TEXT,",
        "  date_added TEXT,",
        "  short_description TEXT,",
        "  required_action TEXT,",
        "  due_date TEXT,",
        "  known_ransomware_use TEXT,",
        "  notes TEXT",
        ");",
    ]
    for (cve_id, vendor, product, vname, dadded, sdesc, raction, ddue, krw, notes) in rows:
        cv = vendor or ""
        corrupted_vendor = vendor_variant(cv, cve_id) if cv else cv
        cve_ref = reformat_cve_id(cve_id, "kev-" + cve_id)

        # synthesize a packed list when product contains a "/" (real KEV uses
        # this as a separator for sibling products); otherwise leave singleton.
        if product and "/" in product:
            products_csv = ",".join(p.strip() for p in product.split("/"))
        else:
            products_csv = product

        lines.append(
            "INSERT INTO kev_entries VALUES (" + ", ".join([
                pgesc(cve_ref),
                pgesc(corrupted_vendor),
                pgesc(products_csv),
                pgesc(vname),
                pgesc(dadded),         # untouched (no date corruption)
                pgesc(sdesc),
                pgesc(raction),
                pgesc(ddue),           # untouched
                pgesc(krw),
                pgesc(notes),
            ]) + ");"
        )
        mcur.execute(
            "INSERT OR REPLACE INTO canonical_kev_vendor VALUES (?,?,?)",
            (cve_id, vendor, corrupted_vendor),
        )

    KEV_SQL.write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest.commit()
    print(f"kev.sql: built ({len(rows)} kev_entries rows)")


def main() -> None:
    if not CLEAN_DB.exists():
        raise SystemExit(f"missing clean snapshot: {CLEAN_DB} — run fetch_clean.py first")
    QD.mkdir(parents=True, exist_ok=True)
    # Don't unlink the manifest — it may hold LLM narrative outputs from
    # llm_corrupt.py that are expensive to regenerate. init_manifest drops
    # only the deterministic-corruption tables.
    clean = sqlite3.connect(CLEAN_DB)
    manifest = sqlite3.connect(MANIFEST_DB)
    init_manifest(manifest)
    build_vulns(clean, manifest)
    build_cpe(clean, manifest)
    build_kev(clean, manifest)
    build_descriptions(clean, manifest)
    clean.close()
    manifest.close()
    print("OK")


if __name__ == "__main__":
    main()
