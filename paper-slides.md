---
name: paper-slides
description: Build production-quality presentation decks in Paper (the design tool) from any source material. Use when the user wants to create slides, a deck, or a presentation in Paper using the Paper MCP tools. Handles content distillation, visual design, layout variety, copy quality, and PDF export. Trigger when the user mentions "deck," "slides," "presentation," "pitch deck," or "conference talk" while working in Paper. Also trigger when the user pastes or references ANY content (outline, doc, article, transcript, notes, URL) and wants it turned into something visual. Even if they don't say "slides" explicitly, if they're in Paper and have content that could become a multi-slide deck, use this skill.
---

# Paper Slides

A layout intelligence engine. Takes content + design system, produces beautiful decks on the Paper canvas.

## FIRST: Read Feedback Log

**Before doing anything else**, read [feedback-log.md](feedback-log.md). It contains binding corrections from previous sessions. Every rule in that file overrides default behavior. At the end of every session, capture any new user corrections and append them to the log.

## What This Skill Is

A design brain that can lay out any kind of deck: strategy, portfolio, capabilities, case study, pitch, thought leadership, research, workshop. The skill doesn't care about deck type. It cares about content structure, visual rhythm, and layout intelligence.

## Core Philosophy

1. **Content and Design System Are Separate Inputs.** The content lives in a markdown file. The design system lives in its own file. The skill applies one to the other. Neither is optional.
2. **Layout Is the Skill.** Choosing which layout pattern fits which content, then sequencing them for narrative rhythm across the full deck. This is the hard part. This is what the skill does.
3. **Restraint Over Decoration.** Fewer elements, highly refined. White space is a feature.
4. **Incremental Building.** Each `write_html` call produces ONE visual group. The user sees progress every few seconds.
5. **Quality Is Mandatory.** The four-pass quality system runs after every round of changes. See [references/quality-system.md](references/quality-system.md).

---

## Hard Requirements (Gate Check)

Before building anything, verify these two inputs exist. If either is missing, stop and resolve.

### 1. Content File (REQUIRED)

A markdown file containing all deck content, structured by slide. This file is the single source of truth for what goes on each slide. It persists across context window changes.

**If the user provides raw content (outline, doc, paste, URL):** distill it into a content markdown file first. Save it to the user's working directory. Present it for approval before building.

**Content file format:**
```markdown
# [Deck Title]

## Slide 1: [Slide Name]
- **Type:** [title | section-divider | content | quote | image-gallery | etc.]
- **Eyebrow:** [optional label]
- **Headline:** [main text]
- **Subtitle:** [optional]
- **Body:** [optional paragraph or bullets]
- **Images:** [optional: count, descriptions, or file paths]
- **Layout:** [assigned in Phase 2]

## Slide 2: [Slide Name]
...
```

Reference this file throughout the build. When context gets long, re-read it rather than relying on memory.

### 2. Design System (REQUIRED, with default fallback)

A markdown file defining palette, typography, spacing, and structural rules.

**If the user provides a design system file:** use it. Follow it exactly.

**If no design system is provided:** use the default system. See [references/default-design-system.md](references/default-design-system.md). This is a minimal monochromatic system (black/gray/white, single grotesque font, hierarchy through size contrast). It works for any deck type.

**The user can also provide:**
- A reference PPTX to extract a system from (use `markitdown` + python-pptx analysis)
- A Figma file to screenshot and extract from
- A PDF to analyze visually
- A description ("make it feel like [X]") to generate a custom system

Design systems are additive. The user can feed in more reference decks over time, and the layout pattern repository grows.

---

## Before You Start

1. **`get_basic_info`** — File structure, artboards, loaded fonts.
2. **`get_font_family_info`** — Verify font availability and weights. Do this before writing any styles.
3. **`get_selection`** — Check what the user is focused on.
4. **Confirm both inputs.** Content file exists? Design system identified? If not, create them.

---

## Phase 1: Content Structuring

Take whatever the user provides and produce the content markdown file.

**From an outline:** Map each point to a slide. Identify narrative arc, slide breaks, slide count.

**From long-form content:** Identify the 3-5 core arguments. Find the single most compelling sentence per argument (headline). Distill supporting evidence to 1-2 sentences (body). Discard everything else.

**From a reference deck (PDF/PPTX):** Extract text, note visual structure, decide with user whether to replicate or create new direction.

**From a topic (no content):** Research, then build outline. Get approval before proceeding.

Save the content file. Present the slide outline for approval:
```
01 — [Type] [Eyebrow]: [Headline]
02 — [Type] [Eyebrow]: [Headline]
...
```

---

## Phase 2: Layout Planning

This is the core intelligence of the skill. Read the full content file. Understand the narrative arc. Then assign a layout to every slide.

### How Layout Selection Works

1. **Read the full story first.** Don't assign layouts slide-by-slide in isolation. The sequence matters. A quote slide after three dense content slides creates a breathing moment. Two image-heavy slides back-to-back exhausts the eye.

2. **Match content shape to layout shape.** Each slide's content has a natural shape:
   - One big idea, no supporting text → Statement or Section Divider
   - Headline + body paragraph → Left-Heavy or Eyebrow + 2-Column
   - Headline + 3-5 parallel items → Cards or Multi-Column Text
   - Headline + images → Image Gallery or Case Study Detail
   - Pull-quote or testimonial → Quote
   - Team or people → People/Bio Grid
   - Navigation/structure → Agenda/TOC
   - Pure visual evidence → Image Mosaic
   - Closing → Thank You/Contact

3. **Sequence for rhythm.** After assigning individual layouts:
   - Check: no same layout back-to-back
   - Check: image-heavy slides separated by text slides
   - Check: at least 4 different layout types in a 10-slide deck
   - Check: statement/quote slides at section transitions
   - Check: density gradient makes sense (don't front-load all dense slides)

4. **Update the content file** with layout assignments. Each slide gets a `Layout:` field.

The full layout pattern library is in [references/layouts.md](references/layouts.md). This library grows as the user feeds in more reference decks.

### Present the Layout Plan

Before building, show the user the full plan:
```
01 — Statement: [Headline] (dark bg)
02 — Agenda: [5 sections]
03 — Section Divider: "01 [Section Name]"
04 — Eyebrow + 2-Column: [Headline] + [Body]
05 — Image Gallery: [Headline] + 4 images
06 — Quote: [Pull quote + attribution]
...
```

Wait for approval. The user may want to swap layouts, reorder slides, or adjust density.

---

## Phase 3: Design Brief

Read the design system file (provided or default). Extract and confirm:

```
DESIGN BRIEF
─────────────
System: [file path or "default"]
Palette: [background, text primary, text secondary, accent (if any)]
Typography: [font family, weight range, size scale]
Spacing: [artboard padding, section gap, element gap, image grid gap]
Structural: [dividers, corners, shadows — what's allowed, what's banned]
```

Check font availability with `get_font_family_info` before committing.

---

## Phase 4: Build

### Artboard Setup
- Default: 1440 x 810px (16:9)
- Position: `(slide_index - 1) * 1520` for left value, consistent top
- Name: `[number] — [Short Name]`

### Content Architecture
Every slide: content frame (flex-grow: 1, pushes footer to bottom) + footer (per design system).

### Building Order
1. Create artboard
2. Add background elements FIRST (textures, glows, gradients — Paper renders first child at the back)
3. Add content frame + footer AFTER backgrounds
4. Add text elements one group at a time
5. Screenshot to verify every 2-3 slides

### Efficiency
After building 2-3 unique slides, clone similar layouts with `duplicate_nodes` and modify with `update_styles` / `set_text_content`.

### Re-read the Content File
After every 5-6 slides, re-read the content markdown file to verify you haven't drifted from the source content. Context windows compress. The file doesn't.

For typography rules and troubleshooting, see [references/typography.md](references/typography.md).
For common mistakes to avoid, see [references/anti-patterns.md](references/anti-patterns.md).

---

## Phase 5: Quality System (MANDATORY)

After every round of content changes, run the four-pass quality system BEFORE telling the user the work is done.

1. **Layout Intelligence Agent** — Reviews the full slide sequence. Checks: layout variety, rhythm, content-to-layout fit, density pacing, section transitions. Suggests layout swaps where the current choice doesn't serve the content.
2. **Design Quality Agent** — Screenshots every slide, scores on Hierarchy/Balance/Typography/Alignment/Contrast. Below 35/50 per slide: fix.
3. **Narrative Flow Agent** — Reads all copy (re-read the content file), scores on Single-mindedness/Redundancy/Logical arc/Earned payoff/Specificity. Below 35/50: restructure.
4. **Copy Quality (Stop Slop) Pass** — Runs quick checks on every line for false agency, passive voice, adverbs, throat-clearing, vague declaratives, dramatic fragmentation. Below 35/50: revise.

Launch all four as parallel background agents. Synthesize reports. Apply fixes in one batch. Screenshot to verify.

Full scoring rubrics, agent prompt templates, and the complete stop-slop checklist are in [references/quality-system.md](references/quality-system.md).

---

## Phase 6: Export

See [references/pdf-export.md](references/pdf-export.md) for the complete pipeline.

**Quick path:** Build an HTML file with all slide content (manually written from the current copy, using the design system's colors/fonts/layouts). Render with Puppeteer using the system Chrome. This is faster and more reliable than JSX extraction.

**Critical:** Use `@import` for Google Fonts. Wait for `document.fonts.ready` before rendering. Set `printBackground: true`.

---

## Optional Review Modes

The user may request these specialized review passes:

**Black Hat Strategist:** Evaluate the deck's strategy for logical gaps, unfounded assumptions, blind spots, and structural fragility. Find every reason the argument will fail.

**Black Hat Editor:** Evaluate the writing for clarity without distinctiveness, false humanity, dead weight, and tonal inconsistency. Quote the offending lines.

**Copy Style Extraction:** Ingest a reference deck (PDF or screenshots), extract the copy patterns (headline style, body length, accent usage, eyebrow convention), and apply them to the current deck.

**Design System Ingestion:** Ingest a PPTX, PDF, or Figma file. Extract the palette, type scale, spacing grid, structural elements, and layout patterns. Save as a new design system markdown file in the references folder.

---

## Session Flow

1. User provides content (or topic to research)
2. **Create content markdown file** — distill, structure, save
3. **Identify design system** — user-provided, or confirm default
4. **Layout planning** — assign layouts to all slides, present full plan
5. User approves or adjusts plan
6. Verify font availability
7. Build title slide → screenshot → **wait for user reaction**
8. Build remaining slides (2-3 at a time, screenshot between batches)
9. Re-read content file every 5-6 slides to prevent drift
10. Run four-pass quality system (including layout intelligence)
11. Apply fixes, verify with screenshots
12. User requests adjustments → apply to ALL affected slides, re-run quality
13. Export to PDF when ready

Always call `finish_working_on_nodes` when done editing.

---

## Growing the Layout Library

The layout patterns in [references/layouts.md](references/layouts.md) are not fixed. When the user provides a new reference deck (PPTX, PDF, Figma), analyze it for layout patterns not already in the library. If new patterns are found, add them to `layouts.md` with the same structure: name, when to use, structure spec. The library gets smarter with every deck the user feeds in.
