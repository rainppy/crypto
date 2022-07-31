# Project: research report on MPT

## 项目简介

​         阅读ethereum的Merkle-patricia-tree (trie) 代码实现并理解。

## 正文

### 数据结构

以太坊区块头部的一个字段是交易的根哈希。而这便是MPT的根哈希。Merkle-patricia-tree (trie)的作用就是验证一系列交易的合法性。

和比特币中的Merkle tree相似，MPT也是一棵哈希树。不同的是，它还是一棵patricia-tree。叶节点的哈希值（地址）确定了它在树中的唯一路径。

以太坊的实现引入了许多改进。 

1. 为了使MPT在密码学意义上安全，每个节点都由其哈希索引（在kv数据库 leveldb 中查找）。 通过该方案，根节点成为整个数据结构的“指纹”。 
2. 引入了许多节点“类型”以提高效率。 
   - 空白节点
   - 叶节点   [key, value] 列表
   - 扩展节点   [key, value] 列表由共同前缀和指向下一个节点的指针构成
   - 分支节点   长度为 17 的列表。前 16 个元素对应于键中的 16 个可能的十六进制字符。若从根到此处恰好是一个完整的key值，则最后一个元素保存value。

```python
(
    NODE_TYPE_BLANK,
    NODE_TYPE_LEAF,
    NODE_TYPE_EXTENSION,
    NODE_TYPE_BRANCH
) = tuple(range(4))
```

在代码中用2bit编码区分。

### 编码

一种特殊的十六进制前缀编码。

- 标准叶节点和扩展节点都是[key,value]列表，但value值的含义不同，故引入TERMINATOR加以区分
  - TERMINATOR=1  叶节点，对应value为交易的值，如1Wei。
  - TERMINATOR=0  中间节点，用于查找在数据库中查找下一个节点rlp编码的hash。
- 增加一位表示key的奇偶性

一个半字节的nibble加到key前，对TERMINATOR和奇偶性进行编码。最低位是奇偶校验位，倒数第二低位编码终止符状态。

- key采用十六进制编码

```python
def pack_nibbles(nibbles):
    """pack nibbles to binary

    :param nibbles: a nibbles sequence. may have a terminator
    """

    if nibbles[-1:] == [NIBBLE_TERMINATOR]:
        flags = 2
        nibbles = nibbles[:-1]
    else:
        flags = 0

    oddlen = len(nibbles) % 2
    flags |= oddlen   # set lowest bit if odd number of nibbles
    if oddlen:
        nibbles = [flags] + nibbles
    else:
        nibbles = [flags, 0] + nibbles
    o = ''
    for i in range(0, len(nibbles), 2):
        o += chr(16 * nibbles[i] + nibbles[i + 1])
    return o
```

### 节点与数据库

当产生新节点时，节点哈希和其数据会以键值对的形式存在leveldb数据库中。

![Image text](https://github.com/rainppy/crypto/blob/57c01e2b7c791a206c08fdae08f178359aa86fa9/project9/hash_node.png)

当获取节点时，通过在用哈希值查找数据库获得。如上图，先获得根哈希，然后查找数据库，获得该节点。若查找中间节点，要转跳下一个节点时，value存储的即为下一个节点的哈希值，便可以查找数据库，进行获取。

### 函数方法

#### get

- 若为空节点，直接返回BLANK_NODE
- 若为分支节点
  - key为空，直接返回value
  - 否则，递归查找value对应的节点
- 若为叶节点
  - 如果key相符，返回value
  - 否则返回BLANK_NODE
- 若为扩展节点
  - 如果key相符，递归查找value对应的节点
  - 否则返回BLANK_NODE

```python
    def _get(self, node, key):
        """ get value inside a node

        :param node: node in form of list, or BLANK_NODE
        :param key: nibble list without terminator
        :return:
            BLANK_NODE if does not exist, otherwise value or hash
        """
        node_type = self._get_node_type(node)
        if node_type == NODE_TYPE_BLANK:
            return BLANK_NODE

        if node_type == NODE_TYPE_BRANCH:
            # already reach the expected node
            if not key:
                return node[-1]
            sub_node = self._decode_to_node(node[key[0]])
            return self._get(sub_node, key[1:])

        # key value node
        curr_key = without_terminator(unpack_to_nibbles(node[0]))
        if node_type == NODE_TYPE_LEAF:
            return node[1] if key == curr_key else BLANK_NODE

        if node_type == NODE_TYPE_EXTENSION:
            # traverse child nodes
            if starts_with(key, curr_key):
                sub_node = self._decode_to_node(node[1])
                return self._get(sub_node, key[len(curr_key):])
            else:
                return BLANK_NODE
```

#### 存在性证明与不存在性证明

借助get方法，从根节点开始，周游address对应路径。若最后返回value，则证明节点存在；若返回BLANK_NODE，则证明节点不存在。

#### update

_update

- 若原节点是空节点，则直接对其赋值k,v，变成一个叶子节点。
- 若原节点是分支节点
  - 若key为空，则直接赋值value
  - 若key不为空，选择对应的槽，递归的更新对应key的节点
- 若原节点是kv节点（叶子节点/扩展节点）
  - 若前缀匹配，则直接修改value/递归向下修改
  - 若前缀不匹配，则分叉。构建新的分支节点，将原kv节点和新节点链接在新的分支节点之下。
  - 具体代码解释见后文_update_kv_node

```python
def _update(self, node, key, value):
    """ update item inside a node

    :param node: node in form of list, or BLANK_NODE
    :param key: nibble list without terminator
        .. note:: key may be []
    :param value: value string
    :return: new node

    if this node is changed to a new node, it's parent will take the
    responsibility to *store* the new node storage, and delete the old
    node storage
    """
    assert value != BLANK_NODE
    node_type = self._get_node_type(node)

    if node_type == NODE_TYPE_BLANK:
        if PRINT: print ('blank')
        return [pack_nibbles(with_terminator(key)), value]

    elif node_type == NODE_TYPE_BRANCH:
        if PRINT: print 'branch'
        if not key:
            if PRINT: print '\tdone', node
            node[-1] = value
            if PRINT: print '\t', node

        else:
            if PRINT: print 'recursive branch'
            if PRINT: print '\t', node, key, value
            new_node = self._update_and_delete_storage(
                self._decode_to_node(node[key[0]]),
                key[1:], value)
            if PRINT: print '\t', new_node
            node[key[0]] = self._encode_node(new_node)
            if PRINT: print '\t', node
        return node

    elif is_key_value_type(node_type):
        if PRINT: print 'kv'
        return self._update_kv_node(node, key, value)
```

_update_kv_node

curr_key是原节点的key，key代表待插入节点的key。首先，寻找它们的最长公共前缀prefix。而余下的部分记为remain_key和remain_curr_key。

```python
    node_type = self._get_node_type(node)
    curr_key = without_terminator(unpack_to_nibbles(node[0]))
    is_inner = node_type == NODE_TYPE_EXTENSION
    if PRINT: print 'this node is an extension node?',  is_inner
    if PRINT: print 'cur key, next key', curr_key, key

    # find longest common prefix
    prefix_length = 0
    for i in range(min(len(curr_key), len(key))):
        if key[i] != curr_key[i]:
            break
        prefix_length = i + 1

    remain_key = key[prefix_length:]
    remain_curr_key = curr_key[prefix_length:]

    if PRINT: print 'remain keys..'
    if PRINT: print prefix_length, remain_key, remain_curr_key
```

- 若remain_key == [] == remain_curr_key，
  - 若节点为叶子节点，直接更新该节点的value。
  - 若为扩展节点，则递归更新子节点

```python
    if remain_key == [] == remain_curr_key:
        if PRINT: print 'keys were same', node[0], key
        if not is_inner:
            if PRINT: print 'not an extension node'
            return [node[0], value]
        if PRINT: print 'yes an extension node!'
        new_node = self._update_and_delete_storage(
            self._decode_to_node(node[1]), remain_key, value)
```

- 若remain_curr_key == []
  - 若为扩展节点，则递归更新子节点
  - 若为叶子节点，则新建一个分支节点。将value值填入value字段。并将原叶子节点链接为该分支节点的子节点。

```python
    elif remain_curr_key == []:
        if PRINT: print 'old key exhausted'
        if is_inner:
            if PRINT: print '\t is extension', self._decode_to_node(node[1])
            new_node = self._update_and_delete_storage(
                self._decode_to_node(node[1]), remain_key, value)
        else:
            if PRINT: print '\tnew branch'
            new_node = [BLANK_NODE] * 17
            new_node[-1] = node[1]
            new_node[remain_key[0]] = self._encode_node([
                pack_nibbles(with_terminator(remain_key[1:])),
                value
            ])
        if PRINT: print new_node
```

- 否则，创建分支节点。
  - 若remain_curr_key长度为1并且原节点是扩展节点，将新节点链接到对应槽位
  - 否则，用remain_curr_key第一比特选择槽位，剩余比特构建新节点。
  - 若remain_key == []，直接将value填入分支节点
  - 否则，用remain_curr_key第一比特选择槽位，剩余比特构建新节点。



```python
    else:
        if PRINT:  print 'making a branch'
        new_node = [BLANK_NODE] * 17
        if len(remain_curr_key) == 1 and is_inner:
            if PRINT: print 'key done and is inner'
            new_node[remain_curr_key[0]] = node[1]
        else:
            if PRINT: print 'key not done or not inner', node, key, value
            if PRINT: print remain_curr_key
            new_node[remain_curr_key[0]] = self._encode_node([
                pack_nibbles(
                    adapt_terminator(remain_curr_key[1:], not is_inner)
                ),
                node[1]
            ])

        if remain_key == []:
            new_node[-1] = value
        else:
            new_node[remain_key[0]] = self._encode_node([
                pack_nibbles(with_terminator(remain_key[1:])), value
            ])
        if PRINT: print new_node
```

#### del

_delete

```python
def _delete(self, node, key):
    node_type = self._get_node_type(node)
    if node_type == NODE_TYPE_BLANK:
        return BLANK_NODE

    if node_type == NODE_TYPE_BRANCH:
        return self._delete_branch_node(node, key)

    if is_key_value_type(node_type):
        return self._delete_kv_node(node, key)
```

- 若删除节点为空节点，返回NODE_TYPE_BLANK
- 若删除节点为分支节点，调用`_delete_branch_node`
- 若删除节点为叶子节点/扩展节点，调用`_delete_kv_node`

 _delete_branch_node 删除分支节点

- 若key为空，直接设为BLANK_NODE，返回正则化结果
- 若key不为空，递归删除子节点，返回新节点

```python
def _delete_branch_node(self, node, key):
    # already reach the expected node
    if not key:
        node[-1] = BLANK_NODE
        return self._normalize_branch_node(node)

    encoded_new_sub_node = self._encode_node(
        self._delete_and_delete_storage(
            self._decode_to_node(node[key[0]]), key[1:])
    )

    if encoded_new_sub_node == node[key[0]]:
        return node

    node[key[0]] = encoded_new_sub_node
    if encoded_new_sub_node == BLANK_NODE:
        return self._normalize_branch_node(node)

    return node
```

_delete_kv_node  删除kv节点

- 若key不以curr_key为前缀，说明没有找到，直接返回
- 若是叶节点
  - 如果key == curr_key，返回空节点
  - 否则，没有找到，返回该节点
- 若是扩展节点，则递归地删除其子节点，得到new_sub_node
  - 若new_sub_node与node值相等，返回node
  - 若new_sub_node是空节点，返回BLANK_NODE
  - 若new_sub_node是kv节点，curr_key与新子节点串联当作key，新子节点的value当作value
  - 若new_sub_node是分支节点，node的value指向新子节点

```python
def _delete_kv_node(self, node, key):
    node_type = self._get_node_type(node)
    assert is_key_value_type(node_type)
    curr_key = without_terminator(unpack_to_nibbles(node[0]))

    if not starts_with(key, curr_key):
        # key not found
        return node

    if node_type == NODE_TYPE_LEAF:
        return BLANK_NODE if key == curr_key else node

    # for inner key value type
    new_sub_node = self._delete_and_delete_storage(
        self._decode_to_node(node[1]), key[len(curr_key):])

    if self._encode_node(new_sub_node) == node[1]:
        return node

    # new sub node is BLANK_NODE
    if new_sub_node == BLANK_NODE:
        return BLANK_NODE

    assert isinstance(new_sub_node, list)

    # new sub node not blank, not value and has changed
    new_sub_node_type = self._get_node_type(new_sub_node)

    if is_key_value_type(new_sub_node_type):
        # collape subnode to this node, not this node will have same
        # terminator with the new sub node, and value does not change
        new_key = curr_key + unpack_to_nibbles(new_sub_node[0])
        return [pack_nibbles(new_key), new_sub_node[1]]

    if new_sub_node_type == NODE_TYPE_BRANCH:
        return [pack_nibbles(curr_key), self._encode_node(new_sub_node)]

    # should be no more cases
    assert False
```

## 贡献说明

本项目由张雨欣一人完成

### REFERENCE

https://easythereentropy.wordpress.com/2014/06/04/understanding-the-ethereum-trie/

https://github.com/ebuchman/understanding_ethereum_trie

https://www.cnblogs.com/fengzhiwu/p/5584809.html
