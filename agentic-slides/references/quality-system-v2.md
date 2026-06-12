# Four-Pass Quality System v2

Deduction-based scoring for agentic-slides. Every point is tied to a countable, verifiable pattern. No 1-10 subjective scales. Start at max, subtract for violations found. Every deduction cites a specific slide and a specific rule. Two agents scoring the same deck should arrive within 3 points of each other.

Modeled on voice-scoring.md. Same mechanics: per-instance costs, caps, free budgets, violation gates.

> **This rubric is the STANDARD layer.** It is operationalized by the `deck-score` workflow (`~/.claude/workflows/deck-score.js`, fired at Phase 5.1 per feedback entry PS-065). The workflow's agents read this file live — **edit here to raise the bar; the workflow mechanism stays stable.** Standard (this file) and mechanism (the workflow) are separate on purpose.

Run all four passes after every round of content changes. Mandatory before presenting work to the user.

**Critique-driven iteration:** For existing decks that need improvement, run /critique first to get a prioritized issue list. Then modify in place rather than rebuilding.

**Voice layers:** Agentic-slides output is client-facing. Apply both Layer 1 (`~/.claude/voice-dna.md`) and Layer 2 (`~/.claude/copy-polish.md`) during Pass 4.

---

## Architecture

Four scores, same deduction mechanic:

| Pass | Max Score | What it measures |
|------|-----------|-----------------|
| Layout Intelligence | /50 | Layout selection, variety, rhythm, pacing |
| Design Quality | /50 | Visual execution per slide |
| Narrative Flow | /60 | Argument structure across the deck |
| Copy Quality | /50 | Writing quality per voice-dna and copy-polish rules |

### Deck size normalization

All per-instance violation costs apply at these density thresholds:

| Deck size | Free violations per layer |
|-----------|-------------------------|
| Under 8 slides | 2 |
| 8-15 slides | 3 |
| 16-25 slides | 4 |
| 25+ slides | 6 |

"Free" means the violation is logged and reported but costs 0 points. Prevents small decks from inflating and large decks from deflating.

The budget applies **per layer**, not per pass or globally. A 16-slide deck gets 4 free violations in L1 AND 4 free in L2, etc. This matches voice-scoring.md's architecture.

**Exemption:** Presence checks (Pass 1 L3, Pass 2 L3, Pass 4 L5) are binary and exempt from the free budget, same as voice-scoring L4.

### Violation count gate

**Per pass, scaling with deck size:**

| Deck size | Gate (auto-fail if exceeded) |
|-----------|---------------------------|
| Under 8 slides | 10 |
| 8-15 slides | 13 |
| 16-25 slides | 16 |
| 25+ slides | 20 |

"Instance" means each individual occurrence. Six orphans = 6 instances. The gate counts all logged violations, including free-budget violations.

### Gestalt override

If Pass 4 L5 "point of view" fails (-3) AND the deck copy reads as assembled (reviewer answers "assembled" to the gestalt question: "Could any AI tool have generated this deck without human editorial judgment?"), the deck **auto-fails Pass 4 regardless of numeric score.**

This override prevents a technically clean but soulless deck from scoring 48/50. A piece can avoid all mechanical violations while fundamentally lacking authorial perspective.

---

## PASS 1: LAYOUT INTELLIGENCE (50 points)

### Layer 1: Content-Layout Fit (0-16 points at risk)

For each slide, check whether the layout matches the content shape. Violations are countable by comparing content structure to layout type.

| Violation | Test | Cost | Cap |
|-----------|------|------|-----|
| Item-count mismatch | Slide has N parallel items (e.g., 4 personas) but uses a layout designed for a different count (e.g., Left-Heavy instead of Cards/Multi-Column) | -3 per slide | -9 |
| Statement overload | Statement/Quote layout used on a slide with 3+ sentences of body copy | -2 per slide | -6 |
| Detail on a divider | Section Divider slide carries more than 1 sentence of body copy | -2 per slide | -4 |
| Wrong density class | Content classified as Dense on a Sparse layout, or Sparse content on a Dense layout (see definitions below) | -2 per slide | -6 |

**Layer cap: -16.**

**Density class definitions (for "wrong density class" test):**

| Class | Content shape | Example layouts |
|-------|--------------|----------------|
| **Sparse** | Single statement, ≤2 sentences, no list | Statement, Quote, Section Divider, Title |
| **Medium** | 1-3 short paragraphs or a headline + 2-3 supporting points | Left-Heavy, Eyebrow + 2-Column, Split Comparison |
| **Dense** | Bullet list (4+ items), data table, multi-item comparison, 3+ paragraphs | Cards, Multi-Column, Phase Cards, Grid |

A mismatch is: Dense content on a Sparse layout, or Sparse content on a Dense layout. Medium content on any layout is acceptable.

**How to test:** Extract the content plan. For each slide, classify content into Sparse/Medium/Dense using the table above. Check against the layout's class. A cross-class mismatch (Sparse↔Dense) = violation. Medium is always safe.

### Layer 2: Variety and Rhythm (0-18 points at risk)

| Violation | Test | Cost | Cap |
|-----------|------|------|-----|
| Layout repetition | Same layout type appears 4+ times in the deck. Count = appearances minus 3. | -2 per occurrence over 3 | -8 |
| Layout drought | Deck uses fewer than (total slides / 4, rounded up) distinct layout types. E.g., a 16-slide deck needs 4+ distinct layouts. | -3 | -3 |
| Dense-slide run | 3+ consecutive slides with body copy exceeding 40 words each, with no breathing slide (Statement, Quote, Section Divider) between them | -3 per run | -6 |
| Sparse-slide run | 3+ consecutive slides with under 15 words each (all Statement/Divider with no content slides between) | -2 per run | -4 |
| Identical adjacency | Two consecutive slides use the exact same layout type | -1 per pair | -4 |

**Layer cap: -18.**

**How to test:** List all layouts in sequence. Count distinct types. Count consecutive same-type pairs. Count runs of dense or sparse slides. All mechanical.

**Layout drought threshold change from v2-draft:** Relaxed from total/3 to total/4 (rounded up). A 16-slide deck needs 4 distinct layouts, not 5. This is achievable with standard layout libraries.

### Layer 3: Structural Placement (0-8 points at risk, no free budget)

Binary presence/absence checks for deck structure.

| Check | Test | Cost if wrong |
|-------|------|---------------|
| Title position | Title slide is not slide 1 | -3 |
| Closer position | Closing/Thank You slide is not the final slide | -3 |
| Orphaned divider | Section Divider with no content slides following it before the next divider or end of deck | -2 per instance, cap -4 |
| Missing divider | Deck has 3+ distinct content sections (identified by eyebrow labels or topic shifts between consecutive slides) with no Section Dividers marking transitions | -3 |

**Layer cap: -8.**

**"Thematic section" definition (for Missing divider test):** A new thematic section starts when the eyebrow label changes (e.g., "THE SITUATION" → "THE OPPORTUNITY") OR when the topic shifts without a shared thread to the previous slide. Count sections by counting distinct eyebrow labels. If the deck doesn't use eyebrows, count topic shifts where two consecutive slides share no vocabulary or logical connection.

### Layer 4: Pacing (0-8 points at risk)

| Violation | Test | Cost | Cap |
|-----------|------|------|-----|
| Front-loaded density | More than 60% of slides with 40+ words of body copy appear in the first half of the deck | -3 | -3 |
| Back-loaded density | More than 60% of slides with 40+ words appear in the second half | -3 | -3 |
| No breathing room | Deck has 10+ content slides with zero Statement, Quote, or Section Divider slides | -3 | -3 |

**Layer cap: -8.**

**How to test:** Count slides with 40+ words of body copy. Note their position (first half vs. second half). Check for presence of breathing slides. All mechanical.

---

## PASS 2: DESIGN QUALITY (50 points)

Screenshot every slide. Violations are countable from visual inspection.

### Layer 1: Typography (0-14 points at risk)

| Violation | Test | Cost | Cap |
|-----------|------|------|-----|
| Orphan | Single word alone on the last line of a text block | -1 per instance | -4 |
| Runt | Line with fewer than 3 words that isn't the last line | -1 per instance | -3 |
| Text overflow | Text clipped, truncated, or overlapping another element (including footers) | -3 per instance | -6 |
| Missing type hierarchy | Content slide has fewer than 2 distinct type sizes with at least 8px difference between them (headline and body must be visually distinct, not just technically different) | -2 per slide | -4 |
| Line length | Body text line exceeds 75 characters on a single line | -1 per instance | -3 |

**Layer cap: -14.**

### Layer 2: Spatial (0-14 points at risk)

| Violation | Test | Cost | Cap |
|-----------|------|------|-----|
| Element collision | Two elements overlap unintentionally (text on text, text on image boundary, element on footer). Intentional overlaps (e.g., text over a background image with sufficient contrast) are not violations. | -3 per instance | -6 |
| Alignment break | Element is visually off-grid from other elements on the same slide (> 8px misalignment from the nearest element sharing the same alignment lane). Centered elements are their own lane and don't violate left-aligned elements. | -2 per instance | -6 |
| Gutter inconsistency | Spacing between parallel items varies by > 20% within the same slide | -2 per slide | -4 |
| Dead zone | More than 40% of a non-Statement slide's area contains no content elements. Statement, Quote, and Section Divider slides are exempt (whitespace is deliberate on sparse layouts). | -1 per slide | -3 |

**Layer cap: -14.**

### Layer 3: Contrast and Color (0-10 points at risk, no free budget)

Binary checks per slide. Exempt from free budget.

| Check | Test | Cost |
|-------|------|------|
| Body text contrast | Body text on its background fails WCAG AA contrast (< 4.5:1 ratio) | -3 per slide, cap -6 |
| Headline contrast | Headline text on its background fails WCAG AA Large Text contrast (< 3:1 ratio for text 18px+ or 14px+ bold) | -2 per slide, cap -4 |
| Surface consistency | Slide uses a surface color not in the deck's defined palette | -2 per slide, cap -4 |

**Layer cap: -10.**

### Layer 4: Visual Completeness (0-12 points at risk)

| Violation | Test | Cost | Cap |
|-----------|------|------|-----|
| Missing footer | Slide is missing the standard footer/branding element present on other slides (when deck has a footer pattern) | -2 per slide | -4 |
| Inconsistent footer | Footer content, position, or style differs between slides that should match | -1 per slide | -3 |
| Placeholder visible | Placeholder text ("Lorem ipsum," "[insert]," "TODO") visible on slide | -3 per instance | -6 |
| Empty frame | Visible empty frame or container with no content | -2 per instance | -4 |

**Layer cap: -12.**

---

## PASS 3: NARRATIVE FLOW (60 points)

Read the complete copy across ALL slides. Every dimension has a formula. The agent MUST compute the formula, show the math, and justify the score. Qualitative judgment without the formula is not a valid score.

### Layer 1: Argument Structure (0-20 points at risk)

| Violation | Formula | Cost |
|-----------|---------|------|
| Multi-idea slide | Count slides carrying 2+ distinct ideas. A slide carries 2 ideas if you cannot summarize it in one sentence without using "and" to join two unrelated claims. | Cap -8 |
| Redundant slide | Two slides make the same core argument. Test: write each slide's argument as one sentence. If two sentences could be combined into one without losing meaning, they're redundant. | -3 per pair, cap -6 |
| Broken transition | Read headline N then headline N+1. A transition is broken if N+1 shares no vocabulary, logical progression, or causal link with N. | -2 per break, cap -8 |

**Layer cap: -20.**

**How to test Multi-idea (disambiguation):**
1. Write ONE sentence summarizing the slide's argument.
2. If the sentence uses "and" to join two claims ("We should enter the market AND demand is growing"), check: are the claims dependent (entering BECAUSE demand is growing) or independent?
3. Dependent = one idea. Independent = two ideas.

### Layer 2: Arc and Payoff (0-16 points at risk)

| Violation | Formula | Cost |
|-----------|---------|------|
| Late tension | The core tension (what's at stake, what's unresolved) doesn't appear until after slide 4 in a deck of 12+ slides, or after slide 3 in a deck under 12 | -4 |
| Unearned closer | Count callback terms in final 3 slides that appeared in the first half. 0 callbacks = -6, 1 = -4, 2 = -2, 3 = -1, 4+ = 0 | -6 max |
| Missing "so what" | A content slide ends without connecting to the reader's situation or next step. Count slides that just state facts without stakes. | -2 per slide, cap -6 |
| Arc gap | Deck jumps from problem to solution without a diagnosis slide (what's causing the problem). Exempt for capability decks where the audience already knows the problem. | -4 |

**Layer cap: -16.**

### Layer 3: Specificity and Evidence (0-14 points at risk)

| Violation | Formula | Cost |
|-----------|---------|------|
| Ungrounded claim | Claim without a specific number, name, or concrete example. Count claims in body copy only (headlines are arguments, not claims requiring evidence). If grounded ratio < 75%, deduct per ungrounded claim. | -2 per ungrounded claim, cap -8 |
| Headline label | Headline is a topic label ("The Market") instead of an argument. Test: does the headline make a claim a reader could disagree with? If no, it's a label. | -3 per label, cap -6 |

**Layer cap: -14.**

**Grounded ratio threshold change from v2-draft:** Relaxed from 80% to 75%. Not every claim in a proposal needs a footnote. The threshold catches decks that make mostly unsubstantiated claims without penalizing decks that have a few assertions supported by context rather than numbers.

### Layer 4: Headline Narrative (0-10 points at risk, no free budget)

Cover all body copy. Read ONLY headlines in sequence. Binary test.

| Check | Test | Cost |
|-------|------|------|
| Headline-only story | Read all headlines in order. If a stranger cannot follow the argument from headlines alone (requires body copy to make sense), this fails. | -5 |
| Headline structure repetition | More than 50% of headlines use the same syntactic opener (all start with "Your...", all start with "We...", all are questions). Count openers; if >50% match, flag. | -3 |
| Headline echo | Two headlines use the same key phrase (4+ words repeated verbatim) | -2 per pair, cap -4 |

**Layer cap: -10.**

---

## PASS 4: COPY QUALITY (50 points)

**Agent: `voice-review`** (`~/.claude/agents/voice-review.md`). Reads voice-dna.md and copy-polish.md fresh from disk. This pass incorporates both Voice and Polish checks from voice-scoring.md, adapted for deck copy.

**Gestalt question (mandatory):** After all layers, the reviewer answers: "Could any AI tool have generated this deck without human editorial judgment?" If yes AND L5 "point of view" fails, the deck auto-fails Pass 4 regardless of numeric score.

### Layer 1: Mechanical (0-18 points at risk)

Same as voice-scoring.md Voice L1. Count per-instance violations:

| Violation | Cost | Cap |
|-----------|------|-----|
| Banned phrase | -2 | -8 |
| The Big One ("not X, this is Y") | -5 | auto-fail |
| Em dash | -1 | -4 |
| Adverb | -1 | -4 |
| False agency | -1 | -4 |
| Passive voice | -1 | -4 |
| Throat-clearing | -2 | -4 |
| Vague declarative | -1 | -4 |
| Generic insider claim ("nobody," "most people don't realize") | -3 | -6 |

**Layer cap: -18.**

### Layer 2: Density (0-14 points at risk)

Slide copy must earn every word.

| Violation | Test | Cost | Cap |
|-----------|------|------|-----|
| Word count exceeded | Statement slide > 30 words body. Argument slide > 60 words body. Evidence slide > 50 words body. Framework/Scope slides: structured list format required, no prose paragraphs. | -2 per slide | -6 |
| Detail masquerading as argument | A body sentence adds detail to the same point as the previous sentence instead of advancing. Test: can you merge the two sentences into one without losing a distinct claim? If yes, it's elaboration. A deliberate emphasis restatement (same idea, sharper language) is not a violation. | -1 per instance | -4 |
| Body copy restates headline | Body copy's first sentence paraphrases the headline instead of advancing past it | -2 per slide | -6 |

**Layer cap: -14.**

**DENSITY HARD GATE:** Any content slide where body copy exceeds 2x its type's word limit (Statement > 60, Argument > 120, Evidence > 100) is an automatic flag regardless of total score. The agent must report: word count, type classification, and which sentences to cut.

### Layer 3: Cadence and Rhythm (0-10 points at risk)

Adapted from voice-scoring.md Voice L2 for deck copy.

| Pattern | Test | Cost |
|---------|------|------|
| Manifesto cadence | Count slide-final sentences. If >60% are punchy declaratives (under 10 words), quotable kickers (screenshot-worthy), or tricolon closers (three parallel items). Threshold is 60% (vs. voice-scoring's 50%) because deck copy has more natural kickers per slide. | -3 |
| Manifesto cadence (severe) | If >75%: | -5 (replaces -3) |
| Metronomic rhythm | 3+ consecutive sentences within 2 words of each other in length, within a single slide's body copy | -2 per instance, cap -4 |
| Repeated phrase | Same phrase (4+ words) appears in body copy of 3+ different slides. Threshold is 3 slides (vs. voice-scoring's 2 sections) because slides are shorter units; repetition across 2 short slides is less noticeable than across 2 long sections. | -2 per instance, cap -4 |

**Layer cap: -10.**

### Layer 4: Register and Polish (0-12 points at risk)

Combines voice-scoring Voice L3 and key Polish checks.

| Violation | Cost | Cap |
|-----------|------|-----|
| Register break | Sentence is formally or informally mismatched with the deck's established register. A deliberate register shift (colloquial line after formal passage, per voice-dna) is not a break. A break feels accidental, like a different author wrote that line. | -2 per instance | -4 |
| Consultant phrase (copy-polish banned list) | -2 per instance | -6 |
| Unexpanded acronym on first use | -1 per instance | -3 |
| Overloaded sentence (2+ distinct ideas joined by "and," "but," "which," or comma splice) | -1 per instance | -3 |
| Qualifier surviving ("somewhat," "relatively," "arguably," "to some extent") | -1 per instance | -3 |

**Layer cap: -12.**

### Layer 5: Voice Presence (0-8 points at risk, no free budget)

Binary checks. Exempt from free budget.

| Marker | Test | Cost if absent |
|--------|------|---------------|
| Physical verbs | Fewer than 1 per 300 words in deck body copy ("sanded down," "bolted on," "stripped back," "wired," etc.). Matches voice-scoring.md canonical threshold. | -2 |
| Register shifts | Deck body copy (500+ words) has fewer than 2 natural register shifts (a colloquial line after a formal passage, or vice versa) | -2 |
| Specificity | Any content slide lacks a specific number, name, or concrete detail | -1 per slide, cap -3 |
| Point of view | Copy could describe any company in the same industry by swapping proper nouns. Nothing is specific to this client, product, or situation. | -3 |

**Layer cap: -8.**

Decks with under 400 words of total body copy are exempt from physical verbs and register shifts checks.

---

## Score Interpretation

| Score Range | Label | What it means |
|-------------|-------|---------------|
| **46-50** (Pass 1/2/4) or **55-60** (Pass 3) | Flawless | 0-2 minor violations. Ships without discussion. |
| **40-45** / **48-54** | Ships | A few violations, nothing structural. General audience won't notice. |
| **35-39** / **42-47** | Passes threshold | Multiple violations across 2+ layers. Functional. Fix before discerning audience. |
| **30-34** / **36-41** | Needs work | Significant violations. Fix before delivering. |
| **<30** / **<36** | Does not ship | Major failures or violation gate triggered. |

### Thresholds

| Context | Pass 1 | Pass 2 | Pass 3 | Pass 4 |
|---------|--------|--------|--------|--------|
| Internal draft | 30/50 | 30/50 | 36/60 | 30/50 |
| Standard client deck | 35/50 | 35/50 | 42/60 | 35/50 |
| High-stakes pitch | 40/50 | 40/50 | 48/60 | 40/50 |

---

## Cross-System Routing

When content moves through the pipeline, each system scores at its stage. They don't stack:

| Stage | System | Scores |
|-------|--------|--------|
| Raw strategy doc (before slides) | quality-gates.md | /50 |
| Slide-ready narrative (before deck build) | narrative-reviewer.md | /70 |
| Final deck (built in Figma/Paper) | quality-system-v2.md | /50+/50+/60+/50 |
| Copy at any stage | voice-scoring.md (delegated) | Voice /50 + Polish /50 |

**Deduplication rule:** If two systems flag the same specific instance (e.g., an ungrounded claim scored in Pass 3 L3 and also caught by voice-scoring Polish L3 via Pass 4), charge the higher deduction only. Do not double-count the same sentence.

## How to Apply Results

1. Synthesize all four reports
2. Fix layout issues first (swap layouts, reorder slides) — these affect everything downstream
3. Fix design issues (text overflow, alignment, spacing)
4. Fix narrative issues by rewriting affected slides' copy
5. Fix copy issues with text edits
6. Screenshot changed slides to verify
7. This loop happens BEFORE presenting work to the user

## When NOT to Run

Skip for single-word text fixes or style-only changes (color, font size) that don't affect content.

---

## Changelog

- 2026-04-28: v1. Five dimensions x 1-10 subjective scales per pass.
- 2026-04-30: v2-draft. Replaced all subjective 1-10 scales with deduction-based axioms modeled on voice-scoring.md.
- 2026-04-30: v2-final. Post-review fixes from completeness and calibration reviewers:
  (1) Free budget changed from per-pass to per-layer, matching voice-scoring.md architecture.
  (2) Violation gate now scales with deck size (10/13/16/20) instead of fixed 12.
  (3) Added gestalt override: auto-fail if assembled + no POV, matching voice-scoring.
  (4) Added Pass 4 L3: Cadence and Rhythm (manifesto cadence, metronomic rhythm, repeated phrase) from voice-scoring Voice L2. Closes the biggest gap: rhythmically dead AI copy.
  (5) Added Pass 4 L4: overloaded sentences and qualifiers from voice-scoring Polish L2.
  (6) Expanded Pass 4 L5 Voice Presence: added register shifts check, raised physical verbs to 1/300 (canonical), added short-deck exemption.
  (7) Added Pass 1 L4: Pacing (front/back-loaded density, no breathing room). Restores v1's pacing check.
  (8) Sharpened ambiguous tests: density class definitions table, thematic section definition, multi-idea disambiguation, alignment lane clarification, dead zone exemption for sparse layouts, headline contrast using WCAG AA Large Text (3:1), register break vs. deliberate shift guidance, detail-vs-elaboration exemption for emphasis restatements.
  (9) Added density hard gate: 2x word limit = automatic flag regardless of score.
  (10) Relaxed layout drought threshold from total/3 to total/4. Relaxed grounded claim ratio from 80% to 75%.
  (11) Late tension threshold now scales with deck size (slide 4 for 12+, slide 3 for <12).
  (12) Unearned closer scale expanded: 3 callbacks = -1, 4+ = 0 (was 3+ = 0).
