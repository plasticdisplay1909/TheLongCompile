import sys
import random

# ---------------------------------------------------------------------
# A "Skyline" is the city's registry of building heights: heights are
# added and removed constantly as buildings go up and come down, and
# duplicates are common (many buildings share a height). The registry
# must answer, at any moment: how many buildings are exactly height x?
# what is the k-th shortest building overall? how many buildings are
# strictly shorter than height x? All of this, with insertions and
# removals happening just as often as queries, and with performance
# that must not degrade even if heights are added in already-sorted
# order (which would make a plain unbalanced BST degenerate into a
# straight line).
#
# You will solve this with a TREAP: a binary search tree on the keys
# (heights), where every node is ALSO given an independent random
# priority, and the tree is kept a max-heap on priority via rotations.
# Because the priorities are random, the tree's shape is (with very
# high probability) balanced regardless of insertion order, giving
# O(log n) EXPECTED time per operation without you ever having to
# write explicit rebalancing logic for particular bad cases the way
# an AVL or red-black tree would need. This is the standard reason
# treaps are taught as "the balanced BST you can actually implement in
# an exam": the balancing is a side-effect of randomness, not of
# casework.
# ---------------------------------------------------------------------


class TreapNode:
    __slots__ = ("key", "priority", "count", "size", "left", "right")

    def __init__(self, key):
        self.key = key
        self.priority = random.random()   # given: do not change this line
        self.count = 1        # how many copies of `key` live at this node
        self.size = 1         # total elements (with multiplicity) in this subtree
        self.left = None
        self.right = None


# ---------------------------------------------------------------------
# Given to you, fully implemented. Use these everywhere instead of
# hand-rolling subtree-size bookkeeping yourself.
# ---------------------------------------------------------------------
def _node_size(node):
    return node.size if node is not None else 0


def _update(node):
    """Recompute node.size from its two children and its own count.
    Call this on a node every time either of its children (or its own
    count) may have changed."""
    node.size = _node_size(node.left) + _node_size(node.right) + node.count


def _rotate_right(node):
    """
       node                 left
      /    \                /   \
    left    R      -->     LL   node
   /   \                          /  \
  LL    LR                      LR    R
    Returns the new subtree root. Updates .size on both nodes touched.
    """
    left = node.left
    node.left = left.right
    left.right = node
    _update(node)
    _update(left)
    return left


def _rotate_left(node):
    """Mirror image of _rotate_right. Returns the new subtree root."""
    right = node.right
    node.right = right.left
    right.left = node
    _update(node)
    _update(right)
    return right


# ---------------------------------------------------------------------
# You implement everything below. All functions are FREE FUNCTIONS
# taking the subtree root as their first argument (not methods), and
# every one of them returns the (possibly new) root of the subtree it
# was given, except count/kth/rank which return the queried value.
# Write them recursively.
# ---------------------------------------------------------------------
def insert(node, key):
    """
    Insert one occurrence of key into the subtree rooted at node
    (node may be None for an empty subtree) and return the new
    subtree root.

    - If key is already present anywhere in this subtree as its OWN
      node (i.e. some existing TreapNode already has .key == key),
      you must not create a second node for the same key -- instead
      increment that node's .count by one (a "multiplicity" count),
      then fix up .size on every ancestor you touched on the way back
      up (via _update).
    - If key is new, insert a fresh TreapNode(key) as a leaf via
      ordinary BST insertion (by key), then rotate it upward with
      _rotate_left/_rotate_right for as long as its priority is
      greater than its parent's priority -- this is what keeps the
      tree heap-ordered on priority (and therefore balanced with high
      probability).
    - Every node whose subtree changed must have _update called on it
      before you return.
    """
    # TODO
    raise NotImplementedError


def delete(node, key):
    """
    Remove ONE occurrence of key from the subtree rooted at node and
    return the new subtree root. If key is not present at all, return
    node unchanged.

    - If the node holding key has .count > 1, just decrement .count
      (the node stays; no structural change other than _update).
    - If the node holding key has .count == 1, the node itself must be
      removed from the tree structure. The standard treap technique:
      repeatedly rotate the node DOWNWARD (toward whichever child has
      the larger priority, using _rotate_left/_rotate_right) until it
      becomes a leaf (or has only one child), at which point it can be
      unlinked directly.
    - Every node whose subtree changed must have _update called on it
      before you return.
    """
    # TODO
    raise NotImplementedError


def count(node, key):
    """Return how many occurrences of key are currently in the subtree
    rooted at node (0 if key is absent). O(log n) expected."""
    # TODO
    raise NotImplementedError


def kth(node, k):
    """
    Return the k-th smallest element (1-indexed, counting duplicates
    individually -- e.g. if the multiset is {2, 2, 5}, kth(1) = 2,
    kth(2) = 2, kth(3) = 5) currently in the subtree rooted at node.
    You may assume 1 <= k <= _node_size(node). O(log n) expected.
    """
    # TODO
    raise NotImplementedError


def rank(node, key):
    """
    Return the number of elements in the subtree rooted at node that
    are STRICTLY LESS than key (regardless of whether key itself is
    present). O(log n) expected.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you. `root` is threaded through exactly like
# `state` was in the RepLang / PQ problems: your functions return the
# new root, and the driver keeps track of it across operations.
# ---------------------------------------------------------------------
def solve():
    random.seed(12345)   # fixed seed: makes local runs reproducible
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1

    root = None
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if parts[0] == "INSERT":
            root = insert(root, int(parts[1]))
        elif parts[0] == "DELETE":
            root = delete(root, int(parts[1]))
        elif parts[0] == "COUNT":
            out.append(str(count(root, int(parts[1]))))
        elif parts[0] == "KTH":
            out.append(str(kth(root, int(parts[1]))))
        elif parts[0] == "RANK":
            out.append(str(rank(root, int(parts[1]))))
        elif parts[0] == "SIZE":
            out.append(str(_node_size(root)))
        else:
            raise ValueError(f"unrecognized op: {parts}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
