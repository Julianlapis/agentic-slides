# Anti-Patterns

Common mistakes that make decks look amateur. Each one includes why it fails and what to do instead.

## CRITICAL: Trusting create_artboard positioning
**Why it fails:** Paper's auto-placement algorithm IGNORES the top/left values passed in create_artboard styles. Every single time. Artboards land on random rows and columns regardless of what you specify. This was violated 4+ times in a single session (2026-03-20) despite being logged after each violation.
**Instead:** After EVERY create_artboard call, IMMEDIATELY call update_styles in the SAME response to force the correct top and left. Never batch multiple create_artboard calls. The pattern is always: create_artboard → update_styles → add content. The position formula is: `left = slide_index * 1536`, `top` = consistent for the deck row. This is non-negotiable.

## CRITICAL: Batching create_artboard calls
**Why it fails:** When you batch 3-5 create_artboard calls in parallel, Paper scatters them across the canvas. You can't fix positions until all calls return, and by then the user has seen the mess.
**Instead:** Create ONE artboard at a time. Immediately fix its position. Then create the next. Sequential, never parallel.

## CRITICAL: Not verifying artboard positions after creation
**Why it fails:** `update_styles` can silently fail, especially after 8-10 artboards when the canvas gets crowded. Paper's auto-placement fights harder as more artboards exist. Slides appear in wrong positions without any error.
**Instead:** After EVERY 5 artboards, run `get_basic_info` and verify ALL positions. Fix any drift BEFORE creating the next artboard. After ALL artboards exist, run a final `get_basic_info` position audit. Don't trust that `update_styles` worked — verify.

## CRITICAL: Paper MCP targets whichever file is focused
**Why it fails:** If the user clicks another tab, all subsequent MCP calls silently target the wrong canvas. Content vanishes. Positions appear to "drift" because they're set on a different artboard in a different project.
**Instead:** Before every batch of writes, verify `fileName` in `get_basic_info` matches the target project. If it doesn't, STOP and tell the user to switch back.

## Building all slides before screenshotting
**Why it fails:** Errors compound. A wrong font size on slide 1 gets duplicated to slides 2-10.
**Instead:** Screenshot every 2-3 slides. Catch issues early.

## Using system fonts
**Why it fails:** After duplicating nodes, Paper sometimes reverts to `system-ui, sans-serif`. The result looks broken.
**Instead:** Always set `fontFamily` explicitly. Verify after every duplication with `get_computed_styles`.

## Same layout back-to-back
**Why it fails:** Five identical layouts in a row puts the audience to sleep regardless of content.
**Instead:** Alternate between light/dark, text-only/cards, statement/2-column. See `references/layouts.md` for the 7 layout types.

## Tiny body text
**Why it fails:** What looks fine on a monitor is unreadable on a projector.
**Instead:** 18-20px minimum for body text. 16px absolute floor.

## Ignoring line breaks
**Why it fails:** Orphaned words and lopsided wraps look amateur.
**Instead:** Adjust `maxWidth` per element to force balanced reflow. Screenshot and verify.

## Recreating similar slides from scratch
**Why it fails:** Wastes tokens, introduces inconsistencies.
**Instead:** Duplicate and modify. Faster, more consistent.

## Forgetting `finish_working_on_nodes`
**Why it fails:** Leaves the working indicator on the canvas.
**Instead:** Always call when done editing.

## Not pausing after the title slide
**Why it fails:** The user's reaction determines the direction. Building 10 slides before they've seen slide 1 risks redoing everything.
**Instead:** Build title slide, screenshot, wait for feedback. Then build the rest.

## Using the same font for every deck
**Why it fails:** Each deck loses its identity.
**Instead:** Each deck gets its own typographic personality. Verify with `get_font_family_info`.

## Using update_styles for artboard height
**Why it fails:** Paper ignores `update_styles` for height on artboards. The value is stored but has no visual effect. Content overflows or the artboard stays at default height.
**Instead:** Use `write_html` with explicit height values. Always verify with `get_computed_styles` and screenshot after setting dimensions.

## Using overlay divs to darken backgrounds
**Why it fails:** Paper renders children in order. Overlays added after content cover the content. z-index is unreliable.
**Instead:** Use background gradients on the artboard itself, or add bg elements FIRST before content.

## Adding background images AFTER content nodes
**Why it fails:** Later children render on top in Paper.
**Instead:** Always add bg images/textures/glows as the FIRST children of the artboard.

## Leaving emphasis text unstyled
**Why it fails:** Punchlines that share the same weight as surrounding text get lost.
**Instead:** Bold closing lines (fontWeight: 700) or use accent color.

## Repeating content across slides
**Why it fails:** The audience gets bored hearing the same idea three ways. It signals the writer doesn't trust their own material.
**Instead:** Each slide introduces one new idea. Run the Narrative Flow scoring pass to catch redundancy.

## Writing slide copy that sounds like AI
**Why it fails:** False agency, passive voice, throat-clearing openers, and dramatic fragmentation are tells.
**Instead:** Copy quality is enforced by `/write:voice` (the canonical voice review agent), which references `~/.claude/voice-dna.md` and `~/.claude/copy-polish.md`. See those files for anti-slop rules.

## Cramming content
**Why it fails:** Dense slides overwhelm. The audience reads ahead instead of listening.
**Instead:** If it doesn't fit, split into two slides. White space is a feature.

## Mixing design systems in one deck
**Why it fails:** A serif headline on one slide and a grotesque-only system on the next creates visual whiplash. The audience loses trust.
**Instead:** Pick one system and commit. Your design system file is the single source of truth.

## Rounded corners on images in a sharp-rectangle system
**Why it fails:** If the design system uses sharp rectangles exclusively, rounded corners break the grid and look like a different template.
**Instead:** All images: sharp corners, object-fit cover, no borders, no shadows.

## Using bold weight in a monofont system
**Why it fails:** Size-contrast systems achieve hierarchy through size, not weight. Adding bold creates a different visual language.
**Instead:** Keep everything at regular weight (400). Scale up headlines instead of bolding them.

## Using paddingBlock/paddingInline on artboards
**Why it fails:** Paper's `create_artboard` and `update_styles` ignore `paddingBlock` and `paddingInline` longhand logical properties. The values are stored but have no visual effect. Content renders edge-to-edge.
**Instead:** Use the shorthand `padding: "60px"`. Always verify with `get_computed_styles` after setting padding, and screenshot to confirm visually.

## Using frame opacity instead of fill opacity for backgrounds
**Why it fails:** `node.opacity = 0.08` makes ALL children transparent, including text. A card with frame-level opacity renders as a dark gray box with invisible text.
**Instead:** Use fill-level opacity: `node.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 }, opacity: 0.08 }]`. This makes the background transparent while keeping text and other children at full opacity.

## Inconsistent image grid gaps
**Why it fails:** Mosaic-grid systems use tight (4-6px) gaps. Mixing 4px and 20px gaps within the same slide breaks the mosaic feel.
**Instead:** Set one gap value per deck and stick with it.

## Putting two image-grid slides back-to-back
**Why it fails:** The eye needs a text-only rest between image-dense slides. Two mosaics in a row feel like a photo dump.
**Instead:** Insert a text slide, quote, or section divider between image-heavy slides.

## Side-stripe borders on cards (CRITICAL — inherits /design:impeccable absolute ban)
**Why it fails:** A thick (3–8px) colored vertical bar hugging the left edge of a card/list-item/callout is the single most recognizable "AI slop" tell. It's an **absolute ban**, and a grid/alignment eval is blind to it (the stripe is on-palette, on-grid, not a collision). It shipped on two real slides while a deterministic eval reported "0 violations" because the eval only measured geometry.
**Instead:** Re-treat the block — subtle surface fill (e.g. a near-white card tint) or a clean full outline, and express any brand color in the **name text**, never a stripe. Deck design evals must inherit the full `/design:impeccable` ban list (side-stripes, gradient text, underline/strike on slide copy), not rely on perceptual agents to catch them. Mechanical check: a 3–8px vertical rect with content immediately to its right and none to its left = a side-stripe → flag.

## Headline size inconsistent across same-type slides
**Why it fails:** A headline that's "fine on its own slide" (e.g. 30px) reads as broken next to twelve 60px siblings. Per-slide review can't see it; only a cross-frame comparison can. Compounded when the outlier is also a non-headline color (royal) or underlined — it reads as a broken hyperlink.
**Instead:** All same-type slide headlines share one size tier. Run a deck-level check: flag any headline under ~70% of the median headline size. Headlines are black ink by default; reserve accent color for semantic emphasis, never a full headline by accident. No `textDecoration` on slide copy.
