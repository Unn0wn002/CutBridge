from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "apps" / "after-effects" / "CutBridge.jsx"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 1:
        print(f"patch: {label}")
        return text.replace(old, new, 1)
    if count == 0 and new in text:
        print(f"already patched: {label}")
        return text
    raise RuntimeError(f"{label}: expected exactly one original anchor, found {count}")


text = PATH.read_text(encoding="utf-8")

text = replace_once(
    text,
    '''    var revisionManager = null;
    var qcPlus = null;
    function log(msg) { $.writeln("[CutBridge] " + msg); }
    function alertError(msg) { alert("CutBridge\\n\\n" + msg); }
    function readTextFile(file) { file.encoding = "UTF-8"; if (!file.open("r")) throw new Error("Could not open: " + file.fsName); var text = file.read(); file.close(); return text; }
''',
    '''    var revisionManager = null;
    var qcPlus = null;
    var localization = null;
    var currentLocale = "EN";
    function log(msg) { $.writeln("[CutBridge] " + msg); }
    function fallbackLocalization() {
        var locale = "EN", strings = {
            language_label: "UI Language", no_package: "No package loaded", import_package: "1. Import Package",
            build_comp: "2. Build Comp", run_qc: "3. Run QC", update_revision: "4. Update Revision",
            workflow_note: "v{version}: validated package -> idempotent comp -> QC",
            package_status: "{name} | {fps}fps | {frames}f", choose_manifest: "Choose CutBridge cutbridge.json",
            choose_revision: "Choose newer CutBridge cutbridge.json", revision_file_required: "Choose the cutbridge.json file from the newer package.",
            revision_confirm: "Update CutBridge revision to V{version}?", warnings: "Warnings:",
            revision_scope: "Only verified CutBridge-managed sources and metadata will be changed.",
            revision_updated: "CutBridge: revision updated to V{version}.", revision_preserved: "Managed layer properties and artist layers were preserved.",
            confirmation_unavailable: "After Effects confirmation UI is unavailable; revision was not applied.",
            comp_built: "CutBridge: comp built", comp_reused: "CutBridge: comp reused safely",
            rollback_created: "Newly created managed objects were rolled back."
        };
        function format(value, values) {
            var out = String(value), key; values = values || {};
            for (key in values) if (Object.prototype.hasOwnProperty.call(values, key)) out = out.replace(new RegExp("\\\\{" + key + "\\\\}", "g"), String(values[key]));
            return out;
        }
        return {
            DEFAULT_LOCALE: "EN", FALLBACK_LOCALE: "EN",
            normalizeLocale: function(value) { return String(value || "").toUpperCase() === "JA" ? "JA" : "EN"; },
            tr: function(value, key, values) { return format(strings[key] || key, values); },
            setLocale: function(value) { locale = String(value || "").toUpperCase() === "JA" ? "JA" : "EN"; return locale; },
            getLocale: function() { return locale; },
            formatError: function(value, detail) { return "CutBridge\\n\\n" + detail; },
            localizeRevisionReason: function(value, reason) { return String(reason); },
            formatRevisionBlocked: function(value, reasons) { return "CutBridge\\n\\nRevision blocked:\\n- " + reasons.join("\\n- "); },
            localizeRecords: function(value, records) { return records; },
            qcHeadline: function(value, headline) { return headline; },
            localizeRenderedQC: function(value, report) { return report; }
        };
    }
    function getLocalization() {
        if (localization) return localization;
        try {
            if (typeof CutBridgeLocalization !== "undefined") localization = CutBridgeLocalization;
            else if (typeof $ !== "undefined" && $.fileName) {
                var localizationFile = new File(new File($.fileName).parent.fsName + "/localization.js");
                if (localizationFile.exists) {
                    $.evalFile(localizationFile);
                    if (typeof CutBridgeLocalization !== "undefined") localization = CutBridgeLocalization;
                }
            }
        } catch (localizationError) { log("Localization unavailable; using English fallback: " + localizationError.toString()); }
        if (!localization || typeof localization.tr !== "function" || typeof localization.normalizeLocale !== "function" ||
            typeof localization.formatError !== "function" || typeof localization.localizeRecords !== "function" ||
            typeof localization.formatRevisionBlocked !== "function") {
            localization = fallbackLocalization();
        }
        return localization;
    }
    function loadLocalePreference() {
        var l10n = getLocalization(), locale = l10n.DEFAULT_LOCALE || "EN";
        try {
            if (typeof app !== "undefined" && app.settings && app.settings.haveSetting && app.settings.haveSetting("CutBridge", "ui_locale")) {
                locale = app.settings.getSetting("CutBridge", "ui_locale");
            }
        } catch (settingsError) { log("Locale preference read failed: " + settingsError.toString()); }
        currentLocale = l10n.setLocale ? l10n.setLocale(locale) : l10n.normalizeLocale(locale);
        return currentLocale;
    }
    function saveLocalePreference(locale) {
        var l10n = getLocalization();
        currentLocale = l10n.setLocale ? l10n.setLocale(locale) : l10n.normalizeLocale(locale);
        try {
            if (typeof app !== "undefined" && app.settings && app.settings.saveSetting) app.settings.saveSetting("CutBridge", "ui_locale", currentLocale);
        } catch (settingsError) { log("Locale preference write failed: " + settingsError.toString()); }
        return currentLocale;
    }
    function tr(key, values) { return getLocalization().tr(currentLocale, key, values || {}); }
    function alertError(msg) { alert(getLocalization().formatError(currentLocale, msg)); }
    function readTextFile(file) { file.encoding = "UTF-8"; if (!file.open("r")) throw new Error("Could not open: " + file.fsName); var text = file.read(); file.close(); return text; }
''',
    "localization bootstrap",
)

text = replace_once(
    text,
    '        var f = File.openDialog("Choose CutBridge cutbridge.json", "JSON:*.json");',
    '        var f = File.openDialog(tr("choose_manifest"), "JSON:*.json");',
    "localized manifest dialog",
)

text = replace_once(
    text,
    '''        var file = File.openDialog("Choose newer CutBridge cutbridge.json / 新しいバージョン", "JSON:*.json");
        if (!file) return null;
        if (String(file.name).toLowerCase() !== "cutbridge.json") throw new Error("Choose the cutbridge.json file from the newer package.");
''',
    '''        var file = File.openDialog(tr("choose_revision"), "JSON:*.json");
        if (!file) return null;
        if (String(file.name).toLowerCase() !== "cutbridge.json") throw new Error(tr("revision_file_required"));
''',
    "localized revision dialog",
)

text = replace_once(
    text,
    '''            var passSetReasons = directRevisionPassSetErrors(state.manifest, selected.manifest);
            if (passSetReasons.length) { alertError("Revision blocked:\\n- " + passSetReasons.join("\\n- ")); return; }
            var manager = getRevisionManager(), assessment = manager.assess(state.manifest, selected.manifest);
            if (assessment.status === "incompatible") { alertError("Revision blocked:\\n- " + assessment.reasons.join("\\n- ")); return; }
            var adapter = makeRevisionAdapter(state.manifest, selected.manifest, selected.root), executor = manager.createExecutor(adapter), ticket = executor.prepare(state.manifest, selected.manifest);
            var message = "Update CutBridge revision to V" + CutBridgeContract.zeroPad(selected.manifest.version, 3) + "?\\n\\n" + (ticket.warnings.length ? "Warnings:\\n- " + ticket.warnings.join("\\n- ") + "\\n\\n" : "") + "Only verified CutBridge-managed sources and metadata will be changed.";
            if (typeof confirm !== "function") throw new Error("After Effects confirmation UI is unavailable; revision was not applied.");
            if (!confirm(message)) return;
''',
    '''            var passSetReasons = directRevisionPassSetErrors(state.manifest, selected.manifest), l10n = getLocalization();
            if (passSetReasons.length) { alert(l10n.formatRevisionBlocked(currentLocale, passSetReasons)); return; }
            var manager = getRevisionManager(), assessment = manager.assess(state.manifest, selected.manifest);
            if (assessment.status === "incompatible") { alert(l10n.formatRevisionBlocked(currentLocale, assessment.reasons)); return; }
            var adapter = makeRevisionAdapter(state.manifest, selected.manifest, selected.root), executor = manager.createExecutor(adapter), ticket = executor.prepare(state.manifest, selected.manifest);
            var revisionVersion = CutBridgeContract.zeroPad(selected.manifest.version, 3), localizedWarnings = [], wi;
            for (wi = 0; wi < ticket.warnings.length; wi++) localizedWarnings.push(l10n.localizeRevisionReason(currentLocale, ticket.warnings[wi]));
            var message = tr("revision_confirm", {version: revisionVersion}) + "\\n\\n" + (localizedWarnings.length ? tr("warnings") + "\\n- " + localizedWarnings.join("\\n- ") + "\\n\\n" : "") + tr("revision_scope");
            if (typeof confirm !== "function") throw new Error(tr("confirmation_unavailable"));
            if (!confirm(message)) return;
''',
    "localized revision guards and prompt",
)

text = replace_once(
    text,
    '''                alert("CutBridge: revision updated to V" + CutBridgeContract.zeroPad(selected.manifest.version, 3) + ".\\nManaged layer properties and artist layers were preserved.");
''',
    '''                alert(tr("revision_updated", {version: revisionVersion}) + "\\n" + tr("revision_preserved"));
''',
    "localized revision success",
)

text = replace_once(
    text,
    '''            var message = "CutBridge: comp " + (compResult.created ? "built" : "reused safely") + "\\n" + comp.name + "\\n" + m.resolution.width + "x" + m.resolution.height + " @ " + m.fps + " fps";
            if (warnings.length) message += "\\n\\nWarnings:\\n- " + warnings.join("\\n- ");
''',
    '''            var message = tr(compResult.created ? "comp_built" : "comp_reused") + "\\n" + comp.name + "\\n" + m.resolution.width + "x" + m.resolution.height + " @ " + m.fps + " fps";
            if (warnings.length) message += "\\n\\n" + tr("warnings") + "\\n- " + warnings.join("\\n- ");
''',
    "localized build result",
)

text = replace_once(
    text,
    '''            if (createdLayers.length || createdFootage.length) errorMessage += "\\nNewly created managed objects were rolled back.";
''',
    '''            if (createdLayers.length || createdFootage.length) errorMessage += "\\n" + tr("rollback_created");
''',
    "localized rollback note",
)

text = replace_once(
    text,
    '''        function finish() {
            var report = qc.render(records);
            alert("CutBridge QC — " + report.headline + "\\n\\n" + report.text);
        }
''',
    '''        function finish() {
            var l10n = getLocalization(), localizedRecords = l10n.localizeRecords(currentLocale, records);
            var report = qc.render(localizedRecords);
            alert("CutBridge QC — " + l10n.qcHeadline(currentLocale, report.headline) + "\\n\\n" + l10n.localizeRenderedQC(currentLocale, report.text));
        }
''',
    "localized QC rendering",
)

text = replace_once(
    text,
    '''    function loadOnly(statusText) { try { var m = chooseManifest(); if (m) statusText.text = (m.package_name || m.cut) + " | " + m.fps + "fps | " + m.frames.count + "f"; } catch (e) { alertError(e.toString()); } }
    function buildUI(thisObj) {
        var pal = (thisObj instanceof Panel) ? thisObj : new Window("palette", "CutBridge", undefined, {resizeable: true}); if (!pal) return pal;
        pal.orientation = "column"; pal.alignChildren = ["fill", "top"]; pal.spacing = 8; pal.margins = 12;
        var title = pal.add("statictext", undefined, "CutBridge / カットブリッジ"); try { title.graphics.font = ScriptUI.newFont(title.graphics.font.name, "BOLD", 16); } catch (e) {}
        var status = pal.add("statictext", undefined, "No package loaded"); status.characters = 45;
        var btnLoad = pal.add("button", undefined, "1. Import Package / 読み込み"); var btnBuild = pal.add("button", undefined, "2. Build Comp / コンポ作成"); var btnQC = pal.add("button", undefined, "3. Run QC / QC実行"); var btnRevision = pal.add("button", undefined, "4. Update Revision / 差し替え");
        btnLoad.onClick = function() { loadOnly(status); }; btnBuild.onClick = function() { buildComp(); }; btnQC.onClick = function() { try { runQC(); } catch (e) { alertError(e.toString()); } }; btnRevision.onClick = function() { updateRevision(); };
        var note = pal.add("statictext", undefined, "v" + CutBridgeContract.PRODUCT_VERSION + ": validated package → idempotent comp → QC", {multiline: true}); note.preferredSize.height = 32;
        pal.onResizing = pal.onResize = function() { this.layout.resize(); }; return pal;
    }
''',
    '''    function packageStatusText(manifest) {
        if (!manifest) return tr("no_package");
        return tr("package_status", {name: manifest.package_name || manifest.cut, fps: manifest.fps, frames: manifest.frames.count});
    }
    function loadOnly(statusText) { try { var m = chooseManifest(); if (m) statusText.text = packageStatusText(m); } catch (e) { alertError(e.toString()); } }
    function buildUI(thisObj) {
        loadLocalePreference();
        var pal = (thisObj instanceof Panel) ? thisObj : new Window("palette", "CutBridge", undefined, {resizeable: true}); if (!pal) return pal;
        pal.orientation = "column"; pal.alignChildren = ["fill", "top"]; pal.spacing = 8; pal.margins = 12;
        var title = pal.add("statictext", undefined, "CutBridge"); try { title.graphics.font = ScriptUI.newFont(title.graphics.font.name, "BOLD", 16); } catch (e) {}
        var localeLabel = pal.add("statictext", undefined, tr("language_label"));
        var localeSelect = pal.add("dropdownlist", undefined, ["日本語", "English"]); localeSelect.selection = currentLocale === "JA" ? 0 : 1;
        var status = pal.add("statictext", undefined, packageStatusText(state.manifest)); status.characters = 45;
        var btnLoad = pal.add("button", undefined, tr("import_package")); var btnBuild = pal.add("button", undefined, tr("build_comp")); var btnQC = pal.add("button", undefined, tr("run_qc")); var btnRevision = pal.add("button", undefined, tr("update_revision"));
        btnLoad.onClick = function() { loadOnly(status); }; btnBuild.onClick = function() { buildComp(); }; btnQC.onClick = function() { try { runQC(); } catch (e) { alertError(e.toString()); } }; btnRevision.onClick = function() { updateRevision(); };
        var note = pal.add("statictext", undefined, tr("workflow_note", {version: CutBridgeContract.PRODUCT_VERSION}), {multiline: true}); note.preferredSize.height = 32;
        function refreshLocale() {
            localeLabel.text = tr("language_label"); status.text = packageStatusText(state.manifest);
            btnLoad.text = tr("import_package"); btnBuild.text = tr("build_comp"); btnQC.text = tr("run_qc"); btnRevision.text = tr("update_revision");
            note.text = tr("workflow_note", {version: CutBridgeContract.PRODUCT_VERSION});
            try { pal.layout.layout(true); } catch (layoutError) {}
        }
        localeSelect.onChange = function() {
            if (!localeSelect.selection) return;
            saveLocalePreference(localeSelect.selection.index === 0 ? "JA" : "EN");
            refreshLocale();
        };
        pal.onResizing = pal.onResize = function() { this.layout.resize(); }; return pal;
    }
''',
    "localized panel UI",
)

PATH.write_text(text, encoding="utf-8")
print("S8 AE localization JSX patch complete")
