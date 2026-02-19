from .base import BaseAgent
from langchain_core.messages import HumanMessage

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Critic", role="Quality Assurance")

    def get_system_prompt(self) -> str:
        return (
            "You are the Critic Agent. Your job is to strictly evaluate the execution output "
            "against the original user request. Look for bugs, missing requirements, "
            "and hallucinations. Be critical."
        )

    async def critique(self, request: str, result: str) -> str:
        prompt = (
            f"User Request: {request}\n\n"
            f"Execution Result: {result}\n\n"
            "Provide a detailed critique. If it is good, say 'PASS'. "
            "If it fails, list the specific issues."
        )
        response = self.invoke([HumanMessage(content=prompt)])
        return response.content
