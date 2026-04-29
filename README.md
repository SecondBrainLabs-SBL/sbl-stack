# SBL Stack

AI-powered campaign management for [sbl.so](https://sbl.so) — built as a Claude Code skill stack.

Type `/sbl` in any Claude Code session to audit, create, optimize, and triage your sbl.so campaigns using playbook intelligence from 320,000+ delivered messages.

---

## What it does

```
/sbl           Audit all campaigns, surface what needs attention, route to the right action
/sbl-create    New campaign wizard — qualifying questions + playbook strategy + AI generation
/sbl-optimize  Fix draft campaigns — score analysis, gap detection, specific copy fixes
/sbl-triage    Daily HI queue — read conversation threads, draft replies, send with approval
/sbl-playbook  Strategy advisor — best campaign type + benchmarks for your vertical and ICP
/sbl-retro     Weekly retro — what's working, what's not, ranked actions for next week
```

---

## Install

**Prerequisites:**
- [Claude Code](https://claude.ai/code) installed
- `sbl-mcp` Python package installed (`pip install sbl-mcp`)
- An sbl.so account

**Run setup:**

```bash
git clone https://github.com/sbl-so/sbl-stack
cd sbl-stack
./setup
```

The setup script:
1. Copies skill files to `~/.claude/skills/sbl/`
2. Adds the `sbl` MCP server to `~/.claude/settings.json`
3. Prompts for your sbl.so credentials if not set

**Optional — set your company ID to skip the prompt:**

```bash
export SBL_COMPANY_ID=<your-company-id>
```

Add to your `~/.zshrc` or `~/.bashrc` to persist it.

---

## Usage

Open any Claude Code session and type:

```
/sbl
```

That's it. Claude audits your campaigns, surfaces what needs attention, and asks what to do.

---

## The playbooks

SBL Stack ships with four proprietary playbooks built from real campaign data:

| Playbook | Data |
|----------|------|
| B2B SaaS & Tech Founders | 211,000 messages · 529 campaigns |
| Edtech & Coaching | 35,000 messages · 65 campaigns |
| Agencies & Lead Gen | 42,000+ messages · 496 campaigns |
| Recruiters & HR | 32,000+ messages · 113 campaigns |

Each playbook contains: benchmark data by campaign type, message angle guidance, chat flow patterns, smart follow-up timing, and diagnostic tables for fixing what's not working.

---

## MCP tools used

The SBL Stack skills call these tools from the `sbl-mcp` server:

| Tool | Used by |
|------|---------|
| `sbl_list_campaigns` | /sbl, /sbl-retro |
| `sbl_get_campaign` | /sbl-optimize, /sbl-retro, /sbl-triage |
| `sbl_create_campaign_from_prompt` | /sbl-create |
| `sbl_list_campaign_users` | /sbl-retro |
| `sbl_get_conversation` | /sbl-triage |
| `sbl_get_campaign_analytics` | /sbl-triage, /sbl-retro |
| `sbl_list_human_intervention` | /sbl, /sbl-triage |
| `sbl_send_campaign_message` | /sbl-triage |
| `sbl_update_campaign` | /sbl-optimize *(coming soon)* |

---

## Roadmap

- [ ] `sbl_update_campaign` — auto-apply copy fixes from /sbl-optimize
- [ ] `sbl_launch_campaign` — launch from draft to live without leaving Claude
- [ ] `sbl_get_company` — auto-pull company context for richer prompts
- [ ] `/sbl-leads` — add and manage leads from within Claude
- [ ] `/sbl-ab` — A/B test management across campaign variants

---

## Stack

- **Skills:** Markdown skill files (Claude Code skill format)
- **MCP server:** [sbl-mcp](https://github.com/sbl-so/sbl-mcp) — Python, stdio transport
- **API:** sbl.so public API (`api.sbl.so`)

---

**© 2026 Second Brain Labs · sbl.so**
