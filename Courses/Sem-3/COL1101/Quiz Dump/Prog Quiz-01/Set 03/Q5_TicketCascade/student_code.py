import sys

# ---------------------------------------------------------------------
# 0. A plain FIFO queue backed by a singly linked list -- given to you.
#    You must use THIS (or an equivalent linked structure you write
#    yourself) for every priority level's queue. You may not use a
#    Python list with pop(0), and you may not use collections.deque --
#    the whole point of this course is that you already know how to
#    build an O(1) FIFO queue from linked nodes, so build it into the
#    scheduler below using this class.
# ---------------------------------------------------------------------
class _QNode:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class SimpleQueue:
    """A minimal FIFO queue: enqueue at the back, dequeue from the
    front, both O(1), backed by a singly linked list with head/tail
    pointers. Fully implemented -- use it as-is."""

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def enqueue(self, value):
        node = _QNode(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value


# ---------------------------------------------------------------------
# 1. Process -- given to you.
# ---------------------------------------------------------------------
class Process:
    """One process being scheduled."""

    def __init__(self, pid, burst):
        self.pid = pid
        self.remaining = burst   # CPU time still needed
        self.level = 0           # current priority level, 0 = highest
        self.finished = False


# ---------------------------------------------------------------------
# 2. Scheduler -- you implement this.
# ---------------------------------------------------------------------
class Scheduler:
    """
    A multilevel feedback queue with `num_levels` priority levels,
    numbered 0 (highest priority) up to num_levels - 1 (lowest). Level i
    has time quantum `base_quantum * 2**i` -- so lower-priority levels
    get progressively longer, but rarer, turns at the CPU.

    New processes always arrive at level 0. Each time the scheduler is
    asked to run one step (see `step` below), it must:
      1. Find the lowest-numbered NON-EMPTY level. If every level is
         empty, there is nothing to run.
      2. Pop the process at the FRONT of that level's queue.
      3. Let it run for min(remaining burst, that level's quantum).
      4. If its remaining burst hits exactly 0, it is finished --
         remove it from the system for good.
      5. Otherwise: if it was NOT already at the last level
         (num_levels - 1), move it to the BACK of the NEXT level's
         queue (level + 1) and update its .level. If it WAS already at
         the last level, it goes back to the BACK OF THAT SAME last
         level (the last level behaves as plain round robin, with no
         further demotion possible).

    Every process id you are ever given is a distinct positive integer.
    You must be able to answer, in O(1), which level (if any) a given
    process id currently sits in, and whether it has finished -- so you
    will need a dict from pid to some per-process bookkeeping alongside
    your num_levels SimpleQueue objects. (Finding *where in its queue*
    that process sits is not something you need to support in O(1) --
    only "which level" and "has it finished".)
    """

    def __init__(self, num_levels, base_quantum):
        # TODO: set up num_levels SimpleQueue objects (one per level),
        # a dict for O(1) process lookup by id, and remember base_quantum.
        raise NotImplementedError

    def arrive(self, pid, burst):
        """A new process with this pid and total burst time arrives and
        joins the back of level 0."""
        # TODO
        raise NotImplementedError

    def step(self):
        """
        Perform exactly one scheduling decision, as described above.
        Return one of:
            ("IDLE", None)             -- every level was empty
            ("DONE", pid)              -- the process that ran to
                                           completion this step
            ("CONTINUE", pid)          -- the process that ran but was
                                           not finished, and has been
                                           requeued as described above
        """
        # TODO
        raise NotImplementedError

    def status(self, pid):
        """Return "UNKNOWN" if pid never arrived, "DONE" if it has
        finished, or the integer level it currently sits in otherwise."""
        # TODO
        raise NotImplementedError

    def count_active(self):
        """Return the number of processes that have arrived but not
        yet finished. Must be O(1) (maintain a running counter)."""
        # TODO
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    first = data[idx].split(); idx += 1
    num_levels, base_quantum, q = int(first[0]), int(first[1]), int(first[2])

    sched = Scheduler(num_levels, base_quantum)
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if parts[0] == "ARRIVE":
            sched.arrive(int(parts[1]), int(parts[2]))
        elif parts[0] == "RUN":
            kind, pid = sched.step()
            if kind == "IDLE":
                out.append("IDLE")
            else:
                out.append(f"{pid} {kind}")
        elif parts[0] == "STATUS":
            result = sched.status(int(parts[1]))
            if result in ("UNKNOWN", "DONE"):
                out.append(result)
            else:
                out.append(f"LEVEL {result}")
        elif parts[0] == "COUNT":
            out.append(str(sched.count_active()))
        else:
            raise ValueError(f"unrecognized op: {parts}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
