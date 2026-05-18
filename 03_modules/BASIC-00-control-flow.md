# BASIC-00 顺序、分支、循环、函数与结构体

模块编号：BASIC-00

模块名称：顺序、分支、循环、函数与结构体

标签：基础语法、顺序结构、分支结构、循环结构、函数、struct、1-index

一句话用途：把题面步骤翻译成稳定的 C++17 单文件程序，先跑通输入输出，再把核心逻辑装进函数。

题面触发词：

- 按步骤处理、依次读入、逐个判断。
- 如果、否则、满足条件、分类讨论。
- 重复、直到、枚举每个数、统计个数。
- 学生、商品、区间、操作记录等多字段对象。

什么时候用：

- 题目本身是基础模拟、统计、分类讨论。
- 算法还没想清时，先搭 `main + solve + 函数` 外壳。
- 需要把多个字段放在一起排序、传参、返回。
- 需要把大段代码拆成 `check/calc/read/print`，降低调试难度。

不要什么时候用：

- 核心复杂度已经明显超时，只写循环结构不能解决模型问题。
- 需要图论、DP、数据结构等专门模板时，本模块只作为外壳。
- 递归深度可能很大且能用循环替代时，不要强行递归。

复杂度：

- 顺序扫描：`O(n)`。
- 双重循环：`O(n^2)`。
- 三重循环：`O(n^3)`。
- 函数调用本身不是主要复杂度，主要看函数内部循环。

数据范围参考：

| 数据范围 | 可先写的结构 |
|---|---|
| `n <= 1e6` | 单循环、少量数组 |
| `n <= 5000` | 双重循环边缘可试 |
| `n <= 500` | 三重循环有时可试 |
| `n <= 10` | 枚举、全排列、暴力分类 |

依赖的标准容器：

- `vector<int>`、`vector<long long>`：默认 1-index，开 `n + 1`。
- `string`：C++ 自然 0-index。
- `struct Node`：多字段对象。

输入如何整理：

```cpp
struct Node {
    long long x;
    long long y;
    int id;
};

int n;
cin >> n;

vector<long long> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];

vector<Node> p(n + 1);
for (int i = 1; i <= n; i++) {
    cin >> p[i].x >> p[i].y;
    p[i].id = i;
}
```

整理顺序：

1. 先读标量：`n, m, q, T`。
2. 再读数组：`a[1..n]`。
3. 再读对象：用 `struct` 存字段和原编号。
4. 最后读操作：每次操作在循环里直接处理或存入 `ops`。

接口：

```text
solve() -> 处理一组数据。
calc_sum(a,n) -> 顺序统计。
count_if_positive(a,n) -> 条件计数。
check(x) -> 判断一个元素或状态是否合法。
better(x,y) -> 排序/取最优时的比较规则。
struct Node -> 把多字段数据绑在一起。
```

输出能力：

- 输出统计值、最大最小值、分类结果。
- 输出排序后的对象编号。
- 输出每次操作后的状态。

下游可接：

- CPP-001 主骨架与 IO。
- CPP-003 排序与比较函数。
- BRUTE 暴力枚举。
- SIM-01 模拟与高精度。

可拼接模块：

- 数组扫描接 PrefixSum。
- 对象排序接 Greedy。
- `check(x)` 接二分答案。
- 循环枚举接暴力部分分。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Node {
    int id;
    ll x;
    ll y;
};

bool check_positive(ll x) {
    return x > 0;
}

ll calc_sum(const vector<ll> &a, int n) {
    ll sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += a[i];
    }
    return sum;
}

int count_positive(const vector<ll> &a, int n) {
    int cnt = 0;
    for (int i = 1; i <= n; i++) {
        if (check_positive(a[i])) {
            cnt++;
        }
    }
    return cnt;
}

bool better_node(const Node &a, const Node &b) {
    if (a.x != b.x) return a.x > b.x;
    if (a.y != b.y) return a.y < b.y;
    return a.id < b.id;
}

void solve() {
    int n;
    cin >> n;

    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    ll sum = calc_sum(a, n);
    int pos_cnt = count_positive(a, n);

    if (n == 0) {
        cout << "ZERO\n";
        cout << "0 0 0 0\n";
        return;
    }

    ll mx = a[1];
    int mx_pos = 1;
    for (int i = 2; i <= n; i++) {
        if (a[i] > mx) {
            mx = a[i];
            mx_pos = i;
        }
    }

    if (sum > 0) {
        cout << "POSITIVE\n";
    } else if (sum == 0) {
        cout << "ZERO\n";
    } else {
        cout << "NEGATIVE\n";
    }

    cout << sum << ' ' << pos_cnt << ' ' << mx << ' ' << mx_pos << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();

    return 0;
}
```

调用示例：

```cpp
// 顺序结构：按题面顺序读入、计算、输出。
ll sum = calc_sum(a, n);
cout << sum << '\n';

// 分支结构：先写最特殊的情况，再写普通情况。
if (n == 1) {
    cout << a[1] << '\n';
} else {
    cout << calc_sum(a, n) << '\n';
}

// 循环结构：数组题默认 1..n。
for (int i = 1; i <= n; i++) {
    if (a[i] % 2 == 0) cout << a[i] << '\n';
}

// 结构体：多字段排序时保留 id。
vector<Node> p(n + 1);
sort(p.begin() + 1, p.end(), better_node);
```

常见坑：

- 1-index 数组要开 `n + 1`，如果要访问 `r + 1` 就开 `n + 2`。
- `for (int i = 1; i <= n; i++)` 不要误写成 `i < n`。
- `if (x = 0)` 是赋值，判断相等必须写 `x == 0`。
- `else` 会匹配最近的未匹配 `if`，复杂分支一定加大括号。
- 求最大值时，如果数组可能全负，初值用 `a[1]` 或 `-INF`，不要默认 `0`。
- 自定义比较函数不能写 `<=`，相等时必须返回 `false`。
- 函数需要修改外部变量时传引用，不需要修改时传 `const &`。
- 多组数据时，全局数组、答案、容器要在每组重新初始化。

暴力/部分分替代：

- 正解不会时，先按题面逐步模拟，保证样例和小数据。
- `n <= 5000` 可先双重循环拿分。
- `n <= 10` 可枚举所有情况，之后再替换核心函数。
- 把暴力也写成 `brute()`，正解写成 `solve_fast()`，方便按数据范围分支。

升级方向：

```text
单循环统计 -> 前缀和/差分
双重循环找区间 -> PrefixSum / 双指针
多字段排序扫描 -> 贪心
check(x) 判断答案是否可行 -> 二分答案
```

最小测试样例：

```text
输入
5
-2 0 4 7 -1

输出
POSITIVE
8 2 7 4
```
