# Repository boundary

The open standard and the commercial truth registry have different jobs.

## Included here

- document schemas;
- format documentation;
- dependency-light validators and client shapes;
- candidate examples;
- public conformance;
- example-only retrieval and MCP behavior;
- public benchmark methodology.

## Not included here

- the 44-entry released commercial registry;
- release locks, runtime indexes, source fingerprints, or verification matrices;
- candidate-generation or ranking logic;
- production context assembly;
- private benchmark cases, prompts, mappings, or raw evaluations;
- tenant extraction, overlays, drift, or memory;
- entitlement and licensed-cache operations.

This boundary is intentional. Anyone can implement and validate the standard
without buying a service. Production users can separately license verified
coverage and operational guarantees instead of rebuilding the truth factory.

The public examples are useful teaching artifacts but must not be described as
the released commercial corpus.
