import sys
sys.setrecursionlimit(20000)

# =============================================================================
# Q2: Postfix over Polynomials
# =============================================================================
# A polynomial is represented as an IMMUTABLE tuple of ints
#   (c0, c1, c2, ...)   meaning   c0 + c1*x + c2*x^2 + ...
# (lowest degree first), with no trailing zero coefficients (so the zero
# polynomial is the empty tuple ()). A "value" on the stack is either an
# int or such a tuple.
#
# Operators (each pops its operands off the top of the stack and pushes
# exactly one result, like every postfix operator you've seen):
#   +        : poly + poly -> poly
#   -        : poly - poly -> poly              (a b -  computes a - b)
#   scale    : poly k -> poly                   (multiply every coeff by k)
#   deriv    : poly -> poly                     (d/dx)
#   integ    : poly -> poly                     (antiderivative, constant
#                                                 term fixed at 0; use exact
#                                                 ints where the division is
#                                                 exact, a float otherwise)
#   eval     : poly x -> int/float               (evaluate the polynomial
#                                                 at the integer x)
# A named word runs its own token sequence against the CURRENT stack with
# exactly the effect those tokens would have inline -- see the question
# paper for the full explanation and worked examples (this is the exact
# same idea as "words" in your postfix-over-signals lab, just replayed
# here with polynomials).
#
# HARD RULES (autograder / manual review both check these):
#   - All iteration must go through YOUR OWN reduce_(), written with
#     recursion. No for/while loop may replace it as the driver of token
#     processing (helper loops inside e.g. poly_add's own recursion are
#     also disallowed -- use recursion there too).
#   - Nothing may be mutated. Every helper returns a NEW tuple/list; the
#     ones passed in are left untouched. Do not reassign a name once it
#     has a value inside a function.
#   - Do not use eval(), exec(), or any other built-in expression
#     evaluator.
# =============================================================================


def is_poly(v):
    """Return True iff v is a polynomial (tuple), False if it's a plain int."""
    return isinstance(v, tuple)


def _trim(coeffs):
    """
    Given an iterable of coefficients (low degree first), return the
    canonical tuple form: no trailing zero coefficients. _trim(()) == ().
    You may use this helper freely; it does not need to be recursive.
    """
    coeffs = list(coeffs)
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    return tuple(coeffs)


def reduce_(function, iterable, initial):
    """
    Fold `function` over `iterable`, starting from `initial`:
        reduce_(f, [x1, x2, x3], init) == f(f(f(init, x1), x2), x3)
    Must be written with recursion; no for/while loop.
    """
    # TODO: implement
    raise NotImplementedError


def poly_add(a, b):
    """Return a + b (as a new, trimmed tuple). Use recursion, not a loop."""
    # TODO: implement
    raise NotImplementedError


def poly_neg(a):
    """Return -a (negate every coefficient). Recursion or a comprehension
    (which is not a `for`/`while` statement) are both fine here."""
    # TODO: implement
    raise NotImplementedError


def poly_sub(a, b):
    """Return a - b. Implement this IN TERMS OF poly_add and poly_neg --
    do not write a second addition-like recursion from scratch."""
    # TODO: implement
    raise NotImplementedError


def poly_scale(a, k):
    """Return a with every coefficient multiplied by k, trimmed."""
    # TODO: implement
    raise NotImplementedError


def poly_deriv(a):
    """
    Return the derivative of a. Recall (c_i * x^i)' = i*c_i*x^(i-1), so
    the new coefficient list drops index 0 and multiplies what remains by
    its (old) exponent. The derivative of a constant or empty polynomial
    is the zero polynomial ().
    """
    # TODO: implement
    raise NotImplementedError


def _rat(c, d):
    """Return c/d as an int if it divides evenly, else as a float. You are
    given this helper -- use it inside poly_integ."""
    if c % d == 0:
        return c // d
    return c / d


def poly_integ(a):
    """
    Return the antiderivative of a with constant term fixed at 0. If a
    represents c0 + c1*x + c2*x^2 + ..., the result represents
    0 + c0*x + (c1/2)*x^2 + (c2/3)*x^3 + ...   (use _rat for each
    division so exact results stay exact ints).
    """
    # TODO: implement
    raise NotImplementedError


def poly_eval(a, x):
    """
    Evaluate polynomial a at integer x and return the resulting number
    (Horner's method or a direct sum are both fine; must be written with
    recursion, not a loop).
    """
    # TODO: implement
    raise NotImplementedError


def step(words):
    """
    Return the two-argument combiner combine(stack, token) that reduce_
    uses for ONE token, where `stack` is a plain Python list used as an
    (immutable-in-spirit -- always replaced wholesale, never mutated in
    place with e.g. .append or .pop) representation of the value stack,
    and `token` is either an int, a polynomial tuple, an operator name
    (string), or a word name (string) that is a key of `words`.

    You MUST reuse this exact function (by recursively building another
    `step(words)` combiner and reduce_-ing it over the word's body) to
    handle the word case -- no separate evaluator, no manual expansion of
    the word ahead of time.
    """
    def combine(stack, token):
        # TODO: implement every case: int/poly literal push, each of the
        # six operators above, and the "token is a word name" case.
        raise NotImplementedError
    return combine


def evaluate_postfix(tokens, polys, words):
    """
    tokens : list of raw tokens as read from the input -- each is either
             an int, an operator name, a name that is a key of `polys`
             (meaning "push this polynomial"), or a name that is a key of
             `words`.
    polys  : dict name -> polynomial tuple (the polynomial registry).
    words  : dict name -> list of tokens (the word registry).

    Resolve every polynomial-name token to its tuple value, run the whole
    program through ONE reduce_() call using step(words), and return the
    single value left on the stack.
    """
    # TODO: implement
    raise NotImplementedError


def fmt_value(v):
    """
    Format a result for printing: an int/float is printed via str(); a
    polynomial tuple () is printed as "[]" and a nonempty one as
    "[c0,c1,c2,...]" with no spaces. You are given this -- do not change
    it, just call it from solve() below.
    """
    if is_poly(v):
        return "[" + ",".join(str(c) for c in v) + "]"
    return str(v)


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
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
