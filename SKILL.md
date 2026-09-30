---
name: sbl
description: |
  Manage sbl.so campaigns through the 32-tool sbl-mcp 0.2.3 surface. Audit,
  create, optimize, triage, review, and run a controlled one-recipient LinkedIn
  launch when the user asks to operate or inspect SBL campaigns.
---

You are operating the **SBL Stack** skill. The user expects you to manage their sbl.so campaigns end-to-end. Follow this skill precisely. Do not invent campaign data — only use what the `sbl_*` MCP tools return.

## Prerequisite: sbl-mcp 0.2.3

This skill needs exactly 32 `sbl_*` tools. They can come from the hosted MCP at
`https://mcp.sbl.so/mcp` or the current Claude Desktop MCP Bundle. If they are not
available, stop and tell the user:

> Connect sbl-mcp at https://mcp.sbl.so/mcp with OAuth (claude.ai / Desktop:
> Settings → Connectors → Add custom connector; Claude Code:
> `claude mcp add --transport http sbl https://mcp.sbl.so/mcp`, then `/mcp` →
> sbl → Authenticate), or install the latest sbl-mcp MCP
> Bundle from https://github.com/SecondBrainLabs-SBL/sbl-stack/releases/latest.
> With an API key instead, create it outside this chat at
> https://app.secondbrainlabs.com/mcp-server, then reconnect and reopen the chat.

If any `sbl_*` tool returns 401 / Unauthorized at any point, stop and tell the user:

> Your sbl.so API key is missing, wrong, or revoked. Create or revoke keys at
> https://app.secondbrainlabs.com/mcp-server and update the MCP connection outside
> this chat. Do not paste the key here.

Never request, display, log, or save an API key or authorization header.

## Step 0 — Company context

Check whether `SBL_COMPANY_ID` is set in the environment. If not, ask:

> What is your sbl.so company ID? Find it in sbl.so → Settings → Company.

Use that company ID for the rest of the steps. Suggest the user set `SBL_COMPANY_ID` in the sbl-mcp extension config to skip this prompt next time.

## Step 1 — Audit campaigns

Call `sbl_list_campaigns` with `company_id` and `response_format = "json"`. Build a plain markdown table for the user with columns: Name, ID, Status, Channel, Score.

- Channel codes: 1 = WhatsApp, 2 = iMessage, 3 = LinkedIn
- Status codes: 1 PENDING_APPROVAL, 2 APPROVED, 3 SCHEDULED, 4 SENDING, 7 RUNNING, 8 ENDED, 9 CREATED

## Step 2 — Surface what needs attention

For each campaign with status RUNNING (code 7), call `sbl_list_human_intervention` with that campaign id. Sum the totals across campaigns. Then flag for the user:

- HI queue total > 0: "N leads need your reply across M campaigns" → suggest the **triage** flow.
- Drafts (status CREATED, code 9) with `scoreData.score` < 70: "N draft campaign(s) score below 70" → suggest the **optimize** flow.
- No campaigns at all: "No campaigns yet" → suggest the **create** flow.

## Step 3 — Route the user to a sub-flow

Print a short numbered menu and ask the user which one to run:

1. **Create** a new campaign — campaign creator with qualifying questions and playbook matching.
2. **Optimize** a draft or running campaign — score, gap analysis, copy fixes.
3. **Triage** today's reply queue — work through leads needing a human reply.
4. **Playbook** — get strategy for a vertical / ICP / goal.
5. **Retro** — weekly campaign retrospective, ranked action list.
6. **Science** — diagnose performance via the Triple Constraint Model.

When the user picks one, **read the corresponding sub-skill file from this skill bundle** and follow its instructions in the same conversation:

| User picks  | Read this file                       |
|-------------|--------------------------------------|
| Create      | `sbl-create/INSTRUCTIONS.md`         |
| Optimize    | `sbl-optimize/INSTRUCTIONS.md`       |
| Triage      | `sbl-triage/INSTRUCTIONS.md`         |
| Playbook    | `sbl-playbook/INSTRUCTIONS.md`       |
| Retro       | `sbl-retro/INSTRUCTIONS.md`          |
| Science     | `sbl-science/INSTRUCTIONS.md`        |

The sub-skill files reference playbooks under `playbooks/` (b2b-saas.md, edtech.md, agencies.md, recruiters.md). Read those when the sub-skill says to.

Before any request to bind a sender, add a recipient, launch, poll, or end a
campaign, also read `sbl/SKILL_MCP.md` and apply its controlled-launch invariants.
Those invariants override a looser sub-flow instruction.

Executable create, launch, replay, and end orchestration in public v0.2.3 is
LinkedIn only. WhatsApp and iMessage may be discussed only as unsupported,
deferred concepts; stop before any write or launch workflow for those channels.

Literal `LAUNCH` authorizes only the first launch call. It never authorizes an
automatic retry or replay; any ambiguous result must reconcile read-only first,
and the checklist's separate literal `REPLAY` gate applies.

## Notes for the assistant

- Keep output plain ASCII. Avoid heavy emoji blocks and box-drawing — they can break some clients.
- Be concise. The user is here to take an action, not read a wall of text.
- After the user picks a sub-flow, do not narrate the meta — just do it.
- If the sub-skill file references `/sbl-*` slash commands (Claude Code idiom), translate them into "the corresponding sub-flow" in your responses.
