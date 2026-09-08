#!/usr/bin/env python3
"""Build deterministic CutBridge release artifacts.

The script is intentionally independent from Blender so CI can verify packaging
on every pull request. Stable and prerelease tags must share the source product
version declared by Blender and After Effects.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BLENDER_ROOT = ROOT / "apps" / "blender" / "cutbridge"
AE_SCRIPT = ROOT / "apps" / "after-effects" / "CutBridge.jsx"
AE_REVISION = ROOT / "apps" / "after-effects" / "revision_manager.js"
AE_QC_PLUS = ROOT / "apps" / "after-effects" / "qc_plus.js"
AE_INSTALL = ROOT / "apps" / "after-effects" / "INSTALL.md"
UPDATE_SCHEMA_VERSION = 1
RELEASE_TAG_RE = re.compile(
    r"^v(?P<base>[0-9]+\.[0-9]+\.[0-9]+)(?:-(?P<label>rc|beta|dev)\.(?P<number>[1-9][0-9]*))?$"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_manifest() -> dict:
    with (BLENDER_ROOT / "blender_manifest.toml").open("rb") as handle:
        return tomllib.load(handle)


def parse_release_tag(tag: str) -> dict:
    """Return product/release version, channel, and prerelease semantics."""
    tag = tag.strip()
    match = RELEASE_TAG_RE.fullmatch(tag)
    if not match:
        raise ValueError(
            "Release tag must use vMAJOR.MINOR.PATCH, vMAJOR.MINOR.PATCH-rc.N, "
            "vMAJOR.MINOR.PATCH-beta.N, or vMAJOR.MINOR.PATCH-dev.N"
        )
    base_version = match.group("base")
    label = match.group("label")
    release_version = tag[1:]
    if label is None:
        channel = "stable"
        prerelease = False
    elif label in {"rc", "beta"}:
        channel = "beta"
        prerelease = True
    else:
        channel = "development"
        prerelease = True
    return {
        "tag": tag,
        "base_version": base_version,
        "release_version": release_version,
        "channel": channel,
        "prerelease": prerelease,
    }


def _release_version(tag: str) -> str:
    """Backward-compatible helper returning the source/product version."""
    return parse_release_tag(tag)["base_version"]


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
    ae_versions = re.findall(r'var PRODUCT_VERSION = "([^"\n]+)";', AE_SCRIPT.read_text(encoding="utf-8"))
    if ae_versions != [version]:
        raise ValueError("CutBridge.jsx PRODUCT_VERSION does not match the release version")


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
    if not AE_SCRIPT.is_file() or not AE_REVISION.is_file() or not AE_QC_PLUS.is_file() or not AE_INSTALL.is_file():
        raise RuntimeError("Missing After Effects scripts or installation guide required for release")
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        _write_entry(archive, AE_SCRIPT, "CutBridge.jsx")
        _write_entry(archive, AE_REVISION, "revision_manager.js")
        _write_entry(archive, AE_QC_PLUS, "qc_plus.js")
        _write_entry(archive, AE_INSTALL, "INSTALL.md")
        _write_entry(archive, ROOT / "LICENSE", "LICENSE")


def build(tag: str, output_dir: Path) -> dict:
    manifest = _read_manifest()
    release = parse_release_tag(tag)
    version = release["base_version"]
    if manifest["version"] != version:
        raise ValueError(
            f"Tag {tag!r} targets product version {version!r}, which does not match "
            f"blender_manifest.toml version {manifest['version']!r}"
        )

    _validate_source_version(version)
    required_release_sources = (ROOT / "LICENSE", AE_SCRIPT, AE_REVISION, AE_QC_PLUS, AE_INSTALL)
    if not all(path.is_file() for path in required_release_sources):
        raise ValueError("Release source must include LICENSE, CutBridge.jsx, revision_manager.js, qc_plus.js and INSTALL.md")
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
        "version": release["release_version"],
        "product_version": version,
        "tag": tag,
        "channel": release["channel"],
        "prerelease": release["prerelease"],
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
    parser.add_argument(
        "--tag",
        required=True,
        help="Release tag, e.g. v0.2.3 or v0.2.3-rc.1",
    )
    parser.add_argument("--output", default="dist", help="Output directory")
    args = parser.parse_args()

    metadata = build(tag=args.tag, output_dir=(ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output))
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
