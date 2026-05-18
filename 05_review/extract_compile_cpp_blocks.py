from pathlib import Path
import hashlib
import re
import shlex
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "03_modules", ROOT / "04_generated_drafts", ROOT / "06_output"]
REPORT = ROOT / "05_review" / "cpp_compile_report.md"

FENCE_RE = re.compile(r"```(?:cpp|c\+\+)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


def to_wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    rest = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{rest}"


def iter_markdown_files():
    for base in TARGETS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            yield path


def is_standalone(code: str) -> bool:
    return re.search(r"\bint\s+main\s*\(", code) is not None or "// standalone" in code


def compile_with_wsl_gpp(src: Path, exe: Path) -> tuple[bool, list[str]]:
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
    text = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    return proc.returncode == 0, text.splitlines()


def main():
    if shutil.which("wsl.exe") is None and shutil.which("wsl") is None:
        REPORT.write_text("# C++ 编译检查报告\n\n未找到 WSL，无法使用 WSL g++ 编译。\n", encoding="utf-8")
        print(f"Wrote {REPORT}")
        raise SystemExit(1)

    rows = []
    seen: set[str] = set()

    with tempfile.TemporaryDirectory(dir=ROOT / "05_review") as tmp:
        tmpdir = Path(tmp)
        for path in iter_markdown_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            for idx, match in enumerate(FENCE_RE.finditer(text), 1):
                code = match.group(1)
                if not is_standalone(code):
                    continue
                digest = hashlib.sha256(code.strip().encode("utf-8")).hexdigest()[:16]
                if digest in seen:
                    continue
                seen.add(digest)
                src = tmpdir / f"block_{len(rows)}.cpp"
                exe = tmpdir / f"block_{len(rows)}.out"
                src.write_text(code, encoding="utf-8")
                ok, out = compile_with_wsl_gpp(src, exe)
                rows.append((path.relative_to(ROOT), idx, "OK" if ok else "FAIL", out[:8]))

    lines = ["# C++ 编译检查报告", "", "编译器：WSL `g++ -std=c++17 -O2 -pipe -Wall -Wextra -Werror`", ""]
    if not rows:
        lines.append("没有发现可独立编译的 C++ 代码块。")
    else:
        lines.append("| 文件 | 代码块 | 状态 | 摘要 |")
        lines.append("|---|---:|---|---|")
        for rel, idx, status, out in rows:
            summary = "<br>".join(e.replace("|", "\\|") for e in out)
            lines.append(f"| `{rel}` | {idx} | {status} | {summary} |")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    if any(row[2] == "FAIL" for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
