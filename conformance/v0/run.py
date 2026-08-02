from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "sdk/python"))

from ocl_spec import validate_document, validate_entry  # noqa: E402


def main() -> int:
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    schema = json.loads((HERE / manifest["schema"]).resolve().read_text(encoding="utf-8"))
    failures: list[str] = []
    ids: set[str] = set()
    for item in manifest["examples"]:
        path = (HERE / item["path"]).resolve()
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != item["sha256"]:
            failures.append(f"{path.name}: content hash mismatch")
            continue
        document = json.loads(payload)
        if document["id"] in ids:
            failures.append(f"{path.name}: duplicate entry ID {document['id']}")
        ids.add(document["id"])
        failures.extend(f"{path.name}:{error.path}: {error.message}" for error in validate_entry(document, schema))
    context_count = 0
    for item in manifest.get("context_packs", []):
        path = (HERE / item["path"]).resolve()
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != item["sha256"]:
            failures.append(f"{path.name}: content hash mismatch")
            continue
        context_schema = json.loads((HERE / item["schema"]).resolve().read_text(encoding="utf-8"))
        document = json.loads(payload)
        failures.extend(
            f"{path.name}:{error.path}: {error.message}"
            for error in validate_document(document, context_schema)
        )
        context_count += 1
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"PASS {manifest['suite']}: {len(ids)} entries, {context_count} context pack")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
