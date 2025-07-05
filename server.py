"""
Hypernode MCP Server with HTTP and SSE support using FastMCP 2.0.
"""

from fastmcp import FastMCP
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("Hypernode MCP Server")

# Auto-register all tools
from tools import register_all_tools
register_all_tools(mcp)

if __name__ == "__main__":
    # TODO: add parameters for other transports
    mcp.run(transport="stdio")