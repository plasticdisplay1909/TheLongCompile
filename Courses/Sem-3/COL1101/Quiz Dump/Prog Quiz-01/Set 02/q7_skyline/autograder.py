import os
import sys
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import harness  # noqa: E402

REF = os.path.join(HERE, "reference_solution.py")
STUDENT = os.path.join(HERE, "student_code.py")


def make_input(cmds):
    return f"{len(cmds)}\n" + "\n".join(cmds) + "\n"


def expected_of(stdin_text, timeout=30):
    result = subprocess.run(
        [sys.executable, REF], input=stdin_text, capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError("reference_solution.py crashed:\n" + result.stderr)
    return result.stdout


def build_cases():
    cases = []

    # ---------- VISIBLE ----------
    cmds = ["APPEND 2", "APPEND 1", "APPEND 5", "APPEND 6", "APPEND 2", "APPEND 3",
            "SPAN 0", "SPAN 1", "SPAN 2", "SPAN 3", "SPAN 4", "SPAN 5", "MAXRECT", "NEXTGREATER 2"]
    cases.append(harness.TestCase("classic worked example", make_input(cmds), None, weight=2.5))

    cmds = ["APPEND 3", "APPEND 1", "APPEND 4", "APPEND 1", "APPEND 5",
            "REMOVE_LAST", "SPAN 3", "MAXRECT", "NEXTGREATER 1"]
    cases.append(harness.TestCase("remove_last rebuild", make_input(cmds), None, weight=2.5))

    cmds = ["APPEND 5", "APPEND 5", "APPEND 5", "SPAN 0", "SPAN 1", "SPAN 2", "NEXTGREATER 0", "NEXTGREATER 1", "MAXRECT"]
    cases.append(harness.TestCase("equal heights (ties)", make_input(cmds), None, weight=2.0))

    cmds = ["APPEND 4", "MAXRECT", "SPAN 0", "NEXTGREATER 0"]
    cases.append(harness.TestCase("single building", make_input(cmds), None, weight=1.5))

    # ---------- HIDDEN ----------
    cmds = ["APPEND 6", "APPEND 5", "APPEND 4", "APPEND 3", "APPEND 2", "APPEND 1",
            "SPAN 5", "MAXRECT", "NEXTGREATER 0"]
    cases.append(harness.TestCase("strictly decreasing histogram", make_input(cmds), None, weight=2.0, hidden=True))

    cmds = ["APPEND 1", "APPEND 2", "APPEND 3", "APPEND 4", "APPEND 5",
            "SPAN 4", "MAXRECT", "NEXTGREATER 4"]
    cases.append(harness.TestCase("strictly increasing histogram", make_input(cmds), None, weight=2.0, hidden=True))

    cmds = ["APPEND 0", "APPEND 0", "APPEND 0", "MAXRECT", "SPAN 2"]
    cases.append(harness.TestCase("all-zero heights", make_input(cmds), None, weight=1.5, hidden=True))

    cmds = ["APPEND 2", "APPEND 4", "APPEND 6", "REMOVE_LAST", "REMOVE_LAST", "APPEND 9",
            "SPAN 1", "MAXRECT"]
    cases.append(harness.TestCase("multiple undos then rebuild", make_input(cmds), None, weight=2.5, hidden=True))

    rng = random.Random(17)
    cmds = []
    n = 0
    for _ in range(300):
        op = rng.choice(["APPEND", "APPEND", "APPEND", "REMOVE_LAST", "SPAN", "NEXTGREATER", "MAXRECT"])
        if op == "APPEND":
            cmds.append(f"APPEND {rng.randint(0,20)}")
            n += 1
        elif op == "REMOVE_LAST" and n > 0:
            cmds.append("REMOVE_LAST")
            n -= 1
        elif op == "SPAN" and n > 0:
            cmds.append(f"SPAN {rng.randint(0,n-1)}")
        elif op == "NEXTGREATER" and n > 0:
            cmds.append(f"NEXTGREATER {rng.randint(0,n-1)}")
        elif op == "MAXRECT":
            cmds.append("MAXRECT")
    cases.append(harness.TestCase("randomized 300-op scenario", make_input(cmds), None, weight=3.5, hidden=True))

    # ---------- PERFORMANCE / TLE TRAPS ----------
    # 40000 appends interleaved with SPAN queries -- an O(n) rescan per
    # APPEND (instead of the required O(1) amortised incremental update)
    # makes this O(n^2).
    rng2 = random.Random(23)
    cmds = []
    for i in range(40000):
        cmds.append(f"APPEND {rng2.randint(0, 10**6)}")
        if i % 500 == 0:
            cmds.append(f"SPAN {i}")
    cases.append(harness.TestCase("PERF: 40000 appends (amortised O(1) required)", make_input(cmds), None,
                                   weight=4.0, hidden=True, timeout=5.0))

    # a smaller number of buildings but many MAXRECT/NEXTGREATER queries,
    # each individually allowed to be O(n) -- this bounds total work at
    # O(n * queries), which should still comfortably finish; it exists to
    # confirm your from-scratch scans are not accidentally O(n^2) THEMSELVES
    # (e.g. an O(n^2) largest-rectangle instead of the O(n) monotonic-stack
    # version).
    cmds = [f"APPEND {rng2.randint(0,1000)}" for _ in range(6000)]
    for _ in range(400):
        cmds.append("MAXRECT")
    cases.append(harness.TestCase("PERF: 6000 buildings, 400 MAXRECT queries", make_input(cmds), None,
                                   weight=3.5, hidden=True, timeout=5.0))

    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q7 -- Skyline Renovation -- Autograder Report")
