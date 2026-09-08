"""Temporary bounded patch helper for Issue #21. Delete after the repair commit is verified."""
from pathlib import Path

path = Path("apps/after-effects/CutBridge.jsx")
text = path.read_text(encoding="utf-8")

helper_anchor = """    function isInteger(value) { return isFiniteNumber(value) && Math.floor(value) === value && Math.abs(value) <= 9007199254740991; }

    function validateFrames(frames) {"""
helper_replacement = r'''    function isInteger(value) { return isFiniteNumber(value) && Math.floor(value) === value && Math.abs(value) <= 9007199254740991; }

    function safePackageToken(value, fallback) {
        var token = String(value || "").replace(/^\s+|\s+$/g, "");
        token = token.replace(/[<>:"\/\\|?*]+/g, "_");
        token = token.replace(/\s+/g, "_");
        return token || fallback;
    }
    function expectedPackageName(manifest) {
        return [
            safePackageToken(manifest.project, "PROJECT"),
            safePackageToken(manifest.episode, "EP00"),
            safePackageToken(manifest.scene, "SC000"),
            safePackageToken(manifest.cut, "C000"),
            safePackageToken(manifest.take, "T01"),
            "V" + zeroPad(manifest.version, 3)
        ].join("_");
    }

    function validateFrames(frames) {'''

validation_anchor = """        var strings = ["cutbridge_version", "project", "episode", "scene", "cut", "take"];
        for (var n = 0; n < strings.length; n++) if (typeof manifest[strings[n]] !== "string") errors.push("Manifest " + strings[n] + " must be a string.");
        if (!isInteger(manifest.version) || manifest.version < 1) errors.push("Manifest version must be a positive integer.");
        var frameError = validateFrames(manifest.frames); if (frameError) errors.push(frameError);"""
validation_replacement = '''        var strings = ["cutbridge_version", "project", "episode", "scene", "cut", "take"];
        var identityFieldsValid = true;
        for (var n = 0; n < strings.length; n++) {
            if (typeof manifest[strings[n]] !== "string") {
                errors.push("Manifest " + strings[n] + " must be a string.");
                if (strings[n] !== "cutbridge_version") identityFieldsValid = false;
            }
        }
        var versionValid = isInteger(manifest.version) && manifest.version >= 1;
        if (!versionValid) errors.push("Manifest version must be a positive integer.");
        if (manifest.package_name !== undefined) {
            if (typeof manifest.package_name !== "string") errors.push("Manifest package_name must be a string when provided.");
            else if (identityFieldsValid && versionValid && manifest.package_name !== expectedPackageName(manifest)) {
                errors.push("Manifest package_name does not match Project/Episode/Scene/Cut/Take/version identity.");
            }
        }
        var frameError = validateFrames(manifest.frames); if (frameError) errors.push(frameError);'''

if text.count(helper_anchor) != 1:
    raise SystemExit(f"helper anchor count was {text.count(helper_anchor)}, expected 1")
if text.count(validation_anchor) != 1:
    raise SystemExit(f"validation anchor count was {text.count(validation_anchor)}, expected 1")

text = text.replace(helper_anchor, helper_replacement, 1)
text = text.replace(validation_anchor, validation_replacement, 1)
path.write_text(text, encoding="utf-8")
