<p align="center">
  <img src="cover.png" alt="agentic-slides" width="100%">
</p>

# Agentic Slides

A Claude Code skill that builds production-quality presentation decks using AI agents.

Takes any source material — outlines, docs, transcripts, URLs — and produces polished decks with real design intelligence. Handles content distillation, layout planning, visual design, copy quality, and export.

## Canvas options

**Paper (default)** — the primary canvas. Builds decks by writing HTML incrementally to the Paper canvas, screenshots to verify, and exports pixel-perfect PDFs. Best for rapid iteration and solo workflows.

**Figma** — builds decks directly on the Figma canvas using your design system's components, variables, and auto-layout via the [Figma MCP server](https://www.figma.com/blog/the-figma-canvas-is-now-open-to-agents/) and its `use_figma` tool. Your team can collaborate on the output, modify text, swap tokens, and hand off to production. Best for team workflows and design system integration.

Specify which canvas when you invoke the skill. Paper is the default if you don't specify.

## What it does

- Builds slide decks from any source material
- Assigns layouts from a pattern library that matches content shape to visual structure
- Enforces a design system (palette, typography, spacing, structural rules)
- Runs a four-pass quality system with parallel scoring agents
- Self-healing loops: screenshots output, evaluates, iterates on mismatches
- Maintains a feedback log that gets smarter with every session

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI)

**For Paper (default):**
- [Paper](https://paper.design) desktop app with MCP enabled
- Python 3 with Pillow (`pip install Pillow`) for PDF export

**For Figma:**
- [Figma MCP server](https://www.figma.com/developers/mcp) configured in Claude Code

## Installation

```bash
# Clone this repo
git clone https://github.com/Julianlapis/agentic-slides.git

# Copy into Claude Code commands
cp -r agentic-slides/paper-slides/ ~/.claude/commands/paper-slides/
```

## Usage

### Build a deck in Paper (default)

```
/paper-slides Build a 15-slide strategy deck from this outline: [paste outline]
```

### Build a deck in Figma

```
/paper-slides Build a 15-slide strategy deck in Figma from this outline: [paste outline]
```

### Export to PDF (Paper only)

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
Constructs the deck on your chosen canvas:

- **Paper** — creates artboards, writes HTML incrementally (one visual group at a time), screenshots to verify every 2-3 slides.
- **Figma** — creates frames using `use_figma`, leveraging your design system's components, variables, and auto-layout. Screenshots and iterates via self-healing loops.

### Phase 5: Quality System
Four parallel agents score the deck:

1. **Layout Intelligence** — layout variety, rhythm, content-to-layout fit, density pacing
2. **Design Quality** — hierarchy, balance, typography, alignment, contrast (scored per slide, 50 max)
3. **Narrative Flow** — single-mindedness, redundancy, logical arc, earned payoff, specificity
4. **Copy Quality** — false agency, passive voice, vague declaratives, dramatic fragmentation

Any score below 35/50 triggers automatic fixes.

### Phase 6: Export
- **Paper** — screenshots each artboard at 2x, assembles with Pillow into a PDF.
- **Figma** — your deck is already in Figma. Share the file, export frames, or hand off to production.

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
