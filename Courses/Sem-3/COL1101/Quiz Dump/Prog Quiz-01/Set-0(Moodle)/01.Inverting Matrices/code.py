def isvalid(A):
    if not isinstance(A,list): raise TypeError
    
    n=len(A)
    if n==0: raise ValueError
    
    
    
    for row in A:
        if not isinstance(row,list): raise TypeError
        if len(row) != n: raise ValueError
        
        for ele in row:
            if not isinstance(ele,(int,float)) or isinstance(ele,bool): raise TypeError

def deep_copy(A):
    return [[ele for ele in row] for row in A]

def identity(n):
    x=[[0] * n for i in range(n)]
    
    for i in range(n):
        x[i][i]=1
    return x
    
    
def matrix_inverse(A):
    isvalid(A)
    
    n=len(A)
    B=deep_copy(A)
    
    C=identity(n)
    
    ## Implementation
    
    for i in range(n):
        row = i
        while row<n and B[row][i]==0: row+=1
        
        # No pivot points 
        if row==n: raise ZeroDivisionError
        
        # Row swap
        B[i],B[row]=B[row],B[i]
        C[i],C[row]=C[row],C[i]
        
        # Setting pivot point
        val=B[i][i]
        
        for j in range(n):
            B[i][j]/=val
            C[i][j]/=val
         
        
        for a in range(n):
            if i!=a and B[a][i]!=0:
                val=B[a][i]
                
                for b in range(n):
                    B[a][b] -= val*B[i][b]
                    C[a][b] -= val*C[i][b]
    return C
