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
        if op[0] == "ENQ":
            d.append(op[1])
        elif op[0] == "DEQ":
            out.append(str(d.popleft()))
        elif op[0] == "MIN":
            out.append(str(min(d)))
        elif op[0] == "MAX":
            out.append(str(max(d)))
        elif op[0] == "SIZE":
            out.append(str(len(d)))
    return "\n".join(out)


def _ops_to_text(ops):
    lines = [str(len(ops))]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


def gen_visible_1():
    return [("ENQ", 5), ("ENQ", 1), ("ENQ", 9), ("MIN",), ("MAX",),
            ("DEQ",), ("MIN",), ("MAX",), ("ENQ", -3), ("MIN",),
            ("DEQ",), ("DEQ",), ("MIN",), ("MAX",), ("SIZE",)]


def gen_visible_2():
    ops = [("ENQ", 4), ("DEQ",), ("ENQ", 4), ("ENQ", 4), ("MIN",),
           ("MAX",), ("DEQ",), ("DEQ",), ("ENQ", 100), ("ENQ", -100),
           ("MIN",), ("MAX",), ("SIZE",)]
    return ops


def gen_hidden_random(seed):
    rng = random.Random(seed)
    ops, n = [], 0
    for _ in range(rng.randint(60, 200)):
        c = rng.random()
        if c < 0.5 or n == 0:
            ops.append(("ENQ", rng.randint(-500, 500))); n += 1
        elif c < 0.75:
            ops.append(("DEQ",)); n -= 1
        elif c < 0.87:
            ops.append(("MIN",))
        elif c < 0.99:
            ops.append(("MAX",))
        else:
            ops.append(("SIZE",))
    return ops


def gen_hidden_interleave_stress(seed):
    """enqueue, dequeue, enqueue, dequeue -- forces the internal
    in-stack/out-stack transfer over and over. A correct amortised
    O(1) solution is unaffected; a solution that reverses/rescans on
    every single call degrades badly."""
    rng = random.Random(seed)
    ops = []
    for i in range(15000):
        ops.append(("ENQ", rng.randint(-1000, 1000)))
        ops.append(("MIN",))
        ops.append(("MAX",))
        ops.append(("DEQ",))
    return ops


def gen_hidden_perf(n=250000):
    rng = random.Random(555)
    ops = [("ENQ", rng.randint(-10**6, 10**6)) for _ in range(n)]
    for _ in range(n):
        c = rng.random()
        if c < 0.4:
            ops.append(("DEQ",))
        elif c < 0.7:
            ops.append(("MIN",))
        else:
            ops.append(("MAX",))
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


def main():
    total, max_total = 0, 0
    tests = [("visible_basic", gen_visible_1(), 8, TIME_LIMIT),
             ("visible_duplicates_and_signs", gen_visible_2(), 8, TIME_LIMIT)]
    for i in range(1, 9):
        tests.append((f"hidden_random_{i}", gen_hidden_random(4000 + i), 6, TIME_LIMIT))
    tests.append(("hidden_interleave_stress", gen_hidden_interleave_stress(1), 16, TIME_LIMIT))
    tests.append(("hidden_perf_smoke_250k", gen_hidden_perf(250000), 20, LARGE_TIME_LIMIT))

    for name, ops, weight, tl in tests:
        max_total += weight
        total += check(name, ops, weight, tl)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
