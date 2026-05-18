from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import json
import re
import shlex
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "05_review"
TARGETS = [
    ROOT / "03_modules",
    ROOT / "04_generated_drafts",
    ROOT / "06_output",
]
MANIFEST = REVIEW / "standalone_runtime_manifest.json"
REPORT = REVIEW / "standalone_runtime_test_report.md"

FENCE_RE = re.compile(r"```(?:cpp|c\+\+)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
MAIN_RE = re.compile(r"\bint\s+main\s*\(")


@dataclass
class Location:
    path: Path
    fence_index: int


@dataclass
class CodeUnit:
    digest: str
    code: str
    locations: list[Location] = field(default_factory=list)
    compile_status: str = "SKIP"
    compile_output: str = ""


@dataclass
class CaseResult:
    digest: str
    name: str
    status: str
    expected: str
    actual: str
    stderr: str
    returncode: int | None
    detail: str


def to_wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    rest = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{rest}"


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def md_cell(text: str, limit: int = 160) -> str:
    text = normalize(text)
    if len(text) > limit:
        text = text[:limit] + "..."
    return text.replace("\\", "\\\\").replace("\n", "<br>").replace("|", "\\|")


def is_standalone(code: str) -> bool:
    return MAIN_RE.search(code) is not None


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for base in TARGETS:
        if base.is_file():
            files.append(base)
        elif base.exists():
            files.extend(sorted(base.rglob("*.md")))
    return files


def extract_units() -> dict[str, CodeUnit]:
    units: dict[str, CodeUnit] = {}
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for idx, match in enumerate(FENCE_RE.finditer(text), 1):
            code = match.group(1).strip() + "\n"
            if not is_standalone(code):
                continue
            digest = hashlib.sha256(code.encode("utf-8")).hexdigest()[:16]
            unit = units.setdefault(digest, CodeUnit(digest=digest, code=code))
            unit.locations.append(Location(path=path, fence_index=idx))
    return units


def compile_unit(unit: CodeUnit, src: Path, exe: Path) -> None:
    src.write_text(unit.code, encoding="utf-8")
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
    unit.compile_status = "OK" if proc.returncode == 0 else "FAIL"
    unit.compile_output = normalize(((proc.stdout or "") + "\n" + (proc.stderr or "")).strip())


def run_case(exe: Path, digest: str, case: dict, default_timeout_ms: int, default_compare: str) -> CaseResult:
    name = str(case.get("name", "unnamed"))
    stdin = str(case.get("stdin", ""))
    expected = normalize(str(case.get("stdout", "")))
    timeout_ms = int(case.get("timeout_ms", default_timeout_ms))
    compare = str(case.get("compare", default_compare))

    cmd = f"timeout {max(1, (timeout_ms + 999) // 1000)}s {shlex.quote(to_wsl_path(exe))}"
    try:
        proc = subprocess.run(
            ["wsl.exe", "--", "bash", "-lc", cmd],
            cwd=ROOT,
            input=stdin,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=max(2, timeout_ms / 1000 + 2),
        )
    except subprocess.TimeoutExpired as exc:
        return CaseResult(
            digest=digest,
            name=name,
            status="TIMEOUT",
            expected=expected,
            actual=normalize(exc.stdout or ""),
            stderr=normalize(exc.stderr or ""),
            returncode=None,
            detail=f"Python timeout after {timeout_ms}ms",
        )

    actual = normalize(proc.stdout or "")
    stderr = normalize(proc.stderr or "")
    if proc.returncode == 124:
        status = "TIMEOUT"
        detail = f"process timeout after {timeout_ms}ms"
    elif proc.returncode != 0:
        status = "RUNTIME_FAIL"
        detail = f"exit code {proc.returncode}"
    else:
        if compare == "exact":
            ok = actual == expected
        elif compare == "tokens":
            ok = actual.split() == expected.split()
        elif compare == "trim":
            ok = actual.strip() == expected.strip()
        else:
            ok = False
        status = "OK" if ok else "WRONG_OUTPUT"
        detail = f"compare={compare}"

    return CaseResult(
        digest=digest,
        name=name,
        status=status,
        expected=expected,
        actual=actual,
        stderr=stderr,
        returncode=proc.returncode,
        detail=detail,
    )


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    tests: dict[str, list[dict]] = manifest["tests"]
    defaults = manifest.get("defaults", {})
    default_timeout_ms = int(defaults.get("timeout_ms", 2000))
    default_compare = str(defaults.get("compare", "trim"))

    units = extract_units()
    unit_digests = set(units)
    manifest_digests = set(tests)
    missing = sorted(unit_digests - manifest_digests)
    stale = sorted(manifest_digests - unit_digests)

    results: list[CaseResult] = []
    compile_failures: list[CodeUnit] = []
    no_case: list[str] = []

    with tempfile.TemporaryDirectory(dir=REVIEW) as tmp:
        tmpdir = Path(tmp)
        for seq, digest in enumerate(sorted(units), 1):
            unit = units[digest]
            src = tmpdir / f"unit_{seq}_{digest}.cpp"
            exe = tmpdir / f"unit_{seq}_{digest}.out"
            compile_unit(unit, src, exe)
            if unit.compile_status != "OK":
                compile_failures.append(unit)
                continue
            if digest not in tests:
                continue
            if not tests[digest]:
                no_case.append(digest)
                continue
            for case in tests[digest]:
                results.append(run_case(exe, digest, case, default_timeout_ms, default_compare))

    failed_results = [r for r in results if r.status != "OK"]
    first_locations = {
        digest: f"{unit.locations[0].path.relative_to(ROOT)}#{unit.locations[0].fence_index}"
        for digest, unit in units.items()
    }

    lines = [
        "# Standalone C++ 运行测试报告",
        "",
        "编译器：WSL `g++ -std=c++17 -O2 -pipe -Wall -Wextra -Werror`",
        "",
        f"- 唯一 standalone 单元：{len(units)}",
        f"- manifest 覆盖单元：{len(manifest_digests & unit_digests)}",
        f"- 未登记运行用例单元：{len(missing)}",
        f"- manifest 过期单元：{len(stale)}",
        f"- 编译失败单元：{len(compile_failures)}",
        f"- 运行用例数：{len(results)}",
        f"- 运行失败用例：{len(failed_results)}",
        "",
    ]

    if missing:
        lines += [
            "## 未登记运行用例（覆盖提示，不代表失败）",
            "",
            "这些 standalone 程序已经由编译审计覆盖；组合例题另由 `v02_example_test_report.md` 做样例运行测试。",
            "",
        ]
        for digest in missing:
            lines.append(f"- `{digest}` at `{first_locations[digest]}`")
        lines.append("")

    if stale:
        lines += ["## Manifest 过期", ""]
        for digest in stale:
            lines.append(f"- `{digest}`")
        lines.append("")

    if compile_failures:
        lines += ["## 编译失败", "", "| digest | 首个位置 | 输出 |", "|---|---|---|"]
        for unit in compile_failures:
            lines.append(
                f"| `{unit.digest}` | `{first_locations[unit.digest]}` | {md_cell(unit.compile_output, 600)} |"
            )
        lines.append("")

    if no_case:
        lines += ["## 无运行用例", ""]
        for digest in no_case:
            lines.append(f"- `{digest}` at `{first_locations[digest]}`")
        lines.append("")

    lines += [
        "## 用例结果",
        "",
        "| 状态 | digest | 首个位置 | 用例 | 期望 stdout | 实际 stdout | stderr | 细节 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for result in sorted(results, key=lambda r: (r.status != "OK", r.digest, r.name)):
        lines.append(
            "| "
            f"{result.status} | `{result.digest}` | `{first_locations.get(result.digest, '')}` | "
            f"{md_cell(result.name, 80)} | {md_cell(result.expected)} | {md_cell(result.actual)} | "
            f"{md_cell(result.stderr)} | {md_cell(result.detail, 80)} |"
        )

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(
        "runtime_units="
        f"{len(units)} cases={len(results)} missing={len(missing)} stale={len(stale)} "
        f"compile_failures={len(compile_failures)} runtime_failures={len(failed_results)}"
    )

    has_failure = bool(stale or compile_failures or failed_results)
    return 1 if has_failure else 0


if __name__ == "__main__":
    sys.exit(main())
