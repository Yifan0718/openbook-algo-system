# 质检目录

本目录用于存放自动检查脚本和检查报告。

建议流程：

```powershell
python .\05_review\build_all_outputs.py
python .\05_review\scan_forbidden_patterns.py
python .\05_review\check_module_fields.py
python .\05_review\scan_index_policy.py
python .\05_review\scan_template_consistency.py
python .\05_review\scan_cpp_pseudocode.py
python .\05_review\extract_compile_cpp_blocks.py
```

生成的报告建议写入：

```text
05_review/forbidden_patterns_report.md
05_review/module_fields_report.md
05_review/cpp_compile_report.md
05_review/final_review_report.md
```

说明：`build_all_outputs.py` 会重建各卷草稿、`openbook_full.md`、`openbook_printable_full.md`，并在本机存在 `pandoc + xelatex` 时重建对应 PDF。
