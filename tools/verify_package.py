#!/usr/bin/env python3
"""Verify candidate CutBridge ZIPs against an exact source snapshot.

``tools/build_release.py`` is byte-deterministic for one toolchain, but the
compressed bytes depend on the zlib implementation (for example CPython 3.14+
on Windows ships zlib-ng). A whole-ZIP SHA-256 therefore proves identity only
against ZIPs built with the same zlib. This verifier rebuilds the artifacts from
the named source snapshot and compares them entry by entry (names, order and the
SHA-256 of each uncompressed entry), independent of compression. It never
installs, modifies or publishes anything.

The source snapshot comes from ``git archive`` of a commit with line-ending
conversion disabled, so a CRLF Windows checkout cannot change the result.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
KINDS = ("blender", "after_effects")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _entries(path: Path) -> list[tuple[str, str]]:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise ValueError(f"{path.name}: corrupt ZIP entry {bad!r}")
        return [(info.filename, _sha256_bytes(archive.read(info))) for info in archive.infolist()]


def compare_zips(expected: Path, actual: Path) -> dict:
    """Compare two ZIPs by entry names, order and uncompressed content."""
    want = _entries(expected)
    have = _entries(actual)
    want_map, have_map = dict(want), dict(have)
    names = [name for name, _ in have]
    unsafe = [n for n in names if n.startswith(("/", "\\")) or ".." in Path(n).parts or ":" in n]
    return {
        "content_identical": want == have,
        "missing_entries": sorted(set(want_map) - set(have_map)),
        "unexpected_entries": sorted(set(have_map) - set(want_map)),
        "changed_entries": sorted(n for n in want_map if n in have_map and want_map[n] != have_map[n]),
        "order_differs": want != have and sorted(want) == sorted(have) and [n for n, _ in want] != names,
        "duplicate_entries": sorted({n for n in names if names.count(n) > 1}),
        "unsafe_entry_names": unsafe,
        "entries": len(have),
    }


def _load_builder(source_root: Path):
    script = source_root / "tools" / "build_release.py"
    spec = importlib.util.spec_from_file_location("snapshot_build_release", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(source_root: Path, tag: str, zips: dict[str, Path], workdir: Path) -> dict:
    """Rebuild from ``source_root`` and compare each supplied ZIP by content."""
    builder = _load_builder(source_root)
    metadata = builder.build(tag=tag, output_dir=workdir / "rebuild")
    report = {"tag": tag, "artifacts": {}, "ok": True}
    for kind, supplied in zips.items():
        filename = metadata["artifacts"][kind]["filename"]
        rebuilt = workdir / "rebuild" / filename
        result = compare_zips(rebuilt, supplied)
        result.update(
            {
                "filename": supplied.name,
                "expected_filename": filename,
                "zip_sha256": _sha256_file(supplied),
                "rebuilt_sha256_this_toolchain": _sha256_file(rebuilt),
                "zip_bytes_identical_to_rebuild": supplied.read_bytes() == rebuilt.read_bytes(),
            }
        )
        result["ok"] = (
            result["content_identical"]
            and supplied.name == filename
            and not result["duplicate_entries"]
            and not result["unsafe_entry_names"]
        )
        report["ok"] = report["ok"] and result["ok"]
        report["artifacts"][kind] = result
    return report


def _snapshot_from_commit(commit: str, destination: Path) -> str:
    full = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--verify", f"{commit}^{{commit}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    tar_path = destination / "source.tar"
    subprocess.run(
        ["git", "-C", str(ROOT), "-c", "core.autocrlf=false", "archive", "--format=tar", "-o", str(tar_path), full],
        check=True,
    )
    source = destination / "source"
    source.mkdir()
    with tarfile.open(tar_path) as archive:
        try:
            archive.extractall(source, filter="data")
        except TypeError:  # Python < 3.12 has no extraction filters
            archive.extractall(source)
    return full


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tag", required=True, help="Release tag used to build the candidate, e.g. v0.2.5")
    parser.add_argument("--source-commit", default="HEAD", help="Commit the candidate must come from (default HEAD)")
    parser.add_argument("--source-dir", help="Use this directory as the source snapshot instead of a git commit")
    parser.add_argument("--blender-zip", type=Path, required=True)
    parser.add_argument("--ae-zip", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="Write the JSON report here")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        if args.source_dir:
            source_root, commit = Path(args.source_dir).resolve(), None
        else:
            commit = _snapshot_from_commit(args.source_commit, work)
            source_root = work / "source"
        report = verify(source_root, args.tag, {"blender": args.blender_zip, "after_effects": args.ae_zip}, work)
    report["source_commit"] = commit
    report["toolchain"] = {"python": sys.version.split()[0], "zlib": zlib.ZLIB_RUNTIME_VERSION}
    report["scope"] = (
        "Package-to-source content identity only. This is not an install, native-host or release approval."
    )
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
