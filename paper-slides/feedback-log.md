---
name: feedback-log
description: Paper Slides Feedback Log - read at the start of every /paper-slides invocation to avoid repeating mistakes
---

# /paper-slides Feedback Log

**CANONICAL LOCATION: `~/.claude/feedback/paper-slides/general.md`**

Read the canonical file above. It contains all corrections from Julian, migrated from this file.
Also read: `~/.claude/feedback/global.md` (cross-cutting rules for all skills).

These are binding. Don't repeat corrected mistakes.

---

## 2026-03-19: Artboard layout order not set

**What happened:** Built/edited 28 slides across multiple rows on the canvas instead of laying them out in a single horizontal row, left to right, in slide order. Julian had to ask for this explicitly.

**The rule:** Always position artboards in a single horizontal row, left to right, in presentation order. Formula: `left = (slide_index - 1) * (artboard_width + 80)`, `top = 0`. Do this from the start when creating new decks, and verify/fix it when editing existing decks. This is how Paper presents slides for PDF export and how the user navigates the canvas.

---

## 2026-03-19: Body copy too small for presentation

**What happened:** Body text was set at 14-18px across content slides. Julian flagged it as unreadable at presentation scale. Had to bump twice before landing on the right sizes.

**The rule:** Body copy minimum is 20px/30px line height. Secondary labels (column headers, week labels, status indicators) minimum is 25px/34px. Secondary text must always be visually larger than body text to create hierarchy. Run `get_computed_styles` on representative body text nodes BEFORE declaring text is readable. Never trust visual inspection at 1x scale for font size.

---

## 2026-03-19: Content crammed at top of slides with massive empty space below

**What happened:** On 11 white content slides, all text sat in the top 30-40% with the bottom 60% completely empty. Attempted multiple CSS approaches (justifyContent on Content frames) that didn't work because of fixed-height internal containers.

**What finally worked:**
1. Set the artboard to `display: flex`, `flexDirection: column`, `padding: 60px`, `justifyContent: center`
2. Set the Content frame to `height: fit-content`, `flexGrow: 0`
3. Pin the Footer frame to `position: absolute`, `bottom: 0`, `left: 0`, `right: 0`

This lets the artboard center the content block vertically while keeping the footer anchored at the bottom.

**The rule:** After building or editing any slide, screenshot it and check: is the content vertically centered between the eyebrow area and the footer? If content sits in the top third with vast empty space below, fix it before moving on. This is a mandatory review checkpoint.

---

## 2026-03-19: Source content not saved before editing

**What happened:** Started making design changes without first saving the slide copy to a reference file. Julian had to ask for this explicitly to prevent losing track of verbatim content.

**The rule:** Before making ANY design changes to an existing deck, extract all text content from every slide and save it as an MD file (e.g., `~/Desktop/[project]-content.md`). Reference this file throughout the editing session. Verify text content against it after making changes.

---

## 2026-03-19: Design system file not loaded proactively

**What happened:** Julian had to point out that a design system file existed and should be referenced. Should have checked for design system layers/files immediately upon opening the Paper file.

**The rule:** After `get_basic_info`, always check for design system files: search for `*design-system*` or `*design_system*` in the Paper file's artboards, and check the skill's references directory for matching design systems. Load the design system BEFORE making any visual changes.

---

## 2026-03-19: Quality system not run automatically

**What happened:** Made changes across multiple passes without running the three-pass quality system (Design Quality Agent, Narrative Flow Agent, Copy Quality Pass) until Julian asked for it.

**The rule:** The quality system is mandatory after every round of changes, not optional. Run it proactively after completing a batch of edits. Don't wait to be asked.

---

## 2026-03-19: Absolute-positioned footers clip at artboard edges

**What happened:** When footers are set to `position: absolute; bottom: 0; left: 0; right: 0`, they ignore the artboard's padding and render edge-to-edge. "CODE AND THEORY" was clipped at the left edge of slide 03.

**The rule:** Any absolute-positioned footer must have its own internal padding: `paddingLeft: 60px`, `paddingRight: 60px`, `paddingBottom: 40px`. Apply this to ALL footer frames when using absolute positioning. Check every slide's footer after making layout changes.

---

## 2026-03-19: Inconsistent font sizes across slides of the same type

**What happened:** Slide 03's headline was 48px while slides 02 and 04 (same red statement style) were 56px and 60px. Body copy on slide 03 was 20px while other slides had been bumped to 25px. This created visible inconsistency when flipping between slides.

**The rule:** Establish a global type scale at the start of any build or enhancement pass, then enforce it across every slide. Run `get_computed_styles` on headlines and body text from 3-4 representative slides to verify consistency BEFORE declaring work complete. Same slide type = same font sizes. The type scale should be:

| Element | Size | Line Height |
|---------|------|-------------|
| Statement headline (red/dark slides) | 56-60px | 62-66px |
| Content headline (white slides) | 40-52px | 48-58px |
| Body copy (everywhere) | 25px | 36px |
| Secondary labels | 25px bold | 34px |
| Column body text | 20px | 30px |
| Footer | 11-12px | 14px |
| Eyebrow | 12-14px | 16px |

If the design system specifies different sizes, follow the design system. But never let the same element type vary across slides without a deliberate reason.

---

## 2026-03-19: Overcomplicated PDF export instead of using established approach

**What happened:** Tried to build a JSX → HTML → Puppeteer pipeline from scratch, spawning a subagent that hit permission issues and took 25 minutes. Then had to extract the HTML from the agent's output log and reassemble manually. The pdf-export reference doc already describes a simpler screenshot-based approach.

**The rule:** Always use the direct MCP screenshot approach for PDF export. Never use JSX conversion.

**The working approach (default to this every time):**

```python
import json, urllib.request, base64, os, glob
from PIL import Image

SLIDE_DIR = "/tmp/paper-pdf/slides"
os.makedirs(SLIDE_DIR, exist_ok=True)

def call_paper_mcp(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    req = urllib.request.Request("http://localhost:29979/mcp", data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    resp = urllib.request.urlopen(req, timeout=60)
    data = resp.read().decode()
    for line in data.split("\n"):
        if line.startswith("data: "):
            return json.loads(line[6:])
    return json.loads(data)

# For each artboard:
result = call_paper_mcp("tools/call", {"name": "get_screenshot", "arguments": {"nodeId": node_id, "scale": 2}})
content = result.get("result", {}).get("content", [])
for item in content:
    if item.get("type") == "image":
        img_data = base64.b64decode(item["data"])
        with open(path, "wb") as f:
            f.write(img_data)

# Assemble PDF with Pillow (no reportlab needed):
slides = sorted(glob.glob(f"{SLIDE_DIR}/slide-*.jpg"))
images = [Image.open(s).convert("RGB") for s in slides]
images[0].save(output_path, save_all=True, append_images=images[1:], resolution=144.0)
```

**Why this works:** Paper's MCP server at localhost:29979 accepts JSON-RPC calls at the `/mcp` endpoint with `Accept: application/json, text/event-stream` header. The response contains base64-encoded screenshots rendered by Paper's own engine. These are pixel-perfect. Pillow can assemble JPEGs into a PDF without needing reportlab (which has install issues on managed Python).

**Why JSX doesn't work:** JSX-to-HTML conversion introduces CSS translation bugs (indentation, line-height rounding, color format mismatches). The export will never be visually identical to Paper. Screenshots are the only pixel-perfect path.

**The export must be visually identical to the Paper file. Zero differences, even tiny ones.**

---

## 2026-03-20: FATAL — Paper ignores position hints. Force position after EVERY create. FOUR VIOLATIONS IN ONE SESSION.

**What happened:** Set explicit `top` and `left` in `create_artboard` styles, but Paper's auto-placement algorithm OVERRIDES these values EVERY TIME. Slides landed on wrong rows (top=1996, top=38, left=-1640) despite correct coordinates being passed. Julian flagged this FOUR SEPARATE TIMES in the same session. This is the single most repeated, most frustrating mistake in paper-slides history.

**The rule (ABSOLUTE, ZERO TOLERANCE):**

1. `create_artboard` position values are LIES. Paper ALWAYS ignores them. Treat them as decoration.
2. The ONLY way to position an artboard is `update_styles` AFTER creation. Period.
3. Every single `create_artboard` call MUST be IMMEDIATELY followed by `update_styles` in the SAME message. Not the next message. Not after adding content. IMMEDIATELY.
4. The formula: `left = slide_index * 1536` (0-indexed), `top` = consistent for the row.
5. NEVER batch multiple `create_artboard` calls. Create ONE, fix position, then create the next.
6. After all artboards exist, run `get_basic_info` and verify every single position.

**The ONLY acceptable pattern:**
```
create_artboard → update_styles(top, left) → write content → next slide
```

**If you skip update_styles after create_artboard, you have failed. There are no exceptions. This rule was violated 4 times in one session after being logged. Do not violate it again.**

---

## 2026-03-20: update_styles position fix applied but Paper STILL misplaces artboards

**What happened:** During a 20-slide v3 build, every `create_artboard` was immediately followed by `update_styles` to fix position. This worked for slides 01-18. But slide 19's `update_styles` did not stick — it landed at top=3096, left=12288 instead of top=2200, left=27648. Paper's auto-placement fought the correction. Required a second `update_styles` call and `get_basic_info` verification to catch it.

**The rule:** After building ALL artboards in a deck, ALWAYS run `get_basic_info` as a final position audit. Check every single artboard's top and left. Fix any that drifted. Do not trust that `update_styles` worked — verify. This is especially true for artboards created later in a session when the canvas is crowded.

---

## 2026-03-20: THIRD SESSION with position drift. Pattern: drift worsens after ~8-10 artboards.

**What happened:** During v4 build (21 slides at top=3300), slides 01-09 landed correctly after `update_styles`. Slide 10 drifted to top=4196, left=4608 despite immediate `update_styles` with correct values (top=3300, left=13824). This is the THIRD session where positions drift, and it consistently happens after 8-10 artboards are created in one session. The canvas gets crowded and Paper's auto-placement algorithm fights harder.

**The rule (UPGRADED):**
1. Every `create_artboard` → immediate `update_styles` (existing rule, keep doing this)
2. After EVERY 5 artboards, run `get_basic_info` and verify ALL positions. Fix any drift BEFORE creating the next artboard. Don't wait until the end.
3. If ANY artboard drifts during a mid-build check, fix it AND re-verify the fix with another `get_basic_info` before continuing.
4. The drift pattern is predictable: it gets worse as more artboards exist on the canvas. Budget for more verification calls in the second half of any build.

---

## 2026-03-20: Statement slides had too much body copy

**What happened:** Red statement slides (slide 02) and white belief slides (slide 03) were built with 3+ sentences of body copy. Julian flagged them as too dense. The headline carries the argument on these slide types. Body copy should support with 1-2 sentences, not expand into paragraphs.

**The rule:** For statement slides (L1, L2) and belief/declaration slides: **max 2 sentences of body copy** beneath the headline. If you're writing a third sentence, the slide is overloaded. Move content to the next slide or cut it. The headline does the work.

---

## 2026-03-20: Edits to narrative MD file not pushed to Paper

**What happened:** Tightened copy in the markdown narrative file but didn't update the corresponding Paper nodes. Julian had to ask if edits were pushed. They weren't.

**The rule:** When editing copy in the narrative markdown file, ALWAYS push the same edits to the corresponding Paper nodes in the same pass. The markdown file and Paper must stay in sync. If you edit one, edit both. Never present copy changes as done until they're reflected in Paper.

---

## 2026-03-20: Footer too close to body copy on statement slides

**What happened:** On red statement slides and dividers, the body copy and italic closers were jammed against the "CODE AND THEORY" footer with almost no breathing room. Screenshot showed the italic closer touching the footer line.

**The rule:** Two fixes needed to prevent footer/content overlap:
1. All absolute-positioned footers: `paddingBottom: 60px` (not 40px).
2. All Content frames with `justifyContent: flex-end` (bottom-anchored slides like red statements, dividers): add `paddingBottom: 50px` to the Content frame itself. This creates clearance between the last content element and the footer zone. Without this, the content pushes all the way to the bottom and overlaps the absolute footer.

---

## 2026-03-20: Eyebrows too small at 12px

**What happened:** Julian asked to bump all eyebrows by 5px. At 12px they were too small relative to the slide content, especially on red backgrounds.

**The rule:** Eyebrows should be **17px**, not 12px. This applies to all slide types: red, white, dark. Update the type scale: eyebrows are Inter Bold, 17px, uppercase, letter-spacing 0.15em. This overrides the design system's 11-14px range for this engagement.

---

## 2026-03-20: create_artboard padding doesn't stick with paddingBlock/paddingInline

**What happened:** Created 11 artboards with `paddingBlock: "60px"` and `paddingInline: "60px"` in the `create_artboard` styles. Paper stored them but they had no visual effect. Content rendered edge-to-edge. `update_styles` with the same properties also failed. Only the shorthand `padding: "60px"` worked.

**The rule:** When setting padding on artboards via `update_styles`, use the shorthand `padding: "60px"` instead of `paddingBlock`/`paddingInline`. The longhand logical properties don't reliably apply through `update_styles`. Always verify with `get_computed_styles` after setting padding, and screenshot to confirm visually.

---

## 2026-03-20: No italic serif for emphasis callouts

**What happened:** Used Cormorant Garamond italic for emphasis/callout lines throughout the deck (closers like "Run them together. They cost less and work better." and "We're in the first column."). Julian flagged it as looking weird. Serif italic for small callout text reads as decorative rather than authoritative.

**The rule:** Never use italic serif (Cormorant Garamond italic) for emphasis or callout lines. Use **Inter semibold (600)** instead. Keep Cormorant Garamond for headlines only (regular weight, not italic). The only acceptable italic in the deck is for direct quotes in Cormorant (like "How do I use this in a conversation?"), and even then, prefer dropping the italic and using regular weight with quote marks.

---

## 2026-03-20: Belief/thesis slides deserve big visual treatment

**What happened:** Slide 03 (Our Belief) was a cream bg slide with a left-aligned headline and body paragraph. Julian called it boring. The deck's thesis statement was visually indistinguishable from a regular content slide.

**The rule:** Belief/thesis slides are the deck's thesis. They should get maximum visual weight: dark bg (#1A1A1A), centered layout, headline at 56px+, body text muted. These are statement moments. Treat them like the title slide's sibling, not like a content slide with different copy.

---

## 2026-03-20: Always invoke /paper-slides skill before building in Paper

**What happened:** Started building slides without loading the paper-slides skill or reading the feedback log. This caused padding issues, layout drift, and style inconsistencies that had already been solved in previous sessions.

**The rule:** Before ANY Paper slide work, invoke the `/paper-slides` skill and read this feedback log. Every rule here was learned from a real failure. Skipping the skill means re-learning them.

---

## 2026-03-20: Use narrative flow agent as iterative advisor, update source file first

**What happened:** Initially treated the narrative flow agent's score as a report card rather than an iterative improvement tool. Julian clarified: the v4 narrative file is the source of truth, the flow agent is an outside advisor, and recommended changes should be applied to the narrative file first, then pushed to Paper.

**The rule:** When the narrative flow agent flags issues (redundancy, earned payoff, etc.), apply the fixes to the narrative markdown file FIRST, then push to Paper. The narrative file is the source of truth. Paper reflects it. Never change Paper copy without updating the narrative file. Never treat quality agent recommendations as FYI-only.

---

## 2026-03-20: Three background colors, not two

**What happened:** The deck only used cream (#F5F5F0) and red (#CC0000) backgrounds. Seven consecutive white slides in the WS2 section created a visual plateau. Layout variety scored 6/10 repeatedly.

**The rule:** Use three background colors: cream (#F5F5F0) for content, red (#CC0000) for statements/closers, dark (#1A1A1A) for breakers/belief slides. Dark bg breaks the cream/red binary and gives the deck visual punctuation at section transitions. Apply dark bg to: belief/thesis slides, workstream dividers, or any moment that needs to signal "pause and pay attention."

---

## 2026-03-20: Figma export — slide frames collapse to content height

**What happened:** First Figma export attempt produced slides ~220px tall instead of 816px. All 10 slides were broken. Setting `layoutMode = "VERTICAL"` on the slide frame causes Figma to default to "hug contents" sizing, ignoring the `resize(1456, 816)` call.

**The rule:** When exporting to Figma, ALWAYS set both `primaryAxisSizingMode = "FIXED"` and `counterAxisSizingMode = "FIXED"` on every slide frame immediately after setting `layoutMode`. Without these two lines, every slide collapses. This is the #1 Figma export bug.

---

## 2026-03-20: Figma export — auto-layout children clip content

**What happened:** Multiple slides had text cut off, descriptions missing, or content hidden. Auto-layout child frames default to `clipsContent = true` and fixed heights, hiding overflow content.

**The rule:** After building all slides in Figma, run a fidelity check comparing every Figma slide against Paper originals. Common fixes: set `clipsContent = false` on content frames, set `layoutSizingVertical = "HUG"` on containers that should expand to fit children, and use `figma.getNodeByIdAsync()` (not `getNodeById`) due to `documentAccess: dynamic-page`.

---

## 2026-03-20: Figma export — always use getNodeByIdAsync

**What happened:** `figma.getNodeById()` threw "Cannot call with documentAccess: dynamic-page" error.

**The rule:** Always use `await figma.getNodeByIdAsync(id)` in Figma Console MCP calls. Never use the synchronous `getNodeById`.

---

## 2026-03-21: Figma export — HORIZONTAL header rows default to 100px FIXED height

**What happened:** Slide 09 (What It Delivers) had numbered items 01-04 spread across the entire right column height with ~100px gaps. Root cause: each header row (containing "01" + "VALIDATED DECISION TRIGGERS") was created as a HORIZONTAL auto-layout frame but defaulted to `height: 100, layoutSizingVertical: "FIXED"` instead of HUG. Each row was 100px tall when it should have been ~34px.

**The rule:** After creating any HORIZONTAL auto-layout frame that contains text, explicitly set `layoutSizingVertical = "HUG"`. Figma defaults new auto-layout frames to a fixed height. This is invisible at creation time but causes massive spacing distortion in vertical stacks.

---

## 2026-03-21: Figma export — HUG panels can't CENTER their content

**What happened:** Slide 14 (The Vision) right panel had `primaryAxisAlignItems = "CENTER"` but content was still top-aligned. Root cause: the panel's `layoutSizingVertical` was "HUG", which shrinks the panel to its content height. Centering requires extra space to distribute, so HUG makes CENTER meaningless.

**The rule:** For vertical centering to work in Figma auto-layout, the container must have `layoutSizingVertical = "FILL"` (not HUG). FILL gives the container its full parent height. Then CENTER distributes the extra space above and below the content. If you set CENTER on a HUG frame, nothing happens.

---

## 2026-03-21: Figma export — footer positioning must account for padding

**What happened:** On all 19 slides, the footer ("CODE AND THEORY" + page number) was partially clipped at the bottom edge. The footer frame was positioned at y=756 (816-60), leaving only 60px which the frame itself consumed, putting text at the absolute edge.

**The rule:** Position footer frames at `y = slideHeight - 86` (not `slideHeight - 60`). This gives ~26px of breathing room below the footer text, matching Paper's visual spacing. For 816px slides: `footer.y = 730`.

---

## 2026-03-21: Figma export — fidelity agent must inspect node properties, not just screenshots

**What happened:** Spawned a layout comparison agent that screenshotted all 19 slides and compared Paper vs Figma. The agent described differences as "slight" and "slightly higher" when in reality items were 200px misaligned. It completely missed the root causes (FIXED 100px header rows, HUG preventing CENTER).

**The rule:** Screenshot comparison catches symptoms, not causes. When the fidelity check finds layout drift, the agent MUST inspect the node tree (`layoutMode`, `layoutSizingVertical`, `primaryAxisAlignItems`, actual height vs expected height) to diagnose the structural issue. "It looks different" is not a diagnosis. "This frame is FIXED at 100px when it should HUG to 34px" is.

---

## 2026-03-21: Figma export — split-panel slides need both panels CENTER + FILL

**What happened:** Slide 14 (The Vision) has a red left panel and cream right panel side by side. The left panel content sat at the bottom while the right panel content sat at the top. The two panels' vertical centers didn't align.

**The rule:** For split-panel slides, both panels must have `primaryAxisAlignItems = "CENTER"` and `layoutSizingVertical = "FILL"`. If one panel is flex-end (bottom) and the other is flex-start (top), the content looks misaligned even though each panel is internally consistent. Center both so they share the same visual midline.

---

## 2026-03-23: Headline-to-headline transitions must flow. Score each one.

**What happened:** Headlines read fine individually but the sequence had cold jumps. "That asymmetry is the imitation premium" → "The time buffer is gone" introduced a completely new metaphor with no shared language. "The scarf is the least important thing Hermes sells" → "The moat doesn't get breached" had tonal whiplash from positive to negative with no bridge.

**The rule:** After writing all headlines, score every A→B transition (1-10): does B follow naturally from A? Shared language, logical progression, or emotional continuity all count. Below 6 on any transition = rewrite. The test: read headlines aloud in sequence. Any moment where you'd think "wait, how did we get here?" is broken. This is now a sub-score within the Narrative Flow pass (added to quality-system.md as the 6th dimension: Headline Narrative).

**Technique:** Use callback language. If slide 4 names "the premium," slide 5 should reference "the premium" or "the gap." If slides 6-7 establish "above the line," slide 9 should use "above the line" when introducing the failure mode. Shared nouns across adjacent headlines are the connective tissue.

---

## 2026-03-23: Headlines must tell the story without body copy.

**What happened:** Julian flagged that headlines should carry the full narrative arc on their own. If you read just the headlines in sequence, you should be able to follow the argument without any body copy.

**The rule:** After writing all slide headlines, read them in sequence as a standalone narrative. Each headline should advance the argument one beat. The body copy supports, adds evidence, and adds texture, but the headlines do the structural work. Add this as a 6th dimension to the Narrative Flow pass: "Headline Narrative" (1-10). Score: can a stranger read the headlines alone and follow the argument?

---

## 2026-03-23: Every slide must introduce a new idea. No hanging provocations.

**What happened:** The deck had 16 slides but several restated the same feature-vs-brand contrast from different angles. Slides 5, 6, and 7 all hammered one idea. The writing had "characteristic AI blurriness" - big words without enough new thinking. Worse: the deck raised "which side of the threshold are you on?" as a question but never gave the reader a way to figure it out. Empty provocation.

**The rule (two parts):**

1. **One new idea per slide.** Before writing any slide, state in one sentence what NEW concept this slide introduces that no previous slide has covered. If you can't, cut the slide or merge it. Restating the same idea with different examples is not a new idea. Proof of an existing idea (examples, stats) earns its slide only if it adds a genuinely new dimension.

2. **No hanging ideas.** If a slide raises a question, framework, or provocation, a subsequent slide must pay it off with specifics. "Which side are you on?" requires a framework for self-assessment. "Pressure-test the worldview" requires at least a gesture at what that looks like. If you can't pay it off, don't raise it.

---

## 2026-03-23: Kill AI blurriness in deck copy.

**What happened:** Julian flagged the source narrative and deck copy as sounding too much like AI. "A lot of big words, not a lot of new ideas." Phrases like "the kind of accumulated meaning" and "building toward the altitude where the imitation premium kicks in" are conceptually vague. They gesture at ideas without landing them.

**The rule:** Deck copy should be concrete, specific, and surprising. Every sentence should either name something (a company, a number, a behavior) or reframe something the audience thought they understood. Abstract conceptual language ("accumulated meaning," "depth of meaning," "cultural weight") must be replaced with observable, testable statements. If you can't point to what it looks like in the real world, the sentence is blurry. Cut it or make it concrete.

---

## 2026-03-22: ALWAYS build in Paper first. Figma is export only.

**What happened:** Paper MCP wasn't immediately connected. Instead of reconnecting Paper, launched Figma Desktop and attempted to build the deck in Figma Slides. Julian flagged this as wrong. Paper is the primary design tool. Figma is a last resort or an export destination.

**The rule:** Paper is always the starting point for /paper-slides. If the Paper MCP isn't connected, tell the user and wait for reconnection (they can run `/mcp` to reconnect). NEVER open Figma as a substitute. Figma is only used in two scenarios: (1) the Figma Export flow in Phase 6, or (2) when Julian explicitly asks to build in Figma. This requires explicit approval. Default to Paper, always.
