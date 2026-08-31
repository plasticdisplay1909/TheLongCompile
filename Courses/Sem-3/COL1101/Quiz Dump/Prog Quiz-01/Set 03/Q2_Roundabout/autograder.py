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
        if op[0] == "PUSHF":
            d.appendleft(op[1])
        elif op[0] == "PUSHB":
            d.append(op[1])
        elif op[0] == "POPF":
            out.append(str(d.popleft()))
        elif op[0] == "POPB":
            out.append(str(d.pop()))
        elif op[0] == "FRONT":
            out.append(str(d[0]))
        elif op[0] == "BACK":
            out.append(str(d[-1]))
        elif op[0] == "SIZE":
            out.append(str(len(d)))
        elif op[0] == "ROTATE":
            d.rotate(-op[1])   # python's rotate(+1) moves back->front; ours is the opposite convention
    return "\n".join(out)


def _ops_to_text(ops):
    lines = [str(len(ops))]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


def gen_visible_1():
    return [("PUSHB", 1), ("PUSHB", 2), ("PUSHB", 3), ("PUSHF", 0),
            ("ROTATE", 1), ("FRONT",), ("BACK",), ("ROTATE", -2),
            ("FRONT",), ("BACK",), ("SIZE",)]


def gen_visible_2():
    ops = [("PUSHB", i) for i in range(6)]
    ops += [("ROTATE", 1000000000000), ("FRONT",), ("BACK",)]
    ops += [("ROTATE", -1000000000003), ("FRONT",), ("BACK",)]
    ops += [("POPF",), ("POPB",), ("SIZE",)]
    return ops


def gen_hidden_random(seed):
    rng = random.Random(seed)
    ops = []
    n = 0
    for _ in range(rng.randint(40, 120)):
        c = rng.random()
        if n == 0 or c < 0.25:
            ops.append(("PUSHF", rng.randint(-999, 999))); n += 1
        elif c < 0.5:
            ops.append(("PUSHB", rng.randint(-999, 999))); n += 1
        elif c < 0.65 and n > 0:
            ops.append(("POPF",)); n -= 1
        elif c < 0.8 and n > 0:
            ops.append(("POPB",)); n -= 1
        elif c < 0.9 and n > 0:
            ops.append(("ROTATE", rng.randint(-50, 50)))
        elif n > 0:
            ops.append(random.choice([("FRONT",), ("BACK",), ("SIZE",)]))
    return ops


def gen_hidden_huge_rotate(seed):
    rng = random.Random(seed)
    ops = [("PUSHB", i) for i in range(200)]
    for _ in range(30):
        k = rng.randint(-10**15, 10**15)
        ops.append(("ROTATE", k))
        ops.append(("FRONT",))
        ops.append(("BACK",))
    return ops


def gen_hidden_perf(n=300000):
    ops = [("PUSHB", i) for i in range(n)]
    ops.append(("ROTATE", 10**18 + 7))
    ops.append(("FRONT",))
    ops.append(("BACK",))
    for _ in range(n // 2):
        ops.append(("POPF",))
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
        print(f"[{name:26s}] TLE               weight={weight:3d} -> 0/{weight}")
        return 0
    if status == "RE":
        print(f"[{name:26s}] RE ({payload})   weight={weight:3d} -> 0/{weight}")
        return 0
    if payload == expected:
        print(f"[{name:26s}] AC ({elapsed:5.2f}s)      weight={weight:3d} -> {weight}/{weight}")
        return weight
    print(f"[{name:26s}] WA ({elapsed:5.2f}s)      weight={weight:3d} -> 0/{weight}")
    return 0


def main():
    total, max_total = 0, 0
    tests = [
        ("visible_basic",           gen_visible_1(),               6, TIME_LIMIT),
        ("visible_bignum_rotate",   gen_visible_2(),                6, TIME_LIMIT),
    ]
    for i in range(1, 9):
        tests.append((f"hidden_random_{i}", gen_hidden_random(500 + i), 6, TIME_LIMIT))
    tests.append(("hidden_huge_rotate_1", gen_hidden_huge_rotate(11), 12, TIME_LIMIT))
    tests.append(("hidden_huge_rotate_2", gen_hidden_huge_rotate(22), 12, TIME_LIMIT))
    tests.append(("hidden_perf_smoke_300k", gen_hidden_perf(300000), 16, LARGE_TIME_LIMIT))

    for name, ops, weight, tl in tests:
        max_total += weight
        total += check(name, ops, weight, tl)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
