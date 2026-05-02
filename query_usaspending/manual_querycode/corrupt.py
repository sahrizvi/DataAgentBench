"""Corrupt clean/clean.sqlite into 4 agent-visible DBs in query_dataset/.

Engines (chosen so each engine matches the data's natural shape):
  contracts_db    postgres  query_dataset/contracts.sql       (transactional fact dump)
  recipients_db   sqlite    query_dataset/recipients.db       (small entity registry)
  agencies_db     duckdb    query_dataset/agencies.duckdb     (analytical reference)
  descriptions_db mongo     query_dataset/descriptions/       (nested per-contract docs)

NO date-format corruption. Each non-date corruption is hash-deterministic.

Layers applied:

  contracts_db (postgres):
    - amount column DROPPED (numeric). Replaced with amount_text TEXT in a
      sibling contract_amounts table — formats vary: "$1,500,000.00", "1.5M",
      "1500000", "1,500,000 USD".
    - award_id format varies per row: "HT940216C0001", "ht940216c0001",
      "HT940216-C-0001".
    - awarding_agency replaced with vendor-style surface variants
      (e.g. Department of Defense -> "DoD", "DOD", "Dept of Defense",
       "Department of Defense (DOD)").
    - naics_code reformatted: "336411" / "naics-336411" / "33-6411".

  recipients_db (sqlite):
    - name column has multiple surface forms for the SAME canonical entity
      (suffix variants: "Inc", "Inc.", "Incorporated", "Corp"/"Corporation",
       trailing/leading whitespace, hyphenation). Real data already has some
       of this; we layer on more.
    - uei format varies: "ZE6ZM6NKSV43" / "uei:ze6zm6nksv43" / "ze6zm6nksv43-uei".
    - state stored as varied surface form ("California" / "CA" / "Calif.").

  agencies_db (duckdb):
    - agency name has surface-form variants (same as in contracts).
    - canonical_to_alias lookup table that the agent can use to resolve
      surface variants to canonical names.
    - naics table preserves the 2-digit sector hierarchy.

  descriptions_db (mongo):
    - One document per award_id with embedded {description, language}.
    - English description dropped for ~10% of contracts; only Spanish or
      French paraphrase remains for those.

Manifest tables (clean/manifest.sqlite — never agent-visible):
    canonical_award_id    (canonical_award_id, corrupted_award_id)
    canonical_recipient   (canonical_uei, canonical_name)
    canonical_agency      (canonical_agency, corrupted_surface)
    canonical_naics       (canonical_code, corrupted_code)
    canonical_amount      (canonical_award_id, canonical_amount, amount_text, format_id)
    planted_eng_dropped   (award_id)
    planted_duplicate     (canonical_award_id, original_amount, duplicate_amount)
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

CONTRACTS_SQL = QD / "contracts.sql"
RECIPIENTS_DB = QD / "recipients.db"
AGENCIES_DB   = QD / "agencies.duckdb"
DESC_DUMP     = QD / "descriptions"


def h(*parts) -> int:
    s = "|".join(str(p) for p in parts)
    return int(hashlib.sha1(s.encode()).hexdigest(), 16)


# ---- amount-as-text formats -----------------------------------------------
def _scaled(n: float, suffix: str, decimals: int = 1) -> str:
    return f"{n:,.{decimals}f}{suffix}"

AMOUNT_FORMATS = [
    lambda x: f"${x:,.2f}",
    lambda x: f"{x:,.2f} USD",
    lambda x: f"{x:.0f}",
    lambda x: (
        _scaled(x / 1_000_000_000, "B")
        if x >= 1_000_000_000 else _scaled(x / 1_000_000, "M")
        if x >= 1_000_000 else _scaled(x / 1_000, "K")
    ),
]


def amount_text(value: float, salt: str) -> tuple[str, int]:
    if value is None:
        return "", 0
    fid = h("amt", salt) % len(AMOUNT_FORMATS)
    return AMOUNT_FORMATS[fid](value), fid


# ---- NAICS code formatting -------------------------------------------------
def naics_format(code: str, salt: str) -> str:
    if not code:
        return code
    fid = h("naics", salt) % 3
    if fid == 0:
        return code
    if fid == 1:
        return f"naics-{code}"
    return f"{code[:2]}-{code[2:]}" if len(code) >= 4 else code


# ---- Agency name surface forms --------------------------------------------
AGENCY_VARIANTS = {
    "Department of Defense": ["Department of Defense", "DoD", "DOD", "Dept of Defense", "Department of Defense (DOD)", "Defense Department"],
    "Department of Energy": ["Department of Energy", "DOE", "Dept of Energy", "DoE"],
    "Department of Health and Human Services": ["Department of Health and Human Services", "HHS", "Dept HHS", "Health and Human Services"],
    "Department of Veterans Affairs": ["Department of Veterans Affairs", "VA", "Dept of Veterans Affairs"],
    "Department of Homeland Security": ["Department of Homeland Security", "DHS", "Dept Homeland Security"],
    "Department of State": ["Department of State", "State Dept", "Dept of State", "DOS"],
    "National Aeronautics and Space Administration": ["NASA", "National Aeronautics and Space Administration", "Nat'l Aeronautics & Space Administration"],
    "General Services Administration": ["General Services Administration", "GSA", "Gen Services Admin"],
    "Department of Justice": ["Department of Justice", "DOJ", "DoJ", "Justice Dept"],
    "Department of Transportation": ["Department of Transportation", "DOT", "DoT", "Transportation Dept"],
    "Department of the Interior": ["Department of the Interior", "DOI", "Interior Dept"],
    "Department of Agriculture": ["Department of Agriculture", "USDA", "Agriculture Dept"],
    "Department of Commerce": ["Department of Commerce", "DOC", "Commerce Dept"],
    "Department of the Treasury": ["Department of the Treasury", "Treasury", "Treasury Dept"],
    "Environmental Protection Agency": ["Environmental Protection Agency", "EPA"],
    "Department of Education": ["Department of Education", "ED", "Education Dept"],
    "Department of Labor": ["Department of Labor", "DOL", "Labor Dept"],
    "Department of Housing and Urban Development": ["Department of Housing and Urban Development", "HUD"],
    "Social Security Administration": ["Social Security Administration", "SSA"],
}


def agency_variant(canonical: str, salt: str) -> str:
    pool = AGENCY_VARIANTS.get(canonical)
    if not pool:
        return canonical
    return pool[h("ag", salt) % len(pool)]


# ---- recipient name fuzzification -----------------------------------------
SUFFIX_VARIANTS = [
    ("INC", ["INC", "INC.", "INCORPORATED", "Inc", "Inc.", "Incorporated"]),
    ("CORP", ["CORP", "CORP.", "CORPORATION", "Corp", "Corp.", "Corporation"]),
    ("LLC", ["LLC", "LLC.", "L.L.C.", "L.L.C", "Llc"]),
    ("CO", ["CO", "CO.", "COMPANY", "Co.", "Company"]),
    ("LTD", ["LTD", "LTD.", "Limited", "Ltd."]),
]


def fuzz_recipient_name(name: str, salt: str) -> str:
    if not name:
        return name
    n = name.strip()
    # Try matching one of the corporate suffixes and swap to a variant
    upper = n.upper()
    for canonical_suffix, variants in SUFFIX_VARIANTS:
        for v in variants:
            sfx = " " + v
            if upper.endswith(sfx.upper()):
                # strip and append a chosen variant
                stem = n[: len(n) - len(sfx)]
                pick = variants[h("rname", salt) % len(variants)]
                return stem + " " + pick
    # No suffix; apply small noise: title-case half the time, keep as-is otherwise
    if h("rname-case", salt) % 2 == 0:
        return n
    return n.title()


# ---- UEI format mixing ----------------------------------------------------
def uei_format(uei: str, salt: str) -> str:
    if not uei:
        return uei
    fid = h("uei", salt) % 3
    if fid == 0:
        return uei
    if fid == 1:
        return f"uei:{uei.lower()}"
    return f"{uei.lower()}-uei"


# ---- Award ID format ------------------------------------------------------
def award_id_format(aid: str, salt: str) -> str:
    if not aid:
        return aid
    fid = h("aid", salt) % 3
    if fid == 0:
        return aid
    if fid == 1:
        return aid.lower()
    # add a hyphen between letter run and numbers if pattern matches
    import re
    m = re.match(r"^([A-Z0-9]+?)([A-Z])(\d+)$", aid.upper())
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return aid


# ---- State name variants --------------------------------------------------
STATE_VARIANTS = {
    "CA": ["CA", "California", "Calif.", "Calif"],
    "NY": ["NY", "New York", "N.Y."],
    "TX": ["TX", "Texas", "Tex."],
    "VA": ["VA", "Virginia", "Va."],
    "DC": ["DC", "District of Columbia", "D.C."],
    "MA": ["MA", "Massachusetts", "Mass."],
    "MD": ["MD", "Maryland", "Md."],
    "FL": ["FL", "Florida", "Fla."],
    "WA": ["WA", "Washington", "Wash."],
    "PA": ["PA", "Pennsylvania", "Penn.", "Penna."],
    "OH": ["OH", "Ohio"],
    "IL": ["IL", "Illinois", "Ill."],
    "MI": ["MI", "Michigan", "Mich."],
    "AZ": ["AZ", "Arizona", "Ariz."],
    "GA": ["GA", "Georgia", "Ga."],
    "NJ": ["NJ", "New Jersey", "N.J."],
    "CO": ["CO", "Colorado", "Colo."],
    "MO": ["MO", "Missouri", "Mo."],
}


def state_variant(s: str, salt: str) -> str:
    if not s:
        return s
    pool = STATE_VARIANTS.get(s)
    if not pool:
        return s
    return pool[h("st", salt) % len(pool)]


# ---- duplicate / language drop selectors ----------------------------------
DROP_ENGLISH_RATE = 10
DUPLICATE_RATE    = 30


def should_drop_english(award_id: str) -> bool:
    return h("drop-eng", award_id) % DROP_ENGLISH_RATE == 0


def should_duplicate(award_id: str) -> bool:
    return h("dup", award_id) % DUPLICATE_RATE == 0


def conflicting_amount(orig: float, salt: str) -> float:
    """Multiply or divide the amount by a deterministic scaling factor."""
    factor = [0.5, 1.5, 2.0, 0.75][h("dup-amt", salt) % 4]
    return round(orig * factor, 2)


# ---- pipeline -------------------------------------------------------------

def init_manifest(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    DROP TABLE IF EXISTS canonical_award_id;
    DROP TABLE IF EXISTS canonical_recipient;
    DROP TABLE IF EXISTS canonical_agency;
    DROP TABLE IF EXISTS canonical_naics;
    DROP TABLE IF EXISTS canonical_amount;
    DROP TABLE IF EXISTS planted_eng_dropped;
    DROP TABLE IF EXISTS planted_duplicate;

    CREATE TABLE canonical_award_id (
      canonical_award_id TEXT PRIMARY KEY, corrupted_award_id TEXT
    );
    CREATE TABLE canonical_recipient (
      canonical_uei TEXT PRIMARY KEY, canonical_name TEXT
    );
    CREATE TABLE canonical_agency (
      award_id TEXT, canonical_agency TEXT, corrupted_surface TEXT
    );
    CREATE TABLE canonical_naics (
      canonical_code TEXT PRIMARY KEY, corrupted_code TEXT
    );
    CREATE TABLE canonical_amount (
      canonical_award_id TEXT PRIMARY KEY,
      canonical_amount REAL,
      amount_text TEXT,
      format_id INTEGER
    );
    CREATE TABLE planted_eng_dropped (award_id TEXT PRIMARY KEY);
    CREATE TABLE planted_duplicate (
      canonical_award_id TEXT PRIMARY KEY,
      original_amount REAL,
      duplicate_amount REAL
    );
    """)
    conn.commit()


def pgesc(s):
    if s is None:
        return "NULL"
    s = str(s).replace("'", "''")
    return "'" + s + "'"


def pgnum(x):
    if x is None:
        return "NULL"
    return f"{x:.2f}"


def _load_planted_amounts(manifest: sqlite3.Connection) -> dict[str, str]:
    if manifest.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='planted_narrative_amount'"
    ).fetchone():
        return {r[0]: r[1] for r in manifest.execute(
            "SELECT canonical_award_id, narrative FROM planted_narrative_amount"
        )}
    return {}


def build_contracts(clean: sqlite3.Connection, manifest: sqlite3.Connection) -> None:
    if CONTRACTS_SQL.exists():
        CONTRACTS_SQL.unlink()
    cur = clean.cursor()
    mcur = manifest.cursor()
    rows = cur.execute("""
        SELECT award_id, generated_internal_id, recipient_name, recipient_uei,
               recipient_state, awarding_agency, awarding_sub_agency,
               funding_agency, amount, total_outlays, start_date, end_date,
               naics_code, naics_description, psc_code, psc_description,
               award_type
        FROM contracts
    """).fetchall()

    lines = [
        "CREATE TABLE contracts (",
        "  award_id TEXT,",
        "  generated_internal_id TEXT,",
        "  recipient_uei TEXT,",
        "  awarding_agency TEXT,",
        "  awarding_sub_agency TEXT,",
        "  funding_agency TEXT,",
        "  start_date TEXT,",
        "  end_date TEXT,",
        "  naics_code TEXT,",
        "  psc_code TEXT,",
        "  award_type TEXT",
        ");",
        "CREATE TABLE contract_amounts (",
        "  award_id TEXT,",
        "  amount_text TEXT",
        ");",
    ]

    narr_amount = _load_planted_amounts(manifest)
    n_dup = 0
    n_narr = 0
    for r in rows:
        (award_id, gen_id, rname, ruei, rstate, agency, sub_agency, fund_agency,
         amt, outlays, sd, ed, naics, naics_desc, psc, psc_desc, atype) = r
        # Corrupt ids/values
        a_corr = award_id_format(award_id, award_id) if award_id else None
        uei_corr = uei_format(ruei, ruei or "")
        agency_corr = agency_variant(agency, award_id or "")
        sub_corr = agency_variant(sub_agency or "", award_id or "")
        fund_corr = agency_variant(fund_agency or "", award_id or "")
        naics_corr = naics_format(naics, award_id or "")

        lines.append(
            "INSERT INTO contracts VALUES (" + ", ".join([
                pgesc(a_corr), pgesc(gen_id), pgesc(uei_corr),
                pgesc(agency_corr), pgesc(sub_corr), pgesc(fund_corr),
                pgesc(sd), pgesc(ed),
                pgesc(naics_corr), pgesc(psc), pgesc(atype),
            ]) + ");"
        )
        # amount in sibling table as text — prefer LLM narrative if available
        if amt is not None:
            if award_id in narr_amount:
                atext = narr_amount[award_id]
                fid = -1  # signals narrative origin
                n_narr += 1
            else:
                atext, fid = amount_text(amt, award_id or "")
            lines.append(
                f"INSERT INTO contract_amounts VALUES ({pgesc(a_corr)}, {pgesc(atext)});"
            )
            mcur.execute(
                "INSERT OR REPLACE INTO canonical_amount VALUES (?,?,?,?)",
                (award_id, amt, atext, fid),
            )
        # duplicate row with conflicting amount
        if should_duplicate(award_id or "") and amt is not None:
            dup_amt = conflicting_amount(amt, award_id or "")
            dup_atext, _ = amount_text(dup_amt, (award_id or "") + "-dup")
            lines.append(
                f"INSERT INTO contract_amounts VALUES ({pgesc(a_corr)}, {pgesc(dup_atext)});"
            )
            mcur.execute(
                "INSERT OR REPLACE INTO planted_duplicate VALUES (?,?,?)",
                (award_id, amt, dup_amt),
            )
            n_dup += 1

        mcur.execute(
            "INSERT OR REPLACE INTO canonical_award_id VALUES (?,?)",
            (award_id, a_corr),
        )
        if agency:
            mcur.execute(
                "INSERT INTO canonical_agency VALUES (?,?,?)",
                (award_id, agency, agency_corr),
            )

    CONTRACTS_SQL.write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest.commit()
    print(
        f"contracts.sql: built ({len(rows)} rows, {n_narr} LLM amount narratives, "
        f"{n_dup} duplicate-amount injections)"
    )


def build_recipients(clean: sqlite3.Connection, manifest: sqlite3.Connection) -> None:
    if RECIPIENTS_DB.exists():
        RECIPIENTS_DB.unlink()
    out = sqlite3.connect(RECIPIENTS_DB)
    out.execute("""
        CREATE TABLE recipients (
          uei TEXT,
          name TEXT,
          state TEXT,
          n_contracts INTEGER,
          total_amount_text TEXT
        );
    """)
    cur = clean.cursor()
    mcur = manifest.cursor()
    rows = cur.execute(
        "SELECT uei, name, state, n_contracts, total_amount FROM recipients"
    ).fetchall()
    for uei, name, state, ncon, total in rows:
        uei_corr = uei_format(uei, uei or "")
        name_corr = fuzz_recipient_name(name or "", uei or "")
        state_corr = state_variant(state, uei or "")
        total_text, _ = amount_text(total or 0, uei or "")
        out.execute(
            "INSERT INTO recipients VALUES (?,?,?,?,?)",
            (uei_corr, name_corr, state_corr, ncon, total_text),
        )
        mcur.execute(
            "INSERT OR REPLACE INTO canonical_recipient VALUES (?,?)",
            (uei, name),
        )
    out.commit()
    out.close()
    manifest.commit()
    print(f"recipients.db: built ({len(rows)} rows)")


def build_agencies(clean: sqlite3.Connection, manifest: sqlite3.Connection) -> None:
    if AGENCIES_DB.exists():
        AGENCIES_DB.unlink()
    con = duckdb.connect(str(AGENCIES_DB))
    con.execute("""
        CREATE TABLE agencies (
          name TEXT,
          n_contracts INTEGER,
          total_amount_text TEXT
        );
        CREATE TABLE agency_aliases (
          surface_form TEXT PRIMARY KEY,
          canonical_name TEXT
        );
        CREATE TABLE naics_sectors (
          code TEXT,
          description TEXT,
          sector TEXT
        );
    """)
    cur = clean.cursor()
    mcur = manifest.cursor()
    rows = cur.execute(
        "SELECT name, n_contracts, total_amount FROM agencies"
    ).fetchall()
    agency_rows = []
    alias_pairs = set()
    for name, ncon, total in rows:
        # Use canonical for the row name (so it appears in agencies table as canonical),
        # but populate agency_aliases with all variants known to map to canonical.
        agency_rows.append((name, ncon, amount_text(total or 0, name)[0]))
        for v in AGENCY_VARIANTS.get(name, [name]):
            alias_pairs.add((v, name))
    con.executemany("INSERT INTO agencies VALUES (?,?,?)", agency_rows)
    con.executemany("INSERT INTO agency_aliases VALUES (?,?)", sorted(alias_pairs))

    naics_rows = []
    for r in cur.execute("SELECT code, description, sector FROM naics"):
        # corrupt the code in the same way as in contracts so a JOIN on
        # contracts.naics_code = naics_sectors.code matches.
        # Actually, let's leave canonical here so the lookup is the
        # canonical-code source-of-truth; the agent must canonicalize the
        # corrupted contracts.naics_code to match.
        naics_rows.append((r[0], r[1], r[2]))
        mcur.execute(
            "INSERT OR REPLACE INTO canonical_naics VALUES (?,?)",
            (r[0], naics_format(r[0], "naics-row-" + r[0])),
        )
    con.executemany("INSERT INTO naics_sectors VALUES (?,?,?)", naics_rows)
    con.close()
    manifest.commit()
    print(
        f"agencies.duckdb: built ({len(agency_rows)} agencies, "
        f"{len(alias_pairs)} aliases, {len(naics_rows)} naics rows)"
    )


def build_descriptions(clean: sqlite3.Connection, manifest: sqlite3.Connection) -> None:
    if DESC_DUMP.exists():
        shutil.rmtree(DESC_DUMP)
    DESC_DUMP.mkdir(parents=True, exist_ok=True)

    cur = clean.cursor()
    mcur = manifest.cursor()
    docs = []
    n_eng_dropped = 0
    for award_id, desc in cur.execute(
        "SELECT award_id, description FROM contracts"
    ):
        a_corr = award_id_format(award_id or "", award_id or "")
        descs = []
        if desc:
            if should_drop_english(award_id or ""):
                # planted: drop English; replace with Spanish placeholder paraphrase
                descs.append({"language": "es", "value": "[contrato federal] " + (desc[:200] if desc else "")})
                mcur.execute(
                    "INSERT OR REPLACE INTO planted_eng_dropped VALUES (?)",
                    (award_id,),
                )
                n_eng_dropped += 1
            else:
                descs.append({"language": "en", "value": desc})
        docs.append({"award_id": a_corr, "descriptions": descs})

    from bson import encode as bson_encode
    coll_dir = DESC_DUMP / "usaspending_descriptions"
    coll_dir.mkdir(parents=True, exist_ok=True)
    bson_path = coll_dir / "contract_documents.bson"
    with bson_path.open("wb") as f:
        for d in docs:
            f.write(bson_encode(d))
    meta = {
        "options": {},
        "indexes": [
            {"v": 2, "key": {"_id": 1}, "name": "_id_"},
            {"v": 2, "key": {"award_id": 1}, "name": "award_id_1"},
        ],
        "uuid": "",
        "collectionName": "contract_documents",
        "type": "collection",
    }
    (coll_dir / "contract_documents.metadata.json").write_text(
        json.dumps(meta), encoding="utf-8"
    )
    manifest.commit()
    print(
        f"descriptions/: built ({len(docs)} docs, {n_eng_dropped} english-dropped)"
    )


def main():
    if not CLEAN_DB.exists():
        raise SystemExit(f"missing clean snapshot: {CLEAN_DB}")
    QD.mkdir(parents=True, exist_ok=True)
    clean = sqlite3.connect(CLEAN_DB)
    manifest = sqlite3.connect(MANIFEST_DB)
    init_manifest(manifest)
    build_contracts(clean, manifest)
    build_recipients(clean, manifest)
    build_agencies(clean, manifest)
    build_descriptions(clean, manifest)
    clean.close()
    manifest.close()
    print("OK")


if __name__ == "__main__":
    main()
