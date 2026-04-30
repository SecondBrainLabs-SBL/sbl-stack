---
name: sbl
version: 1.0.0
description: |
  SBL Stack — the home screen for your sbl.so campaigns. Audits all campaigns,
  surfaces what needs attention, and routes to the right sub-skill: create a new
  campaign, optimize a draft, triage the HI queue, get a playbook strategy, or
  run a weekly retro.
  Use when asked to "sbl", "open sbl", "check my campaigns", "what should I do
  with my campaigns", or any sbl.so campaign management request.
  Proactively invoke when the user mentions sbl.so, campaign management, LinkedIn
  outreach, or wants to run or review outreach campaigns. (sbl-stack)
allowed-tools:
  - Read
  - AskUserQuestion
triggers:
  - sbl
  - open sbl
  - check my campaigns
  - what should I do with my campaigns
  - manage my campaigns
  - sbl.so campaigns
  - campaign science
  - triple constraint
---

## Step 0 — Auth and company context

Check if `SBL_COMPANY_ID` env var is set.

```bash
echo "COMPANY_ID: ${SBL_COMPANY_ID:-not_set}"
```

If not set, ask:
"What is your sbl.so company ID? (Find it in sbl.so → Settings → Company. Set `SBL_COMPANY_ID=<id>` to skip this next time.)"

---

## Step 1 — Audit all campaigns

Call `sbl_list_campaigns` MCP tool with:
- `company_id`: from Step 0
- `response_format`: "json"

Parse the response and build the audit table. For each campaign extract:
- `id`, `name`, `status`, `communicationChannelToUse`, `type`
- `statistics` counts
- `scoreData.score` (if available)

Channel labels: 1 = WhatsApp, 2 = iMessage, 3 = LinkedIn
Status labels: 1 = PENDING_APPROVAL, 2 = APPROVED, 3 = SCHEDULED, 4 = SENDING, 7 = RUNNING, 8 = ENDED, 9 = CREATED

Display:

```
SBL STACK — Company [company_id]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR CAMPAIGNS

┌──────────────────────────────────┬────────┬─────────────┬───────────┬───────┐
│ Name                             │ ID     │ Status      │ Channel   │ Score │
├──────────────────────────────────┼────────┼─────────────┼───────────┼───────┤
│ [name]                           │ [id]   │ 🟡 DRAFT    │ LinkedIn  │ 64    │
│ [name]                           │ [id]   │ 🟢 RUNNING  │ LinkedIn  │  —    │
│ [name]                           │ [id]   │ ⚫ ENDED    │ WhatsApp  │  —    │
└──────────────────────────────────┴────────┴─────────────┴───────────┴───────┘

Status: 🟢 Running  🟡 Draft  🔵 Scheduled  🟠 Pending  ⚫ Ended
```

---

## Step 2 — Surface what needs attention

Check for:

1. **HI queue** — for each RUNNING campaign, call `sbl_list_human_intervention` with:
   - `company_id`: from Step 0
   - `campaign_id`: each running campaign
   - `response_format`: "json"
   
   Count total leads across all campaigns.

2. **Low-score drafts** — campaigns with status CREATED and `scoreData.score < 70`

3. **No campaigns yet** — if the list is empty

Then show the attention banner:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEEDS ATTENTION

[If HI queue > 0]:
🚨 [N] leads need your reply across [M] campaigns  → /sbl-triage

[If low-score drafts exist]:
⚠️  [N] draft campaign(s) have score < 70  → /sbl-optimize [id]

[If no running campaigns but drafts exist]:
💡 You have [N] draft(s) ready to review and launch

[If no campaigns at all]:
👋 No campaigns yet — let's build your first one

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 3 — Route to the right action

If there is an obvious priority (HI queue > 0, or explicitly one thing that needs doing), suggest it directly:

"You have [N] leads waiting for a reply. Want me to triage them now? (yes / no)"

Otherwise, ask what to do:

```
What do you want to do?

A) Create a new campaign           → /sbl-create
B) Optimize a draft                → /sbl-optimize  [show if CREATED campaigns exist]
C) Triage the HI queue             → /sbl-triage    [show if HI count > 0]
D) Get a playbook strategy         → /sbl-playbook
E) Weekly retro — full overview    → /sbl-retro
F) Campaign Science loop           → /sbl-science   [PIC × CIQ × MRS diagnosis]
```

---

## Step 4 — Invoke the chosen sub-skill

Based on the user's choice, read the corresponding skill file and execute it from Step 0:

- **A (Create):** Read `sbl-create/SKILL.md` and follow it from Step 0.
- **B (Optimize):** Read `sbl-optimize/SKILL.md` and follow it from Step 0. If the user specified a campaign ID, pass it.
- **C (Triage):** Read `sbl-triage/SKILL.md` and follow it from Step 0.
- **D (Playbook):** Read `sbl-playbook/SKILL.md` and follow it from Step 0.
- **E (Retro):** Read `sbl-retro/SKILL.md` and follow it from Step 0.
- **F (Science):** Read `sbl-science/SKILL.md` and follow it from Step 0.

Each sub-skill is self-contained — follow it completely before returning control here.

---

## After sub-skill completes

Return to the SBL home screen summary. Ask:
"Anything else? (create / optimize / triage / playbook / retro / done)"

If done: exit.
