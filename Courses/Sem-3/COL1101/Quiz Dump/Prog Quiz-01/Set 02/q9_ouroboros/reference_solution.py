import sys

N = 6


def identity():
    return [[1 if i == j else 0 for j in range(N)] for i in range(N)]


def matmul(A, B, p):
    C = [[0] * N for _ in range(N)]
    for i in range(N):
        Ai = A[i]
        for k in range(N):
            a = Ai[k]
            if a == 0:
                continue
            Bk = B[k]
            Ci = C[i]
            for j in range(N):
                Ci[j] = (Ci[j] + a * Bk[j]) % p
    return C


def matpow(M, power, p):
    result = identity()
    base = M
    while power > 0:
        if power & 1:
            result = matmul(result, base, p)
        base = matmul(base, base, p)
        power >>= 1
    return result


def elem_add(i, j):
    # M such that new_reg[i] = reg[i] + reg[j], everything else unchanged
    M = identity()
    M[i][j] += 1
    return M


def elem_sub(i, j):
    M = identity()
    M[i][j] -= 1
    return M


def elem_swap(i, j):
    M = identity()
    M[i][i], M[j][j] = 0, 0
    M[i][j], M[j][i] = 1, 1
    return M


def evaluate_program(lines, p):
    mat_stack = [identity()]   # mat_stack[-1] = accumulator for current block
    loop_stack = []            # loop_stack[-1] = repeat count for current block
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        tok = line.split()
        if tok[0] in ("add", "sub", "swap"):
            i, j = int(tok[1][1:]), int(tok[2][1:])
            if tok[0] == "add":
                E = elem_add(i, j)
            elif tok[0] == "sub":
                E = elem_sub(i, j)
            else:
                E = elem_swap(i, j)
            top = mat_stack.pop()
            mat_stack.append(matmul(E, top, p))
        elif tok[0] == "loop":
            k = int(tok[1])
            loop_stack.append(k)
            mat_stack.append(identity())
        elif tok[0] == "end":
            body = mat_stack.pop()
            k = loop_stack.pop()
            powered = matpow(body, k, p)
            outer = mat_stack.pop()
            mat_stack.append(matmul(powered, outer, p))
        else:
            raise ValueError(f"bad line: {line}")
    return mat_stack.pop()


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
