from typing import Any, Callable, Iterable, List, Union

# A value on the stack is either an int or a signal: a function int -> int.
Signal = Callable[[int], int]
Value = Union[int, Signal]

EMPTY = None   # the empty stack


def push(stack, value):
    """Return a new stack with value on top."""
    return (value,stack)


def top(stack):
    """Return the top value of the stack."""
    return stack[0]


def rest(stack):
    """Return the stack without its top value."""
    return stack[1]


def reduce(function: Callable[[Any, Any], Any], iterable: Iterable[Any], initial: Any) -> Any:
    """Fold function over iterable, starting from initial."""
    it=iter(iterable)
    item=next(it,None)
    if item is None:    return initial
    
    
    return reduce(function,it, function(initial,item))
    


def diff(f: Signal) -> Signal:
    """Return the signal g with g(x) = f(x + 1) - f(x)."""
    def g(x):  return f(x+1)-f(x)
    return g


def accumulate(f: Signal) -> Signal:
    """Return the signal h with h(x) = f(0) + f(1) + ... + f(x)."""
    def h(x):    return reduce(lambda total, i:total+f(i),range(x+1),0)
    return h


def step(functions: dict, words: dict) -> Callable[[Any, Any], Any]:
    """Return the combiner combine(stack, token) that reduce uses for one token."""
    def combine(stack,token):
        if type(token)== int:   return push(stack,token)
        
        if token in ['+','-','*']:
            b=top(stack)
            stack=rest(stack)
            
            a=top(stack)
            stack=rest(stack)
            
            if token=='+':  res=a+b
            elif token=='-':    res=a-b
            else:   res=a*b
            
            return push(stack,res)
        
        if token=='diff':   return push(rest(stack),diff(top(stack)))
        if token=='accumulate':     return push(rest(stack),accumulate(top(stack)))
        if token== 'sample':
            n=top(stack)
            stack=rest(stack)
            
            f=top(stack)
            stack=rest(stack)
            
            return push(stack,f(n))
        
        if token=='sample':
            n=top(stack)
            stack=rest(stack)
            
            f=top(stack)
            stack=rest(stack)
            
            return push(stack,f(n))
            
        if token in functions:
            return push(stack,functions[token])
            
        if token in words:
            return reduce(combine,words[token],stack)
    
    return combine
    
def final_value(stack) -> Value:
    """Return the single value left on the stack."""
    return top(stack)


def evaluate_postfix(tokens: List[Any], functions: dict, words: dict) -> Value:
    """Evaluate the tokens and return the result, an int or a signal."""
    combine=step(functions,words)
    x=reduce(combine,tokens,EMPTY)
    return final_value(x)
