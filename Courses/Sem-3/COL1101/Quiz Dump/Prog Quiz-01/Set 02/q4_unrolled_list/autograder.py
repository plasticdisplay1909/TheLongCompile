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
    cmds = ["append 10", "append 20", "append 30", "access 0", "access 2", "len",
            "append 40", "access 3", "set 1 99", "access 1"]
    cases.append(harness.TestCase("basic sample", make_input(cmds), None, weight=2.0))

    cmds = ["append 5", "append 3", "append 8", "append 1", "pop", "access 1",
            "append 9", "append 2", "len", "pop", "pop", "access 0", "set 0 100", "access 0"]
    cases.append(harness.TestCase("mixed append/pop/access", make_input(cmds), None, weight=2.0))

    cmds = ["append 1", "pop", "append 2", "append 3", "pop", "pop", "append 9", "access 0", "len"]
    cases.append(harness.TestCase("pop to empty then refill", make_input(cmds), None, weight=1.5))

    # a size that straddles a couple of block boundaries for BLOCK_CAP~300
    cmds = [f"append {i}" for i in range(650)]
    cmds += ["access 0", "access 299", "access 300", "access 301", "access 649", "len"]
    cases.append(harness.TestCase("access across block boundaries", make_input(cmds), None, weight=2.5))

    # ---------- HIDDEN ----------
    cmds = [f"append {i*i}" for i in range(1000)]
    for i in (0, 1, 299, 300, 599, 600, 900, 999):
        cmds.append(f"access {i}")
    for i in range(999, 500, -1):
        cmds.append("pop")
    cmds.append("len")
    cmds.append("access 0")
    cases.append(harness.TestCase("build 1000 then drain to 501", make_input(cmds), None, weight=2.5, hidden=True))

    cmds = [f"append {i}" for i in range(50)]
    for i in range(50):
        cmds.append(f"set {i} {49-i}")
    for i in range(50):
        cmds.append(f"access {i}")
    cases.append(harness.TestCase("reverse via set then read back", make_input(cmds), None, weight=2.0, hidden=True))

    rng = random.Random(3)
    cmds = []
    n = 0
    for _ in range(1500):
        op = rng.choice(["append", "append", "pop", "access", "set", "len"])
        if op == "append":
            cmds.append(f"append {rng.randint(-1000,1000)}")
            n += 1
        elif op == "pop" and n > 0:
            cmds.append("pop")
            n -= 1
        elif op == "access" and n > 0:
            cmds.append(f"access {rng.randint(0,n-1)}")
        elif op == "set" and n > 0:
            cmds.append(f"set {rng.randint(0,n-1)} {rng.randint(-1000,1000)}")
        elif op == "len":
            cmds.append("len")
    cases.append(harness.TestCase("randomized 1500-op scenario", make_input(cmds), None, weight=3.0, hidden=True))

    # ---------- PERFORMANCE / TLE TRAPS ----------
    # Build a large list, then hammer it with far (head<->tail alternating)
    # accesses. A block-chain walk from the nearer end stays cheap; a
    # naive singly-linked, one-node-per-element walk from the head every
    # time will be catastrophically slow here.
    N = 150000
    cmds = [f"append {i}" for i in range(N)]
    rng2 = random.Random(9)
    for _ in range(8000):
        cmds.append(f"access {rng2.randint(0, N-1)}")
    cases.append(harness.TestCase("PERF: 150000 elements, 8000 random accesses", make_input(cmds), None,
                                   weight=4.0, hidden=True, timeout=3.0))

    # Heavy append/pop churn.
    cmds = []
    for _ in range(150000):
        cmds.append("append 1")
    for _ in range(150000):
        cmds.append("pop")
    cmds.append("len")
    cases.append(harness.TestCase("PERF: 300000 append/pop churn", make_input(cmds), None,
                                   weight=3.0, hidden=True, timeout=3.0))

    # Alternating append/set near the tail -- exercises the "walk from
    # the nearer end" optimisation directly.
    cmds = [f"append {i}" for i in range(80000)]
    for i in range(6000):
        cmds.append(f"set {79999 - i} {i}")
        cmds.append(f"access {79999 - i}")
    cases.append(harness.TestCase("PERF: 6000 near-tail set/access pairs", make_input(cmds), None,
                                   weight=3.0, hidden=True, timeout=3.0))

    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q4 -- The Unrolled Ledger -- Autograder Report")
