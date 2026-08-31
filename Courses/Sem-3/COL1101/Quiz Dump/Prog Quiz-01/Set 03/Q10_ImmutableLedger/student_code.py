import sys
import threading
from typing import Any, NamedTuple

# =======================================================================
# PART A -- a purely functional, structurally-shared "persistent vector"
#
# An ordinary Python list gives you O(1) append/get/set, but only
# because it is MUTABLE: every version after the first overwrites the
# one before it. Here you build a vector where EVERY version that has
# ever existed remains valid and readable forever, and creating a new
# version from an old one never touches more than O(log n) existing
# structure -- exactly the "no full copy, ever" idea from the Timeline
# Whiteboard problem, but for a vector instead of a stack, which means
# you now need a genuine tree instead of a single chain.
#
# Structure: a PVector of `size` elements is stored as a COMPLETE
# BINARY TRIE of `height` levels, holding up to 2**height elements:
#   - if height == 0, .root IS the single stored element directly (or
#     None if size == 0, meaning the vector is completely empty).
#   - if height > 0, .root is a 2-tuple (left, right), where left and
#     right are themselves (recursively) tries of height - 1, EXCEPT
#     that a subtree which is not yet needed (because the vector's
#     current size does not reach that far) is represented by the
#     Python value None rather than being built out with dummy leaves.
#     (Only the *rightmost, not-yet-full* path of the trie should ever
#     contain a None child; every fully-used subtree must be a real,
#     complete sub-trie all the way down to height 0.)
# =======================================================================

class PVector(NamedTuple):
    root: Any     # None (empty), a leaf value (height 0), or (left, right)
    height: int   # the trie currently has capacity 2**height slots
    size: int     # how many of those slots are actually in use


EMPTY_VECTOR = PVector(None, 0, 0)


def _insert(root, height, i, x):
    """
    Return a NEW subtree, structurally identical to `root` except that
    position i (0-indexed WITHIN this subtree, 0 <= i < 2**height) now
    holds x. `root` may be None, meaning "this subtree does not exist
    yet" -- in that case you must build a brand new path of nodes down
    to a leaf at position i (every other position along the way stays
    None, since it still doesn't exist).

    This single function does BOTH jobs the finished vector needs:
      - overwriting an existing element (all subtrees on the path to i
        already exist and are real, so this is pure "path copying":
        rebuild only the O(height) nodes from the root down to the
        leaf, reusing every sibling subtree UNCHANGED via structural
        sharing);
      - extending into never-before-used capacity (some subtrees on
        the path to i are still None, so you must create fresh nodes
        for them instead of copying anything).
    You do not need to tell these two cases apart explicitly -- the
    same recursive rule ("if this subtree is None, build fresh;
    otherwise copy just this level and recurse into the correct
    child") handles both. Do not mutate any existing tuple; always
    return new tuples.
    """
    # TODO
    raise NotImplementedError


def _lookup(root, height, i):
    """Return the value stored at position i (0-indexed WITHIN this
    subtree) of the (fully-real, non-None) subtree `root` of the given
    height. You may assume the path you need is entirely non-None."""
    # TODO
    raise NotImplementedError


def pv_get(v, i):
    """Return the element at index i of PVector v. You may assume
    0 <= i < v.size. Must be O(log(v.size))."""
    # TODO
    raise NotImplementedError


def pv_set(v, i, x):
    """Return a NEW PVector, identical to v except index i now holds
    x. v itself must be completely unaffected. You may assume
    0 <= i < v.size. Must be O(log(v.size))."""
    # TODO
    raise NotImplementedError


def pv_append(v, x):
    """Return a NEW PVector with x appended as the new last element
    (at index v.size). v itself must be completely unaffected.

    If v.size is still less than the current capacity (2**v.height),
    this is exactly one _insert call at the existing height. If v is
    already at full capacity, you must first grow: create a new
    height (v.height + 1) whose root is (v.root, None) -- the entire
    old trie becomes the LEFT child of a new root, with a completely
    fresh right side -- and then _insert into THAT at the new height.
    (Convince yourself index v.size lands in the new right child
    before you rely on this.)

    Must be O(log(v.size)) worst-case (occasional height growth is
    itself only O(log n) work, not a problem the way array-doubling
    was in the Elastic Array problem)."""
    # TODO
    raise NotImplementedError


def pv_size(v):
    """Return v.size directly."""
    # TODO
    raise NotImplementedError


# =======================================================================
# PART B -- a thread-safe store of PVector versions ("the Ledger").
#
# Many threads share ONE Ledger object. Version 0 always denotes
# EMPTY_VECTOR. Every successful append_to/set_in call creates exactly
# one brand new version, numbered 1, 2, 3, ... in the order those
# calls are actually SERVICED (not necessarily the order threads
# happened to call them in -- with several threads racing, "who goes
# first" is decided by whoever the scheduler lets acquire the lock
# first, and that is fine, AS LONG AS no two calls are ever handed the
# same version number and no version number is ever skipped or handed
# out before its PVector is actually ready).
#
# The performance point of this class: building a brand new PVector
# (via pv_append / pv_set above) does not touch any shared state at
# all, so it does not need to happen while holding a lock -- only the
# tiny, final "publish this new version under the next id" step
# touches shared state (the dict of versions and the id counter), and
# THAT is the only part that must be done under a lock. If you hold a
# lock for the entire append_to/set_in call, your code will likely
# still be correct, but it serialises every reader and writer against
# each other for no reason and will visibly lose performance-marks
# against a version of this class that only locks the publish step.
# =======================================================================
class Ledger:
    def __init__(self):
        # TODO: set up your dict of version -> PVector (version 0 must
        # already map to EMPTY_VECTOR), a counter for the next id to
        # hand out, and a threading.Lock to protect BOTH of those
        # together.
        raise NotImplementedError

    def append_to(self, version_id, x):
        """Build a new PVector by appending x to version `version_id`,
        publish it as the next version, and return its new id."""
        # TODO
        raise NotImplementedError

    def set_in(self, version_id, i, x):
        """Build a new PVector by setting index i of version
        `version_id` to x, publish it as the next version, and return
        its new id. You may assume 0 <= i < size(version_id)."""
        # TODO
        raise NotImplementedError

    def get(self, version_id, i):
        """Return the element at index i of version `version_id`. You
        may assume 0 <= i < size(version_id)."""
        # TODO
        raise NotImplementedError

    def size(self, version_id):
        """Return the number of elements in version `version_id`."""
        # TODO
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you. This exercises PART A and PART B
# SEQUENTIALLY (no threads) for correctness; a separate concurrency
# test harness (not run through this driver) exercises multiple
# threads directly against a shared Ledger.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1

    ledger = Ledger()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if parts[0] == "APPEND":
            v, x = int(parts[1]), int(parts[2])
            out.append(str(ledger.append_to(v, x)))
        elif parts[0] == "SET":
            v, i, x = int(parts[1]), int(parts[2]), int(parts[3])
            out.append(str(ledger.set_in(v, i, x)))
        elif parts[0] == "GET":
            v, i = int(parts[1]), int(parts[2])
            out.append(str(ledger.get(v, i)))
        elif parts[0] == "SIZE":
            v = int(parts[1])
            out.append(str(ledger.size(v)))
        else:
            raise ValueError(f"unrecognized op: {parts}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
