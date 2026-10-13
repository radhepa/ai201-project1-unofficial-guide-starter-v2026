# The Unofficial Guide

**Radhe Patel**, corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The Unofficial Guide answers questions about student life at this university.
It's built on `campus_life`, 88 short posts about dining halls, dorms,
courses, and the administrative rules nobody ever explains properly, the kind
of thing one student writes to answer another's question. Ask it something
specific, like "how much does laundry cost in Aldridge Hall?" or "how many
hours a week does CS 210 take?", and it finds the one post that actually
answers it and names the file it came from, instead of guessing from general
knowledge. Ask it something the corpus doesn't cover, like a diesel engine or
a Rust for loop, and it tells you it doesn't know instead of making something
up.

## Chunking Strategy

**Chunk size:** Not really a fixed number. It's one paragraph per chunk (`chunker.py::split_documents`), with a 600-character ceiling that only kicks in if a single paragraph runs longer than that.
**Overlap:** 80 characters, and that only applies inside the 600-character fallback. Paragraphs at the top level don't overlap at all.

The starter's fixed 800-character chunker reported 88 documents turning into
88 chunks for campus_life back in Milestone 1. It never split anything,
because almost nothing here reaches 800 characters. But once I actually read
through the documents, I noticed every one of them is really a title line
followed by one to four body paragraphs, and those paragraphs are separate
facts, not one thought stretched across sentences. A dining hall post
separates wait times from hours and price. A course post separates format
from workload from a piece of advice. A hall overview post separates what's
good from what's bad from laundry cost from noise rules. Treating a whole
multi-paragraph post as one chunk is the "too big" failure the brief warns
about: it buries each fact under the others in the same vector, so it half
matches every question about that place and fully matches none.

So I split on paragraph breaks instead of a character count. There was one
thing that broke on its own: the title line is always its own paragraph, and
a title like "CS 210 Data Structures" is a fragment, not a sentence. That's
the "too small" failure. So I merge the title into the first body paragraph
instead of letting it stand alone. When I checked paragraph lengths across
the whole corpus, every body paragraph turned out to be a complete sentence
on its own, even a 36-character one ("Expect 4 hours a week outside class.").
So no other merging rule was needed. Nothing here is a fragment except a
bare title.

600 characters comfortably covers the longest body paragraph I measured (373
characters), with room to spare if a longer one shows up later, so the
fallback stays dormant on this corpus for now. Re-running `python app.py
index` after switching confirms it: 183 chunks, 151 characters on average,
shortest 36, longest 397 (a merged title plus paragraph), all produced by
`chunker.py::split_documents`. The 80 characters of overlap only matter
inside that fallback, if a paragraph ever needs to be cut mid-thought. Since
I never actually saw that happen, it's a smaller, fairly arbitrary number I
picked just so the two halves of a forced cut would still share a bit of
context.

I didn't change my mind partway through this one. The title-line problem was
visible before I wrote any code, since every document I read back in
Milestone 1 had the same shape.

## Sample Chunks

**Chunk 1**, source: `admin_add_drop_deadline.txt#0`, produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2**, source: `course_cs_340_exams.txt#1`, produced by: `chunker.py::split_documents`

```
Start the term project in week three, not week eight; everyone learns this the hard way.
```

**Chunk 3**, source: `course_phys_130_workload.txt#0`, produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.
```

**Chunk 4**, source: `dining_verrill_street_grill_followup.txt#1`, produced by: `chunker.py::split_documents`

```
Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.
```

**Chunk 5**, source: `housing_morrow_house.txt#1`, produced by: `chunker.py::split_documents`

```
The good: cheapest housing tier by about $900 a year, and the singles are real singles.
```

## Sample Answer

**Question:** How much does a wash cost in the Aldridge Hall laundry room?

**Answer:**

```
A wash costs $1.75 in the Aldridge Hall laundry room.

Source: housing_aldridge_hall.txt (and housing_aldridge_hall_laundry.txt)
```

I picked this one on purpose because it's a hard case, not an easy one. The
retrieved context also contained three *other* dorms' laundry posts with
similar-looking prices (Old Brewhouse $1.50, Innisfree $1.75, Calder Annexe
$2.00, see the `--show-prompt` output below), and the model still matched the
right building to the right number instead of grabbing a nearby price.

**My relevance cutoff:** I kept `THRESHOLD = 0.6`, the number the starter
shipped with, but I got there by measuring rather than assuming. I ran my
five test questions and the five `OUT_OF_SCOPE` questions through `python
app.py retrieve` and wrote down the best distance for each one.

| Question | In corpus? | Best distance |
|---|---|---|
| What do students say about wait times at Kestrel Commons during lunch? | Yes | 0.262 |
| How much does a wash cost in the Aldridge Hall laundry room? | Yes | 0.226 |
| How many hours per week outside of class should I expect for CS 210? | Yes | 0.242 |
| What is the campus printing quota per semester? | Yes | 0.337 |
| Until what time is the library open during term? | Yes | 0.248 |
| What is the capital of Mongolia? | No | 0.787 |
| How do I change the oil in a diesel engine? | No | 0.923 |
| Who won the 1994 World Cup? | No | 0.847 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.824 |
| How do I write a for loop in Rust? | No | 0.877 |

The two groups didn't overlap at all. In-corpus questions landed between
0.226 and 0.337, out-of-scope ones between 0.787 and 0.923, a gap of about
0.45 between them, which was wider than I expected. 0.6 sits close to the
middle of that gap (0.263 above the highest in-corpus reading, 0.187 below
the lowest out-of-scope one), so I left it alone. I'd only reconsider this if
a future question landed inside the gap itself, and nothing I've tried so far
has.

I also read the grounding prompt itself (`--show-prompt`) for the two
laundry-cost questions above. campus_life's near-duplicate dorm documents are
exactly the case where a gate pass doesn't guarantee a correct *answer*: the
gate only checks that something relevant came back, not that the model picked
the right one out of several similar options sitting in the same prompt.
Both times, the model matched the named building to its own document
correctly despite three other dorms' similar prices sitting right next to it
in context, so I didn't tighten `GROUNDING_INSTRUCTION`. I didn't have
evidence of drift to justify changing it. This is exactly what criterion 5
exists to keep watching in unit 2, where more repeated runs give it more
chances to slip.

## How I Used AI

**1.** For Milestone 3, I asked Claude to design and write the chunking
function in `chunker.py` for `campus_life`, instead of just picking a
character count myself. Rather than jump straight to paragraph splitting, it
first computed title-length and body-paragraph-length statistics across all
88 documents, and found that every document's title line would end up as its
own short fragment chunk if it split naively on blank lines. I had it add a
merge step so the title always joins the first body paragraph instead of
standing alone, and set `CHUNK_SIZE` and `CHUNK_OVERLAP` in `config.py` to
only matter as a fallback for an oversized paragraph, not as the real
chunk-size decision.

**2.** While writing the "why this target" reasoning for my acceptance
criteria (`criteria.md`), its first draft for criterion 1 claimed the
Aldridge laundry-cost answer lived in only one document. Before I accepted
that, I had it grep the corpus to check its own claim, and it came back
having found that the $1.75 price is actually repeated across four different
dorms' documents, which contradicted what it had just written. I had it
rewrite both criterion 1's reasoning and criterion 5 (source attribution
across near-duplicate dorms) to match what the grep actually showed instead
of leaving the incorrect claim in.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are one complete post | 4 of 5 | 1/5 | 1/5 | 1/5 | MISSED |
| 5. Named dorm/dining hall/course gets the right source | 4 of 5 (revised: 3 of 3) | 3/3 | 3/3 | 3/3 | REVISED, then MET |

Evidence files, all committed in `results/`:

- `run_2026-10-13_0947_before.md`: `python run_eval.py --label before`. All 5
  questions × 3 runs with caching off (15 real model calls), plus the gate pass
  over the 5 `OUT_OF_SCOPE` questions. No `scorer.py`, so I judged each answer
  by reading it.
- `retrieval_check_before.md`: the text of every chunk `store.py::search`
  returned for each question, so criterion 1 is checked against the chunks
  themselves and not against the answer.
- `chunks_sample_before.md`: `python app.py chunks -n 5`, run three times.

How each row was counted:

- **Criteria 1 and 3** depend only on retrieval and the gate, which are
  deterministic (the best distance was identical across all three runs for
  every question), so the same number goes in all three columns.
- **Criterion 4** is also deterministic. `app.py::cmd_chunks` picks every Nth
  chunk with no randomness, and the three runs printed byte-identical output.
- **Criteria 2 and 5** depend on the generated answer, so they're the ones
  that could have moved. They didn't.
- **Criterion 5**: only 3 of my 5 questions name a specific dorm, dining hall
  or course (Kestrel Commons, Aldridge Hall, CS 210). The printing and library
  questions don't, so there is no fifth try to count. That's why the cells
  read 3/3 and not x/5. More on this under Verdicts.

**A note on how the run happened.** On 2026-10-13 Gemini was returning
`503 UNAVAILABLE` ("model is experiencing high demand") on most calls, and
`generate.py` only retries 429s, so `run_eval.py` crashed on its first call
about 15 times in a row. I ran `run_eval.py` unchanged through a small wrapper
(kept outside the repo) that waits and retries a call only when Google answers
503. The prompt, model, top-k, cutoff and code that produce answers were not
touched. The run needed 8 retries.

### Real output (run 1 unless noted)

**Criterion 1, retrieved chunks** (`store.py::search`, from
`results/retrieval_check_before.md`). Printing quota is the only question
with its answer in a single document, and it still came back first:

```
- CONTAINS `admin_printing_quota.txt` (distance 0.337): On the printing quota  Every student gets $30 of printing per semester, which is roughly 600 black-and-white pages. It does not roll over. ...
-          `money_textbooks.txt` (distance 0.556): The campus store price-matches, ...
-          `money_jobs.txt` (distance 0.561): Maximum is 20 hours a week during term. ...
-          `admin_graduation_requirements.txt` (distance 0.591): On the graduation requirements  120 credit hours, ...
-          `money_textbooks.txt` (distance 0.610): Textbooks without paying full price  ...
```

**Criterion 2, answers name a source** (`generate.py::answer_from_chunks`,
called from `run_eval.py::run_once`):

```
Every student gets $30 of printing per semester, which is roughly 600 black-and-white pages (admin_printing_quota.txt).
```

```
A wash costs $1.75 in the Aldridge Hall laundry room (housing_aldridge_hall_laundry.txt and housing_aldridge_hall.txt).
```
(run 2)

**Criterion 3, the gate** (`run_eval.py::check_out_of_scope`, cutoff 0.6):

```
  refused  (best distance 0.787)  What is the capital of Mongolia?
  refused  (best distance 0.923)  How do I change the oil in a diesel engine?
  refused  (best distance 0.847)  Who won the 1994 World Cup?
  refused  (best distance 0.824)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.877)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

**Criterion 4, sampled chunks** (`app.py::cmd_chunks`, chunks from
`chunker.py::split_documents`). 183 chunks total for 88 documents. Only
chunk 1 is a whole post; 3 is a title plus the first of two paragraphs, and
2, 4 and 5 are a single paragraph from the middle or end of a post:

```
Chunk 1  |  source: admin_add_drop_deadline.txt#0
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

Chunk 2  |  source: course_cs_340_exams.txt#1
Start the term project in week three, not week eight; everyone learns this the hard way.

Chunk 3  |  source: course_phys_130_workload.txt#0
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

Chunk 4  |  source: dining_verrill_street_grill_followup.txt#1
Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.

Chunk 5  |  source: housing_morrow_house.txt#1
The good: cheapest housing tier by about $900 a year, and the singles are real singles.
```

**Criterion 5, the right building or course** (`generate.py::answer_from_chunks`).
All three qualifying questions cited the matching document in all three runs:

```
Students say that wait times at Kestrel Commons are 20 to 25 minutes between 12:15 and 1:00, and under 5 minutes before 11:45. 

Source: `dining_kestrel_commons.txt` (supported by `dining_kestrel_commons_followup.txt`).
```

```
You should expect 8 to 10 hours a week outside class for CS 210. 

Source documents: `course_cs_210.txt` and `course_cs_210_workload.txt`
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer, 4 of 5 | **MET** | 5/5 on all three runs. I read the retrieved chunk text for each question (`results/retrieval_check_before.md`), not the answers, and every question had at least one chunk that states the answer for the right place or course. |
| 2 | Every answer names a source, 5 of 5 | **MET** | 15 of 15 answers name at least one `.txt` file, in three different formats (inline brackets, a "Source:" line, a bulleted list). The target was all five on every run and it held on every run. |
| 3 | Gate refuses out-of-corpus questions, 4 of 5 | **MET** | All 5 refused, and not narrowly: the closest off-topic question (Mongolia, 0.787) is 0.187 above the 0.6 cutoff, and the farthest real question (printing, 0.337) is 0.263 below it. |
| 4 | 4 of 5 sampled chunks are one complete post | **MISSED** | 1/5 on all three runs. Only `admin_add_drop_deadline.txt#0` is a whole post. The other four have no sentence cut off, but each is only part of a post, and the criterion says "one complete post start to finish", not just "no cut sentences". |
| 5 | Named dorm/dining hall/course gets the right source, 4 of 5 | **Can't be measured as written, so revised.** Under the revision: **MET** | Only 3 of my 5 questions name a specific dorm, dining hall or course, so there is no fifth try and "4 of 5" has nothing to count. The revision (in `criteria.md`, under the original) fixes what is counted and is stricter, not looser: every named source must be right, on 3 of 3 questions, on every run. Result: 3/3, 3/3, 3/3. |

### The close calls, argued from the other side

I tried to argue the opposite verdict for each one before settling on it.

- **Criterion 1, could it be a MISS?** My first check was a plain text
  search for the expected string, and it counted
  `housing_calder_annexe.txt` as containing "$1.75" for the Aldridge
  question. It does, but as Calder's *dry* price. A text search over-counts,
  so I judged by reading instead. The verdict survives because the
  Aldridge question also retrieved two Aldridge chunks that really do say
  "$1.75 wash". But this shows the criterion is only as good as the person
  reading the chunks.
- **Criterion 2, could it be a MISS?** The library answers name
  `study_library_hours.txt` and also four dorm noise posts. Those posts do say
  "the library is open until 2am", so the citations are accurate, just
  padded. Criterion 2 asks only that a source is named, so MET stands. Citing
  the right one is criterion 5's job.
- **Criterion 4, could it be MET?** The tempting argument is that paragraph
  chunking is *supposed* to split posts, so the criterion is measuring the
  wrong thing. I rejected that. The criterion is perfectly measurable (I can
  look at a chunk and say whether it's a whole post), and rewriting it to "no
  sentence cut off" would turn a 1/5 into a 5/5 without anything changing.
  That is loosening a missed target, which the brief rules out. It stays
  MISSED and gets diagnosed.
- **Criterion 5, am I revising it because it was inconvenient?** No. It
  passed on everything it could measure (3/3). The problem was that the
  denominator didn't exist, plus two ambiguities I couldn't score the same
  way twice: does "tries" mean questions or runs, and when an answer names
  two files, which one counts? The revision answers both and is harder to
  pass than the original.

### Were criteria 1 to 3 set too low?

Probably. Clearing three criteria with no misses on the first try usually
means the bar was safe. Criteria 1 and 3 were met by a wide margin: the
real answers were always in the top 5, and the gate gap is about 0.45 wide.
If I set them again I'd tighten criterion 1 so it looks at *rank*, not just
presence: "for questions that name a place or course, at least 2 of the top
3 chunks are about that place or course". Checked against these same
retrieval results, that would have failed 2 of my 3 named questions:
Kestrel's top 3 were Kestrel, Halden Hall, The Ridgeway Café, and
Aldridge's were Aldridge, Old Brewhouse, Innisfree. Criterion 1 as written
couldn't see that.

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

### Criterion 4 (MISSED, 1/5): stage = chunking

**Mechanism.** `chunker.py::split_documents` splits every post on blank
lines (`re.split(r"\n\s*\n", ...)`), glues the title onto the first
paragraph, and makes every later paragraph its own chunk. A post is only kept
whole if it has exactly one body paragraph. Across the whole corpus that is
16 of 88 posts. The other 72 are split into 2 to 4 chunks each, for 183
chunks total:

| Chunks per post | Posts |
|---|---|
| 1 (kept whole) | 16 |
| 2 | 56 |
| 3 | 9 |
| 4 | 7 |

So only **16 of 183 chunks (9%) are a complete post**. A 5-chunk sample would
be expected to contain about 0.45 whole posts, which means my 1/5 was not bad
luck in the sample. If anything it was slightly lucky. The criterion can't be
met by this chunker on this corpus.

**Why my target was wrong about it.** I wrote criterion 4 in commit
`acf992a`, when the starter's 800-character chunker gave 88 chunks for 88
posts. My "why this target" reasoning rests on that 88-for-88 number. One
commit later (`2e97e2e`, Milestone 3) I replaced the chunker with paragraph
splitting, which is *designed* to break posts apart, and never went back to
check criterion 4 against it. That's not a measurement problem with the
criterion (it's still easy to check), so I'm leaving it as a miss. The
mistake was changing the chunker without re-reading the criterion that
depended on it.

### The pattern: split-off paragraphs lose their subject

Breaking posts apart costs more than criterion 4. **95 of 183 chunks (52%)
don't include the title line**, and the title is usually the only place a
post names its dorm, dining hall or course. The clearest case is that all
seven dorm overview posts end with a laundry paragraph in the same template,
and each one becomes a chunk that never says which building it's about:

```
housing_aldridge_hall.txt#3  | Laundry costs $1.75 wash, $1.50 dry, card only. On noise: quiet floors ...
housing_calder_annexe.txt#3  | Laundry costs $2.00 wash, $1.75 dry, app-based. On noise: depends enti...
housing_innisfree_hall.txt#3 | Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; th...
housing_old_brewhouse.txt#3  | Laundry costs $1.50 wash, $1.50 dry, coin only, and the machines are o...
```

To the embedding model these are nearly the same sentence, so retrieval
can't tell the buildings apart. It shows up in my "passed" results:

- **Aldridge laundry question:** `housing_old_brewhouse.txt` (0.320) ranked
  *above* Aldridge's own overview chunk (0.360), and Innisfree and Calder
  Annexe were retrieved too. Three of the five retrieved chunks are about
  the wrong building.
- **Kestrel Commons wait-time question:** the original Kestrel post ranked
  5th (0.446), behind follow-up posts about Halden Hall, The Ridgeway Café and
  North Kitchen. Those are the same "wait figure" template with a different
  name, and they outranked it.

**So why did criterion 5 still pass?** Not because of retrieval. In
`generate.py` (line 295) every chunk reaches the model labelled
`[from <filename>]`, and the filename carries the building name the chunk
text lost. The model picked the Aldridge chunk by reading
`housing_aldridge_hall.txt`, not by reading the text. Criterion 5 passed
because of the generation stage covering for the chunking stage. If my file
names were `doc_017.txt`, I'd expect criterion 5 to fail.

This is one problem showing up twice, not two problems. Criterion 4's miss
and criterion 5's lucky pass have the same cause: chunks that don't carry
their post's subject.

### Everything else

Criteria 1, 2 and 3 had no misses. As I wrote under Verdicts, that's partly
because the targets were safe. The pattern above is why I'd tighten
criterion 1 to look at rank (at least 2 of the top 3 chunks about the named
place). Under that rule, Kestrel and Aldridge would already fail today.

### What this points the fix at

Both findings point at the chunking stage, so that's where Milestone 4's one
change goes: chunk by whole post instead of by paragraph. Posts are short
(longest 549 characters, under the 600-character ceiling), so every
post would become exactly one chunk with its title included. The risk is the
trade-off I argued in unit 1, that whole posts bury each fact under the
others. Criteria 1 and 5 will show whether that cost is real.

## The Improvement

**What I changed:** One thing, the chunking strategy. `chunker.py::split_documents`
now makes one chunk per whole post instead of one per paragraph. The unit 1
paragraph version is kept as `chunker.py::paragraph_split`, and it's still
used as a fallback for any post over 600 characters, which none of the 88
are (the longest is 549). Re-indexing with `python app.py index` gave 88
chunks for 88 posts, averaging 317 characters. Nothing else changed: same
questions, model, prompt, top-k 5 and cutoff 0.6.

**Why I picked it:** The diagnosis traced criterion 4's miss to paragraph
splitting keeping only 16 of 88 posts whole, and showed the same split was
stripping the title (the building or course name) from 52% of chunks.
Whole-post chunks fix both at the stage where they happen.

**What I expected it to cost:** In unit 1 I chose paragraph chunks because a
whole post "buries each fact under the others". If that was right, the
single-fact questions should match their post *less* closely now.

### Run Log — After

`results/run_2026-10-13_1018_after.md` (`run_eval.py --label after`, same
503-only retry wrapper, which needed 8 retries),
`results/retrieval_check_after.md` and `results/chunks_sample_after.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are one complete post | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Named dorm/dining hall/course gets the right source | 4 of 5 (revised: 3 of 3) | 3/3 | 3/3 | 3/3 | MET (revised) |

**Real output, after (run 1 unless noted):**

Criterion 4 (`app.py::cmd_chunks`), every sampled chunk is now a full post,
title included:

```
Chunk 3  |  source: course_hist_118_workload.txt#0  |  produced by: chunker.py::split_documents
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

Criterion 1 (`store.py::search`), the Aldridge question's top 3. Both
Aldridge chunks now rank 1st and 2nd, and every chunk carries its building
name in the text:

```
1. `housing_aldridge_hall_laundry.txt` (distance 0.233): Laundry in Aldridge Hall  Machines take $1.75 wash, $1.50 dry, card only. ...
2. `housing_aldridge_hall.txt` (distance 0.329): Aldridge Hall — what it's actually like  I lived here my sophomore year. ...
3. `housing_innisfree_hall_laundry.txt` (distance 0.355): Laundry in Innisfree Hall  Machines take $1.75 wash, $1.75 dry, app-based. ...
```

Criteria 2 and 5 (`generate.py::answer_from_chunks`):

```
A wash costs $1.75 in the Aldridge Hall laundry room, as stated in the documents `housing_aldridge_hall_laundry.txt` and `housing_aldridge_hall.txt`.
```

```
For CS 210, you should expect 8 to 10 hours a week outside of class (course_cs_210_workload.txt).
```

Criterion 3 (`run_eval.py::check_out_of_scope`):

```
  refused  (best distance 0.825)  What is the capital of Mongolia?
  refused  (best distance 0.934)  How do I change the oil in a diesel engine?
  refused  (best distance 0.886)  Who won the 1994 World Cup?
  refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.896)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

### Side by side

| Criterion | Before (3 runs) | After (3 runs) | Change |
|---|---|---|---|
| 1. Answer in retrieved chunks | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 | same |
| 2. Answer names a source | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 | same |
| 3. Gate refuses off-topic | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 | same |
| 4. Chunk is a whole post | 1/5, 1/5, 1/5 (MISSED) | 5/5, 5/5, 5/5 (MET) | **fixed** |
| 5. Right named source (revised) | 3/3, 3/3, 3/3 | 3/3, 3/3, 3/3 | same |

The headline numbers only show criterion 4 moving. The distances underneath
show what the change actually did:

| Measure | Before | After |
|---|---|---|
| Chunks in the index | 183 | 88 |
| Chunks without their title line | 95 (52%) | 0 |
| Best distance: library question | 0.248 | **0.448** (worse) |
| Best distance: CS 210 question | 0.242 | 0.262 (slightly worse) |
| Best distance: Aldridge / Kestrel / printing | 0.226 / 0.262 / 0.337 | 0.233 / 0.259 / 0.337 (about the same) |
| Rank of `study_library_hours.txt` for the library question | 1st | **2nd**, behind `admin_library_holds.txt` |
| Wrong-building chunks in Aldridge's top 3 | 2 | 1 |
| Gap from worst real question to the cutoff (0.6) | 0.263 | **0.152** |
| Gap from best off-topic question to the cutoff | 0.187 | 0.225 |
| Input tokens for 15 answers | 6,177 | 9,027 (+46%) |

**Did it help?**

Yes for what it was aimed at, with a real cost I can measure. Criterion 4
went from 1/5 to 5/5 on all three runs, and the subject-loss problem is gone:
no chunk is missing its title now, and the Aldridge question's top two
results are both Aldridge. Nothing that passed before started failing.

But my unit 1 worry was partly right. The library question's best distance
went from 0.248 to 0.448 because "open until 2am" is now one line inside a
longer post about where to sit, and the right post dropped to 2nd behind a
post about library *holds*. The answer still came out right on every run,
because the correct post was still in the top 5. The safety margin under the
gate shrank, though: the worst real question now sits 0.152 below the
cutoff instead of 0.263. A longer post with one key fact could plausibly end
up on the wrong side of 0.6, and the gate would refuse a question the corpus
can answer. Bigger chunks also mean 46% more input tokens per answer.

So the change fixed the criterion it targeted and the retrieval problem
behind it, and paid for it in how sharply single facts inside longer posts
can be matched. I can tell because the per-question distances moved, not
just the pass counts.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
