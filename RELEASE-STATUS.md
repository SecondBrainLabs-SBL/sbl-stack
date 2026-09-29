# Hosted MCP status — 29 September 2026

The hosted endpoint remains `https://mcp.sbl.so/mcp` and exposes all 30 existing tool names. Tool availability is not proof that every workflow completes.

## Released

MCP source `0eb6e88cf13582289838f25bc7b0e8a2bdbaa465` is deployed as ECS `sbl-mcp:4` with image digest `sha256:08dd62ed9a564d873f25445e0d51958127b87960a67cced448c954c938048f42`.

- Component editing publishes its required arguments and keeps strict branch validation. A hosted authenticated draft edit and readback passed; a stale revision returned a structured conflict without overwriting the draft.
- Tool failures carry `isError` and structured categories. The deployed stale-revision check verified this behavior.
- Request deadlines include response bodies; status polls honor their remaining budget. Malformed successful JSON and retargeting receipts without an identifier are rejected. These cases have regression evidence in MCP PRs #8–#10; they were not fault-injected into production.
- The triage skill sends the accepted numeric-string status values (Stack PR #2).

Reconnect your MCP client to refresh its tool catalog. The existing downloadable v0.2.3 MCP bundle has not been rebuilt by this hosted deployment. Health still reports version 0.2.3; use the source/image identity above to distinguish this hosted repair batch.

## Still being verified or repaired

- Sales Navigator submission and attachment succeed after the app route repair, but the last provider job failed. Do not treat `queued` or `attached` as a successful lead import or blindly repeat a submission.
- Campaign end state/notification fixes are deployed in the app. Complete pending-message cleanup remains a separate open repair; ending does not recall messages already sent.
- Campaign generation can return an error after creating a draft. Check the campaign list before retrying creation.
- Hosted CSV file handoff and complete conversation retrieval remain open.
- The current one-recipient LinkedIn delivery journey is not yet verified. No claim of 90% tool coverage is made.
- OAuth remains planned; current authentication uses bearer API keys.

Each subsequent released fix will update this page with its actual outcome. Keep partial, failed and untested workflows distinct from working ones.
