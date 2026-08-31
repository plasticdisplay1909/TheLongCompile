import sys

# =============================================================================
# Q7: Skyline Renovation (classic stack applications, built from scratch)
# =============================================================================
# A histogram of building heights is revealed one building at a time
# (APPEND h adds a new building at the right end; REMOVE_LAST undoes the
# most recent APPEND). At any point you must be able to answer three
# classic queries, each of which is normally solved with a MONOTONIC
# STACK -- and you must implement your OWN Stack class from scratch (no
# using a Python list directly as the stack in Skyline's methods; go
# through your Stack's push/pop/peek/is_empty).
#
#   SPAN i         -- the "stock span": how many consecutive bars ending
#                      at index i (going left, including i itself) have
#                      height <= heights[i]. Formally the largest k such
#                      that heights[i-k+1..i] are all <= heights[i] (a
#                      taller bar anywhere in that run stops the count).
#                      Must be answered using the span value you computed
#                      WHEN i was appended (see below) -- not recomputed
#                      from scratch on every query.
#   NEXTGREATER i  -- the smallest index j > i with heights[j] STRICTLY
#                      greater than heights[i] (equal doesn't count), or
#                      -1 if no such j exists among buildings currently
#                      present.
#   MAXRECT        -- the area of the largest axis-aligned rectangle that
#                      fits under the current skyline (the classic
#                      "largest rectangle in a histogram" problem).
#
# APPEND must run in O(1) AMORTISED time (maintain a monotonically
# decreasing-height stack of indices incrementally, exactly like the
# classic single-pass stock-span algorithm -- do not rescan everything on
# every append). NEXTGREATER and MAXRECT MAY be recomputed from scratch
# on each call in O(current number of buildings) using a fresh monotonic
# stack scan -- that is intended and acceptable here. REMOVE_LAST MAY
# also cost O(current number of buildings) (you are allowed to rebuild
# your incremental span bookkeeping from scratch after an undo -- getting
# an O(1) undo working correctly is extra-credit-hard and NOT required).
# =============================================================================


class Stack:
    """A plain array-backed stack. Implement this yourself -- Skyline's
    methods below must route every push/pop/peek through an instance of
    THIS class, not a bare Python list."""

    def __init__(self):
        # TODO: implement
        raise NotImplementedError

    def push(self, x):
        # TODO: implement
        raise NotImplementedError

    def pop(self):
        """Remove and return the top item. Assume non-empty."""
        # TODO: implement
        raise NotImplementedError

    def peek(self):
        """Return (without removing) the top item. Assume non-empty."""
        # TODO: implement
        raise NotImplementedError

    def is_empty(self):
        # TODO: implement
        raise NotImplementedError

    def size(self):
        # TODO: implement
        raise NotImplementedError


class Skyline:
    def __init__(self):
        """
        Set up:
          self.heights          -- list of building heights seen so far
          self.span             -- self.span[i] is the SPAN value computed
                                     for building i at the moment it was
                                     appended (frozen after that, until a
                                     REMOVE_LAST forces a rebuild)
          self.span_stack_idx   -- a Stack of indices with strictly
                                     decreasing heights.append.., used to
                                     maintain self.span incrementally
        (you're free to use different field names as long as the public
        methods below behave as documented)
        """
        # TODO: implement
        raise NotImplementedError

    def append(self, h):
        """
        Add h as the new last building height, in O(1) amortised time:
        pop every index off span_stack_idx whose height is <= h,
        accumulating their own span values into a running count (this is
        exactly how the classic single-pass stock-span algorithm works --
        think about WHY summing the popped spans, rather than just
        counting the popped indices, gives the right total), then push
        this new index on top. Store the resulting count in self.span.
        """
        # TODO: implement
        raise NotImplementedError

    def remove_last(self):
        """
        Undo the most recent append: drop the last height and the last
        span entry, then rebuild self.span and self.span_stack_idx from
        scratch by replaying append-like logic over the remaining
        self.heights (an O(current n) rebuild is fine -- see the note
        above).
        """
        # TODO: implement
        raise NotImplementedError

    def span_at(self, i):
        """O(1): just look up the frozen span value for building i."""
        # TODO: implement
        raise NotImplementedError

    def next_greater(self, i):
        """
        From scratch, using your own Stack, find the nearest j > i with
        heights[j] > heights[i] (strictly), else -1. (Classic
        right-to-left monotonic stack scan; O(current n) is fine.)
        """
        # TODO: implement
        raise NotImplementedError

    def max_rect(self):
        """
        From scratch, using your own Stack, compute the area of the
        largest rectangle under the current histogram (classic monotonic
        stack "largest rectangle in histogram" algorithm -- treat the
        far right as one extra bar of height 0 to flush the stack).
        O(current n) is fine.
        """
        # TODO: implement
        raise NotImplementedError


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    sky = Skyline()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "APPEND":
            sky.append(int(parts[1]))
        elif cmd == "REMOVE_LAST":
            sky.remove_last()
        elif cmd == "MAXRECT":
            out.append(str(sky.max_rect()))
        elif cmd == "NEXTGREATER":
            out.append(str(sky.next_greater(int(parts[1]))))
        elif cmd == "SPAN":
            out.append(str(sky.span_at(int(parts[1]))))
        else:
            raise ValueError(cmd)
    print("\n".join(out))


if __name__ == "__main__":
    solve()
