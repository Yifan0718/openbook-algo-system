from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "05_review" / "index_policy_report.md"


CRITICAL_PATTERNS = [
    ("关键点/点号改成 0-index", "点编号改成 `0..n-1`"),
    ("关键点 0..k-1", "关键点编号 0..k-1"),
    ("状压关键点强制 0-index", "必须改成 0-index"),
    ("旧关键点循环 last < kcnt", "last < kcnt"),
    ("旧 key.size 关键点矩阵", "key.size()"),
    ("旧 Graph e.id 查 directed", "G.edges[e.id]"),
    ("旧 Kruskal 输出内部边号", "chosen_edge_ids"),
    ("旧 Lowlink bridge_ids", "bridge_ids"),
    ("旧 Floyd vector 矩阵", "vector<vector<ll>> floyd"),
    ("旧 Floyd vector dist", "vector<vector<ll>> dist"),
    ("旧 directed=true 口径", "directed=true"),
    ("旧 directed=false 口径", "directed=false"),
    ("0-index 字符网格读入", "vector<string> g(n)"),
    ("0-index 字符矩阵读入", "vector<vector<char>> g(n, vector<char>(m))"),
]


ALLOW_PATH_PARTS = [
    "STR-",
    "CPP-011-string",
    "GRAPH-10-dinic",
]


def is_allowed(path: Path, text: str) -> bool:
    name = path.name
    if any(part in name for part in ALLOW_PATH_PARTS):
        return True
    if "FlowGraph" in text and "add_edge" in text:
        return True
    return False


def scan_paths(paths: list[Path]) -> list[tuple[str, str, int, str]]:
    hits: list[tuple[str, str, int, str]] = []
    for base in paths:
        for path in sorted(base.glob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in CRITICAL_PATTERNS:
                if is_allowed(path, text):
                    continue
                for lineno, line in enumerate(text.splitlines(), 1):
                    if pattern in line:
                        hits.append((label, str(path.relative_to(ROOT)), lineno, line.strip()))

            if not is_allowed(path, text):
                for lineno, line in enumerate(text.splitlines(), 1):
                    if "G.add_edge(" in line and "不要写" not in line:
                        hits.append(("旧 Graph add_edge 接口", str(path.relative_to(ROOT)), lineno, line.strip()))
    return hits


def freshness_checks() -> list[str]:
    problems: list[str] = []
    modules = list((ROOT / "03_modules").glob("*.md"))
    drafts = [
        p for p in (ROOT / "04_generated_drafts").glob("*.md")
        if not p.name.startswith("v02_examples_worker_")
    ]
    outputs = [
        ROOT / "06_output" / "openbook_core.md",
        ROOT / "06_output" / "openbook_full.md",
        ROOT / "06_output" / "openbook_printable_full.md",
        ROOT / "06_output" / "openbook_core.pdf",
        ROOT / "06_output" / "openbook_full.pdf",
        ROOT / "06_output" / "openbook_printable_full.pdf",
    ]

    if modules and drafts:
        newest_module = max(p.stat().st_mtime for p in modules)
        stale = [p.name for p in drafts if p.stat().st_mtime < newest_module]
        if stale:
            problems.append("生成草稿早于最新模块，需要重建：" + ", ".join(stale))

    existing_outputs = [p for p in outputs if p.exists()]
    if drafts and existing_outputs:
        newest_draft = max(p.stat().st_mtime for p in drafts)
        stale = [p.name for p in existing_outputs if p.stat().st_mtime < newest_draft]
        if stale:
            problems.append("最终输出早于最新草稿，需要重建：" + ", ".join(stale))

    return problems


def main() -> int:
    source_hits = scan_paths([ROOT / "03_modules", ROOT / "02_blueprint", ROOT / "00_management"])
    generated_hits = scan_paths([ROOT / "04_generated_drafts", ROOT / "06_output"])
    freshness = freshness_checks()

    lines = [
        "# 下标与竞赛速写口径审计",
        "",
        "硬口径：普通题面对象、图点、图边、关键点、数组和网格默认 1-index；mask 位号、字符串内部、数学自然下标可例外但必须局部说明。",
        "",
        "## Freshness",
    ]
    if freshness:
        lines += [f"- {p}" for p in freshness]
    else:
        lines.append("- OK：生成稿和最终输出时间戳不旧于源稿。")

    lines += ["", "## Source Critical Hits"]
    if source_hits:
        for label, rel, lineno, line in source_hits:
            lines.append(f"- `{label}` {rel}:{lineno} `{line}`")
    else:
        lines.append("- OK：源模块未发现硬口径命中。")

    lines += ["", "## Generated/Output Critical Hits"]
    if generated_hits:
        for label, rel, lineno, line in generated_hits[:300]:
            lines.append(f"- `{label}` {rel}:{lineno} `{line}`")
        if len(generated_hits) > 300:
            lines.append(f"- 另有 {len(generated_hits) - 300} 条，先重建生成稿后再查。")
    else:
        lines.append("- OK：生成稿和输出未发现硬口径命中。")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"source_hits={len(source_hits)} generated_hits={len(generated_hits)} freshness={len(freshness)}")
    return 1 if (source_hits or generated_hits or freshness) else 0


if __name__ == "__main__":
    raise SystemExit(main())
