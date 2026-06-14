import os

from dotenv import load_dotenv
from groq import Groq

from embed import retrieve

load_dotenv()

_client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """\
You are an unofficial guide for UIUC CS students, built from real Reddit \
discussions on r/UIUC. Answer the user's question using ONLY the context \
excerpts provided below. Do not use any outside knowledge.

If the context does not contain enough information to answer the question, \
respond with exactly: "I don't have enough information on that."

Be concise and direct. Quote or paraphrase the context when helpful.\
"""


def build_prompt(question: str, hits: list[dict]) -> str:
    context_blocks = []
    for i, hit in enumerate(hits, 1):
        context_blocks.append(f"[{i}] (from {hit['source']})\n{hit['text'].strip()}")
    context = "\n\n".join(context_blocks)
    return f"Context:\n{context}\n\nQuestion: {question}"


def ask(question: str, k: int = 5) -> dict:
    hits = retrieve(question, k=k)

    response = _client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(question, hits)},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content.strip()
    sources = list(dict.fromkeys(hit["source"] for hit in hits))  # deduplicated, order preserved

    return {"answer": answer, "sources": sources}
