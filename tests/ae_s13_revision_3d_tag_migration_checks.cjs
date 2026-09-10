/* S13 regression: S10C camera/null ownership and baked samples must migrate across source-only revisions. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const root = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(root, "apps/after-effects/CutBridge.jsx"), "utf8");
const revisionSource = fs.readFileSync(path.join(root, "apps/after-effects/revision_manager.js"), "utf8");
const Revision = require(path.join(root, "apps/after-effects/revision_manager.js"));
const QCPlus = require(path.join(root, "apps/after-effects/qc_plus.js"));
const Contract = require(path.join(root, "apps/after-effects/CutBridge.jsx"));

function manifest(version) {
    const versionToken = String(version).padStart(3, "0");
    const sampleOffset = version * 10;
    return {
        schema: "cutbridge-manifest", schema_version: 1, cutbridge_version: "0.2.3",
        project: "S13TEST", episode: "EP01", scene: "SC001", cut: "C001", take: "T01",
        package_name: `S13TEST_EP01_SC001_C001_T01_V${versionToken}`,
        version, fps: 24, frames: {start: 1, end: 3, count: 3},
        resolution: {width: 1920, height: 1080, pixel_aspect: 1},
        passes: [{name: "BEAUTY", path: "render/beauty", sequence_pattern: "C001_BEAUTY_####.png", required: true}],
        ae: {comp_name: "C001_COMP", layer_order: ["BEAUTY"]},
        handoff_3d: {
            schema: "cutbridge-handoff-3d", schema_version: 1,
            space: {coordinate_system: "after-effects-composition", axis_map: "blender_xyz_to_ae_x_negz_y", origin: "composition-center", position_units: "pixels", pixels_per_blender_unit: 100},
            sampling: {mode: "baked-per-frame", frame_start: 1, frame_end: 3, frame_step: 1},
            camera: {
                name: "S13_Camera", type: "PERSP",
                samples: [1, 2, 3].map((frame, index) => ({
                    frame, time: index / 24,
                    position: [960 + sampleOffset + index, 540, -1000],
                    forward: [0, 0, 1], up: [0, -1, 0], horizontal_fov_radians: 0.691111, ae_zoom: 2666.666 + version
                }))
            },
            nulls: [{
                name: "S13_Null", source_type: "EMPTY",
                samples: [1, 2, 3].map((frame, index) => ({
                    frame, time: index / 24, position: [960 + sampleOffset, 540 + index, 0], scale: [1 + version / 10, 1, 1]
                }))
            }]
        }
    };
}

function packagePath(version) { return `/packages/V${String(version).padStart(3, "0")}`; }
function frameFiles(version) {
    return [1, 2, 3].map(n => `${packagePath(version)}/render/beauty/C001_BEAUTY_000${n}.png`);
}

function makeHost() {
    const controls = [], alerts = [], confirms = [], projectItems = [], dialogQueue = [];
    const diskFiles = new Set([...frameFiles(1), ...frameFiles(2), ...frameFiles(3)]);
    const normalize = value => path.posix.normalize(String(value).replaceAll("\\", "/"));

    function Folder(value) {
        this.fsName = normalize(value); this.alias = false;
        this.exists = [...diskFiles].some(f => f.startsWith(this.fsName + "/")) || /^\/packages\/V\d{3}$/.test(this.fsName);
    }
    Folder.prototype.getFiles = function(filter) {
        return [...diskFiles].filter(f => path.posix.dirname(f) === this.fsName).map(f => new File(f)).filter(filter);
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
        const f = new File(`${packagePath(m.version)}/cutbridge.json`);
        f._text = JSON.stringify(m);
        return f;
    }

    function FolderItem(name) { this.name = name; this.parentFolder = null; this.comment = ""; }
    FolderItem.prototype.remove = function() { const i = projectItems.indexOf(this); if (i >= 0) projectItems.splice(i, 1); };

    function FootageItem(file) {
        this.file = file; this.name = ""; this.parentFolder = null; this.comment = "";
        let fps = 0; this.mainSource = {};
        Object.defineProperty(this.mainSource, "conformFrameRate", {enumerable: true, get: () => fps, set: value => { fps = value; }});
    }
    FootageItem.prototype.remove = function() { const i = projectItems.indexOf(this); if (i >= 0) projectItems.splice(i, 1); };

    function Property(name, matchName) {
        this.name = name; this.matchName = matchName || name; this.value = null; this.keys = [];
        this.rejectKeyRemoval = false;
    }
    Object.defineProperty(Property.prototype, "numKeys", {get() { return this.keys.length; }});
    Property.prototype.setValue = function(value) { this.value = value; };
    Property.prototype.setValueAtTime = function(time, value) {
        const existing = this.keys.find(key => Math.abs(key.time - time) < 1e-9);
        if (existing) existing.value = value;
        else this.keys.push({time, value});
        this.keys.sort((left, right) => left.time - right.time);
        this.value = value;
    };
    Property.prototype.keyTime = function(index) { return this.keys[index - 1].time; };
    Property.prototype.removeKey = function(index) {
        if (this.rejectKeyRemoval) {
            throw new Error("After Effects error: internal verification failure, sorry! {no current context}");
        }
        this.keys.splice(index - 1, 1);
    };

    function PropertyGroup() { this._props = {}; }
    PropertyGroup.prototype.property = function(name) {
        if (!this._props[name]) this._props[name] = new Property(name);
        return this._props[name];
    };

    function AVLayer(comp, sourceItem) {
        this.containingComp = comp; this.name = ""; this.comment = ""; this.startTime = 0;
        this.threeDLayer = false; this.nullLayer = false; this._source = sourceItem;
        this._transform = new PropertyGroup();
        this.position = this._transform.property("ADBE Position");
        this.scale = this._transform.property("ADBE Scale");
        Object.defineProperty(this, "source", {enumerable: true, get: () => this._source, set: () => { throw new Error("AVLayer.source is read-only"); }});
    }
    AVLayer.prototype.replaceSource = function(item) { this._source = item; };
    AVLayer.prototype.property = function(groupName) { return groupName === "ADBE Transform Group" ? this._transform : null; };
    AVLayer.prototype.moveToBeginning = function() {
        const list = this.containingComp._layers, i = list.indexOf(this);
        if (i >= 0) { list.splice(i, 1); list.unshift(this); }
    };
    AVLayer.prototype.remove = function() { const list = this.containingComp._layers, i = list.indexOf(this); if (i >= 0) list.splice(i, 1); };

    function CameraLayer(comp, name) {
        AVLayer.call(this, comp, null); this.name = name; this._cameraOptions = new PropertyGroup();
        this._pointOfInterest = new Property("Point of Interest", "ADBE Anchor Point");
        this._rejectUnsafePOIAccess = false;
        const genericProperty = this._transform.property.bind(this._transform);
        const camera = this;
        this._transform.property = function(propName) {
            if (propName === 1) return camera._pointOfInterest;
            if (propName === "ADBE Anchor Point" || propName === "ADBE Point of Interest" || propName === "Point of Interest") {
                if (camera._rejectUnsafePOIAccess) {
                    throw new Error("After Effects error: internal verification failure, sorry! {no current context}");
                }
                return camera._pointOfInterest;
            }
            return genericProperty(propName);
        };
        Object.defineProperty(this, "pointOfInterest", {
            enumerable: true,
            get() {
                if (camera._rejectUnsafePOIAccess) {
                    throw new Error("After Effects error: internal verification failure, sorry! {no current context}");
                }
                return camera._pointOfInterest;
            }
        });
        this.cameraOption = {zoom: this._cameraOptions.property("ADBE Camera Zoom")};
    }
    CameraLayer.prototype = Object.create(AVLayer.prototype);
    CameraLayer.prototype.constructor = CameraLayer;
    CameraLayer.prototype.property = function(groupName) {
        if (groupName === "ADBE Transform Group") return this._transform;
        if (groupName === "ADBE Camera Options Group") return this._cameraOptions;
        return null;
    };

    function CompItem(name, width, height, pixelAspect, duration, frameRate) {
        this.name = name; this.width = width; this.height = height; this.pixelAspect = pixelAspect;
        this.duration = duration; this.frameRate = frameRate; this.parentFolder = null; this.comment = ""; this._layers = [];
        this.layers = {
            add: item => { const layer = new AVLayer(this, item); this._layers.unshift(layer); return layer; },
            addCamera: name => { const layer = new CameraLayer(this, name); this._layers.unshift(layer); return layer; },
            addNull: () => { const layer = new AVLayer(this, null); layer.nullLayer = true; this._layers.unshift(layer); return layer; }
        };
    }
    Object.defineProperty(CompItem.prototype, "numLayers", {get() { return this._layers.length; }});
    CompItem.prototype.layer = function(index) { return this._layers[index - 1]; };
    CompItem.prototype.openInViewer = function() {};
    CompItem.prototype.remove = function() { const i = projectItems.indexOf(this); if (i >= 0) projectItems.splice(i, 1); };

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
        File, Folder, Window, Panel, FolderItem, FootageItem, CompItem, AVLayer, CameraLayer, ImportOptions,
        ImportAsType: {FOOTAGE: 1}, ScriptUI: {newFont() {}}, CutBridgeRevisionManager: Revision, CutBridgeQCPlus: QCPlus,
        alert: message => alerts.push(String(message)), confirm: message => { confirms.push(String(message)); return true; },
        $: {writeln() {}}, app: {project, beginUndoGroup() {}, endUndoGroup() {}, newProject() {}}
    };
    vm.createContext(runtime);
    vm.runInContext(source, runtime);
    // The CommonJS revision core closes over the CommonJS contract. Native AE loads
    // the manager after CutBridge.jsx exports getState(); bridge the same state here.
    Contract.getState = () => runtime.CutBridgeContract.getState();

    function queue(m) { dialogQueue.push(manifestFile(m)); }
    function click(fragment) {
        const button = controls.find(c => c.text.includes(fragment));
        assert.ok(button, `Missing button: ${fragment}`); button.onClick();
    }
    function comps() { return projectItems.filter(x => x instanceof CompItem); }
    function layerByName(comp, name) { return comp._layers.find(layer => layer.name === name); }
    return {runtime, alerts, confirms, queue, click, comps, layerByName};
}

const host = makeHost();
const v1 = manifest(1), v2 = manifest(2), v3 = manifest(3);
const topologyDrift = manifest(2);
topologyDrift.handoff_3d.nulls[0].name = "Renamed_Null";
assert.equal(Revision.assess(v1, topologyDrift).status, "incompatible", "3D topology drift must fail closed before source-only revision");
const sampleTopologyDrift = manifest(2);
sampleTopologyDrift.handoff_3d.camera.samples[1].time += 0.001;
assert.equal(Revision.assess(v1, sampleTopologyDrift).status, "incompatible", "3D sample topology drift must fail closed before source-only revision");

host.queue(v1); host.click("Import Package"); host.click("Build Comp");
const comp = host.comps()[0];
assert.ok(comp, "V001 comp must exist");
assert.equal(comp.numLayers, 3, "V001 must contain camera, null, and BEAUTY");
const beauty = host.layerByName(comp, "BEAUTY");
const camera = host.layerByName(comp, "S13_Camera");
const nullLayer = host.layerByName(comp, "S13_Null");
assert.ok(beauty && camera && nullLayer, "all managed layers must exist");
assert.equal(camera.comment, Contract.managedTag("camera", v1, "S13_Camera"));
assert.equal(nullLayer.comment, Contract.managedTag("null", v1, "S13_Null"));
assert.deepEqual(Array.from(camera.position.keys.at(-1).value), [972, 540, -1000]);
assert.deepEqual(Array.from(camera._pointOfInterest.keys.at(-1).value), [972, 540, 0]);
assert.deepEqual(Array.from(nullLayer.position.keys.at(-1).value), [970, 542, 0]);

// Native AE 26.3x87 diagnostics proved that all named/direct Point-of-Interest
// access paths can trigger an internal C++ assertion in revision context. Keep
// the healthy V001 Build path, then reject every unsafe access form so only
// Transform property index 1 can succeed during revision and rollback.
camera._rejectUnsafePOIAccess = true;

// AE 26.3x87 can assert while removing existing managed 3D keys. A compatible
// revision must overwrite the already-baked key topology without deleting it.
camera.position.rejectKeyRemoval = true;
camera._pointOfInterest.rejectKeyRemoval = true;
camera.cameraOption.zoom.rejectKeyRemoval = true;
nullLayer.position.rejectKeyRemoval = true;
nullLayer.scale.rejectKeyRemoval = true;

host.queue(v2); host.click("Update Revision");
assert.equal(camera.comment, Contract.managedTag("camera", v2, "S13_Camera"), "camera ownership must migrate V001→V002");
assert.equal(nullLayer.comment, Contract.managedTag("null", v2, "S13_Null"), "null ownership must migrate V001→V002");
assert.equal(beauty.comment, Contract.managedTag("layer", v2, "BEAUTY"));
assert.deepEqual(Array.from(camera.position.keys.at(-1).value), [982, 540, -1000], "camera baked data must refresh to V002");
assert.deepEqual(Array.from(camera._pointOfInterest.keys.at(-1).value), [982, 540, 0], "camera POI must refresh to V002 through verified index access");
assert.deepEqual(Array.from(nullLayer.position.keys.at(-1).value), [980, 542, 0], "null baked data must refresh to V002");
assert.deepEqual(Array.from(nullLayer.scale.keys.at(-1).value), [120, 100, 100], "null scale must refresh to V002");
let state = host.runtime.CutBridgeContract.getState();
assert.strictEqual(state.layers[Contract.managedTag("camera", v2, "S13_Camera")], camera);
assert.strictEqual(state.layers[Contract.managedTag("null", v2, "S13_Null")], nullLayer);
assert.equal(state.layers[Contract.managedTag("camera", v1, "S13_Camera")], undefined);
assert.equal(state.layers[Contract.managedTag("null", v1, "S13_Null")], undefined);
host.click("Run QC");
assert.match(host.alerts.at(-1), /CutBridge QC — PASS/, "V002 QC must have zero stale managed tags");

host.queue(v3); host.click("Update Revision");
assert.equal(camera.comment, Contract.managedTag("camera", v3, "S13_Camera"), "camera ownership must migrate V002→V003");
assert.equal(nullLayer.comment, Contract.managedTag("null", v3, "S13_Null"), "null ownership must migrate V002→V003");
assert.equal(beauty.comment, Contract.managedTag("layer", v3, "BEAUTY"));
assert.deepEqual(Array.from(camera.position.keys.at(-1).value), [992, 540, -1000], "camera baked data must refresh to V003");
assert.deepEqual(Array.from(camera._pointOfInterest.keys.at(-1).value), [992, 540, 0], "camera POI must refresh to V003 through verified index access");
assert.deepEqual(Array.from(nullLayer.position.keys.at(-1).value), [990, 542, 0], "null baked data must refresh to V003");
assert.deepEqual(Array.from(nullLayer.scale.keys.at(-1).value), [130, 100, 100], "null scale must refresh to V003");
state = host.runtime.CutBridgeContract.getState();
assert.strictEqual(state.layers[Contract.managedTag("camera", v3, "S13_Camera")], camera);
assert.strictEqual(state.layers[Contract.managedTag("null", v3, "S13_Null")], nullLayer);
assert.equal(comp.numLayers, 3, "revision chaining must not duplicate managed 3D layers");
host.click("Run QC");
assert.match(host.alerts.at(-1), /CutBridge QC — PASS/, "V003 QC must have zero stale managed tags");
assert.ok(!host.alerts.some(x => /stale or foreign CutBridge-managed tag/i.test(x)), "no stale-tag diagnostic may remain after migration");

assert.match(revisionSource, /transform\.property\(1\)/, "revision manager must resolve Camera POI by numeric Transform property index");
assert.doesNotMatch(revisionSource, /transform\.property\("ADBE Anchor Point"\)/, "revision manager must never query Camera Anchor Point by name in native revision context");
assert.doesNotMatch(revisionSource, /safeProperty\(transform,\s*"ADBE Point of Interest"\)/, "revision manager must never query synthetic Camera POI matchName");
assert.doesNotMatch(revisionSource, /safeProperty\(transform,\s*"Point of Interest"\)/, "revision manager must never query Camera POI by display name");
assert.doesNotMatch(revisionSource, /layer\.pointOfInterest/, "revision manager must never use the direct Camera POI getter in native revision context");
console.log("S13 AE 3D revision migration: PASS (verified indexed camera POI + V001→V002→V003 tags + baked samples + QC clean; real AE retest still required)");
