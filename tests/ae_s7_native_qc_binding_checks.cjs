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
