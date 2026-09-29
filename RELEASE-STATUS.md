# Hosted MCP status — 29 September 2026

The hosted endpoint remains `https://mcp.sbl.so/mcp` and exposes all 30 existing tool names. Tool availability is not proof that every workflow completes.

## Released

Latest MCP source `fba3ec202e556233c28a70c33fdc61d6dfda211b` is deployed as ECS `sbl-mcp:5` with image digest `sha256:67036a923ec076ba17031d7655dec232042fa780bd3aa07a899a8bc6d9c8032b`. Health reports **0.2.6 / 30 tools**. The earlier PR6–10 repair batch remains included.

- Component editing publishes its required arguments and keeps strict branch validation. A hosted authenticated draft edit and readback passed; a stale revision returned a structured conflict without overwriting the draft.
- Tool failures carry `isError` and structured categories. The deployed stale-revision check verified this behavior.
- Request deadlines include response bodies; status polls honor their remaining budget. Malformed successful JSON and retargeting receipts without an identifier are rejected. These cases have regression evidence in MCP PRs #8–#10; they were not fault-injected into production.
- The triage skill sends the accepted numeric-string status values (Stack PR #2).

Reconnect your MCP client to refresh its tool catalog. Desktop users must install [v0.2.6](https://github.com/SecondBrainLabs-SBL/sbl-stack/releases/tag/v0.2.6) to receive the updated schema. Both MCPB and legacy DXT files contain all 30 tools and the `sbl`/`high-intent-outreach` prompts. Checksums and build provenance are included with the release.

### Message-component follow-up released

- [App PR658](https://github.com/SecondBrainLabs-SBL/sbl-app/pull/658) infers an omitted channel from the owned campaign while preserving the caller's expected revision. Unconfigured channels receive a field-specific error.
- CREATED drafts can save message text before an invitation note is configured. Standard initial launches require a note or an explicit no-note choice; graph workflows retain their own launch validation.
- [MCP PR12](https://github.com/SecondBrainLabs-SBL/sbl-mcp/pull/12) makes the channel optional in the tool schema and prepares version 0.2.6.
- The old deployment reproduced the generic 400 on sandbox draft 8578. After deployment, a message-only edit with no channel field succeeded: revision 1→2, exact text readback, channel preserved, objective/audience still blank. A stale-revision edit returned a conflict and did not overwrite the text. The draft remains CREATED with zero sends. The screenshot's company624 campaign was not modified.
- App typechecks and 18 focused tests passed; MCP typecheck and 19 package/repair tests passed. User review approval was recorded before release. Manual Claude GUI installation and live launch-rejection fault injection were not performed.
- App Actions [36590950456](https://github.com/SecondBrainLabs-SBL/sbl-app/actions/runs/36590950456) deployed source `b14934fa0141e91349962538ef053553db264b8e` to client604/public-api282/tasker414. Tasker rebuilt as an affected dependency. Hosted MCP Actions [36591557159](https://github.com/SecondBrainLabs-SBL/sbl-mcp/actions/runs/36591557159) deployed MCP5. Desktop Actions [36590983991](https://github.com/SecondBrainLabs-SBL/sbl-mcp/actions/runs/36590983991) built the downloadable artifacts.
- Bundle SHA256: `3529830e41a6b2734fa1c65abdec0bd88db292e14196d39c48bab8838195d6f5`; both files are 597,614 bytes. Bundled Stack content is pinned to `92167c5bc59641e251e3ba020c2e87c3524947d8`.

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

Production SBL app branch is `main`, as declared in `sbl-app/branch-state.yml`. Subsequent production deployments must run through GitHub Actions, with the deployed source and outcome recorded here. The latest app and MCP releases above used Actions. The MCP repository now has separate manual Desktop bundle and hosted ECS deployment workflows; the app deployment workflow does not include the MCP service. The earlier MCP4 deployment preceded the Actions-only instruction.

