
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

    