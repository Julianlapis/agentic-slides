---
name: figma-export
description: Figma Export Pipeline for Paper Slides - editable Figma layers via Desktop Bridge MCP
---

# Figma Export Pipeline for Paper Slides

## What This Does

Exports a Paper deck into editable Figma frames with real text layers, correct fonts, proper colors, and auto-layout. The team can collaborate on the Figma file, modify text, swap colors, and hand off to production.

## Prerequisites

### 1. Figma Console MCP Server (one-time setup)

Install the MCP server into Claude Code:

```bash
claude mcp add figma-console \
  -s user \
  -e FIGMA_ACCESS_TOKEN=figd_YOUR_TOKEN_HERE \
  -e ENABLE_MCP_APPS=true \
  -- npx -y figma-console-mcp@latest
```

To get a Figma access token: Figma → Settings → Account → Personal access tokens → Generate.

### 2. Desktop Bridge Plugin (one-time setup)

The plugin files live at `~/.figma-console-mcp/plugin/`. They're installed automatically when the MCP server first runs. To load the plugin into Figma:

1. Open Figma Desktop (not web)
2. Plugins → Development → Import plugin from manifest
3. In the file picker, press **Cmd+Shift+G** and paste: `~/.figma-console-mcp/plugin/`
4. Select `manifest.json` → Open

Once imported, it persists across sessions. You only need to run it each time:
Plugins → Development → Figma Desktop Bridge

### 3. Font Availability

Fonts used in Paper must be installed locally for Figma to load them. Cormorant Garamond and Inter are the defaults for C&T strategy decks. Google Fonts installs work. Figma will throw on `loadFontAsync` if a font/weight combo isn't available.

---

## Architecture

Two MCP servers in sequence:

1. **Paper MCP** (read): `get_basic_info`, `get_jsx`, `get_computed_styles`, `get_screenshot`
2. **Figma Console MCP** (write): `figma_execute`, `figma_capture_screenshot`, `figma_set_image_fill`

No intermediate JSON format. Translation happens directly from Paper's JSX output to Figma Plugin API calls.

---

## Preflight (MANDATORY)

Run these checks before extracting anything from Paper. If Figma is unreachable, stop immediately.

### Step 1: Test Bridge Connection

```javascript
// figma_execute
return { ok: true, timestamp: Date.now() }
```

If this fails with "Cannot connect to Figma Desktop", the user needs to open the Desktop Bridge plugin in Figma. Check `lsof -i :9223` to verify the WebSocket port.

### Step 2: Create a Dedicated Page

```javascript
const page = figma.createPage();
page.name = "V4 — Deck Name";
await figma.setCurrentPageAsync(page);
```

Clean up any duplicate/empty pages after creation.

### Step 3: Load All Fonts

```javascript
const fonts = [
  { family: "Inter", style: "Regular" },
  { family: "Inter", style: "Medium" },
  { family: "Inter", style: "Semi Bold" },
  { family: "Inter", style: "Bold" },
  { family: "Inter", style: "Light" },
  { family: "Cormorant Garamond", style: "Regular" },
  { family: "Cormorant Garamond", style: "Light" },
  { family: "Cormorant Garamond", style: "Medium" },
  { family: "Cormorant Garamond", style: "Bold" },
  { family: "Cormorant Garamond", style: "Italic" },
];
const loaded = [], failed = [];
for (const f of fonts) {
  try { await figma.loadFontAsync(f); loaded.push(f); }
  catch { failed.push(f); }
}
```

Present the font manifest to the user. If critical fonts fail, stop and resolve before proceeding.

### Step 4: Get Paper Deck Structure

```
get_basic_info() → artboards list with IDs, names, dimensions
```

Filter to the target version (e.g., artboards starting with "V4 —").

---

## Per-Slide Pipeline

For each slide, in order:

### 1. Extract from Paper

```
get_jsx(nodeId, format: "inline-styles") → JSX with all styles
```

This is the primary source of truth. Only use `get_computed_styles` if JSX inline styles are missing something.

### 2. Translate to Figma

One `figma_execute` call per slide (stays within 30s timeout for typical slides).

#### CRITICAL: Frame Sizing Fix

When you set `layoutMode` on a frame, Figma defaults to "hug contents" sizing, which collapses the slide to content height. You MUST set fixed sizing immediately after:

```javascript
const slide = figma.createFrame();
slide.layoutMode = "VERTICAL";
slide.resize(1456, 816);
slide.primaryAxisSizingMode = "FIXED";  // ← THIS IS MANDATORY
slide.counterAxisSizingMode = "FIXED";  // ← THIS IS MANDATORY
```

Without these two lines, every slide will collapse to ~200px tall. This was the #1 bug in the initial implementation.

#### Helper Functions

Include these in every `figma_execute` call:

```javascript
// Parse hex color (supports #RRGGBB and #RRGGBBAA)
function pc(hex) {
  hex = hex.replace('#','');
  const r = parseInt(hex.substr(0,2),16)/255;
  const g = parseInt(hex.substr(2,2),16)/255;
  const b = parseInt(hex.substr(4,2),16)/255;
  const a = hex.length === 8 ? parseInt(hex.substr(6,2),16)/255 : 1;
  return { r, g, b, a };
}

// Set fill with opacity from hex8
function sf(node, hex) {
  const c = pc(hex);
  node.fills = [{
    type: 'SOLID',
    color: { r: c.r, g: c.g, b: c.b },
    opacity: c.a
  }];
}
```

#### CSS → Figma Property Mapping

| CSS | Figma Plugin API |
|-----|-----------------|
| `display: flex; flex-direction: column` | `layoutMode = "VERTICAL"` |
| `display: flex` (row) | `layoutMode = "HORIZONTAL"` |
| `gap: 12px` | `itemSpacing = 12` |
| `justify-content: flex-end` | `primaryAxisAlignItems = "MAX"` |
| `justify-content: center` | `primaryAxisAlignItems = "CENTER"` |
| `justify-content: space-between` | `primaryAxisAlignItems = "SPACE_BETWEEN"` |
| `align-items: center` | `counterAxisAlignItems = "CENTER"` |
| `flex-grow: 1` | `layoutGrow = 1` |
| `padding: 60px` | `paddingTop/Bottom/Left/Right = 60` |
| `background-color` | `fills = [{ type: 'SOLID', color, opacity }]` |
| `color` (text) | `fills` on text node (same format) |
| `font-family` | `fontName = { family, style }` |
| `font-size` | `fontSize` (px number) |
| `font-weight: 700` | `fontName.style = "Bold"` |
| `font-weight: 600` | `fontName.style = "Semi Bold"` |
| `font-weight: 500` | `fontName.style = "Medium"` |
| `font-weight: 300` | `fontName.style = "Light"` |
| `font-style: italic` | `fontName.style = "Italic"` |
| `letter-spacing: 0.15em` | `letterSpacing = { value: 15, unit: "PERCENT" }` |
| `line-height: 26px` | `lineHeight = { value: 26, unit: "PIXELS" }` |
| `text-transform: uppercase` | `textCase = "UPPER"` |
| `text-align: center` | `textAlignHorizontal = "CENTER"` |
| `overflow: hidden/clip` | `clipsContent = true` |
| `max-width: 900px` | `resize(900, node.height)` |
| `width: 100%` (in auto-layout) | `layoutSizingHorizontal = "FILL"` |
| `flex-grow: 1` (height) | `layoutSizingVertical = "FILL"` |
| `position: absolute` | `layoutPositioning = "ABSOLUTE"` + constraints |
| No fill (transparent) | `fills = []` |

#### Font Weight Map

| CSS fontWeight | Figma style string |
|---------------|-------------------|
| 400 / normal | `"Regular"` |
| 500 | `"Medium"` |
| 600 | `"Semi Bold"` |
| 700 / bold | `"Bold"` |
| 300 | `"Light"` |
| italic | `"Italic"` |

#### Footer Pattern (Absolute Positioned)

The footer in C&T strategy decks is absolute-positioned at the bottom:

```javascript
const footer = figma.createFrame();
slide.appendChild(footer);
footer.name = "Footer";
footer.fills = [];
footer.layoutPositioning = "ABSOLUTE";
footer.constraints = { horizontal: "STRETCH", vertical: "MAX" };
footer.layoutMode = "HORIZONTAL";
footer.primaryAxisAlignItems = "SPACE_BETWEEN"; // or "MAX" for right-only, "CENTER" for centered
footer.x = 0;
footer.y = 730; // slide height (816) minus 86px — gives 26px breathing room below text
footer.resize(1456, 60);
footer.paddingLeft = 60;
footer.paddingRight = 60;
footer.counterAxisAlignItems = "MAX";
```

#### Slide Positioning

Space slides horizontally on the Figma canvas:

```javascript
slide.x = slideIndex * (slideWidth + 80); // 80px gap between slides
```

### 3. Verify

After writing each slide (or every 2-3 slides for speed):

```
figma_capture_screenshot(nodeId, scale: 1)
```

Compare visually against Paper original (`get_screenshot` from Paper MCP).

---

## Known Pitfalls

### 1. Frame Height Collapse (CRITICAL)
**Problem:** `layoutMode = "VERTICAL"` makes frames hug content by default.
**Fix:** Always set `primaryAxisSizingMode = "FIXED"` and `counterAxisSizingMode = "FIXED"` on slide frames.

### 2. Content Clipping
**Problem:** Auto-layout child frames default to `clipsContent = true` and may clip text.
**Fix:** After building, walk the tree and set `clipsContent = false` on content frames. Set `layoutSizingVertical = "HUG"` on containers that should expand to fit their children.

### 3. Stroke API Differences
**Problem:** `node.strokes` requires `color: { r, g, b }` without `a` (opacity goes in a separate property). Using `pc()` which returns `{ r, g, b, a }` will fail.
**Fix:** For strokes, use `color: { r, g, b }` only. Set stroke opacity separately if needed.

### 4. Individual Stroke Weights
**Problem:** Setting `strokeLeftWeight`, `strokeTopWeight` etc. on frames without `strokesAlign` set causes "object is not extensible" errors.
**Fix:** Use a thin colored frame as a visual line/border instead of stroke properties. More reliable.

### 5. Dynamic Page Access
**Problem:** `figma.getNodeById()` fails with `documentAccess: dynamic-page`.
**Fix:** Always use `await figma.getNodeByIdAsync()`.

### 6. figma_execute Timeout
**Problem:** Default timeout is 5000ms. Complex slides need more.
**Fix:** Set `timeout: 30000` on every `figma_execute` call. If a slide has 40+ nodes, split into multiple calls.

### 7. Housekeeping Warnings
**Problem:** Figma Console MCP warns about floating nodes, duplicate pages, etc.
**Fix:** Ignore these during the build. Clean up orphaned frames at the end.

### 8. HORIZONTAL Auto-Layout Frames Default to 100px Height (CRITICAL)
**Problem:** When you create a HORIZONTAL auto-layout frame (e.g., a row containing a number + label), Figma defaults it to ~100px FIXED height even though its content is only ~34px. This causes massive vertical spacing distortion in parent VERTICAL containers.
**Fix:** After creating any HORIZONTAL auto-layout frame, immediately set `layoutSizingVertical = "HUG"`. This was the root cause of slide 09's items being spread across the full height.

### 9. HUG Containers Can't CENTER Content (CRITICAL)
**Problem:** Setting `primaryAxisAlignItems = "CENTER"` on a VERTICAL frame that has `layoutSizingVertical = "HUG"` does nothing. HUG shrinks the frame to exactly fit its content, leaving zero extra space for centering to distribute.
**Fix:** For vertical centering to work, the container must be `layoutSizingVertical = "FILL"` so it takes its full parent height. Then CENTER distributes the extra space above and below the content.

### 10. Split-Panel Slides Need Aligned Vertical Centers
**Problem:** In side-by-side panel layouts (e.g., slide 14's red left + cream right), if one panel uses `MAX` (bottom-align) and the other uses `MIN` (top-align), the content blocks look misaligned even though each panel is internally correct.
**Fix:** Set both panels to `primaryAxisAlignItems = "CENTER"` and `layoutSizingVertical = "FILL"`. This ensures both content blocks share the same visual midline.

---

## Fidelity Check Process

After all slides are written, do a systematic comparison:

1. **Screenshot every Figma slide** via `figma_capture_screenshot`
2. **Screenshot every Paper slide** via Paper MCP `get_screenshot`
3. **Compare side by side** looking for:
   - Content clipping (text cut off)
   - Missing content (elements not rendered)
   - Wrong vertical positioning (centered vs bottom-aligned)
   - Color mismatches
   - Font/weight mismatches
   - Spacing differences
4. **Fix issues** by modifying Figma node properties via `figma_execute` + `figma.getNodeByIdAsync()`
5. **Re-screenshot** to verify fixes

Common fixes needed:
- `clipsContent = false` on frames that clip children
- `layoutSizingVertical = "HUG"` on containers that should expand
- `primaryAxisAlignItems` adjustments (MIN vs CENTER vs MAX)
- `itemSpacing` tweaks to match Paper's CSS gap values

---

## Performance Benchmarks (from spike)

| Operation | Time |
|-----------|------|
| Preflight (`return { ok: true }`) | ~7ms |
| Font loading (10 fonts) | ~2s |
| Simple slide (title, 5 nodes) | ~15s |
| Complex slide (20+ nodes) | ~25s |
| Full 19-slide deck | ~15 min |
| Screenshot (per slide) | instant |
| Fidelity check + fixes | ~10 min |

Total for a 19-slide deck: ~25 minutes (export + fidelity pass).

---

## What This Produces

- One Figma page with one frame per slide at presentation dimensions
- Editable text layers with correct fonts
- Auto-layout frames matching Paper's flex-based structure
- Named layers matching Paper's content hierarchy
- Real color fills (not flattened rasters)
- Absolute-positioned footers matching Paper's layout
- All content visible and un-clipped

## What This Does NOT Produce

- Pixel-perfect rendering (Figma and Paper use different text engines)
- Auto-layout that perfectly mirrors every CSS flex nuance
- Figma components or variants (slides are flat frame hierarchies)
- Design tokens or variables (colors/fonts are per-node)
- Images (image fills would need separate `figma_set_image_fill` calls)
- Speaker notes, animations, or slide ordering

---

## Dependencies

- Figma Desktop app (not web)
- Figma Console MCP server (`npx figma-console-mcp@latest`)
- Desktop Bridge plugin (`~/.figma-console-mcp/plugin/manifest.json`)
- Figma personal access token (in MCP env config)
- Fonts used in Paper installed locally
- Paper MCP (already installed, `localhost:29979`)
