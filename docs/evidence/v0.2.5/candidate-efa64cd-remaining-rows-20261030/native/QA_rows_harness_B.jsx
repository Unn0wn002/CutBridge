#target aftereffects
// Native harness, phase B, the relaunch half of CutBridge row P3 (scratch script, copied into
// the evidence folder). Runs the unmodified CutBridge.jsx beside this file and presses its real panel buttons via
// notify("onClick"). Dialogs are answered by the harness: File.openDialog returns the queued manifest, confirm()
// returns true, alert() text is recorded. Single pass, no retries. Leftover CutBridge globals are recorded and
// cleared first. Phase B (QA_rows_harness_B.jsx) runs after a full After Effects quit and relaunch.
(function () {
    var here = new File($.fileName).parent.fsName;
    var work = new Folder(here).parent.fsName;
    function manifest(root, v) { return new File(work + "/" + root + "/QAPROJ_EP01_SC010_C014_T01_V00" + v + "/cutbridge.json"); }
    var V001 = manifest("cutbridge_exports", 1);
    var N1 = manifest("negative_n1", 1), N2 = manifest("negative_n2", 2), N3 = manifest("negative_n3", 2);
    var log = [], step = "init", openQueue = [], windows = [];

    function j(s) { return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "").replace(/\n/g, "\\n") + '"'; }
    function rec(kind, text) { log.push('{"step":' + j(step) + ',"kind":' + j(kind) + ',"text":' + j(text) + ',"t":' + j(new Date().toString()) + '}'); writeLog(false); }
    function writeLog(done) {
        var f = new File(work + "/harness-log-B.json"); f.encoding = "UTF-8"; f.open("w");
        f.write('{"done":' + (done ? "true" : "false") + ',"ae":' + j(app.version) + ',"entries":[\n' + log.join(",\n") + "\n]}\n"); f.close();
    }
    function writeFile(name, text) { var f = new File(work + "/" + name); f.encoding = "UTF-8"; f.open("w"); f.write(text); f.close(); }

    // Read-only project state dump, classified by typeName. Identical in phases A and B.
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
    function markers(comp) {
        var out = [];
        try { var m = comp.markerProperty; for (var k = 1; k <= m.numKeys; k++) out.push("[" + m.keyTime(k) + "," + j(m.keyValue(k).comment) + "]"); } catch (e) { out.push(j("<err " + e + ">")); }
        return "[" + out.join(",") + "]";
    }
    function dump(label) {
        step = label;
        var out = ['{"label":' + j(label) + ',"ae_version":' + j(app.version) + ',"items":['];
        for (var i = 1; i <= app.project.numItems; i++) {
            var it = app.project.item(i), tn = String(it.typeName);
            var r = '{"index":' + i + ',"typeName":' + j(tn) + ',"name":' + j(it.name) + ',"comment":' + j(it.comment);
            if (tn === "Composition") {
                r += ',"width":' + it.width + ',"height":' + it.height + ',"fps":' + it.frameRate + ',"duration":' + it.duration + ',"displayStartTime":' + it.displayStartTime + ',"markers":' + markers(it) + ',"layers":[';
                for (var l = 1; l <= it.numLayers; l++) {
                    var ly = it.layer(l), src = "", kind = kindOfLayer(ly), tr = ly.property("ADBE Transform Group");
                    try { src = ly.source ? ly.source.name : ""; } catch (e) { src = "<err>"; }
                    r += (l > 1 ? "," : "") + '{"index":' + l + ',"name":' + j(ly.name) + ',"kind":' + j(kind) + ',"threeD":' + (ly.threeDLayer === true) +
                        ',"source":' + j(src) + ',"comment":' + j(ly.comment) + ',"position":' + keys(tr.property("ADBE Position")) + '}';
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
        // P3 second half: after a full quit and relaunch, reopen the saved project and dump it with the same code.
        step = "09-reopen";
        var aep = new File(work + "/qa_p3.aep");
        if (!aep.exists) throw new Error("saved project missing");
        app.open(aep);
        var missing = 0;
        for (var i = 1; i <= app.project.numItems; i++) { var it = app.project.item(i); if (String(it.typeName) === "Footage" && it.footageMissing === true) missing++; }
        rec("note", "reopened " + aep.fsName + "; missing footage items=" + missing);
        dump("09-after-relaunch");

        // Reopen the CutBridge panel in the relaunched process and run QC+ on the reopened project.
        step = "clear-globals";
        var names = ["CutBridgeContract", "CutBridgeRevisionManager", "CutBridgeQCPlus", "CutBridgeLocalization"], seen = [];
        for (var g = 0; g < names.length; g++) { seen.push(names[g] + "=" + typeof $.global[names[g]]); $.global[names[g]] = undefined; }
        rec("globals-before-clear", seen.join(" "));
        var src = new File(here + "/CutBridge.jsx"); src.encoding = "UTF-8"; src.open("r"); var text = src.read(); src.close();
        step = "10-reopen-panel";
        eval("(function (alert, confirm, Window) {\n" + text + "\n$.global.CutBridgeContract = CutBridgeContract;\n})")(stubAlert, stubConfirm, CaptureWindow);
        openQueue.push(V001); press(0, "11-load-V001-after-relaunch");
        press(2, "12-qc-after-relaunch");
        dump("12-after-qc");
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    } catch (err) { rec("harness-error", err.toString() + " line " + err.line); }
    File.openDialog = realOpen;
    step = "end";
    for (var w = 0; w < windows.length; w++) { try { windows[w].close(); } catch (e) {} }
    writeLog(true);
}());
