"""
Autograder for Q1: The Elastic Array.

Usage:
    python3 autograder.py

Runs student_code.py (must be in the same directory) against visible and
hidden test cases, catching Wrong Answer (WA), Runtime Errors (RE), and
Time-Limit-Exceeded (TLE) separately, then prints a per-test report and a
final mark out of 100.
"""
import importlib.util
import random
import subprocess
import sys
import time
import os

TIME_LIMIT = 3.0            # seconds, per test case
LARGE_N_TIME_LIMIT = 4.0    # seconds, for the O(n) vs O(n^2) smoke test
HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(HERE, "student_code.py")


# ---------------------------------------------------------------------
# Reference implementation (used ONLY for generating expected answers).
# ---------------------------------------------------------------------
class _RefArray:
    def __init__(self):
        self.raw = [None]
        self.n = 0
        self.cap = 1

    def push_back(self, x):
        if self.n == self.cap:
            self._resize(self.cap * 2)
        self.raw[self.n] = x
        self.n += 1

    def pop_back(self):
        v = self.raw[self.n - 1]
        self.n -= 1
        if self.cap > 1 and self.n == self.cap // 4:
            self._resize(max(1, self.cap // 2))
        return v

    def get(self, i):
        return self.raw[i]

    def set(self, i, x):
        self.raw[i] = x

    def size(self):
        return self.n

    def capacity(self):
        return self.cap

    def _resize(self, newcap):
        newraw = [None] * newcap
        for i in range(self.n):
            newraw[i] = self.raw[i]
        self.raw = newraw
        self.cap = newcap


def _run_reference(ops):
    a = _RefArray()
    out = []
    for op in ops:
        if op[0] == "PUSH":
            a.push_back(op[1])
        elif op[0] == "POP":
            out.append(str(a.pop_back()))
        elif op[0] == "GET":
            out.append(str(a.get(op[1])))
        elif op[0] == "SET":
            a.set(op[1], op[2])
        elif op[0] == "SIZE":
            out.append(str(a.size()))
        elif op[0] == "CAP":
            out.append(str(a.capacity()))
    return "\n".join(out)


def _ops_to_text(ops):
    lines = [str(len(ops))]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------
# Test-case generators.
# ---------------------------------------------------------------------
def gen_visible_1():
    return [("PUSH", 10), ("CAP",), ("PUSH", 20), ("CAP",), ("PUSH", 30),
            ("CAP",), ("GET", 1), ("SET", 1, 99), ("GET", 1), ("SIZE",),
            ("POP",), ("SIZE",), ("CAP",)]


def gen_visible_2():
    ops = [("PUSH", i) for i in range(1, 9)]
    ops += [("POP",)] * 7
    ops += [("CAP",), ("PUSH", 100), ("PUSH", 200), ("CAP",)]
    return ops


def gen_hidden_small(seed):
    rng = random.Random(seed)
    ops = []
    n = 0
    for _ in range(rng.randint(20, 60)):
        choice = rng.random()
        if choice < 0.45 or n == 0:
            ops.append(("PUSH", rng.randint(-1000, 1000)))
            n += 1
        elif choice < 0.75:
            ops.append(("POP",))
            n -= 1
        elif choice < 0.85 and n > 0:
            ops.append(("GET", rng.randint(0, n - 1)))
        elif n > 0:
            ops.append(("SET", rng.randint(0, n - 1), rng.randint(-1000, 1000)))
        if rng.random() < 0.2:
            ops.append(("SIZE",))
        if rng.random() < 0.2:
            ops.append(("CAP",))
    return ops


def gen_hidden_adversarial_thrash(seed):
    """Push up to a plateau, then alternate push/pop right at a resize
    boundary many times -- this is exactly the pattern that breaks a
    naive 'shrink whenever size < capacity' rule."""
    rng = random.Random(seed)
    ops = [("PUSH", i) for i in range(64)]
    for _ in range(4000):
        ops.append(("POP",))
        ops.append(("PUSH", rng.randint(0, 9)))
    return ops


def gen_hidden_large_perf(n=200000):
    """Large all-push-then-all-pop-then-all-push sequence used as a
    performance smoke test. A correct amortised-O(1) solution finishes
    comfortably inside the time limit; an O(n) push/pop (e.g. shifting
    elements, or resizing by +1 each time) will not."""
    ops = [("PUSH", i) for i in range(n)]
    ops += [("POP",) for _ in range(n // 2)]
    ops += [("PUSH", i) for i in range(n // 2)]
    return ops


# ---------------------------------------------------------------------
# Harness: run the student's program as a subprocess with a time limit.
# ---------------------------------------------------------------------
def run_student(input_text, time_limit):
    try:
        start = time.perf_counter()
        result = subprocess.run(
            [sys.executable, STUDENT_FILE],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=time_limit,
        )
        elapsed = time.perf_counter() - start
        if result.returncode != 0:
            return "RE", result.stderr.strip().splitlines()[-1:] if result.stderr else "runtime error", elapsed
        return "OK", result.stdout.strip("\n"), elapsed
    except subprocess.TimeoutExpired:
        return "TLE", None, time_limit


def check(name, ops, weight, time_limit=TIME_LIMIT, expect_exact=True):
    expected = _run_reference(ops)
    input_text = _ops_to_text(ops)
    status, payload, elapsed = run_student(input_text, time_limit)
    if status == "TLE":
        print(f"[{name:28s}] TLE   (>{time_limit:.1f}s)                 weight={weight:3d}  -> 0/{weight}")
        return 0
    if status == "RE":
        print(f"[{name:28s}] RE    ({payload})   weight={weight:3d}  -> 0/{weight}")
        return 0
    if expect_exact and payload == expected:
        print(f"[{name:28s}] AC    ({elapsed:5.2f}s)                    weight={weight:3d}  -> {weight}/{weight}")
        return weight
    else:
        print(f"[{name:28s}] WA    ({elapsed:5.2f}s)                    weight={weight:3d}  -> 0/{weight}")
        return 0


def main():
    if not os.path.exists(STUDENT_FILE):
        print("student_code.py not found next to autograder.py")
        sys.exit(1)

    total = 0
    max_total = 0

    tests = [
        ("visible_basic_resize",        gen_visible_1(),                 5,  TIME_LIMIT),
        ("visible_shrink_pattern",      gen_visible_2(),                 5,  TIME_LIMIT),
    ]
    for i in range(1, 9):
        tests.append((f"hidden_random_{i}", gen_hidden_small(1000 + i), 5, TIME_LIMIT))
    tests.append(("hidden_thrash_adversarial_1", gen_hidden_adversarial_thrash(7), 15, TIME_LIMIT))
    tests.append(("hidden_thrash_adversarial_2", gen_hidden_adversarial_thrash(42), 15, TIME_LIMIT))
    tests.append(("hidden_perf_smoke_200k", gen_hidden_large_perf(200000), 15, LARGE_N_TIME_LIMIT))
    tests.append(("hidden_perf_smoke_400k", gen_hidden_large_perf(400000), 5, LARGE_N_TIME_LIMIT))

    for name, ops, weight, tl in tests:
        max_total += weight
        total += check(name, ops, weight, tl)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0 * total / max_total:.1f}%)")


if __name__ == "__main__":
    main()
