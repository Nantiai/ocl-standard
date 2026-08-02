# External developer alpha

The external developer alpha is open to developers building Odoo connectors,
agents, MCP servers, context tooling, and independent OCL readers or writers.

## Available now

- cloneable schemas and conformance tests;
- Python validation and TypeScript document types;
- ten candidate examples and one valid context pack;
- an example-only resolver and local MCP server;
- public issues, discussions, and integration reports.

The fastest useful contribution is an independent reader that validates the
sample context pack without importing this repository's Python SDK. A stable
v1 requires independent implementations, not only nanti.ai-owned code.

## Not included

The alpha does not provide the commercial verified registry, production
retrieval, tenant overlays, memory, or an authorization layer for Odoo. The
public resolver cannot answer arbitrary Odoo questions and must not be used as
a production source of business truth.

Production registry access will be a separate controlled service or licensed
cache. Its answers will be request-scoped so one request cannot export the
entire corpus. No hosted endpoint is claimed by this repository today.

## Participate

1. Run the [quickstart](QUICKSTART.md).
2. Follow [Using OCL](USING_OCL.md) to connect a reader, writer, connector, or agent.
3. Submit an [integration report](https://github.com/Nantiai/ocl-standard/issues/new?template=integration-report.yml).
4. Use [Discussions](https://github.com/Nantiai/ocl-standard/discussions) for format questions and proposed changes.

Conformance proves document interoperability. It does not certify that an
ontology statement is true.
