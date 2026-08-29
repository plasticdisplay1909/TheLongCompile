import sys

# =========================================================================
# Q7 : The Max Queue  (Queue ADT built from two Stacks)
# =========================================================================
#
# A queue and a stack look like opposites -- one is FIFO, the other
# LIFO -- but you can build a perfectly good queue using nothing but two
# stacks, and it is a classic and instructive exercise in exactly the
# kind of amortized-cost reasoning this course cares about. On top of
# that queue, you will also support an O(1)-amortized MAX query
# ("what is the largest element currently in the queue?"), using a
# second classic trick: a stack that tracks its own running maximum.
#
# Part A -- MaxStack:
#   A MaxStack behaves exactly like an ordinary stack (push, pop, peek,
#   is_empty, __len__), but ALSO supports peek_max(): return the largest
#   element currently anywhere in the stack, in O(1) time. The standard
#   trick is to keep a second, parallel stack of "running maximums": push
#   onto it, alongside every element you push onto the main stack, the
#   larger of (that new element) and (whatever the running-max stack's
#   current top already is) -- so the running-max stack's top is always
#   the maximum of everything below it in the main stack, and popping
#   the main stack's top and the running-max stack's top together keeps
#   this invariant intact.
#
# Part B -- MaxQueue, built from two MaxStacks:
#   Keep an "in_stack" (freshly enqueued elements, most recent on top)
#   and an "out_stack" (elements ready to be dequeued, oldest on top).
#   ENQUEUE always just pushes onto in_stack -- O(1), always. DEQUEUE and
#   FRONT need the OLDEST element, which is buried at the BOTTOM of
#   in_stack -- so, whenever out_stack is empty, pop every element off
#   in_stack and push it onto out_stack, which reverses their order and
#   puts the oldest element from in_stack on top of out_stack where it
#   belongs. Do this "shift" ONLY when out_stack is empty (never migrate
#   elements back from out_stack to in_stack, and never shift when
#   out_stack still has something on it) -- that is precisely what makes
#   this scheme amortized O(1) per operation overall, even though any
#   single DEQUEUE call might occasionally have to move a large number of
#   elements across.
#   Finally, GET_MAX must return the maximum of everything in the queue,
#   which is now split across two MaxStacks: it is simply the larger of
#   in_stack.peek_max() and out_stack.peek_max() (skipping whichever
#   stack, if either, happens to be empty right now).
#
# Getting the amortized analysis wrong is easy to do without noticing
# it in small tests -- e.g. re-shifting on every single DEQUEUE call
# regardless of whether out_stack is already non-empty still gives
# correct OUTPUT, but is quietly Theta(n) per call instead of amortized
# O(1), and several of the hidden test cases below run on the order of
# a hundred thousand interleaved operations specifically to catch that.


class MaxStack:
    def __init__(self):
        """
        TODO: set up an empty stack together with whatever auxiliary
        state you need to answer peek_max() in O(1).
        """
        raise NotImplementedError

    def push(self, x):
        """
        TODO: implement this, maintaining whatever invariant peek_max()
        depends on.
        """
        raise NotImplementedError

    def pop(self):
        """
        Remove and return the top element. You may assume this is only
        called on a non-empty stack.

        TODO: implement this.
        """
        raise NotImplementedError

    def peek(self):
        """
        Return (without removing) the top element. You may assume this
        is only called on a non-empty stack.

        TODO: implement this.
        """
        raise NotImplementedError

    def peek_max(self):
        """
        Return the maximum element currently anywhere in the stack, in
        O(1) time. You may assume this is only called on a non-empty
        stack.

        TODO: implement this.
        """
        raise NotImplementedError

    def is_empty(self):
        """
        TODO: implement this.
        """
        raise NotImplementedError

    def __len__(self):
        """
        TODO: implement this.
        """
        raise NotImplementedError


class MaxQueue:
    def __init__(self):
        """
        TODO: set up an empty in_stack and an empty out_stack (both
        MaxStacks).
        """
        raise NotImplementedError

    def enqueue(self, x):
        """
        TODO: implement this (should be O(1), always -- no shifting
        here).
        """
        raise NotImplementedError

    def _shift(self):
        """
        If out_stack is currently empty, move every element from
        in_stack onto out_stack (which reverses their order). If
        out_stack is already non-empty, do nothing at all -- this
        precise condition is what gives the amortized O(1) bound, so
        do not "top up" out_stack when it still has elements left.

        TODO: implement this. (dequeue() and front() below should call
        this helper first, then operate on out_stack.)
        """
        raise NotImplementedError

    def dequeue(self):
        """
        Remove and return the element at the front of the queue (the
        oldest element still enqueued). You may assume this is only
        called on a non-empty queue.

        TODO: implement this.
        """
        raise NotImplementedError

    def front(self):
        """
        Return (without removing) the element at the front of the
        queue. You may assume this is only called on a non-empty queue.

        TODO: implement this.
        """
        raise NotImplementedError

    def get_max(self):
        """
        Return the maximum element currently anywhere in the queue. You
        may assume this is only called on a non-empty queue.

        TODO: implement this using peek_max() on whichever of in_stack /
        out_stack are currently non-empty.
        """
        raise NotImplementedError

    def is_empty(self):
        """
        TODO: implement this.
        """
        raise NotImplementedError

    def __len__(self):
        """
        TODO: implement this.
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
#                      MAX
#                      SIZE
#
# DEQUEUE, FRONT, and MAX on an empty queue must print "EMPTY".
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    queue = MaxQueue()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "ENQUEUE":
            queue.enqueue(int(parts[1]))
        elif cmd == "DEQUEUE":
            out.append("EMPTY" if queue.is_empty() else str(queue.dequeue()))
        elif cmd == "FRONT":
            out.append("EMPTY" if queue.is_empty() else str(queue.front()))
        elif cmd == "SIZE":
            out.append(str(len(queue)))
        elif cmd == "MAX":
            out.append("EMPTY" if queue.is_empty() else str(queue.get_max()))
    print("\n".join(out))


if __name__ == "__main__":
    solve()
