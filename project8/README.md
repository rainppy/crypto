# Project: forge a signature to pretend that you are Satoshi

## 项目背景及原理

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

## 项目代码说明

- satoshi.py 项目的核心代码，伪造satoshi的签名
  - blockchain.com上未能显示sig script字段
  - 因此，随机生成一个签名来模拟攻击

![Image text]([.\blockchain.png](https://github.com/rainppy/crypto/blob/1a88780d7ff7cf253daee2d1bd135effb9f6422e/project8/pic/blockchain.png))

## 运行指导

若无安装ecdsa库，则需先用`pip install ecdsa`安装此库。

运行`satoshi.py`即可。

## 代码运行截图

![Image text](https://github.com/rainppy/crypto/blob/1a88780d7ff7cf253daee2d1bd135effb9f6422e/project8/pic/shoot.png)

## 贡献说明

项目由张雨欣同学个人独立完成。
