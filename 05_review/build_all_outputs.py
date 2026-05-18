from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

BUILD_STEPS = [
    "build_remaining_drafts.py",
    "build_volume_1_cpp_stl.py",
    "build_volume_3_dp.py",
    "build_volume_3A_greedy_dp.py",
    "build_volume_4_data_structures.py",
    "build_volume_5_graph_tree.py",
    "integrate_v02_examples.py",
    "build_core_markdown.py",
    "build_combined_markdown.py",
    "build_printable_full.py",
]

PDF_TARGETS = [
    "openbook_core.md",
    "openbook_full.md",
    "openbook_printable_full.md",
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    review = ROOT / "05_review"
    for script in BUILD_STEPS:
        run([sys.executable, str(review / script)])

    if shutil.which("pandoc") is None:
        raise RuntimeError("pandoc not found; PDF rebuild is required for final verification")

    out_dir = ROOT / "06_output"
    for name in PDF_TARGETS:
        md = out_dir / name
        if not md.exists():
            raise FileNotFoundError(md)
        pdf = md.with_suffix(".pdf")
        run([
            "pandoc",
            str(md),
            "-o",
            str(pdf),
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
        ])


if __name__ == "__main__":
    main()
