# 构建与校验说明

本仓库保留原始构建目录结构，脚本默认从仓库根目录运行。

## 环境依赖

必需：

- Python 3.11+
- `pandoc`
- XeLaTeX / TeX Live，且可用中文字体 `Microsoft YaHei`
- Python 包：`pypdf`

用于 C++ 审计：

- WSL
- WSL 中可用 `g++`

## 一键重建主要输出

```powershell
python 05_review\build_all_outputs.py
```

该脚本会重建：

- `06_output/openbook_core.md/pdf`
- `06_output/openbook_full.md/pdf`
- `06_output/openbook_printable_full.md/pdf`

## 重建分卷 PDF

```powershell
$env:OPENBOOK_RELEASE_VERSION='v0.32'
python 05_review\build_chapter_pdfs.py
```

输出位置：

```text
06_output/chapter_pdfs/
07_release/v0.32/01_print_ready/chapter_pdfs/
```

## 重建 v0.32 发布目录和压缩包

```powershell
$env:OPENBOOK_RELEASE_VERSION='v0.32'
python 05_review\publish_v02_release.py
```

输出位置：

```text
07_release/v0.32/
07_release/openbook-v0.32.zip
07_release/openbook-v0.32.zip.sha256.txt
```

## 例题运行测试

```powershell
python 05_review\integrate_v02_examples.py
python 05_review\extract_and_test_v02_examples.py
```

报告：

```text
06_output/v02_example_tests/v02_example_test_report.md
06_output/v02_example_tests/v02_example_test_report.json
```

说明：例题生成脚本名称仍保留 `v02`，表示这批组合例题最初在 v0.2 引入；v0.3 发布继续复用并通过测试。

## 代码审计

```powershell
python 05_review\scan_python_syntax.py
python 05_review\scan_cpp_pseudocode.py
python 05_review\scan_template_consistency.py
python 05_review\scan_index_policy.py
python 05_review\scan_forbidden_patterns.py
python 05_review\check_module_fields.py
python 05_review\extract_compile_cpp_blocks.py
python 05_review\audit_cpp_blocks_wsl.py
python 05_review\second_round_standalone_compile_all.py
python 05_review\run_standalone_tests.py
python 05_review\second_round_module_matrix.py
```

## 常见问题

- 如果发布目录里的 PDF 正在被 Adobe Acrobat 等程序打开，Windows 会拒绝覆盖。关闭 PDF 阅读器后重新运行构建脚本。
- 如果 `pandoc` 或 `xelatex` 不在 PATH 中，PDF 构建会失败。
- 如果没有 WSL/g++，PDF 构建不受影响，但 C++ 编译审计无法运行。

