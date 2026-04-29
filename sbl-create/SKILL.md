---
name: sbl-create
version: 1.0.0
description: |
  SBL Campaign Creator — walks through qualifying questions, matches your ICP to the
  right playbook strategy, builds a rich AI prompt, generates the campaign via the
  sbl.so API, then scores and surfaces gaps with specific copy fixes.
  Use when asked to "create a campaign", "new campaign", "set up outreach", or
  "I want to run a LinkedIn campaign".
  Invoked by /sbl automatically when the user picks "Create new campaign". (sbl-stack)
allowed-tools:
  - Read
  - AskUserQuestion
triggers:
  - create a campaign
  - new campaign
  - set up outreach
  - I want to run a LinkedIn campaign
  - start a campaign
---

## Step 0 — Auth and company context

Check if `SBL_COMPANY_ID` env var is set.

```bash
echo "COMPANY_ID: ${SBL_COMPANY_ID:-not_set}"
```

If not set, ask: "What is your sbl.so company ID? (Find it in sbl.so → Settings → Company)"

Store the company_id for all subsequent MCP calls in this session.

---

## Step 1 — Qualifying questions

Ask these as a single question block — do not ask one at a time:

```
To build the best possible campaign I need 8 quick answers:

1. What is your product or service? (one sentence — what it does and who it's for)

2. Who exactly are you targeting? (job title, company size, geography)

3. What is the primary goal of this campaign?
   a) Book a demo / discovery call
   b) Sign up / trial
   c) Fill a cohort or event
   d) Place a candidate / hire
   e) Other: ___

4. Which channel?
   a) LinkedIn
   b) WhatsApp
   c) iMessage

5. Which vertical best describes your ICP?
   a) B2B SaaS / Tech founders
   b) Edtech / Coaching / Course creators
   c) Agencies / Lead gen teams
   d) Recruiters / HR teams
   e) Other: ___

6. Do you have any social proof? Share it specifically:
   (numbers of customers, a specific client win, a stat, a case study — e.g.
   "helped 40 SaaS founders book demos in 3 weeks" or "used by 100+ teams")

7. What is your calendar or booking link? (paste the actual URL — it goes into
   the chat flow so the AI can share it with interested leads)

8. What lead source are you planning to use?
   a) Cold list — Sales Navigator + ICP Filter
   b) Post engagement — target people who liked/commented a specific post
   c) Community signal — target members of a specific LinkedIn community
   d) Comment-to-DM — auto-DM anyone who comments on a specific post
   e) Warm audience — existing leads, webinar lists, past customers
   f) Not sure — help me pick
```

---

## Step 2 — Load the playbook strategy

Read the appropriate playbook file based on the vertical from Step 1:
- B2B SaaS → read `playbooks/b2b-saas.md`
- Edtech → read `playbooks/edtech.md`
- Agencies → read `playbooks/agencies.md`
- Recruiters → read `playbooks/recruiters.md`

Then follow `sbl-playbook/SKILL.md` Step 2 to match the user's lead source to the right campaign type.

Pull from the playbook:
- Message angle for this vertical + goal
- Character limit guidance
- Chat flow pattern (ENGAGE / IDENTIFY / PITCH / OFFER)
- Smart follow-up timing
- Key rules specific to this vertical

---

## Step 3 — Build the campaign prompt

Construct a rich prompt for `sbl_create_campaign_from_prompt`. Incorporate all of:

```
PRODUCT: [answer 1]
TARGET ICP: [answer 2]
GOAL: [answer 3]
CHANNEL: [answer 4]
VERTICAL: [answer 5]

CAMPAIGN TYPE: [from playbook — community signal / post engagement / Sales Nav / warm audience]
LEAD SOURCE: [from answer 8, validated against playbook recommendation]

TONE AND ANGLE: [from playbook for this vertical]
  - [key message rule 1 from playbook]
  - [key message rule 2 from playbook]
  - Character limit: under 250 for connection request opener

SOCIAL PROOF TO WEAVE IN: [answer 6 — exact words from the user]

OBJECTIVES:
  Primary: [answer 3]
  CTA: [based on goal — book a call / sign up / enrol / apply]
  Calendar link for chat flow: [answer 7]

CHAT FLOW REQUIREMENTS:
  ENGAGE: [playbook pattern for this vertical]
  IDENTIFY: [what to surface about the lead's situation]
  PITCH: [how to frame the offer for this vertical]
  OFFER: low-friction next step — [calendar link / trial link / application]
  Objection handlers to include:
    - "Not interested right now" → [playbook-specific handler]
    - "Already have a solution" → [playbook-specific handler]
    - "How are you different?" → [playbook-specific handler]
  HI triggers: prospect shares contact details, prospect asks to go external,
               AI can't answer a question

SMART FOLLOW-UPS:
  FU 1: [timing from playbook] — [reasoning angle from playbook]
  FU 2: [timing from playbook] — [reasoning angle from playbook]

MUST INCLUDE:
  - Clear connection request message (non-connected leads)
  - Initial message after connecting
  - At least 2 follow-up messages
  - 8+ chat flow rules covering: interest, curiosity, objections, HI triggers
  - Smart follow-up config with reasoning for each delay
```

---

## Step 4 — Generate the campaign

Call the `sbl_create_campaign_from_prompt` MCP tool with:
- `company_id`: from Step 0
- `description`: the full prompt built in Step 3
- `channel`: from answer 4 (linkedin / whatsapp / imessage)
- `response_format`: "json"

Tell the user: "Generating campaign — this takes 10–20 seconds..."

On success, extract the campaign_id from the response payload.

---

## Step 5 — Fetch and display the full campaign

Call `sbl_get_campaign` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: from Step 4
- `response_format`: "json"

Display the full campaign in a structured format:

```
CAMPAIGN CREATED — ID: [campaign_id]

NAME: [name]
CHANNEL: [channel] | TYPE: [type] | STATUS: DRAFT

── INITIAL MESSAGE ───────────────────────────────────────
[initialMessage]

── CONNECTION REQUEST MESSAGE ─────────────────────────────
[nonConnectedLeadsMessage]

── FOLLOW-UPS ────────────────────────────────────────────
FU 1 (after [Xh]): [message]
FU 2 (after [Xh]): [message]

── CHAT FLOW ([N] rules) ─────────────────────────────────
[list all flow rules numbered]

── SMART FOLLOW-UPS ──────────────────────────────────────
Smart FU 1 (after [Xh]): [reasoning]
Smart FU 2 (after [Xh]): [reasoning]

── AI SCORE ──────────────────────────────────────────────
Score: [score]/100
Gaps: [list of gaps]
```

---

## Step 6 — Score and fix gaps

Read the `scoreData` from the campaign JSON.

For each item in `scoreData.gaps`, generate a specific fix:

**Gap: No social proof**
If the user provided social proof in Step 1 (answer 6):
  → Rewrite the initial message to include it:
  BEFORE: "[current initial message]"
  AFTER:  "[rewritten message with specific social proof woven in naturally]"

**Gap: No calendar link**
If the user provided a calendar link in Step 1 (answer 7):
  → Identify chat flow rule 1 (usually the strong interest / book a call rule)
  → Show the fix:
  BEFORE: "Here's my calendar link: <Calendar Link>"
  AFTER:  "Here's my calendar link: [actual URL from answer 7]"

**Gap: Opener too generic**
  → Rewrite the connection request message with a signal-based hook:
  BEFORE: "[current nonConnectedLeadsMessage]"
  AFTER:  "[rewritten with community/post/signal reference appropriate for the lead source]"

**For any other gaps:** generate specific copy based on the gap description and the qualifying answers.

Present each fix as a clear before/after block. Note: "Apply these in sbl.so → campaign [ID] → Edit before launching."

If `sbl_update_campaign` is available as an MCP tool, offer to apply the fixes automatically.

---

## Step 7 — Pre-launch checklist

```
Before launching campaign [campaign_id], complete:

[ ] LinkedIn profile connected: sbl.so → Settings → LinkedIn
[ ] AI persona trained: sbl.so → Settings → Persona (upload voice sample)
[ ] Calendar link added to chat flow rule #1  ← do this now if not auto-applied
[ ] Lead source configured in SBL: [specific source from answer 8]
[ ] ICP Filter set: [if Sales Navigator — minimum 80% match for precision]
[ ] Fractional SDR profiles added: sbl.so → Settings → Sender Profiles
    (each profile: 200 CR/week, 200 messages/day — SBL auto-enforces limits)
[ ] Check HI queue daily after launch: /sbl-triage

EXPECTED RESULTS (from playbook):
  CR acceptance:     [range]
  Reply rate:        [range]
  Hot leads/100:     [range]

Review campaign at sbl.so → Campaigns → [campaign_id]
```

---

## Step 8 — Hand off

If invoked standalone: "Campaign [ID] is ready to review. Run /sbl-triage once it starts sending to monitor the HI queue."

If invoked by `/sbl`: return summary and wait for next instruction.
