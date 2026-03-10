import os
import uvicorn
from fastmcp import FastMCP
from dotenv import load_dotenv

# 1. Import the specific manager class from your fork
# If your fork uses a different name, check 'sharepoint_mcp/sharepoint.py'
from sharepoint_mcp.sharepoint import SharePointManager 

load_dotenv()

# 2. Initialize FastMCP (Required for Streamable HTTP in Azure)
mcp = FastMCP(
    "SharePoint-MCP",
    dependencies=["msal", "httpx", "pandas", "python-docx", "PyPDF2", "openpyxl"]
)

# 3. Initialize the Repo's Graph Logic
# These variables MUST be set in your Azure Container App environment
sp_logic = SharePointManager(
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),
    tenant_id=os.getenv("AZURE_TENANT_ID")
)

# 4. Expose the "Missing" Graph features as Copilot Tools
@mcp.tool()
async def search_files(query: str) -> str:
    """Search for documents and files across all SharePoint sites."""
    # Calls the internal implementation in the git repo
    return await sp_logic.search_files(query)

@mcp.tool()
async def list_sites() -> str:
    """Lists SharePoint sites the current application has access to."""
    return await sp_logic.get_sites()

@mcp.tool()
async def get_document_body(site_id: str, file_id: str) -> str:
    """Downloads and extracts text from Word, PDF, or Excel files."""
    return await sp_logic.get_file_content(site_id, file_id)

# 5. Export the ASGI app for Azure/Uvicorn
app = mcp.get_asgi_app()

if __name__ == "__main__":
    # Local test command: python server.py
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
