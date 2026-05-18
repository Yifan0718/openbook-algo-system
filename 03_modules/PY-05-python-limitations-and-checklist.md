# PY-05 Python 提交风险清单

模块编号：PY-05

模块名称：Python 局限性、TLE/MLE 风险与提交前检查

标签：Python、TLE、MLE、递归、内存、标准库限制、提交检查

一句话用途：因为主力仍是 C++，所以用 Python 前先确认它有明显优势；用 Python 后按清单避免语言常数、内存和标准库缺口导致丢分。

题面触发词：

- 时间限制短。
- `n,m` 很大。
- 多组数据。
- 需要递归、堆、二分、字典、二维数组。
- 需要浮点格式或大整数。

什么时候用：

- 你准备临场放弃 C++ 改用 Python 前，必须先翻这一页。
- Python 代码写完后提交前检查。
- 在 C++ 和 Python 之间犹豫时，用本模块判断风险。
- Python 部分分版本准备提交时，确保不会因为 IO/递归/内存直接 0 分。

不要什么时候用：

- 不要因为 Python 写法短，就忽略复杂度。
- 不要把“样例过了”当成 Python 不会 TLE 的证据。
- 不要使用任何第三方库。

复杂度：

- 语言不会拯救错误复杂度；Python 对常数更敏感。
- 大循环估算要更保守：`1e7` 级别谨慎，`3e7` 以上危险。
- `dict/set/tuple` 很方便，但每个状态内存远大于 C++ 数组。

依赖的标准容器：

- `sys.stdin.buffer`
- `sys.stdout.write`
- `list`
- `dict`
- `set`
- `tuple`
- `deque`
- `heapq`

输入如何整理：

```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    # 统一在这里解析，不要边读边慢速 input

if __name__ == "__main__":
    solve()
```

接口：

```text
Python 提交前检查：
1. 输入是否用 buffer。
2. 输出是否批量。
3. 是否用了第三方库。
4. 最大循环次数是否可接受。
5. 递归深度是否安全。
6. 容器是否会爆内存。
7. list/deque/bisect/heapq 是否用对复杂度。
```

模板代码：

```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    out = []
    for x in data:
        out.append(str(int(x)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

## 提交前检查表

| 检查项 | 风险 | 修法 |
|---|---|---|
| 大输入用 `input()` | 慢 | `sys.stdin.buffer.read().split()`；超大输入改 `buffer.readline()` 流式读 |
| 循环里频繁 `print` | 慢 | `out.append` 后一次输出 |
| 队列用 `pop(0)` | `O(n)` | `deque.popleft()` |
| 中间插入 list | `O(n)` | 换 C++ 平衡树或重新建模 |
| `lru_cache` 状态过多 | MLE | 压状态、剪枝、改 C++ |
| 深递归 | RE/TLE | 迭代写法或 C++ |
| 二维数组太大 | MLE | 滚动数组、稀疏 dict、C++ |
| `heapq` 删除元素 | 没有直接删除 | 懒删除或重复入堆 |
| 使用 `numpy` | 违规 | 只用标准库 |
| 浮点比较 | 精度误差 | 用整数化或 `eps` |

## Python 和 C++ 的临场选择

| 数据特征 | 建议 |
|---|---|
| `n <= 20` 状态/枚举 | Python 可优先 |
| `n <= 40` 折半枚举 | Python 可写，但注意枚举量 |
| `n <= 2000` 字符串 DP | Python 可能可过，最好滚动数组 |
| `n,m <= 1e5` 图论 | C++ 更稳 |
| 高精度输出 | Python 优先 |
| 动态区间修改查询 | C++ 优先 |
| 复杂哈希状态搜索 | Python 优先拿部分分 |
| 强卡常最短路/线段树 | C++ 优先 |

调用示例：

```python
# 多行输出不要这样：
# for x in ans:
#     print(x)

# 建议这样：
ans = [1, 2, 3]
sys.stdout.write("\n".join(map(str, ans)))
```

常见坑：

- `//` 是向下取整，不是向 0 取整。负数除法要特别小心。
- Python `%` 的结果符号跟除数方向有关，和 C++ 负数取模可能不同。
- `True`/`False` 可以当 `1/0`，但输出格式要按题目要求。
- `float` 是双精度，不是高精度实数。
- `sys.setrecursionlimit(1000000)` 不等于递归一定安全。
- `copy()` 只是浅拷贝，二维数组复制要小心。

暴力/部分分替代：

- Python 适合先写清楚的部分分版本，尤其是 DFS/BFS/记忆化。
- 如果估算会 TLE，不要硬冲，用 C++ 正解模板接力。
- 大数据不会做时，Python 也可以写合法兜底输出，但要保证不 RE。

最小测试样例：

```text
输入
1 2 3

输出
1
2
3
```
