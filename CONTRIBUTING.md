# Contributing

OCL v0 is experimental. Contributions should improve interoperability without
turning the public standard repository into an unverified business-fact dump.

Useful contributions include:

- schema issues and backwards-compatible improvements;
- independent parser or writer implementations;
- conformance cases that expose ambiguity;
- small, clearly licensed format examples;
- documentation corrections;
- connector and agent integration examples.

Do not submit:

- customer records, metadata, configuration, or credentials;
- Odoo Enterprise source or copied proprietary documentation;
- facts whose source and redistribution rights are unclear;
- claims that an entry is verified without reproducible verification evidence;
- exports from nanti.ai's commercial registry.

## Process

1. Open an issue describing the interoperability problem.
2. For format changes, include before/after JSON and migration impact.
3. Add or update conformance coverage.
4. Run `python conformance/v0/run.py`.
5. Submit a focused pull request.

All commits must include a Developer Certificate of Origin sign-off:

```text
Signed-off-by: Your Name <your.email@example.com>
```

By contributing, you agree that your contribution is licensed under Apache
License 2.0 and that you have the right to submit it.

Specification conformance and commercial registry inclusion are separate.
Public contributions do not automatically enter the commercial registry.
