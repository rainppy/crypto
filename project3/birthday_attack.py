from sm3 import sm3_hash
import random
import string

n = 256
front = 44 #攻击前32 bit的碰撞为例
str_to_list = lambda data: [i for i in bytes(data,encoding="ascii")]
def birth_attack(front):
    T_hash={}
    while(1):
        a = ''.join(random.sample(string.ascii_letters + string.digits, 30))
        a1 = str_to_list(a)
        res = sm3_hash(a1)[:int(front/4)]
        if(T_hash.get(res,'404')=='404'):
            T_hash[res] = a
        else:
            return a,T_hash[res]
        
    
if __name__=="__main__":
    a,b = birth_attack(front)
    c = sm3_hash(str_to_list(a))
    d = sm3_hash(str_to_list(b))
    print(a,b)
    print(c,d)

