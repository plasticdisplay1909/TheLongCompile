import os
import sys
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import harness  # noqa: E402

REF = os.path.join(HERE, "reference_solution.py")
STUDENT = os.path.join(HERE, "student_code.py")


def make_input(polys, words, queries):
    lines = [str(len(polys))]
    for name, coeffs in polys:
        lines.append(name + " " + " ".join(str(c) for c in coeffs))
    lines.append(str(len(words)))
    for name, body in words:
        lines.append(name + " " + " ".join(str(t) for t in body))
    lines.append(str(len(queries)))
    for qtoks in queries:
        lines.append(" ".join(str(t) for t in qtoks))
    return "\n".join(lines) + "\n"


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
    polys = [("f", [0, 0, 1]), ("g", [0, 1])]
    words = [("double", [2, "scale"])]
    q = [
        ["f", "g", "+"],
        ["f", "deriv"],
        ["f", 3, "eval"],
        ["g", "integ"],
        ["f", "double"],
    ]
    cases.append(harness.TestCase("basic ops + one word", make_input(polys, words, q), None, weight=2.0))

    polys = [("h", [5])]
    q = [["h", "deriv"], ["h", 0, "eval"], ["h", -3, "eval"]]
    cases.append(harness.TestCase("constant polynomial edge cases", make_input(polys, [], q), None, weight=1.5))

    polys = [("a", [1, 2, 3]), ("b", [4, 5])]
    q = [["a", "b", "-"], ["b", "a", "-"]]
    cases.append(harness.TestCase("subtraction is not commutative", make_input(polys, [], q), None, weight=1.5))

    polys = [("p", [0, 0, 0, 2])]  # 2x^3
    words = [("second_deriv", ["deriv", "deriv"]), ("fourth_deriv", ["second_deriv", "second_deriv"])]
    q = [["p", "second_deriv"], ["p", "fourth_deriv"]]
    cases.append(harness.TestCase("nested words", make_input(polys, words, q), None, weight=2.5))

    polys = [("z", [0, 0, 0])]  # trims to zero poly
    q = [["z", "deriv"], ["z", 100, "eval"], ["z", "integ"]]
    cases.append(harness.TestCase("all-zero polynomial trims to []", make_input(polys, [], q), None, weight=1.5))

    # ---------- HIDDEN ----------
    polys = [("u", [1, 1])]  # 1 + x, integral has an odd denominator later
    q = [["u", "integ"], ["u", "integ", "integ"]]
    cases.append(harness.TestCase("repeated integration -> fractions", make_input(polys, [], q), None, weight=2.0, hidden=True))

    polys = [("v", [3, -2, 1])]  # 3 -2x + x^2
    q = [["v", -1, "eval"], ["v", "v", "-"], ["v", 0, "scale"]]
    cases.append(harness.TestCase("negative coefficients & self-subtraction", make_input(polys, [], q), None, weight=2.0, hidden=True))

    polys = [("w", [0, 1])]
    words = [("triple", [3, "scale"]), ("hexed", ["triple", "double"]), ("double", [2, "scale"])]
    q = [["w", "hexed"]]
    cases.append(harness.TestCase("word calling a word defined later in the registry", make_input(polys, words, q), None, weight=2.5, hidden=True))

    polys = [("k1", [10]), ("k2", [-10])]
    q = [["k1", "k2", "+"], ["k1", "k2", "+", "deriv"]]
    cases.append(harness.TestCase("polys that cancel to zero", make_input(polys, [], q), None, weight=1.5, hidden=True))

    polys = [("m", [0, 0, 1])]  # x^2
    words = [("area_to", ["integ", "eval"])]  # note: this word expects x already under the poly? test misuse-safe design
    q = [["m", "integ", 3, "eval"]]
    cases.append(harness.TestCase("integ then eval composed manually", make_input(polys, [], q), None, weight=2.0, hidden=True))

    rng = random.Random(11)
    polys = [(f"P{i}", [rng.randint(-5, 5) for _ in range(rng.randint(1, 4))]) for i in range(10)]
    words = [("d2", ["deriv", "deriv"]), ("neg1", [-1, "scale"])]
    q = []
    names = [p[0] for p in polys]
    for _ in range(40):
        a, b = rng.choice(names), rng.choice(names)
        op = rng.choice(["+", "-"])
        q.append([a, b, op])
    for n in names:
        q.append([n, "d2"])
        q.append([n, "neg1"])
        q.append([n, rng.randint(-3, 3), "eval"])
    cases.append(harness.TestCase("randomized mixed-op stress", make_input(polys, words, q), None, weight=3.0, hidden=True))

    # a deeply nested word chain forcing genuine recursion through step()
    polys = [("s", [0, 1])]
    words = [("lvl1", ["deriv"])]
    for i in range(2, 15):
        words.append((f"lvl{i}", [f"lvl{i-1}", f"lvl{i-1}"]))
    # lvl14 applies 2^13 derivatives -- far more executed steps than tokens
    q = [["s", "lvl3"]]  # keep small enough to have a nonzero/defined answer but still deep
    cases.append(harness.TestCase("deep word recursion", make_input(polys, words, q), None, weight=2.5, hidden=True))

    # large flat program: many tokens, no recursion depth issue, but tests
    # that reduce_ doesn't blow up the Python call stack on a long flat list
    polys = [("t", [1, 1, 1])]
    q = [["t"] + ["1", "scale"] * 3000]
    cases.append(harness.TestCase("long flat token stream (recursion depth)", make_input(polys, [], q), None, weight=2.5, hidden=True, timeout=10.0))

    # fill in expected outputs
    for tc in cases:
        tc.expected_output = expected_of(tc.stdin_text)
    return cases


if __name__ == "__main__":
    cases = build_cases()
    harness.grade(STUDENT, cases, title="Q2 -- Postfix over Polynomials -- Autograder Report")
