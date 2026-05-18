# v0.31 Signoff 核验报告

结论：可以发布 v0.31。v0.31 修复了 v0.3 构建时漏整合组合例题训练区的问题，当前 full PDF 页数已恢复并超过 v0.2。

## 页数对比

| 版本/文件 | 页数 |
|---|---:|
| v0.2 tag `openbook_full.pdf` | 1242 |
| 误发布 v0.3 `openbook_full.pdf` | 1172 |
| v0.31 `openbook_full.pdf` | 1376 |
| v0.31 `openbook_printable_full.pdf` | 1376 |
| v0.31 `11_signoff_encyclopedia.pdf` | 58 |

## 修复确认

| 检查 | 结果 |
|---|---|
| 组合例题训练区标记 | 已恢复，`openbook_full.md` 中 67 处 |
| 组合例题数量 | 188 |
| 第 11 卷签到题百科 | 保留 |
| Markov 样例修正 | 保留 |
| 构建脚本防回归 | `build_all_outputs.py` 已加入 `integrate_v02_examples.py` |

## 自动校验摘要

| 检查 | 结果 |
|---|---|
| 组合例题样例运行 | 188 / 188 通过 |
| standalone C++ 编译失败 | 0 |
| standalone 运行失败 | 0 |
| 模块字段检查 | 通过 |
| `git diff --check` | 无空白错误 |
| 密钥/本地绝对路径扫描 | 未发现高风险命中 |

## 说明

- `v02_example_*` 文件名沿用历史命名，表示这批组合例题最早在 v0.2 引入；v0.31 继续使用这批例题并通过测试。
- `v0.3` tag/release 保留为历史记录；v0.31 是修复后的推荐版本。
