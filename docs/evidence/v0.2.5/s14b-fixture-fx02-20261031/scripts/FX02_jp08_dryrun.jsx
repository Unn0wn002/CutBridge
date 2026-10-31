#target aftereffects
// S14B fixture S14B-FX02 dry run for the shipped JP08 package (not a participant session). Runs the unmodified
// CutBridge.jsx beside this file in a new project and presses its real panel buttons via notify("onClick"):
// load the JP08 package (V001 with one optional LINE frame missing), Build, QC+. File.openDialog returns the queued
// manifest, confirm() returns true, alert() text is recorded. Single pass, no retries. Works on a copy of the bundle.
(function () {
    var here = new File($.fileName).parent.fsName;
    var work = new Folder(here).parent.fsName;
    var JP08 = new File(work + "/bundle-test/JP08_qc_check/S14B_EP01_SC001_C001_T01_V001/cutbridge.json");
    var log = [], step = "init", openQueue = [], windows = [];

    function j(s) { return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "").replace(/\n/g, "\\n") + '"'; }
    function rec(kind, text) { log.push('{"step":' + j(step) + ',"kind":' + j(kind) + ',"text":' + j(text) + '}'); writeLog(false); }
    function writeLog(done) {
        var f = new File(work + "/jp08-dryrun-log.json"); f.encoding = "UTF-8"; f.open("w");
        f.write('{"done":' + (done ? "true" : "false") + ',"ae":' + j(app.version) + ',"entries":[\n' + log.join(",\n") + "\n]}\n"); f.close();
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

    try {
        if (!JP08.exists) throw new Error("JP08 package missing");
        step = "clear-globals";
        var names = ["CutBridgeContract", "CutBridgeRevisionManager", "CutBridgeQCPlus", "CutBridgeLocalization"], seen = [];
        for (var g = 0; g < names.length; g++) { seen.push(names[g] + "=" + typeof $.global[names[g]]); $.global[names[g]] = undefined; }
        rec("globals-before-clear", seen.join(" "));
        app.newProject();
        var src = new File(here + "/CutBridge.jsx"); src.encoding = "UTF-8"; src.open("r"); var text = src.read(); src.close();
        step = "start-panel";
        // eval of the unmodified candidate CutBridge.jsx (hash-checked ZIP) so alert/confirm/Window can be shadowed
        eval("(function (alert, confirm, Window) {\n" + text + "\n$.global.CutBridgeContract = CutBridgeContract;\n})")(stubAlert, stubConfirm, CaptureWindow);
        openQueue.push(JP08); press(0, "01-load-JP08");
        press(1, "02-build-JP08");
        press(2, "03-qc-JP08");
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    } catch (err) { rec("harness-error", err.toString() + " line " + err.line); }
    File.openDialog = realOpen;
    step = "end";
    for (var w = 0; w < windows.length; w++) { try { windows[w].close(); } catch (e) {} }
    writeLog(true);
}());
