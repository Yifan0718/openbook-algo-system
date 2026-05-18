from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "04_generated_drafts"
OUT = ROOT / "06_output" / "chapter_pdfs"
RELEASE_VERSION = os.environ.get("OPENBOOK_RELEASE_VERSION", "v0.1")
RELEASE_OUT = ROOT / "07_release" / RELEASE_VERSION / "01_print_ready" / "chapter_pdfs"


@dataclass(frozen=True)
class Chapter:
    no: str
    source: str
    pdf: str
    title: str
    when: str
    keywords: str
    detail: str


CHAPTERS = [
    Chapter(
        "00",
        "volume_-1_0A_0_ops_route.md",
        "00_route.pdf",
        "第0卷 作战流程与题型路由",
        "考试开始、读题后不知道翻哪里、需要复杂度/提交策略/统一协议时先翻。",
        "时间分配；复杂度表；题型路由；模块拼接；1-index；提交检查。",
        "先扫三题、判断复杂度、选择题型路由、决定先交暴力还是直接套模板；这里是全套资料的总导航。",
    ),
    Chapter(
        "01",
        "volume_1_cpp_stl.md",
        "01_cpp_stl_io.pdf",
        "第1卷 C++17 / STL / 输入输出",
        "卡在语法、容器、string、格式化输出、EOF、快读快写时翻。",
        "cin/cout；scanf/printf；getline；EOF；string；vector；priority_queue；unordered_map；sort；lower_bound。",
        "主查 C++ 现场写法：标准头文件、输入输出、保留小数、右对齐、EOF、string 成员函数、STL 容器和常用算法。",
    ),
    Chapter(
        "02",
        "volume_2_brute_memo_partial.md",
        "02_brute_memo.pdf",
        "第2卷 暴力、枚举、记忆化与部分分",
        "不会正解、想先交小数据、DFS 能写但会超时时翻。",
        "枚举；全排列；子集；DFS；BFS 状态；剪枝；记忆化；折半；合法兜底输出。",
        "主查拿分底线：全排列、子集枚举、组合 DFS、BFS 状态搜索、剪枝、DFS 加 memo、折半枚举和大数据合法兜底。",
    ),
    Chapter(
        "03",
        "volume_3_dp_model_reuse.md",
        "03_dp.pdf",
        "第3卷 DP 建模与模型复用",
        "疑似 DP、需要从暴力升级到记忆化/表推、不会定义状态时翻。",
        "DP 五问；线性；背包；LIS/LCS/LCIS；区间；树形；DAG；状压；数位；例题推导。",
        "主查 DP 怎么想：从暴力搜索找状态、加记忆化、再表推；覆盖背包、LIS/LCS/LCIS、区间、树形、DAG、状压、数位和高阶索引。",
    ),
    Chapter(
        "03A",
        "volume_3A_greedy_dp_discrimination.md",
        "03A_greedy_dp.pdf",
        "第3A卷 贪心与 DP 辨析",
        "不知道能不能贪心、需要证明交换/反例、贪心失败要转 DP 时翻。",
        "排序贪心；区间；堆；局部最优；反例；DP 对照。",
        "主查贪心能不能用：看是否有交换论证、排序依据、堆维护、区间选择；一旦局部选择影响未来就转 DP 或搜索。",
    ),
    Chapter(
        "04",
        "volume_4_data_structures.md",
        "04_ds.pdf",
        "第4卷 数据结构",
        "区间查询修改、动态排名、前缀和、差分、线段树/树状数组时翻。",
        "前缀和；差分；双指针；单调栈队列；堆；DSU；树状数组；线段树；Sparse Table。",
        "主查数组和区间工具：前缀和/差分、双指针、单调结构、堆、并查集、树状数组、线段树、Sparse Table 和坐标压缩拼接。",
    ),
    Chapter(
        "05",
        "volume_5_graph_tree.md",
        "05_graph_tree.pdf",
        "第5卷 图论与树论",
        "图/网格/树题，最短路、连通性、拓扑、LCA、树 DP 时翻。",
        "BFS/DFS；Dijkstra；Floyd；Bellman-Ford；DSU；MST；Topo；SCC；LCA；树形 DP。",
        "主查图树模板：统一 1-index 建图、无权 BFS、非负权 Dijkstra、小图 Floyd、拓扑、最小生成树、强连通、LCA 和树上 DP。",
    ),
    Chapter(
        "06",
        "volume_6_math_string.md",
        "06_math_string.pdf",
        "第6卷 数学与字符串模板",
        "快速幂、组合数、筛法、方程求解、KMP、Trie、Hash、字符串 DP 时翻。",
        "gcd/lcm；快速幂；逆元；组合数；筛；质因数；高斯消元；二分求根；KMP；Z；Trie；Hash；Manacher。",
        "主查常用数学与字符串：gcd/lcm、模运算、快速幂、逆元、组合数、筛法、质因数分解、方程组求解、一元方程求根、KMP/Z、Trie、Hash 和 Manacher。",
    ),
    Chapter(
        "07",
        "volume_7_debug_training.md",
        "07_debug.pdf",
        "第7卷 调试、对拍与训练",
        "样例过但 WA/RE/TLE、需要自造极限数据或赛后训练时翻。",
        "边界；对拍；随机数据；提交前检查；常见错误。",
        "主查最后救命检查：边界样例、随机对拍、RE/WA/TLE 排查、提交前检查清单和赛后训练方法。",
    ),
    Chapter(
        "08",
        "volume_8_competition_math_reference.md",
        "08_math_ref.pdf",
        "第8卷 竞赛数学参考",
        "数学题更深，涉及同余、CRT、莫比乌斯、矩阵、概率、博弈、几何时翻。",
        "整除；同余；exgcd；CRT；欧拉/莫比乌斯；容斥；矩阵快速幂；期望；SG；几何。",
        "主查 NOI/ICPC 风格数学补充：整除与取整、线性同余、exgcd、CRT、欧拉/莫比乌斯、容斥、矩阵、期望、SG 和几何精度。",
    ),
    Chapter(
        "09",
        "volume_9_python_complement.md",
        "09_python.pdf",
        "第9卷 Python 互补卷",
        "只有 Python 明显更省事时翻，主力仍建议 C++。",
        "大整数；字典/集合；heapq；deque；itertools；输入；递归限制；适用/不适用场景。",
        "主查 Python 是否值得用：大整数、字典集合、heapq、deque、itertools、简单模拟和状态搜索；复杂图/区间仍优先 C++。",
    ),
    Chapter(
        "10",
        "volume_10_ai_special_topics.md",
        "10_ai.pdf",
        "第10卷 AI 专题与特判模型",
        "题面带 AI/ML/聚类/回归/神经网络/自动求导/模型评测时翻。",
        "搜索规划；KNN；TF-IDF；聚类；回归；Viterbi；DNN；SVM；反向传播；自动求导；SPJ。",
        "主查 AI 相关模拟题：搜索规划、KNN、相似度、TF-IDF、聚类、回归、HMM/Viterbi、SVM、DNN、反向传播、自动求导和 SPJ。",
    ),
    Chapter(
        "11",
        "volume_11_signoff_encyclopedia.md",
        "11_signoff_encyclopedia.pdf",
        "第11卷 签到题百科",
        "题面是公式、单位、图片大小、日期、统计指标、机器学习小模拟或计算机常识时翻。",
        "BMP；三角形面积；单位换算；微积分；线性代数；Markov；概率统计；F1；kNN；bit/byte；补码；浮点；流程图；AI术语；日期；Excel列号。",
        "主查签到题常识：常用数学、微积分、线代、Markov、概率统计、机器学习指标、文件媒体大小、进制补码浮点、读程序流程图、编码网络和生活模拟模板。",
    ),
]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def page_count(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


def latex_escape(s: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in s)


def build_chapter_pdf(ch: Chapter) -> Path:
    src = DRAFTS / ch.source
    if not src.exists():
        raise FileNotFoundError(src)
    build_dir = OUT / "_build_md"
    build_dir.mkdir(parents=True, exist_ok=True)
    work_src = build_dir / ch.source
    original = src.read_text(encoding="utf-8")
    title_line = ch.title
    subtitle_line = f"考试速查：{ch.detail}"
    first_heading = f"# \\textcolor{{red}}{{{latex_escape(title_line)}}}\n\n"
    quick_block = (
        "## 考试速查定位\n\n"
        f"**{ch.title}**\n\n"
        f"- **这是第几卷：** {ch.no}。\n"
        f"- **主要查什么：** {ch.detail}\n"
        f"- **什么时候翻：** {ch.when}\n"
        f"- **题面关键词：** {ch.keywords}\n\n"
    )
    lines = original.splitlines()
    if lines and lines[0].startswith("# "):
        body = "\n".join(lines[1:]).lstrip() + "\n"
    else:
        body = original
    yaml = (
        "---\n"
        f"title: \"\\\\textcolor{{red}}{{{latex_escape(title_line)}}}\"\n"
        f"subtitle: \"\\\\small {latex_escape(subtitle_line)}\"\n"
        "header-includes:\n"
        "  - \\usepackage{xcolor}\n"
        "---\n\n"
    )
    work_src.write_text(yaml + first_heading + quick_block + body, encoding="utf-8")
    out = OUT / ch.pdf
    run(
        [
            "pandoc",
            str(work_src),
            "-o",
            str(out),
            "--pdf-engine=xelatex",
            "-V",
            "CJKmainfont=Microsoft YaHei",
            "-V",
            "monofont=Consolas",
            "-V",
            "papersize=a4",
            "-V",
            "geometry:margin=1.5cm",
            "--toc",
        ]
    )
    return out


def write_index_md() -> Path:
    path = OUT / "00_which_book_index.md"
    lines = [
        "# 翻哪本书：一页索引",
        "",
        "使用方式：先看题面关键词和数据范围，再按本表选择要打印/翻阅的分卷。",
        "",
        "| 编号 | PDF | 什么时候翻 | 关键词 |",
        "|---|---|---|---|",
    ]
    for ch in CHAPTERS:
        lines.append(f"| {ch.no} | `{ch.pdf}`<br>{ch.title} | {ch.when} | {ch.keywords} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_index_tex() -> Path:
    path = OUT / "00_which_book_index.tex"
    cards = []
    for ch in CHAPTERS:
        cards.append(
            r"\BookCard"
            + "{"
            + latex_escape(ch.no)
            + "}{"
            + latex_escape(ch.title)
            + "}{"
            + latex_escape(ch.pdf)
            + "}{"
            + latex_escape(ch.when)
            + "}{"
            + latex_escape(ch.keywords)
            + "}"
        )
    row_lines = []
    for i in range(0, len(cards), 2):
        left = cards[i]
        right = cards[i + 1] if i + 1 < len(cards) else r"\vphantom{\BookCard{00}{空}{empty.pdf}{空}{空}}"
        row_lines.append(left + " & " + right + r" \\[4pt]")
    tex = r"""
\documentclass[9pt]{article}
\usepackage[a4paper,portrait,margin=0.85cm]{geometry}
\usepackage{fontspec}
\usepackage{xeCJK}
\setmainfont{Arial}
\setCJKmainfont{Microsoft YaHei}
\usepackage{array}
\usepackage{xcolor}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\tabcolsep}{0pt}
\renewcommand{\arraystretch}{1}
\newcommand{\BookCard}[5]{%
  \fcolorbox{black}{gray!4}{%
    \begin{minipage}[t][3.28cm][t]{0.456\textwidth}
      \raggedright
      {\fontsize{10.0pt}{11.4pt}\selectfont\bfseries #1\quad #2}\par
      \vspace{1pt}
      {\fontsize{7.6pt}{8.4pt}\selectfont\ttfamily #3}\par
      \vspace{1pt}
      {\fontsize{8.0pt}{9.2pt}\selectfont\bfseries 翻：}{\fontsize{8.0pt}{9.2pt}\selectfont #4}\par
      \vspace{1pt}
      {\fontsize{8.0pt}{9.2pt}\selectfont\bfseries 词：}{\fontsize{8.0pt}{9.2pt}\selectfont #5}
    \end{minipage}%
  }%
}
\begin{document}
\begin{center}
{\fontsize{18pt}{20pt}\selectfont\bfseries 纸质版算法作战系统：翻哪本书}\\[3pt]
{\fontsize{9.6pt}{11pt}\selectfont 先看题面关键词和数据范围，再选择对应分卷。主力语言：C++17；所有代码默认标准输入输出。}
\end{center}
\vspace{4pt}
\begin{tabular}{@{}p{0.492\textwidth}@{\hspace{0.35cm}}p{0.492\textwidth}@{}}
"""
    tex += "\n".join(row_lines)
    tex += r"""
\end{tabular}
\vfill

\fcolorbox{black}{gray!8}{\begin{minipage}{0.972\textwidth}
{\fontsize{9pt}{10.5pt}\selectfont
\textbf{装订建议：}00/01 放最前；02 和 03 高频；04/05/06 是模板主力；08/09/10/11 作为补充。考试中先交部分分，再升级。}
\end{minipage}}
\end{document}
"""
    path.write_text(tex, encoding="utf-8")
    return path


def build_index_pdf() -> Path:
    write_index_md()
    tex = write_index_tex()
    run(["xelatex", "-halt-on-error", "-interaction", "nonstopmode", tex.name], cwd=OUT)
    pdf = OUT / "00_which_book_index.pdf"
    if page_count(pdf) != 1:
        raise RuntimeError(f"index PDF must be one page, got {page_count(pdf)}")
    return pdf


def sync_release(paths: list[Path]) -> None:
    RELEASE_OUT.mkdir(parents=True, exist_ok=True)
    failures = []
    for path in paths:
        dst = RELEASE_OUT / path.name
        try:
            shutil.copy2(path, dst)
        except PermissionError:
            failures.append(dst)
    if failures:
        joined = "\n".join(str(path) for path in failures)
        raise PermissionError(
            "这些发布目录文件正在被打开，无法覆盖。请关闭对应 PDF 后重跑：\n"
            + joined
        )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RELEASE_OUT.mkdir(parents=True, exist_ok=True)
    for pattern in ("*.pdf", "*.md", "*.json", "*.aux", "*.log", "*.tex"):
        for path in OUT.glob(pattern):
            path.unlink()
    build_md_dir = OUT / "_build_md"
    if build_md_dir.exists():
        for path in build_md_dir.glob("*.md"):
            path.unlink()
    built: list[Path] = []
    built.append(build_index_pdf())
    for ch in CHAPTERS:
        built.append(build_chapter_pdf(ch))

    records = []
    for path in built:
        records.append(
            {
                "file": path.name,
                "pages": page_count(path),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )

    manifest = {
        "version": RELEASE_VERSION.removeprefix("v"),
        "kind": "chapter_pdfs",
        "count": len(records),
        "output_dir": str(OUT),
        "chapters": [
            {
                "no": ch.no,
                "title": ch.title,
                "pdf": ch.pdf,
                "source": ch.source,
                "when": ch.when,
                "keywords": ch.keywords,
                "detail": ch.detail,
            }
            for ch in CHAPTERS
        ],
        "files": records,
    }
    (OUT / "chapter_pdf_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_lines = [
        "# 分卷 PDF 清单",
        "",
        "| 文件 | 页数 | 用途 |",
        "|---|---:|---|",
    ]
    record_by_file = {r["file"]: r for r in records}
    summary_lines.append("| `00_which_book_index.pdf` | 1 | 一页索引：翻哪本书 |")
    for ch in CHAPTERS:
        summary_lines.append(
            f"| `{ch.pdf}` | {record_by_file[ch.pdf]['pages']} | {ch.title} |"
        )
    (OUT / "chapter_pdf_manifest.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )

    built.extend([OUT / "chapter_pdf_manifest.json", OUT / "chapter_pdf_manifest.md", OUT / "00_which_book_index.md"])
    sync_release(built)

    print("CHAPTER PDF BUILD COMPLETE")
    for record in records:
        print(f"{record['file']}: {record['pages']} pages, sha256={record['sha256'][:16]}...")


if __name__ == "__main__":
    main()
