# Connector runtime contract

OCL is connector-neutral: the same scoped Bearer key works through REST,
remote MCP, and the SDK. A connector should discover the key's exact scope
before requesting context instead of guessing module names or limits.

```text
GET  /v1/capabilities
POST /v1/activate
GET  /v1/lifecycle
POST /v1/get-context
POST /v1/resolve-noun
POST /v1/explain-field
POST /v1/get-join-path
POST /v1/validate-write-intent
```

## Integration sequence

1. Call `GET /v1/capabilities` with `Authorization: Bearer <key>`.
2. Intersect `result.modules` with modules actually installed in Odoo.
3. Send only one to ten relevant module identifiers with each operation.
4. Preserve required clarification, warnings, unknowns, and provenance.
5. Execute through Odoo under the real user's access rights and record rules.

Complete integrations exchange a one-time code at `/v1/activate`, store the
returned tenant runtime token, and use that same token for REST, remote MCP and
`/v1/lifecycle`. Lifecycle remains readable after lapse so a connector can show
honest status and dates while continuing its local execution path. The frozen
response schemas are `spec/v0/activate-response.schema.json` and
`spec/v0/lifecycle-response.schema.json`.

Do not send record values, record IDs, credentials, user identities, or raw
questions that contain customer data. OCL returns meaning and risk guidance;
it never grants Odoo authorization. `validate_write_intent.authorized` is
always `false` by design.

The frozen machine-readable examples are in
`conformance/v0/runtime-contract.json`. Unknown arguments are rejected. There
is no registry-list, pagination, wildcard, or delta operation.

## Free execution and paid context

An Odoo connector or MCP server remains independently useful without OCL.
When a customer adds a separately purchased or bundled OCL key, the connector
may enrich its schemas, questions, and write audit evidence. It must degrade
to its local behavior when OCL is unavailable and must never make OCL an
authorization dependency.
