const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'apps', 'after-effects', 'CutBridge.jsx'), 'utf8');
const match = source.match(/function ensureManagedLayer\(comp, footage, manifest, passName\) \{([\s\S]*?)\n    \}\n\n    function findVerifiedPass/);
assert(match, 'ensureManagedLayer implementation must be discoverable');

const implementation = `function ensureManagedLayer(comp, footage, manifest, passName) {${match[1]}\n}`;

function runCase(layer) {
  let addCalls = 0;
  const footage = {kind: 'expected-footage'};
  const context = {
    Error,
    CutBridgeContract: {managedTag: () => 'CUTBRIDGE|1|layer|pkg|Beauty'},
    findManagedLayer: () => layer,
    state: {layers: {}},
  };
  vm.createContext(context);
  vm.runInContext(`${implementation}; this.ensureManagedLayer = ensureManagedLayer;`, context);
  const comp = {layers: {add() { addCalls += 1; return {}; }}};
  let error = null;
  try { context.ensureManagedLayer(comp, footage, {}, 'Beauty'); }
  catch (e) { error = e; }
  return {error, addCalls};
}

const nullSourceLayer = {comment: 'CUTBRIDGE|1|layer|pkg|Beauty', source: null, untouched: true};
const nullResult = runCase(nullSourceLayer);
assert(nullResult.error, 'tagged null-source layer must fail closed');
assert.match(String(nullResult.error), /expected footage|source/i);
assert.strictEqual(nullResult.addCalls, 0, 'failure must not create a duplicate managed layer');
assert.strictEqual(nullSourceLayer.untouched, true, 'existing unrelated layer must remain untouched');
assert.strictEqual(nullSourceLayer.source, null, 'existing unrelated layer source must not be replaced');

const unreadableLayer = {comment: 'CUTBRIDGE|1|layer|pkg|Beauty', untouched: true};
Object.defineProperty(unreadableLayer, 'source', {get() { throw new Error('source unavailable'); }});
const unreadableResult = runCase(unreadableLayer);
assert(unreadableResult.error, 'tagged unreadable-source layer must fail closed');
assert.match(String(unreadableResult.error), /source cannot be read|source/i);
assert.strictEqual(unreadableResult.addCalls, 0, 'unreadable source must not create a duplicate managed layer');
assert.strictEqual(unreadableLayer.untouched, true, 'unreadable existing layer must remain untouched');

const wrongFootage = {kind: 'other-footage'};
const wrongResult = runCase({comment: 'CUTBRIDGE|1|layer|pkg|Beauty', source: wrongFootage});
assert(wrongResult.error, 'tagged wrong-source layer must fail closed');
assert.strictEqual(wrongResult.addCalls, 0, 'wrong source must not create a duplicate managed layer');

console.log('S5 managed-layer source guard regressions passed');
