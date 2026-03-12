import os
from server import mcp
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = mcp.streamable_http_app()

# Disable host header checking entirely
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
    www_redirect=False
)
