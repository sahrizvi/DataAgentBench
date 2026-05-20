"""Compute ground-truth from clean.sqlite + manifest.sqlite.
Each query incorporates >=2 DAB properties.
"""
from __future__ import annotations
import sqlite3
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN_DB = ROOT / "clean" / "clean.sqlite"
MANIFEST_DB = ROOT / "clean" / "manifest.sqlite"


def q1(c, m):
    """Count contracts in DOD (any surface form) with amount > $1M.
    Multi-DB + ill-formatted (agency cluster) + unstructured (amount-as-text)."""
    n = c.execute("""
        SELECT COUNT(*) FROM contracts
        WHERE awarding_agency = 'Department of Defense' AND amount > 1000000
    """).fetchone()[0]
    return str(n)


def q2(c, m):
    """Multi-DB + ill-formatted (state) + unstructured (amount band): count
    of contract awards whose recipient is in California (any surface form)
    AND whose amount is greater than $1,000,000.

    Note: $1M aligns with the boundary between the 'hundreds of thousands'
    and 'millions' magnitude bands, so this threshold is fully recoverable
    from the narrative-corrupted amount_text.
    """
    n = c.execute("""
        SELECT COUNT(*)
        FROM contracts c
        JOIN recipients r ON r.uei = c.recipient_uei
        WHERE r.state = 'CA' AND c.amount IS NOT NULL AND c.amount > 1000000
    """).fetchone()[0]
    return str(n)


def q3(c, m):
    """Distinct UEIs in NAICS sector 33 (Manufacturing).
    Multi-DB + ill-formatted (NAICS reformatting + UEI canon)."""
    n = c.execute("""
        SELECT COUNT(DISTINCT recipient_uei)
        FROM contracts
        WHERE substr(naics_code, 1, 2) = '33'
          AND recipient_uei IS NOT NULL
    """).fetchone()[0]
    return str(n)


def q4(c, m):
    """Canonical agency (>=10 contracts) with highest share of contracts > $1M.
    Multi-DB + ill-formatted (agency cluster) + unstructured (amount) + chained agg."""
    rows = c.execute("""
        SELECT awarding_agency,
               COUNT(*) AS n,
               SUM(CASE WHEN amount > 1000000 THEN 1 ELSE 0 END) AS n_big
        FROM contracts
        WHERE awarding_agency IS NOT NULL
        GROUP BY awarding_agency
        HAVING n >= 10
        ORDER BY (1.0 * n_big / n) DESC, awarding_agency ASC
        LIMIT 1
    """).fetchall()
    return rows[0][0] if rows else "NONE"


def q5(c, m):
    """Multi-DB + ill-formatted (NAICS) + unstructured (amount band): distinct
    NAICS 2-digit sectors represented across contracts of at least $10,000,000.

    Note: $10M aligns with the boundary between the 'millions' and 'tens of
    millions' magnitude bands, so this threshold is fully recoverable from the
    narrative-corrupted amount_text.
    """
    n = c.execute("""
        SELECT COUNT(DISTINCT substr(naics_code, 1, 2))
        FROM contracts
        WHERE amount >= 10000000 AND naics_code IS NOT NULL
    """).fetchone()[0]
    return str(n)


def q6(c, m):
    """Distinct canonical recipients that appear in recipients_db under MORE THAN
    ONE UEI. Canonicalization: lowercase, strip whitespace, drop trailing
    corporate suffix tokens (inc, inc., incorporated, corp, corp., corporation,
    llc, l.l.c., co, co., company, ltd, ltd., limited).
    Multi-DB + ill-formatted (recipient name fuzz)."""
    import re
    suffix_re = re.compile(
        r"[\s,]+(inc\.?|incorporated|corp\.?|corporation|llc\.?|l\.l\.c\.?|"
        r"co\.?|company|ltd\.?|limited)$",
        re.IGNORECASE,
    )
    canon: dict[str, set[str]] = {}
    for uei, name in c.execute(
        "SELECT uei, name FROM recipients WHERE name IS NOT NULL"
    ):
        n = name.strip().lower()
        # repeatedly strip trailing corporate suffix tokens
        while True:
            new_n = suffix_re.sub("", n).strip().rstrip(",")
            if new_n == n:
                break
            n = new_n
        canon.setdefault(n, set()).add(uei)
    return str(sum(1 for ueis in canon.values() if len(ueis) > 1))


def q7(c, m):
    """Multi-DB + ill-formatted (NAICS) + unstructured (amount band): NAICS
    2-digit sector with the most contracts of at least $10,000,000.

    Note: $10M aligns with the boundary between the 'millions' and 'tens of
    millions' magnitude bands. Counting rows with amount in the upper bands
    is fully recoverable from the narrative-corrupted amount_text.
    """
    row = c.execute("""
        SELECT substr(c.naics_code, 1, 2) AS sec, COUNT(*) AS n
        FROM contracts c
        WHERE c.naics_code IS NOT NULL
          AND c.amount IS NOT NULL
          AND c.amount >= 10000000
        GROUP BY sec
        ORDER BY n DESC, sec ASC
        LIMIT 1
    """).fetchone()
    return row[0]


def q8(c, m):
    """Multi-DB + ill-formatted (recipient fuzz + agency cluster) + unstructured
    (amount band): count of contracts awarded to Lockheed Martin (across all
    UEIs and recipient_name surface-form variants) by the Department of Defense
    (across all agency surface-form variants) with amount greater than $1,000,000.

    Note: $1M aligns with the boundary between the 'hundreds of thousands' and
    'millions' magnitude bands, so this threshold is fully recoverable from
    the narrative-corrupted amount_text.
    """
    n = c.execute("""
        SELECT COUNT(*)
        FROM contracts
        WHERE upper(recipient_name) LIKE '%LOCKHEED MARTIN%'
          AND awarding_agency = 'Department of Defense'
          AND amount IS NOT NULL
          AND amount > 1000000
    """).fetchone()[0]
    return str(n)


def q9(c, m):
    """Contracts where English description was DROPPED AND amount > $1M.
    Multi-DB (contracts+descriptions) + ill-formatted + unstructured (amount)."""
    eng_dropped = {r[0] for r in m.execute("SELECT award_id FROM planted_eng_dropped")}
    rows = c.execute("""
        SELECT award_id FROM contracts WHERE amount > 1000000
    """).fetchall()
    return str(sum(1 for (aid,) in rows if aid in eng_dropped))


def q10(c, m):
    """Among top-10 recipients by contract count, how many contracts have a
    superseded (_OLD) amount entry in contract_amounts?
    Multi-DB + ill-formatted (award_id normalization + UEI normalization)."""
    # Top-10 by contract count from canonical contracts (tie-break by uei asc)
    top10_ueis = {r[0] for r in c.execute("""
        SELECT recipient_uei, COUNT(*) AS n
        FROM contracts
        WHERE recipient_uei IS NOT NULL
        GROUP BY recipient_uei
        ORDER BY n DESC, recipient_uei ASC
        LIMIT 10
    """)}
    # Contracts with superseded amounts come from the planted_duplicate manifest
    duped = {r[0] for r in m.execute("SELECT canonical_award_id FROM planted_duplicate")}
    n = sum(
        1 for (award_id, uei) in c.execute(
            "SELECT award_id, recipient_uei FROM contracts "
            "WHERE recipient_uei IS NOT NULL AND award_id IS NOT NULL"
        )
        if award_id in duped and uei in top10_ueis
    )
    return str(n)


QUERIES = {"1": q1, "2": q2, "3": q3, "4": q4, "5": q5,
           "6": q6, "7": q7, "8": q8, "9": q9, "10": q10}


def main():
    c = sqlite3.connect(CLEAN_DB)
    m = sqlite3.connect(MANIFEST_DB)
    for qid, fn in QUERIES.items():
        ans = fn(c, m)
        out = ROOT / f"query{qid}" / "ground_truth.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(ans + "\n", encoding="utf-8")
        print(f"query{qid}: {ans}")


if __name__ == "__main__":
    main()
