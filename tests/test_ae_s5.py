import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _run_node(script_name):
    node = shutil.which("node")
    if not node:
        pytest.fail("Node.js is required for S5 AE import/comp reliability tests")
    subprocess.run([node, str(ROOT / "tests" / script_name)], cwd=ROOT, check=True)


def test_ae_s5_import_comp_reliability_host_regressions():
    _run_node("ae_s5_checks.cjs")


def test_ae_s5_managed_layer_source_guard_regressions():
    _run_node("ae_s5_managed_layer_guard.cjs")


def test_ae_s5_partial_retry_layer_order_regression():
    _run_node("ae_s5_partial_retry_order.cjs")


def test_ae_qc_requires_current_managed_layer_ownership():
    _run_node("ae_qc_managed_layer_checks.cjs")
