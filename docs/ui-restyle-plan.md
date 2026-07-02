# Madame Minou: UI Restyle Plan (visual layer only)

*Restyle the existing components. No layout, copy, DOM, or behavior changes. Approved from ChatGPT mockups, June 30 2026.*

## Locked design decisions

- **Chrome system:** "Starlit Shimmer" (mockup Variation 3). Backgrounds, frames, secondary buttons, badges, nav.
- **Primary Consult CTA:** impasto molten-gold pill (mockup Variation 1). The one loud element per screen.
- **Background:** "Constellation Wash." Impasto night sky, faint gold cat constellations and zodiac glyphs at low opacity.
- **Reading card:** "Crescent Archive." Fine gold frame, restrained painterly corner accents, a watching crescent-moon motif (NOT a cat: the background already carries the constellation cat, so the card takes the moon), amber lamplight glow, gold accent line on the quote, and a bottom icon row.

Mockups are painted references. We approximate them in CSS with the existing tokens. No pixel-matching the oil paint. The impasto is a tasteful suggestion, not literal texture.

## Guardrails (MUST hold for every block)

- **Restyle only.** Do NOT change layout, DOM structure, copy, or JS. Extends "DO NOT refactor other code."
- **Token first.** Every new value is a token in `:root`. No raw hex or px inside a component.
- **Real Tailwind build.** Run `npm run build:css` and inline the output after adding any class. New arbitrary classes will not render otherwise.
- **Security stays.** `textContent` only for dynamic text. No `innerHTML`. No `eval`.
- **Accessibility.** Body text keeps WCAG AA contrast over the new background. Keep `:focus-visible` rings. Honor `prefers-reduced-motion` (no shimmer or float when reduced).
- **Art discipline.** Constellations and glyphs ship as inline SVG at low opacity: no external requests, crisp at any DPI. No functional text baked into art. Dream-text stays decorative only.
- **History nav** stays a greyed `aria-disabled` v2 stub. Do not activate.
- **Performance.** Background is CSS layers plus one small inline SVG, never a heavy raster.

## Step 0: update the source of truth first (so Kiro stops reverting)

Update `.kiro/specs/madame-minou/design-system.md` and `.kiro/steering/ui.md` to describe the locked look and add the new tokens below. This is law. Do it before touching `index.html`, or the next rebuild regresses the design.

## New tokens (add to `:root`)

- `--gradient-gold: linear-gradient(135deg, #ffd273 0%, #ebb42b 100%);` primary CTA fill
- `--color-constellation: rgb(253 243 167 / 0.12);` starlight-gold, low opacity, for line art
- `--card-frame:` 1px starlight-gold at ~35% plus inner amber glow
- Reuse existing `--shadow-lamplight*` glows and the `.impasto-texture` noise.

## Block A: global background, Constellation Wash  [QA gate]

Layer back to front on the surface behind content, not the hero:

1. Base deep-navy gradient (`#080C1A` to `#0A142F`), the existing body gradient.
2. Impasto texture overlay at ~3% (existing `.impasto-texture`).
3. One inline SVG: faint gold cat constellation, a few zodiac glyphs, scattered stars at ~10 to 14% opacity, `pointer-events: none`, biased to the edges so no text column sits under it at full strength.
4. A single brighter "wish star" accent, small, upper area.
5. Soft vignette to keep edges dark.

**PASS/FAIL:** body text over the background still hits AA; no horizontal scroll; reading card stays fully legible; reduced-motion shows a static version.

## Block B: buttons, badges, icons, nav  [QA gate]

- **Primary CTA (`.btn-consult`):** impasto molten-gold pill. `--gradient-gold` fill, 3px painterly darker-gold bottom border, soft inner top highlight, amber glow, ~0.92 opacity rising to 1 on hover, low-opacity gold texture overlay. One component reused everywhere a primary action appears.
- **Secondary button (`.btn-ghost`):** transparent fill, thin gold outline (~40%), gold text, gentle glow on hover. Example: "Explore your cosmic path."
- **Badge (`.badge-soon`):** small chip, gold hairline outline, uppercase micro-label, faint star. Used for History "soon" and future stubs.
- **Icon buttons (share, sound):** circular, gold hairline outline, glow on hover; disabled state at reduced opacity.
- **Bottom nav:** thin gold line icons; active item glows gold with the cat glyph; History greyed stub unchanged.

**PASS/FAIL:** exactly one loud CTA per screen, all others visibly quieter; focus rings present; hover and active states honor reduced-motion; contrast holds.

## Block C: reading card, Crescent Archive  [QA gate]

- **Card (`.card-reading`):** semi-transparent midnight-navy, backdrop blur, fine gold frame (`--card-frame`), restrained painterly corner accents (borrowed from Zodiac Filigree, not the full filigree), amber lamplight glow, subtle impasto texture.
- **Crescent-moon motif:** inline SVG, low opacity, behind the text, `pointer-events: none`, must not reduce legibility. Moon, not cat: the Constellation Wash background already carries the cat, so the card takes the moon for motif variety.
- **Quote accent:** warmed gold hairline along the left of the quote (existing `border-l` pattern).
- **Icon row:** SAVE, SHARE, COPY, FAVORITE, LISTEN with gold hairline dividers. v1 wiring: **Share is live**, **Listen is a greyed `aria-disabled` coming-soon stub** (matches the audio stub elsewhere). **Save, Copy, Favorite are styled greyed stubs only**, not wired to behavior (per "stub, don't build"). All are real `<button>`s with `aria-label`; stubs get `aria-disabled` and a "soon" affordance.
- Keep the care line on behavior reads. AI reading text set via `textContent`.

**PASS/FAIL:** paragraph fully legible over the moon motif; frame crisp on mobile and desktop; no layout shift versus the current card; live actions work, stub actions are visibly quiet and non-interactive.

## Build order

Step 0 (spec) then Block A then Block B then Block C. QA PASS gate between each. One block per commit or PR. No block starts until the previous passes.

## Out of scope (NEVER in this pass)

No layout or copy changes. No new screens. No data or API changes. No activating History. No heavy raster backgrounds. No new web fonts beyond Playfair Display and Manrope.
