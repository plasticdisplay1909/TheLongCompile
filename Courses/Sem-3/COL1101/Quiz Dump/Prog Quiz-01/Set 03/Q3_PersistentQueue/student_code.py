import sys
from typing import Any, NamedTuple

# NOTE: your reversal of `back` into `front` is written recursively, and
# its recursion depth is proportional to how many elements sit in `back`
# at that moment. The autograder raises the recursion limit before it
# calls your code, but if you want to stress-test large cases locally,
# raise it yourself first, e.g.:
#     sys.setrecursionlimit(200000)
sys.setrecursionlimit(1000000)

# ---------------------------------------------------------------------
# Given to you. Do not rename these.
# ---------------------------------------------------------------------
EMPTY = None  # the empty immutable linked list


class Cell(NamedTuple):        # one immutable linked-list cell
    value: Any
    rest: Any                  # the cells behind this one


class Q(NamedTuple):
    """
    A purely functional FIFO queue represented as TWO immutable singly
    linked lists (built from Cell above):

        front : elements due to leave the queue soonest, IN QUEUE ORDER
                (front of front-list == front of queue).
        back  : elements that arrived most recently, IN REVERSE ORDER
                (the most recent arrival is at the HEAD of back).
        count : total number of elements currently in the queue.

    The empty queue is always the exact constant Q(EMPTY, EMPTY, 0)
    (there is no separate "make an empty queue" function to write).

    You must maintain one invariant at all times, immediately after
    every enqueue/dequeue returns: front is EMPTY only if the queue as
    a whole is empty (i.e. you may never be sitting on a queue that is
    logically non-empty but whose front list happens to be EMPTY while
    back is not -- if front ever runs dry, you must immediately move
    everything out of back into front, reversing it in the process,
    before you return).
    """
    front: Any
    back: Any
    count: Any


def is_empty(q):
    """True iff q.count == 0."""
    # TODO
    raise NotImplementedError


def size(q):
    """Return q.count directly (do not walk the lists)."""
    # TODO
    raise NotImplementedError


def enqueue(q, x):
    """
    Return a NEW queue with x added as the newest (last) element.
    q itself must be left completely unchanged (nothing is ever
    mutated anywhere in this file -- Cell and Q are both NamedTuples,
    and once a name has a value inside a function it is never
    reassigned).

    Must run in O(1) worst-case time: this is the "cheap" end of the
    queue, and a fresh arrival only ever needs to be cons'd onto back.
    """
    # TODO
    raise NotImplementedError


def dequeue(q):
    """
    Return the pair (x, new_q): x is the element that has been waiting
    longest, and new_q is a new queue with x removed. q itself is left
    unchanged. You may assume q is non-empty whenever this is called.

    This is the operation with the interesting cost: if front is
    non-empty you can pop its head directly, but if front is EMPTY
    you first need to reverse the entirety of back into front (an O(n)
    walk, built with recursion, not a loop or Python's reversed()/
    [::-1]) before you can hand back the head. Because that expensive
    reversal only happens when front has just run out, and every
    element only ever gets moved from back to front ONCE over its
    lifetime in the queue, this operation is O(1) AMORTISED -- provided
    each value is dequeued only once. (You do not need to prove this in
    code; it is the subject of one of the analysis questions.)
    """
    # TODO
    raise NotImplementedError


def peek_front(q):
    """Return (without removing) the element that has been waiting
    longest. You may assume q is non-empty. This does NOT need to
    trigger the front/back rebalancing that dequeue does -- if front
    is empty you must instead look at the LAST cell of back (the
    oldest arrival still sitting in back), found however you like."""
    # TODO
    raise NotImplementedError


def to_list(q):
    """Return a Python list of every element, oldest first. May be
    O(n). Must not mutate q. Written using recursion, not a loop."""
    # TODO
    raise NotImplementedError


def from_list(xs):
    """Build a Q from a Python list xs (xs[0] is oldest), by calling
    enqueue repeatedly starting from Q(EMPTY, EMPTY, 0). Must be
    written using RECURSION over xs, not a Python for/while loop."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def run(state, operation):
    """Apply one operation; return (state, output). 'state' is a new Q
    whenever the operation changes it, and the Q passed in is left
    untouched (this function itself performs no reassignment of state
    across calls -- the caller threads it through)."""
    code = operation[0]
    if code == 1:      # enqueue x
        return enqueue(state, operation[1]), None
    elif code == 2:    # peek
        if is_empty(state):
            return state, -1
        return state, peek_front(state)
    elif code == 3:    # dequeue
        if is_empty(state):
            return state, -1
        x, new_state = dequeue(state)
        return new_state, x
    elif code == 4:    # size
        return state, size(state)
    raise ValueError(f"bad op {operation}")


def solve():
    import sys
    data = sys.stdin.read().split("\n")
    idx = 0
    q_count = int(data[idx]); idx += 1
    state = Q(EMPTY, EMPTY, 0)
    out = []
    for _ in range(q_count):
        nums = list(map(int, data[idx].split())); idx += 1
        state, result = run(state, nums)
        if result is not None:
            out.append(str(result))
    print("\n".join(out))


if __name__ == "__main__":
    solve()
