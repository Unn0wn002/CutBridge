#target aftereffects
// QA read-only project state dump (scratch script, not part of the repository).
// Writes JSON describing every comp, layer and footage item. Reads only.
(function () {
    function j(s) { return '"' + String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r|\n/g, " ") + '"'; }
    var out = [];
    out.push('{"ae_version":' + j(app.version) + ',"build":' + j(app.buildNumber) + ',"items":[');
    var first = true;
    for (var i = 1; i <= app.project.numItems; i++) {
        var it = app.project.item(i);
        var kind = (it instanceof CompItem) ? "Comp" : (it instanceof FolderItem) ? "Folder" : (it instanceof FootageItem) ? "Footage" : "Other";
        var rec = '{"index":' + i + ',"kind":' + j(kind) + ',"name":' + j(it.name);
        if (it instanceof CompItem) {
            rec += ',"width":' + it.width + ',"height":' + it.height + ',"fps":' + it.frameRate + ',"duration":' + it.duration + ',"numLayers":' + it.numLayers + ',"layers":[';
            for (var l = 1; l <= it.numLayers; l++) {
                var ly = it.layer(l);
                var src = "";
                try { src = ly.source ? ly.source.name : ""; } catch (e) { src = "<err>"; }
                rec += (l > 1 ? "," : "") + '{"index":' + l + ',"name":' + j(ly.name) + ',"source":' + j(src) + ',"enabled":' + ly.enabled + ',"nullLayer":' + (ly.nullLayer === true) + ',"comment":' + j(ly.comment) + '}';
            }
            rec += "]";
        } else if (it instanceof FootageItem) {
            var p = "", missing = false, w = 0, h = 0, fr = 0, dur = 0;
            try { if (it.mainSource instanceof FileSource) { p = it.mainSource.file ? it.mainSource.file.fsName : ""; } } catch (e1) {}
            try { missing = it.footageMissing === true; } catch (e2) {}
            try { w = it.width; h = it.height; fr = it.frameRate; dur = it.duration; } catch (e3) {}
            rec += ',"file":' + j(p) + ',"missing":' + missing + ',"width":' + w + ',"height":' + h + ',"fps":' + fr + ',"duration":' + dur;
        }
        rec += ',"comment":' + j(it.comment) + '}';
        out.push((first ? "" : ",") + rec);
        first = false;
    }
    out.push("]}");
    var f = File.saveDialog("QA state dump (JSON)", "JSON:*.json");
    if (!f) { alert("cancelled"); return; }
    f.encoding = "UTF-8";
    f.open("w"); f.write(out.join("")); f.close();
    alert("State dump written: " + f.fsName);
}());
