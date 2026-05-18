# CPP-006 bitset 与位运算

模块编号：CPP-006

模块名称：`bitset` 与整数位运算

标签：bitset、mask、位运算、子集、状态压缩、快速集合

一句话用途：用二进制位表示集合、状态和可达性，快速做包含、枚举、计数和转移。

题面触发词：子集、状态压缩、选或不选、集合、二进制、开关、可达和、最多 20 个点、位标记。

什么时候用：元素数较小可用 `mask` 表示集合；可达性长度固定且不太大时用 `bitset` 加速。

不要什么时候用：位数运行时才知道且很大时，`bitset<N>` 不方便；`n > 25` 的全子集枚举通常爆炸。

复杂度：单个整数位操作 `O(1)`；枚举所有子集 `O(2^n)`；`bitset` 按机器字批量运算，常数很小。

数据范围参考：`n <= 20` 常可枚举所有 `mask`；`n <= 60` 可用 `long long` 存集合；可达和 `<= 1e5` 常用 `bitset`。

依赖的标准容器：`bitset`、`vector`、整数类型 `int` / `long long`。

输入如何整理：题面第 `i` 个元素仍编号 `1..n`，映射到 bit `i-1`；字符串/开关可转成 `mask`；可达和用 `bitset<MAXS + 1>`。

接口：

- `mask & (1u << (i - 1))`：测试题面第 `i` 个元素，适合 `unsigned int mask`。
- `mask | (1u << (i - 1))`：加入题面第 `i` 个元素。
- `mask & ~(1u << (i - 1))`：删除题面第 `i` 个元素。
- `1LL << (i - 1)`：`i` 可能超过 31 时用 `long long mask`。
- `__builtin_popcount(mask)`：统计 `int` 的 1 个数。
- `__builtin_popcountll(mask)`：统计 `long long` 的 1 个数。
- `bs.test(i) / bs.set(i) / bs.reset(i)`：`bitset` 单点操作。

输出能力：输出集合大小、状态编号、是否可达、满足条件的子集数量。

下游可接：暴力枚举、状压 DP、背包可达性、图上小点集搜索。

可拼接模块：CPP-002 基础容器、CPP-008 整数溢出、DP 状压模块。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXS = 100000;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, target;
    cin >> n >> target;

    bitset<MAXS + 1> can;
    can[0] = 1;

    int mask = 0;
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        if (0 <= x && x <= MAXS) can |= (can << x);
        if (i <= 30 && (x % 2 != 0)) mask |= (1 << (i - 1));
    }

    cout << (0 <= target && target <= MAXS && can[target] ? 1 : 0) << '\n';
    cout << __builtin_popcount((unsigned)mask) << '\n';

    return 0;
}
```

调用示例：

```cpp
// 枚举 mask 的所有非空子集
for (int sub = mask; sub; sub = (sub - 1) & mask) {
    // sub 是 mask 的一个非空子集
}

// 遍历题面元素编号 1..n
for (int i = 1; i <= n; i++) {
    if (mask & (1 << (i - 1))) {
        // 第 i 个元素被选中
    }
}

// long long 位移，k 可能 >= 31 时必须写 1LL
long long one = 1LL << k;
```

常见坑：

- `1 << 40` 会溢出 `int`，要写 `1LL << 40`。
- `__builtin_ctz(0)`、`__builtin_ctzll(0)` 不合法，调用前先判断非零。
- `bitset<N>` 的 `N` 必须是编译期常量。
- 子集枚举是指数复杂度，看到 `n=30` 以上要谨慎。
- mask 位号自然从 0 开始；题面对象编号仍保持 `1..n`。`int mask` 写 `1u << (i - 1)`；`long long mask` 写 `1LL << (i - 1)`。
- `~mask` 会把高位也变成 1，清位时写 `mask & ~(1 << i)`，并确保类型合适。

暴力/部分分替代：元素少时直接 DFS 枚举选/不选；可达和也可用 `vector<int>` 做普通背包。

升级方向：子集枚举接状压 DP；`bitset` 接背包可达性、集合交并、字符串匹配加速。

最小测试样例：

```text
输入
3 5
2 3 4

输出
1
1
```
