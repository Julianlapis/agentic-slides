---
name: reference-builder
description: Build exhaustive, machine-readable reference documents from external sources. Point it at games, products, brands, design systems, artists, or movements — it researches everything and produces structured reference folders. Works standalone. Feeds into /agentic-slides or any other workflow. Trigger when asked to "build references", "research visual inspiration", "compile a mood board", "gather audio references", or "create a reference doc".
metadata:
  trigger: Building reference documents, visual research, audio research, design system analysis, inspiration gathering, mood board compilation
  author: Julian Alexander
---

# /reference-builder

Build exhaustive, machine-readable reference documents by dispatching parallel research agents across the internet.

## What This Does

You give it subjects (games, brands, products, artists, movements, design systems). It asks what you care about, then launches one research agent per subject in parallel. Each agent crawls the web and produces a structured markdown reference document with links to source material.

The output is a folder of `.md` files designed to be consumed by other agents — /agentic-slides, or any workflow that needs grounded creative/technical references.

## Process

### Step 1: Clarify Scope

Use `AskUserQuestion` to establish three things:

**1a. Subjects** — What are we researching? (The user may have already listed them.)

**1b. Focus lenses** — Which lenses apply to this research? Present these options and let the user select multiple:

| Lens | What it covers |
|------|---------------|
| **Visual Art** | Color palettes (hex values), pixel art / illustration style, character design, environment art, lighting, UI/HUD, visual effects, compositional philosophy |
| **Motion / Animation** | Character animation (frame counts, easing), environmental animation, camera behavior, screen transitions, combat feel, parallax |
| **Audio / Music** | Soundtrack analysis (tracks, instruments, synthesis), sound design, adaptive audio, notable compositions, audio aesthetic |
| **Energy / Mood** | Emotional tone, pacing, atmosphere, tension/release patterns, how the work *feels* — the ineffable quality |
| **Design System** | Typography, spacing systems, component patterns, layout grids, token systems, interaction patterns |
| **Brand / Identity** | Logo, color identity, voice/tone, visual language, positioning, how the brand manifests across touchpoints |
| **Narrative / Storytelling** | How story is conveyed (text, visual, environmental, wordless), narrative structure, worldbuilding |
| **Technical** | Engine, rendering approach, resolution, performance tricks, development tools, documented technical decisions |
| **Development / Process** | Dev timeline, team size, tools used, postmortems, GDC talks, documented decisions and pivots |
| **Influences / Context** | Stated influences, genre lineage, cultural context, comparisons to adjacent work |

The user can also define custom lenses not in this list.

**1c. Output location** — Where should the reference folder go? Default: `docs/references/` in the current project. If no project context, ask.

### Step 2: Generate Agent Prompts

For each subject, construct a research agent prompt that:

1. Names the subject with full context (creator, year, medium)
2. Includes ONLY the selected focus lenses as research sections
3. For each lens, includes specific sub-questions calibrated to the subject type:
   - **Games** get sprite dimensions, palette hex values, frame counts, track listings
   - **Brands** get logo specs, brand guidelines analysis, campaign examples
   - **Artists** get technique breakdowns, tool chains, stylistic evolution
   - **Design systems** get token values, component inventories, spacing scales
   - **Movements/genres** get defining characteristics, key works, evolution timeline
4. Instructs the agent to include URLs to every reference (images, video, audio, interviews, talks)
5. Instructs the agent to write the output to the designated file path
6. Instructs the agent to format as structured markdown with clear sections and bullet points

### Step 3: Launch Agents in Parallel

Dispatch all research agents simultaneously using the `Agent` tool with `run_in_background: true`.

Rules:
- **One agent per subject.** Never combine subjects.
- **All agents launch in a single message.** Maximize parallelism.
- **Cap at 10 concurrent agents.** If more than 10 subjects, batch in waves.
- Each agent gets the full prompt constructed in Step 2 — they work autonomously.

Tell the user what you launched and that you'll notify them as results come in.

### Step 4: Collect and Report

As agents complete, briefly notify the user which ones finished. When all are done, present a summary table:

| File | Key Highlights |
|------|---------------|
| `subject.md` | 2-3 sentence summary of what was captured |

### Step 5: Coherence Check

After all agents finish, ask the user:

> "Do all these references paint a cohesive picture for your project, or should any be removed/flagged as outliers?"

If the user identifies outliers:
- Remove the file if they say to drop it
- Add a frontmatter tag `role: philosophy-only` or `role: contrast-reference` if they want to keep it but flag it as non-primary

### Step 6: Generate Index (Optional)

If the user wants it, generate a `_index.md` file in the reference folder that:
- Lists all reference docs with one-line descriptions
- Notes which focus lenses each doc covers
- Flags any docs marked as philosophy-only or contrast-references
- Provides a "common threads" section summarizing what unites the reference set

---

## Agent Prompt Template

Use this structure when constructing each agent's prompt. Adapt the specific questions per lens to the subject type.

```
You are a [subject-type] researcher. Your job is to compile an exhaustive
reference document for **[Subject Name]** ([creator], [year]).

Use WebSearch and WebFetch to find and document everything you can about:

## [Lens 1 Name]
- [Specific question 1]
- [Specific question 2]
- [Specific question 3]
...

## [Lens 2 Name]
- [Specific question 1]
...

[Continue for all selected lenses]

## Key References
Compile all URLs found during research, organized by type:
- Articles & interviews
- Video (gameplay, talks, postmortems)
- Audio (soundtracks, sound design breakdowns)
- Visual (sprite sheets, screenshots, art breakdowns)
- Technical (source code, engine docs, GDC slides)

Search extensively. Include URLs to everything. This is a production
reference document that other AI agents will consume — be thorough
and structured.

Write the complete document to: [output_path]
Format as markdown with clear sections and bullet points.
```

---

## Lens-Specific Question Banks

When building agent prompts, pull from these per-lens question sets. Don't use all of them — select the ones most relevant to the subject type.

### Visual Art
- What is the rendering style? (pixel art, vector, 3D, mixed)
- What resolution / pixel density?
- Document specific color palettes with hex values per area/zone/mood
- Character design: proportions, silhouette philosophy, animation-readiness
- Environment art: layering, parallax, foreground/background separation
- Lighting approach: baked vs dynamic, glow effects, time-of-day shifts
- UI/HUD: minimal vs dense, font choices, how information is presented
- Visual effects: particles, weather, water, screen transitions, post-processing
- Compositional philosophy: framing, negative space, focal points

### Motion / Animation
- Character animation: frame counts, easing curves, squash-and-stretch
- Environmental animation: foliage, water, clouds, ambient creatures
- Camera behavior: fixed vs scrolling, zoom, transitions between areas
- Screen transitions: wipes, fades, dissolves, how spaces connect
- Combat feel: screen shake, hit-stop, impact particles, telegraph patterns
- Parallax scrolling: layer counts, speed ratios, depth illusion

### Audio / Music
- Soundtrack: composer, track count, track names, total runtime
- Instruments and synthesis: analog vs digital, specific synths/DAWs named
- Audio aesthetic: genre blend, how it serves the experience
- Sound design: key sounds (footsteps, impacts, UI), recording techniques
- Adaptive audio: how music responds to gameplay state, location, intensity
- Notable tracks: describe 3-5 key compositions (mood, instruments, structure)

### Energy / Mood
- What emotion does this evoke on first contact?
- Pacing: fast/slow, how tension and release are managed
- Atmosphere: dense/sparse, warm/cold, intimate/vast
- The "feel": what makes this experience distinctive at a gut level
- Contrast patterns: where does it shift energy? (calm → intense, light → dark)

### Design System
- Typography: font families, scale, weight usage, hierarchy
- Color: primary/secondary/accent tokens, semantic colors, dark mode
- Spacing: base unit, scale progression, consistent patterns
- Components: key UI components, their variants, interaction states
- Layout: grid system, breakpoints, container patterns
- Motion tokens: easing curves, duration scale, animation principles

### Brand / Identity
- Logo: construction, clear space, usage rules, variations
- Color identity: primary brand colors with hex, usage ratios
- Voice/tone: how the brand speaks, vocabulary, personality
- Visual language: photography style, illustration style, iconography
- Positioning: what space does this brand own? What does it reject?

### Narrative / Storytelling
- How is story conveyed? (text, cutscenes, environmental, wordless)
- Narrative structure: linear, branching, emergent
- Worldbuilding: how the world is established and revealed
- Character expression: how characters communicate emotion
- Player/audience agency: how much the audience shapes the narrative

### Technical
- Engine/framework and version
- Native resolution, scaling approach, target framerate
- Rendering pipeline: notable techniques or optimizations
- Asset pipeline: how art/audio assets are produced and integrated
- Documented performance tricks or clever technical shortcuts

### Development / Process
- Timeline: conception to release, notable milestones
- Team: size, key roles, notable contributors
- Tools: software, hardware, custom tooling
- Postmortems: GDC talks, blog posts, interviews about the process
- Pivots: major direction changes and why they happened

### Influences / Context
- Stated influences by creators
- Genre lineage: what tradition does this sit in
- Cultural context: what was happening when this was made
- Adjacent works: what else was being made in the same space
- How influences manifest: specific ways source material shows up

---

## File Naming

Slugify the subject name for the filename:
- "Hyper Light Drifter" → `hyper-light-drifter.md`
- "Apple Design System" → `apple-design-system.md`
- "Studio Ghibli" → `studio-ghibli.md`
- "Bauhaus Movement" → `bauhaus-movement.md`

---

## Quality Bar

Each reference document should:
- Be **300+ lines** minimum for a subject with 3+ lenses
- Include **20+ external URLs** to source material
- Have **specific details** (hex colors, frame counts, track names) — not vague summaries
- Be **structured for machine consumption** — consistent headers, bullet points, tables
- Include a **Key References** section at the end with all URLs organized by type

If an agent returns a thin document, flag it and offer to re-run with more specific search terms.

---

## Integration Points

This skill is standalone, but it pairs directly with `/agentic-slides`:

1. Run `/reference-builder` on a brand, deck, or design system with the **Design System** and **Brand / Identity** lenses.
2. The output is a structured design-system markdown file.
3. Hand that file to `/agentic-slides` as the design system input — it will build decks in that visual language.

When any other skill or workflow needs grounded reference material, point it at the folder this skill generates.
