# Quickstart

This quickstart runs entirely on the ten public candidate examples. It does not
download or reconstruct the commercial registry.

## Validate the format

```bash
git clone https://github.com/Nantiai/ocl-standard.git
cd ocl-standard
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e sdk/python
python conformance/v0/run.py
```

Expected result:

```text
PASS ocl-public-conformance-v0: 10 entries, 1 context pack
```

## Ask the example resolver

```bash
python reference/python/ocl_examples.py get-context "What is revenue?"
python reference/python/ocl_examples.py resolve-noun "customer invoice"
python reference/python/ocl_examples.py explain-field account.move invoice_user_id
```

The first command should preserve ambiguity. It demonstrates the context-pack
contract and public example types, not nanti.ai's production retrieval quality.

## Run the example MCP server

The reference server speaks JSON-RPC over stdio and exposes:

- `get_context`;
- `resolve_noun`;
- `explain_field`.

Run it directly:

```bash
python reference/python/ocl_examples.py serve-mcp
```

Example MCP client configuration:

```json
{
  "mcpServers": {
    "ocl-public-examples": {
      "command": "python",
      "args": [
        "/absolute/path/to/ocl-standard/reference/python/ocl_examples.py",
        "serve-mcp"
      ]
    }
  }
}
```

Use an absolute path appropriate to your machine.

## Build your own entry

Copy an example matching the required knowledge type, assign an ID in a
namespace you control, attach evidence you have the right to reference, and
keep the guarantee at `candidate` until your declared verification policy has
actually passed.

The local validator proves format and trust-state invariants. It does not prove
the underlying Odoo business fact.

## Production access

The commercial verified registry and production assembler are not included in
this repository. Developer access will be announced through
[nanti.ai/context-layer](https://nanti.ai/context-layer).
