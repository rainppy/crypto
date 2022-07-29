# Project: report on the application of this deduce technique in Ethereum with ECDSA

## 项目介绍及原理

### 项目应用

该技术是通过签名值恢复出公钥，从而降低了tx的空间开销。在比特币中，省去tx中的`publickey`字段。在以太坊中，则省去了`from`字段（20bytes）和公钥（33bytes），只需要`v,r,s`字段，从签名`r,s`中恢复出公钥来，然后对公钥做哈希得到`from`地址。

由于一个签名映射到2把可能的公钥，所以引入前缀`v`字段加以区分。当`v`是偶数时，“正平方根”求出的$kG$的公钥$P$；当`v`是奇数时，$kG$则是与前者关于x轴对称的点。在下面的原理介绍中可以看出，因为`r`值等于椭圆曲线上点$kG$的横坐标，可以求出两个椭圆曲线上的点，进而求出两种可能的公钥值。

### 原理

- $s=k^{-1}(e+dr)$
- $ks=(e+dr)$
- $P=dG=(s(kG)-eG)·r^{-1}$
- 其中$kG$的计算方法是：
  - $(k G)_x=x_1=r \bmod n$
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

输出由签名推出的公钥和真实的公钥。经比对相同。
## 贡献说明

本项目为张雨欣独立完成
