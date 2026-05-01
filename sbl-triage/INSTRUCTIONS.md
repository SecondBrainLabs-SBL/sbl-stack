---
name: sbl-triage
version: 1.0.0
description: |
  SBL Daily Triage — checks the human intervention queue across all running
  campaigns, reads conversation threads for flagged leads, suggests persona-matched
  replies, and surfaces top analytics insights. The daily operations command.
  Use when asked to "check my inbox", "who needs attention", "triage my campaigns",
  "HI queue", or "what's happening in my campaigns today".
  Invoked by /sbl when HI queue is non-zero. (sbl-stack)
allowed-tools:
  - Read
  - AskUserQuestion
triggers:
  - check my inbox
  - who needs attention
  - triage my campaigns
  - HI queue
  - what's happening in my campaigns
  - daily triage
---

## Step 0 — Auth and company context

Check if `SBL_COMPANY_ID` env var is set.

```bash
echo "COMPANY_ID: ${SBL_COMPANY_ID:-not_set}"
```

If not set, ask for it.

---

## Step 1 — Get all running campaigns

Call `sbl_list_campaigns` MCP tool with:
- `company_id`: from Step 0
- `statuses`: ["RUNNING", "SENDING_INITIAL_MESSAGES", "RESENDING_INITIAL_MESSAGES", "SENDING_INITIAL_MESSAGE_FOLLOWUPS"]
- `response_format`: "json"

Show a brief table of active campaigns (name, ID, channel).

If no running campaigns: "No active campaigns right now. Run /sbl-create to launch one."

---

## Step 2 — Check HI queue for each active campaign

For each running campaign, call `sbl_list_human_intervention` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: each campaign ID
- `response_format`: "json"

Aggregate results across all campaigns:

```
HI QUEUE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Campaign                    | ID     | HI Leads
Chrome Enterprise - IT Heads| 1346   | 3
Demo Booking - Founders     | 1367   | 0
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total leads needing attention: [N]
```

If total is 0: "✅ No leads need attention right now. All conversations are being handled by the AI."
Then jump to Step 5 (analytics check).

---

## Step 3 — Triage each HI lead

For each campaign with HI leads, work through them one by one.

For each lead, call `sbl_get_conversation` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: the campaign
- `user_id`: the lead's user ID
- `response_format`: "markdown"

Display the conversation thread, then provide a recommended reply.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEAD: [name] | Campaign: [campaign name] | ID: [user_id]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONVERSATION THREAD:
[full conversation from sbl_get_conversation]

WHY AI FLAGGED THIS:
[infer from conversation — prospect shared contact details / asked something specific /
 pricing question / wants to go external / complex objection / high intent signal]

RECOMMENDED REPLY:
[Draft a reply in the campaign's tone and persona. Be specific — name the prospect,
 reference what they said, move toward the campaign objective.
 Keep under 300 characters for LinkedIn, under 500 for WhatsApp.]

INTENT SIGNAL: [HIGH / MEDIUM / LOW]
RECOMMENDED ACTION: [Send reply / Book call / Forward to sales / No action needed]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

After showing each lead's analysis, ask:
"Send this reply to [name]? (yes / edit / skip)"

- **Yes** → call `sbl_send_campaign_message` MCP tool with:
  - `campaign_id`: the campaign
  - `user_id`: the lead's user ID
  - `message`: the recommended reply
  - `response_format`: "json"
  - Confirm: "Sent ✅"

- **Edit** → ask for the edited message, then send it

- **Skip** → move to next lead

Work through all HI leads across all campaigns before moving to Step 4.

---

## Step 4 — HI queue summary

After working through all leads:

```
TRIAGE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Leads triaged:      [N]
Replies sent:       [N]
Skipped:            [N]

HIGH INTENT leads (likely to convert):
  [list any leads marked HIGH INTENT with their campaign and user ID]

FOLLOW UP TOMORROW:
  [any leads that need a follow-up from you in 24h]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 5 — Analytics pulse check

For each running campaign that has been active for 7+ days, call `sbl_get_campaign_analytics` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: each active campaign
- `response_format`: "json"

If insights exist, show the top 3 per category:

```
ANALYTICS PULSE — [campaign name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What's working:
  • [top insight — with lead count]

What's not working:
  • [top insight — with lead count]

Friction points:
  • [top insight — with lead count]

User pain points:
  • [top insight — with lead count]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If no insights yet: "Insights appear after the AI has enough conversations — usually 20–30 delivered messages with replies."

---

## Step 6 — Campaign health check

For each running campaign, call `sbl_get_campaign` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: each active campaign
- `response_format`: "json"

Pull stats from `statistics`:

```
CAMPAIGN HEALTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Campaign: [name]

Delivered:    [initiated]
Replied:      [reverted]
Action needed:[actionNeeded]
Unsubscribed: [unsubscribed]

Reply rate:    [reverted/initiated * 100]%  target: 8%+
HI rate:       [actionNeeded/initiated * 100]%

Status: [HEALTHY / WATCH / ACTION NEEDED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Flag if:
- Reply rate < 5% → "Low reply rate. Consider running /sbl-optimize on this campaign."
- HI rate > 15% → "High HI rate — the AI is escalating often. Review chat flow coverage."
- Unsubscribed > 5% → "High unsubscribe rate. Opener or targeting may be off."

---

## Step 7 — Summary and next actions

```
TRIAGE COMPLETE — [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HI leads handled:   [N]
Replies sent:       [N]
Campaigns checked:  [N]
High intent leads:  [N]

TODAY'S ACTIONS:
[numbered list of recommended actions — scale a campaign, optimize a draft,
 fix a low reply rate, follow up with a specific lead, etc.]

TOMORROW: Run /sbl-triage again to stay on top of the HI queue.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 8 — Hand off

If invoked standalone: done.
If invoked by `/sbl`: return summary and wait for next instruction.
