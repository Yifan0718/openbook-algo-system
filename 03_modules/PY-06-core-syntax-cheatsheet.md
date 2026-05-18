# PY-06 Python 核心语法速查

模块编号：PY-06

模块名称：Python 控制流、函数、切片、推导式与语法坑

标签：Python、语法、控制流、函数、切片、推导式、lambda、bytes、str、作用域

一句话用途：当你临场决定用 Python 时，用这一页快速确认基础语法怎么写，避免因为缩进、范围、除法、切片和作用域丢分。

题面触发词：

- 需要把 C++ 思路快速翻译成 Python。
- 需要写循环、判断、函数、递归、排序 key。
- 需要处理字符串、字节输入、切片、下标。
- 需要列表推导式或生成二维数组。
- 需要注意 Python 与 C++ 的整数除法/取模差异。

什么时候用：

- 已经根据 `PY-00` 判断 Python 有明显优势。
- 写 Python 代码前先翻一遍基础语法。
- 把 C++ 模板改成 Python 部分分版本时。
- 调试 Python WA/RE/TLE 时检查语言坑。

不要什么时候用：

- 不要因为语法短就用 Python 硬冲大数据卡常题。
- 不要在考场使用复杂新语法，例如 `match`、海象运算符、复杂装饰器。
- 不要把这一页当 Python 教材；它是考场速查。

复杂度：

- 语法本身不改变复杂度。
- 切片会复制，`a[l:r]` 是 `O(r-l)`。
- 列表推导式通常比手写 `append` 略简洁，但仍然按元素循环。
- `in list` 是 `O(n)`，`in set/dict` 均摊 `O(1)`。

依赖的标准容器：

- `list`
- `tuple`
- `dict`
- `set`
- `str`
- `bytes`
- `range`

输入如何整理：

```python
import sys

data = sys.stdin.buffer.read().split()
it = iter(data)
n = int(next(it))
s = next(it).decode()  # 需要字符串函数时再 decode
```

接口：

```text
控制流：if / elif / else, for, while, break, continue
函数：def solve(): return
排序 key：a.sort(key=lambda x: x[1])
遍历：range, enumerate, zip
推导式：[expr for x in xs if cond]
切片：s[l:r] 左闭右开
```

模板代码：

```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = [0] + [int(x) for x in data[1:1 + n]]

    total = 0
    best = -10 ** 30
    for i in range(1, n + 1):
        x = a[i]
        if x > 0:
            total += x
        elif x == 0:
            continue
        else:
            total -= -x
        best = max(best, total)

    sys.stdout.write(str(best))

if __name__ == "__main__":
    solve()
```

## 控制流

```python
if x < 0:
    print("negative")
elif x == 0:
    print("zero")
else:
    print("positive")

for i in range(1, n + 1):
    if a[i] == 0:
        continue
    if a[i] < 0:
        break

while n > 0:
    n //= 2
```

## 函数、全局变量与递归

```python
import sys
sys.setrecursionlimit(1000000)

ans = 0

def dfs(u, parent):
    global ans
    ans += 1
    for v in g[u]:
        if v != parent:
            dfs(v, u)
```

注意：

- 函数里只读全局变量不需要 `global`。
- 函数里要给全局变量重新赋值，必须写 `global ans`。
- 深递归仍然可能不稳；树很深时 C++ 更可靠。

## range、enumerate、zip

```python
for i in range(1, n + 1):
    print(i)

for idx, x in enumerate(a[1:], 1):
    print(idx, x)

for x, y in zip(a, b):
    print(x, y)
```

## 列表推导式与二维数组

```python
a = [int(x) for x in data]
even = [x for x in a if x % 2 == 0]

grid = [[0] * (m + 1) for _ in range(n + 1)]
```

不要写：

```python
grid = [[0] * (m + 1)] * (n + 1)  # 错，多行共用同一行
```

## 切片与字符串

```python
s = "abcdef"
print(s[0])      # a
print(s[-1])     # f
print(s[1:4])    # bcd
print(s[:3])     # abc
print(s[3:])     # def
print(s[::-1])   # fedcba
```

切片左闭右开，会复制新对象；大循环里频繁切长字符串可能 TLE。

## 排序 key 与 lambda

```python
items = [(90, 18), (90, 17), (80, 20)]
items.sort(key=lambda x: (-x[0], x[1]))

words = ["bbb", "a", "cc"]
words.sort(key=lambda s: (len(s), s))
```

## bytes 和 str

```python
data = sys.stdin.buffer.read().split()
x = int(data[0])          # bytes 可以直接转 int
s = data[1].decode()      # 需要字符串方法时转 str

if s.startswith("abc"):
    print(s.upper())
```

## Python 与 C++ 的除法/取模差异

```python
print(-7 // 3)  # -3，向下取整
print(-7 % 3)   # 2
```

C++ 中 `-7 / 3 == -2`，`-7 % 3 == -1`。如果题目要求 C++ 风格向 0 取整，可写：

```python
def div_trunc(a, b):
    q = abs(a) // abs(b)
    if (a < 0) ^ (b < 0):
        q = -q
    return q

def mod_trunc(a, b):
    return a - div_trunc(a, b) * b
```

调用示例：

```python
print(div_trunc(-7, 3))
print(mod_trunc(-7, 3))
```

常见坑：

- Python 靠缩进表示代码块，不能像 C++ 一样靠 `{}`。
- `range(l, r)` 不包含 `r`。
- `and`、`or`、`not` 不是 `&&`、`||`、`!`。
- `//` 对负数不是向 0 取整。
- `a = b` 不是复制列表，只是引用同一个对象；复制一维列表用 `a = b[:]`。
- 空列表、空字符串、0 都是假；非空容器一般是真。
- `is` 判断对象身份，比较数值/字符串通常用 `==`。

暴力/部分分替代：

- 用 Python 写部分分时，宁可语法朴素，也不要写复杂推导式。
- 能用 `for i in range(...)` 写清楚，就不要强行一行流。
- 排序和哈希统计用内置能力，别手写低效循环。

最小测试样例：

```text
输入
5
3 -1 0 4 -2

输出
6
```
