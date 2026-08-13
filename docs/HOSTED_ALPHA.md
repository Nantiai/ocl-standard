# Verified runtime alpha

The verified runtime alpha is a bounded way to call request-scoped Odoo 19
context without receiving the commercial registry.

## Availability

The controlled runtime is live at `https://api.context.nanti.ai`. The fixed
demo is anonymous; normal context calls use a scoped credential. Developers
can create a seven-day trial immediately and receive:

- an HTTPS base URL;
- a scoped, expiring Bearer token;
- enabled operations and Odoo module scope;
- request, context-budget, and distinct-entry allowances;
- no production SLA during alpha.

Try the fixed, no-login
[revenue decision demo](https://api.context.nanti.ai/demo/revenue), then use
the native [email-only access form](https://api.context.nanti.ai/request-access).
Do not include customer data or confidential database information. Access is
subject to the [External Alpha Acceptable Use](ALPHA_ACCEPTABLE_USE.md)
boundary.

The native form shows its token once in the response and does not require
GitHub, email verification, or founder approval. The
[GitHub form](https://github.com/Nantiai/ocl-standard/issues/new?template=runtime-alpha-access.yml)
and [email](mailto:hello@nanti.ai?subject=OCL%20developer%20alpha%20access)
remain fallback paths.

## Fastest path

1. Try the fixed verified demo, then submit the native short form.
2. Store the scoped seven-day token shown once on the next screen.
3. Set `OCL_TOKEN` and add the remote MCP URL to the existing AI tool.
4. Ask the AI an Odoo question; it calls OCL before using its Odoo connector.

No OCL package or local server is required for remote MCP.

Automatic trials have no request-count meter during the seven-day evaluation.
They include both Odoo 19 editions and all released runtime modules. A
30-request/minute burst guard, 16-distinct-entry daily guard and 6,000-token
context ceiling remain security boundaries. The service rejects bulk
registry extraction, wildcard scope, and requests outside the entitlement.
Submitted access details are removed after 90 days, and keyed abuse-control
fingerprints after 24 hours. The raw trial token is never stored; its hash and
exact quota rows are removed 30 days after the seven-day trial expires.

### Codex CLI

```bash
export OCL_TOKEN="<issued-token>"
codex mcp add ocl \
  --url https://api.context.nanti.ai/mcp \
  --bearer-token-env-var OCL_TOKEN
codex mcp get ocl
```

Launch Codex from the same environment so it can read `OCL_TOKEN`.

### Claude Code

```bash
export OCL_TOKEN="<issued-token>"
claude mcp add --scope user --transport http ocl \
  https://api.context.nanti.ai/mcp \
  --header "Authorization: Bearer $OCL_TOKEN"
```

Claude Code stores the configured header in its user configuration. Treat that
file as a secret and never commit or share it.

## REST

For direct HTTP or SDK calls, set both values once:

```bash
export OCL_URL="https://api.context.nanti.ai"
export OCL_TOKEN="<issued-token>"
```

```bash
curl "$OCL_URL/v1/get-context" \
  -H "Authorization: Bearer $OCL_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "question": "Which invoices are unpaid?",
    "odoo_version": "19.0",
    "edition": "community",
    "modules": ["account"]
  }'
```

The five operations are `get_context`, `resolve_noun`, `explain_field`,
`get_join_path`, and `validate_write_intent`.

## Python

```python
import os
from ocl_spec import OCLClient

ocl = OCLClient(os.environ["OCL_URL"], os.environ["OCL_TOKEN"])
pack = ocl.get_context(
    "Which invoices are unpaid?",
    odoo_version="19.0",
    edition="community",
    modules=["account"],
)
```

## Remote MCP

```json
{
  "mcpServers": {
    "ocl": {
      "url": "https://api.context.nanti.ai/mcp",
      "headers": {
        "Authorization": "Bearer ${OCL_TOKEN}"
      }
    }
  }
}
```

Client configuration syntax differs across MCP hosts. Use the host's supported
method for secret environment variables rather than placing a token in source
control.

## Boundaries

The alpha returns the smallest safe context that fits the request and
entitlement. It has no registry-list or bulk-export operation. Bulk enumeration
and wildcard requests are rejected, and usage is limited per key.

Readable context returned to an authorized developer can still be copied. The
service controls practical extraction through scope, rate, distinct-entry,
token-budget, contractual, provenance, and audit measures rather than claiming
impossible client-side secrecy.
