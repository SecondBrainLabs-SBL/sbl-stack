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

- Sales Navigator submission and attachment succeed after the app route repair. The failed company-126 test is now diagnosed: the provider rejected the connected account with HTTP 403 `errors/subscription_required`, “Sales Navigator seat required.” A connected LinkedIn sender alone is insufficient for Sales Navigator extraction; use an account connected with an active Sales Navigator seat. No new search was submitted against the rejected connection. Do not treat `queued` or `attached` as a successful lead import.
- Campaign end state/notification fixes are deployed in the app. Complete pending-message cleanup remains a separate open repair; ending does not recall messages already sent.
- Campaign generation can return an error after creating a draft. Check the campaign list before retrying creation.
- Hosted CSV file handoff and complete conversation retrieval remain open.
- The one-recipient LinkedIn test campaign 8571 launched through hosted MCP. Its initial recipient was excluded as already belonging to another campaign; the dashboard merge action transferred that one approved recipient into the test campaign. The hosted conversation readback now contains the exact approved test note with message status DELIVERED. Dashboard verification shows one outreach, one connection request sent, zero failures, and zero invitations accepted. This proves the invitation-with-note send path; recipient acceptance/read and a connected-recipient DM are not yet proven. Automatic conversations and follow-ups are disabled; the campaign remains running. No claim of 90% tool coverage is made.
- OAuth remains planned; current authentication uses bearer API keys.

Each subsequent released fix will update this page with its actual outcome. Keep partial, failed and untested workflows distinct from working ones.

## Deployment policy

Production SBL app branch is `main`, as declared in `sbl-app/branch-state.yml`. Subsequent production deployments must run through GitHub Actions, with the deployed source and outcome recorded here. The hosted MCP revision above was deployed before that instruction. The separate MCP repository currently has no deployment workflow; the app deployment workflow does not include the MCP service.
