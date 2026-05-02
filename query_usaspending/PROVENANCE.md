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

- The canonical pre-corruption snapshot (`clean/clean.sqlite`) and the corruption manifest (`clean/manifest.sqlite`) — which together constitute the answer key — are kept local-only (gitignored).
- Construction code lives in `manual_querycode/` and IS shipped in this repo (full source for `fetch_clean.py`, `corrupt.py`, `llm_corrupt.py`, `compute_ground_truth.py`).
- Re-running the corruption pipeline from scratch will not bit-reproduce the shipped artifacts because the LLM narrative steps are non-deterministic by design (temperature > 0). The deterministic transforms are bit-reproducible. Hashes above pin the specific byte-content shipped in this commit, regardless of regeneration path.
- Sonnet pass@1 on this dataset, plain mode, at the time of authoring: **5/10 = 50%**.

## Construction-code reference

Full source: `manual_querycode/fetch_clean.py`, `manual_querycode/corrupt.py`, `manual_querycode/llm_corrupt.py`, `manual_querycode/compute_ground_truth.py`.

Pipeline order to regenerate from scratch:
1. `python manual_querycode/fetch_clean.py` — paginates the USAspending search-by-award API into `clean/clean.sqlite`
2. `python manual_querycode/corrupt.py` — emits the 4 agent-visible DBs into `query_dataset/`; deterministic transforms only (templated `amount_text` placeholder)
3. `python manual_querycode/llm_corrupt.py` — generates verifier-validated narrative amounts into `clean/manifest.sqlite` (Azure OpenAI; reads `.env`)
4. `python manual_querycode/corrupt.py` again — picks up the validated narratives from manifest and bakes them into the `contracts.sql` dump
5. `python manual_querycode/compute_ground_truth.py` — emits `queryN/ground_truth.csv` for all 10 queries from the canonical clean data

### LLM prompt (amount-as-narrative)

```
You are obfuscating a federal contract's dollar amount for a benchmark.

Write ONE sentence (40 - 280 characters) that *implies* the dollar magnitude
of the contract through narrative phrasing. The sentence MUST NOT contain any
digits, currency symbols, "USD", or precision words ("exactly", "precisely").

Constraint — anchor in contract-specific context. Reference at least one of
the contract details below NATURALLY in the sentence (recipient, agency, or
domain hint). This makes each narrative substantively unique per row.

Constraint — VARY phrasing aggressively. Do NOT default to stock templates
like "in the hundreds of thousands range" or "a relatively modest award".
Each row should use distinct vocabulary, syntactic structure, and register.
Treat each row as a unique editorial paraphrase. Some registers to draw
from (rotate through them):
- terse procurement-style: "Mid-six-figure outlay for {{domain}} services."
- analyst-paragraph: "In context, this Air Force agreement sits among the
  smaller-dollar logistics awards typical for the buyer."
- comparative: "A smaller commitment than {{recipient}}'s prior awards in the
  same NAICS bracket."
- hedged: "Roughly an order of magnitude below the median large-vendor IT
  modernization deal of recent quarters."
- domain-flavored: "Hardware-procurement-tier money — sub-million but
  meaningful for the program office."
- counterfactual: "Were this an R&D award rather than O&M, the figure would
  read large; for routine sustainment it is unremarkable."

Magnitude bands (the sentence must clearly imply the band, but never use the
identical phrasing twice across different rows):
- billions: convey "billions" / "ten-figure"
- hundreds of millions: "nine-figure" / "hundreds of millions"
- tens of millions: "eight-figure" / "tens of millions"
- millions: "seven-figure" / "low-to-mid millions"
- hundreds of thousands: "six-figure" / "hundreds of thousands"
- tens of thousands or less: "five-figure or smaller" / "low five-figure"
  / "modest sub-six-figure"

Magnitude band for this row: {band}

CRITICAL — band-specific constraints. The narrative must NOT contain words
that imply a higher band than the target band. Specifically:
- if band is "tens of thousands or less": the words "million", "millions",
  "billion", "billions", "six-figure", "seven-figure", "eight-figure",
  "nine-figure", "ten-figure", "hundreds of thousands" MUST NOT appear.
  Use "five-figure" or "four-figure" or "small four/five-figure" / "tens of
  thousands" / "modest five-figure" only.
- if band is "hundreds of thousands": the words "million", "millions",
  "billion", "billions", "seven-figure", "eight-figure", "nine-figure",
  "ten-figure" MUST NOT appear. Use "six-figure" / "hundreds of thousands"
  only.
- if band is "millions": "billion(s)", "ten-figure", "nine-figure",
  "eight-figure" MUST NOT appear; use "seven-figure" / "low-to-mid millions"
  / "single-digit millions".
- if band is "tens of millions": "billion(s)", "ten-figure", "nine-figure"
  MUST NOT appear; use "eight-figure" / "tens of millions".
- if band is "hundreds of millions": "billion(s)", "ten-figure" MUST NOT
  appear; use "nine-figure" / "hundreds of millions" / "high nine-figure".
- if band is "billions": use "ten-figure" / "billions" / "multi-billion";
  do NOT use "trillion".

Aim for tight, accurate magnitude phrasing — the goal is OBFUSCATING the
exact dollar value while being faithful about the order of magnitude. Even
if the recipient or agency is famous for big-dollar awards, you must reflect
the actual band of THIS row.

Contract context (incorporate naturally — but do not include the contract id):
- recipient: {recipient}
- awarding agency: {agency}
- domain (NAICS description): {naics_desc}

Output ONLY the sentence. No preamble. No digits.
```

Bands are defined as:

```python
def _band(amount: float) -> str:
    if amount >= 1_000_000_000:    return "billions"
    if amount >= 100_000_000:      return "hundreds of millions"
    if amount >= 10_000_000:       return "tens of millions"
    if amount >= 1_000_000:        return "millions"
    if amount >= 100_000:          return "hundreds of thousands"
    return "tens of thousands or less"
```

### Roundtrip verifier prompt

Output is exactly one of `billions` / `hundreds of millions` / `tens of millions` / `millions` / `hundreds of thousands` / `tens of thousands or less`. Rejection if it disagrees with the canonical band.

```
Read the sentence below and decide which dollar-magnitude band it most
naturally describes. Choose EXACTLY one of:
- billions
- hundreds of millions
- tens of millions
- millions
- hundreds of thousands
- tens of thousands or less

Output ONLY the band label, nothing else.

Sentence: {sentence}
```

### Ground-truth-computation SQL highlights

Q4 (canonical agency with highest >$1M-share among agencies with ≥10 contracts):

```sql
SELECT awarding_agency,
       COUNT(*) AS n,
       SUM(CASE WHEN amount > 1000000 THEN 1 ELSE 0 END) AS n_big
FROM contracts
WHERE awarding_agency IS NOT NULL
GROUP BY awarding_agency
HAVING n >= 10
ORDER BY (1.0 * n_big / n) DESC, awarding_agency ASC
LIMIT 1
```

Q6 (distinct canonical recipients with multiple UEIs after corporate-suffix
normalization):

```python
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
    while True:
        new_n = suffix_re.sub("", n).strip().rstrip(",")
        if new_n == n:
            break
        n = new_n
    canon.setdefault(n, set()).add(uei)
result = sum(1 for ueis in canon.values() if len(ueis) > 1)
```

Other queries' GT SQL is in `manual_querycode/compute_ground_truth.py` (one
function per query, each returning a string that becomes the queryN/ground_truth.csv).

