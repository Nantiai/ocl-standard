# Runs the OCL reference MCP server (stdio) over the published public example
# context packs. Stdlib-only; no pip installs.
FROM python:3.12-slim
LABEL io.modelcontextprotocol.server.name="io.github.Nantiai/ocl-standard"
LABEL org.opencontainers.image.source="https://github.com/Nantiai/ocl-standard"
LABEL org.opencontainers.image.description="OCL reference MCP server serving the public example context packs"
LABEL org.opencontainers.image.licenses="Apache-2.0"
WORKDIR /app
COPY reference/ reference/
COPY examples/ examples/
COPY LICENSE NOTICE ./
USER nobody
ENTRYPOINT ["python", "reference/python/ocl_examples.py", "serve-mcp"]
