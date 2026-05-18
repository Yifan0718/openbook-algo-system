from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "03_modules", ROOT / "04_generated_drafts", ROOT / "06_output", ROOT / "00_management", ROOT / "02_blueprint"]
REPORT = ROOT / "05_review" / "forbidden_patterns_report.md"

PATTERNS = [
    r"\bfreopen\s*\(",
    r"#\s*pragma\s+GCC\s+optimize",
    r"#\s*define\s+int\s+long\s+long",
    r"\bsystem\s*\(",
    r"\bifstream\b",
    r"\bofstream\b",
    r"\bfopen\s*\(",
]


def iter_markdown_files():
    for base in TARGETS:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            yield path


def in_cpp_block(line, state):
    stripped = line.strip()
    if stripped.startswith("```"):
        if not state["open"]:
            state["open"] = True
            state["cpp"] = stripped.lower().startswith("```cpp") or stripped.lower().startswith("```c++")
        else:
            state["open"] = False
            state["cpp"] = False
    return state["open"] and state["cpp"]


def main():
    findings = []
    compiled = [re.compile(p) for p in PATTERNS]

    for path in iter_markdown_files():
        state = {"open": False, "cpp": False}
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            is_code = in_cpp_block(line, state)
            if not is_code:
                continue
            for pat, rx in zip(PATTERNS, compiled):
                if rx.search(line):
                    findings.append((path.relative_to(ROOT), lineno, pat, line.strip()))

    lines = ["# 禁止项扫描报告", ""]
    if not findings:
        lines.append("未在 C++ 代码块中发现禁止项。")
    else:
        lines.append("| 文件 | 行 | 规则 | 内容 |")
        lines.append("|---|---:|---|---|")
        for rel, lineno, pat, text in findings:
            text = text.replace("|", "\\|")
            lines.append(f"| `{rel}` | {lineno} | `{pat}` | `{text}` |")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
