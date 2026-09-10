import sys

# =========================================================================
# Q5 : Undo, Redo  (Linked Lists / Stacks and their Applications)
# =========================================================================
#
# You are building the undo/redo engine of a bare-bones text editor. The
# editor holds a single string, `document`, which starts out empty.
# Every edit either appends text to the end of the document (TYPE) or
# removes some number of characters from its end (DELETE). At any point
# the user may UNDO the most recent not-yet-undone edit, or REDO the
# most recently undone edit, following the usual rule you already know
# from every text editor you've ever used: making a brand new edit after
# undoing something throws away the ability to redo whatever you had
# undone (the "future" you rewound out of is gone the moment you type
# something new).
#
# Concretely:
#   TYPE <text>    Append <text> to the end of the document. Remember
#                  the document's PREVIOUS contents on an undo history,
#                  and throw away any redo history (see above).
#   DELETE k       Remove the last k characters from the document (if k
#                  is at least as large as the document's current
#                  length, the document becomes empty). Exactly like
#                  TYPE, this remembers the previous contents on the
#                  undo history and throws away the redo history.
#   UNDO           Revert the document to whatever it was immediately
#                  before the most recent not-yet-undone TYPE or DELETE.
#                  The state you are leaving (i.e. the document just
#                  before this UNDO) must become redoable. If there is
#                  nothing left to undo, this command has no effect.
#   REDO           Re-apply the most recently undone edit, i.e. restore
#                  the document to what it was immediately before the
#                  matching UNDO. The state you are leaving must become
#                  undoable again. If there is nothing to redo, this
#                  command has no effect.
#   PRINT          Print the document's current contents, or the literal
#                  text <EMPTY> if the document is currently the empty
#                  string.
#
# You must implement this with TWO STACKS -- an undo stack and a redo
# stack, each holding past versions of the whole document string -- and,
# critically, you must implement the Stack itself as a genuine SINGLY
# LINKED LIST (using the Node-based LinkedStack class below), not with a
# Python list. Do not use Python's built-in list, collections.deque, or
# any other pre-built container to hold the stacked document versions:
# the entire point of this problem is practising building and using your
# own linked-list-backed Stack ADT and seeing how two stacks together
# give you undo/redo "for free" once the ADT itself is right.


class _Node:
    """A single singly-linked-list node. Do not modify."""
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedStack:
    """A Stack ADT implemented as a singly linked list of _Node objects."""

    def __init__(self):
        """
        TODO: set up an empty stack (you will need at least a reference
        to the top node, and it is convenient, though not required, to
        also track the current size).
        """
        raise NotImplementedError

    def push(self, value):
        """
        Push value onto the top of the stack, in O(1) time.

        TODO: implement this.
        """
        raise NotImplementedError

    def pop(self):
        """
        Remove and return the value at the top of the stack, in O(1)
        time. You may assume this is only called on a non-empty stack.

        TODO: implement this.
        """
        raise NotImplementedError

    def peek(self):
        """
        Return (without removing) the value at the top of the stack, in
        O(1) time. You may assume this is only called on a non-empty
        stack.

        TODO: implement this.
        """
        raise NotImplementedError

    def is_empty(self):
        """
        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def clear(self):
        """
        Discard every element currently on the stack, leaving it empty,
        in O(1) time (do NOT pop elements off one at a time in a loop --
        simply detach the whole chain of nodes from the stack's own
        state so it can be garbage collected).

        TODO: implement this.
        """
        raise NotImplementedError

    def __len__(self):
        """
        TODO: implement this in O(1).
        """
        raise NotImplementedError


class UndoRedoEditor:
    """The editor itself, built on top of two LinkedStacks."""

    def __init__(self):
        """
        TODO: set up an empty document ("") and two empty LinkedStacks,
        one for undo history and one for redo history.
        """
        raise NotImplementedError

    def type_text(self, text):
        """
        Implement the TYPE command described above.

        TODO: implement this.
        """
        raise NotImplementedError

    def delete_last(self, k):
        """
        Implement the DELETE command described above.

        TODO: implement this.
        """
        raise NotImplementedError

    def undo(self):
        """
        Implement the UNDO command described above (a no-op if there is
        nothing to undo).

        TODO: implement this.
        """
        raise NotImplementedError

    def redo(self):
        """
        Implement the REDO command described above (a no-op if there is
        nothing to redo).

        TODO: implement this.
        """
        raise NotImplementedError

    def current(self):
        """
        Return the string that PRINT should output: the document itself,
        or "<EMPTY>" if the document is currently empty.

        TODO: implement this.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you, do not modify.
#
# Input format:
#   line 1        : q
#   next q lines  : one of
#                      TYPE <text>      (text may itself contain spaces;
#                                        it is everything after the
#                                        first space on the line)
#                      DELETE k
#                      UNDO
#                      REDO
#                      PRINT
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    ed = UndoRedoEditor()
    out = []
    for _ in range(q):
        line = data[idx]; idx += 1
        if line.startswith("TYPE "):
            ed.type_text(line[len("TYPE "):])
        elif line.startswith("DELETE "):
            ed.delete_last(int(line.split()[1]))
        elif line == "UNDO":
            ed.undo()
        elif line == "REDO":
            ed.redo()
        elif line == "PRINT":
            out.append(ed.current())
    print("\n".join(out))


if __name__ == "__main__":
    solve()
