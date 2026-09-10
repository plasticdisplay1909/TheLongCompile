# COL106/1101 Practice Quiz — Set A (10 Questions)

This package accompanies `quiz_paper.pdf` (in this folder), which is
the actual question paper — read that first.

## Layout

```
quiz_paper.pdf              <- the question paper (start here)
common/harness.py           <- shared autograder engine (nothing to edit)
q1_campusbank/
q2_postfix_polynomials/
q3_complaint_ledger/
q4_unrolled_list/
q5_er_router/
q6_bounded_buffer/
q7_skyline/
q8_roll_registry/
q9_ouroboros/
q10_orbital_defense/
```

Each `qN_.../` folder contains:

- `student_code.py` — the starter file. This is what you edit. Every
  method you need to implement is a `TODO` + `raise
  NotImplementedError`; fill them in without changing any class name,
  method signature, or the `solve()` I/O driver at the bottom of the
  file.
- `autograder.py` — run it with `python3 autograder.py` from inside
  that question's folder (it needs `../common/harness.py`, so don't
  move it out on its own). It runs your `student_code.py` against a
  mix of visible tests (the same ones printed in the question paper)
  and hidden tests (edge cases, adversarial orderings, and large-scale
  performance stress tests), each as an independent subprocess with a
  wall-clock timeout, and prints a per-test PASS/WA/TLE/RE verdict plus
  a final score out of the total available marks.
- `reference_solution.py` — a complete, working solution. It's here so
  the autograder can compute expected outputs, and so you can check
  your understanding *after* attempting the question yourself — please
  don't open it before you've had a real go, or you're only cheating
  the practice value out of your own practice quiz.

## Running an autograder

```
cd q1_campusbank
python3 autograder.py
```

Sample output shape:

```
==============================================================================
Q1 -- The Multi-Branch CampusBank -- Autograder Report
==============================================================================
  Test  1 [VISIBLE] basic savings + interest    PASS   (+1.5)   0.02s
  Test  2 [VISIBLE] overdraft boundary          PASS   (+1.5)   0.01s
  ...
  Test 11 [HIDDEN]  PERF: large scale performance PASS  (+2.0)   0.49s
------------------------------------------------------------------------------
  TOTAL SCORE: 26.0 / 26.0   (100.0%)
==============================================================================
```

- **WA** — your output didn't match on that test.
- **TLE** — your process didn't finish inside that test's time limit.
  This is almost always a complexity problem (see the question's
  "Requested files" section for what the hidden performance tests are
  specifically designed to catch), not a slow machine.
- **RE** — your program raised an uncaught exception or otherwise
  crashed; the last few lines of its stderr are shown.

## Notes

- Everything runs with the `python3` on your `PATH`. No third-party
  packages are required anywhere in this pack.
- `reference_solution.py` is a *correct* solution but is not
  necessarily written the way you're expected to write yours (e.g. some
  reference solutions favour clarity over the exact micro-optimisation
  a hidden performance test is probing for) — matching its output is
  what's graded, not matching its code.
