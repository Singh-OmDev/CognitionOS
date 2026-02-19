from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
import operator
from langchain_core.messages import BaseMessage, HumanMessage

from src.agents.planner import PlannerAgent
from src.agents.researcher import ResearcherAgent
from src.agents.coder import CoderAgent

# Define the global state of the graph
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    plan: str
    research_notes: str
    code_output: str
    current_agent: str

class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.coder = CoderAgent()
        self.workflow = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Define Nodes
        workflow.add_node("planner", self._call_planner)
        workflow.add_node("researcher", self._call_researcher)
        workflow.add_node("coder", self._call_coder)

        # Define Edges
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "researcher")
        workflow.add_edge("researcher", "coder")
        workflow.add_edge("coder", END)

        return workflow.compile()

    async def _call_planner(self, state: AgentState):
        user_msg = state["messages"][-1].content
        plan = await self.planner.create_plan(user_msg)
        return {"plan": plan, "current_agent": "planner"}

    async def _call_researcher(self, state: AgentState):
        plan = state["plan"]
        # Simplified research logic
        notes = await self.researcher.run(f"Research requirements for: {plan}")
        return {"research_notes": notes, "current_agent": "researcher"}

    async def _call_coder(self, state: AgentState):
        plan = state["plan"]
        notes = state["research_notes"]
        code = await self.coder.run(f"Implement this plan: {plan} based on notes: {notes}")
        return {"code_output": code, "current_agent": "coder"}

    async def run_workflow(self, user_input: str):
        inputs = {"messages": [HumanMessage(content=user_input)]}
        async for output in self.workflow.astream(inputs):
            for key, value in output.items():
                print(f"Finished Agent: {key}")
                # return the final state of the last node
                yield value
