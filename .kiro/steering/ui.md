# Steering: UI

*Persistent UI rules to prevent design drift. Keep visual decisions consistent across every task and session. Re-read this when starting any UI task.*

## Design fidelity: IMPLEMENT the design, do not invent it

Kiro is strong at porting code and weak at inventing art. So the UI is a TRANSLATION job, not a design task. Per Kiro's own guidance, output quality comes from three inputs, all provided here:

1. **Tokens (the law):** `.kiro/specs/madame-minou/design-system.md`. Never invent a value; if something isn't a token, flag it.
2. **Reference implementation (port THIS):** `docs/landing-reference.html` (cleaned + scaled). The raw Stitch export is `docs/design/stitch-landing.html` for comparison. Adapt the reference to the real stack, tokens, and accessibility. Do not redesign it.
3. **Visual ground truth (MATCH this):** `docs/design/stitch-landing.png`. Attach it in the Kiro session and match the layout, proportions, and feel.

Hard rules:
- Implement the provided design exactly. Do NOT redesign layouts, colors, spacing, type, or components. When a detail is missing or ambiguous, ASK; do not improvise a new look.
- **Art assets (hero illustration, favicon, social image) are human-provided files in `assets/`.** Kiro writes the code that places and styles them; Kiro does NOT generate artwork. The art is part of the story and is authored by a human.
- The screens not mocked in Stitch (consultation, results, About) are built from the same tokens + component specs in `design-system.md`, matching the established look. Compose, don't reinvent.
- Optional max-fidelity path: export the Stitch design to Figma and connect it via the Figma MCP for design-to-code mapping. Not required; the reference HTML + screenshot + tokens are usually enough.

## Single source of truth: design tokens

- Define ALL visual values once as CSS custom properties in a `:root` tokens layer: color, type scale, spacing, radius, shadow, motion timing. (This file is code, so it is written FIRST in the UI block during the hackathon, not before.)
- Every component references a token. NEVER hardcode a hex, px, or duration inside a component. "The café blue" is one token, not five guesses.
- Token categories: `--color-*`, `--font-*`, `--space-*`, `--radius-*`, `--shadow-*`, `--motion-*`.

## Primitives first, then compose

- Build the primitives once: the Card (the single reading card), Button, the consultation input field, persona text styles, the reveal animation. Every screen composes them.
- One Card. One Button. No screen hand-rolls its own version.

## Visual world (locked)

- Café terrace at night, Van Gogh idiom, original art. Palette sampled from the locked hero art, not invented.
- Hierarchy: one loud CTA ("Consult Madame Minou"); everything else quiet.
- Dark palette: maintain contrast (R13.3); respect `prefers-reduced-motion` (R13.2).

## Intentional choices (do NOT "fix" these)

- The garbled / nonsense lettering in the BACKGROUND ART (for example the café sign "Café de Nuit Étoilée") is a deliberate surreal easter egg. Keep it. But NEVER replicate garbled text in functional UI: all interface text (nav, buttons, headings, form labels, the reading itself) must be real, correct, legible HTML. Dream-text in the painting; crisp text in the interface.
- All hero/background art ships with NO baked-in functional text; render titles, taglines, and labels as real HTML over a clean image (legibility + accessibility + no misspellings).
- The "History" nav item is a greyed-out, disabled **v2 stub** (`aria-disabled`, a quiet "soon"). Not interactive in v1. Do not build it; do not delete it.

## Anti-drift discipline

- The mockup is the picture; the tokens are the law. Extract tokens + a component list from the mockup, then build to the tokens.
- "DO NOT restyle existing components" when adding a feature (extends "DO NOT refactor other code").
- Screenshot QA at each UI block gate: compare the built screen to the mockup; fix divergence before passing the gate.
