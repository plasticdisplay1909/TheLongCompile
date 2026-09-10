import sys

MOD = 1000000007
sys.setrecursionlimit(10000)

# =========================================================================
# Q2 : The Data Pipeline Factory  (Functional Programming)
# =========================================================================
#
# You must implement three small pieces of generic functional machinery,
# and then use THEM (not hand-rolled equivalents) to build the rest of
# this program. Re-implementing e.g. memoize's caching logic by hand
# inside fib(), instead of applying the memoize decorator to it, defeats
# the point of the exercise and may not be given credit even if the
# output happens to be correct.


def compose(*funcs):
    """
    compose(f, g, h) must return a new function `c` such that, for any x,
        c(x) == f(g(h(x)))
    i.e. the LAST function passed in is applied FIRST, exactly the way
    mathematical function composition (f o g o h) works. compose() with
    zero arguments should return the identity function.

    TODO: implement this.
    """
    raise NotImplementedError


def curry2(f):
    """
    Given a two-argument function f(a, b), return a curried version:
    a function of `a` that returns a function of `b`, i.e.
        curry2(f)(a)(b) == f(a, b)
    for every a, b.

    TODO: implement this.
    """
    raise NotImplementedError


def memoize(f):
    """
    Return a wrapped version of f that caches results by argument tuple,
    so that calling the wrapped function twice with the same arguments
    only ever calls f itself once. f may take any number of positional
    arguments (support *args in your cache key).

    This must work correctly even when f calls the WRAPPED version of
    itself recursively (see fib() below) -- that is precisely what turns
    an exponential-time recursion into a linear-time one, and it is what
    the performance test cases in this problem are designed to check.

    TODO: implement this.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------
# Pipeline stages. A pipeline is a list of (kind, fn) pairs, where kind
# is the string "map" or "filter" and fn is the unary function to apply
# at that stage. You must build the individual stage functions using
# curry2() together with lambdas/closures, rather than writing a fresh
# named function per stage by hand -- curry2 exists so that a single
# generic binary lambda (e.g. "x + a") can be partially applied with a
# fixed `a` to produce each stage's unary function.
# ---------------------------------------------------------------------
def make_stage(opname, arg):
    """
    opname is one of:
        MAP_ADD k     -> stage function: x -> x + k
        MAP_MUL k     -> stage function: x -> x * k
        FILTER_GT k   -> stage function: x -> x > k
        FILTER_LT k   -> stage function: x -> x < k
        FILTER_EVEN   -> stage function: x -> (x % 2 == 0)
        FILTER_ODD    -> stage function: x -> (x % 2 != 0)
    arg is the integer k for the MAP_*/FILTER_GT/FILTER_LT ops, and is
    None for FILTER_EVEN/FILTER_ODD.

    Return a tuple (kind, fn) where kind is "map" for the MAP_* ops and
    "filter" for the FILTER_* ops, and fn is the unary function described
    above. Build the MAP_ADD/MAP_MUL/FILTER_GT/FILTER_LT stage functions
    via curry2 applied to a two-argument lambda -- do not just write
    `lambda x: x + arg` directly for those four (that isn't using the
    currying machinery you just built, and is not accepted here).

    TODO: implement this.
    """
    raise NotImplementedError


def run_pipeline(stages, values):
    """
    Apply the given list of (kind, fn) stages to `values`, IN ORDER
    (stage 0 first), using Python's built-in map() and filter() for the
    two kinds of stage respectively -- not manual for-loops that
    reimplement what map/filter already do. Return the final list.

    TODO: implement this.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------
# The "transform" function used by COMPOSE_EVAL queries below. It must
# be built with a SINGLE call to compose() over the requested named ops,
# not with a hand-written for-loop that applies them one by one.
# ---------------------------------------------------------------------
TRANSFORM_OPS = {
    "ADD1": lambda x: x + 1,
    "DOUBLE": lambda x: x * 2,
    "NEGATE": lambda x: -x,
    "SQUARE": lambda x: x * x,
    "HALF": lambda x: x // 2,
}


def build_transform(op_names):
    """
    op_names is a list of strings naming ops from TRANSFORM_OPS, given in
    the order they must be APPLIED to a value (op_names[0] first, ...,
    op_names[-1] last). Look up the corresponding functions and combine
    them into a single function using exactly one call to compose()
    (remember: compose applies its LAST argument first, so you will need
    to pass the looked-up functions to compose() in the right order to
    get "op_names[0] applied first" out the other end). If op_names is
    empty, the returned function must be the identity.

    TODO: implement this.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------
# A memoized recursive Fibonacci. fib(n) must be built by decorating a
# recursive function with your memoize() from above -- so that fib's
# recursive calls to itself go through the memoized wrapper and get
# their results cached, turning naive-recursive fib (exponential time)
# into a linear-time computation. Some hidden test cases call FIB with
# n large enough, and/or repeated often enough, that a non-memoized
# (or incorrectly memoized) recursive solution will time out.
#
# fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2), all values
# reported modulo MOD = 1000000007.
#
# TODO: define fib as a memoized recursive function below.
# ---------------------------------------------------------------------


def fib(n):
    raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you, do not modify.
#
# Input format:
#   line 1        : N
#   line 2        : N space-separated integers (the initial value list;
#                    blank if N == 0)
#   line 3        : T, the number of pipeline stages
#   next T lines  : one stage each, e.g. "MAP_ADD 5" or "FILTER_EVEN"
#   next line     : C, the number of transform ops for COMPOSE_EVAL
#   next C lines  : one op name each, e.g. "ADD1" (applied in this order)
#   next line     : Q, the number of queries
#   next Q lines  : one of
#                      RUN
#                      FIB n
#                      COMPOSE_EVAL x
#
# For every RUN query, print the resulting list space-separated on its
# own line, or the literal word EMPTY if the result is an empty list.
# For every FIB / COMPOSE_EVAL query, print the single resulting integer
# on its own line.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    n = int(data[idx]); idx += 1
    values = list(map(int, data[idx].split())) if data[idx].strip() else []
    idx += 1
    t = int(data[idx]); idx += 1
    stages = []
    for _ in range(t):
        parts = data[idx].split(); idx += 1
        opname = parts[0]
        arg = int(parts[1]) if len(parts) > 1 else None
        stages.append(make_stage(opname, arg))

    c = int(data[idx]); idx += 1
    op_names = []
    for _ in range(c):
        op_names.append(data[idx].strip()); idx += 1
    transform_fn = build_transform(op_names)

    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        line = data[idx].split(); idx += 1
        if line[0] == "RUN":
            result = run_pipeline(stages, values)
            out.append(" ".join(map(str, result)) if result else "EMPTY")
        elif line[0] == "FIB":
            nn = int(line[1])
            out.append(str(fib(nn) % MOD))
        elif line[0] == "COMPOSE_EVAL":
            x = int(line[1])
            out.append(str(transform_fn(x)))
    print("\n".join(out))


if __name__ == "__main__":
    solve()
