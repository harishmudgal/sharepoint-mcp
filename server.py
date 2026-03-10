"""Main implementation of the SharePoint MCP Server."""
import os
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load your SharePoint credentials from .env
load_dotenv()

# Initialize FastMCP - this replaces the old mcp.server.Server
mcp = FastMCP(
    "SharePoint-MCP",
    dependencies=["msal", "httpx", "pandas", "python-docx", "PyPDF2", "openpyxl"]
)

# Move your existing tool functions here and use the @mcp.tool decorator
@mcp.tool()
async def search_sharepoint(query: str) -> str:
    """Search for documents and files in SharePoint."""
    # Insert your original search logic here
    return f"Results for {query}"

if __name__ == "__main__":
    # Setting transport to "http" or leaving default uses Streamable HTTP
    # This will host the endpoint at http://0.0.0.0 by default
    mcp.run(transport="http")





