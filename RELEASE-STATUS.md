# Hosted MCP status — 29 September 2026

The hosted endpoint remains `https://mcp.sbl.so/mcp` and exposes all 30 existing tool names. Tool availability is not proof that every workflow completes.

## Released

MCP source `0eb6e88cf13582289838f25bc7b0e8a2bdbaa465` is deployed as ECS `sbl-mcp:4` with image digest `sha256:08dd62ed9a564d873f25445e0d51958127b87960a67cced448c954c938048f42`.

- Component editing publishes its required arguments and keeps strict branch validation. A hosted authenticated draft edit and readback passed; a stale revision returned a structured conflict without overwriting the draft.
- Tool failures carry `isError` and structured categories. The deployed stale-revision check verified this behavior.
- Request deadlines include response bodies; status polls honor their remaining budget. Malformed successful JSON and retargeting receipts without an identifier are rejected. These cases have regression evidence in MCP PRs #8–#10; they were not fault-injected into production.
- The triage skill sends the accepted numeric-string status values (Stack PR #2).

Reconnect your MCP client to refresh its tool catalog. Desktop bundle v0.2.5 separately packages these merged MCP repairs, all 30 tools, and the `sbl`/`high-intent-outreach` prompts. Download both supported bundle formats from the [v0.2.5 release](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases/tag/v0.2.5); its checksums and provenance identify the actual build. [MCP PR #11](https://github.com/SecondBrainLabs-SBL/sbl-mcp/pull/11) adds the versioned package metadata and manual Actions build; the release uses MCP source `4798a7bb990457365ce44fb67735917ec37dbeb8` and Stack content `92167c5bc59641e251e3ba020c2e87c3524947d8`. Existing users must install the new bundle to receive the repairs. Health still reports version 0.2.3; use the source/image identity above to distinguish this hosted repair batch.

## Verified live workflows

- Sales Navigator extraction is now verified end to end with an eligible connected account: a bounded 100-lead founder search reached `succeeded`; the lead-list API reports 100 users added. The list remains attached to an unlaunched draft. The previous failure was provider HTTP 403 `errors/subscription_required` on an account without a Sales Navigator seat. Connecting an eligible account resolved this case without another code patch. Do not treat `queued` or `attached` as completed extraction.
- The one-recipient LinkedIn test campaign 8571 launched through hosted MCP. Its initial recipient was excluded as already belonging to another campaign; the dashboard merge action transferred that one approved recipient into the test campaign. The hosted conversation readback now contains the exact approved test note with message status DELIVERED. Dashboard verification shows one outreach, one connection request sent, zero failures, and zero invitations accepted. This proves the invitation-with-note send path; recipient acceptance/read and a connected-recipient DM are not yet proven. Automatic conversations and follow-ups are disabled; the campaign remains running. No claim of 90% tool coverage is made.

- A separately approved second test from Hariharasudhan (sole sender channel 328) in campaign 8573 also returned the exact test message with status DELIVERED through hosted conversation readback. The imported prospect list was not used for either send test.

## Still being verified or repaired

- Campaign end state/notification fixes are deployed in the app. Complete pending-message cleanup remains a separate open repair; ending does not recall messages already sent.
- Campaign generation can return an error after creating a draft. Check the campaign list before retrying creation.
- Hosted CSV file handoff and complete conversation retrieval remain open. The live one-message thread read passed; this does not close pagination/completeness coverage.
- MCP sender binding adds a sender; replacing one currently needs the dashboard to remove the previous sender. Moving a lead out of another active campaign also requires the app’s existing Merge action. These are workflow coverage gaps, not a reason to remove existing tools.
- OAuth remains planned; current authentication uses bearer API keys.

Each subsequent released fix will update this page with its actual outcome. Keep partial, failed and untested workflows distinct from working ones.

## Deployment policy

Production SBL app branch is `main`, as declared in `sbl-app/branch-state.yml`. Subsequent production deployments must run through GitHub Actions, with the deployed source and outcome recorded here. The hosted MCP revision above was deployed before that instruction. The separate MCP repository has a Desktop bundle build workflow but no hosted deployment workflow; the app deployment workflow does not include the MCP service.
