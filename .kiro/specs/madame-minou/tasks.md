# Madame Minou: Tasks

*Block-by-block build order. Each task traces to a requirement (R#) and has a PASS/FAIL QA gate. Spikes come first (15-min reality checks). Build in order; do not start a block until the previous QA gate passes. The daily nudge is the final isolated STRETCH block.*

*Workflow: Kiro proposes the task, Shara approves, Kiro implements. Explicit "DO NOT refactor other code" guardrail on every task. Mock data first, then wire.*

*Last updated: June 24, 2026*

---

## Block 0: Spikes (do these first, 15 min each, hard pass/fail)

- **S1. Ephemeris spike (R3).** Compute a known cat's sun + moon from a date with pyswisseph in a Python script. PASS = correct signs in under ~30 min of setup. FAIL = library fights you; reassess engine.
- **S2. Claude Platform on AWS spike (R4, build-reference §1).** Run `enable-outbound-web-identity-federation`, set workspace + region env, call `AnthropicAWS` for a one-line styled reading. PASS = styled text back. FAIL = fall back to Bedrock or plain API.
- **S3. AI-voice-specificity spike (R2).** Feed a facts object into the persona prompt; confirm the read is specific to those facts, not generic horoscope mush. PASS = a stranger can tell it was written for THIS chart. FAIL = iterate the prompt before building on it.
- **S4. Deploy spike (design §0).** Stand up a hello-world Lambda + static page on the chosen AWS path. PASS = reachable URL. FAIL = consider Vercel fallback for hosting.

QA gate 0: all four spikes pass (or have a decided fallback) before any feature code.

## Block 1: Chart engine (R3) [MUST]

- 1.1 Implement the deterministic chart function: inputs to the facts object (R3.7), per the degradation tiers (design §3).
- 1.2 Implement the noon-UTC assumption + `tz_assumption` recording (R3.6).
- 1.3 Implement moon-cusp detection (R3.4) and rising = null without time/location (R3.2/3.3).
- 1.4 Unit tests for each tier (full / date_only / estimated / mystery) with known fixtures.

QA gate 1: tests green; facts object matches the contract schema (design §2). One file, one responsibility (no god file).

## Block 2: AI reading layer (R2, R4) [MUST]

- 2.1 Author the Madame Minou system prompt (single reusable persona, R2.3).
- 2.2 Implement the server call: facts -> `AnthropicAWS` -> reading_text; model never alters facts (R4.3).
- 2.3 try/catch + in-voice error state (R4.5, R11.5).
- 2.4 Mock the AI response first to build the layout, then wire the real call.

QA gate 2: a posted facts object returns an in-voice reading; failure path shows the cloudy-crystal-ball state, not a blank screen.

## Block 3: Café-terrace UI + intake + reveal (R1, R5) [MUST]

- 3.1 Build the café-terrace landing with the single "Consult Madame Minou" CTA (R1.1, R5.1).
- 3.2 Build the one-question-at-a-time consultation (name, date), reliable accessible date input, unknown-birthday path (R1.2–1.6).
- 3.3 Build the reveal sequence with the anticipation beat covering latency (R5.2–5.4); respect reduced-motion (R13.2).
- 3.4 Build the card renderer (one component, R4.1).
- 3.5 Progressive "go deeper" offer for time/location after first read (R1.7).

QA gate 3: a full pass from landing to revealed card works on desktop and mobile, with mock then real AI.

## Block 4: Sharing + sound (R6, R7) [MUST, light]

- 4.1 Card-to-image + download / Web Share (R7.1); no server storage.
- 4.2 Outbound links `rel="noopener noreferrer"` (R7.3).
- 4.3 Opt-in chanson bed, muted by default, toggle, localStorage preference, swells on consult click, no chime (R6.1–6.3).

QA gate 4: share produces an image; audio never autoplays and is always mutable.

## Block 5: Behavior reads + care disclaimer + freemium (R8, R9) [MUST]

- 5.1 Behavior-log input with client + server validation, length cap, user-content slot only (R9.5, R11.3).
- 5.2 Behavior read card cross-referencing transits (R9.1).
- 5.3 Deterministic red-flag keyword scan -> plain vet-care line, no astrology framing (R8.2–8.3).
- 5.4 Persistent care line on About + every behavior read (R8.1).
- 5.5 localStorage free counter (R9.2) + server-side per-IP rate limit (R9.3–9.4).

QA gate 5: 4th daily read is blocked server-side; a red-flag keyword reliably triggers the vet line; care line always visible on behavior reads.

## Block 6: Penelope's memory + About page (R10) [MUST]

- 6.1 About page: Paris origin (dev.to link), dedication + tie line, Clew Labs / repo / dev.to / Madame Steep cross-link (R10.1).
- 6.2 Discreet "In Penelope's memory" acknowledgment linking Lap of Love Angel Fund, new tab, no collection (R10.2–10.4).
- 6.3 Demo: seed the landing with Penelope's own reading (her origin reading).

QA gate 6: About reads with dignity; memorial is subdued; all links verified live, open correctly.

## Block 7: Security hardening + docs (R11) [MUST]

- 7.1 Confirm keys server-side only; least-privilege IAM (R11.1–11.6).
- 7.2 HTTPS + tight CORS (R11.4).
- 7.3 Run the Aikido scan; capture the report (R11.7).
- 7.4 Write the README + architecture overview + setup + security report (Documentation 10%).
- 7.5 Record the <5 min demo video: show the live loop, walk the architecture, say "durable execution" / "Aikido scan" / "prompt-injection protection," name the welfare impact, land the Penelope dedication.

QA gate 7: pre-deploy checklist passes; Aikido report attached; README runs for a stranger.

## Block 8: Daily nudge (R12) [STRETCH, isolated, non-fatal]

- 8.1 Opt-in email form; on opt-in, store {email, cat_facts, schedule} (subscribers only, R12.2).
- 8.2 Temporal (or durable) daily workflow: transits -> AI nudge card -> SES email, retry without double-send (R12.3).
- 8.3 If unfinished by the deadline, leave the opt-in as a STUB ("Daily readings, coming soon") (R12.4); confirm core app unaffected.

QA gate 8: either a real daily email sends durably, OR the opt-in is a clean stub and nothing else regressed.

---

## Submission checklist (by July 7, 23:59 BST)

ZIP (under 100MB, with project doc) · demo video (<5 min) · GitHub repo · README + architecture + security report · Aikido scan · Kiro Track opt-in (write-up + `.kiro` folder link) · Lap of Love + dev.to + Clew Labs links live · reference ID noted.
