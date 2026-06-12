#!/usr/bin/env python3
"""
Normalize Expert output JSON to the canonical schema.

Real LLM outputs deviate from prompt schemas. This normalizer detects the three
observed variants and maps them to canonical:

  Variant A — canonical (preferred):
    {slide_id, agent_type, expert_fidelity_score, expert_fidelity_cite,
     dilution_flags, naive_match_score, naive_match_cite, recommended_rewrite}

  Variant B — flat but with renamed cite fields ("notes" instead of "cite"):
    {slide_id, agent_type, expert_fidelity_score, expert_fidelity_notes,
     naive_match_score, naive_match_notes, recommended_rewrite, rewrite_rationale, ...}

  Variant C — nested block_a/block_b/verdict structure:
    {slide_id, auditor, block_a: {fidelity_score, fidelity_notes, fabrications, ...},
     block_b: {match_score, verb, stakes, match_notes, ...},
     verdict: {fidelity, match, pass, summary, ...}}

Writes normalized files in-place with a .raw backup of the original.

Usage:  python3 clarity-gate-expert-normalizer.py <run_dir>
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


def normalize_one(d: dict) -> dict:
    """Map any observed shape to canonical schema."""
    out = {"slide_id": d.get("slide_id"), "agent_type": "expert"}

    # Variant C: nested block_a/block_b/verdict
    if "block_a" in d and "block_b" in d:
        a = d.get("block_a", {})
        b = d.get("block_b", {})
        v = d.get("verdict", {})
        out["expert_fidelity_score"] = a.get("fidelity_score") if a.get("fidelity_score") is not None else v.get("fidelity")
        # Cite: prefer fidelity_notes, fall back to verdict.summary
        cite = a.get("fidelity_notes") or v.get("summary") or ""
        out["expert_fidelity_cite"] = cite
        # Dilution flags: collect from any list-shaped field in block_a
        dilutions = []
        for k in ("fabrications", "misattributions", "dilutions", "weasels", "hedges", "flags"):
            v_list = a.get(k)
            if isinstance(v_list, list):
                dilutions.extend(v_list)
        out["dilution_flags"] = dilutions
        # Match score and cite
        out["naive_match_score"] = b.get("match_score") if b.get("match_score") is not None else v.get("match")
        match_notes = b.get("match_notes") or ""
        # Include verb/stakes captured info if available to give substring grounding
        extras = []
        if "verb_captured" in b:
            extras.append(f"verb_captured={b['verb_captured']}")
        if "stakes_captured" in b:
            extras.append(f"stakes_captured={b['stakes_captured']}")
        if extras:
            match_notes = f"{match_notes} [{' '.join(extras)}]"
        out["naive_match_cite"] = match_notes
        # Recommended rewrite: may be in verdict.summary or as separate fields
        rw = d.get("recommended_rewrite") or d.get("rewrite")
        if rw is None and isinstance(v.get("summary"), str) and "rewrite" in v.get("summary", "").lower():
            rw = None  # No clean rewrite available
        out["recommended_rewrite"] = rw

    # Variant B: flat with renamed cite fields
    elif "expert_fidelity_notes" in d or "naive_match_notes" in d:
        out["expert_fidelity_score"] = d.get("expert_fidelity_score")
        out["expert_fidelity_cite"] = d.get("expert_fidelity_notes") or d.get("expert_fidelity_cite") or ""
        out["dilution_flags"] = d.get("dilution_flags") or []
        out["naive_match_score"] = d.get("naive_match_score")
        out["naive_match_cite"] = d.get("naive_match_notes") or d.get("naive_match_cite") or ""
        # Recommended rewrite may be a string or object
        rw = d.get("recommended_rewrite")
        if isinstance(rw, str):
            # String form — convert to object with empty body
            rw = {"headline": rw, "body": ""}
        out["recommended_rewrite"] = rw

    # Variant A: already canonical (just copy verified fields)
    else:
        for k in ("expert_fidelity_score", "expert_fidelity_cite", "dilution_flags",
                  "naive_match_score", "naive_match_cite", "recommended_rewrite"):
            out[k] = d.get(k)

    # Final sanity defaults
    if out.get("dilution_flags") is None:
        out["dilution_flags"] = []
    if not isinstance(out.get("expert_fidelity_cite"), str):
        out["expert_fidelity_cite"] = str(out.get("expert_fidelity_cite") or "")
    if not isinstance(out.get("naive_match_cite"), str):
        out["naive_match_cite"] = str(out.get("naive_match_cite") or "")

    return out


def main(run_dir: str) -> int:
    rd = Path(run_dir)
    if not rd.exists():
        print(f"FATAL: {rd} not found", file=sys.stderr)
        return 2

    expert_files = sorted(rd.glob("slide-*-expert.json"))
    normalized = 0
    untouched = 0
    failures = []

    for f in expert_files:
        raw = json.load(f.open())
        # Detect if already canonical
        is_canonical = (
            "expert_fidelity_cite" in raw
            and "naive_match_cite" in raw
            and "dilution_flags" in raw
            and raw.get("agent_type") == "expert"
            and isinstance(raw.get("expert_fidelity_score"), int)
        )
        if is_canonical:
            untouched += 1
            continue

        try:
            normed = normalize_one(raw)
        except Exception as e:
            failures.append(f"{f.name}: {e}")
            continue

        # Validate result has required fields
        required_int = ["expert_fidelity_score", "naive_match_score"]
        if any(not isinstance(normed.get(k), int) for k in required_int):
            failures.append(f"{f.name}: normalized but missing int scores ({[k for k in required_int if not isinstance(normed.get(k), int)]})")
            continue

        # Backup raw, write normalized
        raw_path = f.with_suffix(".raw.json")
        shutil.copy(f, raw_path)
        with f.open("w") as out:
            json.dump(normed, out, indent=2)
        normalized += 1

    print(f"Normalized: {normalized}")
    print(f"Already canonical: {untouched}")
    if failures:
        print(f"Failures: {len(failures)}", file=sys.stderr)
        for fail in failures:
            print(f"  - {fail}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: clarity-gate-expert-normalizer.py <run_dir>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
