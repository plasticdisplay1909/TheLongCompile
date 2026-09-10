import sys

# ---------------------------------------------------------------------
# 0. A stack augmented with running min/max -- given to you, fully
#    implemented. Every node remembers not just its value but the
#    minimum and maximum of everything AT OR BELOW it in the stack, so
#    peek_min()/peek_max() on the whole stack are O(1): they are just
#    the running min/max stored at the current top.
# ---------------------------------------------------------------------
class _SNode:
    __slots__ = ("value", "running_min", "running_max", "below")

    def __init__(self, value, running_min, running_max, below):
        self.value = value
        self.running_min = running_min
        self.running_max = running_max
        self.below = below


class MinMaxStack:
    """A LIFO stack where push/pop/peek/peek_min/peek_max/is_empty/
    __len__ are all O(1). Fully implemented -- use it as-is; you
    should not need to modify this class."""

    def __init__(self):
        self._top = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def push(self, x):
        if self._top is None:
            rmin, rmax = x, x
        else:
            rmin = min(x, self._top.running_min)
            rmax = max(x, self._top.running_max)
        self._top = _SNode(x, rmin, rmax, self._top)
        self._size += 1

    def pop(self):
        node = self._top
        self._top = node.below
        self._size -= 1
        return node.value

    def peek(self):
        return self._top.value

    def peek_min(self):
        """You may assume the stack is non-empty when this is called."""
        return self._top.running_min

    def peek_max(self):
        """You may assume the stack is non-empty when this is called."""
        return self._top.running_max


# ---------------------------------------------------------------------
# 1. You implement this: a FIFO queue that additionally supports
#    get_min() and get_max() over its CURRENT contents, all four core
#    operations in O(1) AMORTISED time (get_min/get_max may assume the
#    queue is non-empty when called; enqueue/dequeue may be called
#    freely in any order).
#
#    You are NOT permitted to use collections.deque anywhere in this
#    file, and you may not scan the whole queue inside get_min/get_max
#    (that would be O(n), not O(1)).
#
#    The construction you are expected to (re)discover: build the
#    queue out of exactly TWO MinMaxStack objects, `_in_stack` (new
#    arrivals get pushed here) and `_out_stack` (dequeues come from
#    here). This is the classical "implement a queue using two
#    stacks" trick -- when `_out_stack` runs dry, you reverse the
#    entirety of `_in_stack` onto it by repeated pop/push (each
#    element only ever makes that trip once over its lifetime in the
#    queue, which is exactly why this is O(1) AMORTISED and not O(1)
#    worst-case). Once you have that working as a plain queue, getting
#    get_min/get_max for free is just: the minimum (or maximum) over
#    the whole queue is the smaller (or larger) of
#    `_in_stack.peek_min()` and `_out_stack.peek_min()` (treating an
#    empty stack as +infinity for min / -infinity for max) -- because
#    MinMaxStack already tracks exactly that internally, in O(1), for
#    each half of the queue.
# ---------------------------------------------------------------------
class MinMaxQueue:
    def __init__(self):
        # TODO: set up your two MinMaxStack objects.
        raise NotImplementedError

    def __len__(self):
        """Must be O(1)."""
        # TODO
        raise NotImplementedError

    def enqueue(self, x):
        """Add x as the new last element. Must be O(1) worst-case."""
        # TODO
        raise NotImplementedError

    def dequeue(self):
        """Remove and return the current first element. You may assume
        the queue is non-empty. Must be O(1) AMORTISED."""
        # TODO
        raise NotImplementedError

    def get_min(self):
        """Return the minimum element currently in the queue (anywhere,
        not just the front/back). You may assume the queue is
        non-empty. Must be O(1) worst-case."""
        # TODO
        raise NotImplementedError

    def get_max(self):
        """Return the maximum element currently in the queue. You may
        assume the queue is non-empty. Must be O(1) worst-case."""
        # TODO
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1

    mq = MinMaxQueue()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if parts[0] == "ENQ":
            mq.enqueue(int(parts[1]))
        elif parts[0] == "DEQ":
            out.append(str(mq.dequeue()))
        elif parts[0] == "MIN":
            out.append(str(mq.get_min()))
        elif parts[0] == "MAX":
            out.append(str(mq.get_max()))
        elif parts[0] == "SIZE":
            out.append(str(len(mq)))
        else:
            raise ValueError(f"unrecognized op: {parts}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
