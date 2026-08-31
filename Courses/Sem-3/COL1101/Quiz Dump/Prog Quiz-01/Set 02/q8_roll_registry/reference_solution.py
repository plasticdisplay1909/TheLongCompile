import sys

FREE = object()
TOMB = object()


class HashSet:
    INIT_CAP = 8

    def __init__(self):
        self._cap = self.INIT_CAP
        self._slots = [FREE] * self._cap
        self._count = 0     # live elements
        self._used = 0      # live + tombstones (occupied slots)

    def _probe(self, x):
        """Quadratic probing; returns (found, index). If found is False,
        index is the first free-or-tombstone slot suitable for insertion
        (preferring a tombstone if one was passed along the way), or the
        slot containing x if found is True."""
        h = hash(x) % self._cap
        first_tomb = -1
        for i in range(self._cap):
            idx = (h + (i * i + i) // 2) % self._cap  # triangular-number probe
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
        old_slots = self._slots
        self._cap = max(1, new_cap)
        self._slots = [FREE] * self._cap
        self._count = 0
        self._used = 0
        for slot in old_slots:
            if slot is not FREE and slot is not TOMB:
                self._raw_add(slot)

    def _raw_add(self, x):
        found, idx = self._probe(x)
        if not found:
            self._slots[idx] = x
            self._count += 1
            self._used += 1

    def _maybe_grow(self):
        if self._used / self._cap > 0.7:
            self._resize(self._cap * 2)

    def _maybe_shrink(self):
        if self._cap > self.INIT_CAP and self._count / self._cap < 0.2:
            self._resize(max(self.INIT_CAP, self._cap // 2))

    def add(self, x):
        found, idx = self._probe(x)
        if found:
            return
        self._slots[idx] = x
        self._count += 1
        self._used += 1
        self._maybe_grow()

    def remove(self, x):
        found, idx = self._probe(x)
        if not found:
            return
        self._slots[idx] = TOMB
        self._count -= 1
        self._maybe_shrink()

    def contains(self, x):
        found, _ = self._probe(x)
        return found

    def size(self):
        return self._count

    def items(self):
        return sorted((s for s in self._slots if s is not FREE and s is not TOMB), key=str)


def parse_val(tok):
    try:
        return int(tok)
    except ValueError:
        return tok


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
