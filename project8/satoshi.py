import ecdsa
import random

def gcd(a,b):
    while(b>=1):
        a,b=b,a%b
    return a

def invmod(x,n):
    '''using Fermat's little theorem'''
    if gcd(x,n)!=1:
        return None
    else:
        return pow(x,n-2,n)
#攻击函数
def forge(n, G, P):
    u = random.randint(1, n-1)
    v = random.randint(1, n-1)
    R_ = G * u + P * v
    r_ = R_.x()
    s_ = (r_ * invmod(v, n)) % n
    e_ = (s_ * u) % n
    sig_ = ecdsa.ecdsa.Signature(r_, s_)
    return e_, sig_

if __name__ =="__main__":
       #生成参数、公私钥对
    G = ecdsa.SECP256k1.generator
    n = G.order()
    d = random.randint(1, n-1)
    vk = ecdsa.ecdsa.Public_key(G, G * d)
    sk = ecdsa.ecdsa.Private_key(vk, d)
    
    #敌手攻击，伪造签名
    P = vk.point
    e_, sig_ = forge(n, G, P)
    
    #验证伪造的签名
    if(vk.verifies(e_, sig_)):
        print("*************Successfully forge signature!!!*************")
    
