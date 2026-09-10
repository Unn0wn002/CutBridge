/*
CutBridge After Effects
- Reads and validates cutbridge.json schema/version
- Creates deterministic AE folders + comp
- Imports complete required image sequences from manifest
- Skips unavailable optional passes with warnings
- Reuses only validated CutBridge-managed comp/footage/layers on repeated builds
- QC validates exact manifest frame coverage, comp metadata, duration and FPS

Install/test:
File > Scripts > Run Script File... > CutBridge.jsx
For a dockable panel, place this file in After Effects/Scripts/ScriptUI Panels and restart AE.
*/

var CutBridgeContract = (function () {
    var PRODUCT_VERSION = "0.2.3";
    var SCHEMA = "cutbridge-manifest";
    var SCHEMA_VERSION = 1;
    var MANAGED_PREFIX = "CUTBRIDGE|1|";

    function zeroPad(n, width) {
        var s = String(n);
        while (s.length < width) s = "0" + s;
        return s;
    }

    function parseJSON(text) {
        if (typeof JSON !== "undefined" && JSON.parse) return JSON.parse(text);
        var pos = 0;
        function fail() { throw new Error("Invalid JSON at character " + pos + "."); }
        function white() { while (/[ \t\r\n]/.test(text.charAt(pos)) && pos < text.length) pos++; }
        function string() {
            var out = "";
            if (text.charAt(pos++) !== '"') fail();
            while (pos < text.length) {
                var ch = text.charAt(pos++);
                if (ch === '"') return out;
                if (ch === "\\") {
                    ch = text.charAt(pos++);
                    var escapes = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"};
                    if (ch === "u") {
                        var hex = text.substr(pos, 4);
                        if (!/^[0-9a-fA-F]{4}$/.test(hex)) fail();
                        out += String.fromCharCode(parseInt(hex, 16)); pos += 4;
                    } else if (Object.prototype.hasOwnProperty.call(escapes, ch)) out += escapes[ch];
                    else fail();
                } else {
                    if (ch.charCodeAt(0) < 32) fail();
                    out += ch;
                }
            }
            fail();
        }
        function value(depth) {
            if (depth > 100) fail();
            white();
            var ch = text.charAt(pos), result, key;
            if (ch === '"') return string();
            if (ch === "[" || ch === "{") {
                var array = ch === "[", close = array ? "]" : "}";
                result = array ? [] : {}; pos++; white();
                if (text.charAt(pos) === close) { pos++; return result; }
                while (pos < text.length) {
                    white();
                    if (array) result.push(value(depth + 1));
                    else {
                        key = string(); white();
                        if (text.charAt(pos++) !== ":") fail();
                        if (key === "__proto__") fail();
                        result[key] = value(depth + 1);
                    }
                    white(); ch = text.charAt(pos++);
                    if (ch === close) return result;
                    if (ch !== ",") fail();
                }
                fail();
            }
            var tail = text.slice(pos);
            var token = /^(true|false|null|-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?)/.exec(tail);
            if (!token) fail();
            pos += token[0].length;
            if (token[0] === "true") return true;
            if (token[0] === "false") return false;
            if (token[0] === "null") return null;
            return Number(token[0]);
        }
        if (typeof text !== "string") throw new Error("JSON input must be text.");
        var parsed = value(0); white();
        if (pos !== text.length) fail();
        return parsed;
    }

    function isArray(value) { return Object.prototype.toString.call(value) === "[object Array]"; }
    function isFiniteNumber(value) { return typeof value === "number" && isFinite(value); }
    function isInteger(value) { return isFiniteNumber(value) && Math.floor(value) === value && Math.abs(value) <= 9007199254740991; }

    // Python str.strip()/re \s use this set, independent of the JS host version.
    // In particular U+001C..001F/U+0085 are whitespace; U+FEFF/U+180E are not.
    var PYTHON_WHITESPACE = "[\\u0009-\\u000d\\u001c-\\u0020\\u0085\\u00a0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000]";
    var PYTHON_WHITESPACE_EDGES = new RegExp("^" + PYTHON_WHITESPACE + "+|" + PYTHON_WHITESPACE + "+$", "g");
    var PYTHON_WHITESPACE_RUNS = new RegExp(PYTHON_WHITESPACE + "+", "g");
    function trimPythonWhitespace(value) {
        return value.replace(PYTHON_WHITESPACE_EDGES, "");
    }
    function safePackageToken(value, fallback) {
        var token = trimPythonWhitespace(String(value || ""));
        token = token.replace(/[<>:"\/\\|?*]+/g, "_");
        token = token.replace(PYTHON_WHITESPACE_RUNS, "_");
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

    function validateFrames(frames) {
        if (!frames || !isInteger(frames.start) || !isInteger(frames.end) || !isInteger(frames.count)) {
            return "Manifest frames.start/end/count must be finite, exactly representable integers.";
        }
        if (frames.start < 0 || frames.end < 0) {
            return "Negative export frames are unsupported. Rebase the cut and preroll to frame 0 or later, then rebuild the package.";
        }
        if (frames.end < frames.start || frames.count < 1 || frames.count !== frames.end - frames.start + 1) {
            return "Manifest frame range/count is inconsistent; count must equal end - start + 1.";
        }
        return null;
    }

    function relativePassPath(path) {
        if (typeof path !== "string" || !path.length) throw new Error("Pass path must be a non-empty package-relative path.");
        var normalized = path.replace(/\\/g, "/");
        if (/^[\/~]/.test(normalized) || /[:%\x00-\x1f\x7f<>"|?*]/.test(normalized)) {
            throw new Error("Pass path must stay inside the package; absolute, URI and unsafe paths are not allowed.");
        }
        var parts = normalized.split("/");
        for (var i = 0; i < parts.length; i++) {
            if (!parts[i].length || parts[i] === "." || parts[i] === ".." || /[ .]$/.test(parts[i])) {
                throw new Error("Pass path must stay inside the package; empty, dot or traversal segments are not allowed.");
            }
        }
        return normalized;
    }

    function pathIsInside(root, candidate) {
        root = root.replace(/\\/g, "/").replace(/\/+$/, "");
        candidate = candidate.replace(/\\/g, "/");
        if (/^[A-Za-z]:/.test(root) || root.indexOf("//") === 0) { root = root.toLowerCase(); candidate = candidate.toLowerCase(); }
        return candidate.indexOf(root + "/") === 0;
    }

    function normalizedFsPath(value) {
        var result = String(value || "").replace(/\\/g, "/").replace(/\/+$/, "");
        if (/^[A-Za-z]:/.test(result) || result.indexOf("//") === 0) result = result.toLowerCase();
        return result;
    }
    function sameFilesystemPath(left, right) {
        return normalizedFsPath(left) === normalizedFsPath(right);
    }
    function escapeRegex(text) { return text.replace(/([.*+?^${}()|\[\]\\])/g, "\\$1"); }
    function validatePattern(pattern) {
        if (typeof pattern !== "string" || !pattern.length || /[\/\\:%\x00-\x1f\x7f<>"|?*]/.test(pattern) || /[ .]$/.test(pattern)) {
            throw new Error("Sequence pattern must be a safe filename, without directories or URI escapes.");
        }
        var first = pattern.indexOf("####");
        if (first < 0 || pattern.replace("####", "").indexOf("#") >= 0) throw new Error("Sequence pattern must contain exactly one #### frame token.");
    }
    function patternToRegex(pattern) { validatePattern(pattern); return new RegExp("^" + escapeRegex(pattern).replace("####", "(-?\\d+)") + "$", "i"); }
    function expectedFrameName(pattern, frame) {
        validatePattern(pattern);
        if (!isInteger(frame) || frame < 0) throw new Error("Export frame must be a non-negative finite integer.");
        return pattern.replace("####", zeroPad(frame, 4));
    }

    function passNames(manifest) {
        var result = [], seen = {};
        if (manifest.ae && isArray(manifest.ae.layer_order)) {
            for (var i = 0; i < manifest.ae.layer_order.length; i++) {
                var ordered = manifest.ae.layer_order[i];
                var orderedKey = "$" + ordered;
                if (!seen[orderedKey]) { result.push(ordered); seen[orderedKey] = true; }
            }
        }
        for (var j = 0; j < manifest.passes.length; j++) {
            var name = manifest.passes[j].name;
            var nameKey = "$" + name;
            if (!seen[nameKey]) { result.push(name); seen[nameKey] = true; }
        }
        return result;
    }

    function managedIdentity(manifest) {
        if (manifest.package_name) return String(manifest.package_name);
        return [manifest.project, manifest.episode, manifest.scene, manifest.cut, manifest.take, "V" + String(manifest.version)].join("|");
    }
    function managedTag(kind, manifest, name) {
        return MANAGED_PREFIX + kind + "|" + managedIdentity(manifest) + "|" + String(name || "");
    }
    function expectedCompSpec(manifest) {
        return {width: manifest.resolution.width, height: manifest.resolution.height,
            pixelAspect: manifest.resolution.pixel_aspect || 1.0, duration: manifest.frames.count / manifest.fps, frameRate: manifest.fps};
    }
    function compSpecErrors(expected, actual) {
        var errors = [];
        if (actual.width !== expected.width || actual.height !== expected.height) errors.push("resolution");
        if (Math.abs(actual.pixelAspect - expected.pixelAspect) > 0.000001) errors.push("pixel aspect");
        if (Math.abs(actual.frameRate - expected.frameRate) > 0.001) errors.push("frame rate");
        if (Math.abs(actual.duration - expected.duration) >= (1.0 / expected.frameRate)) errors.push("duration");
        return errors;
    }
    function footageReuseErrors(expected, actual) {
        var errors = [];
        if (!actual || actual.isFootage !== true) errors.push("item type");
        if (!actual || !actual.path || !sameFilesystemPath(expected.path, actual.path)) errors.push("source path");
        if (!actual || !isFiniteNumber(actual.conformFrameRate) || actual.conformFrameRate <= 0 || Math.abs(actual.conformFrameRate - expected.frameRate) > 0.001) errors.push("frame rate");
        return errors;
    }

    function validateManifest(manifest) {
        var errors = [];
        if (!manifest || typeof manifest !== "object" || isArray(manifest)) return ["Manifest is empty or invalid JSON data."];
        if (manifest.schema !== SCHEMA) errors.push("Unsupported manifest schema: " + String(manifest.schema));
        if (manifest.schema_version !== SCHEMA_VERSION) errors.push("Unsupported manifest schema_version " + String(manifest.schema_version) + "; CutBridge AE supports " + String(SCHEMA_VERSION) + ".");
        var strings = ["cutbridge_version", "project", "episode", "scene", "cut", "take"];
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
        var frameError = validateFrames(manifest.frames); if (frameError) errors.push(frameError);
        if (!isFiniteNumber(manifest.fps) || manifest.fps <= 0) errors.push("Manifest FPS must be a finite number greater than zero.");
        var r = manifest.resolution;
        if (!r || !isInteger(r.width) || r.width < 1 || !isInteger(r.height) || r.height < 1) errors.push("Manifest resolution width/height must be positive integers.");
        if (r && r.pixel_aspect !== undefined && (!isFiniteNumber(r.pixel_aspect) || r.pixel_aspect <= 0)) errors.push("Manifest resolution pixel_aspect must be a finite number greater than zero.");
        if (!isArray(manifest.passes) || manifest.passes.length === 0) errors.push("Manifest contains no render passes.");
        else {
            var seenPass = {};
            for (var i = 0; i < manifest.passes.length; i++) {
                var p = manifest.passes[i];
                if (!p || typeof p.name !== "string" || !p.name.length) { errors.push("Manifest pass at index " + i + " needs a non-empty name."); continue; }
                var passKey = "$" + p.name;
                if (seenPass[passKey]) errors.push("Manifest contains duplicate render pass name: " + p.name + ".");
                seenPass[passKey] = true;
                try { relativePassPath(p.path); } catch (pathError) { errors.push(p.name + ": " + pathError.message); }
                try { patternToRegex(p.sequence_pattern); } catch (patternError) { errors.push(p.name + ": " + patternError.message); }
                if (p.required !== undefined && typeof p.required !== "boolean") errors.push(p.name + ": required must be a boolean.");
            }
            if (manifest.ae && manifest.ae.layer_order !== undefined) {
                if (!isArray(manifest.ae.layer_order)) errors.push("Manifest ae.layer_order must be an array when provided.");
                else {
                    var seenOrder = {};
                    for (var q = 0; q < manifest.ae.layer_order.length; q++) {
                        var orderedName = manifest.ae.layer_order[q];
                        var orderKey = "$" + orderedName;
                        if (typeof orderedName !== "string" || !seenPass[orderKey]) errors.push("Manifest ae.layer_order references an unknown pass at index " + q + ".");
                        else if (seenOrder[orderKey]) errors.push("Manifest ae.layer_order contains duplicate pass: " + orderedName + ".");
                        seenOrder[orderKey] = true;
                    }
                }
            }
        }
        if (manifest.handoff_3d !== undefined) {
            var handoffErrors = validateHandoff3D(manifest.handoff_3d, manifest.frames);
            for (var he = 0; he < handoffErrors.length; he++) errors.push(handoffErrors[he]);
        }
        return errors;
    }

    function validateHandoff3D(handoff, frames) {
        var errors = [];
        if (!handoff || typeof handoff !== "object" || isArray(handoff)) return ["Manifest handoff_3d must be an object."];
        if (handoff.schema !== "cutbridge-handoff-3d") errors.push("Unsupported handoff_3d schema: " + String(handoff.schema));
        if (handoff.schema_version !== 1) errors.push("Unsupported handoff_3d schema_version " + String(handoff.schema_version) + "; CutBridge AE supports 1.");

        var s = handoff.space;
        if (!s || typeof s !== "object" || isArray(s)) {
            errors.push("handoff_3d space specification missing.");
        } else {
            if (s.coordinate_system !== "after-effects-composition") errors.push("Unsupported handoff_3d coordinate_system: " + String(s.coordinate_system));
            if (s.axis_map !== "blender_xyz_to_ae_x_negz_y") errors.push("Unsupported handoff_3d axis_map: " + String(s.axis_map));
            if (s.origin !== "composition-center") errors.push("Unsupported handoff_3d origin: " + String(s.origin));
            if (s.position_units !== "pixels") errors.push("Unsupported handoff_3d position_units: " + String(s.position_units));
            if (s.pixels_per_blender_unit !== undefined && (!isFiniteNumber(s.pixels_per_blender_unit) || s.pixels_per_blender_unit <= 0)) {
                errors.push("handoff_3d pixels_per_blender_unit must be a positive finite number.");
            }
        }

        var sm = handoff.sampling;
        if (!sm || typeof sm !== "object" || isArray(sm)) {
            errors.push("handoff_3d sampling specification missing.");
        } else {
            if (sm.mode !== "baked-per-frame") errors.push("Unsupported handoff_3d sampling mode: " + String(sm.mode));
            if (!isInteger(sm.frame_start) || !isInteger(sm.frame_end) || !isInteger(sm.frame_step)) {
                errors.push("handoff_3d sampling frame_start/end/step must be integers.");
            } else if (sm.frame_end < sm.frame_start || sm.frame_step <= 0) {
                errors.push("handoff_3d sampling frame range/step is invalid.");
            }
        }

        if (handoff.camera !== undefined) {
            var c = handoff.camera;
            if (!c || typeof c !== "object" || isArray(c)) {
                errors.push("handoff_3d camera must be an object.");
            } else {
                if (typeof c.name !== "string" || !c.name.length) errors.push("handoff_3d camera must have a non-empty name.");
                if (c.type !== "PERSP") errors.push("Unsupported handoff_3d camera type: " + String(c.type));
                if (!isArray(c.samples) || c.samples.length === 0) {
                    errors.push("handoff_3d camera samples must be a non-empty array.");
                } else {
                    for (var cs = 0; cs < c.samples.length; cs++) {
                        var samp = c.samples[cs];
                        if (!samp || typeof samp !== "object" || isArray(samp)) {
                            errors.push("handoff_3d camera sample at index " + cs + " is invalid.");
                            break;
                        }
                        if (!isInteger(samp.frame)) { errors.push("handoff_3d camera sample " + cs + " frame must be an integer."); break; }
                        if (!isFiniteNumber(samp.time)) { errors.push("handoff_3d camera sample " + cs + " time must be a finite number."); break; }
                        if (!isArray(samp.position) || samp.position.length !== 3 || !isFiniteNumber(samp.position[0]) || !isFiniteNumber(samp.position[1]) || !isFiniteNumber(samp.position[2])) {
                            errors.push("handoff_3d camera sample " + cs + " position must be an array of 3 finite numbers.");
                            break;
                        }
                        if (!isFiniteNumber(samp.ae_zoom) || samp.ae_zoom <= 0) {
                            errors.push("handoff_3d camera sample " + cs + " ae_zoom must be a positive finite number.");
                            break;
                        }
                    }
                }
            }
        }

        if (handoff.nulls !== undefined) {
            if (!isArray(handoff.nulls)) {
                errors.push("handoff_3d nulls must be an array.");
            } else {
                var seenNull = {};
                for (var ni = 0; ni < handoff.nulls.length; ni++) {
                    var n = handoff.nulls[ni];
                    if (!n || typeof n !== "object" || isArray(n)) {
                        errors.push("handoff_3d null at index " + ni + " is invalid.");
                        continue;
                    }
                    if (typeof n.name !== "string" || !n.name.length) {
                        errors.push("handoff_3d null at index " + ni + " must have a non-empty name.");
                        continue;
                    }
                    var nullKey = "$" + n.name;
                    if (seenNull[nullKey]) errors.push("handoff_3d contains duplicate null name: " + n.name + ".");
                    seenNull[nullKey] = true;
                    if (n.source_type !== "EMPTY") errors.push("handoff_3d null " + n.name + " source_type must be EMPTY; got " + String(n.source_type));
                    if (!isArray(n.samples) || n.samples.length === 0) {
                        errors.push("handoff_3d null " + n.name + " samples must be a non-empty array.");
                    } else {
                        for (var ns = 0; ns < n.samples.length; ns++) {
                            var nsamp = n.samples[ns];
                            if (!nsamp || typeof nsamp !== "object" || isArray(nsamp)) {
                                errors.push("handoff_3d null " + n.name + " sample at index " + ns + " is invalid.");
                                break;
                            }
                            if (!isInteger(nsamp.frame)) { errors.push("handoff_3d null " + n.name + " sample " + ns + " frame must be an integer."); break; }
                            if (!isFiniteNumber(nsamp.time)) { errors.push("handoff_3d null " + n.name + " sample " + ns + " time must be a finite number."); break; }
                            if (!isArray(nsamp.position) || nsamp.position.length !== 3 || !isFiniteNumber(nsamp.position[0]) || !isFiniteNumber(nsamp.position[1]) || !isFiniteNumber(nsamp.position[2])) {
                                errors.push("handoff_3d null " + n.name + " sample " + ns + " position must be an array of 3 finite numbers.");
                                break;
                            }
                        }
                    }
                }
            }
        }
        return errors;
    }

    function sequenceCoverage(passInfo, manifest, fileNames) {
        var frameError = validateFrames(manifest.frames); if (frameError) throw new Error(frameError);
        var result = {complete: false, firstName: null, missing: [], unexpected: [], matching: []};
        var regex = patternToRegex(passInfo.sequence_pattern), exact = {}, expected = {}, i;
        for (i = 0; i < fileNames.length; i++) {
            var name = String(fileNames[i]);
            if (regex.exec(name)) { result.matching.push(name); exact[name.toLowerCase()] = name; }
        }
        for (var frame = manifest.frames.start; frame <= manifest.frames.end; frame++) {
            var expectedName = expectedFrameName(passInfo.sequence_pattern, frame);
            expected[expectedName.toLowerCase()] = true;
            if (!exact[expectedName.toLowerCase()]) result.missing.push(frame);
        }
        for (i = 0; i < result.matching.length; i++) if (!expected[result.matching[i].toLowerCase()]) result.unexpected.push(result.matching[i]);
        result.complete = result.missing.length === 0;
        if (result.complete) result.firstName = exact[expectedFrameName(passInfo.sequence_pattern, manifest.frames.start).toLowerCase()];
        return result;
    }

    return {parseJSON: parseJSON, zeroPad: zeroPad, trimPythonWhitespace: trimPythonWhitespace, PRODUCT_VERSION: PRODUCT_VERSION, relativePassPath: relativePassPath, pathIsInside: pathIsInside,
        SCHEMA: SCHEMA, SCHEMA_VERSION: SCHEMA_VERSION, validateManifest: validateManifest, validateHandoff3D: validateHandoff3D, patternToRegex: patternToRegex,
        expectedFrameName: expectedFrameName, sequenceCoverage: sequenceCoverage, managedIdentity: managedIdentity, managedTag: managedTag,
        expectedCompSpec: expectedCompSpec, compSpecErrors: compSpecErrors, passNames: passNames, sameFilesystemPath: sameFilesystemPath,
        footageReuseErrors: footageReuseErrors, isArray: isArray};
})();

if (typeof module !== "undefined" && module.exports) {
    module.exports = CutBridgeContract;
} else {
(function CutBridge(thisObj) {
    var state = {manifestFile: null, manifest: null, packageFolder: null, comp: null, imported: {}, layers: {}};
    var revisionManager = null;
    var qcPlus = null;
    var localization = null;
    var currentLocale = "EN";
    function isArray(value) { return Object.prototype.toString.call(value) === "[object Array]"; }
    function log(msg) { $.writeln("[CutBridge] " + msg); }
    function fallbackLocalization() {
        var locale = "EN", strings = {
            language_label: "UI Language", no_package: "No package loaded", import_package: "1. Import Package",
            build_comp: "2. Build Comp", run_qc: "3. Run QC", update_revision: "4. Update Revision",
            workflow_note: "v{version}: validated package -> idempotent comp -> QC",
            package_status: "{name} | {fps}fps | {frames}f", choose_manifest: "Choose CutBridge cutbridge.json",
            choose_revision: "Choose newer CutBridge cutbridge.json", revision_file_required: "Choose the cutbridge.json file from the newer package.",
            revision_confirm: "Update CutBridge revision to V{version}?", warnings: "Warnings:",
            revision_scope: "Only verified CutBridge-managed sources and metadata will be changed.",
            revision_updated: "CutBridge: revision updated to V{version}.", revision_preserved: "Managed layer properties and artist layers were preserved.",
            confirmation_unavailable: "After Effects confirmation UI is unavailable; revision was not applied.",
            comp_built: "CutBridge: comp built", comp_reused: "CutBridge: comp reused safely",
            rollback_created: "Newly created managed objects were rolled back."
        };
        function format(value, values) {
            var out = String(value), key; values = values || {};
            for (key in values) if (Object.prototype.hasOwnProperty.call(values, key)) out = out.replace(new RegExp("\\{" + key + "\\}", "g"), String(values[key]));
            return out;
        }
        return {
            DEFAULT_LOCALE: "EN", FALLBACK_LOCALE: "EN",
            normalizeLocale: function(value) { return "EN"; },
            tr: function(value, key, values) { return format(strings[key] || key, values); },
            setLocale: function(value) { locale = "EN"; return locale; },
            getLocale: function() { return locale; },
            formatError: function(value, detail) { return "CutBridge\n\n" + detail; },
            localizeRevisionReason: function(value, reason) { return String(reason); },
            formatRevisionBlocked: function(value, reasons) { return "CutBridge\n\nRevision blocked:\n- " + reasons.join("\n- "); },
            localizeRecords: function(value, records) { return records; },
            qcHeadline: function(value, headline) { return headline; },
            localizeRenderedQC: function(value, report) { return report; }
        };
    }
    function getLocalization() {
        if (localization) return localization;
        try {
            if (typeof CutBridgeLocalization !== "undefined") localization = CutBridgeLocalization;
            else if (typeof $ !== "undefined" && $.fileName) {
                var localizationFile = new File(new File($.fileName).parent.fsName + "/localization.js");
                if (localizationFile.exists) {
                    $.evalFile(localizationFile);
                    if (typeof CutBridgeLocalization !== "undefined") localization = CutBridgeLocalization;
                }
            }
        } catch (localizationError) { log("Localization unavailable; using English fallback: " + localizationError.toString()); }
        if (!localization || typeof localization.tr !== "function" || typeof localization.normalizeLocale !== "function" ||
            typeof localization.formatError !== "function" || typeof localization.localizeRecords !== "function" ||
            typeof localization.formatRevisionBlocked !== "function") {
            localization = fallbackLocalization();
        }
        return localization;
    }
    function loadLocalePreference() {
        var l10n = getLocalization(), locale = l10n.DEFAULT_LOCALE || "EN";
        try {
            if (typeof app !== "undefined" && app.settings && app.settings.haveSetting && app.settings.haveSetting("CutBridge", "ui_locale")) {
                locale = app.settings.getSetting("CutBridge", "ui_locale");
            }
        } catch (settingsError) { log("Locale preference read failed: " + settingsError.toString()); }
        currentLocale = l10n.setLocale ? l10n.setLocale(locale) : l10n.normalizeLocale(locale);
        return currentLocale;
    }
    function saveLocalePreference(locale) {
        var l10n = getLocalization();
        currentLocale = l10n.setLocale ? l10n.setLocale(locale) : l10n.normalizeLocale(locale);
        try {
            if (typeof app !== "undefined" && app.settings && app.settings.saveSetting) app.settings.saveSetting("CutBridge", "ui_locale", currentLocale);
        } catch (settingsError) { log("Locale preference write failed: " + settingsError.toString()); }
        return currentLocale;
    }
    function tr(key, values) { return getLocalization().tr(currentLocale, key, values || {}); }
    function alertError(msg) { alert(getLocalization().formatError(currentLocale, msg)); }
    function readTextFile(file) { file.encoding = "UTF-8"; if (!file.open("r")) throw new Error("Could not open: " + file.fsName); var text = file.read(); file.close(); return text; }

    function loadManifest(fileOrPath) {
        var f = (fileOrPath && typeof fileOrPath === "object" && typeof fileOrPath.read === "function") ? fileOrPath : new File(fileOrPath);
        if (typeof f.exists !== "undefined" && !f.exists && typeof fileOrPath === "string") throw new Error("Manifest file does not exist: " + (f.fsName || f.name));
        var obj = CutBridgeContract.parseJSON(readTextFile(f));
        var contractErrors = CutBridgeContract.validateManifest(obj);
        if (contractErrors.length) throw new Error("Manifest contract rejected:\n- " + contractErrors.join("\n- "));
        state.manifestFile = f; state.manifest = obj; state.packageFolder = f.parent; state.imported = {}; state.layers = {}; state.comp = null;
        return obj;
    }
    function chooseManifest() {
        var f = File.openDialog(tr("choose_manifest"), "JSON:*.json");
        if (!f) return null;
        return loadManifest(f);
    }
    function ensureManifestLoaded() { if (state.manifest) return true; try { return !!chooseManifest(); } catch (e) { alertError(e.toString()); return false; } }

    function findChildFolder(parent, name) {
        for (var i = 1; i <= app.project.numItems; i++) { var item = app.project.item(i); if (item instanceof FolderItem && item.name === name && item.parentFolder === parent) return item; }
        var folder = app.project.items.addFolder(name); folder.parentFolder = parent; return folder;
    }
    function findExistingChildFolder(parent, name) {
        if (!parent) return null;
        for (var i = 1; i <= app.project.numItems; i++) { var item = app.project.item(i); if (item instanceof FolderItem && item.name === name && item.parentFolder === parent) return item; }
        return null;
    }
    function ensureProjectFolders(manifest) {
        var rootName = manifest.package_name || (manifest.project + "_" + manifest.cut), root = null, rootCount = 0;
        for (var i = 1; i <= app.project.numItems; i++) {
            var rootCandidate = app.project.item(i);
            if (rootCandidate instanceof FolderItem && rootCandidate.parentFolder === app.project.rootFolder && rootCandidate.name === rootName) {
                rootCount++; if (!root) root = rootCandidate;
            }
        }
        if (rootCount > 1) throw new Error("Multiple project-root folders named '" + rootName + "' exist; package ownership is ambiguous. Resolve the duplicate roots before Build. CutBridge will not modify either root.");
        if (root) {
            var managedNames = ["01_COMP", "02_RENDER", "03_PRECOMP", "04_OUTPUT"], childCounts = {}, c;
            for (c = 0; c < managedNames.length; c++) childCounts[managedNames[c]] = 0;
            for (i = 1; i <= app.project.numItems; i++) {
                var childCandidate = app.project.item(i);
                if (!(childCandidate instanceof FolderItem) || childCandidate.parentFolder !== root) continue;
                for (c = 0; c < managedNames.length; c++) if (childCandidate.name === managedNames[c]) childCounts[managedNames[c]]++;
            }
            for (c = 0; c < managedNames.length; c++) {
                if (childCounts[managedNames[c]] !== 1) throw new Error("Managed child folder '" + managedNames[c] + "' must exist exactly once inside '" + rootName + "'. Resolve missing/duplicate folder drift before Build; CutBridge will not create, choose, or modify managed folders inside an existing package root.");
            }
            var compName = (manifest.ae && manifest.ae.comp_name) ? manifest.ae.comp_name : (manifest.cut + "_COMP");
            var compFolder = findExistingChildFolder(root, "01_COMP"), expectedCompTag = CutBridgeContract.managedTag("comp", manifest, compName), taggedCompItems = 0, ownedCompItems = 0;
            for (i = 1; i <= app.project.numItems; i++) {
                var item = app.project.item(i);
                if (itemComment(item) !== expectedCompTag) continue;
                taggedCompItems++;
                if (typeof CompItem !== "undefined" && item instanceof CompItem && item.parentFolder === compFolder && item.name === compName) ownedCompItems++;
            }
            if (!compFolder || taggedCompItems !== 1 || ownedCompItems !== 1) throw new Error("A project-root folder named '" + rootName + "' exists but is not uniquely verified as this CutBridge package. Preserve that folder; resolve missing/duplicate/misplaced managed-comp ownership, rename or move the conflicting root, or build this package in a clean project. CutBridge will not adopt or modify it.");
        } else {
            root = app.project.items.addFolder(rootName); root.parentFolder = app.project.rootFolder;
        }
        return {root: root, comp: findChildFolder(root, "01_COMP"), render: findChildFolder(root, "02_RENDER"), precomp: findChildFolder(root, "03_PRECOMP"), output: findChildFolder(root, "04_OUTPUT")};
    }
    function existingProjectFolders(manifest) {
        var rootName = manifest.package_name || (manifest.project + "_" + manifest.cut), root = findExistingChildFolder(app.project.rootFolder, rootName);
        if (!root) return null;
        return uniqueExistingProjectFolders(manifest);
    }
    function uniqueExistingProjectFolders(manifest) {
        var rootName = manifest.package_name || (manifest.project + "_" + manifest.cut), root = null, rootCount = 0, i;
        for (i = 1; i <= app.project.numItems; i++) {
            var rootCandidate = app.project.item(i);
            if (rootCandidate instanceof FolderItem && rootCandidate.parentFolder === app.project.rootFolder && rootCandidate.name === rootName) {
                rootCount++; if (!root) root = rootCandidate;
            }
        }
        if (rootCount !== 1) throw new Error("Current CutBridge package root '" + rootName + "' must exist exactly once. Resolve missing/duplicate roots; CutBridge will not choose or create one.");
        var names = ["01_COMP", "02_RENDER", "03_PRECOMP", "04_OUTPUT"], keys = ["comp", "render", "precomp", "output"], result = {root: root};
        for (var n = 0; n < names.length; n++) {
            var found = null, count = 0;
            for (i = 1; i <= app.project.numItems; i++) {
                var child = app.project.item(i);
                if (child instanceof FolderItem && child.parentFolder === root && child.name === names[n]) { count++; if (!found) found = child; }
            }
            if (count !== 1) throw new Error("Current CutBridge managed folder '" + names[n] + "' must exist exactly once. Resolve missing/duplicate folder drift; CutBridge will not choose or create one.");
            result[keys[n]] = found;
        }
        return result;
    }
    function itemComment(item) { try { return item.comment || ""; } catch (e) { return ""; } }
    function isAnyManagedTag(comment) { return typeof comment === "string" && comment.indexOf("CUTBRIDGE|1|") === 0; }
    function setItemComment(item, value) { try { item.comment = value; } catch (e) { throw new Error("After Effects item comments are required for safe CutBridge managed-object tracking."); } }
    function findTaggedProjectItem(parentFolder, tag) {
        for (var i = 1; i <= app.project.numItems; i++) { var item = app.project.item(i); if (item.parentFolder === parentFolder && itemComment(item) === tag) return item; }
        return null;
    }
    function findNamedComp(parentFolder, name) {
        for (var i = 1; i <= app.project.numItems; i++) { var item = app.project.item(i); if (item instanceof CompItem && item.parentFolder === parentFolder && item.name === name) return item; }
        return null;
    }

    function listSequenceFileNames(passInfo) {
        var relative = CutBridgeContract.relativePassPath(passInfo.path), parts = relative.split("/"), dir = state.packageFolder;
        for (var p = 0; p < parts.length; p++) { dir = new Folder(dir.fsName + "/" + parts[p]); if (dir.alias || !CutBridgeContract.pathIsInside(state.packageFolder.fsName, dir.fsName)) throw new Error(passInfo.name + ": pass folder must stay inside the package; aliases are not supported."); }
        if (!dir.exists) return {dir: dir, names: []};
        var regex = CutBridgeContract.patternToRegex(passInfo.sequence_pattern);
        var files = dir.getFiles(function(f) { return f instanceof File && regex.test(File.decode(f.name)); }), names = [];
        for (var i = 0; files && i < files.length; i++) { if (files[i].alias || !CutBridgeContract.pathIsInside(dir.fsName, files[i].fsName)) throw new Error(passInfo.name + ": sequence files must stay inside the pass folder; aliases are not supported."); names.push(File.decode(files[i].name)); }
        return {dir: dir, names: names};
    }
    function listSequenceFileNamesAtRoot(passInfo, packageRoot) {
        var relative = CutBridgeContract.relativePassPath(passInfo.path), parts = relative.split("/"), dir = packageRoot;
        for (var p = 0; p < parts.length; p++) {
            dir = new Folder(dir.fsName + "/" + parts[p]);
            if (dir.alias || !CutBridgeContract.pathIsInside(packageRoot.fsName, dir.fsName)) throw new Error(passInfo.name + ": pass folder must stay inside the candidate package; aliases are not supported.");
        }
        if (!dir.exists) return {dir: dir, names: []};
        var regex = CutBridgeContract.patternToRegex(passInfo.sequence_pattern);
        var files = dir.getFiles(function(f) { return f instanceof File && regex.test(File.decode(f.name)); }), names = [];
        for (var i = 0; files && i < files.length; i++) {
            if (files[i].alias || !CutBridgeContract.pathIsInside(dir.fsName, files[i].fsName)) throw new Error(passInfo.name + ": candidate sequence files must stay inside the pass folder; aliases are not supported.");
            names.push(File.decode(files[i].name));
        }
        return {dir: dir, names: names};
    }
    function inspectSequence(passInfo, manifest) { var listing = listSequenceFileNames(passInfo); var coverage = CutBridgeContract.sequenceCoverage(passInfo, manifest, listing.names); coverage.folderExists = listing.dir.exists; coverage.dir = listing.dir; return coverage; }
    function inspectSequenceAtRoot(passInfo, manifest, packageRoot) { var listing = listSequenceFileNamesAtRoot(passInfo, packageRoot); var coverage = CutBridgeContract.sequenceCoverage(passInfo, manifest, listing.names); coverage.folderExists = listing.dir.exists; coverage.dir = listing.dir; return coverage; }
    function formatMissingFrames(frames) { if (!frames.length) return ""; var shown = frames.slice(0, 12).join(", "); if (frames.length > 12) shown += " … +" + (frames.length - 12) + " more"; return shown; }

    function preflightSequences(manifest) {
        var result = {entries: [], warnings: []};
        for (var i = 0; i < manifest.passes.length; i++) {
            var passInfo = manifest.passes[i], coverage = inspectSequence(passInfo, manifest);
            if (!coverage.folderExists || !coverage.complete) {
                var reason = !coverage.folderExists ? "pass folder missing" : ("missing frame(s): " + formatMissingFrames(coverage.missing));
                if (passInfo.required === false) { result.warnings.push(passInfo.name + ": optional pass skipped — " + reason); result.entries.push({passInfo: passInfo, coverage: coverage, skip: true}); continue; }
                throw new Error(passInfo.name + ": required pass cannot be imported — " + reason);
            }
            if (coverage.unexpected.length) result.warnings.push(passInfo.name + ": unexpected matching filename(s): " + coverage.unexpected.join(", "));
            result.entries.push({passInfo: passInfo, coverage: coverage, skip: false});
        }
        return result;
    }

    function expectedFirstFile(passInfo, coverage) {
        var firstFile = new File(coverage.dir.fsName + "/" + coverage.firstName);
        if (firstFile.alias || !CutBridgeContract.pathIsInside(coverage.dir.fsName, firstFile.fsName)) throw new Error(passInfo.name + ": unsafe first-frame path.");
        if (!firstFile.exists) throw new Error(passInfo.name + ": expected first frame is missing: " + coverage.firstName);
        return firstFile;
    }
    function validateReusableFootage(existing, firstFile, passInfo, manifest, renderFolder) {
        var isFootage = typeof FootageItem !== "undefined" && existing instanceof FootageItem;
        var sourcePath = null, conformFrameRate = null;
        try { if (existing.file && existing.file.fsName) sourcePath = existing.file.fsName; } catch (e) {}
        try { if (existing.mainSource && typeof existing.mainSource.conformFrameRate !== "undefined") conformFrameRate = existing.mainSource.conformFrameRate; } catch (e2) {}
        var mismatches = CutBridgeContract.footageReuseErrors(
            {path: firstFile.fsName, frameRate: manifest.fps},
            {isFootage: isFootage, path: sourcePath, conformFrameRate: conformFrameRate}
        );
        if (itemComment(existing) !== CutBridgeContract.managedTag("footage", manifest, passInfo.name)) mismatches.push("managed ownership tag");
        if (!renderFolder || existing.parentFolder !== renderFolder) mismatches.push("managed render folder ownership");
        if (mismatches.length) throw new Error(passInfo.name + ": managed footage no longer matches the package (" + mismatches.join(", ") + "). Preserve the existing project. Restore the intended source/FPS/tag/folder only if appropriate, or build in a clean project; S5 will not silently replace or reclaim it.");
        return existing;
    }
    // Caches are observations only. Always resolve live project membership before reuse.
    function findManagedFootage(passInfo, manifest, renderFolder, firstFile) {
        var tag = CutBridgeContract.managedTag("footage", manifest, passInfo.name), cached = state.imported[tag], found = null;
        delete state.imported[tag];
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i), comment = itemComment(item), path = null;
            if (comment === tag) {
                if (found) throw new Error(passInfo.name + ": duplicate managed footage ownership. Preserve the project and resolve the duplicate tags before retrying.");
                found = validateReusableFootage(item, firstFile, passInfo, manifest, renderFolder);
            } else if (!isAnyManagedTag(comment)) {
                try { if (item.file) path = item.file.fsName; } catch (pathError) {}
                // A matching source or generated name is a collision signal, never ownership proof.
                if ((path && CutBridgeContract.sameFilesystemPath(path, firstFile.fsName)) ||
                    (item.parentFolder === renderFolder && item.name === manifest.cut + "_" + passInfo.name)) {
                    throw new Error(passInfo.name + ": ambiguous footage ownership: an unverified item uses the expected source or managed name. Preserve artist work; restore the original managed tag/folder only if intended, or remove the conflicting item from this project before retrying. CutBridge will not adopt it or import a duplicate.");
                }
            }
        }
        if (cached && liveProjectItem(cached) && cached !== found) throw new Error(passInfo.name + ": cached managed footage no longer proves ownership; preserve the existing project and restore the intended tag/source/folder before retrying. CutBridge will not import a replacement over a live user-modified object.");
        if (found) state.imported[tag] = found;
        return found;
    }

    function liveProjectItem(target) {
        if (!target || !app.project) return false;
        for (var i = 1; i <= app.project.numItems; i++) if (app.project.item(i) === target) return true;
        return false;
    }

    function existingRenderFolder(manifest) {
        var rootName = manifest.package_name || (manifest.project + "_" + manifest.cut);
        for (var i = 1; app.project && i <= app.project.numItems; i++) {
            var item = app.project.item(i), parent = item.parentFolder;
            if (item instanceof FolderItem && item.name === "02_RENDER" && parent instanceof FolderItem &&
                parent.name === rootName && parent.parentFolder === app.project.rootFolder) return item;
        }
        return null;
    }

    function conformAndVerifyImportedFootage(footage, firstFile, passInfo, manifest) {
        if (typeof FootageItem === "undefined" || !(footage instanceof FootageItem) || !footage.mainSource) {
            throw new Error(passInfo.name + ": imported item is not verifiable footage; build stopped before creating a managed layer.");
        }
        try {
            footage.mainSource.conformFrameRate = manifest.fps;
        } catch (setError) {
            throw new Error(passInfo.name + ": After Effects could not conform imported footage to " + manifest.fps + " fps (" + setError.toString() + "). Build stopped; verify the source sequence and AE footage interpretation before retrying.");
        }
        var actualRate;
        try {
            if (typeof footage.mainSource.conformFrameRate === "undefined") throw new Error("conformFrameRate is unavailable");
            actualRate = footage.mainSource.conformFrameRate;
        } catch (readError) {
            throw new Error(passInfo.name + ": CutBridge could not verify the imported footage frame rate after conforming it (" + readError.toString() + "). Build stopped before creating a managed layer.");
        }
        var sourcePath = null;
        try { if (footage.file && footage.file.fsName) sourcePath = footage.file.fsName; } catch (pathError) {}
        var mismatches = CutBridgeContract.footageReuseErrors(
            {path: firstFile.fsName, frameRate: manifest.fps},
            {isFootage: true, path: sourcePath, conformFrameRate: actualRate}
        );
        if (actualRate === null || actualRate === undefined || mismatches.length) {
            throw new Error(passInfo.name + ": imported footage timing/source could not be verified (" + (mismatches.length ? mismatches.join(", ") : "frame rate unavailable") + "). Build stopped before creating a managed layer.");
        }
        return footage;
    }

    function importSequence(passInfo, manifest, renderFolder, coverage, createdFootage) {
        var tag = CutBridgeContract.managedTag("footage", manifest, passInfo.name);
        var firstFile = expectedFirstFile(passInfo, coverage);
        var existing = findManagedFootage(passInfo, manifest, renderFolder, firstFile);
        if (existing) return existing;
        var io = new ImportOptions(firstFile); if (io.canImportAs && io.canImportAs(ImportAsType.FOOTAGE)) io.importAs = ImportAsType.FOOTAGE;
        io.sequence = true; io.forceAlphabetical = false;
        var footage = app.project.importFile(io);
        try {
            footage.name = manifest.cut + "_" + passInfo.name; footage.parentFolder = renderFolder;
            conformAndVerifyImportedFootage(footage, firstFile, passInfo, manifest);
            setItemComment(footage, tag);
            state.imported[tag] = footage;
            if (createdFootage) createdFootage.push({item: footage, tag: tag});
            return footage;
        } catch (importError) {
            try {
                if (!footage || typeof footage.remove !== "function") throw new Error("newly imported footage cannot be removed by this AE host");
                footage.remove();
            } catch (rollbackError) {
                throw new Error(passInfo.name + ": import verification failed and CutBridge could not roll back the newly imported footage (" + rollbackError.toString() + "). Use Undo for the CutBridge Build Comp operation before retrying. Original error: " + importError.toString());
            }
            throw importError;
        }
    }

    function findManagedComp(manifest, compFolder, compName) {
        var tag = CutBridgeContract.managedTag("comp", manifest, compName), found = null;
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (itemComment(item) !== tag) continue;
            if (found) throw new Error("Duplicate managed comp ownership for " + compName + "; resolve duplicate tags before retrying.");
            if (typeof CompItem === "undefined" || !(item instanceof CompItem)) throw new Error("Managed comp tag collision for " + compName + "; the tagged item is not a composition.");
            if (!compFolder || item.parentFolder !== compFolder) throw new Error("Managed comp ownership no longer belongs to the expected comp folder. Preserve the project and restore the intended folder before retrying.");
            if (item.name !== compName) throw new Error("Managed comp name no longer matches the package identity. Preserve the project and restore the intended comp name before retrying.");
            found = item;
        }
        return found;
    }
    function ensureManagedComp(manifest, compFolder, compName) {
        var tag = CutBridgeContract.managedTag("comp", manifest, compName), expected = CutBridgeContract.expectedCompSpec(manifest);
        var comp = findManagedComp(manifest, compFolder, compName);
        if (!comp) {
            var collision = findNamedComp(compFolder, compName);
            if (collision) throw new Error("A non-CutBridge comp named '" + compName + "' already exists in the managed folder. Rename or move it before building to avoid modifying manual work.");
            comp = app.project.items.addComp(compName, expected.width, expected.height, expected.pixelAspect, expected.duration, expected.frameRate);
            try {
                comp.parentFolder = compFolder;
                setItemComment(comp, tag);
            } catch (creationError) {
                try {
                    if (!comp || typeof comp.remove !== "function") throw new Error("newly created managed comp cannot be removed by this AE host");
                    comp.remove();
                } catch (rollbackError) {
                    throw new Error("Managed comp initialization failed and CutBridge could not roll back the newly created comp (" + rollbackError.toString() + "). Use Undo for the CutBridge Build Comp operation before retrying. Original error: " + creationError.toString());
                }
                throw new Error("Managed comp initialization failed and the newly created comp was rolled back (" + creationError.toString() + "). After Effects item comments are required for safe CutBridge idempotency.");
            }
            return {comp: comp, created: true};
        }
        var mismatches = CutBridgeContract.compSpecErrors(expected, {width: comp.width, height: comp.height, pixelAspect: comp.pixelAspect, duration: comp.duration, frameRate: comp.frameRate});
        if (mismatches.length) throw new Error("Managed comp metadata no longer matches the package (" + mismatches.join(", ") + "). Preserve manual work and rebuild into a clean package/comp instead of silently rewriting it.");
        return {comp: comp, created: false};
    }

    function findManagedLayer(comp, tag, footage, passName) {
        var cached = state.layers[tag];
        delete state.layers[tag];
        var found = null;
        // Scan project comps as well, so a moved tagged layer blocks after script reload too.
        for (var p = 1; p <= app.project.numItems; p++) {
            var owner = app.project.item(p);
            if (!(owner instanceof CompItem)) continue;
            for (var i = 1; i <= owner.numLayers; i++) {
                var layer = owner.layer(i), comment = itemComment(layer);
                if (comment === tag) {
                    if (found) throw new Error("Duplicate managed layer ownership; resolve duplicate tags before retrying.");
                    if (owner !== comp || typeof AVLayer === "undefined" || !(layer instanceof AVLayer) || layer.containingComp !== comp) {
                        throw new Error("Managed layer ownership no longer belongs to a valid footage layer in the expected comp. Preserve artist work and restore the intended tag/container before retrying.");
                    }
                    if (footage) {
                        var liveSource;
                        try { liveSource = layer.source; }
                        catch (liveSourceError) { throw new Error("Managed layer source cannot be read; preserve artist work and restore the intended managed layer before retrying."); }
                        if (!liveSource || liveSource !== footage) throw new Error("Managed layer does not point to the expected footage; preserve artist work and restore the intended managed layer before retrying.");
                    }
                    found = layer;
                } else if (owner === comp && ((passName && layer.name === passName) || (footage && layer.source === footage))) {
                    throw new Error("Ambiguous managed layer ownership: an unverified layer uses the expected pass name or footage. Preserve artist work; restore its original tag only if intended, or move/remove the conflicting layer before retrying. CutBridge will not adopt it or add a duplicate.");
                }
            }
        }
        if (cached && liveProjectLayer(cached) && cached !== found) throw new Error("Cached managed layer no longer proves ownership; preserve the existing project and restore the intended tag/source/container before retrying. CutBridge will not add a replacement over a live user-modified layer.");
        if (found) state.layers[tag] = found;
        return found;
    }
    function liveProjectLayer(target) {
        if (!target || !app.project) return false;
        for (var p = 1; p <= app.project.numItems; p++) {
            var owner = app.project.item(p);
            if (!(owner instanceof CompItem)) continue;
            for (var i = 1; i <= owner.numLayers; i++) if (owner.layer(i) === target) return true;
        }
        return false;
    }
    function ensureManagedLayer(comp, footage, manifest, passName) {
        var tag = CutBridgeContract.managedTag("layer", manifest, passName), layer = findManagedLayer(comp, tag, footage, passName);
        if (layer) {
            var source;
            try { source = layer.source; }
            catch (sourceError) { throw new Error(passName + ": managed layer source cannot be read; refusing destructive replacement in S5."); }
            if (!source || source !== footage) throw new Error(passName + ": managed layer does not point to the expected footage; refusing destructive replacement in S5.");
            state.layers[tag] = layer;
            return {layer: layer, created: false};
        }
        layer = comp.layers.add(footage);
        try {
            layer.name = passName;
            layer.startTime = 0;
            layer.comment = tag;
        } catch (creationError) {
            try {
                if (!layer || typeof layer.remove !== "function") throw new Error("newly created managed layer cannot be removed by this AE host");
                layer.remove();
            } catch (rollbackError) {
                throw new Error(passName + ": managed layer initialization failed and CutBridge could not roll back the newly created layer (" + rollbackError.toString() + "). Use Undo for the CutBridge Build Comp operation before retrying. Original error: " + creationError.toString());
            }
            throw new Error(passName + ": managed layer initialization failed and the newly created layer was rolled back (" + creationError.toString() + "). After Effects layer comments are required for safe CutBridge idempotency.");
        }
        state.layers[tag] = layer; return {layer: layer, created: true};
    }

    function isManagedLayerTagForManifest(comment, manifest) {
        for (var i = 0; i < manifest.passes.length; i++) if (comment === CutBridgeContract.managedTag("layer", manifest, manifest.passes[i].name)) return true;
        if (manifest.handoff_3d) {
            if (manifest.handoff_3d.camera && manifest.handoff_3d.camera.name && comment === CutBridgeContract.managedTag("camera", manifest, manifest.handoff_3d.camera.name)) return true;
            if (manifest.handoff_3d.nulls && isArray(manifest.handoff_3d.nulls)) {
                for (var n = 0; n < manifest.handoff_3d.nulls.length; n++) {
                    if (manifest.handoff_3d.nulls[n] && manifest.handoff_3d.nulls[n].name && comment === CutBridgeContract.managedTag("null", manifest, manifest.handoff_3d.nulls[n].name)) return true;
                }
            }
        }
        return false;
    }

    function findManagedCamera(comp, manifest, camData) {
        var tag = CutBridgeContract.managedTag("camera", manifest, camData.name), cached = state.layers[tag], found = null;
        delete state.layers[tag];
        for (var p = 1; p <= app.project.numItems; p++) {
            var owner = app.project.item(p);
            if (!(owner instanceof CompItem)) continue;
            for (var i = 1; i <= owner.numLayers; i++) {
                var layer = owner.layer(i), comment = itemComment(layer);
                if (comment === tag) {
                    if (found) throw new Error(camData.name + ": duplicate managed camera ownership; resolve duplicate tags before retrying.");
                    if (owner !== comp || (typeof CameraLayer !== "undefined" && !(layer instanceof CameraLayer)) || layer.containingComp !== comp) {
                        throw new Error(camData.name + ": managed camera ownership no longer belongs to a valid camera layer in the expected comp. Preserve artist work and restore the intended tag/container before retrying.");
                    }
                    found = layer;
                } else if (owner === comp && layer.name === camData.name && !isAnyManagedTag(comment)) {
                    throw new Error(camData.name + ": ambiguous managed camera ownership: an unverified layer uses the expected camera name. Preserve artist work; restore its original tag only if intended, or move/remove the conflicting layer before retrying. CutBridge will not adopt it or add a duplicate.");
                }
            }
        }
        if (cached && liveProjectLayer(cached) && cached !== found) {
            throw new Error(camData.name + ": cached managed camera no longer proves ownership; preserve the existing project and restore the intended tag before retrying.");
        }
        if (found) state.layers[tag] = found;
        return found;
    }

    function ensureManagedCamera(comp, manifest, camData) {
        var tag = CutBridgeContract.managedTag("camera", manifest, camData.name);
        var layer = findManagedCamera(comp, manifest, camData);
        if (layer) return {layer: layer, created: false};
        layer = comp.layers.addCamera(camData.name, [comp.width / 2, comp.height / 2]);
        try {
            layer.name = camData.name;
            layer.startTime = 0;
            layer.comment = tag;
        } catch (creationError) {
            try {
                if (!layer || typeof layer.remove !== "function") throw new Error("newly created managed camera cannot be removed by this AE host");
                layer.remove();
            } catch (rollbackError) {
                throw new Error(camData.name + ": managed camera initialization failed and CutBridge could not roll back the newly created camera (" + rollbackError.toString() + "). Original error: " + creationError.toString());
            }
            throw new Error(camData.name + ": managed camera initialization failed and the newly created camera was rolled back (" + creationError.toString() + ").");
        }
        state.layers[tag] = layer;
        return {layer: layer, created: true};
    }

    function findManagedNull(comp, manifest, nullData) {
        var tag = CutBridgeContract.managedTag("null", manifest, nullData.name), cached = state.layers[tag], found = null;
        delete state.layers[tag];
        for (var p = 1; p <= app.project.numItems; p++) {
            var owner = app.project.item(p);
            if (!(owner instanceof CompItem)) continue;
            for (var i = 1; i <= owner.numLayers; i++) {
                var layer = owner.layer(i), comment = itemComment(layer);
                if (comment === tag) {
                    if (found) throw new Error(nullData.name + ": duplicate managed null ownership; resolve duplicate tags before retrying.");
                    if (owner !== comp || layer.containingComp !== comp || !layer.threeDLayer) {
                        throw new Error(nullData.name + ": managed null ownership no longer belongs to a valid 3D layer in the expected comp. Preserve artist work and restore the intended tag/container before retrying.");
                    }
                    found = layer;
                } else if (owner === comp && layer.name === nullData.name && !isAnyManagedTag(comment)) {
                    throw new Error(nullData.name + ": ambiguous managed null ownership: an unverified layer uses the expected null name. Preserve artist work; restore its original tag only if intended, or move/remove the conflicting layer before retrying. CutBridge will not adopt it or add a duplicate.");
                }
            }
        }
        if (cached && liveProjectLayer(cached) && cached !== found) {
            throw new Error(nullData.name + ": cached managed null no longer proves ownership; preserve the existing project and restore the intended tag before retrying.");
        }
        if (found) state.layers[tag] = found;
        return found;
    }

    function ensureManagedNull(comp, manifest, nullData) {
        var tag = CutBridgeContract.managedTag("null", manifest, nullData.name);
        var layer = findManagedNull(comp, manifest, nullData);
        if (layer) return {layer: layer, created: false};
        layer = comp.layers.addNull(comp.duration);
        try {
            layer.name = nullData.name;
            layer.threeDLayer = true;
            layer.startTime = 0;
            layer.comment = tag;
        } catch (creationError) {
            try {
                if (!layer || typeof layer.remove !== "function") throw new Error("newly created managed null cannot be removed by this AE host");
                layer.remove();
            } catch (rollbackError) {
                throw new Error(nullData.name + ": managed null initialization failed and CutBridge could not roll back the newly created null (" + rollbackError.toString() + "). Original error: " + creationError.toString());
            }
            throw new Error(nullData.name + ": managed null initialization failed and the newly created null was rolled back (" + creationError.toString() + ").");
        }
        state.layers[tag] = layer;
        return {layer: layer, created: true};
    }

    function clearPropertyKeyframes(prop) {
        if (!prop) return;
        try {
            if (prop.numKeys && prop.numKeys > 0) {
                for (var k = prop.numKeys; k >= 1; k--) {
                    prop.removeKey(k);
                }
            }
        } catch (_e) {}
    }

    function applyCameraSamples(camera, camData, manifest) {
        var transform = camera.property ? camera.property("ADBE Transform Group") : null;
        var posProp = transform ? transform.property("ADBE Position") : camera.position;
        var poiProp = transform ? transform.property("ADBE Anchor Point") : null;
        if (!poiProp && transform) poiProp = transform.property("Point of Interest");
        if (!poiProp) poiProp = camera.pointOfInterest;
        var cameraOptions = camera.property ? camera.property("ADBE Camera Options Group") : null;
        var zoomProp = cameraOptions ? cameraOptions.property("ADBE Camera Zoom") : (camera.cameraOption ? camera.cameraOption.zoom : null);

        if (!posProp || !poiProp || !zoomProp) {
            throw new Error("Camera Position, Point of Interest, or Zoom property unavailable.");
        }

        clearPropertyKeyframes(posProp);
        clearPropertyKeyframes(poiProp);
        clearPropertyKeyframes(zoomProp);

        var samples = camData.samples;
        for (var i = 0; i < samples.length; i++) {
            var s = samples[i];
            var t = s.time;
            var fwd = s.forward || [0, 0, 1];
            var poi = [
                s.position[0] + fwd[0] * 1000.0,
                s.position[1] + fwd[1] * 1000.0,
                s.position[2] + fwd[2] * 1000.0
            ];
            if (samples.length === 1) {
                if (posProp.setValue) posProp.setValue(s.position);
                if (poiProp.setValue) poiProp.setValue(poi);
                if (zoomProp.setValue) zoomProp.setValue(s.ae_zoom);
            } else {
                if (posProp.setValueAtTime) posProp.setValueAtTime(t, s.position);
                else if (posProp.setValue) posProp.setValue(s.position);
                if (poiProp.setValueAtTime) poiProp.setValueAtTime(t, poi);
                else if (poiProp.setValue) poiProp.setValue(poi);
                if (zoomProp.setValueAtTime) zoomProp.setValueAtTime(t, s.ae_zoom);
                else if (zoomProp.setValue) zoomProp.setValue(s.ae_zoom);
            }
        }
    }

    function applyNullSamples(nullLayer, nullData, manifest) {
        var transform = nullLayer.property ? nullLayer.property("ADBE Transform Group") : null;
        var posProp = transform ? transform.property("ADBE Position") : nullLayer.position;
        var scaleProp = transform ? transform.property("ADBE Scale") : nullLayer.scale;

        if (!posProp) {
            throw new Error("Null Position property unavailable.");
        }

        clearPropertyKeyframes(posProp);
        if (scaleProp) clearPropertyKeyframes(scaleProp);

        var samples = nullData.samples;
        for (var i = 0; i < samples.length; i++) {
            var s = samples[i];
            var t = s.time;
            if (samples.length === 1) {
                if (posProp.setValue) posProp.setValue(s.position);
                if (scaleProp && s.scale && isArray(s.scale) && s.scale.length === 3) {
                    if (scaleProp.setValue) scaleProp.setValue([s.scale[0] * 100, s.scale[1] * 100, s.scale[2] * 100]);
                }
            } else {
                if (posProp.setValueAtTime) posProp.setValueAtTime(t, s.position);
                else if (posProp.setValue) posProp.setValue(s.position);
                if (scaleProp && s.scale && isArray(s.scale) && s.scale.length === 3) {
                    if (scaleProp.setValueAtTime) scaleProp.setValueAtTime(t, [s.scale[0] * 100, s.scale[1] * 100, s.scale[2] * 100]);
                    else if (scaleProp.setValue) scaleProp.setValue([s.scale[0] * 100, s.scale[1] * 100, s.scale[2] * 100]);
                }
            }
        }
    }

    function preflightExistingManagedLayers(comp, manifest, entries, renderFolder) {
        if (!comp || !comp.numLayers) return;
        var hasUnverifiedLayer = false;
        for (var i = 1; i <= comp.numLayers; i++) {
            var layerComment = itemComment(comp.layer(i));
            if (isAnyManagedTag(layerComment) && !isManagedLayerTagForManifest(layerComment, manifest)) {
                throw new Error("Managed layer ownership is ambiguous because the active comp contains a stale or foreign CutBridge-managed layer. Preserve artist work and restore or remove the stale managed-layer tag before retrying; CutBridge will not reuse or mutate this comp.");
            }
            if (!isManagedLayerTagForManifest(layerComment, manifest)) hasUnverifiedLayer = true;
        }
        for (var j = 0; j < entries.length; j++) {
            var entry = entries[j]; if (entry.skip) continue;
            var passInfo = entry.passInfo, tag = CutBridgeContract.managedTag("layer", manifest, passInfo.name), layer = findManagedLayer(comp, tag, null, passInfo.name);
            if (layer) {
                var source;
                try { source = layer.source; } catch (sourceError) { throw new Error(passInfo.name + ": managed layer source cannot be read before import; preserve artist work and restore the intended managed layer before retrying."); }
                if (!source) throw new Error(passInfo.name + ": managed layer has no readable footage source; preserve artist work and restore the intended managed layer before retrying.");
                validateReusableFootage(source, expectedFirstFile(passInfo, entry.coverage), passInfo, manifest, renderFolder);
            } else if (hasUnverifiedLayer) {
                throw new Error(passInfo.name + ": managed layer ownership is ambiguous because the existing comp contains an unverified layer. Preserve artist work and restore the intended managed layer tag before retrying; CutBridge will not add a replacement over it.");
            }
        }
        if (manifest.handoff_3d) {
            if (manifest.handoff_3d.camera) {
                var camData = manifest.handoff_3d.camera;
                var camLayer = findManagedCamera(comp, manifest, camData);
                if (!camLayer && hasUnverifiedLayer) {
                    throw new Error(camData.name + ": managed camera ownership is ambiguous because the existing comp contains an unverified layer. Preserve artist work and restore the intended managed camera tag before retrying; CutBridge will not add a replacement over it.");
                }
            }
            if (manifest.handoff_3d.nulls && isArray(manifest.handoff_3d.nulls)) {
                for (var ni = 0; ni < manifest.handoff_3d.nulls.length; ni++) {
                    var nData = manifest.handoff_3d.nulls[ni];
                    var nullLayer = findManagedNull(comp, manifest, nData);
                    if (!nullLayer && hasUnverifiedLayer) {
                        throw new Error(nData.name + ": managed null ownership is ambiguous because the existing comp contains an unverified layer. Preserve artist work and restore the intended managed null tag before retrying; CutBridge will not add a replacement over it.");
                    }
                }
            }
        }
    }
    function rollbackNewBuildObjects(createdLayers, createdFootage) {
        var failures = [], i, record;
        for (i = createdLayers.length - 1; i >= 0; i--) {
            record = createdLayers[i];
            try {
                if (!record.layer || typeof record.layer.remove !== "function") throw new Error("newly created managed layer cannot be removed by this AE host");
                record.layer.remove(); delete state.layers[record.tag];
            } catch (layerError) { failures.push("layer rollback failed: " + layerError.toString()); }
        }
        for (i = createdFootage.length - 1; i >= 0; i--) {
            record = createdFootage[i];
            try {
                if (!record.item || typeof record.item.remove !== "function") throw new Error("newly imported footage cannot be removed by this AE host");
                record.item.remove(); delete state.imported[record.tag];
            } catch (footageError) { failures.push("footage rollback failed: " + footageError.toString()); }
        }
        return failures;
    }

    function findVerifiedPass(passName, verifiedPasses) {
        for (var i = 0; verifiedPasses && i < verifiedPasses.length; i++) if (verifiedPasses[i].name === passName) return verifiedPasses[i];
        return null;
    }
    function orderManagedLayers(comp, manifest, verifiedPasses) {
        if (typeof comp.layer !== "function") return;
        var ordered = CutBridgeContract.passNames(manifest);
        var layers = [];
        for (var i = 0; i < ordered.length; i++) {
            var verified = findVerifiedPass(ordered[i], verifiedPasses);
            if (!verified) continue;
            var tag = CutBridgeContract.managedTag("layer", manifest, ordered[i]);
            var layer = findManagedLayer(comp, tag, verified.footage, ordered[i]);
            if (layer) layers.push(layer);
        }
        for (var j = layers.length - 1; j >= 0; j--) if (layers[j].moveToBeginning) layers[j].moveToBeginning();
    }

    function getQCPlus() {
        if (qcPlus) return qcPlus;
        if (typeof CutBridgeQCPlus !== "undefined") qcPlus = CutBridgeQCPlus;
        else {
            if (typeof $ === "undefined" || !$.fileName) throw new Error("CutBridge QC+ requires qc_plus.js beside CutBridge.jsx.");
            var scriptFile = new File(new File($.fileName).parent.fsName + "/qc_plus.js");
            if (!scriptFile.exists) throw new Error("CutBridge QC+ requires qc_plus.js beside CutBridge.jsx.");
            $.evalFile(scriptFile);
            if (typeof CutBridgeQCPlus === "undefined") throw new Error("CutBridge could not load qc_plus.js beside CutBridge.jsx.");
            qcPlus = CutBridgeQCPlus;
        }
        if (!qcPlus || typeof qcPlus.diagnostic !== "function" || typeof qcPlus.render !== "function" ||
            typeof qcPlus.sequenceRecords !== "function" || typeof qcPlus.compRecords !== "function" ||
            typeof qcPlus.managedObjectRecords !== "function" || typeof qcPlus.hostRecords !== "function") {
            throw new Error("CutBridge QC+ engine is invalid.");
        }
        return qcPlus;
    }

    function getRevisionManager() {
        if (revisionManager) return revisionManager;
        if (typeof CutBridgeRevisionManager !== "undefined") revisionManager = CutBridgeRevisionManager;
        else {
            if (typeof $ === "undefined" || !$.fileName) throw new Error("CutBridge revision support requires revision_manager.js beside CutBridge.jsx.");
            var scriptFile = new File(new File($.fileName).parent.fsName + "/revision_manager.js");
            if (!scriptFile.exists) throw new Error("CutBridge revision support requires revision_manager.js beside CutBridge.jsx.");
            $.evalFile(scriptFile);
            if (typeof CutBridgeRevisionManager === "undefined") throw new Error("CutBridge could not load the revision manager beside CutBridge.jsx.");
            revisionManager = CutBridgeRevisionManager;
        }
        if (!revisionManager || typeof revisionManager.createExecutor !== "function") throw new Error("CutBridge revision manager is invalid.");
        return revisionManager;
    }
    function passByName(manifest, name) {
        for (var i = 0; i < manifest.passes.length; i++) if (manifest.passes[i].name === name) return manifest.passes[i];
        return null;
    }
    function revisionFirstFile(passInfo, manifest, packageRoot) {
        var coverage = inspectSequenceAtRoot(passInfo, manifest, packageRoot);
        if (!coverage.folderExists || !coverage.complete) throw new Error(passInfo.name + ": candidate pass does not contain the complete required frame sequence.");
        var firstFile = new File(coverage.dir.fsName + "/" + coverage.firstName);
        if (firstFile.alias || !CutBridgeContract.pathIsInside(coverage.dir.fsName, firstFile.fsName) || !firstFile.exists) throw new Error(passInfo.name + ": candidate first-frame path is unsafe or missing.");
        return firstFile;
    }
    function makeRevisionAdapter(current, candidate, candidateRoot) {
        var folders = uniqueExistingProjectFolders(current), compName = (current.ae && current.ae.comp_name) ? current.ae.comp_name : (current.cut + "_COMP");
        if (!folders || !folders.root || !folders.comp || !folders.render) throw new Error("Current CutBridge package folders are missing; revision is blocked to protect the project.");
        var comp = findManagedComp(current, folders.comp, compName);
        if (!comp) throw new Error("Current managed comp is missing; revision is blocked to protect the project.");
        var mismatches = CutBridgeContract.compSpecErrors(CutBridgeContract.expectedCompSpec(current),
            {width: comp.width, height: comp.height, pixelAspect: comp.pixelAspect, duration: comp.duration, frameRate: comp.frameRate});
        if (mismatches.length) throw new Error("Current managed comp metadata drift blocks revision (" + mismatches.join(", ") + "). Preserve artist work and restore the intended comp before retrying.");
        // Revision must enforce the same persistent layer ownership gate as Build,
        // including orphan stale tags that do not collide by current name/source.
        preflightExistingManagedLayers(comp, current, preflightSequences(current).entries, folders.render);
        var journal = [], migration = null;
        function currentPass(name) { return passByName(current, name); }
        function candidatePass(name) { return passByName(candidate, name); }
        function liveLayer(layer) { return liveProjectLayer(layer); }
        function validateManagedLayer(layer, expected, passName, key) {
            try {
                var p = currentPass(passName), expectedTag = CutBridgeContract.managedTag("layer", expected, passName);
                if (!p || key !== getRevisionManager().ownershipKey(expected, passName) || !layer || !liveLayer(layer) ||
                    typeof AVLayer === "undefined" || !(layer instanceof AVLayer) || layer.containingComp !== comp ||
                    itemComment(layer) !== expectedTag || !layer.source || typeof FootageItem === "undefined" || !(layer.source instanceof FootageItem)) return false;
                var firstFile = revisionFirstFile(p, expected, state.packageFolder), source = layer.source;
                // Resolve globally rather than accepting a locally correct source whose
                // ownership tag is duplicated elsewhere in the project.
                return findManagedFootage(p, expected, folders.render, firstFile) === source;
            } catch (e) { return false; }
        }
        return {
            listManagedLayers: function() {
                var records = [];
                for (var i = 0; i < current.passes.length; i++) {
                    var p = current.passes[i], tag = CutBridgeContract.managedTag("layer", current, p.name), layer = findManagedLayer(comp, tag, null, p.name);
                    if (layer) records.push({layer: layer, passName: p.name});
                }
                return records;
            },
            validateManagedLayer: validateManagedLayer,
            readSource: function(layer) { if (!layer || !layer.source) throw new Error("Managed layer source is unavailable."); return layer.source; },
            importReplacement: function(manifest, passName, track) {
                var p = candidatePass(passName); if (!p) throw new Error(passName + ": candidate pass is unavailable.");
                var firstFile = revisionFirstFile(p, manifest, candidateRoot), io = new ImportOptions(firstFile);
                if (io.canImportAs && io.canImportAs(ImportAsType.FOOTAGE)) io.importAs = ImportAsType.FOOTAGE;
                io.sequence = true; io.forceAlphabetical = false;
                var footage = app.project.importFile(io);
                track(footage);
                footage.name = manifest.cut + "_" + passName + "_V" + CutBridgeContract.zeroPad(manifest.version, 3);
                footage.parentFolder = folders.render;
                conformAndVerifyImportedFootage(footage, firstFile, p, manifest);
                return footage;
            },
            validateReplacement: function(item, manifest, passName) {
                try {
                    var p = candidatePass(passName); if (!p || !item || !liveProjectItem(item) || typeof FootageItem === "undefined" || !(item instanceof FootageItem) || item.parentFolder !== folders.render) return false;
                    var firstFile = revisionFirstFile(p, manifest, candidateRoot), sourcePath = null, conformFrameRate = null;
                    try { if (item.file && item.file.fsName) sourcePath = item.file.fsName; } catch (pathError) {}
                    try { if (item.mainSource && typeof item.mainSource.conformFrameRate !== "undefined") conformFrameRate = item.mainSource.conformFrameRate; } catch (fpsError) {}
                    return CutBridgeContract.footageReuseErrors({path: firstFile.fsName, frameRate: manifest.fps}, {isFootage: true, path: sourcePath, conformFrameRate: conformFrameRate}).length === 0;
                } catch (e) { return false; }
            },
            swapManagedSource: function(layer, item, passName) {
                if (!layer || typeof layer.replaceSource !== "function") throw new Error("Managed layer source replacement is unavailable in this After Effects host.");
                var record = {layer: layer, oldSource: layer.source, replacement: item, passName: passName};
                journal.push(record);
                layer.replaceSource(item, false);
            },
            restoreManagedSource: function(layer, oldSource, passName) {
                var record = null;
                for (var i = journal.length - 1; i >= 0; i--) if (journal[i].layer === layer && journal[i].oldSource === oldSource) { record = journal[i]; break; }
                if (!layer) throw new Error("Managed layer is unavailable during source restoration.");
                if (layer.source !== oldSource) {
                    if (typeof layer.replaceSource !== "function") throw new Error("Managed layer source restoration is unavailable in this After Effects host.");
                    layer.replaceSource(oldSource, false);
                }
                if (migration) {
                    if (migration.migrateRootComment) setItemComment(folders.root, migration.rootComment);
                    folders.root.name = migration.rootName;
                    setItemComment(comp, migration.compComment);
                    for (var j = 0; j < migration.items.length; j++) {
                        var item = migration.items[j];
                        setItemComment(item.layer, item.layerComment);
                        setItemComment(item.oldSource, item.oldComment);
                        setItemComment(item.replacement, item.replacementComment);
                        delete state.layers[CutBridgeContract.managedTag("layer", candidate, item.passName)];
                        state.layers[CutBridgeContract.managedTag("layer", current, item.passName)] = item.layer;
                        delete state.imported[CutBridgeContract.managedTag("footage", candidate, item.passName)];
                        state.imported[CutBridgeContract.managedTag("footage", current, item.passName)] = item.oldSource;
                    }
                    migration = null;
                }
                if (record && state.imported[CutBridgeContract.managedTag("footage", candidate, record.passName)]) delete state.imported[CutBridgeContract.managedTag("footage", candidate, record.passName)];
            },
            removeImportedReplacement: function(item) {
                if (!item || !liveProjectItem(item) || typeof item.remove !== "function") return false;
                item.remove();
                return !liveProjectItem(item);
            },
            commitRevision: function(oldManifest, newManifest, replacements) {
                var targetName = newManifest.package_name || (newManifest.project + "_" + newManifest.cut), collision = findExistingChildFolder(app.project.rootFolder, targetName);
                if (collision && collision !== folders.root) throw new Error("The candidate package root already exists in this project; revision is ambiguous and was not applied.");
                var rootComment = itemComment(folders.root), currentRootTag = CutBridgeContract.managedTag("root", oldManifest, "PACKAGE");
                migration = {rootName: folders.root.name, rootComment: rootComment, migrateRootComment: rootComment === currentRootTag, compComment: itemComment(comp), items: []};
                for (var i = 0; i < journal.length; i++) migration.items.push({layer: journal[i].layer, oldSource: journal[i].oldSource, replacement: journal[i].replacement, passName: journal[i].passName, layerComment: itemComment(journal[i].layer), oldComment: itemComment(journal[i].oldSource), replacementComment: itemComment(journal[i].replacement)});
                for (i = 0; i < journal.length; i++) {
                    var item = migration.items[i], passName = item.passName;
                    if (!passName) throw new Error("Could not identify the managed pass during revision commit.");
                    item.passName = passName;
                    setItemComment(item.layer, CutBridgeContract.managedTag("layer", newManifest, passName));
                    // Preserve the retired source's old version-scoped CutBridge tag. Clearing it would
                    // convert historical CutBridge footage into an unmanaged S5 collision on later Build/QC.
                    setItemComment(item.oldSource, item.oldComment);
                    setItemComment(item.replacement, CutBridgeContract.managedTag("footage", newManifest, passName));
                    delete state.layers[CutBridgeContract.managedTag("layer", oldManifest, passName)];
                    delete state.imported[CutBridgeContract.managedTag("footage", oldManifest, passName)];
                    state.layers[CutBridgeContract.managedTag("layer", newManifest, passName)] = item.layer;
                    state.imported[CutBridgeContract.managedTag("footage", newManifest, passName)] = item.replacement;
                }
                folders.root.name = targetName;
                if (migration.migrateRootComment) setItemComment(folders.root, CutBridgeContract.managedTag("root", newManifest, "PACKAGE"));
                setItemComment(comp, CutBridgeContract.managedTag("comp", newManifest, comp.name));
                state.comp = comp;
            }
        };
    }
    function chooseRevisionPackage() {
        var file = File.openDialog(tr("choose_revision"), "JSON:*.json");
        if (!file) return null;
        if (String(file.name).toLowerCase() !== "cutbridge.json") throw new Error(tr("revision_file_required"));
        var candidate = CutBridgeContract.parseJSON(readTextFile(file)), errors = CutBridgeContract.validateManifest(candidate);
        if (errors.length) throw new Error("Candidate manifest contract rejected:\n- " + errors.join("\n- "));
        return {file: file, manifest: candidate, root: file.parent};
    }
    // S6 JSX-native pass-set guard: intentionally independent of revision_manager.js host binding.
    // This executes inside CutBridge.jsx before the revision confirmation UI can be reached.
    function directRevisionPassSetErrors(current, candidate) {
        var reasons = [], currentNames = {}, candidateNames = {}, i, p, key;
        if (!current || !candidate || !current.passes || !candidate.passes) {
            return ["Revision pass-set guard could not inspect the current/candidate manifests."];
        }
        for (i = 0; i < current.passes.length; i++) {
            p = current.passes[i];
            if (!p || typeof p.name !== "string") return ["Revision pass-set guard found an invalid current pass."];
            currentNames["$" + p.name] = p;
        }
        for (i = 0; i < candidate.passes.length; i++) {
            p = candidate.passes[i];
            if (!p || typeof p.name !== "string") return ["Revision pass-set guard found an invalid candidate pass."];
            candidateNames["$" + p.name] = p;
        }
        for (i = 0; i < current.passes.length; i++) {
            p = current.passes[i]; key = "$" + p.name;
            if (!candidateNames[key]) {
                if (p.required !== false) reasons.push("Previously required pass missing: " + p.name);
                else reasons.push("Removing an optional pass is unsupported by source-only revision: " + p.name + ". Rebuild or migrate the comp deliberately.");
            }
        }
        for (i = 0; i < candidate.passes.length; i++) {
            p = candidate.passes[i]; key = "$" + p.name;
            if (!currentNames[key]) reasons.push("Adding passes is unsupported by source-only revision: " + p.name);
        }
        return reasons;
    }
    function updateRevision() {
        if (!ensureManifestLoaded()) return;
        try {
            var selected = chooseRevisionPackage(); if (!selected) return;
            var passSetReasons = directRevisionPassSetErrors(state.manifest, selected.manifest), l10n = getLocalization();
            if (passSetReasons.length) { alert(l10n.formatRevisionBlocked(currentLocale, passSetReasons)); return; }
            var manager = getRevisionManager(), assessment = manager.assess(state.manifest, selected.manifest);
            if (assessment.status === "incompatible") { alert(l10n.formatRevisionBlocked(currentLocale, assessment.reasons)); return; }
            var adapter = makeRevisionAdapter(state.manifest, selected.manifest, selected.root), executor = manager.createExecutor(adapter), ticket = executor.prepare(state.manifest, selected.manifest);
            var revisionVersion = CutBridgeContract.zeroPad(selected.manifest.version, 3), localizedWarnings = [], wi;
            for (wi = 0; wi < ticket.warnings.length; wi++) localizedWarnings.push(l10n.localizeRevisionReason(currentLocale, ticket.warnings[wi]));
            var message = tr("revision_confirm", {version: revisionVersion}) + "\n\n" + (localizedWarnings.length ? tr("warnings") + "\n- " + localizedWarnings.join("\n- ") + "\n\n" : "") + tr("revision_scope");
            if (typeof confirm !== "function") throw new Error("After Effects confirmation UI is unavailable; revision was not applied.");
            if (!confirm(message)) return;
            app.beginUndoGroup("CutBridge Update Revision");
            try {
                executor.apply(ticket, true);
                state.manifestFile = selected.file; state.manifest = selected.manifest; state.packageFolder = selected.root;
                alert(tr("revision_updated", {version: CutBridgeContract.zeroPad(selected.manifest.version, 3)}) + "\n" + tr("revision_preserved"));
            } catch (applyError) { alertError(applyError.toString()); }
            finally { app.endUndoGroup(); }
        } catch (e) { alertError(e.toString()); }
    }

    function buildComp() {
        if (!ensureManifestLoaded()) return {success: false, error: "Manifest not loaded"};
        var m = state.manifest, preflight;
        try { preflight = preflightSequences(m); } catch (preflightError) { alertError(preflightError.toString()); return {success: false, error: preflightError.toString()}; }
        if (!app.project) app.newProject();
        var warnings = preflight.warnings.slice(0), compName = (m.ae && m.ae.comp_name) ? m.ae.comp_name : (m.cut + "_COMP");
        app.beginUndoGroup("CutBridge Build Comp");
        var createdFootage = [], createdLayers = [];
        try {
            var folders = ensureProjectFolders(m), compResult = ensureManagedComp(m, folders.comp, compName), comp = compResult.comp, verifiedPasses = []; state.comp = comp;
            if (!compResult.created) preflightExistingManagedLayers(comp, m, preflight.entries, folders.render);
            for (var i = 0; i < preflight.entries.length; i++) {
                var entry = preflight.entries[i]; if (entry.skip) continue;
                var footage = importSequence(entry.passInfo, m, folders.render, entry.coverage, createdFootage), layerResult = ensureManagedLayer(comp, footage, m, entry.passInfo.name);
                if (layerResult.created) createdLayers.push({layer: layerResult.layer, tag: CutBridgeContract.managedTag("layer", m, entry.passInfo.name)});
                verifiedPasses.push({name: entry.passInfo.name, footage: footage});
            }
            orderManagedLayers(comp, m, verifiedPasses);

            var managedNullLayers = [];
            if (m.handoff_3d && m.handoff_3d.nulls && isArray(m.handoff_3d.nulls)) {
                for (var ni = 0; ni < m.handoff_3d.nulls.length; ni++) {
                    var nData = m.handoff_3d.nulls[ni];
                    var nullRes = ensureManagedNull(comp, m, nData);
                    if (nullRes.created) createdLayers.push({layer: nullRes.layer, tag: CutBridgeContract.managedTag("null", m, nData.name)});
                    applyNullSamples(nullRes.layer, nData, m);
                    managedNullLayers.push(nullRes.layer);
                }
            }

            var managedCameraLayer = null;
            if (m.handoff_3d && m.handoff_3d.camera) {
                var camRes = ensureManagedCamera(comp, m, m.handoff_3d.camera);
                if (camRes.created) createdLayers.push({layer: camRes.layer, tag: CutBridgeContract.managedTag("camera", m, m.handoff_3d.camera.name)});
                applyCameraSamples(camRes.layer, m.handoff_3d.camera, m);
                managedCameraLayer = camRes.layer;
            }

            for (var nIdx = managedNullLayers.length - 1; nIdx >= 0; nIdx--) {
                if (managedNullLayers[nIdx].moveToBeginning) managedNullLayers[nIdx].moveToBeginning();
            }
            if (managedCameraLayer && managedCameraLayer.moveToBeginning) {
                managedCameraLayer.moveToBeginning();
            }

            comp.openInViewer();
            var message = tr(compResult.created ? "comp_built" : "comp_reused") + "\n" + comp.name + "\n" + m.resolution.width + "x" + m.resolution.height + " @ " + m.fps + " fps";
            if (warnings.length) message += "\n\n" + tr("warnings") + "\n- " + warnings.join("\n- ");
            alert(message);
            return {success: true, comp: comp, compResult: compResult, warnings: warnings};
        } catch (e) {
            var rollbackFailures = rollbackNewBuildObjects(createdLayers, createdFootage), errorMessage = e.toString();
            if (createdLayers.length || createdFootage.length) errorMessage += "\n" + tr("rollback_created");
            if (rollbackFailures.length) errorMessage += "\n" + rollbackFailures.join("\n");
            alertError(errorMessage);
            return {success: false, error: errorMessage, originalError: e};
        }
        finally { app.endUndoGroup(); }
    }

    function exactCurrentManagedOrphans(manifest) {
        var result = {footage: {}, layer: {}}, i, p, tag;
        for (i = 0; i < manifest.passes.length; i++) {
            result.footage["$" + manifest.passes[i].name] = 0;
            result.layer["$" + manifest.passes[i].name] = 0;
        }
        if (!app.project) return result;
        for (var itemIndex = 1; itemIndex <= app.project.numItems; itemIndex++) {
            var item = app.project.item(itemIndex), comment = itemComment(item);
            for (i = 0; i < manifest.passes.length; i++) {
                p = manifest.passes[i]; tag = "$" + p.name;
                if (comment === CutBridgeContract.managedTag("footage", manifest, p.name)) result.footage[tag]++;
            }
            if (typeof CompItem === "undefined" || !(item instanceof CompItem) || typeof item.layer !== "function") continue;
            for (var layerIndex = 1; layerIndex <= item.numLayers; layerIndex++) {
                var layerComment = itemComment(item.layer(layerIndex));
                for (i = 0; i < manifest.passes.length; i++) {
                    p = manifest.passes[i]; tag = "$" + p.name;
                    if (layerComment === CutBridgeContract.managedTag("layer", manifest, p.name)) result.layer[tag]++;
                }
            }
        }
        return result;
    }

    function runQC() {
        if (!ensureManifestLoaded()) return;
        var m = state.manifest, qc, records = [];
        function append(items) {
            for (var ai = 0; items && ai < items.length; ai++) records.push(items[ai]);
        }
        function add(spec) { records.push(qc.diagnostic(spec)); }
        function finish() {
            var l10n = getLocalization();
            records = l10n.localizeRecords(currentLocale, records);
            var report = qc.render(records);
            alert("CutBridge QC — " + l10n.qcHeadline(currentLocale, report.headline) + "\n\n" + l10n.localizeRenderedQC(currentLocale, report.text));
            return {records: records, report: report};
        }

        try { qc = getQCPlus(); }
        catch (qcLoadError) { alertError(qcLoadError.toString()); return {records: [], report: null, error: qcLoadError.toString()}; }

        var contractErrors = CutBridgeContract.validateManifest(m);
        if (contractErrors.length) {
            for (var ce = 0; ce < contractErrors.length; ce++) {
                add({severity: "ERROR", code: "CBQ-MANIFEST-CONTRACT-ERROR", scope: "manifest",
                    message: contractErrors[ce], remediation: "Repair or regenerate cutbridge.json from the trusted Blender package, then load it again before Build, Revision, or QC."});
            }
            return finish();
        }

        add({severity: "PASS", code: "CBQ-PACKAGE-IDENTITY-OK", scope: "package", subject: m.package_name || m.cut,
            message: "Package identity and manifest naming are valid."});
        add({severity: "PASS", code: "CBQ-MANIFEST-SCHEMA-OK", scope: "manifest",
            message: "Manifest schema " + CutBridgeContract.SCHEMA + " v" + CutBridgeContract.SCHEMA_VERSION + " is supported."});
        add({severity: "PASS", code: "CBQ-MANIFEST-FPS-OK", scope: "manifest", message: "FPS " + m.fps + " is valid."});
        add({severity: "PASS", code: "CBQ-MANIFEST-FRAMES-OK", scope: "manifest", message: "Frame count " + m.frames.count + " is internally consistent."});
        add({severity: "PASS", code: "CBQ-MANIFEST-RESOLUTION-OK", scope: "manifest", message: "Resolution " + m.resolution.width + "x" + m.resolution.height + " is valid."});

        if (!app.project) {
            append(qc.hostRecords({inspectable: false})); state.comp = null; return finish();
        }

        var projectFolders = null, folderLookupError = null;
        try { projectFolders = existingProjectFolders(m); }
        catch (folderError) { folderLookupError = folderError; }

        var managedCompFolder = projectFolders ? projectFolders.comp : null;
        var compName = (m.ae && m.ae.comp_name) ? m.ae.comp_name : (m.cut + "_COMP");
        var liveComp = null, compLookupError = null;
        // Even when the expected package root is absent, scan globally for the
        // exact managed-comp tag. A moved/tagged comp is ownership drift, not a
        // package-only state that QC may silently pass.
        try { liveComp = findManagedComp(m, managedCompFolder, compName); }
        catch (compError) { compLookupError = compError; }

        for (var i = 0; i < m.passes.length; i++) {
            var p = m.passes[i], coverage = null, managedFootage = null;
            try { coverage = inspectSequence(p, m); }
            catch (sequenceError) {
                add({severity: "ERROR", code: "CBQ-SEQ-INSPECTION-ERROR", scope: "sequence", subject: p.name,
                    message: "Sequence inspection failed — " + sequenceError.toString(),
                    remediation: "Verify the package-relative pass path, aliases, and sequence filenames. CutBridge will not follow unsafe paths or guess the intended source."});
                continue;
            }
            append(qc.sequenceRecords(p, m, coverage));
            if (!coverage.folderExists || !coverage.complete || !projectFolders) continue;

            if (!projectFolders.render) {
                add({severity: p.required === false ? "WARNING" : "ERROR", code: p.required === false ? "CBQ-FOOTAGE-OPTIONAL-MISSING" : "CBQ-FOOTAGE-REQUIRED-MISSING", scope: "footage", subject: p.name,
                    message: (p.required === false ? "optional" : "required") + " managed render folder is missing.",
                    remediation: "Restore the deterministic CutBridge package folders or rebuild/migrate deliberately; QC will not create or adopt folders automatically."});
                continue;
            }

            try {
                managedFootage = findManagedFootage(p, m, projectFolders.render, expectedFirstFile(p, coverage));
                append(qc.managedObjectRecords("footage", p, {status: managedFootage ? "ok" : "missing"}));
            } catch (footageError) {
                append(qc.managedObjectRecords("footage", p, {status: "ownership_error", message: "managed footage validation failed — " + footageError.toString()}));
            }

            if (liveComp && typeof liveComp.layer === "function" && managedFootage) {
                try {
                    var managedLayer = findManagedLayer(liveComp, CutBridgeContract.managedTag("layer", m, p.name), managedFootage, p.name);
                    append(qc.managedObjectRecords("layer", p, {status: managedLayer ? "ok" : "missing"}));
                } catch (layerError) {
                    append(qc.managedObjectRecords("layer", p, {status: "ownership_error", message: "managed layer validation failed — " + layerError.toString()}));
                }
            }
        }

        if (folderLookupError) {
            append(qc.hostRecords({ownershipAmbiguous: true, message: "Managed comp validation failed — " + folderLookupError.toString()}));
            state.comp = null;
        } else if (compLookupError) {
            add({severity: "ERROR", code: "CBQ-COMP-OWNERSHIP-ERROR", scope: "comp", subject: compName,
                message: "Managed comp validation failed — " + compLookupError.toString(),
                remediation: "Preserve artist work and resolve duplicate, misplaced, renamed, or incorrectly tagged managed-comp ownership before running QC again."});
            state.comp = null;
        } else if (projectFolders) {
            if (!managedCompFolder) {
                add({severity: "ERROR", code: "CBQ-COMP-FOLDER-MISSING", scope: "comp", subject: compName,
                    message: "Managed comp folder is missing from the expected package folder.",
                    remediation: "Restore the deterministic 01_COMP folder or rebuild/migrate deliberately; CutBridge will not create it during QC."});
                state.comp = null;
            } else if (!liveComp) {
                add({severity: "ERROR", code: "CBQ-COMP-MISSING", scope: "comp", subject: compName,
                    message: "Managed comp is missing from the expected comp folder.",
                    remediation: "Restore or deliberately rebuild the trusted CutBridge comp; QC will not create or adopt a replacement automatically."});
                state.comp = null;
            } else {
                state.comp = liveComp;
                var expected = CutBridgeContract.expectedCompSpec(m);
                var mismatches = CutBridgeContract.compSpecErrors(expected, {width: liveComp.width, height: liveComp.height, pixelAspect: liveComp.pixelAspect, duration: liveComp.duration, frameRate: liveComp.frameRate});
                append(qc.compRecords(mismatches));
                if (typeof liveComp.layer !== "function") {
                    append(qc.hostRecords({inspectable: false}));
                } else {
                    var staleManagedLayerCount = 0;
                    for (var li = 1; li <= liveComp.numLayers; li++) {
                        var qcLayerComment = itemComment(liveComp.layer(li));
                        if (isAnyManagedTag(qcLayerComment) && !isManagedLayerTagForManifest(qcLayerComment, m)) staleManagedLayerCount++;
                    }
                    append(qc.hostRecords({staleManagedTags: staleManagedLayerCount}));
                }
            }
        } else {
            // A genuinely untouched project can be inspected package/sequence-only.
            // Exact-current managed tags, however, prove that managed AE state exists
            // somewhere in the project. If its package root/comp is gone, report the
            // orphan state instead of silently treating it as pre-Build. Historical
            // version-scoped tags do not match the current manifest and are ignored.
            var orphans = exactCurrentManagedOrphans(m);
            for (var oi = 0; oi < m.passes.length; oi++) {
                var orphanPass = m.passes[oi], orphanKey = "$" + orphanPass.name;
                if (orphans.footage[orphanKey] > 0) {
                    append(qc.managedObjectRecords("footage", orphanPass, {
                        status: "ownership_error",
                        message: orphans.footage[orphanKey] + " exact-current managed footage item(s) exist without the expected CutBridge package root/comp."
                    }));
                }
                if (orphans.layer[orphanKey] > 0) {
                    append(qc.managedObjectRecords("layer", orphanPass, {
                        status: "ownership_error",
                        message: orphans.layer[orphanKey] + " exact-current managed layer(s) exist without the expected CutBridge package root/comp."
                    }));
                }
            }
            state.comp = null;
        }
        return finish();
    }

    function packageStatusText(manifest) {
        if (!manifest) return tr("no_package");
        return tr("package_status", {name: manifest.package_name || manifest.cut, fps: manifest.fps, frames: manifest.frames.count});
    }
    function loadOnly(statusText) { try { var m = chooseManifest(); if (m) statusText.text = packageStatusText(m); } catch (e) { alertError(e.toString()); } }
    function buildUI(thisObj) {
        loadLocalePreference();
        var pal = (thisObj instanceof Panel) ? thisObj : new Window("palette", "CutBridge", undefined, {resizeable: true}); if (!pal) return pal;
        pal.orientation = "column"; pal.alignChildren = ["fill", "top"]; pal.spacing = 8; pal.margins = 12;
        var title = pal.add("statictext", undefined, "CutBridge"); try { title.graphics.font = ScriptUI.newFont(title.graphics.font.name, "BOLD", 16); } catch (e) {}
        var localeLabel = pal.add("statictext", undefined, tr("language_label"));
        var localeSelect = pal.add("dropdownlist", undefined, ["日本語", "English"]); localeSelect.selection = currentLocale === "JA" ? 0 : 1;
        var status = pal.add("statictext", undefined, packageStatusText(state.manifest)); status.characters = 45;
        var btnLoad = pal.add("button", undefined, tr("import_package")); var btnBuild = pal.add("button", undefined, tr("build_comp")); var btnQC = pal.add("button", undefined, tr("run_qc")); var btnRevision = pal.add("button", undefined, tr("update_revision"));
        btnLoad.onClick = function() { loadOnly(status); }; btnBuild.onClick = function() { buildComp(); }; btnQC.onClick = function() { try { runQC(); } catch (e) { alertError(e.toString()); } }; btnRevision.onClick = function() { updateRevision(); };
        var note = pal.add("statictext", undefined, tr("workflow_note", {version: CutBridgeContract.PRODUCT_VERSION}), {multiline: true}); note.preferredSize.height = 32;
        function refreshLocale() {
            // Keep the visible selector synchronized with the effective locale.
            // This matters when localization.js is missing and fallback can only
            // provide English even if app.settings previously stored JA.
            localeSelect.selection = currentLocale === "JA" ? 0 : 1;
            localeLabel.text = tr("language_label"); status.text = packageStatusText(state.manifest);
            btnLoad.text = tr("import_package"); btnBuild.text = tr("build_comp"); btnQC.text = tr("run_qc"); btnRevision.text = tr("update_revision");
            note.text = tr("workflow_note", {version: CutBridgeContract.PRODUCT_VERSION});
            try { pal.layout.layout(true); } catch (layoutError) {}
        }
        localeSelect.onChange = function() {
            if (!localeSelect.selection) return;
            saveLocalePreference(localeSelect.selection.index === 0 ? "JA" : "EN");
            refreshLocale();
        };
        pal.onResizing = pal.onResize = function() { this.layout.resize(); }; return pal;
    }
    CutBridgeContract.loadManifest = loadManifest;
    CutBridgeContract.buildComp = buildComp;
    CutBridgeContract.runQC = runQC;
    CutBridgeContract.getState = function() { return state; };
    var panel = buildUI(thisObj); if (panel instanceof Window) { panel.center(); panel.show(); } else { panel.layout.layout(true); }
})(this);
}
