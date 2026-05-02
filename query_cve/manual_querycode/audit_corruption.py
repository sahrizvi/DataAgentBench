"""Roundtrip-audit existing planted narratives in clean/manifest.sqlite.

Calls the LLM classifier on each stored narrative and compares to the canonical
label. Reports the disagreement rate and lists offending rows. Does NOT modify
the manifest — use llm_corrupt.py to regenerate flagged rows.
"""
from __future__ import annotations
import argparse
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DB = ROOT / "clean" / "manifest.sqlite"
sys.path.insert(0, str(ROOT / "scripts"))
from llm_corrupt import _client, classify_severity, classify_score, _score_band  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    client = _client()
    conn = sqlite3.connect(MANIFEST_DB)

    sev_rows = conn.execute(
        "SELECT cve_id, severity, narrative FROM planted_narrative_desc"
    ).fetchall()
    score_rows = conn.execute(
        "SELECT cve_id, canonical_score, narrative FROM planted_narrative_score"
    ).fetchall()
    if args.limit:
        sev_rows = sev_rows[: args.limit]
        score_rows = score_rows[: args.limit]

    print(f"Auditing {len(sev_rows)} severity narratives + {len(score_rows)} score narratives",
          flush=True)

    sev_mismatch = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(classify_severity, client, narr): (cid, sev, narr)
                for (cid, sev, narr) in sev_rows}
        for i, fut in enumerate(as_completed(futs), 1):
            cid, sev, narr = futs[fut]
            implied = fut.result()
            if implied != sev.upper():
                sev_mismatch.append((cid, sev, implied, narr))
            if i % 50 == 0:
                print(f"  severity {i}/{len(sev_rows)}", flush=True)

    score_mismatch = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(classify_score, client, narr): (cid, sc, narr)
                for (cid, sc, narr) in score_rows}
        for i, fut in enumerate(as_completed(futs), 1):
            cid, sc, narr = futs[fut]
            implied = fut.result()
            canonical = _score_band(float(sc))
            if implied != canonical:
                score_mismatch.append((cid, sc, canonical, implied, narr))
            if i % 50 == 0:
                print(f"  score {i}/{len(score_rows)}", flush=True)

    print()
    print(f"Severity mismatches: {len(sev_mismatch)}/{len(sev_rows)} "
          f"({100*len(sev_mismatch)/max(len(sev_rows),1):.1f}%)")
    print(f"Score mismatches:    {len(score_mismatch)}/{len(score_rows)} "
          f"({100*len(score_mismatch)/max(len(score_rows),1):.1f}%)")
    print()
    if sev_mismatch:
        print("Sample severity mismatches (canonical / implied / narrative):")
        for cid, sev, implied, narr in sev_mismatch[:5]:
            print(f"  {cid}: {sev} -> classifier said {implied}")
            print(f"    {narr[:200]}")
            print()
    if score_mismatch:
        print("Sample score mismatches (canonical / implied / narrative):")
        for cid, sc, can, implied, narr in score_mismatch[:5]:
            print(f"  {cid}: score={sc} band={can} -> classifier said {implied}")
            print(f"    {narr[:200]}")
            print()

    # Save offending IDs to a file so llm_corrupt.py can target them
    if sev_mismatch:
        bad_path = ROOT / "clean" / "audit_severity_bad.txt"
        bad_path.write_text("\n".join(c for c, *_ in sev_mismatch))
        print(f"Wrote {len(sev_mismatch)} bad sev cve_ids to {bad_path}")
    if score_mismatch:
        bad_path = ROOT / "clean" / "audit_score_bad.txt"
        bad_path.write_text("\n".join(c for c, *_ in score_mismatch))
        print(f"Wrote {len(score_mismatch)} bad score cve_ids to {bad_path}")


if __name__ == "__main__":
    main()
