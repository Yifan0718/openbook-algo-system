from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
OUT = ROOT / "04_generated_drafts" / "volume_4_data_structures.md"


def main() -> None:
    paths = sorted(MODULES.glob("DS-*.md"))
    parts = [
        "# 第 4 卷：数据结构与双指针",
        "",
        "> 自动由 `03_modules/DS-*.md` 重建。定位是把区间、动态维护、窗口、连通性和排名统计整理成可拼接模块。",
        "",
    ]

    for path in paths:
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{path.name} -->")
        parts.append(path.read_text(encoding="utf-8", errors="replace").rstrip())

    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Included {len(paths)} DS modules")


if __name__ == "__main__":
    main()
