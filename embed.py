"""Local embedding index for the Illini Course Guide."""

from __future__ import annotations

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import DATA_DIR, chunk_texts, load_documents

CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "illini_course_guide"

_model = None
_client = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _client


def embed_and_store(chunks: list[dict]):
    """Replace the collection with a cosine index over source-aware chunks."""
    client = get_client()
    existing = {collection.name for collection in client.list_collections()}
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
    collection = client.get_or_create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    if not chunks:
        return collection

    texts = [chunk["text"] for chunk in chunks]
    embeddings = get_model().encode(texts, normalize_embeddings=True, show_progress_bar=True).tolist()
    collection.add(
        ids=[f"{chunk['source']}__chunk{chunk['chunk_index']}" for chunk in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[
            {"source": chunk["source"], "chunk_index": chunk["chunk_index"]}
            for chunk in chunks
        ],
    )
    return collection


def ensure_index():
    """Build the small local index on first run instead of failing mysteriously."""
    collection = get_client().get_or_create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    if collection.count() == 0:
        collection = embed_and_store(chunk_texts(load_documents(DATA_DIR)))
    return collection


def retrieve(query: str, k: int = 5) -> list[dict]:
    if not query.strip():
        return []
    collection = ensure_index()
    if collection.count() == 0:
        return []

    query_embedding = get_model().encode([query], normalize_embeddings=True).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "text": document,
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "distance": float(distance),
        }
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


if __name__ == "__main__":
    chunks = chunk_texts(load_documents(DATA_DIR))
    embed_and_store(chunks)
    print(f"Indexed {len(chunks)} chunks at {CHROMA_DIR}")
