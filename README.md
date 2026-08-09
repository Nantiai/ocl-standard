# OCL standard

OCL is an experimental open format for giving AI systems structured, scoped,
and verifiable business meaning for Odoo.

An Odoo connector explains how to reach records. An OCL context pack explains
what relevant records and fields mean, which tempting interpretations are
wrong, what ambiguity must be resolved, and which safety boundaries still
apply.

```text
question -> OCL context -> AI reasoning + existing connector -> Odoo
```

## Use OCL

Choose the surface that fits your product:

| Route | Call | Benefit | Alpha availability |
| --- | --- | --- | --- |
| MCP for AI agents | `get_context`, `resolve_noun`, `explain_field` | Put scoped Odoo meaning directly in an agent's tool loop | Public example or invitation runtime |
| CLI | `get-context "What is revenue?"` | Inspect a context pack and its warnings immediately | Public examples now |
| Python validator | `validate_entry(entry, schema)` | Read and produce interoperable OCL documents | Available now |
| TypeScript integration | Five production operation shapes | Connect a product to the verified hosted runtime | Source alpha and invitation runtime |

Clone and try the context behavior:

```bash
git clone https://github.com/Nantiai/ocl-standard.git
cd ocl-standard
python reference/python/ocl_examples.py get-context "What is revenue?"
```

The result asks which revenue definition applies and returns the paired warning
against treating `account.move.amount_total` as universal revenue.

### Add the example MCP to an agent

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

This local server demonstrates the real OCL tool contract using ten public
candidate examples. It is not the commercial 44-entry verified runtime.

See **[Using OCL](docs/USING_OCL.md)** for the integration flow, MCP calls,
CLI commands, SDK examples, response handling, and current access boundary.
Invited runtime clients can follow the **[verified alpha call guide](docs/HOSTED_ALPHA.md)**.
Developers can **[request scoped runtime alpha access](https://github.com/Nantiai/ocl-standard/issues/new?template=runtime-alpha-access.yml)** without posting customer data.
Developers without GitHub can request the same access by emailing
[hello@nanti.ai](mailto:hello@nanti.ai?subject=OCL%20developer%20alpha%20access).

This repository contains the open interoperability layer:

- JSON Schemas for semantic entries and request-scoped context packs;
- a dependency-light Python validator and TypeScript client shape;
- ten Odoo 19 candidate examples covering the major knowledge types;
- an executable conformance suite;
- an example-only resolver and MCP server;
- public benchmark methodology.

It does **not** contain nanti.ai's commercial registry, production assembler,
verification harness, source fingerprints, private benchmarks, tenant
overlays, memory, or unreleased ontology candidates.

## Status

Version `0.1.0` is an experimental technical alpha. The format can change while
independent implementations test it. The examples demonstrate the format; they
are not the commercial verified registry and do not carry a lifetime guarantee.

Odoo 19 is the only current stock-version focus.

## External developer alpha

Developers can now clone the standard, run conformance, integrate the example
MCP server, and report an independent implementation. See the
[developer alpha guide](docs/DEVELOPER_ALPHA.md).

The public alpha is an interoperability surface, not free bulk access to the
commercial verified registry. An invitation-only verified runtime is live at
`https://api.context.nanti.ai`; every caller receives a scoped, expiring key.

## Core idea

```text
meaning -> evidence -> rule -> assertion -> applicability -> confidence
```

Facts do not become verified because an LLM wrote plausible JSON. A conforming
document describes evidence and assertions. A registry operator separately
decides which verification policy is sufficient for a release claim.

## Learn more

- [Introduction](https://nanti.ai/docs/context-layer/introduction)
- [Technical alpha](https://nanti.ai/context-layer)
- [Format v0](spec/v0/README.md)
- [Quickstart](docs/QUICKSTART.md)
- [Using OCL](docs/USING_OCL.md)
- [External developer alpha](docs/DEVELOPER_ALPHA.md)
- [Governance](GOVERNANCE.md)
- [Contributing](CONTRIBUTING.md)

## Independence

Odoo is a trademark of Odoo S.A. This project is independently developed and
is not affiliated with or endorsed by Odoo S.A.

## License

The open repository is licensed under the [Apache License 2.0](LICENSE). The
commercial OCL registry and services are separate and are not distributed by
this repository.
