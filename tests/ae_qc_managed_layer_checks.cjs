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
  assert.doesNotMatch(message, /CutBridge QC — PASS\b/, label + ': QC must not report clean PASS');
  assert.match(message, /managed layer|managed-layer|layer ownership/i, label + ': QC must report managed-layer ownership failure');
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

console.log('QC managed-layer regression: PASS (required layer presence/ownership must be validated; real AE MANUAL NOT EXECUTED)');
