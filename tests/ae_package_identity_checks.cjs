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

// Run the same boundaries with native JSON and the ExtendScript fallback parser.
// The exact tuple is ownership evidence; a sanitized filename is not its substitute.
const revisionSource = fs.readFileSync(path.join(root, 'apps/after-effects/revision_manager.js'), 'utf8');
const pythonWhitespace = [9, 10, 11, 12, 13, 28, 29, 30, 31, 32, 0x85, 0xa0, 0x1680,
    0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006, 0x2007, 0x2008, 0x2009,
    0x200a, 0x2028, 0x2029, 0x202f, 0x205f, 0x3000];
const ids = ['project', 'episode', 'scene', 'cut', 'take'];
const fallbacks = ['PROJECT', 'EP00', 'SC000', 'C000', 'T01'];
const producerCases = process.argv.includes('--producer-cases') ? JSON.parse(fs.readFileSync(0, 'utf8')) : [];
let boundaries = 0;
for (const fallbackJSON of [false, true]) {
    const ctx = {module: {exports: {}}};
    if (fallbackJSON) ctx.JSON = undefined;
    vm.runInNewContext(source, ctx);
    const C = ctx.module.exports;
    const revContext = {CutBridgeContract: C};
    vm.runInNewContext(revisionSource, revContext);
    const R = revContext.CutBridgeRevisionManager;
    const roundtrip = m => C.parseJSON(JSON.stringify(m));
    function accepted(m) {
        assert.deepEqual(plain(C.validateManifest(roundtrip(m))), []);
        boundaries++;
    }
    function withToken(field, raw, token) {
        const m = manifest();
        m[field] = raw;
        const parts = ['桜', 'EP01', 'SC010', 'C001', 'T01', 'V001'];
        parts[ids.indexOf(field)] = token;
        m.package_name = parts.join('_');
        return m;
    }
    function newer(m) {
        const n = plain(m);
        n.version = 2;
        if (typeof n.package_name === 'string') n.package_name = n.package_name.replace(/V001$/, 'V002');
        return n;
    }
    for (const [index, field] of ids.entries()) {
        for (const cp of pythonWhitespace) {
            const w = String.fromCharCode(cp);
            for (const [raw, token] of [[w + '桜', '桜'], ['桜' + w, '桜'],
                [w + '桜' + w, '桜'], ['A' + w + w + 'B', 'A_B']]) {
                const m = withToken(field, raw, token);
                accepted(m);
                assert.equal(R.assess(roundtrip(m), roundtrip(newer(m))).status, 'safe', `${field} U+${cp.toString(16)}`);
            }
            const blank = withToken(field, w + w, fallbacks[index]);
            accepted(blank); // S5 compatibility; Blender Build and S6 reject blank tuples.
            assert.match(R.assess(blank, newer(blank)).reasons.join(' '), /non-empty/, `${field} blank U+${cp.toString(16)}`);
        }
        const empty = withToken(field, '', fallbacks[index]);
        accepted(empty);
        assert.match(R.assess(empty, newer(empty)).reasons.join(' '), /non-empty/);
        for (const bad of [undefined, null, 17, false, [], {}]) {
            const m = manifest();
            m[field] = bad;
            assert.match(C.validateManifest(roundtrip(m)).join(' '), /must be a string/);
            assert.equal(R.assess(m, newer(m)).status, 'incompatible');
        }
        for (const raw of ['Normal009du', '桜🌸', 'é', 'e\u0301', '\ufeff', '\u180e', '\u200b',
            'A\ufeffB', '\u180e桜\u180e', '\u200b桜\u200b']) {
            const m = withToken(field, raw, raw);
            accepted(m);
            assert.equal(R.assess(roundtrip(m), roundtrip(newer(m))).status, 'safe');
        }
        for (const raw of ['A B', ' A_B ', 'A<>B']) {
            const m = withToken(field, raw, 'A_B');
            const other = withToken(field, 'A_B', 'A_B');
            accepted(m);
            accepted(other);
            assert.notEqual(R.identity(m), R.identity(other));
            assert.notEqual(R.ownershipKey(m, 'BEAUTY'), R.ownershipKey(other, 'BEAUTY'));
            assert.match(R.assess(m, newer(other)).reasons.join(' '), /identity differs/);
        }
    }
    const original = manifest();
    for (const invalid of ['', ' ', '\u0085', null, false, 0, [], {},
        ' ' + original.package_name, original.package_name + ' ', '\ufeff' + original.package_name,
        original.package_name.toLowerCase(), '../' + original.package_name]) {
        const m = {...original, package_name: invalid};
        assert.match(C.validateManifest(roundtrip(m)).join(' '), /package_name/);
        assert.equal(R.assess(m, newer(m)).status, 'incompatible');
    }
    delete original.package_name;
    accepted(original);
    assert.equal(R.assess(original, newer(original)).status, 'safe');
    for (const m of producerCases) {
        accepted(m);
        assert.equal(R.assess(roundtrip(m), roundtrip(newer(m))).status, 'safe');
    }
}
console.log(`PASS: ${boundaries} package identity boundaries (native/fallback JSON)`);
