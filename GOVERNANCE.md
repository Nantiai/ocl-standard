# Governance

## Scope

This repository governs the open OCL document formats, public conformance
rules, SDK interoperability, and public examples. It does not govern the
commercial registry or its release decisions.

## Status

The `v0` format is experimental. Breaking changes are allowed only with an
explicit migration note and version change. A stable `v1` will require at least
two independent readers and one independent writer passing conformance.

## Decisions

- Technical discussion happens in public issues and pull requests.
- Maintainers publish the rationale for accepted and rejected format changes.
- Widely useful fields belong in the public specification rather than an
  undocumented proprietary extension.
- Registry-specific metadata can use namespaced extensions while it matures.
- The current specification maintainers retain the final decision when an RFC
  cannot reach consensus.

## Compatibility

Conformance means a tool can read or write the declared schema version and pass
the applicable public suite. It does not certify the truth or commercial
quality of an ontology entry.

Deprecations will be documented before removal. Stable versions will receive a
migration guide rather than silent breaking changes.
