"""Run S7 QC+ diagnostic regressions in the complete pytest suite."""
from pathlib import Path
import shutil
import subprocess


def test_s7_qc_plus_diagnostic_engine():
    node = shutil.which("node")
    assert node, "Node is required for S7 After Effects QC+ regression tests"
    root = Path(__file__).resolve().parents[1]
    subprocess.run([node, str(root / "tests" / "ae_s7_qc_plus_checks.cjs")], cwd=root, check=True)


def test_s7_native_qc_plus_binding():
    node = shutil.which("node")
    assert node, "Node is required for S7 native QC+ binding regressions"
    root = Path(__file__).resolve().parents[1]
    subprocess.run([node, str(root / "tests" / "ae_s7_native_qc_binding_checks.cjs")], cwd=root, check=True)


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

    panel = (root / "apps/after-effects/CutBridge.jsx").read_text(encoding="utf-8")
    assert "function getQCPlus()" in panel
    assert '"/qc_plus.js"' in panel
    assert "CutBridgeQCPlus" in panel
    assert "qc.sequenceRecords" in panel
    assert "qc.managedObjectRecords" in panel
    assert "qc.compRecords" in panel
    assert "qc.hostRecords" in panel
    assert "qc.render(records)" in panel

    # S7 diagnostic core must stay data-only. Host mutation belongs to existing
    # guarded S5/S6 flows, not QC reporting.
    forbidden = ["replaceSource(", ".remove()", "app.project.importFile", "items.addFolder", "layers.add("]
    for token in forbidden:
        assert token not in source


def test_s7_native_after_effects_parser_regressions():
    root = Path(__file__).resolve().parents[1]
    qc_source = (root / "apps/after-effects/qc_plus.js").read_text(encoding="utf-8")
    revision_source = (root / "apps/after-effects/revision_manager.js").read_text(encoding="utf-8")

    # AE 26.3 ExtendScript rejects an unquoted reserved `package` key.
    assert '        "package": 0,' in qc_source
    assert "\n        package: 0," not in qc_source

    # AE 26.3 evaluated the previous nested ternary as warning for errors=1/warnings=0.
    # Keep the compatibility decision explicit and parser-safe.
    assert 'if (errors.length > 0) {' in revision_source
    assert 'status = "incompatible";' in revision_source
    assert 'else if (warnings.length > 0) {' in revision_source
    assert 'errors.length ? "incompatible" : warnings.length ? "warning" : "safe"' not in revision_source
