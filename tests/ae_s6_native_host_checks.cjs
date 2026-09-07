/*
 * Native-host-shaped S6 regression harness.
 * This executes the actual CutBridge.jsx adapter in a Node vm with AVLayer.source
 * deliberately read-only and replaceSource() as the only mutation API.
 * It is regression evidence only; it does not certify a real After Effects host.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const root = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(root, "apps/after-effects/CutBridge.jsx"), "utf8");
const Revision = require(path.join(root, "apps/after-effects/revision_manager.js"));
const Contract = require(path.join(root, "apps/after-effects/CutBridge.jsx"));

function manifest(version) {
    return {
        schema: "cutbridge-manifest", schema_version: 1, cutbridge_version: "0.2.3",
        project: "作品", episode: "E01", scene: "S001", cut: "C001", take: "T01",
        package_name: "作品_E01_S001_C001_T01_V" + String(version).padStart(3, "0"),
        version, fps: 24, frames: {start: 1, end: 3, count: 3},
        resolution: {width: 1920, height: 1080, pixel_aspect: 1},
        passes: [{name: "BEAUTY", path: "render/beauty", sequence_pattern: "C001_BEAUTY_####.png", required: true}],
        ae: {comp_name: "C001_COMP", layer_order: ["BEAUTY"]}
    };
}

function packagePath(version) { return "/packages/V" + String(version).padStart(3, "0"); }
function frameFiles(version) {
    return [1, 2, 3].map(n => packagePath(version) + "/render/beauty/C001_BEAUTY_000" + n + ".png");
}

function makeHost() {
    const controls = [], alerts = [], confirms = [], projectItems = [], dialogQueue = [], replaceFlags = [];
    const diskFiles = new Set([...frameFiles(1), ...frameFiles(2), ...frameFiles(3)]);
    const normalize = value => path.posix.normalize(String(value).replaceAll("\\", "/"));

    function Folder(value) {
        this.fsName = normalize(value); this.alias = false;
        this.exists = [...diskFiles].some(f => f.startsWith(this.fsName + "/")) || /^\/packages\/V\d{3}$/.test(this.fsName);
    }
    Folder.prototype.getFiles = function(filter) {
        return [...diskFiles]
            .filter(f => path.posix.dirname(f) === this.fsName)
            .map(f => new File(f))
            .filter(filter);
    };

    function File(value) {
        this.fsName = normalize(value); this.name = path.posix.basename(this.fsName); this.alias = false;
        this.exists = diskFiles.has(this.fsName) || this.name === "cutbridge.json";
        this.parent = new Folder(path.posix.dirname(this.fsName)); this.encoding = "UTF-8"; this._text = "";
    }
    File.decode = value => decodeURIComponent(value);
    File.openDialog = () => dialogQueue.length ? dialogQueue.shift() : null;
    File.prototype.open = function() { return true; };
    File.prototype.read = function() { return this._text; };
    File.prototype.close = function() {};

    function manifestFile(m) {
        const f = new File(packagePath(m.version) + "/cutbridge.json");
        f._text = JSON.stringify(m); return f;
    }

    function FolderItem(name) { this.name = name; this.parentFolder = null; this.comment = ""; }
    FolderItem.prototype.remove = function() {
        const i = projectItems.indexOf(this); if (i >= 0) projectItems.splice(i, 1);
    };

    function FootageItem(file) {
        this.file = file; this.name = ""; this.parentFolder = null; this.comment = "";
        let fps = 0;
        this.mainSource = {};
        Object.defineProperty(this.mainSource, "conformFrameRate", {
            enumerable: true, get: () => fps, set: value => { fps = value; }
        });
    }
    FootageItem.prototype.remove = function() {
        const i = projectItems.indexOf(this); if (i >= 0) projectItems.splice(i, 1);
    };

    function AVLayer(comp, sourceItem) {
        this.containingComp = comp; this.name = ""; this.comment = ""; this.startTime = 0;
        this._source = sourceItem;
        Object.defineProperty(this, "source", {
            enumerable: true,
            get: () => this._source,
            set: () => { throw new Error("AVLayer.source is read-only in this host"); }
        });
    }
    AVLayer.prototype.replaceSource = function(item, fixExpressions) {
        replaceFlags.push(fixExpressions); this._source = item;
    };
    AVLayer.prototype.moveToBeginning = function() {
        const list = this.containingComp._layers, i = list.indexOf(this);
        if (i >= 0) { list.splice(i, 1); list.unshift(this); }
    };
    AVLayer.prototype.remove = function() {
        const list = this.containingComp._layers, i = list.indexOf(this);
        if (i >= 0) list.splice(i, 1);
    };

    function CompItem(name, width, height, pixelAspect, duration, frameRate) {
        this.name = name; this.width = width; this.height = height; this.pixelAspect = pixelAspect;
        this.duration = duration; this.frameRate = frameRate; this.parentFolder = null; this.comment = ""; this._layers = [];
        this.layers = {add: item => { const layer = new AVLayer(this, item); this._layers.unshift(layer); return layer; }};
    }
    Object.defineProperty(CompItem.prototype, "numLayers", {get() { return this._layers.length; }});
    CompItem.prototype.layer = function(index) { return this._layers[index - 1]; };
    CompItem.prototype.openInViewer = function() {};
    CompItem.prototype.remove = function() {
        const i = projectItems.indexOf(this); if (i >= 0) projectItems.splice(i, 1);
    };

    const project = {
        rootFolder: {name: "ROOT"},
        item: index => projectItems[index - 1],
        items: {
            addFolder(name) { const item = new FolderItem(name); projectItems.push(item); return item; },
            addComp(...args) { const item = new CompItem(...args); projectItems.push(item); return item; }
        },
        importFile(io) { const item = new FootageItem(io.file); projectItems.push(item); return item; }
    };
    Object.defineProperty(project, "numItems", {get() { return projectItems.length; }});

    function ImportOptions(file) { this.file = file; this.sequence = false; this.forceAlphabetical = true; this.importAs = null; }
    ImportOptions.prototype.canImportAs = () => true;

    function Window() { this.layout = {resize() {}, layout() {}}; }
    Window.prototype.add = function(type, unused, text) {
        const control = {type, text, graphics: {font: {name: "Arial"}}, preferredSize: {}};
        if (type === "button") controls.push(control);
        return control;
    };
    Window.prototype.center = Window.prototype.show = function() {};
    function Panel() {}

    const runtime = {
        File, Folder, Window, Panel, FolderItem, FootageItem, CompItem, AVLayer, ImportOptions,
        ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}}, CutBridgeRevisionManager: Revision,
        alert: message => alerts.push(String(message)),
        confirm: message => { confirms.push(String(message)); return true; },
        $: {writeln() {}},
        app: {project, beginUndoGroup() {}, endUndoGroup() {}, newProject() {}}
    };
    vm.createContext(runtime);
    vm.runInContext(source, runtime);

    function reload() { controls.length = 0; vm.runInContext(source, runtime); }
    function queue(m) { dialogQueue.push(manifestFile(m)); }
    function click(fragment) {
        const button = controls.find(c => c.text.includes(fragment));
        assert.ok(button, "Missing button: " + fragment); button.onClick();
    }
    function topRoot(name) {
        return projectItems.find(x => x instanceof FolderItem && x.parentFolder === project.rootFolder && x.name === name);
    }
    function comps() { return projectItems.filter(x => x instanceof CompItem); }
    function footage() { return projectItems.filter(x => x instanceof FootageItem); }

    return {alerts, confirms, replaceFlags, queue, click, reload, topRoot, comps, footage, projectItems};
}

const h = makeHost();
const v1 = manifest(1), v2 = manifest(2), v3 = manifest(3);

h.queue(v1); h.click("Import Package"); h.click("Build Comp");
assert.equal(h.comps().length, 1);
assert.equal(h.footage().length, 1);
const comp = h.comps()[0], layer = comp.layer(1), sourceV1 = layer.source;
let packageRoot = h.topRoot(v1.package_name);
assert.ok(packageRoot, "V001 package root should exist");
packageRoot.comment = "Artist / studio package note";
assert.equal(sourceV1.comment, Contract.managedTag("footage", v1, "BEAUTY"));

h.queue(v2); h.click("Update Revision");
packageRoot = h.topRoot(v2.package_name);
assert.ok(packageRoot, "root should migrate to V002 name");
assert.equal(packageRoot.comment, "Artist / studio package note", "revision must preserve an unmanaged root comment");
assert.equal(layer.comment, Contract.managedTag("layer", v2, "BEAUTY"));
assert.equal(comp.comment, Contract.managedTag("comp", v2, v2.ae.comp_name));
assert.equal(sourceV1.comment, Contract.managedTag("footage", v1, "BEAUTY"));
const sourceV2 = layer.source;
assert.notEqual(sourceV2, sourceV1);
assert.equal(sourceV2.comment, Contract.managedTag("footage", v2, "BEAUTY"));
h.click("Build Comp"); h.click("Run QC");
assert.match(h.alerts.at(-1), /CutBridge QC — PASS/);

h.queue(v3); h.click("Update Revision");
packageRoot = h.topRoot(v3.package_name);
assert.ok(packageRoot, "root should migrate to V003 name");
assert.equal(packageRoot.comment, "Artist / studio package note");
assert.equal(sourceV2.comment, Contract.managedTag("footage", v2, "BEAUTY"));
const sourceV3 = layer.source;
assert.notEqual(sourceV3, sourceV2);
assert.equal(sourceV3.comment, Contract.managedTag("footage", v3, "BEAUTY"));
assert.equal(layer.comment, Contract.managedTag("layer", v3, "BEAUTY"));
assert.equal(comp.comment, Contract.managedTag("comp", v3, v3.ae.comp_name));
assert.equal(h.footage().length, 3, "V001/V002 provenance footage plus active V003 should coexist");
h.click("Build Comp"); h.click("Run QC");
assert.match(h.alerts.at(-1), /CutBridge QC — PASS/);
assert.deepEqual(h.replaceFlags, [false, false], "revision swaps must use replaceSource(..., false)");

// Re-open the V003 package after script reload and prove project-state discovery remains safe.
h.reload(); h.queue(v3); h.click("Import Package"); h.click("Build Comp"); h.click("Run QC");
assert.match(h.alerts.at(-1), /CutBridge QC — PASS/);
assert.equal(h.comps().length, 1);
assert.equal(h.footage().length, 3);
assert.equal(h.topRoot(v3.package_name).comment, "Artist / studio package note");
assert.ok(!h.alerts.some(x => /Revision failed|revision was not applied/.test(x)));

console.log("S6 native-host lifecycle: PASS (V001→V002→V003 + Build/QC + reload; real AE MANUAL NOT EXECUTED)");
