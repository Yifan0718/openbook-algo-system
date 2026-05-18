from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
REPORT = ROOT / "05_review" / "second_round_module_matrix.md"

CPP_RE = re.compile(r"```(?:cpp|c\+\+)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
TEXT_RE = re.compile(r"```text\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)

REQUIRED_FIELDS = [
    ("编号", ["模块编号", "模型编号"]),
    ("名称", ["模块名称", "模型名称"]),
    ("什么时候用", ["什么时候用"]),
    ("不要什么时候用", ["不要什么时候用"]),
    ("复杂度", ["复杂度"]),
    ("输入如何整理", ["输入如何整理", "输入整理", "输入如何建模", "输入", "题面触发词"]),
    ("接口", ["接口"]),
    ("模板代码", ["模板代码", "C++17 模板", "C++17模板", "C++17模板或计算方式", "完整代码", "代码模板", "转移模板", "可抄完整模板"]),
    ("调用示例", ["调用示例", "示例", "样例", "自测", "常用片段"]),
    ("常见坑", ["常见坑"]),
    ("暴力/部分分替代", ["暴力/部分分替代", "部分分", "暴力", "记忆化"]),
    ("最小测试样例", ["最小测试样例", "补充自测", "自测", "样例"]),
]

KEYWORDS = [
    ("1-index", ["1-index", "1..n", "1 到 n"]),
    ("static/防御", ["static", "MAXN", "assert", "越界", "防御"]),
    ("复杂度", ["O(", "复杂度"]),
    ("部分分", ["部分分", "暴力", "记忆化"]),
    ("C++17", ["C++17", "bits/stdc++.h", "using namespace std"]),
]


def has_main(code: str) -> bool:
    return re.search(r"\bint\s+main\s*\(", code) is not None


def field_present(label: str, aliases: list[str], text: str, cpp_blocks: list[str], standalone: int) -> bool:
    if any(alias in text for alias in aliases):
        return True
    if label == "模板代码" and cpp_blocks:
        return True
    if label in {"调用示例", "最小测试样例"} and standalone:
        return True
    return False


def main() -> int:
    rows = []
    problems = []
    for path in sorted(MODULES.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        cpp_blocks = CPP_RE.findall(text)
        text_blocks = TEXT_RE.findall(text)
        standalone = sum(1 for block in cpp_blocks if has_main(block))
        missing = [
            label
            for label, aliases in REQUIRED_FIELDS
            if not field_present(label, aliases, text, cpp_blocks, standalone)
        ]
        marks = []
        for label, words in KEYWORDS:
            if any(word in text for word in words):
                marks.append(label)
        status = "OK" if not missing else "FIELD"
        if missing:
            problems.append((path.name, missing))
        rows.append(
            (
                path.name,
                len(cpp_blocks),
                standalone,
                len(text_blocks),
                status,
                ", ".join(marks),
                ", ".join(missing),
            )
        )

    lines = [
        "# 第二轮模块逐项矩阵",
        "",
        "说明：这是机械矩阵，不替代人工审计；用于保证所有模块逐项进表，没有漏扫。",
        "",
        f"- 模块数：{len(rows)}",
        f"- 字段缺失模块数：{len(problems)}",
        "",
        "| 模块 | cpp块 | 完整main块 | text块 | 状态 | 覆盖标记 | 缺失字段 |",
        "|---|---:|---:|---:|---|---|---|",
    ]
    for name, cpp_count, standalone, text_count, status, marks, missing in rows:
        lines.append(
            f"| `{name}` | {cpp_count} | {standalone} | {text_count} | {status} | {marks} | {missing} |"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"modules={len(rows)} missing={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
