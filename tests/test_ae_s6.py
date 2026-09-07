"""Run S6 contract regressions in the complete pytest suite as well as CI."""
from pathlib import Path
import shutil
import subprocess


def test_revision_contract():
    node = shutil.which("node")
    assert node, "Node is required for S6 revision contract tests"
    root = Path(__file__).resolve().parents[1]
    subprocess.run([node, str(root / "tests/ae_s6_revision_checks.cjs")], cwd=root, check=True)
