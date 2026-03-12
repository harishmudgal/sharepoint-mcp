# syntax=docker/dockerfile:1
FROM python:3.12-slim

# System deps (optional: curl for healthchecks/logs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

# Create app dir
WORKDIR /app

# Copy project files
COPY . /app

# Install deps
# If requirements.txt exists, use it; otherwise fallback to setup.py / editable install
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install --no-cache-dir -e .

# Non-root user (best practice)
RUN useradd -m mcpuser
USER mcpuser

# Expose MCP HTTP port
EXPOSE 8000

# Environment: ensure production defaults
ENV PORT=8000

# Start the MCP server (HTTP transport configured in server.py)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
