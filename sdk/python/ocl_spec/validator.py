from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


@dataclass(frozen=True)
class ValidationError:
    path: str
    message: str


def validate_document(document: dict[str, Any], schema: dict[str, Any]) -> list[ValidationError]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        ValidationError(".".join(map(str, error.absolute_path)) or "$", error.message)
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def validate_entry(document: dict[str, Any], schema: dict[str, Any]) -> list[ValidationError]:
    errors = validate_document(document, schema)
    evidence_ids = {
        item.get("id") for item in document.get("evidence", []) if isinstance(item, dict)
    }
    for index, assertion in enumerate(document.get("assertions", [])):
        for evidence_id in assertion.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                errors.append(
                    ValidationError(
                        f"assertions.{index}.evidence_ids",
                        f"unknown evidence reference: {evidence_id}",
                    )
                )
    validity = document.get("validity", {})
    if document.get("status") == "verified" and validity.get("guarantee") == "candidate":
        errors.append(ValidationError("validity.guarantee", "verified content cannot be candidate"))
    if validity.get("guarantee") in {"release_line_invariant", "lifetime_sealed"}:
        if document.get("status") != "verified":
            errors.append(ValidationError("status", "released guarantees require verified status"))
        if not document.get("provenance", {}).get("reviewed_by"):
            errors.append(ValidationError("provenance.reviewed_by", "released guarantees require review"))
    return errors
