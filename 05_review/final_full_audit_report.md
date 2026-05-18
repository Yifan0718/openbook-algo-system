# 最终全量审计报告

时间：2026-05-18

目标：核验纸质开卷资料是否满足“全面、统一架构、模块化拼接、竞赛快速编码、1-index 优先、完整代码可运行”的要求。

## 结论

- WSL `g++` 可用：`g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`。
- 已重建全部生成稿、合并版、打印版和 PDF。
- `openbook_full.md` 与 `openbook_printable_full.md` 均包含 112 个模块全文。
- 完整独立 C++ 代码块已用 WSL `g++ -std=c++17 -O2 -pipe -Wall -Wextra` 编译通过。
- `cpp` 代码块伪代码扫描通过：0 个疑似伪代码。
- 禁止项扫描通过：未发现 `freopen`、`#pragma GCC optimize`、`#define int long long` 等禁用写法。
- 下标口径扫描通过：普通数组、图、网格、关键点未发现强制 0-index 的硬伤；字符串、bitmask、数学自然下标作为局部例外保留。
- 模块字段检查通过：112 个模块均无缺失字段。

## 本轮重点修复

- 统一将旧式 `(ll)4e18` / `(long long)4e18` 改为整数哨兵 `4'000'000'000'000'000'000LL` 或安全上限。
- 修复 `OPS-00` 主骨架 `solve()` 声明顺序，使完整骨架可编译。
- 将 WSL `g++` 纳入编译检查脚本，避免“本机无编译器就跳过”的假通过。
- 收紧伪代码扫描，`cpp` fence 中出现 `for ... in ...`、`sort(... by ...)` 等会直接失败。
- 修复/加固多处边界：空容器访问、Trie/AC 非小写越界、bitset 负下标、线段树空表、子集枚举位移、BFS 固定数组规模、贪心哨兵、CRT 溢出、容斥除零、矩阵负数取模等。
- DP 卷补强了 P1874、编辑距离、记忆化 DFS、LCIS、后效性升维例题，以及 DFS+记忆化从暴力升级到 DP 的考场策略。
- C++/STL/IO 卷补齐了 `scanf/printf`、`cin/cout`、快读快写、`fixed/setprecision`、`setw/right/left/setfill`、`string/vector/priority_queue/unordered_map` 等考场速查内容。

## 验证命令

```text
wsl.exe -- bash -lc 'g++ --version | head -n 1; uname -a; pwd'
python .\05_review\build_all_outputs.py
python .\05_review\scan_cpp_pseudocode.py
python .\05_review\scan_template_consistency.py
python .\05_review\scan_index_policy.py
python .\05_review\scan_forbidden_patterns.py
python .\05_review\check_module_fields.py
python .\05_review\extract_compile_cpp_blocks.py
python .\05_review\audit_cpp_blocks_wsl.py
```

## 生成产物

- `06_output/openbook_core.md`
- `06_output/openbook_core.pdf`
- `06_output/openbook_full.md`
- `06_output/openbook_full.pdf`
- `06_output/openbook_printable_full.md`
- `06_output/openbook_printable_full.pdf`

## 审计报告

- `05_review/cpp_compile_report.md`：完整独立代码块 WSL 编译报告。
- `05_review/cpp_wsl_audit_report.md`：模块代码块清单与 snippet 线索报告。
- `05_review/cpp_block_inventory.md`：全部 C++ 代码块分类清单。
- `05_review/index_policy_report.md`：1-index/下标口径审计。
- `05_review/template_consistency_report.md`：模板一致性审计。
- `05_review/cpp_pseudocode_report.md`：伪代码混入扫描。
- `05_review/forbidden_patterns_report.md`：禁用写法扫描。
- `05_review/module_fields_report.md`：模块字段完整性扫描。

## 备注

`audit_cpp_blocks_wsl.py` 中仍保留 snippet 包壳编译线索。当前 snippet 失败为 77 个，主要是“依赖同卷前置结构或题目变量”的函数片段，例如依赖 `Graph`、`LCA`、`n/m/a`、`memo` 的局部模板；这些不作为 release blocker。硬门槛是所有带 `int main()` 的完整代码块通过，结果为 0 个 standalone 失败。
