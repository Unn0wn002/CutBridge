/*
 * Regression for QC managed-layer ownership coverage.
 * Reuses the S5 host-shaped fixture and executes the actual CutBridge.jsx panel.
 * Real After Effects desktop validation remains a separate manual gate.
 */
const assert = require('node:assert/strict');
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

function assertQcFailsManagedLayer(h, label) {
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.doesNotMatch(message, /^CutBridge QC — PASS(?:\n| with)/, label + ': QC must not report a passing headline');
  assert.match(message, /managed layer|managed-layer|layer ownership/i, label + ': QC must report managed-layer ownership failure');
}

function manifestWithOptionalLine() {
  const m = manifest();
  m.passes.push({name: 'LINE', path: 'render/line', sequence_pattern: 'C001_LINE_####.png', required: false});
  m.ae.layer_order = ['BEAUTY', 'LINE'];
  return m;
}

function lineFiles() {
  return [1, 2, 3].map(n => `/packages/桜/render/line/C001_LINE_000${n}.png`);
}

{
  const h = host(manifest(), beautyFiles.slice());
  h.click('Build');
  const comp = h.comps()[0];
  const layer = comp.layer(1);
  const footage = h.footage()[0];
  layer.remove();
  assert.equal(comp.numLayers, 0, 'fixture should remove only the managed layer');
  assert.equal(h.footage()[0], footage, 'managed footage must remain so QC cannot rely on footage failure');
  assertQcFailsManagedLayer(h, 'deleted required managed layer');
}

{
  const h = host(manifest(), beautyFiles.slice());
  h.click('Build');
  const comp = h.comps()[0];
  const layer = comp.layer(1);
  const footage = h.footage()[0];
  layer.comment = '';
  assert.equal(comp.numLayers, 1, 'fixture should keep the de-tagged layer present');
  assert.equal(layer.source, footage, 'fixture should preserve the expected managed footage source');
  assertQcFailsManagedLayer(h, 'de-tagged required managed layer');
}

{
  const m = manifestWithOptionalLine();
  const files = beautyFiles.concat(lineFiles());
  const h = host(m, files);
  h.click('Build');
  const comp = h.comps()[0];
  const line = comp._layers.find(layer => layer.name === 'LINE');
  assert.ok(line, 'fixture should build the complete optional LINE layer');
  line.remove();
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.match(message, /^CutBridge QC — PASS with 1 warning\(s\)/, 'missing complete optional managed layer should warn, not hard-fail');
  assert.match(message, /WARN LINE: optional managed layer is missing from the expected comp/);
  assert.doesNotMatch(message, /ERR\s+LINE:/, 'missing optional layer should not become a hard error when ownership is otherwise unambiguous');
}

{
  const m = manifestWithOptionalLine();
  const lineSequence = lineFiles();
  const files = beautyFiles.concat(lineSequence);
  const h = host(m, files);
  h.click('Build');
  for (const file of lineSequence) {
    const index = files.indexOf(file);
    if (index >= 0) files.splice(index, 1);
  }
  h.click('QC');
  const message = h.alerts.at(-1);
  assert.match(message, /^CutBridge QC — PASS with 1 warning\(s\)/, 'missing optional source sequence should remain the documented warning/skip path');
  assert.match(message, /WARN LINE: optional pass folder missing/);
  assert.doesNotMatch(message, /ERR\s+LINE:/, 'skipped optional source must not become a managed-layer hard error');
}

console.log('QC managed-layer regression: PASS (required ownership fails closed; optional complete-missing layer warns; skipped optional source stays warning-only; real AE MANUAL NOT EXECUTED)');
