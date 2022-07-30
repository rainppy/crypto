# implement rho method of reduced SM3

## 项目代码简介

### Pollard's rho算法

#### 算法原始伪代码

![Image text](https://github.com/rainppy/crypto/blob/f4e22d5cd373a124db4ecadbced430c7a97273e4/project1/pic/alg_origin.png)

- 算法前半部分——寻找hash的循环周期

$x=x_i=H^{(i)}(x_0)$     $x'=x_{2i}=H^{(2i)}(x_0)$

遍历$i=1,2,3,...$测试$x$和$x'$是否相等 

发生碰撞时，相差的下标$i$可以度量循环周期

- 寻找首次进入循环的位置

假设$x_{j-1}\ne x_{j+i-1}$ ,但$x_j=x_{j+i}$。那么$x_{k}=x_{k+i}\ \ \  k\ge j$

我们需要找到首次进入循环的位置，输出原象$x_{j-1}$和$ x_{j+i-1}$,即为一对碰撞。

注：$x_{k}$与$x_{k+i}\ \ \  k\ge j$不算作一对碰撞，因为它们本身就相等，hash后自然也相等。必须要找**首次**碰撞发生的位置

**Pollard Rho算法并不适用于截断前n bit找碰撞的问题，它适用于整个哈希值找碰撞的问题**

若$H^{(i)}(x_0)=H^{(i+k)}(x_0)$，则$H^{(i+m)}(x_0)=H^{(m)}(H^{(i)}(x_0))=H^{(m)}(H^{(i+k)}(x_0))=H^{(i+k+m)}(x_0)$

#### 修正版代码（用于截断前n bit的简化版）

![Image text](https://github.com/rainppy/crypto/blob/f4e22d5cd373a124db4ecadbced430c7a97273e4/project1/pic/alg_adjust.png)

- 算法前半部分——寻找hash的循环周期

该部分保持不变

- 找到$H^{(i-1)}$和$H^{(2i-1)}$即可
  - 由于是截断差分，不存在“循环”

#### ==项目存疑及解释==

​        做完本项目（implemen rho method of reduced SM3 ）后，我完成implement the naïve birthday attack of reduced SM3时惊奇地发现，naive的方法竟然比rho算法效率还高很多。经过多日的思考，我得到的原因是Pollard Rho算法并不适用于截断前n bit找碰撞的问题，它只适用于整个哈希值找碰撞的问题。

​        我认为rho算法之所以奏效，是因为存在循环。对整个哈希寻找碰撞的情形，若出现一次碰撞，假设它们哈希次数相差i，那么此后所有哈希次数相差i的都会发生碰撞，进入周期为i的循环。但是问题迁移到前截断前nbit，却不能再成立，就不会存在循环了，此时采用rho算法虽然可以得到解，但是却没有计算复杂度的优势了。

## 项目代码说明

本项目我实现了C++和python两个版本。

python版：

- sm3_1.py 自主实现了sm3算法
- rho.py实现了

C版：

调用了openssl库

- makefile
- project1.c

## 运行指导

C版：

- 运行make
- 代码第6行SIZE 代表截断前SIZE字节

python版：

- 运行rho.py
- 代码第6行front字段代表截断前front比特，老师可以将其调为更小的数值测试。（需要为4的倍数）

## 运行代码截图

![Image text](https://github.com/rainppy/crypto/blob/f4e22d5cd373a124db4ecadbced430c7a97273e4/project1/pic/shoot1.png)

python版运行截图，前16bit碰撞

![Image text](https://github.com/rainppy/crypto/blob/f4e22d5cd373a124db4ecadbced430c7a97273e4/project1/pic/shoot2.png)

C版运行截图，前32bit碰撞

### 测试结果

#### 16bit

```python
a = 91fca6c3e6c416a478fbd22737bf2d385270f1a90d39f38a68f01f135668063f
b = 079585525896b8b8dcaa7675be4950a18a0aa7fd2fc38623df07f9a4066c714e
Hash(a) = 9c2419e994b4f65a0ad311240936461058a5f1a5354686004123305d67256334
Hash(b) = 9c24cea530d5bce3ce4a9667eca51ebea9fdbd529f02c47542c1f4996833f17b
```

#### 24bit

```python
a = 97629be16292ebcf5aecd14c66cb7ecfd5e857b4258f4a24a450d1721530bfb5
b = f3fba5b89ef743edcf831c48d56ce54220e3b02439158dc78ab133ce2d6f6186
Hash(a) = ec03ec0a756212e618bca8039c51bcec063fa4ee3e0bf36501f8a42d9b4dd9ab
Hash(b) = ec03ecb1116ab0f96b6cb024fc340e4237b50a769d787e9a46801300b0815788
```

#### 32bit

```python
a = 14152cf63f4cbe7faf512e9406caa3ed86377a311d0773b8ba50c2e131c5143f
b = 435e8b7f8f9ff395556f44156629f71b89832830689c5b5b473fb5debb118265
Hash(a) = 88cadb5fcfd90e151b12dd77bac8ff7c2cf01a490d20fe0d8409075e7acebad3
Hash(b) = 88cadb5fd7b48dba172d2eaf31bde9a7d0527d6f00f723ee859e1ee1a29cdccf
```



## 贡献说明 

本项目由张雨欣独立完成。


