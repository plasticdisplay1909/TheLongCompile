def smallest_element(a):
    lo,hi=0,len(a)-1
    
    # Base case
    if len(a)<=2:
        return min(a)
    
    while lo<hi:
        mid = (lo+hi)//2
        
        if a[mid] > a[mid+1]: lo=mid+1
        else: hi=mid
    
    return a[lo]
