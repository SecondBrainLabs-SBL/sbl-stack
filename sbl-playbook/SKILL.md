---
name: sbl-playbook
version: 1.0.0
description: |
  SBL Playbook Advisor — surfaces the right campaign strategy for your vertical,
  ICP, and goal. Returns: best lead source, benchmarks, message angle, chat flow
  pattern, smart follow-up timing, and what to watch on the dashboard.
  Use when asked to "what playbook should I use", "what campaign type for my ICP",
  "how should I run outreach for [vertical]", or "what's the strategy for [goal]".
  Invoked by /sbl-create and /sbl automatically. (sbl-stack)
allowed-tools:
  - Read
  - AskUserQuestion
triggers:
  - what playbook
  - campaign strategy
  - outreach strategy for
  - what campaign type
---

## Step 0 — Get context

If `vertical`, `goal`, and `channel` are already known from the calling skill, skip to Step 2.

Otherwise ask:

Ask the user (single question):
- What vertical best describes your ICP?
  - B2B SaaS / Tech founders
  - Edtech / Coaching / Course creators
  - Agencies / Lead gen teams
  - Recruiters / HR teams
  - Other (describe)
- What is the primary goal? (book a demo / fill a cohort / place a candidate / sign up a client / other)
- Which channel? (LinkedIn / WhatsApp / iMessage)

---

## Step 1 — Load the right playbook

Based on the vertical, read the corresponding file:

- B2B SaaS → read `playbooks/b2b-saas.md`
- Edtech / Coaching → read `playbooks/edtech.md`
- Agencies → read `playbooks/agencies.md`
- Recruiters → read `playbooks/recruiters.md`
- Other → use B2B SaaS as the base, note the gaps

---

## Step 2 — Route to the best campaign type

Match goal + context to the ranked campaign types in the playbook:

| If the user has... | Recommend |
|--------------------|-----------|
| An existing warm audience (webinar list, past leads, community) | Warm audience campaign |
| A specific LinkedIn post their ICP engaged with | Post engagement / Comment-to-DM |
| A community their ICP belongs to | Community signal outreach |
| Nothing yet — starting cold | Sales Navigator + ICP Filter |
| Previous campaigns with warm leads who went quiet | Retargeting campaign |

For recruiters: confirm whether they're targeting candidates, hiring managers, or both. Separate campaigns for each.

---

## Step 3 — Output the strategy brief

Return a structured brief in this format:

```
PLAYBOOK BRIEF — [Vertical] / [Goal] / [Channel]

RECOMMENDED CAMPAIGN TYPE
[Name the specific campaign type from the playbook]

WHY THIS TYPE
[One sentence on why it fits their context — signal they have, warmth level, benchmarks]

LEAD SOURCE
[Exact source to use in SBL — Community signal / Post Likes / Comment to DM / Sales Nav / CSV upload]

BENCHMARKS TO EXPECT
  CR acceptance:        [range from playbook]
  Reply rate:           [range]
  Hot leads per 100:    [range]

MESSAGE ANGLE
[2–3 sentences on the core message angle that works for this vertical + goal]
Character limit: under 250 for openers

KEY RULES FOR THIS VERTICAL
[3–5 bullet points pulled from the playbook — the non-obvious rules that change outcomes]

CHAT FLOW PATTERN
  ENGAGE:   [how to open the conversation]
  IDENTIFY: [what to surface/qualify]
  PITCH:    [how to frame the offer]
  OFFER:    [what the CTA is]

SMART FOLLOW-UP TIMING
  FU 1: [timing] — [reasoning / angle]
  FU 2: [timing] — [reasoning / angle]

DASHBOARD SIGNALS TO WATCH
[Table of healthy benchmarks and what to do when something's off]

WHAT FAILS IN THIS VERTICAL
[2–3 specific failure modes from the playbook + the fix]
```

---

## Step 4 — Hand off

If invoked standalone (user typed `/sbl-playbook`):
- Ask: "Want to create a campaign with this strategy? Run /sbl-create."

If invoked by `/sbl-create`:
- Return the brief and continue to the next step in `/sbl-create`.

If invoked by `/sbl`:
- Return the brief and wait for next instruction.
