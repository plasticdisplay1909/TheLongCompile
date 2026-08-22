import sys

class Node:
    def __init__(self,data=None):
        self.data=data
        self.prev,self.next=None,None


class LadderList:
    def __init__(self):
        # TODO: set up whatever internal state you need.
        # raise NotImplementedError
        self.n=0

        # As [head,tail,size]
        self.level=[[None,None,0]]

    #############################################
    ##           Helper functions              ##
    #############################################
    def create(self):
        """Create new empty"""
        self.level.append([None,None,0])

    def addnode(self,curr,node):
        """Add node at end of each level"""
        head,tail,size=self.level[curr]

        if head is None:
            self.level[curr][0]=node
            self.level[curr][1]=node
        else:
            node.prev=tail
            tail.next=node
            self.level[curr][1]=node

        self.level[curr][2]+=1

    def removenode(self,curr):
        head,tail,size=self.level[curr]
        node=tail

        if node.prev is None:
            # Nothing exist
            self.level[curr][0]=None
            self.level[curr][1]=None

        else:
            new=node.prev
            new.next=None
            self.level[curr][1]=new
            node.prev=None

        self.level[curr][2]-=1
        node.next=None
        return node

    #############################################
    ###             Given functions           ###
    #############################################
    def append(self, x):
        """
        Add x as the new last element.
        Must run in O(log n) worst-case time.

        TODO: implement this.
        """
        # raise NotImplementedError
        node=Node(x)

        ## Add each of them to level 0 orignially
        self.addnode(0,node)
        self.n+=1

        pos=self.n-1
        curr=node
        meow=0      ## Shows height


        while pos%2 ==1:
            # Make next level
            if (meow+1) == len(self.level):
                self.create()

            ## Higher level store from below
            next=Node(curr)
            self.addnode(meow+1,next)

            curr=next
            meow+=1

            # For next level
            pos//=2


        """Highest level must be empty"""
        if self.level[-1][2] !=0:
            self.create()
            
    def pop(self):
        """
        Remove and return the current last element.
        Must run in O(log n) worst-case time.
        You may assume this is only called when the LadderList is non-empty.

        TODO: implement this.
        """
        # raise NotImplementedError
        last=self.level[0][1]
        val=last.data

        ## Index being removed
        pos=self.n-1
        self.removenode(0)

        self.n-=1

        ## Remvoe promoted copy
        # Odd nodes at current level was promoted

        meow=0      ## Shows height

        while pos%2==1:
            meow+=1
            self.removenode(meow)
            pos//=2

        """ Maintain level"""
        if self.n==0:
            # Only level 0  should remain
            self.level=[[None,None,0]]
        else:
            while (len(self.level)>2 and self.level[-1][2]==0 and self.level[-2][2]==0):
                self.level.pop()

        return val
    
    def __getitem__(self, i):
        """
        Return the element currently at position i (i.e. what my_list[i]
        would return). Must run in O(log n) worst-case time.
        You may assume 0 <= i < len(self) whenever this is called.

        TODO: implement this. Fix and document your indexing convention.
        """
        # raise NotImplementedError

        # Last level is empty
        height=len(self.level)-2

        node=self.level[height][0]
        idx=2**height-1

        ## Go down on them one at a time
        height-=1

        while height>=0:
            node=node.data
            step= 2**height

            ## If too far night,move one left
            if idx > i:
                node=node.prev
                idx-=step

            elif idx+step <=i:
                ## if left is not past i, move one right
                node=node.next
                idx +=step

            height-=1

        # At 0, node store actual data
        return node.data

    
    def __setitem__(self, i, x):
        """
        Update the element at position i to x (i.e. what my_list[i] = x
        would do). Must run in O(log n) worst-case time.
        You may assume 0 <= i < len(self) whenever this is called.

        TODO: implement this.
        """

        # Same as _getitem

        height=len(self.level)-2
        idx=2**height-1

        node=self.level[height][0]

        height-=1
        ## Go down one at a time
        while height>=0:
            node=node.data
            step=2**height

            ## Move left
            if idx>i:
                node=node.prev
                idx-=step

            # Move right
            elif idx+step<=i:
                node=node.next
                idx+=step

            ## Go done one at a time
            height-=1
        # raise NotImplementedError

        # return node 0
        node.data=x

    def __len__(self):
        """
        Return the number of elements currently stored.
        Must run in O(1) worst-case time (e.g. maintain a running count
        rather than walking the whole structure on every call).

        TODO: implement this.
        """
        return self.n
        # raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1

    ll = LadderList()
    out = []
    for _ in range(q):
        line = data[idx].split(); idx += 1
        if line[0] == "append":
            ll.append(int(line[1]))
        elif line[0] == "pop":
            out.append(str(ll.pop()))
        elif line[0] == "access":
            out.append(str(ll[int(line[1])]))
        elif line[0] == "set":
            ll[int(line[1])] = int(line[2])
        elif line[0] == "len":
            out.append(str(len(ll)))
        else:
            raise ValueError(f"unrecognized op: {line}")

    print("\n".join(out))


if __name__ == "__main__":
    solve()
