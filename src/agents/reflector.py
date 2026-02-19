from .base import BaseAgent
from langchain_core.messages import HumanMessage

class ReflectorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Reflector", role="Root Cause Analyst")

    def get_system_prompt(self) -> str:
        return (
            "You are the Reflector Agent. When a task fails quality checks, "
            "you analyze the critique and provide specific guidance to the Planner "
            "on how to fix the plan."
        )

    async def reflect(self, critique: str, past_plan: str) -> str:
        prompt = (
            f"Critique: {critique}\n\n"
            f"Past Plan: {past_plan}\n\n"
            "Why did this fail? Provide specific instructions for the Planner to improve the next attempt."
        )
        response = self.invoke([HumanMessage(content=prompt)])
        return response.content
