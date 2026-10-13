# Console output of the before run (run_eval.py via the 503-only retry wrapper)

Includes the model-call/token count printed by generate.usage() and the wrapper's 503 retry lines.

```
  [503] Gemini busy, retry 1 in 10s
  [503] Gemini busy, retry 1 in 10s
  [503] Gemini busy, retry 1 in 10s
  [503] Gemini busy, retry 1 in 10s
  [503] Gemini busy, retry 1 in 10s
  [503] Gemini busy, retry 1 in 10s
  [503] Gemini busy, retry 2 in 20s
  [503] Gemini busy, retry 1 in 10s

503 retries needed this run: 8
No scorer.py found — running unscored. Verdict column will be blank.
You'll build scorer.py in class in unit 2.


What do students say about wait times at Kestrel Commons during lunch?
  run 1: —  (best distance 0.262)
  run 2: —  (best distance 0.262)
  run 3: —  (best distance 0.262)

How much does a wash cost in the Aldridge Hall laundry room?
  run 1: —  (best distance 0.226)
  run 2: —  (best distance 0.226)
  run 3: —  (best distance 0.226)

How many hours per week outside of class should I expect for CS 210?
  run 1: —  (best distance 0.242)
  run 2: —  (best distance 0.242)
  run 3: —  (best distance 0.242)

What is the campus printing quota per semester?
  run 1: —  (best distance 0.337)
  run 2: —  (best distance 0.337)
  run 3: —  (best distance 0.337)

Until what time is the library open during term?
  run 1: —  (best distance 0.248)
  run 2: —  (best distance 0.248)
  run 3: —  (best distance 0.248)

Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.787)  What is the capital of Mongolia?
  refused  (best distance 0.923)  How do I change the oil in a diesel engine?
  refused  (best distance 0.847)  Who won the 1994 World Cup?
  refused  (best distance 0.824)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.877)  How do I write a for loop in Rust?
  -> gate refused 5 of 5

Wrote results\run_2026-10-13_0947_before.md
15 model calls this session, 7026 tokens (6177 in, 849 out)

Commit this file. It's the evidence the run actually happened.

[exited with code 0]
```

## Earlier plain run_eval.py attempts that crashed on 503 (retry loop log)

Before the loop: 1 manual run + 3 retries, all crashed with 503 UNAVAILABLE on the first model call. Then:

```
attempt 1 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 2 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 3 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 4 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 5 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 6 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 7 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 8 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 9 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503
attempt 10 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 50
attempt 11 failed: google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 50

[killed]
```
