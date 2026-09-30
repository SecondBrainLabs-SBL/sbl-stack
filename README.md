# SBL Stack

> Your AI campaign manager for [sbl.so](https://sbl.so) — 30 MCP tools plus the `sbl` and
> `high-intent-outreach` prompts for audit, creation, triage, and a
> controlled one-recipient launch.

Built on playbook data from **320,000+ delivered messages across 1,200+ campaigns.**

The public v0.2.6 skill executes campaign creation, launch, replay, and end
orchestration for LinkedIn only. WhatsApp and iMessage may be discussed as
unsupported, deferred concepts, but this release does not run their launch
workflows.

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

1. Create your sbl.so API key at [SBL MCP settings](https://app.secondbrainlabs.com/mcp-server). Keep it out of chat, screenshots, logs, and plaintext documentation.
2. Download [sbl-mcp-0.2.6.mcpb](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases/download/v0.2.6/sbl-mcp-0.2.6.mcpb). Older clients can use the byte-identical [sbl-mcp-0.2.6.dxt](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases/download/v0.2.6/sbl-mcp-0.2.6.dxt). Checksums and build provenance are on the [release page](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases/tag/v0.2.6).
3. In Claude Desktop, open **Settings → Extensions → Advanced settings → Install Extension** and select the bundle.
4. The extension will prompt for two values: your **sbl.so API Key** (required — paste what you copied in step 1) and an optional **API URL** (leave the default `https://api.sbl.so` unless your account is on a non-prod environment). Click Install.

> **No Python, Node, or other user-installed runtime needed.** v0.2.6 exposes
> exactly 30 tools, including read-only LinkedIn sender discovery and
> revision-protected sender binding.

Upgrading from an older bundle? Install v0.2.6 through the same Extensions screen, confirm the installed version, and start a new chat. Each user should configure their own SBL API key. A hosted server update does not update a downloaded extension.

Try: **“List my SBL campaigns. Ask for my company ID if needed; do not change anything.”**

You're done if you only want raw tools. Claude can now list campaigns, send messages, triage leads, etc., on your instruction.

**Step 2 — Add the SBL Stack skill (orchestration)** *(optional but recommended)*

1. On this repo's GitHub page, click **Code → Download ZIP**.
2. In Claude Desktop → **Settings → Skills** (or the skill upload UI in your version) → **Upload skill** → pick the zip you just downloaded.
3. Open any chat → invoke the **sbl** skill (via the skill picker, the `+` menu, or just say "use the sbl skill").

The uploaded skill audits campaigns and loads its sub-flows on demand. The MCP
Bundle itself exposes two packaged prompts, `sbl` and `high-intent-outreach`. The `sbl` prompt includes the independent
controlled-launch checklist in `sbl/SKILL_MCP.md`.

> Don't have Claude Desktop? Download from [claude.ai/download](https://claude.ai/download). Free to start.

---

### Option B — Remote MCP URL (beta) — Claude Code, Codex, n8n, API 🌐

No server download is needed. The hosted endpoint is
**`https://mcp.sbl.so/mcp`**. It supports **OAuth sign-in** (recommended, no API key)
and bearer API keys.

#### Sign in with OAuth (recommended)

- **claude.ai / Claude Desktop:** Settings → Connectors → **Add custom connector** → URL `https://mcp.sbl.so/mcp` → sign in to SBL → choose a company → **Approve**.
- **Claude Code:** run `claude mcp add --transport http sbl https://mcp.sbl.so/mcp`, then `/mcp` → `sbl` → **Authenticate**.

Each connection is bound to **one company**, chosen on the consent screen. To use another company, disconnect and reconnect, choosing that company. Known issues: companies with identical names are not yet distinguished in the picker ([sbl-app#668](https://github.com/SecondBrainLabs-SBL/sbl-app/issues/668)), and a company mismatch returns an unclear error ([sbl-mcp#19](https://github.com/SecondBrainLabs-SBL/sbl-mcp/issues/19)).

To disconnect, open the SBL dashboard → MCP server page → **Connected apps** → **Disconnect**; access is revoked immediately. Access tokens last 1 hour and refresh automatically; refresh tokens last 30 days. See [hosted status](RELEASE-STATUS.md) for what was verified.

#### Use an API key instead

Supply the bearer key through a client environment
variable or secret store; never paste it into chat or commit it to configuration.

The hosted endpoint received the September 29 repair batch. See [current hosted status](RELEASE-STATUS.md) for verified behavior and remaining limitations. Existing downloaded MCP bundles are a separate distribution and are not updated by a server deployment.

Create or revoke the key at
[SBL MCP settings](https://app.secondbrainlabs.com/mcp-server).

#### Claude Code

```bash
claude mcp add --scope user --transport http sbl https://mcp.sbl.so/mcp \
  --header 'Authorization: Bearer ${SBL_API_KEY}'
```

Keep the literal `${SBL_API_KEY}` reference and set the value in the environment or
secret manager that starts Claude Code. Restart Claude Code and verify exactly 30
`sbl_*` tools. Optionally install the `/sbl` skills:

```bash
git clone https://github.com/SecondBrainLabs-SBL/sbl-stack && cd sbl-stack && ./setup
```

#### Codex CLI

Keep the key out of `config.toml` by naming its environment variable:

```toml
[mcp_servers.sbl]
url = "https://mcp.sbl.so/mcp"
bearer_token_env_var = "SBL_MCP_KEY"
```

Restart Codex — done.

`bearer_token_env_var` takes the variable name, not the key. Put the value in the
environment or secret manager used to start Codex.

#### n8n

Add an **MCP Client Tool** node → Endpoint `https://mcp.sbl.so/mcp` → Transport:
HTTP Streamable. Source the bearer authorization credential from an n8n credential
or secret expression; do not place the key directly in the workflow.

#### Anthropic API (build your own agent)

Configure a URL-type MCP server at `https://mcp.sbl.so/mcp` and load its
authorization token from your application's secret manager at runtime.

> **Note:** API-key setup and the Claude Desktop MCP Bundle (Option A) are unchanged
> and still work. Use OAuth above for claude.ai web connectors.

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

## The tools (30)

Everything the sbl-mcp extension gives Claude, grouped by what you'd use it for.

### Campaigns — read & inspect
| Tool | What it does |
|------|--------------|
| `sbl_list_campaigns` | List your campaigns (most recent first) — start here to find a campaign ID |
| `sbl_get_campaign` | Full details for one campaign: status, channel, persona, sequence, chat flow, stats |
| `sbl_get_campaign_analytics` | AI-generated insights — what's working, friction, objections, pain points |
| `sbl_list_campaign_users` | Leads in a campaign, filterable by status (HI queue, active chats, replies) |
| `sbl_get_conversation` | Full message thread with a specific lead |
| `sbl_list_linkedin_channels` | List connected LinkedIn senders as redacted ID/name records |

### Campaigns — create & edit
| Tool | What it does |
|------|--------------|
| `sbl_create_campaign_from_prompt` | Generate a draft campaign from a natural-language prompt |
| `sbl_update_campaign_component` | Edit one draft component: ICP, objective, messages, sequence, or smart follow-ups; message edits can retain the existing channel |
| `sbl_create_retargeting_campaign` | Spin up a new draft targeting users from an existing campaign (by insight, purchase likelihood, or sentiment) |
| `sbl_bind_linkedin_channel` | Bind an explicitly chosen sender to a CREATED draft using its current revision; never launches |

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
→ *Claude Desktop:* reinstall the `.mcpb` bundle (or the release's legacy `.dxt`
asset if your Claude build requires it) and restart the app.
→ *Claude Code:* make sure you ran `./setup` and restarted Claude Code after.

**401 / "Unauthorized" when Claude calls a tool**
→ Create or revoke a key at [SBL MCP settings](https://app.secondbrainlabs.com/mcp-server), update the client outside chat, and reconnect.

**Campaigns not loading**
→ Make sure `SBL_COMPANY_ID` is set correctly (sbl.so → Settings → Company).

**Lost the API key plaintext**
→ You cannot recover it. Revoke it at [SBL MCP settings](https://app.secondbrainlabs.com/mcp-server) and create a fresh one. Never paste it into chat.

---

## Coming soon

- `/sbl-leads` — add and manage leads without leaving Claude
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
- **MCP server** — `sbl-mcp` Desktop bundle 0.2.6, with a separately deployed hosted Streamable HTTP service. The current `.mcpb` bundle—and a verified legacy `.dxt` compatibility asset when provided—ships from this repo's [Releases](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases).
- **API** — sbl.so public API

---

**© 2026 Second Brain Labs · [sbl.so](https://sbl.so)**
