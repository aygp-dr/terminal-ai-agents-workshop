"""Git operation tools for version control"""
import subprocess
from typing import List, Optional

class GitTools:
    @staticmethod
    def status() -> str:
        """Get git status"""
        return subprocess.check_output(
            ["git", "status", "--short"], text=True
        )
    
    @staticmethod
    def diff(file: Optional[str] = None) -> str:
        """Get git diff"""
        cmd = ["git", "diff"]
        if file:
            cmd.append(file)
        return subprocess.check_output(cmd, text=True)
    
    @staticmethod
    def commit(message: str, files: List[str] = None) -> str:
        """Stage and commit changes"""
        # Stage files
        if files:
            subprocess.run(["git", "add"] + files)
        else:
            subprocess.run(["git", "add", "-A"])
        
        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True, text=True
        )
        return result.stdout
    
    @staticmethod
    def branch_info() -> dict:
        """Get branch information"""
        current = subprocess.check_output(
            ["git", "branch", "--show-current"], text=True
        ).strip()
        
        all_branches = subprocess.check_output(
            ["git", "branch", "-a"], text=True
        ).splitlines()
        
        return {
            "current": current,
            "local": [b.strip() for b in all_branches if not b.startswith("  remotes/")],
            "remote": [b.strip() for b in all_branches if b.startswith("  remotes/")]
        }
