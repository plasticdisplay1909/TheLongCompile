import sys
from typing import Any, NamedTuple

# ---------------------------------------------------------------------
# Given to you. Do not rename these.
# ---------------------------------------------------------------------
EMPTY = None  # the empty stack's top cell


class Cell(NamedTuple):     # one immutable cons cell
    value: Any
    rest: Any                # the Cell beneath this one, or EMPTY


class Stack(NamedTuple):
    """One IMMUTABLE version of the whiteboard's stack.
    top  : EMPTY, or a Cell whose .value is the current top element
    size : the number of elements in THIS version (cached, not recomputed)
    """
    top: Any
    size: int


EMPTY_STACK = Stack(EMPTY, 0)


def push(s, x):
    """
    Return a brand NEW Stack with x pushed on top of s. s itself (and
    every Cell reachable from it) must be completely untouched -- other
    code may be holding onto s and expects it to keep meaning exactly
    what it meant before this call, forever.

    Must be O(1) worst-case, and must NOT copy any existing Cell: the
    new Cell you create simply points its .rest at s.top (structural
    sharing -- the old chain of cells is reused as-is, not rebuilt).
    """
    # TODO
    raise NotImplementedError


def pop(s):
    """
    Return the pair (x, new_s): x is the value that was on top of s,
    and new_s is a new Stack with that element removed. s itself is
    left completely unchanged. You may assume s.size > 0.

    Must be O(1) worst-case, and must not touch any Cell -- new_s.top
    is simply s.top.rest, which already exists.
    """
    # TODO
    raise NotImplementedError


def top(s):
    """Return the current top value of s. You may assume s.size > 0."""
    # TODO
    raise NotImplementedError


def size(s):
    """Return s.size directly (do not walk the chain of cells)."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------
# Version bookkeeping.
#
# Version 0 always denotes EMPTY_STACK and is never created by an
# operation. Every PUSH or POP operation you process creates exactly
# one brand new version, numbered 1, 2, 3, ... in the order those
# operations were processed (the very first PUSH or POP you ever
# process creates version 1, the second creates version 2, and so on --
# TOP and SIZE never create a new version). You must be able to look up
# "the Stack for version v" in O(1) for any v you are asked about,
# including branching back to reuse an old version many times.
# ---------------------------------------------------------------------
class VersionStore:
    def __init__(self):
        # TODO: set up whatever bookkeeping you need. Version 0 must
        # already map to EMPTY_STACK before any operation is processed.
        raise NotImplementedError

    def get(self, v):
        """Return the Stack object for version v. O(1)."""
        # TODO
        raise NotImplementedError

    def new_version(self, s):
        """Register a brand new Stack s as the NEXT version (following
        the numbering rule above) and return its newly assigned integer
        id. O(1)."""
        # TODO
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1

    store = VersionStore()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if parts[0] == "PUSH":
            v, x = int(parts[1]), int(parts[2])
            new_s = push(store.get(v), x)
            out.append(str(store.new_version(new_s)))
        elif parts[0] == "POP":
            v = int(parts[1])
            x, new_s = pop(store.get(v))
            out.append(f"{x} {store.new_version(new_s)}")
        elif parts[0] == "TOP":
            v = int(parts[1])
            out.append(str(top(store.get(v))))
        elif parts[0] == "SIZE":
            v = int(parts[1])
            out.append(str(size(store.get(v))))
        else:
            raise ValueError(f"unrecognized op: {parts}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
