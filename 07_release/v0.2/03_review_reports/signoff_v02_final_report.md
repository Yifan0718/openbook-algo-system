# v0.2 Signoff 核验报告

核验日期：2026-05-18

结论：可以发布 v0.2。最终源稿、主 PDF、分卷 PDF、例题代码、模块字段、索引口径和审计报告均已重新生成并通过检查。

## 本轮修复

- 全部用户可见资料中移除旧英文树状数组术语，正文统一改为“树状数组”；代码类名统一改为 `BIT`，差分版为 `BITDiff`，双树状数组为 `RangeBIT`。
- 重新生成主 Markdown、总 PDF、分卷 PDF、分卷索引和例题测试代码，并确认当前源稿/输出/审计报告中无旧术语残留。
- 将图论桥边例题中的边号字段从 `id` 改为 `eid`，避免和旧 Graph 适配器残留写法混淆。
- 将 Floyd 例题从 `vector<vector<ll>> dist` 改为防御性静态数组 `dista[MAXN][MAXN]`，保持 1-index 和竞赛速写口径。
- 修复一个 `scanf` 返回值未检查导致的 `-Werror` 编译问题。
- 修复一个 KNN 例题中未使用变量导致的 `-Werror` 编译问题，并改成可读的完整代码。
- 将 SIM-04 JSON 解析器的 `\uXXXX` 从占位处理升级为 UTF-8 输出，支持代理对。
- 更新历史运行测试 manifest，新增 JSON Unicode 转义回归用例。
- 调整旧 WSL 片段审计报告：依赖上下文的 snippet 不再标成完整程序失败。

## 自动核验结果

| 项目 | 结果 |
|---|---|
| v0.2 例题样例运行 | 204 / 204 通过 |
| standalone C++ 去重编译 | 262 / 262 通过 |
| 逐块 C++ 编译报告 | 无完整程序失败 |
| 历史 standalone 运行回归 | 102 个用例通过，0 失败 |
| Python 语法扫描 | 509 个代码块，0 失败 |
| 模块字段检查 | 142 个模块，无缺失字段 |
| 禁止项扫描 | C++ 代码块未发现 `freopen`、`#pragma`、文件 IO、`#define int long long` |
| 1-index / 旧接口口径扫描 | source_hits=0, generated_hits=0, freshness=0 |
| 模板一致性扫描 | hits=0 |
| C++ 伪代码残留扫描 | Findings=0 |

## PDF 核验

- 已重建 `openbook_core.pdf`、`openbook_full.pdf`、`openbook_printable_full.pdf`。
- 已重建 14 个分卷 PDF 和 1 页“翻哪本书”索引 PDF。
- 已渲染并人工查看关键页：总索引页、DP 卷首页、图论卷首页、数学/模拟卷首页、SIM-04 起始页。
- 视觉抽查未发现标题遮挡、表格错位、代码块明显截断或页面半空异常。

## 注意

- `standalone_runtime_test_report.md` 中“未登记运行用例”是覆盖提示，不代表失败；新增 v0.2 例题由 `v02_example_test_report.md` 单独覆盖。
- snippet 级代码片段有些依赖同卷前置结构体或变量，不按完整程序单独编译；完整程序和 standalone 单元已单独通过编译/运行检查。
