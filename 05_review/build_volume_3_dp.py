from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
OUT = ROOT / "04_generated_drafts" / "volume_3_dp_model_reuse.md"


def main() -> None:
    paths = sorted(MODULES.glob("DP-*.md"))
    parts = [
        "# 第 3 卷：DP 模型复用系统",
        "",
        "> 自动由 `03_modules/DP-*.md` 重建。定位是初学者友好的 DP 路由、建模、暴力到记忆化再到表推。",
        "",
    ]

    for path in paths:
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{path.name} -->")
        parts.append(path.read_text(encoding="utf-8", errors="replace").rstrip())

    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Included {len(paths)} DP modules")


if __name__ == "__main__":
    main()
