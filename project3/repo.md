# Project 3

`实验报告`

## 代码思想

随机生成字符串，用python字典将（前m位哈希值：字符串）以键值对形式存储。直到找到哈希值相同的字符串。

## 测试结果

### 32bit

```python
a = "h9QBWTlbEoc8iRA35GNqOeZzSCXDYgJj"
b = "wUxZ9tGvSimRsJronau2DBfg8VEX46pQ"
Hash(a) = 0xcf109b664b162136669cc2cea1ba073ae7f0237d4507bd9054d85a8a4fd54e38
Hash(b) = 0xcf109b662e1f62be3e93a9bd85aa417706926d2e600b7669636d81abee414be0
```

### 40bit

```python
a = "15iCeXhUxaTWySgkM2uHcQ8jfEK6lA"
b = "tQ9vVLIzKZAR80FyBdoku6YlGnf3gi"
Hash(a) = 0x194aea187a7b4efcaa37d78477872fef33f356a0162a23a3cbf1fc27b0d0b369
Hash(b) = 0x194aea1876aac21ccbcc869051c31f5763f9f5fe445519d327e8fbfc7ce0f94f
```
