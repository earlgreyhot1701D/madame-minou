# Madame Minou: Design

*Technical design for the requirements. Architecture, the deterministic-to-AI contract, data flow, and how each of the four spec-gap blockers is resolved.*

*Last updated: June 24, 2026*

---

## 0. Stack decision (LOCKED)

**All-in AWS** (LOCKED). Chosen because the chart engine is Python (natural Lambda fit), the exploration goal is AWS, and the judging panel is AWS-heavy.

- **Frontend:** static site (HTML/CSS/JS or a light framework) on **S3 + CloudFront**, or **Amplify Hosting** for push-to-deploy.
- **Server endpoints:** **AWS Lambda** (Python) behind **API Gateway**. Two endpoints in v1: `POST /reading` (natal) and `POST /behavior` (behavior read).
- **Chart engine:** Python + **Swiss Ephemeris (pyswisseph)** inside the Lambda.
- **AI layer:** **Claude Platform on AWS** (`AnthropicAWS` client). See `docs/build-reference.md` section 1 for auth, base URL, model IDs, and the federation gotcha.
- **Voice (STRETCH):** **AWS Polly** French neural voice.

**Risk + mitigation:** AWS plumbing (IAM, federation, deploy) can eat hours. Day-one deploy spike with a hard pass/fail (see tasks.md) before committing. If it fights, fall back to Vercel for hosting + serverless while keeping Claude Platform on AWS for the model.

---

## 1. High-level architecture

```
Browser (café-terrace UI, localStorage)
  | "Consult Madame Minou"
  v
API Gateway  ->  Lambda (Python)
                   |  1. validate + sanitize input
                   |  2. chart engine (pyswisseph) -> facts object   [DETERMINISTIC]
                   |  3. AnthropicAWS.messages.create(system=persona, content=facts)  [AI VOICE]
                   |  4. return { facts, reading_text }
                   v
                 per-IP rate limit (wallet guard)
                   |
                 Claude Platform on AWS  (server-side creds only)

Card renderer (one component) <- reading_text + facts
  -> share via download / Web Share API (no server storage)
```

The deterministic step always runs and is cheap. The AI step is the only paid, variable-latency step, and it is isolated behind the server endpoint.

## 2. The deterministic-to-AI contract (the core boundary)

The chart engine emits a structured **facts object**. The AI layer receives it as user content and writes voice over it. The model is instructed never to invent or change positions.

```json
{
  "cat_name": "Biscuit",
  "chart_tier": "estimated",        // "full" | "date_only" | "estimated" | "mystery"
  "sun": "Leo",
  "moon": "Capricorn",              // or null
  "moon_cusp": false,               // true => moon changing sign that day
  "rising": null,                   // null unless birth time + location given
  "notable_transit": "Saturn square natal Venus",
  "tz_assumption": "noon UTC",      // recorded when time/location absent
  "behavior": "won't cuddle"        // present only for behavior reads
}
```

System prompt (persona) = Madame Minou's voice. User content = "Here are the true astrological facts for this cat. Write Madame Minou's reading from THEM. Do not invent or change any positions." This is what keeps determinism as the differentiator (requirement 3.1, 4.3).

## 3. Chart degradation tiers (resolves blocker #3)

| Tier | Inputs known | Computes | Framing |
| --- | --- | --- | --- |
| `full` | date + time + location | sun, moon, rising, transits | full chart |
| `date_only` | date | sun, moon (or cusp), NO rising | "estimated chart" |
| `estimated` | guessed date / gotcha day | sun, moon if derivable | "starlight guesswork" in voice |
| `mystery` | year only / nothing reliable | whatever is derivable, else pure persona | "mystery cat, mystery stars" |

Fixed assumption: when time/location absent, default to **noon UTC**, recorded in `tz_assumption` for reproducibility (requirement 3.6). Rising sign requires birth time + location and is `null` otherwise (never guessed).

## 4. The card (one renderer, three triggers)

A single card component renders `{ reading_text, facts, cat_name }`. Triggered by: the first natal reading, a behavior read, or (STRETCH) the daily nudge email. Resolves the earlier "full card vs just a read" question: everything is the card.

## 5. The reveal + latency (requirement 5)

The "Consult" click starts a fixed-minimum anticipation animation (Madame at her café table, eyes to the sky). The AI call runs concurrently. The card reveals when BOTH the animation minimum has elapsed AND the response is in. If the response is slow, the animation loops gently; if it fails or times out, show the in-voice error (requirement 4.5). Respect `prefers-reduced-motion` (13.2).

## 6. Sharing (resolves blocker #2)

The card is rendered to an image client-side (e.g. html-to-image / canvas) and shared via download or the Web Share API. **No hosted card, no shareable URL, no server storage.** This keeps the free tier localStorage-only and accountless (requirement 7).

## 7. Freemium enforcement (resolves the wallet-guard gap)

- **localStorage counter:** friendly UX only ("X of 3 left"). Spoofable, not a guard.
- **Server-side per-IP rate limit:** the real ceiling on `/reading` and `/behavior`, via API Gateway throttling or a small counter (e.g. DynamoDB or in-memory per-Lambda with a TTL). Protects spend even during judging when a live endpoint is exposed. IP is leaky and is personal data (GDPR / England-Wales governing law), so minimize and disclose in the security report.

## 8. Daily nudge: additive design (resolves blocker #1)

The core app is localStorage-only and accountless. The nudge does NOT change that. It is a separate, opt-in module:

```
Opt-in form (email)  ->  store { email, cat_facts, schedule }  (subscribers only)
                              v
                         Temporal schedule (daily)
                              |  compute transits -> AI nudge card -> SES email
                              |  durable: retry a failed step, never double-send
```

Only opt-in subscribers get a server-side record. Everyone else stays localStorage-only. If unfinished, the opt-in renders as a STUB ("Daily readings, coming soon") and nothing else is affected (requirement 12.4). This is why the nudge is non-fatal.

## 9. Data model (what lives where)

- **Browser localStorage:** the active cat profile (name, birth inputs), the daily free-read counter, the sound/voice preference. No PII leaves the device for the core flow.
- **Server (transient):** request inputs during a call; not persisted in v1 core.
- **Server (rate limit):** per-IP counters with short TTL.
- **Server (nudge subscribers only, STRETCH):** {email, cat_facts, schedule}.
- **NEVER in v1:** accounts table, payment records, behavior history store.

## 10. Security design (maps to requirements 11.x)

Credentials only in the Lambda execution role (SigV4) or Secrets Manager; never client-side. Behavior-log text validated client + server, length-capped, kept strictly in the user-content slot (prompt-injection protection). HTTPS + tight CORS. try/catch on every call with in-voice error states. Least-privilege IAM (AnthropicInferenceAccess or scoped workspace ARN). Aikido scan before submission. CloudWatch alarms are a v2 stub; minimal logging in v1.

## 11. AI provider quick reference

Client `AnthropicAWS`; base `aws-external-anthropic.{region}.api.aws`; Messages API; models `claude-haiku-4-5` (cheap, nudge) and `claude-sonnet-4-6` (marquee reads); env `ANTHROPIC_AWS_WORKSPACE_ID` + `AWS_REGION`; one-time `aws iam enable-outbound-web-identity-federation`. Full detail in `docs/build-reference.md` section 1.
