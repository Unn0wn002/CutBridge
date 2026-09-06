/* Node-only regression harness. Host mocks do not certify After Effects runtime. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');
const version = fs.readFileSync(path.join(root, 'apps/blender/cutbridge/blender_manifest.toml'), 'utf8').match(/^version = "([^"]+)"/m)[1];
function contractContext(legacy = false) {
    const context = {module: {exports: {}}};
    if (legacy) context.JSON = undefined;
    vm.createContext(context);
    vm.runInContext(source, context);
    return {context, c: context.module.exports};
}
const {context, c} = contractContext();
const plain = value => JSON.parse(JSON.stringify(value));
function manifest() {
    return {schema: 'cutbridge-manifest', schema_version: 1, cutbridge_version: version,
        project: '桜', episode: 'EP01', scene: 'SC010', cut: 'C001', take: 'T01', version: 1,
        fps: 24, resolution: {width: 1920, height: 1080, pixel_aspect: 1},
        frames: {start: 1, end: 3, count: 3},
        passes: [{name: 'BEAUTY', path: 'render/beauty', sequence_pattern: 'C001_BEAUTY_####.png', required: true}]};
}
if (process.argv[2] === '--manifest') {
    const m = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
    assert.deepEqual(plain(c.validateManifest(m)), []);
    const names = JSON.parse(process.argv[4]);
    const coverage = c.sequenceCoverage(m.passes[0], m, names);
    assert.equal(coverage.complete, true);
    assert.deepEqual(plain(coverage.unexpected), []);
    console.log('PASS: live Blender producer -> schema-tested manifest -> AE filename contract');
    process.exit(0);
}
let checks = 0;
function check(name, fn) { fn(); checks++; }
check('host and third-realm arrays accepted', () => {
    assert.deepEqual(plain(c.validateManifest(manifest())), []);
    const other = vm.runInNewContext('(' + JSON.stringify(manifest()) + ')');
    assert.deepEqual(plain(c.validateManifest(other)), []);
    for (const passes of [{0: manifest().passes[0], length: 1}, null, [], 'passes']) {
        const m = manifest(); m.passes = passes;
        assert.match(c.validateManifest(m).join(' '), /no render passes/);
    }
});
check('positive, zero-based and single frame ranges', () => {
    for (const [start, end] of [[1, 3], [0, 2], [0, 0], [10001, 10003]]) {
        const m = manifest(); m.frames = {start, end, count: end - start + 1};
        assert.deepEqual(plain(c.validateManifest(m)), []);
        const names = Array.from({length: m.frames.count}, (_, i) => `C001_BEAUTY_${String(start + i).padStart(4, '0')}.png`);
        const coverage = c.sequenceCoverage(m.passes[0], m, names);
        assert.equal(coverage.complete, true); assert.deepEqual(plain(coverage.unexpected), []);
        assert.equal(coverage.firstName, names[0]);
    }
});
check('negative exports consistently rejected', () => {
    for (const [start, end] of [[-3, -1], [-1, 1]]) {
        const m = manifest(); m.frames = {start, end, count: end - start + 1};
        assert.match(c.validateManifest(m).join(' '), /Rebase the cut and preroll/);
        assert.throws(() => c.sequenceCoverage(m.passes[0], m, []), /Negative export/);
    }
    assert.throws(() => c.expectedFrameName('cut_####.png', -1), /non-negative/);
});
check('invalid numeric semantics rejected without entering coverage loop', () => {
    for (const key of ['start', 'end', 'count']) for (const value of [1.5, NaN, Infinity, -Infinity, '1', null, 9007199254740992]) {
        const m = manifest(); m.frames[key] = value;
        assert.ok(c.validateManifest(m).length, `${key}: ${value}`);
        assert.throws(() => c.sequenceCoverage(m.passes[0], m, []));
    }
    for (const frames of [{start: 3, end: 1, count: -1}, {start: 1, end: 3, count: 2}, {start: 0, end: 0, count: 0}]) {
        const m = manifest(); m.frames = frames; assert.match(c.validateManifest(m).join(' '), /inconsistent/);
    }
    for (const value of [0, -1, NaN, Infinity, '24', null]) {
        const m = manifest(); m.fps = value; assert.match(c.validateManifest(m).join(' '), /FPS/);
    }
    for (const key of ['width', 'height']) for (const value of [0, 1.5, Infinity, '1920', null]) {
        const m = manifest(); m.resolution[key] = value; assert.match(c.validateManifest(m).join(' '), /resolution/);
    }
    for (const value of [0, -1, NaN, Infinity, '1']) {
        const m = manifest(); m.resolution.pixel_aspect = value; assert.match(c.validateManifest(m).join(' '), /pixel_aspect/);
    }
});
check('schema identifiers and required fields checked', () => {
    for (const [key, value] of [['schema', 'other'], ['schema_version', 2], ['schema_version', '1'], ['version', 1.2], ['cutbridge_version', undefined]]) {
        const m = manifest(); m[key] = value; assert.ok(c.validateManifest(m).length);
    }
    for (const value of ['false', 0, null]) {
        const m = manifest(); m.passes[0].required = value; assert.match(c.validateManifest(m).join(' '), /boolean/);
    }
    const m = manifest(); delete m.passes[0].required; assert.deepEqual(plain(c.validateManifest(m)), []);
});
check('package-relative paths reject traversal, absolute and URI forms', () => {
    const bad = ['', ' ', '/', '/tmp/render', 'C:/render', 'C:\\render', 'C:render', '\\\\server\\share', '../render', '..\\render',
        'render/../outside', 'render\\..\\outside', 'render/..\\../outside', 'render//beauty', 'render/./beauty',
        'render/.. /outside', 'render/beauty.', 'render/%2e%2e/outside', 'render/%252e%252e/outside', '~user/render',
        'file:///tmp/render', 'render/\u0000beauty', null, {}, 42];
    for (const value of bad) {
        const m = manifest(); m.passes[0].path = value;
        assert.ok(c.validateManifest(m).length, JSON.stringify(value));
        assert.throws(() => c.relativePassPath(value));
    }
    for (const value of ['render/beauty', 'レンダー/線画', 'render\\線画', 'render/shot 01']) {
        const m = manifest(); m.passes[0].path = value; assert.deepEqual(plain(c.validateManifest(m)), []);
    }
    assert.equal(c.relativePassPath('render\\線画'), 'render/線画');
    assert.equal(c.pathIsInside('/package', '/package-other/render'), false);
    assert.equal(c.pathIsInside('/package', '/package/render'), true);
    assert.equal(c.pathIsInside('C:\\Package', 'c:\\package\\render'), true);
});
check('sequence patterns cannot carry paths or malformed tokens', () => {
    for (const pattern of ['../####.png', '..\\####.png', '/####.png', 'C:####.png', '%2e%2e_####.png', 'cut_#####.png',
        'cut_###.png', 'cut_####_####.png', 'cut_####?.png', 'cut_####*.png', '', null]) {
        assert.throws(() => c.patternToRegex(pattern), undefined, String(pattern));
    }
    assert.equal(c.expectedFrameName('カット(線)+_####.png', 0), 'カット(線)+_0000.png');
    assert.equal(c.patternToRegex('カット(線)+_####.png').test('カット(線)+_0000.png'), true);
});
check('coverage distinguishes missing, extra and badly padded filenames', () => {
    const m = manifest(), p = m.passes[0];
    const names = ['C001_BEAUTY_0001.png', 'C001_BEAUTY_0003.png', 'C001_BEAUTY_2.png', 'C001_BEAUTY_00002.png',
        'C001_BEAUTY_-0001.png', 'C001_BEAUTY_0004.png', 'unrelated.png'];
    const coverage = c.sequenceCoverage(p, m, names);
    assert.equal(coverage.complete, false); assert.equal(coverage.firstName, null);
    assert.deepEqual(plain(coverage.missing), [2]);
    assert.deepEqual(plain(coverage.unexpected), names.slice(2, 6));
});
check('AE-facing version equals canonical extension version', () => assert.equal(c.PRODUCT_VERSION, version));
check('legacy JSON parser accepts data without eval', () => {
    const legacy = contractContext(true).c;
    const m = manifest(); m.project = '桜\\\"\n\t\r\b\f😀'; m.extra = [true, false, null, -1.25e-3, {'constructor': 'data'}];
    assert.deepEqual(plain(legacy.parseJSON(JSON.stringify(m))), m);
    assert.deepEqual(plain(legacy.parseJSON('{"x":"\\u685c"}')), {x: '桜'});
    for (const text of ['({x:1})', '{"x":(function(){return 1;})()}', '{"x":undefined}', '{"x":NaN}', '{"x":01}', '[1,]', '{"x":1,}',
        '{"x":"\\q"}', '{"x":"\n"}', '{"x":true}junk', '{"__proto__":{"x":1}}', '', '[', '{', '"unterminated']) {
        assert.throws(() => legacy.parseJSON(text), /Invalid JSON/, text);
    }
});

function host(m, files, aliases = []) {
    const controls = [], alerts = [], imports = [], folders = [], comps = [], footageItems = [];
    const packageRoot = '/packages/桜';
    const normalize = value => path.posix.normalize(decodeURIComponent(String(value).replaceAll('\\', '/')));
    function Folder(value) { this.fsName = normalize(value); this.alias = aliases.includes(this.fsName); this.exists = this.fsName === packageRoot || files.some(f => f.startsWith(this.fsName + '/')); }
    Folder.prototype.getFiles = function(filter) { return files.filter(f => path.posix.dirname(f) === this.fsName).map(f => new File(f)).filter(filter); };
    function File(value) { this.fsName = normalize(value); this.name = encodeURIComponent(path.posix.basename(this.fsName)); this.exists = files.includes(this.fsName); this.alias = aliases.includes(this.fsName); }
    File.decode = decodeURIComponent;
    File.openDialog = () => ({parent: new Folder(packageRoot), open: () => true, read: () => JSON.stringify(m), close() {}});
    function Window() { this.layout = {resize() {}, layout() {}}; }
    Window.prototype.add = function(type, unused, text) { const control = {type, text, graphics: {font: {name: 'Arial'}}, preferredSize: {}}; controls.push(control); return control; };
    Window.prototype.center = Window.prototype.show = function() {};
    function FolderItem(name) { this.name = name; }
    function FootageItem(file) { this.file = file; this.mainSource = {conformFrameRate: 0}; this.comment = ''; this.parentFolder = null; this.name = ''; }
    function CompItem(name, width, height, aspect, duration, fps) {
        Object.assign(this, {name, width, height, pixelAspect: aspect, duration, frameRate: fps, numLayers: 0});
        this.layers = {add: () => {this.numLayers++; return {};}}; this.openInViewer = () => {};
    }
    const project = {rootFolder: {}, numItems: 0, item: i => [...folders, ...comps, ...footageItems][i - 1], items: {
        addFolder(name) { const f = new FolderItem(name); folders.push(f); project.numItems++; return f; },
        addComp(...args) { const comp = new CompItem(...args); comps.push(comp); project.numItems++; return comp; }
    }, importFile(io) { imports.push(io); const item = new FootageItem(io.file); footageItems.push(item); project.numItems++; return item; }};
    const runtime = {File, Folder, Window, Panel: function() {}, FolderItem, FootageItem, CompItem,
        ImportOptions: function(file) {this.file = file;}, ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}},
        alert: message => alerts.push(message), $: {writeln() {}},
        app: {project, beginUndoGroup() {}, endUndoGroup() {}}};
    vm.createContext(runtime); vm.runInContext(source, runtime);
    return {click: word => controls.find(x => x.type === 'button' && x.text.includes(word)).onClick(), alerts, imports, comps};
}
const beautyFiles = [1, 2, 3].map(n => `/packages/桜/render/beauty/C001_BEAUTY_000${n}.png`);
check('required missing frames block actual host-adapter import', () => {
    const h = host(manifest(), [beautyFiles[0], beautyFiles[2]]); h.click('Build');
    assert.equal(h.imports.length, 0); assert.match(h.alerts.join(' '), /required pass.*missing frame\(s\): 2/);
});
check('optional absent/incomplete passes warn and skip; required default blocks', () => {
    for (const files of [beautyFiles, [...beautyFiles, '/packages/桜/render/line/C001_LINE_0001.png']]) {
        const m = manifest(); m.passes.push({name: 'LINE', path: 'render/line', sequence_pattern: 'C001_LINE_####.png', required: false});
        const h = host(m, files); h.click('Build'); h.click('QC');
        assert.equal(h.imports.length, 1); assert.match(h.alerts.join(' '), /optional pass skipped/); assert.match(h.alerts.at(-1), /warning/);
    }
    const m = manifest(); delete m.passes[0].required;
    const h = host(m, []); h.click('Build'); assert.equal(h.imports.length, 0); assert.match(h.alerts.join(' '), /required pass/);
});
check('extras reach build and QC diagnostics', () => {
    const h = host(manifest(), [...beautyFiles, '/packages/桜/render/beauty/C001_BEAUTY_0004.png']);
    h.click('Build'); h.click('QC'); assert.equal(h.imports.length, 1);
    assert.ok(h.alerts.every(text => /unexpected matching filename/.test(text)));
});
check('Unicode filenames are decoded from ExtendScript URI names', () => {
    const m = manifest(); m.passes[0].path = 'レンダー/線画'; m.passes[0].sequence_pattern = 'カット_####.png';
    const h = host(m, [1, 2, 3].map(n => `/packages/桜/レンダー/線画/カット_000${n}.png`)); h.click('Build');
    assert.equal(h.imports.length, 1); assert.equal(h.imports[0].file.fsName, '/packages/桜/レンダー/線画/カット_0001.png');
});
check('folder and file aliases never reach import', () => {
    for (const alias of ['/packages/桜/render', '/packages/桜/render/beauty', beautyFiles[0]]) {
        const h = host(manifest(), beautyFiles, [alias]); h.click('Build'); assert.equal(h.imports.length, 0); assert.match(h.alerts.join(' '), /aliases/);
    }
});
console.log(`PASS: ${checks} AE contract/host-adapter regression groups (Node mocks; AE GUI not executed)`);
