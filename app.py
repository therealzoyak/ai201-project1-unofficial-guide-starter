"""Gradio interface for the Illini Course Guide."""

import gradio as gr

from query import SOURCE_URLS, ask, source_title


def handle_query(question: str) -> tuple[str, str]:
    result = ask(question)
    sources = []
    seen = set()
    for hit in result["sources"]:
        filename = hit["source"]
        if filename in seen:
            continue
        seen.add(filename)
        title = source_title(filename)
        url = SOURCE_URLS.get(filename)
        relevance = max(0, 1 - hit["distance"])
        label = "strong" if relevance >= 0.65 else "related"
        sources.append(f"- [{title}]({url}) · {label} match")
    return result["answer"], "\n".join(sources) or "No source was strong enough to use."


CSS = """
.gradio-container {max-width: 1050px !important; margin: 0 auto !important;}
.hero h1 {font-size: 3rem; letter-spacing: -0.05em; margin-bottom: .25rem;}
"""


def build_interface():
    with gr.Blocks(title="Illini Course Guide", css=CSS) as demo:
        gr.Markdown(
            """
# Illini Course Guide
### The unofficial version—grounded in what students actually said.
Ask about course difficulty, electives, workload, or what older students wish they had known. Answers come from a small, cited collection of r/UIUC discussions, not official university guidance.
            """
        )
        question = gr.Textbox(
            label="What do you want to know?",
            placeholder="Should I take CS 374 as a sophomore?",
            lines=2,
        )
        ask_button = gr.Button("Ask the guide", variant="primary")
        answer = gr.Markdown(label="Answer")
        sources = gr.Markdown(label="Sources")
        gr.Examples(
            examples=[
                "How hard is it to get an A in CS 225?",
                "What electives do students consider manageable?",
                "How should I prepare for CS 341?",
                "What do graduating seniors wish they had done earlier?",
            ],
            inputs=question,
        )
        ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
        question.submit(handle_query, inputs=question, outputs=[answer, sources])
    return demo


if __name__ == "__main__":
    build_interface().launch()
