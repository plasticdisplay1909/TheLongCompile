import sys

# =============================================================================
# Q4: The Unrolled Ledger (an unrolled linked list, sqrt-decomposition style)
# =============================================================================
# Implement UnrolledList: a sequence supporting append (at the end), pop
# (from the end), get(i)/set(i, x) (indexed access), and len(), where the
# structure is a DOUBLY LINKED LIST OF BLOCKS: each Block is a small node
# holding up to BLOCK_CAP elements (you may store those elements inside a
# block using a plain Python list -- the block's own array is not the
# point of this exercise), plus prev/next pointers to its neighbouring
# blocks. The blocks themselves are chained purely via prev/next -- there
# is no outer Python list of blocks anywhere in your implementation.
#
# Rules:
#   - append(x): if the tail block is full (len(tail.items) == BLOCK_CAP),
#     first create a brand new block, link it in after the current tail,
#     and make it the new tail -- THEN place x there.
#   - pop(): remove the last element of the tail block. If that empties
#     the tail block AND there is a previous block, drop the now-empty
#     block from the chain and make the previous block the new tail. (If
#     the whole list has only ever had this one block, keep it even when
#     empty -- you always need somewhere for the next append to land.)
#   - get(i) / set(i, x): locate the block containing index i by WALKING
#     the block chain (never index Python lists by "flattening" the whole
#     structure first) -- for a bit of extra speed, walk from whichever
#     end (head or tail) is closer to index i, since the list is doubly
#     linked. Within the located block, indexing straight into its
#     internal Python list is fine (that part is O(1)).
#   - __len__: O(1), maintain a running counter.
#
# A block-chain walk visits O(size / BLOCK_CAP) blocks, which is far
# fewer than the O(size) node-by-node walk a plain singly linked list of
# individual elements would need -- that gap is exactly what the
# performance tests below are designed to expose.
# =============================================================================


class Block:
    __slots__ = ("items", "prev", "next")

    def __init__(self):
        """A block starts with an empty internal list of items and no
        neighbours."""
        # TODO: implement
        raise NotImplementedError


class UnrolledList:
    BLOCK_CAP = 300  # feel free to change this constant; correctness must
                      # not depend on its exact value, only performance does.

    def __init__(self):
        """Start with exactly one (empty) block, which is both head and
        tail, and a size counter of 0."""
        # TODO: implement
        raise NotImplementedError

    def append(self, x):
        """Add x as the new last element. See the policy above."""
        # TODO: implement
        raise NotImplementedError

    def pop(self):
        """Remove and return the current last element. See the policy
        above. You may assume this is only called on a non-empty list."""
        # TODO: implement
        raise NotImplementedError

    def _locate(self, i):
        """
        Return (block, offset) such that block.items[offset] is logical
        index i of the whole sequence. Walk from the head if i is in the
        first half of the sequence, otherwise walk from the tail
        backwards -- do not always walk from the head.
        """
        # TODO: implement
        raise NotImplementedError

    def get(self, i):
        """Return the element currently at position i."""
        # TODO: implement
        raise NotImplementedError

    def set(self, i, x):
        """Overwrite the element at position i with x."""
        # TODO: implement
        raise NotImplementedError

    def __len__(self):
        """O(1): return the maintained size counter."""
        # TODO: implement
        raise NotImplementedError


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    ul = UnrolledList()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "append":
            ul.append(int(parts[1]))
        elif cmd == "pop":
            out.append(str(ul.pop()))
        elif cmd == "access":
            out.append(str(ul.get(int(parts[1]))))
        elif cmd == "set":
            ul.set(int(parts[1]), int(parts[2]))
        elif cmd == "len":
            out.append(str(len(ul)))
        else:
            raise ValueError(cmd)
    print("\n".join(out))


if __name__ == "__main__":
    solve()
