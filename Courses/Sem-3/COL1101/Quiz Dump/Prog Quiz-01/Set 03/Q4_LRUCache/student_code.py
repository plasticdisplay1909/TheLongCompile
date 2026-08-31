import sys

# ---------------------------------------------------------------------
# Node class -- given to you.
# ---------------------------------------------------------------------
class Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next


class LRUCache:
    """
    A fixed-capacity key -> value cache. Both operations below must run
    in O(1) worst-case time, which is only possible by combining TWO
    structures that point into each other:

        - a dict mapping key -> Node, for O(1) lookup by key;
        - a doubly linked list of those SAME Node objects, kept ordered
          from most-recently-used (front) to least-recently-used (back),
          so the node to evict is always exactly the one at the back.

    You are NOT permitted to use collections.OrderedDict or
    functools.lru_cache anywhere in this file -- the entire point of the
    exercise is to build the mechanism they hide from you.

    Use a sentinel node (as in the Roundabout problem) if you like, or
    two explicit head/tail pointers -- your choice, but document it.
    """

    def __init__(self, capacity):
        """capacity is a positive integer: the maximum number of
        (key, value) pairs the cache may hold at once."""
        # TODO: set up your dict, your linked list, and remember capacity.
        raise NotImplementedError

    def get(self, key):
        """
        If key is currently in the cache, return its value AND mark it
        as the most recently used entry (move its node to the front of
        the list). If key is not present, return -1 and change nothing.

        Must be O(1) worst-case.
        """
        # TODO
        raise NotImplementedError

    def put(self, key, value):
        """
        Insert or update key -> value, and mark it as the most recently
        used entry.

        - If key is already present, update its value in place and move
          it to the front (do NOT treat this as an eviction-triggering
          insertion -- updating an existing key never evicts anything).
        - If key is new and the cache is already at capacity, you must
          first evict the current least-recently-used entry (the one at
          the back of the list) before inserting the new one.
        - If key is new and the cache has spare room, just insert it at
          the front.

        Must be O(1) worst-case.
        """
        # TODO
        raise NotImplementedError

    def size(self):
        """Return the number of entries currently stored. O(1)."""
        # TODO
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    first = data[idx].split(); idx += 1
    capacity, q = int(first[0]), int(first[1])

    cache = LRUCache(capacity)
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if parts[0] == "PUT":
            cache.put(int(parts[1]), int(parts[2]))
        elif parts[0] == "GET":
            out.append(str(cache.get(int(parts[1]))))
        elif parts[0] == "SIZE":
            out.append(str(cache.size()))
        else:
            raise ValueError(f"unrecognized op: {parts}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
