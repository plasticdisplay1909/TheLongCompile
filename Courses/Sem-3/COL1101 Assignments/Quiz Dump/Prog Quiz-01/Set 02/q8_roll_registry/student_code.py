import sys

# =============================================================================
# Q8: The Roll Number Registry (a Set ADT built on your own hash table)
# =============================================================================
# Implement HashSet from scratch using OPEN ADDRESSING with QUADRATIC
# (triangular-number) probing and TOMBSTONES for deletion. You may NOT use
# Python's built-in set, frozenset, or dict as the underlying storage --
# the only allowed backing store is a single fixed-size Python list of
# "slots" (self._slots), each of which holds one of: an actual element, a
# FREE sentinel (given to you), or a TOMB sentinel (given to you, meaning
# "an element used to be here but was removed -- keep probing past me").
#
# Probe sequence (given to you, in _probe -- do not change the formula):
#   idx_i = (hash(x) + i*(i+1)//2) mod capacity,   i = 0, 1, 2, ...
# This particular formula is guaranteed to visit every slot exactly once
# before repeating AS LONG AS capacity is a power of two -- which is why
# INIT_CAP is 8 and every resize below multiplies or divides by exactly 2.
#
# Resizing policy (must be followed exactly -- it drives amortised O(1)):
#   - After a successful add() that increases the number of OCCUPIED
#     slots (live elements + tombstones) past 70% of capacity, double the
#     capacity and rehash every live element into a fresh table (dropping
#     all tombstones in the process -- a resize is also how you reclaim
#     tombstone space).
#   - After a successful remove() that drops the number of LIVE elements
#     below 20% of capacity, halve the capacity (never below INIT_CAP)
#     and rehash, exactly the same way.
# =============================================================================


FREE = object()   # sentinel: this slot has never been used
TOMB = object()   # sentinel: this slot held an element that was removed


class HashSet:
    INIT_CAP = 8

    def __init__(self):
        """Set up: self._cap = INIT_CAP, self._slots = a list of INIT_CAP
        FREE sentinels, self._count = 0 (live elements), self._used = 0
        (live elements + tombstones -- i.e. occupied slots)."""
        # TODO: implement
        raise NotImplementedError

    def _probe(self, x):
        """
        Given here -- do not change. Walks the probe sequence for x.
        Returns (True, idx) if x is already present at idx. Returns
        (False, idx) otherwise, where idx is the best slot to insert x
        into (the FIRST tombstone encountered along the way if any were
        seen, otherwise the first FREE slot reached).
        """
        h = hash(x) % self._cap
        first_tomb = -1
        for i in range(self._cap):
            idx = (h + (i * i + i) // 2) % self._cap
            slot = self._slots[idx]
            if slot is FREE:
                return False, (first_tomb if first_tomb != -1 else idx)
            if slot is TOMB:
                if first_tomb == -1:
                    first_tomb = idx
                continue
            if slot == x:
                return True, idx
        return False, first_tomb

    def _resize(self, new_cap):
        """
        Rebuild the table at the new capacity: allocate a fresh
        all-FREE slot list of length new_cap, reset self._count and
        self._used to 0, then re-insert (via _raw_add, given to you
        below) every currently-LIVE element from the old table (skip
        FREE and TOMB slots -- tombstones are simply dropped).
        """
        # TODO: implement
        raise NotImplementedError

    def _raw_add(self, x):
        """Given here -- a resize-time-only insert that assumes x is not
        already present (true by construction right after a resize) and
        does NOT itself trigger another resize."""
        found, idx = self._probe(x)
        if not found:
            self._slots[idx] = x
            self._count += 1
            self._used += 1

    def _maybe_grow(self):
        """If occupied slots (self._used) exceed 70% of capacity, double
        the capacity via self._resize."""
        # TODO: implement
        raise NotImplementedError

    def _maybe_shrink(self):
        """If live elements (self._count) fall below 20% of capacity,
        halve the capacity via self._resize (never below INIT_CAP)."""
        # TODO: implement
        raise NotImplementedError

    def add(self, x):
        """
        No-op if x is already present. Otherwise probe for an insertion
        slot, place x there, increment self._count and self._used, then
        call self._maybe_grow().
        """
        # TODO: implement
        raise NotImplementedError

    def remove(self, x):
        """
        No-op if x is not present. Otherwise overwrite that slot with
        TOMB, decrement self._count (NOT self._used -- the slot is still
        "occupied" by a tombstone until the next resize), then call
        self._maybe_shrink().
        """
        # TODO: implement
        raise NotImplementedError

    def contains(self, x):
        # TODO: implement
        raise NotImplementedError

    def size(self):
        """O(1): return self._count."""
        # TODO: implement
        raise NotImplementedError

    def items(self):
        """Return a list of every live element, SORTED using key=str
        (so mixed int/string elements compare consistently -- sorting
        does not need to be fast, correctness/determinism is the point)."""
        # TODO: implement
        raise NotImplementedError


def parse_val(tok):
    """Given here: elements are ints when possible, else treated as
    plain strings (so both `ADD A 5` and `ADD A rollnum7` work)."""
    try:
        return int(tok)
    except ValueError:
        return tok


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    registry = {}
    out = []

    def get(name):
        if name not in registry:
            registry[name] = HashSet()
        return registry[name]

    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "CREATE":
            registry[parts[1]] = HashSet()
        elif cmd == "ADD":
            get(parts[1]).add(parse_val(parts[2]))
        elif cmd == "REMOVE":
            get(parts[1]).remove(parse_val(parts[2]))
        elif cmd == "CONTAINS":
            out.append("YES" if get(parts[1]).contains(parse_val(parts[2])) else "NO")
        elif cmd == "SIZE":
            out.append(str(get(parts[1]).size()))
        elif cmd == "ITEMS":
            out.append(",".join(str(v) for v in get(parts[1]).items()))
        elif cmd == "UNION":
            a, b, dest = parts[1], parts[2], parts[3]
            s = HashSet()
            for v in get(a).items():
                s.add(v)
            for v in get(b).items():
                s.add(v)
            registry[dest] = s
        elif cmd == "INTERSECT":
            a, b, dest = parts[1], parts[2], parts[3]
            s = HashSet()
            bset = get(b)
            for v in get(a).items():
                if bset.contains(v):
                    s.add(v)
            registry[dest] = s
        elif cmd == "DIFF":
            a, b, dest = parts[1], parts[2], parts[3]
            s = HashSet()
            bset = get(b)
            for v in get(a).items():
                if not bset.contains(v):
                    s.add(v)
            registry[dest] = s
        else:
            raise ValueError(cmd)
    print("\n".join(out))


if __name__ == "__main__":
    solve()
