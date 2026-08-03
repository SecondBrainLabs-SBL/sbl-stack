---
name: sbl-create
version: 1.0.0
description: |
  SBL Campaign Creator — builds and inspects one run-owned draft, binds an
  explicitly chosen LinkedIn sender with revision protection, and defaults to one
  manually approved recipient before any separately approved launch.
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

## Required authority — read before Step 0

Before doing anything else, read `sbl/SKILL_MCP.md` completely. It is the
authoritative checklist for every LinkedIn write and for all launch, replay,
verification, resume, and end behavior. This create flow may collect inputs and
prepare a draft, but it must not weaken, replace, or duplicate that checklist. If
the checklist cannot be loaded, stop before any write.

The public v0.2.3 executable orchestration path is LinkedIn only. WhatsApp and
iMessage may be discussed as unsupported, deferred draft concepts, but they must
not proceed to campaign creation, sender binding, recipient addition, launch,
replay, or end through this flow.

## Step 0 — Auth and company context

Check if `SBL_COMPANY_ID` env var is set.

```bash
echo "COMPANY_ID: ${SBL_COMPANY_ID:-not_set}"
```

If not set, ask: "What is your sbl.so company ID? (Find it in sbl.so → Settings → Company)"

Store the company_id for all subsequent MCP calls in this session.

Before asking campaign questions or creating a draft, verify that exactly 30
`sbl_*` tools are visible and make `sbl_list_linkedin_channels` the first tool
call. If no channel is returned, pause and direct the user to
https://app.secondbrainlabs.com/settings?tab=communication. After they return,
relist; do not accept a verbal claim as proof. Show the redacted channel IDs/names
and require an explicit sender choice even when there is only one. Then run the
read-only `sbl_list_campaigns` smoke. Do not perform a write unless both reads pass.

---

## Step 1 — Qualifying questions

Ask these as a single question block — do not ask one at a time. Never ask for an
API key or authorization header:

```
To build the safest useful campaign I need 8 quick answers:

1. What is your product or service? (one sentence — what it does and who it's for)

2. Who exactly are you targeting? (job title, company size, geography)

3. What is the primary goal of this campaign?
   a) Book a demo / discovery call
   b) Sign up / trial
   c) Fill a cohort or event
   d) Place a candidate / hire
   e) Other: ___

4. Which channel?
   a) LinkedIn (supported executable orchestration)
   b) WhatsApp (unsupported/deferred concept only)
   c) iMessage (unsupported/deferred concept only)

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

8. Who is the single recipient for the first controlled proof?
   Share their full name and LinkedIn profile URL, and confirm this exact person is
   approved for the proof. The safe default is one manual recipient. CSV, prompt
   leads, Sales Navigator, post engagement, retargeting, and bulk imports require
   a separate request after this proof; do not select or start them by default.
```

If answer 4 is not LinkedIn, provide only a non-executable campaign concept and
stop before Step 2. Do not call any campaign create, bind, recipient, launch,
replay, or end tool for that concept.

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

CAMPAIGN TYPE: controlled one-recipient proof
LEAD SOURCE: one manually approved LinkedIn recipient from answer 8

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
- `channel`: `"linkedin"`
- `response_format`: "json"

Tell the user: "Generating campaign — this takes 10–20 seconds..."

On success, extract the campaign_id from the response payload.
This campaign is run-owned. Do not reuse a pre-existing draft for the controlled
proof and do not create a second draft after an ambiguous response.

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

Require status CREATED. Record the current positive `revision`, exact messages,
sequence timing, recipient count, and campaign-user count. Stop if the status or
content differs from the confirmed brief.

### Step 5A — Discover and bind the LinkedIn sender

For a LinkedIn campaign, call `sbl_list_linkedin_channels` again immediately before
binding to prove the explicitly chosen sender remains connected.

- If no channel is returned, pause and direct the user to
  https://app.secondbrainlabs.com/settings?tab=communication. When they return,
  call `sbl_list_linkedin_channels` again; do not rely on a verbal claim alone.
- Show only each channel's redacted ID and name. Require the user to choose the
  exact sender explicitly, even when there is only one.
- Call `sbl_get_campaign` immediately before binding and use its current revision.
- Call `sbl_bind_linkedin_channel` with numeric `company_id`, `campaign_id`, the
  selected numeric `channel_id`, and that exact `expected_revision`.
- On a revision conflict, refetch, show what changed, and ask before retrying. Do
  not overwrite, silently retry, launch, send, or call a provider.
- Refetch and verify the exact sender binding and new revision.

### Step 5B — Add the one approved recipient

Show the recipient name and LinkedIn URL from answer 8 and ask for a final explicit
confirmation. Only then call `sbl_add_user_to_campaign` once. Do not loop and do
not fall back to CSV, prompt leads, Sales Navigator, post engagement, retargeting,
or any bulk tool. Refetch the campaign users and require exactly one recipient for
this proof. Keep the LinkedIn URL only in the active conversation; do not save it.

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

If `sbl_update_campaign_component` is available, offer each allow-listed component
change separately. Refetch the current revision before each accepted change. Never
invent or call a generic campaign patch.

---

## Step 7 — Freeze and pre-launch checklist

```
Before launching campaign [campaign_id], complete:

[ ] Exactly 30 sbl-mcp 0.2.3 tools visible; read-only campaign smoke passed
[ ] Exact sender listed, explicitly chosen, and revision-aware binding verified
[ ] Exactly one manually approved recipient added; no bulk/import workflow used
[ ] AI persona trained: sbl.so → Settings → Persona (upload voice sample)
[ ] Calendar link added to chat flow rule #1  ← do this now if not auto-applied
[ ] Sender ID/name, recipient, exact messages, sequence timing, status CREATED,
    current revision, and all counts frozen and shown to the user
[ ] Check HI queue daily after launch: /sbl-triage

EXPECTED RESULTS (from playbook):
  CR acceptance:     [range]
  Reply rate:        [range]
  Hot leads/100:     [range]

Review campaign at sbl.so → Campaigns → [campaign_id]
```

Stop this sub-flow at the frozen checklist. Hand the exact verified snapshot to
`sbl/SKILL_MCP.md` Step 3. That authoritative checklist alone collects launch or
replay approval, creates and retains operation state, performs launch and bounded
reconciliation, decides whether a fresh replay approval is even eligible, and
reports pending residue. Standalone invocation does not bypass that handoff.

---

## Step 8 — Hand off

If invoked standalone, report the verified state and every residue. Any later
request to stop or end must be handed to `sbl/SKILL_MCP.md` Step 5; this file does
not collect end approval or execute end behavior.

If invoked by `/sbl`: return summary and wait for next instruction.
