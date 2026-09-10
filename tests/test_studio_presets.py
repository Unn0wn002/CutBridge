import copy
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "apps" / "blender" / "cutbridge" / "presets.py"
SCHEMA_PATH = ROOT / "packages" / "shared" / "cutbridge-studio-preset.schema.json"
EXAMPLE_PATH = ROOT / "docs" / "examples" / "studio-preset.default.json"

spec = importlib.util.spec_from_file_location("cutbridge_presets_s9", MODULE_PATH)
presets = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(presets)


def _manual_settings(**overrides):
    values = {
        "pass_beauty": True,
        "pass_line": False,
        "pass_shadow": False,
        "pass_depth": False,
        "image_format": "PNG",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_builtin_default_matches_published_example_and_schema():
    built_in = presets.default_preset()
    example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert built_in == example
    assert presets.validate_preset(built_in) == built_in
    jsonschema.Draft202012Validator(schema).validate(example)


def test_manual_mode_preserves_legacy_pass_and_format_controls():
    manual = presets.manual_preset(
        _manual_settings(pass_line=True, pass_depth=True, image_format="OPEN_EXR")
    )
    assert [item["name"] for item in manual["passes"]] == ["BEAUTY", "LINE", "DEPTH"]
    assert all(item["required"] is True for item in manual["passes"])
    assert manual["output"]["image_format"] == "OPEN_EXR"
    assert manual["naming"]["package"] == "{project}_{episode}_{scene}_{cut}_{take}_{version}"
    assert presets.version_token_for(manual, 7) == "V007"


def test_valid_custom_preset_can_change_order_format_folders_and_versioning():
    custom = presets.default_preset()
    custom["id"] = "jp-studio-a"
    custom["name"] = "JP Studio A"
    custom["folders"] = {
        "render": "frames/final",
        "preview": "review",
        "camera": "handoff/camera",
    }
    custom["passes"] = [
        {"name": "LINE", "required": False},
        {"name": "BEAUTY", "required": True},
    ]
    custom["output"]["image_format"] = "TIFF"
    custom["versioning"] = {"prefix": "R", "padding": 4}
    custom["naming"]["package"] = "{project}-{cut}-{version}"
    custom["naming"]["sequence"] = "{project}_{cut}_{pass}_####"
    custom["naming"]["ae_comp"] = "{project}_{cut}_COMP"

    normalized = presets.validate_preset(custom)
    assert [item["name"] for item in normalized["passes"]] == ["LINE", "BEAUTY"]
    assert normalized["passes"][0]["required"] is False
    assert normalized["folders"]["render"] == "frames/final"
    assert normalized["output"]["image_format"] == "TIFF"
    assert presets.version_token_for(normalized, 12) == "R0012"
    values = {
        "project": "SHOW",
        "episode": "EP01",
        "scene": "SC010",
        "cut": "C012",
        "take": "T01",
        "version": "R0012",
        "pass": "BEAUTY",
    }
    assert presets.format_template(normalized, "package", values) == "SHOW-C012-R0012"
    assert presets.format_template(normalized, "sequence", values) == "SHOW_C012_BEAUTY_####"
    assert presets.format_template(normalized, "ae_comp", values) == "SHOW_C012_COMP"


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (lambda p: p.update({"schema": "other"}), "PRESET_SCHEMA_INVALID"),
        (lambda p: p.update({"schema_version": 99}), "PRESET_SCHEMA_UNSUPPORTED"),
        (lambda p: p["folders"].update({"render": "../escape"}), "PRESET_PATH_UNSAFE"),
        (lambda p: p["folders"].update({"preview": "/absolute"}), "PRESET_PATH_UNSAFE"),
        (lambda p: p["naming"].update({"package": "{project}/{cut}"}), "PRESET_FIELD_INVALID"),
        (lambda p: p["naming"].update({"package": "{__class__}"}), "PRESET_FIELD_INVALID"),
        (lambda p: p["naming"].update({"sequence": "{cut}_{pass}"}), "PRESET_FIELD_INVALID"),
        (lambda p: p["passes"].append({"name": "BEAUTY", "required": True}), "PRESET_FIELD_INVALID"),
        (lambda p: p["output"].update({"image_format": "MOVIE"}), "PRESET_FIELD_INVALID"),
        (lambda p: p.update({"command": "rm -rf /"}), "PRESET_FIELD_INVALID"),
    ],
)
def test_invalid_or_malicious_preset_data_fails_closed(mutation, code):
    candidate = copy.deepcopy(presets.default_preset())
    mutation(candidate)
    with pytest.raises(presets.PresetError) as caught:
        presets.validate_preset(candidate)
    assert caught.value.code == code


def test_loader_reads_bounded_utf8_json_only(tmp_path):
    valid_path = tmp_path / "studio.json"
    valid_path.write_text(json.dumps(presets.default_preset(), ensure_ascii=False), encoding="utf-8")
    assert presets.load_preset_file(valid_path)["id"] == "cutbridge-default"

    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("{not-json", encoding="utf-8")
    with pytest.raises(presets.PresetError) as caught:
        presets.load_preset_file(invalid_json)
    assert caught.value.code == "PRESET_JSON_INVALID"

    oversized = tmp_path / "large.json"
    oversized.write_bytes(b" " * (presets.MAX_PRESET_BYTES + 1))
    with pytest.raises(presets.PresetError) as caught:
        presets.load_preset_file(oversized)
    assert caught.value.code == "PRESET_FILE_TOO_LARGE"


def test_preset_metadata_does_not_expose_custom_file_path():
    metadata = presets.preset_metadata("CUSTOM", presets.default_preset())
    assert metadata == {
        "mode": "custom",
        "schema": "cutbridge-studio-preset",
        "schema_version": 1,
        "id": "cutbridge-default",
        "name": "CutBridge Default",
    }
    assert "path" not in metadata
