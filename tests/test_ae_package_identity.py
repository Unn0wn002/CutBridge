"""Run AE producer/consumer package identity regressions in the complete pytest suite."""
from pathlib import Path
import shutil
import subprocess


def test_ae_package_name_binds_logical_identity():
    node = shutil.which("node")
    assert node, "Node is required for After Effects package identity regression tests"
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [node, str(root / "tests" / "ae_package_identity_checks.cjs")],
        cwd=root,
        check=True,
    )
