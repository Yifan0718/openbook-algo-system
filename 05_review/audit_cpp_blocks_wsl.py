from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shlex
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
REPORT = ROOT / "05_review" / "cpp_wsl_audit_report.md"
INVENTORY = ROOT / "05_review" / "cpp_block_inventory.md"

FENCE_RE = re.compile(r"```(?:cpp|c\+\+)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
LINE_START_RE = re.compile(r"```(?:cpp|c\+\+)\s*$", re.IGNORECASE)


@dataclass
class Block:
    path: Path
    index: int
    start_line: int
    code: str


def to_wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    rest = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{rest}"


def iter_blocks() -> list[Block]:
    blocks: list[Block] = []
    for path in sorted(MODULES.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        line_no = 1
        idx = 0
        in_cpp = False
        start = 0
        buf: list[str] = []
        for raw in text.splitlines():
            if not in_cpp and LINE_START_RE.match(raw):
                in_cpp = True
                start = line_no + 1
                buf = []
            elif in_cpp and raw.strip() == "```":
                idx += 1
                blocks.append(Block(path, idx, start, "\n".join(buf).rstrip() + "\n"))
                in_cpp = False
            elif in_cpp:
                buf.append(raw)
            line_no += 1
    return blocks


def has_main(code: str) -> bool:
    return re.search(r"\bint\s+main\s*\(", code) is not None


def has_prelude(code: str) -> bool:
    return "#include" in code


def has_bad_placeholder(code: str) -> bool:
    return "TODO" in code or "FIXME" in code or re.search(r"(^|[^.])\.\.\.([^.]|$)", code) is not None


def has_free_statements(code: str) -> bool:
    stripped = re.sub(r"//.*", "", code)
    stripped = re.sub(r"/\*.*?\*/", "", stripped, flags=re.DOTALL)
    depth = 0
    for line in stripped.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if depth == 0:
            if re.match(r"(using|typedef|const|static|struct|class|template|namespace|enum)\b", s):
                pass
            elif re.match(r"(int|long long|ll|bool|char|double|void|string|vector<|pair<|map<|set<|queue<|deque<|priority_queue<|unordered_|auto)\b.*[;{]", s):
                pass
            else:
                return True
        depth += s.count("{") - s.count("}")
    return False


def classify(block: Block) -> str:
    code = block.code
    if has_bad_placeholder(code):
        return "bad-placeholder"
    if has_main(code):
        return "standalone"
    if has_free_statements(code):
        return "fragment"
    return "snippet"


def compile_code(src: Path, exe: Path) -> tuple[bool, str]:
    cmd = (
        "g++ -std=c++17 -O2 -pipe -Wall -Wextra -Werror "
        f"{shlex.quote(to_wsl_path(src))} -o {shlex.quote(to_wsl_path(exe))}"
    )
    proc = subprocess.run(
        ["wsl.exe", "--", "bash", "-lc", cmd],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    out = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    return proc.returncode == 0, out


def main() -> None:
    blocks = iter_blocks()
    inv_lines = [
        "# C++ 代码块清单",
        "",
        "| 文件 | 块 | 行 | 分类 | main | include |",
        "|---|---:|---:|---|---|---|",
    ]
    rows: list[tuple[Block, str, str, str]] = []

    with tempfile.TemporaryDirectory(dir=ROOT / "05_review") as tmp:
        tmpdir = Path(tmp)
        for seq, block in enumerate(blocks, 1):
            kind = classify(block)
            inv_lines.append(
                f"| `{block.path.relative_to(ROOT)}` | {block.index} | {block.start_line} | {kind} | "
                f"{'Y' if has_main(block.code) else ''} | {'Y' if has_prelude(block.code) else ''} |"
            )
            if kind == "standalone":
                code = block.code
            elif kind == "snippet":
                code = (
                    "#include <bits/stdc++.h>\n"
                    "using namespace std;\n"
                    "using ll = long long;\n"
                    "const int INF = 1000000000;\n"
                    "const ll LINF = 4'000'000'000'000'000'000LL;\n"
                    "const int MOD = 1000000007;\n\n"
                    + block.code
                    + "\nint main() { return 0; }\n"
                )
            else:
                continue

            src = tmpdir / f"block_{seq}.cpp"
            exe = tmpdir / f"block_{seq}.out"
            src.write_text(code, encoding="utf-8")
            ok, output = compile_code(src, exe)
            if ok:
                status = "OK"
            elif kind == "standalone":
                status = "FAIL"
            else:
                status = "CONTEXT"
            rows.append((block, kind, status, output))

    INVENTORY.write_text("\n".join(inv_lines) + "\n", encoding="utf-8")

    lines = [
        "# WSL g++ C++ 代码块审计",
        "",
        f"- 模块文件：{len(list(MODULES.glob('*.md')))}",
        f"- C++ 代码块：{len(blocks)}",
        f"- 编译尝试：{len(rows)}（standalone + snippet 包壳）",
        f"- standalone 编译失败：{sum(1 for _, kind, status, _ in rows if kind == 'standalone' and status == 'FAIL')}",
        f"- snippet 需要上下文：{sum(1 for _, kind, status, _ in rows if kind == 'snippet' and status == 'CONTEXT')}（不代表完整程序错误，只作为人工审计线索）",
        "",
        "| 文件 | 块 | 行 | 分类 | 状态 | 摘要 |",
        "|---|---:|---:|---|---|---|",
    ]
    for block, kind, status, output in rows:
        summary = "<br>".join(output.splitlines()[:5]).replace("|", "\\|")
        lines.append(
            f"| `{block.path.relative_to(ROOT)}` | {block.index} | {block.start_line} | {kind} | {status} | {summary} |"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {INVENTORY}")
    print(f"Wrote {REPORT}")
    hard_fail = any(
        kind == "standalone" and status == "FAIL"
        for _, kind, status, _ in rows
    )
    if hard_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
