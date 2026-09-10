def polynomial_add(l0, l1):
    answer = []
    for i in range(len(l0)):
        answer.append(l0[i]+l1[i])
    return answer


def polynomial_multiply_recursive(p, q):
    n=len(p)
    
    if n==1: return [p[0]*q[0],0]
    
    m=n//2
    p0,q0=p[:m],q[:m]
    p1,q1=p[m:],q[m:]
    
    ans=[0]*(2*n)
    
    #p0*q0
    r0=polynomial_multiply_recursive(p0,q0)
    for i in range(len(r0)): ans[i]+=r0[i]
    
    # p1*q1
    r1=polynomial_multiply_recursive(p1,q1)
    for i in range(len(r1)): ans[i+n]+=r1[i]
    
    # (p0+p1) * (q0+q1) -p0*q0 -p1*q1
    px=polynomial_add(p0,p1)
    qx=polynomial_add(q0,q1)
    rx=polynomial_multiply_recursive(px,qx)
    
    mid=[]
    for i in range(len(rx)): mid.append(rx[i] - r0[i]-r1[i])
    for i in range(len(mid)): ans[i+m]+=mid[i]
    
    return ans
