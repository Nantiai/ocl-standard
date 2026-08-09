# Verified runtime alpha

The verified runtime alpha is an invitation-only way to call request-scoped
Odoo 19 context without receiving the commercial registry.

## Availability

The controlled runtime is live at `https://api.context.nanti.ai`. It is not an
anonymous public API. Invited developers receive:

- an HTTPS base URL;
- a scoped, expiring Bearer token;
- enabled operations and Odoo module scope;
- request, context-budget, and distinct-entry allowances;
- no production SLA during alpha.

Request access through the
[verified runtime alpha form](https://github.com/Nantiai/ocl-standard/issues/new?template=runtime-alpha-access.yml).
Do not include customer data or confidential database information in the
public request. Access is subject to the
[External Alpha Acceptable Use](ALPHA_ACCEPTABLE_USE.md) boundary.

The GitHub form requires a GitHub account. If that is inconvenient, email
[hello@nanti.ai](mailto:hello@nanti.ai?subject=OCL%20developer%20alpha%20access)
with the intended integration, Odoo 19 edition, relevant modules, and one or
two questions you want to test.

## Fastest path

1. Submit the GitHub form or short email.
2. Receive a scoped token, expiry, and limits privately.
3. Set `OCL_TOKEN` and add the remote MCP URL to the existing AI tool.
4. Ask the AI an Odoo question; it calls OCL before using its Odoo connector.

No OCL package or local server is required for remote MCP.

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
