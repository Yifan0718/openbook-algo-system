from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import re
import shlex
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "03_modules",
    ROOT / "04_generated_drafts",
    ROOT / "06_output",
]
REPORT = ROOT / "05_review" / "second_round_standalone_compile_all.md"

FENCE_RE = re.compile(r"```(?:cpp|c\+\+)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


@dataclass
class CodeUnit:
    digest: str
    code: str
    locations: list[tuple[Path, int]] = field(default_factory=list)
    status: str = "SKIP"
    output: str = ""


def to_wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    rest = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{rest}"


def is_standalone(code: str) -> bool:
    return re.search(r"\bint\s+main\s*\(", code) is not None


def iter_markdown_files() -> list[Path]:
    out: list[Path] = []
    for base in TARGETS:
        if base.is_file():
            out.append(base)
        elif base.exists():
            out.extend(sorted(base.rglob("*.md")))
    return out


def compile_unit(code: str, src: Path, exe: Path) -> tuple[str, str]:
    src.write_text(code, encoding="utf-8")
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
    return ("OK" if proc.returncode == 0 else "FAIL"), text


def main() -> int:
    units: dict[str, CodeUnit] = {}
    total_blocks = 0
    standalone_blocks = 0

    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for idx, match in enumerate(FENCE_RE.finditer(text), 1):
            total_blocks += 1
            code = match.group(1).strip() + "\n"
            if not is_standalone(code):
                continue
            standalone_blocks += 1
            digest = hashlib.sha256(code.encode("utf-8")).hexdigest()[:16]
            unit = units.setdefault(digest, CodeUnit(digest=digest, code=code))
            unit.locations.append((path, idx))

    with tempfile.TemporaryDirectory(dir=ROOT / "05_review") as tmp:
        tmpdir = Path(tmp)
        for seq, unit in enumerate(units.values(), 1):
            unit.status, unit.output = compile_unit(
                unit.code,
                tmpdir / f"unit_{seq}.cpp",
                tmpdir / f"unit_{seq}.out",
            )

    fail_count = sum(1 for unit in units.values() if unit.status == "FAIL")

    lines = [
        "# 第二轮 standalone C++ 全位置编译报告",
        "",
        "编译器：WSL `g++ -std=c++17 -O2 -pipe -Wall -Wextra -Werror`",
        "",
        f"- 扫描 Markdown 文件：{len(iter_markdown_files())}",
        f"- C++ fence 总数：{total_blocks}",
        f"- standalone fence 总数：{standalone_blocks}",
        f"- 去重后 standalone 单元：{len(units)}",
        f"- 失败单元：{fail_count}",
        "",
        "| 状态 | 唯一ID | 出现次数 | 首个位置 | 摘要 |",
        "|---|---|---:|---|---|",
    ]
    for unit in sorted(units.values(), key=lambda u: (u.status != "FAIL", u.digest)):
        first_path, first_idx = unit.locations[0]
        first = f"{first_path.relative_to(ROOT)}#{first_idx}"
        summary = "<br>".join(unit.output.splitlines()[:6]).replace("|", "\\|")
        lines.append(
            f"| {unit.status} | `{unit.digest}` | {len(unit.locations)} | `{first}` | {summary} |"
        )

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"standalone_units={len(units)} failures={fail_count}")
    return 1 if fail_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
