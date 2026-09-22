import json
import pathlib
import shutil
import subprocess
import tomllib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
AE = ROOT / "apps" / "after-effects" / "CutBridge.jsx"


def _run_node_contract(script: str):
    node = shutil.which("node")
    if not node:
        pytest.fail("Node.js is required for executable AE contract tests")
    source = AE.read_text(encoding="utf-8")
    runner = f"""
const vm = require('vm');
const moduleObj = {{exports: {{}}}};
const context = {{module: moduleObj, exports: moduleObj.exports, console: console}};
vm.createContext(context);
vm.runInContext({json.dumps(source)}, context, {{filename: 'CutBridge.jsx'}});
const contract = moduleObj.exports;
{script}
"""
    result = subprocess.run(
        [node, "-"],
        input=runner,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def _manifest(schema_version=1):
    return {
        "schema": "cutbridge-manifest",
        "schema_version": schema_version,
        "cutbridge_version": tomllib.loads((ROOT / "apps/blender/cutbridge/blender_manifest.toml").read_text())["version"],
        "project": "TEST",
        "episode": "EP01",
        "scene": "SC010",
        "cut": "C001",
        "take": "T01",
        "version": 1,
        "fps": 24,
        "resolution": {"width": 1920, "height": 1080, "pixel_aspect": 1.0},
        "frames": {"start": 1001, "end": 1003, "count": 3},
        "passes": [
            {
                "name": "BEAUTY",
                "path": "render/beauty",
                "sequence_pattern": "C001_BEAUTY_####.png",
                "required": True,
            }
        ],
    }


def test_ae_rejects_unsupported_manifest_schema_version():
    manifest = _manifest(schema_version=2)
    result = _run_node_contract(
        f"console.log(JSON.stringify(contract.validateManifest({json.dumps(manifest)})));"
    )
    assert result
    assert any("schema_version 2" in message for message in result)


def test_ae_accepts_current_manifest_contract():
    manifest = _manifest()
    result = _run_node_contract(
        f"console.log(JSON.stringify(contract.validateManifest({json.dumps(manifest)})));"
    )
    assert result == []


def test_ae_accepts_optional_per_pass_format_and_rejects_extension_mismatch():
    manifest = _manifest()
    manifest["passes"][0]["image_format"] = "PNG"
    assert _run_node_contract(
        f"console.log(JSON.stringify(contract.validateManifest({json.dumps(manifest)})));"
    ) == []

    manifest["passes"][0]["image_format"] = "OPEN_EXR"
    errors = _run_node_contract(
        f"console.log(JSON.stringify(contract.validateManifest({json.dumps(manifest)})));"
    )
    assert any("extension does not match image_format OPEN_EXR" in message for message in errors)


def test_ae_legacy_manifest_without_per_pass_format_remains_valid():
    manifest = _manifest()
    assert "image_format" not in manifest["passes"][0]
    assert _run_node_contract(
        f"console.log(JSON.stringify(contract.validateManifest({json.dumps(manifest)})));"
    ) == []


def test_ae_sequence_coverage_requires_every_expected_frame():
    manifest = _manifest()
    pass_info = manifest["passes"][0]
    names = ["C001_BEAUTY_1001.png", "C001_BEAUTY_1003.png"]
    result = _run_node_contract(
        "console.log(JSON.stringify(contract.sequenceCoverage("
        f"{json.dumps(pass_info)}, {json.dumps(manifest)}, {json.dumps(names)})));"
    )
    assert result["complete"] is False
    assert result["missing"] == [1002]
    assert result["firstName"] is None


def test_ae_sequence_coverage_accepts_exact_range_and_flags_extra_matches():
    manifest = _manifest()
    pass_info = manifest["passes"][0]
    names = [
        "C001_BEAUTY_1001.png",
        "C001_BEAUTY_1002.png",
        "C001_BEAUTY_1003.png",
        "C001_BEAUTY_1004.png",
    ]
    result = _run_node_contract(
        "console.log(JSON.stringify(contract.sequenceCoverage("
        f"{json.dumps(pass_info)}, {json.dumps(manifest)}, {json.dumps(names)})));"
    )
    assert result["complete"] is True
    assert result["missing"] == []
    assert result["firstName"] == "C001_BEAUTY_1001.png"
    assert result["unexpected"] == ["C001_BEAUTY_1004.png"]


def test_ae_sequence_coverage_rejects_wrong_padding_for_expected_frame():
    manifest = _manifest()
    pass_info = manifest["passes"][0]
    names = [
        "C001_BEAUTY_01001.png",
        "C001_BEAUTY_1002.png",
        "C001_BEAUTY_1003.png",
    ]
    result = _run_node_contract(
        "console.log(JSON.stringify(contract.sequenceCoverage("
        f"{json.dumps(pass_info)}, {json.dumps(manifest)}, {json.dumps(names)})));"
    )
    assert result["complete"] is False
    assert result["missing"] == [1001]
    assert "C001_BEAUTY_01001.png" in result["unexpected"]


def test_ae_source_honors_optional_passes_and_has_no_stale_mvp_label():
    source = AE.read_text(encoding="utf-8")
    assert "p.required === false" in source
    assert "optional pass skipped" in source
    assert "MVP v0.1" not in source
    assert "CutBridge After Effects" in source
    assert "CutBridgeContract.PRODUCT_VERSION" in source


def test_ae_revision_entrypoint_and_release_sidecar_are_wired():
    source = AE.read_text(encoding="utf-8")
    revision = (ROOT / "apps/after-effects/revision_manager.js").read_text(encoding="utf-8")
    assert "function getRevisionManager()" in source
    assert "$.evalFile(scriptFile)" in source
    assert "Update Revision" in source
    assert "commitRevision" in source
    assert "CutBridgeRevisionManager" in revision


def test_ae_executable_contract_and_host_adapter_regressions():
    node = shutil.which("node")
    assert node, "Node.js is required for executable AE contract tests"
    subprocess.run([node, str(ROOT / "tests/ae_contract_checks.cjs")], cwd=ROOT, check=True)


@pytest.mark.parametrize("start,end,count,valid", [
    (1, 3, 3, True), (0, 2, 3, True), (0, 0, 1, True),
    (-3, -1, 3, False), (-1, 1, 3, False), (1.5, 3.5, 3, False),
])
def test_schema_and_ae_frame_type_and_sign_agree(start, end, count, valid):
    from jsonschema import Draft202012Validator

    manifest = _manifest()
    manifest["frames"] = {"start": start, "end": end, "count": count}
    schema = json.loads((ROOT / "packages/shared/cutbridge-manifest.schema.json").read_text(encoding="utf-8"))
    assert Draft202012Validator(schema).is_valid(manifest) is valid
    errors = _run_node_contract(f"console.log(JSON.stringify(contract.validateManifest({json.dumps(manifest)})));")
    assert (not errors) is valid
