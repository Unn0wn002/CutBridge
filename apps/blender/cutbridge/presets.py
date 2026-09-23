from __future__ import annotations

import copy
import json
import re
from contextlib import contextmanager
from pathlib import Path
from string import Formatter

PRESET_SCHEMA = "cutbridge-studio-preset"
PRESET_SCHEMA_VERSION = 1
MAX_PRESET_BYTES = 64 * 1024

SUPPORTED_IMAGE_FORMATS = ("PNG", "OPEN_EXR", "TIFF")
SUPPORTED_PASSES = ("BEAUTY", "LINE", "SHADOW", "DEPTH")

_ALLOWED_TEMPLATE_FIELDS = {
    "project",
    "episode",
    "scene",
    "cut",
    "take",
    "version",
    "pass",
}
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_FOLDER_SEGMENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_VERSION_PREFIX_RE = re.compile(r"^[A-Za-z0-9_-]{1,8}$")
_ACTIVE_FILE_SNAPSHOTS: dict[str, dict] = {}


class PresetError(ValueError):
    """Stable fail-closed preset validation error consumed by Blender diagnostics."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


_DEFAULT_PRESET = {
    "schema": PRESET_SCHEMA,
    "schema_version": PRESET_SCHEMA_VERSION,
    "id": "cutbridge-default",
    "name": "CutBridge Default",
    "naming": {
        "package": "{project}_{episode}_{scene}_{cut}_{take}_{version}",
        "sequence": "{cut}_{pass}_####",
        "ae_comp": "{cut}_COMP",
    },
    "folders": {
        "render": "render",
        "preview": "preview",
        "camera": "camera",
    },
    "passes": [
        {"name": "BEAUTY", "required": True},
    ],
    "output": {
        "image_format": "PNG",
    },
    "versioning": {
        "prefix": "V",
        "padding": 3,
    },
}


def default_preset() -> dict:
    """Return a fresh copy of the safe built-in preset."""
    return copy.deepcopy(_DEFAULT_PRESET)


def manual_preset(settings) -> dict:
    """Represent the legacy/manual controls as a normalized effective preset.

    Manual mode intentionally preserves all pre-S9 behavior. It is not loaded
    from disk and therefore cannot introduce a preset-file trust boundary.
    """
    passes = []
    use_per_pass_formats = bool(getattr(settings, "per_pass_formats_enabled", False))
    for name, attr, format_attr in (
        ("BEAUTY", "pass_beauty", "format_beauty"),
        ("LINE", "pass_line", "format_line"),
        ("SHADOW", "pass_shadow", "format_shadow"),
        ("DEPTH", "pass_depth", "format_depth"),
    ):
        if bool(getattr(settings, attr, False)):
            item = {"name": name, "required": True}
            if use_per_pass_formats:
                item["image_format"] = str(
                    getattr(settings, format_attr, getattr(settings, "image_format", "PNG"))
                )
            passes.append(item)

    return {
        "schema": PRESET_SCHEMA,
        "schema_version": PRESET_SCHEMA_VERSION,
        "id": "manual",
        "name": "Manual",
        "naming": copy.deepcopy(_DEFAULT_PRESET["naming"]),
        "folders": copy.deepcopy(_DEFAULT_PRESET["folders"]),
        "passes": passes,
        "output": {
            "image_format": str(getattr(settings, "image_format", "PNG")),
        },
        "versioning": copy.deepcopy(_DEFAULT_PRESET["versioning"]),
    }


def _expect_keys(value: dict, allowed: set[str], required: set[str], location: str) -> None:
    missing = sorted(required.difference(value.keys()))
    if missing:
        raise PresetError(
            "PRESET_FIELD_INVALID",
            f"{location} is missing required field(s): {', '.join(missing)}.",
        )
    unknown = sorted(set(value.keys()).difference(allowed))
    if unknown:
        raise PresetError(
            "PRESET_FIELD_INVALID",
            f"{location} contains unsupported field(s): {', '.join(unknown)}.",
        )


def _validate_template(template: object, location: str, *, require_pass: bool = False, require_hashes: bool = False) -> str:
    if not isinstance(template, str) or not template or len(template) > 160:
        raise PresetError("PRESET_FIELD_INVALID", f"{location} must be a non-empty string up to 160 characters.")
    if any(ord(char) < 32 for char in template) or "/" in template or "\\" in template:
        raise PresetError("PRESET_FIELD_INVALID", f"{location} cannot contain path separators or control characters.")

    seen_fields: set[str] = set()
    try:
        parsed = list(Formatter().parse(template))
    except ValueError as exc:
        raise PresetError("PRESET_FIELD_INVALID", f"{location} is not a valid naming template: {exc}") from exc

    for _literal, field_name, format_spec, conversion in parsed:
        if field_name is None:
            continue
        if not field_name or field_name not in _ALLOWED_TEMPLATE_FIELDS:
            raise PresetError("PRESET_FIELD_INVALID", f"{location} uses unsupported placeholder {{{field_name}}}.")
        if format_spec or conversion:
            raise PresetError("PRESET_FIELD_INVALID", f"{location} cannot use format specs or conversions.")
        seen_fields.add(field_name)

    if require_pass and "pass" not in seen_fields:
        raise PresetError("PRESET_FIELD_INVALID", f"{location} must contain the {{pass}} placeholder.")
    if require_hashes and "####" not in template:
        raise PresetError("PRESET_FIELD_INVALID", f"{location} must contain the literal #### frame token.")
    return template


def _validate_folder(value: object, location: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 192:
        raise PresetError("PRESET_FIELD_INVALID", f"{location} must be a non-empty relative folder path.")
    if "\\" in value or value.startswith("/") or value.endswith("/"):
        raise PresetError("PRESET_PATH_UNSAFE", f"{location} must use a relative forward-slash path.")

    segments = value.split("/")
    if any(segment in ("", ".", "..") for segment in segments):
        raise PresetError("PRESET_PATH_UNSAFE", f"{location} cannot contain empty, dot, or parent path segments.")
    if any(not _FOLDER_SEGMENT_RE.fullmatch(segment) for segment in segments):
        raise PresetError(
            "PRESET_PATH_UNSAFE",
            f"{location} contains unsupported characters; use letters, numbers, dot, underscore, or hyphen.",
        )
    return value


def _validate_folder_separation(folders: dict[str, str]) -> None:
    """Keep render/preview/camera trees disjoint so payload roles cannot alias."""
    items = list(folders.items())
    for index, (left_name, left_path) in enumerate(items):
        for right_name, right_path in items[index + 1:]:
            if left_path == right_path:
                raise PresetError(
                    "PRESET_PATH_UNSAFE",
                    f"preset.folders.{left_name} and preset.folders.{right_name} must be distinct.",
                )
            if left_path.startswith(right_path + "/") or right_path.startswith(left_path + "/"):
                raise PresetError(
                    "PRESET_PATH_UNSAFE",
                    f"preset.folders.{left_name} and preset.folders.{right_name} cannot overlap or contain one another.",
                )


def validate_preset(data: object) -> dict:
    """Validate and normalize untrusted JSON preset data without executing it."""
    if not isinstance(data, dict):
        raise PresetError("PRESET_SCHEMA_INVALID", "Studio preset root must be a JSON object.")

    _expect_keys(
        data,
        {"schema", "schema_version", "id", "name", "naming", "folders", "passes", "output", "versioning"},
        {"schema", "schema_version", "id", "name", "naming", "folders", "passes", "output", "versioning"},
        "preset",
    )

    if data.get("schema") != PRESET_SCHEMA:
        raise PresetError("PRESET_SCHEMA_INVALID", f"Preset schema must be {PRESET_SCHEMA!r}.")
    if data.get("schema_version") != PRESET_SCHEMA_VERSION:
        raise PresetError(
            "PRESET_SCHEMA_UNSUPPORTED",
            f"Preset schema_version must be {PRESET_SCHEMA_VERSION}; got {data.get('schema_version')!r}.",
        )

    preset_id = data.get("id")
    if not isinstance(preset_id, str) or not _ID_RE.fullmatch(preset_id):
        raise PresetError("PRESET_FIELD_INVALID", "Preset id must be 1-64 safe identifier characters.")
    preset_name = data.get("name")
    if not isinstance(preset_name, str) or not preset_name.strip() or len(preset_name) > 96:
        raise PresetError("PRESET_FIELD_INVALID", "Preset name must be a non-empty string up to 96 characters.")

    naming = data.get("naming")
    if not isinstance(naming, dict):
        raise PresetError("PRESET_FIELD_INVALID", "preset.naming must be an object.")
    _expect_keys(naming, {"package", "sequence", "ae_comp"}, {"package", "sequence", "ae_comp"}, "preset.naming")
    normalized_naming = {
        "package": _validate_template(naming.get("package"), "preset.naming.package"),
        "sequence": _validate_template(
            naming.get("sequence"),
            "preset.naming.sequence",
            require_pass=True,
            require_hashes=True,
        ),
        "ae_comp": _validate_template(naming.get("ae_comp"), "preset.naming.ae_comp"),
    }

    folders = data.get("folders")
    if not isinstance(folders, dict):
        raise PresetError("PRESET_FIELD_INVALID", "preset.folders must be an object.")
    _expect_keys(folders, {"render", "preview", "camera"}, {"render", "preview", "camera"}, "preset.folders")
    normalized_folders = {
        key: _validate_folder(folders.get(key), f"preset.folders.{key}")
        for key in ("render", "preview", "camera")
    }
    _validate_folder_separation(normalized_folders)

    passes = data.get("passes")
    if not isinstance(passes, list) or not passes:
        raise PresetError("PRESET_FIELD_INVALID", "preset.passes must contain at least one pass definition.")
    normalized_passes = []
    seen_passes: set[str] = set()
    for index, item in enumerate(passes):
        if not isinstance(item, dict):
            raise PresetError("PRESET_FIELD_INVALID", f"preset.passes[{index}] must be an object.")
        _expect_keys(
            item,
            {"name", "required", "image_format"},
            {"name", "required"},
            f"preset.passes[{index}]",
        )
        name = item.get("name")
        required = item.get("required")
        pass_image_format = item.get("image_format")
        if name not in SUPPORTED_PASSES:
            raise PresetError("PRESET_FIELD_INVALID", f"preset.passes[{index}].name is unsupported: {name!r}.")
        if name in seen_passes:
            raise PresetError("PRESET_FIELD_INVALID", f"Preset pass {name} is duplicated.")
        if not isinstance(required, bool):
            raise PresetError("PRESET_FIELD_INVALID", f"preset.passes[{index}].required must be boolean.")
        if pass_image_format is not None and pass_image_format not in SUPPORTED_IMAGE_FORMATS:
            raise PresetError(
                "PRESET_FIELD_INVALID",
                f"preset.passes[{index}].image_format must be one of {', '.join(SUPPORTED_IMAGE_FORMATS)}.",
            )
        seen_passes.add(name)
        normalized_item = {"name": name, "required": required}
        if pass_image_format is not None:
            normalized_item["image_format"] = pass_image_format
        normalized_passes.append(normalized_item)

    output = data.get("output")
    if not isinstance(output, dict):
        raise PresetError("PRESET_FIELD_INVALID", "preset.output must be an object.")
    _expect_keys(output, {"image_format"}, {"image_format"}, "preset.output")
    image_format = output.get("image_format")
    if image_format not in SUPPORTED_IMAGE_FORMATS:
        raise PresetError(
            "PRESET_FIELD_INVALID",
            f"preset.output.image_format must be one of {', '.join(SUPPORTED_IMAGE_FORMATS)}.",
        )

    versioning = data.get("versioning")
    if not isinstance(versioning, dict):
        raise PresetError("PRESET_FIELD_INVALID", "preset.versioning must be an object.")
    _expect_keys(versioning, {"prefix", "padding"}, {"prefix", "padding"}, "preset.versioning")
    prefix = versioning.get("prefix")
    padding = versioning.get("padding")
    if not isinstance(prefix, str) or not _VERSION_PREFIX_RE.fullmatch(prefix):
        raise PresetError("PRESET_FIELD_INVALID", "preset.versioning.prefix must be 1-8 safe characters.")
    if not isinstance(padding, int) or isinstance(padding, bool) or padding < 1 or padding > 6:
        raise PresetError("PRESET_FIELD_INVALID", "preset.versioning.padding must be an integer from 1 to 6.")

    return {
        "schema": PRESET_SCHEMA,
        "schema_version": PRESET_SCHEMA_VERSION,
        "id": preset_id,
        "name": preset_name.strip(),
        "naming": normalized_naming,
        "folders": normalized_folders,
        "passes": normalized_passes,
        "output": {"image_format": image_format},
        "versioning": {"prefix": prefix, "padding": padding},
    }


def _load_preset_file_uncached(preset_path: Path) -> dict:
    try:
        if not preset_path.is_file():
            raise PresetError("PRESET_FILE_UNAVAILABLE", f"Studio preset file does not exist: {preset_path}")
        size = preset_path.stat().st_size
    except OSError as exc:
        raise PresetError("PRESET_FILE_UNAVAILABLE", f"Studio preset file cannot be inspected: {exc}") from exc

    if size > MAX_PRESET_BYTES:
        raise PresetError(
            "PRESET_FILE_TOO_LARGE",
            f"Studio preset file exceeds the {MAX_PRESET_BYTES}-byte safety limit.",
        )

    try:
        text = preset_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PresetError("PRESET_FILE_UNAVAILABLE", f"Studio preset file cannot be read as UTF-8: {exc}") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise PresetError("PRESET_JSON_INVALID", f"Studio preset is not valid JSON: {exc.msg} at line {exc.lineno}.") from exc
    return validate_preset(data)


def load_preset_file(path: str | Path) -> dict:
    """Load one bounded UTF-8 JSON file, honoring an explicit build snapshot."""
    preset_path = Path(path)
    key = str(preset_path)
    snapshot = _ACTIVE_FILE_SNAPSHOTS.get(key)
    if snapshot is not None:
        return copy.deepcopy(snapshot)
    return _load_preset_file_uncached(preset_path)


@contextmanager
def use_preset_file_snapshot(path: str | Path, preset: dict):
    """Freeze one validated custom preset for the duration of a package build.

    Validation can happen before this context. Once Build Package starts, every
    subsequent load of that same resolved file path receives the same normalized
    data, preventing a mid-build file edit from changing output mapping versus
    the generated manifest.
    """
    key = str(Path(path))
    previous = _ACTIVE_FILE_SNAPSHOTS.get(key)
    _ACTIVE_FILE_SNAPSHOTS[key] = copy.deepcopy(validate_preset(preset))
    try:
        yield copy.deepcopy(_ACTIVE_FILE_SNAPSHOTS[key])
    finally:
        if previous is None:
            _ACTIVE_FILE_SNAPSHOTS.pop(key, None)
        else:
            _ACTIVE_FILE_SNAPSHOTS[key] = previous


def version_token_for(preset: dict, version: int) -> str:
    versioning = preset["versioning"]
    return f"{versioning['prefix']}{int(version):0{int(versioning['padding'])}d}"


def format_template(preset: dict, key: str, values: dict[str, str]) -> str:
    template = preset["naming"][key]
    try:
        return template.format(**values)
    except (KeyError, ValueError) as exc:
        raise PresetError("PRESET_FIELD_INVALID", f"Preset naming template {key!r} could not be resolved: {exc}") from exc


def preset_metadata(mode: str, preset: dict) -> dict:
    return {
        "mode": str(mode).lower(),
        "schema": PRESET_SCHEMA,
        "schema_version": PRESET_SCHEMA_VERSION,
        "id": preset["id"],
        "name": preset["name"],
    }
