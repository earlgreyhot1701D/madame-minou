# Tasks

## Task 1: Spikes (15-min reality checks)
- [x] 1.1 Compute a known cat's sun + moon from a date with pyswisseph in a standalone Python script; verify correct signs [R3.1, R3.2]
- [x] 1.2 Run `enable-outbound-web-identity-federation`, set workspace + region env, call AnthropicAWS for a one-line styled reading; confirm styled text returned [R4.2, R11.2]
- [x] 1.3 Feed a structured facts object into the persona system prompt; confirm the reading is specific to those facts, not generic horoscope [R2.1, R2.3]
- [x] 1.4 Deploy a hello-world Lambda + static page on the chosen AWS path; confirm reachable URL (fall back to Vercel if blocked) [R11.4]

## Task 2: Chart engine {depends: 1}
- [x] 2.1 Implement the deterministic chart function producing the structured facts object with all degradation tiers (full / date_only / estimated / mystery) [R3.1, R3.2, R3.3, R3.5, R3.7]
- [x] 2.2 Implement noon-UTC default timezone assumption and record `tz_assumption` in the facts object [R3.6]
- [x] 2.3 Implement moon-cusp detection for ambiguous moon sign days, and set rising to null when time/location absent [R3.4, R3.2, R3.3]
- [x] 2.4 Write unit tests for each degradation tier (full / date_only / estimated / mystery) using known fixtures [R3.1, R3.7] {depends: 2.1, 2.2, 2.3}

## Task 3: AI reading layer {depends: 2}
- [x] 3.1 Author the single reusable Madame Minou system prompt (persona voice for natal, behavior, and nudge readings) [R2.1, R2.3]
- [ ] 3.2 Implement the server endpoint: receive facts object, call AnthropicAWS with persona prompt + facts as user content, return reading_text; model never alters facts [R4.2, R4.3, R11.2]
- [ ] 3.3 Implement try/catch with in-voice error state ("Madame Minou's crystal ball is cloudy") on AI call failure or timeout [R4.5, R11.5]
- [ ] 3.4 Build with a mock AI response first to validate the data flow, then wire the real AnthropicAWS call [R4.2] {depends: 3.1, 3.2}

## Task 4: Cafe-terrace UI + intake + reveal {depends: 3}
- [ ] 4.1 Build the cafe-terrace-at-night landing page with the single "Consult Madame Minou" CTA (original art in Van Gogh idiom) [R1.1, R5.1]
- [ ] 4.2 Build the one-question-at-a-time consultation flow (name, then date) with reliable accessible date input and unknown-birthday path [R1.2, R1.3, R1.4, R1.5, R1.6]
- [ ] 4.3 Build the reveal sequence: anticipation beat animation covering AI latency, card flourish on response; respect prefers-reduced-motion [R5.2, R5.3, R5.4, R13.2] {depends: 4.1, 4.2}
- [ ] 4.4 Build the single card renderer component (one component rendering natal, behavior, and nudge reads) [R4.1, R4.4]
- [ ] 4.5 Build the progressive "go deeper" offer for birth time/location after the first reading [R1.7] {depends: 4.3, 4.4}

## Task 5: Sharing + sound {depends: 4}
- [ ] 5.1 Implement card-to-image rendering (html-to-image/canvas) with download and Web Share API; no server storage required [R7.1, R7.2]
- [ ] 5.2 Ensure all outbound links open in a new tab with `rel="noopener noreferrer"` [R7.3]
- [ ] 5.3 Implement opt-in French-chanson ambient audio bed: muted by default, always-reachable toggle, localStorage preference, swell on consult click, no separate chime [R6.1, R6.2, R6.3]

## Task 6: Behavior reads + care disclaimer + freemium {depends: 4, 3}
- [ ] 6.1 Build behavior-log input with client-side + server-side validation, length cap, kept in user-content slot only (never system prompt) [R9.5, R11.3]
- [ ] 6.2 Implement behavior read card cross-referencing current transits against natal chart [R9.1] {depends: 6.1}
- [ ] 6.3 Implement deterministic red-flag keyword scan; surface vet-care line and suppress astrological framing when triggered [R8.2, R8.3] {depends: 6.1}
  - [ ] 6.3.1 Red-flag keyword scan MUST be deterministic code (not LLM): scan behavior text for exact keywords (not eating, not urinating, repeated vomiting, lethargy, labored breathing); on hit, EITHER short-circuit the LLM call and return the plain vet-care line directly, OR pass red_flag=true into the user content so the prompt's care-path instruction activates. Do NOT rely on the model to notice keywords. [R8.2, R8.3] {depends: 6.1}
- [ ] 6.4 Display persistent care disclaimer on About page and on every behavior read output [R8.1] {depends: 6.2, 6.3}
- [ ] 6.5 Implement localStorage free-read counter (UX) + server-side per-IP rate limit enforcing daily allowance with paywall/upgrade prompt on exceed [R9.2, R9.3, R9.4] {depends: 6.2}

## Task 7: Penelope's memory + About page {depends: 4}
- [ ] 7.1 Build About page with Paris origin (dev.to link), Penelope dedication + tie line, and attribution (Clew Labs, repo, dev.to, Madame Steep cross-link) [R10.1]
- [ ] 7.2 Add discreet "In Penelope's memory" acknowledgment linking to Lap of Love Angel Fund (verified live, new tab, no donation collection) [R10.2, R10.3, R10.4]
- [ ] 7.3 Seed the landing with Penelope's own origin reading as a demo [R10.1] {depends: 7.1}

## Task 8: Security hardening + docs {depends: 5, 6, 7}
- [ ] 8.1 Confirm all credentials and API keys are server-side only (IAM role / Secrets Manager); verify least-privilege IAM policy [R11.1, R11.2, R11.6]
- [ ] 8.2 Configure HTTPS with tight CORS (own origin only) [R11.4]
- [ ] 8.3 Run the Aikido security scan and capture the report [R11.7] {depends: 8.1, 8.2}
- [ ] 8.4 Write README + architecture overview + setup instructions + security report [R11.7] {depends: 8.3}
- [ ] 8.5 Record the <5 min demo video: live loop walkthrough, architecture, durable execution, Aikido scan, prompt-injection protection, welfare impact, Penelope dedication {depends: 8.4}

## Task 9: Daily nudge (STRETCH, isolated) {depends: 3, 4}
- [ ] 9.1 Build opt-in email form; on opt-in store {email, cat_facts, schedule} server-side for subscriber only [R12.1, R12.2]
- [ ] 9.2 Implement Temporal/durable daily workflow: compute transits, generate AI nudge card, send via SES email; retry without double-send [R12.3] {depends: 9.1}
- [ ] 9.3 If unfinished by deadline, render opt-in as STUB ("Daily readings, coming soon") and confirm core app is unaffected [R12.4] {depends: 9.1}


## Task 10: Deploy pipeline (live URL) {depends: 1}
- [ ] 10.1 Stand up S3 + CloudFront (or Amplify Hosting) with the hello-world from the Block 0 deploy spike; confirm live HTTPS URL [R11.4]
- [ ] 10.2 Deploy the chart engine + AI reading Lambda behind API Gateway; confirm the /reading endpoint responds [R4.2, R11.2] {depends: 2, 3}
- [ ] 10.3 Deploy the full frontend (cafe-terrace UI + intake + reveal) pointing at the live Lambda; confirm the core consultation loop works end-to-end at the public URL [R1.1, R5.1] {depends: 4}
- [ ] 10.4 Redeploy after behavior reads + sharing are wired; confirm all features work at the public URL {depends: 5, 6}
- [ ] 10.5 Final pre-judging deploy: all MUST features live, HTTPS, tight CORS, stable through July 8–14 judging window {depends: 8}

## Task 11: UI Restyle Step 0 — spec and steering update {depends: none}
- [x] 11.1 Update design-system.md with restyle tokens (--gradient-gold, --color-constellation, --card-frame) and component specs (Constellation Wash, Crescent Archive card, impasto-gold CTA pill, ghost button, badge, icon buttons) [R5.1, R13.3]
- [x] 11.2 Update steering/ui.md with locked visual world (Constellation Wash surface, Crescent Archive card, impasto-gold CTA hierarchy, one-loud-element rule) [R5.1]
- [x] 11.3 Add docs/ui-restyle-plan.md with block-by-block build order and QA gates [R5.1]

## Task 12: UI Restyle Block A — Constellation Wash background {depends: 11}
- [x] 12.1 Add new restyle tokens to :root in the CSS source (--gradient-gold, --color-constellation, --card-frame) [R5.1, R13.3]
- [x] 12.2 Implement Constellation Wash background layers: base deep-navy gradient (#080C1A to #0A142F), existing .impasto-texture noise at ~3%, one inline SVG with faint gold cat constellation + zodiac glyphs + scattered stars at --color-constellation (~10-14% opacity, biased to edges, pointer-events: none, aria-hidden="true"), one small brighter "wish star" accent in upper area, soft vignette (radial gradient darkening edges) [R5.1, R13.3]
- [x] 12.3 Run Tailwind build (npm run build:css) and inline compiled output into index.html [R5.1]
- [x] 12.4 QA gate PASS/FAIL: body text over the background still hits WCAG AA contrast; no horizontal scroll; reading card stays fully legible; prefers-reduced-motion shows a static version (no shimmer or float); restyle only (no layout, DOM, copy, or JS changes) [R13.2, R13.3]

## Task 13: UI Restyle Block B — buttons, badges, icon buttons, bottom nav {depends: 12}
- [ ] 13.1 Implement primary CTA (.btn-consult): --gradient-gold fill, 3px painterly darker-gold bottom border, soft inner top highlight, amber lamplight glow, ~0.92 opacity rising to 1 on hover, low-opacity gold texture overlay, rounded-full pill shape. One component reused everywhere a primary action appears [R5.1]
- [ ] 13.2 Implement secondary button (.btn-ghost): transparent fill, thin gold outline (~40% starlight-gold), gold text, gentle lamplight glow on hover [R5.1]
- [ ] 13.3 Implement badge (.badge-soon): small chip, gold hairline outline, uppercase micro-label (label-sm), faint star icon. Used for History "soon" and future stubs [R5.1]
- [ ] 13.4 Implement icon buttons (share, sound): circular, gold hairline outline, lamplight glow on hover; disabled state at reduced opacity (~30%); aria-label required [R5.1, R13.1]
- [ ] 13.5 Implement bottom nav: thin gold line icons; active item glows gold with cat glyph; History stays a greyed aria-disabled v2 stub (do not activate) [R5.1]
- [ ] 13.6 Run Tailwind build and inline compiled output [R5.1]
- [ ] 13.7 QA gate PASS/FAIL: exactly one loud CTA per screen, all others visibly quieter; focus-visible rings present on all interactive elements; hover and active states honor prefers-reduced-motion; WCAG AA contrast holds; History nav stays greyed/disabled; restyle only (no layout, DOM, copy, or JS changes); mobile + desktop verified [R5.1, R13.1, R13.2, R13.3]

## Task 14: UI Restyle Block C — Crescent Archive reading card {depends: 13}
- [ ] 14.1 Implement card (.card-reading): semi-transparent midnight-navy (--color-midnight-blue at 80%), backdrop-blur-xl, fine gold frame (--card-frame), restrained painterly corner accents, amber lamplight glow (--shadow-lamplight), subtle .impasto-texture overlay [R5.1, R4.1]
- [ ] 14.2 Add crescent-moon motif: inline SVG, low opacity (~10-14%), behind the text, pointer-events: none, aria-hidden="true". Moon not cat (background carries the cat constellation) [R5.1]
- [ ] 14.3 Implement quote accent: warmed gold hairline along the left border of the reading quote (existing border-l pattern) [R5.1, R4.1]
- [ ] 14.4 Implement bottom icon row: Save, Share, Copy, Favorite, Listen with gold hairline dividers. v1 wiring: Share is live; Listen is a greyed aria-disabled coming-soon stub; Save, Copy, Favorite are styled greyed stubs only (real buttons with aria-label, aria-disabled, "soon" affordance, not wired to behavior) [R5.1, R7.1]
- [ ] 14.5 Run Tailwind build and inline compiled output [R5.1]
- [ ] 14.6 QA gate PASS/FAIL: paragraph text fully legible over the moon motif; gold frame crisp on mobile and desktop; no layout shift versus the current card; live actions (Share) work; stub actions are visibly quiet and non-interactive; care line on behavior reads preserved; AI reading text uses textContent only; restyle only (no layout, DOM, copy, or JS changes) [R4.1, R5.1, R11.3, R13.1, R13.3]
