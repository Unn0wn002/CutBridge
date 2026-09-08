/*
 * S6 regression for optional-pass removal across the native-host-shaped revision path.
 * Reuses the existing fixture so this executes the actual CutBridge.jsx adapter.
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
// exercises pass-set policy without adding unrelated filesystem mocks.
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
const beauty = comp._layers.find(layer => layer.name === "BEAUTY");
const line = comp._layers.find(layer => layer.name === "LINE");
assert.ok(beauty && line, "V001 managed layers should exist");
const beautySource = beauty.source;
const lineSource = line.source;
const v1Root = h.topRoot(v1.package_name);
assert.ok(v1Root, "V001 package root should exist");
assert.equal(line.comment, Contract.managedTag("layer", v1, "LINE"));

const footageBefore = h.footage().length;
const layersBefore = comp.numLayers;
const replaceBefore = h.replaceFlags.length;
const confirmsBefore = h.confirms.length;

// V002 removes an optional pass. S6 source-only revision must reject pass-set
// removal before confirmation/import/source swap/metadata migration. A deliberate
// rebuild or future migration workflow is required for pass-set changes.
h.queue(v2);
h.click("Update Revision");
assert.match(h.alerts.at(-1), /Revision blocked|Removing an optional pass is unsupported/i);
assert.equal(h.confirms.length, confirmsBefore, "blocked pass removal must not reach confirmation");
assert.equal(h.replaceFlags.length, replaceBefore, "blocked pass removal must not call replaceSource");
assert.equal(h.footage().length, footageBefore, "blocked pass removal must not import replacement footage");
assert.equal(comp.numLayers, layersBefore, "blocked pass removal must not add or remove layers");
assert.strictEqual(beauty.source, beautySource, "blocked pass removal must preserve the active BEAUTY source");
assert.strictEqual(line.source, lineSource, "blocked pass removal must preserve the optional LINE source");
assert.equal(line.comment, Contract.managedTag("layer", v1, "LINE"), "blocked revision must preserve V001 ownership metadata");
assert.equal(comp.comment, Contract.managedTag("comp", v1, v1.ae.comp_name), "blocked revision must preserve V001 comp ownership");
assert.strictEqual(h.topRoot(v1.package_name), v1Root, "blocked revision must preserve the V001 package root");
assert.equal(h.topRoot(v2.package_name), undefined, "blocked revision must not migrate/create a V002 project root");

// Reload the original V001 package and prove the blocked attempt left a coherent,
// idempotent project rather than a half-migrated state.
h.reload();
h.queue(v1);
h.click("Import Package");
h.click("Build Comp");
assert.match(h.alerts.at(-1), /comp reused safely/i);
assert.equal(comp.numLayers, layersBefore);
assert.equal(h.footage().length, footageBefore);
h.click("Run QC");
assert.match(h.alerts.at(-1), /CutBridge QC — PASS/);

console.log("S6 optional-pass lifecycle: PASS (pass removal blocked before mutation; original project remains coherent; real AE MANUAL NOT EXECUTED)");
