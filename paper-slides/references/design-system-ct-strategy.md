# Code & Theory Strategy Deck Design System

This is the canonical design system for C&T strategy presentation decks, extracted from the UBS Brazil pitch and UBS Personas Final Delivery. Every rule here is derived from what shipped. Paper MCP should treat this as binding when building strategy decks.

---

## Canvas

- **Artboard size:** 1456 x 816px (16:9, standard presentation)
- **Content safe zone:** 60px padding on all sides. Footer elements live at y: 770-790.
- **Footer pattern:** "CODE AND THEORY" left-aligned, all caps, letterspaced, 11-12px, muted color. Page number right-aligned, same size, same muted color. Both sit at the bottom margin line. The footer is a constant. It appears on every slide except the title.

---

## Color Palette

### Primary Colors

| Role | Hex | Usage |
|------|-----|-------|
| **UBS Red** | `#CC0000` or `#C80000` | Accent color. Section eyebrows, emphasis text, horizontal rules, bullet dashes, numbered labels. The only saturated color in the system. |
| **Near-Black** | `#1A1A1A` | Dark slide backgrounds, title slides. NOT pure `#000000`. |
| **White** | `#FFFFFF` | Text on dark/red backgrounds. Body text on white slides uses near-black, not white. |
| **Off-White / Warm Gray** | `#F5F5F0` to `#FAFAF8` | Light slide backgrounds. Slightly warm, never blue-tinted. |

### Text Colors by Background

| Background | Headline | Body | Muted/Footer |
|------------|----------|------|-------------|
| Red (`#CC0000`) | `#FFFFFF` | `#FFFFFF` at ~90% opacity or `#FFE0E0` | `rgba(255,255,255,0.5)` |
| Near-Black (`#1A1A1A`) | `#FFFFFF` | `#FFFFFF` at ~85% opacity | `rgba(255,255,255,0.4)` |
| White/Off-White | `#1A1A1A` | `#333333` or `#3A3A3A` | `#999999` or `#AAAAAA` |

### Hard Nos: Color

- **No gradients on backgrounds.** Solid fills only. The one exception: photographic backgrounds with a dark gradient overlay for text legibility.
- **No blue, no purple, no green, no orange anywhere in the system.** Zero. The palette is monochromatic (black/white/gray) plus one red.
- **No tinted reds.** Don't soften the red to pink, coral, or salmon. It's `#CC0000`, full stop.
- **No colored text on colored backgrounds** except white-on-red and white-on-black. Red text only appears on white/light backgrounds.
- **Red is never a background AND text color on the same slide.** If the slide background is red, all text is white. If text is red, the background is white.

---

## Typography

### Font Selection

The decks use a **serif display font** for headlines and a **clean sans-serif** for body, labels, and metadata.

- **Headlines:** A high-contrast serif with classical proportions. The specific font varies per engagement, but it MUST be:
  - High stroke contrast (thick/thin variation)
  - Old-style or transitional classification
  - Available in regular and italic weights minimum
  - Example fonts that match: Cormorant Garamond, Playfair Display, Noto Serif Display, Freight Display, or the actual UBS serif (closest match: a Didone-family serif)
- **Body / Labels / Footer:** A geometric or humanist sans-serif. Clean, professional, no personality. Examples: Inter, Helvetica Neue, Suisse Int'l, Aktiv Grotesk.

### Type Scale

| Element | Size | Weight | Style | Letter Spacing |
|---------|------|--------|-------|---------------|
| **Title slide headline** | 72-96px | Regular (400) | Normal | -0.02em |
| **Section divider headline** | 56-72px | Regular (400) | Normal | -0.02em |
| **Slide headline** | 40-52px | Regular (400) | Normal | -0.01em |
| **Sub-headline** | 28-36px | Regular or Bold (700) | Normal | 0 |
| **Body text** | 18-22px | Regular (400) | Normal | 0.01em |
| **Eyebrow / Section label** | 11-14px | Bold (700) | Normal | 0.12-0.18em |
| **Emphasis italic** | 24-32px | Regular (400) | Italic | 0 |
| **Big stat number** | 48-64px | Regular (400) | Normal | -0.02em |
| **Stat label** | 11-13px | Bold (700) | Normal | 0.12em |
| **Footer** | 11-12px | Regular or Medium (500) | Normal | 0.15em |
| **Quote text** | 20-24px | Regular (400) | Normal | 0 |
| **Source attribution** | 13-14px | Regular (400) | Normal | 0 |

### Typography Rules

1. **Headlines are serif. Always.** The serif headline is the single strongest visual signature in this system. Switching to sans-serif for headlines destroys the identity.

2. **Eyebrows are all-caps sans-serif, always.** Letterspaced at 0.12-0.18em. Bold weight. In red when on white backgrounds, in white when on dark/red backgrounds.

3. **Body text is sans-serif. Always.** Never set body copy in the serif font. The contrast between serif headlines and sans body IS the hierarchy.

4. **Italic serif for closing statements and editorial asides.** The decks use an italic version of the headline serif for bottom-of-slide punchlines (e.g., "The gap isn't brand strength........it's relevance." and "We can be in-market within 4 weeks of kickoff."). This italic is always lighter in opacity or color than the headline, creating a whisper effect.

5. **The ellipsis-bridge pattern.** Both decks use a distinctive pattern: a phrase, followed by 4-8 dots (not a standard ellipsis, but a deliberate string of periods), followed by an italic completion in red. Example: "The gap isn't credibility...............it's perception." This is a signature move. Use it once per deck maximum, always as a closing beat on a slide.

6. **Headline line breaks are intentional.** Headlines break at semantic boundaries, not wherever the text wraps. "Knowing the / New Client" breaks after "the" because the emphasis lands on "New Client." Always set `maxWidth` to force these breaks deliberately.

7. **No bold body text unless it's a label.** Body paragraphs are regular weight. Bold is reserved for section labels, card titles, and emphasis within structured content (not within paragraphs).

### Hard Nos: Typography

- **No all-caps headlines.** Headlines are mixed case. Only eyebrows/labels are all-caps.
- **No script or decorative fonts anywhere.**
- **No more than 2 font families per deck.** One serif, one sans. Period.
- **No underlines for emphasis.** The only underline in the system is the decorative underline on "The Question This Raises" which functions as a section divider, not emphasis.
- **No centered body text.** Body text is always left-aligned. Headlines can be left-aligned or centered depending on layout. Statement headlines center. Content headlines left-align.
- **No justified text anywhere.**

---

## Layout Patterns (Strategy Deck Specific)

These extend the base layout types in `layouts.md` with strategy-deck-specific patterns observed across both UBS decks.

### L1: Title Slide (Dark)

Full dark background (`#1A1A1A`). Headline bottom-left, large (72-96px). Subtitle or project label above headline in smaller text. "Code and Theory" and year bottom-right, small muted text. Massive negative space above the headline. The emptiness signals confidence.

**Key rule:** The headline should occupy only the bottom 30-35% of the slide. The top 65% is intentionally empty.

### L2: Red Statement Slide

Full red background (`#CC0000`). Eyebrow top-left. Headline bottom-left, white, large (48-72px). Optional body text below headline in two columns. Thin white horizontal rule separating headline from body. Page number and footer bottom-right.

**Key rule:** Content gravity is always bottom-left on red slides. Never center content on a red background.

### L3: Red + Right Column Data

Full red background. Eyebrow top-left. Headline left side (40-50%). Right side has structured data: labeled pairs with bold all-caps labels in white, followed by supporting text. A thin horizontal rule separates each labeled pair.

### L4: White Content Slide

White or off-white background. Red eyebrow top-left. Headline in black serif, left-aligned. Body content below in one or two columns. Thin black or red horizontal rule between headline and body. Stats or key figures displayed as large serif numbers with all-caps sans labels below.

### L5: Split Slide (Red Left / White Right)

Vertical split at ~48/52. Left half: red background, headline in white serif, bottom-left positioned. Right half: white background, numbered content blocks with bold sans-serif labels in red and body text in black.

**Key rule:** The left half is always the emotional/statement half. The right half is always the structured/evidence half.

### L6: Full-Bleed Photo

Full-bleed photograph as background. Dark gradient overlay from bottom (transparent to 70% black). Text sits on the gradient in the bottom third. Headline white serif, large. Optional italic subtext to the right.

### L7: White with Numbered Columns (The Methodology Slide)

White background. Large headline at top. Below: 3-5 equal columns, each with:
- A large serif number (in light gray or red): "01", "02", etc.
- A thin horizontal rule in red
- A bold all-caps sans label in red
- Body text in regular sans, dark gray

**Key rule:** Column numbers use the serif font, not sans. Numbers should be slightly lighter than full black to create depth. The red rules and labels create horizontal rhythm across the columns.

### L8: Centered Question Slide

White background. One centered question or provocation in large serif, occupying the middle 60% of the slide. Red text for the key phrase. Eyebrow top-left. Footer bottom. Everything else is whitespace.

**Key rule:** Centered text only works when the slide has ONE idea and no supporting body text. If you're adding body text, switch to a left-heavy layout.

### L9: Two-Panel Side by Side

Two equal panels, each with its own background color. Commonly: red left + white right, or dark left + white right. Each panel has its own eyebrow, headline, body, and supporting bullets. Thin horizontal rules separate headline from body within each panel.

---

## Structural Elements

### Horizontal Rules

The thin horizontal rule is the primary structural element. It replaces cards, boxes, and containers.

- **Width:** Full content width or column width
- **Height:** 1-2px
- **Color:** Matches the primary text color on that background (white on red/dark, black on white, red on white for accent)
- **Placement:** Below headlines to separate from body text. Above footer to close content. Between labeled pairs in data slides.

### Hard Nos: Structural

- **No cards with backgrounds.** Content sits directly on the surface. No rounded rectangles, no card shadows, no card borders. The horizontal rule does the job of separating content.
- **No boxes around stats.** Numbers stand alone with their label beneath them.
- **No icons.** Zero. The system uses typography and color exclusively. No lucide icons, no emoji, no pictograms.
- **No borders on anything except horizontal rules.** No bordered sections, no outlined buttons, no framed images.
- **No drop shadows anywhere.**
- **No rounded corners on any element** (except photo overlays which use 0px radius, i.e., sharp).

### Bullet Style

Bullets use a **red em-dash** (a short horizontal line in `#CC0000`), not circles or squares. On red/dark backgrounds, the dash is white. The dash is followed by the text with no indent beyond the dash width.

```
Format:  [red dash] [space] [text]
NOT:     [bullet point] [text]
NOT:     [number]. [text]
```

For numbered items in methodology/process slides, use serif numbers ("1." "2." "3.") with a period, not parentheses or circles.

### Vertical Left-Border (Quote Indicator)

Quotes and highlighted callouts use a 3-4px vertical red bar on the left edge. The bar spans the height of the text block. Text is indented 16-20px from the bar.

---

## Slide Sequencing Rules (Strategy Decks)

1. **Open on dark.** Title slide is always `#1A1A1A` background. Sets the tone.
2. **Red slides come in clusters of 2-3, then break.** Don't alternate red/white/red/white. Group red slides for narrative sections, then return to white for evidence/methodology.
3. **The first red slide after white is always a statement slide.** It marks a section transition. Big text, no body copy.
4. **Methodology/framework slides are always white.** The structured, numbered-column content needs the legibility of white backgrounds.
5. **Photo slides appear 1-2 times per deck maximum.** They mark major transitions (e.g., moving from context to execution).
6. **Close on either red or dark.** Never close on white. The final slide should feel like a period, not a question mark.
7. **Red slides never exceed 4 in a row.** After 4 red slides, the eye fatigues. Break with white or photo.
8. **Stats/numbers slides are always white.** Large numbers need contrast against a clean background.

### Background Rhythm for a 15-20 Slide Deck

```
DARK (title)
RED RED RED (section: problem/context)
WHITE WHITE (evidence/methodology)
RED (section transition statement)
WHITE WHITE WHITE (framework/methodology detail)
RED RED (section: synthesis/opportunity)
WHITE (final methodology/framework)
RED or DARK (closing)
```

---

## Photographic Treatment

When photos are used:

- **Full-bleed only.** No photos in partial frames or floating in whitespace.
- **Dark overlay required for text legibility.** Use a linear gradient from bottom: `rgba(0,0,0,0.7)` to `transparent`, covering the bottom 40-50% of the image.
- **Photos are cinematic, not stock.** Aerial landscapes, architectural details, atmospheric city shots. Never posed business people at a conference table.
- **One photo per slide maximum.**
- **No photo grids in strategy decks.** Photo grids belong in case study decks, not strategy decks.

---

## The Italic Closing Pattern

Both decks use a specific closing device on key slides: an italic serif line at the bottom of the slide that reads as an editorial aside, a whispered conclusion. This line is:

- Set in the serif font, italic weight
- Smaller than the headline (24-32px)
- Lighter opacity or a muted color compared to surrounding text
- Positioned at the bottom of the content area, above the footer
- Often preceded by a thin horizontal rule

Examples from the decks:
- *"Adapted for Brazilian wealth dynamics, cultural context, and the specific realities of your post-acquisition client base."*
- *"We can be in-market within 4 weeks of kickoff."*
- *"Before a new client ever meets their advisor, they should already feel like UBS knows them."*

**Use once every 3-4 slides.** If every slide has an italic closer, it loses its punch.

---

## Stat/Metric Display

When presenting numbers:

- **Number:** Large serif, 48-64px, red on white backgrounds, white on dark/red backgrounds
- **Label:** All-caps sans-serif, 11-13px, letterspaced 0.12em, placed directly below the number with 8px gap
- **Arrangement:** 3 stats in a row, equal columns, separated by vertical whitespace (no divider lines between them)
- **Alignment:** Left-aligned within their column, not centered

Example layout:
```
10                  8                   15
AI-NATIVE PERSONAS  WEALTH SEGMENTS    PRIORITY DMAS
```

---

## Common Failure Points (Things That Will Break the System)

### 1. Making the serif headline too small
The headline should command the slide. If it doesn't feel oversized relative to everything else, it's too small. The scale contrast between headline and body should be at least 2.5:1.

### 2. Using red too timidly
Red is either the full background or it's the accent text color. Nothing in between. Don't use red as a tint, a border color, or a subtle highlight. It's a punch, not a whisper.

### 3. Centering everything
The default alignment is left. Centering is reserved for statement slides (one line, one idea, nothing else) and the centered question pattern. If you're centering body text alongside a centered headline, you've gone wrong.

### 4. Adding visual elements to fill space
The emptiness is intentional. If a slide feels sparse, that's correct. Do NOT add decorative lines, background shapes, or filler text to "balance" the composition. The whitespace (or redspace) IS the balance.

### 5. Mixing serif into body text
The serif is for headlines and closing italics only. The moment serif appears in a paragraph or bullet list, the hierarchy collapses.

### 6. Forgetting the eyebrow
Every content slide (not title, not statement) needs an eyebrow label top-left. It orients the reader in the deck structure. Missing eyebrows make the deck feel like a collection of disconnected slides instead of a structured argument.

### 7. Making the footer too prominent
The footer is meant to be nearly invisible. If it's competing with body text for attention, it's too large, too dark, or too close to the content.

### 8. Inconsistent red
If you define red as `#CC0000`, every red element uses that exact value. Don't shift to `#E00000` on one slide and `#B00000` on another. One red, everywhere.

### 9. Using the ellipsis-bridge pattern more than once
The "phrase.........italic red completion" pattern is a signature move. Once per deck. Using it twice dilutes the effect.

### 10. Photo slides without sufficient overlay
If text sits on a photo and you can't read it at a glance, the overlay isn't dark enough. Better to over-darken than to have illegible text.

---

## Slide Copy Voice (Strategy Deck Specific)

This supplements the Stop Slop pass with strategy-deck-specific guidance:

- **Headlines are declarations, not descriptions.** "Acquired clients aren't new prospects. They're skeptics with options." beats "Understanding the Post-Acquisition Client Mindset."
- **Body text is evidence, not explanation.** Don't restate the headline in different words. Add new information.
- **Eyebrows are wayfinding, not marketing.** "THE MARKET MOMENT" not "WHY THIS MATTERS NOW."
- **Stats need context, not just numbers.** "10 AI-native personas" tells you what 10 means. "10" alone doesn't.
- **Italic closers earn their drama.** They work because the rest of the slide is restrained. If the body text is already dramatic, the italic closer has nowhere to go.

---

## Quick Reference: Slide Anatomy

```
┌──────────────────────────────────────────────┐
│ EYEBROW (red, all-caps, 12px, letterspaced)  │
│                                              │
│                                              │
│                                              │
│                                              │
│ Headline in Large                            │
│ Serif Font (40-52px)                         │
│ ──────────────────── (thin horizontal rule)  │
│                                              │
│ Body text in sans-serif,   │ Right column    │
│ 18-20px, regular weight.   │ with supporting │
│                             │ structured data │
│                                              │
│ CODE AND THEORY                          07  │
└──────────────────────────────────────────────┘
```

```
┌──────────────────────────────────────────────┐
│ ████████████████████████████████████████████ │
│ ██ EYEBROW (white, all-caps) ██████████████ │
│ ████████████████████████████████████████████ │
│ ████████████████████████████████████████████ │
│ ████████████████████████████████████████████ │
│ ██ Headline in White ██████████████████████ │
│ ██ Serif Font ████████████████████████████ │
│ ██ ──────────── ██████████████████████████ │
│ ██ Body text left █████ Body text right ██ │
│ ████████████████████████████████████████████ │
│ ██ CODE AND THEORY ████████████████ 04 ███ │
└──────────────────────────────────────────────┘
(Red background: #CC0000, all text white)
```
