# SBL Stack — What's Next

The v0.2.3 distribution pairs 30 MCP tools with seven public skill directories.
The MCP Bundle exposes one packaged orchestration prompt named `sbl`.

## Current safety floor

- Hosted Streamable HTTP endpoint: `https://mcp.sbl.so/mcp`
- API-key management: `https://app.secondbrainlabs.com/mcp-server`
- LinkedIn sender discovery before binding
- Explicit sender choice and revision-aware binding
- One run-owned CREATED draft and one manually approved recipient by default
- Literal launch approval, one stable idempotency key, and bounded read-only polling
- Honest separation of accepted, pending, running, and delivered states
- Durable `sbl_reply_and_resolve` for HI replies; no standalone-send fallback
- Separate end confirmation and explicit end-does-not-recall disclosure

## Next priorities

### OAuth for hosted web connectors

Add MCP OAuth 2.1 protected-resource metadata, authorization discovery, resource
binding, and tool-level security schemes before offering the hosted endpoint in
web connector directories. Bearer API keys remain a local-client integration and
must never be pasted into chat.

### MCP Bundle distribution

Validate the current `.mcpb` package on clean Claude Desktop installs and retain a
legacy `.dxt` compatibility asset only while supported and independently tested.
Publish artifact SHA-256 digests and the exact public skill-source commit with each
release.

### Safe resume and operations visibility

Expose durable operation status for launch and HI replies so clients can resume
with the same idempotency key after a timeout without repeating an effect. Keep
accepted, provider-ambiguous, delivered, and failed states distinct.

### Experiment management

Add an `/sbl-ab` flow only after it has explicit sample-size gates, separate
approval for every launch/end effect, and no automatic scaling or sender changes.

### Multi-company context

Allow users to choose a company explicitly while preserving company ownership
checks on every tool call. Never infer company context from stale state.

---

*Updated for sbl-mcp 0.2.3 / 30 tools.*
