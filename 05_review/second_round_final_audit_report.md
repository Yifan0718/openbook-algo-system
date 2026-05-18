# 第二轮最终审计报告

时间：2026-05-18（Asia/Shanghai）

结论：通过。资料包已经按“竞赛快速编码、1-index 优先、模块化拼接、完整代码可运行”的口径完成第二轮全量审计、修复、重建和门禁。

## 本轮重点修复

- 统一图论文字接口：源稿中不再使用 `directed=true / directed=false` 作为考场操作口径，改为 `G.add_directed(u, v)` / `G.add_undirected(u, v)`。
- 修复 Trie / AC 自动机插入时遇到非法字符会半插入的问题：先整串校验，再修改结构。
- 修复高精度 `mul_small` 对负数尤其 `LLONG_MIN` 的取负溢出风险：用 `__int128` 保存乘数绝对值和进位。
- 修复若干 WSL `g++ -Wall -Wextra -Werror` 下会报警的完整代码样例。
- 将状压 DP 表推循环统一为 `total = 1 << k; full = total - 1; mask < total`，避免 `mask <= full` 与 `full = 1 << k` 混淆。
- 新增自动核心版生成脚本 `build_core_markdown.py`，避免 `openbook_core.md` 成为手写旧稿。
- 新增总控门禁脚本 `review_all.py`，串联重建、扫描、字段矩阵、WSL 编译审计。

## 输出文件

- `06_output/openbook_core.md`
- `06_output/openbook_core.pdf`
- `06_output/openbook_full.md`
- `06_output/openbook_full.pdf`
- `06_output/openbook_printable_full.md`
- `06_output/openbook_printable_full.pdf`

## 机器门禁结果

- `review_all.py`：ALL REVIEW GATES PASSED。
- C++ 伪代码扫描：0 findings。
- 模板一致性扫描：0 hits。
- 下标与竞赛速写口径扫描：source_hits=0，generated_hits=0，freshness=0。
- 禁止项扫描：未在 C++ 代码块中发现 `freopen`、`#pragma GCC optimize`、`#define int long long`、文件 IO 等禁用项。
- 模块字段检查：通过。
- 第二轮模块矩阵：112 个模块，字段缺失模块数 0。
- 第二轮 standalone C++ 全位置编译：
  - 扫描 Markdown 文件：126
  - C++ fence 总数：3494
  - standalone fence 总数：315
  - 去重后 standalone 单元：52
  - 编译器：WSL `g++ -std=c++17 -O2 -pipe -Wall -Wextra -Werror`
  - 失败单元：0

## 人工审计备注

- `audit_cpp_blocks_wsl.py` 仍会列出若干 snippet 包壳失败，它们是依赖上下文的函数片段，例如依赖 `Graph`、`LCA`、`State` 或前文函数定义；这些不属于“完整可运行程序”。完整 `main` 程序已经由 standalone 编译门禁覆盖并全部通过。
- LCIS 已覆盖在 `DP-23-lis-lcs-variants.md`，并同步进入 DP 卷和最终输出。
- 字符串、mask 位号、数学自然下标保留局部例外；普通数组、图点、关键点、网格仍按 1-index 作为主口径。
