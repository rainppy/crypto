import ecdsa
import random
from hashlib import sha256
from func import invmod
#问题1攻击函数
def leak_k(e, k, sig, n):    
    return (invmod(sig.r, n) * (k * sig.s - e)) % n
#问题2 攻击函数
def reuse_k(e1, e2, sig1, sig2, n):
    return ((sig1.s * e2 - sig2.s * e1 ) * invmod((sig2.s * sig1.r) - (sig1.s * sig1.r) , n))% n 
#问题3 攻击函数
def other_k(e1, e2, sig1, sig2, n, d1):
    return ((sig2.s * e1 + sig2.s * d1 * sig1.r -sig1.s * e2) * invmod(sig1.r * sig1.s, n)) % n
#问题4 攻击函数
def Mallea(sig):
    sig_ = ecdsa.ecdsa.Signature(sig.r,(-sig.s) % n)
    return sig_
    
if __name__=="__main__":
    #1. Leaking k leads to leaking of d
    #生成参数、公私钥对
    G = ecdsa.NIST384p.generator
    n = G.order()
    d = random.randint(1, n-1)
    vk = ecdsa.ecdsa.Public_key(G, G * d)
    sk = ecdsa.ecdsa.Private_key(vk, d)
    
    #签名
    m = b"Nice to meet u!"
    e = int(sha256(m).hexdigest(), 16)
    k = random.randint(1, n-1)#nonce,暴露给敌手
    sig = sk.sign(e,k)
    #print('message: ' , m)
    #print ("signature: ", sig.r, sig.s)
    
    #攻击，获得私钥
    guess_sk = leak_k(e, k, sig, n)
        
    #验证攻击结果
    print("           1. Leaking k leads to leaking of d           ")
    if(guess_sk==d):
        print("***********Successfully deduce private key!!!***********")
    
    #2. Reusing k leads to leaking of d
    #生成参数、公私钥对
    G = ecdsa.NIST384p.generator
    n = G.order()
    d = random.randint(1, n-1)
    vk = ecdsa.ecdsa.Public_key(G, G * d)
    sk = ecdsa.ecdsa.Private_key(vk, d)
    
    #得到两对消息及签名
    k = random.randint(1, n-1)
    m1 = b"Nice to meet u!"
    e1 = int(sha256(m1).hexdigest(), 16)
    sig1 = sk.sign(e1,k)
    m2 = b"Nice to meet u, too!!!!!"
    e2 = int(sha256(m2).hexdigest(), 16)
    sig2 = sk.sign(e2,k)#k重用
   
    #攻击，获得私钥
    guess_sk = reuse_k(e1, e2, sig1, sig2, n)
    #验证攻击结果
    print("           2. Reusing k leads to leaking of d           ")
    if(guess_sk==d):
        print("***********Successfully deduce private key!!!***********")    
    #3. Two users, using k leads to leaking of d
    #生成参数、公私钥对
    G = ecdsa.NIST384p.generator
    n = G.order()
    
    #Alice 公私钥对
    dA = random.randint(1, n-1)
    vkA = ecdsa.ecdsa.Public_key(G, G * dA)
    skA = ecdsa.ecdsa.Private_key(vkA, dA)
    #Bob 公私钥对
    dB = random.randint(1, n-1)
    vkB = ecdsa.ecdsa.Public_key(G, G * dB)
    skB = ecdsa.ecdsa.Private_key(vkB, dB)
    
    #Alice签名
    m1 = b"Nice to meet u!"
    e1 = int(sha256(m1).hexdigest(), 16)
    k = random.randint(1, n-1)#nonce,重用
    sig1 = skA.sign(e1,k)
    #Bob签名
    m2 = b"Nice to meet u,too!"
    e2 = int(sha256(m2).hexdigest(), 16)
    sig2 = skB.sign(e2,k)
    
    #Alice推测Bob私钥
    guess_dB = other_k(e1, e2, sig1, sig2, n, dA)
    
    #验证攻击结果
    print("      3. Two users, using k leads to leaking of d      ")
    if(guess_dB == dB):
        print("***********Successfully deduce private key!!!***********")
    
    #4. Malleability
    #生成参数、公私钥对
    G = ecdsa.NIST384p.generator
    n = G.order()
    d = random.randint(1, n-1)
    vk = ecdsa.ecdsa.Public_key(G, G * d)
    sk = ecdsa.ecdsa.Private_key(vk, d)
    
    #获得签名(r,s)
    m = b"Nice to meet u!"
    e = int(sha256(m).hexdigest(), 16)
    k = random.randint(1, n-1)#nonce,暴露给敌手
    sig = sk.sign(e,k)    
    
    #伪造合法签名(r,-s)
    sig_ = Mallea(sig)
    print("                    4.Malleability                     ")
    #验证伪造的签名
    if(vk.verifies(e, sig_)):
        print("*************Successfully forge signature!!!*************")
    
    #5. DER encode
    print("                    5. DER encode                    ")
    print("********************见文档理论分析********************")
    
    
    
    
    
    
