# 第三轮运行级全量审计报告

日期：2026-05-18

目标：逐个核验完整 C++ 程序是否能在本地编译并运行；继续检查资料是否满足“全面、统一架构、模块化拼接、竞赛快速编码”的要求。

## 结论

通过。

- 已把运行级门禁加入 `review_all.py`。
- 52 个唯一完整 `main` 程序全部使用 WSL `g++ -std=c++17 -O2 -pipe -Wall -Wextra -Werror` 编译。
- 52 个完整程序全部有 manifest 覆盖。
- 64 个运行用例全部通过。
- 生成稿与最终输出已重建。
- 总审计门禁 `review_all.py` 已通过。

## 新增门禁

- `05_review/standalone_runtime_manifest.json`
- `05_review/run_standalone_tests.py`
- `05_review/standalone_runtime_test_report.md`

运行门禁检查：

- 扫描 `03_modules`、`04_generated_drafts`、`06_output`。
- 对完整 `int main` 代码块按 digest 去重。
- manifest 缺失、过期 digest、编译失败、运行超时、非零退出、stdout 不匹配都会失败。
- 当前结果：`runtime_units=52 cases=64 missing=0 stale=0 compile_failures=0 runtime_failures=0`。

## 本轮修复

- `CPP-006`：负奇数判断从 `x % 2 == 1` 改成 `x % 2 != 0`。
- `DIVIDE-00`：倍增 `LOG` 从 `60` 调整为防御性 `63`，并加入 `2^60` 运行测试。
- `BRUTE-05`：`n > 22` 不再静默无输出，改为读完输入并输出合法兜底。
- `BRUTE-11`：普通网格 BFS 和钥匙状态 BFS 都加入 `S/T` 缺失保护。
- `BRUTE-12`：折半枚举位移改为 `1LL << len`。
- `CPP-10`：自写快读改为无符号累加，避免 `LLONG_MIN` 取负溢出。
- `MATH-03/MATHREF-02`：`inv_prime(0, mod)` 返回 `-1`。
- `MATH-04`：质数表不足时继续朴素试除，避免把合数当质数。
- `MATH-06/MATHREF-01/MATHREF-06`：修复极值取整和 `lcm_limit` 溢出风险。
- `MATHREF-03/04/05`：补齐空范围、位移、非正 SG move 等边界。
- `BRUTE-00/13/14`：明确部分分/兜底模板不是正解模板。
- `GREEDY-00`：明确闭区间选点与半开区间活动选择/会议室模型的区别。

## 数学片段探针

非 standalone 数学代码片段额外用临时程序验证：

- `inv_prime(0, 7) == -1`
- `lcm_limit(LLONG_MAX, LLONG_MAX - 1, LLONG_MAX) == LLONG_MAX`
- `factorize_by_primes(221, {2,3,5,7}) == 13^1 * 17^1`
- `floor_div(LLONG_MIN, 2)` 与 `ceil_div(LLONG_MAX, 2)` 正确
- `count_coprime_pairs(0, 5) == 0`
- `sg_take_stones(3, {0,1}) == 0 1 0 1`

见 `05_review/math_edge_probe_report.md`。

## 总门禁结果

`python .\05_review\review_all.py`

结果：`ALL REVIEW GATES PASSED`

关键报告：

- `cpp_pseudocode_report.md`：Findings 0
- `template_consistency_report.md`：hits 0
- `index_policy_report.md`：source_hits 0, generated_hits 0, freshness 0
- `second_round_standalone_compile_all.md`：standalone_units 52, failures 0
- `standalone_runtime_test_report.md`：runtime_units 52, cases 64, failures 0
- `second_round_module_matrix.md`：modules 112, missing 0

说明：`cpp_wsl_audit_report.md` 里仍有部分 snippet 包壳编译失败，这些是依赖上下文的讲解片段、接口片段或故意不完整的局部代码，不作为 standalone 程序；本轮对完整程序做了运行门禁，对数学关键片段做了额外边界探针。
