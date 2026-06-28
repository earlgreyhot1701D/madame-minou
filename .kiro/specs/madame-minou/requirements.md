# Madame Minou: Requirements

*Spec-driven (Kiro-format). Acceptance criteria in EARS notation: WHEN/WHILE/IF [condition] THE SYSTEM SHALL [behavior]. Each group is tagged MUST (v1), STRETCH (reach for it, non-fatal), STUB (show it, don't build it), or NEVER (not in v1, may have a commented stub).*

*Source of truth for product intent: `docs/what-she-is.md`. Source for the AI integration + security: `docs/build-reference.md`.*

*Last updated: June 24, 2026*

---

## Priority legend

- **MUST**: in v1. The build is not done without it.
- **STRETCH**: reach for it after MUST is solid; non-fatal if unfinished; built as an isolated additive block.
- **STUB**: present in the UI as a disabled/"coming soon" state with a commented implementation note; no real wiring.
- **NEVER (v1)**: out of scope this sprint; may carry a commented stub with notes.

---

## 1. Consultation intake (MUST)

**User story:** As a cat owner, I want Madame Minou to ask me about my cat conversationally, so the experience feels like a consultation, not a form.

- 1.1 WHEN a visitor lands on the page, THE SYSTEM SHALL present a single primary call to action labeled "Consult Madame Minou" and SHALL NOT present a multi-field form up front.
- 1.2 WHEN the consultation begins, THE SYSTEM SHALL ask for the cat's name first, then the birth date, one question at a time, in Madame Minou's voice.
- 1.3 THE SYSTEM SHALL require only name and birth date to produce a first reading.
- 1.4 WHILE the owner has not provided a birth time or location, THE SYSTEM SHALL treat both as optional and SHALL NOT block the reading.
- 1.5 WHEN the owner indicates the birthday is unknown ("She's a mystery to me too"), THE SYSTEM SHALL accept a best-guess date or a "gotcha day" and proceed (see degradation, section 3).
- 1.6 THE SYSTEM SHALL use a reliable, accessible date input with a real labeled control, and SHALL NOT depend on a hand-rolled custom date picker.
- 1.7 AFTER the first reading is shown, THE SYSTEM SHALL offer (not require) a deeper read by optionally collecting birth city and time.

## 2. Persona and voice (MUST)

**User story:** As a user, I want Madame Minou to feel like a real character so the reading delights me.

- 2.1 THE SYSTEM SHALL render all readings in Madame Minou's voice: a French cat astrologer in a beret, warm, witty, light franglais.
- 2.2 THE SYSTEM SHALL treat "Madame Minou" as the persona of Penelope (one cat, two names); the identity SHALL be expressed in the About page, not forced into every reading.
- 2.3 THE persona voice SHALL be defined in a single system prompt reused across all reading types (natal, behavior, nudge).
- 2.4 WHEN the red-flag care path triggers (section 8), THE SYSTEM SHALL drop the playful register and speak plainly.

## 3. Deterministic chart engine + degradation (MUST)

**User story:** As a user, I want the astrology to be computed from real data, so it feels earned rather than invented.

- 3.1 THE SYSTEM SHALL compute the chart deterministically with Python + Swiss Ephemeris (pyswisseph). The AI layer SHALL NOT compute or invent astrological positions.
- 3.2 WHEN a full birth date, time, and location are provided, THE SYSTEM SHALL compute sun sign, moon sign, and rising sign, plus notable current transits.
- 3.3 WHEN only a birth date is provided, THE SYSTEM SHALL compute the sun sign, SHALL compute the moon sign when unambiguous, and SHALL omit the rising sign, labeling the result an "estimated chart."
- 3.4 WHEN the moon changes sign on the given date (ambiguous without a time), THE SYSTEM SHALL note the moon as "on the cusp" rather than assert one sign.
- 3.5 WHEN only an estimated year (or nothing reliable) is provided, THE SYSTEM SHALL produce a "mystery cat" reading from whatever is known and SHALL clearly frame it as starlight-guesswork in voice.
- 3.6 THE SYSTEM SHALL apply a fixed timezone assumption when time/location is absent (default: noon UTC) so results are reproducible, and SHALL record which assumption was used.
- 3.7 THE SYSTEM SHALL output the chart as a structured facts object (see design: the deterministic-to-AI contract) consumed by the AI layer.

## 4. The reading and the card (MUST)

**User story:** As a user, I want my reading delivered as one beautiful shareable card.

- 4.1 THE SYSTEM SHALL present every reading (natal, behavior, and nudge) on a single card component: one renderer, multiple triggers.
- 4.2 WHEN the chart facts are ready, THE SYSTEM SHALL call the AI layer with the persona system prompt and the facts as user content, and SHALL render the returned text on the card.
- 4.3 THE SYSTEM SHALL NOT allow the model to alter the deterministic facts; the model only writes voice over them.
- 4.4 THE card SHALL include a share affordance (see section 7).
- 4.5 IF the AI call fails or exceeds a timeout, THE SYSTEM SHALL show an in-voice error state ("Madame Minou's crystal ball is cloudy, try again, chérie"), never a blank screen or stack trace.

## 5. Café-terrace UI + the reveal (MUST)

**User story:** As a user, I want the moment of the reading to feel like theater.

- 5.1 THE SYSTEM SHALL present the experience in the café-terrace-at-night visual world (original art in the Van Gogh idiom; no copied painting).
- 5.2 WHEN the owner clicks "Consult Madame Minou," THE SYSTEM SHALL play a reveal sequence: anticipation beat, then the card revealed with a flourish.
- 5.3 THE anticipation beat SHALL cover AI latency so the wait reads as a séance, not a spinner.
- 5.4 THE reveal SHALL be motion on the card itself, not a separate visual world (no red-curtain room).
- 5.5 THE UI SHALL be responsive and usable on mobile.

## 6. Sound (MUST: chanson · STRETCH-adjacent: Polly)

- 6.1 THE SYSTEM SHALL offer an opt-in French-chanson ambient bed (royalty-free / CC0, licensed, credited), muted by default, with an always-reachable toggle, preference saved in localStorage. **(MUST, light)**
- 6.2 WHEN sound is enabled, THE bed SHALL swell in on the "Consult Madame Minou" click; THE SYSTEM SHALL NOT autoplay audio before a user interaction.
- 6.3 THE SYSTEM SHALL NOT play a separate "reveal chime."
- 6.4 IF the Polly read-aloud is built, THE SYSTEM SHALL expose a user-triggered "Hear Madame Minou" button using AWS Polly French neural voice, SHALL NOT autoplay it, and SHALL duck the chanson while she speaks. Her words SHALL always be present as on-screen text regardless. **(STRETCH)**

## 7. Sharing (MUST)

**User story:** As a user, I want to share my cat's reading.

- 7.1 THE SYSTEM SHALL let the user share the card as a downloaded image or via the Web Share API. **(Resolves the "share" blocker: no hosted card, no server storage.)**
- 7.2 THE SYSTEM SHALL NOT require an account or server-side persistence to share.
- 7.3 Outbound links on the card or page SHALL open in a new tab with `rel="noopener noreferrer"`.

## 8. Care disclaimer + red-flag path (MUST)

**User story:** As an owner, I should never mistake whimsy for veterinary advice.

- 8.1 THE SYSTEM SHALL display the care line in Madame Minou's voice ("Madame Minou reads stars, not bloodwork...") on the About page AND on every behavior-read output, never buried.
- 8.2 WHEN a behavior log contains a red-flag keyword (not eating, not urinating, repeated vomiting, lethargy, labored breathing), THE SYSTEM SHALL surface the vet-care line and SHALL NOT frame the behavior astrologically. **(MUST-light, deterministic keyword scan.)**
- 8.3 THE red-flag keyword list SHALL be a maintained, documented constant.

## 9. Behavior reads + freemium gating (MUST)

**User story:** As an owner, I want to ask Madame Minou about specific behaviors, with a fair free limit.

- 9.1 WHEN the owner logs a behavior, THE SYSTEM SHALL produce a behavior read card cross-referencing current transits against the natal chart (subject to section 8).
- 9.2 THE SYSTEM SHALL show a friendly free-tier counter in localStorage ("X of 3 free reads left today").
- 9.3 THE SYSTEM SHALL enforce the real limit server-side (per-IP rate limit) on the inference endpoint, because localStorage is UX only and cannot protect spend. **(Resolves the wallet-guard blocker.)**
- 9.4 WHEN a free-tier user exceeds the daily read allowance, THE SYSTEM SHALL block the request server-side and present the paywall/upgrade prompt.
- 9.5 THE behavior-log text SHALL be treated as untrusted input (see security 11.3).

## 10. Penelope's memory + About page (MUST)

- 10.1 THE About page SHALL include the Paris origin (link to the dev.to article), the Penelope dedication and tie line, and attribution (Clew Labs, the repo, dev.to, the Madame Steep cross-link).
- 10.2 THE SYSTEM SHALL include a discreet, subdued "In Penelope's memory" acknowledgment linking out to Lap of Love's Angel Fund (https://www.lapoflove.com/angel-fund), verified live, opening in a new tab.
- 10.3 THE SYSTEM SHALL NOT collect donations itself (no payment processing); it only links out.
- 10.4 THE memorial SHALL be subdued and dignified, never a banner.

## 11. Security (MUST: non-negotiable)

- 11.1 THE SYSTEM SHALL keep all credentials and API keys server-side only (IAM role / Secrets Manager / server env), never in client code or the repo.
- 11.2 THE SYSTEM SHALL call the AI model only from a server-side endpoint; the browser SHALL NEVER hold model credentials.
- 11.3 THE SYSTEM SHALL validate and sanitize behavior-log input client-side AND server-side, keep it in the user-content slot only (never concatenated into the system prompt), and cap its length (prompt-injection protection).
- 11.4 THE SYSTEM SHALL serve over HTTPS with tight CORS (own origin only).
- 11.5 THE SYSTEM SHALL wrap every external/API call in try/catch with a meaningful error state.
- 11.6 THE SYSTEM SHALL grant least-privilege IAM (AnthropicInferenceAccess or a scoped policy on the workspace ARN).
- 11.7 THE SYSTEM SHALL produce an Aikido scan report before submission.

## 12. Daily nudge (STRETCH: additive, non-fatal)

**User story:** As an owner, I'd love Madame Minou to check the stars for my cat each morning.

- 12.1 THE daily nudge SHALL be built as an isolated additive layer that does not modify the core localStorage-only flow.
- 12.2 WHEN (and only when) an owner opts in by providing an email, THE SYSTEM SHALL store {email, cat birth data, schedule} server-side for that subscriber only.
- 12.3 WHEN the daily schedule fires, THE SYSTEM SHALL compute current transits, generate the nudge card via the AI layer, and email it; on step failure THE SYSTEM SHALL retry without double-sending (durable execution / Temporal).
- 12.4 IF the daily nudge is not completed in the sprint, THE SYSTEM SHALL present the opt-in as a STUB ("Daily readings, coming soon") and the rest of the app SHALL be unaffected.
- 12.5 THE opt-in email store SHALL follow the same security rules (11.x) and minimize/disclose data.

## 13. Accessibility (MUST, baseline)

- 13.1 THE SYSTEM SHALL provide semantic labels for all inputs and controls (screen-reader usable).
- 13.2 THE SYSTEM SHALL respect `prefers-reduced-motion` for the reveal animation.
- 13.3 THE SYSTEM SHALL maintain sufficient color contrast on the dark café palette.

## 14. Explicitly NEVER (v1)

Accounts/auth, cross-device sync, real payments/subscriptions, live shelter-adoption API (Adopt-a-Minou, parked), multi-cat households, behavior history/trends, push/SMS channels, voice INPUT (dictation). Each may carry a commented stub with notes. See `docs/v2-someday.md`.
