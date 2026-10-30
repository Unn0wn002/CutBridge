#target aftereffects
// S14B fixture S14B-FX01 dry run (not a participant session). Runs the unmodified CutBridge.jsx beside this file and
// presses its real panel buttons via notify("onClick"); File.openDialog returns the queued manifest, confirm()
// returns true, alert() text is recorded. Single pass, no retries. Leftover CutBridge globals are recorded and
// cleared first. Works on copies of the fixture packages in ../pkgs, never on the fixture originals.
// Variant B: artist state is placed on the CutBridge-managed layers themselves (effect, mask and 40% opacity on the
// BEAUTY layer; the LINE layer parented to an artist null), then V002 and V003 with QC+ after each. No JP08 setup.
(function () {
    var here = new File($.fileName).parent.fsName;
    var work = new Folder(here).parent.fsName;
    function manifest(v) { return new File(work + "/pkgs/S14B_EP01_SC001_C001_T01_V00" + v + "/cutbridge.json"); }
    var log = [], step = "init", openQueue = [], windows = [];

    function j(s) { return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "").replace(/\n/g, "\\n") + '"'; }
    function rec(kind, text) { log.push('{"step":' + j(step) + ',"kind":' + j(kind) + ',"text":' + j(text) + '}'); writeLog(false); }
    function writeLog(done) {
        var f = new File(work + "/dryrun-log-B.json"); f.encoding = "UTF-8"; f.open("w");
        f.write('{"done":' + (done ? "true" : "false") + ',"ae":' + j(app.version) + ',"entries":[\n' + log.join(",\n") + "\n]}\n"); f.close();
    }
    function writeFile(name, text) { var f = new File(work + "/" + name); f.encoding = "UTF-8"; f.open("w"); f.write(text); f.close(); }

    function layerInfo(ly) {
        var tr = ly.property("ADBE Transform Group"), fx = ly.property("ADBE Effect Parade"), masks = ly.property("ADBE Mask Parade"), src = "";
        try { src = ly.source ? ly.source.name : ""; } catch (e) { src = "<err>"; }
        var fxNames = [];
        if (fx) for (var k = 1; k <= fx.numProperties; k++) fxNames.push(fx.property(k).matchName);
        return '{"name":' + j(ly.name) + ',"source":' + j(src) + ',"comment":' + j(ly.comment) +
            ',"opacity":' + tr.property("ADBE Opacity").value + ',"effects":' + j(fxNames.join(",")) +
            ',"masks":' + (masks ? masks.numProperties : 0) + ',"parent":' + j(ly.parent ? ly.parent.name : "") + "}";
    }
    function dump(label) {
        step = label;
        var out = ['{"label":' + j(label) + ',"items":['];
        for (var i = 1; i <= app.project.numItems; i++) {
            var it = app.project.item(i), tn = String(it.typeName);
            var r = '{"typeName":' + j(tn) + ',"name":' + j(it.name) + ',"comment":' + j(it.comment);
            if (tn === "Composition") {
                r += ',"width":' + it.width + ',"height":' + it.height + ',"fps":' + it.frameRate + ',"duration":' + it.duration + ',"markers":' + it.markerProperty.numKeys + ',"layers":[';
                for (var l = 1; l <= it.numLayers; l++) r += (l > 1 ? "," : "") + layerInfo(it.layer(l));
                r += "]";
            } else if (tn === "Footage") {
                var path = ""; try { path = it.mainSource.file ? it.mainSource.file.fsName : ""; } catch (e1) {}
                r += ',"file":' + j(path) + ',"missing":' + (it.footageMissing === true);
            }
            out.push((i > 1 ? "," : "") + r + "}");
        }
        out.push("]}\n");
        writeFile("dryrun-B-state-" + label + ".json", out.join(""));
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
    function managedComp() { for (var i = 1; i <= app.project.numItems; i++) { var it = app.project.item(i); if (String(it.typeName) === "Composition" && it.name === "C001_COMP") return it; } return null; }

    try {
        if (!manifest(1).exists || !manifest(2).exists || !manifest(3).exists) throw new Error("packages missing");
        step = "clear-globals";
        var names = ["CutBridgeContract", "CutBridgeRevisionManager", "CutBridgeQCPlus", "CutBridgeLocalization"], seen = [];
        for (var g = 0; g < names.length; g++) { seen.push(names[g] + "=" + typeof $.global[names[g]]); $.global[names[g]] = undefined; }
        rec("globals-before-clear", seen.join(" "));
        app.newProject();
        var src = new File(here + "/CutBridge.jsx"); src.encoding = "UTF-8"; src.open("r"); var text = src.read(); src.close();
        step = "start-panel";
        // eval of the unmodified candidate CutBridge.jsx (hash-checked ZIP) so alert/confirm/Window can be shadowed
        eval("(function (alert, confirm, Window) {\n" + text + "\n$.global.CutBridgeContract = CutBridgeContract;\n})")(stubAlert, stubConfirm, CaptureWindow);

        openQueue.push(manifest(1)); press(0, "01-load-V001");
        press(1, "02-build-V001");
        press(2, "03-qc-V001-clean");

        step = "04-artist-edits-managed";
        var comp = managedComp();
        if (!comp) throw new Error("managed comp C001_COMP not found");
        var beauty = null, line = null;
        for (var l = 1; l <= comp.numLayers; l++) { var nm = comp.layer(l).name; if (/BEAUTY/.test(nm)) beauty = comp.layer(l); if (/LINE/.test(nm)) line = comp.layer(l); }
        if (!beauty || !line) throw new Error("managed BEAUTY/LINE layers not found");
        rec("managed-layers", beauty.name + " / " + line.name);
        var nul = comp.layers.addNull(comp.duration); nul.name = "ARTIST_NULL";
        beauty.property("ADBE Transform Group").property("ADBE Opacity").setValue(40);
        beauty.property("ADBE Effect Parade").addProperty("ADBE Gaussian Blur 2");
        var shape = new Shape(); shape.vertices = [[100, 100], [500, 100], [500, 400], [100, 400]]; shape.closed = true;
        beauty.property("ADBE Mask Parade").addProperty("ADBE Mask Atom").property("ADBE Mask Shape").setValue(shape);
        line.parent = nul;
        dump("04-before-revisions");

        openQueue.push(manifest(2)); press(3, "09-revision-V001-to-V002"); dump("09-after-V002");
        press(2, "10-qc-V002");
        openQueue.push(manifest(3)); press(3, "11-revision-V002-to-V003"); dump("11-after-V003");
        press(2, "12-qc-V003");
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    } catch (err) { rec("harness-error", err.toString() + " line " + err.line); }
    File.openDialog = realOpen;
    step = "end";
    for (var w = 0; w < windows.length; w++) { try { windows[w].close(); } catch (e) {} }
    writeLog(true);
}());
