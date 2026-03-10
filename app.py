from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from sharepoint_mcp.server import server  # Import your existing server logic

app = FastAPI()

# Initialize FastMCP with your existing server's name
mcp = FastMCP("SharePoint-MCP")

# Re-register your existing tools from the fork
# Example: if your fork has a 'search_files' function
@mcp.tool()
async def search_files(query: str):
    """Search for files in SharePoint."""
    # Call the original logic from your forked server
    return await server.call_tool("search_files", {"query": query})

# Mount the MCP server to the /mcp endpoint
# This creates the required GET (for streaming) and POST (for messages) routes
@app.get("/mcp")
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    return await mcp.handle_http_request(request)
