from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "tools" / "research" / "s10_ae_probe.jsx"


def _source() -> str:
    return PROBE.read_text(encoding="utf-8")


def test_probe_is_explicitly_research_only_and_uses_unique_disposable_comp():
    source = _source()
    assert "Research-only" in source
    assert "__CUTBRIDGE_S10_SPATIAL_PROBE__" in source
    assert "app.project.items.addComp(PROBE_COMP" in source
    assert "comp.remove()" in source
    assert "app.newProject" not in source


def test_probe_requires_explicit_user_file_save_and_never_hides_report_write():
    source = _source()
    assert "File.saveDialog" in source
    assert 'output.open("w")' in source
    assert "output.write(text)" in source
    assert "output.fsName" in source


def test_probe_uses_fixed_candidate_basis_zoom_and_strict_projection_tolerance():
    source = _source()
    assert "candidate_basis: [[1,0,0],[0,0,-1],[0,1,0]]" in source
    assert "2666.6666666666665" in source
    tolerance = re.search(r"var TOLERANCE_PX = ([0-9.]+);", source)
    assert tolerance is not None
    assert float(tolerance.group(1)) <= 0.05
    assert "error <= TOLERANCE_PX" in source
    assert "maxError <= TOLERANCE_PX" in source


def test_probe_uses_native_camera_and_null_projection_primitives_without_artist_adoption():
    source = _source()
    assert ".layers.addCamera(" in source
    assert ".layers.addNull(" in source
    assert ".toComp(" in source
    assert 'property("ADBE Camera Zoom")' in source
    assert 'property("ADBE Position")' in source
    assert "findManaged" not in source
    assert "managedTag" not in source


def test_probe_cleanup_failure_forces_fail_result():
    source = _source()
    cleanup_block = source[source.index("if (comp) {"):source.index("app.endUndoGroup();")]
    assert "report.cleanup = true" in cleanup_block
    assert "report.cleanup = false" in cleanup_block
    assert "report.pass = false" in cleanup_block
