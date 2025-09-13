"""Compare different terminal AI agents"""
import time
import subprocess
from typing import Dict, List, Tuple

class AgentBenchmark:
    def __init__(self):
        self.agents = {
            "claude-code": "claude",
            "aider": "aider",
            "amp": "amp",
            "gemini-cli": "gemini"
        }
        self.tasks = [
            "Create a Python function to calculate fibonacci",
            "Fix the syntax error in main.py",
            "Add error handling to the database connection",
            "Write unit tests for the Calculator class"
        ]
    
    def run_task(self, agent: str, task: str) -> Tuple[str, float]:
        """Run a single task with an agent"""
        start = time.time()
        
        # Agent-specific command construction
        if agent == "claude-code":
            cmd = ["claude", "-m", "sonnet", task]
        elif agent == "aider":
            cmd = ["aider", "--message", task]
        elif agent == "amp":
            cmd = ["amp", "-x", task]
        else:
            cmd = ["gemini", task]
        
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60
            )
            elapsed = time.time() - start
            return result.stdout, elapsed
        except subprocess.TimeoutExpired:
            return "TIMEOUT", 60.0
    
    def compare_agents(self) -> Dict[str, List[float]]:
        """Compare all agents on all tasks"""
        results = {agent: [] for agent in self.agents}
        
        for task in self.tasks:
            print(f"\nTask: {task}")
            for agent_name, agent_cmd in self.agents.items():
                output, time_taken = self.run_task(agent_cmd, task)
                results[agent_name].append(time_taken)
                print(f"  {agent_name}: {time_taken:.2f}s")
        
        return results
