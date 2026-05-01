---
name: sbl-retro
version: 1.0.0
description: |
  SBL Weekly Retrospective — reviews all campaign metrics from the past 7 days,
  surfaces what's working vs what's not, benchmarks against playbook data,
  and gives a ranked action list for next week.
  Use when asked to "weekly retro", "how are my campaigns doing", "campaign report",
  "what should I focus on this week", or "review last week".
  Invoked by /sbl when the user wants a campaign health overview. (sbl-stack)
allowed-tools:
  - Read
  - AskUserQuestion
triggers:
  - weekly retro
  - how are my campaigns doing
  - campaign report
  - what should I focus on this week
  - review last week
  - campaign performance
---

## Step 0 — Auth and company context

Check if `SBL_COMPANY_ID` env var is set.

```bash
echo "COMPANY_ID: ${SBL_COMPANY_ID:-not_set}"
```

If not set, ask for it.

---

## Step 1 — Get all campaigns

Call `sbl_list_campaigns` MCP tool with:
- `company_id`: from Step 0
- `response_format`: "json"

Also call with `is_archived: false` to get only active ones.

Separate campaigns by status:
- RUNNING / SENDING_INITIAL_MESSAGES / SCHEDULED → "Active"
- CREATED → "Drafts"
- ENDED → "Completed"

---

## Step 2 — Deep fetch every active campaign

For each active campaign, call `sbl_get_campaign` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: each active campaign
- `response_format`: "json"

Extract from each:
- `statistics` object (all counts)
- `name`, `communicationChannelToUse`, `type`
- `scoreData` (if present)
- `createdAt` (to calculate age)

Calculate for each campaign:
- Reply rate = `statistics.reverted / statistics.initiated * 100`
- HI rate = `statistics.actionNeeded / statistics.initiated * 100`
- Connection rate = `statistics.initiated / (statistics.initiated + statistics.connectionRequestSent) * 100` (if LinkedIn)
- Unsubscribe rate = `statistics.unsubscribed / statistics.initiated * 100`

---

## Step 3 — Get analytics for active campaigns

For each active campaign with `statistics.initiated > 20`, call `sbl_get_campaign_analytics` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: each active campaign
- `response_format`: "json"

Store insights grouped by category.

---

## Step 4 — Load playbook benchmarks for comparison

For each active campaign, detect the vertical (from campaign name, objective, or targetUsers description) and load the relevant playbook file:
- B2B SaaS → `playbooks/b2b-saas.md`
- Edtech → `playbooks/edtech.md`
- Agencies → `playbooks/agencies.md`
- Recruiters → `playbooks/recruiters.md`

Pull the benchmark ranges for the campaign's lead source type (community signal / post engagement / Sales Nav / warm audience).

---

## Step 5 — Build the retro report

```
SBL WEEKLY RETRO — [date range]
Company: [company_id]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIVE CAMPAIGNS ([N])

┌─────────────────────────────┬──────┬──────────┬───────────┬──────────┬──────────┬────────┐
│ Campaign                    │ Age  │ Delivered│ Reply Rate│ HI Rate  │ Unsub    │ Status │
├─────────────────────────────┼──────┼──────────┼───────────┼──────────┼──────────┼────────┤
│ [name]                      │ [d]  │ [N]      │ [X%]      │ [X%]     │ [X%]     │ [color]│
└─────────────────────────────┴──────┴──────────┴───────────┴──────────┴──────────┴────────┘

Status key: 🟢 Healthy  🟡 Watch  🔴 Action needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAMPAIGN DEEP DIVES

[For each campaign, generate a short paragraph:]

[Campaign name] — [AGE]d old, LinkedIn/WhatsApp
  Delivered [N] messages. Reply rate [X%] vs [playbook benchmark]% benchmark.
  [ABOVE / BELOW / AT] benchmark by [delta].
  Top insight: "[best insight from analytics if available]"
  HI queue: [N] leads needing attention.
  Verdict: [one sentence — what's happening and why]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT'S WORKING THIS WEEK
[Top 3 positive signals across all campaigns — specific, with numbers]

WHAT'S NOT WORKING
[Top 3 problems — specific, with numbers, with root cause diagnosis]

FRICTION PATTERNS (from analytics)
[Top friction points mentioned across conversations — what's creating drop-off]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DRAFTS WAITING TO LAUNCH ([N])

[List CREATED campaigns with their AI scores]
Campaign: [name] | Score: [X]/100 | Gaps: [list]
→ Action: Run /sbl-optimize before launching

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT WEEK PRIORITY LIST

Ranked by impact:

1. [ACTION] — [campaign name]
   Why: [one sentence on what this fixes or improves]
   How: [specific step — /sbl-optimize, add Fractional SDRs, fix the opener, etc.]

2. [ACTION] — [campaign name]
   Why: [reason]
   How: [step]

3. [ACTION]
   Why: [reason]
   How: [step]

[Continue for all actionable campaigns — scale winners, fix problems, launch drafts]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISIONS FOR THIS WEEK

Scale: [campaigns performing above benchmark — add Fractional SDR profiles]
Fix:   [campaigns with fixable problems — /sbl-optimize]
Pause: [campaigns performing significantly below benchmark after 300+ delivers]
Launch:[drafts with score 80+ that are ready]
Kill:  [campaigns that have been running 30+ days with reply rate under 3% — archive]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 6 — Status color logic

Apply status colors based on reply rate vs playbook benchmark:

| Reply rate vs benchmark | Status |
|------------------------|--------|
| > benchmark + 20%      | 🟢 Healthy — scale it |
| Within benchmark range | 🟢 Healthy |
| 50–100% of benchmark   | 🟡 Watch — investigate |
| < 50% of benchmark     | 🔴 Action needed |
| < 2% absolute          | 🔴 Action needed — pause or rewrite |

Special flags:
- HI rate > 20% → "🟡 Chat flow gaps — AI escalating too often"
- Unsubscribe rate > 5% → "🔴 Opener or targeting is wrong"
- 0 messages delivered after 7 days → "🔴 Check LinkedIn connection or sender profile setup"

---

## Step 7 — Hand off

If invoked standalone: "Run /sbl-triage to handle today's HI queue. Run /sbl-optimize [campaign_id] to fix any campaign with gaps."

If invoked by `/sbl`: return summary and wait for next instruction.
