#!/usr/bin/env python3
"""
Per-slide clarity-gate aggregator. Deterministic. No LLM.

Reads .clarity-gate/run-{ts}/ directory, validates schemas, builds the matrix,
computes pass rates, and writes aggregate.json.

Refuses to score if:
- Manifest declared N slides but observed file count != 2N + manifest
- Any per-slide output fails schema validation
- Any score is outside [0,3]
- Expert citation doesn't ground in Naive text (cross-check)

v1.2 additions:
- Cold-context audit on Naive (tool_calls_made must = [Write] only)
- recommended_rewrite source-check: extracts precision claims (percentages,
  dollar figures, specific dates) from every recommended rewrite and surfaces
  them in aggregate.json for verification. Driven by a prior pitch-run finding that
  gate Expert agents can confabulate precision inside rewrites (S09 70-80%
  REDACTED stat caught by pressure-test).

Usage:  python3 clarity-gate-aggregator.py <run_dir>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NAIVE_REQUIRED = [
    "slide_id", "agent_type", "guess_main_point", "evidence_named",
    "confusions", "confidence",
    # v1.1 cold-context audit field — list of tool calls the Naive agent made.
    # Must be exactly [{"tool": "Write", "path": "<output_path>"}]. Any extra entries
    # mark the slide un-judged.
    "tool_calls_made",
]
EXPERT_REQUIRED = [
    "slide_id", "agent_type",
    # Block A — fidelity rated BEFORE Naive's guess is read.
    "expert_fidelity_score", "expert_fidelity_cite", "dilution_flags",
    # Block B — Naive match rated AFTER reading Naive's guess.
    "naive_match_score", "naive_match_cite",
    "recommended_rewrite",
]


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def validate_naive(obj: dict, path: Path) -> list[str]:
    errs = []
    for k in NAIVE_REQUIRED:
        if k not in obj:
            errs.append(f"{path.name}: missing key '{k}'")
    if obj.get("agent_type") != "naive":
        errs.append(f"{path.name}: agent_type != 'naive'")
    # Cold-context audit — Naive must have called exactly one Write tool.
    tcm = obj.get("tool_calls_made")
    if isinstance(tcm, list):
        write_calls = [c for c in tcm if isinstance(c, dict) and c.get("tool") == "Write"]
        non_write_calls = [c for c in tcm if isinstance(c, dict) and c.get("tool") != "Write"]
        if non_write_calls:
            errs.append(
                f"{path.name}: cold-context violation — Naive called non-Write tools: {non_write_calls}"
            )
        if len(write_calls) != 1:
            errs.append(
                f"{path.name}: expected exactly 1 Write call, found {len(write_calls)}"
            )
    return errs


def validate_expert(obj: dict, path: Path) -> list[str]:
    errs = []
    for k in EXPERT_REQUIRED:
        if k not in obj:
            errs.append(f"{path.name}: missing key '{k}'")
    if obj.get("agent_type") != "expert":
        errs.append(f"{path.name}: agent_type != 'expert'")
    for k in ("naive_match_score", "expert_fidelity_score"):
        v = obj.get(k)
        if not isinstance(v, int) or v < 0 or v > 3:
            errs.append(f"{path.name}: {k}={v} outside [0,3]")
    return errs


# v1.2 source-check patterns — extract precision claims from rewrites
PRECISION_PATTERNS = [
    # Percentages: "80%", "70-80%", "+2 YoY"
    (re.compile(r"(?<!\w)(\d+(?:[.\-–]\d+)?%)"), "percentage"),
    # Dollar amounts: "$686B", "$1.66T", "$124 trillion", "$46T"
    (re.compile(r"\$\d+(?:[.,]\d+)?\s*(?:trillion|billion|million|[KMBT])(?!\w)", re.I), "dollar_amount"),
    # Basis points: "263 bps", "37.4 bps"
    (re.compile(r"\d+(?:\.\d+)?\s*(?:bps|basis points)", re.I), "basis_points"),
    # Specific dates: "February 25, 2026", "November 28, 2025", "January 2025"
    (re.compile(r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,?\s+\d{4})?", re.I), "specific_date"),
    # Year-over-year specifics: "FY2025", "Q1 FY2026", "Q4 2024"
    (re.compile(r"\b(?:FY|Q[1-4]\s*(?:FY)?)\d{2,4}\b"), "fiscal_period"),
]


def load_memory(memory_path: str | None = None) -> list[tuple[re.Pattern, str]]:
    """Load skill-level failure mechanisms and return entries shaped to extend PRECISION_PATTERNS.

    v2 stub — empty hook per locked plan §25.1 / build plan Phase B step 4.
    Step 7 of the v2 build (separate session, requires 2-4 weeks of production
    runs to observe compounding) will fill in the body to read
    `~/.claude/commands/agentic-slides/memory/known-failure-mechanisms.json`,
    compile each entry's `regex_signature`, and pair it with `claim_type` as kind.

    Today this returns []. The runtime extension below is therefore a no-op, but
    the call site is wired so step 7 fills in the body without changing any caller.
    """
    if memory_path is None:
        return []
    p = Path(memory_path)
    if not p.exists():
        return []
    # Body intentionally empty until Step 7. Returning [] keeps PRECISION_PATTERNS unchanged.
    return []


# Extend PRECISION_PATTERNS with any skill-level mechanism rules. Today this is
# a no-op because load_memory() returns []. Wired here so Step 7 lights it up
# without touching the rest of the aggregator.
# TODO Step 7: when load_memory() reads the memory file, move this extend() call
# INTO main() instead of running at module load. Module-level extend means every
# `import clarity_gate_aggregator` (e.g., source-verifier's dynamic import) will
# trigger a disk read at import time — surprising side-effect, hard to mock in tests.
PRECISION_PATTERNS.extend(load_memory())


def extract_precision_claims(text: str) -> list[dict]:
    """Extract numeric/specific claims that a fact-checker would want to verify."""
    if not isinstance(text, str):
        return []
    claims: list[dict] = []
    seen: set[str] = set()
    for pattern, kind in PRECISION_PATTERNS:
        for match in pattern.finditer(text):
            value = match.group(0)
            key = f"{kind}:{value.lower()}"
            if key in seen:
                continue
            seen.add(key)
            claims.append({"kind": kind, "value": value})
    return claims


def source_check_rewrite(rewrite, slide_content_text: str) -> list[dict]:
    """Compare precision claims in rewrite against slide content. Flag claims
    that don't appear in the slide content as needing verification."""
    if not rewrite or not isinstance(rewrite, dict):
        return []
    rewrite_text = " ".join(
        [str(rewrite.get("headline", "")), str(rewrite.get("body", ""))]
    )
    claims = extract_precision_claims(rewrite_text)
    if not claims:
        return []
    slide_lower = (slide_content_text or "").lower()
    unverified: list[dict] = []
    for claim in claims:
        if claim["value"].lower() not in slide_lower:
            unverified.append({**claim, "status": "NOT_IN_SLIDE_CONTENT — verify against dossier"})
    return unverified


def verdict_for_slide(naive_match: int, expert_fidelity: int) -> str:
    if naive_match == 0 or expert_fidelity == 0:
        return "CRITICAL — redraft entirely"
    if naive_match >= 2 and expert_fidelity >= 2:
        if naive_match == 3 and expert_fidelity == 3:
            return "SHIP"
        return "SHIP (with minor tightening)"
    if naive_match < 2 and expert_fidelity >= 2:
        return "RIGHT-BUT-UNCLEAR — rewrite for clarity"
    if naive_match >= 2 and expert_fidelity < 2:
        return "CLEAR-BUT-DILUTED — rewrite for fidelity"
    return "BROKEN — full slide rewrite"


def main(run_dir: str) -> int:
    rd = Path(run_dir)
    if not rd.exists():
        print(f"FATAL: run directory {rd} does not exist", file=sys.stderr)
        return 2

    manifest_path = rd / "run-manifest.json"
    if not manifest_path.exists():
        print("FATAL: run-manifest.json missing — refusing to score", file=sys.stderr)
        return 2

    manifest = load_json(manifest_path)
    expected = manifest["expected_agent_spawns"]
    slides_in_scope = manifest["slides_in_scope"]
    slide_count = manifest["slide_count"]

    naive_files = sorted(rd.glob("slide-*-naive.json"))
    expert_files = sorted(rd.glob("slide-*-expert.json"))
    total = len(naive_files) + len(expert_files)
    if total != expected:
        print(f"FATAL: expected {expected} agent outputs, found {total} — tampering or partial run", file=sys.stderr)
        return 3

    errors: list[str] = []
    by_slide: dict[str, dict] = {}

    for path in naive_files:
        obj = load_json(path)
        errors.extend(validate_naive(obj, path))
        sid = obj.get("slide_id")
        by_slide.setdefault(sid, {})["naive"] = obj
        by_slide[sid]["naive_path"] = str(path)

    for path in expert_files:
        obj = load_json(path)
        errors.extend(validate_expert(obj, path))
        sid = obj.get("slide_id")
        by_slide.setdefault(sid, {})["expert"] = obj
        by_slide[sid]["expert_path"] = str(path)

    if errors:
        print("SCHEMA ERRORS:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 4

    for sid in slides_in_scope:
        if sid not in by_slide or "naive" not in by_slide[sid] or "expert" not in by_slide[sid]:
            print(f"FATAL: missing pair for {sid}", file=sys.stderr)
            return 5

    # Cross-check: Expert's naive_match_cite must reference Naive's guess.
    # Either it quotes a meaningful substring (>=15 chars) of guess_main_point,
    # OR it states explicitly that Naive missed a specific argument component.
    cross_check_failures: list[str] = []
    for sid in slides_in_scope:
        naive_guess = by_slide[sid]["naive"]["guess_main_point"]
        expert_cite = by_slide[sid]["expert"]["naive_match_cite"]
        if not isinstance(expert_cite, str) or not isinstance(naive_guess, str):
            cross_check_failures.append(f"{sid}: cite or guess is not a string")
            continue
        # Three acceptance paths:
        # (1) Expert cite contains an n-gram (4-8 words, >=15 chars) from Naive's guess.
        # (2) Expert cite contains any 20+ char verbatim substring of Naive's guess.
        # (3) Expert cite contains explicit discussion phrases about Naive's framing.
        guess_lower = naive_guess.lower()
        cite_lower = expert_cite.lower()
        guess_words = guess_lower.split()
        ngram_hit = False
        for n in (8, 6, 4):
            for i in range(len(guess_words) - n + 1):
                ngram = " ".join(guess_words[i:i + n])
                if len(ngram) >= 15 and ngram in cite_lower:
                    ngram_hit = True
                    break
            if ngram_hit:
                break
        # Sliding substring (catches verbatim quotes of multi-word phrases regardless of word count)
        substring_hit = False
        for L in (40, 30, 20):
            for i in range(len(guess_lower) - L + 1):
                chunk = guess_lower[i:i + L].strip()
                if len(chunk) >= L and chunk in cite_lower:
                    substring_hit = True
                    break
            if substring_hit:
                break
        # Allow explicit framings as valid cites
        explicit_miss = any(
            phrase in cite_lower
            for phrase in (
                "miss", "lack", "absent", "does not capture", "did not capture",
                "without naming", "without surfacing", "fails to", "instead of",
                "rather than", "narrower", "captures", "captured", "naive",
                "stranger", "the headline", "verb_captured", "stakes_captured",
            )
        )
        if not ngram_hit and not substring_hit and not explicit_miss:
            cross_check_failures.append(
                f"{sid}: expert.naive_match_cite does not quote naive.guess_main_point "
                f"and does not explicitly name a missing argument component"
            )

    if cross_check_failures:
        print("CROSS-CHECK FAILURES (Expert cites do not ground in Naive's text):", file=sys.stderr)
        for f in cross_check_failures:
            print(f"  - {f}", file=sys.stderr)
        return 7

    rows = []
    naive_scores: list[int] = []
    expert_scores: list[int] = []
    critical: list[str] = []

    for sid in slides_in_scope:
        e = by_slide[sid]["expert"]
        n_match = e["naive_match_score"]
        e_fid = e["expert_fidelity_score"]
        naive_scores.append(n_match)
        expert_scores.append(e_fid)
        v = verdict_for_slide(n_match, e_fid)
        if "CRITICAL" in v or "BROKEN" in v:
            critical.append(sid)
        # v1.2 source-check: extract precision claims in rewrite that don't
        # appear in Naive's evidence_named or guess_main_point.
        slide_context = " ".join(
            [
                str(by_slide[sid]["naive"].get("guess_main_point", "")),
                " ".join(str(x) for x in by_slide[sid]["naive"].get("evidence_named", [])),
            ]
        )
        rewrite_unverified = source_check_rewrite(e.get("recommended_rewrite"), slide_context)

        rows.append({
            "slide_id": sid,
            "naive_match": n_match,
            "expert_fidelity": e_fid,
            "verdict": v,
            "naive_guess": by_slide[sid]["naive"]["guess_main_point"],
            "dilution_flags": e["dilution_flags"],
            "recommended_rewrite": e["recommended_rewrite"],
            "rewrite_precision_to_verify": rewrite_unverified,
            "naive_path": by_slide[sid]["naive_path"],
            "expert_path": by_slide[sid]["expert_path"],
        })

    clarity_pass = sum(1 for s in naive_scores if s >= 2) / slide_count
    fidelity_pass = sum(1 for s in expert_scores if s >= 2) / slide_count
    composite = (sum(naive_scores) + sum(expert_scores)) / (6 * slide_count) * 100

    deck_verdict = "SHIPS"
    if critical:
        deck_verdict = "CRITICAL FAILURES — slides require redraft"
    elif clarity_pass < 0.7 or fidelity_pass < 0.7:
        deck_verdict = "REDRAFT DECK — clarity or fidelity below 70%"
    elif clarity_pass < 0.9 or fidelity_pass < 0.9:
        deck_verdict = "REWRITE SPECIFIC SLIDES — clarity or fidelity 70-90%"

    # v1.2 source-check rollup: how many rewrites contain precision claims not
    # in slide content?
    rewrites_with_unverified = [r for r in rows if r.get("rewrite_precision_to_verify")]

    out = {
        "run_id": manifest["run_id"],
        "deck_id": manifest["deck_id"],
        "deck_snapshot_sha256": manifest["deck_snapshot_sha256"],
        "slides_in_scope": slides_in_scope,
        "slide_count": slide_count,
        "clarity_pass_rate": clarity_pass,
        "fidelity_pass_rate": fidelity_pass,
        "composite_health": composite,
        "critical_failures": critical,
        "deck_verdict": deck_verdict,
        "rewrite_source_check": {
            "slides_with_unverified_precision": [r["slide_id"] for r in rewrites_with_unverified],
            "count": len(rewrites_with_unverified),
            "note": "Each rewrite below contains numeric/specific claims that do NOT appear in the slide's Naive guess or evidence_named. Verify against dossier before applying rewrite. Driven by a prior pitch-run finding — gate Expert agents can confabulate precision inside fixes (e.g., an invented 70-80% stat in a rewrite).",
        },
        "matrix": rows,
    }

    aggregate_path = rd / "aggregate.json"
    with aggregate_path.open("w") as f:
        json.dump(out, f, indent=2)

    print(f"WROTE: {aggregate_path}")
    print(f"Clarity pass: {clarity_pass*100:.1f}%  |  Fidelity pass: {fidelity_pass*100:.1f}%  |  Composite: {composite:.1f}")
    print(f"Verdict: {deck_verdict}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: clarity-gate-aggregator.py <run_dir>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
