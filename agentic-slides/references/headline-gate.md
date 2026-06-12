# The Headline Gate

> Canonical, consolidated reference for headline quality in agentic-slides. Merges three checks that used to live in three places (the per-slide cold-read, the label-vs-key-idea test, and the sequence-flow test) into one named gate. Created 2026-05-29 after a final-pitch deck's Section 1 drifted to label-headlines despite all three rules already existing — scattered, partly deprecated, and never auto-firing on edits.

## Why this gate exists (the failure it prevents)

The same headline feedback kept recurring across sessions. The rule kept getting lost because it was **scattered across multiple files (one deprecated), and nothing forced it to run when headlines were built or edited.** It only ran when the user caught a bad headline by hand.

The fix is not a new mode. It is: **one home, auto-fired.** This gate is that home. It mirrors how `/write:voice` auto-invokes at the end of every `/write` sub-skill — you never have to remember it.

## The forcing rule (READ THIS FIRST)

**This gate auto-fires on BOTH events:**

1. **Build** — as part of Phase 5.1, on every full deck build. (Always ran here in principle.)
2. **Edit** — the moment ANY headline is created, rewritten, or changed, even a single targeted edit outside a full build. (This is the gap that let labels creep in. A one-slide headline change still fires the gate.)

If you are about to write a headline to the canvas, the Headline Gate runs first. No exceptions. Headline mutations are never "just a quick edit."

**Verify from the render, never from the MD.** Headlines drift between the source doc and the live deck. Pull the actual headline text from the canvas (Figma/Paper) before evaluating. The MD is not the truth; the slide is.

---

## The three checks

A headline passes the gate only if it clears all three.

### Check 1 — Cold read (clear without context)

A stranger landing on this one slide, with zero deck context, must understand what the slide is saying. If the headline only makes sense after you read the body, it is doing **description** work, not **argument** work.

- **Mechanism:** the per-slide cold-read (Naive Reader) from [per-slide-clarity-gate.md](per-slide-clarity-gate.md). Spawn a fresh-context agent that sees ONLY this slide's eyebrow + headline (+ visual description), and ask: "What is this slide claiming? What is the one thing it wants you to believe?"
- **Pass test:** the cold reader restates the slide's actual point. **Fail:** the cold reader can only name the topic ("this is about discovery / about brand equity"), or asks for the body to understand it.

### Check 2 — Key idea, not label (the headline IS the point)

> "The headline should ALWAYS express the key idea — the clearest articulation of it. Then the body proves or extrapolates it." — author's rule, 2026-05-29

This is the `/strategy:narrative` **Headline-vs-Role** test, verbatim:

> "Does the headline DO the job the role requires, or does it just describe the topic? **Headlines that describe topics are OBSERVATIONS. Headlines that do jobs are ARGUMENTS.**"

And the agentic-slides **Unveiling-vs-Supporting** test: "Does this NAME a new idea as a claim, or describe an example/topic of one? If it's opaque or generic without the body, it's doing description work."

- **The "stuff changed" smell:** A headline like "Today, new technologies are evolving the purpose, discovery and ongoing value of asset management" names a subject and asserts nothing a skeptic could disagree with. It is a LABEL. It does not earn its weight.
- **The claim test:** Could a skeptical client read the headline alone and either agree or disagree with a specific assertion? If there is nothing to disagree with, it is a label. Rewrite it into a claim.
- **Compare:** a Bloomberg-style exemplar — "New technologies and the evolution of ABM are making differentiated features the common experience" — makes a claim. The topic version would have been "How ABM is evolving."

### Check 3 — Sequence flow (each headline runs into the next like one story)

Read the eyebrows + headlines in order, with NO body copy. They must tell the whole argument on their own, each one making the next feel inevitable — a run-on story, not a table of contents.

- **Mechanism:** the Headline Transition Scoring + the `/strategy:narrative` **Argument-chain test**. Score every A→B transition 1–10 (does B follow from A — shared language, logical progression, emotional continuity). **Any transition below 6 = rewrite.**
- **Keyword threading:** the 2–3 words carrying the argument should reappear across adjacent slides. If slide N names "the relationship," slide N+1 should pick up "relationship" or its consequence. Shared nouns are the connective tissue.
- **The aloud test:** read the headlines in sequence out loud. Any moment you think "wait, how did we get here?" is a broken transition.
- **Blind-read:** a reader who sees ONLY the headlines must be able to reconstruct the deck's argument from problem to resolution. If the summary misses the core proposition, the headlines aren't carrying it.

---

## Rewrite rule (when a headline fails)

When the gate flags a headline, fix it by **extracting, not summarizing.** This is the `/strategy:narrative` **Extract-Don't-Summarize** rule:

> "If shortening: cut words from the original line. Don't rephrase. Replacing a specific, voiced sentence with a generic summary is a SKILL FAILURE."

The first move on a label-headline is to **hunt the author's existing copy** — the slide's own body, the source doc's archived/prior headline versions, the dossier, the brief — for the sharpest line, and promote it. Lift and cut; never neutralize into generic marketing prose. (See [copy-compression.md](copy-compression.md) "Select, don't summarize.")

**Watch the promotion side-effect:** if you promote a body line to the headline, that line must LEAVE the body (otherwise the body restates the headline). Re-check the body after any headline promotion.

**Voice constraints on any rewrite:** no em dashes, no Big One (negation-correction "X isn't Y, it's Z"), Twin-B register. Run the result through the Copy Quality voice gate before applying.

**Surface, don't auto-apply:** the gate produces findings and sourced rewrite candidates. Present them for accept/reject; the author picks. (Standing rule: critique tools surface, never auto-edit.)

---

## On-demand invocation (the reusable engine)

Beyond auto-firing in Phase 5, this gate can be run on its own at any time ("run a headline pass"). The engine is a fan-out workflow:

1. **Pull headlines render-true** from the canvas (one query, all slides: eyebrow + headline + body + node IDs).
2. **Evaluate** (one agent per headline, this reference loaded): Check 1 + Check 2 → classification (LABEL / BORDERLINE / KEY_IDEA), score 1–10, diagnosis.
3. **Rewrite** (flagged headlines only): candidates that LIFT from existing copy, each citing the verbatim phrase and source.
4. **Sequence** (barrier, one agent): Check 3 — blind-read current vs proposed, transition-score the proposed set, flag breaks.
5. **Surface** the report for accept/reject. Apply picks via one canvas write + paired MD edit. Re-run the voice gate on finalists first.

Reference implementation: a Section-1 headline evaluation run, 2026-05-29. To generalize: parameterize the slide-pull by file key + row, keep the rule text (this file) in every agent prompt.

---

## Relationship to the other references

- [per-slide-clarity-gate.md](per-slide-clarity-gate.md) — owns the full per-slide cold-read + fidelity machinery (Naive + Expert + aggregator). Check 1 is its headline-scoped subset. The clarity gate still runs whole at Phase 5.2.
- [headline-review-agents.md](headline-review-agents.md) — DEPRECATED; its Blind Reader / Gap Analyzer / Transition Scoring are absorbed here.
- `/strategy:narrative` Headline-vs-Role + Argument-chain + Extract-Don't-Summarize — the strategic-authoring source of Checks 2 and 3. This gate is the render-stage enforcement of that discipline. Strategy owns "does the headline argue?"; this gate owns "does it still argue on the canvas, cold, in sequence?"
