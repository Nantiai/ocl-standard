# OCL public conformance v0

This suite proves that an implementation can parse the public entry schema,
enforce evidence references and trust-state invariants, reproduce the
content-addressed exemplar set, and consume the frozen connector runtime
contract.

The exemplars are candidate format demonstrations. They are not the commercial
verified registry and carry no Odoo lifetime guarantee.

Run:

```bash
python conformance/v0/run.py
```

Expected result:

```text
PASS ocl-public-conformance-v0: 10 entries, 1 context pack, 1 runtime contract
```
