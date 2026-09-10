import sys

N = 10


# ---------------------------------------------------------------------
# 1. Stack class -- given to you.
# ---------------------------------------------------------------------
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


# ---------------------------------------------------------------------
# 2. Matrix helpers.
# ---------------------------------------------------------------------
def identity_matrix():
    """Return the 10 x 10 identity matrix as a list of lists."""
    return [[1 if i == j else 0 for j in range(N)] for i in range(N)]


def matrix_multiply(A, B, p):
    C = []

    for i in range(N):
        row=[]
        for j in range(N):
            val=0
            for k in range(N): val+=A[i][k] * B[k][j]

            row.append(val%p)

        C.append(row)
    
    return C

def add(M,i,j,p):
    for k in range(N):
        M[i][k] = (M[i][k] + M[j][k])%p

def sub(M,i,j,p):
    for k in range(N):
        M[i][k] = (M[i][k]-M[j][k])%p

def matrix_power(M, power, p):
    """
    Compute M^power mod p using fast exponentiation by squaring,
    in O(log(power)) matrix multiplications.

    TODO: implement this using matrix_multiply() and identity_matrix().
    """
    # raise NotImplementedError

    """Trying to use binary exponation thing"""
    res=identity_matrix()       ## M^0
    base=M

    while power>0:
        if (power%2 == 1):  res=matrix_multiply(res,base,p)

        ## Changing M to M**2
        base=matrix_multiply(base,base,p)

        ## Shifting bits
        power//=2
    return res

# ---------------------------------------------------------------------
# 3. Parsing + evaluation, using the Stack above.
# ---------------------------------------------------------------------
def evaluate_program(program_lines, p):
    """
    program_lines: list of raw statement strings, e.g.
        ["add v0 v1", "repeat 3", "sub v1 v2", "end"]
    p: the modulus.

    Returns the single 10x10 matrix (mod p) representing the net effect
    of running the whole program once, as a list of 10 lists of 10 ints.

    TODO: initialize whatever stack(s) or other state you need, then
    fill in the four cases below.
    """
    
    curr=identity_matrix()
    stack=Stack()

    for line in program_lines:
        line = line.strip()
        if not line:
            continue
        statement = line.split()

        if statement[0] == "add":
            # statement looks like ["add", "v0", "v1"]
            # Variables are 0-indexed, so "v0" -> index 0, "v1" -> index 1.
            i,j=int(statement[1][1:]),int(statement[2][1:])

            add(curr,i,j,p)

        elif statement[0] == "sub":
            # statement looks like ["sub", "v0", "v1"]
            i,j=int(statement[1][1:]),int(statement[2][1:])

            sub(curr,i,j,p)

        elif statement[0] == "repeat":
            # statement looks like ["repeat", "100"]
            k=int(statement[1])
            stack.push((curr,k))

            curr=identity_matrix()

        elif statement[0] == "end":
            prev,k=stack.pop()
            new=matrix_power(curr,k,p)
            curr=matrix_multiply(new,prev,p)

        else:
            raise ValueError(f"unrecognized statement: {line}")

    # TODO: return the single 10x10 matrix representing the net effect
    # of the whole program (this should be whatever's left in your own
    # stack once every line has been processed).
    return curr


# ---------------------------------------------------------------------
# 4. I/O driver -- given to you.
# ---------------------------------------------------------------------
def read_input():
    data = sys.stdin.read().split("\n")
    p = int(data[0])
    program_lines = [line for line in data[1:]]
    while program_lines and program_lines[-1] == "":
        program_lines.pop()
    return p, program_lines


def solve():
    p, program_lines = read_input()
    M = evaluate_program(program_lines, p)
    for row in M:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    solve()
