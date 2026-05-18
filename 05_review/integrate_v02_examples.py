from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "04_generated_drafts"

START = "<!-- V02_EXAMPLES_START -->"
END = "<!-- V02_EXAMPLES_END -->"

VOLUME_FILES = {
    "0": "volume_-1_0A_0_ops_route.md",
    "1": "volume_1_cpp_stl.md",
    "2": "volume_2_brute_memo_partial.md",
    "3": "volume_3_dp_model_reuse.md",
    "3A": "volume_3A_greedy_dp_discrimination.md",
    "4": "volume_4_data_structures.md",
    "5": "volume_5_graph_tree.md",
    "6": "volume_6_math_string.md",
    "7": "volume_7_debug_training.md",
    "8": "volume_8_competition_math_reference.md",
    "9": "volume_9_python_complement.md",
    "10": "volume_10_ai_special_topics.md",
}


def split_examples(text: str) -> list[str]:
    matches = list(re.finditer(r"(?m)^###\s+V[^\n]+\n", text))
    parts: list[str] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        parts.append(text[start:end].strip())
    return parts


def volume_key(block: str) -> str | None:
    m = re.search(r"归属卷[：:]\s*第\s*([0-9]+A?)\s*卷", block)
    if m:
        key = m.group(1)
        return "8" if key == "6A" else key
    m = re.match(r"###\s+V([0-9]+A?)-", block)
    if m:
        key = m.group(1).lstrip("0")
        if key == "6A":
            return "8"
        return key or "0"
    return None


def is_removed_luogu_index_example(block: str) -> bool:
    return bool(re.match(r"###\s+V0?8-", block)) or "洛谷覆盖索引" in block


def normalize_block_for_volume(key: str, block: str) -> str:
    if key != "8":
        return block
    block = block.replace("V06A-", "V08-")
    block = block.replace("第 6A 卷", "第 8 卷")
    block = block.replace("第6A卷", "第8卷")
    return block


def strip_existing(text: str) -> str:
    pattern = re.compile(rf"\n*{re.escape(START)}.*?{re.escape(END)}\n*", re.S)
    return pattern.sub("\n", text).rstrip() + "\n"


def main() -> None:
    grouped: dict[str, list[str]] = {key: [] for key in VOLUME_FILES}
    for path in sorted(DRAFTS.glob("v02_examples_worker_*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for block in split_examples(text):
            if is_removed_luogu_index_example(block):
                continue
            key = volume_key(block)
            if key not in grouped:
                raise ValueError(f"cannot classify example in {path}: {block[:120]}")
            grouped[key].append(normalize_block_for_volume(key, block))

    counts: dict[str, int] = {}
    for key, filename in VOLUME_FILES.items():
        path = DRAFTS / filename
        original = path.read_text(encoding="utf-8", errors="replace")
        base = strip_existing(original)
        examples = grouped.get(key, [])
        if examples:
            section = [
                "",
                START,
                "",
                "# v0.2 本卷例题训练区",
                "",
                "这一节是 0.2 新增的实战例题。每题都配完整可运行代码和样例；考试时优先看“覆盖模块”和“考场用途”，再复制对应代码骨架。",
                "",
            ]
            section.extend(examples)
            section.extend(["", END, ""])
            path.write_text(base + "\n".join(section), encoding="utf-8")
        else:
            path.write_text(base, encoding="utf-8")
        counts[key] = len(examples)

    report = ["# v0.2 例题整合计数", "", "| 卷 | 文件 | 例题数 |", "|---|---|---:|"]
    for key, filename in VOLUME_FILES.items():
        report.append(f"| {key} | `{filename}` | {counts[key]} |")
    (ROOT / "06_output" / "v02_example_integration_report.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    for key, count in counts.items():
        print(f"volume {key}: {count} examples")


if __name__ == "__main__":
    main()
