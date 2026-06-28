# Steering: Principles

*Persistent rules. Kiro follows these on every task regardless of the prompt. Highest-leverage anti-drift tool.*

## Build philosophy

- PRD-first / spec-first. This spec governs. If a task isn't in the spec, stop and ask.
- MUST / STRETCH / STUB / NEVER labels are binding. NEVER means never for the behavior this sprint, but a commented stub with notes is allowed.
- Stub, don't build half-features. If it's out of phase, leave a commented stub with implementation notes.
- Mock data first, then wire APIs. Never wire a real API to a broken layout.
- One file, one responsibility. No god files.
- Block-by-block. A QA checkpoint (PASS/FAIL) after each block before moving on.
- Staged prompts: propose first, get approval, then implement. Explicit "DO NOT refactor other code" guardrail on every change.
- Deterministic logic + AI reasoning. Structure is deterministic; flavor is AI-generated. Never let the model do the deterministic work (it must not invent astrology).
- Verify claims against the actual files, not memory.

## Execution mode (autonomy + self-check)

- Run autonomously WITHIN a task; keep the human PASS/FAIL gate at each BLOCK boundary, not every file.
- Before marking any task done, self-verify: re-read the requirement (R#), confirm the change meets its EARS acceptance criterion AND the steering rules, run or justify the relevant test, and report PASS/FAIL with evidence from the actual files (not memory).
- If the self-check FAILS, fix and re-check before reporting done. Never report done on a failing check.
- "DO NOT refactor other code" applies to every change.
- Hooks cost credits (each fires an agent run). Prefer manual-trigger hooks at milestones; never broad on-save hooks. See `specs/madame-minou/kiro-workflow.md`.

## Occam's razor (standing rule)

- Build the minimum that satisfies MUST + the scoring guardrails. Stub the rest.
- No infrastructure for its own sake. Every dependency or service must solve a real problem, not look impressive.
- Tool longevity check before adopting any dependency: not deprecated, not EOL, recent release.

## Writing rules (all user-facing copy and docs)

- No em dashes.
- No AI cliches (delve, landscape, straightforward, genuinely, honestly, soapbox phrasing).
- Short, conversational, warm and sharp.
- Honest over optimistic. No overclaiming. Limitations language is a feature.

## Tone of the product

Madame Minou is a delight, not a diagnosis. Whimsy on top, honest structure underneath. The disclaimer is part of the charm, not a buzzkill.
