# PY-02 Python 标准库速查

模块编号：PY-02

模块名称：无第三方库条件下的 Python 标准库算法工具

标签：Python、标准库、heapq、bisect、itertools、collections、functools、math

一句话用途：只用 Python 标准库，把常见算法工具补齐：队列、堆、二分、枚举、记忆化、计数、数学函数。

题面触发词：

- Top-K、最小堆、Dijkstra。
- 排序数组二分、插入位置、第一个大于等于。
- 组合、排列、笛卡尔积。
- 计数、默认字典、双端队列。
- 递归状态记忆化。
- gcd、组合数、整根、取模快速幂。

什么时候用：

- Python 代码需要堆、队列、二分、组合枚举。
- 想快速写暴力枚举或小数据精确解。
- 需要标准数学函数，且不能用第三方库。

不要什么时候用：

- 不要用 `bisect` + `list.insert` 模拟大规模平衡树，中间插入是 `O(n)`。
- 不要用 `itertools.permutations` 处理 `n > 10` 的全排列。
- 不要滥用 `Counter` 在巨量循环里创建新对象。
- 不要把 `lru_cache` 用在参数包含 `list/set/dict` 的函数上，它们不可哈希。

复杂度：

- `heapq.heappush/heappop`：`O(log n)`。
- `bisect_left/right`：`O(log n)`，但 list 中间插入删除 `O(n)`。
- `deque.append/popleft`：`O(1)`。
- `itertools.permutations`：枚举量本身是 `n!`。
- `lru_cache`：每个状态算一次，哈希 key 有常数开销。

依赖的标准容器：

- `collections.deque`
- `collections.Counter`
- `collections.defaultdict`
- `heapq`
- `bisect`
- `itertools`
- `functools.lru_cache`
- `math`

输入如何整理：

```python
import sys
from collections import deque, defaultdict, Counter
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from itertools import combinations, permutations, product
from functools import lru_cache
from math import gcd, isqrt, comb
```

接口：

```text
队列：deque
堆：heapq，默认最小堆
二分：bisect_left / bisect_right
组合枚举：itertools
记忆化：@lru_cache(None)
数学：gcd/isqrt/comb/pow(a,b,mod)
```

模板代码：

```python
from collections import deque, defaultdict, Counter
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from itertools import combinations
from functools import lru_cache
from math import gcd, isqrt

def demo():
    q = deque([1, 2])
    q.append(3)
    first = q.popleft()

    heap = []
    heappush(heap, (5, "a"))
    heappush(heap, (2, "b"))
    smallest = heappop(heap)

    a = [1, 2, 2, 4]
    left = bisect_left(a, 2)
    right = bisect_right(a, 2)

    cnt = Counter(a)
    pos = defaultdict(list)
    for i, x in enumerate(a, 1):
        pos[x].append(i)

    @lru_cache(None)
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    pairs = list(combinations([1, 2, 3], 2))
    return first, smallest, left, right, cnt[2], pos[2][0], fib(10), gcd(12, 18), isqrt(10), pairs

print(demo())
```

## 常用片段

### heapq 最小堆和最大堆

```python
from heapq import heappush, heappop

min_heap = []
heappush(min_heap, 5)
heappush(min_heap, 2)
print(heappop(min_heap))  # 2

max_heap = []
heappush(max_heap, -5)
heappush(max_heap, -2)
print(-heappop(max_heap))  # 5
```

### 二分

```python
from bisect import bisect_left, bisect_right

a = [1, 2, 2, 4, 7]
print(bisect_left(a, 2))   # 第一个 >= 2 的 0-index 位置
print(bisect_right(a, 2))  # 第一个 > 2 的 0-index 位置
```

### 组合枚举

```python
from itertools import combinations, permutations, product

for comb2 in combinations([1, 2, 3, 4], 2):
    print(comb2)

for p in permutations([1, 2, 3]):
    print(p)

for bits in product([0, 1], repeat=3):
    print(bits)
```

### 数学函数

```python
from math import gcd, isqrt, comb

print(gcd(18, 24))
print(isqrt(10))
print(comb(5, 2))
print(pow(2, 10, 1000))  # 2^10 mod 1000
```

调用示例：

```python
from collections import Counter

s = "abacaba"
cnt = Counter(s)
print(cnt["a"])
```

常见坑：

- `heapq` 的元素如果第一关键字相同，会继续比较第二项；第二项不能比较时要加编号。
- `bisect` 返回 0-index 位置；如果你的数组手动 1-index，不要混淆。
- `combinations`、`permutations` 返回迭代器，数量可能爆炸。
- `lru_cache` 的参数必须可哈希，`list` 要转成 `tuple`。
- `defaultdict(list)` 访问不存在 key 时会创建空 list，调试时注意字典大小变化。
- `math.comb(n,k)` 对很大 n 也能算，但结果巨大时输出和内存仍可能很大。

暴力/部分分替代：

- 组合枚举可直接拿 `n <= 20` 或 `k` 很小的子任务分。
- `Counter` 可以快速写频率统计，先过数据较小的统计题。
- `lru_cache` 可以把暴力 DFS 直接升级为记忆化搜索。

最小测试样例：

```text
输出
(1, (2, 'b'), 1, 3, 2, 2, 55, 6, 3, [(1, 2), (1, 3), (2, 3)])
```
