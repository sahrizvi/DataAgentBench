# query_cve provenance

## Source data

| Source | URL | Fetched | Scope |
|---|---|---|---|
| NVD CVE feed (REST API 2.0) | https://services.nvd.nist.gov/rest/json/cves/2.0 | 2026-04-27 | All CVEs published 2023-01-01 .. 2024-12-31 (71,653 CVEs ingested). Paginated 2000 records / page in 120-day windows per the NVD rate-limit policy. |
| CISA Known Exploited Vulnerabilities catalog | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | 2026-04-27 | Full catalog at fetch time (1,583 entries). |
| FIRST EPSS daily scores | https://epss.empiricalsecurity.com/epss_scores-{date}.csv.gz | 2026-04-27 | Three snapshot dates (2024-01-02, 2024-06-01, 2026-04-25); only CVEs already in the NVD ingest set were retained. NOT used in any of the 10 queries — kept off the agent surface in this dataset. |

## Database engine assignment

| DB | Engine | Rationale |
|---|---|---|
| `vulns_db` | SQLite | Small embedded structured registry (cves, cvss_metadata) |
| `cpe_db` | DuckDB | Analytical / columnar — large fact table (585k cpe_match rows) plus reference / version-detail tables |
| `kev_db` | PostgreSQL | Structured catalog dump (CISA's actual API serves the same shape) |
| `descriptions_db` | MongoDB | Free-text + nested arrays per CVE (descriptions in multiple languages, references) |

## Corruption layers (categories only)

Hash-deterministic transforms (each row's choice is keyed by a stable SHA-1 hash of a salted identifier so the build is reproducible given the same source data + scripts):

| Layer | Surface |
|---|---|
| Cross-DB CVE-id format mixing | vulns / cpe / kev / descriptions. Every CVE-bearing join key is prefixed by one of 500 deterministic noisy source prefixes and then stores the CVE as `CVE-YYYY-NNNN`, `cve-YYYY-NNNN`, `YYYY-NNNN`, `YYYY_NNNN`, or `YYYY:NNNN`. |
| CPE vendor aliasing (canonical name → opaque alias) | `cpe_db.cpe_matches.criteria` (with `cpe_db.vendor_aliases` lookup) |
| `vulnerable_flag` varied truthy/falsy tokens | `cpe_db.cpe_matches.vulnerable_flag` |
| CPE version-encoding mix (semver, comma-sep, build-number, etc.) | `cpe_db.cpe_version_details.version_text` |
| KEV vendor surface-form variants | `kev_db.kev_entries.vendor_project` (resolved by visible `kev_db.kev_vendor_aliases`) |
| Packed comma-separated product lists | `kev_db.kev_entries.products_csv` |
| Referential-integrity gap | `kev_db` ↔ `vulns_db` (some KEV CVEs predate the bounded NVD window) |
| Duplicate rows with conflicting `cvss3_attack_vector` | `vulns_db.cves` (~5% of CVEs) |
| English-description dropping | `descriptions_db.cve_documents` (deterministic ~5% subset) |
| Exact CVSS base-score text formatting | `vulns_db.cvss_metadata.score_text` (numeric score preserved, format varies per row) |

LLM-driven per-row narrative corruption with **roundtrip-classifier verification** (each generated severity narrative is classified back to its canonical severity by a separate LLM call before being accepted; mismatches retry up to 3 times):

| Layer | Surface | Anchor context | Generation model |
|---|---|---|---|
| Severity-as-narrative-prose | `descriptions_db.cve_documents.descriptions[].value` (English) | the unique CVE description itself | `gpt-4o`, temp 0.7 |

## Verifier audit (post-generation)

| Layer | Total rows | Distinct narratives | Diversity ratio | Verifier mismatch rate |
|---|---|---|---|---|
| Severity-as-narrative (KEV CVEs) | 294 | 294 | 100.0% | 1.9% |

A narrative is included in the shipped artifacts only if (a) it contains no banned tokens, (b) its content overlaps lexically with the original CVE prose, (c) its length is within 50–600 chars, and (d) an independent LLM classifier recovers the canonical severity. Rows that fail all retry attempts fall back to the deterministic templated form.

## What the corruption preserves vs. discards

The agent-visible CVSS score surface now preserves exact numeric base scores.
`vulns_db.cvss_metadata.score_text` uses varied text wrappers, so agents must
parse each row. The CVSS score is always the first numeric token in the field,
and no CVSS threshold query depends on recovering a hidden severity band from
prose.

KEV vendor surface-form variants are also explicit rather than underspecified:
`kev_db.kev_vendor_aliases` maps every `kev_entries.vendor_project` surface
form in the shipped SQL dump to the canonical lowercase vendor used by the
queries. Agents still need to join row by row through that lookup, but they do
not need to invent a clustering algorithm.

CVE joins are intentionally not solvable by enumerating a short list of known
prefixes. The shipped artifacts contain all 500 noisy CVE-key prefixes. The
recoverable operation is to extract the embedded CVE year and numeric suffix
and normalize to `CVE-YYYY-NNNN` before joining.

## Shipped artifact hashes (SHA-256)

```
305cedf0ba0169f025e21b1e76cf33242470fe4628d853997b462db594b08fe1  query_dataset/cpe.duckdb
fe393f0e761040c843619b3b4f77e2862c25ec5a13dbb2af816f3c5443b9f3f6  query_dataset/descriptions/cve_descriptions/cve_documents.bson
618c30ff559c3de4d1c12bac6ac501f74e94dfed047194343f3e81524afd2d9a  query_dataset/kev.sql
712a32f3336237c2a532d381390d6b630584fe9dd52b942e70511cae19a434c7  query_dataset/vulns.db
```

These pin the exact bytes of the agent-visible corrupted databases in this commit. Reviewers can `shasum -a 256 query_cve/query_dataset/{cpe.duckdb,descriptions/cve_descriptions/cve_documents.bson,kev.sql,vulns.db}` to verify they have the same dataset.

## Reproducibility notes

- The canonical pre-corruption snapshot (`clean/clean.sqlite`) and the corruption manifest (`clean/manifest.sqlite`) — which together constitute the answer key — are kept local-only (gitignored).
- Construction code lives in `manual_querycode/` and IS shipped in this repo (full source for `fetch_clean.py`, `corrupt.py`, `llm_corrupt.py`, `audit_corruption.py`, `compute_ground_truth.py`).
- Re-running the corruption pipeline from scratch will not bit-reproduce the shipped artifacts because the LLM narrative steps are non-deterministic by design (temperature > 0). The deterministic transforms are bit-reproducible. Hashes above pin the specific byte-content shipped in this commit, regardless of regeneration path.
- Sonnet pass@1 on this dataset, plain mode, at the time of authoring: **3/10 = 30%**.

## Construction-code reference

Full source: `manual_querycode/fetch_clean.py`, `manual_querycode/corrupt.py`, `manual_querycode/llm_corrupt.py`, `manual_querycode/audit_corruption.py`, `manual_querycode/compute_ground_truth.py`.

Pipeline order to regenerate from scratch:
1. `python manual_querycode/fetch_clean.py` — downloads NVD + KEV + EPSS into `clean/clean.sqlite`
2. `python manual_querycode/corrupt.py` — emits the 4 agent-visible DBs into `query_dataset/`; deterministic transforms only
3. `python manual_querycode/llm_corrupt.py --scope kev` — populates `clean/manifest.sqlite` with verifier-validated severity narratives (Azure OpenAI; reads `.env`)
4. `python manual_querycode/audit_corruption.py` — roundtrip-classifies every existing narrative; writes lists of mismatched cve_ids; rerun llm_corrupt on those until mismatch rate is <2%
5. `python manual_querycode/corrupt.py` again — picks up the validated severity narratives from manifest and bakes them into the agent-visible DBs
6. `python manual_querycode/compute_ground_truth.py` — emits `queryN/ground_truth.csv` for all 10 queries from the canonical clean data

### LLM prompts (severity-as-narrative)

```
You are obfuscating a CVE description for a benchmark.

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
```

Where `{motifs}` is one of (keyed by canonical severity):

```python
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
```

### Roundtrip verifier prompts

Severity classifier (output is one of CRITICAL / HIGH / MEDIUM / LOW; rejection if it disagrees with the canonical):

```
Read the CVE description below and decide which CVSS v3 severity
classification it most naturally implies. Choose EXACTLY one:
- CRITICAL
- HIGH
- MEDIUM
- LOW

Output ONLY the label, nothing else.

Description: {desc}
```

### Ground-truth-computation SQL highlights

Q4 (vendor with highest share of CVSS ≥ 9.0 among canonical KEV vendors with
≥10 qualifying CVEs):

```sql
WITH kev_with_vuln_cpe AS (
    SELECT DISTINCT lower(k.vendor_project) AS vendor, k.cve_id
    FROM kev k
    JOIN cpe_matches cp ON cp.cve_id = k.cve_id
    WHERE cp.vulnerable = 1
),
sev AS (
    SELECT cve_id, cvss3_base_score FROM cves WHERE cvss3_base_score IS NOT NULL
)
SELECT k.vendor,
       COUNT(*) AS n,
       SUM(CASE WHEN sev.cvss3_base_score >= 9.0 THEN 1 ELSE 0 END) AS n_crit
FROM kev_with_vuln_cpe k
LEFT JOIN sev ON sev.cve_id = k.cve_id
GROUP BY k.vendor
HAVING n >= 10
ORDER BY (1.0 * n_crit / n) DESC, k.vendor ASC
LIMIT 1
```

Other queries' GT SQL is in `manual_querycode/compute_ground_truth.py` (one
function per query, each returning a string that becomes the queryN/ground_truth.csv).
