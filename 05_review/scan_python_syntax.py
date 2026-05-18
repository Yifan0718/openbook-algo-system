from pathlib import Path
import ast
import re


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "03_modules", ROOT / "04_generated_drafts", ROOT / "06_output"]
REPORT = ROOT / "05_review" / "python_syntax_report.md"

PY_RE = re.compile(r"```python\s*\n(.*?)```", re.S | re.I)


def line_number(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def main() -> int:
    rows: list[tuple[str, int, str]] = []
    failures: list[tuple[str, int, str]] = []

    for root in TARGETS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for block in PY_RE.finditer(text):
                code = block.group(1)
                line = line_number(text, block.start(1))
                rel = str(path.relative_to(ROOT))
                try:
                    ast.parse(code)
                    rows.append((rel, line, "OK"))
                except SyntaxError as exc:
                    msg = f"{exc.__class__.__name__}: {exc.msg}"
                    rows.append((rel, line, msg))
                    failures.append((rel, line, msg))

    lines = [
        "# Python 代码块语法扫描",
        "",
        f"- Python 代码块数：{len(rows)}",
        f"- 语法错误数：{len(failures)}",
        "",
        "| 文件 | 起始行 | 状态 |",
        "|---|---:|---|",
    ]
    for rel, line, status in rows:
        lines.append(f"| `{rel}` | {line} | {status} |")

    REPORT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"python_blocks={len(rows)} failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

