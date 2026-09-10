import threading
import collections

# ---------------------------------------------------------------------
# A tiny bakery runs one display case that holds at most `capacity`
# trays of bread at any instant. Bakers (producers) keep sliding
# fresh trays onto the case; customers (consumers) keep taking trays
# off it. Both sides run as separate threads, all sharing this ONE
# BoundedBuffer object, and none of them may ever observe or cause a
# corrupted case: no tray may be handed to two customers, no tray may
# vanish, and the case must never appear to hold more than `capacity`
# trays or a negative number of trays.
# ---------------------------------------------------------------------


class BoundedBuffer:
    """
    A thread-safe bounded FIFO buffer of fixed capacity.

    RULES (read all of them before writing a single line):
      * You may use threading.Lock, threading.Condition, and
        threading.Semaphore, in any combination. You may NOT use
        queue.Queue, queue.SimpleQueue, multiprocessing, or asyncio
        anywhere in this file -- you are building the primitive that
        those modules hide from you.
      * put(item) must BLOCK (the calling thread must actually go to
        sleep, not spin in a `while ...: pass` or `while ...:
        time.sleep(0.001)` busy-loop) whenever the buffer is already
        at capacity, until some other thread removes an item and there
        is room. It must then insert the item and return.
      * get() must BLOCK whenever the buffer is empty, until some
        other thread inserts an item, then remove and return the
        OLDEST item currently in the buffer (FIFO order) and return.
      * Multiple producer threads may call put() concurrently with
        each other and with multiple consumer threads calling get()
        concurrently -- your implementation must be correct under
        ANY interleaving the scheduler chooses, not just the
        interleavings you happened to test locally. In particular: two
        puts must never silently overwrite each other's item, two gets
        must never return the same item twice, and the buffer's
        reported size must always match what is really inside it.
      * The internal storage you keep the waiting items in may be a
        plain Python list used ONLY as a FIFO (e.g. via
        collections.deque, which is already imported for you) --
        the graded part of this problem is the SYNCHRONISATION, not
        reinventing a linked queue again.
    """

    def __init__(self, capacity):
        """capacity is a positive integer: the maximum number of items
        the buffer may hold at once."""
        # TODO: set up your storage (a collections.deque is fine), a
        # Lock/Condition (or Semaphores) to protect it, and remember
        # capacity.
        raise NotImplementedError

    def put(self, item):
        """Block until there is room, then insert item at the back."""
        # TODO
        raise NotImplementedError

    def get(self):
        """Block until an item is available, then remove and return
        the item at the front (FIFO)."""
        # TODO
        raise NotImplementedError

    def qsize(self):
        """Return the number of items currently in the buffer. This is
        only used for diagnostics between test phases and does not
        need to be perfectly synchronised with concurrent activity."""
        # TODO
        raise NotImplementedError
