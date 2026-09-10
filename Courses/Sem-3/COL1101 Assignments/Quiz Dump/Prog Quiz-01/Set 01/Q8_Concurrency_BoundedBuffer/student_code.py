import sys
import threading

# =========================================================================
# Q8 : The Bounded Buffer  (Concurrency)
# =========================================================================
#
# You are implementing the classic Producer-Consumer synchronization
# problem: a fixed-capacity buffer shared between some number of
# producer threads and some number of consumer threads. A producer
# calls put(item) to add an item to the buffer; if the buffer is
# currently full, put() must BLOCK (the calling thread must sleep,
# consuming no CPU, rather than spin-checking in a loop) until a
# consumer makes room. A consumer calls get() to remove and return the
# oldest item in the buffer (FIFO order); if the buffer is currently
# empty, get() must BLOCK until a producer adds something.
#
# You must implement this using threading.Lock and threading.Condition
# from Python's standard library -- NOT queue.Queue, NOT
# multiprocessing, and NOT a manual busy-wait loop (e.g. "while full:
# time.sleep(0.001)"), which technically produces correct answers here
# but wastes CPU and is not what this exercise is about. A Condition
# variable lets a thread release its lock and go to sleep in one atomic
# step, and be woken up efficiently by another thread the moment the
# condition it's waiting for might have become true -- that is the
# mechanism you are practising.
#
# Concretely, implement the class BoundedBuffer below with:
#   __init__(self, capacity)  Set up an empty buffer of the given fixed
#                             capacity.
#   put(self, item)           Block, without busy-waiting, until there
#                             is room in the buffer, then insert `item`
#                             at the back and wake up any consumer
#                             thread that might be waiting for a new
#                             item.
#   get(self)                 Block, without busy-waiting, until the
#                             buffer is non-empty, then remove and
#                             return the item at the front, and wake up
#                             any producer thread that might be waiting
#                             for room to open up.
#
# A standard, robust design uses ONE lock together with TWO Condition
# objects built on that same lock -- conventionally called not_full and
# not_empty -- so that a thread blocked in put() is only ever woken up
# by a get() (and vice versa), rather than every waiting thread being
# woken on every single change (which would still be correct, but is
# needlessly wasteful). You are free to use a single shared Condition
# instead if you prefer, as long as your implementation is genuinely
# free of race conditions and busy-waiting.
#
# IMPORTANT: whenever you wait on a condition, you MUST re-check the
# condition you were waiting for in a while-loop after waking up (not
# an if-statement) -- "spurious wakeups", and the fact that several
# threads can be woken for the same event but only one of them can
# actually proceed, are exactly why "while condition_not_yet_true:
# cond.wait()" is the correct pattern and "if condition_not_yet_true:
# cond.wait()" is not.
#
# The rest of this file (below the class) is a complete driver that
# spins up several producer and consumer threads against your
# BoundedBuffer, has every producer generate a distinct sequence of
# tagged items, has every consumer collect whatever items it manages to
# get, and then checks (once every thread has finished) that:
#   (a) every single item that was produced was consumed exactly once
#       (nothing lost, nothing duplicated, nothing left behind), and
#   (b) the total count of consumed items matches the total count of
#       produced items.
# It prints "OK" followed by the total number of items successfully
# accounted for if both checks pass, or "FAIL" otherwise. A correct,
# deadlock-free BoundedBuffer will always print "OK" here -- if your
# program prints "FAIL", hangs forever (until the grader's timeout
# kills it), or crashes, that means your synchronization has a bug
# (most commonly: waking the wrong condition, checking a condition with
# `if` instead of `while`, or a lock that isn't actually held while the
# shared buffer is being read or written).


class BoundedBuffer:
    def __init__(self, capacity):
        """
        TODO: set up an empty buffer (of whatever underlying container
        you like) together with the lock/condition-variable machinery
        described above.
        """
        raise NotImplementedError

    def put(self, item):
        """
        TODO: implement this as described above.
        """
        raise NotImplementedError

    def get(self):
        """
        TODO: implement this as described above.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------
# Driver -- given to you, do not modify.
#
# Input format:
#   line 1 : capacity
#   line 2 : number of producer threads
#   line 3 : number of items EACH producer thread will produce
#   line 4 : number of consumer threads
#
# Output: two lines, "OK" or "FAIL", followed by the number of items
# successfully consumed and verified.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    capacity = int(data[idx]); idx += 1
    num_producers = int(data[idx]); idx += 1
    items_per_producer = int(data[idx]); idx += 1
    num_consumers = int(data[idx]); idx += 1

    buf = BoundedBuffer(capacity)
    total_items = num_producers * items_per_producer
    consumed = []
    consumed_lock = threading.Lock()

    def producer(pid):
        for i in range(items_per_producer):
            buf.put((pid, i))

    consumed_total = [0]

    def consumer():
        while True:
            with consumed_lock:
                if consumed_total[0] >= total_items:
                    return
                consumed_total[0] += 1
            item = buf.get()
            with consumed_lock:
                consumed.append(item)

    producers = [threading.Thread(target=producer, args=(p,)) for p in range(num_producers)]
    consumers = [threading.Thread(target=consumer) for _ in range(num_consumers)]

    for t in producers:
        t.start()
    for t in consumers:
        t.start()
    for t in producers:
        t.join()
    for t in consumers:
        t.join(timeout=10)

    expected = set()
    for p in range(num_producers):
        for i in range(items_per_producer):
            expected.add((p, i))
    got = set(consumed)

    ok = (len(consumed) == total_items) and (got == expected) and (len(set(consumed)) == len(consumed))
    print("OK" if ok else "FAIL")
    print(len(consumed))


if __name__ == "__main__":
    solve()
