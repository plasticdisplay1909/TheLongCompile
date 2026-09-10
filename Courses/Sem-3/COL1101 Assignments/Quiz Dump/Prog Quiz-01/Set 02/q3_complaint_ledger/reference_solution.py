import sys


class Vector:
    INIT_CAP = 1

    def __init__(self):
        self._cap = self.INIT_CAP
        self._data = [None] * self._cap
        self._size = 0

    def _resize(self, new_cap):
        new_cap = max(1, new_cap)
        new_data = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._cap = new_cap

    def push_back(self, x):
        if self._size == self._cap:
            self._resize(self._cap * 2)
        self._data[self._size] = x
        self._size += 1

    def pop_back(self):
        x = self._data[self._size - 1]
        self._data[self._size - 1] = None
        self._size -= 1
        if self._size > 0 and self._size <= self._cap // 4:
            self._resize(max(1, self._cap // 2))
        return x

    def get(self, i):
        return self._data[i]

    def set(self, i, x):
        self._data[i] = x

    def size(self):
        return self._size

    def capacity(self):
        return self._cap


class MovingAverageTracker:
    def __init__(self):
        self.vec = Vector()
        self.prefix = Vector()  # prefix[i] = sum of first i elements (prefix[0]=0)
        self.prefix.push_back(0)

    def add(self, x):
        self.vec.push_back(x)
        self.prefix.push_back(self.prefix.get(self.prefix.size() - 1) + x)

    def undo(self):
        self.vec.pop_back()
        self.prefix.pop_back()

    def average_last(self, k):
        n = self.vec.size()
        if k <= 0 or k > n:
            return None
        total = self.prefix.get(n) - self.prefix.get(n - k)
        return total / k

    def get(self, i):
        return self.vec.get(i)

    def set_(self, i, x):
        old = self.vec.get(i)
        self.vec.set(i, x)
        n = self.vec.size()
        delta = x - old
        # naive rebuild of the tail of the prefix array (kept simple: this
        # is the reference, correctness matters more than speed here)
        for j in range(i + 1, n + 1):
            self.prefix.set(j, self.prefix.get(j) + delta)

    def size(self):
        return self.vec.size()

    def capacity(self):
        return self.vec.capacity()


def fmt_avg(v):
    if v is None:
        return "NA"
    if v == int(v):
        return str(int(v))
    return f"{v:.4f}"


def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    tr = MovingAverageTracker()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "PUSH":
            tr.add(int(parts[1]))
        elif cmd == "POP":
            tr.undo()
        elif cmd == "GET":
            out.append(str(tr.get(int(parts[1]))))
        elif cmd == "SET":
            tr.set_(int(parts[1]), int(parts[2]))
        elif cmd == "SIZE":
            out.append(str(tr.size()))
        elif cmd == "CAPACITY":
            out.append(str(tr.capacity()))
        elif cmd == "AVG":
            out.append(fmt_avg(tr.average_last(int(parts[1]))))
        else:
            raise ValueError(cmd)
    print("\n".join(out))


if __name__ == "__main__":
    solve()
