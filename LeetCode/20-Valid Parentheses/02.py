class Solution:
    def isValid(self, s: str) -> bool:
        x=[]
        open=['(','[','{']
        dick={')':'(', ']' : '[', '}' : '{'}

        for c in s:
            if c in open:
                x.append(c)
            else:
                if len(x)==0:
                    return False
                else:
                    if dick[c]==x[-1]:
                        x.pop()
                    else: return False
        
        return len(x)==0

        
