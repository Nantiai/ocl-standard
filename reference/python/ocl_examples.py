"""Example-only OCL resolver and MCP server for the public exemplar set."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples/v0"
WARNING_TYPES = {"negative_knowledge", "write_policy", "security_note", "gotcha"}
TOOLS = ("get_context", "resolve_noun", "explain_field")
TECHNICAL_IDENTIFIER = re.compile(r"\b[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\b")


def load_examples() -> list[dict[str, Any]]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(EXAMPLES.glob("entry.*.json"))]


def _terms(entry: dict[str, Any]) -> set[str]:
    claim = entry["claim"]
    values = [entry["id"], entry["type"], claim.get("summary", "")]
    values.extend(
        str(claim.get(key, ""))
        for key in ("business_noun", "model", "field", "concept", "from_model", "to_model", "operation")
    )
    values.extend(claim.get("aliases", []))
    return set(re.findall(r"[a-z][a-z0-9_.]+", " ".join(values).lower()))


def _identifiers(entry: dict[str, Any]) -> set[str]:
    claim = entry["claim"]
    identifiers = set()
    for key in ("model", "from_model", "to_model"):
        if claim.get(key):
            identifiers.add(claim[key])
    if claim.get("model") and claim.get("field"):
        identifiers.add(f"{claim['model']}.{claim['field']}")
        identifiers.add(claim["field"])
    if claim.get("preferred_method"):
        identifiers.add(claim["preferred_method"])
    return identifiers


def _score(entry: dict[str, Any], question: str) -> tuple[int, list[str], list[str]]:
    lowered = question.lower()
    exact = sorted(identifier for identifier in _identifiers(entry) if identifier.lower() in lowered)
    words = set(re.findall(r"[a-z][a-z0-9_.]+", lowered))
    matched = sorted(term for term in _terms(entry) & words if len(term) >= 4)
    score = len(exact) * 100 + len(matched) * 10
    if entry["type"] == "disambiguation" and entry["claim"].get("concept", "").lower() in lowered:
        score += 50
    return score, exact, matched


def _render(entry: dict[str, Any]) -> str:
    claim = entry["claim"]
    pieces = [claim["summary"]]
    if claim.get("domain"):
        pieces.append(f"Domain: {json.dumps(claim['domain'], ensure_ascii=True)}")
    if claim.get("meaning"):
        pieces.append(f"Meaning: {claim['meaning']}")
    if claim.get("correction"):
        pieces.append(f"Correction: {claim['correction']}")
    if claim.get("preferred_method"):
        pieces.append(f"Preferred method: {claim['preferred_method']}")
    if claim.get("questions"):
        pieces.append("Clarify: " + " ".join(claim["questions"]))
    if claim.get("limitations"):
        pieces.append("Limits: " + " ".join(claim["limitations"]))
    return " ".join(pieces)


def _intent(question: str) -> str:
    lowered = question.lower()
    if any(term in lowered for term in ("post", "create", "write", "cancel", "update")):
        return "write"
    if any(term in lowered for term in ("revenue", "total", "count", "how much")):
        return "metric"
    if any(term in lowered for term in ("join", "relationship", "connect")):
        return "join"
    if any(term in lowered for term in ("which", "list", "find", "show")):
        return "read"
    return "explain"


def get_context(
    question: str,
    *,
    odoo_version: str = "19.0",
    edition: str = "community",
    modules: list[str] | None = None,
    token_budget: int = 2000,
    generated_at: str | None = None,
) -> dict[str, Any]:
    modules = modules or ["account", "sale", "stock"]
    ranked = []
    for entry in load_examples():
        if odoo_version not in entry["applies_to"]["odoo_versions"]:
            continue
        if edition not in entry["applies_to"]["editions"]:
            continue
        if not set(entry["applies_to"]["requires_modules"]).issubset(set(modules)):
            continue
        score, exact, matched = _score(entry, question)
        if "revenue" in question.lower() and entry["id"].endswith("amount_total_warning"):
            score = max(score, 40)
            matched = sorted({*matched, "revenue_guard"})
        if score:
            ranked.append((score, entry["id"], entry, exact, matched))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    selected = ranked[:4]

    facts: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    unknowns: list[dict[str, Any]] = []
    retrieval: list[dict[str, Any]] = []
    for score, _entry_id, entry, exact, matched in selected:
        item = {
            "entry_id": entry["id"],
            "revision": entry["revision"],
            "rendered": _render(entry),
            "confidence": entry["confidence"]["score"],
            "status": entry["status"],
            "selection_reason": "public example exact/lexical match",
        }
        if entry["type"] in WARNING_TYPES:
            warnings.append({**item, "severity": "critical" if entry["claim"].get("risk") == "critical" else "warning"})
        else:
            facts.append(item)
        if entry["type"] == "disambiguation":
            unknowns.append(
                {
                    "code": f"clarify_{entry['claim']['concept'].replace(' ', '_')}",
                    "message": " ".join(entry["claim"]["questions"]),
                    "required_action": "clarify_before_execution",
                    "entry_id": entry["id"],
                    "revision": entry["revision"],
                }
            )
        retrieval.append(
            {
                "entry_id": entry["id"],
                "score": score,
                "exact_identifiers": exact,
                "matched_terms": matched,
                "source": "public_example_reference",
            }
        )
    if not selected:
        unknowns.append(
            {
                "code": "public_example_coverage",
                "message": "The ten public examples do not cover this request.",
                "required_action": "use_a_conforming_pack_with_relevant_entries",
            }
        )

    entry_ids = [item[2]["id"] for item in selected]
    index_digest = hashlib.sha256("\n".join(entry_ids).encode()).hexdigest()
    rendered = json.dumps({"facts": facts, "warnings": warnings, "unknowns": unknowns}, ensure_ascii=True)
    estimated_tokens = max(1, (len(rendered.encode()) + 3) // 4)
    pack_digest = hashlib.sha256(f"{question}\n{index_digest}".encode()).hexdigest()[:16]
    detected = sorted(set(TECHNICAL_IDENTIFIER.findall(question)))
    return {
        "document_kind": "ocl.context_pack",
        "schema_version": "0.1.0",
        "pack_id": f"ocl.public.example.context.{pack_digest}",
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "request": {
            "question": question,
            "intent": _intent(question),
            "token_budget": token_budget,
            "models": sorted(identifier for identifier in detected if identifier.count(".") == 1),
            "fields": sorted(identifier for identifier in detected if identifier.count(".") >= 2),
        },
        "scope": {"odoo_version": odoo_version, "edition": edition, "modules": sorted(modules)},
        "facts": facts,
        "warnings": warnings,
        "unknowns": unknowns,
        "provenance": {
            "registry_pack_id": "ocl.public.examples.v0",
            "registry_release": "0.1.0-alpha.1",
            "release_lock_ids": ["public-examples-not-a-release-lock"],
            "verification_report_ids": ["public-examples-candidate-only"],
            "runtime_index_id": "public-example-reference-index",
            "runtime_index_sha256": index_digest,
            "entry_ids": entry_ids,
            "token_estimator": "utf8_chars_div_4_example_only",
            "estimated_tokens": estimated_tokens,
            "truncation": {
                "token_budget": token_budget,
                "safe_minimum_tokens": estimated_tokens,
                "omitted_entry_ids": [],
                "truncated": False,
            },
        },
        "diagnostics": {
            "detected_identifiers": detected,
            "matched_terms": sorted({term for item in retrieval for term in item["matched_terms"]}),
            "retrieval": retrieval,
        },
    }


def resolve_noun(noun: str, **_scope: Any) -> list[dict[str, Any]]:
    needle = noun.casefold()
    results = []
    for entry in load_examples():
        if entry["type"] != "noun_mapping":
            continue
        claim = entry["claim"]
        names = [claim["business_noun"], *claim.get("aliases", [])]
        if needle not in {name.casefold() for name in names}:
            continue
        results.append(
            {
                "entry_id": entry["id"],
                "revision": entry["revision"],
                "status": entry["status"],
                "business_noun": claim["business_noun"],
                "model": claim["model"],
                "domain": claim["domain"],
                "public_example_only": True,
            }
        )
    return results


def explain_field(model: str, field: str, **_scope: Any) -> list[dict[str, Any]]:
    return [
        {
            "entry_id": entry["id"],
            "revision": entry["revision"],
            "status": entry["status"],
            "model": model,
            "field": field,
            "meaning": entry["claim"]["meaning"],
            "limitations": entry["claim"].get("limitations", []),
            "public_example_only": True,
        }
        for entry in load_examples()
        if entry["type"] == "field_semantic"
        and entry["claim"].get("model") == model
        and entry["claim"].get("field") == field
    ]


def call_tool(name: str, arguments: dict[str, Any]) -> Any:
    if name == "get_context":
        return get_context(**arguments)
    if name == "resolve_noun":
        return resolve_noun(**arguments)
    if name == "explain_field":
        return explain_field(**arguments)
    raise ValueError(f"unknown public example tool: {name}")


def serve_mcp(input_stream: TextIO = sys.stdin, output_stream: TextIO = sys.stdout) -> None:
    descriptions = {
        "get_context": "Assemble context from ten candidate public examples only.",
        "resolve_noun": "Resolve an exact business noun from public examples.",
        "explain_field": "Explain an exact model field from public examples.",
    }
    for line in input_stream:
        request = json.loads(line)
        method = request.get("method")
        if method == "initialize":
            result: Any = {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "ocl-public-examples", "version": "0.1.0-alpha.1"},
            }
        elif method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": name,
                        "description": descriptions[name],
                        "inputSchema": {"type": "object", "additionalProperties": True},
                    }
                    for name in TOOLS
                ]
            }
        elif method == "tools/call":
            params = request.get("params", {})
            try:
                value = call_tool(params["name"], params.get("arguments", {}))
                result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=True)}]}
            except (KeyError, TypeError, ValueError) as error:
                result = {"isError": True, "content": [{"type": "text", "text": str(error)}]}
        else:
            result = {}
        if "id" in request:
            output_stream.write(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}) + "\n")
            output_stream.flush()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    context = subparsers.add_parser("get-context")
    context.add_argument("question")
    context.add_argument("--edition", choices=("community", "enterprise"), default="community")
    context.add_argument("--token-budget", type=int, default=2000)
    noun = subparsers.add_parser("resolve-noun")
    noun.add_argument("noun")
    field = subparsers.add_parser("explain-field")
    field.add_argument("model")
    field.add_argument("field")
    subparsers.add_parser("serve-mcp")
    args = parser.parse_args()

    if args.command == "get-context":
        result = get_context(args.question, edition=args.edition, token_budget=args.token_budget)
    elif args.command == "resolve-noun":
        result = resolve_noun(args.noun)
    elif args.command == "explain-field":
        result = explain_field(args.model, args.field)
    else:
        serve_mcp()
        return 0
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
