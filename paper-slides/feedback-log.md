---
name: feedback-log
description: Paper Slides Feedback Log - read at the start of every /paper-slides invocation to avoid repeating mistakes
---

# /paper-slides Feedback Log

Read this file at the start of every /paper-slides invocation. It contains corrections from real usage sessions. Every rule here overrides default behavior. At the end of every session, capture any new user corrections and append them to this log.

---

## 2026-03-19: Artboard layout order not set

**What happened:** Built/edited 28 slides across multiple rows on the canvas instead of laying them out in a single horizontal row, left to right, in slide order. the user had to ask for this explicitly.

**The rule:** Always position artboards in a single horizontal row, left to right, in presentation order. Formula: `left = (slide_index - 1) * (artboard_width + 80)`, `top = 0`. Do this from the start when creating new decks, and verify/fix it when editing existing decks. This is how Paper presents slides for PDF export and how the user navigates the canvas.

---

## 2026-03-19: Body copy too small for presentation

**What happened:** Body text was set at 14-18px across content slides. the user flagged it as unreadable at presentation scale. Had to bump twice before landing on the right sizes.

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

**What happened:** Started making design changes without first saving the slide copy to a reference file. the user had to ask for this explicitly to prevent losing track of verbatim content.

**The rule:** Before making ANY design changes to an existing deck, extract all text content from every slide and save it as an MD file (e.g., `~/Desktop/[project]-content.md`). Reference this file throughout the editing session. Verify text content against it after making changes.

---

## 2026-03-19: Design system file not loaded proactively

**What happened:** the user had to point out that a design system file existed and should be referenced. Should have checked for design system layers/files immediately upon opening the Paper file.

**The rule:** After `get_basic_info`, always check for design system files: search for `*design-system*` or `*design_system*` in the Paper file's artboards, and check the skill's references directory for matching design systems. Load the design system BEFORE making any visual changes.

---

## 2026-03-19: Quality system not run automatically

**What happened:** Made changes across multiple passes without running the three-pass quality system (Design Quality Agent, Narrative Flow Agent, Copy Quality Pass) until the user asked for it.

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
