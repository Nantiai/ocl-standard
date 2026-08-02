from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ocl_examples


ROOT = Path(__file__).resolve().parents[2]


class PublicExampleReferenceTests(unittest.TestCase):
    def test_revenue_preserves_ambiguity_and_validates(self) -> None:
        pack = ocl_examples.get_context("What is revenue?", generated_at="2026-08-02T00:00:00Z")
        schema = json.loads((ROOT / "spec/v0/context-pack.schema.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(pack))
        self.assertEqual([], errors)
        self.assertTrue(any(item["code"] == "clarify_revenue" for item in pack["unknowns"]))
        self.assertTrue(any("amount_total" in item["entry_id"] for item in pack["warnings"]))
        self.assertTrue(all(item["status"] != "verified" for item in pack["facts"] + pack["warnings"]))

    def test_exact_noun_and_field_tools_use_examples_only(self) -> None:
        noun = ocl_examples.resolve_noun("customer invoice")
        field = ocl_examples.explain_field("account.move", "invoice_user_id")
        self.assertEqual("out_invoice", noun[0]["domain"][0][2])
        self.assertEqual("invoice_user_id", field[0]["field"])
        self.assertTrue(noun[0]["public_example_only"])
        self.assertTrue(field[0]["public_example_only"])

    def test_mcp_lists_only_three_public_example_tools(self) -> None:
        requests = "\n".join(
            [
                json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
                json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}),
            ]
        )
        output = io.StringIO()
        ocl_examples.serve_mcp(io.StringIO(requests + "\n"), output)
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(list(ocl_examples.TOOLS), [item["name"] for item in responses[1]["result"]["tools"]])


if __name__ == "__main__":
    unittest.main()
