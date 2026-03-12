"""Main implementation of the SharePoint MCP Server."""
import sys
import os
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from auth.sharepoint_auth import SharePointContext, get_auth_context
from config.settings import APP_NAME, DEBUG
from tools.site_tools import register_site_tools

logging_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    level=logging_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("sharepoint_mcp")

@asynccontextmanager
async def sharepoint_lifespan(server: FastMCP) -> AsyncIterator[SharePointContext]:
    """Manage SharePoint connection lifecycle."""
    logger.info("Initializing SharePoint connection...")
    try:
        logger.debug("Attempting to get authentication context...")
        context = await get_auth_context()
        logger.info(f"Authentication successful. Token expiry: {context.token_expiry}")
        yield context
    except Exception as e:
        logger.error(f"Error during SharePoint authentication: {e}")
        error_context = SharePointContext(
            access_token="error",
            token_expiry=datetime.now() + timedelta(seconds=10),
            graph_url="https://graph.microsoft.com/v1.0",
        )
        logger.warning("Using error context due to authentication failure")
        yield error_context
    finally:
        logger.info("Ending SharePoint connection...")


mcp = FastMCP(
    APP_NAME,
    lifespan=sharepoint_lifespan,
    json_response=True,              # ← forces JSON, no SSE requirement
    stateless_http=True,             # ← no session state needed
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    )
)

register_site_tools(mcp)

def main():
    """Main entry point for the SharePoint MCP server."""
    import uvicorn
    logger.info(f"Starting {APP_NAME} server...")
    uvicorn.run(
        mcp.streamable_http_app(),
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        proxy_headers=True,
        forwarded_allow_ips="*",
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error in SharePoint MCP server: {e}")
        sys.exit(1)

