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

1. Get your sbl.so API key at [sbl.so/api-integration](https://sbl.so/api-integration) → "Create new key" → copy the `sk_live_…` value.
2. Download `sbl-mcp-<version>.dxt` from [the latest sbl-stack release](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases/latest) (look under the "Assets" section).
3. Double-click the file → Claude Desktop's install dialog opens → paste the API key → Install.

You're done if you only want raw tools. Claude can now list campaigns, send messages, triage leads, etc., on your instruction.

**Step 2 — Add the SBL Stack skill (orchestration)** *(optional but recommended)*

1. On this repo's GitHub page, click **Code → Download ZIP**.
2. In Claude Desktop → **Settings → Skills** (or the skill upload UI in your version) → **Upload skill** → pick the zip you just downloaded.
3. Open any chat → invoke the **sbl** skill (via the skill picker, the `+` menu, or just say "use the sbl skill").

The skill audits your campaigns, surfaces what needs attention, and routes you to the right sub-flow (create / optimize / triage / retro / playbook / science). Each sub-flow lives in its own subfolder (`sbl-create/`, `sbl-triage/`, etc.) and the top-level `SKILL.md` reads them on demand.

> Don't have Claude Desktop? Download from [claude.ai/download](https://claude.ai/download). Free to start.

---

### Option B — Claude Code (for developers, terminal-based)

Better if you live in the terminal.

#### Step 1 — Install Claude Code

Download from [claude.ai/code](https://claude.ai/code).

#### Step 2 — Install the SBL MCP server

```bash
pip install sbl-mcp
```

> Don't have pip? [Install Python first](https://python.org/downloads).

#### Step 3 — Install SBL Stack

```bash
git clone https://github.com/SecondBrainLabs-SBL/sbl-stack
cd sbl-stack
./setup
```

The setup script asks for your **sbl.so API key** (create one at [sbl.so/api-integration](https://sbl.so/api-integration)) and wires everything up.

**That's it.** Open Claude Code and type `/sbl`.

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

**"sbl-mcp not found" during setup** (Claude Code only)
→ Run `pip install sbl-mcp` first, then re-run `./setup`.

**401 / "Unauthorized" when Claude calls a tool**
→ Your API key is missing, wrong, or revoked. Go to [sbl.so/api-integration](https://sbl.so/api-integration), create a new one, and:
  - *Claude Desktop:* re-install the `.dxt` and paste the new key.
  - *Claude Code:* re-run `./setup` with the new key, or edit `~/.claude/settings.json` directly (look for `mcpServers.sbl.env.SBL_API_KEY`).

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
- **MCP server** — `sbl-mcp` (Python, stdio). Source is private under the SBL org; the built `.dxt` ships as an asset on this repo's [Releases](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases).
- **API** — sbl.so public API

---

**© 2026 Second Brain Labs · [sbl.so](https://sbl.so)**
