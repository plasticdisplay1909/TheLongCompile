import random
import subprocess
import sys
import time
import os
import bisect

TIME_LIMIT = 4.0
LARGE_TIME_LIMIT = 5.0
HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(HERE, "student_code.py")


class _Fenwick:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def prefix(self, i):
        # sum of indices [0, i] inclusive (0-indexed)
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def total(self):
        return self.prefix(self.n - 1) if self.n > 0 else 0

    def find_kth(self, k):
        """1-indexed k-th smallest present element's compressed index."""
        pos = 0
        remaining = k
        logn = self.n.bit_length()
        bitmask = 1 << logn
        while bitmask > 0:
            nxt = pos + bitmask
            if nxt <= self.n and self.tree[nxt] < remaining:
                pos = nxt
                remaining -= self.tree[nxt]
            bitmask >>= 1
        return pos  # 0-indexed compressed coordinate of the k-th element


def _run_reference(ops):
    all_keys = sorted(set(op[1] for op in ops if len(op) > 1))
    fen = _Fenwick(len(all_keys))
    counts = {}
    out = []
    for op in ops:
        if op[0] == "INSERT":
            x = op[1]
            i = bisect.bisect_left(all_keys, x)
            fen.update(i, 1)
            counts[x] = counts.get(x, 0) + 1
        elif op[0] == "DELETE":
            x = op[1]
            if counts.get(x, 0) > 0:
                i = bisect.bisect_left(all_keys, x)
                fen.update(i, -1)
                counts[x] -= 1
        elif op[0] == "COUNT":
            out.append(str(counts.get(op[1], 0)))
        elif op[0] == "KTH":
            k = op[1]
            i = fen.find_kth(k)
            out.append(str(all_keys[i]))
        elif op[0] == "RANK":
            x = op[1]
            i = bisect.bisect_left(all_keys, x)
            out.append(str(fen.prefix(i - 1) if i > 0 else 0))
        elif op[0] == "SIZE":
            out.append(str(fen.total()))
    return "\n".join(out)


def _ops_to_text(ops):
    lines = [str(len(ops))]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


def gen_visible_1():
    return [("INSERT", 5), ("INSERT", 2), ("INSERT", 8), ("INSERT", 2),
            ("COUNT", 2), ("KTH", 1), ("KTH", 2), ("KTH", 3), ("KTH", 4),
            ("RANK", 5), ("RANK", 8), ("RANK", 1), ("DELETE", 2),
            ("COUNT", 2), ("KTH", 2), ("SIZE",)]


def gen_visible_2():
    ops = [("INSERT", v) for v in [10, 10, 10, 20, 20, 30]]
    ops += [("RANK", 10), ("RANK", 20), ("RANK", 30), ("RANK", 5), ("RANK", 100)]
    ops += [("DELETE", 10), ("DELETE", 10), ("DELETE", 10), ("DELETE", 10)]
    ops += [("COUNT", 10), ("KTH", 1), ("SIZE",)]
    return ops


def gen_hidden_random(seed):
    rng = random.Random(seed)
    ops = []
    present = {}
    total = 0
    keyspace = list(range(-200, 200))
    for _ in range(rng.randint(100, 400)):
        c = rng.random()
        x = rng.choice(keyspace)
        if c < 0.45:
            ops.append(("INSERT", x)); present[x] = present.get(x, 0) + 1; total += 1
        elif c < 0.65 and total > 0:
            ops.append(("DELETE", x))
            if present.get(x, 0) > 0:
                present[x] -= 1; total -= 1
        elif c < 0.75:
            ops.append(("COUNT", x))
        elif c < 0.85 and total > 0:
            ops.append(("RANK", x))
        elif total > 0:
            k = rng.randint(1, total)
            ops.append(("KTH", k))
        else:
            ops.append(("SIZE",))
    return ops


def gen_hidden_sorted_order_stress(n=6000):
    """Insert already-sorted (ascending) keys -- the classic case that
    turns a plain unbalanced BST into a straight line of depth n,
    making every subsequent operation O(n) instead of O(log n). A
    treap with random priorities must not degrade here."""
    ops = [("INSERT", i) for i in range(n)]
    for i in range(0, n, 7):
        ops.append(("KTH", i + 1))
        ops.append(("RANK", i))
    for i in range(0, n, 11):
        ops.append(("DELETE", i))
    ops.append(("SIZE",))
    return ops


def gen_hidden_duplicates_stress(seed, n=4000):
    rng = random.Random(seed)
    ops = []
    for _ in range(n):
        ops.append(("INSERT", rng.randint(0, 30)))  # heavy duplication, 31 distinct values
    for _ in range(n // 2):
        ops.append(("DELETE", rng.randint(0, 30)))
    ops.append(("SIZE",))
    for v in range(31):
        ops.append(("COUNT", v))
    return ops


def gen_hidden_perf(n=120000):
    rng = random.Random(777)
    ops = []
    for i in range(n):
        ops.append(("INSERT", rng.randint(0, 10**9)))
    for i in range(n // 4):
        ops.append(("KTH", rng.randint(1, n)))
    for i in range(n // 4):
        ops.append(("RANK", rng.randint(0, 10**9)))
    for i in range(n // 8):
        ops.append(("DELETE", rng.randint(0, 10**9)))
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


def main():
    total, max_total = 0, 0
    tests = [("visible_basic_multiset", gen_visible_1(), 6, TIME_LIMIT),
             ("visible_bulk_duplicates", gen_visible_2(), 6, TIME_LIMIT)]
    for i in range(1, 8):
        tests.append((f"hidden_random_{i}", gen_hidden_random(3000 + i), 5, TIME_LIMIT))
    tests.append(("hidden_duplicates_stress", gen_hidden_duplicates_stress(9), 8, TIME_LIMIT))
    tests.append(("hidden_sorted_order_balance", gen_hidden_sorted_order_stress(6000), 25, TIME_LIMIT))
    tests.append(("hidden_perf_smoke_120k", gen_hidden_perf(120000), 20, LARGE_TIME_LIMIT))

    for name, ops, weight, tl in tests:
        max_total += weight
        total += check(name, ops, weight, tl)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
