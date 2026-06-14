from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import DATA_DIR, chunk_texts, load_documents

CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "uiuc_cs_guide"

_model = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path=str(CHROMA_DIR))


def embed_and_store(chunks: list[dict]) -> chromadb.Collection:
    # Delete and recreate so the cosine metric is applied cleanly
    _client.delete_collection(COLLECTION_NAME) if COLLECTION_NAME in [c.name for c in _client.list_collections()] else None
    collection = _client.get_or_create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [c["text"] for c in chunks]
    embeddings = _model.encode(texts, normalize_embeddings=True, show_progress_bar=True).tolist()

    collection.add(
        ids=[f"{c['source']}__chunk{c['chunk_index']}" for c in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
    )
    return collection


def retrieve(query: str, k: int = 5) -> list[dict]:
    collection = _client.get_or_create_collection(COLLECTION_NAME)
    query_embedding = _model.encode([query], normalize_embeddings=True).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({"text": doc, "source": meta["source"], "chunk_index": meta["chunk_index"], "distance": dist})
    return hits


if __name__ == "__main__":
    print("=== UIUC CS Unofficial Guide — Embedding ===\n")

    docs = load_documents(DATA_DIR)
    chunks = chunk_texts(docs)
    print(f"Embedding {len(chunks)} chunks...\n")
    embed_and_store(chunks)
    print(f"\nStored {len(chunks)} chunks in ChromaDB at {CHROMA_DIR}\n")

    test_queries = [
        "How hard is it to get an A in CS 225?",
        "Should an incoming sophomore take CS 374?",
        "What CS electives are easiest?",
    ]

    for query in test_queries:
        print(f"Query: {query}")
        print("-" * 60)
        for hit in retrieve(query):
            print(f"  [{hit['distance']:.4f}] {hit['source']} (chunk {hit['chunk_index']})")
            print(f"  {hit['text'][:300].strip()}...")
            print()
        print()
