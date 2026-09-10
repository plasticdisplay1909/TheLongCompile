import sys

# ---------------------------------------------------------------------
# 0. Helpers -- given to you. Do not modify.
# ---------------------------------------------------------------------

def make_raw_array(n):
    """Return a fresh 'raw' fixed-size storage block of length n, all slots
    initialised to None. You must treat this exactly like a fixed-capacity
    C-style array: you may only ever read/write raw[i] for a valid index,
    you may never call .append/.pop/.insert/slicing on it, and copying its
    contents into a bigger or smaller block is YOUR responsibility (that is
    the whole point of this problem)."""
    return [None] * n


class DynamicArray:
    """
    A from-scratch re-implementation of the 'array doubling' idea that
    Python's own list uses internally, except here YOU control exactly
    when the underlying raw block grows or shrinks, and by how much.

    You must maintain three pieces of state:
        self._raw       : a raw array (see make_raw_array above), whose
                           length is the current CAPACITY.
        self._size      : the number of logically 'live' elements
                           currently stored (0 <= size <= capacity).
    You may add any other private fields you find useful, but you must not
    remove self._raw or self._size, and you must not use a Python list's
    append/pop/insert/remove/slicing anywhere in your solution -- the only
    list operations you are allowed to use on self._raw are indexed
    reads self._raw[i] and indexed writes self._raw[i] = x, plus
    allocating a brand-new block with make_raw_array(n).
    """

    def __init__(self):
        # TODO: initialise an empty DynamicArray with capacity 1.
        raise NotImplementedError

    def size(self):
        """Return the number of live elements. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def capacity(self):
        """Return the length of the current raw block. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def get(self, i):
        """Return the element currently at index i. 0 <= i < size().
        Must be O(1)."""
        # TODO
        raise NotImplementedError

    def set(self, i, x):
        """Overwrite the element at index i with x. 0 <= i < size().
        Must be O(1)."""
        # TODO
        raise NotImplementedError

    def push_back(self, x):
        """Append x as the new last element.

        Must run in O(1) AMORTISED time. When the raw block is full,
        you must allocate a new block of TWICE the capacity (never less,
        never more) and copy every live element across before inserting
        the new one. Capacity must never be allowed to reach 0 once the
        array has been created -- the smallest capacity you may ever hold
        is 1.
        """
        # TODO
        raise NotImplementedError

    def pop_back(self):
        """Remove and return the current last element. You may assume
        size() > 0 whenever this is called.

        Must run in O(1) AMORTISED time. This is the subtle half of the
        problem: you must shrink the raw block when occupancy gets too
        low, but shrinking on every single pop (e.g. as soon as
        size < capacity) throws the amortised bound away entirely --
        a push immediately after such a pop would force another resize,
        and an adversary alternating push/pop would make EVERY call
        pay for a full copy. Pick a shrink threshold and a new capacity
        after shrinking that together avoid this 'thrashing' failure
        mode. (Halving the capacity only when occupancy drops to
        one QUARTER of capacity -- not one half -- is the classical fix;
        think about why one half does not work before you commit to a
        threshold.) Capacity must never drop below 1.
        """
        # TODO
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1

    arr = DynamicArray()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if parts[0] == "PUSH":
            arr.push_back(int(parts[1]))
        elif parts[0] == "POP":
            out.append(str(arr.pop_back()))
        elif parts[0] == "GET":
            out.append(str(arr.get(int(parts[1]))))
        elif parts[0] == "SET":
            arr.set(int(parts[1]), int(parts[2]))
        elif parts[0] == "SIZE":
            out.append(str(arr.size()))
        elif parts[0] == "CAP":
            out.append(str(arr.capacity()))
        else:
            raise ValueError(f"unrecognized op: {parts}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
