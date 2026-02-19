from typing import List
from langchain_core.messages import BaseMessage, HumanMessage
from .base import BaseAgent
from src.mcp.filesystem.tool import FileSystemTools

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Coder", role="Software Engineer")
        self.fs_tools = FileSystemTools(root_dir=".")
        # In real world, bind self.fs_tools.get_tools() to model

    def get_system_prompt(self) -> str:
        return (
            "You are the Coder Agent. You can read/write files to implement features. "
            "Always check existing files before writing."
        )

    async def run(self, input_text: str) -> str:
        # Placeholder tool usage logic
        # 1. If input implies writing file, use tool
        if "write" in input_text.lower() and "file" in input_text.lower():
            # Minimal parsing logic for demo
            # "Write hello world to test.txt"
            # This is where an LLM function call would happen
            pass
            
        response = self.invoke([HumanMessage(content=input_text)])
        return response.content

    async def write_code(self, plan: str, research: str) -> str:
        # In a real impl, this would generate code and call FS tools
        prompt = f"Plan: {plan}\nResearch: {research}\n\nShow me the code structure."
        res = self.model.invoke(prompt)
        return res.content
