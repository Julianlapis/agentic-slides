# Copy Compression: Select, Don't Summarize

> **Ownership (consolidation 2026-06-01):** This file is the **canonical owner of the slide word-cap table** (the values + the method to hit them). voice-scoring.md and `/write:edit` carry the numbers as marked mirrors — change a cap *here* first. · The **doctrine** behind "select, don't summarize" is owned upstream by `/strategy:narrative` → **"Extract, Don't Summarize"** (authoring) and `voice-dna.md` → **"The Extraction Principle"** (voice axiom); this file is the *render-stage application* with slide-level worked examples.

The default AI failure mode when asked to shorten copy is to summarize everything in fewer words. This produces vague, flattened prose that sounds like a brief instead of a slide. The correct approach is **selection**: pick the one idea that earns its place, cut the rest.

## The Method (per slide)

### Step 1: Name the one thing
Read the headline and body together. What is the single idea this slide exists to land? Write it in one sentence. If you can't write it in one sentence, the slide is doing two jobs and needs structural work, not compression.

### Step 2: Find the sharpest proof
Of all the evidence in the body (stats, examples, comparisons, analogies), which ONE makes the case most concretely? Keep that proof. Cut the rest. The presenter will narrate the secondary evidence.

### Step 3: Write claim + proof

**Word count is the load-bearing rule. Sentence count is a heuristic floor only.** Length is length — a 30-word single compound sentence overwhelms exactly as much as four 7-word sentences. The original failure mode (2026-05-12, a vision research dossier) had operators treating labeled beats as structural elements rather than body sentences, which let sentence-count rules pass while word counts ran 2–5× over cap.

**Word caps (the gate — CANONICAL SOURCE; mirrors point here):**
- Statement slides: **body ≤30 words.** The headline IS the claim; body is the proof.
- Argument slides: **body ≤60 words.** Claim + proof.
- Evidence slides: **body ≤50 words.** Example + why it matters.
- Grid cards: **each card ≤15 words.**
- PRIMER slides: **body ≤100 words** across all definitions.

**Sentence count heuristic (floor only):**
- Statement: ideally 1–2 sentences. Multi-beat structured bodies count every labeled beat as a sentence.
- Argument: ideally 2–3 sentences. Same rule for structured bodies.
- Evidence: ideally 2 sentences.

If sentence count says fine but word count says over: word count wins. Recompress.

### Step 4: Check against the headline
Body must not restate the headline. See `strategy-engine/references/slide-conventions.md` → "Body copy extends, never restates" for the full rule and examples. Common violations to catch during compression:
- Body sentence 1 rephrases the headline in different words
- Body final sentence re-lands the same point as a "kicker"

## What NOT to do

### Don't summarize all ideas in fewer words
BAD: "Acme solves retention through multi-vertical engagement and a persistent identity layer"
GOOD: "Markets close daily. Pack drops ship weekly. Races run seven days a week."
The bad version preserves all ideas vaguely. The good version keeps one idea concretely.

### Don't compress compound sentences
BAD: Taking "DraftKings consolidated four products under one wallet, generating $6.3B with 4.8M users" and shortening to "DraftKings unified its products for billions in revenue"
GOOD: "DraftKings: four products, one wallet, $6.3 billion in revenue."
Keep the specifics. Cut the connective tissue.

### Don't keep setup sentences
If a sentence exists to set up the next sentence, cut the setup and let the payoff sentence stand alone. The audience doesn't need a runway.

BAD: "Fantasy football works because people talk about the boldness of the roster. Acme applies the same logic."
GOOD: Start with the product example directly. The analogy is for the presenter to say.

### Don't preserve all proof points
If you have three examples that prove the same claim, keep the most specific one. Two examples are elaboration. Three are a list. One is a slide.

### Don't echo the headline in the body
See Step 4 above. If the headline landed the point, the body moves forward. Don't re-land it.

## SCDS Hard Gate Integration

After compression, compute SCDS: (distinct new ideas / total words) x 10

| Slide Type | Max Words | SCDS Target |
|------------|-----------|-------------|
| Statement | 30 | ≥ 1.5 |
| Argument | 60 | ≥ 1.0 |
| Evidence | 50 | ≥ 1.0 |

If the compressed version fails SCDS, you cut too little or you summarized instead of selecting. Go back to Step 1 and re-identify the one thing.

## When to invoke this reference

- After any copy-polish pass flags SCDS failures
- When body copy exceeds the word budget for its slide type
- Before pushing copy to Figma (final gate)
- When the user says "this is too long" or "distill this"

## Relationship to /strategy-engine:distill

/strategy-engine:distill is for **narrative documents** (briefs, specs) where you need the full story in fewer words. That's compression.

This reference is for **slide copy** where you need one idea per slide. That's selection. Different problem, different tool. Don't use distill for slides. Use this method.
