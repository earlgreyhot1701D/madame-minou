---
name: L'Astre de Minou
colors:
  surface: '#0f1321'
  surface-dim: '#0f1321'
  surface-bright: '#353948'
  surface-container-lowest: '#090e1c'
  surface-container-low: '#171b2a'
  surface-container: '#1b1f2e'
  surface-container-high: '#252939'
  surface-container-highest: '#303444'
  on-surface: '#dfe1f6'
  on-surface-variant: '#d3c5ae'
  inverse-surface: '#dfe1f6'
  inverse-on-surface: '#2c303f'
  outline: '#9b8f7a'
  outline-variant: '#4f4634'
  surface-tint: '#f6be35'
  primary: '#ffd273'
  on-primary: '#402d00'
  primary-container: '#ebb42b'
  on-primary-container: '#624700'
  inverse-primary: '#795900'
  secondary: '#b3c6fb'
  on-secondary: '#1b2f5b'
  secondary-container: '#334573'
  on-secondary-container: '#a2b4e8'
  tertiary: '#ffcdc0'
  on-tertiary: '#611300'
  tertiary-container: '#ffa68e'
  on-tertiary-container: '#912200'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdf9f'
  primary-fixed-dim: '#f6be35'
  on-primary-fixed: '#261a00'
  on-primary-fixed-variant: '#5c4300'
  secondary-fixed: '#dae2ff'
  secondary-fixed-dim: '#b3c6fb'
  on-secondary-fixed: '#011945'
  on-secondary-fixed-variant: '#334573'
  tertiary-fixed: '#ffdbd1'
  tertiary-fixed-dim: '#ffb5a1'
  on-tertiary-fixed: '#3c0800'
  on-tertiary-fixed-variant: '#881f00'
  background: '#0f1321'
  on-background: '#dfe1f6'
  surface-variant: '#303444'
  starlight-gold: '#FDF3A7'
  midnight-blue: '#0A142F'
  cobblestone-gray: '#3D4251'
  impasto-white: '#F4F1EA'
  lamplight-glow: rgba(235, 180, 43, 0.15)
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.2'
  body-lg:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  margin-mobile: 24px
  margin-desktop: 64px
  gutter: 16px
  reading-width: 600px
---

## Brand & Style

This design system embodies the "Painterly Surrealism" of a Van Gogh-inspired Parisian night. The brand personality is whimsical yet authoritative, mysterious yet warm—much like the gaze of a tuxedo cat. It targets cat owners who appreciate a blend of humor, art, and the esoteric.

The visual style is a hybrid of **Tactile / Skeuomorphic** and **Glassmorphism**, specifically designed to mimic the thick impasto brushstrokes of a painting while maintaining modern digital usability. The "Are cats even real?" energy is captured through subtle atmospheric animations (swirling stars, flickering candlelight) and a deep, immersive dark-mode-first approach that evokes a moonlit terrace.

**Keywords:** Witty, Parisian, Esoteric, Painterly, Warm, Tuxedo-chic.

## Colors

The palette is derived directly from the "Cafe Terrace at Night" aesthetic. 

- **Primary (Starlight Gold):** Used for primary CTAs, active states, and astrological symbols. It represents the warm amber of gaslight and the glow of distant stars.
- **Secondary (Deep Navy):** Used for surface backgrounds and containers, mimicking the depth of the Parisian sky.
- **Tertiary (Terracotta Red):** Used sparingly for "Madame Minou" accents (like her beret) or critical alerts.
- **Neutral (Midnight Void):** The foundational background color, a near-black navy that allows the gold elements to pop.

Use the `lamplight-glow` for subtle background blurs and shadows to create a sense of radiant heat from a cafe candle.

## Typography

The type system balances 19th-century elegance with modern readability.

- **Playfair Display** (Headings): Captures the literary and sophisticated tone of a French fortune teller. Use for the app name, Madame Minou’s speech bubbles, and reading titles.
- **Manrope** (Body/UI): A clean, modern sans-serif that ensures the "facts object" and behavior logs are perfectly legible against textured backgrounds.

Large display type should favor a tighter letter-spacing to feel more editorial. Body text requires generous line heights to maintain a "dreamy" and unhurried reading experience.

## Layout & Spacing

This system utilizes a **Fixed Grid** centered layout for the desktop to mimic the focused intimacy of a one-on-one consultation, while employing a **Fluid Grid** for mobile.

- **Mobile First:** Content is stacked vertically. The reading card should take up 100% of the viewport width minus the 24px margins.
- **Desktop:** The app is centered with a max-width of 600px for the "Reading Card" and intake steps to maintain focus. 
- **The "Terrace" Rhythm:** Use wide vertical spacing (64px+) between the headline/mascot and the primary interaction to create a "breathable" and surreal atmosphere.

## Elevation & Depth

Hierarchy is established through **Tonal Layers** and **Ambient Shadows** that feel organic rather than digital:

1.  **Level 0 (The Night):** The background—a subtle gradient from `#080C1A` to `#0A142F` with a soft "impasto" texture overlay.
2.  **Level 1 (The Table):** Surfaces (Cards/Inputs) use a semi-transparent Midnight Blue (`rgba(10, 20, 47, 0.8)`) with a 1px border colored like `starlight-gold` at 20% opacity.
3.  **Level 2 (The Glow):** Elevated elements (Active buttons, reading results) don't use black shadows. They use a diffused `lamplight-glow` (amber) shadow with a large blur radius (32px+) to simulate light casting across wet cobblestones.

## Shapes

The shape language is **Rounded**, avoiding the harshness of modern tech.

- **Buttons & Cards:** Use a 1rem (16px) base radius.
- **Speech Bubbles:** Use a slightly larger radius on three corners with a distinct "tail" to indicate Madame Minou is speaking.
- **Interactive States:** Soft, pill-like transitions for toggle buttons or secondary links.

## Components

### Buttons
One prominent CTA per screen. Use a solid `primary-color` (gold) with dark navy text. Use a thick "painterly" border-bottom (3px) in a slightly darker gold to give it a tactile, "stamped" feel.

### The Reading Card
The "hero" component. It must feature a subtle backdrop-filter (blur) and a fine gold border. The "Hear Madame Minou" icon should be understated, using the gold color as a ghost-icon style.

### Input Fields
Inputs are styled as "understated lines" or "soft-wells." For the cat's name, use a single bottom-border (2px gold) that glows when focused. The date picker should be a minimalist custom overlay that feels like an astronomical calendar.

### Speech Bubbles
Used for Madame Minou’s questions. These should be `Midnight Blue` with `Impasto White` text. They appear with a slight "fade and float" animation to enhance the surreal mood.

### The Nudge Card
A "coming soon" module that uses a dashed border and lower opacity, signaling it is secondary to the current consultation.