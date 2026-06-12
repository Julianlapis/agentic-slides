#!/usr/bin/env python3
"""
Inferential-detector — regex layer.

Hybrid implementation per build plan Phase F step 13. This script handles the
TWO regex-tractable markers from i-need-you-to-shiny-kahan.md §17:

  1. Causal language: words that assert a mechanism not stated in the original
     slide. Examples: 'because', 'drives', 'explains'.

  2. Standing / positioning assertions: copy that claims a firm has rare or
     unique position. Examples: 'uniquely positioned', 'alone among peers'.

The THIRD marker — named entities present in the rewrite but absent in the
original slide content — requires comparing two text blocks. That cannot be
done well with regex (a regex for 'name' false-positives on every capitalized
noun). The named-entity check lives in
`~/.claude/commands/agentic-slides/agents/inferential-detector.md` and fires
ONLY on rewrites this regex layer didn't already flag.

Usage:
  python3 inferential-detector.py --rewrite-text "<text>"
  python3 inferential-detector.py --aggregate <path>           # batch over aggregate.json's recommended_rewrite fields
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Causal language — assertions of mechanism.
CAUSAL_PATTERNS = [
    (re.compile(r"\bbecause\b", re.I), "because"),
    (re.compile(r"\bdrives?\b", re.I), "drives"),
    (re.compile(r"\bexplains?\b", re.I), "explains"),
    (re.compile(r"\bcauses?\b", re.I), "causes"),
    (re.compile(r"\bforces?\b", re.I), "forces"),
    (re.compile(r"\btriggers?\b", re.I), "triggers"),
    (re.compile(r"\bthe reason\b", re.I), "the reason"),
    (re.compile(r"\bdue to\b", re.I), "due to"),
    (re.compile(r"\bas a result\b", re.I), "as a result"),
]

# Standing / positioning assertions — claims about competitive position.
STANDING_PATTERNS = [
    (re.compile(r"\brare standing\b", re.I), "rare standing"),
    (re.compile(r"\buniquely positioned\b", re.I), "uniquely positioned"),
    (re.compile(r"\balone among peers\b", re.I), "alone among peers"),
    (re.compile(r"\bthe only\b", re.I), "the only"),
    (re.compile(r"\bfirst to\b", re.I), "first to"),
    (re.compile(r"\bsole (?:provider|firm|player|carrier|owner|holder)\b", re.I), "sole [role]"),
    (re.compile(r"\bno other firm\b", re.I), "no other firm"),
    (re.compile(r"\bunmatched\b", re.I), "unmatched"),
    (re.compile(r"\bunique standing\b", re.I), "unique standing"),
]


def scan_text(text: str) -> dict:
    """Return regex_flagged + markers_found for one rewrite text."""
    if not isinstance(text, str) or not text.strip():
        return {"regex_flagged": False, "markers_found": [], "reason": "empty input"}

    found: list[dict] = []
    for pattern, label in CAUSAL_PATTERNS:
        for m in pattern.finditer(text):
            found.append({"marker_class": "causal", "marker": label, "match": m.group(0), "position": m.start()})
    for pattern, label in STANDING_PATTERNS:
        for m in pattern.finditer(text):
            found.append({"marker_class": "standing", "marker": label, "match": m.group(0), "position": m.start()})

    return {"regex_flagged": bool(found), "markers_found": found}


def scan_rewrite_struct(rewrite: dict | None) -> dict:
    if not isinstance(rewrite, dict):
        return {"regex_flagged": False, "markers_found": [], "reason": "no rewrite"}
    combined = " ".join(str(rewrite.get(k, "")) for k in ("headline", "body"))
    return scan_text(combined)


def main_text(text: str) -> int:
    print(json.dumps(scan_text(text), indent=2))
    return 0


def main_aggregate(aggregate_path: str) -> int:
    p = Path(aggregate_path)
    if not p.exists():
        print(f"FATAL: {p} missing", file=sys.stderr)
        return 2
    aggregate = json.loads(p.read_text())
    results = []
    for row in aggregate.get("matrix", []):
        result = scan_rewrite_struct(row.get("recommended_rewrite"))
        results.append({"slide_id": row["slide_id"], **result})
    print(json.dumps({"count": len(results), "flagged_count": sum(1 for r in results if r.get("regex_flagged")), "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--rewrite-text", help="Single rewrite text to scan")
    grp.add_argument("--aggregate", help="Path to aggregate.json — batch-scan all matrix rewrites")
    args = ap.parse_args()
    if args.rewrite_text is not None:
        sys.exit(main_text(args.rewrite_text))
    sys.exit(main_aggregate(args.aggregate))
