from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_readme_tracks_released_v023_and_fail_closed_v024_baseline():
    text = _read("README.md")
    assert "S12" in text and "S13" in text
    assert "9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95" in text
    assert "S14A" in text and "S14B" in text
    assert "S14B remains NOT_EXECUTED" in text
    assert "Stable v0.2.3 remains published and immutable" in text
    assert "v0.2.4 — unreleased development baseline" in text
    assert "1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f" in text
    assert "https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json" in text
    assert "automatic startup update scheduling remains disabled" in text
    assert "no representative Japanese-user usability claim" in text
    assert "v0.2.4 UNRELEASED / PUBLICATION NOT AUTHORIZED" in text
    assert '"approved": false' in text
    assert "S12 — End-to-End Blender → package → After Effects validation harness" not in text


def test_completion_status_reconciles_released_v023_and_v024_development():
    text = _read("docs/COMPLETION_STATUS.md")
    assert "Integrated product/validation sessions:** S1–S13" in text
    assert "S12" in text and "PASS" in text
    assert "S13" in text and "PASS" in text
    assert "0a86d9a0605e1dd9714ef35a547693de76f714f4" in text
    assert "9c99ae23ccd8c47fdc0fffbd05b99e1326f2ea95" in text
    assert "v0.2.3 is released, published, independently verified" in text
    assert "v0.2.4 source baseline is **UNRELEASED / NOT AUTHORIZED FOR PUBLICATION**" in text
    assert "1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f" in text
    assert "635c1384af2649d4ce49705cce41f98826a861cc" in text
    assert "S14" in text
    assert "S14B remains NOT_EXECUTED" in text


def test_release_readiness_records_published_v023_and_fail_closed_v024():
    text = _read("docs/RELEASE_READINESS.md")
    assert "v0.2.3 PUBLISHED / VERIFIED" in text
    assert "v0.2.4 UNRELEASED / NOT AUTHORIZED" in text
    assert "S12 release-target campaign executed and reconciled to PASS" in text
    assert "S13 real-host Camera/Null revision defects repaired and integrated" in text
    assert "STRUCTURED-EVIDENCE TRACEABILITY DECISION RESOLVED" in text
    assert "Issue #18" in text and "OPEN" in text
    assert "PR #74 promoted exact `develop` head" in text
    assert "1fd2f67935600b06ef9d5301d9d8d6c2d723ca4f" in text
    assert "635c1384af2649d4ce49705cce41f98826a861cc" in text
    assert "https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json" in text
    assert "https://unn0wn002.github.io/cutbridge-distribution/blender/index.json" in text
    assert "Require release tag eligibility" in text
    assert "release-authorization.json" in text
    assert "claim-scope narrowing resolves the v0.2.3 S14 release-claim gate" in text
    assert "S14B representative Japanese-speaking target-user execution remains **NOT_EXECUTED**" in text


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
    assert "Structured evidence-record resolution" in text
    assert "historically unavailable / not reconstructable without fabrication" in text
    assert "no retroactive PASS JSON will be created" in text
    assert "NOT RELEASE READY" in text


def test_quick_starts_track_s13_and_point_to_s14():
    en = _read("docs/QUICK_START.md")
    ja = _read("docs/QUICK_START_JA.md")

    assert "development workflow through S13" in en
    assert "S13F" in en
    assert "S14 — Japanese Target-User Validation & Release Preparation" in en
    assert "S12 — End-to-End Blender → package → After Effects validation harness" not in en
    assert "S12_S13_EVIDENCE_SUMMARY.md" in en

    assert "S13 までの v0.2.3 未リリース開発版" in ja
    assert "S13F" in ja
    assert "S14 — Japanese Target-User Validation & Release Preparation" in ja
    assert "S12 — Blender → package → After Effects End-to-End Validation Harness" not in ja
    assert "S12_S13_EVIDENCE_SUMMARY.md" in ja


def test_technical_debt_uses_current_release_baseline_and_evidence_limits():
    text = _read("docs/TECHNICAL_DEBT.md")
    assert "S1–S13 validated product baseline" in text
    assert "stable v0.2.3: released and immutable" in text
    assert "active development: `0.2.4`" in text
    assert "release authorization: `approved: false`" in text
    assert "publication governance issue #18: OPEN" in text
    assert "307 tests + 2 subtests" in text
    assert "72 deprecation warnings" in text
    assert "S12 structured evidence traceability" in text
    assert "Repository-level configuration is now present on the public repository" in text
    assert "release-facing Japanese claim was deliberately narrowed" in text
    assert "The v0.2.3 governance path is complete" in text
    assert "green S8-integrated product baseline" not in text
    assert "develop` contains S1–S8" not in text


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


def test_after_effects_install_guide_is_release_state_neutral():
    text = _read("apps/after-effects/INSTALL.md")
    lowered = text.lower()

    assert "development packages" not in lowered
    assert "first development test" not in lowered
    assert "normal development use" not in lowered
    assert "does **not** authorize publication of" not in text
    assert "remains published and immutable" not in text
    assert "release-metadata.json" in text
    assert "SHA256SUMS.txt" in text
    assert "GitHub Release page" in text
    assert "intentionally does not encode whether a particular tag is current, authorized, or published" in text


def test_compatibility_scopes_native_ae_evidence_to_tested_host():
    text = _read("docs/COMPATIBILITY.md")
    assert "After Effects 2026 Build 87 (`26.3x87`) on Windows 11" in text
    assert "0.00018066 px" in text
    assert "target range rather than a blanket certification claim" in text
    assert "Stable broad compatibility certification: **not yet claimed**" in text


def test_s14_protocol_preserves_not_executed_state_after_claim_narrowing():
    text = _read("docs/S14_JP_USER_VALIDATION.md")
    assert "S14A COMPLETE / S14B NOT EXECUTED / v0.2.3 RELEASE CLAIM SCOPE NARROWED" in text
    assert "S14B remains `NOT_EXECUTED`" in text
    assert "no S14 PASS" in text
    assert "validated by representative Japanese production users" in text
    assert "resolves the **v0.2.3 S14 release-claim gate**" in text
    assert "S14B is not a prerequisite for the narrowed release-facing claim" in text


def test_update_architecture_separates_public_source_from_distribution():
    text = _read("docs/UPDATE_ARCHITECTURE.md")
    assert "currently public and protected by branch/tag rulesets" in text
    assert "Repository visibility does not make the GitHub source repository the client update server" in text
    assert "https://unn0wn002.github.io/cutbridge-distribution/cutbridge/release-index.json" in text
    assert "https://unn0wn002.github.io/cutbridge-distribution/blender/index.json" in text
    assert "Automatic startup update scheduling remains disabled" in text
    assert "Do not use source-repository visibility as an update-distribution mechanism" in text
    assert "private source repository" not in text


def test_roadmap_tracks_completed_promotion_and_deferred_s14b():
    text = _read("docs/ROADMAP.md")
    assert "S14A COMPLETE / S14B NOT_EXECUTED for v0.2.3" in text
    assert "COMPLETE / VERIFIED" in text
    assert "35513361337" in text
    assert "Stable v0.2.3 publication and production D1 distribution are complete" in text
    assert "v0.2.4 is the active unreleased development baseline" in text
    assert "subsequent releases and distribution automation" in text


def test_v024_current_facing_docs_track_frozen_candidate_and_promotion_gate():
    readiness = _read("docs/RELEASE_READINESS.md")
    completion = _read("docs/COMPLETION_STATUS.md")
    checklist = _read("docs/RELEASE_CHECKLIST.md")

    for text in (readiness, completion, checklist):
        assert "ef5911a83270a4ce8121741ada2d2726fa09ec29" in text

    for text in (readiness, completion):
        assert "f2abcd814fde2bc8a2a45ba0c897fec1544f8e55" not in text
        assert "f39b9f41c66c8abc0f895066675d80b0747c6053" not in text

    assert "candidate/v0.2.4-beta.1" in readiness
    assert "3819b6178cac31b6613d475aeaf84faeaee99b97add94eca6375f1c408f487c2" in readiness
    assert "e249d6f83c95b7eded472c8bd473c5034e8ab500fa28945b460f150518a6f73b" in readiness
    assert "35797413040" in readiness
    assert "focused Issue #82 exact-candidate rerun" in readiness
    assert "process code `0`" in readiness
    assert "Issue #80: COMPLETED for v0.2.4" in completion
    assert "Issue #80: OPEN" not in completion
    assert "307 passed, 72 warnings + 2 subtests" in completion
    assert "focused Issue #82 rerun PASS" in completion
    assert "protected `develop` → `main`" in checklist


def test_current_release_docs_do_not_restore_stale_prepublication_claims():
    documents = {
        path: _read(path)
        for path in (
            "docs/RELEASE_READINESS.md",
            "docs/ROADMAP.md",
            "docs/TECHNICAL_DEBT.md",
            "docs/RELEASE_CHECKLIST.md",
        )
    }
    combined = "\n".join(documents.values())

    assert "private source repository" not in combined
    assert "Version `0.2.3` remains unreleased" not in combined
    assert "product version: `0.2.3` unreleased" not in combined
    assert "no release tag or GitHub Release exists" not in combined
    assert "there are still no GitHub Releases or release tags" not in combined
    assert "release tag refs: none" not in combined
    assert "GitHub Releases: none" not in combined
    assert "production D1 distribution: pending" not in combined
    assert "deploy/verify the production update/distribution endpoint" not in combined
