/* Regression for producer/consumer package identity binding. Host mocks do not certify native AE. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');
const context = {module: {exports: {}}};
vm.createContext(context);
vm.runInContext(source, context);
const contract = context.module.exports;
const plain = value => JSON.parse(JSON.stringify(value));

function manifest() {
    return {
        schema: 'cutbridge-manifest',
        schema_version: 1,
        cutbridge_version: '0.2.3',
        project: '桜',
        episode: 'EP01',
        scene: 'SC010',
        cut: 'C001',
        take: 'T01',
        version: 1,
        package_name: '桜_EP01_SC010_C001_T01_V001',
        fps: 24,
        resolution: {width: 1920, height: 1080, pixel_aspect: 1},
        frames: {start: 0, end: 2, count: 3},
        passes: [{name: 'BEAUTY', path: 'render/beauty', sequence_pattern: 'C001_BEAUTY_####.png', required: true}],
        ae: {comp_name: 'C001_COMP', layer_order: ['BEAUTY']},
    };
}

let checks = 0;
function check(name, fn) { fn(); checks++; }

check('canonical Blender package_name is accepted', () => {
    const m = manifest();
    assert.deepEqual(plain(contract.validateManifest(m)), []);
});

check('legacy manifest may omit package_name', () => {
    const m = manifest();
    delete m.package_name;
    assert.deepEqual(plain(contract.validateManifest(m)), []);
});

check('present package_name must be a string', () => {
    const m = manifest();
    m.package_name = 123;
    assert.match(contract.validateManifest(m).join(' '), /package_name/i);
});

check('unchanged package_name cannot alias a changed logical identity', () => {
    for (const [field, value] of [
        ['project', '別作品'],
        ['episode', 'EP02'],
        ['scene', 'SC011'],
        ['cut', 'C002'],
        ['take', 'T02'],
        ['version', 2],
    ]) {
        const m = manifest();
        m[field] = value;
        assert.match(contract.validateManifest(m).join(' '), /package_name.*identity|identity.*package_name/i, field);
    }
});

check('AE canonical sanitization matches Blender package_name contract', () => {
    const m = manifest();
    m.project = '  桜 project  ';
    m.episode = 'EP:01';
    m.scene = 'SC/010';
    m.cut = 'C\\001';
    m.take = 'T?01';
    m.version = 7;
    m.package_name = '桜_project_EP_01_SC_010_C_001_T_01_V007';
    m.ae.comp_name = 'C_001_COMP';
    assert.deepEqual(plain(contract.validateManifest(m)), []);
});

check('invalid filesystem character runs collapse exactly like Blender', () => {
    const m = manifest();
    m.project = 'A<>:"/\\|?*B';
    m.package_name = 'A_B_EP01_SC010_C001_T01_V001';
    assert.deepEqual(plain(contract.validateManifest(m)), []);
});

console.log(`PASS: ${checks} AE package identity checks`);
