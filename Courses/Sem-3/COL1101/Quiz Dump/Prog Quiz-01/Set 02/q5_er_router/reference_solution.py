import sys

NUM_LEVELS = 5


class PNode:
    __slots__ = ("pid", "level", "prev", "next")

    def __init__(self, pid, level):
        self.pid = pid
        self.level = level
        self.prev = None
        self.next = None


class LevelQueue:
    """Doubly linked FIFO for one triage level."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def push_back(self, node):
        node.prev = self.tail
        node.next = None
        if self.tail is not None:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self.count += 1

    def push_front(self, node):
        node.next = self.head
        node.prev = None
        if self.head is not None:
            self.head.prev = node
        else:
            self.tail = node
        self.head = node
        self.count += 1

    def remove(self, node):
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self.count -= 1

    def pop_front(self):
        node = self.head
        self.remove(node)
        return node

    def is_empty(self):
        return self.count == 0


class Router:
    def __init__(self):
        self.levels = [LevelQueue() for _ in range(NUM_LEVELS)]
        self.by_id = {}
        self.discharge_stack = []  # entries: (pid, original_level)

    def register(self, pid, level):
        if pid in self.by_id:
            return
        node = PNode(pid, level)
        self.levels[level - 1].push_back(node)
        self.by_id[pid] = node

    def peek(self):
        for lvl in self.levels:
            if not lvl.is_empty():
                return lvl.head.pid
        return -1

    def serve(self):
        for lvl in self.levels:
            if not lvl.is_empty():
                node = lvl.pop_front()
                del self.by_id[node.pid]
                self.discharge_stack.append((node.pid, node.level))
                return node.pid
        return -1

    def count(self):
        return len(self.by_id)

    def requeue(self, pid, new_level):
        node = self.by_id.get(pid)
        if node is None:
            return
        self.levels[node.level - 1].remove(node)
        node.level = new_level
        node.prev = node.next = None
        self.levels[new_level - 1].push_back(node)

    def recall(self):
        if not self.discharge_stack:
            return -1
        pid, orig_level = self.discharge_stack.pop()
        node = PNode(pid, orig_level)
        self.levels[orig_level - 1].push_front(node)
        self.by_id[pid] = node
        return pid


def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    r = Router()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "REGISTER":
            r.register(parts[1], int(parts[2]))
        elif cmd == "NEXT":
            out.append(str(r.peek()))
        elif cmd == "SERVE":
            out.append(str(r.serve()))
        elif cmd == "COUNT":
            out.append(str(r.count()))
        elif cmd == "REQUEUE":
            r.requeue(parts[1], int(parts[2]))
        elif cmd == "RECALL":
            out.append(str(r.recall()))
        else:
            raise ValueError(cmd)
    print("\n".join(out))


if __name__ == "__main__":
    solve()
