from typing import List, Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from src.core.config import settings
from src.memory.vector_store import VectorStore
from src.memory.sql_store import SQLStore

class BaseAgent:
    def __init__(self, name: str, role: str, model_name: str = "gemini-2.0-flash"):
        self.name = name
        self.role = role
        self.model = ChatGoogleGenerativeAI(
            model=model_name, 
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.0
        )
        self.vector_mem = VectorStore()
        self.sql_mem = SQLStore()

    def get_system_prompt(self) -> str:
        """Override in subclasses."""
        return f"You are {self.name}, a {self.role} in CognitionOS."

    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Invoke the agent with a list of messages."""
        system_msg = SystemMessage(content=self.get_system_prompt())
        full_history = [system_msg] + messages
        return self.model.invoke(full_history)

    async def run(self, input_text: str, context: Optional[dict] = None) -> str:
        """High-level run method."""
        # 1. Retrieve relevant memory (Semantic)
        context_docs = self.vector_mem.query_similar(input_text, n_results=2)
        context_str = "\n".join([d.page_content for d in context_docs])
        
        # 2. Construct Prompt
        user_msg = f"Context:\n{context_str}\n\nTask: {input_text}"
        
        # 3. Invoke LLM
        response = self.invoke([HumanMessage(content=user_msg)])
        
        # 4. Log Interaction (Episodic)
        # Note: In a real flow, logging might happen at the Orchestrator level
        # self.sql_mem.log_interaction(...)
        
        return response.content
