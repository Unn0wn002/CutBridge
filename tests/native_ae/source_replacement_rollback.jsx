// Supplemental phase of the retained corrected-harness; never edit ZIP runtime.
// Requires the disposable artist-V003.aep from run_all.jsx and fresh output.
$.evalFile(new File("C:/NativeAEInput/common.jsx"));
CB.execute("source-replacement-rollback", function () {
    CB.openSaved(3);
    CB.build("source rollback baseline V003 Build/QC");
    if (typeof isValid !== "function") throw CB.insufficient("Native isValid API unavailable");

    function cacheEntries(cache) {
        var keys = [], result = [], key;
        for (key in cache) if (cache.hasOwnProperty(key)) keys.push(key);
        keys.sort();
        for (var i = 0; i < keys.length; i++) result.push({key: keys[i], id: cache[keys[i]].id});
        return result;
    }
    function capture() {
        var state = CutBridgeContract.getState(), footage = [];
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (item instanceof FootageItem) footage.push({id: item.id, path: item.file ? item.file.fsName : null,
                comment: item.comment, parent: item.parentFolder.id, conform_fps: item.mainSource.conformFrameRate});
        }
        return {project: CB.snapshot(), footage: footage, state: {
            manifest: CB.parse(CB.json(state.manifest)), manifest_file: state.manifestFile.fsName,
            package_folder: state.packageFolder.fsName, comp_id: state.comp.id,
            imported: cacheEntries(state.imported), layers: cacheEntries(state.layers)}};
    }
    var before = capture(), initialIds = CB.ids();
    var fixture = CB.variant("source-replacement-failure-V004", 4, null);
    var evidence = {case_name: "real first swap then invalid native second swap", before: before,
        fixture: fixture, swaps: [], staged: [], runtime_bytes_modified: false,
        native_call_threw: false, first_native_swap_completed: false};
    CB.report.source_replacement_rollback = evidence;
    var evidencePath = CB.config.output_root + "/source-replacement-rollback-evidence.json";
    CB.save(evidencePath, evidence);
    if (!$.global.CutBridgeRevisionManager) $.evalFile(new File(CB.config.runtime_directory + "/revision_manager.js"));
    var manager = $.global.CutBridgeRevisionManager;
    if (!manager || typeof manager.createExecutor !== "function") throw CB.insufficient("Public revision executor seam unavailable");
    var originalFactory = manager.createExecutor, adapters = [], stagedHandles = [], calls = 0, result;
    try {
        try {
            manager.createExecutor = function (adapter) {
                var originalSwap = adapter.swapManagedSource;
                evidence.expected_replacements = adapter.listManagedLayers().length;
                if (evidence.expected_replacements < 2) throw CB.insufficient("Source rollback needs at least two active managed passes");
                adapters.push({adapter: adapter, swap: originalSwap});
                adapter.swapManagedSource = function (layer, replacement, passName) {
                    calls++;
                    if (calls === 1) {
                        // The real executor imports all replacements before its first swap.
                        for (var i = 1; i <= app.project.numItems; i++) {
                            var item = app.project.item(i), known = false;
                            for (var k = 0; k < initialIds.length; k++) if (initialIds[k] === item.id) known = true;
                            if (!known) {
                                CB.check("staged replacement is native footage", item instanceof FootageItem && isValid(item) && typeof item.id === "number");
                                stagedHandles.push(item);
                                evidence.staged.push({id: item.id, path: item.file.fsName, comment: item.comment, parent: item.parentFolder.id});
                            }
                        }
                    }
                    var record = {ordinal: calls, pass: passName, layer_id: layer.id,
                        old_source_id: layer.source.id, staged_source_id: replacement.id};
                    evidence.swaps.push(record);
                    CB.save(evidencePath, evidence);
                    if (calls === 1) {
                        originalSwap.call(adapter, layer, replacement, passName);
                        evidence.first_native_swap_completed = layer.source === replacement && layer.source.id === record.staged_source_id;
                        evidence.after_first_swap = capture();
                        CB.save(evidencePath, evidence);
                        return;
                    }
                    if (calls === 2) {
                        // Do not replace/throw from the native method. The reviewed real
                        // adapter journals then calls layer.replaceSource(null, false).
                        // Its guard cannot fail for this valid, callable native layer.
                        CB.check("second swap has live native inputs", layer instanceof AVLayer && isValid(layer) &&
                            isValid(layer.source) && replacement instanceof FootageItem && isValid(replacement) &&
                            typeof layer.replaceSource === "function" && typeof originalSwap === "function");
                        var nativeMethod = layer.replaceSource;
                        record.invalid_argument = "null"; record.real_adapter_called = true;
                        CB.save(evidencePath, evidence);
                        try { originalSwap.call(adapter, layer, null, passName); }
                        catch (nativeError) {
                            evidence.native_call_threw = true;
                            record.native_method_unchanged = layer.replaceSource === nativeMethod;
                            record.exception = {text: String(nativeError), file: nativeError.fileName, line: nativeError.line};
                            CB.save(evidencePath, evidence);
                            throw nativeError;
                        }
                        record.returned_without_throw = true;
                        CB.save(evidencePath, evidence);
                        return;
                    }
                    return originalSwap.call(adapter, layer, replacement, passName);
                };
                return originalFactory.call(manager, adapter);
            };
            if (manager.createExecutor === originalFactory) throw CB.insufficient("Executor seam cannot be instrumented");
            result = CB.revision(fixture.path, 3, true);
            evidence.revision = result;
        } finally {
            // Restore even when the native call, UI assertion or evidence check fails.
            manager.createExecutor = originalFactory;
            var restored = manager.createExecutor === originalFactory;
            for (var a = 0; a < adapters.length; a++) {
                adapters[a].adapter.swapManagedSource = adapters[a].swap;
                restored = restored && adapters[a].adapter.swapManagedSource === adapters[a].swap;
            }
            evidence.instrumentation_restored = restored;
            try { evidence.after = capture(); }
            catch (captureError) { evidence.after_capture_error = String(captureError); }
            CB.save(evidencePath, evidence);
        }
        CB.check("real first source replacement completed", calls === 2 && evidence.first_native_swap_completed, evidence.swaps);
        CB.check("second real native operation actually threw", evidence.native_call_threw && evidence.swaps[1].native_method_unchanged, evidence.swaps[1]);
        CB.check("source failure reports completed rollback", /rollback completed/i.test(result.alerts.join("\n")) && !/ROLLBACK INCOMPLETE/i.test(result.alerts.join("\n")), result.alerts);
        CB.check("all staged replacements captured before removal", evidence.staged.length >= 2 && evidence.staged.length === evidence.expected_replacements, evidence.staged);
        var afterIds = CB.ids();
        evidence.cleanup = [];
        for (var j = 0; j < evidence.staged.length; j++) {
            var absent = true;
            for (var n = 0; n < afterIds.length; n++) if (afterIds[n] === evidence.staged[j].id) absent = false;
            var invalid = isValid(stagedHandles[j]) === false;
            evidence.cleanup.push({id: evidence.staged[j].id, absent: absent, invalid_handle: invalid});
            CB.save(evidencePath, evidence);
            CB.check("staged source ID removed and native handle invalid " + j, absent && invalid, evidence.cleanup[j]);
        }
        CB.check("sources metadata caches and artist state restored", CB.equal(before, evidence.after), {before: before, after: evidence.after});
        CB.check("all instrumentation restored", evidence.instrumentation_restored);

        // Reload the actual installed panel, then rediscover the current V003
        // manifest/project; opening the saved project alone is not a panel reload.
        var panel = Window.find("palette", "CutBridge"); if (panel) panel.close();
        $.evalFile(new File(CB.config.runtime_directory + "/CutBridge.jsx"));
        $.global.CutBridgeContract = CutBridgeContract;
        CutBridgeContract.loadManifest(CB.packages[3].path);
        CB.comp(); CB.build("source rollback reload V003 Build/QC");
        evidence.recovered = capture();
        CB.check("reload Build/QC preserves restored project", CB.equal(before, evidence.recovered), evidence.recovered);
        evidence.saved_project = CB.config.output_root + "/source-replacement-rollback-recovered.aep";
        app.project.save(new File(evidence.saved_project));
    } finally { CB.save(evidencePath, evidence); }
});
try { if (app.project) app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (_) {}
app.quit();
