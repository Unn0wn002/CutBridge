import json
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
AE = ROOT / "apps" / "after-effects" / "CutBridge.jsx"


def _run_node_contract(script: str):
    node = shutil.which("node")
    if not node:
        pytest.skip("Node.js is required for executable AE contract tests")
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
        [node, "-e", runner],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _manifest(schema_version=1):
    return {
        "schema": "cutbridge-manifest",
        "schema_version": schema_version,
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
    assert "CutBridge After Effects v0.2.3" in source
