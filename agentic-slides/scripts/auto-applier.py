#!/usr/bin/env python3
# STAGE-ONLY MODE. Do not flip LIVE_APPLY = True until:
#   (a) you have read pending-apply.diff from the most recent run end-to-end,
#   (b) every staged edit matches a recommended_rewrite entry in aggregate.json,
#   (c) no source-check mismatch or pressure-test surviving_fix was silently passed.
# Reference: ~/.claude/commands/agentic-slides/references/v2-pipeline.md §auto-applier-promotion
"""
Pipeline link 4 — auto-applier.

Reads a clarity-gate run's aggregate.json and stages (or applies, when LIVE_APPLY)
rewrites that survived all upstream checks. Pre-flight asserts the deck file's
sha256 matches the manifest's snapshot — halts on state drift.

Stage-only behavior: writes proposed edits to pending-apply.diff. Does NOT
modify the canonical deck file. Pre/post snapshots still run.

Usage:  python3 auto-applier.py <run_dir>
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

LIVE_APPLY = False   # promotion gate — see header comment + v2-pipeline.md §auto-applier-promotion


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# Slide block extraction — mirrored verbatim in source-verifier.py.
# If you change this function, change the twin in source-verifier.py at the same time.
# Intentional duplication per plan §C (let-s-pick-this-up-functional-ember.md): two CLI tools, ~15 lines, simplicity > premature extraction.
# Trigger to extract into deck_utils.py: when a third script needs the same logic.
def slide_id_to_marker_candidates(slide_id: str) -> list[str]:
    """Manifest 'S10C' may appear as 'Slide 10C' or 'Slide 10b' in deck. Try both."""
    digits = re.sub(r"^S", "", slide_id)
    m = re.match(r"^(\d+)([A-Za-z]*)$", digits)
    if not m:
        return [f"## Slide {digits}:"]
    num, suffix = m.group(1), m.group(2)
    out = [f"## Slide {int(num)}{suffix}:"]
    if suffix.lower() == "c":
        out.append(f"## Slide {int(num)}b:")
    return out


def extract_slide_block(deck_text: str, slide_id: str) -> str | None:
    """Return the markdown block for a slide (from its header to the next `---` or next `## Slide`)."""
    for marker in slide_id_to_marker_candidates(slide_id):
        start = deck_text.find(marker)
        if start == -1:
            continue
        rest = deck_text[start:]
        end_rule = rest.find("\n---\n")
        end_next = rest.find("\n## Slide ", 1)
        candidates = [e for e in (end_rule, end_next) if e != -1]
        if not candidates:
            return rest
        return rest[: min(candidates)]
    return None


def field_line(block: str, field: str) -> str | None:
    """Find a `- **Field:** ...` line in a slide block. Returns the full line or None.

    Tolerates parenthesized qualifiers: `**Body (under stats):**` matches field=Body.
    The deck file uses these variants for layout context."""
    # Try exact match first
    pattern_exact = re.compile(rf"^- \*\*{re.escape(field)}:\*\* .*$", re.MULTILINE)
    m = pattern_exact.search(block)
    if m:
        return m.group(0)
    # Fallback: tolerate `**Field (qualifier):**`
    pattern_loose = re.compile(rf"^- \*\*{re.escape(field)}\s*\([^)]+\):\*\* .*$", re.MULTILINE)
    m = pattern_loose.search(block)
    return m.group(0) if m else None


def stage_rewrite(row: dict, deck_text: str, run_dir: Path) -> dict:
    """Produce snapshot files + diff entry for one rewrite. Returns log entry."""
    slide_id = row["slide_id"]
    rewrite = row.get("recommended_rewrite") or {}
    new_headline = rewrite.get("headline")
    new_body = rewrite.get("body")

    block = extract_slide_block(deck_text, slide_id)
    if block is None:
        return {"slide_id": slide_id, "status": "skipped", "reason": "slide marker not found in deck"}

    old_headline_line = field_line(block, "Headline")
    old_body_line = field_line(block, "Body")
    if not old_headline_line or not old_body_line:
        return {"slide_id": slide_id, "status": "skipped", "reason": "missing Headline or Body field in slide block"}

    edits = []
    if new_headline:
        edits.append({"field": "Headline", "old": old_headline_line, "new": f"- **Headline:** {new_headline}"})
    if new_body:
        edits.append({"field": "Body", "old": old_body_line, "new": f"- **Body:** {new_body}"})

    # Pre/post snapshots — exist in both modes so the audit trail is identical.
    snapshot_pre = run_dir / f"pre-apply-snapshot-{slide_id}.json"
    snapshot_post = run_dir / f"post-apply-snapshot-{slide_id}.json"
    snapshot_pre.write_text(json.dumps({"slide_id": slide_id, "headline_line": old_headline_line, "body_line": old_body_line}, indent=2))
    post_state = {"slide_id": slide_id, "edits": edits, "live_apply": LIVE_APPLY}
    snapshot_post.write_text(json.dumps(post_state, indent=2))

    if LIVE_APPLY:
        return {"slide_id": slide_id, "status": "would_apply_live", "edits": edits,
                "note": "LIVE_APPLY=True — Edit tool invocation belongs to orchestrator, not this script."}
    return {"slide_id": slide_id, "status": "staged", "edits": edits}


def _assert_safe_deck_path(deck_path: Path, run_dir: Path) -> None:
    """Reject path traversal. deck_path must resolve under the project root that
    contains run_dir and must end in .md. Same guard as source-verifier._assert_safe_deck_path."""
    resolved = deck_path.resolve()
    if resolved.suffix.lower() != ".md":
        raise ValueError(f"deck_path {resolved} is not a .md file")
    project_root = run_dir.resolve().parent.parent
    try:
        resolved.relative_to(project_root)
    except ValueError:
        raise ValueError(f"deck_path {resolved} is not inside project root {project_root}")


def _pressure_test_halted(run_dir: Path) -> str | None:
    """Inspect rewrite-pressure-test.json (if present) for a halt signal from link 3.
    Absence of the file is fine — it means link 3 didn't fire (no qualifying rewrites).
    Returns reason or None."""
    rpt_path = run_dir / "rewrite-pressure-test.json"
    if not rpt_path.exists():
        return None
    try:
        rpt = json.loads(rpt_path.read_text())
    except json.JSONDecodeError as e:
        return f"rewrite-pressure-test.json is malformed: {e}"
    halt = rpt.get("halt_reasons") or []
    if halt:
        return f"pressure-tester halt: {halt}"
    return None


def main(run_dir_str: str) -> int:
    run_dir = Path(run_dir_str)
    aggregate_path = run_dir / "aggregate.json"
    manifest_path = run_dir / "run-manifest.json"
    if not aggregate_path.exists() or not manifest_path.exists():
        print(f"FATAL: aggregate.json or run-manifest.json missing in {run_dir}", file=sys.stderr)
        return 2

    aggregate = json.loads(aggregate_path.read_text())
    manifest = json.loads(manifest_path.read_text())

    # Halt cascade from link 3 — if pressure-tester surfaced surviving fixes, do not stage.
    halt = _pressure_test_halted(run_dir)
    if halt:
        print(f"FATAL: {halt}", file=sys.stderr)
        log = {"hash_check": "skipped", "halt_reason": halt}
        (run_dir / "auto-apply-log.json").write_text(json.dumps(log, indent=2))
        return 4

    deck_path = Path(manifest["deck_path"])
    try:
        _assert_safe_deck_path(deck_path, run_dir)
    except ValueError as e:
        print(f"FATAL: unsafe deck_path — {e}", file=sys.stderr)
        return 2
    expected_hash = manifest["deck_snapshot_sha256"]
    actual_hash = sha256_file(deck_path)
    if actual_hash != expected_hash:
        log = {"hash_check": "FAIL", "expected": expected_hash, "actual": actual_hash, "deck_path": str(deck_path),
               "halt_reason": "deck-hash drift between gate run and apply (state drift, §25.2)"}
        (run_dir / "auto-apply-log.json").write_text(json.dumps(log, indent=2))
        print("FATAL: deck-hash drift — refusing to apply", file=sys.stderr)
        return 3

    deck_text = deck_path.read_text()
    pending_diff_lines: list[str] = [f"# pending-apply.diff for run {manifest['run_id']}\n# LIVE_APPLY={LIVE_APPLY}\n# deck={deck_path}\n"]
    log_entries: list[dict] = []

    for row in aggregate["matrix"]:
        if row.get("naive_match", 0) < 2 or row.get("expert_fidelity", 0) < 2:
            log_entries.append({"slide_id": row["slide_id"], "status": "skipped", "reason": "score below 2/2 gate"})
            continue
        if row.get("rewrite_precision_to_verify"):
            log_entries.append({"slide_id": row["slide_id"], "status": "skipped", "reason": "source-check flagged unverified precision in rewrite"})
            continue
        if not row.get("recommended_rewrite"):
            log_entries.append({"slide_id": row["slide_id"], "status": "skipped", "reason": "no recommended_rewrite"})
            continue
        entry = stage_rewrite(row, deck_text, run_dir)
        log_entries.append(entry)
        if entry["status"] in ("staged", "would_apply_live"):
            pending_diff_lines.append(f"\n--- SLIDE {entry['slide_id']} ---\n")
            for ed in entry["edits"]:
                pending_diff_lines.append(f"- {ed['old']}\n+ {ed['new']}\n")

    (run_dir / "pending-apply.diff").write_text("".join(pending_diff_lines))
    (run_dir / "auto-apply-log.json").write_text(json.dumps(
        {"hash_check": "ok", "live_apply": LIVE_APPLY, "deck_path": str(deck_path),
         "applied_rewrites": log_entries}, indent=2))

    staged = sum(1 for e in log_entries if e["status"] == "staged")
    skipped = sum(1 for e in log_entries if e["status"] == "skipped")
    print(f"OK: hash check passed. {staged} rewrites staged, {skipped} skipped. LIVE_APPLY={LIVE_APPLY}")
    print(f"Diff: {run_dir / 'pending-apply.diff'}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: auto-applier.py <run_dir>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
