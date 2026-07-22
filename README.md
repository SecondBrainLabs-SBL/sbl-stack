# SBL Stack

> Your AI campaign manager for [sbl.so](https://sbl.so) — type `/sbl` in Claude and it audits, creates, optimizes, and triages your campaigns automatically.

Built on playbook data from **320,000+ delivered messages across 1,200+ campaigns.**

---

## What you can do

| Command | What it does |
|---------|-------------|
| `/sbl` | Home screen — see all campaigns, surface what needs attention |
| `/sbl-create` | Answer 8 questions → get a full campaign built by AI |
| `/sbl-optimize` | Fix a draft campaign — score it, identify gaps, rewrite copy |
| `/sbl-triage` | See who needs a reply today, read the conversation, send with one click |
| `/sbl-playbook` | Get the right strategy for your vertical and ICP |
| `/sbl-retro` | Weekly report — what's working, what's not, what to do next week |

---

## Install — pick your path

SBL Stack is split into two pieces. Install both:

- **sbl-mcp** — the *tools* layer. Lets Claude talk to your sbl.so account.
- **sbl-stack** — the *skill* layer (this repo). The orchestration logic that turns the raw tools into `/sbl-create`, `/sbl-triage`, etc. **Optional** — sbl-mcp works on its own if you just want raw tool access.

### Option A — Claude Desktop (recommended, no terminal) 🎉

**Step 1 — Install the sbl-mcp extension (tools)**

1. Get your sbl.so API key at [sbl.so/api-integration](https://sbl.so/api-integration) → "Create new key" → copy the value.
2. Download `sbl-mcp-0.2.2.dxt` from [the latest sbl-stack release](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases/latest) (look under the "Assets" section).
3. Double-click the file → Claude Desktop's install dialog opens.
4. The extension will prompt for two values: your **sbl.so API Key** (required — paste what you copied in step 1) and an optional **API URL** (leave the default `https://api.sbl.so` unless your account is on a non-prod environment). Click Install.

> **No Python, Node, or other runtime needed.** As of v0.2.0 the extension is fully self-contained — Claude Desktop runs everything for you. v0.2.2 exposes the full 28-tool suite: campaign lifecycle, human-intervention resolution, retargeting, and three lead sources (CSV, LinkedIn, prompt-based).

You're done if you only want raw tools. Claude can now list campaigns, send messages, triage leads, etc., on your instruction.

**Step 2 — Add the SBL Stack skill (orchestration)** *(optional but recommended)*

1. On this repo's GitHub page, click **Code → Download ZIP**.
2. In Claude Desktop → **Settings → Skills** (or the skill upload UI in your version) → **Upload skill** → pick the zip you just downloaded.
3. Open any chat → invoke the **sbl** skill (via the skill picker, the `+` menu, or just say "use the sbl skill").

The skill audits your campaigns, surfaces what needs attention, and routes you to the right sub-flow (create / optimize / triage / retro / playbook / science). Each sub-flow lives in its own subfolder (`sbl-create/`, `sbl-triage/`, etc.) and the top-level `SKILL.md` reads them on demand.

> Don't have Claude Desktop? Download from [claude.ai/download](https://claude.ai/download). Free to start.

---

### Option B — Claude Code (terminal-based)

The MCP server itself now ships as a bundled Node DXT (see Option A) rather than a pip package, so there is not yet a documented one-line `claude mcp add` install for Claude Code. **Coming soon.**

In the meantime, if you live in the terminal:

#### Step 1 — Install Claude Code

Download from [claude.ai/code](https://claude.ai/code).

#### Step 2 — Install SBL Stack (skills only)

```bash
git clone https://github.com/SecondBrainLabs-SBL/sbl-stack
cd sbl-stack
./setup
```

The setup script asks for your **sbl.so API key** (create one at [sbl.so/api-integration](https://sbl.so/api-integration)) and wires up the `/sbl` skills.

#### Step 3 — Tools (sbl-mcp)

For the `sbl_*` MCP tools themselves under Claude Code, use the Claude Desktop DXT path (Option A) for now. Direct Claude Code registration will be documented once a supported invocation is published.

---

## First time? Here's what happens

```
You type:  /sbl

Claude:    Checking your campaigns...

           YOUR CAMPAIGNS
           ┌──────────────────────┬────────┬─────────┬───────────┬───────┐
           │ Name                 │ ID     │ Status  │ Channel   │ Score │
           ├──────────────────────┼────────┼─────────┼───────────┼───────┤
           │ Demo Booking - SaaS  │ 1367   │ DRAFT   │ LinkedIn  │ 64    │
           │ Chrome Enterprise    │ 1346   │ RUNNING │ LinkedIn  │  —    │
           └──────────────────────┴────────┴─────────┴───────────┴───────┘

           ⚠️  1 draft has a score of 64/100 — 2 gaps to fix.

           What do you want to do?
           A) Create a new campaign
           B) Fix the draft (campaign 1367)
           C) Triage today's HI queue
```

Pick an option and Claude takes it from there.

---

## Save your company ID (skip the prompt every time)

After setup, add this to your terminal profile (`~/.zshrc` on Mac):

```bash
export SBL_COMPANY_ID=<your-company-id>
```

Find your company ID in sbl.so → Settings → Company.

Reload your terminal (`source ~/.zshrc`) and you're set.

---

## The tools (28)

Everything the sbl-mcp extension gives Claude, grouped by what you'd use it for.

### Campaigns — read & inspect
| Tool | What it does |
|------|--------------|
| `sbl_list_campaigns` | List your campaigns (most recent first) — start here to find a campaign ID |
| `sbl_get_campaign` | Full details for one campaign: status, channel, persona, sequence, chat flow, stats |
| `sbl_get_campaign_analytics` | AI-generated insights — what's working, friction, objections, pain points |
| `sbl_list_campaign_users` | Leads in a campaign, filterable by status (HI queue, active chats, replies) |
| `sbl_get_conversation` | Full message thread with a specific lead |

### Campaigns — create & edit
| Tool | What it does |
|------|--------------|
| `sbl_create_campaign_from_prompt` | Generate a draft campaign from a natural-language prompt |
| `sbl_update_campaign_component` | Edit one draft component: ICP, objective, messages, sequence, or smart follow-ups |
| `sbl_create_retargeting_campaign` | Spin up a new draft targeting users from an existing campaign (by insight, purchase likelihood, or sentiment) |

### Campaign lifecycle
| Tool | What it does |
|------|--------------|
| `sbl_run_campaign` | Launch a draft campaign (requires your explicit approval) |
| `sbl_end_campaign` | End a running campaign |

### Messaging & human intervention
| Tool | What it does |
|------|--------------|
| `sbl_send_campaign_message` | Send a message to a (non-HI) campaign lead |
| `sbl_list_human_intervention` | See which leads need a human to step in |
| `sbl_reply_and_resolve` | Reply to an HI lead and resolve the flag in one durable step |
| `sbl_resolve_human_intervention` | Resolve an HI flag when no reply is needed |
| `sbl_add_user_to_campaign` | Add a single lead by LinkedIn URL or phone number |

### Leads — CSV import
| Tool | What it does |
|------|--------------|
| `sbl_upload_campaign_leads_csv` | Upload a leads CSV (up to 20 MB) for a campaign |
| `sbl_start_csv_lead_import` | Kick off the bulk import of an uploaded CSV |
| `sbl_get_csv_lead_import_status` | Check / wait on an import job |

### Leads — LinkedIn Sales Navigator
| Tool | What it does |
|------|--------------|
| `sbl_start_sales_navigator_lead_import` | Pull a Sales Navigator lead list into a draft campaign |
| `sbl_get_sales_navigator_lead_import_status` | Check that import's status |

### Leads — post engagement
| Tool | What it does |
|------|--------------|
| `sbl_preview_post_engagement` | Preview who liked/commented on a LinkedIn post — before importing anyone |
| `sbl_import_post_engagement_leads` | Import those engagers as campaign leads |
| `sbl_get_post_engagement_lead_import_status` | Check that import's status |
| `sbl_configure_post_engagement` | Set up comment-to-DM / like-to-DM behavior on a draft |

### Leads — AI prompt (native ICP)
| Tool | What it does |
|------|--------------|
| `sbl_create_prompt_lead_session` | Describe your ICP in plain English → get lead filters (same chat sbl.so customers use) |
| `sbl_refine_prompt_lead_session` | Refine those filters (up to 2 refinements) |
| `sbl_get_prompt_lead_session` | Check the session/export state |
| `sbl_approve_prompt_lead_sample` | Approve and start the real lead export (billable; default 10, max 100 leads) |

> Safety by design: nothing launches, sends, or bills without an explicit approval step — drafts stay drafts until you say go.

---

## The playbooks

SBL Stack ships with four proprietary playbooks built from real sbl.so campaign data.
Every campaign recommendation, benchmark, and copy suggestion comes from these.

| Vertical | Data behind it |
|----------|---------------|
| B2B SaaS & Tech Founders | 211,000 messages · 529 campaigns |
| Edtech & Coaching | 35,000 messages · 65 campaigns |
| Agencies & Lead Gen | 42,000+ messages · 496 campaigns |
| Recruiters & HR | 32,000+ messages · 113 campaigns |

---

## Troubleshooting

**`/sbl` isn't recognized**
→ *Claude Desktop:* re-install the `.dxt` and restart the app.
→ *Claude Code:* make sure you ran `./setup` and restarted Claude Code after.

**401 / "Unauthorized" when Claude calls a tool**
→ Your API key is missing, wrong, or revoked. Go to [sbl.so/api-integration](https://sbl.so/api-integration), create a new one, and re-install the `.dxt` in Claude Desktop, pasting the new key when prompted.

**Campaigns not loading**
→ Make sure `SBL_COMPANY_ID` is set correctly (sbl.so → Settings → Company).

**Lost the API key plaintext**
→ You can't recover it — sbl.so only shows it once. Revoke the old key at sbl.so/api-integration and create a fresh one.

---

## Coming soon

- `/sbl-leads` — add and manage leads without leaving Claude
- Auto-apply copy fixes from `/sbl-optimize` (needs `sbl_update_campaign` API)
- One-click campaign launch from Claude
- `/sbl-ab` — A/B test two campaign variants side by side

---

## Contributors

| Name | GitHub |
|------|--------|
| Ayush Singh | [@ayush488-glitch](https://github.com/ayush488-glitch) |
| Claude | Anthropic |
| Codex | OpenAI |

---

## Stack

- **Skills** — Claude Code markdown skill format
- **MCP server** — `sbl-mcp` (Node, stdio; bundled with esbuild into a single JS file). Source is private under the SBL org; the built `.dxt` ships as an asset on this repo's [Releases](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases).
- **API** — sbl.so public API

---

**© 2026 Second Brain Labs · [sbl.so](https://sbl.so)**
