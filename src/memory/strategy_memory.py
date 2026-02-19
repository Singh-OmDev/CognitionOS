from typing import List, Optional
from langchain_core.documents import Document
from .vector_store import VectorStore

class StrategyMemory:
    def __init__(self):
        # We reuse the VectorStore but targeting a specific collection or checking metadata
        self.vector_store = VectorStore(collection_name="cognition_strategies")

    def save_strategy(self, goal: str, plan: str, outcome: str, metadata: Optional[dict] = None):
        """Save a successful (or failed) strategy for future reference."""
        full_text = f"GOAL: {goal}\nPLAN: {plan}\nOUTCOME: {outcome}"
        
        if metadata is None:
            metadata = {}
            
        metadata.update({
            "type": "strategy",
            "goal": goal,
            "outcome": outcome
        })
        
        # Simple ID generation
        import uuid
        strategy_id = str(uuid.uuid4())
        
        self.vector_store.store_text(
            text=full_text,
            metadata=metadata,
            id=strategy_id
        )

    def find_similar_strategies(self, current_goal: str, n_results: int = 3) -> List[Document]:
        """Find strategies used for similar goals."""
        return self.vector_store.query_similar(current_goal, n_results=n_results)
