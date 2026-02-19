from .base import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Coder", role="Software Engineer")

    def get_system_prompt(self) -> str:
        return (
            "You are the Coder Agent. Your job is to write clean, efficient code "
            "based on the provided plan and research. "
            "You have access to file system tools."
        )

    async def write_code(self, plan: str, research: str) -> str:
        # In a real impl, this would generate code and call FS tools
        prompt = f"Plan: {plan}\nResearch: {research}\n\nShow me the code structure."
        res = self.model.invoke(prompt)
        return res.content
