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

When invitations open, request access through the
[verified runtime alpha form](https://github.com/Nantiai/ocl-standard/issues/new?template=runtime-alpha-access.yml).
Do not include customer data or confidential database information in the
public request. Access is subject to the
[External Alpha Acceptable Use](ALPHA_ACCEPTABLE_USE.md) boundary.

## REST

Set the issued token once:

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
