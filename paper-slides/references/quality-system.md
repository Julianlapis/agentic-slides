# Four-Pass Quality System

Run all four passes in parallel after every round of content changes. This is mandatory before presenting work to the user.

---

## Pass 1: Layout Intelligence

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

Read the complete copy across ALL slides. Score the full deck on 5 dimensions (1-10).

| Dimension | Question | What 10 looks like |
|-----------|----------|-------------------|
| Single-mindedness | Does each slide land exactly one idea? | You can state the slide's point in one sentence. If you need two, the slide is doing two jobs. |
| Redundancy | Are any ideas, phrases, or stats repeated across slides? | Each slide introduces something new. Zero repeated concepts, zero echoed phrasing. |
| Logical arc | Does each slide build on the one before it? | A stranger could read the deck in order and follow the argument without context. |
| Earned payoff | Does the closer feel like a conclusion the deck built toward? | The last slide uses language or concepts seeded earlier. Nothing arrives cold. |
| Specificity | Are claims grounded in concrete details, or floating as abstractions? | Named platforms, named roles, named workflows. No vague "the industry" or "teams everywhere." |

**Below 35/50 for the full deck: restructure before delivering.**

### Agent Prompt Template

```
You are a Narrative Flow Agent. Score the full deck on 5 dimensions (1-10): Single-mindedness, Redundancy, Logical arc, Earned payoff, Specificity.

Below 7 on any dimension: flag with specific slides and fixes.
Below 35/50 total: restructure.

Here is ALL the copy: [paste all slide copy]

Output dimension scores, total, and specific fixes for anything below 7.
```

---

## Pass 4: Copy Quality (Stop Slop)

Score the full deck copy on 5 dimensions (1-10).

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

**Below 35/50: revise before delivering.**

### Quick Checks (run on every line)

- Any adverbs (-ly words, "really," "just," "literally," "genuinely," "simply," "actually")? Kill them.
- Any passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb ("the decision emerges," "context flows," "data builds")? Name the person or system doing it.
- Sentence starts with a Wh- word? Restructure.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em-dash anywhere? Remove it.
- Vague declarative ("The implications are significant")? Name the specific implication.
- Narrator-from-a-distance ("Nobody designed this")? Put the reader in the scene.
- Lazy extremes ("every," "always," "never," "everyone")? Use specifics.
- Dramatic fragmentation ("[Noun]. That's it. That's the [thing].")? Justify or rewrite.
- Negative listing ("Not a X... Not a Y... A Z.")? State Z directly.
- False agency ("the complaint becomes a fix," "the culture shifts")? Name who did it.

### Phrases to Kill

**Throat-clearing openers:** "Here's the thing:" / "Here's what X" / "The uncomfortable truth is" / "It turns out" / "Let me be clear" / "Can we talk about"

**Emphasis crutches:** "Full stop." / "Let that sink in." / "This matters because" / "Make no mistake"

**Business jargon:** Navigate → Handle. Unpack → Explain. Lean into → Accept. Landscape → Situation. Game-changer → Significant. Deep dive → Analysis. Moving forward → Next. Circle back → Revisit.

**Adverbs to kill:** really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally, inherently, inevitably, interestingly, importantly, crucially.

**Filler phrases:** "At its core" / "In today's X" / "It's worth noting" / "At the end of the day" / "When it comes to" / "In a world where" / "The reality is"

**Meta-commentary:** "Hint:" / "Plot twist:" / "You already know this, but" / "X is a feature, not a bug"

### Structures to Avoid

**Binary contrasts:** "Not because X. Because Y." / "[X] isn't the problem. [Y] is." / "The answer isn't X. It's Y." State Y directly. Drop the negation.

**Negative listing:** "Not a X... Not a Y... A Z." State Z. The reader doesn't need the runway.

**Dramatic fragmentation:** "[Noun]. That's it. That's the [thing]." Complete sentences. Trust content over presentation.

**Rhetorical setups:** "What if [reframe]?" / "Here's what I mean:" / "Think about it:" Make the point. Let readers draw conclusions.

**False agency:** Giving inanimate things human verbs. "A complaint becomes a fix" → "The team fixed it." "The decision emerges" → "Someone decides." Name the human.

**Passive voice:** "X was created" → Name who created it. Every sentence needs a subject doing something.

### Agent Prompt Template

```
You are running a Stop Slop pass on a [N]-slide pitch deck. Score on 5 dimensions (1-10): Directness, Rhythm, Trust, Authenticity, Density.

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
