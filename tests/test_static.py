import ast
import hashlib
import importlib.util
import json
import pathlib
import py_compile
import re
import subprocess
import sys
import tomllib
import zipfile

import pytest
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER = ROOT / "apps" / "blender" / "cutbridge"


def _load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _version_from_source() -> str:
    tree = ast.parse((BLENDER / "version.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__version__":
                    assert isinstance(node.value, ast.Constant)
                    return str(node.value.value)
    raise AssertionError("__version__ not found")


def test_python_sources_compile():
    for path in (ROOT / "apps" / "blender").rglob("*.py"):
        py_compile.compile(str(path), doraise=True)
    py_compile.compile(str(ROOT / "tools" / "build_release.py"), doraise=True)


def test_blender_manifest_is_hardened_and_version_synced():
    with (BLENDER / "blender_manifest.toml").open("rb") as fh:
        manifest = tomllib.load(fh)

    assert manifest["schema_version"] == "1.0.0"
    assert manifest["id"] == "cutbridge"
    assert manifest["type"] == "add-on"
    assert manifest["version"] == _version_from_source() == "0.2.3"
    assert manifest["blender_version_min"] == "4.2.0"
    assert "Animation" in manifest["tags"]
    assert "files" in manifest["permissions"]
    assert "network" in manifest["permissions"]
    assert manifest["build"]["paths_exclude_pattern"]
    version_module = _load_module("cutbridge_version_test", BLENDER / "version.py")
    assert version_module.VERSION == tuple(int(x) for x in manifest["version"].split("."))
    assert "SPDX:GPL-3.0-or-later" in manifest["license"]
    assert "GNU GENERAL PUBLIC LICENSE" in (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert f'**v{manifest["version"]} ' in (ROOT / "README.md").read_text(encoding="utf-8")
    assert f'## [{manifest["version"]}]' in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_addon_preferences_do_not_store_transport_strings_in_rna():
    """Updater URLs/status strings are runtime data, not Blender RNA preferences."""
    source = (BLENDER / "preferences.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    string_property_calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (isinstance(func, ast.Name) and func.id == "StringProperty") or (
            isinstance(func, ast.Attribute) and func.attr == "StringProperty"
        ):
            string_property_calls.append(node)

    assert not string_property_calls
    assert "update_index_url" not in source
    assert "RUNTIME_UPDATE_STATE" in source


def test_registration_has_partial_failure_rollback():
    source = (BLENDER / "__init__.py").read_text(encoding="utf-8")
    assert "_cleanup_partial_registration" in source
    assert "_registered_class_for" in source
    assert "for cls in reversed(registered)" in source
    assert "raise" in source


def test_blender_52_lts_is_in_target_matrix():
    source = (BLENDER / "version.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    value = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "TARGET_LTS_SERIES"
            for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            break
    assert value is not None
    assert (5, 2) in value


def test_shared_and_update_schemas_parse():
    shared = json.loads(
        (ROOT / "packages" / "shared" / "cutbridge-manifest.schema.json").read_text(encoding="utf-8")
    )
    update_schema = json.loads(
        (ROOT / "packages" / "update" / "release-index.schema.json").read_text(encoding="utf-8")
    )
    example = json.loads(
        (ROOT / "packages" / "update" / "release-index.example.json").read_text(encoding="utf-8")
    )
    assert shared["title"] == "CutBridge Manifest"
    assert update_schema["title"] == "CutBridge Release Index"
    assert example["schema_version"] == 1
    Draft202012Validator.check_schema(shared)
    Draft202012Validator.check_schema(update_schema)
    Draft202012Validator(update_schema).validate(example)


def test_update_selection_respects_channel_version_platform_and_blender():
    updates = _load_module("cutbridge_updates_test", BLENDER / "updates.py")
    payload = {
        "schema_version": 1,
        "releases": [
            {
                "version": "0.2.2",
                "channel": "stable",
                "blender_version_min": "4.2.0",
                "platforms": ["windows-x64", "linux-x64"],
                "release_page_url": "https://example.invalid/0.2.2",
            },
            {
                "version": "0.3.0-beta.1",
                "channel": "beta",
                "blender_version_min": "4.2.0",
                "platforms": ["windows-x64"],
                "release_page_url": "https://example.invalid/0.3.0-beta.1",
            },
            {
                "version": "1.0.0",
                "channel": "stable",
                "blender_version_min": "6.0.0",
                "platforms": ["windows-x64"],
                "release_page_url": "https://example.invalid/1.0.0",
            },
        ],
    }

    stable = updates.select_latest_compatible(
        payload,
        current_version="0.2.1",
        blender_version=(5, 2, 1),
        platform_name="windows-x64",
        selected_channel="stable",
    )
    assert stable["version"] == "0.2.2"

    beta = updates.select_latest_compatible(
        payload,
        current_version="0.2.1",
        blender_version=(5, 2, 1),
        platform_name="windows-x64",
        selected_channel="beta",
    )
    assert beta["version"] == "0.3.0-beta.1"

    too_old = updates.select_latest_compatible(
        payload,
        current_version="0.2.1",
        blender_version=(4, 1, 9),
        platform_name="windows-x64",
        selected_channel="stable",
    )
    assert too_old is None

    wrong_platform = updates.select_latest_compatible(
        payload,
        current_version="0.2.1",
        blender_version=(5, 2, 1),
        platform_name="macos-arm64",
        selected_channel="stable",
    )
    assert wrong_platform is None

    with pytest.raises(updates.UpdateIndexError):
        updates.validate_update_index({"schema_version": 99, "releases": []})


def test_release_builder_produces_expected_artifacts(tmp_path):
    output = tmp_path / "dist"
    version = _version_from_source()
    tag = f"v{version}"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "build_release.py"),
            "--tag",
            tag,
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    blender_zip = output / f"CutBridge-Blender-{tag}.zip"
    ae_zip = output / f"CutBridge-AfterEffects-{tag}.zip"
    checksum_file = output / "SHA256SUMS.txt"
    metadata_file = output / "release-metadata.json"

    assert blender_zip.is_file()
    assert ae_zip.is_file()
    assert checksum_file.is_file()
    assert metadata_file.is_file()

    with zipfile.ZipFile(blender_zip) as archive:
        names = set(archive.namelist())
        expected_python_modules = {
            path.relative_to(BLENDER).as_posix()
            for path in BLENDER.rglob("*.py")
        }
        assert "blender_manifest.toml" in names
        assert expected_python_modules <= names
        assert all(not name.startswith("cutbridge/") for name in names)

        archived_manifest = tomllib.loads(
            archive.read("blender_manifest.toml").decode("utf-8")
        )
        archived_version_source = archive.read("version.py").decode("utf-8")
        assert archived_manifest["version"] == version
        assert f'__version__ = "{version}"' in archived_version_source
        assert archive.read("LICENSE") == (ROOT / "LICENSE").read_bytes()

    with zipfile.ZipFile(ae_zip) as archive:
        assert archive.namelist() == ["CutBridge.jsx", "LICENSE"]
        assert archive.read("CutBridge.jsx") == (ROOT / "apps/after-effects/CutBridge.jsx").read_bytes()
        assert archive.read("LICENSE") == (ROOT / "LICENSE").read_bytes()

    checksum_lines = checksum_file.read_text(encoding="utf-8").splitlines()
    assert len(checksum_lines) == 2
    assert all(re.match(r"^[a-f0-9]{64}  CutBridge-", line) for line in checksum_lines)
    recorded_checksums = dict(line.split("  ", 1)[::-1] for line in checksum_lines)
    for artifact in (blender_zip, ae_zip):
        actual_checksum = hashlib.sha256(artifact.read_bytes()).hexdigest()
        assert recorded_checksums[artifact.name] == actual_checksum

    metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
    assert metadata["version"] == version
    assert metadata["tag"] == tag
    assert metadata["blender_version_min"] == "4.2.0"
    assert metadata["artifacts"]["blender"]["sha256"] == recorded_checksums[blender_zip.name]
    assert metadata["artifacts"]["after_effects"]["sha256"] == recorded_checksums[ae_zip.name]
