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
             patch("src.agents.coder.CoderAgent.run", new_callable=AsyncMock) as mock_code, \
             patch("src.agents.critic.CriticAgent.critique", new_callable=AsyncMock) as mock_critique, \
             patch("src.agents.reflector.ReflectorAgent.reflect", new_callable=AsyncMock) as mock_reflect:
            
            # Setup mocks for a loop scenario: Fail once, then Pass
            mock_plan.side_effect = ["Plan A", "Plan B (Fixed)"]
            mock_research.return_value = "Research found."
            mock_code.return_value = "Code"
            mock_critique.side_effect = ["FAIL: Too simple", "PASS: Good job"]
            mock_reflect.return_value = "Make it more complex."

            print("Initializing Orchestrator...")
            orchestrator = Orchestrator()
            
            print("Running workflow...")
            results = []
            async for step in orchestrator.run_workflow("Build app"):
                print(f"Step received: {step.keys()}")
                results.append(step)
                
            # Expected sequence:
            # 1. Planner (Plan A)
            # 2. Researcher
            # 3. Coder
            # 4. Critic (Fail)
            # 5. Reflector
            # 6. Planner (Plan B)
            # 7. Researcher
            # 8. Coder
            # 9. Critic (Pass)
            
            print(f"Total steps: {len(results)}")
            if len(results) != 9:
                print(f"FAILED: Expected 9 steps, got {len(results)}")
                return

            if results[4]["current_agent"] != "reflector":
                 print(f"FAILED: Expected reflector at step 5, got {results[4]['current_agent']}")
                 return

            print("SUCCESS: Reflection loop passed!")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
