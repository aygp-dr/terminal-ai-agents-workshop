"""File operation tools for terminal agents"""
import os
import shutil
from pathlib import Path

class FileOperations:
    @staticmethod
    def create_file(path: str, content: str) -> str:
        """Create a new file with content"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return f"Created file: {path}"
    
    @staticmethod
    def edit_file(path: str, old_content: str, new_content: str) -> str:
        """Replace content in a file"""
        with open(path, 'r') as f:
            content = f.read()
        
        if old_content not in content:
            raise ValueError(f"Content not found in {path}")
        
        content = content.replace(old_content, new_content, 1)
        with open(path, 'w') as f:
            f.write(content)
        
        return f"Updated {path}"
    
    @staticmethod
    def list_directory(path: str = ".") -> str:
        """List directory contents"""
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                items.append(f"📁 {item}/")
            else:
                size = os.path.getsize(item_path)
                items.append(f"📄 {item} ({size} bytes)")
        return "\n".join(items)
