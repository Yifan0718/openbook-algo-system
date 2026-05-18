# CPP-001 C++17 主骨架与输入输出

模块编号：CPP-001

模块名称：C++17 主骨架与输入输出

标签：C++17、标准输入输出、多组数据、EOF、getline、统一类型

一句话用途：每道题先抄这一页，得到稳定的 `main + solve` 外壳和常用读入方式。

题面触发词：多组数据、直到输入结束、每行一个字符串、字符串可能含空格、输出每组答案、标准输入输出。

什么时候用：所有 C++17 题目开写前；需要统一 `long long`、换行、数组 1-index 和多组数据结构时。

不要什么时候用：交互题需要按题面及时刷新输出；题面明确给出完全不同的框架时。

复杂度：读入输出本身是 `O(输入规模 + 输出规模)`。

数据范围参考：数值、权值、答案、计数可能到 `1e18` 时用 `long long`；下标、点数、边数通常用 `int`。

依赖的标准容器：`vector`、`string`、`pair`；全卷统一 `ll = long long`。

输入如何整理：数组默认整理成 `vector<ll> a(n + 1)`，使用下标 `1..n`；字符串保留 C++ 默认 `0..len-1`。

接口：

- `void solve()`：处理一组数据。
- `int main()`：只负责加速 IO、选择单组/多组/EOF 模式、调用 `solve()`。
- `read_case()`：遇到 EOF 多组时可写成返回 `bool` 的读入函数。

输出能力：使用 `cout << ans << '\n'`；大量输出时也用 `'\n'`，避免频繁强制刷新。

下游可接：所有算法模块、数据结构模块、图论模块、DP 模块。

可拼接模块：CPP-002 基础容器、CPP-008 整数溢出、CPP-009 语言坑。

模板代码：

考场默认可以用 GNU g++ 时，第一行写：

```cpp
#include <bits/stdc++.h>
```

如果现场环境不支持 `bits/stdc++.h`，把它替换成下面这个“标准头文件安全包”。这组头文件覆盖本资料中常用的 STL 容器、算法、数学、格式化、字符串流、快读快写和断言。

```cpp
#include <algorithm>
#include <array>
#include <bitset>
#include <cassert>
#include <cctype>
#include <climits>
#include <cmath>
#include <complex>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <functional>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <limits>
#include <list>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <tuple>
#include <type_traits>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
```

头文件速查：

| 用到的东西 | 标准头 |
|---|---|
| `cin/cout/ios` | `<iostream>` |
| `printf/scanf/getchar/putchar` | `<cstdio>` |
| `vector/string/array/list/deque` | `<vector>`、`<string>`、`<array>`、`<list>`、`<deque>` |
| `queue/stack/priority_queue` | `<queue>`、`<stack>` |
| `set/map/unordered_map/unordered_set` | `<set>`、`<map>`、`<unordered_map>`、`<unordered_set>` |
| `sort/lower_bound/unique/min/max` | `<algorithm>` |
| `iota/accumulate/partial_sum/gcd/lcm` | `<numeric>` |
| `pair/tuple` | `<utility>`、`<tuple>` |
| `greater/function/hash` | `<functional>` |
| `bitset` | `<bitset>` |
| `numeric_limits/LLONG_MAX/INT_MAX` | `<limits>`、`<climits>` |
| `setw/setfill/setprecision/fixed` | `<iomanip>` |
| `stringstream` | `<sstream>` |
| `isdigit/tolower` | `<cctype>` |
| `sqrt/fabs` | `<cmath>` |
| `assert` | `<cassert>` |
| `make_unsigned` 快写模板 | `<type_traits>` |

完整主骨架：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

const int INF = 1000000000;
const ll LINF = 4'000'000'000'000'000'000LL;

void solve() {
    int n;
    cin >> n;

    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    ll sum = 0;
    for (int i = 1; i <= n; i++) sum += a[i];

    cout << sum << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();              // 单组数据

    return 0;
}
```

调用示例：

```cpp
// 题面写“第一行 T，表示 T 组数据”时，把 main 中的 solve() 换成：
int T;
cin >> T;
while (T--) {
    solve();
}

// 题面写“直到输入结束”时，常用写法：
int n, m;
while (cin >> n >> m) {
    // 处理这一组 n, m
}

// 题面有整行字符串且前面刚用过 cin >> x：
cin.ignore(numeric_limits<streamsize>::max(), '\n');
string line;
getline(cin, line);
```

常见坑：

- 如果 `#include <bits/stdc++.h>` 不可用，不要现场猜头文件；直接替换成上面的标准头文件安全包。
- 题面没有 `T` 时不要强读 `T`。
- `cin >> s` 读不到空格；含空格必须用 `getline(cin, s)`。
- `cin >> x` 后立刻 `getline`，要先用 `ignore` 吃掉行尾换行。
- `endl` 会刷新缓冲，大量输出时可能慢；普通换行用 `'\n'`。
- 不要依赖本地文件输入，OJ 默认使用标准输入输出。
- 不要写编译器私有优化指令；纸质模板以稳为主。
- 不要用宏把所有 `int` 替换成 `long long`，下标和容器大小仍用 `int` 更稳。

暴力/部分分替代：先把读入和输出跑通；不会算法时也先输出合法格式，避免格式错误。

升级方向：把 `solve()` 内部替换为暴力、记忆化、DP、图论或数据结构正解；`main` 通常不动。

最小测试样例：

```text
输入
3
10 20 30

输出
60
```
