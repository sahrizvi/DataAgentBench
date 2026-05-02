# query_usaspending provenance

## Source data

| Source | URL | Fetched | Scope |
|---|---|---|---|
| USAspending.gov contract awards (REST API v2) | https://api.usaspending.gov/api/v2/search/spending_by_award/ | 2026-05-01 | Definitive contracts (award_type_codes A/B/C/D) with start dates 2024-07-01 .. 2024-09-30, sorted by Start Date desc. 10,000 awards paginated 100 / page (9,921 with non-null amount; 9,563 with non-null award_id after filtering); 3,317 unique recipients derived from those awards; 47 unique awarding agencies; NAICS sector hierarchy from `references/naics/`. |

The fetch sorts by start date, NOT by amount, so award amounts span 5+ orders of magnitude (p5 ≈ $890; p50 ≈ $59K; p95 ≈ $5M; max ≈ $1.6B). This makes threshold filters in queries (>$1M, >$5M, >$9M) meaningfully selective.

## Database engine assignment

| DB | Engine | Rationale |
|---|---|---|
| `contracts_db` | PostgreSQL | Transactional fact table (~9.9k contract rows) plus a sibling `contract_amounts` table |
| `recipients_db` | SQLite | Small entity registry (~3.3k recipients) |
| `agencies_db` | DuckDB | Analytical reference: agency hierarchy + agency-alias lookup + NAICS sector hierarchy |
| `descriptions_db` | MongoDB | Free-text contract descriptions, organized as one document per award with nested descriptions[] |

## Corruption layers (categories only)

Hash-deterministic transforms:

| Layer | Surface |
|---|---|
| Award ID format mixing | `contracts_db.contracts.award_id` (and the reference in `contract_amounts` and `descriptions_db`) |
| Recipient UEI format mixing | `contracts_db.contracts.recipient_uei`, `recipients_db.recipients.uei` |
| Awarding-agency surface-form variants (cluster needed for canonicalization) | `contracts_db.contracts.awarding_agency` (with `agencies_db.agency_aliases` lookup) |
| NAICS code reformatting (6-digit / `naics-XXXXXX` / `XX-XXXX`) | `contracts_db.contracts.naics_code` |
| Recipient name fuzzification (corporate-suffix variants, case, whitespace) | `recipients_db.recipients.name` |
| State surface-form variants | `recipients_db.recipients.state` |
| Templated amount-as-text fallback (`$1.5M` / `1,500,000.00 USD` / `1.5M`) | `contract_amounts.amount_text`, `recipients_db.recipients.total_amount_text` |
| Duplicate `contract_amounts` rows with conflicting amount values | ~3.5% of awards |
| English-description dropping | `descriptions_db.contract_documents` (deterministic ~10% subset) |

LLM-driven per-row narrative corruption with **roundtrip-classifier verification** (each generated narrative is classified back to its magnitude band by a separate LLM call before being accepted; mismatches retry up to 3 times):

| Layer | Surface | Anchor context | Generation model |
|---|---|---|---|
| Amount-as-narrative-prose | `contracts_db.contract_amounts.amount_text` | per-row recipient + awarding agency + NAICS description | `gpt-4o`, temp 0.95 |

## Verifier audit (post-generation)

| Layer | Total rows | Distinct narratives | Diversity ratio | Verifier mismatch rate |
|---|---|---|---|---|
| Amount-as-narrative | 9,744 | 9,737 | 99.93% | <1% |

A narrative is included only if (a) it contains no digits, (b) it contains no banned magnitude-leak tokens for its band (e.g. a `tens of thousands or less` row may not contain `million`/`billion`/`seven-figure`/etc.), (c) its length is within 30–280 chars, and (d) an independent LLM classifier recovers the canonical band. Rows that fail all retry attempts fall back to the templated form.

The narrative anchors on per-row context so each phrasing is substantively unique. Examples:
- `"This Department of Defense contract with LEIDOS, INC. represents a modest five-figure investment in computer systems design services."` (band: tens-of-thousands-or-less)
- `"For a defense giant like Lockheed Martin, this aircraft manufacturing contract reflects a substantial yet routine allocation within the eight-figure realm."` (band: tens-of-millions)

## Shipped artifact hashes (SHA-256)

```
3ec7cb010ad78868358b4a3cffe81a5adc037def483669d11a34bc3452253bb7  query_dataset/agencies.duckdb
7fdde155670e23568458570bdb17171b36f4789b49c95dde5461b03ca951a861  query_dataset/contracts.sql
a964552f7bbda8bb608046bae63714b791fcb90294e2956d9f1c8fe29b860518  query_dataset/descriptions/usaspending_descriptions/contract_documents.bson
008916d8764ba11e759be1499a78c0c090da2fa8b72ff409ed69623c2f1733b5  query_dataset/recipients.db
```

These pin the exact bytes of the agent-visible corrupted databases in this commit. Reviewers can verify with `shasum -a 256 query_usaspending/query_dataset/{agencies.duckdb,contracts.sql,recipients.db,descriptions/usaspending_descriptions/contract_documents.bson}`.

## Reproducibility notes

- The canonical pre-corruption snapshot (`clean/clean.sqlite`) and the corruption manifest (`clean/manifest.sqlite`) — which together constitute the answer key — are kept local-only (gitignored). Construction code lives in `manual_querycode/` (also gitignored, matching `query_googlelocal`, `query_yelp`, `query_stockmarket` convention).
- Re-running the corruption pipeline from scratch will not bit-reproduce the shipped artifacts because the LLM narrative steps are non-deterministic by design (temperature > 0). The deterministic transforms are bit-reproducible. Hashes above pin the specific byte-content shipped in this commit, regardless of regeneration path.
- Sonnet pass@1 on this dataset, plain mode, at the time of authoring: **5/10 = 50%**.
