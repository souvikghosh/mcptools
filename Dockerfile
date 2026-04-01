FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY . .

# Expose MCP server on stdio (default MCP transport)
# Run: docker run -e ANTHROPIC_API_KEY=... mcptools
CMD ["python", "-m", "mcptools"]
