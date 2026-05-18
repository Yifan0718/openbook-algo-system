from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
OUT = ROOT / "06_output" / "openbook_core.md"

CORE_MODULES = [
    "OPS-00-unified-protocols.md",
    "OPS-01-exam-operations.md",
    "ROUTE-00-routing-tables.md",
    "CPP-001-main-io.md",
    "CPP-10-io-formatting.md",
    "CPP-013-stl-containers-reference.md",
    "BRUTE-01-complexity-cheatsheet.md",
    "BRUTE-07-memoized-search-overview.md",
    "DP-00-total-flow.md",
    "DP-01-routing-table.md",
    "DP-02-state-sentence-library.md",
    "DP-03-dfs-memo-table-upgrade.md",
    "DP-03B-state-dimension-router.md",
    "DP-21-p1874-modeling-example.md",
    "DP-22-edit-distance-modeling-example.md",
    "DP-25-dfs-memo-case-strategy.md",
    "DP-26-aftereffect-state-augmentation.md",
    "DS-00-data-structure-routing.md",
    "DS-06-two-pointers-sliding-window.md",
    "GRAPH-00-standard-graph.md",
    "GRAPH-03-dijkstra-path-multisource.md",
    "MATH-01-gcd-lcm.md",
    "SIM-01-high-precision.md",
    "STR-01-basic-operations.md",
    "STR-05-manacher.md",
    "TRAIN-00-debug-checklist.md",
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        "# 核心速查版",
        "",
        "> 这是考场第一页到前几十页的快速导航包：只放最高频、最能救分、最容易拼接的模块。完整资料见 `openbook_full.md/pdf` 和 `openbook_printable_full.md/pdf`。",
        "",
        "## 核心目录",
        "",
    ]

    for name in CORE_MODULES:
        path = MODULES / name
        if not path.exists():
            raise FileNotFoundError(path)
        title = path.read_text(encoding="utf-8", errors="replace").splitlines()[0].lstrip("# ").strip()
        parts.append(f"- `{name}`：{title}")

    for name in CORE_MODULES:
        path = MODULES / name
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{name} -->")
        parts.append(path.read_text(encoding="utf-8", errors="replace").rstrip())

    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Included {len(CORE_MODULES)} core module files")


if __name__ == "__main__":
    main()
