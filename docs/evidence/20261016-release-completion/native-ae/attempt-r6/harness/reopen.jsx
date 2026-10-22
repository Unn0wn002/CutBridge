$.evalFile(new File("C:/NativeAEInput/common.jsx"));
CB.execute("reopen", function () {
    var c = CB.openSaved(3), before = CB.preservation(), ids = CB.ids(), layerCount = c.numLayers;
    var baseline = CB.parse(CB.read(CB.config.output_root + "/preservation-baseline.json"));
    CB.check("reopened V003 concrete artist values match saved baseline", CB.equal(before, baseline), {expected: baseline, actual: before});
    CB.handoff(); CB.build("reopened V003 Build/QC");
    CB.check("reopened Build preserves all artist values", CB.equal(before, CB.preservation()));
    CB.check("reopened Build creates no duplicate objects", CB.equal(ids, CB.ids()) && layerCount === c.numLayers);
    app.project.save(new File(CB.config.output_root + "/reopened-V003.aep"));
    CB.report.reopen_scope = "Project close/open plus freshly evaluated exact installed CutBridge runtime. Process restart is established only when launcher records distinct process IDs.";
});
