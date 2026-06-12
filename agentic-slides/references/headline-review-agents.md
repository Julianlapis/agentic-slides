# Headline Review Agents

> **DEPRECATED 2026-05-11.** Superseded by `per-slide-clarity-gate.md`. The deck-level Blind Reader + Gap Analyzer caught some headline-narrative issues but missed the per-slide failure modes (clarity dilution, fidelity overclaim) that surfaced on a later pitch run. The per-slide gate operates one slide at a time, has tamper-proof file trails, and supersedes both agents below.
>
> Kept for archive. New agentic-slides runs should invoke the per-slide gate as their Phase 5 final check, not the agents documented here.
>
> **2026-05-29 — headline-specific discipline consolidated into [`headline-gate.md`](headline-gate.md).** The Blind Reader, Gap Analyzer, and Headline Transition Scoring below are absorbed there, alongside the cold-read and the label-vs-key-idea test, as one auto-firing gate. For any headline work, use `headline-gate.md`, not this file.

---

Two mandatory sub-agents that run during Phase 5 (Quality System) of every agentic-slides build. They run AFTER the four-pass quality system, as a dedicated headline-narrative gate.

---

## Agent 1: Headline Blind Reader

**Model: sonnet.** Structural test, not aesthetic judgment.

**Purpose:** Test whether the eyebrows + headlines alone tell the full story.

**IMPORTANT:** Include eyebrows (the small label text above each headline, e.g. "01 / BRAND STRATEGY", "THE KEY PROBLEM", "DESIGN PRINCIPLE 1"). Eyebrows provide wayfinding context that is critical to following the argument. A headline like "The morning run is the meeting that can't be moved" reads differently under "THE KEY INSIGHT" than it does under "PRODUCT STRATEGY." Always extract and include eyebrows alongside headlines.

**Prompt template:**

```
You are reading the eyebrows and headlines of a pitch deck with ZERO other context. You have not seen the brief, the spec, the body copy, or any supporting material. You only see the eyebrow labels and headlines.

Read these in order:

[INSERT ALL EYEBROWS + HEADLINES]

Now:
1. In 3-4 sentences, summarize what you think this deck is arguing.
2. List any points where you got confused or lost the thread.
3. Identify any headline where you couldn't tell what the slide was about from the headline alone.
4. Note any place where the argument jumps without a bridge.

Be honest. If you can't follow it, the headlines are failing.
```

**How to use the output:**
- If the blind reader's summary misses the core proposition, the headlines aren't landing it.
- If confusion points cluster in one section, that section needs headline rewrites.
- If a headline is opaque without body copy, it's doing description work, not argument work.

**Pass criteria:** The blind reader's summary must contain: (1) what the product is, (2) the core insight/positioning, (3) why it's different from competitors. If any of these three are missing, the headlines fail.

---

## Agent 2: Headline Gap Analyzer

**Model: haiku.** Mechanical comparison of list A against list B.

**Purpose:** Compare what the headlines communicate against what the source material says they need to communicate.

**Prompt template:**

```
You have two inputs:

INPUT 1 — THE SOURCE BRIEF (what the deck needs to argue):
[INSERT BRIEF OR OUTLINE CONTENT]

INPUT 2 — THE EYEBROWS + HEADLINES (what the deck actually says):
[INSERT ALL EYEBROWS + HEADLINES — eyebrows provide section context that changes how headlines read]

Your job:
1. Extract the 5-7 key arguments from the source brief that the deck MUST land.
2. For each argument, find the headline(s) that carry it.
3. Flag any argument that has NO headline carrying it.
4. Flag any headline that doesn't advance any of the key arguments (dead weight).
5. Score headline coverage: what percentage of the brief's arguments have a headline champion?

Output as a table:
| Brief Argument | Headline(s) That Carry It | Coverage |
|...

Then list: UNCOVERED (arguments with no headline) and ORPHANED (headlines advancing nothing from the brief).
```

**How to use the output:**
- UNCOVERED arguments need new headlines or existing headlines rewritten to carry them.
- ORPHANED headlines should be cut or repurposed.
- Coverage below 80% means the headline narrative has structural gaps.

---

## When to Run

These agents run during Phase 5, AFTER the standard four-pass quality system:

1. Layout Intelligence Agent
2. Design Quality Agent
3. Narrative Flow Agent
4. Copy Quality (Stop Slop) Pass
5. **Headline Blind Reader** ← NEW
6. **Headline Gap Analyzer** ← NEW

If either agent fails, the copy goes back for revision before the deck is presented to the user.

## Headline Transition Scoring
After writing all headlines, score every A→B transition (1-10): does B follow naturally from A? Shared language, logical progression, or emotional continuity all count. Below 6 on any transition = rewrite. The test: read headlines aloud in sequence. Any moment where you'd think "wait, how did we get here?" is broken.

**Technique:** Use callback language. If slide 4 names "the premium," slide 5 should reference "the premium" or "the gap." Shared nouns across adjacent headlines are the connective tissue.

## Unveiling vs Supporting Headlines
Slides that unveil a new concept must name that concept in the headline. The example drops to the body.

Two headline types:
1. **Unveiling slides** (introduce a new idea): headline NAMES the concept simply. Examples: "Own the morning, everywhere." / "The morning run is the meeting that can't be moved."
2. **Supporting slides** (back up a claim): headline explains WHY or HOW. Example: "Every competitor sells performance, and that's exactly why they can't sell belonging."

**Test:** After writing a headline, ask: "Does this name a new idea, or describe an example of one?" If it's an example, rewrite.

## Why These Exist

Added 2026-04-03 after a pitch deck build. The standard quality system scored headlines on pattern and rhythm but missed that the headline sequence didn't tell the full story on its own. A reader skimming just the headlines couldn't follow the argument from problem to solution. These agents catch that gap by testing headline narrative completeness from two angles: comprehension (blind reader) and coverage (gap analyzer).
