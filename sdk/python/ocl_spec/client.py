from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class OCLClientError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None, code: str | None = None) -> None:
        self.status = status
        self.code = code
        super().__init__(message)


class OCLClient:
    """Dependency-free client for an authorized OCL REST implementation."""

    def __init__(self, base_url: str, token: str, *, timeout: float = 20) -> None:
        if not base_url.startswith(("http://", "https://")):
            raise ValueError("base_url must be an HTTP(S) URL")
        if not token:
            raise ValueError("token is required")
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _call(self, operation: str, arguments: dict[str, Any]) -> Any:
        body = json.dumps(arguments, separators=(",", ":"), ensure_ascii=True).encode()
        request = Request(
            f"{self.base_url}/v1/{operation.replace('_', '-')}",
            data=body,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = json.load(response)
        except HTTPError as error:
            try:
                payload = json.loads(error.read().decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                payload = {}
            detail = payload.get("error", {}) if isinstance(payload, dict) else {}
            if isinstance(detail, str):
                message, code = detail, None
            else:
                message = detail.get("message", f"OCL HTTP {error.code}")
                code = detail.get("code")
            raise OCLClientError(message, status=error.code, code=code) from error
        except URLError as error:
            raise OCLClientError(f"OCL connection failed: {error.reason}") from error
        if not isinstance(payload, dict) or "result" not in payload:
            raise OCLClientError("OCL response did not contain a result")
        return payload["result"]

    def get_context(self, question: str, **scope: Any) -> dict[str, Any]:
        return self._call("get_context", {"question": question, **scope})

    def resolve_noun(self, noun: str, **scope: Any) -> list[dict[str, Any]]:
        return self._call("resolve_noun", {"noun": noun, **scope})

    def explain_field(self, model: str, field: str, **scope: Any) -> list[dict[str, Any]]:
        return self._call("explain_field", {"model": model, "field": field, **scope})

    def get_join_path(self, from_model: str, to_model: str, **scope: Any) -> list[dict[str, Any]]:
        return self._call(
            "get_join_path",
            {"from_model": from_model, "to_model": to_model, **scope},
        )

    def validate_write_intent(
        self,
        model: str,
        operation: str,
        **options: Any,
    ) -> dict[str, Any]:
        return self._call(
            "validate_write_intent",
            {"model": model, "operation": operation, **options},
        )
