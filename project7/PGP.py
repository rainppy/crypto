import sm2
import sm3
import func
from sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
class sender(object):
    def __init__(self, sm2_crypt):
        self.public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
        self.sm2_crypt = sm2_crypt
    def gen_sessionkey(self):
        '''生成sm4会话密钥，用接收方公钥加密之'''
        self.session_key = b'3l5butlj26hvv313'
        enc_sessionkey = self.sm2_crypt.encrypt(self.session_key)
        return enc_sessionkey
    def enc_data(self, data):
        iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(self.session_key, SM4_ENCRYPT)
        encrypt_data = crypt_sm4.crypt_cbc(iv, data)
        return encrypt_data

class receiver(object):
    def __init__(self, sm2_crypt):
        self.private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
        self.sm2_crypt = sm2_crypt
    def get_sessionkey(self, enc_sessionkey):
        dec_sessionkey =sm2_crypt.decrypt(enc_sessionkey)
        self.session_key = dec_sessionkey
    def dec_data(self, enc_data):
        iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(self.session_key, SM4_DECRYPT)
        dec_data = crypt_sm4.crypt_cbc(iv, enc_data)
        return dec_data
        
if __name__ =="__main__":
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)

    #初始化收发对象
    Alice = sender(sm2_crypt)
    Bob = receiver(sm2_crypt)
    
    #PGP过程模拟
    enc_sessionkey = Alice.gen_sessionkey()
    Bob.get_sessionkey(enc_sessionkey)
    data = b'Nice to meet u!'
    print("Alice send",data)
    encrypt_data = Alice.enc_data(data)
    crypt_data = Bob.dec_data(encrypt_data)
    print("Bob receive",crypt_data)
   
