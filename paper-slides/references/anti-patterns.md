# Anti-Patterns

Common mistakes that make decks look amateur. Each one includes why it fails and what to do instead.

## CRITICAL: Trusting create_artboard positioning
**Why it fails:** Paper's auto-placement algorithm IGNORES the top/left values passed in create_artboard styles. Every single time. Artboards land on random rows and columns regardless of what you specify. This was violated 4+ times in a single session (2026-03-20) despite being logged after each violation.
**Instead:** After EVERY create_artboard call, IMMEDIATELY call update_styles in the SAME response to force the correct top and left. Never batch multiple create_artboard calls. The pattern is always: create_artboard → update_styles → add content. The position formula is: `left = slide_index * 1536`, `top` = consistent for the deck row. This is non-negotiable.

## CRITICAL: Batching create_artboard calls
**Why it fails:** When you batch 3-5 create_artboard calls in parallel, Paper scatters them across the canvas. You can't fix positions until all calls return, and by then the user has seen the mess.
**Instead:** Create ONE artboard at a time. Immediately fix its position. Then create the next. Sequential, never parallel.

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
**Why it fails:** False agency ("the decision emerges"), passive voice, throat-clearing openers, and dramatic fragmentation are tells.
**Instead:** Run the Copy Quality (Stop Slop) pass on every line. See `references/quality-system.md`.

## Cramming content
**Why it fails:** Dense slides overwhelm. The audience reads ahead instead of listening.
**Instead:** If it doesn't fit, split into two slides. White space is a feature.

## Mixing design systems in one deck
**Why it fails:** A serif headline on one slide and a grotesque-only system on the next creates visual whiplash. The audience loses trust.
**Instead:** Pick one system (C&T Strategy or TMS Core) and commit. Both live in `references/design-system-*.md`.

## Rounded corners on images in a TMS Core deck
**Why it fails:** TMS Core uses sharp rectangles exclusively. Rounded corners break the mosaic grid and look like a different template.
**Instead:** All images: sharp corners, object-fit cover, no borders, no shadows.

## Using bold weight in a monofont system
**Why it fails:** TMS Core achieves hierarchy through size contrast, not weight. Adding bold creates a different visual language.
**Instead:** Keep everything at regular weight (400). Scale up headlines instead of bolding them.

## Inconsistent image grid gaps
**Why it fails:** TMS Core grids use 4-6px gaps. Mixing 4px and 20px gaps within the same slide breaks the mosaic feel.
**Instead:** Set one gap value per deck and stick with it.

## Putting two image-grid slides back-to-back
**Why it fails:** The eye needs a text-only rest between image-dense slides. Two mosaics in a row feel like a photo dump.
**Instead:** Insert a text slide, quote, or section divider between image-heavy slides.
