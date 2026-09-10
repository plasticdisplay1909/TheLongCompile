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
    cmds = ["REGISTER p1 3", "REGISTER p2 1", "REGISTER p3 1", "NEXT", "SERVE",
            "NEXT", "REQUEUE p3 5", "NEXT", "SERVE", "RECALL", "COUNT", "NEXT"]
    cases.append(harness.TestCase("worked example from paper", make_input(cmds), None, weight=2.5))

    cmds = ["NEXT", "SERVE", "COUNT", "RECALL"]
    cases.append(harness.TestCase("empty router edge cases", make_input(cmds), None, weight=1.5))

    cmds = ["REGISTER a 1", "REGISTER b 1", "REGISTER c 1", "SERVE", "SERVE", "NEXT", "SERVE", "NEXT"]
    cases.append(harness.TestCase("FIFO within a single level", make_input(cmds), None, weight=1.5))

    cmds = ["REGISTER a 2", "REGISTER b 4", "REQUEUE a 4", "NEXT", "REQUEUE b 1", "NEXT"]
    cases.append(harness.TestCase("requeue changes priority ordering", make_input(cmds), None, weight=2.0))

    cmds = ["REGISTER a 2", "SERVE", "REGISTER b 1", "RECALL", "NEXT", "COUNT"]
    cases.append(harness.TestCase("recall reinserts at original level", make_input(cmds), None, weight=2.0))

    # ---------- HIDDEN ----------
    cmds = ["REGISTER a 3", "SERVE", "REGISTER a 1", "SERVE", "RECALL", "NEXT"]
    cases.append(harness.TestCase("pid reused after fully discharged", make_input(cmds), None, weight=2.0, hidden=True))

    cmds = ["REGISTER a 2", "REGISTER b 2", "REQUEUE a 2", "NEXT", "SERVE", "NEXT"]
    cases.append(harness.TestCase("requeue to the SAME level moves to back", make_input(cmds), None, weight=2.0, hidden=True))

    cmds = ["REQUEUE ghost 1", "REGISTER a 1", "REQUEUE ghost 2", "NEXT"]
    cases.append(harness.TestCase("requeue of unknown pid is a no-op", make_input(cmds), None, weight=1.5, hidden=True))

    cmds = ["REGISTER a 1", "SERVE", "REGISTER a 5"]  # pid re-registered while "gone" (served) -- allowed
    cmds += ["NEXT", "RECALL", "NEXT", "COUNT"]
    cases.append(harness.TestCase("re-register after discharge, then recall old one", make_input(cmds), None, weight=2.5, hidden=True))

    cmds = ["REGISTER a 1", "REGISTER b 1", "REGISTER c 1", "SERVE", "SERVE", "SERVE", "RECALL", "RECALL", "RECALL", "RECALL", "NEXT"]
    cases.append(harness.TestCase("stack order of multiple recalls (LIFO)", make_input(cmds), None, weight=2.5, hidden=True))

    rng = random.Random(21)
    cmds = []
    active = set()
    served_ids = []
    next_id = 0
    for _ in range(600):
        op = rng.choice(["REG", "REG", "SERVE", "NEXT", "COUNT", "REQ", "RECALL"])
        if op == "REG":
            pid = f"pt{next_id}"; next_id += 1
            cmds.append(f"REGISTER {pid} {rng.randint(1,5)}")
            active.add(pid)
        elif op == "SERVE":
            cmds.append("SERVE")
        elif op == "NEXT":
            cmds.append("NEXT")
        elif op == "COUNT":
            cmds.append("COUNT")
        elif op == "REQ" and active:
            pid = rng.choice(list(active))
            cmds.append(f"REQUEUE {pid} {rng.randint(1,5)}")
        elif op == "RECALL":
            cmds.append("RECALL")
    cases.append(harness.TestCase("randomized 600-op scenario", make_input(cmds), None, weight=3.5, hidden=True))

    # ---------- PERFORMANCE / TLE TRAPS ----------
    # 100000 registrations spread across levels, then 100000 REQUEUEs of
    # random existing patients (an O(level size) search-based REQUEUE
    # will be quadratic here), then drain everything.
    cmds = []
    ids = []
    rng2 = random.Random(77)
    for i in range(100000):
        pid = f"x{i}"
        cmds.append(f"REGISTER {pid} {rng2.randint(1,5)}")
        ids.append(pid)
    for _ in range(100000):
        pid = rng2.choice(ids)
        cmds.append(f"REQUEUE {pid} {rng2.randint(1,5)}")
    for _ in range(100000):
        cmds.append("SERVE")
    cases.append(harness.TestCase("PERF: 100000 registers + requeues + serves", make_input(cmds), None,
                                   weight=4.0, hidden=True, timeout=5.0))

    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q5 -- The Emergency Router -- Autograder Report")
