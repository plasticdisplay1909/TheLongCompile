import sys

NEG_INF = float("-inf")

# =========================================================================
# Q3 : Maximum Gain Window  (Divide and Conquer / Asymptotic Analysis)
# =========================================================================
#
# A trader has a list of n daily profit/loss values arr[0..n-1] (each may
# be positive, negative, or zero). She wants to know the largest total
# gain achievable by holding a position over some CONTIGUOUS run of days
# arr[l], arr[l+1], ..., arr[r] (l <= r; a single day, i.e. l == r, is
# always an allowed "window"). This is the classic Maximum Subarray Sum
# problem, and you will implement it TWO different ways so that you can
# see, on your own machine, exactly why one of them scales and the other
# does not.
#
# Method 1 -- Brute force, Theta(n^2):
#   Try every pair of indices (i, j) with i <= j, and for each compute
#   the sum arr[i] + ... + arr[j] directly, keeping the best sum seen.
#   This is exactly the sort of algorithm you'd write in your first week
#   of programming: correct, easy to convince yourself of, and useless
#   once n gets into the tens of thousands.
#
# Method 2 -- Divide and conquer, Theta(n log n):
#   Split the range [low, high] at mid = (low + high) // 2. The best
#   window lies ENTIRELY in the left half [low, mid], ENTIRELY in the
#   right half [mid+1, high], or straddles the midpoint (i.e. it
#   contains both arr[mid] and arr[mid+1]). Recursively solve the first
#   two cases; for the third, you cannot recurse -- you must scan
#   outward from the midpoint in both directions to find the best
#   "crossing" window, which takes only Theta(high - low + 1) time (not
#   Theta((high-low+1)^2)) because you can track a running sum instead
#   of recomputing it from scratch for every candidate endpoint. Solving
#   the crossing case in linear time is precisely what makes the overall
#   recurrence T(n) = 2T(n/2) + Theta(n) work out to Theta(n log n)
#   rather than something worse.
#
# You must implement BOTH methods below, keeping every function name and
# signature exactly as given (the I/O driver at the bottom calls them by
# name). The hidden test cases are specifically designed so that a
# correct-but-quadratic implementation of the DC method (e.g. one that
# secretly falls back on brute force, or that recomputes the crossing
# sum from scratch for every candidate split point) will time out on the
# larger inputs, while a genuine Theta(n log n) implementation comfortably
# will not. The BRUTE method, by contrast, is only ever exercised on
# small inputs in this problem -- it is meant to run slowly, and is
# there to give you and the grader an independent way to sanity-check
# the divide-and-conquer answer on cases small enough to double-check.


def max_crossing_sum(arr, low, mid, high):
    """
    Return the maximum sum of a window arr[i..j] with low <= i <= mid
    and mid < j <= high, i.e. a window that includes BOTH arr[mid] and
    arr[mid + 1] and stays within [low, high]. You may assume
    low <= mid < high.

    Do this in Theta(high - low + 1) time: scan left from mid down to
    low maintaining a running sum and the best left-sum seen, then scan
    right from mid+1 up to high the same way, and add the two best
    halves together. Do NOT recompute a fresh sum from scratch for every
    candidate i or j -- that would make this function Theta(n^2) on its
    own and defeat the entire point of the divide-and-conquer approach.

    TODO: implement this.
    """
    raise NotImplementedError


def max_subarray_dc(arr, low, high):
    """
    Return the maximum window sum of arr[low..high] (inclusive), using
    the divide-and-conquer method described above. You may assume
    low <= high.

    Base case: if low == high, the only possible window is the single
    element arr[low].
    Recursive case: split at mid = (low + high) // 2, recursively solve
    the left half [low, mid] and the right half [mid+1, high], solve the
    crossing case with max_crossing_sum, and return the best of the
    three.

    TODO: implement this.
    """
    raise NotImplementedError


def max_subarray_brute(arr, low, high):
    """
    Return the maximum window sum of arr[low..high] (inclusive) by
    directly trying every pair of start/end indices i <= j within that
    range and computing each window's sum with a running total (i.e.
    the standard Theta((high-low+1)^2) double loop). This function is
    intentionally the "naive" method -- do not call max_subarray_dc from
    inside it, and do not try to make it fast; that is not the point of
    this function.

    TODO: implement this.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you, do not modify.
#
# Input format:
#   line 1       : n
#   line 2       : n space-separated integers, arr[0..n-1]
#   line 3       : q, the number of queries
#   next q lines : one of
#                     BRUTE          -> report max_subarray_brute over the WHOLE array
#                     DC             -> report max_subarray_dc over the WHOLE array
#                     RANGE l r      -> report max_subarray_dc over arr[l..r] (0-indexed, inclusive)
#
# For each query, print the single resulting integer on its own line.
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
        if cmd == "BRUTE":
            out.append(str(max_subarray_brute(arr, 0, n - 1)))
        elif cmd == "DC":
            out.append(str(max_subarray_dc(arr, 0, n - 1)))
        elif cmd == "RANGE":
            l, r = int(parts[1]), int(parts[2])
            out.append(str(max_subarray_dc(arr, l, r)))
    print("\n".join(out))


if __name__ == "__main__":
    solve()
