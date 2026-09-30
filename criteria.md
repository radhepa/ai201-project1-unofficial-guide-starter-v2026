# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** I checked how many documents actually contain each
answer before picking this number, and only one of my five questions
(printing quota, "$30") has its answer in a single document with nothing else
to fall back on. That's the one question where a retrieval miss is
unrecoverable. The other four turned out more redundant than I expected: the
$1.75 laundry price is repeated across four different dorms' documents, "2am"
library hours shows up in eight files (seven dorm noise posts plus the
library-hours post itself), and the Kestrel Commons and CS 210 facts each
appear in two documents about that same place. That redundancy is exactly why
I'm not worried about criterion 1, and it's why I wrote criterion 5 instead,
since a chunk containing the right *number* is not the same as it coming from
the right *building or course*.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** All five, because `generate.py`'s system prompt
explicitly instructs the model to name the file for every answer, and my
questions all produce short, single-fact answers. Following a formatting
instruction on a simple factual response is close to the easiest thing the
model is asked to do here. This isn't code-enforced (nothing in `app.py`
inserts the source line for the model), so it's a real instruction-following
check, not a guaranteed pass. If it slips even once, that's worth knowing
rather than excusing with a looser target.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** I'm writing this before Milestone 4, so I haven't
measured any actual distances yet, and I don't want to justify a number with
data I don't have. My five `OUT_OF_SCOPE` questions (Mongolia's capital, diesel oil
changes, a 1994 World Cup winner, ibuprofen dosage, a Rust for-loop) are about
as far from a university-life corpus as questions get, so I'd hope for 5 of 5.
I'm setting 4 of 5 rather than claiming perfection up front, since "clearly
doesn't cover" is still a judgment call until I've actually seen where the gap
between in-corpus and out-of-corpus distances falls. I'll revisit this once
Milestone 4 gives me real numbers.

---

## 4. Something about your chunks

Of 5 chunks sampled with `python app.py chunks -n 5`, at least 4 read as one
complete post start to finish, with no sentence cut off at either end.

**Why this target:** The documents I read in Milestone 1 are short, 1 to 3
sentences, averaging about 317 characters, and Milestone 1's index run
already chunked all 88 documents into 88 chunks averaging 317 characters
(shortest 178, longest 549), which means the current 800-character chunk size
is producing roughly one chunk per document rather than splitting any of them.
I'm not requiring 5 of 5 because the longest document I saw was 549
characters, comfortably under 800, but I haven't actually read all 88, and
if a longer one exists near the 800-character boundary it could still get cut
mid-sentence. This is the number Milestone 3 is supposed to test directly.

---

## 5. Your choice

When a question names a specific dorm, dining hall, or course, the source the
system names is that specific one, not a same-topic document about a
different building or course, in at least 4 of 5 tries.

**Why this target:** I picked this after noticing, while checking criterion 1,
that several of my "expected" facts aren't unique: the $1.75 wash price is the
same in at least four different dorms' documents, so a question about
Aldridge Hall's laundry could be answered correctly on the *number* by a
chunk about Calder Annexe or Fenwick Court instead. A source being *present*
isn't the same as it being the *right* one, and campus_life's six near-
identical dorm posts and six near-identical course posts make that an easy
mistake to not notice, since a wrong-building answer still reads as
confident and grounded. I picked 4 of 5 rather than 5 of 5 because with a
price shared across several buildings, at least one mix-up between
same-topic, same-number documents feels like the realistic case rather than
the unlucky one.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
