from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "apps" / "after-effects" / "INSTALL.md"


def test_after_effects_install_note_requires_all_s7_scripts():
    text = INSTALL.read_text(encoding="utf-8")
    assert "CutBridge.jsx" in text
    assert "revision_manager.js" in text
    assert "qc_plus.js" in text
    assert "Keep these files together" in text
    assert "Scripts/ScriptUI Panels" in text
    assert "V001 → V002 → V003" in text
    assert "S7 QC+" in text
    assert "not native After Effects certification" in text
