#!/usr/bin/env python3
"""Complete terminal agent with all features"""
import os
import sys
import json
import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass
import anthropic

# Import our tools
from tools.file_operations import FileOperations
from tools.project_analysis import ProjectAnalyzer
from tools.web_search import WebSearchTool
from tools.git_operations import GitTools

@dataclass
class Message:
    role: str
    content: str
    tool_calls: List[Dict] = None
    tool_results: List[Dict] = None

class TerminalAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation = []
        self.tools = self._setup_tools()
    
    def _setup_tools(self) -> Dict[str, Any]:
        """Setup all available tools"""
        return {
            # File operations
            "create_file": {
                "function": FileOperations.create_file,
                "schema": {
                    "name": "create_file",
                    "description": "Create a new file with content",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            "edit_file": {
                "function": FileOperations.edit_file,
                "schema": {
                    "name": "edit_file",
                    "description": "Edit existing file content",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "old_content": {"type": "string"},
                            "new_content": {"type": "string"}
                        },
                        "required": ["path", "old_content", "new_content"]
                    }
                }
            },
            # Add more tools...
        }
    
    async def process_message(self, user_input: str) -> str:
        """Process user message and return response"""
        self.conversation.append(Message("user", user_input))
        
        # Get LLM response with tools
        response = await self._get_llm_response()
        
        # Process any tool calls
        if hasattr(response, 'tool_calls'):
            tool_results = await self._execute_tools(response.tool_calls)
            # Send results back to LLM
            response = await self._get_llm_response(tool_results)
        
        return response.content
    
    async def _get_llm_response(self, tool_results=None):
        """Get response from LLM"""
        messages = [{"role": m.role, "content": m.content} 
                   for m in self.conversation]
        
        if tool_results:
            messages.append({
                "role": "user",
                "content": f"Tool results: {json.dumps(tool_results)}"
            })
        
        tools = [t["schema"] for t in self.tools.values()]
        
        return self.client.messages.create(
            model="claude-3-opus-20240229",
            messages=messages,
            tools=tools,
            max_tokens=4096
        )
    
    async def _execute_tools(self, tool_calls: List[Dict]) -> List[Dict]:
        """Execute requested tools"""
        results = []
        for call in tool_calls:
            tool_name = call["name"]
            if tool_name in self.tools:
                try:
                    result = self.tools[tool_name]["function"](**call["input"])
                    results.append({
                        "tool": tool_name,
                        "result": result
                    })
                except Exception as e:
                    results.append({
                        "tool": tool_name,
                        "error": str(e)
                    })
        return results
    
    def run(self):
        """Run the agent REPL"""
        print("Terminal AI Agent")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("> ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                response = asyncio.run(self.process_message(user_input))
                print(f"\n{response}\n")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set ANTHROPIC_API_KEY")
        sys.exit(1)
    
    agent = TerminalAgent(api_key)
    agent.run()
