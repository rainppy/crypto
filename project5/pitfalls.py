import ecdsa
import random
from hashlib import sha256
from func_1 import invmod
import myecdsa
import sm2_2

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
#问题5 DER编码
def encode_DER(sig):
    return "\x30".encode("latin-1")+ecdsa.der.encode_length(len(sig.s)+len(sig.r))+ecdsa.der.encode_integer(sig.r)+ecdsa.der.encode_integer(sig.s)
#问题6 攻击函数
def forge(n, G, P):
    u = random.randint(1, n-1)
    v = random.randint(1, n-1)
    R_ = G * u + P * v
    r_ = R_.x()
    s_ = (r_ * invmod(v, n)) % n
    e_ = (s_ * u) % n
    sig_ = ecdsa.ecdsa.Signature(r_, s_)
    return e_, sig_
#问题7 攻击函数
def mix(r, s, r_, s_, data, n):
    data = int.from_bytes(data, byteorder='big', signed=False)
    d = ((s * s_ - data) * invmod(r - s * s_ - s * r_, n)) % n
    return d
   
    
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
    print(encode_DER(sig))
    #6. One can forge signature if the verification does not check m
    #生成参数、公私钥对
    G = ecdsa.NIST384p.generator
    n = G.order()
    d = random.randint(1, n-1)
    vk = ecdsa.ecdsa.Public_key(G, G * d)
    sk = ecdsa.ecdsa.Private_key(vk, d)
    
    #敌手攻击，伪造签名
    P = vk.point
    e_, sig_ = forge(n, G, P)
    
    print("6.One can forge signature if the verification does not check m")
    #验证伪造的签名
    if(vk.verifies(e_, sig_)):
        print("*************Successfully forge signature!!!*************")
    
    #7. Same d and k in sm2 & ECDSA, leads to leaking of d
    #生成参数、公私钥对
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    ecdsa_crypt = myecdsa.CryptECDSA(public_key=public_key, private_key=private_key)
    sm2_crypt = sm2_2.CryptSM2(public_key=public_key, private_key=private_key)
    k = random.randint(1,int(ecdsa_crypt.n,16))
    data = b"111"
    r,s = ecdsa_crypt.sign(data, k)
    data_ = b"222"    
    r_,s_ = sm2_crypt.sign(data_, k)
    guess_d = mix(r, s, r_, s_, data, int(ecdsa_crypt.n,16))
    print("7. Same d and k in sm2 & ECDSA, leads to leaking of d")
    if guess_d==int(private_key, 16):
        print("*************Successfully forge signature!!!*************")
      
    
    
    
    
    
    
