# COL106 / COL1101 Practice Quiz Set (10 Problems)

## Personal Suggestion
1. Copy the student code and do it in Moodle VPL (Don't use VS code for coding)
2. Try to solve each questions in 1 hour as we don't know what would be the number of questions during the lab quiz
3. To test your cases, open VS code and do the following commands one by one. Like for each question copy the original folder name. Do not change any file names
     - ```cd Q1_OOP_FleetConsole```
     - ```python grader.py```


#### This has been made entirely using Claude Sonnet 5 Medium

This archive contains 10 original practice problems in the style of the
course's CSE Moodle VPL lab assignments, covering: OOP, functional
programming, asymptotic analysis / divide-and-conquer, arrays, linked
lists, Set/Queue/Sequence ADTs, concurrency, and stacks/queues and
their applications.

## Contents
- `question_paper.pdf`
- `Q1_OOP_FleetConsole/` ... `Q10_LRU_Cache/` -- one folder per problem,
  each containing:
  - `student_code.py` -- the starter file. Fill in every function/method
    marked `TODO`, keeping all given names/signatures and the I/O
    driver at the bottom exactly as provided.
  - `visible_cases/` -- 2 sample input/expected-output pairs per
    problem, for your own debugging (ungraded).
  - `hidden_tests.json` -- 20 additional test cases used only by
    `grader.py` (includes correctness edge cases AND large-scale
    performance tests designed to time out non-optimal solutions).
  - `grader.py` -- run this (`python3 grader.py`) from inside the
    problem folder once you've written your solution. It reports
    AC / WA / TLE / RE per test case and a final score.

## Suggested workflow

1. Open `question_paper.pdf` and pick a problem (they're ordered
   easiest -> hardest).
2. Read the full problem description before touching the code --
   several exact-format and exact-policy details (output formatting,
   resize thresholds, tie-breaking rules, etc.) are load-bearing for
   the grader.
3. Implement in `student_code.py`.
4. Test against `visible_cases/` by hand, or just run `grader.py`
   directly -- it grades the visible cases too (for free, ungraded)
   and shows a full diff if you get one wrong.
5. Budget about two hours per problem if attempting under quiz
   conditions -- the later problems (7-10) are intentionally long and
   have tight performance requirements.

Good luck.


