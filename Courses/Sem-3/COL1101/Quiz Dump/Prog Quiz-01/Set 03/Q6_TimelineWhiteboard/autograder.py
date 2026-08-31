import random
import subprocess
import sys
import time
import os

TIME_LIMIT = 3.0
LARGE_TIME_LIMIT = 4.0
HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(HERE, "student_code.py")


class _RCell:
    __slots__ = ("value", "rest")

    def __init__(self, value, rest):
        self.value = value
        self.rest = rest


def _run_reference(ops):
    # version -> (top_cell_or_None, size) -- true O(1) cons-based stack,
    # so the reference itself stays fast even on the huge perf test.
    versions = {0: (None, 0)}
    next_id = 1
    out = []
    for op in ops:
        if op[0] == "PUSH":
            v, x = op[1], op[2]
            top_cell, sz = versions[v]
            versions[next_id] = (_RCell(x, top_cell), sz + 1)
            out.append(str(next_id))
            next_id += 1
        elif op[0] == "POP":
            v = op[1]
            top_cell, sz = versions[v]
            x = top_cell.value
            versions[next_id] = (top_cell.rest, sz - 1)
            out.append(f"{x} {next_id}")
            next_id += 1
        elif op[0] == "TOP":
            top_cell, sz = versions[op[1]]
            out.append(str(top_cell.value))
        elif op[0] == "SIZE":
            out.append(str(versions[op[1]][1]))
    return "\n".join(out)


def _ops_to_text(ops):
    lines = [str(len(ops))]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


def gen_visible_1():
    return [("PUSH", 0, 1), ("PUSH", 1, 2), ("PUSH", 2, 3), ("TOP", 3),
            ("POP", 3), ("TOP", 4), ("PUSH", 2, 99), ("TOP", 5),
            ("SIZE", 5), ("SIZE", 3)]


def gen_visible_2():
    # branch heavily off version 0 and version produced early
    return [("PUSH", 0, 10), ("PUSH", 1, 20), ("PUSH", 0, 30),
            ("TOP", 1), ("TOP", 2), ("TOP", 3), ("SIZE", 2),
            ("POP", 2), ("TOP", 4), ("SIZE", 4), ("SIZE", 2)]


def gen_hidden_random(seed):
    rng = random.Random(seed)
    ops = []
    version_sizes = {0: 0}
    next_id = 1
    for _ in range(rng.randint(60, 200)):
        v = rng.choice(list(version_sizes.keys()))
        c = rng.random()
        if c < 0.55:
            ops.append(("PUSH", v, rng.randint(-999, 999)))
            version_sizes[next_id] = version_sizes[v] + 1
            next_id += 1
        elif c < 0.75 and version_sizes[v] > 0:
            ops.append(("POP", v))
            version_sizes[next_id] = version_sizes[v] - 1
            next_id += 1
        elif version_sizes[v] > 0 and c < 0.9:
            ops.append(("TOP", v))
        else:
            ops.append(("SIZE", v))
    return ops


def gen_hidden_deep_branch_perf(depth=40000, branches=4000):
    """Build one very deep chain (depth pushes off version 0), then take
    a large number of independent branches off an EARLY version and
    push once on each -- a solution that copies the whole stack on
    push, or on version lookup, blows up here; true structural sharing
    handles it easily."""
    ops = [("PUSH", 0, 1)]
    for i in range(1, depth):
        ops.append(("PUSH", i, i))
    # version `depth` now has size `depth`. Branch off version 5 (shallow)
    # `branches` times.
    for i in range(branches):
        ops.append(("PUSH", 5, i))
    ops.append(("SIZE", depth))
    ops.append(("SIZE", depth + branches))
    return ops


def gen_hidden_reuse_stress(seed):
    """Repeatedly reuse the SAME old version to fork many short-lived
    branches, verifying it is never mutated in the process."""
    rng = random.Random(seed)
    ops = [("PUSH", 0, 1), ("PUSH", 1, 2), ("PUSH", 2, 3)]  # version 3: [1,2,3]
    for _ in range(2000):
        ops.append(("PUSH", 3, rng.randint(0, 9)))
        ops.append(("TOP", 3))
        ops.append(("SIZE", 3))
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
        print(f"[{name:30s}] TLE               weight={weight:3d} -> 0/{weight}")
        return 0
    if status == "RE":
        print(f"[{name:30s}] RE ({payload})   weight={weight:3d} -> 0/{weight}")
        return 0
    if payload == expected:
        print(f"[{name:30s}] AC ({elapsed:5.2f}s)      weight={weight:3d} -> {weight}/{weight}")
        return weight
    print(f"[{name:30s}] WA ({elapsed:5.2f}s)      weight={weight:3d} -> 0/{weight}")
    return 0


def main():
    total, max_total = 0, 0
    tests = [("visible_basic_branching", gen_visible_1(), 8, TIME_LIMIT),
             ("visible_multi_branch", gen_visible_2(), 8, TIME_LIMIT)]
    for i in range(1, 8):
        tests.append((f"hidden_random_{i}", gen_hidden_random(2000 + i), 6, TIME_LIMIT))
    tests.append(("hidden_reuse_stress", gen_hidden_reuse_stress(5), 10, TIME_LIMIT))
    tests.append(("hidden_deep_branch_perf", gen_hidden_deep_branch_perf(40000, 4000), 32, LARGE_TIME_LIMIT))

    for name, ops, weight, tl in tests:
        max_total += weight
        total += check(name, ops, weight, tl)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
