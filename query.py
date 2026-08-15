"""Grounded answer generation for the Illini Course Guide."""

from __future__ import annotations

import os

from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = """You are an unofficial guide for UIUC CS students.
Answer only from the numbered excerpts supplied from r/UIUC discussions.
You may synthesize a reasonable implication across excerpts, but distinguish it
from something a student said directly. Cite supporting excerpts inline as [1],
[2], and so on. If the excerpts do not support an answer, say: "I don't have
enough information on that." Be concise, candid, and remind the user when a
claim is a student opinion rather than official course policy."""

SOURCE_URLS = {
    "ease_of_getting_an_a_in_cs225.txt": "https://www.reddit.com/r/UIUC/comments/9g5mpi/ease_of_getting_an_a_in_cs_225/",
    "does_cs225_get_harder_over_time.txt": "https://www.reddit.com/r/UIUC/comments/ifqkgt/does_cs_225_get_harder_as_time_progressestoward/",
    "most_useful_cs_courses_alumni.txt": "https://www.reddit.com/r/UIUC/comments/176n8tq/to_cs_alumni_what_are_some_of_the_most_useful_cs/",
    "reflections_from_a_senior_in_cs.txt": "https://www.reddit.com/r/UIUC/comments/1cs5ull/reflections_from_a_senior_in_cs/",
    "cs_major_do_nots_freshman_advice.txt": "https://www.reddit.com/r/UIUC/comments/1lyc4vx/cs_major_do_nots_that_i_wish_i_knew_as_a_freshman/",
    "easy_fun_cs_electives.txt": "https://www.reddit.com/r/UIUC/comments/jygo4g/easyfun_cs_electives/",
    "taking_cs374_as_incoming_sophomore.txt": "https://www.reddit.com/r/UIUC/comments/1kwxfy7/taking_cs_374_as_an_incoming_sophomore/",
    "cs421_student_performance_discussion.txt": "https://www.reddit.com/r/UIUC/comments/1h8yomn/cs421_students_are_performing_better_currently/",
    "cs_course_difficulty_tier_list.txt": "https://www.reddit.com/r/UIUC/comments/10w3far/cs_course_difficulty_tier_list/",
    "cs440_447_elective_comparison.txt": "https://www.reddit.com/r/UIUC/comments/141b2lk/out_of_all_of_the_cs_courses_between_440447_which/",
    "easy_cs_electives_for_minor.txt": "https://www.reddit.com/r/UIUC/comments/t92a7m/easy_cs_electives_to_finish_minor/",
    "cs341_prep_advice.txt": "https://www.reddit.com/r/UIUC/comments/1psmiep/cs_341/",
}


def source_title(filename: str) -> str:
    return filename.removesuffix(".txt").replace("_", " ").title().replace("Cs", "CS")


def build_prompt(question: str, hits: list[dict]) -> str:
    context = "\n\n".join(
        f"[{index}] {source_title(hit['source'])}\n{hit['text'].strip()}"
        for index, hit in enumerate(hits, 1)
    )
    return f"Context:\n{context}\n\nQuestion: {question.strip()}"


def ask(question: str, k: int = 5) -> dict:
    if not question or not question.strip():
        return {"answer": "Ask a question about UIUC CS courses or student experience.", "sources": []}

    from embed import retrieve

    hits = retrieve(question, k=k)
    if not hits:
        return {"answer": "I don't have enough information on that.", "sources": []}

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or Groq is None:
        return {
            "answer": "The local retrieval index is ready, but GROQ_API_KEY is required to generate a grounded answer.",
            "sources": hits,
        }

    response = Groq(api_key=api_key).chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(question, hits)},
        ],
        temperature=0.2,
    )
    return {
        "answer": response.choices[0].message.content.strip(),
        "sources": hits,
    }
