import logging
import os
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
from auth.sharepoint_auth import SharePointContext, get_auth_context
from config.settings import APP_NAME, DEBUG

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger("sharepoint_mcp")

@asynccontextmanager
async def sharepoint_lifespan(server: FastMCP) -> AsyncIterator[SharePointContext]:
    logger.info("Initializing SharePoint connection...")
    try:
        context = await get_auth_context()
        logger.info(f"Auth successful. Expiry: {context.token_expiry}")
        yield context
    except Exception as e:
        logger.error(f"Auth error: {e}")
        yield SharePointContext(
            access_token="error",
            token_expiry=datetime.now() + timedelta(seconds=10),
            graph_url="https://graph.microsoft.com/v1.0",
        )
    finally:
        logger.info("Shutting down SharePoint connection...")

mcp = FastMCP(APP_NAME, lifespan=sharepoint_lifespan)

from tools.site_tools import register_site_tools
register_site_tools(mcp)


