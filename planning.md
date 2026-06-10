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

     

**Chunk size:** 300 tokens

**Overlap:** 50 tokens

**Reasoning:**  Reddit comments are by design short opinion pieces. 300 tokens 
is large enough to capture a full comment plus context, but small enough 
that each chunk stays focused on one person's take. Overlap of 50 tokens 
prevents a key sentence from being cut off at a boundary mid-thought. So we are able to account for people with slightly longer and shorter thoughts.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 5

**Production tradeoff reflection:** In production I'd consider OpenAI's 
text-embedding-3-large for better accuracy on domain-specific terms like 
"MPs", "curve", or course numbers. The tradeoff is cost per query vs. 
retrieval quality. For a student-facing tool all-MiniLM is much faster since it runs locally.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | How hard is it to get an A in CS 225? | Students say it's possible but requires consistent MP effort; the curve helps |
| 2 | What CS electives do students consider easiest?  | Commonly mentioned: CS 400-level courses with project-based grading |
| 3 | What do UIUC CS seniors most regret not doing earlier?| Not doing side projects or internships early enough|
| 4 | Should an incoming sophomore take CS 374?| Most say wait unless you're strong in discrete math and proofs |
| 5 | How should you prepare for CS 341? | Start early on MPs, get comfortable with C and systems concepts beforehand |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Off topic comment noise: Reddit threads contain off-topic jokes, memes, and 
   one-word replies that add no useful information. These will get embedded 
   and retrieved, polluting results with low-quality chunks.

2. Outdated: Some threads are from 2018-2022. Course difficulty, 
   professors, and grading policies change. The system might retrieve 
   outdated advice confidently without flagging it as old.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     Claude-aided design:

     Document Ingestion     →    Chunking           →    Embedding + Vector Store
(PRAW or saved HTML)       (LangChain           (all-MiniLM-L6-v2 via
                            RecursiveCharacter    sentence-transformers
                            TextSplitter,         + ChromaDB)
                            500 tok / 50 overlap)

        →    Retrieval              →    Generation
             (ChromaDB similarity        (Groq LLM via API,
              search, top-k=5)            prompt = question +
                                          retrieved chunks)

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
Ingestion: I'll give Claude my 12 Reddit URLs and ask it to write a scraper 
that pulls the post title, body, and top comments into a list of strings. 
I'll know it's working if I print the first 3 documents and they contain 
actual comment text.

Chunking: I'll share my chunking strategy with Claude and ask it to implement 
chunk_text() using LangChain's RecursiveCharacterTextSplitter with chunk_size=300 
and chunk_overlap=50. I'll verify by printing the chunk count and spot-checking 
that none are empty or weirdly cut off.

Embedding: I'll give Claude my retrieval approach section and ask it to implement 
embed_and_store() using all-MiniLM-L6-v2 and ChromaDB. To test it I'll run a 
sample question against the database and see if the chunks that come back 
actually relate to what I asked.

Retrieval + Generation: I'll give Claude the full architecture and ask it to 
wire everything into a query() function — question goes in, top-5 chunks get 
retrieved, answer comes out via Groq. I'll run my 5 eval questions through it 
and compare the outputs to my expected answers to see if it's actually working.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
