import sys


class Block:
    __slots__ = ("items", "prev", "next")

    def __init__(self):
        self.items = []
        self.prev = None
        self.next = None


class UnrolledList:
    BLOCK_CAP = 300

    def __init__(self):
        b = Block()
        self.head = b
        self.tail = b
        self._size = 0

    def append(self, x):
        if len(self.tail.items) >= self.BLOCK_CAP:
            nb = Block()
            nb.prev = self.tail
            self.tail.next = nb
            self.tail = nb
        self.tail.items.append(x)
        self._size += 1

    def pop(self):
        x = self.tail.items.pop()
        self._size -= 1
        if not self.tail.items and self.tail.prev is not None:
            self.tail = self.tail.prev
            self.tail.next = None
        return x

    def _locate(self, i):
        # walk from whichever end is closer
        if i <= self._size - i:
            block = self.head
            base = 0
            while base + len(block.items) <= i:
                base += len(block.items)
                block = block.next
            return block, i - base
        else:
            block = self.tail
            end = self._size
            while end - len(block.items) > i:
                end -= len(block.items)
                block = block.prev
            base = end - len(block.items)
            return block, i - base

    def get(self, i):
        block, off = self._locate(i)
        return block.items[off]

    def set(self, i, x):
        block, off = self._locate(i)
        block.items[off] = x

    def __len__(self):
        return self._size


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
