import sm3_2

bytes_to_list = lambda data: [i for i in data]
def check_res(extend_msg,hash_res):
    B0 = bytes_to_list(b"secretkeyBest wishes!")
    sm3_2.Padding(B0)
    Bi = bytes_to_list(bytes(extend_msg,encoding="ascii"))
    B0.extend(Bi)
    if(sm3_2.sm3_hash(B0)==hash_res):
        print("success!")
    else:
        print("fail!")
    
 
    
if __name__ == '__main__':
    origin_msg = "secretkeyBest wishes!"
    Vi = sm3_2.sm3_hash(bytes_to_list(bytes(origin_msg,encoding="ascii")))
    extend_msg = "Attack!"
    Bi = bytes_to_list(bytes(extend_msg,encoding="ascii"))
    length = len(Bi) + 64
    Bi.append(0x80)
    trunc_length = (length + 1) % 64
    if trunc_length>56:
        pad = 128 - (trunc_length + 8)
    else:
        pad = 64 - (trunc_length + 8)
    for i in range(pad):
        Bi.append(0x00)
    length_bit = length*8
    length_bit_arr = []
    for i in range(8):
        length_bit_arr.append(length_bit % 0x100)
        length_bit = int(length_bit / 0x100)
    #fill in the reverse order
    for m in length_bit_arr[::-1]:
        Bi.append(m)
    hash_res = sm3_2.CF(Vi, Bi)
    result=""
    for i in hash_res:
        result = '%s%08x' % (result, i)
    print("Hash is {}".format(result))
    #When person who has secretkey to check
    check_res(extend_msg,hash_res)
