#!/usr/bin/env python3
"""Fail-closed authorization gate for CutBridge GitHub Release publication."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_release import parse_release_tag

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORIZATION = ROOT / "release-authorization.json"


def validate_authorization(*, approval: dict, tag: str, release_sha: str, main_sha: str) -> dict:
    release = parse_release_tag(tag)
    if release_sha != main_sha:
        raise ValueError(
            f"Tagged commit {release_sha} is not the current main HEAD {main_sha}."
        )
    if approval.get("approved") is not True:
        raise ValueError("Release authorization is not approved.")
    if approval.get("tag") != tag:
        raise ValueError(
            f"Authorization tag {approval.get('tag')!r} does not match release tag {tag!r}."
        )
    if approval.get("channel") != release["channel"]:
        raise ValueError(
            f"Authorization channel {approval.get('channel')!r} does not match "
            f"tag channel {release['channel']!r}."
        )
    if approval.get("prerelease") is not release["prerelease"]:
        raise ValueError(
            f"Authorization prerelease flag {approval.get('prerelease')!r} does not match "
            f"tag prerelease={release['prerelease']!r}."
        )
    return release


def _write_github_output(path: Path, release: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"channel={release['channel']}\n")
        handle.write(f"prerelease={'true' if release['prerelease'] else 'false'}\n")
        handle.write(f"release_version={release['release_version']}\n")
        handle.write(f"product_version={release['base_version']}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    parser.add_argument("--sha", required=True, help="Tagged commit SHA")
    parser.add_argument("--main-sha", required=True, help="Current origin/main HEAD SHA")
    parser.add_argument("--authorization", default=str(DEFAULT_AUTHORIZATION))
    parser.add_argument("--github-output")
    args = parser.parse_args()

    authorization_path = Path(args.authorization)
    if not authorization_path.is_file():
        raise SystemExit(f"Refusing release: {authorization_path} is missing.")
    try:
        approval = json.loads(authorization_path.read_text(encoding="utf-8"))
        release = validate_authorization(
            approval=approval,
            tag=args.tag,
            release_sha=args.sha,
            main_sha=args.main_sha,
        )
    except (ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Refusing release: {exc}") from exc

    if args.github_output:
        _write_github_output(Path(args.github_output), release)
    print(
        f"Authorized {release['tag']} as channel={release['channel']} "
        f"prerelease={release['prerelease']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
