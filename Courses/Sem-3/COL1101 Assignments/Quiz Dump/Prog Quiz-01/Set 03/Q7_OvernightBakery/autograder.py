"""
Autograder for Q7: The Overnight Bakery.

Concurrency correctness cannot be checked by comparing stdout to one
fixed expected string the way a sequential problem can -- interleavings
are non-deterministic. Instead, each test below is a small self-checking
Python program that imports YOUR BoundedBuffer, spins up producer and/or
consumer threads against it, and asserts an invariant that must hold no
matter how the scheduler interleaves things (e.g. "every item produced
was consumed exactly once", or "a put() on a full buffer does not
return until a slot frees up"). Each test is run in its own subprocess
with a timeout: a real deadlock (a classic bug in bounded-buffer code)
shows up as a timeout (TLE), a violated invariant shows up as an
assertion failure (WA), and any exception is a runtime error (RE).
"""
import subprocess
import sys
import time
import os

TIME_LIMIT = 6.0
HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE = os.path.join(HERE, "student_code.py")


def run_snippet(code, time_limit=TIME_LIMIT):
    try:
        result = subprocess.run([sys.executable, "-c", code], capture_output=True,
                                 text=True, timeout=time_limit)
        if result.returncode != 0:
            err = (result.stderr.strip().splitlines() or ["error"])[-1]
            return "RE", err
        return "OK", result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TLE", None


HEADER = f"import sys; sys.path.insert(0, {HERE!r})\n"


SNIPPET_BASIC_ORDER = HEADER + r'''
from student_code import BoundedBuffer
import threading

buf = BoundedBuffer(3)
N = 500
consumed = []

def producer():
    for i in range(N):
        buf.put(i)

def consumer():
    for _ in range(N):
        consumed.append(buf.get())

pt = threading.Thread(target=producer)
ct = threading.Thread(target=consumer)
pt.start(); ct.start()
pt.join(); ct.join()

assert consumed == list(range(N)), f"expected strict FIFO order, got first mismatch near {[ (i,a,b) for i,(a,b) in enumerate(zip(consumed, range(N))) if a != b ][:3]}"
print("OK")
'''


SNIPPET_NO_LOSS_NO_DUP = HEADER + r'''
from student_code import BoundedBuffer
import threading

CAPACITY = 5
NUM_PRODUCERS = 6
NUM_CONSUMERS = 5
ITEMS_PER_PRODUCER = 800
TOTAL = NUM_PRODUCERS * ITEMS_PER_PRODUCER

buf = BoundedBuffer(CAPACITY)
results = []
results_lock = threading.Lock()
reserve_lock = threading.Lock()
reserved = [0]

def producer(pid):
    base = pid * ITEMS_PER_PRODUCER
    for i in range(ITEMS_PER_PRODUCER):
        buf.put(base + i)

def consumer():
    while True:
        with reserve_lock:
            if reserved[0] >= TOTAL:
                return
            reserved[0] += 1
        item = buf.get()
        with results_lock:
            results.append(item)

producers = [threading.Thread(target=producer, args=(i,)) for i in range(NUM_PRODUCERS)]
consumers = [threading.Thread(target=consumer) for _ in range(NUM_CONSUMERS)]
for t in producers + consumers:
    t.start()
for t in producers + consumers:
    t.join()

assert len(results) == TOTAL, f"expected {TOTAL} items consumed in total, got {len(results)} (lost or duplicated items)"
assert sorted(results) == list(range(TOTAL)), "the multiset of consumed items does not match the multiset of produced items"
print("OK")
'''


SNIPPET_PUT_BLOCKS_WHEN_FULL = HEADER + r'''
from student_code import BoundedBuffer
import threading
import time

buf = BoundedBuffer(1)
buf.put("first")

flag = {"put_returned": False}

def putter():
    buf.put("second")
    flag["put_returned"] = True

t = threading.Thread(target=putter)
t.start()
time.sleep(0.5)
assert not flag["put_returned"], "put() on a FULL buffer returned before any slot was freed -- it must block"

got = buf.get()
assert got == "first", f"get() should return the oldest item first, got {got!r}"

t.join(timeout=3)
assert flag["put_returned"], "put() never returned even after a slot was freed -- possible deadlock or missed wakeup"

got2 = buf.get()
assert got2 == "second", f"expected the second item next, got {got2!r}"
print("OK")
'''


SNIPPET_GET_BLOCKS_WHEN_EMPTY = HEADER + r'''
from student_code import BoundedBuffer
import threading
import time

buf = BoundedBuffer(2)
flag = {"got": None}

def getter():
    flag["got"] = buf.get()

t = threading.Thread(target=getter)
t.start()
time.sleep(0.5)
assert flag["got"] is None, "get() on an EMPTY buffer returned before any item was put -- it must block"

buf.put(42)
t.join(timeout=3)
assert flag["got"] == 42, f"expected the getter to eventually receive 42, got {flag['got']!r} (possible deadlock or missed wakeup)"
print("OK")
'''


SNIPPET_CAPACITY_NEVER_EXCEEDED = HEADER + r'''
from student_code import BoundedBuffer
import threading

CAPACITY = 4
buf = BoundedBuffer(CAPACITY)
max_seen = [0]
lock = threading.Lock()
stop = [False]

def watcher():
    while not stop[0]:
        s = buf.qsize()
        with lock:
            if s > max_seen[0]:
                max_seen[0] = s

def producer():
    for i in range(3000):
        buf.put(i)

def consumer():
    for _ in range(3000):
        buf.get()

w = threading.Thread(target=watcher)
p = threading.Thread(target=producer)
c = threading.Thread(target=consumer)
w.start(); p.start(); c.start()
p.join(); c.join()
stop[0] = True
w.join(timeout=2)

assert max_seen[0] <= CAPACITY, f"buffer size was observed to exceed capacity: saw {max_seen[0]} > {CAPACITY}"
print("OK", max_seen[0])
'''


TESTS = [
    ("hidden_single_producer_consumer_fifo", SNIPPET_BASIC_ORDER, 15),
    ("hidden_put_blocks_when_full", SNIPPET_PUT_BLOCKS_WHEN_FULL, 15),
    ("hidden_get_blocks_when_empty", SNIPPET_GET_BLOCKS_WHEN_EMPTY, 15),
    ("hidden_capacity_never_exceeded", SNIPPET_CAPACITY_NEVER_EXCEEDED, 15),
    ("hidden_multi_producer_multi_consumer_no_loss", SNIPPET_NO_LOSS_NO_DUP, 40),
]


def main():
    total, max_total = 0, 0
    for name, code, weight in TESTS:
        max_total += weight
        status, payload = run_snippet(code)
        if status == "TLE":
            print(f"[{name:42s}] TLE (possible deadlock)   weight={weight:3d} -> 0/{weight}")
        elif status == "RE":
            print(f"[{name:42s}] RE  ({payload})   weight={weight:3d} -> 0/{weight}")
        elif payload.startswith("OK"):
            print(f"[{name:42s}] AC  ({payload})            weight={weight:3d} -> {weight}/{weight}")
            total += weight
        else:
            print(f"[{name:42s}] WA  ({payload})            weight={weight:3d} -> 0/{weight}")

    print("-" * 70)
    print(f"TOTAL: {total} / {max_total}  ({100.0*total/max_total:.1f}%)")


if __name__ == "__main__":
    main()
