# Steering: Security

*Persistent security rules. Apply to every task. Non-negotiable. Maps to requirements 11.x.*

## Credentials and keys

- API keys / AWS credentials server-side only: IAM execution role (SigV4) or Secrets Manager. NEVER in client code, NEVER in the repo, NEVER in a public env var.
- The browser never holds model credentials. The AI model is called only from a server endpoint.
- `.env` is gitignored. No secrets in commits.

## Input handling (textContent, not innerHTML)

- Render user/AI text with `textContent`, never `innerHTML`. No `eval()`.
- Validate and sanitize all input client-side AND server-side. Never trust the front end. Never trust users.
- Behavior-log text is untrusted: keep it in the user-content slot only (never concatenated into the system prompt), cap its length. This is the prompt-injection surface.

## Network and errors

- HTTPS only. CORS restricted to the app's own origin.
- try/catch on every fetch / API call, with a meaningful in-voice error state. Never a blank screen.
- Outbound links open in a new tab with `rel="noopener noreferrer"`.

## AWS / IAM

- Least-privilege IAM: AnthropicInferenceAccess or a scoped policy on the workspace ARN. Deny what isn't used (e.g. batch).
- Per-IP server-side rate limit on inference endpoints (the wallet guard). IP is personal data: minimize and disclose.

## Pre-deploy checklist (11 points)

Authorization · input validation/sanitization · CORS · rate limiting · (password reset expiration: N/A v1, no accounts) · frontend error handling · database indexes (N/A v1 core) · logging · alarms (CloudWatch alarms = v2 stub) · rollback plan · prompt-injection protection.

## Reporting

- Run an Aikido scan before submission (dependency scan, SAST, secret detection). Include the report. Security is 15% of the score, and a judge is the Aikido pentest lead.
