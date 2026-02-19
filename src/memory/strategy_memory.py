from .vector_store import VectorStore
from .sql_store import SQLStore

class StrategyMemory:
    def __init__(self):
        self.vector_store = VectorStore(collection_name="cognition_strategies")
        # In future, link to SQL for structured feedback logs
        
    def retrieve_strategy(self, query: str) -> str:
        """Retrieve relevant past strategies or lessons."""
        docs = self.vector_store.query_similar(query, n_results=1)
        if not docs:
            return ""
        return f"Past Strategy/Lesson: {docs[0].page_content}"

    def find_similar_strategies(self, query: str, k: int = 3):
        """Retrieve a list of similar strategies."""
        return self.vector_store.query_similar(query, n_results=k)
        
    def store_lesson(self, query: str, lesson: str, score: float):
        """Store a lesson learned from a specific query context."""
        # Only store significant lessons
        if score > 0.8:
            prefix = "[SUCCESS PATTERN]"
        elif score < 0.4:
            prefix = "[FAILURE WARNING]"
        else:
            return # Ignore mediocre results to reduce noise
            
        content = f"{prefix} Context: {query} -> Lesson: {lesson}"
        metadata = {"score": score, "type": "strategy"}
        
        # Use query as ID for simple deduplication (in real app, use content hash)
        import uuid
        self.vector_store.store_text(content, metadata, str(uuid.uuid4()))
