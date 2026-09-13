from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def test_beta2_quick_start_pair_and_cross_links_exist():
    en = (DOCS / "QUICK_START_BETA2.md").read_text(encoding="utf-8")
    ja = (DOCS / "QUICK_START_BETA2_JA.md").read_text(encoding="utf-8")
    assert "QUICK_START_BETA2_JA.md" in en
    assert "QUICK_START_BETA2.md" in ja
    for text in (en, ja):
        assert "FOUR_PASS_WORKFLOW_BETA2.md" in text
        assert "COMPATIBILITY_CAMPAIGN_BETA2.md" in text
        assert "NOT RELEASE READY" in text


def test_usability_docs_explain_line_depth_version_and_overwrite_safety():
    en = (DOCS / "QUICK_START_BETA2.md").read_text(encoding="utf-8")
    for phrase in (
        "As Render Pass",
        "OpenEXR",
        "V001",
        "V002",
        "V003",
        "same-version package",
        "Validate Cut",
        "Build Package",
        "QC+",
    ):
        assert phrase in en


def test_four_pass_doc_records_renderer_boundary_without_blanket_claim():
    text = (DOCS / "FOUR_PASS_WORKFLOW_BETA2.md").read_text(encoding="utf-8")
    assert "Beauty + Line + Shadow + Depth" in text
    assert "EEVEE" in text
    assert "Cycles" in text
    assert "SHADOW_OUTPUT_UNAVAILABLE" in text
    assert "does **not** upgrade Blender 4.2 or 4.5 to tested status" in text


def test_compatibility_campaign_does_not_claim_legacy_ae_support_without_evidence():
    text = (DOCS / "COMPATIBILITY_CAMPAIGN_BETA2.md").read_text(encoding="utf-8")
    for version in ("2020", "2021", "2022", "2023"):
        assert f"| {version} | UNVERIFIED |" in text
    assert "Do not upgrade AE 2020–2025 to **TESTED / SUPPORTED**" in text
    assert "Material source changes after that freeze invalidate the candidate evidence" in text
