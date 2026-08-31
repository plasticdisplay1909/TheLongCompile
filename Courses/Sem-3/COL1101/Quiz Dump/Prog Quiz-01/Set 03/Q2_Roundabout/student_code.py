import sys

# ---------------------------------------------------------------------
# Node class -- given to you.
# ---------------------------------------------------------------------
class Node:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class CircularDeque:
    """
    A deque backed by a CIRCULAR doubly linked list with a single
    sentinel node. There is exactly one Node object, self._sentinel,
    that never stores a real element: self._sentinel.next is the
    front of the deque, self._sentinel.prev is the back of the deque,
    and if the deque is empty, self._sentinel.next is self._sentinel.prev
    is self._sentinel itself. This is the standard trick that removes
    every 'is this end of the list?' special case from push/pop, because
    the sentinel is always there to link against.

    You must maintain:
        self._sentinel : the sentinel Node (created once, never replaced)
        self._size      : the number of real elements currently stored

    You may not use Python's collections.deque anywhere in this file.
    """

    def __init__(self):
        # TODO: create the sentinel node and point it to itself in both
        # directions; initialise size to 0.
        raise NotImplementedError

    def __len__(self):
        """Return the number of elements. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def push_front(self, x):
        """Insert x as the new front element. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def push_back(self, x):
        """Insert x as the new back element. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def pop_front(self):
        """Remove and return the current front element.
        You may assume len(self) > 0. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def pop_back(self):
        """Remove and return the current back element.
        You may assume len(self) > 0. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def front(self):
        """Return (without removing) the current front element.
        You may assume len(self) > 0. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def back(self):
        """Return (without removing) the current back element.
        You may assume len(self) > 0. Must be O(1)."""
        # TODO
        raise NotImplementedError

    def rotate(self, k):
        """
        Rotate the deque by k steps, where k may be any integer
        (positive, negative, zero, or with |k| far larger than the
        current size).

        A rotation by +1 means: the current front element moves to
        become the new back, i.e. it behaves exactly like calling
        push_back(pop_front()) once. A rotation by -1 is the mirror
        image: push_front(pop_back()) once. Rotating by k is defined
        as doing that primitive step k times in the corresponding
        direction (k > 0 means +1 direction, k < 0 means -1 direction).

        Doing this literally, one element at a time, is only O(k) -- and
        the whole point of this question is that k can be given to you
        as something like 10**15 while the deque itself might hold only
        50 elements. You must implement rotate(k) so that its running
        time depends only on the CURRENT SIZE of the deque (specifically
        O(min(k mod n, n - (k mod n))) where n = len(self)), never on the
        raw magnitude of k, and never by moving elements one at a time
        n times over. Think about what a rotation by n steps does to the
        deque, and what that tells you about how large an *effective*
        rotation you ever really need to perform, and then think about
        walking in from BOTH the front and the back to find the new
        boundary in the cheaper direction, re-linking a constant number
        of pointers to 'cut' the circular list at the new front/back
        rather than moving any element's value.

        You may assume rotate is never called on an empty deque.
        """
        # TODO
        raise NotImplementedError

    def to_list(self):
        """Return a Python list of the elements from front to back.
        This helper may be O(n) -- it is only used for debugging /
        printing and is not one of the graded O(1) operations."""
        out = []
        node = self._sentinel.next
        while node is not self._sentinel:
            out.append(node.value)
            node = node.next
        return out


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1

    dq = CircularDeque()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if parts[0] == "PUSHF":
            dq.push_front(int(parts[1]))
        elif parts[0] == "PUSHB":
            dq.push_back(int(parts[1]))
        elif parts[0] == "POPF":
            out.append(str(dq.pop_front()))
        elif parts[0] == "POPB":
            out.append(str(dq.pop_back()))
        elif parts[0] == "FRONT":
            out.append(str(dq.front()))
        elif parts[0] == "BACK":
            out.append(str(dq.back()))
        elif parts[0] == "SIZE":
            out.append(str(len(dq)))
        elif parts[0] == "ROTATE":
            dq.rotate(int(parts[1]))
        else:
            raise ValueError(f"unrecognized op: {parts}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
