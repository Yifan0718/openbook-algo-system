from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "05_review" / "template_consistency_report.md"
CHECK_DIRS = [ROOT / "03_modules", ROOT / "02_blueprint", ROOT / "00_management", ROOT / "04_generated_drafts", ROOT / "06_output"]


CPP_BLOCK_RE = re.compile(r"```(?:cpp|c\+\+)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


HARD_PATTERNS = [
    ("cpp TODO/FIXME", re.compile(r"\b(TODO|FIXME)\b")),
    ("cpp ellipsis placeholder", re.compile(r"(^|\s)\.\.\.(\s|$)")),
    ("old Graph add_edge", re.compile(r"\bG\.add_edge\s*\(")),
    ("old Graph e.id", re.compile(r"\be\.id\b|G\.edges\s*\[\s*e\.id\s*\]")),
    ("old graph output edge ids", re.compile(r"\b(chosen_edge_ids|bridge_ids)\b")),
    ("0-index string grid", re.compile(r"vector\s*<\s*string\s*>\s+g\s*\(\s*n\s*\)")),
    ("0-index char grid", re.compile(r"vector\s*<\s*vector\s*<\s*char\s*>\s*>\s+g\s*\(\s*n\s*,")),
    ("freopen", re.compile(r"\bfreopen\s*\(")),
    ("pragma optimize", re.compile(r"#\s*pragma\s+GCC")),
]


ALLOW_FILE_CONTAINS = [
    "GRAPH-10-dinic",
]


def is_allowed(path: Path, label: str, block: str) -> bool:
    name = path.name
    if any(s in name for s in ALLOW_FILE_CONTAINS) and "add_edge" in block and "FlowGraph" in block:
        return True
    if label == "cpp ellipsis placeholder" and ("MATHREF" in name or "ROUTE" in name):
        return True
    return False


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def scan_file(path: Path) -> list[tuple[str, int, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    hits: list[tuple[str, int, str]] = []
    for match in CPP_BLOCK_RE.finditer(text):
        block = match.group(1)
        base = match.start(1)
        for label, pattern in HARD_PATTERNS:
            if is_allowed(path, label, block):
                continue
            for hit in pattern.finditer(block):
                lineno = line_number(text, base + hit.start())
                line = text.splitlines()[lineno - 1].strip()
                hits.append((label, lineno, line))
    return hits


def main() -> int:
    all_hits: list[tuple[str, str, int, str]] = []
    for base in CHECK_DIRS:
        if not base.exists():
            continue
        for path in sorted(base.glob("*.md")):
            for label, lineno, line in scan_file(path):
                all_hits.append((label, str(path.relative_to(ROOT)), lineno, line))

    lines = ["# 模板代码一致性扫描", ""]
    if not all_hits:
        lines.append("未发现硬性模板占位、旧 Graph 接口、旧边字段、禁止 IO 或 0-index 网格读入。")
    else:
        for label, rel, lineno, line in all_hits:
            lines.append(f"- `{label}` {rel}:{lineno} `{line}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"hits={len(all_hits)}")
    return 1 if all_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
