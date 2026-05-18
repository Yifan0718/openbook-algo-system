import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "04_generated_drafts"
MODULES = ROOT / "03_modules"
OUT = ROOT / "06_output" / "openbook_full.md"

ORDER = [
    "volume_-1_0A_0_ops_route.md",
    "volume_1_cpp_stl.md",
    "volume_2_brute_memo_partial.md",
    "volume_3_dp_model_reuse.md",
    "volume_3A_greedy_dp_discrimination.md",
    "volume_4_data_structures.md",
    "volume_5_graph_tree.md",
    "volume_6_math_string.md",
    "volume_7_debug_training.md",
    "volume_8_competition_math_reference.md",
    "volume_9_python_complement.md",
    "volume_10_ai_special_topics.md",
    "volume_11_signoff_encyclopedia.md",
]

MODULE_PREFIX_ORDER = [
    "OPS",
    "ROUTE",
    "AI",
    "CPP",
    "PY",
    "BASIC",
    "BRUTE",
    "DP",
    "DS",
    "SIM",
    "GREEDY",
    "GRAPH",
    "TREE",
    "DIVIDE",
    "MATH",
    "MATHREF",
    "MATH-LA",
    "STR",
    "SIGN",
    "TRAIN",
]


def natural_key(name: str) -> list[object]:
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", name)]


def module_sort_key(path: Path) -> tuple[int, list[object]]:
    name = path.name
    prefix = name.split("-", 1)[0]
    if name.startswith("MATH-LA"):
        prefix = "MATH-LA"
    try:
        rank = MODULE_PREFIX_ORDER.index(prefix)
    except ValueError:
        rank = len(MODULE_PREFIX_ORDER)
    return rank, natural_key(name)


def demote_markdown_headings(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            lines.append(line)
            continue
        if not in_fence and re.match(r"^#{1,5}\s", line):
            line = "#" + line
        lines.append(line)
    return "\n".join(lines)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        "# 北京中关村学院夏令营机考纸质开卷资料包",
        "",
        "> 最终合并版：前半是分卷路由和重点讲解，附录收录模块全文；重复展开是为了打印后不断链。",
        "",
    ]

    for name in ORDER:
        path = DRAFTS / name
        if not path.exists():
            raise FileNotFoundError(f"missing draft: {name}")
        parts.append("\n\n---\n\n")
        parts.append(path.read_text(encoding="utf-8", errors="replace"))

    module_paths = sorted(MODULES.glob("*.md"), key=module_sort_key)
    parts.append("\n\n---\n\n")
    parts.append("# 附录 A：模块全文库")
    parts.append("")
    parts.append("这一部分按模块文件直接合并，确保 `openbook_full` 不是只有路由和引用。")
    for path in module_paths:
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{path.name} -->")
        parts.append(demote_markdown_headings(path.read_text(encoding="utf-8", errors="replace")).rstrip())

    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Included {len(module_paths)} module files in appendix")


if __name__ == "__main__":
    main()
