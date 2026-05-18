from __future__ import annotations

from datetime import date
from pathlib import Path
import hashlib
import json
import os
import shutil
import zipfile

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "06_output"
REVIEW = ROOT / "05_review"
REL_ROOT = ROOT / "07_release"
VERSION = os.environ.get("OPENBOOK_RELEASE_VERSION", "0.2").removeprefix("v")
REL = REL_ROOT / f"v{VERSION}"


PRINT_PDFS = [
    "openbook_core.pdf",
    "openbook_full.pdf",
    "openbook_printable_full.pdf",
]

CHAPTER_PDFS = [
    "00_route.pdf",
    "00_which_book_index.pdf",
    "01_cpp_stl_io.pdf",
    "02_brute_memo.pdf",
    "03_dp.pdf",
    "03A_greedy_dp.pdf",
    "04_ds.pdf",
    "05_graph_tree.pdf",
    "06_math_string.pdf",
    "07_debug.pdf",
    "08_math_ref.pdf",
    "09_python.pdf",
    "10_ai.pdf",
    "11_signoff_encyclopedia.pdf",
]

REVIEW_FILES = [
    REVIEW / "README.md",
    REVIEW / "core_pack_selection_notes.md",
    REVIEW / "cpp_block_inventory.md",
    REVIEW / "cpp_compile_report.md",
    REVIEW / "cpp_pseudocode_report.md",
    REVIEW / "cpp_wsl_audit_report.md",
    REVIEW / "forbidden_patterns_report.md",
    REVIEW / "index_policy_report.md",
    REVIEW / "module_fields_report.md",
    REVIEW / "python_syntax_report.md",
    REVIEW / "second_round_module_matrix.md",
    REVIEW / "second_round_standalone_compile_all.md",
    REVIEW / "standalone_runtime_manifest.json",
    REVIEW / "standalone_runtime_test_report.md",
    REVIEW / "template_consistency_report.md",
    REVIEW / "signoff_v02_final_report.md",
    REVIEW / f"signoff_v{VERSION.replace('.', '')}_final_report.md",
    OUT / "v02_example_integration_report.md",
    OUT / "v02_example_structure_audit.json",
    OUT / "v02_example_structure_audit.md",
    OUT / "v02_example_tests" / "v02_example_test_report.json",
    OUT / "v02_example_tests" / "v02_example_test_report.md",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pages(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def clean_release_dir() -> None:
    rel_resolved = REL.resolve()
    expected_parent = (ROOT / "07_release").resolve()
    if rel_resolved.parent != expected_parent or rel_resolved.name != f"v{VERSION}":
        raise RuntimeError(f"refuse to remove unexpected release path: {rel_resolved}")
    if REL.exists():
        shutil.rmtree(REL)
    REL.mkdir(parents=True, exist_ok=True)


def copy_optional_file(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    copy_file(src, dst)
    return True


def build_release() -> dict:
    clean_release_dir()

    write_text(REL / "VERSION", VERSION)
    write_text(
        REL / "README.md",
        f"""
# 纸质版算法作战系统 v{VERSION}

这是用于北京中关村学院夏令营机考的纸质开卷资料包。

主力语言：C++17。资料目标是考场快速路由、模块化拼接、先拿部分分再升级。

许可证：MIT License。详见 `LICENSE`。

## 目录

- `01_print_ready/`：可直接打印的 PDF。
- `01_print_ready/chapter_pdfs/`：每卷单独 PDF，适合一本一本打印。
- `02_markdown_source/`：本次发布对应的 Markdown 源稿。
- `03_review_reports/`：本次发布的自动审计和 signoff 报告。
- `LICENSE`：MIT 许可证文本。

优先打印：`00_which_book_index.pdf`、`00_route.pdf`、`01_cpp_stl_io.pdf`、`02_brute_memo.pdf`、`03_dp.pdf`、`04_ds.pdf`、`05_graph_tree.pdf`、`06_math_string.pdf`、`11_signoff_encyclopedia.pdf`。
""",
    )
    write_text(
        REL / "00_PRINT_GUIDE.md",
        f"""
# v{VERSION} 打印指南

1. 先打印 `01_print_ready/chapter_pdfs/00_which_book_index.pdf`，考试时用它决定翻哪本。
2. 分卷打印优先于总 PDF：每章一本，更容易现场查。
3. `openbook_core.pdf` 是较薄核心版；`openbook_printable_full.pdf` 是完整自包含版。
4. 每卷末尾包含实战例题训练区，例题代码已通过样例级运行测试。
5. 主力语言仍建议 C++17；Python 卷只在明显省事时作为互补。
""",
    )

    for name in PRINT_PDFS:
        copy_file(OUT / name, REL / "01_print_ready" / name)
    for name in ["openbook_core.md", "openbook_full.md", "openbook_printable_full.md"]:
        copy_file(OUT / name, REL / "02_markdown_source" / name)

    chapter_dir = OUT / "chapter_pdfs"
    rel_chapter = REL / "01_print_ready" / "chapter_pdfs"
    for name in CHAPTER_PDFS:
        copy_file(chapter_dir / name, rel_chapter / name)
    for name in ["00_which_book_index.md", "chapter_pdf_manifest.json", "chapter_pdf_manifest.md"]:
        copy_file(chapter_dir / name, rel_chapter / name)

    copy_file(ROOT / "LICENSE", REL / "LICENSE")
    copy_optional_file(ROOT / f"RELEASE_NOTES_v{VERSION}.md", REL / f"RELEASE_NOTES_v{VERSION}.md")

    copied_reports: list[str] = []
    for src in REVIEW_FILES:
        dst = REL / "03_review_reports" / src.name
        if copy_optional_file(src, dst):
            copied_reports.append(str(dst.relative_to(REL)).replace("\\", "/"))

    outputs = []
    for name in PRINT_PDFS:
        path = REL / "01_print_ready" / name
        role = {
            "openbook_core.pdf": "core printable pdf",
            "openbook_full.pdf": "full pdf",
            "openbook_printable_full.pdf": "self-contained printable pdf",
        }[name]
        outputs.append({"path": str(path.relative_to(REL)).replace("\\", "/"), "role": role, "pages": pages(path)})

    chapter_entries = []
    for name in CHAPTER_PDFS:
        path = rel_chapter / name
        chapter_entries.append({"path": str(path.relative_to(REL)).replace("\\", "/"), "pages": pages(path)})
    outputs.append(
        {
            "path": "01_print_ready/chapter_pdfs",
            "role": "one PDF per volume for separate printing",
            "files": len(CHAPTER_PDFS),
        }
    )

    example_report = json.loads((OUT / "v02_example_tests" / "v02_example_test_report.json").read_text(encoding="utf-8"))
    structure_report = json.loads((OUT / "v02_example_structure_audit.json").read_text(encoding="utf-8"))
    structure_issues = structure_report.get("issues", 0)
    if isinstance(structure_issues, list):
        structure_issues = len(structure_issues)
    manifest = {
        "name": "zhongguancun-algo-openbook-system",
        "version": VERSION,
        "license": "MIT",
        "release_date": str(date.today()),
        "purpose": "C++17 paper open-book algorithm contest combat system with complete tested examples.",
        "example_summary": {
            "total_examples": int(example_report["total"]),
            "structure_audit_issues": int(structure_issues),
            "sample_runtime_tests": int(example_report["total"]),
            "sample_runtime_passed": int(example_report["passed"]),
            "sample_runtime_failed": int(example_report["failed"]),
        },
        "outputs": outputs,
        "chapter_pdfs": chapter_entries,
        "included_review_reports": copied_reports,
        "license_file": "LICENSE",
    }
    write_text(REL / "MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    sha_lines = []
    for path in sorted(p for p in REL.rglob("*") if p.is_file()):
        rel = str(path.relative_to(REL)).replace("\\", "/")
        sha_lines.append(f"{sha256_file(path)}  {rel}")
    write_text(REL / "SHA256SUMS.txt", "\n".join(sha_lines))

    zip_path = REL_ROOT / f"openbook-v{VERSION}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in REL.rglob("*") if p.is_file()):
            arc = Path(f"v{VERSION}") / path.relative_to(REL)
            zf.write(path, arc.as_posix())
    write_text(REL_ROOT / f"openbook-v{VERSION}.zip.sha256.txt", f"{sha256_file(zip_path)}  {zip_path.name}")
    return manifest


def main() -> None:
    manifest = build_release()
    print(f"published v{VERSION}")
    print(f"main outputs={len(manifest['outputs'])}")
    print(f"chapter pdfs={len(manifest['chapter_pdfs'])}")
    print(f"reports={len(manifest['included_review_reports'])}")


if __name__ == "__main__":
    main()
