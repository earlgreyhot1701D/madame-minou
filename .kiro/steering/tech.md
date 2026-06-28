# Steering: Tech

*Persistent technical context. The stack, the AI integration, and the determinism contract. Full detail lives in `docs/build-reference.md`.*

## Stack (LOCKED — all-in AWS)

Platform decision is LOCKED. No non-AWS hosting or services without explicit approval.

- **Frontend:** S3 + CloudFront (or Amplify Hosting)
- **Backend:** AWS Lambda (Python) + API Gateway
- **AI:** Claude Platform on AWS (`AnthropicAWS` client). Fallback: Amazon Bedrock.
- **Voice (STRETCH):** Amazon Polly French neural
- **Secrets/identity:** IAM roles + Secrets Manager; keys server-side only
- **Logging:** CloudWatch (alarms = v2 stub)
- **Chart engine:** Python + Swiss Ephemeris (pyswisseph). Deterministic.
- **Build tool:** Kiro (spec-driven, this `.kiro/` folder). Kiro Track opt-in: yes.

The app MUST deploy to a live public HTTPS URL for judging (July 8–14). No non-AWS hosting or services without flagging it first.

## Claude Platform on AWS (the AI layer)

- Client: `AnthropicAWS` (Python), beta. Package `anthropic[aws]`.
- Base URL: `aws-external-anthropic.{region}.api.aws`. Messages API (`/v1/messages`).
- Models: `claude-haiku-4-5` (cheap, daily nudge), `claude-sonnet-4-6` (marquee reads). No `anthropic.` prefix, no ARNs.
- Env: `ANTHROPIC_AWS_WORKSPACE_ID` (`wrkspc_...`) + `AWS_REGION` (required, no default).
- One-time per account: `aws iam enable-outbound-web-identity-federation` (most common setup error if skipped).
- Auth: SigV4 (IAM role) preferred for the Lambda; API key option for local dev. SDK is beta: pin versions, recheck changelog.

## The determinism contract (do not violate)

- The chart engine computes positions. The model only writes voice over them.
- Facts object: `{ cat_name, chart_tier, sun, moon, moon_cusp, rising, notable_transit, tz_assumption, behavior? }`.
- System prompt = Madame Minou persona. User content = the facts + "write the reading from THESE facts, do not invent or change positions."
- Rising sign requires birth time + location; otherwise `null`, never guessed.
- Absent time/location => assume noon UTC, record in `tz_assumption`.

## Models / costs

- Cheap model for high-volume nudges, stronger for marquee reads. Cost couples to the gate-the-reads decision. Prompt caching available to cut cost.

## What's NOT in v1 (NEVER)

Accounts/auth, cross-device sync, payments, live shelter API, multi-cat, behavior history, push/SMS, voice input. Stubs allowed. See `docs/v2-someday.md`.
