---
name: sbl-science
version: 1.0.0
description: |
  SBL Campaign Sales Science — applies the Triple Constraint Model
  (Performance = PIC × CIQ × MRS) to turn campaign data into a structured
  scientific loop: Hypothesize → Design → Execute → Analyze → Prescribe → Iterate.
  Calculates live Platform Infrastructure Capacity, Conversation Intelligence
  Quality, and Market Resonance Strength scores from campaign data. Identifies
  the binding constraint and prescribes the specific fix.
  Use when asked to "run the science loop", "what's my PIC score", "analyze
  my campaign scientifically", "triple constraint", "campaign science",
  "what should I test next", or "why isn't my campaign converting".
  Invoked by /sbl when the user wants a scientific diagnosis. (sbl-stack)
allowed-tools:
  - Read
  - AskUserQuestion
triggers:
  - campaign science
  - triple constraint
  - run the science loop
  - what should I test next
  - why isn't my campaign converting
  - PIC score
  - CIQ score
  - MRS score
  - campaign sales science
  - CSS framework
---

# Campaign Sales Science Framework

**Core thesis:** Every campaign failure has a root cause in exactly one of three
constraints. Fix the right constraint and performance compounds. Fix the wrong one
and efficiency stays flat.

```
Performance = PIC × CIQ × MRS

PIC — Platform Infrastructure Capacity   (are messages getting through?)
CIQ — Conversation Intelligence Quality  (are conversations flowing correctly?)
MRS — Market Resonance Strength          (is the message landing with the market?)
```

The multiplicative relationship is non-negotiable: a score of 0.2 in any dimension
caps total performance at 0.2, regardless of how good the other two are.

---

## Step 0 — Auth and company context

Check if `SBL_COMPANY_ID` env var is set.

```bash
echo "COMPANY_ID: ${SBL_COMPANY_ID:-not_set}"
```

If not set, ask: "What is your sbl.so company ID?"

---

## Step 1 — Select the campaign to analyze

If `campaign_id` was passed from a calling skill, use it. Otherwise:

Call `sbl_list_campaigns` MCP tool with:
- `company_id`: from Step 0
- `response_format`: "json"

Show all campaigns. Campaigns with status RUNNING, SENDING, or ENDED (with
at least 50 delivers) are valid candidates.

Ask: "Which campaign do you want to run the science loop on? (enter ID)"

Minimum data threshold: 50 delivered messages. If a campaign has fewer than
50 delivers, warn: "Only [N] delivers recorded — results may not be
statistically meaningful. Continue anyway? (yes / no)"

---

## Step 2 — Pull all campaign data

Call `sbl_get_campaign` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: selected
- `response_format`: "json"

Extract and hold:
- `statistics` (all counts)
- `scoreData` (score, gaps, questions)
- `flow` (chat flow rules — count them)
- `followupMessages`
- `smartFollowupsConfig`
- `initialMessage`, `nonConnectedLeadsMessage`
- `communicationChannelToUse`
- `type` (campaign type)

Also call `sbl_get_campaign_analytics` MCP tool with:
- `company_id`: from Step 0
- `campaign_id`: selected
- `response_format`: "json"

Store the analytics insights for CIQ and MRS scoring.

---

## Step 3 — Calculate the Triple Constraint scores

### 3A — PIC: Platform Infrastructure Capacity

PIC measures whether messages are reaching people. Score 0–1.

Calculate from `statistics`:

```
total_attempted  = statistics.initiated + statistics.connectionRequestSent
                   + (failed actions if available from stats)

failed_rate      = failed_actions / total_attempted
                   [if failed_actions not directly available:
                    estimate from unsubscribed + no-delivery signals]

character_issues = infer from scoreData.gaps (if "character limit" gap exists → flag)

PIC_raw = 1 - failed_rate
PIC     = clamp(PIC_raw, 0, 1)
```

PIC component breakdown:
| Signal | Weight | Calculation |
|--------|--------|-------------|
| Message delivery rate | 50% | initiated / total_attempted |
| No character-limit gaps | 30% | 1 if no char-limit gap in scoreData, 0.5 if gap exists |
| No rate-limiting signals | 20% | 1 if no rate-limit in analytics, 0.5 if flagged |

If `scoreData.score` exists and is available, also factor in template health:
- Score 90+ → PIC infrastructure component = 0.95
- Score 70–89 → 0.80
- Score 50–69 → 0.65
- Score < 50 → 0.40

**PIC label:**
- 0.85–1.0 → ✅ Healthy infrastructure
- 0.65–0.84 → ⚠️ Infrastructure friction present
- < 0.65 → 🚨 Infrastructure is the binding constraint

---

### 3B — CIQ: Conversation Intelligence Quality

CIQ measures how well the AI handles conversations once started. Score 0–1.

Calculate from statistics and analytics:

```
reply_rate        = statistics.reverted / statistics.initiated
hi_rate           = statistics.actionNeeded / statistics.initiated
flow_rule_count   = count of rules in campaign.flow array
has_objection_handlers = count rules matching objection patterns
                         (look for "not interested", "already have", "how are you different")
```

CIQ component breakdown:
| Signal | Weight | Calculation |
|--------|--------|-------------|
| Reply rate vs benchmark (8%+ target) | 35% | min(reply_rate / 0.10, 1.0) |
| HI rate (lower is better — AI handling more) | 25% | 1 - min(hi_rate / 0.25, 1.0) |
| Chat flow coverage (rules count) | 20% | min(flow_rule_count / 10, 1.0) |
| Objection handler coverage | 20% | min(objection_rules / 3, 1.0) |

Also factor in:
- If analytics shows "AI escalating too often" → CIQ penalty of -0.15
- If analytics shows "repetitive follow-ups" or "wrong tone" → CIQ penalty of -0.10

**CIQ label:**
- 0.75–1.0 → ✅ Conversations flowing well
- 0.55–0.74 → ⚠️ Conversation gaps — AI missing signals
- < 0.55 → 🚨 Conversation intelligence is the binding constraint

---

### 3C — MRS: Market Resonance Strength

MRS measures how well the message fits the market. Score 0–1.

```
reply_rate_abs    = statistics.reverted / statistics.initiated
accept_rate       = statistics.initiated / (statistics.initiated + statistics.connectionRequestSent)
                    (LinkedIn only)
unsub_rate        = statistics.unsubscribed / statistics.initiated
```

MRS component breakdown:
| Signal | Weight | Calculation |
|--------|--------|-------------|
| Reply rate (absolute) | 40% | min(reply_rate / 0.15, 1.0) — 15% is excellent |
| Connection acceptance rate | 30% | min(accept_rate / 0.40, 1.0) — 40% is excellent |
| Low unsubscribe rate | 30% | 1 - min(unsub_rate / 0.05, 1.0) — 5% is ceiling |

Also factor in:
- If analytics mentions "value prop unclear" or "confused about offer" → MRS penalty of -0.15
- If analytics mentions "not relevant to me" or "wrong ICP" → MRS penalty of -0.20

**MRS label:**
- 0.70–1.0 → ✅ Message resonating with market
- 0.50–0.69 → ⚠️ Market fit friction — message or targeting
- < 0.50 → 🚨 Market resonance is the binding constraint

---

## Step 4 — Display the Triple Constraint Dashboard

```
CAMPAIGN SCIENCE REPORT — [campaign name] (ID: [campaign_id])
Generated: [today's date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRIPLE CONSTRAINT MODEL
Performance = PIC × CIQ × MRS

  PIC  [Platform Infrastructure]   [X.XX]  [███░░░░░░░] [label]
  CIQ  [Conversation Intelligence] [X.XX]  [████░░░░░░] [label]
  MRS  [Market Resonance]          [X.XX]  [██░░░░░░░░] [label]

  OVERALL EFFICIENCY:  [PIC × CIQ × MRS = X.XX]  ([XX]%)

  Current:    [P_current] efficiency
  Potential:  If all constraints reach 0.85 → [0.85³ ≈ 0.614] = 61% efficiency
  Gap to close: [delta] — [XX]× improvement available

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RAW STATISTICS
  Delivers:           [initiated]
  Replied:            [reverted]
  Reply rate:         [X.X%]
  Connection accepts: [X.X%]  (LinkedIn)
  HI escalations:     [actionNeeded] ([X.X%])
  Unsubscribed:       [X.X%]
  AI score:           [scoreData.score]/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BINDING CONSTRAINT: [PIC / CIQ / MRS — the lowest score]
[One sentence: what this means in plain English]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 5 — Identify the current hypothesis and what it proves

Ask (if not already clear from context):

"What was the hypothesis you were testing with this campaign?
(e.g. 'free trial offer will get higher reply rate than demo request' — or
describe the audience / message angle you were betting on)"

If the user doesn't have a defined hypothesis, help them reconstruct it:
- Look at the campaign objective and initial message
- State the implicit hypothesis: "Based on your campaign, the hypothesis appears to be:
  [reconstruct from message + ICP + goal]"

Then evaluate:

```
HYPOTHESIS VERDICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hypothesis: "[stated hypothesis]"

Evidence:
  Reply rate:     [X%] vs hypothesis expected [Y%]
  Deep engagement:[X%] — [above / below] typical 5–15% baseline
  Conversions:    [N] from [N] delivers = [X%] per 100

Verdict: [SUPPORTED / PARTIALLY SUPPORTED / REJECTED]

Why: [one paragraph — what the data says about whether the hypothesis holds.
     Reference the binding constraint — if MRS is low, the hypothesis about
     message-market fit is rejected. If CIQ is low, the hypothesis about
     AI handling is what failed, not the offer itself.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 6 — Generate the optimization prescription

Based on the binding constraint, produce the specific next action.

### If PIC is the binding constraint:

```
PRESCRIPTION: Fix infrastructure before scaling

Root cause: [X%] of attempts are failing to deliver.
Multiplying accounts without fixing this creates [X× failure volume].

Fix this cycle (Days 1–14):
  1. [If character limit gap detected]:
     Compress initial message from [N] chars → under 250 chars.
     BEFORE: [current initialMessage — first 100 chars]...
     AFTER:  [rewrite that says the same in ≤ 240 chars]

  2. [If template score < 70]:
     Run /sbl-optimize → apply all gaps → get score to 80+

  3. [If rate limiting suspected]:
     Reduce send frequency. Add more Fractional SDR profiles to
     spread load — each profile operates at safe velocity.

Expected PIC improvement: [X.XX] → 0.85+
Performance gain: [current P] → [0.85 × CIQ × MRS] = [new P]
```

### If CIQ is the binding constraint:

```
PRESCRIPTION: Fix the conversation flow

Root cause: The AI is [escalating too often / missing objections /
losing curiosity prospects] — conversations are starting but not converting.

[If HI rate > 15%]:
  The AI is escalating [N]% of conversations. Fix: add explicit
  handlers for the top 3 objections from your analytics.

[If curiosity gap detected — reply rate high but conversions low]:
  CURIOSITY GAP DETECTED
  [X%] of replies express curiosity but only [Y%] convert to buying signals.
  This is the most common CIQ failure. Fix:
  1. Replace trial-first sequence with education-first:
     - Message 1: Problem statement
     - Message 2: Case study / social proof
     - Message 3: Specific use case for their industry
     - Message 4: Soft CTA (demo, not trial)

  2. Add sentiment routing to chat flow:
     - IF prospect says "interesting" / "curious" / "tell me more"
       → route to education sequence, NOT trial link
     - IF prospect says "how much" / "let's do it" / "I'm ready"
       → route to booking link immediately

[If flow_rule_count < 8]:
  Chat flow has only [N] rules — too few to cover real conversations.
  Add handlers for:
  [list missing objection types based on analytics friction points]

Expected CIQ improvement: [X.XX] → 0.75+
Performance gain: [PIC × 0.75 × MRS] = [new P]
```

### If MRS is the binding constraint:

```
PRESCRIPTION: Fix message-market fit

Root cause: The message is not resonating — either the wrong ICP
is being targeted, or the value proposition is not matching their
actual pain.

[If accept_rate < 30%]:
  LOW CONNECTION ACCEPTANCE ([X%])
  People aren't even accepting connections. The opener is either:
  a) Too salesy — rewrite as a curiosity hook, not a pitch
  b) Wrong ICP — the people being targeted don't recognize the problem
  c) Profile mismatch — the sender profile doesn't match the audience

  Rewrite the connection request:
  BEFORE: [current nonConnectedLeadsMessage]
  AFTER:  [rewrite — curiosity hook, problem-led, under 200 chars]

[If reply_rate < 5%]:
  LOW REPLY RATE ([X%])
  Messages are being received but ignored. The value prop is missing.
  Test: Add a specific outcome stat to the opener.
  BEFORE: [current initialMessage]
  AFTER:  [rewrite with specific stat or case study woven in]

[If unsub_rate > 5%]:
  HIGH UNSUBSCRIBE RATE ([X%])
  Prospects are opting out — the message feels irrelevant.
  The ICP filter may be too broad. Consider:
  - Tightening ICP from [current description] to [more specific version]
  - Adding an industry qualifier to the opener

[Next hypothesis for MRS]:
  Test: [specific message change to test — angle, stat, hook, or ICP]
  Hypothesis: "[new hypothesis — e.g. 'adding a specific outcome stat
                will increase reply rate from X% to Y%']"
  Minimum delivers needed: 100 per variant for statistical significance

Expected MRS improvement: [X.XX] → 0.65+
Performance gain: [PIC × CIQ × 0.65] = [new P]
```

---

## Step 7 — Design the next experiment

Ask: "Do you want to design the next campaign experiment now? (yes / no)"

If yes:

```
EXPERIMENT DESIGN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT HYPOTHESIS:
"[State the specific hypothesis to test in one sentence]"

WHAT WE'RE CHANGING: [one variable only — PIC fix / CIQ fix / MRS fix]

CONTROL:   Campaign [current_id] — [current approach]
VARIANT:   New campaign — [single change being tested]

WHAT COUNTS AS A WIN:
  Metric to watch: [reply rate / conversion rate / deep engagement rate]
  Win threshold:   [current value] → [target value] (+[X%] improvement)
  Minimum delivers: 150 per variant before reading results

SUCCESS / FAIL CRITERIA:
  ✅ SUPPORTED if: [metric] ≥ [threshold] at ≥ 150 delivers
  ❌ REJECTED if:  [metric] < [current baseline] at ≥ 150 delivers
  ⏳ INCONCLUSIVE: run to 250 delivers if between

TIMELINE: [estimated days to 150 delivers at current send velocity]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next action: Run /sbl-create to build the variant campaign.
When you have 150+ delivers on each variant, run /sbl-science again
to compare them and read the result.
```

If no: skip to Step 8.

---

## Step 8 — 90-day optimization projection

Calculate what happens if all three constraints are improved over three cycles:

```
90-DAY PROJECTION (3 × 30-day optimization cycles)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TODAY (Cycle 0):
  PIC = [X.XX] | CIQ = [X.XX] | MRS = [X.XX]
  Efficiency = [P_current × 100]%
  Conversions per 100 sends ≈ [P_current × 100 × conversion_rate]

CYCLE 1 — Fix [binding constraint] (Days 1–30):
  PIC = [new_pic] | CIQ = [X.XX] | MRS = [X.XX]
  Efficiency = [new_P × 100]%
  Gain: +[delta × 100]% efficiency

CYCLE 2 — Fix [second constraint] (Days 31–60):
  PIC = [new_pic] | CIQ = [new_ciq] | MRS = [X.XX]
  Efficiency = [newer_P × 100]%
  Gain: +[delta × 100]% efficiency

CYCLE 3 — Fix [third constraint] (Days 61–90):
  PIC = [new_pic] | CIQ = [new_ciq] | MRS = [new_mrs]
  Efficiency = [final_P × 100]%
  Gain: +[delta × 100]% efficiency

TOTAL 90-DAY GAIN:
  [P_current × 100]% → [final_P × 100]% efficiency
  [final_P / P_current]× improvement = [final_P / P_current - 1 × 100]% gain
  Conversions per 100: [P_current × conversion_factor] → [final_P × conversion_factor]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 9 — Science loop summary and hand off

```
SCIENCE LOOP SUMMARY — [campaign name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONSTRAINT SCORES:
  PIC [X.XX] | CIQ [X.XX] | MRS [X.XX] → [P × 100]% efficiency

BINDING CONSTRAINT: [name]

HYPOTHESIS STATUS: [SUPPORTED / PARTIALLY SUPPORTED / REJECTED]

THIS CYCLE'S PRESCRIPTION:
  [1 sentence summary of the main fix]

NEXT EXPERIMENT:
  Hypothesis: "[next hypothesis to test]"
  Start: /sbl-create to build the variant

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Campaign Science runs on a loop:
  Hypothesize → Design → Execute → Analyze → Prescribe → Iterate

Each cycle fixes one constraint. Three cycles = 200–300% efficiency gain.
```

Route to:
- Fix exists in campaign copy → `/sbl-optimize [campaign_id]`
- New experiment needed → `/sbl-create`
- Infrastructure fix needed → show copy fix inline, no sub-skill needed
- If invoked by `/sbl` → return summary and wait for next instruction

---

## Reference: Triple Constraint benchmarks

| Constraint | Weak | Acceptable | Strong |
|-----------|------|-----------|--------|
| PIC | < 0.65 | 0.65–0.84 | 0.85+ |
| CIQ | < 0.55 | 0.55–0.74 | 0.75+ |
| MRS | < 0.50 | 0.50–0.69 | 0.70+ |
| Overall P | < 0.20 | 0.20–0.45 | 0.45+ |

**Minimum data thresholds for reliable scores:**
- PIC: 50 attempts (infrastructure failures are detectable early)
- CIQ: 30 replied conversations
- MRS: 100 delivers (reply patterns need volume)

**One constraint at a time.** The science loop fixes the lowest constraint
each cycle. Fixing two at once makes it impossible to know what drove the gain.
