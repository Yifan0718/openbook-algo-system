from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
OUT = ROOT / "04_generated_drafts" / "volume_3A_greedy_dp_discrimination.md"


def main() -> None:
    paths = sorted(MODULES.glob("GREEDY-*.md"))
    parts = [
        "# 第 3A 卷：贪心判别、证明与反例系统",
        "",
        "> 自动由 `03_modules/GREEDY-*.md` 重建。定位是帮助初学者判断什么时候能贪心，什么时候必须回到 DP/记忆化搜索。",
        "",
    ]

    for path in paths:
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{path.name} -->")
        parts.append(path.read_text(encoding="utf-8", errors="replace").rstrip())

    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Included {len(paths)} GREEDY modules")


if __name__ == "__main__":
    main()
