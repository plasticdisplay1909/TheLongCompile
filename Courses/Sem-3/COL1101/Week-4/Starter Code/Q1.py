import sys


class LadderList:
    def __init__(self):
        # TODO: set up whatever internal state you need.
        raise NotImplementedError

    def append(self, x):
        """
        Add x as the new last element.
        Must run in O(log n) worst-case time.

        TODO: implement this.
        """
        raise NotImplementedError

    def pop(self):
        """
        Remove and return the current last element.
        Must run in O(log n) worst-case time.
        You may assume this is only called when the LadderList is non-empty.

        TODO: implement this.
        """
        raise NotImplementedError

    def __getitem__(self, i):
        """
        Return the element currently at position i (i.e. what my_list[i]
        would return). Must run in O(log n) worst-case time.
        You may assume 0 <= i < len(self) whenever this is called.

        TODO: implement this. Fix and document your indexing convention.
        """
        raise NotImplementedError

    def __setitem__(self, i, x):
        """
        Update the element at position i to x (i.e. what my_list[i] = x
        would do). Must run in O(log n) worst-case time.
        You may assume 0 <= i < len(self) whenever this is called.

        TODO: implement this.
        """
        raise NotImplementedError

    def __len__(self):
        """
        Return the number of elements currently stored.
        Must run in O(1) worst-case time (e.g. maintain a running count
        rather than walking the whole structure on every call).

        TODO: implement this.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1

    ll = LadderList()
    out = []
    for _ in range(q):
        line = data[idx].split(); idx += 1
        if line[0] == "append":
            ll.append(int(line[1]))
        elif line[0] == "pop":
            out.append(str(ll.pop()))
        elif line[0] == "access":
            out.append(str(ll[int(line[1])]))
        elif line[0] == "set":
            ll[int(line[1])] = int(line[2])
        elif line[0] == "len":
            out.append(str(len(ll)))
        else:
            raise ValueError(f"unrecognized op: {line}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
