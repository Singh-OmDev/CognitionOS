import os
from pathlib import Path
from typing import List, Union
from langchain_core.tools import Tool

class FileSystemTools:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        
    def get_tools(self) -> List[Tool]:
        return [
            Tool(
                name="read_file",
                func=self.read_file,
                description="Read content of a file. Args: file_path"
            ),
            Tool(
                name="write_file",
                func=self.write_file,
                description="Write content to a file. Args: file_path, content"
            ),
            Tool(
                name="list_directory",
                func=self.list_directory,
                description="List files in a directory. Args: dir_path"
            )
        ]

    def _safe_path(self, path_str: str) -> Path:
        """Resolve path and ensure it's within the root directory (Sandbox)."""
        full_path = (self.root / path_str).resolve()
        
        
        try:
            full_path.relative_to(self.root)
        except ValueError:
             raise ValueError(f"Access denied: {path_str} is outside the workspace.")
             
        return full_path

    def read_file(self, file_path: str) -> str:
        try:
            path = self._safe_path(file_path)
            if not path.exists():
                return f"Error: File {file_path} does not exist."
            return path.read_text(encoding='utf-8')
        except Exception as e:
            return f"Error reading file {file_path}: {str(e)}"

    def write_file(self, file_path: str, content: str) -> str:
        try:
            path = self._safe_path(file_path)
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file {file_path}: {str(e)}"

    def list_directory(self, dir_path: str = ".") -> str:
        try:
            path = self._safe_path(dir_path)
            if not path.is_dir():
                return f"Error: {dir_path} is not a directory."
            
            items = []
            for item in path.iterdir():
                type_str = "DIR" if item.is_dir() else "FILE"
                items.append(f"{type_str}: {item.name}")
            return "\n".join(items)
        except Exception as e:
             return f"Error listing directory {dir_path}: {str(e)}"
