import sys


class Account:
    TYPE_TAG = "ACCOUNT"

    def __init__(self, account_id, name, balance):
        self.account_id = account_id
        self.name = name
        self.balance = round(float(balance), 2)
        self.status = "OPEN"
        self._log = []

    def deposit(self, amount):
        if self.status != "OPEN":
            return False
        self.balance = round(self.balance + amount, 2)
        self._log.append(f"DEPOSIT {amount}")
        return True

    def withdraw(self, amount):
        raise NotImplementedError

    def tick(self):
        pass

    def __str__(self):
        return f"{self.account_id} {self.name} {self.TYPE_TAG} {self.balance:.2f} {self.status} {len(self)}"

    def __len__(self):
        return len(self._log)

    def __eq__(self, other):
        if isinstance(other, Account):
            return self.account_id == other.account_id
        return False

    def __lt__(self, other):
        if self.balance != other.balance:
            return self.balance < other.balance
        return self.account_id < other.account_id

    def __add__(self, other):
        if isinstance(other, Account):
            return self.balance + other.balance
        elif isinstance(other, (int, float)):
            return self.balance + float(other)
        return NotImplemented


class SavingsAccount(Account):
    TYPE_TAG = "SAVINGS"

    def __init__(self, account_id, name, balance, rate, limit):
        super().__init__(account_id, name, balance)
        self.rate = rate
        self.limit = limit
        self.withdrawals_this_month = 0

    def withdraw(self, amount):
        if self.status != "OPEN":
            return False
        if self.withdrawals_this_month >= self.limit:
            return False
        if amount > self.balance:
            return False
        self.balance = round(self.balance - amount, 2)
        self.withdrawals_this_month += 1
        self._log.append(f"WITHDRAW {amount}")
        return True

    def tick(self):
        if self.balance > 0:
            self.balance = round(self.balance * (1 + self.rate), 2)
        self.withdrawals_this_month = 0


class CurrentAccount(Account):
    TYPE_TAG = "CURRENT"

    def __init__(self, account_id, name, balance, overdraft):
        super().__init__(account_id, name, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if self.status != "OPEN":
            return False
        if self.balance - amount < -self.overdraft - 1e-9:
            return False
        self.balance = round(self.balance - amount, 2)
        self._log.append(f"WITHDRAW {amount}")
        return True

    def tick(self):
        pass


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_savings(self, aid, name, balance, rate, limit):
        self.accounts[aid] = SavingsAccount(aid, name, balance, rate, limit)

    def create_current(self, aid, name, balance, overdraft):
        self.accounts[aid] = CurrentAccount(aid, name, balance, overdraft)

    def get(self, aid):
        return self.accounts.get(aid)

    def deposit(self, aid, amount):
        acc = self.get(aid)
        if acc is None or acc.status != "OPEN":
            return
        acc.deposit(amount)

    def withdraw(self, aid, amount):
        acc = self.get(aid)
        if acc is None or acc.status != "OPEN":
            return
        acc.withdraw(amount)

    def transfer(self, fid, tid, amount):
        f = self.get(fid)
        t = self.get(tid)
        if f is None or t is None or f.status != "OPEN" or t.status != "OPEN":
            return
        if f.withdraw(amount):
            t.deposit(amount)

    def tick(self):
        for acc in self.accounts.values():
            if acc.status == "OPEN":
                acc.tick()

    def status(self, aid):
        acc = self.get(aid)
        if acc is None:
            return "NOT FOUND"
        return str(acc)

    def top(self, k):
        if k <= 0:
            return []
        open_accs = [a for a in self.accounts.values() if a.status == "OPEN"]
        open_accs.sort(reverse=True)
        return [f"{a.account_id} {a.balance:.2f}" for a in open_accs[:k]]

    def merge(self, id1, id2):
        a1 = self.get(id1)
        a2 = self.get(id2)
        if a1 is None or a2 is None or id1 == id2:
            return
        if a1.status != "OPEN" or a2.status != "OPEN":
            return
        new_balance = a1 + a2
        a1.balance = round(new_balance, 2)
        a1._log.append(f"MERGE {id2}")
        a2.status = "CLOSED"
        a2.balance = 0.0


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
