from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT / "03_modules"
REPORT = ROOT / "05_review" / "module_fields_report.md"

REQUIRED_GROUPS = [
    ("模块编号", "模型编号"),
    ("模块名称", "模型名称"),
    ("题面触发词",),
    ("什么时候用",),
    ("不要什么时候用",),
    ("复杂度",),
    ("依赖的标准容器",),
    ("接口",),
    ("常见坑",),
    ("暴力/部分分替代",),
]


def main():
    rows = []
    if MODULE_DIR.exists():
        for path in sorted(MODULE_DIR.glob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            missing = ["/".join(group) for group in REQUIRED_GROUPS if not any(field in text for field in group)]
            rows.append((path.relative_to(ROOT), missing))

    lines = ["# 模块字段检查报告", ""]
    if not rows:
        lines.append("尚未发现模块文件。")
    else:
        lines.append("| 文件 | 缺失字段 |")
        lines.append("|---|---|")
        for rel, missing in rows:
            miss = "、".join(missing) if missing else "无"
            lines.append(f"| `{rel}` | {miss} |")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")


if __name__ == "__main__":
    main()
