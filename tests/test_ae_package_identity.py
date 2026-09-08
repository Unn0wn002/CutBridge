"""Run AE producer/consumer package identity regressions in the complete pytest suite."""
from pathlib import Path
import shutil
import subprocess


def _run_node(root, filename):
    node = shutil.which("node")
    assert node, "Node is required for After Effects package identity regression tests"
    subprocess.run([node, str(root / "tests" / filename)], cwd=root, check=True)


def test_ae_package_name_binds_logical_identity():
    root = Path(__file__).resolve().parents[1]
    _run_node(root, "ae_package_identity_checks.cjs")


def test_vm_contract_diagnostic():
    root = Path(__file__).resolve().parents[1]
    _run_node(root, "ae_vm_contract_diagnostic.cjs")
