/*
CutBridge After Effects
- Reads and validates cutbridge.json schema/version
- Creates deterministic AE folders + comp
- Imports complete required image sequences from manifest
- Skips unavailable optional passes with warnings
- QC validates exact manifest frame coverage, duration and FPS

Install/test:
File > Scripts > Run Script File... > CutBridge.jsx
For a dockable panel, place this file in After Effects/Scripts/ScriptUI Panels and restart AE.
*/

var CutBridgeContract = (function () {
    // Centrally checked against blender_manifest.toml by the release builder.
    var PRODUCT_VERSION = "0.2.3";
    var SCHEMA = "cutbridge-manifest";
    var SCHEMA_VERSION = 1;

    function zeroPad(n, width) {
        var s = String(n);
        while (s.length < width) s = "0" + s;
        return s;
    }

    function parseJSON(text) {
        if (typeof JSON !== "undefined" && JSON.parse) return JSON.parse(text);
        // Older ExtendScript engines lack JSON. Parse data without executing it.
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
                        // Do not let an input key mutate the legacy object's prototype.
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

    function isArray(value) {
        // ES3-compatible; instanceof Array fails for host/Node vm realm boundaries.
        return Object.prototype.toString.call(value) === "[object Array]";
    }

    function isFiniteNumber(value) {
        return typeof value === "number" && isFinite(value);
    }

    function isInteger(value) {
        return isFiniteNumber(value) && Math.floor(value) === value && Math.abs(value) <= 9007199254740991;
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
        // '%' is rejected because ExtendScript File/Folder accepts URI-escaped paths.
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
        if (/^[A-Za-z]:/.test(root) || root.indexOf("//") === 0) {
            root = root.toLowerCase(); candidate = candidate.toLowerCase();
        }
        return candidate.indexOf(root + "/") === 0;
    }

    function escapeRegex(text) {
        return text.replace(/([.*+?^${}()|\[\]\\])/g, "\\$1");
    }

    function validatePattern(pattern) {
        if (typeof pattern !== "string" || !pattern.length || /[\/\\:%\x00-\x1f\x7f<>"|?*]/.test(pattern) || /[ .]$/.test(pattern)) {
            throw new Error("Sequence pattern must be a safe filename, without directories or URI escapes.");
        }
        var first = pattern.indexOf("####");
        if (first < 0 || pattern.replace("####", "").indexOf("#") >= 0) {
            throw new Error("Sequence pattern must contain exactly one #### frame token.");
        }
    }

    function patternToRegex(pattern) {
        validatePattern(pattern);
        // Match wrong padding/signs too, so QC can diagnose unexpected filenames.
        return new RegExp("^" + escapeRegex(pattern).replace("####", "(-?\\d+)") + "$", "i");
    }

    function expectedFrameName(pattern, frame) {
        validatePattern(pattern);
        if (!isInteger(frame) || frame < 0) throw new Error("Export frame must be a non-negative finite integer.");
        return pattern.replace("####", zeroPad(frame, 4));
    }

    function validateManifest(manifest) {
        var errors = [];
        if (!manifest || typeof manifest !== "object" || isArray(manifest)) return ["Manifest is empty or invalid JSON data."];
        if (manifest.schema !== SCHEMA) errors.push("Unsupported manifest schema: " + String(manifest.schema));
        if (manifest.schema_version !== SCHEMA_VERSION) {
            errors.push("Unsupported manifest schema_version " + String(manifest.schema_version) + "; CutBridge AE supports " + String(SCHEMA_VERSION) + ".");
        }
        var strings = ["cutbridge_version", "project", "episode", "scene", "cut", "take"];
        for (var n = 0; n < strings.length; n++) {
            if (typeof manifest[strings[n]] !== "string") errors.push("Manifest " + strings[n] + " must be a string.");
        }
        if (!isInteger(manifest.version) || manifest.version < 1) errors.push("Manifest version must be a positive integer.");
        var frameError = validateFrames(manifest.frames);
        if (frameError) errors.push(frameError);
        if (!isFiniteNumber(manifest.fps) || manifest.fps <= 0) errors.push("Manifest FPS must be a finite number greater than zero.");
        var r = manifest.resolution;
        if (!r || !isInteger(r.width) || r.width < 1 || !isInteger(r.height) || r.height < 1) {
            errors.push("Manifest resolution width/height must be positive integers.");
        }
        if (r && r.pixel_aspect !== undefined && (!isFiniteNumber(r.pixel_aspect) || r.pixel_aspect <= 0)) {
            errors.push("Manifest resolution pixel_aspect must be a finite number greater than zero.");
        }
        if (!isArray(manifest.passes) || manifest.passes.length === 0) {
            errors.push("Manifest contains no render passes.");
        } else {
            for (var i = 0; i < manifest.passes.length; i++) {
                var p = manifest.passes[i];
                if (!p || typeof p.name !== "string" || !p.name.length) {
                    errors.push("Manifest pass at index " + i + " needs a non-empty name."); continue;
                }
                try { relativePassPath(p.path); } catch (pathError) { errors.push(p.name + ": " + pathError.message); }
                try { patternToRegex(p.sequence_pattern); } catch (patternError) { errors.push(p.name + ": " + patternError.message); }
                if (p.required !== undefined && typeof p.required !== "boolean") errors.push(p.name + ": required must be a boolean.");
            }
        }
        return errors;
    }

    function sequenceCoverage(passInfo, manifest, fileNames) {
        var frameError = validateFrames(manifest.frames);
        if (frameError) throw new Error(frameError);
        var result = {
            complete: false,
            firstName: null,
            missing: [],
            unexpected: [],
            matching: []
        };
        var regex = patternToRegex(passInfo.sequence_pattern);
        var exact = {};
        var expected = {};
        var i;

        for (i = 0; i < fileNames.length; i++) {
            var name = String(fileNames[i]);
            var match = regex.exec(name);
            if (match) {
                result.matching.push(name);
                exact[name.toLowerCase()] = name;
            }
        }

        for (var frame = manifest.frames.start; frame <= manifest.frames.end; frame++) {
            var expectedName = expectedFrameName(passInfo.sequence_pattern, frame);
            expected[expectedName.toLowerCase()] = true;
            if (!exact[expectedName.toLowerCase()]) result.missing.push(frame);
        }

        for (i = 0; i < result.matching.length; i++) {
            if (!expected[result.matching[i].toLowerCase()]) result.unexpected.push(result.matching[i]);
        }

        result.complete = result.missing.length === 0;
        if (result.complete) result.firstName = exact[expectedFrameName(passInfo.sequence_pattern, manifest.frames.start).toLowerCase()];
        return result;
    }

    return {
        parseJSON: parseJSON,
        PRODUCT_VERSION: PRODUCT_VERSION,
        relativePassPath: relativePassPath,
        pathIsInside: pathIsInside,
        SCHEMA: SCHEMA,
        SCHEMA_VERSION: SCHEMA_VERSION,
        validateManifest: validateManifest,
        patternToRegex: patternToRegex,
        expectedFrameName: expectedFrameName,
        sequenceCoverage: sequenceCoverage
    };
})();

if (typeof module !== "undefined" && module.exports) {
    module.exports = CutBridgeContract;
} else {
(function CutBridge(thisObj) {
    var state = {manifestFile: null, manifest: null, packageFolder: null, comp: null, imported: {}};

    function log(msg) { $.writeln("[CutBridge] " + msg); }
    function alertError(msg) { alert("CutBridge\n\n" + msg); }

    function readTextFile(file) {
        file.encoding = "UTF-8";
        if (!file.open("r")) throw new Error("Could not open: " + file.fsName);
        var text = file.read();
        file.close();
        return text;
    }

    function chooseManifest() {
        var f = File.openDialog("Choose CutBridge cutbridge.json", "JSON:*.json");
        if (!f) return null;
        var obj = CutBridgeContract.parseJSON(readTextFile(f));
        var contractErrors = CutBridgeContract.validateManifest(obj);
        if (contractErrors.length) throw new Error("Manifest contract rejected:\n- " + contractErrors.join("\n- "));
        state.manifestFile = f;
        state.manifest = obj;
        state.packageFolder = f.parent;
        state.imported = {};
        state.comp = null;
        return obj;
    }

    function ensureManifestLoaded() {
        if (state.manifest) return true;
        try { return !!chooseManifest(); }
        catch (e) { alertError(e.toString()); return false; }
    }

    function findChildFolder(parent, name) {
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (item instanceof FolderItem && item.name === name && item.parentFolder === parent) return item;
        }
        var folder = app.project.items.addFolder(name);
        folder.parentFolder = parent;
        return folder;
    }

    function ensureProjectFolders(manifest) {
        var rootName = manifest.package_name || (manifest.project + "_" + manifest.cut);
        var root = findChildFolder(app.project.rootFolder, rootName);
        return {root: root, comp: findChildFolder(root, "01_COMP"), render: findChildFolder(root, "02_RENDER"), precomp: findChildFolder(root, "03_PRECOMP"), output: findChildFolder(root, "04_OUTPUT")};
    }

    function listSequenceFileNames(passInfo) {
        var relative = CutBridgeContract.relativePassPath(passInfo.path);
        var parts = relative.split("/");
        var dir = state.packageFolder;
        for (var p = 0; p < parts.length; p++) {
            dir = new Folder(dir.fsName + "/" + parts[p]);
            if (dir.alias || !CutBridgeContract.pathIsInside(state.packageFolder.fsName, dir.fsName)) {
                throw new Error(passInfo.name + ": pass folder must stay inside the package; aliases are not supported.");
            }
        }
        if (!dir.exists) return {dir: dir, names: []};
        var regex = CutBridgeContract.patternToRegex(passInfo.sequence_pattern);
        var files = dir.getFiles(function(f) { return f instanceof File && regex.test(File.decode(f.name)); });
        var names = [];
        for (var i = 0; files && i < files.length; i++) {
            if (files[i].alias || !CutBridgeContract.pathIsInside(dir.fsName, files[i].fsName)) {
                throw new Error(passInfo.name + ": sequence files must stay inside the pass folder; aliases are not supported.");
            }
            names.push(File.decode(files[i].name));
        }
        return {dir: dir, names: names};
    }

    function inspectSequence(passInfo, manifest) {
        var listing = listSequenceFileNames(passInfo);
        var coverage = CutBridgeContract.sequenceCoverage(passInfo, manifest, listing.names);
        coverage.folderExists = listing.dir.exists;
        coverage.dir = listing.dir;
        return coverage;
    }

    function formatMissingFrames(frames) {
        if (!frames.length) return "";
        var shown = frames.slice(0, 12).join(", ");
        if (frames.length > 12) shown += " … +" + (frames.length - 12) + " more";
        return shown;
    }

    function importSequence(passInfo, manifest, renderFolder, coverage) {
        coverage = coverage || inspectSequence(passInfo, manifest);
        if (!coverage.folderExists) throw new Error(passInfo.name + ": pass folder missing.");
        if (!coverage.complete) throw new Error(passInfo.name + ": missing frame(s): " + formatMissingFrames(coverage.missing));
        var firstFile = new File(coverage.dir.fsName + "/" + coverage.firstName);
        if (firstFile.alias || !CutBridgeContract.pathIsInside(coverage.dir.fsName, firstFile.fsName)) throw new Error(passInfo.name + ": unsafe first-frame path.");
        if (!firstFile.exists) throw new Error(passInfo.name + ": expected first frame is missing: " + coverage.firstName);
        var io = new ImportOptions(firstFile);
        if (io.canImportAs && io.canImportAs(ImportAsType.FOOTAGE)) io.importAs = ImportAsType.FOOTAGE;
        io.sequence = true;
        io.forceAlphabetical = false;
        var footage = app.project.importFile(io);
        footage.name = manifest.cut + "_" + passInfo.name;
        footage.parentFolder = renderFolder;
        try { footage.mainSource.conformFrameRate = manifest.fps; } catch (e) { log("Could not conform FPS for " + passInfo.name + ": " + e.toString()); }
        state.imported[passInfo.name] = footage;
        return footage;
    }

    function findExistingComp(name, parentFolder) {
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (item instanceof CompItem && item.name === name && item.parentFolder === parentFolder) return item;
        }
        return null;
    }

    function buildComp() {
        if (!ensureManifestLoaded()) return;
        if (!app.project) app.newProject();
        var m = state.manifest;
        var folders = ensureProjectFolders(m);
        var compName = (m.ae && m.ae.comp_name) ? m.ae.comp_name : (m.cut + "_COMP");
        var duration = m.frames.count / m.fps;
        var warnings = [];
        app.beginUndoGroup("CutBridge Build Comp");
        try {
            var comp = findExistingComp(compName, folders.comp);
            if (!comp) {
                comp = app.project.items.addComp(compName, m.resolution.width, m.resolution.height, m.resolution.pixel_aspect || 1.0, duration, m.fps);
                comp.parentFolder = folders.comp;
            }
            state.comp = comp;
            for (var i = 0; i < m.passes.length; i++) {
                var p = m.passes[i];
                var coverage = inspectSequence(p, m);
                if (!coverage.folderExists || !coverage.complete) {
                    var reason = !coverage.folderExists ? "pass folder missing" : ("missing frame(s): " + formatMissingFrames(coverage.missing));
                    if (p.required === false) { warnings.push(p.name + ": optional pass skipped — " + reason); continue; }
                    throw new Error(p.name + ": required pass cannot be imported — " + reason);
                }
                if (coverage.unexpected.length) warnings.push(p.name + ": unexpected matching filename(s): " + coverage.unexpected.join(", "));
                var footage = state.imported[p.name] || importSequence(p, m, folders.render, coverage);
                var layer = comp.layers.add(footage);
                layer.name = p.name;
                layer.startTime = 0;
            }
            if (m.ae && m.ae.layer_order) {
                for (var j = m.ae.layer_order.length - 1; j >= 0; j--) {
                    var lname = m.ae.layer_order[j];
                    for (var k = 1; k <= comp.numLayers; k++) {
                        if (comp.layer(k).name === lname) { comp.layer(k).moveToBeginning(); break; }
                    }
                }
            }
            comp.openInViewer();
            var message = "CutBridge: comp built\n" + comp.name + "\n" + m.resolution.width + "x" + m.resolution.height + " @ " + m.fps + " fps";
            if (warnings.length) message += "\n\nWarnings:\n- " + warnings.join("\n- ");
            alert(message);
        } catch (e) { alertError(e.toString()); }
        finally { app.endUndoGroup(); }
    }

    function runQC() {
        if (!ensureManifestLoaded()) return;
        var m = state.manifest;
        var lines = [];
        var errors = 0;
        var warnings = 0;
        function ok(msg) { lines.push("PASS " + msg); }
        function warn(msg) { warnings++; lines.push("WARN " + msg); }
        function bad(msg) { errors++; lines.push("ERR  " + msg); }
        var contractErrors = CutBridgeContract.validateManifest(m);
        if (contractErrors.length) { alertError("Manifest contract rejected:\n- " + contractErrors.join("\n- ")); return; }
        else ok("Manifest schema " + CutBridgeContract.SCHEMA + " v" + CutBridgeContract.SCHEMA_VERSION);
        if (m.fps > 0) ok("FPS " + m.fps); else bad("Invalid FPS");
        if (m.frames && m.frames.count === (m.frames.end - m.frames.start + 1)) ok("Frame count " + m.frames.count); else bad("Frame count mismatch");
        if (m.resolution && m.resolution.width > 0 && m.resolution.height > 0) ok("Resolution " + m.resolution.width + "x" + m.resolution.height); else bad("Invalid resolution");
        for (var i = 0; i < m.passes.length; i++) {
            var p = m.passes[i];
            var coverage = inspectSequence(p, m);
            var optional = p.required === false;
            if (!coverage.folderExists) { if (optional) warn(p.name + ": optional pass folder missing"); else bad(p.name + ": required pass folder missing"); continue; }
            if (!coverage.complete) {
                var missingMsg = p.name + ": missing frame(s): " + formatMissingFrames(coverage.missing);
                if (optional) warn(missingMsg + " (optional pass)"); else bad(missingMsg);
                continue;
            }
            ok(p.name + ": " + m.frames.count + "/" + m.frames.count + " expected frames present");
            if (coverage.unexpected.length) warn(p.name + ": " + coverage.unexpected.length + " unexpected matching filename(s)");
        }
        if (state.comp) {
            if (Math.abs(state.comp.frameRate - m.fps) < 0.001) ok("Comp FPS matches manifest"); else bad("Comp FPS mismatch");
            var expectedDuration = m.frames.count / m.fps;
            if (Math.abs(state.comp.duration - expectedDuration) < (1.0 / m.fps)) ok("Comp duration matches manifest"); else bad("Comp duration mismatch");
        }
        var headline = errors === 0 ? (warnings === 0 ? "PASS" : ("PASS with " + warnings + " warning(s)")) : (errors + " error(s), " + warnings + " warning(s)");
        alert("CutBridge QC — " + headline + "\n\n" + lines.join("\n"));
    }

    function loadOnly(statusText) {
        try {
            var m = chooseManifest();
            if (m) statusText.text = (m.package_name || m.cut) + " | " + m.fps + "fps | " + m.frames.count + "f";
        } catch (e) { alertError(e.toString()); }
    }

    function buildUI(thisObj) {
        var pal = (thisObj instanceof Panel) ? thisObj : new Window("palette", "CutBridge", undefined, {resizeable: true});
        if (!pal) return pal;
        pal.orientation = "column";
        pal.alignChildren = ["fill", "top"];
        pal.spacing = 8;
        pal.margins = 12;
        var title = pal.add("statictext", undefined, "CutBridge / カットブリッジ");
        try { title.graphics.font = ScriptUI.newFont(title.graphics.font.name, "BOLD", 16); } catch (e) {}
        var status = pal.add("statictext", undefined, "No package loaded");
        status.characters = 45;
        var btnLoad = pal.add("button", undefined, "1. Import Package / 読み込み");
        var btnBuild = pal.add("button", undefined, "2. Build Comp / コンポ作成");
        var btnQC = pal.add("button", undefined, "3. Run QC / QC実行");
        btnLoad.onClick = function() { loadOnly(status); };
        btnBuild.onClick = function() { buildComp(); };
        btnQC.onClick = function() { try { runQC(); } catch (e) { alertError(e.toString()); } };
        var note = pal.add("statictext", undefined, "v" + CutBridgeContract.PRODUCT_VERSION + ": validated package → comp → QC", {multiline: true});
        note.preferredSize.height = 32;
        pal.onResizing = pal.onResize = function() { this.layout.resize(); };
        return pal;
    }

    var panel = buildUI(thisObj);
    if (panel instanceof Window) { panel.center(); panel.show(); }
    else { panel.layout.layout(true); }
})(this);
}
