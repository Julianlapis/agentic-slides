# Slide IA & Importance Ranking: Cut Whole, Never Blandify

The default AI failure mode when asked to compress a deck is to *summarize everything* — shave words off every element until the whole thing is shorter and uniformly blander. That flattens the thinking into slop. It is the single worst recurring tendency on any compression task, and it must be actively resisted.

This reference is the **above-the-slide** companion to `copy-compression.md`. Copy-compression operates at the line altitude (select the sharpest line inside one element). This operates at the section / slide / element altitudes (cut whole pieces by rank). They stack into one framework, zoomed.

The core move: assign every piece of the deck an explicit importance rank, then compress by **subtracting whole units**, never by **diluting all units**.

## The goal: let P1 do the work (this is always on)

Ranking is not only for when you're over budget. The standing goal of every slide is to **minimize P2 and P3 so the P1 carries the slide on its own.** Support and ornament are not neutral — they are *waste*. Every P2/P3 element is one more thing the audience has to process before the point lands, so each one makes the slide slower and harder to understand. A slide carrying only its P1 is structurally stronger and clearer than the same slide padded out with P1 + P2 + P3 — budget or no budget.

So compression is not a special event a deadline triggers; it is the **default discipline of authoring**. Budget pressure just forces the cut you should have wanted anyway. Two things to strip toward P1 on every slide, both of them pure waste:

1. **Over-support** — P2/P3 that isn't load-bearing. Cut toward the spine.
2. **Redundancy of every kind** — the same point made twice (in words, or once in words and once in the visual). Covered in the diagnostic below; both forms drag the slide and add zero argument.

Rank to find P1, then strip toward it.

## The spine principle (what "important" means)

Importance stays a **judgment** — this framework does not compute it. What it does is make the judgment *defensible*: every element has to justify itself against the argument, not against taste or how much work it was to make. The unit of that judgment is an element's **distance from the spine**.

The spine is the project's **strategy atom** — the `differentiator → positioning → activation` chain, defined canonically in `~/Projects/studio-v2/plugins/strategy/references/spine.md`. It is named *per project*, never hardcoded here. Name the spine before ranking anything; every element either advances a link, proves one, or decorates around it.

*(Illustration — one pitch deck's spine: founding science → a contrarian investment thesis → the brand architecture. This is an example of the shape, not a definition baked into this reference.)*

> **Wiring note (spine consolidation 2026-06-01):** these IA files are read as text into context — there is no parameter slot. How the *current* project's spine reaches this file at runtime (pre-processing substitution vs. a second verifier-manifest read of `spine.md`) is the open mechanism decision deferred to the spine-wiring phase. Until then, name the spine inline before ranking.

If you can't say which axiom an element serves, that is the rank signal: it's ornament.

## The three ranks

Tag with the machine code; think in the human word.

| Rank | Tag | What it is | Test |
|---|---|---|---|
| **Spine** | `P1` | Advances a spine axiom directly. Remove it and the argument has a hole. | "If I cut this, does the case stop standing?" Yes → P1. |
| **Support** | `P2` | Proves, grounds, or makes a P1 feel incontrovertible — the named example, the chart, the stat, the comparison. Strengthens belief; the argument survives its loss because the presenter can narrate it. | "Does the claim survive if the speaker just *says* this instead of showing it?" Yes → P2. |
| **Ornament** | `P3` | Texture, transition, delight, secondary color, the third example, the nice-to-have. | "Is this here to feel good / move the eye / round out a list?" Yes → P3. |

**P1 is what does the work, not what *type* of element it is.** Do not assume copy outranks visuals. On most argument slides the real P1 is the diagram, the chart, or the one number — the picture *is* the argument — and the surrounding copy is P2 or P3 narrating it. Divine each slide's IA from its own content: look at the actual slide, ask what carries the point, and rank from there. Never apply a default template of "headline = P1, body = P2, everything else below." The template is how you miss that the left rail is just re-describing the diagram.

Tag inline at the end of each beat in the narrative MD. Add the axiom for P1s so the spine link is explicit:

```
- The firm shows up in eighteen places and registers in none. {P1:differentiator}
- 18-logo satellite wall {P2}
- ambient royal gradient on the divider {P3}
```

A workflow reading the MD can then compute a cut deterministically and report what it dropped.

**Ranks are relative to the target length.** A rank is not a permanent property of an element — it's that element's importance *at a given budget*. An element that is P1 at twelve slides can fold into a neighboring P1 at eleven (a structural merge, not a demotion). The same unit ranks differently at different budgets and different altitudes. Re-rank when the target changes; don't treat last week's ranks as fixed data.

## The compression law (the only legal moves)

**First, name the binding constraint — time or slide count. They are not the same cut.**

- **Slide-count / density budget** ("get to 10 slides," "lighten the leave-behind"): demotion to voiceover *is* a real cut — the element leaves the surface, the speaker absorbs it.
- **Time budget** ("90 minutes down to 60"): demotion to voiceover is **not** a cut. A demoted P2 still gets spoken, so the clock doesn't move — it just hides the minutes in the talk track where they're harder to see and harder to hold. Under a time budget, **skip demotion entirely** and cut whole. The only thing that buys back stage minutes is content that stops being said.

Then, with the constraint named:

1. **Cut P3 whole**, bottom-up, until you hit budget. Stop here if you can.
2. Still over, *and the budget is slide-count* → **demote P2 to presenter voiceover.** The element leaves the slide; the speaker carries it. (A cut from the *slide*, not the *pitch* — which is why this step is void under a time budget.)
3. Still over → **cut P2 whole.** Under a time budget this is Step 2 — demotion is skipped.
4. **Never touch P1.** If hitting budget would require cutting P1, one of two things is true and both are escalations, not averagings:
   - the budget is wrong (surface to the human), or
   - two P1 elements are doing one job and need a **structural merge** (combine into one stronger element, not two diluted ones).
5. **A surviving element is never shortened to make room.** Kept elements stay at full strength.

Notice what the algorithm has no step for: "shorten everything a little." That structural absence is the anti-blandification guarantee. The only verbs are CUT WHOLE and DEMOTE WHOLE. Extraction (promote the existing sharpest line) beats summarization (write a new blander one) every time — see `copy-compression.md` for the line-level version of the same law.

**Ranking and length are two passes, not one rule.** "A surviving element is never shortened *to make room*" governs **selection** — you don't dilute survivors to fit more units onto the slide. It is not a license for a survivor to run long. After the cut, every surviving element is still subject to `copy-compression.md`'s word caps (Statement ≤30, Argument ≤60, etc.), applied by *selecting the sharpest line within it*, never by averaging it down. Sequence: **rank and cut whole first, then length-check the survivors.** The two laws don't compete — one decides what stays, the other decides how tight what-stays is written.

## One framework, four altitudes

The same rank applies at every zoom level. Compress top-down: cut whole sections before whole slides, whole slides before whole elements, whole elements before lines.

| Altitude | Unit ranked | P1 example | P3 example | Hands off to |
|---|---|---|---|---|
| **Deck** | sections / chapters | the architecture reveal | logistics / agenda / thank-you | — |
| **Section** | slides | the slide that lands the axiom | a second proof slide, a breather | — |
| **Slide** | elements (headline / body / diagram / caption / eyebrow / footnote) | the headline claim + its one diagram | decorative caption, footnote | — |
| **Line** | sentences inside an element | the claim sentence | the setup / runway sentence | `copy-compression.md` |

This is also the "one viz zoomed at different altitudes" pattern: don't build separate ranking systems per level — it's the same spine-distance test applied at four zooms.

## IA-health diagnostic (compression-readiness)

Run this before any compression, and as a deck-score companion. It finds slides that will *resist* clean cutting:

- **Structural slides are exempt — tag them `{STRUCT}`, never rank them.** Dividers, section bridges, and not-yet-authored placeholders carry pacing and navigation, not argument. They have no P1 by design. Skip them in the diagnostic and never feed them to a content-cut. This exemption is for the *machine*: a human knows not to cut a divider; an agent running the law literally needs it said. (A divider can still be cut as a whole-section decision at the deck altitude — that's a pacing call, not an IA-health failure.)
- **Every content slide should have exactly one clear P1.** That P1 is the slide's reason to exist.
- **Zero P1 on a content slide** → the whole slide is support or ornament. The slide itself is P2/P3. Cut it whole; fold any needed proof into the slide it was supporting.
- **Two or more competing P1s on one slide** → the slide is doing two jobs. It will fight compression because neither half is cuttable. Split it now (so each half can be ranked independently later) or merge the two claims into one genuinely-single claim.
- **A P1 you can't link to a spine axiom** → either the spine is incomplete, or the element is mis-ranked. Resolve before cutting.
- **Copy-vs-visual redundancy (diagram-led slides).** When a slide's P1 is a diagram or chart — the reveal *is* the picture — ask of every line of copy: *does this restate what the visual already shows?* If yes, that copy is **P3 by default**, regardless of how well-written it is. A busy diagram slide is almost always busy because the copy is narrating the picture. Cut the narration; let the diagram carry it. Keep only the copy the visual genuinely **cannot** say (the off-diagram context, the rationale, the breadth a node can't list). The legend names the tiers; it does not re-describe them. (Origin: 2026-05-31, user feedback on a brand-model slide — "Is the left rail duplicating what is on the right? If the diagram showed this clearly… this slide is too busy.")
- **Copy-internal redundancy (the same idea, twice in words).** Ask of every line in a body: *does this restate a point another line — or the headline, or a neighboring slide — already made?* If yes, it is **P3 by default**, however well-written. Cut it whole; do **not** merge the two lines into one blander combined sentence — that is averaging. Keep the single sharpest instance, kill the rest. Redundancy is waste in exactly the way over-support is: more to read, no added argument. (This is the slide/element-altitude version of `copy-compression.md`'s "body must not restate the headline.")

A deck whose every slide has one spine-linked P1 compresses surgically. A deck without that structure can only be compressed by averaging — which is the failure mode this reference exists to kill.

## What NOT to do

- **Don't shave words off every element to hit a budget.** That's averaging. Cut whole P3s instead.
- **Don't keep a weak P1 and a strong P1 by shortening both.** Merge them into one strong element or escalate the budget.
- **Don't silently drop elements.** When a workflow cuts by rank, it logs every unit dropped and its rank. Silent truncation reads as "we covered everything" when we didn't.
- **Don't rank by length or effort.** A one-word P1 outranks a paragraph of P2. Rank by distance from the spine, never by how much work an element was to make.
- **Don't blandify the survivors.** The point of cutting whole is that what remains stays sharp. If the kept copy got softer, the cut was done wrong.

## When to invoke this reference

- Any "condense this deck / cut to N minutes / make this shorter" task at the slide or section level.
- Before authoring a deck that will later need to flex to multiple lengths (rank as you build; compression becomes free).
- As a deck-score companion (IA-health pass) before a quality run.
- Whenever the instinct is to "tighten everything" — that instinct is the failure mode; rank and subtract instead.

## Relationship to neighbors

- **`copy-compression.md`** — the line altitude. Selection inside one element. This reference hands off to it at the bottom zoom.
- **`quality-system-v2.md`** — scores finished quality. IA-health is the pre-compression structural check that makes a deck *cuttable* before it's scored.
- **The project spine (strategy atom)** — the north star that makes ranking objective rather than taste. No spine named = no valid ranking. Name the spine first. Canonical definition: `~/Projects/studio-v2/plugins/strategy/references/spine.md`.
