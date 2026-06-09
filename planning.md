# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

I chose reddit because it's probably the place I look to the most for any UIUC related inquiries, advice, course struggles, school news, etc. r/UIUC is a verry active subreddit. Since I'm a CS major, I centered on CS related inquiries. Here students are a lot more honest, they're speaking to one another and a few helpful professors, they use a bit more coloquil language, and overall I feel use a bit more cerative and unique in their endeavors to finish the degree, career prospects, and unique issues. Official college website is a lot more structure and impersonal. 

Questions it should handle:
1. How hard is it to get an A in CS 225?
2. What CS electives are the easiest or most fun?
3. What do UIUC CS seniors wish they knew as freshmen?
4. Is CS 374 too hard to take as a sophomore?
5. How does CS 341 compare to other hard CS courses?
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/UIUC | Ease of getting an A in CS 225 — grading and curve discussion | https://www.reddit.com/r/UIUC/comments/9g5mpi/ease_of_getting_an_a_in_cs_225/ |
| 2 | r/UIUC | Does CS 225 get harder over time — workload progression and pacing | https://www.reddit.com/r/UIUC/comments/ifqkgt/does_cs_225_get_harder_as_time_progressestoward/ |
| 3 | r/UIUC | Alumni reflect on the most useful CS courses at UIUC | https://www.reddit.com/r/UIUC/comments/176n8tq/to_cs_alumni_what_are_some_of_the_most_useful_cs/ |
| 4 | r/UIUC | Senior CS student reflections — advice and lessons learned | https://www.reddit.com/r/UIUC/comments/1cs5ull/reflections_from_a_senior_in_cs/ |
| 5 | r/UIUC | CS major do-nots — mistakes freshmen should avoid | https://www.reddit.com/r/UIUC/comments/1lyc4vx/cs_major_do_nots_that_i_wish_i_knew_as_a_freshman/ |
| 6 | r/UIUC | Easy and fun CS electives — community recommendations | https://www.reddit.com/r/UIUC/comments/jygo4g/easyfun_cs_electives/ |
| 7 | r/UIUC | Taking CS 374 as an incoming sophomore — readiness and difficulty | https://www.reddit.com/r/UIUC/comments/1kwxfy7/taking_cs_374_as_an_incoming_sophomore/ |
| 8 | r/UIUC | CS 421 student performance discussion — grade and curve data | https://www.reddit.com/r/UIUC/comments/1h8yomn/cs421_students_are_performing_better_currently/ |
| 9 | r/UIUC | CS course difficulty tier list — community rankings of all CS courses | https://www.reddit.com/r/UIUC/comments/10w3far/cs_course_difficulty_tier_list/ |
| 10 | r/UIUC | CS 440–447 elective comparison — which upper-level course is most worth it | https://www.reddit.com/r/UIUC/comments/141b2lk/out_of_all_of_the_cs_courses_between_440447_which/ |
| 11 | r/UIUC | Easy CS electives for finishing a minor — course load advice | https://www.reddit.com/r/UIUC/comments/t92a7m/easy_cs_electives_to_finish_minor/ |
| 12 | r/UIUC | CS 341 prep advice — how to prepare for systems programming | https://www.reddit.com/r/UIUC/comments/1psmiep/cs_341/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
