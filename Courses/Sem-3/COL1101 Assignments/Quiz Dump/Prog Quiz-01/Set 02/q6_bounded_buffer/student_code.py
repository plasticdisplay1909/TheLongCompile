import sys

# =============================================================================
# Q6: The Bounded Buffer Bakery (a deterministic producer/consumer simulator)
# =============================================================================
# This models the classic bounded-buffer / producer-consumer concurrency
# problem WITHOUT real OS threads, so that its behaviour is 100%
# reproducible: you are simulating what a semaphore + mutex would enforce,
# by hand, with explicit wait queues.
#
# There is one shared circular Buffer of fixed capacity C (implemented on
# a fixed-size array with wraparound indices -- see Buffer below). Threads
# (identified by an arbitrary string id) attempt PRODUCE or CONSUME
# operations one at a time, in the order they appear in the input:
#
#   PRODUCE tid item
#       If there is currently space in the buffer AND no other producer
#       is already waiting (fairness: nobody may cut in line ahead of an
#       earlier-blocked producer even if space exists), the item is
#       inserted immediately: log "PRODUCED <tid> <item>". Otherwise tid
#       is appended to the back of the producer wait-queue and you log
#       "BLOCKED <tid>". Immediately after a successful insertion, check
#       whether any WAITING consumers can now be served (see below).
#
#   CONSUME tid
#       Symmetric: if the buffer is non-empty AND no other consumer is
#       already waiting, remove the front item immediately: log
#       "CONSUMED <tid> <item>". Otherwise tid is appended to the back of
#       the consumer wait-queue and you log "BLOCKED <tid>". Immediately
#       after a successful removal, check whether any waiting producers
#       can now be let in (see below).
#
#   Waking up: whenever the buffer gains space (because of a successful
#   CONSUME) you must let waiting producers in, strictly in the FIFO
#   order they blocked, for as long as there is room -- for each one you
#   wake, log "WOKEN <tid> PRODUCED <item>" (using the item they *tried*
#   to produce back when they first called PRODUCE and got blocked -- you
#   must remember it). Symmetrically, whenever the buffer gains an item
#   (because of a successful PRODUCE, including one that just got woken
#   up), wake waiting consumers in FIFO order for as long as items
#   remain, logging "WOKEN <tid> CONSUMED <item>" for each.
#
#   STATUS
#       Print (see fmt_status, given to you) the buffer's current
#       contents front-to-back, and the id at the FRONT of each wait
#       queue (or "-" if that wait queue is empty). Produces no log
#       entries of its own.
#
# PERFORMANCE REQUIREMENT: both wait queues MUST support O(1) push-to-back
# and O(1) pop-from-front. Do NOT implement them with a Python list and
# list.pop(0) (that is O(n) per pop!) -- use your own linked-list-based
# queue, exactly like the ones you've already built in this course.
# =============================================================================


class Buffer:
    """A fixed-capacity circular FIFO on a preallocated array."""

    def __init__(self, capacity):
        """Store capacity; allocate a list of that length as the backing
        array; track a start index and a count -- do NOT use Python list
        insert/pop/append to manage this array's contents, only direct
        indexing (this is exactly the circular array you've seen for
        implementing a queue over a fixed-size buffer)."""
        # TODO: implement
        raise NotImplementedError

    def is_full(self):
        # TODO: implement
        raise NotImplementedError

    def is_empty(self):
        # TODO: implement
        raise NotImplementedError

    def enqueue(self, item):
        """Assume not full. O(1)."""
        # TODO: implement
        raise NotImplementedError

    def dequeue(self):
        """Assume not empty. Return the removed item. O(1)."""
        # TODO: implement
        raise NotImplementedError


class WaitQueue:
    """
    A FIFO queue of waiting thread ids (each with an attached payload --
    the item a blocked producer was trying to insert; None for
    consumers), implemented with YOUR OWN linked list so that push and
    pop are both O(1). Do not use a Python list here.
    """

    def __init__(self):
        # TODO: implement (e.g. head/tail node pointers + a count)
        raise NotImplementedError

    def push(self, tid, payload=None):
        """Add (tid, payload) to the back. O(1)."""
        # TODO: implement
        raise NotImplementedError

    def pop(self):
        """Remove and return the (tid, payload) at the front. O(1).
        Assume non-empty."""
        # TODO: implement
        raise NotImplementedError

    def peek(self):
        """Return (without removing) the (tid, payload) at the front.
        Assume non-empty."""
        # TODO: implement
        raise NotImplementedError

    def is_empty(self):
        # TODO: implement
        raise NotImplementedError


class Bakery:
    def __init__(self, capacity):
        """Set up: self.buf = Buffer(capacity), an empty producer_wait and
        consumer_wait WaitQueue each, and self.log = [] (a plain list you
        append formatted strings to -- see the docstrings above for the
        exact strings expected)."""
        # TODO: implement
        raise NotImplementedError

    def _wake_producers_if_possible(self):
        """While there is a waiting producer AND the buffer has room,
        pop the front of producer_wait, insert their remembered item,
        and log "WOKEN <tid> PRODUCED <item>"."""
        # TODO: implement
        raise NotImplementedError

    def _wake_consumers_if_possible(self):
        """Symmetric to the above, for consumers."""
        # TODO: implement
        raise NotImplementedError

    def produce(self, tid, item):
        # TODO: implement (see the PRODUCE spec above; remember to try
        # waking consumers after a successful, immediate insertion)
        raise NotImplementedError

    def consume(self, tid):
        # TODO: implement (see the CONSUME spec above; remember to try
        # waking producers after a successful, immediate removal)
        raise NotImplementedError

    def status(self):
        """Return the STATUS line. You are given fmt_status below to do
        the actual string formatting -- just gather the pieces:
        the buffer contents front-to-back as a list, the tid at the
        front of producer_wait (or None if empty), and the tid at the
        front of consumer_wait (or None if empty)."""
        # TODO: implement (call fmt_status(items, p_front, c_front) and
        # return its result)
        raise NotImplementedError


def fmt_status(items, p_front, c_front):
    """Given here: exact STATUS formatting -- do not change."""
    p = p_front if p_front is not None else "-"
    c = c_front if c_front is not None else "-"
    return f"BUF[{','.join(map(str, items))}] PWAIT={p} CWAIT={c}"


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    cap = int(data[idx]); idx += 1
    bakery = Bakery(cap)
    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        before = len(bakery.log)
        if cmd == "PRODUCE":
            bakery.produce(parts[1], parts[2])
        elif cmd == "CONSUME":
            bakery.consume(parts[1])
        elif cmd == "STATUS":
            out.append(bakery.status())
            continue
        else:
            raise ValueError(cmd)
        out.extend(bakery.log[before:])
    print("\n".join(out))


if __name__ == "__main__":
    solve()
