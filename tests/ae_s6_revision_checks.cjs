const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const R = require("../apps/after-effects/revision_manager.js");
const C = require("../apps/after-effects/CutBridge.jsx");
let groups = 0;
function test(name, fn) { fn(); groups++; console.log("PASS " + name); }
function m(version, overrides = {}) {
    return Object.assign({
        schema: "cutbridge-manifest", schema_version: 1, cutbridge_version: "0.2.3",
        project: "作品", episode: "E01", scene: "S001", cut: "C001", take: "T01",
        package_name: "作品_E01_S001_C001_T01_V" + String(version).padStart(3, "0"),
        version, fps: 24, frames: {start: 0, end: 23, count: 24},
        resolution: {width: 1920, height: 1080, pixel_aspect: 1},
        passes: [
            {name: "BEAUTY", path: "beauty", sequence_pattern: "b####.png", required: true},
            {name: "LINE", path: "line", sequence_pattern: "l####.png", required: false}
        ]
    }, overrides);
}
const clone = value => JSON.parse(JSON.stringify(value));
function fixture(overrides = {}) {
    const current = m(1), next = m(2), render = {}, comp = {}, events = [], imports = [];
    const sources = current.passes.map(p => ({pass: p.name, fps: 24, folder: render, path: p.path}));
    const layers = current.passes.map((p, i) => ({
        type: "AVLayer", comp, tag: C.managedTag("layer", current, p.name),
        source: sources[i], metadata: clone(current), effects: ["artist effect"], masks: ["mask"],
        transform: [1, 2, 3], parent: {name: "artist parent"}, startTime: 0.5,
        blendMode: "multiply", enabled: false
    }));
    const artist = {source: {name: "artist"}, effects: ["manual"]};
    const order = [artist, layers[0], layers[1]];
    const adapter = {
        listManagedLayers() { return layers.map((layer, i) => ({layer, passName: current.passes[i].name})); },
        validateManagedLayer(layer, expected, passName, key) {
            const index = layers.indexOf(layer);
            return index >= 0 && layer.type === "AVLayer" && layer.comp === comp &&
                layer.tag === C.managedTag("layer", expected, passName) &&
                R.ownershipKey(layer.metadata, passName) === key &&
                layer.source === sources[index] && layer.source.folder === render &&
                layer.source.fps === expected.fps && layer.source.path === expected.passes[index].path;
        },
        readSource(layer) { return layer.source; },
        importReplacement(candidate, passName, track) {
            const item = {name: passName, version: candidate.version, valid: true};
            imports.push(item); track(item); events.push("import:" + passName); return item;
        },
        validateReplacement(item) { events.push("validate:" + item.name); return item.valid === true; },
        swapManagedSource(layer, item) { events.push("swap:" + item.name); layer.source = item; },
        restoreManagedSource(layer, source) { events.push("restore:" + source.pass); layer.source = source; },
        removeImportedReplacement(item) { events.push("remove:" + item.name); item.removed = true; return true; },
        commitRevision() { events.push("commit"); return true; }
    };
    Object.assign(adapter, overrides);
    return {current, next, sources, layers, artist, order, imports, events, adapter};
}
test("producer-style V001/V002/V003 names can differ for the same cut", () => {
    assert.equal(R.assess(m(1), m(2)).status, "safe");
    for (const candidates of [[m(2), m(3)], [m(3), m(2)]]) assert.equal(R.selectLatest(m(1), candidates).version, 3);
    assert.equal(R.selectLatest(m(2), [m(1), m(2)]), null);
});
test("all tuple fields reject drift despite equal package_name", () => {
    for (const field of ["project", "episode", "scene", "cut", "take"]) {
        assert.equal(R.assess(m(1), m(2, {[field]: "OTHER", package_name: m(1).package_name})).status, "incompatible");
    }
});
test("delimiter tuples and ownership keys cannot collide", () => {
    const a = m(1, {project: "A|B", episode: "C"});
    const b = m(2, {project: "A", episode: "B|C"});
    assert.notEqual(R.identity(a), R.identity(b));
    assert.equal(R.assess(a, b).status, "incompatible");
    assert.notEqual(R.ownershipKey(m(1), "X"), R.ownershipKey(m(2), "X"));
    assert.notEqual(R.ownershipKey(m(1), "X"), R.ownershipKey(m(1, {cut: "OTHER"}), "X"));
});
test("canonical revision token helper rejects malformed values", () => {
    for (const [value, expected] of [[1, 1], ["V001", 1], ["V002", 2], ["V003", 3], ["V1000", 1000]]) {
        assert.equal(R.revisionNumber(value), expected);
    }
    for (const value of [-1, 0, 1.5, NaN, Infinity, 9007199254740992, "V002draft", "V2", "V0002", "V000", "2", "v002", " V002", {}, null]) {
        assert.ok(Number.isNaN(R.revisionNumber(value)), String(value));
    }
    for (const value of ["V002", -1, 0, 1.5]) assert.equal(R.assess(m(1), m(value)).status, "incompatible");
});
test("duplicate candidate numbers cannot select by input order", () => {
    const a = m(3), b = m(3, {package_name: "other-location"});
    for (const list of [[a, b, m(2)], [b, a, m(2)]]) {
        assert.equal(R.selectLatest(m(1), list), null);
        assert.equal(R.discover(m(1), list).filter(r => r.ambiguous).length, 2);
    }
});
test("malformed manifests fail closed through the existing AE contract", () => {
    for (const candidate of [null, {}, [], m(2, {schema_version: 2}), m(2, {fps: 0}),
        m(2, {frames: {start: 0, end: 23, count: 23}}), m(2, {resolution: {width: -1, height: 1080}}),
        m(2, {package_name: {}})]) assert.equal(R.assess(m(1), candidate).status, "incompatible");
    for (const field of ["project", "episode", "scene", "cut", "take"]) {
        for (const value of ["", " ", null, undefined]) assert.equal(R.assess(m(1), m(2, {[field]: value})).status, "incompatible");
    }
});
test("malformed, duplicate and unsafe passes fail closed", () => {
    for (const passes of [[], [null], [{name: "BEAUTY"}], [m(2).passes[0], m(2).passes[0]],
        [{...m(2).passes[0], path: "../escape"}], [{...m(2).passes[0], required: "yes"}]]) {
        assert.equal(R.assess(m(1), m(2, {passes})).status, "incompatible");
    }
    assert.equal(R.assess(m(1), m(2, {passes: [m(2).passes[1]]})).status, "incompatible");
    assert.equal(R.assess(m(1), m(2, {passes: [m(2).passes[0]]})).status, "warning");
    assert.equal(R.assess(m(1), m(2, {passes: [...m(2).passes, {...m(2).passes[0], name: "NEW"}]})).status, "incompatible");
});
test("prototype pass names remain valid", () => {
    const passes = ["constructor", "__proto__", "toString"].map(name => ({...m(1).passes[0], name}));
    assert.equal(R.assess(m(1, {passes}), m(2, {passes})).status, "safe");
});
test("media changes follow conservative source-only compatibility policy", () => {
    for (const changes of [{fps: 30}, {fps: 24.0001}, {frames: {start: 1, end: 24, count: 24}},
        {resolution: {width: 1920, height: 1080, pixel_aspect: 1.1}},
        {resolution: {width: 2048, height: 1080, pixel_aspect: 1}}]) {
        assert.equal(R.assess(m(1), m(2, changes)).status, "incompatible");
    }
    const next = m(2); next.passes[1].required = true;
    assert.equal(R.assess(m(1), next).status, "warning");
});
test("all validation and rollback callbacks are mandatory", () => {
    const f = fixture();
    for (const name of Object.keys(f.adapter)) {
        const adapter = {...f.adapter}; delete adapter[name];
        assert.throws(() => R.createExecutor(adapter), /Required adapter callback/);
    }
    assert.equal(f.imports.length, 0);
});
test("successful source-only transaction preserves mock layer properties and ordering", () => {
    const f = fixture(), oldOrder = f.order.slice(), before = f.layers.map(l => ({...l}));
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.equal(ex.apply(ticket).replaced, 2);
    assert.deepEqual(f.order, oldOrder);
    for (let i = 0; i < f.layers.length; i++) {
        assert.equal(f.layers[i], oldOrder[i + 1]);
        for (const key of Object.keys(before[i]).filter(k => k !== "source")) assert.equal(f.layers[i][key], before[i][key]);
    }
    assert.ok(f.events.indexOf("validate:LINE") < f.events.indexOf("swap:BEAUTY"));
    assert.equal(f.events[f.events.length - 1], "commit");
    assert.throws(() => ex.apply(ticket), /already applied/);
});
test("warnings require explicit confirmation even if public ticket is modified", () => {
    const f = fixture(); f.next.passes[1].required = true;
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    ticket.requiresConfirmation = false; ticket.status = "safe";
    assert.throws(() => ex.apply(ticket), /explicit confirmation/);
    assert.equal(f.imports.length, 0);
    assert.equal(ex.apply(ticket, true).status, "applied");
});
test("forged tickets and caller changes cannot redirect a plan", () => {
    const f = fixture(), ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply({...ticket}), /Unknown/);
    f.next.passes[0].path = "../escape"; f.next.version = 500;
    ticket.actions = [{layer: f.artist}];
    ex.apply(ticket);
    assert.equal(f.imports[0].version, 2);
    assert.equal(f.artist.source.name, "artist");
});
test("live host ownership rejects forged records, tag/type/container/source and tuple drift", () => {
    for (const mutate of [
        f => f.layers[0].tag = "artist", f => f.layers[0].type = "TextLayer",
        f => f.layers[0].comp = {}, f => f.sources[0].folder = {},
        f => f.sources[0].fps = 30, f => f.layers[0].metadata.cut = "OTHER",
        f => f.layers[0].source = {},
        f => f.adapter.listManagedLayers = () => [{layer: f.artist, passName: "BEAUTY", managed: true, tag: "forged"}]
    ]) {
        const f = fixture(); mutate(f); const ex = R.createExecutor(f.adapter);
        assert.throws(() => ex.prepare(f.current, f.next), /ownership\/source drift/);
        assert.equal(f.imports.length, 0);
    }
});
test("duplicate or missing required live layers block", () => {
    for (const mode of ["duplicate", "missing"]) {
        const f = fixture(), record = {layer: f.layers[0], passName: "BEAUTY"};
        f.adapter.listManagedLayers = () => mode === "duplicate" ? [record, record] : [];
        assert.throws(() => R.createExecutor(f.adapter).prepare(f.current, f.next), /duplicate|Missing required/);
    }
});
test("ownership is checked again after planning and before importing", () => {
    const f = fixture(), ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    f.layers[0].tag = "artist";
    assert.throws(() => ex.apply(ticket), /ownership\/source drift/);
    assert.equal(f.imports.length, 0);
});
test("tag drift during import blocks all source swaps and removes staged imports", () => {
    const f = fixture(), original = f.adapter.importReplacement;
    f.adapter.importReplacement = (...args) => { const item = original(...args); f.layers[0].tag = "artist"; return item; };
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), /ownership\/source drift/);
    assert.equal(f.events.filter(e => e.startsWith("swap")).length, 0);
    assert.ok(f.imports.every(i => i.removed));
});
test("validation failure cleans the failing import as well as earlier staged imports", () => {
    const f = fixture();
    f.adapter.validateReplacement = item => item.name !== "LINE";
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), /Replacement validation failed/);
    assert.ok(f.imports.every(i => i.removed));
    assert.deepEqual(f.layers.map(l => l.source), f.sources);
    assert.equal(f.events.filter(e => e.startsWith("swap")).length, 0);
});
test("import allocation then throw is cleaned via mandatory tracking", () => {
    const f = fixture(), original = f.adapter.importReplacement;
    f.adapter.importReplacement = (...args) => { original(...args); throw Error("import setup failed"); };
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), /import setup failed/);
    assert.ok(f.imports.every(i => i.removed));
});
test("multi-action mutate-then-throw restores every attempted layer", () => {
    const f = fixture(), swap = f.adapter.swapManagedSource;
    f.adapter.swapManagedSource = (layer, item) => { swap(layer, item); if (item.name === "LINE") throw Error("after mutation"); };
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), /after mutation/);
    assert.deepEqual(f.layers.map(l => l.source), f.sources);
    assert.ok(f.imports.every(i => i.removed));
    assert.deepEqual(f.events.filter(e => e.startsWith("restore")), ["restore:LINE", "restore:BEAUTY"]);
});
test("silent swap failure is detected and restored", () => {
    const f = fixture({swapManagedSource() {}});
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), /Source swap verification failed/);
    assert.ok(f.imports.every(i => i.removed));
});
test("restore failure retains all replacements and prevents retry", () => {
    const f = fixture();
    f.adapter.swapManagedSource = (l, item) => { l.source = item; throw Error("after swap"); };
    f.adapter.restoreManagedSource = () => { throw Error("restore unavailable"); };
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    let caught; try { ex.apply(ticket); } catch (e) { caught = e; }
    assert.match(caught.message, /ROLLBACK INCOMPLETE/);
    assert.equal(caught.retainedReplacements, 2);
    assert.ok(f.imports.every(i => !i.removed));
    assert.throws(() => ex.prepare(f.current, f.next), /Rollback incomplete/);
});
test("cleanup failure is explicit and cleanup continues for remaining imports", () => {
    const f = fixture();
    f.adapter.validateReplacement = item => item.name !== "LINE";
    const remove = f.adapter.removeImportedReplacement;
    f.adapter.removeImportedReplacement = item => item.name === "LINE" ? false : remove(item);
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), e => e.retainedReplacements === 1 && /ROLLBACK INCOMPLETE/.test(e.message));
    assert.equal(f.imports[0].removed, true);
    assert.equal(f.imports[1].removed, undefined);
    assert.throws(() => ex.prepare(f.current, f.next), /Rollback incomplete/);
});
test("commit failure rolls back all swapped sources and staged replacements", () => {
    const f = fixture();
    f.adapter.commitRevision = () => { throw Error("metadata write failed"); };
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), /metadata write failed/);
    assert.deepEqual(f.layers.map(l => l.source), f.sources);
    assert.ok(f.imports.every(i => i.removed));
});
test("unprintable removal errors cannot interrupt cleanup or bypass poisoning", () => {
    const f = fixture(), remove = f.adapter.removeImportedReplacement;
    f.adapter.validateReplacement = item => item.name !== "LINE";
    f.adapter.removeImportedReplacement = item => {
        if (item.name === "LINE") throw Object.create(null);
        return remove(item);
    };
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), e => e.retainedReplacements === 1 && /ROLLBACK INCOMPLETE/.test(e.message));
    assert.equal(f.imports[0].removed, true);
    assert.throws(() => ex.prepare(f.current, f.next), /Rollback incomplete/);
});
test("unprintable restore and original errors preserve subsequent recovery attempts", () => {
    const f = fixture(), swap = f.adapter.swapManagedSource, restore = f.adapter.restoreManagedSource;
    f.adapter.swapManagedSource = (layer, item) => { swap(layer, item); if (item.name === "LINE") throw Object.create(null); };
    f.adapter.restoreManagedSource = (layer, source) => {
        if (source.pass === "LINE") throw Object.create(null);
        restore(layer, source);
    };
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    assert.throws(() => ex.apply(ticket), e => e.retainedReplacements === 2 && /ROLLBACK INCOMPLETE/.test(e.message));
    assert.equal(f.layers[0].source, f.sources[0]);
    assert.ok(f.imports.every(i => !i.removed));
    assert.throws(() => ex.prepare(f.current, f.next), /Rollback incomplete/);
});
test("malformed schema coercion cannot abort valid candidate discovery", () => {
    for (const field of ["schema", "schema_version"]) {
        const bad = m(2); bad[field] = JSON.parse('{"toString":null}');
        assert.equal(R.assess(m(1), bad).status, "incompatible");
        assert.equal(R.discover(m(1), [bad, m(3)]).length, 2);
        assert.equal(R.selectLatest(m(1), [m(3), bad]).version, 3);
    }
});
test("removed optional layer remains unchanged", () => {
    const f = fixture(); f.next.passes.pop();
    const ex = R.createExecutor(f.adapter), ticket = ex.prepare(f.current, f.next);
    ex.apply(ticket, true); assert.equal(f.layers[1].source, f.sources[1]);
});
test("missing optional layer promoted to required blocks", () => {
    const f = fixture(); f.next.passes[1].required = true;
    f.adapter.listManagedLayers = () => [{passName: "BEAUTY", layer: f.layers[0]}];
    assert.throws(() => R.createExecutor(f.adapter).prepare(f.current, f.next), /Missing required managed layer/);
});
test("browser/ExtendScript-style loading fails closed without the contract", () => {
    const source = fs.readFileSync(require.resolve("../apps/after-effects/revision_manager.js"), "utf8");
    assert.throws(() => vm.runInNewContext(source, {}), /Load CutBridgeContract/);
    const context = {CutBridgeContract: C};
    vm.runInNewContext(source, context);
    assert.equal(context.CutBridgeRevisionManager.assess(m(1), m(2)).status, "safe");
});
console.log("S6 revision checks: PASS (" + groups + " groups; native AE MANUAL NOT EXECUTED)");
