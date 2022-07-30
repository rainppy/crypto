# verify the above pitfalls with proof-of-concept code

## 项目简介

本项目实现了表格中ECDSA算法的7种漏洞攻击。下面是具体攻击方法的说明。

### 1. Leaking k leads to leaking of d

假设敌手获得消息m的签名(r,s)，并且该签名使用的k泄漏了。可以利用以下公式求解出私钥d。

$d = r^{-1}(ks-H(m))$

### 2. Reusing k leads to leaking of d

假设同一签名者签署消息$m_1$、$m_2$时重复使用了$k$，那么求得的$r$也相同，设签名分别为$(r,s_1)$,$(r,s_2)$。

- $s_1=k^{-1}(e_1+dr)$,  $s_2=k^{-1}(e_2+dr)$
  - 作商，$d = (s_2e_1-s_1e_2)/(s_1r-s_2r)$

### 3.Two users, using k leads to leaking of  d

假设Alice用私钥$d_A、k$签署消息$m_1$,得到$(r_1,s_1)$;Bob用私钥$d_B、k$签署消息$m_2$,得到$(r_2,s_2)$

- Alice可以计算出Bob的私钥$d_B$
  - $s_1=k^{-1}(e_1+d_Ar)$,  $s_2=k^{-1}(e_2+d_Br)$
  - 作商，得到$d_B=(s_2e_1 + s_2d_Ar-e_2s_1)/(rs_1)$
- 同理，Bob也可以计算出Alice的私钥

### 4.Malleability

当敌手获得消息m的一个合法签名$(r,s)$后，可以伪造该消息的另一个合法签名$(r,-s)$，即攻破了改签名算法的强存在不可伪造性。验签$(r,-s)$如下：

$(-s)^{-1}(eG+rP)=-s^{-1}(eG+rP)=-k(e+dr)^{-1}(e+dr)G=-kG=-R=(R_x,-R_y)$

$R_x==r$验签通过

### 思考

1. 该攻击之所以可以成功是因为验签时只验了$R$的横坐标。在椭圆曲线群上又满足以下等式

$$
eG=(x,y)\\
(n-e)G=(x,p-y)
$$

2. 对于一个消息存在着两种合法的签名。敌手构造出一个transaction的多个副本，都是可以解码成功（验签通过）的，发给不同的矿工每矿工的视角不同，产生分歧，会导致网络分裂

### 5. Ambiguity of DER encode could lead to blockchain network split

- 正确的DER编码方式
  - 0x30 [total-length] 0x02 [R-length] [R] 0x02 [S-length] [S] [sighash-type]
  - R 值: 不能以任何 0x00 字节开始，除非后面的第一个字节是 0x80 或更高
- 不安全的编码方式：DER变体，如R值前加0x00字节，也可能通过验证
  - 不安全的原因：对于同一$(r,s)$可以有多种编码方式，对应多种签名值的二进制流，导致TX不同，进而导致hash值的共识打破，导致网络分裂。

该部分代码是实现了将ECDSA签名值进行正确的编码。

### 6.One can forge signature if the verification does not check m

> 如果验签的时候不要求提供消息m，只提供H(m)。只要事先知道某人的一个签名，则可以冒充他签名。

验签：$s^{-1}(e G+r P)=\left(x^{\prime}, y^{\prime}\right)=R^{\prime}, r^{\prime}=x^{\prime} \bmod n==r$

攻击：

- 选择$u,v\in\mathbb{F}_n^*$
- 计算$R'=(x',y')=uG+vP$
- 令$r^{\prime}=x^{\prime} \bmod n$ 
- 为了通过验签，有$s'^{-1}(e' G+r' P)=uG+vP$
  - $s^{\prime-1} e^{\prime}=u \bmod n \rightarrow e^{\prime}=r^{\prime} u v^{-1} \bmod n$
  - $s^{\prime-1} r^{\prime}=v \bmod n \rightarrow s^{\prime}=r^{\prime} v^{-1} \bmod n$
- $\sigma'=(r',s')$是某人对$e'$的签名

### 7. Same d and k in sm2 & ECDSA, leads to leaking of d

- ECDSA方案用私钥$d$签名
  - 随机选择$k$, $R = kG=(x,y)$
  - $e_1=hash(m)$
  - $r_{1}=x \bmod n, s_{1}=\left(e_{1}+r_{1} d\right) k^{-1} \bmod n$
  - 得到签名$r_2,s_2$
- SM2方案也用私钥$d$签名
  - 重用与ECDSA相同的$k$，$kG=(x,y)$
  - $e_{2}=h\left(Z_{A} \| m\right)$
  - $r_{2}=\left(e_{2}+x\right) \bmod n$
  - $s_{2}=(1+d)^{-1} \cdot\left(k-r_{2} d\right) \bmod n$
  - 得到签名$(r_2,s_2)$
- 利用上述两个签名，可以恢复出私钥$d$
  - $d \cdot r_{1}=k s_{1}-e_{1} \bmod n$
  - $d \cdot\left(s_{2}+r_{2}\right)=k-s_{2} \bmod n$
  - 消掉$k$，$d=\frac{s_{1} s_{2}-e_{1}}{\left(r_{1}-s_{1} s_{2}-s_{1} r_{2}\right)} \bmod n$

#### 思考

SM2官方文档中提供的椭圆曲线推荐参数与NIST等的标准不同，进而$n$不同，若使用推荐参数则规避了此类攻击

## 项目代码说明

项目实现了ECDSA签名的7种攻击。

- pitfalls.py 项目的**核心代码**，实例化攻击
- func.py 项目调用的基础函数
- sm2.py sm2实现，在project4的sm2.py文件基础上稍作修改
- myecdsa.py 自主实现ECDSA算法。在第七种攻击时调用，前6种攻击调用ecdsa-python包中的实现

pitfalls.py中，

![Image text](https://github.com/rainppy/crypto/blob/6e1c8330ae9b3e80dbcaf7de23b59322549ccbc6/project5/picture/1.png)

七个函数对应实现了七种攻击（其中问题5为实现DER编码）

main函数部分则是对攻击进行测试。

![Image text](https://github.com/rainppy/crypto/blob/6e1c8330ae9b3e80dbcaf7de23b59322549ccbc6/project5/picture/2.png)

## 运行指导

若无安装ecdsa库，则需用`pip install ecdsa`安装此库。

运行`pitfalls.py`即可。

## 代码运行截图

![Image text](https://github.com/rainppy/crypto/blob/6e1c8330ae9b3e80dbcaf7de23b59322549ccbc6/project5/picture/shoot.png)

验证7种攻击均成功！（伪造签名或者恢复私钥）其中问题5实现了DER编码方案。
## 贡献说明

项目由张雨欣同学个人独立完成。

**核心代码**pitfalls.py 、func.py为独立完成

sm2.py在project4的文件上稍作修改，来自gmssl库

myecdsa.py 是在gmssl的sm2实现上经过修改实现的

















