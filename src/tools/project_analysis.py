"""Project analysis tools for understanding codebases"""
import ast
import subprocess
from collections import defaultdict

class ProjectAnalyzer:
    @staticmethod
    def analyze_python_file(path: str) -> dict:
        """Analyze a Python file for structure"""
        with open(path, 'r') as f:
            tree = ast.parse(f.read())
        
        analysis = {
            "classes": [],
            "functions": [],
            "imports": []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                analysis["classes"].append({
                    "name": node.name,
                    "methods": [n.name for n in node.body 
                               if isinstance(n, ast.FunctionDef)]
                })
            elif isinstance(node, ast.FunctionDef):
                analysis["functions"].append(node.name)
            elif isinstance(node, ast.Import):
                analysis["imports"].extend(alias.name for alias in node.names)
        
        return analysis
    
    @staticmethod
    def find_todos(directory: str = ".") -> list:
        """Find all TODO comments in project"""
        result = subprocess.run(
            ["grep", "-r", "-n", "TODO", directory],
            capture_output=True, text=True
        )
        
        todos = []
        for line in result.stdout.splitlines():
            parts = line.split(":", 2)
            if len(parts) >= 3:
                todos.append({
                    "file": parts[0],
                    "line": parts[1],
                    "text": parts[2].strip()
                })
        return todos
