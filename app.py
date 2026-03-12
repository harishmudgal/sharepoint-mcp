from server import mcp

# This exposes the ASGI app for uvicorn
app = mcp.streamable_http_app()
