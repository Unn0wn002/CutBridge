#target aftereffects
// Native retest harness for CutBridge rows P5/N4/N5/N6 (scratch script, copied into the evidence folder).
// Runs the unmodified CutBridge.jsx from this folder and presses its real panel buttons via notify("onClick").
// Dialogs are answered by the harness: File.openDialog returns the queued manifest, confirm() returns true,
// alert() text is recorded. alert/confirm/Window are shadowed as function parameters because AE 26.5 ignores
// reassignment of the global alert. Single pass, no retries: every step runs once and is logged.
// Lessons from the first 2026-10-30 run are built in: CutBridge globals left in this AE process are recorded
// and cleared first so the runtime files beside this script are the ones loaded, CutBridgeContract is
// re-exported to $.global as a normal run has it, and the state dump is inline and classifies by typeName.
(function () {
    var here = new File($.fileName).parent.fsName;
    var work = new Folder(here).parent.fsName;
    var exportsRoot = work + "/cutbridge_exports/";
    function pkg(v) { return new File(exportsRoot + "QAPROJ_EP01_SC010_C014_T01_V00" + v + "/cutbridge.json"); }
    var V001 = pkg(1), V002 = pkg(2), V003 = pkg(3);
    var log = [], step = "init", openQueue = [], windows = [];

    function j(s) { return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "").replace(/\n/g, "\\n") + '"'; }
    function rec(kind, text) { log.push('{"step":' + j(step) + ',"kind":' + j(kind) + ',"text":' + j(text) + ',"t":' + j(new Date().toString()) + '}'); writeLog(false); }
    function writeLog(done) {
        var f = new File(work + "/harness-log.json"); f.encoding = "UTF-8"; f.open("w");
        f.write('{"done":' + (done ? "true" : "false") + ',"ae":' + j(app.version) + ',"entries":[\n' + log.join(",\n") + "\n]}\n"); f.close();
    }
    function writeFile(name, text) { var f = new File(work + "/" + name); f.encoding = "UTF-8"; f.open("w"); f.write(text); f.close(); }

    // Read-only project state dump, classified by typeName.
    function kindOfLayer(ly) {
        if (ly.matchName === "ADBE Camera Layer") return "Camera";
        if (ly.nullLayer === true) return "Null";
        if (ly.matchName === "ADBE AV Layer") return "AV";
        return "Other:" + ly.matchName;
    }
    function keys(prop) {
        var out = [];
        try {
            if (prop.numKeys > 0) { for (var k = 1; k <= prop.numKeys; k++) { var v = prop.keyValue(k); out.push("[" + prop.keyTime(k) + "," + (v instanceof Array ? v.join(",") : v) + "]"); } }
            else { var s = prop.value; out.push('["static",' + (s instanceof Array ? s.join(",") : s) + "]"); }
        } catch (e) { out.push(j("<err " + e + ">")); }
        return "[" + out.join(",") + "]";
    }
    function dump(label) {
        step = label;
        var out = ['{"label":' + j(label) + ',"ae_version":' + j(app.version) + ',"items":['];
        for (var i = 1; i <= app.project.numItems; i++) {
            var it = app.project.item(i), tn = String(it.typeName);
            var r = '{"index":' + i + ',"typeName":' + j(tn) + ',"name":' + j(it.name) + ',"comment":' + j(it.comment);
            if (tn === "Composition") {
                r += ',"width":' + it.width + ',"height":' + it.height + ',"fps":' + it.frameRate + ',"duration":' + it.duration + ',"displayStartTime":' + it.displayStartTime + ',"layers":[';
                for (var l = 1; l <= it.numLayers; l++) {
                    var ly = it.layer(l), src = "", kind = kindOfLayer(ly), tr = ly.property("ADBE Transform Group");
                    try { src = ly.source ? ly.source.name : ""; } catch (e) { src = "<err>"; }
                    r += (l > 1 ? "," : "") + '{"index":' + l + ',"name":' + j(ly.name) + ',"kind":' + j(kind) + ',"threeD":' + (ly.threeDLayer === true) +
                        ',"source":' + j(src) + ',"comment":' + j(ly.comment) + ',"position":' + keys(tr.property("ADBE Position"));
                    if (kind === "Camera") {
                        var poi = tr.property("ADBE Anchor Point"), orient = tr.property("ADBE Orientation");
                        r += ',"pointOfInterest":' + (poi ? keys(poi) : "null") + ',"orientation":' + (orient ? keys(orient) : "null") +
                            ',"zoom":' + keys(ly.property("ADBE Camera Options Group").property("ADBE Camera Zoom"));
                    }
                    r += '}';
                }
                r += "]";
            } else if (tn === "Footage") {
                var path = ""; try { path = it.mainSource.file ? it.mainSource.file.fsName : ""; } catch (e1) {}
                r += ',"file":' + j(path) + ',"missing":' + (it.footageMissing === true);
            }
            out.push((i > 1 ? "," : "") + r + "}");
        }
        out.push("]}\n");
        writeFile("state-" + label + ".json", out.join(""));
        rec("dump", label);
    }

    // P5 projection parity: AE's own projection of QA_NULL through the active camera, read with a temporary
    // expression probe (a text layer, which adds no project item) that is removed again.
    function probeProjection(label) {
        step = label;
        var comp = managedComp(), rows = [];
        if (!comp) { rec("note", "C014_COMP not found"); return; }
        var probe = comp.layers.addText("QA_PROJ_PROBE"), pos = probe.property("ADBE Transform Group").property("ADBE Position");
        pos.expression = 'var L = thisComp.layer("QA_NULL"); L.toComp(L.anchorPoint);';
        for (var i = 0; i < 3; i++) {
            var t = i / comp.frameRate, v = pos.valueAtTime(t, false);
            rows.push('{"ae_frame_index":' + i + ',"time":' + t + ',"x_px":' + v[0] + ',"y_px":' + v[1] + '}');
        }
        var err = pos.expressionError;
        probe.remove();
        writeFile("ae_projection-" + label + ".json", "[\n" + rows.join(",\n") + "\n]\n");
        rec("projection", rows.join(" ") + (err ? " expressionError=" + err : ""));
    }

    var stubAlert = function (m) { rec("alert", m); };
    var stubConfirm = function (m) { rec("confirm(true)", m); return true; };
    var RealWindow = Window;
    var CaptureWindow = function (a, b, c, d) { var w = new RealWindow(a, b, c, d); windows.push(w); return w; };
    var realOpen = File.openDialog;
    File.openDialog = function (title) { var f = openQueue.shift(); rec("openDialog", title + " -> " + (f ? f.fsName : "<none queued>")); return f || null; };

    function buttons(container, out) {
        for (var i = 0; i < container.children.length; i++) {
            var c = container.children[i];
            if (c.type === "button" && c.text !== "?") out.push(c);
            if (c.children && c.children.length) buttons(c, out);
        }
        return out;
    }
    function press(index, label) { step = label; var b = buttons(windows[0], [])[index]; rec("press", b.text); try { b.notify("onClick"); } catch (e) { rec("exception", e.toString()); } }
    function managedComp() { for (var i = 1; i <= app.project.numItems; i++) { var it = app.project.item(i); if (String(it.typeName) === "Composition" && it.name === "C014_COMP") return it; } return null; }

    try {
        if (!V001.exists || !V002.exists || !V003.exists) throw new Error("packages missing");
        step = "clear-globals";
        var names = ["CutBridgeContract", "CutBridgeRevisionManager", "CutBridgeQCPlus", "CutBridgeLocalization"], seen = [];
        for (var g = 0; g < names.length; g++) { seen.push(names[g] + "=" + typeof $.global[names[g]]); $.global[names[g]] = undefined; }
        rec("globals-before-clear", seen.join(" "));
        app.newProject();
        var src = new File(here + "/CutBridge.jsx"); src.encoding = "UTF-8"; src.open("r"); var text = src.read(); src.close();
        step = "start-panel";
        eval("(function (alert, confirm, Window) {\n" + text + "\n$.global.CutBridgeContract = CutBridgeContract;\n})")(stubAlert, stubConfirm, CaptureWindow);
        rec("panel-buttons", (function () { var b = buttons(windows[0], []), t = []; for (var i = 0; i < b.length; i++) t.push(b[i].text); return t.join(" | "); })());
        dump("00-empty");

        // P5 + N4: load V001 (LINE frames removed), Build, QC+, projection parity
        openQueue.push(V001); press(0, "01-load-V001");
        press(1, "02-build-V001"); dump("02-after-build");
        press(2, "03-qc-V001");
        probeProjection("03b-after-build");

        // N6 Null: an untagged artist Null with the managed null's name, then Build again
        step = "04-add-artist-null";
        var comp = managedComp(), artist = null;
        if (comp) { artist = comp.layers.addNull(comp.duration); artist.name = "QA_NULL"; artist.comment = ""; rec("note", "artist null added, layers=" + comp.numLayers); }
        dump("04-before-rebuild-null");
        press(1, "05-rebuild-with-artist-null"); dump("05-after-rebuild-null");
        step = "05b-remove-artist-null";
        if (artist) { artist.remove(); rec("note", "artist null removed, layers=" + comp.numLayers); }

        // N6 Camera: an untagged artist camera with the managed camera's name, then Build again
        step = "06-add-artist-camera";
        var artistCam = null;
        if (comp) { artistCam = comp.layers.addCamera("Camera", [comp.width / 2, comp.height / 2]); artistCam.comment = ""; rec("note", "artist camera added, layers=" + comp.numLayers); }
        dump("06-before-rebuild-camera");
        press(1, "07-rebuild-with-artist-camera"); dump("07-after-rebuild-camera");
        step = "07b-remove-artist-camera";
        if (artistCam) { artistCam.remove(); rec("note", "artist camera removed, layers=" + comp.numLayers); }
        dump("08-restored");

        // N5: skip V002 (V001 -> V003), then an older (V002) and the same (V003) candidate
        openQueue.push(V003); press(3, "09-revision-V001-to-V003"); dump("09-after-revision-V003");
        press(2, "10-qc-after-revision");
        openQueue.push(V002); press(3, "11-revision-V003-to-V002-older"); dump("11-after-older-attempt");
        openQueue.push(V003); press(3, "12-revision-V003-to-V003-same"); dump("12-after-same-attempt");
        probeProjection("13-after-revision");
    } catch (err) { rec("harness-error", err.toString() + " line " + err.line); }
    File.openDialog = realOpen;
    step = "end";
    for (var w = 0; w < windows.length; w++) { try { windows[w].close(); } catch (e) {} }
    writeLog(true);
    app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}());
