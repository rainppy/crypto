# Project: report on the application of this deduce technique in Ethereum with ECDSA

## 项目介绍及原理

### 项目应用

该技术是通过签名值恢复出公钥，从而降低了存储公钥的空间开销。在比特币中，是通过删去tx中的公钥字段，降低了开销。在以太坊中，

### 原理

- $s=k^{-1}(e+dr)$
- $ks=(e+dr)$
- $P=dG=(s(kG)-eG)·r^{-1}$
- 其中$kG$的计算方法是：
  - $(k G)_{x}=x_{1}=r \bmod n$
  - 将$x1$带入椭圆曲线，计算得$y_1$

## 项目代码说明

- func.py 实现底层函数，如求模逆，勒让德符号，求模平方根等
- deduce_key.py  **核心函数**，实现ECDSA的由签名推测公钥的算法，并实例化测试

## 项目运行

运行代码deduce_key.py即可，如果没有下载包ecdsa，则需用以下命令下载安装。

```python
pip install ecdsa
```

## 运行截图

![Image text](https://github.com/rainppy/crypto/blob/7234d8779d7cd55db915cb6bfe8979d2fcb7c577/project6/pic/shoot.png)

## 贡献说明

本项目为张雨欣独立完成
