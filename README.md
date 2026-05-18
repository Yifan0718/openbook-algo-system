# 纸质版算法作战系统 v0.2

一套面向 3 小时 3 题算法机考的纸质开卷资料包。核心目标不是系统讲算法原理，而是在考场中快速完成：

```text
读题 -> 判断数据范围和题型 -> 查路由表 -> 套 C++17 模块 -> 先交部分分 -> 再升级
```

核心设计原则：

- 主力语言：C++17。
- 默认标准输入输出，不使用文件读写。
- 默认图、数组、DP 等竞赛模板尽量采用 1-index。
- 资料以模块化拼接为目标，每个模块强调适用场景、复杂度、接口、完整代码、常见坑和部分分替代方案。
- DP 单独强化“从暴力 DFS 到记忆化，再到表推”的建模过程。

## 直接打印

推荐优先打开：

- `07_release/v0.2/01_print_ready/chapter_pdfs/00_which_book_index.pdf`：一页索引，考试时先看它决定翻哪本。
- `07_release/v0.2/01_print_ready/chapter_pdfs/06_math_string.pdf`：数学与字符串模板，已包含独立 `STR-05 Manacher`。
- `07_release/v0.2/01_print_ready/openbook_printable_full.pdf`：完整自包含总 PDF。

完整发布压缩包：

- `07_release/openbook-v0.2.zip`
- `07_release/openbook-v0.2.zip.sha256.txt`

## 分卷结构

| 编号 | 文件 | 内容 |
|---|---|---|
| 00 | `00_route.pdf` | 作战流程、题型路由、复杂度、提交策略 |
| 01 | `01_cpp_stl_io.pdf` | C++17、STL、输入输出 |
| 02 | `02_brute_memo.pdf` | 暴力、枚举、记忆化、部分分 |
| 03 | `03_dp.pdf` | DP 建模与模型复用 |
| 03A | `03A_greedy_dp.pdf` | 贪心与 DP 辨析 |
| 04 | `04_ds.pdf` | 数据结构 |
| 05 | `05_graph_tree.pdf` | 图论与树论 |
| 06 | `06_math_string.pdf` | 数学与字符串模板 |
| 07 | `07_debug.pdf` | 调试、对拍与训练 |
| 08 | `08_math_ref.pdf` | 竞赛数学参考 |
| 09 | `09_python.pdf` | Python 互补卷 |
| 10 | `10_ai.pdf` | AI 专题与特判模型 |

## 仓库目录

```text
00_management/        写作计划、整合记录
01_source_rules/     原始规则摘要和来源记录
02_blueprint/        顶层设计与模块拼接架构
03_modules/          模块化算法/数据结构源码文档
04_generated_drafts/ 分卷 Markdown 源稿
05_review/           构建、审计、测试脚本和报告
06_output/           构建输出 Markdown/PDF
07_release/          v0.2 发布目录和压缩包
```

## 构建与审计

详见 `BUILD.md`。

已记录的 v0.2 校验结果：

- v0.2 例题样例运行：`188/188` 通过。
- standalone C++ 编译：`265` 个去重单元，失败 `0`。
- standalone 运行用例：`102` 个，编译失败 `0`，运行失败 `0`。
- Python 代码块语法检查：失败 `0`。

## 发布状态

当前版本：

- 版本：v0.2。
- 许可证：MIT License。
- 状态：可公开发布，可直接打印使用。
