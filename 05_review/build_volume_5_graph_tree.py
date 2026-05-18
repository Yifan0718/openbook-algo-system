from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
OUT = ROOT / "04_generated_drafts" / "volume_5_graph_tree.md"


def main() -> None:
    graph_paths = sorted(MODULES.glob("GRAPH-*.md"))
    tree_paths = sorted(MODULES.glob("TREE-*.md"))
    dp_tree_paths = [
        MODULES / "DP-14-tree-dp.md",
        MODULES / "DP-15-dag-dp.md",
    ]
    paths = graph_paths + tree_paths + [p for p in dp_tree_paths if p.exists()]

    parts = [
        "# 第 5 卷：图论与树",
        "",
        "> 自动由 `03_modules/GRAPH-*.md`、`TREE-*.md`、`DP-14/15` 重建。定位是统一建图、图论算法、树信息层、树形 DP 与部分分路线。",
        "",
        "## 使用顺序",
        "",
        "1. 先看 `GRAPH-00` 和 `OPS-00` 的建图协议，确认有向/无向和边权。",
        "2. 普通图问题查 `GRAPH-01` 到 `GRAPH-08`。",
        "3. 树题先用 `TREE-01` 整理 parent/depth/DFS 序，再接 `GRAPH-09` 或 `DP-14`。",
        "4. 不会正解时先看 `GRAPH-11` 的 V0 到 V5 部分分路线。",
        "",
    ]

    for path in paths:
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{path.name} -->")
        parts.append(path.read_text(encoding="utf-8", errors="replace").rstrip())

    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    included_dp_refs = sum(p.exists() for p in dp_tree_paths)
    print(f"Included {len(graph_paths)} GRAPH modules, {len(tree_paths)} TREE modules, {included_dp_refs} DP tree/DAG refs")


if __name__ == "__main__":
    main()
