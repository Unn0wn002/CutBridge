"""Run S7 QC+ diagnostic regressions in the complete pytest suite."""
from pathlib import Path
import shutil
import subprocess


def test_s7_qc_plus_diagnostic_engine():
    node = shutil.which("node")
    assert node, "Node is required for S7 After Effects QC+ regression tests"
    root = Path(__file__).resolve().parents[1]
    subprocess.run([node, str(root / "tests" / "ae_s7_qc_plus_checks.cjs")], cwd=root, check=True)


def test_s7_qc_plus_engine_is_host_independent_and_non_mutating():
    root = Path(__file__).resolve().parents[1]
    source = (root / "apps/after-effects/qc_plus.js").read_text(encoding="utf-8")

    assert "CutBridgeQCPlus" in source
    assert "function diagnostic(spec)" in source
    assert "function normalize(records)" in source
    assert "function sequenceRecords(passInfo, manifest, coverage)" in source
    assert "function compRecords(mismatches)" in source
    assert "function managedObjectRecords(kind, passInfo, observation)" in source
    assert "function hostRecords(observation)" in source
    assert "function revisionRecords(assessment, subject)" in source

    # S7 diagnostic core must stay data-only. Host mutation belongs to existing
    # guarded S5/S6 flows, not QC reporting.
    forbidden = ["replaceSource(", ".remove()", "app.project.importFile", "items.addFolder", "layers.add("]
    for token in forbidden:
        assert token not in source
