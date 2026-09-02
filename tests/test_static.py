import json
import pathlib
import py_compile
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLENDER = ROOT / "apps" / "blender" / "cutbridge"


def test_python_sources_compile():
    for path in BLENDER.glob("*.py"):
        py_compile.compile(str(path), doraise=True)


def test_blender_manifest_parses():
    with (BLENDER / "blender_manifest.toml").open("rb") as fh:
        manifest = tomllib.load(fh)
    assert manifest["id"] == "cutbridge"
    assert manifest["type"] == "add-on"
    assert manifest["version"] == "0.1.0"


def test_shared_manifest_schema_parses():
    schema_path = ROOT / "packages" / "shared" / "cutbridge-manifest.schema.json"
    with schema_path.open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    assert schema["title"] == "CutBridge Manifest"
