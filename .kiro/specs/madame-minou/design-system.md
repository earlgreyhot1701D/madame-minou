# Madame Minou: Design System ("L'Astre de Minou")

*Harvested from the Stitch export (DESIGN.md). This is the UI law: tokens + component specs. Kiro builds every screen from these. The Material-Design role colors from the raw export are pruned here to the brand tokens actually in use. Build a `:root` tokens layer from this FIRST in the UI block, then compose every screen from the components.*

*Last updated: June 24, 2026*

---

## Tokens

### Color (brand set)

```
--color-background      #0F1321   /* near-black navy, the night */
--color-midnight-blue   #0A142F   /* surfaces, cards, speech bubbles */
--color-surface         #0F1321
--color-surface-bright  #353948
--color-primary         #FFD273   /* gold CTA fill */
--color-primary-container #EBB42B /* deeper gold (painterly border-bottom) */
--color-on-primary      #402D00   /* dark text on gold */
--color-starlight-gold  #FDF3A7   /* headline gold, accents, hairline borders @20% */
--color-secondary       #B3C6FB   /* soft periwinkle, tagline/secondary text */
--color-tertiary        #FFCDC0   /* terracotta accents, Minou's beret, alerts (sparing) */
--color-cobblestone-gray #3D4251
--color-impasto-white   #F4F1EA   /* speech-bubble text */
--color-on-surface      #DFE1F6
--color-on-surface-variant #D3C5AE
--color-outline         #9B8F7A
--color-error           #FFB4AB
--color-lamplight-glow  rgba(235,180,43,0.15)  /* amber glow shadows/blurs */

/* ── Restyle additions ─────────────────────────────────────── */
--gradient-gold         linear-gradient(135deg, #ffd273 0%, #ebb42b 100%)  /* primary CTA */
--color-constellation   rgb(253 243 167 / 0.12)  /* starlight-gold, low opacity linework */
--card-frame            1px solid rgb(var(--color-starlight-gold) / 0.35)  /* + inner amber glow */
```

Background gradient (the night): `#080C1A` to `#0A142F` with a faint impasto noise texture overlay.

### Typography

- **Playfair Display** (headings, app name, speech bubbles, reading titles): display-lg 48px/700/-0.02em, headline-lg 32px/600, headline-lg-mobile 28px/600.
- **Manrope** (body + UI): body-lg 18px/400/1.6, body-md 16px/400/1.5, label-sm 12px/600/0.05em.
- Large display favors tight letter-spacing (editorial). Body uses generous line-height (dreamy, unhurried).

### Radius

`sm 4px · DEFAULT 8px · md 12px · lg 16px · xl 24px · full 9999px`. Base for buttons/cards: 16px.

### Spacing

`unit 8px · gutter 16px · margin-mobile 24px · margin-desktop 64px · reading-width 600px`. Wide vertical rhythm (64px+) between mascot/headline and the primary interaction.

---

## Style guide (from the system)

**Brand:** Painterly Surrealism, a Van Gogh-inspired Parisian night. Whimsical yet authoritative, mysterious yet warm. Keywords: Witty, Parisian, Esoteric, Painterly, Warm, Tuxedo-chic.

**Color roles:** Primary gold = CTAs, active states, astrological symbols (gaslight/starglow). Deep navy = surfaces/containers (sky depth). Terracotta = sparing Minou accents (her beret) or critical alerts. Midnight void = foundational background that lets gold pop. Use `lamplight-glow` for soft background blurs/shadows (candle heat).

**Layout:** Centered fixed grid on desktop (max-width 600px for the reading card and intake steps, intimate one-on-one feel); fluid stacked grid on mobile (card = 100% minus 24px margins). Breathable vertical spacing.

**Hero (do not regress):** the hero is a full-width 16:9 banner (w-full, aspect-video, min-h-[420px], max-h-[75vh]) holding the wide painting at background-size: cover (never contain, never a centered square, no dark side bars). A bottom gradient scrim keeps foreground text legible. The "Madame Minou" title + tagline overlay the TOP over the sky. Madame Minou's speech bubble + the gold "Consult Madame Minou" CTA sit together at the BOTTOM LEFT of the hero, anchored to the left (NOT centered, no mx-auto) and capped so they never cross into the right half where Madame's portrait lives. The sample reading card + about link follow below the hero. The CTA is a warm gold gradient (#ffd273 to #ebb42b), ~0.92 opacity, soft amber glow, painterly bottom-border.

**Hero image asset:** `assets/hero.png`, the café-terrace tuxedo-cat painting (human-authored; no UI or title text baked in; the garbled "Café de Nuit Étolée" sign is the kept easter egg). It is a **wide 16:9 painting** while the hero band is wide, so set `background-position` to keep the cat and café table in frame on wide screens (around center to center-bottom), and add a dark scrim at the band's lower edge for text legibility. Reference the LOCAL file, never an external URL.

**Elevation (organic, not digital):** Level 0 the Night (background gradient + impasto). Level 1 the Table (semi-transparent midnight-blue cards, 1px starlight-gold border @20%). Level 2 the Glow (elevated elements use a diffused amber `lamplight-glow` shadow with 32px+ blur, never black shadows).

**Shapes:** Rounded, soft. Buttons/cards 16px radius. Speech bubbles: larger radius on three corners with a distinct tail.

## Components

- **Primary CTA (impasto molten-gold pill):** `--gradient-gold` fill, 3px painterly darker-gold bottom border (`--color-primary-container`), soft inner top highlight, amber lamplight glow (`--shadow-lamplight`), ~0.92 opacity rising to 1 on hover with subtle lift, low-opacity gold texture via `.impasto-texture`. `rounded-full` pill shape. One loud CTA per screen; everything else quiet. Reuse the one component.
- **Secondary button (ghost):** transparent fill, thin gold outline (~40% `--color-starlight-gold`), gold text, gentle lamplight glow on hover. Quiet, never competes with the primary CTA.
- **Badge ("soon"):** small chip, gold hairline outline, uppercase micro-label (`label-sm`), faint star icon. Used for v2 stubs (History, etc.).
- **Icon buttons (share, sound, save, copy, favorite):** circular, gold hairline outline, lamplight glow on hover. Disabled state at reduced opacity (~30%). `aria-label` required.
- **The Reading Card ("Crescent Archive"):** semi-transparent midnight-navy (`--color-midnight-blue` at 80%), `backdrop-blur-xl`, fine gold frame (`--card-frame`), restrained painterly corner accents, amber lamplight glow (`--shadow-lamplight`), subtle `.impasto-texture` overlay. A watching crescent-MOON motif as low-opacity (~10-14%) inline SVG behind the text (moon, not cat — the background carries the cat). Warmed gold hairline along the quote border-left. Bottom icon row: Save, Share, Copy, Favorite, Listen with gold hairline dividers. v1 wiring: Share live, Listen a greyed `aria-disabled` coming-soon stub, Save/Copy/Favorite styled greyed stubs only (stub, don't build). Include the care line on behavior reads. Reused everywhere (natal, behavior, nudge).
- **Input fields:** understated lines / soft wells. Cat name = single 2px gold bottom-border that glows on focus. Date = minimalist accessible native-style control.
- **Speech bubbles:** midnight-blue with impasto-white text, fade-and-float animation. Faint gold inner glow to rhyme with the CTA.
- **The Nudge Card:** "coming soon" module, dashed border, lower opacity, clearly secondary (the daily-nudge STRETCH stub).

## Background: Constellation Wash

The surface behind content (NOT the hero) is layered CSS:
1. Base deep-navy gradient (`#080C1A` to `#0A142F`)
2. `.impasto-texture` noise overlay at ~3% opacity
3. One inline SVG: a faint gold cat constellation + a few zodiac glyphs + scattered stars at `--color-constellation` (~10-14% opacity), biased to the edges so it never sits at full strength under a text column
4. One small brighter "wish star" accent
5. A soft vignette (radial gradient darkening the edges)

Must keep body text at WCAG AA contrast. Inline SVG only — no external requests, no heavy raster images. The constellation is decorative (`aria-hidden="true"`).

## Build notes (do not skip)

- Build the `:root` token layer first; every component references tokens, never raw hex.
- Functional UI text is real, legible HTML; garbled lettering stays in the art layer only (the easter egg).
- Icon controls are real `<button>`s with `aria-label`. History nav = greyed/disabled v2 stub.
- AI reading text inserted with `textContent`, never `innerHTML`.
- Real Tailwind build, not the Play CDN.
