import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "04_generated_drafts", ROOT / "03_modules", ROOT / "06_output"]
REPORT = ROOT / "05_review" / "cpp_pseudocode_report.md"

CODE_BLOCK = re.compile(r"```(?:cpp|c\+\+)\s*\n(.*?)```", re.S | re.I)
SUSPICIOUS = [
    re.compile(r"^\s*read\b", re.I | re.M),
    re.compile(r"^\s*print\b", re.I | re.M),
    re.compile(r"^\s*repeat\b", re.I | re.M),
    re.compile(r"^\s*for each\b", re.I | re.M),
    re.compile(r"^\s*for\s+.+\s+in\s+.+:?$", re.I | re.M),
    re.compile(r"^\s*(读入|输出|遍历|处理)\b", re.M),
    re.compile(r"\bsort\s*\([^)]*\bby\b", re.I),
    re.compile(r"^\s*return answer\b", re.I | re.M),
    re.compile(r"\bno solution\b", re.I),
    re.compile(r"\bdo something\b", re.I),
    re.compile(r"\bprocess one case\b", re.I),
]


def line_number(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def main() -> None:
    findings: list[str] = []

    for root in TARGETS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for block in CODE_BLOCK.finditer(text):
                body = block.group(1)
                for pattern in SUSPICIOUS:
                    match = pattern.search(body)
                    if match:
                        line = line_number(text, block.start(1) + match.start())
                        rel = path.relative_to(ROOT)
                        snippet = match.group(0).strip()
                        findings.append(f"- `{rel}` line {line}: `{snippet}`")
                        break

    lines = ["# cpp 代码块伪代码扫描", ""]
    if findings:
        lines.append("发现疑似伪代码混入 `cpp` 代码块：")
        lines.append("")
        lines.extend(findings)
    else:
        lines.append("未发现疑似伪代码混入 `cpp` 代码块。")

    REPORT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"Findings: {len(findings)}")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
