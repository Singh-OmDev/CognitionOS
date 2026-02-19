from duckduckgo_search import DDGS
from langchain_core.tools import Tool

class SearchTool:
    def __init__(self):
        pass
        
    def get_tool(self) -> Tool:
        return Tool(
            name="web_search",
            func=self.run,
            description="Useful for searching the internet for current events and technical documentation."
        )

    def run(self, query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=3)]
                return str(results)
        except Exception as e:
            print(f"DEBUG: Search error: {e}")
            return f"Error searching for '{query}': {str(e)}"
