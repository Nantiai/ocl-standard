# OCL format v0

Status: experimental  
Version: `0.1.0`

This directory is the planned public interoperability boundary. The schemas are
draft contracts and can change until independent implementations exercise them.

## Documents

- `entry.schema.json`: one semantic fact, its scope, evidence, assertions,
  confidence, and provenance.
- `pack.schema.json`: a deterministic collection of entry files and source
  snapshots.
- `context-pack.schema.json`: request-scoped output for AI consumers.
- `benchmark-case.schema.json`: one independently scored evaluation case.
- `benchmark-suite.schema.json`: a content-hashed sealed set of benchmark cases.
- `benchmark-artifact.schema.json`: prepared prompts, raw model runs, and scored
  three-arm evaluation artifacts.
- `registry-catalog.schema.json`: composition of independently released packs.

Catalog pack items may optionally pin their own `release`. Readers that do not
see this field use the catalog-level release, preserving v0 compatibility while
allowing additive packs to advance independently.

Private registry implementations can define additional verification, release,
and runtime-index artifacts. Those operational formats are not required to read
or write a public OCL entry or context pack.

## Trust levels

An entry can move through these states:

```text
draft -> evidence_attached -> asserted -> verified
                                  |           |
                                  v           v
                               degraded -> deprecated -> retired
```

`asserted` means declared assertions pass at their stated level. `verified`
requires the entry's full release policy, including live/behavioral assertions
and human review where applicable. Confidence is a separate estimate and never
upgrades status.

## Portable domains

Domains use JSON arrays. A condition is `[field, operator, value]`; Odoo prefix
logical operators are represented as `"&"`, `"|"`, and `"!"`. Runtime values
use a structured placeholder such as `{"$var": "today"}` rather than an
unquoted expression.

Example:

```json
[
  ["move_type", "=", "out_invoice"],
  ["state", "=", "posted"]
]
```

Syntax validation does not prove that a domain compiles on a model. That needs
a live `domain_executes` assertion.

## Additive claim fields

Migration note, 2026-08-11: schema `0.1.0` now recognizes optional structured
detail for discriminators, join paths/cardinality, write approvals and failure
boundaries, and security access/safe-behavior notes. Existing `0.1.0` entries
remain valid and readers may ignore these optional fields. The required core
shape and write-policy risk enum are unchanged.
