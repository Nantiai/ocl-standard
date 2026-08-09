# External developer alpha

The external developer alpha is open to developers building Odoo connectors,
agents, MCP servers, context tooling, and independent OCL readers or writers.

## Available now

- cloneable schemas and conformance tests;
- Python validation and TypeScript document types;
- ten candidate examples and one valid context pack;
- an example-only resolver and local MCP server;
- invitation-gated access to the verified hosted runtime;
- public issues, discussions, and integration reports.

The fastest useful contribution is an independent reader that validates the
sample context pack without importing this repository's Python SDK. A stable
v1 requires independent implementations, not only nanti.ai-owned code.

## Not included

The alpha does not provide the commercial verified registry, production
retrieval, tenant overlays, memory, or an authorization layer for Odoo. The
public resolver cannot answer arbitrary Odoo questions and must not be used as
a production source of business truth.

Verified registry access is a separate controlled service at
`https://api.context.nanti.ai` or, later, a licensed cache. Hosted answers are
request-scoped so one request cannot export the entire corpus. The open
repository does not contain or grant access to that corpus.

## Participate

1. Run the [quickstart](QUICKSTART.md).
2. Follow [Using OCL](USING_OCL.md) to connect a reader, writer, connector, or agent.
3. Request [scoped runtime access](https://github.com/Nantiai/ocl-standard/issues/new?template=runtime-alpha-access.yml) if the public examples are insufficient.
4. Submit an [integration report](https://github.com/Nantiai/ocl-standard/issues/new?template=integration-report.yml).
5. Use [Discussions](https://github.com/Nantiai/ocl-standard/discussions) for format questions and proposed changes.

Conformance proves document interoperability. It does not certify that an
ontology statement is true.

The GitHub request path requires sign-in. Developers without a GitHub account
can instead email [hello@nanti.ai](mailto:hello@nanti.ai?subject=OCL%20developer%20alpha%20access)
with their integration, Odoo 19 edition, modules, and intended test questions.
