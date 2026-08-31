import sys

# =============================================================================
# Q9: The Ouroboros Machine (toy register language -> net linear transform)
# =============================================================================
# A tiny language with exactly 6 registers r0..r5, each holding an integer
# mod p. Three statement types (i, j are register indices 0..5):
#   add ri rj    -- ri <- (ri + rj) mod p   (rj unchanged)
#   sub ri rj    -- ri <- (ri - rj) mod p   (rj unchanged)
#   swap ri rj   -- ri and rj trade values (both change)
# plus a block construct:
#   loop k
#   ...
#   end
# which runs the statements between `loop k` and its matching `end`
# exactly k times, in order (k is a non-negative integer; loop blocks may
# be nested).
#
# Exactly as in your RepLang lab, every statement here is a LINEAR
# function of the register vector (add/sub/swap are all expressible as
# multiplying the register vector by a 6x6 matrix -- yes, even swap: it's
# a permutation matrix), so the whole program corresponds to a single
# 6x6 matrix M such that running the program is equivalent to
# left-multiplying the initial register vector by M. Your job is to
# compute and return that matrix, with every entry reduced into
# [0, p-1].
#
# COMPOSITION ORDER (the detail everyone gets backwards): if statement T1
# runs before statement T2, and each is represented by its own 6x6
# matrix, then running T1 then T2 on a vector v gives T2 @ (T1 @ v) =
# (T2 @ T1) @ v -- so the NET matrix accumulates with each new
# statement's matrix multiplied ON THE LEFT of whatever came before it,
# not the right. Get this backwards and every single-column test will
# still pass by coincidence when p == 2 but nothing else will.
#
# EFFICIENCY: `loop k ... end` must be handled with FAST MATRIX
# EXPONENTIATION (repeated squaring, O(log k) matrix multiplications) on
# the block's OWN net matrix -- never by literally executing the body k
# times (k can be enormous). Maintain a stack of matrix accumulators, one
# per currently-open block (the outermost "program so far" counts as a
# block too), pushing a fresh identity matrix on `loop` and, on the
# matching `end`, exponentiating what you built inside by the loop count
# and folding that INTO the enclosing block's accumulator using the same
# left-multiplication rule as any other statement.
# =============================================================================

N = 6


def identity():
    """Given here: the 6x6 identity matrix as a list of lists."""
    return [[1 if i == j else 0 for j in range(N)] for i in range(N)]


def matmul(A, B, p):
    """
    Return A @ B mod p (both N x N). This is given as a plain triple loop
    for clarity -- you do not need to optimise it, just USE it correctly
    inside matpow and evaluate_program.
    """
    C = [[0] * N for _ in range(N)]
    for i in range(N):
        for k in range(N):
            a = A[i][k]
            if a == 0:
                continue
            for j in range(N):
                C[i][j] = (C[i][j] + a * B[k][j]) % p
    return C


def matpow(M, power, p):
    """
    Return M^power mod p using fast exponentiation by squaring, in
    O(log power) calls to matmul. (power >= 0; M^0 is the identity.)
    """
    # TODO: implement
    raise NotImplementedError


def elem_add(i, j):
    """Return the 6x6 elementary matrix E such that E @ v performs
    exactly `ri <- ri + rj` and leaves every other register unchanged
    (start from identity() and change ONE entry)."""
    # TODO: implement
    raise NotImplementedError


def elem_sub(i, j):
    """Like elem_add, but for `ri <- ri - rj`."""
    # TODO: implement
    raise NotImplementedError


def elem_swap(i, j):
    """
    Return the 6x6 PERMUTATION matrix that swaps registers i and j (start
    from identity() and think about which four entries must change, and
    to what).
    """
    # TODO: implement
    raise NotImplementedError


def evaluate_program(lines, p):
    """
    lines : list of raw statement strings (already given to you split by
            line -- may contain blank lines, ignore those), e.g.
            ["add r0 r1", "loop 3", "sub r1 r2", "end"]
    p     : the modulus.

    Return the single 6x6 matrix (as a list of 6 lists of 6 ints, each
    reduced into [0, p-1]) representing the net effect of running the
    whole program once, starting from the identity.

    Maintain TWO stacks as you scan the lines top to bottom:
      - a stack of matrix accumulators, one per currently-open block
        (push identity() at the very start for the outermost "program"
        block, and again every time you see `loop k`)
      - a stack of pending loop counts (push k every time you see
        `loop k`)
    For `add`/`sub`/`swap`: build the elementary matrix E for that
    statement, pop the top accumulator, and push back (E @ accumulator)
    mod p -- i.e. fold E into the CURRENT (innermost open) block.
    For `end`: pop the just-finished block's accumulator (call it
    `body`) and the matching loop count k; compute body^k mod p via
    matpow; pop the now-exposed ENCLOSING block's accumulator (`outer`);
    push back (body^k @ outer) mod p, folding the whole loop into its
    enclosing block exactly like a single statement would be folded in.
    At the end, exactly one accumulator remains on the stack -- return it.
    """
    # TODO: implement
    raise NotImplementedError


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
def solve():
    data = sys.stdin.read().split("\n")
    p = int(data[0].strip())
    lines = data[1:]
    while lines and lines[-1].strip() == "":
        lines.pop()
    M = evaluate_program(lines, p)
    out = []
    for row in M:
        out.append(" ".join(str(x % p) for x in row))
    print("\n".join(out))


if __name__ == "__main__":
    solve()
