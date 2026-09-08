#!/usr/bin/env python3
"""Apply the S7 QC+ native binding with exact fail-closed source anchors.

This is intentionally temporary integration tooling. It refuses to modify files
when the expected S6/S7 anchors drift, so an automated workflow cannot rewrite
an unexpected CutBridge.jsx layout.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, label: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return False
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one source anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def replace_between(path: Path, start: str, end: str, replacement: str, label: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if replacement in text:
        return False
    start_count = text.count(start)
    end_count = text.count(end)
    if start_count != 1 or end_count != 1:
        raise RuntimeError(f"{label}: expected one start/end marker, found {start_count}/{end_count}")
    left = text.index(start)
    right = text.index(end, left)
    path.write_text(text[:left] + replacement + text[right:], encoding="utf-8")
    return True


def patch_cutbridge() -> bool:
    path = ROOT / "apps/after-effects/CutBridge.jsx"
    changed = False
    changed |= replace_once(
        path,
        "    var revisionManager = null;\n",
        "    var revisionManager = null;\n    var qcPlus = null;\n",
        "CutBridge QC+ state",
    )

    loader = '''    function getQCPlus() {
        if (qcPlus) return qcPlus;
        if (typeof CutBridgeQCPlus !== "undefined") qcPlus = CutBridgeQCPlus;
        else {
            if (typeof $ === "undefined" || !$.fileName) throw new Error("CutBridge QC+ requires qc_plus.js beside CutBridge.jsx.");
            var scriptFile = new File(new File($.fileName).parent.fsName + "/qc_plus.js");
            if (!scriptFile.exists) throw new Error("CutBridge QC+ requires qc_plus.js beside CutBridge.jsx.");
            $.evalFile(scriptFile);
            if (typeof CutBridgeQCPlus === "undefined") throw new Error("CutBridge could not load qc_plus.js beside CutBridge.jsx.");
            qcPlus = CutBridgeQCPlus;
        }
        if (!qcPlus || typeof qcPlus.diagnostic !== "function" || typeof qcPlus.render !== "function" ||
            typeof qcPlus.sequenceRecords !== "function" || typeof qcPlus.compRecords !== "function" ||
            typeof qcPlus.managedObjectRecords !== "function" || typeof qcPlus.hostRecords !== "function") {
            throw new Error("CutBridge QC+ engine is invalid.");
        }
        return qcPlus;
    }

'''
    changed |= replace_once(
        path,
        "    function getRevisionManager() {\n",
        loader + "    function getRevisionManager() {\n",
        "CutBridge QC+ loader",
    )

    run_qc = '''    function runQC() {
        if (!ensureManifestLoaded()) return;
        var m = state.manifest, qc, records = [];
        function append(items) {
            for (var ai = 0; items && ai < items.length; ai++) records.push(items[ai]);
        }
        function add(spec) { records.push(qc.diagnostic(spec)); }
        function finish() {
            var report = qc.render(records);
            alert("CutBridge QC — " + report.headline + "\\n\\n" + report.text);
        }

        try { qc = getQCPlus(); }
        catch (qcLoadError) { alertError(qcLoadError.toString()); return; }

        var contractErrors = CutBridgeContract.validateManifest(m);
        if (contractErrors.length) {
            for (var ce = 0; ce < contractErrors.length; ce++) {
                add({severity: "ERROR", code: "CBQ-MANIFEST-CONTRACT-ERROR", scope: "manifest",
                    message: contractErrors[ce], remediation: "Repair or regenerate cutbridge.json from the trusted Blender package, then load it again before Build, Revision, or QC."});
            }
            finish(); return;
        }

        add({severity: "PASS", code: "CBQ-PACKAGE-IDENTITY-OK", scope: "package", subject: m.package_name || m.cut,
            message: "Package identity and manifest naming are valid."});
        add({severity: "PASS", code: "CBQ-MANIFEST-SCHEMA-OK", scope: "manifest",
            message: "Manifest schema " + CutBridgeContract.SCHEMA + " v" + CutBridgeContract.SCHEMA_VERSION + " is supported."});
        add({severity: "PASS", code: "CBQ-MANIFEST-FPS-OK", scope: "manifest", message: "FPS " + m.fps + " is valid."});
        add({severity: "PASS", code: "CBQ-MANIFEST-FRAMES-OK", scope: "manifest", message: "Frame count " + m.frames.count + " is internally consistent."});
        add({severity: "PASS", code: "CBQ-MANIFEST-RESOLUTION-OK", scope: "manifest", message: "Resolution " + m.resolution.width + "x" + m.resolution.height + " is valid."});

        if (!app.project) {
            append(qc.hostRecords({inspectable: false})); state.comp = null; finish(); return;
        }

        var projectFolders = null, folderLookupError = null;
        try { projectFolders = existingProjectFolders(m); }
        catch (folderError) { folderLookupError = folderError; }

        var managedCompFolder = projectFolders ? projectFolders.comp : null;
        var compName = (m.ae && m.ae.comp_name) ? m.ae.comp_name : (m.cut + "_COMP");
        var liveComp = null, compLookupError = null;
        if (projectFolders) {
            try { liveComp = findManagedComp(m, managedCompFolder, compName); }
            catch (compError) { compLookupError = compError; }
        }

        for (var i = 0; i < m.passes.length; i++) {
            var p = m.passes[i], coverage = null, managedFootage = null;
            try { coverage = inspectSequence(p, m); }
            catch (sequenceError) {
                add({severity: "ERROR", code: "CBQ-SEQ-INSPECTION-ERROR", scope: "sequence", subject: p.name,
                    message: "Sequence inspection failed — " + sequenceError.toString(),
                    remediation: "Verify the package-relative pass path, aliases, and sequence filenames. CutBridge will not follow unsafe paths or guess the intended source."});
                continue;
            }
            append(qc.sequenceRecords(p, m, coverage));
            if (!coverage.folderExists || !coverage.complete || !projectFolders) continue;

            if (!projectFolders.render) {
                add({severity: p.required === false ? "WARNING" : "ERROR", code: p.required === false ? "CBQ-FOOTAGE-OPTIONAL-MISSING" : "CBQ-FOOTAGE-REQUIRED-MISSING", scope: "footage", subject: p.name,
                    message: (p.required === false ? "optional" : "required") + " managed render folder is missing.",
                    remediation: "Restore the deterministic CutBridge package folders or rebuild/migrate deliberately; QC will not create or adopt folders automatically."});
                continue;
            }

            try {
                managedFootage = findManagedFootage(p, m, projectFolders.render, expectedFirstFile(p, coverage));
                append(qc.managedObjectRecords("footage", p, {status: managedFootage ? "ok" : "missing"}));
            } catch (footageError) {
                append(qc.managedObjectRecords("footage", p, {status: "ownership_error", message: "managed footage validation failed — " + footageError.toString()}));
            }

            if (liveComp && typeof liveComp.layer === "function" && managedFootage) {
                try {
                    var managedLayer = findManagedLayer(liveComp, CutBridgeContract.managedTag("layer", m, p.name), managedFootage, p.name);
                    append(qc.managedObjectRecords("layer", p, {status: managedLayer ? "ok" : "missing"}));
                } catch (layerError) {
                    append(qc.managedObjectRecords("layer", p, {status: "ownership_error", message: "managed layer validation failed — " + layerError.toString()}));
                }
            }
        }

        if (folderLookupError) {
            append(qc.hostRecords({ownershipAmbiguous: true, message: "Managed comp validation failed — " + folderLookupError.toString()}));
            state.comp = null;
        } else if (compLookupError) {
            add({severity: "ERROR", code: "CBQ-COMP-OWNERSHIP-ERROR", scope: "comp", subject: compName,
                message: "Managed comp validation failed — " + compLookupError.toString(),
                remediation: "Preserve artist work and resolve duplicate, misplaced, renamed, or incorrectly tagged managed-comp ownership before running QC again."});
            state.comp = null;
        } else if (projectFolders) {
            if (!managedCompFolder) {
                add({severity: "ERROR", code: "CBQ-COMP-FOLDER-MISSING", scope: "comp", subject: compName,
                    message: "Managed comp folder is missing from the expected package folder.",
                    remediation: "Restore the deterministic 01_COMP folder or rebuild/migrate deliberately; CutBridge will not create it during QC."});
                state.comp = null;
            } else if (!liveComp) {
                add({severity: "ERROR", code: "CBQ-COMP-MISSING", scope: "comp", subject: compName,
                    message: "Managed comp is missing from the expected comp folder.",
                    remediation: "Restore or deliberately rebuild the trusted CutBridge comp; QC will not create or adopt a replacement automatically."});
                state.comp = null;
            } else {
                state.comp = liveComp;
                var expected = CutBridgeContract.expectedCompSpec(m);
                var mismatches = CutBridgeContract.compSpecErrors(expected, {width: liveComp.width, height: liveComp.height, pixelAspect: liveComp.pixelAspect, duration: liveComp.duration, frameRate: liveComp.frameRate});
                append(qc.compRecords(mismatches));
                if (typeof liveComp.layer !== "function") {
                    append(qc.hostRecords({inspectable: false}));
                } else {
                    var staleManagedLayerCount = 0;
                    for (var li = 1; li <= liveComp.numLayers; li++) {
                        var qcLayerComment = itemComment(liveComp.layer(li));
                        if (isAnyManagedTag(qcLayerComment) && !isManagedLayerTagForManifest(qcLayerComment, m)) staleManagedLayerCount++;
                    }
                    append(qc.hostRecords({staleManagedTags: staleManagedLayerCount}));
                }
            }
        } else {
            // Before Build, QC remains a package/sequence-only inspection. Do not
            // claim missing managed AE state when no CutBridge package root exists.
            state.comp = null;
        }
        finish();
    }
'''
    changed |= replace_between(
        path,
        "    function runQC() {\n",
        "\n    function loadOnly(statusText)",
        run_qc,
        "CutBridge native runQC",
    )
    return changed


def patch_qc_plus() -> bool:
    path = ROOT / "apps/after-effects/qc_plus.js"
    changed = False
    changed |= replace_once(
        path,
        '                message: "Managed comp " + mismatches[i] + " differs from the manifest.",\n',
        '                message: "Managed comp metadata mismatch: " + mismatches[i] + ".",\n',
        "QC+ comp drift compatibility message",
    )
    changed |= replace_once(
        path,
        '                message: (optional ? "Optional " : "Required ") + label + " is missing.",\n',
        '                message: (optional ? "optional " : "required ") + label + " is missing.",\n',
        "QC+ managed missing compatibility message",
    )
    return changed


def patch_s5_fixture() -> bool:
    path = ROOT / "tests/ae_s5_checks.cjs"
    changed = False
    changed |= replace_once(
        path,
        "const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');\n",
        "const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');\nconst QCPlus = require(path.join(root, 'apps/after-effects/qc_plus.js'));\n",
        "S5 fixture QC+ module",
    )
    changed |= replace_once(
        path,
        "    ScriptUI: {newFont() {}}, alert: message => alerts.push(String(message)), $: {writeln() {}},\n",
        "    ScriptUI: {newFont() {}}, CutBridgeQCPlus: QCPlus, alert: message => alerts.push(String(message)), $: {writeln() {}},\n",
        "S5 fixture QC+ global",
    )
    return changed


def patch_s6_native_fixture() -> bool:
    path = ROOT / "tests/ae_s6_native_host_checks.cjs"
    changed = False
    changed |= replace_once(
        path,
        'const Revision = require(path.join(root, "apps/after-effects/revision_manager.js"));\n',
        'const Revision = require(path.join(root, "apps/after-effects/revision_manager.js"));\nconst QCPlus = require(path.join(root, "apps/after-effects/qc_plus.js"));\n',
        "S6 native fixture QC+ module",
    )
    changed |= replace_once(
        path,
        '        ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}}, CutBridgeRevisionManager: Revision,\n',
        '        ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}}, CutBridgeRevisionManager: Revision, CutBridgeQCPlus: QCPlus,\n',
        "S6 native fixture QC+ global",
    )
    return changed


def patch_managed_layer_expectations() -> bool:
    path = ROOT / "tests/ae_qc_managed_layer_checks.cjs"
    text = path.read_text(encoding="utf-8")
    replacements = [
        ("/^CutBridge QC — PASS with 1 warning\\(s\\)/", "/^CutBridge QC — WARNING — 1 warning\\(s\\)/"),
        ("/WARN LINE: optional managed layer is missing from the expected comp/", "/WARNING \\[CBQ-LAYER-OPTIONAL-MISSING\\] LINE: optional managed layer is missing/"),
        ("/WARN LINE: optional pass folder missing/", "/WARNING \\[CBQ-SEQ-OPTIONAL-FOLDER-MISSING\\] LINE: Optional pass folder is missing/"),
        ("/ERR\\s+LINE:/", "/ERROR \\[[^\\]]+\\] LINE:/"),
    ]
    changed = False
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
            changed = True
        elif new not in text:
            raise RuntimeError(f"managed-layer expectation anchor missing: {old}")
    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def write_native_binding_test() -> bool:
    path = ROOT / "tests/ae_s7_native_qc_binding_checks.cjs"
    content = r'''const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');

const fixturePath = path.resolve(__dirname, 'ae_s5_checks.cjs');
const fixtureSource = fs.readFileSync(fixturePath, 'utf8');
const fixtureModule = new Module(fixturePath, module);
fixtureModule.filename = fixturePath;
fixtureModule.paths = Module._nodeModulePaths(path.dirname(fixturePath));
fixtureModule._compile(
  fixtureSource + '\nmodule.exports = { host: host, manifest: manifest, beautyFiles: beautyFiles };\n',
  fixturePath
);

const {host, manifest, beautyFiles} = fixtureModule.exports;

{
  const h = host(manifest(), beautyFiles.slice());
  const beforeItems = h.projectItems.length;
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.match(message, /^CutBridge QC — PASS/);
  assert.match(message, /PASS \[CBQ-PACKAGE-IDENTITY-OK\]/);
  assert.match(message, /PASS \[CBQ-MANIFEST-SCHEMA-OK\]/);
  assert.match(message, /PASS \[CBQ-SEQ-COMPLETE\] BEAUTY:/);
  assert.equal(h.projectItems.length, beforeItems, 'package-only QC must not create AE project state');
}

{
  const h = host(manifest(), beautyFiles.slice());
  h.click('Build');
  const beforeItems = h.projectItems.length;
  h.comps()[0].frameRate = 30;
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.match(message, /^CutBridge QC — ERROR/);
  assert.match(message, /ERROR \[CBQ-COMP-DRIFT-FRAME-RATE\]/);
  assert.match(message, /Managed comp metadata mismatch: frame rate/);
  assert.equal(h.projectItems.length, beforeItems, 'QC must not repair comp drift');
}

{
  const h = host(manifest(), beautyFiles.slice());
  h.click('Build');
  const beforeItems = h.projectItems.length;
  h.comps()[0].layer(1).comment = '';
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.match(message, /ERROR \[CBQ-LAYER-OWNERSHIP-ERROR\] BEAUTY:/);
  assert.match(message, /managed layer validation failed/i);
  assert.equal(h.projectItems.length, beforeItems, 'ownership diagnostics must not adopt or replace the modified layer');
}

{
  const m = manifest();
  m.passes.push({name: 'LINE', path: 'render/line', sequence_pattern: 'C001_LINE_####.png', required: false});
  m.ae.layer_order = ['BEAUTY', 'LINE'];
  const h = host(m, beautyFiles.slice());
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.match(message, /^CutBridge QC — WARNING — 1 warning\(s\)/);
  assert.match(message, /WARNING \[CBQ-SEQ-OPTIONAL-FOLDER-MISSING\] LINE:/);
  assert.match(message, /Next:/);
}

console.log('S7 native QC+ binding: PASS (sidecar binding, stable codes, comp/ownership diagnostics, warning remediation, non-mutation)');
'''
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def patch_pytest_registration() -> bool:
    path = ROOT / "tests/test_ae_s7.py"
    text = path.read_text(encoding="utf-8")
    changed = False
    anchor = '''def test_s7_qc_plus_diagnostic_engine():
    node = shutil.which("node")
    assert node, "Node is required for S7 After Effects QC+ regression tests"
    root = Path(__file__).resolve().parents[1]
    subprocess.run([node, str(root / "tests" / "ae_s7_qc_plus_checks.cjs")], cwd=root, check=True)
'''
    addition = anchor + '''\n\ndef test_s7_native_qc_plus_binding():
    node = shutil.which("node")
    assert node, "Node is required for S7 native QC+ binding regressions"
    root = Path(__file__).resolve().parents[1]
    subprocess.run([node, str(root / "tests" / "ae_s7_native_qc_binding_checks.cjs")], cwd=root, check=True)
'''
    if "def test_s7_native_qc_plus_binding():" not in text:
        if text.count(anchor) != 1:
            raise RuntimeError("S7 pytest registration anchor drifted")
        text = text.replace(anchor, addition, 1)
        changed = True
    assertions_anchor = '''    assert "function revisionRecords(assessment, subject)" in source
'''
    assertions_new = assertions_anchor + '''\n    panel = (root / "apps/after-effects/CutBridge.jsx").read_text(encoding="utf-8")
    assert "function getQCPlus()" in panel
    assert '"/qc_plus.js"' in panel
    assert "CutBridgeQCPlus" in panel
    assert "qc.sequenceRecords" in panel
    assert "qc.managedObjectRecords" in panel
    assert "qc.compRecords" in panel
    assert "qc.hostRecords" in panel
    assert "qc.render(records)" in panel
'''
    if "function getQCPlus()" not in text:
        if text.count(assertions_anchor) != 1:
            raise RuntimeError("S7 static binding assertion anchor drifted")
        text = text.replace(assertions_anchor, assertions_new, 1)
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def patch_ci() -> bool:
    path = ROOT / ".github/workflows/ci.yml"
    old = '''      - name: Run S7 QC+ diagnostic checks
        run: node tests/ae_s7_qc_plus_checks.cjs
'''
    new = '''      - name: Run S7 QC+ diagnostic checks
        run: |
          node tests/ae_s7_qc_plus_checks.cjs
          node tests/ae_s7_native_qc_binding_checks.cjs
'''
    return replace_once(path, old, new, "S7 CI native binding registration")


def main() -> int:
    operations = [
        patch_cutbridge,
        patch_qc_plus,
        patch_s5_fixture,
        patch_s6_native_fixture,
        patch_managed_layer_expectations,
        write_native_binding_test,
        patch_pytest_registration,
        patch_ci,
    ]
    changed = []
    for operation in operations:
        if operation():
            changed.append(operation.__name__)
    print("S7 native QC+ patch complete; changed=" + (", ".join(changed) if changed else "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
