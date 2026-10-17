$.evalFile(new File("C:/NativeAEInput/common.jsx"));
CB.execute("negative", function () {
    function noMutation(name, before) { CB.check(name, CB.equal(before, CB.snapshot()), {before: before, after: CB.snapshot()}); }
    function requiredLayer(c) {
        var passes = CutBridgeContract.getState().manifest.passes;
        for (var i = 0; i < passes.length; i++) if (passes[i].required !== false) return c.layer(passes[i].name);
        throw CB.insufficient("Required managed layer fixture unavailable");
    }
    var c = CB.openSaved(3), layer = requiredLayer(c); layer.remove();
    var before = CB.snapshot(), q = CB.qc();
    CB.check("deleted required managed layer makes QC fail closed", q.report.summary.ERROR > 0, q);
    noMutation("deleted-layer QC does not mutate project", before);
    c = CB.openSaved(3); layer = requiredLayer(c); layer.comment = "ARTIST_DETAGGED";
    before = CB.snapshot(); q = CB.qc();
    CB.check("detagged required managed layer makes QC fail closed", q.report.summary.ERROR > 0, q);
    noMutation("detagged-layer QC does not mutate project", before);

    var safeNext = CB.variant("safe-V004", 4, null);
    for (var folderCase = 0; folderCase < 2; folderCase++) {
        c = CB.openSaved(3);
        if (folderCase === 0) c.parentFolder.name = "ARTIST_RENAMED_COMP_FOLDER";
        else { var duplicate = app.project.items.addFolder("01_COMP"); duplicate.parentFolder = c.parentFolder.parentFolder; }
        before = CB.snapshot();
        var built = CutBridgeContract.buildComp();
        CB.check((folderCase === 0 ? "missing" : "duplicate") + " deterministic folder blocks Build", !!built && built.success === false, built ? built.error : null);
        q = CB.qc(); CB.check("damaged folder QC fails closed", q.report.summary.ERROR > 0, q);
        CB.revision(safeNext.path, 3, false);
        noMutation("damaged-folder Build/revision/QC do not mutate project", before);
    }

    var variants = [];
    variants.push(CB.variant("fps-incompatible-V004", 4, function (m) { m.fps = m.fps + 1; }));
    variants.push(CB.variant("required-removed-V004", 4, function (m) {
        var remove = -1;
        for (var i = 0; i < m.passes.length; i++) if (m.passes[i].required !== false) { remove = i; break; }
        if (remove < 0 || m.passes.length < 2) throw CB.insufficient("Required-removal fixture needs at least two passes");
        var name = m.passes[remove].name; m.passes.splice(remove, 1);
        for (i = m.ae.layer_order.length - 1; i >= 0; i--) if (m.ae.layer_order[i] === name) m.ae.layer_order.splice(i, 1);
    }));
    variants.push(CB.variant("pass-added-V004", 4, function (m) {
        var p = m.passes[0];
        m.passes.push({name: "EXTRA", path: p.path, sequence_pattern: p.sequence_pattern, required: false});
        m.ae.layer_order.push("EXTRA");
    }));
    for (var i = 0; i < variants.length; i++) {
        CB.openSaved(3); before = CB.snapshot();
        CB.revision(variants[i].path, 3, false);
        noMutation("incompatible/pass-set revision blocks before import/migration " + i, before);
        CB.build("original V003 remains coherent after blocked revision " + i);
    }

    // Supported required->optional status change, with explicit confirmation.
    var statusChange = CB.variant("status-change-V004", 4, function (m) { m.passes[0].required = false; });
    CB.openSaved(3); var preserved = CB.preservation();
    var result = CB.revision(statusChange.path, 4, true);
    CB.check("required/optional status change explicitly warns", /required|optional|status/i.test(result.confirmations.join("\n")), result.confirmations);
    CB.check("status change preserves concrete artist values", CB.equal(preserved, CB.preservation()));
    CB.build("status-change V004 Build/QC");
    app.project.save(new File(CB.config.output_root + "/status-change-V004.aep"));
    var optionalName = statusChange.manifest.passes[0].name;
    c = CB.comp(); c.layer(optionalName).remove(); before = CB.snapshot(); q = CB.qc();
    CB.check("absent complete optional managed layer is warning only", q.report.summary.ERROR === 0 && q.report.summary.WARNING > 0, q);
    noMutation("optional-layer QC preserves project", before);

    // Reload the exact optional-current package before candidate optional removal.
    app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    app.open(new File(CB.config.output_root + "/status-change-V004.aep"));
    CutBridgeContract.loadManifest(statusChange.path); CB.comp();
    var optionalRemoved = CB.variant("optional-removed-V005", 5, function (m) {
        m.passes[0].required = false;
        var removed = m.passes.shift().name;
        for (var k = m.ae.layer_order.length - 1; k >= 0; k--) if (m.ae.layer_order[k] === removed) m.ae.layer_order.splice(k, 1);
    });
    before = CB.snapshot(); CB.revision(optionalRemoved.path, 4, false);
    noMutation("optional removal blocks before confirmation/import/tag migration", before);
    CB.build("original optional-current V004 remains coherent after blocked removal");

    // A fresh disposable Build with a missing optional source must warn/skip.
    var missingOptional = CB.variant("optional-source-missing-V004", 4, function (m) {
        m.passes[0].required = false; m.passes[0].path = "render/not-generated-optional";
    });
    CB.fresh(); CutBridgeContract.loadManifest(missingOptional.path);
    CB.build("missing optional source native Build/QC"); q = CB.qc();
    CB.check("missing optional sequence warns/skips rather than errors", q.report.summary.ERROR === 0 && q.report.summary.WARNING > 0, q);
    app.project.save(new File(CB.config.output_root + "/missing-optional-source.aep"));
    CB.openSaved(3);
});
