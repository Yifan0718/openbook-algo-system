# 资料包质量检查清单

## 1. 总体目标检查

资料必须服务于以下考场动作：

```text
读题 -> 看数据范围 -> 看题面信号 -> 找食谱 -> 整理成标准容器 -> 拼模块 -> 先交部分分 -> 升级
```

不合格信号：

- 只有算法名，没有题面触发词。
- 只有代码，没有接口和调用示例。
- 只有正解，没有暴力/部分分版本。
- 讲太多原理证明，缺少考场操作步骤。
- 同类模块接口不一致，例如一会儿 `ask`，一会儿 `query`。

## 2. 单模块字段检查

每个模块应包含：

```text
模块编号：
模块名称：
标签：
一句话用途：
题面触发词：
什么时候用：
不要什么时候用：
复杂度：
数据范围参考：
依赖的标准容器：
输入如何整理：
接口：
输出能力：
下游可接：
可拼接模块：
模板代码：
调用示例：
常见坑：
暴力/部分分替代：
升级方向：
最小测试样例：
```

允许少数字段在速查表中合并，但正文模块不能缺少：

- 题面触发词。
- 什么时候用。
- 不要什么时候用。
- 复杂度。
- 依赖的标准容器。
- 接口。
- 常见坑。
- 暴力/部分分替代。

## 3. 统一接口检查

### 全局约定

- 图默认 1-index。
- 数组默认 1-index。
- 区间默认闭区间 `[l, r]`。
- 字符串默认 C++ 0-index，必要时显著标注。
- bitmask 默认 0-index，必须显著标注元素编号 `0..n-1`。
- 点编号、下标、数量用 `int`。
- 权值、距离、答案、计数优先用 `long long`。
- 数组空间允许防御性开大：`n + 1`、`n + 2`、`n + 5`、线段树 `4*n + 4/5`。
- 考场优先“少想、少改、能拼接”，不追求最短或最优雅代码。
- 现代 C++ 特性可以用，但只在能降低考场编码难度时使用，例如 `auto`、结构化绑定、lambda 比较函数、`iota`、范围 `for`。
- 不为了展示语言新特性而增加复杂度；避免模板元编程、过度泛型封装、难以抄写的抽象。
- ACM/机考速写允许并推荐统一骨架使用 `using namespace std;`，减少抄写量和命名噪音。
- 不按大型工程规范禁止 `using namespace std;`，本资料以标准输入输出、单文件提交、快速得分为目标。

### 函数命名

统一使用：

```text
init
build
add
add_edge
setv
range_add
query
prefix
at
```

需要警惕：

- `ask/get/sum/rangeAdd/modify/update` 混用。
- `addEdge` 与 `add_edge` 混用。最终资料建议统一为 `add_edge`。
- 区间写成半开 `[l, r)` 但没有显著标注。

## 4. Graph 一致性检查

标准 Graph：

```cpp
struct AdjEdge {
    int to;
    ll w;
    int id;
};

struct FullEdge {
    int from, to;
    ll w;
    bool directed;
};

struct Graph {
    int n;
    vector<vector<AdjEdge>> g;
    vector<FullEdge> edges;
    void init(int n_);
    void add_undirected(int u, int v, ll w = 1);
    void add_directed(int u, int v, ll w = 1);
};
```

检查点：

- BFS/DFS/Dijkstra/Topo/SCC/LCA 使用 `G.g`。
- Kruskal/Floyd/Bellman-Ford 使用 `G.edges`。
- 无权边默认 `w = 1`。
- 无向图用 `add_undirected`，有向图用 `add_directed`。
- Dijkstra 明确禁止负权。
- Kruskal 明确通常用于无向图。
- LCA 明确要求树。

## 5. 数据结构一致性检查

检查点：

- `PrefixSum` 支持 `build(a)`, `prefix(i)`, `query(l,r)`。
- `树状数组` 支持 `init(n)`, `build(a)`, `add(pos,val)`, `prefix(pos)`, `query(l,r)`, `at(pos)`。
- `Difference` 支持 `build(a)`, `range_add(l,r,val)`, `restore()`。
- `Compressor` 压缩后编号从 1 开始。
- 坐标范围查询使用 `lower_id(L)` 与 `upper_id(R)`，不要假设端点出现过。
- 线段树统一 `query(l,r)`，区间修改统一 `range_add(l,r,val)`。

## 6. 第 2 卷记忆化检查

必须覆盖：

- 什么时候用记忆化。
- 状态能否缓存的判断：同样参数，答案是否永远一样。
- 状态遗漏风险：`last/mask/cnt/used/path`。
- 暴力 DFS -> memo 的固定改造流程。
- `vector` memo。
- `map<tuple,...>` memo。
- `unordered_map` 编码 memo。
- 最大值/最小值/方案数/可行性模板。
- 非法状态、终止状态、查 memo 的推荐顺序。
- 有环状态风险。
- 与 DP 卷关系：记忆化是抢分版本，表推是进一步升级。

## 7. DP 模型检查

每个 DP 模型必须有：

- 题面触发词。
- 数据范围信号。
- 状态句式。
- 初始化。
- 转移模板。
- 答案位置。
- 循环顺序。
- 暴力 DFS 版本。
- 记忆化版本。
- 表推版本。
- 常见坑。
- 可拼接模块。

DP 卷前三页必须包含：

```text
DP 路由表
状态句式库
DFS -> 记忆化 -> 表推 DP 升级图
```

## 8. 禁止项检查

资料代码中不得出现：

```text
freopen
#pragma GCC optimize
#define int long long
system(
ifstream
ofstream
fopen
```

允许在“不要使用”说明中出现这些词，但代码块中不得出现。

## 9. 代码块检查

后续脚本应执行：

1. 扫描所有 Markdown。
2. 抽取 fenced `cpp` 代码块。
3. 对包含 `int main(` 或明确标记 `// standalone` 的代码块尝试 C++17 编译。
4. 对所有代码块扫描禁止项。
5. 报告文件、代码块编号、错误原因。

## 10. 打印版检查

生成 PDF 后检查：

- 页眉/页脚含卷名和模块编号。
- 代码块没有截断。
- 表格没有严重跨页破碎。
- 路由表和食谱在前置卷中容易翻。
- 核心版不被低频高级算法污染。
- 完整版保留高级模块，但放后面。

## 11. 考场速成实现审计

重点不是代码风格优美，而是：

```text
1-index 优先
空间防御性足够
接口名字统一
模块依赖少
从题面到标准容器的步骤明确
暴力/记忆化/正解能逐步替换
```

需要警惕：

- 模板为了泛型过度复杂。
- 同一个概念出现多套命名。
- 使用 0-index 但没提醒。
- `vector` 大小刚好卡边界，没有给 `n+2/n+5`。
- 图论模块绕开标准 `Graph` 自己建一套。
- 线段树懒标记模板没有明确闭区间。
- 记忆化模板没有强调“状态完整才能缓存”。
