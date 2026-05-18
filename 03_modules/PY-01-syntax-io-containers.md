# PY-01 Python 语法、输入输出与基础容器

模块编号：PY-01

模块名称：Python 考场语法与容器速查

标签：Python、IO、list、dict、set、str、tuple、排序、格式化输出

一句话用途：当你决定用 Python 时，用这一页快速抄输入输出、1-index 数组、字典集合、字符串和格式化输出写法。

题面触发词：

- 输入很大、需要快速读。
- 需要数组、二维数组、字符串、字典计数、集合判重。
- 需要排序、多关键字排序、去重。
- 输出小数、对齐、拼接多行答案。

什么时候用：

- 所有 Python 提交都先从本模块骨架开始。
- 需要把 C++ 思路翻译成 Python 代码。
- 需要快速确认某个容器函数怎么写。

不要什么时候用：

- 不要把 Python 写成复杂工程风格；考场只需要短函数和全局变量。
- 不要为表现语法新特性使用 `match`、复杂生成器链、装饰器魔法。
- 数据很大时不要逐行 `input()` 加大量字符串拼接。

复杂度：

- `list` 末尾 `append/pop`：均摊 `O(1)`。
- `dict/set` 查询插入删除：均摊 `O(1)`。
- `sort`：`O(n log n)`。
- `str` 拼接多段：用 `''.join(parts)`，不要循环 `s += piece`。
- `list.insert(0,x)`、`pop(0)`：`O(n)`，队列不要这样写。

依赖的标准容器：

- `list`：数组、栈、邻接表。
- `tuple`：多关键字、不可变状态 key。
- `dict`：映射、稀疏 DP。
- `set`：去重、访问标记。
- `str`：字符串处理。
- `collections.deque`：队列。

输入如何整理：

```python
import sys

data = sys.stdin.buffer.read().split()
it = iter(data)

n = int(next(it))
a = [0] + [int(next(it)) for _ in range(n)]  # 1-index
```

## 输入分隔方式总表

先判断输入是“token 流”，还是“每行有特殊含义”。

| 输入形态 | Python 推荐 | 说明 |
|---|---|---|
| 整数/单词由空格、换行、Tab 任意分隔 | `sys.stdin.buffer.read().split()` | 全部空白都当分隔符，通常最快 |
| 数据量小、每行格式简单 | `input().split()` | 写法短，但大量输入偏慢 |
| 每一行是一条记录/句子/表达式 | `sys.stdin.readline()` 或 `for line in sys.stdin` | 保留行边界 |
| 字符串可能含空格 | `line = sys.stdin.readline().rstrip('\n')` | 不要用 `split()` |
| 要保留行首/行尾空格 | 只去掉换行：`rstrip('\n')` | 不要用 `strip()`，它会删空格 |
| 逗号分隔且无引号 | `line.split(',')` | 真 CSV 有引号时翻 `SIM-04` 或用 `csv` 标准库 |
| JSON/脚本/多行文本 | `sys.stdin.read()` | 整段读入，自己解析 |

口令：

```text
`read().split()` 会一次性保存所有 token；输入极大或必须流式处理时，改用 `buffer.readline()`、`for line in sys.stdin.buffer`，或自写流式整数解析。
普通算法题整数输入：read().split()。
行有意义：readline()/for line in sys.stdin。
含空格字符串：不要 split 整行。
```

### 空格和换行等价的例子

下面两份输入对 `read().split()` 完全一样：

```text
3
10 20 30
```

```text
3 10
20
30
```

代码：

```python
import sys

data = sys.stdin.buffer.read().split()
it = iter(data)
n = int(next(it))
a = [0] + [int(next(it)) for _ in range(n)]
```

### 行边界有意义的例子

```python
import sys

n = int(sys.stdin.readline())
lines = [""]
for _ in range(n):
    line = sys.stdin.readline().rstrip("\n")  # 保留其他空格
    lines.append(line)
```

### 混合 token 和整行

读完第一行的 `n` 后，再读 `n` 行句子：

```python
import sys

n = int(sys.stdin.readline())
sentences = [""]
for _ in range(n):
    sentences.append(sys.stdin.readline().rstrip("\n"))
```

如果先用 `read().split()`，就已经丢掉了所有行边界，后面不能再恢复整行。

### EOF 读到输入末尾就停止

Python 有两种常用 EOF 模式。

Token 流直到 EOF，最快：

```python
import sys

data = sys.stdin.buffer.read().split()
for token in data:
    x = int(token)
    # use x
```

每组两个整数直到 EOF：

```python
import sys

data = sys.stdin.buffer.read().split()
out = []
for i in range(0, len(data), 2):
    if i + 1 >= len(data):
        break  # 或按题意报错
    n = int(data[i])
    m = int(data[i + 1])
    out.append(str(n + m))

sys.stdout.write("\n".join(out))
```

每组长度不固定，例如每组先给 `n`，后面跟 `n` 个数：

```python
import sys

data = sys.stdin.buffer.read().split()
p = 0
out = []
while p < len(data):
    n = int(data[p])
    p += 1
    a = [0]
    for _ in range(n):
        a.append(int(data[p]))
        p += 1
    out.append(str(sum(a)))

sys.stdout.write("\n".join(out))
```

按行读到 EOF：

```python
import sys

for line in sys.stdin:
    line = line.rstrip("\n")
    # process line
```

或者显式 `readline()`：

```python
import sys

while True:
    line = sys.stdin.readline()
    if line == "":  # EOF
        break
    line = line.rstrip("\n")
    # process line
```

注意：空行是 `"\n"`，不是 EOF；如果用 `if not line.strip(): break`，会把空行误判成输入结束。

接口：

```text
solve() 里读入、计算、输出。
普通数组开 n+1。
图开 g = [[] for _ in range(n + 1)]。
答案多行先 append 到 out，最后 '\n'.join(out)。
```

模板代码：

```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))

    a = [0] + [int(next(it)) for _ in range(n)]
    a[1:] = sorted(a[1:])

    cnt = {}
    for i in range(1, n + 1):
        cnt[a[i]] = cnt.get(a[i], 0) + 1

    out = []
    out.append(str(sum(a)))
    out.append(" ".join(map(str, a[1:])))
    out.append(str(len(cnt)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

## 基础写法速查

### 1-index 数组

```python
n = int(input())
a = [0] + list(map(int, input().split()))
for i in range(1, n + 1):
    a[i] += 1
```

### 二维数组

```python
n, m = map(int, input().split())
grid = [[0] * (m + 1)]
for _ in range(n):
    row = [0] + list(map(int, input().split()))
    grid.append(row)
```

### 多关键字排序

```python
items = [(90, 18), (90, 17), (80, 20)]
items.sort(key=lambda x: (-x[0], x[1]))  # 第一关键字降序，第二关键字升序
```

### 字典计数

```python
cnt = {}
for x in a[1:]:
    cnt[x] = cnt.get(x, 0) + 1
```

### 集合判重

```python
seen = set()
state = (x, y, mask)
if state not in seen:
    seen.add(state)
```

### 字符串常用操作

```python
s = "  abc,def,ghi  "
s = s.strip()
parts = s.split(",")
t = "-".join(parts)
print(s[0], s[-1], s[1:4])
```

### 简单分隔格式

空白分隔：

```python
nums = list(map(int, line.split()))
```

逗号分隔：

```python
cells = line.rstrip("\n").split(",")
```

`key=value`：

```python
key, value = line.rstrip("\n").split("=", 1)
```

`key: value`：

```python
key, value = line.rstrip("\n").split(":", 1)
value = value.lstrip()  # 只去掉冒号后的前导空格
```

### 格式化输出

```python
x = 3.1415926
print(f"{x:.2f}")       # 3.14
print(f"{123:>6}")      # 右对齐宽度 6
print(f"{123:06d}")     # 000123
```

调用示例：

```python
from collections import deque

q = deque()
q.append(1)
q.append(2)
print(q.popleft())
```

常见坑：

- `range(1, n)` 不包含 `n`；1-index 循环写 `range(1, n + 1)`。
- `a = [[0] * m] * n` 是错的，多行会共用同一个列表。
- `sort()` 原地排序并返回 `None`；`b = sorted(a)` 才是新数组。
- `dict` 不等于有序平衡树；不能高效求前驱后继。
- `int(next(it))` 中 `next(it)` 是 `bytes`，`int` 可以直接处理，不必 `.decode()`。
- `read().split()` 会丢掉换行和空行；行结构重要时不要用。
- `strip()` 会删除行首和行尾空格；只想删换行用 `rstrip("\n")`。
- `print` 很多次会慢，答案多行用列表收集后一次输出。

暴力/部分分替代：

- 不会优化时，用 `dict/set` 直接记状态，先过小数据。
- 字符串题先用 `split/replace/count/find` 写朴素解。
- 排序后扫描能拿一部分时，不要先写复杂数据结构。

最小测试样例：

```text
输入
5
3 1 2 2 5

输出
13
1 2 2 3 5
4
```
