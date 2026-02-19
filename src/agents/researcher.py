from typing import List
from langchain_core.messages import BaseMessage, HumanMessage
from .base import BaseAgent
from src.memory.tool_memory import ToolMemory
from src.mcp.search.tool import SearchTool

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Researcher", role="Information Gatherer")
        self.tool_mem = ToolMemory()
        self.search_tool = SearchTool()
        # Bind tools to the model if using function calling, 
        # or just make them available for manual invocation
        # self.model = self.model.bind_tools([self.search_tool.get_tool()])

    def get_system_prompt(self) -> str:
        return (
            "You are the Researcher Agent. Your job is to find information "
            "using available tools. Use the 'web_search' tool for current data."
        )
        
    async def run(self, query: str) -> str:
        # Simple tool usage logic for now (ReAct pattern would be better)
        # 1. Search
        print(f"[Researcher] Searching for: {query}")
        search_results = self.search_tool.run(query)
        
        # 2. Update Tool Memory (Success)
        self.tool_mem.update_tool_stats("web_search", success=True, duration_ms=100.0)
        
        # 3. Synthesize
        prompt = (
            f"Query: {query}\n\n"
            f"Search Results: {search_results}\n\n"
            "Summarize the findings."
        )
        response = self.invoke([HumanMessage(content=prompt)])
        return response.content
