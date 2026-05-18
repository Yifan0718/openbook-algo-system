# 实现审计报告：考场速成与模块化拼接

审计人：Worker N

审计范围：

- `03_modules/*.md`
- `04_generated_drafts/*.md`

审计重点：1-index/0-index 标注、空间防御、Graph 双视图、数据结构接口、考场速抄复杂度、危险宏/文件 IO、记忆化状态完整性、DP 暴力/记忆化/表推路线、后续需要简化或补说明的模块。

结论概览：

- P0：未发现必须立即阻断合并的问题。
- P1：发现 5 类建议修复点，集中在 DP 与统一协议交界处。
- P2：整体约定执行较好，但有若干可接受提醒，适合主 Agent 收尾时统一补注。

## P0 必须修

无。

当前没有发现危险宏、文件 IO、明显会污染考试提交环境的依赖，也没有发现 Graph 主模板本身的 `G.g/G.edges/add_edge` 协议错误。

## P1 建议修

### P1-1：DP-17 数位 DP 的 memo 空间和缓存生命周期说明不足

证据：

- `03_modules/DP-17-digit-dp.md:37-38` 同时覆盖 `N <= 1e18` 和长字符串场景。
- `03_modules/DP-17-digit-dp.md:98` 建议区间写 `solve(R) - solve(L - 1)`。
- `03_modules/DP-17-digit-dp.md:125-126` 使用固定数组 `memo[20][100][2]`、`vis[20][100][2]`。
- 汇总稿同样出现在 `04_generated_drafts/volume_3_dp_model_reuse.md:3452-3453`、`:3513`、`:3540-3541`。

风险：

- 若 `K >= 100` 或 `N` 为长字符串，固定数组不够防御。
- 若 `solve(R)` 和 `solve(L-1)` 之间不清空 `vis/memo`，而 `len` 或状态范围变化，`tight=false` 缓存会复用到不同长度，可能 WA。

建议：

- 把示例改成 `vector` 按 `len + 1`、`K` 分配，或明确标注“此代码仅适用于 `N <= 1e18` 且 `K < 100`”。
- 在 `solve(N)` 骨架中显式重建 `digits` 并清空 `vis/memo`；继续保留“只缓存 `tight=false`”。

### P1-2：DP-08 分组背包文字说 1-index，但代码用 0-index

证据：

- `03_modules/DP-08-group-knapsack.md:48` 写“组编号统一 `1..G`”。
- `03_modules/DP-08-group-knapsack.md:116`、`:133` 用 `if (g == G) return 0`。
- `03_modules/DP-08-group-knapsack.md:148-150` 用 `for (int g = 0; g < G; g++)` 和 `groups[g]`。
- 汇总稿同样出现在 `04_generated_drafts/volume_3_dp_model_reuse.md:1648`、`:1716`、`:1733`、`:1748-1750`。

风险：

- 考场速抄时，如果按文字开 `groups(G + 1)` 且放入 `1..G`，代码会漏第 `G` 组并访问空的第 0 组。

建议：

- 优先按全书约定改成 1-index：`groups` 开 `G + 1`，DFS 终止为 `g == G + 1`，循环 `for (int g = 1; g <= G; g++)`。
- 若保留 0-index，则必须在“输入如何整理”处醒目标注“本模块组数组内部 0-index”。

### P1-3：DP-18 的 `树状数组最大值版.query(idx)` 与统一数据结构接口冲突

证据：

- `03_modules/DS-00-data-structure-routing.md:69-70` 统一 `prefix(pos)` 和 `query(l, r)`。
- `03_modules/DP-18-dp-with-data-structure-optimization.md:179-187` 定义 `树状数组最大值版`，其中 `query(int idx)` 实际表示前缀最大值。
- `03_modules/DP-18-dp-with-data-structure-optimization.md:206` 调用 `bit.query(p - 1)`。
- 汇总稿同样出现在 `04_generated_drafts/volume_3_dp_model_reuse.md:3810-3818`、`:3837`。

风险：

- `query(idx)` 容易和全书 `query(l,r)` 习惯冲突，降低模块互换性。

建议：

- 将 `树状数组最大值版.query(idx)` 改名为 `prefix(idx)`，调用处写 `bit.prefix(p - 1)`。
- 或在 DP-18 明确写“这是前缀 max 查询，不是区间 `query(l,r)`”。

### P1-4：树形 DP / DAG DP 使用裸 `g`，与 Graph 双视图协议不够统一

证据：

- `03_modules/DP-00-total-flow.md:56` 写“使用统一 `Graph` 或 `vector<vector<int>> g(n + 1)`”，留了双口径。
- `03_modules/DP-14-tree-dp.md:42` 依赖 `vector<vector<int>> g(n + 1)`，代码多处 `for (int v : g[u])`。
- `03_modules/DP-15-dag-dp.md:43` 依赖 `vector<vector<pair<int,ll>>> g`，代码多处 `for (auto [v,w] : g[u])`。
- 汇总稿同样在 `04_generated_drafts/volume_3_dp_model_reuse.md:85`、`:2831`、`:3040` 及后续代码中出现裸 `g`。

风险：

- 图论卷已经统一 `Graph`、`G.g`、`G.edges`，但 DP 卷在树和 DAG 处又回到局部 `g`，考场拼接时要手工翻译边结构。

建议：

- 主 Agent 选择一个口径：若坚持全书拼接，DP-14/15 示例改成 `const Graph& G` 并迭代 `G.g[u]`。
- 若为了速抄保留裸 `g`，需明确写“这是从 `G.g` 抽出的局部简写版本；与图论模块拼接时优先使用 `Graph`”。

### P1-5：DP-14 树形 DP 的记忆化版本容易弱化“状态完整才能缓存”

证据：

- `03_modules/DP-14-tree-dp.md:133-145` 的 `dfs_memo(int u, int p, int parentChosen)` 只用 `vis[u][parentChosen]` 缓存，没有把 `p` 放入 key。
- 汇总稿同样出现在 `04_generated_drafts/volume_3_dp_model_reuse.md:2922-2934`。
- 体系内已有总原则：`03_modules/BRUTE-15-brute-memo-pitfalls.md:117` 提醒状态遗漏。

风险：

- 对固定根树，`p` 可由根确定，代码通常能用；但模板没有先“定根/固定 parent”的显式步骤，读者容易把带 `p` 的 DFS 误当任意可缓存状态。
- 树形 DP 本身通常无重叠子问题，memo 版本并不比后序 DFS 更适合速抄，反而增加解释负担。

建议：

- 在 DP-14 里补一句：“本 memo 只在固定根后使用，`u` 的父亲唯一；换根或同一 `u` 可能带不同 `p` 时，`p/parent` 必须进状态或不要缓存。”
- 更简洁的方案是保留“暴力 DFS + 表推 DFS”，把 memo 版本降为提醒而非主模板。

## P2 可接受提醒

### P2-1：索引约定总体执行良好

- 数组、图、DP 表大多默认 1-index。
- 字符串模块明确使用 C++ 自然 0-index，并写了题面 1-index 转换。
- bitmask、子集枚举、矩阵快速幂、容斥条件数组等 0-index 例外多数已明确标注。
- 主要例外是 P1-2 的分组背包组编号。

### P2-2：空间防御总体够用

- 常见数组使用 `n + 1`，差分使用 `n + 2`，线段树使用 `4 * n + 4`。
- `DS-01` 的 `diff[r+1]` 已配 `n+2`。
- `DS-03` 的线段树空间符合防御习惯。
- 树状数组仍依赖调用方不传 0；训练卷已提示 `add(0,x)` 死循环。可考虑在树状数组模块再加一行“`pos` 必须从 1 开始”。

### P2-3：Graph 卷本身统一性较强

- `GRAPH-00` 的 `Graph` 同时维护 `G.g` 和 `G.edges`，`add_edge(u,v,w,directed=false)` 一致。
- BFS/DFS/Dijkstra/Topo/SCC/LCA 使用 `G.g`，Kruskal/Floyd/Bellman-Ford 使用 `G.edges`。
- Dinic 明确使用独立 `FlowGraph`，这是合理例外。
- 后续主要是把 DP-14/15 的裸 `g` 与该协议对齐。

### P2-4：危险宏、文件 IO、复杂依赖未见实质问题

- 未发现 `#define int long long`、`#pragma GCC optimize`、`freopen`、文件 IO、PBDS 等危险写法。
- 代码块里常见的是 `#include <bits/stdc++.h>`、`ios::sync_with_stdio(false)`、`using ll = long long`，符合 C++17 考场模板习惯。
- 既有 `05_review/forbidden_patterns_report.md` 也显示未在 C++ 代码块中发现禁止项。

### P2-5：DP 路线保留充分

- DP 模块普遍保留“暴力 DFS 版本 / 记忆化版本 / 表推版本 / 暴力或部分分替代 / 升级方向”。
- `04_generated_drafts/volume_3_dp_model_reuse.md` 对这条路线保留最完整，利于开卷查阅。
- 收尾时主要修 P1 中的几处例外，不需要重写 DP 体系。

### P2-6：低优先级或参考型模块可保持，但最终装订时应控篇幅

- `STR-04`、`GRAPH-10`、`MATHREF-*` 内容偏参考或低优先级，适合作为附录。
- 若最终材料强调“考场速成”，主 Agent 可在目录中继续突出低优先级标签，避免学生优先背 AC 自动机、Dinic、Lucas/CRT 等高复杂模板。

## 后续建议清单

建议主 Agent 优先处理：

1. `DP-17-digit-dp.md` 与 `volume_3_dp_model_reuse.md`：补 `solve()` 清空缓存与动态空间说明。
2. `DP-08-group-knapsack.md` 与 `volume_3_dp_model_reuse.md`：统一分组编号。
3. `DP-18-dp-with-data-structure-optimization.md` 与 `volume_3_dp_model_reuse.md`：把 `树状数组最大值版.query(idx)` 改成 `prefix(idx)` 或补强说明。
4. `DP-14-tree-dp.md`、`DP-15-dag-dp.md`、`DP-00-total-flow.md` 与 `volume_3_dp_model_reuse.md`：明确 Graph 口径，避免裸 `g` 和 `G.g` 双体系并列。
5. `DP-14-tree-dp.md`：弱化或补注树形 DP memo 的状态完整性条件。

总体评价：模板库已经基本符合“考场速成、简单模块化拼接”的方向；主要问题不是模板过度优雅，而是个别章节在“局部更短”和“全书统一接口”之间没有完全收口。
