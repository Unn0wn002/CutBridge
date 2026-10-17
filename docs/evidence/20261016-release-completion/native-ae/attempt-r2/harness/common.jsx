var CB = (function () {
    var api = {}, originalAlert = alert, originalConfirm = confirm, originalDialog = File.openDialog;
    function json(value) {
        if (value === null || value === undefined) return "null";
        if (typeof value === "number") return isFinite(value) ? String(value) : "null";
        if (typeof value === "boolean") return String(value);
        if (typeof value === "string") return '"' + value.replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "\\r").replace(/\n/g, "\\n").replace(/\t/g, "\\t") + '"';
        var parts = [], key;
        if (value instanceof Array) {
            for (key = 0; key < value.length; key++) parts.push(json(value[key]));
            return "[" + parts.join(",") + "]";
        }
        for (key in value) if (value.hasOwnProperty(key)) parts.push(json(key) + ":" + json(value[key]));
        return "{" + parts.join(",") + "}";
    }
    function read(file) {
        file = file instanceof File ? file : new File(file);
        file.encoding = "UTF-8";
        if (!file.open("r")) throw insufficient("Required input cannot be read: " + file.fsName);
        var text = file.read(); file.close(); return text;
    }
    function parse(text) {
        if (typeof JSON !== "undefined" && JSON.parse) return JSON.parse(text);
        // Only reviewed orchestration JSON uses this fallback. Candidate package
        // manifests are parsed by the unchanged installed CutBridge parser.
        return eval("(" + text + ")");
    }
    function mkdir(path) {
        var folder = path instanceof Folder ? path : new Folder(path);
        if (folder.exists) return folder;
        if (folder.parent && !folder.parent.exists) mkdir(folder.parent);
        if (!folder.create()) throw insufficient("Output directory cannot be created: " + folder.fsName);
        return folder;
    }
    function save(path, value) {
        var file = new File(path); mkdir(file.parent); file.encoding = "UTF-8";
        if (!file.open("w")) throw insufficient("Output cannot be written: " + file.fsName);
        file.write(json(value)); file.close();
    }
    function insufficient(message) { var error = Error(message); error.infrastructure = true; return error; }
    var config = parse(read("C:/NativeAEInput/config.json"));
    mkdir(config.output_root);
    var metadata = parse(read(config.candidate_metadata));
    var candidateSha = metadata.sha || metadata.candidate_sha;
    if (!candidateSha || !/^[a-f0-9]{40}$/.test(candidateSha)) throw insufficient("Exact candidate SHA is unavailable");
    var report = {status: "IN_PROGRESS", candidate_sha: candidateSha, host_version: app.version, os: $.os,
        temp: $.getenv("TEMP"), config: config, checks: [], alerts: [], confirmations: [],
        scope: config.scope, gui_visual_inspection: "NOT_EXECUTED", S14B: "NOT_EXECUTED"};
    try { report.build_name = app.buildName; report.build_number = app.buildNumber; } catch (_) {}
    function flush() { if (api.phase) save(config.output_root + "/" + api.phase + ".json", report); }
    function check(name, passed, details) {
        report.checks.push({name: name, passed: passed === true, details: details}); flush();
        if (passed !== true) throw Error("Check failed: " + name);
    }
    function near(actual, expected) {
        if (actual instanceof Array && expected instanceof Array) {
            if (actual.length !== expected.length) return false;
            for (var i = 0; i < actual.length; i++) if (!near(actual[i], expected[i])) return false;
            return true;
        }
        return Math.abs(actual - expected) < 0.001;
    }
    function findManifestPaths(folder, paths) {
        if (!folder.exists) return;
        var entries = folder.getFiles();
        for (var i = 0; i < entries.length; i++) {
            if (entries[i] instanceof Folder) findManifestPaths(entries[i], paths);
            else if (String(entries[i].name).toLowerCase() === "cutbridge.json") paths.push(entries[i].fsName);
        }
    }
    function loadRuntime() {
        if (config.expected_host_prefix && String(app.version).indexOf(config.expected_host_prefix) !== 0) throw insufficient("Unexpected AE host version: " + app.version);
        var required = ["CutBridge.jsx", "revision_manager.js", "qc_plus.js", "localization.js"];
        for (var i = 0; i < required.length; i++) if (!new File(config.runtime_directory + "/" + required[i]).exists) throw insufficient("Installed packaged runtime/sidecar missing: " + required[i]);
        if (!new File(config.installation_metadata).exists) throw insufficient("ZIP/runtime hash installation metadata is unavailable");
        report.installation = parse(read(config.installation_metadata));
        try { app.settings.saveSetting("CutBridge", "ui_locale", "EN"); } catch (e) { throw insufficient("Cannot set isolated AE locale: " + e); }
        alert = function (message) { report.alerts.push(String(message)); flush(); };
        $.evalFile(new File(config.runtime_directory + "/CutBridge.jsx"));
        if (typeof CutBridgeContract === "undefined" || typeof CutBridgeContract.buildComp !== "function") throw insufficient("Installed CutBridge public API did not initialize");
        $.global.CutBridgeContract = CutBridgeContract;
        report.harness_global_api_alias = true;
        var paths = config.manifests.slice(0), byVersion = {};
        if (!paths.length) findManifestPaths(new Folder(config.package_root), paths);
        for (i = 0; i < paths.length; i++) {
            var manifest = CutBridgeContract.parseJSON(read(paths[i])), version = manifest.version;
            if (version >= 1 && version <= 3) {
                if (byVersion[version]) throw insufficient("Ambiguous Blender package version V00" + version + "; configure exact manifest paths");
                byVersion[version] = {path: paths[i], manifest: manifest};
            }
        }
        for (i = 1; i <= 3; i++) if (!byVersion[i]) throw insufficient("Blender-produced V00" + i + " package is unavailable");
        api.packages = byVersion;
        report.package_inputs = byVersion;
        flush();
    }
    function projectPath(version) { return config.output_root + "/artist-V00" + version + ".aep"; }
    function safeClose() {
        if (!app.project) return;
        if (app.project.numItems && (!app.project.file || normalize(app.project.file.fsName).indexOf(normalize(config.output_root) + "/") !== 0)) throw insufficient("Refusing to close a project outside this disposable campaign");
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    }
    function fresh() { safeClose(); app.newProject(); }
    function normalize(path) { return String(path).replace(/\\/g, "/").toLowerCase(); }
    function comp() {
        var manifest = CutBridgeContract.getState().manifest, tag = CutBridgeContract.managedTag("comp", manifest, manifest.ae.comp_name), found = null;
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (item instanceof CompItem && item.comment === tag) { if (found) throw Error("Duplicate managed comp"); found = item; }
        }
        if (!found) throw Error("Managed comp unavailable");
        CutBridgeContract.getState().comp = found; return found;
    }
    function openSaved(version) {
        var file = new File(projectPath(version));
        if (!file.exists) throw insufficient("Saved campaign project unavailable: " + file.fsName);
        safeClose(); app.open(file); CutBridgeContract.loadManifest(api.packages[version].path); return comp();
    }
    function ids() { var result = []; for (var i = 1; i <= app.project.numItems; i++) result.push(app.project.item(i).id); return result; }
    function value(value) {
        if (value instanceof Shape) return {vertices: value.vertices, inTangents: value.inTangents, outTangents: value.outTangents, closed: value.closed};
        if (value instanceof Array || typeof value === "number" || typeof value === "string" || typeof value === "boolean") return value;
        return String(value);
    }
    function propertySnapshot(prop) {
        if (!prop) return null;
        var result = {name: prop.name, matchName: prop.matchName};
        if (prop.propertyType !== PropertyType.PROPERTY) {
            result.properties = [];
            for (var i = 1; i <= prop.numProperties; i++) result.properties.push(propertySnapshot(prop.property(i)));
            return result;
        }
        if (prop.propertyValueType === PropertyValueType.NO_VALUE) { result.valueType = "NO_VALUE"; return result; }
        result.value = value(prop.value); result.keys = [];
        for (var k = 1; k <= prop.numKeys; k++) result.keys.push({time: prop.keyTime(k), value: value(prop.keyValue(k)), inType: String(prop.keyInInterpolationType(k)), outType: String(prop.keyOutInterpolationType(k))});
        if (prop.canSetExpression) { result.expression = prop.expression; result.expressionEnabled = prop.expressionEnabled; }
        return result;
    }
    function layerSnapshot(layer, includeSource) {
        var result = {id: layer.id, index: layer.index, name: layer.name, parent: layer.parent ? layer.parent.id : null,
            enabled: layer.enabled, shy: layer.shy, locked: layer.locked, startTime: layer.startTime, inPoint: layer.inPoint,
            outPoint: layer.outPoint, stretch: layer.stretch, threeDLayer: layer.threeDLayer,
            transform: propertySnapshot(layer.property("ADBE Transform Group")),
            effects: propertySnapshot(layer.property("ADBE Effect Parade")), masks: propertySnapshot(layer.property("ADBE Mask Parade"))};
        if (includeSource) { result.comment = layer.comment; result.source = layer.source ? layer.source.id : null; }
        return result;
    }
    function preservation() {
        var c = comp(), layers = [], m = CutBridgeContract.getState().manifest;
        for (var i = 1; i <= c.numLayers; i++) {
            var layer = c.layer(i);
            // Do not query unsafe named Camera POI properties or claim unsupported 3D channels.
            if (layer instanceof CameraLayer || layer.nullLayer) continue;
            layers.push(layerSnapshot(layer, layer.name.indexOf("Artist ") === 0));
        }
        var unrelated = [];
        for (i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (item.name.indexOf("Unrelated ") === 0) unrelated.push({id: item.id, name: item.name, comment: item.comment, parent: item.parentFolder.id});
        }
        return {comp: {id: c.id, width: c.width, height: c.height, pixelAspect: c.pixelAspect, frameRate: c.frameRate, duration: c.duration},
            root_note: c.parentFolder.parentFolder.comment, layers: layers, unrelated: unrelated};
    }
    function projectSnapshot() {
        var items = [], layers = [], c = comp();
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            items.push({id: item.id, name: item.name, comment: item.comment, parent: item.parentFolder.id});
        }
        for (i = 1; i <= c.numLayers; i++) {
            var layer = c.layer(i);
            layers.push({id: layer.id, index: layer.index, name: layer.name, comment: layer.comment, source: layer.source ? layer.source.id : null});
        }
        return {items: items, layers: layers, artist: preservation()};
    }
    function qc() {
        var result = CutBridgeContract.runQC();
        if (!result || !result.report || !result.report.summary) throw Error("QC returned no inspectable report");
        return result;
    }
    function build(label) {
        var result = CutBridgeContract.buildComp();
        check(label, !!(result && result.success), result ? {success: result.success, error: result.error, warnings: result.warnings} : null);
        var q = qc(); check(label + " QC has no errors", q.report.summary.ERROR === 0, q); return result;
    }
    function handoff() {
        var m = CutBridgeContract.getState().manifest, h = m.handoff_3d, c = comp(), checks = [];
        if (!h || !h.camera || !h.nulls || !h.nulls.length) throw insufficient("Representative Camera/Null fixture unavailable");
        var camera = c.layer(h.camera.name), transform = camera.property("ADBE Transform Group");
        var position = transform.property("ADBE Position"), poi = transform.property(1), zoom = camera.property("ADBE Camera Options Group").property("ADBE Camera Zoom");
        check("native Camera layer", camera instanceof CameraLayer);
        for (var i = 0; i < h.camera.samples.length; i++) {
            var sample = h.camera.samples[i], expectedPOI = [sample.position[0] + sample.forward[0] * 1000, sample.position[1] + sample.forward[1] * 1000, sample.position[2] + sample.forward[2] * 1000];
            check("Camera position/POI/zoom sample " + i, near(position.valueAtTime(sample.time, false), sample.position) && near(poi.valueAtTime(sample.time, false), expectedPOI) && near(zoom.valueAtTime(sample.time, false), sample.ae_zoom));
        }
        for (i = 0; i < h.nulls.length; i++) {
            var n = h.nulls[i], layer = c.layer(n.name), t = layer.property("ADBE Transform Group");
            check("native 3D Null " + n.name, !!(layer.nullLayer && layer.threeDLayer));
            for (var k = 0; k < n.samples.length; k++) {
                sample = n.samples[k];
                check("Null position/scale sample " + n.name + "/" + k, near(t.property("ADBE Position").valueAtTime(sample.time, false), sample.position) && near(t.property("ADBE Scale").valueAtTime(sample.time, false), [sample.scale[0] * 100, sample.scale[1] * 100, sample.scale[2] * 100]));
            }
        }
    }
    function findButton(control) {
        if (control.type === "button" && String(control.text) === "Update Revision") return control;
        var children = control.children || [];
        for (var i = 0; i < children.length; i++) { var found = findButton(children[i]); if (found) return found; }
        return null;
    }
    function revision(path, expectedVersion, expectConfirmation) {
        var palette = Window.find("palette", "CutBridge"), button = palette ? findButton(palette) : null;
        if (!button || typeof button.onClick !== "function") throw insufficient("Actual installed revision ScriptUI button is unavailable");
        var dialogCalls = 0, confirmsBefore = report.confirmations.length, alertsBefore = report.alerts.length;
        var injectedDialog = function () { dialogCalls++; return new File(path); };
        try {
            File.openDialog = injectedDialog;
            if (File.openDialog !== injectedDialog) throw insufficient("Native File.openDialog cannot be intercepted without modifying runtime bytes");
            confirm = function (message) { report.confirmations.push(String(message)); flush(); return true; };
            button.onClick();
        } finally { File.openDialog = originalDialog; confirm = originalConfirm; }
        check("revision selected exact fixture", dialogCalls === 1, path);
        var confirmations = report.confirmations.slice(confirmsBefore), alerts = report.alerts.slice(alertsBefore);
        check("revision confirmation boundary", expectConfirmation ? confirmations.length === 1 : confirmations.length === 0, confirmations);
        check("revision resulting version", CutBridgeContract.getState().manifest.version === expectedVersion, {expected: expectedVersion, actual: CutBridgeContract.getState().manifest.version, alerts: alerts});
        return {alerts: alerts, confirmations: confirmations};
    }
    function copyTree(source, target) {
        mkdir(target); var children = source.getFiles();
        for (var i = 0; i < children.length; i++) {
            var destination = target.fsName + "/" + File.decode(children[i].name);
            if (children[i] instanceof Folder) copyTree(children[i], new Folder(destination));
            else if (!children[i].copy(destination)) throw insufficient("Fixture file copy failed: " + children[i].fsName);
        }
    }
    function variant(name, version, mutate) {
        var sourcePackage = api.packages[3], destination = new Folder(config.output_root + "/fixtures/" + name);
        if (destination.exists) throw insufficient("Use fresh fixture output: " + destination.fsName);
        copyTree(new File(sourcePackage.path).parent, destination);
        var m = CutBridgeContract.parseJSON(read(sourcePackage.path));
        m.version = version; m.version_label = "V" + CutBridgeContract.zeroPad(version, 3); m.package_name = m.package_name.replace(/_V\d+$/, "_V" + CutBridgeContract.zeroPad(version, 3));
        if (mutate) mutate(m);
        var errors = CutBridgeContract.validateManifest(m);
        if (errors.length) throw insufficient("Derived negative fixture is not contract-valid: " + errors.join("; "));
        var manifestPath = destination.fsName + "/cutbridge.json"; save(manifestPath, m);
        if (!report.derived_fixtures) report.derived_fixtures = [];
        report.derived_fixtures.push({name: name, source_manifest: sourcePackage.path, derived_manifest: manifestPath, version: version}); flush();
        return {path: manifestPath, manifest: m};
    }
    function execute(phase, task) {
        api.phase = phase; report.phase = phase; flush();
        try { loadRuntime(); task(); report.status = "PASS"; }
        catch (error) { report.status = error.infrastructure ? "INSUFFICIENT EVIDENCE" : "FAIL"; report.error = String(error); report.line = error.line; }
        finally { alert = originalAlert; confirm = originalConfirm; File.openDialog = originalDialog; flush(); }
    }
    api.config = config; api.report = report; api.json = json; api.read = read; api.save = save; api.parse = parse;
    api.check = check; api.insufficient = insufficient; api.execute = execute; api.projectPath = projectPath;
    api.openSaved = openSaved; api.fresh = fresh; api.comp = comp; api.ids = ids; api.preservation = preservation;
    api.snapshot = projectSnapshot; api.build = build; api.qc = qc; api.handoff = handoff; api.revision = revision;
    api.variant = variant; api.equal = function (a, b) { return json(a) === json(b); };
    return api;
}());
