import sys

# =========================================================================
# Q6 : The Interval Set  (Set ADT, built on a Sorted Doubly Linked List)
# =========================================================================
#
# A set of integers can be enormous (imagine "every integer from 0 to
# one billion except a handful of gaps"), far too large to store one
# element at a time. But if the set happens to consist of a small
# number of contiguous RANGES of integers, we can represent it far more
# compactly: as a collection of disjoint intervals. This problem asks
# you to build exactly such a representation, called an IntervalSet,
# and to support adding a range of integers to the set, removing a
# range of integers from the set, and testing membership -- all backed
# by a SORTED DOUBLY LINKED LIST of interval nodes (not a Python list,
# not a Python set, not any other built-in container to hold the
# intervals themselves).
#
# Represent each interval as the half-open range [lo, hi), i.e.
# containing every integer lo, lo+1, ..., hi-1 but NOT hi itself (this
# is exactly the Python slicing/range() convention, and it is what
# makes "adjacent" ranges like [1,5) and [5,10) unambiguously mergeable
# into [1,10) -- together they cover 1..9 with no gap and no overlap).
# At all times, the linked list must store the current set as the
# SMALLEST possible number of intervals: sorted in increasing order,
# each one non-empty, and with a gap of at least 1 between the hi of
# one interval and the lo of the next (two intervals that touch or
# overlap must always be merged into one before you return control to
# the caller -- never leave the structure in a state where two
# neighbouring nodes could have been combined into one).
#
# You must support:
#   ADD lo hi        Add every integer in [lo, hi) to the set. This may
#                     need to merge with, or completely swallow, any
#                     number of existing intervals that it overlaps or
#                     touches (see the "bridging" example in the
#                     description below). If lo >= hi, this command has
#                     no effect (it does not represent a valid range).
#   REMOVE lo hi      Remove every integer in [lo, hi) from the set.
#                     This may split an existing interval into two
#                     pieces (if [lo, hi) carves a hole out of its
#                     middle), shrink an interval from one end, or
#                     delete some number of intervals entirely, all
#                     within the same call. If lo >= hi, this command
#                     has no effect.
#   CONTAINS x        Report whether x is currently in the set.
#   COUNT_INTERVALS   Report how many intervals (linked list nodes) the
#                     set currently consists of.
#   SIZE              Report the TOTAL number of integers currently in
#                     the set (the sum of hi - lo over every interval).
#   DUMP              Print every interval, in increasing order, each
#                     formatted as "[lo,hi)", separated by single
#                     spaces -- or the literal word EMPTY if the set is
#                     currently empty.
#
# Example of a "bridging" ADD: if the set currently holds the two
# disjoint intervals [1,3) and [5,7), then ADD 0 20 must replace BOTH of
# them (and everything else) with the single interval [0,20) -- your ADD
# needs to walk however many existing intervals the new range touches,
# merge them all together with the new range, remove every one of the
# old nodes it swallowed, and insert exactly one new node in their
# place.
#
# You must implement every one of the six operations above so that each
# one only ever visits the intervals that are actually relevant to it
# (the ones near [lo, hi), or near x) rather than, say, rebuilding the
# entire linked list from scratch on every call -- a hidden performance
# test exercises tens of thousands of ADD/REMOVE calls on a coordinate
# space of size up to 10^9, which an implementation that does anything
# resembling "convert to a literal set of integers and back" will not
# survive within the time limit.


class _Node:
    """A single doubly-linked interval node, representing [lo, hi)."""
    __slots__ = ("lo", "hi", "prev", "next")

    def __init__(self, lo, hi, prev=None, next=None):
        self.lo = lo
        self.hi = hi
        self.prev = prev
        self.next = next


class IntervalSet:
    def __init__(self):
        """
        TODO: set up an empty doubly linked list (you will want head and
        tail references, both starting as None).
        """
        raise NotImplementedError

    def _insert_after(self, node, lo, hi):
        """
        Insert a brand new node representing [lo, hi) immediately after
        `node` in the linked list (or at the very front, becoming the
        new head, if node is None), fixing up every prev/next pointer
        involved (including the list's head/tail references if the new
        node becomes the new head or tail). Return the newly created
        node, so callers can use it as an anchor for further insertions.

        This is a plain doubly-linked-list "insert after" -- there is no
        interval-merging logic here; ADD and REMOVE are responsible for
        making sure they only ever ask you to insert a node that
        doesn't overlap or touch its neighbours.

        TODO: implement this.
        """
        raise NotImplementedError

    def _remove(self, node):
        """
        Unlink `node` from the doubly linked list, fixing up its
        neighbours' pointers (and the list's head/tail references if
        node was the head or tail).

        TODO: implement this.
        """
        raise NotImplementedError

    def add_range(self, lo, hi):
        """
        Implement ADD as described above.

        A reasonable approach: walk forward through the list to find
        every existing interval that overlaps OR touches [lo, hi) (i.e.
        every node with node.lo <= hi and node.hi >= lo), remember the
        node immediately before the first such interval (or None if
        there isn't one -- this is where you'll re-insert), expand
        [lo, hi) to also cover every one of those intervals, remove all
        of them from the list, and finally insert a single new node for
        the merged range right after your remembered anchor.

        TODO: implement this.
        """
        raise NotImplementedError

    def remove_range(self, lo, hi):
        """
        Implement REMOVE as described above.

        A reasonable approach: walk forward through the list to find
        every existing interval that overlaps [lo, hi) at all (i.e.
        every node with node.lo < hi and node.hi > lo). For each such
        interval, figure out what (if anything) survives on its left
        side (the part of it strictly before lo) and on its right side
        (the part of it strictly after hi), remove the original node,
        and afterwards re-insert whatever survivors there were, in
        sorted order, in the gap left behind.

        TODO: implement this.
        """
        raise NotImplementedError

    def contains(self, x):
        """
        Return True if x belongs to some interval currently in the set,
        False otherwise. You do not need to be faster than O(number of
        intervals) for this one operation, but you should still stop
        walking the list as soon as you've gone far enough to know the
        answer (you don't need to walk past the first interval whose
        lo is already greater than x).

        TODO: implement this.
        """
        raise NotImplementedError

    def count_intervals(self):
        """
        TODO: implement this (walk the list and count nodes).
        """
        raise NotImplementedError

    def total_size(self):
        """
        TODO: implement this (walk the list and sum hi - lo over every
        node).
        """
        raise NotImplementedError

    def dump(self):
        """
        Return the string DUMP should print: every interval in
        increasing order formatted as "[lo,hi)" separated by single
        spaces, or "EMPTY" if there are no intervals.

        TODO: implement this.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you, do not modify.
#
# Input format:
#   line 1        : q
#   next q lines  : one of
#                      ADD lo hi
#                      REMOVE lo hi
#                      CONTAINS x
#                      COUNT_INTERVALS
#                      SIZE
#                      DUMP
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    s = IntervalSet()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "ADD":
            s.add_range(int(parts[1]), int(parts[2]))
        elif cmd == "REMOVE":
            s.remove_range(int(parts[1]), int(parts[2]))
        elif cmd == "CONTAINS":
            out.append("YES" if s.contains(int(parts[1])) else "NO")
        elif cmd == "COUNT_INTERVALS":
            out.append(str(s.count_intervals()))
        elif cmd == "SIZE":
            out.append(str(s.total_size()))
        elif cmd == "DUMP":
            out.append(s.dump())
    print("\n".join(out))


if __name__ == "__main__":
    solve()
