import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "04_generated_drafts"
MODULES = ROOT / "03_modules"
OUT = ROOT / "06_output" / "openbook_printable_full.md"

DRAFT_ORDER = [
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
    "12_zhongguancun_machine_exam_companion.md",
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


def main() -> None:
    parts = [
        "# 北京中关村学院夏令营机考纸质开卷资料包：自包含打印版",
        "",
        "> 版本定位：考场纸质资料。前半是路由和卷结构，后半附录收录模块全文，避免打印后出现“只有引用没有代码”的断链。",
        "",
    ]

    for name in DRAFT_ORDER:
        path = DRAFTS / name
        if not path.exists():
            raise FileNotFoundError(f"missing draft: {name}")
        parts.append("\n\n---\n\n")
        parts.append(path.read_text(encoding="utf-8", errors="replace").rstrip())

    parts.append("\n\n---\n\n")
    parts.append("# 附录 A：模块全文库")
    parts.append("")
    parts.append("这一部分按模块文件直接合并。考场使用时，如果正文路由表指到某个模块，就在这里翻模块编号。")

    module_paths = sorted(MODULES.glob("*.md"), key=module_sort_key)
    for path in module_paths:
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{path.name} -->")
        parts.append(demote_markdown_headings(path.read_text(encoding="utf-8", errors="replace")).rstrip())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Included {len(module_paths)} module files")


if __name__ == "__main__":
    main()
