import chromadb
from chromadb.config import Settings as ChromaSettings
from openai import OpenAI
from pathlib import Path
from typing import Any

from .knowledge_loader import load_knowledge_base, create_chunks


class VectorStore:
    """ChromaDB-based vector store for RAG retrieval."""
    
    def __init__(
        self,
        persist_directory: str,
        knowledge_base_path: str,
        openai_api_key: str,
        embedding_model: str = "text-embedding-3-small"
    ):
        self.persist_directory = persist_directory
        self.knowledge_base_path = knowledge_base_path
        self.embedding_model = embedding_model
        self.openai_client = OpenAI(api_key=openai_api_key)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        self.collection = self.client.get_or_create_collection(
            name="qasim_knowledge",
            metadata={"description": "Qasim's professional knowledge base"}
        )
        
        # Index if empty
        if self.collection.count() == 0:
            self._index_knowledge_base()
    
    def _get_embedding(self, text: str) -> list[float]:
        """Get embedding from OpenAI."""
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def _index_knowledge_base(self) -> None:
        """Load and index the knowledge base."""
        print("Indexing knowledge base...")
        
        knowledge_base = load_knowledge_base(self.knowledge_base_path)
        chunks = create_chunks(knowledge_base)
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        embeddings = []
        
        for chunk in chunks:
            ids.append(chunk["id"])
            documents.append(chunk["text"])
            metadatas.append(chunk["metadata"])
            embeddings.append(self._get_embedding(chunk["text"]))
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
        
        print(f"Indexed {len(chunks)} chunks.")
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_type: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Search for relevant chunks.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_type: Optional filter by type (profile, experience, project, skills, etc.)
        
        Returns:
            List of relevant chunks with scores
        """
        query_embedding = self._get_embedding(query)
        
        where_filter = None
        if filter_type:
            where_filter = {"type": filter_type}
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0
                })
        
        return formatted_results
    
    def reindex(self) -> None:
        """Force reindex of the knowledge base."""
        # Delete existing collection
        self.client.delete_collection("qasim_knowledge")
        
        # Recreate and index
        self.collection = self.client.create_collection(
            name="qasim_knowledge",
            metadata={"description": "Qasim's professional knowledge base"}
        )
        self._index_knowledge_base()
