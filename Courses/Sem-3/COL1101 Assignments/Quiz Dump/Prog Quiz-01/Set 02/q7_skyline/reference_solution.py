import sys


class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


class Skyline:
    def __init__(self):
        self.heights = []      # heights[i]
        self.span = []         # span[i] computed at the time it was appended
        self.span_stack_idx = []  # a monotonic stack of indices, decreasing height

    def append(self, h):
        i = len(self.heights)
        self.heights.append(h)
        cnt = 1
        while self.span_stack_idx and self.heights[self.span_stack_idx[-1]] <= h:
            j = self.span_stack_idx.pop()
            cnt += self.span[j]
        self.span.append(cnt)
        self.span_stack_idx.append(i)

    def remove_last(self):
        # undo append(): pop heights/span, and restore span_stack_idx to
        # exactly what it was before that append. Because span_stack_idx
        # only ever had entries popped off (never destroyed, we can't
        # trivially "unpop" them without recomputation) -- for REMOVE_LAST
        # we simply recompute span_stack_idx and span from scratch over
        # the remaining heights (still fine: REMOVE_LAST is defined to be
        # allowed to cost O(current n)).
        self.heights.pop()
        self.span.pop()
        self._rebuild_span_stack()

    def _rebuild_span_stack(self):
        self.span_stack_idx = []
        self.span = []
        for i, h in enumerate(self.heights):
            cnt = 1
            while self.span_stack_idx and self.heights[self.span_stack_idx[-1]] <= h:
                j = self.span_stack_idx.pop()
                cnt += self.span[j]
            self.span.append(cnt)
            self.span_stack_idx.append(i)

    def span_at(self, i):
        return self.span[i]

    def next_greater(self, i):
        # from scratch each query, O(current n), using a Stack
        n = len(self.heights)
        st = Stack()
        result = [-1] * n
        for k in range(n - 1, -1, -1):
            while not st.is_empty() and self.heights[st.peek()] <= self.heights[k]:
                st.pop()
            result[k] = st.peek() if not st.is_empty() else -1
            st.push(k)
        return result[i]

    def max_rect(self):
        # classic monotonic-stack largest rectangle in histogram, using
        # our own Stack class, from scratch each query
        st = Stack()
        best = 0
        n = len(self.heights)
        i = 0
        while i <= n:
            h = self.heights[i] if i < n else 0
            if st.is_empty() or self.heights[st.peek()] <= h:
                st.push(i)
                i += 1
            else:
                top = st.pop()
                width = i if st.is_empty() else i - st.peek() - 1
                best = max(best, self.heights[top] * width)
        return best


def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    sky = Skyline()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "APPEND":
            sky.append(int(parts[1]))
        elif cmd == "REMOVE_LAST":
            sky.remove_last()
        elif cmd == "MAXRECT":
            out.append(str(sky.max_rect()))
        elif cmd == "NEXTGREATER":
            out.append(str(sky.next_greater(int(parts[1]))))
        elif cmd == "SPAN":
            out.append(str(sky.span_at(int(parts[1]))))
        else:
            raise ValueError(cmd)
    print("\n".join(out))


if __name__ == "__main__":
    solve()
