"""
MCP Server implementation for AI Chatbot feature
Registers and manages MCP tools for AI agent
"""
import asyncio
from typing import Dict, Any, Callable
from .tools import MCPTaskTools


class MCPToolRegistry:
    """Registry for managing MCP tools."""

    def __init__(self):
        self.tools = {}
        self.task_tools = MCPTaskTools()

        # Register the tools
        self._register_tools()

    def _register_tools(self):
        """Register all available MCP tools."""
        self.tools = {
            "add_task": self.task_tools.add_task,
            "list_tasks": self.task_tools.list_tasks,
            "complete_task": self.task_tools.complete_task,
            "delete_task": self.task_tools.delete_task,
            "update_task": self.task_tools.update_task
        }

    async def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a registered tool with the provided arguments."""
        if tool_name not in self.tools:
            return {
                "success": False,
                "message": f"Tool '{tool_name}' not found"
            }

        try:
            tool_func = self.tools[tool_name]
            result = await tool_func(**kwargs)
            return result
        except Exception as e:
            return {
                "success": False,
                "message": f"Error calling tool '{tool_name}': {str(e)}"
            }


# Global registry instance
registry = MCPToolRegistry()


def get_tool_registry():
    """Get the global MCP tool registry instance."""
    return registry


async def call_mcp_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """Convenience function to call an MCP tool."""
    return await registry.call_tool(tool_name, **kwargs)