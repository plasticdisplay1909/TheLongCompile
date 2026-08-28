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
        C.append([])
        for j in range(N):
            C[i].append(0)
            for k in range(N):
                C[i][j] = (C[i][j] + A[i][k]*B[k][j]) % p
    
    return C


def matrix_power(M, power, p):
    """
    Compute M^power mod p using fast exponentiation by squaring,
    in O(log(power)) matrix multiplications.

    TODO: implement this using matrix_multiply() and identity_matrix().
    """
    while (power):
        x=power%2
        power/=2
        
        M=matrix_multiply(M,M,p)
    return M
    # raise NotImplementedError


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
    
    r,s=Stack(),Stack()
    a,b=identity_matrix(), identity_matrix()
    
    for line in program_lines:
        line = line.strip()
        if not line:
            continue
        statement = line.split()

        if statement[0] == "add":
            # statement looks like ["add", "v0", "v1"]
            # Variables are 0-indexed, so "v0" -> index 0, "v1" -> index 1.
            m=identity_matrix()
            
            idx1=int(statement[1][1])
            idx2=int(statement[2][1])
            
            m[idx1]=row_add(m[idx1],m[idx2])
            a=matrix_multiply(a,m,p)
            # pass

        elif statement[0] == "sub":
            # statement looks like ["sub", "v0", "v1"]
            m=identity_matrix()
            
            idx1=int(statement[1][1])
            idx2=int(statement[2][1])
            
            m[idx1]=row_sub(m[idx1],m[idx2])
            a=matrix_multiply(a,m,p)

        elif statement[0] == "repeat":
            # statement looks like ["repeat", "100"]
            val=int(statement[1])
            if r.is_empty():
               raise ValueError
            n=r.pop() 
            pass

        elif statement[0] == "end":
            pass

        else:
            raise ValueError(f"unrecognized statement: {line}")

    # TODO: return the single 10x10 matrix representing the net effect
    # of the whole program (this should be whatever's left in your own
    # stack once every line has been processed).
    raise NotImplementedError


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
