---
name: high-intent-outreach
description: |
  Find the people engaging with posts in your market — competitors, adjacent
  vendors, the loud voices your buyers follow — and turn them into an
  approval-gated LinkedIn campaign. Suggests who to watch, previews the audience
  for free, tells you honestly whether they match, and launches only on your
  explicit word. Use for "reach out to people engaging with my competitors",
  "who's commenting on posts in my space", or "turn this post into pipeline".
---

# High-intent outreach

Someone who commented on a competitor's post this week is in-market right now.
A filter query only tells you someone matches a description. That difference is
the whole point of this workflow.

You do four things: help them decide **whose posts to watch**, show them **who
engaged** before spending anything, tell them honestly **whether that audience
matches**, and then run the standard build-bind-approve-launch chain.

The connection, launch, and reconciliation gates below are the same ones the
`sbl` prompt enforces. This file covers the sourcing and messaging legs.

## What you can and cannot do here

**You cannot find posts.** There is no search tool in this surface. You cannot
browse LinkedIn, fetch a post, resolve a company to its LinkedIn page, or verify
that a post exists. Do not invent, guess, or reconstruct a LinkedIn URL — a
fabricated URL either fails or, worse, points at a stranger.

**You can suggest who to watch.** That is reasoning about their market, and it
is genuinely useful. The division of labour is: you name the targets, the user
brings the URLs.

If the client you are running in has web search and the user wants you to use
it, you may — but say that you are doing so, and still have the user confirm the
final URL before it goes into any tool call.

## Step 1 — Understand what they sell

Before suggesting anyone, get:

- What they sell, in one sentence
- Who buys it — role, company size, industry, geography
- What problem the buyer has just before they go looking
- What the buyer is usually using instead today
- The offer and the CTA they want to land on

If they cannot answer "what does someone use instead of you", you do not yet
know enough to name competitors. Ask.

## Step 2 — Propose the intent map

Now suggest whose posts are worth watching. Give them a ranked shortlist across
these categories, because direct competitors are usually not the best source:

**Direct competitors.** Their engaged audience is the highest-intent group
available — these people are actively evaluating this category right now.
Downside: the comment sections are often other vendors, job seekers, and the
competitor's own employees. Say so.

**Adjacent tools in the same stack.** People engaging with a tool that sits
next to yours in the workflow have the problem but are not mid-evaluation with a
rival. Frequently the best yield.

**Loud practitioners and thought leaders.** Individuals your buyer follows.
Higher volume, looser fit, and the comment sections are more genuinely made up
of practitioners rather than vendors.

**Category-defining posts.** A post about the *problem* rather than a product —
"why our outbound stopped working", that kind of thing. Everyone who comments
has self-identified as having the problem.

For each suggestion give: who, why their audience matches this ICP, what kind of
person you expect in the comments, and the risk. Rank them by expected ICP
density, not by follower count. A post with 30 comments from exactly the right
people beats one with 400 from nobody.

Then say plainly: *"I can't pull these posts myself — pick one or two and paste
the post URLs."*

## Step 3 — Take the URL and judge the post

The URL must contain `/posts/`. Profile URLs, company pages, and Sales Navigator
URLs will not work — say which one they gave you and what to get instead.

Good posts to source from:

- Recent. Engagement decays; a six-month-old post is a cold list.
- Substantive comments, not just reaction emojis.
- On-topic for the problem, not a hiring post, a funding announcement, or a
  personal milestone. Congratulations-fishing posts produce terrible lists.

If they hand you a post you expect to yield badly, say so *before* the preview,
then preview anyway if they want. Being right in advance is how you earn the
right to be believed at Step 5.

## Step 4 — Preview for free

Call `sbl_preview_post_engagement`:

- `post_url` — the confirmed URL
- `mode` — `comments` or `likes`. Commenters cost more effort to produce and
  are meaningfully higher intent. Default to `comments`. Use `likes` for volume
  when comments are thin.
- `selector` — `any` or `keyword`. `likes` supports only `any`. `keyword`
  requires a `keyword`, and it filters on the comment text — useful for pulling
  just the people expressing a specific pain.
- `limit` — 1 to 25
- `idempotency_key`

This persists nothing and costs nothing. Say that before you run it.

## Step 5 — The honest read

This is the step that earns everything else. Look at who actually came back and
say whether they match the ICP from Step 1.

Report:

- How many look like real ICP matches, and what they have in common
- Who is clearly not a fit — vendors, job seekers, students, the wrong
  geography, the wrong company size
- Whether the post author is in the set
- Any segment worth splitting into its own angle

Then give a verdict, in one line: worth importing, worth importing only the
narrower keyword slice, or not worth importing.

**If the audience does not match, say do not import.** In the one recorded
production run of this route the previewed audience was largely the wrong
region and the wrong role, and the correct call was to stop. Never import a list
you have just described as wrong — offer a different post, a keyword filter, or
`comments` instead of `likes`.

## Step 6 — Approve the spend, then import

State plainly: import is billable, it charges for successfully imported leads,
and there is no cancel once it starts. Get approval for **this import
specifically**. A general "yes, go ahead" from earlier in the conversation does
not count.

Call `sbl_import_post_engagement_leads` with the `preview_id`, a fresh
`operation_id` (UUID), and an idempotency key.

If it returns `enqueue_unknown`, the outcome is genuinely unknown. **Do not mint
a new `operation_id` and do not retry.** Poll instead.

## Step 7 — Verify what actually attached

Poll `sbl_get_post_engagement_lead_import_status` with `wait_for_terminal`.
You will get inserted and conflict counts; conflicts are usually people already
on the campaign.

Then call `sbl_list_campaign_users` and report **that** number as the real one.
The import job's own count is not proof of attachment. If the two disagree, say
so and trust the campaign read.

## Step 8 — Write to the intent, not to the surveillance

The audience shares a context. Use it — but there is a line, and crossing it
kills the reply rate.

**Do not** name the post, the competitor, or the fact that you saw them comment.
"I noticed you commented on [Competitor]'s post" reads as surveillance and is
the single fastest way to get ignored or reported.

**Do** write to the problem the post was about, in the words the commenters
themselves used. If eleven people said some version of "our connect rates
collapsed", that phrase belongs in the opener. The relevance lands without ever
explaining how you found them.

Build the draft with `sbl_create_campaign_from_prompt` on the LinkedIn channel,
then read it back with `sbl_get_campaign`. Show the SBL quality score and the
named gaps, and say the score comes from SBL rather than from you. Fix editable
components with `sbl_update_campaign_component` under
`expected_status: "CREATED"` plus the current `expected_revision`, re-reading
after every change because the revision moves each time.

Be straight about what personalization is here: the sequence is templated and
shared across the list. The audience is what makes it relevant, not the copy.
Real personalization happens in the 1:1 reply.

## Step 9 — The Premium warning

Before the launch card, tell them this:

> LinkedIn only delivers a note with a connection request for Premium accounts.
> On a free account the invite still goes out, but the note is dropped and your
> prospect receives a bare connection request.

This is LinkedIn's behavior, not a product defect, and it is a known issue. For
this workflow it matters more than usual, because the whole value is the
context-matched opener — and on a free account that opener silently disappears.

If the sender is not on Premium, offer the honest options: upgrade the sending
account, or restructure so the first touch is a bare connect and the real
message lands after the connection is accepted.

## Step 10 — Bind, freeze, launch

Call `sbl_list_linkedin_channels` and require an explicit sender choice even if
only one comes back. Bind with `sbl_bind_linkedin_channel` using the current
`expected_revision`; if it is stale, re-read with `sbl_get_campaign` rather than
guessing.

Present the frozen launch card — sender, verified recipient count, exact first
message, follow-up sequence, campaign id, revision — and require the literal
token `LAUNCH`. Not "yes". Not "go".

Then `sbl_run_campaign` with `approval: true`, the frozen status and revision,
and one stable idempotency key.

A 202 is acceptance, not delivery. Dispatch has been observed to lag acceptance
by more than ten minutes. Poll read-only, at most six checks over two minutes,
then report pending honestly. Never retry.

## Step 11 — Hand off

Replies land in the human-intervention queue. Work them with
`sbl_list_human_intervention`, `sbl_get_conversation`, and
`sbl_reply_and_resolve`, requiring approval for each individual reply.

## What to say about scale

One post yields tens, not hundreds. Preview caps at 25. The recorded run
previewed 18 and attached 17. That is the honest shape of this: small,
high-intent lists, run often — not a bulk list build. Say so rather than letting
someone imagine thousands.

## Money moment

A competitor posts. Twenty minutes later their comment section is a live
campaign — with the mismatches called out before a single credit was spent.
