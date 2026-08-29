#!/usr/bin/env python3
"""
Generic autograder driver.

Usage:
    python3 grader.py

It expects, in the SAME directory as this script:
    - student_code.py        (the file you write your solution in)
    - hidden_tests.json      (hidden test cases -- do not open, do not edit)
    - visible_cases/         (folder with *_input.txt / *_expected.txt pairs
                               you can look at and test against yourself)

For each test case it:
    1. Runs `python3 student_code.py` in a fresh subprocess, feeding the
       test's input on stdin.
    2. Enforces a per-test wall-clock timeout -> classified as TLE.
    3. Captures a non-zero exit code / traceback on stderr -> classified as RE.
    4. Compares stdout (whitespace-normalised per line) against the expected
       output -> AC (correct) or WA (wrong answer).

It then prints a per-test verdict table and a final score out of the total
marks available, exactly the way the real VPL-based Moodle grader on the
course would.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(HERE, "student_code.py")
HIDDEN_FILE = os.path.join(HERE, "hidden_tests.json")
VISIBLE_DIR = os.path.join(HERE, "visible_cases")


def normalize(s):
    lines = [ln.rstrip() for ln in s.strip("\n").splitlines()]
    return "\n".join(lines).strip()


def run_one(input_text, timeout):
    try:
        start = time.time()
        proc = subprocess.run(
            [sys.executable, STUDENT_FILE],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start
        if proc.returncode != 0:
            return "RE", proc.stdout, proc.stderr, elapsed
        return "OK", proc.stdout, proc.stderr, elapsed
    except subprocess.TimeoutExpired as e:
        return "TLE", (e.stdout or ""), (e.stderr or ""), timeout


def load_visible_cases():
    cases = []
    if not os.path.isdir(VISIBLE_DIR):
        return cases
    inputs = sorted(f for f in os.listdir(VISIBLE_DIR) if f.endswith("_input.txt"))
    for inp in inputs:
        base = inp[: -len("_input.txt")]
        exp_path = os.path.join(VISIBLE_DIR, base + "_expected.txt")
        inp_path = os.path.join(VISIBLE_DIR, inp)
        if not os.path.exists(exp_path):
            continue
        with open(inp_path) as f:
            input_text = f.read()
        with open(exp_path) as f:
            expected = f.read()
        cases.append({
            "name": f"visible:{base}",
            "input": input_text,
            "expected": expected,
            "marks": 0,          # visible cases are ungraded, for your own debugging
            "timeout": 5,
            "visible": True,
        })
    return cases


def load_hidden_cases():
    if not os.path.exists(HIDDEN_FILE):
        return []
    with open(HIDDEN_FILE) as f:
        data = json.load(f)
    out = []
    for t in data:
        t = dict(t)
        t["visible"] = False
        out.append(t)
    return out


def main():
    if not os.path.exists(STUDENT_FILE):
        print("ERROR: student_code.py not found next to grader.py")
        sys.exit(1)

    cases = load_visible_cases() + load_hidden_cases()
    if not cases:
        print("No test cases found.")
        sys.exit(1)

    total_marks = sum(c.get("marks", 0) for c in cases)
    scored = 0.0
    print("=" * 72)
    print(f"Grading {STUDENT_FILE}")
    print("=" * 72)

    for i, case in enumerate(cases, 1):
        timeout = case.get("timeout", 5)
        verdict, out, err, elapsed = run_one(case["input"], timeout)
        label = case["name"]
        marks = case.get("marks", 0)

        if verdict == "TLE":
            result = "TLE"
        elif verdict == "RE":
            result = "RE"
        else:
            if normalize(out) == normalize(case["expected"]):
                result = "AC"
                scored += marks
            else:
                result = "WA"

        tag = "[VISIBLE]" if case.get("visible") else "[HIDDEN] "
        time_str = f"{elapsed:5.2f}s"
        mark_str = f"+{marks}" if marks else "  -"
        print(f"{tag} Test {i:2d} ({label:<28s}) : {result:4s}  time={time_str}  marks={mark_str}")

        if case.get("visible") and result != "AC":
            print("    ---- your stdout ----")
            print("    " + normalize(out).replace("\n", "\n    "))
            print("    ---- expected ----")
            print("    " + normalize(case["expected"]).replace("\n", "\n    "))
            if err.strip():
                print("    ---- stderr (last 20 lines) ----")
                print("    " + "\n    ".join(err.strip().splitlines()[-20:]))

        if (not case.get("visible")) and result in ("RE",) and err.strip():
            # Give a small hint for hidden RE cases without revealing the test data.
            last_line = err.strip().splitlines()[-1]
            print(f"    (hint: your program raised: {last_line})")

    print("=" * 72)
    print(f"SCORE: {scored:.1f} / {total_marks:.1f}")
    print("=" * 72)


if __name__ == "__main__":
    main()
