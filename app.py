"""Entry point for container deployment - delegates to server.py"""
from server import mcp
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Get the ASGI app from FastMCP
app = mcp.streamable_http_app()

# Allow all hosts (Container App uses dynamic hostnames)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)
