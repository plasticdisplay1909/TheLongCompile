import os
import sys
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import harness  # noqa: E402

REF = os.path.join(HERE, "reference_solution.py")
STUDENT = os.path.join(HERE, "student_code.py")


def make_input(cmds):
    return f"{len(cmds)}\n" + "\n".join(cmds) + "\n"


def expected_of(stdin_text):
    result = subprocess.run(
        [sys.executable, REF], input=stdin_text, capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError("reference_solution.py crashed:\n" + result.stderr)
    return result.stdout


def build_cases():
    cases = []

    # ---------- VISIBLE ----------
    cmds = [
        "CREATE_SAVINGS A1 Priya 1000 0.10 2",
        "CREATE_CURRENT A2 Rohan 500 200",
        "WITHDRAW A1 100",
        "WITHDRAW A1 100",
        "WITHDRAW A1 100",  # 3rd this month -> denied (limit 2)
        "STATUS A1",
        "TICK",
        "STATUS A1",
    ]
    cases.append(harness.TestCase("basic savings + interest", make_input(cmds), None, weight=1.5))

    cmds = [
        "CREATE_CURRENT B1 Meera 100 50",
        "WITHDRAW B1 150",   # exactly to -50, allowed
        "STATUS B1",
        "WITHDRAW B1 1",     # would go to -51, denied
        "STATUS B1",
    ]
    cases.append(harness.TestCase("overdraft boundary", make_input(cmds), None, weight=1.5))

    cmds = [
        "CREATE_SAVINGS S1 A 300 0.0 5",
        "CREATE_CURRENT S2 B 300 100",
        "CREATE_CURRENT S3 C 999 100",
        "TOP 2",
        "TOP 10",
    ]
    cases.append(harness.TestCase("TOP with ties", make_input(cmds), None, weight=1.5))

    cmds = [
        "CREATE_SAVINGS M1 A 100 0.0 5",
        "CREATE_CURRENT M2 B 250 0",
        "MERGE M1 M2",
        "STATUS M1",
        "STATUS M2",
        "DEPOSIT M2 50",
        "STATUS M2",
    ]
    cases.append(harness.TestCase("merge closes target", make_input(cmds), None, weight=2.0))

    cmds = [
        "CREATE_SAVINGS T1 A 500 0.0 1",
        "CREATE_CURRENT T2 B 0 500",
        "TRANSFER T1 T2 400",
        "TRANSFER T1 T2 50",   # savings withdrawal limit already used
        "STATUS T1",
        "STATUS T2",
    ]
    cases.append(harness.TestCase("transfer respects savings limit", make_input(cmds), None, weight=2.0))

    # ---------- HIDDEN ----------
    cmds = ["STATUS ghost", "TOP 5", "TOP 0", "TOP -3"]
    cases.append(harness.TestCase("empty bank edge cases", make_input(cmds), None, weight=1.0, hidden=True))

    cmds = [
        "CREATE_SAVINGS X1 A 1000 0.05 1",
        "WITHDRAW X1 10", "TICK",
        "WITHDRAW X1 10", "TICK",
        "WITHDRAW X1 10", "TICK",
        "STATUS X1",
    ]
    cases.append(harness.TestCase("limit resets every tick", make_input(cmds), None, weight=1.5, hidden=True))

    cmds = [
        "CREATE_CURRENT Y1 A 0 0",
        "WITHDRAW Y1 1", "STATUS Y1",
        "DEPOSIT Y1 1", "WITHDRAW Y1 1", "STATUS Y1",
    ]
    cases.append(harness.TestCase("zero overdraft account", make_input(cmds), None, weight=1.5, hidden=True))

    cmds = [
        "CREATE_SAVINGS Z1 A 100 0.0 3",
        "CREATE_CURRENT Z2 B 100 100",
        "MERGE Z1 Z2",
        "MERGE Z2 Z1",   # Z2 already closed -> no-op
        "MERGE Z1 Z1",   # same id -> no-op
        "STATUS Z1", "STATUS Z2",
    ]
    cases.append(harness.TestCase("merge idempotence / self-merge", make_input(cmds), None, weight=2.0, hidden=True))

    cmds = [
        "CREATE_SAVINGS L1 A 50 0.0 2",
        "TRANSFER L1 GHOST 10",   # target never existed
        "STATUS L1",
        "TRANSFER GHOST L1 10",
        "STATUS L1",
    ]
    cases.append(harness.TestCase("transfer with nonexistent endpoint", make_input(cmds), None, weight=1.5, hidden=True))

    cmds = [
        "CREATE_SAVINGS P1 A 100 0.2 10",
        "TICK", "TICK", "TICK",
        "STATUS P1",
    ]
    cases.append(harness.TestCase("compounding interest thrice", make_input(cmds), None, weight=1.5, hidden=True))

    # len()/transaction-log correctness
    cmds = [
        "CREATE_SAVINGS N1 A 500 0.0 5",
        "CREATE_CURRENT N2 B 500 500",
        "DEPOSIT N1 10", "WITHDRAW N1 5", "TRANSFER N1 N2 5",
        "WITHDRAW N1 999999",  # denied, must not count
        "STATUS N1",
    ]
    cases.append(harness.TestCase("transaction count only on success", make_input(cmds), None, weight=2.0, hidden=True))

    # equality / merge arithmetic precision
    cmds = [
        "CREATE_SAVINGS E1 A 10.10 0.0 5",
        "CREATE_CURRENT E2 B 20.20 0",
        "MERGE E1 E2",
        "STATUS E1",
    ]
    cases.append(harness.TestCase("float rounding on merge", make_input(cmds), None, weight=1.5, hidden=True))

    # a longer scripted scenario mixing everything
    rng = random.Random(42)
    cmds = []
    ids = []
    for i in range(30):
        if i % 2 == 0:
            cmds.append(f"CREATE_SAVINGS S{i} name{i} {rng.randint(0,1000)} 0.0{rng.randint(1,9)} {rng.randint(1,4)}")
        else:
            cmds.append(f"CREATE_CURRENT C{i} name{i} {rng.randint(0,1000)} {rng.randint(0,300)}")
        ids.append(("S" if i % 2 == 0 else "C") + str(i))
    for _ in range(200):
        op = rng.choice(["DEP", "WD", "TR", "TICK", "STAT", "TOP"])
        a = rng.choice(ids)
        b = rng.choice(ids)
        if op == "DEP":
            cmds.append(f"DEPOSIT {a} {rng.randint(1,200)}")
        elif op == "WD":
            cmds.append(f"WITHDRAW {a} {rng.randint(1,200)}")
        elif op == "TR":
            cmds.append(f"TRANSFER {a} {b} {rng.randint(1,200)}")
        elif op == "TICK":
            cmds.append("TICK")
        elif op == "STAT":
            cmds.append(f"STATUS {a}")
        else:
            cmds.append(f"TOP {rng.randint(1,10)}")
    cases.append(harness.TestCase("randomized 200-op stress scenario", make_input(cmds), None, weight=3.0, hidden=True))

    # large scale performance sanity check (not asymptotically tight, but
    # will catch egregiously quadratic per-operation mistakes)
    cmds = []
    ids = []
    for i in range(4000):
        cmds.append(f"CREATE_CURRENT K{i} n {1000+i} 100")
        ids.append(f"K{i}")
    rng2 = random.Random(7)
    for _ in range(4000):
        a, b = rng2.choice(ids), rng2.choice(ids)
        cmds.append(f"TRANSFER {a} {b} {rng2.randint(1,50)}")
    cmds.append("TOP 5")
    cases.append(harness.TestCase("large scale performance", make_input(cmds), None, weight=2.0, hidden=True, timeout=8.0))

    # fill in expected outputs
    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q1 -- The Multi-Branch CampusBank -- Autograder Report")
