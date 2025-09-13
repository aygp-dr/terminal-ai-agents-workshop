"""Basic tool calling pattern used by most terminal agents"""
from typing import Dict, Any, Callable
import json

class Tool:
    def __init__(self, name: str, description: str, 
                 parameters: Dict[str, Any], 
                 function: Callable):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function
    
    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters"""
        return self.function(**kwargs)

class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, tool: Tool):
        """Register a tool for use by the agent"""
        self.tools[tool.name] = tool
    
    def get_schema(self) -> list:
        """Get schema for all tools (for LLM)"""
        return [{
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters
        } for tool in self.tools.values()]
