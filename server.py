import os
import sys
import logging
from pathlib import Path
from fastmcp import FastMCP
from dotenv import load_dotenv

# --- FIX: Ensure Python finds the local package ---
# This adds the current folder to the search path to prevent ModuleNotFoundError
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sharepoint-mcp-copilot")

load_dotenv()

# --- INITIALIZE FASTMCP ---
# This enables Streamable HTTP required for Copilot Studio
mcp = FastMCP("SharePoint-MCP")

# --- INITIALIZE REPO LOGIC ---
# We use a try-except to catch import errors if the folder structure varies
try:
    # Based on the fork structure, the main logic is typically in these paths:
    # Option A: from sharepoint_mcp.server import SharePointServer
    # Option B: from server import SharePointServer (if it's a flat structure)
    from sharepoint_mcp.mcp_server import SharePointServer
    
    sp_logic = SharePointServer(
        client_id=os.getenv("AZURE_CLIENT_ID"),
        tenant_id=os.getenv("AZURE_TENANT_ID"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET")
    )
    logger.info("Successfully loaded SharePointServer logic from fork.")
except ImportError as e:
    logger.error(f"Import failed: {e}. Check if folder '__init__.py' is missing.")
    sp_logic = None

# --- REGISTER TOOLS FOR COPILOT ---
@mcp.tool()
async def search_sharepoint(query: str) -> str:
    """Search for documents and content across SharePoint sites."""
    if not sp_logic: return "Server logic not initialized."
    return await sp_logic.search(query)

@mcp.tool()
async def list_sites() -> str:
    """Retrieve all accessible SharePoint sites."""
    if not sp_logic: return "Server logic not initialized."
    return await sp_logic.get_sites()

@mcp.tool()
async def get_file_content(drive_id: str, file_id: str) -> str:
    """Read content from SharePoint files (PDF, DOCX, XLSX)."""
    if not sp_logic: return "Server logic not initialized."
    return await sp_logic.get_file(drive_id, file_id)

# --- EXPORT FOR AZURE ---
# This 'app' is what Uvicorn will serve on port 8000
app = mcp.get_asgi_app()

if __name__ == "__main__":
    # Local debugging
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
