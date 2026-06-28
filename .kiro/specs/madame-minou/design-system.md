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

**Hero (do not regress):** the hero art is a CONTAINED banner, roughly 40vh (min ~300px, max ~460px), never a full-viewport takeover. The title and tagline overlay the art; the art fades into the background at its bottom edge. The gold CTA, Madame Minou's speech bubble, and the sample reading ("results") card must all be visible without heavy scrolling. (The original Stitch export used a 751px hero that buried everything below the fold; that is the bug this rule prevents.)

**Hero image asset:** `assets/hero.png`, the café-terrace tuxedo-cat painting (human-authored; no UI or title text baked in; the garbled "Café de Nuit Étolée" sign is the kept easter egg). It is **square (1024x1024)** while the hero band is wide, so set `background-position` to keep the cat and café table in frame on wide screens (around center to center-bottom), and add a dark scrim at the band's lower edge for text legibility. Reference the LOCAL file, never an external URL.

**Elevation (organic, not digital):** Level 0 the Night (background gradient + impasto). Level 1 the Table (semi-transparent midnight-blue cards, 1px starlight-gold border @20%). Level 2 the Glow (elevated elements use a diffused amber `lamplight-glow` shadow with 32px+ blur, never black shadows).

**Shapes:** Rounded, soft. Buttons/cards 16px radius. Speech bubbles: larger radius on three corners with a distinct tail.

## Components

- **Buttons:** one prominent CTA per screen. Solid gold fill, dark navy text, a 3px "painterly" darker-gold border-bottom for a tactile stamped feel.
- **The Reading Card (hero component):** semi-transparent midnight-blue, backdrop blur, fine gold border, amber glow shadow. Reused everywhere (natal, behavior, nudge). Understated ghost-gold "Hear Madame Minou" icon. Include the care line on behavior reads.
- **Input fields:** understated lines / soft wells. Cat name = single 2px gold bottom-border that glows on focus. Date = minimalist astronomical-calendar overlay (but keep it a reliable, accessible native-style control under the hood).
- **Speech bubbles:** midnight-blue with impasto-white text, fade-and-float animation. Madame Minou's questions.
- **The Nudge Card:** "coming soon" module, dashed border, lower opacity, clearly secondary (the daily-nudge STRETCH stub).

## Build notes (do not skip)

- Build the `:root` token layer first; every component references tokens, never raw hex.
- Functional UI text is real, legible HTML; garbled lettering stays in the art layer only (the easter egg).
- Icon controls are real `<button>`s with `aria-label`. History nav = greyed/disabled v2 stub.
- AI reading text inserted with `textContent`, never `innerHTML`.
- Real Tailwind build, not the Play CDN.
