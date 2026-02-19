from typing import List
from langchain_core.messages import BaseMessage
from .base import BaseAgent
from src.memory.tool_memory import ToolMemory

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Researcher", role="Information Gatherer")
        self.tool_mem = ToolMemory()
        # In a real impl, this agent would be bound to search tools

    def get_system_prompt(self) -> str:
        return (
            "You are the Researcher Agent. Your job is to find information "
            "using available tools. Use the most reliable tools based on history."
        )
        
    async def invoke_with_tools(self, query: str):
        # This is placeholder logic for tool selection based on memory
        # In reality, we'd look up which search tool has high success rate
        stats = self.tool_mem.get_tool_stats("web_search")
        
        # ... logic to define tools ...
        
        return f"Researching: {query} (Stats: {stats})"
