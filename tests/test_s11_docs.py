from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_quick_start_is_reconciled_through_s10c_and_points_to_s12():
    text = _read("docs/QUICK_START.md")
    assert "through S10C" in text
    assert "handoff_3d" in text
    assert "0.00018066 px" in text
    assert "S12 — End-to-End" in text
    assert "After S9 Studio Presets is integrated, the next engineering phase is **S10" not in text


def test_japanese_quick_start_is_reconciled_through_s10c_and_points_to_s12():
    text = _read("docs/QUICK_START_JA.md")
    assert "S10C" in text
    assert "handoff_3d" in text
    assert "0.00018066 px" in text
    assert "S12" in text
    assert "S9 Studio Presets 統合後の次フェーズは **S10" not in text


def test_3d_handoff_guide_no_longer_claims_ae_reconstruction_is_future_work():
    text = _read("docs/HANDOFF_3D.md")
    assert "S10C" in text
    assert "managed AE camera and 3D Null" in text
    assert "0.00018066 px" in text
    assert "no After Effects reconstruction yet" not in text
    assert "A later S10C phase must validate" not in text


def test_after_effects_install_guide_records_s10c_without_broad_certification_claim():
    text = _read("apps/after-effects/INSTALL.md")
    assert "S10C" in text
    assert "0.00018066 px" in text
    assert "0 duplicate managed layers" in text
    assert "does **not** certify every After Effects 2024–2026" in text


def test_compatibility_scopes_native_ae_evidence_to_the_tested_host():
    text = _read("docs/COMPATIBILITY.md")
    assert "After Effects 2026 Build 87 (`26.3x87`) on Windows 11" in text
    assert "0.00018066 px" in text
    assert "target range rather than a blanket certification claim" in text
    assert "Stable broad compatibility certification: **not yet claimed**" in text


def test_release_readiness_is_fail_closed_and_keeps_governance_external():
    text = _read("docs/RELEASE_READINESS.md")
    assert "UNRELEASED / PUBLICATION BLOCKED" in text
    assert "release-authorization.json" in text
    assert "approved: false" in text
    assert "issue #18" in text
    assert "Do **not** perform a blind merge" in text
    assert "S12 release-target end-to-end evidence — REQUIRED" in text
    assert "NOT RELEASE READY" in text
    assert "GitHub Release publication alone is not a functioning production update channel" in text
