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
    cmds = ["CREATE A", "ADD A 5", "ADD A 3", "ADD A 5", "CONTAINS A 5", "CONTAINS A 9",
            "SIZE A", "REMOVE A 3", "SIZE A", "CREATE B", "ADD B 3", "ADD B 5", "ADD B 7",
            "UNION A B U", "ITEMS U", "INTERSECT A B I", "ITEMS I"]
    cases.append(harness.TestCase("basic ops + union/intersect", make_input(cmds), None, weight=2.5))

    cmds = ["ADD A 1", "ADD A 2", "ADD A 3", "DIFF A A D", "ITEMS D",
            "REMOVE A 2", "REMOVE A 99", "ITEMS A"]
    cases.append(harness.TestCase("self-diff and remove-missing no-op", make_input(cmds), None, weight=2.0))

    cmds = ["CONTAINS ghost 1", "SIZE ghost", "ITEMS ghost"]
    cases.append(harness.TestCase("querying an implicitly-created empty set", make_input(cmds), None, weight=1.5))

    cmds = ["ADD A hello", "ADD A world", "ADD A 5", "CONTAINS A hello", "CONTAINS A 5", "ITEMS A"]
    cases.append(harness.TestCase("string and int elements mixed", make_input(cmds), None, weight=2.0))

    # ---------- HIDDEN ----------
    cmds = [f"ADD A {i}" for i in range(20)] + [f"REMOVE A {i}" for i in range(0, 20, 2)] + ["ITEMS A", "SIZE A"]
    cases.append(harness.TestCase("grow then shrink back down", make_input(cmds), None, weight=2.5, hidden=True))

    # add, remove, re-add the SAME key repeatedly (tombstone reuse)
    cmds = []
    for _ in range(50):
        cmds += ["ADD A 42", "REMOVE A 42"]
    cmds += ["ADD A 42", "CONTAINS A 42", "SIZE A"]
    cases.append(harness.TestCase("repeated add/remove of the same key (tombstone churn)", make_input(cmds), None, weight=2.5, hidden=True))

    # negative numbers / hash sign handling
    cmds = ["ADD A -5", "ADD A -1", "ADD A 0", "CONTAINS A -5", "ITEMS A"]
    cases.append(harness.TestCase("negative integers", make_input(cmds), None, weight=1.5, hidden=True))

    # UNION/INTERSECT/DIFF where dest name collides with a source name
    cmds = ["ADD A 1", "ADD A 2", "ADD B 2", "ADD B 3", "UNION A B A", "ITEMS A"]
    cases.append(harness.TestCase("union writing into one of its own operands", make_input(cmds), None, weight=2.0, hidden=True))

    rng = random.Random(31)
    cmds = []
    truth = {"A": set(), "B": set()}
    for _ in range(800):
        op = rng.choice(["ADD", "ADD", "REMOVE", "CONTAINS", "SIZE"])
        name = rng.choice(["A", "B"])
        val = rng.randint(-20, 20)
        if op == "ADD":
            cmds.append(f"ADD {name} {val}")
            truth[name].add(val)
        elif op == "REMOVE":
            cmds.append(f"REMOVE {name} {val}")
            truth[name].discard(val)
        elif op == "CONTAINS":
            cmds.append(f"CONTAINS {name} {val}")
        elif op == "SIZE":
            cmds.append(f"SIZE {name}")
    cmds += ["ITEMS A", "ITEMS B"]
    cases.append(harness.TestCase("randomized 800-op scenario on two sets", make_input(cmds), None, weight=3.0, hidden=True))

    # ---------- PERFORMANCE / TLE TRAPS ----------
    # 200000 adds of distinct keys, then 200000 CONTAINS lookups. A linear
    # (non-hashed) implementation, or one that never grows its table (so
    # every probe degrades toward O(n)), will not finish in time.
    N = 200000
    cmds = [f"ADD A {i}" for i in range(N)]
    cmds += [f"CONTAINS A {i}" for i in range(0, N, 2)]
    cases.append(harness.TestCase("PERF: 200000 adds + 100000 lookups", make_input(cmds), None,
                                   weight=4.0, hidden=True, timeout=6.0))

    # heavy churn: add/remove the same growing/shrinking key set repeatedly,
    # to stress the grow/shrink resize policy under load.
    cmds = []
    rng2 = random.Random(55)
    for _ in range(150000):
        v = rng2.randint(0, 5000)
        if rng2.random() < 0.55:
            cmds.append(f"ADD A {v}")
        else:
            cmds.append(f"REMOVE A {v}")
    cmds.append("SIZE A")
    cases.append(harness.TestCase("PERF: 150000 churned add/remove", make_input(cmds), None,
                                   weight=4.0, hidden=True, timeout=6.0))

    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q8 -- The Roll Number Registry -- Autograder Report")
