# agentic-slides v2 Pipeline — Phase 5 Reference

Canonical reference for the 5-link orchestrated pipeline that runs as Phase 5 of `/agentic-slides`. Replaces the standalone clarity gate as the LAST gate before a deck ships.

Source design: `~/.claude/plans/i-need-you-to-shiny-kahan.md` §15–§25.
Build plan: `~/.claude/plans/let-s-pick-this-up-functional-ember.md`.

---

## Pipeline diagram

```
Phase 5 (after Pass 1–4 quality):
  │
  ▼
┌────────────────────────────────────────────────────────────┐
│  1. per-slide-clarity-gate (existing v1.2)                 │
│  Outputs: aggregate.json + per-slide-{naive,expert}.json   │
│  Halt: Naive≤1 OR Expert=0 → surface to user, stop         │
└────────────────────────────┬───────────────────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────┐
│  2. source-verifier (scripts/source-verifier.py)           │
│  Scope: skill-level mechanisms only (see §source-verifier- │
│  scope below).                                             │
│  - Parallel WebFetch on URL'd citations                    │
│  - Verbatim search on named-author quotes in dossier       │
│  - Numeric precision check against dossier excerpts        │
│  Outputs: source-verification.json                         │
│  Halt: confirmed mismatch on named-author quote            │
└────────────────────────────┬───────────────────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────┐
│  3. rewrite-pressure-tester (scripts/rewrite-pressure-     │
│     tester.md — orchestrator playbook)                     │
│  Conditional firing: regex-flagged OR agent-flagged        │
│  rewrites only.                                            │
│  Detector: inferential-detector.py (regex) → agents/       │
│  inferential-detector.md (named-entity novelty) as         │
│  fallback.                                                 │
│  On qualifying rewrites: spawn 2-pass strategy:pressure-   │
│  test:pressure-test-critic (Pass 1 attack → Pass 2 attack  │
│  the attack).                                              │
│  Outputs: rewrite-pressure-test.json                       │
│  Halt: Pass 2 confirms a Pass 1 objection — orchestrator-  │
│  enforced (see §halt-enforcement-class).                   │
└────────────────────────────┬───────────────────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────┐
│  4. auto-applier (scripts/auto-applier.py)                 │
│  - Pre-flight: assert sha256(deck) matches                 │
│    run-manifest.json:deck_snapshot_sha256                  │
│  - Apply only rewrites with naive≥2 AND expert≥2 AND       │
│    source_check==clean (and pressure-test pass if          │
│    triggered)                                              │
│  - Pre/post snapshot per rewrite                           │
│  - STAGE-ONLY MODE at v2 launch: writes pending-apply.diff │
│    instead of editing canonical deck file. Manual          │
│    promotion (see §auto-applier-promotion).                │
│  Outputs: auto-apply-log.json + pending-apply.diff         │
│  Halt: deck-hash drift OR snapshot inconsistency           │
└────────────────────────────┬───────────────────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────┐
│  5. failure-pattern-logger (scripts/failure-pattern-       │
│     logger.py)                                             │
│  Extracts new mechanisms caught this run.                  │
│  - Skill-level: memory/known-failure-mechanisms.json       │
│    (typed entries, deduped by id)                          │
│  - Project-level: <project>/.clarity-gate/                 │
│    known-failure-patterns.json (instance hints, feed       │
│    Expert prompt next run for THIS project)                │
└────────────────────────────────────────────────────────────┘
```

---

## §source-verifier-scope

The source-verifier loads **skill-level mechanisms only** (`memory/known-failure-mechanisms.json`). It does NOT load project-level patterns (`<project>/.clarity-gate/known-failure-patterns.json`).

**Why this scope:** project-scoped instance hints (e.g., "the cited industry stat does not name this client") are session-and-judgment artifacts. They live in the Expert prompt where they become hint text the Expert weighs. Source-verifier is universal — its rules apply identically across every project. Skill-level mechanisms are deterministic regex patterns that catch known confabulation classes anywhere.

**Implication:** project-specific attribution failures (misattributed-stat class) are caught at the Expert prompt layer on the NEXT run after they're first logged. There is a one-run lag between "first caught" and "auto-prevented." Skill-level mechanisms, by contrast, propagate to all projects immediately.

This is decision Q3 in the review pass on the build plan.

---

## §halt-enforcement-class

Pipeline links 1, 2, 4, 5 are Python scripts. They halt via process exit codes — deterministic, code-enforced.

Pipeline link 3 (`rewrite-pressure-tester.md`) is a markdown orchestrator playbook. A Claude session reads the playbook and follows the halt instruction. **Halt behavior is orchestrator-enforced, not code-enforced.**

The two enforcement classes have the same intent but different reliability profiles. A Python halt cannot be skipped by future drift in interpretation; a markdown halt depends on the orchestrator reading the doc correctly each run.

When this matters: if a future contributor wires Phase 5 to a non-Claude orchestrator, link 3 needs to be reimplemented as code or the halt is lost.

---

## §re-run-policy

Pipeline runs are **idempotent from scratch, not resumable.**

If any link halts midway, the run directory contains partial outputs (e.g., `aggregate.json` and `source-verification.json` but nothing downstream). To pass the halt, fix the underlying issue and re-run the entire pipeline. Do NOT build a "resume from checkpoint" feature without rethinking the manifest's `expected_agent_spawns` assertion — a partial resume would violate the spawn count and trip the tamper-detection check.

This is a design constraint, not a performance limitation. Re-running guarantees the snapshot hash, manifest spawn counts, and per-slide files are all consistent. A resume primitive that bypasses these checks would weaken the tamper-proof guarantee.

---

## §auto-applier-promotion

`auto-applier.py` ships in **stage-only mode** at v2 launch. The constant `LIVE_APPLY = False` at the top of the file controls behavior:

- **Stage-only (`LIVE_APPLY = False`):** writes proposed edits to `pending-apply.diff` in the run directory. Does NOT modify the canonical deck file. All pre/post snapshots and the deck-hash assertion still run.
- **Live (`LIVE_APPLY = True`):** applies edits to the canonical deck file via `Edit`. Same safety checks; the difference is whether the edit is performed.

**Promotion checklist** (manual, performed once before flipping the flag):

1. Read `pending-apply.diff` from the most recent successful run end-to-end.
2. Confirm every staged edit matches a `recommended_rewrite` entry in that run's `aggregate.json`. No phantom edits.
3. Confirm no source-check `mismatch` or pressure-test `surviving_fix` status was silently passed through (these should already have halted the pipeline; this is a belt-and-suspenders check).
4. Confirm the pre-apply hash assertion succeeded in the last run (`auto-apply-log.json:hash_check == "ok"`).
5. Flip `LIVE_APPLY = True` in `auto-applier.py`.
5.5. **Update the orchestrator (Phase 5.2 step 4 in `agentic-slides.md`) to perform Edit tool invocations against entries in `pending-apply.diff`.** Flipping the flag alone does NOT enable live application — the script emits `would_apply_live` status but defers the actual Edit calls to the orchestrator. Without this step, post-flip behavior is a silent no-op.
6. Run the full pipeline against the same project fixture and confirm the canonical deck file now changes match the previously-staged diff.

Until step 5, the auto-applier link is observational. The pipeline still gates on its halt conditions but cannot modify the deck.

---

## Audit commands

```bash
RUN_DIR=.clarity-gate/run-<ts>

# 1. All five sub-components ran and wrote outputs
test -f $RUN_DIR/aggregate.json                       # gate
test -f $RUN_DIR/source-verification.json             # source-verifier
test -f $RUN_DIR/rewrite-pressure-test.json           # pressure-tester (may be empty)
test -f $RUN_DIR/auto-apply-log.json                  # auto-applier
test -f $RUN_DIR/patterns-logged.json                 # failure-pattern-logger

# 2. Halt decisions visible
jq '.halt_reason // "none"' $RUN_DIR/run-summary.json

# 3. Auto-applied (or staged) changes match recommended rewrites
jq '.applied_rewrites[].slide_id' $RUN_DIR/auto-apply-log.json
# Cross-reference: $RUN_DIR/aggregate.json:.matrix[].recommended_rewrite

# 4. Per-slide audit unchanged (gate v1.2 audit commands still apply)
# See: per-slide-clarity-gate.md §audit-commands

# 5. Memory growth visible
diff ~/.claude/commands/agentic-slides/memory/known-failure-mechanisms.json{,.before-run}

# 6. Pre-apply hash assertion succeeded
jq '.hash_check' $RUN_DIR/auto-apply-log.json   # expected: "ok"

# 7. Stage-only invariant (until promotion)
test -f $RUN_DIR/pending-apply.diff
# Confirm no canonical deck mutation
git -C <project> diff --stat docs/research/deck-headlines-*.md
```

---

## Pattern memory schema

### Skill-level: `memory/known-failure-mechanisms.json`

```json
{
  "schema_version": "1.0",
  "mechanisms": [
    {
      "id": "M001",
      "claim_type": "numeric_confabulation_in_rewrites",
      "regex_signature": "(\\d+)[-–](\\d+)% of (REDACTED|advisors|institutional)",
      "mechanism_description": "Expert agent introduces percentage range in rewrite to replace an 'every X' overclaim from the slide. The range is not in the dossier; it's a 'reasonable-sounding' fabrication.",
      "first_caught": {
        "project_anon": "client-deck-A",
        "slide_id": "S09",
        "date": "2026-05-11",
        "specific_value": "70-80%"
      },
      "aggregator_action": "flag_in_rewrite_precision_to_verify",
      "severity": "HIGH"
    }
  ]
}
```

The aggregator's `load_memory()` reads this file at startup and appends each `regex_signature` to its precision-check pattern list. Deterministic; no prompt injection.

### Project-level: `<project>/.clarity-gate/known-failure-patterns.json`

```json
{
  "schema_version": "1.0",
  "project_id": "example-pitch",
  "patterns": [
    {
      "id": "P001",
      "claim_type": "source_misattribution",
      "instance": "Named-firm attribution to an industry stat — the original source reports the figure as category-level and doesn't name the firm",
      "first_caught": { "slide_id": "S13", "date": "2026-05-11" },
      "expert_hint": "When this project's slides reference the industry stat, verify any named-firm attribution is in the cited source. Default assumption: it is not."
    }
  ]
}
```

The Expert prompt for THIS project loads this file and includes a block: "Past failure patterns caught on this project — flag if you see anything similar:" followed by the `expert_hint` text. The source-verifier does NOT read this file (see §source-verifier-scope).

---

## Halt thresholds (consolidated)

| Layer | Halt condition |
|---|---|
| Gate | Naive≤1 (lost OR polarity-inverted) on any slide. Expert=0 (misrepresents source) on any slide. |
| Source-verifier | Confirmed mismatch on named-author quote. URL'd citation returns 404. |
| Pressure-tester | Pass 2 confirms a Pass 1 objection (surviving fix) on any rewrite. *(Orchestrator-enforced.)* |
| Auto-applier | Pre-apply hash assertion fails (state drift). Pre/post snapshot fails to write. |
| Logger | Schema validation fails on a new mechanism entry. |

If none fire, the pipeline auto-applies (or stages, until §auto-applier-promotion is complete) all rewrites that scored ≥2/≥2 AND passed source-check AND passed pressure-test (if triggered).

---

## See also

- `per-slide-clarity-gate.md` — canonical spec for link 1 (the gate v1.2)
- `clarity-gate-spawn.md` — orchestrator playbook for link 1
- `~/.claude/plans/i-need-you-to-shiny-kahan.md` §15–§25 — full v2 design rationale
- `~/.claude/plans/let-s-pick-this-up-functional-ember.md` — this build's execution plan and review decisions
