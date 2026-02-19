from typing import List, Optional
from langchain_core.messages import BaseMessage, HumanMessage
from .base import BaseAgent
from src.memory.strategy_memory import StrategyMemory

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Planner", role="Strategic Planner")
        self.strategy_mem = StrategyMemory()

    def get_system_prompt(self) -> str:
        return (
            "You are the Planner Agent. Your job is to decompose high-level user requests "
            "into a step-by-step execution plan. "
            "You should check history for similar successful strategies."
        )

    async def create_plan(self, goal: str) -> str:
        # 1. Retrieve proven strategies
        strategies = self.strategy_mem.find_similar_strategies(goal)
        strategy_context = ""
        if strategies:
            strategy_context = "Here are similar past strategies:\n" + "\n".join(
                [f"- {d.page_content}" for d in strategies]
            )

        # 2. specific prompt
        prompt = (
            f"Goal: {goal}\n\n"
            f"{strategy_context}\n\n"
            "Create a detailed step-by-step plan. Output as a numbered list."
        )
        
        response = self.invoke([HumanMessage(content=prompt)])
        return response.content
