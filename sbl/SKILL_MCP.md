---
name: sbl
description: |
  Run a safety-first sbl.so campaign proof from connection through a controlled
  one-recipient LinkedIn launch, bounded verification, and optional end.
---

# SBL controlled launch checklist

Operate one auditable sbl.so proof. Do not infer success from an accepted request,
hide pending state, or broaden the user's scope.

## Safety invariants

- Discover the server through the MCP `initialize` handshake followed by
  `tools/list`. Require exactly 30 unique `sbl_*` tool names with no duplicates
  and require
  `sbl_list_linkedin_channels`, `sbl_bind_linkedin_channel`,
  `sbl_run_campaign`, `sbl_get_campaign`, and `sbl_end_campaign`. Record the
  server version when the initialize handshake exposes it and require 0.2.3.
  Stop on a missing tool, duplicate name, different count, or conflicting
  version. If the host hides handshake metadata, say that the version is
  unverified rather than inventing it.
- Use `https://mcp.sbl.so/mcp` for remote MCP. Create or revoke the API key at
  `https://app.secondbrainlabs.com/mcp-server`.
- The SBL API key used as the bearer credential is secret. Never ask the user to
  paste it into chat and never print, log, screenshot, persist, save, or repeat
  that bearer credential or its `Authorization` header. If authentication fails,
  direct the user to the key page and wait for them to reconnect outside the chat.
- A launch idempotency key is different: it is non-secret operation state. Retain
  its exact full value in protected, non-user-visible resume state so the original
  launch can be replayed exactly when the checklist permits. User-visible output
  must show only its SHA-256 fingerprint, never the full idempotency key.
- Default to one run-owned CREATED LinkedIn draft and one manually approved
  recipient. Do not use CSV, prompt-lead, Sales Navigator, post-engagement, bulk
  import, retargeting, or multiple recipients unless the user separately expands
  the scope.
- Never use `sbl_send_campaign_message` as a fallback for campaign launch or an HI
  reply. HI replies must use `sbl_reply_and_resolve` with one stable operation key.

## 0. Establish company context and read-only proof

Ask for the numeric company ID if it is not already known. Run only these reads:

1. `sbl_list_linkedin_channels` for the company. This is the first tool call.
2. `sbl_list_campaigns` for the company.

Report the tool count, MCP version if visible, campaign-list result, and connected
channel count without exposing credentials or unnecessary contact data. Do not
perform a write until both reads succeed.

If no LinkedIn channel is returned, pause. Tell the user to connect one at
`https://app.secondbrainlabs.com/settings?tab=communication`. When the user says
it is connected, call `sbl_list_linkedin_channels` again; do not rely on their
statement alone.

Show each returned channel's redacted `id` and `name`. Require the user to choose
the exact sender explicitly, even when there is only one. Never choose by position,
recency, or guesswork.

## Campaign state interpretation

Use the exact status returned by `sbl_get_campaign`:

- CREATED = code 9: draft; not launched.
- SENDING_INITIAL_MESSAGES = code 4: launch effects may be underway.
- RUNNING = code 7: running state verified.
- ENDED = code 8: ended; ending does not recall prior effects.

Treat every other code, missing status, conflicting label/code, or unknown state
as ambiguous. Never map an unknown state to CREATED or use it to justify launch or
replay.

## 1. Freeze the proof scope

Before creating anything, show and confirm:

- company ID;
- chosen sender channel ID and name;
- one recipient's name and LinkedIn URL;
- campaign objective and exact channel (`linkedin`);
- exact connection request, initial message, follow-ups, sequence timing, and chat
  flow that will be placed in the draft;
- expected counts: one campaign, one sender, one recipient, zero bulk imports.

Treat the recipient as approved only after the user confirms that exact identity.
Keep contact data only in the active conversation; do not write it to a file or
include it in the resume block below.

## 2. Create, inspect, bind, and add one recipient

1. Call `sbl_create_campaign_from_prompt` once with the confirmed brief and
   `channel = "linkedin"`. Record the returned campaign ID as run-owned.
2. Call `sbl_get_campaign`. Require status CREATED and record its current positive
   revision. Stop if ownership, status, content, or counts differ from the frozen
   scope.
3. Call `sbl_bind_linkedin_channel` with numeric `company_id`, `campaign_id`, the
   explicitly chosen numeric `channel_id`, and that exact `expected_revision`.
4. If the bind reports a revision conflict, call `sbl_get_campaign`, show the
   changed revision/content, and ask the user whether to retry. Never silently
   overwrite or reuse a stale revision.
5. Call `sbl_get_campaign` again and verify the bound sender and new revision.
6. Ask for a final add-recipient confirmation, then call
   `sbl_add_user_to_campaign` once for the approved recipient. Do not loop or fall
   back to an import tool.
7. Read the campaign and its users. Require exactly the frozen sender, recipient,
   messages, sequence, and expected counts.

## 3. Launch with a compare-and-set gate

Present a final launch card containing the exact campaign ID/name, sender,
recipient, message sequence, current status, current revision, and counts. Ask:

> Type `LAUNCH` to launch this exact frozen one-recipient campaign.

Anything other than the literal word `LAUNCH` is not approval. After approval:

1. Create one caller-stable, non-secret idempotency key. Retain its exact full
   value in protected, non-user-visible resume state and record its SHA-256
   fingerprint for user-visible reconciliation. Never reveal the full key in
   status summaries and never generate a second key because a response is slow or
   ambiguous.
2. Call `sbl_run_campaign` with `approval = true`,
   `expected_status = "CREATED"`, the last verified `expected_revision`, and the
   stable `idempotency_key`.
3. Treat HTTP 202, an accepted operation, or a queued response as acknowledgment
   only—not delivery and not proof that the campaign is running.

## 4. Verify honestly and stop safely

After a launch timeout, transport error, or ambiguous response, never auto-retry.
Poll and reconcile first with read-only `sbl_get_campaign` calls: at most six
reads over no more than two minutes. Report the observed status, revision,
message counts, and statistics on every transition.

- If status is SENDING_INITIAL_MESSAGES (4), RUNNING (7), or ENDED (8), or if any
  accepted, running, pending, delivered, revision-change, message-count, or
  statistics-change evidence exists, do not replay. Report the exact evidence.
- If the campaign reaches RUNNING (7), report `RUNNING_VERIFIED`.
- If the bounded reconciliation ends in an ambiguous or in-progress state, report
  `PENDING`, preserve the exact original key in protected resume state along with
  the frozen snapshot, and stop. `PENDING` is a valid bounded result; resume later
  with another read-only reconciliation.
- Only if every reconciliation read still reports CREATED (9) and the revision,
  frozen messages, sequence, recipient count, message counts, and statistics are
  exactly unchanged may a single replay be considered. Show the exact frozen
  snapshot plus the original key's SHA-256 fingerprint and ask:

  > Type `REPLAY` to replay the original launch operation once with the same key.

  Prior `LAUNCH` approval does not authorize replay. Anything other than literal
  `REPLAY` is refusal. After `REPLAY`, retrieve the protected full key and call
  `sbl_run_campaign` at most once with that exact original idempotency key and the
  still-current CREATED revision. Never generate a new key and never perform a
  second replay. Reconcile read-only again; it may still finish as `PENDING` for
  later resume.
- If it fails or the frozen state changes, report the exact safe error and stop.

Never resend, use standalone send, or treat a new `LAUNCH` request as permission to
bypass this reconciliation and replay gate.

## 5. End only under separate confirmation

Launching never authorizes ending. If the user asks to stop, first explain that
ending prevents future campaign work but cannot recall a message already accepted
or delivered. Show the current campaign state and ask:

> Type `END` to end campaign [id].

Only literal `END` authorizes `sbl_end_campaign(confirm = true)`. Verify the ended
state with `sbl_get_campaign`. Do not claim recall, deletion, or rollback.

## 6. Residue and safe resume

Always finish with:

- final campaign status and revision;
- whether sender binding and the one recipient remain;
- acknowledged, delivered, pending, or unknown message state—never merge these;
- any draft, campaign-user row, operation, queue item, or outbound effect that
  remains;
- whether ending occurred and the explicit reminder that end does not recall;
- the next read-only action required.

Emit this sanitized, user-visible resume block when work is pending:

```text
SBL_RESUME
company_id: <numeric id>
campaign_id: <numeric id>
sender_channel_id: <numeric id>
recipient_user_id: <numeric id or pending>
status: <observed status>
revision: <positive integer>
launch_key_fingerprint: <SHA-256 fingerprint or not-created>
launch_key_retained: <true or false>
replay_used: <true or false>
polls_used: <0-6>
next_action: <one read-only step>
```

Separately retain the full launch idempotency key in protected, non-user-visible
resume state together with its campaign ID, fingerprint, replay-used flag, and
frozen launch snapshot. This protected operation state is non-secret, but it must
not be accidentally displayed; exact retention is required for a permitted
same-key replay. If the host cannot retain protected resume state, set
`launch_key_retained: false`, report that replay is unavailable, and never print
the full key as a workaround.

Never put the secret SBL bearer credential, authorization headers, raw phone
numbers, cookies, or session tokens in either resume state. Never put the full
launch idempotency key in the user-visible resume block.
