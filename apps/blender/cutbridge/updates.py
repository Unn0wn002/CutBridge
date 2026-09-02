"""Pure update-index parsing and selection logic.

CutBridge never installs or replaces itself from this module. The updater only
selects a compatible release and reports it to Blender UI code. Installation is
left to the user / Blender Extensions repository workflow.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, List, Optional, Tuple

UPDATE_INDEX_SCHEMA_VERSION = 1
ALLOWED_CHANNELS = ("stable", "beta", "development")
CHANNEL_VISIBILITY = {
    "stable": {"stable"},
    "beta": {"stable", "beta"},
    "development": {"stable", "beta", "development"},
}

_SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$"
)


class UpdateIndexError(ValueError):
    """Raised when update metadata is missing, malformed, or unsafe to consume."""


def _pre_release_key(value: Optional[str]) -> Tuple[Any, ...]:
    # SemVer: stable releases sort after prereleases with the same numeric core.
    if value is None:
        return (1,)

    tokens: List[Tuple[int, Any]] = []
    for token in value.split("."):
        if token.isdigit():
            tokens.append((0, int(token)))
        else:
            tokens.append((1, token.lower()))
    return (0, *tokens)


def semver_key(value: str) -> Tuple[Any, ...]:
    match = _SEMVER_RE.match(value.strip())
    if not match:
        raise UpdateIndexError(f"Invalid semantic version: {value!r}")
    major, minor, patch = (int(match.group(i)) for i in (1, 2, 3))
    return major, minor, patch, _pre_release_key(match.group(4))


def normalize_blender_version(value: Iterable[int]) -> Tuple[int, int, int]:
    parts = list(value)[:3]
    while len(parts) < 3:
        parts.append(0)
    return int(parts[0]), int(parts[1]), int(parts[2])


def _parse_blender_version(value: str) -> Tuple[int, int, int]:
    parts = value.split(".")
    if not 2 <= len(parts) <= 3 or not all(part.isdigit() for part in parts):
        raise UpdateIndexError(f"Invalid Blender version: {value!r}")
    values = [int(part) for part in parts]
    while len(values) < 3:
        values.append(0)
    return values[0], values[1], values[2]


def validate_update_index(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise UpdateIndexError("Update index must be a JSON object")
    if payload.get("schema_version") != UPDATE_INDEX_SCHEMA_VERSION:
        raise UpdateIndexError(
            f"Unsupported update-index schema: {payload.get('schema_version')!r}"
        )
    releases = payload.get("releases")
    if not isinstance(releases, list):
        raise UpdateIndexError("Update index must contain a releases array")

    for item in releases:
        if not isinstance(item, dict):
            raise UpdateIndexError("Every release entry must be an object")
        for key in ("version", "channel", "blender_version_min", "release_page_url"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise UpdateIndexError(f"Release is missing required string field: {key}")
        semver_key(item["version"])
        _parse_blender_version(item["blender_version_min"])
        if item["channel"] not in ALLOWED_CHANNELS:
            raise UpdateIndexError(f"Unsupported release channel: {item['channel']!r}")
        if "blender_version_max" in item and item["blender_version_max"] is not None:
            if not isinstance(item["blender_version_max"], str):
                raise UpdateIndexError("blender_version_max must be a string when present")
            _parse_blender_version(item["blender_version_max"])
        if "platforms" in item:
            if not isinstance(item["platforms"], list) or not all(
                isinstance(platform_name, str) and platform_name
                for platform_name in item["platforms"]
            ):
                raise UpdateIndexError("platforms must be an array of non-empty strings")

    return payload


def release_is_compatible(
    release: Dict[str, Any],
    blender_version: Iterable[int],
    platform_name: str,
    selected_channel: str,
) -> bool:
    if selected_channel not in CHANNEL_VISIBILITY:
        raise UpdateIndexError(f"Unknown selected channel: {selected_channel!r}")
    if release["channel"] not in CHANNEL_VISIBILITY[selected_channel]:
        return False

    current_blender = normalize_blender_version(blender_version)
    minimum = _parse_blender_version(release["blender_version_min"])
    if current_blender < minimum:
        return False

    maximum = release.get("blender_version_max")
    if maximum and current_blender >= _parse_blender_version(maximum):
        return False

    platforms = release.get("platforms")
    if platforms and platform_name not in platforms:
        return False

    return True


def select_latest_compatible(
    payload: Dict[str, Any],
    *,
    current_version: str,
    blender_version: Iterable[int],
    platform_name: str,
    selected_channel: str = "stable",
) -> Optional[Dict[str, Any]]:
    payload = validate_update_index(payload)
    current_key = semver_key(current_version)

    candidates = [
        release
        for release in payload["releases"]
        if release_is_compatible(
            release,
            blender_version=blender_version,
            platform_name=platform_name,
            selected_channel=selected_channel,
        )
        and semver_key(release["version"]) > current_key
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda release: semver_key(release["version"]))


def fetch_update_index(url: str, *, timeout: float = 4.0, max_bytes: int = 1_000_000) -> Dict[str, Any]:
    url = (url or "").strip()
    if not url:
        raise UpdateIndexError("No update index URL is configured")

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"https", "http", "file"}:
        raise UpdateIndexError("Update index URL must use https, http, or file")

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "CutBridge-Update-Check/0.2",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read(max_bytes + 1)
    except (OSError, urllib.error.URLError) as exc:
        raise UpdateIndexError(f"Unable to read update index: {exc}") from exc

    if len(data) > max_bytes:
        raise UpdateIndexError("Update index exceeds the maximum allowed size")

    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UpdateIndexError("Update index is not valid UTF-8 JSON") from exc

    return validate_update_index(payload)
