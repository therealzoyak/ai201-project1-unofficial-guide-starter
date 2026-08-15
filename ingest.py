import re
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def clean_text(text: str) -> str:
    # Collapse markdown links [label](url) → label
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Strip bare URLs
    text = re.sub(r"https?://\S+", "", text)
    # Strip bold/italic markers
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    # Strip markdown headers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Strip leftover special characters (>, |, ~, ^)
    text = re.sub(r"[>|~^]+", "", text)
    # Collapse runs of blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse runs of spaces/tabs on a single line
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def load_documents(data_dir: Path) -> list[tuple[str, str]]:
    docs = []
    for path in sorted(data_dir.glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        cleaned = clean_text(raw)
        if cleaned:
            docs.append((path.name, cleaned))
    return docs


def chunk_texts(docs: list[tuple[str, str]]) -> list[dict]:
    chunks: list[dict] = []
    for name, text in docs:
        for index, chunk in enumerate(split_text(text)):
            chunks.append({"source": name, "chunk_index": index, "text": chunk})
    return chunks


def split_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> list[str]:
    """Split text at nearby whitespace while retaining a small context overlap."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Use chunk_size > overlap >= 0")
    if len(text) <= chunk_size:
        return [text] if text else []

    chunks = []
    start = 0
    while start < len(text):
        proposed_end = min(start + chunk_size, len(text))
        end = proposed_end
        if proposed_end < len(text):
            boundary = text.rfind(" ", start + chunk_size // 2, proposed_end)
            if boundary > start:
                end = boundary
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return [chunk for chunk in chunks if chunk]


def main():
    print("=== UIUC CS Unofficial Guide — Ingestion ===\n")

    print(f"Loading .txt files from {DATA_DIR}...")
    docs = load_documents(DATA_DIR)
    print(f"Loaded {len(docs)} documents.\n")

    print("Document character counts:")
    for name, text in docs:
        print(f"  {name}: {len(text):,} chars")
    print()

    print("Chunking (1500 chars / 200 overlap)...")
    chunks = chunk_texts(docs)
    print(f"Total chunks: {len(chunks)}\n")

    print("=== 5 Sample Chunks ===\n")
    for i, chunk in enumerate(chunks[:5], 1):
        text = chunk["text"]
        preview = text[:500] + ("..." if len(text) > 500 else "")
        print(f"--- Chunk {i} ---")
        print(f"Source: {chunk['source']}")
        print(preview)
        print()


if __name__ == "__main__":
    main()
