# Default Design System

The fallback when no design system is provided. Minimal, monochromatic, works for any deck type. Derived from the TMS Core 2.0 template system.

---

## Canvas

- **Artboard size:** 1440 x 810px (16:9)
- **Content safe zone:** 32px padding on all sides
- **Footer zone:** Bottom 56px of the slide

---

## Color Palette

Pick one variant per deck and commit. Never mix variants within a deck.

| Variant | Background | Primary Text | Secondary Text | Panel Fill |
|---------|-----------|-------------|---------------|-----------|
| **Light** | `#FFFFFF` | `#1A1A1A` | `#777777` | `#1A1A1A` |
| **Dark** | `#111111` | `#F5F5F5` | `#999999` | `#222222` |

### Rules
- No accent colors by default. The system is monochromatic.
- Panel contrast: when a slide has a data panel, the panel fill contrasts with the background.
- No gradients, no shadows, no borders. Visual separation comes from background contrast and whitespace.

---

## Typography

### Font
One font family throughout. Default: **Helvetica Neue**. If unavailable, use Inter, Suisse Int'l, or whatever clean grotesque is available. Verify with `get_font_family_info`.

### Type Scale

| Role | Size | Weight |
|------|------|--------|
| Display | 68-72px | Regular (400) |
| Section Title | 40-44px | Regular (400) |
| Body | 24-26px | Regular (400) |
| Caption | 16-18px | Regular (400) |
| Label / Footer | 14px | Regular (400) |

### Rules
- No bold. Hierarchy comes from size contrast alone.
- No italic. Everything is upright.
- No all-caps. Sentence case or title case throughout.
- No letterspacing on labels (unlike strategy decks).
- Subtitles: same font, same weight, differentiated only by secondary text color.
- Section numbers ("01", "02") sit inline with their labels at the same size.

---

## Spacing

| Element | Value |
|---------|-------|
| Artboard padding | 32px |
| Section gap | 48px |
| Element gap (within a group) | 16px |
| Image grid gap | 5px |
| Column gap | 24px |

---

## Structural Elements

### Allowed
- Whitespace as separator
- Background color contrast between panels
- Thin horizontal rules (1px, primary text color) sparingly

### Banned
- Drop shadows
- Rounded corners (all rectangles are sharp)
- Borders on containers
- Icons or pictograms
- Decorative elements
- Card backgrounds (content sits directly on the surface)

---

## Images

- Sharp corners, no rounding
- Object-fit: cover, fill containers completely
- Tight grid gaps (5px)
- No image borders or shadows
- No captions beneath images unless the layout specifically calls for them

---

## Footer

Three lines, stacked vertically, bottom-left, 14px, primary text color:
```
[Company]
[Date]
[Project]
```
Appears on every slide except title and full-bleed images.

---

## Slide Backgrounds

All slides in a deck use the same background color (light or dark variant). Unlike editorial/strategy systems that alternate backgrounds for drama, this system keeps the background constant. Visual variety comes from layout diversity and content, not background switching.

The one exception: panel fills (TOC index panels, data containers) use the contrasting color.
