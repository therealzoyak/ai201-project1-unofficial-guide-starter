# The Unofficial Guide — Project 1
Demo video: https://www.loom.com/share/67dec7fa2c8f4bd69c7296d3e5704db0
---

## Domain

This system covers student discussions about CS courses at UIUC, sourced from 
r/UIUC. It captures honest, peer-to-peer takes on course difficulty, grading 
policies, professor recommendations, and elective choices for CS majors and minors.

This knowledge is valuable because official course descriptions and the course 
explorer don't reflect what a class is actually like, such as how hard the curve is, 
whether MPs are manageable, or which electives are worth your time. This kind 
of information usually only gets passed down through older students, RSOs, or 
word of mouth, which means newer students or those without those connections 
miss out on it. r/UIUC threads capture these conversations, but they're scattered 
across years of posts with no way to search across them for a specific question.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/9g5mpi/ease_of_getting_an_a_in_cs_225/ |
| 2 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/ifqkgt/does_cs_225_get_harder_as_time_progressestoward/ |
| 3 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/176n8tq/to_cs_alumni_what_are_some_of_the_most_useful_cs/ |
| 4 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/1cs5ull/reflections_from_a_senior_in_cs/ |
| 5 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/1lyc4vx/cs_major_do_nots_that_i_wish_i_knew_as_a_freshman/ |
| 6 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/jygo4g/easyfun_cs_electives/ |
| 7 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/1kwxfy7/taking_cs_374_as_an_incoming_sophomore/ |
| 8 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/1h8yomn/cs421_students_are_performing_better_currently/ |
| 9 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/10w3far/cs_course_difficulty_tier_list/ |
| 10 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/141b2lk/out_of_all_of_the_cs_courses_between_440447_which/ |
| 11 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/t92a7m/easy_cs_electives_to_finish_minor/ |
| 12 | r/UIUC | Reddit thread | https://www.reddit.com/r/UIUC/comments/1psmiep/cs_341/ |

---

## Chunking Strategy

**Chunk size:** 1500 characters (roughly 300-375 tokens)

**Overlap:** 200 characters (roughly 50 tokens)

**Why these choices fit your documents:** My documents are short Reddit 
threads — the longest is under 5,000 characters. 1500 characters is enough 
to grab one full comment plus some context without smashing multiple unrelated 
comments together. Before chunking I manually cleaned each thread, stripping 
out Reddit's sidebar, vote counts, "Archived post" notices, and avatar/flair 
clutter, keeping just the post and comments labeled [Post]/[Comment]. The 
200 char overlap helps avoid cutting a sentence in half at a chunk boundary.

**Final chunk count:** 23 chunks across 12 documents. That's under the 
50-chunk guideline, but it's accurate — each thread only had a few real 
comments left after cleaning.

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers, with 
normalize_embeddings=True and cosine similarity in ChromaDB.

**Production tradeoff reflection:** If cost wasn't an issue I'd look at 
something like OpenAI's text-embedding-3-large — it'd probably handle 
UIUC-specific terms like "MPs" or course numbers better since all-MiniLM 
is pretty general purpose. The tradeoff is cost and latency from an API 
call vs. running locally for free. For this project all-MiniLM was the 
right call, but for something with real traffic the accuracy bump might 
be worth it.

---

## Grounded Generation

**System prompt grounding instruction:** [paste your actual system prompt 
from query.py here]

**How source attribution is surfaced in the response:** Sources are added 
programmatically, not by the LLM. After retrieval, I pull the source filename 
from each chunk's metadata, dedupe them, and return that list alongside the 
answer. So the sources shown are always exactly what was retrieved, no risk 
of the model making up a citation.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How hard is it to get an A in CS 225? | Students say it's possible but requires consistent MP effort; the curve helps | Says it's relatively easy to get an A, citing students who got full MP points with extra credit and a large portion of the class getting As | Relevant | Accurate |
| 2 | What CS electives do students consider easiest? | Commonly mentioned: CS 400-level courses with project-based grading | Lists CS 361, 374, 418 (with Shaffer), 464 (Cyber Dystopia), 412 (Data Mining), and mentions 440/448 as approachable | Relevant | Accurate |
| 3 | What do UIUC CS seniors most regret not doing earlier? | Not doing side projects or internships early enough | "I don't have enough information on that." | Partially relevant | Inaccurate (false negative) |
| 4 | Should an incoming sophomore take CS 374? | Most say wait unless you're strong in discrete math and proofs | Says it depends on math/theory background, citing faculty and the CS 374 instructor; if background is strong, okay to take it | Relevant | Accurate |
| 5 | How should you prepare for CS 341? | Start early on MPs, get comfortable with C and systems concepts beforehand | Recommends reading the course textbook and OSTEP, starting assignments early, attending class, and developing debugging skills | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** What do UIUC CS seniors most regret not doing earlier?

**What the system returned:** "I don't have enough information on that," even 
though `reflections_from_a_senior_in_cs.txt` was retrieved and is the single 
most relevant document in the entire corpus for this question — it directly 
contains a senior's list of things they wish they'd done differently 
(do research, network with professors, don't compare yourself to others, go 
out more).

**Root cause (tied to a specific pipeline stage):** This is a generation-stage 
failure, not a retrieval failure. Retrieval correctly surfaced the right document. 
The problem is that the source content is phrased as advice/recommendations 
("figure out your goal," "do research," "go out more") rather than as 
explicit statements of regret ("I wish I had done X earlier"). My grounding 
instruction is strict — answer only from the retrieved context — but the LLM 
appears to have interpreted "regret" too literally and didn't connect the 
advice-style phrasing to the question, even though the underlying content 
(e.g., "I graduated with a very high GPA but didn't apply to a single masters 
program because I had no connections") is functionally a regret.

**What you would change to fix it:** I'd loosen the grounding instruction 
slightly to allow the model to make reasonable inferences from related phrasing 
in the context, rather than requiring a near-literal keyword match between the 
question and the source text. Alternatively, I could rephrase chunks during 
ingestion to make implicit regrets more explicit (e.g., prefixing list items 
in this document with "[Regret/Advice]" tags), which would make the semantic 
connection clearer for both retrieval and generation.

---

## Spec Reflection

**One way the spec helped you during implementation:** The Chunking Strategy 
section in planning.md gave me a concrete starting point (300 tokens, 50 
overlap) that I could test and adjust rather than guessing blindly. When my 
first attempt produced only 23 chunks, having a documented target in 
planning.md made it clear something was off, and having already reasoned 
through *why* 300 tokens made sense for Reddit comments helped me quickly 
identify that the issue was a token/character mismatch rather than a flawed 
strategy.

**One way your implementation diverged from the spec, and why:** My planning.md 
originally assumed I'd be scraping Reddit via its JSON API, but Reddit blocked 
all automated requests with a 403 error. I diverged by manually copying and 
cleaning 12 threads into local .txt files instead, which the milestone 
explicitly anticipates as a fallback. This also affected my final chunk count — 
I expected closer to 50+ chunks, but ended up with 23 because manually copied 
threads were naturally shorter than I estimated. I documented this divergence 
in planning.md rather than forcing artificial chunk sizes to hit an arbitrary 
number.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md 
  (chunk_size=300 tokens, chunk_overlap=50) plus my ingestion code.
- *What it produced:* A chunker using LangChain's RecursiveCharacterTextSplitter 
  with `from_tiktoken_encoder`. This gave me only 33 chunks, which felt too low.
- *What I changed or overrode:* Turns out "300 tokens" wasn't behaving the way 
  I expected, so I had Claude switch it to character-based chunking instead 
  (1500 chars / 200 char overlap) and updated planning.md to match.

**Instance 2**

- *What I gave the AI:* My retrieval test results — distance scores were 
  sitting between 0.6 and 1.0, which is above the 0.5 threshold the milestone 
  says indicates weak matches.
- *What it produced:* Claude figured out ChromaDB was probably defaulting to 
  L2 distance and suggested switching to cosine similarity with normalized 
  embeddings.
- *What I changed or overrode:* I didn't change the fix itself, but I made 
  sure to re-run all 3 test queries myself afterward to confirm it actually 
  helped — scores dropped to 0.30–0.45 and the results were noticeably more 
  relevant.
