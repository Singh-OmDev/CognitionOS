import asyncio
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(".")
load_dotenv()

from src.agents.researcher import ResearcherAgent

async def test_search():
    print("Initializing Researcher...")
    import os
    key = os.getenv("GOOGLE_API_KEY")
    if key:
        print(f"API Key loaded: {key[:5]}...")
    else:
        print("API Key NOT loaded")
        
    agent = ResearcherAgent()
    
    query = "What is the latest version of LangChain?"
    print(f"Running query: {query}")
    
    response = await agent.run(query)
    print("\n[Response]\n")
    print(response)

if __name__ == "__main__":
    asyncio.run(test_search())
