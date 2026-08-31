import random
import subprocess
import sys
import time
import os
from collections import OrderedDict

TIME_LIMIT = 3.0
LARGE_TIME_LIMIT = 4.0
HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(HERE, "student_code.py")


def _run_reference(capacity, ops):
    od = OrderedDict()
    out = []
    for op in ops:
        if op[0] == "PUT":
            k, v = op[1], op[2]
            if k in od:
                od.move_to_end(k)
                od[k] = v
            else:
                if len(od) >= capacity:
                    od.popitem(last=False)
                od[k] = v
        elif op[0] == "GET":
            k = op[1]
            if k in od:
                od.move_to_end(k)
                out.append(str(od[k]))
            else:
                out.append("-1")
        elif op[0] == "SIZE":
            out.append(str(len(od)))
    return "\n".join(out)


def _ops_to_text(capacity, ops):
    lines = [f"{capacity} {len(ops)}"]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


def gen_visible_1():
    cap = 2
    ops = [("PUT", 1, 100), ("PUT", 2, 200), ("GET", 1), ("PUT", 3, 300),
           ("GET", 2), ("PUT", 4, 400), ("GET", 1), ("GET", 3), ("GET", 4),
           ("SIZE",)]
    return cap, ops


def gen_visible_2():
    cap = 1
    ops = [("PUT", 1, 10), ("GET", 1), ("PUT", 2, 20), ("GET", 1), ("GET", 2),
           ("PUT", 1, 99), ("GET", 1), ("SIZE",)]
    return cap, ops


def gen_hidden_random(seed):
    rng = random.Random(seed)
    cap = rng.randint(1, 8)
    ops = []
    keyspace = list(range(1, 20))
    for _ in range(rng.randint(60, 200)):
        c = rng.random()
        k = rng.choice(keyspace)
        if c < 0.55:
            ops.append(("PUT", k, rng.randint(0, 10000)))
        elif c < 0.9:
            ops.append(("GET", k))
        else:
            ops.append(("SIZE",))
    return cap, ops


def gen_hidden_update_no_evict(seed):
    """Repeatedly PUT the same small set of keys at a cache exactly at
    capacity -- updating an existing key must NEVER trigger an eviction."""
    rng = random.Random(seed)
    cap = 3
    ops = [("PUT", 1, 1), ("PUT", 2, 2), ("PUT", 3, 3)]
    for _ in range(500):
        k = rng.randint(1, 3)
        ops.append(("PUT", k, rng.randint(0, 999)))
        ops.append(("GET", rng.randint(1, 3)))
    return cap, ops


def gen_hidden_perf(n=150000):
    cap = 1000
    ops = []
    for i in range(n):
        ops.append(("PUT", i % 2000, i))
        if i % 3 == 0:
            ops.append(("GET", (i * 7) % 2000))
    return cap, ops


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


def check(name, capacity, ops, weight, time_limit=TIME_LIMIT):
    expected = _run_reference(capacity, ops)
    status, payload, elapsed = run_student(_ops_to_text(capacity, ops), time_limit)
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
    tests = [("visible_basic_eviction", *gen_visible_1(), 8, TIME_LIMIT),
             ("visible_capacity_one", *gen_visible_2(), 8, TIME_LIMIT)]
    for i in range(1, 9):
        cap, ops = gen_hidden_random(700 + i)
        tests.append((f"hidden_random_{i}", cap, ops, 6, TIME_LIMIT))
    cap, ops = gen_hidden_update_no_evict(9)
    tests.append(("hidden_update_no_evict", cap, ops, 12, TIME_LIMIT))
    cap, ops = gen_hidden_perf(150000)
    tests.append(("hidden_perf_smoke_150k", cap, ops, 24, LARGE_TIME_LIMIT))

    for entry in tests:
        name, cap, ops, weight, tl = entry
        max_total += weight
        total += check(name, cap, ops, weight, tl)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
