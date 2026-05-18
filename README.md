# 纸质版算法作战系统 v0.32

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

- `07_release/v0.32/01_print_ready/chapter_pdfs/00_which_book_index.pdf`：一页索引，考试时先看它决定翻哪本。
- `07_release/v0.32/01_print_ready/chapter_pdfs/12_zhongguancun_machine_exam_companion.pdf`：中关村机试必带，覆盖往年题专项、现场拼装卡片和救分路线。
- `07_release/v0.32/01_print_ready/chapter_pdfs/11_signoff_encyclopedia.pdf`：签到题百科，覆盖 Markov、常用数学、计算机常识、AI 术语、读程序和生活模拟。
- `07_release/v0.32/01_print_ready/chapter_pdfs/06_math_string.pdf`：数学与字符串模板，包含方程求解和 `STR-05 Manacher`。
- `07_release/v0.32/01_print_ready/openbook_printable_full.pdf`：完整自包含总 PDF。

完整发布压缩包：

- `07_release/openbook-v0.32.zip`
- `07_release/openbook-v0.32.zip.sha256.txt`

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
| 11 | `11_signoff_encyclopedia.pdf` | 签到题百科 |
| 12 | `12_zhongguancun_machine_exam_companion.pdf` | 中关村机试往年题专项与现场拼装卡片 |

## v0.32 新增重点

- 新增第 12 卷“中关村机试往年题专项与现场拼装卡片”。
- 覆盖 2025 春/夏/秋与 2026 冬共 12 道已整理往年题。
- 每题按题目信号、部分分、升级路线、正解推导、模块拼装和易错点组织。
- 新增 D1-D14 现场卡片：规则、节奏、32 次提交、复杂度、分数规划、套利 log 图、环形线段树、字符单射、混合输入、浮点、溢出、题面矛盾、部分分优先和最终检查。

## v0.31 修复重点

- 修复 v0.3 发布构建顺序问题：恢复 v0.2 中每卷的组合例题训练区。
- `openbook_full.pdf` / `openbook_printable_full.pdf` 从 v0.3 的 1172 页恢复并扩展到 1376 页。
- 分卷 00-10 恢复例题页数，同时保留第 11 卷 58 页签到题百科。
- `build_all_outputs.py` 已把 `integrate_v02_examples.py` 纳入构建链，防止以后全量构建再次覆盖例题区。

## v0.3 新增内容继续保留

- 新增第 11 卷“签到题百科”。
- 补充 Markov 性质、Markov 链、转移矩阵、平稳分布、HMM/MDP 路由。
- 补充现代 AI 术语：Token、Embedding、Attention、Transformer、RAG、向量检索。
- 补充计算机常识：进制、补码、浮点、字节序、内存、Cache、OS/网络/数据库、安全。
- 补充 NOIP/CSP 初赛式读程序、流程图、伪代码、递归栈和运算符优先级。
- 补充 SIM 方程求解：高斯消元、二分求根、牛顿法等。

## 仓库目录

```text
00_management/        写作计划、整合记录
01_source_rules/     原始规则摘要和来源记录
02_blueprint/        顶层设计与模块拼接架构
03_modules/          模块化算法/数据结构源码文档
04_generated_drafts/ 分卷 Markdown 源稿
05_review/           构建、审计、测试脚本和报告
06_output/           构建输出 Markdown/PDF
07_release/          v0.2/v0.3/v0.31/v0.32 发布目录和压缩包
```

## 构建与审计

详见 `BUILD.md`。

已记录的 v0.32 校验目标：

- 组合例题样例运行：`188/188` 通过。
- standalone C++ 去重单元：编译失败 `0`。
- 分卷 PDF：加入第 12 卷中关村机试专项。
- full/printable full PDF：`1376` 页。

## 发布状态

当前版本：

- 版本：v0.32。
- 许可证：MIT License。
- 状态：可公开发布，可直接打印使用。
