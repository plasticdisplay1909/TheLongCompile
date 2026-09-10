import os
import sys
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import harness  # noqa: E402

REF = os.path.join(HERE, "reference_solution.py")
STUDENT = os.path.join(HERE, "student_code.py")


def make_input(B, cmds):
    return f"{B}\n{len(cmds)}\n" + "\n".join(cmds) + "\n"


def expected_of(stdin_text, timeout=40):
    result = subprocess.run(
        [sys.executable, REF], input=stdin_text, capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError("reference_solution.py crashed:\n" + result.stderr)
    return result.stdout


def build_cases():
    cases = []

    # ---------- VISIBLE ----------
    cmds = ["CREATE 0 D1 3 0.5 0 0 0 0", "UPDATE 0 D1 2 0",
            "STATUS 1 D1", "STATUS 2 D1"]
    cases.append(harness.TestCase("overspeed self-destruction", make_input(1000, cmds), None, weight=2.0))

    cmds = ["CREATE 0 D2 100 0.1 0 0 5 0", "STATUS 1 D2", "STATUS 3 D2"]
    cases.append(harness.TestCase("boundary breach at constant velocity", make_input(10, cmds), None, weight=2.0))

    cmds = ["CREATE 0 D3 100 1 -5 0 1 0", "CREATE 0 D4 100 1 5 0 -1 0",
            "STATUS 3 D3", "STATUS 5 D3", "STATUS 5 D4"]
    cases.append(harness.TestCase("head-on collision, both destroyed", make_input(1000, cmds), None, weight=3.0))

    cmds = ["CREATE 0 SG55 3 0.01 0 0 0 0", "UPDATE 0 SG55 2 0",
            "CREATE 0 SG56 99 0.01 8 0 -2 0", "STATUS 1 SG55", "STATUS 2 SG55", "STATUS 3 SG56"]
    cases.append(harness.TestCase("self-destruction removes a drone from a would-be collision", make_input(1000, cmds), None, weight=3.0))

    cmds = ["STATUS 0 ghost"]
    cases.append(harness.TestCase("querying a never-created id", make_input(10, cmds), None, weight=1.0))

    # ---------- HIDDEN ----------
    cmds = ["CREATE 0 E1 10 0.1 5 0 0 0", "STATUS 0 E1"]
    cases.append(harness.TestCase("created already touching the wall", make_input(5, cmds), None, weight=2.0, hidden=True))

    cmds = ["CREATE 0 E2 10 0.1 4.9 0 -1 0", "STATUS 3 E2"]
    cases.append(harness.TestCase("created just inside boundary, moving away", make_input(5, cmds), None, weight=1.5, hidden=True))

    cmds = ["CREATE 0 P 100 0.5 -10 0 2 0", "CREATE 0 Q 100 0.5 10 0 -2 0",
            "STATUS 4.74 P", "STATUS 4.76 P"]
    cases.append(harness.TestCase("collision timing precision (~0.02 window)", make_input(1000, cmds), None, weight=3.0, hidden=True))

    cmds = ["CREATE 0 A 5 1 0 0 0 0", "CREATE 0 B 5 1 10 0 0 0",
            "STATUS 5 A", "STATUS 5 B", "UPDATE 1 A 1 0", "STATUS 10 A"]
    cases.append(harness.TestCase("later acceleration causes a delayed collision/overspeed", make_input(1000, cmds), None, weight=2.5, hidden=True))

    # drone that self-destructs from overspeed, but AFTER an UPDATE call
    # that was itself sent past its destruction time -- the update must
    # be silently ignored
    cmds = ["CREATE 0 F1 2 0.1 0 0 0 0", "UPDATE 0 F1 5 0",
            "STATUS 10 F1", "UPDATE 20 F1 -5 0", "STATUS 30 F1"]
    cases.append(harness.TestCase("instruction sent to an already-destroyed drone is ignored", make_input(1000, cmds), None, weight=2.5, hidden=True))

    # three drones where the two closest collide, leaving the third alone
    cmds = ["CREATE 0 G1 100 1 0 0 1 0", "CREATE 0 G2 100 1 4 0 -1 0",
            "CREATE 0 G3 100 1 100 100 0 0",
            "STATUS 5 G1", "STATUS 5 G2", "STATUS 5 G3"]
    cases.append(harness.TestCase("bystander drone unaffected by a nearby collision", make_input(1000, cmds), None, weight=2.5, hidden=True))

    # diagonal boundary breach via the y-axis specifically
    cmds = ["CREATE 0 H1 100 0.1 0 0 0 4", "STATUS 1 H1", "STATUS 3 H1"]
    cases.append(harness.TestCase("boundary breach on the y-axis", make_input(10, cmds), None, weight=2.0, hidden=True))

    # acceleration that curves a drone away from an apparent collision
    cmds = ["CREATE 0 K1 100 0.5 -5 0 1 0", "CREATE 0 K2 100 0.5 5 0 -1 0",
            "UPDATE 1 K1 0 3", "STATUS 10 K1", "STATUS 10 K2"]
    cases.append(harness.TestCase("acceleration curves a drone out of a collision course", make_input(1000, cmds), None, weight=3.0, hidden=True))

    # a modest multi-drone randomized scenario (kept small deliberately --
    # this problem is about correctness under continuous time, not raw
    # scale)
    rng = random.Random(4)
    n_drones, n_q = 8, 40
    cmds = []
    for i in range(n_drones):
        x, y = rng.uniform(-60, 60), rng.uniform(-60, 60)
        vx, vy = rng.uniform(-3, 3), rng.uniform(-3, 3)
        cmds.append(f"CREATE 0 R{i} 15 1 {x:.2f} {y:.2f} {vx:.2f} {vy:.2f}")
    tail = []
    for _ in range(n_q):
        t = rng.uniform(0.5, 30)
        did = f"R{rng.randint(0, n_drones-1)}"
        if rng.random() < 0.3:
            ax, ay = rng.uniform(-1, 1), rng.uniform(-1, 1)
            tail.append((t, f"UPDATE {t:.3f} {did} {ax:.2f} {ay:.2f}"))
        else:
            tail.append((t, f"STATUS {t:.3f} {did}"))
    tail.sort(key=lambda p: p[0])
    cmds += [c for _, c in tail]
    cases.append(harness.TestCase("randomized 8-drone / 40-instruction scenario", make_input(100, cmds), None,
                                   weight=4.0, hidden=True, timeout=20.0))

    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q10 -- Orbital Defense Grid -- Autograder Report")
