"""
Generic tool base class for Hypernode MCP Server tools.
Provides common functionality that other tools can inherit from.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from utils.command_executor import CommandExecutor, CommandResult

class GenericTool(ABC):
    """
    Base class for all MCP tools in the Hypernode MCP Server.
    Provides common functionality.
    """
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """
        Abstract method to be implemented by subclasses.
        """
        return "Tool has not been implemented."

class ToolCollection:
    """
    Collection of tools for the MCP server.
    """
    
    def __init__(self):
        self.tools = []
        
    def add_tool(self, tool: GenericTool):
        self.tools.append(tool)