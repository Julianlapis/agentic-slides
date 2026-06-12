# Per-Slide Clarity & Fidelity Gate

> Canonical reference for the per-slide gate that runs as the final quality check in agentic-slides Phase 5.
> Supersedes `headline-review-agents.md` (now deprecated). Added 2026-05-11 after a high-stakes pitch run.

The gate spawns two fresh-context agents per slide (Naive Reader + Expert Reviewer), aggregates deterministically, and surfaces conflicts to the user. It catches dilution + clarity failures that the four-pass quality system + deck-level Headline Blind Reader miss.

---

## Why this exists

The four-pass quality system (`quality-system-v2.md`) operates at deck level. Pass 3 Narrative Flow checks transitions, Pass 4 Copy Quality applies voice rules. Both miss two specific failure modes:

1. **Per-slide clarity dilution.** A stranger landing on a single slide cannot stitch missing meaning from surrounding context. A slide that reads fine in sequence can be opaque in isolation. The Headline Blind Reader reads all headlines in a row — that's deck-level, not slide-level.

2. **Per-slide fidelity overclaim.** A slide can attach its punch line to a citation that doesn't support it (claiming a named firm is inside an industry stat when the cited source reports the figure at category level only). The Gap Analyzer maps headlines against the brief, not slide bodies against source dossier finding-by-finding.

This gate catches both. It is the LAST gate before ship. It is not optional.

**Origin:** Built 2026-05-11 during a high-stakes agency pitch. The deck passed the four-pass system at Pass 3 60/60 ("FLAWLESS"). The per-slide gate caught two genuine fact-check failures (S13 unsupported attribution, S22 heritage conflation) and one BROKEN slide (S15 an unverified dollar figure + category error). Both fact-checks would have embarrassed the team in front of the client. A post-gate pressure-test additionally caught the gate's own Expert confabulating a number inside a recommended rewrite (S09 70-80% REDACTED stat) — this drove the v1.2 source-check patch.

---

## Architecture

```
Per slide N, the gate spawns 2 agents in parallel waves:

  ┌─────────────────────────┐    ┌────────────────────────────┐
  │  NAIVE READER           │    │  EXPERT REVIEWER           │
  │  (general-purpose,      │    │  (general-purpose,         │
  │   tool-restricted by    │    │   skeptical fact-checker   │
  │   prompt contract)      │    │   role)                    │
  │                         │    │                            │
  │  Reads ONLY slide N     │    │  Reads slide N + intended  │
  │  content. No project    │    │  Argument + source dossier │
  │  context.               │    │  excerpt + Naive's guess.  │
  │                         │    │                            │
  │  Reports tool_calls_made│    │  Two-block prompt:         │
  │  for cold-context audit.│    │  Block A scores fidelity   │
  │                         │    │  BEFORE reading Naive.     │
  │                         │    │  Block B scores match.     │
  └────────────┬────────────┘    └─────────────┬──────────────┘
               │                                │
               └────────────┬───────────────────┘
                            │
                  ┌─────────▼──────────┐
                  │  AGGREGATOR SCRIPT │  (Python, deterministic, no LLM)
                  │  - Schema validate │
                  │  - Cold-context    │
                  │    audit (Naive)   │
                  │  - Cross-check     │
                  │    (Expert cite vs │
                  │    Naive text)     │
                  │  - Source-check    │
                  │    (rewrites trace │
                  │    to dossier)     │
                  │  - Score rollup    │
                  └─────────┬──────────┘
                            │
                  ┌─────────▼──────────┐
                  │  ORCHESTRATOR      │  (main Claude session)
                  │  Reads aggregate   │
                  │  Quotes per-slide  │
                  │  files with paths  │
                  │  Surfaces conflicts│
                  │  Reports to user   │
                  └────────────────────┘
```

**Important sequencing:** Naive fires BEFORE Expert. Expert's prompt receives Naive's output. The two agents run in parallel temporally, but Expert's input reads Naive's output file once Naive has written it. Implementation: spawn Naive batch → verify all Naive output files exist → spawn Expert batch.

---

## Tamper-proof mechanisms

The gate's value comes from the orchestration being non-fakeable. Each mechanism closes a specific failure mode.

### 1. Pre-flight run manifest

Before any agent fires, the orchestrator writes `.clarity-gate/run-{ISO_TS}/run-manifest.json`:

```json
{
  "run_id": "...",
  "deck_id": "...",
  "deck_path": "...",
  "deck_snapshot_sha256": "<hash of deck content file>",
  "slides_in_scope": ["S02", "S05", ...],
  "slide_count": 28,
  "expected_agent_spawns": 56,
  "gate_version": "v1.2",
  "patches_applied": [...],
  "started_at": "..."
}
```

The deck snapshot hash makes mid-run tampering detectable. The aggregator at the end refuses to score if observed spawns ≠ expected.

**Closes failure mode:** "Claimed N spawns, actually did fewer."

### 2. One file per agent output, deterministic paths

Each agent writes to:
```
.clarity-gate/run-{ts}/slide-{ID}-naive.json
.clarity-gate/run-{ts}/slide-{ID}-expert.json
```

No verdicts ever live in orchestrator memory or are echoed by the orchestrator without citing the file path. Every verdict in the final report is quoted from a file with the path inline.

**Closes failure mode:** "Orchestrator fabricates agent output in summary."

### 3. Schema validation

Each output JSON must conform to a strict schema. Aggregator rejects malformed outputs (exit code 4).

**Naive schema (v1.1+):**
```json
{
  "slide_id": "S02",
  "agent_type": "naive",
  "guess_main_point": "<one sentence>",
  "evidence_named": ["..."],
  "confusions": "<or 'none'>",
  "confidence": "high|medium|low",
  "tool_calls_made": [{"tool": "Write", "path": "<output_path>"}]
}
```

**Expert schema (v1.1+):**
```json
{
  "slide_id": "S02",
  "agent_type": "expert",
  "expert_fidelity_score": 0|1|2|3,
  "expert_fidelity_cite": "<Block A evidence>",
  "dilution_flags": ["..."],
  "naive_match_score": 0|1|2|3,
  "naive_match_cite": "<Block B evidence>",
  "recommended_rewrite": null | {"headline": "...", "body": "..."}
}
```

### 4. Cold-context audit for Naive (v1.1+)

Naive's prompt instructs the agent to emit `tool_calls_made` listing every tool call it made. The aggregator validates that this list contains EXACTLY ONE entry — the Write call for its output file. Any extra tool call (Read, Bash, WebFetch, Glob, Grep) marks the slide as un-judged with a cold-context violation.

This is post-hoc audit, not true sandboxing. v2 fix: SDK-level tool allowlist when supported.

**Closes failure mode:** "Naive 'cold' agent was actually pre-loaded with hints by reading other files."

### 5. Expert two-block fidelity-first prompt (v1.1+)

Original Expert prompts saw Naive's guess before scoring fidelity. Naive's confidence anchored Expert's fidelity rating.

v1.1 split Expert into two sequential blocks:
- **Block A** — Read slide + intended Argument + dossier excerpt. Score `expert_fidelity_score` with cite. Commit before advancing.
- **Block B** — NOW read Naive's guess. Score `naive_match_score` with cite.

Block A's input does NOT include Naive. Order of reasoning enforced by prompt structure.

### 6. Skeptical-fact-checker Expert role (v1.1+)

The Expert prompt opens with: "You are a SKEPTICAL FACT-CHECKER. You do NOT extend benefit of the doubt to inferential leaps the source does not directly support." Earlier framing as "senior strategy director" was too lenient — strategy directors trust the dossier; fact-checkers audit it.

### 7. Cross-check between Expert citation and Naive text (v1.1+)

The aggregator asserts Expert's `naive_match_cite` either:
- Contains a 4+ word n-gram (≥15 chars) from Naive's `guess_main_point`, OR
- Contains a verbatim substring (≥20 chars) of Naive's guess, OR
- Contains an explicit framing about Naive's read ("miss", "lack", "instead of", "rather than", "captures", etc.)

Mismatches flag the slide as un-judged.

**Closes failure mode:** "Expert fabricated a citation that doesn't ground in Naive's actual text."

### 8. Source-check on recommended_rewrite (v1.2+, NEW)

The pressure-test of one gate run caught the gate's own Expert agent confabulating a "70-80% of REDACTED" stat inside a recommended rewrite (S09). The stat wasn't in the dossier — the Expert produced it from its own reasoning and presented it as research-grounded.

v1.2 adds: any numeric claim or specific entity name in a `recommended_rewrite` must trace to either the dossier excerpt the Expert received, or be explicitly flagged as "INFERENTIAL — needs verification" in the cite. The aggregator runs a pattern scan for unflagged precision (percentages, dollar figures, specific dates, named entities) that doesn't appear in the slide content or the dossier excerpt.

This is the most important v1.2 patch. The gate is built to catch overclaims, and v1.1 caught the gate itself producing overclaims inside its fixes.

**Closes failure mode:** "Gate fixes one fidelity hole by introducing another."

---

## Scoring rubric

### Per-slide, two dimensions, 0–3 each

**Naive Match Score** (set by Expert reading Naive's output + intended Argument):

| Score | Meaning |
|---|---|
| 3 | Naive captures BOTH the argument's VERB (what happens / what's true) AND its STAKES (why it matters / who is affected) |
| 2 | Captures verb OR stakes, not both |
| 1 | Topic right, polarity inverted |
| 0 | Cannot extract a coherent guess |

**Expert Fidelity Score** (Expert vs source dossier):

| Score | Meaning |
|---|---|
| 3 | Slide matches dossier substance + stat values + polarity. Survives senior scrutiny. |
| 2 | One weasel/softening/genericizing. Substance intact. |
| 1 | Two+ dilutions, OR a key qualifier dropped, OR an inferential leap presented as sourced fact |
| 0 | Misrepresents or contradicts source |

### Deck-level rollup (deterministic aggregator)

- **Clarity Pass Rate** = (count of slides with Naive Match ≥ 2) / slide_count
- **Fidelity Pass Rate** = (count of slides with Expert Fidelity ≥ 2) / slide_count
- **Critical Failures** = count of slides with EITHER score = 0
- **Composite Health** = (sum(Naive Match) + sum(Expert Fidelity)) / (6 × slide_count) × 100

### Thresholds

| Status | Condition |
|---|---|
| Ships | Clarity ≥ 90% AND Fidelity ≥ 90% AND Critical Failures = 0 |
| Rewrites specific slides | Clarity 70–90% OR Fidelity 70–90% |
| Redraft section | Any section has > 30% slides failing |
| Redraft deck | Clarity < 70% OR Fidelity < 70% |

### Verdict mapping per slide

| Naive | Expert | Verdict |
|---|---|---|
| 3 | 3 | Ship |
| 3 | <3 | Clear-but-diluted — rewrite for fidelity |
| <3 | 3 | Right-but-unclear — rewrite for clarity |
| <3 | <3 | Broken — full slide rewrite |
| Either = 0 | | Critical — redraft |

---

## Prompt templates

See `clarity-gate-prompts-v1.1.md` for the full Naive + Expert v1.1 templates. v1.2 prompt updates (TBD when source-check is added to the Expert prompt — currently source-check runs at the aggregator level only).

---

## Aggregator + normalizer

- **`clarity-gate-aggregator.py`** — Python script, ~150 lines. Schema validation, cold-context audit, cross-check, score rollup. Deterministic. Exit codes:
  - 0 = ship-clean
  - 2 = run dir missing
  - 3 = tampering (count mismatch)
  - 4 = schema validation failure
  - 5 = missing pair for a slide
  - 6 = (reserved for v1.2 partial_run_mode transient failures)
  - 7 = cross-check failure (Expert cite doesn't ground in Naive text)
  - 8 = (reserved for v1.2 source-check failure on recommended_rewrite)

- **`clarity-gate-expert-normalizer.py`** — One-time normalizer for v1.1 Expert outputs. 21 of 28 Experts in one run produced a nested `block_a/block_b/verdict` schema instead of the flat schema. The normalizer maps three observed variants (canonical, flat-with-renamed-fields, nested) to canonical. v1.2 prompt enforcement should reduce reliance on this.

---

## Where to run, when to run

Run the gate **after** the four-pass quality system (Pass 1 Layout, Pass 2 Design, Pass 3 Narrative, Pass 4 Copy) — it's the FINAL gate before ship.

Scope: all content slides. Skip cover, agenda, section dividers, closing. Section closers (black-bg key-takeaway slides) ARE in scope.

Cost: each spawn is ~50K tokens of harness context + ~500-1000 tokens of prompt content. Full deck runs are 2N spawns where N is content slide count. Plan accordingly — for a 28-slide run, expect ~2.3M tokens and 5-10 minutes wall time.

---

## v1.2 patches (open)

The pressure-test of the same gate run surfaced four v1.2 fixes. Implement in this order:

1. **`recommended_rewrite` source-check (most important).** Catches gate Expert confabulations inside fixes. See §8 above.
2. **Strict JSON schema enforcement on Expert prompt.** 75% of v1.1 Experts deviated from schema. Prompt must include "MUST output only this flat JSON, do not nest under block_a/block_b" warning.
3. **`partial_run_mode` flag.** Distinguish transient agent failures (rate limit, timeout) from tampering. Currently both produce non-scorable runs. New exit code 6 for partial runs.
4. **Per-slide content hash cache.** If a slide hasn't changed since a prior run, copy outputs forward. Saves spawns on rewrite iterations.

Deferred to v2:
- SDK-level tool allowlist on Naive spawns (replaces post-hoc cold-context audit)
- Naive-summarizes alternative test (Naive produces a one-sentence summary that a third reader compares against headline-only). Strictly better measurement of clarity-vs-headline alignment. Requires rubric redesign.
- Chapter-divider rubric (currently dividers are out of scope; v2 adds a chapter-coherence rubric for them)

---

## Audit commands (any run)

```bash
RUN_DIR=.clarity-gate/run-<ts>

# 1. File count matches expected
ls $RUN_DIR/slide-*.json | wc -l                          # = 2 * slide_count

# 2. Each slide has both naive and expert
for s in <slide_ids>; do
  test $(ls $RUN_DIR/slide-${s}-{naive,expert}.json 2>/dev/null | wc -l) -eq 2
done

# 3. Deck snapshot hash matches
shasum -a 256 <deck_file>                                 # compare to run-manifest.json deck_snapshot_sha256

# 4. Cold-context audit
python3 -c "
import json,glob
for f in glob.glob('$RUN_DIR/slide-*-naive.json'):
    d = json.load(open(f))
    tools = [c['tool'] for c in d.get('tool_calls_made',[])]
    if tools != ['Write']: print(f, tools)
"

# 5. Aggregator is deterministic (re-run produces identical output)
python3 ~/.claude/commands/agentic-slides/scripts/clarity-gate-aggregator.py $RUN_DIR
diff $RUN_DIR/aggregate.json <(python3 ~/.claude/commands/agentic-slides/scripts/clarity-gate-aggregator.py $RUN_DIR > /tmp/r.json && cat $RUN_DIR/aggregate.json)
```

If any audit fails, the run is invalid. Re-run.
