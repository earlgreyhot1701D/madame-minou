# Madame Minou: Kiro Workflow (autonomy, self-check, hooks)

*Reference doc, not steering. Kept out of always-loaded steering so it doesn't burn tokens on every interaction. Configure the hooks in Kiro once; follow the autonomy model throughout.*

*Last updated: June 24, 2026*

---

## Autonomy model: free within a task, gated at the block

- **Within a task:** let Kiro run autonomously (Autopilot). It implements the task end to end without stopping you for every file.
- **At a block boundary:** human PASS/FAIL gate (you). Kiro does not start the next block until you pass the current one.
- This keeps speed high and approvals cheap: you review per block (8 gates total), not per file.

## The self-check loop (mandatory before "done")

Before Kiro reports any task complete, it runs this loop on itself:

1. **Re-read the requirement** it was implementing (the R# from tasks.md).
2. **Check against the EARS acceptance criterion**: does the behavior actually satisfy the WHEN/SHALL?
3. **Check against steering**: security rules, no em-dashes / no AI cliches in copy, one-file-one-responsibility, "DO NOT refactor other code," determinism contract not violated.
4. **Run or justify the test** for that piece (chart-engine tests, a manual UI pass, an error-path check).
5. **Report PASS/FAIL with evidence** quoted from the actual files, not memory.
6. **If FAIL:** fix and re-run the loop. Never report done on a failing check.

This is the cheapest insurance against confident drift. A self-check costs a little; rebuilding a wrong block costs a lot.

## Hooks: the smart minimal set (max 3)

Each hook fires an agent run and spends credits. Keep them few, manual, and narrow.

| Hook | Trigger | When to run | Why it earns its keep |
| --- | --- | --- | --- |
| **Spec-compliance check** | Manual | At each block's QA gate | Verifies the block against requirements.md + steering, reports PASS/FAIL. This automates your QA checkpoint. |
| **Security sweep** | Manual | Before deploy + at Block 7 | Walks the security steering checklist over changed files. Security is 15% and a judge is the Aikido lead. |
| **Chart-engine test** | On-save, scoped ONLY to the chart-engine module/tests (optional) | While building Block 1 | Determinism is the differentiator; these tests are fast and cheap. If credits feel tight, make it manual too. |

## What to avoid (the credit killers)

- On-save hooks on frequently-edited files (fire constantly).
- "Review the whole repo on any change" hooks.
- Auto-generate docs on every save.
- Any hook whose value is vague. If you cannot name what it catches, do not add it.

## Token / credit economy (you have 2000 + Kiro Pro)

- Steering files load into context every interaction, so keep them short. Detail lives in reference docs like this one.
- Manual hooks at milestones beat automatic hooks on hot paths.
- Scope every hook to specific files or directories, never the whole tree.
- Prompt caching (Claude Platform on AWS) cuts cost on repeated system prompts.
- The self-check is worth its tokens because it prevents expensive rework. The hooks are worth theirs only if they stay few and narrow.
