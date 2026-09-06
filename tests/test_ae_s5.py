import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_ae_s5_import_comp_reliability_host_regressions():
    node = shutil.which("node")
    if not node:
        pytest.fail("Node.js is required for S5 AE import/comp reliability tests")
    subprocess.run([node, str(ROOT / "tests" / "ae_s5_checks.cjs")], cwd=ROOT, check=True)
