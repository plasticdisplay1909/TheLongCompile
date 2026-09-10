import sys

# =============================================================================
# Q5: The Emergency Router (queue + stack + hash map ADT combination)
# =============================================================================
# A hospital triage router with NUM_LEVELS = 5 priority levels (1 = most
# urgent, 5 = least). Every patient sits in exactly one level's FIFO queue
# at a time. All FIVE of these operations must be O(1) (COUNT truly O(1)
# via a maintained size; the others via the doubly linked structure and a
# hash map from patient id to their node -- NOT by scanning a level):
#
#   REGISTER pid level  -- add a new patient at the back of that level's
#                           queue. (You may assume pids are never reused
#                           while a patient is still active in the system.)
#   NEXT               -- report (without removing) the id of the patient
#                           at the front of the lowest-numbered non-empty
#                           level, or -1 if nobody is waiting.
#   SERVE              -- like NEXT, but also removes that patient and
#                           pushes (pid, their level) onto a discharge
#                           STACK, for RECALL to undo later. Report the id
#                           served, or -1 if nobody is waiting.
#   COUNT              -- report how many patients are currently waiting,
#                           across every level.
#   REQUEUE pid level  -- move an ALREADY-WAITING patient to a different
#                           level's queue (at the BACK of the new level),
#                           removing them from wherever they currently sit
#                           WITHOUT walking that level's queue to find
#                           them -- use the hash map to jump straight to
#                           their node, then unlink it in O(1) using its
#                           own prev/next pointers. No-op if pid is not
#                           currently waiting.
#   RECALL             -- pop the most recently discharged patient off the
#                           discharge stack and put them back, at the
#                           FRONT (not the back!) of the queue for their
#                           ORIGINAL level (the level they were serving
#                           from at the moment they were SERVEd -- NOT any
#                           level they may have been REQUEUEd to and from
#                           earlier, since REQUEUE only affects patients
#                           who are still waiting). Report the id
#                           recalled, or -1 if the discharge stack is
#                           empty.
#
# You will need: a doubly linked list class for each level's FIFO queue
# (with O(1) push front, push back, and "remove this specific node"), and
# a plain dict mapping pid -> the node object currently holding them (only
# while they are waiting -- remove the dict entry the moment they are
# SERVEd, and re-add it when RECALLed).
# =============================================================================

NUM_LEVELS = 5


class PNode:
    __slots__ = ("pid", "level", "prev", "next")

    def __init__(self, pid, level):
        """A patient node: holds their id, their current level, and
        prev/next pointers within that level's queue (None, None to
        start)."""
        # TODO: implement
        raise NotImplementedError


class LevelQueue:
    """A doubly linked FIFO queue of PNodes for one triage level."""

    def __init__(self):
        """Empty queue: head, tail = None, None; a running count = 0."""
        # TODO: implement
        raise NotImplementedError

    def push_back(self, node):
        """Link node in as the new tail. O(1)."""
        # TODO: implement
        raise NotImplementedError

    def push_front(self, node):
        """Link node in as the new head. O(1)."""
        # TODO: implement
        raise NotImplementedError

    def remove(self, node):
        """
        Unlink node from WHEREVER it currently sits in this queue (head,
        tail, or the middle), using only node.prev / node.next -- do NOT
        search for it. O(1).
        """
        # TODO: implement
        raise NotImplementedError

    def pop_front(self):
        """Remove and return the head node (assume non-empty). O(1)."""
        # TODO: implement
        raise NotImplementedError

    def is_empty(self):
        # TODO: implement
        raise NotImplementedError


class Router:
    def __init__(self):
        """Set up NUM_LEVELS empty LevelQueues, an empty pid -> PNode map,
        and an empty discharge stack (a plain Python list used purely as
        a stack -- push/pop from its end only)."""
        # TODO: implement
        raise NotImplementedError

    def register(self, pid, level):
        # TODO: implement
        raise NotImplementedError

    def peek(self):
        # TODO: implement
        raise NotImplementedError

    def serve(self):
        # TODO: implement
        raise NotImplementedError

    def count(self):
        # TODO: implement
        raise NotImplementedError

    def requeue(self, pid, new_level):
        # TODO: implement
        raise NotImplementedError

    def recall(self):
        # TODO: implement
        raise NotImplementedError


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    r = Router()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "REGISTER":
            r.register(parts[1], int(parts[2]))
        elif cmd == "NEXT":
            out.append(str(r.peek()))
        elif cmd == "SERVE":
            out.append(str(r.serve()))
        elif cmd == "COUNT":
            out.append(str(r.count()))
        elif cmd == "REQUEUE":
            r.requeue(parts[1], int(parts[2]))
        elif cmd == "RECALL":
            out.append(str(r.recall()))
        else:
            raise ValueError(cmd)
    print("\n".join(out))


if __name__ == "__main__":
    solve()
