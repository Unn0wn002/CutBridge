#target aftereffects
// Native QA harness for CutBridge rows P5/N4/N5/N6 (scratch script, not part of the repository).
// Runs the unmodified CutBridge.jsx from this folder and presses its real panel buttons via notify("onClick").
// Dialogs are answered by the harness: File.openDialog returns the queued manifest, confirm() returns true,
// alert() text is recorded. alert/confirm/Window are shadowed as function parameters because AE 26.5 ignores
// reassignment of the global alert. Every dialog and each step is logged to harness-log.json.
(function () {
    var here = new File($.fileName).parent.fsName;
    var work = new Folder(here).parent.fsName;
    var exportsRoot = work + "/cutbridge_exports/";
    var V001 = new File(exportsRoot + "QAPROJ_EP01_SC010_C014_T01_V001/cutbridge.json");
    var V003 = new File(exportsRoot + "QAPROJ_EP01_SC010_C014_T01_V003/cutbridge.json");
    var log = [], step = "init", openQueue = [], windows = [];

    function j(s) { return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "").replace(/\n/g, "\\n") + '"'; }
    function rec(kind, text) { log.push('{"step":' + j(step) + ',"kind":' + j(kind) + ',"text":' + j(text) + ',"t":' + j(new Date().toString()) + '}'); writeLog(false); }
    function writeLog(done) {
        var f = new File(work + "/harness-log.json"); f.encoding = "UTF-8"; f.open("w");
        f.write('{"done":' + (done ? "true" : "false") + ',"ae":' + j(app.version) + ',"entries":[\n' + log.join(",\n") + "\n]}\n"); f.close();
    }
    // Read-only project state dump, inlined: the same logic $.evalFile'd from here misreported item types.
    function kindOfLayer(ly) {
        if (ly.matchName === "ADBE Camera Layer") return "Camera";
        if (ly.nullLayer === true) return "Null";
        if (ly.matchName === "ADBE AV Layer") return "AV";
        return "Other:" + ly.matchName;
    }
    function positions(ly) {
        var out = [];
        try {
            var p = ly.property("ADBE Transform Group").property("ADBE Position");
            if (p.numKeys > 0) { for (var k = 1; k <= p.numKeys; k++) out.push("[" + p.keyTime(k) + "," + p.keyValue(k).join(",") + "]"); }
            else out.push('["static",' + p.value.join(",") + "]");
        } catch (e) { out.push(j("<err " + e + ">")); }
        return "[" + out.join(",") + "]";
    }
    function dump(label) {
        step = label;
        var out = ['{"label":' + j(label) + ',"ae_version":' + j(app.version) + ',"items":['];
        for (var i = 1; i <= app.project.numItems; i++) {
            var it = app.project.item(i), kind = (it instanceof CompItem) ? "Comp" : (it instanceof FolderItem) ? "Folder" : (it instanceof FootageItem) ? "Footage" : "Other";
            var r = '{"index":' + i + ',"kind":' + j(kind) + ',"typeName":' + j(it.typeName) + ',"name":' + j(it.name) + ',"comment":' + j(it.comment);
            if (it instanceof CompItem) {
                r += ',"width":' + it.width + ',"height":' + it.height + ',"fps":' + it.frameRate + ',"duration":' + it.duration + ',"layers":[';
                for (var l = 1; l <= it.numLayers; l++) {
                    var ly = it.layer(l), src = "";
                    try { src = ly.source ? ly.source.name : ""; } catch (e) { src = "<err>"; }
                    r += (l > 1 ? "," : "") + '{"index":' + l + ',"name":' + j(ly.name) + ',"kind":' + j(kindOfLayer(ly)) + ',"threeD":' + (ly.threeDLayer === true) + ',"source":' + j(src) + ',"comment":' + j(ly.comment) + ',"position":' + positions(ly) + '}';
                }
                r += "]";
            } else if (it instanceof FootageItem) {
                var path = ""; try { path = it.mainSource.file ? it.mainSource.file.fsName : ""; } catch (e1) {}
                r += ',"file":' + j(path) + ',"missing":' + (it.footageMissing === true);
            }
            out.push((i > 1 ? "," : "") + r + "}");
        }
        out.push("]}\n");
        var f = new File(work + "/state-" + label + ".json"); f.encoding = "UTF-8"; f.open("w"); f.write(out.join("")); f.close();
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
    function managedComp() { for (var i = 1; i <= app.project.numItems; i++) { var it = app.project.item(i); if (it instanceof CompItem && it.name === "C014_COMP") return it; } return null; }

    try {
        if (!V001.exists || !V003.exists) throw new Error("packages missing");
        app.newProject();
        var src = new File(here + "/CutBridge.jsx"); src.encoding = "UTF-8"; src.open("r"); var text = src.read(); src.close();
        step = "start-panel";
        // CutBridge.jsx declares `var CutBridgeContract` at top level, which is global in a normal run and is
        // looked up globally by revision_manager.js. Inside this wrapper it would be local, so re-export it.
        eval("(function (alert, confirm, Window) {\n" + text + "\n$.global.CutBridgeContract = CutBridgeContract;\n})")(stubAlert, stubConfirm, CaptureWindow);
        rec("panel-buttons", (function () { var b = buttons(windows[0], []), t = []; for (var i = 0; i < b.length; i++) t.push(b[i].text); return t.join(" | "); })());
        dump("00-empty");

        // P5 + N4: load V001 (LINE frames removed), Build, QC+
        openQueue.push(V001); press(0, "01-load-V001");
        press(1, "02-build-V001"); dump("02-after-build");
        press(2, "03-qc-V001");

        // N6: an untagged artist Null with the managed null's name, then Build again
        step = "04-add-artist-null";
        var comp = managedComp(), artist = null;
        if (comp) { app.beginUndoGroup("QA artist null"); artist = comp.layers.addNull(comp.duration); artist.name = "QA_NULL"; artist.comment = ""; app.endUndoGroup(); rec("note", "artist null added, layers=" + comp.numLayers); }
        else rec("note", "C014_COMP not found");
        dump("04-before-rebuild");
        press(1, "05-rebuild-with-artist-null"); dump("05-after-rebuild");
        step = "06-remove-artist-null";
        if (artist) { artist.remove(); rec("note", "artist null removed, layers=" + comp.numLayers); }
        dump("06-restored");

        // N5: revision V001 -> V003 (V002 skipped)
        openQueue.push(V003); press(3, "07-revision-V001-to-V003"); dump("07-after-revision");
        press(2, "08-qc-after-revision");
    } catch (err) { rec("harness-error", err.toString() + " line " + err.line); }
    File.openDialog = realOpen;
    step = "end";
    for (var w = 0; w < windows.length; w++) { try { windows[w].close(); } catch (e) {} }
    writeLog(true);
    app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
}());
