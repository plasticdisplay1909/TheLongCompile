Q7 -- The Overnight Bakery: how this one is graded differently
================================================================

Every other problem in this set is graded by feeding your program a
script of operations on stdin and comparing stdout to an exact expected
string. That does not make sense here: correctness for a concurrent
bounded buffer is about invariants that must hold under EVERY possible
thread interleaving, not about one fixed sequence of commands producing
one fixed output.

So `autograder.py` in this folder does NOT read `visible_cases_*.txt`
files at all (there are none). Instead it directly imports your
`BoundedBuffer` class from `student_code.py` and runs several small,
self-checking multithreaded programs against it -- each one spins up
producer/consumer threads, exercises `put`/`get`, and asserts an
invariant (e.g. "put() on a full buffer must not return until a slot
frees up", "every item produced is consumed exactly once, with no
losses and no duplicates"). A genuine deadlock in your implementation
shows up as a timeout (TLE); a broken invariant shows up as an
assertion failure (WA); any exception is a runtime error (RE).

To test locally while you are developing, just run:

    python3 autograder.py

directly -- there is nothing to pipe into it.
