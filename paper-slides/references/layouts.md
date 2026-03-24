# Layout Pattern Library

A growing repository of slide layout patterns. Each pattern describes a content shape and how to arrange it. The skill selects from this library based on content structure and narrative position.

These patterns are deck-type-agnostic. A Cards layout works for strategy pillars, product features, team values, or research findings. The design system controls the visual treatment. The layout controls the spatial arrangement.

---

## How to Use This Library

1. **Read the full content first.** Understand the narrative arc before assigning layouts.
2. **Match content shape to layout shape.** Each slide's content has a natural form: one big idea, parallel items, image + text, pure visual, etc.
3. **Sequence for rhythm.** No same layout back-to-back. Alternate density. Place breathing moments (Statement, Quote) between dense slides.
4. **The library grows.** When a new reference deck introduces a pattern not listed here, add it.

---

## A. Statement

One bold idea, massive type, nothing else. The whitespace IS the design.

**Content shape:** A single sentence or phrase strong enough to stand alone. No supporting text needed.

**When to use:** Section openers, provocative claims, key takeaways, moments of emphasis. Works as a palate cleanser between dense slides.

**Structure:**
- Content centered vertically and horizontally
- Headline: display size (68-72px), max-width ~1000px
- Optional smaller kicker or subtitle below (24px, secondary color)
- Optional eyebrow label (top-left, 14px)
- Everything else is empty

---

## B. Section Divider

Number + section name, top-left. The rest is empty. Marks a structural transition in the deck.

**Content shape:** A section number and name. Nothing else.

**When to use:** Between major deck sections. After an agenda slide, each section starts with its divider.

**Structure:**
- Number ("01") + section name, same line, top-left
- Display size (68-72px)
- Number in secondary text color, name in primary
- Footer at bottom
- Everything else is intentionally empty

---

## C. Agenda / Table of Contents

Numbered section list providing deck navigation.

**Content shape:** 3-6 section names that define the deck structure.

**When to use:** After the title slide. Establishes what's coming.

**Variant 1 — Simple Stack:**
- Items stacked vertically, each row: "01" + "Section name"
- Display size, number in secondary color
- Content pinned top-left

**Variant 2 — Index Panel:**
- Left panel: subtitle + heading + body text at bottom
- Right panel (contrasting bg fill): content header + item list with right-aligned page numbers
- Consistent row height across all items

**Variant 3 — Multi-Section Grid:**
- 2×3 or 3×2 grid of section groups
- Each group: number + heading + 3-5 bullet items
- Left panel has the TOC heading

---

## D. Left-Heavy

Headline and body pinned to the left 50-60% of the slide. Right half intentionally empty.

**Content shape:** One idea with optional supporting text. The emptiness signals authority.

**When to use:** Single-idea slides that need gravity. Claims, declarations, brand statements.

**Structure:**
- Content constrained to max-width ~700px
- Headline: section title size (40-44px)
- Body: caption size (16-18px) below headline
- Right half empty (no filler elements)
- Eyebrow label top-left

---

## E. Eyebrow + 2-Column

The workhorse. Eyebrow label, headline in the left column, body/detail in the right column.

**Content shape:** A headline + supporting detail that benefits from spatial separation.

**When to use:** The default when no other layout fits. Limit to max 3 appearances per deck.

**Structure:**
- Eyebrow (14px, top-left)
- Headline left column (40-44px), ~55% width
- Body/detail right column (16-18px), ~45% width
- 48-60px gap between columns
- Content vertically centered or top-aligned

---

## F. Cards

3-5 equal columns, each with its own title + body. For parallel items that deserve equal visual weight.

**Content shape:** 3-5 items that are conceptually parallel: phases, features, values, categories, capabilities.

**When to use:** Whenever content breaks into distinct parallel blocks. GTM phases. Competitive landscape. Value propositions. Research themes.

**Structure:**
- Optional section header above (eyebrow + headline)
- 3-5 cards: equal width, 20-24px gap
- Card internals: optional number (body size) + title (24-26px) + body (16-18px, secondary color)
- Separated by whitespace only (no card backgrounds or borders in the default system)
- Design system may add card backgrounds, dividers, or accent elements

---

## G. Split Comparison

Full-width split into two halves showing contrasting or complementary content.

**Content shape:** Two things that need to be seen side by side: before/after, problem/solution, old/new.

**When to use:** Any natural tension or comparison between two ideas.

**Structure:**
- Vertical split at ~50/50 or 48/52
- Each half has its own content: eyebrow + headline + body or bullets
- Halves may have different background colors for contrast (per design system)
- Content vertically centered within each half

---

## H. Image Gallery

Left text panel + right image grid. The primary layout for content that pairs explanation with visual evidence.

**Content shape:** A headline + body text, with 1-6 images as supporting evidence.

**When to use:** Case studies, project showcases, product features, any slide where visual evidence supports a text claim. The most versatile image layout.

**Structure:**
- Left panel (~33% width): eyebrow (14px) + section title (40-44px) + subtitle (secondary color) + body text (16-18px, bottom of panel)
- Right panel (~67% width): contrasting background fill, tight image grid
- Images: object-fit cover, sharp corners, 5px gaps
- Grid adapts to image count:

| Count | Grid |
|-------|------|
| 1 | Full panel |
| 2 | Side by side |
| 3 | 1 large left + 2 stacked right, OR 3 equal columns |
| 4 | 2×2 |
| 5 | 2 top + 3 bottom |
| 6 | 2×3 |

---

## I. Image Mosaic

Pure image grid, no text (or minimal text overlay). Dense visual impact.

**Content shape:** Multiple images that speak for themselves. No explanation needed.

**When to use:** Portfolio overviews, visual evidence, mood slides. Use 1-2 per deck max.

**Structure:**
- Images fill the full artboard or content area
- Tight gaps (5px)
- Object-fit cover, sharp corners

| Count | Grid |
|-------|------|
| 4 | 2×2 |
| 6 | 2×3 |
| 8 | 2×4 |
| 12 | 3×4 |
| 18 | 3×6 |

- Optional variant: one cell replaced with a text overlay (title + body on contrasting background)

---

## J. People / Bio Grid

Equal columns of portraits with name + subtitle beneath each.

**Content shape:** 3-5 people who need equal visual weight.

**When to use:** Team slides, leadership pages, contributor credits, panel introductions.

**Structure:**
- 3-5 equal columns
- Each: image (square or 4:3, top) + name (24-26px, below) + subtitle (secondary color, below name)
- All images: same aspect ratio, same size, aligned on same horizontal baseline
- Names and subtitles aligned on same baseline across columns
- No bios, no body paragraphs. Just name + title.

---

## K. Full-Page Quote

Large quote text with optional photo and attribution.

**Content shape:** A quote, testimonial, or pull-quote that deserves its own slide.

**When to use:** Client testimonials, stakeholder endorsements, provocative pull-quotes. Works as a transition between sections.

**Variant 1 — Quote Only:**
- Quote text: 40-44px, regular weight, left-aligned, ~60% width
- Inline quotation marks (not decorative oversized marks)

**Variant 2 — Quote + Photo + Attribution:**
- Small photo (left side) + quote text (right)
- Attribution below: Name / Title / Company (3 lines, 14px)

**Variant 3 — Centered Quote:**
- Quote text centered, display size
- Attribution centered below
- Name / Title / Company

---

## L. Multi-Column Text

3, 4, or 5 parallel columns of title + body text. No images.

**Content shape:** 3-5 parallel items that don't need visual treatment. Lighter-weight than Cards.

**When to use:** When content breaks into parallel text blocks but doesn't warrant the visual weight of Cards. Features, principles, capabilities, definitions.

**Structure:**
- Section header area: eyebrow + section title + subtitle (full width)
- 3-5 equal columns below
- Each column: title (24-26px) + body (16-18px)
- Columns separated by whitespace only
- Body text in narrow columns uses smaller size (16px) to avoid excessive wrapping

---

## M. Case Study Detail

Deep dive into a single project or feature with hero image + supporting visuals.

**Content shape:** A project or feature that needs explanation + multiple images at different scales.

**When to use:** Detailed project pages, feature walkthroughs, portfolio deep dives. Come in clusters of 2-4.

**Structure:**
- Left third: subtitle + title + body paragraph (supports 2-3 paragraphs of longer copy)
- Right two-thirds: hero image (large) + 1-3 supporting thumbnails below
- Text panel width stays fixed regardless of image count
- Supporting thumbnails always smaller than hero

**Variants:**
- 1 hero + 0 supporting: simple text-left, image-right
- 1 hero + 2 thumbnails: hero top, thumbnails bottom row
- 2 equal images: stacked vertically
- 3 images with titles: 3 columns, each image + title + body

---

## N. 2-Up Tension

Two equal columns, each with its own eyebrow + headline. Creates a dialectic.

**Content shape:** Two ideas that gain meaning from juxtaposition.

**When to use:** Problem/solution, before/after, challenge/ambition. Any natural tension between two ideas.

**Structure:**
- Two columns, equal width, 48-60px gap
- Each column: eyebrow label (14px) + headline (40-44px) + optional body
- Content vertically centered

---

## O. Sequential Stack

Multiple statements stacked vertically. Each line is its own beat. Rhythmic, building cadence.

**Content shape:** 4-6 short statements that build on each other in sequence.

**When to use:** Linear storytelling, process descriptions, closing sequences. When the rhythm IS the argument.

**Structure:**
- Eyebrow top-left
- 4-6 lines, centered or left-aligned, vertically distributed with 40-48px gaps
- Optional progressive contrast (text fades from dim to bright)
- Final line in accent color or bold weight
- Each line: 28-32px

---

## P. Category Matrix

Content organized by multiple categories in a grid. For comparative or taxonomic content.

**Content shape:** 4-6 categories, each with a label, description, and optional image.

**When to use:** Competitive analysis, feature comparison, capability mapping, research taxonomy.

**Structure:**
- Section header: eyebrow + title + subtitle (spanning full width or left portion)
- 2×3 or 3×2 grid of category blocks
- Each block: category name (24-26px) + description (16-18px) + optional image
- Images in select cells, not all (mix text-only and image cells for variety)

---

## Q. Full-Bleed Image

Single image covers the entire artboard. Pure visual moment.

**Content shape:** One image that speaks for itself.

**When to use:** Major transitions, mood setting, visual punctuation. 1-2 per deck maximum.

**Structure:**
- Image fills the entire artboard
- No text overlay in the basic variant
- Optional variant: dark gradient overlay from bottom + text in the bottom third

---

## R. Full Image + Text Overlay

Background image with text panel overlaid.

**Content shape:** An image that needs context or narration.

**When to use:** Feature showcase with visual context, location-based content, atmospheric slides.

**Structure:**
- Background image fills artboard
- Semi-transparent dark overlay or gradient for text legibility
- Text panel: subtitle + title + body, bottom-left or left-third
- Text always on the overlay, never directly on the unprocessed image

---

## S. Thank You / Contact

Closing slide. Bookends the deck with the title slide.

**Content shape:** A closing message + contact information.

**When to use:** Final slide. Every deck ends with this.

**Structure:**
- "Thank you!" or closing message in display size
- Contact label below
- Email and website in body text
- Same footer as all other slides
- No logos, no social icons, no decorative elements

---

## Layout Sequencing Rules

1. **Never use the same layout back-to-back.** Even if content shapes are similar, vary the arrangement.
2. **Image-heavy slides need text-only buffers.** Don't put Image Gallery (H) next to Image Mosaic (I) without a text slide between them.
3. **Statement/Quote slides are breathing moments.** Place them at section transitions, not mid-section.
4. **People slides belong in the second half.** Team intros come after the work speaks.
5. **Case Study slides come in clusters of 2-4.** A single case study slide feels orphaned.
6. **Every deck starts with a title slide.** Either Statement (A) or a custom title layout.
7. **Every deck ends with Thank You (S).**
8. **An Agenda (C) slide follows the title for structured decks.**
9. **Density should vary deliberately.** Dense → breathing → dense → breathing. Not all dense, not all sparse.
10. **A 10-slide deck should use at least 4 different layout types.** A 20-slide deck, at least 7.
11. **Quote slides (K) work as transitions.** Between sections, not within them.

---

## Strategy Framework Layouts (from TMS Strategy)

These patterns come from the TMS Strategy template system. They're built for strategy decks: roadmaps, frameworks, journeys, projections. Each one encodes a specific strategic argument in its spatial structure.

---

### T. Growth Stairs

Ascending blocks that visualize crawl-walk-run progression. The growth is the argument.

**Content shape:** 3-4 sequential phases that represent increasing scale, maturity, or investment.

**When to use:** Crawl-walk-run progressions, roadmaps, capability maturity models, phased investment plans. Any content showing sequential growth or expansion over time.

**Structure:**
- Eyebrow + headline + body text in the top-left quadrant
- Bottom section: 3-4 blocks ascending left to right, each progressively taller and wider
- Smallest block anchored bottom-left, largest anchored bottom-right
- Each block contains a phase label (centered)
- Blocks use a darker fill (accent color or dark gray) against the slide background
- Optional: body text in the top-right providing context

**Key design rule:** The ascending scale creates the argument visually. The growth is the point. Don't undermine it with equal-sized containers.

---

### U. Phase Cards

Discrete containers for time-bound workstreams. Each card is a self-contained unit.

**Content shape:** 2-4 parallel time-bound chunks that each contain a list of deliverables or actions.

**When to use:** Multi-phase plans, year-over-year objectives, workstream breakdowns. Content with 2-4 parallel time-bound chunks that each contain a list of deliverables or actions.

**Structure:**
- Top half: eyebrow + headline (left) + body paragraph (right), split layout
- Bottom half: 2-4 equal-width cards with rounded corners and subtle fill (light gray or tinted)
- Each card has: bold phase label top-left, bullet list of items below
- Cards sit in a horizontal row with small gaps (8-12px)
- Cards take up roughly 50-60% of slide height

**Key design rule:** Cards should feel like discrete containers, not just columns. The rounded corners and fill differentiate this from a flat multi-column layout.

---

### V. Journey Matrix

Stages as columns, dimensions as rows. A framework for mapping customer movement.

**Content shape:** Stages as columns and dimensions as rows. Content that maps behavior, channels, or touchpoints across a journey.

**When to use:** Customer journeys, funnel mapping, channel strategy across stages. Content with stages as columns and dimensions as rows.

**Structure:**
- Eyebrow + headline top-left
- Column headers in bold across the top (e.g., Awareness, Consideration, Purchase, Loyalty)
- Horizontal timeline/arrow connecting the stages
- Rows below for different dimensions (labeled on the left edge)
- Each cell contains brief text
- Subtle horizontal dividers between rows

**Key design rule:** This is a matrix, not a table. Keep cell content to 1-2 lines max. The structure communicates the framework; the content fills in the specifics.

---

### W. 2x2 Strategy Map

Four quadrants with a synthesis point at the center. The classic strategic positioning tool.

**Content shape:** Four related concepts that can be arranged in quadrants, with a central proposition tying them together.

**When to use:** Strategic positioning, tension mapping, four-forces frameworks. Any content with four related concepts that can be arranged in quadrants.

**Structure:**
- Large rounded-corner container filling most of the slide
- Divided into four quadrants by thin vertical and horizontal lines
- Each quadrant: bold label centered, descriptive text below in muted color
- Central element: pill/badge at the intersection point with the core proposition
- Eyebrow + headline above the container (or subtitle below headline)

**Key design rule:** The center element is the synthesis of the four quadrants. It should visually dominate the intersection.

---

### X. Cycle Diagram

A circular process with labeled nodes. For content where the loop is the argument.

**Content shape:** 3-5 steps in a continuous process that feeds back into itself.

**When to use:** Iterative processes, reinforcement loops, research cycles. Any content showing a continuous process with 3-5 steps that feed back into each other.

**Structure:**
- Split layout: text left (eyebrow + headline + body), diagram right
- Right panel: large rounded-corner container with a dashed circular path
- 3-5 labeled nodes (circles with gradient fills) positioned along the path
- Nodes labeled with step names
- Dashed connectors between nodes suggesting flow direction

**Key design rule:** The circle communicates "this never stops." Use it when the loop is the argument, not just the structure.

---

### Y. Projection Timeline

An ascending curve with milestones below. Forward momentum on a time axis.

**Content shape:** A growth trajectory with specific milestones along a time axis.

**When to use:** Growth trajectories, launch timelines, milestone planning. Content showing forward momentum along a time axis.

**Structure:**
- Eyebrow + headline top-left
- Ascending curve from bottom-left to top-right (can be a simple SVG path)
- Legend or bullet list in top-right corner showing what the endpoint represents
- Horizontal timeline axis at bottom with milestone markers (circles on a line)
- Below each marker: bold month/date label + brief description
- Optional: small accent block at the start showing "current state"

**Key design rule:** The curve does the emotional work. The milestones below do the informational work. Don't clutter the curve area with text.

---

### Z. Staircase Gantt

Staggered workstream blocks that build on each other over time.

**Content shape:** Multiple workstreams that start at different times and layer onto each other.

**When to use:** Multi-workstream timelines, capability buildout over time. Content showing parallel tracks that start at different times and grow.

**Structure:**
- Eyebrow + headline top-left
- Ascending staircase of blocks from bottom-left to top-right
- Each "step" is a labeled block (workstream name) with additional unlabeled blocks extending right (representing deliverables or milestones)
- Horizontal timeline axis at the bottom with date labels
- Blocks use gradient fills, darker for the named workstream, lighter for extensions

**Key design rule:** This communicates "building on each other." Each new workstream starts where the previous one has established a foundation.

---

## Adding New Patterns

When analyzing a new reference deck, look for layout patterns not already in this library. A new pattern qualifies if:
- It arranges content in a spatially distinct way from existing patterns
- It serves a content shape not already covered
- It appears in at least 2-3 slides in the reference (not a one-off)

Add new patterns with: letter code, name, content shape description, when to use, and structure spec.
