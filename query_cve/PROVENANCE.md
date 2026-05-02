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
| Cross-DB CVE-id format mixing | vulns / cpe / kev / descriptions |
| CPE vendor aliasing (canonical name → opaque alias) | `cpe_db.cpe_matches.criteria` (with `cpe_db.vendor_aliases` lookup) |
| `vulnerable_flag` varied truthy/falsy tokens | `cpe_db.cpe_matches.vulnerable_flag` |
| CPE version-encoding mix (semver, comma-sep, build-number, etc.) | `cpe_db.cpe_version_details.version_text` |
| KEV vendor surface-form variants | `kev_db.kev_entries.vendor_project` |
| Packed comma-separated product lists | `kev_db.kev_entries.products_csv` |
| Referential-integrity gap | `kev_db` ↔ `vulns_db` (some KEV CVEs predate the bounded NVD window) |
| Duplicate rows with conflicting `cvss3_attack_vector` | `vulns_db.cves` (~5% of CVEs) |
| English-description dropping | `descriptions_db.cve_documents` (deterministic ~5% subset) |

LLM-driven per-row narrative corruption with **roundtrip-classifier verification** (each generated narrative is classified back to its canonical band by a separate LLM call before being accepted; mismatches retry up to 3 times):

| Layer | Surface | Anchor context | Generation model |
|---|---|---|---|
| CVSS-score-as-narrative-prose | `vulns_db.cvss_metadata.score_text` | per-row vendor + product + 240-char vulnerability summary | `gpt-4o`, temp 0.95 |
| Severity-as-narrative-prose | `descriptions_db.cve_documents.descriptions[].value` (English) | the unique CVE description itself | `gpt-4o`, temp 0.7 |

## Verifier audit (post-generation)

| Layer | Total rows | Distinct narratives | Diversity ratio | Verifier mismatch rate |
|---|---|---|---|---|
| CVSS-score-as-narrative | 225 | 225 | 100.0% | <2% |
| Severity-as-narrative (KEV CVEs) | 309 | 309 | 100.0% | 1.9% |

A narrative is included in the shipped artifacts only if (a) it contains no banned tokens, (b) its content overlaps lexically with the original CVE prose, (c) its length is within 50–600 chars, and (d) an independent LLM classifier recovers the canonical band. Rows that fail all retry attempts fall back to the deterministic templated form.

## Shipped artifact hashes (SHA-256)

```
ba16013d0e57fc909f4c880efb6b2992860482765cecc6ef18d1386f3199f525  query_dataset/cpe.duckdb
5b8b57e41dce71cbea100502c879fc837743caaccbb9df5bc69de0081fb78743  query_dataset/descriptions/cve_descriptions/cve_documents.bson
96bcf4abe38bd5a3a2f83cbaed267833d8bc1996b39dedf6c041a68aa16b20f5  query_dataset/kev.sql
8b88f651fa43541c914ac585b21c8d093922117671c953a84b753c710f53ff72  query_dataset/vulns.db
```

These pin the exact bytes of the agent-visible corrupted databases in this commit. Reviewers can `shasum -a 256 query_cve/query_dataset/{cpe.duckdb,descriptions/cve_descriptions/cve_documents.bson,kev.sql,vulns.db}` to verify they have the same dataset.

## Reproducibility notes

- The canonical pre-corruption snapshot (`clean/clean.sqlite`) and the corruption manifest (`clean/manifest.sqlite`) — which together constitute the answer key — are kept local-only (gitignored). Construction code lives in `manual_querycode/` (also gitignored, matching `query_googlelocal`, `query_yelp`, `query_stockmarket` convention).
- Re-running the corruption pipeline from scratch will not bit-reproduce the shipped artifacts because the LLM narrative steps are non-deterministic by design (temperature > 0). The deterministic transforms are bit-reproducible. Hashes above pin the specific byte-content shipped in this commit, regardless of regeneration path.
- Sonnet pass@1 on this dataset, plain mode, at the time of authoring: **3/10 = 30%**.
