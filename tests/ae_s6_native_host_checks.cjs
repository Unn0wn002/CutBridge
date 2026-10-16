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
const QCPlus = require(path.join(root, "apps/after-effects/qc_plus.js"));
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

function makeHost(options = {}) {
    const controls = [], alerts = [], confirms = [], projectItems = [], dialogQueue = [], replaceFlags = [];
    const invalidHandles = new WeakSet(), validityChecks = [], nativeEvents = [];
    let nextItemId = 1;
    const diskFiles = new Set([...frameFiles(1), ...frameFiles(2), ...frameFiles(3)]);
    const normalize = value => path.posix.normalize(String(value).replaceAll("\\", "/"));

    // A removed native AE object is an invalid handle, not an ordinary JS object.
    // Reject every property/prototype access after deletion; only the host's
    // isValid() operation and an ID captured before remove() remain usable.
    function nativeHandle(item) {
        if (!options.nativeHandles) return item;
        let handle;
        handle = new Proxy(item, {
            get(target, key, receiver) {
                if (invalidHandles.has(handle)) {
                    nativeEvents.push("invalid-access:" + String(key));
                    throw new ReferenceError("Object is invalid: removed native AE handle");
                }
                return Reflect.get(target, key, receiver);
            },
            getPrototypeOf(target) {
                if (invalidHandles.has(handle)) {
                    nativeEvents.push("invalid-prototype-access");
                    throw new ReferenceError("Object is invalid: removed native AE handle");
                }
                return Reflect.getPrototypeOf(target);
            }
        });
        return handle;
    }

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
        this.id = nextItemId++;
        this.file = file; this.name = ""; this.parentFolder = null; this.comment = "";
        let fps = 0;
        this.mainSource = {};
        Object.defineProperty(this.mainSource, "conformFrameRate", {
            enumerable: true, get: () => fps, set: value => {
                if (options.failConformVersion && file.fsName.startsWith(packagePath(options.failConformVersion) + "/")) {
                    throw new Error("Injected replacement conform failure");
                }
                fps = value;
            }
        });
    }
    FootageItem.prototype.remove = function() {
        nativeEvents.push("remove:" + this.id);
        if (options.refuseRemoval) return;
        const i = projectItems.indexOf(this); if (i >= 0) projectItems.splice(i, 1);
        if (options.nativeHandles) invalidHandles.add(this);
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
        if (options.nativeHandles) invalidHandles.add(this);
    };

    function CompItem(name, width, height, pixelAspect, duration, frameRate) {
        this.name = name; this.width = width; this.height = height; this.pixelAspect = pixelAspect;
        this.duration = duration; this.frameRate = frameRate; this.parentFolder = null; this.comment = ""; this._layers = [];
        this.layers = {add: item => { const layer = nativeHandle(new AVLayer(this, item)); this._layers.unshift(layer); return layer; }};
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
        importFile(io) { const item = nativeHandle(new FootageItem(io.file)); projectItems.push(item); return item; }
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
        ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}}, CutBridgeRevisionManager: Revision, CutBridgeQCPlus: QCPlus,
        alert: message => alerts.push(String(message)),
        confirm: message => { confirms.push(String(message)); return true; },
        $: {writeln() {}},
        app: {project, beginUndoGroup() {}, endUndoGroup() {}, newProject() {}}
    };
    if (options.nativeHandles) runtime.isValid = target => {
        const valid = !invalidHandles.has(target);
        validityChecks.push({target, valid});
        return valid;
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
    function addManualRoot(name, comment) {
        const item = new FolderItem(name); item.parentFolder = project.rootFolder; item.comment = comment || ""; projectItems.push(item); return item;
    }
    function childFolders(parent) { return projectItems.filter(x => x instanceof FolderItem && x.parentFolder === parent); }

    return {alerts, confirms, replaceFlags, queue, click, reload, topRoot, comps, footage, addManualRoot, childFolders,
        projectItems, runtime, validityChecks, nativeEvents, invalidHandles};
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
assert.ok(packageRoot, "root should migrate to V002 name; alerts=" + JSON.stringify(h.alerts) + "; confirms=" + JSON.stringify(h.confirms));
assert.equal(packageRoot.comment, "Artist / studio package note", "revision must preserve an unmanaged root comment");
assert.equal(layer.comment, Contract.managedTag("layer", v2, "BEAUTY"));
assert.equal(comp.comment, Contract.managedTag("comp", v2, v2.ae.comp_name));
assert.equal(sourceV1.comment, Contract.managedTag("footage", v1, "BEAUTY"));
const sourceV2 = layer.source;
assert.notEqual(sourceV2, sourceV1);
assert.equal(sourceV2.comment, Contract.managedTag("footage", v2, "BEAUTY"));
h.click("Build Comp"); h.click("Run QC");
assert.match(h.alerts.at(-1), /CutBridge QC — PASS/);

// Revision must not choose an arbitrary current root or deterministic child folder.
const duplicateCurrentRoot = h.addManualRoot(v2.package_name, "duplicate current root");
let sourceBeforeBlockedRevision = layer.source;
let footageBeforeBlockedRevision = h.footage().length;
let replaceCallsBeforeBlockedRevision = h.replaceFlags.length;
let confirmsBeforeBlockedRevision = h.confirms.length;
h.queue(v3); h.click("Update Revision");
assert.strictEqual(layer.source, sourceBeforeBlockedRevision, "duplicate current root must not swap a source");
assert.equal(h.footage().length, footageBeforeBlockedRevision, "duplicate current root must not import replacement footage");
assert.equal(h.replaceFlags.length, replaceCallsBeforeBlockedRevision, "duplicate current root must not call replaceSource");
assert.equal(h.confirms.length, confirmsBeforeBlockedRevision, "duplicate current root must block before confirmation");
assert.equal(h.topRoot(v2.package_name), packageRoot, "current managed root must not migrate on ambiguous revision");
assert.match(h.alerts.at(-1), /package root.*must exist exactly once|duplicate roots/i);
h.projectItems.splice(h.projectItems.indexOf(duplicateCurrentRoot), 1);

const renderFolderV2 = h.childFolders(packageRoot).find(folder => folder.name === "02_RENDER");
assert.ok(renderFolderV2, "V002 render folder should exist");
const duplicateRenderFolder = new renderFolderV2.constructor("02_RENDER");
duplicateRenderFolder.parentFolder = packageRoot;
h.projectItems.push(duplicateRenderFolder);
sourceBeforeBlockedRevision = layer.source;
footageBeforeBlockedRevision = h.footage().length;
replaceCallsBeforeBlockedRevision = h.replaceFlags.length;
confirmsBeforeBlockedRevision = h.confirms.length;
h.queue(v3); h.click("Update Revision");
assert.strictEqual(layer.source, sourceBeforeBlockedRevision, "duplicate render folder must not swap a source");
assert.equal(h.footage().length, footageBeforeBlockedRevision, "duplicate render folder must not import replacement footage");
assert.equal(h.replaceFlags.length, replaceCallsBeforeBlockedRevision, "duplicate render folder must not call replaceSource");
assert.equal(h.confirms.length, confirmsBeforeBlockedRevision, "duplicate render folder must block before confirmation");
assert.equal(h.topRoot(v2.package_name), packageRoot, "current managed root must stay V002 on folder ambiguity");
assert.match(h.alerts.at(-1), /managed folder '02_RENDER'.*must exist exactly once|02_RENDER.*duplicate folder/i);
h.projectItems.splice(h.projectItems.indexOf(duplicateRenderFolder), 1);

h.queue(v3); h.click("Update Revision");
packageRoot = h.topRoot(v3.package_name);
assert.ok(packageRoot, "root should migrate to V003 name; alerts=" + JSON.stringify(h.alerts) + "; confirms=" + JSON.stringify(h.confirms));
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

// Exercise the actual adapter cleanup, not only the portable revision executor.
// Conform fails after importReplacement() has registered the newly allocated ID.
// Removing it invalidates the handle immediately, so cleanup must prove absence
// by the captured numeric ID without touching that handle again.
const failedImportOptions = {nativeHandles: true, failConformVersion: 2};
const failedImportHost = makeHost(failedImportOptions);
failedImportHost.queue(v1); failedImportHost.click("Import Package"); failedImportHost.click("Build Comp");
const preservedComp = failedImportHost.comps()[0], preservedLayer = preservedComp.layer(1);
const preservedSource = preservedLayer.source, preservedRoot = failedImportHost.topRoot(v1.package_name);
preservedLayer.artistEffects = {glow: 42, mask: [1, 2, 3]};
preservedRoot.comment = "Artist package note: keep after failed revision";
const preservedItems = failedImportHost.projectItems.slice();
const oldSourceId = preservedSource.id;
assert.equal(typeof oldSourceId, "number", "native mock footage IDs must exercise numeric-ID cleanup");
failedImportHost.queue(v2); failedImportHost.click("Update Revision");
assert.match(failedImportHost.alerts.at(-1), /Injected replacement conform failure.*rollback completed/i);
assert.doesNotMatch(failedImportHost.alerts.at(-1), /ROLLBACK INCOMPLETE|Object is invalid/i);
assert.deepEqual(failedImportHost.projectItems, preservedItems, "failed replacement import must remove only its new project item");
assert.strictEqual(preservedLayer.source, preservedSource, "failed import must leave the old source live");
assert.equal(preservedSource.id, oldSourceId);
assert.equal(preservedRoot.name, v1.package_name);
assert.equal(preservedRoot.comment, "Artist package note: keep after failed revision");
assert.equal(preservedComp.comment, Contract.managedTag("comp", v1, v1.ae.comp_name));
assert.equal(preservedLayer.comment, Contract.managedTag("layer", v1, "BEAUTY"));
assert.deepEqual(preservedLayer.artistEffects, {glow: 42, mask: [1, 2, 3]});
assert.deepEqual(failedImportHost.replaceFlags, [], "failed import must block every source swap");
assert.deepEqual(failedImportHost.nativeEvents, ["remove:" + (oldSourceId + 1)], "cleanup must not dereference an invalidated removed handle");
assert.ok(failedImportHost.validityChecks.every(check => check.valid), "numeric-ID cleanup must not send the removed handle back to liveProjectItem/isValid");
failedImportOptions.failConformVersion = null;
failedImportHost.queue(v2); failedImportHost.click("Update Revision");
assert.ok(failedImportHost.topRoot(v2.package_name), "a corrected import must remain retryable after complete rollback");
assert.deepEqual(failedImportHost.replaceFlags, [false]);
assert.deepEqual(preservedLayer.artistEffects, {glow: 42, mask: [1, 2, 3]});

// Absence of an exception from remove() is insufficient: a native host that
// retains the captured ID must produce an explicit incomplete rollback.
const refusedImportHost = makeHost({nativeHandles: true, failConformVersion: 2, refuseRemoval: true});
refusedImportHost.queue(v1); refusedImportHost.click("Import Package"); refusedImportHost.click("Build Comp");
const refusedLayer = refusedImportHost.comps()[0].layer(1), refusedSource = refusedLayer.source;
refusedImportHost.queue(v2); refusedImportHost.click("Update Revision");
assert.match(refusedImportHost.alerts.at(-1), /ROLLBACK INCOMPLETE.*Removal not verified/i);
assert.strictEqual(refusedLayer.source, refusedSource);
assert.equal(refusedImportHost.footage().length, 2, "retained replacement must be reported rather than declared removed");
assert.deepEqual(refusedImportHost.replaceFlags, []);
assert.ok(refusedImportHost.topRoot(v1.package_name));

// Stale in-memory references must be rejected by native isValid() before the
// adapter compares/dereferences them. Live, correctly tagged replacements are
// discovered from project state; neither extra imports nor layers are allowed.
for (const kind of ["footage", "layer"]) {
    const invalidHost = makeHost({nativeHandles: true});
    invalidHost.queue(v1); invalidHost.click("Import Package"); invalidHost.click("Build Comp");
    const activeComp = invalidHost.comps()[0], oldLayer = activeComp.layer(1), oldFootage = oldLayer.source;
    const oldHandle = kind === "footage" ? oldFootage : oldLayer;
    let replacement;
    if (kind === "footage") {
        replacement = new oldFootage.constructor(oldFootage.file);
        replacement.name = oldFootage.name;
        replacement.parentFolder = oldFootage.parentFolder;
        replacement.comment = oldFootage.comment;
        replacement.mainSource.conformFrameRate = oldFootage.mainSource.conformFrameRate;
        invalidHost.projectItems.push(replacement);
        oldLayer.replaceSource(replacement, false);
    } else {
        replacement = activeComp.layers.add(oldFootage);
        replacement.name = oldLayer.name;
        replacement.comment = oldLayer.comment;
    }
    oldHandle.remove();
    assert.equal(invalidHost.invalidHandles.has(oldHandle), true);
    const itemCount = invalidHost.projectItems.length, layerCount = activeComp.numLayers;
    invalidHost.validityChecks.length = 0;
    invalidHost.click("Build Comp");
    assert.match(invalidHost.alerts.at(-1), /reused safely/i, "invalid cached " + kind + " must not prevent safe live discovery");
    assert.ok(invalidHost.validityChecks.some(check => check.target === oldHandle && check.valid === false), "native invalidity guard must inspect the cached " + kind + " handle");
    assert.equal(invalidHost.projectItems.length, itemCount);
    assert.equal(activeComp.numLayers, layerCount);
    assert.ok(!invalidHost.nativeEvents.some(event => event.startsWith("invalid-")), "Build must not read an invalid cached " + kind + " handle");
    const activeLayer = kind === "layer" ? replacement : oldLayer;
    assert.strictEqual(activeLayer.source, kind === "footage" ? replacement : oldFootage);
    invalidHost.reload(); invalidHost.queue(v1); invalidHost.click("Import Package"); invalidHost.click("Build Comp");
    assert.match(invalidHost.alerts.at(-1), /reused safely/i);
    assert.equal(invalidHost.projectItems.length, itemCount);
    assert.equal(activeComp.numLayers, layerCount);
}

// A prior-version managed layer tag inside the active comp is drift, not historical state.
// Reload clears in-memory layer caches so this proves persistent discovery fails closed.
const staleLayerHost = makeHost();
const staleV1 = manifest(1), staleV2 = manifest(2);
staleLayerHost.queue(staleV1); staleLayerHost.click("Import Package"); staleLayerHost.click("Build Comp");
const staleComp = staleLayerHost.comps()[0], staleLayer = staleComp.layer(1), staleSourceV1 = staleLayer.source;
staleLayerHost.queue(staleV2); staleLayerHost.click("Update Revision");
assert.equal(staleLayer.comment, Contract.managedTag("layer", staleV2, "BEAUTY"));
assert.equal(staleSourceV1.comment, Contract.managedTag("footage", staleV1, "BEAUTY"), "historical V001 footage provenance must remain allowed");
const staleActiveSource = staleLayer.source;
const staleLayerCount = staleComp.numLayers;
const staleFootageCount = staleLayerHost.footage().length;
staleLayer.comment = Contract.managedTag("layer", staleV1, "BEAUTY");
staleLayerHost.reload(); staleLayerHost.queue(staleV2); staleLayerHost.click("Import Package"); staleLayerHost.click("Build Comp");
assert.equal(staleComp.numLayers, staleLayerCount, "stale prior-version managed layer must not cause a duplicate layer after reload");
assert.equal(staleLayerHost.footage().length, staleFootageCount, "blocked Build must not import extra footage");
assert.strictEqual(staleLayer.source, staleActiveSource, "blocked Build must not change the active layer source");
assert.equal(staleSourceV1.comment, Contract.managedTag("footage", staleV1, "BEAUTY"), "historical footage must remain version-scoped rather than becoming a collision");
assert.match(staleLayerHost.alerts.at(-1), /managed layer ownership|unverified layer|ambiguous managed layer/i);

// An extra prior-version managed layer in the active comp is still CutBridge-owned drift
// even if its name/source no longer collide with the current pass. Build and QC must fail closed.
const orphanLayerHost = makeHost();
const orphanV1 = manifest(1), orphanV2 = manifest(2);
orphanLayerHost.queue(orphanV1); orphanLayerHost.click("Import Package"); orphanLayerHost.click("Build Comp");
const orphanComp = orphanLayerHost.comps()[0], orphanCurrentLayer = orphanComp.layer(1), orphanSourceV1 = orphanCurrentLayer.source;
orphanLayerHost.queue(orphanV2); orphanLayerHost.click("Update Revision");
const orphanSourceV2 = orphanCurrentLayer.source;
assert.notEqual(orphanSourceV2, orphanSourceV1);
const orphanLayer = orphanComp.layers.add(orphanSourceV1);
orphanLayer.name = "ARCHIVE";
orphanLayer.comment = Contract.managedTag("layer", orphanV1, "BEAUTY");
const orphanLayerCount = orphanComp.numLayers;
const orphanFootageCount = orphanLayerHost.footage().length;
const orphanReplaceCount = orphanLayerHost.replaceFlags.length;
orphanLayerHost.reload(); orphanLayerHost.queue(orphanV2); orphanLayerHost.click("Import Package"); orphanLayerHost.click("Build Comp");
assert.equal(orphanComp.numLayers, orphanLayerCount, "orphan prior-version managed layer must not be removed or duplicated silently");
assert.equal(orphanLayerHost.footage().length, orphanFootageCount, "blocked orphan-layer Build must not import footage");
assert.equal(orphanLayerHost.replaceFlags.length, orphanReplaceCount, "blocked orphan-layer Build must not swap managed sources");
assert.strictEqual(orphanCurrentLayer.source, orphanSourceV2, "blocked orphan-layer Build must preserve the active current source");
assert.match(orphanLayerHost.alerts.at(-1), /stale|orphan|managed layer ownership|unverified layer|ambiguous managed layer/i);
orphanLayerHost.click("Run QC");
assert.doesNotMatch(orphanLayerHost.alerts.at(-1), /CutBridge QC — PASS\b/);
assert.match(orphanLayerHost.alerts.at(-1), /stale|orphan|managed layer ownership|managed layer/i);

// A user-owned top-level folder with the deterministic package name is a collision,
// not ownership proof. Build must not create children or managed objects inside it.
const collisionHost = makeHost();
const manualRoot = collisionHost.addManualRoot(v1.package_name, "Studio-owned folder");
collisionHost.queue(v1); collisionHost.click("Import Package"); collisionHost.click("Build Comp");
assert.equal(collisionHost.comps().length, 0, "unverified package root must not receive a managed comp");
assert.equal(collisionHost.footage().length, 0, "unverified package root must not receive managed footage");
assert.equal(collisionHost.childFolders(manualRoot).length, 0, "unverified package root must not be mutated with CutBridge child folders");
assert.equal(manualRoot.comment, "Studio-owned folder");
assert.match(collisionHost.alerts.at(-1), /project-root folder|package root|package folder|ownership|collision|not verified/i);

console.log("S6 native-host lifecycle: PASS (V001→V002→V003 + failed-import numeric-ID cleanup + invalid native caches + Build/QC/reload + ownership collisions; real AE MANUAL NOT EXECUTED)");
