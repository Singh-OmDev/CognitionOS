import asyncio
import sys
from datetime import datetime, timezone
sys.path.append(".")

from src.memory.tool_memory import ToolMemory
from src.agents.reflector import ReflectorAgent

async def test_learning_loop():
    print("Testing Tool Memory (Alpha-Beta)...")
    tm = ToolMemory()
    import uuid
    tool_name = f"test_tool_{uuid.uuid4()}"
    
    # Simulate partial success (0.5 score)
    tm.update_tool_stats(tool_name, success_score=0.5, duration_ms=200.0)
    stats = tm.get_tool_stats(tool_name)
    
    print(f"Stats: {stats}")
    assert stats["successes"] == 0.5
    assert stats["failures"] == 0.5
    assert stats["total_uses"] >= 1
    
    print("Testing Reflector Lesson Extraction...")
    agent = ReflectorAgent()
    
    # Mock invoke to avoid API Rate Limits during testing
    from langchain_core.messages import AIMessage
    async def mock_invoke(messages):
        return AIMessage(content="When searching fails, avoid using generic terms because they yield too many results.")
    agent.invoke = mock_invoke
    
    # Mock task state
    task_state = {
        "plan": "Search for github.com",
        "result": "Error: Connection timeout",
        "critique": "Failed to retrieve data."
    }
    
    lesson = await agent.extract_lesson(task_state, success=False)
    print(f"Lesson Extracted: {lesson}")
    assert "avoid" in lesson.lower() or "when" in lesson.lower()
    
    print("\nAll learning tests passed!")

if __name__ == "__main__":
    asyncio.run(test_learning_loop())
