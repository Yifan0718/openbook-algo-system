# 第 5 卷图论与树合成说明

Worker：L

写入文件：

- `04_generated_drafts/volume_5_graph_tree.md`
- `05_review/volume_5_graph_synthesis_notes.md`

## 已阅读来源

- `00_management/FINAL_WRITING_PLAN.md`
- `03_modules/GRAPH-00-standard-graph.md`
- `03_modules/GRAPH-01-dfs-bfs-connectivity.md`
- `03_modules/GRAPH-02-unweighted-bfs-shortest.md`
- `03_modules/GRAPH-03-dijkstra-path-multisource.md`
- `03_modules/GRAPH-04-floyd-bellman-spfa.md`
- `03_modules/GRAPH-05-topo-dag-dp.md`
- `03_modules/GRAPH-06-dsu-kruskal.md`
- `03_modules/GRAPH-07-bipartite.md`
- `03_modules/GRAPH-08-scc.md`
- `03_modules/GRAPH-09-tree-dfs-lca.md`
- `03_modules/GRAPH-10-dinic-low-priority.md`

## 合成原则

- 未修改任何 `03_modules/GRAPH-*.md` 源模块。
- 保留既有第 5 卷草稿的路由表、标准 `Graph`、拼接食谱和 60 秒检查清单。
- 在卷稿末尾补充更适合纸质开卷使用的内容：双视图速查、方向与权值限制、按题型摘要、关键模板、部分分替代、最小验错样例包、模块接线图。
- 汇总稿中的代码片段尽量沿用源模块函数名和核心逻辑，但做了压缩，不替代源模块的完整模板。

## 已覆盖要求

- 图论路由表：见 `5.1`。
- 标准 `Graph` 使用说明：见 `5.2`。
- `G.g` / `G.edges` 双视图：见开头约定、`5.6`、`5.11`。
- 何时有向/无向：见 `5.2` 建图场景、`5.7`。
- 负边限制：见 `5.1`、`5.3` 负权边最短路、`5.7`、`5.8.4`。
- 按题型组织的模块摘要：见 `5.8.1` 到 `5.8.10`。
- 关键模板：见 `5.8` 各小节。
- 部分分替代：见 `5.3` 各食谱、`5.8` 各题型、`5.9`。
- 最小验错：见 `5.3` 各食谱、`5.8` 各题型、`5.10`。
- Dinic 低优先级且不使用标准 `Graph`：见 `5.1`、`5.5`、`5.8.10`、`5.11`。

## 需要后续总合并注意

- `volume_5_graph_tree.md` 现在是汇总稿，不是逐模块全集；若最终版需要“完整模板代码”，建议在排版时把 `03_modules/GRAPH-*.md` 作为附录或源码目录引用。
- 汇总稿中的代码块包含片段式模板，依赖全局 `ll`、`LINF`、`Graph`、若干结果结构体和完整模块定义；不应单独抽取每个片段直接编译。
- `Topo` 的入度统计使用 `G.edges`，要求输入为有向边；若用户把无向边放入 DAG 模块，结果会失真，卷稿已强调。
- `SCC`、`LCA`、`Dinic` 源模块存在递归深度或残量网络等实现细节风险，汇总稿只做考场提醒，没有展开替代实现。
- 最大流、费用流、动态 MST、重链剖分、Hopcroft-Karp、最小费用最大流均只作为升级方向或低优先级提示，没有展开完整章节。

## 缺口

- 没有新增独立可编译的 `graph_templates.cpp`。
- 没有对所有汇总稿代码块做编译抽取，因为新增内容中包含依赖上下文的片段。
- 没有渲染 PDF 或做最终排版检查。
