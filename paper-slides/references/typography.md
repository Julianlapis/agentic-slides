# Typography Rules for Paper Slides

## Line Break Balance

If body copy wraps to 2+ lines, the lines must be roughly equal length. A long first line with a 2-word orphan second line looks broken. Fix by adjusting `maxWidth` on the text element to force a more balanced reflow. Screenshot and verify after adjusting.

## Never Use System Fonts

Always set `fontFamily` explicitly. After duplicating nodes, fonts sometimes revert to `system-ui, sans-serif`. Verify with `get_computed_styles` and re-apply both `fontFamily` and any `fontVariationSettings` if they've been lost.

## Headlines Fill the Width

Headlines should use most of the available width. If a headline only takes up half the slide, it's too small. Scale up until it commands the space. Presentation headlines are the first thing the audience reads.

## Body Copy is Readable

Body text: 18-20px for presentations. 16px is the absolute minimum. What looks fine on a monitor looks tiny on a projector.

## Weight Contrast Creates Hierarchy

The gap between heaviest and lightest weights should be dramatic. Pair 900-weight headlines with 300-weight body text. This contrast creates hierarchy without needing boxes, lines, or color differences.

## Emphasis Lines Need Distinct Styling

Body text that serves as a punchline or closing statement should be bold (fontWeight: 700) or use the accent color to visually separate it from regular body copy.

## Card Number Styling

Card/column numbers (01, 02, 03) should be upright bold, not italic. Card numbers act as anchors and should feel stable.

## Font Troubleshooting

When fonts look wrong after building or duplicating:
1. Check computed styles with `get_computed_styles` — look for `system-ui` or missing variation settings
2. Re-apply with `update_styles`: set both `fontFamily` and `fontVariationSettings`
3. For variable fonts, ensure both `wdth` and `wght` axes are specified where needed

## Typographic Units

- Use "px" for font sizes
- Use "em" for letter spacing
- Use "px" or relative values for line height (avoid subpixel sizes)

## Choosing a Font

Use `get_font_family_info` before writing any styles. Great presentation fonts have:
- Wide weight range (300-900 minimum)
- Variable font support preferred
- A distinctive display personality

Every deck deserves its own typographic identity. Don't repeat the same font across different decks.
