/* S5 partial-retry ordering regression. Node mocks only; AE GUI not executed. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');

const buildStart = source.indexOf('    function buildComp() {');
const buildEnd = source.indexOf('\n    function runQC()', buildStart);
assert.ok(buildStart >= 0 && buildEnd > buildStart, 'buildComp function must exist');
const buildSource = source.slice(buildStart, buildEnd);
assert.match(buildSource, /\n\s*orderManagedLayers\(comp, m\);/,
  'buildComp must normalize managed layer order after all passes are ensured');
assert.doesNotMatch(buildSource, /if\s*\(\s*compResult\.created\s*\)\s*orderManagedLayers/,
  'managed ordering must not be limited to newly created comps');

const contractContext = {module: {exports: {}}};
vm.createContext(contractContext);
vm.runInContext(source, contractContext);
const contract = contractContext.module.exports;

const orderStart = source.indexOf('    function orderManagedLayers(comp, manifest) {');
const orderEnd = source.indexOf('\n    function buildComp()', orderStart);
assert.ok(orderStart >= 0 && orderEnd > orderStart, 'orderManagedLayers function must exist');
const orderSource = source.slice(orderStart, orderEnd);

const manifest = {
  package_name: '桜_EP01_SC010_C001_T01_V001',
  passes: [{name: 'BEAUTY'}, {name: 'LINE'}],
  ae: {layer_order: ['BEAUTY', 'LINE']}
};

const layers = [];
function makeLayer(name, comment) {
  return {
    name,
    comment,
    moveToBeginning() {
      const index = layers.indexOf(this);
      assert.ok(index >= 0);
      layers.splice(index, 1);
      layers.unshift(this);
    }
  };
}

const artistA = makeLayer('ARTIST_A', '');
const artistB = makeLayer('ARTIST_B', '');
const beauty = makeLayer('BEAUTY', contract.managedTag('layer', manifest, 'BEAUTY'));

// State after first attempt: BEAUTY succeeded, LINE failed and rolled back.
layers.push(artistA, beauty, artistB);
const beforeArtistOrder = layers.filter(x => !x.comment).map(x => x.name);

// Retry: AE adds LINE at the beginning of the reused comp.
const line = makeLayer('LINE', contract.managedTag('layer', manifest, 'LINE'));
layers.unshift(line);

const context = {
  CutBridgeContract: contract,
  findManagedLayer(comp, tag) {
    return comp._layers.find(layer => layer.comment === tag) || null;
  }
};
vm.createContext(context);
vm.runInContext(orderSource + '\nthis.orderManagedLayers = orderManagedLayers;', context);

const comp = {
  _layers: layers,
  get numLayers() { return this._layers.length; },
  layer(index) { return this._layers[index - 1]; }
};
context.orderManagedLayers(comp, manifest);

const managedNames = layers.filter(x => x.comment).map(x => x.name);
assert.deepEqual(managedNames, ['BEAUTY', 'LINE'], 'retry must restore manifest managed-layer order');
assert.equal(layers.filter(x => x === beauty).length, 1, 'BEAUTY must not be duplicated');
assert.equal(layers.filter(x => x === line).length, 1, 'LINE must not be duplicated');
assert.deepEqual(layers.filter(x => !x.comment).map(x => x.name), beforeArtistOrder,
  'manual artist layer relative order must be preserved');
assert.equal(layers.length, 4, 'ordering must not add or remove layers');

console.log('PASS: S5 partial-retry managed layer ordering regression (Node mocks; AE GUI not executed)');
