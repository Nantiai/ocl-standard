# OCL standard

OCL is an experimental open format for giving AI systems structured, scoped,
and verifiable business meaning for Odoo.

An Odoo connector explains how to reach records. An OCL context pack explains
what relevant records and fields mean, which tempting interpretations are
wrong, what ambiguity must be resolved, and which safety boundaries still
apply.

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

## Try it

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e sdk/python
python conformance/v0/run.py
python reference/python/ocl_examples.py get-context "What is revenue?"
```

The final command uses only the ten public examples. It should ask for a
revenue definition instead of inventing one.

For a local example MCP server:

```bash
python reference/python/ocl_examples.py serve-mcp
```

See [the quickstart](docs/QUICKSTART.md) for client configuration and the exact
boundary between this reference implementation and the commercial runtime.

## External developer alpha

Developers can now clone the standard, run conformance, integrate the example
MCP server, and report an independent implementation. See the
[developer alpha guide](docs/DEVELOPER_ALPHA.md).

The public alpha is an interoperability surface, not free bulk access to the
commercial verified registry. A production registry endpoint is not live yet.

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
