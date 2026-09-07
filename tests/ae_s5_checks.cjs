/* S5 Node host-adapter regression harness. This does not certify After Effects GUI/runtime. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');
const version = fs.readFileSync(path.join(root, 'apps/blender/cutbridge/blender_manifest.toml'), 'utf8').match(/^version = "([^"]+)"/m)[1];

function manifest() {
  return {
    schema: 'cutbridge-manifest', schema_version: 1, cutbridge_version: version,
    project: '桜', episode: 'EP01', scene: 'SC010', cut: 'C001', take: 'T01', version: 1,
    package_name: '桜_EP01_SC010_C001_T01_V001', fps: 24,
    resolution: {width: 1920, height: 1080, pixel_aspect: 1},
    frames: {start: 1, end: 3, count: 3},
    passes: [{name: 'BEAUTY', path: 'render/beauty', sequence_pattern: 'C001_BEAUTY_####.png', required: true}],
    ae: {comp_name: 'C001_COMP', layer_order: ['BEAUTY']}
  };
}

function contract() {
  const context = {module: {exports: {}}};
  vm.createContext(context);
  vm.runInContext(source, context);
  return context.module.exports;
}

function host(m, files, options = {}) {
  const controls = [], alerts = [], projectItems = [], imports = [];
  const packageRoot = '/packages/桜';
  const normalize = value => path.posix.normalize(decodeURIComponent(String(value).replaceAll('\\', '/')));

  function Folder(value) {
    this.fsName = normalize(value);
    this.alias = false;
    this.exists = this.fsName === packageRoot || files.some(f => f.startsWith(this.fsName + '/'));
  }
  Folder.prototype.getFiles = function(filter) {
    return files.filter(f => path.posix.dirname(f) === this.fsName).map(f => new File(f)).filter(filter);
  };
  function File(value) {
    this.fsName = normalize(value);
    this.name = encodeURIComponent(path.posix.basename(this.fsName));
    this.exists = files.includes(this.fsName);
    this.alias = false;
  }
  File.decode = decodeURIComponent;
  File.openDialog = () => ({parent: new Folder(packageRoot), open: () => true, read: () => JSON.stringify(m), close() {}});

  function Window() { this.layout = {resize() {}, layout() {}}; }
  Window.prototype.add = function(type, unused, text) {
    const control = {type, text, graphics: {font: {name: 'Arial'}}, preferredSize: {}};
    controls.push(control); return control;
  };
  Window.prototype.center = Window.prototype.show = function() {};
  function Panel() {}

  function FolderItem(name) { this.name = name; this.parentFolder = null; this.comment = ''; }
  function FootageItem(file) {
    this.name = ''; this.parentFolder = null; this.comment = ''; this.file = file;
    this._conformGetterThrows = false; this._conformUnavailable = false;
    let conformFrameRate = 0;
    this.mainSource = {};
    Object.defineProperty(this.mainSource, 'conformFrameRate', {
      enumerable: true,
      get: () => {
        if (this._conformGetterThrows) throw new Error('mock conform getter failure');
        return this._conformUnavailable ? undefined : conformFrameRate;
      },
      set(value) {
        if (options.conformSetterThrows) throw new Error('mock conform setter failure');
        conformFrameRate = options.conformRefuses ? 30 : value;
      }
    });
  }
  function Layer(comp, sourceItem) {
    this.containingComp = comp; this.comp = comp; this.source = sourceItem; this.name = ''; this.comment = ''; this.startTime = 0;
  }
  Layer.prototype.moveToBeginning = function() {
    const list = this.comp._layers, index = list.indexOf(this);
    if (index >= 0) { list.splice(index, 1); list.unshift(this); }
  };
  function CompItem(name, width, height, aspect, duration, fps) {
    this.name = name; this.width = width; this.height = height; this.pixelAspect = aspect;
    this.duration = duration; this.frameRate = fps; this.parentFolder = null; this.comment = ''; this._layers = [];
    const self = this;
    this.layers = {add(sourceItem) { const layer = new Layer(self, sourceItem); self._layers.unshift(layer); return layer; }};
    this.openInViewer = () => {};
  }
  Object.defineProperty(CompItem.prototype, 'numLayers', {get() { return this._layers.length; }});
  CompItem.prototype.layer = function(index) { return this._layers[index - 1]; };

  const project = {rootFolder: {name: 'ROOT'}, item: i => projectItems[i - 1], items: {
    addFolder(name) { const f = new FolderItem(name); projectItems.push(f); return f; },
    addComp(...args) { const c = new CompItem(...args); projectItems.push(c); return c; }
  }, importFile(io) {
    const item = new FootageItem(io.file);
    item.remove = () => { const index = projectItems.indexOf(item); if (index >= 0) projectItems.splice(index, 1); };
    projectItems.push(item); imports.push(item); return item;
  }};
  Object.defineProperty(project, 'numItems', {get() { return projectItems.length; }});

  function ImportOptions(file) { this.file = file; this.sequence = false; this.forceAlphabetical = true; }
  ImportOptions.prototype.canImportAs = () => true;
  const runtime = {File, Folder, Window, Panel, FolderItem, FootageItem, CompItem, AVLayer: Layer, ImportOptions, ImportAsType: {FOOTAGE: 1},
    ScriptUI: {newFont() {}}, alert: message => alerts.push(String(message)), $: {writeln() {}},
    app: {project, beginUndoGroup() {}, endUndoGroup() {}, newProject() {}}};
  vm.createContext(runtime); vm.runInContext(source, runtime);

  function reloadScript() { controls.length = 0; vm.runInContext(source, runtime); }

  function click(word) {
    const button = controls.find(x => x.type === 'button' && x.text.includes(word));
    assert.ok(button, `missing ${word} button`); button.onClick();
  }
  function rootFolder() { return projectItems.find(x => x instanceof FolderItem && x.parentFolder === project.rootFolder && x.name === m.package_name); }
  function compFolder() { const root = rootFolder(); return projectItems.find(x => x instanceof FolderItem && x.parentFolder === root && x.name === '01_COMP'); }
  function renderFolder() { const root = rootFolder(); return projectItems.find(x => x instanceof FolderItem && x.parentFolder === root && x.name === '02_RENDER'); }
  function comps() { return projectItems.filter(x => x instanceof CompItem); }
  function footage() { return projectItems.filter(x => x instanceof FootageItem); }
  function seedPackageFolders() {
    const root = project.items.addFolder(m.package_name); root.parentFolder = project.rootFolder;
    const cf = project.items.addFolder('01_COMP'); cf.parentFolder = root;
    const rf = project.items.addFolder('02_RENDER'); rf.parentFolder = root;
    for (const name of ['03_PRECOMP', '04_OUTPUT']) { const f = project.items.addFolder(name); f.parentFolder = root; }
    return {root, cf, rf};
  }
  function seedManualComp() {
    const {cf} = seedPackageFolders();
    const spec = m.resolution;
    const c = project.items.addComp(m.ae.comp_name, spec.width, spec.height, spec.pixel_aspect, m.frames.count / m.fps, m.fps);
    c.parentFolder = cf; return c;
  }
  function seedWrongTypeFootageTag(passName = 'BEAUTY') {
    const {rf} = seedPackageFolders();
    const wrong = new FolderItem('WRONG_TYPE');
    wrong.parentFolder = rf;
    wrong.comment = `CUTBRIDGE|1|footage|${m.package_name}|${passName}`;
    projectItems.push(wrong);
    return wrong;
  }
  function seedArtistWork(comp) {
    const item = new FootageItem(new File('/artist/reference.png'));
    item.name = 'Artist reference'; item.comment = 'Artist notes'; item.parentFolder = renderFolder();
    projectItems.push(item);
    const layer = comp.layers.add(item); layer.name = 'Artist title'; layer.comment = 'Artist layer notes';
    return {item, layer};
  }
  function moveLayer(layer, from) {
    const other = project.items.addComp('Artist comp', 640, 360, 1, 1, 24);
    other.parentFolder = project.rootFolder;
    from._layers.splice(from._layers.indexOf(layer), 1); other._layers.push(layer);
    layer.containingComp = other; layer.comp = other;
  }
  function duplicateFootage(original) {
    const item = new FootageItem(original.file);
    item.name = original.name; item.comment = original.comment; item.parentFolder = original.parentFolder;
    item.mainSource.conformFrameRate = original.mainSource.conformFrameRate;
    projectItems.push(item); return item;
  }
  function driftFootageSource(item, filePath) { item.file = new File(filePath); }
  function breakFootageFpsRead(item, mode) {
    item._conformGetterThrows = mode === 'throw';
    item._conformUnavailable = mode === 'unavailable';
  }
  return {click, reloadScript, seedArtistWork, moveLayer, duplicateFootage, alerts, imports, projectItems, comps, footage, compFolder, renderFolder, seedManualComp, seedWrongTypeFootageTag, driftFootageSource, breakFootageFpsRead};
}

const beautyFiles = [1, 2, 3].map(n => `/packages/桜/render/beauty/C001_BEAUTY_000${n}.png`);
let checks = 0;
function check(name, fn) { fn(); checks++; }

check('contract exposes deterministic managed identity and comp spec checks', () => {
  const c = contract(), m = manifest();
  assert.equal(c.managedIdentity(m), m.package_name);
  assert.match(c.managedTag('comp', m, m.ae.comp_name), /^CUTBRIDGE\|1\|comp\|/);
  const expected = c.expectedCompSpec(m);
  assert.deepEqual(JSON.parse(JSON.stringify(c.compSpecErrors(expected, expected))), []);
  assert.deepEqual(JSON.parse(JSON.stringify(c.compSpecErrors(expected, {...expected, frameRate: 30}))), ['frame rate']);
  assert.deepEqual(JSON.parse(JSON.stringify(c.footageReuseErrors(
    {path: '/pkg/render/beauty/C001_0001.png', frameRate: 24},
    {isFootage: true, path: '/pkg/render/beauty/C001_0001.png', conformFrameRate: 24}
  ))), []);
  assert.deepEqual(JSON.parse(JSON.stringify(c.footageReuseErrors(
    {path: '/pkg/render/beauty/C001_0001.png', frameRate: 24},
    {isFootage: true, path: '/pkg/render/beauty/C001_0001.png', conformFrameRate: null}
  ))), ['frame rate']);
  assert.deepEqual(JSON.parse(JSON.stringify(c.footageReuseErrors(
    {path: '/pkg/render/beauty/C001_0001.png', frameRate: 24},
    {isFootage: true, path: '/pkg/render/beauty/C001_0001.png', conformFrameRate: undefined}
  ))), ['frame rate']);
});

check('duplicate pass names and invalid layer order are rejected before runtime', () => {
  const c = contract();
  const duplicate = manifest(); duplicate.passes.push({...duplicate.passes[0]});
  assert.match(c.validateManifest(duplicate).join(' '), /duplicate render pass name/);
  const unknown = manifest(); unknown.ae.layer_order = ['LINE'];
  assert.match(c.validateManifest(unknown).join(' '), /unknown pass/);
  const dupOrder = manifest(); dupOrder.ae.layer_order = ['BEAUTY', 'BEAUTY'];
  assert.match(c.validateManifest(dupOrder).join(' '), /duplicate pass/);
});

check('prototype-key pass names remain valid and deterministic', () => {
  const c = contract();
  for (const name of ['constructor', 'toString', '__proto__']) {
    const m = manifest(); m.passes[0].name = name; m.ae.layer_order = [name];
    assert.deepEqual(Array.from(c.validateManifest(m)), [], `${name} should not be treated as an inherited membership key`);
    assert.deepEqual(Array.from(c.passNames(m)), [name]);
  }
});

check('required-pass preflight fails before creating project items', () => {
  const h = host(manifest(), [beautyFiles[0], beautyFiles[2]]);
  h.click('Build');
  assert.equal(h.projectItems.length, 0);
  assert.equal(h.imports.length, 0);
  assert.match(h.alerts.join(' '), /required pass.*missing frame\(s\): 2/);
});

check('repeated Build is idempotent for managed comp footage and layer', () => {
  const h = host(manifest(), beautyFiles);
  h.click('Build'); h.click('Build');
  assert.equal(h.comps().length, 1);
  assert.equal(h.footage().length, 1);
  assert.equal(h.comps()[0].numLayers, 1);
  assert.match(h.alerts.at(-1), /reused safely/);
});

check('reload then Build rediscovers managed project items instead of duplicating', () => {
  const h = host(manifest(), beautyFiles);
  h.click('Build'); h.click('Import Package'); h.click('Build');
  assert.equal(h.comps().length, 1);
  assert.equal(h.footage().length, 1);
  assert.equal(h.comps()[0].numLayers, 1);
});

check('manual same-name comp collision is blocked before footage import', () => {
  const h = host(manifest(), beautyFiles); h.seedManualComp(); h.click('Build');
  assert.equal(h.imports.length, 0);
  assert.match(h.alerts.join(' '), /non-CutBridge comp.*already exists/);
});

check('moved managed comp fails closed without creating a replacement', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  const comp = h.comps()[0], beforeItems = h.projectItems.slice();
  comp.parentFolder = h.renderFolder();
  for (const reload of [false, true]) {
    if (reload) h.reloadScript();
    h.click('Build');
    assert.equal(h.comps().length, 1);
    assert.deepEqual(h.projectItems, beforeItems);
    assert.match(h.alerts.at(-1), /managed comp ownership.*expected comp folder/i);
  }
});

check('duplicate managed comp tags fail closed before build mutation', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  const original = h.comps()[0];
  const duplicate = new original.constructor(original.name, original.width, original.height, original.pixelAspect, original.duration, original.frameRate);
  duplicate.parentFolder = original.parentFolder; duplicate.comment = original.comment; h.projectItems.push(duplicate);
  const beforeItems = h.projectItems.slice();
  for (const reload of [false, true]) {
    if (reload) h.reloadScript();
    h.click('Build');
    assert.equal(h.comps().length, 2);
    assert.deepEqual(h.projectItems, beforeItems);
    assert.match(h.alerts.at(-1), /duplicate managed comp ownership/i);
  }
});

check('managed comp metadata drift blocks silent destructive correction', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  h.comps()[0].frameRate = 30; h.click('Build');
  assert.equal(h.comps().length, 1); assert.equal(h.footage().length, 1); assert.equal(h.comps()[0].numLayers, 1);
  assert.match(h.alerts.at(-1), /metadata no longer matches.*frame rate/);
});

check('QC rediscovers managed comp metadata after script reload', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  h.comps()[0].frameRate = 30; h.click('QC');
  assert.match(h.alerts.at(-1), /ERR.*Managed comp metadata mismatch.*frame rate/);
  h.reloadScript(); h.click('QC');
  assert.match(h.alerts.at(-1), /ERR.*Managed comp metadata mismatch.*frame rate/);
  assert.doesNotMatch(h.alerts.at(-1), /QC — PASS\b/);
});

check('wrong-type project item carrying managed footage tag fails closed', () => {
  const h = host(manifest(), beautyFiles); h.seedWrongTypeFootageTag(); h.click('Build');
  assert.equal(h.imports.length, 0);
  assert.match(h.alerts.at(-1), /managed footage no longer matches.*item type/);
});

check('managed footage source drift fails closed without replacement or duplicate layer', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  const original = h.footage()[0];
  h.driftFootageSource(original, '/packages/桜/render/beauty/C001_BEAUTY_9999.png');
  h.click('Build');
  assert.equal(h.imports.length, 1);
  assert.equal(h.footage().length, 1);
  assert.equal(h.comps()[0].numLayers, 1);
  assert.match(h.alerts.at(-1), /managed footage no longer matches.*source path/);
});

check('managed footage conform FPS drift fails closed', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  h.footage()[0].mainSource.conformFrameRate = 30;
  h.click('Build');
  assert.equal(h.imports.length, 1);
  assert.equal(h.comps()[0].numLayers, 1);
  assert.match(h.alerts.at(-1), /managed footage no longer matches.*frame rate/);
});

check('managed footage throwing FPS getter fails closed without replacement and QC does not pass footage', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  h.breakFootageFpsRead(h.footage()[0], 'throw');
  h.click('Build');
  assert.equal(h.imports.length, 1);
  assert.equal(h.footage().length, 1);
  assert.equal(h.comps()[0].numLayers, 1);
  assert.match(h.alerts.at(-1), /managed footage no longer matches.*frame rate/);
  h.click('QC');
  assert.match(h.alerts.at(-1), /managed footage validation failed/);
  assert.doesNotMatch(h.alerts.at(-1), /PASS BEAUTY: managed footage source\/FPS matches manifest/);
});

check('managed footage unavailable FPS fails closed without replacement and QC does not pass footage', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  h.breakFootageFpsRead(h.footage()[0], 'unavailable');
  h.click('Build');
  assert.equal(h.imports.length, 1);
  assert.equal(h.footage().length, 1);
  assert.equal(h.comps()[0].numLayers, 1);
  assert.match(h.alerts.at(-1), /managed footage no longer matches.*frame rate/);
  h.click('QC');
  assert.match(h.alerts.at(-1), /managed footage validation failed/);
  assert.doesNotMatch(h.alerts.at(-1), /PASS BEAUTY: managed footage source\/FPS matches manifest/);
});

check('initial conform FPS setter failure rolls back only the new import across retries', () => {
  const h = host(manifest(), beautyFiles, {conformSetterThrows: true});
  h.click('Build');
  assert.equal(h.imports.length, 1);
  assert.equal(h.footage().length, 0);
  assert.equal(h.comps().length, 1);
  assert.equal(h.comps()[0].numLayers, 0);
  const afterFirstFailure = h.projectItems.length;
  h.click('Build');
  assert.equal(h.imports.length, 2);
  assert.equal(h.footage().length, 0);
  assert.equal(h.projectItems.length, afterFirstFailure);
  assert.equal(h.comps()[0].numLayers, 0);
  assert.doesNotMatch(h.alerts.at(-1), /comp built/);
  assert.match(h.alerts.at(-1), /could not conform imported footage.*Build stopped/);
});

check('initial conform FPS readback mismatch rolls back only the new import across retries', () => {
  const h = host(manifest(), beautyFiles, {conformRefuses: true});
  h.click('Build');
  assert.equal(h.imports.length, 1);
  assert.equal(h.footage().length, 0);
  assert.equal(h.comps().length, 1);
  assert.equal(h.comps()[0].numLayers, 0);
  const afterFirstFailure = h.projectItems.length;
  h.click('Build');
  assert.equal(h.imports.length, 2);
  assert.equal(h.footage().length, 0);
  assert.equal(h.projectItems.length, afterFirstFailure);
  assert.equal(h.comps()[0].numLayers, 0);
  assert.doesNotMatch(h.alerts.at(-1), /comp built/);
  assert.match(h.alerts.at(-1), /timing\/source could not be verified.*frame rate/);
});

check('initial managed layer order is deterministic', () => {
  const m = manifest();
  m.passes.push({name: 'LINE', path: 'render/line', sequence_pattern: 'C001_LINE_####.png', required: true});
  m.ae.layer_order = ['BEAUTY', 'LINE'];
  const lineFiles = [1, 2, 3].map(n => `/packages/桜/render/line/C001_LINE_000${n}.png`);
  const h = host(m, [...beautyFiles, ...lineFiles]); h.click('Build');
  assert.deepEqual(h.comps()[0]._layers.map(x => x.name), ['BEAUTY', 'LINE']);
});

check('skipped optional pass is not reused or reordered as a verified layer', () => {
  const m = manifest();
  m.passes.push({name: 'LINE', path: 'render/line', sequence_pattern: 'C001_LINE_####.png', required: false});
  m.ae.layer_order = ['LINE', 'BEAUTY'];
  const lineFiles = [1, 2, 3].map(n => `/packages/桜/render/line/C001_LINE_000${n}.png`);
  const files = [...beautyFiles, ...lineFiles], h = host(m, files); h.click('Build');
  const comp = h.comps()[0], line = comp._layers.find(x => x.name === 'LINE');
  assert.deepEqual(comp._layers.map(x => x.name), ['LINE', 'BEAUTY']);
  line.source = null; files.splice(3);
  h.reloadScript(); h.click('Build');
  assert.match(h.alerts.at(-1), /optional pass skipped/);
  assert.deepEqual(comp._layers.map(x => x.name), ['BEAUTY', 'LINE']);
  assert.equal(line.source, null);
});


for (const kind of ['footage', 'layer']) {
  for (const drift of ['removed', 'changed', 'moved', 'unreadable', 'wrong-type', 'wrong-container']) {
    check(`${kind} ${drift} ownership blocks same-session and actual script reload without duplicates`, () => {
      const h = host(manifest(), beautyFiles); h.click('Build');
      assert.match(h.alerts.at(-1), /comp built/);
      const comp = h.comps()[0], footage = h.footage()[0], layer = comp.layer(1);
      const target = kind === 'footage' ? footage : layer;
      if (drift === 'removed') target.comment = '';
      if (drift === 'changed') target.comment = 'ARTIST: retained for manual work';
      if (drift === 'moved' && kind === 'footage') target.parentFolder = h.compFolder();
      if (drift === 'moved' && kind === 'layer') h.moveLayer(target, comp);
      if (drift === 'wrong-container') {
        if (kind === 'footage') target.parentFolder = null;
        else target.containingComp = {};
      }
      if (drift === 'unreadable') Object.defineProperty(target, 'comment', {get() { throw new Error('comment unavailable'); }});
      if (drift === 'wrong-type') Object.setPrototypeOf(target, {});
      const {item: artistFootage, layer: artistLayer} = h.seedArtistWork(comp);
      const beforeItems = h.projectItems.slice(), beforeLayers = comp._layers.slice();
      const comment = drift === 'unreadable' ? null : target.comment;
      for (const reload of [false, true, false]) {
        if (reload) h.reloadScript();
        h.click('Build');
        assert.doesNotMatch(h.alerts.at(-1), /comp built|reused safely/, `${kind} ${drift} must fail closed`);
        assert.match(h.alerts.at(-1), /ownership|ambiguous|managed.*folder|expected comp|item type/i);
        if (drift !== 'unreadable') assert.equal(target.comment, comment, 'must not reclaim/re-tag artist-edited object');
        assert.deepEqual(h.projectItems, beforeItems, 'no duplicate footage or project mutations');
        assert.deepEqual(comp._layers, beforeLayers, 'no duplicate layers or reordering on rejection');
        assert.equal(h.imports.length, 1);
        assert.equal(artistFootage.comment, 'Artist notes');
        assert.equal(artistLayer.source, artistFootage);
        if (kind === 'footage') {
          h.click('QC');
          assert.match(h.alerts.at(-1), /managed footage validation failed/);
          assert.doesNotMatch(h.alerts.at(-1), /PASS BEAUTY: managed footage source/);
        }
      }
    });
  }
}

check('valid live fallback survives replacing a cached reference and actual script reload', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  const comp = h.comps()[0], old = h.footage()[0], replacement = h.duplicateFootage(old);
  comp.layer(1).source = replacement; old.remove();
  const artist = h.seedArtistWork(comp), count = h.projectItems.length;
  for (const reload of [false, true]) {
    if (reload) h.reloadScript();
    h.click('Build');
    assert.match(h.alerts.at(-1), /reused safely/);
    assert.equal(h.projectItems.length, count);
    assert.equal(comp.numLayers, 2);
    assert.equal(comp._layers.find(x => x.name === 'BEAUTY').source, replacement);
    assert.equal(artist.layer.source, artist.item);
  }
});

check('live layer lookup discards a cached layer no longer in the comp', () => {
  const h = host(manifest(), beautyFiles); h.click('Build');
  const comp = h.comps()[0], old = comp.layer(1);
  comp._layers.splice(comp._layers.indexOf(old), 1);
  const replacement = comp.layers.add(old.source);
  replacement.name = old.name; replacement.comment = old.comment;
  const artist = h.seedArtistWork(comp);
  for (const reload of [false, true]) {
    if (reload) h.reloadScript();
    h.click('Build');
    assert.match(h.alerts.at(-1), /reused safely/);
    assert.equal(comp.numLayers, 2);
    assert.equal(comp._layers.find(x => x.name === 'BEAUTY'), replacement);
    assert.equal(artist.layer.source, artist.item);
    assert.equal(h.imports.length, 1);
  }
});

for (const kind of ['footage', 'layer']) {
  check(`duplicate live ${kind} tags fail closed in both cache states`, () => {
    const h = host(manifest(), beautyFiles); h.click('Build');
    const comp = h.comps()[0], original = comp.layer(1);
    if (kind === 'footage') h.duplicateFootage(h.footage()[0]);
    else { const duplicate = comp.layers.add(original.source); duplicate.name = original.name; duplicate.comment = original.comment; }
    const count = h.projectItems.length, layers = comp._layers.slice();
    for (const reload of [false, true]) {
      if (reload) h.reloadScript();
      h.click('Build');
      assert.match(h.alerts.at(-1), /duplicate managed.*ownership/i);
      assert.equal(h.projectItems.length, count);
      assert.deepEqual(comp._layers, layers);
    }
  });
}
console.log(`PASS: ${checks} S5 AE import/comp reliability groups (Node mocks; AE GUI not executed)`);
