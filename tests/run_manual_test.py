import asyncio
import sys
from unittest.mock import MagicMock, AsyncMock, patch

# Add src to path
sys.path.append(".")

from src.core.orchestration import Orchestrator

async def run_test():
    print("Starting manual test...")
    try:
        # Mock Memory classes to avoid DB connections
        with patch("src.agents.base.VectorStore"), \
             patch("src.agents.base.SQLStore"), \
             patch("src.agents.planner.StrategyMemory"), \
             patch("src.agents.researcher.ToolMemory"), \
             patch("src.agents.planner.PlannerAgent.create_plan", new_callable=AsyncMock) as mock_plan, \
             patch("src.agents.researcher.ResearcherAgent.run", new_callable=AsyncMock) as mock_research, \
             patch("src.agents.coder.CoderAgent.run", new_callable=AsyncMock) as mock_code:
            
            mock_plan.return_value = "1. Step one\n2. Step two"
            mock_research.return_value = "Research found: X, Y, Z"
            mock_code.return_value = "def hello(): print('world')"

            print("Initializing Orchestrator...")
            orchestrator = Orchestrator()
            
            print("Running workflow...")
            results = []
            async for step in orchestrator.run_workflow("Build a hello world app"):
                print(f"Step received: {step.keys()}")
                results.append(step)
                
            # Verify results
            print(f"Total steps: {len(results)}")
            if len(results) != 3:
                print("FAILED: Expected 3 steps")
                return
                
            if results[0]["current_agent"] != "planner":
                print(f"FAILED: Step 1 agent mismatch. Got {results[0]['current_agent']}")
                return

            if results[2]["code_output"] != "def hello(): print('world')":
                 print("FAILED: Code output mismatch")
                 return

            print("SUCCESS: Manual verification passed!")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
