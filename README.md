<p align="center">
  <img src="cover.png" alt="agentic-slides" width="100%">
</p>

# Agentic Slides

A Claude Code skill that builds production-quality presentation decks using AI agents. Works with [Paper](https://paper.design) and [Figma](https://figma.com).

Takes any source material — outlines, docs, transcripts, URLs — and produces polished decks with real design intelligence. Handles content distillation, layout planning, visual design, copy quality, and export.

## What it does

- Builds slide decks from any source material
- Assigns layouts from a pattern library that matches content shape to visual structure
- Enforces a design system (palette, typography, spacing, structural rules)
- Runs a four-pass quality system with parallel scoring agents
- Exports to PDF (via Paper) or editable Figma files (via Desktop Bridge MCP)
- Maintains a feedback log that gets smarter with every session

## Design tools

**Paper** — primary canvas for building decks. Writes HTML incrementally, screenshots to verify, exports pixel-perfect PDFs.

**Figma** — exports Paper decks into editable Figma frames with real text layers, correct fonts, proper colors, and auto-layout. Your team can collaborate on the Figma file and hand off to production.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI)
- [Paper](https://paper.design) desktop app with MCP enabled
- Python 3 with Pillow (`pip install Pillow`) for PDF export
- Figma + [Figma Console MCP](https://www.npmjs.com/package/figma-console-mcp) (optional, for Figma export)

## Installation

```bash
# Clone this repo
git clone https://github.com/Julianlapis/agentic-slides.git

# Copy into Claude Code commands
cp -r agentic-slides/paper-slides/ ~/.claude/commands/paper-slides/
```

Your directory structure should look like:

```
~/.claude/commands/
  paper-slides/
    SKILL.md                   # Main skill file
    feedback-log.md            # Learning log (grows with use)
    references/
      anti-patterns.md         # Common mistakes to avoid
      default-design-system.md # Fallback design system
      figma-export.md          # Figma export pipeline
      layouts.md               # Layout pattern library
      pdf-export.md            # PDF export pipeline
      quality-system.md        # Four-pass quality scoring
      typography.md            # Typography rules
```

## Usage

### Build a new deck

```
/paper-slides Build a 15-slide strategy deck from this outline: [paste outline]
```

### Export to Figma

```
/paper-slides Export this deck to Figma
```

### Export to PDF

```
/paper-slides Export the current deck to PDF
```

### Run quality review

```
/paper-slides Run the quality system on this deck
```

## How it works

### Phase 1: Content Structuring
Takes whatever you provide and produces structured markdown. One slide per section, with eyebrow, headline, body, and layout fields.

### Phase 2: Layout Planning
Reads the full content, understands the narrative arc, and assigns a layout to every slide from the pattern library. Checks for rhythm, variety, density pacing, and section transitions.

### Phase 3: Design Brief
Reads the design system file and extracts palette, typography, spacing, and structural rules.

### Phase 4: Build
Creates artboards in Paper, writes HTML incrementally (one visual group at a time), and screenshots to verify every 2-3 slides.

### Phase 5: Quality System
Four parallel agents score the deck:

1. **Layout Intelligence** — layout variety, rhythm, content-to-layout fit, density pacing
2. **Design Quality** — hierarchy, balance, typography, alignment, contrast (scored per slide, 50 max)
3. **Narrative Flow** — single-mindedness, redundancy, logical arc, earned payoff, specificity
4. **Copy Quality** — false agency, passive voice, vague declaratives, dramatic fragmentation

Any score below 35/50 triggers automatic fixes.

### Phase 6: Export
**PDF** — screenshots each artboard at 2x via Paper's MCP API, assembles with Pillow.
**Figma** — writes editable frames via Desktop Bridge MCP with real text layers, fonts, colors, and auto-layout.

## Design Systems

Ships with example design systems you can reference or extend:

- **default-design-system.md** — Minimal monochromatic system. Works for any deck.
- **design-system-ct-strategy.md** — Strategy deck system with serif/sans pairing and red accent.
- **design-system-tms-core.md** — Product deck system.

Create your own by following the same format.

## Feedback Log

The feedback log is read at the start of every invocation. It contains binding rules from past sessions. As you correct the skill's behavior, those corrections get appended automatically. It gets better every time you use it.

## License

MIT
