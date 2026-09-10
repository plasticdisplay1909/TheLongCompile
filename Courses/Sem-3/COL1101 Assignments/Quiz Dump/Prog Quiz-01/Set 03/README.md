# COL106 / COL1101 -- Practice Quiz (Set B)

10 original practice problems modeled on the department's VPL-style
programming quizzes, covering: OOP, functional programming, asymptotic
analysis, arrays/linked lists, ADTs (sets/lists/vectors/sequences),
concurrency, and stacks/queues.

**Start here:** `COL106_Practice_Quiz_Question_Paper.pdf` -- the full
question paper (10 questions, ~1000-1300 words each, in the same format
as the real assignments: story, operations table, worked example,
complexity requirements, requested files).

## Folder structure

Each `Qn_*` folder contains:
- `student_code.py` -- starter code. Helper/bookkeeping methods are
  fully implemented; every graded method is a stub with a detailed
  docstring and `raise NotImplementedError`. Fill these in.
- `autograder.py` -- run with `python3 autograder.py` (no arguments).
  Prints a per-test verdict (AC/WA/RE/TLE) and a final mark out of 100.
  Contains ~15-20 test cases per question: 2 visible (matching the
  sample files), several randomized hidden cases, adversarial hidden
  cases targeting the common wrong shortcut for that problem, and one
  or more large-input performance smoke tests.
- `visible_cases_1.txt` / `visible_cases_2.txt` (+ `_expected.txt`) --
  the two sample cases from the question paper, in the same input
  format your `student_code.py` reads from stdin. Test manually via:
      python3 student_code.py < visible_cases_1.txt
  and compare against `visible_cases_1_expected.txt`.
  (Q7 has no such files -- it's a concurrency problem graded by
  directly importing your class; see its `README.txt`.)

## Difficulty curve

Q1-Q2 (easy-medium) -> Q3-Q5 (medium-hard) -> Q6, Q8 (hard) ->
Q9 (very hard) -> Q10 (hardest: persistent trie + thread safety
combined). Budget ~3 hours per question, exactly like the real quiz.

## A note on grading

The autograders check correctness and catch obviously-wrong asymptotic
complexity via timed performance smoke tests, but (exactly as the real
department assignments warn) passing the autograder does not by itself
prove your solution meets every stated Big-O requirement -- a human
still needs to read the code for that. Don't fake your way past the
timer; the point of each problem is the technique, not the score.
