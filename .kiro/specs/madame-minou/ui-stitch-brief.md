# Madame Minou: Stitch UI Brief

*Paste-ready prompts for Google Stitch. Stitch designs screen looks from prompts + image references; it does NOT know our tech stack, build order, or architecture, and does not need to. Feed it: the two hero screenshots (style anchor) + the prompts below (screens, copy, states).*

*Last updated: June 24, 2026*

---

## How to drive Stitch

1. Upload the two hero screenshots as the style reference.
2. Paste the **master style prompt** first to set the design system.
3. Use Stitch's multi-screen workspace so components stay consistent across screens (the anti-drift win).
4. Generate each screen with its prompt below. Keep the same style language each time.
5. Iterate with short follow-ups ("more muted," "bigger CTA," "show the loading state").
6. When happy: extract the **design tokens** (exact colors, type scale, spacing, radii, motion) and the **component list**. Those are the law (see `steering/ui.md`). Then build clean in Kiro to the tokens. Treat Stitch's exported code as a visual reference, not the submission code.

## Master style prompt

> Design a whimsical, surreal web app called **Madame Minou**, a cat astrology app. Visual style: a Parisian café terrace at night in the painterly style of Van Gogh, swirling starry sky, deep navy blues, warm gold and amber lamplight, wet cobblestones. Dreamy and a little surreal, with the tagline energy "Are cats even real?". The mascot and guide is a **tuxedo cat in a small beret**, a French fortune teller named Madame Minou. Mood: warm, witty, mysterious, French. Match the palette and mood of the uploaded reference images. Use an elegant display typeface for headings and a clean, readable body face. **One prominent call-to-action per screen; everything else understated.** Mobile-first and responsive. Keep components consistent across all screens (one card style, one button style, one input style).

## Per-screen prompts

**1. Landing / hero**
> Landing screen. Full-bleed hero of the café-terrace starry-night art with the tuxedo cat in a beret at a café table. Show the app name "Madame Minou" and the line "Are cats even real?". One large primary button: "Consult Madame Minou". Below it, a single sample reading card (a demo reading) so a first-time visitor understands the product, and a quiet text link to "About". Atmospheric and uncluttered.

**2. The consultation (intake)**
> Consultation screen, styled like sitting down at the fortune teller's café table. Ask one question at a time as a speech bubble from Madame Minou, not a form. Step 1: "What do they call this little beast?" with one text input for the cat's name. Step 2: the cat's birthday with a clean, simple date input, plus a soft secondary option "She's a mystery to me too". Only one question visible at a time. A single "Continue" action.

**3. The reveal / loading**
> A loading and reveal moment. Madame Minou at her candlelit café table under the swirling stars, eyes lifted to the sky, reading. An anticipation animation that feels like a séance, not a technical spinner. Then the reading card is revealed with a gentle flourish.

**4. The reading card (the core reusable component)**
> A single elegant reading card holding Madame Minou's reading text for the cat, with the cat's name and its sun, moon, and rising signs, written in a warm French voice. Include a "Share" button and an optional small "Hear Madame Minou" speaker icon. Include a small, quiet care line: "Madame Minou reads stars, not bloodwork." This card style is reused everywhere (daily readings, behavior reads).

**5. Behavior read + free counter + paywall**
> A behavior screen: a simple input to log a cat behavior (for example "won't cuddle" or "knocked a glass off the table"), returning a behavior reading on the same card style. Show a friendly counter: "2 of 3 free reads left today". When the free reads run out, show a gentle, on-brand upgrade prompt styled as Madame Minou offering more readings, warm rather than a hard sell.

**6. About + Penelope's memory**
> An About page. Tell the short story of how the app was born on a trip to Paris (with a link to a dev.to article). A quiet dedication to Penelope, a tuxedo cat (May 2009 to February 17, 2026), with the line "Madame Minou is, and always was, Penelope." A discreet, subdued "In Penelope's memory" note linking to Lap of Love's Angel Fund, dignified and understated, not a banner. Small attribution links at the bottom. Calm and tender.

**7. Daily nudge opt-in (coming-soon stub)**
> A small, quiet opt-in card: "Want Madame Minou in your inbox each morning?" with an email field and a "Notify me" button. Secondary and understated. This is a coming-soon feature.

## States to ask Stitch for explicitly

- **Loading:** the séance/anticipation beat (not a spinner).
- **Error:** an in-voice message, "Madame Minou's crystal ball is cloudy, try again, chérie", never a blank screen.
- **Unknown-birthday path:** the "She's a mystery to me too" branch and its "mystery cat, mystery stars" reading.
- **Mobile layouts** for every screen.

## After Stitch (the handoff that prevents drift)

1. Pick the version you love.
2. Extract design **tokens**: exact hex colors, the type scale, spacing, border radii, shadow, motion timing. Name them (`--color-night`, `--color-gold`, etc.).
3. Extract the **component list**: card, button, input, speech bubble, the reveal.
4. Hand those to Kiro as the UI law (per `steering/ui.md`). Build the tokens file first in the UI block, then compose every screen from the components.
5. The Stitch export is the picture. The tokens are the law.
