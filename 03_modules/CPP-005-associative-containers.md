# CPP-005 set/multiset/map/unordered_map

模块编号：CPP-005

模块名称：有序集合、可重集合、映射和哈希映射

标签：set、multiset、map、unordered_map、计数、去重、有序查找

一句话用途：处理去重、计数、动态有序查找、键值映射和快速按键访问。

题面触发词：去重、出现次数、字典、映射、动态插入删除、第一个不小于、前驱后继、按名字统计、按值分组。

什么时候用：需要自动排序、自动去重、保存键到值的关系，或需要快速判断某个键是否出现时。

不要什么时候用：只需要连续下标数组时不要用 `map`；需要区间和/排名且数据很大时考虑坐标压缩 + 树状数组。

复杂度：`set/multiset/map` 插入删除查找 `O(log n)`；`unordered_map` 平均 `O(1)`，最坏情况可能退化。

数据范围参考：`2e5` 级别动态有序操作用红黑树容器稳；键是字符串或大整数且只需查值时可用哈希映射。

依赖的标准容器：`set`、`multiset`、`map`、`unordered_map`、`string`、`vector`。

输入如何整理：把需要查重/计数的值作为 key；若 key 是大坐标且后续要接数组结构，优先先压缩。

接口：

- `s.insert(x)`：插入。
- `s.erase(x)`：删除所有等于 `x` 的元素，`set` 中最多一个。
- `auto it = ms.find(x); if (it != ms.end()) ms.erase(it);`：`multiset` 只删一个 `x`。
- `s.lower_bound(x)`：第一个 `>= x`。
- `mp[key]++`：计数，但会创建默认值。
- `mp.count(key)`：判断 key 是否存在。

输出能力：输出去重后的有序序列、某值出现次数、某键对应答案、前驱后继。

下游可接：离散化、扫描线、贪心、模拟、记忆化搜索。

可拼接模块：CPP-003 排序二分、CPP-007 坐标压缩、CPP-009 语言坑。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    set<int> unique_values;
    multiset<int> bag;
    map<string, int> name_count;
    unordered_map<int, int> fast_count;
    fast_count.reserve(n * 2 + 1);
    fast_count.max_load_factor(0.7);

    for (int i = 1; i <= n; i++) {
        int x;
        string name;
        cin >> x >> name;

        unique_values.insert(x);
        bag.insert(x);
        name_count[name]++;
        fast_count[x]++;
    }

    int query_x;
    cin >> query_x;
    auto it = unique_values.lower_bound(query_x);

    cout << (int)unique_values.size() << '\n';
    if (it == unique_values.end()) cout << -1 << '\n';
    else cout << *it << '\n';
    auto it_cnt = fast_count.find(query_x);
    cout << (it_cnt == fast_count.end() ? 0 : it_cnt->second) << '\n';

    return 0;
}
```

调用示例：

```cpp
// multiset 只删除一个 x
auto it = ms.find(x);
if (it != ms.end()) {
    ms.erase(it);
}

// map 按 key 从小到大遍历
for (auto [key, value] : mp) {
    cout << key << ' ' << value << '\n';
}

// set 前驱：严格小于 x 的最大值
auto it = s.lower_bound(x);
if (it != s.begin()) {
    --it;
    int predecessor = *it;
}
```

常见坑：

- `mp[x]` 会在 `x` 不存在时创建键；只判断存在性用 `count` 或 `find`。
- `multiset.erase(x)` 会删除所有 `x`；只删一个要先 `find`，存在再 `erase(it)`。
- `unordered_map` 没有顺序，不能找前驱后继，也不能 `lower_bound`。
- `set` 中元素不能直接修改；要先删除旧值，再插入新值。
- 迭代器到 `begin()` 时不能再 `--it`。
- 需要第 k 小、动态排名时，普通 STL 不直接支持，常转坐标压缩 + 树状数组。

暴力/部分分替代：小数据用 `vector` 存所有元素，每次排序/扫描查找，复杂度较高但容易写。

升级方向：值域大且要排名时接 Compressor + 树状数组；复杂状态缓存接 `map<tuple<...>, value>`。

最小测试样例：

```text
输入
4
5 a
2 b
5 a
8 c
4

输出
3
5
0
```
