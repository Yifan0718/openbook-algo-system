# CPP-009 常见 RE/WA 语言坑清单

模块编号：CPP-009

模块名称：常见 RE/WA 语言坑清单

标签：RE、WA、越界、空容器、迭代器、初始化、多组数据、比较函数

一句话用途：提交前按清单扫一遍，优先排除语言层面的低级错误。

题面触发词：多组数据、边界、空集合、没有答案、字符串、动态删除、排序、哈希、递归。

什么时候用：代码写完后、样例过了但担心隐藏点时；出现 RE/WA/TLE 不知道从哪查时。

不要什么时候用：算法逻辑明显不对时不要只改语言细节；先确认模型、复杂度和边界。

复杂度：检查清单本身无复杂度；防御性判断通常 `O(1)`。

数据范围参考：数组大小接近上限、多组数据总量大、递归深度大、答案接近 `1e18` 时尤其要查。

依赖的标准容器：`vector`、`string`、`queue`、`stack`、`set`、`map`、`unordered_map`。

输入如何整理：每组数据都重新初始化容器；读字符串行前处理换行；数组按统一 1-index 开 `n + 1`。

接口：

- `empty()`：访问队首、栈顶、末尾前先判断。
- `assign(size, value)`：多组数据重置 `vector`。
- `clear()`：清空容器。
- `find()`：删除或解引用迭代器前先确认存在。
- `count()`：只判断是否存在。

输出能力：帮助定位错误类型，不直接产生题目答案。

下游可接：所有模块的提交前检查。

可拼接模块：CPP-001 主骨架、CPP-002 基础容器、CPP-005 关联容器、CPP-008 整数溢出。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;

        vector<ll> a;
        a.assign(n + 1, 0);
        for (int i = 1; i <= n; i++) cin >> a[i];

        stack<int> st;
        if (!st.empty()) {
            cout << st.top() << '\n';
        }

        set<int> s;
        s.insert(1);
        auto it = s.find(1);
        if (it != s.end()) {
            s.erase(it);
        }

        cout << a[n] << '\n';
    }

    return 0;
}
```

调用示例：

```cpp
// 边遍历边删除 map/set 的安全写法
for (auto it = s.begin(); it != s.end(); ) {
    if (need_delete(*it)) {
        it = s.erase(it);
    } else {
        ++it;
    }
}

// 多组数据重置邻接表
g.assign(n + 1, {});
dist.assign(n + 1, -1);
```

常见坑：

- 越界：1-index 数组要开 `n + 1`，循环别写到 `n + 1`。
- 空容器：`front/back/top` 前先判断 `empty()`。
- 字符串：`cin >> s` 不读空格，`getline` 前注意行尾换行。
- 多组数据：`vector/map/set/queue` 没清空会串数据。
- 比较函数：排序比较不能用 `<=`，相等时必须返回 `false`。
- 迭代器：删除后旧迭代器失效；按容器返回的新迭代器继续。
- `map[key]`：会创建新键；只查存在用 `find/count`。
- 哈希容器：遍历顺序不固定，不能依赖输出顺序。
- 整数：乘法先转 `long long` 或 `__int128`；答案变量不要用 `int`。
- 递归：深 DFS 可能栈溢出；可改显式栈或确认深度安全。
- 浮点：比较小数不要直接用 `==`，一般用误差。
- 下标混用：数组/图默认 1-index，字符串默认 0-index，写转换时标注清楚。

暴力/部分分替代：遇到 RE 先把可疑访问加边界判断；遇到 WA 先打印或手算极小样例验证索引。

升级方向：把本清单放到提交前流程；质检时可自动扫描大数组、空容器访问和禁止写法。

最小测试样例：

```text
输入
1
3
10 20 30

输出
30
```

