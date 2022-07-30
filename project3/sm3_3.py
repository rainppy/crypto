

IV = [1937774191, 1226093241, 388252375, 3666478592,2842636476, 372324522, 3817729613, 2969243214,]

T_j = [2043430169]*16+[2055708042]*48

def FF_j(x, y, z, j):
    if 0 <= j and j < 16:
        return x ^ y ^ z
    elif 16 <= j and j < 64:
        return (x & y) | (x & z) | (y & z)    

def GG_j(x, y, z, j):
    if 0 <= j and j < 16:
        return x ^ y ^ z
    elif 16 <= j and j < 64:
        return (x & y) | ((~ x) & z)
def rotl(x,n):
    n = n % 32
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)
def P_0(x):
    return x ^ (rotl(x, 9)) ^ (rotl(x, 17))

def P_1(x):
    return x ^ (rotl(x, 15)) ^ (rotl(x, 23 ))

def Padding(msg):
    length = len(msg)
    msg.append(0x80)
    trunc_length = (length + 1) % 64
    if trunc_length>56:
        pad = 128 - (trunc_length + 8)
    else:
        pad = 64 - (trunc_length + 8)
    for i in range(pad):
        msg.append(0x00)
    length_bit = length * 8
    length_bit_arr = []
    for i in range(8):
        length_bit_arr.append(length_bit % 0x100)
        length_bit = int(length_bit / 0x100)
    #fill in the reverse order
    for m in length_bit_arr[::-1]:
        msg.append(m)
    
    
def CF(Vi, Bi):
    #Step1 Message Extension
    W = []
    
    for i in range(16):
        r = 3
        Wi = 0
        for j in range(i*4,(i+1)*4):
            Wi = Wi + (Bi[j]<<(r*8))
            r-=1
        W.append(Wi)

    for j in range(16, 68):
        W.append( P_1(W[j-16] ^ W[j-9] ^ (rotl(W[j-3], 15 ))) ^ (rotl(W[j-13], 7)) ^ W[j-6])
        #str1 = "%08x" % W[j]
    W1 = []
    for j in range(0, 64):
        W1.append(W[j] ^ W[j+4]) 
        #str1 = "%08x" % W1[j]
    #Step2 Cmpress Fuction
    A, B, C, D, E, F, G, H = Vi

    for j in range(0, 64):
        SS1 = rotl((rotl(A,12) + E + rotl(T_j[j],j))& 0xffffffff,7)#Note: modulus add
        SS2 = SS1 ^ (rotl(A, 12))
        TT1 = (FF_j(A, B, C, j) + D + SS2 + W1[j]) & 0xffffffff
        TT2 = (GG_j(E, F, G, j) + H + SS1 + W[j]) & 0xffffffff
        D = C
        C = rotl(B, 9)
        B = A
        A = TT1
        H = G
        G = rotl(F, 19)
        F = E
        E = P_0(TT2)
        A, B, C, D, E, F, G, H = map(
            lambda x:x & 0xFFFFFFFF ,[A, B, C, D, E, F, G, H])

    v_j = [A, B, C, D, E, F, G, H]
    return [v_j[i] ^ Vi[i] for i in range(8)]

def sm3_hash(msg):
    #Step1 padding
    Padding(msg)
    #Step2 grouping
    BB = []
    for i in range(0, int(len(msg) / 64)):
        BB.append(msg[i*64:(i+1)*64])
    #Step3 Iteration
    V = []
    V.append(IV)
    for i in range(0, int(len(msg) / 64)):
        V.append(CF(V[i], BB[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result
bytes_to_list = lambda data: [i for i in data]
if __name__ == '__main__':
    y = sm3_hash(bytes_to_list(b"abcd"*16))
    print(y)
