---
name: figma-export
description: Figma build and export pipeline using the official Figma MCP use_figma tool
---

# Figma Pipeline

## What This Does

Two modes:

1. **Build in Figma** — constructs slides directly on the Figma canvas using `use_figma`. The deck lives natively in Figma with real frames, auto-layout, text layers, and (when available) design system components and variables.
2. **Paper → Figma export** — reads a completed Paper deck, translates each slide into editable Figma frames. The team can collaborate, modify, and hand off in Figma.

## Prerequisites

The official Figma MCP server must be connected. This is available as a claude.ai integration — no local install required.

**Required tools:**
- `mcp__claude_ai_Figma__use_figma` — write to the canvas (Plugin API JavaScript)
- `mcp__claude_ai_Figma__get_screenshot` — screenshot nodes for verification
- `mcp__claude_ai_Figma__get_design_context` — read existing designs
- `mcp__claude_ai_Figma__search_design_system` — find reusable components/variables
- `mcp__claude_ai_Figma__get_metadata` — file structure and pages

**User provides:** A Figma file URL or file key. Extract the key from the URL: `figma.com/design/:fileKey/:fileName`.

**Fonts:** Fonts used in the deck must be available in the Figma file. Use `loadFontAsync` to verify before writing text. Google Fonts are generally available. Custom fonts need to be uploaded to the Figma team.

---

## Architecture

Single MCP server: the official Figma MCP. Each slide is one `use_figma` call containing Plugin API JavaScript.

For Paper → Figma export, Paper MCP is also used (read-only) to extract slide structure:
- `get_basic_info` → artboard list
- `get_jsx(nodeId, format: "inline-styles")` → slide structure and styles
- `get_computed_styles(nodeIds)` → precise CSS values when needed

---

## Preflight

### Step 1: Test Access

```javascript
// use_figma probe
return { ok: true, timestamp: Date.now() }
```

If this fails, the Figma MCP server isn't connected.

### Step 2: Create a Dedicated Page

```javascript
const page = figma.createPage();
page.name = "Deck Name — V1";
await figma.setCurrentPageAsync(page);
return { pageId: page.id, pageName: page.name };
```

### Step 3: Load Fonts

```javascript
const fonts = [
  { family: "Inter", style: "Regular" },
  { family: "Inter", style: "Medium" },
  { family: "Inter", style: "Semi Bold" },
  { family: "Inter", style: "Bold" },
  { family: "Inter", style: "Light" },
];
const loaded = [], failed = [];
for (const f of fonts) {
  try { await figma.loadFontAsync(f); loaded.push(f); }
  catch { failed.push(f); }
}
return { loaded, failed };
```

Adapt the font list to the design system. Present results to the user. If critical fonts fail, resolve before proceeding.

### Step 4: Search for Design System Components

Before building from scratch, check what's already available:

```
mcp__claude_ai_Figma__search_design_system(fileKey, query: "button")
```

Import reusable components via `importComponentByKeyAsync` / `importComponentSetByKeyAsync` instead of recreating them.

---

## Per-Slide Build

### Building Directly in Figma

One `use_figma` call per slide. Each call creates a complete slide frame with all content.

```javascript
// Slide frame setup — CRITICAL sizing rules
const slide = figma.createFrame();
slide.name = "01 — Title Slide";
slide.layoutMode = "VERTICAL";
slide.resize(1456, 816);
slide.primaryAxisSizingMode = "FIXED";   // MANDATORY — prevents height collapse
slide.counterAxisSizingMode = "FIXED";   // MANDATORY — prevents width collapse
slide.paddingTop = 60;
slide.paddingBottom = 60;
slide.paddingLeft = 60;
slide.paddingRight = 60;
slide.x = slideIndex * (1456 + 80);      // horizontal spacing between slides

// Background
sf(slide, "#1A1A1A");

// Content + text nodes...
```

### Paper → Figma Export

For each Paper slide:

1. **Extract from Paper:** `get_jsx(nodeId, format: "inline-styles")` — primary source of truth
2. **Translate to Figma:** Convert CSS properties to Plugin API equivalents (see mapping below)
3. **Write to Figma:** One `use_figma` call per slide

### Verify

After every 2-3 slides:

```
mcp__claude_ai_Figma__get_screenshot(fileKey, nodeId)
```

Compare visually against intent (or Paper original for exports). Fix mismatches before continuing.

---

## Helper Functions

Include these in `use_figma` calls that need them:

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

---

## CSS → Figma Property Mapping

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

### Font Weight Map

| CSS fontWeight | Figma style string |
|---------------|-------------------|
| 400 / normal | `"Regular"` |
| 500 | `"Medium"` |
| 600 | `"Semi Bold"` |
| 700 / bold | `"Bold"` |
| 300 | `"Light"` |
| italic | `"Italic"` |

---

## Known Pitfalls

### 1. Frame Height Collapse (CRITICAL)
**Problem:** `layoutMode = "VERTICAL"` makes frames hug content by default.
**Fix:** Always set `primaryAxisSizingMode = "FIXED"` and `counterAxisSizingMode = "FIXED"` on slide frames.

### 2. HORIZONTAL Frames Default to 100px Height (CRITICAL)
**Problem:** HORIZONTAL auto-layout frames default to ~100px FIXED height even when content is shorter.
**Fix:** After creating any HORIZONTAL auto-layout frame, immediately set `layoutSizingVertical = "HUG"`.

### 3. HUG Containers Can't CENTER Content (CRITICAL)
**Problem:** `primaryAxisAlignItems = "CENTER"` on a HUG frame does nothing — there's no extra space to distribute.
**Fix:** Container must be `layoutSizingVertical = "FILL"` for vertical centering to work.

### 4. Content Clipping
**Problem:** Auto-layout child frames default to `clipsContent = true`.
**Fix:** Set `clipsContent = false` on content frames. Use `layoutSizingVertical = "HUG"` on containers that should expand.

### 5. Stroke API
**Problem:** `node.strokes` requires `color: { r, g, b }` without `a`.
**Fix:** For strokes, use `color: { r, g, b }` only. Set stroke opacity separately.

### 6. Dynamic Page Access
**Problem:** `figma.getNodeById()` fails with dynamic page access.
**Fix:** Always use `await figma.getNodeByIdAsync()`.

### 7. Split-Panel Alignment
**Problem:** Side-by-side panels with different vertical alignment look misaligned.
**Fix:** Set both panels to `primaryAxisAlignItems = "CENTER"` and `layoutSizingVertical = "FILL"`.

---

## Footer Pattern (Absolute Positioned)

```javascript
const footer = figma.createFrame();
slide.appendChild(footer);
footer.name = "Footer";
footer.fills = [];
footer.layoutPositioning = "ABSOLUTE";
footer.constraints = { horizontal: "STRETCH", vertical: "MAX" };
footer.layoutMode = "HORIZONTAL";
footer.primaryAxisAlignItems = "SPACE_BETWEEN";
footer.x = 0;
footer.y = 730; // slide height (816) minus 86px
footer.resize(1456, 60);
footer.paddingLeft = 60;
footer.paddingRight = 60;
footer.counterAxisAlignItems = "MAX";
```

---

## Fidelity Check (Paper → Figma Export)

After all slides are written:

1. Screenshot every Figma slide via `mcp__claude_ai_Figma__get_screenshot`
2. Screenshot every Paper slide via Paper MCP `get_screenshot`
3. Compare side by side for: clipping, missing content, wrong positioning, color/font mismatches, spacing differences
4. Fix via `use_figma` with `figma.getNodeByIdAsync()` to target specific nodes
5. Re-screenshot to verify

---

## What This Produces

- One Figma page with one frame per slide at presentation dimensions
- Editable text layers with correct fonts
- Auto-layout frames matching the deck's flex-based structure
- Named layers matching the content hierarchy
- Real color fills (not flattened rasters)
- When available: design system components and variables reused from the file's existing library

## What This Does NOT Produce (yet)

- Pixel-perfect rendering (Figma and Paper use different text engines)
- Images (image support coming in future Figma MCP updates)
- Speaker notes, animations, or slide transitions
- Figma components or variants from scratch (slides are frame hierarchies unless building from existing components)
