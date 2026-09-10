/*
CutBridge S10 native After Effects spatial probe.

Research-only: this script is NOT part of the CutBridge production runtime.
It creates one uniquely named disposable comp, validates the S10 synthetic
projection fixture in the real AE host, removes the comp, then optionally saves
a JSON report through an explicit Save dialog.
*/
(function () {
    var PROBE_COMP = "__CUTBRIDGE_S10_SPATIAL_PROBE__";
    var WIDTH = 1920;
    var HEIGHT = 1080;
    var FPS = 24;
    var DURATION = 2;
    var ZOOM = 2666.6666666666665;
    var CAMERA_POSITION = [960, 540, -1000];
    var CAMERA_POI = [960, 540, 0];
    var TOLERANCE_PX = 0.05;
    var FIXTURES = [
        {name: "ORIGIN", ae: [960, 540, 0], expected: [960, 540]},
        {name: "X_PLUS", ae: [1060, 540, 0], expected: [1226.6666666666667, 540]},
        {name: "Y_PLUS", ae: [960, 540, 100], expected: [960, 540]},
        {name: "Z_PLUS", ae: [960, 440, 0], expected: [960, 273.3333333333333]},
        {name: "XYZ_PLUS", ae: [1060, 440, 100], expected: [1202.4242424242425, 297.57575757575756]}
    ];

    function abs(value) { return value < 0 ? -value : value; }
    function finite(value) { return typeof value === "number" && isFinite(value); }
    function copyArray(value) {
        var out = [], i;
        for (i = 0; value && i < value.length; i++) out.push(Number(value[i]));
        return out;
    }
    function safeError(error) {
        try { return error.toString(); }
        catch (_ignored) { return "Unprintable native AE error"; }
    }
    function escapeExpressionName(name) {
        return String(name).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
    }
    function cameraPointOfInterest(camera) {
        var transform = camera.property("ADBE Transform Group");
        var prop = transform ? transform.property("ADBE Anchor Point") : null;
        if (!prop && transform) prop = transform.property("Point of Interest");
        if (!prop) throw new Error("AE camera Point of Interest property is unavailable to the probe.");
        return prop;
    }
    function jsonEscape(text) {
        return String(text).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "\\r").replace(/\n/g, "\\n").replace(/\t/g, "\\t");
    }
    function stringify(value, indent, depth) {
        var i, keys, out, prefix, nextPrefix;
        indent = indent || "  ";
        depth = depth || 0;
        prefix = new Array(depth + 1).join(indent);
        nextPrefix = new Array(depth + 2).join(indent);
        if (value === null) return "null";
        if (typeof value === "string") return '"' + jsonEscape(value) + '"';
        if (typeof value === "number") return finite(value) ? String(value) : "null";
        if (typeof value === "boolean") return value ? "true" : "false";
        if (Object.prototype.toString.call(value) === "[object Array]") {
            if (!value.length) return "[]";
            out = [];
            for (i = 0; i < value.length; i++) out.push(nextPrefix + stringify(value[i], indent, depth + 1));
            return "[\n" + out.join(",\n") + "\n" + prefix + "]";
        }
        keys = [];
        for (i in value) if (Object.prototype.hasOwnProperty.call(value, i)) keys.push(i);
        keys.sort();
        if (!keys.length) return "{}";
        out = [];
        for (i = 0; i < keys.length; i++) {
            out.push(nextPrefix + '"' + jsonEscape(keys[i]) + '": ' + stringify(value[keys[i]], indent, depth + 1));
        }
        return "{\n" + out.join(",\n") + "\n" + prefix + "}";
    }
    function uniqueProbeName(base, index) { return "__CB_S10_" + base + "_" + index + "__"; }

    if (typeof app === "undefined" || !app) {
        throw new Error("CutBridge S10 AE probe must run inside Adobe After Effects.");
    }
    if (!app.project) {
        alert("CutBridge S10 probe requires an open After Effects project. It will only create and remove one disposable temporary comp.");
        return;
    }
    if (typeof confirm === "function" && !confirm(
        "CutBridge S10 spatial probe will create and remove one disposable temporary comp.\n\n" +
        "It will not modify existing project items. Continue?"
    )) return;

    var report = {
        schema: "cutbridge-s10-spatial-probe",
        schema_version: 1,
        host: "after-effects",
        host_version: String(app.version || "unknown"),
        host_build: (app.buildName !== undefined ? String(app.buildName) : null),
        os: (typeof $ !== "undefined" && $.os ? String($.os) : "unknown"),
        fixture: "front_camera_50mm_1920x1080",
        tolerance_px: TOLERANCE_PX,
        candidate_basis: [[1,0,0],[0,0,-1],[0,1,0]],
        candidate_zoom: ZOOM,
        camera: null,
        points: [],
        max_projection_error_px: null,
        pass: false,
        cleanup: false,
        errors: []
    };

    var comp = null;
    app.beginUndoGroup("CutBridge S10 Spatial Probe");
    try {
        comp = app.project.items.addComp(PROBE_COMP, WIDTH, HEIGHT, 1.0, DURATION, FPS);
        var camera = comp.layers.addCamera("__CB_S10_CAMERA__", [WIDTH / 2, HEIGHT / 2]);
        var cameraTransform = camera.property("ADBE Transform Group");
        var cameraPosition = cameraTransform.property("ADBE Position");
        var cameraPoi = cameraPointOfInterest(camera);
        var cameraOptions = camera.property("ADBE Camera Options Group");
        var cameraZoom = cameraOptions ? cameraOptions.property("ADBE Camera Zoom") : null;
        if (!cameraPosition || !cameraPoi || !cameraZoom) throw new Error("AE camera Position / Point of Interest / Zoom properties are unavailable.");

        cameraPosition.setValue(CAMERA_POSITION);
        cameraPoi.setValue(CAMERA_POI);
        cameraZoom.setValue(ZOOM);
        report.camera = {
            position: copyArray(cameraPosition.value),
            point_of_interest: copyArray(cameraPoi.value),
            zoom: Number(cameraZoom.value)
        };

        var maxError = 0.0;
        for (var i = 0; i < FIXTURES.length; i++) {
            var fixture = FIXTURES[i];
            var source = comp.layers.addNull(DURATION);
            source.name = uniqueProbeName(fixture.name, i);
            source.threeDLayer = true;
            source.property("ADBE Transform Group").property("ADBE Position").setValue(fixture.ae);

            var observer = comp.layers.addNull(DURATION);
            observer.name = uniqueProbeName("PROJECTED_" + fixture.name, i);
            observer.threeDLayer = false;
            var observedPosition = observer.property("ADBE Transform Group").property("ADBE Position");
            var sourceName = escapeExpressionName(source.name);
            observedPosition.expression = 'var s=thisComp.layer("' + sourceName + '"); s.toComp(s.anchorPoint);';
            var observed = copyArray(observedPosition.value);
            if (observed.length < 2 || !finite(observed[0]) || !finite(observed[1])) {
                throw new Error(fixture.name + ": AE toComp probe did not return finite 2D coordinates.");
            }
            var dx = observed[0] - fixture.expected[0];
            var dy = observed[1] - fixture.expected[1];
            var error = Math.sqrt(dx * dx + dy * dy);
            if (error > maxError) maxError = error;
            report.points.push({
                name: fixture.name,
                ae_world_candidate: fixture.ae,
                expected_comp_px: fixture.expected,
                observed_comp_px: [observed[0], observed[1]],
                delta_px: [dx, dy],
                error_px: error,
                pass: error <= TOLERANCE_PX
            });
        }
        report.max_projection_error_px = maxError;
        report.pass = maxError <= TOLERANCE_PX;
    } catch (probeError) {
        report.errors.push(safeError(probeError));
        report.pass = false;
    } finally {
        if (comp) {
            try {
                comp.remove();
                report.cleanup = true;
            } catch (cleanupError) {
                report.errors.push("Disposable probe comp cleanup failed: " + safeError(cleanupError));
                report.cleanup = false;
                report.pass = false;
            }
        }
        app.endUndoGroup();
    }

    var text = stringify(report, "  ", 0);
    var output = null;
    try { output = File.saveDialog("Save CutBridge S10 AE spatial probe report", "JSON:*.json"); }
    catch (dialogError) { report.errors.push("Save dialog failed: " + safeError(dialogError)); text = stringify(report, "  ", 0); }

    if (output) {
        try {
            output.encoding = "UTF-8";
            if (!output.open("w")) throw new Error("Could not open selected report path for writing.");
            output.write(text);
            output.close();
            alert("CutBridge S10 probe " + (report.pass ? "PASS" : "FAIL") + ".\nReport saved to:\n" + output.fsName);
        } catch (writeError) {
            try { if (output.opened) output.close(); } catch (_closeIgnored) {}
            alert("CutBridge S10 probe completed but report save failed.\n\n" + safeError(writeError) + "\n\n" + text);
        }
    } else {
        alert("CutBridge S10 probe " + (report.pass ? "PASS" : "FAIL") + ". No report file was saved.\n\n" + text);
    }
})();
