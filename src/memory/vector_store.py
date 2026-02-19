import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from typing import List, Optional
from src.core.config import settings

class VectorStore:
    def __init__(self, collection_name: str = "cognition_memory"):
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=ChromaSettings(allow_reset=True, anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        # Initialize embeddings - using Google Gemini
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )

    def store_text(self, text: str, metadata: dict, id: str):
        """Store a text chunk with metadata."""
        embedding = self.embeddings.embed_query(text)
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[id],
            embeddings=[embedding]
        )

    def query_similar(self, query: str, n_results: int = 5) -> List[Document]:
        """Retrieve similar documents."""
        query_embedding = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        documents = []
        if results["documents"]:
            for i, doc_text in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i]
                documents.append(Document(page_content=doc_text, metadata=meta))
                
        return documents

    def clear(self):
        """Clear the collection."""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(self.collection.name)
