from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_readme_tracks_live_state_through_s13_and_next_s14():
    text = _read("README.md")
    assert "0a86d9a0605e1dd9714ef35a547693de76f714f4" in text
    assert "S12" in text and "PASS" in text
    assert "S13" in text and "9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95" in text
    assert "S14" in text
    assert "UNRELEASED / PUBLICATION BLOCKED" in text
    assert '"approved": false' in text
    assert "S12 — End-to-End Blender → package → After Effects validation harness" not in text


def test_completion_status_reconciles_s12_s13_without_release_claim():
    text = _read("docs/COMPLETION_STATUS.md")
    assert "Integrated product/validation sessions:** S1–S13" in text
    assert "S12" in text and "PASS" in text
    assert "S13" in text and "PASS" in text
    assert "0a86d9a0605e1dd9714ef35a547693de76f714f4" in text
    assert "9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95" in text
    assert "NOT RELEASE READY" in text
    assert "S14" in text


def test_release_readiness_records_completed_native_path_but_fails_closed():
    text = _read("docs/RELEASE_READINESS.md")
    assert "UNRELEASED / PUBLICATION BLOCKED" in text
    assert "S12 release-target campaign executed and reconciled to PASS" in text
    assert "S13 real-host Camera/Null revision defects repaired and integrated" in text
    assert "STRUCTURED-EVIDENCE TRACEABILITY GAP REMAINS" in text
    assert "issue #18" in text
    assert "Do not perform a blind merge" in text
    assert "NOT RELEASE READY" in text
    assert "release-authorization.json" in text


def test_s12_runbook_is_now_a_completed_campaign_record():
    text = _read("docs/S12_E2E_VALIDATION.md")
    assert "PASS AFTER S13F REPAIR CHAIN / CLOSED" in text
    assert "9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95" in text
    assert "34504009878" in text
    assert "structured `s12-evidence.json` PASS record is **not present" in text
    assert "do **not** manufacture a retroactive PASS record" in text
    assert "S12 PASS is not release authorization" in text


def test_evidence_summary_preserves_sha_bound_native_evidence_and_limitations():
    text = _read("docs/S12_S13_EVIDENCE_SUMMARY.md")
    assert "S12 PASS / S13 PASS / v0.2.3 STILL UNRELEASED" in text
    assert "9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95" in text
    assert "0a86d9a0605e1dd9714ef35a547693de76f714f4" in text
    assert "34503571091" in text
    assert "34503805612" in text
    assert "34504009878" in text
    assert "evidence-traceability gap" in text
    assert "NOT RELEASE READY" in text


def test_3d_handoff_guide_still_records_native_s10c_boundary():
    text = _read("docs/HANDOFF_3D.md")
    assert "S10C" in text
    assert "CutBridge-managed perspective camera" in text
    assert "CutBridge-managed 3D Null layers" in text
    assert "0.00018066 px" in text
    assert "no After Effects reconstruction yet" not in text


def test_after_effects_install_guide_avoids_blanket_certification():
    text = _read("apps/after-effects/INSTALL.md")
    assert "S10C" in text
    assert "0.00018066 px" in text
    assert "0 duplicate managed layers" in text
    assert "does **not** certify every After Effects 2024–2026" in text


def test_compatibility_scopes_native_ae_evidence_to_tested_host():
    text = _read("docs/COMPATIBILITY.md")
    assert "After Effects 2026 Build 87 (`26.3x87`) on Windows 11" in text
    assert "0.00018066 px" in text
    assert "target range rather than a blanket certification claim" in text
    assert "Stable broad compatibility certification: **not yet claimed**" in text
