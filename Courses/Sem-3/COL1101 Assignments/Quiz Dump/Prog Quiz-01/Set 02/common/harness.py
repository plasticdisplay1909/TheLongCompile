"""
COL106/1101 Practice Quiz -- shared autograder harness.

Every question's autograder.py imports this module. It is responsible for:
  - running the student's student_code.py as a fresh subprocess against a
    given stdin string,
  - catching three distinct failure modes: Wrong Answer (WA), Time Limit
    Exceeded (TLE), and Runtime Error (RE),
  - scoring a list of weighted test cases and printing an exam-style report.

Nothing here needs to be edited by the student.
"""

import subprocess
import sys
import time
import os

PYTHON = sys.executable or "python3"


class TestCase:
    def __init__(self, name, stdin_text, expected_output, weight=1, hidden=False, timeout=5.0):
        self.name = name
        self.stdin_text = stdin_text
        self.expected_output = expected_output
        self.weight = weight
        self.hidden = hidden
        self.timeout = timeout


def _normalize(s):
    # Compare token-stream-ish: strip trailing whitespace per line, drop
    # trailing blank lines, so cosmetic whitespace differences don't fail
    # an otherwise-correct submission.
    lines = [ln.rstrip() for ln in s.strip("\n").splitlines()]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def run_one(student_path, tc):
    start = time.time()
    try:
        result = subprocess.run(
            [PYTHON, student_path],
            input=tc.stdin_text,
            capture_output=True,
            text=True,
            timeout=tc.timeout,
        )
    except subprocess.TimeoutExpired:
        return "TLE", "", time.time() - start
    elapsed = time.time() - start
    if result.returncode != 0:
        err = (result.stderr or "").strip().splitlines()
        tail = " | ".join(err[-3:]) if err else "(no stderr captured)"
        return "RE", tail, elapsed
    return "OK", result.stdout, elapsed


def grade(student_path, cases, title="Autograder Report"):
    if not os.path.isfile(student_path):
        print(f"FATAL: cannot find {student_path}")
        sys.exit(1)

    total_weight = sum(tc.weight for tc in cases)
    score = 0.0
    rows = []
    for i, tc in enumerate(cases, 1):
        status, output, elapsed = run_one(student_path, tc)
        label = f"[HIDDEN]" if tc.hidden else f"[VISIBLE]"
        if status == "OK":
            if _normalize(output) == _normalize(tc.expected_output):
                score += tc.weight
                verdict = f"PASS   (+{tc.weight:.1f})  {elapsed:5.2f}s"
            else:
                verdict = f"WA     (+0.0)          {elapsed:5.2f}s"
        elif status == "TLE":
            verdict = f"TLE    (+0.0)          >{tc.timeout:.1f}s"
        else:  # RE
            verdict = f"RE     (+0.0)          {elapsed:5.2f}s  :: {output[:120]}"
        rows.append(f"  Test {i:>2} {label:9s} {tc.name:<28s} {verdict}")

    print("=" * 78)
    print(title)
    print("=" * 78)
    for r in rows:
        print(r)
    print("-" * 78)
    pct = 100.0 * score / total_weight if total_weight else 0.0
    print(f"  TOTAL SCORE: {score:.1f} / {total_weight:.1f}   ({pct:.1f}%)")
    print("=" * 78)
    return score, total_weight
