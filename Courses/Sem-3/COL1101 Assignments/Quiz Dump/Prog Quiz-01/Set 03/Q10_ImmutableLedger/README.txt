Q10 -- The Immutable Ledger: a note on grading

`visible_cases_1.txt` / `visible_cases_2.txt` exercise PART A and PART B
(the persistent trie and the Ledger's version bookkeeping) SEQUENTIALLY,
through the ordinary stdin protocol described in the question -- exactly
like every other problem in this set.

The CONCURRENCY requirement on the Ledger class (multiple readers and
writers safely sharing one Ledger, with only the "publish" step under
the lock) cannot be exercised through a sequential stdin script at all,
so `autograder.py` additionally imports your `Ledger` class directly and
runs two multithreaded stress tests against it (see
`hidden_concurrent_unique_ids` and `hidden_concurrent_read_stability`
in the autograder's output). A deadlock shows up as a timeout; a race
condition shows up as an assertion failure.

Run `python3 autograder.py` directly to see all of this locally.
