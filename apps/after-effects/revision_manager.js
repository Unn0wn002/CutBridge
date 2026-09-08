/*
 * S6 revision core for the native CutBridge After Effects adapter.
 * Host integration remains subject to native AE/manual release validation.
 */
(function (root, factory) {
    function aeContractFallback() {
        var PYTHON_WHITESPACE = "[\\u0009-\\u000d\\u001c-\\u0020\\u0085\\u00a0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000]";
        var PYTHON_WHITESPACE_EDGES = new RegExp("^" + PYTHON_WHITESPACE + "+|" + PYTHON_WHITESPACE + "+$", "g");
        var PYTHON_WHITESPACE_RUNS = new RegExp(PYTHON_WHITESPACE + "+", "g");
        function trimPythonWhitespace(value) { return String(value).replace(PYTHON_WHITESPACE_EDGES, ""); }
        function array(value) { return Object.prototype.toString.call(value) === "[object Array]"; }
        function finite(value) { return typeof value === "number" && isFinite(value); }
        function integer(value) {
            return finite(value) && Math.floor(value) === value && Math.abs(value) <= 9007199254740991;
        }
        function zeroPad(n, width) {
            var s = String(n);
            while (s.length < width) s = "0" + s;
            return s;
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
        function validatePattern(pattern) {
            if (typeof pattern !== "string" || !pattern.length || /[\/\\:%\x00-\x1f\x7f<>"|?*]/.test(pattern) || /[ .]$/.test(pattern)) {
                return false;
            }
            var first = pattern.indexOf("####");
            return first >= 0 && pattern.replace("####", "").indexOf("#") < 0;
        }
        function validateRelativePath(path) {
            if (typeof path !== "string" || !path.length) return false;
            var normalized = path.replace(/\\/g, "/");
            if (/^[\/~]/.test(normalized) || /[:%\x00-\x1f\x7f<>"|?*]/.test(normalized)) return false;
            var parts = normalized.split("/");
            for (var i = 0; i < parts.length; i++) {
                if (!parts[i].length || parts[i] === "." || parts[i] === ".." || /[ .]$/.test(parts[i])) return false;
            }
            return true;
        }
        function validateManifest(manifest) {
            var errors = [], i, p, key;
            if (!manifest || typeof manifest !== "object" || array(manifest)) return ["Manifest is empty or invalid JSON data."];
            if (manifest.schema !== "cutbridge-manifest") errors.push("Unsupported manifest schema.");
            if (manifest.schema_version !== 1) errors.push("Unsupported manifest schema_version.");
            var strings = ["cutbridge_version", "project", "episode", "scene", "cut", "take"];
            var identityValid = true;
            for (i = 0; i < strings.length; i++) {
                if (typeof manifest[strings[i]] !== "string") {
                    errors.push("Manifest " + strings[i] + " must be a string.");
                    if (strings[i] !== "cutbridge_version") identityValid = false;
                }
            }
            if (!integer(manifest.version) || manifest.version < 1) errors.push("Manifest version must be a positive integer.");
            if (manifest.package_name !== undefined) {
                if (typeof manifest.package_name !== "string") errors.push("Manifest package_name must be a string when provided.");
                else if (identityValid && integer(manifest.version) && manifest.version >= 1 &&
                    manifest.package_name !== expectedPackageName(manifest)) {
                    errors.push("Manifest package_name does not match Project/Episode/Scene/Cut/Take/version identity.");
                }
            }
            if (!finite(manifest.fps) || manifest.fps <= 0) errors.push("Manifest FPS must be greater than zero.");
            if (!manifest.frames || !integer(manifest.frames.start) || !integer(manifest.frames.end) ||
                !integer(manifest.frames.count) || manifest.frames.start < 0 || manifest.frames.end < manifest.frames.start ||
                manifest.frames.count !== manifest.frames.end - manifest.frames.start + 1) {
                errors.push("Manifest frame range/count is invalid.");
            }
            if (!manifest.resolution || !integer(manifest.resolution.width) || manifest.resolution.width < 1 ||
                !integer(manifest.resolution.height) || manifest.resolution.height < 1) {
                errors.push("Manifest resolution is invalid.");
            } else if (manifest.resolution.pixel_aspect !== undefined &&
                (!finite(manifest.resolution.pixel_aspect) || manifest.resolution.pixel_aspect <= 0)) {
                errors.push("Manifest pixel aspect is invalid.");
            }
            if (!array(manifest.passes) || !manifest.passes.length) {
                errors.push("Manifest contains no render passes.");
            } else {
                var seen = {};
                for (i = 0; i < manifest.passes.length; i++) {
                    p = manifest.passes[i];
                    if (!p || typeof p.name !== "string" || !p.name.length) {
                        errors.push("Manifest pass needs a non-empty name.");
                        continue;
                    }
                    key = "$" + p.name;
                    if (seen[key]) errors.push("Manifest contains duplicate render pass name: " + p.name + ".");
                    seen[key] = true;
                    if (!validateRelativePath(p.path)) errors.push(p.name + ": invalid package-relative path.");
                    if (!validatePattern(p.sequence_pattern)) errors.push(p.name + ": invalid sequence pattern.");
                    if (p.required !== undefined && typeof p.required !== "boolean") errors.push(p.name + ": required must be a boolean.");
                }
                if (manifest.ae && manifest.ae.layer_order !== undefined) {
                    if (!array(manifest.ae.layer_order)) errors.push("Manifest ae.layer_order must be an array when provided.");
                    else {
                        var ordered = {};
                        for (i = 0; i < manifest.ae.layer_order.length; i++) {
                            key = "$" + manifest.ae.layer_order[i];
                            if (typeof manifest.ae.layer_order[i] !== "string" || !seen[key]) {
                                errors.push("Manifest ae.layer_order references an unknown pass.");
                            } else if (ordered[key]) {
                                errors.push("Manifest ae.layer_order contains a duplicate pass.");
                            }
                            ordered[key] = true;
                        }
                    }
                }
            }
            return errors;
        }
        return {validateManifest: validateManifest, trimPythonWhitespace: trimPythonWhitespace};
    }

    if (typeof module !== "undefined" && module.exports) {
        module.exports = factory(require("./CutBridge.jsx"));
    } else {
        var contract = root && root.CutBridgeContract;
        if ((!contract || typeof contract.validateManifest !== "function") &&
            typeof $ !== "undefined" && $.global) {
            contract = aeContractFallback();
        }
        if (!root) root = (typeof $ !== "undefined" && $.global) ? $.global : this;
        root.CutBridgeRevisionManager = factory(contract);
    }
}(typeof $ !== "undefined" && $.global ? $.global : this, function (Contract) {
    "use strict";
    if (!Contract || typeof Contract.validateManifest !== "function") {
        throw new Error("Load CutBridgeContract before the revision core.");
    }
    var IDS = ["project", "episode", "scene", "cut", "take"];
    function own(o, key) { return Object.prototype.hasOwnProperty.call(o, key); }
    function array(value) { return Object.prototype.toString.call(value) === "[object Array]"; }
    function errorText(value) {
        try { return String(value); }
        catch (formatError) { return "Unprintable host/manifest error"; }
    }
    function integer(value) {
        return typeof value === "number" && isFinite(value) &&
            value > 0 && Math.floor(value) === value && value <= 9007199254740991;
    }
    function revisionNumber(value) {
        if (integer(value)) return value;
        if (typeof value !== "string" || !/^V[0-9]{3,}$/.test(value)) return NaN;
        var number = Number(value.slice(1)), digits = String(number);
        while (digits.length < 3) digits = "0" + digits;
        return integer(number) && value === "V" + digits ? number : NaN;
    }
    function manifestErrors(m) {
        var errors, i;
        if (m && typeof m === "object" && !array(m) &&
            (typeof m.schema !== "string" || typeof m.schema_version !== "number")) {
            return ["Manifest schema must be a string and schema_version must be numeric."];
        }
        try { errors = Contract.validateManifest(m); }
        catch (validationError) { return ["Manifest validator rejected data: " + errorText(validationError)]; }
        if (!m || typeof m !== "object" || array(m)) return errors;
        for (i = 0; i < IDS.length; i++) {
            if (typeof m[IDS[i]] !== "string" || !Contract.trimPythonWhitespace(m[IDS[i]]).length) {
                errors.push("S6 requires a non-empty " + IDS[i] + " identity field.");
            }
        }
        if (m.package_name !== undefined &&
            (typeof m.package_name !== "string" || !Contract.trimPythonWhitespace(m.package_name).length)) {
            errors.push("package_name must be a non-empty string when provided.");
        }
        return errors;
    }
    function requireManifest(m) {
        var errors = manifestErrors(m);
        if (errors.length) throw new Error("Revision manifest rejected: " + errors.join("; "));
    }
    function sameCut(a, b) {
        for (var i = 0; i < IDS.length; i++) if (a[IDS[i]] !== b[IDS[i]]) return false;
        return true;
    }
    function encode(value) { value = String(value); return value.length + ":" + value; }
    function identity(m) {
        requireManifest(m);
        var value = "";
        for (var i = 0; i < IDS.length; i++) value += encode(m[IDS[i]]);
        return value;
    }
    function ownershipKey(m, passName) {
        return "CUTBRIDGE-REVISION-1:" + identity(m) + encode(m.version) +
            encode(m.package_name === undefined ? "" : m.package_name) + encode(passName);
    }
    function passMap(m) {
        var out = {};
        for (var i = 0; i < m.passes.length; i++) out["$" + m.passes[i].name] = m.passes[i];
        return out;
    }
    function aspect(m) { return m.resolution.pixel_aspect === undefined ? 1 : m.resolution.pixel_aspect; }
    function assess(current, candidate) {
        var errors = [], warnings = [], left = manifestErrors(current), right = manifestErrors(candidate), i;
        for (i = 0; i < left.length; i++) errors.push("Current: " + left[i]);
        for (i = 0; i < right.length; i++) errors.push("Candidate: " + right[i]);
        if (errors.length) return {status: "incompatible", reasons: errors, warnings: warnings};
        if (!sameCut(current, candidate)) errors.push("Project/episode/scene/cut/take identity differs.");
        if (candidate.version <= current.version) errors.push("Candidate must be a newer revision.");
        var currentComp = current.ae && current.ae.comp_name ? current.ae.comp_name : current.cut + "_COMP";
        var candidateComp = candidate.ae && candidate.ae.comp_name ? candidate.ae.comp_name : candidate.cut + "_COMP";
        if (currentComp !== candidateComp) errors.push("Composition identity/name changes are unsupported.");
        if (current.fps !== candidate.fps) errors.push("FPS changes are unsupported.");
        if (current.frames.start !== candidate.frames.start || current.frames.end !== candidate.frames.end ||
            current.frames.count !== candidate.frames.count) errors.push("Frame range/count changes are unsupported.");
        if (aspect(current) !== aspect(candidate)) errors.push("Pixel aspect changes are unsupported.");
        if (current.resolution.width !== candidate.resolution.width || current.resolution.height !== candidate.resolution.height) {
            errors.push("Resolution changes are unsupported by source-only revision; rebuild or migrate the comp deliberately.");
        }
        var old = passMap(current), next = passMap(candidate), p;
        for (i = 0; i < current.passes.length; i++) {
            p = current.passes[i];
            if (!own(next, "$" + p.name)) {
                if (p.required !== false) errors.push("Previously required pass missing: " + p.name);
                else errors.push("Removing an optional pass is unsupported by source-only revision: " + p.name + ". Rebuild or migrate the comp deliberately.");
            } else if ((p.required !== false) !== (next["$" + p.name].required !== false)) {
                warnings.push("Required/optional status changed: " + p.name);
            }
        }
        for (i = 0; i < candidate.passes.length; i++) {
            p = candidate.passes[i];
            if (!own(old, "$" + p.name)) {
                errors.push("Adding passes is unsupported by source-only revision: " + p.name);
            }
        }
        return {status: errors.length ? "incompatible" : warnings.length ? "warning" : "safe",
            reasons: errors, warnings: warnings};
    }
    function discover(current, candidates) {
        requireManifest(current);
        if (!array(candidates)) throw new Error("Candidates must be an array.");
        var out = [], counts = {}, i, m, valid, key;
        for (i = 0; i < candidates.length; i++) {
            m = candidates[i];
            valid = manifestErrors(m).length === 0;
            if (valid && sameCut(current, m) && m.version > current.version) {
                key = "$" + m.version; counts[key] = (counts[key] || 0) + 1;
            }
            out.push({manifest: m, version: valid ? m.version : null,
                newer: valid && m.version > current.version, compatibility: assess(current, m)});
        }
        for (i = 0; i < out.length; i++) {
            m = out[i].manifest;
            if (out[i].version !== null && sameCut(current, m) && counts["$" + m.version] > 1) {
                out[i].compatibility.status = "incompatible";
                out[i].compatibility.reasons.push("Duplicate candidate revision is ambiguous: V" + m.version);
                out[i].ambiguous = true;
            }
        }
        return out;
    }
    function selectLatest(current, candidates) {
        var rows = discover(current, candidates), best = null;
        for (var i = 0; i < rows.length; i++) {
            if (rows[i].ambiguous) return null;
            if (rows[i].compatibility.status !== "incompatible" && (!best || rows[i].version > best.version)) best = rows[i];
        }
        return best;
    }
    function snapshot(m) {
        var out = {schema: m.schema, schema_version: m.schema_version, cutbridge_version: m.cutbridge_version,
            version: m.version, fps: m.fps, frames: {start: m.frames.start, end: m.frames.end, count: m.frames.count},
            resolution: {width: m.resolution.width, height: m.resolution.height, pixel_aspect: aspect(m)}, passes: []};
        if (m.package_name !== undefined) out.package_name = m.package_name;
        for (var i = 0; i < IDS.length; i++) out[IDS[i]] = m[IDS[i]];
        for (i = 0; i < m.passes.length; i++) {
            var p = m.passes[i];
            out.passes.push({name: p.name, path: p.path, sequence_pattern: p.sequence_pattern, required: p.required !== false});
        }
        return out;
    }
    function createExecutor(adapter) {
        var methods = ["listManagedLayers", "validateManagedLayer", "readSource", "importReplacement",
            "validateReplacement", "swapManagedSource", "restoreManagedSource", "removeImportedReplacement",
            "commitRevision"];
        var host = {}, pending = null, busy = false, poisoned = false;
        for (var i = 0; i < methods.length; i++) {
            if (!adapter || typeof adapter[methods[i]] !== "function") throw new Error("Required adapter callback: " + methods[i]);
            host[methods[i]] = adapter[methods[i]];
        }
        function available() {
            if (busy) throw new Error("Revision executor is busy.");
            if (poisoned) throw new Error("Rollback incomplete; recover the project before creating a new executor.");
        }
        function verify(action, current) {
            if (host.validateManagedLayer(action.layer, snapshot(current), action.passName,
                ownershipKey(current, action.passName)) !== true ||
                host.readSource(action.layer) !== action.oldSource) {
                throw new Error("Live managed ownership/source drift: " + action.passName);
            }
        }
        function prepare(current, candidate) {
            available(); pending = null;
            var compatibility = assess(current, candidate);
            if (compatibility.status === "incompatible") throw new Error(compatibility.reasons.join("; "));
            current = snapshot(current); candidate = snapshot(candidate);
            var records = host.listManagedLayers(snapshot(current)), actions = [], seen = {}, old = passMap(current), next = passMap(candidate);
            if (!array(records)) throw new Error("Adapter must return verified managed-layer records.");
            for (var j = 0; j < records.length; j++) {
                var record = records[j], key = record && "$" + record.passName;
                if (!record || !own(old, key) || seen[key] || !record.layer) throw new Error("Invalid or duplicate managed-layer record.");
                for (var k = 0; k < j; k++) if (records[k].layer === record.layer) throw new Error("Duplicate managed layer handle.");
                seen[key] = true;
                var action = {passName: record.passName, layer: record.layer, oldSource: host.readSource(record.layer),
                    replacement: next[key]};
                if (!action.oldSource) throw new Error("Managed layer has no source.");
                verify(action, current);
                if (own(next, key)) actions.push(action);
            }
            for (j = 0; j < current.passes.length; j++) {
                var pass = current.passes[j], nextPass = next["$" + pass.name];
                if ((pass.required !== false || (nextPass && nextPass.required !== false)) && !seen["$" + pass.name]) {
                    throw new Error("Missing required managed layer: " + pass.name);
                }
            }
            if (!actions.length) throw new Error("No managed source replacements available.");
            var ticket = {status: compatibility.status, warnings: compatibility.warnings.slice(0),
                requiresConfirmation: compatibility.status === "warning", replacementCount: actions.length};
            pending = {ticket: ticket, current: current, candidate: candidate, actions: actions,
                requiresConfirmation: ticket.requiresConfirmation};
            return ticket;
        }
        function apply(ticket, confirmed) {
            available();
            if (!pending || pending.ticket !== ticket) throw new Error("Unknown, expired or already applied revision plan.");
            if (pending.requiresConfirmation && confirmed !== true) throw new Error("Revision requires explicit confirmation.");
            var plan = pending; pending = null; busy = true;
            var made = [], attempted = [], replacements = [], failures = [], j;
            function track(item) {
                if (!item) throw new Error("Cannot track empty replacement.");
                for (var a = 0; a < plan.actions.length; a++) if (plan.actions[a].oldSource === item) throw new Error("Import must create new footage.");
                for (var b = 0; b < made.length; b++) if (made[b] === item) throw new Error("Replacement already tracked.");
                made.push(item);
            }
            try {
                for (j = 0; j < plan.actions.length; j++) verify(plan.actions[j], plan.current);
                for (j = 0; j < plan.actions.length; j++) {
                    var action = plan.actions[j], before = made.length;
                    var item = host.importReplacement(snapshot(plan.candidate), action.passName, track);
                    if (made.length !== before + 1 || made[before] !== item) throw new Error("Import must register exactly one new replacement.");
                    if (host.validateReplacement(item, snapshot(plan.candidate), action.passName) !== true) {
                        throw new Error("Replacement validation failed: " + action.passName);
                    }
                    replacements.push(item);
                }
                for (j = 0; j < plan.actions.length; j++) verify(plan.actions[j], plan.current);
                for (j = 0; j < plan.actions.length; j++) {
                    action = plan.actions[j];
                    verify(action, plan.current);
                    attempted.push(action);
                    host.swapManagedSource(action.layer, replacements[j], action.passName);
                    if (host.readSource(action.layer) !== replacements[j]) throw new Error("Source swap verification failed.");
                }
                host.commitRevision(snapshot(plan.current), snapshot(plan.candidate), replacements);
                return {status: "applied", replaced: attempted.length};
            } catch (error) {
                for (j = attempted.length - 1; j >= 0; j--) {
                    try {
                        host.restoreManagedSource(attempted[j].layer, attempted[j].oldSource, attempted[j].passName);
                        if (host.readSource(attempted[j].layer) !== attempted[j].oldSource) throw new Error("Source restoration not verified.");
                    } catch (restoreError) {
                        poisoned = true;
                        failures.push("Restore " + attempted[j].passName + ": " + errorText(restoreError));
                    }
                }
                var retained = failures.length ? made.length : 0;
                if (!failures.length) {
                    for (j = made.length - 1; j >= 0; j--) {
                        try {
                            if (host.removeImportedReplacement(made[j]) !== true) throw new Error("Removal not verified.");
                        } catch (removeError) {
                            poisoned = true;
                            retained++;
                            failures.push("Remove replacement: " + errorText(removeError));
                        }
                    }
                }
                poisoned = failures.length > 0;
                var report = new Error("Revision failed: " + errorText(error) +
                    (failures.length ? "; ROLLBACK INCOMPLETE: " + failures.join("; ") : "; rollback completed."));
                report.rollbackFailures = failures;
                report.retainedReplacements = retained;
                throw report;
            } finally { busy = false; }
        }
        return {prepare: prepare, apply: apply};
    }
    return {assess: assess, identity: identity, ownershipKey: ownershipKey, revisionNumber: revisionNumber,
        discover: discover, selectLatest: selectLatest, createExecutor: createExecutor};
}));

/*
 * Real After Effects host defense-in-depth.
 *
 * Native S6 validation found that a separately evaluated ExtendScript manager could
 * reach the UI confirmation path even though the core compatibility rule already
 * rejects pass additions/removals. Keep the core rule above, and independently
 * re-check the pass-set at the exported AE-host boundary before CutBridge.jsx can
 * consume assess(). This does not run in CommonJS/Node, so the portable core API
 * and its tests remain unchanged.
 */
(function (root) {
    if (typeof module !== "undefined" && module.exports) return;
    if (!root || !root.CutBridgeRevisionManager ||
        typeof root.CutBridgeRevisionManager.assess !== "function") return;

    var manager = root.CutBridgeRevisionManager;
    var coreAssess = manager.assess;

    function hasPass(manifest, name) {
        if (!manifest || !manifest.passes || typeof manifest.passes.length !== "number") return false;
        for (var i = 0; i < manifest.passes.length; i++) {
            if (manifest.passes[i] && manifest.passes[i].name === name) return true;
        }
        return false;
    }

    function hostPassSetErrors(current, candidate) {
        var errors = [], i, p;
        if (!current || !candidate || !current.passes || !candidate.passes) return errors;

        for (i = 0; i < current.passes.length; i++) {
            p = current.passes[i];
            if (!p || typeof p.name !== "string") continue;
            if (!hasPass(candidate, p.name)) {
                if (p.required !== false) errors.push("Previously required pass missing: " + p.name);
                else errors.push("Removing an optional pass is unsupported by source-only revision: " + p.name + ". Rebuild or migrate the comp deliberately.");
            }
        }
        for (i = 0; i < candidate.passes.length; i++) {
            p = candidate.passes[i];
            if (!p || typeof p.name !== "string") continue;
            if (!hasPass(current, p.name)) {
                errors.push("Adding passes is unsupported by source-only revision: " + p.name);
            }
        }
        return errors;
    }

    manager.assess = function (current, candidate) {
        var result = coreAssess(current, candidate);
        var hostErrors = hostPassSetErrors(current, candidate);
        if (!hostErrors.length) return result;

        var reasons = result && result.reasons && typeof result.reasons.slice === "function" ? result.reasons.slice(0) : [];
        for (var i = 0; i < hostErrors.length; i++) {
            var duplicate = false;
            for (var j = 0; j < reasons.length; j++) if (reasons[j] === hostErrors[i]) { duplicate = true; break; }
            if (!duplicate) reasons.push(hostErrors[i]);
        }
        return {
            status: "incompatible",
            reasons: reasons,
            warnings: result && result.warnings && typeof result.warnings.slice === "function" ? result.warnings.slice(0) : []
        };
    };

    root.CutBridgeRevisionManager = manager;
}(typeof $ !== "undefined" && $.global ? $.global : this));
