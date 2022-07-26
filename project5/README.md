# verify the above pitfalls with proof-of-concept code

## 项目代码说明

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

2. 对于一个消息存在着两种合法的签名，每矿工的视角不同，产生分歧，会导致网络分裂

### 5. Ambiguity of DER encode could lead to blockchain network split

- 正确的DER编码方式
  - 0x30 [total-length] 0x02 [R-length] [R] 0x02 [S-length] [S] [sighash-type]
  - R 值: 不能以任何 0x00 字节开始，除非后面的第一个字节是 0x80 或更高
- 不安全的编码方式：DER变体，如R值前加0x00字节，也可能通过验证
  - 不安全的原因：对于同一$(r,s)$可以有多种编码方式，对应多种二进制流，导致hash值得共识打破，导致网络分裂。

该部分不宜用代码说明，故理论分析之。

### 6.

如果验签的时候不要求提供消息m，只提供H(m)。实现知道他的一个签名，则可以冒充中本聪

## 运行指导

现在









