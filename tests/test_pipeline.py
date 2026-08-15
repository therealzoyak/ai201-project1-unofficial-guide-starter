import unittest

from ingest import chunk_texts, clean_text
from query import build_prompt, source_title


class PipelineTests(unittest.TestCase):
    def test_clean_text_removes_markdown_links_but_keeps_label(self):
        self.assertEqual(clean_text("Read [this guide](https://example.com)"), "Read this guide")

    def test_chunks_keep_source_metadata(self):
        chunks = chunk_texts([("thread.txt", "A useful comment about CS 225.")])
        self.assertEqual(chunks[0]["source"], "thread.txt")
        self.assertEqual(chunks[0]["chunk_index"], 0)

    def test_prompt_numbers_sources(self):
        prompt = build_prompt(
            "Is it hard?",
            [{"source": "cs225_thread.txt", "text": "Start MPs early."}],
        )
        self.assertIn("[1]", prompt)
        self.assertIn("Start MPs early.", prompt)

    def test_source_title_is_readable(self):
        self.assertEqual(source_title("cs341_prep_advice.txt"), "CS341 Prep Advice")


if __name__ == "__main__":
    unittest.main()
