from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "05_review"

CHECKS = [
    "build_all_outputs.py",
    "scan_python_syntax.py",
    "scan_cpp_pseudocode.py",
    "scan_template_consistency.py",
    "scan_index_policy.py",
    "scan_forbidden_patterns.py",
    "check_module_fields.py",
    "extract_compile_cpp_blocks.py",
    "audit_cpp_blocks_wsl.py",
    "second_round_standalone_compile_all.py",
    "run_standalone_tests.py",
    "second_round_module_matrix.py",
]


def run(script: str) -> None:
    cmd = [sys.executable, str(REVIEW / script)]
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    for script in CHECKS:
        run(script)
    print("ALL REVIEW GATES PASSED")


if __name__ == "__main__":
    main()
