#!/usr/bin/env python3
"""Minimal terminal agent implementation"""
import os
import json
from typing import Dict, Any
import anthropic  # or openai, google.generativeai

class MinimalAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.tools = ToolRegistry()
        self._register_basic_tools()
    
    def _register_basic_tools(self):
        """Register basic file and shell tools"""
        # File reading tool
        self.tools.register(Tool(
            name="read_file",
            description="Read contents of a file",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"}
                },
                "required": ["path"]
            },
            function=lambda path: open(path).read()
        ))
        
        # Shell command tool
        import subprocess
        self.tools.register(Tool(
            name="run_command",
            description="Run a shell command",
            parameters={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to run"}
                },
                "required": ["command"]
            },
            function=lambda command: subprocess.check_output(
                command, shell=True, text=True
            )
        ))
    
    def chat(self, message: str) -> str:
        """Send message to LLM with tool support"""
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": message}],
            tools=self.tools.get_schema(),
            max_tokens=4096
        )
        
        # Handle tool calls
        if hasattr(response, 'tool_calls'):
            for tool_call in response.tool_calls:
                tool = self.tools.tools[tool_call.name]
                result = tool.execute(**tool_call.parameters)
                # Send result back to LLM...
        
        return response.content

if __name__ == "__main__":
    agent = MinimalAgent(os.getenv("ANTHROPIC_API_KEY"))
    while True:
        user_input = input("> ")
        if user_input.lower() in ['quit', 'exit']:
            break
        print(agent.chat(user_input))
