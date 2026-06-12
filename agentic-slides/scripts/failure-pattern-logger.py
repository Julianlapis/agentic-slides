#!/usr/bin/env python3
"""
Pipeline link 5 — failure-pattern-logger.

Reads a clarity-gate run's outputs and extracts new failure mechanisms caught
this run. Writes to two memory layers:

  - Skill-level: ~/.claude/commands/agentic-slides/memory/known-failure-mechanisms.json
    Typed entries with regex_signature. Deduplicated by id. Loaded by the
    aggregator at startup (currently a no-op stub; Step 7 lights it up).

  - Project-level: <project>/.clarity-gate/known-failure-patterns.json
    Instance hints with expert_hint text. Injected into the Expert prompt for
    THIS project on subsequent gate runs. Scoped to the project.

The logger reads:
  - aggregate.json (always present)
  - source-verification.json (if present)
  - rewrite-pressure-test.json (if present)

When upstream files are absent (e.g., the logger is run before the source-verifier
or pressure-tester exist), it gracefully no-ops on those branches. Phase D of the
v2 build exercises exactly this "only aggregate.json" path.

Usage:  python3 failure-pattern-logger.py <run_dir>
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

SKILL_MEMORY = Path.home() / ".claude/commands/agentic-slides/memory/known-failure-mechanisms.json"

REQUIRED_MECHANISM_FIELDS = (
    "id", "claim_type", "regex_signature", "mechanism_description",
    "first_caught", "aggregator_action", "severity",
)
REQUIRED_FIRST_CAUGHT_FIELDS = ("project_anon", "slide_id", "date", "specific_value")


def validate_mechanism(m: dict) -> list[str]:
    errs = []
    for k in REQUIRED_MECHANISM_FIELDS:
        if k not in m:
            errs.append(f"missing field '{k}'")
    fc = m.get("first_caught")
    if not isinstance(fc, dict):
        errs.append("first_caught must be a dict")
    else:
        for k in REQUIRED_FIRST_CAUGHT_FIELDS:
            if k not in fc:
                errs.append(f"first_caught missing '{k}'")
    if m.get("severity") not in ("LOW", "MEDIUM", "HIGH"):
        errs.append(f"severity must be LOW/MEDIUM/HIGH, got {m.get('severity')!r}")
    return errs


def load_skill_memory() -> dict:
    if not SKILL_MEMORY.exists():
        return {"schema_version": "1.0", "mechanisms": []}
    return json.loads(SKILL_MEMORY.read_text())


def write_skill_memory(data: dict) -> None:
    SKILL_MEMORY.parent.mkdir(parents=True, exist_ok=True)
    SKILL_MEMORY.write_text(json.dumps(data, indent=2) + "\n")


def next_mechanism_id(existing: list[dict]) -> str:
    nums = [int(m["id"][1:]) for m in existing if isinstance(m.get("id"), str) and m["id"].startswith("M") and m["id"][1:].isdigit()]
    return f"M{max(nums) + 1:03d}" if nums else "M001"


def append_skill_mechanism(mechanism: dict) -> tuple[bool, list[str]]:
    """Append a mechanism if its (claim_type, regex_signature) is novel. Returns (was_added, errors)."""
    errs = validate_mechanism(mechanism)
    if errs:
        return False, errs
    data = load_skill_memory()
    existing = data["mechanisms"]
    for m in existing:
        if m.get("claim_type") == mechanism["claim_type"] and m.get("regex_signature") == mechanism["regex_signature"]:
            return False, []   # dedup hit, not an error
    existing.append(mechanism)
    write_skill_memory(data)
    return True, []


def extract_mechanisms_from_run(run_dir: Path) -> list[dict]:
    """Survey aggregate.json + optional upstream files for new failure mechanisms.

    Today this is a thin extractor. As the pipeline matures, this function grows
    pattern-recognition heuristics (e.g., 'every rewrite_precision_to_verify with
    a percentage range → emit M001-class candidate'). For now it surfaces the
    structured shape so subsequent runs can fold new mechanisms in by hand or
    via dedicated diagnostic agents.
    """
    candidates: list[dict] = []
    agg_path = run_dir / "aggregate.json"
    if not agg_path.exists():
        return candidates
    aggregate = json.loads(agg_path.read_text())
    deck_id = aggregate.get("deck_id", "unknown-deck")

    # 1. aggregate.json signal: any slide with rewrite_precision_to_verify is
    # a candidate instance of M001-class confabulation.
    for row in aggregate.get("matrix", []):
        unverified = row.get("rewrite_precision_to_verify") or []
        if unverified:
            for claim in unverified:
                candidates.append({
                    "source": "aggregate.rewrite_precision_to_verify",
                    "slide_id": row["slide_id"],
                    "deck_id": deck_id,
                    "claim_kind": claim.get("kind"),
                    "claim_value": claim.get("value"),
                    "note": "Candidate numeric_confabulation_in_rewrites instance — review for new regex_signature.",
                })

    # 2. source-verification.json signal (if present): mismatch citations.
    sv_path = run_dir / "source-verification.json"
    if sv_path.exists():
        sv = json.loads(sv_path.read_text())
        for slide_entry in sv if isinstance(sv, list) else sv.get("slides", []):
            for citation in slide_entry.get("citations", []):
                if citation.get("fetch_status") == "mismatch":
                    candidates.append({
                        "source": "source-verification.mismatch",
                        "slide_id": slide_entry.get("slide_id"),
                        "deck_id": deck_id,
                        "citation": citation.get("text") or citation.get("url"),
                        "note": "Candidate paraphrase_as_verbatim_quote instance — review for project-level expert_hint.",
                    })

    # 3. rewrite-pressure-test.json signal (if present): surviving fixes.
    rpt_path = run_dir / "rewrite-pressure-test.json"
    if rpt_path.exists():
        rpt = json.loads(rpt_path.read_text())
        for verdict in rpt if isinstance(rpt, list) else rpt.get("verdicts", []):
            if verdict.get("status") == "surviving_fix":
                candidates.append({
                    "source": "pressure-test.surviving_fix",
                    "slide_id": verdict.get("slide_id"),
                    "deck_id": deck_id,
                    "objection": verdict.get("objection"),
                    "note": "Candidate inferential_overclaim instance — review for new aggregator pattern.",
                })

    return candidates


def write_project_patterns(run_dir: Path, candidates: list[dict]) -> Path | None:
    """Write candidates as project-scoped instance hints (next-run Expert prompt fuel)."""
    if not candidates:
        return None
    # Project root is two levels up from the clarity-gate run dir.
    project_clarity_gate = run_dir.parent
    target = project_clarity_gate / "known-failure-patterns.json"
    existing = {"schema_version": "1.0", "project_id": project_clarity_gate.parent.name, "patterns": []}
    if target.exists():
        existing = json.loads(target.read_text())
    existing_keys = {(p.get("claim_type"), p.get("instance")) for p in existing.get("patterns", [])}
    today = date.today().isoformat()
    next_p = max([int(p["id"][1:]) for p in existing.get("patterns", []) if isinstance(p.get("id"), str) and p["id"].startswith("P") and p["id"][1:].isdigit()] or [0]) + 1

    added = 0
    for c in candidates:
        claim_type = c["source"].split(".")[-1] + "_candidate"
        instance = f"{c.get('claim_kind') or c.get('citation') or c.get('objection') or 'unknown'} @ {c['slide_id']}"
        if (claim_type, instance) in existing_keys:
            continue
        existing["patterns"].append({
            "id": f"P{next_p:03d}",
            "claim_type": claim_type,
            "instance": instance,
            "first_caught": {"slide_id": c["slide_id"], "date": today},
            "expert_hint": c["note"],
        })
        next_p += 1
        added += 1

    target.write_text(json.dumps(existing, indent=2) + "\n")
    print(f"  project-level: +{added} pattern(s) written to {target}")
    return target


def main(run_dir_str: str) -> int:
    run_dir = Path(run_dir_str)
    if not (run_dir / "aggregate.json").exists():
        print(f"FATAL: aggregate.json missing in {run_dir}", file=sys.stderr)
        return 2

    candidates = extract_mechanisms_from_run(run_dir)
    print(f"Surveyed run {run_dir.name}: {len(candidates)} candidate instance(s) found")
    for c in candidates:
        print(f"  - {c['source']:40s} | {c.get('slide_id'):8s} | {c.get('claim_value') or c.get('citation') or c.get('objection')}")

    # Skill-level memory write happens via append_skill_mechanism() — but new
    # mechanism PROMOTION from candidate → typed regex_signature is a human
    # judgment step (a candidate isn't a mechanism until we can write a regex
    # that catches the class, not just this instance). Project-level patterns
    # auto-write since they're instance hints, not class generalizations.
    project_target = write_project_patterns(run_dir, candidates)

    (run_dir / "patterns-logged.json").write_text(json.dumps({
        "candidates": candidates,
        "skill_memory_updates": 0,
        "project_patterns_written_to": str(project_target) if project_target else None,
        "note": "Skill-level mechanism promotion requires human review. Project-level instance hints written automatically.",
    }, indent=2))
    print(f"WROTE: {run_dir / 'patterns-logged.json'}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: failure-pattern-logger.py <run_dir>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
