# Using OCL

OCL is consumed before or alongside an Odoo connector. It does not replace the
connector and it never grants Odoo authorization.

```text
1. User asks an Odoo question
2. Agent calls OCL get_context
3. OCL returns relevant meaning, warnings, unknowns, and provenance
4. Agent clarifies when required
5. Agent uses its existing Odoo connector under the user's real permissions
```

## Choose an integration

| You are building | Start with | What OCL contributes |
| --- | --- | --- |
| AI agent or assistant | MCP | Request-scoped meaning inside the tool loop |
| Odoo connector | Context-pack schema | A standard semantic response beside transport tools |
| Python application | Validator SDK | Valid entries and context packs with trust-state checks |
| TypeScript product | Public types and operation shapes | Stable integration boundary while the endpoint matures |
| Ontology tooling | Entry schema and conformance | Interoperable facts without adopting private registry internals |

## MCP

Clone the repository, then point an MCP client at the example server:

```json
{
  "mcpServers": {
    "ocl-public-examples": {
      "command": "python",
      "args": [
        "/absolute/path/to/ocl-standard/reference/python/ocl_examples.py",
        "serve-mcp"
      ]
    }
  }
}
```

The public MCP exposes:

- `get_context(question, odoo_version, edition, modules, token_budget)`;
- `resolve_noun(noun)`;
- `explain_field(model, field)`.

Recommended agent instruction:

```text
Before interpreting, querying, or changing Odoo, call OCL get_context with the
user's question and known Odoo scope. Treat required clarification and critical
warnings as hard constraints. OCL supplies meaning, not Odoo authorization.
```

The production contract also defines `get_join_path` and
`validate_write_intent`. They are not exposed by the public example server
because the ten examples cannot support those operations safely.

## CLI

Inspect the same public behavior without an MCP client:

```bash
python reference/python/ocl_examples.py get-context "What is revenue?"
python reference/python/ocl_examples.py get-context \
  "Explain account.move.amount_total" --edition enterprise
python reference/python/ocl_examples.py resolve-noun "vendor bill"
python reference/python/ocl_examples.py explain-field account.move invoice_user_id
```

The output is a schema-valid context pack or a scoped lookup result. Facts and
warnings retain entry identity, revision, confidence, and alpha provenance.

## Python

Install the validator from the clone:

```bash
python -m pip install -e sdk/python
```

Validate an entry before accepting or publishing it:

```python
import json
from pathlib import Path

from ocl_spec import validate_entry

schema = json.loads(Path("spec/v0/entry.schema.json").read_text())
entry = json.loads(Path("examples/v0/entry.customer_invoice.json").read_text())
errors = validate_entry(entry, schema)
if errors:
    raise ValueError(errors)
```

Use `validate_document` with `context-pack.schema.json` for assembled packs.
Schema validation proves interoperability, not the truth of a business claim.

## TypeScript

The source under `sdk/typescript` describes the five production operations and
their scope. It is intentionally not published to npm until a stable endpoint
and package release process exist.

```ts
import { OCLClient } from "./sdk/typescript/src/index.js";

const ocl = new OCLClient("https://api.context.nanti.ai", process.env.OCL_TOKEN);
const pack = await ocl.getContext("Which invoices are unpaid?", {
  odoo_version: "19.0",
  edition: "community",
  modules: ["account"],
});
```

The hosted URL is live but requires a scoped, expiring invitation token. It is
not an anonymous registry or bulk-export endpoint.

See [Verified runtime alpha](HOSTED_ALPHA.md) for the Bearer REST, Python, and
remote MCP call shapes used after an invitation is issued.

## Handle the response safely

An OCL context pack separates:

- `facts`: relevant meaning and filters;
- `warnings`: tempting interpretations and unsafe operations;
- `unknowns`: information that must be clarified or supplied;
- `provenance`: entry, release, verification, and truncation identity;
- `diagnostics`: inspectable retrieval reasons.

Do not discard warnings to save prompt space. Do not convert an `unknown` into
a guessed default. Pass the pack to the AI together with connector tool
descriptions, then let Odoo enforce ACLs, record rules, and business methods.

## What is usable today

The public repository is usable today for format adoption, conformance,
integration development, and a ten-example MCP demonstration. Invited
developers can also call the private 44-entry verified runtime through
request-scoped REST or remote MCP. The public examples must not be presented as
production ontology coverage.
