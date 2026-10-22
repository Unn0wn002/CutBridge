$.evalFile(new File("C:/NativeAEInput/common.jsx"));
CB.execute("rollback", function () {
    var c = CB.openSaved(3), before = CB.snapshot(), initialIds = CB.ids();
    CB.build("pre-rollback V003 Build/QC"); before = CB.snapshot();
    var fixture = CB.variant("failed-import-V004", 4, null);
    var prefix = String(new File(fixture.path).parent.fsName).replace(/\\/g, "/").toLowerCase() + "/";
    var originalReuseErrors = CutBridgeContract.footageReuseErrors;
    var injected = false, captured = [], capturedIds = [];
    try {
        // Public JS contract seam only: installed ZIP runtime bytes stay exact.
        // The wrapper fires after a real native footage allocation was tracked,
        // then forces the adapter's normal verification failure and rollback.
        CutBridgeContract.footageReuseErrors = function (expected, actual) {
            if (!injected && String(expected.path).replace(/\\/g, "/").toLowerCase().indexOf(prefix) === 0) {
                for (var i = 1; i <= app.project.numItems; i++) {
                    var item = app.project.item(i), known = false;
                    for (var k = 0; k < initialIds.length; k++) if (initialIds[k] === item.id) known = true;
                    if (!known && item instanceof FootageItem) { captured.push(item); capturedIds.push(item.id); }
                }
                injected = true; return ["Injected post-import verification failure"];
            }
            return originalReuseErrors(expected, actual);
        };
        var result = CB.revision(fixture.path, 3, true);
        CB.check("fault reached actual native post-import validation", injected && captured.length === 1 && typeof capturedIds[0] === "number", capturedIds);
        CB.check("failed import reports completed rollback", /Injected post-import verification failure/.test(result.alerts.join("\n")) && /rollback completed/.test(result.alerts.join("\n")) && !/ROLLBACK INCOMPLETE/.test(result.alerts.join("\n")), result.alerts);
        var afterIds = CB.ids(), absent = true;
        for (var j = 0; j < afterIds.length; j++) if (afterIds[j] === capturedIds[0]) absent = false;
        CB.check("captured native numeric ID is absent after cleanup", absent);
        if (typeof isValid !== "function") throw CB.insufficient("Native isValid API unavailable");
        CB.check("removed real native handle is invalid", isValid(captured[0]) === false);
        CB.check("failed import preserves every project object and artist value", CB.equal(before, CB.snapshot()), {before: before, after: CB.snapshot()});
        CB.report.failure_injection = {method: "temporary public CutBridgeContract.footageReuseErrors wrapper", runtime_bytes_modified: false, native_footage_ids_captured_before_removal: capturedIds, native_handles_invalid_after_removal: true};
    } finally { CutBridgeContract.footageReuseErrors = originalReuseErrors; }
    CB.build("V003 coherent after failed native import rollback");

    for (var kind = 0; kind < 2; kind++) {
        c = CB.openSaved(3); CB.build("populate real native caches " + kind);
        var state = CutBridgeContract.getState(), m = state.manifest, beauty = c.layer("BEAUTY"), old = kind === 0 ? beauty.source : beauty;
        var tag = CutBridgeContract.managedTag(kind === 0 ? "footage" : "layer", m, "BEAUTY");
        CB.check("old native handle is cached before invalidation " + kind, (kind === 0 ? state.imported[tag] : state.layers[tag]) === old);
        var replacement;
        if (kind === 0) {
            var io = new ImportOptions(old.file); io.sequence = true; io.forceAlphabetical = false;
            replacement = app.project.importFile(io); replacement.mainSource.conformFrameRate = m.fps;
            replacement.name = old.name; replacement.comment = old.comment; replacement.parentFolder = old.parentFolder;
            beauty.replaceSource(replacement, false);
        } else {
            replacement = c.layers.add(old.source); replacement.name = old.name; replacement.comment = old.comment;
            // Preserve ordering relative to every other layer while replacing
            // only this disposable managed layer to create a genuinely stale cache.
            replacement.moveBefore(old);
        }
        var retiredId = old.id; old.remove();
        CB.check("native removed cache handle is invalid " + kind, isValid(old) === false, {retired_id: retiredId});
        var itemIds = CB.ids(), layerCount = c.numLayers;
        CB.build("invalid native cache safe rediscovery " + kind);
        CB.check("invalid native cache produces no duplicate objects " + kind, CB.equal(itemIds, CB.ids()) && c.numLayers === layerCount);
        CB.check("live replacement discovered from actual project state " + kind, (kind === 0 ? CutBridgeContract.getState().imported[tag] : CutBridgeContract.getState().layers[tag]) === replacement);
        app.project.save(new File(CB.config.output_root + "/invalid-cache-" + kind + ".aep"));
    }
    CB.openSaved(3);
});
