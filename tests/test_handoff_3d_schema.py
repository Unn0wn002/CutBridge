import json
import shutil
import subprocess
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "packages" / "shared" / "cutbridge-manifest.schema.json"


def _legacy_manifest():
    return {
        "schema": "cutbridge-manifest",
        "schema_version": 1,
        "cutbridge_version": "0.2.3",
        "project": "PROJECT",
        "episode": "EP01",
        "scene": "SC010",
        "cut": "C001",
        "take": "T01",
        "version": 1,
        "fps": 24.0,
        "resolution": {"width": 1920, "height": 1080, "pixel_aspect": 1.0},
        "frames": {"start": 1, "end": 2, "count": 2},
        "passes": [
            {
                "name": "BEAUTY",
                "path": "render/beauty",
                "sequence_pattern": "C001_BEAUTY_####.png",
                "required": True,
            }
        ],
    }


def _sample(frame, time, x=960.0):
    return {
        "frame": frame,
        "time": time,
        "position": [x, 540.0, 0.0],
        "basis": {
            "x": [1.0, 0.0, 0.0],
            "y": [0.0, 0.0, 1.0],
            "z": [0.0, -1.0, 0.0],
        },
        "scale": [1.0, 1.0, 1.0],
    }


def _handoff():
    camera_sample = _sample(1, 0.0)
    camera_sample.update(
        {
            "forward": [0.0, 1.0, 0.0],
            "up": [0.0, 0.0, 1.0],
            "horizontal_fov_radians": 0.691111,
            "ae_zoom": 2666.666,
        }
    )
    return {
        "schema": "cutbridge-handoff-3d",
        "schema_version": 1,
        "space": {
            "coordinate_system": "after-effects-composition",
            "axis_map": "blender_xyz_to_ae_x_negz_y",
            "origin": "composition-center",
            "position_units": "pixels",
            "pixels_per_blender_unit": 100.0,
        },
        "sampling": {
            "mode": "baked-per-frame",
            "frame_start": 1,
            "frame_end": 1,
            "frame_step": 1,
        },
        "camera": {
            "name": "Camera",
            "type": "PERSP",
            "samples": [camera_sample],
        },
        "nulls": [
            {
                "name": "Guide",
                "source_type": "EMPTY",
                "samples": [_sample(1, 0.0, 1060.0)],
            }
        ],
    }


def _validator():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def test_legacy_manifest_without_handoff_3d_remains_valid():
    _validator().validate(_legacy_manifest())


def test_optional_handoff_3d_payload_is_schema_valid():
    manifest = _legacy_manifest()
    manifest["handoff_3d"] = _handoff()
    _validator().validate(manifest)


def test_handoff_schema_version_is_fail_closed():
    manifest = _legacy_manifest()
    payload = _handoff()
    payload["schema_version"] = 2
    manifest["handoff_3d"] = payload
    with pytest.raises(jsonschema.ValidationError):
        _validator().validate(manifest)


def test_handoff_rejects_unknown_payload_fields():
    manifest = _legacy_manifest()
    payload = _handoff()
    payload["command"] = "execute something"
    manifest["handoff_3d"] = payload
    with pytest.raises(jsonschema.ValidationError):
        _validator().validate(manifest)


def test_handoff_nulls_are_empty_only():
    manifest = _legacy_manifest()
    payload = _handoff()
    payload["nulls"][0]["source_type"] = "MESH"
    manifest["handoff_3d"] = payload
    with pytest.raises(jsonschema.ValidationError):
        _validator().validate(manifest)


def test_existing_ae_validator_ignores_optional_handoff_block():
    node = shutil.which("node")
    assert node, "Node is required for AE compatibility validation"
    manifest = _legacy_manifest()
    manifest["handoff_3d"] = _handoff()
    script = """
const C = require('./apps/after-effects/CutBridge.jsx');
const manifest = JSON.parse(process.argv[1]);
const errors = C.validateManifest(manifest);
if (errors.length) { console.error(errors.join('\\n')); process.exit(1); }
"""
    subprocess.run(
        [node, "-e", script, json.dumps(manifest)],
        cwd=ROOT,
        check=True,
    )
