import random
import subprocess
import sys
import time
import os
from collections import deque

TIME_LIMIT = 3.0
LARGE_TIME_LIMIT = 4.0
HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(HERE, "student_code.py")


def _run_reference(ops):
    d = deque()
    out = []
    for op in ops:
        if op[0] == 1:
            d.append(op[1])
        elif op[0] == 2:
            out.append(str(d[0]) if d else "-1")
        elif op[0] == 3:
            out.append(str(d.popleft()) if d else "-1")
        elif op[0] == 4:
            out.append(str(len(d)))
    return "\n".join(out)


def _ops_to_text(ops):
    lines = [str(len(ops))]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


def gen_visible_1():
    return [(1, 10), (1, 20), (1, 30), (2,), (3,), (3,), (4,), (1, 40),
            (2,), (3,), (3,), (3,), (4,)]


def gen_visible_2():
    return [(2,), (3,), (4,), (1, 5), (1, 6), (3,), (1, 7), (2,), (3,), (3,), (4,)]


def gen_hidden_random(seed):
    rng = random.Random(seed)
    ops, n = [], 0
    for _ in range(rng.randint(40, 150)):
        c = rng.random()
        if c < 0.5 or n == 0:
            ops.append((1, rng.randint(-999, 999))); n += 1
        elif c < 0.8:
            ops.append((3,)); n = max(0, n - 1)
        elif c < 0.9:
            ops.append((2,))
        else:
            ops.append((4,))
    return ops


def gen_hidden_alternating(seed):
    """enqueue, dequeue, enqueue, dequeue... forces the front/back
    rebalance repeatedly -- a correct O(1)-amortised solution handles
    this fine; an accidental O(n) per op (e.g. reversing on every single
    call regardless of whether front is empty) will not scale."""
    ops = []
    for i in range(20000):
        ops.append((1, i))
        ops.append((3,))
    return ops


def gen_hidden_perf(n=30000):
    ops = [(1, i) for i in range(n)] + [(3,) for _ in range(n)]
    return ops


def run_student(input_text, time_limit):
    try:
        start = time.perf_counter()
        result = subprocess.run([sys.executable, STUDENT_FILE], input=input_text,
                                 capture_output=True, text=True, timeout=time_limit)
        elapsed = time.perf_counter() - start
        if result.returncode != 0:
            return "RE", (result.stderr.strip().splitlines() or ["error"])[-1], elapsed
        return "OK", result.stdout.strip("\n"), elapsed
    except subprocess.TimeoutExpired:
        return "TLE", None, time_limit


def check(name, ops, weight, time_limit=TIME_LIMIT):
    expected = _run_reference(ops)
    status, payload, elapsed = run_student(_ops_to_text(ops), time_limit)
    if status == "TLE":
        print(f"[{name:28s}] TLE               weight={weight:3d} -> 0/{weight}")
        return 0
    if status == "RE":
        print(f"[{name:28s}] RE ({payload})   weight={weight:3d} -> 0/{weight}")
        return 0
    if payload == expected:
        print(f"[{name:28s}] AC ({elapsed:5.2f}s)      weight={weight:3d} -> {weight}/{weight}")
        return weight
    print(f"[{name:28s}] WA ({elapsed:5.2f}s)      weight={weight:3d} -> 0/{weight}")
    return 0


IMMUTABILITY_SNIPPET = r'''
import sys
sys.path.insert(0, {here!r})
from student_code import Q, EMPTY, enqueue, dequeue, size, is_empty

q0 = Q(EMPTY, EMPTY, 0)
q1 = enqueue(q0, 1)
q2 = enqueue(q1, 2)
q3 = enqueue(q2, 3)
a, q4 = dequeue(q3)      # a should be 1; q3 must remain untouched
q5 = enqueue(q4, 4)      # branch A: [2,3,4]
b, q6 = dequeue(q3)      # branch B, re-derived from the OLD q3 -- must also give 1
c, q7 = dequeue(q6)      # branch B continues: should give 2
d, q8 = dequeue(q5)      # branch A continues: should give 2
print(a, b, c, d, size(q3), size(q5), size(q7), size(q8), is_empty(Q(EMPTY, EMPTY, 0)))
'''


def check_immutability(weight):
    name = "hidden_persistence_branching"
    code = IMMUTABILITY_SNIPPET.format(here=HERE)
    try:
        result = subprocess.run([sys.executable, "-c", code], capture_output=True,
                                 text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        print(f"[{name:28s}] TLE               weight={weight:3d} -> 0/{weight}")
        return 0
    expected = "1 1 2 2 3 3 1 2 True"
    got = result.stdout.strip()
    if result.returncode != 0:
        err = (result.stderr.strip().splitlines() or ["error"])[-1]
        print(f"[{name:28s}] RE ({err})   weight={weight:3d} -> 0/{weight}")
        return 0
    if got == expected:
        print(f"[{name:28s}] AC               weight={weight:3d} -> {weight}/{weight}")
        return weight
    print(f"[{name:28s}] WA (got {got!r})   weight={weight:3d} -> 0/{weight}")
    return 0


def main():
    total, max_total = 0, 0
    tests = [
        ("visible_basic", gen_visible_1(), 6, TIME_LIMIT),
        ("visible_empty_edge", gen_visible_2(), 6, TIME_LIMIT),
    ]
    for i in range(1, 7):
        tests.append((f"hidden_random_{i}", gen_hidden_random(300 + i), 6, TIME_LIMIT))
    tests.append(("hidden_alternating_stress", gen_hidden_alternating(1), 12, TIME_LIMIT))
    tests.append(("hidden_perf_smoke_30k", gen_hidden_perf(30000), 16, LARGE_TIME_LIMIT))

    for name, ops, weight, tl in tests:
        max_total += weight
        total += check(name, ops, weight, tl)

    max_total += 24
    total += check_immutability(24)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
