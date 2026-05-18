from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
DRAFTS = ROOT / "04_generated_drafts"


VOLUMES: list[tuple[str, str, str, list[str]]] = [
    (
        "volume_-1_0A_0_ops_route.md",
        "第 0 卷：考场作战与模块拼接总控",
        "自动由 OPS/ROUTE 模块重建。定位是统一协议、题型路由、考场时间分配和提交检查。",
        ["OPS-*.md", "ROUTE-*.md"],
    ),
    (
        "volume_2_brute_memo_partial.md",
        "第 2 卷：暴力、记忆化与部分分",
        "自动由 BRUTE 模块重建。定位是先活下来，再用记忆化和剪枝涨分。",
        ["BRUTE-*.md"],
    ),
    (
        "volume_6_math_string.md",
        "第 6 卷：数学与字符串",
        "自动由 MATH/STR/SIM 模块重建。定位是常用数论、组合、矩阵、字符串和高精度补充。",
        ["MATH-[0-9]*.md", "STR-*.md", "SIM-*.md"],
    ),
    (
        "volume_8_competition_math_reference.md",
        "第 8 卷：竞赛数学参考",
        "自动由 MATHREF/MATH-LA 模块重建。定位是 NOI/ICPC 风格数学查阅补充。",
        ["MATHREF-*.md", "MATH-LA-*.md"],
    ),
    (
        "volume_7_debug_training.md",
        "第 7 卷：调试、反例与训练",
        "自动由 TRAIN 模块重建。定位是考场自查、反例库和小规模验证。",
        ["TRAIN-*.md"],
    ),
    (
        "volume_9_python_complement.md",
        "第 9 卷：Python 互补讲义",
        "自动由 PY 模块重建。定位是 C++ 主战之外的补位工具：高精度、状态记忆化、字符串和小数据部分分。",
        ["PY-*.md"],
    ),
    (
        "volume_10_ai_special_topics.md",
        "第 10 卷：AI 专项可能题型补充",
        "自动由 AI 模块重建。定位是人工智能专项招生中可能包装成算法题的搜索、分类、相似度和模拟主题。",
        ["AI-*.md"],
    ),
]


INTRO_BY_FILENAME = {
    "volume_-1_0A_0_ops_route.md": """## 第 0 卷组速查

| 分区 | 用途 |
|---|---|
| `OPS-*` | 考场流程、提交策略、检查清单 |
| `ROUTE-*` | 题型信号到模块组合的总路由 |

## 常见路由名到模块编号

| 路由名 | 模块入口 |
|---|---|
| `PrefixSum / Difference` | `DS-01` |
| `树状数组 / 双树状数组` | `DS-02` |
| `SegmentTree / SparseTable` | `DS-03` |
| `TwoPointers / SlidingWindow` | `DS-06` |
| `DSU / Kruskal` | `DS-04` 或 `GRAPH-06` |
| `Graph / BFS / Dijkstra` | `GRAPH-00/02/03` |
| `Topo / DAG DP` | `GRAPH-05` |
| `LCA / Tree` | `GRAPH-09 / TREE-*` |
| `Knapsack / LIS / LCS` | `DP-06/07/08/11/23/24` |
| `String matching` | `STR-02 / CPP-011` |
""",
    "volume_2_brute_memo_partial.md": """## 暴力与部分分快速目录

| 数据/场景 | 先翻模块 |
|---|---|
| `n <= 10` 排列/顺序 | `BRUTE-03` |
| `n <= 20` 子集/状态 | `BRUTE-05/07/08` |
| `n <= 40` 子集和/选或不选 | `BRUTE-12` |
| 能写 DFS 但会重复 | `BRUTE-07/08/09/10` |
| 最少步数状态搜索 | `BRUTE-11` |
| 正解不会但要提交 | `BRUTE-13/14/15` |
""",
    "volume_6_math_string.md": """## 数学与字符串速查索引

| 题面信号 | 模块入口 |
|---|---|
| `gcd/lcm/快速幂/逆元` | `MATH-01/02/03` |
| `组合数/计数/阶乘` | `MATH-03/04` |
| `线性递推/矩阵快速幂` | `MATH-05` |
| `质数/因数/筛法` | `MATH-06` |
| `大数/高精度/BigInteger` | `SIM-01/02` |
| `表达式求值/AST` | `SIM-03` |
| `JSON/CSV/INI 解析` | `SIM-04` |
| `手写解释器/小语言模拟` | `SIM-05` |
| `日期/时区/历法` | `SIM-06` |
| `字符串匹配/前缀/哈希` | `STR-02/03` |
| `最长回文/回文半径/区间回文判断` | `STR-05 Manacher` |
""",
    "volume_8_competition_math_reference.md": """## 竞赛数学参考速查索引

| 题面信号 | 模块入口 |
|---|---|
| 整除、同余、取模化简 | `MATHREF-01` |
| 扩展欧几里得、CRT、逆元 | `MATHREF-02` |
| 素数、因数、欧拉函数、莫比乌斯 | `MATHREF-03` |
| 组合计数、容斥、Lucas | `MATHREF-04` |
| 递推、概率期望、博弈 | `MATHREF-05` |
| 几何、数值建模 | `MATHREF-06` |
| 矩阵/线性代数补充 | `MATH-LA-00` |

低优先级但可打印备用：FFT/NTT、BSGS、Miller-Rabin/Pollard-Rho、Burnside/Polya、Min_25 筛等不作为主模板，遇到高阶真题时优先拿小数据/暴力/特判分。
""",
    "volume_9_python_complement.md": """## Python 互补卷使用原则

| 判断 | 建议 |
|---|---|
| C++ 模板稳、数据大、卡常 | 用 C++ |
| 高精度/复杂状态/字符串解析明显省代码 | 可用 Python |
| 只想先拿部分分 | Python 可快速写暴力/记忆化 |
| 需要第三方库才方便 | 不要用，考试不允许 |

这卷不是第二主语言资料。它的作用是：当 Python 明显降低实现难度时，帮你快速写出可靠版本；其他时候继续用 C++。
""",
    "volume_10_ai_special_topics.md": """## AI 专项卷使用原则

| 题面 AI 信号 | 算法本质 |
|---|---|
| 机器人/智能体/规划 | BFS、Dijkstra、A* |
| 对弈/智能决策 | Minimax、Alpha-Beta、博弈 DP |
| 训练集/测试集/标签 | kNN、朴素贝叶斯、感知机、SVM、统计 |
| Special Judge/得分函数 | baseline、指标、验证集调参 |
| 相似文档/推荐 | Cosine、Jaccard、Top-K |
| 文本关键词/检索 | TF-IDF、词频、倒排索引 |
| 聚类/回归 | k-means、线性回归、梯度下降 |
| Markov/HMM | Viterbi、概率 DP |
| 神经网络推理/训练 | 前向传播、softmax、反向传播 |
| 计算图/自动求导 | 反向模式自动微分、链式法则 |
| 强化学习 | MDP、值迭代、Q-learning 公式 |
| 脚本/规则/配置 | SIM-03/04/05 解析和解释 |

这卷的核心判断：AI 背景不是新语法，也不是深度学习框架；它通常是搜索、统计、排序、字符串、模拟和数学公式的包装。
""",
}


LUOGU_TOPICS = [
    "顺序结构", "分支结构", "循环结构", "数组", "字符串", "函数与结构体",
    "模拟与高精度", "排序", "暴力枚举", "递推与递归", "贪心", "二分查找与二分答案",
    "搜索", "线性表", "二叉树", "集合", "图的基本应用", "基础数学问题",
    "前缀和、差分与离散化", "常见优化技巧", "分治与倍增", "进阶搜索", "二叉堆与树状数组",
    "线段树", "树", "最短路", "最小生成树", "连通性问题",
    "动态规划引入", "线性状态动态规划", "区间与环形动态规划", "树与图上的动态规划",
    "状态压缩动态规划", "动态规划的设计与优化", "进阶数论", "组合数学与计数",
    "概率与统计", "基础线性代数", "线段树的进阶用法",
]


def natural_key(name: str) -> list[object]:
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", name)]


def collect(patterns: list[str]) -> list[Path]:
    seen: set[str] = set()
    paths: list[Path] = []
    for pattern in patterns:
        for path in sorted(MODULES.glob(pattern), key=lambda p: natural_key(p.name)):
            if path.name in seen:
                continue
            seen.add(path.name)
            paths.append(path)
    return paths


def write_volume(filename: str, title: str, subtitle: str, patterns: list[str]) -> None:
    paths = collect(patterns)
    parts = [
        f"# {title}",
        "",
        f"> {subtitle}",
        "",
    ]
    intro = INTRO_BY_FILENAME.get(filename)
    if intro:
        parts.append(intro.rstrip())
        parts.append("")
    for path in paths:
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{path.name} -->")
        parts.append(path.read_text(encoding="utf-8", errors="replace").rstrip())
    out = DRAFTS / filename
    out.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(paths)} modules)")


def write_luogu_index() -> None:
    module_names = {p.name for p in MODULES.glob("*.md")}
    rows = [
        "# 第 8 卷：洛谷题单覆盖索引",
        "",
        "> 根据用户截图中的浅入浅出基础篇/进阶篇主题整理。用于确认纸质资料覆盖面，不作为刷题题解。",
        "",
        "| 截图主题 | 对应资料入口 |",
        "|---|---|",
    ]
    mapping = {
        "顺序结构": "BASIC / CPP-001",
        "分支结构": "BASIC",
        "循环结构": "BASIC / BRUTE",
        "数组": "CPP-002 / DS-00 / 前缀和差分",
        "字符串": "CPP-011 / STR-* / DP-09/10",
        "函数与结构体": "CPP-001 / CPP-002 / GRAPH-00",
        "模拟与高精度": "SIM-01 / CPP-10",
        "排序": "CPP-003 / CPP-012",
        "暴力枚举": "BRUTE-03/04/05/06",
        "递推与递归": "BRUTE-07 / DP-00",
        "贪心": "GREEDY-*",
        "二分查找与二分答案": "CPP-003 / DS-06 / ROUTE",
        "搜索": "BRUTE-06/11/12",
        "线性表": "CPP-013 / DS",
        "二叉树": "TREE-00",
        "集合": "CPP-005 / CPP-006",
        "图的基本应用": "GRAPH-00/01/02",
        "基础数学问题": "MATH-*",
        "前缀和、差分与离散化": "DS-01 / CPP-007",
        "常见优化技巧": "ROUTE / DS / GREEDY",
        "分治与倍增": "DIVIDE-00 / GRAPH-09",
        "进阶搜索": "BRUTE-06/07/11/12",
        "二叉堆与树状数组": "CPP-004 / DS-02",
        "线段树": "DS-03",
        "树": "TREE-* / GRAPH-09 / DP-14",
        "最短路": "GRAPH-02/03/04/12",
        "最小生成树": "GRAPH-06",
        "连通性问题": "GRAPH-01/06/08/13",
        "动态规划引入": "DP-00/01/02/21/22",
        "线性状态动态规划": "DP-03B/04/11/23",
        "区间与环形动态规划": "DP-13 / DP-19",
        "树与图上的动态规划": "DP-14/15 / GRAPH-05",
        "状态压缩动态规划": "DP-16",
        "动态规划的设计与优化": "DP-19/25/26",
        "进阶数论": "MATHREF-02/03",
        "组合数学与计数": "MATH-03 / MATHREF-04 / DP-20",
        "概率与统计": "MATHREF-05",
        "基础线性代数": "MATH-LA-00 / MATH-05",
        "线段树的进阶用法": "DS-03",
    }
    for topic in LUOGU_TOPICS:
        rows.append(f"| {topic} | {mapping.get(topic, 'ROUTE 总表')} |")
    rows += [
        "",
        "## 覆盖校验",
        "",
        f"- 当前模块数：{len(module_names)}。",
        "- 字符串 0-index、mask 位号、数学自然下标是局部例外；普通数组/图/网格/关键点仍按 1-index 口径。",
    ]
    out = DRAFTS / "volume_8_luogu_coverage_index.md"
    out.write_text("\n".join(rows).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {out} (coverage index)")


def main() -> None:
    DRAFTS.mkdir(parents=True, exist_ok=True)
    for filename, title, subtitle, patterns in VOLUMES:
        write_volume(filename, title, subtitle, patterns)


if __name__ == "__main__":
    main()
