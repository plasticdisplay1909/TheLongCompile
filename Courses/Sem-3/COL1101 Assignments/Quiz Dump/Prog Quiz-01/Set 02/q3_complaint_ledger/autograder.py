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
    cmds = ["PUSH 5", "PUSH 7", "PUSH 9", "CAPACITY", "PUSH 1", "CAPACITY",
            "POP", "POP", "POP", "CAPACITY", "AVG 2", "SIZE", "GET 0", "SET 0 100", "GET 0"]
    cases.append(harness.TestCase("capacity policy trace", make_input(cmds), None, weight=2.5))

    cmds = ["PUSH 10", "PUSH 20", "PUSH 30", "AVG 3", "AVG 1", "AVG 4", "AVG 0", "AVG -1"]
    cases.append(harness.TestCase("average edge cases", make_input(cmds), None, weight=2.0))

    cmds = ["PUSH 1", "POP", "SIZE", "CAPACITY"]
    cases.append(harness.TestCase("push then pop to empty keeps capacity", make_input(cmds), None, weight=1.5))

    cmds = ["PUSH 4", "PUSH 8", "SET 1 100", "AVG 2", "GET 1"]
    cases.append(harness.TestCase("SET updates prefix sums correctly", make_input(cmds), None, weight=2.0))

    # ---------- HIDDEN ----------
    cmds = []
    for i in range(1, 20):
        cmds.append(f"PUSH {i}")
    cmds.append("CAPACITY")
    for _ in range(15):
        cmds.append("POP")
    cmds.append("CAPACITY")
    cmds.append("SIZE")
    cases.append(harness.TestCase("many grows then many shrinks", make_input(cmds), None, weight=2.5, hidden=True))

    cmds = ["PUSH 3", "PUSH 6", "PUSH 9", "PUSH 12", "SET 0 0", "SET 3 0", "AVG 4"]
    cases.append(harness.TestCase("SET boundary indices", make_input(cmds), None, weight=1.5, hidden=True))

    rng = random.Random(5)
    cmds = []
    n = 0
    for _ in range(500):
        op = rng.choice(["PUSH", "PUSH", "PUSH", "POP", "AVG", "SET", "SIZE", "CAPACITY"])
        if op == "PUSH":
            cmds.append(f"PUSH {rng.randint(-50,50)}")
            n += 1
        elif op == "POP" and n > 0:
            cmds.append("POP")
            n -= 1
        elif op == "AVG" and n > 0:
            cmds.append(f"AVG {rng.randint(1,n)}")
        elif op == "SET" and n > 0:
            cmds.append(f"SET {rng.randint(0,n-1)} {rng.randint(-50,50)}")
        elif op in ("SIZE", "CAPACITY"):
            cmds.append(op)
        # else: precondition not met (e.g. POP/AVG/SET with n==0) -- skip,
        # don't emit a malformed command.
    cases.append(harness.TestCase("randomized 500-op scenario", make_input(cmds), None, weight=3.0, hidden=True))

    # Non-integer average formatting
    cmds = ["PUSH 1", "PUSH 2", "AVG 2", "PUSH 4", "AVG 3"]
    cases.append(harness.TestCase("fractional average formatting", make_input(cmds), None, weight=1.5, hidden=True))

    # ---------- PERFORMANCE / TLE TRAPS ----------
    # 30000 pushes then 30000 large-k AVG queries: an O(k)-per-query
    # rescan (instead of O(1) via prefix sums) will time out here.
    cmds = [f"PUSH {i % 97}" for i in range(30000)]
    cmds += ["AVG 30000"] * 30000
    cases.append(harness.TestCase("PERF: 30000 full-window AVG queries", make_input(cmds), None,
                                   weight=4.0, hidden=True, timeout=6.0))

    # 200000 pure push/pop cycling: an implementation that reallocates on
    # EVERY push/pop (i.e. not amortized -- e.g. always doubling or always
    # rebuilding from scratch) will time out; correct amortized O(1) will
    # finish quickly.
    cmds = []
    for _ in range(100000):
        cmds.append("PUSH 1")
        cmds.append("PUSH 2")
        cmds.append("POP")
    cmds.append("SIZE")
    cases.append(harness.TestCase("PERF: 300000 push/pop amortized check", make_input(cmds), None,
                                   weight=4.0, hidden=True, timeout=6.0))

    # thrash right at the shrink boundary many times, to catch an off-by
    # one in the >= vs > condition, or missing the "size>0" guard.
    cmds = ["PUSH 1"] * 8
    for _ in range(2000):
        cmds.append("POP")
        cmds.append("PUSH 1")
    cmds.append("CAPACITY")
    cases.append(harness.TestCase("thrash exactly at shrink boundary", make_input(cmds), None,
                                   weight=3.0, hidden=True, timeout=5.0))

    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q3 -- The Complaint Ledger -- Autograder Report")
