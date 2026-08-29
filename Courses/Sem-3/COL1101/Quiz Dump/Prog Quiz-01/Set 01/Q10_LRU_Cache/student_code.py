import sys

# =========================================================================
# Q10 : The LRU Cache  (Capstone: Linked Lists + a Hash Map, worst-case O(1))
# =========================================================================
#
# This is the hardest problem in this set, and it asks you to combine
# almost everything from the course so far into a single data
# structure: a Least-Recently-Used (LRU) cache of fixed capacity,
# supporting PUT and GET, BOTH in worst-case O(1) time -- not amortized,
# not "usually fast", but O(1) on every single call, exactly the way
# the Ladder List problem demanded worst-case O(log n) rather than
# merely amortized O(log n).
#
# The cache stores up to `capacity` distinct (key, value) pairs. Every
# time a key is accessed -- by a successful GET, or by a PUT that
# touches it (whether inserting it fresh or updating its value) -- that
# key becomes the "most recently used" (MRU) one. Whenever a PUT would
# need to insert a brand new key while the cache is already at capacity,
# the "least recently used" (LRU) key -- the one that has gone the
# longest without being touched -- is evicted to make room, and only
# then is the new key inserted.
#
# Concretely:
#   PUT key value   If key is already present, update its value and
#                    mark it as most recently used. Otherwise, insert
#                    it as most recently used; if this would make the
#                    cache exceed its capacity, first evict whichever
#                    key is currently least recently used.
#   GET key          If key is present, mark it as most recently used
#                    and return its value. If key is not present,
#                    return "NULL" and do not otherwise affect the
#                    cache.
#   SIZE             Report the number of keys currently stored.
#   CAPACITY         Report the cache's fixed capacity.
#   KEYS_MRU_TO_LRU  Report every key currently stored, ordered from
#                     most recently used to least recently used,
#                     space-separated -- or "NONE" if the cache is
#                     currently empty. (This exists purely so you, and
#                     the grader, can directly check that your notion of
#                     "recency order" is exactly right -- a subtly wrong
#                     LRU implementation often still passes basic
#                     GET/PUT tests by coincidence while getting the
#                     eviction ORDER wrong under more elaborate access
#                     patterns.)
#
# Why a dict alone isn't enough: a plain dict gives you O(1) lookup by
# key, but it does not give you a fast way to find "the key that was
# least recently touched" -- maintaining that ordering by hand (e.g. by
# scanning, or by keeping a separate Python list you re-sort or
# re-search on every access) reduces at least one of GET/PUT to O(n) or
# worse. Why a linked list alone isn't enough: a linked list gives you
# O(1) insertion/removal at either end once you already have a
# reference to the right node, and O(1) "move this node to the front"
# once you have a reference to it -- but finding WHICH node corresponds
# to a given key, from the key alone, is O(n) without something extra.
#
# The standard solution -- which you must implement -- combines the
# two: a DOUBLY LINKED LIST of nodes ordered from most-recently-used
# (right after the head sentinel) to least-recently-used (right before
# the tail sentinel), together with a dict mapping each key directly to
# its node in that list. Looking up a key is an O(1) dict lookup;
# once you have the node, unlinking it from wherever it currently sits
# and re-inserting it at the MRU end are both O(1) doubly-linked-list
# operations; evicting the LRU key means reading off tail.prev (O(1))
# and unlinking it (O(1)) and deleting its entry from the dict (O(1)).
# Every operation this cache needs to perform is therefore O(1)
# worst-case, PROVIDED you actually keep a node-reference in the dict
# (rather than, say, storing keys in the dict and re-searching the
# linked list to find the matching node -- that would silently turn
# every operation back into O(n), and is exactly the mistake several of
# the large hidden performance tests below are designed to catch).
#
# A dummy head sentinel and a dummy tail sentinel (two extra nodes that
# never hold real data, always present, with the head sentinel's `next`
# initially pointing at the tail sentinel and vice versa) make the
# linked-list bookkeeping considerably less fiddly, since every real
# node then always has a genuine, non-None node on both sides -- you
# never need to special-case "inserting into an empty list" or
# "removing the only node". You are strongly encouraged to use them,
# though you are free to structure the linked list differently if you
# are confident your version is correct.


class _DNode:
    """A single doubly-linked-list node holding one (key, value) pair
    (or, for the two sentinels, holding no meaningful key/value at all)."""
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        """
        capacity : int, the fixed maximum number of (key, value) pairs
        this cache may hold at once.

        TODO: store capacity as self.capacity (the I/O driver reads this
        attribute directly for the CAPACITY command), set up an empty
        dict from key to node, and an empty doubly linked list
        represented via a head sentinel and a tail sentinel (both
        _DNode instances holding no real data), linked directly to each
        other so the list starts genuinely empty.
        """
        raise NotImplementedError

    def _remove_node(self, node):
        """
        Unlink `node` from wherever it currently sits in the doubly
        linked list (node is guaranteed to actually be in the list, and
        is guaranteed NOT to be either sentinel), fixing up its
        neighbours' prev/next pointers. This does NOT touch the dict --
        callers are responsible for that.

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def _insert_front(self, node):
        """
        Insert `node` (not currently in the list) immediately after the
        head sentinel, i.e. as the new most-recently-used entry. This
        does NOT touch the dict -- callers are responsible for that.

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def _touch(self, node):
        """
        Mark an EXISTING node (already linked somewhere in the list) as
        the new most-recently-used entry, by moving it to the front.
        A reasonable implementation calls _remove_node then
        _insert_front on the very same node object -- do not create a
        new node here, since the dict already holds a reference to this
        exact node.

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def get(self, key):
        """
        If key is present, mark its node as most recently used and
        return its value. If key is absent, return None (the I/O driver
        below turns a None return into the printed string "NULL" for
        you -- you do not need to worry about that formatting here).

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def put(self, key, value):
        """
        Implement PUT as described above: update-and-touch if key is
        already present; otherwise insert as most-recently-used,
        evicting the current least-recently-used entry first if the
        cache is already at capacity.

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def size(self):
        """
        Return the number of (key, value) pairs currently stored, in
        O(1) (do not walk the linked list to count).

        TODO: implement this.
        """
        raise NotImplementedError

    def keys_mru_to_lru(self):
        """
        Return a Python list of every key currently stored, in order
        from most recently used to least recently used, by walking the
        doubly linked list from the head sentinel's next node up to
        (but not including) the tail sentinel.

        TODO: implement this.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you, do not modify.
#
# Input format:
#   line 1        : capacity
#   line 2        : q
#   next q lines  : one of
#                      PUT key value    (key and value are both treated
#                                        as plain strings/tokens -- do
#                                        not assume they are numeric)
#                      GET key
#                      SIZE
#                      CAPACITY
#                      KEYS_MRU_TO_LRU
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    capacity = int(data[idx]); idx += 1
    q = int(data[idx]); idx += 1
    cache = LRUCache(capacity)
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "PUT":
            cache.put(parts[1], parts[2])
        elif cmd == "GET":
            result = cache.get(parts[1])
            out.append("NULL" if result is None else result)
        elif cmd == "SIZE":
            out.append(str(cache.size()))
        elif cmd == "CAPACITY":
            out.append(str(cache.capacity))
        elif cmd == "KEYS_MRU_TO_LRU":
            keys = cache.keys_mru_to_lru()
            out.append(" ".join(keys) if keys else "NONE")
    print("\n".join(out))


if __name__ == "__main__":
    solve()
