
账户名称：rainppy

个人完成
# 完成项目及简介
## Project1: implemen rho method of reduced SM3
Pollard's rho算法是一种寻找生日攻击的算法。该算法的优势是将空间复杂度降低到$O(1)$。本项目中，我用C、python实现了两个版本，进行测试，找到了32bit的碰撞。
## Project2: implement length extension attack for SM3
MD结构的哈希函数存在长度扩展攻击漏洞。本项目借以此攻击，以攻击利用哈希函数构造消息验证码的方案，获得合法伪造。在项目中，我查阅sm3官方文档，对sm3进行实现，而后实现长度扩展攻击。
## Project3: implement the naïve birthday attack of reduced SM3
该方法利用以空间换时间的策略，实现生日攻击。我实现了python和c版本。python版利用其内置的字典数据结构加快查找速度，C版则用C++11标准中的unordered_map。由于unordered_map重载实现起来略显复杂，在项目截止时仍未调试成功。最多找到了40bit碰撞，大约耗时20分钟。
## Project4: implement sm2 with RFC6979
由于ECDSA方案因代码实现时随机源质量不高屡次出现问题(如项目5中的攻击)，RFC6979文档定义了确定性数字签名生成过程。本实验我依据该文档，实现了sm2中的随机数k生成算法。
## Project5: verify the above pitfalls with proof-of-concept code
本项目实现了表格中ECDSA算法的7种漏洞攻击。攻击的具体原理及代码参见文件夹project5。
## Project6: report on the application of this deduce technique in Ethereum with ECDSA
该技术是通过签名值恢复出公钥，从而降低了tx的空间开销。在比特币中，省去tx中的`publickey`字段。在以太坊中，则省去了`from`字段（20bytes）和公钥（33bytes），只需要`v,r,s`字段，从签名`r,s`中恢复出公钥来，然后对公钥做哈希得到`from`地址。

本项目实现了这一由签名恢复公钥的代码。
## Project7: Implement a PGP scheme with sm2
本项目实现了PGP方案。该方案用公钥密码加密会话密钥，再用对称密码加密数据。兼顾了公钥密码的安全性和对称密码的高效性。
## Project8: forge a signature to pretend that you are Satoshi
如果验签的时候不要求提供消息m，只提供H(m)。只要事先知道中本聪的一个签名，则可以冒充他签名。本实验就实现了这一过程。
## Project9: research report on MPT
阅读ethereum的Merkle-patricia-tree (trie) 代码实现并撰写代码解析。
# 清单
## 已完成项目：

|      | 名称                                                         | 文件夹   |
| ---- | ------------------------------------------------------------ | -------- |
| 1    | Implement the naïve birthday attack of reduced SM3           | project3 |
| 2    | Implemen rho method of reduced SM3                           | project1 |
| 3    | Implement length extension attack for SM3, SHA256, etc       | project2 |
| 4    | Report on the application of this deduce technique in Ethereum with ECDSA | project6 |
| 5    | Impl sm2 with RFC6979                                        | project4 |
| 6    | Verify the above pitfalls with proof-of-concept code         | project5 |
| 7    | Implement a PGP scheme with SM2                              | project7 |
| 8    | Forge a signature to pretend that you are Satoshi            | project8 |
| 9    | Research report on MPT                                       | project9 |

## 未完成项目：

|      | 名称                                                         |
| ---- | ------------------------------------------------------------ |
| 1    | Do your best to optimize SM3 implementation (software)       |
| 2    | Impl Merkle Tree following RFC6962                           |
| 3    | Do your best to optimize SM4 implementation (software)       |
| 4    | Implement the above ECMH scheme                              |
| 5    | Implement sm2 2P sign with real network communication        |
| 6    | Implement sm2 2P decrypt with real network communication     |
| 7    | Send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself |
| 8    | PoC impl of the scheme, or do implement analysis by Google   |
| 9    | Find a key with hash value `sdu_cst_20220610` under a message composed of your name followed by your student ID. For example, `San Zhan 202000460001` |
| 10   | Find a 64-byte message under some k fulfilling that their hash value is symmetrical |
| 11   | Write a circuit to prove that your CET6 grade is larger than 425.（a. Your grade info is like `(cn_id, grade, year, sig_by_moe)`. These grades are published as commitments onchain by MoE. b. When you got an interview from an employer, you can prove to them that you have passed the exam without letting them know the exact grade.） |

## 有问题的项目：Implemen rho method of reduced SM3 
问题：rho算法似乎不适用于截断的生日攻击

做完本项目（implemen rho method of reduced SM3 ）后，我完成implement the naïve birthday attack of reduced SM3时惊奇地发现，naive的方法竟然比rho算法效率还高很多。经过多日的思考，我得到的原因是Pollard Rho算法并不适用于截断前n bit找碰撞的问题，它只适用于整个哈希值找碰撞的问题。

我认为rho算法之所以奏效，是因为存在循环。对整个哈希寻找碰撞的情形，若出现一次碰撞，假设它们哈希次数相差i，那么此后所有哈希次数相差i的都会发生碰撞，进入周期为i的循环。但是问题迁移到前截断前nbit，却不能再成立，就不会存在循环了，此时采用rho算法虽然可以得到解，但是却没有计算复杂度的优势了。
