# CPP-008 long long 与 __int128 溢出处理

模块编号：CPP-008

模块名称：整数类型、乘法溢出与大整数中间量

标签：long long、__int128、溢出、取模、二分中点、距离无穷大

一句话用途：避免答案、乘法、距离和计数在中间过程爆掉导致 WA。

题面触发词：答案很大、方案数、权值到 `1e9`、乘积、平方、最短路距离、取模、二分答案、`1e18`。

什么时候用：权值/答案/计数可能超过 `int`，或两个 `long long` 相乘可能超过 `9e18` 时。

不要什么时候用：真正需要上百位整数时，C++ 内建类型不够，要按题意使用字符串高精或大整数思路。

复杂度：类型转换本身 `O(1)`；`__int128` 比普通整数慢一点，但考场中用于中间量很稳。

数据范围参考：`int` 约到 `2e9`；`long long` 约到 `9e18`；`1e9 * 1e9` 必须先转 `long long`；`1e18 * 1e18` 需要 `__int128` 中间量。

依赖的标准容器：无；常与 `vector<ll>`、图论距离数组、DP 数组拼接。

输入如何整理：点数、下标用 `int`；权值、距离、答案、方案数优先读入 `long long`；乘法比较时转 `__int128`。

接口：

- `using ll = long long`：常用整数答案类型。
- `using i128 = __int128_t`：大乘法中间量。
- `print_i128(x)`：输出 `__int128`。
- `l + (r - l) / 2`：安全二分中点。
- `LINF = 4'000'000'000'000'000'000LL`：距离无穷大哨兵。

输出能力：输出 `long long` 答案或 `__int128` 答案。

下游可接：最短路、DP、组合计数、二分答案、数学取模。

可拼接模块：CPP-001 主骨架、CPP-003 二分、图论 Dijkstra、数学快速幂。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using i128 = __int128_t;

const ll LINF = 4'000'000'000'000'000'000LL;

void print_i128(i128 x) {
    if (x == 0) {
        cout << 0;
        return;
    }
    if (x < 0) {
        cout << '-';
        x = -x;
    }
    string s;
    while (x > 0) {
        int digit = (int)(x % 10);
        s.push_back((char)('0' + digit));
        x /= 10;
    }
    reverse(s.begin(), s.end());
    cout << s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll a, b, limit;
    cin >> a >> b >> limit;

    i128 product = (i128)a * b;
    cout << (product <= (i128)limit ? "OK" : "OVER") << '\n';

    print_i128(product);
    cout << '\n';

    ll l = 0, r = limit;
    ll mid = l + (r - l) / 2;
    cout << mid << '\n';

    return 0;
}
```

调用示例：

```cpp
// 先转再乘
long long area = 1LL * width * height;

// 比较 a * b <= c，避免 a*b 溢出
if ((__int128)a * b <= c) {
    // safe
}

// 最短路松弛
if (dist[u] != LINF && dist[v] > dist[u] + w) {
    dist[v] = dist[u] + w;
}
```

常见坑：

- `int * int` 会先按 `int` 乘完再赋给 `long long`，必须写 `1LL * a * b`。
- `abs(x)` 遇到 `long long` 时注意函数重载，稳妥写 `llabs(x)` 或自己处理。
- 二分中点写 `(l + r) / 2` 可能溢出，稳妥写 `l + (r - l) / 2`。
- `LINF + w` 可能溢出，最短路松弛前先判断 `dist[u] != LINF`。
- `__int128` 不能直接 `cin/cout`，需要自己读写或只作中间比较。
- 取模乘法时，两个数都可能到 `1e18`，中间乘法用 `__int128` 再 `% mod`。

暴力/部分分替代：小数据可先用 `long long`，但一旦样例外数据范围接近 `1e18`，必须处理乘法中间量。

升级方向：接快速幂、组合计数、二分答案、几何面积、最短路距离。

最小测试样例：

```text
输入
1000000000000 1000000000000 1000000000000000000

输出
OVER
1000000000000000000000000
500000000000000000
```
