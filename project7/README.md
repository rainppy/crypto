# Project: Implement a PGP scheme with sm2

## 项目代码说明

本项目实现了PGP方案。用面向对象编程的方式还原了交互过程。

**核心代码**为PGP.py

发送方

- 公开渠道获取接收方的sm2公钥`pk`
- 生成会话密钥`sessionkey`，并用`pk`加密，得到`enc_sessionkey`【对应函数gen_sessionkey(self)】
- 用sm4会话密钥`sessionkey`加密消息，得到`enc_data`【对应函数enc_data(self,data)】

![Image text](https://github.com/rainppy/crypto/blob/e517c2cbf1f3538dba4328b47f2633a930b70399/project7/pic/code1.png)

接收方

- 收到`enc_sessionkey`和`enc_data`
- 用私钥解密`enc_sessionkey`得到sm4会话密钥`sessionkey`【对应函数get_sessionkey(self, enc_sessionkey)】
- 用会话密钥`sessionkey`解密`enc_data`，得到明文消息- 【对应函数dec_data(self, enc_data)】



![Image text](https://github.com/rainppy/crypto/blob/e517c2cbf1f3538dba4328b47f2633a930b70399/project7/pic/code2.png)

此外，func.py、sm2.py、sm3.py、sm4.py来自于gmssl包

## 运行指导

运行PGP.py即可

## 代码运行截图

![Image text](https://github.com/rainppy/crypto/blob/e517c2cbf1f3538dba4328b47f2633a930b70399/project7/pic/shoot.png)

利用PGP方案模拟Alice向Bob发送'Nice to meet u!'。Bob经过两次解密得到消息'Nice to meet u!'。

## 贡献说明

项目由张雨欣同学个人独立完成。其中核心代码PGP.py自主完成。func.py、sm2.py、sm3.py、sm4.py来自于gmssl包。
