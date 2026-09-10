import os
import sys
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import harness  # noqa: E402

REF = os.path.join(HERE, "reference_solution.py")
STUDENT = os.path.join(HERE, "student_code.py")


def make_input(p, lines):
    return f"{p}\n" + "\n".join(lines) + "\n"


def expected_of(stdin_text, timeout=30):
    result = subprocess.run(
        [sys.executable, REF], input=stdin_text, capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError("reference_solution.py crashed:\n" + result.stderr)
    return result.stdout


def gen_random_program(rng, max_depth, stmts_per_level, max_regs=6, max_loop=6):
    lines = []

    def gen_block(depth):
        for _ in range(stmts_per_level):
            kind = rng.choice(["add", "sub", "swap", "loop"] if depth < max_depth else ["add", "sub", "swap"])
            if kind == "loop":
                k = rng.randint(0, max_loop)
                lines.append(f"loop {k}")
                gen_block(depth + 1)
                lines.append("end")
            else:
                i, j = rng.randint(0, max_regs - 1), rng.randint(0, max_regs - 1)
                lines.append(f"{kind} r{i} r{j}")

    gen_block(0)
    return lines


def build_cases():
    cases = []

    # ---------- VISIBLE ----------
    cases.append(harness.TestCase("single add", make_input(1000000007, ["add r0 r1"]), None, weight=1.5))

    lines = ["loop 2", "add r0 r0", "end"]
    cases.append(harness.TestCase("simple doubling loop", make_input(1000000007, lines), None, weight=2.0))

    lines = ["add r0 r1", "loop 2", "add r1 r2", "end", "add r2 r0"]
    cases.append(harness.TestCase("sequential add + loop + add (matches worked trace style)",
                                   make_input(1000000007, lines), None, weight=2.5))

    lines = ["swap r0 r1"]
    cases.append(harness.TestCase("single swap is a permutation matrix", make_input(1000000007, lines), None, weight=1.5))

    lines = ["loop 2", "loop 3", "add r0 r1", "end", "end"]
    cases.append(harness.TestCase("nested loops multiply iteration counts", make_input(1000000007, lines), None, weight=2.5))

    # ---------- HIDDEN ----------
    lines = ["loop 0", "add r0 r1", "end", "add r1 r2"]
    cases.append(harness.TestCase("loop 0 executes body zero times", make_input(1000000007, lines), None, weight=2.0, hidden=True))

    lines = ["sub r0 r1", "sub r0 r1", "sub r0 r1"]
    cases.append(harness.TestCase("repeated sub accumulates negative coefficient (mod p)", make_input(97, lines), None, weight=1.5, hidden=True))

    lines = ["swap r0 r1", "swap r1 r2", "swap r0 r2"]
    cases.append(harness.TestCase("chained swaps compose into a 3-cycle", make_input(1000000007, lines), None, weight=2.0, hidden=True))

    lines = ["loop 5", "swap r0 r1", "end"]  # odd number of swaps -> still swapped
    cases.append(harness.TestCase("looped swap: parity matters", make_input(1000000007, lines), None, weight=2.0, hidden=True))

    lines = ["loop 4", "swap r0 r1", "end"]  # even -> identity again
    cases.append(harness.TestCase("looped swap an even number of times cancels", make_input(1000000007, lines), None, weight=2.0, hidden=True))

    lines = ["add r0 r1", "loop 3", "add r0 r0", "sub r1 r2", "end", "swap r2 r3"]
    cases.append(harness.TestCase("mixed ops inside and outside a loop", make_input(1000000007, lines), None, weight=2.5, hidden=True))

    # small prime modulus, exercises the mod arithmetic more visibly
    lines = ["loop 10", "add r0 r0", "end"]  # r0 *= 2^10 = 1024
    cases.append(harness.TestCase("power-of-two doubling under a small prime modulus", make_input(13, lines), None, weight=2.0, hidden=True))

    rng = random.Random(101)
    for k in range(3):
        lines = gen_random_program(random.Random(200 + k), max_depth=3, stmts_per_level=4, max_loop=5)
        cases.append(harness.TestCase(f"randomized nested program #{k+1}", make_input(1000000007, lines), None,
                                       weight=2.5, hidden=True))

    # ---------- PERFORMANCE / TLE TRAPS ----------
    # a loop count so large that literally executing the body that many
    # times is impossible; only matrix exponentiation survives.
    lines = ["loop 1000000000000000", "add r0 r0", "end"]
    cases.append(harness.TestCase("PERF: loop count of 10^15 (must use fast exponentiation)",
                                   make_input(1000000007, lines), None, weight=4.0, hidden=True, timeout=5.0))

    # deep nesting that multiplies to an astronomically large effective
    # iteration count (2^30), while the PROGRAM TEXT itself stays tiny --
    # only a genuinely recursive/stacked handling of nested loops (never
    # literal unrolling) can possibly finish.
    lines = []
    depth = 30
    for _ in range(depth):
        lines.append("loop 2")
    lines.append("add r0 r1")
    for _ in range(depth):
        lines.append("end")
    cases.append(harness.TestCase("PERF: 30 nested loop-2 blocks (2^30 effective iterations)",
                                   make_input(1000000007, lines), None, weight=4.0, hidden=True, timeout=5.0))

    # a longer, wider random program (many statements, moderate nesting,
    # large-ish loop counts) to catch anything accidentally quadratic in
    # the number of *lines* of the program itself.
    lines = gen_random_program(random.Random(999), max_depth=4, stmts_per_level=30, max_loop=50000)
    cases.append(harness.TestCase("PERF: wide randomized program with large loop counts",
                                   make_input(1000000007, lines), None, weight=3.0, hidden=True, timeout=5.0))

    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q9 -- The Ouroboros Machine -- Autograder Report")
