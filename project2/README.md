# Project2: implement length extension attack for SM3

## 项目简介

本项目实现了长度扩展攻击

### 问题场景

早期人们利用哈希函数构造消息验证码的方法是，将密钥$k$和消息直接并联后计算哈希值，即$\text{Mac}_k(m)=H(k||m)$。但是这一签名方案并不是安全的，我们可以利用哈希长度扩展攻击，在未知签名密钥$k$的情况下，构造合法的签名伪造。

在本项目我将上述攻击实例化到MD结构的哈希函数`sm3`上，完成上述的攻击。

## 项目代码说明

- sm3_2.py 依照官方文档实现了sm3算法
- attack.py 实现了长度扩展攻击

### 代码思想

敌手获得消息$m'=Best wishes!$的签名$s'$，试图在不知道密钥$k$的情况下，在消息后附加任意拓展的消息，伪造它的签名值。

#### 敌手攻击

首先，敌手模拟SM3的消息填充过程，将$m'$进行填充至512bit的倍数。计算此时的字节长度$len'$。将$m'$后追加攻击字符串"attack!"，对整个字符串进行SM3的消息填充（消息长度为$len('attack!')+len'$）。如有必要，对消息进行分组。

然后，将收到的哈希$s'$作为“IV”，对消息进行哈希。即可伪造出追加消息后的哈希值（签名值）。

#### 验签

check_res(extend_msg,hash_res)函数

该函数模仿了拥有私钥的一方，验证签名的过程。作为本实验正确性的检验。

## 项目运行截图

![Image text](https://github.com/rainppy/crypto/blob/8c2a1a6893dfffda527a4bc1a4ff0248e91b9e59/project2/pic/shoot.png)

长度扩展攻击，得到的消息及其哈希值。那么就实现了在未知secretkey的情况下，伪造了签名。

## 贡献说明

本项目由张雨欣独立完成。
