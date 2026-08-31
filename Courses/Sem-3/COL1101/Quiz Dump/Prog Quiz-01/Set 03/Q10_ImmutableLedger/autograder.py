import random
import subprocess
import sys
import time
import os

TIME_LIMIT = 4.0
LARGE_TIME_LIMIT = 5.0
CONC_TIME_LIMIT = 8.0
HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(HERE, "student_code.py")


# ---------------------------------------------------------------------
# An independent, efficient (O(log n)) reference implementation of the
# same trie, used ONLY to compute expected answers quickly enough to
# grade the large branching-performance test.
# ---------------------------------------------------------------------
def _ref_insert(root, height, i, x):
    if height == 0:
        return x
    half = 1 << (height - 1)
    left, right = root if root is not None else (None, None)
    if i < half:
        return (_ref_insert(left, height - 1, i, x), right)
    else:
        return (left, _ref_insert(right, height - 1, i - half, x))


def _ref_lookup(root, height, i):
    if height == 0:
        return root
    half = 1 << (height - 1)
    left, right = root
    if i < half:
        return _ref_lookup(left, height - 1, i)
    return _ref_lookup(right, height - 1, i - half)


class _RefV:
    __slots__ = ("root", "height", "size")

    def __init__(self, root, height, size):
        self.root = root
        self.height = height
        self.size = size


REF_EMPTY = _RefV(None, 0, 0)


def _ref_append(v, x):
    capacity = 1 << v.height
    if v.size < capacity:
        return _RefV(_ref_insert(v.root, v.height, v.size, x), v.height, v.size + 1)
    newheight = v.height + 1
    combined = (v.root, None)
    newroot = _ref_insert(combined, newheight, v.size, x)
    return _RefV(newroot, newheight, v.size + 1)


def _ref_set(v, i, x):
    return _RefV(_ref_insert(v.root, v.height, i, x), v.height, v.size)


def _ref_get(v, i):
    return _ref_lookup(v.root, v.height, i)


def _run_reference(ops):
    versions = {0: REF_EMPTY}
    next_id = 1
    out = []
    for op in ops:
        if op[0] == "APPEND":
            v, x = op[1], op[2]
            versions[next_id] = _ref_append(versions[v], x)
            out.append(str(next_id))
            next_id += 1
        elif op[0] == "SET":
            v, i, x = op[1], op[2], op[3]
            versions[next_id] = _ref_set(versions[v], i, x)
            out.append(str(next_id))
            next_id += 1
        elif op[0] == "GET":
            v, i = op[1], op[2]
            out.append(str(_ref_get(versions[v], i)))
        elif op[0] == "SIZE":
            out.append(str(versions[op[1]].size))
    return "\n".join(out)


def _ops_to_text(ops):
    lines = [str(len(ops))]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


def gen_visible_1():
    return [("APPEND", 0, 10), ("APPEND", 1, 20), ("APPEND", 2, 30),
            ("GET", 3, 0), ("GET", 3, 1), ("GET", 3, 2), ("SIZE", 3),
            ("SET", 3, 1, 99), ("GET", 4, 1), ("GET", 3, 1), ("SIZE", 4)]


def gen_visible_2():
    ops = [("APPEND", 0, i) for i in range(9)]
    ops += [("GET", 9, k) for k in range(9)]
    ops += [("SIZE", 9), ("SET", 9, 0, -1), ("GET", 10, 0), ("GET", 9, 0)]
    return ops


def gen_hidden_random(seed):
    rng = random.Random(seed)
    ops = []
    version_size = {0: 0}
    next_id = 1
    for _ in range(rng.randint(80, 250)):
        v = rng.choice(list(version_size.keys()))
        c = rng.random()
        if c < 0.55:
            ops.append(("APPEND", v, rng.randint(-999, 999)))
            version_size[next_id] = version_size[v] + 1
            next_id += 1
        elif c < 0.8 and version_size[v] > 0:
            i = rng.randrange(version_size[v])
            ops.append(("SET", v, i, rng.randint(-999, 999)))
            version_size[next_id] = version_size[v]
            next_id += 1
        elif version_size[v] > 0 and c < 0.93:
            i = rng.randrange(version_size[v])
            ops.append(("GET", v, i))
        else:
            ops.append(("SIZE", v))
    return ops


def gen_hidden_growth_boundary():
    """Cross several power-of-two capacity boundaries (1, 2, 4, 8, 16,
    ...) exactly, and check GET on every element immediately after
    each crossing -- this is where an off-by-one in the height-growth
    logic breaks."""
    ops = [("APPEND", 0, 0)]
    for i in range(1, 40):
        ops.append(("APPEND", i, i))
    for k in range(40):
        ops.append(("GET", 40, k))
    ops.append(("SIZE", 40))
    return ops


def gen_hidden_deep_branch_perf(depth=15000, branches=3000):
    ops = [("APPEND", 0, 1)]
    for i in range(1, depth):
        ops.append(("APPEND", i, i))
    for i in range(branches):
        ops.append(("APPEND", 5, i))
    ops.append(("SIZE", depth))
    ops.append(("GET", depth, depth - 1))
    ops.append(("SIZE", depth + branches))
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
        print(f"[{name:32s}] TLE               weight={weight:3d} -> 0/{weight}")
        return 0
    if status == "RE":
        print(f"[{name:32s}] RE ({payload})   weight={weight:3d} -> 0/{weight}")
        return 0
    if payload == expected:
        print(f"[{name:32s}] AC ({elapsed:5.2f}s)      weight={weight:3d} -> {weight}/{weight}")
        return weight
    print(f"[{name:32s}] WA ({elapsed:5.2f}s)      weight={weight:3d} -> 0/{weight}")
    return 0


# ---------------------------------------------------------------------
# Concurrency stress test (direct import, not the stdin protocol).
# ---------------------------------------------------------------------
HEADER = f"import sys; sys.path.insert(0, {HERE!r})\n"

SNIPPET_CONCURRENT_APPEND = HEADER + r'''
from student_code import Ledger
import threading

ledger = Ledger()
NUM_THREADS = 8
APPENDS_PER_THREAD = 300
TOTAL = NUM_THREADS * APPENDS_PER_THREAD

results_lock = threading.Lock()
new_ids = []

def worker(tid):
    local_ids = []
    for i in range(APPENDS_PER_THREAD):
        vid = ledger.append_to(0, tid * 100000 + i)
        local_ids.append(vid)
    with results_lock:
        new_ids.extend(local_ids)

threads = [threading.Thread(target=worker, args=(t,)) for t in range(NUM_THREADS)]
for t in threads: t.start()
for t in threads: t.join()

assert len(new_ids) == TOTAL, f"expected {TOTAL} successful appends, got {len(new_ids)}"
assert len(set(new_ids)) == TOTAL, "two concurrent append_to calls were handed the SAME new version id -- a race in the publish step"
assert sorted(new_ids) == list(range(1, TOTAL + 1)), "version ids are not exactly 1..TOTAL with no gaps or repeats"

# every one of these appended-from-version-0 vectors must have size 1
# and contain exactly the value that particular call appended.
for vid in new_ids:
    assert ledger.size(vid) == 1, f"version {vid} should have size 1"

print("OK")
'''

SNIPPET_CONCURRENT_READ_DURING_WRITE = HEADER + r'''
from student_code import Ledger
import threading

ledger = Ledger()
BASE_SIZE = 500
v = 0
expected = []
for i in range(BASE_SIZE):
    v = ledger.append_to(v, i * 3 + 1)
    expected.append(i * 3 + 1)
STABLE_VERSION = v

errors = []
errors_lock = threading.Lock()

def reader():
    for _ in range(4000):
        for idx in (0, BASE_SIZE // 2, BASE_SIZE - 1):
            got = ledger.get(STABLE_VERSION, idx)
            if got != expected[idx]:
                with errors_lock:
                    errors.append((idx, got, expected[idx]))

def writer():
    cur = STABLE_VERSION
    for i in range(3000):
        cur = ledger.append_to(cur, -i)

readers = [threading.Thread(target=reader) for _ in range(4)]
writers = [threading.Thread(target=writer) for _ in range(3)]
for t in readers + writers: t.start()
for t in readers + writers: t.join()

assert not errors, f"a stable, already-published version changed value under concurrent writes elsewhere: {errors[:3]}"
print("OK")
'''


def run_snippet(code, time_limit=CONC_TIME_LIMIT):
    try:
        result = subprocess.run([sys.executable, "-c", code], capture_output=True,
                                 text=True, timeout=time_limit)
        if result.returncode != 0:
            return "RE", (result.stderr.strip().splitlines() or ["error"])[-1]
        return "OK", result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TLE", None


def check_snippet(name, code, weight, time_limit=CONC_TIME_LIMIT):
    status, payload = run_snippet(code, time_limit)
    if status == "TLE":
        print(f"[{name:32s}] TLE               weight={weight:3d} -> 0/{weight}")
        return 0
    if status == "RE":
        print(f"[{name:32s}] RE ({payload})   weight={weight:3d} -> 0/{weight}")
        return 0
    if payload.startswith("OK"):
        print(f"[{name:32s}] AC               weight={weight:3d} -> {weight}/{weight}")
        return weight
    print(f"[{name:32s}] WA ({payload})   weight={weight:3d} -> 0/{weight}")
    return 0


def main():
    total, max_total = 0, 0
    tests = [("visible_basic_trie", gen_visible_1(), 6, TIME_LIMIT),
             ("visible_capacity_growth", gen_visible_2(), 6, TIME_LIMIT)]
    for i in range(1, 7):
        tests.append((f"hidden_random_{i}", gen_hidden_random(5500 + i), 4, TIME_LIMIT))
    tests.append(("hidden_growth_boundaries", gen_hidden_growth_boundary(), 10, TIME_LIMIT))
    tests.append(("hidden_deep_branch_perf", gen_hidden_deep_branch_perf(15000, 3000), 18, LARGE_TIME_LIMIT))

    for name, ops, weight, tl in tests:
        max_total += weight
        total += check(name, ops, weight, tl)

    max_total += 16
    total += check_snippet("hidden_concurrent_unique_ids", SNIPPET_CONCURRENT_APPEND, 16)
    max_total += 20
    total += check_snippet("hidden_concurrent_read_stability", SNIPPET_CONCURRENT_READ_DURING_WRITE, 20)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
