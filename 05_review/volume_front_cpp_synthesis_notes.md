# 前置卷与 C++ 卷综合备注

## 已完成汇总稿

| 文件 | 覆盖来源 | 状态 |
|---|---|---|
| `04_generated_drafts/volume_-1_0A_0_ops_route.md` | `OPS-00`、`ROUTE-00`、`ROUTE-01`、`OPS-01` | 已新建 |
| `04_generated_drafts/volume_1_cpp_stl.md` | `CPP-001` 到 `CPP-009` | 已新建 |

## 编写原则

这两份稿件没有重写模块源文件，只把已有模块压缩成可打印、可翻查的卷稿：

```text
目录 -> 使用说明 -> 核心表格 -> 按模块顺序摘要 -> 关键模板 -> 最小验错
```

风格保持“作战系统”：

```text
先路由，不讲长原理。
先部分分，再升级。
先统一接口，再拼模块。
先查语言坑，再提交。
```

## 覆盖检查

前置卷已覆盖：

| 要点 | 覆盖情况 |
|---|---|
| 全局 C++17 约束 | 已覆盖 |
| 图/数组/区间/查询/状态统一规则 | 已覆盖 |
| 标准 `Graph` 双视图 | 已覆盖 |
| `Array`、`Query`、`Compressor`、`State` | 已覆盖 |
| 统一函数名 | 已覆盖 |
| 题面信号路由 | 已覆盖 |
| 数据范围预算 | 已覆盖 |
| 操作类型路由 | 已覆盖 |
| 20 个拼接食谱 | 已用总表和高频骨架覆盖 |
| 3 小时时间策略 | 已覆盖 |
| 32 次提交策略 | 已覆盖 |
| 兜底输出 | 已覆盖 |

C++ 卷已覆盖：

| 要点 | 覆盖情况 |
|---|---|
| 主骨架与 IO | 已覆盖 |
| `vector/string/pair/tuple` | 已覆盖 |
| `sort/lambda/lower_bound/upper_bound` | 已覆盖 |
| `queue/deque/stack/priority_queue` | 已覆盖 |
| `set/multiset/map/unordered_map` | 已覆盖 |
| `bitset` 和位运算 | 已覆盖 |
| 坐标压缩 | 已覆盖 |
| `long long` / `__int128` 溢出处理 | 已覆盖 |
| 常见 RE/WA 坑 | 已覆盖 |

## 已知缺口

| 缺口 | 影响 |
|---|---|
| 前置卷只汇总了高频食谱骨架，没有逐条展开 R01-R20 的全部原文细节 | 纸质速查足够；若要完整说明，可继续从 `ROUTE-01` 扩写 |
| C++ 卷没有加入完整可运行的每个模块最小样例输出 | 保留了关键模板和坑表；样例仍可回源模块查 |
| 当前未运行代码编译抽取 | 两份汇总稿是 Markdown 汇编，代码块来自已有模块，未新增算法实现依赖 |

## 后续建议

合并最终总稿时，建议顺序为：

```text
volume_-1_0A_0_ops_route.md
volume_1_cpp_stl.md
volume_2_brute_memo_partial.md
volume_3_dp_model_reuse.md
volume_4_data_structures.md
后续图论、数学、字符串卷
```
