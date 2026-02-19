import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from src.core.orchestration import Orchestrator

@pytest.mark.asyncio
async def test_orchestration_flow():
    # Mock the agents to avoid API calls
    with patch("src.agents.planner.PlannerAgent.create_plan", new_callable=AsyncMock) as mock_plan, \
         patch("src.agents.researcher.ResearcherAgent.run", new_callable=AsyncMock) as mock_research, \
         patch("src.agents.coder.CoderAgent.run", new_callable=AsyncMock) as mock_code:
        
        mock_plan.return_value = "1. Step one\n2. Step two"
        mock_research.return_value = "Research found: X, Y, Z"
        mock_code.return_value = "def hello(): print('world')"

        orchestrator = Orchestrator()
        
        results = []
        async for step in orchestrator.run_workflow("Build a hello world app"):
            results.append(step)
            
        # Verify the flow
        assert len(results) == 3
        assert results[0]["current_agent"] == "planner"
        assert results[0]["plan"] == "1. Step one\n2. Step two"
        
        assert results[1]["current_agent"] == "researcher"
        assert results[1]["research_notes"] == "Research found: X, Y, Z"
        
        assert results[2]["current_agent"] == "coder"
        assert results[2]["code_output"] == "def hello(): print('world')"
