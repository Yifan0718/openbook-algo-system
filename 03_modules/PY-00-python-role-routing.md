# PY-00 Python 互补使用路由

模块编号：PY-00

模块名称：Python 适用场景与 C++ 切换路由

标签：Python、语言选择、部分分、标准库、开卷补充、不能使用第三方库

一句话用途：默认仍用 C++；只有当 Python 能明显省掉高精度、复杂状态、字符串解析、暴力记忆化等实现成本时，才把 Python 当作补位工具。

题面触发词：

- 高精度、大整数、整数位数很长，但运算次数不巨大。
- 状态天然是字符串、元组、集合、字典键。
- 输入格式杂、字符串处理多、需要快速拆分统计。
- 小数据部分分、暴力枚举、记忆化搜索。
- 组合枚举、排列枚举、计数器、哈希集合。
- 需要快速写出正确版本，而不是压榨常数。

什么时候用：

- 你明显更熟悉 C++，但这道题 Python 的实现优势足够大。
- 题目允许 Python，且时间限制没有明显卡常。
- 你能用 Python 在 10 分钟内写出 C++ 要 25 分钟才稳的版本。
- 大整数直接用 `int` 能避免手写高精度。
- 状态可以直接用 `tuple` / `str` / `frozenset` 做字典键。
- 目标是先拿小数据或中等数据部分分。
- 代码以清晰正确为主，复杂度本身已经足够。

不要什么时候用：

- `n,m` 到 `2e5` 以上，核心循环很多，且算法常数敏感。
- 重型图论、线段树懒标记、最大流、SCC、LCA 多查询等已经有 C++ 稳模板。
- 需要动态有序集合、排名、前驱后继，Python 标准库没有好用的平衡树。
- 题目卡 `O(n log n)` 常数或输入巨大，Python 容易 TLE。
- 需要大量二维数组对象，Python 内存开销远高于 C++。
- 考场 Python 版本不明确，而你用了较新的语法。

复杂度：

- Python 不改变算法复杂度，只改变编码成本和常数。
- 粗略经验：Python 纯循环 `1e7` 级别已经要谨慎，`3e7` 以上通常危险。
- 内置函数和标准库通常由 C 实现，排序、哈希、`math`、大整数比纯 Python 循环更可靠。

依赖的标准容器：

- 内置：`list`、`tuple`、`dict`、`set`、`str`、`int`。
- 标准库：`sys`、`collections`、`heapq`、`bisect`、`itertools`、`functools`、`math`。
- 禁止依赖第三方库：不要使用 `numpy`、`pandas`、`sortedcontainers`、`networkx`。

输入如何整理：

```python
import sys

data = sys.stdin.buffer.read().split()
it = iter(data)
n = int(next(it))
a = [0] + [int(next(it)) for _ in range(n)]
```

接口：

```text
先判断语言：
0. 默认语言是 C++。
1. C++ 模板已经很稳、数据大、卡常 -> 坚持 C++。
2. Python 能直接省掉大量实现，且数据中小 -> 可以用 Python。
3. 不确定能否过 -> Python 先交部分分，C++ 再冲正解。
```

## Python 特别适合的任务

| 任务 | Python 优势 | C++ 对照 |
|---|---|---|
| 高精度整数 | `int` 自动任意精度 | 要手写 BigInteger |
| 状态记忆化 | `@lru_cache(None)` + `tuple` 参数 | 要设计数组/hash 编码 |
| 字典计数 | `Counter/defaultdict` | `map/unordered_map` 写法更长 |
| 集合判重 | `set` 直接存 tuple/string | C++ 需要 hash 或结构体比较 |
| 排列组合 | `itertools` 一行枚举 | C++ 要 DFS 或 next_permutation |
| 字符串解析 | `split/strip/join/replace` 快 | C++ string 处理更繁 |
| 小数据暴力 | 代码短，容易先拿分 | C++ 稳但更长 |
| 子集和位集 | Python `int` 位运算很强 | C++ 要 bitset 或手写 |

## Python 明显不适合的任务

| 任务 | 风险 | 优先方案 |
|---|---|---|
| 大图 Dijkstra `m >= 2e5` | 堆和邻接表对象常数大 | C++ `GRAPH-03` |
| 懒标记线段树大量操作 | 递归/对象/函数调用慢 | C++ `DS-03` |
| 最大流、SCC、复杂树链 | 模板长且常数高 | C++ 图论卷 |
| 动态有序集合 | 标准库没有平衡树 | C++ `set/multiset` |
| 巨大二维 DP | Python int/list 对象开销大 | C++ 静态数组或滚动数组 |
| 深递归 `> 1e5` | 栈风险和函数调用慢 | C++ 或 Python 迭代 |

模板代码：

```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = [0] + [int(next(it)) for _ in range(n)]
    print(sum(a))

if __name__ == "__main__":
    solve()
```

调用示例：

```python
# 高精度直接算
a = int("9" * 100)
b = int("8" * 100)
print(a + b)
print(a * b)

# 状态可以直接用 tuple 做 key
seen = set()
seen.add((3, 5, "mask"))
```

常见坑：

- `input()` 循环读大输入容易慢，优先 `sys.stdin.buffer.read().split()`。
- Python 的数组下标天然 0-index；本资料建议普通数组仍手动开 `n+1`，用 `1..n`。
- 字符串天然 0-index，字符串题不要强行 1-index，除非你非常确定。
- `heapq` 是最小堆，没有删除和修改 key；删除要用懒删除。
- `list.insert`、`pop(0)` 是 `O(n)`；队列用 `collections.deque`。
- `bisect` 只能高效二分，不能高效中间插入。
- `lru_cache` 会占内存，状态过多时可能 MLE。
- `sys.setrecursionlimit` 只提高限制，不保证深递归安全。

暴力/部分分替代：

- 先用 Python 写小数据精确解：排列、子集、DFS、BFS、记忆化。
- 如果 Python 正解可能 TLE，可以先交 Python 部分分，再切回 C++ 冲满分。
- 对构造题，Python 可先写合法兜底输出。
- 对计数题，不取模且答案很大时 Python 先直接输出大整数。

最小测试样例：

```text
输入
3
10 20 30

输出
60
```
