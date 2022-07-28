import ecdsa
import random
from func import invmod,sqrtmod
from hashlib import sha256

#NIST384p parameters
ECC ={'p':39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319,
      'b':int("b3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef",16)}
def deduce_pk(sig, e, G, n):
    r = sig.r
    s = sig.s
    x1 = r 
    y_square = (pow(x1, 3, ECC['p']) -3 * x1 + ECC['b']) % ECC['p']
    y1,y1_ = sqrtmod(y_square, ECC['p'])
    kG = ecdsa.ellipticcurve.PointJacobi(ecdsa.NIST384p.curve, x1, y1, 1)
    P = ((kG * s) + (G * (-e))) * (invmod(r, n)) 
    kG_ = ecdsa.ellipticcurve.PointJacobi(ecdsa.NIST384p.curve, x1, y1_, 1)
    P_ = ((kG_ * s) + (G * (-e))) * (invmod(r, n))    
    return P, P_

if __name__ == "__main__":
    #生成参数、公私钥对
    G = ecdsa.NIST384p.generator
    n = G.order()
    d = random.randint(1, n-1)
    vk = ecdsa.ecdsa.Public_key(G, G * d)
    sk = ecdsa.ecdsa.Private_key(vk, d)
    
    #生成一个签名
    m = b"Nice to meet u!"
    e = int(sha256(m).hexdigest(), 16)
    k = random.randint(1, n -1 )
    sig = sk.sign(e, k)
    
    #从签名恢复公钥,有两种可能的结果
    P,P_= deduce_pk(sig, e, G, n)
    
    if(P == (G * d)):
        print("Deduce pubilc key:({},{})".format(P.x(),P.y()))
        print("True public key:({},{})".format((G * d).x(),(G * d).y()))
        print("Success!")
    if(P_ == (G * d)):
        print("Deduce pubilc key:({},{})".format(P_.x(),P_.y()))
        print("True public key:({},{})".format((G * d).x(),(G * d).y()))
        print("Suceess!！")

        