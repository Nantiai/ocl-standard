# Python validator

Install from a clone:

```bash
python -m pip install -e sdk/python
```

Validate any schema-backed OCL document:

```python
import json
from pathlib import Path

from ocl_spec import validate_document, validate_entry

schema = json.loads(Path("spec/v0/entry.schema.json").read_text())
entry = json.loads(Path("examples/v0/entry.customer_invoice.json").read_text())

errors = validate_entry(entry, schema)
if errors:
    raise ValueError(errors)
```

`validate_entry` adds public trust-state and evidence-reference checks on top of
JSON Schema. It does not execute Odoo assertions or certify business truth.
