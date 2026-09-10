import sys

# =========================================================================
# Q9 : The Sliding Window Maximum  (Applications of Stacks/Queues: a
#       Monotonic Deque built on a Doubly Linked List)
# =========================================================================
#
# You are given an array arr[0..n-1] and, for each query, a window size
# k. A "window" is any block of k consecutive elements
# arr[i], arr[i+1], ..., arr[i+k-1]. There are exactly n-k+1 such
# windows (for i = 0, 1, ..., n-k). For a given k, you must report the
# maximum element within EVERY window, in order, as k slides one
# position to the right at a time across the whole array.
#
# Example: arr = [1, 3, -1, -3, 5, 3, 6, 7], k = 3. The windows are
# [1,3,-1], [3,-1,-3], [-1,-3,5], [-3,5,3], [5,3,6], [3,6,7], with
# maxima 3, 3, 5, 5, 6, 7 respectively.
#
# Method 1 -- Brute force, Theta(n*k):
#   For every window, scan all k of its elements and take the max
#   directly. Simple, and fine for small n and k, but far too slow once
#   both get large (a single query with n = k = 300000 would need on
#   the order of 9*10^10 element comparisons).
#
# Method 2 -- Monotonic deque, Theta(n) per query:
#   Maintain a deque of INDICES (not values) into arr, with the
#   invariant that the corresponding VALUES are always in strictly
#   decreasing order from the front of the deque to the back. Process
#   indices i = 0, 1, ..., n-1 in order:
#     1. Before adding index i, pop indices off the BACK of the deque
#        for as long as the deque is non-empty and arr[the back index]
#        <= arr[i] -- those indices can never again be the maximum of
#        any future window (arr[i] is at least as large as they are,
#        and will outlast them in every window they're both in, since i
#        is further to the right).
#     2. Push index i onto the back of the deque.
#     3. If the index at the FRONT of the deque has fallen out of the
#        current window (i.e. it is <= i - k), pop it off the front --
#        it is too old to belong to the window ending at i.
#     4. Once i >= k - 1 (i.e. a full window ending at i exists), the
#        maximum of that window is arr[the index currently at the
#        front of the deque] -- report it.
#   Because each index is pushed onto the deque exactly once and popped
#   from it at most once (from either end, across the entire run), the
#   TOTAL work across all n steps is Theta(n), regardless of k.
#
# You must implement BOTH methods, and -- this is the point of the
# exercise -- you must implement the deque itself as a DOUBLY LINKED
# LIST of your own (the Deque class below), not with Python's list or
# collections.deque. Every one of push_front / push_back / pop_front /
# pop_back / peek_front / peek_back must run in O(1).
#
# As with the Maximum Gain Window problem earlier in this set, the
# hidden tests are built so that FAST is exercised on inputs large
# enough that an O(n*k) approach (even one dressed up to look
# superficially different) will not finish in time, while BRUTE is only
# ever asked for on inputs small enough that Theta(n*k) is fine -- use
# BRUTE, and the visible test cases, to sanity-check FAST against it
# yourself before you trust it on anything large.


class _DNode:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class Deque:
    """A double-ended queue, implemented as a doubly linked list."""

    def __init__(self):
        """
        TODO: set up an empty deque (however you like -- a pair of
        head/tail sentinels, as in the LRU Cache problem, is one clean
        option, but plain head/tail references that can become None
        together when the deque is empty work fine too).
        """
        raise NotImplementedError

    def push_back(self, value):
        """
        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def push_front(self, value):
        """
        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def pop_back(self):
        """
        Remove and return the value at the back of the deque. You may
        assume this is only called on a non-empty deque.

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def pop_front(self):
        """
        Remove and return the value at the front of the deque. You may
        assume this is only called on a non-empty deque.

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def peek_back(self):
        """
        Return (without removing) the value at the back of the deque.
        You may assume this is only called on a non-empty deque.

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def peek_front(self):
        """
        Return (without removing) the value at the front of the deque.
        You may assume this is only called on a non-empty deque.

        TODO: implement this in O(1).
        """
        raise NotImplementedError

    def is_empty(self):
        """
        TODO: implement this in O(1).
        """
        raise NotImplementedError


def sliding_window_max_bruteforce(arr, k):
    """
    Return a Python list containing, for every window of size k in arr
    (in left-to-right order), the maximum element of that window,
    computed directly (the Theta(n*k) method described above). You may
    assume 1 <= k <= len(arr).

    TODO: implement this.
    """
    raise NotImplementedError


def sliding_window_max_monotonic(arr, k):
    """
    Return the same result as sliding_window_max_bruteforce, but using
    the monotonic-deque method described above, built on YOUR Deque
    class (not a Python list or collections.deque). You may assume
    1 <= k <= len(arr).

    TODO: implement this.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you, do not modify.
#
# Input format:
#   line 1        : n
#   line 2        : n space-separated integers, arr[0..n-1]
#   line 3        : q, the number of queries
#   next q lines  : one of
#                      BRUTE k
#                      FAST k
#
# For each query, print the resulting list of window maxima,
# space-separated, on its own line (this list is never empty, since
# 1 <= k <= n is guaranteed for every query).
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    n = int(data[idx]); idx += 1
    arr = list(map(int, data[idx].split())); idx += 1
    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        k = int(parts[1])
        if cmd == "BRUTE":
            res = sliding_window_max_bruteforce(arr, k)
        elif cmd == "FAST":
            res = sliding_window_max_monotonic(arr, k)
        out.append(" ".join(map(str, res)) if res else "NONE")
    print("\n".join(out))


if __name__ == "__main__":
    solve()
