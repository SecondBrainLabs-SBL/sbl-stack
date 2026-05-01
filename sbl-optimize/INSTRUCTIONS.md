---
name: sbl-optimize
version: 1.0.0
description: |
  SBL Campaign Optimizer — fetches a draft or running campaign, reads its AI
  score and gaps, benchmarks it against playbook data, and generates specific
  before/after copy fixes for every gap. Auto-applies fixes when sbl_update_campaign
  is available.
  Use when asked to "optimize my campaign", "fix this campaign", "improve the score",
  or "why is my campaign score low".
  Invoked by /sbl-create (post-generation) and /sbl (when drafts need fixing). (sbl-stack)
allowed-tools:
  - Read
  - AskUserQuestion
triggers:
  - optimize my campaign
  - fix this campaign
  - improve the score
  - why is my campaign score low
  - review this campaign
---

## Step 0 — Auth and company context

Check if `SBL_COMPANY_ID` env var is set.

```bash
echo "COMPANY_ID: ${SBL_COMPANY_ID:-not_set}"
```

If not set, ask for it.

If `campaign_id` was passed from a calling skill, use it. Otherwise go to Step 1.

---

## Step 1 — Select campaign

If campaign_id is not already known, call `sbl_list_campaigns` MCP tool with:
- `company_id`: from Step 0
- `response_format`: "json"

Show a table of all campaigns. Highlight CREATED (draft) status campaigns — these are the priority.

Ask: "Which campaign do you want to optimize? (enter the ID)"

---

## Step 2 — Fetch full campaign

Call `sbl_get_campaign` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: selected campaign
- `response_format`: "json"

Extract and hold:
- `scoreData.score` — the AI quality score (0–100)
- `scoreData.gaps` — list of gap strings
- `scoreData.questions` — the AI's questions for the user (what it couldn't fill)
- `scoreData.status` — 1 = poor, 2 = fair, 3 = good, 4 = excellent
- `initialMessage`
- `nonConnectedLeadsMessage`
- `followupMessages` (array)
- `flow` (chat flow rules array)
- `smartFollowupsConfig` (delay timings + reasoning)
- `targetUsers` (ICP description)
- `objective`
- `communicationChannelToUse` (1=WhatsApp, 2=iMessage, 3=LinkedIn)
- `aiCampaignGenerationPrompt` — the original prompt used to generate it

---

## Step 3 — Display current state

Show the campaign health snapshot:

```
CAMPAIGN AUDIT — [campaign name] (ID: [campaign_id])

AI SCORE: [score]/100  [POOR < 50 | FAIR 50–69 | GOOD 70–89 | EXCELLENT 90+]

GAPS TO FIX:
[numbered list of gaps from scoreData.gaps]

AI QUESTIONS STILL OPEN:
[numbered list from scoreData.questions — things the AI couldn't fill confidently]

CURRENT OUTREACH SEQUENCE:
  Connection request: [nonConnectedLeadsMessage]
  Initial message:    [initialMessage]
  FU 1 (after Xh):   [followupMessages[0].message]
  FU 2 (after Xh):   [followupMessages[1].message]

CHAT FLOW: [N] rules
SMART FOLLOW-UPS: [N] configured

TARGET ICP: [targetUsers.description]
OBJECTIVE:  [objective]
```

---

## Step 4 — Load the right playbook for benchmarking

Detect the vertical from the campaign's original prompt or ICP description:
- Mentions "founder", "CEO", "SaaS", "B2B software" → B2B SaaS → read `playbooks/b2b-saas.md`
- Mentions "course", "cohort", "bootcamp", "coaching", "edtech" → Edtech → read `playbooks/edtech.md`
- Mentions "agency", "lead gen", "client campaigns", "outbound" → Agencies → read `playbooks/agencies.md`
- Mentions "candidate", "hiring", "recruiter", "HR", "placement" → Recruiters → read `playbooks/recruiters.md`
- Uncertain → ask the user which vertical

Use the playbook to benchmark the campaign's message angle, char count, follow-up timing, and chat flow completeness.

---

## Step 5 — Generate fixes for every gap

For each gap in `scoreData.gaps`, produce a specific fix. Do not give generic advice — produce the actual copy.

### Gap: "No social proof" or "Social Proof"
Ask if not already known: "Do you have any specific numbers, client wins, or case studies? (e.g. 'helped 40 founders book demos in 3 weeks')"

Rewrite the initial message with social proof woven in naturally:
```
BEFORE:
[current initialMessage]

AFTER:
[rewritten message with social proof — match existing tone, keep under 300 chars for initial message]
```

### Gap: "No Call Booking Link" or calendar link missing
Ask if not already known: "What is your calendar or booking link?"

Identify the chat flow rule that says "Here's my calendar link" or similar. Show the fix:
```
BEFORE (chat flow rule [N]):
[current rule text with placeholder]

AFTER:
[same rule with the actual calendar URL]
```

### Gap: "Opener too generic" or connection request too cold
Rewrite `nonConnectedLeadsMessage` with a signal-based hook appropriate to the vertical:
```
BEFORE:
[current nonConnectedLeadsMessage]

AFTER (with [community/post/signal] reference):
[rewritten — under 250 characters, references a behavioral signal]
```

### Gap: "Missing follow-up angle" or follow-ups too repetitive
Rewrite follow-ups so each adds a new angle (not a re-pitch):
```
BEFORE — FU 1: [current]
AFTER — FU 1:  [new angle: warm check-in + micro-nudge]

BEFORE — FU 2: [current]
AFTER — FU 2:  [new angle: urgency or specificity, simple yes/no close]
```

### Gap: "Chat flow incomplete" or missing objection handlers
Add the missing rules based on the vertical's playbook patterns:
```
MISSING RULE — "IF USER SAYS [common objection for this vertical]":
[add the handler the playbook recommends]
```

### AI questions still open (from scoreData.questions)
For each question the AI flagged, either:
- Answer it from context (if the user has provided the info)
- Ask the user for the specific missing info
- Generate copy that fills the gap

---

## Step 6 — Apply fixes

Present all fixes together in a clear summary:

```
OPTIMIZATION SUMMARY — [N] fixes for campaign [campaign_id]

Fix 1: Social proof added to initial message
  → [before/after]

Fix 2: Calendar link added to chat flow rule 1
  → [before/after]

Fix 3: Connection request rewritten with signal hook
  → [before/after]

PROJECTED SCORE AFTER FIXES: [estimate — 85–95/100 if all gaps closed]
```

If `sbl_update_campaign` MCP tool is available:
  → Offer to apply all fixes automatically: "Apply all fixes now? (yes/no)"
  → On yes: call `sbl_update_campaign` with the updated fields
  → On no: "Copy the fixes above into sbl.so → campaign [ID] → Edit"

If `sbl_update_campaign` is not available:
  → "Apply these in sbl.so → Campaigns → [campaign_id] → Edit. Each fix is a direct copy-paste."

---

## Step 7 — Running campaign optimization (if campaign is not in CREATED status)

If the campaign is RUNNING, SCHEDULED, or any active status:
- Do not recommend pausing — suggest iterating
- Focus on: initial message A/B testing, follow-up angle adjustments, chat flow gap handlers
- Frame as "For the next campaign variant" rather than "change the live campaign"
- Pull analytics first: call `sbl_get_campaign_analytics` to see what's actually failing in conversations

```
RUNNING CAMPAIGN NOTE:
This campaign is live. Recommend:
1. Create a duplicate with the optimized copy — run as A/B variant
2. After 200 delivers on each, kill the underperformer
3. Scale Fractional SDR profiles on the winner
```

---

## Step 8 — Pre-launch reminder (if CREATED status)

```
Once fixes are applied, before launching:
[ ] Calendar link in chat flow rule #1 ← most critical
[ ] LinkedIn profile connected in SBL Settings
[ ] AI persona trained (voice sample uploaded)
[ ] Lead source configured
[ ] ICP Filter set (if Sales Navigator — 80%+ match)
[ ] Fractional SDR profiles added

/sbl-triage once live — check HI queue daily.
```

---

## Step 9 — Hand off

If invoked standalone: offer to triage any running campaigns with `/sbl-triage`.
If invoked by `/sbl-create`: return summary and exit.
If invoked by `/sbl`: return summary and wait for next instruction.
