"""Compute ground-truth answers from clean/clean.sqlite + clean/manifest.sqlite.

Each query incorporates >=2 of DAB's 4 properties (multi-DB integration,
ill-formatted joins, unstructured text transformation, domain knowledge).
Answers are deterministic Python over the canonical clean tables.
"""
from __future__ import annotations
import sqlite3
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN_DB = ROOT / "clean" / "clean.sqlite"
MANIFEST_DB = ROOT / "clean" / "manifest.sqlite"


def q1(c, m):
    """Multi-DB (vulns+kev+cpe) + ill-formatted (cve-id canon + vendor alias +
    vulnerable_flag): distinct CVEs published 2023, in KEV, with vulnerable Apache CPE."""
    row = c.execute("""
        SELECT COUNT(DISTINCT v.cve_id)
        FROM cves v
        JOIN kev k ON k.cve_id = v.cve_id
        JOIN cpe_matches cp ON cp.cve_id = v.cve_id
        WHERE substr(v.published, 1, 4) = '2023'
          AND lower(cp.vendor) = 'apache'
          AND cp.vulnerable = 1
    """).fetchone()
    return str(row[0])


def q2(c, m):
    """Multi-DB (kev+vulns) + ill-formatted (vendor clustering + cve-id canon)
    + unstructured (severity from narrative text): among KEV ransomware-flagged
    CVEs, which canonical vendor (lowercase) has the most CRITICAL-severity
    CVEs (consider only vendors with at least 3 ransomware-flagged CVEs)?

    Note: this is band-aligned. The narrative corruption preserves CVSS severity
    band (CRITICAL/HIGH/MEDIUM/LOW per the CVSS v3 spec), so a count of CRITICAL
    rows is fully recoverable from the narrative.
    """
    row = c.execute("""
        WITH ransom_kev AS (
            SELECT lower(k.vendor_project) AS v, c.cve_id, c.cvss3_severity
            FROM kev k
            JOIN cves c ON c.cve_id = k.cve_id
            WHERE lower(k.known_ransomware_use) = 'known'
        ),
        per_vendor AS (
            SELECT v,
                   COUNT(*) AS n,
                   SUM(CASE WHEN cvss3_severity = 'CRITICAL' THEN 1 ELSE 0 END) AS n_crit
            FROM ransom_kev
            GROUP BY v
            HAVING n >= 3
        )
        SELECT v FROM per_vendor
        ORDER BY n_crit DESC, v ASC
        LIMIT 1
    """).fetchone()
    return row[0]


def q3(c, m):
    """Multi-DB (kev+vulns) + ill-formatted (cve-id canon): KEV rows with no
    matching CVE in vulns_db."""
    row = c.execute("""
        SELECT COUNT(*) FROM kev k
        WHERE k.cve_id NOT IN (SELECT cve_id FROM cves)
    """).fetchone()
    return str(row[0])


def q4(c, m):
    """4-hop chained aggregation: among canonical KEV vendors with >=10 KEV
    CVEs that have at least one vulnerable CPE configuration, return the vendor
    with the HIGHEST SHARE of CVEs whose CVSS severity is CRITICAL.

    Properties exercised: multi-DB (kev+cpe+vulns) + ill-formatted (KEV vendor
    cluster + CVE-id canon + alias/vuln_flag) + unstructured (severity).
    """
    rows = c.execute("""
        WITH kev_with_vuln_cpe AS (
            SELECT DISTINCT lower(k.vendor_project) AS vendor, k.cve_id
            FROM kev k
            JOIN cpe_matches cp ON cp.cve_id = k.cve_id
            WHERE cp.vulnerable = 1
        ),
        sev AS (
            SELECT cve_id, cvss3_severity FROM cves WHERE cvss3_severity IS NOT NULL
        )
        SELECT k.vendor,
               COUNT(*) AS n,
               SUM(CASE WHEN sev.cvss3_severity = 'CRITICAL' THEN 1 ELSE 0 END) AS n_crit
        FROM kev_with_vuln_cpe k
        LEFT JOIN sev ON sev.cve_id = k.cve_id
        GROUP BY k.vendor
        HAVING n >= 10
        ORDER BY (1.0 * n_crit / n) DESC, k.vendor ASC
        LIMIT 1
    """).fetchall()
    return rows[0][0] if rows else "NONE"


def q5(c, m):
    """Multi-DB (kev+cpe) + ill-formatted (cve-id canon + vendor alias) +
    unstructured (version encoding): distinct affected version strings for
    apache:tomcat AMONG CVEs that are also in KEV."""
    row = c.execute("""
        SELECT COUNT(DISTINCT cp.version)
        FROM cpe_matches cp
        JOIN kev k ON k.cve_id = cp.cve_id
        WHERE lower(cp.vendor) = 'apache'
          AND lower(cp.product) = 'tomcat'
          AND cp.version IS NOT NULL
          AND cp.version != '*'
    """).fetchone()
    return str(row[0])


def q6(c, m):
    """Multi-DB (descriptions+kev) + ill-formatted (cve-id canon) + unstructured
    (language detection): CVEs with NO English description but with a non-English
    one AND listed in KEV."""
    eng_dropped = {r[0] for r in m.execute("SELECT cve_id FROM planted_eng_dropped")}
    has_other_lang = {
        r[0] for r in c.execute(
            "SELECT DISTINCT cve_id FROM cve_descriptions WHERE lang != 'en'"
        )
    }
    in_kev = {r[0] for r in c.execute("SELECT cve_id FROM kev")}
    return str(len(eng_dropped & has_other_lang & in_kev))


def q7(c, m):
    """Multi-DB (cpe+kev) + ill-formatted (cve-id canon + vendor alias +
    vulnerable_flag): canonical (vendor, product) with highest count of
    vulnerable CPE rows whose CVE is also in KEV."""
    row = c.execute("""
        SELECT lower(cp.vendor) || ':' || lower(cp.product) AS vp, COUNT(*) AS n
        FROM cpe_matches cp
        JOIN kev k ON k.cve_id = cp.cve_id
        WHERE cp.vulnerable = 1
          AND cp.vendor IS NOT NULL
          AND cp.product IS NOT NULL
        GROUP BY vp
        ORDER BY n DESC, vp ASC
        LIMIT 1
    """).fetchone()
    return row[0]


def q8(c, m):
    """Multi-DB (vulns+kev+cpe) + ill-formatted (alias + cve-id canon +
    vulnerable_flag) + unstructured (severity from narrative text): how many
    CVEs are in KEV AND have at least one vulnerable Microsoft CPE configuration
    AND have CVSS v3 severity HIGH or CRITICAL (i.e. base score >= 7.0)?

    Note: this is band-aligned. The threshold 7.0 is the boundary between MEDIUM
    and HIGH per the CVSS v3 spec, so 'HIGH or CRITICAL' is a band-level question
    fully recoverable from the narrative-corrupted score_text.
    """
    row = c.execute("""
        SELECT COUNT(*)
        FROM cves v
        JOIN kev k ON k.cve_id = v.cve_id
        JOIN (
            SELECT DISTINCT cve_id FROM cpe_matches
            WHERE lower(vendor) = 'microsoft' AND vulnerable = 1
        ) ms ON ms.cve_id = v.cve_id
        WHERE v.cvss3_severity IN ('HIGH', 'CRITICAL')
    """).fetchone()
    return str(row[0])


def q9(c, m):
    """Multi-DB (vulns+kev) + ill-formatted (cve-id canon for self-join + KEV
    join): CVEs that have a duplicate row with conflicting attack_vector AND
    are also listed in KEV."""
    in_kev = {r[0] for r in c.execute("SELECT cve_id FROM kev")}
    duped = {r[0] for r in m.execute("SELECT cve_id FROM planted_duplicate")}
    return str(len(in_kev & duped))


def q10(c, m):
    """Multi-DB (kev+vulns) + ill-formatted (KEV vendor clustering + cve-id
    canon + products_csv split) + unstructured (CSV parsing): how many distinct
    Microsoft products (per canonical KEV vendor 'microsoft', after splitting
    on '/' or ',') have at least one CVE in KEV with CVSS base score >= 9.0?"""
    products = set()
    rows = c.execute("""
        SELECT k.product, v.cvss3_base_score
        FROM kev k
        JOIN cves v ON v.cve_id = k.cve_id
        WHERE lower(k.vendor_project) = 'microsoft'
          AND k.product IS NOT NULL
          AND v.cvss3_base_score IS NOT NULL
          AND v.cvss3_base_score >= 9.0
    """).fetchall()
    for prod, _ in rows:
        for p in prod.split("/"):
            p = p.strip()
            if p:
                products.add(p.lower())
    return str(len(products))


QUERIES = {
    "1":  q1, "2":  q2, "3":  q3, "4":  q4, "5":  q5,
    "6":  q6, "7":  q7, "8":  q8, "9":  q9, "10": q10,
}


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
