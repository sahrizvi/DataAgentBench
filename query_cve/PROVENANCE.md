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

- The canonical pre-corruption snapshot (`clean/clean.sqlite`) and the corruption manifest (`clean/manifest.sqlite`) — which together constitute the answer key — are kept local-only (gitignored).
- Construction code lives in `manual_querycode/` and IS shipped in this repo (full source for `fetch_clean.py`, `corrupt.py`, `llm_corrupt.py`, `audit_corruption.py`, `compute_ground_truth.py`).
- Re-running the corruption pipeline from scratch will not bit-reproduce the shipped artifacts because the LLM narrative steps are non-deterministic by design (temperature > 0). The deterministic transforms are bit-reproducible. Hashes above pin the specific byte-content shipped in this commit, regardless of regeneration path.
- Sonnet pass@1 on this dataset, plain mode, at the time of authoring: **3/10 = 30%**.

## Construction-code reference

Full source: `manual_querycode/fetch_clean.py`, `manual_querycode/corrupt.py`, `manual_querycode/llm_corrupt.py`, `manual_querycode/audit_corruption.py`, `manual_querycode/compute_ground_truth.py`.

Pipeline order to regenerate from scratch:
1. `python manual_querycode/fetch_clean.py` — downloads NVD + KEV + EPSS into `clean/clean.sqlite`
2. `python manual_querycode/corrupt.py` — emits the 4 agent-visible DBs into `query_dataset/`; deterministic transforms only
3. `python manual_querycode/llm_corrupt.py --scope kev` — populates `clean/manifest.sqlite` with verifier-validated severity narratives + score narratives (Azure OpenAI; reads `.env`)
4. `python manual_querycode/audit_corruption.py` — roundtrip-classifies every existing narrative; writes lists of mismatched cve_ids; rerun llm_corrupt on those until mismatch rate is <2%
5. `python manual_querycode/corrupt.py` again — picks up the validated narratives from manifest and bakes them into the agent-visible DBs
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

### LLM prompts (CVSS-score-as-narrative)

```
You are obfuscating a CVE's CVSS v3 base score (scale 0.0-10.0) for a benchmark.

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

Score-band classifier (output is one of `9.0-10.0` / `7.0-8.9` / `4.0-6.9` / `0.1-3.9`; rejection if it disagrees with the canonical band):

```
Read the sentence below and decide which CVSS v3 base score band it implies
(the score scale is 0.0 to 10.0). Choose EXACTLY one:
- 9.0-10.0
- 7.0-8.9
- 4.0-6.9
- 0.1-3.9

Output ONLY the band label.

Sentence: {sentence}
```

### Ground-truth-computation SQL highlights

Q4 (vendor with highest CRITICAL share among canonical KEV vendors with ≥10
qualifying CVEs):

```sql
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
```

Other queries' GT SQL is in `manual_querycode/compute_ground_truth.py` (one
function per query, each returning a string that becomes the queryN/ground_truth.csv).

