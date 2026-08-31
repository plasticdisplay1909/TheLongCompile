import sys


class Buffer:
    """Fixed-capacity circular FIFO buffer implemented on a plain array."""

    def __init__(self, capacity):
        self.cap = capacity
        self.data = [None] * capacity
        self.start = 0
        self.count = 0

    def is_full(self):
        return self.count == self.cap

    def is_empty(self):
        return self.count == 0

    def enqueue(self, item):
        pos = (self.start + self.count) % self.cap
        self.data[pos] = item
        self.count += 1

    def dequeue(self):
        item = self.data[self.start]
        self.start = (self.start + 1) % self.cap
        self.count -= 1
        return item


class WaitQueue:
    """O(1) FIFO of waiting thread ids, implemented as a singly linked
    list with head/tail pointers (this is the reference: it deliberately
    avoids Python list.pop(0), which is O(n) per call)."""

    class _Node:
        __slots__ = ("tid", "payload", "next")

        def __init__(self, tid, payload):
            self.tid = tid
            self.payload = payload
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def push(self, tid, payload=None):
        node = WaitQueue._Node(tid, payload)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.count += 1

    def pop(self):
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self.count -= 1
        return (node.tid, node.payload)

    def peek(self):
        return (self.head.tid, self.head.payload)

    def is_empty(self):
        return self.count == 0


class Bakery:
    def __init__(self, capacity):
        self.buf = Buffer(capacity)
        self.producer_wait = WaitQueue()
        self.consumer_wait = WaitQueue()
        self.log = []

    def _wake_producers_if_possible(self):
        while not self.producer_wait.is_empty() and not self.buf.is_full():
            tid, item = self.producer_wait.pop()
            self.buf.enqueue(item)
            self.log.append(f"WOKEN {tid} PRODUCED {item}")

    def _wake_consumers_if_possible(self):
        while not self.consumer_wait.is_empty() and not self.buf.is_empty():
            tid, _ = self.consumer_wait.pop()
            item = self.buf.dequeue()
            self.log.append(f"WOKEN {tid} CONSUMED {item}")

    def produce(self, tid, item):
        if not self.producer_wait.is_empty() or self.buf.is_full():
            self.producer_wait.push(tid, item)
            self.log.append(f"BLOCKED {tid}")
            return
        self.buf.enqueue(item)
        self.log.append(f"PRODUCED {tid} {item}")
        self._wake_consumers_if_possible()

    def consume(self, tid):
        if not self.consumer_wait.is_empty() or self.buf.is_empty():
            self.consumer_wait.push(tid)
            self.log.append(f"BLOCKED {tid}")
            return
        item = self.buf.dequeue()
        self.log.append(f"CONSUMED {tid} {item}")
        self._wake_producers_if_possible()

    def status(self):
        items = []
        for i in range(self.buf.count):
            items.append(self.buf.data[(self.buf.start + i) % self.buf.cap])
        p = self.producer_wait.peek()[0] if not self.producer_wait.is_empty() else "-"
        c = self.consumer_wait.peek()[0] if not self.consumer_wait.is_empty() else "-"
        return f"BUF[{','.join(map(str,items))}] PWAIT={p} CWAIT={c}"


def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    cap = int(data[idx]); idx += 1
    bakery = Bakery(cap)
    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        before = len(bakery.log)
        if cmd == "PRODUCE":
            bakery.produce(parts[1], parts[2])
        elif cmd == "CONSUME":
            bakery.consume(parts[1])
        elif cmd == "STATUS":
            out.append(bakery.status())
            continue
        else:
            raise ValueError(cmd)
        out.extend(bakery.log[before:])
    print("\n".join(out))


if __name__ == "__main__":
    solve()
