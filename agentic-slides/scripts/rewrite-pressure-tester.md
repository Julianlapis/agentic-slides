# rewrite-pressure-tester — Pipeline Link 3 (orchestrator playbook)

Execution playbook for pipeline link 3. Canonical spec lives in `references/v2-pipeline.md §link-3-pressure-tester`. This playbook is read by a Claude session and executed — **halt behavior is enforced by Claude following the doc, not by code assertion.** Unlike the `.py` links in this pipeline, this link's halt is judgment-based. See `v2-pipeline.md §halt-enforcement-class`.

## When this fires

This link runs AFTER `source-verifier.py` produces `source-verification.json` and BEFORE `auto-applier.py` stages or applies any rewrites.

The link runs only on rewrites that passed source-check (no `mismatch` flag) but contain inferential claims that source-check cannot evaluate.

## Inputs

- `<run_dir>/aggregate.json` (gate output — has `matrix[].recommended_rewrite`)
- `<run_dir>/source-verification.json` (source-verifier output)
- The deck content file (path in `<run_dir>/run-manifest.json:deck_path`)

## Outputs

- `<run_dir>/rewrite-pressure-test.json` with per-rewrite verdicts

## Halt condition

If **Pass 2 confirms a Pass 1 objection** on any rewrite (a "surviving fix"), STOP the pipeline. Do not advance to `auto-applier.py`. Surface the surviving fix to the user via a final report and wait for direction.

## Step-by-step

### 1. Load the inputs

```python
import json
from pathlib import Path
run_dir = Path("<run_dir>")
aggregate = json.loads((run_dir / "aggregate.json").read_text())
source_check = json.loads((run_dir / "source-verification.json").read_text())
manifest = json.loads((run_dir / "run-manifest.json").read_text())
deck_text = Path(manifest["deck_path"]).read_text()
```

### 2. Identify candidate rewrites

For each row in `aggregate["matrix"]`:

- Skip if `naive_match < 2` OR `expert_fidelity < 2` (gate failed; rewrite isn't going to apply anyway).
- Skip if the source-check found a `mismatch` or `404` for this slide (pipeline already halted at link 2).
- Otherwise, this rewrite is a CANDIDATE.

### 3. Run the regex detector (cheap layer)

```bash
python3 ~/.claude/commands/agentic-slides/scripts/inferential-detector.py --aggregate <run_dir>/aggregate.json
```

Read the output. For each row in `results[]`: if `regex_flagged == true`, mark that slide for pressure-test (skip the agent layer for it).

### 4. Run the named-entity agent (gated layer)

For rows in step 3 where `regex_flagged == false` (cheap layer didn't catch anything), dispatch the named-entity agent for each:

Use the Agent tool with:

```
subagent_type: general-purpose
description: Inferential-detector named-entity check, slide <SID>
prompt: |
  Read ~/.claude/commands/agentic-slides/agents/inferential-detector.md fully.
  Execute the protocol on these two text blocks:

  ORIGINAL SLIDE CONTENT:
  <extract from deck file using slide_id_to_marker_candidates>

  PROPOSED REWRITE:
  <recommended_rewrite headline + body from aggregate>

  Return JSON only, per the schema in the agent file.
```

Capture the JSON output per slide. If `needs_pressure_test == true`, add the slide to the pressure-test set.

### 5. Pressure-test the qualifying rewrites (two-pass)

For each slide in the pressure-test set, dispatch TWO sequential agents:

**Pass 1 — attack:**

```
subagent_type: strategy:pressure-test:pressure-test-critic
description: Pass 1 attack on slide <SID> rewrite
prompt: |
  Attack this rewrite. Find the strongest case that it overclaims, infers
  unsupported standing, or attributes mechanism without source.

  ORIGINAL SLIDE: <verbatim from deck>
  PROPOSED REWRITE: <recommended_rewrite>
  REGEX MARKERS FOUND (if any): <from step 3 output>
  NOVEL ENTITIES FOUND (if any): <from step 4 output>

  Return: {"slide_id": "<SID>", "pass": 1, "objections": [
    {"claim": "<verbatim>", "objection": "<your strongest>", "severity": "low|medium|high"}
  ]}
```

**Pass 2 — attack the attack:**

```
subagent_type: strategy:pressure-test:pressure-test-critic
description: Pass 2 attack on Pass 1 objections, slide <SID>
prompt: |
  Attack Pass 1's objections. For each, decide whether the objection survives
  scrutiny or is itself overreach. The original rewrite was:

  <recommended_rewrite>

  PASS 1 OBJECTIONS:
  <from Pass 1>

  Return: {"slide_id": "<SID>", "pass": 2, "verdicts": [
    {"original_objection": "<verbatim>", "pass_2_verdict": "objection_survives|objection_is_overreach", "reasoning": "..."}
  ]}
```

### 6. Aggregate into rewrite-pressure-test.json

```json
{
  "run_id": "<from manifest>",
  "candidates_examined": <int>,
  "regex_flagged": <int>,
  "agent_flagged": <int>,
  "pressure_tested": <int>,
  "halt_reasons": [
    "S<NN>: Pass 2 confirmed objection — <verbatim Pass 1 claim> — surviving fix"
  ],
  "verdicts": [
    {
      "slide_id": "S<NN>",
      "regex_markers": [...],
      "novel_entities": [...],
      "pass_1": {...},
      "pass_2": {...},
      "status": "ship|surviving_fix"
    }
  ]
}
```

### 7. Halt decision (orchestrator-enforced)

If `halt_reasons` is non-empty, STOP. Write `rewrite-pressure-test.json` and surface the halt to the user. Do NOT run `auto-applier.py`.

If `halt_reasons` is empty, write `rewrite-pressure-test.json` and proceed to `auto-applier.py`.

## Audit commands

```bash
RUN_DIR=<run_dir>

# 1. Did the file get written
test -f $RUN_DIR/rewrite-pressure-test.json

# 2. Did pressure-test fire on the expected slides
jq '.pressure_tested' $RUN_DIR/rewrite-pressure-test.json

# 3. Surviving fixes (must be empty for pipeline to have proceeded)
jq '.halt_reasons' $RUN_DIR/rewrite-pressure-test.json
```

## Reuse

- `strategy:pressure-test:pressure-test-critic` agent — used as-is for both passes. Do NOT create a new critic agent for this pipeline.
- `inferential-detector.py` regex layer — runs first; saves spawn cost on rewrites it already flagged.
- `agents/inferential-detector.md` agent — runs only on rewrites the regex layer didn't flag.

## Out of scope

- Pass 3 (third-degree adversarial loop) — over-engineering for v2. Two passes is the design.
- Pressure-testing slides that didn't get a rewrite recommendation. The pipeline only tests proposed changes.
- Pressure-testing the gate's Naive/Expert scoring itself. That's the gate's own concern, not link 3's.
