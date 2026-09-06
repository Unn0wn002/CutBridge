#!/usr/bin/env python3
"""Build deterministic CutBridge release artifacts.

The script is intentionally independent from Blender so CI can verify packaging
on every pull request. A release tag must match blender_manifest.toml exactly.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BLENDER_ROOT = ROOT / "apps" / "blender" / "cutbridge"
AE_SCRIPT = ROOT / "apps" / "after-effects" / "CutBridge.jsx"
UPDATE_SCHEMA_VERSION = 1


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_manifest() -> dict:
    with (BLENDER_ROOT / "blender_manifest.toml").open("rb") as handle:
        return tomllib.load(handle)


def _release_version(tag: str) -> str:
    tag = tag.strip()
    if not tag.startswith("v") or len(tag) <= 1:
        raise ValueError("Release tag must use vMAJOR.MINOR.PATCH")
    return tag[1:]


def _validate_source_version(version: str) -> None:
    """Read constants without importing Blender or executing extension code."""
    tree = ast.parse((BLENDER_ROOT / "version.py").read_text(encoding="utf-8"))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"__version__", "VERSION"}:
                    values[target.id] = ast.literal_eval(node.value)
    if values.get("__version__") != version or values.get("VERSION") != tuple(int(x) for x in version.split(".")):
        raise ValueError("version.py constants do not match the release version")


def _write_entry(archive: zipfile.ZipFile, source: Path, name: str) -> None:
    # Checkout times and OS permissions must not change release checksums.
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    archive.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def _include_blender_file(path: Path) -> bool:
    relative = path.relative_to(BLENDER_ROOT)
    parts = relative.parts
    if any(part == "__pycache__" or part.startswith(".") for part in parts):
        return False
    if path.suffix in {".pyc", ".pyo", ".zip"}:
        return False
    return path.is_file()


def _write_blender_zip(path: Path) -> None:
    entries = sorted(
        (item for item in BLENDER_ROOT.rglob("*") if _include_blender_file(item)),
        key=lambda item: item.relative_to(BLENDER_ROOT).as_posix(),
    )
    if not entries:
        raise RuntimeError("No Blender extension files found")

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in entries:
            relative = source.relative_to(BLENDER_ROOT).as_posix()
            _write_entry(archive, source, relative)
        _write_entry(archive, ROOT / "LICENSE", "LICENSE")


def _write_ae_zip(path: Path) -> None:
    if not AE_SCRIPT.is_file():
        raise RuntimeError(f"Missing After Effects script: {AE_SCRIPT}")
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        _write_entry(archive, AE_SCRIPT, "CutBridge.jsx")
        _write_entry(archive, ROOT / "LICENSE", "LICENSE")


def build(tag: str, output_dir: Path) -> dict:
    manifest = _read_manifest()
    version = _release_version(tag)
    if manifest["version"] != version:
        raise ValueError(
            f"Tag {tag!r} does not match blender_manifest.toml version {manifest['version']!r}"
        )

    _validate_source_version(version)
    if not (ROOT / "LICENSE").is_file() or not AE_SCRIPT.is_file():
        raise ValueError("Release source must include LICENSE and CutBridge.jsx")
    blender_name = f"CutBridge-Blender-{tag}.zip"
    ae_name = f"CutBridge-AfterEffects-{tag}.zip"
    output_dir = output_dir.resolve()
    # Never erase source, another release, or unrelated user files.
    if output_dir == ROOT.resolve() or output_dir in ROOT.resolve().parents or output_dir.is_relative_to((ROOT / "apps").resolve()):
        raise ValueError("Release output must not overlap source directories")
    expected_names = {blender_name, ae_name, "SHA256SUMS.txt", "release-metadata.json"}
    if output_dir.exists():
        for existing in output_dir.iterdir():
            if existing.name not in expected_names or existing.is_symlink() or not existing.is_file():
                raise ValueError(f"Use an empty release directory; refusing to replace {existing.name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    blender_zip = output_dir / blender_name
    ae_zip = output_dir / ae_name

    _write_blender_zip(blender_zip)
    _write_ae_zip(ae_zip)

    checksums = {
        blender_name: _sha256(blender_zip),
        ae_name: _sha256(ae_zip),
    }
    checksum_path = output_dir / "SHA256SUMS.txt"
    checksum_path.write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())),
        encoding="utf-8",
    )

    release_metadata = {
        "schema_version": UPDATE_SCHEMA_VERSION,
        "version": version,
        "tag": tag,
        "channel": "stable",
        "blender_version_min": manifest["blender_version_min"],
        "artifacts": {
            "blender": {
                "filename": blender_name,
                "sha256": checksums[blender_name],
            },
            "after_effects": {
                "filename": ae_name,
                "sha256": checksums[ae_name],
            },
        },
        "distribution_note": (
            "Mirror release artifacts and a generated update index to a distribution endpoint "
            "that is separate from the private source repository"
        ),
    }
    metadata_path = output_dir / "release-metadata.json"
    metadata_path.write_text(
        json.dumps(release_metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return release_metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True, help="Release tag, e.g. v0.2.0")
    parser.add_argument("--output", default="dist", help="Output directory")
    args = parser.parse_args()

    metadata = build(args.tag, (ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output))
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
