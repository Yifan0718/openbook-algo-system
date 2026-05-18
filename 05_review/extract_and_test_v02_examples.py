from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "04_generated_drafts"
OUT = ROOT / "06_output" / "v02_example_tests"
V02_MARKER = "<!-- V02_EXAMPLES_START -->"


@dataclass
class Example:
    source: Path
    title: str
    code_lang: str
    code: str
    sample_input: str
    sample_output: str


def normalize_output(s: str) -> str:
    lines = [line.rstrip() for line in s.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def wsl_path(path: Path) -> str:
    resolved = path.resolve()
    s = str(resolved)
    if len(s) >= 3 and s[1:3] == ":\\":
        drive = s[0].lower()
        rest = s[3:].replace("\\", "/")
        return f"/mnt/{drive}/{rest}"
    res = subprocess.run(
        ["wsl", "wslpath", "-a", s],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return res.stdout.strip()


def run_wsl(cmd: str, timeout: int = 20) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["wsl", "bash", "-lc", cmd],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def split_examples(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^###\s+([^\n]+)\n", text))
    parts: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        parts.append((match.group(1).strip(), text[start:end]))
    return parts


def first_fenced_after(block: str, label: str, langs: tuple[str, ...] | None = None) -> tuple[str, str] | None:
    pos = block.find(label)
    if pos < 0:
        return None
    tail = block[pos:]
    m = re.search(r"```([A-Za-z0-9_+-]*)\n(.*?)\n```", tail, re.S)
    if not m:
        return None
    lang = m.group(1).strip().lower()
    code = m.group(2)
    if langs is not None and lang not in langs:
        return None
    return lang, code


def extract_examples() -> list[Example]:
    examples: list[Example] = []
    volume_paths = sorted(EXAMPLES_DIR.glob("volume_*.md"))
    if any(V02_MARKER in path.read_text(encoding="utf-8", errors="replace") for path in volume_paths):
        source_paths = volume_paths
    else:
        source_paths = sorted(EXAMPLES_DIR.glob("v02_examples_worker_*.md"))
    for path in source_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for title, block in split_examples(text):
            code_part = first_fenced_after(block, "**完整代码：", ("cpp", "c++", "python", "py"))
            if code_part is None:
                continue
            in_part = first_fenced_after(block, "**样例输入：", None)
            out_part = first_fenced_after(block, "**样例输出：", None)
            if in_part is None or out_part is None:
                continue
            lang, code = code_part
            examples.append(
                Example(
                    source=path,
                    title=title,
                    code_lang="python" if lang in ("python", "py") else "cpp",
                    code=code.strip() + "\n",
                    sample_input=in_part[1],
                    sample_output=out_part[1],
                )
            )
    return examples


def safe_name(title: str, idx: int) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", title).strip("_")
    if not cleaned:
        cleaned = f"example_{idx:03d}"
    return f"{idx:03d}_{cleaned[:80]}"


def test_cpp(ex: Example, stem: str) -> dict[str, object]:
    src = OUT / f"{stem}.cpp"
    exe = OUT / f"{stem}.out"
    inp = OUT / f"{stem}.in"
    src.write_text(ex.code, encoding="utf-8", newline="\n")
    inp.write_text(ex.sample_input, encoding="utf-8", newline="\n")
    src_w = shlex.quote(wsl_path(src))
    exe_w = shlex.quote(wsl_path(exe))
    inp_w = shlex.quote(wsl_path(inp))
    compile_res = run_wsl(f"g++ -std=c++17 -O2 -pipe -Wall -Wextra {src_w} -o {exe_w}", timeout=30)
    if compile_res.returncode != 0:
        return {
            "status": "compile_fail",
            "stderr": compile_res.stderr[-4000:],
        }
    run_res = run_wsl(f"{exe_w} < {inp_w}", timeout=10)
    if run_res.returncode != 0:
        return {
            "status": "runtime_fail",
            "stderr": run_res.stderr[-4000:],
            "stdout": run_res.stdout[-4000:],
        }
    ok = normalize_output(run_res.stdout) == normalize_output(ex.sample_output)
    return {
        "status": "ok" if ok else "wrong_answer",
        "expected": normalize_output(ex.sample_output),
        "actual": normalize_output(run_res.stdout),
    }


def test_python(ex: Example, stem: str) -> dict[str, object]:
    src = OUT / f"{stem}.py"
    inp = OUT / f"{stem}.in"
    src.write_text(ex.code, encoding="utf-8", newline="\n")
    inp.write_text(ex.sample_input, encoding="utf-8", newline="\n")
    res = subprocess.run(
        [sys.executable, str(src)],
        input=ex.sample_input,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
    )
    if res.returncode != 0:
        return {
            "status": "runtime_fail",
            "stderr": res.stderr[-4000:],
            "stdout": res.stdout[-4000:],
        }
    ok = normalize_output(res.stdout) == normalize_output(ex.sample_output)
    return {
        "status": "ok" if ok else "wrong_answer",
        "expected": normalize_output(ex.sample_output),
        "actual": normalize_output(res.stdout),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    examples = extract_examples()
    results = []
    for idx, ex in enumerate(examples, 1):
        stem = safe_name(ex.title, idx)
        if ex.code_lang == "cpp":
            result = test_cpp(ex, stem)
        else:
            result = test_python(ex, stem)
        results.append(
            {
                "index": idx,
                "title": ex.title,
                "source": str(ex.source.relative_to(ROOT)),
                "lang": ex.code_lang,
                **result,
            }
        )
        print(f"[{idx}/{len(examples)}] {result['status']} {ex.code_lang} {ex.title}")
    passed = sum(1 for r in results if r["status"] == "ok")
    failed = len(results) - passed
    report = {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": results,
    }
    (OUT / "v02_example_test_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# v0.2 例题代码测试报告",
        "",
        f"- 总数：{len(results)}",
        f"- 通过：{passed}",
        f"- 失败：{failed}",
        "",
        "| 状态 | 语言 | 题目 | 来源 |",
        "|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['status']} | {r['lang']} | {r['title']} | `{r['source']}` |")
    (OUT / "v02_example_test_report.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
