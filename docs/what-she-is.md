# Madame Minou: What She Already Is

*Capture doc. Not a PRD. Just what we landed on across the Paris conversations, written down so the PRD has a starting point. Product first. The build serves the product, never the other way around.*

*Last updated: June 23, 2026 (hackathon eve)*

---

## The one-line

A daily cat astrology app for people who love their cats and cannot quite figure them out.

## The actual thesis (why this is more than a novelty)

Cats are inscrutable. The people who love them are obsessive about decoding them. There is almost no scientific consensus on cat behavior, even among researchers. Astrology is a culturally accepted, several-thousand-year-old framework for making the unknowable feel readable.

Madame Minou does not sell astrology as truth. She sells it as a *vocabulary* for the gap between cat behavior and human understanding. The astrology is the vocabulary. The structure underneath it is the catnip.

This is the Clew thread in a different coat: take something invisible and make it inspectable. Cat behavior is the most invisible signal in the home. Astrology is the inspection layer. The fact that the inspection layer is absurd is the joke. The scaffolding under it (daily nudge, behavior log, owner peace of mind) is real.

## Who it's for

Cat owners who feel the "is this normal??" 2am Google spiral. People fanatical about their cats' behavior with no insight into it. Not built for me (I'm allergic, not a cat person). Built for the cat people, which is the point: the outsider builds the decoder.

## The core loop (the thing that has to work)

1. Owner enters the cat's birth data (date, time, location) once. This earns the natal chart.
2. System produces a **daily nudge** tied to actual planetary transits against that natal chart.
3. Owner can **log a behavior** ("spat up food," "won't cuddle," "knocked glass off the table").
4. System cross-references current transits against the natal chart and returns an astrologically framed read.
5. The daily nudge becomes a low-stakes check-in routine.

## One oracle, one card (the unification)

The reading and the daily nudge are not two features. They are the same oracle reaching you two ways: **you pull (consult her on demand) or she pushes (the daily nudge).** Same Madame Minou, same chart, same voice. The nudge is the reading *continued*: you visit the fortune teller once, and then she keeps a candle lit for your cat and watches the sky every morning. That continuity is the relationship and the retention hook. She doesn't forget your cat after one visit.

**The card is the atomic unit of everything she does.** The first natal reading is a card. A behavior question returns a card. The daily nudge that lands in the inbox is a card. One renderer, three triggers, every card shareable. You are not building a reading feature plus a nudge feature plus a share feature. You are building *Madame Minou hands you a card*, then deciding what made her hand it over. (This also settles the earlier open question: there is no "just a read." Everything is the card.)

## The reveal (the ritual, not a page load)

1. Finish the consultation, click *Consult Madame Minou*.
2. The chanson swells in. Curtain up.
3. A beat of anticipation: Madame Minou at her café table under the swirling stars, beret on, eyes lifting to read the sky. This pause IS the séance, and it conveniently hides the second or two the AI takes to write the reading. Latency becomes theater, never a spinner.
4. The card is revealed with a flourish (a flip, a slide, a curtain-wipe on the card itself).
5. The share button lives on the card. The next morning, that same card format arrives as the daily nudge. Same ritual, smaller, every day.

The "theater" is the reveal *motion*, not a separate red-velvet room. The set is the café terrace at night.

## The deterministic spine vs the AI flavor (the architecture principle)

- **Deterministic:** birth chart math. Date, time, location to sun/moon/rising and planetary positions, from real ephemeris data. This is the earned, honest layer. Same role `symbols.js` played in Steep. Determinism is the differentiator.
- **AI flavor:** the daily nudge copy and the behavior reads. The voice is the product. "Why is your cat hiding today? Saturn is squaring her natal Venus. Tuxedos with Capricorn moons need 48 hours of low-stimulation recovery after houseguests."

Structure is deterministic. Flavor is AI-generated. Never the reverse.

## The persona (LOCKED: Madame Minou IS Penelope)

Madame Minou. French cat astrologer in a **beret**. *Madame* for the fortuneteller-reading-the-stars persona, *Minou* because it's the French diminutive for cat and it's warm. A little sister to Madame Steep (the persona that reads tea leaves over your GitHub repo). Light franglais: "Ma chérie, your Bombay's Mars is in chaos today."

**The identity, decided:** Madame Minou *is* Penelope. "Madame Minou" is her stage name, her oracle act. Penelope is the soul underneath, the real tuxedo, the dedication. One cat, two names. The beret is the costume that signals she's the astrologer now.

This keeps the voice sustainable. "Madame Minou" is the light, playful register you can write thousands of daily reads in, and Penelope is the truth under the act that you only feel when you go looking. You get the brand and the gut-punch without grief crushing the daily voice.

The demo reading on the landing page is **her own origin reading**: before she read the whole world, Madame Minou read herself. The cat who could never be understood became the one who understands.

## Visual identity, mascot, vibe (LOCKED)

- **Mascot:** one tuxedo cat, two names. Penelope (the soul, the dedication) performing as Madame Minou (the oracle), signalled by the **beret**. Locked. The dedication cat is the face of the app, the narrator, and the demo reading, all at once.
- **Vibe:** surreal, dreamlike, a little philosophical. The wink is **"Are cats even real?"** Astrology asks the unanswerable, the art leans into it.
- **Visual reference:** the starry-night Paris cover (tuxedo cat on a rooftop, zodiac constellations in a swirling sky, Eiffel Tower, the Seine). Rich blues and golds, painterly, otherworldly.
- **Visual world (DECIDED): the café terrace at night.** Post-Impressionist, Van Gogh *Café Terrace at Night* idiom. This resolves everything: Madame Minou reads at a **café table on the terrace**, warm yellow awning glow around her, the starry zodiac sky overhead, cobblestones underfoot. The "table" the reading needs is a café table. No red-curtain theater (different palette, would split the identity). The earlier painterly-vs-surreal question is settled: painterly café-night with surreal touches (zodiac woven into the stars, "Are cats even real?").
- **Copyright note:** Van Gogh's actual paintings are public domain (died 1890, far past life+70), so the *style* and his real works are free to draw on. But do NOT lift a specific modern reproduction (e.g. the café image in chat is signed by a contemporary artist and dated 1994, so it carries its own copyright). Clean path, same as the original cover: generate ORIGINAL art in the café-terrace-at-night idiom. Style is free, a living artist's specific painting is not. Airtight for the app, cover, and demo video.

## The landing page (the first three seconds)

The art makes the pitch before the copy does, so the hero is the single strongest asset to build: the starry-night Penelope rooftop, the zodiac sky, the line **"Are cats even real?"**

- **One loud call to action:** *Consult Madame Minou* (with *s'il vous plaît* as the franglais grace note). Everything else on the screen stays quiet. Spelling note: it's *s'il vous plaît* if it goes on screen.
- **Seed the page with a live sample reading** so a visitor *gets it* before typing anything. Show, don't tell. That one reading is the whole product in miniature and it's exactly what a judge sees before deciding to care. Proposed demo cat: **Penelope herself.** The mascot demonstrates the product, it's hardcoded so it never goes stale, and it folds a quiet tribute into the most-viewed pixel on the site. (Alt: a neutral demo cat if Penelope should stay only in the dedication.)
- **Friction is the enemy.** Cat name + birthday to get a reading. Time-of-birth optional (nobody knows their cat's). No account for the free read. Arrive, laugh, then decide to go deeper.

## Sound (skeleton, opt-in)

The visuals pop, and silence under them feels like "why." So sound earns its place, done with restraint.

- **The vibe:** French chanson / musette / accordion, that Parisian ache. Piaf-*adjacent*.
- **Piaf herself is OFF the table (copyright).** Not public domain. Her hits were written by composers who outlived her by decades (*La Vie en rose* music by Louiguy, d.1991, published by Universal/Sony; *Non, je ne regrette rien* by Charles Dumont, d.2024, locked until ~2094), and the master recordings carry separate long protection. The rules also ban copyrighted music in the demo video. The *feeling* is a genre, not a copyright.
- **Source:** royalty-free / CC0 "French café" or accordion track, or AI-generated in that style with the license verified. Own the rights, keep the goosebumps. Credit the source.
- **Trigger:** the bed swells in on the *Consult Madame Minou* click. Browsers block autoplay-with-sound, so the click is the honest trigger, and it doubles as the curtain going up. **No reveal chime** (it reads as a notification ding shouting "look at me"). The music itself carries the reveal: the accordion breathing under Madame Minou's verdict *is* the magic.
- **Respect:** always-reachable mute toggle, quiet/off by default, preference saved in localStorage so a returning visitor isn't ambushed.
- **Madame's spoken voice (Polly, optional, opt-in):** she can read a reading aloud via AWS Polly's French neural voice (real accent, on the AWS stack, accessibility bonus). It is a user-triggered **"Hear Madame Minou"** button, NEVER autoplay. When tapped it ducks/pauses the chanson so the two never fight: ambient music by default, spoken voice on demand, music steps back after. Use Polly French neural ONLY; browser SpeechSynthesis is robotic and breaks the spell. Her words are ALWAYS on screen as text (the card / speech bubble), so Polly is additive audio, never the only channel. If Polly never ships, nothing is lost. MUST-light or STUB.
- **Voice INPUT is v2.** The user dictating answers (especially the birthday) is a parsing trap and a browser-support gamble. Keep the reliable typed intake. Revisit in v2.
- **Scope:** one looping bed is the skeleton. UX/UI score (15%). Light MUST or STUB depending on the hours.

## Intake (the consultation, not a form)

Madame Minou is a fortune teller, and fortune tellers don't hand you a form, they ask you things. So the intake is a **consultation**, one question at a time, in her voice. The art is on screen, the chanson swells, the consultation IS the experience, not a gate before it.

- **Minimum first:** name, then birthday. That's enough for the first reading. Get them to the payoff fast.
  - *"Asseyez-vous. Madame Minou will read your creature. First, what do they call this little beast?"* (name)
  - *"Biscuit. Bien sûr. And when did Biscuit descend upon this earth?"* (birthday)
- **The "I don't know her birthday" path is first-class, not an error.** Rescues and strays have no known DOB. A soft out beside the date: *"She's a mystery to me too"* leads to best guess or gotcha day, and Madame Minou shrugs: *"Mystery cat, mystery stars. We read what we have."* Same fallback as the shelter cats. One idea, two problems solved.
- **Progressive disclosure:** after the first reading delights them, OFFER the deeper cut: *"You want more, chérie? Tell me the city where it began, and the hour, and I will go deeper."* Birth time and location enrich the chart, but nobody knows their cat's birth hour, so never front-load them as required.
- **Guardrail:** keep the actual date input boringly reliable. The magic is the framing and her voice, NOT a hand-rolled spinning calendar. Custom date pickers are a time-sink and an accessibility trap. Clean styled input, real labels underneath for screen readers. Theater on top, solid plumbing underneath.

## The shareable card (core output, almost always)

Madame Minou should produce a **shareable card**, the same pattern as the other builds. It's the thing people screenshot and post, which is the organic growth loop and a UX/UI scoring surface. Cat people share cat content compulsively, so this is doing real work, not decoration.

**Open question (real work, for the PRD):** how many card styles in v1? One clean style done well, or a small set (e.g. 4) the user picks from. More styles = more design and template time, which competes with the core loop for hackathon hours. Decide the count deliberately. One polished card beats four rushed ones.

## In Penelope's memory (a quiet acknowledgment, NOT the focus)

The build is personal pet astrology. That's the headline and the MUST line. This is a **discreet, subdued** grace note, not a campaign. (Replaces the earlier Adopt-a-Minou idea, now parked in v2.)

The why: Penelope was able to pass peacefully at home because of in-home hospice / end-of-life care. So Madame Minou, the app that helps you understand your cat across her whole life, gently acknowledges the end of it too, in Penelope's memory. A truer center than shelter adoption, because it ties to the cat who is already the soul of the app. It closes the loop instead of adding a side quest.

- **Tone: subdued, dignified, a tribute, not a fundraiser.** Lives quietly near the About page and the dedication. Never a loud DONATE banner. "Very subdued, but there."
- **Link out, do NOT collect.** Do not be a money intermediary. v1 has no payment processing (stubbed), and collecting donations yourself raises tax, trust, and liability questions that don't belong near something this tender. Link to a reputable in-home pet hospice / end-of-life org (or the actual service that cared for Penelope) so people give directly to them. Cleaner, more honest, lower risk, Occam-friendly.
- **Dead-link guard applies.** Link a stable org page, verified live. Open in a new tab (`rel="noopener noreferrer"`).
- **Recipient: Lap of Love (LOCKED, verified live June 24, 2026).** National in-home pet hospice, euthanasia, and pet-loss support ([lapoflove.com](https://www.lapoflove.com/)). Primary giving link: their **Angel Fund** ([lapoflove.com/angel-fund](https://www.lapoflove.com/angel-fund)), which helps families afford end-of-life care, by linking, never collecting. Secondary resource link (optional): **Find a Vet** ([lapoflove.com/find-a-vet](https://www.lapoflove.com/find-a-vet)) for an owner facing this right now.
- **Open question (for the PRD):** placement only (a quiet line on the About page near the dedication, vs a small dedicated tribute panel). Recipient and link resolved.

## Delivery and freemium gating

- **Delivery channel:** email for the daily nudge (cheap, no app install, natural for a daily habit). Push/SMS are later channels, not v1.
- **Cost shape (aim the gate correctly):** the daily nudge is one small LLM call per cat per day, cheap and predictable. The on-demand behavior reads are the unbounded, expensive surface (a fanatical owner can log forty things before lunch). So **gate the reads, not the nudge.** The nudge is the free habit hook. The reads are where cost scales with use and where heavy users will happily pay.
- **Free tier:** localStorage only. No accounts. Privacy-clean, account-free, cheap. Counter shown to the user ("X of 3 free reads left today").
- **Important honesty:** localStorage is the *friendly counter*, not the wallet guard. The LLM call is server-side, so the real cost ceiling is a **server-side rate limit** (IP-based when there are no accounts: API Gateway throttling, WAF rate rule, or a Lambda counter). For the live demo a basic rate limit leans **MUST** so a judge hitting a live endpoint can't drain the account. IP is leaky (shared NAT, VPN) and is personal data under GDPR (England/Wales governing law), so minimize and note it in the security report.
- **Premium = cross-device:** using Madame Minou across multiple devices needs real accounts (localStorage is single-device by nature). That whole tier is **STUBBED** for the hackathon: show the paywall moment, comment-stub the payment and the account/sync, document the model. Stub, don't build. No Stripe this week.

## Positive impact frame (this is Theme Relevance, 15% of score)

**The thesis IS the theme anchor, and it's not a stretch.** The theme page names a "For cat owners" bucket explicitly: "cat behaviour decoders... tools that help humans be better cat servants." Madame Minou is a cat behavior decoder wearing an astrology costume. That maps directly onto a named bucket, so personal pet astrology is squarely on-theme, not a surface mention.

The real impact, plainly and without overclaiming: reduces owner anxiety by giving language to ambiguous behavior, and encourages owners to *observe their cats more carefully*, which is genuinely good for catching real health issues early. The daily nudge is a low-stakes check-in habit. The 2am "is this normal??" spiral gets a framework instead of a void. Limitations language is a feature, not a weakness.

**The thesis carries the theme on its own; the memorial is a grace note, not the anchor.** The owner-facing behavior-decoder thesis is the named-bucket fit that secures Theme Relevance. The quiet in-Penelope's-memory acknowledgment (in-home hospice / end-of-life care) is a tender grace note on top, not a scale-impact claim. Honest note: the old Adopt-a-Minou was more judge-legible "impact at scale," but the thesis already secures the category, and the authenticity and coherence here are worth more to this build.

**The requirement (drift guard):** the relevance must be *visible and intentional*, not just true in the founder's head. Foreground the decoder loop and name the welfare impact on screen, in the demo, and in the README. A judge pattern-matches "astrology" to "novelty" unless you show the substance and say the impact out loud. Depth of integration is exactly what the category rewards.

## Limitations and the care disclaimer (NAMED guard)

Madame Minou is a delight, not a diagnosis. She reads stars, not bloodwork. This has to be explicit, in her voice, so no anxious owner ever reads "Mercury retrograde" and skips a real problem. The charm is exactly why the disclaimer is non-negotiable.

- **In-voice line (persistent, light):** *"Madame Minou reads stars, not bloodwork. If your creature is truly unwell, see a vet, mon chéri, not a mystic."*
- **Where it shows:** quietly on the About page AND on every behavior-read output (the spot an owner is most likely to be asking "is this normal?"). Never buried.
- **Why it matters:** user wellbeing first (some logged behaviors are real red flags), it strengthens the responsible-handling / ethics story for Security, and it's pure on-brand honesty (limitations language is a feature).
- **Optional thoughtful upgrade (deterministic, fits the spine):** scan the logged behavior for a few genuine red-flag keywords (not eating, repeated vomiting, not urinating, lethargy, labored breathing). On a hit, Madame Minou drops the act just enough to care: *"This one is for a vet, not the stars, ma chérie. Please don't wait."* Welfare + theme depth + responsible-handling in one small check. A not-peeing cat is a true emergency. MUST-light or STUB, your call.

## The dedication

In memory of Ms. Penelope Randall. May 2009 to February 17, 2026. Tuxedo. Frenemy. The reason this build exists. Goes quiet at the bottom of the README / about page. The build has a center of gravity: the tool I wish had existed to understand one specific, inscrutable cat.

The line that ties it together: **Madame Minou is, and always was, Penelope.**

## The About page (the room behind the curtain)

Front of house is pure Madame Minou. The About page is where the real story and the maker live, so the reading experience stays uncluttered.

- **The Paris origin,** linked to the dev.to article *Do Devs Dream of Électrique Chats?* It documents the build being born, and doubles as proof the idea predates the code (on the right side of the no-pre-written-code rule).
- **Penelope's dedication** and the tie line, quietly: *Madame Minou is, and always was, Penelope.*
- **Attribution / clout:** Clew Labs, the GitHub repo, the dev.to profile, and the *AI Assisted. Human Approved. Powered by NLP.* signature. **Cross-link to Madame Steep** (the sister persona): buys coherence as well as clout, because it shows a persona family, not a one-off.
- **How it works + limitations (light):** deterministic chart + AI voice, and the named care line in her voice: *Madame Minou reads stars, not bloodwork.* (See the Limitations and care disclaimer guard.) On-brand honesty that also strengthens the responsible-handling story.
- **Built-with credits:** Temporal, Aikido, AWS/Kiro (good documentation and good manners; can also live in the README).
- **Conscious tradeoff:** linking Clew Labs / dev.to / GitHub opts OUT of judging anonymity (which the rules make optional). Chosen on purpose, for the build-in-public clout.

## Where she lives

Undecided, on purpose. The product defines the requirements, the requirements pick the stack. Not the reverse. Leaning standalone (her own URL, persona family with Steep but not under it, not inside the Clew dev-tools suite since she's consumer-facing). Decided only when a real requirement forces it.

---

## Sponsor tech, thoughtfully (not bolted on)

### Temporal (durable execution): strong, genuine fit

The daily nudge is literally a recurring, scheduled, multi-step workflow, which is exactly what Temporal is for. The chain is: daily schedule fires, compute current transits, cross-reference the cat's natal chart, call the LLM for the nudge copy, deliver by email. If the LLM call fails or times out, Temporal retries that step without re-running the whole chain or double-sending a nudge. The behavior-read flow is the same shape on demand.

This isn't decoration. "A daily check-in that reliably shows up and never double-sends" is a durability requirement, and durable execution is the honest answer to it. Rubric note: Technical Execution (25%) explicitly nods to durable execution and names Temporal.

**Open question for the PRD:** is the daily nudge a MUST or a STUB for the 14-day window? That decision determines whether Temporal is in the v1 build or a documented stub with implementation notes.

### Aikido (security scan): easy points, and we'd do it anyway

Run an Aikido scan on the repo for the bonus and the Security category (15%). It covers dependency scanning, SAST, and secret detection, which maps onto the existing pre-deploy checklist. Responsible data handling angle: the app holds cat birth data, owner-entered behavior logs, and (if rate-limiting) IP addresses. Low sensitivity, but still user data, so minimize collection and keep keys server-side.

The real security story worth flagging: **behavior logs are free text that get fed to an LLM.** That's a live prompt-injection surface. Input validation client-side and server-side, plus prompt-injection protection, is already item 11 on the pre-deploy checklist. Madame Minou makes it concrete. That's a genuine security narrative for the report, not a checkbox.

---

## Tooling reality (tool longevity + the credit situation)

- **Kiro from day one (June 24).** 2000 free Kiro participation credits for this build, plus Kiro Pro already held from a previous win. No waiting until July 1, no Antigravity-first phase required. Kiro is the executor from the first commit. (Antigravity stays available as an optional fallback if Kiro ever stalls.)
- **Spec-driven from the start.** The spec set lives in the repo's `.kiro/` folder (specs + steering), Kiro's native format, so Kiro builds from it directly.
- **Kiro Track opt-in: YES.** Building with Kiro the whole way makes the separate Kiro Track prizes a definite claim: a short write-up of how Kiro was used + the `.kiro` folder link on the submission form.
- **Longevity check (still do it in the spikes):** confirm Kiro current status, the Claude Platform on AWS beta SDK versions, and Swiss Ephemeris (pyswisseph) last release before locking.

## AI provider: Claude on AWS (verified June 2026)

Three ways to call Claude on AWS, which pins the "model not specified" gap:

- **Claude Platform on AWS** (GA May 11, 2026): the *native* Claude API (full feature set: Skills, MCP connector, prompt caching, citations, batch), authenticated with AWS IAM and billed through your AWS account. Anthropic operates it; data is processed outside the AWS boundary. Newest models land here same-day.
- **Amazon Bedrock:** Claude *inside* AWS infrastructure, AWS is the data processor (data stays in AWS, not shared with Anthropic), via Bedrock's Converse API. The long-standing, heavily documented path the AWS-architect judges know cold. Security edge: "data never leaves AWS."
- **Plain Anthropic API:** the fallback you already know.

**Decision:** try **Claude Platform on AWS** as a day-one SPIKE (15 min, pass/fail: can I get a styled reading back?). Upside: full native Claude DX + AWS billing/IAM + real clout with the AWS/Kiro judges. Risk: it's ~6 weeks old, so fewer examples and possible rough edges. Don't let bleeding-edge eat sprint hours. If the spike fights you, fall back to Bedrock or the plain API. All three are low-risk to swap because the model call is small and isolated behind your server endpoint.

**Model choice (per feature):** a cheap Haiku-class model for the high-volume daily nudge, a stronger Sonnet/Opus-class for the marquee on-demand reads where the voice matters most. Cost couples to the gate-the-reads decision. Pin the exact model in the spike.

**Clarifier:** the IDE (Antigravity, then Kiro) is the coding ASSISTANT. The app's runtime model (Claude via AWS) is a SEPARATE choice. Code in Antigravity, app still calls Claude. No conflict.

---

## Locked vs not decided

**Locked:**
- **The build is personal pet astrology.** That's the headline and the MUST line.
- **Identity: Madame Minou IS Penelope.** One tuxedo, two names. Beret = the oracle costume. Minou is the act, Penelope is the soul. Tie line: "Madame Minou is, and always was, Penelope."
- Primary CTA: *Consult Madame Minou* (s'il vous plaît).
- Landing seeded with Penelope's own reading as the demo (framed as her origin reading).
- Intake is a consultation in Madame Minou's voice (not a form): unknown-birthday path first-class, progressive disclosure, reliable date input underneath.
- In Penelope's memory: a discreet, subdued acknowledgment of in-home pet hospice / end-of-life care, near the About/dedication. Link out to **Lap of Love** (lapoflove.com, primary link their Angel Fund at lapoflove.com/angel-fund), verified live; never collect donations ourselves. NOT the focus. (Replaces Adopt-a-Minou, parked in v2.)
- Mascot: Penelope the tuxedo cat
- Vibe: surreal/dreamlike, "Are cats even real?"
- Visual world: the café terrace at night (Van Gogh idiom, ORIGINAL art, not a copied painting). Madame reads at a café table under the starry zodiac sky.
- Unification: one oracle, one card. Reading = behavior read = daily nudge = a card. You pull or she pushes.
- The reveal is a ritual (chanson swell, anticipation beat as séance, card revealed with a flourish), not a page load.
- Free tier: localStorage only, gate the reads not the nudge
- Premium (cross-device): STUBBED for the hackathon
- Daily nudge delivery: email
- Sound: opt-in French-chanson bed, swells in on the consult click, no chime, mute toggle, default quiet. Piaf ruled out (copyright).
- Madame's spoken voice: optional AWS Polly French neural, on-demand "Hear Madame Minou" button that ducks the chanson, never autoplay. Her words always shown as text regardless. Voice INPUT = v2.
- About page: Paris origin (dev.to link), Penelope dedication, Clew Labs + repo + dev.to + Madame Steep cross-link, light "for delight not a vet" note. Opts out of judging anonymity, by choice.
- Care disclaimer (NAMED guard): "Madame Minou reads stars, not bloodwork." Shown on About + every behavior read, never buried. Optional deterministic red-flag keyword nudge to see a vet.
- Dedication: Penelope, at the bottom
- Scope: lean polished MVP is the MUST; the daily nudge is a STRETCH (additive opt-in layer, non-fatal if unfinished)
- Stack: all-in AWS (S3/CloudFront or Amplify frontend, Lambda server, Claude Platform on AWS); day-one deploy spike
- Engine: Python + Swiss Ephemeris (pyswisseph) for the deterministic chart
- Build tool: Kiro from day one (2000 free credits + Kiro Pro); spec-driven, `.kiro/` in the repo; Kiro Track opt-in YES

**Not decided yet (for the PRD session):**
- MVP scope / the MUST line (lean polished MVP vs full working loop)
- Stack (AWS vs Vercel vs hybrid): waits for requirements
- Whether the behavior log persists (MUST) or is stubbed (STUB)
- Whether the daily nudge ships in v1 (pulls Temporal in) or is stubbed
- Shareable card: how many styles in v1 (1 vs ~4)
- Visual lead lane: starry-night-painterly vs true-surreal
- Is a basic server-side rate limit a MUST for the live demo (leaning yes)
- Final name lock + where she's hosted

---

## Spec gaps to close in the PRD (the open-questions ledger)

The confusions a coding agent (or Future Shara) hits. Each is one decision. The top four block scaffolding or contradict each other; resolve those first.

**Resolve first (blockers / contradictions):**

1. **Daily-nudge vs localStorage contradiction.** Emailing a daily reading needs a server to know {email, cat birth data, schedule}. localStorage is client-only and accounts are stubbed, so a server can't read it. Decide: daily nudge BUILT in v1 (forces a minimal server-side store + email sender + scheduler/Temporal, and an asterisk on "localStorage only") or STUBBED (show the opt-in, don't send). Leaning STUB for v1.
2. **What "share" means.** A shareable LINK needs server storage of the card. A downloaded PNG or Web Share API hand-off does not. Decide: downloaded image (localStorage-friendly) or hosted shareable URL (needs storage). Leaning download / Web Share for v1.
3. **Chart degradation rules.** Rising sign is impossible without birth time + location; moon sign is ambiguous on sign-change days; sun sign is fine from date. Define exactly what the engine computes for (a) full data, (b) date only, (c) estimated year only, (d) total mystery. The "mystery cat" path needs a spec, not vibes.
4. **Deterministic-to-AI contract.** Define the structured object the chart engine emits (e.g. `{sun, moon, rising?, notable_transit}`) and the prompt template that consumes it as FACTS to flavor. Without this, the LLM invents the astrology and the determinism differentiator dies.

**Resolve before coding the relevant piece:**

5. **Model + provider** (mostly resolved: Claude Platform on AWS pending the spike; cheap model for nudges, stronger for reads; see AI provider section).
6. **Rate-limit enforcement.** Which is the real gate (server-side IP) vs the friendly counter (localStorage), and WHERE the server counter lives (KV store, etc.). Mechanism, not just intent.
7. **Stack.** Hosting + runtime + framework + language. Couples to the ephemeris library (Python Swiss Ephemeris vs a JS chart lib). Can't scaffold without it.
8. **Adopt-a-Minou data schema + sourcing.** Define the JSON shape; flag that the 5 to 8 real cats, photos (licensing), and stable shelter URLs are human-provided content, not agent-inventable.

**Small but will bite:**

9. **Timezone assumption** for the birthday when time/location absent (e.g. default noon UTC). Affects cusp sun/moon signs and reproducibility.
10. **Error + slow states** for a failed or 8-second reading. Your rule: meaningful error states, never blank screens. The reveal animation must handle a late or failed response.
11. **Red-flag override spec.** The keyword list and the rule for WHEN Madame breaks character, or it never fires / misfires.
12. **Card rendering tech.** DOM element vs generated image (satori / @vercel/og / html-to-image). Decides how "share" and the daily email card are produced.

**Umbrella:** assign MUST / STUB / NEVER to every line in the Locked list. That's what tells the agent what to build vs stub.

## Scoring guardrails (the judge lens, as requirements)

The build can't drift if every rubric category has a concrete requirement and a "don't let this slip" guard. This is the judge's-eye view turned into acceptance criteria. The panel skews technical: an Aikido pentest lead, a Temporal dev advocate, two AWS/Kiro architects, a robotics+fullstack analyst, an AI/accessible-UX engineer. Judges may NOT run the code.

**Technical Execution (25%).** Requirement: the deterministic chart engine is real (honest ephemeris math), the AI is a flavor layer, and the daily nudge is a durable workflow (Temporal) or a documented stub with implementation notes. Guard: never let it collapse into a single LLM-prompt wrapper. Show the architecture in the video.

**Innovation & Creativity (20%).** Requirement: the human direction is visible (Penelope-as-Madame-Minou, the one-oracle-one-card unification, the behavior-decoder-via-astrology frame). State the novel idea plainly. Guard: the rules dock work that reads as all-AI-no-direction. Name the decisions you made.

**Theme Relevance (15%).** Requirement: foreground the cat-behavior-decoder thesis (a named theme bucket) and say the welfare impact out loud. The theme rests fully on the thesis now (the in-Penelope's-memory acknowledgment is a grace note, not the anchor). Guard: don't let the connection live only in your head; state the decoder/welfare impact explicitly in the demo and README.

**Security (15%).** Requirement: Aikido scan report included; prompt-injection protection on behavior logs (client + server validation); keys server-side; IP rate limit as the wallet guard; minimize and disclose IP/data. Guard: never ship the LLM endpoint unguarded or keys client-side.

**UX/UI (15%).** Requirement: the café-terrace world, the reveal ritual, low-friction consultation, accessible date input with real labels, sound muted by default. Guard: never sacrifice the working loop for art. Theater on top, solid plumbing underneath.

**Documentation (10%).** Requirement: clean README + architecture overview + setup instructions + security report + the project story. Guard: write it like a stranger must run it without asking you a single question.

**The demo video (cross-cutting, since judges may not run it).** Requirement: under 5 minutes, SHOW the loop live (intake, reveal, card, the nudge arriving), walk the architecture, say "durable execution," "Aikido scan," and "prompt-injection protection" out loud (two judges' whole jobs are those words), show one real adoptable cat, and land the Penelope dedication at the end. Guard: not a reel of static mockups.

---

## Rubric this maps to (for reference)

Technical Execution 25 · Innovation & Creativity 20 · Theme Relevance 15 · Security 15 · UX/UI 15 · Documentation 10. Judges may not run the code, so the demo video and README may carry the whole thing.
