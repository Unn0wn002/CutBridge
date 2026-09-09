import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLENDER = ROOT / "apps" / "blender" / "cutbridge"


def _load_localization():
    path = BLENDER / "localization.py"
    spec = importlib.util.spec_from_file_location("cutbridge_s8_localization_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_japanese_is_first_class_default_and_english_is_fallback():
    loc = _load_localization()
    assert loc.DEFAULT_LANGUAGE == "JA"
    assert loc.FALLBACK_LANGUAGE == "EN"
    assert loc.normalize_language("JA") == "JA"
    assert loc.normalize_language("ja") == "JA"
    assert loc.normalize_language("EN") == "EN"
    assert loc.normalize_language("unknown") == "EN"


def test_primary_ui_strings_have_japanese_and_english_variants():
    loc = _load_localization()
    keys = (
        "project_setup",
        "scene_metadata",
        "pass_package",
        "export",
        "validation_status",
        "environment",
        "updates",
        "validate_cut",
        "build_package",
        "open_package_folder",
    )
    for key in keys:
        ja = loc.tr("JA", key)
        en = loc.tr("EN", key)
        assert ja and en
        assert ja != key
        assert en != key
        assert ja != en


def test_missing_translation_falls_back_without_breaking_ui():
    loc = _load_localization()
    assert loc.tr("JA", "missing.s8.key") == "missing.s8.key"
    assert loc.tr("invalid", "build_package") == "Build Package"


def test_issue_localization_preserves_machine_code_and_canonical_support_text():
    loc = _load_localization()
    item = {
        "level": "ERROR",
        "code": "CAMERA_MISSING",
        "message": "No active scene camera.",
        "fix": "Assign an active camera in Scene Properties.",
    }
    ja_message, ja_fix = loc.localized_issue("JA", item)
    en_message, en_fix = loc.localized_issue("EN", item)
    assert "CAMERA_MISSING" not in ja_message
    assert "CAMERA_MISSING" not in ja_fix
    assert ja_message != en_message
    assert ja_fix != en_fix
    assert en_message == item["message"]
    assert en_fix == item["fix"]
    assert item["code"] == "CAMERA_MISSING"

    formatted = loc.format_localized_issue("JA", item)
    assert formatted.startswith("アクティブカメラが設定されていません。")
    assert "[EN] No active scene camera." in formatted
    assert "Fix: Assign an active camera in Scene Properties." in formatted
    assert "CAMERA_MISSING" not in formatted


def test_untranslated_japanese_issue_falls_back_without_duplicate_english_block():
    loc = _load_localization()
    item = {
        "code": "UNKNOWN_FUTURE_CODE",
        "message": "Canonical future diagnostic.",
        "fix": "Keep the workflow safe.",
    }
    formatted = loc.format_localized_issue("JA", item)
    assert formatted == "Canonical future diagnostic. 対処: Keep the workflow safe."
    assert "[EN]" not in formatted


def test_blender_panel_uses_locale_contract_instead_of_bilingual_slash_labels():
    source = (BLENDER / "ui.py").read_text(encoding="utf-8")
    assert "from .localization import localized_issue, tr" in source
    assert "s.language" in source
    assert 'tr(language, "validate_cut")' in source
    assert 'tr(language, "build_package")' in source
    assert 'tr(language, "validation_status")' in source
    assert "Import Package /" not in source
    assert "Validate Cut /" not in source


def test_operator_reports_follow_selected_locale_and_console_stays_canonical():
    source = (BLENDER / "operators.py").read_text(encoding="utf-8")
    assert "format_localized_issue" in source
    assert 'tr(language, "validation_passed")' in source
    assert 'tr(language, "package_created"' in source
    assert "=== CutBridge Validation ===" in source
    assert "format_issue(item)" in source


def test_blender_language_property_defaults_to_japanese():
    source = (BLENDER / "properties.py").read_text(encoding="utf-8")
    assert 'items=(("JA", "日本語", "Japanese"), ("EN", "English", "English"))' in source
    assert 'default="JA"' in source


def test_blender_panel_uses_narrow_safe_full_width_identity_controls():
    source = (BLENDER / "ui.py").read_text(encoding="utf-8")
    assert "def labeled_prop" in source
    for property_name in ("language", "project", "episode", "scene_id", "cut", "take", "version", "image_format", "output_dir"):
        assert f'"{property_name}"' in source
    assert 'row.prop(s, "episode"' not in source
    assert 'row.prop(s, "scene_id"' not in source
    assert 'row.prop(s, "cut"' not in source
    assert 'row.prop(s, "take"' not in source
    assert 'row.prop(s, "version"' not in source
    assert 'row.operator("cutbridge.validate"' not in source
    assert 'row.operator("cutbridge.build_package"' not in source
