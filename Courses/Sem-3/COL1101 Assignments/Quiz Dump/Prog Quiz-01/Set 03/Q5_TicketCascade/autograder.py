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


class _RefProc:
    __slots__ = ("pid", "remaining", "level", "finished")

    def __init__(self, pid, burst):
        self.pid = pid
        self.remaining = burst
        self.level = 0
        self.finished = False


class _RefScheduler:
    def __init__(self, num_levels, base_quantum):
        self.levels = [deque() for _ in range(num_levels)]
        self.base_quantum = base_quantum
        self.procs = {}
        self.active = 0

    def arrive(self, pid, burst):
        p = _RefProc(pid, burst)
        self.procs[pid] = p
        self.levels[0].append(pid)
        self.active += 1

    def step(self):
        for lvl, q in enumerate(self.levels):
            if q:
                pid = q.popleft()
                p = self.procs[pid]
                quantum = self.base_quantum * (2 ** lvl)
                run_time = min(p.remaining, quantum)
                p.remaining -= run_time
                if p.remaining == 0:
                    p.finished = True
                    self.active -= 1
                    return "DONE", pid
                else:
                    newlvl = lvl + 1 if lvl < len(self.levels) - 1 else lvl
                    p.level = newlvl
                    self.levels[newlvl].append(pid)
                    return "CONTINUE", pid
        return "IDLE", None

    def status(self, pid):
        if pid not in self.procs:
            return "UNKNOWN"
        p = self.procs[pid]
        if p.finished:
            return "DONE"
        return str(p.level)

    def count_active(self):
        return self.active


def _run_reference(num_levels, base_quantum, ops):
    s = _RefScheduler(num_levels, base_quantum)
    out = []
    for op in ops:
        if op[0] == "ARRIVE":
            s.arrive(op[1], op[2])
        elif op[0] == "RUN":
            kind, pid = s.step()
            out.append("IDLE" if kind == "IDLE" else f"{pid} {kind}")
        elif op[0] == "STATUS":
            r = s.status(op[1])
            out.append(r if r in ("UNKNOWN", "DONE") else f"LEVEL {r}")
        elif op[0] == "COUNT":
            out.append(str(s.count_active()))
    return "\n".join(out)


def _ops_to_text(num_levels, base_quantum, ops):
    lines = [f"{num_levels} {base_quantum} {len(ops)}"]
    for op in ops:
        lines.append(" ".join(str(t) for t in op))
    return "\n".join(lines) + "\n"


def gen_visible_1():
    nl, bq = 3, 2
    ops = [("ARRIVE", 1, 5), ("ARRIVE", 2, 3), ("RUN",), ("RUN",), ("RUN",),
           ("STATUS", 1), ("STATUS", 2), ("RUN",), ("RUN",), ("COUNT",)]
    return nl, bq, ops


def gen_visible_2():
    nl, bq = 2, 1
    ops = [("ARRIVE", 10, 1), ("ARRIVE", 20, 4), ("RUN",), ("RUN",), ("RUN",),
           ("RUN",), ("RUN",), ("RUN",), ("RUN",), ("STATUS", 10), ("STATUS", 20),
           ("STATUS", 999)]
    return nl, bq, ops


def gen_hidden_random(seed):
    rng = random.Random(seed)
    nl = rng.randint(2, 5)
    bq = rng.randint(1, 3)
    ops = []
    next_pid = 1
    live_pids = []
    for _ in range(rng.randint(80, 250)):
        c = rng.random()
        if c < 0.3:
            ops.append(("ARRIVE", next_pid, rng.randint(1, 40)))
            live_pids.append(next_pid)
            next_pid += 1
        elif c < 0.8:
            ops.append(("RUN",))
        elif c < 0.9 and live_pids:
            ops.append(("STATUS", rng.choice(live_pids)))
        else:
            ops.append(("COUNT",))
    return nl, bq, ops


def gen_hidden_last_level_roundrobin(seed):
    """Push everything to the deepest level quickly with tiny bursts on
    a single level, then verify round-robin cycling there forever."""
    nl, bq = 1, 1
    ops = [("ARRIVE", i, 5) for i in range(1, 6)]
    ops += [("RUN",)] * 30
    ops.append(("COUNT",))
    return nl, bq, ops


def gen_hidden_perf(n=60000):
    nl, bq = 4, 2
    ops = []
    for i in range(1, n // 3 + 1):
        ops.append(("ARRIVE", i, (i % 17) + 1))
    for _ in range(n):
        ops.append(("RUN",))
    return nl, bq, ops


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


def check(name, nl, bq, ops, weight, time_limit=TIME_LIMIT):
    expected = _run_reference(nl, bq, ops)
    status, payload, elapsed = run_student(_ops_to_text(nl, bq, ops), time_limit)
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
    tests = [("visible_basic_demotion", *gen_visible_1(), 8, TIME_LIMIT),
             ("visible_quantum_finish", *gen_visible_2(), 8, TIME_LIMIT)]
    for i in range(1, 9):
        tests.append((f"hidden_random_{i}", *gen_hidden_random(1200 + i), 6, TIME_LIMIT))
    tests.append(("hidden_last_level_rr", *gen_hidden_last_level_roundrobin(3), 12, TIME_LIMIT))
    tests.append(("hidden_perf_smoke_60k", *gen_hidden_perf(60000), 24, LARGE_TIME_LIMIT))

    for name, nl, bq, ops, weight, tl in tests:
        max_total += weight
        total += check(name, nl, bq, ops, weight, tl)

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
