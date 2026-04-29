# SBL Stack — What's Next

The SBL Stack v1.0 ships 6 skills and 9 MCP tools. Here is the prioritized build plan.

---

## Priority 1 — Close the optimization loop

**Problem:** `/sbl-optimize` can diagnose gaps and write copy fixes, but can't apply them.
The user has to manually paste fixes into the sbl.so UI.

**What to build:**

### `sbl_update_campaign` MCP tool
Needs a new API endpoint in sbl-app public-api first.

**API endpoint needed:**
```
PATCH /campaigns/:id
Body: {
  initialMessage?:        string
  nonConnectedLeadsMessage?: string
  followupMessages?:      { id: string, message: string, followupAfterInMs: number }[]
  flow?:                  string[]
  smartFollowupsConfig?:  { delayInMs: number[], followupMessageReasoning: string[] }
  objective?:             string
  targetUsers?:           { title: string, description: string }
}
```

**MCP tool:** `sbl_update_campaign(campaign_id, fields)` → calls PATCH, returns updated campaign.

**Impact:** `/sbl-optimize` becomes fully autonomous — detects gaps, generates fixes, applies them in one command. Score goes from 64 → 90+ without the user touching the UI.

**Who builds it:** Lokesh (sbl-app public-api) + MCP team (sbl-mcp Python tool)
**Estimated effort:** 1 day (API) + 2 hours (MCP tool)

---

## Priority 2 — One-click launch from Claude

**Problem:** After creating or optimizing a campaign, the user still has to go to sbl.so UI to launch it.

**What to build:**

### `sbl_launch_campaign` MCP tool
Needs to know what endpoint changes campaign status to active.

**Check:** Does `PATCH /campaigns/:id` with `{ status: 2 }` work? Or is there a dedicated launch endpoint?

**MCP tool:** `sbl_launch_campaign(campaign_id)` → changes status from CREATED to active.

**Skill update:** Add a "Launch now?" prompt at the end of `/sbl-create` and `/sbl-optimize`.

**Impact:** Full campaign lifecycle — create, optimize, launch — without leaving Claude.

---

## Priority 3 — Company context for richer prompts

**Problem:** `/sbl-create` asks the user to describe their product every time. sbl.so already has this data.

**What to build:**

### `sbl_get_company` MCP tool
```
GET /companies/:id
Returns: name, description, website, industry, logo
```

**Skill update:** `/sbl-create` calls `sbl_get_company` first → pre-fills product context → asks the user only for what's missing (ICP, goal, channel, social proof, calendar link).

**Impact:** 8 qualifying questions → 4. Faster, less friction, better context.

---

## Priority 4 — Lead management from Claude

**Problem:** Adding leads to campaigns requires the sbl.so UI or manual CSV uploads.

**What to build:**

### `/sbl-leads` skill
- Add a single lead: `sbl_add_user_to_campaign(campaign_id, name, phone/linkedin)`
- Bulk add from a pasted list (Claude parses names + contacts → loops through `sbl_add_user_to_campaign`)
- Show current lead counts and status breakdown

**Impact:** Sales reps can add leads from Claude without switching to the sbl.so UI.

---

## Priority 5 — A/B test management

**Problem:** Running two campaign variants and picking the winner requires manually tracking metrics in the UI.

**What to build:**

### `/sbl-ab` skill
- Takes two campaign IDs (or creates a duplicate automatically)
- Polls both every 24h via `sbl_get_campaign`
- After 200+ delivers each, shows side-by-side: reply rate, HI rate, sentiment
- Recommends the winner
- When `sbl_update_campaign` ships: can pause the loser and scale the winner

---

## Priority 6 — PyPI distribution

**Problem:** `pip install sbl-mcp` doesn't work yet — the package isn't on PyPI.

**What to build:**

1. Move `sbl-mcp` from the internal MCP project to a public repo: `SecondBrainLabs-SBL/sbl-mcp`
2. Add `pyproject.toml` with proper metadata (name, version, entry point)
3. Publish to PyPI: `python -m build && twine upload dist/*`
4. Update `sbl-stack/setup` to install from PyPI

**Impact:** `./setup` works end-to-end for any sbl.so customer. No manual cloning.

**Estimated effort:** 2–3 hours

---

## Priority 7 — One-line install

Once PyPI is live, the entire install becomes:

```bash
pip install sbl-mcp && curl -s https://raw.githubusercontent.com/SecondBrainLabs-SBL/sbl-stack/main/setup | bash
```

No git clone. No manual steps.

---

## Backlog (post v1.1)

| Feature | Description |
|---------|-------------|
| `/sbl-schedule` | Set up campaign send schedule from Claude |
| `/sbl-persona` | Train the AI persona (upload voice sample, set tone) |
| Slack integration | Daily HI queue summary posted to a Slack channel |
| Webhook support | Trigger `/sbl-triage` automatically when new HI lead appears |
| Multi-company | Switch between company accounts within the same skill session |
| Voice note detection | Detect when a lead sends a voice note, transcribe, suggest reply |

---

## Immediate next actions (this week)

1. **Lokesh:** Add `PATCH /campaigns/:id` endpoint to sbl-app public-api
2. **MCP team:** Implement `sbl_update_campaign` in sbl-mcp once endpoint is live
3. **MCP team:** Publish `sbl-mcp` to PyPI
4. **Ayush:** Test `/sbl-create` end-to-end on a real new campaign
5. **Ayush:** Add GitHub topics to this repo: `claude-code`, `mcp`, `linkedin-outreach`, `sbl`
6. **Ayush:** Create `SecondBrainLabs-SBL/sbl-mcp` as the companion public repo

---

*Last updated: April 2026*
