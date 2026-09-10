import sys

# =============================================================================
# Q1: The Multi-Branch CampusBank
# =============================================================================
# Implement Account, SavingsAccount, CurrentAccount and Bank exactly as
# described in the question paper. Keep class / method names EXACTLY as
# given below -- the autograder drives your code only through Bank's
# public methods (called from solve(), which is already written for you).
#
# Reminder: round every balance to 2 decimal places with round(x, 2)
# immediately after it changes, so floating point noise cannot cause a
# spurious WA verdict.
# =============================================================================


class Account:
    """Base class for every kind of account. Do not instantiate directly."""

    TYPE_TAG = "ACCOUNT"

    def __init__(self, account_id, name, balance):
        """
        account_id : str, unique identifier
        name       : str, holder's name
        balance    : float, opening balance (already >= 0)

        Set up: self.account_id, self.name, self.balance (rounded to 2dp),
        self.status ("OPEN" initially), and an internal transaction log
        (a list of strings) that len(account) will report the size of.
        """
        # TODO: implement
        raise NotImplementedError

    def deposit(self, amount):
        """
        Add amount to balance if the account is OPEN, and append a log
        entry "DEPOSIT <amount>" (amount printed exactly as given, no
        trailing .0 formatting needed -- just str(amount) is fine since
        the driver always passes a float here; feel free to store the log
        message however you like as long as len() counts one entry per
        successful deposit). Return True on success, False if the account
        is not OPEN.
        """
        # TODO: implement
        raise NotImplementedError

    def withdraw(self, amount):
        """
        Polymorphic hook: each subclass enforces its own withdrawal rule.
        Must be overridden. Should return True/False exactly like deposit.
        """
        raise NotImplementedError

    def tick(self):
        """Polymorphic hook called once per TICK command. Default: no-op."""
        pass

    def __str__(self):
        """
        Return EXACTLY:
            "<account_id> <name> <TYPE_TAG> <balance:.2f> <status> <len(self)>"
        e.g. "A1 Priya SAVINGS 1050.00 OPEN 3"
        """
        # TODO: implement
        raise NotImplementedError

    def __len__(self):
        """Number of successful transactions logged (deposits, successful
        withdrawals, successful incoming/outgoing transfer legs, and a
        successful incoming MERGE) -- see the question paper for exactly
        which operations log an entry."""
        # TODO: implement
        raise NotImplementedError

    def __eq__(self, other):
        """Two accounts are equal iff they share the same account_id."""
        # TODO: implement
        raise NotImplementedError

    def __lt__(self, other):
        """
        Ordering used by Bank.top(): primarily by balance ascending; ties
        broken by account_id ascending (lexicographic string comparison).
        (Bank.top() will sort with reverse=True to get a descending
        leaderboard -- you only need to implement ascending "less than".)
        """
        # TODO: implement
        raise NotImplementedError

    def __add__(self, other):
        """
        If other is an Account, return the SUM of the two balances (a
        plain float, not a new Account). If other is an int/float, return
        self.balance + other. This is the operator used by Bank.merge().
        """
        # TODO: implement
        raise NotImplementedError


class SavingsAccount(Account):
    """
    Extra state: rate (interest rate applied on every TICK), limit (max
    number of successful withdrawals -- direct WITHDRAWs AND outgoing legs
    of a TRANSFER both count -- allowed per month), and a running counter
    of withdrawals made so far this month.
    """

    TYPE_TAG = "SAVINGS"

    def __init__(self, account_id, name, balance, rate, limit):
        # TODO: call super().__init__(...) then store rate, limit, and a
        # withdrawals-this-month counter starting at 0.
        raise NotImplementedError

    def withdraw(self, amount):
        """
        Denied (return False, balance unchanged) if the account is not
        OPEN, OR the monthly withdrawal counter has already reached
        `limit`, OR amount exceeds the current balance. Otherwise:
        subtract amount, round to 2dp, increment the counter, log
        "WITHDRAW <amount>", return True.
        """
        # TODO: implement
        raise NotImplementedError

    def tick(self):
        """
        If balance > 0: balance *= (1 + rate), rounded to 2dp (an
        overdrawn/zero balance never earns interest -- it can't happen for
        a SavingsAccount under these rules, but keep the guard anyway).
        Always reset the monthly withdrawal counter to 0.
        """
        # TODO: implement
        raise NotImplementedError


class CurrentAccount(Account):
    """Extra state: overdraft, the most negative the balance may go."""
    TYPE_TAG='CURRENT'          ## I wasted 45 mins debugging as this line was missing :)
    def __init__(self, account_id, name, balance, overdraft):
        # TODO: implement
        raise NotImplementedError

    def withdraw(self, amount):
        """
        Denied if the account is not OPEN, or if balance - amount would
        fall strictly below -overdraft. (Landing EXACTLY on -overdraft is
        allowed.) No monthly limit for current accounts.
        """
        # TODO: implement
        raise NotImplementedError

    # tick(): no interest, nothing to reset -- the inherited default is fine.


class Bank:
    """Owns every account, keyed by account_id."""

    def __init__(self):
        # TODO: set up whatever storage you need.
        raise NotImplementedError

    def create_savings(self, aid, name, balance, rate, limit):
        # TODO: implement
        raise NotImplementedError

    def create_current(self, aid, name, balance, overdraft):
        # TODO: implement
        raise NotImplementedError

    def deposit(self, aid, amount):
        """No-op if aid was never created or is CLOSED."""
        # TODO: implement
        raise NotImplementedError

    def withdraw(self, aid, amount):
        """No-op if aid was never created or is CLOSED."""
        # TODO: implement
        raise NotImplementedError

    def transfer(self, fid, tid, amount):
        """
        No-op if either account was never created or is CLOSED. Otherwise
        attempt to withdraw `amount` from fid (respecting that account's
        own withdrawal rule, polymorphically); only if that succeeds do
        you deposit `amount` into tid. A denied withdrawal must leave both
        accounts completely untouched (no partial transfer).
        """
        # TODO: implement
        raise NotImplementedError

    def tick(self):
        """Call .tick() on every currently-OPEN account."""
        # TODO: implement
        raise NotImplementedError

    def status(self, aid):
        """Return str(account), or the literal string "NOT FOUND" if aid
        was never created (whether or not it is currently CLOSED)."""
        # TODO: implement
        raise NotImplementedError

    def top(self, k):
        """
        Return a list of strings "<account_id> <balance:.2f>" for the top
        k OPEN accounts by balance descending (ties: account_id
        ascending), using the __lt__ ordering you defined above (e.g. via
        Python's sorted(..., reverse=True)). If k <= 0 return an empty
        list. If fewer than k open accounts exist, return all of them.
        """
        # TODO: implement
        raise NotImplementedError

    def merge(self, id1, id2):
        """
        No-op if either id was never created, either is already CLOSED,
        or id1 == id2. Otherwise: compute the combined balance using the
        `+` operator (Account.__add__) applied to the two account
        objects, assign that (rounded) value as id1's new balance, log a
        "MERGE <id2>" entry on id1, and CLOSE id2 (its status becomes
        "CLOSED" and its balance becomes 0.0 -- but its transaction count
        so far is preserved for any future STATUS query).
        """
        # TODO: implement
        raise NotImplementedError


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx].strip()); idx += 1
    bank = Bank()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        if not parts:
            continue
        cmd = parts[0]
        if cmd == "CREATE_SAVINGS":
            _, aid, name, bal, rate, limit = parts
            bank.create_savings(aid, name, float(bal), float(rate), int(limit))
        elif cmd == "CREATE_CURRENT":
            _, aid, name, bal, over = parts
            bank.create_current(aid, name, float(bal), float(over))
        elif cmd == "DEPOSIT":
            _, aid, amount = parts
            bank.deposit(aid, float(amount))
        elif cmd == "WITHDRAW":
            _, aid, amount = parts
            bank.withdraw(aid, float(amount))
        elif cmd == "TRANSFER":
            _, fid, tid, amount = parts
            bank.transfer(fid, tid, float(amount))
        elif cmd == "TICK":
            bank.tick()
        elif cmd == "STATUS":
            _, aid = parts
            out.append(bank.status(aid))
        elif cmd == "TOP":
            _, k = parts
            out.extend(bank.top(int(k)))
        elif cmd == "MERGE":
            _, id1, id2 = parts
            bank.merge(id1, id2)
        else:
            raise ValueError(f"bad command: {parts}")
    print("\n".join(out))


if __name__ == "__main__":
    solve()
