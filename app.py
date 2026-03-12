import uvicorn
import os
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from starlette.requests import Request
from server import mcp

async def health(request: Request):
    return JSONResponse({"status": "ok"})

# Get the MCP ASGI app — bypasses any host checking
mcp_app = mcp.streamable_http_app()

app = Starlette(routes=[
    Route("/health", health),
    Mount("/mcp", app=mcp_app),
])

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
