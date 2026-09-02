#!/usr/bin/env python3
"""Build deterministic CutBridge release artifacts.

The script is intentionally independent from Blender so CI can verify packaging
on every pull request. A release tag must match blender_manifest.toml exactly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
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
            archive.write(source, relative)


def _write_ae_zip(path: Path) -> None:
    if not AE_SCRIPT.is_file():
        raise RuntimeError(f"Missing After Effects script: {AE_SCRIPT}")
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(AE_SCRIPT, "CutBridge.jsx")


def build(tag: str, output_dir: Path) -> dict:
    manifest = _read_manifest()
    version = _release_version(tag)
    if manifest["version"] != version:
        raise ValueError(
            f"Tag {tag!r} does not match blender_manifest.toml version {manifest['version']!r}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    for existing in output_dir.iterdir():
        if existing.is_dir():
            shutil.rmtree(existing)
        else:
            existing.unlink()

    blender_name = f"CutBridge-Blender-{tag}.zip"
    ae_name = f"CutBridge-AfterEffects-{tag}.zip"
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
