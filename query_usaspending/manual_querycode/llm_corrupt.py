"""LLM-driven per-row amount narrative corruption for USAspending contracts.

For each contract amount we want to obfuscate, call Azure OpenAI to produce a
short sentence that implies the dollar magnitude through phrasing — never
digits, never the literal number.

Guardrails (each output must pass; up to 3 retries; otherwise the row keeps
its templated amount_text from corrupt.py):

  * MUST contain no digits at all
  * MUST contain no banned tokens (currency-symbol $, "USD", numeric words like
    "one"/"two"/"three" if they would leak the exact value, etc. — softer here:
    we allow rough words like "million" / "billion" / "thousand" but NOT exact
    counts)
  * MUST be 1 short sentence, 30 - 250 chars
  * MUST be in English (ascii ratio > 0.9)

Outputs landed in clean/manifest.sqlite:
  planted_narrative_amount  (canonical_award_id, canonical_amount, narrative)
"""
from __future__ import annotations
import argparse
import os
import re
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN_DB = ROOT / "clean" / "clean.sqlite"
MANIFEST_DB = ROOT / "clean" / "manifest.sqlite"
ENV_FILE = ROOT.parent / ".env"


def _load_env():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


_load_env()


def _client():
    from openai import AzureOpenAI
    return AzureOpenAI(
        api_key=os.environ["AZURE_API_KEY"],
        azure_endpoint=os.environ["AZURE_API_BASE"],
        api_version=os.environ["AZURE_API_VERSION"],
    )


DEPLOYMENT = os.environ.get("AZURE_DEPLOYMENT", "gpt-4o")


# Block only explicit-precision tokens. The word "dollars" / "$" is fine
# because it doesn't leak the magnitude — we enforce no-digits separately.
DENY = {"exactly", "precisely"}


PROMPT = """You are obfuscating a federal contract's dollar amount for a benchmark.

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
"""


def _band(amount: float) -> str:
    if amount >= 1_000_000_000:
        return "billions"
    if amount >= 100_000_000:
        return "hundreds of millions"
    if amount >= 10_000_000:
        return "tens of millions"
    if amount >= 1_000_000:
        return "millions"
    if amount >= 100_000:
        return "hundreds of thousands"
    return "tens of thousands or less"


def _length_ok(s: str) -> bool:
    return 30 <= len(s) <= 250


def _ascii_ratio(s: str) -> float:
    if not s:
        return 1.0
    return sum(1 for c in s if ord(c) < 128) / len(s)


def _has_banned(text: str) -> str | None:
    text_l = text.lower()
    for w in DENY:
        if w in text_l:
            return w
    return None


VERIFY_PROMPT = """Read the sentence below and decide which dollar-magnitude
band it most naturally describes. Choose EXACTLY one of:
- billions
- hundreds of millions
- tens of millions
- millions
- hundreds of thousands
- tens of thousands or less

Output ONLY the band label, nothing else.

Sentence: {sentence}
"""


VALID_BANDS = {
    "billions",
    "hundreds of millions",
    "tens of millions",
    "millions",
    "hundreds of thousands",
    "tens of thousands or less",
}


def classify_amount(client, narrative: str) -> str | None:
    """Roundtrip verifier: ask the LLM what band the narrative implies."""
    try:
        r = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[{"role": "user", "content": VERIFY_PROMPT.format(sentence=narrative)}],
            max_tokens=20,
            temperature=0.0,
        )
        out = (r.choices[0].message.content or "").strip().lower().strip(".")
        # find the longest matching band
        for b in sorted(VALID_BANDS, key=len, reverse=True):
            if b in out:
                return b
        return None
    except Exception:
        return None


def rewrite_amount(client, award_id: str, amount: float,
                   recipient: str = "", agency: str = "", naics_desc: str = "",
                   retries: int = 3) -> str | None:
    band = _band(amount)
    last = None
    for attempt in range(retries):
        try:
            r = client.chat.completions.create(
                model=DEPLOYMENT,
                messages=[{"role": "user", "content": PROMPT.format(
                    band=band,
                    recipient=recipient or "(unspecified)",
                    agency=agency or "(unspecified)",
                    naics_desc=naics_desc or "(unspecified)",
                )}],
                max_tokens=120,
                temperature=0.95,
            )
            out = (r.choices[0].message.content or "").strip()
            # Strip wrapping quotes if any
            out = out.strip('"').strip("'")
            if re.search(r"\d", out):
                last = "contains digits"
                continue
            bh = _has_banned(out)
            if bh:
                last = f"banned: {bh!r}"
                continue
            if not _length_ok(out):
                last = f"length {len(out)}"
                continue
            if _ascii_ratio(out) < 0.9:
                last = "non-english"
                continue
            # Roundtrip verification: a second LLM call must classify the
            # narrative back into the same band as the canonical amount.
            implied = classify_amount(client, out)
            if implied != band:
                last = f"verifier disagreed: implied={implied!r} canonical={band!r}"
                continue
            return out
        except Exception as e:
            last = str(e)[:120]
            time.sleep(1.5 ** attempt)
    print(f"  [skip {award_id}] {last}", file=sys.stderr)
    return None


def _ensure_manifest():
    conn = sqlite3.connect(MANIFEST_DB)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS planted_narrative_amount (
      canonical_award_id TEXT PRIMARY KEY,
      canonical_amount REAL,
      narrative TEXT
    );
    """)
    conn.commit()
    conn.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    _ensure_manifest()
    client = _client()

    clean = sqlite3.connect(CLEAN_DB)
    rows = clean.execute(
        "SELECT award_id, amount, recipient_name, awarding_agency, naics_description "
        "FROM contracts "
        "WHERE award_id IS NOT NULL AND amount IS NOT NULL"
    ).fetchall()
    clean.close()
    if args.limit:
        rows = rows[: args.limit]

    mconn = sqlite3.connect(MANIFEST_DB)
    done = {r[0] for r in mconn.execute("SELECT canonical_award_id FROM planted_narrative_amount")}
    mconn.close()
    todo = [r for r in rows if r[0] not in done]
    print(f"Total rows: {len(rows)}; already done: {len(rows)-len(todo)}; todo: {len(todo)}",
          flush=True)

    n_ok = 0
    lock = sqlite3.connect(MANIFEST_DB, isolation_level=None)
    lock.execute("PRAGMA journal_mode=WAL")

    def work(row):
        aid, amt, recipient, agency, naics_desc = row
        out = rewrite_amount(client, aid, float(amt),
                             recipient=recipient or "",
                             agency=agency or "",
                             naics_desc=naics_desc or "")
        return aid, amt, out

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(work, r) for r in todo]
        for i, fut in enumerate(as_completed(futures), 1):
            aid, amt, out = fut.result()
            if out:
                lock.execute(
                    "INSERT OR REPLACE INTO planted_narrative_amount VALUES (?,?,?)",
                    (aid, amt, out),
                )
                n_ok += 1
            if i % 200 == 0:
                print(f"  [{i}/{len(todo)}] ok={n_ok}", flush=True)
    lock.close()
    print(f"DONE: {n_ok}/{len(todo)}")


if __name__ == "__main__":
    main()
