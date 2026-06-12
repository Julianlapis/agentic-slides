# Four-Pass Quality System

Run all four passes in parallel after every round of content changes. This is mandatory before presenting work to the user.

**Critique-driven iteration:** For existing decks that need improvement, run /critique first to get a prioritized issue list. Then modify in place rather than rebuilding. The critique output maps directly to targeted modifications. This workflow (critique -> targeted modifications) is the default for deck iteration, not "rebuild the whole thing."

**Voice layers (optional):** If you maintain your own voice/style guide files, apply them during the Copy Quality pass. Otherwise the checks defined in Pass 4 below are self-contained.

---

## Pass 1: Layout Intelligence

**Model: sonnet.** Pattern matching against layout library, not aesthetic judgment.

Review the full slide sequence for layout selection quality. Score the full deck on 5 dimensions (1-10).

| Dimension | Question | What 10 looks like |
|-----------|----------|-------------------|
| Content-Layout Fit | Does each slide's layout match its content shape? | A slide with 4 parallel items uses Cards or Multi-Column, not Left-Heavy. A single bold idea uses Statement, not Eyebrow + 2-Column. Every layout earns its spot. |
| Variety | How many distinct layouts appear? | A 10-slide deck uses 4+ different layouts. A 20-slide deck uses 7+. No layout appears more than 3 times. |
| Rhythm | Do dense and sparse slides alternate? | Image-heavy slides are buffered by text-only slides. Statement/Quote slides create breathing moments at transitions. No 3+ dense slides in a row. |
| Sequencing | Are structural slides (Agenda, Section Divider, Thank You) placed correctly? | Agenda follows title. Section Dividers mark transitions. Quote slides sit between sections, not within. Thank You closes. |
| Pacing | Does content density build and release across the deck? | The deck doesn't front-load all dense slides or save all visual slides for the end. Density varies deliberately. |

**Below 35/50 for the full deck: reassign layouts before delivering.**

### Agent Prompt Template

```
You are a Layout Intelligence Agent. Review the full slide sequence for layout selection quality.

Score on 5 dimensions (1-10): Content-Layout Fit, Variety, Rhythm, Sequencing, Pacing.

Below 7 on any dimension: flag with specific slides and layout swap recommendations.
Below 35/50 total: reassign layouts.

Here is the slide plan with assigned layouts:
[paste slide plan]

Reference the layout library for available patterns. Suggest specific layout swaps where the current choice doesn't serve the content.
```

---

## Pass 2: Design Quality

**Model: opus.** Requires aesthetic judgment from screenshots.

Screenshot every slide. Score each on 5 dimensions (1-10).

| Dimension | Question | What 10 looks like |
|-----------|----------|-------------------|
| Hierarchy | Can you identify headline, body, and label in under 2 seconds? | Massive scale contrast between tiers. No ambiguity about what to read first. |
| Balance | Is content distributed across the slide, or crammed in one quadrant? | Visual weight feels even. Intentional whitespace, not accidental dead zones. |
| Typography | Are line breaks clean? Any orphans, runts, or awkward wraps? | Every text block breaks at natural phrase boundaries. No single-word lines. |
| Alignment | Do elements share consistent vertical/horizontal lanes? | Everything snaps to an invisible grid. Nothing feels placed by accident. |
| Contrast | Can you read every element without squinting? Do accent colors pop? | Text passes contrast checks on its background. Accent moments are distinct. |

**Below 35/50 per slide: fix before delivering.**

Flag anything below 7 with node IDs and specific fixes.

### Agent Prompt Template

```
You are a Design Quality Agent. Screenshot every slide and score each on 5 dimensions (1-10): Hierarchy, Balance, Typography, Alignment, Contrast.

Below 7 on any dimension: flag with node ID and specific fix.
Below 35/50 total for a slide: FAIL.

Slide artboard IDs: [list IDs]

Screenshot each slide. Output a scorecard per slide with scores, total, and specific fixes needed.
```

---

## Pass 3: Narrative Flow

**Model: sonnet.** Structural analysis of copy sequence.

Read the complete copy across ALL slides. Score the full deck on 6 dimensions (1-10).

**QUANTIFICATION RULE:** Every dimension below has a formula. The agent MUST compute the formula, show the math, and justify the score with it. Qualitative judgment without the formula is not a valid score.

| Dimension | Question | Formula | Target |
|-----------|----------|---------|--------|
| Single-mindedness | Does each slide land exactly one idea? | Count distinct ideas per slide. Score = (slides with exactly 1 idea / total content slides) x 10 | ≥ 9 (90%+ of slides at 1 idea) |
| Redundancy | Are any ideas repeated across slides? | Extract core idea per slide. Score = (unique ideas / total slides) x 10 | 10 (zero repeats) |
| Logical arc | Does each slide build on the one before it? | Score each transition 1 (advances) or 0 (doesn't). Score = (advancing / total transitions) x 10 | ≥ 9 |
| Earned payoff | Does the closer feel earned? | Count callback terms in final 3 slides that appeared earlier. Score: 0 callbacks = 4, 1 = 6, 2 = 7, 3+ = 9, 5+ = 10 | ≥ 7 (3+ callbacks) |
| Specificity | Are claims grounded? | Count claims with named evidence (number, name, example) / total claims. Score = ratio x 10 | ≥ 8 (80%+ grounded) |
| Headline Narrative | Can you follow the argument from headlines alone? | Score each headline transition 1-10. Score = (transitions ≥ 6 / total transitions) x 10 | 10 (100% above 6) |

**Below 42/60 for the full deck: restructure before delivering.**
**Below 7 on any single dimension: flag with specific slides and fixes.**

### Headline Connection Sub-Score

Score each headline-to-headline transition (1-10): does headline B follow naturally from headline A? Shared language, logical progression, or emotional continuity all count. Below 6 on any transition: rewrite one or both headlines to create a bridge.

### Agent Prompt Template

```
You are a Narrative Flow Agent. Score the full deck on 6 dimensions (1-10).

MANDATORY: For each dimension, compute the formula FIRST, then justify with examples.
Do not assign scores based on feel. Show the math.

Formulas:
- Single-mindedness: (slides at 1 idea / total content slides) × 10
- Redundancy: (unique ideas / total slides) × 10
- Logical arc: (advancing transitions / total transitions) × 10
- Earned payoff: count callback terms in final 3 slides (0=4, 1=6, 2=7, 3+=9, 5+=10)
- Specificity: (grounded claims / total claims) × 10
- Headline Narrative: (transitions scoring ≥6 / total transitions) × 10

Below 7 on any dimension: flag with specific slides and fixes.
Below 42/60 total: restructure.

Here is ALL the copy: [paste all slide copy]

Output: formula computation per dimension, score, total, and specific fixes.
```

---

## Pass 4: Copy Quality

**Agent:** spawn a fresh-context copy-review subagent that receives ONLY the deck copy plus the rules in this pass (and your own voice guide files, if you keep any). Fresh context prevents long-session decay from softening the checks.

Score the full deck copy on 5 dimensions (1-10).

**QUANTIFICATION RULE:** Dimensions 1-4 are judgment calls backed by pattern counts. Dimension 5 (SCDS) is a hard-gated formula.

| Dimension | Question | Formula | Target |
|-----------|----------|---------|--------|
| Directness | Statements or announcements? | Count sentences that lead with the claim / total sentences. Score = ratio x 10 | ≥ 8 |
| Rhythm | Varied or metronomic? | Count runs of 3+ sentences within 3 words of each other's length. Score = 10 - (runs x 2) | ≥ 7 |
| Trust | Respects reader intelligence? | Count unnecessary definitions or over-explanations / total explanatory sentences. Score = 10 - (ratio x 10) | ≥ 8 |
| Authenticity | Sounds human? | Count false agency instances + banned phrase violations + Big One violations. Score = 10 - (violations x 1.5), floor 0 | ≥ 7 |
| **Copy Density (SCDS)** | How efficiently does each slide communicate? | Per slide: (distinct new ideas / total words) x 10. Grade by slide type. **HARD GATE.** | See table below |

### Slide Copy Density Score (SCDS): Slide-Type Thresholds

| Slide Type | Examples | Max Words | SCDS Target |
|------------|----------|-----------|-------------|
| Statement/Proposition | Insight, Proposition, Section openers | ≤ 30 | ≥ 1.5 |
| Argument | Category, Competition, Moat, Reframe | ≤ 60 | ≥ 1.0 |
| Evidence | Audience, Design Principles | ≤ 50 | ≥ 1.0 |
| Framework | Pillars, Metrics | Structured list | N/A (count items instead) |
| Scope/Plan | Approach, Team | Deliverables list | N/A |

**HARD GATE:** Any content slide with SCDS below its type target = automatic flag, regardless of total score. The agent must provide: word count, idea count, SCDS score, and the specific sentences that elaborate without advancing.

**NARRATIVE ADVANCEMENT TEST (part of SCDS):** For each sentence in body copy, ask: does this advance past the previous sentence, or add detail to the same point? Detail is for the presenter to say. If it adds detail: recommend merge or cut.

**Below 35/50: revise before delivering.**

Run against your own voice/style guides if you keep them; otherwise the rules in this pass are the rubric. The review subagent catches every violation in a single pass: mechanical violations (banned phrases, em dashes, adverbs, staccato, false agency) plus judgment calls (rhythm, register, voice authenticity, narrative density).

Detailed rules, banned phrases, and structures to avoid are in the canonical sources. Do not duplicate them here.

### Agent Prompt Template

```
You are running a Copy Quality pass on a [N]-slide pitch deck. Score on 5 dimensions (1-10): Directness, Rhythm, Trust, Authenticity, Density.

Below 35/50: revise.

Run the Quick Checks on EVERY line. [paste checks list]

Here is ALL the copy: [paste all slide copy]

Flag any remaining issues with exact replacements. Score the full deck.
```

---

## How to Apply Results

1. Synthesize all four reports
2. Fix layout issues first (swap layouts, reorder slides) — these affect everything downstream
3. Fix design issues with `update_styles`
4. Fix narrative issues by rewriting affected slides' copy (re-read the content markdown file)
5. Fix copy issues with `set_text_content`
6. Screenshot changed slides to verify
7. This entire loop happens BEFORE presenting work to the user

## When NOT to Run

Skip for single-word text fixes or style-only changes (color, font size) that don't affect content.
