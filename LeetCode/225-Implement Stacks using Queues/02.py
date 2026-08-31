class MyStack:
    def __init__(self):
        self.q1=collections.deque()
        self.q2=collections.deque()

    def push(self, x: int) -> None:
        self.q1.append(x)

    def pop(self) -> int:
        while len(self.q1)!=1:
            self.q2.append(self.q1.popleft())
        
        # Now after this q1 becomes empty
        # And q2 has all elements of q1
        val=self.q1.popleft()

        # Interchanging q1 and q2
        self.q1,self.q2=self.q2,self.q1
        return val

    def top(self) -> int:
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        
        val=self.q1[0]  # Top element

        # This interchange q1 and q2 completely without discrimination
        self.q2.append(self.q1.popleft())

        # Again interchanging 
        self.q1,self.q2=self.q2,self.q1
        return val

    def empty(self) -> bool:
        return not self.q1


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()
