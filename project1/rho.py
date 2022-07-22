from sm3 import sm3_hash
import random
import string


front = 32
str_to_list = lambda data: [i for i in bytes(data,encoding="ascii")]

def print_bytes(x,y):
    x_p = ""
    for i in x:
        x_p = '%s%02x' % (x_p, i)
    print(x_p)
    x_p = ""
    for i in y:
        x_p = '%s%02x' % (x_p, i)
    print(x_p)     
def rho(front):
    x0 = ''.join(random.sample(string.ascii_letters + string.digits, 30))
    x0 = str_to_list(x0)
    x1 = x0[:]
    x = x0[:]
    i = 1 
    while 1:
        x = sm3_hash(x)
        x1 = sm3_hash(sm3_hash(x1))
        if x[:int(front/8)]==x1[:int(front/8)]:
            break
        i+=1    
    x1 = x[:]
    x = x0[:]
    for j in range(i-1):
        x = sm3_hash(x)
        x1 = sm3_hash(x1)
    return x,x1
        
if __name__=="__main__":
    a,b = rho(front)
    c = sm3_hash(a[:])
    d = sm3_hash(b[:])
    print_bytes(a,b)
    print_bytes(c,d)

            
        
    
    