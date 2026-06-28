# Madame Minou: Build Reference (for Antigravity / Kiro)

*This is a reference doc, not a freestyle prompt. The agent builds FROM these facts, not from vibes. Everything in the Claude-on-AWS section is pulled from the official docs (June 2026), links at the bottom. Verify against the live docs before relying on any single line; SDK clients here are in beta and can shift.*

*Last updated: June 23, 2026*

---

## How to use this doc

Point the coding agent at this file. It pins the AI provider, the security rules, and the infra decisions so the build doesn't drift or invent an integration. When a section says MUST, it's a hard requirement. When it says STUB or NEVER, do not build it in v1 (a NEVER can still have a commented stub with notes).

---

## 0. Build methodology: spec-driven development (Kiro-style)

This build uses **spec-driven development**, the same method as Kiro: write a formal spec before code. Not a new way of working, it's the existing PRD-first / architecture-before-code / MUST-STUB-NEVER / block-by-block method, formalized into Kiro's structure. The "PRD" and "the Kiro spec" are the same artifact.

**The spec set (portable markdown, executor-agnostic):**

- **requirements.md**: user stories + acceptance criteria in EARS notation: *WHEN [condition] THE SYSTEM SHALL [behavior]*. Every Locked item, guardrail, and spec-gap becomes a testable WHEN/SHALL. Writing them is what closes the spec-gaps ledger. Examples:
  - WHEN the owner submits a cat name and birth date, THE SYSTEM SHALL compute the sun sign deterministically and pass it to the AI layer as a fact (the model never invents positions).
  - WHILE no birth time is provided, THE SYSTEM SHALL omit the rising sign and label the result an estimated chart.
  - WHEN a behavior log contains a red-flag keyword (not eating, not urinating, repeated vomiting, lethargy, labored breathing), THE SYSTEM SHALL surface the vet-care line and SHALL NOT frame it astrologically.
  - WHEN a free-tier user requests a 4th behavior read in a day, THE SYSTEM SHALL block the request server-side and present the paywall.
- **design.md**: technical design: the café-terrace UI, the deterministic-to-AI contract, the Claude-on-AWS integration (section 1), data flow, the card renderer. Most already exists in this doc + what-she-is.
- **tasks.md**: the block-by-block build order, each task traceable to a requirement, executed one at a time with an approval gate (propose, approve, implement) and a PASS/FAIL QA checkpoint.
- **steering files (`.kiro/steering/`)**: persistent rules the agent obeys on every task regardless of the prompt: the security MUSTs, Occam's razor, the deterministic-AI contract, the writing rules (no em-dashes, no AI cliches), the MUST/STUB/NEVER conventions. Author once, governs everything. Highest-leverage anti-drift tool.

**Timing (Kiro from day one):**

- 2000 free Kiro participation credits for this build + Kiro Pro already held. Kiro is the executor from June 24, no Antigravity-first phase needed. (Antigravity stays as an optional fallback.)
- The spec set lives in the repo's `.kiro/` folder (`.kiro/specs/madame-minou/` + `.kiro/steering/`), Kiro's native format. Kiro builds from it task by task with approval gates.
- The `.kiro/` folder + a short write-up = the **Kiro Track opt-in** (separate prize pool), now a definite claim.
- Still portable: it's just markdown, so Antigravity or any agent can read it if needed.

**Why it fits the rubric:** EARS acceptance criteria are testable, which closes the spec-gaps ledger and strengthens Technical Execution + Documentation. The `.kiro` folder adds the Kiro Track.

---

## 1. AI provider: Claude Platform on AWS (the new method)

We are NOT using Bedrock and NOT using the plain Anthropic API. We are using **Claude Platform on AWS**: the native Anthropic Messages API, operated by Anthropic, authenticated and billed through AWS. Same API shape as the first-party Claude API, different base URL + auth + a required workspace header.

### The hard facts (from the docs)

- **Base URL:** `aws-external-anthropic.{region}.api.aws`
- **API surface:** Anthropic Messages API (`/v1/messages`). Same request/response shape as first-party Claude.
- **SDK client:** `AnthropicAWS` (Python) / `AnthropicAws` (other langs). **In beta.** Packages: `anthropic[aws]` (Python), `@anthropic-ai/aws-sdk` (TS).
- **Model IDs** (identical to first-party, NO `anthropic.` prefix, NO ARNs):

  | Use | Model | Model ID |
  | --- | --- | --- |
  | Marquee on-demand reads (voice matters) | Claude Sonnet 4.6 | `claude-sonnet-4-6` |
  | High-volume daily nudge (cheap) | Claude Haiku 4.5 | `claude-haiku-4-5` |
  | If a read needs more depth | Claude Opus 4.6 / 4.7 | `claude-opus-4-6` / `claude-opus-4-7` |

- **Streaming:** SSE (same as Claude API).
- **Required env vars:** `ANTHROPIC_AWS_WORKSPACE_ID` (format `wrkspc_...`) and `AWS_REGION`. Region is required; the client throws if it is missing (no default, unlike Bedrock).
- **Required header:** `anthropic-workspace-id` (the SDK sets it from the env var automatically).

### One-time setup (do this in the day-one spike)

1. Sign up for Claude Platform on AWS in the AWS Console (provisions a new Anthropic org tied to the AWS account, accepts terms, sets up Marketplace billing).
2. Create a workspace (one per region), note the `wrkspc_...` ID.
3. **Enable outbound web identity federation, once per account:**
   ```
   aws iam enable-outbound-web-identity-federation
   ```
   This is the single most common setup error. Skip it and every request fails with "Outbound web identity federation is disabled for your account." This step is NOT needed on Bedrock, so it surprises people migrating.
4. Set env:
   ```
   export ANTHROPIC_AWS_WORKSPACE_ID='wrkspc_xxx'
   export AWS_REGION='us-west-2'
   ```

### Auth (pick one)

- **SigV4 (primary, enterprise path):** uses the standard AWS default credential provider chain (env vars, `~/.aws/credentials`, SSO, IRSA, ECS/EC2 roles). SigV4 service name is `aws-external-anthropic`. Best for server/Lambda running under an IAM role.
- **API key (simpler, for local dev or a serverless function):** set `ANTHROPIC_AWS_API_KEY`. Generate keys in the **AWS Console** under Claude Platform on AWS → API keys (NOT the regular Claude Console). Principal needs the `aws-external-anthropic:CallWithBearerToken` IAM action. Short-term tokens (12h) available via AWS token-generator libs.

For Madame Minou: the model call lives **server-side only** (Lambda or a server route). Run it under an IAM role with SigV4, or use an API key stored server-side. NEVER ship either to the browser.

### Minimal call (Python)

```python
from anthropic import AnthropicAWS

client = AnthropicAWS()  # reads AWS_REGION + ANTHROPIC_AWS_WORKSPACE_ID from env

message = client.messages.create(
    model="claude-haiku-4-5",          # cheap model for the daily nudge
    max_tokens=1024,
    system=MADAME_MINOU_VOICE,          # persona system prompt
    messages=[{"role": "user", "content": chart_facts_as_text}],
)
print(message.content)
```

### Minimal call (TypeScript)

```ts
import { AnthropicAws } from "@anthropic-ai/aws-sdk";

const client = new AnthropicAws(); // reads AWS_REGION + ANTHROPIC_AWS_WORKSPACE_ID

const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  system: MADAME_MINOU_VOICE,
  messages: [{ role: "user", content: chartFactsAsText }],
});
```

### The deterministic-to-AI contract (DO NOT let the model do the astrology)

The chart engine computes the facts. The model only writes the voice. The boundary is a structured object passed in as facts:

```
chart facts (deterministic)  ->  { sun, moon, rising?, notable_transit, behavior? }
        |                                          |
   ephemeris lib                          system prompt = Madame Minou voice
                                          user message  = the facts above
                                          model output  = the flavored reading
```

The model is told: "Here are the true astrological facts. Write Madame Minou's reading from THEM. Do not invent positions." This is what keeps determinism as the differentiator.

### Provider gotchas / longevity notes

- SDK clients are **beta**. Pin exact package versions in the spike and re-check the changelog before relying on them.
- Rate limits start at **Tier 1** on signup with no auto-advancement. Fine for a hackathon, but it's a real ceiling. Don't load-test carelessly.
- `inference_geo` defaults to `global`. Set `inference_geo="us"` per request if you want US-only inference (1.1x price; only on Sonnet 4.6 / Opus 4.6 and later).
- Spike pass/fail: "Can I get a styled Madame Minou reading back through `AnthropicAWS`?" If yes, commit. If the beta SDK fights you, fall back to Bedrock (`AnthropicBedrockMantle`, base `bedrock-mantle.{region}.api.aws`) or the plain Anthropic API. The model call is small and isolated, so swapping is cheap.

---

## 2. Security (MUST, every line)

- **Credentials server-side only.** IAM role (SigV4) or the AWS-Console API key, in server env / Secrets Manager. NEVER in the browser, NEVER in client JS, NEVER in the repo. `.env` is gitignored.
- **Least-privilege IAM.** Grant only what the app needs. The managed policy `AnthropicInferenceAccess` (or a scoped policy allowing `aws-external-anthropic:CreateInference` + `CountTokens` on your workspace ARN) is the fit. Deny batch if unused.
- **Prompt-injection protection (MUST).** Behavior-log text is free user input that gets fed to the model. Validate and sanitize client-side AND server-side. Treat the log as untrusted: keep it in the user-content slot, never concatenated into the system prompt, and cap its length.
- **Rate limit = the wallet guard.** localStorage counter is UX only. The real ceiling is a server-side limit (per-IP) on the inference endpoint so no one (judge or bad actor) can drain the account. Decide the mechanism in the PRD.
- **Transport + headers.** HTTPS only. Tight CORS (only your origin). `rel="noopener noreferrer"` on outbound links (Adopt-a-Minou).
- **try/catch on every call.** Meaningful error states, never a blank screen. A failed reading shows Madame Minou shrugging in-voice, not a stack trace.
- **Aikido scan** on the repo before submission (dependency scan, SAST, secret detection). Include the report in the submission for the Security category + bonus.

---

## 3. Docker (Occam's razor decision)

Honest call: **don't add Docker for "tech cred."** Cred comes from fit, not from extra tech. An AWS or Temporal judge is more impressed by a clean deploy than a gratuitous container, and a needless Dockerfile reads as noise, not sophistication.

- **Containerize ONLY if the deploy or the judges need it.** If the stack is serverless (Lambda / Amplify / Vercel), Docker adds nothing. Skip it.
- **The one good reason:** reproducible local runs. Judges may try to run it ("installs and runs consistently" is a submission requirement). A single minimal Dockerfile that lets a judge `docker run` the whole thing is a real reproducibility win, MUST-light if you want it.
- **NEVER in v1:** docker-compose sprawl, Kubernetes, multi-service orchestration. That's ceremony for a solo 14-day build.

Decision: defer to the stack. If serverless, no Docker. If you want one-command local repro for judges, one tiny Dockerfile, nothing more.

---

## 4. Monitoring and logging

- **v1 (minimal, cheap):** structured app logging + CloudTrail is on by default for management events. Enough to debug and to write the security report. Log on a ~30-day rolling basis (Anthropic's recommendation). Capture the `x-amzn-requestid` (AWS) and `request-id` (Anthropic) response headers for support.
- **CloudWatch alarms: STUB for v1, real in v2.** Alarm thresholds + SNS notifications (spend spikes, error-rate, throttling) are a v2 feature. In v1, leave a commented stub and a line in the security report: "alarms designed, deferred to v2." Note in CloudWatch: inference calls are CloudTrail **Data events** and need explicit (paid) configuration, another reason to keep it minimal now.

---

## 5. Occam's razor (the standing rule)

Build the minimum that satisfies the MUST list and the scoring guardrails. Stub the rest. Do not add infrastructure for its own sake.

- If a feature isn't in the current phase, it's a commented stub with notes, not a half-build.
- No dependency joins the project without a longevity check (not deprecated, not EOL, recent release).
- One file, one responsibility. No god files.
- Deterministic where structure matters, AI only for flavor.
- Every added tool must earn its place by solving a real problem, not by looking impressive.

---

## 6. Reference links (official)

- Claude Platform on AWS: https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws
- Claude in Amazon Bedrock (fallback): https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock
- IAM actions for Claude Platform on AWS: https://platform.claude.com/docs/en/api/claude-platform-on-aws-iam-actions
- Client SDKs: https://platform.claude.com/docs/en/api/client-sdks
- Messages API: https://platform.claude.com/docs/en/build-with-claude/working-with-messages
- Pricing (CCUs): https://platform.claude.com/docs/en/about-claude/pricing#claude-platform-on-aws-pricing
- Prompt caching (cost control): https://platform.claude.com/docs/en/build-with-claude/prompt-caching
