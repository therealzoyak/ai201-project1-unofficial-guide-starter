# Illini Course Guide

Official course descriptions tell you what a class covers. They rarely tell you whether the MPs quietly consume your week, which electives students actually enjoyed, or what seniors wish they had done differently.

Illini Course Guide is a small retrieval-augmented guide built from candid r/UIUC discussions. It searches a local semantic index, asks an LLM to answer only from the retrieved excerpts, and links every source thread so the user can read the conversation—not just trust a generated summary.

[Watch the original walkthrough](https://www.loom.com/share/67dec7fa2c8f4bd69c7296d3e5704db0)

## What it does

- cleans and chunks 12 UIUC student discussions while preserving source identity
- embeds 23 chunks locally with `all-MiniLM-L6-v2`
- retrieves with cosine distance in ChromaDB
- generates concise, inline-cited answers through Groq
- distinguishes student opinion from official policy
- shows linked source threads and a plain-language relevance label
- builds the local index automatically on first use

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="..."
python app.py
```

The first run downloads the embedding model and builds `chroma_db/`. Later runs reuse the local index.

## Pipeline

```text
r/UIUC threads
    → markdown and URL cleanup
    → source-aware chunks (1,500 characters / 200 overlap)
    → normalized MiniLM embeddings
    → cosine retrieval in ChromaDB
    → grounded answer with inline [n] citations
    → clickable Reddit sources
```

## Evaluation

I evaluated five realistic questions covering CS 225, CS 341, CS 374, electives, and senior reflections. Retrieval found relevant material for all five. Four answers were accurate; the failure was a senior-regret question where the correct document was retrieved but the generator treated advice phrased as “do X” as unrelated to “what do you regret?”

I changed the grounding policy to allow a clearly labeled inference across excerpts while still prohibiting outside knowledge. That fixes the overly literal behavior without letting the model freestyle.

## Limits

- Twelve Reddit threads are a useful prototype, not representative evidence.
- Course structure and instructors change; every answer should be checked against current official information.
- Similarity labels describe retrieval closeness, not factual confidence.
- Student anecdotes can be biased toward unusually positive or negative experiences.

## Tests

```bash
python -m unittest discover -s tests
```

The lightweight tests cover cleaning, source-aware chunking, readable source titles, and numbered prompt construction.

## Origin

Built in CodePath's Applied AI program. The course supplied the milestone structure; I selected the domain and sources, built the ingestion and retrieval pipeline, diagnosed the generation failure, added citation handling, and designed the student-facing product.
