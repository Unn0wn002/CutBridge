#!/usr/bin/env python3
"""Second-stage exact-anchor fixes for the guarded S7 native QC patch."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, label: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return False
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def patch_native_ownership_scan() -> bool:
    path = ROOT / "apps/after-effects/CutBridge.jsx"
    old = '''        var liveComp = null, compLookupError = null;
        if (projectFolders) {
            try { liveComp = findManagedComp(m, managedCompFolder, compName); }
            catch (compError) { compLookupError = compError; }
        }
'''
    new = '''        var liveComp = null, compLookupError = null;
        // Even when the expected package root is absent, scan globally for the
        // exact managed-comp tag. A moved/tagged comp is ownership drift, not a
        // package-only state that QC may silently pass.
        try { liveComp = findManagedComp(m, managedCompFolder, compName); }
        catch (compError) { compLookupError = compError; }
'''
    return replace_once(path, old, new, "native moved-comp ownership scan")


def patch_contract_fixture() -> bool:
    path = ROOT / "tests/ae_contract_checks.cjs"
    changed = False
    changed |= replace_once(
        path,
        "const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');\n",
        "const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');\nconst QCPlus = require(path.join(root, 'apps/after-effects/qc_plus.js'));\n",
        "AE contract fixture QC+ module",
    )
    changed |= replace_once(
        path,
        "        ImportOptions: function(file) {this.file = file;}, ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}},\n        alert: message => alerts.push(message), $: {writeln() {}},\n",
        "        ImportOptions: function(file) {this.file = file;}, ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}}, CutBridgeQCPlus: QCPlus,\n        alert: message => alerts.push(message), $: {writeln() {}},\n",
        "AE contract fixture QC+ global",
    )
    return changed


def patch_root_structure_fixture() -> bool:
    path = ROOT / "tests/ae_s6_root_structure_checks.cjs"
    changed = False
    changed |= replace_once(
        path,
        'const source = fs.readFileSync(path.join(rootDir, "apps/after-effects/CutBridge.jsx"), "utf8");\n',
        'const source = fs.readFileSync(path.join(rootDir, "apps/after-effects/CutBridge.jsx"), "utf8");\nconst QCPlus = require(path.join(rootDir, "apps/after-effects/qc_plus.js"));\n',
        "S6 root fixture QC+ module",
    )
    changed |= replace_once(
        path,
        '        ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}},\n        alert: message => alerts.push(String(message)), $: {writeln() {}},\n',
        '        ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}}, CutBridgeQCPlus: QCPlus,\n        alert: message => alerts.push(String(message)), $: {writeln() {}},\n',
        "S6 root fixture QC+ global",
    )
    return changed


def main() -> int:
    changed = []
    for fn in (patch_native_ownership_scan, patch_contract_fixture, patch_root_structure_fixture):
        if fn():
            changed.append(fn.__name__)
    print("S7 native QC+ fix2 complete; changed=" + (", ".join(changed) if changed else "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
