import os
import sys
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import harness  # noqa: E402

REF = os.path.join(HERE, "reference_solution.py")
STUDENT = os.path.join(HERE, "student_code.py")


def make_input(cap, cmds):
    return f"{cap}\n{len(cmds)}\n" + "\n".join(cmds) + "\n"


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
    cmds = ["PRODUCE t1 A", "PRODUCE t2 B", "PRODUCE t3 C", "STATUS",
            "CONSUME c1", "STATUS", "CONSUME c2", "CONSUME c3", "STATUS"]
    cases.append(harness.TestCase("basic blocking + wake, cap=2", make_input(2, cmds), None, weight=2.5))

    cmds = ["CONSUME c1", "STATUS", "PRODUCE t1 X", "STATUS"]
    cases.append(harness.TestCase("consumer blocks on empty buffer first", make_input(1, cmds), None, weight=2.0))

    cmds = ["PRODUCE t1 A", "PRODUCE t2 B", "PRODUCE t3 C", "PRODUCE t4 D", "STATUS"]
    cases.append(harness.TestCase("multiple producers queue up fairly", make_input(1, cmds), None, weight=2.0))

    cmds = ["CONSUME c1", "CONSUME c2", "CONSUME c3", "PRODUCE t1 X", "STATUS", "STATUS"]
    cases.append(harness.TestCase("multiple consumers queue up, one wakes", make_input(1, cmds), None, weight=2.0))

    # ---------- HIDDEN ----------
    cmds = ["PRODUCE t1 A", "PRODUCE t2 B", "PRODUCE t3 C", "PRODUCE t4 D",
            "CONSUME c1", "STATUS"]
    cases.append(harness.TestCase("one consume wakes exactly one producer (cap=1)", make_input(1, cmds), None, weight=2.0, hidden=True))

    cmds = ["PRODUCE t1 A", "PRODUCE t2 B", "PRODUCE t3 C", "PRODUCE t4 D", "PRODUCE t5 E",
            "CONSUME c1", "CONSUME c2", "STATUS"]
    cases.append(harness.TestCase("wake chain drains multiple producers, cap=2", make_input(2, cmds), None, weight=2.5, hidden=True))

    # fairness: a producer that arrives while another producer is already
    # blocked must ALSO block, even though the buffer isn't literally full
    # (it becomes full only because of accumulation) -- exercised with a
    # capacity where a naive "just check is_full()" implementation could
    # be tempted to let a later arrival cut the line.
    cmds = ["PRODUCE t1 A", "PRODUCE t2 B", "PRODUCE t3 C", "STATUS", "CONSUME c1", "STATUS"]
    cases.append(harness.TestCase("fairness: no cutting the producer line", make_input(2, cmds), None, weight=2.5, hidden=True))

    cmds = ["PRODUCE t1 A", "CONSUME c1", "CONSUME c2", "CONSUME c3", "PRODUCE t2 B", "PRODUCE t3 C", "STATUS"]
    cases.append(harness.TestCase("fairness on the consumer side too", make_input(1, cmds), None, weight=2.5, hidden=True))

    # empty system status
    cmds = ["STATUS"]
    cases.append(harness.TestCase("status on a fresh empty bakery", make_input(3, cmds), None, weight=1.0, hidden=True))

    rng = random.Random(13)
    cmds = []
    for i in range(400):
        if rng.random() < 0.5:
            cmds.append(f"PRODUCE p{i} item{i}")
        else:
            cmds.append(f"CONSUME c{i}")
        if i % 25 == 0:
            cmds.append("STATUS")
    cases.append(harness.TestCase("randomized 400-op producer/consumer mix, cap=5", make_input(5, cmds), None, weight=3.0, hidden=True))

    # ---------- PERFORMANCE / TLE TRAPS ----------
    # capacity 1: first PRODUCE succeeds, the next N all block, then N
    # CONSUMEs each wake exactly one waiting producer in turn. An O(n)
    # pop-from-front wait queue (e.g. python list.pop(0)) makes the whole
    # drain O(n^2); a proper O(1) linked queue makes it O(n).
    N = 400000
    cmds = [f"PRODUCE p{i} item{i}" for i in range(N)]
    cmds += [f"CONSUME c{i}" for i in range(N)]
    cases.append(harness.TestCase("PERF: 400000 blocked producers drained one by one", make_input(1, cmds), None,
                                   weight=4.0, hidden=True, timeout=4.0))

    # symmetric consumer-side version
    cmds = [f"CONSUME c{i}" for i in range(N)]
    cmds += [f"PRODUCE p{i} item{i}" for i in range(N)]
    cases.append(harness.TestCase("PERF: 400000 blocked consumers drained one by one", make_input(1, cmds), None,
                                   weight=4.0, hidden=True, timeout=4.0))

    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q6 -- The Bounded Buffer Bakery -- Autograder Report")
