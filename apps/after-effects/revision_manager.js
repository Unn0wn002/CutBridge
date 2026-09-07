/*
 * S6 revision core. Native AE adapter/UI and release integration are outstanding.
 * Existing S5 project tags are never rewritten by this module.
 */
(function (root, factory) {
    if (typeof module !== "undefined" && module.exports) {
        module.exports = factory(require("./CutBridge.jsx"));
    } else {
        root.CutBridgeRevisionManager = factory(root.CutBridgeContract);
    }
}(this, function (Contract) {
    "use strict";
    if (!Contract || typeof Contract.validateManifest !== "function") {
        throw new Error("Load CutBridgeContract before the revision core.");
    }
    var IDS = ["project", "episode", "scene", "cut", "take"];
    function own(o, key) { return Object.prototype.hasOwnProperty.call(o, key); }
    function array(value) { return Object.prototype.toString.call(value) === "[object Array]"; }
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
        var errors = Contract.validateManifest(m), i;
        if (!m || typeof m !== "object" || array(m)) return errors;
        for (i = 0; i < IDS.length; i++) {
            if (typeof m[IDS[i]] !== "string" || !/\S/.test(m[IDS[i]])) {
                errors.push("S6 requires a non-empty " + IDS[i] + " identity field.");
            }
        }
        if (m.package_name !== undefined &&
            (typeof m.package_name !== "string" || !/\S/.test(m.package_name))) {
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
    // Length prefixes prevent delimiter collisions without requiring native JSON.
    function encode(value) { value = String(value); return value.length + ":" + value; }
    function identity(m) {
        requireManifest(m);
        var value = "";
        for (var i = 0; i < IDS.length; i++) value += encode(m[IDS[i]]);
        return value;
    }
    // Verification key only, NOT a replacement for persisted S5 item comments.
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
        // Producer package names include V### and therefore normally differ across revisions.
        if (current.fps !== candidate.fps) errors.push("FPS changes are unsupported.");
        if (current.frames.start !== candidate.frames.start || current.frames.end !== candidate.frames.end ||
            current.frames.count !== candidate.frames.count) errors.push("Frame range/count changes are unsupported.");
        if (aspect(current) !== aspect(candidate)) errors.push("Pixel aspect changes are unsupported.");
        if (current.resolution.width !== candidate.resolution.width || current.resolution.height !== candidate.resolution.height) {
            warnings.push("Resolution changes require confirmation; source geometry can change appearance.");
        }
        var old = passMap(current), next = passMap(candidate), p;
        for (i = 0; i < current.passes.length; i++) {
            p = current.passes[i];
            if (!own(next, "$" + p.name)) {
                if (p.required !== false) errors.push("Previously required pass missing: " + p.name);
                else warnings.push("Removed optional pass will be retained unchanged: " + p.name);
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
        // Diagnostic rows retain input order; selection below never breaks ties by input order.
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
        // The adapter is trusted host code. Package data and public plan records are not.
        var methods = ["listManagedLayers", "validateManagedLayer", "readSource", "importReplacement",
            "validateReplacement", "swapManagedSource", "restoreManagedSource", "removeImportedReplacement"];
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
            // Callback must inspect live host type, project membership, comp/render folders,
            // persisted package metadata/tags, uniqueness, source path and conform FPS.
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
                // Import AND validate every replacement before changing any existing layer.
                for (j = 0; j < plan.actions.length; j++) {
                    var action = plan.actions[j], before = made.length;
                    var item = host.importReplacement(snapshot(plan.candidate), action.passName, track);
                    // Adapter must track immediately after allocation, before any fallible setup.
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
                    attempted.push(action); // Record BEFORE a host write can mutate then throw.
                    host.swapManagedSource(action.layer, replacements[j]);
                    if (host.readSource(action.layer) !== replacements[j]) throw new Error("Source swap verification failed.");
                }
                return {status: "applied", replaced: attempted.length};
            } catch (error) {
                for (j = attempted.length - 1; j >= 0; j--) {
                    try {
                        host.restoreManagedSource(attempted[j].layer, attempted[j].oldSource);
                        if (host.readSource(attempted[j].layer) !== attempted[j].oldSource) throw new Error("Source restoration not verified.");
                    } catch (restoreError) { failures.push("Restore " + attempted[j].passName + ": " + String(restoreError)); }
                }
                // Retain footage if any restoration failed: a layer may still reference it.
                var retained = failures.length ? made.length : 0;
                if (!failures.length) {
                    for (j = made.length - 1; j >= 0; j--) {
                        try {
                            if (host.removeImportedReplacement(made[j]) !== true) throw new Error("Removal not verified.");
                        } catch (removeError) {
                            retained++;
                            failures.push("Remove replacement: " + String(removeError));
                        }
                    }
                }
                poisoned = failures.length > 0;
                var report = new Error("Revision failed: " + String(error) +
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
