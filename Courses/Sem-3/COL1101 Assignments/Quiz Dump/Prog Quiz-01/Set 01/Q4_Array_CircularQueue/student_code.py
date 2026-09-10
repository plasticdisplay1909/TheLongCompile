import sys

# =========================================================================
# Q4 : The Growable Ring Buffer  (Arrays / Amortized Analysis)
# =========================================================================
#
# Python's list already gives you a dynamic array for free, which makes
# it tempting to build a queue on top of it with list.append(x) for
# enqueue and list.pop(0) for dequeue. Don't do that here: list.pop(0)
# is Theta(n), because removing the first element of a Python list means
# shifting every remaining element one slot to the left. Over n
# dequeues that is Theta(n^2) in total -- exactly the trap this problem
# is designed to catch.
#
# Instead, you will build a DynamicCircularQueue directly on top of a
# fixed-size Python list used as a raw array (a "ring buffer"): a
# contiguous block of slots, a head index that wraps around using
# modular arithmetic, and a count of how many elements are currently
# stored. Enqueuing writes into the slot just past the current tail and
# advances virtually; dequeuing simply advances the head index and
# decrements the count -- no element is ever shifted.
#
# The one wrinkle is that a ring buffer has a fixed capacity, and yours
# must grow and shrink automatically so that operations stay amortized
# O(1) while memory usage stays proportional to the number of elements
# actually stored (never unboundedly larger). You must follow this
# EXACT policy, since some hidden test cases query the capacity
# directly and expect it to match precisely:
#
#   * The queue starts with capacity 2.
#   * Just before an enqueue that would make count exceed the current
#     capacity (i.e. count == capacity right before this enqueue), you
#     must DOUBLE the capacity (capacity = capacity * 2) before placing
#     the new element in the (now larger) buffer.
#   * Just after a dequeue, if capacity > 2 AND count <= capacity // 4
#     (integer division), you must HALVE the capacity
#     (capacity = capacity // 2). The capacity must never be allowed to
#     drop below 2.
#   * A resize (grow or shrink) must copy every currently-stored element,
#     in queue order (the current front first), into a freshly allocated
#     list of the new size, and the head index of the new buffer must be
#     reset to 0. Nothing else about resizing is unspecified.
#
# This "double when full, halve when a quarter full" policy is the
# standard way to get amortized O(1) enqueue/dequeue while guaranteeing
# the buffer is never more than a small constant factor larger than it
# needs to be -- but it only WORKS if you get the exact thresholds
# right (a queue that shrinks every time it drops below half-full, for
# instance, can be made to thrash: repeatedly resizing on alternating
# enqueue/dequeue calls, destroying the amortized bound). Test yourself
# against the last few hidden test cases in particular, which alternate
# single enqueues and dequeues right at capacity boundaries specifically
# to catch that mistake.


class DynamicCircularQueue:
    def __init__(self):
        """
        Set up an empty queue with capacity 2, an empty backing list of
        that size, head index 0, and count 0.

        TODO: implement this.
        """
        raise NotImplementedError

    def _resize(self, new_capacity):
        """
        Reallocate the backing array to have exactly new_capacity slots,
        copying the count currently-stored elements into it in queue
        order starting at index 0, and reset the head index to 0.

        TODO: implement this. (You will call this helper from enqueue
        and dequeue below -- it should never be called directly by the
        I/O driver.)
        """
        raise NotImplementedError

    def enqueue(self, x):
        """
        Insert x at the back of the queue, growing the backing array
        first (following the exact doubling rule above) if it is
        currently full.

        TODO: implement this.
        """
        raise NotImplementedError

    def dequeue(self):
        """
        Remove and return the element at the front of the queue. You may
        assume this is only called when the queue is non-empty (the I/O
        driver checks is_empty() first). After removing the element,
        shrink the backing array if the exact halving rule above applies.

        TODO: implement this.
        """
        raise NotImplementedError

    def front(self):
        """
        Return (without removing) the element at the front of the queue.
        You may assume this is only called when the queue is non-empty.

        TODO: implement this.
        """
        raise NotImplementedError

    def __len__(self):
        """
        Return the number of elements currently stored, in O(1).

        TODO: implement this.
        """
        raise NotImplementedError

    def is_empty(self):
        """
        TODO: implement this in O(1), in terms of len(self) or otherwise.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you, do not modify.
#
# Input format:
#   line 1        : q
#   next q lines  : one of
#                      ENQUEUE x
#                      DEQUEUE
#                      FRONT
#                      SIZE
#                      CAPACITY
#
# DEQUEUE and FRONT on an empty queue must print "EMPTY" instead of
# raising an error or crashing.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    dq = DynamicCircularQueue()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "ENQUEUE":
            dq.enqueue(int(parts[1]))
        elif cmd == "DEQUEUE":
            if dq.is_empty():
                out.append("EMPTY")
            else:
                out.append(str(dq.dequeue()))
        elif cmd == "FRONT":
            out.append("EMPTY" if dq.is_empty() else str(dq.front()))
        elif cmd == "SIZE":
            out.append(str(len(dq)))
        elif cmd == "CAPACITY":
            out.append(str(dq.capacity))
    print("\n".join(out))


if __name__ == "__main__":
    solve()
