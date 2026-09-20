from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "apps" / "after-effects" / "INSTALL.md"


def test_after_effects_install_note_requires_all_runtime_scripts():
    text = INSTALL.read_text(encoding="utf-8")
    assert "CutBridge.jsx" in text
    assert "revision_manager.js" in text
    assert "qc_plus.js" in text
    assert "localization.js" in text
    assert "Keep these files together" in text
    assert "all four" in text
    assert "Scripts/ScriptUI Panels" in text
    assert "Japanese" in text
    assert "English" in text
    assert "CBQ-*" in text
    assert "After Effects 2026 (26.3 Build 87)" in text
    assert "not native After Effects certification" in text
