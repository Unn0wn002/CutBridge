#!/usr/bin/env python3
"""Apply the S7 exact-current orphan managed-tag guard with strict anchors."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_panel() -> None:
    path = ROOT / "apps/after-effects/CutBridge.jsx"
    helper = '''    function exactCurrentManagedOrphans(manifest) {
        var result = {footage: {}, layer: {}}, i, p, tag;
        for (i = 0; i < manifest.passes.length; i++) {
            result.footage["$" + manifest.passes[i].name] = 0;
            result.layer["$" + manifest.passes[i].name] = 0;
        }
        if (!app.project) return result;
        for (var itemIndex = 1; itemIndex <= app.project.numItems; itemIndex++) {
            var item = app.project.item(itemIndex), comment = itemComment(item);
            for (i = 0; i < manifest.passes.length; i++) {
                p = manifest.passes[i]; tag = "$" + p.name;
                if (comment === CutBridgeContract.managedTag("footage", manifest, p.name)) result.footage[tag]++;
            }
            if (typeof CompItem === "undefined" || !(item instanceof CompItem) || typeof item.layer !== "function") continue;
            for (var layerIndex = 1; layerIndex <= item.numLayers; layerIndex++) {
                var layerComment = itemComment(item.layer(layerIndex));
                for (i = 0; i < manifest.passes.length; i++) {
                    p = manifest.passes[i]; tag = "$" + p.name;
                    if (layerComment === CutBridgeContract.managedTag("layer", manifest, p.name)) result.layer[tag]++;
                }
            }
        }
        return result;
    }

'''
    replace_once(path, "    function runQC() {\n", helper + "    function runQC() {\n", "orphan helper")

    old = '''        } else {
            // Before Build, QC remains a package/sequence-only inspection. Do not
            // claim missing managed AE state when no CutBridge package root exists.
            state.comp = null;
        }
        finish();
'''
    new = '''        } else {
            // A genuinely untouched project can be inspected package/sequence-only.
            // Exact-current managed tags, however, prove that managed AE state exists
            // somewhere in the project. If its package root/comp is gone, report the
            // orphan state instead of silently treating it as pre-Build. Historical
            // version-scoped tags do not match the current manifest and are ignored.
            var orphans = exactCurrentManagedOrphans(m);
            for (var oi = 0; oi < m.passes.length; oi++) {
                var orphanPass = m.passes[oi], orphanKey = "$" + orphanPass.name;
                if (orphans.footage[orphanKey] > 0) {
                    append(qc.managedObjectRecords("footage", orphanPass, {
                        status: "ownership_error",
                        message: orphans.footage[orphanKey] + " exact-current managed footage item(s) exist without the expected CutBridge package root/comp."
                    }));
                }
                if (orphans.layer[orphanKey] > 0) {
                    append(qc.managedObjectRecords("layer", orphanPass, {
                        status: "ownership_error",
                        message: orphans.layer[orphanKey] + " exact-current managed layer(s) exist without the expected CutBridge package root/comp."
                    }));
                }
            }
            state.comp = null;
        }
        finish();
'''
    replace_once(path, old, new, "package-only orphan guard")


def patch_test() -> None:
    path = ROOT / "tests/ae_s7_native_qc_binding_checks.cjs"
    text = path.read_text(encoding="utf-8")
    marker = "\nconsole.log('S7 native QC+ binding: PASS"
    if "orphan exact-current managed footage" in text:
        return
    if text.count(marker) != 1:
        raise RuntimeError("native binding test marker drifted")
    addition = r'''
{
  const h = host(manifest(), beautyFiles.slice());
  h.click('Build');
  const comp = h.comps()[0];
  const footage = h.footage()[0];
  h.movePackageRoot();
  h.projectItems.splice(h.projectItems.indexOf(comp), 1);
  const beforeItems = h.projectItems.length;
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.match(message, /^CutBridge QC — ERROR/);
  assert.match(message, /ERROR \[CBQ-FOOTAGE-OWNERSHIP-ERROR\] BEAUTY:/);
  assert.match(message, /exact-current managed footage item\(s\) exist without the expected CutBridge package root\/comp/);
  assert.equal(h.footage()[0], footage, 'orphan exact-current managed footage must be reported without mutation');
  assert.equal(h.projectItems.length, beforeItems, 'orphan QC must not remove or relocate managed footage');
}

{
  const m = manifest();
  const h = host(m, beautyFiles.slice());
  // Historical revision-retired footage uses another version-scoped identity and
  // must not make a clean pre-Build current package fail QC.
  h.projectItems.push({
    name: 'retired V000 BEAUTY',
    comment: `CUTBRIDGE|1|footage|Sakura_EP01_SC010_C001_T01_V000|BEAUTY`,
    parentFolder: null
  });
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.match(message, /^CutBridge QC — PASS/);
  assert.doesNotMatch(message, /CBQ-FOOTAGE-OWNERSHIP-ERROR/);
}
'''
    path.write_text(text.replace(marker, addition + marker, 1), encoding="utf-8")


def main() -> int:
    patch_panel()
    patch_test()
    print("S7 orphan managed-tag guard patch applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
