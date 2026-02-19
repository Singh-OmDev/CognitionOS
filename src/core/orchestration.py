from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated, Optional
import operator
from langchain_core.messages import BaseMessage, HumanMessage

from src.agents.planner import PlannerAgent
from src.agents.researcher import ResearcherAgent
from src.agents.coder import CoderAgent
from src.agents.critic import CriticAgent
from src.agents.reflector import ReflectorAgent

# Define the global state of the graph
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    plan: str
    research_notes: str
    code_output: str
    critique: str
    reflection: str
    current_agent: str
    loop_count: int

MAX_RETRIES = 3

class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.coder = CoderAgent()
        self.critic = CriticAgent()
        self.reflector = ReflectorAgent()
        self.workflow = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Define Nodes
        workflow.add_node("planner", self._call_planner)
        workflow.add_node("researcher", self._call_researcher)
        workflow.add_node("coder", self._call_coder)
        workflow.add_node("critic", self._call_critic)
        workflow.add_node("reflector", self._call_reflector)

        # Define Edges
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "researcher")
        workflow.add_edge("researcher", "coder")
        workflow.add_edge("coder", "critic")
        
        # Conditional Edge
        workflow.add_conditional_edges(
            "critic",
            self._check_quality,
            {
                "pass": END,
                "fail": "reflector"
            }
        )
        workflow.add_edge("reflector", "planner")

        return workflow.compile()

    def _check_quality(self, state: AgentState):
        critic_msg = state.get("critique", "").lower()
        loop_count = state.get("loop_count", 0)
        
        if loop_count >= MAX_RETRIES:
            return "pass" # Force exit
            
        if "pass" in critic_msg:
            return "pass"
        return "fail"

    async def _call_planner(self, state: AgentState):
        user_msg = state["messages"][0].content
        reflection = state.get("reflection", "")
        
        # If we have reflection, append it to the prompt
        if reflection:
            prompt = f"Original Request: {user_msg}\n\nPrevious Failure Feedback: {reflection}\n\nUpdate the plan:"
            plan = await self.planner.create_plan(prompt)
        else:
            plan = await self.planner.create_plan(user_msg)
            
        return {"plan": plan, "current_agent": "planner"}

    async def _call_researcher(self, state: AgentState):
        plan = state["plan"]
        notes = await self.researcher.run(f"Research requirements for: {plan}")
        return {"research_notes": notes, "current_agent": "researcher"}

    async def _call_coder(self, state: AgentState):
        plan = state["plan"]
        notes = state.get("research_notes", "")
        code = await self.coder.run(f"Implement this plan: {plan} based on notes: {notes}")
        return {"code_output": code, "current_agent": "coder"}
        
    async def _call_critic(self, state: AgentState):
        user_msg = state["messages"][0].content
        code = state["code_output"]
        critique = await self.critic.critique(user_msg, code)
        return {"critique": critique, "current_agent": "critic"}
        
    async def _call_reflector(self, state: AgentState):
        critique = state["critique"]
        plan = state["plan"]
        reflection = await self.reflector.reflect(critique, plan)
        
        # Learning Loop
        print("[Orchestrator] Running Learning Loop...")
        result = state.get("code_output", "No Output")
        critique = state.get("critique", "No Critique")
        
        success = "approved" in critique.lower()
        lesson = await self.reflector.extract_lesson(
            {"plan": plan, "result": result, "critique": critique}, 
            success=success
        )
        print(f"[Orchestrator] Lesson Learned: {lesson}")
        
        # Calculate Confidence Score (Mock for now, real implementation would use Critic's verdict)
        confidence = 0.9 if success else 0.4

        return {
            "reflection": reflection, 
            "current_agent": "Reflector",
            "loop_count": state.get("loop_count", 0) + 1,
            "lesson": lesson,
            "confidence": confidence,
            "step": state.get("loop_count", 0) + 1
        }

    async def run_workflow(self, user_input: str):
        inputs = {
            "messages": [HumanMessage(content=user_input)],
            "loop_count": 0
        }
        async for output in self.workflow.astream(inputs):
            for key, value in output.items():
                # Yield context for CLI display
                yield value
