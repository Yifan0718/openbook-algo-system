# CPP-013 STL 容器成员函数速查

模块编号：CPP-013

模块名称：STL 容器成员函数速查

标签：STL、vector、deque、list、array、string、stack、queue、priority_queue、set、multiset、map、multimap、unordered_map、unordered_set、pair、tuple、iterator

一句话用途：在考场上快速确认 STL 容器该用哪个成员函数、复杂度大致是多少、哪些写法安全可抄。

题面触发词：数组、队列、栈、堆、集合、映射、去重、计数、前驱后继、哈希表、字符串、二元组、多元组、遍历删除。

什么时候用：已经知道算法方向，但卡在容器接口、删除写法、堆排序规则、哈希表预留空间或 `pair/tuple` 写法时。

不要什么时候用：需要自己实现线段树、树状数组、DSU、图算法主体时，本模块只提供 STL 接口速查，不替代算法模块。

复杂度：顺序容器按位置访问/插入删除不同；红黑树容器 `O(log n)`；哈希容器平均 `O(1)`；堆 `push/pop O(log n)`、`top O(1)`。

数据范围参考：`n <= 2e5` 时 STL 容器通常可用；哈希表大量插入前建议 `reserve` 和 `max_load_factor`；需要稳定最坏复杂度时优先有序容器。

依赖的标准容器：`vector`、`deque`、`list`、`array`、`string`、`stack`、`queue`、`priority_queue`、`set`、`multiset`、`map`、`multimap`、`unordered_map`、`unordered_set`、`pair`、`tuple`。

输入如何整理：

- 连续下标、DP 表、邻接表：优先 `vector`。
- 两端进出、单调队列、0-1 BFS：优先 `deque`。
- 先进先出：`queue`；后进先出：`stack`。
- 每次取最大/最小：`priority_queue`。
- 自动排序、去重、前驱后继：`set/map`。
- 只按 key 快速查找/计数：`unordered_map/unordered_set`。
- 多字段排序或存状态：`pair/tuple`，字段多且含义复杂时改 `struct`。

接口：

- 通用查询：`c.empty()`、`c.size()`。
- 端点访问：`c.front()`、`c.back()`；栈和堆用 `c.top()`。
- 清空：`c.clear()`；注意 `array` 没有 `clear()`。
- 改大小：`vector/string/deque` 常用 `resize()`；`array` 大小固定。
- 替换内容：`vector/string/deque/list` 可用 `assign()`。
- 预留容量：`vector/string/unordered_map/unordered_set` 常用 `reserve()`。

输出能力：输出容器元素、计数结果、映射值、堆顶、集合最小/最大值、排序后的记录字段。

下游可接：排序、二分、前缀和、BFS、Dijkstra、贪心、DP、离散化、扫描线、记忆化搜索。

可拼接模块：CPP-002 基础容器、CPP-003 排序二分、CPP-004 队列栈堆、CPP-005 关联容器、CPP-007 坐标压缩、CPP-009 常见 RE/WA。

## 顺序容器简表

| 容器 | 常用用途 | 常用接口 | 关键提醒 |
|---|---|---|---|
| `vector<T>` | 数组、表、邻接表、DP | `push_back`、`pop_back`、`back`、`resize`、`reserve`、`assign`、`clear` | 支持 `a[i]`；中间插删慢；扩容会使旧迭代器/引用/指针失效 |
| `deque<T>` | 两端队列、单调队列、0-1 BFS | `push_front`、`push_back`、`pop_front`、`pop_back`、`front`、`back` | 支持 `dq[i]`；两端快，中间插删仍不适合大量使用 |
| `list<T>` | 已知迭代器位置的频繁插删 | `push_back`、`push_front`、`insert`、`erase`、`sort`、`splice` | 不支持 `a[i]`；遍历只能用迭代器；算法题较少用 |
| `array<T, N>` | 固定小数组、方向数组 | `fill`、`front`、`back`、`begin`、`end`、`size` | 大小编译期固定；没有 `push_back/clear/resize` |
| `string` | 字符串、字符数组 | `push_back`、`pop_back`、`substr`、`find`、`resize`、`reserve`、`clear` | `size()` 是无符号类型；空串不能 `s[0]`、`front`、`back` |

## 通用成员函数速查

| 函数 | 作用 | 可抄写法 | 注意 |
|---|---|---|---|
| `empty()` | 是否为空 | `if (c.empty())` | 访问端点前先判空 |
| `size()` | 元素个数 | `int n = (int)c.size();` | 和 `int` 比较时常强转 |
| `clear()` | 清空元素 | `c.clear();` | `vector` 容量通常不变；`array` 没有 |
| `front()` | 第一个元素 | `int x = c.front();` | `vector/deque/list/array/string/queue` 支持，非空才可用 |
| `back()` | 最后一个元素 | `int x = c.back();` | `queue` 也有 `back()` |
| `top()` | 栈顶/堆顶 | `int x = st.top();` | 只用于 `stack/priority_queue` |
| `resize(n)` | 改变元素个数 | `a.resize(n + 1);` | 变大补默认值，变小删除尾部 |
| `resize(n, v)` | 改大小并指定新增值 | `a.resize(n, -1);` | 只影响新增元素，不会重置旧元素 |
| `reserve(n)` | 预留容量 | `a.reserve(n);` | 不改变 `size()`，不能直接访问新位置 |
| `assign(n, v)` | 替换为 `n` 个 `v` | `a.assign(n + 1, 0);` | 会清掉原内容 |
| `begin()/end()` | 半开区间迭代器 | `for (auto it = c.begin(); it != c.end(); ++it)` | `end()` 不是最后一个元素 |

## vector/deque/list/array/string 常用模板

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> a;
    a.reserve(n);              // 只预留容量，size 仍是 0
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        a.push_back(x);
    }

    a.resize(n + 1, 0);         // size 变为 n + 1，新增位置补 0
    a.assign(n + 1, -1);        // 整个 vector 变成 n + 1 个 -1
    a.clear();                  // size 变 0

    deque<int> dq;
    dq.push_back(1);
    dq.push_front(2);
    if (!dq.empty()) {
        cout << dq.front() << ' ' << dq.back() << '\n';
    }

    list<int> ls = {3, 1, 2};
    ls.sort();                  // list 不能用 sort(ls.begin(), ls.end())

    array<int, 4> dir = {0, 1, 0, -1};
    dir.fill(0);

    string s = "abc";
    s.push_back('d');
    cout << s.substr(1, 2) << '\n'; // 从下标 1 开始取 2 个字符，输出 bc

    return 0;
}
```

## stack/queue/priority_queue

| 容器 | 用途 | 插入 | 查看 | 删除 | 备注 |
|---|---|---|---|---|---|
| `stack<T>` | 后进先出 | `push(x)` | `top()` | `pop()` | 括号、DFS 模拟、撤销 |
| `queue<T>` | 先进先出 | `push(x)` | `front()` | `pop()` | BFS；也可 `back()` 看队尾 |
| `priority_queue<T>` | 默认最大堆 | `push(x)` | `top()` | `pop()` | 每次取最大 |
| `priority_queue<T, vector<T>, greater<T>>` | 最小堆 | `push(x)` | `top()` | `pop()` | 每次取最小 |

```cpp
stack<int> st;
st.push(1);
if (!st.empty()) {
    int x = st.top();
    st.pop();
}

queue<int> q;
q.push(1);
if (!q.empty()) {
    int u = q.front();
    q.pop();
}

priority_queue<int> max_heap;
max_heap.push(5);
max_heap.push(2);
cout << max_heap.top() << '\n'; // 5

priority_queue<int, vector<int>, greater<int>> min_heap;
min_heap.push(5);
min_heap.push(2);
cout << min_heap.top() << '\n'; // 2
```

## priority_queue 存 pair 与自定义排序

```cpp
using pii = pair<int, int>;

// pair 默认字典序：先比较 first，再比较 second。
// 最小堆常用于 Dijkstra：{距离, 点}
priority_queue<pii, vector<pii>, greater<pii>> pq;
pq.push({0, 1});
while (!pq.empty()) {
    auto [d, u] = pq.top();
    pq.pop();
}

struct Node {
    int dist, id;
};

struct Cmp {
    bool operator()(const Node& a, const Node& b) const {
        if (a.dist != b.dist) return a.dist > b.dist; // dist 小的优先
        return a.id > b.id;                           // id 小的优先
    }
};

priority_queue<Node, vector<Node>, Cmp> heap;
heap.push({3, 2});
heap.push({1, 5});
```

## set/multiset

| 容器 | 特点 | 常用接口 | 适合场景 |
|---|---|---|---|
| `set<T>` | 自动排序，自动去重 | `insert`、`erase`、`find`、`count`、`lower_bound`、`upper_bound` | 去重、有序遍历、前驱后继 |
| `multiset<T>` | 自动排序，允许重复 | 同 `set` | 动态维护一堆数，重复值要保留 |

```cpp
set<int> s;
s.insert(3);
s.insert(1);

if (s.count(3)) {
    cout << "exist\n";
}

auto it = s.lower_bound(2);     // 第一个 >= 2
if (it != s.end()) cout << *it << '\n';

// 前驱：严格小于 x 的最大值
int x = 3;
auto p = s.lower_bound(x);
if (p != s.begin()) {
    --p;
    cout << *p << '\n';
}

multiset<int> ms;
ms.insert(5);
ms.insert(5);

// multiset 只删除一个 5
auto one = ms.find(5);
if (one != ms.end()) {
    ms.erase(one);
}

// ms.erase(5) 会删除所有 5
```

## map/multimap

| 容器 | 特点 | 常用接口 | 适合场景 |
|---|---|---|---|
| `map<K, V>` | key 自动排序且唯一 | `mp[k]`、`insert`、`find`、`count`、`erase`、`lower_bound` | 映射、计数、有序 key 查询 |
| `multimap<K, V>` | key 自动排序且可重复 | `insert`、`equal_range`、`find`、`erase` | 一个 key 对应多条记录且需要有序 |

```cpp
map<string, int> cnt;
cnt["alice"]++;

if (cnt.find("bob") == cnt.end()) {
    cout << "bob not found\n";
}

for (auto [key, value] : cnt) {
    cout << key << ' ' << value << '\n';
}

multimap<int, string> mm;
mm.insert({90, "alice"});
mm.insert({90, "bob"});

auto range = mm.equal_range(90);
for (auto it = range.first; it != range.second; ++it) {
    cout << it->first << ' ' << it->second << '\n';
}
```

## unordered_map/unordered_set

| 容器 | 特点 | 常用接口 | 适合场景 |
|---|---|---|---|
| `unordered_set<T>` | 哈希集合，不保证顺序 | `insert`、`erase`、`find`、`count`、`reserve`、`max_load_factor` | 快速判重、存在性 |
| `unordered_map<K, V>` | 哈希映射，不保证顺序 | `mp[k]`、`find`、`count`、`erase`、`reserve`、`max_load_factor` | 快速计数、快速查值 |

```cpp
int n;
cin >> n;

unordered_map<long long, int> cnt;
cnt.max_load_factor(0.7);
cnt.reserve(n * 2 + 1);

for (int i = 1; i <= n; i++) {
    long long x;
    cin >> x;
    cnt[x]++;
}

unordered_set<int> seen;
seen.max_load_factor(0.7);
seen.reserve(n * 2 + 1);

seen.insert(10);
if (seen.find(10) != seen.end()) {
    cout << "seen\n";
}
```

## pair/tuple

```cpp
using pii = pair<int, int>;
using tiii = tuple<int, int, int>;

pii p = {3, 5};
cout << p.first << ' ' << p.second << '\n';

auto [x, y] = p;

tuple<int, int, long long> state = {1, 2, 100LL};
auto [i, j, val] = state;

vector<pair<int, int>> v = {{2, 3}, {1, 9}, {1, 4}};
sort(v.begin(), v.end());       // 默认先 first 升序，再 second 升序

// 自定义排序：first 升序；first 相同时 second 降序
sort(v.begin(), v.end(), [](const pii& a, const pii& b) {
    if (a.first != b.first) return a.first < b.first;
    return a.second > b.second;
});
```

## 迭代器遍历与 erase 安全写法

```cpp
// vector/string/deque/list/set/map/unordered_* 通用：erase 返回下一个合法迭代器
for (auto it = c.begin(); it != c.end(); ) {
    if (need_delete(*it)) {
        it = c.erase(it);
    } else {
        ++it;
    }
}
```

```cpp
// map/unordered_map 删除时，元素是 pair<const K, V>
for (auto it = mp.begin(); it != mp.end(); ) {
    if (it->second == 0) {
        it = mp.erase(it);
    } else {
        ++it;
    }
}
```

```cpp
// 不要在 range-for 中直接 erase 当前容器
// 错误示例：
// for (int x : v) {
//     if (x < 0) v.erase(...);
// }

// vector 按条件删除的可靠写法
v.erase(remove(v.begin(), v.end(), value), v.end());

v.erase(remove_if(v.begin(), v.end(), [](int x) {
    return x < 0;
}), v.end());
```

## 常用完整模板

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
const int MAXN = 200000 + 5;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    static int sorted[MAXN];

    unordered_map<int, int> cnt;
    cnt.max_load_factor(0.7);
    cnt.reserve(n * 2 + 1);

    priority_queue<pii, vector<pii>, greater<pii>> min_heap;
    set<int> unique_values;

    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        sorted[i] = x;
        cnt[x]++;
        unique_values.insert(x);
        min_heap.push({x, i});
    }

    sort(sorted + 1, sorted + n + 1);

    while (!min_heap.empty()) {
        auto [value, id] = min_heap.top();
        min_heap.pop();
        cout << value << ' ' << id << '\n';
    }

    return 0;
}
```

调用示例：

```cpp
// 1-index 数组：上限明确时优先静态数组
static int a[MAXN];
for (int i = 1; i <= n; i++) cin >> a[i];

// 邻接表：上限明确时直接静态数组，每个点一个 vector
static vector<int> g[MAXN];
g[u].push_back(v);

// 固定方向数组
array<int, 4> dx = {-1, 0, 1, 0};
array<int, 4> dy = {0, 1, 0, -1};

// map 的 lower_bound：第一个 key >= x
auto it = mp.lower_bound(x);
if (it != mp.end()) {
    cout << it->first << ' ' << it->second << '\n';
}
```

常见坑：

- `front/back/top` 前必须先确认非空。
- `reserve(n)` 只改容量，不改元素个数；写完 `reserve` 后不能用 `a[i] = x` 填新元素。
- `resize(n, v)` 只给新增位置填 `v`，旧位置不会被重置。
- `assign(n, v)` 会替换整个容器内容，旧内容全部消失。
- `clear()` 后 `size()` 为 0，但 `vector/string` 的容量通常还在。
- `array` 大小固定，没有 `push_back`、`pop_back`、`clear`、`resize`。
- `priority_queue` 默认最大堆；小根堆写 `priority_queue<T, vector<T>, greater<T>>`。
- `pair` 默认排序是字典序，先 `first` 后 `second`。
- `set/map` 的 `lower_bound` 是按有序 key 查；`unordered_map/unordered_set` 没有 `lower_bound`。
- `unordered_map/unordered_set` 大量插入前，推荐先 `max_load_factor(0.7)` 再 `reserve(n * 2 + 1)`。
- `mp[key]` 会在 key 不存在时创建默认值；只判断存在用 `find` 或 `count`。
- `multiset.erase(x)` 删除所有等于 `x` 的元素；只删一个要先 `find`，存在再 `erase(it)`。
- 遍历时删除元素要写 `it = c.erase(it)`，不要在 range-for 中删除当前容器。
- `string::find()` 找不到时返回 `string::npos`，不要拿它和 `-1` 混用。
- `list` 不支持随机访问，也不能用普通 `sort(begin, end)`，要用成员函数 `ls.sort()`。

暴力/部分分替代：小数据可以用 `vector` 存全部元素，每次线性扫描、排序或手动删除；确认思路后再替换成 `set/map/unordered_map/priority_queue`。

升级方向：哈希计数接记忆化搜索；`set/map` 接扫描线和离线查询；`priority_queue` 接 Dijkstra、贪心合并；`vector` 接前缀和、树状数组、线段树和 DP。

最小测试样例：

```text
输入
3
5 2 5

输出
2 2
5 1
5 3
```
