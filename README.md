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
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

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

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

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
