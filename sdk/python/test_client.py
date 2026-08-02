from __future__ import annotations

import io
import json
import unittest
from unittest.mock import patch

from ocl_spec import OCLClient


class FakeResponse:
    def __init__(self, value: dict) -> None:
        self.value = value

    def __enter__(self):
        return io.BytesIO(json.dumps(self.value).encode())

    def __exit__(self, *_args):
        return False


class OCLClientTests(unittest.TestCase):
    def test_bearer_client_calls_request_scoped_context_route(self) -> None:
        client = OCLClient("https://context.example/", "alpha-secret")
        with patch("ocl_spec.client.urlopen", return_value=FakeResponse({"result": {"facts": []}})) as call:
            result = client.get_context(
                "What is revenue?",
                odoo_version="19.0",
                modules=["account"],
            )
        request = call.call_args.args[0]
        self.assertEqual("https://context.example/v1/get-context", request.full_url)
        self.assertEqual("Bearer alpha-secret", request.get_header("Authorization"))
        self.assertEqual("What is revenue?", json.loads(request.data)["question"])
        self.assertEqual({"facts": []}, result)


if __name__ == "__main__":
    unittest.main()
