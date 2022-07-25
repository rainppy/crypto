import hmac
import hashlib
from binascii import hexlify
def bits2int(b,qlen):
    rshift = len(b) * 8 - qlen
    b = int(hexlify(b), 16)
    if rshift > 0:
        return b >> rshift
    else:
        return b
def generate_k(n, private_key, data, extra_entropy=b""):
    hlen = 256
    qlen = len(n) * 4
    #a. Process m through the hash function H, yielding:
    h1 = hashlib.sha256(data).digest()
    
    #b. Set V
    V = b"\x01" * hlen
    
    #c. Set K
    K = b"\x00" * hlen
    
    #d. Updata K
    K = hmac.new(K, digestmod='sha256')
    K.update(V + b"\x00")
    K.update(bytes.fromhex(private_key))
    K.update(h1)
    K.update(extra_entropy)
    K = K.digest()
    
    #e. Update V
    V = hmac.new(K, V, 'sha256').digest()

    #f. Update K
    K = hmac.new(K, digestmod='sha256')
    K.update(V + b"\x01") #0x01 this time
    K.update(bytes.fromhex(private_key))
    K.update(h1)
    K.update(extra_entropy)
    K = K.digest()

    #g. Update V
    V = hmac.new(K, V, 'sha256').digest()

    #h. Apply the following algorithm until a proper value is found for k:
    while 1:
        T = b""
        while len(T) < qlen:
            V = hmac.new(K, V, 'sha256').digest()
            T += V
        k = bits2int(T, qlen)
        n_int = int(n,16)
        if 1 <= k < n_int:
            return k
        K = hmac.new(K, V + b"\x00", 'sha256').digest()
        V = hmac.new(K, V, 'sha256').digest()