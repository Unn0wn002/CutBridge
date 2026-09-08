/*
 * Host-shaped regression for existing CutBridge package-root structure.
 * Proves Build fails before mutation and QC cannot pass when deterministic
 * managed folders are missing or duplicated. This is not native After Effects certification.
 */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const rootDir = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(rootDir, "apps/after-effects/CutBridge.jsx"), "utf8");

const manifest = {
    schema: "cutbridge-manifest", schema_version: 1, cutbridge_version: "0.2.3",
    project: "作品", episode: "E01", scene: "S001", cut: "C001", take: "T01",
    package_name: "作品_E01_S001_C001_T01_V001", version: 1, fps: 24,
    frames: {start: 1, end: 3, count: 3},
    resolution: {width: 1920, height: 1080, pixel_aspect: 1},
    passes: [{name: "BEAUTY", path: "render/beauty", sequence_pattern: "C001_BEAUTY_####.png", required: true}],
    ae: {comp_name: "C001_COMP", layer_order: ["BEAUTY"]}
};

function makeHost() {
    const controls = [], alerts = [], projectItems = [], imports = [];
    const packagePath = "/packages/V001";
    const files = [1, 2, 3].map(n => packagePath + "/render/beauty/C001_BEAUTY_000" + n + ".png");
    const normalize = value => path.posix.normalize(String(value).replaceAll("\\", "/"));

    function Folder(value) {
        this.fsName = normalize(value);
        this.alias = false;
        this.exists = this.fsName === packagePath || files.some(f => f.startsWith(this.fsName + "/"));
    }
    Folder.prototype.getFiles = function(filter) {
        return files.filter(f => path.posix.dirname(f) === this.fsName).map(f => new File(f)).filter(filter);
    };

    function File(value) {
        this.fsName = normalize(value);
        this.name = path.posix.basename(this.fsName);
        this.alias = false;
        this.exists = files.includes(this.fsName) || this.name === "cutbridge.json";
        this.parent = new Folder(path.posix.dirname(this.fsName));
        this.encoding = "UTF-8";
        this._text = "";
    }
    File.decode = value => decodeURIComponent(value);
    const manifestFile = new File(packagePath + "/cutbridge.json");
    manifestFile._text = JSON.stringify(manifest);
    File.openDialog = () => manifestFile;
    File.prototype.open = function() { return true; };
    File.prototype.read = function() { return this._text; };
    File.prototype.close = function() {};

    function FolderItem(name) { this.name = name; this.parentFolder = null; this.comment = ""; }
    FolderItem.prototype.remove = function() {
        const index = projectItems.indexOf(this);
        if (index >= 0) projectItems.splice(index, 1);
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
        const index = projectItems.indexOf(this);
        if (index >= 0) projectItems.splice(index, 1);
    };

    function AVLayer(comp, footage) {
        this.containingComp = comp; this.source = footage; this.name = ""; this.comment = ""; this.startTime = 0;
    }
    AVLayer.prototype.moveToBeginning = function() {
        const list = this.containingComp._layers, index = list.indexOf(this);
        if (index >= 0) { list.splice(index, 1); list.unshift(this); }
    };
    AVLayer.prototype.remove = function() {
        const list = this.containingComp._layers, index = list.indexOf(this);
        if (index >= 0) list.splice(index, 1);
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
        const index = projectItems.indexOf(this);
        if (index >= 0) projectItems.splice(index, 1);
    };

    const project = {
        rootFolder: {name: "ROOT"},
        item: index => projectItems[index - 1],
        items: {
            addFolder(name) { const item = new FolderItem(name); projectItems.push(item); return item; },
            addComp(...args) { const item = new CompItem(...args); projectItems.push(item); return item; }
        },
        importFile(io) { const item = new FootageItem(io.file); projectItems.push(item); imports.push(item); return item; }
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
        ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}},
        alert: message => alerts.push(String(message)), $: {writeln() {}},
        app: {project, beginUndoGroup() {}, endUndoGroup() {}, newProject() {}}
    };
    vm.createContext(runtime);
    vm.runInContext(source, runtime);

    function click(fragment) {
        const button = controls.find(control => control.text.includes(fragment));
        assert.ok(button, "Missing button: " + fragment);
        button.onClick();
    }
    function topRoot() {
        return projectItems.find(item => item instanceof FolderItem && item.parentFolder === project.rootFolder && item.name === manifest.package_name);
    }
    function childFolders(parent) {
        return projectItems.filter(item => item instanceof FolderItem && item.parentFolder === parent);
    }
    function addChild(parent, name) {
        const item = new FolderItem(name); item.parentFolder = parent; projectItems.push(item); return item;
    }
    function snapshot() { return projectItems.slice(); }
    function assertSameItems(before, message) {
        assert.equal(projectItems.length, before.length, message + " (length)");
        before.forEach((item, index) => assert.strictEqual(projectItems[index], item, message + " (identity at " + index + ")"));
    }

    return {alerts, imports, projectItems, click, topRoot, childFolders, addChild, snapshot, assertSameItems};
}

const h = makeHost();
h.click("Build Comp");
const root = h.topRoot();
assert.ok(root, "initial Build should create the managed package root");
assert.deepEqual(h.childFolders(root).map(folder => folder.name).sort(), ["01_COMP", "02_RENDER", "03_PRECOMP", "04_OUTPUT"]);
assert.equal(h.imports.length, 1);

// Missing deterministic child folder is package drift, not permission to repair by mutation.
const missingPrecomp = h.childFolders(root).find(folder => folder.name === "03_PRECOMP");
assert.ok(missingPrecomp);
h.projectItems.splice(h.projectItems.indexOf(missingPrecomp), 1);
const afterRemoval = h.snapshot();
const importsBeforeMissingRetry = h.imports.length;
h.click("Build Comp");
h.assertSameItems(afterRemoval, "missing child folder retry must not mutate the project");
assert.equal(h.imports.length, importsBeforeMissingRetry, "missing child folder retry must not import footage");
assert.equal(h.childFolders(root).filter(folder => folder.name === "03_PRECOMP").length, 0, "Build must not recreate missing managed folder implicitly");
assert.match(h.alerts.at(-1), /03_PRECOMP.*must exist exactly once|must exist exactly once.*03_PRECOMP/i);
h.click("Run QC");
h.assertSameItems(afterRemoval, "QC on missing managed folder must remain read-only");
assert.doesNotMatch(h.alerts.at(-1), /QC — PASS\b/);
assert.match(h.alerts.at(-1), /03_PRECOMP.*must exist exactly once|must exist exactly once.*03_PRECOMP/i);

// Restore the deliberately removed folder, then prove duplicate deterministic children also fail before mutation.
h.projectItems.push(missingPrecomp);
const duplicateRender = h.addChild(root, "02_RENDER");
assert.ok(duplicateRender);
const afterDuplicate = h.snapshot();
const importsBeforeDuplicateRetry = h.imports.length;
h.click("Build Comp");
h.assertSameItems(afterDuplicate, "duplicate child folder retry must not mutate the project");
assert.equal(h.imports.length, importsBeforeDuplicateRetry, "duplicate child folder retry must not import footage");
assert.equal(h.childFolders(root).filter(folder => folder.name === "02_RENDER").length, 2);
assert.match(h.alerts.at(-1), /02_RENDER.*must exist exactly once|must exist exactly once.*02_RENDER/i);
h.click("Run QC");
h.assertSameItems(afterDuplicate, "QC on duplicate managed folder must remain read-only");
assert.doesNotMatch(h.alerts.at(-1), /QC — PASS\b/);
assert.match(h.alerts.at(-1), /02_RENDER.*must exist exactly once|must exist exactly once.*02_RENDER/i);

console.log("S6 package-root structure: PASS (Build/QC reject missing/duplicate managed folders; real AE MANUAL NOT EXECUTED)");
