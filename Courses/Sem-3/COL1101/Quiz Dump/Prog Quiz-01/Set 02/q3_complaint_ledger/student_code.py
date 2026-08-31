import sys

# =============================================================================
# Q3: The Complaint Ledger (amortized-O(1) dynamic array from scratch)
# =============================================================================
# You must implement Vector WITHOUT ever calling Python's own list.append,
# list.pop, list.insert, del on a list, or slicing that copies more than
# the fixed-size internal buffer allows. The internal buffer IS allowed to
# be a plain Python list, but you must treat it as a fixed-capacity raw
# array: you manually track _size vs _cap and manually reallocate.
#
# CAPACITY POLICY (must be followed EXACTLY -- CAPACITY is graded output):
#   - Initial capacity is 1.
#   - push_back: if the array is completely full (size == capacity) BEFORE
#     inserting, first reallocate to double the capacity (capacity *= 2),
#     copying every existing element across, THEN insert the new element.
#   - pop_back: remove the last element FIRST, THEN, only if the new size
#     is strictly positive AND size <= capacity // 4, reallocate down to
#     capacity // 2 (never below 1), copying the surviving elements
#     across. If size becomes exactly 0, do NOT shrink any further no
#     matter how large capacity currently is.
# See the question paper for a fully worked trace of this policy.
# =============================================================================


class Vector:
    INIT_CAP = 1

    def __init__(self):
        """Set up an empty Vector: internal buffer of length INIT_CAP,
        self._cap = INIT_CAP, self._size = 0."""
        # TODO: implement
        raise NotImplementedError

    def _resize(self, new_cap):
        """
        Allocate a fresh internal buffer of length new_cap (never below 1)
        and copy the first self._size elements of the old buffer into it,
        by INDEX -- do not use slicing tricks that secretly do the copy
        for you in one call; write the copy yourself. Replace self._data
        and update self._cap.
        """
        # TODO: implement
        raise NotImplementedError

    def push_back(self, x):
        """Append x as the new last element, following the capacity
        policy above exactly. Amortized O(1)."""
        # TODO: implement
        raise NotImplementedError

    def pop_back(self):
        """Remove and return the current last element, following the
        capacity policy above exactly. Amortized O(1). (You may assume
        this is only called on a non-empty Vector.)"""
        # TODO: implement
        raise NotImplementedError

    def get(self, i):
        """Return the element at index i. O(1). (0 <= i < size guaranteed.)"""
        # TODO: implement
        raise NotImplementedError

    def set(self, i, x):
        """Overwrite the element at index i with x. O(1)."""
        # TODO: implement
        raise NotImplementedError

    def size(self):
        """Current number of stored elements. O(1)."""
        # TODO: implement
        raise NotImplementedError

    def capacity(self):
        """Current length of the internal buffer. O(1)."""
        # TODO: implement
        raise NotImplementedError


class MovingAverageTracker:
    """
    Wraps a Vector of complaint-resolution times and answers "average of
    the last k entries" queries. To keep AVG fast, also maintain a second
    Vector `prefix` where prefix.get(i) is the sum of the first i entries
    (so prefix.get(0) == 0, prefix.get(n) == sum of everything). Then
    average_last(k) is a single O(1) lookup + one division -- NOT an O(k)
    rescan. (A stress test with thousands of large-k AVG queries after
    thousands of pushes WILL time out an O(k)-per-query implementation.)
    """

    def __init__(self):
        # TODO: implement (set up self.vec and self.prefix, matching the
        # reference's field names is NOT required, but the *behaviour*
        # below is required).
        raise NotImplementedError

    def add(self, x):
        """Push x onto the ledger and extend the prefix-sum Vector to match."""
        # TODO: implement
        raise NotImplementedError

    def undo(self):
        """Pop the most recent entry off the ledger and shrink the
        prefix-sum Vector to match."""
        # TODO: implement
        raise NotImplementedError

    def average_last(self, k):
        """
        Return the average of the last k entries as a float, in O(1)
        using the prefix-sum Vector (a single subtraction, then a single
        division). Return None if k <= 0 or k is greater than the current
        number of entries.
        """
        # TODO: implement
        raise NotImplementedError

    def get(self, i):
        """Return the raw entry at index i."""
        # TODO: implement
        raise NotImplementedError

    def set_(self, i, x):
        """
        Overwrite the entry at index i with x, and correctly update every
        affected prefix sum (every prefix.get(j) for j > i changes by the
        same delta = x - old_value). This one operation is allowed to be
        O(n) -- it is NOT on the hot path the complexity requirement
        above is about.
        """
        # TODO: implement
        raise NotImplementedError

    def size(self):
        # TODO: implement
        raise NotImplementedError

    def capacity(self):
        """Return the capacity of the MAIN ledger Vector (not the
        prefix-sum one) -- this is what the CAPACITY command reports."""
        # TODO: implement
        raise NotImplementedError


def fmt_avg(v):
    """Given here: format an average for printing -- "NA" if None,
    otherwise a bare integer string if it's a whole number, else 4
    decimal places. Call this from solve(); do not change it."""
    if v is None:
        return "NA"
    if v == int(v):
        return str(int(v))
    return f"{v:.4f}"


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
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
