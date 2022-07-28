
def gcd(a,b):
    while(b>=1):
        a,b=b,a%b
    return a
#方法1：利用扩展欧几里得算法求模逆
def FindModInverse(a,m):
    if gcd(a,m)!=1:
        return None
    u1,u2,u3=1,0,a
    v1,v2,v3=0,1,m
    while v3!=0:
        q=u3//v3
        v1,v2,v3,u1,u2,u3=u1-v1*q,u2-v2*q,a-v3*q,v1,v2,v3
    return u1%m
#方法2：利用费马小定理求模逆
def invmod(x,n):
    '''using Fermat's little theorem'''
    if gcd(x,n)!=1:
        return None
    else:
        return pow(x,n-2,n)
# Legendre
def Legendre(a, p):
    return pow(a, (p-1)//2, p)

def sqrtmod(a, p):
    #先用Legendre符号判定有无二次剩余
    if(Legendre(a, p) == -1):
        return None
    #再用Tonelli–Shanks算法求解二次剩余
    Q = p-1
    S = 0
    while(Q % 2 == 0):
        Q //= 2
        S  += 1
    if 1 == S:
        R = pow(a, (p+1)//4, p)
        R_ = (-R) % p
        return R, R_
    for z in range(2,p):
        if(Legendre(z, p) == -1):
            break
    c = pow(z, Q, p)
    R = pow(a, (Q+1)/2, p)
    t = pow(a, Q, p)
    M = S
    while((t % p) != 1):
        t_ = t
        for i in range(1, M):
            t_ = pow(t_, 2)
            if t_ % p == 1:
                break
        b = (pow(c, pow(2, M-i-1), p)) % p
        R = (R * b) % p
        t = (t * pow(b, 2)) % p
        c = (pow(b, 2)) % p
        M = i
    R_ = p -R
    return R, R_
