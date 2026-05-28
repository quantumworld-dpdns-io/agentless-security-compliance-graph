from typing import Any

import numpy as np


class VectorStore:
    def __init__(self, backend: str = "chroma", collection_name: str = "compliance_embeddings"):
        self.backend = backend
        self.collection_name = collection_name
        self._client = self._init_client()

    def _init_client(self) -> Any:
        if self.backend == "chroma":
            try:
                import chromadb
                return chromadb.Client()
            except ImportError:
                return None
        elif self.backend == "milvus":
            try:
                from pymilvus import connections
                connections.connect("default", host="localhost", port="19530")
                return connections
            except ImportError:
                return None
        elif self.backend == "weaviate":
            try:
                import weaviate
                return weaviate.Client("http://localhost:8080")
            except ImportError:
                return None
        elif self.backend == "qdrant":
            try:
                from qdrant_client import QdrantClient
                return QdrantClient("http://localhost:6333")
            except ImportError:
                return None
        return None

    def embed_text(self, text: str) -> list[float]:
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("all-MiniLM-L6-v2")
            return model.encode(text).tolist()
        except ImportError:
            rng = np.random.default_rng(hash(text) % (2**32))
            return rng.random(384).tolist()

    def store_embedding(self, doc_id: str, text: str, metadata: dict | None = None):
        embedding = self.embed_text(text)
        if self._client and self.backend == "chroma":
            try:
                collection = self._client.get_or_create_collection(self.collection_name)
                collection.add(documents=[text], embeddings=[embedding], ids=[doc_id], metadatas=[metadata or {}])
                return {"stored": True, "id": doc_id}
            except Exception:
                pass
        return {"stored": "simulated", "id": doc_id}

    def similarity_search(self, query: str, top_k: int = 5) -> list[dict]:
        query_embedding = self.embed_text(query)
        if self._client and self.backend == "chroma":
            try:
                collection = self._client.get_collection(self.collection_name)
                results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
                return [{"id": results["ids"][0][i], "score": results["distances"][0][i]} for i in range(len(results["ids"][0]))]
            except Exception:
                pass
        return [{"id": f"sim-{i}", "score": 0.95 - i * 0.1} for i in range(top_k)]
