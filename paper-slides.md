---
name: paper-slides
description: Build production-quality presentation decks in Paper (default) or Figma from any source material. Use when the user wants to create slides, a deck, or a presentation. Handles content distillation, visual design, layout variety, copy quality, and export. Trigger when the user mentions "deck," "slides," "presentation," "pitch deck," or "conference talk." Also trigger when the user pastes or references ANY content (outline, doc, article, transcript, notes, URL) and wants it turned into something visual. Even if they don't say "slides" explicitly, if they have content that could become a multi-slide deck, use this skill. Paper is the default canvas. If the user says "in Figma" or provides a Figma file URL, use the Figma canvas path instead.
---

# Agentic Slides

A layout intelligence engine. Takes content + design system, produces beautiful decks on Paper (default) or Figma.

## FIRST: Read Feedback Log

**Before doing anything else**, read [feedback-log.md](feedback-log.md). It contains binding corrections from previous sessions. Every rule in that file overrides default behavior. At the end of every session, capture any new user corrections and append them to the log.

## MANDATORY: Never Skip Phases

**This skill has phase gates. They are not optional. They are not skippable when the task "seems simple" or when you "already have the content in context."**

On 2026-03-24, all phase gates were skipped. The essay was read, the slide breakdown was eyeballed, and copy was written directly into Paper artboards with no structured extraction, no AskUserQuestion approval, no anti-blandification check, and no voice quality pass on the slide copy. The result: 16 slides of flattened, generic summaries that stripped the voice from a document that took 5 sessions to craft.

**The rule:** If you are building slides from any source material, you MUST execute Phase 1 (Content Structuring) with the AskUserQuestion gate BEFORE touching Paper or Figma. There are zero exceptions. "The user asked me to just build it" is not an exception. "I already read the source document" is not an exception. "The content is short enough to hold in context" is not an exception. The phase exists to prevent summarization reflex, which happens every time the gate is skipped.

**How to self-check:** Before your first `create_artboard` or `use_figma` call, verify:
1. Does a content markdown file exist on disk with slide-by-slide copy? If no, STOP.
2. Did the user approve the slide breakdown via AskUserQuestion? If no, STOP.
3. Does every slide's body copy trace back to specific source lines? If no, STOP.

If any answer is no, you are about to skip the gates. Go back to Phase 1.

---

## Canvas Selection

This skill builds on two canvases. Paper is the default.

**Paper (default):** Uses Paper MCP tools (`write_html`, `get_screenshot`, `update_styles`, etc.). Builds incrementally with HTML. Exports to PDF via screenshot pipeline. Best for rapid iteration and solo workflows.

**Figma:** Uses the official Figma MCP `use_figma` tool to write directly to the Figma canvas via the Plugin API. Builds with real Figma frames, auto-layout, components, and variables. The output is a native Figma file your team can edit, comment on, and hand off. Best for team workflows and design system integration.

**How to select:**
- Default: Paper. No need to specify.
- If the user says "in Figma", provides a Figma file URL, or asks to build using their Figma design system → use Figma.
- If the user says "export to Figma" after building in Paper → use the Figma export pipeline (see Phase 6).

**Figma requirements:** The Figma MCP server must be connected (available as a claude.ai integration). The user needs to provide a Figma file key or URL for the target file.

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

### Paper (default)
1. **`get_basic_info`** — File structure, artboards, loaded fonts.
2. **`get_font_family_info`** — Verify font availability and weights. Do this before writing any styles.
3. **`get_selection`** — Check what the user is focused on.
4. **Confirm both inputs.** Content file exists? Design system identified? If not, create them.

### Figma
1. **Get the file key.** Extract from the Figma URL (`figma.com/design/:fileKey/...`) or ask the user.
2. **`mcp__claude_ai_Figma__get_metadata`** — Understand file structure, pages, existing components.
3. **`mcp__claude_ai_Figma__search_design_system`** — Check for existing design system components, variables, and styles to reuse.
4. **Test `use_figma` access** — Run a simple probe: `return { ok: true, timestamp: Date.now() }`.
5. **Confirm both inputs.** Content file exists? Design system identified? If not, create them.

---

## Phase 1: Content Structuring

Take whatever the user provides and produce the content markdown file.

### The Core Rule: Extract, Don't Summarize

The source document IS the copy. The job is to select which lines go on which slides, not to rephrase them in blander language. If a line from the source needs shortening, cut words from the line. Don't rewrite it.

**Why this rule exists:** In the 2026-03-24 Imitation Premium session, a 1,582-word essay (voice-checked at 38/50, distilled from 6 versions and 2 courtroom rounds) was turned into slide copy that "bland-ified" the source. Physical verbs were replaced with neutral summaries. Rhythmic cascades ("A pirated highlight became an on-ramp. A remix started a conversation. Each unauthorized clip invited someone new into a world that rewards knowledge") were flattened to single generic sentences. The sharpness that took 5 sessions to build was lost in one pass because the skill summarized instead of extracting.

### Input Types

**From an outline:** Map each point to a slide. Identify narrative arc, slide breaks, slide count.

**From long-form content (essay, strategy doc, article):**

1. **Read the full source.** Mark every sentence that could be a headline (punchy, specific, one idea). Mark every sentence that carries evidence (names, numbers, examples). Mark every sentence with strong voice texture (physical verbs, register shifts, rhythm).
2. **Map sections to slides.** Each essay section or argument becomes 1-3 slides depending on density. Don't compress a section with 3 distinct ideas into 1 slide.
3. **For each slide, extract lines verbatim from the source:**
   - **Headline** = the sharpest line from that section. Promote it directly. If no line works at display size, that's a signal the section needs work, not a signal to write a generic replacement.
   - **Body** = the 2-3 sentences that add the most evidence or texture. Lift them. Don't rewrite.
   - **Source attribution** = note which paragraph/line numbers each slide draws from. This creates a traceable chain.
4. **If you must shorten a line:** cut words from the original. Don't rephrase. "Commissioner Adam Silver called it 'snacks versus meals': give fans the highlights for free, and they'll still pay for the games" can lose "Commissioner" but should never become "The NBA adopted an open content strategy."

**From a reference deck (PDF/PPTX):** Extract text, note visual structure, decide with user whether to replicate or create new direction.

**From a topic (no content):** Research, then build outline. Get approval before proceeding.

### Mandatory: AskUserQuestion Gate

Before writing any slide copy, present the proposed slide breakdown to the user using AskUserQuestion:

```
Proposed slide breakdown from [source document]:

01 — [Type]: [Headline extracted from source, with line reference]
02 — [Type]: [Headline extracted from source, with line reference]
...

[N] slides total. Source lines not assigned to any slide: [list any orphaned content].

Does this breakdown capture the argument? Any sections that need more or fewer slides?
```

Wait for approval. The user may want to reassign lines, add slides for underserved sections, or flag lines that must appear verbatim.

### Anti-Blandification Check (run after extraction, before building)

Compare each slide's body copy against its source paragraph. For each slide, ask:
- Did I lose a physical verb? Restore it.
- Did I cut a specific name or number? Restore it.
- Did I flatten a rhythm (short-long-short) into uniform sentence length? Restore the rhythm.
- Did I replace the author's phrasing with a neutral summary? Revert to the original.
- Does the two-column split make sense structurally (claim + proof), or did I default to "summary left, evidence right"?

If any answer is yes, fix it before proceeding to layout.

### Save and present

Save the content file. Present the slide outline for approval:
```
01 — [Type] [Eyebrow]: [Headline] (source: ¶3)
02 — [Type] [Eyebrow]: [Headline] (source: ¶5-6)
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

### Paper Path (default)

#### Artboard Setup
- Default: 1440 x 810px (16:9)
- Position: `(slide_index - 1) * 1520` for left value, consistent top
- Name: `[number] — [Short Name]`
- **CRITICAL: Paper ignores position values in create_artboard.** Every `create_artboard` MUST be immediately followed by `update_styles` to set the correct `top` and `left`. This is non-negotiable.
- **CRITICAL: Position drift worsens after ~8-10 artboards.** After every 5 artboards, run `get_basic_info` and verify ALL positions before creating the next one. Fix any drift immediately.
- All artboards in a deck MUST be in a single horizontal row, left to right, in presentation order. No exceptions. This has been violated in 3 separate sessions.

#### Content Architecture
Every slide: content frame (flex-grow: 1, pushes footer to bottom) + footer (per design system).

#### Building Order
1. Create artboard → **immediately** `update_styles` to fix position (SAME message, not next)
2. Verify: after every 5th artboard, run `get_basic_info` and check ALL positions
3. Add background elements FIRST (textures, glows, gradients — Paper renders first child at the back)
4. Add content frame + footer AFTER backgrounds
5. Add text elements one group at a time
6. Screenshot to verify every 2-3 slides

#### Efficiency
After building 2-3 unique slides, clone similar layouts with `duplicate_nodes` and modify with `update_styles` / `set_text_content`.

### Figma Path

#### Frame Setup
- Default: 1456 x 816px (16:9, Figma presentation standard)
- Position slides horizontally: `slide.x = slideIndex * (1456 + 80)`
- Name: `[number] — [Short Name]`
- Create a dedicated page for the deck: `figma.createPage()` → `figma.setCurrentPageAsync(page)`

#### Building with `use_figma`
Each slide is one `use_figma` call containing Plugin API JavaScript. The tool takes a `fileKey`, `code`, and `description`.

**CRITICAL rules for every `use_figma` call:**
1. After setting `layoutMode` on any frame, IMMEDIATELY set `primaryAxisSizingMode = "FIXED"` and `counterAxisSizingMode = "FIXED"` on slide-level frames. Without this, slides collapse to content height.
2. After creating any HORIZONTAL auto-layout frame, set `layoutSizingVertical = "HUG"` to prevent 100px default height.
3. Use `await figma.loadFontAsync({ family, style })` before setting text content.
4. Use `await figma.getNodeByIdAsync()` (not `figma.getNodeById()`) for dynamic page access.

**Search for existing components first.** Before building from scratch, call `mcp__claude_ai_Figma__search_design_system` to find reusable components in the user's design system. Import matches via `importComponentByKeyAsync` instead of recreating them.

#### Building Order
1. Create page → load fonts
2. Build slide frame with auto-layout (VERTICAL, fixed size)
3. Add content frame (layoutGrow: 1) + footer
4. Add text and visual elements
5. Screenshot via `mcp__claude_ai_Figma__get_screenshot` every 2-3 slides
6. Self-healing: compare screenshot against intent, fix mismatches

#### CSS → Figma Property Reference
See [references/figma-export.md](references/figma-export.md) for the complete CSS-to-Figma-Plugin-API mapping, helper functions, font weight map, and known pitfalls.

### Both Paths

#### Re-read the Content File
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

**Screenshots by canvas:**
- Paper: `get_screenshot` from Paper MCP
- Figma: `mcp__claude_ai_Figma__get_screenshot` with the file key and node ID

Full scoring rubrics, agent prompt templates, and the complete stop-slop checklist are in [references/quality-system.md](references/quality-system.md).

---

## Phase 6: Export

Export depends on which canvas you built on.

### Built in Paper

**PDF Export:** See [references/pdf-export.md](references/pdf-export.md). Screenshots each artboard via MCP, assembles with Pillow. Pixel-perfect, not editable. Fast (~2 min for 20 slides).

**Paper → Figma Export:** Translates the Paper deck into editable Figma frames. See [references/figma-export.md](references/figma-export.md) for the full pipeline.

**Requires:** Figma MCP server connected + a target Figma file URL/key.

**Process:**
1. Get target Figma file key from user
2. Test `use_figma` access with a probe call
3. Create a dedicated page, load fonts
4. Extract JSX from each Paper artboard (`get_jsx`, inline-styles format)
5. Translate to Figma Plugin API calls, one `use_figma` call per slide
6. CRITICAL: set `primaryAxisSizingMode = "FIXED"` on every slide frame after setting `layoutMode`
7. Fidelity check: screenshot every Figma slide, compare against Paper originals, fix clipping/spacing
8. Clean up orphan frames

### Built in Figma

Your deck is already in Figma. No export step needed. The user can:
- Share the Figma file directly with their team
- Export frames as PNG/PDF from Figma's native export
- Use Figma's presentation mode to present

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
2. **Determine canvas** — Paper (default) or Figma (if user specifies or provides Figma URL)
3. **Create content markdown file** — distill, structure, save
4. **Identify design system** — user-provided, or confirm default. For Figma: search for existing design system components first.
5. **Layout planning** — assign layouts to all slides, present full plan
6. User approves or adjusts plan
7. Verify font availability (Paper: `get_font_family_info` / Figma: `loadFontAsync` in probe call)
8. Build title slide → screenshot → **wait for user reaction**
9. Build remaining slides (2-3 at a time, screenshot between batches)
10. Re-read content file every 5-6 slides to prevent drift
11. Run four-pass quality system (including layout intelligence)
12. Apply fixes, verify with screenshots
13. User requests adjustments → apply to ALL affected slides, re-run quality
14. Export when ready (Paper: PDF or Figma export / Figma: already done)

Paper: always call `finish_working_on_nodes` when done editing.

---

## Growing the Layout Library

The layout patterns in [references/layouts.md](references/layouts.md) are not fixed. When the user provides a new reference deck (PPTX, PDF, Figma), analyze it for layout patterns not already in the library. If new patterns are found, add them to `layouts.md` with the same structure: name, when to use, structure spec. The library gets smarter with every deck the user feeds in.
