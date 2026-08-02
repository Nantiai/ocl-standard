# OCL public conformance v0

This suite proves that an implementation can parse the public entry schema,
enforce evidence references and trust-state invariants, and reproduce the
content-addressed exemplar set.

The exemplars are candidate format demonstrations. They are not the commercial
verified registry and carry no Odoo lifetime guarantee.

Run:

```bash
python conformance/v0/run.py
```

Expected result:

```text
PASS ocl-public-conformance-v0: 10 entries, 1 context pack
```
