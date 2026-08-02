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

## Authorized runtime client

When issued an External Developer Alpha endpoint and token:

```python
import os

from ocl_spec import OCLClient

ocl = OCLClient(os.environ["OCL_URL"], os.environ["OCL_TOKEN"])
pack = ocl.get_context(
    "Which invoices are unpaid?",
    odoo_version="19.0",
    edition="community",
    modules=["account"],
)
```

The client is dependency-free and supports all five production operations. It
does not include a registry or make the public examples production truth.
