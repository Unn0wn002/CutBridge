/*
 * S6 regression for optional-pass removal across revision + reload + Build/QC.
 * Reuses the native-host-shaped fixture so this executes the actual CutBridge.jsx adapter.
 * Real After Effects validation remains a separate manual gate.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const Module = require("node:module");

const fixturePath = path.resolve(__dirname, "ae_s6_native_host_checks.cjs");
const fixtureSource = fs.readFileSync(fixturePath, "utf8");
const fixtureModule = new Module(fixturePath, module);
fixtureModule.filename = fixturePath;
fixtureModule.paths = Module._nodeModulePaths(path.dirname(fixturePath));
fixtureModule._compile(
    fixtureSource + "\nmodule.exports = { makeHost: makeHost, manifest: manifest, Contract: Contract };\n",
    fixturePath
);

const {makeHost, manifest, Contract} = fixtureModule.exports;
const h = makeHost();
const v1 = manifest(1);
const v2 = manifest(2);

// Use the same deterministic sequence for the optional LINE pass so the fixture
// can exercise the ownership lifecycle without adding unrelated filesystem mocks.
v1.passes.push({
    name: "LINE",
    path: "render/beauty",
    sequence_pattern: "C001_BEAUTY_####.png",
    required: false
});
v1.ae.layer_order = ["BEAUTY", "LINE"];

h.queue(v1);
h.click("Import Package");
h.click("Build Comp");
const comp = h.comps()[0];
assert.equal(comp.numLayers, 2, "V001 should contain required BEAUTY and optional LINE managed layers");
const line = comp._layers.find(layer => layer.name === "LINE");
assert.ok(line, "V001 optional LINE layer should exist");
const lineSource = line.source;
assert.equal(line.comment, Contract.managedTag("layer", v1, "LINE"));

// V002 removes only the optional pass. S6 classifies this as warning/confirm and
// promises to retain the removed optional pass rather than destructively deleting it.
h.queue(v2);
h.click("Update Revision");
assert.strictEqual(line.source, lineSource, "removed optional pass source must be preserved");
assert.equal(comp._layers.includes(line), true, "removed optional pass layer must be preserved");
assert.match(h.alerts.at(-1), /revision updated to V002/i);

// Reload clears in-memory observations. The persisted project state produced by a
// successful revision must remain internally coherent for the new current manifest.
h.reload();
h.queue(v2);
h.click("Import Package");
const footageBeforeBuild = h.footage().length;
const layersBeforeBuild = comp.numLayers;
h.click("Build Comp");
assert.match(
    h.alerts.at(-1),
    /comp built|comp reused safely/i,
    "Build after optional-pass removal must not reject the intentionally retained layer as stale/foreign"
);
assert.equal(comp.numLayers, layersBeforeBuild, "post-revision Build must not duplicate or delete the retained optional layer");
assert.equal(h.footage().length, footageBeforeBuild, "post-revision Build must not import duplicate footage");
assert.strictEqual(line.source, lineSource, "post-revision Build must preserve the retained optional source");

h.click("Run QC");
assert.match(
    h.alerts.at(-1),
    /CutBridge QC — PASS/,
    "QC after optional-pass removal must not fail solely because the intentionally retained optional layer survived"
);

console.log("S6 optional-pass lifecycle: PASS (removed optional layer preserved across revision/reload/Build/QC; real AE MANUAL NOT EXECUTED)");
