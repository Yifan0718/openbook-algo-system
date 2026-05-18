# GitHub 发布检查清单

## 内容确认

- [x] README 语气和公开范围确认。
- [x] 保留机考/夏令营准备语境，但仓库定位为通用开卷算法资料包。
- [x] 保留 AI 专题，作为专项招生与模拟题补充内容。
- [x] 加入 MIT License。

## 文件确认

- [x] `07_release/v0.32/01_print_ready/` 中总 PDF 可打开。
- [x] `07_release/v0.32/01_print_ready/chapter_pdfs/` 中分卷 PDF 可打开。
- [x] `07_release/openbook-v0.32.zip` SHA256 与 `openbook-v0.32.zip.sha256.txt` 一致。
- [x] 不包含临时目录 `tmp/`、`__pycache__/`、编译产物 `.exe/.out`。
- [x] 已执行本地路径与常见密钥模式扫描。

## Git 操作建议

```powershell
git init -b main
git status
git add .
git commit -m "Release v0.32 openbook algorithm system"
```

发布到 GitHub 前再设置 remote：

```powershell
git remote add origin <repo-url>
git push -u origin main
```

本清单随 v0.32 public release 保留，用于记录发布前检查项。

