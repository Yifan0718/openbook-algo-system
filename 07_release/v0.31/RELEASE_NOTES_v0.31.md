# v0.31 Release Notes

## 定位

v0.31 是 v0.3 的修复发布版：恢复 v0.2 中已经整合进各分卷的组合例题训练区，同时保留 v0.3 新增的第 11 卷签到题百科和 Markov/AI/计算机常识补充。

## 修复

- 修复 v0.3 全量构建顺序问题：`build_all_outputs.py` 现在会在生成分卷基础稿后自动运行 `integrate_v02_examples.py`。
- 恢复每卷的组合例题训练区：共 188 道组合例题，覆盖 00-10 卷。
- 修复后 `openbook_full.pdf` / `openbook_printable_full.pdf` 为 `1376` 页，高于 v0.2 tag 的 `1242` 页，也高于误发布 v0.3 的 `1172` 页。

## 继续保留

- 第 11 卷签到题百科：`58` 页。
- Markov 性质、Markov 链、转移矩阵、平稳分布、HMM/MDP。
- 现代 AI 术语、RAG、Attention、Transformer、向量检索。
- 进制、补码、浮点、字节序、内存、读程序、流程图。
- SIM 方程求解专题。

## 校验摘要

- 组合例题样例运行：`188/188` 通过。
- standalone C++ 编译：失败 `0`。
- standalone 运行用例：失败 `0`。
- 分卷 PDF：`14` 个。
- PDF 页数核验：
  - `openbook_full.pdf`：`1376` 页。
  - `openbook_printable_full.pdf`：`1376` 页。
  - `11_signoff_encyclopedia.pdf`：`58` 页。
- 发布压缩包：`07_release/openbook-v0.31.zip`。

## 发布

- README 已更新到 v0.31。
- 许可证：MIT License。
- 完整 PDF、分卷 PDF、v0.31 zip 和 SHA256 校验文件随仓库保留，方便直接下载和打印。
