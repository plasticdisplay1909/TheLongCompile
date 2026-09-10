import sys
sys.setrecursionlimit(20000)

# A polynomial is an immutable tuple of ints (c0, c1, c2, ...) meaning
# c0 + c1*x + c2*x^2 + ...  (low degree first). The zero polynomial is ().


def is_poly(v):
    return isinstance(v, tuple)


def _trim(coeffs):
    coeffs = list(coeffs)
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    return tuple(coeffs)


def reduce_(function, iterable, initial):
    it = iter(iterable)

    def helper(acc, i):
        try:
            item = next(i)
        except StopIteration:
            return acc
        return helper(function(acc, item), i)

    return helper(initial, it)


def poly_add(a, b):
    def helper(a, b):
        if not a:
            return b
        if not b:
            return a
        return (a[0] + b[0],) + helper(a[1:], b[1:])
    return _trim(helper(a, b))


def poly_neg(a):
    return tuple(-c for c in a)


def poly_sub(a, b):
    return poly_add(a, poly_neg(b))


def poly_scale(a, k):
    return _trim(tuple(c * k for c in a))


def poly_deriv(a):
    if len(a) <= 1:
        return ()
    return _trim(tuple(c * i for i, c in enumerate(a) if i >= 1))


def poly_integ(a):
    # antiderivative with constant term 0
    return _trim((0,) + tuple(_rat(c, i + 1) for i, c in enumerate(a)))


def _rat(c, d):
    # keep exact ints where possible, else float
    if c % d == 0:
        return c // d
    return c / d


def poly_eval(a, x):
    def helper(coeffs, power, acc):
        if not coeffs:
            return acc
        return helper(coeffs[1:], power + 1, acc + coeffs[0] * (x ** power))
    return helper(a, 0, 0)


def step(words):
    def combine(stack, token):
        if isinstance(token, int):
            return stack + [token]
        if isinstance(token, tuple):
            return stack + [token]
        if token == "+":
            b = stack[-1]; a = stack[-2]
            return stack[:-2] + [poly_add(a, b)]
        if token == "-":
            b = stack[-1]; a = stack[-2]
            return stack[:-2] + [poly_sub(a, b)]
        if token == "scale":
            k = stack[-1]; a = stack[-2]
            return stack[:-2] + [poly_scale(a, k)]
        if token == "deriv":
            a = stack[-1]
            return stack[:-1] + [poly_deriv(a)]
        if token == "integ":
            a = stack[-1]
            return stack[:-1] + [poly_integ(a)]
        if token == "eval":
            x = stack[-1]; a = stack[-2]
            return stack[:-2] + [poly_eval(a, x)]
        if token in words:
            body = words[token]
            combiner = step(words)
            return reduce_(combiner, body, stack)
        raise ValueError(f"bad token {token!r}")
    return combine


def evaluate_postfix(tokens, polys, words):
    def to_val(tok):
        if tok in polys:
            return polys[tok]
        return tok
    real_tokens = [to_val(t) for t in tokens]
    combiner = step(words)
    final_stack = reduce_(combiner, real_tokens, [])
    return final_stack[-1]


def fmt_value(v):
    if is_poly(v):
        return "[" + ",".join(str(c) for c in v) + "]"
    return str(v)


def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    npolys = int(data[idx]); idx += 1
    polys = {}
    for _ in range(npolys):
        parts = data[idx].split(); idx += 1
        name = parts[0]
        coeffs = tuple(int(c) for c in parts[1:])
        polys[name] = _trim(coeffs)
    nwords = int(data[idx]); idx += 1
    words = {}
    for _ in range(nwords):
        parts = data[idx].split(); idx += 1
        wname = parts[0]
        body = []
        for t in parts[1:]:
            if t.lstrip("-").isdigit():
                body.append(int(t))
            else:
                body.append(t)
        words[wname] = body
    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        toks = []
        for t in parts:
            if t.lstrip("-").isdigit():
                toks.append(int(t))
            else:
                toks.append(t)
        result = evaluate_postfix(toks, polys, words)
        out.append(fmt_value(result))
    print("\n".join(out))


if __name__ == "__main__":
    solve()
