/* S10C Node contract & reconstruction checks. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const root = path.resolve(__dirname, "..");
const source = fs.readFileSync(path.join(root, "apps/after-effects/CutBridge.jsx"), "utf8");
const version = fs.readFileSync(path.join(root, "apps/blender/cutbridge/blender_manifest.toml"), "utf8").match(/^version = "([^"]+)"/m)[1];

let testsPassed = 0;
function test(name, fn) {
    fn();
    testsPassed++;
    console.log("PASS " + name);
}

function validManifestWithHandoff(overrides = {}) {
    return {
        schema: "cutbridge-manifest",
        schema_version: 1,
        cutbridge_version: version,
        project: "PROJ",
        episode: "EP01",
        scene: "SC010",
        cut: "C001",
        take: "T01",
        version: 1,
        package_name: "PROJ_EP01_SC010_C001_T01_V001",
        fps: 24,
        resolution: { width: 1920, height: 1080, pixel_aspect: 1 },
        frames: { start: 1, end: 2, count: 2 },
        passes: [{ name: "BEAUTY", path: "render/beauty", sequence_pattern: "C001_BEAUTY_####.png", required: true }],
        ae: { comp_name: "C001_COMP", layer_order: ["BEAUTY"] },
        handoff_3d: {
            schema: "cutbridge-handoff-3d",
            schema_version: 1,
            space: {
                coordinate_system: "after-effects-composition",
                axis_map: "blender_xyz_to_ae_x_negz_y",
                origin: "composition-center",
                position_units: "pixels",
                pixels_per_blender_unit: 100.0
            },
            sampling: {
                mode: "baked-per-frame",
                frame_start: 1,
                frame_end: 2,
                frame_step: 1
            },
            camera: {
                name: "TestCamera",
                type: "PERSP",
                samples: [
                    {
                        frame: 1,
                        time: 0.0,
                        position: [960.0, 540.0, -1000.0],
                        forward: [0.0, 0.0, 1.0],
                        up: [0.0, -1.0, 0.0],
                        horizontal_fov_radians: 0.691111,
                        ae_zoom: 2666.666
                    },
                    {
                        frame: 2,
                        time: 1.0 / 24.0,
                        position: [960.0, 540.0, -1000.0],
                        forward: [0.0, 0.0, 1.0],
                        up: [0.0, -1.0, 0.0],
                        horizontal_fov_radians: 0.691111,
                        ae_zoom: 2666.666
                    }
                ]
            },
            nulls: [
                {
                    name: "TestNull",
                    source_type: "EMPTY",
                    samples: [
                        {
                            frame: 1,
                            time: 0.0,
                            position: [960.0, 540.0, 0.0],
                            scale: [1.0, 1.0, 1.0]
                        },
                        {
                            frame: 2,
                            time: 1.0 / 24.0,
                            position: [960.0, 540.0, 0.0],
                            scale: [1.0, 1.0, 1.0]
                        }
                    ]
                }
            ]
        }
    };
}

const Contract = require("../apps/after-effects/CutBridge.jsx");

// Test 1: validateManifest with valid handoff_3d
test("validateManifest passes for valid handoff_3d", () => {
    const m = validManifestWithHandoff();
    const errors = Contract.validateManifest(m);
    assert.deepEqual(errors, []);
});

// Test 2: validateHandoff3D fail-closed on malformed schema / version
test("validateHandoff3D rejects unsupported schema or version", () => {
    const m = validManifestWithHandoff();
    m.handoff_3d.schema = "wrong-schema";
    assert.ok(Contract.validateManifest(m).some(e => e.includes("Unsupported handoff_3d schema")));

    m.handoff_3d.schema = "cutbridge-handoff-3d";
    m.handoff_3d.schema_version = 2;
    assert.ok(Contract.validateManifest(m).some(e => e.includes("Unsupported handoff_3d schema_version")));
});

// Test 3: validateHandoff3D fail-closed on unsupported camera type
test("validateHandoff3D rejects non-perspective cameras", () => {
    const m = validManifestWithHandoff();
    m.handoff_3d.camera.type = "ORTHO";
    assert.ok(Contract.validateManifest(m).some(e => e.includes("Unsupported handoff_3d camera type")));
});

// Test 4: validateHandoff3D fail-closed on non-EMPTY null source
test("validateHandoff3D rejects non-EMPTY null objects", () => {
    const m = validManifestWithHandoff();
    m.handoff_3d.nulls[0].source_type = "MESH";
    assert.ok(Contract.validateManifest(m).some(e => e.includes("source_type must be EMPTY")));
});

// Test 5: validateHandoff3D checks coordinates and numbers
test("validateHandoff3D rejects non-finite coordinates", () => {
    const m = validManifestWithHandoff();
    m.handoff_3d.camera.samples[0].position = [NaN, 0, 0];
    assert.ok(Contract.validateManifest(m).some(e => e.includes("position must be an array of 3 finite numbers")));

    m.handoff_3d.camera.samples[0].position = [0, 0, 0];
    m.handoff_3d.camera.samples[0].ae_zoom = -10;
    assert.ok(Contract.validateManifest(m).some(e => e.includes("ae_zoom must be a positive finite number")));
});

// Test 6: managedTag generates distinct, predictable tags
test("managedTag generates distinct camera and null tags", () => {
    const m = validManifestWithHandoff();
    const camTag = Contract.managedTag("camera", m, "TestCamera");
    const nullTag = Contract.managedTag("null", m, "TestNull");
    assert.match(camTag, /^CUTBRIDGE\|1\|camera\|PROJ_EP01_SC010_C001_T01_V001\|TestCamera$/);
    assert.match(nullTag, /^CUTBRIDGE\|1\|null\|PROJ_EP01_SC010_C001_T01_V001\|TestNull$/);
    assert.notEqual(camTag, nullTag);
});

// Test 7: Mock AE Host Lifecycle for Camera & Null Reconstruction
function createMockHost(m, files = []) {
    const normalize = v => path.posix.normalize(decodeURIComponent(String(v).replaceAll("\\", "/")));
    const packageRoot = "/packages/" + m.project;
    const alerts = [];
    const controls = [];
    const projectItems = [];

    function Folder(value) {
        this.fsName = normalize(value);
        this.alias = false;
        this.exists = true;
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
    File.openDialog = () => ({
        parent: new Folder(packageRoot),
        open: () => true,
        read: () => JSON.stringify(m),
        close() {}
    });

    function Window() { this.layout = { resize() {}, layout() {} }; }
    Window.prototype.add = function(type, u, text) {
        const c = { type, text, graphics: { font: { name: "Arial" } }, preferredSize: {} };
        controls.push(c);
        return c;
    };
    Window.prototype.center = Window.prototype.show = function() {};
    function Panel() {}

    function FolderItem(name) {
        this.name = name;
        this.parentFolder = null;
        this.comment = "";
        projectItems.push(this);
    }
    FolderItem.prototype.remove = function() {
        const idx = projectItems.indexOf(this);
        if (idx >= 0) projectItems.splice(idx, 1);
    };

    function FootageItem(file) {
        this.name = "";
        this.parentFolder = null;
        this.comment = "";
        this.file = file;
        this.mainSource = { conformFrameRate: m.fps };
        projectItems.push(this);
    }
    FootageItem.prototype.remove = function() {
        const idx = projectItems.indexOf(this);
        if (idx >= 0) projectItems.splice(idx, 1);
    };

    function Property(name) {
        this.name = name;
        this.value = null;
        this.keys = [];
    }
    Object.defineProperty(Property.prototype, "numKeys", { get() { return this.keys.length; } });
    Property.prototype.setValue = function(v) { this.value = v; };
    Property.prototype.setValueAtTime = function(t, v) {
        this.keys.push({ time: t, value: v });
        this.value = v;
    };
    Property.prototype.removeKey = function(index) {
        this.keys.splice(index - 1, 1);
    };

    function PropertyGroup() {
        this._props = {};
    }
    PropertyGroup.prototype.property = function(name) {
        if (!this._props[name]) this._props[name] = new Property(name);
        return this._props[name];
    };

    function Layer(comp, name) {
        this.containingComp = comp;
        this.comp = comp;
        this.name = name || "";
        this.comment = "";
        this.startTime = 0;
        this.threeDLayer = false;
        this._transform = new PropertyGroup();
        this.position = this._transform.property("ADBE Position");
        this.scale = this._transform.property("ADBE Scale");
    }
    Layer.prototype.property = function(groupName) {
        if (groupName === "ADBE Transform Group") return this._transform;
        return null;
    };
    Layer.prototype.moveToBeginning = function() {
        const list = this.comp._layers, idx = list.indexOf(this);
        if (idx >= 0) { list.splice(idx, 1); list.unshift(this); }
    };
    Layer.prototype.remove = function() {
        const list = this.comp._layers, idx = list.indexOf(this);
        if (idx >= 0) list.splice(idx, 1);
    };

    function AVLayer(comp, sourceItem) {
        Layer.call(this, comp, sourceItem ? sourceItem.name : "");
        this.source = sourceItem;
    }
    AVLayer.prototype = Object.create(Layer.prototype);
    AVLayer.prototype.constructor = AVLayer;

    function CameraLayer(comp, name, center) {
        Layer.call(this, comp, name);
        this._cameraOptions = new PropertyGroup();
        this.pointOfInterest = this._transform.property("ADBE Anchor Point");
        this.cameraOption = { zoom: this._cameraOptions.property("ADBE Camera Zoom") };
    }
    CameraLayer.prototype = Object.create(Layer.prototype);
    CameraLayer.prototype.constructor = CameraLayer;
    CameraLayer.prototype.property = function(groupName) {
        if (groupName === "ADBE Transform Group") return this._transform;
        if (groupName === "ADBE Camera Options Group") return this._cameraOptions;
        return null;
    };

    function CompItem(name, width, height, aspect, duration, fps) {
        this.name = name;
        this.width = width;
        this.height = height;
        this.pixelAspect = aspect;
        this.duration = duration;
        this.frameRate = fps;
        this.parentFolder = null;
        this.comment = "";
        this._layers = [];
        const self = this;
        this.layers = {
            add(sourceItem) {
                const layer = new AVLayer(self, sourceItem);
                self._layers.unshift(layer);
                return layer;
            },
            addCamera(camName, center) {
                const cam = new CameraLayer(self, camName, center);
                self._layers.unshift(cam);
                return cam;
            },
            addNull(dur) {
                const n = new AVLayer(self, null);
                n.nullLayer = true;
                self._layers.unshift(n);
                return n;
            }
        };
        this.openInViewer = () => {};
        projectItems.push(this);
    }
    Object.defineProperty(CompItem.prototype, "numLayers", { get() { return this._layers.length; } });
    CompItem.prototype.layer = function(index) { return this._layers[index - 1]; };
    CompItem.prototype.remove = function() {
        const idx = projectItems.indexOf(this);
        if (idx >= 0) projectItems.splice(idx, 1);
    };

    const project = {
        items: {
            addFolder(name) { const f = new FolderItem(name); return f; },
            addComp(name, w, h, pa, d, fps) { const c = new CompItem(name, w, h, pa, d, fps); return c; }
        },
        rootFolder: { name: "Root" },
        get numItems() { return projectItems.length; },
        item(idx) { return projectItems[idx - 1]; },
        importFile(io) {
            const item = new FootageItem(io.file);
            return item;
        }
    };

    function ImportOptions(f) { this.file = f; }
    ImportOptions.prototype.canImportAs = () => true;

    const sandbox = {
        app: {
            project,
            newProject() {},
            beginUndoGroup() {},
            endUndoGroup() {}
        },
        Folder,
        File,
        FolderItem,
        FootageItem,
        CompItem,
        Layer,
        AVLayer,
        CameraLayer,
        ImportOptions,
        ImportAsType: { FOOTAGE: 1 },
        Window,
        Panel,
        ScriptUI: { newFont: () => {} },
        alert: msg => alerts.push(String(msg)),
        confirm: () => true,
        $: { writeln() {} }
    };

    const ctx = vm.createContext(sandbox);
    vm.runInContext(source, ctx);

    function click(text) {
        const b = controls.find(c => c.type === "button" && c.text.includes(text));
        assert.ok(b, "Button " + text + " not found in UI");
        b.onClick();
    }

    return {
        sandbox,
        project,
        projectItems,
        alerts,
        click,
        comps() { return projectItems.filter(it => it instanceof CompItem); }
    };
}

test("buildComp creates managed camera and nulls with correct keyframes and ordering", () => {
    const m = validManifestWithHandoff();
    const files = [
        "/packages/PROJ/render/beauty/C001_BEAUTY_0001.png",
        "/packages/PROJ/render/beauty/C001_BEAUTY_0002.png"
    ];
    const host = createMockHost(m, files);

    // Click 1. Import Package, then 2. Build Comp
    host.click("1.");
    host.click("2.");

    const comp = host.comps()[0];
    assert.ok(comp, "Comp must be created");
    assert.equal(comp.name, "C001_COMP");
    console.log("ALERTS:", host.alerts); assert.equal(comp.numLayers, 3, "Must have 3 layers: camera, null, beauty");

    // Check layer 1 is Camera
    const layer1 = comp.layer(1);
    assert.equal(layer1.name, "TestCamera");
    assert.equal(layer1.comment, Contract.managedTag("camera", m, "TestCamera"));
    assert.equal(layer1.position.numKeys, 2, "Camera position must have 2 keyframes");
    assert.deepEqual(Array.from(layer1.position.keys[0].value), [960.0, 540.0, -1000.0]);

    // Check layer 2 is Null
    const layer2 = comp.layer(2);
    assert.equal(layer2.name, "TestNull");
    assert.equal(layer2.threeDLayer, true, "Null must be 3D layer");
    assert.equal(layer2.comment, Contract.managedTag("null", m, "TestNull"));
    assert.equal(layer2.position.numKeys, 2, "Null position must have 2 keyframes");
    assert.deepEqual(Array.from(layer2.position.keys[0].value), [960.0, 540.0, 0.0]);

    // Check layer 3 is Footage
    const layer3 = comp.layer(3);
    assert.equal(layer3.name, "BEAUTY");
    assert.equal(layer3.comment, Contract.managedTag("layer", m, "BEAUTY"));

    // Test Idempotent rebuild: click Build Comp again
    host.click("2.");
    console.log("ALERTS:", host.alerts); assert.equal(comp.numLayers, 3, "Rebuilding must not duplicate layers");
});

test("buildComp fails closed if unmanaged camera or null collides by name", () => {
    const m = validManifestWithHandoff();
    const files = [
        "/packages/PROJ/render/beauty/C001_BEAUTY_0001.png",
        "/packages/PROJ/render/beauty/C001_BEAUTY_0002.png"
    ];
    const host = createMockHost(m, files);

    // First build normal comp
    host.click("1.");
    host.click("2.");
    const comp = host.comps()[0];
    assert.ok(comp);

    // Remove managed camera tag to simulate artist camera collision
    const camLayer = comp.layer(1);
    camLayer.comment = ""; // Now unmanaged

    host.click("2.");

    assert.ok(host.alerts.some(a => a.toLowerCase().includes("ambiguous managed camera ownership") || a.includes("managed camera ownership is ambiguous")),
        "Must alert on ambiguous camera collision: " + host.alerts.join(" | "));
    assert.equal(camLayer.comment, "", "Artist camera must NOT be adopted or mutated");
});


console.log(`\nS10C Reconstruction Checks: ALL ${testsPassed} TEST GROUPS PASSED`);

