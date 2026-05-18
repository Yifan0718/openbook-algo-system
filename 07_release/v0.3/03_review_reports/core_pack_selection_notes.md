# 核心速查版筛选说明

Worker M 初稿。目标是为 `06_output/openbook_core.md` 做最前置的薄资料，不复制完整长模板，只筛选高频、救分、可拼接内容。

## 已阅读来源

| 来源 | 状态 | 用途 |
|---|---|---|
| `00_management/FINAL_WRITING_PLAN.md` | 已读 | 确认总目标、卷结构、统一约束 |
| `04_generated_drafts/volume_-1_0A_0_ops_route.md` | 已读 | 考场流程、题面路由、统一接口、提交检查 |
| `04_generated_drafts/volume_1_cpp_stl.md` | 已读 | C++17 骨架、类型和 STL 坑位 |
| `04_generated_drafts/volume_2_brute_memo_partial.md` | 已读 | 暴力、部分分、记忆化升级路径 |
| `04_generated_drafts/volume_3_dp_model_reuse.md` | 已读 | DP 路由、状态句式、初始化和循环方向 |
| `04_generated_drafts/volume_4_data_structures.md` | 已读 | 数据结构选择表和统一接口 |
| `04_generated_drafts/volume_5_graph_tree.md` | 已读 | Graph、图论路由、常用图食谱 |
| `04_generated_drafts/volume_6_math_string.md` | 已读 | 数学与字符串路由入口 |
| `04_generated_drafts/volume_7_debug_training.md` | 已读 | WA/RE/TLE、极端样例、自检清单 |
| `04_generated_drafts/volume_8_competition_math_reference.md` | 已读 | 竞赛数学知识参考入口 |

## 筛选原则

```text
1. 优先保留考场最先需要的判断动作：数据范围、题面信号、操作类型。
2. 优先保留能直接提高部分分的版本路线：合法输出、暴力、memo、正解升级。
3. 优先保留跨模块统一接口：Graph、Array、Query、Compressor、State、函数名。
4. 长模板只留最短骨架或核心循环，完整实现回对应分卷。
5. 低频或高复杂模板只留路由入口，避免核心版变厚。
```

## 已纳入核心版的内容

| 核心版章节 | 来源 | 选择理由 |
|---|---|---|
| 考场流程 | 前置卷、调试卷 | 最前页必须先控节奏和提交策略 |
| 复杂度预算 | 前置卷、暴力卷、DP 卷 | 路由第一依据，决定暴力还是优化 |
| 题面路由总表 | 前置卷、7 卷训练题 | 覆盖最常见模型选择 |
| C++17 骨架 | 第 1 卷 | 降低语言层面失误 |
| Graph 双视图 | 前置卷、第 5 卷 | 后续图论模块统一入口 |
| 数据结构接口名 | 前置卷、第 4 卷 | 方便不同模板拼接 |
| 暴力/memo 升级路径 | 第 2 卷、第 3 卷 | 保部分分的核心能力 |
| DP 路由和状态句式 | 第 3 卷 | 初学者最需要的复用入口 |
| 数据结构选择表 | 第 4 卷、第 7 卷 | 操作类型到模块的直接映射 |
| 图论选择表 | 第 5 卷、第 7 卷 | 边权、方向、树/DAG/MST 的路由 |
| 数学字符串入口 | 第 6 卷 | 保留高频入口，不展开长公式 |
| 提交前检查 | 前置卷、第 7 卷 | 防止最后阶段低级失分 |

## 有意删减或只留入口的内容

| 内容 | 处理 | 原因 |
|---|---|---|
| 每个模块的完整卡片格式 | 不收入核心版 | 过厚，且完整卷已有 |
| 完整 树状数组、SegmentTree、SparseTable、DSU 代码 | 只留接口和选择表 | 核心版目标是先选对模块 |
| 完整 LCA、SCC、Dinic、二分图匹配 | 只留图论路由 | 高频程度低于 BFS/Dijkstra/Kruskal/Topo |
| AC 自动机 | 只留低优先级入口 | 单模式优先 KMP，多模式复杂时再翻 |
| Manacher | 保留独立速查入口 | 回文长串/多询问时有明显实战价值 |
| 组合数、逆元、矩阵快速幂完整模板 | 只留路由入口 | 完整公式和细节放第 8 卷 |
| 大量模拟路由训练题 | 不逐题收入 | 已抽象进路由表和检查清单 |

## 后续核对

```text
完整卷合并后，应再核对：
  Graph 接口是否与最终第 5 卷一致
  数据结构接口名是否与最终第 4 卷一致
  DP 状态句式是否与最终第 3 卷一致
  禁止项和 C++17 约束是否仍一致
  第 8 卷数学参考是否保持“核心版只入口、完整版查细节”的分层
```

## 写入范围确认

本次只新建：

```text
06_output/openbook_core.md
05_review/core_pack_selection_notes.md
```

没有修改、删除或回退其他 worker 的文件。
