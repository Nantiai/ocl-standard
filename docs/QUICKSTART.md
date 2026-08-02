# Quickstart

This quickstart runs entirely on the ten public candidate examples. It does not
download or reconstruct the commercial registry.

## 1. Ask OCL for context

```bash
git clone https://github.com/Nantiai/ocl-standard.git
cd ocl-standard
python reference/python/ocl_examples.py get-context "What is revenue?"
```

The public example runtime returns an `ocl.context_pack` with provenance,
relevant facts, warnings, and required clarification. It should not silently
choose a revenue formula.

Try the other public operations:

```bash
python reference/python/ocl_examples.py resolve-noun "customer invoice"
python reference/python/ocl_examples.py explain-field account.move invoice_user_id
```

## 2. Add the example MCP to an AI client

Use this generic stdio MCP configuration, replacing the path with the absolute
path to your clone:

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

The agent will discover `get_context`, `resolve_noun`, and `explain_field`.
Tell the agent to call `get_context` before interpreting or planning Odoo work,
then preserve every clarification and warning in the returned pack.

## 3. Validate the format

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e sdk/python
python conformance/v0/run.py
```

Expected result:

```text
PASS ocl-public-conformance-v0: 10 entries, 1 context pack
```

## 4. Build your own entry

Copy an example matching the required knowledge type, assign an ID in a
namespace you control, attach evidence you have the right to reference, and
keep the guarantee at `candidate` until your declared verification policy has
actually passed.

The local validator proves format and trust-state invariants. It does not prove
the underlying Odoo business fact.

Read [Using OCL](USING_OCL.md) for the complete runtime pattern and code
examples.

## Production access

The commercial verified registry and production assembler are not included in
this repository. Developer access will be announced through
[nanti.ai/context-layer](https://nanti.ai/context-layer).
