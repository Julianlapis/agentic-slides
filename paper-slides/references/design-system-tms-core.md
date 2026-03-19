# TMS Core 2.0 Design System

A modular, monofont presentation template system extracted from the TMS Core 2.0 deck (192 slides, 64 unique layouts across 3 color variants). Use this as a reference for corporate/portfolio/case study decks that need visual richness through imagery and systematic structure rather than typographic drama.

This system complements the C&T Strategy design system. Strategy decks use serif/sans contrast and red as a narrative device. TMS Core uses a single font family, neutral palette, and image density as the primary design tool.

---

## When to Use TMS Core vs C&T Strategy

| Signal | Use TMS Core | Use C&T Strategy |
|--------|-------------|-----------------|
| Content is image-heavy (case studies, portfolio, capabilities) | Yes | No |
| Deck needs a neutral, client-agnostic aesthetic | Yes | No |
| Deck is making a strategic argument with minimal imagery | No | Yes |
| Content involves people bios, team pages, image galleries | Yes | No |
| Deck needs to feel editorial, opinionated, high-conviction | No | Yes |
| Client wants a template they can reuse across projects | Yes | No |

---

## Canvas

- **Artboard size:** 1440 x 810px (16:9, matching 1920x1080 proportional)
- **Content safe zone:** 22px padding all sides
- **Content area:** 1396 x 766px
- **Footer zone:** Bottom 56px of the slide (Company / Date / Project stacked left)

---

## Color System

TMS Core works in 3 parallel colorways. Every layout exists in all 3. Pick one per deck and commit.

| Variant | Background | Primary Text | Secondary Text | Panel Fill |
|---------|-----------|-------------|---------------|-----------|
| **Light** | `#FFFFFF` | `#000000` | `#666666` | `#000000` |
| **Mid** | `#C9CACF` | `#000000` | `#555555` | `#FFFFFF` |
| **Dark** | `#000000` | `#FFFFFF` | `#C9CACF` | `#C9CACF` |

### Color Rules

1. **No accent colors.** The system is monochromatic. Black, white, and one mid-gray. Period.
2. **Panel contrast.** When a slide has a data panel (TOC index, content block), the panel fill is the opposite of the background. Dark panel on light slide. Light panel on dark slide.
3. **Text color flips with background.** On light backgrounds, text is black. On dark backgrounds, text is white. Secondary text uses the mid-gray in both cases.
4. **No gradients, no shadows, no borders.** Visual separation comes from background contrast between panels, not decorative elements.

---

## Typography

### Single Font System

TMS Core uses **one font family** throughout. The original uses Helvetica Neue. In Paper, use whichever clean grotesque is available: Helvetica Neue, Inter, Suisse Int'l, or Aktiv Grotesk. Verify with `get_font_family_info`.

The hierarchy comes entirely from size and weight contrast, not font pairing.

### Type Scale

| Role | Size | Weight | Usage |
|------|------|--------|-------|
| **Display** | 68-72px | Regular (400) | Title slide headline, section dividers |
| **Section Title** | 40-44px | Regular (400) | Content slide headlines, "Title of section" |
| **Body** | 24-26px | Regular (400) | Main content text, TOC items, card descriptions |
| **Caption** | 16-18px | Regular (400) | Body paragraphs, descriptions, smaller content |
| **Label** | 14px | Regular (400) | Caption labels, footer text, metadata |
| **Micro** | 12px | Regular (400) | Image captions, numbering overlays |

### Typography Rules (TMS-Specific)

1. **No bold anywhere.** TMS Core achieves hierarchy through size contrast alone, not weight. Every text element is regular weight (400). This creates a distinctly calm, editorial feel.
2. **No italic.** Unlike the C&T Strategy system, there are no italic closers or emphasis. Everything is upright.
3. **No letterspacing on labels.** Unlike strategy decks where eyebrows are tracked out, TMS labels use default tracking.
4. **No all-caps.** Everything is sentence case or title case. The system avoids shouting.
5. **Subtitle sits directly below headline.** Same font, same weight, differentiated only by a muted color (secondary text color from the palette).
6. **Section numbers ("01", "02") are the same size and weight as their labels.** They don't get oversized treatment. The number and label sit side by side, inline, with a small gap.

---

## Spatial Grid

### Consistent Margins

Every slide uses the same margin system. Content starts at 22px from every edge. This creates a precise, engineered feel across 64 layouts.

### Panel Composition

When a slide splits into a text zone and a data/image zone, the split follows these rules:
- **Left text panel:** 33% width (approximately 474px) with 22px internal padding
- **Right content panel:** 67% width with a contrasting background fill, 35px internal padding
- The panels share the same top and bottom edges (22px from slide edges)
- No gap between panels. They abut directly.

### Image Grid Spacing

- **Gap between images:** 4-6px (very tight, creating a mosaic feel)
- **Images fill their cell completely.** No rounded corners, no padding within cells.
- **Grid bleeds to panel edges.** No margin between the image grid and its container.

---

## Footer System

Every slide (except title and full-bleed images) carries a footer.

### Structure
Three lines, stacked vertically, bottom-left:
```
Company     (14px, primary text color)
Date        (14px, primary text color)
Project     (14px, primary text color)
```

### Rules
- Footer sits at the very bottom of the content safe zone
- Left-aligned to the content margin (22px from left)
- No horizontal rule above the footer. It separates from content via whitespace.
- On slides with bottom content, the footer lives in the left text panel only

---

## Image Treatment

### Philosophy
TMS Core treats images as first-class content, not decoration. The system has layouts for 1, 2, 3, 4, 5, 6, 8, 12, and 18 images on a single slide. This range means you never need to artificially limit or pad your visual content.

### Image Rules
1. **All images are rectangular with sharp corners.** No rounded corners ever.
2. **Images fill their containers completely.** Object-fit: cover. No letterboxing.
3. **Tight grid gaps (4-6px).** The mosaic feel comes from images nearly touching.
4. **No captions beneath individual images** unless the layout specifically calls for them (the numbered caption variant).
5. **No image borders or shadows.** The image edge IS the boundary.

### Image Grid Patterns

| Count | Layout | Notes |
|-------|--------|-------|
| 1 | Full right panel or full bleed | Single hero image |
| 2 | Side by side, equal width | Horizontal split |
| 3 | 1 large left + 2 stacked right, OR 3 equal columns | Asymmetric preferred |
| 4 | 2×2 grid | Equal cells |
| 5 | 2 top + 3 bottom, OR 3 top + 2 bottom | Uneven rows create interest |
| 6 | 2×3 grid | Equal cells |
| 8 | 2×4 grid | 2 rows of 4 |
| 12 | 3×4 grid | Dense mosaic |
| 18 | 3×6 grid | Maximum density |

---

## Content Slides with Image Galleries

The most distinctive TMS Core pattern: a left text panel + right image gallery. The text panel contains:
- Caption label (top, 14px)
- Section title (40-44px)
- Subtitle (40-44px, secondary color)
- Body text (16-18px, bottom of panel)

The right panel contains the image grid. As image count increases (1→6), the text panel stays fixed and the grid densifies.

### Numbered Image Captions (Special Variant)
One layout adds numbered captions below each image in the grid:
- Small text label below image (12px, white text on image)
- Sequential number (12px) in the opposite corner
- This variant is for process steps or sequenced visual content

---

## Navigational Slides

### Agenda / Table of Contents (Simple)
- 5 items stacked vertically, each row: "01" + "Section name"
- Number and name are the same size (display scale, 68-72px)
- Number in secondary color, name in primary
- Content pinned to top-left, rest is whitespace
- All items left-aligned on the same vertical lane

### Table of Contents (Index Panel)
- Left panel: Subtitle + "Table of contents" heading + body text at bottom
- Right panel (dark): "Content" header + list of items with page numbers right-aligned
- Items are vertically stacked with consistent row height
- Page numbers right-aligned within the panel

### Table of Contents (Multi-Section)
- Left panel: Subtitle + "Table of contents" heading
- Right area: 2×3 grid of section groups
- Each group: "01" + "Content" header + 5 bullet items
- Groups arranged in 2 columns, 3 rows

### Section Divider
- Number ("01") + section name, same line, top-left
- Display size (68-72px)
- Everything else is empty. The emptiness is the point.

---

## People / Bio Slides

### 3-Person Layout
- 3 equal columns
- Each: headshot image (top, square or 4:3), name below (24-26px), subtitle below name (24-26px, secondary color)
- Images aligned on same horizontal baseline
- Text centered below each image

### 4-Person Layout
- Same pattern, 4 columns, slightly smaller images

### 5-Person Layout
- Same pattern, 5 columns, compact

### People Slide Rules
1. All headshots the same aspect ratio and size within a slide
2. Names and subtitles aligned on the same baseline across all columns
3. No bios or body text. Just name + title. Keep it clean.
4. These slides also exist in "Card" variants where each column gets a title + body paragraph instead of name + subtitle (for capabilities or features rather than people)

---

## Quote Slides

### Full-Page Quote
- Large quote text filling the upper portion of the slide
- Quote size: 40-44px, regular weight
- Quote marks are part of the text (not decorative oversized marks)
- Text left-aligned, constrained to ~60% width

### Quote + Photo + Attribution
- Round or square photo (small, left side)
- Quote text right of photo
- Attribution below: Name / Title / Company (3 lines, 14px)

### Quote + Attribution (No Photo)
- Quote text large and centered
- Attribution centered below

### Quote Rules
1. Quotes are always in the same font as body text. No italic, no serif.
2. Attribution is always: Name, Title, Company on separate lines
3. No decorative quote marks. The quotation marks are inline with the text.

---

## Full-Bleed Slides

### Full-Bleed Image
- Single image covers the entire artboard
- No text overlay. Pure visual moment.
- Use sparingly: 1-2 per deck maximum

### Full Image + Text Overlay
- Background image covers the artboard
- Text panel overlaid (with slight dark gradient or semi-transparent background for legibility)
- Title + body + subtitle text in the overlay
- Overlay typically bottom-left or left-third of the slide

---

## Case Study / Feature Detail Slides

A family of layouts for presenting a project or feature with supporting imagery.

### Structure
- **Left third:** Text content (subtitle, title, body paragraph)
- **Right two-thirds:** Mixed image layout
  - Hero image (large) + 1-3 supporting thumbnails
  - OR 2 equal images stacked
  - OR 3 images in a row with titles below

### Variants by Image Count
- 1 hero + 0 supporting: simple text-left, image-right
- 1 hero + 2 supporting thumbnails: hero top-right, thumbnails bottom-right
- 2 equal images: stacked vertically in right panel
- 3 images with titles: 3 columns in right panel, each image + title + body

### Rules
1. Text panel width stays fixed regardless of image count
2. Body text in the text panel supports longer copy (2-3 paragraphs)
3. Supporting thumbnails are always smaller than the hero image
4. Image titles (when present) use the body text size, not section title

---

## Category Matrix

For content organized by multiple categories (competitive analysis, feature comparison, capability mapping).

### Structure
- Caption + section title + subtitle top-left (spanning full width or left portion)
- 2×3 or 3×2 grid of category blocks
- Each block: Category name (bold or primary text) + description + optional image
- Images appear in select cells, not all (creating visual variety)
- Body text below the grid for context

### Rules
1. Category names are the same size across all cells
2. Descriptions are secondary text color
3. Images in category cells are small (thumbnail size)
4. Not every cell needs an image. Mix text-only and image cells.

---

## Multi-Column Text (3, 4, 5 Columns)

For parallel content without images.

### 3-Column Text
- Caption + section title + subtitle header area
- 3 equal columns below
- Each column: title (24-26px) + body (16-18px)
- Columns separated by whitespace only (no dividers)

### 4-Column Text
- Same structure, 4 columns, narrower body text

### 5-Column Text
- Same structure, 5 columns, most compact

### Rules
1. Body text in narrow columns needs smaller size (16px) to avoid excessive line breaks
2. Titles within columns should be the same length across columns where possible
3. No divider lines between columns. Whitespace handles separation.

---

## Thank You / Contact Slide

### Structure
- "Thank you!" in display size, centered or left-aligned
- "Contact" label below
- Email and website in body text size
- Generous whitespace. Nothing else on the slide.

### Rules
1. Same footer as all other slides (Company/Date/Project)
2. No logos, no social media icons, no decorative elements
3. Contact info is text only, not hyperlinked visually

---

## Deck Composition Rules (TMS-Specific)

These supplement the sequencing rules in the base layouts.md:

1. **Every deck starts with a title slide and ends with a thank you slide.** Bookend structure.
2. **An agenda slide follows the title slide.** Establishes the deck structure immediately.
3. **Section dividers separate major content groups.** They use the same visual language as the agenda items (number + name).
4. **Image density should increase through the deck.** Start with text-heavy slides (context, strategy), progress to image-heavy slides (work, results, portfolio).
5. **Never put two image-grid slides back-to-back without a text slide between them.** The eye needs a rest.
6. **People slides belong in the second half.** Team intros come after the work speaks for itself.
7. **Quote slides work as transitions.** Place them between sections, not within a section.
8. **Full-bleed image slides are punctuation.** They signal a major shift. Use 1-2 per deck.
9. **Case study slides come in clusters of 2-4.** A single case study slide feels orphaned.
10. **The color variant is chosen once and used throughout.** Never mix light and dark variants in the same deck (unlike C&T Strategy which alternates dark/red/white backgrounds).
