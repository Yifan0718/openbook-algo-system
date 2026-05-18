# 合并计划

## 1. 输入来源

各 worker 先生成：

```text
04_generated_drafts/volume_-1_0A_0_ops_route.md
04_generated_drafts/volume_1_cpp_stl.md
04_generated_drafts/volume_2_brute_memo_partial.md
04_generated_drafts/volume_3_dp_model_reuse.md
04_generated_drafts/volume_4_data_structures.md
04_generated_drafts/volume_5_graph_tree.md
04_generated_drafts/volume_6_math_string.md
04_generated_drafts/volume_6A_competition_math_reference.md
04_generated_drafts/volume_7_debug_training.md
```

模块源文件保留在：

```text
03_modules/*.md
```

## 2. 初步合并顺序

```text
title page
第 -1 卷
第 0A 卷
第 0 卷
第 1 卷
第 2 卷
第 3 卷
第 4 卷
第 5 卷
第 6 卷
第 6A 卷
第 7 卷
附录：模块索引
附录：提交前检查清单
```

## 3. 合并后人工统一

需要人工检查：

- 模块编号是否重复。
- `Graph` 是否全部使用标准版本。
- 数据结构接口是否统一。
- 记忆化章节和 DP 卷是否重复过多。
- 高频内容是否在前，低频内容是否在后。
- 所有代码块是否遵守 C++17 与考试限制。

## 4. 输出文件

```text
06_output/openbook_full.md
06_output/openbook_core.md
06_output/openbook_full.pdf
06_output/openbook_core.pdf
```
