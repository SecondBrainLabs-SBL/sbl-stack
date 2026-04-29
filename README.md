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

## Install in 3 steps

### Step 1 — Install Claude Code

Download from [claude.ai/code](https://claude.ai/code). It's free to start.

Claude Code is the AI coding assistant from Anthropic that runs in your terminal.
SBL Stack turns it into a campaign manager for sbl.so.

---

### Step 2 — Install the SBL MCP server

The MCP server is what lets Claude talk to your sbl.so account.

```bash
pip install sbl-mcp
```

> Don't have pip? [Install Python first](https://python.org/downloads) — it comes with pip.

---

### Step 3 — Install SBL Stack

```bash
git clone https://github.com/SecondBrainLabs-SBL/sbl-stack
cd sbl-stack
./setup
```

The setup script will ask for your sbl.so email and password, then wire everything up automatically.

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

**`/sbl` isn't recognized in Claude Code**
→ Make sure you ran `./setup` and restarted Claude Code after.

**"sbl-mcp not found" during setup**
→ Run `pip install sbl-mcp` first, then re-run `./setup`.

**"Invalid credentials" error**
→ Check your sbl.so email and password. Reset at sbl.so if needed.

**Campaigns not loading**
→ Make sure `SBL_COMPANY_ID` is set correctly (sbl.so → Settings → Company).

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
- **MCP server** — [sbl-mcp](https://github.com/SecondBrainLabs-SBL/sbl-mcp) (Python, stdio)
- **API** — sbl.so public API

---

**© 2026 Second Brain Labs · [sbl.so](https://sbl.so)**
